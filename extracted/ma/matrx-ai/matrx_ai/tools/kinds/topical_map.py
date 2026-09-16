"""`topical_map_result` — the ONE result kind of the `topical_map` agent tool.

The tool is an action dispatcher over a brand's topical map (the tree of topics
that website plans, page targeting and content are built on). Every action's
result is the seo RPC's own JSON passed through under the key the contract
names, plus `action` and `map_id`. One union kind across every action, the
`cms_page` precedent, not a kind per action (the near-duplicate the kind
doctrine forbids).

EVERY key is typed: the tool validates each result against this model before
returning it, so a database contract change that adds, drops or reshapes a key
fails loudly as `result_kind_mismatch` instead of reaching an agent untyped.
The shapes are the database's as of `seo_topical_map_18`:

* an associated item the caller cannot open is ABSENT from every listing (no
  entry, no count); a facet value's `ref` to such a row is `null`, the same as no
  ref — so there is no "hidden" variant anywhere here;
* `merge` reports no foreign-organization count;
* `upsert` has no `errors` (it is all-or-nothing and raises); only `patch` reports
  per-edit `errors`;
* ids are the whitelisted projection of `platform.resolve_entity_ref`, never a row.

Field semantics live with the stored tool definition (`tool.definition` row);
the implementation is `aidream/tools/topical_map_tool.py` (this package never
imports aidream).

Publish with::

    uv run python scripts/publish_kind_catalog.py matrx_ai.tools.kinds.topical_map --apply
"""

from __future__ import annotations

from typing import Literal

from matrx_graph.content_ir.model import KindModel, KindSubModel
from matrx_graph.content_ir.sdk import kind
from pydantic import JsonValue

# ── shared pieces ────────────────────────────────────────────────────────────


class EntityRef(KindSubModel):
    """`platform.resolve_entity_ref` projection of a row the caller may open."""

    type: str
    id: str
    label: str | None = None
    slug: str | None = None
    url: str | None = None
    status: str | None = None
    country_code: str | None = None
    region_code: str | None = None
    region: str | None = None
    city: str | None = None


class Attachments(KindSubModel):
    """What hangs off a topic, counted within the map's organization (absent = 0)."""

    pages: int | None = None
    planned: int | None = None
    keywords: int | None = None
    facets: int | None = None
    #: every other association to or from the topic.
    other: int | None = None


# ── associations (`associations`, `tree`/`get` with include) ─────────────────


class Association(KindSubModel):
    kind: str
    direction: Literal["in", "out"]
    role: str | None = None
    #: what the writer recorded on the edge (e.g. reason / confidence / source / site_id).
    payload: dict[str, JsonValue] | None = None


class AssociatedItem(EntityRef):
    #: set on `seo_map_facet_value` items: the facet key and the value's own ref.
    facet: str | None = None
    ref: EntityRef | None = None


class AssociationRow(KindSubModel):
    topic: str
    association: Association
    item: AssociatedItem


# ── topics ───────────────────────────────────────────────────────────────────


class TopicNode(KindSubModel):
    """One topic of `tree` / `get`. Condensed = slug, name, children; the rest by `include`."""

    slug: str
    name: str
    description: str | None = None
    status: str | None = None
    pages: int | None = None
    planned: int | None = None
    keywords: int | None = None
    path: list[str] | None = None
    #: facet key → value slug.
    facets: dict[str, str] | None = None
    associations: list[AssociationRow] | None = None
    children: list[TopicNode] | None = None
    #: children beyond `depth`, or folded to fit the output budget.
    children_count: int | None = None


class SearchHit(KindSubModel):
    slug: str
    name: str
    status: str
    path: list[str]


# ── maps and facets listings ─────────────────────────────────────────────────


class MapSite(KindSubModel):
    site_id: str
    name: str | None = None
    domain: str | None = None


class MapSummary(KindSubModel):
    id: str
    name: str
    description: str | None = None
    status: str
    brand_id: str
    created_at: str | None = None
    updated_at: str | None = None
    topic_count: int
    sites: list[MapSite]


class MapRow(KindSubModel):
    """The map row written by `create_map` / `update_map` (or what a dry run would write)."""

    id: str | None = None
    name: str | None = None
    description: str | None = None
    status: str | None = None
    brand_id: str | None = None
    organization_id: str | None = None
    created_at: str | None = None
    updated_at: str | None = None
    #: dry-run `create_map` only: how many topics `tree` would create.
    topics_in_tree: int | None = None


class FacetValueRow(KindSubModel):
    facet: str
    label: str | None = None
    description: str | None = None
    applies_to: str | None = None
    inherits: bool | None = None
    is_builtin: bool | None = None
    value_id: str
    slug: str
    name: str | None = None
    ref_type: str | None = None
    ref_id: str | None = None
    parent_slug: str | None = None
    brand_owned: bool


# ── page coverage (`map_pages`) ──────────────────────────────────────────────


class PageMapping(KindSubModel):
    page_id: str | None = None
    url: str | None = None
    ok: bool
    map_id: str | None = None
    covers: int | None = None
    replaced: int | None = None
    unknown_slugs: list[str] | None = None
    #: the per-item refusal (e.g. `set_pages_map_topics_denied` for a page not of `site`).
    error: str | None = None


# ── graph ────────────────────────────────────────────────────────────────────


class GraphTopicData(KindSubModel):
    slug: str
    name: str
    description: str | None = None
    status: str
    depth: int
    parent_id: str | None = None
    sort_order: int | None = None
    page_count: int
    planned_count: int
    keyword_count: int
    facets: dict[str, str] | None = None
    auto_layout: bool | None = None


class GraphFacetData(KindSubModel):
    slug: str
    name: str
    facet: str | None = None
    parent_id: str | None = None
    ref: EntityRef | None = None


class GraphNode(KindSubModel):
    id: str
    type: Literal["topic", "facet_value"]
    position: dict[str, float] | None = None
    data: GraphTopicData | GraphFacetData


class GraphEdge(KindSubModel):
    id: str
    type: Literal["tree", "facet"]
    source: str
    target: str
    inherited: bool | None = None


# ── diagnostics ──────────────────────────────────────────────────────────────


class CrowdedTopic(KindSubModel):
    slug: str
    pages: int


class PageRef(KindSubModel):
    page_id: str
    url: str | None = None


class PageOnManyTopics(PageRef):
    topics: int


class RetiredWithAttachments(KindSubModel):
    slug: str
    attachments: Attachments


class MapDiagnostics(KindSubModel):
    topics_total: int
    topics_empty: int
    topics_empty_sample: list[str]
    topics_crowded: list[CrowdedTopic]
    topics_proposed: list[str]
    pages_on_many_topics: list[PageOnManyTopics]
    pages_on_no_topic: int
    pages_on_no_topic_sample: list[PageRef]
    retired_with_attachments: list[RetiredWithAttachments]
    #: only sites the caller may view.
    sites_using_map: list[str]


# ── write reports ────────────────────────────────────────────────────────────


class RemovedTopic(KindSubModel):
    slug: str
    #: retired | retired_with_attachments | attachments_moved_to_parent | attachments_merged_into_<slug>
    action: str | None = None
    attachments: Attachments
    message: str | None = None


class EditError(KindSubModel):
    """`patch` only: one edit that did not apply (the rest did)."""

    slug: str | None = None
    message: str


# ── the kind ─────────────────────────────────────────────────────────────────


@kind(
    "topical_map_result",
    label="Topical Map Result",
    family="seo",
    example={
        "action": "tree",
        "map_id": "9c1a2f3e-0000-4000-8000-000000000001",
        "root": None,
        "total_topics": 1,
        "topics": [{"slug": "recycling", "name": "Recycling", "children": []}],
    },
    maturity="placeholder",
)
class TopicalMapResult(KindModel):
    action: str
    map_id: str | None = None
    site_id: str | None = None
    dry_run: bool | None = None
    #: `map_dry_run` names the function it rolled back.
    function: str | None = None
    ok: bool | None = None
    note: str | None = None
    #: rows dropped from `omitted_from` to fit the output budget (the note says how to narrow).
    omitted: int | None = None
    omitted_from: str | None = None

    # reads
    #: `outline` — the text block an agent reasons over.
    outline: str | None = None
    maps: list[MapSummary] | None = None
    #: `tree` / `get`: the root slug the tree was taken from (null = the map roots).
    root: str | None = None
    #: `tree` from the roots.
    topics: list[TopicNode] | None = None
    total_topics: int | None = None
    #: `tree` with a root, and `get`.
    topic: TopicNode | None = None
    #: search hits · associations · facet_values listings · map_pages per-page results.
    results: list[SearchHit | AssociationRow | FacetValueRow | PageMapping] | None = None
    nodes: list[GraphNode] | None = None
    edges: list[GraphEdge] | None = None
    group_by: str | None = None
    diagnostics: MapDiagnostics | None = None

    # map rows
    map: MapRow | None = None

    # write reports
    created: list[str] | None = None
    updated: list[str] | None = None
    unchanged: list[str] | None = None
    moved_in: list[str] | None = None
    removed: list[RemovedTopic] | None = None
    errors: list[EditError] | None = None
    #: `move` / `set_facet`: the topic acted on.
    slug: str | None = None
    #: `move`: the new parent (null = root); `split`: the topic split.
    parent: str | None = None
    #: `split`: where the parent's attachments went ("left on parent").
    attachments: str | None = None
    #: `merge`.
    into: str | None = None
    retired: list[str] | None = None
    associations_moved: int | None = None
    associations_dropped_as_duplicate: int | None = None
    planned_pages_moved: int | None = None
    keywords_moved: int | None = None
    children_reparented: int | None = None
    #: `set_facet`.
    facet: str | None = None
    value: str | None = None
    cleared: str | None = None
    #: `map_pages`.
    mapped: int | None = None
    failed: int | None = None


TopicNode.model_rebuild()

__all__ = ["TopicalMapResult"]
