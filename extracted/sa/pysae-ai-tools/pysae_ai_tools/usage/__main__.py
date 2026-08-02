"""CLI entry point: pysae-ai-tools usage <command>.

Subcommands:
    show        — print the current Claude plan usage (session 5H + weekly), or API-key cost
    hook        — PreToolUse hook handler (notify on thresholds, optionally block a tool call)
    prompt-hook — UserPromptSubmit hook handler (block the whole turn at the threshold)
    pricing — manage the live per-token pricing cache (show / refresh)
    setup   — install/uninstall/status of the hook in Claude Code settings
    config  — persistent hook settings, re-read on every run (show / get / set / reset)
"""

import json
import time
from datetime import datetime, timezone
from typing import Annotated, cast

import typer

from ..config import CONFIG_FILE
from . import account as account_mod
from . import unblock as unblock_mod
from .client import UsageSnapshot, Window, get_usage
from .config import (
    USAGE_TABLE,
    UsageConfig,
    WorkHours,
    dotted_fields,
    get_dotted,
    load_config,
    reset_config,
    save_config,
    with_dotted,
)
from .history import WINDOW_KEYS, WindowSpend, aggregate
from .hook import hook as _hook
from .hook import prompt_hook as _prompt_hook
from .pricing import ModelPricing
from .pricing_source import PRICING_URL, cache_age_seconds, load_pricing, refresh_cache
from .prime import run as run_prime
from .render import format_money
from .setup import app as setup_app
from .show import show
from .statusline import statusline as _statusline
from .workhours import day_bounds, from_config, parse_ranges, target_starts

app = typer.Typer(help="Claude plan usage — session 5H & weekly windows, API-key cost", no_args_is_help=True)
app.command()(show)
app.add_typer(setup_app, name="setup")

pricing_app = typer.Typer(help="Live per-token pricing cache (downloaded from the official doc).")
app.add_typer(pricing_app, name="pricing")

config_app = typer.Typer(
    help="Réglages persistants du hook (relus à chaque exécution, sans toucher à settings.json).",
    no_args_is_help=True,
)
app.add_typer(config_app, name="config")


@app.command(context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
def hook(ctx: typer.Context) -> None:
    """PreToolUse hook — lit le payload sur stdin, notifie aux paliers, bloque si configuré.

    Tous les réglages viennent de `pysae-ai-tools usage config` (relus à chaque appel) ;
    aucune option en ligne de commande. Les flags inconnus (config héritée) sont ignorés
    pour ne jamais casser un tool call.
    """
    _ = ctx  # extras tolerated and ignored — the installed hook command is bare
    _hook(load_config())


@app.command("prompt-hook", context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
def prompt_hook(ctx: typer.Context) -> None:
    """UserPromptSubmit hook — refuse le tour entier au seuil de blocage (stop plus dur que
    le PreToolUse), sauf si le prompt demande un déblocage. Réglages via `usage config`.
    """
    _ = ctx
    _prompt_hook(load_config())


@app.command("statusline", context_settings={"ignore_unknown_options": True, "allow_extra_args": True})
def statusline(ctx: typer.Context) -> None:
    """Status line Claude Code qui alimente le cache d'usage — lit le JSON de session sur stdin.

    À configurer comme `statusLine` de Claude Code (`usage setup install`). Extrait le bloc
    `rate_limits` (fenêtres 5H + semaine) vers le cache partagé, évitant l'appel à l'API d'usage
    (agressivement rate-limitée), puis imprime une ligne de statut compacte. `--exec <cmd>`
    délègue l'affichage à une status line existante en lui repassant le même stdin.
    """
    _statusline(ctx.args)


@config_app.command("show")
def config_show(
    as_json: Annotated[bool, typer.Option("--json", help="Sortie JSON brute")] = False,
) -> None:
    """Affiche la configuration effective du hook (fichier + défauts)."""
    cfg = load_config()
    if as_json:
        print(cfg.model_dump_json())
        return
    typer.echo(f"Fichier : {CONFIG_FILE}  (table [{USAGE_TABLE}])")
    for name, value in cfg.model_dump().items():
        if isinstance(value, dict):
            typer.echo(f"  [{name}]")
            for sub, sub_value in value.items():
                typer.echo(f"    {sub:<18} {sub_value}")
        else:
            typer.echo(f"  {name:<20} {value}")


@config_app.command("get")
def config_get(key: Annotated[str, typer.Argument(help="Réglage (ex : five_hour.alert_from)")]) -> None:
    """Affiche la valeur effective d'un réglage."""
    try:
        value = get_dotted(load_config(), key)
    except KeyError:
        typer.echo(f"Réglage inconnu : {key} (voir `usage config show`).", err=True)
        raise typer.Exit(2) from None
    print(value)


@config_app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Réglage (ex : five_hour.alert_from, seven_day.enabled)")],
    value: Annotated[str, typer.Argument(help="Nouvelle valeur (nombre, true/false, ou string ex work_hours.monday)")],
) -> None:
    """Modifie un réglage et l'écrit dans le fichier de config.

    La valeur brute est coercée selon le type du champ par Pydantic (bool, float ou string),
    ce qui permet aussi de régler les champs texte comme ``work_hours.monday``."""
    if key not in dotted_fields():
        typer.echo(f"Réglage inconnu : {key} (voir `usage config show`).", err=True)
        raise typer.Exit(2)
    try:
        cfg = with_dotted(load_config(), key, value)
    except (ValueError, KeyError) as exc:
        typer.echo(f"Valeur invalide pour {key} : {value}", err=True)
        raise typer.Exit(2) from exc
    save_config(cfg)
    typer.echo(f"{key} = {get_dotted(cfg, key)}  →  {CONFIG_FILE} [{USAGE_TABLE}]")


@config_app.command("reset")
def config_reset() -> None:
    """Réinitialise tous les réglages aux défauts (supprime la table [usage] du config.toml)."""
    reset_config()
    typer.echo("Configuration réinitialisée aux défauts.")


def _fmt_ts(ts: float) -> str:
    return datetime.fromtimestamp(ts, timezone.utc).astimezone().strftime("%d/%m %H:%M")


def _print_window(label: str, rows: list[WindowSpend]) -> None:
    typer.echo(f"\n{label} ({len(rows)} fenêtre(s)) :")
    if not rows:
        typer.echo("  (aucun historique — démarre à l'installation du hook)")
        return
    for w in rows:
        money = format_money(w.spend, w.currency) if w.spend > 0 else "—"
        typer.echo(
            f"  {_fmt_ts(w.start_ts)} → {_fmt_ts(w.end_ts)}  "
            f"max {w.max_pct:5.1f}%   extra {money:>12}   ({w.samples} pts)"
        )


@app.command()
def history(
    window: Annotated[str, typer.Option(help="Fenêtre : 5h | week | all")] = "all",
    as_json: Annotated[bool, typer.Option("--json", help="Sortie JSON brute")] = False,
    account: Annotated[str, typer.Option("--account", help="Historique d'un autre forfait (email/uuid)")] = "",
) -> None:
    """Historique du spend extra-usage forfait par forfait (reconstruit localement)."""
    windows = ["5h", "week"] if window == "all" else [window]
    if any(w not in WINDOW_KEYS for w in windows):
        typer.echo("Fenêtre invalide : utiliser 5h, week ou all.", err=True)
        raise typer.Exit(2)

    ref = account or account_mod.env_ref()
    target = account_mod.resolve(ref) if ref else None
    if ref and target is None:
        known = ", ".join(a.label for a in account_mod.list_accounts()) or "(aucun connu)"
        typer.echo(f"Compte inconnu : {ref}. Comptes connus : {known}", err=True)
        raise typer.Exit(2)

    data = {w: aggregate(w, target) for w in windows}
    if as_json:
        print(
            json.dumps(
                {w: [vars(row) for row in rows] for w, rows in data.items()},
                ensure_ascii=False,
            )
        )
        return
    acct = target or account_mod.current_account()
    if acct is not None:
        typer.echo(f"👤 Compte : {acct.label}")
    labels = {"5h": "Sessions 5H", "week": "Semaines"}
    for w in windows:
        _print_window(labels[w], data[w])


@app.command()
def prime(
    dry_run: Annotated[bool, typer.Option("--dry-run", help="Montre la décision sans rien amorcer")] = False,
    verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Affiche la décision même hors --dry-run")] = False,
) -> None:
    """Amorce une fenêtre 5H au moment optimal des heures de travail (conçu pour un cron `*/5`).

    Décide seul s'il est pertinent de démarrer une fenêtre maintenant (fenêtre libre + dans la
    plage utile dérivée de `[usage.work_hours]`) ; sinon ne fait rien. Toujours silencieux hors
    `--dry-run`/`--verbose`, sauf quand il amorce réellement.
    """
    run_prime(dry_run=dry_run, verbose=verbose)


_WEEKDAY_LABELS: tuple[tuple[str, str], ...] = (
    ("monday", "lundi"),
    ("tuesday", "mardi"),
    ("wednesday", "mercredi"),
    ("thursday", "jeudi"),
    ("friday", "vendredi"),
    ("saturday", "samedi"),
    ("sunday", "dimanche"),
)


def _hhmm(minutes: int) -> str:
    return f"{minutes // 60:02d}h{minutes % 60:02d}"


def _echo_prime_schedule(cfg: UsageConfig) -> None:
    """Show, per worked day, the 5H windows the primer would aim for — a confirmation recap."""
    schedule = from_config(cfg.work_hours)
    typer.echo("")
    typer.secho("Fenêtres 5H visées par l'amorçage :", fg=typer.colors.CYAN)
    for idx, (_field, label) in enumerate(_WEEKDAY_LABELS):
        bounds = day_bounds(schedule, idx)
        if bounds is None:
            typer.secho(f"  {label:<9} —", fg=typer.colors.BRIGHT_BLACK)
            continue
        starts = target_starts(*bounds)
        arrows = " → ".join(_hhmm(max(0, s)) for s in starts)
        typer.echo(f"  {label:<9} {len(starts)} fenêtre(s) — démarrages {arrows}")


@app.command("work-hours")
def work_hours() -> None:
    """Configure les heures de travail jour par jour (interactif)."""
    cfg = load_config()
    current = cfg.work_hours
    typer.secho(
        "Heures de travail — format HH:MM-HH:MM (plusieurs créneaux séparés par des virgules,",
        fg=typer.colors.CYAN,
    )
    typer.secho("ex : 09:00-12:30,14:00-18:00). Laisse vide pour un jour non travaillé.", fg=typer.colors.CYAN)
    values: dict[str, str] = {}
    for field_name, label in _WEEKDAY_LABELS:
        default = str(getattr(current, field_name))
        while True:
            answer = typer.prompt(f"  {label:<9}", default=default, show_default=True).strip()
            if answer == "" or parse_ranges(answer):
                values[field_name] = answer
                break
            typer.secho("    ⨯ format invalide, réessaie (ex : 09:00-18:00)", fg=typer.colors.RED)
    cfg = cfg.model_copy(update={"work_hours": WorkHours(**values)})
    save_config(cfg)
    typer.echo("")
    typer.secho(f"Enregistré → {CONFIG_FILE} [{USAGE_TABLE}.work_hours]", fg=typer.colors.GREEN)
    _echo_prime_schedule(cfg)


def _blocking_window(snap: UsageSnapshot, cfg: UsageConfig) -> Window | None:
    """The plan window whose reset lifts the current block: among the windows at or over
    their block threshold, the one resetting latest — a block clears only once every
    exhausted window has reset. None when no window is currently over its threshold.

    Mirrors the block criterion used by the hook (``window.percent >= block_at``), so the
    override binds to whichever window actually triggered the block — the 5H *or* the
    weekly one — instead of always assuming the 5H window.
    """
    over = [
        window
        for window, wcfg in ((snap.five_hour, cfg.five_hour), (snap.seven_day, cfg.seven_day))
        if wcfg.enabled and wcfg.block_at > 0 and window.percent >= wcfg.block_at and window.resets_at is not None
    ]
    if not over:
        return None
    return max(over, key=lambda w: cast(datetime, w.resets_at))


def _current_window() -> tuple[str, float, str]:
    """Return (window id, reset epoch, label) the unblock/block override should bind to.

    The blocking window that resets latest when a block is in effect, else the 5H window.
    Falls back to ("", now+1h, "") when usage is unavailable (e.g. API-key sessions).
    """
    cfg = load_config()
    snap = get_usage(cache_ttl=0.0, min_fetch_interval=cfg.min_fetch_interval, statusline_ttl=cfg.statusline_fresh_ttl)
    if snap is not None:
        window = _blocking_window(snap, cfg) or snap.five_hour
        if window.resets_at is not None:
            return window.resets_at.isoformat(), window.resets_at.timestamp(), window.label
    return "", time.time() + 3600.0, ""


@app.command()
def unblock(
    until: Annotated[
        str, typer.Option(help="Débloquer jusqu'à cet instant ISO-8601 (sinon : reset de la window)")
    ] = "",
    minutes: Annotated[float, typer.Option(help="Débloquer pendant N minutes (sinon : reset de la window)")] = 0.0,
) -> None:
    """Suspend le blocage du hook, globalement, jusqu'au reset de la fenêtre qui bloque."""
    label = ""
    if until:
        ep = unblock_mod.parse_until(until)
        if ep is None:
            typer.echo("--until invalide (format ISO-8601 attendu).", err=True)
            raise typer.Exit(2)
        window = ""
    elif minutes > 0:
        ep, window = time.time() + minutes * 60.0, ""
    else:
        window, ep, label = _current_window()
    unblock_mod.set_unblock(window, ep)
    when = datetime.fromtimestamp(ep, timezone.utc).astimezone().strftime("%d/%m %H:%M")
    scope = f"reset {label}" if label else "reset de la window"
    typer.echo(f"Extra usage débloqué jusqu'à {when} ({scope}).")


@app.command()
def block(
    until: Annotated[str, typer.Option(help="Bloquer jusqu'à cet instant ISO-8601 (sinon : reset de la window)")] = "",
) -> None:
    """Force le blocage du hook, globalement, jusqu'au reset de la fenêtre qui bloque."""
    label = ""
    if until:
        ep = unblock_mod.parse_until(until)
        if ep is None:
            typer.echo("--until invalide (format ISO-8601 attendu).", err=True)
            raise typer.Exit(2)
        window = ""
    else:
        window, ep, label = _current_window()
    unblock_mod.set_block(window, ep)
    when = datetime.fromtimestamp(ep, timezone.utc).astimezone().strftime("%d/%m %H:%M")
    scope = f"reset {label}" if label else "reset de la window"
    typer.echo(f"Forfait Claude bloqué jusqu'à {when} ({scope}).")


@pricing_app.command("refresh")
def pricing_refresh() -> None:
    """Télécharge les tarifs depuis la doc officielle et met à jour le cache."""
    table = refresh_cache(time.time())
    if table is None:
        typer.echo("PRICING: refresh failed (source unreachable or unparseable)", err=True)
        raise typer.Exit(1)
    typer.echo(f"PRICING: refreshed {len(table)} models from {PRICING_URL}")


@pricing_app.command("show")
def pricing_show(
    refresh: Annotated[bool, typer.Option("--refresh", help="Forcer un téléchargement avant l'affichage")] = False,
) -> None:
    """Affiche les tarifs en cache (USD/MTok)."""
    if refresh:
        refresh_cache(time.time())
    table: dict[str, ModelPricing] = load_pricing()
    if not table:
        typer.echo("Tarifs indisponibles (source injoignable et aucun cache).")
        raise typer.Exit(1)
    age = cache_age_seconds()
    if age is not None:
        typer.echo(f"Cache : {age / 3600:.1f} h  (source : {PRICING_URL})")
    typer.echo(f"  {'modèle':<22} {'in':>8} {'out':>8} {'read':>8} {'w5m':>8} {'w1h':>8}   $/MTok")
    for model in sorted(table):
        p = table[model]
        typer.echo(
            f"  {model:<22} {p.input:>8.2f} {p.output:>8.2f} {p.read_rate:>8.2f} "
            f"{p.write_5m_rate:>8.2f} {p.write_1h_rate:>8.2f}"
        )


if __name__ == "__main__":
    app()
