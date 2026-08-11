"""Local usage-history log, reconstructed from the snapshots the hook already fetches.

The OAuth API exposes no spend history — only a live snapshot whose ``spend`` is a
cumulative figure. So we append each *distinct* snapshot (one per real API fetch,
≤1/60s thanks to the cache) to a JSONL, then attribute the per-window spend as the
delta of ``spend`` across the samples sharing the same ``resets_at`` (i.e. the same
5-hour session or weekly window).

History necessarily starts at install time — the API gives nothing retroactive.
"""

import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from . import account as account_mod
from .client import UsageSnapshot
from .pace import round_to_minute

HISTORY_PATH = account_mod.active_state_dir() / "usage-history.jsonl"
_STATE_PATH = account_mod.active_state_dir() / "usage-history-last.json"

WINDOW_KEYS = {"5h": "five_hour", "week": "seven_day"}


def _iso(dt: datetime | None) -> str:
    return dt.isoformat() if dt is not None else ""


def _read_last_ts() -> float | None:
    try:
        data = json.loads(_STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    ts = data.get("ts") if isinstance(data, dict) else None
    return float(ts) if isinstance(ts, (int, float)) else None


def record_snapshot(snapshot: UsageSnapshot) -> None:
    """Append a sample for this snapshot, unless this exact fetch was already logged."""
    last = _read_last_ts()
    if last is not None and abs(last - snapshot.fetched_at) < 0.5:
        return
    sample = {
        "ts": snapshot.fetched_at,
        "five_hour": {"pct": snapshot.five_hour.percent, "resets_at": _iso(snapshot.five_hour.resets_at)},
        "seven_day": {"pct": snapshot.seven_day.percent, "resets_at": _iso(snapshot.seven_day.resets_at)},
        "spend": snapshot.extra.amount,
        "currency": snapshot.extra.currency,
    }
    account_mod.ensure_dir(HISTORY_PATH.parent)
    with open(HISTORY_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(sample, ensure_ascii=False) + "\n")
    _STATE_PATH.write_text(json.dumps({"ts": snapshot.fetched_at}), encoding="utf-8")


@dataclass
class WindowSpend:
    """Spend attributed to one plan window (a single 5H session or week)."""

    resets_at: str
    start_ts: float
    end_ts: float
    max_pct: float
    spend: float
    currency: str
    samples: int


def _window_id(resets_at: str) -> str | None:
    """Stable per-window key: the reset instant rounded to the minute. The raw ``resets_at``
    jitters by sub-second amounts between fetches, so the exact string would split one real
    window into hundreds of singleton groups (each with a zero spend delta)."""
    try:
        return round_to_minute(datetime.fromisoformat(resets_at)).isoformat()
    except ValueError:
        return None


# A plan window bills extra usage only once it is exhausted (100% of the plan).
_EXHAUSTED = 100.0


def _pct(entry: dict[str, object], key: str) -> float:
    w = entry.get(key)
    pct = w.get("pct") if isinstance(w, dict) else None
    return float(pct) if isinstance(pct, (int, float)) else 0.0


def _resets_at(entry: dict[str, object], key: str) -> str | None:
    w = entry.get(key)
    resets_at = w.get("resets_at") if isinstance(w, dict) else None
    return resets_at if isinstance(resets_at, str) and resets_at else None


def _blocked_family(five_pct: float, seven_pct: float) -> str:
    """The window family the extra usage is charged to: the exhausted one (percent at or
    over the plan limit). If both are exhausted, the more-exhausted window (ties go to the
    weekly one); if neither is, the more-exhausted anyway — extra usage only accrues once a
    window is over its plan limit, so the busier window is the one that produced it."""
    five_over = five_pct >= _EXHAUSTED
    seven_over = seven_pct >= _EXHAUSTED
    if five_over != seven_over:
        return "five_hour" if five_over else "seven_day"
    return "five_hour" if five_pct > seven_pct else "seven_day"


def _history_path(target: account_mod.Account | None) -> Path:
    """History file to read: a specific account's, or the active one's default path."""
    return account_mod.state_dir(target) / "usage-history.jsonl" if target is not None else HISTORY_PATH


def _iter_samples(history_path: Path) -> list[dict[str, object]]:
    out: list[dict[str, object]] = []
    try:
        with open(history_path, encoding="utf-8", errors="replace") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    entry = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(entry, dict):
                    out.append(entry)
    except OSError:
        return []
    return out


def _attributed_spend(key: str, history_path: Path) -> dict[str, float]:
    """Extra spend attributed to each window instance of family ``key``.

    ``spend`` is a single *monthly* cumulative figure, so a step-to-step increase is one
    real billed amount — it must be charged to exactly one window, never to both the 5H and
    the weekly one. Each positive delta is charged to the window that was blocked when it
    accrued (the state at the start of the interval), keyed by that window's reset instant.
    """
    samples = sorted(
        (e for e in _iter_samples(history_path) if isinstance(e.get("ts"), (int, float))),
        key=lambda e: float(e["ts"]),  # type: ignore[arg-type]
    )
    attributed: dict[str, float] = {}
    prev: dict[str, object] | None = None
    for entry in samples:
        cur_spend = entry.get("spend")
        prev_spend = prev.get("spend") if prev is not None else None
        if prev is not None and isinstance(cur_spend, (int, float)) and isinstance(prev_spend, (int, float)):
            delta = float(cur_spend) - float(prev_spend)
            if delta > 0 and _blocked_family(_pct(prev, "five_hour"), _pct(prev, "seven_day")) == key:
                wid = _window_id(_resets_at(prev, key) or "")
                if wid is not None:
                    attributed[wid] = attributed.get(wid, 0.0) + delta
        prev = entry
    return attributed


def aggregate(window: str, account: account_mod.Account | None = None) -> list[WindowSpend]:
    """Per-window spend for ``window`` ('5h' or 'week'), oldest first.

    ``account`` reads another plan's history (read-only); None reads the active account's."""
    history_path = _history_path(account)
    key = WINDOW_KEYS[window]
    attributed = _attributed_spend(key, history_path)
    groups: dict[str, list[tuple[float, float, str]]] = {}
    for entry in _iter_samples(history_path):
        w = entry.get(key)
        if not isinstance(w, dict):
            continue
        resets_at = w.get("resets_at")
        ts = entry.get("ts")
        if not isinstance(resets_at, str) or not resets_at or not isinstance(ts, (int, float)):
            continue
        wid = _window_id(resets_at)
        if wid is None:
            continue
        pct = w.get("pct")
        groups.setdefault(wid, []).append(
            (
                float(ts),
                float(pct) if isinstance(pct, (int, float)) else 0.0,
                str(entry.get("currency", "")),
            )
        )

    result: list[WindowSpend] = []
    for wid, samples in groups.items():
        samples.sort(key=lambda s: s[0])
        result.append(
            WindowSpend(
                resets_at=wid,
                start_ts=samples[0][0],
                end_ts=samples[-1][0],
                max_pct=max(s[1] for s in samples),
                spend=attributed.get(wid, 0.0),
                currency=samples[-1][2],
                samples=len(samples),
            )
        )
    result.sort(key=lambda w: w.resets_at)
    return result


def window_spend_for(
    window: str, resets_at: datetime, account: account_mod.Account | None = None
) -> WindowSpend | None:
    """Reconstructed extra-usage spend for the specific window ending at ``resets_at`` (i.e.
    the current one), or None when no local samples cover it yet."""
    wid = round_to_minute(resets_at).isoformat()
    return next((w for w in aggregate(window, account) if w.resets_at == wid), None)
