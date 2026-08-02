"""Auto-prime the 5H plan windows during working hours.

Run on a short cron tick (``*/5``), :func:`run` decides whether *now* is the right moment
to open a fresh 5H window and, if so, fires a throw-away ``claude -p`` request to start it.
The goal: shift the window resets *inside* the working day so more windows (typically three
instead of two) overlap it — 50 % more usable quota, at the cost of a window primed while
you sleep.

The decision reduces to two bounds derived from ``[usage.work_hours]`` plus the live window
state (see :func:`evaluate`):

    prime  ⟺  enabled ∧ free ∧ (morning_start ≤ now ≤ end) ∧ not primed-recently

``free`` is the pivot: a request during an open window *consumes* it rather than starting a
new one, so priming is impossible until the current window resets. The algorithm therefore
waits and primes at the first free tick — degrading gracefully to fewer windows only when a
long-running window physically leaves no room, never doing worse than the natural behaviour.

The priming request skips MCP (``--strict-mcp-config``) to stay fast and exports
``PRIME_ENV_VAR`` so the usage hooks (:mod:`.hook`) short-circuit for it — the throw-away
request can never block itself on the ``UserPromptSubmit`` guard. It authenticates through the
plan's OAuth credentials, so it must not run ``--bare`` (which forces API-key-only auth and
would fail on a subscription).
"""

import json
import os
import shutil
import subprocess
import time
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import typer

from . import account
from . import workhours as wh
from .client import UsageSnapshot, get_usage
from .config import PRIME_ENV_VAR, UsageConfig, load_config

FIVE_HOUR_SECONDS = 5 * 3600.0

# Throw-away prompt — the response is irrelevant, only the request (which opens the window) is.
PRIME_PROMPT = "ok"

# Usual install locations for the `claude` binary, checked when it is not on PATH — so a stale
# or minimal cron PATH (or a claude reinstalled elsewhere since the cron was written) does not
# silently stop priming.
_CLAUDE_FALLBACK_DIRS = (
    Path.home() / ".local" / "bin",
    Path("/usr/local/bin"),
    Path("/opt/homebrew/bin"),
)

STATE_PATH = account.active_state_dir() / "prime-state.json"

# The cron tick redirects stdout/stderr to /dev/null, so this file is the only trace of what the
# primer decided (and why) on each run — the sole way to see why a window was never primed.
LOG_PATH = account.active_state_dir() / "prime.log"
_LOG_MAX_BYTES = 1024 * 1024


def _log(now: float, message: str) -> None:
    """Append one timestamped line to the primer log, self-trimming to the most recent half once
    it grows past ``_LOG_MAX_BYTES``. Never raises: a logging failure must not break a tick."""
    try:
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        stamp = datetime.fromtimestamp(now).astimezone().isoformat(timespec="seconds")
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(f"{stamp} {message}\n")
        if LOG_PATH.stat().st_size > _LOG_MAX_BYTES:
            lines = LOG_PATH.read_text(encoding="utf-8", errors="replace").splitlines()
            LOG_PATH.write_text("\n".join(lines[len(lines) // 2 :]) + "\n", encoding="utf-8")
    except OSError:
        pass


def _read_last_primed() -> float | None:
    try:
        data = json.loads(STATE_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    value = data.get("last_primed_at") if isinstance(data, dict) else None
    return float(value) if isinstance(value, (int, float)) else None


def _write_last_primed(ts: float) -> None:
    try:
        STATE_PATH.parent.mkdir(parents=True, exist_ok=True)
        STATE_PATH.write_text(json.dumps({"last_primed_at": ts}), encoding="utf-8")
    except OSError:
        pass


@dataclass
class PrimePlan:
    """The outcome of :func:`evaluate` — whether to prime, and every factor that led there
    (so ``--dry-run`` can show the full reasoning)."""

    should_prime: bool
    reason: str
    now_min: int
    day_off: bool = False
    enabled: bool = False
    free: bool = True
    in_window: bool = False
    primed_recently: bool = False
    usage_available: bool = True
    day_start: int | None = None
    morning_start: int | None = None
    end_min: int | None = None
    starts: list[int] = field(default_factory=list)
    resets_at: datetime | None = None


@dataclass
class _WorkingDay:
    """Working-day geometry for a given instant — every fact the prime decision needs that
    depends only on config + clock, never on the live usage snapshot. ``None`` on a day off."""

    now_min: int
    day_start: int
    morning_start: int
    end_min: int
    starts: list[int]

    @property
    def in_window(self) -> bool:
        return self.morning_start <= self.now_min <= self.end_min


def _working_day(cfg: UsageConfig, now: float) -> tuple[int, _WorkingDay | None]:
    """Return ``(now_min, frame)`` where ``frame`` is None on a non-worked day."""
    local = datetime.fromtimestamp(now).astimezone()
    now_min = local.hour * 60 + local.minute
    bounds = wh.day_bounds(wh.from_config(cfg.work_hours), local.weekday())
    if bounds is None:
        return now_min, None
    start, end = bounds
    morning_start = max(0, wh.compute_morning_start(start, end))
    return now_min, _WorkingDay(now_min, start, morning_start, end, wh.target_starts(start, end))


def snapshot_needed(cfg: UsageConfig, now: float, last_primed_at: float | None) -> bool:
    """Whether :func:`run` must query the usage endpoint on this tick.

    True only when priming is plausible from config + clock alone and the one remaining
    unknown is the live 5H-window state (is it free?). This is what keeps the ``*/5`` cron
    from polling the aggressively rate-limited usage API around the clock: on the vast
    majority of ticks — priming disabled, day off, outside the morning-to-end window, or
    already primed this window — the outcome is decided without a network call, so the read
    is skipped entirely."""
    if not cfg.prime.enabled:
        return False
    if last_primed_at is not None and (now - last_primed_at) < FIVE_HOUR_SECONDS:
        return False
    _now_min, day = _working_day(cfg, now)
    return day is not None and day.in_window


def evaluate(
    cfg: UsageConfig,
    snapshot: UsageSnapshot | None,
    now: float,
    last_primed_at: float | None,
) -> PrimePlan:
    """Decide whether to prime a 5H window *now*, from config, the live usage snapshot and
    the last-primed marker. Pure: no I/O, no clock read — ``now`` is passed in."""
    enabled = cfg.prime.enabled
    now_min, day = _working_day(cfg, now)
    if day is None:
        return PrimePlan(False, "jour non travaillé", now_min, day_off=True, enabled=enabled)

    resets_at = snapshot.five_hour.resets_at if snapshot is not None else None
    free = resets_at is None or resets_at.timestamp() <= now
    primed_recently = last_primed_at is not None and (now - last_primed_at) < FIVE_HOUR_SECONDS

    plan = PrimePlan(
        should_prime=False,
        reason="",
        now_min=now_min,
        enabled=enabled,
        free=free,
        in_window=day.in_window,
        primed_recently=primed_recently,
        usage_available=snapshot is not None,
        day_start=day.day_start,
        morning_start=day.morning_start,
        end_min=day.end_min,
        starts=day.starts,
        resets_at=resets_at,
    )

    if not enabled:
        plan.reason = "amorçage désactivé (usage.prime.enabled = false)"
    elif primed_recently:
        plan.reason = "déjà amorcé — fenêtre en cours"
    elif now_min < day.morning_start:
        plan.reason = f"trop tôt (optimal à {_hhmm(day.morning_start)})"
    elif now_min > day.end_min:
        plan.reason = "hors heures de travail"
    elif snapshot is None:
        # Reachable only inside the priming window (run() reads usage exactly then): a None
        # snapshot here is a real failed/absent read — missing credentials or an API error —
        # so we skip rather than prime blind, and the next tick retries once it recovers.
        plan.reason = "usage indisponible — fenêtre non vérifiable"
    elif not free:
        plan.reason = "fenêtre 5H déjà active"
    else:
        plan.should_prime = True
        plan.reason = "conditions réunies"
    return plan


def _resolve_claude() -> str | None:
    """Absolute path to the ``claude`` binary — PATH first, then the usual install dirs — or
    None when it cannot be found (so the caller reports a clean error instead of a crash)."""
    found = shutil.which("claude")
    if found:
        return found
    for directory in _CLAUDE_FALLBACK_DIRS:
        candidate = directory / "claude"
        if candidate.exists():
            return str(candidate)
    return None


def prime_window(model: str, timeout: float = 90.0) -> tuple[bool, str]:
    """Fire the throw-away ``claude -p`` request that opens a fresh 5H window.

    Runs with the plan's OAuth auth (never ``--bare``, which forces API-key-only auth and
    fails on a subscription), skips MCP for speed, and sets ``PRIME_ENV_VAR`` so the usage
    hooks short-circuit and cannot self-block the request. Returns ``(ok, error)``."""
    claude = _resolve_claude()
    if claude is None:
        return False, "binaire `claude` introuvable (PATH ni emplacements usuels)"
    cmd = [claude, "-p", PRIME_PROMPT, "--model", model, "--no-session-persistence", "--strict-mcp-config"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
            check=False,
            env={**os.environ, PRIME_ENV_VAR: "1"},
        )
    except FileNotFoundError:
        return False, "binaire `claude` introuvable sur le PATH"
    except subprocess.TimeoutExpired:
        return False, f"`claude` n'a pas répondu en {timeout:.0f}s"
    if result.returncode != 0:
        detail = (result.stderr or result.stdout or "").strip()
        return False, detail[:300] or f"code de sortie {result.returncode}"
    return True, ""


def _hhmm(minutes: int) -> str:
    # A minute-of-day is never negative; a computed start before midnight is a display artefact
    # (exotic work hours starting before ~05:00) — clamp so it never renders as e.g. "-1h00".
    minutes = max(0, minutes)
    return f"{minutes // 60:02d}h{minutes % 60:02d}"


def _yn(value: bool) -> str:
    return "oui" if value else "non"


def format_plan(plan: PrimePlan) -> list[str]:
    """Human-readable breakdown of a :class:`PrimePlan` (one line per fact) for ``--dry-run``."""
    if plan.day_off:
        return [f"Maintenant        : {_hhmm(plan.now_min)}", "Décision          : jour non travaillé — rien à faire"]
    day = f"{_hhmm(plan.day_start)}–{_hhmm(plan.end_min)}" if plan.day_start is not None and plan.end_min else "?"
    optimal = _hhmm(plan.morning_start) if plan.morning_start is not None else "?"
    starts = " → ".join(_hhmm(s) for s in plan.starts)
    window = "aucune (libre)" if plan.resets_at is None else f"active jusqu'à {plan.resets_at.astimezone():%Hh%M}"
    lines = [
        f"Maintenant        : {_hhmm(plan.now_min)}",
        f"Heures de travail : {day}",
        f"Amorçage optimal  : {optimal}   (démarrages visés {starts})",
        f"Fenêtre 5H        : {window}",
        f"État              : activé={_yn(plan.enabled)}  libre={_yn(plan.free)}  "
        f"dans_plage={_yn(plan.in_window)}  amorcé_récemment={_yn(plan.primed_recently)}",
        f"Décision          : {'AMORCER' if plan.should_prime else 'ne rien faire'} — {plan.reason}",
    ]
    return lines


def _tick_summary(plan: PrimePlan) -> str:
    """One-line, greppable digest of a tick's decision for the log."""
    if plan.day_off:
        return f"tick skip — {plan.reason} | now={_hhmm(plan.now_min)}"
    window = "libre" if plan.free else (f"active→{plan.resets_at.astimezone():%Hh%M}" if plan.resets_at else "active")
    verb = "AMORCER" if plan.should_prime else "skip"
    return (
        f"tick {verb} — {plan.reason} | now={_hhmm(plan.now_min)} "
        f"enabled={_yn(plan.enabled)} free={_yn(plan.free)} in_window={_yn(plan.in_window)} "
        f"primed_recently={_yn(plan.primed_recently)} usage={_yn(plan.usage_available)} window={window}"
    )


def run(dry_run: bool, verbose: bool) -> None:
    """Orchestrate one tick: read config + live usage, decide, and prime if warranted.

    Never raises and always leaves a zero exit to the caller — a cron tick must stay quiet.
    Prints the full reasoning under ``--dry-run``/``--verbose``; otherwise only speaks when it
    actually primes (or fails to)."""
    cfg = load_config()
    now = time.time()
    last_primed = _read_last_primed()
    # Only touch the usage endpoint when priming is time-plausible: on a */5 cron this turns a
    # round-the-clock poll of an aggressively rate-limited API into a handful of reads a day.
    snapshot = (
        get_usage(
            cache_ttl=cfg.cache_ttl, min_fetch_interval=cfg.min_fetch_interval, statusline_ttl=cfg.statusline_fresh_ttl
        )
        if snapshot_needed(cfg, now, last_primed)
        else None
    )
    plan = evaluate(cfg, snapshot, now, last_primed)

    if dry_run or verbose:
        for line in format_plan(plan):
            typer.echo(line)

    # A dry-run is a manual inspection, not a real tick — it must not pollute the log.
    if not dry_run:
        _log(now, _tick_summary(plan))

    if not plan.should_prime:
        return
    if dry_run:
        typer.echo("→ amorcerait maintenant (dry-run : rien lancé).")
        return

    ok, err = prime_window(cfg.prime.model)
    if ok:
        _write_last_primed(now)
        clock = f"{datetime.fromtimestamp(now).astimezone():%Hh%M}"
        typer.echo(f"✅ Fenêtre 5H amorcée à {clock} (modèle {cfg.prime.model}).")
        _log(now, f"prime OK — modèle {cfg.prime.model}")
    else:
        typer.secho(f"✗ Amorçage échoué : {err}", fg=typer.colors.RED, err=True)
        _log(now, f"prime FAIL — {err}")
