"""RunCommandsMixin, Client's methods: ask a running run's script for a run kind (checkpoint, config, stop, or a kind
it declared), list a run's commands, and the producer's claim and answer (twin: app/runs/commands)."""

from __future__ import annotations

from typing import Any

from .... import errors
from .....generated.records import CommandKind


class RunCommandsMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def ask_run_command(self, run_id: str, kind: CommandKind, args: dict[str, Any] | None = None, *,
                        note: str | None = None) -> dict:  # fmt: skip
        """``POST /v1/runs/{id}/commands``: ask the run's script. Answers the command, ``open`` for the script or
        ``refused`` at once with ``reason`` (the run is not running, no writer, an older SDK, no handler). A custom
        kind is ``CommandKind.CUSTOM`` with ``args={"name": ..., "payload": {...}}``."""
        if not isinstance(kind, CommandKind):
            raise TypeError(f"a command's kind is a CommandKind (CommandKind.CHECKPOINT, ...), not {kind!r}")
        body: dict[str, Any] = {"kind": kind.value, "args": args or {}}
        if note:
            body["note"] = note
        return self.transport.post(f"/v1/runs/{run_id}/commands", body)

    def list_run_commands(self, run_id: str, *, after: int | None = None, limit: int | None = None) -> dict:
        """``GET /v1/runs/{id}/commands``: ``{commands, seq, next_after}``, by seq after ``after``."""
        query = {key: value for key, value in (("after", after), ("limit", limit)) if value is not None}
        return self.transport.get(f"/v1/runs/{run_id}/commands", params=query or None)

    def claim_run_command(self, run_id: str, command_id: str, session_id: str) -> dict | None:
        """Take a command for this writer session; None when another producer took it or it ended (409)."""
        try:
            return self.transport.post(f"/v1/runs/{run_id}/commands/{command_id}/claim", {"session_id": session_id})
        except errors.RosError as exc:
            if exc.status == 409:
                return None
            raise

    def answer_run_command(self, run_id: str, command_id: str, session_id: str, *, state: str,
                           reason: str | None = None, result: dict | None = None) -> dict:  # fmt: skip
        """The claiming session's answer: ``done`` with its ``result``, or ``refused`` with why."""
        body: dict[str, Any] = {"session_id": session_id, "state": state, "result": result or {}}
        if reason:
            body["reason"] = reason[:1024]
        return self.transport.post(f"/v1/runs/{run_id}/commands/{command_id}", body)
