"""Shared /v1/search + MCP-envelope vocabulary (CONTRACT.md, workspaces+kb fold-in).

Enum-style constants so ``service.py`` and ``source.py`` cannot drift on the wire
strings. ``StrEnum`` members are plain ``str`` at runtime, so they serialize and
compare exactly like the literals they replace.
"""

from __future__ import annotations

from probe.foundation.compat.compat import StrEnum

# THE SHARED VOCABULARY, generated from research-os `contracts/probe_contracts/agent_surface/agent_surface.py`,
# not declared here. This MCP and the dashboard assistant answer the same question about the same
# record: with different WORDS a researcher learns nothing from one about the other and a fix to one
# silently diverges (a lineage fix here, returning ancestry AND edges, was re-broken by an
# independently-written second matrix). Re-exported under the name this module always used, so every
# `View.X` keeps working.
# THE DOCSTRING IS DELIBERATELY SHORT: an enum on a tool signature ships its whole `__doc__` into every
# session loading the tools, so rationale lives in comments like this one.
# Refresh with `make gen-views` (or `make regen`) against a research-os checkout. Coverage may differ
# (this server has no saved-metric-view route; the assistant has no `metrics` view) but SPELLING may
# not, and `_VIEWS` is checked against this matrix. The import is at the bottom of the file.


class BackendCorpus(StrEnum):
    """`corpus` values accepted by POST /v1/search."""

    EXPERIMENTS = "experiments"
    FILES = "files"
    GITHUB = "github"
    TRANSCRIPTS = "transcripts"
    # The team note (research-os 0125). ADDITIVE: an older backend does not know the value; the request is otherwise unchanged.
    NOTES = "notes"
    # Session digests (research-os 0105). Reachable from POST /v1/search since it shipped but never
    # added HERE, so `search_in` could not scope to it (the "SDK-regen tail" in CONTRACT.md); paid off
    # with the notes rider.
    DIGESTS = "digests"
    # Papers (research-os 0170), the THIRD time this tail was paid: the corpus shipped with
    # `index_paper_customers` and never reached this enum. ADDITIVE. The one corpus the backend cannot
    # separate by source_key (papers sit under the EXPERIMENTS key, told apart by document-id prefix
    # after retrieval): /v1/search's business, a plain corpus value from here.
    PAPERS = "papers"


# THIS DOCSTRING IS THE MAPPING TABLE'S ONLY AGENT-FACING HOME, not `search`'s docstring: a client
# caps a tool `description` (Claude Code slices MCP descriptions at 2,048 chars) but passes
# `input_schema` verbatim. The table sat ~1,150 chars deep in the tool docstring and was cut in half
# unread. tests/test_mcp_schema_docs.py parses the arrows out of THIS string and checks them against
# `_SEARCH_IN_TO_BACKEND`. The parameter was `corpora` until renamed: the plural read as `corpus` + s
# and the identity mappings confirmed the misreading.
class ToolCorpus(StrEnum):
    """``search``'s `search_in` vocabulary. NOT the backend's `corpus`
    values. What each one covers:

      transcripts -> transcripts
      projects -> experiments
      files -> files
      github -> github
      notes -> notes + experiments
      digests -> digests
      papers -> papers
      docs -> Probe's own docs, not the team's record

    `projects` is the projects, experiments and runs themselves. `files` is
    workspace files (scripts, datasets, configs, protocols -- the index does
    not separate those); `github` is indexed GitHub docs. `notes` spans two
    backend corpora on purpose: the team's shared note and the notes hanging
    off projects, experiments and runs. A hit on an entity's note comes back
    AS that entity, so you can open it."""

    # One value, not the former assets/procedures pair: both mapped to one backend corpus (the index has a
    # single IndexDocType.WORKSPACE_FILE bucket), so narrowing to one never excluded the other.
    FILES = "files"
    #: Indexed GitHub docs alone. The older `documents` (github + files) stays accepted: `TOOL_CORPUS_LEGACY`.
    GITHUB = "github"
    TRANSCRIPTS = "transcripts"
    #: The backend's `experiments` corpus (project, experiment and run projections), named for what callers
    #: reach for; the older `experiments` stays accepted (`TOOL_CORPUS_LEGACY`).
    PROJECTS = "projects"
    #: The team's shared note and every entity's notes (0125): ONE value over two backend corpora, since
    #: "search what the team wrote down" is one question (entity notes ride their entity's document in
    #: `experiments`, the team note is its own `notes` corpus). Splitting makes a caller pick a KIND first.
    NOTES = "notes"
    #: Session digests (0105): the lane that wrote them retired in 0204 and the corpus is draining. The
    #: value stays legal so an older client's request is not a 422; expect nothing under it.
    DIGESTS = "digests"
    #: The papers a project was built from (0170). ITS OWN VALUE, not folded into `files` or `notes`:
    #: a paper is what the FIELD published, and both existing multi-corpus values fold together things
    #: answering ONE question ("what has been written about X" differs from "what did we decide about X").
    PAPERS = "papers"
    #: Probe's OWN documentation (docs.prbe.ai), read from `GET /public/v1/docs`, not POST /v1/search: not
    #: the team's record, no backend corpus, never searched unless named (`is_docs_only`, `service.NON_BACKEND_CORPORA`).
    DOCS = "docs"


# -- legacy spellings ---------------------------------------------------------
# Values a tool accepted before its vocabulary moved to the words models reach for (reader-tool-fit
# 1B, 2026-11-11). Each maps to one OR MORE current members and is accepted forever, but named in no
# schema, description or skill (enum `__doc__`s ship in schemas, so they live here, as comments).
# `get_current_values` applies them; the MCP server runs it before pydantic checks the enum.

#: `search_in`: `experiments` was the backend corpus's own name; `documents` meant github + files.
TOOL_CORPUS_LEGACY: dict[str, tuple[ToolCorpus, ...]] = {
    "experiments": (ToolCorpus.PROJECTS,),
    "documents": (ToolCorpus.GITHUB, ToolCorpus.FILES),
}


def get_current_values(value: object, legacy: dict) -> object:
    """`value` with each legacy spelling in `legacy` replaced by its current member(s). A list is
    flattened in order without repeats; a single value must map to exactly one member. Anything else
    passes through untouched, for the type check to judge."""
    if isinstance(value, list):
        out: list = []
        for item in value:
            for current in legacy.get(item, (item,)) if _is_key(item) else (item,):
                if current not in out:
                    out.append(current)
        return out
    if _is_key(value) and value in legacy:
        (current,) = legacy[value]
        return current
    return value


def _is_key(value: object) -> bool:
    return value is None or isinstance(value, str)


def is_docs_only(search_in: list[str] | None) -> bool:
    """Does this `search_in` name Probe's docs and nothing else?

    The one test of "docs only", shared by the MCP service (which then answers
    from the docs route and never runs the team search) and the daemon's audit
    (where a read of Probe's docs is not a look at the team's record). Omitted
    or empty means EVERY team corpus, never the docs."""
    return bool(search_in) and all(value == ToolCorpus.DOCS for value in search_in)


class DocsState(StrEnum):
    """`state` in a `GET /public/v1/docs` response body (mirrored from the route)."""

    OK = "ok"
    # The last good copy, served while docs.prbe.ai cannot be read.
    STALE = "stale"
    # No copy yet: `sections` is empty.
    UNAVAILABLE = "unavailable"


#: The longest `query` the docs route accepts (422 past it, and for an empty one). Checked here first so
#: a docs search says what to fix instead of reading as "the docs could not be read".
DOCS_QUERY_MAX_CHARS = 512


class EntityType(StrEnum):
    """Entity types across exact hits, semantic refs, and tool results."""

    PROJECT = "project"
    EXPERIMENT = "experiment"
    # Reached by NAME (`artifact:<name>`): the reuse check asks "does an official X exist" and you have the
    # name, not an id, and no `GET /v1/artifacts/{id}` route exists. Absorbed the retired `asset` member
    # (#143 folded assets into artifacts keeping their id).
    ARTIFACT = "artifact"
    RUN = "run"
    # One rollout as an entity (research-os 0135), as `trial:<rollout span id>`, the id the dashboard's
    # `/runs/{id}/trials/{rolloutSpanId}` URL carries. NOT a `rollout` SPAN: the span is what the producer
    # emitted, the Trial the authored sidecar holding the title, description and note; reading spans
    # never finds it.
    TRIAL = "trial"
    GROUP = "group"  # a sweep/ensemble: an experiment-shaped noun, reached by ref
    FILE = "file"
    DOCUMENT = "document"  # a semantic hit whose ref is null
    # The TEAM NOTE (research-os 0125). A SINGLETON, the only member whose ref carries no value:
    # `ref="team-note"`, never `team-note:<id>` (one per tenant, the credential names the tenant, and an
    # id would imply a second and need a 404 for an id nobody can construct).
    TEAM_NOTE = "team-note"
    # A captured coding-agent session: `session:<id>` (the id a project/experiment/run card's `sessions`
    # field carries) or `session:<agent>/<id>` when the recording agent is known. Before, its transcript
    # was searchable and renderable (dashboard) but not readable here.
    SESSION = "session"
    # One titled SUB-NOTE (0146) by its own UUID, `sub_note:<id>` (the id a `notes` view row carries); its
    # card IS the document. Before, `view="notes"` showed a 700-char excerpt and pointed at the dashboard.
    SUB_NOTE = "sub_note"
    # The data catalog (C3/C4), by PREFIX only, never a bare id: `dataset:<name>[@<N>|@latest]` /
    # `dataset:<uuid>`, `source:<uuid>` / `source:<canonical_key>[@<revision>]`, `checkpoint:<uuid>` /
    # `checkpoint:<run ref>@best[:<callback>]|latest|step<N>`. The server resolves every form
    # (`app/catalog/refs.py`); this side routes. `artifact:<name>` is NOT one: it stays the Shared reuse
    # check, which still sees a catalog dataset (a Shared row).
    DATASET = "dataset"
    SOURCE = "source"
    CHECKPOINT = "checkpoint"


# Its OWN type rather than a reuse of `EntityType.EXPERIMENT`: those strings coincide, but "dedupe by
# experiment" and "this row IS an experiment" are different ideas, and typing the parameter as EntityType
# would advertise `project`/`run`/`artifact` as collapse modes that do not exist.
class CollapseMode(StrEnum):
    """``search(collapse=...)``: `experiment` keeps one row per experiment, `none` keeps every hit."""

    EXPERIMENT = "experiment"
    #: No dedupe. Was spelled JSON `null` (still accepted: `COLLAPSE_MODE_LEGACY`).
    NONE = "none"


#: `collapse`: an explicit JSON null meant "no dedupe" before `none` existed.
COLLAPSE_MODE_LEGACY: dict[str | None, tuple[CollapseMode, ...]] = {None: (CollapseMode.NONE,)}


# THIS DOCSTRING SHIPS TO EVERY SESSION, uncapped, in `$defs`: it says only what a caller choosing a mode
# needs (it once carried ~600 chars of design history naming three tools retired in #1257).
# History: three tools became one because they differed by a ROUTE, not a concept ("read this run's
# metrics" is the tool, the grain an argument). The members are the ONLY modes; `server._METRIC_ROUTES`
# and its two companion tables are keyed on this type and a structural test asserts all three agree,
# since a mode with no table entry is a KeyError at call time, not a schema rejection.
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
    #: Several runs x several keys in ONE read (`POST /v1/series/query`), the comparison read. The only
    #: grain that is not one run, so it takes `run_ids` + `keys` where the others take `run_id` + `key`.
    SERIES = "series"


# The wire's `smoothing` Literal on `POST /v1/series/query`, mirrored not imported (this package never
# imports the backend). Typed on the tool signature so a misspelling is refused before the request is
# built (the endpoint's 422 names a field the caller never wrote).
class SeriesSmoothing(StrEnum):
    """`smoothing` on metrics(mode="series"): adds a `smoothed` value per point."""

    EMA = "ema"
    SMA = "sma"
    GAUSSIAN = "gaussian"
    TWEMA = "twema"


# THE ONE TOOL, FIVE LISTINGS. `projects` is what browse always was (projects -> experiments -> runs via
# GET /v1/browse; spelled `tree` until 2026-11-11, still accepted: `BROWSE_MODE_LEGACY`); the other four are
# flat listings behind their own routes ("my last N runs", "what is running now", "which workspace is
# this", "what did we write down about X", "what is in Shared") that the dashboard assistant had and this
# surface lacked. Each mode REFUSES the arguments it does not read (`server._BROWSE_MODE_ARGS`), as
# `MetricMode` does. The data catalog (C4) added three more over `/v1/catalog/*`: team datasets, every
# checkpoint team-wide, external sources.
class BrowseMode(StrEnum):
    """What browse lists: `projects` (projects/experiments/runs, the default),
    `runs` (flat, newest first), `workspaces`, `notes` (the notes catalog),
    `files` (Shared, or one workspace's), the data catalog's `datasets`,
    `checkpoints` and `sources`, a workspace's `branches`, the team's
    `people` (with user ids), or agent `sessions` (newest first)."""

    PROJECTS = "projects"
    RUNS = "runs"
    WORKSPACES = "workspaces"
    NOTES = "notes"
    FILES = "files"
    DATASETS = "datasets"
    CHECKPOINTS = "checkpoints"
    SOURCES = "sources"
    #: A workspace's lines of work across its projects, ranked per metric
    #: (`GET /v1/workspaces/{W}/branches`; swarm visibility D6, A23).
    BRANCHES = "branches"
    #: The team's members with their user ids (`GET /v1/people`; people and time filters, D13).
    PEOPLE = "people"
    #: Agent sessions team-wide, newest activity first (`GET /v1/sessions`; B1).
    SESSIONS = "sessions"


#: The browse modes that list work people made, so take `owner`, `since`, `until` and `order="recent"`
#: (people and time filters B2, AR5). Not workspaces, sources or branches: containers and connections.
#: Must equal the server's owner-capable routes; tests/mcp/tools/reads/test_people_filters.py checks it
#: against the schema snapshot.
OWNER_MODES: frozenset[BrowseMode] = frozenset(
    {
        BrowseMode.PROJECTS,
        BrowseMode.RUNS,
        BrowseMode.NOTES,
        BrowseMode.FILES,
        BrowseMode.DATASETS,
        BrowseMode.CHECKPOINTS,
        BrowseMode.SESSIONS,
    }
)


# `order="recent"` on browse: newest activity first (D16). A plain value, not an enum on the signature:
# browse's `order` is also mode=runs' free sort string (`-metric.acc`).
class BrowseOrder(StrEnum):
    """`order` values every authored browse mode reads."""

    RECENT = "recent"


class SearchSort(StrEnum):
    """`relevance` (default): best match first. `recent`: newest first."""

    RELEVANCE = "relevance"
    RECENT = "recent"


#: `mode`: the projects -> experiments -> runs walk was `tree`.
BROWSE_MODE_LEGACY: dict[str, tuple[BrowseMode, ...]] = {"tree": (BrowseMode.PROJECTS,)}

#: Every enum with legacy spellings, and its map (tests walk this).
LEGACY_VALUES: dict[type, dict] = {
    BrowseMode: BROWSE_MODE_LEGACY,
    ToolCorpus: TOOL_CORPUS_LEGACY,
    CollapseMode: COLLAPSE_MODE_LEGACY,
}


# -- the data catalog's closed vocabularies, as this server sends them ---------
# Mirrored, not imported (this package never imports `app/`), and held value-for-value to the server's
# enums by tests/test_mcp_catalog.py: `Direction` (app/catalog/provenance.py), `Registered` and
# `StoredState` (app/catalog/router.py), `SourceKind` and `SourceProvider` (app/core/catalog_vocab.py).
# The browse ones type browse's arguments, so a typo is refused before a request is built.
# DOCSTRINGS ONE LINE: an enum on a tool signature ships its `__doc__` into every session's schema.
class ProvenanceDirection(StrEnum):
    """Up to the sources, or down to what used it."""

    UPSTREAM = "upstream"
    DOWNSTREAM = "downstream"


class DatasetRegistered(StrEnum):
    """Named team datasets (yes), unregistered run-logged dataset files (no), or both."""

    ALL = "all"
    YES = "yes"
    NO = "no"


class CheckpointStored(StrEnum):
    """Bytes Probe holds (stored), or a location it points at (reference)."""

    STORED = "stored"
    REFERENCE = "reference"


class SourceKind(StrEnum):
    """What an external source is."""

    DATASET = "dataset"
    MODEL = "model"
    OTHER = "other"


class SourceProvider(StrEnum):
    """Where an external source lives."""

    HUGGINGFACE = "huggingface"
    S3 = "s3"
    GCS = "gcs"
    AZURE = "azure"
    HTTP = "http"
    GIT = "git"
    DATABASE = "database"
    LOCAL = "local"
    OTHER = "other"


class ReadmeState(StrEnum):
    """`state` on GET /v1/projects/{id}/readme (the backend's `ReadmeState`)."""

    # Mirrored, not imported. Only SNAPSHOT carries text: LIVE = no GitHub-app installation covers the
    # repository (Probe holds no copy, the dashboard fetches it in the browser); NONE = no repository
    # attached; UNAVAILABLE carries a `reason`. The view says which in words (`service._README_STATE_NOTES`),
    # because an empty `markdown` reads the same for all three.
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
    SUB_NOTE = "sub_note"


class Channel(StrEnum):
    """Which door produced a result (per-result provenance).

    `keyword` is back with a different meaning: the old client-side fallback
    for pre-/v1/search backends is gone (the MCP cannot reach one), and
    `search(semantic=false)` labels its content hits `keyword` -- BM25 over
    document text, no model -- so an agent never reads them as semantic matches.
    """

    EXACT = "exact"
    SEMANTIC = "semantic"
    KEYWORD = "keyword"


class MatchMode(StrEnum):
    EXACT = "exact"
    SEMANTIC = "semantic"
    KEYWORD = "keyword"


class BackendRetrieval(StrEnum):
    """`retrieval` on POST /v1/search (and its echo `semantic.retrieval`)."""

    KEYWORD = "keyword"


class BackendSearchState(StrEnum):
    """`state` in the POST /v1/search response."""

    OK = "ok"
    PARTIAL = "partial"


class EnvelopeState(StrEnum):
    """`completeness.state` in the MCP tool envelope."""

    COMPLETE = "complete"
    PARTIAL = "partial"
    # Answered in full and the answer is "nothing satisfies that constraint": distinct from COMPLETE-with-
    # empty-rows and load-bearing on the reuse check: "this artifact exists, no version meets your
    # requirement" (pin a new version of the SAME identity) must NOT read as "no such artifact" (licenses a
    # new identity). Promised by the tool description since the asset registry; emitted only once
    # artifact:<name> replaced that route.
    NO_MATCH = "no_match"


class Capability(StrEnum):
    """Keys of the capability map in the VERBOSE tool envelope (the compact one
    omits it: the map is static per release): what this backend can do,
    reported for information.

    A key earns its place by describing something the product HAS or could have.
    ``promotion_manifests`` is gone rather than False because promotion tiers were
    deliberately REJECTED (``sdk/client/client.py``: experiment versions replaced the
    removed run-level promote) — reporting a rejected concept as unavailable
    implies it is coming. ``portable_snapshots`` stays False because it is "not
    yet", not "no": ``sdk/capture/code/code.py`` captures git/env locally and no backend
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
    # GET /v1/browse: enumerate structure without a query. Separate from UNIFIED_SEARCH (different
    # releases); browse still raises CapabilityUnavailable on its own 404 rather than reporting absence up front.
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
    # Backend provider capability, shared by all POST /v1/web/* routes. MCP exposes only the literature
    # endpoint but keeps the wire flag: `Settings.web_search_configured` gates the shared Firecrawl key.
    # True is the DEPLOYMENT's answer, not a promise about the next call (a key can exist on an account out
    # of credits); the runtime signal is `MissingMarker.WEB_SEARCH` on the failed response.
    WEB_SEARCH = "web_search"


class MissingMarker(StrEnum):
    """`completeness.missing` markers emitted by the read tools."""

    # research_browse: the backend predates GET /v1/browse. Emitted INSTEAD of an empty tree ("nothing
    # exists" vs "this server cannot tell you" are opposite claims; the first stops an agent looking).
    STRUCTURED_BROWSE = "structured_browse"
    # research_search
    EXACT_SEARCH = "exact_search"
    SEMANTIC_SEARCH = "semantic_search"
    KB_VALUES = "kb_values"
    # `search_in` named `docs` and Probe's docs could not be read (route `unavailable` or failed), or, in a
    # mixed search, were not searched because the query is outside 1..512 chars (docs alone answers 422):
    # no docs hits, and `note` / `docs_note` says so. A mixed search's team results are unaffected.
    DOCS = "docs"
    # The semantic channel ANSWERED but one of its retrieval channels was dead: thinner recall. Distinct
    # from SEMANTIC_SEARCH (whole channel failed, nothing returned); this one is more dangerous because
    # it looks like success. 2026-08-25 kb incident: a failover left the BM25 index unusable and for forty
    # minutes every search said `state: "complete"` while missing every lexical match. The engine knew;
    # this marker is that fact reaching the agent.
    SEMANTIC_CHANNEL_DEGRADED = "semantic_channel_degraded"
    # The engine ANSWERED, every channel alive, but the answer is lower-quality than healthy: the
    # gatherer timed out, its output was truncated, it violated its schema and was repaired, or the
    # harness fell back to the raw pre-fan-out pool. The engine reports `degraded` + `degraded_reason`;
    # research-os forwards both. Distinct from SEMANTIC_CHANNEL_DEGRADED (a DEAD channel: thinner recall,
    # same curation) and SEMANTIC_SEARCH (channel failed outright). Most dangerous of the three: results
    # arrive, the count is plausible, the curation is not healthy's. The reason rides the channel block as
    # `degraded_reason` so the agent can tell a loop timeout from a schema repair without another call.
    SEMANTIC_ANSWER_DEGRADED = "semantic_answer_degraded"
    # The BACKEND trimmed the response onto its byte budget (dropped chunks or whole results). Distinct from
    # truncated_by_token_budget (this tool's own row budget). Either way absence is not evidence of absence.
    TRUNCATED_BY_RESPONSE_BUDGET = "truncated_by_response_budget"
    # The search RAN and the corpus answered; every surviving row was removed by the caller's own
    # self-exclusion. Deliberately NOT a degraded marker: "degraded" invites a retry, and this one must not
    # get one (the search worked, it found the caller's own conversation, rewording cannot yield another
    # corpus). 2026-08-31 anthrogen incident: 21 searches in 52 min all reporting success, 13 of 20
    # delivering nothing usable; the agent could not tell "all that exists" from "you asked badly".
    ALL_RESULTS_WERE_OWN_SESSION = "all_results_were_own_session"
    # The backend did not echo `exclusion_applied`: it predates the field and SILENTLY IGNORED the
    # exclusion (`SearchRequest` permits extra body fields), so results still contain the caller's own
    # session. Said out loud: an unmarked wrong answer is the failure this surface exists to prevent.
    SELF_EXCLUSION_UNSUPPORTED = "self_exclusion_unsupported"
    # The same for the caller's own WORK (`X-Probe-Hide-Session-Work`): no `origin_exclusion_applied` echo, so
    # the filter was ignored and the projects, experiments and runs its session created are still here.
    SESSION_WORK_EXCLUSION_UNSUPPORTED = "session_work_exclusion_unsupported"
    # `search(semantic=false)` asked for keyword and the backend did not echo `semantic.retrieval:
    # "keyword"`: it predates the field and ran the full semantic search; the hits are labelled semantic.
    KEYWORD_SEARCH_UNSUPPORTED = "keyword_search_unsupported"
    # A keyword search matched more than it returned (candidate cap hit, or more ranked than kept). Absence
    # is NOT evidence of absence: raise `top_k`, add a rarer word, or narrow with `search_in` / `project_id`.
    KEYWORD_MATCHES_BEYOND_BACKEND_LIMIT = "keyword_matches_beyond_backend_limit"
    # Results found that this response could not carry: the budget holds fewer WHOLE cards than were
    # available (a card is never shrunk or cut), so the report is "there were more, here is the budget that
    # fits" (`fits_all_at_token_budget` on the payload). Deliberately no cursor: the semantic channel has
    # no pagination yet and a cursor over unseen rows would skip them silently.
    RESULTS_BEYOND_BUDGET = "results_beyond_budget"
    # Even ONE result does not fit the budget asked for. Nothing is truncated (a half card is not a result):
    # the response carries the number that would work, or points at `entity` when none would (8,000 is the ceiling).
    FIRST_RESULT_EXCEEDS_BUDGET = "first_result_exceeds_budget"
    # research_get
    TRUNCATED_BY_TOKEN_BUDGET = "truncated_by_token_budget"
    TOKEN_BUDGET_EXCEEDED = "token_budget_exceeded"
    EXECUTION_RECORD = "execution_record"
    EXPERIMENT = "experiment"  # a run whose experiment could not be read
    # A backend `limit` ceiling was reached, so rows past it are unreachable. At the ceiling the lookahead
    # row cannot be fetched (limit == want), so `more_beyond` is False by construction and THIS is the only
    # signal the agent has not seen everything. Every _bounded consumer must emit its marker.
    SPANS_BEYOND_BACKEND_LIMIT = "spans_beyond_backend_limit"
    METRIC_POINTS_BEYOND_BACKEND_LIMIT = "metric_points_beyond_backend_limit"
    # A trial's trajectory is the ROLLOUT'S SUBTREE, and the spans route filters by direct
    # `parent_span_id` only, so the subtree is walked locally over a bounded slice of the run's spans. If
    # that slice hit its ceiling a descendant past it is missing and the subtree is short without looking
    # short. Distinct from SPANS_BEYOND_BACKEND_LIMIT: the window to narrow belongs to the CONTAINING RUN.
    TRIAL_SPANS_BEYOND_RUN_SLICE = "trial_spans_beyond_run_slice"
    # The trial exists (its sidecar row answered) but its rollout SPAN was not in the readable slice.
    # Emitted INSTEAD of an empty span list, as with STRUCTURED_BROWSE: "recorded no spans" and "could not
    # reach them" are opposite claims. 0135 made the sidecar outlive the bounded span slice on purpose.
    TRIAL_ROLLOUT_SPAN_UNREAD = "trial_rollout_span_unread"
    # The run has more trials than this server walks in one view: its OWN bound, not the backend's
    # (`GET /v1/runs/{id}/trials` pages with a real keyset cursor). Distinct from ROWS_BEYOND_PAGE_BOUND,
    # whose contract says the rest is reachable via `next_cursor` as `step_from`/`after_id`, metric
    # arguments this view does not take. Narrow the question instead: ask a thousands-of-rollouts run by step.
    TRIALS_BEYOND_WALK_BOUND = "trials_beyond_walk_bound"
    # entity(run, view="commands"): the run had more commands than the view walks (`_COMMAND_BACKEND_MAX`); the
    # rest are `probe run commands RUN --after <seq>`.
    COMMANDS_BEYOND_WALK_BOUND = "commands_beyond_walk_bound"
    # GET /v1/runs/{ref}/bundle caps its artifact list at 200 server-side (`artifact_total` is the true
    # count; no offset), so handoff cannot show the rest: view="artifacts" (uncapped route) has the full list.
    ARTIFACTS_BEYOND_BUNDLE_LIMIT = "artifacts_beyond_bundle_limit"
    # A `sessions` view (run or artifact) capped server-side at 50 (`session_total` counts them all), on routes
    # with no offset: the rest is unreachable here and the exact total rides the payload.
    SESSIONS_BEYOND_SERVER_LIMIT = "sessions_beyond_server_limit"
    # browse(mode="files"): the Shared and workspace file routes take no cursor and serve at most 1,000 rows
    # per read; past that, narrow with `prefix`.
    FILES_BEYOND_BACKEND_LIMIT = "files_beyond_backend_limit"
    # entity(checkpoint, view="versions"): the read carries one page of the run's other saves
    # (`saves_next_cursor`); the rest is browse(mode="checkpoints", run=...), which pages (the payload names it).
    SAVES_BEYOND_SERVER_PAGE = "saves_beyond_server_page"
    # browse(mode="runs"/"notes"/"datasets"/"checkpoints") under `X-Probe-Hide-Session-Work`: every row the
    # backend pages this read covered was the caller's own session's work and was left out, up to the
    # read's bound. NOT "nothing exists": the empty page says nothing about what lies past `next_cursor`.
    PAGE_HIDDEN_AS_OWN_SESSION_WORK = "page_hidden_as_own_session_work"
    # browse(mode="runs"): `GET /v1/runs/counts` did not answer (an older API, or the count ran past its
    # bound), so the page carries no `totals`. The page is still right; how many there are in all is unknown.
    TOTALS_UNAVAILABLE = "totals_unavailable"
    # entity on a failed/crashed run: `GET /v1/runs/failures` did not answer, so the card has no `failure`
    # block. Not "no cause": the reason was not read.
    FAILURE_UNAVAILABLE = "failure_unavailable"
    # metrics(mode="series"): the backend answered but some series could not be read (a provider-backed
    # run's source failed); they are listed in `data.errors`, the series that DID read are complete.
    SERIES_READ_ERRORS = "series_read_errors"
    # lineage on a project or experiment: the SERVER's read stopped at a window, and the payload's
    # `*_truncated` flags say which: children past the route's limit, stored links past 500, links among
    # runs past the edges route's 1,000, or "built on" derived over only the newest runs. No offset exists;
    # `probe experiment edges` lists the whole graph among an experiment's runs and files.
    LINEAGE_BEYOND_WINDOW = "lineage_beyond_window"
    # lineage on a project or experiment (swarm friction P6): a link list on this page (`built_on`,
    # `used_by`, `run_edges`) is a glance cut to the budget; `total` counts all and `read_more` names the
    # `view_options.links` that pages the whole list. Nothing is out of reach.
    LINKS_BEYOND_PAGE = "links_beyond_page"
    # picks on a project, or `pick_history` on browse(mode="branches"): the best route reads at most 50
    # events (`MAX_PICK_HISTORY`) with no offset, so older events are unreachable here.
    PICKS_BEYOND_SERVER_LIMIT = "picks_beyond_server_limit"
    # browse(mode="branches"): the workspace's pick history could not be read (best route failed). Emitted
    # INSTEAD of omitting `pick_history` (absence means "no events") unless `pick_history_total` rides the page.
    PICK_HISTORY = "pick_history"
    # browse(mode="branches"): the first page shows only the newest pick events fitting its budget share
    # (`pick_history_total` counts all read). A larger token_budget shows more; later pages carry none.
    PICK_HISTORY_BEYOND_PAGE = "pick_history_beyond_page"
    # get_metrics_grouped / export_metric_points: cut at the tool's own row bound. Unlike the
    # *_beyond_backend_limit markers the rest IS reachable: `next_cursor` is the resume position
    # (`step_from` for grouped, `after_id` for export).
    ROWS_BEYOND_PAGE_BOUND = "rows_beyond_page_bound"
    # -- find_papers ---------------------------------------------------------
    # The open-web door did not answer. TWO CAUSES SHARE THIS MARKER (a wire limit): `app/websearch/router.py`
    # returns 503 both for a deployment with no Firecrawl key and for a provider over quota or rate limited,
    # told apart only by the body sentence. So the marker says "no answer from the web" and `data.reason`
    # carries the BACKEND's sentence ("is unset" vs "try later"); matching on it here would couple to
    # strings that break when somebody rewords a 503.
    WEB_SEARCH = "web_search"


# -- research literature: POST /v1/web/papers vocabulary ----------------------
# Mirrored from app/websearch/schemas.py, not imported (the agent package never imports the backend;
# these are wire strings).
# THEIR DOCSTRINGS ARE AGENT-FACING SURFACE: FastMCP builds each tool's JSON schema from its annotations,
# so an enum on a signature ships its `__doc__` verbatim into `tools/list`, loaded whole by every session
# that pulls these tools. Rationale lives in comments like this one; docstrings say only what a caller
# choosing a value needs. (`MetricMode` above predates this and ships ~900 chars of history: do not copy it.)


class PaperMode(StrEnum):
    """`mode` on find_papers: which literature question is being asked."""

    # One tool, three modes, as `read_metrics` has three grains: one noun read three ways. The BACKEND refuses
    # arguments the mode cannot read (a `paper_id` with `mode="search"` is a 422), so that table is not
    # repeated here (two copies would drift; the endpoint's decides).
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

    # `empty` is an ANSWER (the provider ran the query, nothing matched); the service turns it into
    # `completeness.state="no_match"`. A model told only that its call failed rephrases and retries for every
    # step it has left. Not on any tool signature, so its docstring costs nothing in a schema.
    OK = "ok"
    EMPTY = "empty"


class ChannelError(StrEnum):
    """Client-side per-channel error markers (backend errors pass through as-is)."""

    MALFORMED_RESPONSE = "malformed_response"
    PROJECT_SCOPE_UNSUPPORTED = "project_scope_unsupported"

