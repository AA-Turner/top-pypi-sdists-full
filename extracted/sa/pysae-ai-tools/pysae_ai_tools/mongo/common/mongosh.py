"""Run a JavaScript snippet against a MongoDB deployment through the mongosh CLI.

The connection URI is handed to mongosh through the environment
(``PYSAE_MONGO_URI``) and consumed inside the script with ``new Mongo(uri)``,
never as a positional argument — so the secret never surfaces in the process
list (``ps``/``/proc``).

mongosh stdout is streamed line by line: lines prefixed with ``__PROGRESS__`` are
routed to an optional ``on_progress`` callback (for live progress display) and
stripped from the returned payload; everything else is accumulated and returned.
"""

import os
import shutil
import subprocess
import threading
from collections.abc import Callable

MONGOSH_BIN = "mongosh"
URI_ENV = "PYSAE_MONGO_URI"
OPTS_ENV = "PYSAE_MONGO_OPTS"
PROGRESS_PREFIX = "__PROGRESS__"

INSTALL_HINT = "mongosh not found — run: pysae-ai-tools tools install mongo-tools"


class MongoshError(RuntimeError):
    """mongosh is missing, exited non-zero, timed out, or produced unusable output."""


def _terminate(proc: "subprocess.Popen[str]") -> None:
    """Stop mongosh cleanly: SIGTERM, then SIGKILL if it lingers."""
    if proc.poll() is not None:
        return
    proc.terminate()
    try:
        proc.wait(timeout=5)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait()


def run_mongosh(
    script: str,
    uri: str,
    *,
    opts_json: str = "{}",
    timeout: float = 600.0,
    on_progress: Callable[[str], None] | None = None,
) -> str:
    """Execute ``script`` with mongosh (``--nodb``) and return its stdout payload.

    ``opts_json`` is exposed to the script as ``PYSAE_MONGO_OPTS`` so callers can
    pass structured options (db filters, thresholds) without string-splicing them
    into the JavaScript. ``on_progress`` receives the JSON body of each
    ``__PROGRESS__`` line as it is emitted.
    """
    exe = shutil.which(MONGOSH_BIN)
    if not exe:
        raise MongoshError(INSTALL_HINT)

    env = {**os.environ, URI_ENV: uri, OPTS_ENV: opts_json}
    try:
        proc = subprocess.Popen(
            [exe, "--nodb", "--quiet", "--norc", "--eval", script],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            bufsize=1,
        )
    except FileNotFoundError as exc:
        raise MongoshError(INSTALL_HINT) from exc

    timed_out = threading.Event()

    def _kill() -> None:
        timed_out.set()
        proc.kill()

    timer = threading.Timer(timeout, _kill)
    timer.start()
    payload: list[str] = []
    try:
        assert proc.stdout is not None
        for line in proc.stdout:
            text = line.rstrip("\n")
            if text.startswith(PROGRESS_PREFIX):
                if on_progress is not None:
                    on_progress(text[len(PROGRESS_PREFIX) :])
            else:
                payload.append(text)
        proc.wait()
    except (KeyboardInterrupt, BrokenPipeError):
        _terminate(proc)
        raise
    finally:
        timer.cancel()

    stderr = proc.stderr.read() if proc.stderr is not None else ""
    if timed_out.is_set():
        raise MongoshError(f"mongosh timed out after {timeout:.0f}s")
    if proc.returncode:
        detail = (stderr or "\n".join(payload)).strip()
        raise MongoshError(f"mongosh exited {proc.returncode}: {detail[:2000]}")
    return "\n".join(payload)
