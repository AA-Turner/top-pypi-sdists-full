"""What a server says of each answer beyond its rows (DSL-424).

Praxis-1's worker reports, in ``runtime_metadata.server``:

- ``model_rows``: the model's real rows (21 when the call started its context, 24 after). An
  answer is never longer than its real rows from a worker of DSL-424 on; one from an older
  worker padded the first answer to 24, and the SDK trims it back to its real rows.
- ``restart`` and ``restart_reason``: whether the call started a new context (a cold start at
  depth 0), and why. ``episode_start`` is expected; any other reason means the robot's context
  was lost (states or frames not sent, or too many steps since the last request), which used
  to happen silently.
- ``history_frames_missing``: executed steps whose frames never arrived (the stack repeated a
  neighbour).
- ``ik_retries`` and ``ik_misses``: target rows the joint solver had to retry from home, and
  rows it left more than 1 mm or 0.5 degrees off.
- ``engine`` and ``engine_reason`` (DSL-429, experimental): the engine that served the answer,
  and why standard served a lightning session's, which each ``ActionChunkResult`` carries.

``record_server_report`` adds them to the session's ``runtime_stats``, where the CLI's summary
and a trace read them.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from dreamscale.policy.types import RuntimeStats

EXPECTED_RESTARTS = frozenset({"episode_start"})


def server_report(chunk: Any) -> Mapping[str, Any]:
    """An answer's ``runtime_metadata.server`` block, or an empty mapping."""
    chunk = getattr(chunk, "raw_chunk", None) or chunk
    metadata = getattr(chunk, "runtime_metadata", None)
    if metadata is None:
        return {}
    server = (metadata.get("server") if isinstance(metadata, Mapping)
              else getattr(metadata, "server", None))
    return server if isinstance(server, Mapping) else {}


def real_rows(chunk: Any) -> int | None:
    """The answer's real rows where its server reports them (``model_rows``), else None."""
    value = server_report(chunk).get("model_rows")
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        return None
    return value


def answer_engine(chunk: Any) -> tuple[str | None, str | None]:
    """The engine that served an answer and why standard did for a lightning session, where
    its server reports them, else (None, None)."""
    server = server_report(chunk)
    engine, reason = server.get("engine"), server.get("engine_reason")
    if not isinstance(engine, str):
        return None, None
    return engine, reason if isinstance(reason, str) else None


def _count(value: Any) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        return 0
    return value


def record_server_report(policy: Any, chunk: Any) -> None:
    """Add an answer's context and kinematics report to ``policy.runtime_stats``."""
    stats = getattr(policy, "runtime_stats", None)
    server = server_report(chunk)
    if not isinstance(stats, RuntimeStats) or not server:
        return
    if "restart" in server:
        stats.context_reports += 1
        reason = server.get("restart_reason")
        if server.get("restart") is True and reason is not None and (
            reason not in EXPECTED_RESTARTS
        ):
            stats.context_restarts += 1
    stats.history_frames_missing += _count(server.get("history_frames_missing"))
    stats.ik_retries += _count(server.get("ik_retries"))
    stats.ik_misses += _count(server.get("ik_misses"))
