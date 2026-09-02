"""Typed evidence payloads for every SEO analysis check.

**Why this file exists.** Each check in ``seo_audit`` / ``web_crawl.analysis`` /
``web_crawl.site_analysis`` returns a ``CheckOutcome`` whose ``evidence`` field
was ``dict[str, Any]`` — an untyped hole. The data behind it is *computed by
this package*, deterministically, so its shape was always knowable; leaving it
untyped meant the platform received real data and could only render it as text.
One model per check closes that hole at the source: the payload becomes a
declared shape, which the host registers as a content-IR kind and from which
TypeScript types are generated. Nothing downstream has to guess again.

**Every field is optional.** A check reaches its verdict through branches, and
each branch supplies the evidence that branch actually has (``robots_txt_health``
alone has six). A model is therefore the UNION of its check's branches, never a
single required record. The field set was derived from two sources and is the
union of both: the 101 ``evidence={...}`` literals in the producing code, and
the key/type census of 27,280 live ``web.analysis_result`` rows.

**``extra="allow"`` is deliberate.** A branch this file has not caught keeps its
data and passes through rather than raising — evidence we paid to compute is
never dropped to satisfy a schema. The host's stamping seam logs unknown keys so
the gap gets closed instead of hiding.

Checks that emit no evidence at all (``title_length``, ``h1_presence``,
``thin_content``, …) are intentionally absent: their verdict IS the whole
finding, and an empty model would be a lie about there being a payload.
"""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class CheckEvidence(BaseModel):
    """Base for every per-check evidence payload."""

    model_config = ConfigDict(extra="allow")


# ── Content structure ────────────────────────────────────────────────────────


class HeadingHierarchyEvidence(CheckEvidence):
    heading_count: int | None = None
    empty_headings: int | None = None
    heading_levels: list[int] | None = None
    skipped_levels: list[str] | None = None


class ContentDepthEvidence(CheckEvidence):
    word_count: int | None = None
    page_type: str | None = None


class TextHtmlRatioEvidence(CheckEvidence):
    ratio: float | None = None
    text_bytes: int | None = None
    html_bytes: int | None = None


class SoftFourOhFourEvidence(CheckEvidence):
    http_status: int | None = None
    title: str | None = None
    word_count: int | None = None


# ── Performance (lab) ────────────────────────────────────────────────────────


class LcpEvidence(CheckEvidence):
    lcp_ms: float | None = None
    strategy: str | None = None


class ClsEvidence(CheckEvidence):
    cls: float | None = None
    strategy: str | None = None


class InpTbtEvidence(CheckEvidence):
    tbt_ms: float | None = None
    strategy: str | None = None


class TtfbEvidence(CheckEvidence):
    ttfb_ms: float | None = None
    response_time_ms: float | None = None


class AssetDeliveryEvidence(CheckEvidence):
    #: Lighthouse audit id -> estimated savings in milliseconds.
    audits: dict[str, float] | None = None
    total_savings_ms: float | None = None
    strategy: str | None = None


class CachingPolicyEvidence(CheckEvidence):
    static_bytes: int | None = None
    well_cached_bytes: int | None = None
    short_ttl_urls: list[str] | None = None
    strategy: str | None = None


class PageWeightEvidence(CheckEvidence):
    bytes: int | None = None


# ── Images & media ───────────────────────────────────────────────────────────


class BrokenImagesEvidence(CheckEvidence):
    broken_images: list[Any] | None = None


class ImageDimensionAttrsEvidence(CheckEvidence):
    missing_dimensions: list[Any] | None = None


class ImageLazyLoadingEvidence(CheckEvidence):
    eager_below_fold: list[Any] | None = None
    lazy_above_fold: list[Any] | None = None


class ImageModernFormatEvidence(CheckEvidence):
    legacy_format_images: list[Any] | None = None


class ImageOversizedEvidence(CheckEvidence):
    oversized_images: list[Any] | None = None
    estimated_waste_bytes: int | None = None
    largest_image_bytes: int | None = None


# ── Internal linking ─────────────────────────────────────────────────────────


class BrokenTargetsEvidence(CheckEvidence):
    """Shared by ``broken_internal_links`` and ``broken_external_links``."""

    broken_targets: list[Any] | None = None


class InternalRedirectLinksEvidence(CheckEvidence):
    redirecting_targets: list[Any] | None = None


class NofollowInternalLinksEvidence(CheckEvidence):
    nofollowed_targets: list[Any] | None = None


class AnchorTextDescriptivenessEvidence(CheckEvidence):
    generic_anchor_targets: list[Any] | None = None


class ExcessiveOutlinksEvidence(CheckEvidence):
    outlinks_total: int | None = None
    internal_outlinks: int | None = None


class CrawlDepthEvidence(CheckEvidence):
    depth: int | None = None


class InternalInlinkCoverageEvidence(CheckEvidence):
    unique_inlinks: int | None = None


class InternalLinkEquityEvidence(CheckEvidence):
    link_score: float | None = None
    pagerank_percentile: float | None = None
    pages_scored: int | None = None
    prioritized: bool | None = None
    priority_penalty_applied: bool | None = None


class OrphanPagesEvidence(CheckEvidence):
    captured: bool | None = None
    crawled_orphans: int | None = None
    known_live_pages: int | None = None
    known_uncrawled_orphans: int | None = None
    known_uncrawled_orphan_samples: list[str] | None = None


# ── Canonicalisation & duplication ───────────────────────────────────────────


class DuplicatePagesEvidence(CheckEvidence):
    """Shared by ``title_duplication``, ``meta_description_duplication`` and
    ``duplicate_content_exact`` — all three report the same clustered shape."""

    duplicate_pages: list[Any] | None = None


class NearDuplicateContentEvidence(CheckEvidence):
    clusters: list[Any] | None = None
    clusters_total: int | None = None
    clusters_returned: int | None = None
    clusters_omitted: int | None = None
    near_duplicate_pages: int | None = None
    indexable_pages: int | None = None
    fingerprinted_pages: int | None = None
    pages_without_fingerprint: int | None = None
    pages_without_indexability: int | None = None
    canonical_pairs_excluded: int | None = None
    threshold_percent: float | None = None


class CanonicalConflictsEvidence(CheckEvidence):
    canonical_url: str | None = None


# ── HTTP status & redirects ──────────────────────────────────────────────────


class HttpStatusEvidence(CheckEvidence):
    """Shared by ``broken_page_4xx`` and ``server_error_5xx``."""

    http_status: int | None = None


class RedirectChainEvidence(CheckEvidence):
    redirect_chain: list[Any] | None = None
    http_status: int | None = None


class RedirectLoopEvidence(CheckEvidence):
    redirect_chain: list[Any] | None = None


class TemporaryRedirectUsageEvidence(CheckEvidence):
    redirect_chain: list[Any] | None = None
    temporary_statuses: list[Any] | None = None


class MetaRefreshRedirectEvidence(CheckEvidence):
    meta_refresh: str | None = None
    target: str | None = None


# ── Crawlability & indexability ──────────────────────────────────────────────


class MetaRobotsConflictsEvidence(CheckEvidence):
    meta_robots: str | None = None


class RobotsTxtHealthEvidence(CheckEvidence):
    robots_url: str | None = None
    http_status: int | None = None
    blocked_agents: list[Any] | None = None
    blocked_urls: list[str] | None = None
    syntax_errors: list[Any] | None = None
    sitemaps_declared: list[str] | None = None


class SitemapHealthEvidence(CheckEvidence):
    checked: int | None = None
    sitemaps: list[Any] | None = None
    unreachable: list[Any] | None = None
    oversized: list[Any] | None = None
    noindexed: list[Any] | None = None
    redirecting: list[Any] | None = None
    not_found_or_error: list[Any] | None = None


class SitemapCoverageEvidence(CheckEvidence):
    missing_from_sitemap: list[Any] | None = None
    never_reached: list[Any] | None = None


class PaginationMarkupEvidence(CheckEvidence):
    pagination: dict[str, Any] | None = None


# ── Security ─────────────────────────────────────────────────────────────────


class HttpsEnforcementEvidence(CheckEvidence):
    http_variant: dict[str, Any] | None = None
    scheme: str | None = None
    url: str | None = None


class MixedContentEvidence(CheckEvidence):
    mixed_content: list[Any] | None = None


class SecurityHeadersEvidence(CheckEvidence):
    header_coverage: dict[str, Any] | None = None
    missing_headers: list[str] | None = None
    pages_sampled: int | None = None


class HstsPolicyEvidence(CheckEvidence):
    include_subdomains: bool | None = None
    min_max_age_seconds: int | None = None
    pages_sampled: int | None = None
    pages_without_hsts: list[str] | None = None
    pages_unparsable: list[str] | None = None
    weakest_page: str | None = None


class TlsCertificateEvidence(CheckEvidence):
    issuer: str | None = None
    not_after: str | None = None
    days_to_expiry: int | None = None


# ── URL architecture ─────────────────────────────────────────────────────────


class UrlDesignQualityEvidence(CheckEvidence):
    url_length: int | None = None
    parameter_count: int | None = None
    has_uppercase: bool | None = None
    has_underscores: bool | None = None
    has_non_ascii: bool | None = None
    session_params: list[str] | None = None


class HostProtocolConsistencyEvidence(CheckEvidence):
    canonical: str | None = None
    variants: list[Any] | None = None
    live_variants: list[Any] | None = None
    host_forms: list[Any] | None = None
    paths_checked: int | None = None
    slash_pairs_checked: int | None = None
    slash_duplicate_paths: list[Any] | None = None


# ── International ────────────────────────────────────────────────────────────


class HreflangValidityEvidence(CheckEvidence):
    declared: list[Any] | None = None
    invalid_codes: list[str] | None = None
    relative_urls: list[str] | None = None
    canonical_url: str | None = None
    self_href: str | None = None


class HreflangReciprocityEvidence(CheckEvidence):
    missing_return_tags: list[Any] | None = None
    unverified_targets: list[Any] | None = None


class HtmlLangValidityEvidence(CheckEvidence):
    lang: str | None = None


# ── Mobile & social ──────────────────────────────────────────────────────────


class ViewportMetaEvidence(CheckEvidence):
    viewport: str | None = None


class SocialMetaCompletenessEvidence(CheckEvidence):
    og_url: str | None = None
    canonical_url: str | None = None
    twitter_card: str | None = None
    missing_og_tags: list[str] | None = None


class OgImageValidityEvidence(CheckEvidence):
    og_image: str | None = None


# ── Structured data ──────────────────────────────────────────────────────────


class StructuredDataValidityEvidence(CheckEvidence):
    missing_required: list[Any] | None = None
    missing_recommended: list[Any] | None = None
    parse_errors: list[Any] | None = None


class LocalBusinessMarkupEvidence(CheckEvidence):
    types: list[str] | None = None
    missing: list[str] | None = None
    conflicting_values: dict[str, Any] | None = None


# ── Search Console signals ───────────────────────────────────────────────────


class GscCtrOpportunityEvidence(CheckEvidence):
    #: Set instead of the metrics when the site has no usable GSC binding.
    gsc_binding: str | None = None
    clicks: int | None = None
    impressions: int | None = None
    ctr: float | None = None
    expected_ctr: float | None = None
    missed_clicks: float | None = None
    average_position: float | None = None
    window: dict[str, Any] | None = None


class GscPerformanceDecayEvidence(CheckEvidence):
    gsc_binding: str | None = None
    current: dict[str, Any] | None = None
    prior: dict[str, Any] | None = None
    quarter: dict[str, Any] | None = None
    drop_vs_prior: float | None = None
    drop_vs_quarter: float | None = None


# ── The registry ─────────────────────────────────────────────────────────────

#: ``web.analysis_item.key`` -> the model describing that check's evidence.
#: A key absent here emits no evidence payload; that is not an error.
CHECK_EVIDENCE_MODELS: dict[str, type[CheckEvidence]] = {
    "anchor_text_descriptiveness": AnchorTextDescriptivenessEvidence,
    "asset_delivery": AssetDeliveryEvidence,
    "broken_external_links": BrokenTargetsEvidence,
    "broken_images": BrokenImagesEvidence,
    "broken_internal_links": BrokenTargetsEvidence,
    "broken_page_4xx": HttpStatusEvidence,
    "caching_policy": CachingPolicyEvidence,
    "canonical_conflicts": CanonicalConflictsEvidence,
    "content_depth": ContentDepthEvidence,
    "crawl_depth": CrawlDepthEvidence,
    "cwv_cls": ClsEvidence,
    "cwv_inp_tbt": InpTbtEvidence,
    "cwv_lcp": LcpEvidence,
    "duplicate_content_exact": DuplicatePagesEvidence,
    "excessive_outlinks": ExcessiveOutlinksEvidence,
    "gsc_ctr_opportunity": GscCtrOpportunityEvidence,
    "gsc_performance_decay": GscPerformanceDecayEvidence,
    "heading_hierarchy": HeadingHierarchyEvidence,
    "host_protocol_consistency": HostProtocolConsistencyEvidence,
    "hreflang_reciprocity": HreflangReciprocityEvidence,
    "hreflang_validity": HreflangValidityEvidence,
    "hsts_policy": HstsPolicyEvidence,
    "html_lang_validity": HtmlLangValidityEvidence,
    "https_enforcement": HttpsEnforcementEvidence,
    "image_dimension_attrs": ImageDimensionAttrsEvidence,
    "image_lazy_loading": ImageLazyLoadingEvidence,
    "image_modern_format": ImageModernFormatEvidence,
    "image_oversized": ImageOversizedEvidence,
    "internal_inlink_coverage": InternalInlinkCoverageEvidence,
    "internal_link_equity": InternalLinkEquityEvidence,
    "internal_redirect_links": InternalRedirectLinksEvidence,
    "local_business_markup": LocalBusinessMarkupEvidence,
    "meta_description_duplication": DuplicatePagesEvidence,
    "meta_refresh_redirect": MetaRefreshRedirectEvidence,
    "meta_robots_conflicts": MetaRobotsConflictsEvidence,
    "mixed_content": MixedContentEvidence,
    "near_duplicate_content": NearDuplicateContentEvidence,
    "nofollow_internal_links": NofollowInternalLinksEvidence,
    "og_image_validity": OgImageValidityEvidence,
    "orphan_pages": OrphanPagesEvidence,
    "page_weight": PageWeightEvidence,
    "pagination_markup": PaginationMarkupEvidence,
    "redirect_chain": RedirectChainEvidence,
    "redirect_loop": RedirectLoopEvidence,
    "robots_txt_health": RobotsTxtHealthEvidence,
    "security_headers": SecurityHeadersEvidence,
    "server_error_5xx": HttpStatusEvidence,
    "sitemap_coverage": SitemapCoverageEvidence,
    "sitemap_health": SitemapHealthEvidence,
    "social_meta_completeness": SocialMetaCompletenessEvidence,
    "soft_404_detection": SoftFourOhFourEvidence,
    "structured_data_validity": StructuredDataValidityEvidence,
    "temporary_redirect_usage": TemporaryRedirectUsageEvidence,
    "text_html_ratio": TextHtmlRatioEvidence,
    "title_duplication": DuplicatePagesEvidence,
    "tls_certificate": TlsCertificateEvidence,
    "ttfb_server_response": TtfbEvidence,
    "url_design_quality": UrlDesignQualityEvidence,
    "viewport_meta": ViewportMetaEvidence,
}


def _snake(name: str) -> str:
    """``LcpEvidence`` -> ``lcp_evidence``."""
    out: list[str] = []
    for i, ch in enumerate(name):
        if ch.isupper() and i:
            out.append("_")
        out.append(ch.lower())
    return "".join(out)


#: ``web.analysis_item.key`` -> the content-IR kind slug its evidence carries.
#: Two checks that share a model share a kind: the shape IS the same shape, and
#: minting a second slug for it would be a near-duplicate (the merge law).
EVIDENCE_KIND_SLUGS: dict[str, str] = {
    key: "web_evidence_" + _snake(model.__name__).removesuffix("_evidence") + "_v1"
    for key, model in CHECK_EVIDENCE_MODELS.items()
}


def evidence_model_for(item_key: str) -> type[CheckEvidence] | None:
    """The evidence model for a check key, or ``None`` when it emits none."""
    return CHECK_EVIDENCE_MODELS.get(item_key)


def evidence_kind_for(item_key: str) -> str | None:
    """The content-IR kind slug for a check key's evidence payload."""
    return EVIDENCE_KIND_SLUGS.get(item_key)


__all__ = [
    "CHECK_EVIDENCE_MODELS",
    "EVIDENCE_KIND_SLUGS",
    "CheckEvidence",
    "evidence_kind_for",
    "evidence_model_for",
]
