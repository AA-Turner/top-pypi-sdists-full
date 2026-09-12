"""Navigation chrome is stripped whether it is a `<nav>`, a role, or a div marker.

`NoiseRemover` matched classes only as exact tokens from a literal list and ids
only as exact strings, so `<nav>`, `div[role=navigation]` and `div.menu` were
removed while `<div class="nav">`, `<div class="navbar">` and
`<div id="header-links">` were not — their link text ("Home About Pricing")
leaked into the page's main text. The break these tests catch: a nav-like
class/id token no longer counted as noise, or the main-content guard removed.

Every expected string is a literal chosen independently of the code.
"""

from __future__ import annotations

import pytest

from matrx_scraper.parser.core import ParserOrchestrator

BODY = "<h1>Article title</h1><p>Real article body copy that must survive parsing.</p>"
NAV_LINKS = '<a href="/">Home</a> <a href="/about">About</a> <a href="/pricing">Pricing</a>'


def _text(html: str) -> str:
    return ParserOrchestrator().parse_content(html, url="https://example.test/page")["text_data"]


def _page(chrome: str) -> str:
    return f"<html><head><title>T</title></head><body>{chrome}<main>{BODY}</main></body></html>"


@pytest.mark.parametrize(
    "case, chrome",
    [
        ("A_nav_tag", f"<nav>{NAV_LINKS}</nav>"),
        ("B1_div_class_nav", f'<div class="nav">{NAV_LINKS}</div>'),
        ("B2_div_class_menu", f'<div class="menu">{NAV_LINKS}</div>'),
        ("B3_div_role_navigation", f'<div role="navigation">{NAV_LINKS}</div>'),
        ("C_div_id_header_links", f'<div id="header-links">{NAV_LINKS}</div>'),
        ("D_div_class_navbar", f'<div class="navbar">{NAV_LINKS}</div>'),
        ("E_div_class_site_nav", f'<div class="site-nav">{NAV_LINKS}</div>'),
        ("F_div_class_nav_primary", f'<div class="nav-primary">{NAV_LINKS}</div>'),
        ("G_div_id_topbar", f'<div id="topbar">{NAV_LINKS}</div>'),
        ("H_div_class_breadcrumbs", f'<div class="breadcrumbs">{NAV_LINKS}</div>'),
        ("I_div_class_skip_links", f'<div class="skip-links">{NAV_LINKS}</div>'),
        ("J_div_class_main_menu", f'<div class="main-menu">{NAV_LINKS}</div>'),
        ("K_div_class_site_header", f'<div class="site-header">{NAV_LINKS}</div>'),
    ],
)
def test_nav_chrome_link_text_never_reaches_text_data(case: str, chrome: str) -> None:
    text = _text(_page(chrome))

    assert "Real article body copy that must survive parsing." in text, case
    for leaked in ("Home", "About", "Pricing"):
        assert leaked not in text, f"{case}: nav link text {leaked!r} leaked into text_data"


def test_article_paragraph_whose_class_merely_contains_nav_survives() -> None:
    """`navigate-your-career` is prose, not chrome: the token is not `nav`."""
    html = (
        "<html><body><article><h1>Careers</h1>"
        '<p class="navigate-your-career">Navigate your career with confidence.</p>'
        "</article></body></html>"
    )
    text = _text(html)

    assert "Navigate your career with confidence." in text


def test_nav_marked_wrapper_holding_the_main_content_survives() -> None:
    """A `div.nav-content` that wraps `<main>` IS the page; the heuristic must not eat it."""
    html = (
        '<html><body><div class="nav-content"><main>'
        "<h1>Only content</h1><p>The whole page lives inside a badly named wrapper.</p>"
        "</main></div></body></html>"
    )
    text = _text(html)

    assert "The whole page lives inside a badly named wrapper." in text
    assert "Only content" in text


def test_nav_marked_element_that_holds_most_of_the_body_text_survives() -> None:
    """No <main>/<article>, but the marked div carries the page's text: keep it."""
    html = (
        '<html><body><div id="header-links"><a href="/">Home</a></div>'
        '<div class="navigation"><h1>Guide</h1>'
        "<p>Paragraph one of a long guide that is clearly the substance of this page.</p>"
        "<p>Paragraph two continues the guide with even more real content for readers.</p>"
        "</div></body></html>"
    )
    text = _text(html)

    assert "Paragraph one of a long guide that is clearly the substance of this page." in text
    assert "Home" not in text.split()
