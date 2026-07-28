import contextlib
import io
import os
import shutil
import tempfile
from pathlib import Path
from typing import Callable, List, Optional
from uuid import uuid4

from abstra_internals.controllers.execution.executor_types import ExecutorResponse
from abstra_internals.controllers.execution.snippet_packages import (
    add_smartchat_packages_to_path,
    ensure_snippet_requirements,
    get_smartchat_packages_dir,
)
from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.factory import Repositories
from abstra_internals.sandbox.landlock import SandboxUnavailable, restrict_filesystem
from abstra_internals.settings import Settings

# Ephemeral scratch lives under the project temp dir (/temp on EFS), a sibling of
# the persistent packages dir; a subdir per run, removed by the parent afterwards.
_SNIPPETS_SCRATCH_SUBDIR = "smartchat-snippets"

# Safety cap; cloud-api normally sends a shorter timeout_ms and waits past it.
_SNIPPET_HARD_TIMEOUT_S = 300


def _child_entry(
    conn,
    snippet_path: str,
    run_dir: str,
    home_dir: str,
    packages_dir: str,
    requirements: Optional[List[str]],
    worker_id: str,
    root_path: str,
    repositories_factory: Callable[[], Repositories],
    title: str,
) -> None:
    """Throwaway child; MUST always send exactly one result dict.

    Two-phase Landlock so a snippet's declared deps can be pip-installed into the
    persistent ``packages_dir`` without the snippet code itself being able to
    write there:

      * phase 1 — write roots ``[run_dir, packages_dir]``: pip installs the
        requirements (no user code has run yet);
      * phase 2 — stack a tighter ruleset, write root ``[run_dir]`` only:
        ``packages_dir`` becomes read-only, then the snippet runs.

    Landlock rulesets intersect (each ``restrict_self`` can only remove access),
    so the second call demotes ``packages_dir`` to read-only for the snippet.
    Reads are allowed everywhere; ``run_dir`` is the only writable scratch.
    """
    from abstra_internals.controllers.execution.execution import ExecutionController

    def _reply(ok: bool, error: Optional[str], logs) -> None:
        try:
            conn.send({"ok": ok, "error": error, "logs": logs})
        finally:
            conn.close()

    AbstraLogger.debug(f"[sandboxed-snippet] running {title!r} (worker={worker_id})")
    Settings.set_root_path(root_path)

    # Keep all scratch under run_dir so the single (phase-2) write root covers it.
    os.environ["TMPDIR"] = run_dir
    os.environ["HOME"] = home_dir

    # Sandbox BEFORE any user code. Fail-closed — refuse to run if it can't apply
    # (or if the install fails: the snippet needs those deps).
    try:
        if requirements:
            # phase 1: packages_dir writable so pip can install into it.
            restrict_filesystem(
                read_roots=["/"], write_roots=[run_dir, packages_dir], min_abi=3
            )
            ensure_snippet_requirements(requirements)
            add_smartchat_packages_to_path()
            # phase 2: stacked ruleset drops the packages_dir write bit.
            restrict_filesystem(read_roots=["/"], write_roots=[run_dir], min_abi=3)
        else:
            # No install: packages stay read-only throughout, but remain
            # importable so a snippet can use libs a previous run persisted.
            add_smartchat_packages_to_path()
            restrict_filesystem(read_roots=["/"], write_roots=[run_dir], min_abi=3)
    except SandboxUnavailable as e:
        _reply(False, f"Sandbox unavailable, refusing to execute: {e}", [])
        return
    except Exception as e:  # noqa: BLE001 — sandbox/install failure is fail-closed
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
    requirements: Optional[List[str]] = None,
) -> ExecutorResponse:
    """Spawn the sandboxed child, wait up to timeout_s, relay its result.

    Parent owns the private scratch dir (under /temp): writes the snippet file,
    removes the dir when done. Declared ``requirements`` are pip-installed inside
    the sandbox into the persistent packages dir (see _child_entry); only the
    scratch is discarded afterwards.
    """
    timeout_s = min(timeout_s or _SNIPPET_HARD_TIMEOUT_S, _SNIPPET_HARD_TIMEOUT_S)

    # /temp/smartchat-snippets/<uuid> (respects TMPDIR → EFS /temp in cloud).
    run_dir = os.path.join(tempfile.gettempdir(), _SNIPPETS_SCRATCH_SUBDIR, uuid4().hex)
    home_dir = os.path.join(run_dir, "home")
    snippet_path = os.path.join(run_dir, "snippet.py")
    os.makedirs(home_dir, exist_ok=True)
    # Ensure the packages dir exists so its Landlock write-root rule can attach.
    packages_dir = str(get_smartchat_packages_dir())
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
            packages_dir,
            requirements,
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
        # Only the scratch is removed; installed packages persist in packages_dir.
        shutil.rmtree(run_dir, ignore_errors=True)
