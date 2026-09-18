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
The shapes are the database's as of
`20260918100000_seo_topical_map_23_a_persons_edge_is_never_overwritten`, which
added `kept_existing` (`PageMapping`, `IntentWriteResult`) and `kept`
(`set_page_intents`): precedence is human > agent > mapper, so a write from a
lower source never overwrites, deletes or replaces an edge a higher source
holds — it is reported as kept instead. Kept means a person's (or higher
source's) decision stands; it is settled — an agent must never retry it or
report it as a failure:

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


class KeptTopicCoverage(KindSubModel):
    """One slug a `map_pages` write left alone (migration 23 precedence)."""

    slug: str
    #: human | agent | mapper | null — who holds this pair. Kept means a person's
    #: (or higher source's) decision stands; it is settled, do not retry.
    kept_existing: str | None = None


class PageMapping(KindSubModel):
    page_id: str | None = None
    url: str | None = None
    ok: bool
    map_id: str | None = None
    covers: int | None = None
    replaced: int | None = None
    unknown_slugs: list[str] | None = None
    #: pairs a HIGHER source (human > agent > mapper) already held, left untouched
    #: rather than overwritten (migration 23). Kept means a person's (or higher
    #: source's) decision stands; it is settled — do not retry, do not report as failed.
    kept_existing: list[KeptTopicCoverage] | None = None
    #: the per-item refusal (e.g. `set_pages_map_topics_denied` for a page not of `site`).
    error: str | None = None


# ── page intents (`page_intents`, `set_page_intents`) ────────────────────────


class IntentPage(EntityRef):
    """`seo.list_page_intents` page projection + its Search Console totals."""

    site_id: str | None = None
    clicks: int | None = None
    impressions: int | None = None
    #: the window the totals were summed over (the `performance_window_days` knob).
    performance_window_days: int | None = None


class IntentTopicRef(KindSubModel):
    slug: str
    name: str


class CoveredTopic(KindSubModel):
    """A `covers` edge: where the page sits TODAY."""

    slug: str
    name: str
    confidence: int | None = None
    #: mapper | human | agent — who asserted the coverage.
    source: str | None = None


class PageIntent(KindSubModel):
    """The one `intent` edge of a page: where it is GOING and what happens to it."""

    topic: IntentTopicRef
    #: keep | move | merge | redirect | rewrite | delete.
    disposition: str
    #: proposed | accepted | done.
    state: str | None = None
    source: str | None = None
    note: str | None = None
    #: merge / redirect only: the live page or planned page it points at. Null when
    #: the destination row is one the caller cannot open — the same as no destination.
    into: EntityRef | None = None
    updated_at: str | None = None


class PageIntentRow(KindSubModel):
    page: IntentPage
    current_topics: list[CoveredTopic]
    #: null when the page carries `covers` edges but no intent yet.
    intent: PageIntent | None = None


class KeptIntent(KindSubModel):
    """Who holds a page's intent edge when `set_page_intents` left it alone
    (migration 23 precedence: human > agent > mapper, or already accepted/done)."""

    source: str | None = None
    state: str | None = None


class IntentWriteResult(KindSubModel):
    """One `set_page_intents` write outcome: succeeded, failed, or kept because a
    higher source already holds the edge."""

    ok: bool
    page_id: str | None = None
    url: str | None = None
    error: str | None = None
    #: present only on a kept item. Kept means a person's (or higher source's)
    #: decision stands; it is settled — do not retry, do not report as failed.
    kept_existing: KeptIntent | None = None


# ── gaps, history, planned pages (`topic_gaps`, `map_history`, `create_planned_page`) ──


class TopicGap(KindSubModel):
    """A topic of the map carrying no live page and no planned page."""

    slug: str
    name: str
    status: str
    depth: int
    keyword_count: int


class MapHistoryRow(KindSubModel):
    """A topic the map no longer shows — rejected or retired — and who changed it.

    `changed_at` / `changed_by` come from `history.row_versions`, so they are the
    platform's record of the change, not a column a writer could set."""

    slug: str
    name: str
    status: str
    description: str | None = None
    parent_slug: str | None = None
    version: int | None = None
    attachments: Attachments | None = None
    changed_at: str | None = None
    changed_by: str | None = None
    #: user | agent | code — the actor tier the change was made under.
    changed_by_tier: str | None = None


class PlannedPage(KindSubModel):
    """The `plan.node` `create_planned_page` had the content plan create. `slug` and
    `route` are the plan's own derivations, never ours."""

    id: str | None = None
    site_id: str | None = None
    label: str | None = None
    slug: str | None = None
    route: str | None = None
    node_type: str | None = None
    page_type: str | None = None
    status: str | None = None


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
    #: search hits · associations · facet_values listings · map_pages per-page results ·
    #: set_page_intents per-item write results.
    results: (
        list[SearchHit | AssociationRow | FacetValueRow | PageMapping | IntentWriteResult] | None
    ) = None
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

    # page intents
    #: `page_intents`: one row per page carrying an intent OR a `covers` edge.
    #: Each listing keeps its OWN key — three shapes under one `items` would make an
    #: agent guess which one it is holding, and would widen a published kind's field.
    items: list[PageIntentRow] | None = None
    #: `page_intents`: the unpaged count, and the window actually applied.
    total: int | None = None
    limit: int | None = None
    offset: int | None = None
    performance_window_days: int | None = None
    #: `page_intents`: extra `intent` edges beyond the one per page that should exist —
    #: nonzero is a data defect, never hidden.
    duplicate_intents: int | None = None
    #: `set_page_intents`: how many intents were written (`failed` counts the rest).
    set: int | None = None
    #: `set_page_intents`: how many items were left alone because a higher source
    #: (human > agent > mapper) already held the edge, or it was already
    #: accepted/done (migration 23). Kept means that decision stands; it is
    #: settled — do not retry, and never report a kept item as failed.
    kept: int | None = None

    # proposals and planned pages
    #: `reject_topics`: the proposals moved to `status = 'rejected'` — kept, never lost.
    rejected: list[RemovedTopic] | None = None
    #: `create_planned_page`: the node the content plan created (or would create).
    node: PlannedPage | None = None
    #: `topic_gaps`: topics with no live page and no planned page.
    gaps: list[TopicGap] | None = None
    #: `map_history`: topics the map no longer shows, newest change first.
    history: list[MapHistoryRow] | None = None


TopicNode.model_rebuild()

__all__ = ["TopicalMapResult"]
