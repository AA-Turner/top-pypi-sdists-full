from pathlib import Path

import httpx
import pytest

from probe.sdk.client import Client
from probe.sdk.config import Settings
from probe.sdk.transport import Transport


@pytest.mark.parametrize("declared", [True, False])
def test_streamed_download_refuses_oversized_bytes_and_removes_partial(tmp_path, declared):
    settings = Settings(base_url="http://test", token="test")

    class Chunks(httpx.SyncByteStream):
        def __iter__(self):
            yield b"first"
            yield b"second"

    def respond(request):
        if request.url.path.endswith("/download"):
            return httpx.Response(200, json={"download_url": "http://blob.test/data"})
        return httpx.Response(200, headers={"content-length": "11"} if declared else {}, stream=Chunks())

    transport = Transport(settings=settings, client=httpx.Client(base_url=settings.base_url,
                                                               transport=httpx.MockTransport(respond)))
    client = Client(settings=settings, transport=transport, async_writes=False, auto_drain=False,
                    spool_dir=str(tmp_path / "outbox"))
    target = tmp_path / "download.partial"
    with pytest.raises(ValueError, match="byte budget"):
        client.download_artifact_to("artifact-a", str(target), max_bytes=5)
    assert not target.exists()
    client.close()


def test_bounded_download_returns_hash_of_written_bytes(tmp_path):
    settings = Settings(base_url="http://test")
    transport = Transport(settings=settings, client=httpx.Client(transport=httpx.MockTransport(
        lambda _: httpx.Response(200, content=b"abc"))))
    target = tmp_path / "download"
    size, digest = transport.download_to("http://blob.test/data", str(target), max_bytes=3)
    assert size == 3 and len(digest) == 64 and Path(target).read_bytes() == b"abc"
    transport.close()
