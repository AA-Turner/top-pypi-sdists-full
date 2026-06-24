"""Editor-process side of the linter sidecar.

SidecarLinterRepository implements the LinterRepository ABC so every existing
call site (codebase_events, routes, deploy gate, AI tools) keeps working
unchanged — each method becomes an RPC to the persistent child process, and a
local MIRROR of the serialized checks answers all reads.

Key invariants:
- the mirror is only written by the channel's pump thread (pipe order), via
  the request on_result hook — callers never apply responses themselves;
- mirror non-empty + find_issues_in_codebase ⇒ NO RPC (same fast path as the
  in-process repository); an empty checks payload never wipes a non-empty
  mirror;
- degraded mode (child dead/respawning): reads serve the stale mirror,
  fix_issue returns False, nothing raises — EXCEPT the deploy gate, which is
  fail-closed (one respawn attempt, then SidecarUnavailableError);
- irrecoverability: too many consecutive premature child deaths stop the
  respawn loop. Web editor: exiter (os._exit(1)) so the kubelet restarts the
  pod — k8s CrashLoopBackOff is the anti-loop damper, ABSTRA_LINTER_SIDECAR=0
  the escape hatch. Local CLI: terminal degraded mode, never kill the editor.
"""

import atexit
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from typing import Any, Callable, List, Optional, Sequence

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter import process_actions
from abstra_internals.repositories.linter.models import (
    LinterCheck,
    LinterFix,
    LinterIssue,
    LinterRule,
    normalize_linter_path,
)
from abstra_internals.repositories.linter.repository import (
    BLOCKING_TYPES,
    LinterRepository,
)
from abstra_internals.repositories.linter.sidecar.protocol import (
    PROTOCOL_VERSION,
    ConnectionClosed,
    ProtocolError,
    RpcChannel,
    RpcError,
)
from abstra_internals.settings import Settings

DEFAULT_REQUEST_TIMEOUT = 600.0
DEFAULT_BACKOFF_SCHEDULE: Sequence[float] = (0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 30.0)
DEFAULT_PREMATURE_DEATH_WINDOW = 30.0
DEFAULT_PREMATURE_DEATH_THRESHOLD = 5


class SidecarUnavailableError(Exception):
    """The sidecar is not able to serve a request right now."""


def spawn_sidecar_process(stderr=None) -> "subprocess.Popen":
    """Spawn the real sidecar child for the current Settings.root_path.

    cwd is the library's parent dir, NOT the user's project: `python -m`
    prepends cwd to sys.path, so a user file like json.py would shadow the
    stdlib inside the child. The child chdirs to the project root itself via
    Settings.set_root_path(argv[1]).
    """
    import abstra_internals

    lib_dir = Path(abstra_internals.__file__).resolve().parent.parent
    kwargs: dict = {}
    if os.name == "posix":
        # Own process group: immune to the terminal's Ctrl-C (the editor
        # shuts the child down explicitly) and killable as a tree (pip).
        kwargs["start_new_session"] = True
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "abstra_internals.repositories.linter.sidecar",
            str(Settings.root_path),
        ],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=stderr,
        cwd=str(lib_dir),
        **kwargs,
    )


# ── Mirror objects ───────────────────────────────────────────────
# Rebuilt from the child's serialized checks. They satisfy every consumer in
# the editor process: .to_dict() (WS broadcast, routes), attribute access and
# make_label()/fix.name (AI tool in controllers/main.py).


class _MirrorFix(LinterFix):
    def __init__(self, data: dict):
        self._name = data.get("name", "")
        self.label = data.get("label", "")

    @property
    def name(self):
        return self._name

    def fix(self):
        raise NotImplementedError(
            "mirror fixes are applied by name via the sidecar RPC"
        )


class _MirrorIssue(LinterIssue):
    def __init__(self, data: dict):
        self.label = data.get("label", "")
        self.fixes = [_MirrorFix(f) for f in data.get("fixes", [])]
        self.path = None


def _check_from_dict(data: dict) -> LinterCheck:
    return LinterCheck(
        name=data.get("name", ""),
        label=data.get("label", ""),
        type=data.get("type", "info"),
        issues=[_MirrorIssue(i) for i in data.get("issues", [])],
        fix_with_ai=bool(data.get("fixWithAi", False)),
    )


def _default_exiter() -> None:
    os._exit(1)


def _is_web_editor() -> bool:
    from abstra_internals.environment import EDITOR_MODE

    return EDITOR_MODE == "web"


class _Child:
    __slots__ = ("proc", "channel", "generation", "spawned_at", "death_counted")

    def __init__(self, proc, channel, generation):
        self.proc = proc
        self.channel = channel
        self.generation = generation
        self.spawned_at = time.monotonic()
        self.death_counted = False


class SidecarLinterRepository(LinterRepository):
    def __init__(
        self,
        *,
        popen_factory: Optional[Callable[[], Any]] = None,
        request_timeout: float = DEFAULT_REQUEST_TIMEOUT,
        backoff_schedule: Sequence[float] = DEFAULT_BACKOFF_SCHEDULE,
        premature_death_window: float = DEFAULT_PREMATURE_DEATH_WINDOW,
        premature_death_threshold: int = DEFAULT_PREMATURE_DEATH_THRESHOLD,
        is_web: Optional[bool] = None,
        exiter: Optional[Callable[[], None]] = None,
        process_action_executor: Optional[Callable[[str], None]] = None,
        on_checks_updated: Optional[Callable[[List[LinterCheck]], None]] = None,
    ):
        self._popen_factory = popen_factory or spawn_sidecar_process
        self._request_timeout = request_timeout
        self._backoff_schedule = list(backoff_schedule)
        self._premature_death_window = premature_death_window
        self._premature_death_threshold = premature_death_threshold
        self._is_web = is_web
        self._exiter = exiter or _default_exiter
        self._process_action_executor = (
            process_action_executor or process_actions.execute_process_action
        )
        self._on_checks_updated = on_checks_updated

        self._lock = threading.RLock()
        self._child: Optional[_Child] = None
        self._generation = 0
        self._consecutive_failures = 0
        self._stopped = False
        self._irrecoverable = False
        self._exited = False

        # The checks mirror. Same discipline as LocalLinterRepository: the
        # list is always REBOUND (never mutated in place), only by the pump
        # thread, so readers always see a consistent snapshot.
        self._mirror_lock = threading.Lock()
        self.checks: List[LinterCheck] = []

        atexit.register(self.stop)

    # ── LinterRepository ABC ────────────────────────────────────

    def find_issues_in_codebase(self) -> List[LinterCheck]:
        mirror = self.checks
        if mirror:
            return mirror
        try:
            self._request("get_checks")
        except SidecarUnavailableError as e:
            AbstraLogger.warning(f"[LinterSidecar] get_checks degraded: {e}")
        return self.checks

    def update_checks(self) -> List[LinterCheck]:
        try:
            self._request("run_all")
        except SidecarUnavailableError as e:
            AbstraLogger.warning(
                f"[LinterSidecar] update_checks degraded (stale mirror): {e}"
            )
        return self.checks

    def update_specific_checks(
        self, target_rules: List[LinterRule], paths: Optional[List[Path]] = None
    ) -> List[LinterCheck]:
        params = {
            "rules": [rule.name for rule in target_rules],
            "paths": (
                [str(normalize_linter_path(p)) for p in paths]
                if paths is not None
                else None
            ),
        }
        try:
            self._request("run_rules", params)
        except SidecarUnavailableError as e:
            AbstraLogger.warning(
                f"[LinterSidecar] update_specific_checks degraded (stale mirror): {e}"
            )
        return self.checks

    def fix_issue_in_codebase(self, rule_name: str, fix_name: str) -> bool:
        try:
            result = self._request("apply_fix", {"rule": rule_name, "fix": fix_name})
        except SidecarUnavailableError as e:
            AbstraLogger.warning(f"[LinterSidecar] apply_fix degraded: {e}")
            return False
        self._maybe_execute_process_action(result)
        return bool(result.get("ok"))

    def fix_all_linters(self):
        try:
            result = self._request("fix_all")
        except SidecarUnavailableError as e:
            AbstraLogger.warning(f"[LinterSidecar] fix_all degraded: {e}")
            return
        self._maybe_execute_process_action(result)

    def get_blocking_checks(self) -> List[LinterCheck]:
        return [
            check
            for check in self.checks
            if check.type in BLOCKING_TYPES and check.issues
        ]

    def get_blocking_checks_for_deploy(self) -> List[LinterCheck]:
        # Fail-closed: a dead linter must BLOCK deploys, never silently allow
        # them with a stale gate. One respawn attempt, then a loud error.
        last_error: Optional[Exception] = None
        for _attempt in range(2):
            try:
                result = self._request("blocking_checks_for_deploy")
                return [_check_from_dict(d) for d in (result.get("blocking") or [])]
            except SidecarUnavailableError as e:
                last_error = e
        raise SidecarUnavailableError(
            "Linter is unavailable; cannot verify blocking issues before "
            "deploy. Please try again."
        ) from last_error

    # ── public wiring ───────────────────────────────────────────

    def set_on_checks_updated(
        self, callback: Optional[Callable[[List[LinterCheck]], None]]
    ) -> None:
        self._on_checks_updated = callback

    @property
    def child_process(self):
        with self._lock:
            return self._child.proc if self._child is not None else None

    def stop(self) -> None:
        with self._lock:
            if self._stopped:
                return
            self._stopped = True
            child = self._child
            self._child = None
        if child is None:
            return
        if child.proc.poll() is None:
            try:
                child.channel.request_async("shutdown")
            except Exception:
                pass
            try:
                child.proc.stdin.close()  # EOF: the guaranteed shutdown signal
            except Exception:
                pass
            try:
                child.proc.wait(timeout=5)
            except Exception:
                pass
            if child.proc.poll() is None:
                self._kill_process(child.proc)
        else:
            try:
                child.proc.wait(timeout=1)
            except Exception:
                pass

    # ── process management ──────────────────────────────────────

    def _ensure_child(self) -> _Child:
        with self._lock:
            if self._stopped:
                raise SidecarUnavailableError("linter sidecar was stopped")
            child = self._child
            if child is not None and child.proc.poll() is None:
                return child
            if child is not None:
                self._note_death_locked(child)
                self._child = None
            if self._irrecoverable:
                raise SidecarUnavailableError(
                    "linter sidecar is irrecoverable (too many consecutive "
                    "premature deaths)"
                )

            if self._consecutive_failures > 0 and self._backoff_schedule:
                index = min(
                    self._consecutive_failures - 1,
                    len(self._backoff_schedule) - 1,
                )
                delay = self._backoff_schedule[index]
                if delay > 0:
                    time.sleep(delay)

            try:
                proc = self._popen_factory()
            except Exception as e:
                self._register_failure_locked()
                raise SidecarUnavailableError(
                    f"failed to spawn linter sidecar: {e}"
                ) from e

            self._generation += 1
            child = _Child(
                proc=proc,
                channel=RpcChannel(proc.stdout, proc.stdin),
                generation=self._generation,
            )
            self._child = child
            threading.Thread(
                target=self._reader_loop,
                args=(child,),
                daemon=True,
                name="LinterSidecarReader",
            ).start()

            # Resync BEFORE any queued caller op: the frame is written here,
            # under the spawn lock, so FIFO in the child guarantees the full
            # state is rebuilt first. The wait + broadcast happen async.
            if self.checks:
                self._send_resync_locked(child)
            return child

    def _send_resync_locked(self, child: _Child) -> None:
        try:
            future = child.channel.request_async(
                "run_all",
                on_result=lambda result: self._apply_checks_payload(result),
            )
        except Exception as e:
            AbstraLogger.warning(f"[LinterSidecar] resync send failed: {e}")
            return

        def waiter():
            try:
                result = future.wait(self._request_timeout)
            except Exception as e:
                AbstraLogger.warning(
                    f"[LinterSidecar] resync after respawn failed: {e}"
                )
                return
            callback = self._on_checks_updated
            if callback is None:
                return
            try:
                checks = [
                    _check_from_dict(d) for d in (result or {}).get("checks") or []
                ]
                if checks:
                    callback(checks)
            except Exception as e:
                AbstraLogger.error(f"[LinterSidecar] resync broadcast failed: {e}")

        threading.Thread(target=waiter, daemon=True, name="LinterSidecarResync").start()

    def _reader_loop(self, child: _Child) -> None:
        try:
            child.channel.pump(lambda msg: self._dispatch_from_child(child, msg))
        except ProtocolError as e:
            AbstraLogger.error(f"[LinterSidecar] protocol corruption from child: {e}")
            self._kill_process(child.proc)
        except Exception as e:  # noqa: BLE001
            AbstraLogger.error(f"[LinterSidecar] reader failed: {e}")
            self._kill_process(child.proc)
        finally:
            child.channel.close()
            with self._lock:
                if not self._stopped:
                    self._note_death_locked(child)

    def _note_death_locked(self, child: _Child) -> None:
        if child.death_counted:
            return
        child.death_counted = True
        age = time.monotonic() - child.spawned_at
        if age < self._premature_death_window:
            self._register_failure_locked()
        else:
            self._consecutive_failures = 1

    def _register_failure_locked(self) -> None:
        self._consecutive_failures += 1
        if (
            self._consecutive_failures >= self._premature_death_threshold
            and not self._irrecoverable
        ):
            self._irrecoverable = True
            is_web = self._is_web if self._is_web is not None else _is_web_editor()
            AbstraLogger.error(
                "[LinterSidecar] irrecoverable: %d consecutive premature "
                "deaths. %s"
                % (
                    self._consecutive_failures,
                    "Exiting so the pod restarts (set ABSTRA_LINTER_SIDECAR=0 "
                    "to fall back to in-process linting)."
                    if is_web
                    else "Linting disabled for this session; restart the "
                    "editor to retry.",
                )
            )
            if is_web and not self._exited:
                self._exited = True
                self._exiter()

    def _kill_for_timeout(self, child: _Child) -> None:
        with self._lock:
            if self._child is not child:
                return  # stale generation: never kill a healthy replacement
            self._child = None
            self._note_death_locked(child)
        self._kill_process(child.proc)

    @staticmethod
    def _kill_process(proc) -> None:
        try:
            if isinstance(proc, subprocess.Popen) and os.name == "posix":
                import signal

                # start_new_session=True ⇒ pgid == pid: kills grandchildren
                # too (a pip install spawned by a fix must not survive).
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except Exception:
                    proc.kill()
            else:
                proc.kill()
        except Exception:
            pass
        try:
            proc.wait(timeout=5)
        except Exception:
            pass

    # ── request plumbing ────────────────────────────────────────

    def _request(self, method: str, params: Optional[dict] = None) -> dict:
        child = self._ensure_child()
        try:
            future = child.channel.request_async(
                method,
                params,
                on_result=lambda result: self._apply_checks_payload(result),
            )
            result = future.wait(self._request_timeout)
        except TimeoutError as e:
            AbstraLogger.error(
                f"[LinterSidecar] {method} timed out; killing child: {e}"
            )
            self._kill_for_timeout(child)
            raise SidecarUnavailableError(str(e)) from e
        except ConnectionClosed as e:
            raise SidecarUnavailableError(str(e)) from e
        except RpcError as e:
            AbstraLogger.warning(f"[LinterSidecar] {method} failed in child: {e}")
            raise SidecarUnavailableError(str(e)) from e

        with self._lock:
            self._consecutive_failures = 0
        return result if isinstance(result, dict) else {}

    def _apply_checks_payload(self, result: Any) -> None:
        """Runs on the channel's pump thread: mirror writes happen in pipe
        order, by a single writer."""
        if not isinstance(result, dict):
            return
        checks = result.get("checks")
        if checks is None:
            return
        with self._mirror_lock:
            if not checks and self.checks:
                AbstraLogger.warning(
                    "[LinterSidecar] ignoring empty checks payload over a "
                    "non-empty mirror"
                )
                return
            self.checks = [_check_from_dict(d) for d in checks]

    def _maybe_execute_process_action(self, result: dict) -> None:
        action = result.get("process_action")
        if action:
            self._process_action_executor(action)

    # ── child notifications (child → editor) ────────────────────

    def _dispatch_from_child(self, child: _Child, msg: dict) -> None:
        # The child only sends the `hello` notification (protocol-version
        # handshake). It no longer issues reverse REQUESTS — TypeCheckingRule
        # uses the child's OWN pyrefly, not the editor's, so anything else here
        # is ignored.
        if msg.get("method") != "hello":
            return
        params = msg.get("params") or {}
        if params.get("protocol_version") != PROTOCOL_VERSION:
            AbstraLogger.warning(
                "[LinterSidecar] protocol version mismatch: editor=%s "
                "child=%s (lib %s) — restart the editor after upgrades"
                % (
                    PROTOCOL_VERSION,
                    params.get("protocol_version"),
                    params.get("lib_version"),
                )
            )
