from __future__ import annotations

import asyncio
import enum
import io
import os
import pathlib
import shutil
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from typing import (
    IO,
    TYPE_CHECKING,
    AsyncIterator,
    BinaryIO,
    Callable,
    ClassVar,
    Iterable,
    Mapping,
    Optional,
    Protocol,
    cast,
    overload,
)

import pyarrow.parquet as pq
from typing_extensions import assert_never, override

from chalk.utils.async_helpers import to_async_iterable
from chalk.utils.collections import unwrap_optional
from chalk.utils.log_with_context import get_logger
from chalk.utils.missing_dependency import missing_dependency_exception
from chalk.utils.tracing import safe_distribution, safe_incr, safe_trace

if TYPE_CHECKING:
    import google.cloud.storage
    import pyarrow as pa
    from fsspec import AbstractFileSystem
    from mypy_boto3_s3.client import S3Client


_logger = get_logger(__name__)


class _IOWithLen(io.BytesIO):
    def __len__(self):
        return len(self.getvalue())


class SignedUrlMode(enum.Enum):
    """Download or upload mode when requesting a signed URL"""

    DOWNLOAD = enum.auto()
    UPLOAD = enum.auto()


class StorageClient(Protocol):
    """Interface for a gcs / s3 client"""

    ...
    protocol: ClassVar[str]
    """The protocol for this storage client"""

    bucket: str
    """The bucket for this storage client"""

    fs: AbstractFileSystem
    """The fsspec filesystem for this storage client, e.g. used for parquet file metadata reading"""

    def upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        """Upload ``data`` to the ``filename``"""
        ...

    async def async_upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        ...

    def get_uri(self, filename: str) -> str:
        """Return a URI for a filename"""
        return f"{self.protocol}://{self.bucket}/{filename}"

    def get_filename(self, uri: str):
        """Return a filename for a uri"""
        return uri.replace(f"{self.protocol}://{self.bucket}/", "")

    def get_directory(self, uri: str):
        """NB: pathlib changes protocol strings"""
        return os.path.dirname(uri)

    @overload
    def download_object(self, filename: str) -> bytes:
        """Download ``filename`` and return the contents as bytes"""
        ...

    @overload
    def download_object(self, filename: str, destination: BinaryIO | str) -> None:
        """Download ``bucket/filename`` to the destination, which can either be an io object or a filepath"""
        ...

    @overload
    async def async_download_object(self, filename: str) -> bytes:
        """Download ``filename`` and return the contents as bytes"""
        ...

    @overload
    async def async_download_object(self, filename: str, destination: BinaryIO | str) -> None:
        """Download ``bucket/filename`` to the destination, which can either be an io object or a filepath"""
        ...

    def sign_url(
        self,
        filename: str,
        expiration: datetime,
        mode: SignedUrlMode,
        response_disposition: str | None = None,
    ) -> str:
        """
        Generate a signed url for ``filename`` that expires at ``expiration``
        """
        ...

    def list_files(self, prefix: str, delimiter: Optional[str] = None) -> Iterable[str]:
        """
        Yield filenames from the bucket that begin with the given prefix.
        Please use 'async_list_files` when possible (in an async function)
        """
        ...

    def async_list_files(self, prefix: str, delimiter: Optional[str] = None) -> AsyncIterator[str]:
        ...

    def copy(self, source_filename: str, dest_filename: str) -> None:
        """Copy ``source_filename`` to dest_filename``, including all metadata"""
        ...

    def get_file_size(self, filename: str) -> int:
        """Get the file size, in bytes"""
        ...


class ParquetStorageClient:
    def __init__(self, fs: AbstractFileSystem, file_normalizer_fn: Callable[[str], str]):
        super().__init__()
        self.fs = fs
        self.file_normalizer_fn = file_normalizer_fn

    def _get_parquet_lazy(self, filename: str) -> pq.ParquetFile:
        normalized_filename = self.file_normalizer_fn(filename)
        with self.fs.open(normalized_filename, "rb") as f:
            return pq.ParquetFile(f)

    def get_num_rows_parquet(self, filename: str) -> int:
        parquet_file = self._get_parquet_lazy(filename)
        assert parquet_file.metadata is not None, "no parquet metadata found"
        return parquet_file.metadata.num_rows

    def get_schema_parquet(self, filename: str) -> pa.Schema:
        parquet_file = self._get_parquet_lazy(filename)
        return parquet_file.schema_arrow

    @classmethod
    def from_storage_client(cls, storage_client: StorageClient):
        return cls(fs=storage_client.fs, file_normalizer_fn=storage_client.get_uri)


class GCSStorageClient(StorageClient):
    protocol = "gs"

    def __init__(
        self,
        gcs_client: google.cloud.storage.Client,
        gcs_executor: ThreadPoolExecutor,
        bucket: str,
    ):
        super().__init__()
        try:
            import gcsfs
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        self.bucket = bucket
        self._gcs_client = gcs_client
        self._gcs_executor = gcs_executor
        self._bucket = self._gcs_client.bucket(bucket)
        self.fs = gcsfs.GCSFileSystem()

    @override
    def upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        if isinstance(data, bytes):
            data = io.BytesIO(data)
        assert isinstance(data, io.IOBase)
        data.seek(0, os.SEEK_END)
        num_bytes = data.tell()
        data.seek(0)
        file_uri = self.get_uri(filename)
        blob = self._bucket.blob(filename)
        blob.metadata = metadata
        _logger.debug(f"Uploading file '{file_uri}' of size {num_bytes} bytes")

        from tenacity import RetryCallState, Retrying, stop_after_attempt, wait_fixed

        def _log_upload_retry(state: RetryCallState) -> None:
            if state.outcome is not None:
                safe_incr(
                    counter="chalk.engine.gcs_bulk_upload_output.retry",
                    value=state.attempt_number,
                    tags=[f"success:{not state.outcome.failed}"],
                )

        # Empirically this appears to fail occasionally, so let's just try it five times.
        # FIXME: Configure the retrying on the google storage client, instead of doing our own wrapper around it
        for attempt in Retrying(
            stop=stop_after_attempt(5),
            reraise=True,
            wait=wait_fixed(3),
            after=_log_upload_retry,
        ):
            # matters for retries
            data.seek(0)
            with attempt:
                with safe_trace(
                    "CloudStorageBulkUploadOutput.do_upload",
                    attributes={
                        "size_bytes": str(num_bytes),
                        "file_uri": file_uri,
                    },
                ):
                    # Not using the actual filename in the tag to avoid tag blowup
                    safe_distribution(
                        "chalk.engine.storage_client.files_uploaded",
                        1,
                        tags=[f"bucket:{self.bucket}", f"protocol:{self.protocol}"],
                    )
                    safe_distribution(
                        "chalk.engine.storage_client.bytes_uploaded",
                        num_bytes,
                        tags=[f"bucket:{self.bucket}", f"protocol:{self.protocol}"],
                    )
                    blob.upload_from_file(
                        data,
                        size=num_bytes,
                        content_type=content_type,
                        if_generation_match=blob.generation,
                    )

    @overload
    @override
    def download_object(self, filename: str) -> bytes:
        ...

    @overload
    @override
    def download_object(self, filename: str, destination: BinaryIO | str) -> None:
        ...

    @override
    def download_object(self, filename: str, destination: str | BinaryIO | None = None) -> bytes | None:
        blob = self._bucket.blob(filename)
        if destination is None:
            return blob.download_as_bytes()
        elif isinstance(destination, str):
            blob.download_to_filename(destination)
        else:
            blob.download_to_file(destination)

    async def async_upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        return await asyncio.get_running_loop().run_in_executor(
            self._gcs_executor,
            self.upload_object,
            filename,
            content_type,
            data,
            metadata,
        )

    @overload
    @override
    async def async_download_object(self, filename: str) -> bytes:
        ...

    @overload
    @override
    async def async_download_object(self, filename: str, destination: BinaryIO | str) -> None:
        ...

    @override
    async def async_download_object(self, filename: str, destination: str | BinaryIO | None = None) -> bytes | None:
        if destination is None:
            return cast(
                None,
                await asyncio.get_running_loop().run_in_executor(self._gcs_executor, self.download_object, filename),
            )
        else:
            return await asyncio.get_running_loop().run_in_executor(
                self._gcs_executor, self.download_object, filename, destination
            )

    def sign_url(
        self,
        filename: str,
        expiration: datetime,
        mode: SignedUrlMode,
        response_disposition: str | None = None,
    ) -> str:
        blob = self._bucket.blob(filename)
        if mode == SignedUrlMode.DOWNLOAD:
            method = "GET"
        elif mode == SignedUrlMode.UPLOAD:
            method = "PUT"
        else:
            assert_never(mode)
        try:
            return blob.generate_signed_url(
                expiration=expiration,
                method=method,
                version="v4",
                response_disposition=response_disposition,
            )
        except Exception as e:
            _logger.error(
                f"Failed to create signed url for '{filename}'; falling back to storage client URL",
                exc_info=e,
            )

        return self.get_uri(filename)

    def list_files(self, prefix: str, delimiter: Optional[str] = None) -> Iterable[str]:
        blobs = self._gcs_client.list_blobs(self.bucket, prefix=prefix, delimiter=delimiter)
        for blob in blobs:
            yield blob.name

    async def async_list_files(self, prefix: str, delimiter: Optional[str] = None) -> AsyncIterator[str]:
        iterable = await asyncio.get_running_loop().run_in_executor(
            self._gcs_executor, self.list_files, prefix, delimiter
        )
        async for filename in to_async_iterable(iterable, self._gcs_executor):
            yield filename

    def copy(self, source_filename: str, dest_filename: str) -> None:
        blob = self._bucket.blob(source_filename)
        self._bucket.copy_blob(blob, destination_bucket=self._bucket, new_name=dest_filename)

    def get_file_size(self, filename: str) -> int:
        blob = self._bucket.get_blob(filename)
        assert blob is not None
        size = blob.size
        assert size is not None
        return size


class S3StorageClient(StorageClient):
    protocol = "s3"

    def __init__(
        self,
        bucket: str,
        s3_client: S3Client,
        executor: ThreadPoolExecutor,
        aws_region: str | None = None,
    ) -> None:
        super().__init__()
        try:
            import s3fs
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        self.bucket = bucket
        self._s3_client = s3_client
        self._executor = executor
        region = aws_region or os.environ.get("AWS_DEFAULT_REGION")
        _logger.info(f"AWS storage client using {region=}")
        self.fs = s3fs.S3FileSystem(
            client_kwargs={"region_name": region},
        )

    def upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        if not isinstance(data, bytes):
            data.seek(0)
            data = data.read()
        assert isinstance(data, bytes)
        wrapped_data = _IOWithLen(
            data
        )  # boto3 wants to call len() the io, manually wrapping it in a class that supports that
        if metadata is None:
            metadata = {}
        # Not using the actual filename in the tag to avoid tag blowup
        safe_distribution(
            "chalk.engine.storage_client.files_uploaded",
            1,
            tags=[f"bucket:{self.bucket}", f"protocol:{self.protocol}"],
        )
        safe_distribution(
            "chalk.engine.storage_client.bytes_uploaded",
            len(data),
            tags=[f"bucket:{self.bucket}", f"protocol:{self.protocol}"],
        )

        if len(wrapped_data) <= 5 * 1024 * 1024 - 1000:  # 5MB is the limit for a single PUT request
            self._s3_client.put_object(
                Bucket=self.bucket,
                Key=filename,
                Body=wrapped_data,
                ContentType=content_type,
                Metadata=metadata,
            )
        else:
            # Multipart upload
            multipart_upload = self._s3_client.create_multipart_upload(
                Bucket=self.bucket,
                Key=filename,
                ContentType=content_type,
                Metadata=metadata,
            )
            upload_id = multipart_upload["UploadId"]
            part_size = 100 * 1024 * 1024  # 100MB
            parts = []

            for i in range(0, len(data), part_size):
                part_number = i // part_size + 1
                part_data = data[i : i + part_size]
                part = self._s3_client.upload_part(
                    Bucket=self.bucket,
                    Key=filename,
                    PartNumber=part_number,
                    UploadId=upload_id,
                    Body=part_data,
                )
                parts.append(
                    {
                        "PartNumber": part_number,
                        "ETag": part["ETag"],
                    }
                )

            self._s3_client.complete_multipart_upload(
                Bucket=self.bucket,
                Key=filename,
                UploadId=upload_id,
                MultipartUpload={"Parts": parts},
            )

    @overload
    @override
    def download_object(self, filename: str) -> bytes:
        ...

    @overload
    @override
    def download_object(self, filename: str, destination: BinaryIO | str) -> None:
        ...

    def _download_to_file(self, filename: str, output_filename: str):
        self._s3_client.download_file(
            Bucket=self.bucket,
            Key=filename,
            Filename=output_filename,
        )

    def _download_to_fileobj(self, filename: str, output_file: IO):
        self._s3_client.download_fileobj(
            Bucket=self.bucket,
            Key=filename,
            Fileobj=output_file,
        )

    @override
    def download_object(self, filename: str, destination: str | BinaryIO | None = None) -> bytes | None:
        if isinstance(destination, str):
            self._download_to_file(filename, destination)
            return
        if destination is None:
            destination = io.BytesIO()
            self._download_to_fileobj(filename, destination)
            destination.seek(0)
            return destination.read()
        else:
            self._download_to_fileobj(filename, destination)

    async def async_upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        return await asyncio.get_running_loop().run_in_executor(
            self._executor, self.upload_object, filename, content_type, data, metadata
        )

    @overload
    @override
    async def async_download_object(self, filename: str) -> bytes:
        ...

    @overload
    @override
    async def async_download_object(self, filename: str, destination: BinaryIO | str) -> None:
        ...

    @override
    async def async_download_object(self, filename: str, destination: str | BinaryIO | None = None) -> bytes | None:
        if destination is None:
            return cast(
                None,
                await asyncio.get_running_loop().run_in_executor(self._executor, self.download_object, filename),
            )
        else:
            return await asyncio.get_running_loop().run_in_executor(
                self._executor, self.download_object, filename, destination
            )

    def sign_url(
        self,
        filename: str,
        expiration: datetime,
        mode: SignedUrlMode,
        response_disposition: str | None = None,
    ) -> str:
        expiration_secs = (expiration - datetime.now(timezone.utc)).total_seconds()
        if expiration_secs <= 0:
            raise ValueError("Expiration time is in the past")
        params = {"Bucket": self.bucket, "Key": filename}
        if response_disposition is not None:
            params["ResponseContentDisposition"] = response_disposition
        if mode == SignedUrlMode.DOWNLOAD:
            client_method = "get_object"
        elif mode == SignedUrlMode.UPLOAD:
            client_method = "put_object"
        else:
            assert_never(mode)
        return self._s3_client.generate_presigned_url(
            ClientMethod=client_method,
            Params=params,
            ExpiresIn=int(expiration_secs),
        )

    def list_files(self, prefix: str, delimiter: Optional[str] = None) -> Iterable[str]:
        try:
            if delimiter is None:
                continuation_token = None
                while True:
                    if continuation_token is None:
                        resp = self._s3_client.list_objects_v2(
                            Bucket=self.bucket,
                            Prefix=prefix,
                        )
                    else:
                        resp = self._s3_client.list_objects_v2(
                            Bucket=self.bucket,
                            Prefix=prefix,
                            ContinuationToken=continuation_token,
                        )
                    # If no keys returned, the server omits 'Contents'
                    for row in resp.get("Contents", []):
                        key = row.get("Key")
                        assert key is not None, "all objects must have a key"
                        yield key
                    if not resp["IsTruncated"]:
                        return
                    continuation_token = resp["NextContinuationToken"]
            else:
                resp = self._s3_client.list_objects_v2(
                    Bucket=self.bucket,
                    Prefix=prefix,
                    Delimiter=delimiter,
                )
                if "CommonPrefixes" not in resp:
                    return  # s3 doesn't include the key if empty
                for result in resp["CommonPrefixes"]:
                    yield unwrap_optional(result.get("Prefix"))
        except Exception:
            _logger.error(f"Got exception while listing files for {prefix=}", exc_info=True)
            raise

    async def async_list_files(self, prefix: str, delimiter: Optional[str] = None):
        iterable = await asyncio.get_running_loop().run_in_executor(self._executor, self.list_files, prefix, delimiter)
        async for filename in to_async_iterable(iterable, self._executor):
            yield filename

    def copy(self, source_filename: str, dest_filename: str) -> None:
        self._s3_client.copy(
            CopySource={
                "Bucket": self.bucket,
                "Key": source_filename,
            },
            Bucket=self.bucket,
            Key=dest_filename,
        )

    def get_file_size(self, filename: str) -> int:
        obj = self._s3_client.get_object(
            Bucket=self.bucket,
            Key=filename,
        )
        return obj["ContentLength"]


class LocalStorageClient(StorageClient):
    protocol = "file"

    def __init__(self, folder: str):
        super().__init__()
        try:
            import fsspec
        except ImportError:
            raise missing_dependency_exception("chalkpy[runtime]")
        self.bucket = ""
        self._folder = pathlib.Path(os.path.abspath(folder))
        self.fs = fsspec.filesystem("file")

    def _normalize_path(self, prefix: str):
        if prefix.startswith("file://"):
            return pathlib.Path(prefix[len("file://") :])
        if prefix.lstrip("/").startswith(str(self._folder).lstrip("/")):
            # It's possible that the prefixes were derived from a uri, in which case the full path is being passed in
            if not prefix.startswith("/"):
                prefix = "/" + prefix
            return pathlib.Path(prefix)
        return self._folder / prefix

    def list_files(self, prefix: str, delimiter: str | None = None) -> Iterable[str]:
        if delimiter is not None:
            raise ValueError("delimiter is not supported for the local storage client")
        joined = self._normalize_path(prefix)
        filename_prefix = ""
        parent = joined
        if not joined.exists():
            parent = joined.parent
            filename_prefix = joined.name
        if not parent.exists():
            return

        # Joined could be a folder, file, or folder with filename prefix
        if joined.is_file():
            yield prefix
            return

        for root, _, files in os.walk(parent):
            for name in files:
                if os.path.relpath(os.path.join(root, name), parent).startswith(filename_prefix):
                    full_path = os.path.join(root, name)
                    rel_path = os.path.relpath(full_path, self._folder)
                    yield rel_path

    def sign_url(
        self,
        filename: str,
        expiration: datetime,
        mode: SignedUrlMode,
        response_disposition: str | None = None,
    ) -> str:
        return "file://" + str(self._normalize_path(filename))

    def upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        """Upload ``data`` to the ``filename``"""
        full_path = self._normalize_path(filename)
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, "wb") as f:
            if not isinstance(data, bytes):
                data = data.read()
            f.write(data)

    async def async_upload_object(
        self,
        filename: str,
        content_type: str,
        data: bytes | BinaryIO,
        metadata: Mapping[str, str] | None = None,
    ):
        return self.upload_object(filename, content_type, data, metadata)

    def get_uri(self, filename: str):
        """Return a URI for a filename"""
        return f"{self.protocol}://" + str(self._normalize_path(filename))

    @overload
    @override
    def download_object(self, filename: str) -> bytes:
        ...

    @overload
    @override
    def download_object(self, filename: str, destination: BinaryIO | str) -> None:
        ...

    def download_object(self, filename: str, destination: BinaryIO | str | None = None) -> bytes | None:
        """Download ``bucket/filename`` to the destination, which can either be an io object or a filepath"""
        path = self._normalize_path(filename)
        if destination is None:
            with open(path, "rb") as f:
                return f.read()
        if isinstance(destination, str):
            shutil.copy2(path, destination)
        else:
            with open(path, "rb") as f:
                destination.write(f.read())

    @overload
    @override
    async def async_download_object(self, filename: str) -> bytes:
        ...

    @overload
    @override
    async def async_download_object(self, filename: str, destination: BinaryIO | str) -> None:
        ...

    async def async_download_object(self, filename: str, destination: BinaryIO | str | None = None):
        """Download ``filename`` and return the contents as bytes"""
        if destination is None:
            return self.download_object(filename)
        else:
            return self.download_object(filename, destination)

    async def async_list_files(self, prefix: str, delimiter: str | None = None) -> AsyncIterator[str]:
        for x in self.list_files(prefix, delimiter):
            yield x

    def copy(self, source_filename: str, dest_filename: str):
        shutil.copy2(self._normalize_path(source_filename), self._normalize_path(dest_filename))

    def get_file_size(self, filename: str):
        return os.stat(self._normalize_path(filename)).st_size
