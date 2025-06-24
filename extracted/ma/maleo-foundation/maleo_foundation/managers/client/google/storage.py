import os
from datetime import timedelta
from google.cloud.storage import Bucket, Client
from google.oauth2.service_account import Credentials
from pathlib import Path
from redis.asyncio.client import Redis
from typing import Optional, Union
from maleo_foundation.enums import BaseEnums
from maleo_foundation.types import BaseTypes
from maleo_foundation.utils.logging import SimpleConfig
from .base import GoogleClientManager

class GoogleCloudStorage(GoogleClientManager):
    def __init__(
        self,
        log_config: SimpleConfig,
        service_key: BaseTypes.OptionalString = None,
        credentials: Optional[Credentials] = None,
        credentials_path: Optional[Union[Path, str]] = None,
        bucket_name: BaseTypes.OptionalString = None,
        redis: Optional[Redis] = None
    ) -> None:
        key = "google-cloud-storage"
        name = "GoogleCloudStorage"
        super().__init__(key, name, log_config, service_key, credentials, credentials_path)
        self._client = Client(credentials=self._credentials)
        self._bucket_name = bucket_name or os.getenv("GCS_BUCKET_NAME")
        if self._bucket_name is None:
            self._client.close()
            raise ValueError("GCS_BUCKET_NAME environment variable must be set if 'bucket_name' is set to None")
        self._bucket = self._client.lookup_bucket(bucket_name=self._bucket_name)
        if self._bucket is None:
            self._client.close()
            raise ValueError(f"Bucket '{self._bucket_name}' does not exist.")
        self._root_location = service_key
        self._logger.info("Client manager initialized successfully")
        self._redis = redis

    @property
    def bucket_name(self) -> str:
        return self._bucket_name

    @property
    def bucket(self) -> Bucket:
        return self._bucket

    def dispose(self) -> None:
        if self._client is not None:
            self._logger.info("Disposing client manager")
            self._client.close()
            self._client = None
            self._logger.info("Client manager disposed successfully")

    async def upload(
        self,
        content: bytes,
        location: str,
        content_type: Optional[str]=None,
        make_public: bool=False,
        expiration: BaseEnums=BaseEnums.Expiration.EXP_15MN,
        root_location_override: BaseTypes.OptionalString=None,
        set_in_redis: bool=True
    ) -> str:
        """
        Upload a file to Google Cloud Storage.

        Args:
            content (bytes): The file content as bytes.
            location (str): The path inside the bucket to save the file.
            content_type (Optional[str]): MIME type (e.g., 'image/png').
            make_public (bool): Whether to make the file publicly accessible.

        Returns:
            str: The public URL or blob path depending on `make_public`.
        """
        if root_location_override is None or (isinstance(root_location_override, str) and len(root_location_override) <= 0):
            blob_name = f"{self._root_location}/{location}"
        else:
            blob_name = f"{root_location_override}/{location}"

        blob = self._bucket.blob(blob_name=blob_name)
        blob.upload_from_string(content, content_type=content_type)

        if make_public:
            blob.make_public()
            url = blob.public_url
        else:
            url = blob.generate_signed_url(
                version="v4",
                expiration=timedelta(seconds=int(expiration)),
                method="GET"
            )

        if set_in_redis:
            if make_public:
                await self._redis.set(f"{self.key}:{blob_name}", url)
            else:
                await self._redis.set(f"{self.key}:{blob_name}", url, ex=int(expiration))

        return url

    async def generate_signed_url(
        self,
        location: str,
        expiration: BaseEnums=BaseEnums.Expiration.EXP_15MN,
        root_location_override: BaseTypes.OptionalString = None,
        use_redis: bool = True
    ) -> str:
        """
        generate signed URL of a file in the bucket based on its location.

        Args:
            location: str
                Location of the file inside the bucket

        Returns:
            str: File's pre-signed download url

        Raises:
            ValueError: If the file does not exist
        """
        if use_redis and self._redis is None:
            raise ValueError("Can not use redis. Redis is not initialized")

        if root_location_override is None or (isinstance(root_location_override, str) and len(root_location_override) <= 0):
            blob_name=f"{self._root_location}/{location}"
        else:
            blob_name=f"{root_location_override}/{location}"

        blob = self._bucket.blob(blob_name=blob_name)
        if not blob.exists():
            raise ValueError(f"File '{location}' did not exists.")

        if use_redis:
            if self._redis is None:
                raise ValueError("Can not use redis. Redis is not initialized")
            url = await self._redis.get(f"{self.key}:{blob_name}")
            if url is not None:
                return url

        url = blob.generate_signed_url(
            version="v4",
            expiration=timedelta(seconds=int(expiration)),
            method="GET"
        )
        await self._redis.set(f"{self.key}:{blob_name}", url, ex=int(expiration))
        return url