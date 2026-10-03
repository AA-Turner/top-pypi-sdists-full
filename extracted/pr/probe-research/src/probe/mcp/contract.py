"""Shared /v1/search + MCP-envelope vocabulary (CONTRACT.md, workspaces+kb fold-in).

Enum-style constants so ``service.py`` and ``source.py`` cannot drift on the wire
strings. ``StrEnum`` members are plain ``str`` at runtime, so they serialize and
compare exactly like the literals they replace.
"""

from __future__ import annotations

from probe._compat import StrEnum

# THE SHARED VOCABULARY, generated from research-os `app/core/agent_views.py`
# rather than declared here. Two agent surfaces answer the same question about
# the same record -- this MCP and the dashboard assistant -- and if they answer
# to different WORDS then a researcher who learns one has learned nothing about
# the other, and a fix to one diverges silently from the other. That already
# happened once: this server fixed a lineage bug by returning ancestry AND
# edges, and an independently-written second matrix re-broke it.
#
# Re-exported under the name this module has always used, so every `View.X` in
# this package keeps working. What changed is where the values come from.
#
# THE DOCSTRING IS DELIBERATELY SHORT. An enum on a tool signature ships its
# whole `__doc__` into every session that loads the tools, so the rationale
# lives in comments like this one and never in the docstring.
#
# Refresh with `make gen-views` (or `make regen`) against a research-os
# checkout. Coverage may differ between the surfaces -- this server has no
# saved-metric-view route and the assistant has no `metrics` view because it
# has a richer tool -- but SPELLING may not, and `_VIEWS` is checked against
# this matrix.
from probe.mcp._generated.views import VIEW_MATRIX, VIEW_PURPOSE, View  # noqa: F401


class BackendCorpus(StrEnum):
    """`corpus` values accepted by POST /v1/search."""

    EXPERIMENTS = "experiments"
    FILES = "files"
    GITHUB = "github"
    TRANSCRIPTS = "transcripts"
    # The team note (research-os 0125). ADDITIVE: an older backend simply does
    # not know the value, and the request is otherwise unchanged.
    NOTES = "notes"
    # Session digests (research-os 0105). Reachable from POST /v1/search since it
    # shipped and never added HERE, so `search_in` could not scope to it -- the
    # "SDK-regen tail" CONTRACT.md records. Paid off with the notes rider rather
    # than left for a third feature to trip over.
    DIGESTS = "digests"
    # Papers (research-os 0170), and the THIRD time this tail was paid: the
    # corpus shipped with `index_paper_customers` and never reached this enum,
    # so no `search_in` value could name it. ADDITIVE, like the two above.
    #
    # The one corpus the backend cannot separate by source_key -- papers are
    # written under the EXPERIMENTS key and told apart by document-id prefix
    # after retrieval. That is entirely /v1/search's business; from here it is
    # a corpus value like any other.
    PAPERS = "papers"


# THIS DOCSTRING IS THE MAPPING TABLE'S ONLY AGENT-FACING HOME, and it is here
# rather than in `search_knowledge`'s docstring because the two channels are not
# equal: a client caps a tool `description` (Claude Code slices MCP descriptions
# at 2,048 chars) and passes `input_schema` verbatim at any size. The table used
# to sit in the tool docstring, ~1,150 chars deep, and was silently cut in half
# before any agent read it. tests/test_mcp_schema_docs.py parses the arrows out
# of THIS string and checks them against `_SEARCH_IN_TO_BACKEND`.
#
# The parameter was called `corpora` until it was renamed: the plural read as
# `corpus` + s, and the identity mappings confirmed the misreading on whichever
# value a caller tried first. That history is a comment, not agent-facing text.
class ToolCorpus(StrEnum):
    """``search_knowledge``'s `search_in` vocabulary. NOT the backend's `corpus`
    values -- three coincide, `documents` does not. What each one covers:

      transcripts -> transcripts
      experiments -> experiments
      files -> files
      documents -> github + files
      notes -> notes + experiments
      digests -> digests
      papers -> papers

    `files` is workspace files (scripts, datasets, configs, protocols -- the
    index does not separate those); `documents` is those PLUS indexed GitHub
    docs. `notes` spans two backend corpora on purpose: the team's shared note
    and the notes hanging off projects, experiments, runs and groups. A hit on
    an entity's note comes back AS that entity, so you can open it."""

    # One value, not the former assets/procedures pair: both mapped to the same
    # backend corpus, so narrowing to one never excluded the other. The index has
    # a single bucket for these (IndexDocType.WORKSPACE_FILE), so the split was a
    # distinction the data model cannot make.
    FILES = "files"
    DOCUMENTS = "documents"
    TRANSCRIPTS = "transcripts"
    EXPERIMENTS = "experiments"
    #: The team's shared note and every entity's notes (0125). ONE agent-facing
    #: value over two backend corpora, because "search what the team wrote down"
    #: is one question: entity notes ride their entity's document in
    #: `experiments`, and the team note is its own `notes` corpus. Splitting them
    #: would make a caller pick which KIND of note they wanted before they knew.
    NOTES = "notes"
    #: Session digests (0105): the lane that wrote them retired in 0204 and the
    #: corpus is draining. The value stays legal so an older client's request
    #: is not a 422; expect nothing under it.
    DIGESTS = "digests"
    #: The papers a research project was built from (0170). ITS OWN VALUE rather
    #: than folded into `documents` or `notes`: a paper is its own noun -- what
    #: the FIELD published, not what this team wrote or ran -- and both existing
    #: multi-corpus values fold together things that answer ONE question.
    #: "What has been written about X" is a different question from "what did we
    #: decide about X", and a caller made to guess which bucket holds the
    #: literature would guess wrong.
    PAPERS = "papers"


class EntityType(StrEnum):
    """Entity types across exact hits, semantic refs, and tool results."""

    PROJECT = "project"
    EXPERIMENT = "experiment"
    # Reached by NAME as a ref (`artifact:<name>`), because the reuse check asks
    # "does an official X already exist" and you have the name, not an id -- and
    # because no `GET /v1/artifacts/{id}` read route exists at all. This absorbed
    # the retired `asset` member: #143 folded every asset into an artifact keeping
    # its id, so one noun now covers both.
    ARTIFACT = "artifact"
    RUN = "run"
    # One rollout as an entity (research-os 0135), reached as `trial:<rollout
    # span id>` -- the same id the dashboard's `/runs/{id}/trials/{rolloutSpanId}`
    # URL carries, so a pasted link and a ref name the same record. NOT the same
    # thing as a `rollout` SPAN: the span is what the producer emitted, the Trial
    # is the authored sidecar beside it, and only the sidecar holds a title, a
    # description and a note. Reading the run's spans finds the former and can
    # never see the latter.
    TRIAL = "trial"
    GROUP = "group"  # a sweep/ensemble: an experiment-shaped noun, reached by ref
    FILE = "file"
    DOCUMENT = "document"  # a semantic hit whose ref is null
    # The TEAM NOTE (research-os 0125): the team's shared markdown document.
    # A SINGLETON, and the only member here whose ref carries no value:
    # `ref="team-note"`, never `team-note:<id>`. There is one per tenant and the
    # credential names the tenant, so an id would imply a second one exists and
    # would need a 404 for an id nobody can construct.
    TEAM_NOTE = "team-note"
    # A captured coding-agent session. Reached as `session:<id>` (the id the
    # `sessions` field on a project/experiment/run card carries) or
    # `session:<agent>/<id>` when the caller knows which agent recorded it.
    # Before this member existed a
    # session was metadata riding on other entities: its transcript was
    # searchable (chunk hits) and renderable (dashboard), but not readable here.
    SESSION = "session"
    # One titled SUB-NOTE (0146), by its own UUID: `sub_note:<id>`, the id a
    # `notes` view row and a notes-catalog row carry. Its card IS the document.
    # Before this member existed `view="notes"` showed a 700-character excerpt
    # of each sub-note and pointed at the dashboard for the rest, so the whole
    # body of a caveat tab was unreadable on this surface.
    SUB_NOTE = "sub_note"


class CollapseMode(StrEnum):
    """``search_knowledge(collapse=...)`` — the result-dedupe vocabulary.

    One member today, and deliberately its OWN type rather than a reuse of
    ``EntityType.EXPERIMENT``: those strings coincide, but "dedupe by experiment"
    and "this row IS an experiment" are different ideas, and typing the parameter
    as EntityType would advertise `project`/`run`/`artifact` as collapse modes
    that do not exist.

    `null` (skip the dedupe) is expressed by the parameter being optional, not by
    a member here -- an enum member spelled "none" would be a second way to say
    the same thing.
    """

    EXPERIMENT = "experiment"


# THIS DOCSTRING SHIPS TO EVERY SESSION, uncapped, in `$defs` -- so it says what a
# caller choosing a mode needs and nothing else. It used to carry ~600 characters
# of design history (why three tools became one) which also named three tool
# names retired in #1257, so every agent was paying tokens to be told about a
# refactor in vocabulary that no longer exists. The history:
#
#   Three tools became one because they differed by a ROUTE, not a concept --
#   "read this run's metrics" is the tool and the grain is an argument. The
#   members are the ONLY modes; `server._METRIC_ROUTES` and its two companion
#   tables are keyed on this type, and a structural test asserts all three
#   agree, because a mode with no table entry is a KeyError at call time
#   rather than a schema rejection.
class MetricMode(StrEnum):
    """Which grain to read: `grouped` (server-side reduction), `coordinates`
    (the axis catalog), `points` (raw), or `series` (several runs and keys at
    once, for comparison)."""

    #: Server-side reduction over coordinate axes and step buckets.
    GROUPED = "grouped"
    #: The coordinate catalog — what axes this run logged anything on. Takes no
    #: key: it enumerates the run, it does not read a metric.
    COORDINATES = "coordinates"
    #: Raw points, losslessly, one bounded keyset page at a time.
    POINTS = "points"
    #: Several runs x several keys in ONE read (`POST /v1/series/query`), the
    #: comparison read. The only grain that is not one run, which is why it
    #: takes `run_ids` + `keys` where the other three take `run_id` + `key`.
    SERIES = "series"


# The wire's `smoothing` Literal on `POST /v1/series/query`, mirrored rather
# than imported (this package does not import the backend). Typed on the tool
# signature so a misspelling is refused before the request is built -- the
# endpoint's own 422 names a field the caller never wrote.
class SeriesSmoothing(StrEnum):
    """`smoothing` on metrics(mode="series"): adds a `smoothed` value per point."""

    EMA = "ema"
    SMA = "sma"
    GAUSSIAN = "gaussian"
    TWEMA = "twema"


# THE ONE TOOL, FIVE LISTINGS. `tree` is what browse always was (projects ->
# experiments -> runs via GET /v1/browse); the other four are flat listings
# behind their own routes, added so an agent can answer "my last N runs", "what
# is running now", "which workspace is this", "what did we write down about X"
# and "what is in Shared" without a tree walk -- the reads the dashboard
# assistant had and this surface lacked. Each mode REFUSES the arguments it does
# not read (`server._BROWSE_MODE_ARGS`), for the reason `MetricMode` does.
class BrowseMode(StrEnum):
    """What browse lists: `tree` (projects/experiments/runs, the default),
    `runs` (flat, newest first), `workspaces`, `notes` (the notes catalog),
    or `files` (Shared, or one workspace's)."""

    TREE = "tree"
    RUNS = "runs"
    WORKSPACES = "workspaces"
    NOTES = "notes"
    FILES = "files"


class ReadmeState(StrEnum):
    """`state` on GET /v1/projects/{id}/readme (the backend's `ReadmeState`)."""

    # Mirrored, not imported. Only SNAPSHOT carries text: LIVE means no
    # installation of the GitHub app covers the repository, so Probe holds no
    # copy and the dashboard fetches it in the browser; NONE means no repository
    # is attached; UNAVAILABLE carries a `reason`. The view says which in words
    # (`service._README_STATE_NOTES`), because an empty `markdown` reads the same
    # for all three.
    SNAPSHOT = "snapshot"
    LIVE = "live"
    NONE = "none"
    UNAVAILABLE = "unavailable"


class ReadmeUnavailableReason(StrEnum):
    """`reason` on an `unavailable` README (the backend's enum, mirrored)."""

    NOT_FOUND_OR_NO_ACCESS = "not_found_or_no_access"
    RATE_LIMITED = "rate_limited"
    UPSTREAM_ERROR = "upstream_error"
    APP_PERMISSION_REQUIRED = "app_permission_required"


class NoteCatalogKind(StrEnum):
    """`kind` on a `GET /v1/notes` row (the backend's `NoteKind`)."""

    # Mirrored, not imported. Every member but two is also an `entity` ref kind
    # spelled the same; TEAM_NOTE is the bare `team-note` ref and SUB_NOTE is
    # `sub_note:<id>` -- the mapping lives in `service._note_row_ref`.
    TEAM_NOTE = "team_note"
    PROJECT = "project"
    EXPERIMENT = "experiment"
    RUN = "run"
    GROUP = "group"
    ARTIFACT = "artifact"
    SUB_NOTE = "sub_note"


class Channel(StrEnum):
    """Which door produced a result (per-result provenance).

    `keyword` went with the client-side fallback for pre-/v1/search backends,
    which the MCP cannot reach — see `source.capabilities()`. A search is
    answered by exactly these two channels now.
    """

    EXACT = "exact"
    SEMANTIC = "semantic"


class MatchMode(StrEnum):
    EXACT = "exact"
    SEMANTIC = "semantic"


class BackendSearchState(StrEnum):
    """`state` in the POST /v1/search response."""

    OK = "ok"
    PARTIAL = "partial"


class EnvelopeState(StrEnum):
    """`completeness.state` in the MCP tool envelope."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    # The query was answered in full and the answer is "nothing satisfies that
    # constraint" -- distinct from COMPLETE-with-empty-rows, and load-bearing on
    # the reuse check: "this artifact exists, no version meets your requirement"
    # must NOT read the same as "no such artifact". The first says pin a new
    # version of the SAME identity; the second licenses a new identity. The tool
    # description has promised this state since the asset registry shipped; it was
    # never actually emitted until artifact:<name> replaced that route.
    NO_MATCH = "no_match"


class Capability(StrEnum):
    """Keys of the capability map in the VERBOSE tool envelope (the compact one
    omits it: the map is static per release): what this backend can do,
    reported for information.

    A key earns its place by describing something the product HAS or could have.
    ``promotion_manifests`` is gone rather than False because promotion tiers were
    deliberately REJECTED (``sdk/client.py``: experiment versions replaced the
    removed run-level promote) — reporting a rejected concept as unavailable
    implies it is coming. ``portable_snapshots`` stays False because it is "not
    yet", not "no": ``sdk/snapshot.py`` captures git/env locally and no backend
    route reads one back.

    A False here must NOT, by itself, make a response partial. ``completeness.missing``
    says what a given response lacks; deriving it from every False flag is what
    pinned every research_context envelope to ``partial`` regardless of what was
    actually returned, which trains agents to ignore the signal entirely.

    Every member here is answered STATICALLY by ``source.capabilities()`` because
    the MCP only ever talks to the hosted backend — see the comment there before
    reintroducing any runtime detection.

    EVERY MEMBER MUST BE RETURNED by ``capabilities()``. ``project_scoped_search``
    sat here unpopulated from the day it was declared, so every reader saw a
    declared capability as absent;
    ``tests/test_mcp.py::test_every_declared_capability_is_reported`` now fails
    if the map and this enum drift apart again.
    """

    STRUCTURED_EXPERIMENTS = "structured_experiments"
    # GET /v1/browse: enumerate structure without a query. Named separately from
    # UNIFIED_SEARCH -- they shipped in different releases, and browse still
    # raises CapabilityUnavailable on its own 404 rather than reporting absence
    # up front.
    STRUCTURED_BROWSE = "structured_browse"
    UNIFIED_SEARCH = "unified_search"
    # Server-side project scoping (research-os #103). The backend applies the
    # scope; `service._echoes_project_scope` degrades honestly and marks
    # `project_scope_unsupported` if a response ever fails to confirm it.
    PROJECT_SCOPED_SEARCH = "project_scoped_search"
    SEMANTIC_SEARCH = "semantic_search"
    KB_DOCUMENTS = "kb_documents"
    PORTABLE_SNAPSHOTS = "portable_snapshots"
    MANAGED_ARTIFACT_UPLOAD = "managed_artifact_upload"
    # Backend provider capability, shared by all POST /v1/web/* routes.
    # MCP exposes only the literature endpoint, but keeps this wire flag:
    # `Settings.web_search_configured` gates the shared Firecrawl key.
    #
    # True here is the DEPLOYMENT's answer, not a promise about the next call:
    # a key can be present and the account still be out of credits. The runtime
    # signal is `MissingMarker.WEB_SEARCH` on the response that failed, which is
    # where a caller can actually act on it.
    WEB_SEARCH = "web_search"


class MissingMarker(StrEnum):
    """`completeness.missing` markers emitted by the read tools."""

    # research_browse — the backend predates GET /v1/browse. Emitted INSTEAD of
    # an empty tree: "nothing exists" and "this server cannot tell you what
    # exists" are opposite claims, and the first would stop an agent looking.
    STRUCTURED_BROWSE = "structured_browse"
    # browse at the lab root could not list the runs filed nowhere yet (daemon
    # v2 floating runs): the backend predates them or the read failed. Emitted
    # INSTEAD of omitting `unfiled`, whose absence means "none".
    UNFILED_RUNS = "unfiled_runs"
    # research_search
    EXACT_SEARCH = "exact_search"
    SEMANTIC_SEARCH = "semantic_search"
    KB_VALUES = "kb_values"
    # The semantic channel ANSWERED, but one of its retrieval channels was
    # dead, so recall is thinner than a healthy run's. Distinct from
    # SEMANTIC_SEARCH, which means the whole channel failed and returned
    # nothing: this one means results came back and are incomplete, which is
    # the more dangerous of the two because it looks like success.
    #
    # From the 2026-08-25 kb incident: a failover left the BM25 index
    # unusable, and for forty minutes every search answered
    # `state: "complete"` while missing every lexical match. The engine knew
    # the whole time. This marker is that fact reaching the agent.
    SEMANTIC_CHANNEL_DEGRADED = "semantic_channel_degraded"
    # The engine ANSWERED, every channel alive, and the answer itself is
    # lower-quality than a healthy run's: the gatherer timed out, its output
    # was truncated, it violated its schema and was repaired, or the harness
    # fell back to the raw pre-fan-out pool. The engine reports this as
    # `degraded` with a `degraded_reason`; research-os forwards both, and this
    # marker is that fact reaching the agent.
    #
    # Distinct from SEMANTIC_CHANNEL_DEGRADED, which is a DEAD retrieval
    # channel (thinner recall, same curation), and from SEMANTIC_SEARCH, which
    # is the channel failing outright. This one is the most dangerous of the
    # three because nothing about the response looks wrong: results arrive,
    # the count is plausible, and the curation behind them is not what a
    # healthy search would have produced. The reason rides the channel block
    # as `degraded_reason` so the agent can tell a loop timeout from a
    # schema repair without another call.
    SEMANTIC_ANSWER_DEGRADED = "semantic_answer_degraded"
    # The BACKEND trimmed the response onto its byte budget (dropped chunks or
    # whole results). Distinct from truncated_by_token_budget, which is this
    # tool's own row budget: one is the server shrinking the payload, the other
    # is us. Either way an absent document is not evidence of absence.
    TRUNCATED_BY_RESPONSE_BUDGET = "truncated_by_response_budget"
    # The search RAN and the corpus answered; every surviving row was then
    # removed by the caller's own self-exclusion. Deliberately NOT one of the
    # degraded markers above, and the distinction is the whole point.
    #
    # "Degraded" invites a retry, because a thinner answer really might improve
    # on the next attempt. This one must not: the search worked, and what it
    # found was the caller's own conversation. Rewording cannot produce a
    # different corpus. From the 2026-08-31 anthrogen incident: 21 searches in
    # 52 minutes, every one reporting success, 13 of 20 delivering nothing
    # usable -- the agent had no way to tell "this is all that exists" from
    # "you asked badly", so it reworded and went again.
    ALL_RESULTS_WERE_OWN_SESSION = "all_results_were_own_session"
    # The backend did not echo `exclusion_applied`, so it predates the field and
    # SILENTLY IGNORED the exclusion: `SearchRequest` permits extra body fields.
    # The results therefore still contain the caller's own session. Said out
    # loud rather than assumed, because an unmarked wrong answer is the failure
    # this whole surface exists to prevent.
    SELF_EXCLUSION_UNSUPPORTED = "self_exclusion_unsupported"
    # The same failure for the caller's own WORK (`X-Probe-Hide-Session-Work`):
    # the backend did not echo `origin_exclusion_applied`, so it ignored the
    # filter and the projects, experiments and runs the caller's session created
    # are still in these results.
    SESSION_WORK_EXCLUSION_UNSUPPORTED = "session_work_exclusion_unsupported"
    # Results the search found and this response could not carry: the budget
    # holds fewer WHOLE cards than were available. A card is never shrunk and
    # never cut in half, so the honest report is "there were more, here is the
    # budget that fits them" -- `fits_all_at_token_budget` on the payload says
    # which number to ask for. There is deliberately no cursor: the semantic
    # channel has no pagination yet, and a cursor built over rows the caller
    # never saw would skip them silently, which is worse than saying so.
    RESULTS_BEYOND_BUDGET = "results_beyond_budget"
    # Even ONE result does not fit the budget asked for. Nothing is truncated to
    # make it fit -- a half card is not a result -- so the response carries the
    # number that would work instead, or points at `entity` when no legal budget
    # would (8,000 is the ceiling).
    FIRST_RESULT_EXCEEDS_BUDGET = "first_result_exceeds_budget"
    # research_get
    TRUNCATED_BY_TOKEN_BUDGET = "truncated_by_token_budget"
    TOKEN_BUDGET_EXCEEDED = "token_budget_exceeded"
    EXECUTION_RECORD = "execution_record"
    EXPERIMENT = "experiment"  # a run whose experiment could not be read
    # A backend `limit` ceiling was reached, so rows past it are unreachable. At the
    # ceiling the lookahead row cannot be fetched (limit == want), so `more_beyond`
    # is False by construction and THIS is the only remaining signal that the agent
    # has not seen everything. Every _bounded consumer must emit its marker.
    SPANS_BEYOND_BACKEND_LIMIT = "spans_beyond_backend_limit"
    METRIC_POINTS_BEYOND_BACKEND_LIMIT = "metric_points_beyond_backend_limit"
    # A trial's trajectory is the ROLLOUT'S SUBTREE, and the spans route filters
    # by direct `parent_span_id` only -- so the subtree is walked locally over a
    # bounded slice of the run's spans. When that slice hit its ceiling, a
    # descendant past it is simply not in the walk, and the subtree is short
    # without looking short. Distinct from SPANS_BEYOND_BACKEND_LIMIT because the
    # remedy differs: there the agent narrows its own window, here the window it
    # would narrow belongs to the CONTAINING RUN, not to the trial it asked about.
    TRIAL_SPANS_BEYOND_RUN_SLICE = "trial_spans_beyond_run_slice"
    # The trial exists (its sidecar row answered) and its rollout SPAN was not in
    # the readable slice. Emitted INSTEAD of an empty span list, for the reason
    # STRUCTURED_BROWSE exists: "this trial recorded no spans" and "this server
    # could not reach them" are opposite claims, and only the first stops an
    # agent looking. 0135 made the sidecar outlive the bounded span slice on
    # purpose -- this marker is where that shows up on the read side.
    TRIAL_ROLLOUT_SPAN_UNREAD = "trial_rollout_span_unread"
    # The run has more trials than this server will walk in one view. Its OWN
    # bound, not the backend's: `GET /v1/runs/{id}/trials` pages with a real
    # keyset cursor and would keep going. Distinct from ROWS_BEYOND_PAGE_BOUND,
    # whose contract says the rest is reachable by passing `next_cursor` back as
    # `step_from`/`after_id` -- those are metric arguments this view does not
    # take, so reusing it would name a resume affordance that does not exist
    # here. Narrow the question instead: a run with thousands of rollouts is one
    # to ask about by step, not to enumerate.
    TRIALS_BEYOND_WALK_BOUND = "trials_beyond_walk_bound"
    # GET /v1/runs/{ref}/bundle caps its artifact list at 200 server-side while
    # `artifact_total` reports the true count, and there is no offset to page it.
    # So handoff cannot show the rest: it says so, and view="artifacts" (which reads
    # the uncapped route) is where the full list lives.
    ARTIFACTS_BEYOND_BUNDLE_LIMIT = "artifacts_beyond_bundle_limit"
    # A `sessions` view (run or artifact) whose server list is capped at 50
    # while `session_total` counts them all, on routes with no offset: the rest
    # are not reachable here, and the exact total rides the payload.
    SESSIONS_BEYOND_SERVER_LIMIT = "sessions_beyond_server_limit"
    # browse(mode="files"): the Shared and workspace file routes take no cursor
    # and serve at most 1,000 rows per read, so a folder past that is not
    # reachable by paging. Narrow with `prefix`.
    FILES_BEYOND_BACKEND_LIMIT = "files_beyond_backend_limit"
    # browse(mode="runs"/"notes") under `X-Probe-Hide-Session-Work`: every row
    # the backend pages this read covered was the caller's own session's work and
    # was left out, up to the read's own bound. NOT "nothing exists": the empty
    # page says nothing about what lies past `next_cursor`, which continues.
    PAGE_HIDDEN_AS_OWN_SESSION_WORK = "page_hidden_as_own_session_work"
    # metrics(mode="series"): the backend answered, and some series could not be
    # read (a provider-backed run's source failed). Those failures are listed in
    # `data.errors`; the series that DID read are complete as far as they go.
    SERIES_READ_ERRORS = "series_read_errors"
    # lineage on a project or experiment: the read stopped at a window, and the
    # payload's `*_truncated` flags say which -- its children past the route's
    # limit, its links past the view's cap, links among its runs past that cap,
    # or "built on" derived over only its newest runs. Neither route takes an
    # offset, so the rest is not reachable here; `probe experiment edges` lists
    # the whole graph among an experiment's runs and files.
    LINEAGE_BEYOND_WINDOW = "lineage_beyond_window"
    # get_metrics_grouped / export_metric_points — the read was cut at the tool's
    # own row bound. Unlike the *_beyond_backend_limit markers the rest IS
    # reachable: `next_cursor` carries the resume position (pass it back as
    # `step_from` for grouped, `after_id` for export).
    ROWS_BEYOND_PAGE_BOUND = "rows_beyond_page_bound"
    # -- find_papers ---------------------------------------------------------
    # The open-web door did not answer. TWO CAUSES SHARE THIS MARKER, and that
    # is a limit of the wire rather than a decision: `app/websearch/router.py`
    # returns 503 both when the deployment has no Firecrawl key and when the
    # provider is over quota or rate limited, and the two are told apart only by
    # the sentence in the body. So the marker says "no answer from the web" and
    # `data.reason` carries the BACKEND's own sentence, which is the half that
    # differs -- one ends "is unset", the other "try later". Read the sentence
    # before deciding whether to try again; matching on it in code here would be
    # a string coupling that breaks the first time somebody rewords a 503.
    WEB_SEARCH = "web_search"


# -- research literature: POST /v1/web/papers vocabulary ----------------------
#
# Mirrored from app/websearch/schemas.py rather than imported, like every other
# vocabulary in this file: the agent package does not import the backend, and
# these are wire strings.
#
# THEIR DOCSTRINGS ARE AGENT-FACING SURFACE, not developer notes. FastMCP builds
# each tool's JSON schema from its annotations, so an enum used on a signature
# ships its `__doc__` verbatim into `tools/list`, loaded whole by every session
# that pulls these tools. Rationale therefore lives in comments like this one, and the
# docstrings say only what a caller choosing a value needs. (`MetricMode` above
# predates that realisation and ships ~900 characters of design history to every
# agent; do not copy it.)


class PaperMode(StrEnum):
    """`mode` on find_papers: which literature question is being asked."""

    # One tool, three modes, for the same reason `read_metrics` has three
    # grains: they are one noun read three ways. The BACKEND refuses arguments
    # the chosen mode cannot read (a `paper_id` with `mode="search"` is a 422),
    # so that table is not repeated here -- two copies would drift, and the
    # endpoint's is the one that decides.
    SEARCH = "search"
    READ = "read"
    SIMILAR = "similar"


class PaperExpansion(StrEnum):
    """`expand` on find_papers(mode="similar"): which direction to walk."""

    SIMILAR = "similar"
    CITERS = "citers"
    REFERENCES = "references"


class WebState(StrEnum):
    """`state` in a POST /v1/web/* response body."""

    # `empty` is an ANSWER -- the provider ran the query and nothing matched --
    # and the service turns it into `completeness.state="no_match"`. A model
    # told only that its call failed rephrases and retries for as many steps as
    # it has left. Not used on any tool signature, so this docstring costs
    # nothing in a schema; it is kept short for consistency with its neighbours.
    OK = "ok"
    EMPTY = "empty"


class ChannelError(StrEnum):
    """Client-side per-channel error markers (backend errors pass through as-is)."""

    MALFORMED_RESPONSE = "malformed_response"
    PROJECT_SCOPE_UNSUPPORTED = "project_scope_unsupported"
