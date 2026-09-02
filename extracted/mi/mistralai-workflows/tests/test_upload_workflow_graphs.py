import json
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import httpx

from mistralai.workflows.core._dataflow import CONTROL_FLOW_VIEW
from mistralai.workflows.core._graph import build_graph_statically
from mistralai.workflows.core.config.config import config
from mistralai.workflows.core.graph_summaries import NodeSummary, SummariseError, SummaryResult
from mistralai.workflows.core.wire_format import AtlasWireFormat
from mistralai.workflows.core.worker import _GRAPH_PAYLOAD_VERSION, _upload_workflow_graphs
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


_SUMMARISE_PATH = "mistralai.workflows.core.graph_summaries.summarise_workflow"
_SUMMARY_CONFIG_PATH = "mistralai.workflows.core.worker._get_summary_config"

_NO_SUMMARIES = patch(_SUMMARISE_PATH, AsyncMock(return_value=SummaryResult(status="ready", summaries={})))
_MOCK_SUMMARY_CONFIG = patch(_SUMMARY_CONFIG_PATH, return_value=(MagicMock(), "mistral-small-latest"))


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
        assert "LLM down" in body["error"]

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
