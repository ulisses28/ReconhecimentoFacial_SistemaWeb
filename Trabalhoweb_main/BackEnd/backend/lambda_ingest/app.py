# backend/lambda_ingest/app.py
import os
import json
import boto3
import uuid
from datetime import datetime, timedelta

s3 = boto3.client('s3')
sqs = boto3.client('sqs')

BUCKET = os.environ['BUCKET']          # definido pelo SAM
SQS_URL = os.environ['SQS_URL']

def lambda_handler(event, context):
    # Ex.: cliente solicita presigned URL (POST /ingest body: { "filename": "img.jpg" })
    body = json.loads(event.get('body') or "{}")
    filename = body.get('filename') or f"{uuid.uuid4()}.jpg"
    key = f"uploads/{filename}"
    # Gera presigned PUT URL
    presigned = s3.generate_presigned_url(
        'put_object',
        Params={'Bucket': BUCKET, 'Key': key, 'ContentType': 'image/jpeg'},
        ExpiresIn=300
    )
    # Envolver job info: o cliente fará PUT direto e depois chamará /notify (ou podemos detectar via S3 event)
    job_id = str(uuid.uuid4())
    # Retorna presigned e job_id ao front
    return {
        "statusCode": 200,
        "body": json.dumps({"job_id": job_id, "presigned_url": presigned, "s3_key": key})
    }
