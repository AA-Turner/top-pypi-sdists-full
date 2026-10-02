"""#2073: a presigned upload refused by the server it points at fails THAT
upload, never this machine's credential.

A presigned PUT carries no Authorization header -- the URL (or its capability
header) is the authorization. So a 401/403 on it says the signed capability was
refused: expired, or minted by another server. The 2.10 staging run hit the
second: a self-host install whose `public_base_url` still named Probe's hosted
API handed out upload URLs there, the hosted API refused every one ("invalid
upload capability"), and the SDK read each 401 as a refused credential. It
paused all delivery of the run -- 29% of its points arrived, and the terminal
status never did.
"""

from __future__ import annotations

import httpx
import pytest

from probe.sdk import errors
from probe.sdk.client import Client
from probe.sdk.journal import Journal, classify
from tests.served_fake_app import serve
from tests.test_outbox_credential_stamp import STORED_B, _login


class _OtherServer:
    """The server a misconfigured install's upload URLs point at: it refuses
    every PUT, as Probe's hosted API refused the install's capabilities."""

    def __init__(self, status: int = 401) -> None:
        self.status = status
        self.puts: list[httpx.Request] = []

    def handler(self, request: httpx.Request) -> httpx.Response:
        self.puts.append(request)
        return httpx.Response(self.status, json={"detail": "invalid upload capability"})


@pytest.mark.parametrize("status", [401, 403])
def test_a_refused_presigned_upload_fails_only_that_upload(app, tmp_path, monkeypatch, status):
    other = _OtherServer(status)
    root = tmp_path / "outbox"
    output = tmp_path / "metrics.json"
    output.write_text('{"loss": 0.25}')
    with serve(app) as url, serve(other) as elsewhere:
        app.upload_base = elsewhere
        monkeypatch.setenv("PROBE_BASE_URL", url)
        _login(url, STORED_B)
        client = Client(spool_dir=root, async_writes=True, auto_drain=False)
        try:
            client.create_project("uploads", "Uploads", kind="general")
            run = client.run(project="uploads", name="r", heartbeat=False)
            run.log({"loss": 1.0}, step=0)
            run.log_artifact("metrics.json", path=str(output))
            for step in range(1, 4):
                run.log({"loss": 1.0 / (step + 1)}, step=step)
            run.finish(flush_timeout=5)
        finally:
            client.close()
        status_file = Journal.read_status(root) or {}

    assert other.puts, "the upload never reached the other server"
    assert all("authorization" not in r.headers for r in other.puts), "a bearer left for it"
    steps = sorted(p["step_index"] for p in app.metric_points_posted[run.id])
    assert steps == [0, 1, 2, 3], "the run's other writes waited behind the refused upload"
    assert app.runs[run.id]["status"] == "completed"
    assert not status_file.get("auth_blocked_since")
    assert not status_file.get("refused_fingerprints")
    # The upload itself failed, visibly: a reference row that says so (beside
    # the presign's pending row, which never completes).
    (failed,) = [
        a for a in app.artifacts[run.id] if a.get("name") == "metrics.json" and a.get("is_reference")
    ]
    assert failed["meta"]["upload"] == "failed"
    assert "UploadRefused" in failed["meta"]["upload_error"]


def test_a_presigned_put_refusal_is_its_own_error(tmp_path):
    """The transport names it: not an AuthError (no credential was sent), and
    the outbox classifies it permanent -- this upload fails, the queue goes on."""
    from probe.sdk.config import Settings
    from probe.sdk.transport import Transport

    def refuse(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, json={"detail": "invalid upload capability"})

    blob = tmp_path / "b.bin"
    blob.write_bytes(b"bytes")
    transport = Transport(
        Settings(base_url="https://install.example", token="probe_pat_x"),
        client=httpx.Client(transport=httpx.MockTransport(refuse)),
    )
    signed = "https://api.elsewhere.example/v1/artifact-upload-bytes?X-Amz-Signature=SECRET"
    with pytest.raises(errors.UploadRefused) as caught:
        transport.put_file(signed, str(blob))
    assert not isinstance(caught.value, (errors.AuthError, errors.ScopeError))
    assert caught.value.status == 401
    assert "api.elsewhere.example" in str(caught.value)
    assert "SECRET" not in str(caught.value)
    assert classify(caught.value) == "permanent"
    with pytest.raises(errors.UploadRefused):
        transport.put_url(signed, b"bytes")
    with blob.open("rb") as fh, pytest.raises(errors.UploadRefused):
        transport.put_fileobj(signed, fh, size=5)


def test_a_network_failure_never_prints_the_signed_address():
    """`put_url` put the whole presigned URL, signature included, in its error."""
    from probe.sdk.config import Settings
    from probe.sdk.transport import Transport

    def down(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("connection refused", request=request)

    transport = Transport(
        Settings(base_url="https://install.example", token="probe_pat_x"),
        client=httpx.Client(transport=httpx.MockTransport(down)),
        max_retries=0,
    )
    signed = "https://store.example/bucket/key?X-Amz-Signature=SECRET"
    with pytest.raises(errors.TransportError) as caught:
        transport.put_url(signed, b"bytes")
    assert "store.example/bucket/key" in str(caught.value)
    assert "SECRET" not in str(caught.value)

