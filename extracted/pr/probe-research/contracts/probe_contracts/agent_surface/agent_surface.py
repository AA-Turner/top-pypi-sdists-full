"""The view vocabulary both agent surfaces (MCP, page generation) speak; generated into agent/.

Imports nothing. Coverage may differ per surface, spelling may not. Why: DESIGN.md.
"""

from __future__ import annotations

from ..compat import StrEnum


class ViewKind(StrEnum):
    """Entities a view can be taken on.

    The shared noun list. A surface serves a subset of it and a contract test
    holds each surface to its subset, so one surface adding a kind never
    silently changes another's vocabulary.
    """

    PROJECT = "project"
    EXPERIMENT = "experiment"
    RUN = "run"
    #: One titled sub-note (0146), by its own id (the one catalog rows and sub-note lists carry).
    #: Card-only: the card is the document (title, body, headroom); history stays on the dashboard.
    SUB_NOTE = "sub_note"
    #: One rollout as an entity, not a span (0135): it carries an authored title, description and notes.
    #: Reached by its rollout span id, the dashboard's URL identity. Why: DESIGN.md (trial).
    TRIAL = "trial"
    ARTIFACT = "artifact"
    #: One paper (0152) a research project was built from. A kind, not a filter on `papers`: it has its
    #: own row, distilled record and citation identity (`source_ref.paper_id`).
    PAPER = "paper"
    GROUP = "group"
    SESSION = "session"
    #: The tenant's one shared note. MCP-only: the assistant gets it in its system prompt every turn
    #: (`render_team_note`), and its cap is the assistant's whole tool-result budget.
    TEAM_NOTE = "team-note"
    #: The data catalog (C3/C4): a team dataset and its versions, an external source, a checkpoint.
    #: Reached by prefix ref only (`app/catalog/refs.py`). MCP-only today.
    DATASET = "dataset"
    SOURCE = "source"
    CHECKPOINT = "checkpoint"


class View(StrEnum):
    """One word per purpose-shaped read.

    THIS IS THE THIN HARNESS. Capability lives in this parameter rather than in
    extra tools, so reading a trajectory costs a `view` value and not a
    `read_run_spans` entry in every turn's catalog. The MCP's own contract module
    says the same thing in the same words, which is the point.
    """

    #: The cheap identity/status glance, and the default everywhere.
    CARD = "card"
    #: Explicit complete-record read on MCP; supports selecting one nested field.
    #: Delivery is bounded separately from the stored record's shape.
    RECORD = "record"
    #: The spans themselves, not span-type COUNTS.
    TRAJECTORY = "trajectory"
    #: Both relations on a run: the parent/child walk and artifact provenance edges (`_view_run_lineage`).
    #: The walk alone said "no lineage" for a run that consumed a dataset and produced 3 artifacts.
    LINEAGE = "lineage"
    #: Everything needed to run it again, plus an honest completeness verdict.
    REPRODUCE = "reproduce"
    #: The append-only lifecycle log.
    EVENTS = "events"
    #: Saved metric views. Without it an agent could save a view but never list it back.
    VIEWS = "views"
    #: One trial's begin/end filesystem diff. Needs a `trial`, which comes off
    #: the run's own files.
    DIFF = "diff"
    #: Which coding sessions produced this thing.
    SESSIONS = "sessions"
    #: The files registered under this entity. MCP-only as a VIEW.
    ARTIFACTS = "artifacts"
    #: Free-text notes as a document of their own.
    NOTES = "notes"
    #: Sweeps and ensembles under an experiment.
    GROUPS = "groups"
    #: Rollouts under a run (like `GROUPS` on an experiment: a trial has one parent run). Filtering the
    #: run's spans for `rollout` returns spans, not authored Trials, so no title, description or note.
    TRIALS = "trials"
    #: Immutable published manifests.
    VERSIONS = "versions"
    #: A session's normalized transcript, in bounded sections.
    TRANSCRIPT = "transcript"
    #: A project's rendered README.
    README = "readme"
    #: Dashboard-visible authored Markdown on a project, experiment or run.
    SUMMARY = "summary"
    #: Complete unified saved Overview, including generated and authored content.
    OVERVIEW = "overview"
    #: Series summaries. MCP-only; the MCP's `metrics` tool is the richer
    #: per-grain read.
    METRICS = "metrics"
    #: Everything a new session needs to continue. MCP-only today.
    HANDOFF = "handoff"
    #: GitHub resolution per grain: a project's code sources and proxied timeline; an experiment's per-run
    #: `owner/repo@sha` and stored commit window; a run's own (compare diffs another). MCP-only today.
    CODE = "code"
    #: A published document's own text, bounded (the artifact-content lane, 1.36, as a view). An
    #: unpublished artifact refuses it; everything else about an artifact stays metadata.
    CONTENT = "content"
    #: A project's papers (0152), one row each: the paper's idea, the repo read alongside it, where they
    #: disagree. MCP-only today; the dashboard shows the same rows as a tab.
    PAPERS = "papers"
    #: What a fork reads live from its source: its runs as they were at the fork, or their files. Same
    #: word in the API and CLI (`GET .../experiments/{E}/inherited`, `probe experiment inherited`).
    INHERITED = "inherited"
    #: A project's or experiment's summary versions, newest first (who, when, via what), or one by number.
    #: MCP-only; a recorder rewriting the summary must see what it replaces and what a person last wrote.
    SUMMARY_HISTORY = "summary_history"
    #: Lines of work: a project's tree, or an experiment's line and those it split from; best value on the
    #: declared metric, effort, state, links (swarm D6). MCP-only; workspace: `browse mode=branches`.
    BRANCHES = "branches"
    #: A project's best-pick history, newest first: each pick and clear, who and why (#3624). The branches
    #: header shows only the current pick, hiding churn. MCP-only; workspace: rides `browse mode=branches`.
    PICKS = "picks"


#: What a view MEANS on a kind. The union across both surfaces; each declares the
#: subset it serves. A pair absent here is a pair neither surface may invent.
VIEW_MATRIX: dict[ViewKind, frozenset[View]] = {
    ViewKind.SUB_NOTE: frozenset({View.CARD}),
    ViewKind.PROJECT: frozenset(
        {
            View.CARD,
            View.RECORD,
            View.NOTES,
            View.SUMMARY,
            View.README,
            View.OVERVIEW,
            View.SESSIONS,
            View.ARTIFACTS,
            View.CODE,
            View.PAPERS,
            # lineage plan 2 (L12/L18): its OWN links, in and out, and its
            # children each with a derived origin (GET /v1/projects/{id}/lineage).
            View.LINEAGE,
            # The summary's versions (GET /v1/projects/{P}/summary/versions[/{v}]).
            View.SUMMARY_HISTORY,
            # Its tree's lines of work (GET /v1/projects/{P}/branches).
            View.BRANCHES,
            # Its best pick's history (GET /v1/projects/{P}/best?history=N).
            View.PICKS,
        }
    ),
    ViewKind.EXPERIMENT: frozenset(
        {
            View.CARD,
            View.RECORD,
            View.NOTES,
            View.GROUPS,
            View.VERSIONS,
            View.REPRODUCE,
            View.LINEAGE,
            View.SESSIONS,
            View.ARTIFACTS,
            View.SUMMARY,
            View.OVERVIEW,
            # integrations-v2 phase 6: repo changes between this experiment's runs
            # (stored rows only; GET /v1/experiments/{ref}/code).
            View.CODE,
            # A fork's runs and files read live from its source
            # (GET /v1/projects/{P}/experiments/{E}/inherited).
            View.INHERITED,
            # The summary's versions
            # (GET /v1/projects/{P}/experiments/{E}/summary/versions[/{v}]).
            View.SUMMARY_HISTORY,
            # Its own line of work and the ones it split from
            # (GET /v1/projects/{P}/experiments/{E}/branch).
            View.BRANCHES,
        }
    ),
    ViewKind.RUN: frozenset(
        {
            View.CARD,
            View.RECORD,
            View.NOTES,
            View.TRAJECTORY,
            View.LINEAGE,
            View.REPRODUCE,
            View.EVENTS,
            View.VIEWS,
            View.DIFF,
            View.SESSIONS,
            View.METRICS,
            View.HANDOFF,
            View.ARTIFACTS,
            View.TRIALS,
            # integrations-v2 phase 6: the run's owner/repo@sha, and a diff against another run
            # (GET /v1/runs/{ref}/code and /code/compare).
            View.CODE,
        }
    ),
    # The one entity with no notes (immutable; `description` holds it). Its `trajectory` is its whole
    # subtree, which narrowing the run's cannot give; no `artifacts` or `diff`: DESIGN.md (trial views).
    ViewKind.TRIAL: frozenset({View.CARD, View.RECORD, View.TRAJECTORY}),
    #: `lineage` (0255): which run wrote this file and which read it. No `notes` here or on a group: since
    #: 2026-10-16 a file is described in its run's notes, a sweep in its experiment's.
    ViewKind.ARTIFACT: frozenset(
        {
            View.CARD,
            View.RECORD,
            View.VERSIONS,
            View.SESSIONS,
            View.CONTENT,
            View.LINEAGE,
        }
    ),
    ViewKind.GROUP: frozenset({View.CARD, View.RECORD}),
    #: `card` is the distilled record (row plus digest, what comparisons use). No separate `digest`
    #: view: the useful read would always be the second call.
    ViewKind.PAPER: frozenset({View.CARD}),
    ViewKind.SESSION: frozenset({View.CARD, View.RECORD, View.TRANSCRIPT}),
    ViewKind.TEAM_NOTE: frozenset({View.CARD, View.RECORD}),
    #: `versions`: a dataset's versions, a checkpoint's run's other saves. `lineage`: the provenance walk
    #: (`GET /v1/provenance`), which reaches sources. A source has no versions: its revision is in its key.
    ViewKind.DATASET: frozenset({View.CARD, View.RECORD, View.VERSIONS, View.LINEAGE}),
    ViewKind.CHECKPOINT: frozenset({View.CARD, View.RECORD, View.VERSIONS, View.LINEAGE}),
    ViewKind.SOURCE: frozenset({View.CARD, View.RECORD, View.LINEAGE}),
}


#: One agent-facing line per view (what it returns, no history), for the error a wrong view raises
#: and the MCP `entity` schema. `available_views` stays bare (`_views_offered`, MCP service); a view
#: absent here prints bare. DESIGN.md. These are the MCP reads: the page writer's own `summary`
#: reads only the person-written block (app/generation/agent/views/readers/summaries.py).
VIEW_PURPOSE: dict[View, str] = {
    View.CARD: "identity, status, and this kind's available_views",
    View.RECORD: "the raw source record, pageable; one field via view_options.field",
    View.SUMMARY: "the dashboard's Summary tab as text (Markdown; charts as placeholders)",
    View.OVERVIEW: "the same Summary page as saved HTML, with its chart data",
    View.NOTES: "hidden operational notes: decisions, caveats, handoffs",
    View.ARTIFACTS: "the files the work produced at this grain",
    View.VERSIONS: "an artifact's or dataset's versions (a checkpoint: its run's saves); the reuse check",
    View.METRICS: "series summaries; view_options.key drills to raw points",
    View.TRAJECTORY: "the spans themselves -- ask a TRIAL for one rollout's subtree",
    View.TRIALS: "the run's authored trials, newest step first",
    View.EVENTS: "the append-only lifecycle log",
    View.LINEAGE: "what it came from: parents, files read, and who wrote them",
    View.REPRODUCE: "everything needed to run it again, plus a completeness verdict",
    View.HANDOFF: "what a new session needs to continue the work",
    View.CODE: "the GitHub resolution at this grain; diff with view_options.compare_to",
    View.GROUPS: "sweeps and ensembles under an experiment",
    View.PAPERS: "the literature attached to this project",
    View.TRANSCRIPT: "a captured session's text; view_options.grep or view_options.start_line",
    View.SESSIONS: "the captured agent sessions that touched this entity",
    View.CONTENT: "the artifact's own bytes",
    View.README: "the repository's README at this grain",
    View.VIEWS: "saved metric views on this entity",
    View.DIFF: "what changed, against the comparison this kind defines",
    View.INHERITED: "what a fork reads live from its source: its files, or its runs with runs=true",
    View.SUMMARY_HISTORY: "the summary's versions, newest first; view_options.version=N reads one's markdown",
    View.BRANCHES: "lines of work: best value, effort, state; view_options.branch for one in full",
    View.PICKS: "the best pick's history, newest first: who picked or cleared what, and why",
}


class MissingMarker(StrEnum):
    """Why a payload is incomplete, in words a model can act on.

    A view that clips and says nothing is worse than one that refuses: the model
    reads a short list as a complete list and answers confidently from it. Every
    projection that can clip must emit one of these.
    """

    #: The server capped the rows before we saw them, and the route takes no
    #: offset -- so paging here would page an already-truncated list.
    ROWS_CAPPED_BY_SERVER = "rows_capped_by_server"
    #: We asked for a window and the window filled. Move the window, do not page.
    WINDOW_FULL = "window_full"
    #: The source route answered, but with a degraded body (legacy rows).
    SOURCE_DEGRADED = "source_degraded"


class Admits(StrEnum):
    """What citing power a GRANTED view hands the summary writer.

    THE HALF THAT MAKES CITING SAFE, as a table rather than as a branch. A
    Tier-2 grant widens the context and the allowed-ref set together, and the
    two must move as one -- so the rule lives beside the view it belongs to
    rather than inside an `elif` chain that a new view forgets to extend.

    Route-specific ON PURPOSE. A generic "admit whatever came back" reads a
    session digest's incidental run mention as a citeable measurement, and a
    card's `project_id` as something a metric block may point at.
    """

    #: Prose about a thing, not a reading of it. Nothing here is a source.
    NOTHING = "nothing"
    #: The rows the DATABASE returned become citeable -- never the ids asked
    #: for, which is how a scoped-out request stops being an existence oracle.
    RETURNED_IDS = "returned_ids"
    #: A metric read: the run AND the (run, key) pairs it actually carried.
    RUN_AND_METRIC_KEYS = "run_and_metric_keys"


#: Per view, not per kind: a `card` admits its own row's id, run or paper. A view absent here admits
#: NOTHING, asserted by a test so a new view cannot silently inherit citing power.
VIEW_ADMISSION: dict[View, Admits] = {
    View.CARD: Admits.RETURNED_IDS,
    View.RECORD: Admits.NOTHING,
    View.ARTIFACTS: Admits.RETURNED_IDS,
    View.TRIALS: Admits.RETURNED_IDS,
    View.GROUPS: Admits.RETURNED_IDS,
    View.VERSIONS: Admits.RETURNED_IDS,
    View.LINEAGE: Admits.RETURNED_IDS,
    View.PAPERS: Admits.RETURNED_IDS,
    View.INHERITED: Admits.RETURNED_IDS,
    View.TRAJECTORY: Admits.RETURNED_IDS,
    View.METRICS: Admits.RUN_AND_METRIC_KEYS,
    # Prose and documents: readable evidence, never a citation source.
    View.NOTES: Admits.NOTHING,
    View.SESSIONS: Admits.NOTHING,
    View.TRANSCRIPT: Admits.NOTHING,
    View.SUMMARY: Admits.NOTHING,
    View.SUMMARY_HISTORY: Admits.NOTHING,
    View.OVERVIEW: Admits.NOTHING,
    View.README: Admits.NOTHING,
    View.CONTENT: Admits.NOTHING,
    View.REPRODUCE: Admits.NOTHING,
    View.EVENTS: Admits.NOTHING,
    View.HANDOFF: Admits.NOTHING,
    View.CODE: Admits.NOTHING,
    View.DIFF: Admits.NOTHING,
    View.VIEWS: Admits.NOTHING,
    # Computed standings and effort: a reading of many records, not one.
    View.BRANCHES: Admits.NOTHING,
    # Who chose what, and when: a judgement about results, never a reading of one.
    View.PICKS: Admits.NOTHING,
}


#: The pairs the generation surface serves; a test holds its dispatcher to exactly this, and any other
#: pair refuses, naming what is valid. Narrower than VIEW_MATRIX: DESIGN.md (GENERATION_VIEWS).
GENERATION_VIEWS: dict[ViewKind, frozenset[View]] = {
    ViewKind.PROJECT: frozenset(
        {View.CARD, View.NOTES, View.SESSIONS, View.PAPERS, View.ARTIFACTS, View.SUMMARY}
    ),
    ViewKind.EXPERIMENT: frozenset(
        {View.CARD, View.NOTES, View.SESSIONS, View.LINEAGE, View.ARTIFACTS, View.SUMMARY}
    ),
    ViewKind.RUN: frozenset(
        {
            View.CARD,
            View.NOTES,
            View.SESSIONS,
            View.LINEAGE,
            View.METRICS,
            View.ARTIFACTS,
            View.TRIALS,
            # No `summary`: 0220 removed a run's authored document (a column, never on the
            # Overview page lane), so there is nothing to read.
        }
    ),
    ViewKind.TRIAL: frozenset({View.CARD, View.TRAJECTORY}),
    # No `notes`: an artifact carries a `description`, not a notes document.
    ViewKind.ARTIFACT: frozenset({View.CARD, View.VERSIONS, View.CONTENT}),
    ViewKind.SESSION: frozenset({View.CARD}),
    ViewKind.PAPER: frozenset({View.CARD}),
}
