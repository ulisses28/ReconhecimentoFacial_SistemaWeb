# Projeto: Reconhecimento Facial (Arquitetura e Configuração recomendada)

## Visão Geral
Sistema serverless que recebe imagens via frontend, processa com AWS Rekognition para estimar faixa etária e entrega um feedback ao usuário.
Componentes principais: API Gateway, Lambdas (ingest + process), S3, SQS (3 filas), Rekognition, DynamoDB, SNS.

## Arquitetura (pontos-chave)
- Uso de **S3** para armazenamento de imagens. Ativar SSE (Server Side Encryption) e lifecycle rules para limpeza (ex.: 24h/7d).
- **Presigned URL**: recomendado que a Lambda de ingest gere presigned PUT para S3 em vez de upload direto pela Lambda. Reduz custo e tempo.
- **SQS**: três filas:
  - `fotos_para_processar` (principal) - redrive policy para DLQ.
  - `resultados_processados` - desacopla processamento do consumo dos resultados.
  - `falhas_processamento` - DLQ para mensagens que falharem repetidamente.

## Parâmetros operacionais sugeridos
- **maxReceiveCount (DLQ redrive)**: 3
- **VisibilityTimeout**: >= tempo máximo de execução da Lambda + 30s (ex.: se Lambda pode levar 40s, definir 90s)
- **SQS Type**: Standard (recomendado) a menos que precise de ordenação → FIFO
- **Lambda Batch Size**: 1 (imagens) para evitar timeouts; aumente se fizer bundling e tratar paralelismo
- **S3 Lifecycle**: remover objetos após 24h ou 7d (conforme política de privacidade)
- **DynamoDB TTL**: definir TTL para items, por exemplo 30 dias

## IAM (princípio do menor privilégio)
- **Lambda Ingest**: s3:PutObject (bucket-uploads), sqs:SendMessage (fotos_para_processar)
- **Lambda Process**: s3:GetObject, rekognition:DetectFaces, dynamodb:PutItem/GetItem, sqs:SendMessage (resultados_processados), sqs:ChangeMessageVisibility (se necessário), sns:Publish (opcional)
- **API Gateway**: invoke permissions para Lambdas
- Use roles separados por função/stack e evite chaves permanentes (prefira OIDC/GitHub Actions Roles)

## Observabilidade & Alarmes
- CloudWatch Logs para cada Lambda
- CloudWatch metric filtros: alarmar quando mensagens na DLQ > 0
- X-Ray (opcional) para tracing end-to-end
- SNS para notificação de alerta

## Segurança & Privacidade
- Consentimento claro no frontend antes de capturar imagem
- Criptografia em trânsito (HTTPS) e em repouso (SSE)
- Evitar armazenamento indefinido; limpar imagens e resultados sensíveis
- Controle de acesso (Cognito / JWT)

## Ambientes e CI/CD
- Branches: `dev` (push direto), `hom` (pull request), `main` (produção)
- Stacks separados: `myapp-dev`, `myapp-hom`, `myapp-prod`
- Use GitHub Actions + SAM CLI para deploy; prefira OIDC roles para evitar secrets

## Debug / testes
- Testar imagens corrompidas para validar DLQ
- Testar retry behavior e visibility timeout
- Testes unitários para lambdas (pytest) e integração (simulação local com moto)
