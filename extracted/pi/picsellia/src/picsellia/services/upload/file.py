import logging
import mimetypes
import os
from pathlib import Path
from uuid import UUID

import requests
from requests import Session

from picsellia import exceptions
from picsellia.services.upload.adapters import (
    AzureUploadAdapter,
    GoogleMultipartUploadAdapter,
    S3MultipartUploadAdapter,
    S3UploadAdapter,
    UploadAdapter,
)
from picsellia.services.upload.platform import PlatformAdapter

logger = logging.getLogger("picsellia")

LARGE_FILE_SIZE = 25 * 1024 * 1024
DEFAULT_TIMEOUT = 30


class FileUploader:
    def __init__(self, connector_id: UUID, session: Session, host: str, headers: dict):
        self.platform_adapter = PlatformAdapter(connector_id, session, host, headers)

    def upload(
        self, object_name: str, path: str | Path
    ) -> tuple[requests.Response, bool, str]:
        is_large, content_type = self._read_file(path)

        if is_large:
            upload = self._upload_large_file(object_name, path, content_type)
        else:
            upload = self._upload_small_file(object_name, path, content_type)

        return upload, is_large, content_type

    def _upload_large_file(
        self,
        object_name: str,
        path: str | Path,
        content_type: str,
    ):
        try:
            response = self.platform_adapter.init_multipart_upload(
                object_name, content_type
            ).json()
            adapter = self._build_multipart_adapter(response)
        except exceptions.BadRequestError:
            logger.warning(
                "This file is large but it is impossible to use multipart for this upload."
                "Trying to upload in only one upload."
            )
            return self._upload_small_file(object_name, path, content_type)

        return adapter.upload(object_name, path, content_type)

    def _upload_small_file(self, object_name: str, path: str | Path, content_type: str):
        response = self.platform_adapter.generate_presigned_url(
            object_name, content_type
        ).json()
        adapter = self._build_adapter(response)
        return adapter.upload(object_name, path, content_type)

    @staticmethod
    def _read_file(path: str | Path) -> tuple[bool, str]:
        if not os.path.isfile(path):
            raise exceptions.FileNotFoundException(f"{path} not found")

        is_large = Path(path).stat().st_size > LARGE_FILE_SIZE
        content_type = mimetypes.guess_type(path, strict=False)[0]
        if content_type is None:
            content_type = "application/octet-stream"

        return is_large, content_type

    def _build_adapter(self, response: dict) -> UploadAdapter:
        if (
            "client_type" not in response
            or "presigned_url_data" not in response
            or "url" not in response["presigned_url_data"]
            or "fields" not in response["presigned_url_data"]
        ):
            raise exceptions.DistantStorageError(
                "Platform could not generate a presigned url to upload this file."
            )

        client_type = response["client_type"].lower()
        url = response["presigned_url_data"]["url"]
        fields = response["presigned_url_data"]["fields"]
        if client_type in ["aws", "minio", "google"]:
            return S3UploadAdapter(self.platform_adapter, url, fields)
        elif client_type == "azure":
            return AzureUploadAdapter(self.platform_adapter, url, fields)
        else:
            raise exceptions.BadRequestError(
                f"This version of SDK cannot upload on {client_type} connector."
            )

    def _build_multipart_adapter(self, response: dict) -> UploadAdapter:
        if "client_type" not in response:
            raise exceptions.BadRequestError(
                "Platform cannot accept a multipart upload for this file."
            )

        client_type = response["client_type"].lower()
        if client_type in ["aws", "minio"]:
            upload_id = response["upload_id"]
            return S3MultipartUploadAdapter(self.platform_adapter, upload_id)
        elif client_type == "google":
            url = response["url"]
            return GoogleMultipartUploadAdapter(self.platform_adapter, url)
        else:
            raise exceptions.BadRequestError(
                f"This version of SDK cannot upload on {client_type} connector."
            )
