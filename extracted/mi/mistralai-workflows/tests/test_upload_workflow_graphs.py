import asyncio
import json
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import httpx
import pytest

from mistralai.workflows.core._dataflow import CONTROL_FLOW_VIEW
from mistralai.workflows.core._graph import build_graph_statically
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.graph_summaries import NodeSummary, SummariseError, SummaryResult
from mistralai.workflows.core.wire_format import AtlasWireFormat
from mistralai.workflows.core.worker import (
    _GRAPH_PAYLOAD_VERSION,
    _GRAPH_SUMMARY_CONCURRENCY,
    _GRAPH_SUMMARY_REQUEST_TIMEOUT_S,
    _request_graph_summaries,
    _summaries_enabled,
    _upload_workflow_graphs,
)
from mistralai.workflows.protocol.v1.workflow import WorkflowRegistrationRef

WF_ID = uuid4()
REG_ID = uuid4()


def _fake_graph(sources: dict[str, str] | None = None) -> AtlasWireFormat:
    return AtlasWireFormat(
        version=_GRAPH_PAYLOAD_VERSION,
        workflow_name="FakeWorkflow",
        nodes=[],
        edges=[],
        files={},
        incomplete=False,
        sources=sources,
    )


FAKE_GRAPH = _fake_graph()

_LEAK_SECRET = "sk-live-do-not-upload"  # noqa: S105

_LEAKY_SOURCE = f"""
from mistralai import workflows

@workflows.activity()
async def fetch() -> dict:
    return {{}}

@workflows.workflow.define(name="FakeWorkflow")
class FakeLeaky:
    @workflows.workflow.entrypoint
    async def run(self) -> dict:
        data = await fetch()
        api_key = "{_LEAK_SECRET}"
        return {{**data, "k": api_key}}
"""


def _leaky_graph() -> AtlasWireFormat:
    """A real analysable graph carrying a secret, not an empty stub.

    An empty-node graph produces no transform nodes, so a leak assertion over it
    passes vacuously — which is how the source leak in transform labels survived.
    """
    return build_graph_statically(_LEAKY_SOURCE, "/tmp/fake_leaky.py", lambda _path: None)[0]


_SUMMARISE_PATH = "mistralai.workflows.core.worker._request_graph_summaries"
_SUMMARY_CONFIG_PATH = "mistralai.workflows.core.worker._summaries_enabled"

_NO_SUMMARIES = patch(_SUMMARISE_PATH, AsyncMock(return_value=SummaryResult(status="ready", summaries={})))
_MOCK_SUMMARY_CONFIG = patch(_SUMMARY_CONFIG_PATH, return_value=True)


def _make_ref(workflow_id=None, registration_id=None) -> WorkflowRegistrationRef:
    return WorkflowRegistrationRef(
        workflow_id=workflow_id or WF_ID,
        workflow_registration_id=registration_id or REG_ID,
    )


def _make_client(status_code: int = 200) -> MagicMock:
    response = httpx.Response(status_code, request=httpx.Request("POST", "http://test"))
    http_client = MagicMock()
    http_client.build_request = MagicMock(
        side_effect=lambda method, url, **kw: httpx.Request(method, url, json=kw.get("json"))
    )
    http_client.send = AsyncMock(return_value=response)

    sdk_config = MagicMock()
    sdk_config.server_url = "http://api.example.com"
    sdk_config.async_client = http_client

    client = MagicMock()
    client.sdk_configuration = sdk_config
    return client


class FakeWorkflow:
    __name__ = "FakeWorkflow"


_workflow_definition = MagicMock(name="FakeWorkflow")
_workflow_definition.name = "FakeWorkflow"
setattr(FakeWorkflow, "__workflows_workflow_def", _workflow_definition)


class TestUploadWorkflowGraphs:
    def test_summaries_require_feature_and_credentials(self) -> None:
        token_provider = MagicMock()

        with (
            patch.object(config.worker.graph, "graph_summarise_enabled", True),
            patch("mistralai.workflows.core.worker.get_token_provider", return_value=token_provider),
        ):
            assert _summaries_enabled()

    async def test_routes_summary_requests_through_domain_endpoint(self) -> None:
        client = _make_client()
        ref = _make_ref()
        summarise = AsyncMock(return_value=SummaryResult(status="ready", summaries={}))

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            patch(_SUMMARISE_PATH, summarise),
            patch(_SUMMARY_CONFIG_PATH, return_value=True),
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        assert summarise.call_args.kwargs["workflow_identifier"] == "FakeWorkflow"
        assert summarise.call_args.kwargs["workflow_registration_id"] == REG_ID
        assert summarise.call_args.kwargs["http_client"] is client.sdk_configuration.async_client

    async def test_domain_request_contains_redacted_summary_input_only(self) -> None:
        graph = _leaky_graph()
        http_client = MagicMock()
        response = httpx.Response(
            200,
            json={"summaries": {}, "workflow_summary": None},
            request=httpx.Request("POST", "http://api.example.com"),
        )
        http_client.send = AsyncMock(return_value=response)
        http_client.build_request.side_effect = lambda method, url, **kwargs: httpx.Request(
            method, url, json=kwargs["json"]
        )

        await _request_graph_summaries(
            base_url="http://api.example.com",
            workflow_identifier="FakeWorkflow",
            workflow_registration_id=REG_ID,
            graph_data=graph,
            extra_nodes=None,
            http_client=http_client,
        )

        sent_request = http_client.send.await_args.args[0]
        assert str(sent_request.url) == (f"http://api.example.com/v1/workflows/FakeWorkflow/graphs/{REG_ID}/summaries")
        assert http_client.build_request.call_args.kwargs["timeout"] == _GRAPH_SUMMARY_REQUEST_TIMEOUT_S
        body = json.loads(sent_request.content)
        assert not {"messages", "model", "user_prompt", "tag", "id_map"} & body.keys()
        assert body["version"] == 1
        assert body["workflow_name"] == "FakeWorkflow"
        assert body["nodes"]
        assert _LEAK_SECRET not in sent_request.content.decode()

    async def test_waits_out_a_rate_limit_window(self) -> None:
        """retry-after reports the limiter's window reset, so at worker startup it is
        close to a full minute. A workspace registering more workflows than the
        per-minute allowance only gets summaries for the rest if that wait is honoured.
        """
        http_client = MagicMock()
        rate_limited = httpx.Response(
            429,
            headers={"retry-after": "60"},
            request=httpx.Request("POST", "http://api.example.com"),
        )
        success = httpx.Response(
            200,
            json={"summaries": {}, "workflow_summary": None},
            request=httpx.Request("POST", "http://api.example.com"),
        )
        http_client.send = AsyncMock(side_effect=[rate_limited, success])
        http_client.build_request.side_effect = lambda method, url, **kwargs: httpx.Request(
            method, url, json=kwargs["json"]
        )

        with patch("mistralai.workflows.core.worker.asyncio.sleep", new_callable=AsyncMock) as sleep:
            result = await _request_graph_summaries(
                base_url="http://api.example.com",
                workflow_identifier="FakeWorkflow",
                workflow_registration_id=REG_ID,
                graph_data=FAKE_GRAPH,
                extra_nodes=None,
                http_client=http_client,
            )

        assert result.status == "ready"
        assert http_client.send.await_count == 2
        sleep.assert_awaited_once_with(60.0)

    async def test_does_not_retry_rate_limit_beyond_short_retry_budget(self) -> None:
        """A reset hours away is the daily limit, not a burst; the summary is dropped."""
        http_client = MagicMock()
        rate_limited = httpx.Response(
            429,
            headers={"retry-after": "86400"},
            request=httpx.Request("POST", "http://api.example.com"),
        )
        http_client.send = AsyncMock(return_value=rate_limited)
        http_client.build_request.side_effect = lambda method, url, **kwargs: httpx.Request(
            method, url, json=kwargs["json"]
        )

        with (
            patch("mistralai.workflows.core.worker.asyncio.sleep", new_callable=AsyncMock) as sleep,
            pytest.raises(httpx.HTTPStatusError),
        ):
            await _request_graph_summaries(
                base_url="http://api.example.com",
                workflow_identifier="FakeWorkflow",
                workflow_registration_id=REG_ID,
                graph_data=FAKE_GRAPH,
                extra_nodes=None,
                http_client=http_client,
            )

        assert http_client.send.await_count == 1
        sleep.assert_not_awaited()

    async def test_retries_transient_summary_failure(self) -> None:
        http_client = MagicMock()
        unavailable = httpx.Response(503, request=httpx.Request("POST", "http://api.example.com"))
        success = httpx.Response(
            200,
            json={"summaries": {}, "workflow_summary": None},
            request=httpx.Request("POST", "http://api.example.com"),
        )
        http_client.send = AsyncMock(side_effect=[unavailable, success])
        http_client.build_request.side_effect = lambda method, url, **kwargs: httpx.Request(
            method, url, json=kwargs["json"]
        )

        with patch("mistralai.workflows.core.worker.asyncio.sleep", new_callable=AsyncMock) as sleep:
            result = await _request_graph_summaries(
                base_url="http://api.example.com",
                workflow_identifier="FakeWorkflow",
                workflow_registration_id=REG_ID,
                graph_data=FAKE_GRAPH,
                extra_nodes=None,
                http_client=http_client,
            )

        assert result.status == "ready"
        assert http_client.send.await_count == 2
        sleep.assert_awaited_once_with(1)

    @pytest.mark.parametrize("status_code", [404, 405])
    async def test_old_server_without_summary_endpoint_disables_summaries(self, status_code: int) -> None:
        http_client = MagicMock()
        http_client.send = AsyncMock(
            return_value=httpx.Response(status_code, request=httpx.Request("POST", "http://api.example.com"))
        )
        http_client.build_request.side_effect = lambda method, url, **kwargs: httpx.Request(
            method, url, json=kwargs["json"]
        )

        result = await _request_graph_summaries(
            base_url="http://api.example.com",
            workflow_identifier="FakeWorkflow",
            workflow_registration_id=REG_ID,
            graph_data=FAKE_GRAPH,
            extra_nodes=None,
            http_client=http_client,
        )

        assert result.status == "disabled"

    async def test_old_server_without_summary_endpoint_still_receives_graph(self) -> None:
        client = _make_client()
        http_client = client.sdk_configuration.async_client
        unavailable = httpx.Response(404, request=httpx.Request("POST", "http://api.example.com"))
        uploaded = httpx.Response(200, request=httpx.Request("POST", "http://api.example.com"))
        http_client.send = AsyncMock(side_effect=[unavailable, uploaded])

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[_make_ref()], classes=[FakeWorkflow], client=client)

        graph_request = http_client.send.await_args_list[1].args[0]
        body = json.loads(graph_request.content)
        assert body["graph_data"] is not None
        assert body["error"] is None

    async def test_posts_correct_body(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        http_client = client.sdk_configuration.async_client
        http_client.send.assert_called_once()
        sent_request: httpx.Request = http_client.send.call_args[0][0]
        assert str(sent_request.url) == "http://api.example.com/v1/workflows/FakeWorkflow/graphs"
        body = json.loads(sent_request.content)
        assert body["workflow_registration_id"] == str(REG_ID)
        assert body["version"] == 3
        assert {key: value for key, value in body["graph_data"].items() if key not in {"view", "views"}} == (
            FAKE_GRAPH.model_dump(by_alias=True, exclude_none=True)
        )
        assert body["error"] is None

    async def test_attributes_summary_usage_to_the_feature(self) -> None:
        client = _make_client()
        ref = _make_ref()
        summarise = AsyncMock(return_value=SummaryResult(status="ready", summaries={}))

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            patch(_SUMMARISE_PATH, summarise),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        assert summarise.await_count == 1

    async def test_posts_control_and_data_flow_views(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        graph_data = json.loads(sent_request.content)["graph_data"]

        # The control-flow view stays at the top level for clients that predate
        # `views`, and `views` holds only the extra renderings — never a second
        # copy of the control-flow graph.
        assert graph_data["view"] == CONTROL_FLOW_VIEW
        assert [view["view"] for view in graph_data["views"]] == ["Data flow"]

    async def test_no_workflow_source_reaches_the_graphs_api(self) -> None:
        """Sources feed the analyser but must never leave the worker.

        The data-flow analyser needs the source text, so `to_dict` is called with
        `include_sources=True`. Uploading that would ship the workflow's source —
        and any secret written as a literal in it — to the graphs API.
        """
        client = _make_client()
        ref = _make_ref()
        graph = _leaky_graph()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=graph),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        raw_body = sent_request.content.decode()
        graph_data = json.loads(raw_body)["graph_data"]

        dataflow = next(v for v in graph_data["views"] if v["view"] == "Data flow")
        transforms = [n for n in dataflow["nodes"] if n["type"] == "transform"]
        assert transforms, "fixture produced no transform nodes — the leak assertion below would be vacuous"

        assert "sources" not in graph_data
        for view in graph_data["views"]:
            assert "sources" not in view, f"{view['view']} view still carries sources"
        assert _LEAK_SECRET not in raw_body

    async def test_dataflow_views_disabled_uploads_legacy_control_flow_only(self) -> None:
        """The kill-switch restores the pre-data-flow payload exactly."""
        client = _make_client()
        ref = _make_ref()
        graph = _fake_graph()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=graph),
            patch.object(config.worker.graph, "dataflow_views_enabled", False),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        graph_data = json.loads(sent_request.content)["graph_data"]
        assert "views" not in graph_data
        assert "sources" not in graph_data
        assert graph_data == graph.to_dict()

    async def test_build_graph_failure_uploads_error_record(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with patch("mistralai.workflows.core._graph.build_graph_dynamically", side_effect=RuntimeError("parse failed")):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        http_client = client.sdk_configuration.async_client
        http_client.send.assert_called_once()
        sent_request: httpx.Request = http_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert body["graph_data"] is None
        assert "parse failed" in body["error"]

    async def test_http_failure_is_swallowed(self) -> None:
        client = _make_client(status_code=500)
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        client.sdk_configuration.async_client.send.assert_called_once()

    async def test_empty_refs_is_noop(self) -> None:
        client = _make_client()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH) as mock_build,
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[], classes=[], client=client)

        mock_build.assert_not_called()
        client.sdk_configuration.async_client.send.assert_not_called()

    async def test_posts_once_per_workflow(self) -> None:
        client = _make_client()
        refs = [_make_ref(uuid4(), uuid4()), _make_ref(uuid4(), uuid4())]
        classes = [FakeWorkflow, FakeWorkflow]

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        assert client.sdk_configuration.async_client.send.call_count == 2

    async def test_bounds_concurrent_summary_requests(self) -> None:
        client = _make_client()
        refs = [_make_ref(uuid4(), uuid4()) for _ in range(_GRAPH_SUMMARY_CONCURRENCY * 2)]
        classes = [FakeWorkflow] * len(refs)
        active = 0
        peak = 0

        async def summarise(**kwargs):
            nonlocal active, peak
            active += 1
            peak = max(peak, active)
            await asyncio.sleep(0.01)
            active -= 1
            return SummaryResult(status="ready", summaries={})

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            patch(_SUMMARISE_PATH, side_effect=summarise),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        assert peak == _GRAPH_SUMMARY_CONCURRENCY

    async def test_summary_queue_has_one_shared_deadline_per_workflow(self) -> None:
        client = _make_client()
        refs = [_make_ref(uuid4(), uuid4()) for _ in range(_GRAPH_SUMMARY_CONCURRENCY * 2)]
        classes = [FakeWorkflow] * len(refs)

        async def summarise(**kwargs):
            await asyncio.sleep(1)

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            patch(_SUMMARISE_PATH, side_effect=summarise),
            patch("mistralai.workflows.core.worker._GRAPH_SUMMARY_LIFECYCLE_TIMEOUT_S", 0.01),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        assert client.sdk_configuration.async_client.send.await_count == len(refs)

    async def test_queued_workflows_are_not_charged_for_the_wait_for_a_slot(self) -> None:
        """The deadline starts when the concurrency slot is acquired.

        Counted from submission instead, every workflow queued behind more waves than
        the budget covers is cancelled while still waiting, without ever having sent a
        summary request.
        """
        client = _make_client()
        refs = [_make_ref(uuid4(), uuid4()) for _ in range(_GRAPH_SUMMARY_CONCURRENCY * 3)]
        classes = [FakeWorkflow] * len(refs)

        async def summarise(**kwargs):
            await asyncio.sleep(0.05)
            return SummaryResult(status="ready", summaries={"step_a": NodeSummary(short="s", long="l")})

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", side_effect=lambda cls: _fake_graph()),
            patch(_SUMMARISE_PATH, side_effect=summarise),
            # Room for one summary but not for the three waves ahead of the last one.
            patch("mistralai.workflows.core.worker._GRAPH_SUMMARY_LIFECYCLE_TIMEOUT_S", 0.1),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        bodies = [
            json.loads(call.args[0].content) for call in client.sdk_configuration.async_client.send.await_args_list
        ]
        assert len(bodies) == len(refs)
        assert all(body["graph_data"]["node_summaries"] for body in bodies)

    async def test_summary_failure_does_not_embed_exception_message_in_graph_payload(self) -> None:
        client = _make_client()
        secret_url = "https://api.example.com/private?token=secret"

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            patch(_SUMMARISE_PATH, AsyncMock(side_effect=RuntimeError(secret_url))),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[_make_ref()], classes=[FakeWorkflow], client=client)

        request = client.sdk_configuration.async_client.send.await_args.args[0]
        body = json.loads(request.content)
        assert body["error"] == "Graph summary generation failed (RuntimeError)"
        assert secret_url not in request.content.decode()

    async def test_fewer_refs_than_classes_sends_only_matched(self) -> None:
        client = _make_client()
        refs = [_make_ref()]
        classes = [FakeWorkflow, FakeWorkflow]

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        assert client.sdk_configuration.async_client.send.call_count == 1

    async def test_summaries_embedded_in_graph_data(self) -> None:
        client = _make_client()
        ref = _make_ref()
        mock_summaries = {"step_a": NodeSummary(short="fetch data", long="Fetches data from the API.")}

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            patch(_SUMMARISE_PATH, AsyncMock(return_value=SummaryResult(status="ready", summaries=mock_summaries))),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert body["graph_data"]["node_summaries"] == {
            "step_a": {"short": "fetch data", "long": "Fetches data from the API."}
        }
        assert body["graph_data"]["version"] == _GRAPH_PAYLOAD_VERSION

    async def test_workflow_summary_embedded_in_graph_data(self) -> None:
        client = _make_client()
        ref = _make_ref()
        result = SummaryResult(
            status="ready",
            summaries={},
            workflow_summary=NodeSummary(short="Data ingestion run", long="Pulls data and stores it."),
        )

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            patch(_SUMMARISE_PATH, AsyncMock(return_value=result)),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert body["graph_data"]["workflow_summary"] == {
            "short": "Data ingestion run",
            "long": "Pulls data and stores it.",
        }

    async def test_workflow_summary_absent_when_not_generated(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            _NO_SUMMARIES,
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert "workflow_summary" not in body["graph_data"]

    async def test_summary_failure_still_uploads_graph_with_error(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            patch(
                _SUMMARISE_PATH,
                AsyncMock(side_effect=SummariseError("LLM down")),
            ),
            _MOCK_SUMMARY_CONFIG,
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert body["graph_data"] is not None
        assert "node_summaries" not in body["graph_data"]
        assert body["error"] == "Graph summary generation failed (SummariseError)"

    async def test_summaries_skipped_when_client_none(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            patch(_SUMMARISE_PATH) as mock_summarise,
            patch(_SUMMARY_CONFIG_PATH, return_value=None),
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        mock_summarise.assert_not_called()
        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert body["graph_data"] is not None
        assert body["error"] is None
