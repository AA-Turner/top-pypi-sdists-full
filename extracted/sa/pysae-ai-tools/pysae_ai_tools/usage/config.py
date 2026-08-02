"""Persistent runtime configuration for the usage hook.

Stored as the ``[usage]`` table of pysae-ai-tools' central ``config.toml`` (OS-standard
config dir via ``platformdirs``) and **re-read on every hook invocation**, so the
behaviour can be tuned without ever touching Claude Code's ``settings.json``: the hook
command stays a bare ``pysae-ai-tools usage hook`` and this table is the single source of
truth. Manage it with ``pysae-ai-tools usage config …``.

Settings from the legacy standalone file (``~/.claude/pysae-ai-tools/usage-config.json``)
are migrated into the central config on first read, then the legacy file is removed.
"""

import json
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from .. import config as central
from .pricing_source import DEFAULT_TTL

USAGE_TABLE = "usage"

# Set in the environment of the throw-away ``usage prime`` request so the usage hooks
# (:mod:`.hook`) short-circuit for it: the priming request must never block itself on the
# UserPromptSubmit guard, nor pay the hook's latency.
PRIME_ENV_VAR = "PYSAE_AI_TOOLS_USAGE_PRIMING"

LEGACY_JSON_PATH = Path.home() / ".claude" / "pysae-ai-tools" / "usage-config.json"

_TABLE_COMMENT = (
    " Claude usage hook — per-window thresholds, notification cadence and blocking policy.",
    " The 5H and weekly windows are configured independently under [usage.five_hour]",
    " and [usage.seven_day]. Managed by `pysae-ai-tools usage config`; re-read on every run.",
)


class WorkHours(BaseModel):
    """Working hours per weekday, as ``"HH:MM-HH:MM"`` ranges (comma-separated for several
    slots, e.g. ``"09:00-12:30,14:00-18:00"``); an empty string means the day is off. Used by
    the pace/ETA projection to count only worked time (see :mod:`.workhours`)."""

    monday: str = Field(default="09:00-18:00", description="Créneaux travaillés le lundi")
    tuesday: str = Field(default="09:00-18:00", description="Créneaux travaillés le mardi")
    wednesday: str = Field(default="09:00-18:00", description="Créneaux travaillés le mercredi")
    thursday: str = Field(default="09:00-18:00", description="Créneaux travaillés le jeudi")
    friday: str = Field(default="09:00-18:00", description="Créneaux travaillés le vendredi")
    saturday: str = Field(default="", description="Créneaux travaillés le samedi (vide = off)")
    sunday: str = Field(default="", description="Créneaux travaillés le dimanche (vide = off)")


class WindowConfig(BaseModel):
    """Per-window notification + blocking settings (one for 5H, one for the weekly window)."""

    enabled: bool = Field(default=True, description="Interrupteur maître de la fenêtre (False = ni notif ni blocage)")
    notification: bool = Field(default=True, description="Activer les notifications (le blocage reste indépendant)")
    alert_from: float = Field(default=90.0, ge=0.0, le=200.0, description="% de démarrage des alertes fines")
    step: float = Field(default=1.0, ge=0.0, description="Pas fin des alertes au-dessus du seuil")
    checkpoint_step: float = Field(default=20.0, ge=0.0, description="Pas secondaire notifié quoi qu'il arrive")
    block_at: float = Field(default=0.0, ge=0.0, description="Bloquer les tool calls au-delà de ce % (0 = jamais)")
    work_hours_aware: bool = Field(
        default=False, description="Projeter le rythme/ETA sur les seules heures de travail (cf. [usage.work_hours])"
    )


class PrimeConfig(BaseModel):
    """Auto-priming of the 5H windows during working hours (see :mod:`.prime`).

    A cron tick fires ``pysae-ai-tools usage prime`` every few minutes; when enabled it
    starts a fresh 5H window at the optimal moment so more windows (typically three
    instead of two) overlap the working day declared in ``[usage.work_hours]``. Disabled
    by default — priming only happens once explicitly turned on."""

    enabled: bool = Field(default=False, description="Amorcer automatiquement les fenêtres 5H (cron)")
    model: str = Field(default="haiku", description="Modèle du ping d'amorçage (le moins cher suffit)")


class UsageConfig(BaseModel):
    """Tunable settings for the PreToolUse usage hook. Defaults match the historical
    hard-coded behaviour, so an absent ``[usage]`` table changes nothing.

    Scalar fields are declared before the per-window sub-models so the serialized TOML
    keeps the ``[usage]`` scalars above the ``[usage.five_hour]`` / ``[usage.seven_day]``
    sub-tables (a TOML sub-table header captures every bare key that follows it).
    """

    cache_ttl: float = Field(default=60.0, ge=0.0, description="Cache de l'appel API d'usage, en secondes")
    min_fetch_interval: float = Field(
        default=30.0, ge=0.0, description="Throttle réseau : au plus 1 appel API d'usage / N s (anti rate-limit)"
    )
    statusline_fresh_ttl: float = Field(
        default=600.0,
        ge=0.0,
        description="Durée (s) pendant laquelle un cache alimenté par le statusline évite l'appel API",
    )
    api_notify_interval: float = Field(default=120.0, ge=0.0, description="Anti-spam clé API : 1 notif max / N s")
    notify_timeout: float = Field(default=15000.0, ge=0.0, description="Durée de vie des notifs en ms (0 = persistant)")
    pricing_ttl: float = Field(default=DEFAULT_TTL, ge=0.0, description="TTL du cache des tarifs, en secondes")
    work_hours: WorkHours = Field(default_factory=WorkHours, description="Heures de travail par jour (Lun→Dim)")
    five_hour: WindowConfig = Field(default_factory=WindowConfig, description="Fenêtre 5H")
    seven_day: WindowConfig = Field(
        default_factory=lambda: WindowConfig(work_hours_aware=True), description="Fenêtre hebdomadaire"
    )
    prime: PrimeConfig = Field(default_factory=PrimeConfig, description="Amorçage auto des fenêtres 5H")


def _from_legacy_flat(flat: dict[str, object]) -> dict[str, object]:
    """Map a pre-per-window flat config onto the nested schema.

    The old shape carried one shared ``alert_from``/``checkpoint_step``/``block_at`` plus
    ``session_step`` (5H) and ``week_step`` (weekly); those fan out to both windows.
    """

    def _num(key: str, default: float) -> float:
        value = flat.get(key, default)
        return float(value) if isinstance(value, (int, float)) else default

    shared = {"alert_from": _num("alert_from", 90.0), "checkpoint_step": _num("checkpoint_step", 20.0)}
    block_at = _num("block_at", 0.0)
    return {
        "cache_ttl": _num("cache_ttl", 60.0),
        "api_notify_interval": _num("api_notify_interval", 120.0),
        "notify_timeout": _num("notify_timeout", 15000.0),
        "pricing_ttl": _num("pricing_ttl", DEFAULT_TTL),
        "five_hour": {**shared, "step": _num("session_step", 1.0), "block_at": block_at},
        "seven_day": {**shared, "step": _num("week_step", 1.0), "block_at": block_at},
    }


def _with_week_default(data: dict[str, object]) -> dict[str, object]:
    """Default ``seven_day.work_hours_aware`` to True when the sub-table exists but predates the
    option (the field default is False, shared with the 5H window; the factory only fires when
    ``seven_day`` is wholly absent). An explicit value is left untouched."""
    seven = data.get("seven_day")
    if isinstance(seven, dict) and "work_hours_aware" not in seven:
        return {**data, "seven_day": {**seven, "work_hours_aware": True}}
    return data


def _validate(data: dict[str, object]) -> UsageConfig:
    """Build a config from raw values, falling back to defaults on any invalid value."""
    try:
        return UsageConfig.model_validate(_with_week_default(data))
    except ValidationError:
        return UsageConfig()


def load_config(path: Path | None = None) -> UsageConfig:
    """Read the ``[usage]`` table (missing keys fall back to defaults).

    Migrates older layouts in place on first read: the legacy standalone JSON file when the
    table is absent, and the pre-per-window flat schema (``alert_from``/``session_step``/…)
    when it is detected — both are rewritten in the nested per-window form.
    """
    table = central.get_subtable(USAGE_TABLE, path)
    if not table and LEGACY_JSON_PATH.exists():
        return _migrate_legacy(path)
    if table and "five_hour" not in table and "seven_day" not in table:
        cfg = _validate(_from_legacy_flat(table))
        save_config(cfg, path)
        return cfg
    return _validate(table)


def save_config(cfg: UsageConfig, path: Path | None = None) -> None:
    central.set_subtable(USAGE_TABLE, cfg.model_dump(), _TABLE_COMMENT, path)


def dotted_fields() -> list[str]:
    """Every settable key, dotted for nested sub-models (e.g. ``five_hour.alert_from``,
    ``work_hours.monday``)."""
    keys: list[str] = []
    for name, field in UsageConfig.model_fields.items():
        annotation = field.annotation
        if isinstance(annotation, type) and issubclass(annotation, BaseModel):
            keys.extend(f"{name}.{sub}" for sub in annotation.model_fields)
        else:
            keys.append(name)
    return keys


def get_dotted(cfg: UsageConfig, key: str) -> object:
    """Read a (possibly dotted) key off the config. Raises ``KeyError`` for unknown keys."""
    obj: object = cfg
    for part in key.split("."):
        if not isinstance(obj, BaseModel) or part not in type(obj).model_fields:
            raise KeyError(key)
        obj = getattr(obj, part)
    return obj


def with_dotted(cfg: UsageConfig, key: str, value: object) -> UsageConfig:
    """Return a copy of ``cfg`` with ``key`` set to ``value`` (validated). Raises on bad key/value."""
    if key not in dotted_fields():
        raise KeyError(key)
    data = cfg.model_dump()
    parts = key.split(".")
    target = data
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value
    return UsageConfig.model_validate(data)


def reset_config(path: Path | None = None) -> None:
    """Restore defaults by dropping the ``[usage]`` table from the config file."""
    central.remove_subtable(USAGE_TABLE, path)


def _migrate_legacy(path: Path | None) -> UsageConfig:
    try:
        data = json.loads(LEGACY_JSON_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        data = {}
    flat = data if isinstance(data, dict) else {}
    cfg = _validate(_from_legacy_flat(flat))
    save_config(cfg, path)
    try:
        LEGACY_JSON_PATH.unlink()
    except OSError:
        pass
    return cfg
