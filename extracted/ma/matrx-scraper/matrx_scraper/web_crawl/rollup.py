"""One shared cause is ONE finding, not one per page.

A theme's footer logo with no width/height, a hosting header that expires
every file in a day, a WordPress template that skips from h4 to h6 — each is
one fix, made once, in a part every page shares. Reported per page they became
hundreds of findings (2026-10-14 census: one footer logo in 298
`image_dimension_attrs` findings; one jQuery file in 208 `caching_policy`
findings; one theme in 181 high CLS findings). Nobody can act on that, and it
buries the findings that ARE about one page.

This module reads the per-page results a run already wrote and plans, per
check, at most ONE site-subject result that names the shared causes and the
pages they touch. The page results stay (they are the immutable record); the
reconciler closes their page FINDINGS as ``rolled_up`` so the register holds
the one finding a person can act on.

Pure: rows in, plans out. No I/O.
"""

from __future__ import annotations

import statistics
from collections import Counter, defaultdict
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from urllib.parse import urlsplit

from matrx_scraper.seo_audit import CheckOutcome

#: A cause shared by at least this many failing pages is a template cause.
ROLLUP_MIN_PAGES = 5
#: A whole-page metric (speed, a missing tag) rolls up when at least this share
#: of the pages the check judged fail it together — then the page is not the cause.
ROLLUP_SITEWIDE_SHARE = 0.5
#: A page whose metric is beyond this multiple of the typical failing value is
#: an outlier with its own cause and is never covered by a site-wide roll-up.
SITEWIDE_OUTLIER_FACTOR = 1.5

_FAILING = ("warn", "fail")
_JUDGED = ("pass", "warn", "fail")


def _evidence(row: dict) -> dict:
    ev = (row.get("metadata") or {}).get("evidence")
    return ev if isinstance(ev, dict) else {}


def _list_tokens(key: str, normalize: Callable[[str], str] | None = None):
    def tokens(row: dict) -> set[str]:
        values = _evidence(row).get(key)
        if not isinstance(values, list):
            return set()
        out = {str(v) for v in values if isinstance(v, str) and v and not v.startswith("(")}
        return {normalize(v) for v in out} if normalize else out

    return tokens


def _dict_key_tokens(key: str):
    def tokens(row: dict) -> set[str]:
        values = _evidence(row).get(key)
        return {str(k) for k in values} if isinstance(values, dict) else set()

    return tokens


def _scalar_token(key: str):
    def tokens(row: dict) -> set[str]:
        value = _evidence(row).get(key)
        return {str(value)} if value not in (None, "") else set()

    return tokens


def _missing_types(row: dict) -> set[str]:
    out: set[str] = set()
    for entry in _evidence(row).get("missing_recommended") or []:
        if isinstance(entry, dict):
            for prop in entry.get("missing") or []:
                out.add(f"{entry.get('type')} is missing {prop}")
    for entry in _evidence(row).get("errors") or []:
        if isinstance(entry, str):
            out.add(entry)
    return out


def _reason_token(row: dict) -> set[str]:
    """The verdict sentence's first clause: a missing tag and a relative one are
    different causes and must never merge into one "missing" finding."""
    reason = str((row.get("metadata") or {}).get("reasoning") or "").strip()
    head = reason.split(" — ")[0].split(". ")[0]
    return {head} if head else set()


def _asset_folder(url: str) -> str:
    """Files expire by folder (one server rule), so the folder is the cause."""
    parts = urlsplit(url)
    segments = [s for s in parts.path.split("/") if s][:-1][:2]
    return f"{parts.netloc}/{'/'.join(segments)}".rstrip("/")


@dataclass(frozen=True)
class RollupRule:
    #: token extractor for "same cause" checks; None = a whole-page condition
    #: (a speed metric, a tag that is simply absent) judged by share of pages.
    tokens: Callable[[dict], set[str]] | None
    #: what one shared cause reads as, for the sentence ("the file X …").
    noun: str
    #: evidence key holding the page's metric value, for the median.
    metric: str | None = None
    unit: str = ""


#: Only checks whose cause lives in shared code or hosting. Checks whose fix is
#: per page by nature — titles, descriptions, Google CTR, word counts, broken
#: addresses — are never rolled up.
ROLLUP_RULES: dict[str, RollupRule] = {
    "image_dimension_attrs": RollupRule(_list_tokens("missing_dimensions"), "image"),
    "image_lazy_loading": RollupRule(_list_tokens("eager_below_fold"), "image"),
    "caching_policy": RollupRule(_list_tokens("short_ttl_urls", _asset_folder), "file folder"),
    "anchor_text_descriptiveness": RollupRule(
        _list_tokens("generic_anchor_targets"), "link target"
    ),
    "nofollow_internal_links": RollupRule(_list_tokens("nofollowed_targets"), "link target"),
    "heading_hierarchy": RollupRule(_list_tokens("skipped_levels"), "heading skip"),
    "social_meta_completeness": RollupRule(_list_tokens("missing_og_tags"), "missing tag"),
    "structured_data_validity": RollupRule(_missing_types, "markup problem"),
    "viewport_meta": RollupRule(_scalar_token("viewport"), "viewport setting"),
    "asset_delivery": RollupRule(_dict_key_tokens("audits"), "delivery problem"),
    "cwv_lcp": RollupRule(None, "slow main content", metric="lcp_ms", unit="ms"),
    "cwv_cls": RollupRule(None, "layout shift", metric="cls"),
    "cwv_inp_tbt": RollupRule(None, "busy page", metric="tbt_ms", unit="ms"),
    "canonical_presence": RollupRule(_reason_token, "canonical-tag problem"),
    "og_image_validity": RollupRule(_reason_token, "share-image problem"),
}


@dataclass
class RollupPlan:
    item_key: str
    item_id: str
    outcome: CheckOutcome
    #: page subject ids whose page finding this one replaces
    covered: set[str] = field(default_factory=set)
    worst_status: str = "warn"


def _fmt_metric(value: float, unit: str) -> str:
    if unit == "ms":
        return f"{value / 1000:.1f}s" if value >= 1000 else f"{round(value)}ms"
    return f"{value:.2f}"


def plan_rollups(
    rows: Iterable[dict],
    page_urls: dict[str, str],
) -> list[RollupPlan]:
    """Group a run's page rows by check and plan one site result per shared cause set."""

    by_item: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        if row.get("subject_type") == "page" and row.get("item_key") in ROLLUP_RULES:
            by_item[row["item_key"]].append(row)

    plans: list[RollupPlan] = []
    for item_key, item_rows in by_item.items():
        rule = ROLLUP_RULES[item_key]
        judged = [r for r in item_rows if r.get("status") in _JUDGED]
        failing = [r for r in item_rows if r.get("status") in _FAILING]
        if len(failing) < ROLLUP_MIN_PAGES:
            continue
        plan = (
            _plan_shared_causes(item_key, rule, failing, page_urls)
            if rule.tokens is not None
            else _plan_sitewide(item_key, rule, judged, failing, page_urls)
        )
        if plan is not None:
            plans.append(plan)
    return plans


def _samples(rows: list[dict], page_urls: dict[str, str], n: int = 5) -> list[str]:
    out = []
    for r in rows:
        url = page_urls.get(str(r.get("subject_id")))
        if url and url not in out:
            out.append(url)
        if len(out) >= n:
            break
    return out


def _base_plan(failing: list[dict], covered: list[dict]) -> tuple[str, int, str]:
    item_id = str(failing[0]["item_id"])
    scores = [r["score"] for r in covered if isinstance(r.get("score"), int)]
    worst = "fail" if any(r.get("status") == "fail" for r in covered) else "warn"
    return item_id, (min(scores) if scores else 50), worst


def _plan_shared_causes(
    item_key: str, rule: RollupRule, failing: list[dict], page_urls: dict[str, str]
) -> RollupPlan | None:
    assert rule.tokens is not None
    tokens_by_row = [(r, rule.tokens(r)) for r in failing]
    counts: Counter[str] = Counter(t for _r, toks in tokens_by_row for t in toks)
    shared = {t for t, c in counts.items() if c >= ROLLUP_MIN_PAGES}
    if not shared:
        return None
    # A page is covered only when EVERY cause it carries is a shared one; a page
    # with its own extra cause keeps its own finding.
    # Evidence lists are SAMPLES (first 5). A page with more problems than its
    # listed tokens may hide its own beyond the sample — it keeps its finding.
    covered = [
        r
        for r, toks in tokens_by_row
        if toks and toks <= shared and int(r.get("issue_count") or 0) <= len(toks)
    ]
    if len(covered) < ROLLUP_MIN_PAGES:
        return None
    pages_with = defaultdict(list)
    for r, toks in tokens_by_row:
        for t in toks & shared:
            pages_with[t].append(r)
    causes = [
        {"cause": t, "pages": len(pages_with[t]), "sample_pages": _samples(pages_with[t], page_urls)}
        for t in sorted(shared, key=lambda t: -counts[t])
    ]
    item_id, score, worst = _base_plan(failing, covered)
    top = causes[0]
    more = f" and {len(causes) - 1} more" if len(causes) > 1 else ""
    n_pages = len({str(r["subject_id"]) for r, toks in tokens_by_row if toks & shared})
    reasoning = (
        f"One shared {rule.noun} causes this on {n_pages} pages: {top['cause']}"
        f" ({top['pages']} pages){more}. It lives in something every page shares — "
        "your theme, header or footer, or hosting — so fixing it once clears every page."
    )
    outcome = CheckOutcome(
        worst,
        score,
        reasoning,
        issue_count=len(causes),
        evidence={
            "rolled_up": True,
            "shared_causes": causes[:20],
            "pages_affected": n_pages,
            "pages_failing": len(failing),
        },
    )
    return RollupPlan(item_key, item_id, outcome, {str(r["subject_id"]) for r in covered}, worst)


def _plan_sitewide(
    item_key: str,
    rule: RollupRule,
    judged: list[dict],
    failing: list[dict],
    page_urls: dict[str, str],
) -> RollupPlan | None:
    if not judged or len(failing) / len(judged) < ROLLUP_SITEWIDE_SHARE:
        return None
    values: list[float] = []
    if rule.metric:
        for r in failing:
            v = _evidence(r).get(rule.metric)
            if isinstance(v, (int, float)):
                values.append(float(v))
    typical = statistics.median(values) if values else None
    # A page far worse than the typical failing page has its own problem on
    # top of the shared one (a 12s page among 3s pages): it keeps its finding.
    covered_rows = [
        r
        for r in failing
        if typical is None
        or not isinstance(_evidence(r).get(rule.metric or ""), (int, float))
        or float(_evidence(r)[rule.metric or ""]) <= typical * SITEWIDE_OUTLIER_FACTOR
    ]
    item_id, score, worst = _base_plan(failing, covered_rows)
    median = _fmt_metric(typical, rule.unit) if typical is not None else None
    worst_rows = (
        sorted(failing, key=lambda r: -float(_evidence(r).get(rule.metric) or 0))
        if rule.metric
        else failing
    )
    measured = f" (typical value {median})" if median else ""
    reasoning = (
        f"{len(failing)} of the {len(judged)} pages we checked have the same {rule.noun}"
        f"{measured}. When most pages fail together the cause is the shared theme, "
        "plugins or hosting, not the pages — fix it once there."
    )
    outcome = CheckOutcome(
        worst,
        score,
        reasoning,
        issue_count=len(failing),
        evidence={
            "rolled_up": True,
            "pages_affected": len(failing),
            "pages_checked": len(judged),
            "typical_value": median,
            "sample_pages": _samples(worst_rows, page_urls),
        },
    )
    return RollupPlan(item_key, item_id, outcome, {str(r["subject_id"]) for r in covered_rows}, worst)


__all__ = ["ROLLUP_RULES", "RollupPlan", "plan_rollups", "ROLLUP_MIN_PAGES"]
