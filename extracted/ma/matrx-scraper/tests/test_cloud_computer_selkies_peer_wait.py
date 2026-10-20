"""The Cloud Computer's Selkies app never blocks its event loop (2026-10-17).

Selkies 1.6.2 waits for the browser's peer with ``time.sleep(2)`` inside an
async error handler, once for the video peer and once for the audio peer. That
event loop also serves the screen page, its assets, the signalling handshake and
HELLO, so until a viewer registered every one of those waited for the next
4 s tick: live, the page took ~15 s from entry to socket and ~4 s more to
register. The image patch (``patch-selkies-web.py``) swaps the blocking sleep
for a non-blocking wait that starts the session as soon as the peer registers.

This runs the upstream handler text verbatim, then the same text through the
patcher's real edits, in one asyncio loop beside a ticker that measures how long
the loop was blocked.
"""
from __future__ import annotations

import asyncio
import importlib.util
import logging
import time
from pathlib import Path
from types import SimpleNamespace

PATCHER = Path(__file__).resolve().parents[1] / "docker" / "cloud-computer" / "patch-selkies-web.py"

# Selkies 1.6.2 selkies_gstreamer/__main__.py, lines 535-551, verbatim.
UPSTREAM = """\
    # Handle errors from the signalling server
    async def on_signalling_error(e):
       if isinstance(e, WebRTCSignallingErrorNoPeer):
           # Waiting for peer to connect, retry in 2 seconds.
           time.sleep(2)
           await signalling.setup_call()
       else:
           logger.error("signalling error: %s", str(e))
           app.stop_pipeline()
    async def on_audio_signalling_error(e):
       if isinstance(e, WebRTCSignallingErrorNoPeer):
           # Waiting for peer to connect, retry in 2 seconds.
           time.sleep(2)
           await audio_signalling.setup_call()
       else:
           logger.error("signalling error: %s", str(e))
           audio_app.stop_pipeline()
"""


class NoPeer(Exception):
    pass


def _patcher():
    spec = importlib.util.spec_from_file_location("patch_selkies_web", PATCHER)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def _handlers(fragment: str, server: SimpleNamespace, calls: list[tuple[str, float]]):
    def peer(name: str, peer_id: int) -> SimpleNamespace:
        async def setup_call() -> None:
            calls.append((name, time.monotonic()))

        return SimpleNamespace(peer_id=peer_id, setup_call=setup_call)

    source = (
        "def build(time, asyncio, WebRTCSignallingErrorNoPeer, signalling, audio_signalling,"
        " app, audio_app, logger, server):\n"
        + fragment
        + "    return on_signalling_error, on_audio_signalling_error\n"
    )
    namespace: dict = {}
    exec(compile(source, "selkies_main_fragment", "exec"), namespace)
    stub = SimpleNamespace(stop_pipeline=lambda: None)
    return namespace["build"](
        time, asyncio, NoPeer, peer("video", 1), peer("audio", 3), stub, stub,
        logging.getLogger("selkies-fragment"), server,
    )


async def _run(fragment: str) -> tuple[float, float]:
    """(longest loop stall, session start after the browser's peers registered)."""
    server = SimpleNamespace(peers={})
    calls: list[tuple[str, float]] = []
    video, audio = _handlers(fragment, server, calls)
    stall = 0.0
    done = asyncio.Event()

    async def ticker() -> None:
        nonlocal stall
        last = time.monotonic()
        while not done.is_set():
            await asyncio.sleep(0.01)
            now = time.monotonic()
            stall = max(stall, now - last)
            last = now

    async def browser() -> float:
        await asyncio.sleep(0.3)
        server.peers["1"] = server.peers["3"] = object()
        return time.monotonic()

    tick = asyncio.create_task(ticker())
    joined = asyncio.create_task(browser())
    await asyncio.wait_for(asyncio.gather(video(NoPeer()), audio(NoPeer())), timeout=10)
    registered = await joined
    done.set()
    await tick
    started = max(at for _, at in calls)
    return stall, max(0.0, started - registered)


def test_upstream_handler_blocks_the_loop() -> None:
    """The harness sees the defect: upstream blocks the loop for the full sleep."""
    stall, _ = asyncio.run(_run(UPSTREAM))
    assert stall >= 1.9


def test_patched_handler_never_blocks_and_starts_on_register() -> None:
    patcher = _patcher()
    # Only the edits for this fragment; the full-file run checks every edit once.
    edits = [e for e in patcher.PACKAGE_EDITS["__main__.py"] if e[0] in UPSTREAM]
    patched = patcher.patch_text("__main__.py", UPSTREAM, edits)
    assert "time.sleep" not in patched
    stall, start_after_register = asyncio.run(_run(patched))
    assert stall < 0.25
    assert start_after_register < 0.2
