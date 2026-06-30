"""Tests for mistralai.workflows.core.graph_summaries."""

import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mistralai.client.errors import MistralError
from pydantic import SecretStr

import mistralai.workflows.core.graph_summaries as _summaries_mod
from mistralai.workflows.core.graph_summaries import (
    SummariseError,
    _bottom_up_order,
    _build_user_message,
    _redact_string_literals,
    _serialize_node,
    summarise_workflow,
)
from mistralai.workflows.core.wire_format import AtlasWireFormat, FileRange, FlatNode, SourceRange


@pytest.fixture(autouse=True)
def _reset_mistral_client():
    """Clear the cached Mistral client between tests."""
    _summaries_mod._get_client.cache_clear()
    yield
    _summaries_mod._get_client.cache_clear()


_SR = SourceRange(begin=0, end=10, line=1)


def _node(id_: str, type_: str = "activity", name: str = "", **kwargs) -> FlatNode:
    return FlatNode(id=id_, type=type_, name=name or id_, source_range=_SR, line=1, **kwargs)


def _wire(*nodes: FlatNode, edges=None, workflow_name="MyWF") -> AtlasWireFormat:
    return AtlasWireFormat(
        workflow_name=workflow_name,
        nodes=list(nodes),
        edges=edges or [],
        files={},
        incomplete=False,
    )


# ── _bottom_up_order ──────────────────────────────────────────────────────────


def test_bottom_up_order_flat():
    a, b, c = _node("a"), _node("b"), _node("c")
    result = _bottom_up_order([a, b, c])
    assert [n.id for n in result] == ["a", "b", "c"]


def test_bottom_up_order_container_after_children():
    child = _node("child")
    parent = _node("parent", children=["child"])
    result = _bottom_up_order([parent, child])
    ids = [n.id for n in result]
    assert ids.index("child") < ids.index("parent")


def test_bottom_up_order_branches():
    t = _node("t")
    f = _node("f")
    cond = _node("cond", type_="conditional", branches=[["t"], ["f"]])
    result = _bottom_up_order([cond, t, f])
    ids = [n.id for n in result]
    assert ids.index("t") < ids.index("cond")
    assert ids.index("f") < ids.index("cond")


# ── _build_user_message ───────────────────────────────────────────────────────


def test_build_user_message_skips_workflow_entrypoint_output():
    wire = _wire(
        _node("wf", type_="workflow"),
        _node("ep", type_="entrypoint"),
        _node("out", type_="output"),
        _node("act", type_="activity", name="do_something"),
    )
    msg = _build_user_message(wire)
    assert "wf" not in msg
    assert "ep" not in msg
    assert "out" not in msg
    assert "act" in msg
    assert "do_something" in msg


def test_build_user_message_empty_when_only_skipped():
    wire = _wire(
        _node("wf", type_="workflow"),
        _node("ep", type_="entrypoint"),
    )
    assert _build_user_message(wire) == ""


def test_build_user_message_includes_workflow_name():
    wire = _wire(_node("a"), workflow_name="BillingWorkflow")
    msg = _build_user_message(wire)
    assert "BillingWorkflow" in msg


def test_serialize_node_unknown_includes_source_snippet():
    source_bytes = b"x" * 100
    node = FlatNode(id="ell", type="unknown", name="...", source_range=SourceRange(begin=0, end=100, line=1), line=1)
    result = _serialize_node(node, source_bytes)
    assert "source:" in result
    assert "x" * 100 in result


def test_serialize_node_unknown_truncates_long_source():
    from mistralai.workflows.core.graph_summaries import _SOURCE_SNIPPET_LIMIT

    source_bytes = b"a" * (_SOURCE_SNIPPET_LIMIT + 200)
    node = FlatNode(
        id="ell", type="unknown", name="...", source_range=SourceRange(begin=0, end=len(source_bytes), line=1), line=1
    )
    result = _serialize_node(node, source_bytes)
    assert "…" in result
    assert "a" * (_SOURCE_SNIPPET_LIMIT + 1) not in result


def test_serialize_node_unknown_no_source_omits_snippet():
    node = FlatNode(id="ell", type="unknown", name="...", source_range=SourceRange(begin=0, end=10, line=1), line=1)
    result = _serialize_node(node, source_bytes=None)
    assert "source:" not in result


def test_serialize_node_activity_never_includes_source():
    source_bytes = b"some python code here"
    node = FlatNode(
        id="act",
        type="activity",
        name="do_thing",
        source_range=SourceRange(begin=0, end=len(source_bytes), line=1),
        line=1,
    )
    result = _serialize_node(node, source_bytes)
    assert "source:" not in result


def test_build_user_message_passes_source_to_unknown_nodes():
    source = "idx = None  # placeholder"
    node = FlatNode(
        id="ell", type="unknown", name="...", source_range=SourceRange(begin=0, end=len(source), line=1), line=1
    )
    wire = AtlasWireFormat(
        workflow_name="Wf",
        nodes=[node],
        edges=[],
        sources={"/fake/file.py": source},
        files={"/fake/file.py": FileRange(begin=0, end=len(source))},
        incomplete=False,
    )
    msg = _build_user_message(wire)
    assert "idx = None" in msg


def test_build_user_message_includes_callees():
    wire = _wire(_node("d", type_="dispatch", callees=["foo", "bar"]))
    msg = _build_user_message(wire)
    assert "foo" in msg
    assert "bar" in msg


# ── _redact_string_literals ───────────────────────────────────────────────────


def test_redact_string_literals_replaces_strings():
    result = _redact_string_literals('x = "secret"')
    assert "secret" not in result
    assert "..." in result


def test_redact_string_literals_scrubs_untokenisable_source():
    # Snippet extracted mid-block: indents from 0→8, then dedents to 4 which is not
    # in the tokenizer's stack → IndentationError. Secrets must not leak.
    result = _redact_string_literals("        foo('secret')\n    bar()\n")
    assert "secret" not in result
    assert "foo(" in result


# ── summarise_workflow ────────────────────────────────────────────────────────


async def test_summarise_workflow_no_api_key():
    with patch("mistralai.workflows.core.graph_summaries.config") as mock_config:
        mock_config.common.mistral_api_key = None
        result = await summarise_workflow(_wire(_node("a")))
    assert result.status == "disabled"
    assert result.summaries == {}


async def test_summarise_workflow_disabled_by_flag():
    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.worker.graph.graph_summarise_enabled = False
        mock_config.common.mistral_api_key = SecretStr("test-key")
        result = await summarise_workflow(_wire(_node("a")))
    assert result.status == "disabled"
    assert result.summaries == {}
    mock_get_client.assert_not_called()


async def test_summarise_workflow_returns_summaries():
    wire = _wire(_node("a", name="fetch_data"), _node("b", name="send_result"))
    payload = {
        "a": {"short": "fetch data", "long": "Fetches data from the API."},
        "b": {"short": "send result", "long": "Sends the result downstream."},
    }

    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(payload)

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        result = await summarise_workflow(wire)

    assert result.status == "ready"
    assert "a" in result.summaries
    assert result.summaries["a"].short == "fetch data"
    assert result.summaries["a"].long == "Fetches data from the API."
    assert result.summaries["b"].short == "send result"


async def test_summarise_workflow_retries_on_validation_error():
    wire = _wire(_node("a"))

    bad_payload = {"a": {"short": "ok"}}
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(bad_payload)

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        with pytest.raises(SummariseError):
            await summarise_workflow(wire)
        call_count = mock_client.chat.complete_async.call_count

    assert call_count == 3


async def test_summarise_workflow_retries_on_json_decode_error():
    wire = _wire(_node("a"))

    mock_response = MagicMock()
    mock_response.choices[0].message.content = "not json"

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        with pytest.raises(SummariseError):
            await summarise_workflow(wire)
        call_count = mock_client.chat.complete_async.call_count

    assert call_count == 3


async def test_summarise_workflow_raises_on_api_error():
    wire = _wire(_node("a"))

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(side_effect=RuntimeError("network error"))
        mock_get_client.return_value = mock_client

        with pytest.raises(SummariseError, match="network error"):
            await summarise_workflow(wire)


async def test_summarise_workflow_passes_retry_config():
    wire = _wire(_node("a", name="fetch_data"))

    payload = {"a": {"short": "fetch data", "long": "Fetches data."}}
    mock_response = MagicMock()
    mock_response.choices[0].message.content = json.dumps(payload)

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(return_value=mock_response)
        mock_get_client.return_value = mock_client

        await summarise_workflow(wire)

    # Supplying a RetryConfig is what activates the SDK's native 429/5xx backoff; without
    # it the SDK does no retries. Guard that we always opt in.
    retries = mock_client.chat.complete_async.call_args.kwargs["retries"]
    assert retries is _summaries_mod._RETRY_CONFIG
    assert retries.strategy == "backoff"


async def test_summarise_workflow_raises_on_persistent_rate_limit():
    """A 429 that survives the SDK's internal retry budget surfaces as SummariseError."""
    wire = _wire(_node("a"))

    raw_response = MagicMock()
    raw_response.status_code = 429
    raw_response.text = "rate limited"
    raw_response.headers = {}
    rate_limit_exc = MistralError("Too Many Requests", raw_response)

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(side_effect=rate_limit_exc)
        mock_get_client.return_value = mock_client

        with pytest.raises(SummariseError):
            await summarise_workflow(wire)
        # The persistent rate limit is fatal (not re-looped); the SDK already retried it.
        assert mock_client.chat.complete_async.call_count == 1


async def test_summarise_workflow_succeeds_on_retry_after_validation_error():
    wire = _wire(_node("a", name="fetch_data"))

    bad_payload = {"a": {"short": "ok"}}
    bad_response = MagicMock()
    bad_response.choices[0].message.content = json.dumps(bad_payload)

    good_payload = {"a": {"short": "fetch data", "long": "Fetches data."}}
    good_response = MagicMock()
    good_response.choices[0].message.content = json.dumps(good_payload)

    with (
        patch("mistralai.workflows.core.graph_summaries.config") as mock_config,
        patch("mistralai.workflows.core.graph_summaries.get_mistral_client") as mock_get_client,
    ):
        mock_config.common.mistral_api_key = SecretStr("test-key")
        mock_config.worker.graph.graph_summarise_model = "mistral-small-latest"
        mock_client = MagicMock()
        mock_client.chat.complete_async = AsyncMock(side_effect=[bad_response, good_response])
        mock_get_client.return_value = mock_client

        result = await summarise_workflow(wire)

    assert result.status == "ready"
    assert result.summaries["a"].short == "fetch data"
    assert mock_client.chat.complete_async.call_count == 2
