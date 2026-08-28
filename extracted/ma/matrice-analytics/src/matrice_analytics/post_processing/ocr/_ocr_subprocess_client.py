"""Parent-side client for the isolated OCR worker subprocess.

:class:`OcrSubprocessClient` duck-types ``LicensePlateRecognizer.run`` so
``license_plate_monitoring._run_ocr`` can use it transparently. It spawns the
worker (:mod:`_ocr_subprocess_worker`) with the OCR venv's python, validates a
GPU-ready handshake with multiple retries, serves requests over the worker's
stdin/stdout, restarts the worker if it crashes, and -- when the GPU path is
permanently unavailable -- raises :class:`OcrSubprocessUnavailable` so the
caller can fall back to the in-process CPU recognizer.

Only stdlib + numpy are imported here (any numpy version): the parent process
on Thor runs numpy>=2 and must never import ``onnxruntime``/``fast_plate_ocr``.
"""

from __future__ import annotations

import atexit
import contextlib
import logging
import os
import select
import subprocess
import threading
import time
from typing import Dict, List, Optional, Sequence, Tuple

import numpy as np

from . import _ocr_ipc

logger = logging.getLogger(__name__)

_DEFAULT_OCR_PYTHON = "/opt/ocr-venv/bin/python3"
_WORKER_FILENAME = "_ocr_subprocess_worker.py"

# ANA-21: how long the FIRST FRAME can spend bringing this worker up.
#
# Filed as its own item rather than under ANA-16, which this was found while
# investigating: ANA-16 is "async def process() contains zero awaits", a different
# claim about a different mechanism (see tests/unit/test_lpr_first_frame_cost.py for
# why that premise does not hold). An ID in a comment outlives the PR that wrote it,
# so it has to name the thing it actually describes.
#
# start() runs inline on the frame that first needs OCR. The old numbers made that
# stall unbounded in practice: ready_timeout was 60 s *per attempt*, and start()
# makes len(startup_retry_delays)+1 = 4 attempts with 1+3+5 s between them, so the
# real worst case was 4*60 + 9 = 249 s of dead frame -- not the 60 s the parameter
# reads like.
#
# The healthy path is nowhere near either number. The CUDA execution provider builds
# this model in ~3 s (measured on the H100 LPR deployment; see
# license_plate_monitoring._preferred_ocr_providers), so 15 s per attempt is 5x
# headroom over a known-good start, and 20 s total is the hard cap on the stall.
# Exceeding the budget is not a loss of GPU OCR: the frame falls back to the
# in-process CPU recognizer, the failure stays classified transient, and the
# client's own reinit_cooldown retries the whole sequence on a later frame -- off
# this frame's critical path.
#
# The TensorRT provider is the known exception at >120 s (engine rebuild, no cache),
# which is why it is already opt-in via MATRICE_OCR_ENABLE_TRT. A deployment that
# turns it on must raise these two with it, hence the env overrides.
_ENV_READY_TIMEOUT_S = "MATRICE_OCR_READY_TIMEOUT_S"
_ENV_STARTUP_BUDGET_S = "MATRICE_OCR_STARTUP_BUDGET_S"
_DEFAULT_READY_TIMEOUT_S = 15.0
_DEFAULT_STARTUP_BUDGET_S = 20.0


def _env_float(name: str, default: float) -> float:
    """Positive float from *name*, or *default*. Never raises on junk input."""
    raw = (os.environ.get(name) or "").strip()
    if not raw:
        return default
    try:
        value = float(raw)
    except ValueError:
        logger.warning("Ignoring %s=%r (not a number); using %.1fs", name, raw, default)
        return default
    if value <= 0:
        logger.warning("Ignoring %s=%r (must be > 0); using %.1fs", name, raw, default)
        return default
    return value


# Substrings (lowercased) in a startup error / worker stderr that mark a
# NON-recoverable failure: the OCR stack or the interpreter is missing.
# Anything else (model-download 5xx, timeouts, network blips) is treated as
# transient and left recoverable so a one-off hiccup can't disable OCR for the
# whole container lifetime.
_PERMANENT_FAILURE_MARKERS = (
    "onnx runtime is not installed",
    "onnxruntime is not installed",
    "no module named",
    "modulenotfounderror",
    "importerror",
    "no such file or directory",
)


def _is_permanent_failure(text: str) -> bool:
    """True if ``text`` (exception + worker stderr) names a non-recoverable cause."""
    t = (text or "").lower()
    return any(marker in t for marker in _PERMANENT_FAILURE_MARKERS)


class OcrSubprocessUnavailable(RuntimeError):  # noqa: N818 - intentional public name
    """Raised when the GPU OCR subprocess cannot serve requests.

    Signals the caller to fall back to the in-process CPU OCR path.
    """


class OcrSubprocessClient:
    """Manages one long-lived OCR worker subprocess (per parent process)."""

    def __init__(
        self,
        model_name: str = "cct-s-v1-global-model",
        providers: Optional[Sequence[str]] = None,
        python_exe: Optional[str] = None,
        ready_timeout: Optional[float] = None,
        request_timeout: float = 15.0,
        startup_retry_delays: Sequence[float] = (1.0, 3.0, 5.0),
        reinit_cooldown: float = 30.0,
        startup_budget_s: Optional[float] = None,
    ) -> None:
        self.model_name = model_name
        self.providers: List[str] = list(providers or [])
        self.python_exe = python_exe or os.environ.get("MATRICE_OCR_PYTHON", _DEFAULT_OCR_PYTHON)
        # Self-heal: when auto-venv is enabled and no usable interpreter was
        # provided (env unset or the path is missing), build/repair the isolated
        # OCR venv at runtime and point the worker at it. Opt-in so pre-baked
        # images (which set MATRICE_OCR_PYTHON to a real venv) are untouched.
        if os.environ.get("MATRICE_OCR_AUTO_VENV") == "1":
            preset = python_exe or os.environ.get("MATRICE_OCR_PYTHON")
            if not preset or not os.path.exists(self.python_exe):
                bootstrapped = self._bootstrap_venv_python()
                if bootstrapped:
                    self.python_exe = bootstrapped
        # An explicit argument wins (the tests pass one); otherwise the env override,
        # otherwise the frame-budget default above.
        self.ready_timeout = (
            float(ready_timeout)
            if ready_timeout is not None
            else _env_float(_ENV_READY_TIMEOUT_S, _DEFAULT_READY_TIMEOUT_S)
        )
        self.startup_budget_s = (
            float(startup_budget_s)
            if startup_budget_s is not None
            else _env_float(_ENV_STARTUP_BUDGET_S, _DEFAULT_STARTUP_BUDGET_S)
        )
        self.request_timeout = request_timeout
        self.startup_retry_delays = list(startup_retry_delays)
        self.reinit_cooldown = reinit_cooldown

        self._proc: Optional[subprocess.Popen] = None
        self._lock = threading.Lock()
        self._request_counter = 0
        self._permanently_unavailable = False
        self._last_start_attempt = 0.0
        self.health: Optional[dict] = None

    # -- lifecycle ---------------------------------------------------------
    def _bootstrap_venv_python(self) -> Optional[str]:
        """Create/repair the isolated OCR venv and return its python, or None.

        Lazy import keeps construction cheap and the dependency one-directional
        (the bootstrap is stdlib-only and never imports onnxruntime). Never
        raises -- a None return leaves ``python_exe`` at its default so startup
        fails into the in-process fallback, unchanged.
        """
        try:
            from ._ocr_venv_bootstrap import ensure_ocr_venv

            return ensure_ocr_venv(self.model_name)
        except Exception as exc:  # noqa: BLE001 - best effort
            logger.warning("OCR venv bootstrap unavailable: %s", exc)
            return None

    def _worker_path(self) -> str:
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), _WORKER_FILENAME)

    def _child_env(self) -> dict:
        env = os.environ.copy()
        env["PYTHONUNBUFFERED"] = "1"
        # Point the fast_plate_ocr hub cache at the pre-baked location so the
        # worker never hits the network at startup.
        ocr_home = os.environ.get("MATRICE_OCR_HOME")
        if ocr_home:
            env["HOME"] = ocr_home
        return env

    def _spawn_once(self) -> subprocess.Popen:
        argv = [
            self.python_exe,
            self._worker_path(),
            "--model",
            self.model_name,
            "--providers",
            ",".join(self.providers),
        ]
        logger.debug("Spawning OCR worker: %s", argv)
        return subprocess.Popen(  # nosec B603 - fixed argv, no shell
            argv,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            bufsize=0,
        )

    def start(self) -> bool:
        """Bring up the worker with retries. Returns True if GPU-ready.

        A *permanent* failure (missing onnxruntime / interpreter) sets
        ``_permanently_unavailable`` so we never retry. A *transient* failure
        (model-download 5xx, timeout, network blip) is left recoverable: the
        full retry sequence is rate-limited by ``reinit_cooldown`` so a later
        call -- e.g. once the model is cached -- can bring OCR up without
        stalling every request in between.

        The whole sequence -- every attempt and every inter-attempt sleep -- is
        bounded by ``startup_budget_s``, because this runs inline on the frame that
        first needs OCR. Before ANA-21 only each individual attempt was bounded, so
        the frame could wait 4 * ready_timeout + the sleeps.
        """
        with self._lock:
            if self._permanently_unavailable:
                return False
            if self._is_alive():
                return True
            # Rate-limit (re)start sequences: a recoverable failure must not
            # run the full retry sequence (up to startup_budget_s) on every OCR
            # request.
            now = time.monotonic()
            if self._last_start_attempt and (now - self._last_start_attempt) < self.reinit_cooldown:
                return False
            self._last_start_attempt = now

            budget_deadline = now + self.startup_budget_s
            attempts = len(self.startup_retry_delays) + 1
            last_failure = ""
            budget_spent = False
            for attempt in range(attempts):
                proc = None
                try:
                    proc = self._spawn_once()
                    health = self._await_ready(proc, budget_deadline)
                    self._proc = proc
                    self.health = health
                    logger.info(
                        "OCR GPU subprocess ready (attempt %d/%d): numpy=%s providers=%s model=%s",
                        attempt + 1,
                        attempts,
                        health.get("numpy_version"),
                        health.get("bound_providers"),
                        health.get("model_name"),
                    )
                    return True
                except Exception as exc:  # noqa: BLE001
                    stderr_tail = self._kill(proc)
                    last_failure = f"{exc} {stderr_tail}"
                    logger.warning(
                        "OCR subprocess startup attempt %d/%d failed: %s%s",
                        attempt + 1,
                        attempts,
                        exc,
                        f"\nworker stderr: {stderr_tail}" if stderr_tail else "",
                    )
                    if attempt < len(self.startup_retry_delays):
                        delay = self.startup_retry_delays[attempt]
                        # Do not sleep into (or past) the budget: the caller is a
                        # video frame, and a sleep it cannot use is pure latency.
                        if time.monotonic() + delay >= budget_deadline:
                            budget_spent = True
                            break
                        time.sleep(delay)
                if time.monotonic() >= budget_deadline:
                    budget_spent = True
                    break

            if _is_permanent_failure(last_failure):
                self._permanently_unavailable = True
                logger.error(
                    "OCR GPU subprocess permanently unavailable after %d attempts "
                    "(non-recoverable); using in-process fallback. cause=%s",
                    attempts,
                    last_failure.strip()[:200],
                )
            else:
                logger.warning(
                    "OCR GPU subprocess start failed (transient)%s; will retry after %.0fs cooldown. cause=%s",
                    f" -- {self.startup_budget_s:.0f}s startup budget spent" if budget_spent else "",
                    self.reinit_cooldown,
                    last_failure.strip()[:200],
                )
            return False

    def _await_ready(self, proc: subprocess.Popen, budget_deadline: Optional[float] = None) -> dict:
        """Read the worker's READY handshake, or raise.

        Waits at most ``ready_timeout``, and never past ``budget_deadline`` -- the
        cap on the whole start() sequence, so the last attempt in a sequence gets
        whatever is left rather than a fresh full timeout.
        """
        deadline = time.monotonic() + self.ready_timeout
        if budget_deadline is not None:
            deadline = min(deadline, budget_deadline)
        frame = _ocr_ipc.read_frame(self._reader(proc, deadline))
        if frame.tag != _ocr_ipc.TAG_CONTROL:
            raise OcrSubprocessUnavailable(f"expected control frame, got {frame.tag!r}")
        msg_type = frame.header.get("type")
        if msg_type == _ocr_ipc.CTRL_READY:
            return frame.header
        raise OcrSubprocessUnavailable(f"worker not ready: {frame.header.get('error', msg_type)}")

    # -- request path ------------------------------------------------------
    def run(self, source, return_confidence: bool = True) -> "Tuple[List[str], np.ndarray] | List[str]":
        """OCR one image, or a list of crops in one round trip.

        Mirrors ``LicensePlateRecognizer.run``. ``source`` is an array-like for a
        single image, or a list/tuple of arrays -- which is sent as one ``run_batch``
        request rather than N separate ones, collapsing N IPC round trips into one.
        Result ``i`` belongs to ``source[i]``.

        Raises :class:`OcrSubprocessUnavailable` if the worker dies and cannot
        be recovered. A per-request failure raises a plain ``RuntimeError``
        (the worker stays up).
        """
        if self._permanently_unavailable:
            raise OcrSubprocessUnavailable("OCR subprocess permanently unavailable")

        # A sequence of crops goes over the batch op. It must NOT go through
        # np.asarray: crops from one frame have different shapes, so that raises on
        # a ragged list under numpy >= 1.24 -- which is why batching was impossible
        # before the run_batch frame existed.
        if isinstance(source, (list, tuple)):
            arrays = [np.asarray(a) for a in source]
            runner = lambda: self._run_batch_once(arrays, return_confidence)  # noqa: E731
        else:
            arr = np.asarray(source)
            runner = lambda: self._run_once(arr, return_confidence)  # noqa: E731

        pipe_errors = (EOFError, TimeoutError, BrokenPipeError, ConnectionError)
        try:
            return runner()
        except pipe_errors as exc:
            logger.warning("OCR subprocess pipe error (%s); attempting restart", exc)
            if self._restart_on_crash():
                try:
                    return runner()
                except pipe_errors as exc2:
                    raise OcrSubprocessUnavailable("OCR subprocess crashed again after restart") from exc2
            raise OcrSubprocessUnavailable("OCR subprocess crashed and could not restart") from exc

    def _run_once(self, arr: np.ndarray, return_confidence: bool):
        request = lambda rid: _ocr_ipc.pack_request(rid, arr, return_confidence, op="run")  # noqa: E731
        return self._exchange(request, return_confidence)

    def _run_batch_once(self, arrays: "List[np.ndarray]", return_confidence: bool):
        """OCR several crops in one round trip. Result ``i`` belongs to ``arrays[i]``."""
        request = lambda rid: _ocr_ipc.pack_batch_request(rid, arrays, return_confidence)  # noqa: E731
        return self._exchange(request, return_confidence)

    def _exchange(self, build_request, return_confidence: bool):
        """Write one request, read its response, decode it. Holds the worker lock."""
        with self._lock:
            if not self._is_alive():
                raise EOFError("worker not running")
            self._request_counter += 1
            request_id = self._request_counter
            self._write_all(build_request(request_id))
            deadline = time.monotonic() + self.request_timeout
            frame = _ocr_ipc.read_frame(self._reader(self._proc, deadline))

        if frame.header.get("status") == "error":
            raise RuntimeError(f"OCR worker error: {frame.header.get('error')}")
        texts = list(frame.header.get("texts", []))
        confs = _ocr_ipc.decode_response_confs(frame)
        if return_confidence and confs is not None:
            return texts, confs
        return texts

    def _restart_on_crash(self) -> bool:
        self._close_proc()
        return self.start()

    # -- low-level io ------------------------------------------------------
    def _reader(self, proc: subprocess.Popen, deadline: float):
        """Return a ``read_exact(n)`` bound to ``proc.stdout`` with a deadline."""
        stdout = proc.stdout

        def read_exact(n: int) -> bytes:
            buf = bytearray()
            while len(buf) < n:
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise TimeoutError("OCR worker read timed out")
                ready, _, _ = select.select([stdout], [], [], remaining)
                if not ready:
                    if proc.poll() is not None:
                        raise EOFError("OCR worker exited")
                    raise TimeoutError("OCR worker read timed out")
                chunk = stdout.read(n - len(buf))
                if not chunk:
                    raise EOFError("OCR worker pipe closed")
                buf += chunk
            return bytes(buf)

        return read_exact

    def _write_all(self, data: bytes) -> None:
        stdin = self._proc.stdin
        view = memoryview(data)
        while view:
            written = stdin.write(view)
            if written is None:  # pragma: no cover - rare for blocking pipe
                written = 0
            view = view[written:]
        stdin.flush()

    def _is_alive(self) -> bool:
        return self._proc is not None and self._proc.poll() is None

    def is_available(self) -> bool:
        return not self._permanently_unavailable and self._is_alive()

    def is_permanently_unavailable(self) -> bool:
        """True if the GPU OCR path failed for a non-recoverable reason."""
        return self._permanently_unavailable

    @staticmethod
    def _kill(proc: Optional[subprocess.Popen]) -> str:
        """Terminate ``proc`` and return a short tail of its stderr."""
        if proc is None:
            return ""
        stderr_tail = ""
        try:
            proc.terminate()
            proc.wait(timeout=3)
        except Exception:
            try:
                proc.kill()
                proc.wait(timeout=2)
            except Exception:  # nosec B110 - best effort
                logger.debug("ocr worker kill() failed after terminate()", exc_info=True)
        try:
            if proc.stderr is not None:
                stderr_tail = proc.stderr.read(2000).decode(errors="replace").strip()
        except Exception:  # nosec B110 - best effort
            logger.debug("could not read ocr worker stderr tail", exc_info=True)
        return stderr_tail

    def _close_proc(self) -> None:
        self._kill(self._proc)
        self._proc = None

    def close(self) -> None:
        with self._lock:
            self._close_proc()

    def __del__(self):  # pragma: no cover - GC timing dependent
        # No logging here: GC may run after the logging module is torn down.
        with contextlib.suppress(Exception):
            self._close_proc()


# ---------------------------------------------------------------------------
# Per-process singleton registry
# ---------------------------------------------------------------------------
_clients: Dict[Tuple[str, Tuple[str, ...]], OcrSubprocessClient] = {}
_clients_lock = threading.Lock()


def get_shared_ocr_client(model_name: str, providers: Optional[Sequence[str]] = None) -> OcrSubprocessClient:
    """Return a process-wide singleton client keyed by (model, providers).

    The plate model is tiny, so all post-processing threads in a worker process
    share one subprocess rather than spawning one per camera/thread.
    """
    key = (model_name, tuple(providers or ()))
    with _clients_lock:
        client = _clients.get(key)
        if client is None:
            client = OcrSubprocessClient(model_name, providers)
            _clients[key] = client
        return client


@atexit.register
def _shutdown_all_clients() -> None:  # pragma: no cover - interpreter teardown
    with _clients_lock:
        for client in _clients.values():
            # Teardown: logging may already be unusable, so suppress rather than log.
            with contextlib.suppress(Exception):
                client.close()
