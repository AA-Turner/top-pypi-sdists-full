"""A GET that DOES something is never crawled (2026-10-30: `?add-to-cart=`
URLs were fetched on live stores and then judged as pages)."""

import pytest

from matrx_scraper.utils.url import is_action_url


@pytest.mark.parametrize(
    "url",
    [
        "https://ritualcoffee.com/shop/merch-gifts/heavy-drinker-tee?add-to-cart=80269",
        "https://shop.example/cart?remove_item=abc&_wpnonce=1",
        "https://blog.example/post?replytocom=12#respond",
        "https://shop.example/?wc-ajax=get_refreshed_fragments",
        "https://site.example/wp-login.php?action=lostpassword",
        "https://site.example/account/logout",
    ],
)
def test_action_urls_are_detected(url):
    assert is_action_url(url)


@pytest.mark.parametrize(
    "url",
    [
        "https://shop.example/products/mug",
        "https://shop.example/collections/cups?sort=price",
        "https://shop.example/cart",
        "https://site.example/page?action-figures=1",
        "https://site.example/index.php?action=view&id=3",
    ],
)
def test_ordinary_pages_are_not_actions(url):
    assert not is_action_url(url)


def test_the_crawler_excludes_action_urls():
    from types import SimpleNamespace

    from matrx_scraper.crawler import SiteCrawler

    fake = SimpleNamespace(
        base_host="ritualcoffee.com",
        config=SimpleNamespace(follow_subdomains=False, max_depth=None),
        _exclude=[],
        _include=[],
    )
    decide = SiteCrawler._classify_pure
    assert decide(fake, "https://ritualcoffee.com/shop/tee?add-to-cart=80269", 1) == (
        "excluded", "excluded", "action_url",
    )
    assert decide(fake, "https://ritualcoffee.com/shop/tee", 1)[2] == "accepted"
