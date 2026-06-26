from __future__ import annotations

import re
from collections.abc import Mapping
from datetime import UTC, datetime, time, timedelta
from enum import Enum, StrEnum
from pathlib import PurePosixPath
from typing import TYPE_CHECKING, Annotated, Any, Generic, Literal, TypeAlias, TypedDict, TypeVar
from uuid import UUID

import icechunk

if TYPE_CHECKING:
    import obstore as obs
    from obstore.store import AzureConfig, ClientConfig, GCSCredential, S3Config
from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    PlainValidator,
    SecretStr,
    ValidationInfo,
    field_serializer,
    field_validator,
    model_validator,
)
from pydantic.functional_validators import BeforeValidator

HTML = str

VALID_NAME = r"(\w[\w\.\-_]+)"

# AWS STS session tag values are limited to 256 characters. Repo names are passed as the
# AlRepoName tag value in STS AssumeRole calls, so we cap well below that.
MAX_REPO_NAME_LENGTH = 128
# Bucket prefixes are embedded (×3) in AWS session policy JSON (2048-char limit) and GCP
# CAB CEL expressions. 256 keeps worst-case total prefix comfortably within budget.
MAX_BUCKET_PREFIX_LENGTH = 256
# S3 bucket names are capped at 63 by AWS; GCS and Azure containers have similar limits.
MAX_BUCKET_NAME_LENGTH = 63

ScalarType = str | int | float | bool | None

RepoMetadataT = dict[str, ScalarType | list[ScalarType]]

T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int
    pages: int


def validate_name(name: str, *, entity: str) -> str:
    """
    All names must start with a word character (i.e. letter, digit, or underscore),
    then have at least one more character, which is either another word character, a dot, or a hyphen.
    """
    if not re.fullmatch(VALID_NAME, name):
        raise ValueError(f"Invalid {entity} name: `{name}`")

    return name


class NameValidator:
    def __init__(self, *, entity: str) -> None:
        self.entity = entity

    def __call__(self, name: str) -> str:
        return validate_name(name, entity=self.entity)


# TODO in python 3.12+ we should add `type ` to the start of these lines
# That should stop IDE linters complaining that "Variable is not allowed in type expression" by making it a proper type alias
OrgName: TypeAlias = Annotated[str, BeforeValidator(NameValidator(entity="org"))]
RepoName: TypeAlias = Annotated[str, BeforeValidator(NameValidator(entity="repo"))]


def validate_org_and_repo_name(org_and_repo_name: str) -> str:
    expr = f"{VALID_NAME}/{VALID_NAME}"
    res = re.fullmatch(expr, org_and_repo_name)
    if not res:
        raise ValueError(f"Not a valid repo identifier: `{org_and_repo_name}`. Should have the form `[ORG]/[REPO]`.")

    return org_and_repo_name


OrgAndRepoName: TypeAlias = Annotated[str, BeforeValidator(validate_org_and_repo_name)]  # of the form {org_name}/{repo_name}


def validate_bucket_name(name: str) -> str:
    """
    S3 and GCS have fairly strict naming rules so we can mostly rely on them here.
    Our checks are meant to make sure the data we receive is valid.
    """

    if " " in name:
        raise ValueError(f"Bucket name must not contain spaces. Received {name}")
    if "://" in name:
        raise ValueError(f"Bucket name must not contain schemes. Received {name}")
    if "/" in name:
        raise ValueError(f"Bucket name must not contain slashes. Received {name}")
    if len(name) < 3:
        raise ValueError(f"Bucket name must be at least 3 characters long. Received {name}")
    validate_name(name, entity="bucket")

    return name


BucketName: TypeAlias = Annotated[str, BeforeValidator(validate_bucket_name)]


def validate_nickname(nickname: str) -> str:
    # Remove leading and trailing whitespace.
    nickname = nickname.strip()

    validate_name(name=nickname, entity="bucket nickname")

    # NOTE: We only impose a limit on string size. This is intended to be a
    # human-friendly identifier, so we're looser than e.g. S3 regarding
    # naming conventions and restrictions.
    if len(nickname) < 3:
        raise ValueError("Bucket nickname must be at least 3 characters long.")
    if len(nickname) > 64:
        raise ValueError("Bucket nickname must be at most 64 characters long.")

    return nickname


BucketNickname: TypeAlias = Annotated[str, BeforeValidator(validate_nickname)]


def validate_bucket_prefix(prefix: str) -> str:
    if prefix == "":
        return prefix
    # Remove leading and trailing whitespace.
    prefix = prefix.strip()
    if " " in prefix:
        raise ValueError("Bucket prefix must not contain spaces.")
    if prefix.startswith("/") or prefix.endswith("/"):
        raise ValueError("Bucket prefix must not start or end with a slash.")
    return prefix


BucketPrefix: TypeAlias = Annotated[str, BeforeValidator(validate_bucket_prefix)]
URI: TypeAlias = str  # of the form "platform://bucket_name[/prefix]"


class StorageOptions(TypedDict, total=False):
    """Options for configuring the underlying Icechunk storage.

    These options are passed to the Icechunk storage creation functions
    (e.g., s3_storage, tigris_storage, r2_storage).

    Attributes:
        `network_stream_timeout_seconds`: Timeout in seconds for network stream operations.
            If no bytes can be transmitted during this period, the request will timeout.
            Set to 0 to disable timeout. Only applies to S3, Tigris, and R2 storage.
    """

    network_stream_timeout_seconds: int


def utc_now():
    # drop microseconds because bson does not support them
    return datetime.now(UTC).replace(microsecond=0)


def datetime_to_isoformat(v: datetime) -> str:
    return v.isoformat()


def to_dbid_bytes(v: Any) -> DBIDBytes:
    if isinstance(v, str):
        return DBIDBytes.fromhex(v)
    if isinstance(v, bytes):
        return DBIDBytes(v)
    if hasattr(v, "binary"):
        return DBIDBytes(v.binary)
    raise ValueError("Invalid DBID object")


class DBIDBytes(bytes):
    def __str__(self) -> str:
        """Format as hex digits"""
        return self.hex()

    def __repr__(self):
        return str(self)


def dbid_validator(v: Any) -> DBIDBytes:
    return to_dbid_bytes(v)


DBID = Annotated[DBIDBytes, PlainValidator(dbid_validator)]


class RepoKind(StrEnum):
    V1 = "v1"
    Icechunk = "icechunk"


class SubscriptionType(StrEnum):
    """Type/tier of a repo subscription.

    FILTERED: Selection of variables from repo
    DIRECT: Mirror of source repo
    PRIVATE: Data fully materialized in subscriber bucket
    """

    DIRECT = "direct"
    FILTERED = "filtered"
    PRIVATE = "private"


class SubscriptionPricingType(StrEnum):
    """Pricing type for a repo subscription.

    FREE: No cost ($0)
    ONE_TIME: Single payment
    MONTHLY: Recurring monthly payment
    """

    FREE = "free"
    ONE_TIME = "one_time"
    MONTHLY = "monthly"


class RepoCreateBodyBase(BaseModel):
    """Base fields shared across all repo creation modes."""

    name: RepoName
    description: str | None = None
    bucket_nickname: BucketNickname | None = None
    kind: RepoKind = RepoKind.Icechunk
    metadata: RepoMetadataT | None = None

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, v: str) -> str:
        if len(v) > MAX_REPO_NAME_LENGTH:
            raise ValueError(f"Repo name must be at most {MAX_REPO_NAME_LENGTH} characters long. Got {len(v)}.")
        return v


class RepoCreateBody(RepoCreateBodyBase):
    """Body for creating or registering a new repo.

    Note: create_mode="import" is deprecated. Use the dedicated /repos/import endpoint instead.
    """

    prefix: BucketPrefix | None = None
    create_mode: Literal["create", "register", "import"] = "register"
    spec_version: Literal[1, 2] | None = None  # Icechunk spec version

    @field_validator("prefix")
    @classmethod
    def validate_prefix_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) > MAX_BUCKET_PREFIX_LENGTH:
            raise ValueError(f"Prefix must be at most {MAX_BUCKET_PREFIX_LENGTH} characters long. Got {len(v)}.")
        return v


class RepoImportBody(RepoCreateBodyBase):
    """Body for importing an existing icechunk repo from storage.

    Note: spec_version is not specified by the user - it's detected from the imported repo.
    """

    prefix: BucketPrefix  # Required for import

    @field_validator("prefix")
    @classmethod
    def validate_prefix_length(cls, v: str) -> str:
        if len(v) > MAX_BUCKET_PREFIX_LENGTH:
            raise ValueError(f"Prefix must be at most {MAX_BUCKET_PREFIX_LENGTH} characters long. Got {len(v)}.")
        return v


class RepoSubscribeBody(RepoCreateBodyBase):
    """Body for subscribing to a marketplace listing.

    Note: spec_version is inherited from the parent repo, not specified by the user.
    """

    marketplace_listing_id: str = Field(..., description="The ID of the marketplace listing to subscribe to")
    target_filter: DatasetFilter | None = Field(
        None, description="Subscriber-defined filter applied on top of the provider's source filter. None means no additional filtering."
    )
    subscription_type: SubscriptionType = Field(default=SubscriptionType.DIRECT, description="The type/tier of subscription.")
    prefix: BucketPrefix | None = Field(
        None, description="Custom storage prefix for filtered/private subscriptions. If not provided, one is auto-generated."
    )

    @field_validator("prefix")
    @classmethod
    def validate_prefix_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) > MAX_BUCKET_PREFIX_LENGTH:
            raise ValueError(f"Prefix must be at most {MAX_BUCKET_PREFIX_LENGTH} characters long. Got {len(v)}.")
        return v

    @model_validator(mode="after")
    def validate_subscription_type_with_filter(self) -> RepoSubscribeBody:
        if self.target_filter is not None and self.subscription_type == SubscriptionType.DIRECT:
            raise ValueError("subscription_type cannot be 'direct' when target_filter is specified. Use 'filtered' or 'private' instead.")
        # Filtered/private subscriptions require explicit target_filter with explicit allowlist
        if self.subscription_type in (SubscriptionType.FILTERED, SubscriptionType.PRIVATE):
            if self.target_filter is None:
                raise ValueError(f"target_filter is required for {self.subscription_type.value} subscriptions.")
            if self.target_filter.nodes is None:
                raise ValueError(f"target_filter.nodes cannot be None for {self.subscription_type.value} subscriptions.")
            if not self.target_filter.nodes.include_paths:
                raise ValueError(f"target_filter must have explicit include_paths for {self.subscription_type.value} subscriptions.")
            if self.target_filter.nodes.include_paths == ["/"]:
                raise ValueError(f"target_filter cannot be the root group for {self.subscription_type.value} subscriptions.")
        return self


class RepoClaimBody(RepoCreateBodyBase):
    """Body for claiming a subscription via claim code.

    Note: spec_version is inherited from the parent repo, not specified by the user.
    """

    claim_code: str = Field(..., description="The claim code to redeem")
    prefix: BucketPrefix | None = Field(
        None, description="Custom storage prefix for filtered/private subscriptions. If not provided, one is auto-generated."
    )

    @field_validator("prefix")
    @classmethod
    def validate_prefix_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) > MAX_BUCKET_PREFIX_LENGTH:
            raise ValueError(f"Prefix must be at most {MAX_BUCKET_PREFIX_LENGTH} characters long. Got {len(v)}.")
        return v


class RepoModifyRequest(BaseModel):
    description: str | None = None
    add_metadata: RepoMetadataT | None = None
    remove_metadata: list[str] | None = None
    update_metadata: RepoMetadataT | None = None
    optimization_config: OptimizationConfig | None = None


class RepoModifyBody(BaseModel):
    description: str | None = None
    metadata: RepoMetadataT | None = None
    optimization_config: OptimizationConfig | None = None


# Used for `/orgs/{org}/{repo}/visibility` endpoint
class RepoVisibilityModel(BaseModel):
    """The visibility of a repo"""

    visibility: RepoVisibility


class RepoVisibility(StrEnum):
    # PRIVATE: Visible only to repo members.
    # NOTE: Currently, this means any member of an org.
    PRIVATE = "PRIVATE"

    # AUTHENTICATED_PUBLIC: Visible to any authenticated user of Arraylake.
    AUTHENTICATED_PUBLIC = "AUTHENTICATED_PUBLIC"

    # PUBLIC: Visible to anybody on the public internet.
    # PUBLIC = "PUBLIC"


Platform = Literal["s3", "s3-compatible", "minio", "gs", "azure"]


class AWSCustomerManagedRoleAuth(BaseModel):
    # TODO: Run a Mongo migration to convert all existing customer_managed_role
    # auth to aws_customer_managed_role.
    method: Literal["aws_customer_managed_role", "customer_managed_role"]
    external_customer_id: str
    external_role_name: str
    shared_secret: SecretStr | None = None

    @field_serializer("shared_secret", when_used="unless-none")
    def serialize_shared_secret(self, v, _info):
        """
        Serialize shared_secret based on context:
        - context={'reveal_secrets': True}: Reveal secret (for client → server API calls)
        - Otherwise: Keep obfuscated (for server → client responses and display)
        """
        if _info.context and _info.context.get("reveal_secrets"):
            return v.get_secret_value() if isinstance(v, SecretStr) else v
        # Default: keep obfuscated
        return str(v) if isinstance(v, SecretStr) else v


class GCPCustomerManagedRoleAuth(BaseModel):
    method: Literal["gcp_customer_managed_role"]
    target_service_account: str


class R2CustomerManagedRoleAuth(BaseModel):
    method: Literal["r2_customer_managed_role"]
    external_account_id: str
    account_api_token: SecretStr
    parent_access_key_id: SecretStr
    duration_seconds: int = 3600  # Default to 1 hour TODO: figure out how we want to handle expiration

    @field_serializer("account_api_token", "parent_access_key_id", when_used="unless-none")
    def serialize_secrets(self, v, _info):
        """
        Serialize secrets based on context:
        - context={'reveal_secrets': True}: Reveal secret (for client → server API calls)
        - Otherwise: Keep obfuscated (for server → client responses and display)
        """
        if _info.context and _info.context.get("reveal_secrets"):
            return v.get_secret_value() if isinstance(v, SecretStr) else v
        # Default: keep obfuscated
        return str(v) if isinstance(v, SecretStr) else v


class AzureDelegatedCredentialsAuth(BaseModel):
    method: Literal["azure_credential_delegation"]
    tenant_id: str  # Tenant ID where the storage account resides
    storage_account: str  # Azure storage account name that contains the container/bucket


CustomerManagedRoleAuth: TypeAlias = (
    AWSCustomerManagedRoleAuth | GCPCustomerManagedRoleAuth | R2CustomerManagedRoleAuth | AzureDelegatedCredentialsAuth
)


# NOTE: Deprecating bucket policy method
class BucketPolicyAuth(BaseModel):
    method: Literal["bucket_policy"]


class HmacAuth(BaseModel):
    method: Literal["hmac"]
    # NOTE: these ideally would be secret strings
    access_key_id: str
    secret_access_key: str


# TODO: Rename to Self Managed
class AnonymousAuth(BaseModel):
    method: Literal["anonymous"]
    # Anonymous (public) Azure containers need the storage account name to resolve the
    # blob endpoint host (<storage_account>.blob.core.windows.net). It's carried here so
    # the account lives in auth_config for both anonymous and delegated Azure buckets, and
    # is left None for s3/gcs anonymous buckets. Required for azure (see NewBucket).
    storage_account: str | None = None


AuthConfig: TypeAlias = CustomerManagedRoleAuth | BucketPolicyAuth | HmacAuth | AnonymousAuth


class BucketModel(BaseModel):
    """
    Common attributes defining a bucket configuration in arraylake.

    Used for NewBucket requests, so should only contain parameters that users should be allowed to set.
    """

    nickname: BucketNickname
    platform: Platform
    name: BucketName
    prefix: BucketPrefix = ""
    extra_config: Mapping[str, str | bool]

    @property
    def protocol(self) -> str:
        """The protocol (or "scheme") used for urls to this bucket, e.g. 's3://'."""
        match self.platform:
            case "s3" | "s3-compatible" | "minio":
                return "s3://"
            case "gs":
                return "gs://"
            case "azure":
                return "az://"
            case _:
                raise NotImplementedError(self.platform)

    @property
    def url(self) -> URI:
        """
        The full url to the bucket, e.g. 's3://bucket/prefix/'.

        Includes platform scheme, bucket name, and possibly prefix.
        """
        url = f"{self.protocol}{self.name}/{self.prefix}"
        return url + "/" if not url.endswith("/") else url

    def url_with_subprefix(self, subprefix: str) -> URI:
        """The full url to a location within this bucket, e.g. 's3://bucket/prefix/subprefix/'."""
        if not subprefix:
            return self.url
        return f"{self.url}{subprefix.strip('/')}/"

    @property
    def region_name(self) -> str | None:
        """
        Cloud region for this bucket (e.g. `us-east-1`)

        Returns `None` If not applicable (e.g. for R2 or Tigris buckets).
        """
        region = self.extra_config.get("region_name")
        return str(region) if region else None

    def to_vcc_store_config(self, user_id: UUID | None = None) -> icechunk.AnyObjectStoreConfig:
        """Create an Icechunk ObjectStoreConfig for use as a virtual chunk container.

        This extracts the necessary configuration from the bucket's extra_config
        to create a properly configured store config for accessing virtual chunks.

        Args:
            user_id: Optional user ID for logging purposes (used in GCS user_agent).

        Returns:
            An icechunk ObjectStoreConfig for the bucket's platform.
        """
        if self.platform in ("s3", "s3-compatible", "minio"):
            endpoint_url = self.extra_config.get("endpoint_url")
            if endpoint_url is not None:
                endpoint_url = str(endpoint_url)

            region = self.extra_config.get("region_name")
            if region is not None:
                region = str(region)

            use_ssl = self.extra_config.get("use_ssl", True)
            allow_http = not use_ssl

            force_path_style_raw = self.extra_config.get("force_path_style", False if use_ssl else True)
            force_path_style = bool(force_path_style_raw)

            options = icechunk.S3Options(
                region=region,
                endpoint_url=endpoint_url,
                allow_http=allow_http,
                force_path_style=force_path_style,
            )
            return icechunk.ObjectStoreConfig.S3(options)
        elif self.platform == "gs":
            from arraylake import __version__ as arraylake_version

            # Used for logging and debugging purposes in GCS access logs to help identify which client/version and optionally which user is accessing virtual chunks
            config = {"user_agent": f"arraylake/{arraylake_version} (uuid={str(user_id)})" if user_id else f"arraylake/{arraylake_version}"}
            return icechunk.ObjectStoreConfig.Gcs(config)
        elif self.platform == "azure":
            return icechunk.ObjectStoreConfig.Azure({})
        else:
            raise ValueError(f"Unsupported platform for VCC store config: {self.platform}")

    def as_obstore_store(
        self,
        credentials: TempCredentials | None,
        prefix: str | None = None,
        retry_config: Any | None = None,
    ) -> obs.store.ObjectStore:
        """Build an obstore ObjectStore for this bucket using the given credentials.

        Requires the optional ``obstore`` extra (``pip install arraylake[obstore]``).

        Args:
            credentials: Temporary credentials for the bucket. Pass ``None`` for
                anonymous access (the resulting store will use ``skip_signature``).
            prefix: Object key prefix to scope the store to. Defaults to ``self.prefix``
                if not provided.

        Returns:
            An ``obstore.store.S3Store``, ``GCSStore``, or ``AzureStore``
            depending on this bucket's platform.

        Raises:
            ImportError: If the optional ``obstore`` extra is not installed.
            ValueError: If the bucket's platform or credential type is unsupported.
        """
        try:
            import obstore as obs
        except ImportError as e:
            raise ImportError(
                "The 'obstore' package is required for this functionality but is not installed. "
                "Install it with: pip install 'arraylake[obstore]'"
            ) from e

        effective_prefix = prefix if prefix is not None else self.prefix

        endpoint_url = self.extra_config.get("endpoint_url")
        s3_client_options: ClientConfig = {}
        if endpoint_url and str(endpoint_url).startswith("http://"):
            s3_client_options["allow_http"] = True

        if self.platform in ("s3", "s3-compatible", "minio"):
            if credentials is None:
                s3_config: S3Config = {"skip_signature": True}
            elif isinstance(credentials, S3Credentials):
                s3_config = {
                    "access_key_id": credentials.aws_access_key_id,
                    "secret_access_key": credentials.aws_secret_access_key,
                }
                if credentials.aws_session_token:
                    s3_config["session_token"] = credentials.aws_session_token
            else:
                raise ValueError(f"Expected S3Credentials or None for platform {self.platform!r}, got {type(credentials).__name__}")
            if self.region_name:
                s3_config["region"] = self.region_name
            if endpoint_url:
                s3_config["endpoint"] = str(endpoint_url)
            return obs.store.S3Store(
                bucket=self.name,
                prefix=effective_prefix,
                config=s3_config,
                client_options=s3_client_options or None,
                retry_config=retry_config,
            )
        elif self.platform == "gs":
            if credentials is None:
                return obs.store.GCSStore(
                    bucket=self.name,
                    prefix=effective_prefix,
                    config={"skip_signature": True},
                    retry_config=retry_config,
                )
            elif isinstance(credentials, GSCredentials):
                # google-auth returns naive datetimes (utcnow with tzinfo stripped) but
                # obstore requires timezone-aware datetimes; normalize in the provider.
                gcs_creds = credentials

                def gcs_credential_provider() -> GCSCredential:
                    expires_at = gcs_creds.expiration
                    if expires_at is not None and expires_at.tzinfo is None:
                        expires_at = expires_at.replace(tzinfo=UTC)
                    return {"token": gcs_creds.access_token, "expires_at": expires_at}

                return obs.store.GCSStore(
                    bucket=self.name,
                    prefix=effective_prefix,
                    credential_provider=gcs_credential_provider,
                    retry_config=retry_config,
                )
            else:
                raise ValueError(f"Expected GSCredentials or None for platform 'gs', got {type(credentials).__name__}")
        elif self.platform == "azure":
            if credentials is None:
                azure_config: AzureConfig = {"skip_signature": True}
                # Anonymous access still needs the storage account name to resolve the host.
                # It lives on the (anonymous) auth_config, only present on Bucket subclasses
                # that carry auth_config, e.g. BucketResponse.
                account_name = getattr(getattr(self, "auth_config", None), "storage_account", None)
                if account_name:
                    azure_config["account_name"] = account_name
            elif isinstance(credentials, AzureCredentials):
                azure_config = {
                    "sas_key": credentials.sas_token,
                    "account_name": credentials.storage_account,
                }
            else:
                raise ValueError(f"Expected AzureCredentials or None for platform 'azure', got {type(credentials).__name__}")
            return obs.store.AzureStore(
                container_name=self.name,
                prefix=effective_prefix,
                config=azure_config,
                retry_config=retry_config,
            )
        else:
            raise ValueError(f"Unsupported platform: {self.platform}")


class Bucket(BucketModel):
    """A bucket configuration which actually exists in arraylake."""

    id: UUID
    created: datetime = Field(default_factory=utc_now)
    updated: datetime
    created_by: EmailStr | None = None

    # NOTE: To prevent credential leakage, we don't share the auth_config here.

    @model_validator(mode="before")
    @classmethod
    def set_initial_updated(cls, data: Any) -> Any:
        if isinstance(data, dict) and "updated" not in data:
            data["updated"] = data.get("created", utc_now())
        return data

    @field_validator("created", "updated")
    @classmethod
    def timestamp_in_utc_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=UTC)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)

    @property
    def protocol(self) -> str:
        """The protocol (or "scheme") used for urls to this bucket, e.g. 's3://'."""
        match self.platform:
            case "s3" | "s3-compatible" | "minio":
                # TODO is this right for e.g. r2?
                return "s3://"
            case "gs":
                return "gs://"
            case "azure":
                return "az://"
            case _:
                raise NotImplementedError(self.platform)

    @property
    def url(self) -> URI:
        """
        The full url to the bucket, e.g. 's3://bucket/prefix/'.

        Included platform scheme, bucket name, and possibly prefix.
        """
        url = f"{self.protocol}{self.name}/{self.prefix}"
        return url + "/" if not url.endswith("/") else url


def _validate_role_auth_shared_secret(auth_config: AuthConfig | None) -> None:
    if isinstance(auth_config, AWSCustomerManagedRoleAuth):
        secret = auth_config.shared_secret
        if secret is None or not secret.get_secret_value():
            raise ValueError("AWS customer-managed-role buckets require a shared_secret (used as the STS AssumeRole ExternalId).")


class NewBucket(BucketModel):
    """A request to create a new bucket."""

    auth_config: AuthConfig = Field(discriminator="method")

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, v: str) -> str:
        if len(v) > MAX_BUCKET_NAME_LENGTH:
            raise ValueError(f"Bucket name must be at most {MAX_BUCKET_NAME_LENGTH} characters long.")
        return v

    @field_validator("prefix")
    @classmethod
    def validate_prefix_length(cls, v: str) -> str:
        if v and len(v) > MAX_BUCKET_PREFIX_LENGTH:
            raise ValueError(f"Bucket prefix must be at most {MAX_BUCKET_PREFIX_LENGTH} characters long.")
        return v

    @model_validator(mode="after")
    def _validate_bucket_options(self):
        if self.platform in ["s3"]:  # TODO: decide if the same is needed for gs buckets
            if "region_name" not in self.extra_config:
                raise ValueError("S3 buckets require a region_name.")
        if self.platform == "s3-compatible":
            if "endpoint_url" not in self.extra_config:
                raise ValueError("S3-compatible buckets require an endpoint_url.")
        # Anonymous Azure buckets need the storage account name (the blob endpoint host),
        # which the generic AnonymousAuth only carries optionally.
        if self.platform == "azure" and isinstance(self.auth_config, AnonymousAuth) and not self.auth_config.storage_account:
            raise ValueError("Anonymous Azure buckets require a storage_account (the Azure storage account name).")
        return self

    @field_validator("auth_config")
    @classmethod
    def validate_auth_config(cls, auth_config: AuthConfig | None, info: ValidationInfo) -> AuthConfig | None:
        valid_methods = [
            "customer_managed_role",
            "aws_customer_managed_role",
            "gcp_customer_managed_role",
            "r2_customer_managed_role",
            "azure_credential_delegation",
            "anonymous",
            "hmac",
        ]
        if auth_config and auth_config.method not in valid_methods:
            # Deprecating bucket policy method
            raise ValueError(f"Bucket auth config method must be one of {valid_methods}")
        if auth_config:
            if auth_config.method in ("customer_managed_role", "aws_customer_managed_role") and not info.data["platform"] == "s3":
                raise ValueError("Customer managed role is only supported for s3 buckets.")
            if auth_config.method == "gcp_customer_managed_role" and not info.data["platform"] == "gs":
                raise ValueError("GCP customer managed role is only supported for gs buckets.")
            if auth_config.method == "r2_customer_managed_role":
                # Can't use _is_r2_bucket because of circular import issues
                if not (
                    info.data["platform"] == "s3-compatible"
                    and info.data["extra_config"].get("endpoint_url")
                    and ".r2." in info.data["extra_config"]["endpoint_url"]
                ):
                    raise ValueError("R2 customer managed role is only supported for R2 buckets.")
            if auth_config.method == "azure_credential_delegation" and not info.data["platform"] == "azure":
                raise ValueError("Azure credential delegation is only supported for azure buckets.")
            _validate_role_auth_shared_secret(auth_config)
        return auth_config if auth_config else None


class BucketModifyRequest(BaseModel):
    """A request with optional fields to modify a bucket's config on a per-field
    basis."""

    nickname: BucketNickname | None = None
    platform: Platform | None = None
    name: BucketName | None = None
    prefix: BucketPrefix | None = None
    extra_config: dict[str, Any] | None = None
    auth_config: AuthConfig | None = None

    @field_validator("name")
    @classmethod
    def validate_name_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) > MAX_BUCKET_NAME_LENGTH:
            raise ValueError(f"Bucket name must be at most {MAX_BUCKET_NAME_LENGTH} characters long.")
        return v

    @field_validator("prefix")
    @classmethod
    def validate_prefix_length(cls, v: str | None) -> str | None:
        if v is not None and len(v) > MAX_BUCKET_PREFIX_LENGTH:
            raise ValueError(f"Bucket prefix must be at most {MAX_BUCKET_PREFIX_LENGTH} characters long.")
        return v

    @field_validator("auth_config")
    @classmethod
    def validate_auth_config(cls, auth_config: AuthConfig | None) -> AuthConfig | None:
        if auth_config and auth_config.method not in [
            "customer_managed_role",
            "aws_customer_managed_role",
            "gcp_customer_managed_role",
            "r2_customer_managed_role",
            "azure_credential_delegation",
            "anonymous",
            "hmac",
        ]:
            # Deprecating bucket policy method
            raise ValueError("Bucket auth config method must be Anonymous, Customer Managed Role, or HMAC")
        _validate_role_auth_shared_secret(auth_config)
        return auth_config if auth_config else None


class BucketResponse(Bucket):
    """A response after successfully creating a bucket configuration."""

    is_default: bool
    auth_config: AuthConfig | None = None


class VirtualChunkAccessPolicyResponse(BaseModel):
    """Response body for a virtual chunk access policy."""

    use_case: str
    bucket_id: str
    subprefix: str | None = None
    public: bool
    url_prefix: str
    created: datetime
    created_by: str


class ExplicitVirtualChunkAccessPolicyResponse(BaseModel):
    """Response body for an explicit virtual chunk access policy."""

    bucket_id: str
    subprefix: str
    public: bool
    url_prefix: str
    created: datetime
    created_by: str


class RepoOperationMode(StrEnum):
    ONLINE = "online"
    MAINTENANCE = "maintenance"
    OFFLINE = "offline"


class NewRepoOperationStatus(BaseModel):
    mode: RepoOperationMode
    message: str | None = None


class RepoOperationStatusResponse(NewRepoOperationStatus):
    initiated_by: dict
    is_user_modifiable: bool = True
    estimated_end_time: datetime | None = None


class ModelWithID(BaseModel):
    id: DBID = Field(alias="_id")

    model_config = ConfigDict(populate_by_name=True, arbitrary_types_allowed=True)

    @field_validator("id", mode="before")
    @classmethod
    def validate_id(cls, id: Any) -> DBIDBytes:
        return to_dbid_bytes(id)

    @field_serializer("id")
    def serialize_id(self, id: DBID) -> str:
        return str(id)


def timedelta_from_seconds(v: Any) -> timedelta:
    if isinstance(v, (int, float)):
        return timedelta(seconds=v)
    if isinstance(v, timedelta):
        return v
    raise ValueError("input must be a timedelta or number of seconds")


class GCKeep(BaseModel):
    pass


class GCDeleteOlderThan(BaseModel):
    date: timedelta


GCAction = GCKeep | GCDeleteOlderThan


class GCConfig(BaseModel):
    """Configuration for garbage collection"""

    extra_gc_roots: set[str] = Field(default_factory=set)
    dangling_chunks: GCAction = Field(default_factory=GCKeep)
    dangling_manifests: GCAction = Field(default_factory=GCKeep)
    dangling_attributes: GCAction = Field(default_factory=GCKeep)
    dangling_transaction_logs: GCAction = Field(default_factory=GCKeep)
    dangling_snapshots: GCAction = Field(default_factory=GCKeep)
    gc_every: timedelta | None = None  # None means no gc
    enabled: bool = False

    @field_validator(
        "dangling_chunks", "dangling_manifests", "dangling_attributes", "dangling_transaction_logs", "dangling_snapshots", mode="before"
    )
    @classmethod
    def _parse_dangling(cls, v: Any) -> GCAction:
        if v is None:
            return GCKeep()
        if isinstance(v, (int, float)):
            return GCDeleteOlderThan(date=timedelta_from_seconds(v))
        else:
            # we let pydantic handle other cases
            return v

    @field_serializer("dangling_chunks", "dangling_manifests", "dangling_attributes", "dangling_transaction_logs", "dangling_snapshots")
    @classmethod
    def serialize_dangling(self, value: GCAction) -> float | None:
        if isinstance(value, GCKeep):
            return None
        else:
            assert isinstance(value, GCDeleteOlderThan)
            return value.date.total_seconds()

    @field_validator("gc_every", mode="before")
    @classmethod
    def parse_gc_every(cls, v: Any) -> timedelta | None:
        if v is not None:
            return timedelta_from_seconds(v)
        return None

    @field_serializer("gc_every")
    @classmethod
    def serialize_gc_every(self, value: timedelta | None) -> float | None:
        if value is not None:
            return value.total_seconds()
        return None


class ExpirationConfig(BaseModel):
    """Configuration for expiration"""

    expire_versions_older_than: timedelta
    expire_every: timedelta | None = None  # None means no expiration
    enabled: bool = False

    @field_validator("expire_every", "expire_versions_older_than", mode="before")
    @classmethod
    def parse_expire_every(cls, v: Any) -> timedelta | None:
        if v is not None:
            return timedelta_from_seconds(v)
        return None

    @field_serializer("expire_every", "expire_versions_older_than")
    @classmethod
    def serialize_expire_every(self, value: timedelta | None) -> float | None:
        if value is not None:
            return value.total_seconds()
        return None


class OptimizationWindow(BaseModel):
    """The preferred time to run optimization tasks on a repo"""

    duration: timedelta
    start_time: time  # Time of day in UTC
    day_of_week: int  # 0 = Monday, 6 = Sunday

    @field_validator("duration", mode="before")
    @classmethod
    def parse_duration(cls, v: Any) -> timedelta:
        return timedelta_from_seconds(v)

    @field_serializer("duration")
    @classmethod
    def serialize_duration(self, duration: timedelta) -> float:
        return duration.total_seconds()


class OptimizationConfig(BaseModel):
    """High-level config for repo optimizations"""

    window: OptimizationWindow | None = None  # If None, uses the org default
    gc_config: GCConfig | None = None
    expiration_config: ExpirationConfig | None = None


class NodeFilter(BaseModel):
    """Filter specification for dataset nodes using include/exclude path semantics."""

    include_paths: list[str] = Field(
        default_factory=list,
        description="Paths to include. Empty means include everything (before exclusions).",
    )
    exclude_paths: list[str] = Field(
        default_factory=list,
        description="Paths to exclude. Exclusion always wins over inclusion.",
    )

    @field_validator("exclude_paths", "include_paths", mode="before")
    @classmethod
    def validate_paths(cls, paths: list[str]) -> list[str]:
        """Check that paths are absolute, normalized, and unique."""
        if paths is None:
            return []
        normalized_paths = []
        for path in paths:
            if not path.startswith("/") or path.startswith("//"):
                raise ValueError(f"Path must be absolute (start with single '/'): {path}")
            # Use PurePosixPath to normalize and validate the path
            posix_path = PurePosixPath(path)
            normalized = posix_path.as_posix()
            if normalized != path:
                raise ValueError(f"Path must be normalized (no trailing '/', or '//'): {path!r} (normalized: {normalized!r})")
            # Check for . or .. components (PurePosixPath doesn't resolve these)
            if "." in posix_path.parts or ".." in posix_path.parts:
                raise ValueError(f"Path cannot contain '.' or '..' components: {path!r}")
            # Check for * and ? characters which could cause issues for downstream processing
            if "*" in path or "?" in path:
                raise ValueError(f"Path cannot contain '*' or '?' characters: {path!r}")
            normalized_paths.append(normalized)
        # Ensure uniqueness
        if len(normalized_paths) != len(set(normalized_paths)):
            raise ValueError(f"Duplicate paths not allowed: {paths}")
        return normalized_paths

    @model_validator(mode="after")
    def validate_not_empty(self) -> NodeFilter:
        """Reject empty filters - use None at DatasetFilter level instead."""
        if not self.include_paths and not self.exclude_paths:
            raise ValueError(
                "NodeFilter must have at least one include or exclude path. "
                "Use None at the DatasetFilter level to represent 'no filtering'."
            )
        return self


class DatasetFilter(BaseModel):
    """Dataset filter specification for marketplace listings and subscriptions.

    Used by:
    - source_filter: Provider-defined filter that sets the maximum sellable surface
    - target_filter: Subscriber-defined filter that selects a purchased subset
    """

    nodes: NodeFilter | None = Field(
        default=None,
        description="Node-level (groups and arrays) include/exclude filter. None means no filtering.",
    )


class SubscriptionStatus(StrEnum):
    """Status of a repo subscription"""

    ACTIVE = "active"
    ORPHANED = "orphaned"
    PENDING_CLAIM = "pending_claim"


class MarketplaceListingPricingModel(StrEnum):
    """Pricing model for marketplace listings."""

    FREE = "free"
    PAID = "paid"


class MarketplaceListing(BaseModel):
    """Marketplace listing information"""

    id: str
    repo_id: str | None
    org: str
    org_display_name: str | None = None
    org_description: str | None = None
    org_avatar: str | None = None
    org_email: str | None = None
    status: str
    repo_readme: str
    listing_name: str
    description: str | None = None
    license_text: str | None = None
    created_on: datetime
    last_updated: datetime
    thumbnail_url: str | None = None
    pricing_model: str = MarketplaceListingPricingModel.FREE
    featured_rank: float | None = None
    source_filter: DatasetFilter | None = None

    class Config:
        populate_by_name = True


class RepoSubscriptionInfo(BaseModel):
    """Information about a repo's subscription to a parent repo"""

    parent_repo: Repo | None
    status: SubscriptionStatus = SubscriptionStatus.ACTIVE
    subscription_type: SubscriptionType = SubscriptionType.DIRECT
    marketplace_listing: MarketplaceListing | None
    source_filter: DatasetFilter | None = None
    target_filter: DatasetFilter | None = None
    pricing_type: SubscriptionPricingType | None = None
    price_minor_units: int | None = None
    currency: str = "USD"


class Repo(ModelWithID):
    org: OrgName
    name: RepoName
    created: datetime = Field(default_factory=utc_now)
    updated: datetime
    description: str | None = None
    metadata: RepoMetadataT | None = None
    created_by: UUID | None = None
    visibility: RepoVisibility = RepoVisibility.PRIVATE
    subscription: RepoSubscriptionInfo | None = None
    bucket: BucketResponse | None = None
    status: RepoOperationStatusResponse
    kind: RepoKind = RepoKind.Icechunk
    prefix: str
    optimization_config: OptimizationConfig = Field(
        default_factory=lambda: OptimizationConfig(
            window=None,
            gc_config=None,
            expiration_config=None,
        )
    )
    permissions: list[Permission[RepoActions]] = Field(default_factory=list)

    def _asdict(self):
        """custom dict method ready to be serialized as json"""
        d = self.model_dump()
        d["id"] = str(d["id"])
        if self.created_by is not None:
            d["created_by"] = str(d["created_by"])
        if d["bucket"]:
            d["bucket"]["id"] = str(d["bucket"]["id"])
        if d["status"]["estimated_end_time"]:
            d["status"]["estimated_end_time"] = datetime_to_isoformat(d["status"]["estimated_end_time"])
        return d

    def __repr__(self) -> str:
        from arraylake.display.repo import reporepr

        return reporepr(self)

    @model_validator(mode="before")
    @classmethod
    def set_initial_updated(cls, data: Any) -> Any:
        if isinstance(data, dict) and "updated" not in data:
            data["updated"] = data.get("created", utc_now())
        return data

    @field_validator("created", "updated")
    @classmethod
    def timestamp_in_utc_tz(cls, v: datetime) -> datetime:
        return v.replace(tzinfo=UTC)

    @field_serializer("created", "updated")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)


class Author(BaseModel):
    name: str | None = None
    email: EmailStr

    def entry(self) -> str:
        if self.name:
            return f"{self.name} <{self.email}>"
        else:
            return f"<{self.email}>"


class OrgActions(Enum):
    """Actions a user can take on a specific org"""

    CAN_MANAGE_USERS = "CAN_MANAGE_USERS"
    CAN_WRITE_REPOS = "CAN_WRITE_REPOS"
    CAN_READ_REPOS = "CAN_READ_REPOS"
    CAN_READ_REPOS_WITH_FLUX = "CAN_READ_REPOS_WITH_FLUX"


class RepoActions(Enum):
    """Actions a user can take on a specific repo"""

    CAN_READ_WITH_FLUX = "CAN_READ_WITH_FLUX"
    CAN_READ = "CAN_READ"
    CAN_WRITE = "CAN_WRITE"
    CAN_MANAGE_USERS = "CAN_MANAGE_USERS"
    CAN_SYNC = "CAN_SYNC"


ActionType = TypeVar("ActionType", OrgActions, RepoActions)


class Permission(BaseModel, Generic[ActionType]):
    """Holds a permission"""

    principal_id: UUID
    actions: set[ActionType] = set()


class PermissionBody(BaseModel):
    principal_id: str
    resource: str
    action: str  # OrgActions | RepoActions


class PermissionCheckResponse(BaseModel):
    has_permission: bool


class TokenAuthenticateBody(BaseModel):
    token: str


class TokenAuthenticateResponse(BaseModel):
    client_id: UUID


class OauthTokensResponse(BaseModel):
    access_token: SecretStr
    id_token: SecretStr
    refresh_token: SecretStr | None = None
    expires_in: int
    token_type: str

    def dict(self, **kwargs) -> dict[str, Any]:
        """custom dict that drops default values"""
        tokens = super().model_dump(**kwargs)
        # special case: drop refresh token if it is None
        if not tokens.get("refresh_token", 1):
            del tokens["refresh_token"]
        return tokens

    @field_serializer("access_token", "id_token", "refresh_token", when_used="unless-none")
    def dump_secret(self, v) -> str:
        if isinstance(v, SecretStr):
            return v.get_secret_value()
        return v


class OauthTokens(OauthTokensResponse):
    refresh_token: SecretStr

    def dict(self, **kwargs) -> dict[str, Any]:
        """custom dict method that decodes secrets"""
        tokens = super().model_dump(**kwargs)
        for k, v in tokens.items():
            if isinstance(v, SecretStr):
                tokens[k] = v.get_secret_value()
        return tokens

    def __hash__(self):
        return hash((self.access_token, self.id_token, self.refresh_token, self.expires_in, self.token_type))


class AuthProviderConfig(BaseModel):
    """
    Used to communicate Auth0 configuration to Arraylake Client/CLI
    """

    domain: str
    client_id: str


class UserInfo(BaseModel):
    id: UUID
    first_name: str | None = None
    family_name: str | None = None
    email: EmailStr

    def as_author(self) -> Author:
        return Author(name=f"{self.first_name} {self.family_name}", email=self.email)


class ApiTokenInfo(BaseModel):
    id: UUID
    client_id: str
    email: EmailStr
    expiration: int

    def as_author(self) -> Author:
        return Author(email=self.email)


class UserDiagnostics(BaseModel):
    system: dict[str, str] | None = None
    versions: dict[str, str] | None = None
    config: dict[str, str] | None = None
    service: dict[str, str] | None = None


class ApiClientResponse(BaseModel):
    id: UUID = Field(alias="_id")
    email: EmailStr
    created: datetime
    expiration: datetime
    last_used: datetime | None = None

    @field_serializer("created", "expiration", "last_used")
    def serialize_datetime(self, dt: datetime) -> str:
        return datetime_to_isoformat(dt)


class S3Credentials(BaseModel):
    aws_access_key_id: str
    aws_secret_access_key: str
    aws_session_token: str | None
    expiration: datetime | None


class GSCredentials(BaseModel):
    access_token: str
    principal: str
    expiration: datetime | None


class AzureCredentials(BaseModel):
    sas_token: str  # User delegation SAS token
    storage_account: str  # Storage account name
    expiration: datetime | None  # Token expiration


TempCredentials: TypeAlias = S3Credentials | GSCredentials | AzureCredentials


### Icechunk workarounds
# GcsBearerCredential is not included in AnyGcsCredential, so we need to create a new type alias
ICECHUNK_ANY_CREDENTIAL: TypeAlias = (
    icechunk.AnyS3Credential | icechunk.GcsBearerCredential | icechunk.AnyGcsCredential | icechunk.AnyAzureCredential | None
)


class VirtualChunkCredentials(BaseModel):
    """Credentials and refresh metadata for a single virtual chunk bucket.

    The org, bucket_nickname, and platform fields are needed so the client can
    construct credential refresh closures for delegated-creds buckets.

    The store config fields (region, endpoint_url, allow_http, force_path_style)
    allow the client to construct VirtualChunkContainer objects without extra
    API calls to fetch the full bucket config.
    """

    # TODO: consider a dedicated server-side refresh endpoint to avoid exposing cross-org metadata to the client?
    credentials: TempCredentials | None = None
    org: OrgName
    bucket_nickname: BucketNickname
    platform: Platform
    # If set, create a VCC with this name at runtime (e.g., for filtered subscriptions
    # where subsync writes placeholder refs like vcc://__al_source/CHUNK_ID)
    # If None, assume the VCC already exists
    runtime_vcc_name: str | None = None
    # Store config fields for constructing VCCs without extra get_bucket_config() calls.
    # Populated from the bucket's extra_config via from_bucket().
    region: str | None = None
    endpoint_url: str | None = None
    allow_http: bool = False
    force_path_style: bool = False

    @classmethod
    def from_bucket(
        cls,
        org: OrgName,
        bucket: BucketModel,
        credentials: TempCredentials | None,
    ) -> VirtualChunkCredentials:
        """Build VirtualChunkCredentials from a bucket model, extracting store config fields."""
        extra = bucket.extra_config
        use_ssl = extra.get("use_ssl", True)
        region = extra.get("region_name")
        endpoint_url = extra.get("endpoint_url")
        return cls(
            credentials=credentials,
            org=org,
            bucket_nickname=bucket.nickname,
            platform=bucket.platform,
            region=str(region) if region is not None else None,
            endpoint_url=str(endpoint_url) if endpoint_url is not None else None,
            allow_http=not use_ssl,
            force_path_style=bool(extra.get("force_path_style", False if use_ssl else True)),
        )

    def to_vcc_store_config(self, user_id: UUID | None = None) -> icechunk.AnyObjectStoreConfig:
        """Create an Icechunk ObjectStoreConfig from the embedded store config fields."""
        if self.platform in ("s3", "s3-compatible", "minio"):
            options = icechunk.S3Options(
                region=self.region,
                endpoint_url=self.endpoint_url,
                allow_http=self.allow_http,
                force_path_style=self.force_path_style,
            )
            return icechunk.ObjectStoreConfig.S3(options)
        elif self.platform == "gs":
            from arraylake import __version__ as arraylake_version

            config = {"user_agent": f"arraylake/{arraylake_version} (uuid={str(user_id)})" if user_id else f"arraylake/{arraylake_version}"}
            return icechunk.ObjectStoreConfig.Gcs(config)
        elif self.platform == "azure":
            return icechunk.ObjectStoreConfig.Azure({})
        else:
            raise ValueError(f"Unsupported platform for VCC store config: {self.platform}")


class OpenRepoResponse(BaseModel):
    """Everything the client needs to open an icechunk repo."""

    # Repo storage
    repo_bucket: BucketResponse
    repo_prefix: str
    repo_credentials: TempCredentials | None = None
    # Virtual chunks: VCC url_prefix -> credentials + refresh metadata
    # TODO: use a dedicated VccUrlPrefix type? Can't use BucketPrefix because VCC URL prefixes
    # (e.g. "s3://bucket/") can have trailing slashes, which BucketPrefix rejects.
    virtual_chunk_credentials: dict[str, VirtualChunkCredentials]
    # Author
    author: Author
    # Principal (for user-agent string in icechunk storage)
    principal_id: str
    # Repo operation status
    status: RepoOperationStatusResponse
