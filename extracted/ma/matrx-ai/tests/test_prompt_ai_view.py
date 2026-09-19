"""The AI-view projection at the prompt door.

Arman, 2026-08-24: a workflow step emits a kind, the author binds it to an
agent variable, and without a projection the model receives the entire payload
— *"if you overdo it, then you're killing the model's context window."*

These tests pin the three things that make the door safe: it projects when a
kind declares an ai_view, it recurses into collections (where the blow-up
actually lives), and it changes NOTHING for a kind that declares none.

THE FIXTURE IS PACKAGE-LOCAL ON PURPOSE. Until 2026-09-17 these tests read
aidream's ``services.scraper_kinds.models`` through ``pytest.importorskip``,
so in the package suite — where a package may never import aidream — every one
of them SKIPPED, silently and forever. What is under test is this package's
door, not that host module, so the kinds it needs are declared here with the
same ``@kind(..., ai_view=(...))`` primitive a host uses.
"""

from __future__ import annotations

import json

from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind

from matrx_ai.config.prompt_values import prompt_safe_value


@kind("prompt_door_trial_link", label="Trial Link", family="prompt_door_trial")
class TrialLink(KindModel):
    """An item kind that declares NO ai_view — the untouched case."""

    target_url: str = ""
    anchor_text: str = ""
    region: str = ""


@kind(
    "prompt_door_trial_page",
    label="Trial Page",
    family="prompt_door_trial",
    # The body is the markdown; the alternate renderings, the link records and
    # the operator data are all either already inline in it or not reading
    # material. What rides beside the body is only what a model cannot infer
    # from it: where the page came from, when, and whether the read worked.
    ai_view=("url", "title", "status_code", "scraped_at", "markdown"),
)
class TrialPage(KindModel):
    url: str = ""
    title: str = ""
    status_code: int = 200
    scraped_at: str = ""
    markdown: str = ""
    plain_text: str = ""
    research_text: str = ""
    links: list[TrialLink] = []
    fingerprint: str = ""


@kind("prompt_door_trial_batch", label="Trial Batch", family="prompt_door_trial")
class TrialBatch(KindModel):
    pages: list[TrialPage] = []
    successful: int = 0


def _big_page(url: str = "https://example.com/a") -> TrialPage:
    return TrialPage(
        url=url,
        title="A page",
        scraped_at="2026-09-17T00:00:00Z",
        markdown="# Heading\n\n[a link](https://elsewhere.com) and ![img](https://i/x.png)",
        plain_text="x" * 40_000,
        research_text="y" * 40_000,
        links=[TrialLink(target_url=f"https://z.com/{i}") for i in range(400)],
        fingerprint="7046352583261510909",
    )


def test_a_declared_ai_view_projects_the_payload() -> None:
    page = _big_page()
    full = len(json.dumps(page.model_dump(mode="json")))

    sent = prompt_safe_value(page)

    assert len(sent) < full / 50, "the projection must be a fraction of the payload"
    keys = set(json.loads(sent))
    assert "markdown" in keys, "the body is the point"
    for absent in ("links", "plain_text", "research_text", "fingerprint"):
        assert absent not in keys, f"{absent} is already inline in the markdown or is operator data"


def test_the_projection_keeps_the_provenance_a_model_cannot_infer() -> None:
    sent = json.loads(prompt_safe_value(_big_page()))
    for required in ("url", "title", "status_code", "scraped_at"):
        assert required in sent, f"{required} cannot be recovered from the body text"


def test_a_collection_projects_every_item_not_just_the_root() -> None:
    """The blow-up lives in the items — a 40-page batch is 40 whole pages."""
    batch = TrialBatch(
        pages=[_big_page(f"https://example.com/{i}") for i in range(5)],
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


def test_kind_markers_are_still_stripped_at_this_door() -> None:
    sent = prompt_safe_value(_big_page())
    assert "__kind" not in sent, "the prompt door is one of the two lawful strip doors"


def test_a_kind_without_an_ai_view_is_untouched() -> None:
    """The projection is opt-in. Silence must mean 'send everything', forever."""
    link = TrialLink(target_url="https://x.com", anchor_text="x", region="nav")

    sent = json.loads(prompt_safe_value(link))

    assert sent["target_url"] == "https://x.com"
    assert sent["anchor_text"] == "x"
    assert sent["region"] == "nav", "no declaration means no trimming"


def test_a_plain_dict_with_no_kind_is_untouched() -> None:
    payload = {"anything": "at all", "nested": {"deep": [1, 2, 3]}}
    assert json.loads(prompt_safe_value(payload)) == payload


def test_the_door_never_raises_on_an_unregistered_kind() -> None:
    payload = {"__kind": "a_kind_that_was_never_registered", "a": 1, "b": 2}
    assert json.loads(prompt_safe_value(payload)) == {"a": 1, "b": 2}
