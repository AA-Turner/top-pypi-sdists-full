from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse

_S3_SCHEME = "s3"
_GCS_SCHEME = "gs"
_FILE_SCHEME = "file"


@dataclass(frozen=True)
class ParsedObjectStorageUri:
    provider: str
    bucket: Optional[str]
    key_prefix: Optional[str]
    local_root: Optional[str]


def normalize_prefix(path: Optional[str]) -> str:
    if path is None or not str(path).strip():
        return ""
    trimmed = str(path).strip()
    while trimmed.startswith("/"):
        trimmed = trimmed[1:]
    while trimmed.endswith("/"):
        trimmed = trimmed[:-1]
    return trimmed


def parse_object_storage_uri(uri: str) -> ParsedObjectStorageUri:
    trimmed = uri.strip()
    if trimmed.startswith(f"{_S3_SCHEME}://"):
        return _parse_cloud_uri("s3", trimmed[len(f"{_S3_SCHEME}://") :])
    if trimmed.startswith(f"{_GCS_SCHEME}://"):
        return _parse_cloud_uri("gcs", trimmed[len(f"{_GCS_SCHEME}://") :])
    if trimmed.startswith(f"{_FILE_SCHEME}://") or trimmed.startswith(
        f"{_FILE_SCHEME}:"
    ):
        return _parse_file_uri(trimmed)
    raise ValueError(
        f"Unsupported object storage URI scheme (expected s3://, gs://, or file://): {uri}"
    )


def _parse_cloud_uri(provider: str, without_scheme: str) -> ParsedObjectStorageUri:
    slash = without_scheme.find("/")
    if slash < 0:
        if not without_scheme:
            raise ValueError("bucket must be non-empty in URI")
        return ParsedObjectStorageUri(
            provider=provider, bucket=without_scheme, key_prefix="", local_root=None
        )
    bucket = without_scheme[:slash]
    prefix = without_scheme[slash + 1 :]
    if not bucket:
        raise ValueError("bucket must be non-empty in URI")
    return ParsedObjectStorageUri(
        provider=provider,
        bucket=bucket,
        key_prefix=normalize_prefix(prefix),
        local_root=None,
    )


def _parse_file_uri(uri: str) -> ParsedObjectStorageUri:
    parsed = urlparse(uri)
    if (parsed.scheme or "").lower() != _FILE_SCHEME:
        raise ValueError(f"Unsupported file URI: {uri}")
    path = parsed.path
    if not path or not path.strip():
        raise ValueError(f"file URI must include a path: {uri}")
    return ParsedObjectStorageUri(
        provider="local", bucket=None, key_prefix=None, local_root=path
    )


def merge_prefix(uri_key_prefix: Optional[str], explicit_prefix: Optional[str]) -> str:
    uri_part = normalize_prefix(uri_key_prefix)
    explicit_part = normalize_prefix(explicit_prefix)
    if uri_part and explicit_part:
        return f"{uri_part}/{explicit_part}"
    return uri_part or explicit_part
