"""Claude plan usage hooks — monitor, notify, and optionally block.

Two entry points share this module:

- :func:`hook` — the **PreToolUse** hook (``pysae-ai-tools usage hook``): notify on
  thresholds and deny individual tool calls when at the block threshold (Claude can still
  reply in text and self-unblock via the whitelisted command).
- :func:`prompt_hook` — the **UserPromptSubmit** hook (``pysae-ai-tools usage prompt-hook``):
  a harder stop that denies the whole turn at the block threshold, unless the prompt asks to
  unblock (then it's let through so the user can lift the block by asking).

The PreToolUse hook, fired before every tool call, it:

- detects the billing mode (team subscription vs API key);
- **subscription**: reads the cached usage snapshot and, from ``notify_from`` (90%)
  every ``step`` (5%), fires a desktop notification + transcript message; past 100%
  it appends the extra-usage surcharge accrued *since* the overage started;
- **API key**: treats the session as permanent extra usage — estimates the running
  cost from the transcript and notifies every ``warn_interval`` seconds;
- **blocking**: when ``block_at`` is set and the effective usage reaches it, denies
  the tool call (PreToolUse ``deny``). API-key mode counts as 100%, so any
  ``block_at`` ≤ 100 blocks per-token-billed sessions.

It always exits 0, is silent on any error, and never runs in CI (so it can never
break a pipeline).
"""

import json
import os
import re
import sys
import time
from collections.abc import Iterable
from datetime import datetime, timezone
from pathlib import Path

from . import account, history, notify, pace, unblock, workhours
from .client import ExtraUsage, UsageSnapshot, Window, get_usage
from .config import PRIME_ENV_VAR, UsageConfig, WindowConfig
from .mode import PlanMode, SessionCost, detect_mode, session_cost_from_transcript
from .pricing_source import load_pricing, maybe_background_refresh
from .render import (
    format_compact,
    format_extra_month,
    format_gauge,
    format_gauges,
    format_money,
    format_period,
    format_reset,
    format_tokens,
    format_window_compact,
)
from .workhours import WorkSchedule

WARN_STATE_PATH = account.active_state_dir() / "usage-warn-state.json"
OVERAGE_PATH = account.active_state_dir() / "usage-overage.json"
_PRUNE_AFTER = 86_400.0

# Plan usage is shared across every Claude Code session, so a threshold crossing is
# deduplicated account-wide: the reached level lives under one global key rather than per
# session, otherwise each open session re-announces the very same crossing.
_GLOBAL_KEY = "__global__"

# Escape hatch: never block the unblock/block commands themselves, or the user could
# never re-enable Claude from inside Claude Code once blocking kicks in.
_ESCAPE_RE = re.compile(r"pysae-ai-tools\s+usage\s+(?:un)?block\b")


def _is_escape_command(tool_name: str, command: str) -> bool:
    return tool_name == "Bash" and bool(_ESCAPE_RE.search(command))


def _soonest_reset_of(windows: Iterable[Window]) -> datetime | None:
    """Soonest reset among ``windows`` — when the first of them falls back to 0% (None if unknown)."""
    resets = [w.resets_at for w in windows if w.resets_at is not None]
    return min(resets) if resets else None


def _soonest_reset(snapshot: UsageSnapshot) -> datetime | None:
    """Soonest reset among both windows (the 5H one, typically) — when usage returns to 0%."""
    return _soonest_reset_of((snapshot.five_hour, snapshot.seven_day))


def _window_id(snapshot: UsageSnapshot) -> str:
    """Identifier of the current plan window — the 5H window's reset time (unique per window)."""
    return snapshot.five_hour.resets_at.isoformat() if snapshot.five_hour.resets_at is not None else ""


def _window_epoch(resets_at: datetime | None) -> float:
    """Stable per-window id: the reset instant truncated to the minute (0.0 when unknown).

    Truncating absorbs the sub-second/second jitter in ``resets_at`` seen across sources
    (status line vs API) so a single window keeps one id, while a real rollover — hours (5H)
    or days (weekly) away — always yields a new one.
    """
    if resets_at is None:
        return 0.0
    return float(int(resets_at.timestamp() // 60) * 60)


# --------------------------------------------------------------------------- state
def _read_json(path: Path) -> dict[str, object]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
        return data if isinstance(data, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def _write_json(path: Path, data: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")


def _session_entry(state: dict[str, object], session_id: str) -> dict[str, float]:
    entry = state.get(session_id)
    return dict(entry) if isinstance(entry, dict) else {}


def _prune(state: dict[str, object], now: float) -> dict[str, object]:
    out: dict[str, object] = {}
    for sid, entry in state.items():
        if isinstance(entry, dict) and now - float(entry.get("ts", 0.0)) < _PRUNE_AFTER:
            out[sid] = entry
    return out


def _floor_seq(percent: float, start: float, step: float) -> int | None:
    """Largest ``start + step*k`` (k≥0) that is ≤ ``percent``; None if below ``start``."""
    if step <= 0 or percent < start:
        return None
    return int(start + ((percent - start) // step) * step)


def _level(percent: float, alert_from: float, step: float, checkpoint: float) -> int:
    """Notification level: a ``checkpoint``-% cadence (20/40/…) *plus* ``step`` boundaries
    from ``alert_from`` (90/95/…). Highest reached threshold (0 if none).
    """
    cands = [_floor_seq(percent, checkpoint, checkpoint), _floor_seq(percent, alert_from, step)]
    reached = [c for c in cands if c is not None]
    return max(reached) if reached else 0


def _advance_levels(lvl_5h: int, lvl_week: int, win_5h: float, win_week: float, now: float) -> tuple[bool, bool]:
    """Record the account-wide per-window levels; return (5H advanced, weekly advanced)
    since the last notification.

    The reached level is shared across every session (keyed globally), so a threshold is
    announced once no matter how many sessions are open. The two windows (5H and weekly) are
    tracked independently. Within a single window the recorded level never regresses: pct
    jitter dipping below a checkpoint and climbing back does NOT re-notify. Only a genuine
    rollover — a new window id (``win_5h`` / ``win_week``) — rearms that window's level so the
    fresh window can notify again from scratch.
    """
    state = _read_json(WARN_STATE_PATH)
    entry = _session_entry(state, _GLOBAL_KEY)
    changed = False
    fired: list[bool] = []
    for lvl_key, win_key, level, win in (
        ("lvl_5h", "win_5h", lvl_5h, win_5h),
        ("lvl_week", "win_week", lvl_week, win_week),
    ):
        prev_level = int(entry.get(lvl_key, 0))
        same_window = win == float(entry.get(win_key, 0.0))
        baseline = prev_level if same_window else 0
        fired.append(level > baseline)
        stored = max(prev_level, level) if same_window else level
        if stored != prev_level or not same_window:
            entry[lvl_key] = stored
            entry[win_key] = win
            changed = True
    if changed:
        entry["ts"] = now
        state[_GLOBAL_KEY] = entry
        _write_json(WARN_STATE_PATH, _prune(state, now))
    return fired[0], fired[1]


def _should_notify_time(session_id: str, now: float, warn_interval: float) -> bool:
    """True when at least ``warn_interval`` seconds have passed since the last notify."""
    state = _read_json(WARN_STATE_PATH)
    entry = _session_entry(state, session_id)
    if warn_interval > 0 and now - float(entry.get("last", 0.0)) < warn_interval:
        return False
    entry["last"] = now
    entry["ts"] = now
    state[session_id] = entry
    _write_json(WARN_STATE_PATH, _prune(state, now))
    return True


def _overage_surcharge(extra: ExtraUsage, effective: float) -> tuple[float, str] | None:
    """Extra-usage cost accrued since usage first crossed 100%. None when not in overage."""
    if effective < 100.0 or not extra.enabled:
        try:
            OVERAGE_PATH.unlink()
        except OSError:
            pass
        return None
    base = _read_json(OVERAGE_PATH)
    baseline = base.get("amount")
    if not isinstance(baseline, (int, float)):
        _write_json(OVERAGE_PATH, {"amount": extra.amount, "currency": extra.currency})
        return (0.0, extra.currency)
    currency = base.get("currency")
    return (max(0.0, extra.amount - float(baseline)), str(currency) if currency else extra.currency)


# --------------------------------------------------------------------------- output
def _md(text: str) -> str:
    """Convert plain newlines to GitHub-flavored-markdown hard breaks (two trailing spaces)."""
    return text.replace("\n", "  \n")


def _emit(reason: str | None, system_message: str | None) -> None:
    out: dict[str, object] = {"suppressOutput": True}
    if reason is not None:
        out["hookSpecificOutput"] = {
            "hookEventName": "PreToolUse",
            "permissionDecision": "deny",
            "permissionDecisionReason": reason,
        }
    if system_message is not None:
        out["systemMessage"] = system_message
    print(json.dumps(out, ensure_ascii=False))


def _apikey_body(cost: SessionCost | None) -> str:
    if cost is None or cost.total_usd <= 0:
        return "facturé à l'usage (hors forfait)"
    head = f"session ~{format_money(cost.total_usd, 'USD')}"
    top = cost.top_model
    if top:
        tm = cost.by_model[top]
        short = top.replace("claude-", "")
        head += f" · {short}: {format_tokens(tm['input'])} in / {format_tokens(tm['output'])} out"
    return head + " · facturé à l'usage"


# --------------------------------------------------------------------------- entry
def hook(cfg: UsageConfig) -> None:
    """PreToolUse hook entry point. Reads the hook payload from stdin; ``cfg`` is the
    effective configuration (``pysae-ai-tools usage config``, re-read on every run)."""
    if os.environ.get("CI"):
        return  # never notify or block in CI — it must not affect pipelines
    if os.environ.get(PRIME_ENV_VAR):
        return  # our own 5H-priming request — must not self-block or pay the hook's latency

    notify.DEFAULT_TIMEOUT_MS = int(cfg.notify_timeout)

    raw = sys.stdin.read()
    session_id, transcript_path, tool_name, command = "unknown", "", "", ""
    if raw.strip():
        try:
            payload = json.loads(raw)
            if isinstance(payload, dict):
                session_id = str(payload.get("session_id", "unknown"))
                transcript_path = str(payload.get("transcript_path", ""))
                tool_name = str(payload.get("tool_name", ""))
                tool_input = payload.get("tool_input")
                if isinstance(tool_input, dict):
                    command = str(tool_input.get("command", ""))
        except json.JSONDecodeError:
            pass

    now = time.time()
    escape = _is_escape_command(tool_name, command)
    mode = detect_mode()

    if mode == PlanMode.API_KEY:
        _handle_api_key(session_id, transcript_path, cfg, escape, now)
    else:
        _handle_subscription(session_id, cfg, escape, now)


# A prompt asking to lift the block is always let through, so the user can unblock by
# asking (Claude then runs the whitelisted `usage unblock`). Matches "unblock" and the
# French "débloque/débloquer/déblocage/débloqué".
_UNBLOCK_INTENT_RE = re.compile(r"unblock|d[ée]blo", re.IGNORECASE)

_UNBLOCK_CMD = "pysae-ai-tools usage unblock"
# Shown to the USER (static messages: OS notification body, UserPromptSubmit block reason,
# and the PreToolUse transcript line). Both ways to lift the block.
_UNBLOCK_USER_HINT = f"Pour débloquer : demande « débloque l'usage », ou lance `{_UNBLOCK_CMD}`."
# Shown to CLAUDE on a PreToolUse deny (Claude is still alive there): tell it to surface both
# ways and to run the whitelisted command itself when asked.
_UNBLOCK_CLAUDE_HINT = (
    "Indique à l'utilisateur les deux façons de débloquer : (1) te demander « débloque l'usage » — tu "
    f"exécutes alors `{_UNBLOCK_CMD}` (autorisé malgré le blocage) ; (2) lancer lui-même `{_UNBLOCK_CMD}`. "
    "Débloque jusqu'au reset de la window."
)


def is_blocking(cfg: UsageConfig, now: float) -> bool:
    """Whether the hook is currently in a blocking state — the same decision the PreToolUse
    hook uses to deny a tool call. Pure (no notifications); used by the UserPromptSubmit hook.
    """
    if detect_mode() == PlanMode.API_KEY:
        block_configured = (cfg.five_hour.enabled and cfg.five_hour.block_at > 0) or (
            cfg.seven_day.enabled and cfg.seven_day.block_at > 0
        )
        return unblock.state(now) == "block" or (block_configured and unblock.state(now) != "unblock")
    snapshot = get_usage(
        cache_ttl=cfg.cache_ttl, min_fetch_interval=cfg.min_fetch_interval, statusline_ttl=cfg.statusline_fresh_ttl
    )
    if snapshot is None:
        return False
    over = any(
        wcfg.enabled and wcfg.block_at > 0 and window.percent >= wcfg.block_at
        for window, wcfg in ((snapshot.five_hour, cfg.five_hour), (snapshot.seven_day, cfg.seven_day))
    )
    st = unblock.state(now, _window_id(snapshot))
    return st == "block" or (over and st != "unblock")


def prompt_hook(cfg: UsageConfig) -> None:
    """UserPromptSubmit hook — deny the whole turn when the plan is at its blocking threshold
    (the prompt is never processed). A prompt that asks to unblock is always let through, and
    Claude is nudged to run the whitelisted `usage unblock`. Silent + non-blocking on any
    error, never runs in CI.
    """
    if os.environ.get("CI") or os.environ.get(PRIME_ENV_VAR):
        return
    try:
        raw = sys.stdin.read()
        prompt = ""
        if raw.strip():
            payload = json.loads(raw)
            if isinstance(payload, dict):
                prompt = str(payload.get("prompt", ""))
        if not is_blocking(cfg, time.time()):
            return
        if _UNBLOCK_INTENT_RE.search(prompt):
            print(
                json.dumps(
                    {
                        "hookSpecificOutput": {
                            "hookEventName": "UserPromptSubmit",
                            "additionalContext": (
                                "Le forfait Claude est au seuil de blocage et l'utilisateur demande un "
                                "déblocage : exécute `pysae-ai-tools usage unblock` (commande whitelistée, "
                                "autorisée malgré le blocage), puis poursuis sa demande."
                            ),
                        }
                    },
                    ensure_ascii=False,
                )
            )
            return
        print(
            json.dumps(
                {
                    "decision": "block",
                    "reason": f"🛑 Forfait Claude au seuil de blocage — tour ignoré. {_UNBLOCK_USER_HINT}",
                },
                ensure_ascii=False,
            )
        )
    except Exception:
        return  # never let a bug in the prompt hook block a turn


def _period_body(window: Window, window_seconds: float, now: float) -> str:
    """Notification body: ``📊 <pct>% [▶️ <start> → ⏹️ <end>]`` — progression plus the
    fixed period bounds (start and reset time), each with its own pictogram. Falls back
    to the compact label+percent when the window has no known reset time."""
    if window.resets_at is None:
        return format_window_compact(window)
    return f"📊 {window.percent:.0f}% {format_period(window, window_seconds, now)}"


def _window_extra(window_key: str, window: Window) -> tuple[float, str] | None:
    """Extra usage billed during *this* window (5H or week), reconstructed from local
    history. None unless the window is over its plan (≥ 100 %) — extra usage is only shown
    once the forfait is exhausted — and has a known reset and a non-zero reconstructed spend."""
    if window.resets_at is None or window.percent < 100.0:
        return None
    spend = history.window_spend_for(window_key, window.resets_at)
    if spend is None or spend.spend <= 0:
        return None
    return (spend.spend, spend.currency)


def _window_view(
    window: Window, window_seconds: float, now: float, block_at: float, schedule: WorkSchedule | None = None
) -> tuple[str, str, str]:
    """``(title fragment, body line, gauge detail line)`` scoped to one window.

    The title fragment stays short — the window label and its rhythm pictogram + pace — so the
    notification's first line never overflows. The ETA estimates (which can be long, with both
    a worked-hours and a 24/7 figure) are appended at the *end* of the body and gauge lines.
    """
    tag = window.label.strip()
    rhythm = pace.compute(window.percent, window.resets_at, now, window_seconds, schedule)
    body = _period_body(window, window_seconds, now)
    gauge = format_gauge(window)
    if rhythm is None:
        return tag, body, gauge
    fragment = f"{tag} · {pace.emoji(rhythm)} {pace.format_short(rhythm)}"
    eta = pace.eta_text(rhythm, now, block_at)
    return fragment, body + eta, gauge + eta


def _level_for(window: Window, wcfg: WindowConfig) -> int:
    """Notification level reached on ``window`` given its config (0 when off or below).

    Notifications require both the window master switch (``enabled``) and its notification
    toggle (``notification``); blocking is gated separately on ``enabled`` alone.
    """
    if not (wcfg.enabled and wcfg.notification):
        return 0
    return _level(window.percent, wcfg.alert_from, wcfg.step, wcfg.checkpoint_step)


def _handle_subscription(session_id: str, cfg: UsageConfig, escape: bool, now: float) -> None:
    snapshot = get_usage(
        cache_ttl=cfg.cache_ttl, min_fetch_interval=cfg.min_fetch_interval, statusline_ttl=cfg.statusline_fresh_ttl
    )
    if snapshot is None:
        return
    history.record_snapshot(snapshot)
    effective = snapshot.max_percent
    surcharge = _overage_surcharge(snapshot.extra, effective)

    # Full both-window renderings, used only by the block / unblock messages (there the
    # whole-plan picture is what matters). Compact one-liner for OS notifications (they
    # collapse newlines), multi-line with bars for the transcript message.
    notif = format_compact(snapshot)
    detail = format_gauges(snapshot)
    if surcharge is not None:
        money = format_money(surcharge[0], surcharge[1])
        notif += f" · Extra : {money}"
        detail += f"\nExtra usage depuis dépassement : {money}"

    # Each enabled window blocks on its own threshold; a tool call is denied as soon as any
    # window is at/over its configured block_at. A disabled window never blocks.
    blocking = [
        window
        for window, wcfg in ((snapshot.five_hour, cfg.five_hour), (snapshot.seven_day, cfg.seven_day))
        if wcfg.enabled and wcfg.block_at > 0 and window.percent >= wcfg.block_at
    ]
    window_id = _window_id(snapshot)
    st = unblock.state(now, window_id)
    over = bool(blocking)
    if st == "block" or (over and st != "unblock"):
        if escape:
            return  # let the unblock/block command run despite blocking
        _deny_block(session_id, now, snapshot, blocking, notif, detail, forced=st == "block")
        return
    if over and st == "unblock":
        _notify_unblocked(session_id, now, snapshot, notif, detail)
        return

    lvl_5h = _level_for(snapshot.five_hour, cfg.five_hour)
    lvl_week = _level_for(snapshot.seven_day, cfg.seven_day)
    win_5h = _window_epoch(snapshot.five_hour.resets_at)
    win_week = _window_epoch(snapshot.seven_day.resets_at)
    fire_5h, fire_week = _advance_levels(lvl_5h, lvl_week, win_5h, win_week, now)

    # One notification per firing window — a 5H alert shows only 5H, a weekly alert only the
    # week. Both can fire in the same tick (rare); we emit a separate desktop notification for
    # each and stack their blocks in the single transcript message the hook is allowed to emit.
    fired = [
        (key, window, window_seconds, wcfg)
        for key, window, window_seconds, wcfg, hit in (
            ("5h", snapshot.five_hour, pace.FIVE_HOUR_SECONDS, cfg.five_hour, fire_5h),
            ("week", snapshot.seven_day, pace.WEEK_SECONDS, cfg.seven_day, fire_week),
        )
        if hit
    ]
    if not fired:
        return
    schedule = workhours.from_config(cfg.work_hours)
    blocks: list[str] = []
    for key, window, window_seconds, wcfg in fired:
        win_schedule = schedule if wcfg.work_hours_aware else None
        fragment, body, gauge = _window_view(window, window_seconds, now, wcfg.block_at, win_schedule)
        extra = _window_extra(key, window)
        if extra is not None:
            win_money = format_money(extra[0], extra[1])
            month = format_extra_month(snapshot.extra)
            body += f" · 💸 Extra : {win_money} (fenêtre) · {month} (mois)"
            gauge += f"\nExtra usage sur cette fenêtre : {win_money}\nExtra usage mensuel : {month}"
        icon = "🛑" if window.percent >= 100 else ("⚠️" if window.percent >= wcfg.alert_from else "ℹ️")
        title = f"{icon} {fragment}"
        notify.send(title, body)
        blocks.append(f"{title}\n{gauge}")
    _emit(reason=None, system_message=_md("\n\n".join(blocks)))


def _deny_block(
    session_id: str,
    now: float,
    snapshot: UsageSnapshot,
    blocking: list[Window],
    notif: str,
    detail: str,
    forced: bool,
) -> None:
    # The unblock action is keyed to the current window (its resets_at) so it auto-clears
    # when the window falls back to 0%.
    until = _soonest_reset(snapshot) if forced else _soonest_reset_of(blocking)
    until_iso = until.isoformat() if until is not None else ""
    if forced:
        header = "Forfait Claude bloqué manuellement (jusqu'au reset de la window) — tool call refusé"
    else:
        windows = " / ".join(f"{w.label.strip()} {w.percent:.0f}%" for w in blocking)
        header = f"Usage au seuil de blocage ({windows}) — tool call refusé"
    sysmsg = None
    if _should_notify_time(session_id, now, 120.0):
        label = f"Débloquer jusqu'au reset ({format_reset(until)})" if until is not None else "Débloquer"
        notify.send_action("🛑 Claude usage — blocage", f"{header} · {notif}", label, "unblock", until_iso=until_iso)
        sysmsg = _md(f"🛑 {header}\n{detail}\n{_UNBLOCK_USER_HINT}")
    # The reason reaches Claude on the denied call (it stays alive here): tell it to surface
    # both unblock routes and honour a natural-language "débloque l'usage" request itself.
    _emit(reason=f"{header}\n{detail}\n{_UNBLOCK_CLAUDE_HINT}", system_message=sysmsg)


def _notify_unblocked(session_id: str, now: float, snapshot: UsageSnapshot, notif: str, detail: str) -> None:
    if not _should_notify_time(session_id, now, 120.0):
        return
    until = unblock.active_until(now)
    until_txt = format_reset(datetime.fromtimestamp(until, timezone.utc)) if until else "le reset de la window"
    win_iso = _window_id(snapshot)
    notify.send_action(
        "💸 Claude usage — extra-usage en cours",
        f"Extra-usage en cours jusqu'à {until_txt} · {notif}",
        "Bloquer maintenant",
        "block",
        until_iso=win_iso,
    )
    _emit(
        reason=None,
        system_message=_md(
            f"💸 Extra-usage en cours jusqu'à {until_txt}\n{detail}\nBloquer : `pysae-ai-tools usage block`"
        ),
    )


def _handle_api_key(session_id: str, transcript_path: str, cfg: UsageConfig, escape: bool, now: float) -> None:
    maybe_background_refresh(cfg.pricing_ttl)
    cost = session_cost_from_transcript(transcript_path, load_pricing())
    body = _apikey_body(cost)

    # API key is permanent extra usage (counts as 100%), so it blocks as soon as any enabled
    # window has a blocking threshold configured. It has no plan window → override is time-based.
    block_configured = (cfg.five_hour.enabled and cfg.five_hour.block_at > 0) or (
        cfg.seven_day.enabled and cfg.seven_day.block_at > 0
    )
    interval = cfg.api_notify_interval
    st = unblock.state(now)
    if st == "block" or (block_configured and st != "unblock"):
        if escape:
            return
        sysmsg = None
        if _should_notify_time(session_id, now, interval):
            notify.send_action("🛑 Claude (clé API) — blocage", body, "Débloquer 1h", "unblock")
            sysmsg = _md(f"🛑 Claude (clé API) bloqué — {body}\n{_UNBLOCK_USER_HINT}")
        _emit(
            reason=f"Session sur clé API (facturé à l'usage), blocage actif. {body}\n{_UNBLOCK_CLAUDE_HINT}",
            system_message=sysmsg,
        )
        return

    if block_configured and st == "unblock" and _should_notify_time(session_id, now, interval):
        notify.send_action("💸 Claude (clé API) — extra-usage en cours", body, "Bloquer maintenant", "block")
        _emit(
            reason=None,
            system_message=_md(
                f"💸 Claude (clé API) — extra-usage en cours — {body}\nBloquer : `pysae-ai-tools usage block`"
            ),
        )
        return

    if _should_notify_time(session_id, now, interval):
        notify.send("💸 Claude — clé API", body)
        _emit(reason=None, system_message=f"💸 Claude (clé API) — {body}")
