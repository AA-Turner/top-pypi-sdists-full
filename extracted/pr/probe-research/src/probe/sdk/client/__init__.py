"""Client, split by domain (resources/ hold its methods). Front door for the old `probe.sdk.client`:
names read live from their pieces; a patch lands on every piece binding the name (foundation/front_door)."""

from __future__ import annotations
import importlib


from ...foundation.front_door.front_door import serve_pieces

#: The old module's pieces, in the split's load order: a write through the door reaches these only.
_PIECES = (
    "probe.sdk.client.authorship",
    "probe.sdk.client.core",
    "probe.sdk.client.credentials",
    "probe.sdk.client.ids",
    "probe.sdk.client.resources.artifacts",
    "probe.sdk.client.resources.auth",
    "probe.sdk.client.resources.catalog",
    "probe.sdk.client.resources.delivery",
    "probe.sdk.client.resources.integrations",
    "probe.sdk.client.resources.lineage",
    "probe.sdk.client.resources.notes",
    "probe.sdk.client.resources.projects.admin",
    "probe.sdk.client.resources.projects.experiment_admin",
    "probe.sdk.client.resources.projects.experiment_locator",
    "probe.sdk.client.resources.projects.experiments",
    "probe.sdk.client.resources.projects.headlines",
    "probe.sdk.client.resources.projects.papers",
    "probe.sdk.client.resources.projects.projects",
    "probe.sdk.client.resources.projects.summaries",
    "probe.sdk.client.resources.reads",
    "probe.sdk.client.resources.runs.attach",
    "probe.sdk.client.resources.runs.check",
    "probe.sdk.client.resources.runs.create",
    "probe.sdk.client.resources.runs.listing",
    "probe.sdk.client.resources.runs.metrics",
    "probe.sdk.client.resources.runs.reads",
    "probe.sdk.client.resources.runs.reopen.conflict",
    "probe.sdk.client.resources.runs.reopen.reopen",
    "probe.sdk.client.resources.runs.reopen.retry_lineage",
    "probe.sdk.client.resources.runs.reopen.status_holds",
    "probe.sdk.client.resources.runs.reopen.takeover",
    "probe.sdk.client.resources.runs.runs",
    "probe.sdk.client.resources.runs.views",
    "probe.sdk.client.resources.runs.writers",
    "probe.sdk.client.resources.sessions",
    "probe.sdk.client.resources.workspaces",
    "probe.sdk.client.server_features",
    "probe.sdk.delivery.notices",
    "probe.sdk.delivery.outbox.drainer",
    "probe.sdk.client.client",
)

# Every piece loads here, as the old module ran whole on import: a piece first imported at
# interpreter exit would exec there (CPython 3.12 then loses an uncaught Ctrl-C's exit code).
for _piece in _PIECES:
    importlib.import_module(_piece)
del _piece

#: Every name the old module bound -> the piece that holds it (defines it, else imports it).
_HOMES = {
    # probe.sdk.client.resources.projects.experiment_locator
    "contextvars": "probe.sdk.client.resources.projects.experiment_locator",
    "functools": "probe.sdk.client.resources.projects.experiment_locator",
    "ThreadPoolExecutor": "probe.sdk.client.resources.projects.experiment_locator",
    "contextmanager": "probe.sdk.client.resources.projects.experiment_locator",
    "Iterable": "probe.sdk.client.resources.projects.experiment_locator",
    "_ScopeKind": "probe.sdk.client.resources.projects.experiment_locator",
    "CapabilityUnavailable": "probe.sdk.client.resources.projects.experiment_locator",
    "_EXPERIMENT_PAGE_MAX": "probe.sdk.client.resources.projects.experiment_locator",
    "_PREDATES_CHILD_ROUTES": "probe.sdk.client.resources.projects.experiment_locator",
    "_moved_away": "probe.sdk.client.resources.projects.experiment_locator",
    "_experiment_pages": "probe.sdk.client.resources.projects.experiment_locator",
    "_offset_cursor": "probe.sdk.client.resources.projects.experiment_locator",
    "_WALK_CONCURRENCY": "probe.sdk.client.resources.projects.experiment_locator",
    "_WALK_MEMO": "probe.sdk.client.resources.projects.experiment_locator",
    "_one_walk": "probe.sdk.client.resources.projects.experiment_locator",
    "_walks_once": "probe.sdk.client.resources.projects.experiment_locator",
    # probe.sdk.client.resources.runs.attach
    "difflib": "probe.sdk.client.resources.runs.attach",
    "random": "probe.sdk.client.resources.runs.attach",
    "Run": "probe.sdk.client.resources.runs.attach",
    # probe.sdk.client.resources.runs.metrics
    "json": "probe.sdk.client.resources.runs.metrics",
    "SourceReadContractEnum": "probe.sdk.client.resources.runs.metrics",
    "nonfinite": "probe.sdk.client.resources.runs.metrics",
    "SOURCE_READ_CONTRACT": "probe.sdk.client.resources.runs.metrics",
    "_MAX_STEPPED_PAGES": "probe.sdk.client.resources.runs.metrics",
    "_series_key": "probe.sdk.client.resources.runs.metrics",
    "_merge_wide_page": "probe.sdk.client.resources.runs.metrics",
    # probe.sdk.client.core
    "os": "probe.sdk.client.core",
    "socket": "probe.sdk.client.core",
    "uuid": "probe.sdk.client.core",
    "warnings": "probe.sdk.client.core",
    "weakref": "probe.sdk.client.core",
    "deque": "probe.sdk.client.core",
    "Callable": "probe.sdk.client.core",
    "Mapping": "probe.sdk.client.core",
    "Path": "probe.sdk.client.core",
    "Any": "probe.sdk.client.core",
    "config_module": "probe.sdk.client.core",
    "_diagnostics": "probe.sdk.client.core",
    "errors": "probe.sdk.client.core",
    "Settings": "probe.sdk.client.core",
    "resolve": "probe.sdk.client.core",
    "WIZARD_HINT": "probe.sdk.client.core",
    "CredentialSource": "probe.sdk.client.core",
    "credential_fingerprint": "probe.sdk.client.core",
    "Journal": "probe.sdk.client.core",
    "Surface": "probe.sdk.client.core",
    "Transport": "probe.sdk.client.core",
    "_env_async_writes": "probe.sdk.client.core",
    "_usable_journal": "probe.sdk.client.core",
    "_DEFAULT_EXPORT_INTERVAL_SECONDS": "probe.sdk.client.core",
    "_CODE_TOKEN_EXPORT_INTERVAL_S": "probe.sdk.client.core",
    # probe.sdk.client.ids
    "re": "probe.sdk.client.ids",
    "_is_uuid": "probe.sdk.client.ids",
    "_BARE_ID": "probe.sdk.client.ids",
    "_id_ref": "probe.sdk.client.ids",
    "catalog_path_ref": "probe.sdk.client.ids",
    "_present": "probe.sdk.client.ids",
    "_norm_id": "probe.sdk.client.ids",
    "_same_id": "probe.sdk.client.ids",
    # probe.sdk.client.resources.projects.experiments
    "shlex": "probe.sdk.client.resources.projects.experiments",
    "_ProjectKind": "probe.sdk.client.resources.projects.experiments",
    "_EXPERIMENT_DESCRIPTION_RETIRED": "probe.sdk.client.resources.projects.experiments",
    "_PREDATES_FORKS": "probe.sdk.client.resources.projects.experiments",
    "_refuse_read_only_experiment_fields": "probe.sdk.client.resources.projects.experiments",
    "_from_experiment_api": "probe.sdk.client.resources.projects.experiments",
    # probe.sdk.client.resources.auth
    "sys": "probe.sdk.client.resources.auth",
    # probe.sdk.client.client
    "threading": "probe.sdk.client.client",
    "Authorship": "probe.sdk.client.client",
    "observe_with": "probe.sdk.client.client",
    "Delivery": "probe.sdk.client.client",
    "_request_log": "probe.sdk.client.client",
    "Client": "probe.sdk.client.client",
    # probe.sdk.client.credentials
    "time": "probe.sdk.client.credentials",
    "_failure_kind": "probe.sdk.client.credentials",
    # probe.sdk.client.resources.artifacts
    "nullcontext": "probe.sdk.client.resources.artifacts",
    "ScopedUploadRequest": "probe.sdk.client.resources.artifacts",
    "UploadRequest": "probe.sdk.client.resources.artifacts",
    "read_artifact_rows": "probe.sdk.client.resources.artifacts",
    "name_with_extension": "probe.sdk.client.resources.artifacts",
    "fingerprint": "probe.sdk.client.resources.artifacts",
    "InspectionResult": "probe.sdk.client.resources.artifacts",
    "PreparedUpload": "probe.sdk.client.resources.artifacts",
    "freeze_upload": "probe.sdk.client.resources.artifacts",
    "Anchor": "probe.sdk.client.resources.artifacts",
    "_SCOPED_ANCHORS": "probe.sdk.client.resources.artifacts",
    # probe.sdk.client.resources.runs.reopen.conflict
    "dataclass": "probe.sdk.client.resources.runs.reopen.conflict",
    "Rewind": "probe.sdk.client.resources.runs.reopen.conflict",
    "_repin_bracket_lease": "probe.sdk.client.resources.runs.reopen.conflict",
    "_LEASES_FEATURE": "probe.sdk.client.resources.runs.reopen.conflict",
    "_ATTACH_JITTER_PER_RANK": "probe.sdk.client.resources.runs.reopen.conflict",
    "_ATTACH_JITTER_MAX": "probe.sdk.client.resources.runs.reopen.conflict",
    "_attach_jitter_seconds": "probe.sdk.client.resources.runs.reopen.conflict",
    "_writer_lease": "probe.sdk.client.resources.runs.reopen.conflict",
    # probe.sdk.client.resources.projects.papers
    "StrEnum": "probe.sdk.client.resources.projects.papers",
    "CitationDirection": "probe.sdk.client.resources.projects.papers",
    "ProjectRelation": "probe.sdk.client.resources.projects.papers",
    "_citation_direction": "probe.sdk.client.resources.projects.papers",
    # probe.sdk.client.resources.catalog
    "ArtifactVersionCreate": "probe.sdk.client.resources.catalog",
    "UploadGcRequest": "probe.sdk.client.resources.catalog",
    "_checkpoints": "probe.sdk.client.resources.catalog",
    "ArtifactRedactedWarning": "probe.sdk.client.resources.catalog",
    # probe.sdk.client.resources.lineage
    "EdgeCreate": "probe.sdk.client.resources.lineage",
    "ExecutionRecordCreate": "probe.sdk.client.resources.lineage",
    "ExperimentVersionMint": "probe.sdk.client.resources.lineage",
    # probe.sdk.client.resources.reads
    "IngestRunRequest": "probe.sdk.client.resources.reads",
    "LatestScalarsRequest": "probe.sdk.client.resources.reads",
    # probe.sdk.client.resources.runs.views
    "MetricViewCreate": "probe.sdk.client.resources.runs.views",
    "MetricViewPatch": "probe.sdk.client.resources.runs.views",
    "MetricViewPreviewRequest": "probe.sdk.client.resources.runs.views",
    "_view_spec": "probe.sdk.client.resources.runs.views",
    # probe.sdk.client.resources.projects.experiment_admin
    "RunGroupCreate": "probe.sdk.client.resources.projects.experiment_admin",
    "RunGroupPatch": "probe.sdk.client.resources.projects.experiment_admin",
    "_EXPERIMENT_PAGE_DEFAULT": "probe.sdk.client.resources.projects.experiment_admin",
    # probe.sdk.client.resources.runs.reads
    "TrialPatch": "probe.sdk.client.resources.runs.reads",
    # probe.sdk.client.authorship
    "agent_session": "probe.sdk.client.authorship",
    "_authored_by": "probe.sdk.client.authorship",
    "_put_authorship": "probe.sdk.client.authorship",
    # probe.sdk.client.resources.runs.create
    "_coerce": "probe.sdk.client.resources.runs.create",
    "outcome_unknown": "probe.sdk.client.resources.runs.create",
    "wait_out_retry_after": "probe.sdk.client.resources.runs.create",
    # probe.sdk.client.resources.runs.check
    "KIND_LABEL_KEY": "probe.sdk.client.resources.runs.check",
    # probe.sdk.client.resources.projects.admin
    "canonical_tags": "probe.sdk.client.resources.projects.admin",
    "Page": "probe.sdk.client.resources.projects.admin",
    "_UNSET": "probe.sdk.client.resources.projects.admin",
    # probe.sdk.client.resources.delivery
    "UNPLACED_PROJECT": "probe.sdk.client.resources.delivery",
    # probe.sdk.client.resources.runs.runs
    "without_patience": "probe.sdk.client.resources.runs.runs",
    # probe.sdk.delivery.notices
    "_telemetry": "probe.sdk.delivery.notices",
    "_age_seconds": "probe.sdk.delivery.notices",
    "_minutes_since": "probe.sdk.delivery.notices",
    # probe.sdk.client.resources.projects.summaries
    "_PREDATES_SUMMARIES": "probe.sdk.client.resources.projects.summaries",
    # probe.sdk.client.resources.projects.projects
    "_session_page_params": "probe.sdk.client.resources.projects.projects",
    "_same_name": "probe.sdk.client.resources.projects.projects",
    "_exactly": "probe.sdk.client.resources.projects.projects",
    # probe.sdk.client.server_features
    "_route_absent": "probe.sdk.client.server_features",
    # probe.sdk.client.resources.runs.reopen.takeover
    "_TAKEOVER_WAIT_SECONDS": "probe.sdk.client.resources.runs.reopen.takeover",
    "_TAKEOVER_MIN_SILENCE": "probe.sdk.client.resources.runs.reopen.takeover",
    "_TAKEOVER_MAX_SILENCE": "probe.sdk.client.resources.runs.reopen.takeover",
    "_env_seconds": "probe.sdk.client.resources.runs.reopen.takeover",
    "_takeover_wait_budget": "probe.sdk.client.resources.runs.reopen.takeover",
    "_takeover_threshold": "probe.sdk.client.resources.runs.reopen.takeover",
    "_takeover_sleep": "probe.sdk.client.resources.runs.reopen.takeover",
    # probe.sdk.client.resources.runs.reopen.reopen
    "_TAKEOVER_DRAIN_SECONDS": "probe.sdk.client.resources.runs.reopen.reopen",
    # probe.sdk.client.resources.runs.reopen.status_holds
    "_TAKEOVER_BUDGET_SLACK_SECONDS": "probe.sdk.client.resources.runs.reopen.status_holds",
    "_TAKEOVER_HOLD_KEY": "probe.sdk.client.resources.runs.reopen.status_holds",
    "_TAKEOVER_HOLD_MARGIN_SECONDS": "probe.sdk.client.resources.runs.reopen.status_holds",
    # probe.sdk.delivery.outbox.drainer
    "_at_exit": "probe.sdk.delivery.outbox.drainer",
    # probe.sdk.client.resources.sessions
    "DEFAULT_SESSION_SOURCE": "probe.sdk.client.resources.sessions",
}
#: `from <old path> import *` takes what the old module's did.
__all__ = [name for name in _HOMES if not name.startswith("_")]

serve_pieces(__name__, _HOMES, pieces=_PIECES)
