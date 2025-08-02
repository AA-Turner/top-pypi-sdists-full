import json
from io import BytesIO
from typing import Optional

import pandas as pd
from google.cloud import storage
from qwak.clients.secret_service import SecretServiceClient

from qwak_inference.batch_client.file_serialization import SerializationFormat
from qwak_inference.batch_client.s3 import S3Utils

AWS_TYPE = "AWS"
GCP_TYPE = "GCP"
DEFAULT_ENVIRONMENT_CLOUD = "default"


class CloudProviderClient:
    def __init__(
        self,
        access_key_secret: Optional[str] = None,
        secret_access_key_secret: Optional[str] = None,
        aws_user_role_arn: Optional[str] = None,
        service_account_key_secret_name: Optional[str] = None,
    ):
        self.access_key_secret = access_key_secret
        self.secret_access_key_secret = secret_access_key_secret
        self.aws_user_role_arn = aws_user_role_arn
        self.service_account_key_secret_name = service_account_key_secret_name
        self.cloud_provider_type = self._get_cloud_type()
        self.secret_service_client = SecretServiceClient()
        self.cloud_storage_client = (
            self._get_gcs_client()
            if self.cloud_provider_type == GCP_TYPE
            else self._get_s3_client()
        )

    def _get_cloud_type(self):
        if self.service_account_key_secret_name:
            return GCP_TYPE
        elif self.secret_access_key_secret or self.access_key_secret:
            return AWS_TYPE
        else:
            return DEFAULT_ENVIRONMENT_CLOUD

    def _get_s3_client(self):
        if self.access_key_secret:
            aws_access_key_id = self.secret_service_client.get_secret(
                self.access_key_secret
            )
            aws_secret_access_key = self.secret_service_client.get_secret(
                self.secret_access_key_secret
            )
            return S3Utils.get_client(aws_access_key_id, aws_secret_access_key)
        else:
            return None

    def _get_gcs_client(self):
        """
        Get GCS client with session credentials by json key string
        Returns: GCS client

        """
        json_string = self.secret_service_client.get_secret(
            self.service_account_key_secret_name
        )
        json_dict = json.loads(json_string)
        storage_client = storage.Client.from_service_account_info(json_dict)
        return storage_client

    def upload_data_to_storage(self, body, bucket: str, path: str):
        """
        Upload data to cloud storage
        Args:
            body: Data to be uploaded
            bucket: Bucket name
            path: Path in the bucket

        """
        if self.cloud_provider_type == GCP_TYPE:
            bucket = self.cloud_storage_client.bucket(bucket)
            blob = bucket.blob(path)
            blob.upload_from_string(body)
        else:
            self.cloud_storage_client.put_object(
                Body=body,
                Bucket=bucket,
                Key=path,
            )

    def _get_s3_files_to_df(
        self, prefix: str, bucket: str, serde_handler: SerializationFormat
    ):
        objects = self.cloud_storage_client.list_objects(
            Bucket=bucket,
            Prefix=prefix,
        )
        dfs = []
        for object in objects["Contents"]:
            response = self.cloud_storage_client.get_objects(
                bucket=bucket, key=f"{object['Key']}"
            )
            dfs.append(
                serde_handler.read_df(
                    BytesIO(b"".join(response.get("Body").readlines()))
                )
            )
        return pd.concat(dfs, axis=0, ignore_index=True)

    def _get_gcs_files_to_df(
        self, prefix: str, bucket: str, serde_handler: SerializationFormat
    ):
        bucket = self.cloud_storage_client.bucket(bucket)
        blobs = bucket.list_blobs(prefix=prefix)
        dfs = []
        for blob in blobs:
            df = serde_handler.read_df(BytesIO(blob.download_as_string()))
            dfs.append(df)
        return pd.concat(dfs, axis=0, ignore_index=True)

    def get_files_to_df(
        self, prefix: str, bucket: str, serde_handler: SerializationFormat
    ):
        if self.cloud_provider_type == GCP_TYPE:
            return self._get_gcs_files_to_df(
                prefix=prefix, bucket=bucket, serde_handler=serde_handler
            )
        else:
            return self._get_s3_files_to_df(
                prefix=prefix, bucket=bucket, serde_handler=serde_handler
            )
