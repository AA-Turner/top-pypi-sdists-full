"""the view registry: (entity kind, view) -> builder, each view's options, and what a builder takes and returns."""

from __future__ import annotations
from dataclasses import dataclass, field
from collections.abc import Callable
from typing import Any
from ...shared.reads.search_contract import EntityType
from ..generated.views import VIEW_PURPOSE, View


@dataclass(frozen=True)
class _Req:
    """What a view builder needs beyond the entity itself."""

    filters: dict[str, Any]
    offset: int
    #: Last row the previous page sent, for a view resuming on its route's own cursor
    #: (`_ViewData.resume_key`); None on a first page.
    after: str | None = None
    #: The ref as written; a catalog view reads its version selector (`dataset:c4@3`) from it.
    ref: str | None = None
    #: Caller's `token_budget`, for a view that sizes its FIXED part to it (lineage link glance).
    token_budget: int = 2000
    #: Ids of work the caller's own session created, when it asked to hide it
    #: (`X-Probe-Hide-Session-Work`) and the entity is not that work; else None. For views that
    #: reshape reads before the structural scrub (lineage named links, picks events). A call, made
    #: AFTER the view's own reads so work created in between is in the set.
    hidden: Callable[[], frozenset[str] | None] = lambda: None


@dataclass
class _ViewData:
    """One view's payload, split by what SCALES.

    `rows` is the unbounded part (what token_budget bounds and cursor walks); `payload` the fixed
    part. rows=None is ATOMIC: never truncated (see ResearchReadService.research_get).
    `more_beyond`: the backend has rows past the fetched window. Forgetting it LIES: a 200-span
    fetch of a 500-span run would be reported complete.
    `no_match`: the view answered fully and nothing satisfies the constraint. NOT `missing`
    (nothing is absent, so "partial" would read as a degraded backend); see EnvelopeState.NO_MATCH.
    """

    payload: dict[str, Any] = field(default_factory=dict)
    rows: list[dict] | None = None
    rows_key: str = "rows"
    missing: list[str] = field(default_factory=list)
    more_beyond: bool = False
    no_match: bool = False
    #: Row field holding the ROUTE'S OWN cursor: rows are one route page read from `_Req.after`
    #: and the next cursor names the last row sent, not an offset into a re-read.
    resume_key: str | None = None
    #: Route cursor of the last row FETCHED, before filtering (session-work exclusion). If
    #: filtering empties a page the walk resumes past it, else it would re-ask the same rows forever.
    resume_fetched: str | None = None
    #: Fit WHOLE rows to the budget exactly (`_fit_resume_rows`) with an offset cursor, for rows
    #: with no unique key. The chars/4 estimate undercounts uuid-heavy rows, so a filled page
    #: overflows into text fragments of its JSON.
    exact_fit: bool = False


_VIEWS: dict[tuple[str, str], str] = {
    # 0124: run and experiment cards carry a notes excerpt and each kind gains a full `notes` view
    # (sweep groups and files carry none). A caveat an agent must know to ask for is one it never
    # reads, and a run's caveat is the one most likely to change what its numbers mean.
    (EntityType.RUN, View.CARD): "_view_card_with_notes",
    (EntityType.RUN, View.NOTES): "_view_run_notes",
    (EntityType.RUN, View.TRAJECTORY): "_view_trajectory",
    (EntityType.RUN, View.METRICS): "_view_metrics",
    (EntityType.RUN, View.ARTIFACTS): "_view_run_artifacts",
    (EntityType.RUN, View.REPRODUCE): "_view_reproduce",
    (EntityType.RUN, View.HANDOFF): "_view_handoff",
    (EntityType.RUN, View.LINEAGE): "_view_run_lineage",
    (EntityType.RUN, View.EVENTS): "_view_events",
    # 0135. The AUTHORED inventory, not `trajectory` narrowed to rollouts: those spans carry no
    # title, description or note, so an agent cannot see a researcher already wrote down what went
    # wrong on trial 34. A sidecar also outlives the bounded span slice that would report it absent.
    (EntityType.RUN, View.TRIALS): "_view_run_trials",
    # Phase 6: the run's resolved owner/repo@sha, plus the diff against another run via
    # view_options={"compare_to": ...} (see the builder for why it rides this view, not `reproduce`).
    (EntityType.RUN, View.CODE): "_view_run_code",
    # Metric views saved on the run: the id a chart or follow-up read names one by; listed nowhere else.
    (EntityType.RUN, View.VIEWS): "_view_run_views",
    # One trial's begin/end FILESYSTEM diff (sandbox-state bundle); needs `view_options.trial`.
    # Rows are changed paths; `counts` totals the whole scan whatever the window.
    (EntityType.RUN, View.DIFF): "_view_run_diff",
    # Captured coding sessions that produced the run. Only the run BUNDLE carries them
    # (`GET /v1/runs/{ref}` does not, `handoff` drops them): "which session made this run" had no answer.
    (EntityType.RUN, View.SESSIONS): "_view_run_sessions",
    # Its data edits (agentic W&B B.4), read-only: a rescaled or cut curve is not what the run logged.
    (EntityType.RUN, View.EDITS): "_build_run_edits_view",
    # What was asked of it while it ran (agentic W&B C.1), read-only: a stop or LR change explains a curve's turn.
    (EntityType.RUN, View.COMMANDS): "_build_run_commands_view",
    (EntityType.EXPERIMENT, View.CARD): "_view_card_with_notes",
    (EntityType.EXPERIMENT, View.NOTES): "_view_experiment_notes",
    (EntityType.EXPERIMENT, View.SUMMARY): "_view_experiment_summary",
    (EntityType.EXPERIMENT, View.OVERVIEW): "_view_experiment_overview",
    (EntityType.EXPERIMENT, View.ARTIFACTS): "_view_experiment_artifacts",
    # Lineage plan 2 (L12/L18): an experiment's OWN links and children with origins (the same read
    # as a project's) plus, as `run_edges`, the graph AMONG its runs and files this view always returned.
    (EntityType.EXPERIMENT, View.LINEAGE): "_view_project_lineage",
    (EntityType.EXPERIMENT, View.GROUPS): "_view_groups",
    (EntityType.EXPERIMENT, View.VERSIONS): "_view_versions",
    (EntityType.EXPERIMENT, View.REPRODUCE): "_view_experiment_reproduce",
    # Phase 6: what changed in the repo between this experiment's runs. The CARD stays untouched:
    # the backend experiment read has no code facts (unlike the project row's `code_sources`), so a
    # card hint would add a backend call to the cheapest read (sub-notes N+1 rule); `available_views`
    # already advertises `code`.
    (EntityType.EXPERIMENT, View.CODE): "_view_experiment_code",
    # A fork's source runs and their files, read live through its link; the card's `read_inherited` hint (forks only) is the door.
    (EntityType.EXPERIMENT, View.INHERITED): "_view_experiment_inherited",
    # Captured sessions on the experiment, newest first, walkable past the route's page
    # (GET …/experiments/{E}/sessions), and the summary's version history (GET …/summary/versions[/{v}]),
    # so a recorder rewriting the summary can read what it replaces and whose sessions it covers.
    (EntityType.EXPERIMENT, View.SESSIONS): "_view_experiment_sessions",
    (EntityType.EXPERIMENT, View.SUMMARY_HISTORY): "_view_experiment_summary_history",
    (EntityType.PROJECT, View.CARD): "_view_project_card",
    (EntityType.PROJECT, View.NOTES): "_view_project_notes",
    (EntityType.PROJECT, View.SUMMARY): "_view_project_summary",
    (EntityType.PROJECT, View.OVERVIEW): "_view_project_overview",
    # 0134: attached repositories + proxied commit timeline. The card carries a bounded `code`
    # block like notes: a connection an agent must know to ask for is one it never sees.
    (EntityType.PROJECT, View.CODE): "_view_project_code",
    # A project's only view was `card`, so a project-anchored artifact (`probe artifact add
    # --project`, fold #22) was write-only over MCP: stored, unreadable, worse than untracked.
    (EntityType.PROJECT, View.ARTIFACTS): "_view_project_artifacts",
    # 0152: the literature a project was built from. Its own view, not a card block: a review's
    # papers are the project's CONTENT, and the card's bounded excerpt would truncate the summaries worth reading.
    (EntityType.PROJECT, View.PAPERS): "_view_project_papers",
    (EntityType.PROJECT, View.LINEAGE): "_view_project_lineage",
    # The attached repo's README as text; a document view, delivery pages its markdown (repo and commit ride along).
    (EntityType.PROJECT, View.README): "_view_project_readme",
    # The project's sessions (GET /v1/projects/{P}/sessions) and summary versions; see the experiment pair above.
    (EntityType.PROJECT, View.SESSIONS): "_view_project_sessions",
    (EntityType.PROJECT, View.SUMMARY_HISTORY): "_view_project_summary_history",
    # Lines of work (swarm visibility D6): a project's tree, an experiment's own line and the ones
    # it split from. Compact by default; one branch in full with `view_options.branch`.
    (EntityType.PROJECT, View.BRANCHES): "_view_project_branches",
    (EntityType.EXPERIMENT, View.BRANCHES): "_view_experiment_branches",
    # Best-pick history (#3624): every pick and clear, newest first, who and why (churn the
    # branches header's one current pick cannot show). Projects only: the best route takes a
    # project; a workspace's history rides `browse mode=branches`.
    (EntityType.PROJECT, View.PICKS): "_view_project_picks",
    (EntityType.GROUP, View.CARD): "_view_card",
    # One rollout as an entity (0135). NO `notes` view or card excerpt, unlike every other entity: a
    # Trial has no notes document. A rollout ran once and is immutable, so `description` holds what
    # a reader needs; a second free-text field is one more place to look. `trajectory` needs work: see below.
    (EntityType.TRIAL, View.CARD): "_view_card",
    (EntityType.TRIAL, View.TRAJECTORY): "_view_trial_trajectory",
    # Artifacts: the reuse-before-create seam, reached by NAME; where the retired `asset:<name>`
    # check went. #143 folded assets into artifacts and for one release the instructions named a
    # route with no builder: compliant agents got a 422 and read it as licence to duplicate,
    # inverting the guard. Lineage reads `GET /v1/artifacts/{id}/lineage` (0255): the run that wrote
    # the file and the runs that read it. It was absent before the route, as an empty answer would
    # read as "no lineage".
    (EntityType.ARTIFACT, View.LINEAGE): "_view_artifact_lineage",
    (EntityType.ARTIFACT, View.CARD): "_view_card",
    (EntityType.ARTIFACT, View.VERSIONS): "_view_artifact_versions",
    # Captured sessions that registered or touched the file ("who made this"; not in its own row).
    (EntityType.ARTIFACT, View.SESSIONS): "_view_artifact_sessions",
    # The file's own TEXT in bounded line sections (like a session transcript). Binary, oversized
    # and reference-only files refuse by name and point at `probe artifact download`.
    (EntityType.ARTIFACT, View.CONTENT): "_view_artifact_content",
    # One titled SUB-NOTE (0146). Like the team note its card IS the document (`notes` shows 700-char
    # excerpts; the rest lives here). Card only: see the RECORD note below.
    (EntityType.SUB_NOTE, View.CARD): "_view_sub_note_card",
    # The TEAM NOTE (research-os 0125). Its `card` IS the document: excerpting would send an agent
    # asking for the briefing on a second call. The bounded excerpt lives on `browse_research`. No
    # `versions` view: the team note keeps no history, by design.
    (EntityType.TEAM_NOTE, View.CARD): "_view_team_note_card",
    # Captured coding-agent sessions. The card is the session's WORK read (what it touched, by
    # entity type): a session is "the one that produced run X", not its megabytes of dialogue. The
    # transcript is served in bounded line sections behind its own view, with `filters.grep` for
    # search WITHIN one document (search ranks chunks across every session and an exact id can miss its window).
    (EntityType.SESSION, View.CARD): "_view_card",
    (EntityType.SESSION, View.TRANSCRIPT): "_view_session_transcript",
    # Data catalog (C4), on `/v1/catalog` and `/v1/provenance`. A dataset's `versions` is its version
    # list, a checkpoint's the run's other saves; a source has none (a revision is part of its key).
    # `lineage` is the provenance walk, reaching SOURCES, which run and artifact lineage cannot name.
    (EntityType.DATASET, View.CARD): "_view_dataset_card",
    (EntityType.DATASET, View.VERSIONS): "_view_dataset_versions",
    (EntityType.DATASET, View.LINEAGE): "_view_catalog_lineage",
    (EntityType.CHECKPOINT, View.CARD): "_view_checkpoint_card",
    (EntityType.CHECKPOINT, View.VERSIONS): "_view_checkpoint_saves",
    (EntityType.CHECKPOINT, View.LINEAGE): "_view_catalog_lineage",
    (EntityType.SOURCE, View.CARD): "_view_card",
    (EntityType.SOURCE, View.LINEAGE): "_view_catalog_lineage",
}
# Every kind with a card gets the raw record, except a sub-note (its card IS the record, and
# `VIEW_MATRIX` declares it card-only). Serving a pair the matrix lacks would invent a word.
_VIEWS.update(
    {
        (kind, View.RECORD): "_view_record"
        for kind, view in _VIEWS
        if view == View.CARD and kind != EntityType.SUB_NOTE
    }
)

# Filters each (kind, view) accepts, mapped onto the backend's REAL server-side filters. Anything
# else is rejected loudly: a silently-ignored filter returns a full result the agent believes narrowed.
# Keyed by (kind, view): GET /v1/projects/{id}/artifacts takes no filters, so `kind` is honest on a
# RUN's artifacts and a lie on an experiment's.
_VIEW_OPTIONS: dict[tuple[str, str], set[str]] = {
    (EntityType.RUN, View.TRAJECTORY): {"span_type", "parent_span_id", "step_from", "step_to"},
    # `span_type` ONLY, applied AFTER the subtree walk, not passed to the route: server-side it would
    # delete intermediate parents and orphan descendants, so a rollout -> turn -> tool_call tree
    # filtered to `tool_call` would come back EMPTY, confidently wrong. `step_from`/`step_to` are
    # absent likewise: the window is chosen from the trial's own step and a caller's could exclude it.
    (EntityType.TRIAL, View.TRAJECTORY): {"span_type"},
    (EntityType.RUN, View.METRICS): {"key", "kind"},
    (EntityType.RUN, View.ARTIFACTS): {"kind", "step_from", "step_to", "name", "scope"},
    # `requirement` is applied HERE: /v1/artifacts/{id}/versions takes no filter, so this is an
    # honest client-side narrowing of a fully-read chain.
    (EntityType.ARTIFACT, View.VERSIONS): {"requirement"},
    # `version` pins the reproduce map to a minted experiment_versions manifest; applied server-side
    # by /v1/projects/{id}/reproduce?version=N.
    (EntityType.EXPERIMENT, View.REPRODUCE): {"version"},
    # `at` is deliberately absent: the SDK accepted and never read it and no backend as-of
    # resolution exists; an advertised no-op is worse than none.
    # Transcript narrowing is CLIENT-SIDE over one complete document the backend returned whole (honest
    # like the artifact `requirement` filter). `grep` is literal and case-insensitive (a regex would
    # answer wrongly on the first bracket in a code-heavy transcript). The recording agent is NOT a
    # filter: `session:<agent>/<id>` names it, and a `source` filter could only contradict the ref.
    (EntityType.SESSION, View.TRANSCRIPT): {"grep", "context_lines", "start_line"},
    (EntityType.ARTIFACT, View.CONTENT): {"grep", "context_lines", "start_line"},
    # The filters `_view_project_code` always read and documented. The entry was MISSING, so
    # `_checked_view_options` rejected them all ("accepts no view options") while the docstring
    # advertised them: the dead-switch failure the "vocabulary spans the wire" rule warns of, fixed
    # alongside phase 6's two new (kind, CODE) pairs.
    (EntityType.PROJECT, View.CODE): {
        "commit",
        "source",
        "cursor",
        "author",
        "path",
        "include_excluded",
    },
    # `compare_to` names the other run (`run:<uuid-or-slug>`, prefix optional); resolved server-side
    # by GET /v1/runs/{ref}/code/compare.
    (EntityType.RUN, View.CODE): {"compare_to"},
    # `depth` (1-5) adds the upstream walk, resolved server-side by GET /v1/runs/{ref}/upstream?depth=N (0255).
    (EntityType.RUN, View.LINEAGE): {"depth"},
    # The sandbox-state diff route's own query parameters. `trial` is REQUIRED there (`Query(...)`),
    # so the builder refuses its absence in the caller's words, not a relayed 422.
    (EntityType.RUN, View.DIFF): {"trial", "path_prefix"},
    # `runs` picks the route's `kind=runs` (source runs) over default `kind=files` (their files).
    (EntityType.EXPERIMENT, View.INHERITED): {"runs"},
    # `version` reads ONE version's markdown (GET …/summary/versions/{v}) in place of the list. The
    # sessions views take NO options: order is fixed to newest and the page walks by `cursor`.
    **{
        (kind, View.SUMMARY_HISTORY): {"version"}
        for kind in (EntityType.PROJECT, EntityType.EXPERIMENT)
    },
    # `branch` picks ONE branch by root ref and returns it in full; a ref that is not one is refused, naming those that are.
    **{
        (kind, View.BRANCHES): {"branch"}
        for kind in (EntityType.PROJECT, EntityType.EXPERIMENT)
    },
    # `links` (swarm friction P6) makes one link list the ROWS, paged whole by `cursor`; the first page shows a glance of each.
    **{
        (kind, View.LINEAGE): {"links"}
        for kind in (EntityType.PROJECT, EntityType.EXPERIMENT)
    },
    # GET /v1/provenance's own parameters: `direction`/`depth` shape the graph, `steps` asks for the methods view (`format=steps`).
    **{
        (kind, View.LINEAGE): {"direction", "depth", "steps"}
        for kind in (EntityType.DATASET, EntityType.SOURCE, EntityType.CHECKPOINT)
    },
}
_VIEW_OPTIONS.update(
    {(kind, View.RECORD): {"field"} for kind, view in _VIEWS if view == View.RECORD}
)


def _supported_views(kind: str) -> list[str]:
    return sorted(str(view) for entity_kind, view in _VIEWS if entity_kind == kind)


def _views_offered(kind: str) -> str:
    """The kind's views, one per line, each with what it returns.

    ERROR PATH ONLY. `available_views` on a response stays a bare list (it rides every card and
    browse node). Here the caller has just shown it did not know, so a gloss is worth its cost.
    A view with no VIEW_PURPOSE line still appears, bare: the list must stay COMPLETE, or a
    missing gloss hiding a real view would be a smaller lie than the one this replaced.
    """
    lines = []
    for name in _supported_views(kind):
        purpose = VIEW_PURPOSE.get(View(name))
        lines.append(f"  {name:<11}{purpose}" if purpose else f"  {name}")
    return "\n".join(lines)
