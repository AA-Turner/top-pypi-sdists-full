"""The AI-view projection at the prompt door.

Arman, 2026-08-24: a workflow step emits a kind, the author binds it to an
agent variable, and without a projection the model receives the entire payload
— *"if you overdo it, then you're killing the model's context window."*

These tests pin the three things that make the door safe: it projects when a
kind declares an ai_view, it recurses into collections (where the blow-up
actually lives), and it changes NOTHING for a kind that declares none.
"""

from __future__ import annotations

import json

import pytest

from matrx_ai.config.prompt_values import prompt_safe_value


@pytest.fixture(scope="module")
def scraper_kinds():
    return pytest.importorskip("aidream.services.scraper_kinds.models")


def _big_page(models, url: str = "https://example.com/a"):
    return models.ScrapedPage(
        url=url,
        title="A page",
        markdown="# Heading\n\n[a link](https://elsewhere.com) and ![img](https://i/x.png)",
        plain_text="x" * 40_000,
        research_text="y" * 40_000,
        links=[models.PageLink(target_url=f"https://z.com/{i}") for i in range(400)],
        blocks=[models.PageBlock(type="text", text="b" * 80) for _ in range(150)],
        fingerprint=models.ContentFingerprint(simhash="7046352583261510909"),
    )


def test_a_declared_ai_view_projects_the_payload(scraper_kinds):
    page = _big_page(scraper_kinds)
    full = len(json.dumps(page.model_dump(mode="json")))

    sent = prompt_safe_value(page)

    assert len(sent) < full / 50, "the projection must be a fraction of the payload"
    keys = set(json.loads(sent))
    assert "markdown" in keys, "the body is the point"
    for absent in ("links", "blocks", "plain_text", "research_text", "fingerprint"):
        assert absent not in keys, f"{absent} is already inline in the markdown or is operator data"


def test_the_projection_keeps_the_provenance_a_model_cannot_infer(scraper_kinds):
    sent = json.loads(prompt_safe_value(_big_page(scraper_kinds)))
    for required in ("url", "title", "status_code", "scraped_at"):
        assert required in sent, f"{required} cannot be recovered from the body text"


def test_a_collection_projects_every_item_not_just_the_root(scraper_kinds):
    """The blow-up lives in the items — a 40-page batch is 40 whole pages."""
    batch = scraper_kinds.ScraperBatchResult(
        pages=[_big_page(scraper_kinds, f"https://example.com/{i}") for i in range(5)],
        successful=5,
    )
    full = len(json.dumps(batch.model_dump(mode="json")))

    sent = prompt_safe_value(batch)

    assert len(sent) < full / 50
    payload = json.loads(sent)
    assert len(payload["pages"]) == 5, "every page survives — only its fields are trimmed"
    for page in payload["pages"]:
        assert "markdown" in page
        assert "links" not in page


def test_kind_markers_are_still_stripped_at_this_door(scraper_kinds):
    sent = prompt_safe_value(_big_page(scraper_kinds))
    assert "__kind" not in sent, "the prompt door is one of the two lawful strip doors"


def test_a_kind_without_an_ai_view_is_untouched(scraper_kinds):
    """The projection is opt-in. Silence must mean 'send everything', forever."""
    link = scraper_kinds.PageLink(target_url="https://x.com", anchor_text="x", region="nav")

    sent = json.loads(prompt_safe_value(link))

    assert sent["target_url"] == "https://x.com"
    assert sent["anchor_text"] == "x"
    assert sent["region"] == "nav", "no declaration means no trimming"


def test_a_plain_dict_with_no_kind_is_untouched(scraper_kinds):
    payload = {"anything": "at all", "nested": {"deep": [1, 2, 3]}}
    assert json.loads(prompt_safe_value(payload)) == payload


def test_the_door_never_raises_on_an_unregistered_kind(scraper_kinds):
    payload = {"__kind": "a_kind_that_was_never_registered", "a": 1, "b": 2}
    assert json.loads(prompt_safe_value(payload)) == {"a": 1, "b": 2}
