"""Request-scoped chat/agent latency trace.

Collection is ALWAYS ON for AI run routes: every request's marks/blocks feed the one
``platform.ai_request_latency`` row (aidream/services/ai_execution/latency_report.py).
``CHAT_TIME_CHECK_ENABLED`` now gates ONLY the console output (mark lines + block table).
"""

from __future__ import annotations

import time
from contextvars import ContextVar
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any

CHAT_TIME_CHECK_ENABLED = False  # console output only; collection is always on (see module docstring)

# Per-mark line printing. The block-table summary (emit_prep_summary) is the real signal;
# the ~30 individual mark lines are mostly sub-millisecond noise (+0.00). When not verbose,
# only marks that actually cost time (delta ≥ threshold) or milestones print — cutting the
# per-request wall of lines to the handful that matter. Flip _VERBOSE_MARKS to see them all.
_VERBOSE_MARKS = False
_MARK_PRINT_MIN_DELTA_S = 0.03

# Inbound probe — only stamp routes that may arm chat timing. Remove once confirmed clean.
_CHAT_TIMING_PATH_PREFIXES = (
    "/agents",
    "/agent/",
    "/conversations",
    "/conversation/",
    "/chat",
    "/manual",
    "/prompts",
    "/prompt/",
    "/ai/",
    "/mandates",
)

_PROVIDER_SDK_START_KEYS = frozenset({"provider_sdk_call"})
_PROVIDER_SDK_END_KEYS = frozenset({"provider_sdk_complete", "provider_execute_complete"})
_PROVIDER_BOUNDARY_KEYS = (
    _PROVIDER_SDK_START_KEYS | _PROVIDER_SDK_END_KEYS | frozenset({"turn_complete"})
)
# Prep timing ends here — provider SDK call is out of our hands.
PREP_COMPLETE_KEY = "payload_captured"

# ---------------------------------------------------------------------------
# Block rollup
# ---------------------------------------------------------------------------
# Folds the ~30 fine-grained marks into the handful of BLOCKS that actually
# matter, each tagged by the kind of work it is, so the summary answers the only
# questions worth asking — "where did controllable time go, and which blocks
# touch the database?" — instead of drowning the signal in sub-millisecond marks.
#
# io tag:  read  = a DB read that SHOULD be cache/prefetch-able
#          write = a DB write that SHOULD be async / off the critical path
#          rpc   = a DB function call (resolve_full_context — session essentials)
#          local = CPU only, no DB (noise — collapse, never optimize)
#
# `keys` are the marks that CLOSE each block's segment(s); a segment's delta is
# attributed to the block owning its `to_key`. `op` names the actual operation so
# the table reads as a ledger of what we fetch, not a wall of labels.
_BLOCKS: tuple[tuple[str, str, str, tuple[str, ...], str], ...] = (
    ("entry", "Route + auth entry", "local", ("prep_begin", "prepare_entry"), "—"),
    (
        "agent_load",
        "Agent definition load",
        "read",
        ("agx_loaded",),
        "agx_definition SELECT (10-min cache)",
    ),
    (
        "conversation",
        "Conversation create",
        "write",
        ("conversation_resolved",),
        "cx_conversation INSERT (out-of-band Session)",
    ),
    (
        "scope_picklist",
        "Memory + scope + picklist",
        "local",
        ("memory_resolved", "scope_bindings", "picklist_staged"),
        "local resolve",
    ),
    (
        "sandbox",
        "Sandbox arm",
        "read",
        ("sandbox_armed",),
        "conversation binding lookup (skipped for new conv)",
    ),
    ("skills", "Skills catalog", "read", ("skills_merged",), "skill catalog (process cache)"),
    (
        "tools",
        "Tools + surface + model caps",
        "read",
        ("tools_merge_start", "tools_model_caps", "tools_surface_manifest", "tools_merged"),
        "surface manifest + model caps (process cache)",
    ),
    (
        "context_intro",
        "Org catalog (new chat)",
        "read",
        ("u_session_open", "u_intro_built"),
        "membership catalog (per-person cache, prefetched)",
    ),
    (
        "context_selection",
        "Active selection",
        "rpc",
        ("u_selection",),
        "resolve_active_selection (resolve_full_context)",
    ),
    (
        "user_context",
        "User context",
        "rpc",
        ("u_active_rendered", "u_record_scope", "agent_context_block"),
        "active block + record scope",
    ),
    ("context_apply", "Context apply", "local", ("c_surface", "context_objects"), "local merge"),
    (
        "user_request",
        "User-request INSERT",
        "write",
        ("user_request_ensured",),
        "cx_user_request INSERT",
    ),
    (
        "stream_handoff",
        "Stream handoff",
        "local",
        (
            "h_dictionary",
            "h_final_stage",
            "h_dispatch_guards",
            "prep_complete",
            "stream_task_started",
            "v2_spine_open_awaited",
            "run_ai_task_entry",
            "h_vault",
            "h_coppa",
            "h_minor",
            "h_minor_swap",
            "run_ai_task_media_normalized",
            "h_om_pre",
            "h_stamp_blocks",
            "run_ai_task_ready",
        ),
        "spine open + vault + safety + handoff",
    ),
    (
        "exec_conversation",
        "Executor conv. check",
        "read",
        ("execute_inner_entry",),
        "ensure_conversation_exists SELECT (memoized)",
    ),
    (
        "reservations",
        "Reservations",
        "local",
        ("user_request_inner", "reservations_complete", "iteration_request_reserved"),
        "message/request reserve (queued)",
    ),
    (
        "structured_inputs",
        "Structured inputs + inbox drain",
        "read",
        ("structured_inputs_resolved",),
        "structured-input resolve + cx_pending_injection drain",
    ),
    (
        "wire_config",
        "Wire config / payload",
        "local",
        ("wire_config_built", "pre_provider_execute", "payload_captured"),
        "local payload build",
    ),
)
_KEY_TO_BLOCK: dict[str, int] = {key: idx for idx, blk in enumerate(_BLOCKS) for key in blk[3]}
_DB_IO = frozenset({"read", "write", "rpc"})
_IO_TAG_INNER_WIDTH = max(len(blk[2]) for blk in _BLOCKS)
_IO_TAG_COL_WIDTH = _IO_TAG_INNER_WIDTH + 2  # brackets
_SUMMARY_LABEL_WIDTH = 14
_BLOCK_LABEL_WIDTH = 34
_BLOCK_TABLE_SEP = "  " + "─" * 70


def _io_tag_col(io: str) -> str:
    return f"[{io.upper():<{_IO_TAG_INNER_WIDTH}}]"


def _prep_bottom_summary(data: dict[str, Any]) -> list[str]:
    label = _SUMMARY_LABEL_WIDTH
    lines = [
        "",
        _BLOCK_TABLE_SEP,
        f"  {'total':<{label}} {data['prep_s']:>8.2f}s",
        f"  {'DB':<{label}} {data['db_round_trip_s']:>8.2f}s  ({data['db_block_count']} blocks)",
        f"  {'local':<{label}} {data['local_prep_s']:>8.2f}s",
    ]
    inbound = data.get("inbound_to_first_mark_s")
    if inbound is not None:
        lines.append(f"  {'inbound→1st':<{label}} +{inbound:.3f}s")
    lines.append("")
    return lines


def _prep_points(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    for idx, point in enumerate(points):
        if point["key"] == PREP_COMPLETE_KEY:
            return points[: idx + 1]
    for idx, point in enumerate(points):
        if point["key"] in _PROVIDER_SDK_START_KEYS:
            return points[:idx] if idx > 0 else []
    return list(points)


def _segments_from_points(points: list[dict[str, Any]]) -> list[dict[str, Any]]:
    segments: list[dict[str, Any]] = []
    for i in range(1, len(points)):
        prev_pt = points[i - 1]
        curr_pt = points[i]
        segments.append(
            {
                "from_label": prev_pt.get("label", prev_pt["key"]),
                "from_key": prev_pt["key"],
                "to_key": curr_pt["key"],
                "to_label": curr_pt.get("label", curr_pt["key"]),
                "delta_s": curr_pt["delta_s"],
            }
        )
    return segments


@dataclass(frozen=True)
class _InboundStamp:
    perf: float
    wall_utc: str
    path: str


_inbound: ContextVar[_InboundStamp | None] = ContextVar("chat_timing_inbound", default=None)


def _wall_utc_now() -> str:
    return datetime.now(UTC).strftime("%H:%M:%S.%f")[:-3] + "Z"


def stamp_inbound_request(*, path: str) -> None:
    """Earliest request hook — auth middleware, before auth/parse/route work."""
    from matrx_connect.request_latency import unversioned_path

    bare = unversioned_path(path)
    if not any(bare.startswith(prefix) for prefix in _CHAT_TIMING_PATH_PREFIXES):
        return
    stamp = _InboundStamp(perf=time.perf_counter(), wall_utc=_wall_utc_now(), path=path)
    _inbound.set(stamp)
    if CHAT_TIME_CHECK_ENABLED:
        print(
            f"[CHAT TIME CHECK] inbound | wall={stamp.wall_utc} | path={path}",
            flush=True,
        )


def clear_inbound_stamp() -> None:
    _inbound.set(None)


def _inbound_gap_s() -> float | None:
    stamp = _inbound.get()
    if stamp is None:
        return None
    return time.perf_counter() - stamp.perf


def _inbound_probe_suffix(*, label: str) -> str:
    gap = _inbound_gap_s()
    stamp = _inbound.get()
    if gap is None or stamp is None:
        return ""
    return (
        f" | {label} inbound→now +{gap:.3f}s "
        f"(inbound wall={stamp.wall_utc}, now wall={_wall_utc_now()})"
    )


def _integer_pct_shares(values: list[float], total: float) -> list[int]:
    if total <= 0:
        return [0] * len(values)
    exact = [100.0 * value / total for value in values]
    shares = [int(part) for part in exact]
    remainder = 100 - sum(shares)
    if remainder:
        order = sorted(range(len(values)), key=lambda i: exact[i] - shares[i], reverse=True)
        for idx in order[:remainder]:
            shares[idx] += 1
    return shares


def _block_breakdown(segments: list[dict[str, Any]], controllable_s: float) -> list[dict[str, Any]]:
    """Roll segment deltas up into the named blocks, in execution order."""
    totals = [0.0] * len(_BLOCKS)
    for seg in segments:
        idx = _KEY_TO_BLOCK.get(seg["to_key"])
        if idx is not None:
            totals[idx] += seg["delta_s"]
    out: list[dict[str, Any]] = []
    for idx, (key, label, io, _keys, op) in enumerate(_BLOCKS):
        secs = round(totals[idx], 4)
        out.append(
            {
                "block": key,
                "label": label,
                "io": io,
                "op": op,
                "bucket": "prep",
                "seconds": secs,
                "pct_controllable": None,
            }
        )

    prep_total = sum(block["seconds"] for block in out) or controllable_s or 1.0
    pct_shares = _integer_pct_shares([block["seconds"] for block in out], prep_total)
    for block, pct in zip(out, pct_shares, strict=True):
        block["pct_controllable"] = float(pct)
    return out


@dataclass
class ChatTimingTrace:
    _start: float = field(default_factory=time.perf_counter)
    points: list[dict[str, Any]] = field(default_factory=list)
    _prep_summary_emitted: bool = False

    def mark(self, key: str, label: str) -> float:
        elapsed = time.perf_counter() - self._start
        prev_elapsed = self.points[-1]["elapsed_s"] if self.points else 0.0
        delta = elapsed - prev_elapsed
        seq = len(self.points) + 1
        point = {
            "seq": seq,
            "key": key,
            "label": label,
            "elapsed_s": round(elapsed, 4),
            "delta_s": round(delta, 4),
        }
        self.points.append(point)
        # Print only marks that cost real time, plus the milestones (first mark, prep
        # complete) — the block table carries the full per-block breakdown. Keeps the
        # console to the handful of lines that matter unless _VERBOSE_MARKS is on.
        is_milestone = seq == 1 or key == PREP_COMPLETE_KEY
        if CHAT_TIME_CHECK_ENABLED and (
            _VERBOSE_MARKS or is_milestone or delta >= _MARK_PRINT_MIN_DELTA_S
        ):
            probe = _inbound_probe_suffix(label="first mark") if seq == 1 else ""
            print(
                f"[CHAT TIME CHECK] {seq:02d} | ELAPSED TIME: {elapsed:.2f} Seconds | "
                f"(+{delta:.2f}) {label}{probe}",
                flush=True,
            )
        return elapsed

    def summary(self) -> dict[str, Any]:
        prep_points = _prep_points(self.points)
        segments = _segments_from_points(prep_points)
        prep_s = round(prep_points[-1]["elapsed_s"], 4) if prep_points else 0.0
        controllable_s = prep_s

        controllable_segments = [s for s in segments if _is_controllable_segment(s)]
        slowest_controllable = sorted(
            controllable_segments,
            key=lambda s: s["delta_s"],
            reverse=True,
        )[:5]

        blocks = _block_breakdown(segments, controllable_s)
        db_blocks = [b for b in blocks if b["io"] in _DB_IO and b["seconds"] > 0.0]
        db_round_trip_s = round(sum(b["seconds"] for b in db_blocks), 4)
        local_prep_s = round(sum(b["seconds"] for b in blocks if b["io"] == "local"), 4)

        inbound_to_first_mark_s = self._inbound_to_first_mark_s()

        return {
            "prep_s": prep_s,
            "controllable_s": controllable_s,
            "inbound_to_first_mark_s": inbound_to_first_mark_s,
            "blocks": blocks,
            "db_block_count": len(db_blocks),
            "db_round_trip_s": db_round_trip_s,
            "local_prep_s": local_prep_s,
            "point_count": len(prep_points),
            "points": list(prep_points),
            "segments": segments,
            "slowest_segments": slowest_controllable,
            "slowest_controllable_segments": slowest_controllable,
            "prep_complete": any(point["key"] == PREP_COMPLETE_KEY for point in prep_points),
        }

    def headline(self) -> str:
        data = self.summary()
        line = (
            f"prep {data['prep_s']:.2f}s | "
            f"DB {data['db_round_trip_s']:.2f}s | "
            f"local {data['local_prep_s']:.2f}s"
        )
        inbound = data.get("inbound_to_first_mark_s")
        if inbound is not None:
            line += f" | inbound→first +{inbound:.3f}s"
        return line

    def block_table(self) -> str:
        """Human-readable prep ledger — time through payload captured only."""
        data = self.summary()
        lines: list[str] = [
            _BLOCK_TABLE_SEP,
            f"  {'io':<{_IO_TAG_COL_WIDTH}} {'block':<{_BLOCK_LABEL_WIDTH}} {'secs':>8}  {'%':>6}  op",
        ]
        for b in data["blocks"]:
            if b["seconds"] <= 0.0 and b["io"] == "local":
                continue
            pct = f"{int(b['pct_controllable'])}%"
            secs = f"{b['seconds']:.3f}s"
            lines.append(
                f"  {_io_tag_col(b['io'])} {b['label']:<{_BLOCK_LABEL_WIDTH}} {secs:>8}  {pct:>6}  {b['op']}"
            )
        lines.extend(_prep_bottom_summary(data))
        return "\n".join(lines)

    def _inbound_to_first_mark_s(self) -> float | None:
        stamp = _inbound.get()
        if stamp is None or not self.points:
            return None
        first_mark_at = self._start + self.points[0]["elapsed_s"]
        return round(first_mark_at - stamp.perf, 4)

    def emit_prep_summary(self) -> None:
        from matrx_utils import vcprint

        print(
            "[CHAT TIME CHECK] prep timing summary (payload captured — provider next)", flush=True
        )
        print(self.block_table(), flush=True)
        vcprint(self.summary(), "[CHAT TIME CHECK] prep summary", color="cyan")


_active: ContextVar[ChatTimingTrace | None] = ContextVar("chat_timing_trace", default=None)


def _is_controllable_segment(segment: dict[str, Any]) -> bool:
    if segment["from_key"] in _PROVIDER_BOUNDARY_KEYS:
        return False
    if segment["to_key"] in _PROVIDER_SDK_END_KEYS:
        return False
    if segment["to_key"] in _PROVIDER_SDK_START_KEYS:
        return False
    return True


def arm_chat_timing(*, path: str) -> ChatTimingTrace | None:
    """Arm the trace at the earliest hook for an AI route (called by the auth middleware),
    so /agents, /mandates and /conversations continue are all covered with no per-route call."""
    from matrx_connect.request_latency import is_ai_route

    if not is_ai_route(path):
        return None
    trace = ChatTimingTrace()
    _active.set(trace)
    return trace


def start_chat_timing() -> ChatTimingTrace | None:
    """Return this request's trace, arming one if the middleware did not.

    Idempotent: a trace the middleware armed (which includes auth time in the ``entry``
    block) is kept, never restarted."""
    existing = _active.get()
    if existing is not None and not existing._prep_summary_emitted:
        return existing
    trace = ChatTimingTrace()
    _active.set(trace)
    probe = _inbound_probe_suffix(label="trace arm") if CHAT_TIME_CHECK_ENABLED else ""
    if probe:
        print(f"[CHAT TIME CHECK] trace arm | wall={_wall_utc_now()}{probe}", flush=True)
    return trace


def get_chat_timing_trace() -> ChatTimingTrace | None:
    return _active.get()


def _emit_prep_summary_safe(trace: ChatTimingTrace) -> None:
    try:
        trace.emit_prep_summary()
    except Exception as exc:
        print(f"[CHAT TIME CHECK] prep summary emit failed: {exc}", flush=True)


def chat_timing_mark(key: str, label: str) -> float | None:
    trace = _active.get()
    if trace is None or trace._prep_summary_emitted:
        return None
    elapsed = trace.mark(key, label)
    if key == PREP_COMPLETE_KEY:
        trace._prep_summary_emitted = True
        if CHAT_TIME_CHECK_ENABLED:
            _emit_prep_summary_safe(trace)
    return elapsed


def chat_timing_finish() -> dict[str, Any] | None:
    trace = _active.get()
    if trace is None:
        return None
    summary = trace.summary() if trace._prep_summary_emitted else None
    _active.set(None)
    clear_inbound_stamp()
    return summary


def get_chat_timing_elapsed() -> float | None:
    trace = _active.get()
    if trace is None or not trace.points:
        return None
    return trace.points[-1]["elapsed_s"]


def get_chat_timing_last_step() -> int | None:
    trace = _active.get()
    if trace is None or not trace.points:
        return None
    return trace.points[-1]["seq"]


def chat_time_check(step: int, label: str = "") -> float | None:
    """Backward-compatible numbered checkpoint."""
    return chat_timing_mark(f"step_{step:02d}", label or f"step {step}")
