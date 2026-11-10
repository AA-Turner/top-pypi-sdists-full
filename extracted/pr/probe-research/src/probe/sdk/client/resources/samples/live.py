"""LiveSamplesMixin, Client's methods: which samples run now, one watched sample's turns, and the asks on one sample
(cancel, retry, watch), each a dict as the route answers it (twin: app/runs/samples)."""

from __future__ import annotations

from collections.abc import Iterable
from typing import Any
from urllib.parse import quote

from .....generated.records import CommandKind


def _quote(value: Any) -> str:
    return quote(str(value), safe="")


class LiveSamplesMixin:
    """Part of Client: its methods run with `self` the Client; compose() folds them into Client."""

    def list_live_samples(
        self,
        run_id: str,
        *,
        states: Iterable[str] | None = None,
        hung_after: str | None = None,
        window: str | None = None,
        limit: int | None = None,
    ) -> dict:
        """`GET /v1/runs/{id}/samples/live`: which samples run now, which are slow, hung or abandoned, and what is
        failing (`LiveSampleList`). ``states``: running, hung, abandoned, superseded, ended (default the first
        three); ``hung_after`` / ``window``: `10m`."""
        query: dict[str, Any] = {"state": [str(state) for state in states or ()]}
        for name, value in (("hung_after", hung_after), ("window", window), ("limit", limit)):
            if value is not None:
                query[name] = value
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/live", params=query)

    def list_live_turns(self, run_id: str, attempt_id: str, *, after: int | None = None,
                        limit: int | None = None) -> dict:  # fmt: skip
        """`GET /v1/runs/{id}/samples/live/{attempt}/turns`: a watched sample's turns by seq, after ``after``
        (`LiveTurnList`; pass back its `next_after`)."""
        query = {name: value for name, value in (("after", after), ("limit", limit)) if value is not None}
        return self.transport.get(f"/v1/runs/{_quote(run_id)}/samples/live/{_quote(attempt_id)}/turns",
                                  params=query or None)  # fmt: skip

    def ask_sample_command(self, run_id: str, attempt_id: str, kind: CommandKind, *, note: str | None = None) -> dict:
        """Ask a live sample's producer to cancel, retry or watch it: the command as written, `open` for its
        producer, or `refused` at once with `reason` (its producer cannot do it, or holds the sample no more)."""
        asks = {CommandKind.CANCEL: self.cancel_live_sample, CommandKind.RETRY: self.retry_live_sample,
                CommandKind.WATCH: self.watch_live_sample}  # fmt: skip
        if kind not in asks:
            raise ValueError(f"a sample is asked to cancel, retry or watch, not {kind!r}")
        return asks[CommandKind(kind)](run_id, attempt_id, note=note)

    def cancel_live_sample(self, run_id: str, attempt_id: str, *, note: str | None = None) -> dict:
        """`POST /v1/runs/{id}/samples/live/{attempt}/cancel`: stop it by its framework's safe path."""
        return self.transport.post(f"/v1/runs/{_quote(run_id)}/samples/live/{_quote(attempt_id)}/cancel",
                                   _build_ask(note))  # fmt: skip

    def retry_live_sample(self, run_id: str, attempt_id: str, *, note: str | None = None) -> dict:
        """`POST /v1/runs/{id}/samples/live/{attempt}/retry`: a fresh attempt in its slot; the answer names it."""
        return self.transport.post(f"/v1/runs/{_quote(run_id)}/samples/live/{_quote(attempt_id)}/retry",
                                   _build_ask(note))  # fmt: skip

    def watch_live_sample(self, run_id: str, attempt_id: str, *, note: str | None = None) -> dict:
        """`POST /v1/runs/{id}/samples/live/{attempt}/watch`: its live turns for 10 min (ask again to renew)."""
        return self.transport.post(f"/v1/runs/{_quote(run_id)}/samples/live/{_quote(attempt_id)}/watch",
                                   _build_ask(note))  # fmt: skip


def _build_ask(note: str | None) -> dict:
    """The ask's body (`CommandAsk`)."""
    return {"note": note} if note else {}
