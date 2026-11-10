"""One TRL generation batch's live samples (rl-next W37): each row of a `_generate_and_score_completions` call starts
as the call enters, reads `scoring` while TRL's reward functions run, and ends with its reward as the call returns.
Only the main process's own rows: the others' tasks are not in hand there, and the adapter adds no collective. A
live sample's key is its sample's key, `{split}:{step}:{call}:{rank}:{i}`. Why: DESIGN.md "Live samples"."""

from __future__ import annotations

from collections.abc import Iterable, Mapping
from typing import Any

from probe.generated.samples import AttemptPhase

from .._live import LiveAttempts

#: The refusal the server answers a cancel, retry or watch of a TRL sample with (the W30 spike, T1).
COMMAND_REFUSAL = "verl/TRL gives Probe no handle on one rollout"


class LiveBatch:
    """The live samples one generation call started (none on another process, or with no run)."""

    def __init__(self, live: LiveAttempts | None = None, keys: Iterable[str] = ()) -> None:
        self._live = live
        self.keys = list(keys)
        self._started = set(self.keys)

    @classmethod
    def start(cls, live: LiveAttempts | None, starts: list[dict]) -> LiveBatch:
        if live is None or not starts:
            return cls()
        return cls(live, live.start(starts))

    def mark_scoring(self) -> None:
        """TRL's reward functions run: generation is over for every row."""
        if self._live is not None and self.keys:
            self._live.send_progress(self.keys, phase=AttemptPhase.SCORING, activity="reward functions")

    def link(self, part: dict) -> None:
        """A final generator part names the live sample it came from (its own key)."""
        if part.get("key") in self._started:
            part["attempt_key"] = part["key"]

    def end(self, parts: Iterable[Mapping[str, Any]]) -> None:
        """Each started row's end, graded as its generator part is: its reward, or the error that left it unscored."""
        live = self._live
        if live is None:
            return
        ends = []
        for part in parts:
            if part.get("role", "generator") != "generator" or part.get("key") not in self._started:
                continue
            is_error = part.get("error_reason") is not None
            end: dict[str, Any] = {"key": part["key"], "outcome": live.get_outcome(part.get("reward"), is_error=is_error)}
            if is_error:
                end.update(error_reason=part["error_reason"], error_message=part.get("error_message"))
            ends.append(end)
        live.end(ends)

    def end_rest(self, error: BaseException | None = None) -> None:
        """Rows not ended yet: broken with ``error`` (TRL raised), else `ungraded` (their record failed)."""
        live = self._live
        if live is None:
            return
        rest = [key for key in self.keys if live.is_open(key)]
        if error is not None:
            live.end_error(rest, error)
        else:
            live.end({"key": key, "outcome": live.get_outcome(None)} for key in rest)
