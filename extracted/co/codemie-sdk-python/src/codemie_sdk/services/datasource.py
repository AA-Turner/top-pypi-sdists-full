"""DataSource service implementation."""

from __future__ import annotations

import json
import mimetypes
from typing import Literal, Tuple, Any
from pathlib import Path

from ..models.common import PaginationParams
from ..models.datasource import (
    DataSource,
    DataSourceType,
    DataSourceStatus,
    BaseDataSourceRequest,
    CodeDataSourceRequest,
    UpdateCodeDataSourceRequest,
    BaseUpdateDataSourceRequest,
    FileDataSourceRequest,
    UpdateFileDataSourceRequest,
    CodeAnalysisDataSourceRequest,
    CodeExplorationDataSourceRequest,
    ElasticsearchStatsResponse,
)
from ..models.assistant import AssistantListResponse
from ..utils import ApiRequestHandler, TokenSource


class DatasourceService:
    """Service for managing CodeMie Datasources."""

    def __init__(self, api_domain: str, token: TokenSource, verify_ssl: bool = True):
        """Initialize the datasource service.

        Args:
            api_domain: Base URL for the CodeMie API
            token: Authentication token
            verify_ssl: Whether to verify SSL certificates
        """
        self._api = ApiRequestHandler(api_domain, token, verify_ssl)

    def create(self, request: BaseDataSourceRequest) -> dict:
        """Create a new datasource.

        Args:
            request: Create datasource request

        Returns:
            dict: Response from the server containing operation status
        """
        if isinstance(request, CodeDataSourceRequest):
            endpoint = f"/v1/application/{request.project_name}/index"
        else:
            # All other datasources follow the same pattern
            endpoint = f"/v1/index/knowledge_base/{request.type.name.lower()}"

        return self._api.post(
            endpoint,
            dict,
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

    @staticmethod
    def _build_file_uploads(
        files: list[str | Tuple[str, bytes, str]],
    ) -> list[tuple[str, tuple[str, bytes, str]]]:
        """Build multipart file tuples from file paths or (filename, content, mime_type) tuples.

        Args:
            files: List of files to upload. Each item can be:
                   - str: file path (will read file and detect MIME type)
                   - Tuple[str, bytes, str]: (filename, content, mime_type)

        Returns:
            list: Multipart-ready ("files", (filename, content, mime_type)) tuples
        """
        file_uploads = []

        for file_item in files:
            if isinstance(file_item, str):
                # File path provided - read file and detect MIME type
                file_path = Path(file_item)
                with open(file_path, "rb") as f:
                    content = f.read()

                # Basic MIME type detection
                mime_type = (
                    mimetypes.guess_type(file_path.name)[0]
                    or "application/octet-stream"
                )
                file_uploads.append(("files", (file_path.name, content, mime_type)))

            elif isinstance(file_item, tuple) and len(file_item) == 3:
                # (filename, content, mime_type) tuple provided
                filename, content, mime_type = file_item
                file_uploads.append(("files", (filename, content, mime_type)))

            else:
                raise ValueError(
                    "Each file must be either a file path (str) or a tuple of (filename, content, mime_type)"
                )

        return file_uploads

    def create_file_datasource(
        self,
        request: FileDataSourceRequest,
        files: list[str | Tuple[str, bytes, str]],
    ) -> dict:
        """Create a new file datasource with file uploads.

        Args:
            request: File datasource creation request
            files: List of files to upload. Each item can be:
                   - str: file path (will read file and detect MIME type)
                   - Tuple[str, bytes, str]: (filename, content, mime_type)

        Returns:
            dict: Response from the server containing operation status
        """
        endpoint = "/v1/index/knowledge_base/file"

        # Prepare multipart form data
        params = request.model_dump(by_alias=True, exclude_none=True)
        file_uploads = self._build_file_uploads(files)

        return self._api.post_multipart(
            endpoint, dict, params=params, files=file_uploads
        )

    def update(
        self,
        datasource_id: str,
        request: BaseUpdateDataSourceRequest,
        files: list[str | Tuple[str, bytes, str]] | None = None,
    ) -> dict:
        """Update an existing datasource.

        Args:
            request: Update datasource request
            files: Optional list of files to add to a File datasource. Each item
                   can be a file path (str) or a (filename, content, mime_type)
                   tuple. Only supported for UpdateFileDataSourceRequest.

        Returns:
            dict: Response from the server containing operation status
        """
        if isinstance(request, UpdateCodeDataSourceRequest):
            endpoint = f"/v1/application/{request.project_name}/index/{request.name}"
        else:
            endpoint = f"/v1/index/knowledge_base/{request.type.name.lower()}"

        # Extract reindex params
        params = {
            "full_reindex": request.full_reindex,
            "skip_reindex": request.skip_reindex,
            "resume_indexing": request.resume_indexing,
            "incremental_reindex": request.incremental_reindex,
        }

        # Remove reindex fields from request body
        data = request.model_dump(by_alias=True, exclude_none=True)
        for param in params.keys():
            data.pop(param, None)

        # PUT /index/knowledge_base/file now uses Depends() — all fields are query params
        if isinstance(request, UpdateFileDataSourceRequest):
            params.update(data)
            if files:
                file_uploads = self._build_file_uploads(files)
                return self._api.put_multipart(
                    endpoint, dict, params=params, files=file_uploads
                )
            return self._api.put(endpoint, dict, {}, params=params)

        return self._api.put(endpoint, dict, params=params, json_data=data)

    def list(
        self,
        page: int = 0,
        per_page: int = 10,
        sort_key: Literal["date", "update_date"] = "update_date",
        sort_order: Literal["asc", "desc"] = "desc",
        datasource_types: list[DataSourceType] = None,
        projects: list[str] = None,
        owner: str = None,
        status: DataSourceStatus = None,
        filters: dict[str, Any] | None = None,
    ) -> list[DataSource]:
        """
        List datasources with pagination and sorting support.

        Args:
            page: Page number (0-based). Defaults to 0.
            per_page: Number of items per page. Defaults to 10.
            sort_key: Field to sort by. Either "date" or "update_date". Defaults to "update_date".
            sort_order: Sort order. Either "asc" or "desc". Defaults to "desc".
            datasource_types: Optional data source types to filter by.
            projects: Optional projects to filter by.
            owner: Optional owner to filter by in format: FirstName LastName.
            status: Optional data source status to filter by.
            filters: Optional filters to apply. Should be a dictionary with filter criteria.

        Returns:
            DataSourceListResponse object containing list of datasources and pagination information.
        """
        params = PaginationParams(page=page, per_page=per_page).to_dict()
        params["sort_key"] = sort_key
        params["sort_order"] = sort_order

        unified_filters = {}
        if datasource_types:
            unified_filters["index_type"] = datasource_types
        if projects:
            unified_filters["project"] = projects
        if status:
            unified_filters["status"] = status.value
        if owner:
            unified_filters["created_by"] = owner
        if filters:
            unified_filters.update(filters)
        if unified_filters:
            params["filters"] = json.dumps(unified_filters)

        return self._api.get("/v1/index", list[DataSource], params=params)

    def get(self, datasource_id: str) -> DataSource:
        """
        Get datasource by ID.

        Args:
            datasource_id: The ID of the datasource to retrieve.

        Returns:
            DataSource object containing the datasource information.

        Raises:
            ApiError: If the datasource is not found or other API errors occur.
        """
        return self._api.get(f"/v1/index/{datasource_id}", DataSource)

    def delete(self, datasource_id: str) -> dict:
        """Delete an datasource by ID.

        Args:
            datasource_id: ID of the datasource to delete

        Returns:
            Deletion confirmation
        """
        return self._api.delete(f"/v1/index/{datasource_id}", dict)

    def get_assistants_using_datasource(
        self, datasource_id: str
    ) -> list[AssistantListResponse]:
        """Get list of assistants that are using this datasource.

        Args:
            datasource_id: ID of the datasource

        Returns:
            List of AssistantListResponse objects containing assistants using this datasource

        Raises:
            ApiError: If the datasource is not found or other API errors occur.
        """
        return self._api.get(
            f"/v1/index/{datasource_id}/assistants", list[AssistantListResponse]
        )

    def create_provider_datasource(
        self,
        toolkit_id: str,
        provider_name: str,
        request: CodeAnalysisDataSourceRequest | CodeExplorationDataSourceRequest,
    ) -> dict:
        """Create a provider-based datasource.

        Args:
            toolkit_id: ID of the toolkit to use
            provider_name: Name of the provider
            request: Provider datasource creation request (CodeAnalysisDataSourceRequest or CodeExplorationDataSourceRequest)

        Returns:
            dict: Response from the server containing operation status
        """
        endpoint = (
            f"/v1/index/provider?toolkit_id={toolkit_id}&provider_name={provider_name}"
        )

        return self._api.post(
            endpoint,
            dict,
            json_data=request.model_dump(by_alias=True, exclude_none=True),
        )

    def health_check(
        self,
        index_type: str,
        git_url: str = None,
        setting_id: str = None,
        project_name: str = None,
        space: str = None,
        wiki: str = None,
        **extra_kwargs,
    ) -> dict:
        """POST v1/index/health — probe datasource connectivity without indexing.

        Args:
            index_type: Type of the datasource index (e.g., "git", "xwiki", "jira")
            git_url: Git repository URL (required for git type)
            setting_id: Optional integration setting ID (for authenticated repos)
            project_name: Optional project name context (defaults to empty string)
            space: xWiki space id to probe (required for xwiki type)
            wiki: xWiki wiki id to probe (defaults to "xwiki" on the backend)
            **extra_kwargs: Additional payload fields forwarded verbatim (e.g.
                ``jql`` and ``custom_fields`` for Jira KB health checks).

        Returns:
            dict: Response containing 'error' (None on success), 'documents_count',
                and optionally 'field_error' / 'help' when a field-level validation
                error is detected.
        """
        payload: dict = {"index_type": index_type, "project_name": project_name or ""}
        if git_url is not None:
            payload["git_url"] = git_url
        if setting_id is not None:
            payload["setting_id"] = setting_id
        if space is not None:
            payload["space"] = space
        if wiki is not None:
            payload["wiki"] = wiki
        payload.update(extra_kwargs)
        return self._api.post("/v1/index/health", dict, json_data=payload)

    def get_jira_fields(self, setting_id: str, project_name: str = "") -> list:
        """GET /v1/index/jira/fields — retrieve available Jira custom fields.

        Returns the list of non-default Jira fields available for the given
        integration, sorted custom-first then alphabetically. Used by the UI
        field picker for the ``custom_fields`` datasource configuration.

        Args:
            setting_id: The Jira integration setting ID whose Jira instance
                should be queried for available fields.
            project_name: Project name context for the request.

        Returns:
            list: Sorted list of field dicts (``id``, ``name``, ``custom``).

        Raises:
            ApiError: HTTP 422 when the Jira instance is unreachable
                (ConnectionException maps to VPN-specific help text).
        """
        return self._api.get(
            f"/v1/index/jira/fields?setting_id={setting_id}&project_name={project_name}",
            list[dict],
        )

    def get_elasticsearch_stats(self, datasource_id: str) -> ElasticsearchStatsResponse:
        """Get Elasticsearch statistics for a specific datasource index.

        Args:
            datasource_id: ID of the datasource

        Returns:
            ElasticsearchStatsResponse with Elasticsearch statistics including:
            - index_name: Name of the index in Elasticsearch
            - size_in_bytes: Size of the index in bytes

        Raises:
            ApiError: If the datasource is not found, platform datasources are not supported,
                     or Elasticsearch statistics are not available.
        """
        return self._api.get(
            f"/v1/index/{datasource_id}/elasticsearch", ElasticsearchStatsResponse
        )
