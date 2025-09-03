from __future__ import annotations
import uuid
import boto3

from bigeye_sdk.log import get_logger
from bigeye_sdk.functions.file_functs import FileType, WriteDataResult

# create logger
log = get_logger(__name__)


def object_exists(bucket_name: str, object: str) -> bool:
    s3 = boto3.resource('s3')
    # Bucket name we wanna use
    bucket = s3.Bucket(bucket_name)
    # list files matching a filter: the path
    objs = list(bucket.objects.filter(Prefix=object))
    return len(objs) > 0


def generate_unique_s3_object_uri(bucket_name: str, path: str, type: FileType) -> str:
    """
    :param bucket_name: AWS Bucket Name
    :param path: path to add to the object key.
    :return: a unique s3:// object uri.
    """
    object_key = f'{path}/{str(uuid.uuid4())}.{type.name.lower()}'
    return f's3://{bucket_name}/{object_key}'


def truncate_s3(bucket: str, prefix: str = None):
    log.info(f'Truncating s3 data.\nBucket: {bucket}\nPrefix: {prefix}')
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket, Prefix=prefix)

    if 'Contents' in response:
        for o in response['Contents']:
            print('Deleting', o['Key'])
            s3.delete_object(Bucket=bucket, Key=o['Key'])
