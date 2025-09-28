<?xml version="1.0" encoding="UTF-8"?>
<mxfile host="app.diagrams.net">
  <diagram id="aws_full" name="AWS Facial Recognition - full">
    <mxGraphModel dx="1400" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="827" pageHeight="1169" math="0" shadow="0">
      <root>
        <mxCell id="0" />
        <mxCell id="1" parent="0" />

        <!-- User -->
        <mxCell id="user" value="1. Usuário\n(Browser / App)" style="shape=ellipse;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="40" y="140" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- Auth (Cognito / JWT) -->
        <mxCell id="auth" value="(Auth)\nCognito / JWT" style="shape=rectangle;rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="190" y="140" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- API Gateway -->
        <mxCell id="apigw" value="2. API Gateway\n(REST/HTTP)" style="shape=hexagon;perimeter=hexagonPerimeter2;fillColor=#ffcc99;strokeColor=#d79b00;fontSize=12;" vertex="1" parent="1">
          <mxGeometry x="340" y="140" width="120" height="60" as="geometry" />
        </mxCell>

        <!-- Presigned URL note -->
        <mxCell id="presigned" value="(Opcional) Presigned URL PUT para S3\nreduz carga na Lambda" style="shape=note;fillColor=#fff2cc;strokeColor=#d79b00;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="340" y="210" width="260" height="60" as="geometry" />
        </mxCell>

        <!-- Lambda Ingestão -->
        <mxCell id="lambda1" value="3. Lambda Ingestão\n- gera presigned OR recebe image\n- PutObject S3\n- SendMessage -> SQS main" style="shape=process;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="520" y="120" width="180" height="80" as="geometry" />
        </mxCell>

        <!-- S3 -->
        <mxCell id="s3" value="4. Amazon S3\n(bucket-uploads)\nSSE, lifecycle ttl" style="shape=cylinder;fillColor=#f5f5f5;strokeColor=#666666;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="520" y="240" width="140" height="90" as="geometry" />
        </mxCell>

        <!-- SQS - fila principal -->
        <mxCell id="sqs1" value="5. SQS - fotos_para_processar\n(Standard / FIFO?)" style="shape=parallelogram;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="740" y="100" width="200" height="80" as="geometry" />
        </mxCell>

        <!-- Lambda Processamento -->
        <mxCell id="lambda2" value="6. Lambda Processamento\n- Read S3\n- Rekognition\n- grava DynamoDB\n- Send -> SQS resultados / SNS" style="shape=process;fillColor=#ffe6cc;strokeColor=#d79b00;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="980" y="100" width="220" height="100" as="geometry" />
        </mxCell>

        <!-- Rekognition -->
        <mxCell id="rekog" value="7. Amazon Rekognition\n(DetectFaces / AgeRange)" style="shape=hexagon;perimeter=hexagonPerimeter2;fillColor=#d5e8d4;strokeColor=#82b366;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1240" y="80" width="160" height="80" as="geometry" />
        </mxCell>

        <!-- SQS - resultados -->
        <mxCell id="sqs2" value="8. SQS - resultados_processados\n(pode ser consumida por worker / frontend polling)" style="shape=parallelogram;fillColor=#e1d5e7;strokeColor=#9673a6;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1240" y="200" width="220" height="80" as="geometry" />
        </mxCell>

        <!-- DynamoDB -->
        <mxCell id="ddb" value="9. DynamoDB\n(results_table)\njob_id PK" style="shape=cylinder;fillColor=#dae8fc;strokeColor=#6c8ebf;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="1240" y="320" width="160" height="90" as="geometry" />
        </mxCell>

        <!-- SNS -->
        <mxCell id="sns" value="10. SNS (Notificação)\n(opcional: email / mobile)" style="shape=hexagon;perimeter=hexagonPerimeter2;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="980" y="240" width="160" height="80" as="geometry" />
        </mxCell>

        <!-- SQS DLQ -->
        <mxCell id="sqs_dlq" value="11. SQS - falhas_processamento (DLQ)\n(maxReceiveCount configurado)" style="shape=parallelogram;fillColor=#f8cecc;strokeColor=#b85450;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="740" y="240" width="220" height="80" as="geometry" />
        </mxCell>

        <!-- Observability note -->
        <mxCell id="obs" value="Observability:\nCloudWatch Logs / Alarms / X-Ray" style="shape=note;fillColor=#ffffff;strokeColor=#7f8c8d;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="40" y="340" width="300" height="80" as="geometry" />
        </mxCell>

        <!-- Environments note -->
        <mxCell id="envs" value="Ambientes: dev / hom / main\nStacks separados (sufixos)" style="shape=note;fillColor=#ffffff;strokeColor=#7f8c8d;fontSize=11;" vertex="1" parent="1">
          <mxGeometry x="40" y="440" width="300" height="80" as="geometry" />
        </mxCell>

        <!-- Conexões -->
        <mxCell id="e1" edge="1" parent="1" source="user" target="auth"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e2" edge="1" parent="1" source="auth" target="apigw"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e3" edge="1" parent="1" source="apigw" target="lambda1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e4" edge="1" parent="1" source="lambda1" target="s3"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e5" edge="1" parent="1" source="lambda1" target="sqs1"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e6" edge="1" parent="1" source="sqs1" target="lambda2"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e7" edge="1" parent="1" source="lambda2" target="rekog"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e8" edge="1" parent="1" source="lambda2" target="sqs2"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e9" edge="1" parent="1" source="lambda2" target="ddb"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e10" edge="1" parent="1" source="lambda2" target="sns"><mxGeometry relative="1" as="geometry"/></mxCell>
        <mxCell id="e11" edge="1" parent="1" source="sqs1" target="sqs_dlq" style="dashed=1;strokeColor=#ff0000;"><mxGeometry relative="1" as="geometry"/></mxCell>

      </root>
    </mxGraphModel>
  </diagram>
</mxfile>
