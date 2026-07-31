"""Integration tests for ConnectorAuthInterceptor with Temporal test environment.

Verifies the full interceptor flow: activity resolution,
auth preflight with Task events, timeout handling, and multi-connector scenarios.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

import pytest
from mistralai.client.models import CredentialsResponse, PublicAuthenticationMethod
from pydantic import BaseModel
from pydantic_core import to_json
from temporalio.client import WorkflowFailureError
from temporalio.converter import DataConverter
from temporalio.testing import WorkflowEnvironment
from temporalio.worker import Worker
from temporalio.worker.workflow_sandbox import SandboxedWorkflowRunner

from mistralai.workflows import workflow
from mistralai.workflows.core._events.event_activities import (
    _emit_task_completed,
    _emit_task_failed,
    _emit_task_in_progress,
    _emit_task_started,
)
from mistralai.workflows.core._events.event_context import EventContext
from mistralai.workflows.core._events.event_interceptor import EventInterceptor
from mistralai.workflows.core.activity import activity
from mistralai.workflows.core.sandbox import get_sandbox_restrictions
from mistralai.workflows.core.temporal.context_handler_interceptor import (
    ContextHandlerInterceptor,
    define_context,
    retrieve_context,
)
from mistralai.workflows.core.temporal.payload_converter import MistralWorkflowsPayloadConverter
from mistralai.workflows.models import PayloadWithContext, WorkflowContext
from mistralai.workflows.plugins.mistralai.connectors import (
    ConnectorAuthInterceptor,
    ConnectorError,
    connector,
    uses_connectors,
)
from mistralai.workflows.plugins.mistralai.connectors.constants import (
    CONNECTORS_KEY,
    MISTRALAI_PLUGIN_KEY,
    RESOLVED_CONNECTORS_KEY,
)
from mistralai.workflows.plugins.mistralai.connectors.event_activities import (
    _emit_connector_auth_completed,
    _emit_connector_auth_failed,
    _emit_connector_auth_started,
)
from mistralai.workflows.plugins.mistralai.connectors.interceptor import ConnectorAuthWorkflowInboundInterceptor
from mistralai.workflows.plugins.mistralai.connectors.models import (
    ConnectorExtensionBinding,
    ResolvedConnector,
    resolved_connector_bindings_from_extension,
)
from mistralai.workflows.plugins.mistralai.connectors.run_as import ConnectorRunAs
from mistralai.workflows.testing import (
    create_capturing_mock_events_client,
    create_test_worker,
)

# ---------------------------------------------------------------------------
# Configurable credential/auth-method state for fake activities
# ---------------------------------------------------------------------------

_fake_user_credentials: dict[str, dict[str, Any]] = {}
_fake_auth_methods: dict[str, list[dict[str, Any]]] = {}
_fake_list_tools_results: dict[str, bool] = {}
_fake_mcp_app_resource_uris: dict[str, dict[str, str]] = {}
_fake_poll_credentials: dict[str, dict[str, Any]] = {}
_creds_call_count: dict[str, int] = {}
_list_tools_calls: list[tuple[str, str | None]] = []
_mcp_app_resource_uri_calls: list[tuple[str, str | None]] = []


def _reset_fake_state() -> None:
    _fake_user_credentials.clear()
    _fake_auth_methods.clear()
    _fake_list_tools_results.clear()
    _fake_mcp_app_resource_uris.clear()
    _fake_poll_credentials.clear()
    _creds_call_count.clear()
    _list_tools_calls.clear()
    _mcp_app_resource_uri_calls.clear()


@activity(name="__internal__connector_resolve", _allow_reserved_name=True, _skip_registering=True)
async def fake_connector_resolve(connector_id_or_name: str, run_as: str = "auto") -> ResolvedConnector:
    return ResolvedConnector(id=f"conn-{connector_id_or_name}", name=connector_id_or_name, description="")


@activity(name="__internal__connector_get_auth_url", _allow_reserved_name=True, _skip_registering=True)
async def fake_connector_get_auth_url(
    connector_id_or_name: str, credentials_name: str | None = None, run_as: str = "auto"
) -> str:
    url = f"https://auth.example.com/{connector_id_or_name}"
    if credentials_name is not None:
        url = f"{url}?credentials_name={credentials_name}"
    return url


@activity(name="__internal__connector_list_user_credentials", _allow_reserved_name=True, _skip_registering=True)
async def fake_connector_list_user_credentials(connector_id_or_name: str, run_as: str = "auto") -> CredentialsResponse:
    _creds_call_count[connector_id_or_name] = _creds_call_count.get(connector_id_or_name, 0) + 1
    if _creds_call_count[connector_id_or_name] > 1 and connector_id_or_name in _fake_poll_credentials:
        return CredentialsResponse.model_validate(_fake_poll_credentials[connector_id_or_name])
    data = _fake_user_credentials.get(
        connector_id_or_name,
        {"credentials": [], "connector_preset_credentials_for_auth": []},
    )
    return CredentialsResponse.model_validate(data)


@activity(name="__internal__connector_get_auth_methods", _allow_reserved_name=True, _skip_registering=True)
async def fake_connector_get_auth_methods(
    connector_id_or_name: str, run_as: str = "auto"
) -> list[PublicAuthenticationMethod]:
    data = _fake_auth_methods.get(
        connector_id_or_name, [{"method_type": "oauth2", "headers": None, "has_default_credentials": False}]
    )
    return [PublicAuthenticationMethod.model_validate(m) for m in data]


@activity(name="__internal__connector_list_tools", _allow_reserved_name=True, _skip_registering=True)
async def fake_connector_list_tools(
    connector_id_or_name: str, credentials_name: str | None = None, run_as: str = "auto"
) -> bool:
    _list_tools_calls.append((connector_id_or_name, credentials_name))
    return _fake_list_tools_results.get(connector_id_or_name, True)


@activity(name="__internal__connector_get_mcp_app_resource_uris", _allow_reserved_name=True, _skip_registering=True)
async def fake_connector_get_mcp_app_resource_uris(
    connector_id_or_name: str,
    credentials_name: str | None = None,
    raise_on_error: bool = False,
    run_as: str = "auto",
) -> dict[str, str]:
    _mcp_app_resource_uri_calls.append((connector_id_or_name, credentials_name))
    return _fake_mcp_app_resource_uris.get(connector_id_or_name, {})


@activity(
    name="__internal__connector_wait_for_credentials",
    _allow_reserved_name=True,
    _skip_registering=True,
    heartbeat_timeout=None,
)
async def fake_connector_wait_for_credentials(
    connector_id: str, credentials_name: str | None = None, run_as: str = "auto"
) -> bool:
    """Fake polling activity: returns True if poll credentials are configured.

    When credentials_name is provided, verifies that the specific named credential
    is present in the poll results (mirroring the real activity's list_tools verification).
    """
    poll_data = _fake_poll_credentials.get(connector_id)
    if not poll_data:
        return False
    credentials = poll_data.get("credentials", [])
    if not credentials:
        return False
    if credentials_name is not None:
        return any(c.get("name") == credentials_name for c in credentials)
    return True


EXTRA_TASK_EVENT_ACTIVITIES = [_emit_task_started, _emit_task_in_progress, _emit_task_completed, _emit_task_failed]
CONNECTOR_AUTH_EVENT_ACTIVITIES = [
    _emit_connector_auth_started,
    _emit_connector_auth_completed,
    _emit_connector_auth_failed,
]

CONNECTOR_ACTIVITIES = [
    fake_connector_resolve,
    fake_connector_get_auth_url,
    fake_connector_list_user_credentials,
    fake_connector_get_auth_methods,
    fake_connector_list_tools,
    fake_connector_get_mcp_app_resource_uris,
    fake_connector_wait_for_credentials,
    *EXTRA_TASK_EVENT_ACTIVITIES,
    *CONNECTOR_AUTH_EVENT_ACTIVITIES,
]

# ---------------------------------------------------------------------------
# Test workflow definitions
# ---------------------------------------------------------------------------

slack = connector("slack")
github = connector("github")
manual_auth = connector("manual", auto_auth=False)
manual_mcp_auth = connector("manual-mcp", auto_auth=False, allow_mcp_ui=True)
api_key_conn = connector("apikey")
bearer_with_creds = connector("bearer-svc", credentials_name="my-bearer-token")
slack_mcp = connector("slack", allow_mcp_ui=True)
mcp_app_conn = connector("mcp-apps", allow_mcp_ui=True)


@workflow.define(name="test-single-connector-wf")
@uses_connectors(slack)
class SingleConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "single-done"


@workflow.define(name="test-multi-connector-wf")
@uses_connectors(slack, github)
class MultiConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "multi-done"


@workflow.define(name="test-obo-multi-connector-wf", on_behalf_of=True)
@uses_connectors(slack, github)
class OboMultiConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "obo-multi-done"


@workflow.define(name="test-no-connector-wf")
class NoConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "no-connector-done"


@workflow.define(name="test-no-connector-tool-call-wf")
class NoConnectorToolCallWorkflow:
    """A workflow with no @uses_connectors that builds a ToolCallClient directly.

    Used to prove a caller-forged resolved_connectors binding is inert: the inbound
    interceptor strips trusted_extensions from caller input, so ToolCallClient finds
    no resolved binding and raises ConnectorError instead of honouring the forge.
    """

    @workflow.entrypoint
    async def run(self) -> str:
        from mistralai.workflows.plugins.mistralai.connectors.client import ToolCallClient

        client = ToolCallClient("github")
        await client.call_tool("create_issue", {"title": "bug"})
        return "should-not-reach"


class _CanIteration(BaseModel):
    iteration: int = 0


@workflow.define(name="test-can-connector-wf")
@uses_connectors(slack)
class ContinueAsNewConnectorWorkflow:
    @workflow.entrypoint
    async def run(self, params: _CanIteration) -> str:
        if params.iteration == 0:
            workflow.continue_as_new(_CanIteration(iteration=1))
        return "continued-done"


@workflow.define(name="test-manual-auth-wf")
@uses_connectors(manual_auth)
class ManualAuthWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "manual-done"


@workflow.define(name="test-manual-mcp-auth-wf")
@uses_connectors(manual_mcp_auth)
class ManualMcpAuthWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "manual-mcp-done"


@workflow.define(name="test-api-key-wf")
@uses_connectors(api_key_conn)
class ApiKeyWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "apikey-done"


@workflow.define(name="test-mixed-connectors-wf")
@uses_connectors(slack, manual_auth, api_key_conn)
class MixedConnectorsWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "mixed-done"


@workflow.define(name="test-bearer-creds-wf")
@uses_connectors(bearer_with_creds)
class BearerWithCredsWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "bearer-done"


@workflow.define(name="test-oauth2-with-existing-creds-wf")
@uses_connectors(slack)
class OAuth2WithExistingCredsWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "oauth2-existing-done"


@workflow.define(name="test-mcp-connector-wf")
@uses_connectors(slack_mcp)
class McpConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "mcp-done"


@workflow.define(name="test-mcp-app-connector-wf")
@uses_connectors(mcp_app_conn)
class McpAppConnectorWorkflow:
    @workflow.entrypoint
    async def run(self) -> dict[str, Any]:
        ctx = retrieve_context()
        if ctx is None:
            return {}
        return ctx.trusted_extensions.get(MISTRALAI_PLUGIN_KEY, {}).get(RESOLVED_CONNECTORS_KEY, {})


@workflow.define(name="test-preset-creds-wf")
@uses_connectors(slack)
class PresetCredsWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "preset-done"


@workflow.define(name="test-bearer-no-oauth2-wf")
@uses_connectors(connector("bearer-only"))
class BearerOnlyNoCredsWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "bearer-only-done"


@workflow.define(name="test-single-github-connector-wf")
@uses_connectors(github)
class SingleConnectorGithubWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "github-done"


@workflow.define(name="test-obo-single-github-connector-wf", on_behalf_of=True)
@uses_connectors(github)
class OboSingleConnectorGithubWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "obo-github-done"


@workflow.define(name="test-worker-identity-wf", on_behalf_of=True)
@uses_connectors(connector("worker-svc", run_as="deployment"))
class WorkerIdentityWorkflow:
    @workflow.entrypoint
    async def run(self) -> str:
        return "worker-done"


def _filter_connector_auth_events(events: list[Any]) -> list[Any]:
    """Filter captured events to only connector_auth CustomTask events."""
    return [
        e
        for e in events
        if hasattr(e, "event_type")
        and hasattr(e, "attributes")
        and getattr(e.attributes, "custom_task_type", None) == "connector_auth"
    ]


def _unwrap_result(result: Any) -> Any:
    if isinstance(result, PayloadWithContext):
        result = result.payload
    if isinstance(result, dict) and "result" in result:
        return result["result"]
    return result


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestConnectorInterceptorIntegration:
    @pytest.mark.asyncio
    async def test_no_connector_workflow_passes_through(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        interceptor = ConnectorAuthInterceptor(workflows=[NoConnectorWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[NoConnectorWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-no-connector-wf",
                id="test-no-conn-passthrough",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "no-connector-done"

    @pytest.mark.asyncio
    async def test_auto_auth_connector_completes_after_poll(self, temporal_env: WorkflowEnvironment) -> None:
        """Polling detects credentials after user completes OAuth."""
        _reset_fake_state()
        _fake_poll_credentials["conn-slack"] = {
            "credentials": [
                {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[SingleConnectorWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with create_test_worker(
                temporal_env,
                workflows=[SingleConnectorWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-single-connector-wf",
                    id="test-auto-auth-poll",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "single-done"

        # Verify CustomTask events were published to the event stream
        connector_events = _filter_connector_auth_events(captured_events)
        started = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_STARTED"]
        completed = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_COMPLETED"]
        assert len(started) == 1, f"Expected 1 started event, got {len(started)}"
        assert len(completed) == 1, f"Expected 1 completed event, got {len(completed)}"
        assert started[0].attributes.payload.value["connector_name"] == "slack"
        assert started[0].attributes.payload.value["connector_id"] == "conn-slack"
        assert started[0].attributes.payload.value["auth_url"] == "https://auth.example.com/conn-slack"
        assert started[0].attributes.custom_task_id == completed[0].attributes.custom_task_id

    @pytest.mark.asyncio
    async def test_manual_auth_skips_preflight(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        interceptor = ConnectorAuthInterceptor(workflows=[ManualAuthWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[ManualAuthWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-manual-auth-wf",
                id="test-manual-auth-skip",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "manual-done"

    @pytest.mark.asyncio
    async def test_manual_auth_with_mcp_ui_skips_preflight(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_mcp_app_resource_uris["conn-manual-mcp"] = {"debug-tool": "ui://debug/app"}
        interceptor = ConnectorAuthInterceptor(workflows=[ManualMcpAuthWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[ManualMcpAuthWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-manual-mcp-auth-wf",
                id="test-manual-mcp-auth-skip",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "manual-mcp-done"

        assert "conn-manual-mcp" not in _creds_call_count
        assert ("conn-manual-mcp", None) not in _list_tools_calls
        assert ("conn-manual-mcp", None) not in _mcp_app_resource_uri_calls

    @pytest.mark.asyncio
    async def test_non_oauth2_connector_skips_preflight(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_auth_methods["conn-apikey"] = [{"method_type": "none", "headers": None, "has_default_credentials": False}]
        interceptor = ConnectorAuthInterceptor(workflows=[ApiKeyWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[ApiKeyWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-api-key-wf",
                id="test-apikey-skip",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "apikey-done"

    @pytest.mark.asyncio
    async def test_multiple_connectors_complete_after_poll(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        for conn_id in ("conn-slack", "conn-github"):
            _fake_poll_credentials[conn_id] = {
                "credentials": [
                    {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
                ],
                "connector_preset_credentials_for_auth": [],
            }
        interceptor = ConnectorAuthInterceptor(workflows=[MultiConnectorWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with create_test_worker(
                temporal_env,
                workflows=[MultiConnectorWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-multi-connector-wf",
                    id="test-multi-conn-poll",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "multi-done"

        # Both connectors should emit started + completed events
        connector_events = _filter_connector_auth_events(captured_events)
        started = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_STARTED"]
        completed = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_COMPLETED"]
        assert len(started) == 2, f"Expected 2 started events, got {len(started)}"
        assert len(completed) == 2, f"Expected 2 completed events, got {len(completed)}"
        connector_names = {e.attributes.payload.value["connector_name"] for e in started}
        assert connector_names == {"slack", "github"}

    @pytest.mark.asyncio
    async def test_mixed_connectors_only_auto_oauth_polls(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_auth_methods["conn-apikey"] = [{"method_type": "none", "headers": None, "has_default_credentials": False}]
        _fake_poll_credentials["conn-slack"] = {
            "credentials": [
                {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[MixedConnectorsWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with create_test_worker(
                temporal_env,
                workflows=[MixedConnectorsWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-mixed-connectors-wf",
                    id="test-mixed-conn",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "mixed-done"

    @pytest.mark.asyncio
    async def test_connector_auth_emits_marker_events(self, temporal_env: WorkflowEnvironment) -> None:
        """Connector auth emits started + completed marker events."""
        _reset_fake_state()
        _fake_poll_credentials["conn-slack"] = {
            "credentials": [
                {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[SingleConnectorWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[SingleConnectorWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-single-connector-wf",
                id="test-auth-marker-events",
                task_queue="test-task-queue",
            )
            await handle.result()
            history = [e async for e in handle.fetch_history_events()]
            # The connector auth markers are recorded as local activities;
            # check for activity-completed events with our marker names.
            activity_types: list[str] = []
            for e in history:
                if e.HasField("activity_task_completed_event_attributes"):
                    # Regular activity completed
                    pass
                if e.HasField("activity_task_scheduled_event_attributes"):
                    activity_types.append(e.activity_task_scheduled_event_attributes.activity_type.name)
                if e.HasField("marker_recorded_event_attributes"):
                    details = e.marker_recorded_event_attributes.details
                    if "data" in details:
                        payloads = details["data"].payloads
                        for p in payloads:
                            decoded = p.data.decode("utf-8", errors="ignore")
                            if "__emit_connector_auth_" in decoded:
                                activity_types.append(decoded.strip().strip('"'))
            has_started = any("__emit_connector_auth_started" in t for t in activity_types)
            has_completed = any("__emit_connector_auth_completed" in t for t in activity_types)
            assert has_started, f"Expected started marker in {activity_types}"
            assert has_completed, f"Expected completed marker in {activity_types}"

    @pytest.mark.asyncio
    async def test_connector_auth_emits_failed_custom_task_on_timeout(self, temporal_env: WorkflowEnvironment) -> None:
        """When polling times out, a CUSTOM_TASK_FAILED event is published."""
        _reset_fake_state()
        # No poll credentials → fake_connector_wait_for_credentials returns False → timeout
        interceptor = ConnectorAuthInterceptor(workflows=[SingleConnectorWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with Worker(
                temporal_env.client,
                task_queue="test-task-queue",
                workflows=[SingleConnectorWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
                workflow_failure_exception_types=[Exception],
                workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-single-connector-wf",
                    id="test-auth-timeout-events",
                    task_queue="test-task-queue",
                )
                with pytest.raises(WorkflowFailureError):
                    await handle.result()

        connector_events = _filter_connector_auth_events(captured_events)
        started = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_STARTED"]
        failed = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_FAILED"]
        assert len(started) == 1, f"Expected 1 started event, got {len(started)}"
        assert len(failed) == 1, f"Expected 1 failed event, got {len(failed)}"
        assert "timed out" in failed[0].attributes.failure.message
        assert started[0].attributes.custom_task_id == failed[0].attributes.custom_task_id

    @pytest.mark.asyncio
    async def test_bearer_credentials_set_skips_oauth(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_auth_methods["conn-bearer-svc"] = [
            {"method_type": "oauth2", "headers": None, "has_default_credentials": False},
            {"method_type": "bearer", "headers": None, "has_default_credentials": False},
        ]
        interceptor = ConnectorAuthInterceptor(workflows=[BearerWithCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[BearerWithCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-bearer-creds-wf",
                id="test-bearer-skip-oauth",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "bearer-done"

    @pytest.mark.asyncio
    async def test_existing_valid_credentials_skip_auth(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-slack"] = {
            "credentials": [
                {"name": "my-oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-slack"] = True
        interceptor = ConnectorAuthInterceptor(workflows=[OAuth2WithExistingCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[OAuth2WithExistingCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-oauth2-with-existing-creds-wf",
                id="test-existing-creds-skip",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "oauth2-existing-done"

    @pytest.mark.asyncio
    async def test_reuses_mcp_app_discovery_as_tool_check(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-slack"] = {
            "credentials": [
                {"name": "my-oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-slack"] = True
        _fake_mcp_app_resource_uris["conn-slack"] = {"debug-tool": "ui://debug/app"}
        interceptor = ConnectorAuthInterceptor(workflows=[McpConnectorWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[McpConnectorWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-mcp-connector-wf",
                id="test-mcp-discovery-as-tool-check",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "mcp-done"

        assert _creds_call_count["conn-slack"] == 1
        assert _list_tools_calls.count(("conn-slack", None)) == 0
        assert _mcp_app_resource_uri_calls.count(("conn-slack", None)) == 1

    @pytest.mark.asyncio
    async def test_mcp_app_connector_resource_uris_are_stored_on_binding(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-mcp-apps"] = {
            "credentials": [
                {"name": "my-oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_mcp_app_resource_uris["conn-mcp-apps"] = {
            "debug-tool": "ui://debug/app",
        }
        connector_interceptor = ConnectorAuthInterceptor(workflows=[McpAppConnectorWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        original_client = temporal_env.client
        temporal_env._client = custom_client  # type: ignore[attr-defined]
        try:
            async with create_test_worker(
                temporal_env,
                workflows=[McpAppConnectorWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            ):
                handle = await custom_client.start_workflow(
                    "test-mcp-app-connector-wf",
                    id="test-mcp-app-connector-resource-uris",
                    task_queue="test-task-queue",
                )
                connectors_context = _unwrap_result(await handle.result())
        finally:
            temporal_env._client = original_client  # type: ignore[attr-defined]

        assert connectors_context == {
            "bindings": [
                {
                    "connector_name": "mcp-apps",
                    "connector_id": "conn-mcp-apps",
                    "credentials_name": None,
                    "run_as": "auto",
                    "allow_mcp_ui": True,
                    "mcp_ui_resource_uris": {"debug-tool": "ui://debug/app"},
                    "mcp_ui_resource_uris_fetched": True,
                    "status": "ready",
                }
            ]
        }
        assert _mcp_app_resource_uri_calls.count(("conn-mcp-apps", None)) == 1

    @pytest.mark.asyncio
    async def test_existing_credentials_need_reauth(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-slack"] = {
            "credentials": [
                {"name": "my-oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-slack"] = False
        _fake_auth_methods["conn-slack"] = [
            {"method_type": "oauth2", "headers": None, "has_default_credentials": False}
        ]
        _fake_poll_credentials["conn-slack"] = {
            "credentials": [
                {"name": "refreshed-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[OAuth2WithExistingCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[OAuth2WithExistingCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-oauth2-with-existing-creds-wf",
                id="test-existing-creds-reauth",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "oauth2-existing-done"

    @pytest.mark.asyncio
    async def test_preset_oauth2_no_user_creds_requires_auth(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-slack"] = {
            "credentials": [],
            "connector_preset_credentials_for_auth": ["oauth2"],
        }
        _fake_poll_credentials["conn-slack"] = {
            "credentials": [
                {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[PresetCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[PresetCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-preset-creds-wf",
                id="test-preset-creds-needs-auth",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "preset-done"

    @pytest.mark.asyncio
    async def test_bearer_only_no_creds_raises_error(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_auth_methods["conn-bearer-only"] = [
            {"method_type": "bearer", "headers": None, "has_default_credentials": False}
        ]
        interceptor = ConnectorAuthInterceptor(workflows=[BearerOnlyNoCredsWorkflow])
        async with Worker(
            temporal_env.client,
            task_queue="test-task-queue",
            workflows=[BearerOnlyNoCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            handle = await temporal_env.client.start_workflow(
                "test-bearer-no-oauth2-wf",
                id="test-bearer-only-no-prompt",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "requires bearer authentication" in str(exc_info.value.__cause__)

    @pytest.mark.asyncio
    async def test_worker_identity_oauth2_no_creds_raises_without_callback(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        """A worker-identity connector must never emit an OAuth callback URL.

        With oauth2 auth and no worker credentials the interceptor fails fast
        instead of waiting, because the worker has no interactive user to
        complete the flow.
        """
        _reset_fake_state()
        # Default fake auth method is oauth2; no user credentials configured.
        interceptor = ConnectorAuthInterceptor(workflows=[WorkerIdentityWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with Worker(
                temporal_env.client,
                task_queue="test-task-queue",
                workflows=[WorkerIdentityWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
                workflow_failure_exception_types=[Exception],
                workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-worker-identity-wf",
                    id="test-worker-identity-no-callback",
                    task_queue="test-task-queue",
                )
                with pytest.raises(WorkflowFailureError) as exc_info:
                    await handle.result()
                assert "run_as='deployment'" in str(exc_info.value.__cause__)

        # No OAuth callback marker should ever be emitted for a deployment connector.
        connector_events = _filter_connector_auth_events(captured_events)
        started = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_STARTED"]
        assert started == [], f"Expected no connector auth started events, got {started}"

    @pytest.mark.asyncio
    async def test_runtime_extension_credentials_on_worker_identity_rejected(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        """A runtime binding must never override a deployment connector slot."""
        _reset_fake_state()
        _fake_user_credentials["conn-worker-svc"] = {
            "credentials": [
                {"name": "my-token", "authentication_type": "bearer", "scope": "deployment", "is_default": False}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        connector_interceptor = ConnectorAuthInterceptor(workflows=[WorkerIdentityWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        async with Worker(
            custom_client,
            task_queue="test-task-queue",
            workflows=[WorkerIdentityWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            extensions = {
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"credentials_name": "my-token"}]},
                },
            }
            ctx = WorkflowContext(namespace="default", execution_id="ext-worker-creds", extensions=extensions)
            arg = PayloadWithContext(payload=to_json(None), empty=True, context=ctx)
            handle = await custom_client.start_workflow(
                "test-worker-identity-wf",
                arg,
                id="test-ext-worker-creds",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()

        assert "declares run_as='auto' connectors" in str(exc_info.value.__cause__)
        assert ("conn-worker-svc", "my-token") not in _list_tools_calls

    @pytest.mark.asyncio
    async def test_missing_credentials_name_raises_error(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-bearer-svc"] = {
            "credentials": [],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[BearerWithCredsWorkflow])
        async with Worker(
            temporal_env.client,
            task_queue="test-task-queue",
            workflows=[BearerWithCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            handle = await temporal_env.client.start_workflow(
                "test-bearer-creds-wf",
                id="test-missing-cred-raises",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "Credential 'my-bearer-token' not found" in str(exc_info.value.__cause__)

    @pytest.mark.asyncio
    async def test_credentials_exist_but_need_reauth(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-bearer-svc"] = False
        _fake_auth_methods["conn-bearer-svc"] = [
            {"method_type": "oauth2", "headers": None, "has_default_credentials": False}
        ]
        _fake_poll_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[BearerWithCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[BearerWithCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-bearer-creds-wf",
                id="test-creds-need-reauth",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "bearer-done"

    @pytest.mark.asyncio
    async def test_wait_for_credentials_mismatched_name_causes_timeout(self, temporal_env: WorkflowEnvironment) -> None:
        """Poll returns a credential, but not the one requested by credentials_name → auth times out."""
        _reset_fake_state()
        _fake_user_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-bearer-svc"] = False
        _fake_auth_methods["conn-bearer-svc"] = [
            {"method_type": "oauth2", "headers": None, "has_default_credentials": False}
        ]
        # Poll returns a credential, but with a different name than the one requested
        _fake_poll_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "other-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[BearerWithCredsWorkflow])
        async with Worker(
            temporal_env.client,
            task_queue="test-task-queue",
            workflows=[BearerWithCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            handle = await temporal_env.client.start_workflow(
                "test-bearer-creds-wf",
                id="test-mismatched-creds-name-timeout",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "auth timed out" in str(exc_info.value.__cause__)

    @pytest.mark.asyncio
    async def test_list_tools_called_with_credentials_name(self, temporal_env: WorkflowEnvironment) -> None:
        """connector_list_tools receives the correct credentials_name when verifying existing credentials."""
        _reset_fake_state()
        _fake_user_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        # list_tools returns True by default → workflow skips auth
        interceptor = ConnectorAuthInterceptor(workflows=[BearerWithCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[BearerWithCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-bearer-creds-wf",
                id="test-list-tools-creds-name",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "bearer-done"

        assert ("conn-bearer-svc", "my-bearer-token") in _list_tools_calls

    @pytest.mark.asyncio
    async def test_list_tools_called_without_credentials_name(self, temporal_env: WorkflowEnvironment) -> None:
        """connector_list_tools receives credentials_name=None when no named credential is configured."""
        _reset_fake_state()
        _fake_user_credentials["conn-slack"] = {
            "credentials": [
                {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        # list_tools returns True by default → workflow skips auth
        interceptor = ConnectorAuthInterceptor(workflows=[OAuth2WithExistingCredsWorkflow])
        async with create_test_worker(
            temporal_env,
            workflows=[OAuth2WithExistingCredsWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[interceptor, EventInterceptor()],
        ):
            handle = await temporal_env.client.start_workflow(
                "test-oauth2-with-existing-creds-wf",
                id="test-list-tools-no-creds-name",
                task_queue="test-task-queue",
            )
            assert _unwrap_result(await handle.result()) == "oauth2-existing-done"

        assert ("conn-slack", None) in _list_tools_calls

    @pytest.mark.asyncio
    async def test_oauth2_reauth_with_credentials_name_passes_correct_url(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        """credentials_name is forwarded to get_auth_url and appears in the started event."""
        _reset_fake_state()
        _fake_user_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-bearer-svc"] = False
        _fake_auth_methods["conn-bearer-svc"] = [
            {"method_type": "oauth2", "headers": None, "has_default_credentials": False}
        ]
        _fake_poll_credentials["conn-bearer-svc"] = {
            "credentials": [
                {"name": "my-bearer-token", "authentication_type": "bearer", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[BearerWithCredsWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with create_test_worker(
                temporal_env,
                workflows=[BearerWithCredsWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-bearer-creds-wf",
                    id="test-reauth-creds-name-url",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "bearer-done"

        connector_events = _filter_connector_auth_events(captured_events)
        started = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_STARTED"]
        completed = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_COMPLETED"]
        assert len(started) == 1
        assert len(completed) == 1
        assert started[0].attributes.payload.value["credentials_name"] == "my-bearer-token"
        assert (
            started[0].attributes.payload.value["auth_url"]
            == "https://auth.example.com/conn-bearer-svc?credentials_name=my-bearer-token"
        )
        assert completed[0].attributes.payload.value["credentials_name"] == "my-bearer-token"

    @pytest.mark.asyncio
    async def test_oauth2_auth_url_without_credentials_name(self, temporal_env: WorkflowEnvironment) -> None:
        """get_auth_url called without credentials_name produces a clean URL (no query string)."""
        _reset_fake_state()
        _fake_poll_credentials["conn-slack"] = {
            "credentials": [
                {"name": "oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        interceptor = ConnectorAuthInterceptor(workflows=[SingleConnectorWorkflow])
        captured_events: list[Any] = []
        mock_client = create_capturing_mock_events_client(captured_events)
        async with EventContext(mock_client):
            async with create_test_worker(
                temporal_env,
                workflows=[SingleConnectorWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[interceptor, EventInterceptor()],
            ):
                handle = await temporal_env.client.start_workflow(
                    "test-single-connector-wf",
                    id="test-auth-url-no-creds-name",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "single-done"

        connector_events = _filter_connector_auth_events(captured_events)
        started = [e for e in connector_events if e.event_type.value == "CUSTOM_TASK_STARTED"]
        assert len(started) == 1
        assert started[0].attributes.payload.value["auth_url"] == "https://auth.example.com/conn-slack"
        assert "credentials_name" not in started[0].attributes.payload.value

    @pytest.mark.asyncio
    async def test_runtime_extension_credentials_name_skips_auth(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-github"] = {
            "credentials": [{"name": "my-pat", "authentication_type": "bearer", "scope": "user", "is_default": False}],
            "connector_preset_credentials_for_auth": [],
        }
        connector_interceptor = ConnectorAuthInterceptor(workflows=[OboSingleConnectorGithubWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        original_client = temporal_env.client
        temporal_env._client = custom_client  # type: ignore[attr-defined]
        try:
            async with create_test_worker(
                temporal_env,
                workflows=[OboSingleConnectorGithubWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            ):
                extensions = {
                    MISTRALAI_PLUGIN_KEY: {
                        CONNECTORS_KEY: {"bindings": [{"credentials_name": "my-pat"}]},
                    },
                }
                ctx = WorkflowContext(namespace="default", execution_id="ext-creds-test", extensions=extensions)
                arg = PayloadWithContext(payload=to_json(None), empty=True, context=ctx)
                handle = await custom_client.start_workflow(
                    "test-obo-single-github-connector-wf",
                    arg,
                    id="test-ext-creds-skip-auth",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "obo-github-done"
        finally:
            temporal_env._client = original_client  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_runtime_extension_credentials_name_can_target_multiple_obo_auto_connectors(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-github"] = {
            "credentials": [
                {"name": "github-pat", "authentication_type": "bearer", "scope": "user", "is_default": False}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_user_credentials["conn-slack"] = {
            "credentials": [
                {"name": "slack-token", "authentication_type": "bearer", "scope": "user", "is_default": False}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        connector_interceptor = ConnectorAuthInterceptor(workflows=[OboMultiConnectorWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        original_client = temporal_env.client
        temporal_env._client = custom_client  # type: ignore[attr-defined]
        try:
            async with create_test_worker(
                temporal_env,
                workflows=[OboMultiConnectorWorkflow],
                activities=CONNECTOR_ACTIVITIES,
                interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            ):
                extensions = {
                    MISTRALAI_PLUGIN_KEY: {
                        CONNECTORS_KEY: {
                            "bindings": [
                                {"connector_name": "github", "credentials_name": "github-pat"},
                                {"connector_name": "slack", "credentials_name": "slack-token"},
                            ]
                        },
                    },
                }
                ctx = WorkflowContext(namespace="default", execution_id="ext-multi-creds-test", extensions=extensions)
                arg = PayloadWithContext(payload=to_json(None), empty=True, context=ctx)
                handle = await custom_client.start_workflow(
                    "test-obo-multi-connector-wf",
                    arg,
                    id="test-ext-multi-creds-skip-auth",
                    task_queue="test-task-queue",
                )
                assert _unwrap_result(await handle.result()) == "obo-multi-done"
        finally:
            temporal_env._client = original_client  # type: ignore[attr-defined]

    @pytest.mark.asyncio
    async def test_runtime_extension_credentials_name_rejected_for_non_obo_auto_connector(
        self, temporal_env: WorkflowEnvironment
    ) -> None:
        _reset_fake_state()
        connector_interceptor = ConnectorAuthInterceptor(workflows=[SingleConnectorGithubWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        async with Worker(
            custom_client,
            task_queue="test-task-queue",
            workflows=[SingleConnectorGithubWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            extensions = {
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"credentials_name": "my-pat"}]},
                },
            }
            ctx = WorkflowContext(namespace="default", execution_id="ext-non-obo", extensions=extensions)
            arg = PayloadWithContext(payload=to_json(None), empty=True, context=ctx)
            handle = await custom_client.start_workflow(
                "test-single-github-connector-wf",
                arg,
                id="test-ext-non-obo-rejected",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()

        assert "on_behalf_of=True" in str(exc_info.value.__cause__)


class TestConnectorInterceptorSlotRetrieval:
    def test_metadata_index_built_correctly(self) -> None:
        interceptor = ConnectorAuthInterceptor(
            workflows=[SingleConnectorWorkflow, MultiConnectorWorkflow, NoConnectorWorkflow]
        )
        assert "test-single-connector-wf" in interceptor._metadata_by_name
        assert "test-no-connector-wf" not in interceptor._metadata_by_name

    def test_interceptor_class_carries_metadata(self) -> None:
        interceptor = ConnectorAuthInterceptor(workflows=[SingleConnectorWorkflow])
        cls = interceptor.workflow_interceptor_class(MagicMock())
        assert cls is not None
        assert "test-single-connector-wf" in cls._metadata_by_name

    def test_empty_workflows_produces_empty_index(self) -> None:
        assert ConnectorAuthInterceptor(workflows=[])._metadata_by_name == {}


class TestRunAsCannotBeCallerInjected:
    """run_as is interceptor-owned. A direct ToolCallClient inherits it from the
    persisted binding, so a caller-supplied runtime binding must not be able to carry
    run_as (or other authority fields). Such fields are silently ignored — never
    honoured — so they can never influence the slot's identity."""

    @pytest.mark.parametrize(
        "binding",
        [
            {"credentials_name": "x", "run_as": "deployment"},
            {"credentials_name": "x", "connector_id": "caller-controlled"},
            {"credentials_name": "x", "authentication_name": "caller-controlled"},
        ],
        ids=["run-as", "connector-id", "authentication-name"],
    )
    def test_runtime_binding_ignores_caller_authority_fields(self, binding: dict[str, str]) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="raw-authority-field",
            extensions={MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: {"bindings": [binding]}}},
        )
        slot = connector("github")

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                [slot], bindings, workflow_on_behalf_of=True
            )

        assert len(bindings) == 1
        assert bindings[0].credentials_name == "x"
        # run_as stays interceptor-owned; the caller-supplied field had no effect.
        assert slot.run_as == ConnectorRunAs.AUTO
        assert slot.credentials_name == "x"

    def test_runtime_binding_with_unknown_connector_name_is_rejected(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="raw-connector-name",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"connector_name": "slack", "credentials_name": "x"}]}
                }
            },
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            with pytest.raises(ConnectorError, match="can only target declared run_as='auto' connectors"):
                ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                    [connector("github")], bindings, workflow_on_behalf_of=True
                )

    @pytest.mark.parametrize(
        "extensions",
        [
            {MISTRALAI_PLUGIN_KEY: "bad"},
            {MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: "bad"}},
            {MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: {"bindings": None}}},
        ],
        ids=["mistralai-not-object", "connectors-not-object", "bindings-none"],
    )
    def test_runtime_extension_payload_shape_is_rejected(self, extensions: dict[str, Any]) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="bad-runtime-extension",
            extensions=extensions,
        )

        with define_context(ctx):
            with pytest.raises(ConnectorError, match="Malformed runtime connector extension bindings"):
                ConnectorAuthWorkflowInboundInterceptor._extension_bindings()

    def test_runtime_binding_unknown_top_level_field_is_ignored(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="connectors-extra-field",
            extensions={MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: {"bindings": [], "run_as": "deployment"}}},
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()

        assert bindings == []

    def test_runtime_multiple_bindings_without_connector_name_are_rejected(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="bad-multiple-bindings",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"credentials_name": "x"}, {"credentials_name": "y"}]}
                }
            },
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            with pytest.raises(ConnectorError, match="must include connector_name"):
                ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                    [connector("github"), connector("slack")], bindings, workflow_on_behalf_of=True
                )

    def test_runtime_multiple_bindings_for_multiple_obo_auto_connectors_are_allowed(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="multi-obo-auto",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {
                        "bindings": [
                            {"connector_name": "github", "credentials_name": "x"},
                            {"connector_name": "slack", "credentials_name": "y"},
                        ]
                    }
                }
            },
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                [connector("github"), connector("slack")], bindings, workflow_on_behalf_of=True
            )

        assert [(b.connector_name, b.credentials_name) for b in bindings] == [("github", "x"), ("slack", "y")]

    @pytest.mark.parametrize("credentials_name", ["", "   "], ids=["empty", "whitespace"])
    def test_runtime_binding_rejects_blank_credentials_name(self, credentials_name: str) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="blank-credentials-name",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"connector_name": "github", "credentials_name": credentials_name}]}
                }
            },
        )

        with define_context(ctx):
            with pytest.raises(ConnectorError, match="Malformed runtime connector extension bindings"):
                ConnectorAuthWorkflowInboundInterceptor._extension_bindings()

    def test_runtime_duplicate_connector_binding_is_rejected(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="duplicate-connector-binding",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {
                        "bindings": [
                            {"connector_name": "github", "credentials_name": "x"},
                            {"connector_name": "github", "credentials_name": "y"},
                        ]
                    }
                }
            },
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            with pytest.raises(ConnectorError, match="duplicate binding"):
                ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                    [connector("github"), connector("slack")], bindings, workflow_on_behalf_of=True
                )

    def test_runtime_binding_cannot_target_deployment_connector_when_auto_connector_exists(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="target-deployment-with-auto-present",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"connector_name": "worker-svc", "credentials_name": "x"}]}
                }
            },
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            with pytest.raises(ConnectorError, match="can only target declared run_as='auto' connectors"):
                ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                    [connector("github"), connector("worker-svc", run_as="deployment")],
                    bindings,
                    workflow_on_behalf_of=True,
                )

    def test_runtime_binding_for_deployment_connector_is_rejected(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="deployment-override",
            extensions={MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: {"bindings": [{"credentials_name": "x"}]}}},
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            with pytest.raises(ConnectorError, match="declares run_as='auto' connectors"):
                ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                    [connector("worker-svc", run_as="deployment")], bindings, workflow_on_behalf_of=True
                )

    def test_runtime_binding_for_non_obo_auto_connector_is_rejected(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="non-obo-auto",
            extensions={MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: {"bindings": [{"credentials_name": "x"}]}}},
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            with pytest.raises(ConnectorError, match="on_behalf_of=True"):
                ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                    [connector("github")], bindings, workflow_on_behalf_of=False
                )

    def test_runtime_binding_for_single_obo_auto_connector_is_allowed(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="obo-auto",
            extensions={MISTRALAI_PLUGIN_KEY: {CONNECTORS_KEY: {"bindings": [{"credentials_name": "x"}]}}},
        )

        with define_context(ctx):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()
            ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings(
                [connector("github")], bindings, workflow_on_behalf_of=True
            )

        assert len(bindings) == 1
        assert bindings[0].connector_name is None
        assert bindings[0].credentials_name == "x"


class TestApplyExtensionBindings:
    """A runtime binding carries credentials_name as its only value. A binding
    without one is a selector with nothing to set, so it must leave the slot's
    statically declared credentials_name untouched rather than clearing it."""

    def test_name_only_binding_does_not_wipe_static_credentials_name(self) -> None:
        slot = connector("github", credentials_name="static-token")
        binding = ConnectorExtensionBinding(connector_name="github", credentials_name=None)

        ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings([slot], [binding], workflow_on_behalf_of=True)

        assert slot.credentials_name == "static-token"

    def test_binding_with_credentials_name_overrides_static_value(self) -> None:
        slot = connector("github", credentials_name="static-token")
        binding = ConnectorExtensionBinding(connector_name="github", credentials_name="runtime-token")

        ConnectorAuthWorkflowInboundInterceptor._apply_extension_bindings([slot], [binding], workflow_on_behalf_of=True)

        assert slot.credentials_name == "runtime-token"


class TestResolvedBindingsSeparateChannel:
    """Resolved bindings live in the worker-only ``trusted_extensions`` channel, separate
    from the caller-writable ``extensions``. The runtime binding reader (which parses the
    caller's ``connectors`` input) isn't confused by them, and the resolved reader pulls
    from the trusted channel."""

    @staticmethod
    def _reentry_context() -> WorkflowContext:
        return WorkflowContext(
            namespace="default",
            execution_id="reentry",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"credentials_name": "user-cred"}]},
                }
            },
            trusted_extensions={
                MISTRALAI_PLUGIN_KEY: {
                    RESOLVED_CONNECTORS_KEY: {
                        "bindings": [
                            {
                                "connector_name": "github",
                                "connector_id": "conn-gh",
                                "credentials_name": "user-cred",
                                "run_as": "auto",
                                "allow_mcp_ui": False,
                                "status": "ready",
                            }
                        ]
                    },
                }
            },
        )

    def test_runtime_reader_reads_caller_override(self) -> None:
        with define_context(self._reentry_context()):
            bindings = ConnectorAuthWorkflowInboundInterceptor._extension_bindings()

        assert [b.credentials_name for b in bindings] == ["user-cred"]

    def test_resolved_reader_reads_trusted_channel(self) -> None:
        ctx = self._reentry_context()
        resolved = resolved_connector_bindings_from_extension(ctx.trusted_extensions[MISTRALAI_PLUGIN_KEY])
        assert [b.connector_name for b in resolved] == ["github"]
        assert resolved[0].connector_id == "conn-gh"

    def test_store_resolved_bindings_overwrites_pre_planted_forged(self) -> None:
        """A slotted workflow's interceptor overwrites any pre-planted ``resolved_connectors``
        in ``trusted_extensions``, so a forged binding cannot survive into the reader.
        Documents the invariant that ``_store_resolved_bindings`` defends slotted workflows."""
        ctx = WorkflowContext(
            namespace="default",
            execution_id="clobber",
            trusted_extensions={
                MISTRALAI_PLUGIN_KEY: {
                    RESOLVED_CONNECTORS_KEY: {
                        "bindings": [
                            {
                                "connector_name": "github",
                                "connector_id": "forged",
                                "credentials_name": "attacker",
                                "run_as": "deployment",
                            }
                        ]
                    }
                }
            },
        )
        with define_context(ctx):
            ConnectorAuthWorkflowInboundInterceptor._store_resolved_bindings(
                [{"connector_name": "github", "connector_id": "conn-gh", "status": "ready", "run_as": "auto"}]
            )

            resolved = resolved_connector_bindings_from_extension(
                retrieve_context().trusted_extensions[MISTRALAI_PLUGIN_KEY]
            )
        assert len(resolved) == 1
        assert resolved[0].connector_id == "conn-gh"
        assert resolved[0].credentials_name is None
        assert resolved[0].run_as == ConnectorRunAs.AUTO


class TestNoConnectorWorkflowIgnoresInheritedBindings:
    """A workflow that declares no connectors must not validate connector bindings it
    inherited from a connector parent's propagated extensions. Regression: the runtime
    binding check used to run before the no-slots early return."""

    @pytest.mark.asyncio
    async def test_no_connector_child_ignores_inherited_bindings(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        connector_interceptor = ConnectorAuthInterceptor(workflows=[NoConnectorWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        async with Worker(
            custom_client,
            task_queue="test-task-queue",
            workflows=[NoConnectorWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            extensions = {
                MISTRALAI_PLUGIN_KEY: {
                    CONNECTORS_KEY: {"bindings": [{"credentials_name": "user-cred"}]},
                },
            }
            trusted_extensions = {
                MISTRALAI_PLUGIN_KEY: {
                    RESOLVED_CONNECTORS_KEY: {
                        "bindings": [{"connector_name": "github", "connector_id": "conn-gh", "status": "ready"}]
                    },
                },
            }
            ctx = WorkflowContext(
                namespace="default",
                execution_id="no-connector-inherited",
                extensions=extensions,
                trusted_extensions=trusted_extensions,
            )
            arg = PayloadWithContext(payload=to_json(None), empty=True, context=ctx)
            handle = await custom_client.start_workflow(
                "test-no-connector-wf",
                arg,
                id="test-no-connector-inherited",
                task_queue="test-task-queue",
            )
            result = _unwrap_result(await handle.result())

        assert result == "no-connector-done"

    @pytest.mark.asyncio
    async def test_no_slot_tool_call_client_rejects_forged_binding(self, temporal_env: WorkflowEnvironment) -> None:
        """A no-slot workflow that builds ToolCallClient directly must not honour a
        caller-forged resolved_connectors binding. The inbound interceptor strips
        trusted_extensions from caller input, so the client raises ConnectorError
        rather than using the forged connector_id/credentials_name."""
        _reset_fake_state()
        connector_interceptor = ConnectorAuthInterceptor(workflows=[NoConnectorToolCallWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        async with Worker(
            custom_client,
            task_queue="test-task-queue",
            workflows=[NoConnectorToolCallWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            # Forge both extensions and trusted_extensions — the inbound interceptor
            # drops trusted_extensions, so only extensions survives. ToolCallClient reads
            # trusted_extensions only, so the forge is inert.
            ctx = WorkflowContext(
                namespace="default",
                execution_id="no-connector-forged",
                extensions={
                    MISTRALAI_PLUGIN_KEY: {
                        RESOLVED_CONNECTORS_KEY: {
                            "bindings": [
                                {
                                    "connector_name": "github",
                                    "connector_id": "forged",
                                    "credentials_name": "attacker",
                                    "run_as": "deployment",
                                }
                            ]
                        }
                    }
                },
                trusted_extensions={
                    MISTRALAI_PLUGIN_KEY: {
                        RESOLVED_CONNECTORS_KEY: {
                            "bindings": [
                                {
                                    "connector_name": "github",
                                    "connector_id": "forged",
                                    "credentials_name": "attacker",
                                    "run_as": "deployment",
                                }
                            ]
                        }
                    }
                },
            )
            arg = PayloadWithContext(payload=to_json(None), empty=True, context=ctx)
            handle = await custom_client.start_workflow(
                "test-no-connector-tool-call-wf",
                arg,
                id="test-no-connector-forged",
                task_queue="test-task-queue",
            )
            with pytest.raises(WorkflowFailureError) as exc_info:
                await handle.result()
            assert "uses_connectors" in str(exc_info.value.__cause__)


class TestConnectorWorkflowContinueAsNew:
    """A connector workflow that continues-as-new re-runs preflight on each run.

    Resolved bindings live in the worker-only ``trusted_extensions`` channel, which is not
    propagated across runs, so the continued run resolves connectors from scratch (the
    caller's ``connectors`` input in ``extensions`` still rides along, so credentials_name
    overrides re-apply). The continued run must complete and preflight must run again."""

    @pytest.mark.asyncio
    async def test_preflight_succeeds_after_continue_as_new(self, temporal_env: WorkflowEnvironment) -> None:
        _reset_fake_state()
        _fake_user_credentials["conn-slack"] = {
            "credentials": [
                {"name": "my-oauth-cred", "authentication_type": "oauth2", "scope": "user", "is_default": True}
            ],
            "connector_preset_credentials_for_auth": [],
        }
        _fake_list_tools_results["conn-slack"] = True

        connector_interceptor = ConnectorAuthInterceptor(workflows=[ContinueAsNewConnectorWorkflow])
        dc = DataConverter(payload_converter_class=MistralWorkflowsPayloadConverter)
        custom_client = type(temporal_env.client)(
            temporal_env.client.service_client,
            namespace=temporal_env.client.namespace,
            data_converter=dc,
        )
        async with Worker(
            custom_client,
            task_queue="test-task-queue",
            workflows=[ContinueAsNewConnectorWorkflow],
            activities=CONNECTOR_ACTIVITIES,
            interceptors=[ContextHandlerInterceptor(), connector_interceptor, EventInterceptor()],
            workflow_failure_exception_types=[Exception],
            workflow_runner=SandboxedWorkflowRunner(restrictions=get_sandbox_restrictions()),
        ):
            initial_arg = PayloadWithContext(
                payload=to_json(_CanIteration(iteration=0).model_dump()),
                context=WorkflowContext(namespace="default", execution_id="can-connector"),
            )
            handle = await custom_client.start_workflow(
                "test-can-connector-wf",
                initial_arg,
                id="test-can-connector",
                task_queue="test-task-queue",
            )
            result = _unwrap_result(await handle.result())

        assert result == "continued-done"
        # Preflight ran on both the initial run and the continued run.
        assert _creds_call_count["conn-slack"] == 2


class TestCallerCannotForgeResolvedBindings:
    """Resolved bindings are read only from ``trusted_extensions``; a forged binding in
    the caller-writable ``extensions`` is ignored."""

    def test_forged_extensions_bindings_are_not_read(self) -> None:
        ctx = WorkflowContext(
            namespace="default",
            execution_id="forge-exec",
            extensions={
                MISTRALAI_PLUGIN_KEY: {
                    RESOLVED_CONNECTORS_KEY: {"bindings": [{"connector_name": "github", "connector_id": "forged"}]}
                }
            },
        )
        # The resolved reader targets the trusted channel, which is empty here.
        assert resolved_connector_bindings_from_extension(ctx.trusted_extensions.get(MISTRALAI_PLUGIN_KEY, {})) == []
