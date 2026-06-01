"""
The Client module contains the main classes used to interact with the Arraylake service.
For asyncio interaction, use the #AsyncClient. For regular, non-async interaction, use the #Client.

**Example usage:**

```python
from arraylake import Client
client = Client()
repo = client.get_repo("my-org/my-repo")
```
"""

# mypy: disable-error-code="name-defined"
from __future__ import annotations

import warnings
from collections.abc import AsyncGenerator, Callable, Generator, Mapping
from datetime import UTC
from functools import partial
from typing import TYPE_CHECKING, Literal
from urllib.parse import urlparse
from uuid import UUID

import icechunk
from icechunk import IcechunkError, RepositoryConfig
from icechunk import Repository as IcechunkRepository

from arraylake._credential_cache import CredentialCacheKey, get_or_refresh
from arraylake.asyn import async_gather_tasks, asyncio_run, sync
from arraylake.compute.services import AsyncComputeClient, ComputeClient
from arraylake.config import config as arraylake_config
from arraylake.config import default_service_uri
from arraylake.credentials import (
    _get_hmac_credentials,
    _is_r2_bucket,
    _use_anonymous_credentials,
    _use_delegated_credentials,
    _use_hmac_credentials,
)
from arraylake.display.repolist import RepoList
from arraylake.exceptions import BucketNotFoundError
from arraylake.log_util import get_logger
from arraylake.metastore import HttpMetastore, HttpMetastoreConfig
from arraylake.repos.icechunk.storage import (
    _get_credential_type,
    _get_icechunk_storage_obj,
)
from arraylake.repos.icechunk.virtual import (
    create_virtual_chunk_container,
    forbid_unsafe_virtual_bucket_configs,
    forbid_unsafe_virtual_chunk_containers,
    get_icechunk_container_credentials,
    reject_unresolvable_vccs,
)
from arraylake.token import get_auth_handler
from arraylake.types import (
    ICECHUNK_ANY_CREDENTIAL,
    URI,
    ApiClientResponse,
    Author,
    AzureCredentials,
    BucketNickname,
    BucketPrefix,
    BucketResponse,
    ExplicitVirtualChunkAccessPolicyResponse,
    GSCredentials,
    NewBucket,
    OptimizationConfig,
    OrgActions,
    OrgAndRepoName,
    OrgName,
    RepoActions,
    RepoKind,
    RepoMetadataT,
    RepoName,
    RepoOperationMode,
    RepoOperationStatusResponse,
    S3Credentials,
    StorageOptions,
    TempCredentials,
    validate_name,
    validate_org_and_repo_name,
)
from arraylake.types import Repo as RepoModel

if TYPE_CHECKING:
    import obstore as obs

logger = get_logger(__name__)

_VALID_NAME = r"(\w[\w\.\-_]+)"


def _parse_org_and_repo(org_and_repo: OrgAndRepoName) -> tuple[OrgName, RepoName]:
    validate_org_and_repo_name(org_and_repo)
    parts = org_and_repo.split("/")
    return (parts[0], parts[1])


def _validate_service_uri(service_uri: str) -> None:
    if not service_uri.startswith("http"):
        raise ValueError("service uri must start with http")


def _default_token() -> str | None:
    return arraylake_config.get("token", None)


class AsyncClient:
    """Asyncio Client for interacting with ArrayLake

    Args:
        service_uri:
            [Optional] The service URI to target.
        token:
            [Optional] API token for service account authentication.
        cache_credentials:
            [Optional] When True (default), delegated bucket credentials are
            served from a process-wide cache so all consumers in a worker
            share one in-flight refresh per ``(auth, target, access)``. Set
            to False for server-side contexts that should not retain
            credentials in memory — every call hits the server.
    """

    _service_uri: str | None
    token: str | None
    _cache_credentials: bool

    def __init__(self, service_uri: str | None = None, token: str | None = None, cache_credentials: bool = True) -> None:
        if service_uri is not None:
            _validate_service_uri(service_uri)

        self._service_uri = service_uri

        if token is None:
            token = _default_token()

        if token is not None and (not token.startswith("ema_") and not token.startswith("ey")):
            # Ignore telling the user they can use JWT tokens, shhhh
            raise ValueError("Invalid token provided. Tokens must start with ema_ or be a JWT token.")

        self.token = token
        self._cache_credentials = cache_credentials

    @property
    def service_uri(self) -> str:
        """
        The service URI to target.

        If a URI was explicitly set in the client constructor it uses that, else it uses the global config,
        and if not set there it defaults to ``https://api.earthmover.io``.
        """
        if self._service_uri is not None:
            api_endpoint = self._service_uri
        else:
            api_endpoint = default_service_uri()

        _validate_service_uri(api_endpoint)

        return api_endpoint

    def __repr__(self):
        return f"arraylake.AsyncClient(service_uri='{self.service_uri}')"

    def _metastore_for_org(self, org: OrgName) -> HttpMetastore:
        validate_name(org, entity="org")
        return HttpMetastore(HttpMetastoreConfig(self.service_uri, org, self.token))

    async def list_repos(self, org: OrgName, filter_metadata: RepoMetadataT | None = None) -> RepoList:
        """List all repositories for the specified org

        Args:
            org: Name of the org
            filter_metadata: Optional metadata to filter the repos by.
                If provided, only repos with the specified metadata will be returned.
                Filtering is inclusive and will return repos that match all of the provided metadata.
        """

        mstore = self._metastore_for_org(org)
        repo_models = await mstore.list_databases(filter_metadata)
        return RepoList(repo_models, org=org)

    async def list_repos_paginated(
        self,
        org: OrgName,
        filter_metadata: RepoMetadataT | None = None,
        page_size: int = 50,
    ) -> AsyncGenerator[RepoModel, None]:
        """List repositories for the specified org, yielding results page by page.

        This is a generator that lazily fetches pages from the server.

        Args:
            org: Name of the org
            filter_metadata: Optional metadata to filter the repos by.
            page_size: Number of repos per page.

        Yields:
            Repo objects one at a time, fetching pages as needed.
        """
        mstore = self._metastore_for_org(org)
        page = 1
        while True:
            result = await mstore.list_databases_page(
                filter_metadata=filter_metadata,
                page=page,
                size=page_size,
            )
            for repo in result.items:
                yield repo
            if result.page >= result.pages:
                break
            page += 1

    async def _get_s3_delegated_credentials_from_repo(self, org: OrgName, repo_name: RepoName) -> S3Credentials:
        """Get delegated credentials for a repo's S3 bucket.

        Args:
            org: Name of the organization.
            repo_name: Name of the repository.

        Returns:
            S3Credentials: Temporary credentials for the S3 bucket.
        """
        key = CredentialCacheKey(
            api_url=self.service_uri,
            auth_key=hash(self.token),
            scope="repo",
            org=org,
            identifier=repo_name,
            platform="s3",
        )

        async def fetch() -> S3Credentials:
            mstore = self._metastore_for_org(org)
            return await mstore.get_s3_bucket_credentials_from_repo(repo_name)

        creds = await get_or_refresh(key, fetch, use_cache=self._cache_credentials)
        assert isinstance(creds, S3Credentials)
        return creds

    async def _get_gcs_delegated_credentials_from_repo(self, org: OrgName, repo_name: RepoName) -> GSCredentials:
        """Get delegated credentials for a repo's GCS bucket.

        Args:
            org: Name of the organization.
            repo_name: Name of the repository.

        Returns:
            GSCredentials: Temporary credentials for the GCS bucket.
        """
        key = CredentialCacheKey(
            api_url=self.service_uri,
            auth_key=hash(self.token),
            scope="repo",
            org=org,
            identifier=repo_name,
            platform="gs",
        )

        async def fetch() -> GSCredentials:
            mstore = self._metastore_for_org(org)
            return await mstore.get_gs_bucket_credentials_from_repo(repo_name)

        creds = await get_or_refresh(key, fetch, use_cache=self._cache_credentials)
        assert isinstance(creds, GSCredentials)
        return creds

    async def _get_azure_delegated_credentials_from_repo(self, org: OrgName, repo_name: RepoName) -> AzureCredentials:
        """Get delegated credentials for a repo's Azure Blob Storage container.

        Args:
            org: Name of the organization.
            repo_name: Name of the repository.

        Returns:
            AzureCredentials: Temporary credentials for the Azure Blob Storage container.
        """
        key = CredentialCacheKey(
            api_url=self.service_uri,
            auth_key=hash(self.token),
            scope="repo",
            org=org,
            identifier=repo_name,
            platform="azure",
        )

        async def fetch() -> AzureCredentials:
            mstore = self._metastore_for_org(org)
            return await mstore.get_azure_container_credentials_from_repo(repo_name)

        creds = await get_or_refresh(key, fetch, use_cache=self._cache_credentials)
        assert isinstance(creds, AzureCredentials)
        return creds

    async def _get_s3_delegated_credentials_from_bucket(
        self, org: OrgName, nickname: BucketNickname, access: Literal["read", "write"] = "read"
    ) -> S3Credentials:
        """Get delegated credentials for an S3 bucket.

        Defaults to read-only credentials. Pass ``access="write"`` to request read+write
        credentials; the caller must have ``CAN_MANAGE_USERS`` on the org.

        Args:
            org: Name of the organization that the bucket belongs to.
            nickname: Nickname of the bucket.
            access: ``"read"`` (default) or ``"write"``.

        Returns:
            S3Credentials: Temporary credentials for the S3 bucket.
        """
        key = CredentialCacheKey(
            api_url=self.service_uri,
            auth_key=hash(self.token),
            scope="bucket",
            org=org,
            identifier=nickname,
            platform="s3",
            access=access,
        )

        async def fetch() -> S3Credentials:
            mstore = self._metastore_for_org(org)
            bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
            return await mstore.get_s3_bucket_credentials_from_bucket(bucket_id, access=access)

        creds = await get_or_refresh(key, fetch, use_cache=self._cache_credentials)
        assert isinstance(creds, S3Credentials)
        return creds

    async def _get_gcs_delegated_credentials_from_bucket(
        self, org: RepoName, nickname: BucketNickname, access: Literal["read", "write"] = "read"
    ) -> GSCredentials:
        """Get delegated credentials for a GCS bucket.

        Defaults to read-only credentials. Pass ``access="write"`` to request read+write
        credentials; the caller must have ``CAN_MANAGE_USERS`` on the org.

        Args:
            org: Name of the organization that the bucket belongs to.
            nickname: Nickname of the bucket.
            access: ``"read"`` (default) or ``"write"``.

        Returns:
            GSCredentials: Temporary credentials for the GCS bucket.
        """
        key = CredentialCacheKey(
            api_url=self.service_uri,
            auth_key=hash(self.token),
            scope="bucket",
            org=org,
            identifier=nickname,
            platform="gs",
            access=access,
        )

        async def fetch() -> GSCredentials:
            mstore = self._metastore_for_org(org)
            bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
            return await mstore.get_gs_bucket_credentials_from_bucket(bucket_id, access=access)

        creds = await get_or_refresh(key, fetch, use_cache=self._cache_credentials)
        assert isinstance(creds, GSCredentials)
        return creds

    async def _get_azure_delegated_credentials_from_bucket(
        self, org: RepoName, nickname: BucketNickname, access: Literal["read", "write"] = "read"
    ) -> AzureCredentials:
        """Get delegated credentials for an Azure Blob Storage container.

        Defaults to read-only credentials. Pass ``access="write"`` to request read+write
        credentials; the caller must have ``CAN_MANAGE_USERS`` on the org.

        Args:
            org: Name of the organization that the bucket belongs to.
            nickname: Nickname of the bucket.
            access: ``"read"`` (default) or ``"write"``.

        Returns:
            AzureCredentials: Temporary credentials for the Azure Blob Storage container.
        """
        key = CredentialCacheKey(
            api_url=self.service_uri,
            auth_key=hash(self.token),
            scope="bucket",
            org=org,
            identifier=nickname,
            platform="azure",
            access=access,
        )

        async def fetch() -> AzureCredentials:
            mstore = self._metastore_for_org(org)
            bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
            return await mstore.get_azure_container_credentials_from_bucket(bucket_id, access=access)

        creds = await get_or_refresh(key, fetch, use_cache=self._cache_credentials)
        assert isinstance(creds, AzureCredentials)
        return creds

    def _get_icechunk_s3_credentials_refresh_function_for_repo(self, org: OrgName, repo_name: RepoName) -> icechunk.S3StaticCredentials:
        """Get a function that returns S3 credentials for the given org and repo
        for credential refreshes in Icechunk.

        The returned Callable may not have any args, must return a new
        S3StaticCredentials object, and must be synchronous.

        Args:
            org: Name of the org
            repo_name: Name of the repo

        Returns:
            Callable: Function that returns a S3StaticCredentials object.
        """
        s3_credentials = asyncio_run(self._get_s3_delegated_credentials_from_repo(org, repo_name), timeout=None)
        return icechunk.S3StaticCredentials(
            access_key_id=s3_credentials.aws_access_key_id,
            secret_access_key=s3_credentials.aws_secret_access_key,
            session_token=s3_credentials.aws_session_token,
            expires_after=s3_credentials.expiration,
        )

    def _get_icechunk_gcs_credentials_refresh_function_for_repo(self, org: OrgName, repo_name: RepoName) -> icechunk.GcsBearerCredential:
        """Get a function that returns GCS credentials for the given org and repo
        for credential refreshes in Icechunk.

        The returned Callable may not have any args, must return a new
        GcsBearerCredential object, and must be synchronous.

        Args:
            org: Name of the org
            repo_name: Name of the repo

        Returns:
            Callable: Function that returns a GcsBearerCredential object.
        """
        gcs_credentials = asyncio_run(self._get_gcs_delegated_credentials_from_repo(org, repo_name), timeout=None)
        return icechunk.GcsBearerCredential(
            bearer=gcs_credentials.access_token,
            expires_after=gcs_credentials.expiration.replace(tzinfo=UTC) if gcs_credentials.expiration else None,
        )

    def _get_icechunk_azure_credentials_refresh_function_for_repo(
        self, org: OrgName, repo_name: RepoName
    ) -> icechunk.AzureStaticCredentials:
        raise NotImplementedError("Azure credential refreshes not implemented in Icechunk.")

    def _get_icechunk_s3_credentials_refresh_function_for_bucket(
        self, org: OrgName, nickname: BucketNickname
    ) -> icechunk.S3StaticCredentials:
        """Get a function that returns S3 credentials for the given org and bucket
        for credential refreshes in Icechunk.

        The returned Callable may not have any args, must return a new
        S3StaticCredentials object, and must be synchronous.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket

        Returns:
            Callable: Function that returns a S3StaticCredentials object.
        """
        s3_credentials = asyncio_run(self._get_s3_delegated_credentials_from_bucket(org, nickname), timeout=None)
        return icechunk.S3StaticCredentials(
            access_key_id=s3_credentials.aws_access_key_id,
            secret_access_key=s3_credentials.aws_secret_access_key,
            session_token=s3_credentials.aws_session_token,
            expires_after=s3_credentials.expiration,
        )

    def _get_icechunk_gcs_credentials_refresh_function_for_bucket(
        self, org: OrgName, nickname: BucketNickname
    ) -> icechunk.GcsBearerCredential:
        """Get a function that returns GCS credentials for the given org and bucket
        for credential refreshes in Icechunk.

        The returned Callable may not have any args, must return a new
        GcsBearerCredential object, and must be synchronous.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket

        Returns:
            Callable: Function that returns a GcsBearerCredential object.
        """
        gcs_credentials = asyncio_run(self._get_gcs_delegated_credentials_from_bucket(org, nickname), timeout=None)
        return icechunk.GcsBearerCredential(
            bearer=gcs_credentials.access_token,
            expires_after=gcs_credentials.expiration.replace(tzinfo=UTC) if gcs_credentials.expiration else None,
        )

    def _get_icechunk_azure_credentials_refresh_function_for_bucket(
        self, org: OrgName, nickname: BucketNickname
    ) -> icechunk.AzureStaticCredentials:
        raise NotImplementedError("Azure credential refreshes not implemented in Icechunk.")

    async def _maybe_get_credentials_for_icechunk(
        self,
        bucket: BucketResponse,
        org: OrgName,
        repo_name: RepoName | None,
        bucket_access: Literal["read", "write"] = "read",
    ) -> TempCredentials | None:
        """Checks if the bucket is configured for delegated or HMAC credentials and gets the
        credentials if it is configured.

        Returns None if delegated or HMAC credentials are not configured for the bucket.

        ``bucket_access`` only applies when ``repo_name`` is None (the bucket-scoped path);
        repo-scoped credential fetches always inherit the caller's permissions on the repo.
        """
        if _use_delegated_credentials(bucket):
            if bucket.platform == "s3" or _is_r2_bucket(bucket):
                if repo_name:
                    return await self._get_s3_delegated_credentials_from_repo(org, repo_name)
                else:
                    return await self._get_s3_delegated_credentials_from_bucket(org, bucket.nickname, access=bucket_access)
            elif bucket.platform == "gs":
                if repo_name:
                    return await self._get_gcs_delegated_credentials_from_repo(org, repo_name)
                else:
                    return await self._get_gcs_delegated_credentials_from_bucket(org, bucket.nickname, access=bucket_access)
            elif bucket.platform == "azure":
                if repo_name:
                    return await self._get_azure_delegated_credentials_from_repo(org, repo_name)
                else:
                    return await self._get_azure_delegated_credentials_from_bucket(org, bucket.nickname, access=bucket_access)
            else:
                raise ValueError(f"Unsupported platform for delegated credentials: {bucket.platform}")
        elif _use_hmac_credentials(bucket):
            return await _get_hmac_credentials(bucket)
        return None

    def _maybe_get_credential_refresh_func_for_icechunk(
        self, bucket: BucketResponse, org: OrgName, repo_name: RepoName | None
    ) -> Callable | None:  # Removed S3StaticCredentials output type so icechunk import is not required
        """Checks if the bucket is configured for delegated credentials and gets the
        refresh function if it is configured.

        Returns None if delegated credentials are not configured for the bucket.
        """
        if _use_delegated_credentials(bucket):
            if bucket.platform == "s3" or _is_r2_bucket(bucket):
                if repo_name:
                    return partial(self._get_icechunk_s3_credentials_refresh_function_for_repo, org, repo_name)
                else:
                    return partial(self._get_icechunk_s3_credentials_refresh_function_for_bucket, org, bucket.nickname)
            elif bucket.platform == "gs":
                if repo_name:
                    return partial(self._get_icechunk_gcs_credentials_refresh_function_for_repo, org, repo_name)
                else:
                    return partial(self._get_icechunk_gcs_credentials_refresh_function_for_bucket, org, bucket.nickname)
            elif bucket.platform == "azure":
                # Credential refreshes currently not implemented in Icechunk, return None
                return None
            else:
                raise ValueError(f"Unsupported platform for delegated credentials: {bucket.platform}")
        return None

    async def get_repo_object(self, name: OrgAndRepoName) -> RepoModel:
        """Get the repo configuration object.

        See `get_repo` for an instantiated repo.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)

        repo_model = await mstore.get_database(repo_name)
        return repo_model

    async def get_repo(
        self,
        name: OrgAndRepoName,
        *,
        config: icechunk.RepositoryConfig | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IcechunkRepository:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            config: Optional config for the repo.
                This is the `icechunk.RepositoryConfig`.
                Config settings passed here will take precedence over
                the stored repo config when opening the repo.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
                If not supplied this method will attempt to auto-discover them,
                by inspecting the icechunk repository config for any virtual chunk containers,
                and attempting to authorize all of them.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

        Returns:
            A icechunk.Repository object.
        """
        from arraylake import __version__ as arraylake_version

        if isinstance(config, RepositoryConfig):
            pass
        elif config is None:
            # config object is really a config diff - so `RepositoryConfig.default()` will not override any existing configuration
            config = icechunk.RepositoryConfig.default()
        else:
            raise ValueError(f"config must be an icechunk.RepositoryConfig object or None: {config}.")

        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)

        # Single API call to get everything needed to open the repo
        response = await mstore.open_repo(repo_name)

        if response.status.mode == RepoOperationMode.OFFLINE:
            raise ValueError(f"Repository is offline, check back after {response.status.estimated_end_time}")
        elif response.status.mode == RepoOperationMode.MAINTENANCE:
            warnings.warn(
                f"Repository is in maintenance mode until {response.status.estimated_end_time}, do not attempt to write to the store"
            )

        # Build icechunk storage from the response
        credential_refresh_func = self._maybe_get_credential_refresh_func_for_icechunk(
            bucket=response.repo_bucket, org=org, repo_name=repo_name
        )
        credentials = response.repo_credentials if credential_refresh_func is None else None
        icechunk_storage = _get_icechunk_storage_obj(
            bucket_config=response.repo_bucket,
            prefix=response.repo_prefix,
            credential_type=_get_credential_type(credentials, credential_refresh_func),
            credentials=credentials,
            credential_refresh_func=credential_refresh_func,
            scatter_initial_credentials=arraylake_config.get("icechunk.scatter_initial_credentials", True),
            arraylake_version=arraylake_version,
            user_id=UUID(response.principal_id),
            storage_options=storage_options,
        )

        # Check if the user passed a custom config with VCCs that weren't authorized by the repo writer
        server_authorized_vcc_prefixes = set(response.virtual_chunk_credentials.keys())
        config_vccs = config.virtual_chunk_containers if config.virtual_chunk_containers is not None else {}
        if config_vccs:
            unauthorized_vccs = set(config_vccs.keys()) - server_authorized_vcc_prefixes
            if unauthorized_vccs:
                # TODO this is likely uneccessarily restrictive
                raise ValueError(
                    f"All virtual chunk access must be pre-authorized by a user with repo writer permissions, not just by the user reading the repo. "
                    f"The following virtual chunk container prefixes in your custom config were not authorized by a repo writer: {unauthorized_vccs}"
                )

        # Resolve VCC credentials
        vcc_credentials: dict[BucketPrefix, icechunk.AnyCredential | None]
        if authorize_virtual_chunk_access is not None:
            # User explicitly provided VCC overrides — fetch credentials for those buckets
            # This incurs an extra roundtrip to the DB but it's not the happy-path so that's okay.
            vcc_credentials = await self._containers_credentials_for_buckets(
                org,
                containers_to_buckets_map=dict(authorize_virtual_chunk_access),
                forbid_configs_unsafe_for_virtual_chunks=True,
            )
        else:
            # Use server-provided VCC credentials
            vcc_credentials = {}
            if response.virtual_chunk_credentials:
                credentials_map: dict[str, icechunk.AnyS3Credential | icechunk.AnyGcsCredential | icechunk.AnyAzureCredential | None] = {}
                for vcc_prefix, vcc_creds in response.virtual_chunk_credentials.items():
                    # Create VCC objects for all server-provided VCCs, not just runtime ones,
                    # because icechunk's config merge replaces virtual_chunk_containers
                    # rather than extending them.
                    store_config = vcc_creds.to_vcc_store_config(user_id=UUID(response.principal_id))
                    container = icechunk.VirtualChunkContainer(
                        url_prefix=vcc_prefix,
                        store=store_config,
                    )
                    if vcc_creds.runtime_vcc_name is not None:
                        container.name = vcc_creds.runtime_vcc_name
                    config.set_virtual_chunk_container(container)

                    # TODO: build refresh closures here using vcc_creds.org, vcc_creds.bucket_nickname,
                    # and vcc_creds.platform so that credentials can be refreshed when they expire. (See https://github.com/earth-mover/arraylake/issues/5122)
                    # TODO: support Azure virtual chunk credentials
                    if isinstance(vcc_creds.credentials, AzureCredentials):
                        raise NotImplementedError(f"Azure virtual chunk credentials are not yet supported. (prefix: {vcc_prefix}).")
                    # TODO: fix return type of get_icechunk_container_credentials (returns GcsBearerCredential
                    # which is not in icechunk's AnyGcsCredential union — icechunk typing gap)
                    credentials_map[vcc_prefix] = get_icechunk_container_credentials(  # type: ignore[assignment]
                        bucket_platform=vcc_creds.platform,
                        credentials=vcc_creds.credentials,
                        credential_refresh_func=None,
                    )
                vcc_credentials = icechunk.containers_credentials(credentials_map)

        ic_repo: IcechunkRepository = await IcechunkRepository.open_async(
            icechunk_storage,
            config=config,
            authorize_virtual_chunk_access=vcc_credentials,
        )

        ic_repo.set_default_commit_metadata({"author_name": response.author.name, "author_email": response.author.email})

        return ic_repo

    async def _maybe_fetch_credentials_for_virtual_chunks(
        self,
        org: OrgName,
        config: icechunk.RepositoryConfig,
        pre_authorized_vccs: Mapping[BucketPrefix, BucketNickname | None],
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None,
    ) -> dict[BucketPrefix, icechunk.AnyCredential | None]:
        """
        Fetch credentials for accessing any virtual chunks.

        If there is no need to get any credentials for virtual chunks, this function is meant to detect that as quickly as possible without doing extra remote requests.
        This could happen either because `authorize_virtual_chunk_access` is explicitly an empty dict, or because pre-fetching the repo config found no VCCs.

        Note that we (currently) don't actually need to know the name of the repo in arraylake to do this - we only need to know about the IC repo config (for the VCCs),
        and which buckets are "pre-authorized" for virtual access (currently defined as all anonymous access buckets in the same org).

        Args:
            org: The organization the repo belongs to.
            config: icechunk.RepositoryConfig - the config the user asked for by passing it to `.get_repo`
            pre_authorized_vccs: Mapping[BucketPrefix, BucketNickname | None]
                VCCs fetched from the server. Nicknames may be None if the server could not resolve
                the VCC to a bucket config. Must be supplied as complete urls.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
                Acts an an optional override of the default behaviour, which is to authorize using `pre_authorized_vccs`.

        Returns:
            prefixes_credential_mapping
        """

        # if `authorize_virtual_chunk_access` was set explicitly then it should take precedence
        # else we should use whatever was authorized by the repo writer (i.e. the `pre_authorized_vccs`)
        vccs = authorize_virtual_chunk_access if authorize_virtual_chunk_access is not None else pre_authorized_vccs
        buckets_to_authenticate = reject_unresolvable_vccs(vccs)

        # Check if the user passed a custom config with VCCs that weren't authorized by the writer,
        # otherwise this would be a sneaky way to get around the requirement for the repo writer to authorize all VCCs
        config_vccs = config.virtual_chunk_containers if config.virtual_chunk_containers is not None else {}
        if config_vccs:
            unauthorized_vccs = set(config_vccs.keys()) - set(pre_authorized_vccs.keys())
            if unauthorized_vccs:
                raise ValueError(
                    f"All virtual chunk access must be pre-authorized by the repo writer, not just by the reader. "
                    f"The following virtual chunk container prefixes in your custom config were not authorized by the repo writer: {unauthorized_vccs}"
                )

        # fetch credentials for any buckets containing virtual chunks
        prefixes_credential_mapping = await self._containers_credentials_for_buckets(
            org,
            containers_to_buckets_map=buckets_to_authenticate,
            forbid_configs_unsafe_for_virtual_chunks=True,
        )

        return prefixes_credential_mapping

    async def get_or_create_repo(
        self,
        name: OrgAndRepoName,
        *,
        bucket_config_nickname: BucketNickname | None = None,
        prefix: str | None = None,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        config: icechunk.RepositoryConfig | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IcechunkRepository:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO]).
            bucket_config_nickname: Bucket in which the underlying Icechunk repo will be created.
                If the repo exists, bucket_config_nickname is ignored.
            prefix: Optional prefix for Icechunk store. If not provided, a random ID + the repo name will be used.
            description: Optional description for the repo.
            metadata: Optional dictionary of metadata to tag the repo with.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            config: Optional config for the repo.
                This is the `icechunk.RepositoryConfig`.
                Config settings passed here will take precedence over the stored repo config when opening the repo.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
                If not supplied this method will attempt to auto-discover them,
                by inspecting the icechunk repository config for any virtual chunk containers,
                and attempting to authorize all of them.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

        Returns:
            An icechunk.Repository object
        """
        org, repo_name = _parse_org_and_repo(name)
        repos = [r for r in await self.list_repos(org) if r.name == repo_name]
        if repos:
            (repo,) = repos
            if bucket_config_nickname:
                if not repo.bucket:
                    raise ValueError(
                        "This repo exists, but does not have a bucket config attached. Please remove the bucket_config_nickname argument."
                    )
                elif bucket_config_nickname != repo.bucket.nickname:
                    raise ValueError(
                        f"This repo exists, but the provided {bucket_config_nickname=} "
                        f"does not match the configured bucket_config_nickname {repo.bucket.nickname!r}."
                    )
                elif not repo.bucket:
                    raise ValueError(
                        "This repo exists, but does not have a bucket config attached. Please remove the bucket_config_nickname argument."
                    )

            return await self.get_repo(
                name,
                config=config,
                authorize_virtual_chunk_access=authorize_virtual_chunk_access,
                storage_options=storage_options,
            )
        else:
            return await self.create_repo(
                name,
                bucket_config_nickname=bucket_config_nickname,
                prefix=prefix,
                description=description,
                metadata=metadata,
                config=config,
                authorize_virtual_chunk_access=authorize_virtual_chunk_access,
                storage_options=storage_options,
            )

    async def create_repo(
        self,
        name: OrgAndRepoName,
        *,
        bucket_config_nickname: BucketNickname | None = None,
        prefix: str | None = None,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        config: icechunk.RepositoryConfig | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
        spec_version: int = 2,
    ) -> IcechunkRepository:
        """Create a new repo.

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO]).
            bucket_config_nickname: Bucket in which the underlying Icechunk repo will be created.
            prefix: Optional prefix for Icechunk store. If not provided, a random ID + the repo name will be used.
            description: Optional description for the repo.
            metadata: Optional dictionary of metadata to tag the repo with.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            config: Optional config for the repo.
                This is the `icechunk.RepositoryConfig`, and the config will be saved alongside the repo upon creation.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.
            spec_version: The Icechunk spec version to use for the repo. Defaults to 2.

        Returns:
            icechunk.Repository object for the repo.
        """

        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)

        user = await mstore.get_user()
        author: Author = user.as_author()

        repo_model = await mstore.create_database(
            repo_name,
            bucket_config_nickname,
            kind=RepoKind.Icechunk,
            prefix=prefix,
            description=description,
            metadata=metadata,
        )

        # Raise a warning about token scoping for Azure delegated credentials
        if repo_model.bucket and repo_model.bucket.auth_config and repo_model.bucket.auth_config.method == "azure_credential_delegation":
            warnings.warn(
                "The bucket is configured to use Azure Customer Managed Role authentication. "
                "Credentials will be scoped to the container level only for this repo. "
                "Ensure that no other sensitive data is stored in the same container, as the credentials will have read access to all data in the container.",
                UserWarning,
            )

        try:
            # Throw error if the bucket is configured for anonymous access, this is only supported for imported repo
            if _use_anonymous_credentials(repo_model.bucket):
                bucket_name = f"{repo_model.bucket.nickname}" if repo_model.bucket else ""
                raise ValueError(
                    f"The bucket {bucket_name} is configured for anonymous access and cannot be written to. Use `import_repo` to import existing repositories from this bucket."
                )

            if not isinstance(config, RepositoryConfig) and config is not None:
                raise ValueError(f"config must be an icechunk.RepositoryConfig object or None: {config}.")

            icechunk_storage = await self._get_icechunk_storage_from_repo_model(
                repo_model, user_id=user.id, storage_options=storage_options
            )

            if authorize_virtual_chunk_access is not None:
                config = await self._add_virtual_chunk_containers(
                    org=org, user=user, config=config, authorize_virtual_chunk_access=authorize_virtual_chunk_access
                )

                # fetch credentials to access buckets containing virtual chunks
                prefixes_credential_mapping = await self.containers_credentials_for_buckets(
                    org, containers_to_buckets_map=dict(authorize_virtual_chunk_access)
                )
            else:
                # TODO: make icechunk accept an empty dict instead of None
                prefixes_credential_mapping = None

            create_kwargs: dict[str, object] = {
                "config": config,
                "authorize_virtual_chunk_access": prefixes_credential_mapping,
                "spec_version": spec_version,
            }

            ic_repo = IcechunkRepository.create(
                icechunk_storage,
                **create_kwargs,  # type: ignore[arg-type]
            )

            ic_repo.set_default_commit_metadata({"author_name": author.name, "author_email": author.email})

            return ic_repo

        except (IcechunkError, ValueError):
            # If the repo fails to create, we need to delete the repo model
            await mstore.delete_database(repo_name, imsure=True, imreallysure=True)
            raise

    async def import_repo(
        self,
        name: OrgAndRepoName,
        bucket_config_nickname: BucketNickname,
        prefix: str,
        *,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IcechunkRepository:
        """Create a new Arraylake Repo by importing an existing Icechunk Repository.

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO]).
            bucket_config_nickname: Bucket in which the underlying Icechunk repo exists.
            prefix: Prefix in which the Icechunk repo exists in the bucket.
            description: Optional description for the repo.
            metadata: Optional dictionary of metadata to tag the repo with.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

        Returns:
            icechunk.Repository object for the repo.
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)

        user = await mstore.get_user()
        author: Author = user.as_author()

        repo_model = await mstore.import_database(
            repo_name,
            bucket_config_nickname,
            prefix=prefix,
            kind=RepoKind.Icechunk,
            description=description,
            metadata=metadata,
        )

        # Raise a warning about token scoping for Azure delegated credentials
        if repo_model.bucket and repo_model.bucket.auth_config and repo_model.bucket.auth_config.method == "azure_credential_delegation":
            warnings.warn(
                "The bucket is configured to use Azure Customer Managed Role authentication. "
                "Credentials will be scoped to the container level only for this repo. "
                "Ensure that no other sensitive data is stored in the same container, as the credentials will have read access to all data in the container.",
                UserWarning,
            )

        try:
            icechunk_storage = await self._get_icechunk_storage_from_repo_model(
                repo_model, user_id=user.id, storage_options=storage_options
            )

            if authorize_virtual_chunk_access is not None:
                config = await self._add_virtual_chunk_containers(
                    org=org, user=user, config=None, authorize_virtual_chunk_access=authorize_virtual_chunk_access
                )

                # fetch credentials to access buckets containing virtual chunks
                prefixes_credential_mapping = await self.containers_credentials_for_buckets(
                    org, containers_to_buckets_map=dict(authorize_virtual_chunk_access)
                )

                # Warn that VCCs won't be persisted when importing
                warnings.warn(
                    "New virtual chunk containers will not be persisted to the icechunk repo config. "
                    "If you want future `client.get_repo` calls to be authorized to access the same virtual chunks, please now modify the config explicitly. "
                    "You can do this using `client.set_virtual_chunk_containers()` with the same `authorize_virtual_chunk_access`, i.e: "
                    f"`client.set_virtual_chunk_containers({name}, authorize_virtual_chunk_access={authorize_virtual_chunk_access})`. "
                    "Note that this requires write access to the location of the icechunk repository, so will not work for anonymous access buckets, for example.",
                    UserWarning,
                )
            else:
                config = None
                prefixes_credential_mapping = None

            ic_repo = IcechunkRepository.open(
                icechunk_storage,
                config=config,
                authorize_virtual_chunk_access=prefixes_credential_mapping,
            )

            ic_repo.set_default_commit_metadata({"author_name": author.name, "author_email": author.email})

            return ic_repo

        except (IcechunkError, ValueError):
            # If the repo fails to create, we need to delete the repo model
            await mstore.delete_database(repo_name, imsure=True, imreallysure=True)
            raise

    async def _get_icechunk_storage_from_repo_model(
        self,
        repo_model: RepoModel,
        user_id: UUID,
        credentials_override: icechunk.AnyCredential | None = None,
        storage_options: StorageOptions | None = None,
    ) -> icechunk.Storage:
        """Get the icechunk storage object from a repo model.

        Args:
            repo_model: The repo model object.
            credentials_override: Optional credentials to use for the storage object.
            storage_options: Optional storage options to pass to the Icechunk storage
                creation functions. Currently supports `network_stream_timeout_seconds`
                for S3, Tigris, and R2 storage.

        Returns:
            icechunk.Storage object for the repo.
        """
        from arraylake import __version__ as arraylake_version

        if not repo_model.subscription and not repo_model.bucket:
            raise ValueError("The bucket on the catalog object cannot be None for Icechunk V2 repos!")

        effective_bucket = repo_model.bucket
        effective_prefix = repo_model.prefix
        if repo_model.subscription and not repo_model.bucket:
            if repo_model.subscription.parent_repo:
                effective_bucket = repo_model.subscription.parent_repo.bucket
                effective_prefix = repo_model.subscription.parent_repo.prefix

        if effective_bucket is None:
            raise ValueError("Repo has no bucket configured")

        credential_refresh_func = self._maybe_get_credential_refresh_func_for_icechunk(
            bucket=effective_bucket, org=repo_model.org, repo_name=repo_model.name
        )
        if credential_refresh_func is None:
            # We can't pass credentials to icechunk if we have a credential refresh function
            credentials = (
                credentials_override
                if credentials_override
                else await self._maybe_get_credentials_for_icechunk(bucket=effective_bucket, org=repo_model.org, repo_name=repo_model.name)
            )
        else:
            credentials = None

        # If config is not set, set scatter_initial_credentials to True by default
        scatter_initial_credentials = arraylake_config.get("icechunk.scatter_initial_credentials", True)

        return _get_icechunk_storage_obj(
            bucket_config=effective_bucket,
            prefix=effective_prefix,
            credential_type=_get_credential_type(credentials, credential_refresh_func),
            credentials=credentials,
            credential_refresh_func=credential_refresh_func,
            scatter_initial_credentials=scatter_initial_credentials,
            arraylake_version=arraylake_version,
            user_id=user_id,
            storage_options=storage_options,
        )

    async def get_icechunk_storage(self, name: OrgAndRepoName, credentials_override=None) -> icechunk.Storage:
        """Gets the icechunk storage object for the repo.

        Args:
            repo_name: Full name of the repo (of the form [ORG]/[REPO])
            credentials_override:
                Optional credentials to use for the storage object.
                If not provided, the credentials will be fetched from
                the bucket config.

        Returns:
            icechunk.Storage object for the repo.
        """
        org, repo_name = _parse_org_and_repo(name)

        mstore = self._metastore_for_org(org)

        # fetch everything we need from the metastore concurrently
        repo_model_raw, user_raw = await async_gather_tasks(
            mstore.get_database(repo_name),
            mstore.get_user(),
        )

        if not isinstance(repo_model_raw, RepoModel):
            raise ValueError("Expected Repo object from metastore")
        if isinstance(user_raw, RepoModel):
            raise ValueError("Expected UserInfo or ApiTokenInfo from metastore")

        user_id = UUID(str(user_raw.id)) if not isinstance(user_raw.id, UUID) else user_raw.id

        return await self._get_icechunk_storage_from_repo_model(repo_model_raw, user_id, credentials_override)

    async def get_icechunk_container_credentials_from_bucket(
        self,
        org: OrgName,
        bucket_config_nickname: BucketNickname,
    ) -> ICECHUNK_ANY_CREDENTIAL:
        """Get the icechunk virtual container credentials for a given bucket.

        Args:
            org: The organization the bucket belongs to.
            bucket_config_nickname: Nickname of the bucket to get credentials for.

        Returns:
            icechunk.Credentials.S3 | icechunk.Credentials.Gcs: The icechunk virtual chunk credentials for the bucket.
        """
        return await self._get_icechunk_container_credentials_from_bucket(
            org=org,
            bucket_config_nickname=bucket_config_nickname,
            forbid_configs_unsafe_for_virtual_chunks=False,
        )

    async def _get_icechunk_container_credentials_from_bucket(
        self,
        org: OrgName,
        bucket_config_nickname: BucketNickname,
        forbid_configs_unsafe_for_virtual_chunks: bool,
    ) -> ICECHUNK_ANY_CREDENTIAL:
        """
        A private version of ``get_icechunk_container_credentials_from_bucket``, which also includes an additional argument to forbid all bucket configs deemed unsafe for use with virtual chunks.
        """
        bucket = await self.get_bucket_config(org=org, nickname=bucket_config_nickname)

        if forbid_configs_unsafe_for_virtual_chunks:
            forbid_unsafe_virtual_bucket_configs(bucket=bucket, bucket_nickname=bucket_config_nickname)

        credential_refresh_func = self._maybe_get_credential_refresh_func_for_icechunk(bucket=bucket, org=org, repo_name=None)
        if credential_refresh_func is None:
            credentials = await self._maybe_get_credentials_for_icechunk(bucket=bucket, org=org, repo_name=None)
        else:
            credentials = None

        # Azure credentials are not supported for virtual chunks yet
        if isinstance(credentials, AzureCredentials):
            credentials = None

        return get_icechunk_container_credentials(
            bucket_platform=bucket.platform, credentials=credentials, credential_refresh_func=credential_refresh_func
        )

    async def containers_credentials_for_buckets(
        self,
        org: OrgName,
        containers_to_buckets_map: dict[BucketPrefix, BucketNickname] = {},
        **kwargs: str,
    ) -> dict[BucketPrefix, icechunk.AnyCredential | None]:
        """Builds a map of credentials for icechunk virtual chunk containers
        from the provided bucket nicknames and calls icechunk.containers_credentials
        on this mapping.

        Args:
            org: The organization the buckets belong to.
            containers_to_buckets_map:
                A dictionary mapping virtual chunk container names to bucket nicknames.

        Returns:
            A dictionary mapping container names to icechunk virtual chunk credentials.
        """
        return await self._containers_credentials_for_buckets(
            org=org,
            containers_to_buckets_map=containers_to_buckets_map,
            forbid_configs_unsafe_for_virtual_chunks=False,
            **kwargs,
        )

    async def _containers_credentials_for_buckets(
        self,
        org: OrgName,
        containers_to_buckets_map: Mapping[BucketPrefix, BucketNickname] = {},
        forbid_configs_unsafe_for_virtual_chunks=False,
        **kwargs: str,
    ) -> dict[BucketPrefix, icechunk.AnyCredential | None]:
        """
        A private version of ``container_credentials_for_buckets``, which also includes an additional argument to forbid all bucket setups deemed unsafe for use with virtual chunks.
        """

        # We always run this check because there is no legitimate reason to use a `file:///` url prefix with Arraylake
        forbid_unsafe_virtual_chunk_containers(list(containers_to_buckets_map.keys()))

        containers_to_nicknames_map = {**containers_to_buckets_map, **kwargs}

        for container_name, bucket_nickname in containers_to_nicknames_map.items():
            if not isinstance(bucket_nickname, str):
                raise ValueError(f"Invalid bucket nickname {bucket_nickname} for container {container_name}.")

        # concurrently fetch all the credentials needed
        credentials = await async_gather_tasks(
            *[
                self._get_icechunk_container_credentials_from_bucket(
                    org=org,
                    bucket_config_nickname=bucket_nickname,
                    forbid_configs_unsafe_for_virtual_chunks=forbid_configs_unsafe_for_virtual_chunks,
                )
                for bucket_nickname in containers_to_nicknames_map.values()
            ]
        )

        credentials_map: Mapping[str, ICECHUNK_ANY_CREDENTIAL] = {
            container_name: creds for container_name, creds in zip(containers_to_nicknames_map.keys(), credentials)
        }

        return icechunk.containers_credentials(credentials_map)  # type: ignore[arg-type]

    async def authorize_virtual_chunk_access(
        self,
        name: OrgAndRepoName,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname],
    ) -> None:
        """
        Set virtual chunk containers on the underlying Icechunk repo.

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO])
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls. Used for Icechunk repos only.
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)
        await mstore.patch_virtual_chunk_containers(repo_name, add=dict(authorize_virtual_chunk_access))

    async def _add_virtual_chunk_containers(
        self,
        org: OrgName,
        user,
        config: icechunk.RepositoryConfig | None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname],
    ) -> icechunk.RepositoryConfig:
        """Add virtual chunk containers to an `icechunk.RepositoryConfig` instance."""

        if config is None:
            # this should only change config fields that are explicitly set
            config = RepositoryConfig()

        # we list the unsafe ones too here instead of only the pre-authorized ones as `create_virtual_chunk_containers` will forbid the unsafe ones with a clear error message anyway
        bucket_configs = await self.list_bucket_configs(org=org)

        for prefix, nickname in authorize_virtual_chunk_access.items():
            matching_bucket_configs = [bucket for bucket in bucket_configs if bucket.nickname == nickname]

            if not matching_bucket_configs:
                raise ValueError(f"No existing bucket config found in org {org} with nickname {nickname}")

            container = create_virtual_chunk_container(
                bucket_config=matching_bucket_configs[0],
                prefix=prefix,
                user_id=user.id,
            )

            config.set_virtual_chunk_container(container)

        return config

    async def get_virtual_chunk_containers(self, name: OrgAndRepoName) -> Mapping[BucketPrefix, BucketNickname | None]:
        """
        Get virtual chunk containers for this repo and the buckets containing the data they refer to.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO]).

        Returns:
            A mapping from virtual chunk container prefixes to bucket config nicknames.
            Nicknames may be None if the VCC could not be resolved to a bucket config.
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)
        return await mstore.get_virtual_chunk_containers(repo_name)

    async def modify_repo(
        self,
        name: OrgAndRepoName,
        description: str | None = None,
        add_metadata: RepoMetadataT | None = None,
        remove_metadata: list[str] | None = None,
        update_metadata: RepoMetadataT | None = None,
        optimization_config: OptimizationConfig | None = None,
    ) -> None:
        """Modify a repo's metadata, description, or optimization config.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            description: Optional description for the repo.
            add_metadata: Optional dictionary of metadata to add to the repo.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
                Cannot use if the key already exists in the metadata.
            remove_metadata: List of metadata keys to remove from the repo.
            update_metadata: Optional dictionary of metadata to update on the repo.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            optimization_config: Optional optimization configuration for the repo.
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)
        await mstore.modify_database(
            repo_name,
            description=description,
            add_metadata=add_metadata,
            remove_metadata=remove_metadata,
            update_metadata=update_metadata,
            optimization_config=optimization_config,
        )

    async def delete_repo(self, name: OrgAndRepoName, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form [ORG]/[REPO])
            imsure, imreallysure: confirm you intend to delete this bucket config
        """
        org, repo_name = _parse_org_and_repo(name)
        mstore = self._metastore_for_org(org)
        await mstore.delete_database(repo_name, imsure=imsure, imreallysure=imreallysure)

    async def _set_repo_status(
        self, qualified_repo_name: OrgAndRepoName, mode: RepoOperationMode, message: str | None = None
    ) -> RepoOperationStatusResponse:
        """Sets the repo status to the given mode.

        Args:
            qualified_repo_name: Full name of the repo (of the form [ORG]/[REPO])
            mode: The mode to set the repo to.
            message: Optional message to associate with the mode change.

        Returns:
            RepoOperationStatusResponse object containing mode change outputs.
        """
        org, repo_name = _parse_org_and_repo(qualified_repo_name)
        mstore = self._metastore_for_org(org)
        return await mstore.set_repo_status(repo_name, mode, message)

    async def _bucket_id_for_nickname(self, mstore: HttpMetastore, nickname: BucketNickname) -> UUID:
        buckets = await mstore.list_bucket_configs()
        bucket_id = next((b.id for b in buckets if b.nickname == nickname), None)
        if not bucket_id:
            raise BucketNotFoundError(nickname)
        return bucket_id

    def _make_bucket_config(
        self,
        *,
        nickname: BucketNickname,
        uri: str,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        use_ssl: bool | None = None,
        force_path_style: bool | None = None,
        extra_config: dict | None = None,
        auth_config: dict | None = None,
    ) -> dict:
        if not nickname:
            raise ValueError("nickname must be specified if uri is provided.")

        # Build extra_config from explicit parameters, with extra_config dict as fallback
        # for backwards compatibility. Explicit parameters take precedence.
        merged_extra_config: dict[str, str | bool] = {}
        if extra_config is not None:
            warnings.warn(
                "Passing 'extra_config' as a dict is deprecated. "
                "Use the explicit keyword arguments instead: region_name, endpoint_url, use_ssl, force_path_style.",
                DeprecationWarning,
                stacklevel=3,
            )
            merged_extra_config.update(extra_config)
        if region_name is not None:
            merged_extra_config["region_name"] = region_name
        if endpoint_url is not None:
            merged_extra_config["endpoint_url"] = endpoint_url
        if use_ssl is not None:
            merged_extra_config["use_ssl"] = use_ssl
        if force_path_style is not None:
            merged_extra_config["force_path_style"] = force_path_style

        # unpack optionals
        if auth_config is None:
            auth_config = {"method": "anonymous"}

        # parse uri and get prefix
        res = urlparse(uri)
        platform: Literal["s3", "gs", "s3-compatible", "azure"] | None = (
            "s3" if res.scheme == "s3" else "gs" if res.scheme == "gs" else "azure" if res.scheme == "az" else None
        )
        if platform == "s3" and merged_extra_config.get("endpoint_url"):
            platform = "s3-compatible"
        if platform not in ["s3", "gs", "s3-compatible", "azure"]:
            raise ValueError(f"Invalid platform {platform} for uri {uri}")
        name = res.netloc
        prefix = res.path[1:] if res.path.startswith("/") else res.path  # is an empty string if not specified

        valid_methods = [
            "customer_managed_role",
            "aws_customer_managed_role",
            "gcp_customer_managed_role",
            "r2_customer_managed_role",
            "azure_credential_delegation",
            "anonymous",
            "hmac",
        ]
        if "method" not in auth_config or auth_config["method"] not in valid_methods:
            raise ValueError(f"invalid auth_config, must provide method key {valid_methods}")

        if prefix != "" and auth_config["method"] == "hmac":
            warnings.warn(
                "HMAC bucket permissions cannot be downscoped to a specific prefix. "
                f"You are creating a BucketConfig for a bucket with HMAC authentication, but also specifying the object store prefix {prefix}. "
                "Arraylake cannot guarantee that the credentials are scoped only to the requested prefix due to how HMAC credentials work. "
                f"The scope of HMAC credentials is set once, when created, and there is no way for Arraylake to verify that the credentials that exist for your bucket are restricted only to the prefix {prefix}. "
                "Consider using delegated credentials instead. Please see https://docs.earthmover.io/setup/manage-storage#configuring-hmac for more details.",
                UserWarning,
            )

        return dict(
            platform=platform,
            name=name,
            prefix=prefix,
            nickname=nickname,
            extra_config=merged_extra_config,
            auth_config=auth_config,
        )

    async def create_bucket_config(
        self,
        *,
        org: OrgName,
        nickname: BucketNickname,
        uri: URI,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        use_ssl: bool | None = None,
        force_path_style: bool | None = None,
        extra_config: dict | None = None,
        auth_config: dict | None = None,
    ) -> BucketResponse:
        """Create a new bucket config entry.

        NOTE: This does not create any actual buckets in the object store.

        Args:
            org: Name of the org.
            nickname: Bucket nickname (e.g. ``"my-s3-bucket"``).
            uri: The URI of the object store, of the form
                ``platform://bucket_name[/prefix]`` (e.g. ``"s3://my-bucket/prefix"``).
            region_name: Cloud region for the bucket (e.g. ``"us-west-2"``).
                Required for S3 buckets.
            endpoint_url: Custom endpoint URL for S3-compatible storage
                (e.g. ``"https://account-id.r2.cloudflarestorage.com"``).
                Setting this automatically marks the bucket as S3-compatible.
            use_ssl: Whether to use HTTPS for storage connections.
                Defaults to ``True``. Set to ``False`` for local or insecure endpoints.
                Only applies to S3-type buckets.
            force_path_style: Use path-style URLs (``endpoint/bucket``) instead of
                virtual-hosted style (``bucket.endpoint``). Defaults to ``False`` when
                ``use_ssl=True``, ``True`` when ``use_ssl=False``. Often required for
                S3-compatible storage. Only applies to S3-type buckets.
            extra_config: Dictionary of additional config options. Prefer using the
                explicit parameters above when possible. Keys set here are overridden
                by any explicit parameters that are also provided.
            auth_config: Dictionary of auth parameters. Must include a ``"method"`` key.
                Defaults to ``{"method": "anonymous"}``.
        """
        validated = NewBucket(
            **self._make_bucket_config(
                nickname=nickname,
                uri=uri,
                region_name=region_name,
                endpoint_url=endpoint_url,
                use_ssl=use_ssl,
                force_path_style=force_path_style,
                extra_config=extra_config,
                auth_config=auth_config,
            )
        )
        mstore = self._metastore_for_org(org)
        bucket = await mstore.create_bucket_config(validated)
        return bucket

    async def set_default_bucket_config(self, *, org: OrgName, nickname: BucketNickname) -> None:
        """Set the organization's default bucket for any new repos

        Args:
            nickname: Nickname of the bucket config to set as default.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        await mstore.set_default_bucket_config(bucket_id)

    async def get_bucket_config(self, *, org: OrgName, nickname: BucketNickname) -> BucketResponse:
        """Get a bucket's configuration

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to retrieve.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        bucket = await mstore.get_bucket_config(bucket_id)
        return bucket

    async def get_obstore_for_bucket(
        self, *, org: OrgName, nickname: BucketNickname, access: Literal["read", "write"] = "read"
    ) -> obs.store.ObjectStore:
        """Get an obstore ObjectStore for the named bucket.

        Resolves the bucket nickname, fetches scoped credentials, and returns an
        ``obstore.store.S3Store``, ``GCSStore``, or ``AzureStore`` ready for use.

        Defaults to read-only credentials. Pass ``access="write"`` to request a
        read+write store; that variant requires ``CAN_MANAGE_USERS`` on the org.

        Requires the optional ``obstore`` extra (``pip install arraylake[obstore]``).

        Args:
            org: Name of the org that owns the bucket.
            nickname: Nickname of the bucket config.
            access: ``"read"`` (default) or ``"write"``.

        Returns:
            An obstore ObjectStore scoped to the bucket and its configured prefix.

        Raises:
            ImportError: If the optional ``obstore`` extra is not installed.
        """
        # Fail fast before making any API calls if obstore isn't available.
        try:
            import obstore  # noqa: F401
        except ImportError as e:
            raise ImportError(
                "The 'obstore' package is required for this functionality but is not installed. "
                "Install it with: pip install 'arraylake[obstore]'"
            ) from e
        bucket = await self.get_bucket_config(org=org, nickname=nickname)
        creds = await self._maybe_get_credentials_for_icechunk(bucket, org, repo_name=None, bucket_access=access)
        return bucket.as_obstore_store(creds)

    async def list_bucket_configs(self, org: OrgName) -> list[BucketResponse]:
        """List all bucket config entries

        Args:
            org: Name of the organization.
        """
        mstore = self._metastore_for_org(org)
        return await mstore.list_bucket_configs()

    async def list_repos_for_bucket_config(self, *, org: OrgName, nickname: BucketNickname) -> RepoList:
        """List repos using a given bucket.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket configuration.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        repos = await mstore.list_repos_for_bucket_config(bucket_id)
        return RepoList(repos, org=org)

    async def delete_bucket_config(
        self, *, org: OrgName, nickname: BucketNickname, imsure: bool = False, imreallysure: bool = False
    ) -> None:
        """Delete a bucket config entry

        NOTE: If a bucket config is in use by one or more repos, it cannot be
        deleted. This does not actually delete any buckets in the object store.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to delete.
            imsure, imreallysure: confirm you intend to delete this bucket config
        """
        if not (imsure and imreallysure):
            raise ValueError("imsure and imreallysure must be set to True")
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, nickname)
        await mstore.delete_bucket_config(bucket_id)

    async def set_virtual_chunk_access_policy(
        self,
        org: OrgName,
        *,
        bucket_nickname: BucketNickname,
        subprefix: str = "",
        public: bool = False,
    ) -> ExplicitVirtualChunkAccessPolicyResponse:
        """Set an explicit virtual chunk access policy on this org.

        Args:
            org: Name of the organization.
            bucket_nickname: Nickname of the bucket config to associate with this VCAP.
            subprefix: Subprefix within the bucket for this VCAP.
            public: Whether this VCAP allows public access.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, bucket_nickname)
        vcap = await mstore.set_virtual_chunk_access_policy(
            bucket_id=str(bucket_id),
            subprefix=subprefix.strip("/"),
            public=public,
        )
        return ExplicitVirtualChunkAccessPolicyResponse.model_validate(vcap.model_dump())

    async def list_virtual_chunk_access_policies(self, org: OrgName) -> list[ExplicitVirtualChunkAccessPolicyResponse]:
        """List explicit virtual chunk access policies on this org.

        Args:
            org: Name of the organization.
        """
        mstore = self._metastore_for_org(org)
        vcaps = await mstore.list_virtual_chunk_access_policies()
        return [ExplicitVirtualChunkAccessPolicyResponse.model_validate(v.model_dump()) for v in vcaps if v.use_case == "explicit"]

    async def delete_virtual_chunk_access_policy(
        self,
        org: OrgName,
        *,
        bucket_nickname: BucketNickname,
        subprefix: str,
        public: bool,
    ) -> None:
        """Delete a virtual chunk access policy from this org (idempotent).

        Args:
            org: Name of the organization.
            bucket_nickname: Nickname of the bucket config for the VCAP.
            subprefix: Subprefix of the VCAP to delete.
            public: Whether this VCAP allows public access.
        """
        mstore = self._metastore_for_org(org)
        bucket_id = await self._bucket_id_for_nickname(mstore, bucket_nickname)
        await mstore.delete_virtual_chunk_access_policy(
            bucket_id=str(bucket_id),
            subprefix=subprefix.strip("/"),
            public=public,
        )

    async def login(self, *, browser: bool = False) -> None:
        """Login to ArrayLake.

        Args:
            browser: if True, open the browser to the login page
        """
        handler = get_auth_handler(api_endpoint=self.service_uri)
        await handler.login(browser=browser)

    async def logout(self) -> None:
        """Log out of ArrayLake."""
        handler = get_auth_handler(api_endpoint=self.service_uri)
        await handler.logout()

    async def get_api_client_from_token(self, org: OrgName, token: str) -> ApiClientResponse:
        """Fetch the user corresponding to the provided token"""
        mstore = self._metastore_for_org(org)
        api_client = await mstore.get_api_client_from_token(token)
        return api_client

    async def get_permission_check(self, org: OrgName, principal_id: str, resource: str, action: OrgActions | RepoActions) -> bool:
        """Verify whether the provided principal has permission to perform the
        action against the resource"""
        mstore = self._metastore_for_org(org)
        is_approved = await mstore.get_permission_check(principal_id, resource, action)
        return is_approved

    def get_services(self, org: OrgName) -> AsyncComputeClient:
        """Get the compute client services for the given org.

        Args:
            org: Name of the org
        """
        return AsyncComputeClient(service_uri=self.service_uri, token=self.token, org=org)


class Client:
    """Client for interacting with ArrayLake.

    Args:
        service_uri (str):
            [Optional] The service URI to target.
        token (str):
            [Optional] API token for service account authentication.
        cache_credentials (bool):
            [Optional] When True (default), delegated bucket credentials are
            served from a process-wide cache. Set to False for server-side
            contexts that should not retain credentials in memory.
    """

    aclient: AsyncClient

    def __init__(self, service_uri: str | None = None, token: str | None = None, cache_credentials: bool = True) -> None:
        self.aclient = AsyncClient(service_uri=service_uri, token=token, cache_credentials=cache_credentials)

    @property
    def service_uri(self) -> str:
        """The service URI to target."""
        return self.aclient.service_uri

    @property
    def token(self) -> str | None:
        """API token for service account authentication."""
        return self.aclient.token

    def __repr__(self):
        return f"arraylake.Client(service_uri='{self.service_uri}')"

    def list_repos(self, org: OrgName, filter_metadata: RepoMetadataT | None = None) -> RepoList:
        """List all repositories for the specified org

        Args:
            org: Name of the org
            filter_metadata: Optional metadata to filter the repos by.
                If provided, only repos with the specified metadata will be returned.
                Filtering is inclusive and will return repos that match all of the provided metadata.
        """
        return sync(self.aclient.list_repos, org=org, filter_metadata=filter_metadata)

    def list_repos_paginated(
        self,
        org: OrgName,
        filter_metadata: RepoMetadataT | None = None,
        page_size: int = 50,
    ) -> Generator[RepoModel, None, None]:
        """List repositories for the specified org, yielding results page by page.

        This is a generator that lazily fetches pages from the server.

        Args:
            org: Name of the org
            filter_metadata: Optional metadata to filter the repos by.
            page_size: Number of repos per page.

        Yields:
            Repo objects one at a time, fetching pages as needed.
        """
        # Can't use sync(self.aclient.list_repos_paginated, ...) here because
        # sync() runs a single coroutine to completion, and async generators
        # aren't coroutines. Instead we sync() each page fetch individually.
        mstore = self.aclient._metastore_for_org(org)
        page = 1
        while True:
            result = sync(
                mstore.list_databases_page,
                filter_metadata=filter_metadata,
                page=page,
                size=page_size,
            )
            yield from result.items
            if result.page >= result.pages:
                break
            page += 1

    def get_repo_object(self, name: OrgAndRepoName) -> RepoModel:
        """Get the repo configuration object.
        See `get_repo` for an instantiated repo.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
        """
        return sync(self.aclient.get_repo_object, name=name)

    def get_repo(
        self,
        name: OrgAndRepoName,
        *,
        config: icechunk.RepositoryConfig | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IcechunkRepository:
        """Get a repo by name

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            config: Optional config for the repo. For Icechunk repos, this is the RepositoryConfig.
                Config settings passed here will take precedence over
                the stored repo config when opening the repo.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
                If not supplied this method will attempt to auto-discover them,
                by inspecting the icechunk repository config for any virtual chunk containers,
                and attempting to authorize all of them.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

        Returns:
            icechunk.Repository: The retrieved Icechunk repository.
        """
        return sync(
            self.aclient.get_repo,
            name,
            config=config,
            authorize_virtual_chunk_access=authorize_virtual_chunk_access,
            storage_options=storage_options,
        )

    def get_or_create_repo(
        self,
        name: OrgAndRepoName,
        *,
        bucket_config_nickname: BucketNickname | None = None,
        prefix: str | None = None,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        config: icechunk.RepositoryConfig | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IcechunkRepository:
        """Get a repo by name. Create the repo if it doesn't already exist.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            bucket_config_nickname: The created repo will use this bucket for its chunks.
                If the repo exists, bucket_config_nickname is ignored.
            prefix: Optional prefix for Icechunk store. If not provided, a random ID + the repo name will be used.
            description: Optional description for the repo.
            metadata: Optional dictionary of metadata to tag the repo with.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            config: Optional config for the repo.
                For Icechunk repos, this is the RepositoryConfig.
                Config settings passed here will take precedence over
                the stored repo config when opening the repo. When creating
                a new repo, the config will be saved alongside the repo.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
                If not supplied this method will attempt to auto-discover them,
                by inspecting the icechunk repository config for any virtual chunk containers,
                and attempting to authorize all of them.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

        Returns:
            icechunk.Repository: The created or retrieved Icechunk repository.
        """
        return sync(
            self.aclient.get_or_create_repo,
            name,
            bucket_config_nickname=bucket_config_nickname,
            prefix=prefix,
            description=description,
            metadata=metadata,
            config=config,
            authorize_virtual_chunk_access=authorize_virtual_chunk_access,
            storage_options=storage_options,
        )

    def create_repo(
        self,
        name: OrgAndRepoName,
        *,
        bucket_config_nickname: BucketNickname | None = None,
        prefix: str | None = None,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        config: icechunk.RepositoryConfig | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
        spec_version: int = 2,
    ) -> IcechunkRepository:
        """Create a new repo

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO])
            bucket_config_nickname: An optional bucket to use for the chunkstore
            prefix: Optional prefix for Icechunk store. If not provided, a random ID + the repo name will be used.
            description: Optional description for the repo.
            metadata: Optional dictionary of metadata to tag the repo with.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            config: Optional config for the repo.
                For Icechunk repos, this is the RepositoryConfig, and
                the config will be saved alongside the repo upon creation.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Used for Icechunk repos only.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.
            spec_version: The Icechunk spec version to use for the repo. Defaults to 2.

        Returns:
            icechunk.Repository: The created Icechunk repository.
        """
        return sync(
            self.aclient.create_repo,
            name,
            bucket_config_nickname=bucket_config_nickname,
            prefix=prefix,
            description=description,
            metadata=metadata,
            config=config,
            authorize_virtual_chunk_access=authorize_virtual_chunk_access,
            storage_options=storage_options,
            spec_version=spec_version,
        )

    def import_repo(
        self,
        name: OrgAndRepoName,
        bucket_config_nickname: BucketNickname,
        prefix: str,
        *,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
        storage_options: StorageOptions | None = None,
    ) -> IcechunkRepository:
        """Create a new Arraylake Repo by importing an existing Icechunk Repository.

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO]).
            bucket_config_nickname: Bucket in which the underlying Icechunk repo exists.
            prefix: Prefix in which the Icechunk repo exists in the bucket.
            description: Optional description for the repo.
            metadata: Optional dictionary of metadata to tag the repo with.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls.
            storage_options: Optional storage options for the underlying Icechunk storage.
                Currently supports `network_stream_timeout_seconds` for S3, Tigris, and R2 storage.

        Returns:
            icechunk.Repository object for the repo.
        """
        return sync(
            self.aclient.import_repo,
            name,
            bucket_config_nickname,
            prefix,
            description=description,
            metadata=metadata,
            authorize_virtual_chunk_access=authorize_virtual_chunk_access,
            storage_options=storage_options,
        )

    def get_icechunk_storage(self, name: OrgAndRepoName, *, credentials_override: icechunk.AnyCredential | None = None) -> icechunk.Storage:
        """Gets the icechunk storage object for the repo.

        Example usage:

            ```python
            from arraylake import Client
            client = Client()
            storage = client.get_icechunk_storage("my-org/my-repo")
            icechunk.Repository.exists(storage)
            icechunk.Repository.fetch_config(storage)
            repo = icechunk.Repository.open(storage)
            ```

        Args:
            repo_name: Full name of the repo (of the form [ORG]/[REPO])
            credentials_override: Optional credentials to use for the storage object.
                If not provided, the credentials will be fetched from
                the bucket config.

        Returns:
            icechunk.Storage object for the repo.
        """
        return sync(self.aclient.get_icechunk_storage, name, credentials_override=credentials_override)

    def get_icechunk_container_credentials_from_bucket(
        self, org: OrgName, bucket_config_nickname: BucketNickname
    ) -> icechunk.Credentials.S3 | icechunk.Credentials.Gcs:
        """Get the icechunk virtual chunk credentials for a given bucket.

        Args:
            org: The organization the bucket belongs to.
            bucket_config_nickname: Nickname of the bucket to get credentials for.

        Returns:
            icechunk.Credentials.S3 | icechunk.Credentials.Gcs: The icechunk virtual chunk credentials for the bucket.
        """
        return sync(self.aclient.get_icechunk_container_credentials_from_bucket, org, bucket_config_nickname)

    def containers_credentials_for_buckets(
        self, org: OrgName, containers_to_buckets_map: dict[BucketPrefix, BucketNickname] = {}, **kwargs: str
    ) -> dict[BucketPrefix, icechunk.AnyCredential]:
        """Builds a map of credentials for icechunk virtual chunk containers
        from the provided bucket nicknames and calls icechunk.containers_credentials
        on this mapping.

        Example usage:
        ```python
        import icechunk as ic
        from arraylake import Client

        client = Client()
        storage = client.get_icechunk_storage("my-org/my-repo")
        config = ic.Repository.fetch_config(storage)
        container_names = [container.name for container in config.virtual_chunk_containers()]
        container_creds = client.containers_credentials_for_buckets("my-org", conatiner_name="my-bucket")
        repo = ic.Repository.open(storage, config=config, virtual_chunk_credentials=container_creds)
        ```

        Args:
            org: The organization the bucket belongs to.
            containers_to_buckets_map:
                A dictionary mapping virtual chunk container names to bucket nicknames.

        Returns:
            A dictionary mapping container names to icechunk virtual chunk credentials.
        """
        return sync(
            self.aclient.containers_credentials_for_buckets,
            org=org,
            containers_to_buckets_map=containers_to_buckets_map,
            **kwargs,  # type: ignore
        )

    def authorize_virtual_chunk_access(
        self,
        name: OrgAndRepoName,
        authorize_virtual_chunk_access: Mapping[BucketPrefix, BucketNickname] | None = None,
    ) -> None:
        """
        Set virtual chunk containers on the underlying Icechunk repo.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO]).
            authorize_virtual_chunk_access: A mapping from virtual chunk container prefixes to bucket nicknames.
                Credentials will be fetched for these buckets based on the auth configuration
                and used for the containers. Must be supplied as complete urls. Used for Icechunk repos only.
        """
        return sync(
            self.aclient.authorize_virtual_chunk_access,
            name=name,
            authorize_virtual_chunk_access=authorize_virtual_chunk_access,
        )

    def get_virtual_chunk_containers(
        self,
        name: OrgAndRepoName,
    ) -> Mapping[BucketPrefix, BucketNickname | None]:
        """
        Get virtual chunk containers for this repo and the buckets containing the data they refer to.

        Args:
            name: Full name of the repo to create (of the form [ORG]/[REPO]).

        Returns:
            A mapping from virtual chunk container prefixes to bucket config nicknames.
            Nicknames may be None if the VCC could not be resolved to a bucket config.
        """
        return sync(
            self.aclient.get_virtual_chunk_containers,
            name=name,
        )

    def modify_repo(
        self,
        name: OrgAndRepoName,
        description: str | None = None,
        add_metadata: RepoMetadataT | None = None,
        remove_metadata: list[str] | None = None,
        update_metadata: RepoMetadataT | None = None,
        optimization_config: OptimizationConfig | None = None,
    ) -> None:
        """Modify a repo's metadata, description, or optimization config.

        Args:
            name: Full name of the repo (of the form [ORG]/[REPO])
            description: Optional description for the repo.
            add_metadata: Optional dictionary of metadata to add to the repo.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
                Cannot use if the key already exists in the metadata.
            remove_metadata: List of metadata keys to remove from the repo.
            update_metadata: Optional dictionary of metadata to update on the repo.
                Dictionary values can be a scalar (string, int, float, bool, or None) or a list of scalars.
            optimization_config: Optional optimization configurations for the repo.
        """
        return sync(
            self.aclient.modify_repo,
            name,
            description=description,
            add_metadata=add_metadata,
            remove_metadata=remove_metadata,
            update_metadata=update_metadata,
            optimization_config=optimization_config,
        )

    def delete_repo(self, name: OrgAndRepoName, *, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a repo

        Args:
            name: Full name of the repo to delete (of the form [ORG]/[REPO])
        """

        return sync(self.aclient.delete_repo, name, imsure=imsure, imreallysure=imreallysure)

    def create_bucket_config(
        self,
        *,
        org: OrgName,
        nickname: BucketNickname,
        uri: URI,
        region_name: str | None = None,
        endpoint_url: str | None = None,
        use_ssl: bool | None = None,
        force_path_style: bool | None = None,
        extra_config: dict | None = None,
        auth_config: dict | None = None,
    ) -> BucketResponse:
        """Create a new bucket config entry.

        NOTE: This does not create any actual buckets in the object store.

        Args:
            org: Name of the org.
            nickname: Bucket nickname (e.g. ``"my-s3-bucket"``).
            uri: The URI of the object store, of the form
                ``platform://bucket_name[/prefix]`` (e.g. ``"s3://my-bucket/prefix"``).
            region_name: Cloud region for the bucket (e.g. ``"us-west-2"``).
                Required for S3 buckets.
            endpoint_url: Custom endpoint URL for S3-compatible storage
                (e.g. ``"https://account-id.r2.cloudflarestorage.com"``).
                Setting this automatically marks the bucket as S3-compatible.
            use_ssl: Whether to use HTTPS for storage connections.
                Defaults to ``True``. Set to ``False`` for local or insecure endpoints.
                Only applies to S3-type buckets.
            force_path_style: Use path-style URLs (``endpoint/bucket``) instead of
                virtual-hosted style (``bucket.endpoint``). Defaults to ``False`` when
                ``use_ssl=True``, ``True`` when ``use_ssl=False``. Often required for
                S3-compatible storage. Only applies to S3-type buckets.
            extra_config: Dictionary of additional config options. Prefer using the
                explicit parameters above when possible. Keys set here are overridden
                by any explicit parameters that are also provided.
            auth_config: Dictionary of auth parameters. Must include a ``"method"`` key.
                Defaults to ``{"method": "anonymous"}``.
        """
        return sync(
            self.aclient.create_bucket_config,
            org=org,
            nickname=nickname,
            uri=uri,
            region_name=region_name,
            endpoint_url=endpoint_url,
            use_ssl=use_ssl,
            force_path_style=force_path_style,
            extra_config=extra_config,
            auth_config=auth_config,
        )

    def set_default_bucket_config(self, *, org: OrgName, nickname: BucketNickname) -> None:
        """Set the organization's default bucket config for any new repos

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to set as default.
        """
        return sync(self.aclient.set_default_bucket_config, org=org, nickname=nickname)

    def get_bucket_config(self, *, org: OrgName, nickname: BucketNickname) -> BucketResponse:
        """Get a bucket's configuration

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to retrieve.
        """
        return sync(self.aclient.get_bucket_config, org=org, nickname=nickname)

    def get_obstore_for_bucket(
        self, *, org: OrgName, nickname: BucketNickname, access: Literal["read", "write"] = "read"
    ) -> obs.store.ObjectStore:
        """Get an obstore ObjectStore for the named bucket.

        Defaults to read-only credentials. Pass ``access="write"`` to request a
        read+write store; that variant requires ``CAN_MANAGE_USERS`` on the org.

        Requires the optional ``obstore`` extra (``pip install arraylake[obstore]``).

        Args:
            org: Name of the org that owns the bucket.
            nickname: Nickname of the bucket config.
            access: ``"read"`` (default) or ``"write"``.

        Returns:
            An obstore ObjectStore scoped to the bucket and its configured prefix.
        """
        return sync(self.aclient.get_obstore_for_bucket, org=org, nickname=nickname, access=access)

    def list_bucket_configs(self, org: OrgName) -> list[BucketResponse]:
        """List all buckets for the specified org

        Args:
            org: Name of the org
        """
        return sync(self.aclient.list_bucket_configs, org)

    def list_repos_for_bucket_config(self, *, org: OrgName, nickname: BucketNickname) -> RepoList:
        """List repos using a given bucket config

        Args:
            org: Name of the org
            nickname: Nickname of the bucket.
        """
        return sync(self.aclient.list_repos_for_bucket_config, org=org, nickname=nickname)

    def delete_bucket_config(self, *, org: OrgName, nickname: BucketNickname, imsure: bool = False, imreallysure: bool = False) -> None:
        """Delete a bucket config entry

        NOTE: If a bucket config is in use by one or more repos, it cannot be
        deleted. This does not actually delete any buckets in the object store.

        Args:
            org: Name of the org
            nickname: Nickname of the bucket config to delete.
            imsure, imreallysure: confirm you intend to delete this bucket config
        """
        return sync(self.aclient.delete_bucket_config, org=org, nickname=nickname, imsure=imsure, imreallysure=imreallysure)

    def set_virtual_chunk_access_policy(
        self,
        org: OrgName,
        *,
        bucket_nickname: BucketNickname,
        subprefix: str,
        public: bool,
    ) -> ExplicitVirtualChunkAccessPolicyResponse:
        """Set an explicit virtual chunk access policy on this org.

        Args:
            org: Name of the organization.
            bucket_nickname: Nickname of the bucket config to associate with this VCAP.
            subprefix: Subprefix within the bucket for this VCAP.
            public: Whether this VCAP allows public access.
        """
        return sync(self.aclient.set_virtual_chunk_access_policy, org, bucket_nickname=bucket_nickname, subprefix=subprefix, public=public)

    def list_virtual_chunk_access_policies(self, org: OrgName) -> list[ExplicitVirtualChunkAccessPolicyResponse]:
        """List explicit virtual chunk access policies on this org.

        Args:
            org: Name of the organization.
        """
        return sync(self.aclient.list_virtual_chunk_access_policies, org)

    def delete_virtual_chunk_access_policy(
        self,
        org: OrgName,
        *,
        bucket_nickname: BucketNickname,
        subprefix: str,
        public: bool,
    ) -> None:
        """Delete a virtual chunk access policy from this org.

        Args:
            org: Name of the organization.
            bucket_nickname: Nickname of the bucket config for the VCAP.
            subprefix: Subprefix of the VCAP to delete.
            public: Whether this VCAP allows public access.
        """
        return sync(
            self.aclient.delete_virtual_chunk_access_policy, org, bucket_nickname=bucket_nickname, subprefix=subprefix, public=public
        )

    def login(self, *, browser: bool = False) -> None:
        """Login to ArrayLake.

        Args:
            browser: if True, open the browser to the login page
        """
        return sync(self.aclient.login, browser=browser)

    def logout(self) -> None:
        """Log out of ArrayLake."""
        return sync(self.aclient.logout)

    def get_services(self, org: OrgName) -> ComputeClient:
        """Get the compute client services for the given org.

        Args:
            org: Name of the org
        """
        return self.aclient.get_services(org).to_sync_client()
