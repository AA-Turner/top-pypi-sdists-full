import abc
import os
from io import BufferedReader
from typing import BinaryIO

import requests

from picsellia.decorators import retry
from picsellia.services.upload.platform import PlatformAdapter

CHUNK_SIZE = 25 * 1024 * 1024
DEFAULT_TIMEOUT = 30


class UploadAdapter(abc.ABC):
    def __init__(self, platform_adapter: PlatformAdapter):
        self.platform_adapter = platform_adapter
        self.session = self.platform_adapter.session

    @abc.abstractmethod
    def upload(self, object_name: str, path: str, content_type: str):
        pass


class S3UploadAdapter(UploadAdapter):
    def __init__(self, platform_adapter: PlatformAdapter, url: str, fields: dict):
        super().__init__(platform_adapter)
        self.url = url
        self.fields = fields

    @retry((requests.ReadTimeout, requests.ConnectionError))
    def upload(
        self, object_name: str, path: str, content_type: str
    ) -> requests.Response:
        with open(path, "rb") as file:
            url = self.url
            data = {**self.fields, "Content-Type": content_type}
            response = self.session.post(
                url=url,
                data=data,
                files={"file": (object_name, file)},
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            return response


class AzureUploadAdapter(UploadAdapter):
    def __init__(self, platform_adapter: PlatformAdapter, url: str, fields: dict):
        super().__init__(platform_adapter)
        self.url = url
        self.fields = fields

    @retry((requests.ReadTimeout, requests.ConnectionError))
    def upload(
        self, object_name: str, path: str, content_type: str
    ) -> requests.Response:
        with open(path, "rb") as file:
            url = self.url
            headers = {
                **self.fields,
                "Content-Type": content_type,
                "x-ms-blob-type": "BlockBlob",
            }
            response = self.session.put(
                url=url,
                data=file.read(),
                headers=headers,
                timeout=DEFAULT_TIMEOUT,
            )
            response.raise_for_status()
            return response


class S3MultipartUploadAdapter(UploadAdapter):
    def __init__(self, platform_adapter: PlatformAdapter, upload_id: str):
        super().__init__(platform_adapter)
        self.upload_id = upload_id

    def upload(
        self, object_name: str, path: str, content_type: str
    ) -> requests.Response:
        file_size = os.path.getsize(path)
        chunk_count = int(file_size / CHUNK_SIZE) + 1
        parts = []
        with open(path, "rb") as file:
            for part in range(1, chunk_count + 1):
                etag = self._upload_part(object_name, part, file)
                parts.append({"ETag": etag, "PartNumber": part})

        additional_payload = {
            "upload_id": self.upload_id,
            "parts": parts,
        }
        return self.platform_adapter.complete_part_upload(
            object_name, additional_payload
        )

    def _upload_part(
        self,
        object_name: str,
        part: int,
        file: BufferedReader | BinaryIO,
    ):
        additional_payload = {
            "upload_id": self.upload_id,
            "part_no": part,
        }
        url = self.platform_adapter.generate_part_presigned_url(
            object_name, additional_payload
        ).json()["url"]
        file_data = file.read(CHUNK_SIZE)
        response = self._put_part_with_retry(url, file_data)
        response.raise_for_status()
        return response.headers["ETag"]

    @retry((requests.ReadTimeout, requests.ConnectionError))
    def _put_part_with_retry(self, url: str, file_data: bytes):
        return self.session.put(url, data=file_data, timeout=DEFAULT_TIMEOUT)


class GoogleMultipartUploadAdapter(UploadAdapter):
    def __init__(self, platform_adapter: PlatformAdapter, url: str):
        super().__init__(platform_adapter)
        self.url = url

    def upload(
        self, object_name: str, path: str, content_type: str
    ) -> requests.Response:
        file_size = os.path.getsize(path)
        with open(path, "rb") as file:
            start = 0
            while start < file_size:
                chunk = file.read(CHUNK_SIZE)
                end = min(start + len(chunk) - 1, file_size - 1)
                content_length = end - start + 1
                headers = {
                    "Content-Length": str(content_length),
                    "Content-Range": f"bytes {start}-{end}/{file_size}",
                }
                response = self._put_part_with_retry(chunk, headers)
                response.raise_for_status()

                start = end + 1

            return response

    @retry((requests.ReadTimeout, requests.ConnectionError))
    def _put_part_with_retry(self, chunk: bytes, headers: dict):
        return self.session.put(
            url=self.url,
            data=chunk,
            headers=headers,
            timeout=DEFAULT_TIMEOUT,
        )
