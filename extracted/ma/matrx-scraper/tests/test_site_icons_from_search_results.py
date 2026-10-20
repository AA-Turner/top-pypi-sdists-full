"""Brave's own site icons reach the reader's screen, never the model's text."""

from matrx_scraper.search.search import generate_search_text_summary, site_icons_from_search_results

ICON = "https://imgs.search.brave.com/abc/rs:fit:32:32:1:0/g:ce/aHR0cA"
RESULTS = [
    (
        "q",
        {
            "web": {
                "results": [
                    {"url": "https://example.com/a", "title": "A", "meta_url": {"favicon": ICON}},
                    {"url": "https://nofavicon.org/b", "title": "B", "meta_url": {}},
                    {"url": "https://bad.net/c", "title": "C", "meta_url": {"favicon": "javascript:x"}},
                ]
            },
            "news": {"results": [{"url": "https://news.site/n", "meta_url": {"favicon": ICON + "n"}}]},
        },
    ),
    ("empty", None),
]


def test_maps_each_result_url_to_its_provider_icon():
    assert site_icons_from_search_results(RESULTS) == {
        "https://example.com/a": ICON,
        "https://news.site/n": ICON + "n",
    }


def test_the_model_text_never_carries_the_icons():
    assert ICON not in generate_search_text_summary(RESULTS)
