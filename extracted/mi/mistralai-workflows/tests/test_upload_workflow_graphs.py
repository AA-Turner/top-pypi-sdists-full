import json
from unittest.mock import AsyncMock, MagicMock, patch
from uuid import uuid4

import httpx

from mistralai.workflows.core.graph_summaries import NodeSummary, SummariseError, SummaryResult
from mistralai.workflows.core.wire_format import AtlasWireFormat
from mistralai.workflows.core.worker import _GRAPH_PAYLOAD_VERSION, _upload_workflow_graphs
from mistralai.workflows.protocol.v1.workflow import WorkflowRegistrationRef

WF_ID = uuid4()
REG_ID = uuid4()


def _fake_graph() -> AtlasWireFormat:
    return AtlasWireFormat(
        version=_GRAPH_PAYLOAD_VERSION,
        workflow_name="FakeWorkflow",
        nodes=[],
        edges=[],
        files={},
        incomplete=False,
    )


FAKE_GRAPH = _fake_graph()

_SUMMARISE_PATH = "mistralai.workflows.core.graph_summaries.summarise_workflow"

_NO_SUMMARIES = patch(_SUMMARISE_PATH, AsyncMock(return_value=SummaryResult(status="ready", summaries={})))


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


class TestUploadWorkflowGraphs:
    async def test_posts_correct_body(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH), _NO_SUMMARIES:
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        http_client = client.sdk_configuration.async_client
        http_client.send.assert_called_once()
        sent_request: httpx.Request = http_client.send.call_args[0][0]
        assert str(sent_request.url) == f"http://api.example.com/v1/workflows/{WF_ID}/graphs"
        body = json.loads(sent_request.content)
        assert body["workflow_registration_id"] == str(REG_ID)
        assert body["version"] == 3
        assert body["graph_data"] == FAKE_GRAPH.model_dump(by_alias=True, exclude_none=True)
        assert body["error"] is None

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

        with patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH), _NO_SUMMARIES:
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        client.sdk_configuration.async_client.send.assert_called_once()

    async def test_empty_refs_is_noop(self) -> None:
        client = _make_client()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH) as mock_build,
            _NO_SUMMARIES,
        ):
            await _upload_workflow_graphs(refs=[], classes=[], client=client)

        mock_build.assert_not_called()
        client.sdk_configuration.async_client.send.assert_not_called()

    async def test_posts_once_per_workflow(self) -> None:
        client = _make_client()
        refs = [_make_ref(uuid4(), uuid4()), _make_ref(uuid4(), uuid4())]
        classes = [FakeWorkflow, FakeWorkflow]

        with patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH), _NO_SUMMARIES:
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        assert client.sdk_configuration.async_client.send.call_count == 2

    async def test_fewer_refs_than_classes_sends_only_matched(self) -> None:
        # Shouldn't happen (_run_worker guards against it), but _upload_workflow_graphs is safe via zip truncation.
        client = _make_client()
        refs = [_make_ref()]
        classes = [FakeWorkflow, FakeWorkflow]

        with patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=FAKE_GRAPH), _NO_SUMMARIES:
            await _upload_workflow_graphs(refs=refs, classes=classes, client=client)

        assert client.sdk_configuration.async_client.send.call_count == 1

    async def test_summaries_embedded_in_graph_data(self) -> None:
        client = _make_client()
        ref = _make_ref()
        mock_summaries = {"step_a": NodeSummary(short="fetch data", long="Fetches data from the API.")}

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            patch(_SUMMARISE_PATH, AsyncMock(return_value=SummaryResult(status="ready", summaries=mock_summaries))),
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        assert body["graph_data"]["node_summaries"] == {
            "step_a": {"short": "fetch data", "long": "Fetches data from the API."}
        }
        assert body["graph_data"]["version"] == _GRAPH_PAYLOAD_VERSION

    async def test_summary_failure_still_uploads_graph_with_error(self) -> None:
        client = _make_client()
        ref = _make_ref()

        with (
            patch("mistralai.workflows.core._graph.build_graph_dynamically", return_value=_fake_graph()),
            patch(
                _SUMMARISE_PATH,
                AsyncMock(side_effect=SummariseError("LLM down")),
            ),
        ):
            await _upload_workflow_graphs(refs=[ref], classes=[FakeWorkflow], client=client)

        sent_request: httpx.Request = client.sdk_configuration.async_client.send.call_args[0][0]
        body = json.loads(sent_request.content)
        # Build succeeded, so the graph is still uploaded (just without summaries),
        # but the summary error is now surfaced in the payload's error field.
        assert body["graph_data"] is not None
        assert "node_summaries" not in body["graph_data"]
        assert "LLM down" in body["error"]
