# springtownai-rag.py
import boto3

class springtownai-rag:
    def __init__(self):
        self.s3 = boto3.client('s3')

    def download_file(self, bucket_name, key, download_path):
        """
        Download a file from S3.

        :param bucket_name: The name of the S3 bucket.
        :param key: The object key in the S3 bucket (file path in S3).
        :param download_path: The local path to save the downloaded file.
        """
        self.s3.download_file(bucket_name, key, download_path)

