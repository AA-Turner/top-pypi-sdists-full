from matrx_scraper.meta_metrics import (
    DESCRIPTION_DESKTOP_PIXEL_LIMIT,
    DESCRIPTION_MOBILE_PIXEL_LIMIT,
    TITLE_DESKTOP_PIXEL_LIMIT,
    TITLE_MOBILE_PIXEL_LIMIT,
    calculate_meta_description_metrics,
    calculate_meta_title_metrics,
)


def test_mobile_and_desktop_use_the_same_metadata_allowances() -> None:
    assert TITLE_MOBILE_PIXEL_LIMIT == TITLE_DESKTOP_PIXEL_LIMIT == 600
    assert DESCRIPTION_MOBILE_PIXEL_LIMIT == DESCRIPTION_DESKTOP_PIXEL_LIMIT == 920


def test_metadata_that_only_failed_the_old_mobile_limits_now_passes() -> None:
    title = calculate_meta_title_metrics("W" * 30)
    description = calculate_meta_description_metrics("W" * 70)

    assert title["pixel_width"] == 564
    assert title["desktop_ok"] is True
    assert title["mobile_ok"] is True
    assert title["title_ok"] is True

    assert description["pixel_width"] == 855
    assert description["desktop_ok"] is True
    assert description["mobile_ok"] is True
    assert description["description_ok"] is True
