"""Bot-challenge interstitials are walls, never Sources (2026-09-26: a Reddit "Prove your
humanity" page landed as Source 5deb9bc0). Breaks these tests name: a known vendor challenge
page not detected; a real article that embeds a captcha on its comment form called a wall."""

from __future__ import annotations

import pytest

from matrx_scraper.scraper import detect_challenge_reasons

REDDIT = (
    "<html><head><title>Reddit - Prove your humanity</title></head><body><h1>Prove your humanity</h1>"
    "<p>We’re committed to safety and security. But not for bots. Complete the challenge below and "
    "let us know you’re a real person.</p></body></html>"
)

WALLS = {
    "reddit": REDDIT,
    "cloudflare": "<html><head><title>Just a moment...</title></head><body>Checking if the site connection is secure</body></html>",
    "cloudflare-block": "<html><head><title>Attention Required!</title></head><body>Why have I been blocked?</body></html>",
    "akamai": "<html><head><title>Access Denied</title></head><body>You don't have permission to access this server. Reference #18.abc</body></html>",
    "perimeterx": "<html><head><title>Access to this page has been denied</title></head><body><div id='px-captcha'></div>Press &amp; Hold to confirm you are a human</body></html>",
    "hcaptcha": "<html><head><title>example.com</title></head><body><iframe src='https://newassets.hcaptcha.com/captcha/v1'></iframe></body></html>",
    "recaptcha": "<html><head><title>Checkpoint</title></head><body><div class='g-recaptcha' data-sitekey='x'></div></body></html>",
    "imperva": "<html><head><title>Pardon Our Interruption</title></head><body>As you were browsing something about your browser made us think you were a bot.</body></html>",
    "datadome": "<html><head><title>shop.example</title></head><body><iframe src='https://geo.captcha-delivery.com/captcha/'></iframe></body></html>",
}


@pytest.mark.parametrize("vendor", sorted(WALLS))
def test_a_known_challenge_page_is_a_wall(vendor: str) -> None:
    from selectolax.parser import HTMLParser

    soup = HTMLParser(WALLS[vendor])
    title_node = soup.css_first("title")
    assert detect_challenge_reasons(soup=soup, title=title_node.text() if title_node else None), vendor


def test_a_real_article_with_a_comment_captcha_is_not_a_wall() -> None:
    from selectolax.parser import HTMLParser

    article = "<p>" + ("Python's asyncio runs coroutines on an event loop. " * 80) + "</p>"
    html = f"<html><head><title>Asyncio: the complete guide</title></head><body>{article}<div class='g-recaptcha'></div></body></html>"
    assert detect_challenge_reasons(soup=HTMLParser(html), title="Asyncio: the complete guide") == []
