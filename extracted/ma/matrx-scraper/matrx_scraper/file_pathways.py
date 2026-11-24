"""The file placement pathways matrx-scraper's own writers name (placement registry).

Declared HERE, beside the writers, because this package runs in several hosts — aidream's
monolith, the hosted ``scraper.app.matrxserver.com`` (whose image does not contain aidream), a
crawler worker. A pathway declared only by aidream is unknown in the hosted service, so its crawl
artifacts were written with no pathway at all (2026-11-02/03: 1,139 rows under ``web-crawls-<org>``).
aidream's ``services/files/pathways.py`` imports this module so the host's declared set (and the
live ``files.file_pathway`` rows) still lists them. Needs the ``[files]`` extra — imported only by
the modules that write files. Plan: common-docs
systems/files/file-service/projects/placement-registry/PLAN.md.
"""

from __future__ import annotations

from matrx_files.placement import register_pathway

#: Immutable crawl captures (page HTML, screenshots, audits) — ``web_crawl/persistence.py``.
WEB_CRAWL_PATHWAY = "web.crawl"
#: Backlink source-page link evidence screenshots — ``api/scrape_router.py``.
SEO_BACKLINK_EVIDENCE_PATHWAY = "seo.backlink_evidence"

register_pathway(
    WEB_CRAWL_PATHWAY,
    owner_feature="web/scraper",
    audience="automated",
    root="system",
    subfolder="web/crawls/{source}",
    naming="id_only",
    description="Pages a crawl saves.",
    legacy_prefixes=("web-crawls-", "system-files/crawls"),
)
register_pathway(
    SEO_BACKLINK_EVIDENCE_PATHWAY,
    owner_feature="marketing/seo",
    audience="automated",
    root="system",
    subfolder="seo/{source}",
    naming="id_only",
    description="Screenshots proving a backlink is on its source page.",
)

__all__ = ["SEO_BACKLINK_EVIDENCE_PATHWAY", "WEB_CRAWL_PATHWAY"]
