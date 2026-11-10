"""What a live event is about: its kind (the v1 catalogue, RL first) and the kind filter a subscription sends."""

from __future__ import annotations

import re
from collections.abc import Iterable, Sequence
from dataclasses import dataclass

from ..compat import StrEnum

#: `family.name[.more]`, lower case. A client accepts any kind of this shape (a newer server may add kinds).
KIND_PATTERN = r"^[a-z][a-z0-9_]*(\.[a-z][a-z0-9_]*)*$"
KIND_RE = re.compile(KIND_PATTERN)
MAX_KIND_CHARS = 128
#: A subscription names at most this many kind patterns.
MAX_KIND_PATTERNS = 32


class LiveFamily(StrEnum):
    """The part of a kind before its first dot. `entity.*` mirrors the audit log one to one."""

    SAMPLES = "samples"
    RUN = "run"
    ENTITY = "entity"
    NOTES = "notes"
    SUMMARY = "summary"
    ACCESS = "access"


class LiveEventKind(StrEnum):
    """The v1 catalogue (`app/live/DESIGN.md` "Kinds"). A comment names the keys its `data` carries."""

    SAMPLES_STEP_SEALED = "samples.step_sealed"  # `StepSealedData`: step, producer, samples, dropped
    SAMPLES_CAPTURE = "samples.capture"  # `CaptureData`: is_complete, reason (the first one's code)
    SAMPLES_LIVE = "samples.live"  # `LiveSampleData`: attempt_key, state, task_key, outcome, reason, elapsed_s
    SAMPLES_FAILING = "samples.failing"  # `FailingData`: reason, host, count, window_s
    SAMPLES_TURN = "samples.turn"  # `TurnData`: attempt_key, seq, role, content (scrubbed, cut): watched samples only
    SAMPLES_COMMAND = "samples.command"  # `CommandData`: command_id, seq, kind, state, attempt_key, requested_by, ...
    SAMPLES_WEIGHTS = "samples.weights"  # `WeightsData`: version, step
    SAMPLES_CHECKPOINT_BEST = "samples.checkpoint_best"  # `CheckpointBestData`: metric, mode, step, value
    RUN_STATUS = "run.status"  # `RunStatusData`: status, reason
    RUN_METRICS = "run.metrics"  # `RunMetricsData`: keys, last_step: at most one per run per 5 s per apply pod
    RUN_ALERT = "run.alert"  # `RunAlertData`: kind, key, value, text
    RUN_FINDING = "run.finding"  # `RunFindingData`: kind, key, value, severity
    RUN_CHECKPOINT = "run.checkpoint"  # `RunCheckpointData`: name, step
    RUN_ARTIFACT = "run.artifact"  # `RunArtifactData`: name, kind (a file that is not a checkpoint)
    RUN_COMMAND = "run.command"  # `CommandData` of a run kind (checkpoint, config, stop, custom): asked, taken, ended
    NOTES_CHANGED = "notes.changed"  # `DocumentChangedData`: entity, entity_id, version
    SUMMARY_CHANGED = "summary.changed"  # `DocumentChangedData`: entity, entity_id, version
    ACCESS_CHANGED = "access.changed"  # target (`AccessChangedData`)
    # Control events: about the stream, not the data. Every subscription gets them whatever its filter.
    RESYNC = "resync"  # reason (`ResyncData`): events may be missed; re-read state, then follow from `seq`
    LAGGED = "lagged"  # behind (`LaggedData`): the stream fell behind and catches up from the table


#: Kinds every subscription receives, whatever it asked for.
CONTROL_KINDS = frozenset({LiveEventKind.RESYNC.value, LiveEventKind.LAGGED.value})


def make_entity_kind(event_type: str) -> str:
    """`run.status_changed` (an audit `EventType`) -> `entity.run.status_changed`."""
    kind = f"{LiveFamily.ENTITY.value}.{event_type}"
    if not KIND_RE.fullmatch(kind) or len(kind) > MAX_KIND_CHARS:
        raise ValueError(f"audit event type {event_type!r} does not make a live kind")
    return kind


def get_family(kind: str) -> LiveFamily | None:
    """The kind's family; None for a control kind or a family this copy does not know."""
    if "." not in kind:
        return None
    try:
        return LiveFamily(kind.split(".", 1)[0])
    except ValueError:
        return None


def list_catalogued_kinds() -> tuple[str, ...]:
    """Every data kind in the catalogue (control kinds left out). The server adds one `entity.*` per audit type."""
    return tuple(kind.value for kind in LiveEventKind if kind.value not in CONTROL_KINDS)


@dataclass(frozen=True)
class KindFilter:
    """The kinds a subscription wants: exact kinds and `family.*` prefixes (`samples.*`, `entity.run.*`).

    Empty means every kind. Control kinds always match.
    """

    patterns: tuple[str, ...] = ()

    @classmethod
    def parse(cls, text: str | Sequence[str] | None) -> KindFilter:
        """`samples.*,run.status` (the `kinds=` query) or a list; refuses a malformed pattern."""
        if text is None:
            return cls()
        parts = text.split(",") if isinstance(text, str) else list(text)
        patterns = tuple(dict.fromkeys(part.strip() for part in parts if part.strip()))
        if len(patterns) > MAX_KIND_PATTERNS:
            raise ValueError(f"at most {MAX_KIND_PATTERNS} kind patterns")
        for pattern in patterns:
            if pattern == "*":
                continue
            body = pattern[:-2] if pattern.endswith(".*") else pattern
            if len(pattern) > MAX_KIND_CHARS or not KIND_RE.fullmatch(body):
                raise ValueError(f"{pattern!r} is not a kind or a `family.*` pattern")
        return cls(("*",) if "*" in patterns else patterns)

    def matches(self, kind: str) -> bool:
        """Does a kind pass? Control kinds always do."""
        if not self.patterns or kind in CONTROL_KINDS:
            return True
        return any(_match_pattern(pattern, kind) for pattern in self.patterns)

    def find_unknown(self, known: Iterable[str]) -> list[str]:
        """The patterns that match none of `known`: the server answers 422 naming them (a typo never waits forever)."""
        kinds = tuple(known)
        return [pattern for pattern in self.patterns
                if not any(_match_pattern(pattern, kind) for kind in kinds)]

    def to_query(self) -> str | None:
        """The `kinds=` value, or None for every kind."""
        return ",".join(self.patterns) if self.patterns else None


def _match_pattern(pattern: str, kind: str) -> bool:
    if pattern == "*":
        return True
    if pattern.endswith(".*"):
        return kind.startswith(pattern[:-1])
    return kind == pattern
