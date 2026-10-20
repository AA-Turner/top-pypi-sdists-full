"""A bot wall answered with HTTP 200 is a FAILED read, never a success (2026-10-19, "Try advanced reader" lane).

The Walmart "Robot or human?" page came back from the server browser as a successful 464-char read: the
browser rung only classified walls on status >= 400, and the content-sanity gate (the one place every
result passes) did not know walls. Texts below are real rows of ``scraper.scrape_parsed_page``.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from matrx_scraper.content_sanity import BOT_WALL, assess

WALMART = (
    "# Robot or human?\nActivate and hold the button to confirm that you’re human. Thank You!\n"
    "[Terms of Use](https://help.walmart.com/app/answers/detail/a_id/8) "
    "[Privacy Policy](https://corporate.walmart.com/privacy-security) "
    "[Do Not Sell My Personal Information](https://www.walmart.com/account/api/ccpa-intake?native=false&type=sod)\n"
    "© 2026 Walmart Stores, Inc."
)


def _result(text: str, title: str | None = None, url: str = "https://www.walmart.com/ip/x/1"):
    return SimpleNamespace(success=True, text_data=text, title=title, url=url, response_url=url)


@pytest.mark.parametrize(
    ("title", "text"),
    [
        ("Robot or human?", WALMART),
        (None, WALMART),  # title lost: the text alone is enough
        (None, "# Sorry, you have been blocked\n## You are unable to access einnews.com\n## Why have I been blocked? " + "x" * 40),
        (None, "# 403 ERROR\n## The request could not be satisfied.\nRequest blocked. We can't connect to the server for this app."),
        (None, "#### Click the button below to continue shopping\n[Conditions of Use](https://www.amazon.com/gp/help/customer/display.html)"),
        (None, "# Let's confirm you are human\nComplete the security check before continuing."),
        (None, "# One more step\n## Please complete the security check to access the site"),
        (None, "# Please wait\nWe are optimizing your request for the best experience.\n\nPlease Wait"),
    ],
)
def test_a_short_wall_is_a_failure_even_when_the_status_said_200(title, text):
    v = assess(_result(text, title))
    assert v.is_failure and v.failure_reason == BOT_WALL, v
    assert "bot check" in (v.message or "")


def test_a_real_page_that_mentions_a_robot_is_untouched():
    article = "# Robots in the kitchen\n" + ("A long and real article about robot or human cooks. " * 80)
    assert not assess(_result(article, "Robots in the kitchen")).is_failure


def test_a_short_real_page_is_still_only_thin_not_a_wall():
    v = assess(_result("# Example Domain\nThis domain is for use in documentation examples without needing permission.",
                       "Example Domain", "https://example.com/"))
    assert not v.is_failure
