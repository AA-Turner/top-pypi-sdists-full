"""Narrow read-only mirrors of canonical SEO evidence owned by ``matrx-seo``.

**matrx-seo owns this table.** It writes every row through the single
``run_collection("pagespeed_insights", …)`` funnel; this module never writes and
never fetches — it exists so the deterministic analysis sweep
(``web_crawl/analysis.py``) can READ the lab metrics that the performance half of
the ``web.analysis_item`` catalogue is scored from.

Why a mirror rather than a dependency: matrx-seo already mirrors the host's
``web.site`` / ``web.page`` in its own ``db/models_host.py`` for exactly this
reason — a narrow read surface on someone else's table costs one model class,
where a package dependency costs the whole graph. Same pattern, opposite
direction. Bound to ``matrx_web`` so it shares the ONE pool the crawler already
registered; `seo` is a schema on the same database.

A field is here only because a check reads it. Do not grow this into a copy of
``matrx_seo.db.models_seo``.
"""

from typing import ClassVar

from matrx_orm import (
    DateField,
    DateTimeField,
    DecimalField,
    IntegerField,
    JSONBField,
    Model,
    TextField,
    UUIDField,
)


class SeoPagePerformance(Model):
    id = UUIDField(primary_key=True, null=False)
    organization_id = UUIDField(null=False)
    page_id = UUIDField(null=False)
    site_id = UUIDField()
    provider = TextField(null=False)
    strategy = TextField(null=False)
    performance_score = DecimalField()
    lighthouse = JSONBField(null=False, default={})
    observed_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "page_performance"
    _db_schema = "seo"
    _read_only = True


class SeoSearchPerformanceDaily(Model):
    id = UUIDField(primary_key=True, null=False)
    run_id = UUIDField(null=False)
    provider = TextField(null=False)
    site_id = UUIDField(null=False)
    page_id = UUIDField()
    date = DateField(null=False)
    query = TextField()
    dimension_profile = TextField(null=False)
    impressions = IntegerField(null=False, default=0)
    created_at = DateTimeField(null=False)
    _inverse_foreign_keys: ClassVar[dict[str, dict[str, str]]] = {}
    _database = "matrx_web"
    _table_name = "search_performance_daily"
    _db_schema = "seo"
    _read_only = True


__all__ = ["SeoPagePerformance", "SeoSearchPerformanceDaily"]
