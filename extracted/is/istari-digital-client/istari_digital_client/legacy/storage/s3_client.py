"""Direct S3 transfer support (upload and download) using boto3."""

import io
import logging

try:
    import boto3  # type: ignore[import-not-found,import-untyped]
    from botocore.config import Config as BotoConfig  # type: ignore[import-not-found,import-untyped]
except ImportError:
    boto3 = None
    BotoConfig = None

logger = logging.getLogger("istari_digital_client")


class S3AccessError(Exception):
    """Raised when an S3 operation fails due to permissions."""


class S3Client:
    """Direct S3 transfers (upload and download) using boto3.

    Uses boto3's managed transfer which automatically handles multipart
    with concurrent parts. On first 403 for upload or download, that
    direction is permanently disabled so callers can fall back to
    presigned URLs.
    """

    def __init__(self, bucket_name: str) -> None:
        if boto3 is None:
            raise ImportError(
                "boto3 is required for direct S3 transfer. "
                "Install with: pip install istari-digital-client[s3]"
            )
        self._bucket = bucket_name
        self._client = boto3.client(
            "s3",
            config=BotoConfig(s3={"preferred_transfer_client": "auto"}),
        )
        self._can_head = True
        self.can_upload = True
        self.can_download = True

    def upload(self, key: str, data: bytes) -> None:
        """Upload bytes to S3, skipping if the key already exists.

        Raises S3AccessError on 403 so the caller can fall back.
        """
        if self._can_head:
            try:
                self._client.head_object(Bucket=self._bucket, Key=key)
                logger.debug(
                    "S3 key already exists, skipping upload: bucket=%s key=%s",
                    self._bucket,
                    key,
                )
                return
            except self._client.exceptions.ClientError as exc:
                code = exc.response["Error"]["Code"]
                if code == "403":
                    logger.debug("S3 head_object forbidden, disabling existence checks")
                    self._can_head = False
                elif code != "404":
                    raise

        logger.debug(
            "S3 direct upload: bucket=%s key=%s size=%d", self._bucket, key, len(data)
        )
        try:
            self._client.upload_fileobj(
                Fileobj=io.BytesIO(data),
                Bucket=self._bucket,
                Key=key,
            )
        except self._client.exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "403":
                raise S3AccessError("S3 upload forbidden") from exc
            raise

    def download(self, key: str) -> bytes:
        """Download bytes from S3.

        Raises S3AccessError on 403 so the caller can fall back.
        """
        logger.debug("S3 direct download: bucket=%s key=%s", self._bucket, key)
        buf = io.BytesIO()
        try:
            self._client.download_fileobj(
                Bucket=self._bucket,
                Key=key,
                Fileobj=buf,
            )
        except self._client.exceptions.ClientError as exc:
            if exc.response["Error"]["Code"] == "403":
                raise S3AccessError("S3 download forbidden") from exc
            raise
        return buf.getvalue()
