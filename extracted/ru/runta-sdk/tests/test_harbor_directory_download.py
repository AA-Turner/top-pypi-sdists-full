"""Harbor forwards directory merges to the real SDK transfer implementation."""

from types import SimpleNamespace
from unittest.mock import AsyncMock

import pytest

pytest.importorskip("harbor")
from runta_harbor.environment import RuntaEnvironment, transfer_tar_filter  # noqa: E402

from runta import AsyncFileManager, AsyncRunta  # noqa: E402
from runta._internal import streaming_transfer as transfer  # noqa: E402
from test_download_dir_contents import make_archive  # noqa: E402
from test_streaming_transfer import _FakeSocket, _FakeSocketContext, _data_frame  # noqa: E402


@pytest.mark.asyncio
async def test_directory_download_forwards_callback_and_paths(tmp_path):
    files = SimpleNamespace(download_dir_contents=AsyncMock())
    env = object.__new__(RuntaEnvironment)
    env._runtime = SimpleNamespace(files=files)
    await env._runtime_download_dir("/logs/agent", tmp_path)
    files.download_dir_contents.assert_awaited_once_with(
        "/logs/agent",
        str(tmp_path),
        filter=transfer_tar_filter,
    )


@pytest.mark.asyncio
@pytest.mark.parametrize("empty", [False, True])
async def test_directory_download_real_sdk_merge(tmp_path, monkeypatch, empty):
    payload = tmp_path / "payload.tar"
    make_archive(
        payload,
        []
        if empty
        else [
            ("./nested/data", b"\x00\xff", ""),
            ("./replace", b"new", ""),
        ],
    )
    socket = _FakeSocket(
        [_data_frame("stdout", payload.read_bytes()), '{"type":"exit","code":0}', None]
    )
    monkeypatch.setattr(
        transfer, "_async_socket", lambda *a, **kw: _FakeSocketContext(socket)
    )
    target = tmp_path / "target"
    target.mkdir()
    (target / "keep").write_text("keep")
    (target / "replace").write_text("old")
    async with AsyncRunta(endpoint="http://test", token="test") as client:
        runtime = SimpleNamespace(id="runtime", _client=client)
        runtime.files = AsyncFileManager._from_owner(runtime)
        env = object.__new__(RuntaEnvironment)
        env._runtime = runtime
        await env._runtime_download_dir("/logs/agent", target)
    assert (target / "keep").read_text() == "keep"
    assert (target / "replace").read_text() == ("old" if empty else "new")
    assert not (target / "agent").exists()
    if not empty:
        assert (target / "nested/data").read_bytes() == b"\x00\xff"


@pytest.mark.asyncio
async def test_directory_download_propagates_failure(tmp_path):
    files = SimpleNamespace(
        download_dir_contents=AsyncMock(side_effect=ConnectionError("interrupted"))
    )
    env = object.__new__(RuntaEnvironment)
    env._runtime = SimpleNamespace(files=files)
    (tmp_path / "keep").write_text("keep")
    with pytest.raises(ConnectionError):
        await env._runtime_download_dir("/logs/agent", tmp_path)
    assert (tmp_path / "keep").read_text() == "keep"
