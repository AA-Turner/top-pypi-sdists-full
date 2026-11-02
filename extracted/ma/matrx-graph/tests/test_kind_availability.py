"""Kind Availability Index — the picker, path exposure, and trigger primitive.

Pins the behaviors Arman ratified (plan of record §7.7): nested kinds surface
from the REGISTRY even when the workflow never names them, selection carries its
own path (which is what retires extraction nodes), "unused" is the default view,
availability is workflow-wide, and a kind that contains itself neither hangs nor
disappears.

FIXTURES MODEL THE REAL PILOT SHAPE. The search kinds pilot (Stage A, approved
2026-08-20) registered a MULTI-SECTION result — web / news / video / local /
entity sections, each its own kind, with shared core primitives (`rating`,
`opening_hours`) nested inside — NOT a flat list of one "website" kind. A node
built on the flat assumption silently loses most of what a search returns, so
these fixtures use the registered slugs and the sectioned shape. (The index was
also run against the live registered schemas themselves — `local_place`
surfaces `opening_hours`/`rating`/`postal_address`/`geo_coordinates` with
correct paths, unmodified.)
"""

from __future__ import annotations

from matrx_graph.content_ir.availability import (
    NodeKindDeclaration,
    build_availability_index,
)
from matrx_graph.content_ir.model import KindModel


class Rating(KindModel, kind="rating"):
    value: float
    count: int | None = None


class OpeningHours(KindModel, kind="opening_hours"):
    monday: str | None = None


class WebResult(KindModel, kind="web_result"):
    url: str
    title: str
    snippet: str = ""
    rating: Rating | None = None


class NewsResult(KindModel, kind="news_result"):
    url: str
    title: str
    published_at: str | None = None


class VideoResult(KindModel, kind="video_result"):
    url: str
    duration_s: int | None = None


class LocalPlace(KindModel, kind="local_place"):
    name: str
    rating: Rating | None = None
    hours: OpeningHours | None = None


class SearchResults(KindModel, kind="search_results"):
    """The sectioned root: different section kinds, never one flattened list."""

    query: str
    web: list[WebResult] = []
    news: list[NewsResult] = []
    videos: list[VideoResult] = []
    places: list[LocalPlace] = []


class Comment(KindModel, kind="comment"):
    body: str
    replies: list["Comment"] = []


Comment.model_rebuild()


SCHEMAS = {
    "search_results": SearchResults.model_json_schema(),
    "web_result": WebResult.model_json_schema(),
    "news_result": NewsResult.model_json_schema(),
    "video_result": VideoResult.model_json_schema(),
    "local_place": LocalPlace.model_json_schema(),
    "rating": Rating.model_json_schema(),
    "opening_hours": OpeningHours.model_json_schema(),
    "comment": Comment.model_json_schema(),
}


def _search_workflow() -> list[NodeKindDeclaration]:
    return [
        NodeKindDeclaration(
            node_id="search", label="Brave search", output_kind="search_results", step=1
        ),
        NodeKindDeclaration(
            node_id="summarize",
            label="Summarize",
            output_kind="web_result",
            consumes=("search_results",),
            step=2,
        ),
        NodeKindDeclaration(node_id="report", label="Report", step=3),
    ]


def test_every_section_kind_surfaces_not_just_one_flattened_type() -> None:
    # The mistake this pins: treating every search result as one "website"
    # kind loses most of what a search returns. All sections must surface.
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    reachable = {(e.kind, e.reference()) for e in index.entries}
    assert ("web_result", "search.web[]") in reachable
    assert ("news_result", "search.news[]") in reachable
    assert ("video_result", "search.videos[]") in reachable
    assert ("local_place", "search.places[]") in reachable


def test_nested_kinds_surface_though_the_workflow_never_names_them() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    reachable = {(e.kind, e.reference()) for e in index.entries}
    # Core primitives two levels down, never mentioned by the definition.
    assert ("rating", "search.web[].rating") in reachable
    assert ("rating", "search.places[].rating") in reachable
    assert ("opening_hours", "search.places[].hours") in reachable


def test_selection_carries_its_path() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    hours = next(e for e in index.entries if e.kind == "opening_hours")
    # This accessor is what makes an extraction node unnecessary.
    assert hours.reference() == "search.places[].hours"
    assert hours.is_nested is True


def test_collections_are_marked() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    news = next(e for e in index.entries if e.kind == "news_result" and e.depth == 1)
    assert news.is_collection is True
    hours = next(e for e in index.entries if e.kind == "opening_hours")
    assert hours.is_collection is False


def test_unused_is_the_pickers_default_view() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    unused = {e.kind for e in index.unused()}
    used = {e.kind for e in index.used_entries()}
    assert "search_results" in used  # summarize consumes it
    assert {"news_result", "video_result", "local_place", "opening_hours"} <= unused


def test_availability_is_workflow_wide_not_adjacency_bound() -> None:
    # 'report' is wired to nothing, yet everything produced before it is
    # offered: "just because something goes from step two to three doesn't
    # mean that step nine can't also consume it."
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    kinds = {e.kind for e in index.for_node("report")}
    assert {"search_results", "web_result", "news_result", "local_place", "rating"} <= kinds


def test_a_node_is_not_offered_its_own_output() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    assert index.for_node("search") == ()


def test_order_is_respected_when_known() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    # summarize runs at step 2, so search (step 1) is available...
    assert any(e.source_node_id == "search" for e in index.for_node("summarize"))
    # ...and a later node's output is not offered to an earlier one.
    assert not any(e.source_node_id == "summarize" for e in index.for_node("summarize"))


def test_of_kind_finds_every_occurrence_at_any_depth() -> None:
    # What a kind-triggered node subscribes against: "doesn't matter how
    # deeply nested they are". `rating` appears in web results, in places,
    # AND inside the web_result that 'summarize' outputs — all must be seen.
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    assert sorted(e.reference() for e in index.of_kind("rating")) == [
        "search.places[].rating",
        "search.web[].rating",
        "summarize.rating",
    ]


def test_self_referencing_kind_terminates_and_is_marked() -> None:
    declarations = [NodeKindDeclaration(node_id="thread", output_kind="comment", step=1)]
    index = build_availability_index(declarations, SCHEMAS.get)
    replies = [e for e in index.entries if e.path.endswith("replies[]")]
    assert len(replies) == 1
    # Recorded, marked "more inside", and not walked forever.
    assert replies[0].truncated is True


def test_unregistered_kind_is_loud_but_still_offered() -> None:
    declarations = [NodeKindDeclaration(node_id="n", output_kind="not_registered", step=1)]
    index = build_availability_index(declarations, SCHEMAS.get)
    assert index.unresolved_kinds == ("not_registered",)
    # The workflow declares it, so hiding it would make the picker lie; only
    # its interior is unknown.
    entry = index.entries[0]
    assert entry.kind == "not_registered"
    assert entry.truncated is True


def test_from_node_shows_everything_one_node_offers() -> None:
    index = build_availability_index(_search_workflow(), SCHEMAS.get)
    kinds = {e.kind for e in index.from_node("search")}
    assert kinds == {
        "search_results",
        "web_result",
        "news_result",
        "video_result",
        "local_place",
        "rating",
        "opening_hours",
    }


# ---------------------------------------------------------------------------
# Declared composition (content_ir.kind_edge) — the OTHER nesting source.
#
# Measured on the live registry 2026-08-20: 51 parent kinds declare their
# composition in kind_edge while pinning `__kind` on NOTHING — every kind
# registered before KindModel existed (flashcard_set -> cards -> flashcard,
# quiz_set -> questions -> quiz_question, study_notes -> sections/glossary).
# With only the schema walk their interiors are invisible to the picker, which
# is the precise capability §7.7a promises. Verified live: Study Pack v1 went
# from 13 entries / 0 nested to 20 / 7 once edges were consulted.
# ---------------------------------------------------------------------------


LEGACY_SCHEMAS = {
    # A pre-KindModel registration: real $defs, no discriminator anywhere.
    "flashcard_set": {
        "type": "object",
        "properties": {
            "title": {"type": "string"},
            "cards": {"type": "array", "items": {"$ref": "#/$defs/flashcard"}},
        },
        "$defs": {"flashcard": {"type": "object", "properties": {"front": {"type": "string"}}}},
    },
    "flashcard": {"type": "object", "properties": {"front": {"type": "string"}}},
    "enhanced_flashcard": {"type": "object", "properties": {"front": {"type": "string"}}},
}

LEGACY_EDGES = {
    "flashcard_set": (("cards", "flashcard"), ("cards", "enhanced_flashcard")),
}


def _legacy_declarations() -> list[NodeKindDeclaration]:
    return [NodeKindDeclaration(node_id="make", output_kind="flashcard_set", step=1)]


def test_declared_composition_surfaces_what_the_schema_cannot() -> None:
    index = build_availability_index(
        _legacy_declarations(),
        LEGACY_SCHEMAS.get,
        resolve_edges=lambda slug: LEGACY_EDGES.get(slug, ()),
    )
    reachable = {(e.kind, e.reference()) for e in index.entries}
    assert ("flashcard", "make.cards[]") in reachable
    # Without edges the same registration is a featureless blob.
    schema_only = build_availability_index(_legacy_declarations(), LEGACY_SCHEMAS.get)
    assert {e.kind for e in schema_only.entries} == {"flashcard_set"}


def test_one_field_may_declare_several_child_kinds() -> None:
    # flashcard_set.cards really does declare three card kinds live. The list
    # may hold any of them, so hiding two would make the picker lie.
    index = build_availability_index(
        _legacy_declarations(),
        LEGACY_SCHEMAS.get,
        resolve_edges=lambda slug: LEGACY_EDGES.get(slug, ()),
    )
    at_cards = {e.kind for e in index.entries if e.reference() == "make.cards[]"}
    assert at_cards == {"flashcard", "enhanced_flashcard"}


def test_collection_ness_comes_from_the_schema_not_the_edge() -> None:
    index = build_availability_index(
        _legacy_declarations(),
        LEGACY_SCHEMAS.get,
        resolve_edges=lambda slug: LEGACY_EDGES.get(slug, ()),
    )
    card = next(e for e in index.entries if e.kind == "flashcard")
    assert card.is_collection is True  # `cards` is an array in the schema


def test_a_kind_declared_in_BOTH_sources_appears_once() -> None:
    # The converged state (a KindModel kind that also has kind_edge rows) must
    # not double-report — the picker would show the same value twice.
    edges = {"search_results": (("web", "web_result"),)}
    index = build_availability_index(
        _search_workflow(), SCHEMAS.get, resolve_edges=lambda s: edges.get(s, ())
    )
    at_web = [e for e in index.entries if e.reference() == "search.web[]"]
    assert len(at_web) == 1


def test_an_edge_resolver_that_fails_never_breaks_the_picker() -> None:
    def _boom(_slug: str):
        raise RuntimeError("registry down")

    index = build_availability_index(_search_workflow(), SCHEMAS.get, resolve_edges=_boom)
    # Schema-derived entries still resolve — a degraded registry read yields a
    # smaller world, never no world.
    assert any(e.kind == "web_result" for e in index.entries)
