"""Regression cases from the pre-merge NUL safeguard audit."""

import json
import subprocess
import sys
import warnings

import httpx
import pytest

from probe.sdk import errors, unstorable
from probe.sdk.config import Settings
from probe.sdk.journal import Journal, classify, drain
from probe.sdk.transport import Transport

SPAN_PATH = "/v1/runs/run-a/spans"

#: Must stay CREDENTIAL-SHAPED. These cases prove that scrubbing removes a
#: secret carried alongside a NUL, so the value has to be one the scrubber
#: recognizes. It was `opaque`, which stopped being a credential once a
#: plain-word key such as `token` began requiring a key-shaped value too --
#: an English word after `token=` is exactly the false positive that change
#: exists to stop, and the safeguard here is about the NUL, not the heuristic.
NUL_SECRET = "8Fk2mQxRv91TzPbNw4Lc7Hd3"


def transport(sent):
    def handle(request):
        sent.append(request)
        return httpx.Response(200, json={"upserted": 1})

    return Transport(
        Settings(base_url="http://test", token="test-token"),
        client=httpx.Client(base_url="http://test", transport=httpx.MockTransport(handle)),
    )


@pytest.mark.parametrize("reverse", [False, True])
def test_colliding_keys_are_rejected_without_sending_or_mutating(reverse):
    entries = [("x\x00", "first"), (r"x\0", "second")]
    attrs = dict(reversed(entries) if reverse else entries)
    body = {"spans": [{"attributes": {"result": attrs}}]}
    before = json.dumps(body)
    sent = []
    with pytest.raises(errors.ValidationError) as caught:
        transport(sent).post(SPAN_PATH, body)
    assert classify(caught.value) == "permanent"
    assert json.dumps(body) == before
    assert sent == []


@pytest.mark.parametrize(
    "path,body",
    [
        ("/v1/runs/run-a/metrics", {"points": [{"dimensions": {"worker": "gpu\x00"}}]}),
        ("/v1/execution-records", {"code": {"source": "a\x00b"}}),
        ("/v1/metric-views", {"spec": {"expression": {"dimensions": {"worker": "gpu\x00"}}}}),
        (SPAN_PATH, {"spans": [{"external_key": "a\x00", "attributes": {}}]}),
        (SPAN_PATH, {"spans": [{"attributes": {"tool_call_id": "a\x00"}}]}),
        (SPAN_PATH, {"spans": [{"attributes": {"extra": {"dimensions": {"worker": "gpu\x00"}}}}]}),
        ("/v1/projects", {"attributes": {"result": "a\x00"}}),
    ],
)
def test_identity_and_unknown_schema_values_are_not_rewritten(path, body):
    sent = []
    before = json.dumps(body)
    with pytest.raises(errors.ValidationError):
        transport(sent).post(path, body)
    assert not sent
    assert json.dumps(body) == before


def test_warning_does_not_disclose_arbitrary_keys_and_is_bounded():
    private = "private-customer-prompt"
    body = {"spans": [{"attributes": {"result": {private + str(i): "a\x00" for i in range(1000)}}}]}
    sent = []
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        transport(sent).post(SPAN_PATH, body)
    message = " ".join(str(w.message) for w in caught)
    assert private not in message
    assert len(message) < 1024
    assert "1000" in message
    assert json.loads(sent[0].content)["spans"][0]["attributes"]["result"][private + "0"] == r"a\0"


def test_cycles_fail_promptly_before_the_network():
    # A subprocess makes the old infinite scan a bounded regression failure.
    code = """
from probe.sdk import unstorable, errors
x = []; x.append(x)
try:
    unstorable.has_nul(x)
except errors.ValidationError:
    pass
else:
    raise AssertionError('cycle was accepted')
"""
    result = subprocess.run([sys.executable, "-c", code], timeout=3, capture_output=True)
    assert result.returncode == 0, result.stderr.decode()


def test_metadata_collision_is_rejected_instead_of_hiding_the_rewrite():
    sent = []
    attrs = {"result": "a\x00", unstorable.RECORD_KEY: {"user": "owned"}}
    with pytest.raises(errors.ValidationError):
        transport(sent).post(SPAN_PATH, {"spans": [{"attributes": attrs}]})
    assert not sent
    assert attrs[unstorable.RECORD_KEY] == {"user": "owned"}


def test_old_queued_span_is_escaped_and_bad_identity_does_not_block_next_write(tmp_path):
    journal = Journal(tmp_path / "outbox")
    bad = {"points": [{"dimensions": {"worker": "gpu\x00"}}]}
    journal.append_http("POST", "/v1/runs/run-a/metrics", bad, run_ref="run-a")
    journal.append_http(
        "POST", SPAN_PATH, {"spans": [{"attributes": {"result": "a\x00"}}]}, run_ref="run-a"
    )
    journal.append_http("POST", "/v1/runs/run-b/metrics", {"points": []}, run_ref="run-b")
    sent = []

    class Client:
        def __init__(self):
            self.transport = transport(sent)

        def close(self):
            self.transport.close()

    report = drain(journal, client_factory=lambda _: Client())
    assert report.dead_lettered == 1
    assert report.delivered == 2
    assert report.remaining == 0
    assert journal.failed()[0][1]["body"] == bad
    # By content, not position: runs drain in turn (plan 1.6), so run-b's
    # write may go before run-a's span; only each run's own order is kept.
    (span,) = [json.loads(r.content) for r in sent if "spans" in json.loads(r.content)]
    assert span["spans"][0]["attributes"]["result"] == r"a\0"


def test_sets_and_opaque_objects_cannot_introduce_unchecked_nul():
    class Opaque:
        def __repr__(self):
            return "opaque\x00text"

    for value in ({"a\x00"}, Opaque()):
        sent = []
        with pytest.raises(errors.ValidationError):
            transport(sent).post("/v1/projects", {"name": value})
        assert not sent
        with pytest.warns(UserWarning):
            transport(sent).post(SPAN_PATH, {"spans": [{"attributes": {"result": value}}]})
        assert not unstorable.has_nul(json.loads(sent[0].content))


def test_aliases_cannot_bypass_the_depth_limit():
    body = {}
    chain = "leaf"
    for index in range(10):
        for _ in range(240):
            chain = [chain]
        body[str(index)] = chain
    with pytest.raises(errors.ValidationError, match="nesting"):
        unstorable.has_nul(body)


def test_public_sdk_cycles_are_permanent_before_scrubbing(client):
    cyclic = []
    cyclic.append(cyclic)
    with pytest.raises(errors.ValidationError) as caught:
        client.write(
            "POST", SPAN_PATH, {"spans": [{"attributes": {"result": cyclic}}]}, strict=True
        )
    assert classify(caught.value) == "permanent"


def test_formatted_warning_does_not_echo_the_callers_source_line():
    import linecache

    sent = []
    token = "sk-proj-" + "A" * 48
    filename = "synthetic-private-caller.py"
    source = (
        't.request("POST", PATH, json_body={"spans":[{"attributes":{"result":"\\x00'
        + token
        + '","message":"safe\\x00text"}}]})\n'
    )
    linecache.cache[filename] = (len(source), None, source.splitlines(True), filename)
    try:
        with warnings.catch_warnings(record=True) as caught:
            warnings.simplefilter("always")
            exec(compile(source, filename, "exec"), {"t": transport(sent), "PATH": SPAN_PATH})
        formatted = "".join(
            warnings.formatwarning(w.message, w.category, w.filename, w.lineno) for w in caught
        )
        assert caught
        assert token not in formatted
        assert filename not in formatted
        assert token.encode() not in sent[0].content
    finally:
        linecache.cache.pop(filename, None)


def test_interleaved_nul_credential_is_redacted_before_it_becomes_uploadable():
    token = "sk-proj-" + "A" * 48
    interleaved = token.encode("utf-16-le").decode("utf-8")
    sent = []
    transport(sent).post(SPAN_PATH, {"spans": [{"attributes": {"result": interleaved}}]})
    result = json.loads(sent[0].content)["spans"][0]["attributes"]["result"]
    assert result == "<redacted>"
    assert token not in result.replace(r"\0", "").replace("\x00", "")


def test_scrubbing_cannot_turn_a_forbidden_identity_into_a_valid_alias():
    sent = []
    with pytest.raises(errors.ValidationError):
        transport(sent).post(
            SPAN_PATH, {"spans": [{"external_key": f"token={NUL_SECRET}\x00", "attributes": {}}]}
        )
    assert not sent


@pytest.mark.parametrize("async_writes", [False, True])
def test_fail_open_retains_identity_refusal_even_when_scrubbing_removes_nul(
    client, monkeypatch, async_writes
):
    client.async_writes = async_writes
    monkeypatch.setattr(client, "_after_enqueue", lambda: None)
    sent = []
    client.transport = transport(sent)
    body = {"spans": [{"external_key": f"token={NUL_SECRET}\x00", "attributes": {}}]}
    assert client.write("POST", SPAN_PATH, body, strict=False) is None
    entries = client.journal.pending()
    assert len(entries) == 1
    assert entries[0][1]["kind"] == "rejected_http"
    assert NUL_SECRET not in json.dumps(entries[0][1])
    report = drain(client.journal, client_factory=lambda _: client)
    assert report.dead_lettered == 1
    assert not sent
    client.journal.retry_failed()
    report = drain(client.journal, client_factory=lambda _: client)
    assert report.dead_lettered == 1 and not sent


def test_legacy_queue_identity_is_validated_before_replay_scrubbing(tmp_path):
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", SPAN_PATH, {"spans": []})
    path, op = journal.pending()[0]
    op["body"] = {"spans": [{"external_key": f"token={NUL_SECRET}\x00", "attributes": {}}]}
    path.write_text(json.dumps(op))
    sent = []

    class Client:
        def __init__(self):
            self.transport = transport(sent)

    report = drain(journal, client_factory=lambda _: Client())
    assert report.dead_lettered == 1 and not sent
    failed_path, failed = journal.failed()[0]
    assert failed["kind"] == "rejected_http"
    assert NUL_SECRET not in failed_path.read_text()
    journal.retry_failed()
    report = drain(journal, client_factory=lambda _: Client())
    assert report.dead_lettered == 1 and not sent


def test_queued_interleaved_credentials_are_redacted_at_rest(tmp_path):
    token = "sk-proj-" + "A" * 48
    journal = Journal(tmp_path / "outbox")
    journal.append_http(
        "POST", SPAN_PATH, {"spans": [{"attributes": {"result": "\x00".join(token)}}]}
    )
    body = journal.pending()[0][1]["body"]
    assert body["spans"][0]["attributes"]["result"] == "<redacted>"


@pytest.mark.parametrize("key", ["pass\x00word", "\x00".join("password")])
def test_nul_sensitive_keys_redact_opaque_values_at_rest(tmp_path, key):
    journal = Journal(tmp_path / "outbox")
    journal.append_http(
        "POST", SPAN_PATH, {"spans": [{"attributes": {"result": {key: "private-value"}}}]}
    )
    path, op = journal.pending()[0]
    assert op["kind"] == "rejected_http"
    assert "private-value" not in path.read_text()
    assert op["body"]["spans"][0]["attributes"]["result"][key] == "<redacted>"


@pytest.mark.parametrize(
    "options",
    [
        {"strict": True},
        {"strict": False, "raise_permanent": True},
        {"strict": False, "durable": False},
    ],
)
def test_explicit_strict_refusal_never_queues_an_altered_identity(client, options):
    with pytest.raises(errors.ValidationError):
        client.write(
            "POST",
            SPAN_PATH,
            {"spans": [{"external_key": f"token={NUL_SECRET}\x00", "attributes": {}}]},
            **options,
        )
    assert not client.journal.pending()


@pytest.mark.parametrize("serialized", [False, True])
def test_nul_credentials_are_inspected_before_partial_scrubbing(tmp_path, serialized):
    suffix = "B" * 32
    value = "sk-proj-" + "A" * 15 + "\x00" + suffix
    if serialized:
        value = json.dumps({"output": "\x00".join("sk-proj-" + suffix)})
    body = {"spans": [{"attributes": {"result": value}}]}
    sent = []
    transport(sent).post(SPAN_PATH, body)
    result = json.loads(sent[0].content)["spans"][0]["attributes"]["result"]
    assert result == "<redacted>" or json.loads(result)["output"] == "<redacted>"
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", SPAN_PATH, body)
    result = journal.pending()[0][1]["body"]["spans"][0]["attributes"]["result"]
    assert result == "<redacted>" or json.loads(result)["output"] == "<redacted>"


def test_opaque_identity_is_validated_before_repr_scrubbing(tmp_path):
    class Opaque:
        def __repr__(self):
            return f"token={NUL_SECRET}\x00"

    body = {"spans": [{"external_key": Opaque(), "attributes": {}}]}
    sent = []
    with pytest.raises(errors.ValidationError):
        transport(sent).post(SPAN_PATH, body)
    assert not sent
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", SPAN_PATH, body)
    assert journal.pending()[0][1]["kind"] == "rejected_http"


def test_overdeep_legacy_record_is_safely_retained_without_poisoning_queue(tmp_path):
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", SPAN_PATH, {"spans": []})
    path, op = journal.pending()[0]
    nested = "leaf"
    for _ in range(260):
        nested = [nested]
    op["body"] = {"password": "private-value", "nested": nested}
    path.write_text(json.dumps(op))
    journal.append_http("POST", SPAN_PATH, {"spans": []})
    sent = []

    class Client:
        def __init__(self):
            self.transport = transport(sent)

    report = drain(journal, client_factory=lambda _: Client())
    assert report.dead_lettered == 1 and report.delivered == 1
    failed_path, failed = journal.failed()[0]
    assert failed["kind"] == "rejected_http"
    assert "private-value" not in failed_path.read_text()


def test_depth_limit_is_identical_for_enqueue_and_replay(tmp_path):
    nested = "leaf"
    for _ in range(252):
        nested = [nested]
    body = {"spans": [{"attributes": {"result": nested}}]}
    assert not unstorable.has_nul(body)
    journal = Journal(tmp_path / "outbox")
    journal.append_http("POST", SPAN_PATH, body)
    sent = []

    class Client:
        def __init__(self):
            self.transport = transport(sent)

    report = drain(journal, client_factory=lambda _: Client())
    assert report.delivered == 1 and report.dead_lettered == 0
    assert json.loads(sent[0].content) == body
