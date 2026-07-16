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
  fix_issue returns False, nothing raises; the deploy gate is the one caller
  that still needs a real answer, so on a slow/unavailable child it recomputes
  the blocking checks in-process rather than blocking the deploy;
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
    LocalLinterRepository,
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
# The deploy gate waits at most this long on the sidecar before computing the
# blocking checks in-process instead — a slow child must never make the user
# sit through (nor be blocked by) the full request timeout on a publish.
DEFAULT_DEPLOY_GATE_TIMEOUT = 120.0
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
        type=data.get("type", "warning"),
        issues=[_MirrorIssue(i) for i in data.get("issues", [])],
        fix_with_ai=bool(data.get("fixWithAi", False)),
        status=data.get("status", "ok"),
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
        deploy_gate_timeout: float = DEFAULT_DEPLOY_GATE_TIMEOUT,
        deploy_fallback_factory: Optional[Callable[[], LinterRepository]] = None,
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
        self._deploy_gate_timeout = deploy_gate_timeout
        self._deploy_fallback_factory = deploy_fallback_factory or LocalLinterRepository
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

    def update_checks(self, revalidate_caches: bool = False) -> List[LinterCheck]:
        try:
            self._request("run_all", {"revalidate_caches": revalidate_caches})
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
        # A failed blocking check blocks too (fail-closed, same policy as a
        # dead sidecar): the rule crashed, so "no issues" was never verified.
        return [
            check
            for check in self.checks
            if check.type in BLOCKING_TYPES
            and (check.issues or check.status == "failed")
        ]

    def get_blocking_checks_for_deploy(self) -> List[LinterCheck]:
        # The deploy gate MUST verify blocking issues, but a slow or unavailable
        # linter must never HARD-BLOCK a publish. Ask the sidecar with a bounded
        # timeout; if the child can't answer in time (or is down), recompute the
        # gate in-process — same rule stack, parallel fan-out, no request
        # timeout — so the deploy is still verified instead of failed.
        try:
            result = self._request(
                "blocking_checks_for_deploy", timeout=self._deploy_gate_timeout
            )
            return [_check_from_dict(d) for d in (result.get("blocking") or [])]
        except SidecarUnavailableError as e:
            AbstraLogger.warning(
                "[LinterSidecar] deploy gate unavailable via sidecar; running "
                f"in-process fallback: {e}"
            )
            return self._blocking_checks_for_deploy_in_process()

    def _blocking_checks_for_deploy_in_process(self) -> List[LinterCheck]:
        """Compute the deploy gate directly in the editor process when the
        sidecar can't answer. Mirrors the pre-sidecar path: a fresh in-process
        repository (parallel fan-out), no request timeout, no fail-closed block.
        The freshly computed blocking-rule checks are merged into the mirror so
        the post-deploy broadcast reflects them (unrelated non-blocking checks in
        the mirror are kept)."""
        fallback = self._deploy_fallback_factory()
        blocking = fallback.get_blocking_checks_for_deploy()
        fresh = {check.name for check in fallback.checks}
        with self._mirror_lock:
            merged = [c for c in self.checks if c.name not in fresh]
            merged.extend(fallback.checks)
            self.checks = merged
        return blocking

    def _notify_checks_updated(self) -> None:
        callback = self._on_checks_updated
        if callback is None:
            return
        try:
            callback(self.checks)
        except Exception as e:
            AbstraLogger.warning(f"[LinterSidecar] checks-updated notify failed: {e}")

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
                    (
                        "Exiting so the pod restarts (set ABSTRA_LINTER_SIDECAR=0 "
                        "to fall back to in-process linting)."
                        if is_web
                        else "Linting disabled for this session; restart the "
                        "editor to retry."
                    ),
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

    def _request(
        self,
        method: str,
        params: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        # Degraded bookkeeping wraps every RPC (including _ensure_child spawn
        # failures): callers that swallow SidecarUnavailableError and serve the
        # stale mirror leave a visible trace, and the WS broadcast payload
        # reports it to the editor UI as status=degraded.
        try:
            result = self._do_request(method, params, timeout)
        except SidecarUnavailableError:
            self.degraded = True
            raise
        self.degraded = False
        return result

    def _do_request(
        self,
        method: str,
        params: Optional[dict] = None,
        timeout: Optional[float] = None,
    ) -> dict:
        child = self._ensure_child()
        wait_timeout = timeout if timeout is not None else self._request_timeout
        try:
            future = child.channel.request_async(
                method,
                params,
                on_result=lambda result: self._apply_checks_payload(result),
            )
            result = future.wait(wait_timeout)
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
