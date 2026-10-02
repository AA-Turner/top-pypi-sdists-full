"""Span text escaping at the signed HTTP boundary; identities stay unchanged."""

import copy
import gzip
import hashlib
import hmac
import json
import warnings

import httpx
import pytest

from probe._generated.models import IngestRunRequest, SpanBatch
from probe.sdk import errors, unstorable
from probe.sdk.config import Settings
from probe.sdk.transport import Transport

NUL = "\x00"
PATH = "/v1/runs/r1/spans"


def escape(body):
    return unstorable.escape_nuls(body, path=PATH)


def transport(sent, **settings):
    def handle(request):
        sent.append(request)
        return httpx.Response(200, json={"upserted": 1})

    return Transport(
        Settings(base_url="http://test", token="test-token", **settings),
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle)),
    )


def test_nested_tool_output_copies_are_escaped_with_one_honest_count():
    stdout = "binary\x00output"
    attrs = {
        "result": stdout,
        "tool_result_metadata": {"content": stdout},
        "raw_tool_result": [{"text": stdout}],
        "extra": {"stderr": stdout, "depth": [[stdout]]},
        "tool_call_id": "call-1",
    }
    body = {"spans": [{"attributes": attrs}]}
    before = copy.deepcopy(body)
    out, counts = escape(body)
    result = out["spans"][0]["attributes"]
    assert result["result"] == r"binary\0output"
    assert result["raw_tool_result"][0]["text"] == r"binary\0output"
    assert result["extra"]["depth"] == [[r"binary\0output"]]
    assert result[unstorable.RECORD_KEY] == {"count": 5, "encoding": "literal-backslash-zero"}
    assert counts == {"spans[0].attributes": 5}
    assert not unstorable.has_nul(out)
    assert body == before


def test_literal_escape_is_unchanged_and_replaying_a_rewrite_is_idempotent():
    literal = {"spans": [{"attributes": {"result": r"literal\0"}}]}
    assert escape(literal) == (literal, {})
    assert escape(literal)[0] is literal
    dirty = {"spans": [{"attributes": {"result": "actual\x00 and literal\\0"}}]}
    out, _ = escape(dirty)
    assert out["spans"][0]["attributes"][unstorable.RECORD_KEY]["count"] == 1
    assert escape(out) == (out, {})
    assert escape(out)[0] is out


@pytest.mark.parametrize("body", [{}, {"a": [1, None, True, "text"]}, "plain", None, 42])
def test_clean_payloads_are_returned_without_copying(body):
    assert not unstorable.has_nul(body)
    out, counts = escape(body)
    assert out is body and counts == {}


def test_shared_containers_are_not_mistaken_for_cycles():
    attrs = {"result": "a\x00"}
    body = {"spans": [{"attributes": attrs}, {"attributes": attrs}]}
    out, counts = escape(body)
    assert sum(counts.values()) == 2
    assert out["spans"][0]["attributes"]["result"] == r"a\0"
    assert attrs == {"result": "a\x00"}


def test_deep_payload_is_a_bounded_permanent_failure():
    body = "text"
    for _ in range(300):
        body = [body]
    with pytest.raises(errors.ValidationError, match="nesting"):
        unstorable.has_nul(body)


@pytest.mark.parametrize("path", [PATH, "/ingest/v1/runs"])
def test_actual_sent_bytes_are_escaped_and_signed(path):
    sent = []
    body = {
        "spans": [
            {
                "id": "11111111-1111-4111-8111-111111111111",
                "span_type": "tool_call",
                "attributes": {"result": "a\x00b"},
            }
        ]
    }
    if path.startswith("/ingest"):
        body.update(project_slug="nul-tests", run={"external_id": "run-1"})
    schema = IngestRunRequest if path.startswith("/ingest") else SpanBatch
    schema.model_validate(body)
    with pytest.warns(UserWarning, match="escaped 1 NUL"):
        transport(sent, ingest_token="test-ingest", hmac_secret="test-secret").post(path, body)
    parsed = json.loads(sent[0].content)
    schema.model_validate(parsed)
    assert parsed["spans"][0]["attributes"]["result"] == r"a\0b"
    assert not unstorable.has_nul(parsed)
    if path.startswith("/ingest"):
        digest = hmac.new(b"test-secret", sent[0].content, hashlib.sha256).hexdigest()
        assert sent[0].headers["X-Signature"] == f"sha256={digest}"


def test_ingest_execution_record_is_not_escaped_alongside_spans():
    sent = []
    body = {"spans": [{"attributes": {"result": "a\x00"}}], "execution_record": {"code": "a\x00"}}
    with pytest.raises(errors.ValidationError):
        transport(sent).post("/ingest/v1/runs", body)
    assert not sent


def test_credential_scrubbing_still_applies_to_escaped_span_text():
    sent = []
    token = "sk-proj-" + "A" * 48
    with pytest.warns(UserWarning):
        transport(sent).post(
            PATH,
            {"spans": [{"attributes": {"result": "\x00" + token, "message": "safe\x00text"}}]},
        )
    assert token.encode() not in sent[0].content
    assert not unstorable.has_nul(json.loads(sent[0].content))


def test_warnings_as_errors_cannot_prevent_the_write():
    sent = []
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        transport(sent).post(PATH, {"spans": [{"attributes": {"result": "a\x00"}}]})
    assert len(sent) == 1


def test_clean_request_has_no_warning_or_rewrite():
    sent = []
    body = {"spans": [{"attributes": {"result": r"clean\0"}}]}
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        transport(sent).post(PATH, body)
    assert not caught
    assert json.loads(sent[0].content) == body


def test_hand_written_span_uses_the_same_safeguard(client, app):
    from conftest import open_run

    run = open_run(client, experiment="nul-exp")
    run.span("tool_call", name="grep", attributes={"result": "a\x00\x00b"})
    attrs = app.spans[run.id][0]["attributes"]
    assert attrs["result"] == r"a\0\0b"
    assert attrs[unstorable.RECORD_KEY]["count"] == 2


def test_artifact_bytes_are_not_escaped():
    sent = []
    payload = gzip.compress(b'{"text":"original"}', mtime=0)
    assert b"\x00" in payload
    transport(sent).put_url("http://objects.test/blob", payload)
    assert sent[0].content == payload


@pytest.mark.parametrize("method", ["GET", "PATCH", "PUT"])
def test_only_span_post_can_rewrite(method):
    with pytest.raises(errors.ValidationError):
        unstorable.escape_nuls(
            {"spans": [{"attributes": {"result": "a\x00"}}]}, path=PATH, method=method
        )


def test_nul_query_is_rejected_without_changing_search_identity():
    sent = []
    with pytest.raises(errors.ValidationError):
        transport(sent).request("GET", "/v1/runs", params={"name": "a\x00"})
    assert not sent
