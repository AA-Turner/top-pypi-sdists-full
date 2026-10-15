"""clean_page_content is the scrape's own ai_research_content; contact_footer_text keeps a contact footer only."""

from matrx_scraper.clean_content import clean_page_content, contact_footer_text

PAGE = """<html><body><header><nav><a href="/">Home</a><a href="/about">About us</a></nav></header>
<main><h1>Coffee roasted in San Francisco</h1><p>We roast every morning.</p></main>
<footer>Acme Coffee · 123 Main Street · (415) 555-0100 · hello@acme.com</footer></body></html>"""


def test_clean_page_content_is_the_main_content_without_menu_or_footer():
    text = clean_page_content(PAGE, "https://acme.com/")
    assert "Coffee roasted in San Francisco" in text
    assert "About us" not in text and "hello@acme.com" not in text


def test_contact_footer_is_kept_only_when_it_holds_contacts():
    assert "hello@acme.com" in (contact_footer_text(PAGE) or "")
    assert contact_footer_text("<html><body><main>x</main><footer>© 2026 Acme</footer></body></html>") is None
