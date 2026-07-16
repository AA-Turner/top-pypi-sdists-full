import contextlib
import io
import os
import shutil
from pathlib import Path
from typing import Callable, Optional
from uuid import uuid4

from abstra_internals.controllers.execution.executor_types import ExecutorResponse
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.factory import Repositories
from abstra_internals.sandbox.landlock import SandboxUnavailable, restrict_filesystem
from abstra_internals.settings import Settings

# Safety cap; cloud-api normally sends a shorter timeout_ms and waits past it.
_SNIPPET_HARD_TIMEOUT_S = 300


def _child_entry(
    conn,
    snippet_path: str,
    run_dir: str,
    home_dir: str,
    worker_id: str,
    root_path: str,
    repositories_factory: Callable[[], Repositories],
    title: str,
) -> None:
    """Throwaway child; MUST always send exactly one result dict.

    Parent wrote the snippet into `run_dir`, so the child's only write root is
    `run_dir` — no project/EFS write access needed. Reads allowed everywhere.
    """
    from abstra_internals.controllers.execution.execution import ExecutionController

    def _reply(ok: bool, error: Optional[str], logs) -> None:
        try:
            conn.send({"ok": ok, "error": error, "logs": logs})
        finally:
            conn.close()

    AbstraLogger.debug(f"[sandboxed-snippet] running {title!r} (worker={worker_id})")
    Settings.set_root_path(root_path)

    # Keep all scratch under run_dir (tmpfs) so the single write root covers it.
    os.environ["TMPDIR"] = run_dir
    os.environ["HOME"] = home_dir

    # Sandbox BEFORE any user code: read-only everywhere, write only run_dir.
    # Fail-closed — refuse to run if it can't be applied.
    try:
        restrict_filesystem(read_roots=["/"], write_roots=[run_dir], min_abi=3)
    except SandboxUnavailable as e:
        _reply(False, f"Sandbox unavailable, refusing to execute: {e}", [])
        return
    except Exception as e:  # noqa: BLE001 — any sandbox failure is fail-closed
        AbstraLogger.capture_exception(e)
        _reply(False, f"Sandbox setup failed, refusing to execute: {e}", [])
        return

    stdout, stderr = io.StringIO(), io.StringIO()
    try:
        repositories = repositories_factory()
        # Capture print() directly; skip the pooled executor's log pipeline.
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            result = ExecutionController.run_snippet(
                file_path=Path(snippet_path),
                worker_id=worker_id,
                repositories=repositories,
            )
        _reply(
            result["ok"],
            result.get("error"),
            _as_logs(stdout.getvalue(), stderr.getvalue()),
        )
    except Exception as e:  # noqa: BLE001
        AbstraLogger.capture_exception(e)
        _reply(False, str(e), _as_logs(stdout.getvalue(), stderr.getvalue()))


def _as_logs(out: str, err: str) -> list:
    logs = []
    if out:
        logs.append({"type": "stdout", "text": out})
    if err:
        logs.append({"type": "stderr", "text": err})
    return logs


def run_snippet_sandboxed(
    code: str,
    title: str,
    worker_id: str,
    mp_context,
    repositories_factory: Callable[[], Repositories],
    timeout_s: Optional[int] = None,
) -> ExecutorResponse:
    """Spawn the sandboxed child, wait up to timeout_s, relay its result.

    Parent owns the private scratch dir: writes the snippet file, removes the
    dir when done — nothing the snippet wrote persists.
    """
    timeout_s = min(timeout_s or _SNIPPET_HARD_TIMEOUT_S, _SNIPPET_HARD_TIMEOUT_S)

    run_dir = f"/tmp/abstra-snippet-{uuid4().hex}"
    home_dir = os.path.join(run_dir, "home")
    snippet_path = os.path.join(run_dir, "snippet.py")
    os.makedirs(home_dir, exist_ok=True)
    with open(snippet_path, "w", encoding="utf-8") as f:
        f.write(code)

    parent_conn, child_conn = mp_context.Pipe()
    proc = mp_context.Process(
        target=_child_entry,
        args=(
            child_conn,
            snippet_path,
            run_dir,
            home_dir,
            worker_id,
            str(Settings.root_path),
            repositories_factory,
            title,
        ),
        daemon=True,
    )
    proc.start()
    child_conn.close()  # parent keeps only its end; EOF becomes detectable

    try:
        if parent_conn.poll(timeout_s):
            payload = parent_conn.recv()
            return ExecutorResponse(
                success=payload["ok"],
                error=payload.get("error"),
                logs=payload.get("logs", []),
            )
        return ExecutorResponse(
            success=False,
            error=f"Snippet execution timed out after {timeout_s}s",
            logs=[],
        )
    except EOFError:
        return ExecutorResponse(
            success=False, error="Sandbox process died unexpectedly", logs=[]
        )
    finally:
        parent_conn.close()
        if proc.is_alive():
            proc.terminate()
            proc.join(timeout=5)
            if proc.is_alive():
                proc.kill()
        shutil.rmtree(run_dir, ignore_errors=True)
