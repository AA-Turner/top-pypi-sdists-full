from __future__ import annotations

import asyncio
import base64
import json
import subprocess
import time
from unittest.mock import patch

import pytest
from websockets.asyncio.server import serve
from websockets.exceptions import ConnectionClosed

from runta._internal import streaming_transfer as transfer


@pytest.mark.asyncio
@pytest.mark.parametrize("sync", [False, True])
async def test_directory_upload_waits_for_close_stdin_before_exit(tmp_path, sync):
    source = tmp_path / "source"
    (source / "nested").mkdir(parents=True)
    payload = bytes(range(256)) * 128
    (source / "nested" / "binary").write_bytes(payload)
    (source / "message").write_text("complete directory upload\n")
    failures = []
    eof_received = []

    async def handler(ws):
        frame = json.loads(await ws.recv())
        assert frame["type"] == "start"
        process = await asyncio.create_subprocess_exec(
            frame["command"],
            *frame["args"],
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.DEVNULL,
            stderr=asyncio.subprocess.PIPE,
        )

        async def receive():
            async for raw in ws:
                message = json.loads(raw)
                if message["type"] == "stdin":
                    process.stdin.write(base64.b64decode(message["data_base64"]))
                    await process.stdin.drain()
                elif message["type"] == "close_stdin":
                    eof_received.append(True)
                    process.stdin.close()
                    return

        receiver = asyncio.create_task(receive())
        try:
            code = await process.wait()
            receiver.cancel()
            await asyncio.gather(receiver, return_exceptions=True)
            errors = await process.stderr.read()
            await ws.send(
                json.dumps(
                    {"type": "stderr", "data_base64": base64.b64encode(errors).decode()}
                )
            )
            await ws.send(json.dumps({"type": "exit", "code": code}))
            await ws.close()
        except ConnectionClosed:
            pass
        finally:
            receiver.cancel()
            await asyncio.gather(receiver, return_exceptions=True)
            if process.returncode is None:
                process.kill()
            await process.communicate()

    original_sync = transfer._send_close_stdin
    original_async = transfer._async_send_close_stdin

    def delayed_sync(send):
        time.sleep(0.25)
        original_sync(send)

    async def delayed_async(send):
        await asyncio.sleep(0.25)
        await original_async(send)

    async with serve(handler, "127.0.0.1", 0) as server:
        endpoint = f"http://127.0.0.1:{server.sockets[0].getsockname()[1]}"
        with (
            patch.object(transfer, "_send_close_stdin", delayed_sync),
            patch.object(transfer, "_async_send_close_stdin", delayed_async),
        ):
            for iteration in range(20):
                destination = tmp_path / f"destination-{iteration}"
                try:
                    if sync:
                        await asyncio.to_thread(
                            transfer.upload_path,
                            endpoint,
                            "test",
                            "runtime",
                            source,
                            str(destination),
                            timeout=2,
                            attempts=1,
                        )
                    else:
                        await transfer.async_upload_path(
                            endpoint,
                            "test",
                            "runtime",
                            source,
                            str(destination),
                            timeout=2,
                            attempts=1,
                        )
                except ConnectionClosed as exc:
                    failures.append(type(exc).__name__)
                # A successful extraction alone must not be reported as an upload failure.
                assert (destination / "nested" / "binary").read_bytes() == payload
                assert (
                    destination / "message"
                ).read_text() == "complete directory upload\n"
    assert not failures, f"upload falsely failed {len(failures)}/20 times: {failures}"
    assert len(eof_received) == 20
    assert not list(tmp_path.glob(".*.runta-stage-*"))
    assert not list(tmp_path.glob(".*.runta-backup-*"))


def test_invalid_archive_waits_for_eof_and_preserves_existing_directory(tmp_path):
    destination = tmp_path / "destination"
    destination.mkdir()
    (destination / "keep").write_text("existing content")
    process = subprocess.Popen(
        ["sh", "-c", transfer._UPLOAD_DIRECTORY_SCRIPT, "_", str(destination)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    try:
        process.stdin.write(b"not a tar archive" * 1024)
        process.stdin.flush()
        time.sleep(0.25)
        assert process.poll() is None
        process.stdin.close()
        process.stdin = None
        _, errors = process.communicate(timeout=5)
        assert process.returncode != 0 and errors
        assert (destination / "keep").read_text() == "existing content"
        assert not list(tmp_path.glob(".*.runta-stage-*"))
        assert not list(tmp_path.glob(".*.runta-backup-*"))
    finally:
        if process.poll() is None:
            process.kill()
        process.communicate()
