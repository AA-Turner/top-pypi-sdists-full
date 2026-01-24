import hashlib
import os
from abc import ABC, abstractmethod
from collections import defaultdict
from math import ceil
from typing import Dict, List, Mapping, NamedTuple, Optional, Tuple, Type
from urllib.parse import urlparse

import requests

### To create a new upload source
### 1.) Create a new config class that inherits from SourceConfig
### 2.) Create a new uploader class that inherits from FileUploader
### 3.) Update `CONFIG_UPLOADER_MAP` to pair
### 4.) (Optional) Add a default fallback in `_create_uploaders`


class SourceConfig:
    def __init__(self, source_type: str):
        self.type = source_type
        super().__init__()


class LocalSourceConfig(SourceConfig):
    def __init__(self):
        super().__init__("local")


class S3SourceConfig(SourceConfig):
    def __init__(self, aws_profile: Optional[str] = None, aws_region: Optional[str] = None):
        super().__init__("s3")
        self.aws_profile = aws_profile
        self.aws_region = aws_region


class HFSourceConfig(SourceConfig):
    def __init__(self, token: Optional[str] = None):
        super().__init__("hf")
        self.token = token


class FileInfo(NamedTuple):
    name: str
    size_kb: int
    file_hash: bytes


class FileUploader(ABC):
    def __init__(self, config: SourceConfig):
        self.config = config
        super().__init__()

    @abstractmethod
    def can_handle(self, file_path: str) -> bool:
        pass

    @abstractmethod
    def upload(
        self, filename: str, file_path: str, presigned_url: str, dir_allowlist: Optional[List[str]] = None
    ) -> FileInfo:
        pass


class LocalFileUploader(FileUploader):
    def __init__(self, config: LocalSourceConfig):
        super().__init__(config)

    def can_handle(self, file_path: str) -> bool:
        parsed_path = urlparse(file_path)
        return parsed_path.scheme == "" or parsed_path.scheme == "file"

    def upload(
        self, filename: str, file_path: str, presigned_url: str, dir_allowlist: Optional[List[str]] = None
    ) -> FileInfo:
        try:
            safe_path = self._validate_local_path(file_path, dir_allowlist or [])

            with open(safe_path, "rb") as f:
                file_data = f.read()

            file_hash = hashlib.sha256(file_data).digest()
            filesize_kb = ceil(os.path.getsize(file_path) / 1024.0)

            put_response = requests.put(presigned_url, data=file_data)

            if put_response.status_code != 200:
                raise RuntimeError(
                    f"Failed to upload local file {file_path} to presigned URL: "
                    + f"{put_response.status_code} {put_response.text}"
                )

            return FileInfo(filename, filesize_kb, file_hash)

        except Exception as e:
            raise RuntimeError(f"Failed to upload local file {file_path}: {e}")

    @staticmethod
    def _validate_local_path(path: str, dir_allowlist: List[str]) -> str:
        abs_path = os.path.abspath(path)

        if ".." in os.path.relpath(abs_path, start=os.getcwd()).split(os.sep):
            if not any(
                len(allowed_dir) > 0 and os.path.commonpath([abs_path, allowed_dir]) == allowed_dir
                for allowed_dir in dir_allowlist
            ):
                raise ValueError(f"Unsafe file path: {path}")

        if not os.path.isfile(abs_path):
            raise FileNotFoundError(f"Local file not found: {path}")

        return abs_path


class S3FileUploader(FileUploader):
    def __init__(self, config: S3SourceConfig):
        super().__init__(config)
        self.s3_client = None

    def can_handle(self, file_path: str) -> bool:
        parsed_path = urlparse(file_path)
        return parsed_path.scheme == "s3"

    def upload(
        self, filename: str, file_path: str, presigned_url: str, dir_allowlist: Optional[List[str]] = None
    ) -> FileInfo:
        if self.s3_client is None:
            self._setup_s3_client()

        assert self.s3_client is not None, "Unable to initialize s3 client."
        parsed_path = urlparse(file_path)
        src_bucket = parsed_path.netloc
        src_key = parsed_path.path.lstrip("/")

        try:
            response = self.s3_client.get_object(Bucket=src_bucket, Key=src_key)
            file_data = response["Body"].read()

            file_hash = hashlib.sha256(file_data).digest()
            filesize_kb = ceil(response["ContentLength"] / 1024.0)

            put_response = requests.put(
                presigned_url,
                data=file_data,
                headers={"Content-Type": response.get("ContentType", "application/octet-stream")},
            )

            if put_response.status_code != 200:
                raise RuntimeError(
                    f"Failed to upload to presigned URL for {filename}: "
                    + f"{put_response.status_code} {put_response.text}"
                )

            return FileInfo(filename, filesize_kb, file_hash)

        except Exception as e:
            raise RuntimeError(f"Unable to get object from {file_path}. {e}")

    def _setup_s3_client(self):
        try:
            import boto3
        except ImportError:
            raise ImportError("Please install boto3 to enable model registration.")

        aws_profile = getattr(self.config, "aws_profile", None) or os.environ.get("AWS_PROFILE")
        aws_region = getattr(self.config, "aws_region", None) or os.environ.get("AWS_REGION")

        session = boto3.Session(profile_name=aws_profile, region_name=aws_region)
        self.s3_client = session.client("s3")


class HFFileUploader(FileUploader):
    def __init__(self, config: HFSourceConfig):
        super().__init__(config)

    def can_handle(self, file_path: str) -> bool:
        parsed_path = urlparse(file_path)
        return parsed_path.scheme == "hf" or "huggingface.co" in file_path

    def upload(
        self, filename: str, file_path: str, presigned_url: str, dir_allowlist: Optional[List[str]] = None
    ) -> FileInfo:
        raise NotImplementedError()


CONFIG_UPLOADER_MAP: Dict[Type[SourceConfig], Type[FileUploader]] = {
    LocalSourceConfig: LocalFileUploader,
    S3SourceConfig: S3FileUploader,
    HFSourceConfig: HFFileUploader,
}


class ModelFileUploader:
    def __init__(self, source_config: Optional[SourceConfig]):
        self.source_config = source_config if source_config else SourceConfig(source_type="")
        self.uploaders = self._create_uploaders()
        super().__init__()

    def _create_uploaders(self) -> List[FileUploader]:
        uploaders: List[FileUploader] = []

        uploader_cls = CONFIG_UPLOADER_MAP.get(type(self.source_config))
        if uploader_cls:
            uploaders.append(uploader_cls(self.source_config))

        existing_types = {type(uploader) for uploader in uploaders}

        for fallback_config_cls, fallback_uploader_cls in [
            (LocalSourceConfig, LocalFileUploader),
            (S3SourceConfig, S3FileUploader),
        ]:
            if fallback_uploader_cls not in existing_types:
                uploaders.append(fallback_uploader_cls(fallback_config_cls()))  # pyright: ignore[reportArgumentType]

        return uploaders

    def upload_files(
        self,
        file_paths: Dict[str, str],
        model_file_names: List[str],
        presigned_urls: Mapping[str, str],
        dir_allowlist: List[str],
    ) -> Tuple[List[FileInfo], List[FileInfo]]:
        """
        Upload files using appropriate uploaders based on file path schemes.

        Args:
            file_paths: Dict mapping filename -> local_or_s3_path
            model_file_names: List of filenames that are model files
            presigned_urls: Dict mapping filename -> presigned_url
            dir_allowlist: List of allowed directories for local files

        Returns:
            Tuple of (model_uploaded_files, additional_uploaded_files)
        """
        model_uploaded_files: List[FileInfo] = []
        additional_uploaded_files: List[FileInfo] = []

        for filename, file_path in file_paths.items():
            presigned_url = presigned_urls[filename]

            uploader = self._get_uploader_for_path(file_path)
            if not uploader:
                raise ValueError(f"No suitable uploader found for file path: {file_path}")

            file_info = uploader.upload(filename, file_path, presigned_url, dir_allowlist)

            if filename in model_file_names:
                model_uploaded_files.append(file_info)
            else:
                additional_uploaded_files.append(file_info)

        return model_uploaded_files, additional_uploaded_files

    def _get_uploader_for_path(self, file_path: str) -> Optional[FileUploader]:
        for uploader in self.uploaders:
            if uploader.can_handle(file_path):
                return uploader
        return None

    @staticmethod
    def prepare_file_mapping(
        model_paths: List[str],
        additional_files: Optional[List[str]] = None,
    ) -> Tuple[Dict[str, str], List[str]]:
        """Prepare mapping of all files to be uploaded."""
        all_files: Dict[str, str] = defaultdict(str)
        model_file_names: List[str] = []

        for model_path in model_paths:
            filename = os.path.basename(model_path)
            all_files[filename] = model_path
            model_file_names.append(filename)

        if additional_files:
            for file_path in additional_files:
                filename = os.path.basename(file_path)
                all_files[filename] = file_path

        return all_files, model_file_names
