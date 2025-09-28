# backend/lambda_process/app.py
import os
import json
import boto3
import time

s3 = boto3.client('s3')
rek = boto3.client('rekognition')
dynamo = boto3.resource('dynamodb')
sqs = boto3.client('sqs')
sns = boto3.client('sns')

BUCKET = os.environ['BUCKET']
DDB_TABLE = os.environ['DDB_TABLE']
SQS_RESULTS_URL = os.environ.get('SQS_RESULTS_URL')
SNS_TOPIC_ARN = os.environ.get('SNS_TOPIC_ARN')

def lambda_handler(event, context):
    table = dynamo.Table(DDB_TABLE)
    for record in event['Records']:
        body = json.loads(record['body'])
        job_id = body.get('job_id') or body.get('s3_key', '')  # adapte conforme mensagem enviada
        s3_key = body.get('s3_key')
        try:
            # Chamar rekognition
            resp = rek.detect_faces(Image={'S3Object': {'Bucket': BUCKET, 'Name': s3_key}}, Attributes=['ALL'])
            if resp['FaceDetails']:
                face = resp['FaceDetails'][0]
                age_low = face['AgeRange']['Low']
                age_high = face['AgeRange']['High']
            else:
                age_low = None
                age_high = None

            item = {
                'job_id': job_id,
                's3_key': s3_key,
                'age_low': age_low,
                'age_high': age_high,
                'timestamp': int(time.time()),
            }
            table.put_item(Item=item)

            # enviar msg para resultados
            if SQS_RESULTS_URL:
                sqs.send_message(QueueUrl=SQS_RESULTS_URL, MessageBody=json.dumps(item))
            if SNS_TOPIC_ARN:
                sns.publish(TopicArn=SNS_TOPIC_ARN, Message=json.dumps(item))
        except Exception as e:
            print("Erro processando:", e)
            raise e  # faz com que SQS reenvie até DLQ
