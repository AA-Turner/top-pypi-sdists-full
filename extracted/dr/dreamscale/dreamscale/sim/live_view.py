"""Open a native window for a hosted run. The viewer subprocess receives JPEG frames only."""

from __future__ import annotations

import os
import struct
import subprocess
import sys
import tempfile
import threading
import time
from contextlib import suppress
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from dreamscale.config import API_KEY_ENV, LEGACY_API_KEY_ENV

_MAX_FRAME_BYTES = 256 * 1024
_HEADER_BYTES = 8
_MAX_FRAME_AGE_S = 2.0
_VISIBLE_INTERVAL_MS = 30
_TITLE = "Dreamscale RoboLab sim"


class LiveView:
    def __init__(self, api_url: str, api_key: str, run_id: str) -> None:
        url = urlsplit(api_url)
        self._url = urlunsplit(("wss" if url.scheme == "https" else "ws", url.netloc,
                               f"/v1/sim-runs/{run_id}/preview", "", ""))
        self._api_key = api_key
        self._stop = threading.Event()
        self._dir = tempfile.TemporaryDirectory(prefix="dreamscale-preview-")
        self._process: subprocess.Popen | None = None
        self._thread = threading.Thread(target=self._receive, daemon=True, name="sim-live-view")
        self._thread.start()

    def _receive(self) -> None:
        from websockets.exceptions import WebSocketException
        from websockets.sync.client import connect

        path = Path(self._dir.name) / "frame.jpg"
        incoming = path.with_suffix(".part")
        while not self._stop.is_set():
            try:
                with connect(
                    self._url, additional_headers={"Authorization": f"Bearer {self._api_key}"},
                    open_timeout=2, close_timeout=0.25, max_size=_MAX_FRAME_BYTES,
                    max_queue=1, compression=None,
                ) as socket:
                    while not self._stop.is_set():
                        if self._process is not None and self._process.poll() is not None:
                            return  # closing the window only stops the preview
                        try:
                            frame = socket.recv(timeout=0.25)
                        except TimeoutError:
                            continue
                        if not isinstance(frame, bytes) or len(frame) <= _HEADER_BYTES:
                            continue
                        captured_at, = struct.unpack("!d", frame[:_HEADER_BYTES])
                        age = time.time() - captured_at
                        if not -1 <= age <= _MAX_FRAME_AGE_S:
                            continue
                        incoming.write_bytes(frame[_HEADER_BYTES:])
                        incoming.replace(path)
                        if self._process is None:
                            env = {k: v for k, v in os.environ.items()
                                   if k not in (API_KEY_ENV, LEGACY_API_KEY_ENV)}
                            self._process = subprocess.Popen(
                                [sys.executable, "-m", "dreamscale.sim.live_view", str(path)],
                                stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                                stderr=subprocess.DEVNULL, env=env,
                            )
            except (OSError, WebSocketException, TimeoutError):
                self._stop.wait(1)

    def close(self) -> None:
        self._stop.set()
        self._thread.join(timeout=3)
        if self._process is not None and self._process.poll() is None:
            self._process.terminate()
            try:
                self._process.wait(timeout=1)
            except subprocess.TimeoutExpired:
                self._process.kill()
                self._process.wait()
        self._dir.cleanup()


def _show(path: Path) -> None:
    import cv2

    from dreamscale.sim.viewer_window import open_window

    open_window(cv2, _TITLE)
    last_write: int | None = None
    try:
        while True:
            mtime = path.stat().st_mtime_ns
            if mtime != last_write:
                frame = cv2.imread(str(path))
                if frame is not None:
                    cv2.imshow(_TITLE, frame)
                    last_write = mtime
            if cv2.waitKey(_VISIBLE_INTERVAL_MS) in (27, ord("q")):
                break
            if cv2.getWindowProperty(_TITLE, cv2.WND_PROP_VISIBLE) < 1:
                break
    except (cv2.error, FileNotFoundError):
        pass
    finally:
        with suppress(cv2.error):
            cv2.destroyWindow(_TITLE)


if __name__ == "__main__":
    _show(Path(sys.argv[1]))
