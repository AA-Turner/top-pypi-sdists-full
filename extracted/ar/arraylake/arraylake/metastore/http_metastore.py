from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Any, Literal
from urllib.parse import quote
from uuid import UUID

from pydantic import TypeAdapter

from arraylake.api_utils import ArraylakeHttpClient, handle_response
from arraylake.metastore.abc import Metastore
from arraylake.types import (
    ApiClientResponse,
    AzureCredentials,
    BucketModifyRequest,
    BucketResponse,
    GSCredentials,
    IcebergNamespaceResponse,
    IcebergNamespaceSort,
    IcebergTableSort,
    IcebergTableSummaryResponse,
    NewBucket,
    NewRepoOperationStatus,
    OpenRepoResponse,
    OptimizationConfig,
    OrgActions,
    OrgResponse,
    PaginatedResponse,
    PermissionBody,
    PermissionCheckResponse,
    Repo,
    RepoActions,
    RepoCreateBody,
    RepoImportBody,
    RepoKind,
    RepoMetadataT,
    RepoModifyRequest,
    RepoOperationMode,
    RepoOperationStatusResponse,
    RepoVisibility,
    S3Credentials,
    TokenAuthenticateBody,
    VirtualChunkAccessPolicyResponse,
)

# type adapters
LIST_ORGS_ADAPTER = TypeAdapter(list[OrgResponse])
LIST_DATABASES_ADAPTER = TypeAdapter(list[Repo])
LIST_DATABASES_PAGINATED_ADAPTER = TypeAdapter(PaginatedResponse[Repo])
LIST_BUCKETS_ADAPTER = TypeAdapter(list[BucketResponse])
LIST_REPOS_FOR_BUCKET_ADAPTER = TypeAdapter(list[Repo])
LIST_VCAPS_PAGINATED_ADAPTER = TypeAdapter(PaginatedResponse[VirtualChunkAccessPolicyResponse])
LIST_ICEBERG_NAMESPACES_ADAPTER = TypeAdapter(list[IcebergNamespaceResponse])


@dataclass
class HttpMetastoreConfig:
    """Encapsulates the configuration for the HttpMetastore"""

    api_service_url: str
    org: str
    token: str | None = field(default=None, repr=False)  # machine token. id/access/refresh tokens are managed by CustomOauth


class HttpMetastore(ArraylakeHttpClient, Metastore):
    """ArrayLake's HTTP Metastore

    This metastore connects to ArrayLake over HTTP

    args:
        config: config for the metastore

    :::note
    Authenticated calls require an Authorization header. Run ``arraylake auth login`` to login before using this metastore.
    :::
    """

    _config: HttpMetastoreConfig

    def __init__(self, config: HttpMetastoreConfig):
        super().__init__(config.api_service_url, token=config.token)

        self._config = config
        self.api_url = config.api_service_url

    async def ping(self) -> dict[str, Any]:
        response = await self._request("GET", "user")
        handle_response(response)

        return response.json()

    async def get_orgs(self) -> list[OrgResponse]:
        """List all orgs for the authenticated user."""
        response = await self._request("GET", "/user/orgs")
        handle_response(response)
        return LIST_ORGS_ADAPTER.validate_json(response.content)

    async def get_database(self, name: str) -> Repo:
        response = await self._request("GET", f"/repos/{self._config.org}/{name}")
        handle_response(response)
        return Repo.model_validate_json(response.content)

    async def open_repo(self, name: str) -> OpenRepoResponse:
        """Fetch everything needed to open a repo in a single request.

        Args:
            name: Name of the repository (without org prefix).

        Returns:
            OpenRepoResponse with storage config, credentials, VCC credentials, and author.
        """
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/open")
        handle_response(response)
        return OpenRepoResponse.model_validate_json(response.content)

    async def list_databases(
        self,
        filter_metadata: RepoMetadataT | None = None,
        include_ghosts: bool = False,
    ) -> list[Repo]:
        all_repos: list[Repo] = []
        page = 1
        while True:
            result = await self.list_databases_page(filter_metadata=filter_metadata, page=page, size=100, include_ghosts=include_ghosts)
            all_repos.extend(result.items)
            if result.page >= result.pages:
                break
            page += 1
        return all_repos

    async def list_databases_page(
        self,
        filter_metadata: RepoMetadataT | None = None,
        page: int = 1,
        size: int = 50,
        include_ghosts: bool = False,
    ) -> PaginatedResponse[Repo]:
        filter_metadata_json = json.dumps(filter_metadata) if filter_metadata else None
        params: dict[str, Any] = {"page": page, "size": size}
        if filter_metadata_json:
            params["filter_metadata"] = filter_metadata_json
        if include_ghosts:
            params["include_ghosts"] = "true"
        response = await self._request("GET", f"/orgs/{self._config.org}/repos/paginated", params=params)
        handle_response(response)
        return LIST_DATABASES_PAGINATED_ADAPTER.validate_json(response.content)

    async def create_database(
        self,
        name: str,
        bucket_nickname: str | None = None,
        kind: RepoKind = RepoKind.Icechunk,
        prefix: str | None = None,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
    ) -> Repo:
        """
        Creates a repo database entry in the metastore.

        Args:
            name: Name of the repo to create
            bucket_nickname: Optional nickname of a bucket already existing in the org.
            kind: Kind of repo to create
            prefix: Optional prefix for the icechunk repo
            description: Optional description for the repo
            metadata: Optional metadata for the repo

        Returns:
            The created Repo object
        """
        body = RepoCreateBody(
            name=name,
            bucket_nickname=bucket_nickname,
            kind=kind,
            prefix=prefix,
            create_mode="register",
            description=description,
            metadata=metadata,
        )
        response = await self._request("POST", f"/orgs/{self._config.org}/repos", content=body.model_dump_json())
        handle_response(response)
        repo = Repo.model_validate_json(response.content)

        if repo.kind == RepoKind.Icechunk:
            return repo

        raise ValueError(f"Unknown repo kind: {repo.kind}")

    async def import_database(
        self,
        name: str,
        bucket_nickname: str,
        prefix: str,
        kind: RepoKind = RepoKind.Icechunk,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
    ) -> Repo:
        """
        Imports an existing icechunk repo from storage.

        Args:
            name: Name of the repo to create
            bucket_nickname: Nickname of the bucket containing the existing icechunk repo.
            prefix: Prefix where the icechunk repo exists in the bucket.
            kind: Kind of repo to create
            description: Optional description for the repo
            metadata: Optional metadata for the repo

        Returns:
            The imported Repo object
        """
        body = RepoImportBody(
            name=name,
            bucket_nickname=bucket_nickname,
            kind=kind,
            prefix=prefix,
            description=description,
            metadata=metadata,
        )
        response = await self._request("POST", f"/orgs/{self._config.org}/repos/import", content=body.model_dump_json())
        handle_response(response)
        repo = Repo.model_validate_json(response.content)

        if repo.kind == RepoKind.Icechunk:
            return repo

        raise ValueError(f"Unknown repo kind: {repo.kind}")

    async def set_repo_status(self, name: str, mode: RepoOperationMode, message: str | None = None) -> RepoOperationStatusResponse:
        """Set repo status"""
        new_status = NewRepoOperationStatus(mode=mode, message=message)
        response = await self._request("PUT", f"/orgs/{self._config.org}/{name}/status", content=new_status.model_dump_json())
        handle_response(response)
        return RepoOperationStatusResponse.model_validate_json(response.content)

    async def modify_database(
        self,
        name: str,
        description: str | None = None,
        add_metadata: RepoMetadataT | None = None,
        remove_metadata: list[str] | None = None,
        update_metadata: RepoMetadataT | None = None,
        optimization_config: OptimizationConfig | None = None,
    ) -> None:
        # Only pass through what the caller actually supplied: passing an argument
        # explicitly puts it in model_fields_set, which would defeat exclude_unset
        # below and send a null for every field the caller left alone.
        supplied: dict[str, Any] = {
            "description": description,
            "add_metadata": add_metadata,
            "remove_metadata": remove_metadata,
            "update_metadata": update_metadata,
            "optimization_config": optimization_config,
        }
        repo_modify_request = RepoModifyRequest(**{k: v for k, v in supplied.items() if v is not None})
        response = await self._request(
            "PATCH", f"/orgs/{self._config.org}/{name}", content=repo_modify_request.model_dump_json(exclude_unset=True)
        )
        handle_response(response)

    async def delete_database(
        self,
        name: str,
        *,
        imsure: bool = False,
        imreallysure: bool = False,
        immediate: bool = False,
        retain_data: bool = False,
    ) -> None:
        if not (imsure and imreallysure):
            raise ValueError("Don't do this unless you're really sure. Once the database has been deleted, it's gone forever.")

        # Default behavior is a soft-delete: the repo enters a recoverable
        # "ghost" state for the grace period and the daily cleanup job reclaims
        # the bucket bytes afterward. Callers can opt out:
        #   immediate=True   - skip the grace period; ghost vanishes immediately
        #                      and the subscription cascade runs now
        #   retain_data=True - leave bucket bytes alone when the cleanup job
        #                      finalizes (only the Arraylake metadata is removed)
        # Setting both together makes the server drop the row inline so the
        # (org, name) slot is immediately reusable.
        params: dict[str, str] = {}
        if immediate:
            params["immediate"] = "true"
        if retain_data:
            params["retain_data"] = "true"
        response = await self._request(
            "DELETE",
            f"/orgs/{self._config.org}/{name}",
            params=params,
        )
        handle_response(response)

    # ------------------------------------------------------------------
    # Iceberg namespaces
    #
    # Namespaces are their own entity tree, served by the namespace management
    # API at /orgs/{org}/iceberg/namespaces. The Iceberg REST catalog itself
    # (mounted at /iceberg) is spoken to by pyiceberg, not by this metastore.
    # ------------------------------------------------------------------

    def _iceberg_namespace_url(self, name: str | None = None) -> str:
        url = f"/orgs/{quote(self._config.org, safe='')}/iceberg/namespaces"
        return f"{url}/{quote(name, safe='')}" if name is not None else url

    async def create_iceberg_namespace(
        self,
        name: str,
        *,
        bucket_nickname: str | None = None,
        description: str | None = None,
        metadata: RepoMetadataT | None = None,
        visibility: RepoVisibility = RepoVisibility.PRIVATE,
        properties: dict[str, str] | None = None,
    ) -> IcebergNamespaceResponse:
        body: dict[str, Any] = {"name": name}
        for key, value in {
            "bucket_nickname": bucket_nickname,
            "description": description,
            "metadata": metadata,
            "properties": properties,
        }.items():
            if value is not None:
                body[key] = value
        if visibility != RepoVisibility.PRIVATE:
            body["visibility"] = visibility.value
        response = await self._request("POST", self._iceberg_namespace_url(), content=json.dumps(body))
        handle_response(response)
        return IcebergNamespaceResponse.model_validate_json(response.content)

    async def get_iceberg_namespace(self, name: str) -> IcebergNamespaceResponse:
        response = await self._request("GET", self._iceberg_namespace_url(name))
        handle_response(response)
        return IcebergNamespaceResponse.model_validate_json(response.content)

    async def modify_iceberg_namespace(
        self,
        name: str,
        *,
        description: str | None = None,
        add_metadata: RepoMetadataT | None = None,
        remove_metadata: list[str] | None = None,
        update_metadata: RepoMetadataT | None = None,
        visibility: RepoVisibility | None = None,
    ) -> IcebergNamespaceResponse:
        body = {
            key: value
            for key, value in {
                "description": description,
                "add_metadata": add_metadata,
                "remove_metadata": remove_metadata,
                "update_metadata": update_metadata,
                "visibility": visibility.value if visibility is not None else None,
            }.items()
            if value is not None
        }
        response = await self._request("PATCH", self._iceberg_namespace_url(name), content=json.dumps(body))
        handle_response(response)
        return IcebergNamespaceResponse.model_validate_json(response.content)

    async def delete_iceberg_namespace(
        self, name: str, *, imsure: bool = False, immediate: bool = False, retain_data: bool = False
    ) -> None:
        """Delete an empty namespace: a restorable soft-delete unless ``immediate``."""
        if not imsure:
            raise ValueError("Don't do this unless you're sure. Pass imsure=True to delete the namespace.")
        params = {"imsure": "true"}
        if immediate:
            params["immediate"] = "true"
        if retain_data:
            params["retain_data"] = "true"
        response = await self._request("DELETE", self._iceberg_namespace_url(name), params=params)
        handle_response(response)

    async def restore_iceberg_namespace(self, name: str) -> None:
        response = await self._request("POST", f"{self._iceberg_namespace_url(name)}/restore")
        handle_response(response)

    async def list_iceberg_namespaces(self, *, include_ghosts: bool = False) -> list[IcebergNamespaceResponse]:
        params = {"include_ghosts": "true"} if include_ghosts else {}
        response = await self._request("GET", self._iceberg_namespace_url(), params=params)
        handle_response(response)
        return LIST_ICEBERG_NAMESPACES_ADAPTER.validate_json(response.content)

    async def list_iceberg_namespaces_page(
        self,
        *,
        filter_metadata: RepoMetadataT | None = None,
        search: str | None = None,
        sort: IcebergNamespaceSort | None = None,
        direction: Literal["asc", "desc"] = "desc",
        include_ghosts: bool = False,
        page: int = 1,
        size: int = 50,
    ) -> PaginatedResponse[IcebergNamespaceResponse]:
        params: dict[str, Any] = {"page": page, "size": size, "direction": direction}
        if filter_metadata is not None:
            params["filter_metadata"] = json.dumps(filter_metadata)
        if search is not None:
            params["search"] = search
        if sort is not None:
            params["sort"] = sort
        if include_ghosts:
            params["include_ghosts"] = "true"
        response = await self._request("GET", f"{self._iceberg_namespace_url()}/paginated", params=params)
        handle_response(response)
        return PaginatedResponse[IcebergNamespaceResponse].model_validate_json(response.content)

    async def list_iceberg_tables_page(
        self,
        name: str,
        *,
        search: str | None = None,
        sort: IcebergTableSort | None = None,
        direction: Literal["asc", "desc"] = "desc",
        page: int = 1,
        size: int = 50,
    ) -> PaginatedResponse[IcebergTableSummaryResponse]:
        params: dict[str, Any] = {"page": page, "size": size, "direction": direction}
        if search is not None:
            params["search"] = search
        if sort is not None:
            params["sort"] = sort
        response = await self._request("GET", f"{self._iceberg_namespace_url(name)}/tables/paginated", params=params)
        handle_response(response)
        return PaginatedResponse[IcebergTableSummaryResponse].model_validate_json(response.content)

    async def create_bucket_config(self, bucket_config: NewBucket) -> BucketResponse:
        response = await self._request(
            "POST",
            f"/orgs/{self._config.org}/buckets",
            content=bucket_config.model_dump_json(context={"reveal_secrets": True}),
        )
        handle_response(response)
        return BucketResponse.model_validate_json(response.content)

    async def get_bucket_config(self, bucket_id: UUID) -> BucketResponse:
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}")
        handle_response(response)
        return BucketResponse.model_validate_json(response.content)

    async def modify_bucket_config(self, bucket_id: UUID, bucket_config: BucketModifyRequest) -> BucketResponse:
        response = await self._request(
            "PATCH",
            f"/orgs/{self._config.org}/buckets/{bucket_id}",
            content=bucket_config.model_dump_json(context={"reveal_secrets": True}, exclude_unset=True),
        )
        handle_response(response)
        return BucketResponse.model_validate_json(response.content)

    async def delete_bucket_config(self, bucket_id: UUID) -> None:
        response = await self._request("DELETE", f"/orgs/{self._config.org}/buckets/{bucket_id}")
        handle_response(response)

    async def list_bucket_configs(self) -> list[BucketResponse]:
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets")
        handle_response(response)
        return LIST_BUCKETS_ADAPTER.validate_json(response.content)

    async def list_repos_for_bucket_config(self, bucket_id: UUID) -> list[Repo]:
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/repos")
        handle_response(response)
        return LIST_REPOS_FOR_BUCKET_ADAPTER.validate_json(response.content)

    async def set_default_bucket_config(self, bucket_id: UUID) -> None:
        response = await self._request("POST", f"/orgs/{self._config.org}/buckets/{bucket_id}/default")
        handle_response(response)

    async def get_s3_bucket_credentials_from_repo(self, name: str) -> S3Credentials:
        """Gets the S3 credentials for a repo."""
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/bucket-credentials")
        handle_response(response)
        return S3Credentials.model_validate_json(response.content)

    async def get_gs_bucket_credentials_from_repo(self, name: str) -> GSCredentials:
        """Gets the GCS credentials for a repo."""
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/bucket-credentials")
        handle_response(response)
        return GSCredentials.model_validate_json(response.content)

    async def get_azure_container_credentials_from_repo(self, name: str) -> AzureCredentials:
        """Gets the Azure credentials for a repo."""
        response = await self._request("GET", f"/repos/{self._config.org}/{name}/bucket-credentials")
        handle_response(response)
        return AzureCredentials.model_validate_json(response.content)

    async def get_s3_bucket_credentials_from_bucket(self, bucket_id: UUID, access: Literal["read", "write"] = "read") -> S3Credentials:
        """Gets the S3 credentials for a bucket.

        Defaults to read-only credentials; pass ``access="write"`` for read+write.
        """
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/credentials", params={"access": access})
        handle_response(response)
        return S3Credentials.model_validate_json(response.content)

    async def get_gs_bucket_credentials_from_bucket(self, bucket_id: UUID, access: Literal["read", "write"] = "read") -> GSCredentials:
        """Gets the GCS credentials for a bucket.

        Defaults to read-only credentials; pass ``access="write"`` for read+write.
        """
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/credentials", params={"access": access})
        handle_response(response)
        return GSCredentials.model_validate_json(response.content)

    async def get_azure_container_credentials_from_bucket(
        self, bucket_id: UUID, access: Literal["read", "write"] = "read"
    ) -> AzureCredentials:
        """Gets the Azure credentials for a bucket.

        Defaults to read-only credentials; pass ``access="write"`` for read+write.
        """
        response = await self._request("GET", f"/orgs/{self._config.org}/buckets/{bucket_id}/credentials", params={"access": access})
        handle_response(response)
        return AzureCredentials.model_validate_json(response.content)

    async def get_api_client_from_token(self, token: str) -> ApiClientResponse:
        token_body = TokenAuthenticateBody(token=token)
        data = token_body.model_dump()
        response = await self._request("GET", f"/orgs/{self._config.org}/api-clients/authenticate", params=data)
        handle_response(response)
        auth_resp = ApiClientResponse.model_validate_json(response.content)
        return auth_resp

    async def get_permission_check(self, principal_id: str, resource: str, action: OrgActions | RepoActions) -> bool:
        permission_body = PermissionBody(principal_id=principal_id, resource=resource, action=action.value)
        data = permission_body.model_dump()
        response = await self._request("GET", f"/orgs/{self._config.org}/permissions/check", params=data)
        handle_response(response)
        decision = PermissionCheckResponse.model_validate_json(response.content)
        return decision.has_permission

    async def get_virtual_chunk_containers(self, repo: str) -> dict[str, str | None]:
        """Get virtual chunk containers for a repo.

        Args:
            repo: Name of the repository.

        Returns:
            Mapping from virtual chunk container prefixes to bucket config nicknames.
        """
        response = await self._request("GET", f"/repos/icechunk/{self._config.org}/{repo}/virtual-chunk-containers")
        handle_response(response)
        return response.json()

    async def patch_virtual_chunk_containers(
        self,
        repo: str,
        add: dict[str, str] | None = None,
        remove: list[str] | None = None,
    ) -> dict[str, str | None]:
        """Update virtual chunk containers for a repo.

        Args:
            repo: Name of the repository.
            add: Mapping from VCC prefixes to bucket config nicknames to add.
            remove: List of VCC prefixes to remove.

        Returns:
            The updated mapping from virtual chunk container prefixes to bucket config nicknames.
        """
        payload = {"add": add or {}, "remove": remove or []}
        response = await self._request(
            "PATCH",
            f"/repos/icechunk/{self._config.org}/{repo}/virtual-chunk-containers",
            content=json.dumps(payload),
        )
        handle_response(response)
        return response.json()

    async def set_virtual_chunk_access_policy(
        self,
        *,
        bucket_id: str,
        subprefix: str,
        public: bool,
    ) -> VirtualChunkAccessPolicyResponse:
        """Set an explicit virtual chunk access policy on this org (idempotent).

        Args:
            bucket_id: Bucket ID for this VCAP.
            subprefix: Subprefix within the bucket for this VCAP.
            public: Whether this VCAP allows public access.
        """
        payload: dict[str, str | bool] = {
            "use_case": "explicit",
            "bucket_id": bucket_id,
            "subprefix": subprefix,
            "public": public,
        }
        response = await self._request(
            "PUT",
            f"/orgs/{self._config.org}/settings/virtual-chunk-access-policies",
            content=json.dumps(payload),
        )
        handle_response(response)
        return VirtualChunkAccessPolicyResponse.model_validate_json(response.content)

    async def list_virtual_chunk_access_policies(self) -> list[VirtualChunkAccessPolicyResponse]:
        """List all virtual chunk access policies on this org."""
        response = await self._request(
            "GET",
            f"/orgs/{self._config.org}/settings/virtual-chunk-access-policies",
            params={"size": 100},
        )
        handle_response(response)
        return LIST_VCAPS_PAGINATED_ADAPTER.validate_json(response.content).items

    async def delete_virtual_chunk_access_policy(
        self,
        *,
        bucket_id: str,
        subprefix: str,
        public: bool,
    ) -> None:
        """Delete an explicit virtual chunk access policy from this org (idempotent).

        Args:
            bucket_id: Bucket ID of the VCAP to delete.
            subprefix: Subprefix of the VCAP to delete.
            public: Whether this VCAP allows public access.
        """
        payload: dict[str, str | bool] = {
            "use_case": "explicit",
            "bucket_id": bucket_id,
            "subprefix": subprefix,
            "public": public,
        }
        response = await self._request(
            "DELETE",
            f"/orgs/{self._config.org}/settings/virtual-chunk-access-policies",
            content=json.dumps(payload),
        )
        handle_response(response)
