from __future__ import annotations

from typing import Any

from matrx_graph.errors import ChannelError
from matrx_graph.types.channel import ChannelSpec, coerce_to_json
from matrx_graph.types.primitives import Reducer


def _apply_replace(_current: Any, writes: list[Any]) -> Any:
    if not writes:
        return _current
    return writes[-1]


def _apply_append(current: Any, writes: list[Any]) -> list[Any]:
    base: list[Any] = list(current) if isinstance(current, list) else []
    for w in writes:
        if isinstance(w, list):
            base.extend(w)
        else:
            base.append(w)
    return base


def _apply_merge(current: Any, writes: list[Any]) -> dict[str, Any]:
    base: dict[str, Any] = dict(current) if isinstance(current, dict) else {}
    for w in writes:
        if not isinstance(w, dict):
            raise ChannelError(f"merge reducer received a non-dict write: {type(w).__name__}")
        base.update(w)
    return base


def _apply_sum(current: Any, writes: list[Any]) -> int | float:
    base: int | float = current if isinstance(current, int | float) else 0
    for w in writes:
        if not isinstance(w, int | float):
            raise ChannelError(f"sum reducer received a non-numeric write: {type(w).__name__}")
        base += w
    return base


def _apply_last_writer_wins(_current: Any, writes: list[Any]) -> Any:
    # Identical runtime behavior to `replace`; the distinction is that the
    # PostgresCheckpointer will log writer identity for audit. In Phase 1 we
    # keep the runtime simple — auditing lands with the Postgres backend.
    return _apply_replace(_current, writes)


def _apply_topic_map(current: Any, writes: list[Any]) -> dict[str, list[Any]]:
    base: dict[str, list[Any]] = (
        {k: list(v) for k, v in current.items() if isinstance(v, list)}
        if isinstance(current, dict)
        else {}
    )
    for w in writes:
        if not isinstance(w, dict) or "topic" not in w:
            raise ChannelError(
                "topic_map reducer requires each write to be a dict with a 'topic' key"
            )
        topic = w["topic"]
        if not isinstance(topic, str):
            raise ChannelError("topic_map reducer: 'topic' must be a string")
        entry = {k: v for k, v in w.items() if k != "topic"}
        base.setdefault(topic, []).append(entry)
    return base


_REDUCERS: dict[Reducer, Any] = {
    "replace": _apply_replace,
    "append": _apply_append,
    "merge": _apply_merge,
    "sum": _apply_sum,
    "last_writer_wins": _apply_last_writer_wins,
    "topic_map": _apply_topic_map,
}


def resolve_reducer(name: str) -> Any:
    """Return the reducer fn for ``name`` — the ONE reducer vocabulary.

    Join arg_merge (ENGINE_SPEC §3.7) reuses the channel reducers instead of
    growing a parallel merge dialect: ``fn(current, writes)`` where a fresh
    merge passes ``current=None``. Raises ChannelError for an unknown name
    (validate_definition rejects it earlier; this is the loud backstop).
    """
    try:
        return _REDUCERS[name]  # type: ignore[index]
    except KeyError:
        raise ChannelError(f"Unknown reducer '{name}'. Known: {sorted(_REDUCERS)}.") from None


class ChannelManager:
    """Holds channel state between super-steps and applies reducers on commit.

    The scheduler:
        1. At step start — calls `snapshot()` to produce a read-only view
           that every node invocation in the step shares.
        2. During step — collects pending writes (channel_name, value) from
           each invocation's ChannelView.drain().
        3. At step end — passes ALL writes to `commit(writes)`, which groups
           by channel and applies each channel's reducer once.

    Channels not declared in the definition get an implicit `replace` channel
    with default=None — unless strict=True, in which case undeclared writes
    raise ChannelError.
    """

    def __init__(self, specs: dict[str, ChannelSpec], strict: bool = False) -> None:
        self._specs: dict[str, ChannelSpec] = dict(specs)
        self._strict = strict
        self._values: dict[str, Any] = {
            name: spec.default for name, spec in specs.items() if spec.default is not None
        }

    def values(self) -> dict[str, Any]:
        return dict(self._values)

    def snapshot(self) -> dict[str, Any]:
        return dict(self._values)

    def load_values(self, values: dict[str, Any]) -> None:
        """Replace current state from a checkpoint snapshot. Used on resume."""
        self._values = dict(values)

    def commit(self, writes: list[tuple[str, Any]]) -> None:
        """Apply a batch of writes via each channel's reducer.

        Writes to unknown channels are accepted in non-strict mode (implicit
        'replace' channel) and rejected in strict mode.
        """
        grouped: dict[str, list[Any]] = {}
        for channel, value in writes:
            grouped.setdefault(channel, []).append(coerce_to_json(value))

        for channel, channel_writes in grouped.items():
            spec = self._specs.get(channel)
            if spec is None:
                if self._strict:
                    known = sorted(self._specs)
                    raise ChannelError(
                        f"Write to undeclared channel '{channel}' in strict mode. "
                        f"Declare it in Definition.channels. Known: {known}."
                    )
                spec = ChannelSpec(name=channel, reducer="replace")
                self._specs[channel] = spec

            reducer_fn = _REDUCERS[spec.reducer]
            current = self._values.get(channel, spec.default)
            self._values[channel] = reducer_fn(current, channel_writes)
