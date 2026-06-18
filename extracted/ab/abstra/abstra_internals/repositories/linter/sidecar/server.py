"""Child-process side of the linter sidecar.

Owns the canonical lint state (a real LocalLinterRepository) and serves the
editor's RPCs. Threading model:

- the caller of serve() (the child's main thread) reads frames and dispatches:
  lint operations are queued; shutdown is answered inline and stops serving;
- a single worker thread drains the lint queue in FIFO order — operations are
  serial, mirroring the single-flight semantics callers get in-process today;
- reverse requests (lsp_diagnostics) go out through the same channel and wait
  bounded; on timeout they degrade to [] exactly like the in-process wrapper.
"""

import queue
import threading
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from abstra_internals.logger import AbstraLogger
from abstra_internals.repositories.linter.process_actions import (
    set_process_action_handler,
)
from abstra_internals.repositories.linter.sidecar.protocol import (
    PROTOCOL_VERSION,
    RpcChannel,
    StopPump,
)

LINT_METHODS = frozenset(
    {
        "run_all",
        "run_rules",
        "apply_fix",
        "fix_all",
        "get_checks",
        "blocking_checks_for_deploy",
    }
)


def _resolve_lib_version() -> str:
    try:
        from importlib.metadata import version

        return version("abstra")
    except Exception:
        return "unknown"


class SidecarLinterServer:
    def __init__(
        self,
        repository,
        registry: List[Any],
        reader,
        writer,
        *,
        reverse_request_timeout: float = 15.0,
        lib_version: Optional[str] = None,
    ):
        self._repository = repository
        self._rules_by_name: Dict[str, Any] = {rule.name: rule for rule in registry}
        self._channel = RpcChannel(reader, writer)
        self._reverse_request_timeout = reverse_request_timeout
        self._lib_version = (
            lib_version if lib_version is not None else _resolve_lib_version()
        )
        self._queue: "queue.Queue[Optional[dict]]" = queue.Queue()

    def serve(self) -> None:
        """Blocking. Returns on stdin EOF or on a shutdown request."""
        self._channel.notify(
            "hello",
            {
                "lib_version": self._lib_version,
                "protocol_version": PROTOCOL_VERSION,
            },
        )
        worker = threading.Thread(
            target=self._worker_loop, daemon=True, name="LinterSidecarWorker"
        )
        worker.start()
        try:
            self._channel.pump(self._dispatch)
        finally:
            self._queue.put(None)
            worker.join(timeout=1.0)

    # ── reverse requests (child → editor) ──────────────────────

    def request_diagnostics(self, code: str) -> list:
        """Diagnostics from the EDITOR's pyrefly via reverse RPC. Degrades to
        [] on timeout/failure, mirroring the in-process wrapper."""
        try:
            result = self._channel.request(
                "lsp_diagnostics",
                {"code": code},
                timeout=self._reverse_request_timeout,
            )
        except Exception:
            return []
        if not isinstance(result, dict):
            return []
        return result.get("diagnostics") or []

    # ── incoming dispatch ───────────────────────────────────────

    def _dispatch(self, msg: dict) -> None:
        method = msg.get("method")
        rid = msg.get("id")
        if method == "shutdown":
            if rid is not None:
                self._channel.respond(rid, {"ok": True})
            raise StopPump()
        if rid is None:
            return  # stray notification — nothing to do
        if method in LINT_METHODS:
            self._queue.put(msg)
            return
        self._channel.respond_error(rid, "unknown method: %s" % method)

    def _worker_loop(self) -> None:
        while True:
            msg = self._queue.get()
            if msg is None:
                return
            rid = msg.get("id")
            try:
                result = self._handle(msg.get("method"), msg.get("params") or {})
            except Exception as e:  # noqa: BLE001 - report to the peer, keep serving
                try:
                    self._channel.respond_error(rid, "%s: %s" % (type(e).__name__, e))
                except Exception:
                    return
                continue
            try:
                self._channel.respond(rid, result)
            except Exception:
                return

    # ── lint operations ─────────────────────────────────────────

    @staticmethod
    def _serialized(checks) -> list:
        return [check.to_dict() for check in checks]

    def _handle(self, method: Optional[str], params: dict) -> dict:
        repository = self._repository
        if method == "run_all":
            return {"checks": self._serialized(repository.update_checks())}
        if method == "run_rules":
            rules = self._resolve_rules(params.get("rules") or [])
            raw_paths = params.get("paths")
            paths = [Path(p) for p in raw_paths] if raw_paths is not None else None
            checks = repository.update_specific_checks(rules, paths=paths)
            return {"checks": self._serialized(checks)}
        if method == "apply_fix":
            ok, action = self._collect_process_action(
                lambda: repository.fix_issue_in_codebase(params["rule"], params["fix"])
            )
            return {
                "ok": bool(ok),
                "checks": self._serialized(repository.checks),
                "process_action": action,
            }
        if method == "fix_all":
            _, action = self._collect_process_action(repository.fix_all_linters)
            return {"ok": True, "process_action": action}
        if method == "get_checks":
            return {"checks": self._serialized(repository.find_issues_in_codebase())}
        if method == "blocking_checks_for_deploy":
            blocking = repository.get_blocking_checks_for_deploy()
            return {
                "blocking": self._serialized(blocking),
                "checks": self._serialized(repository.checks),
            }
        raise ValueError("unhandled method: %s" % method)

    def _resolve_rules(self, names: List[str]) -> List[Any]:
        rules = []
        for name in names:
            rule = self._rules_by_name.get(name)
            if rule is None:
                AbstraLogger.warning(
                    "[LinterSidecar] Unknown rule %r requested — skipping" % name
                )
                continue
            rules.append(rule)
        return rules

    @staticmethod
    def _collect_process_action(
        fn: Callable[[], Any],
    ) -> Tuple[Any, Optional[str]]:
        """Run a fix operation capturing any requested process action instead
        of executing it in this (child) process. Only the worker thread runs
        fixes, so the module-level hook swap is race-free here."""
        actions: List[str] = []
        set_process_action_handler(actions.append)
        try:
            result = fn()
        finally:
            set_process_action_handler(None)
        return result, (actions[-1] if actions else None)
