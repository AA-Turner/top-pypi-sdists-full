"""ProxySidecar: `probe samples proxy`, the rollout proxy as a process of its own, for a harness that cannot host it
(another language, a launcher script). It joins the run as a producer and owns the samples started through its
control routes from start to end, so each sample still has one owner."""

from __future__ import annotations

import json
import secrets
import signal
import threading
import uuid
from collections.abc import Callable
from typing import Any
from urllib.parse import unquote

from ......generated.samples import AttemptOutcome
from .proxy import LOCALHOST, RolloutProxy

#: The producer a sidecar writes as unless `--producer` names another.
DEFAULT_PRODUCER = "proxy"
#: What a control start may set on the sample's start part (`run.samples.attempt_start`).
START_FIELDS = frozenset({"group_key", "scheduled_step", "weight_version", "try_number", "retry_of", "started_at",
                          "step", "scenario", "host", "worker", "engine", "sandbox_id"})  # fmt: skip
_END_FIELDS = ("error_reason", "error_message")
_OUTCOMES = frozenset(outcome.value for outcome in AttemptOutcome)


class ProxySidecar:
    """``run``: the run's id or slug. The control token (128-bit unless given) guards `/control/<token>/...`."""

    def __init__(self, *, run: str, upstream: str, producer: str = DEFAULT_PRODUCER, host: str = LOCALHOST,
                 port: int = 0, can_cancel: bool = False, control_token: str | None = None) -> None:  # fmt: skip
        self.token = control_token or secrets.token_urlsafe(16)
        self._run_ref = run
        self._upstream = upstream
        self._producer = producer
        self._can_cancel = can_cancel
        self._proxy = RolloutProxy(host=host, port=port, control=self)
        self._handle: Any = None
        self._samples: Any = None

    def start(self) -> dict:
        """Join the run, listen; returns the addresses to print."""
        from probe.sdk.run.samples import attach_producer

        self._handle = attach_producer(self._producer, run_id=self._run_ref)
        self._samples = self._handle.samples
        self._proxy.start()
        self._proxy.register_handlers(self._samples, can_cancel=self._can_cancel)
        base = self._proxy.base_url
        return {"proxy": base, "control": f"{base}/control/{self.token}", "run": str(self._handle.id),
                "producer": self._producer, "upstream": self._upstream, "can_cancel": self._can_cancel}  # fmt: skip

    def run_forever(self, on_ready: Callable[[dict], None]) -> None:
        """Serve until SIGINT or SIGTERM (or the proxy dies); then end the samples still running `error`
        (`probe_proxy`: their model path is gone) and release the run."""
        stopped = threading.Event()
        for number in (signal.SIGINT, signal.SIGTERM):
            signal.signal(number, lambda *_: stopped.set())
        on_ready(self.start())
        try:
            while not stopped.wait(1.0) and self._proxy.is_healthy():
                pass
        finally:
            self.stop()

    def stop(self) -> None:
        self._proxy.stop(should_fail_live=True)
        if self._handle is not None:
            self._handle.finish("completed", flush_timeout=10)

    # -- the control routes (on a worker thread) --------------------------------------------------
    def handle(self, method: str, path: str, body: bytes) -> tuple[int, dict]:
        """`POST rollouts` starts a sample and hands back its model URL; `POST rollouts/<attempt_key>/end` ends it."""
        try:
            payload = json.loads(body or b"{}")
        except ValueError:
            return 400, _make_error("the body is not JSON")
        if not isinstance(payload, dict):
            return 400, _make_error("the body must be a JSON object")
        parts = path.strip("/").split("/")
        if method == "POST" and parts == ["rollouts"]:
            return self._start_sample(payload)
        if method == "POST" and len(parts) == 3 and parts[0] == "rollouts" and parts[2] == "end":
            return self._end_sample(unquote(parts[1]), payload)
        return 404, _make_error("POST rollouts, or POST rollouts/<attempt_key>/end")

    def _start_sample(self, payload: dict) -> tuple[int, dict]:
        task_key = payload.get("task_key")
        if not isinstance(task_key, str) or not task_key:
            return 400, _make_error("task_key is required")
        unknown = sorted(set(payload) - START_FIELDS - {"task_key", "attempt_key", "upstream"})
        if unknown:
            return 400, _make_error(f"unknown fields: {', '.join(unknown)}")
        key = str(payload.get("attempt_key") or f"proxy:{uuid.uuid4()}")
        upstream = str(payload.get("upstream") or self._upstream)
        fields = {name: value for name, value in payload.items() if name in START_FIELDS}
        self._samples.attempt_start(key, task_key=task_key, **fields)
        return 201, {"attempt_key": key, "url": self._proxy.open_route(self._samples, key, upstream)}

    def _end_sample(self, key: str, payload: dict) -> tuple[int, dict]:
        outcome = payload.get("outcome")
        if outcome not in _OUTCOMES:
            return 400, _make_error(f"outcome must be one of {', '.join(sorted(_OUTCOMES))}")
        fields = {name: str(payload[name]) for name in _END_FIELDS if payload.get(name) is not None}
        self._samples.attempt_end(key, outcome, **fields)
        self._proxy.end_route(key)
        return 200, {"attempt_key": key, "outcome": outcome}


def _make_error(message: str) -> dict:
    return {"error": {"type": "probe_bad_request", "message": message}}
