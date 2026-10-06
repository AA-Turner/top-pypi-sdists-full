"""Findings that were FALSE or duplicated, proven from real stored data (2026-10-05).

Expected values were written down from the live `web.finding` / `web.link_edge` /
`web.snapshot` rows BEFORE the fixes; each class has a planted break at the bottom
that must fail for the stated reason (see PLANTED_BREAKS in the report).

Real rows quoted here:
- `web.link_edge`, allgreenrecycling.com: five share buttons (rel "nofollow noopener",
  anchor Facebook/Twitter/Pinterest/LinkedIn/Email) on 578 pages -> 372 of the 437
  open nofollow findings; "Cancel reply" comment-form links; and one real content
  link (datadestruction.com -> /compliance/nist-800-88) that IS an actual defect.
- `web.snapshot.structured_data` for iopbm.com `/`: the LEGACY shape
  `{"schema_org": {}, "schema_types": ["http://schema.org/Organization"]}`; the
  live page declares `MedicalClinic`.
- datadestruction.com/author/arman-sadeghi: 12 <img>, 11 with `alt=""`; the stored
  finding said "9 of 10 images have no alt text" at severity HIGH.
- pbw-law.com / cosmeticinjectables.com: images placed by a lazy-loading script
  (`data:` placeholder + `data-src`, `nitro-lazy-src`); stored as "(no src)" and
  reported as "35 of 35 images load eagerly".
"""

from __future__ import annotations

import asyncio
import json
from contextlib import asynccontextmanager
from datetime import UTC, datetime
from types import SimpleNamespace

from matrx_scraper.seo_audit import (
    PageEvidence,
    audit_html,
    check_image_alt_presence,
    check_image_lazy_loading,
    evidence_from_audit,
    legacy_business_types_in,
)
from matrx_scraper.web_crawl import analysis_write
from matrx_scraper.web_crawl.analysis import (
    PAGE_CHECKS,
    PER_PAGE_RUN_CHECKS,
    SITE_SCOPED_CROSS_PAGE_CHECKS,
    PageFacts,
    SiteAggregates,
    index_page_facts,
    is_utility_link,
    local_business_outcome,
)

# --------------------------------------------------------------------- nofollow

REAL_NOFOLLOW_EDGES = [
    # (target_url, anchor_text, expected_utility)
    ("https://allgreenrecycling.com/", "Twitter", True),
    ("https://allgreenrecycling.com/", "Pinterest", True),
    ("https://allgreenrecycling.com/", "LinkedIn", True),
    ("https://allgreenrecycling.com/", "Email", True),
    ("https://allgreenrecycling.com/", "Facebook", True),
    ("https://allgreenrecycling.com/are-ziploc-bags-recyclable", "Cancel reply", True),
    ("https://search-quake.com/events/list?tribe-bar-date=2026-08-31&ical=1", "Add to calendar", True),
    ("https://search-quake.com/events/list?tribe-bar-date=2026-08-31&outlook-ical=1", "Outlook", True),
    (
        "https://datadestruction.com/compliance/nist-800-88",
        "blank” rel=”noopener”>NIST SP 800-88 r2 guidelines",
        False,  # a real content link wrongly nofollowed: stays a finding
    ),
]


def test_utility_links_are_not_nofollow_mistakes():
    got = [is_utility_link(url, anchor) for url, anchor, _ in REAL_NOFOLLOW_EDGES]
    assert got == [expected for *_, expected in REAL_NOFOLLOW_EDGES]


# -------------------------------------------------------------------- alt text

# Real tags from datadestruction.com/author/arman-sadeghi (src trimmed).
REAL_AUTHOR_PAGE = """<html lang="en"><head><title>Arman Sadeghi author page</title></head><body>
<img class="mega-menu-logo" src="/logo.png" alt="Data Destruction logo">
<img fetchpriority="high" width="1237" height="639" src="/a.jpg" alt="">
<img width="637" height="358" src="/armani.jpeg" alt="">
<img width="800" height="800" src="/b.png" alt="">
<img src="/image-24.png" alt=""><img src="/image-22.png" alt="">
</body></html>"""


def test_empty_alt_is_a_decorative_marker_not_a_missing_alt():
    evidence = evidence_from_audit(audit_html(REAL_AUTHOR_PAGE, "https://datadestruction.com/x"), http_status=200)
    assert evidence.image_count == 6
    # the capture-side counter stays byte-identical with matrx-extend's auditor
    # (parity fixture); the CHECK recomputes from the per-image inventory.
    outcome = check_image_alt_presence(evidence)
    assert outcome.status == "pass"


def test_a_missing_alt_attribute_is_still_missing():
    html = '<html lang="en"><body><img src="/a.jpg"><img src="/b.jpg" alt=""><img src="/c.jpg" alt="c"></body></html>'
    evidence = evidence_from_audit(audit_html(html, "https://example.com/"), http_status=200)
    assert check_image_alt_presence(evidence).issue_count == 1


def test_a_snapshot_stored_with_the_old_count_is_corrected_from_its_inventory():
    """Old rows carry images_missing_alt=9 beside an inventory showing alt == ''."""
    items = [{"src": f"/i{n}.png", "alt": ""} for n in range(9)] + [{"src": "/ok.png", "alt": "ok"}]
    stale = PageEvidence(url="https://datadestruction.com/x", image_count=10, images_missing_alt=9, image_items=items)
    assert check_image_alt_presence(stale).status == "pass"


# ------------------------------------------------------------------ lazy loading


def _lazy_items(n: int, **overrides) -> list[dict]:
    return [{"src": None, "loading": None, "width": 1, "height": 1, **overrides} for _ in range(n)]


def test_script_placed_images_are_not_called_eager():
    """cosmeticinjectables.com lip-filler page: 18 images, none with a source."""
    ev = PageEvidence(url="https://cosmeticinjectables.com/x", image_count=18, image_items=_lazy_items(18))
    outcome = check_image_lazy_loading(ev)
    assert outcome.status == "n_a" and outcome.score is None


def test_real_eager_below_the_fold_images_are_still_reported():
    items = [{"src": f"https://a.com/{n}.jpg", "loading": None} for n in range(12)]
    outcome = check_image_lazy_loading(PageEvidence(url="https://a.com/", image_count=12, image_items=items))
    assert outcome.status == "warn" and outcome.issue_count > 0


def test_images_flagged_js_lazy_count_as_lazy():
    items = [{"src": f"https://a.com/{n}.jpg", "loading": None, "js_lazy": n >= 3} for n in range(12)]
    outcome = check_image_lazy_loading(PageEvidence(url="https://a.com/", image_count=12, image_items=items))
    assert outcome.status == "pass"


def test_capture_flags_data_src_and_lazyload_class_images():
    html = (
        '<html lang="en"><body>'
        '<img src="/hero.jpg" width="9" height="9" alt="h">'
        + "".join(
            f'<img width="500" height="103" data-class="LazyLoad" src="data:image/svg+xml,%3Csvg/%3E" '
            f'data-src="https://pbw-law.com/{n}.png" alt="x">'
            for n in range(6)
        )
        + "</body></html>"
    )
    ev = evidence_from_audit(audit_html(html, "https://www.pbw-law.com/"), http_status=200)
    flags = [i.get("js_lazy") for i in ev.image_items]
    assert flags[0] is False and all(flags[1:])


# ------------------------------------------------------------ local_business_markup

LEGACY_IOPBM = {"schema_org": {}, "schema_types": ["http://schema.org/Organization"]}

MEDICAL_CLINIC = json.dumps(
    {
        "@context": "https://schema.org",
        "@type": "MedicalClinic",
        "name": "Institute of Plant-Based Medicine",
        "address": {"@type": "PostalAddress", "streetAddress": "1 Way", "addressLocality": "Newport Beach"},
        "telephone": "+1-949-555-0100",
    }
)


def _facts(url: str, structured_data: dict | None, **kw) -> PageFacts:
    return PageFacts(page_id=url, url=url, structured_data=structured_data, **kw)


def test_legacy_capture_naming_organization_is_unknown_not_absent():
    assert legacy_business_types_in(LEGACY_IOPBM) == ["Organization"]
    pages = [_facts("https://iopbm.com/", LEGACY_IOPBM), _facts("https://iopbm.com/a", {"schema_org": {}, "schema_types": []})]
    site = SiteAggregates()
    index_page_facts(pages, site)
    outcome = local_business_outcome(site)
    assert outcome.status == "n_a", outcome  # stored finding said: "No page on this site says who the business is"
    assert outcome.remediation is not None


def test_medical_clinic_counts_as_a_business_entity():
    page = page_with_ld(MEDICAL_CLINIC, "https://iopbm.com/")
    site = SiteAggregates()
    index_page_facts([page], site)
    assert [e["types"] for e in site.business.entities] == [["MedicalClinic"]]
    assert local_business_outcome(site).status == "pass"


def page_with_ld(doc: str, url: str) -> PageFacts:
    audit = audit_html(
        f"<html lang='en'><head><script type='application/ld+json'>{doc}</script></head><body><p>x</p></body></html>",
        url,
    )
    ev = evidence_from_audit(audit, http_status=200)
    return PageFacts(
        page_id=url,
        **{f: getattr(ev, f) for f in ev.__dataclass_fields__ if f != "url"},
        url=url,
    )


def test_genuinely_absent_business_markup_still_warns():
    plain = {"schema_org": {}, "schema_types": ["http://schema.org/WebPage"]}
    pages = [_facts(f"https://example.com/{n}", plain) for n in range(3)]
    site = SiteAggregates()
    index_page_facts(pages, site)
    assert local_business_outcome(site).status == "warn"


# --------------------------------------------------- one finding per site, not per page


def test_a_site_level_check_is_not_run_per_page():
    """809 identical findings on 9 sites came from running this once PER PAGE."""
    assert SITE_SCOPED_CROSS_PAGE_CHECKS == {"local_business_markup"}
    assert "local_business_markup" in PAGE_CHECKS  # still catalogued + callable
    assert "local_business_markup" not in PER_PAGE_RUN_CHECKS


def test_two_pages_produce_one_local_business_verdict():
    pages = [_facts(f"https://iopbm.com/{n}", LEGACY_IOPBM) for n in range(2)]
    site = SiteAggregates()
    index_page_facts(pages, site)
    per_page_rows = [
        key for _page in pages for key in PER_PAGE_RUN_CHECKS if key in SITE_SCOPED_CROSS_PAGE_CHECKS
    ]
    assert per_page_rows == []  # zero per-page rows; the single site row comes from local_business_outcome(site)
    assert local_business_outcome(site).status == "n_a"


# ----------------------------------------------- stale page findings are retired


class _FakeFinding(SimpleNamespace):
    pass


class _Q:
    def __init__(self, rows):
        self.rows = rows

    async def all(self):
        return self.rows


def _run_reconcile(monkeypatch, findings, results, site_scoped):
    retired_updates = []

    @asynccontextmanager
    async def fake_tx(_name):
        yield

    async def fake_bulk_update(_model, rows, casts=None):
        retired_updates.append(rows)

    async def fake_bulk_create(rows):
        return rows

    fake_model = SimpleNamespace(
        filter=lambda **kw: _Q(findings), bulk_create=fake_bulk_create
    )
    monkeypatch.setattr(analysis_write, "WebFinding", fake_model)
    monkeypatch.setattr(analysis_write, "transaction", fake_tx)
    monkeypatch.setattr(analysis_write, "bulk_update_by_pk", fake_bulk_update)
    summary = SimpleNamespace(findings_opened=0, findings_refreshed=0, findings_reopened=0, findings_resolved=0)
    asyncio.run(
        analysis_write.reconcile_findings(
            site_id="s",
            organization_id="o",
            computed_at=datetime.now(UTC),
            results=results,
            summary=summary,
            site_scoped_item_ids=site_scoped,
        )
    )
    return summary, retired_updates


def _page_finding(i, item="item-lbm"):
    return _FakeFinding(id=f"f{i}", subject_id=f"p{i}", item_id=item, subject_type="page", status="open", resolved_at=None)


def _site_row(status, item="item-lbm"):
    row = {"subject_type": "site", "subject_id": "s", "page_id": None, "item_id": item, "item_key": "k",
           "category": "c", "subcategory": None, "severity": "low", "status": status}
    return row, SimpleNamespace(id="r1")


def test_old_page_rows_are_resolved_when_the_site_row_arrives(monkeypatch):
    findings = [_page_finding(i) for i in range(809 // 100)]  # 8 stale per-page findings
    summary, updates = _run_reconcile(monkeypatch, findings, [_site_row("warn")], {"item-lbm"})
    assert len(updates) == 1  # the retirement; the site row is a create, not an update
    retired = [u for batch in updates for u in batch if u.get("status") == "resolved"]
    assert sorted(u["id"] for u in retired) == sorted(f.id for f in findings)
    assert summary.findings_opened == 1  # exactly ONE site finding replaces them
    assert summary.findings_resolved == len(findings)


def test_a_crashed_site_check_retires_nothing(monkeypatch):
    findings = [_page_finding(i) for i in range(3)]
    summary, updates = _run_reconcile(monkeypatch, findings, [_site_row("error")], {"item-lbm"})
    assert updates == [] and summary.findings_resolved == 0


def test_other_items_page_findings_are_untouched(monkeypatch):
    findings = [_page_finding(i, item="item-title") for i in range(3)]
    _summary, updates = _run_reconcile(monkeypatch, findings, [_site_row("warn")], {"item-lbm"})
    assert updates == []
