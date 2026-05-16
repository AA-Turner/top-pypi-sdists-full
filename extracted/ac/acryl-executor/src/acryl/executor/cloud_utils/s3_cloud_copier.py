import logging
from typing import Optional

import boto3

from acryl.executor.cloud_utils.cloud_copier import CloudCopier

logger = logging.getLogger(__name__)


class S3CloudCopier(CloudCopier):
    """``CloudCopier`` implementation that uploads files to Amazon S3.

    Credentials are resolved in order:
    1. Explicit ``aws_access_key_id`` / ``aws_secret_access_key`` / ``aws_session_token``
       passed to the constructor (typically fetched from DataHub's executor config).
    2. The default boto3 credential chain (environment variables, ``~/.aws/credentials``,
       EC2 instance profile, etc.) when no explicit credentials are supplied.
    """

    log = logging.getLogger(__name__)

    def __init__(
        self,
        bucket: str,
        base_path: str,
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        aws_session_token: Optional[str] = None,
        region_name: Optional[str] = None,
    ) -> None:
        """Initialise the copier.

        Args:
            bucket: Name of the target S3 bucket.
            base_path: Key prefix applied to every uploaded object.
            aws_access_key_id: Optional explicit AWS access key.
            aws_secret_access_key: Optional explicit AWS secret key.
            aws_session_token: Optional STS session token.
            region_name: Optional AWS region (e.g. ``"us-east-1"``).
        """
        self.bucket = bucket
        self.base_path = base_path

        # Create boto3 session with provided credentials or use default chain.
        self.session = boto3.session.Session(
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            aws_session_token=aws_session_token,
            region_name=region_name,
        )

    def upload(self, source_local_file: str, target_cloud_file: str) -> str:
        """Upload a local file to S3 and return its URI.

        The final S3 key is ``{base_path}/{target_cloud_file}`` with redundant
        slashes normalised.

        Args:
            source_local_file: Absolute path of the local file to upload.
            target_cloud_file: Relative key suffix appended to ``base_path``.

        Returns:
            The ``s3://`` URI of the uploaded object.

        Raises:
            Exception: Propagated from boto3 if the upload fails.
        """
        s3 = self.session.resource("s3")

        key = self.base_path.rstrip("/") + "/" + target_cloud_file.lstrip("/")
        logger.info(
            f"Uploading {source_local_file} to bucket: {self.bucket} and base path {self.base_path} and key {key}"
        )
        s3.meta.client.upload_file(
            Filename=source_local_file,
            Bucket=self.bucket,
            Key=key,
        )
        return f"s3://{self.bucket}/{key}"
