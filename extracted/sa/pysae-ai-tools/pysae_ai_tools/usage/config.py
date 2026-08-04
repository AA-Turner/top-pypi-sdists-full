"""Persistent runtime configuration for the usage hook.

Stored as the ``[usage]`` table of pysae-ai-tools' central ``config.toml`` (OS-standard
config dir via ``platformdirs``) and **re-read on every hook invocation**, so the
behaviour can be tuned without ever touching Claude Code's ``settings.json``: the hook
command stays a bare ``pysae-ai-tools usage hook`` and this table is the single source of
truth. Manage it with ``pysae-ai-tools usage config …``.

The table holds one global value set, plus optional **per-account overlays** under
``[usage.accounts.<key>]`` (``key`` = the account directory name from :mod:`.account`).
An overlay carries only the keys it overrides; the effective config of an account is the
global values with its overlay merged on top. This is what lets two Claude plans on the
same machine keep distinct working hours or thresholds, while state stays partitioned by
:mod:`.account`. No overlay → the global values, and the account is not even resolved.

Settings from the legacy standalone file (``~/.claude/pysae-ai-tools/usage-config.json``)
are migrated into the central config on first read, then the legacy file is removed.
"""

import json
from collections.abc import Mapping
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

from .. import config as central
from . import account as account_mod
from .pricing_source import DEFAULT_TTL

USAGE_TABLE = "usage"

# Sub-table of [usage] holding the per-account overlays, keyed by account directory name.
ACCOUNTS_KEY = "accounts"

# Account key that resolves to no overlay at all — the global values exactly as written.
NO_ACCOUNT = ""

# Set in the environment of the throw-away ``usage prime`` request so the usage hooks
# (:mod:`.hook`) short-circuit for it: the priming request must never block itself on the
# UserPromptSubmit guard, nor pay the hook's latency.
PRIME_ENV_VAR = "PYSAE_AI_TOOLS_USAGE_PRIMING"

LEGACY_JSON_PATH = Path.home() / ".claude" / "pysae-ai-tools" / "usage-config.json"

_TABLE_COMMENT = (
    " Claude usage hook — per-window thresholds, notification cadence and blocking policy.",
    " The 5H and weekly windows are configured independently under [usage.five_hour]",
    " and [usage.seven_day]. Managed by `pysae-ai-tools usage config`; re-read on every run.",
    " [usage.accounts.<key>] overrides any of these keys for a single Claude account",
    " (`usage config set --account <email> …`); everything else falls back to the values above.",
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


def _copy_nested(data: Mapping[str, object]) -> dict[str, object]:
    """Deep copy of a plain nested mapping (sub-tables copied, scalars shared)."""
    return {str(k): _copy_nested(v) if isinstance(v, Mapping) else v for k, v in data.items()}


def _deep_merge(base: Mapping[str, object], overlay: Mapping[str, object]) -> dict[str, object]:
    """``overlay`` on top of ``base``: sub-tables merge key by key, scalars are replaced."""
    merged = _copy_nested(base)
    for key, value in overlay.items():
        current = merged.get(key)
        if isinstance(current, Mapping) and isinstance(value, Mapping):
            merged[key] = _deep_merge(current, value)
        else:
            merged[key] = _copy_nested(value) if isinstance(value, Mapping) else value
    return merged


def _split_accounts(table: Mapping[str, object]) -> tuple[dict[str, object], dict[str, object]]:
    """Split the raw ``[usage]`` table into its global values and its per-account overlays."""
    accounts = table.get(ACCOUNTS_KEY)
    values = {k: v for k, v in table.items() if k != ACCOUNTS_KEY}
    return values, dict(accounts) if isinstance(accounts, Mapping) else {}


def _overlay_for(accounts: Mapping[str, object], account_key: str | None) -> dict[str, object]:
    """The overlay of ``account_key`` (None = the active account), or empty.

    The active account is only resolved when at least one overlay exists, so the common
    single-account setup never pays the ``~/.claude.json`` read on the hook path.
    """
    if not accounts:
        return {}
    key = account_key if account_key is not None else account_mod.account_key(account_mod.current_account())
    overlay = accounts.get(key)
    return dict(overlay) if isinstance(overlay, Mapping) else {}


def _raw_table(path: Path | None) -> tuple[dict[str, object], dict[str, object]]:
    """The stored global values and overlays, migrating older layouts in place on first read:
    the legacy standalone JSON file when the table is absent, and the pre-per-window flat
    schema (``alert_from``/``session_step``/…) when detected — both rewritten nested."""
    values, accounts = _split_accounts(central.get_subtable(USAGE_TABLE, path))
    if not values and not accounts and LEGACY_JSON_PATH.exists():
        return _migrate_legacy(path).model_dump(), {}
    if values and "five_hour" not in values and "seven_day" not in values:
        cfg = _validate(_from_legacy_flat(values))
        save_config(cfg, path)
        return cfg.model_dump(), accounts
    return values, accounts


def load_config(path: Path | None = None, account_key: str | None = None) -> UsageConfig:
    """Effective config of an account: the global ``[usage]`` values with that account's
    ``[usage.accounts.<key>]`` overlay merged on top (missing keys fall back to defaults).

    ``account_key`` None targets the active Claude account; :data:`NO_ACCOUNT` skips the
    overlay entirely. An overlay that fails validation is dropped rather than taking the
    whole config down with it.
    """
    values, accounts = _raw_table(path)
    overlay = _overlay_for(accounts, account_key)
    if not overlay:
        return _validate(values)
    try:
        return UsageConfig.model_validate(_with_week_default(_deep_merge(values, overlay)))
    except ValidationError:
        return _validate(values)


def load_global_config(path: Path | None = None) -> UsageConfig:
    """The global values alone — the base every account overlays, and what ``config set``
    without ``--account`` writes back."""
    return load_config(path, NO_ACCOUNT)


def _write_table(values: Mapping[str, object], accounts: Mapping[str, object], path: Path | None) -> None:
    """Write the whole ``[usage]`` table; overlays go last so their sub-table headers land
    below the global scalars and windows."""
    data = dict(values)
    if accounts:
        data[ACCOUNTS_KEY] = dict(accounts)
    central.set_subtable(USAGE_TABLE, data, _TABLE_COMMENT, path)


def save_config(cfg: UsageConfig, path: Path | None = None) -> None:
    """Persist the global values, leaving the per-account overlays untouched."""
    _, accounts = _split_accounts(central.get_subtable(USAGE_TABLE, path))
    _write_table(cfg.model_dump(), accounts, path)


def account_overlay(account_key: str, path: Path | None = None) -> dict[str, object]:
    """The stored overlay of ``account_key`` (only the keys it overrides), or empty."""
    _, accounts = _split_accounts(central.get_subtable(USAGE_TABLE, path))
    return _overlay_for(accounts, account_key)


def save_account_overlay(account_key: str, overlay: Mapping[str, object], path: Path | None = None) -> None:
    """Replace ``account_key``'s overlay; an empty overlay drops the sub-table altogether."""
    values, accounts = _raw_table(path)
    if overlay:
        accounts[account_key] = _copy_nested(overlay)
    else:
        accounts.pop(account_key, None)
    _write_table(values, accounts, path)


def overlay_with_dotted(overlay: Mapping[str, object], key: str, value: object) -> dict[str, object]:
    """Copy of ``overlay`` with the (possibly dotted) ``key`` set to ``value``."""
    head, _, rest = key.partition(".")
    out = _copy_nested(overlay)
    if not rest:
        out[head] = value
        return out
    sub = out.get(head)
    out[head] = overlay_with_dotted(sub if isinstance(sub, Mapping) else {}, rest, value)
    return out


def overlay_without_dotted(overlay: Mapping[str, object], key: str) -> dict[str, object]:
    """Copy of ``overlay`` without ``key``; sub-tables left empty are pruned."""
    head, _, rest = key.partition(".")
    out = _copy_nested(overlay)
    if not rest:
        out.pop(head, None)
        return out
    sub = out.get(head)
    if isinstance(sub, Mapping):
        pruned = overlay_without_dotted(sub, rest)
        if pruned:
            out[head] = pruned
        else:
            out.pop(head, None)
    return out


def overlay_keys(overlay: Mapping[str, object], prefix: str = "") -> set[str]:
    """Every key an overlay overrides, in dotted form (``five_hour.alert_from``)."""
    keys: set[str] = set()
    for key, value in overlay.items():
        dotted = f"{prefix}{key}"
        if isinstance(value, Mapping):
            keys |= overlay_keys(value, f"{dotted}.")
        else:
            keys.add(dotted)
    return keys


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
    """Restore defaults by dropping the whole ``[usage]`` table, per-account overlays included
    (drop a single account's overlay with :func:`save_account_overlay` and an empty overlay)."""
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
