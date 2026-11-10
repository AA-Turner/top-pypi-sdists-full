"""
Contract tests for SDK endpoints against OpenAPI specification.

These tests verify that SDK request construction conforms to the API spec
without making any network calls. Six test classes cover:

1. TestRequestContracts — every active module has standard SDK functions
2. TestAllEndpointsHaveValidPaths — strict path + method validation
3. TestSpecificEndpoints — detailed per-endpoint contract checks
4. TestDeprecatedEndpoints — deprecated/migration-pending raise correctly
5. TestBidirectionalCoverage — SDK↔spec drift detection
6. TestResponseContracts — _parse_response covers spec success codes
7. TestDeadModels — orphaned model files
8. TestUtilsApiWiring — utils→api import integrity
9. TestModelSerialization / TestResponseModels — serialization round-trips
"""

import importlib
import inspect
import re
from pathlib import Path
from typing import Any, Dict
from urllib.parse import urlparse

import pytest
from conftest import (
    ALL_API_MODULES,
    API_IMPORT_ERRORS,
    API_MODULES,
    import_api_module,
)

SDK_ROOT = Path(__file__).parent.parent / "octostar"

# ---------------------------------------------------------------------------
# SDK endpoints targeting paths that don't exist in the OpenAPI spec yet.
# These get xfail — the SDK module is structurally correct but the backend
# hasn't exposed the route.
# ---------------------------------------------------------------------------
KNOWN_MISSING_PATH_ENDPOINTS = {
    # All previously-missing paths are now in the spec.
    # Keep this dict for any future SDK modules that precede backend routes.
}

# ---------------------------------------------------------------------------
# Spec routes that intentionally have no SDK endpoint.
# Grouped by category with justification.
# ---------------------------------------------------------------------------
SPEC_ROUTES_WITHOUT_SDK = {
    # Health & probes
    "/": "Root redirect",
    "/health": "Health check",
    "/favicon.ico": "Browser favicon",
    "/api/v1/health": "Health check",
    "/api/v1/health/images": "Image health probe",
    "/api/v1/health/liveness": "K8s liveness probe",
    "/api/v1/health/readiness": "K8s readiness probe",
    "/api/v1/health/startup": "K8s startup probe",
    # Auth / OAuth (browser-only flows)
    "/login": "Browser login page",
    "/logout": "Browser logout page",
    "/internal/set_ontology_cookie": "Internal cookie management",
    "/api/v1/auth/auth/external": "External auth redirect",
    "/api/v1/auth/oauth2/callback": "OAuth2 callback",
    "/api/v1/auth/oauth2/login": "OAuth2 login redirect",
    "/api/v1/auth/oauth2/logout": "OAuth2 logout",
    "/api/v1/auth/oauth2/logout/callback": "OAuth2 logout callback",
    # SDK downloads (self-referential)
    "/api/v1/meta/sdk/octostar-python-client.tar.gz": "SDK tarball download",
    "/api/v1/meta/sdk/octostar_python_client.whl": "SDK wheel download",
    # Manifest validation & schema (editor-only, not SDK-suitable)
    "/api/v1/apps/bulk": "Bulk redeploy/undeploy (frontend-driven; poll via tasks API)",
    "/api/v1/apps/manifest-schema": "Manifest JSON Schema for frontend editor",
    "/api/v1/apps/validate-manifest": "Manifest YAML validation for frontend editor",
    # K8s events streaming (SSE event stream, not SDK-suitable)
    "/api/v1/apps/{workspace}/{entity_id}/events": "SSE K8s status events stream",
    # K8s log streaming (SSE event stream, not SDK-suitable)
    "/api/v1/apps/{workspace}/{entity_id}/logs/stream": "SSE K8s pod log stream",
    # AI Chat (complex streaming, not SDK-suitable)
    "/api/v1/chat": "AI chat (streaming)",
    "/api/v1/chat/models": "AI chat model listing",
    "/api/v1/chat/templates": "AI chat templates",
    "/api/v1/chat/detokenize": "Legacy detokenize",
    "/api/v1/chat/tokenize": "Legacy tokenize",
    "/api/v2/ai/llm/complete": "Completion (wrapped via utils/chat/complete.py)",
    "/api/v2/ai/llm/detokenize": "Detokenize (wrapped via utils/chat/detokenize.py)",
    "/api/v2/ai/llm/tokenize": "Tokenize (wrapped via utils/chat/tokenize.py)",
    # File operations (multipart upload/download, not yet SDK-wrapped)
    "/api/v1/files/content/{token}": "File download by token",
    "/api/v1/files/download-blob/{filename}": "Blob download",
    "/api/v1/files/download/{os_workspace}/{path}": "File download",
    "/api/v1/files/list/{os_workspace}": "File listing",
    "/api/v1/files/list/{os_workspace}/{path}": "File listing at path",
    "/api/v1/files/source/list/{os_workspace}": "Source-backed file peek (by entity_id)",
    "/api/v1/files/source/list/{os_workspace}/{path}": "Source-backed file peek (by path)",
    "/api/v1/files/source/bytes/{os_workspace}": "Source-backed byte stream (peek-before-export; HEAD/GET with Range)",
    "/api/v1/files/source/export/{os_workspace}": "Source-backed bulk export (files + folders, two-phase upsert)",
    "/api/v1/files/source/extract/{os_workspace}": "Selection extraction job from a zip (frontend Archive Previewer)",
    "/api/v1/files/stat/{os_workspace}": "File stat",
    "/api/v1/files/stat/{os_workspace}/{path}": "File stat at path",
    "/api/v1/files/upload-blob/{filename}": "Blob upload",
    "/api/v1/files/create/{os_workspace}": "File creation",
    "/api/v1/files/create/{os_workspace}/{file_path}": "File creation at path",
    "/api/v1/files/move/{os_workspace}/{path}": "File move",
    "/api/v1/files/mkdir/{os_workspace}/{path}": "Directory creation",
    "/api/v1/files/mkdir-parent/{os_workspace}/{os_parent_folder}/{path}": "Parent dir creation",
    "/api/v1/files/unzip/{os_workspace}/{entity_id}": "File unzip in workspace",
    "/api/v1/files/delete-file/{os_workspace}/{entity}": "File deletion",
    "/api/v1/files/delete-recursive/{os_workspace}/{entity}": "Recursive deletion",
    "/api/v1/files/attachments/batch_attachments": "Batch attachment upload",
    "/api/v1/files/attachments/{os_workspace}/{entity_id}": "Attachment upload",
    # v2 Files
    "/api/v2/files/upload-from-url/{os_workspace}": "Server-side URL fetch + stream-to-S3 (no temp files)",
    # v2 Report export
    "/api/v2/report-export/capabilities": "Composer export dialog limits; no SDK export flow",
    "/api/v2/report-export/download/{tracking_id}": "Composer temporary export download; no SDK export flow",
    "/api/v2/report-export/{os_workspace}/{entity_uid}": "Report export job started from the Composer (202; poll tasks/status)",
    # v2 Workspaces
    "/api/v2/workspaces/{os_workspace}": "Whole-workspace delete (202 background job; poll tasks/status)",
    # v2 Mounts (Phase 0 scaffold — 501 stubs, SDK wrappers land with each capability)
    "/api/v2/mounts": "Mount create/list",
    "/api/v2/mounts/{mount_id}": "Mount get/update/delete",
    "/api/v2/mounts/{mount_id}/test": "Mount connectivity test",
    "/api/v2/mounts/{mount_id}/grants": "Mount grants list/create",
    "/api/v2/mounts/{mount_id}/grants/{grant_id}": "Mount grant revoke",
    "/api/v2/mounts/{mount_id}/credentials": "Per-user mount credentials",
    "/api/v2/mounts/{mount_id}/browse": "Remote source browse",
    "/api/v2/mounts/{mount_id}/import": "Remote → workspace import",
    "/api/v2/mounts/{mount_id}/preview-bytes": "Mount file preview byte stream",
    "/api/v2/relationships/query": "Relationship query (count body or ndjson edge stream)",
    # v2 Ontology read surface — the v1 wrappers (get_ontologies, fetch_ontology_data)
    # stay the SDK path until the localized labels in TEAM-6928 give v2 something v1 lacks.
    "/api/v2/ontologies": "Ontology listing with active/default flags",
    "/api/v2/ontologies/{ontology}/schema": "Canonical ontology schema by path",
    # Resumable (tus) attachment uploads (tus 1.0.0 client protocol, not SDK-suitable)
    "/api/v2/entities/{os_workspace}/{entity_uid}/attachment/uploads": "tus create/discovery",
    "/api/v2/entities/{os_workspace}/{entity_uid}/attachment/uploads/{upload_id}": "tus offset/append/abort",
    # Geocoding
    "/api/v1/geocoding/geocode": "Geocoding lookup",
    "/api/v1/geocoding/reverse": "Reverse geocoding",
    # Settings (admin UI)
    "/api/v1/settings/": "Settings CRUD",
    "/api/v1/settings/flat": "Settings flat view",
    "/api/v1/settings/{key}": "Settings by key",
    "/api/v1/settings/general": "General settings",
    # Tags listing (GET only, no SDK wrapper needed)
    "/api/v1/tags/": "Tags listing",
    "/api/v1/tags/{os_workspace}": "Tags by workspace",
    # Tasks (background job tracking)
    "/api/v1/tasks/status": "Task status listing",
    "/api/v1/tasks/status/{tracking_id}": "Task status by ID",
    "/api/v1/tasks/{tracking_id}": "Task operations",
    "/api/v1/tasks/{tracking_id}/delete": "Task deletion",
    "/api/v1/tasks/bulk-delete": "Bulk task deletion",
    # Pipeline (admin operations)
    "/api/v1/pipeline/stats": "Pipeline statistics",
    "/api/v1/pipeline/totals": "Pipeline totals",
    "/api/v1/pipeline/health": "Pipeline health",
    # Pipeline operator console (admin observability + control, not SDK-suitable)
    "/api/v1/pipeline/console/snapshot": "Operator console snapshot (admin UI)",
    "/api/v1/pipeline/console/issues": "Operator console issues report (admin UI)",
    "/api/v1/pipeline/console/timing": "Operator console timing report (admin UI)",
    "/api/v1/pipeline/control/stop": "Operator console: stop workflows (admin UI)",
    "/api/v1/pipeline/control/restart": "Operator console: restart workflows (admin UI)",
    # Search API
    "/api/v1/search_api/get_filter_workspaces": "Search filter workspaces",
    "/api/v1/search_api/get_filters": "Search filters",
    "/api/v1/search_api/{ontology}/entities": "Search entities",
    "/api/v1/search_api/{ontology}/mapping": "Search mapping",
    "/api/v1/search_api/{ontology}/searchable_fields": "Searchable fields",
    "/api/v1/search_api/{ontology}/_msearch": "Multi-search",
    "/api/v1/search_api/{ontology}/refresh-opensearch-mapping": "Refresh mapping",
    # Entity operations (not yet SDK-wrapped)
    "/api/v1/entities/copy": "Entity copy",
    "/api/v1/entities/create-workspace": "Workspace creation",
    "/api/v1/entities/workspace-records/{os_workspace}": "Workspace records",
    "/api/v1/entities/records/by-source/{os_workspace}": "Workspace records by import source",
    "/api/v1/entities/{concept}/{os_workspace}": "Entities by concept",
    # Notifications operations (partially SDK-wrapped)
    "/api/v1/notifications/mark_as": "Mark notifications read/unread",
    # Realtime events
    "/api/v1/realtime_events/send": "Realtime event dispatch",
    # Relationships
    "/api/v1/relationships/entities/expand": "Relationship expansion",
    "/api/v1/relationships/entities/expand/count": "Expansion count",
    "/api/v1/relationships/entities/expand/edge-discovery": "Induced-subgraph edge discovery",
    # Sets
    "/api/v1/sets/count": "Set count",
    "/api/v1/sets/expand": "Set expansion (NDJSON streaming)",
    "/api/v1/sets/opensearch-query": "OpenSearch set query",
    # UI components
    "/api/v1/ui/": "UI component serving",
    "/api/v1/ui/return_channel": "UI return channel",
    # Ontology operations (partially SDK-wrapped)
    "/api/v1/ontology/query/stream": "Streaming query",
    "/api/v1/ontology/relationship_mappings": "Relationship mappings",
    "/api/v1/ontology/refresh_local_tables": "Refresh local tables",
    # Permissions (partially SDK-wrapped)
    "/api/v1/permissions/verify-write-permissions": "Write permission check",
    "/api/v1/permissions/workspace-permissions/roles": "Permission roles listing",
    "/api/v1/permissions/workspace-permissions/users": "Permission users listing",
    # Apps (partially SDK-wrapped)
    "/api/v1/apps/list": "App listing (alternative endpoint)",
    "/api/v1/apps/reconcile-orphans": "Operator orphan-deployment GC (admin affordance, not SDK-suitable)",
    "/api/v1/apps/secrets/": "Secrets management",
    # TEAM-8348: new frontend-facing app contract routes; SDK wrappers are not
    # planned yet, the frontend calls them directly.
    "/api/v1/apps/{workspace}/{entity_id}": "Single-app lookup (one list row)",
    "/api/v1/apps/{app_id}/secrets": "RESTful app secrets (GET/PUT/DELETE)",
    # Archive / workspace import-export
    "/api/v1/archive/export/{os_workspace}": "Archive export",
    "/api/v1/archive/import/": "Archive import",
    "/api/v1/workspace/export/{os_workspace}": "Workspace export",
    "/api/v1/workspace/import/": "Workspace import",
    "/api/v1/folders/export": "Folder export",
    "/api/v1/folders/import": "Folder import",
    # Pipeline operations
    "/api/v1/pipeline/send": "Pipeline send",
    "/api/v1/pipeline/stop": "Pipeline processing cancel",
    "/api/v1/pipeline/cleanup-orphan-fragments": "Pipeline orphan-fragment cleanup",
    # Search API (additional)
    "/api/v1/search_api/index": "Direct OpenSearch indexing",
    "/api/v1/search_api/{ontology}/_count": "Search count",
    "/api/v1/search_api/{ontology}/_index_definition": "Index definition",
    # V2 Entities API (SDK-wrapped via write_file, read_file, write_attachment, read_attachment)
    "/api/v2/entities/{os_workspace}": "V2 entity creation",
    "/api/v2/entities/{os_workspace}/{entity_uid}": "V2 entity operations",
    "/api/v2/entities/{os_workspace}/{entity_uid}/attachment": "V2 entity attachment",
    "/api/v2/entities/{os_workspace}/{entity_uid}/attachment/_thumbnail": "V2 entity attachment thumbnail (browser image URL, not an SDK call)",
}

# ---------------------------------------------------------------------------
# Utils files known to use raw API calls instead of the api/ layer.
# These get xfail — to be refactored to use the api/ modules.
# ---------------------------------------------------------------------------
KNOWN_RAW_API_UTILS = {
    "utils/workspace/get_attachment_url.py": "known using raw api, to be changed",
    "utils/workspace/read_file.py": "known using raw api, to be changed",
    "utils/workspace/read_temporary_blob.py": "builds API URLs directly for presigned URL + HEAD flow",
    "utils/workspace/write_temporary_blob.py": "builds API URLs directly for presigned upload flow",
    "utils/workspace/delete_temporary_blob.py": "builds API URLs directly for delete flow",
}

# ---------------------------------------------------------------------------
# Utils → API wiring pairs.
# Each entry is (utils_file_relative_to_SDK_ROOT, api_module_pattern).
# The meta-test ensures every utils file importing from api/ is listed here.
# ---------------------------------------------------------------------------
UTILS_API_WIRING = [
    # Pipeline
    (
        "utils/pipeline/get_processing_status.py",
        "api.pipeline.get_processing_status",
    ),
    ("utils/pipeline/update_processing_status.py", "api.pipeline"),
    # Workspace permissions
    (
        "utils/workspace/permissions/get_permissions.py",
        "api.workspace_permissions.get_permissions",
    ),
    # Workspace tags
    ("utils/workspace/tags/tag_entities.py", "api.workspace_tags.tag_entities"),
    (
        "utils/workspace/tags/delete_tag_from_entities.py",
        "api.workspace_tags.delete_tag_from_entities",
    ),
    # Workspace data
    ("utils/workspace/delete_entities.py", "api.workspace_data.delete_entities"),
    ("utils/workspace/get_files_tree.py", "api.workspace_data.get_files_tree"),
    # Metadata
    ("utils/meta/get_whoami.py", "api.metadata.get_whoami"),
    ("utils/meta/get_version.py", "api.metadata.get_version"),
    # Ontology
    ("utils/ontology/query_ontology.py", "api.ontology.query"),
    ("utils/ontology/fetch_ontology_data.py", "api.ontology.fetch_ontology_data"),
    ("utils/ontology/multiquery_ontology.py", "api.ontology.multi_query"),
    ("utils/ontology/get_ontologies.py", "api.ontology.get_ontologies"),
    # Jobs
    # Apps
    ("utils/jobs/apps/deploy_app.py", "api.apps.deploy_app"),
    ("utils/jobs/apps/undeploy_app.py", "api.apps.undeploy_app"),
    ("utils/jobs/apps/get_app_logs.py", "api.apps.get_app_logs"),
    ("utils/jobs/apps/get_apps_url.py", "api.apps.get_apps_url"),
    # Notifications
    (
        "utils/notifications/get_my_subscriptions.py",
        "api.notifications.get_subscriptions",
    ),
    ("utils/notifications/toast.py", "api.notifications.toast"),
    (
        "utils/notifications/publish_notification.py",
        "api.notifications.publish_notification",
    ),
    # Search
    (
        "utils/search/get_entity_annotations.py",
        "api.search.get_annotations",
    ),
]


# ---------------------------------------------------------------------------
# Example parameters for dynamic endpoint invocation
# ---------------------------------------------------------------------------


def get_example_params() -> dict:
    """Realistic example parameters for all active SDK endpoints."""
    from octostar.models import (
        GetAppsUrlJsonBody,
        MultiQueryJsonBody,
        MultiQueryJsonBodyQueriesItem,
        OsNotification,
        QueryJsonBody,
        UpsertEntity,
        UpsertEntityBase,
    )
    from octostar.models.entity import Entity

    return {
        # Common identifiers
        "app_id": "test-app-123",
        "workspace": "test-workspace-789",
        "os_entity_uid": "test-entity-uid-abc",
        "ontology": "test_ontology",
        "os_workspace": "test-workspace-alpha",
        "tag": "test-tag-name",
        "os_concept": "Person",
        "entity_id": "entity-uid-abc123",
        "file_path": "attachments/document.pdf",
        "filename": "export-2024.csv",
        "ws_id": "workspace-abc",
        "wso_id": "wso-xyz-789",
        # JSON bodies keyed as "json_body:<endpoint_name>"
        "json_body:delete_entities": ["entity-uid-1", "entity-uid-2"],
        "json_body:upsert_entities": [
            UpsertEntity(
                entity=UpsertEntityBase(
                    entity_id="person-001",
                    os_entity_uid="person-001",
                    entity_type="Person",
                    entity_label="John Doe",
                )
            )
        ],
        # Toast requires message in the JSON body per spec
        "message:toast": "Test notification",
        "json_body:publish_notification": [
            OsNotification(
                channel="workspace:ws-123",
                title="Entity Updated",
                body="Person record modified",
            )
        ],
        "json_body:query": QueryJsonBody(query="SELECT * FROM Person LIMIT 10"),
        "json_body:multi_query": MultiQueryJsonBody(
            queries=[
                MultiQueryJsonBodyQueriesItem(
                    query_id="q1", sql="SELECT * FROM Person LIMIT 5"
                ),
            ]
        ),
        "json_body:get_apps_url": GetAppsUrlJsonBody(app_ids=["app-1", "app-2"]),
        # Tags
        "json_body:tag_entities": [Entity("test-entity-uid", "Person")],
        "json_body:delete_tag_from_entities": [Entity("test-entity-uid", "Person")],
        # Pipeline processing status
        "entity_ids": ["entity-uid-1", "entity-uid-2"],
        "json_body:update_processing_status": [
            {
                "entity_id": "entity-uid-1",
                "entity_type": "File",
                "status_code": "RUNNING",
                "do_not_update_before": "2026-03-09T10:00:00Z",
            },
        ],
        # Search annotations
        "json_body:get_annotations": {
            "os_entity_uids": ["entity-uid-1"],
            "recurse": True,
            "merge": True,
        },
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _build_kwargs_for_endpoint(
    module_name: str,
    endpoint_name: str,
    mock_client,
    example_params: dict,
    strict: bool = True,
) -> Dict[str, Any]:
    """Build kwargs dict for calling _get_kwargs on any endpoint module.

    If strict=True, missing required params cause pytest.fail().
    If strict=False, missing required params cause pytest.skip().
    """
    module = importlib.import_module(module_name)
    get_kwargs = getattr(module, "_get_kwargs")
    sig = inspect.signature(get_kwargs)
    kwargs_to_call = {}

    for param_name, param in sig.parameters.items():
        if param_name == "client":
            kwargs_to_call["client"] = mock_client
        elif param_name in ("args", "kwargs"):
            continue
        else:
            endpoint_key = f"{param_name}:{endpoint_name}"
            if endpoint_key in example_params:
                kwargs_to_call[param_name] = example_params[endpoint_key]
            elif param_name in example_params:
                kwargs_to_call[param_name] = example_params[param_name]
            elif param.default is inspect.Parameter.empty:
                msg = (
                    f"{module_name}: required param '{param_name}' has no example. "
                    f"Add it to get_example_params()."
                )
                if strict:
                    pytest.fail(msg)
                else:
                    pytest.skip(msg)

    return get_kwargs(**kwargs_to_call)


def _paths_match(spec_parts: list, actual_parts: list) -> bool:
    """Check if actual URL path parts match a spec path pattern."""
    if len(spec_parts) == len(actual_parts):
        for spec_part, actual_part in zip(spec_parts, actual_parts):
            if spec_part.startswith("{") and spec_part.endswith("}"):
                continue
            if spec_part != actual_part:
                return False
        return True

    # Catch-all: spec has fewer parts, last segment is a path parameter
    if (
        len(actual_parts) > len(spec_parts)
        and spec_parts
        and spec_parts[-1].startswith("{")
    ):
        for i in range(len(spec_parts) - 1):
            if not spec_parts[i].startswith("{") and spec_parts[i] != actual_parts[i]:
                return False
        return True

    return False


def _http_code_to_status_name(code: str) -> str:
    """Map HTTP status code string to the HTTPStatus attribute name used in source."""
    return {
        "200": "HTTPStatus.OK",
        "201": "HTTPStatus.CREATED",
        "202": "HTTPStatus.ACCEPTED",
        "204": "HTTPStatus.NO_CONTENT",
    }.get(code, "")


# ===================================================================
# Test classes
# ===================================================================


class TestRequestContracts:
    """Verify all SDK endpoint modules follow the standard pattern."""

    @pytest.mark.parametrize("module_name,endpoint_name", API_MODULES)
    def test_module_has_standard_functions(self, module_name: str, endpoint_name: str):
        """Every active API module must have _get_kwargs, _parse_response, and
        at least one execution function (sync/asyncio)."""
        module = importlib.import_module(module_name)

        assert hasattr(module, "_get_kwargs"), f"{module_name} missing _get_kwargs"
        assert hasattr(module, "_parse_response"), (
            f"{module_name} missing _parse_response"
        )

        has_execution = any(
            hasattr(module, fn)
            for fn in ["sync", "sync_detailed", "asyncio", "asyncio_detailed"]
        )
        assert has_execution, f"{module_name} missing execution functions"


class TestAllEndpointsHaveValidPaths:
    """Strict: every active SDK endpoint must target a valid OpenAPI path
    and use the correct HTTP method."""

    @pytest.mark.parametrize("module_name,endpoint_name", API_MODULES)
    def test_endpoint_path_exists_in_spec(
        self, module_name: str, endpoint_name: str, request_validator, mock_client
    ):
        """SDK-constructed URL must resolve to a real OpenAPI path."""
        if endpoint_name in KNOWN_MISSING_PATH_ENDPOINTS:
            pytest.xfail(KNOWN_MISSING_PATH_ENDPOINTS[endpoint_name])

        result_kwargs = _build_kwargs_for_endpoint(
            module_name, endpoint_name, mock_client, get_example_params()
        )

        url = result_kwargs.get("url", "")
        base_url = mock_client.base_url
        v1_base_url = mock_client.get_base_url_v1()
        assert url.startswith(base_url) or url.startswith(v1_base_url), (
            f"URL {url} doesn't start with {base_url} or {v1_base_url}"
        )

        validation = request_validator.validate_request(result_kwargs)
        if not validation.is_valid:
            pytest.fail(
                f"SDK/spec contract violation for {endpoint_name}:\n"
                + "\n".join(f"  - {e}" for e in validation.errors)
            )

    @pytest.mark.parametrize("module_name,endpoint_name", API_MODULES)
    def test_endpoint_method_matches_spec(
        self, module_name: str, endpoint_name: str, request_validator, mock_client
    ):
        """SDK HTTP method must match what the spec declares for that path."""
        if endpoint_name in KNOWN_MISSING_PATH_ENDPOINTS:
            pytest.xfail(KNOWN_MISSING_PATH_ENDPOINTS[endpoint_name])

        result_kwargs = _build_kwargs_for_endpoint(
            module_name, endpoint_name, mock_client, get_example_params()
        )

        result = request_validator.validate_method(result_kwargs)
        if not result.is_valid:
            pytest.fail(
                f"HTTP method mismatch for {endpoint_name}:\n"
                + "\n".join(f"  - {e}" for e in result.errors)
            )


class TestSpecificEndpoints:
    """Detailed contract tests for individual endpoints with example data."""

    # --- Metadata ---

    def test_get_whoami_request(self, request_validator, mock_client):
        from octostar.api.metadata import get_whoami

        kwargs = get_whoami._get_kwargs(client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/meta/whoami"
        )
        result.raise_if_invalid()

    def test_get_version_request(self, request_validator, mock_client):
        from octostar.api.metadata import get_version

        kwargs = get_version._get_kwargs(client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/meta/version"
        )
        result.raise_if_invalid()

    # --- Ontology ---

    def test_get_ontologies_request(self, request_validator, mock_client):
        from octostar.api.ontology import get_ontologies

        kwargs = get_ontologies._get_kwargs(client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/ontology/get_ontologies"
        )
        result.raise_if_invalid()

    def test_ontology_query_request(self, request_validator, mock_client):
        from octostar.api.ontology import query
        from octostar.models import QueryJsonBody

        kwargs = query._get_kwargs(
            client=mock_client,
            json_body=QueryJsonBody(query="SELECT * FROM entities LIMIT 10"),
            ontology="test_ontology",
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/ontology/query"
        )
        result.raise_if_invalid()

    def test_multi_query_request(self, request_validator, mock_client):
        from octostar.api.ontology import multi_query
        from octostar.models import MultiQueryJsonBody, MultiQueryJsonBodyQueriesItem

        kwargs = multi_query._get_kwargs(
            client=mock_client,
            ontology="test_ontology",
            json_body=MultiQueryJsonBody(
                queries=[
                    MultiQueryJsonBodyQueriesItem(query_id="q1", sql="SELECT 1"),
                ]
            ),
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/ontology/multi_query"
        )
        result.raise_if_invalid()

    def test_fetch_ontology_data_request(self, request_validator, mock_client):
        from octostar.api.ontology import fetch_ontology_data

        kwargs = fetch_ontology_data._get_kwargs(client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/ontology/fetch_ontology_data"
        )
        result.raise_if_invalid()

    # --- Workspace data ---

    def test_delete_entities_request(self, request_validator, mock_client):
        from octostar.api.workspace_data import delete_entities

        kwargs = delete_entities._get_kwargs(
            client=mock_client, json_body=["entity-uid-1", "entity-uid-2"]
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/entities/delete"
        )
        result.raise_if_invalid()

    def test_upsert_entities_request(self, request_validator, mock_client):
        from octostar.api.workspace_data import upsert_entities
        from octostar.models import UpsertEntity, UpsertEntityBase

        entity = UpsertEntity(
            entity=UpsertEntityBase(
                entity_id="test-entity",
                entity_type="Person",
                os_entity_uid="test-uid",
            )
        )
        kwargs = upsert_entities._get_kwargs(client=mock_client, json_body=[entity])
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/entities/upsert"
        )
        result.raise_if_invalid()

    def test_get_attachment_request(self, request_validator, mock_client):
        from octostar.api.workspace_data import get_attachment

        kwargs = get_attachment._get_kwargs(
            client=mock_client, workspace="test-ws", file_path="path/to/file.txt"
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/files/attachments/{path}"
        )
        result.raise_if_invalid()

    def test_get_files_tree_request(self, request_validator, mock_client):
        from octostar.api.workspace_data import get_files_tree

        kwargs = get_files_tree._get_kwargs(client=mock_client, os_workspace="test-ws")
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/files/tree"
        )
        result.raise_if_invalid()

    # --- Notifications ---

    def test_publish_notification_request(self, request_validator, mock_client):
        from octostar.api.notifications import publish_notification
        from octostar.models import OsNotification

        notification = OsNotification(channel="test", title="Test", body="Body")
        kwargs = publish_notification._get_kwargs(
            client=mock_client, json_body=[notification]
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/notifications/"
        )
        result.raise_if_invalid()

    def test_toast_request(self, request_validator, mock_client):
        """Validates POST method + JSON body after SDK fix."""
        from octostar.api.notifications import toast

        kwargs = toast._get_kwargs(
            client=mock_client, message="Hello", description="World"
        )
        assert kwargs["method"] == "post", "toast must use POST"
        assert "json" in kwargs, "toast must send JSON body"
        json_body = kwargs["json"]
        assert json_body.get("message") == "Hello"
        assert json_body.get("description") == "World"
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/notifications/toast"
        )
        result.raise_if_invalid()

    def test_get_subscriptions_request(self, request_validator, mock_client):
        from octostar.api.notifications import get_subscriptions

        kwargs = get_subscriptions._get_kwargs(client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/notifications/subscriptions"
        )
        result.raise_if_invalid()

    # --- Permissions ---

    def test_get_permissions_request(self, request_validator, mock_client):
        """Validates POST method + JSON body after SDK fix."""
        from octostar.api.workspace_permissions import get_permissions

        kwargs = get_permissions._get_kwargs(
            client=mock_client,
            os_workspace="workspace-1",
            os_workspaces="workspace-2,workspace-3",
        )
        assert kwargs["method"] == "post", "get_permissions must use POST"
        assert "json" in kwargs, "get_permissions must send JSON body"
        json_body = kwargs["json"]
        assert "workspaces" in json_body
        assert "workspace-1" in json_body["workspaces"]
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/permissions/workspace-permissions"
        )
        result.raise_if_invalid()

    # --- Apps ---

    def test_list_apps_request(self, request_validator, mock_client):
        from octostar.api.apps import list_apps

        kwargs = list_apps._get_kwargs(client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/apps/"
        )
        result.raise_if_invalid()

    def test_deploy_app_request(self, request_validator, mock_client):
        from octostar.api.apps import deploy_app

        kwargs = deploy_app._get_kwargs(
            workspace="test-ws", os_entity_uid="test-entity", client=mock_client
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/apps/deploy/{workspace}/{entity_id}"
        )
        result.raise_if_invalid()

    def test_undeploy_app_request(self, request_validator, mock_client):
        from octostar.api.apps import undeploy_app

        kwargs = undeploy_app._get_kwargs(app_id="test-app", client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/apps/{app_id}"
        )
        result.raise_if_invalid()

    def test_get_app_logs_request(self, request_validator, mock_client):
        from octostar.api.apps import get_app_logs

        kwargs = get_app_logs._get_kwargs(app_id="test-app", client=mock_client)
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/apps/logs/{app_id}"
        )
        result.raise_if_invalid()

    def test_get_apps_url_request(self, request_validator, mock_client):
        from octostar.api.apps import get_apps_url
        from octostar.models import GetAppsUrlJsonBody

        kwargs = get_apps_url._get_kwargs(
            client=mock_client,
            json_body=GetAppsUrlJsonBody(app_ids=["app-1"]),
        )
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/apps/urls"
        )
        result.raise_if_invalid()

    # --- Tags ---

    def test_tag_entities_request(self, request_validator, mock_client):
        from octostar.api.workspace_tags import tag_entities
        from octostar.models.entity import Entity

        kwargs = tag_entities._get_kwargs(
            "test-workspace",
            client=mock_client,
            tag="my-tag",
            json_body=[Entity("entity-1", "Person")],
        )
        assert kwargs["method"] == "post", "tag_entities must use POST"
        assert kwargs["json"] == {
            "entities": [{"entity_id": "entity-1", "entity_type": "Person"}]
        }
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/tags/{os_workspace}/{tag}"
        )
        result.raise_if_invalid()

    def test_delete_tag_from_entities_request(self, request_validator, mock_client):
        from octostar.api.workspace_tags import delete_tag_from_entities
        from octostar.models.entity import Entity

        kwargs = delete_tag_from_entities._get_kwargs(
            "test-workspace",
            "my-tag",
            client=mock_client,
            json_body=[Entity("entity-1", "Person")],
        )
        assert kwargs["method"] == "delete", "delete_tag_from_entities must use DELETE"
        assert kwargs["json"] == {
            "entities": [{"entity_id": "entity-1", "entity_type": "Person"}]
        }
        result = request_validator.validate_request(
            kwargs, expected_path="/api/v1/tags/{os_workspace}/{tag}"
        )
        result.raise_if_invalid()


class TestModelSerialization:
    """Model serialization produces valid JSON structures."""

    def test_upsert_entity_serialization(self):
        from octostar.models import UpsertEntity, UpsertEntityBase

        entity = UpsertEntity(
            entity=UpsertEntityBase(
                os_entity_uid="test-123",
                entity_type="Person",
                entity_label="John Doe",
            )
        )
        serialized = entity.to_dict()
        assert isinstance(serialized, dict)
        assert "entity" in serialized
        assert serialized["entity"]["os_entity_uid"] == "test-123"

    def test_notification_serialization(self):
        from octostar.models import OsNotification

        notification = OsNotification(
            channel="alerts", title="Alert", body="Something happened"
        )
        serialized = notification.to_dict()
        assert isinstance(serialized, dict)
        assert serialized["channel"] == "alerts"


class TestResponseModels:
    """Response models can deserialize expected response structures."""

    def test_whoami_response_deserialization(self):
        from octostar.models import GetWhoamiResponse200

        response_data = {
            "username": "testuser",
            "email": "test@example.com",
            "roles": ["user"],
            "timbr_roles": ["timbr_user"],
            "is_superuser": False,
            "os_jwt": "eyJ...",
            "async_channel": "channel_testuser",
        }
        model = GetWhoamiResponse200.from_dict(response_data)
        assert model.username == "testuser"
        assert model.is_superuser is False


class TestDeprecatedEndpoints:
    """Verify deprecated/migration-pending modules behave correctly."""

    DEPRECATED_MODULES = [
        (mod, name, cls)
        for mod, name, cls in ALL_API_MODULES
        if cls in ("deprecated", "migration_pending")
    ]

    @pytest.mark.parametrize(
        "module_name,endpoint_name,classification",
        DEPRECATED_MODULES,
        ids=[name for _, name, _ in DEPRECATED_MODULES],
    )
    def test_deprecated_module_raises_on_sync(
        self, module_name, endpoint_name, classification
    ):
        """Calling sync() on a deprecated module must raise the appropriate error."""
        from octostar.errors import DeprecatedEndpointError, V1MigrationPendingError

        module = importlib.import_module(module_name)
        expected_error = (
            DeprecatedEndpointError
            if classification == "deprecated"
            else V1MigrationPendingError
        )
        with pytest.raises(expected_error):
            module.sync()

    @pytest.mark.parametrize(
        "module_name,endpoint_name,classification",
        DEPRECATED_MODULES,
        ids=[name for _, name, _ in DEPRECATED_MODULES],
    )
    def test_deprecated_module_has_no_get_kwargs(
        self, module_name, endpoint_name, classification
    ):
        """Deprecated modules must not expose _get_kwargs."""
        module = importlib.import_module(module_name)
        assert not hasattr(module, "_get_kwargs"), (
            f"{module_name} is {classification} but still has _get_kwargs"
        )


class TestBidirectionalCoverage:
    """Ensure SDK and spec don't silently drift apart."""

    def _collect_sdk_targeted_paths(self, mock_client) -> set:
        """Return the set of URL paths that active SDK modules target."""
        sdk_paths = set()
        example_params = get_example_params()

        for module_name, endpoint_name in API_MODULES:
            module = importlib.import_module(module_name)
            get_kwargs = getattr(module, "_get_kwargs")
            sig = inspect.signature(get_kwargs)
            kwargs_to_call = {}

            for param_name, param in sig.parameters.items():
                if param_name == "client":
                    kwargs_to_call["client"] = mock_client
                elif param_name in ("args", "kwargs"):
                    continue
                else:
                    endpoint_key = f"{param_name}:{endpoint_name}"
                    if endpoint_key in example_params:
                        kwargs_to_call[param_name] = example_params[endpoint_key]
                    elif param_name in example_params:
                        kwargs_to_call[param_name] = example_params[param_name]
                    elif param.default is inspect.Parameter.empty:
                        continue

            try:
                result_kwargs = get_kwargs(**kwargs_to_call)
                url = result_kwargs.get("url", "")
                path = urlparse(url).path.rstrip("/")
                sdk_paths.add(path)
            except Exception:
                pass

        return sdk_paths

    def test_spec_routes_covered_by_sdk_or_allowlisted(self, spec_paths, mock_client):
        """Every OpenAPI route must have an SDK endpoint or be in the allowlist."""
        sdk_paths = self._collect_sdk_targeted_paths(mock_client)

        uncovered = []
        for spec_path in spec_paths:
            normalized = spec_path.rstrip("/")
            if normalized in SPEC_ROUTES_WITHOUT_SDK:
                continue
            if spec_path in SPEC_ROUTES_WITHOUT_SDK:
                continue

            spec_parts = normalized.split("/")
            covered = any(
                _paths_match(spec_parts, sdk_path.split("/")) for sdk_path in sdk_paths
            )
            if not covered:
                uncovered.append(spec_path)

        if uncovered:
            pytest.fail(
                f"{len(uncovered)} spec routes not covered by SDK or allowlist:\n"
                + "\n".join(f"  - {p}" for p in sorted(uncovered))
                + "\n\nAdd SDK endpoints or update SPEC_ROUTES_WITHOUT_SDK."
            )

    def test_allowlist_entries_still_in_spec(self, spec_paths):
        """Catch stale allowlist entries — removed spec routes should be cleaned up."""
        stale = []
        for path in SPEC_ROUTES_WITHOUT_SDK:
            if path not in spec_paths:
                stale.append(path)

        if stale:
            pytest.fail(
                f"{len(stale)} allowlist entries no longer in spec:\n"
                + "\n".join(f"  - {p}" for p in sorted(stale))
                + "\n\nRemove from SPEC_ROUTES_WITHOUT_SDK."
            )

    def test_no_sdk_endpoints_target_missing_paths(
        self, request_validator, mock_client
    ):
        """Catch orphaned SDK modules targeting paths not in spec."""
        orphaned = []
        example_params = get_example_params()

        for module_name, endpoint_name in API_MODULES:
            if endpoint_name in KNOWN_MISSING_PATH_ENDPOINTS:
                continue

            try:
                result_kwargs = _build_kwargs_for_endpoint(
                    module_name,
                    endpoint_name,
                    mock_client,
                    example_params,
                    strict=False,
                )
            except Exception:
                continue

            validation = request_validator.validate_request(result_kwargs)
            if not validation.is_valid:
                path_errors = [e for e in validation.errors if "not found" in e.lower()]
                if path_errors:
                    orphaned.append(f"{endpoint_name}: {path_errors[0]}")

        if orphaned:
            pytest.fail(
                f"{len(orphaned)} SDK endpoints target missing spec paths:\n"
                + "\n".join(f"  - {o}" for o in orphaned)
                + "\n\nAdd to KNOWN_MISSING_PATH_ENDPOINTS or fix the SDK."
            )


class TestResponseContracts:
    """Verify SDK _parse_response covers success status codes from spec."""

    @pytest.mark.parametrize("module_name,endpoint_name", API_MODULES)
    def test_parse_response_covers_spec_success_codes(
        self, module_name, endpoint_name, request_validator, mock_client
    ):
        if endpoint_name in KNOWN_MISSING_PATH_ENDPOINTS:
            pytest.xfail(KNOWN_MISSING_PATH_ENDPOINTS[endpoint_name])

        module = importlib.import_module(module_name)
        parse_response = getattr(module, "_parse_response", None)
        if not parse_response:
            pytest.skip(f"{module_name} has no _parse_response")

        try:
            result_kwargs = _build_kwargs_for_endpoint(
                module_name,
                endpoint_name,
                mock_client,
                get_example_params(),
                strict=False,
            )
        except Exception:
            pytest.skip(f"_get_kwargs failed for {module_name}")

        url = result_kwargs.get("url", "")
        method = result_kwargs.get("method", "").lower()
        path = urlparse(url).path

        spec_path, _ = request_validator._match_path(path)
        if not spec_path:
            pytest.skip(f"No spec path for {module_name}")

        path_spec = request_validator.paths.get(spec_path, {})
        operation = path_spec.get(method, {})
        if not operation:
            pytest.skip(f"No operation for {method} {spec_path}")

        spec_responses = operation.get("responses", {})
        success_codes = [code for code in spec_responses if code.startswith("2")]

        source = inspect.getsource(parse_response)
        missing = []
        for code in success_codes:
            status_name = _http_code_to_status_name(code)
            if status_name and status_name not in source:
                missing.append(f"{code} ({status_name})")

        if missing:
            pytest.fail(
                f"{endpoint_name}._parse_response missing success codes: "
                + ", ".join(missing)
            )


class TestAcceptedLifecycleResponses:
    """Deploy and undeploy accept 202 Accepted as well as 200 (TEAM-8348).

    The server moves both operations to 202 in TEAM-8350; the SDK must parse
    the body instead of raising on the new status.
    """

    @pytest.mark.parametrize("status_code", [200, 202])
    @pytest.mark.parametrize(
        "util_module,call_kwargs",
        [
            (
                "octostar.utils.jobs.apps.deploy_app",
                {"workspace_id": "ws-1", "os_entity_uid": "eid-1"},
            ),
            ("octostar.utils.jobs.apps.undeploy_app", {"app_id": "od-c2-ws-eid"}),
        ],
    )
    def test_lifecycle_call_returns_body_on_success_status(
        self, monkeypatch, mock_client, util_module, call_kwargs, status_code
    ):
        import httpx

        body = {"status": "ok", "app_id": "od-c2-ws-eid"}

        def fake_request(**kwargs):
            return httpx.Response(
                status_code, json=body, request=httpx.Request("POST", kwargs["url"])
            )

        monkeypatch.setattr(httpx, "request", fake_request)
        module = importlib.import_module(util_module)

        assert module.sync(client=mock_client, **call_kwargs) == body


class TestDeadModels:
    """Detect orphaned model files."""

    def test_model_files_importable(self):
        """Every .py in models/ should be importable."""
        models_dir = SDK_ROOT / "models"
        if not models_dir.exists():
            pytest.skip("models/ directory not found")

        failures = []
        for py_file in sorted(models_dir.glob("*.py")):
            if py_file.name.startswith("_"):
                continue
            module_name = f"octostar.models.{py_file.stem}"
            try:
                importlib.import_module(module_name)
            except Exception as e:
                failures.append(f"{module_name}: {e}")

        if failures:
            pytest.fail(
                f"{len(failures)} model files failed to import:\n"
                + "\n".join(f"  - {f}" for f in failures[:20])
            )

    def test_models_init_entries_resolve(self):
        """Every import in models/__init__.py should resolve."""
        init_file = SDK_ROOT / "models" / "__init__.py"
        if not init_file.exists():
            pytest.skip("models/__init__.py not found")

        source = init_file.read_text()
        import_pattern = re.compile(r"from\s+\.(\w+)\s+import\s+(\w+)")
        matches = import_pattern.findall(source)

        failures = []
        for module_stem, class_name in matches:
            module_name = f"octostar.models.{module_stem}"
            try:
                mod = importlib.import_module(module_name)
                if not hasattr(mod, class_name):
                    failures.append(f"{module_name}.{class_name}: class not found")
            except Exception as e:
                failures.append(f"{module_name}: import failed ({e})")

        if failures:
            pytest.fail(
                f"{len(failures)} models/__init__.py entries don't resolve:\n"
                + "\n".join(f"  - {f}" for f in failures[:20])
            )

    def test_models_all_entries_importable(self):
        """Every entry in models.__all__ should be importable."""
        try:
            import octostar.models as models_pkg
        except Exception:
            pytest.skip("Cannot import octostar.models")

        all_entries = getattr(models_pkg, "__all__", None)
        if not all_entries:
            pytest.skip("models.__all__ not defined")

        failures = []
        for name in all_entries:
            if not hasattr(models_pkg, name):
                failures.append(name)

        if failures:
            pytest.fail(
                f"{len(failures)} __all__ entries not importable:\n"
                + "\n".join(f"  - {f}" for f in failures[:20])
            )


class TestUtilsApiWiring:
    """Verify the utils → api wiring is intact."""

    @pytest.mark.parametrize(
        "utils_file,api_module",
        UTILS_API_WIRING,
        ids=[f"{u} -> {a}" for u, a in UTILS_API_WIRING],
    )
    def test_utils_imports_expected_api_module(self, utils_file, api_module):
        """Each utils file must import from its expected api module."""
        if utils_file in KNOWN_RAW_API_UTILS:
            pytest.xfail(KNOWN_RAW_API_UTILS[utils_file])

        file_path = SDK_ROOT / utils_file
        if not file_path.exists():
            pytest.fail(f"Utils file not found: {file_path}")

        source = file_path.read_text()
        # Extract the subpackage from "api.X.Y" → check for "api.X" in imports
        api_subpackage = api_module.split(".")[1]  # e.g., "processing"
        assert f"api.{api_subpackage}" in source, (
            f"{utils_file} does not import from {api_module}"
        )

    def test_all_utils_api_imports_are_tracked(self):
        """Meta-test: every utils file importing from api/ must be in UTILS_API_WIRING."""
        tracked_files = {entry[0] for entry in UTILS_API_WIRING}
        utils_dir = SDK_ROOT / "utils"
        if not utils_dir.exists():
            pytest.skip("utils/ directory not found")

        untracked = []
        for py_file in sorted(utils_dir.rglob("*.py")):
            if py_file.name.startswith("_"):
                continue
            relative = str(py_file.relative_to(SDK_ROOT))
            source = py_file.read_text()
            if re.search(r"from\s+\.+api\.", source):
                if relative not in tracked_files:
                    untracked.append(relative)

        if untracked:
            pytest.fail(
                f"{len(untracked)} utils files import from api/ but are not tracked:\n"
                + "\n".join(f"  - {f}" for f in untracked)
                + "\n\nAdd them to UTILS_API_WIRING in test_contracts.py."
            )


class TestApiModulesImport:
    """Module discovery must not hide an import error.

    A module that imports a deleted model would otherwise drop out of every
    contract test without a failure.
    """

    def test_every_api_module_imports(self):
        assert API_IMPORT_ERRORS == [], "\n".join(
            f"{name}: {err}" for name, err in API_IMPORT_ERRORS
        )

    def test_discovery_records_an_import_error(self):
        errors: list = []
        assert import_api_module("octostar.api.no_such_module_x", errors) is None
        assert errors and errors[0][0] == "octostar.api.no_such_module_x"
