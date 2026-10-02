"""Artifact callers see both local and server-side inspection limitations."""

import io
import warnings

import httpx
import pytest

from probe.sdk.config import Settings
from probe.sdk.secret_gate import ArtifactInspectionWarning
from probe.sdk.transport import Transport


def _send(transport, method, raw, tmp_path):
    url = "https://synthetic.invalid/upload"
    if method == "put_url":
        transport.put_url(url, raw)
    elif method == "put_file":
        source = tmp_path / "artifact.bin"
        source.write_bytes(raw)
        transport.put_file(url, str(source))
    else:
        transport.put_fileobj(url, io.BytesIO(raw), size=len(raw))


def test_direct_put_url_sends_opaque_bytes_without_a_local_scan(monkeypatch):
    """Pinned bytes are not scanned again here: a scan could only warn, and
    the server inspects the upload and answers with its own warning, which the
    next test pins."""
    import warnings

    monkeypatch.delenv("PROBE_ARTIFACT_OPAQUE_POLICY", raising=False)
    raw = b"\xff\x00\x80"
    sent = []

    def respond(request):
        sent.append(request.read())
        return httpx.Response(200)

    with httpx.Client(transport=httpx.MockTransport(respond)) as http:
        transport = Transport(Settings(base_url="https://synthetic.invalid"), client=http, surface="mcp")
        with warnings.catch_warnings():
            warnings.simplefilter("error", ArtifactInspectionWarning)
            transport.put_url("https://synthetic.invalid/upload", raw)
    assert sent == [raw]


@pytest.mark.parametrize("method", ["put_url", "put_file", "put_fileobj"])
def test_successful_upload_surfaces_server_warning_without_echoing_header(tmp_path, method):
    raw = b"ordinary checkpoint description\n"
    sent = []
    untrusted_header = "password=FabricatedHeaderOnly123! " + "x" * 4000

    def respond(request):
        sent.append(request.read())
        return httpx.Response(200, headers={"X-Probe-Inspection-Warning": untrusted_header})

    with httpx.Client(transport=httpx.MockTransport(respond)) as http:
        transport = Transport(Settings(base_url="https://synthetic.invalid"), client=http, surface="mcp")
        with pytest.warns(ArtifactInspectionWarning, match="cannot confirm") as captured:
            _send(transport, method, raw, tmp_path)
    assert sent == [raw]
    assert len(captured) == 1
    message = str(captured[0].message)
    assert "FabricatedHeaderOnly123" not in message
    assert len(message) < 500


@pytest.mark.parametrize("method", ["put_url", "put_file", "put_fileobj"])
def test_fully_inspected_upload_without_server_warning_is_quiet(tmp_path, method):
    with httpx.Client(transport=httpx.MockTransport(lambda _: httpx.Response(200))) as http:
        transport = Transport(Settings(base_url="https://synthetic.invalid"), client=http, surface="mcp")
        with warnings.catch_warnings(record=True) as captured:
            warnings.simplefilter("always")
            _send(transport, method, b"ordinary checkpoint description\n", tmp_path)
    assert not captured
