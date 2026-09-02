from __future__ import annotations

import pytest
from bs4 import BeautifulSoup

from matrx_scraper.media_embed import video_embed_provider
from matrx_scraper.parser.transform import HtmlTransformer


@pytest.mark.parametrize(
    ("url", "provider"),
    [
        ("https://www.youtube.com/embed/abc123", "youtube"),
        ("https://www.youtube-nocookie.com/embed/abc123", "youtube"),
        ("https://player.vimeo.com/video/12345", "vimeo"),
        ("https://player.twitch.tv/?channel=matrx", "twitch"),
        ("https://www.loom.com/embed/abc123", "loom"),
        ("https://fast.wistia.net/embed/iframe/abc123", "wistia"),
        ("https://play.vidyard.com/abc123.html", "vidyard"),
    ],
)
def test_video_embed_provider_recognizes_known_media(url: str, provider: str) -> None:
    assert video_embed_provider(url) == provider


@pytest.mark.parametrize(
    "url",
    [
        "https://www.googletagmanager.com/ns.html?id=GTM-EXAMPLE",
        "https://challenges.cloudflare.com/turnstile/v0/",
        "https://www.google.com/recaptcha/api2/anchor",
        "https://example.com/application-frame",
    ],
)
def test_video_embed_provider_rejects_non_media_iframes(url: str) -> None:
    assert video_embed_provider(url) is None


def test_html_transformer_only_rewrites_recognized_video_iframes() -> None:
    transformed = HtmlTransformer(
        """
        <iframe src="https://www.youtube.com/embed/abc123"></iframe>
        <iframe src="https://www.googletagmanager.com/ns.html?id=GTM-EXAMPLE"></iframe>
        """
    ).process()

    assert isinstance(transformed, BeautifulSoup)
    video = transformed.find("video")
    assert video is not None
    assert video.get("provider") == "youtube"
    iframe = transformed.find("iframe")
    assert iframe is not None
    assert "googletagmanager.com" in str(iframe.get("src"))
