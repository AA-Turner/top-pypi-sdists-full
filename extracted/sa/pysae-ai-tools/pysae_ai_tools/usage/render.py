"""Human-readable formatting for usage snapshots (hook line + `show` detail)."""

from datetime import datetime, timedelta, timezone

from . import pace, workhours
from .client import ExtraUsage, UsageSnapshot, Window
from .config import UsageConfig
from .workhours import WorkSchedule

_FR_WEEKDAYS = ["lun.", "mar.", "mer.", "jeu.", "ven.", "sam.", "dim."]
_CURRENCY_SYMBOLS = {"EUR": "€", "USD": "$", "GBP": "£"}


def format_money(amount: float, currency: str) -> str:
    """Format a monetary amount with a currency symbol when known (e.g. ``12.34 €``)."""
    symbol = _CURRENCY_SYMBOLS.get(currency.upper(), currency)
    return f"{amount:.2f} {symbol}".rstrip()


def format_tokens(n: int) -> str:
    """Compact token count: 1_234_567 → '1.2M', 84_000 → '84k'."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.0f}k"
    return str(n)


def format_reset(dt: datetime | None) -> str:
    """Format a reset time in local time. Same-day → ``HH:MM``, else ``jeu. 04/07``."""
    if dt is None:
        return "?"
    local = pace.round_to_minute(dt.astimezone())
    now = datetime.now(timezone.utc).astimezone()
    if local.date() == now.date():
        return local.strftime("%H:%M")
    return f"{_FR_WEEKDAYS[local.weekday()]} {local.strftime('%d/%m')}"


_EIGHTHS = " ▏▎▍▌▋▊▉"


def _bar(percent: float, width: int = 20) -> str:
    """Fine-grained progress bar using eighth-block partials (e.g. ``██████▍░░░``)."""
    ratio = max(0.0, min(1.0, percent / 100.0))
    eighths = round(ratio * width * 8)
    full, rem = divmod(eighths, 8)
    bar = "█" * full
    if rem and full < width:
        bar += _EIGHTHS[rem]
        full += 1
    return bar + "░" * (width - full)


def _gauge(window: Window) -> str:
    return (
        f"{window.label:<10} {_bar(window.percent, 10)} {window.percent:3.0f}% "
        f"(reset {format_reset(window.resets_at)})"
    )


def format_gauges(snapshot: UsageSnapshot) -> str:
    """Multi-line gauges (one window per line, with a bar) — for the transcript message.

    Desktop notifications collapse newlines, so this form is *not* used there; see
    ``format_compact``.
    """
    return f"{_gauge(snapshot.five_hour)}\n{_gauge(snapshot.seven_day)}"


def format_gauge(window: Window) -> str:
    """Single-window gauge line (bar + percent + reset) — for window-scoped notifications."""
    return _gauge(window)


def format_period(window: Window, window_seconds: float, now: float) -> str:
    """Fixed window bounds ``[▶️ <start> → ⏹️ <end>]`` (start = reset − window length),
    or ``""`` when the window has no known reset time."""
    if window.resets_at is None:
        return ""
    start = window.resets_at - timedelta(seconds=window_seconds)
    return f"[▶️ {pace.format_clock(start, now)} → ⏹️ {pace.format_clock(window.resets_at, now)}]"


def format_rhythm(
    window: Window,
    window_seconds: float,
    now: float,
    block_at: float = 0.0,
    schedule: WorkSchedule | None = None,
) -> str:
    """Rhythm line ``<emoji> Rythme <pct>% (<label>)<eta>`` for a window, or ``""`` when it
    can't be rated yet (too early or no usage)."""
    rhythm = pace.compute(window.percent, window.resets_at, now, window_seconds, schedule)
    if rhythm is None:
        return ""
    return f"{pace.emoji(rhythm)} Rythme {rhythm.pct:.0f}% ({rhythm.label}){pace.eta_text(rhythm, now, block_at)}"


def _compact(window: Window) -> str:
    return f"{window.label.strip()} {window.percent:.0f}%"


def format_window_compact(window: Window) -> str:
    """Single-window compact form (label + percent) — for window-scoped notifications."""
    return _compact(window)


def format_compact(snapshot: UsageSnapshot) -> str:
    """Single-line gauges (no bars/resets) for desktop notifications, which collapse newlines."""
    return f"{_compact(snapshot.five_hour)} · {_compact(snapshot.seven_day)}"


def format_detail(snapshot: UsageSnapshot, now: float, cfg: UsageConfig | None = None) -> str:
    """Multi-line detail used by `usage show`: per window, a gauge with its fixed period
    bounds, then the rhythm + ETA line — the same picture as the desktop notifications, for
    both the 5H and weekly windows. ``cfg`` drives the per-window work-hours projection."""
    schedule = workhours.from_config(cfg.work_hours) if cfg is not None else None
    lines = ["Claude — usage du forfait"]
    for window, window_seconds, aware in (
        (snapshot.five_hour, pace.FIVE_HOUR_SECONDS, cfg is not None and cfg.five_hour.work_hours_aware),
        (snapshot.seven_day, pace.WEEK_SECONDS, cfg is not None and cfg.seven_day.work_hours_aware),
    ):
        lines.append(
            f"  {window.label:<10} {_bar(window.percent)} {window.percent:5.1f}%"
            f"   {format_period(window, window_seconds, now)}".rstrip()
        )
        rhythm = format_rhythm(window, window_seconds, now, schedule=schedule if aware else None)
        if rhythm:
            lines.append(f"    {rhythm}")
    return "\n".join(lines)


def format_extra_month(extra: ExtraUsage) -> str:
    """Monthly extra-usage figure: ``6.88 € / 300.00 € (2 %)`` when the cap is known,
    else just the spend ``6.88 €``. The authoritative number reported by the API."""
    used = format_money(extra.amount, extra.currency)
    if extra.limit is not None and extra.limit > 0:
        pct = extra.amount / extra.limit * 100
        return f"{used} / {format_money(extra.limit, extra.currency)} ({pct:.0f} %)"
    return used


def format_extra(extra: ExtraUsage, spend_5h: float | None, spend_week: float | None) -> str | None:
    """Extra-usage section for `usage show`, or None when extra usage is disabled. The
    monthly line (spend / cap, authoritative from the API) is always shown; the 5H and week
    amounts are reconstructed from local history and only shown when history covers them."""
    if not extra.enabled:
        return None
    cur = extra.currency
    lines = ["  Extra usage (hors forfait, facturé)", f"    {'Mois':<12} {format_extra_month(extra)}"]
    local = [("Fenêtre 5H", spend_5h), ("Semaine", spend_week)]
    shown = [(label, amount) for label, amount in local if amount is not None]
    for label, amount in shown:
        lines.append(f"    {label + '*':<12} {format_money(amount, cur)}")
    if shown:
        lines.append("    * reconstruit localement (démarre à l'installation du hook)")
    return "\n".join(lines)
