import os
import json
import boto3
import logging

logger = logging.getLogger(__name__)

def send_message_to_sqs(action, type, s3_uri, domain, subdomain, project_type):
    aws_access_key_id = os.environ.get('AWS_ACCESS_KEY_ID', 'AKIAZ7YFAWD6HLD47Z4O')
    aws_secret_access_key = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')
    region_name = os.environ.get('AWS_REGION', 'us-east-1')

    if project_type == 0 or project_type == "0":
        queue_url = os.environ.get('QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/686668427516/ZinleyDeploy')
    elif project_type == 1 or project_type == "1":
        queue_url = os.environ.get('QUEUE_URL', 'https://sqs.us-east-1.amazonaws.com/686668427516/ZinleyReactBuild')
    else:
        logger.error(f"Cannot deploy: Invalid project_type {project_type}")
        return None

    # Create SQS client with credentials
    sqs_client = boto3.client('sqs',
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    
    message_body = json.dumps({
        'action': action,
        'type': type,
        's3_uri': s3_uri,
        'domain': domain,
        'subdomain': subdomain
    })

    logger.debug(queue_url)
    logger.debug(message_body)
    
    response = sqs_client.send_message(
        QueueUrl=queue_url,
        MessageBody=message_body
    )
    return response
