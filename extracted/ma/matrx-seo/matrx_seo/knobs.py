"""Operational knobs — the values an admin turns, never constants in this file.

Authority: ``common-docs/policies/limits-are-knobs-agents-set-them.md`` (Arman,
2026-08-20). *"Must be knobs not code and always per feature."*

Every ceiling, backstop and feature default this package needs is a row in
``platform.feature_knob`` — a per-feature registry with a typed value, a range
the admin UI enforces, the agent-set default it can be reset to, and a review
date. Changing one is a row, never a deploy. This module is the read side.

**What belongs here and what does not.** A PLATFORM operational backstop ("what
is the worst single call we absorb?", "at what point does the platform stop
paying this provider this month?") and a FEATURE default ("what SERP depth do we
check at?") live here. A PER-ACCOUNT allowance ("how much does this plan get?")
does NOT — that is ``billing.plan_limit`` for capability ``seo.provider_spend``,
resolved by ``billing.resolve_capability`` and handed to
:mod:`matrx_seo.budget` by the host through
:func:`matrx_seo.budget.set_account_ceiling_resolver`. Blurring those two is how
a platform grows a sixth level ladder — see
``common-docs/systems/platform/entitlements-knobs/PLAN_MODEL.md``.

**No fallback constants.** A missing knob row RAISES. A default frozen in this
file would be exactly the thing the policy bans, and it would mean an admin
turning the knob in the UI changed nothing — the silent-failure class the
platform's env-var rule exists to prevent.
"""

from __future__ import annotations

import time
from decimal import Decimal
from typing import Any, ClassVar

from matrx_orm import (
    DateField,
    DateTimeField,
    DecimalField,
    JSONBField,
    Model,
    TextField,
    UUIDField,
    model_registry,
)

#: How long a resolved knob is trusted before it is re-read. An admin turning a
#: knob sees it take effect within this window on every process, with no
#: invalidation channel to build or to forget to fire.
KNOB_CACHE_TTL_SECONDS = 60.0


class FeatureKnob(Model):
    """Package-owned mirror of ``platform.feature_knob`` (read-only).

    Same shape as the other host surfaces this package reads through its own
    narrow model classes (``matrx_seo.db.models_host``), so a standalone install
    needs no host model injection."""

    feature = TextField(primary_key=True, null=False)
    key = TextField(primary_key=True, null=False)
    value = JSONBField(null=False)
    default_value = JSONBField(null=False)
    value_type = TextField(null=False)
    unit = TextField()
    min_value = DecimalField()
    max_value = DecimalField()
    allowed_values = JSONBField()
    label = TextField(null=False)
    description = TextField(null=False)
    set_by = TextField(null=False)
    basis = TextField()
    review_due = DateField()
    updated_by = UUIDField()
    updated_at = DateTimeField()
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_seo"
    _table_name = "feature_knob"
    _db_schema = "platform"
    _read_only = True


model_registry.register_all([FeatureKnob], skip_existing=True)


class KnobNotRegisteredError(RuntimeError):
    """A knob the code asks for has no row. Loud on purpose: the code and the
    registry disagree, and guessing a value here would make the admin UI a lie."""

    def __init__(self, feature: str, key: str) -> None:
        self.feature = feature
        self.key = key
        super().__init__(
            f"feature knob {feature!r}.{key!r} is not registered in "
            f"platform.feature_knob. Every limit is a knob (see "
            f"common-docs/policies/limits-are-knobs-agents-set-them.md) — seed "
            f"the row with its value, range, basis and review date rather than "
            f"restoring a constant."
        )


_cache: dict[str, tuple[float, dict[str, Any]]] = {}


def clear_knob_cache() -> None:
    """Drop the process cache. Tests, and any caller that just wrote a knob."""
    _cache.clear()


async def _feature_values(feature: str) -> dict[str, Any]:
    cached = _cache.get(feature)
    now = time.monotonic()
    if cached is not None and now - cached[0] < KNOB_CACHE_TTL_SECONDS:
        return cached[1]
    rows = await FeatureKnob.filter(feature=feature).values("key", "value")
    values = {str(row["key"]): row["value"] for row in rows}
    _cache[feature] = (now, values)
    return values


async def _raw(feature: str, key: str) -> Any:
    values = await _feature_values(feature)
    if key not in values:
        # One retry against a cold/stale cache before declaring it missing: a
        # knob seeded seconds ago must not raise for a whole TTL.
        _cache.pop(feature, None)
        values = await _feature_values(feature)
        if key not in values:
            raise KnobNotRegisteredError(feature, key)
    return values[key]


async def usd_knob(feature: str, key: str) -> Decimal:
    """A money knob, as an exact :class:`~decimal.Decimal` of US dollars."""
    return Decimal(str(await _raw(feature, key)))


async def int_knob(feature: str, key: str) -> int:
    return int(await _raw(feature, key))


async def str_knob(feature: str, key: str) -> str:
    return str(await _raw(feature, key))


__all__ = [
    "KNOB_CACHE_TTL_SECONDS",
    "FeatureKnob",
    "KnobNotRegisteredError",
    "clear_knob_cache",
    "int_knob",
    "str_knob",
    "usd_knob",
]
