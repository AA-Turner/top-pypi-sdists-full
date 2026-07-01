"""Storage provider implementations for cloud and local filesystems.

Supports:
- AWS S3 and S3-compatible (R2, MinIO)
- Azure Blob Storage / Azure Data Lake Storage Gen2
- Google Cloud Storage (GCS)
- Local filesystem
"""

from dataclasses import dataclass
from typing import Any, Literal

from fsspec import AbstractFileSystem

StorageProvider = Literal["s3", "r2", "minio", "azure", "gcs", "local"]


@dataclass
class S3Credentials:
    """AWS S3 / S3-compatible (R2, MinIO) credentials."""

    access_key_id: str
    secret_access_key: str
    session_token: str | None = None
    endpoint_url: str | None = None
    region: str | None = None

    def to_storage_options(self) -> dict[str, Any]:
        opts: dict[str, Any] = {
            "key": self.access_key_id,
            "secret": self.secret_access_key,
        }
        if self.session_token:
            opts["token"] = self.session_token
        if self.endpoint_url or self.region:
            opts["client_kwargs"] = {}
            if self.endpoint_url:
                opts["client_kwargs"]["endpoint_url"] = self.endpoint_url
            if self.region:
                opts["client_kwargs"]["region_name"] = self.region
        return opts


@dataclass
class MinioCredentials:
    """MinIO credentials."""

    access_key_id: str
    secret_access_key: str
    session_token: str | None = None
    endpoint_url: str | None = None
    region: str | None = None

    def to_storage_options(self) -> dict[str, Any]:
        opts: dict[str, Any] = {
            "key": self.access_key_id,
            "secret": self.secret_access_key,
        }
        if self.session_token:
            opts["token"] = self.session_token
        if self.endpoint_url or self.region:
            opts["client_kwargs"] = {}
            if self.endpoint_url:
                opts["client_kwargs"]["endpoint_url"] = self.endpoint_url
            if self.region:
                opts["client_kwargs"]["region_name"] = self.region
        return opts


@dataclass
class AzureBlobCredentials:
    """Azure Blob Storage / ADLS Gen2 credentials.

    Supports multiple authentication methods:
    - Connection string
    - Account key
    - SAS token
    - Service principal (client credentials)
    - Managed identity (when running on Azure)
    """

    account_name: str
    """Azure storage account name."""

    account_key: str | None = None
    """Storage account access key."""

    sas_token: str | None = None
    """Shared Access Signature token."""

    connection_string: str | None = None
    """Full connection string (overrides other auth)."""

    tenant_id: str | None = None
    """Azure AD tenant ID for service principal auth."""

    client_id: str | None = None
    """Azure AD client/application ID."""

    client_secret: str | None = None
    """Azure AD client secret."""

    use_managed_identity: bool = False
    """Use Azure Managed Identity for auth."""

    def to_storage_options(self) -> dict[str, Any]:
        """Convert to adlfs storage options."""
        opts: dict[str, Any] = {
            "account_name": self.account_name,
        }

        if self.connection_string:
            opts["connection_string"] = self.connection_string
        elif self.account_key:
            opts["account_key"] = self.account_key
        elif self.sas_token:
            opts["sas_token"] = self.sas_token
        elif self.tenant_id and self.client_id and self.client_secret:
            opts["tenant_id"] = self.tenant_id
            opts["client_id"] = self.client_id
            opts["client_secret"] = self.client_secret
        elif self.use_managed_identity:
            # adlfs will use DefaultAzureCredential
            pass

        return opts


@dataclass
class GCSCredentials:
    """Google Cloud Storage credentials.

    Supports multiple authentication methods:
    - Service account JSON key file
    - Service account JSON key content
    - Application Default Credentials (ADC)
    - Anonymous access (for public buckets)
    """

    project: str | None = None
    """GCP project ID."""

    token: str | None = None
    """Path to service account JSON key file, or the JSON content itself."""

    access: str = "full_control"
    """Access level: read_only, read_write, full_control."""

    use_anonymous: bool = False
    """Use anonymous access (public buckets only)."""

    def to_storage_options(self) -> dict[str, Any]:
        """Convert to gcsfs storage options."""
        opts: dict[str, Any] = {}

        if self.project:
            opts["project"] = self.project

        if self.use_anonymous:
            opts["token"] = "anon"  # noqa: S105
        elif self.token:
            opts["token"] = self.token
        # else: uses Application Default Credentials

        if self.access:
            opts["access"] = self.access

        return opts


def from_provider(
    provider: StorageProvider,
    credentials: dict[str, Any] | None = None,
) -> AbstractFileSystem:
    """Create filesystem from provider and credentials.

    Args:
        provider: Storage provider type.
        credentials: Provider-specific credentials dict.

    Returns:
        Configured filesystem instance.

    Raises:
        ValueError: If provider is unsupported or credentials missing.
        ImportError: If required package not installed.
    """
    if provider == "local":
        from fsspec.implementations.local import LocalFileSystem

        return LocalFileSystem()

    if credentials is None:
        raise ValueError(f"Credentials required for provider: {provider}")

    if provider in ("s3", "r2"):
        try:
            from s3fs import S3FileSystem
        except ImportError as e:
            raise ImportError("s3fs not installed. Install with: pip install s3fs") from e

        creds = S3Credentials(**credentials)
        return S3FileSystem(
            **creds.to_storage_options(),
            use_listings_cache=False,
            listings_expiry_time=0,
            skip_instance_cache=True,
        )

    if provider == "minio":
        try:
            from s3fs import S3FileSystem
        except ImportError as e:
            raise ImportError("s3fs not installed. Install with: pip install s3fs") from e

        creds = MinioCredentials(**credentials)
        return S3FileSystem(
            **creds.to_storage_options(),
            use_listings_cache=False,
            listings_expiry_time=0,
            skip_instance_cache=True,
        )

    if provider == "azure":
        try:
            from adlfs import AzureBlobFileSystem  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError("adlfs not installed. Install with: pip install adlfs") from e

        creds = AzureBlobCredentials(**credentials)
        return AzureBlobFileSystem(**creds.to_storage_options())

    if provider == "gcs":
        try:
            from gcsfs import GCSFileSystem  # type: ignore[import-untyped]
        except ImportError as e:
            raise ImportError("gcsfs not installed. Install with: pip install gcsfs") from e

        creds = GCSCredentials(**credentials)
        return GCSFileSystem(**creds.to_storage_options())

    raise ValueError(f"Unsupported storage provider: {provider}")


__all__ = [
    "AzureBlobCredentials",
    "GCSCredentials",
    "MinioCredentials",
    "S3Credentials",
    "StorageProvider",
    "from_provider",
]
