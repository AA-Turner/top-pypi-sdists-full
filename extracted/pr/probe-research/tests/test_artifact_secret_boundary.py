"""Credential refusals happen before local persistence or outbound transport."""

import base64
import gzip
import io
import json
import zipfile
from pathlib import Path

import pytest

KEY = "AKIA" + "IOSFODNN7EXAMPLE"
SECRET = ("AWS_ACCESS_KEY_ID=" + KEY + "\n").encode()


def test_plaintext_is_redacted_before_snapshot(tmp_path):
    """The staged copy is what gets hashed, so the key must be gone from IT.

    Stronger than the refusal this replaces: the credential still never
    reaches a second place on disk, and the artifact survives.
    """
    from probe.sdk.secret_gate import safe_snapshot_file

    src = tmp_path / "config.txt"
    src.write_bytes(SECRET)
    dst = tmp_path / "staged"
    safe_snapshot_file(src, dst)
    staged = dst.read_bytes()
    assert KEY.encode() not in staged
    assert b"<redacted:aws-access-key-id>" in staged
    assert src.read_bytes() == SECRET  # the researcher's own file is untouched


def _encoded(encoding: str) -> bytes:
    if encoding == "utf8":
        return SECRET
    if encoding == "utf16":
        return SECRET.decode().encode("utf-16")
    if encoding == "utf32":
        return SECRET.decode().encode("utf-32")
    if encoding == "nul":
        return b"\0" + SECRET
    if encoding == "base64":
        return base64.b64encode(SECRET)
    if encoding == "gzip":
        return gzip.compress(SECRET)
    if encoding == "tail":
        return b"x" * (8 * 1024 * 1024) + b"\n" + SECRET
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, "w", zipfile.ZIP_DEFLATED) as archive:
        archive.writestr("config.env", SECRET)
    return stream.getvalue()


_ENCODINGS = ["utf8", "utf16", "utf32", "nul", "base64", "gzip", "zip", "tail"]


@pytest.mark.parametrize("encoding", _ENCODINGS)
def test_the_full_gate_sees_every_encoding(encoding):
    """Every encoding is still SEEN by the full gate -- the one the server runs
    on every upload (`app/security/_credential_gate.py` is generated from it).
    `tail` pins that a credential 8 MB in is still reached."""
    from probe.sdk.secret_gate import inspect_bytes

    assert inspect_bytes(_encoded(encoding)).has_findings, encoding


@pytest.mark.parametrize("encoding", _ENCODINGS)
def test_the_client_rewrites_readable_text_and_leaves_the_rest(tmp_path, encoding):
    """The researcher-side check replaces credentials in UTF-8 text, and returns
    everything else byte-for-byte for the server to inspect: a wide encoding or
    a container is never rewritten (a replaced span corrupts it), and a
    base64-encoded key is not decoded on this side of the wire."""
    from probe.sdk.secret_gate import read_upload_redacted

    raw = _encoded(encoding)
    path = tmp_path / "file"
    path.write_bytes(raw)
    clean, result = read_upload_redacted(path)
    if encoding in {"utf8", "nul", "tail"}:
        assert result.has_findings
        assert clean != raw and b"<redacted:" in clean
        assert KEY.encode() not in clean
    else:
        assert clean == raw, f"{encoding} must not be rewritten"
        assert not result.has_findings, f"{encoding} is the server's to inspect"


def test_safe_snapshot_is_immutable_and_benign(tmp_path):
    from probe.sdk.secret_gate import checked_upload

    source = tmp_path / "clean.txt"
    source.write_text("learning_rate: 0.003\n")
    with checked_upload(source) as frozen:
        source.write_bytes(SECRET)
        assert Path(frozen).read_text() == "learning_rate: 0.003\n"
    assert not Path(frozen).exists()


def test_legacy_blob_is_redacted_on_replay_and_tampering_still_refuses(tmp_path):
    """A blob staged by an OLD client is redacted when it is read back, and the
    source-digest contract that catches tampering is untouched.

    This replaces a refusal test. The refusal it checked -- no network call for
    a blob carrying a credential -- is gone by design: a detected credential
    never costs the upload now. What had to survive is that the credential does
    not leave in the bytes, and that a CHANGED source is still caught.
    """
    import hashlib

    from probe.sdk.secret_gate import CredentialBlocked, checked_upload, read_upload_redacted

    source = tmp_path / "old-blob"
    source.write_bytes(SECRET)

    clean, result = read_upload_redacted(source)
    assert KEY.encode() not in clean
    assert "aws-access-key-id" in result.rules

    # The digest describes the SOURCE, so a legacy fingerprint still validates
    # and redaction does not masquerade as tampering.
    with checked_upload(source, digest=hashlib.sha256(SECRET).hexdigest(), size=len(SECRET)):
        pass

    source.write_bytes(SECRET + b"appended after the fingerprint\n")
    with pytest.raises(CredentialBlocked) as error:
        with checked_upload(source, digest=hashlib.sha256(SECRET).hexdigest(), size=len(SECRET)):
            pass
    assert KEY not in str(error.value)


@pytest.fixture
def wire_client(tmp_path, monkeypatch):
    import httpx
    from probe.sdk.client import Client
    from probe.sdk.config import Settings
    from probe.sdk.transport import Transport
    from probe.sdk.journal import Journal
    from probe.sdk.run import Run

    monkeypatch.setenv("PROBE_CONFIG_PATH", str(tmp_path / "config.json"))
    monkeypatch.setenv("XDG_STATE_HOME", str(tmp_path / "state"))
    monkeypatch.setenv("XDG_CONFIG_HOME", str(tmp_path / "config"))
    import probe.sdk.journal as jm

    monkeypatch.setattr(jm, "MIN_FREE_BYTES", 0)
    requests = []

    def respond(req):
        requests.append((req.method, req.url.path, req.read()))
        if req.url.path.endswith("/uploads"):
            return httpx.Response(
                200,
                json={
                    "artifact_id": "a",
                    "have": False,
                    "upload_url": "https://blob.invalid/object",
                },
            )
        return httpx.Response(200, json={"id": "a", "status": "complete"})

    settings = Settings(base_url="https://api.invalid", token="synthetic-test-auth")
    http = httpx.Client(base_url=settings.base_url, transport=httpx.MockTransport(respond))
    transport = Transport(settings, client=http, surface="mcp", max_retries=0)
    journal = Journal(tmp_path / "outbox", context={"name": None, "base_url": settings.base_url})
    client = Client(
        settings=settings,
        transport=transport,
        journal=journal,
        async_writes=False,
        auto_drain=False,
        redact=False,
    )
    client._after_enqueue = lambda: None
    client._wake_delivery = lambda: None
    yield client, Run(client, {"id": "r"}), journal, requests
    http.close()


@pytest.mark.parametrize("entry", ["client", "run", "run-async", "client-queue", "receipt-queue"])
def test_public_boundaries_never_emit_the_credential(wire_client, tmp_path, entry):
    """Every public entry point uploads, and none of them emits the key.

    An async upload is promoted and delivered here too: until then it waits,
    unscanned, in `waiting/`, and "nothing was sent" would prove nothing.

    This replaces a refusal test. The artifact is no longer destroyed to
    protect the secret -- but the secret still reaches neither the wire nor
    the outbox on disk, which is what the refusal was actually protecting.
    """
    c, run, journal, requests = wire_client
    path = tmp_path / "secret.txt"
    path.write_bytes(SECRET)
    if entry == "client":
        c.upload_file("run", "r", "secret.txt", str(path))
    elif entry == "run":
        run.log_artifact("secret.txt", path=str(path), sync=True)
    elif entry == "run-async":
        from probe.sdk.journal import drain

        c.async_writes = True
        run.log_artifact("secret.txt", path=str(path), sync=False)
        # The waiting room holds the plain copy until its scan; the key must be
        # gone from everything that is ever SENT, so promote and deliver.
        assert drain(journal, client_factory=lambda _: c).delivered >= 1
        assert not journal.waiting_dir.exists() or not any(journal.waiting_dir.iterdir())
        puts = [body for method, _, body in requests if method == "PUT"]
        assert puts and all(b"<redacted:" in body for body in puts), "a positive control"
    elif entry == "client-queue":
        c._enqueue_upload(anchor="run", anchor_id="r", name="secret.txt", src_path=str(path))
    else:
        c.enqueue_artifact_upload(
            correlation="test", anchor="run", anchor_id="r", name="secret.txt", path=str(path)
        )
    assert all(KEY.encode() not in body for _, _, body in requests)
    for spool in (journal.blobs_dir, journal.ops_dir):
        if spool.exists():
            for staged in spool.rglob("*"):
                if staged.is_file():
                    assert KEY.encode() not in staged.read_bytes(), staged
    assert path.read_bytes() == SECRET  # the source file is never modified


@pytest.mark.parametrize("entry", ["client", "run", "run-async"])
def test_benign_upload_and_metadata_scrub(wire_client, tmp_path, entry):
    from probe.sdk.journal import drain

    c, run, journal, requests = wire_client
    path = tmp_path / "clean.txt"
    path.write_bytes(b"learning_rate: 0.003\n")
    kwargs = {
        "meta": {"api_key": KEY, "nested": {"details": SECRET.decode()}},
        "notes": SECRET.decode(),
    }
    if entry == "client":
        c.upload_file("run", "r", KEY + ".txt", str(path), **kwargs)
    else:
        c.async_writes = entry == "run-async"
        run.log_artifact(KEY + ".txt", path=str(path), sync=entry != "run-async", **kwargs)
    if entry == "run-async":
        assert all(KEY.encode() not in f.read_bytes() for f in journal.ops_dir.glob("*.json"))
        assert drain(journal, client_factory=lambda _: c).delivered == 1
    assert [body for method, _, body in requests if method == "PUT"] == [path.read_bytes()]
    assert all(KEY.encode() not in body for method, _, body in requests if method != "PUT")


def test_low_level_transport_inspects_without_rewriting(wire_client, tmp_path):
    """Transport is BELOW the redaction boundary and must not rewrite.

    By the time bytes reach a PUT their digest is signed and R2 verifies it
    independently, so changing one here could only produce a checksum the
    server refuses. These primitives inspect and warn; redaction happened
    earlier, in `prepare_upload`. The server gate records whatever a caller
    that skipped that step sends.
    """
    c, _, _, requests = wire_client
    path = tmp_path / "secret.txt"
    path.write_bytes(SECRET)
    c.transport.put_url("https://blob.invalid/object", SECRET)
    c.transport.put_file("https://blob.invalid/object", str(path))
    c.transport.put_fileobj(
        "https://blob.invalid/object", io.BytesIO(SECRET), size=len(SECRET)
    )
    puts = [body for method, _, body in requests if method == "PUT"]
    assert len(puts) == 3
    assert all(body == SECRET for body in puts)


def test_resource_limits_still_refuse_but_a_credential_does_not():
    """The two reasons left to refuse are RESOURCE limits and an unreadable
    source. Neither is a finding, and there is nothing to record for them."""
    from probe.sdk.secret_gate import CredentialBlocked, ScanPolicy, inspect_bytes, redact_bytes

    with pytest.raises(CredentialBlocked):
        inspect_bytes(b"abcde", scan_policy=ScanPolicy(max_bytes=4))
    with pytest.raises(CredentialBlocked):
        inspect_bytes(gzip.compress(b"x" * 1024), scan_policy=ScanPolicy(max_expanded_bytes=100))
    with pytest.raises(CredentialBlocked):
        inspect_bytes(b"\xff\x00\x80", scan_policy=ScanPolicy(allow_opaque=False))
    inspect_bytes(b"\xff\x00\x80", scan_policy=ScanPolicy(allow_opaque=True))
    # Opaque bytes carrying a credential: recorded, stored, never rewritten.
    carrier = b"\xff\x00\x80" + SECRET
    clean, result = redact_bytes(carrier, scan_policy=ScanPolicy(allow_opaque=True))
    assert "aws-access-key-id" in result.rules
    assert clean == carrier


def test_presign_time_source_mutation_cannot_change_uploaded_bytes(wire_client, tmp_path):
    c, _, _, requests = wire_client
    source = tmp_path / "clean.txt"
    original = b"learning_rate: 0.003\n"
    source.write_bytes(original)
    mock = c.transport._client._transport
    previous = mock.handler

    def mutate_after_presign(request):
        response = previous(request)
        if request.url.path.endswith("/uploads"):
            source.write_bytes(SECRET)
        return response

    mock.handler = mutate_after_presign
    c.upload_file("run", "r", "clean.txt", str(source))
    assert source.read_bytes() == SECRET
    assert [body for method, _, body in requests if method == "PUT"] == [original]


def test_legacy_queued_secret_is_rejected_without_reference_fallback(wire_client, tmp_path):
    from probe.sdk.journal import drain

    c, _, journal, requests = wire_client
    source = tmp_path / "clean.txt"
    source.write_bytes(b"clean")
    queued = journal.append_upload(
        anchor="run", anchor_id="r", name="clean.txt", src_path=str(source), inline_hash=True
    )
    # Model bytes left behind by an older SDK, without sending them anywhere.
    (journal.blobs_dir / queued["blob"]).write_bytes(SECRET)
    report = drain(journal, client_factory=lambda _: c)
    assert report.dead_lettered == 1
    assert requests == []
    assert all(KEY not in error for error in report.errors)


def test_tar_gzip_inspects_members_and_keeps_benign_archives():
    import tarfile
    from probe.sdk.secret_gate import inspect_bytes

    def archive(contents):
        stream = io.BytesIO()
        with tarfile.open(fileobj=stream, mode="w:gz") as tar:
            info = tarfile.TarInfo("config.txt")
            info.size = len(contents)
            tar.addfile(info, io.BytesIO(contents))
        return stream.getvalue()

    from probe.sdk.secret_gate import redact_bytes

    assert not inspect_bytes(archive(b"learning_rate: 0.003\n")).has_findings
    carrier = archive(SECRET)
    clean, result = redact_bytes(carrier)
    assert "aws-access-key-id" in result.rules  # the member was read
    assert clean == carrier  # ...and the archive was NOT rewritten


def test_source_path_credential_is_not_persisted(tmp_path):
    from probe.sdk.secret_gate import CredentialBlocked, safe_snapshot_file

    source = tmp_path / (KEY + ".txt")
    source.write_bytes(b"clean")
    with pytest.raises(CredentialBlocked) as error:
        safe_snapshot_file(source, tmp_path / "copy")
    assert KEY not in str(error.value)
    assert not (tmp_path / "copy").exists()


def test_scanner_failure_is_closed_and_error_has_no_secret(monkeypatch):
    import traceback
    from probe.sdk import secret_gate

    def broken_scanner(_):
        raise RuntimeError(KEY)

    monkeypatch.setattr(secret_gate, "scan", broken_scanner)
    with pytest.raises(secret_gate.CredentialBlocked) as error:
        secret_gate.inspect_bytes(b"clean")
    assert KEY not in "".join(traceback.format_exception(error.value))


@pytest.mark.parametrize(
    "contents",
    [
        b"https://example.invalid/?token=abc",
        b'{"apiKey":"ab"}',
        b"Authorization: Bearer abc",
    ],
)
def test_short_credentials_in_explicit_context_are_still_detected(contents):
    """Short values in an explicit credential slot stay findings. They are
    recorded by the key-name tier, which deliberately does not rewrite."""
    from probe.sdk.secret_gate import inspect_bytes

    assert inspect_bytes(contents).has_findings


@pytest.mark.parametrize(
    "contents",
    [
        b'{"tokenizer":"cl100k_base","max_tokens":1024}',
        b"sha256: 0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef",
        b"/home/researcher/checkpoints/run-4000/model.pt",
        b'{ "learning_rate": 0.003, "batch_size": 32 }',
    ],
)
def test_benign_contexts_and_formatting_are_not_credentials(contents):
    from probe.sdk.secret_gate import inspect_bytes

    inspect_bytes(contents)


@pytest.mark.parametrize(
    "contents",
    [
        b"HTTPS://example.com/a",
        b'{"api_key":null}',
        b"API_KEY=${API_KEY}",
        b'API_KEY="${API_KEY}"',
        b'{ "api_key": "${API_KEY}" }',
        "Résumé from today — approved".encode("cp1252"),
    ],
)
def test_benign_url_null_reference_and_legacy_text_are_accepted(contents):
    from probe.sdk.secret_gate import inspect_bytes

    inspect_bytes(contents)


@pytest.mark.parametrize(
    "contents",
    [
        b"HTTPS://example.com/a?api_key=abc",
        b'{"api_key":"abc"}',
        b"API_KEY=abc",
        "Résumé — API_KEY=abc".encode("cp1252"),
    ],
)
def test_benign_compatibility_does_not_waive_credentials(contents):
    """A benign-looking wrapper never hides a credential from the record."""
    from probe.sdk.secret_gate import inspect_bytes

    assert inspect_bytes(contents).has_findings


def test_opaque_default_allows_original_bytes_with_warning(tmp_path, monkeypatch):
    from probe.sdk.secret_gate import ArtifactInspectionWarning, read_upload

    monkeypatch.delenv("PROBE_ARTIFACT_OPAQUE_POLICY", raising=False)
    raw = b"\xff\x00\x80"
    source = tmp_path / "opaque.bin"
    source.write_bytes(raw)
    with pytest.warns(ArtifactInspectionWarning, match="cannot confirm"):
        assert read_upload(source) == raw


# ---------------------------------------------------------------------------
# Model output is not a credential
#
# A GSM8K training run had `predictions_final.jsonl` (500 rows) refused whole
# because row 153 read `60 cookies * $0.10/cookie = $<<60*0.1=6>>6.`: `cookie`
# is a member of `_SENSITIVE_KEYS`, so an arithmetic answer about biscuits was
# read as a browser session cookie. These tests pin both directions of the fix.
# ---------------------------------------------------------------------------

GSM8K_ROW = json.dumps(
    {
        "question": "Carl buys 10 packs of 6 cookies at $0.10 each. What change from $10?",
        "pred": (
            "The number of cookies is 10 packs * 6 cookies/pack = <<10*6=60>>60 cookies.\n"
            "The total cost of the cookies is 60 cookies * $0.10/cookie = $<<60*0.1=6>>6.\n"
            "Carl receives $10 - $6 = $<<10-6=4>>4 in change.\n#### 4"
        ),
        "pred_answer": "4",
    }
).encode()

#: A GPT-2 style vocabulary dump. `Ġ` is U+0120, the space marker, and its
#: ESCAPE supplies the digits and second character class the short-anchored
#: entropy rule asks for; decoded, `Ġcookie` scores 2.52 against a 2.50
#: floor. Both halves matched before the fix, so every row was a credential.
VOCAB_DUMP = b"\n".join(
    json.dumps({"token": token, "id": index}).encode()
    for token, index in [
        ("Ġthe", 262), ("Ġcookie", 12045), ("abc", 1),
        ("Ġand", 290), ("Ġ\"", 12), ("!", 0),
    ]
)

MODEL_OUTPUT = {
    "48 repeated digits": b"The answer is " + b"3" * 48 + b" cookies.",
    "long run of one letter": b"attention mask: " + b"A" * 300,
    "tokenizer vocab dump": VOCAB_DUMP,
    "tokenizer id as an int": b'{"token": 50257, "id": 262}',
    "column of repeated hex": b"\n".join([b"deadbeef" * 6] * 40),
    "gsm8k cookie arithmetic": GSM8K_ROW,
    "cookie as a countable noun": b"Each cookie = 3 dollars",
    "token as a bus fare": b"token = one bus token",
    "cookie field holding food": json.dumps({"cookie": "chocolate chip"}).encode(),
    "secret field holding prose": json.dumps({"secret": "the flour"}).encode(),
}


@pytest.mark.parametrize("name", sorted(MODEL_OUTPUT))
def test_model_output_shapes_are_not_credentials(name):
    from probe.sdk.secret_gate import inspect_bytes

    inspect_bytes(MODEL_OUTPUT[name])


def test_the_refused_predictions_row_uploads_unchanged():
    """The exact row that cost a 500-row predictions file its upload."""
    from probe.sdk.redaction import scrub_string
    from probe.sdk.secret_gate import inspect_bytes

    inspect_bytes(GSM8K_ROW)
    text = GSM8K_ROW.decode()
    assert scrub_string(text) == text


#: Real credential material, in the base64-ish runs a scanner actually meets.
#: Used BOTH to prove detection survives and as the negative control below.
REAL_CREDENTIAL_RUNS = {
    "aws secret access key": "wJalrXUtnFEMI7K9MDENGbPxRfiCYEXAMPLEKEY",
    "github pat body": "8a29Df63bC17eA94fE61dB82aC03eF75dA19",
    "jwt signature": "dBjftJeZ4CVPmB92K27uhbUJU1p1r_wW1gFWFOEjXk",
    "base64 private key": base64.b64encode(
        b"-----BEGIN RSA PRIVATE KEY-----\nMIIEowIBAAKCAQEA"
        + b"Zq7Yx3Kd91PvNmWcRt4Hs6Lb2Jg8Fn5Tz0Qa" * 2
        + b"\n-----END RSA PRIVATE KEY-----"
    ).decode(),
    "session cookie": "8Fk2mQxRv91TzPbNw4Lc7Hd3",
}

REAL_CREDENTIALS = {
    "aws access key id": b"AWS_ACCESS_KEY_ID=AKIA" + b"IOSFODNN7EXAMPLE",
    "aws id and secret, no separator":
        REAL_CREDENTIAL_RUNS["aws secret access key"].encode() + b"=AKIA" + b"IOSFODNN7EXAMPLE",
    "github pat": b"ghp_" + REAL_CREDENTIAL_RUNS["github pat body"].encode(),
    "jwt": b"eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0."
           + REAL_CREDENTIAL_RUNS["jwt signature"].encode(),
    "base64 private key": REAL_CREDENTIAL_RUNS["base64 private key"].encode(),
    # The relaxed plain-word keys keep firing when the VALUE is key-shaped.
    "cookie field holding a session":
        b"cookie = " + REAL_CREDENTIAL_RUNS["session cookie"].encode(),
    "token field holding a pat":
        json.dumps({"token": "ghp_" + REAL_CREDENTIAL_RUNS["github pat body"]}).encode(),
    "secret field holding a key":
        json.dumps({"secret": REAL_CREDENTIAL_RUNS["aws secret access key"]}).encode(),
}


@pytest.mark.parametrize("name", sorted(REAL_CREDENTIALS))
def test_real_credential_shapes_are_still_detected(name):
    """Detection is unchanged by the redact-instead-of-refuse policy.

    What changed is the RESPONSE, not the eye. Every shape here is still seen;
    a readable-text one additionally has its span replaced, so the value does
    not survive into the bytes that leave the machine.
    """
    from probe.sdk.secret_gate import redact_bytes

    raw = REAL_CREDENTIALS[name]
    clean, result = redact_bytes(raw)
    assert result.has_findings, name
    if result.rewritten:
        assert clean != raw and b"<redacted:" in clean


def test_diversity_floor_admits_no_real_secret():
    """NEGATIVE CONTROL for `_MIN_CANDIDATE_DISTINCT`.

    `low_diversity` is a SKIP: a run it calls uniform is never decoded and so
    can never become a finding. Raising the floor therefore admits MORE, which
    is what "set loose enough to admit a real secret" means for a floor of this
    shape. This test fails the moment the floor reaches the least diverse real
    credential we know of, and it fails if the floor stops rejecting the
    uniform runs it exists for.
    """
    from probe.tap_core import secrets

    distinct = {name: len(set(run)) for name, run in REAL_CREDENTIAL_RUNS.items()}
    assert secrets._MIN_CANDIDATE_DISTINCT < min(distinct.values()), distinct
    for name, run in REAL_CREDENTIAL_RUNS.items():
        assert not secrets.low_diversity(run), name
    for uniform in ("3" * 48, "A" * 300, "ab" * 24, "deadbeef" * 6):
        assert secrets.low_diversity(uniform) == (len(set(uniform)) < 6)
    assert secrets.low_diversity("3" * 48)


def test_both_halves_of_the_boundary_share_one_diversity_floor():
    """The gate and the tap scanner must not disagree about what a candidate is."""
    from probe.sdk import secret_gate
    from probe.tap_core import secrets

    assert secret_gate.low_diversity is secrets.low_diversity


# ---------------------------------------------------------------------------
# Redact instead of refuse
#
# The policy: a detected credential is REPLACED, never a reason to drop the
# upload. Refusing destroyed a researcher's artifact to protect a secret that
# was usually not there -- a GSM8K run lost a 500-row predictions file that way.
# ---------------------------------------------------------------------------


def _tar(payload: bytes) -> bytes:
    import tarfile

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w") as archive:
        info = tarfile.TarInfo("config.env")
        info.size = len(payload)
        archive.addfile(info, io.BytesIO(payload))
    return buf.getvalue()


def _zip(payload: bytes) -> bytes:
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w") as archive:
        archive.writestr("config.env", payload)
    return buf.getvalue()


#: (bytes, rewritten?, finding?) -- the whole contract on one table.
REDACTION_CASES = {
    "text with an AWS key":      (SECRET, True, True),
    "text with a PAT":           (b"ghp_" + b"8a29Df63bC17eA94fE61dB82aC03eF75dA19", True, True),
    "gsm8k cookie arithmetic":   (GSM8K_ROW, False, False),
    "tokenizer vocabulary row":  (VOCAB_DUMP, False, False),
    "gzip carrying a key":       (gzip.compress(SECRET), False, True),
    "tar carrying a key":        (_tar(SECRET), False, True),
    "zip carrying a key":        (_zip(SECRET), False, True),
    "non-utf8 bytes with a key": (b"\xff\xfe\x00" + SECRET, False, True),
    "clean training config":     (b'{"learning_rate": 0.003}', False, False),
}


@pytest.mark.parametrize("name", sorted(REDACTION_CASES))
def test_a_credential_is_never_a_reason_to_drop_the_upload(name):
    from probe.sdk.secret_gate import CredentialBlocked, redact_bytes

    raw, expect_rewrite, expect_finding = REDACTION_CASES[name]
    try:
        clean, result = redact_bytes(raw)
    except CredentialBlocked as exc:  # pragma: no cover - the thing under test
        pytest.fail(f"{name} was refused: {exc}")
    assert (clean != raw) is expect_rewrite, name
    assert result.has_findings is expect_finding, name
    if not expect_rewrite:
        # Byte-for-byte. Corrupting a checkpoint to hide a match is worse than
        # storing it with the finding recorded.
        assert clean == raw, name


@pytest.mark.parametrize("name", sorted(REDACTION_CASES))
def test_no_matched_value_ever_reaches_the_record(name):
    """The value-free contract, applied to the new fields as well as errors."""
    from probe.sdk.secret_gate import redact_bytes

    raw, _, _ = REDACTION_CASES[name]
    _, result = redact_bytes(raw)
    for rule in result.rules:
        assert KEY not in rule and "8a29Df63" not in rule
        assert rule.replace("-", "").isalnum(), rule


def test_prepare_upload_redacts_before_the_fingerprint(tmp_path):
    """THE ORDERING IS THE FEATURE.

    The server signs a sha256 and R2 verifies it independently, so the digest
    must describe the bytes that actually leave. Redacting after it would
    guarantee a checksum refusal.
    """
    from probe.sdk.hashing import fingerprint
    from probe.sdk.secret_gate import fingerprint_upload, prepare_upload

    source = tmp_path / "predictions.jsonl"
    source.write_bytes(SECRET)
    with prepare_upload(source) as prepared:
        assert prepared.was_redacted
        assert Path(prepared.path) != source
        uploaded = Path(prepared.path).read_bytes()
        assert KEY.encode() not in uploaded
        # The digest describes the REDACTED bytes, and both entry points agree.
        assert fingerprint(prepared.path) == fingerprint_upload(source)
        assert fingerprint(prepared.path)[0] != fingerprint(str(source))[0]
    assert not Path(prepared.path).exists()  # the staged copy does not linger
    assert source.read_bytes() == SECRET  # the researcher's file is untouched


def test_redaction_is_idempotent():
    """Re-reading a prepared file must not redact twice.

    Load-bearing: transport re-reads and re-inspects the bytes it is handed,
    and a second pass that changed anything would break the digest.
    """
    from probe.sdk.secret_gate import redact_bytes

    once, first = redact_bytes(SECRET)
    twice, second = redact_bytes(once)
    assert twice == once
    assert first.rewritten and not second.rewritten


def test_marker_receipt_lets_the_server_read_back_what_a_client_replaced():
    """No wire field and no trust: the marker is self-describing."""
    from probe.sdk.secret_gate import marker_receipt, redact_bytes

    clean, _ = redact_bytes(SECRET + b"\nghp_8a29Df63bC17eA94fE61dB82aC03eF75dA19\n")
    spans, rules = marker_receipt(clean)
    assert spans == 2
    assert set(rules) == {"aws-access-key-id", "github-token"}
    assert marker_receipt(b"learning_rate: 0.003") == (0, ())


def test_nested_findings_are_not_dropped_when_the_outer_text_is_rewritten():
    """A credential `redact` could not reach must still reach the RECORD.

    `inspect_bytes` recurses into base64 and containers, so it sees things a
    single pass over the outer text cannot. Reporting only the outer rules left
    the nested credential in the uploaded bytes AND absent from the row -- the
    artifact would name one credential and ship two.
    """
    import base64
    import gzip

    from probe.sdk.secret_gate import inspect_bytes, redact_bytes

    nested = gzip.compress(b"ghp_" + b"A1b2C3d4E5f6G7h8I9j0K1l2M3n4O5p6Q7r8")
    raw = (
        'api_key = "Xy9f2Kq8ZpL4mN7bVc3R"\npayload = '
        + base64.b64encode(nested).decode()
        + "\n"
    ).encode()
    seen = set(inspect_bytes(raw).rules)
    clean, result = redact_bytes(raw)
    assert clean != raw, "the outer literal must still be replaced"
    assert seen - set(result.rules) == set(), f"dropped from the record: {seen - set(result.rules)}"
    assert "github-token" in result.rules


def test_an_unstaged_op_digest_matches_what_the_drainer_will_send():
    """`fingerprint` at enqueue and `read_upload` at drain must agree.

    They did not: enqueue hashed the REDACTED bytes while the drainer re-read
    the file unredacted, so `checked_upload` refused every unstaged op with
    "source changed since its fingerprint was taken" -- a guaranteed dead
    letter, which is the exact opposite of what this policy is for.
    """
    import hashlib

    from probe.sdk.hashing import fingerprint
    from probe.sdk.secret_gate import checked_upload, read_upload

    import tempfile

    source = Path(tempfile.mkdtemp()) / "notes.txt"
    source.write_bytes(b'api_key = "Xy9f2Kq8ZpL4mN7bVc3R"\n')
    digest, size = fingerprint(str(source))
    assert hashlib.sha256(read_upload(source)).hexdigest() == digest
    with checked_upload(source, digest=digest, size=size):
        pass  # must not raise


def test_the_researcher_is_told_their_bytes_were_rewritten(tmp_path):
    """The row records it, but the person running the upload should not have
    to go and look."""
    from probe.sdk.secret_gate import ArtifactRedactedWarning, prepare_upload

    source = tmp_path / "preds.jsonl"
    source.write_bytes(SECRET)
    with pytest.warns(ArtifactRedactedWarning, match="NOT byte-identical"):
        with prepare_upload(source) as prepared:
            assert prepared.was_redacted


# The #2000 security review (HIGH-2, MED-2): benign files `log_artifact` used to
# rewrite. Their bytes must go up unchanged.
_REVIEW3_BENIGN_FILES = {
    "rows.jsonl": ('{"source":"https://huggingface.co","id":"a1b2c3","n_tokens":123456,"label":"positive",'
                   '"split":"train","annotator":"worker-17","score":0.9321,"created":"2026-09-01T12:00:00Z",'
                   '"reviewer":"alice@lab.org"}\n') * 3,
    "settings-template.xml": "<settings><servers><server><id>central</id><username>{user}</username>"
                             "<password>{password}</password></server></servers></settings>\n",
    "README.md": "Set it in `~/.m2/settings.xml` as `<password>...</password>`.\n",
    "client_messages.py": "class Db:\n    adminPassword = _messages.StringField(1)\n    sslKeyPassword = _messages.StringField(7)\n",
    "notes.txt": 'cfg.get("secret_name", "prod-db-2")\n',
    "ci-netrc.sh": 'printf "machine github.com login ci password $GH_TOKEN\\n" > ~/.netrc\n',
}


@pytest.mark.parametrize("fname", list(_REVIEW3_BENIGN_FILES))
def test_review3_benign_artifacts_upload_byte_identical(fname, client, app, tmp_path):
    from tests.conftest import open_run

    path = tmp_path / fname
    path.write_text(_REVIEW3_BENIGN_FILES[fname])
    run = open_run(client, experiment="e-review3", name="r")
    run.log_artifact(fname, path=str(path), sync=True)
    original = _REVIEW3_BENIGN_FILES[fname].encode()
    bodies = [request.content or b"" for request in app.requests]
    assert any(body == original for body in bodies), f"{fname}: uploaded bytes were rewritten"
    assert not any(b"<redacted:" in body for body in bodies if len(body) < 4096)
