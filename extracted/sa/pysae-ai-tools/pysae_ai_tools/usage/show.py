"""`pysae-ai-tools usage show` — print the current Claude plan usage on demand."""

import json
import time
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Annotated

import typer

from . import account as account_mod
from . import history, notify, pace, workhours
from .client import CACHE_SOURCE_STATUSLINE, UsageSnapshot, Window, get_usage, read_cached_usage
from .config import UsageConfig, load_config
from .mode import PlanMode, detect_mode
from .render import format_compact, format_detail, format_extra, format_reset


def _format_age(seconds: float) -> str:
    """Human-readable cache age: ``45 s``, ``23 min`` or ``1 h 05``."""
    total = int(seconds)
    if total < 60:
        return f"{total} s"
    if total < 3600:
        return f"{total // 60} min"
    return f"{total // 3600} h {(total % 3600) // 60:02d}"


def _hold_note(age: str, label: str, until_epoch: float, now: float) -> str:
    remaining = _format_age(max(0.0, until_epoch - now))
    until = format_reset(datetime.fromtimestamp(until_epoch, timezone.utc))
    return f"{label} (en cache {age}, prochain appel dans {remaining}, à {until})"


def _source_note(snapshot: UsageSnapshot, now: float, cache_ttl: float) -> str:
    """Always-shown line stating whether the data is live or cached, and — when
    cached — why no live fetch happened: cache still within its TTL, our own fetch
    throttle, an API 429 backoff, or an unreachable API."""
    if not snapshot.from_cache:
        return "🟢 Récupéré en direct depuis l'API"
    age_seconds = now - snapshot.fetched_at
    age = _format_age(age_seconds)
    if snapshot.rate_limited_until is not None:
        return "⛔ " + _hold_note(age, "Rate-limité par l'API Anthropic", snapshot.rate_limited_until, now)
    if snapshot.unavailable_until is not None:
        code = f" HTTP {snapshot.unavailable_status}" if snapshot.unavailable_status is not None else ""
        return "⛔ " + _hold_note(age, f"API Anthropic indisponible{code}", snapshot.unavailable_until, now)
    if snapshot.throttled_until is not None:
        return "🕒 " + _hold_note(age, "Throttle local (intervalle de fetch)", snapshot.throttled_until, now)
    if snapshot.source == CACHE_SOURCE_STATUSLINE:
        return f"🟢 Alimenté par la status line Claude Code (il y a {age}) — API non sollicitée"
    if age_seconds < cache_ttl:
        valid = _format_age(max(0.0, cache_ttl - age_seconds))
        return f"🟢 En cache ({age}) — données récentes, valides encore {valid}"
    return f"⚠️ Données en cache ({age}) — API injoignable, réessai au prochain appel"


def _notify_snapshot(snapshot: UsageSnapshot) -> None:
    """Fire a desktop notification with the current usage — same title/body as the hook."""
    cfg = load_config()
    notify.DEFAULT_TIMEOUT_MS = int(cfg.notify_timeout)
    now = time.time()
    effective = snapshot.max_percent
    # On-demand summary spans both windows: warn from the lower of the two thresholds, and
    # rate the ETA on the 5H window (the rhythm shown) with its own block threshold.
    alert_from = min(cfg.five_hour.alert_from, cfg.seven_day.alert_from)
    icon = "🛑" if effective >= 100 else ("⚠️" if effective >= alert_from else "ℹ️")
    schedule = workhours.from_config(cfg.work_hours) if cfg.five_hour.work_hours_aware else None
    rhythm = pace.compute(
        snapshot.five_hour.percent, snapshot.five_hour.resets_at, now, pace.FIVE_HOUR_SECONDS, schedule
    )
    rhythm_txt = f"{pace.emoji(rhythm)} {pace.format_short(rhythm)}" if rhythm is not None else ""
    title = f"{icon} {rhythm_txt}".rstrip() if rhythm_txt else icon
    # The ETA estimates go at the end of the body, keeping the title (first line) short.
    eta = pace.eta_text(rhythm, now, cfg.five_hour.block_at) if rhythm is not None else ""
    notify.send(title, format_compact(snapshot) + eta)


def _account_dict(acct: account_mod.Account | None) -> dict[str, object] | None:
    if acct is None:
        return None
    return {"key": acct.key, "email": acct.email, "uuid": acct.uuid}


def _emit(
    snapshot: UsageSnapshot,
    cfg: UsageConfig,
    mode_value: str,
    acct: account_mod.Account | None,
    target: account_mod.Account | None,
    as_json: bool,
) -> None:
    """Render ``snapshot`` for both the live active account (``target`` None) and a consulted
    one (``target`` set, read from its cache — its history is read under that account)."""

    def _extra_for(window: str, reset: datetime | None) -> float | None:
        spend = history.window_spend_for(window, reset, target) if reset else None
        return spend.spend if spend else None

    extra_5h = _extra_for("5h", snapshot.five_hour.resets_at)
    extra_week = _extra_for("week", snapshot.seven_day.resets_at)

    if as_json:

        def _window_dict(window: Window) -> dict[str, object]:
            d = asdict(window)
            d["resets_at"] = format_reset(window.resets_at)
            return d

        def _epoch_str(epoch: float | None) -> str | None:
            return format_reset(datetime.fromtimestamp(epoch, timezone.utc)) if epoch is not None else None

        payload: dict[str, object] = {
            "mode": mode_value,
            "account": _account_dict(acct),
            "five_hour": _window_dict(snapshot.five_hour),
            "seven_day": _window_dict(snapshot.seven_day),
            "extra": asdict(snapshot.extra),
            "extra_five_hour": extra_5h,
            "extra_seven_day": extra_week,
            "fetched_at": snapshot.fetched_at,
            "from_cache": snapshot.from_cache,
            "fetched_now": snapshot.fetched_now,
            "source": snapshot.source,
            "age_seconds": max(0.0, time.time() - snapshot.fetched_at),
            "rate_limited_until": _epoch_str(snapshot.rate_limited_until),
            "unavailable_until": _epoch_str(snapshot.unavailable_until),
            "unavailable_status": snapshot.unavailable_status,
            "throttled_until": _epoch_str(snapshot.throttled_until),
        }
        print(json.dumps(payload, ensure_ascii=False, default=str))
        return

    now = time.time()
    if acct is not None:
        print(f"👤 Compte : {acct.label}")
    print(format_detail(snapshot, now, cfg))
    extra_block = format_extra(snapshot.extra, extra_5h, extra_week)
    if extra_block:
        print(extra_block)
    if target is not None:
        # A consulted account has no token to fetch with, so the live-vs-throttle source note
        # (which promises a "next call") would be misleading — state the read-only nature instead.
        age = _format_age(max(0.0, now - snapshot.fetched_at))
        print(f"  🗄️ Cache d'un autre forfait ({age}) — lecture seule, aucun appel API")
        return
    if snapshot.fetched_now:
        print("  📡 Requête API émise (appel réseau à l'endpoint d'usage)")
    print(f"  {_source_note(snapshot, now, cfg.cache_ttl)}")


def _show_cached_account(target: account_mod.Account, as_json: bool) -> None:
    """Consult a non-active account: replay its last cached snapshot, no fetch (no token)."""
    snapshot = read_cached_usage(target)
    if snapshot is None:
        if as_json:
            print(json.dumps({"error": "no_cache", "account": _account_dict(target)}))
        else:
            print(f"👤 Compte : {target.label}")
            print("Aucun état en cache pour ce compte (jamais alimenté sur cette machine).")
        raise typer.Exit(1)
    _emit(snapshot, load_config(), PlanMode.SUBSCRIPTION.value, target, target, as_json)


def show(
    as_json: Annotated[bool, typer.Option("--json", help="Sortie JSON brute")] = False,
    fresh: Annotated[
        bool, typer.Option("--fresh", help="Ignorer le cache et le throttle local, forcer un appel API")
    ] = False,
    force: Annotated[
        bool,
        typer.Option("--force", help="Comme --fresh mais ignore aussi le backoff 429/5xx (tape l'API sous rate-limit)"),
    ] = False,
    notify_desktop: Annotated[bool, typer.Option("--notify", help="Envoyer aussi une notification bureau")] = False,
    account: Annotated[
        str,
        typer.Option("--account", help="Consulter un autre forfait (email/uuid) — lecture du cache, sans appel API"),
    ] = "",
) -> None:
    """Affiche l'usage du forfait Claude (fenêtre 5H + semaine), ou le mode clé API."""
    ref = account or account_mod.env_ref()
    target = account_mod.resolve(ref) if ref else None
    if ref and target is None:
        known = ", ".join(a.label for a in account_mod.list_accounts()) or "(aucun connu)"
        typer.echo(f"Compte inconnu : {ref}. Comptes connus : {known}", err=True)
        raise typer.Exit(2)

    if target is not None:
        _show_cached_account(target, as_json)
        return

    mode = detect_mode()

    if mode == PlanMode.API_KEY:
        if as_json:
            print(json.dumps({"mode": "api_key"}))
        else:
            print("Mode : clé API — facturé à l'usage (hors forfait).")
            print("Le coût par session s'affiche via le hook ; tarifs : `pysae-ai-tools usage pricing show`.")
        if notify_desktop:
            notify.send("💸 Claude — clé API", "Facturé à l'usage (hors forfait).")
        return

    skip_cache = fresh or force
    cfg = load_config()
    snapshot = get_usage(
        cache_ttl=0.0 if skip_cache else cfg.cache_ttl,
        bypass_throttle=skip_cache,
        bypass_rate_limit=force,
        min_fetch_interval=cfg.min_fetch_interval,
        statusline_ttl=0.0 if skip_cache else cfg.statusline_fresh_ttl,
    )
    if snapshot is None:
        if as_json:
            print(json.dumps({"error": "usage_unavailable"}))
        else:
            print("Usage indisponible (token Claude absent/expiré ou API injoignable).")
        if notify_desktop:
            notify.send("⚠️ Claude usage", "Usage indisponible (token absent/expiré ou API injoignable).")
        raise typer.Exit(1)

    if notify_desktop:
        _notify_snapshot(snapshot)

    _emit(snapshot, cfg, mode.value, account_mod.current_account(), None, as_json)
