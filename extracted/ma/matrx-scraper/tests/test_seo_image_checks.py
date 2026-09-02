"""The five `images_media` catalogue checks — one file, one defect each.

Each check must (a) fire for its OWN defect, (b) stay quiet on a page that gets
images right, and (c) answer `n_a` rather than `pass` when the evidence it needs
was never captured. That last one is the whole point: a green verdict on images
nobody measured is a lie. The live crawl now fills those fields in one bounded
capture pass; these pure check tests also pin the old-snapshot/failure behavior.

Written against `seo_audit` directly — these are pure evidence-in / verdict-out
functions, so no HTML parsing and no database are involved except in the one
end-to-end test at the bottom.
"""

from __future__ import annotations

import pytest

from matrx_scraper.seo_audit import (
    IMAGE_ABOVE_FOLD_DOM_COUNT,
    IMAGE_OVERSIZE_MINOR_RATIO,
    IMAGE_OVERSIZE_SEVERE_RATIO,
    IMAGE_OVERSIZE_FAIL_BYTES,
    IMAGE_OVERSIZE_WARN_BYTES,
    CheckOutcome,
    PageEvidence,
    audit_html,
    check_broken_images,
    check_image_dimension_attrs,
    check_image_lazy_loading,
    check_image_modern_format,
    check_image_oversized,
    evidence_from_audit,
)

IMAGE_CHECKS = (
    check_image_dimension_attrs,
    check_image_lazy_loading,
    check_image_modern_format,
    check_image_oversized,
    check_broken_images,
)


def assert_db_valid(outcome: CheckOutcome) -> None:
    """`web.analysis_result`'s status/score constraint, mirrored."""
    assert outcome.status in ("pass", "warn", "fail", "n_a")
    if outcome.status in ("pass", "warn", "fail"):
        assert outcome.score is not None and 1 <= outcome.score <= 100
    else:
        assert outcome.score is None
    assert outcome.reasoning


def img(**overrides) -> dict:
    """One inventory item that nothing is wrong with."""
    item = {
        "src": "https://example.com/photo.webp",
        "srcset": [],
        "srcset_widths": [],
        "picture_formats": [],
        "sizes": None,
        "alt": "described",
        "width": 800,
        "height": 600,
        "loading": None,
        "decoding": None,
        "fetchpriority": None,
        "title": None,
        "capture_status": "complete",
        "http_status": 200,
        "bytes": 100,
        "natural_width": 800,
        "natural_height": 600,
        "actual_format": "webp",
    }
    item.update(overrides)
    return item


def page(items: list[dict]) -> PageEvidence:
    return PageEvidence(
        url="https://example.com/a",
        image_count=len(items),
        images_missing_alt=0,
        image_items=items,
    )


# Three images that get everything right: modern format, explicit dimensions,
# eager above the fold, lazy below it, sized for their slot.
HEALTHY_ITEMS = [
    img(),
    img(src="https://example.com/two.avif"),
    img(src="https://example.com/three.webp"),
    img(src="https://example.com/four.webp", loading="lazy"),
    img(src="https://example.com/five.webp", loading="lazy"),
]


# ---------------------------------------------------------------------------
# The healthy page, and the missing-evidence contract


@pytest.mark.parametrize("check", IMAGE_CHECKS)
def test_a_page_that_gets_images_right_trips_nothing(check):
    outcome = check(page(HEALTHY_ITEMS))
    assert_db_valid(outcome)
    assert outcome.status in ("pass", "n_a"), f"{check.__name__} flagged a healthy page: {outcome}"


@pytest.mark.parametrize("check", IMAGE_CHECKS)
def test_an_uncaptured_inventory_is_n_a_never_a_pass(check):
    """A snapshot that predates the per-image inventory knows nothing."""
    outcome = check(PageEvidence(url="https://example.com/a", image_count=12, image_items=[]))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


@pytest.mark.parametrize("check", IMAGE_CHECKS)
def test_a_page_with_no_images_is_n_a(check):
    outcome = check(page([]))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


# ---------------------------------------------------------------------------
# image_dimension_attrs


def test_dimension_attrs_fires_when_images_declare_no_size():
    items = [img(width=None, height=None) for _ in range(4)]
    outcome = check_image_dimension_attrs(page(items))
    assert_db_valid(outcome)
    assert outcome.status == "fail"
    assert outcome.issue_count == 4
    assert outcome.evidence and outcome.evidence["missing_dimensions"]


def test_dimension_attrs_warns_in_the_middle_band_and_scores_the_coverage():
    items = [img() for _ in range(3)] + [img(width=None, height=None)]
    outcome = check_image_dimension_attrs(page(items))
    assert outcome.status == "warn"
    assert outcome.score == 75  # 3 of 4


def test_dimension_attrs_needs_both_attributes():
    outcome = check_image_dimension_attrs(page([img(height=None)]))
    assert outcome.status == "fail"


# ---------------------------------------------------------------------------
# image_lazy_loading — both directions


def test_lazy_loading_fails_when_the_hero_is_lazy_loaded():
    items = [img(loading="lazy"), *HEALTHY_ITEMS[1:]]
    outcome = check_image_lazy_loading(page(items))
    assert_db_valid(outcome)
    assert outcome.status == "fail"
    assert outcome.score == 30
    assert "hero" in outcome.reasoning or "LCP" in outcome.reasoning


def test_lazy_loading_fails_when_the_featured_image_is_lazy_even_far_down_the_page():
    """The featured/OG image is the usual LCP element wherever it sits."""
    items = [img() for _ in range(IMAGE_ABOVE_FOLD_DOM_COUNT)]
    items += [img(loading="lazy") for _ in range(4)]
    items.append(img(src="https://example.com/hero.webp", loading="lazy", featured=True))
    outcome = check_image_lazy_loading(page(items))
    assert outcome.status == "fail"
    assert outcome.evidence["lazy_above_fold"] == ["https://example.com/hero.webp"]


def test_lazy_loading_warns_harder_when_most_below_fold_images_are_eager():
    items = [img() for _ in range(IMAGE_ABOVE_FOLD_DOM_COUNT)]
    items += [img(loading="lazy"), img(), img(), img()]  # 3 of 4 below-fold eager
    outcome = check_image_lazy_loading(page(items))
    assert outcome.status == "warn"
    assert outcome.score == 60
    assert outcome.issue_count == 3


def test_lazy_loading_warns_softly_on_a_minority_of_eager_below_fold_images():
    items = [img() for _ in range(IMAGE_ABOVE_FOLD_DOM_COUNT)]
    items += [img(loading="lazy"), img(loading="lazy"), img(loading="lazy"), img()]
    outcome = check_image_lazy_loading(page(items))
    assert outcome.status == "warn"
    assert outcome.score == 80


def test_lazy_loading_accepts_an_explicitly_eager_hero():
    items = [img(loading="eager"), *HEALTHY_ITEMS[1:]]
    assert check_image_lazy_loading(page(items)).status == "pass"


# ---------------------------------------------------------------------------
# image_modern_format


def test_modern_format_fires_on_a_page_of_jpegs():
    items = [img(src=f"https://example.com/{i}.jpg", actual_format="jpg") for i in range(5)]
    outcome = check_image_modern_format(page(items))
    assert_db_valid(outcome)
    assert outcome.status == "fail"
    assert outcome.score == 1  # 0% modern, floored by clamp_score
    assert outcome.issue_count == 5


def test_modern_format_counts_a_picture_source_as_what_the_browser_gets():
    """`<picture><source type=image/avif><img src=hero.jpg>` is the RIGHT shape."""
    items = [
        img(
            src=f"https://example.com/{i}.jpg",
            picture_formats=["avif", "jpg"],
            actual_format="avif",
        )
        for i in range(5)
    ]
    assert check_image_modern_format(page(items)).status == "pass"


def test_modern_format_ignores_vectors_and_extensionless_cdn_urls():
    items = [
        img(src="https://example.com/logo.svg", actual_format="svg"),
        img(src="https://cdn.example.com/cdn-cgi/image/w=800/hero", actual_format=None),
        img(src="https://example.com/photo.webp"),
    ]
    outcome = check_image_modern_format(page(items))
    assert outcome.status == "pass"
    assert outcome.score == 100  # judged on the one classifiable raster image


def test_modern_format_is_n_a_when_no_image_declares_a_format():
    items = [img(src="https://cdn.example.com/cdn-cgi/image/w=800/hero", actual_format=None)]
    outcome = check_image_modern_format(page(items))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"


def test_modern_format_is_weighted_by_bytes_not_image_count():
    items = [
        img(src="https://example.com/large.jpg", actual_format="jpg", bytes=900_000),
        img(src="https://example.com/small.webp", actual_format="webp", bytes=50_000),
        img(src="https://example.com/tiny.avif", actual_format="avif", bytes=50_000),
    ]
    outcome = check_image_modern_format(page(items))
    assert outcome.status == "fail"
    assert outcome.score == 10
    assert "900000 of 1000000" in outcome.reasoning


def test_modern_format_is_honestly_n_a_without_transfer_bytes():
    outcome = check_image_modern_format(page([img(bytes=None, capture_status="network_error")]))
    assert outcome.status == "n_a"
    assert outcome.remediation


# ---------------------------------------------------------------------------
# image_oversized


def oversized_item(intrinsic: int, display: int) -> dict:
    return img(
        src=f"https://example.com/hero-{intrinsic}.webp",
        srcset=[f"https://example.com/hero-{intrinsic}.webp"],
        srcset_widths=[intrinsic],
        width=display,
        natural_width=intrinsic,
        sizes=None,
    )


def test_oversized_fails_on_a_wildly_overfetched_image():
    outcome = check_image_oversized(page([oversized_item(4000, 200)]))
    assert_db_valid(outcome)
    assert outcome.status == "fail"
    assert outcome.score == 25
    assert "4000px" in outcome.reasoning and "200px" in outcome.reasoning


def test_oversized_bands_step_down_with_the_ratio():
    major = check_image_oversized(page([oversized_item(1200, 200)]))  # 6x
    assert (major.status, major.score) == ("warn", 50)
    minor = check_image_oversized(page([oversized_item(600, 200)]))  # 3x
    assert (minor.status, minor.score) == ("warn", 80)


def test_oversized_allows_retina_headroom():
    """A 2x intrinsic width is CORRECT on a high-DPR screen, not a defect."""
    ratio = IMAGE_OVERSIZE_MINOR_RATIO
    assert check_image_oversized(page([oversized_item(int(200 * ratio), 200)])).status == "pass"
    assert IMAGE_OVERSIZE_SEVERE_RATIO > IMAGE_OVERSIZE_MINOR_RATIO


def test_oversized_applies_transfer_byte_bands_and_reports_waste():
    warning = check_image_oversized(
        page([img(width=800, natural_width=800, bytes=IMAGE_OVERSIZE_WARN_BYTES + 1)])
    )
    assert (warning.status, warning.score) == ("warn", 50)
    failure = check_image_oversized(
        page([img(width=800, natural_width=800, bytes=IMAGE_OVERSIZE_FAIL_BYTES + 1)])
    )
    assert (failure.status, failure.score) == ("fail", 25)
    waste = check_image_oversized(page([img(width=200, natural_width=800, bytes=100_000)]))
    assert waste.evidence["estimated_waste_bytes"] == 93_750


def test_oversized_uses_captured_dimensions_even_when_sizes_is_declared():
    item = oversized_item(4000, 200)
    item["sizes"] = "(max-width: 600px) 100vw, 200px"
    outcome = check_image_oversized(page([item]))
    assert outcome.status == "fail"


def test_oversized_is_n_a_when_capture_has_no_natural_dimensions():
    outcome = check_image_oversized(page([img(natural_width=None)]))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert "bytes" in outcome.reasoning


# ---------------------------------------------------------------------------
# broken_images — blocked on a capture pass, and says so


def test_broken_images_is_n_a_when_capture_failed_before_status():
    outcome = check_broken_images(page([img(http_status=None, capture_status="network_error")]))
    assert_db_valid(outcome)
    assert outcome.status == "n_a"
    assert "status-checked" in outcome.reasoning


def test_broken_images_fires_once_statuses_are_captured():
    """The contract the capture pass has to satisfy."""
    items = [img(http_status=200), img(http_status=404), img(http_status=500)]
    outcome = check_broken_images(page(items))
    assert_db_valid(outcome)
    assert outcome.status == "fail"
    assert outcome.score == 50 and outcome.issue_count == 2
    items.append(img(http_status=403))
    worse = check_broken_images(page(items))
    assert worse.score == 25 and worse.issue_count == 3
    assert check_broken_images(page([img(http_status=200)])).status == "pass"


def test_broken_images_rejects_html_returned_with_a_200_status():
    outcome = check_broken_images(page([img(http_status=200, content_type="text/html")]))
    assert outcome.status == "fail"


def test_broken_images_does_not_pass_partial_status_capture():
    outcome = check_broken_images(
        page([img(http_status=200), img(http_status=None, capture_status="network_error")])
    )
    assert outcome.status == "n_a"
    assert outcome.remediation


# ---------------------------------------------------------------------------
# End to end — real HTML through the real auditor


def test_real_html_reaches_the_image_checks():
    html = """
    <html><body>
      <img src="/hero.jpg" srcset="/hero-3000.jpg 3000w" width="250" loading="lazy">
      <img src="/a.png">
      <img src="/b.png">
      <img src="/c.png">
      <picture><source type="image/avif" srcset="/d.avif"><img src="/d.jpg"></picture>
    </body></html>
    """
    evidence = evidence_from_audit(audit_html(html, "https://example.com/page"), http_status=200)
    assert len(evidence.image_items) == 5
    assert evidence.image_items[0]["srcset_widths"] == [3000]
    assert evidence.image_items[4]["picture_formats"] == ["avif"]

    assert check_image_dimension_attrs(evidence).status == "fail"
    assert check_image_lazy_loading(evidence).status == "fail"  # lazy hero
    assert check_image_modern_format(evidence).status == "n_a"  # bytes need live capture
    assert check_image_oversized(evidence).status == "n_a"  # natural dimensions need capture
    assert check_broken_images(evidence).status == "n_a"  # never status-checked


def test_a_page_that_does_images_right_passes_end_to_end():
    html = """
    <html><body>
      <img src="/hero.webp" width="800" height="600" alt="hero">
      <img src="/a.webp" width="400" height="300" alt="a">
      <img src="/b.webp" width="400" height="300" alt="b">
      <img src="/c.webp" width="400" height="300" alt="c" loading="lazy">
      <picture><source type="image/webp" srcset="/d.webp">
        <img src="/d.jpg" width="400" height="300" alt="d" loading="lazy"></picture>
    </body></html>
    """
    evidence = evidence_from_audit(audit_html(html, "https://example.com/page"), http_status=200)
    for check in IMAGE_CHECKS:
        outcome = check(evidence)
        assert_db_valid(outcome)
        assert outcome.status in ("pass", "n_a"), f"{check.__name__}: {outcome}"
