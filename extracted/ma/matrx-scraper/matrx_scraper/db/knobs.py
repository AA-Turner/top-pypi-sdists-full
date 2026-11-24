"""``platform.feature_knob`` for the scraper server — read through matrx-orm, never raw SQL.

The package ships its OWN read-only model over the table, bound to the server's one registered
database (``matrx_web``), the same narrow-reader pattern as ``matrx_batch/knobs.py`` and
``matrx_seo/knobs.py``: a standalone install needs no host model and never imports aidream.
The scoped resolve is THE platform resolver, ``platform.knob_resolve``, through ``call_function``.
"""

from __future__ import annotations

import asyncio
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
from matrx_orm.core.db_function import call_function

from matrx_scraper.db.web import WEB_DB_NAME


class FeatureKnob(Model):
    """Package-owned read-only mirror of ``platform.feature_knob`` on ``matrx_web``."""

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
    _database = WEB_DB_NAME
    _table_name = "feature_knob"
    _db_schema = "platform"
    _read_only = True


model_registry.register_all([FeatureKnob], skip_existing=True)


async def feature_knob_values(feature: str) -> dict[str, Any]:
    """Every ``key -> value`` row of one feature (values decoded from jsonb)."""
    rows = await FeatureKnob.filter(feature=feature).values("key", "value")
    return {str(row["key"]): row["value"] for row in rows}


async def resolve_knobs(
    feature: str,
    keys: list[str],
    *,
    organization_id: str,
    user_id: str | None,
    scopes: list[dict[str, str]] | None,
) -> dict[str, Any]:
    """Each key resolved by ``platform.knob_resolve`` (platform → organization → site → user)."""

    async def one(key: str) -> Any:
        value = await call_function(
            WEB_DB_NAME, "platform", "knob_resolve", feature, key, organization_id, user_id, scopes
        )
        if value is None:
            raise KeyError(f"{feature}.{key} resolved to nothing in platform.knob_resolve")
        return value

    values = await asyncio.gather(*(one(k) for k in keys))
    return dict(zip(keys, values, strict=True))
