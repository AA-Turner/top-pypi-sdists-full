"""The Probe Research SDK client core.

Two write paths, one core (per the SDK/CLI primitives sketch):
  * granular ``/v1`` calls for interactive / agent-driven capture (Anthrogen);
  * one-shot idempotent ``/ingest`` push for install-once passive capture (Osmosis).

Every method maps onto a real v4 endpoint (Probe Research v0.4.0.0 ingestion fold-in).
"""

from __future__ import annotations

import contextvars
import difflib
import functools
import errno
import json
import os
import random
import shlex
import socket
import sys
import threading
import time
import uuid
import warnings
import weakref
from collections import deque
from concurrent.futures import ThreadPoolExecutor
from contextlib import contextmanager
from collections.abc import Callable, Iterable, Mapping
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any

#: Re-exported through `probe.sdk` so a caller can write `probe.Authorship.human`
#: without reaching into `probe._generated`. The enum is generated from the
#: OpenAPI schema, which is the only place the vocabulary is defined.
from .._generated.models import Authorship as Authorship  # re-export: probe.Authorship
from .._generated.models import SourceReadContractEnum
from ..models import (
    ArtifactVersionCreate,
    ProjectKind as _ProjectKind,
    ScopeKind as _ScopeKind,
    CitationDirection,
    EdgeCreate,
    ExecutionRecordCreate,
    ExperimentVersionMint,
    IngestRunRequest,
    LatestScalarsRequest,
    MetricViewCreate,
    MetricViewPatch,
    MetricViewPreviewRequest,
    RunGroupCreate,
    RunGroupPatch,
    ScopedUploadRequest,
    TrialPatch,
    UploadGcRequest,
    UploadRequest,
)
from . import config as config_module
from . import agent_session
from . import coerce as _coerce
from . import safe_warn as _diagnostics

from . import errors
from . import nonfinite
from .artifact_listing import read_artifact_rows
from .errors import CapabilityUnavailable
from .config import Settings, resolve
from .tags import canonical_tags
from .filetype import name_with_extension
from .hashing import fingerprint
from .secret_gate import check_upload, freeze_upload, prepare_upload
from .session_marker import WIZARD_HINT
from .journal import CredentialSource, Journal, credential_fingerprint, run_ref_for_path
from .journal import classify as _journal_classify

from .surface import Surface
from .transport import (
    Page,
    Transport,
    outcome_unknown,
    wait_out_retry_after,
    without_patience,
)

# Eager, not lazy (review of #2056): first importing a module during
# interpreter finalization made an uncaught Ctrl-C exit 1 instead of
# re-raising SIGINT (observed on 3.12; pre-importing fixes it).
# `_report_delivery` below used to do this import lazily, right there in the
# finalizer -- which is exactly the first-import-at-exit case that trips it.
# Importing it here, at ordinary module load time (well before any close can
# run), keeps the module already imported by the time exit teardown starts.
from probe._shared import telemetry as _telemetry

#: Kinds of unstorable metric point this process has warned about.
_UNSTORABLE_WARNED: set[str] = set()


def _age_seconds(stamp: object) -> int | None:
    """Seconds since an ISO timestamp from status.json, or None."""
    if not stamp:
        return None
    try:
        from datetime import datetime, timezone

        then = datetime.fromisoformat(str(stamp))
        if then.tzinfo is None:
            then = then.replace(tzinfo=timezone.utc)
        return max(0, int((datetime.now(timezone.utc) - then).total_seconds()))
    except (TypeError, ValueError):
        return None


def _minutes_since(stamp: object) -> int | None:
    try:
        from datetime import datetime, timezone

        then = datetime.fromisoformat(str(stamp))
        if then.tzinfo is None:
            then = then.replace(tzinfo=timezone.utc)
        return max(0, int((datetime.now(timezone.utc) - then).total_seconds() // 60))
    except (TypeError, ValueError):
        return None


def _warn_unstorable(reasons: list[str]) -> None:
    """One warning per kind per process for points dropped as unstorable."""
    from .unstorable import MAX_METRIC_KEY_BYTES

    for reason in sorted(set(reasons)):
        if reason in _UNSTORABLE_WARNED:
            continue
        _UNSTORABLE_WARNED.add(reason)
        what = (
            "a step outside a 64-bit signed integer"
            if reason == "step"
            else f"a key over {MAX_METRIC_KEY_BYTES} bytes"
        )
        _diagnostics.warn(
            f"probe: dropped metric point(s) with {what}: the server cannot store them. "
            "Later ones are dropped without a warning."
        )

#: Outbox directories this process has already warned about falling back from.
_FALLBACK_WARNED: set[str] = set()
_K8S_NOTICE_GIVEN = False


def _usable_journal(directory: Path | None) -> Journal:
    """The journal a `Client` should queue in: ``directory`` (default: the
    machine's outbox) when it can take appends, else the ``$TMPDIR`` fallback
    with ONE warning that says it does not survive a pod or machine restart
    (plan 1.5). An unusable queue used to drop every write, one warning per
    write; an explicit ``PROBE_OUTBOX_DIR`` that is unusable falls back too."""
    from .journal import fallback_dir, private_fallback_root

    primary = Journal(directory)
    try:
        reason = primary.usable()
    except Exception:  # noqa: BLE001 -- cannot tell: keep the configured queue
        return primary
    if reason is None:
        if (
            directory is None
            and not os.environ.get("PROBE_OUTBOX_DIR")
            and _under_private_fallback(primary.dir, private_fallback_root)
        ):
            # No home directory at all (`journal.default_root`): the default
            # already IS the fallback, which must still be said once.
            _warn_fallback(primary, "there is no home directory", primary)
        elif directory is None:
            # Only the DEFAULT outbox: an explicit `spool_dir` is the caller's
            # own choice of place (review of #2054).
            _kubernetes_notice(primary)
        return primary
    try:
        fallback = Journal(fallback_dir())
        if fallback.dir == primary.dir or fallback.usable() is not None:
            return primary
    except Exception:  # noqa: BLE001
        return primary
    _warn_fallback(primary, reason, fallback)
    return fallback


def _under_private_fallback(path: Path, private_fallback_root) -> bool:
    try:
        return path.is_relative_to(private_fallback_root())
    except Exception:  # noqa: BLE001
        return False


def _warn_fallback(primary: Journal, reason: str, fallback: Journal) -> None:
    if str(primary.dir) in _FALLBACK_WARNED:
        return
    _FALLBACK_WARNED.add(str(primary.dir))
    where = (
        f"queueing in {fallback.dir}"
        if fallback.dir == primary.dir
        else f"the outbox at {primary.dir} cannot be used; queueing in {fallback.dir} instead"
    )
    small = ""
    try:
        import shutil

        free = shutil.disk_usage(fallback.dir if fallback.dir.exists() else fallback.dir.parent).free
        if free < 256 * 1024 * 1024:
            # A small tmpfs: most writes will be sent directly or dropped, and
            # this is the one place that can say why (review of #2054).
            small = f" It has only {free // (1024 * 1024)} MiB free, so writes may be dropped."
    except OSError:
        pass
    _diagnostics.warn(
        f"probe: {reason}: {where}. That directory does NOT survive a pod or machine "
        f"restart: set PROBE_OUTBOX_DIR to a writable, persistent path.{small}"
    )


def _kubernetes_notice(journal: Journal) -> None:
    """Once per process, on Kubernetes with the default outbox: the queue sits
    on the container's own disk, and the detached worker dies with the pod, so
    writes still queued when the pod is deleted are lost (plan 1.5)."""
    global _K8S_NOTICE_GIVEN
    if (
        _K8S_NOTICE_GIVEN
        or not os.environ.get("KUBERNETES_SERVICE_HOST")
        or os.environ.get("PROBE_OUTBOX_DIR")
        or os.environ.get("PROBE_OUTBOX_WORKER")
        or not _on_container_root_disk(journal.dir)
    ):
        return
    _K8S_NOTICE_GIVEN = True
    _diagnostics.warn(
        f"probe: running on Kubernetes with the outbox on the container's disk "
        f"({journal.dir}); writes still queued when the pod is deleted are lost. Set "
        "PROBE_OUTBOX_DIR to a persistent volume, and PROBE_FINISH_TIMEOUT_SEC=600 with "
        "terminationGracePeriodSeconds at least that long."
    )


def _on_container_root_disk(path: Path) -> bool:
    """Whether ``path`` sits on the same filesystem as ``/`` (the container's
    own writable layer). A HOME that is itself a mounted volume (JupyterHub's
    per-user PV) is on another device, and the notice would be wrong there
    (review of #2054)."""
    try:
        probe_path = path
        while not probe_path.exists() and probe_path.parent != probe_path:
            probe_path = probe_path.parent
        return os.stat(probe_path).st_dev == os.stat("/").st_dev
    except OSError:
        return False


#: An append that failed for want of space (plan 1.5): ENOSPC, and EDQUOT
#: where the platform has it.
_OUT_OF_SPACE = frozenset(
    code for code in (errno.ENOSPC, getattr(errno, "EDQUOT", None)) if code is not None
)

#: A run mirrored from another tool (a W&B live-sync run, say) keeps its metric
#: POINTS at the source; Probe stores a passport, not a copy. The provider read
#: paths therefore refuse a caller that has not declared which coverage contract
#: it understands, because a silent fallback would hand back a truncated or
#: re-sampled series as though it were the whole run. Every read below is
#: written against coverage-v1, so every read below says so. Omitting it is how
#: the MCP metric views came to report a mirrored run as having no metrics at
#: all while the same data returned fine over HTTP.
SOURCE_READ_CONTRACT = SourceReadContractEnum.coverage_v1.value


def _authored_by(explicit: str | None) -> str | None:
    """The `authored_by` to send: what the caller declared, else the environment.

    ONE RESOLVER, so every door agrees. `None` back means SEND NO KEY -- not
    `"authored_by": null` -- because the server reads an absent field as "this
    client has not been taught to say" and applies its historical inference,
    which is exactly the behaviour every release before this one had.
    """
    return explicit if explicit is not None else agent_session.default_authorship()


def _put_authorship(body: dict, explicit: str | None) -> None:
    """Stamp `authored_by` into a request body, or leave the body untouched."""
    resolved = _authored_by(explicit)
    if resolved is not None:
        body["authored_by"] = resolved


def _view_spec(spec: Any) -> dict:
    """Normalize an expression-view spec through ``probe.expr``.

    An ``Expr``, a bare node dict, and a full ``{"expression": ...}`` mapping are
    all accepted and all validated. Imported lazily: ``expr`` pulls the generated
    models, and a client that never touches views should not pay for them.
    """
    from . import expr as expr_module

    return expr_module.spec(spec)


def _failure_kind(exc: BaseException) -> str:
    """An exception's type and HTTP status, never its text: a request error can
    carry the Authorization header (a non-ASCII token), and warnings reach the
    run's uploaded stderr."""
    status = getattr(exc, "status", None)
    return f"{type(exc).__name__}{f' {status}' if status else ''}"


def _touch_run_lease(
    path: str, *, base_url: str | None = None, spool_dir: str | None = None
) -> None:
    """Renew the auto-update lease for whichever run this write targets.

    Reuses ``run_ref_for_path`` -- the journal's own extractor -- rather than a
    second parser, so the run a write is attributed to for lease purposes is by
    construction the same one it is attributed to for barrier purposes.

    Never raises: instrumentation must not be able to break the write it rides on.
    """
    try:
        run_ref = run_ref_for_path(path)
        if not run_ref:
            return
        from probe._shared import run_lock

        run_lock.renew_lease_if_stale(run_ref)
    except Exception as exc:  # noqa: BLE001 -- see docstring
        # Still swallowed. But a lease that stops renewing is how a live run
        # silently becomes `untracked`, so the evidence stops being deleted.
        _capture_swallowed(exc, site="client.lease_renew", base_url=base_url, spool_dir=spool_dir)


def _capture_swallowed(
    exc: BaseException, *, site: str, base_url: str | None = None, spool_dir: str | None = None
) -> None:
    """Report a swallowed exception without importing diagnostics at module load.

    Lazy on purpose: `diagnostics` reaches `probe.cli.telemetry` on its no-run
    leg, and `import probe` in a training script must not drag the CLI in.

    `base_url` is the backend THIS client is talking to and is what gates the
    report against the self-host egress contract -- the SDK resolves it from
    `probe.init(base_url=...)` or a named context, so the CLI config file (which
    is what `report_crash` falls back to) can name a different backend entirely.
    Omitted means suppressed, never guessed."""
    try:
        from . import diagnostics as _diag

        _diag.capture_swallowed(exc, site=site, base_url=base_url, spool_dir=spool_dir)
    except Exception:  # noqa: BLE001 -- a reporter must never break a swallow
        pass


class _UNSET:  # noqa: N801 — a sentinel type, used as the value itself
    """Distinguishes "argument omitted" from an explicit ``None`` (0148).

    ``update_project``'s ``parent_project_id`` is the one field where those
    differ on the wire: an explicit null DETACHES, an omitted key leaves the
    parent untouched. A default of ``None`` could not express that.
    """


#: AN EXPERIMENT'S ADDRESS ON THE WIRE.
#:
#: 0231 made an experiment a project row (a "leaf") and retired
#: `/v1/experiments/*` (410). The light-experiments split gave experiments their
#: own record again and, at R4, this client moved onto the experiment API:
#: `/v1/projects/{project}/experiments[/{experiment}]` (see the experiments
#: section of `Client`). `_as_experiment` below stays for the read-only
#: `Reader`: a service token reaches only allowlisted reads, and the experiment
#: API is not on that list, so the Reader still reads the leaf row.
#:
#: Paths are spelled out at every call site rather than built by a helper:
#: `tests/test_parity.py` READS the client's source to decide which backend
#: routes a client can reach, and refuses a transport call whose path it cannot
#: resolve.


def _as_experiment(row: object) -> object:
    """A project-shaped row, answered back in the experiment vocabulary.

    The SDK's public surface is unchanged by the move -- callers that read
    `row["question"]` keep reading it -- so the two renames are undone on the
    way out. Additive, never destructive: the project fields stay, because a
    caller that has already learned the new names should not lose them.
    """
    if not isinstance(row, dict):
        return row
    out = dict(row)
    if "question" not in out and "description" in out:
        out["question"] = out["description"]
    if "project_id" not in out and "parent_project_id" in out:
        out["project_id"] = out["parent_project_id"]
    return out


#: An experiment's description was replaced by its question (0231); both the
#: project address and the experiment API refuse it, and this says why first.
_EXPERIMENT_DESCRIPTION_RETIRED = (
    "an experiment's description was replaced by its QUESTION (0231): a "
    "leaf project's `description` field holds the question it answers, so "
    "there is no separate slot left for this text. Pass question= for what "
    "the experiment is testing, or document= for prose about it -- which is "
    "where existing descriptions were moved."
)

#: The experiment API's page sizes (`app/experiments/store.py`,
#: `read_router.py`): at most 500 per page, 100 when unasked.
_EXPERIMENT_PAGE_MAX = 500
_EXPERIMENT_PAGE_DEFAULT = 100


def _refuse_read_only_experiment_fields(**fields: object) -> None:
    """Refuse the fields an experiment no longer takes, before anything is sent.

    Since the light experiments' R3 switch an experiment is its own record, and
    the tags and metadata its project row carried are kept read-only (the
    project address answers 422 naming them); the experiment API has no such
    fields at all. Refusing here says so in one line instead of a round trip."""
    given = sorted(name for name, value in fields.items() if value is not None)
    if given:
        raise ValueError(
            f"{', '.join(given)} cannot be set on an experiment: an experiment's "
            "tags and metadata are kept read-only since it moved to its own record "
            "(light experiments). Set its name, question, notes or document instead."
        )


def _from_experiment_api(row: object) -> object:
    """An experiment from the experiment API, in the vocabulary callers already read.

    The experiment API answers an experiment AS an experiment: `project_id` is
    the project it is filed under and `question` the question it answers. Code
    written against the project address also reads `parent_project_id`,
    `description` (which held the question) and `kind`, so those are added --
    never replacing a field the API sent.

    `summary` on the API's detail read is the OVERVIEW PAGE's status, while on
    the project address `summary` was the deprecated alias of `summary_metrics`
    (headline numbers). It is renamed `overview_status` so no reader takes a
    page's queue state for a result."""
    if not isinstance(row, dict):
        return row
    out = dict(row)
    if isinstance(out.get("summary"), dict) and "content" in out["summary"]:
        out["overview_status"] = out.pop("summary")
    out.setdefault("kind", _ProjectKind.experiment.value)
    if "project_id" in out:
        out.setdefault("parent_project_id", out["project_id"])
    if "question" in out:
        out.setdefault("description", out["question"])
    return out


def _is_uuid(value: object) -> bool:
    try:
        uuid.UUID(str(value))
    except (ValueError, AttributeError, TypeError):
        return False
    return True


def _offset_cursor(cursor: str | None) -> int:
    """The experiment list's page token: an offset, as this client hands it out."""
    if cursor in (None, ""):
        return 0
    try:
        offset = int(str(cursor))
    except ValueError:
        raise ValueError(
            f"cursor {cursor!r} is not an experiment-list cursor (an older client's "
            "keyset cursor does not carry over); start from the first page"
        ) from None
    if offset < 0:
        raise ValueError("cursor cannot be negative")
    return offset


def _same_name(row: dict, name: str) -> bool:
    return str(row.get("name", "")).lower() == name.lower()


#: How many projects' experiment lists one walk fetches at once.
_WALK_CONCURRENCY = 8

#: A walk of every project's experiments, kept for ONE top-level call
#: (`run()`, `ensure_experiment`, `resolve_or_raise`): the near-miss guard can
#: be asked twice in one call (before a parent project is committed, then again
#: in the create), and the second ask must not walk the tenant again. Keyed by
#: client, per context (so per thread), and only ever holding a COMPLETE walk.
_WALK_MEMO: contextvars.ContextVar[dict[int, list[dict]] | None] = contextvars.ContextVar(
    "probe_experiment_walk_memo", default=None
)


@contextmanager
def _one_walk():
    """Share one experiment walk across everything inside this block."""
    if _WALK_MEMO.get() is not None:
        yield
        return
    token = _WALK_MEMO.set({})
    try:
        yield
    finally:
        _WALK_MEMO.reset(token)


def _walks_once(method):
    """Run a top-level method inside :func:`_one_walk`."""

    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        with _one_walk():
            return method(*args, **kwargs)

    return wrapper


def _route_absent(exc: errors.RosError) -> bool:
    """FastAPI's own 404 for a path no route matches: an older server."""
    return isinstance(exc, errors.NotFoundError) and exc.detail == "Not Found"


class Anchor(str, Enum):
    """What an artifact hangs off.

    The database CHECKs that exactly one anchor is set, so this is a closed
    vocabulary, not a hint. Four of these are *artifacts*; workspace and shared are
    *files*, which is a different noun on the wire (see :meth:`Client.upload_file`).
    """

    RUN = "run"
    EXPERIMENT = "experiment"
    PROJECT = "project"
    WORKSPACE = "workspace"
    SHARED = "shared"


#: Anchors whose upload body is a ``ScopedUploadRequest``. That model is declared
#: ``extra="forbid"``, so a run-only field (``kind``, ``meta``, ``span_id``,
#: ``step_index``) sent to one of these is a 422 — silently ignored is NOT what
#: happens, which is why the client rejects it up front with a readable message.
_SCOPED_ANCHORS = frozenset({Anchor.EXPERIMENT, Anchor.PROJECT, Anchor.WORKSPACE, Anchor.SHARED})

#: Anchors addressed as "files" rather than "artifacts": their identity is
#: (anchor, name) rather than (anchor, name, content_hash), so re-uploading a name
#: REPLACES it via a confirm-time swap instead of adding a second version. They also
#: have no metadata-only form — a file is its bytes.
_FILE_ANCHORS = frozenset({Anchor.WORKSPACE, Anchor.SHARED})

#: Iteration cap for the step-paged reads (metrics grouped/wide). The loop already
#: stops when the server reports the read exhausted; the cap only exists so a server
#: that keeps answering ``truncated`` with a non-advancing ``next_step`` cannot spin
#: a notebook forever. Hitting it returns honestly: ``truncated`` stays True and
#: ``next_step`` says where to resume.
_MAX_STEPPED_PAGES = 100


def _series_key(column: dict) -> tuple:
    """A wide-read column's series identity: (key, kind, canonical dimensions)."""
    return (
        column.get("key"),
        column.get("kind"),
        json.dumps(column.get("dimensions") or {}, sort_keys=True),
    )


def _merge_wide_page(merged: dict, page: dict) -> None:
    """Append one page of a wide read onto the merged result, in place.

    Columns are per-window: a series with no point inside a page's step range is
    absent from that page's ``columns``, so later pages can be wider (or narrower)
    than the first. Positions therefore cannot be trusted across pages — values are
    realigned by series identity, and a column new to the merge back-fills ``None``
    into the rows already collected, exactly as the server would have emitted had
    the whole range fit in one page."""
    if page.get("columns") == merged["columns"]:
        merged["rows"].extend(page.get("rows") or [])
        return
    positions = {_series_key(column): i for i, column in enumerate(merged["columns"])}
    for column in page.get("columns") or []:
        if _series_key(column) not in positions:
            positions[_series_key(column)] = len(merged["columns"])
            merged["columns"].append(column)
            for row in merged["rows"]:
                row["values"].append(None)
    width = len(merged["columns"])
    page_keys = [_series_key(column) for column in page.get("columns") or []]
    for row in page.get("rows") or []:
        values: list = [None] * width
        for series, value in zip(page_keys, row.get("values") or []):
            values[positions[series]] = value
        merged["rows"].append({**row, "values": values})


def _exactly(rows: list[dict], slug: str, *, strict: bool = False) -> dict | None:
    """The row whose slug actually MATCHES, or None.

    Never `rows[0]`. FastAPI silently drops a query parameter it does not
    declare, so a backend without the `?slug=` filter (an older engine, a
    rolled-back data plane, a self-hosted install) answers an unfiltered first
    page — and taking `rows[0]` there attaches the caller to a real, arbitrary,
    WRONG entity instead of erroring. That failure is worse than the
    get-or-create it replaced: get-or-create at least made an isolated new
    identity, where this appends your metrics to someone else's experiment.

    The membership check in `run()` cannot catch it either, because it reads its
    comparand from the same broken listing and so agrees with the bug. Verifying
    the slug here is what makes an unfiltered response degrade to "not found".
    """
    for row in rows or ():
        if row.get("slug") == slug:
            return row
    if strict and len(rows or ()) > 1:
        # A miss from a listing nobody filtered is not an absence. Only callers
        # deciding id-vs-slug ask for strict; get-or-create still wants "absent".
        raise errors.UnfilteredListing(
            f"this backend did not apply ?slug={slug!r} (returned {len(rows)} rows)"
        )
    return None


#: Poll interval handed to the in-process exporter (F2) when a client needs one
#: and the caller named none. Only a FALLBACK for the interval: the exporter is
#: woken by an Event on every enqueue, so this is how long an idle client waits
#: before re-checking, not how long a write waits to be delivered. Two seconds
#: mirrors the value the parity doc uses in its own example.
_DEFAULT_EXPORT_INTERVAL_SECONDS = 2.0

#: The `PROBE_ASYNC` spellings. This is the ONLY parser for them: the CLI used to
#: keep a second copy of this set and now delegates here, so there is one answer
#: to what the variable means rather than two that can drift apart.
_ASYNC_TRUE = {"1", "true", "yes", "on"}
_ASYNC_FALSE = {"0", "false", "no", "off"}


def _env_async_writes() -> bool | None:
    """`PROBE_ASYNC` as a tri-state: on, off, or unset (None -> use the default).

    Unset and unrecognised both return None on purpose. A typo'd value must not
    silently pin a write mode -- it warns and defers to the default, because the
    failure this knob exists to prevent is a training loop stuck on the wrong
    path with no way to tell.
    """
    raw = (os.environ.get("PROBE_ASYNC") or "").strip().lower()
    if not raw:
        return None
    if raw in _ASYNC_TRUE:
        return True
    if raw in _ASYNC_FALSE:
        return False
    warnings.warn(
        f"ignoring unrecognised PROBE_ASYNC={raw!r}; expected one of "
        f"{sorted(_ASYNC_TRUE | _ASYNC_FALSE)}",
        stacklevel=3,
    )
    return None


@dataclass(frozen=True)
class Rewind:
    """``on_conflict`` policy object (0185): resume the incumbent from a
    checkpoint, DISCARDING its step-indexed record from ``step`` onward.

    The parameterized member of the policy vocabulary — the four string
    policies need no arguments, a rewind needs its step, and carrying the step
    ON the policy means the two can never disagree. ``step`` matches W&B
    muscle memory: everything from it (inclusive) is rewritten, so a loop may
    re-log the checkpoint step itself or start one above it.

    Destructive by explicit request only, and the request is also the consent:
    a ``completed`` incumbent — the deliberate stop-then-rewind flow — reopens
    under a Rewind where a plain resume keeps refusing it. Keep-both belongs
    to :meth:`Client.fork_run`; from-scratch retries to ``"supersede"``.
    """

    step: int

    def __post_init__(self) -> None:
        if isinstance(self.step, bool) or not isinstance(self.step, int) or self.step < 0:
            raise errors.ValidationError(
                f"Rewind(step={self.step!r}): the rewind step must be a "
                "non-negative integer — the first step the relaunch will "
                "rewrite."
            )


def _repin_bracket_lease(run_id: str, write_epoch: object) -> None:
    """A reopen from THIS machine moved the run to a new epoch: carry it into
    the `probe run start` bracket's lease, if this machine holds a live one.

    The lease pins the epoch every later run-scoped CLI write stamps (0185),
    and since 1.10 that includes `probe run end`. The measured shape: `run
    start` pins 1, the quiet bracket is reaped `untracked`, the job's own
    `probe.init()` attaches and reopens (epoch 2), and `probe run end` then
    sent 1 and was refused (sync exit 1, async dead-lettered). A reopen made
    by the bracket's own job is not a newer attempt to fence out.

    Only a LIVE lease that already pins an epoch is touched: a run with no
    bracket must not grow a lease file. A reopen on ANOTHER machine cannot
    reach this file; see the PR notes. Never raises."""
    try:
        from probe._shared import run_lock

        if run_lock.lease_write_epoch(str(run_id)) is not None:
            run_lock.touch_lease(str(run_id), write_epoch=int(write_epoch))
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        pass


#: SDK reliability 2.3, requeue takeover. How long a relaunch waits for a
#: `running` incumbent to go silent before taking it over, and how long it spends
#: first delivering what the incumbent left queued in this outbox.
_TAKEOVER_WAIT_SECONDS = 300.0
_TAKEOVER_DRAIN_SECONDS = 120.0
#: The server's bounds on `takeover_stale_after_seconds`.
_TAKEOVER_MIN_SILENCE = 180
_TAKEOVER_MAX_SILENCE = 3600
#: A wait budget that allows any wait covers at least one threshold plus this,
#: so a relaunch seconds after the death is not refused at its first 409.
_TAKEOVER_BUDGET_SLACK_SECONDS = 30
#: The key marking a status op the takeover barrier set aside, and how long
#: past the barrier's own bounds a hold is honoured before the next drain or
#: relaunch treats its holder as dead and puts the op back (on the holder's own
#: host, a dead holder pid ends the hold at once: `journal.hold_abandoned`).
#: Short: both barrier phases are deadline-bounded, and a hold outliving the
#: reaper's 900 s cost a finished run its verdict (review of #2019). A hold
#: restored under a barrier still finishing is harmless -- 1.10's fence refuses
#: the old close once the takeover's epoch moves.
_TAKEOVER_HOLD_KEY = "takeover_hold"
_TAKEOVER_HOLD_MARGIN_SECONDS = 120.0


def _env_seconds(name: str, default: float) -> float:
    """A non-negative seconds budget from the environment; malformed warns."""
    raw = os.environ.get(name)
    if raw is None or not raw.strip():
        return default
    try:
        return max(0.0, float(raw))
    except ValueError:
        _diagnostics.warn(f"ignoring malformed {name}={raw!r}; expected seconds as a number")
        return default


def _takeover_wait_budget() -> float:
    """``PROBE_TAKEOVER_WAIT_SEC`` (300). A notebook cell never blocks for
    minutes on its own: under ipykernel the default is 0, so a live incumbent
    conflicts at once unless the variable asks for a wait."""
    default = 0.0 if "ipykernel" in sys.modules else _TAKEOVER_WAIT_SECONDS
    return _env_seconds("PROBE_TAKEOVER_WAIT_SEC", default)


def _takeover_threshold() -> int:
    """Silence that proves an incumbent dead: three of OUR beat intervals (a
    live one beats at least that often), never under the server's floor."""
    from .run import _heartbeat_interval

    import math

    interval = _heartbeat_interval()
    wanted = math.ceil(3 * interval) if interval > 0 else 0
    return int(min(_TAKEOVER_MAX_SILENCE, max(_TAKEOVER_MIN_SILENCE, wanted)))


#: SDK reliability 2.8: the server takes per-writer leases (0271).
_LEASES_FEATURE = "run_writer_leases"
#: (rank, world size, local rank) environment variables, most specific first,
#: the same schemes `fluent._GLOBAL_RANK_VARS` reads.
_LEASE_RANK_VARS = (
    ("RANK", "WORLD_SIZE", "LOCAL_RANK"),
    ("SLURM_PROCID", "SLURM_NTASKS", "SLURM_LOCALID"),
    ("OMPI_COMM_WORLD_RANK", "OMPI_COMM_WORLD_SIZE", "OMPI_COMM_WORLD_LOCAL_RANK"),
)


def _env_int(name: str) -> int | None:
    raw = (os.environ.get(name) or "").strip()
    return int(raw) if raw.isdigit() else None


#: The attach beat's spread: this many seconds per rank of the job, capped.
_ATTACH_JITTER_PER_RANK = 0.005
_ATTACH_JITTER_MAX = 2.0


def _attach_jitter_seconds(world_size: object) -> float:
    """How long a rank may wait before its attach beat: 0 for a single process,
    ~0.3 s for 64 ranks, 2 s from 400 ranks up."""
    try:
        size = int(world_size or 0)
    except (TypeError, ValueError):
        return 0.0
    if size <= 1:
        return 0.0
    return min(_ATTACH_JITTER_MAX, _ATTACH_JITTER_PER_RANK * size)


def _writer_lease(role: str, session_id: str) -> dict:
    """Who this process is, as a lease (sent on create/attach/reopen and on
    every lease beat). Rank fields come from the launcher's environment."""
    from .run import _heartbeat_interval

    lease: dict[str, Any] = {
        "session_id": str(session_id),
        "role": role,
        "host": socket.gethostname()[:255] or None,
        "pid": os.getpid(),
        "interactive": "ipykernel" in sys.modules,
    }
    interval = _heartbeat_interval()
    if interval > 0:
        lease["interval_seconds"] = float(interval)
    for rank_var, size_var, local_var in _LEASE_RANK_VARS:
        rank = _env_int(rank_var)
        if rank is None:
            continue
        lease["rank"] = rank
        size = _env_int(size_var)
        if size:
            lease["world_size"] = size
        local = _env_int(local_var)
        if local is not None:
            lease["local_rank"] = local
        break
    return lease


def _takeover_sleep(seconds: float) -> None:
    """The wait between takeover attempts, by a name tests can replace."""
    time.sleep(seconds)


def _at_exit(callback) -> None:
    """`atexit.register`, by a name tests can point elsewhere: a callback that
    outlives pytest runs after every monkeypatch is undone."""
    import atexit

    atexit.register(callback)


def _norm_id(value: object) -> str:
    return str(value or "").strip().removeprefix("id:").lower()


def _same_id(got: object, want: str) -> bool:
    """Two refs to one row: an `id:` prefix and case do not count."""
    return bool(_norm_id(got)) and _norm_id(got) == _norm_id(want)


#: The in-process exporter's interval for a client built with a token in code,
#: which the detached worker cannot hold (#2041 re-review).
_CODE_TOKEN_EXPORT_INTERVAL_S = 2.0


def _citation_direction(value: object) -> str:
    """``reference`` or ``citer``, checked before the request so a typo fails
    naming the vocabulary rather than as the server's 422."""
    raw = getattr(value, "value", value)
    try:
        return CitationDirection(str(raw).strip()).value
    except ValueError:
        allowed = ", ".join(d.value for d in CitationDirection)
        raise ValueError(f"citation direction must be one of {allowed}; got {raw!r}") from None


class Client:
    #: True for a client whose queue is drained by hand on purpose -- the
    #: offline run's, which `probe sync` drains (plan 2.12) -- so the "no
    #: background drainer" notice below would only be noise.
    _drains_by_hand = False

    def __init__(
        self,
        *,
        base_url: str | None = None,
        token: str | None = None,
        ingest_token: str | None = None,
        hmac_secret: str | None = None,
        settings: Settings | None = None,
        transport: Transport | None = None,
        fail_open: bool = True,
        journal: "Journal | None" = None,
        spool_dir: str | Path | None = None,
        async_writes: bool | None = None,
        auto_drain: bool = True,
        drain_interval: float | None = None,
        redact: "Callable[[dict], dict] | bool | None" = None,
        surface: str = Surface.SDK.value,
        client_headers: Mapping[str, str] | None = None,
        attribution: str | None = None,
        raise_permanent: bool = False,
    ):
        self.settings = settings or resolve(
            base_url=base_url,
            token=token,
            ingest_token=ingest_token,
            hmac_secret=hmac_secret,
        )
        # Plan 2.7: a credential read from the environment or the stored login's
        # config (what `probe.init()` builds) may be re-read when the API
        # refuses it; one the caller handed in never is. See
        # `refresh_credentials`.
        self._ambient_credentials = (
            settings is None and token is None and ingest_token is None and transport is None
        )
        #: Where the token came from, which is the ONLY place a refresh may look
        #: again: "env" re-reads PROBE_TOKEN alone (never the stored login, which
        #: can be another account on a shared box), "config" re-reads this
        #: context's stored token. None: passed in code, never re-read.
        self._credential_source: str | None = None
        if self._ambient_credentials and self.settings.token:
            self._credential_source = "env" if os.environ.get("PROBE_TOKEN") else "config"
        self._credential_lock = threading.Lock()
        self._credential_checked_at = float("-inf")
        self._credential_stale_warned = False
        #: (customer_id, user_id) of the credential this client started with.
        #: Looked up once, in the background, only when something that may
        #: need a refresh starts (a heartbeat, the exporter): after a revocation
        #: it can no longer be asked, a refresh adopts a new token only for the
        #: SAME account, and a one-request CLI command must not pay for it.
        self._credential_identity: tuple[str, str] | None = None
        self._credential_identity_started = False
        self._credential_identity_ready = threading.Event()
        #: A stored login already refused as another account's: not asked
        #: about again (a `/v1/me` every 30 s) until the config changes.
        self._credential_rejected: str | None = None
        # `surface` tags outbound requests for analytics attribution (cli/sdk/mcp).
        # Ignored when an already-built `transport` is supplied — it carries its own.
        if transport is not None and client_headers:
            raise ValueError(
                "client_headers configure the default Transport; pass them to "
                "a custom Transport directly"
            )
        self.transport = transport or Transport(
            self.settings,
            surface=surface,
            client_headers=client_headers,
            attribution=attribution,
        )
        if transport is not None and attribution is not None:
            from .transport import resolve_attribution

            transport.attribution = resolve_attribution(attribution)
        self.fail_open = fail_open
        #: `write`'s ``raise_permanent`` for every call that does not pass one.
        #: The CLI sets it for all its writes (lineage plan L14): a refusal
        #: raises and exits 1 instead of printing `null`, while a failure that
        #: could still succeed later is queued, as before. Off for the SDK: see
        #: `write`.
        self.raise_permanent = raise_permanent
        #: Called with each write whose request failed and fell back to the
        #: outbox (``queued``) or was lost with it (not ``queued``):
        #: `{"method", "path", "error", "queued"}`. `write()` returns None either
        #: way, the same None a 204 returns, so without it a caller one layer up
        #: (the CLI) could not say "queued" instead of printing `null` as a
        #: success. Nothing is recorded while it is None -- every SDK client:
        #: a training loop's failed writes are the delivery notices' to count.
        self.on_undelivered: Callable[[dict], None] | None = None
        #: With a hook set: the last `UNDELIVERED_KEPT` of those, and how many
        #: there were in all (the deque forgets the oldest).
        self.undelivered_writes: deque[dict] = deque(maxlen=self.UNDELIVERED_KEPT)
        self.undelivered_count = 0
        # One queue (eng review 2026-07-29, T1-C): the journal holds both
        # async-mode writes and the sync fail-open safety net that used to be
        # the spool. `spool_dir` keeps its name as the directory override.
        #
        # Async is the DEFAULT (ProSeCo, 2026-08-19): a synchronous data write
        # puts the network on the training loop's critical path, where a stalled
        # or refusing endpoint costs the run rather than the datapoint. `None`
        # means "nobody asked", which is what lets the credential gate below
        # degrade to sync instead of raising -- an explicit True still raises,
        # because a caller who asked for async deserves to hear that it cannot
        # be delivered. Reads, creates and `finish()` are unaffected: they never
        # travel through `write()`.
        # `_async_requested` is the ARGUMENT, and only the argument. It is
        # captured BEFORE the environment is folded in: assigning it after made
        # a stray `PROBE_ASYNC=1` (a documented CLI knob, so plausibly exported
        # in a shell profile or a SLURM script) read as an explicit request,
        # which skipped the transport gate below and produced an async client
        # with no auto-drain, no exporter and no credential guard -- writes
        # journaled to disk that nothing would ever deliver. The environment
        # steers the default; it never overrides the invariants that make
        # delivery possible.
        self._async_requested = async_writes
        if async_writes is None:
            # PROBE_ASYNC as an SDK knob, not just a CLI flag. The campaign that
            # forced this change had no way to change write mode without editing
            # the training script, because the var was read only in cli/main.py.
            async_writes = _env_async_writes()
        if async_writes is None:
            async_writes = True
        if async_writes and transport is not None and self._async_requested is not True:
            # Async needs the DEFAULT transport: the detached worker "can never
            # replay an injected one" (F1 below). This keeps every caller that
            # injects a transport -- the hosted MCP, the fake-transport tests --
            # on the synchronous, immediately-assertable path it was built
            # against. An explicit async_writes=True still opts in, delivering
            # through the in-process exporter (F2).
            async_writes = False
        if (
            async_writes
            and self._async_requested is not True
            and transport is None
            and not (self.settings.token or self.settings.ingest_token)
        ):
            # Nothing could ever drain this journal, and the caller never asked
            # for async, so the honest default is the path that still works.
            # The explicit-True gate further down keeps raising (F7).
            async_writes = False
        self.async_writes = async_writes
        #: Writes this client ACCEPTED and then dropped, because the outbox
        #: could not be written (ENOSPC, read-only state dir, flock ENOSYS).
        #: Exists because the signal dies otherwise: `_enqueue` returns a bool
        #: that `write()` discards, so a caller one layer up cannot distinguish
        #: "queued" from "lost" and would report success for data that reached
        #: nothing. Monotonic per client, and THIS process's drops only (another
        #: process writing the same run keeps its own); snapshot it around a
        #: write to check.
        self.dropped_writes = 0
        #: Writes sent straight to the server because the outbox's volume was
        #: under its free-space floor and the run had nothing queued (plan 1.5).
        #: Reported at `finish()` beside `dropped_writes`.
        self.direct_sends = 0
        self._direct_closed_until = float("-inf")
        self._direct_failures = 0
        self._direct_lock = threading.Lock()
        self._lanes: dict[str, Any] = {}
        if journal is not None and spool_dir is not None:
            raise ValueError("pass journal or spool_dir, not both")
        self.journal = journal or _usable_journal(
            Path(spool_dir).expanduser() if spool_dir else None
        )
        self.journal.attribution = str(getattr(self.transport, "attribution", "ambient"))
        #: Fingerprints of every credential this client has written with. An op
        #: whose stamp is not among them is not this client's to replay (#2035).
        self._credential_fingerprints: set[str] = set()
        mine = credential_fingerprint(self.settings.token, self.settings.ingest_token)
        if mine:
            self._credential_fingerprints.add(mine)
        #: The same for the ingest token, which `/ingest` writes go out with.
        self._ingest_fingerprints: set[str] = set()
        mine_ingest = credential_fingerprint(None, self.settings.ingest_token)
        if mine_ingest:
            self._ingest_fingerprints.add(mine_ingest)
        stamp = None
        if self.journal.context is None:
            name = config_module.current_context_name() or None
            self.journal.context = {"name": name, "base_url": self.settings.base_url}
            stamp = self._credential_stamp(name)
            if stamp is not None:
                self.journal.context["principal"] = stamp
                if (
                    journal is None
                    and stamp["source"] in (CredentialSource.ENV, CredentialSource.CODE)
                    and not self._is_the_stored_login(name)
                ):
                    # Its own queue (journal.CREDENTIAL_NAMESPACE): no release
                    # before the stamp reads it, so none can send these writes
                    # as the stored login -- or stop its pass on them -- and
                    # this credential's worker never waits behind another's
                    # (#2041 reviews). The stored login's writes stay in the
                    # shared queue, where older releases send them as that login.
                    self.journal = Journal.for_credential(
                        self.journal.dir,
                        self._credential_queue_name(stamp),
                        context=self.journal.context,
                        attribution=self.journal.attribution,
                    )
        # After the queue is settled (a credential's own queue, #2041): the
        # notices' baseline is read from the queue this client writes to.
        self._init_delivery_notices()
        # Never a run's code, reads or outputs, wherever it is (an explicit
        # `spool_dir` no environment variable names).
        from . import owndirs

        owndirs.note(self.journal.outbox_root)
        # Parity F1/F2 (docs/2026-08-04-outbox-miles-parity.md): async enqueue
        # wakes a delivery loop. Default (F1): kick the detached outbox worker
        # -- default-transport clients only, because the worker resolves its
        # own transport from config and can never replay an injected one.
        # With ``drain_interval`` (or PROBE_EXPORT_INTERVAL_SEC) set (F2): an
        # in-process exporter thread delivers through THIS client instead --
        # the fork-free path, and the one that works with any transport.
        if drain_interval is None and async_writes:
            raw = os.environ.get("PROBE_EXPORT_INTERVAL_SEC")
            if raw:
                try:
                    drain_interval = float(raw)
                except ValueError:
                    warnings.warn(
                        f"ignoring malformed PROBE_EXPORT_INTERVAL_SEC={raw!r}; "
                        "expected seconds as a float",
                        stacklevel=2,
                    )
        if (
            drain_interval is None
            and async_writes
            and auto_drain
            and transport is None
            and isinstance(stamp, dict)
            and stamp.get("source") == CredentialSource.CODE
        ):
            # A token passed in code is in no environment and no config file,
            # so the detached worker can never hold it: deliver in-process
            # instead, or these writes wait for flush()/finish() (#2041
            # re-review: 0 of 5 delivered live, stranded after exit).
            drain_interval = _CODE_TOKEN_EXPORT_INTERVAL_S
        self._drain_interval = drain_interval if async_writes else None
        self._exporter = None
        self._exporter_lock = threading.Lock()
        # A worker fork only makes sense for default-transport clients, but a
        # FORCED kick (deferred finish, F3) must work from sync clients too.
        self._default_transport = transport is None
        # ------------------------------------------------------------------
        # Async REQUIRES a drainer. There are exactly two (parity F1/F2) and
        # each has a precondition: the detached worker needs the default
        # transport, and the in-process exporter needs a drain_interval. Async
        # mode itself used to be gated on neither, so three reachable
        # configurations journaled every write to disk with nothing that would
        # ever deliver them -- silently, since a queued write returns None
        # exactly like a delivered one.
        #
        # The rule below makes "queues with no drainer" unrepresentable rather
        # than merely documented. Each branch picks the mechanism that CAN work
        # for that shape instead of accepting an undeliverable client.
        if (
            async_writes
            and self._drain_interval is None
            and not (auto_drain and self._default_transport)
        ):
            if transport is not None and self._drains_by_hand:
                pass
            elif transport is not None:
                # F1 is disqualified (the detached worker resolves its own
                # transport from config and can never replay an injected one)
                # and F2 needs an interval nobody named. That is not
                # automatically a void, though: `flush()`/`finish()` is a real
                # delivery mechanism, and draining by hand is exactly what the
                # CLI barrier and the fake-transport tests do on purpose.
                # Forcing an exporter here would start a background thread in
                # every one of them and race their assertions.
                #
                # So: say so, once, and leave the choice with the caller. The
                # silence was the bug, not the configuration.
                _diagnostics.warn(
                    "probe: async writes with a custom transport have no "
                    "background drainer — the detached worker cannot replay an "
                    "injected transport. Pass drain_interval=<seconds> for the "
                    "in-process exporter, or call flush()/finish() yourself; "
                    "otherwise queued writes stay on disk."
                )
            elif self._async_requested is None:
                # Nobody asked for async, and auto_drain=False rules out the
                # worker -- but this is a DEFAULT transport, so F2 is available.
                # Take it rather than degrading to sync: falling back to sync
                # puts the network back on the training loop's critical path,
                # which is the failure this whole change exists to remove, and
                # it would do so silently on a flag whose meaning shifted
                # underneath its users (before async became the default,
                # auto_drain=False only meant "do not auto-drain the fail-open
                # spool" and writes still went over the network).
                #
                # Async stays on and delivery is guaranteed; the caller loses
                # only the crash-surviving subprocess they opted out of.
                self._drain_interval = _DEFAULT_EXPORT_INTERVAL_SECONDS
            else:
                # Explicitly async AND explicitly no background drainer. Say
                # so, do not refuse: this is a real configuration, used by
                # writers that drain by hand and by tests that want a journal
                # to inspect without a thread racing their assertions. The
                # defect was never the shape, it was that a write into a queue
                # nothing would drain looked identical to a delivered one.
                _diagnostics.warn(
                    "probe: async writes with auto_drain=False have no "
                    "background drainer. Pass drain_interval=<seconds> for the "
                    "in-process exporter, or call flush()/finish() yourself; "
                    "otherwise queued writes stay on disk."
                )
        # Producer accounting (parity F4). Long-lived writers get a
        # per-process identity; the CLI surface shares one per-host id -- a
        # training loop of thousands of `probe --async log` invocations is ONE
        # producer line, not thousands of registry files (sequences stay safe:
        # allocation reads the registry under the append lock).
        # Parity F5: scrub payloads at CAPTURE -- before bytes hit the journal
        # (commonly on shared storage) or the wire. True selects the standard
        # scrubber; a callable brings your own. Default None: untouched.
        if redact is True:
            from .redaction import default_scrub

            self._redact: Callable | None = default_scrub
        else:
            self._redact = redact or None
        self._seal_producer_on_close = False
        if async_writes:
            host = socket.gethostname()
            if surface == Surface.CLI.value:
                producer_id = f"cli:{host}"
            else:
                producer_id = f"{surface}:{host}:{os.getpid()}:{uuid.uuid4().hex[:8]}"
                self._seal_producer_on_close = True
            # The per-host CLI id is right for a training loop and wrong for
            # concurrent CLI writers: several importers on one box collapse into
            # a single producer line and cannot be told apart afterwards. This
            # lets the caller name them (`PROBE_OUTBOX_PRODUCER_ID=import:shard-3`)
            # without every `probe --async log` minting a registry file.
            # Deliberately id-only: the seal-on-close decision stays with the
            # SURFACE, so naming a shared id does not make the first process to
            # exit mark the line closed under its still-live siblings.
            override = (os.environ.get("PROBE_OUTBOX_PRODUCER_ID") or "").strip()
            if override:
                producer_id = override
            try:
                self.journal.register_producer(producer_id, role=surface)
            except Exception:  # noqa: BLE001 -- accounting must never block writes
                pass
        self._auto_drain = (
            async_writes and auto_drain and transport is None and self._drain_interval is None
        )
        # Explicit receipt enqueue is asynchronous even on a client whose
        # ordinary entity writes are synchronous.
        self._delivery_auto_drain = auto_drain
        self._drainer_kick_interval = 1.0
        self._drainer_kicked_at = float("-inf")
        if (
            async_writes
            and transport is None
            and (auto_drain or self._drain_interval is not None)
            and not (self.settings.token or self.settings.ingest_token)
        ):
            # F7: queueing an op nothing can ever deliver fails hours later in
            # the drainer log, which is the worst place to learn it.
            raise errors.ValidationError(
                f"async_writes needs deliverable credentials: {WIZARD_HINT} "
                "or set PROBE_TOKEN -- or pass auto_drain=False to queue "
                "offline and deliver later via flush()/`probe outbox drain`"
            )
        self._events = None
        # Stop signals for every live run-heartbeat thread this client minted.
        # Weak so a finished beat (its Run collected, its thread exited) doesn't
        # accumulate here for the client's whole life.
        self._run_heartbeat_stops: weakref.WeakSet[threading.Event] = weakref.WeakSet()
        # 2.3: a close a relaunch killed mid-barrier held aside goes back in
        # the queue now, whatever this client's delivery mode (one stat when
        # nothing is held); the kick below then delivers it.
        try:
            self._restore_abandoned_holds()
        except Exception:  # noqa: BLE001 -- a hold left in place is the old behaviour
            pass
        if self._auto_drain:
            # A queue left by an earlier process (a pod recreated on the same
            # persistent volume, a laptop back from sleep) drains now, not at
            # this process's first write (plan 1.5). One status read; only a
            # queue with something in it is kicked.
            try:
                waiting = Journal.read_status(self.journal.dir) or {}
                if int(waiting.get("pending") or 0) or int(waiting.get("waiting") or 0):
                    self._kick_drainer()
            except Exception:  # noqa: BLE001 -- a kick is latency, never a gate
                pass
        if async_writes and auto_drain and self._default_transport:
            try:
                root = self.journal.outbox_root
                if root != self.journal.dir:
                    # This client queues in its credential's own queue (#2035),
                    # and may deliver it in-process; the shared queue's backlog
                    # is the shared worker's, which any process may start.
                    shared = Journal.read_status(root, credential_queues=False) or {}
                    if int(shared.get("pending") or 0) or int(shared.get("waiting") or 0):
                        from . import outbox_worker

                        outbox_worker.maybe_spawn(str(root))
            except Exception:  # noqa: BLE001 -- a kick is latency, never a gate
                pass

    # -- lifecycle ----------------------------------------------------------
    def _register_run_heartbeat(self, stop: threading.Event) -> None:
        self._run_heartbeat_stops.add(stop)

    def hand_off_delivery(self) -> None:
        """Stop delivering through this client and leave the queue deliverable.

        ONE definition, called from every place that stops an exporter. It used
        to be copy-pasted into `_settle_journaled_finish` and
        `_queue_deferred_finish`, one copy was fixed, and the other kept the bug
        through three reviews -- a near-duplicate is exactly how a fix fails to
        stick.

        Two rules, both learned the hard way:

        * Only hand off where a detached worker can actually be spawned.
          `_kick_drainer` early-returns on a non-default transport, so closing
          the exporter on an F2 client (explicit async + injected transport +
          drain_interval) left NOTHING delivering -- and `_after_enqueue` never
          respawns a closed exporter, so every later write was stranded too.
        * Clear the attribute after closing, but only if the exporter was
          ALIVE. A dead one is dead because of an auth block, and the
          documented invariant is that those are not respawned -- clearing it
          unconditionally would rebuild an exporter against the same rejected
          credential, which is the zombie-uploader pitfall.
        """
        exporter = self._exporter
        if not self._default_transport:
            return
        if exporter is not None:
            was_alive = getattr(exporter, "alive", True)
            exporter.close()
            if was_alive:
                self._exporter = None
        self._kick_drainer(force=True)

    def close(self, *, timeout: float | None = None) -> None:
        # The exporter drains over this client's transport; join it first. Its
        # own stop path now does a final pass, so ops written since the last
        # tick are delivered rather than left for a worker this client never
        # kicked. Then hand what remains to the detached worker: a closed
        # exporter delivers nothing, and `with Client(...) as c:` used to strand
        # everything written in the last drain_interval.
        #
        # ``timeout`` caps that join below its own 5 s: a reinit passes what is
        # left of its bound, which an exporter stuck mid-request overran by up
        # to 5 s (review of #2016). An exporter still running is abandoned as
        # after any timed-out join; its ops are on disk, and the worker kicked
        # below delivers them.
        if self._exporter is not None:
            if timeout is None:
                self._exporter.close()
            else:
                self._exporter.close(timeout=max(0.0, min(5.0, timeout)))
            self._exporter = None
            try:
                self._kick_drainer(force=True)
            except Exception:  # noqa: BLE001 -- a close may never raise
                pass
        if self._seal_producer_on_close:
            try:
                self.journal.seal_producer()
            except Exception:  # noqa: BLE001 -- accounting must never block close
                pass
        # Beats ride this client's transport; leaving them running would spin a
        # thread per unfinished run against a closed httpx client every interval.
        for stop in list(self._run_heartbeat_stops):
            stop.set()
        self.transport.close()

    def __enter__(self) -> Client:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()

    # -- fail-open write ----------------------------------------------------
    def write(
        self,
        method: str,
        path: str,
        body: dict | None = None,
        *,
        strict: bool | None = None,
        durable: bool = True,
        sync: bool = False,
        blocking: bool = True,
        raise_permanent: bool | None = None,
        admitted: bool = False,
    ):
        """A data write. In ``async_writes`` mode it is journaled without ever
        touching the network (the outbox drainer delivers it); otherwise it is
        attempted and journaled on failure unless ``strict`` (or ``fail_open``
        is off). Returns the parsed response, or None if it was journaled.

        ``sync=True`` forces the network path even under ``async_writes`` -- for
        the writes whose RESPONSE the caller needs in hand, not eventually. The
        terminal status flip is the one that matters: ``finish()`` drains the
        journal and then closes the run, so a queued close would return no row
        and leave the barrier claiming a delivery it had not made. It keeps the
        fail-open journal fallback, so forcing sync costs latency, never a raise.

        ``blocking=False`` marks a write that must never hold a run's close --
        `finish()` refuses to mark a run terminal while any of its ops are
        undelivered, which is right for data and wrong for a best-effort
        diagnostic that would otherwise decide the run's recorded fate.

        ``durable=False``: attempt directly, RAISE on failure, never touch the
        journal. Under async writes, only for a write that names no run -- the
        hardware rail's content-addressed inventory record. A direct write TO a
        run races the drainer on the server's run-row lock (503
        ``MetricWriteBusy``), so under async writes the rail's points and its
        env_ref PATCH go through :meth:`_enqueue_best_effort` (plan 0.3); under
        sync writes (`PROBE_ASYNC=0`) nothing drains until `finish()`, so the
        rail writes to the run directly here, as it did before.

        ``raise_permanent=True`` narrows fail-open to what fail-open is FOR: a
        failure that could succeed later. A 4xx refusal cannot -- the journal
        replays it until the drainer dead-letters it -- so queueing one converts
        an error the caller could act on into a success it cannot. A notes
        append against a full document was exactly that: the CLI printed
        "appended to project notes", exited 0, and the paragraph was never
        stored. Transient failures and auth blocks still journal, which is the
        resilience the fail-open path exists for. NOT the default: the metric
        rail must not raise into a training loop over one refused point, which
        is the same reason ``clamp_notes`` truncates at the ingest door instead
        of 422-ing the envelope. None (not passed) takes the client's own
        `raise_permanent`, which the CLI turns on for every write it makes
        (lineage plan L14) and nothing else does.

        A 409 carrying ``existing_id`` raises under it too. The outbox reads
        that answer as its OWN earlier delivery landing ("idempotent") -- true
        of a replay, never of this first attempt: the transport does not
        re-send a write that may have landed, and a daemon retry's
        Idempotency-Key replays the stored answer, not a 409. Queued, a
        duplicate `edge add` or a second genealogy parent drained as delivered
        and the CLI printed `null`, exit 0.

        A write that fails and falls back to the outbox (or is lost with it)
        is handed to `on_undelivered` when one is set (the CLI's).

        ``admitted=True``: if this write ends up journaled, the queue-length cap
        and the free-space floor do not refuse it (`Journal.append_http`). Only
        for a run's terminal status: its fail-open copy used to be refused by
        the same full queue that made it fail open (review of #2014, H5b)."""
        # Renew a DETACHED run's auto-update lease off its own traffic. This is
        # the single funnel every SDK write passes through, which is what makes
        # the renewal complete rather than sprinkled: a detached run
        # (heartbeat=False) has no process of ours to hold an flock, so without
        # this its 30-minute lease expires under a longer job and an upgrade
        # lands mid-run. No-ops for process-bound runs, which hold an flock and
        # have no lease file, and skips the write until the lease is half spent.
        _touch_run_lease(path, base_url=self.settings.base_url, spool_dir=str(self.journal.dir))
        from . import unstorable

        # Structural errors cannot be journaled. Policy errors can: preserve a
        # permanent refusal before scrubbing can remove the offending identity.
        body = unstorable.normalize_json(body)
        # Points the server cannot store (a step past int64, a key past its
        # index row size) are 500s the outbox would retry for a day, holding
        # the run's later writes: dropped here, every metric writer's door
        # (review of #2053).
        body, unstorable_reasons = unstorable.drop_unstorable_points(method, path, body)
        if unstorable_reasons:
            _warn_unstorable(unstorable_reasons)
            if not body.get("points"):
                return None
        if raise_permanent is None:
            raise_permanent = bool(getattr(self, "raise_permanent", False))
        strict = (not self.fail_open) if strict is None else strict
        validation_error = None
        try:
            unstorable.validate_nuls(body, path=path, method=method)
        except errors.ValidationError as exc:
            if strict or raise_permanent or not durable:
                raise
            validation_error = str(exc)
        if self._redact is not None and body is not None:
            body = self._redact(body)
        # The runs this process writes: the delivery notices name only
        # trouble of these (plan 1.7).
        run_ref = run_ref_for_path(path)
        runs = self.__dict__.get("_my_runs")
        if run_ref is not None and runs is not None:
            runs.add(run_ref)
        if "_attempted_writes" in self.__dict__:
            self._attempted_writes += 1  # the report's denominator (plan 1.12)
        # `scrub_body`: `default_scrub`, minus the ISO timestamps `Run.log`
        # stamps on every point (plan 1.4), which cannot hold a credential.
        from .stamp_scrub import scrub_body

        body = scrub_body(body)
        if validation_error is not None:
            if self._enqueue(
                method,
                path,
                body,
                blocking=blocking,
                validation_error=validation_error,
                prepared=True,
            ):
                self._after_enqueue()
            return None
        if not durable:
            resp = self.transport.request(method, path, json_body=body)
            return resp.json() if resp.content else None
        # Resolve `strict` BEFORE the async branch. It used to be read after,
        # which meant async mode silently downgraded a strict write into a
        # queued replay -- harmless while async was opt-in, a data-loss bug the
        # moment it became the default: Miles passes strict=True and then
        # `queue.acknowledge()` DELETES its durable record on the strength of
        # not seeing an exception, so a queued write erased the only copy.
        #
        # strict means "fail loudly, never journal", which is a demand for the
        # network. It therefore implies sync, and an explicit strict=True beats
        # async mode rather than being quietly overruled by it.
        strict = (not self.fail_open) if strict is None else strict
        if self.async_writes and not sync and not strict:
            if self._send_instead_of_queueing(method, path, body):
                return None
            if self._enqueue(
                method,
                path,
                body,
                blocking=blocking,
                prepared=True,
                direct_ok=True,
                admitted=admitted,
            ):
                self._after_enqueue()
            return None
        try:
            resp = self.transport.request(method, path, json_body=body)
            # A 2xx carrying a non-JSON body raises ValueError, not RosError --
            # `Transport.delete` already defends against exactly this ("an
            # ingress/CDN HTML interstitial in front of the API"). Through the
            # door every write uses, that interstitial used to take down the
            # training loop instead of spooling.
            if not resp.content:
                return None
            try:
                return resp.json()
            except ValueError:
                return None
        except errors.RosError as exc:
            if strict:
                raise
            if raise_permanent and _journal_classify(exc) in ("permanent", "idempotent"):
                raise
            landed = self._enqueue(method, path, body, blocking=blocking, prepared=True, admitted=admitted)
            self._note_undelivered(method, path, exc, queued=landed)
            return None

    #: How many undelivered writes a hooked client keeps (`undelivered_writes`).
    UNDELIVERED_KEPT = 32

    def _note_undelivered(self, method: str, path: str, exc: BaseException, *, queued: bool) -> None:
        """Hand a write that failed and fell back to the outbox (`queued`), or
        was lost with it, to `on_undelivered`, and keep it; nothing at all
        without a hook. Never raises: it runs on the fail-open path, whose
        whole promise is not raising."""
        report = getattr(self, "on_undelivered", None)
        if report is None:
            return
        try:
            text = str(exc).strip()
            # httpx timeouts stringify EMPTY: the type is then all there is to say.
            error = f"{type(exc).__name__}: {text}" if text else type(exc).__name__
            entry = {"method": method, "path": path, "error": error[:300], "queued": bool(queued)}
            self.undelivered_writes.append(entry)
            self.undelivered_count += 1
            report(entry)
        except Exception:  # noqa: BLE001 -- a report about a write never breaks the write
            pass

    #: How long a direct send (below the free-space floor, plan 1.5) may hold
    #: the training thread, and how long after a failed one none is tried:
    #: from the first wait, doubling to the ceiling.
    DIRECT_SEND_TIMEOUT_SECONDS = 5.0
    DIRECT_SEND_BACKOFF = (60.0, 600.0)
    #: Above this many queued ops, no direct send is tried (see
    #: `_send_instead_of_queueing`).
    DIRECT_SEND_MAX_QUEUED = 1000

    def _send_instead_of_queueing(
        self, method: str, path: str, body: dict | None, *, out_of_space: bool = False
    ) -> bool:
        """Below the outbox's free-space floor, deliver ``body`` directly
        rather than drop it (plan 1.5). True when it was delivered.

        Only while the run has NOTHING queued: the metric insert keeps the
        first write of a (series, step), so a direct `loss=2` at step 10 landing
        ahead of a queued `loss=1` at step 10 would replace the original (Codex,
        round 2). Bounded: at most `DIRECT_SEND_TIMEOUT_SECONDS` on the
        training thread, and after a failure none for a minute, doubling to
        ten. Otherwise the write is queued -- which, under the floor, the
        journal refuses and the caller drops with a capture gap, as before.

        ``out_of_space``: the append itself just failed with ENOSPC/EDQUOT
        (the disk filled between free-space samples, or the floor is off).

        Never for a queue only `probe sync` drains (``_drains_by_hand``: an
        offline run, plan 2.12, which must not touch the network at all)."""
        if getattr(self, "_drains_by_hand", False):
            return False
        journal = self.journal
        if not out_of_space:
            try:
                if journal.below_floor() is None:
                    return False
            except Exception:  # noqa: BLE001 -- the journal decides on its own below
                return False
        from .journal import RunOps

        run_ref = run_ref_for_path(path)
        now = time.monotonic()
        with self._direct_lock:
            if run_ref is None or now < self._direct_closed_until:
                return False
        try:
            # Proving the run clear parses queued op files the first time it
            # is asked (on this thread). A deep queue means delivery is behind
            # anyway: then no direct send, and no seconds-long first scan
            # (review of #2054).
            status = Journal.read_status(journal.dir, include_receipts=False) or {}
            if int(status.get("pending") or 0) > self.DIRECT_SEND_MAX_QUEUED:
                return False
            with self._direct_lock:
                lane = self._lanes.get(run_ref)
                if lane is None:
                    # Every queue of the outbox: a write of this run queued
                    # under another credential (#2035) is overtaken just the
                    # same by a direct send (#2041 round 4).
                    lane = self._lanes[run_ref] = RunOps(
                        journal, run_ref, blocking_only=False, queues=journal.outbox_queues()
                    )
            if lane.pending():
                # Queued ops hold this write back, and on a full disk it will
                # be dropped before it is ever queued -- so no enqueue will
                # kick the drainer. Kick it here (throttled), or an op whose
                # worker already exited strands and every later write of the
                # run is dropped behind it (7-day soak, 0.200.2).
                self._kick_drainer()
                return False
        except Exception:  # noqa: BLE001 -- cannot prove the run is clear: queue it
            return False
        from .transport import deadline_scope

        try:
            with deadline_scope(now + self.DIRECT_SEND_TIMEOUT_SECONDS):
                self.transport.request(method, path, json_body=body)
        except Exception as exc:  # noqa: BLE001 -- the write falls back to the queue
            try:
                # Only a failure that says the SERVER is down or refusing
                # everyone opens the breaker. A 422 or 409 is about this write:
                # closing direct sends for every run over it dropped every good
                # write under low disk for minutes (review of #2054).
                if _journal_classify(exc) in ("transient", "auth"):
                    with self._direct_lock:
                        self._direct_failures += 1
                        first, ceiling = self.DIRECT_SEND_BACKOFF
                        wait = min(ceiling, first * 2 ** (self._direct_failures - 1))
                        self._direct_closed_until = time.monotonic() + wait
            except Exception:  # noqa: BLE001 -- the breaker may never raise out of write()
                pass
            return False
        with self._direct_lock:
            self._direct_failures = 0
            self.direct_sends += 1
        return True

    def _enqueue(
        self,
        method: str,
        path: str,
        body: dict | None,
        *,
        blocking: bool = True,
        validation_error: str | None = None,
        prepared: bool = False,
        admitted: bool = False,
        direct_ok: bool = False,
    ) -> bool:
        """Journal one op. Returns whether it landed; NEVER raises for a
        failure of ours. A KeyboardInterrupt or SystemExit propagates.

        ``direct_ok`` (the async write path): when the append fails for want of
        space, try `_send_instead_of_queueing` before dropping (plan 1.5).

        ``prepared=True`` only from `write`, whose body is already normalized,
        NUL-checked and scrubbed: the journal then skips doing all three again
        (plan 1.3). Any other caller (the CLI's reference door) hands a raw
        body, and the journal scrubs it.

        Async-by-default moved the per-write failure surface from the network to
        the disk, and the disk was left unguarded -- so ENOSPC on the state
        partition, a read-only or full `XDG_STATE_HOME`, a stale NFS handle, or
        an `flock` that returns ENOSYS (Lustre mounted without `-o flock`, some
        container overlays, several FUSE mounts) raised a raw OSError straight
        out of `run.log()`. That is the original bug with the substrate swapped:
        telemetry killing a training step.

        Losing a datapoint is the correct outcome when the outbox itself is
        broken. The gap is recorded where the record belongs -- in the journal's
        own accounting when it can be written, and in a warning when it cannot.

        It is ALSO counted on `dropped_writes`, because the return value dies
        here: `write()` discards it and returns None either way, so a caller one
        layer up cannot tell a queued write from a dropped one. A CLI that
        printed "queued" on a dropped write would be reporting success for data
        that reached nothing -- see `Client.dropped_writes`.
        """
        try:
            options: dict[str, Any] = (
                {"validation_error": validation_error} if validation_error is not None else {}
            )
            if prepared:
                options["_prepared"] = True
            if admitted:
                options["admitted"] = True
            self.journal.append_http(method, path, body, blocking=blocking, **options)
            return True
        except (KeyboardInterrupt, SystemExit):
            # A Ctrl-C (or a `sys.exit`) landing mid-append is the user stopping
            # the process, not a broken outbox: counting it a dropped write let
            # training carry on past the Ctrl-C, and closed an interrupted run
            # with a drop notice. Nothing is left half-written for it to clean:
            # `write_text_atomic` unlinks its temp file on the way out, and the
            # op file either landed whole (it delivers) or not at all.
            raise
        except BaseException as enqueue_error:  # noqa: BLE001
            if (
                direct_ok
                and isinstance(enqueue_error, OSError)
                and enqueue_error.errno in _OUT_OF_SPACE
                and self._send_instead_of_queueing(method, path, body, out_of_space=True)
            ):
                return True
            self.dropped_writes += 1
            try:
                # Once per drop: a refusal at the cap was already recorded by
                # the journal itself (review of #2014: each drop rewrote the
                # producer file twice).
                if not getattr(enqueue_error, "gap_recorded", False):
                    self.journal.note_capture_gap(str(enqueue_error))
            except Exception:  # noqa: BLE001 -- the journal is the thing that broke
                pass
            # One line per kind, then at most one per 5 min with the running
            # count (plan 1.7): a warning per drop was 44 lines for 50 drops.
            self._note_drop(f"{method} {path}: {_diagnostics.describe(enqueue_error)}")
            # The warning reaches the operator's terminal and nothing else. This
            # branch is DATA LOSS -- the write reached neither the server nor the
            # journal -- so it is exactly the failure that must not stay local.
            _capture_swallowed(
                enqueue_error,
                site="client.enqueue_dropped",
                base_url=self.settings.base_url,
                spool_dir=str(self.journal.dir),
            )
            return False

    def _enqueue_upload(self, **kwargs) -> dict | None:
        """Journal one byte upload. Returns the journal's result, or None when
        it could not be queued; NEVER raises for a failure of ours.

        The symmetric sibling of :meth:`_enqueue`. Both surfaces that queue
        uploads -- this client and the CLI -- go through here so the
        "telemetry must not raise into the caller" rule has ONE implementation
        rather than one per caller. The CLI used to call
        ``journal.append_upload`` directly, which is why the guard `_enqueue`
        added for the http path never covered the upload path.

        Two differences from `_enqueue`, both deliberate:

        ``Exception``, not ``BaseException``. `append_upload` does a full byte
        copy, so a Ctrl-C during a multi-GB checkpoint lands here far more often
        than anywhere else in the SDK, and swallowing it would leave the user
        unable to interrupt their own upload. ``Exception`` still covers every
        failure of ours -- ENOSPC, a read-only `XDG_STATE_HOME`, `flock` ENOSYS
        on Lustre/FUSE, `OutboxFull`, and the serialization and redaction errors
        a narrower tuple would miss -- while KeyboardInterrupt and SystemExit
        pass through untouched. (`_enqueue` passes those two through as well:
        a Ctrl-C mid-append used to be counted a dropped write.)

        Redaction happens HERE, before the bytes reach the journal, and it is
        UNCONDITIONAL rather than gated on ``self._redact``. That is the one
        place this client departs from "the caller owns redaction", and it is
        deliberate: `write()` scrubs a payload on its way to the NETWORK, where
        the caller's preference is the whole story, while this writes to durable
        local disk that a dead-lettered op keeps in `failed/` indefinitely. An
        SDK caller who passed no redactor was asking not to reshape their API
        payloads; they were not asking for their `--meta` secrets to be parked
        on the filesystem forever. A caller-supplied ``_redact`` still runs, on
        top.

        `notes` gets `scrub_text`, not `default_scrub`. The two are not
        interchangeable: `default_scrub` redacts by KEY NAME, which is right for
        a structured payload and wrong for prose -- `notes` is not a sensitive
        key, so a bare token or a `PROBE_TOKEN=...` assignment inside the text
        sails straight through it. `scrub_text` is the value-level pass built
        for exactly that (redaction.py's own comment says so). String leaves
        inside `meta` get the same treatment for the same reason.
        """
        check_upload(kwargs.get("src_path"))
        try:
            # INSIDE the try, not before it. Redaction is arbitrary code -- the
            # caller's especially -- and one that raises would otherwise escape a
            # method whose contract is that it never raises, taking out the
            # caller's synchronous fallback with it.
            from .redaction import default_scrub, scrub_text

            notes = kwargs.get("notes")
            if isinstance(notes, str):
                kwargs["notes"] = scrub_text(notes)
            meta = kwargs.get("meta")
            if isinstance(meta, dict):
                scrubbed = default_scrub(meta)
                if isinstance(scrubbed, dict):
                    # default_scrub caught the sensitive KEYS; scrub_text catches
                    # a secret sitting in prose under an innocent one.
                    scrubbed = {
                        k: (scrub_text(v) if isinstance(v, str) else v) for k, v in scrubbed.items()
                    }
                kwargs["meta"] = scrubbed
            if self._redact is not None:
                for field in ("meta", "notes"):
                    value = kwargs.get(field)
                    if not isinstance(value, dict):
                        continue
                    # Only structured values go to a caller redactor: its
                    # declared type is dict -> dict, and round-tripping a string
                    # through a wrapper key silently DROPPED the value whenever
                    # the redactor returned an allowlisted subset.
                    kwargs[field] = self._redact(value)
            kwargs = default_scrub(kwargs)
            return self.journal.append_upload(**kwargs)
        except Exception as enqueue_error:  # noqa: BLE001 -- see the docstring
            self.dropped_writes += 1
            try:
                if not getattr(enqueue_error, "gap_recorded", False):
                    self.journal.note_capture_gap(str(enqueue_error))
            except Exception:  # noqa: BLE001 -- the journal is the thing that broke
                pass
            self._note_drop(
                f"upload {kwargs.get('name')!r}: {_diagnostics.describe(enqueue_error)}"
            )
            _capture_swallowed(
                enqueue_error,
                site="client.enqueue_upload_dropped",
                base_url=self.settings.base_url,
                spool_dir=str(self.journal.dir),
            )
            return None

    #: How often a writing process reads status.json for delivery trouble
    #: (plan 1.7); between reads it costs one monotonic check per write.
    NOTICE_POLL_SECONDS = 15.0
    #: A queue whose oldest write has waited this long is "stalled".
    STALLED_AFTER_SECONDS = 600.0

    def _init_delivery_notices(self) -> None:
        """The baseline the delivery poller compares against (plan 1.7): what
        was already dead-lettered or auth-blocked before this client existed
        is not news."""
        from .journal import _rank_suffix
        from .safe_warn import DeliveryNotices

        try:
            suffix = _rank_suffix()
        except Exception:  # noqa: BLE001
            suffix = None
        self._notices = DeliveryNotices(prefix=f"probe[{suffix}]" if suffix else "probe")
        self._notice_polled_at = self._notices.clock()
        self._my_runs: set[str] = set()
        try:
            status = Journal.read_status(self.journal.dir) or {}
            recent = self.journal.recent_dead_letters()
        except Exception:  # noqa: BLE001
            status, recent = {}, []
        self._dead_seen = {str(entry.get("op_id")) for entry in recent}
        self._failed_seen = int(status.get("failed") or 0)
        self._auth_seen = self._auth_blocked_since(status)
        self._auth_block_started(self._auth_seen)
        self._pending_seen = int(status.get("pending") or 0)
        self._delivered_seen = self._own_delivered()
        # Plan 1.12: what this process's delivery report counts, and what its
        # last report already said (the report carries deltas).
        self._attempted_writes = 0
        self._dead_lettered_mine = 0
        self._dead_lettered_by_status: dict[str, int] = {}
        self._last_status: dict = {}
        self._reported: dict = {}
        self._reported_at = self._notice_polled_at

    def _auth_blocked_since(self, status: dict) -> str | None:
        """When delivery of this client's writes was last refused (401/403),
        or None: the queue-wide block, or THIS client's credential among the
        ones a drain set aside (`journal.auth_blocked_since`)."""
        from .journal import auth_blocked_since

        mine = set(self.__dict__.get("_credential_fingerprints") or ())
        mine |= set(self.__dict__.get("_ingest_fingerprints") or ())
        return auth_blocked_since(status, mine)

    def _auth_block_started(self, blocked: str | None) -> str | None:
        """When the current, unbroken block began, as far as this client has
        seen: the first `_auth_blocked_since` stamp of it. A drain rewrites
        that stamp at every refusal (the credential cooldown counts from the
        latest), so "stopped for N min" read from it always said 0-5 min."""
        if not blocked:
            self._auth_first = None
            return None
        first = self.__dict__.get("_auth_first")
        if first is None:
            self._auth_first = first = blocked
        return first

    def _own_delivered(self) -> int | None:
        """How many of this client's queued writes have landed so far (its
        producer record, one small file), or None without a producer."""
        producer_id = getattr(self.journal, "_producer_id", None)
        if not producer_id:
            return None
        try:
            record = self.journal._read_producer_locked(producer_id)
            return int(record.get("delivered") or 0)
        except Exception:  # noqa: BLE001
            return None

    def _note_drop(self, detail: str) -> None:
        """One dropped write, through the rate-limited notices (plan 1.7)."""
        notices = getattr(self, "_notices", None)
        if notices is None:  # a Client built without __init__ (a test double)
            _diagnostics.warn(f"probe: dropped a write before it reached the outbox: {detail}")
            return
        notices.note(notices.DROP, "{n} write(s) dropped before they reached the outbox",
                     detail=detail)

    def _poll_delivery(self, *, force: bool = False) -> None:
        """Say, in THIS process, when this process's writes are in trouble:
        dead letters of its own runs, an auth block, a queue stalled for 10
        minutes. At most one status.json read per `NOTICE_POLL_SECONDS`.
        Never raises. Not for a queue only `probe sync` drains (an offline run,
        plan 2.12): nothing delivers it by design, so "stalled" would be noise."""
        if getattr(self, "_drains_by_hand", False):
            return
        try:
            now = self._notices.clock()
            if not force and now - self._notice_polled_at < self.NOTICE_POLL_SECONDS:
                return
            self._notice_polled_at = now
            status = Journal.read_status(self.journal.dir) or {}
            notices = self._notices
            recent = self.journal.recent_dead_letters()
            fresh = [e for e in recent if str(e.get("op_id")) not in self._dead_seen]
            self._dead_seen = {str(e.get("op_id")) for e in recent}
            mine = [e for e in fresh if e.get("run_ref") in self._my_runs]
            self._dead_lettered_mine += len(mine)
            for entry in mine:
                code = str(entry.get("status") or "none")
                self._dead_lettered_by_status[code] = self._dead_lettered_by_status.get(code, 0) + 1
            self._last_status = status
            if mine:
                notices.note(
                    notices.DEAD_LETTER,
                    "{n} of this process's writes were permanently rejected by the "
                    "server (dead-lettered)",
                    count=len(mine),
                    detail=str(mine[-1].get("error") or "")[:200] or None,
                )
            # Dead letters no status entry accounts for were written by a worker
            # that predates 1.7 (it names no runs): the machine's, said so.
            failed = int(status.get("failed") or 0)
            unnamed = failed - self._failed_seen - len(fresh)
            if unnamed > 0:
                notices.note(
                    notices.DEAD_LETTER,
                    "{n} write(s) in this machine's outbox were dead-lettered",
                    count=unnamed,
                )
            self._failed_seen = failed
            blocked = self._auth_blocked_since(status)
            started = self._auth_block_started(blocked)
            if blocked and blocked != self._auth_seen:
                # The elapsed time is in the text: Python's default warning
                # filter shows an identical message from one place only once,
                # so a reminder that never changed never repeated (review of
                # #2055).
                minutes = _minutes_since(started)
                notices.note(
                    notices.AUTH_BLOCK,
                    "delivery has been stopped"
                    + (f" for {minutes} min" if minutes is not None else "")
                    + f": the server refused this machine's credential (401/403) since {started}",
                )
            oldest = status.get("oldest_pending")
            pending = int(status.get("pending") or 0)
            # Progress since the last look -- this client's writes landing, or
            # the queue shrinking -- means a drain is working through it, if
            # slowly (a long recovery pass after an outage), not stalled
            # (review of #2055).
            delivered = self._own_delivered()
            progressed = (
                delivered is not None
                and self._delivered_seen is not None
                and delivered > self._delivered_seen
            ) or pending < self._pending_seen
            self._delivered_seen, self._pending_seen = delivered, pending
            if pending and oldest and not progressed:
                from datetime import datetime, timezone

                waited = (
                    datetime.now(timezone.utc) - datetime.fromisoformat(str(oldest))
                ).total_seconds()
                if waited >= self.STALLED_AFTER_SECONDS:
                    notices.note(
                        notices.STALLED,
                        f"{pending} write(s) are queued and the oldest has waited "
                        f"{int(waited // 60)} min: the server is not taking them",
                    )
            if not force and now - self._reported_at >= self.DELIVERY_REPORT_SECONDS:
                self._report_delivery()
        except Exception:  # noqa: BLE001 -- a notice may never break a write
            pass

    #: How often a writing process reports its delivery counts (plan 1.12).
    DELIVERY_REPORT_SECONDS = 900.0

    def _report_delivery(self, *, final: bool = False) -> None:
        """Send this process's delivery counts since its last report to our
        telemetry (plan 1.12): counts only, never a key, body, name or path;
        nothing when the telemetry opt-out is set or the backend is not ours,
        and never for a queue only `probe sync` drains (an offline run, plan
        2.12, which must not touch the network). Skipped when there is
        nothing to say, except at a close.

        A periodic report goes out from a daemon thread (its first send
        imports the telemetry module and resolves an identity, which must not
        cost the training loop). A CLOSE's report is handed to the telemetry
        sender on the CALLING thread, after re-reading the outbox's status:
        the interpreter often shuts down milliseconds after `finish()`, too
        soon for a thread to start or register the sender's exit flush, and
        the 15 s poll's numbers can be stale (review of #2056). During
        interpreter exit (the auto-close at exit) it is flushed right away,
        since the sender's own exit flush may already have run."""
        if getattr(self, "_drains_by_hand", False):
            return
        try:
            if final:
                self._poll_delivery(force=True)
            now = self._notices.clock()
            status = self._last_status or {}
            counts = {
                "attempted": self._attempted_writes,
                "dropped": int(self.dropped_writes or 0),
                "direct_sends": int(self.direct_sends or 0),
                "dead_lettered": self._dead_lettered_mine,
            }
            delta = {k: v - int(self._reported.get(k, 0)) for k, v in counts.items()}
            by_status = {
                code: n - int((self._reported.get("dead_lettered_by_status") or {}).get(code, 0))
                for code, n in self._dead_lettered_by_status.items()
            }
            by_status = {code: n for code, n in by_status.items() if n > 0}
            if not final and not any(delta.values()):
                return
            props: dict[str, Any] = {
                **delta,
                "dead_lettered_by_status": by_status or None,
                "pending": int(status.get("pending") or 0),
                "oldest_pending_s": _age_seconds(status.get("oldest_pending")),
                "auth_blocked_s": _age_seconds(
                    self._auth_block_started(self._auth_blocked_since(status))
                ),
                "final": final,
                "interval_s": round(now - self._reported_at, 1),
            }
            self._reported = {
                **counts, "dead_lettered_by_status": dict(self._dead_lettered_by_status)
            }
            self._reported_at = now
            base_url = self.settings.base_url

            def send(flush: bool = False) -> None:
                try:
                    _telemetry.emit_delivery_summary(base_url=base_url, flush=flush, **props)
                except Exception:  # noqa: BLE001 -- observability is a bystander
                    pass

            if final:
                send(flush=not threading.main_thread().is_alive())
            else:
                threading.Thread(target=send, name="probe-delivery-report", daemon=True).start()
        except Exception:  # noqa: BLE001
            pass

    def _after_enqueue(self) -> None:
        """Wake delivery for a just-journaled op (F1/F2). A DEAD exporter is
        not respawned: the only thing that kills one is an auth block, and
        respawning per write would retry rejected credentials forever -- the
        zombie-uploader pitfall. Re-login + `probe outbox retry` resumes."""
        self._poll_delivery()
        if self._drain_interval is not None:
            exporter = self._exporter
            if exporter is None:
                with self._exporter_lock:
                    exporter = self._exporter
                    if exporter is None:
                        from .exporter import OutboxExporter

                        # Its thread outlives any patience scope a write here
                        # happens inside (init); see `_wrap_run`.
                        with without_patience():
                            exporter = OutboxExporter(self, self._drain_interval)
                            self._learn_identity()
                        self._exporter = exporter
            exporter.wake()
            return
        self._kick_drainer()

    #: The most an exiting process spends promoting its own waiting uploads;
    #: a scan already started finishes, none starts after it.
    _EXIT_PROMOTE_SECONDS = 60.0

    def _promote_waiting_at_exit(self, run_ref: str) -> None:
        """Make sure an upload this process queued for a background credential
        scan is promoted even if no worker could be started (a frozen or
        embedded interpreter): at exit, promote what is still waiting for THIS
        process's runs -- not other processes' in a shared journal -- within
        `_EXIT_PROMOTE_SECONDS`, then kick delivery the way `_kick_drainer`
        would. Registered once. Normally a no-op: the worker or `finish()` got
        there first."""
        runs = self.__dict__.setdefault("_waiting_exit_runs", set())
        runs.add(run_ref)
        if len(runs) > 1 or getattr(self, "_waiting_exit_armed", False):
            return
        self._waiting_exit_armed = True
        journal_dir = str(self.journal.dir)
        spawn = self._default_transport and self._auto_drain
        budget = self._EXIT_PROMOTE_SECONDS

        def promote() -> None:
            from . import outbox_worker
            from .journal import Journal

            try:
                journal = Journal(journal_dir)
                deadline = time.monotonic() + budget
                promoted = 0
                for ref in sorted(runs):
                    left = deadline - time.monotonic()
                    if left <= 0:
                        break
                    promoted += journal.promote_waiting(run_ref=ref, timeout=left)
                if spawn and (promoted or journal.waiting()):
                    outbox_worker.maybe_spawn(journal_dir)
            except Exception:  # noqa: BLE001 -- exit must not raise; items stay queued
                pass

        _at_exit(promote)

    def _kick_drainer(self, *, force: bool = False) -> None:
        """Wake the detached outbox worker (parity F1). Throttled: this runs
        on every async write and a training loop logs hundreds of points a
        second; ``maybe_spawn`` is O(1) but not free. Best-effort by design --
        ``finish()``/`probe run end` is the delivery barrier, this is latency.

        ``force`` (deferred finish, F3): skip the mode gate and the throttle
        -- a queued terminal status must not have its one kick swallowed --
        but never the transport gate; a worker cannot replay an injected one.

        The throttle arms ONLY on an actual spawn (prod smoke 2026-08-06): a
        probe that declined because a worker was alive must not suppress the
        next write's probe, or a worker exiting inside the window strands the
        writer's last op if the writer then dies. While a worker lives, every
        write pays one O(1) probe -- a status read and a lock check."""
        if not self._default_transport:
            return
        if not (self._auto_drain or force):
            return
        if not force and (time.monotonic() - self._drainer_kicked_at < self._drainer_kick_interval):
            return
        from . import outbox_worker

        try:
            if outbox_worker.maybe_spawn(str(self.journal.dir)) and not force:
                self._drainer_kicked_at = time.monotonic()
        except Exception:  # noqa: BLE001 -- best-effort; run end is the barrier
            pass

    def _enqueue_best_effort(self, method: str, path: str, body: dict | None) -> bool:
        """Queue a best-effort write to a run (the hardware rail's door under
        async writes; plan 0.3, D2). Not public API.

        A write that goes around the journal lands on the run row while the
        drainer is delivering the run's own metrics, and the server's metric
        insert takes that row NOWAIT, so the collision answers 503: with
        hardware on, ``finish()`` raised on 4 of 6 short runs (0 of 6 with
        ``PROBE_HW=0``). Queued here, the write drains FIFO with the run's
        other ops, one request at a time.

        ``blocking=False``: it never holds the run's close, so a hardware op
        that dead-letters cannot decide how the run ends.

        Returns False when the journal REFUSED the op for room (``OutboxFull``:
        the op ceiling or the free-disk floor). The op is dropped on purpose:
        spool space belongs to training metrics, and a refusal retried from a
        buffer is only refused again. It is not the user's data, so it prints
        nothing, records no capture gap and is not counted on
        ``dropped_writes`` (``best_effort=True``).

        RAISES when the journal is broken (read-only state dir, ENOSPC mid-write,
        ``flock`` ENOSYS): the caller keeps its own bounded buffer for exactly
        this, and retrying next tick can succeed where retrying a refusal
        cannot.
        """
        from .journal import OutboxFull

        _touch_run_lease(path, base_url=self.settings.base_url, spool_dir=str(self.journal.dir))
        if self._redact is not None and body is not None:
            body = self._redact(body)
        try:
            # append_http normalizes, NUL-checks (a bad body becomes a
            # rejected_http op that dead-letters) and scrubs, as write() does.
            self.journal.append_http(method, path, body, blocking=False, best_effort=True)
        except OutboxFull:
            return False
        self._after_enqueue()
        return True

    def _credential_queue_name(self, stamp: dict) -> str:
        """Which credential queue this client writes to: named by the key its
        ENVIRONMENT holds, so a kick from a shell with that environment finds
        it (`outbox_worker._env_fingerprints`). An ingest-only job
        (`PROBE_INGEST_TOKEN`, its personal token from the stored login) goes
        by its ingest token's fingerprint (#2041 round 4); otherwise the
        stamp's fingerprint."""
        token, ingest = self.settings.token, self.settings.ingest_token
        if (
            ingest
            and ingest == os.environ.get("PROBE_INGEST_TOKEN")
            and not (token and token == os.environ.get("PROBE_TOKEN"))
        ):
            return credential_fingerprint(None, ingest) or stamp["fingerprint"]
        return stamp["fingerprint"]

    def _is_the_stored_login(self, context_name: str | None) -> bool:
        """Whether this client's credential IS the context's stored login, by
        value, however it arrived (a `PROBE_TOKEN` set to the same token, say).
        Its writes then stay in the shared queue: every drainer, older ones
        included, sends them with that same token, and they keep their order
        against the stored login's own writes -- a close queued there cannot
        overtake them (#2041 round 3)."""
        token, ingest = self.settings.token, self.settings.ingest_token
        try:
            stored = config_module.load_context(context_name)
        except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
            return False
        if not (token or ingest):
            return False
        return (not token or token == stored.get("token")) and (
            not ingest or ingest == stored.get("ingest_token")
        )

    def _credential_stamp(self, context_name: str | None) -> dict | None:
        """What every op this client queues records about its credential:
        where it came from and a fingerprint of it, never the token (#2035).

        Told apart by VALUE, not by which argument carried it: a token equal to
        this environment's ``PROBE_TOKEN`` is an env credential however it got
        here, and one equal to this context's stored login is that login. Only
        a stored-login op may later go out with a NEW login of its context (a
        re-login); see `journal._settings_for_op`.
        """
        token, ingest = self.settings.token, self.settings.ingest_token
        fingerprint = credential_fingerprint(token, ingest)
        if fingerprint is None:
            return None
        env = {k: os.environ.get(k) for k in ("PROBE_TOKEN", "PROBE_INGEST_TOKEN")}
        try:
            stored = config_module.load_context(context_name)
        except Exception:  # noqa: BLE001 -- an unreadable config stores nothing
            stored = {}
        if (token and token == env["PROBE_TOKEN"]) or (ingest and ingest == env["PROBE_INGEST_TOKEN"]):
            source = CredentialSource.ENV
        elif (not token or token == stored.get("token")) and (
            not ingest or ingest == stored.get("ingest_token")
        ):
            source = CredentialSource.CONFIG
        else:
            source = CredentialSource.CODE
        stamp = {"source": source.value, "fingerprint": fingerprint}
        # `/ingest` writes go out with the ingest token: named apart (#2041
        # re-review), so a drainer holding another ingest token cannot match.
        ingest_fingerprint = credential_fingerprint(None, ingest)
        if ingest_fingerprint:
            stamp["ingest_fingerprint"] = ingest_fingerprint
        # The account behind a stored login, as the sign-in recorded it -- only
        # when recorded for THIS token. A drainer may send a stored-login write
        # with a LATER login of the context only if that login is the same
        # account (`journal._settings_for_op`), and this is what it compares.
        recorded = stored.get("identity") if source == CredentialSource.CONFIG else None
        if (
            isinstance(recorded, dict)
            and recorded.get("fingerprint") == fingerprint
            and recorded.get("customer_id")
            and recorded.get("user_id")
        ):
            stamp["customer_id"] = str(recorded["customer_id"])
            stamp["user_id"] = str(recorded["user_id"])
        return stamp

    def _stamp_account(self, token: str | None, who: tuple[str, str], *, adopt: bool = False) -> None:
        """Record in this client's credential stamp which account ``token``
        belongs to, so the writes it queues from now on carry it (#2041 review).

        ``adopt`` is a refresh (plan 2.7) that verified ``token`` as the same
        account: the stamp moves to the new token's fingerprint. Otherwise the
        stamp must already name ``token``; a stamp for another credential is
        left alone. Replaces the stamp dict whole, never mutates it: an append
        on another thread may be serialising the old one."""
        context = self.journal.context
        stamp = context.get("principal") if isinstance(context, dict) else None
        if not isinstance(stamp, dict):
            return
        fingerprint = credential_fingerprint(token, self.settings.ingest_token)
        if fingerprint is None:
            return
        if adopt:
            self._credential_fingerprints.add(fingerprint)
        elif stamp.get("fingerprint") != fingerprint:
            return
        context["principal"] = {
            **stamp,
            "fingerprint": fingerprint,
            "customer_id": who[0],
            "user_id": who[1],
        }

    def _outbox_client_factory(self):
        """client_factory for ``journal.drain`` -- shared by ``flush()`` and
        the in-process exporter (F2).

        Ops pinned to THIS client's endpoint (or unpinned) replay over this
        client -- that keeps fake-transport tests and custom transports
        working. Ops pinned elsewhere resolve their own client from the named
        context, tokens fresh (5A): a context switch between enqueue and flush
        must never deliver to the wrong tenant.

        An op that records which credential queued it replays here only if
        that credential is this client's (#2035): the journal is shared by
        every process on the machine, and another job's op must go out as
        that job, never as whoever happens to flush.
        """

        def factory(context: dict | None):
            base = (context or {}).get("base_url")
            name = (context or {}).get("name")
            mine = (self.journal.context or {}).get("name")
            stamp = (context or {}).get("principal")
            if isinstance(stamp, dict):
                # The key the op's route is sent with (journal.op_credential).
                if (context or {}).get("route") == "ingest":
                    if stamp.get("ingest_fingerprint") not in self._ingest_fingerprints:
                        return None
                elif stamp.get("fingerprint") not in self._credential_fingerprints:
                    return None  # journal.drain looks for the credential that queued it
            # BOTH the endpoint and the context name must match before an op
            # replays over this client's credential: tenants can share one API
            # URL, and an op pinned to another context must resolve its own
            # stored token (red team: base_url alone re-opened wrong-principal
            # replay through the flush path).
            if (not base or base == self.settings.base_url) and (name is None or name == mine):
                return self
            return None  # journal.drain builds one from the pinned context

        return factory

    #: At most one credential re-read per this many seconds (plan 2.7). A
    #: revoked token refuses EVERY request, and a beat, a drain and a flush
    #: asking at once must not each re-read the config and each warn.
    _CREDENTIAL_REFRESH_SECONDS = 30.0

    def refresh_credentials(self, *, refused: str | None = None) -> bool:
        """Re-read this client's API token after the API refused it (plan 2.7).

        A re-login on the box (the wizard's sign-in) revokes the old token, and a
        running job keeps the one it was built with: its heartbeat was refused
        from then on, the refusal was swallowed, and 15 minutes later the
        reaper marked a live run `crashed` (a false crash email for a 3h+ run).

        Only for an AMBIENT client, built from the environment or the stored
        login (`probe.init()`, a bare `Client()`): a token the caller passed is
        never second-guessed. It looks again ONLY where the token came from --
        `PROBE_TOKEN` for an environment token, this context's stored login
        for a stored one -- because the stored login on a shared box may be
        another person's. And it adopts a new token only after `GET /v1/me`
        with it names the SAME team and user as the credential this client
        started with; a login as anyone else is refused, with a warning, and
        the old token is kept.

        At most one re-read per 30 s, under a lock; no network unless the token
        actually changed. One warning when a new token is picked up; one, until
        the next success, when it cannot be.

        ``refused`` is the token the failed request carried: if another thread
        already swapped it, this answers True without reading anything.

        Returns True when a different token is now in use (retry once).
        """
        if not getattr(self, "_ambient_credentials", False):
            return False
        with self._credential_lock:
            if refused is not None and self.settings.token and self.settings.token != refused:
                return True
            now = time.monotonic()
            if now - self._credential_checked_at < self._CREDENTIAL_REFRESH_SECONDS:
                return False
            self._credential_checked_at = now
            candidate, why_not = self._reread_credential()
            if candidate is None or candidate == self.settings.token:
                self._warn_credential_stale(why_not or "there is no newer credential to read")
                return False
            if candidate == self._credential_rejected:
                return False  # already refused as another account's; said so then
            mismatch = self._different_account(candidate)
            if mismatch is not None:
                self._warn_credential_stale(mismatch)
                return False
            self.settings.token = candidate
            self._credential_stale_warned = False
            if self._credential_identity is not None:
                # Same account, verified above: later writes carry the new
                # token's fingerprint, and this client may replay the old one's.
                self._stamp_account(candidate, self._credential_identity, adopt=True)
        _diagnostics.warn(
            "probe: the API refused this process's credential (a re-login revokes the "
            "old one); picked up the new login for the same account and carried on"
        )
        return True

    def _reread_credential(self) -> tuple[str | None, str | None]:
        """(token, None), or (None, why) -- from the token's own source only."""
        if self._credential_source == "env":
            token = os.environ.get("PROBE_TOKEN") or None
            if token is None or token == self.settings.token:
                return None, (
                    "its token comes from PROBE_TOKEN, which cannot change while the "
                    "process runs (a Kubernetes secret or an exported variable); restart "
                    "the job with a valid token"
                )
            return token, None
        if self._credential_source == "config":
            name = (self.journal.context or {}).get("name")
            try:
                stored = config_module.load_context(name)
            except Exception as exc:  # noqa: BLE001 -- an unreadable config is "nothing new"
                return None, f"the stored login could not be read ({_failure_kind(exc)})"
            base = (stored.get("base_url") or config_module.DEFAULT_BASE_URL).rstrip("/")
            if base != self.settings.base_url.rstrip("/"):
                return None, f"the stored login is for {base}, not {self.settings.base_url}"
            token = stored.get("token") or None
            if token is None or token == self.settings.token:
                return None, f"there is no newer login to read; {WIZARD_HINT}"
            return token, None
        return None, None

    def _learn_identity(self) -> None:
        """Start the one background lookup of who this client's credential
        belongs to, if a refresh could ever be asked of it. Idempotent; called
        when a heartbeat or the exporter starts, never at construction."""
        if self._credential_source is None:
            return
        with self._credential_lock:
            if self._credential_identity_started:
                return
            self._credential_identity_started = True
        threading.Thread(
            target=self._remember_identity, name="probe-credential-identity", daemon=True
        ).start()

    def _remember_identity(self) -> None:
        """Record who the starting credential belongs to. Never raises."""
        self._credential_identity_started = True
        try:
            token = self.settings.token
            who = self._whoami(token)
            if who is not None:
                self._credential_identity = who
                self._stamp_account(token, who)
                from .journal import record_account

                record_account(credential_fingerprint(token, None), who)
        except Exception:  # noqa: BLE001 -- unknown stays None; a thread traceback would reach stderr
            pass
        finally:
            self._credential_identity_ready.set()

    def _whoami(self, token: str | None) -> tuple[str, str] | None:
        """(customer_id, user_id) that ``token`` belongs to: ONE attempt with a
        5 s timeout and no retries (the flush() or beat waiting on it must not
        sit through the transport's full retry budget). None when unknown.
        Raises what the request raised."""
        import copy

        probe_transport = copy.copy(self.transport)
        probe_transport.settings = copy.copy(self.settings)
        probe_transport.settings.token = token
        probe_transport.max_retries = 0
        response = probe_transport.request("GET", "/v1/me", idempotent=True, timeout=5.0)
        who = response.json() if response.content else {}
        if who.get("customer_id") and who.get("user_id"):
            return str(who["customer_id"]), str(who["user_id"])
        return None

    def _different_account(self, candidate: str) -> str | None:
        """None when ``candidate`` belongs to the account this client started
        with, else why it may not be adopted. Asks `/v1/me` WITH the candidate."""
        if not self._credential_identity_started:
            return (
                "the account the process started as is unknown (it was never looked up), "
                "so a new login cannot be matched to it"
            )
        self._credential_identity_ready.wait(timeout=5.0)
        started_as = self._credential_identity
        if started_as is None:
            return "the account the process started as is unknown, so a new login cannot be matched to it"
        try:
            now_as = self._whoami(candidate)
        except Exception as exc:  # noqa: BLE001 -- unverifiable is refused
            return f"the new login could not be verified ({_failure_kind(exc)})"
        if now_as != started_as:
            if now_as is not None:
                self._credential_rejected = candidate
            return (
                "the new login on this machine belongs to a different account; this "
                "process keeps writing as the one it started with"
            )
        return None

    def _own_credential_refusal(self, report: Any) -> bool:
        """Did a drain stop because THIS client's credential was refused?

        Not a 403 naming a missing scope (the key still works), and not an op
        pinned to another context in the shared outbox (not our key at all)."""
        from .key_refusal import credential_refused

        if not getattr(report, "auth_blocked", False):
            return False
        refusals = getattr(report, "auth_refusals", None) or [
            {
                "status": getattr(report, "auth_status", None),
                "message": getattr(report, "auth_message", None),
                "context": getattr(report, "auth_context", None),
            }
        ]
        mine = (self.journal.context or {}).get("name")
        for refusal in refusals:
            if not credential_refused(refusal.get("status"), refusal.get("message")):
                continue
            context = refusal.get("context") or {}
            stamp = context.get("principal")
            if isinstance(stamp, dict) and stamp.get("fingerprint"):
                # The write names the credential that queued it (#2041): ours
                # only if it is one this client has written with. Another
                # login's 401 on a shared machine is not our key being refused.
                refused = refusal.get("fingerprint") or stamp["fingerprint"]
                if refused in self._credential_fingerprints | self._ingest_fingerprints:
                    return True
                continue
            base = context.get("base_url")
            name = context.get("name")
            if (not base or base == self.settings.base_url) and (name is None or name == mine):
                return True
        return False

    def _warn_credential_stale(self, why: str) -> None:
        if self._credential_stale_warned:
            return
        self._credential_stale_warned = True
        _diagnostics.warn(
            f"probe: the API refused this process's credential and {why}. Heartbeats "
            "and delivery stay refused; the run is marked crashed if this lasts 15 minutes."
        )

    def flush(self, *, run_ref: str | None = None, on_error=None, on_delivered=None) -> int:
        """Foreground-drain the journal; returns the delivered count.

        MACHINE-WIDE by default, and that default is load-bearing: `probe
        outbox drain`, recovery after an outage and the tests that assert a
        whole queue lands all rely on one call moving every run's ops. This is
        a NEW keyword rather than a changed default for exactly that reason.

        ``run_ref`` scopes the pass to one run's ops -- a barrier drain (T3-A),
        the same scoping ``drain(run_ref=...)`` has always offered. Pass it
        wherever the drain exists to make ONE run's writes durable, so a
        neighbour's undeliverable op cannot decide this run's outcome. The
        journal is shared per directory across runs, so an unscoped barrier
        drain stops at the first stuck op in the whole queue no matter whose
        it is.

        FIFO is not weakened by scoping: ops are still attempted in enqueue
        order within the scope, and a run's own writes only ever need to be
        ordered against each other. `Run._queue_deferred_finish` depends on
        that and no more.

        ``on_error`` observes typed delivery errors and may raise to leave the
        current operation queued for a caller that owns its retry policy.
        ``on_delivered(correlation)`` observes each durably completed operation.
        Observer failures cannot change delivery; legacy ops have no correlation.
        """
        from .journal import drain

        def one_pass():
            return drain(
                self.journal,
                run_ref=run_ref,
                client_factory=self._outbox_client_factory(),
                on_error=on_error,
                on_delivered=on_delivered,
            )

        refused = self.settings.token
        report = one_pass()
        if self._own_credential_refusal(report) and self.refresh_credentials(refused=refused):
            # Plan 2.7: a re-login revoked the token this process was built
            # with. One more pass under the current one.
            return report.delivered + one_pass().delivered
        return report.delivered

    def _drain_for_close(self, run_ref: str, *, lock_timeout: float | None):
        """One barrier pass over ``run_ref``'s ops for `Run.finish()`; returns
        the whole `DrainReport` (flush() keeps only the count), because the
        close loop needs the server's Retry-After, whether the pass got the
        drain lock, and whether it hit an auth block. ``lock_timeout`` bounds
        both the wait for that lock -- a detached worker mid-pass -- and the
        pass's promotion of waiting uploads, so neither can outlive the close's
        deadline (plan 0.6)."""
        from .journal import drain

        return drain(
            self.journal,
            run_ref=run_ref,
            client_factory=self._outbox_client_factory(),
            lock_timeout=lock_timeout,
            promote_timeout=lock_timeout,
        )

    def _delivery_journal(self) -> Journal:
        return Journal.for_receipts(
            self.journal.dir,
            context=self.journal.context,
            attribution=self.journal.attribution,
        )

    def enqueue_artifact_upload(
        self,
        *,
        correlation: str,
        anchor: Anchor | str,
        anchor_id: str,
        name: str,
        path: str,
        notes: str | None = None,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        expected_content_hash: str | None = None,
    ) -> dict:
        """Queue immutable artifact bytes with a durable, replayable receipt.

        Backpressure and source changes raise: the importer retains its intent.
        Reusing a correlation replays the frozen request, never newer source bytes.
        """
        from .redaction import default_scrub, scrub_text

        result = self._delivery_journal().append_upload(
            correlation=correlation,
            anchor=Anchor(anchor).value,
            anchor_id=anchor_id,
            name=name,
            src_path=path,
            notes=scrub_text(notes) if notes is not None else None,
            meta=default_scrub(meta) if meta is not None else None,
            content_type=content_type,
            kind=kind,
            expected_content_hash=expected_content_hash,
        )
        self._wake_delivery()
        return result

    def enqueue_artifact_reference(
        self,
        *,
        correlation: str,
        anchor: Anchor | str,
        anchor_id: str,
        name: str,
        uri: str,
        notes: str | None = None,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        content_hash: str | None = None,
        size_bytes: int | None = None,
    ) -> dict:
        """Record a pointer through the same outbox, retaining its artifact ID."""
        from .redaction import default_scrub, scrub_text

        anchor = Anchor(anchor)
        # Literal paths, one per anchor, for the reason `_presign_anchored` gives:
        # a segment table here once mapped EXPERIMENT to `experiments`, which the
        # parity guard could not see, so after the 5b cut an experiment-anchored
        # reference was journaled to a 410 and dead-lettered on drain.
        if anchor is Anchor.RUN:
            path = f"/v1/runs/{anchor_id}/artifacts"
        elif anchor is Anchor.EXPERIMENT:
            path = f"/v1/projects/{anchor_id}/artifacts"
        elif anchor is Anchor.PROJECT:
            path = f"/v1/projects/{anchor_id}/artifacts"
        else:
            raise ValueError("receipt references require a run, experiment or project")
        body = {
            k: v
            for k, v in {
                "name": name,
                "uri": uri,
                "is_reference": True,
                "notes": scrub_text(notes) if notes is not None else None,
                "meta": default_scrub(meta) if meta is not None else None,
                "kind": kind,
                "content_type": content_type,
                "content_hash": content_hash,
                "size_bytes": size_bytes,
            }.items()
            if v is not None
        }
        journal = self._delivery_journal()
        op_id = journal.append_http(
            "POST",
            path,
            body,
            correlation=correlation,
        )
        self._wake_delivery()
        return {**journal.delivery_state(correlation), "op_id": op_id}

    def delivery_receipt(self, correlation: str) -> dict | None:
        return self._delivery_journal().receipt(correlation)

    def compact_delivery_receipts(
        self, *, max_records: int = 256, max_seconds: float = 1.0
    ) -> dict:
        """Bounded local maintenance; every historical delivery identity remains readable."""
        return self._delivery_journal().compact_receipts(
            max_records=max_records, max_seconds=max_seconds
        )

    def delivery_state(self, correlation: str) -> dict:
        """Read queued, failed, discarded, or delivered state without waking a worker."""
        return self._delivery_journal().delivery_state(correlation)

    def resume_delivery(self, correlation: str) -> dict:
        """Resume an already frozen request, including after the source is remounted."""
        journal = self._delivery_journal()
        state = journal.delivery_state(correlation)
        if state["state"] == "pending":
            journal.recover_intents()
        elif state["state"] == "failed":
            journal.retry_failed(state["op_id"])
        if state["state"] not in {"unknown", "discarded", "delivered"}:
            self._wake_delivery()
        return journal.delivery_state(correlation)

    def _wake_delivery(self) -> None:
        if self._drain_interval is not None:
            self._after_enqueue()
        elif self._delivery_auto_drain:
            self._kick_drainer(force=True)

    # -- identity / auth ----------------------------------------------------
    def ensure_authenticated(self, *, interactive: bool | None = None) -> bool:
        """Make sure a user token exists, minting one via the browser device flow
        when a human can approve it.

        The interactive path runs only when stdin+stderr are TTYs and
        ``PROBE_AUTO_LOGIN`` is not ``0`` (or when ``interactive=True`` forces it).
        On success the token is persisted to the same config file the wizard's
        sign-in writes, so the browser round-trip happens once per machine. Returns
        True when a token is available; False leaves the transport to raise its normal
        ``AuthError`` on first use (the crisp headless/CI behavior)."""
        if self.settings.token:
            return True
        if interactive is None:
            interactive = (
                os.environ.get("PROBE_AUTO_LOGIN", "1") != "0"
                and sys.stdin.isatty()
                and sys.stderr.isatty()
            )
        if not interactive:
            return False
        from .config import save_context
        from .device import DeviceLoginError, device_login

        print(
            f"no Probe token found — opening {self.settings.base_url} for browser approval…",
            file=sys.stderr,
        )

        def _show(prompt) -> None:
            print(f"  visit: {prompt.verification_uri_complete}", file=sys.stderr)
            print(f"  code:  {prompt.user_code}", file=sys.stderr)

        try:
            token = device_login(self.settings.base_url, on_prompt=_show)
        except DeviceLoginError as exc:
            warnings.warn(f"automatic device login failed: {exc}", stacklevel=2)
            return False
        save_context({"base_url": self.settings.base_url, "token": token})
        # Settings is shared with the transport; mutating it authenticates both.
        self.settings.token = token
        print("logged in — token saved for future runs", file=sys.stderr)
        return True

    def me(self) -> dict:
        # /v1/me (not the session-only /auth/me): resolves through the unified
        # door, so a `probe_pat` or OAuth token identifies its own tenant/role.
        return self.transport.get("/v1/me")

    def logout(self) -> dict:
        """Release the calling token from THIS machine.

        Device-aware on a current backend: the transport sends `X-Probe-Device`,
        so the server unbinds the credential from this machine and revokes it
        only when no other live device still holds it. That is what stops
        reauthorizing one laptop from signing another one out when both were
        using the same shared PAT.

        Returns `{revoked, detached, still_used_by}` so the caller can report
        what actually happened. An older backend answers 204 with no body, which
        arrives as `{}` -- callers must treat a missing `revoked` key as "this
        server could not tell me", never as "nothing happened".
        """
        return self.transport.delete("/v1/tokens/current") or {}

    # -- tokens -------------------------------------------------------------
    def list_tokens(self) -> list[dict]:
        """My live (unrevoked) tokens. Secrets are never returned — only
        ``token_prefix``, which is what a human matches against."""
        return self.transport.get("/v1/tokens")

    def create_token(
        self,
        name: str,
        *,
        scopes: list[str] | None = None,
        open_browser: bool = True,
        on_prompt=None,
    ) -> dict:
        """Mint a named token through the browser device flow.

        NOT ``POST /v1/tokens``: that route is session-only by design, so it 403s
        for a token-authenticated CLI. The device flow reaches the same minter with
        a human approving in the browser, which is what the invariant "a leaked
        token must not be able to mint more tokens" is protecting.

        Returns ``TokenCreated``; ``["token"]`` is the plaintext secret and this is
        the only time it exists. Callers must show it once and never persist it.
        """
        from .device import device_authorize

        return device_authorize(
            self.settings.base_url,
            scopes=scopes,
            token_name=name,
            open_browser=open_browser,
            on_prompt=on_prompt,
        )

    def revoke_token(self, token_id: str) -> None:
        """Revoke a token by id. Your own: any writer. A teammate's: needs a
        browser session AND owner/admin, so it 403s from the CLI (by design)."""
        self.transport.delete(f"/v1/tokens/{token_id}")

    # -- client installations ----------------------------------------------
    def register_client_capabilities(
        self,
        *,
        schema_version: int = 2,
        auto_update: str,
        tracking: str,
        capture: str,
    ) -> dict:
        """Replace the complete allowlisted snapshot for this token's install.

        The token identifies the installation; no token or installation id is
        accepted in the body. The schema deliberately carries only coarse
        tri-states, never paths, commands, environment variables, or secrets.

        v2 replaced v1's `mcp`/`skills` pair with a single `tracking` -- they
        were always written from one boolean -- and added `capture`, which v1
        could not report at all. The server still accepts v1 from clients in the
        field and reads their capture as `unknown`.
        """
        return self.transport.put(
            "/v1/client-installations/current/capabilities",
            {
                "schema_version": schema_version,
                "auto_update": auto_update,
                "tracking": tracking,
                "capture": capture,
            },
        )

    def name_client_installation(self, *, hostname: str) -> dict:
        """Name this token's installation after the machine it runs on.

        Sends the BARE hostname, not a label: the machine's name is a fact the
        client observes, and how it is rendered is the server's convention. Two
        callers composing their own label is how one laptop comes to appear
        under two spellings.

        The server replaces only names it generated itself, so a device someone
        named deliberately is left alone; `renamed` in the response says which
        happened. A backend that predates this route 404s, which the caller
        treats as "nothing to do".
        """
        return self.transport.put(
            "/v1/client-installations/current/name",
            {"hostname": hostname},
        )

    def create_credential_attachment_grant(self, installation_id: str) -> dict:
        """Mint a short-lived installation join grant with the linked API PAT."""
        return self.transport.post(
            f"/v1/client-installations/{installation_id}/credential-attachment-grants"
        )

    def attach_current_credential(self, installation_id: str, *, grant: str) -> dict:
        """Consume an API-minted join grant using this read-only MCP PAT."""
        return self.transport.put(
            f"/v1/client-installations/{installation_id}/credentials/current",
            {"grant": grant},
        )

    def list_client_installations(self) -> dict:
        """Unified view of installs, API/MCP credentials, and capture devices."""
        return self.transport.get("/v1/client-installations")

    # -- workspaces ---------------------------------------------------------
    def list_workspaces(self) -> list[dict]:
        """Every workspace in the team, as an unpaginated list in server order.

        The server sorts alphabetically, equally for every team member.
        """
        return self.transport.get("/v1/workspaces")

    def get_workspace(self, workspace_id: str) -> dict:
        return self.transport.get(f"/v1/workspaces/{workspace_id}")

    def create_workspace(self, slug: str, name: str | None = None) -> dict:
        """POST /v1/workspaces — a workspace any team member may use or rename.

        Pass ``workspace_id`` to :meth:`create_project`, or select it in the CLI
        with ``probe workspace use <slug>``. Without a workspace, the server uses
        the oldest existing one and creates a Default workspace only if none remain.

        A taken slug is a 409 carrying the existing id and a free suggestion, never a
        silent hand-back of somebody else's row.
        """
        body: dict = {"slug": slug}
        if name is not None:
            body["name"] = name
        return self.transport.post("/v1/workspaces", body)

    def rename_workspace(self, workspace_id: str, name: str) -> dict:
        """PATCH /v1/workspaces/{id}. Any team member may rename any workspace.

        ``name`` is the only editable field; the slug stays unchanged.
        """
        return self.transport.patch(f"/v1/workspaces/{workspace_id}", {"name": name})

    def delete_workspace(self, workspace_id: str) -> None:
        """DELETE /v1/workspaces/{id}. Any workspace, only while empty.

        Projects, files, or an integration targeting it cause a 409. Move work out
        and disconnect integrations first. If none remain, the next write without
        a workspace creates a Default workspace.
        """
        self.transport.delete(f"/v1/workspaces/{workspace_id}")

    # -- write permissions (0214) -------------------------------------------
    #
    # THE INTERIM ADMIN SURFACE. The dashboard half of this feature ships in a
    # later change, so until then these methods (and the `probe access-group` /
    # `probe workspace writers` commands over them) are the only way to say who
    # may edit a workspace. Every mutation is owner/admin-only server-side.
    #
    # None of this touches READS: a restricted workspace stays fully visible to
    # every team member, which is the product decision, not an omission.

    def list_access_groups(self) -> list[dict]:
        """Every named group in the team, with its member user ids.

        Names and emails come from the team roster, not from here -- a group
        stores ids so a rename or an email change cannot strand a grant.
        """
        return self.transport.get("/v1/access-groups")

    def create_access_group(self, name: str) -> dict:
        """POST /v1/access-groups. The slug is derived from the name.

        NOT `groups`: that word already means a RUN group (a sweep) everywhere
        else in this client.
        """
        return self.transport.post("/v1/access-groups", {"name": name})

    def rename_access_group(self, group_id: str, name: str) -> dict:
        return self.transport.patch(f"/v1/access-groups/{group_id}", {"name": name})

    def delete_access_group(self, group_id: str) -> None:
        """Deleting a group drops it from every writer list it guards.

        That can only NARROW access: a restricted workspace left with no writers
        is writable by nobody, never by everybody.
        """
        self.transport.delete(f"/v1/access-groups/{group_id}")

    def add_access_group_member(self, group_id: str, user_id: str) -> None:
        """Idempotent. A user may belong to several groups."""
        self.transport.put(f"/v1/access-groups/{group_id}/members/{user_id}", None)

    def remove_access_group_member(self, group_id: str, user_id: str) -> None:
        """Idempotent."""
        self.transport.delete(f"/v1/access-groups/{group_id}/members/{user_id}")

    def get_workspace_writers(self, workspace_id: str) -> dict:
        """`{mode, users, groups}` — who may EDIT this workspace.

        Readable by every member: a permission nobody can see is a save that
        mysteriously fails.
        """
        return self.transport.get(f"/v1/workspaces/{workspace_id}/writers")

    def set_workspace_writers(
        self,
        workspace_id: str,
        *,
        mode: str,
        users: list[str] | None = None,
        groups: list[str] | None = None,
    ) -> dict:
        """Replace the WHOLE write state (mode + both lists) in one call.

        Whole-state rather than add/remove because "restrict this to the lab" as
        three requests can interleave with another admin's three and commit a
        state neither asked for. The server takes a row lock for the same reason.

        `mode='open'` restores the default: every team member may edit.
        """
        return self.transport.put(
            f"/v1/workspaces/{workspace_id}/writers",
            {"mode": mode, "users": users or [], "groups": groups or []},
        )

    # -- projects -----------------------------------------------------------
    def create_project(
        self,
        slug: str,
        name: str | None = None,
        *,
        kind: str,
        parent_project_id: str | None = None,
        workspace_id: str | None = None,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        authored_by: str | None = None,
    ) -> dict:
        """Create a project. Raises ``ConflictError`` if the slug is taken.

        ``kind`` is REQUIRED and declares what the project is for:
        ``training`` (weights move), ``evaluation`` (frozen weights — sweeps,
        evals), ``research`` (papers, design, theory) or ``general``. It
        structures the dashboard page; it never gates data. Machine paths with
        no intent-holder pass ``"general"``.

        ``parent_project_id`` files the new project under an existing one
        (0148): it inherits the parent's workspace (tree = one workspace,
        owned by the root), the depth cap applies, and passing a
        ``workspace_id`` that is not the parent's is a 422.

        Creation is always explicit: there is no get-or-create. A caller that
        does not know whether the project exists asks :meth:`resolve_project`
        first and decides.

        ``document`` is authored Markdown that lives INSIDE the
        project's Overview page, as a block the page's AI writer may not
        rewrite. When the project is about a codebase, put a line containing only
        ``[README](https://github.com/owner/repo)`` in ``document``: the
        dashboard renders that repository's README there, refreshed on push, and
        for a private repo too when the team's GitHub App is installed on that
        account. The LINK TEXT is what makes it an embed, and ``project.repo`` is
        derived from it -- see :meth:`update_project`."""
        body: dict[str, Any] = {"slug": slug, "kind": kind}
        # OMITTED, not `name or slug`. The server nulls a name byte-identical to
        # the slug (`app/core/naming.py::chosen_name`), so sending it was already
        # a no-op -- but with `authored_by` on the wire it became a LIE: the slug
        # plus a human declaration claims a person chose the identifier as the
        # title. Say nothing instead.
        if name:
            body["name"] = name
        _put_authorship(body, authored_by)
        if parent_project_id is not None:
            body["parent_project_id"] = parent_project_id
        if workspace_id is not None:
            body["workspace_id"] = workspace_id
        if description is not None:
            body["description"] = description
        if document is not None:
            body["document"] = document
        if tags is not None:
            body["tags"] = tags
        if metadata is not None:
            body["metadata"] = metadata
        row = self.transport.post("/v1/projects", body)
        if tags is not None:
            self._verify_tags_written(tags, row, "POST /v1/projects")
        return row

    def resolve_project(self, slug: str, *, strict: bool = False) -> dict | None:
        """Look a project up by slug. ``None`` when it does not exist.

        `(customer_id, slug)` is UNIQUE, so ``?slug=`` returns 0 or 1 row and an
        empty result is an unambiguous "absent" rather than "not on this page".
        Nothing is hidden from this read: a deleted project is gone, and its slug
        is free again."""
        rows = self.transport.get("/v1/projects", params={"slug": slug})
        return _exactly(rows, slug, strict=strict)

    def ensure_project(
        self, slug: str, name: str | None = None, *, kind: str = "general", **kw
    ) -> dict:
        """Get-or-create a project by slug. SDK-only; see :meth:`run`.

        ``kind`` defaults to ``"general"`` HERE, unlike :meth:`create_project`:
        the ensure path is what implicit machinery (``run()``'s auto-create,
        folder backfills) calls, and a default that silently mislabeled real
        intent would be worse than the neutral label. A caller that knows what
        it is building passes the real kind.

        :meth:`create_project` stays the explicit one, where a taken slug is an
        error. This is for callers who do not care whether it existed, only that
        it does now — but a slug that LOOKS like a typo of an existing one is
        refused rather than created. See :meth:`_refuse_near_miss`."""
        found = self.resolve_project(slug)
        if found is not None:
            return found
        self._guard_creatable("project", slug)
        try:
            return self.create_project(slug, name, kind=kind, **kw)
        except errors.ConflictError:
            # Lost a create race with a concurrent process. Get-or-create promises
            # the row exists afterwards, not that WE made it, so re-resolve rather
            # than surface a conflict the caller cannot act on. Re-raise if it is
            # still absent — then the 409 meant something else.
            #
            # NOT the swallow #87 removed. That one hid a TYPO behind a
            # successful-looking create; this resolves a race between two
            # processes asking for the same, correct, slug.
            found = self.resolve_project(slug)
            if found is None:
                raise
            return found

    def get_project(self, project_id: str) -> dict:
        return self.transport.get(f"/v1/projects/{project_id}")

    def list_project_contributors(self, project_id: str) -> list[dict]:
        """Who worked on this project. `direct` false = their work is in a
        subproject, named by `via_project_id`."""
        return self.transport.get(f"/v1/projects/{project_id}/contributors")

    def add_project_contributor(self, project_id: str, user_id: str) -> dict:
        """Credit someone who has not written anything yet (a reviewer).
        422 if they are not an active member of the team."""
        return self.transport.post(f"/v1/projects/{project_id}/contributors", {"user_id": user_id})

    def remove_project_contributor(self, project_id: str, user_id: str) -> None:
        """Drop a DIRECT credit. 409 if they contribute through a subproject --
        removing them here cannot undo that. Not a ban: contributing again
        re-adds them."""
        self.transport.delete(f"/v1/projects/{project_id}/contributors/{user_id}")

    @staticmethod
    def _verify_tags_filter(requested: list[str], items: list, route: str) -> None:
        """A pre-0066 backend IGNORES the ``tags=`` filter and returns the
        unfiltered list — a confident wrong answer presented as filtered (the
        same failure shape as the 0054 ``project_id`` guard in list_runs).
        Every returned row must carry ALL requested tags; both sides compare in
        canonical form so a legacy un-normalized row can never false-positive.
        Refuse rather than mislabel. (An empty page proves nothing and passes.)"""
        want = set(canonical_tags(requested))
        for item in items:
            if want - set(canonical_tags(item.get("tags") or [])):
                raise errors.NotFoundError(
                    f"this research-os backend predates {route}?tags= (0066): it "
                    "ignored the filter and returned unfiltered rows. Upgrade "
                    "the backend to filter by tags."
                )

    @staticmethod
    def _verify_tags_written(sent: list[str], row: dict | None, route: str) -> None:
        """A pre-0066 backend silently DROPS ``tags`` from write bodies (unknown
        Pydantic fields are ignored) and answers 200 with the row unchanged — a
        confident no-op. The response must echo the canonical sent list; refuse
        rather than pretend (the write-side twin of ``_verify_tags_filter``).
        ``row=None`` (a spooled fail-open write) is unverifiable and passes."""
        if row is None:
            return
        from .redaction import default_scrub

        if "tags" not in row or canonical_tags(row.get("tags") or []) != canonical_tags(
            default_scrub(sent)
        ):
            raise errors.NotFoundError(
                f"this research-os backend predates tags on {route} (0066): it "
                "ignored the tags write and returned the row unchanged. Upgrade "
                "the backend."
            )

    @staticmethod
    def _verify_parent_filter(requested: str, items: list, route: str) -> None:
        """A pre-0148 backend IGNORES ``parent_id=`` and returns EVERY project in
        the tenant -- which a caller asking for one project's children would then
        present as those children. The same failure shape as the tags and
        ``project_id`` guards: a confident wrong answer wearing the shape of a
        filtered one. Refuse rather than mislabel. (An empty page proves nothing
        and passes.)"""
        for item in items:
            if str(item.get("parent_project_id") or "") != str(requested):
                raise errors.NotFoundError(
                    f"this research-os backend predates {route}?parent_id= (0148): "
                    "it ignored the filter and returned unfiltered rows. Upgrade "
                    "the backend to list subprojects."
                )

    def list_projects(
        self,
        *,
        workspace_id: str | None = None,
        tags: list[str] | None = None,
        parent_id: str | None = None,
        **params,
    ) -> Page:
        """``tags`` filters to projects carrying ALL of them (AND, 0066).

        ``parent_id`` lists one project's DIRECT children (0148) -- one level,
        not the whole subtree, matching the dashboard's Subprojects tab.
        """
        query = dict(params)
        if workspace_id is not None:
            query["workspace_id"] = workspace_id
        if parent_id is not None:
            query["parent_id"] = parent_id
        # Send the canonical form (the server normalizes anyway): the guard
        # below then compares like against like.
        tags = canonical_tags(tags) if tags else None
        if tags:
            query["tags"] = tags
        page = self.transport.get_page("/v1/projects", params=query or None)
        if tags and page.items:
            self._verify_tags_filter(tags, page.items, "GET /v1/projects")
        if parent_id is not None and page.items:
            self._verify_parent_filter(parent_id, page.items, "GET /v1/projects")
        return page

    def update_project(
        self,
        project_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        kind: str | None = None,
        parent_project_id: str | None | type[_UNSET] = _UNSET,
        authored_by: str | None = None,
    ) -> dict:
        """PATCH /v1/projects/{id} for display fields and visible Markdown.

        ``document`` is authored Markdown that lives INSIDE the
        project's Overview page, as a block the page's AI writer may not
        rewrite. It is replaced wholesale and is last-write-wins: read the
        current project immediately before editing and preserve its existing
        sections. ``""`` clears it. It is separate from the project's private
        Notes, but NOT from the Overview page -- it is part of it.

        DO NOT expect a read-back to be byte-identical: a detail GET answers
        from the page, which renders the document. A fenced block loses its
        language and an ``http://`` link loses its href, because a page may
        carry neither. Verify that what you meant is THERE, not that the bytes
        match.

        ``tags`` REPLACES the whole list ([] clears); the server normalizes to
        lowercase-kebab (CONTRACT.md "tags").

        ``kind`` re-declares what the project is for (0149); ``None`` leaves it
        untouched (kind cannot be cleared).

        ``parent_project_id`` is the ONE explicit-null field (0148): pass a
        project id to attach/move (the whole subtree re-files into the
        parent's workspace), pass ``None`` to DETACH to top level, and omit
        the argument to leave the parent untouched. Cycles, depth and size are
        refused by the server; a request carrying both this and
        ``workspace_id`` is refused too (the workspace follows the parent).

        A project's README embed is part of ``document``, not a separate
        field: write ``[README](https://github.com/owner/repo)`` on its own line
        and the repository's README renders at that point in the document. The
        server derives ``project.repo`` from it, so there is nothing else to set.

        Re-filing into another workspace is :meth:`move_project`, not a keyword here.
        Same route, but splitting the verbs keeps a reindex fan-out (see move_project)
        from being something you can trigger by mistyping an update.
        """
        body = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
                "document": document,
                "tags": tags,
                "metadata": metadata,
                "kind": kind,
            }.items()
            if value is not None
        }
        if parent_project_id is not _UNSET:
            # Explicit null on the wire = detach; a uuid = attach/move.
            body["parent_project_id"] = parent_project_id
        if not body:
            raise ValueError("update_project needs at least one field to set")
        # AFTER the emptiness check, deliberately. `authored_by` declares who
        # wrote the OTHER fields; on its own it declares authorship of nothing,
        # and letting it satisfy "at least one field to set" would turn a
        # no-op call into a PATCH.
        _put_authorship(body, authored_by)
        row = self.transport.patch(f"/v1/projects/{project_id}", body)
        if document is not None:
            self._verify_entity_markdown_written(
                "project",
                document,
                row,
                "PATCH /v1/projects/{id}",
            )
        if tags is not None:
            self._verify_tags_written(tags, row, "PATCH /v1/projects/{id}")
        return row

    @staticmethod
    def _verify_entity_markdown_written(
        kind: str,
        sent: str,
        row: dict,
        route: str,
    ) -> None:
        """Refuse a successful-looking ``document`` no-op.

        Older Pydantic schemas ignore an unknown field and still answer 2xx. A
        visible document that silently vanished is worse than a capability
        error, so every entity write compares the value the write's OWN
        response carries before returning success.

        ``row`` MUST be that response, never a fresh detail read. Since 0219 a
        project's or experiment's detail GET answers ``document`` from
        the Overview page, which renders the document rather than storing it
        verbatim -- so a read-back comparison fails for text that landed
        exactly as sent, and reports it as a backend too old to trust.
        """
        from .redaction import default_scrub

        # The transport intentionally stores the safe form. Compare against
        # that same form while retaining the guard against silently lost writes.
        expected = default_scrub(sent) if sent.strip() else ""
        if row.get("document") != expected:
            raise errors.RosError(
                f"the research-os backend accepted the {kind} Markdown write on "
                f"{route} but did not store it; upgrade the backend before relying "
                "on document/--summary"
            )

    @staticmethod
    def _verify_entity_markdown_present(
        kind: str,
        sent: str,
        row: dict,
        route: str,
    ) -> None:
        """The weaker half of the guard, for a read that cannot be byte-exact.

        A project's or experiment's detail GET answers from the Overview page,
        which renders the document; comparing bytes there fails for text that
        landed perfectly. What the guard actually defends against is a schema
        that took the field and stored nothing, and a document that comes back
        at all disproves that. Weaker on purpose, and said out loud rather than
        dressed up as the stronger check.
        """
        if sent.strip() and not str(row.get("document") or "").strip():
            raise errors.RosError(
                f"the research-os backend accepted the {kind} Markdown write on "
                f"{route} but stored nothing; upgrade the backend before relying "
                "on document/--summary"
            )

    def move_project(self, project_id: str, workspace_id: str) -> dict:
        """Re-file a project into another workspace.

        PATCH is the only backend door, but this is a much heavier operation than the
        verb suggests: when the workspace actually changes, the server reindexes every
        live descendant experiment and terminal run in the same transaction, because
        those documents denormalize ``workspace_id``. A no-op move (same workspace)
        skips the fan-out entirely.

        An unknown workspace is a 422, not a 404 — it is a rejected *value*, not a
        missing resource. Since 0148 two more refusals exist: a SUBPROJECT's
        workspace follows its tree's root (409 — detach first, or move the
        root), and moving a root drags its whole subtree, refused (422) past
        MAX_TREE_MUTATION_PROJECTS affected projects.
        """
        return self.transport.patch(f"/v1/projects/{project_id}", {"workspace_id": workspace_id})

    def delete_project(self, project_id: str, *, recursive: bool = False) -> dict | None:
        """Move a project, and everything under it, to the server's TRASH.

        Experiments, runs, telemetry and files go with it, and the slug is freed.
        Probe support can restore it for 21 days (the returned receipt says
        until when); after that it is deleted for good. A server without the
        `trash` feature (:meth:`supports_feature`) deletes PERMANENTLY and
        returns None. 409 if a published experiment
        version pins something in the tree — and 409, carrying the TOTAL
        descendant blast radius, when the project has live subprojects (0148):
        pass ``recursive=True`` to explicitly take the whole subtree with it,
        in one transaction."""
        # transport.request, not .delete: the parity guard resolves paths from
        # the AST, and a path mutated by += would read as unreachable. The
        # query rides `params`, keeping the literal template intact.
        resp = self.transport.request(
            "DELETE",
            f"/v1/projects/{project_id}",
            params={"recursive": "true"} if recursive else None,
            idempotent=True,
        )
        return resp.json() if resp.content else None

    # -- anchored artifacts / files -----------------------------------------
    # Every route below is written as its own literal call site rather than looked up
    # in a table. That is deliberate: the contract-parity guard resolves paths from the
    # AST, and a path built by `.format()` or a dict lookup is invisible to it — the
    # routes would read as unreachable and the guard would stop guarding them.

    def _presign_anchored(self, anchor: Anchor, anchor_id: str | None, body: dict) -> dict:
        if anchor is Anchor.RUN:
            return self.transport.post(f"/v1/runs/{anchor_id}/artifacts/uploads", body)
        if anchor is Anchor.EXPERIMENT:
            return self.transport.post(f"/v1/projects/{anchor_id}/artifacts/uploads", body)
        if anchor is Anchor.PROJECT:
            return self.transport.post(f"/v1/projects/{anchor_id}/artifacts/uploads", body)
        if anchor is Anchor.WORKSPACE:
            return self.transport.post(f"/v1/workspaces/{anchor_id}/files/uploads", body)
        return self.transport.post("/v1/shared/files/uploads", body)

    def list_anchored(self, anchor: Anchor, anchor_id: str | None = None, **params) -> Any:
        """List the artifacts/files under one anchor."""
        query = params or None
        if anchor is Anchor.RUN:
            if "limit" not in params and "offset" not in params:
                return read_artifact_rows(
                    lambda page: self.transport.request(
                        "GET", f"/v1/runs/{anchor_id}/artifacts", params=page, idempotent=True
                    ),
                    query,
                )
            return self.transport.get(f"/v1/runs/{anchor_id}/artifacts", params=query)
        if anchor is Anchor.EXPERIMENT:
            return self.transport.get(f"/v1/projects/{anchor_id}/artifacts", params=query)
        if anchor is Anchor.PROJECT:
            return self.transport.get(f"/v1/projects/{anchor_id}/artifacts", params=query)
        if anchor is Anchor.WORKSPACE:
            return self.transport.get(f"/v1/workspaces/{anchor_id}/files", params=query)
        return self.transport.get("/v1/shared/files", params=query)

    def create_anchored_reference(self, anchor: Anchor, anchor_id: str, body: dict) -> dict:
        """Record a metadata-only (reference) artifact — no bytes uploaded.

        Only the three *artifact* anchors have this door. Workspace and shared are
        file anchors: a file is its bytes, so there is no reference-without-bytes form
        of one, and the backend declares no such route.
        """
        if anchor is Anchor.RUN:
            return self.transport.post(f"/v1/runs/{anchor_id}/artifacts", body)
        if anchor is Anchor.EXPERIMENT:
            return self.transport.post(f"/v1/projects/{anchor_id}/artifacts", body)
        if anchor is Anchor.PROJECT:
            return self.transport.post(f"/v1/projects/{anchor_id}/artifacts", body)
        raise ValueError(
            f"{anchor.value} is a file anchor — a file has no metadata-only form; "
            "upload bytes with upload_file() instead"
        )

    def upload_file(
        self,
        anchor: Anchor,
        anchor_id: str | None,
        name: str,
        path: str,
        *,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
    ) -> dict:
        """Upload a local file to any anchor: fingerprint -> presign -> PUT -> confirm.

        ``kind``/``meta``/``span_id``/``step_index`` are run-only. Passing them with a
        non-run anchor raises here rather than letting the server 422, because
        ``ScopedUploadRequest`` forbids extras and the resulting error does not say
        which field was the problem.

        ``notes`` is the exception and is accepted on EVERY anchor (0095). That is
        the point of it: `ScopedUploadRequest` forbidding extras meant a
        project/experiment upload had no way to describe itself at all, so agents
        concatenated the description onto ``name`` -- which is the file's relative
        posix path, so it broke the extension, the preview and the derived folder.

        Strict by design — no fail-open reference fallback. The fallback exists on
        :meth:`Run.log_artifact` so a training loop is never blocked by a flaky
        upload; an operator running ``probe artifact add`` wants to be told it failed.
        """
        anchor = Anchor(anchor)
        # The caller's `name` is the artifact's relative posix path, and the preview
        # route reads its extension. A caller naming the upload for what it IS
        # ("ckpt") rather than where it came from loses that, so it is restored from
        # the local path. Idempotent -- a name that has one is untouched.
        from .redaction import default_scrub, scrub_text

        name = scrub_text(name_with_extension(name, path))
        notes = scrub_text(notes) if notes is not None else None
        meta = default_scrub(meta)
        run_only = {
            "kind": kind,
            "meta": meta,
            "span_id": span_id,
            "step_index": step_index,
        }
        if anchor in _SCOPED_ANCHORS:
            offending = sorted(k for k, v in run_only.items() if v is not None)
            if offending:
                raise ValueError(
                    f"{', '.join(offending)} {'is' if len(offending) == 1 else 'are'} "
                    f"only accepted on a run anchor; the {anchor.value} upload contract "
                    "rejects extra fields (422)"
                )
        if anchor is not Anchor.SHARED and not anchor_id:
            raise ValueError(f"a {anchor.value} anchor needs an id")

        # Redact BEFORE fingerprinting: the digest has to describe the bytes
        # that actually leave, because the server signs it and R2 checks it.
        with prepare_upload(path) as prepared:
            digest, size = fingerprint(prepared.path)
            return self.upload_fingerprinted(
                anchor,
                anchor_id,
                name,
                prepared.path,
                digest=digest,
                size=size,
                content_type=content_type,
                kind=kind,
                meta=meta,
                notes=notes,
                span_id=span_id,
                step_index=step_index,
            )

    def presign_upload(
        self,
        anchor: Anchor | str,
        anchor_id: str | None,
        name: str,
        *,
        digest: str,
        size: int,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
    ) -> dict:
        """Register upload intent: the server creates (or revives) the
        ``pending`` artifact row and returns a presigned PUT. Called by
        :meth:`upload_fingerprinted` on every attempt -- a remembered URL or
        row is never trusted (the reaper may have expired both) -- and by the
        async enqueue's capped best-effort ping (1A)."""
        anchor = Anchor(anchor)
        if anchor in _SCOPED_ANCHORS:
            req = ScopedUploadRequest(
                name=name,
                content_hash=digest,
                size_bytes=size,
                content_type=content_type,
                notes=notes,
            )
        else:
            req = UploadRequest(
                name=name,
                content_hash=digest,
                size_bytes=size,
                content_type=content_type,
                span_id=span_id,
                step_index=step_index,
                kind=kind,
                meta=meta or None,
                notes=notes,
            )
        return self._presign_anchored(
            anchor, anchor_id, req.model_dump(mode="json", exclude_none=True)
        )

    @freeze_upload
    def upload_fingerprinted(
        self,
        anchor: Anchor | str,
        anchor_id: str | None,
        name: str,
        path: str,
        *,
        digest: str,
        size: int,
        content_type: str | None = None,
        kind: str | None = None,
        meta: dict | None = None,
        notes: str | None = None,
        span_id: str | None = None,
        step_index: int | None = None,
    ) -> dict:
        """The presign -> PUT -> confirm core, for callers that already hold the
        fingerprint -- :meth:`upload_file` after hashing, and the outbox journal
        drain replaying a staged blob (whose hash was taken at enqueue or by the
        drainer, 11A). Phase-aware failure handling lives HERE, where the phase
        is known: a 404 on confirm after a ``have`` dedup is success (see below),
        and every attempt re-presigns rather than trusting a remembered URL.
        """
        anchor = Anchor(anchor)
        presign = self.presign_upload(
            anchor,
            anchor_id,
            name,
            digest=digest,
            size=size,
            content_type=content_type,
            kind=kind,
            meta=meta,
            notes=notes,
            span_id=span_id,
            step_index=step_index,
        )
        # `have` means the server already holds these bytes (content-addressed dedup),
        # so there is nothing to PUT. For a file anchor the swap to live also already
        # happened, in its own transaction.
        if not presign.get("have"):
            # Stream the file (an anchored artifact can be model weights); never read
            # it whole into memory. size is the fingerprinted length the presign signed.
            self.transport.put_file(
                presign["upload_url"],
                path,
                content_type=content_type or "application/octet-stream",
                headers=presign.get("upload_headers") or presign.get("headers"),
            )
        # Confirmed unconditionally, including on the `have` path: the server's confirm
        # returns an already-complete row unchanged (uploads_router.py `_confirm_pending_row`
        # is explicitly idempotent), so this costs one call and buys a single uniform
        # return shape — the stored artifact — across every anchor.
        try:
            return self.transport.post(f"/v1/artifacts/{presign['artifact_id']}/confirm", None)
        except errors.NotFoundError:
            if not presign.get("have"):
                raise
            # `have` means the bytes were already stored and, for a file anchor, already
            # swapped live. A concurrent replace of the same (anchor, name) can then
            # soft-delete this row before the confirm reads it. The upload succeeded;
            # failing here would report a phantom error for work the server did.
            #
            # Return an artifact-shaped row, NOT the presign: the presign carries
            # `upload_url` (a signed, bearer-equivalent write capability) and callers
            # print this — `probe shared add` sends it straight to stdout, where it
            # would land in CI logs. It also has no `id`/`status`, so every caller
            # relying on the documented uniform return shape would KeyError on exactly
            # this race.
            return {
                "id": presign["artifact_id"],
                "name": name,
                "content_hash": digest,
                "size_bytes": size,
                "status": "complete",
                "superseded": True,
            }

    # -- shared folder ------------------------------------------------------
    def share_workspace_file(self, artifact_id: str, *, replace: bool = False) -> dict:
        """Move a workspace file into the team's Shared folder.

        A MOVE, not a copy: ownership transfers and the search index is re-keyed in the
        same transaction, so the file leaves your workspace listing when it lands in
        Shared.

        A name collision in the destination is a 409 by default — the server never
        auto-supersedes someone else's file. ``replace=True`` atomically supersedes
        the prior one, which has to be asked for explicitly.
        """
        return self.transport.request(
            "POST",
            f"/v1/workspace-files/{artifact_id}/share",
            params={"replace": replace} if replace else None,
        ).json()

    def unshare_file(self, artifact_id: str, *, replace: bool = False) -> dict:
        """Move a Shared file into the server default workspace.

        Uses the oldest existing workspace, creating a Default workspace if needed.
        Same collision rule as :meth:`share_workspace_file`, in the other direction.
        """
        return self.transport.request(
            "POST",
            f"/v1/shared/files/{artifact_id}/unshare",
            params={"replace": replace} if replace else None,
        ).json()

    def download_shared_file(self, artifact_id: str) -> dict:
        """Presigned download URL for a Shared file."""
        return self.transport.get(f"/v1/shared/files/{artifact_id}/download")

    def delete_shared_file(self, artifact_id: str) -> None:
        self.transport.delete(f"/v1/shared/files/{artifact_id}")

    def confirm_shared_file(self, artifact_id: str) -> dict:
        """The Shared folder's own confirm door. Equivalent to the generic
        ``/v1/artifacts/{id}/confirm``; both delegate to the same core."""
        return self.transport.post(f"/v1/shared/files/{artifact_id}/confirm", None)

    # -- experiments --------------------------------------------------------
    #
    # THE EXPERIMENT API (light experiments R4). An experiment is read and
    # written as an experiment, under the project it is filed in:
    #
    #   GET    /v1/projects/{P}/experiments            list (offset paged, with a total)
    #   POST   /v1/projects/{P}/experiments            create
    #   GET    /v1/projects/{P}/experiments/{E}        one (uuid, slug or legacy slug)
    #   PATCH  /v1/projects/{P}/experiments/{E}        edit; `project_id` moves it
    #   DELETE /v1/projects/{P}/experiments/{E}        move to the trash
    #   GET    /v1/scopes/{id}                         where an id is filed
    #   GET    /v1/projects/{P}/workspace?scope=...    T16: one scope in one read
    #
    # Nothing here addresses an experiment as a project (`/v1/projects/{E}`):
    # from the server's R4 refusal on, an older client that does is answered
    # 410 `client_too_old`. Two things still go through that address because
    # the experiment API has no field for them yet, and the server serves them
    # to this client until R6: the experiment's `document` (a block of its
    # Overview page) and the child routes (runs, groups, edges, files, notes
    # history, versions). See `agent/CHANGELOG.md` for the list.
    #
    # The writes take uuids only (the server refuses a slug in either slot:
    # a slug can be minted again once its holder is in the trash), so a slug is
    # resolved to its id first.

    def get_scope(self, scope_id: str) -> dict:
        """What a project, experiment or run id is, and where it is filed:
        ``{id, kind: project|experiment|run, project_id, experiment_id, run_id}``.

        ``GET /v1/scopes/{id}``. 404 for an id the caller cannot see, 410 with the
        trash notice for one in the trash. ``project_id`` is null only for an
        unfiled run."""
        return self.transport.get(f"/v1/scopes/{scope_id}")

    def get_scope_by_slug(self, slug: str) -> dict:
        """The project or experiment ``slug`` names, tenant-wide, in the same
        shape as :meth:`get_scope`: a live experiment slug, else a project's,
        else the slug an experiment had before a rename.

        ``GET /v1/scopes?slug=``. 404 when nothing the caller can see holds it,
        410 with the trash notice when the holder is in the trash. Raises
        ``CapabilityUnavailable`` against a server that predates the route."""
        try:
            return self.transport.get("/v1/scopes", params={"slug": slug})
        except errors.NotFoundError as exc:
            if _route_absent(exc):
                raise CapabilityUnavailable(
                    "scope_by_slug", "this Probe server has no GET /v1/scopes?slug= yet"
                ) from None
            raise

    def _experiment_scope(self, slug: str) -> dict | None:
        """The scope of the EXPERIMENT ``slug`` names, or None (nothing holds it,
        the holder is in the trash, or a project holds it). Raises
        ``CapabilityUnavailable`` against an older server."""
        try:
            scope = self.get_scope_by_slug(slug)
        except errors.NotFoundError:
            return None
        except errors.RosError as exc:
            if exc.in_trash:
                return None
            raise
        if scope.get("kind") != _ScopeKind.experiment.value or not scope.get("project_id"):
            return None
        return scope

    def get_project_workspace(
        self,
        project_id: str,
        *,
        scope: str | None = None,
        runs_limit: int | None = None,
        runs_offset: int | None = None,
        files_limit: int | None = None,
        include_experiments: bool | None = None,
    ) -> dict:
        """One scope of a project in one read (the T16 workspace read model).

        Not :meth:`get_workspace`, which reads a WORKSPACE (the place projects
        are filed); this reads a project's page for one of its scopes.

        ``scope`` is ``project:<id>`` (the default), ``experiment:<id>`` or
        ``run:<id>``, and must be inside the project. Answers ``{project_id,
        scope, writable, experiments, runs: {ids, total, limit, offset,
        next_offset, series_cap}, question, summary, files}``: the project's
        experiments with run counts (null with ``include_experiments=False``),
        the run ids in scope newest first (at most ``series_cap`` per page, the
        most one series query takes), the experiment's question, the scope's
        overview status and the root of its Files tree."""
        params = {
            key: value
            for key, value in {
                "scope": scope,
                "runs_limit": runs_limit,
                "runs_offset": runs_offset,
                "files_limit": files_limit,
                "include_experiments": (
                    None if include_experiments is None else str(include_experiments).lower()
                ),
            }.items()
            if value is not None
        }
        return self.transport.get(f"/v1/projects/{project_id}/workspace", params=params or None)

    def _locate_experiment(self, ref: str, project_id: str | None) -> tuple[str, str]:
        """``(project id, experiment ref)`` for an experiment the caller named.

        With the project known, the ref goes to the server as given (the item
        route takes a uuid, slug or legacy slug). Without it, ONE request places
        it: ``GET /v1/scopes/{id}`` for a uuid, ``GET /v1/scopes?slug=`` for a
        slug. Only a server older than that route makes a slug cost a walk of
        the caller's projects (:meth:`_tenant_experiments`)."""
        ref = str(ref)
        if project_id:
            return str(project_id), ref
        if _is_uuid(ref):
            scope = self.get_scope(ref)
            if scope.get("kind") != _ScopeKind.experiment.value or not scope.get("project_id"):
                raise errors.NotFoundError(
                    f"no experiment with id {ref!r}: that id is a {scope.get('kind') or 'something else'}"
                )
            return str(scope["project_id"]), ref
        try:
            scope = self._experiment_scope(ref)
        except CapabilityUnavailable:
            row = self._walk_for_slug(ref)
            if row is None:
                raise errors.NotFoundError(f"no experiment {ref!r}") from None
            return str(row["project_id"]), str(row["id"])
        if scope is None:
            raise errors.NotFoundError(f"no experiment {ref!r}")
        return str(scope["project_id"]), str(scope.get("experiment_id") or scope["id"])

    def _experiment_ids(self, ref: str, project_id: str | None) -> tuple[str, str]:
        """``(project uuid, experiment uuid)``: what the experiment API's writes take."""
        project, experiment = self._locate_experiment(ref, project_id)
        if not _is_uuid(experiment) or not _is_uuid(project):
            row = self.get_experiment(experiment, project_id=project)
            project, experiment = str(row["project_id"]), str(row["id"])
        return project, experiment

    def _tenant_experiments(self, *, stop_at: str | None = None) -> list[dict]:
        """Every experiment the caller can see, project by project.

        The experiment API lists experiments PER PROJECT, so this reads the
        project list (it never holds an experiment) and each project's
        experiments, :data:`_WALK_CONCURRENCY` projects at a time. Paid only
        where a whole list is the question -- the near-miss guard, a
        project-less ``list_experiments`` -- or against a server older than
        ``GET /v1/scopes?slug=``. ``stop_at`` ends the walk at the first batch
        holding that live slug. A project trashed or hidden mid-walk is skipped.
        Inside :func:`_one_walk` a complete walk is fetched once."""
        memo = _WALK_MEMO.get()
        if memo is not None and id(self) in memo:
            return memo[id(self)]
        projects = [str(row["id"]) for row in self._all_slugs("project")]
        rows: list[dict] = []
        complete = True
        if projects:
            with ThreadPoolExecutor(max_workers=min(_WALK_CONCURRENCY, len(projects))) as pool:
                for start in range(0, len(projects), _WALK_CONCURRENCY):
                    batch = projects[start : start + _WALK_CONCURRENCY]
                    # Each task in a COPY of this context: the hosted MCP binds the
                    # caller's client headers in a context variable, and a bare
                    # worker thread would report the server's own version instead.
                    futures = [
                        pool.submit(contextvars.copy_context().run, self._experiments_of, pid)
                        for pid in batch
                    ]
                    for future in futures:
                        rows.extend(future.result())
                    if stop_at is not None and any(r.get("slug") == stop_at for r in rows):
                        complete = start + _WALK_CONCURRENCY >= len(projects)
                        break
        if complete and memo is not None:
            memo[id(self)] = rows
        return rows

    def _experiments_of(self, project_id: str) -> list[dict]:
        """One project's experiments, every page; [] for a project that went
        away (404) or into the trash (410) since the project list was read."""
        rows: list[dict] = []
        offset = 0
        while True:
            try:
                page = self.transport.get(
                    f"/v1/projects/{project_id}/experiments",
                    params={"limit": _EXPERIMENT_PAGE_MAX, "offset": offset},
                )
            except errors.NotFoundError:
                return rows
            except errors.RosError as exc:
                if exc.in_trash:
                    return rows
                raise
            rows.extend(_from_experiment_api(item) for item in page.get("items") or [])
            next_offset = page.get("next_offset")
            if next_offset is None:
                return rows
            offset = next_offset

    def _walk_for_slug(self, slug: str) -> dict | None:
        """The experiment ``slug`` names, found by walking (an older server only)."""
        return self._find_experiment(self._tenant_experiments(stop_at=slug), slug)

    @staticmethod
    def _find_experiment(rows: Iterable[dict], slug: str) -> dict | None:
        """The experiment ``slug`` names: its slug, else the slug it had before a
        rename (``legacy_slug``) -- second, as the server's resolvers rank them,
        so a live slug outranks somebody's remembered name for another row."""
        rows = list(rows)
        for row in rows:
            if row.get("slug") == slug:
                return row
        for row in rows:
            if row.get("legacy_slug") == slug:
                return row
        return None

    def create_experiment(
        self,
        slug: str,
        name: str | None = None,
        *,
        question: str | None = None,
        project_id: str,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        authored_by: str | None = None,
    ) -> dict:
        """Create an experiment in a project. Raises ``ConflictError`` if the slug is taken.

        ``POST /v1/projects/{project_id}/experiments``. The question is REQUIRED
        and is not synthesised. This used to accept ``None`` and compose a marked
        ``[auto]`` placeholder from ambient context, which then became permanent:
        an existing experiment keeps its own question first-write-wins, so
        nothing ever replaced the placeholder unless a human noticed and ran
        ``probe experiment set``. Making creation explicit means naming what you
        are testing at the moment you create it.

        Slugs are one namespace with project slugs, tenant-wide. On a 409 the
        error's ``existing`` names the holder (``id``, ``parent_project_id``,
        ``kind``); it is this experiment only when ``kind`` is ``experiment``
        and ``parent_project_id`` is ``project_id``.

        ``document`` seeds authored Markdown that lives INSIDE the experiment's
        Overview page, as a block the page's AI writer may not rewrite (written
        right after the create; the experiment API has no field for it yet). A
        README embed in that document also derives the experiment's repo, using
        the same syntax documented by :meth:`update_experiment`.

        ``tags`` and ``description`` are refused: an experiment's tags are kept
        read-only since it moved to its own record, and its question replaced
        its description."""
        if not question:
            raise errors.ValidationError(
                f"an experiment needs a question: what do you expect {slug} to show?"
            )
        if not project_id:
            raise errors.ValidationError(
                "an experiment needs an explicit project_id; create or resolve the project first"
            )
        if description is not None:
            raise ValueError(_EXPERIMENT_DESCRIPTION_RETIRED)
        _refuse_read_only_experiment_fields(tags=tags)
        body: dict[str, Any] = {"slug": slug, "question": question}
        # See create_project: omitted, never the slug. Same reason.
        if name:
            body["name"] = name
        _put_authorship(body, authored_by)
        row = _from_experiment_api(
            self.transport.post(f"/v1/projects/{project_id}/experiments", body)
        )
        if document is not None:
            try:
                row["document"] = self._write_experiment_document(
                    str(row["id"]), document, authored_by
                )
            except errors.RosError as exc:
                raise errors.DocumentNotWritten(
                    f"experiment {slug!r} was created ({row['id']}), but its document was "
                    f"not written: {exc}. Write it with `probe experiment set "
                    f"{shlex.quote(slug)} --summary <markdown or @file>` (SDK: "
                    f"update_experiment({str(row['id'])!r}, document=...)); creating it "
                    "again would only meet its own slug.",
                    experiment=row,
                    status=exc.status,
                ) from exc
        return row

    def _write_experiment_document(
        self, experiment_id: str, document: str, authored_by: str | None
    ) -> str | None:
        """Write an experiment's Overview-page block and check it landed.

        THROUGH THE PROJECT ADDRESS, on purpose and for now: the experiment API
        takes no `document`, and the server keeps this write working for a
        client at or above its experiment floor until R6. The check reads the
        write's OWN row: a detail GET answers from the page, a lossy rendering of
        what was sent (see :meth:`update_project`)."""
        body: dict[str, Any] = {"document": document}
        _put_authorship(body, authored_by)
        written = self.transport.patch(f"/v1/projects/{experiment_id}", body)
        self._verify_entity_markdown_written(
            "experiment", document, written, "PATCH /v1/projects/{id}"
        )
        return written.get("document") if isinstance(written, dict) else None

    def resolve_experiment(
        self, slug: str, *, strict: bool = False, project_id: str | None = None
    ) -> dict | None:
        """Look an experiment up by slug. ``None`` when it does not exist.

        With ``project_id``, one request: ``GET /v1/projects/{P}/experiments/{slug}``
        (None when it is not filed there, or is in the trash). Without it,
        experiment slugs are unique per TENANT: ``GET /v1/scopes?slug=`` places
        it and its project's item route reads it (two requests). Against a
        server older than that route, the caller's projects are walked.

        A slug an experiment had before a rename (``legacy_slug``) resolves too,
        after every live slug, as it does on the server. ``strict`` is accepted
        for callers of the old signature; there is no unfiltered listing left
        for it to guard against."""
        del strict
        if project_id:
            try:
                row = self.transport.get(f"/v1/projects/{project_id}/experiments/{slug}")
            except errors.NotFoundError:
                return None
            except errors.RosError as exc:
                if exc.in_trash:
                    # In the trash: its slug was moved aside and is free again.
                    return None
                raise
            return self._find_experiment([_from_experiment_api(row)], slug)
        try:
            scope = self._experiment_scope(slug)
        except CapabilityUnavailable:
            return self._walk_for_slug(slug)
        if scope is None:
            return None
        try:
            return self.get_experiment(
                str(scope.get("experiment_id") or scope["id"]), project_id=str(scope["project_id"])
            )
        except errors.NotFoundError:
            return None  # gone between the two reads

    @_walks_once
    def ensure_experiment(
        self,
        slug: str,
        name: str | None = None,
        *,
        question: str,
        project_id: str,
        **kw,
    ) -> dict:
        """Get-or-create an experiment by slug in a project. SDK-only; see :meth:`run`.

        ``question`` is REQUIRED and keyword-only: reaching this method means
        creation is on the table, and an experiment is never created without one.
        It is NOT applied to an experiment that already exists — those are
        first-write-wins, so reopening never rewrites the question. Nothing is
        synthesised; the ``[auto]`` placeholder was permanent unless a human
        noticed it, which is why it is gone.

        A slug that resolves to nothing but looks like a typo of an existing one
        is REFUSED, not created — see :meth:`_refuse_near_miss`. A create that
        loses a race adopts the winner only when it is an experiment filed in
        this same project (the server's 409 names the holder); a slug held by a
        project, or by an experiment in another project, raises. Callers who want
        the strict three-outcome error for an absent slug use
        :meth:`resolve_or_raise` instead."""
        found = self.resolve_experiment(slug, project_id=project_id)
        if found is not None:
            return found
        self._guard_creatable("experiment", slug)
        try:
            return self.create_experiment(
                slug, name, question=question, project_id=project_id, **kw
            )
        except errors.ConflictError as exc:
            holder = exc.existing if isinstance(exc.existing, dict) else {}
            if holder.get("kind") != _ProjectKind.experiment.value:
                raise
            if str(holder.get("parent_project_id")) != str(project_id):
                raise errors.ValidationError(
                    f"experiment {slug!r} already exists in another project "
                    f"({holder.get('parent_project_id')}), not in {project_id}. Name "
                    "the project it belongs to, or choose another slug."
                ) from exc
            # Lost a create race to the same experiment; see ensure_project.
            return self.get_experiment(
                str(holder.get("id") or exc.existing_id), project_id=project_id
            )

    def get_experiment(self, experiment_id: str, *, project_id: str | None = None) -> dict:
        """One experiment: identity, question, notes, run count, overview status.

        ``GET /v1/projects/{P}/experiments/{E}``, the project from ``project_id``
        or ``GET /v1/scopes/{E}``. ``experiment_id`` may also be its slug. The
        row names the project it is filed under as ``project_id`` (and, for
        callers of the project address, as ``parent_project_id``)."""
        project, experiment = self._locate_experiment(experiment_id, project_id)
        return _from_experiment_api(
            self.transport.get(f"/v1/projects/{project}/experiments/{experiment}")
        )

    def get_experiment_document(self, experiment_id: str) -> str | None:
        """The experiment's authored Markdown (``document=``), as its Overview page
        holds it; None when it has none.

        :meth:`get_experiment` no longer carries it: the experiment API serves
        the page (HTML) and not the authored block the server cuts out of it.
        This reads it at the experiment's PROJECT address, which the server keeps
        serving this client until R6. Not byte-identical to what was sent: the
        page renders it (see :meth:`update_project`)."""
        row = self.get_experiment_leaf(experiment_id)
        return row.get("document") if isinstance(row, dict) else None

    def get_experiment_leaf(self, experiment_id: str) -> dict:
        """The experiment as its PROJECT address answers it (``GET /v1/projects/{E}``).

        For the two things only that read still carries: the authored
        ``document`` and the notes' headroom pair (``notes_limit_chars``,
        ``notes_remaining_chars``). The server keeps it answering this client
        until R6; everything else about an experiment is :meth:`get_experiment`."""
        experiment = str(experiment_id)
        if not _is_uuid(experiment):
            experiment = self._experiment_ids(experiment, None)[1]
        return self.transport.get(f"/v1/projects/{experiment}")

    def get_experiment_overview(
        self, experiment_id: str, *, project_id: str | None = None, status_only: bool = False
    ) -> dict:
        """The experiment's Overview page (``OverviewOut``, the same shape as a
        project's), or with ``status_only`` just its freshness and queue state.

        ``GET /v1/projects/{P}/experiments/{E}/overview[/status]``. Its
        ``anchor_type`` reads ``project`` before the server's R3 switch and
        ``experiment`` after; never branch on it."""
        project, experiment = self._locate_experiment(experiment_id, project_id)
        if status_only:
            return self.transport.get(
                f"/v1/projects/{project}/experiments/{experiment}/overview/status"
            )
        return self.transport.get(f"/v1/projects/{project}/experiments/{experiment}/overview")

    def update_experiment(
        self,
        experiment_id: str,
        *,
        question: str | None = None,
        name: str | None = None,
        description: str | None = None,
        document: str | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        summary: dict | None = None,
        authored_by: str | None = None,
        project_id: str | None = None,
    ) -> dict:
        """Amend an experiment's question, name or visible Markdown.

        ``question`` and ``name`` go to ``PATCH /v1/projects/{P}/experiments/{E}``.

        ``document`` replaces the authored Markdown that lives INSIDE the
        experiment's Overview page, as a block the page's AI writer may not
        rewrite. It is whole-document and last-write-wins, separate from the
        experiment's private Notes. Read immediately before editing and preserve
        useful sections; ``""`` clears it. A line containing only
        ``[README](https://github.com/owner/repo)`` embeds that README and derives
        the experiment's read-only ``repo`` field. (Written through the project
        address: the experiment API has no field for it yet.)

        DO NOT expect a read-back to be byte-identical: a detail GET answers
        from the page, which renders the document -- see :meth:`update_project`.

        ``tags``, ``metadata`` and ``summary`` are refused: the server keeps an
        experiment's tags and metadata read-only since it moved to its own
        record. ``description`` is refused too: the question replaced it."""
        if description is not None:
            raise ValueError(_EXPERIMENT_DESCRIPTION_RETIRED)
        _refuse_read_only_experiment_fields(tags=tags, metadata=metadata, summary=summary)
        identity = {
            key: value
            for key, value in {"question": question, "name": name}.items()
            if value is not None
        }
        if not identity and document is None:
            raise ValueError("update_experiment needs at least one field to set")
        project, experiment = self._experiment_ids(experiment_id, project_id)
        row: dict | None = None
        if identity:
            # AFTER the emptiness check, deliberately. `authored_by` declares who
            # wrote the OTHER fields; on its own it declares authorship of nothing.
            _put_authorship(identity, authored_by)
            row = _from_experiment_api(
                self.transport.patch(
                    f"/v1/projects/{project}/experiments/{experiment}", identity
                )
            )
        if document is not None:
            try:
                written = self._write_experiment_document(experiment, document, authored_by)
            except errors.RosError as exc:
                if row is None:
                    raise  # nothing landed: the one failure is the whole answer
                raise errors.DocumentNotWritten(
                    f"experiment {row.get('slug') or experiment!r} ({experiment}): "
                    f"{' and '.join(sorted(k for k in identity if k != 'authored_by'))} "
                    f"changed, but its document was not written: {exc}. Write it with "
                    f"`probe experiment set {shlex.quote(str(row.get('slug') or experiment))} "
                    "--summary <markdown or @file>`.",
                    experiment=row,
                    status=exc.status,
                ) from exc
            if row is None:
                row = self.get_experiment(experiment, project_id=project)
            row["document"] = written
        assert row is not None
        return row

    def move_experiment(
        self, experiment_id: str, project_id: str, *, from_project_id: str | None = None
    ) -> dict:
        """Move an experiment, with its runs, files and groups, to another project.

        ``PATCH /v1/projects/{from}/experiments/{E}`` with ``{project_id}``: one
        statement on the server. Needs edit access on both projects (403); a
        target that is an experiment is 422, one in the trash 410, a project
        being purged 409, and a move under a restricted project revokes the
        experiment's public share. Answers the experiment filed under its new
        project. ``project_id`` is the TARGET's uuid; ``from_project_id`` saves
        the lookup of where it is now."""
        if not project_id:
            raise ValueError("move_experiment needs the target project's id")
        project, experiment = self._experiment_ids(experiment_id, from_project_id)
        return _from_experiment_api(
            self.transport.patch(
                f"/v1/projects/{project}/experiments/{experiment}",
                {"project_id": str(project_id)},
            )
        )

    def list_experiments(
        self,
        *,
        project_id: str | None = None,
        tags: list[str] | None = None,
        name: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        **params,
    ) -> Page:
        """A project's experiments, newest first; with no ``project_id``, every
        project's.

        ``GET /v1/projects/{project_id}/experiments``, offset paged (at most 500
        per page): pass a page's ``next_cursor`` back as cursor= for the next one,
        an opaque token. Without a
        project, the caller's projects are walked (:meth:`_tenant_experiments`):
        one request per project, sorted newest first, then paged here.

        ``name`` keeps rows whose name matches exactly (case-insensitive).
        ``tags`` is refused: an experiment's tags are read-only since it moved to
        its own record, and the experiment API filters on none."""
        if tags:
            _refuse_read_only_experiment_fields(tags=tags)
        if params:
            raise ValueError(
                f"list_experiments takes project_id, name, limit and cursor; "
                f"{', '.join(sorted(params))} is not a filter of the experiment list"
            )
        offset = _offset_cursor(cursor)
        if project_id is not None:
            query: dict[str, Any] = {"offset": offset}
            if limit is not None:
                query["limit"] = limit
            page = self.transport.get(f"/v1/projects/{project_id}/experiments", params=query)
            items = [_from_experiment_api(item) for item in page.get("items") or []]
            if name is not None:
                items = [row for row in items if _same_name(row, name)]
            next_offset = page.get("next_offset")
            return Page(items=items, next_cursor=None if next_offset is None else str(next_offset))
        rows = self._tenant_experiments()
        if name is not None:
            rows = [row for row in rows if _same_name(row, name)]
        rows.sort(key=lambda row: (str(row.get("created_at") or ""), str(row["id"])), reverse=True)
        size = limit if limit is not None else _EXPERIMENT_PAGE_DEFAULT
        window = rows[offset : offset + size]
        more = offset + size < len(rows)
        return Page(items=window, next_cursor=str(offset + size) if more else None)

    def delete_experiment(
        self,
        experiment_id: str,
        *,
        project_id: str | None = None,
        dry_run: bool = False,
        reason: str | None = None,
    ) -> dict | None:
        """Move an experiment, its runs, groups, files, notes and page to the
        server's TRASH. Frees the slug.

        ``DELETE /v1/projects/{P}/experiments/{E}``. Probe support can restore it
        for 21 days (the returned receipt says until when); after that it is
        deleted for good. ``dry_run=True`` changes nothing and answers what would
        go and whose it is. 409 if a published experiment version outside this
        experiment pins something under it, or a live W&B mirror is bound to it."""
        project, experiment = self._experiment_ids(experiment_id, project_id)
        params: dict[str, str] = {}
        if dry_run:
            params["dry_run"] = "true"
        if reason:
            params["reason"] = reason
        if not params:
            return self.transport.delete(f"/v1/projects/{project}/experiments/{experiment}")
        resp = self.transport.request(
            "DELETE",
            f"/v1/projects/{project}/experiments/{experiment}",
            params=params,
            idempotent=True,
        )
        return resp.json() if resp.content else None

    def experiment_edges(self, experiment_id: str, *, limit: int | None = None) -> list[dict]:
        """Every lineage edge under an experiment (the run-level view is
        :meth:`run_edges`); at most ``limit`` (1-1000) when given, stored edges
        first. The experiment's OWN links are :meth:`project_lineage`.

        Still read at the project address: the experiment API has no edges
        route yet, and the server serves this one to this client until R6."""
        params = {"limit": limit} if limit is not None else None
        return self.transport.get(f"/v1/projects/{experiment_id}/edges", params=params)

    # -- run groups (sweeps / ensembles) ------------------------------------
    @staticmethod
    def _warn_if_notes_dropped(sent: str | None, row: dict, what: str) -> None:
        """Surface the silent drop when the backend predates research-os 0096.

        Neither RunPatch/RunCreate nor the group schemas forbid extra fields, so an
        older backend ACCEPTS `notes`, ignores it, and answers 2xx -- the caveat
        vanishes and the caller is told it succeeded. This is the 0094 hazard, and
        the check is free: create and PATCH both return the row, so nothing extra
        is fetched.

        WARN rather than raise, unlike `set_project_notes`. That call's only effect
        is the notes write, so failing it loses nothing. These calls have already
        created or mutated the entity by the time the response is in hand -- raising
        would leave a run created on the server and an exception in the caller's
        lap, which is worse than a dropped note.
        """
        if sent is None or "notes" in row:
            return
        warnings.warn(
            f"this research-os backend predates `notes` on {what} (0096): it "
            "accepted the field, ignored it, and answered 2xx, so the note was "
            "NOT stored. Upgrade the backend to >= 0.107.0.0.",
            stacklevel=3,
        )

    def create_group(
        self,
        experiment_id: str,
        name: str,
        *,
        kind: str = "group",
        spec: dict | None = None,
        notes: str | None = None,
    ) -> dict:
        """Create a run group under an experiment — coordination metadata for a
        sweep or ensemble; ``spec`` holds e.g. the search space.

        Pass the returned ``id`` to :meth:`create_run` as ``group_id`` to file a run
        under it. 409 if the name is taken within the experiment.

        ``notes`` (server 0096) is free text about the sweep itself — what varies,
        what it was testing, why it was abandoned. Put it HERE rather than in
        ``name``: the name is part of the group's uniqueness key within the
        experiment, so a description appended to it does not merely read badly, it
        changes the row's identity and mints a second group instead of colliding
        with the one it describes."""
        model = RunGroupCreate(name=name, kind=kind, spec=spec or {}, notes=notes)
        row = self.transport.post(
            f"/v1/projects/{experiment_id}/groups",
            model.model_dump(mode="json", exclude_none=True),
        )
        self._warn_if_notes_dropped(notes, row, "run groups")
        return row

    def list_groups(self, experiment_id: str) -> list[dict]:
        return self.transport.get(f"/v1/projects/{experiment_id}/groups")

    def get_group(self, group_id: str) -> dict:
        return self.transport.get(f"/v1/groups/{group_id}")

    def update_group(
        self,
        group_id: str,
        *,
        name: str | None = None,
        spec: dict | None = None,
        notes: str | None = None,
    ) -> dict:
        """Field-replace PATCH: only the fields you pass change.

        ``notes`` is the field most likely to be written here rather than at
        create — what a sweep was actually testing tends to be known after it has
        run. Omitting it leaves any existing note alone; passing ``""`` clears it."""
        # THE GUARD READS THE CALLER'S ARGUMENTS, not the dumped model. The
        # generated model tracks the backend's, and the backend added `force`
        # with a default of `False` -- which `exclude_none` keeps, so the body
        # was never empty and an argumentless `update_group()` stopped raising
        # and started PATCHing a group with nothing in it.
        if name is None and spec is None and notes is None:
            raise ValueError("update_group needs at least one of name/spec/notes")
        model = RunGroupPatch(name=name, spec=spec, notes=notes)
        body = model.model_dump(mode="json", exclude_none=True)
        row = self.transport.patch(f"/v1/groups/{group_id}", body)
        self._warn_if_notes_dropped(notes, row, "run groups")
        return row

    # -- runs (create) ------------------------------------------------------
    @staticmethod
    def _run_create_body(
        name: str | None,
        *,
        description: str | None,
        notes: str | None,
        source: str,
        external_id: str | None,
        parent_run_id: str | None,
        parent_relation: str | None,
        group_id: str | None,
        config: dict | None,
        tags: list[str] | None,
        metadata: dict | None,
        labeled_point_budget: int | None,
        slug: str | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        authored_by: str | None = None,
        parent_provenance: str | None = None,
    ) -> dict[str, Any]:
        # 0268 (plan 2.5): a fresh key per create, so the SAME body can be sent
        # again when its response is lost and the server hands back the run it
        # already made instead of a second one. Sent always: a server that
        # predates the field ignores it, and the re-send is gated on the
        # feature (`_create_idempotently`), never on the key being present.
        body: dict[str, Any] = {"source": source, "creation_key": uuid.uuid4().hex}
        # Stamped even when `name` is omitted: `authored_by` also governs
        # `description_customized`, and a run created with a description and no
        # name still has an authored field on it.
        _put_authorship(body, authored_by)
        # OMITTED, not null: `name` is optional server-side since 0080, and leaving
        # it out is the only way to say "the server picks it". Sending it -- with
        # any value -- stamps `name_customized` and takes the run out of generated
        # titles permanently. `min_length=1` on the server field also means an
        # explicit null and an empty string are not interchangeable here.
        if name is not None:
            body["name"] = name
        # The run's own slug (server 0.110.0.0), stored in the `slug` column.
        # Omitted = the server mints a petname, which stays the normal case. A
        # TAKEN one is a 409, never a silent substitution.
        if slug is not None:
            body["slug"] = slug
        if description is not None:
            body["description"] = description
        # Separate from `description` on purpose (server 0096): a description says
        # what the run IS, notes is the caveat a later reader needs ("suspect, the
        # dataloader was stale"). With one field the two compete.
        if notes is not None:
            body["notes"] = notes
        if external_id is not None:
            body["external_id"] = external_id
        if parent_run_id is not None:
            # NO DEFAULT. This read `parent_relation or "fork"` and quietly stamped
            # `fork` on every parent whose relation the caller left unset -- turning
            # the server's 422 (`RunCreate._parent_pair`, mirrored by
            # `runs_parent_pair_chk`) into a silent success carrying a word nobody
            # chose. The miles integration hit it exactly: its own comment says none
            # of the four honestly describes "evaluated this run's checkpoint", so it
            # deliberately omitted the relation, and this line supplied `fork` anyway.
            if not parent_relation:
                raise errors.ValidationError(
                    "parent_run_id needs parent_relation — fork, resume, retry or "
                    "branch. They mean different things and a guess is stored as a "
                    "claim. If this run CONSUMED the parent's output rather than "
                    "re-attempting it (an eval of its checkpoint, training on its "
                    "rollouts), that is a lineage edge, not parentage: use "
                    "`probe edge add --relation consumes`."
                )
            body["parent_run_id"] = parent_run_id
            body["parent_relation"] = parent_relation
            if parent_provenance is not None:
                # How the parent is known (server 0255): `observed_call` when
                # the SDK derived it itself; omitted means the caller declared it.
                body["parent_provenance"] = parent_provenance
        if group_id is not None:
            body["group_id"] = group_id
        if config is not None:
            # Plan (c): a Namespace, dataclass, DictConfig or numpy leaf used to
            # reach the server as one repr() string (or a 422). Every create
            # path funnels through here; a dict that is already plain comes
            # back equal.
            body["config"] = _coerce.to_config(config)
        if tags is not None:
            body["tags"] = tags
        if metadata is not None:
            body["metadata"] = metadata
        # Per-run labeled-point budget (server 0061): a run that will log more
        # per-sample points than the server default declares its plan up front.
        if labeled_point_budget is not None:
            body["labeled_point_budget"] = labeled_point_budget
        # 0205. The server DERIVES liveness_mode from signals rather than taking
        # a label, and this is the signal: "this process will beat for the run"
        # gets last_heartbeat_at stamped at insert, so an owned run is never
        # momentarily indistinguishable from an unowned one. Sent only when
        # true, so a pre-0205 server sees the request it always saw.
        if heartbeat:
            body["heartbeat"] = True
        if launcher:
            # A fact about the CALLER, not a mode: "I am wrapping a child".
            body["launcher"] = True
        if awaiting_attach:
            # A hand-off: the row is for a job that has not started. Nothing owns
            # it yet, so it lands 'created' and the sweep is the backstop.
            body["awaiting_attach"] = True
        return body

    def _wrap_run(
        self,
        data: dict,
        *,
        heartbeat: bool,
        attached: bool = False,
        session_id: str | None = None,
        lease: dict | None = None,
        lease_registered: bool = False,
        lease_protocol: str | None = None,
    ) -> Run:
        run = Run(self, data)
        run._lease_registered = lease_registered
        # Which rules the run follows, as far as this process knows: `leases`
        # for a create that carried the lease, else unknown until a lease beat
        # answers (an unknown protocol closes the pre-2.8 way).
        run._lease_protocol = lease_protocol
        # The writer session BEFORE the beat starts: a lease beat names it, and
        # 2.2's writer-gone report and the capture record carry the same id.
        if session_id is not None:
            run.session_id = str(session_id)
        # 2.8: this handle writes under a lease (its beats and its close go to
        # /writers/{session}); None keeps the run-level heartbeat.
        run._lease = lease
        # 0205. Marks every beat this handle sends as coming from inside the
        # work. Set only by the env-attach path; a launcher's handle leaves it
        # False so its beats keep the run live without claiming the job itself
        # ever reported.
        run.attached = attached
        # A handle minted here is presumed to live and die with this process, so
        # it beats by default and the server's reaper can flip it to 'crashed'
        # when the process dies. Pass heartbeat=False when the run is DETACHED —
        # created here but executed and finished from somewhere else (CLI
        # `run start`, the miles exporter) — because beating briefly and then
        # going silent gets a legitimately-running run reaped.
        #
        # `heartbeat` also decides which tier of the auto-update run lock applies,
        # and it is exactly the right question: a run that lives and dies with
        # this process can hold an flock the kernel releases on death, while a
        # detached one has no process to hold anything and needs a renewable
        # lease. This is the single construction boundary, so every path that
        # opens a run — client.run(), probe.init(), a directly built handle —
        # is covered by it.
        run._hold_run_lock(process_bound=heartbeat)
        if heartbeat:
            # OUTSIDE `probe.init()`'s retry budget (plan 2.5): where a thread
            # inherits its creator's context (free-threaded 3.14), a beat thread
            # started inside it would carry init's deadline for the whole run.
            with without_patience():
                run.start_heartbeat(attached=attached)
        # Every run open in this process counts when deciding whether spawned
        # workers may be bound to one (lineage plan 3, F5): a second run --
        # recording or not -- and a worker's reads belong to neither for sure.
        from . import _open_runs

        _open_runs.opened(run)
        return run

    def create_run(
        self,
        experiment_id: str,
        name: str | None,
        *,
        description: str | None = None,
        notes: str | None = None,
        source: str = "api",
        external_id: str | None = None,
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        parent_provenance: str | None = None,
        group_id: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        labeled_point_budget: int | None = None,
        slug: str | None = None,
        authored_by: str | None = None,
    ) -> Run:
        """Create an experiment-attached run.

        0220: a run carries no authored document. Projects and experiments
        keep theirs as ``document``, which is the Overview page's marked block.
        """
        body = self._run_create_body(
            name,
            slug=slug,
            description=description,
            notes=notes,
            source=source,
            external_id=external_id,
            parent_run_id=parent_run_id,
            parent_relation=parent_relation,
            parent_provenance=parent_provenance,
            group_id=group_id,
            config=config,
            tags=tags,
            metadata=metadata,
            labeled_point_budget=labeled_point_budget,
            heartbeat=heartbeat,
            awaiting_attach=awaiting_attach,
            launcher=launcher,
            authored_by=authored_by,
        )
        session_id, lease = self._lease_for_create(
            body, heartbeat=heartbeat, awaiting_attach=awaiting_attach, launcher=launcher
        )
        data = self._create_idempotently(
            # Literal call site: the tests/test_parity.py AST scan must see the route.
            lambda replay: self.transport.post(
                f"/v1/projects/{experiment_id}/runs", body, idempotent=replay
            ),
            path=f"/v1/projects/{experiment_id}/runs",
            body=body,
        )
        self._verify_slug_written(slug, data)
        self._warn_if_notes_dropped(notes, data, "runs")
        return self._opened(
            self._wrap_run(
                data,
                heartbeat=heartbeat,
                session_id=session_id,
                lease=lease,
                # The create's own transaction wrote it.
                lease_registered=lease is not None,
                # The create carried the lease: the run is on leases.
                lease_protocol="leases" if lease is not None else None,
            )
        )

    #: 0268. The server feature that makes a run create safe to send twice.
    _CREATION_REPLAY_FEATURE = "run_creation_key"

    def _create_idempotently(
        self, send: Callable[[bool], Any], *, path: str | None = None, body: dict | None = None
    ) -> Any:
        """Send a run create once, and AGAIN only when that is provably safe.

        ``send(replay)`` posts the create body, which carries its own
        ``creation_key``; ``replay=True`` lets the transport retry it like a
        read. A create whose outcome is unknown (read timeout, dropped
        connection, 502/503/504 -- ``outcome_unknown``) may have committed, so
        re-sending it is safe only on a server that replays a key it has seen
        (``run_creation_key``). There it comes back with the run it already
        made; anywhere else the failure stands, because a second POST would be
        a second run (or, with an ``external_id``, a 409 against itself).

        The feature is read only on that failure, so a healthy create costs no
        extra request; once the answer is cached, the first send already
        retries.

        A 429 on the first send is re-sent on ANY server: rate limiting refuses
        a request before processing it, so nothing can have landed. Every
        re-send first waits the failure's ``Retry-After`` by the transport's
        own rule for that header: inside init's budget, whenever the budget
        still holds it; outside one, up to the inline cap. When it does not
        fit, the failure is raised at once instead (`wait_out_retry_after`).

        Every create leaves ``_last_run_create`` behind for
        ``PROBE_INIT_FALLBACK=offline`` (plan 2.12): the request as sent, and
        whether it LANDED (``landed``: this client got the run back). One that
        did not land is what the fallback records -- the offline queue keeps it
        and replays it verbatim at sync ONLY if the server says its key already
        made a run (`offline.deliver_create`), so whether a lost answer "may have
        landed" is decided by the server, never guessed here. One that landed
        stops the fallback: recording offline would make a second run."""
        record = {"path": path, "body": body, "landed": False} if path and body else None
        self._last_run_create = record

        def attempt(replay: bool) -> Any:
            created = send(replay)
            if record is not None:
                record["landed"] = True
            return created

        known = getattr(self, "_server_features_cache", None)
        replay_known = known is not None and self._CREATION_REPLAY_FEATURE in known
        try:
            return attempt(replay_known)
        except errors.RosError as exc:
            if replay_known:
                raise  # the transport already retried it within its own policy
            rate_limited = exc.status == 429
            if not rate_limited and not outcome_unknown(exc):
                raise
            try:
                supported = self.supports_feature(self._CREATION_REPLAY_FEATURE)
            except errors.RosError:
                supported = False  # cannot tell: only a 429 is still safe to re-send
            if not (supported or rate_limited):
                raise
            if not wait_out_retry_after(exc, minimum=0.5 if rate_limited else 0.0):
                raise
            replay = supported
        return attempt(replay)

    @staticmethod
    def _opened(run: Run) -> Run:
        """Tell this session's Probe daemon a run just opened (R3.1).

        Every create door ends here, so `probe.init()`, `Client.run()`, `probe
        run start`, `probe exec`, children and forks all announce, exactly once.
        Fire-and-forget: no daemon, no session or any error changes nothing."""
        from . import daemon_channel

        daemon_channel.run_started(getattr(run, "data", None))
        return run

    def create_floating_run(
        self,
        name: str | None,
        *,
        description: str | None = None,
        notes: str | None = None,
        source: str = "api",
        external_id: str | None = None,
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        labeled_point_budget: int | None = None,
        slug: str | None = None,
        authored_by: str | None = None,
    ) -> Run:
        """POST /v1/runs — open a FLOATING run: no project, no experiment (daemon v2, D1).

        The run is its own record from its first second (metrics, spans, files,
        parentage), and is filed afterwards -- by the Probe daemon, or a person
        with `probe run move` -- which moves everything it holds with it. Same
        body as a project-direct run, and like one it cannot join a group.
        """
        body = self._run_create_body(
            name,
            slug=slug,
            description=description,
            notes=notes,
            source=source,
            external_id=external_id,
            parent_run_id=parent_run_id,
            parent_relation=parent_relation,
            group_id=None,
            config=config,
            tags=tags,
            metadata=metadata,
            labeled_point_budget=labeled_point_budget,
            heartbeat=heartbeat,
            awaiting_attach=awaiting_attach,
            launcher=launcher,
            authored_by=authored_by,
        )
        session_id, lease = self._lease_for_create(
            body, heartbeat=heartbeat, awaiting_attach=awaiting_attach, launcher=launcher
        )
        try:
            data = self._create_idempotently(
                # Literal call site: the tests/test_parity.py AST scan must see the route.
                lambda replay: self.transport.post("/v1/runs", body, idempotent=replay),
                path="/v1/runs",
                body=body,
            )
        except errors.RosError as exc:
            # A backend that predates floating runs has GET /v1/runs only, so a
            # POST there is FastAPI's 405 (or a route-level "Not Found" behind a
            # proxy; a handler's own 404, like a missing parent run, says more
            # and passes through). Name the way out instead of "Method Not Allowed".
            if exc.status == 405 or (exc.status == 404 and str(exc).strip().lower() == "not found"):
                raise errors.CapabilityUnavailable(
                    "floating_runs",
                    "this research-os backend predates floating runs (POST /v1/runs). "
                    "Upgrade the backend, or open the run in a project: pass "
                    "project= / experiment= (CLI: --project / --experiment, or "
                    "`probe project use`).",
                ) from exc
            raise
        self._verify_slug_written(slug, data)
        self._warn_if_notes_dropped(notes, data, "runs")
        return self._opened(
            self._wrap_run(
                data,
                heartbeat=heartbeat,
                session_id=session_id,
                lease=lease,
                # The create's own transaction wrote it.
                lease_registered=lease is not None,
                # The create carried the lease: the run is on leases.
                lease_protocol="leases" if lease is not None else None,
            )
        )

    @staticmethod
    def _verify_slug_written(slug: str | None, row: dict) -> None:
        """A backend predating run slugs DROPS the field and names the run itself.

        Pydantic ignores an undeclared body field by default, so the create
        succeeds, returns 201, and hands back a random petname -- and the caller
        exits 0 believing it owns a handle it does not. Reading the stored value
        back is the only thing that tells the two apart.
        """
        if slug is None:
            return
        from .redaction import default_scrub

        expected = default_scrub(slug)
        written = row.get("slug")
        if written != expected:
            raise CapabilityUnavailable(
                f"this backend ignored the run slug {expected!r} (it stored "
                f"{default_scrub(written)!r}); run slugs need research-os >= 0.110.0.0"
            )

    def create_project_run(
        self,
        project_id: str,
        name: str | None,
        *,
        description: str | None = None,
        notes: str | None = None,
        source: str = "api",
        external_id: str | None = None,
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        parent_provenance: str | None = None,
        config: dict | None = None,
        tags: list[str] | None = None,
        metadata: dict | None = None,
        heartbeat: bool = True,
        awaiting_attach: bool = False,
        launcher: bool = False,
        labeled_point_budget: int | None = None,
        slug: str | None = None,
        authored_by: str | None = None,
    ) -> Run:
        """POST /v1/projects/{id}/runs — open a PROJECT-DIRECT run (W&B shape).

        The experiment level is optional grouping; a run opened here attaches
        straight to the project. No ``group_id``: run groups are
        experiment-anchored, so the backend rejects one on a direct run (422).

        0220: a run carries no authored document. Projects and experiments
        keep theirs as ``document``, which is the Overview page's marked block.
        """
        body = self._run_create_body(
            name,
            slug=slug,
            description=description,
            notes=notes,
            source=source,
            external_id=external_id,
            parent_run_id=parent_run_id,
            parent_relation=parent_relation,
            parent_provenance=parent_provenance,
            group_id=None,
            config=config,
            tags=tags,
            metadata=metadata,
            labeled_point_budget=labeled_point_budget,
            heartbeat=heartbeat,
            awaiting_attach=awaiting_attach,
            launcher=launcher,
            authored_by=authored_by,
        )
        session_id, lease = self._lease_for_create(
            body, heartbeat=heartbeat, awaiting_attach=awaiting_attach, launcher=launcher
        )
        try:
            data = self._create_idempotently(
                # Literal call site: the tests/test_parity.py AST scan must see the route.
                lambda replay: self.transport.post(
                    f"/v1/projects/{project_id}/runs", body, idempotent=replay
                ),
                path=f"/v1/projects/{project_id}/runs",
                body=body,
            )
        except errors.NotFoundError as exc:
            # A pre-0054 backend has no such route, and its route-level 404
            # ("Not Found") is indistinguishable from a missing project. The
            # handler's own 404 says "project not found"; anything else means
            # the backend predates the route — say so, and say what to do
            # (the browse/search degraded-backend standard).
            if "project" not in str(exc).lower():
                raise errors.NotFoundError(
                    "this research-os backend predates POST /v1/projects/{id}/runs "
                    "(project-direct runs, 0054). Upgrade the backend, or open "
                    "the run inside an experiment (--experiment / run(experiment=...)).",
                    status=exc.status,
                    detail=exc.detail,
                ) from exc
            raise
        self._verify_slug_written(slug, data)
        self._warn_if_notes_dropped(notes, data, "runs")
        return self._opened(
            self._wrap_run(
                data,
                heartbeat=heartbeat,
                session_id=session_id,
                lease=lease,
                # The create's own transaction wrote it.
                lease_registered=lease is not None,
                # The create carried the lease: the run is on leases.
                lease_protocol="leases" if lease is not None else None,
            )
        )

    @_walks_once
    def run(
        self,
        *,
        experiment: str | None = None,
        question: str | None = None,
        name: str | None = None,
        project: str | None = None,
        experiment_name: str | None = None,
        on_conflict: str | Rewind = "auto",
        hw: bool | None = None,
        snapshot: bool | None = None,
        # Named here rather than left to `**run_kw`. They ALWAYS worked through it
        # -- `_run_impl` splats run_kw straight into `create_run` -- but appeared in
        # no signature, so the only way to learn the door existed was to read
        # `create_run`. Fleet-wide that showed up as one organic hand-declared
        # lineage edge in the whole history, and six runs that wrote
        # `parent_run_id` into `foreign_keys` instead, where no query can follow it.
        parent_run_id: str | None = None,
        parent_relation: str | None = None,
        capture_reads: bool | None = None,
        outputs: str | os.PathLike | None = None,
        capture_outputs: bool | None = None,
        intent: str | None = None,
        ignore: str | list[str] | tuple[str, ...] | None = None,
        **run_kw,
    ) -> Run:
        """Open a run — full resolution/creation/``on_conflict`` semantics in
        :meth:`_run_impl` (unchanged). ``hw=True`` (or ``PROBE_HW=1``) also
        starts the opt-in hardware collector when this process is the
        node-local leader. Best-effort by contract: a broken collector never
        touches the run (docs/2026-08-05-hw-metrics-design.md). ``snapshot``
        controls the open-time auto-snapshot: ``None`` follows
        ``PROBE_AUTO_SNAPSHOT`` (default on), ``False`` skips, ``True`` forces.

        Output capture (D17, :mod:`probe.sdk.outputs`): a run this process owns
        captures what it writes to the working directory -- or to ``outputs``,
        for runs that share a folder -- and everything it prints, when it
        closes. ``capture_outputs=False`` (or ``PROBE_CAPTURE_OUTPUTS=0``) opts
        out. A detached run (``heartbeat=False``, ``awaiting_attach``) captures
        nothing: this process is not the work.

        With NEITHER ``experiment`` NOR ``project`` the run opens FLOATING (daemon
        v2): no home yet, filed afterwards by the Probe daemon or `probe run
        move`. ``intent`` is free text saying what the run is meant to show; it
        rides in the run's ``metadata.intent`` (the run schema has no field for
        it), and the daemon files and describes the run by it.

        ``ignore`` adds gitignore-style patterns to the ``.probeignore`` file at
        the git toplevel and to ``PROBE_IGNORE`` (plan (n)): matching files are
        left out of code capture, output capture and read capture. It only
        excludes -- a credential stays withheld whatever it says -- and an
        explicit ``log_artifact`` or ``snapshot(include=...)`` still wins.
        Inside a ``probe exec`` child (``probe.init(ignore=...)`` joining the
        launcher's run) the patterns reach the launcher's read and output
        capture, but not its code snapshot, taken before the child started:
        put those in ``.probeignore`` or ``PROBE_IGNORE`` (it warns).
        """
        # This process is doing a researcher's run: the scrubber may cache
        # (plan (k); off in every multi-tenant process, see redaction.py).
        from . import redaction as _redaction

        _redaction.enable_scrub_cache()
        if intent is not None:
            if not isinstance(intent, str) or not intent.strip():
                raise errors.ValidationError(
                    "intent= is empty. Say what this run is meant to show, or drop it."
                )
            run_kw["metadata"] = {**(run_kw.get("metadata") or {}), "intent": intent.strip()}
        if run_kw.get("config") is not None:
            # Plan (c): coerce at the door too, so the retry detection in
            # `_run_impl` compares the config the server will store, not the
            # Namespace or DictConfig it was built from.
            run_kw["config"] = _coerce.to_config(run_kw["config"])
        if ignore is not None:
            # Checked before the run exists, so a bad value opens nothing.
            from . import ignore as _ignore

            try:
                ignore = _ignore.normalize(ignore)
            except ValueError as exc:
                raise errors.ValidationError(str(exc)) from None
        handle = self._run_impl(
            experiment=experiment,
            question=question,
            name=name,
            project=project,
            experiment_name=experiment_name,
            on_conflict=on_conflict,
            snapshot=snapshot,
            ignore=ignore,
            # Only forwarded when set: `_run_impl` splats run_kw into `create_run`,
            # and an unconditional `parent_run_id=None` would make every ordinary
            # run look like it declared a null parent.
            **({"parent_run_id": parent_run_id} if parent_run_id is not None else {}),
            **({"parent_relation": parent_relation} if parent_relation is not None else {}),
            **run_kw,
        )
        from probe.hw import integration as hw_integration

        # The run is open. What follows is best-effort capture, never part of
        # opening it, so it is carved out of `probe.init()`'s retry budget.
        with without_patience():
            handle._hw_monitor = hw_integration.maybe_start(self, handle, hw)
            # Read capture is on by default only through `probe.init()`, where the
            # process IS the run's work. Here it is an explicit opt-in: a CLI or a
            # service opening runs on someone's behalf must not record its own
            # config reads as the run's inputs.
            if capture_reads:
                from . import inputs as _inputs

                _inputs.start(
                    handle.id,
                    capture_reads=True,
                    capture_outputs=capture_outputs,
                    client=self,
                    ignore=handle._ignore_rules(),
                )
            if run_kw.get("heartbeat", True) and not run_kw.get("awaiting_attach"):
                handle._start_capture(outputs=outputs, capture_outputs=capture_outputs)
        return handle

    def _run_impl(
        self,
        *,
        experiment: str | None = None,
        question: str | None = None,
        name: str | None = None,
        project: str | None = None,
        experiment_name: str | None = None,
        on_conflict: str | Rewind = "auto",
        snapshot: bool | None = None,
        ignore: str | list[str] | tuple[str, ...] | None = None,
        **run_kw,
    ) -> Run:
        """Open a run inside an experiment — or straight under a project.

        With ``experiment``, the run opens inside that experiment (and ``project``,
        if also given, is a cross-check). With only ``project`` (W&B shape), the run
        attaches PROJECT-DIRECT — no experiment at all. With neither, it opens
        FLOATING (daemon v2): no home until it is filed.

        Resolution is strict by default: an unknown slug raises, naming the closest
        existing ones.

        ``question=`` is the ONE opt-in to creation. Pass it and an absent
        experiment (and its project) is created; omit it and nothing is ever
        created. Creation is gated this way because a question is the thing you
        can only write when you know what you are trying to find out — so the cost of a new
        experiment is one sentence, and an accident cannot pay it.

        That opt-in is SDK-only on purpose. Here the slug is written once in a file
        and code-reviewed; on the CLI it is hand-typed on every invocation, which is
        where typos come from — so ``probe run start`` cannot create at all. Use
        ``probe experiment create`` / ``probe project create`` there.

        For work with no question, the honest home is a project-direct run, not an
        experiment named after whatever directory you happened to be in.

        ``on_conflict`` decides what a duplicate ``external_id`` means.
        ``"auto"`` (the default) reads the incumbent's state: dead
        (failed/crashed/canceled) → RESUME it in place — same run, same curve,
        recovery on the record; completed or still alive → the 409 stands,
        because repeating a good run or hijacking a live one must be
        deliberate. ``"resume"`` demands the resume and errors when the
        incumbent is not dead. ``"supersede"`` treats the collision as a
        from-scratch RETRY: a fresh run opens as ``external_id-rN`` with
        ``parent_relation="retry"`` pointing at the incumbent, and a dead
        incumbent is tagged ``superseded`` so nobody trusts its partial
        numbers (a completed one is left unmarked — a repeat is not a
        correction). ``"error"`` keeps the bare 409. The two recovery policies
        split on step continuity: resume continues the curve past the crash
        point (checkpointed relaunch), supersede replays it from step 0.

        A REQUEUE (2.3): when the incumbent still reads ``running`` but its
        process is gone (a replaced pod the reaper has not reached yet),
        ``"auto"``, ``"resume"`` and ``Rewind`` take it over once the server
        judges it silent for three heartbeat intervals (at least 180 s),
        waiting up to ``PROBE_TAKEOVER_WAIT_SEC`` (300; 0 in a notebook) with
        one stderr line. An incumbent that speaks while this waits is a live
        duplicate and still conflicts. Before any resume or takeover, what the
        incumbent left queued in this outbox is delivered first (bounded by
        ``PROBE_TAKEOVER_DRAIN_SEC``, 120), because the reopen's new write
        epoch would refuse it. A server without ``run_reopen_takeover``
        keeps today's conflict.

        ``snapshot`` — None (default) follows ``PROBE_AUTO_SNAPSHOT`` (on
        unless set to "0"); False skips the auto-capture; True forces it
        regardless of the env var. A run opened here and then driven through
        ``run.execute()`` snapshots twice; the second is cheap (same tree →
        same execution record via server dedupe, code-bytes deduped by the
        presign have-check) and overwrites the launch block with the more
        specific child argv — intended. This dedupe is genuine even in a git
        repo: the execution record hashes the code MANIFEST only, never the
        per-snapshot shadow commit (design doc D1), so two snapshots of an
        unchanged tree always land on the same content_hash regardless of how
        many shadow refs were minted along the way."""
        if not isinstance(on_conflict, Rewind) and on_conflict not in (
            "auto",
            "error",
            "supersede",
            "resume",
        ):
            raise errors.ValidationError(
                f'on_conflict={on_conflict!r} is not a policy. Use "auto" '
                '(resume a dead incumbent, else 409), "resume" (demand it), '
                '"supersede" (retry lineage under a fresh -rN external_id), '
                '"error" (the bare 409), or probe.Rewind(step=N) — resume '
                "from an earlier checkpoint, overwriting the run's record "
                "from step N onward (0185)."
            )
        # NO FALLBACK to the git repo or script name when both are missing: that
        # silently created an experiment named after whatever directory you
        # happened to be in. Daemon v2 opens the run FLOATING instead (below),
        # with no home at all, and the daemon files it where it belongs.
        if experiment_name is not None and question is None:
            raise errors.ValidationError(
                "experiment_name only titles an experiment run() CREATES, and "
                "creation needs a question. Pass question=, or rename an "
                "existing experiment with update_experiment()."
            )
        if question is not None and not experiment:
            raise errors.ValidationError(
                "question= creates an experiment, so it needs an experiment "
                "slug. A project-direct run has no experiment to hold one."
            )
        if question is not None and not project:
            raise errors.ValidationError(
                "creating an experiment needs an explicit project slug. Pass "
                "project= after creating the project first."
            )
        if question is not None and not question.strip():
            # `question=args.question or ""` is an ordinary way to get here.
            # Creation gates on `is not None` while create_experiment gates on
            # falsiness, so an empty string used to unlock the create path far
            # enough to commit a PROJECT before failing on the experiment.
            raise errors.ValidationError(
                "question= is empty. Creating an experiment needs one that says "
                "something: what do you expect this to show? Pass a real "
                "question, or drop the argument to open an existing experiment."
            )
        self.ensure_authenticated()
        if not experiment and not project:
            # FLOATING (daemon v2, D1). Every validation above still ran; the
            # only one this skips is "needs an experiment slug", which is the
            # point. `question=` cannot reach here (it needs an experiment).
            if run_kw.get("group_id") is not None:
                raise errors.ValidationError(
                    "a group needs an experiment: run groups are "
                    "experiment-anchored, so a run with no project cannot join "
                    "one. Name the experiment or drop the group."
                )
            run_kw.pop("group_id", None)
            self._maybe_attach_retry_parent(run_kw, project_id=None)
            handle = self._create_run_with_policy(
                lambda kw, nm: self.create_floating_run(nm, **kw),
                run_kw,
                name,
                on_conflict,
                experiment_id=None,
                project_id=None,
            )
            self._maybe_auto_snapshot(handle, snapshot, ignore)
            return handle
        # NO FALLBACK. This fabricated `run-<timestamp>` whenever the caller left
        # the name unset, and the server reads ANY supplied name as human-chosen:
        # it stamps `name_customized` and freezes the run out of generated titles
        # forever (app/generation/kinds/title.py, whose docstring names this exact
        # string as the thing it exists to replace). Passing None through is what
        # lets the server name the run after the caller's slug -- or a petname when
        # there is none -- and leave the flag False so the title kind may improve it
        # later. It must be None and NOT `name or slug`: runs never pass through
        # `chosen_name()` (that is the projects/experiments door), so a slug sent as
        # a name is indistinguishable from a human choice and re-freezes the row.
        # Refuse an uncreatable experiment slug BEFORE any parent is committed.
        # ensure_project runs first below, so without this a refused experiment
        # leaves a brand-new orphan project behind — the exact stray identity the
        # refusal exists to prevent.
        if experiment and question is not None:
            # Read-only: the project may not exist yet (ensure_project below
            # creates it), and then the lookup is tenant-wide.
            known = self.resolve_project(project) if project else None
            if (
                self.resolve_experiment(experiment, project_id=known["id"] if known else None)
                is None
            ):
                self._guard_creatable("experiment", experiment)
        project_id = None
        if project:
            # The project follows the experiment: creation is unlocked only by a
            # question, so a project-direct run (which cannot carry one) always
            # resolves strictly.
            project_id = (
                self.ensure_project(project, authored_by=run_kw.get("authored_by"))["id"]
                if question is not None
                else self.resolve_or_raise("project", project)["id"]
            )
        if not experiment:
            # Project-direct (0054): the run attaches straight to the project.
            if run_kw.get("group_id") is not None:
                raise errors.ValidationError(
                    "a group needs an experiment: run groups are "
                    "experiment-anchored, so a project-direct run cannot join "
                    "one. Name the experiment or drop the group."
                )
            run_kw.pop("group_id", None)
            self._maybe_attach_retry_parent(run_kw, project_id=project_id)
            handle = self._create_run_with_policy(
                lambda kw, nm: self.create_project_run(project_id, nm, **kw),
                run_kw,
                name,
                on_conflict,
                experiment_id=None,
                project_id=project_id,
            )
            self._maybe_auto_snapshot(handle, snapshot, ignore)
            return handle
        if question is not None:
            exp = self.ensure_experiment(
                experiment,
                # `experiment_name or experiment` used to pass the SLUG as the
                # name. The server nulls a slug-equal name, so it was a no-op --
                # but paired with an authorship declaration it claims someone
                # chose the identifier as the title. Omit it instead.
                experiment_name,
                question=question,
                project_id=project_id,
                # An experiment auto-created for a run inherits the run's
                # authorship: the same caller composed both, and without this
                # the parent is stamped human-owned by the server's historical
                # inference and locked out of naming forever.
                authored_by=run_kw.get("authored_by"),
            )
        else:
            exp = self.resolve_or_raise("experiment", experiment, project_id=project_id)
        # Naming a project for an experiment that already lives somewhere else is a
        # real mistake rather than a no-op: `project` would otherwise silently do
        # nothing, which is its own quiet wrong answer.
        if project_id and exp.get("project_id") not in (None, project_id):
            raise errors.ValidationError(
                f"experiment {experiment!r} is not in project {project!r}. "
                "Drop the project argument, or name the one it actually belongs to."
            )
        self._maybe_attach_retry_parent(run_kw, experiment_id=exp["id"])
        handle = self._create_run_with_policy(
            lambda kw, nm: self.create_run(exp["id"], nm, **kw),
            run_kw,
            name,
            on_conflict,
            experiment_id=exp["id"],
            project_id=None,
        )
        self._maybe_auto_snapshot(handle, snapshot, ignore)
        return handle

    #: Statuses that mean the predecessor is over. Mirrors `_DEAD_RUN_STATUSES`
    #: and INCLUDES `untracked` -- the reaper's verdict for a run that never
    #: heartbeated, which is the designed terminal state for agent-driven CLI runs
    #: and therefore exactly this feature's population. 48 runs carry it fleet-wide.
    _RETRY_DEAD_STATUSES = frozenset({"failed", "crashed", "canceled", "untracked"})

    def _maybe_attach_retry_parent(
        self,
        run_kw: dict,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
    ) -> None:
        """Attach `retry` parentage when this run is plainly a relaunch.

        WHY THIS EXISTS. The only other automatic producer of lineage is the
        `external_id` collision path, which fires when a caller REUSES an id. That
        is a mistake-shaped trigger, and the two natural ways to launch a retry both
        avoid it: measured fleet-wide, 12 of 34 retry-shaped runs carry no
        `external_id` at all and 16 minted a fresh one per attempt (`…-attempt-1..4`
        -- someone numbering their attempts correctly, and thereby never colliding).
        This path catches those; the two overlap on nothing.

        FIVE CONJUNCTS, each load-bearing (the first four measured):

        * **same agent session** -- scopes the question to runs THIS SDK opened, not
          a colleague's. Session ids are stamped by the server. (They are
          client-SUPPLIED on `X-Probe-Agent-Session`, so this is a scoping device,
          not an authorization one -- see app/runs/agent_session.py.)
        * **immediately preceding** -- the run before this one in the session, not
          "the most recent dead one". Without it a pipeline reads as a retry chain:
          a `dataset-prep` sequence of fail, fail, ok, ok, ok had the last two
          labeled retries of a failure two successes earlier. 4 wrong edges in 9.
        * **config equality, non-empty** -- separates a retry from a SWEEP SIBLING.
          Name matching does not: one failed seed would make every later seed a
          "retry" of it, 48% false positives on the fleet. The seed lives in the
          config, which is why config equality excludes them correctly.
        * **the predecessor has ENDED** -- a concurrent sibling is not a
          predecessor. Parallel subagents of one Claude Code session share ONE
          session id (`agent_session.py`: "no child-session handling"), so under
          fan-out "immediately preceding" is otherwise a race.
        * **the same launch** -- entrypoint, argv (as stored: scrubbed) and cwd
          equal to the predecessor's `metadata.launch.process`, each compared
          only where BOTH sides have it (lineage plan L6). A relaunch runs the
          same command in the same place; config equality alone let a different
          script with the same (or a default) config read as a retry. The new
          run has no launch block yet (the snapshot writes it after the open),
          so its side is computed by the same rules (`launch.process_identity`):
          this process's command, or the one `launch.launching()` names
          (`probe exec`'s child).

        SCOPE is weak since floating runs (daemon v2): every unfiled run has
        scope None, so the scope conjunct no longer separates two lines of work
        opened without a project; config equality and the launch do.

        LIMITS, on the record. Precision was measured retrospectively on SETTLED
        statuses. A predecessor whose process died reads `running` only until
        its death is noticed -- seconds for a sole writer since #2049, the
        reaper's 900s stale window otherwise -- and this fails closed meanwhile.
        A run marked crashed that comes back (its owner's next heartbeat undoes
        the mark) is a new false positive the measurement has to count. Live
        recall and precision are unmeasured. Hence OFF BY DEFAULT.

        FAILS OPEN and is SILENT ON AMBIGUITY: any error opens the run with no
        edge, and lineage is never worth failing a training run over.
        """
        mode = os.environ.get("PROBE_AUTO_RETRY_LINEAGE", "").strip().lower()
        if mode not in ("1", "true", "on", "shadow"):
            return
        if run_kw.get("parent_run_id") is not None:
            return  # the caller declared it; never second-guess a stated claim
        config = run_kw.get("config")
        if not isinstance(config, dict) or not config:
            return  # config equality is the discriminator; without one there is none
        try:
            resolved = agent_session.resolve_agent_session()
            if resolved is None:
                return
            agent, session_id = resolved
            # UNFILTERED, deliberately, and that includes the SCOPE. Any narrowing
            # before `limit=1` answers a different question: `status=failed` gives
            # the most recent DEAD run, and an `experiment_id` filter gives the most
            # recent run IN THIS EXPERIMENT -- neither is "the run immediately before
            # this one". A session that went A(exp1, failed) -> B(exp2, completed) ->
            # C(exp1) would attach C to A under either filter, which is precisely the
            # false positive the immediately-preceding conjunct exists to prevent.
            # So: fetch the session's single most recent run and check scope, status
            # and config locally. `created_at DESC` is the list order, so limit=1 IS
            # the predecessor.
            page = self.list_runs(foreign_key=f"{agent}_session_id:{session_id}", limit=1)
            candidates = page.items or []
            if not candidates:
                return
            previous = candidates[0]
            scope_id = experiment_id if experiment_id is not None else project_id
            scope_key = "experiment_id" if experiment_id is not None else "project_id"
            # A floating run (scope None) matches only a floating predecessor.
            found = previous.get(scope_key)
            if (None if found is None else str(found)) != (None if scope_id is None else str(scope_id)):
                return
            if str(previous.get("status") or "") not in self._RETRY_DEAD_STATUSES:
                return
            if not previous.get("ended_at"):
                return  # still open: a concurrent sibling, not a predecessor
            if previous.get("config") != config:
                return
            if not self._same_launch(previous):
                return
        except Exception:  # noqa: BLE001 -- never fail a run for a lineage guess
            return
        if mode == "shadow":
            # SHADOW MODE. The measured precision is retrospective, so watch what
            # this would have written before letting it write anything.
            _diagnostics.warn(
                f"probe: auto-retry lineage WOULD attach parent_run_id="
                f"{previous.get('id')} (relation=retry) — matched on session + "
                "immediately-preceding + config equality + launch. Set "
                "PROBE_AUTO_RETRY_LINEAGE=1 to write it."
            )
            return
        run_kw["parent_run_id"] = str(previous["id"])
        run_kw["parent_relation"] = "retry"
        run_kw["parent_provenance"] = "observed_call"

    #: The launch fields a relaunch keeps (`metadata.launch.process`).
    _RETRY_LAUNCH_KEYS = ("entrypoint", "argv", "cwd")

    @classmethod
    def _same_launch(cls, previous: Mapping[str, Any]) -> bool:
        """Is the run about to open launched like `previous` was? Each of
        `_RETRY_LAUNCH_KEYS` is compared only where both sides have it: a
        predecessor with no launch block (snapshots off, `probe run start`) is
        judged on the other conjuncts alone, as before."""
        from . import launch as _launch

        metadata = previous.get("metadata")
        block = metadata.get("launch") if isinstance(metadata, Mapping) else None
        stored = block.get("process") if isinstance(block, Mapping) else None
        if not isinstance(stored, Mapping):
            return True
        mine, _ = _launch.process_identity()
        for key in cls._RETRY_LAUNCH_KEYS:
            theirs = stored.get(key)
            if theirs is None or mine.get(key) is None:
                continue
            if theirs != mine[key]:
                return False
        return True

    @staticmethod
    def _maybe_auto_snapshot(handle: Run, snapshot: bool | None, ignore: Any = None) -> None:
        """Auto-snapshot hook for ``run()`` (design D3). ``snapshot=None``
        follows ``PROBE_AUTO_SNAPSHOT`` (default on); best-effort like
        ``execute()``'s hook -- failure warns rather than losing the run.
        Capture is never a gate, opt-in or otherwise (maintainer decision
        2026-08-06).

        Also where every freshly opened handle takes its ``ignore=`` patterns
        (plan (n)): all three ways `_run_impl` opens a run pass through here,
        and the snapshot below must already honour them."""
        handle._set_ignore(ignore)
        auto = (
            snapshot
            if snapshot is not None
            else (os.environ.get("PROBE_AUTO_SNAPSHOT", "1") != "0")
        )
        if auto:
            try:
                # Best-effort capture is not part of opening the run: carved out
                # of `probe.init()`'s retry budget (plan 2.5), so it keeps its
                # own timeouts however long the create took.
                with without_patience():
                    handle.snapshot()  # in-process: THIS interpreter is the env
            except Exception as exc:
                warnings.warn(
                    f"auto-snapshot failed; run continues uncaptured: {exc}",
                    stacklevel=2,
                )

    #: Statuses whose numbers cannot be trusted; superseding one marks it.
    _DEAD_RUN_STATUSES = frozenset({"failed", "crashed", "canceled", "untracked"})

    def _create_run_with_policy(
        self,
        create,
        run_kw: dict,
        name: str,
        on_conflict: str | Rewind,
        *,
        experiment_id: str | None,
        project_id: str | None,
        max_attempts: int = 5,
    ) -> Run:
        """``create()``, except an external_id 409 is resolved by policy.

        RESUME reopens the incumbent in place — same identity, same curve —
        which is only honest when the relaunch continues from a checkpoint;
        the step guard on the returned handle enforces that. SUPERSEDE opens a
        NEW run as ``external_id-rN`` carrying ``parent_relation="retry"``
        plus ``retry_of``/``retry_attempt`` foreign keys, for the relaunch
        that replays from step 0 (appending that into a half-dead run would
        splice two executions into one curve — the W&B ``resume="allow"``
        failure mode). Either way a dead incumbent's partial record survives:
        resume continues it, supersede tags it ``superseded``."""
        try:
            return create(run_kw, name)
        except errors.ConflictError as conflict:
            base = run_kw.get("external_id")
            if on_conflict == "error" or base is None:
                raise
            existing_id = conflict.existing_id
        old = None
        if existing_id:
            # The SERVER already resolved the incumbent, on the real key --
            # `SELECT id FROM runs WHERE source = $1 AND external_id = $2`, which
            # is the (customer_id, source, external_id) uniqueness the 409 came
            # from. Ask it rather than re-deriving the answer from a listing.
            try:
                old = self.get_run(existing_id)
            except errors.NotFoundError:
                old = None  # raced with a delete; fall through to the scan
        if old is None:
            # Older backends send a bare 409. Match on BOTH halves of the key:
            # external_id alone is not unique -- ingest and sdk runs share the
            # namespace by design -- so this used to be able to hand back a
            # different source's run and resume or supersede the wrong one.
            source = (run_kw.get("source") or "api").strip().lower()
            page = self.list_runs(experiment_id=experiment_id, project_id=project_id)
            old = next(
                (
                    r
                    for r in page.items
                    if r.get("external_id") == base
                    and str(r.get("source") or "").strip().lower() == source
                ),
                None,
            )
        if old is None:
            # The 409 is real but the incumbent is not on the first page (or
            # belongs to another source). Acting on it blind would resume or
            # supersede the wrong thing, so the original conflict stands.
            raise errors.ConflictError(
                f"run {base!r} conflicts but its incumbent is not visible "
                "here — resolve the collision by hand",
            )
        status = old.get("status")
        if isinstance(on_conflict, Rewind):
            # Rewind = resume from an earlier checkpoint. `completed` is
            # ALLOWED here — the deliberate stop-then-rewind flow ends cleanly
            # first, and naming the destructive step is the consent the plain
            # resume's 409 exists to demand. A live writer still refuses.
            takeover = status == "running" and self._supports_takeover()
            if status not in self._DEAD_RUN_STATUSES and status != "completed" and not takeover:
                raise errors.ConflictError(
                    f"run {base!r} is {status} and its writer may still be "
                    "alive — rewind refuses to hijack an open run. End it (or "
                    "let the reaper mark it crashed), then relaunch."
                )
            # Preflight BEFORE any state changes: a pre-0185 server silently
            # drops the unknown body field, reopens the run, and deletes
            # nothing — the worst failure shape a destructive request can
            # have. One cheap GET turns that skew into a loud no-op error.
            self._require_feature(
                "run_rewind",
                "this server predates run rewind (0185): a reopen would "
                "silently ignore rewind_to_step and delete nothing. Upgrade "
                'research-os, or use on_conflict="supersede" / fork_run().',
            )
            return self._resume_run(
                old, run_kw, rewind_to_step=on_conflict.step, takeover=takeover
            )
        if on_conflict in ("auto", "resume"):
            if status in self._DEAD_RUN_STATUSES:
                return self._resume_run(old, run_kw)
            if status == "running" and self._supports_takeover():
                # 2.3: a requeued job whose previous pod is gone but not yet
                # reaped. The server takes the run over only once it has been
                # silent long enough to be dead, and says how long to wait.
                return self._resume_run(old, run_kw, takeover=True)
            if status == "completed":
                raise errors.ConflictError(
                    f"run {base!r} already completed — resuming would append "
                    "onto a good record. Repeat it deliberately with "
                    'on_conflict="supersede", or rewind it from a checkpoint '
                    "with on_conflict=probe.Rewind(step=N)."
                )
            raise errors.ConflictError(
                f"run {base!r} is {status} and its writer may still be alive "
                "— refusing to hijack an open run. If it is truly dead, wait "
                "for the reaper to mark it crashed, or supersede explicitly."
            )
        for n in range(2, max_attempts + 2):
            retry_id = f"{base}-r{n}"
            retry_kw = dict(
                run_kw,
                external_id=retry_id,
                parent_run_id=old["id"],
                parent_relation="retry",
                # The SDK derived this parent (an id collision), nobody
                # declared it: stored as observed, not as a person's claim.
                parent_provenance="observed_call",
            )
            if name == base and retry_kw.get("authored_by") is None:
                # `retry_id` below is a string the SDK composed (`<base>-r2`),
                # so it declares itself -- same rule as `fork_run`, and only
                # when the caller has not already said. Without it a nightly
                # `on_conflict="supersede"` from a bare terminal locks
                # `nightly-eval-r2` as human-chosen, forever.
                retry_kw["authored_by"] = agent_session.AUTHORSHIP_AGENT
            try:
                run = create(retry_kw, retry_id if name == base else name)
                break
            except errors.ConflictError:
                continue
        else:
            raise errors.ConflictError(
                f"no free retry slot for {base!r} after {max_attempts} "
                "attempts — the run has been superseded that many times "
                "already, which is worth a look before retrying again",
            )
        # link() is the sanctioned foreign-keys surface (create_run does not
        # take them); per-key new-wins, so this cannot clobber anything.
        run.link(retry_of=old["id"], retry_attempt=n)
        if old.get("status") in self._DEAD_RUN_STATUSES:
            tags = sorted({*(old.get("tags") or []), "superseded"})
            # sync=True, for two reasons that compound. `tags` is a whole-list
            # REPLACE built from a row read a moment ago, so a delayed replay
            # would overwrite whatever the old run acquired in between. And the
            # op would carry the OLD run's run_ref, which the NEW run's finish()
            # barrier -- scoped to its own id -- never covers, so it could sit
            # queued indefinitely while the run it marks looks merely dead.
            self.write("PATCH", f"/v1/runs/{old['id']}", {"tags": tags}, sync=True)
        return run

    @staticmethod
    def _attached_owns_verdict(row: dict) -> bool:
        """Whether a job attaching to ``row`` from inside the work owns the
        run's verdict: no finalizing `probe exec` launcher names this run, and
        this process is not a non-zero rank of a distributed job."""
        from .fluent import _nonzero_global_rank
        from .run import EXEC_FINALIZES_ENV

        finalized = (os.environ.get(EXEC_FINALIZES_ENV) or "").strip() == str(row.get("id"))
        return not finalized and _nonzero_global_rank() is None

    def _leases_available(self) -> bool:
        """Whether this client's server takes per-writer leases (2.8). A failed
        preflight reads as "no": the run-level heartbeat, as before."""
        try:
            return self.supports_feature(_LEASES_FEATURE)
        except Exception:  # noqa: BLE001 -- never a reason for a run not to open
            return False

    def _lease_for_create(
        self, body: dict, *, heartbeat: bool, awaiting_attach: bool, launcher: bool
    ) -> tuple[str | None, dict | None]:
        """Ask for a `leases` run when this process will beat for it: adds
        `liveness_protocol` + `writer` to the create body. Returns the session
        and lease the handle must carry, or (None, None).

        A HAND-OFF (`awaiting_attach`: `probe exec -- sbatch`,
        `--detached-launcher`) asks for `leases` too, with NO writer: the job's
        ranks each register their own lease when they attach (`attach_run`),
        and the run closes by the lease rules like any other (plan 2.8: every
        rank holds a lease). Without it the run stayed legacy, where the ranks'
        writer-gone reports change nothing and a scancel'd job waited for the
        900 s reaper. The submitter holds no lease on purpose: it exits the
        moment the scheduler accepts the job, so its release would end the run
        as `completed` before the work starts (a launcher's release waives the
        rank slots), and a lease it never released would expire into a false
        `writer_lost` on every job queued or running past an hour. The
        created-sweep still ends a hand-off nobody attaches to. A hand-off
        whose opener beats the run itself (`heartbeat=True`) stays legacy: its
        run-level heartbeat would flip the run anyway."""
        if awaiting_attach:
            if not heartbeat and self._leases_available():
                body["liveness_protocol"] = "leases"
            return None, None
        if not heartbeat or not self._leases_available():
            return None, None
        session_id = str(uuid.uuid4())
        lease = _writer_lease("launcher" if launcher else "owner", session_id)
        body["liveness_protocol"] = "leases"
        body["writer"] = lease
        return session_id, lease

    def _supports_takeover(self) -> bool:
        """Whether the server takes over a silent `running` run (2.3). A
        failed preflight reads as "no": today's ConflictError, not a new
        failure mode at init."""
        try:
            return self.supports_feature("run_reopen_takeover")
        except errors.RosError:
            return False

    def _resume_run(
        self,
        old: dict,
        run_kw: dict,
        *,
        rewind_to_step: int | None = None,
        takeover: bool = False,
    ) -> Run:
        """Reopen a dead incumbent and hand back a live handle on it.

        The session id minted here is the writer fingerprint the reopen
        registers (research-os#364): the engine's write epoch bumps, so a
        zombie predecessor still logging can be told apart from this process
        — and, since 0185, refused at the door (the receipt's epoch rides on
        every write the handle makes). The receipt's ``last_step`` arms the
        handle's resume guard. Snapshot again after this returns — each
        attempt's code+env is its own execution record.

        ``rewind_to_step`` asks the reopen to discard the record from that
        step onward in the same transaction. The echo check is the second
        lock behind the feature preflight: never trust a destructive request
        a server did not explicitly confirm honoring.

        ``takeover`` (2.3) reopens a `running` incumbent the server judges
        silent, waiting within ``PROBE_TAKEOVER_WAIT_SEC`` when it is not
        silent yet. Either way the incumbent's own queued ops in this outbox
        are delivered FIRST: a replacement pod on a persistent outbox finds
        the old attempt's epoch-E ops there, and the reopen's E+1 would fence
        every one of them.

        The incumbent's queued STATUS writes are held aside meanwhile, and
        retired only once the reopen succeeds: then the relaunch owns the
        verdict (and 1.10's fence would refuse them anyway). Any refusal or
        error puts them back, so a relaunch that does NOT take over never
        costs the incumbent its close (review of #2019, MED-A)."""
        from .transport import without_patience

        # Both long steps have their own bounds (PROBE_TAKEOVER_DRAIN_SEC and
        # PROBE_TAKEOVER_WAIT_SEC), and `probe.init()`'s budget (#2027,
        # PROBE_INIT_TIMEOUT_SEC) must not cut them off: a requeue that waits
        # for its dead incumbent to go quiet would otherwise die at 90 s with
        # a DeadlineExceeded after doing most of the wait.
        closes = self._queued_completed_close(old) if takeover else False
        with without_patience():
            held = self._drain_before_takeover(old)
        if closes:
            # The incumbent FINISHED: its `completed` close was still queued
            # here, and the barrier just delivered it. A resume never appends
            # onto a completed run; a rewind still may (review of #2019).
            fresh = self.get_run(old["id"])
            if fresh.get("status") == "completed":
                if rewind_to_step is None:
                    self._release_status_writes(held, retire=False)
                    name = old.get("slug") or old.get("id")
                    raise errors.ConflictError(
                        f"run {name!r} already completed -- its close was still queued "
                        "in this outbox and has now been delivered. Resuming would append "
                        'onto a good record. Repeat it deliberately with on_conflict='
                        '"supersede", or rewind it from a checkpoint with '
                        "on_conflict=probe.Rewind(step=N)."
                    )
                takeover = False  # a rewind of a completed run is a plain reopen
        session_id = str(uuid.uuid4())
        # 2.8: the resumed attempt writes under its own lease -- a launcher's
        # when a launcher resumes, and none when it will not beat (as a create).
        writer = (
            _writer_lease("launcher" if run_kw.get("launcher") else "owner", session_id)
            if run_kw.get("heartbeat", True) and self._leases_available()
            else None
        )
        try:
            if takeover:
                with without_patience():
                    receipt = self._reopen_taking_over(
                        old,
                        session_id,
                        rewind_to_step,
                        heartbeat=run_kw.get("heartbeat", True),
                        launcher=bool(run_kw.get("launcher")),
                        writer=writer,
                    )
            else:
                receipt = self.reopen_run(
                    old["id"], session_id=session_id, rewind_to_step=rewind_to_step, writer=writer
                )
        except BaseException:
            self._release_status_writes(held, retire=False)
            raise
        self._release_status_writes(held, retire=True)
        self._clear_draining_tag(old, receipt)
        if rewind_to_step is not None and receipt.get("rewound_to") != rewind_to_step:
            raise errors.ConflictError(
                f"reopen returned no rewind echo for step {rewind_to_step} — "
                "the server did not honor the rewind (a pre-0185 backend "
                f"drops the field silently). Run {old['id']} is now reopened "
                "WITHOUT anything deleted; its old points still hold their "
                "steps. Upgrade the server, then retry."
            )
        row = receipt.get("run") or receipt
        if receipt.get("write_epoch") is not None:
            _repin_bracket_lease(old["id"], receipt["write_epoch"])
        return self.attach_run(
            row,
            heartbeat=run_kw.get("heartbeat", True),
            session_id=session_id,
            resume_from_step=receipt.get("last_step"),
            write_epoch=receipt.get("write_epoch"),
            writer=writer,
        )

    def _queued_completed_close(self, old: dict) -> bool:
        """Whether this outbox still holds the incumbent's queued `completed`
        close (one read of the queue; False when it cannot be read)."""
        refs = {str(r) for r in (old.get("id"), old.get("slug")) if r}
        try:
            return any(
                op.get("run_ref") in refs
                and (
                    (
                        op.get("method") == "PATCH"
                        and (op.get("body") or {}).get("status") == "completed"
                    )
                    # 2.8: a leased writer's verdict is its queued release.
                    or (
                        op.get("method") == "POST"
                        and str(op.get("path") or "").endswith("/release")
                        and (op.get("body") or {}).get("exit_status") == "completed"
                    )
                )
                for _, op in self.journal.pending()
            )
        except Exception:  # noqa: BLE001 -- unreadable: nothing is known to be queued
            return False

    def _drain_before_takeover(self, old: dict) -> None:
        """Deliver what the incumbent left queued HERE before its epoch moves.

        Scoped to the incumbent's refs (its id, and its slug for CLI ops), and
        to the ops queued BEFORE this barrier began: an op of those refs that
        appears meanwhile means a LIVE writer shares this outbox (a duplicate
        launch on the same box), so the barrier stops at once and the takeover
        conflicts as it should, instead of chasing a live queue and then
        warning about ops that are not a dead attempt's.

        The incumbent's queued STATUS writes are HELD aside, never delivered
        by the barrier: a queued `completed` would close the run the relaunch
        is taking over (and fail it), a queued `failed` would mail a crash
        notice. Returns their names; `_resume_run` retires them once the
        reopen succeeds and puts them back otherwise. Data still lands, under
        the old epoch, before the reopen moves it.

        Bounded by ``PROBE_TAKEOVER_DRAIN_SEC`` (120), every request of every
        pass included (`deadline_scope`). A detached worker mid-pass holds the
        drain lock, so this never blocks on it.
        What is still queued at the bound is SAID, not silently fenced."""
        refs = {str(r) for r in (old.get("id"), old.get("slug")) if r}
        mine = str(self.journal.dir)

        def queued() -> dict[tuple[str, str], dict]:
            """The incumbent's queued ops, by (queue, name): this client's queue,
            and every other queue of the outbox whose own worker is running --
            writes of the run queued under another credential (#2035) that
            someone is delivering right now (#2041 round 5). One nobody can
            send here is only named in the warning below."""
            out: dict[tuple[str, str], dict] = {}
            try:
                for path, op in self.journal.pending():
                    if op.get("run_ref") in refs:
                        out[(mine, path.name)] = op
                for queue in self.journal.other_queues():
                    if queue.receipt_enabled or not queue.worker_alive():
                        continue
                    for path, op in queue.pending():
                        if op.get("run_ref") in refs:
                            out[(str(queue.dir), path.name)] = op
            except Exception:  # noqa: BLE001 -- an unreadable queue has nothing to barrier
                return out
            return out

        # A relaunch killed mid-barrier left its hold behind: put it back.
        self._restore_expired_holds()
        if not refs:
            return []
        before = queued()
        if not before and not self._incumbent_writes_elsewhere(refs):
            return []
        held = self._hold_status_writes(
            old, {name: op for (where, name), op in before.items() if where == mine}
        )
        try:
            return self._deliver_backlog(old, refs, queued, held)
        except BaseException:
            # Ctrl-C or a bug mid-barrier: the hold must not outlive it.
            self._release_status_writes(held, retire=False)
            raise

    def _deliver_backlog(self, old: dict, refs: set[str], queued, held: list[str]) -> list[str]:
        """The barrier's delivery loop (see `_drain_before_takeover`).

        ONE deadline, inside a pass too (#2011's `deadline_scope`): each
        request of the drain is bounded by what is left of
        ``PROBE_TAKEOVER_DRAIN_SEC``, and one that would start after it is not
        sent, so a long backlog can no longer hold a relaunch's `init()` for as
        long as a whole pass takes (review of #2019, MED-2)."""
        from .durable import backoff_delays
        from .journal import drain
        from .transport import deadline_scope

        before = queued()
        budget = _env_seconds("PROBE_TAKEOVER_DRAIN_SEC", _TAKEOVER_DRAIN_SECONDS)
        deadline = time.monotonic() + budget
        delays = backoff_delays(1_000_000, (0.5, 10.0))
        remaining: set[str] = set(before)
        outage = False
        while remaining:
            for ref in sorted(refs):
                if time.monotonic() >= deadline:
                    break
                try:
                    with deadline_scope(deadline):
                        report = drain(
                            self.journal,
                            run_ref=ref,
                            client_factory=self._outbox_client_factory(),
                            wait_for_lock=False,
                            promote_timeout=max(0.0, deadline - time.monotonic()),
                        )
                except errors.TransportError:
                    outage = True
                except Exception:  # noqa: BLE001 -- the bound below decides, not one error
                    pass
                else:
                    stall = (report.stalled_runs or {}).get(ref)
                    if (
                        report.unreachable
                        or report.auth_blocked
                        or (
                            stall is not None
                            and stall.status is None
                            # A HELD run sent nothing, so says nothing about the
                            # server (#2041 round 5).
                            and not getattr(stall, "held", False)
                        )
                    ):
                        # The server cannot be reached (or refuses the
                        # credential): nothing of the backlog can land, and the
                        # reopen after this would fail the same way. Stop now
                        # rather than loop for the whole budget outside
                        # `probe.init()`'s own (review of #2019).
                        outage = True
                if outage:
                    break
            if outage:
                break
            now_queued = queued()
            if set(now_queued) - set(before):
                # A live writer is appending: not a dead attempt's backlog, and
                # its verdict is its own. Back at once, ahead of what it adds.
                self._release_status_writes(held, retire=False)
                return []
            remaining = set(now_queued) & set(before)
            now = time.monotonic()
            if not remaining or now >= deadline:
                break
            time.sleep(min(next(delays), max(deadline - now, 0.0)))
        if outage:
            remaining = set(queued()) & set(before)
        stranded = self._incumbent_writes_elsewhere(refs)
        if remaining or stranded:
            why = (
                "the server could not be reached"
                if outage
                else f"not delivered within {budget:g}s (PROBE_TAKEOVER_DRAIN_SEC)"
            )
            also = (
                f" {stranded} of them are queued under another credential this process "
                "does not hold (a rotated PROBE_TOKEN, say) and no worker of that "
                "credential is running: they cannot land before the reopen."
                if stranded
                else ""
            )
            _diagnostics.warn(
                f"probe: {len(remaining) + stranded} op(s) the previous attempt of run "
                f"{old.get('slug') or old.get('id')} queued in this outbox were not "
                f"delivered: {why if remaining else 'nothing here may send them'}.{also} If "
                "this relaunch reopens the run under a new write epoch the server will "
                "refuse them; they stay visible in `probe outbox status`."
            )
        return held

    def _incumbent_writes_elsewhere(self, refs: set[str]) -> int:
        """The incumbent's queued writes in OTHER credential queues (#2035)
        that no running worker is delivering: stranded as far as a takeover
        is concerned (#2041 round 5, a relaunch with a rotated PROBE_TOKEN)."""
        count = 0
        try:
            for queue in self.journal.other_queues():
                if queue.receipt_enabled or queue.worker_alive():
                    continue
                count += sum(1 for _path, op in queue.pending() if op.get("run_ref") in refs)
        except Exception:  # noqa: BLE001 -- best-effort: the warning is the point
            return count
        return count

    def _hold_status_writes(self, old: dict, ops: dict[str, dict]) -> list[str]:
        """Set the incumbent's queued STATUS PATCHes aside for the barrier (see
        `_drain_before_takeover`); returns the names held.

        Aside means the dead-letter folder, marked as a hold: no drain delivers
        from there, and if this process dies mid-barrier the op is still
        VISIBLE (`probe outbox status`, `probe outbox retry`) and the next
        relaunch's barrier puts an expired hold back. Under the drain lock, so a
        worker can never be delivering one of them at the same moment; if a
        worker holds the lock for more than a few seconds, nothing is held and
        the barrier may deliver them, as before 2.3."""
        from .._shared import oscompat

        # A `completed` close is NOT held: the incumbent finished, so the
        # barrier delivers it with the data and the relaunch must not continue
        # a finished run (review of #2019; `_resume_run` then refuses, as a
        # resume of a completed run does). Every other verdict is the dead
        # attempt's, which a requeue continues.
        doomed = [
            name
            for name, op in ops.items()
            if (
                op.get("method") == "PATCH"
                and "status" in (op.get("body") or {})
                and (op.get("body") or {}).get("status") != "completed"
            )
            # 2.8: on a `leases` run the incumbent's verdict is its queued
            # lease release, held and retired exactly like a status write (a
            # `completed` one is delivered, like a `completed` close).
            or (
                op.get("method") == "POST"
                and str(op.get("path") or "").endswith("/release")
                and (op.get("body") or {}).get("exit_status") != "completed"
            )
        ]
        if not doomed:
            return []
        try:
            handle = self.journal.drain_lock.open("a+")
        except OSError:
            return []
        held: list[str] = []
        try:
            give_up = time.monotonic() + 5.0
            while True:
                try:
                    oscompat.flock(handle.fileno(), oscompat.LOCK_EX | oscompat.LOCK_NB)
                    break
                except BlockingIOError:
                    if time.monotonic() >= give_up:
                        return []
                    time.sleep(0.05)
            until = (
                time.time()
                + _env_seconds("PROBE_TAKEOVER_DRAIN_SEC", _TAKEOVER_DRAIN_SECONDS)
                + max(
                    _takeover_wait_budget(),
                    _takeover_threshold() + _TAKEOVER_BUDGET_SLACK_SECONDS,
                )
                + _TAKEOVER_HOLD_MARGIN_SECONDS
            )
            hold = {"pid": os.getpid(), "host": socket.gethostname(), "until": until}
            # The marker first: whatever happens next, a drain or a new client
            # knows to look for a hold this process may not live to release.
            self.journal.holds_marker.touch()
            for name in doomed:
                path = self.journal.ops_dir / name
                try:
                    op = json.loads(path.read_text())
                except (OSError, ValueError):
                    continue
                op[_TAKEOVER_HOLD_KEY] = {
                    **hold,
                    "last_error": op.get("last_error"),
                    "blocking": op.get("blocking"),
                }
                op["last_error"] = (
                    "held by a relaunch taking over run "
                    f"{old.get('slug') or old.get('id')}: retired if it takes over, "
                    "put back if it does not"
                )
                op["blocking"] = False
                self._move_op(path, self.journal.failed_dir / name, op)
                held.append(name)
        except Exception:  # noqa: BLE001 -- a close left queued is the old behaviour
            pass
        finally:
            handle.close()
        self._recount_outbox()
        return held

    def _release_status_writes(self, names: list[str], *, retire: bool) -> None:
        """End the barrier's hold on ``names``: RETIRED (the reopen succeeded,
        the relaunch owns the verdict) or PUT BACK at their original queue
        positions (anything else), with the drainer woken to deliver them."""
        if not names:
            return
        moved = False
        for name in names:
            path = self.journal.failed_dir / name
            try:
                op = json.loads(path.read_text())
            except (OSError, ValueError):
                continue  # retried by hand meanwhile, or gone: nothing to undo
            hold = op.pop(_TAKEOVER_HOLD_KEY, None)
            if not isinstance(hold, dict):
                continue
            try:
                if retire:
                    op["last_error"] = (
                        "retired by a takeover: the relaunch of this run owns its verdict now"
                    )
                    self._move_op(path, path, op)
                else:
                    op["last_error"] = hold.get("last_error")
                    if hold.get("blocking") is None:
                        op.pop("blocking", None)
                    else:
                        op["blocking"] = hold["blocking"]
                    self._move_op(path, self.journal.ops_dir / name, op)
                    moved = True
            except Exception:  # noqa: BLE001 -- the next barrier restores an expired hold
                continue
        self._recount_outbox()
        if moved:
            self._kick_drainer(force=True)

    def _restore_expired_holds(self) -> None:
        """Put back holds whose relaunch died before releasing them: expired,
        or held by a process of this host that no longer exists. A full scan
        (a hold an older client left carries no marker); the barrier runs it."""
        from .journal import hold_abandoned

        try:
            stale = [
                path.name
                for path, op in self.journal.failed()
                if isinstance(op.get(_TAKEOVER_HOLD_KEY), dict)
                and hold_abandoned(op[_TAKEOVER_HOLD_KEY])
            ]
        except Exception:  # noqa: BLE001 -- an unreadable folder has nothing to restore
            return
        self._release_status_writes(stale, retire=False)

    def _restore_abandoned_holds(self) -> list[str]:
        """The cheap check every new client makes (`journal.restore_abandoned_holds`),
        with the outbox's counts kept right. Returns what went back."""
        from .journal import restore_abandoned_holds

        restored = restore_abandoned_holds(self.journal)
        if restored:
            self._recount_outbox()
        return restored

    def _move_op(self, src: Path, dst: Path, op: dict) -> None:
        """Rewrite ``op`` at ``src`` and move it to ``dst`` atomically: written
        in place first, so a crash never leaves it in both folders."""
        from .durable import fsync_directory, write_text_atomic

        write_text_atomic(src, json.dumps(op, indent=2) + "\n", mode=0o600)
        if src != dst:
            os.replace(src, dst)
            fsync_directory(dst.parent)
        fsync_directory(src.parent)

    def _recount_outbox(self) -> None:
        """status.json follows ops moved between the queue and dead letters."""
        try:
            from .durable import file_lock

            with file_lock(self.journal.append_lock):
                self.journal._write_status_locked()
        except Exception:  # noqa: BLE001 -- the next append recounts
            pass

    def _clear_draining_tag(self, old: dict, receipt: dict) -> None:
        """A retired close was also what took the incumbent's "draining" tag
        back off (its deferred finish restores the tags). The run is running
        again under this relaunch, so the tag is wrong: drop it (review of
        #2019, LOW-D)."""
        row = receipt.get("run") if isinstance(receipt.get("run"), dict) else receipt
        tags = row.get("tags") if isinstance(row, dict) else None
        if not isinstance(tags, list) or "draining" not in tags:
            return
        try:
            self.write(
                "PATCH",
                f"/v1/runs/{old['id']}",
                {"tags": [t for t in tags if t != "draining"]},
                sync=True,
            )
        except Exception:  # noqa: BLE001 -- a stale hint, never a reason to fail init
            pass

    def _reopen_taking_over(
        self,
        old: dict,
        session_id: str,
        rewind_to_step: int | None,
        *,
        heartbeat: bool | None = None,
        launcher: bool = False,
        writer: dict | None = None,
    ) -> dict:
        """Reopen a `running` incumbent once the server judges it silent.

        The server answers a not-yet-silent incumbent with 409 +
        ``retry_after_seconds``. Wait that long while it fits the remaining
        budget, one stderr line in all, and retry with the SAME session (the
        reopen is idempotent by session). The budget is ``PROBE_TAKEOVER_WAIT_SEC``
        (300; 0 in a notebook), and whenever it allows any wait it covers at
        least one full threshold plus slack, or a relaunch seconds after the
        death could never succeed. A live duplicate therefore waits out the
        budget and then conflicts: at the first 409 a pod dead for seconds and
        a live one look exactly alike."""
        threshold = _takeover_threshold()
        budget = _takeover_wait_budget()
        if budget > 0:
            budget = max(budget, threshold + _TAKEOVER_BUDGET_SLACK_SECONDS)
        started = time.monotonic()
        waited = 0.0  # what the budget has paid in waits, whatever the clock says
        announced = False
        name = old.get("slug") or old.get("id")
        while True:
            try:
                return self.reopen_run(
                    old["id"],
                    session_id=session_id,
                    rewind_to_step=rewind_to_step,
                    takeover_stale_after_seconds=threshold,
                    heartbeat=heartbeat,
                    launcher=launcher,
                    writer=writer,
                )
            except errors.ConflictError as exc:
                detail = exc.detail if isinstance(exc.detail, dict) else {}
                retry_after = detail.get("retry_after_seconds")
                if not isinstance(retry_after, (int, float)) or isinstance(retry_after, bool):
                    raise
                spent = max(time.monotonic() - started, waited)
                if retry_after > budget - spent:
                    raise errors.ConflictError(
                        f"run {name} is running and its writer may still be alive: "
                        f"the server can hand it over in {int(retry_after)}s, past "
                        f"this relaunch's wait budget ({budget:g}s, "
                        "PROBE_TAKEOVER_WAIT_SEC). If it is a live duplicate, stop "
                        'it; otherwise relaunch later, or use on_conflict="supersede".',
                        detail=exc.detail,
                    ) from exc
                if not announced:
                    announced = True
                    _diagnostics.warn(
                        f"probe: run {name} still reads running. Taking it over once "
                        "its writer has been silent long enough: waiting up to "
                        f"{budget:g}s (PROBE_TAKEOVER_WAIT_SEC)."
                    )
                _takeover_sleep(float(retry_after))
                waited += float(retry_after)

    def reopen_run(
        self,
        run_id: str,
        *,
        session_id: str,
        rewind_to_step: int | None = None,
        keep_epoch: bool = False,
        expected_write_epoch: int | None = None,
        takeover_stale_after_seconds: int | None = None,
        heartbeat: bool | None = None,
        launcher: bool = False,
        writer: dict | None = None,
    ) -> dict:
        """``POST /v1/runs/{id}/reopen`` — flip a dead run back to running.

        Returns the reopen receipt: the updated row plus ``write_epoch`` and
        ``last_step``. The caller just resolved the run, so a 404 here is the
        ROUTE missing, not the run — a backend that predates reopen
        (research-os#364) — and is translated into the actionable message
        rather than passed through as \"run not found\".

        ``keep_epoch`` + ``expected_write_epoch`` (SDK reliability 1.1) are
        SELF-recovery: the same attempt coming back after the reaper crashed
        it during an outage. The server keeps the epoch instead of bumping it,
        and only for a ``crashed`` row still on ``expected_write_epoch``;
        anything else is a 409. A server predating it silently ignores both
        fields and bumps, so check ``supports_feature("run_reopen_keep_epoch")``
        first."""
        try:
            body: dict = {"session_id": session_id}
            if rewind_to_step is not None:
                body["rewind_to_step"] = rewind_to_step
            if keep_epoch:
                body["keep_epoch"] = True
                body["expected_write_epoch"] = expected_write_epoch
            if takeover_stale_after_seconds is not None:
                # 2.3: only after `supports_feature("run_reopen_takeover")`; an
                # older server drops it and refuses the running run as before.
                body["takeover_stale_after_seconds"] = int(takeover_stale_after_seconds)
                if heartbeat is not None:
                    # How THIS attempt will be alive, so the server re-derives
                    # the run's liveness mode the takeover resets (2.2's
                    # writer-gone needs `in-process`). Ignored by older servers.
                    body["heartbeat"] = bool(heartbeat)
                    body["launcher"] = bool(launcher)
            if writer is not None:
                # 2.8: the reopening process's lease, written in the reopen's
                # transaction under the receipt's epoch (ignored on a run that
                # is not `leases`). Only after `run_writer_leases`.
                body["writer"] = writer
            # A large rewind legitimately outlasts the 30s default (measured:
            # ~34s for 2.5M points), and the route is idempotent by session_id
            # so even a timeout here is safely retryable — but not needing the
            # retry is better than surviving it.
            resp = self.transport.request(
                "POST",
                f"/v1/runs/{run_id}/reopen",
                json_body=body,
                # The route is idempotent BY SESSION (a replay returns the
                # committed receipt, no second epoch bump or delete), and this
                # body carries a fixed session_id — so the transport may
                # safely retry a lost response. Without this, a timeout after
                # the server committed left the run running-but-unowned, and
                # every later relaunch 409'd: the wedge the replay exists for.
                idempotent=True,
                timeout=180.0 if rewind_to_step is not None else None,
            )
            return resp.json() if resp.content else None
        except errors.NotFoundError as exc:
            raise errors.NotFoundError(
                "this backend predates run reopen (research-os#364): upgrade "
                'the server, or relaunch with on_conflict="supersede"'
            ) from exc

    #: Verdicts attach will reopen automatically. ALL are verdicts NOBODY
    #: CHOSE: 'created' means the run was registered and never started,
    #: 'untracked' means the reaper found nothing owning it, and 'crashed'
    #: means the system saw the job's processes die -- the reaper's silence, a
    #: writer-gone report, a hand-off's leases all GONE (plan 2.8). The last is
    #: exactly what a requeued Slurm job finds seconds after `scontrol requeue`
    #: SIGTERMed its first attempt (the crash notice waits
    #: `crash_notice_requeue_grace_seconds` for it to come back). 'failed' and
    #: 'canceled' are deliberately absent -- a human or a real exit code chose
    #: those, and a stale PROBE_RUN_ID pasted into a .env must not quietly
    #: resurrect last week's cancelled run and write this week's curves into it.
    _REOPENABLE_ON_ATTACH = ("created", "untracked", "crashed")

    #: How long after a run ended attach will still adopt it. Past this, the id
    #: in your environment is much more likely to be stale than to be the run
    #: you meant. 24h covers an overnight queue wait, which is the case this
    #: exists for.
    _REOPEN_MAX_AGE_SECONDS = 24 * 60 * 60

    def _reopen_for_attach(self, data: dict, *, session_id: str | None) -> dict:
        """Make `data` a row this process can actually write to, or raise.

        Four cases, and the distinctions are the whole point:

        * already 'running' -- nothing to do. This is also the MULTI-RANK case:
          eight DDP workers read the same PROBE_RUN_ID, the first reopens, and
          the other seven arrive here to find it live. That is success, not a
          race to lose; treating it as an error would kill every rank but one
          at import and leave a run that looks tracked because rank 0 attached.
        * 'created', 'untracked' or 'crashed' inside the age window -- reopen.
          A queued job reaching its run after the sweep rejoins instead of
          beating into a silent no-op forever, and a requeued one continues the
          run its killed attempt left `crashed`. So is a 'failed' that the
          SIGTERM close wrote (`probe_finish.reason` 'preempted', #2119): a
          scheduler's stop, which is how `scontrol requeue` ends the attempt
          it is about to start again with the same PROBE_RUN_ID.
        * any other 'failed' / 'canceled' / anything past the window -- raise,
          naming the run and when it ended. Somebody chose that ending.
        * reopen refused because a concurrent attach won -- re-read and accept
          the live row, same reasoning as the first case.
        """
        status = data.get("status")
        if status == "running":
            return data
        run_id = data["id"]
        if status not in self._REOPENABLE_ON_ATTACH and not self._ended_by_preemption(data):
            raise errors.ConflictError(
                f"run {data.get('slug') or run_id} is {status!r} and will not be "
                f"reopened by attach (ended {data.get('ended_at')!r}). Something "
                "chose that ending. If PROBE_RUN_ID is left over from an earlier "
                "job, clear it; to deliberately continue this run, reopen it "
                "explicitly with `probe run reopen`."
            )
        ended_at = data.get("ended_at")
        if ended_at and self._older_than_reopen_window(ended_at):
            raise errors.ConflictError(
                f"run {data.get('slug') or run_id} ended at {ended_at}, past the "
                f"{self._REOPEN_MAX_AGE_SECONDS // 3600}h window attach will adopt. "
                "A run id this old in the environment is far more likely to be "
                "stale than intended; clear PROBE_RUN_ID or reopen explicitly."
            )
        if status == "created":
            # 'created' is not a DEAD run, so /reopen refuses it (its reopenable
            # set is the four terminal verdicts). It was never started -- the
            # honest transition is a plain status PATCH, and it needs no epoch
            # bump because no earlier attempt wrote anything to supersede.
            self.transport.request("PATCH", f"/v1/runs/{run_id}", json_body={"status": "running"})
            return self.get_run(run_id)
        try:
            receipt = self.reopen_run(run_id, session_id=session_id or str(uuid.uuid4()))
        except errors.ConflictError:
            # Lost the race to a sibling rank. Whatever it did, the row is live
            # now -- re-read and use it rather than dying on a door someone else
            # already opened.
            fresh = self.get_run(run_id)
            if fresh.get("status") == "running":
                return fresh
            raise
        row = receipt.get("run") or receipt
        if receipt.get("write_epoch") is not None:
            row = {**row, "write_epoch": receipt["write_epoch"]}
            _repin_bracket_lease(run_id, receipt["write_epoch"])
        if receipt.get("last_step") is not None:
            # Plan 2.4: the step the dead attempt reached arms the resume
            # guard (attach_run pops this; it is not a row field).
            row = {**row, "_resume_last_step": receipt["last_step"]}
        return row

    @staticmethod
    def _ended_by_preemption(row: dict) -> bool:
        """A `failed` this SDK's SIGTERM close wrote (#2119): the run's own
        `probe_finish` says `preempted`. Nobody chose it -- a scheduler (or a
        person's `scancel`, which SIGTERM cannot tell apart) stopped the job."""
        from .preempt import REASON

        if row.get("status") != "failed":
            return False
        summary = row.get("summary_metrics") or row.get("summary")
        finish = summary.get("probe_finish") if isinstance(summary, dict) else None
        return isinstance(finish, dict) and finish.get("reason") == REASON

    @classmethod
    def _older_than_reopen_window(cls, ended_at: str) -> bool:
        """True when `ended_at` is outside the adopt window. Unparseable ⇒ False:
        a timestamp we cannot read is not evidence the run is stale, and refusing
        on it would break attach against any server whose format drifts."""
        from datetime import datetime
        from probe._compat import UTC

        try:
            parsed = datetime.fromisoformat(str(ended_at).replace("Z", "+00:00"))
        except (TypeError, ValueError):
            return False
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=UTC)
        return (datetime.now(UTC) - parsed).total_seconds() > cls._REOPEN_MAX_AGE_SECONDS

    def attach_run(
        self,
        run: str | dict,
        *,
        heartbeat: bool = True,
        attached: bool = False,
        reopen_if_dead: bool = False,
        session_id: str | None = None,
        resume_from_step: int | None = None,
        write_epoch: int | None = None,
        writer: dict | None = None,
    ) -> Run:
        """A live handle on an EXISTING run row (or id) in this process.

        The counterpart of create, through the same construction boundary
        (`_wrap_run`), so the heartbeat and auto-update-lock story is
        identical. ``resume_from_step`` arms the monotonic-step guard and
        floors the auto-step counters, so a resumed process cannot re-log
        steps the first execution already wrote.

        ``attached`` (0205) marks every beat from this handle as coming from
        INSIDE the work, which is what stamps ``attached_at`` server-side. The
        launcher's own handle leaves it False.

        ``reopen_if_dead`` (0205) is what makes a late start survivable. The
        server's heartbeat is a SILENT no-op on any non-'running' row, so a job
        that reaches its run after the created-sweep -- a queued Slurm job, a
        Modal cold start -- would otherwise beat forever into nothing and never
        learn it. See :meth:`_reopen_for_attach` for which verdicts it will
        reopen and, more importantly, which it refuses."""
        data = self.get_run(run) if isinstance(run, str) else run
        armed_by_attach = False
        if reopen_if_dead:
            data = self._reopen_for_attach(data, session_id=session_id)
            # A reopen MINTS a new generation, and that generation is the only
            # one the server will accept writes under. The caller's
            # `write_epoch` (PROBE_RUN_EPOCH, exported by the launcher BEFORE
            # this reopen existed) is now stale by exactly one, so it must not
            # win: applying it fenced every metric, log and span for the rest of
            # the job -- in precisely the queued-start case the reopen is for.
            reopened_epoch = data.get("write_epoch")
            if reopened_epoch is not None:
                write_epoch = int(reopened_epoch)
            data = dict(data)
            reopened_last_step = data.pop("_resume_last_step", None)
            if resume_from_step is None and reopened_last_step is not None:
                # A requeued job restarting from an older checkpoint must drop
                # what the dead attempt already wrote, not splice over it.
                resume_from_step = int(reopened_last_step)
                armed_by_attach = True
        # Settle the epoch BEFORE _wrap_run, not after: _wrap_run starts the
        # beat thread and the synchronous attached-beat below, and both read the
        # handle's epoch. Setting it afterwards left the fence off exactly the
        # beats that keep a superseded run looking alive.
        if write_epoch is not None:
            data = {**data, "write_epoch": int(write_epoch)}
        lease = None
        if heartbeat and self._leases_available():
            # 2.8: this process writes the run under its own lease. An OWNER
            # when its verdict is the run's: a resume or takeover this process
            # reopened, or a job that joined from inside the work (PROBE_RUN_ID)
            # with no finalizing launcher to close it and no non-zero rank --
            # a forwarded PROBE_RUN_ID, a scheduler hand-off. Its release is
            # then a work-ender and it sends no status of its own (review of
            # #2060: a status PATCH after the leases' close overwrote the
            # worst verdict). A `rank` otherwise: a rank of a distributed job,
            # or a job under `probe exec`, whose launcher decides.
            session_id = session_id or str(uuid.uuid4())
            # ``writer``: the lease a reopen this process made already sent (a
            # resume keeps the role it reopened under, a launcher's included).
            lease = writer or _writer_lease(
                "rank" if attached and not self._attached_owns_verdict(data) else "owner",
                session_id,
            )
        handle = self._wrap_run(
            data, heartbeat=heartbeat, attached=attached, session_id=session_id, lease=lease
        )
        if lease is not None:
            # The lease is registered SYNCHRONOUSLY, before this process writes
            # anything (review of the 2.8 design, MED-6); the beat also stamps
            # `attached_at` for a rank and answers which rules the run follows.
            # Every rank of a large job attaches at once, so each first waits a
            # moment scaled to the job's size (at most 2 s) instead of landing
            # 600 inserts on one run in the same instant (review of #2060).
            # Best-effort: a liveness report, never a reason to take down the work.
            try:
                pause = _attach_jitter_seconds(lease.get("world_size"))
                if pause:
                    time.sleep(random.uniform(0.0, pause))
                body = {**lease, "write_epoch": handle.write_epoch or 1}
                if attached:
                    body["attached"] = True
                answer = self.beat_writer(handle.id, session_id, body)
                handle._note_lease_answer(answer)
            except Exception:
                pass
        elif attached:
            # One beat SYNCHRONOUSLY, here, rather than waiting for the loop's
            # first tick. `attached_at` is what the dashboard reads as "the job
            # itself is reporting", and leaving it up to thread scheduling means
            # a job that attaches and immediately finishes never records that it
            # attached at all. Best-effort: a failure here is a liveness report,
            # never a reason to take down the work.
            try:
                self.heartbeat_run(handle.id, attached=True, write_epoch=handle.write_epoch)
            except Exception:
                pass
        if resume_from_step is not None:
            from probe.hw.integration import SUSPECT_RESUME_FLOOR

            if resume_from_step >= SUSPECT_RESUME_FLOOR:
                # A last_step in hardware's epoch range means the server
                # computed the receipt WITHOUT the #364 hardware exclusion.
                # Arming would refuse every training step — fail open with a
                # warning instead (warn-never-gate).
                warnings.warn(
                    f"resume receipt last_step={resume_from_step} is in the "
                    "hardware rail's epoch range — this server predates the "
                    "hardware exclusion (research-os#364); the resume step "
                    "guard is disabled for this attach",
                    stacklevel=2,
                )
            else:
                handle.arm_resume_guard(resume_from_step)
                # Its drop warning then names the exits that work from an
                # attach, since probe.init() joining PROBE_RUN_ID takes no
                # on_conflict (Run._resume_exits).
                handle._resume_via_attach = armed_by_attach
        return handle

    @_walks_once
    def resolve_or_raise(self, kind: str, slug: str, *, project_id: str | None = None) -> dict:
        """Resolve a slug or raise the error that says what to do about it.

        Two outcomes: present (return it) or absent (create it, with near misses
        named). There used to be a third — ARCHIVED, where lookup said "missing"
        and create said "already exists" about the same slug — but archiving is
        gone, so a deleted slug is genuinely free. Both `run()` and the CLI go
        through here so the same failure cannot exit 1 from one surface and 2
        from the other."""
        if kind == "project":
            found = self.resolve_project(slug)
            if found is not None:
                return found
            raise self._no_such(kind, slug, self.list_projects(limit=200).items)
        # An experiment: in the named project first (one request), then -- only
        # on a miss -- every project's, so an experiment filed elsewhere comes
        # back for `run()` to name the mismatch ("not in project ...") rather
        # than reading as absent, and a real absence names near misses from the
        # whole tenant (slugs are tenant-wide).
        if project_id:
            found = self.resolve_experiment(slug, project_id=project_id)
            if found is not None:
                return found
        found = self.resolve_experiment(slug)
        if found is not None:
            return found
        # A real absence: name the near misses, which needs the whole list.
        raise self._no_such(kind, slug, self._all_slugs("experiment"))

    @staticmethod
    def _near(slug: str, existing: Iterable[dict]) -> list[str]:
        """Existing slugs close enough to ``slug`` to be what the caller meant.

        A mistyped slug is by definition CLOSE to a real one; a genuinely new
        name is not. That asymmetry is what lets one list serve both a hard
        error (when we cannot proceed) and a warning (when we can)."""
        slugs = [row["slug"] for row in existing if row.get("slug")]
        return difflib.get_close_matches(slug, slugs, n=3, cutoff=0.6)

    def _all_slugs(self, kind: str) -> list[dict]:
        """Every row of `kind`, following the cursor.

        The near-miss guard leans on seeing the WHOLE namespace. `limit=200` is
        the schema maximum, and page ordering is unspecified, so stopping at one
        page means the guard silently stops firing past 200 rows — and it is the
        older slugs that drop out of view, which are exactly the ones a typo is
        likely to be a near-miss of. `analysis.compare()` follows the cursor for
        the same reason."""
        if kind != "project":
            # Tenant-wide on purpose: experiment slugs are unique per TENANT, not
            # per project (see resolve_experiment). Scoping this to a project
            # would let a typo of an experiment filed elsewhere sail through.
            return self._tenant_experiments()
        rows: list[dict] = []
        cursor = None
        while True:
            page = self.list_projects(limit=200, cursor=cursor)
            rows.extend(page.items)
            cursor = page.next_cursor
            if not cursor:
                return rows

    def _guard_creatable(self, kind: str, slug: str) -> None:
        """Raise unless `slug` is safe to CREATE (near-miss guard).

        Split out of ensure_* so `run()` can run it BEFORE it commits a parent:
        otherwise a refused experiment leaves a brand-new project behind, which is
        precisely the orphan identity this whole guard exists to prevent."""
        self._refuse_near_miss(kind, slug, self._all_slugs(kind))

    def _refuse_near_miss(self, kind: str, slug: str, existing: Iterable[dict]) -> None:
        """Refuse to CREATE a slug that looks like a typo of an existing one.

        A warning was the obvious first answer and it is the wrong one. The two
        places this fires — a detached ``probe run start`` process and a training
        loop — are both places nobody reads warnings, and this repo has already
        run that experiment: the ``[auto]`` question shipped WITH a fix
        affordance (``probe experiment set``) and it went unused every time. An
        invisible guard is not a guard.

        Refusing costs a caller who genuinely wants a near-identical name one
        explicit ``create_experiment``. Warning costs everyone else a second
        identity that every later comparison reads as a different thing.

        The 0.6 cutoff keeps short version-y names usable — ``v1`` vs ``v2``
        scores 0.5 and passes — so what this catches is long, near-identical
        slugs, which are far likelier to be typos than intent."""
        # An EXACT match is not a typo, it is the row itself — reachable when the
        # listing sees a slug the resolve did not (a create race, or a stale read
        # replica). Refusing there would turn "someone just made this" into a hard
        # error about a name that is already correct.
        near = [n for n in self._near(slug, existing) if n != slug]
        if not near:
            return
        cli_hint = ' --question "..." --project PROJECT_SLUG' if kind == "experiment" else ""
        sdk_hint = ", question=..., project_id=PROJECT_ID" if kind == "experiment" else ""
        raise errors.ValidationError(
            f"refusing to create {kind} {slug!r}: it is a near-miss of "
            f"{', '.join(repr(n) for n in near)}. If you meant the existing one, "
            f"use that slug. If this really is new, create it explicitly — "
            f"`client.create_{kind}({slug!r}{sdk_hint})` or "
            f"`probe {kind} create {shlex.quote(slug)}{cli_hint}`."
        )

    @staticmethod
    def _no_such(kind: str, slug: str, existing: Iterable[dict]) -> errors.NotFoundError:
        """A not-found that names near misses, so a typo says what you meant.

        A mistyped slug is by definition CLOSE to a real one; a genuinely new
        name is not. Suggesting neighbours turns the common case from "what do
        you mean it does not exist" into an obvious one-character fix."""
        near = Client._near(slug, existing)
        hint = f" Did you mean: {', '.join(near)}?" if near else ""
        # The suggested command has to actually RUN. `experiment create` requires
        # --question, so omitting it would print a command that fails on the one
        # field this whole change exists to force. The slug is quoted because it
        # arrives from the caller and this string is presented as copy-pasteable.
        extra = ' --question "..." --project PROJECT_SLUG' if kind == "experiment" else ""
        return errors.NotFoundError(
            f"no {kind} with slug {slug!r}.{hint} "
            f"Create it with `probe {kind} create {shlex.quote(slug)}{extra}` "
            "if it is genuinely new."
        )

    def heartbeat_run(
        self,
        run_id: str,
        role: str = "owner",
        *,
        attached: bool = False,
        write_epoch: int | None = None,
    ) -> dict:
        """``POST /v1/runs/{id}/heartbeat``: report that this run is still alive.

        Liveness cannot be inferred from `status`: it is a plain column, so a run
        whose process dies without a final PATCH stays 'running' forever and any
        "what is active" count decays into noise. Call this periodically while a
        run executes; the server's reaper marks an OWNER that stops beating as
        'crashed', and a run that goes silent without ever having had an owner
        beat as 'untracked'.

        ``role`` keeps the ownership rule honest. ``owner`` (the default)
        asserts "the run's process is alive" and may only be sent by a process
        whose lifetime IS the run's lifetime -- beat for the run's whole life or
        not at all. ``observer`` asserts only "something is still watching"
        (the miles exporter sidecar): it keeps the run out of the reaper's scan
        while attached, but its silence resolves to 'untracked', never
        'crashed', because a watcher dying proves nothing about the work.

        SDK handles beat automatically: ``create_run`` starts a background
        thread (see :meth:`Run.start_heartbeat`) unless called with
        ``heartbeat=False``. Call this method directly only for runs managed
        outside the SDK — e.g. a workflow driver renewing the lease on a run it
        opened with ``probe run start``.

        Only a 'running' run is stamped; a late beat racing a normal completion
        is a no-op rather than an error.
        """
        if role not in ("owner", "observer"):
            # The beat loop swallows exceptions; a typo'd role would 422
            # silently forever. Fail at the call site instead.
            raise ValueError(f"heartbeat role must be 'owner' or 'observer', got {role!r}")
        # Fencing (0185): the epoch rides as a query param (this route has no
        # body); a pre-0185 server drops it, a 0185+ one 409s a superseded
        # writer so the zombie learns it lost.
        params: dict = {}
        if role != "owner":
            params["role"] = role
        # 0205. `attached` says this beat comes from INSIDE the work, not from a
        # launcher holding the run open around it. Only these stamp attached_at,
        # which is how "the job never plugged in" stays expressible under a
        # wrapped run where both processes beat as owners. Omitted when false so
        # a pre-0205 server sees exactly the request it saw before.
        if attached:
            params["attached"] = "true"
        if write_epoch is not None:
            params["write_epoch"] = write_epoch
        if params:
            return self.transport.request(
                "POST",
                f"/v1/runs/{run_id}/heartbeat",
                params=params,
                idempotent=True,
            ).json()
        return self.transport.post(f"/v1/runs/{run_id}/heartbeat", None, idempotent=True)

    def beat_writer(self, run_id: str, session_id: str, body: dict) -> dict:
        """``POST /v1/runs/{id}/writers/{session}/beat`` (SDK reliability 2.8):
        one lease beat. The first registers the lease. Returns
        ``{run_status, write_epoch, liveness_protocol}``; a 409 means a newer
        attempt took the run over."""
        return self.transport.post(
            f"/v1/runs/{run_id}/writers/{session_id}/beat", body, idempotent=True
        ) or {}

    def release_writer(self, run_id: str, session_id: str, body: dict) -> dict:
        """``POST /v1/runs/{id}/writers/{session}/release`` (2.8): this writer
        is done with ``exit_status``; the server closes the run once its leases
        say the work ended. Idempotent per session. Returns ``{run_status,
        closed, liveness_protocol}``."""
        return self.transport.post(
            f"/v1/runs/{run_id}/writers/{session_id}/release", body, idempotent=True
        ) or {}

    def list_writers(self, run_id: str) -> list[dict]:
        """``GET /v1/runs/{id}/writers`` (2.8): the run's writer leases, newest
        epoch first, each with its derived ``state`` (beating, draining,
        released, gone, expired) and whether it is on the ``current`` epoch."""
        return self.transport.get(f"/v1/runs/{run_id}/writers") or []

    def report_writer_gone(self, run_id: str, body: dict) -> dict:
        """``POST /v1/runs/{id}/writer-gone`` (SDK reliability 2.2): tell the
        server this run's writer process is gone, so a sole-writer run ends
        `crashed` in seconds rather than after the reaper's 900 s. Sent by the
        output helper's reporter and the node agent, never by the writer
        itself; only after ``supports_feature("run_writer_gone")``. Returns
        ``{run_id, applied, status, reason}``."""
        resp = self.transport.request("POST", f"/v1/runs/{run_id}/writer-gone", json_body=body)
        return resp.json() if resp.content else {}

    # -- server capabilities (0185) -----------------------------------------
    def supports_feature(self, name: str) -> bool:
        """Whether the connected server declares ``name`` in
        ``GET /v1/server/features``.

        Cached for the client's lifetime: the answer is a property of the
        deployed build, and one process talks to one deployment. A 404 on the
        route itself IS the answer — a server too old to have the route is too
        old to have any feature the route would declare."""
        feats = getattr(self, "_server_features_cache", None)
        if feats is None:
            try:
                data = self.transport.get("/v1/server/features")
                feats = frozenset((data or {}).get("features") or ())
            except errors.NotFoundError:
                feats = frozenset()
            self._server_features_cache = feats
        return name in feats

    def _require_feature(self, name: str, message: str) -> None:
        """Preflight gate: refuse BEFORE any state changes, with the fix named.

        Exists for requests whose worst failure is a server silently ignoring
        an unknown field — for those, discovering skew after the write is
        discovering it too late."""
        if not self.supports_feature(name):
            raise errors.NotFoundError(message)

    # -- fork (0185) ---------------------------------------------------------
    def fork_run(
        self,
        source: str,
        *,
        step: int | None = None,
        name: str | None = None,
        **run_kw,
    ) -> Run:
        """Open a NEW run that continues ``source`` from ``step``, leaving the
        source untouched and unmarked — the keep-both alternative to
        ``Rewind``.

        W&B's fork shape: the new run carries ``parent_relation="fork"`` plus
        ``fork_of``/``fork_step`` foreign keys and logs from the checkpoint
        step onward under its own identity, so both curves survive. Works from
        any source status — a fork reads the source's row and writes nothing
        to it (unlike ``supersede``, which is a from-scratch RETRY and tags a
        dead incumbent ``superseded``).
        """
        src = self.get_run(source)
        fork_name = name or f"{src.get('name') or str(src['id'])[:8]}-fork"
        if name is None and run_kw.get("authored_by") is None:
            # THE SDK composed this NAME, so say so -- but only when the caller
            # has not declared anything. `--authored-by human` on a fork with no
            # `--name` is the normal shape of "the researcher dictated the
            # description", and overwriting it here made the flag silently
            # inert on the exact path it is most used on.
            run_kw["authored_by"] = agent_session.AUTHORSHIP_AGENT
        kw = dict(run_kw, parent_run_id=src["id"], parent_relation="fork")
        experiment_id = src.get("experiment_id")
        if experiment_id:
            run = self.create_run(experiment_id, fork_name, **kw)
        elif src.get("project_id"):
            run = self.create_project_run(src["project_id"], fork_name, **kw)
        elif "project_id" in src:
            # A FLOATING source (daemon v2) begets a floating fork; it is filed
            # with its source, or on its own, later.
            run = self.create_floating_run(fork_name, **kw)
        else:
            raise errors.ValidationError(
                f"run {source} reports neither an experiment nor a project — this "
                "research-os backend predates project-direct runs (0054)."
            )
        links: dict = {"fork_of": src["id"]}
        if step is not None:
            links["fork_step"] = step
        # link() is the sanctioned foreign-keys surface; per-key new-wins.
        run.link(**links)
        return run

    # -- runs (read) --------------------------------------------------------
    def get_run(self, run_id: str) -> dict:
        return self.transport.get(f"/v1/runs/{run_id}")

    # -- trials (read) ------------------------------------------------------
    def list_run_trials(
        self,
        run_ref: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
    ) -> Page:
        """One cursor-aware page of authored Trials belonging to a Run."""
        params = {
            key: value
            for key, value in {"cursor": cursor, "limit": limit}.items()
            if value is not None
        }
        return self.transport.get_page(f"/v1/runs/{run_ref}/trials", params=params or None)

    def get_trial(self, trial_id: str) -> dict:
        """Read one rollout-backed Trial by its rollout span id."""
        return self.transport.get(f"/v1/trials/{trial_id}")

    # -- trials (write) -----------------------------------------------------
    def update_trial(
        self,
        trial_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
    ) -> dict:
        """Field-replace PATCH on the AUTHORED half of a Trial.

        Only what a person writes: title and description. Lifecycle, result and
        timing stay the producer's, and a span retry keeps rewriting them --
        which is exactly why the two halves are separate rows and why this cannot
        reach the other one.

        Notes are NOT here because a Trial HAS none -- the one research entity
        without a notes document. A rollout ran once and is immutable, so
        `description` is the whole of its prose; there is no `--trial` flag on
        `probe notes push` either.
        """
        model = TrialPatch(name=name, description=description)
        body = model.model_dump(mode="json", exclude_none=True)
        if not body:
            raise ValueError("update_trial needs at least one of name/description")
        return self.transport.patch(f"/v1/trials/{trial_id}", body)

    def claim_sandbox_base_state(self, run_id: str, ref: str, owner_key: str) -> dict:
        """Atomically elect one begin-state capturer for a run-local ref.

        This is intentionally synchronous: a queued claim cannot tell the
        caller whether to archive the environment it is about to execute.
        """
        return self.transport.post(
            f"/v1/runs/{run_id}/sandbox-state/base-state/claim",
            {"ref": ref, "owner_key": owner_key},
        )

    def update_run(
        self,
        run_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        notes: str | None = None,
        status: str | None = None,
        authored_by: str | None = None,
    ) -> dict:
        """PATCH /v1/runs/{id} — amend a run's authored fields.

        ``status`` CORRECTS the run's recorded status and sends nothing else: no
        ``ended_at``, no ``started_at``, no ``write_epoch``, so the run's start,
        end and duration stay exactly as recorded. Closing a run you are running
        is ``Run.finish`` (``probe run end``), which stamps the end time.

        0220: a run carries no authored document -- see ``update_project`` and
        ``update_experiment``, whose ``document`` is the Overview page's marked
        block. Read immediately before editing and preserve useful
        sections; ``""`` clears it. A line containing only
        ``[README](https://github.com/owner/repo)`` embeds that README and derives
        the run's read-only ``repo`` field.

        ``notes`` (server 0096) is the door that matters most for that field: a
        run's caveat is nearly always learned after the run finished. It is NOT a
        second description — a description says what the run is, notes says what a
        later reader should distrust about it, and writing the caveat into
        ``description`` means destroying the description to keep it.

        Omitting a field leaves it alone; passing ``""`` for ``notes`` clears it."""
        body = {
            key: value
            for key, value in {
                "name": name,
                "description": description,
                "notes": notes,
                "status": status,
            }.items()
            if value is not None
        }
        if not body:
            raise ValueError("update_run needs at least one of name/description/notes/status")
        # AFTER the emptiness check, deliberately. `authored_by` declares who
        # wrote the OTHER fields; on its own it declares authorship of nothing,
        # and letting it satisfy "at least one field to set" would turn a
        # no-op call into a PATCH.
        _put_authorship(body, authored_by)
        row = self.transport.patch(f"/v1/runs/{run_id}", body)
        self._warn_if_notes_dropped(notes, row, "runs")
        return row

    def run_bundle(self, run_id: str, *, source_read_contract: str | None = None) -> dict:
        """GET /v1/runs/{id}/bundle. A SOURCE-BACKED run (a W&B mirror, say)
        answers 422 `unsupported_source_query` unless the caller names the
        coverage read contract: its metric catalog carries the provider's
        coverage receipts, which an older client would render as exact. Pass
        ``source_read_contract=SOURCE_READ_CONTRACT`` where the caller reads
        those receipts (or ignores the catalog); the default sends nothing."""
        params = (
            {"source_read_contract": source_read_contract} if source_read_contract else None
        )
        return self.transport.get(f"/v1/runs/{run_id}/bundle", params=params)

    def run_reproduce(self, run_id: str) -> dict:
        """GET /v1/runs/{id}/reproduce — the server-assembled reproduction record:
        execution record, launch context, restore command, code snapshot,
        inputs-decision (content inlined when small), notes, lockfiles, lineage
        edges, per-span env refs, and a completeness verdict. This is a thin
        passthrough on purpose — the backend is the one place that reads every
        piece together (research-os app/read_models/reproduce.py). A run captured
        before capture-core answers 200 with a degraded body, never a 404."""
        return self.transport.get(f"/v1/runs/{run_id}/reproduce")

    def experiment_reproduce(self, experiment_id: str, *, version: int | None = None) -> dict:
        """GET /v1/projects/{id}/reproduce — per-run reproduction summaries (a
        map, not N full assemblies; each summary carries a `reproduce_url` for
        drill-down). `version` pins against a minted experiment_versions manifest;
        omitted reads live rows."""
        params = {"version": version} if version is not None else None
        return self.transport.get(f"/v1/projects/{experiment_id}/reproduce", params=params)

    def run_lineage(self, run_id: str) -> dict:
        return self.transport.get(f"/v1/runs/{run_id}/lineage")

    def run_metrics(
        self,
        run_id: str,
        *,
        key: str | None = None,
        kind: str | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Raw metric points for a run. :meth:`run_series` is the summarized view;
        :meth:`query_series` is the multi-run comparison. A logged NaN / +inf /
        -inf comes back as that float (see :mod:`probe.sdk.nonfinite`)."""
        params = {
            k: v for k, v in {"key": key, "kind": kind, "limit": limit}.items() if v is not None
        }
        rows = self.transport.get(f"/v1/runs/{run_id}/metrics", params=params or None)
        return [nonfinite.to_float(row) for row in rows]

    def delete_series(
        self,
        run_id: str,
        *,
        key: str,
        kind: str = "model",
        dimensions: dict | None = None,
    ) -> None:
        """Delete a DERIVED series and its points — the counterpart to pushing one.

        Derived only: a logged series is the run's captured record, cannot be
        recomputed, and has no undo, so the server refuses it with a 409.

        Identity is (kind, key, dimensions), the same triple a write uses.
        `dimensions` pins ONE variant; omitting it addresses the dimension-less
        series, not every variant of the key."""
        params = {"kind": kind, "key": key}
        if dimensions is not None:
            params["dimensions"] = json.dumps(dimensions)
        self.transport.request("DELETE", f"/v1/runs/{run_id}/series", params=params)

    def run_series(self, run_id: str) -> list[dict]:
        """Per-series summary for a run (key/kind/dimensions + first/last/min/max)."""
        return self.transport.get(
            f"/v1/runs/{run_id}/series",
            params={"source_read_contract": SOURCE_READ_CONTRACT},
        )

    # -- coordinate reads (below-run coordinates, research-os 0059-0062) -----
    def get_metrics_grouped(
        self,
        run_id: str,
        key: str,
        *,
        kind: str | None = None,
        agg: str | None = None,
        by: list[str] | None = None,
        where: dict[str, Any] | None = None,
        step_bucket: int | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """Server-side reduce/group over one metric's stepped points (0059).

        ``by`` names coordinate axes to split on (sent comma-joined; one cell per
        combination of axis values); ``where`` is a coord filter dict (sent
        JSON-encoded, matched by type-faithful containment). ``agg`` is one of
        mean|sum|min|max|count — OPTIONAL since server 0062: omitted resolves to
        the key's DECLARED reduce fn (see :meth:`Run.log`'s ``agg``), else mean;
        conflicting declarations are a 422. An unknown ``by``/``where`` axis or a
        kind-ambiguous key is a 422, never a silent empty reduction.

        Paging is followed here: a truncated page's ``next_step`` is fed back as
        ``step_from`` until the reduction is exhausted, so one call answers the
        whole range. ``max_rows`` bounds the TOTAL cells returned — when it cuts
        the read short (or ``_MAX_STEPPED_PAGES`` does), the result says so:
        ``truncated`` is True and ``next_step`` is where to resume."""
        merged: dict | None = None
        remaining = max_rows
        for _ in range(_MAX_STEPPED_PAGES):
            params = {
                param: value
                for param, value in {
                    "key": key,
                    "kind": kind,
                    "agg": agg,
                    "by": ",".join(by) if by else None,
                    "where": json.dumps(where) if where is not None else None,
                    "step_bucket": step_bucket,
                    "step_from": step_from,
                    "step_to": step_to,
                    "max_rows": remaining,
                }.items()
                if value is not None
            }
            page = self.transport.get(f"/v1/runs/{run_id}/metrics/grouped", params=params)
            if merged is None:
                merged = page
            else:
                merged["groups"].extend(page.get("groups") or [])
                merged["truncated"] = page.get("truncated", False)
                merged["next_step"] = page.get("next_step")
            if remaining is not None:
                remaining -= len(page.get("groups") or ())
                if remaining <= 0:
                    break
            if not page.get("truncated") or page.get("next_step") is None:
                break
            step_from = page["next_step"]
        return merged

    def get_metrics_wide(
        self,
        run_id: str,
        *,
        key: list[str] | None = None,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """Step x metric table for a run — the DataFrame pivot, aligned by step.

        Same paging treatment as :meth:`get_metrics_grouped`: ``next_step`` is
        followed until the table is exhausted (rows realigned by series identity,
        since a page's columns cover only its own step window), ``max_rows``
        bounds the TOTAL step rows, and a short read reports ``truncated`` +
        ``next_step``. ``key`` narrows to those metric keys (repeated query
        param, matching the route's array parameter)."""
        merged: dict | None = None
        remaining = max_rows
        for _ in range(_MAX_STEPPED_PAGES):
            params = {
                param: value
                for param, value in {
                    "key": key or None,
                    "kind": kind,
                    "step_from": step_from,
                    "step_to": step_to,
                    "max_rows": remaining,
                    "source_read_contract": SOURCE_READ_CONTRACT,
                }.items()
                if value is not None
            }
            page = self.transport.get(f"/v1/runs/{run_id}/metrics/wide", params=params or None)
            if merged is None:
                merged = page
            else:
                _merge_wide_page(merged, page)
                merged["truncated"] = page.get("truncated", False)
                merged["next_step"] = page.get("next_step")
            if remaining is not None:
                remaining -= len(page.get("rows") or ())
                if remaining <= 0:
                    break
            if not page.get("truncated") or page.get("next_step") is None:
                break
            step_from = page["next_step"]
        return merged

    def export_metric_points(
        self,
        run_id: str,
        *,
        key: str | None = None,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        after_id: int | None = None,
        limit: int | None = None,
    ):
        """Lossless raw-point export: every point exactly once, labels included,
        no downsampling. A GENERATOR — the ``after_id`` keyset paging is followed
        transparently, so callers just iterate; ``limit`` is the page size of the
        walk, not a total bound. Pass ``after_id`` to resume a previous walk from
        its last point id. A logged NaN / +inf / -inf comes back as that float
        (see :mod:`probe.sdk.nonfinite`)."""
        while True:
            params = {
                param: value
                for param, value in {
                    "key": key,
                    "kind": kind,
                    "step_from": step_from,
                    "step_to": step_to,
                    "after_id": after_id,
                    "limit": limit,
                }.items()
                if value is not None
            }
            page = self.transport.get(f"/v1/runs/{run_id}/metrics/export", params=params or None)
            for point in page.get("points") or ():
                yield nonfinite.to_float(point)
            next_after_id = page.get("next_after_id")
            # None means the last currently visible page. The monotonic check is
            # the loop's own guard: a cursor that fails to advance would replay
            # the same page forever, and an infinite generator that yields
            # duplicates is worse than stopping at the point already delivered.
            if next_after_id is None or (after_id is not None and next_after_id <= after_id):
                return
            after_id = next_after_id

    def list_run_coordinates(self, run_id: str) -> list[dict]:
        """The run's coordinate catalog (0060): every non-empty coordinate any
        fact has landed on, with which fact tables have it — enumeration for
        split/overlay pickers without scanning points/spans/artifacts. Bounded by
        the series cap's cardinality arithmetic, so no pagination."""
        return self.transport.get(f"/v1/runs/{run_id}/coordinates")

    # -- expression views (read-time computed panels, research-os 0088) ------
    def create_view(self, run_id: str, name: str, spec: Any) -> dict:
        """Save an expression view on a run — a formula over series the run has
        already logged, evaluated at READ time (no points are stored).

        ``spec`` is a :class:`probe.expr.Expr`, a node dict, or a full
        ``{"expression": ...}`` mapping; all three normalize through
        :func:`probe.expr.spec`, which validates before anything reaches the
        wire. Names are unique per run among live views.

        Works on a COMPLETED run: a view reads the catalog, it does not append to
        the run's history. Nothing about finishing a run closes this door."""
        body = MetricViewCreate(name=name, spec=_view_spec(spec))
        return self.transport.post(
            f"/v1/runs/{run_id}/views", body.model_dump(mode="json", exclude_none=True)
        )

    def list_views(self, run_id: str) -> list[dict]:
        """Every live view on a run, with its spec and provenance."""
        return self.transport.get(f"/v1/runs/{run_id}/views")

    def update_view(
        self,
        view_id: str,
        *,
        name: str | None = None,
        spec: Any = None,
        expected_updated_at: str | None = None,
    ) -> dict:
        """Rename a view and/or replace its expression. Omitted fields are left
        alone — this is a PATCH, not a whole-row write.

        ``spec`` REPLACES the stored expression whole. ``expected_updated_at``
        is the view's ``updated_at`` as you read it: the server then refuses
        (409, carrying the current name, spec and ``updated_at``) instead of
        overwriting an edit made since. Omitted, the write is unconditional."""
        body: dict = {}
        if name is not None:
            body["name"] = name
        if spec is not None:
            body["spec"] = _view_spec(spec)
        if not body:
            raise ValueError("update_view needs a name or a spec to change")
        # AFTER the emptiness check: a precondition alone changes nothing.
        if expected_updated_at is not None:
            body["expected_updated_at"] = expected_updated_at
        return self.transport.patch(
            f"/v1/views/{view_id}",
            MetricViewPatch(**body).model_dump(mode="json", exclude_none=True),
        )

    def delete_view(self, view_id: str) -> None:
        """Soft-delete a view. The series it read are untouched."""
        self.transport.delete(f"/v1/views/{view_id}")

    def view_data(
        self,
        run_id: str,
        view_id: str,
        *,
        step_from: int | None = None,
        step_to: int | None = None,
        max_points: int | None = None,
    ) -> dict:
        """Evaluate a saved view and return its curve.

        Read the envelope, not just ``points``: ``missing_inputs`` names series
        the expression referenced that the run has none of, ``dropped_nonfinite``
        counts steps whose result was NaN/inf (a divide-by-zero), and
        ``truncated`` says the input scan hit its bound before the range ended.
        An empty ``points`` with a populated ``missing_inputs`` is a typo in the
        spec, not a run with no data."""
        params = {
            param: value
            for param, value in {
                "step_from": step_from,
                "step_to": step_to,
                "max_points": max_points,
            }.items()
            if value is not None
        }
        return self.transport.get(f"/v1/runs/{run_id}/views/{view_id}/data", params=params or None)

    def preview_view(
        self,
        run_id: str,
        spec: Any,
        *,
        step_from: int | None = None,
        step_to: int | None = None,
        max_points: int | None = None,
    ) -> dict:
        """Evaluate a spec WITHOUT saving it — same envelope as :meth:`view_data`.

        The check to run before :meth:`create_view`: a spec that names a series
        the run never logged comes back with ``missing_inputs`` here, instead of
        being saved as a panel that renders empty for everyone."""
        body = MetricViewPreviewRequest(
            spec=_view_spec(spec),
            step_from=step_from,
            step_to=step_to,
            **({"max_points": max_points} if max_points is not None else {}),
        )
        return self.transport.post(
            f"/v1/runs/{run_id}/views/preview",
            body.model_dump(mode="json", exclude_none=True),
        )

    def run_spans(
        self,
        run_id: str,
        *,
        span_type: str | None = None,
        parent_span_id: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        limit: int | None = None,
    ) -> list[dict]:
        """Read a run's trajectory spans back (the write path is ``Run.span``)."""
        params = {
            k: v
            for k, v in {
                "span_type": span_type,
                "parent_span_id": parent_span_id,
                "step_from": step_from,
                "step_to": step_to,
                "limit": limit,
            }.items()
            if v is not None
        }
        return self.transport.get(f"/v1/runs/{run_id}/spans", params=params or None)

    def get_span(self, span_id: str) -> dict:
        return self.transport.get(f"/v1/spans/{span_id}")

    # -- lifecycle (delete = move to the trash) -----------------------------
    def delete_run(self, run_id: str) -> dict | None:
        """Move a run, with its telemetry, to the server's TRASH. Frees its
        natural key.

        Spans, metrics, artifacts and lineage go with it. Probe support can
        restore it for 21 days (the returned receipt says until when); after
        that it is deleted for good. A server without the `trash` feature
        deletes PERMANENTLY and returns None. 404 if the run does not exist."""
        return self.transport.delete(f"/v1/runs/{run_id}")

    # -- per-file code capture (0193) ----------------------------------------
    def presign_capture_batch(
        self, run_id: str, items: list[dict], *, captured_at: str | None = None
    ) -> dict:
        """Mint one ``kind='code'`` artifact row per captured file, deduped on
        content (``POST /v1/runs/{id}/artifacts/uploads/batch``). Each item is
        ``{name, content_hash, size_bytes, mode}``; the answer carries, per item,
        ``have`` (already stored, nothing to PUT), a checksum-pinned
        ``upload_url`` + ``upload_headers``, or a per-item ``error``."""
        body: dict[str, Any] = {"items": items}
        if captured_at is not None:
            body["captured_at"] = captured_at
        # Idempotent by the server's contract (a retried batch returns the same
        # ids), so the transport's bounded backoff covers a 502/503/504.
        return self.transport.post(
            f"/v1/runs/{run_id}/artifacts/uploads/batch", body, idempotent=True
        )

    def confirm_capture_batch(self, artifact_ids: list[str]) -> dict:
        """HEAD-verify and flip capture rows complete
        (``POST /v1/artifacts/confirm/batch``). Five buckets: ``confirmed``;
        ``unconfirmed`` (object not there yet -- retry the PUT once); ``refused``
        (a live row that is not a capture row: the researcher registered that
        name and bytes on purpose); ``failed`` (the upload reaper gave up on it;
        re-run the capture to revive it); ``unknown`` (no live row). Only
        ``unconfirmed`` is worth a retry; the rest are verdicts."""
        return self.transport.post(
            "/v1/artifacts/confirm/batch", {"artifact_ids": list(artifact_ids)}, idempotent=True
        )

    def presign_download_batch(self, artifact_ids: list[str]) -> dict:
        """Presigned GETs for up to 1,000 artifacts at once
        (``POST /v1/artifacts/download/batch``): ``{items: {id: {download_url}},
        unknown: [...], refused: {id: reason}}`` -- ``refused`` names a live row
        that cannot be fetched (not complete, a reference pointer, no pointer).
        Restore of a captured tree needs one URL per file."""
        return self.transport.post(
            "/v1/artifacts/download/batch", {"artifact_ids": list(artifact_ids)}, idempotent=True
        )

    def list_run_artifact_tree(
        self, run_id: str, *, prefix: str = "", limit: int | None = None
    ) -> dict:
        """One folder level of a run's artifacts
        (``GET /v1/runs/{id}/artifacts/tree``): the files whose folder is exactly
        ``prefix`` plus each direct child folder with its descendant count."""
        params = {k: v for k, v in {"prefix": prefix, "limit": limit}.items() if v is not None}
        return self.transport.get(f"/v1/runs/{run_id}/artifacts/tree", params=params)

    def presign_download(self, artifact_id: str) -> str:
        """Presigned GET URL for an artifact's blob (``POST /v1/artifacts/{id}/download``).

        The one home for this route literal: ``download_artifact*`` and the callers
        that need the raw doc in memory (``trial expand``, ``asset materialize``) all
        route through here, so the parity guard sees one reachable call site."""
        return self.transport.post(f"/v1/artifacts/{artifact_id}/download", None)["download_url"]

    def download_artifact(self, artifact_id: str) -> bytes:
        """Fetch an artifact's bytes into memory. Use :meth:`download_artifact_to`
        for anything large -- this holds the whole blob at once."""
        return self.transport.get_url(self.presign_download(artifact_id))

    def download_artifact_to(
        self, artifact_id: str, dest: str, *, max_bytes: int | None = None
    ) -> dict:
        """Stream an artifact's blob to ``dest`` without buffering it in memory.

        Returns ``{artifact_id, dest, size_bytes, sha256}`` -- ``sha256`` is computed
        over the bytes as they land, so the caller can check it against the
        ``content_hash`` from a listing to prove the round trip (metadata match is not
        blob existence). On a mid-stream failure the partial file is removed rather
        than left behind as a truncated blob masquerading as the artifact -- the old
        in-memory path buffered before writing, so it never wrote a partial, and this
        preserves that guarantee."""
        url = self.presign_download(artifact_id)
        ok = False
        try:
            kwargs = {"max_bytes": max_bytes} if max_bytes is not None else {}
            size, digest = self.transport.download_to(url, dest, **kwargs)
            ok = True
        finally:
            if not ok:
                Path(dest).unlink(missing_ok=True)
        return {"artifact_id": artifact_id, "dest": str(dest), "size_bytes": size, "sha256": digest}

    # -- artifact versions (an artifact's content history) ------------------
    def list_artifact_versions(self, artifact_id: str) -> list[dict]:
        """The artifact's version chain, newest first.

        An artifact is a named thing in a container; this is the chain of immutable,
        content-addressed versions behind that name. Immutability lives on the version,
        never the artifact, so renames and moves do not break a pin."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/versions")

    def create_artifact_version(
        self,
        artifact_id: str,
        *,
        from_artifact_id: str | None = None,
        uri: str | None = None,
        content_hash: str | None = None,
        size_bytes: int | None = None,
        content_type: str | None = None,
        label: str | None = None,
        meta: dict | None = None,
    ) -> dict:
        """Append the next version. Exactly one source: promote an existing artifact
        (``from_artifact_id``, zero-copy -- pins its hash + uri + size, the R2 object is
        shared, never re-uploaded) or name a pointer directly (``uri``).

        Re-sending content identical to the artifact's current live content is a no-op
        that returns the existing version, so this is safe to retry."""
        if bool(from_artifact_id) == bool(uri):
            raise ValueError("create_artifact_version needs exactly one of from_artifact_id or uri")
        model = ArtifactVersionCreate(
            from_artifact_id=from_artifact_id,
            uri=uri,
            content_hash=content_hash,
            size_bytes=size_bytes,
            content_type=content_type,
            label=label,
            meta=meta,
        )
        return self.transport.post(
            f"/v1/artifacts/{artifact_id}/versions",
            model.model_dump(mode="json", exclude_none=True),
        )

    def presign_version_download(self, artifact_id: str, version: int) -> str:
        """Presigned GET for one version's bytes -- the pin-resolution path.

        The one home for this route literal, mirroring :meth:`presign_download`, so the
        parity guard sees a single reachable call site. A force-deleted version raises
        410 WITH its deletion metadata, so a manifest can tell "deliberately destroyed"
        apart from "never existed"."""
        return self.transport.post(
            f"/v1/artifacts/{artifact_id}/versions/{version}/download", None
        )["download_url"]

    def download_artifact_version(self, artifact_id: str, version: int) -> bytes:
        """Fetch one version's bytes into memory. Use
        :meth:`download_artifact_version_to` for anything large -- this holds the whole
        blob at once."""
        return self.transport.get_url(self.presign_version_download(artifact_id, version))

    def download_artifact_version_to(self, artifact_id: str, version: int, dest: str) -> dict:
        """Stream one version's bytes to ``dest``, hashing as they land. Same partial-file
        guarantee as :meth:`download_artifact_to`: a mid-stream failure removes the file
        rather than leaving a truncated blob that looks like the artifact."""
        url = self.presign_version_download(artifact_id, version)
        ok = False
        try:
            size, digest = self.transport.download_to(url, dest)
            ok = True
        finally:
            if not ok:
                Path(dest).unlink(missing_ok=True)
        return {
            "artifact_id": artifact_id,
            "version": version,
            "dest": str(dest),
            "size_bytes": size,
            "sha256": digest,
        }

    def artifact_pin_impact(self, artifact_id: str) -> dict:
        """Which projects -- and which experiments within them -- pin this artifact's
        versions. What a delete confirmation should show a human before destroying
        something reproducible: not a count, but the work that would break."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/pin-impact")

    def delete_artifact(self, artifact_id: str) -> None:
        """Delete an artifact row."""
        self.transport.delete(f"/v1/artifacts/{artifact_id}")

    def gc_uploads(self, older_than: str) -> dict:
        """Sweep abandoned (never-confirmed) artifact uploads older than
        ``older_than``. Only ever touches pending rows; confirmed artifacts are
        untouched."""
        model = UploadGcRequest(older_than=older_than)
        return self.transport.post("/v1/artifacts/uploads/gc", model.model_dump(mode="json"))

    def check_run(self, run_id: str, *, verify: bool = False) -> dict:
        """Assess capture completeness from the bounded run bundle.

        Three verdicts, and the distinction is the point:

        * ``incomplete`` -- something is absent or provably unrecoverable.
        * ``unverified`` -- nothing is obviously absent. The default. It does NOT
          mean the run can be rebuilt.
        * ``complete`` -- earned only under ``verify=True``, either because the
          code record is self-contained (``n_git_referenced == 0``: every byte is
          on Probe, so there is nothing to resolve) or by resolving a legacy git
          reference against its remote.

        This used to answer ``complete`` for the first case's near-miss: a run
        whose code_snapshot artifact existed and pointed at a commit that lived
        nowhere. Seventeen runs read as captured for a week on the strength of a
        row being present. Counting rows is not the same as proving retrieval, so
        the cheap path no longer claims a word it has not earned.

        Runs captured since git referencing was retired cannot land in that hole
        at all -- their bytes are stored, not pointed at -- so ``verify`` on them
        costs nothing and never reports ``unresolvable_code_reference``. The
        network probe remains for the runs captured while it was live: one
        depth-1 fetch per DISTINCT (remote, commit), memoized, so auditing a
        project's runs is a few calls rather than one per run. Never called
        during a run: it cannot slow training or upload.

        ``advisories`` reports gaps that are surfaced but never flip the verdict:
        judgment calls a human makes on purpose (no ``notes``, no recorded
        ``inputs_decision``) and legacy gaps (a run captured before capture-core
        has no ``launch`` block at all; a launch block that recorded its own
        capture errors). ``missing`` remains the only input to ``state`` -- a
        launch block that EXISTS but is missing a slot (process/runtime/
        determinism) is a genuine capture failure and lands in ``missing``, not
        ``advisories``.
        """
        bundle = self.run_bundle(run_id)
        run = bundle.get("run", bundle)
        artifacts = bundle.get("artifacts", [])
        metadata = run.get("metadata") or {}
        missing: list[str] = []
        # env_ref (execution record) is the launch-capture signal (fold #7). On the
        # ingest path it is run.env_ref; on the interactive path it is metadata.env_ref.
        if not (run.get("env_ref") or metadata.get("env_ref")):
            missing.append("execution_record")
        if not any(item.get("kind") == "code_snapshot" for item in artifacts):
            missing.append("code_snapshot_artifact")
        # A reference recorded because a managed upload FAILED (fold #16 fail-open) is a
        # real capture gap: its bytes never reached R2. An INTENTIONAL path reference (a
        # shared-volume checkpoint the agent resolves locally) is NOT -- it names bytes
        # that exist, just off-platform. Distinguish by meta.upload, not uri presence:
        # both now carry a file:// uri, so the old `not uri` test would both miss the
        # failure and false-flag every intentional reference.
        failed_uploads = [
            item.get("id") or item.get("name")
            for item in artifacts
            if item.get("is_reference") and (item.get("meta") or {}).get("upload") == "failed"
        ]
        if failed_uploads:
            missing.append("portable_artifact_bytes")

        # Free: the manifest summary already rode in on the artifact's meta, so
        # this costs a dict lookup. A file classified as needing upload whose
        # bytes nobody stored is unrecoverable exactly like a dead reference --
        # and this is the failure mode per-file capture INTRODUCED, so leaving it
        # unchecked would repeat the original mistake in a new place.
        snapshot_meta: dict = next(
            ((item.get("meta") or {}) for item in artifacts if item.get("kind") == "code_snapshot"),
            {},
        )
        pending = snapshot_meta.get("n_pending_upload")
        if isinstance(pending, int) and pending > 0:
            missing.append("pending_code_bytes")

        advisories: list[str] = []
        launch = metadata.get("launch") or {}
        if not launch:
            # Pre-capture-core run: honest advisory, not a verdict flip --
            # otherwise every historical run reads incomplete and the exit-2
            # gate becomes noise during migration.
            advisories.append("launch_context")
        else:
            for slot in ("process", "runtime", "determinism"):
                if not launch.get(slot):
                    missing.append(f"launch_{slot}")
            if launch.get("errors"):
                advisories.append("launch_errors")
        n_lockfiles = snapshot_meta.get("n_lockfiles")
        if isinstance(n_lockfiles, int) and n_lockfiles == 0:
            advisories.append("no_lockfiles")
        if not any(a.get("kind") == "inputs_decision" for a in artifacts):
            advisories.append("inputs_decision")
        if not run.get("notes") and not any(a.get("kind") == "note" for a in artifacts):
            advisories.append("notes")

        verified = None
        if verify and not missing:
            from . import snapshot as _snapshot

            base_commit = snapshot_meta.get("base_commit")
            remote = snapshot_meta.get("remote")
            n_git_referenced = snapshot_meta.get("n_git_referenced")
            # Typed like `n_pending_upload` above, and for the same reasons.
            # `isinstance` rather than `== 0`, because this is server-supplied
            # JSON and Python's `False == 0` would let a malformed meta collect
            # `complete`. PRESENT rather than defaulted, because an absent key
            # is a pre-0.26.3 run that recorded no manifest at all -- unknown,
            # never zero, or the no-manifest case below collects the verdict on
            # a missing key. A test pins both.
            #
            # An OFFSITE reference (a file over the size threshold) deliberately
            # does NOT disqualify a run here. Its bytes are off-platform, so
            # this is not a claim that the run rebuilds from Probe alone -- it
            # is the same judgment `capture-run-inputs` states to agents: a
            # deliberate size reference is part of a complete capture, not a gap
            # in one. A rebuild needs that volume mounted, and `snapshot-restore`
            # reports it as OFF-PLATFORM rather than as a failure.
            self_contained = (
                isinstance(n_git_referenced, int)
                and not isinstance(n_git_referenced, bool)
                and n_git_referenced == 0
            )
            if self_contained:
                # Nothing in this manifest depends on anything but Probe for its
                # bytes, and `missing` already proved no upload is outstanding.
                # The code record is self-contained, so it is complete WITHOUT a
                # network probe -- and a stale `base_commit`, which is now
                # provenance rather than a retrieval path, must not fail a run
                # whose bytes are in R2.
                verified = True
            elif base_commit and remote:
                # A run captured while git referencing was live: some of its
                # bytes exist only on that remote, so the probe is still the
                # only thing that can tell a live reference from a dead one.
                verified = _snapshot.commit_on_remote(str(remote), str(base_commit))
                if not verified:
                    missing.append("unresolvable_code_reference")
            else:
                # Pre-0.26.3 runs recorded no manifest, so there is nothing to
                # resolve against. Absence of evidence; say so rather than
                # inventing a pass or a failure.
                verified = False

        if missing:
            state = "incomplete"
        elif verify and verified:
            state = "complete"
        else:
            state = "unverified"
        return {
            "run_id": run_id,
            "state": state,
            "missing": missing,
            "local_only_artifacts": failed_uploads,
            "verified_code_reference": verified,
            "advisories": advisories,
        }

    # -- lineage edges (fold #2) -------------------------------------------
    def add_edge(
        self,
        *,
        source_type: str,
        source_id: str,
        relation: str,
        target_type: str,
        target_id: str,
        meta: dict | None = None,
        provenance: str | None = None,
        reason: str | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST /v1/edges. Closed vocab for types
        (run/artifact/artifact_version/paper/project -- `project` is a project
        or an experiment) and relation
        (consumes/produces/evaluates_on/discovered_via/supersedes/informed_by/...);
        the generated EdgeCreate enforces it. A project end takes
        derived_from, supersedes or informed_by (-> a paper) only.

        ``provenance`` is REQUIRED on a paper edge and optional on a run or
        artifact edge, where it is stored and shown: ``observed_call`` (a tool
        was watched making it), ``human`` or ``inferred``. ``provider_citation``
        (you found the paper in a reference list) is paper-only and refused
        elsewhere; the literature fact "A's bibliography names B" is a
        ``cites`` link (:meth:`paper_citations`), not an edge.
        """
        model = EdgeCreate(
            source_type=source_type,
            source_id=source_id,
            relation=relation,
            target_type=target_type,
            target_id=target_id,
            meta=meta or {},
            provenance=provenance,
            reason=reason,
        )
        return self.write(
            "POST", "/v1/edges", model.model_dump(mode="json", exclude_none=True), strict=strict
        )

    def run_edges(self, run_id: str) -> list[dict]:
        return self.transport.get(f"/v1/runs/{run_id}/edges")

    # -- what runs READ (lineage, server 0255) -------------------------------
    def record_run_inputs(
        self,
        run_id: str,
        inputs: list[dict],
        *,
        coverage: dict | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST the files a run read (at most 2,000 per call). The read
        recorder journals these itself as non-blocking ops; this is the direct
        door for a caller holding its own list."""
        body: dict[str, Any] = {"inputs": inputs}
        if coverage is not None:
            body["coverage"] = coverage
        return self.write("POST", f"/v1/runs/{run_id}/inputs", body, strict=strict)

    def run_inputs(self, run_id: str) -> dict:
        """The files a run read, each with the run and version that wrote those
        bytes (derived by content hash), and what the recorder could see."""
        return self.transport.get(f"/v1/runs/{run_id}/inputs")

    def correct_run_input(
        self,
        run_id: str,
        path: str,
        *,
        content_hash: str | None = None,
        dismissed: bool | None = None,
        version_id: str | None = None,
        writer_run_id: str | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """Correct one read's derived match: ``dismissed=True`` drops it,
        ``version_id=`` pins the version really read, ``writer_run_id=`` pins
        the RUN that wrote it (a write that run only recorded has no version
        to pin, lineage plan 3), ``dismissed=False`` hands it back to
        automatic matching. A pin replaces the one before; ``content_hash``
        picks one read when the path was read more than once. The server
        refuses a writer that is the reader itself or that it cannot find
        (422), and one in the trash (410)."""
        if version_id is not None and writer_run_id is not None:
            raise ValueError("pin a version or a writer run, not both")
        body: dict[str, Any] = {"path": path}
        if content_hash is not None:
            body["content_hash"] = content_hash
        if dismissed is not None:
            body["dismissed"] = dismissed
        if version_id is not None:
            body["version_id"] = version_id
        if writer_run_id is not None:
            body["writer_run_id"] = writer_run_id
        return self.write("PATCH", f"/v1/runs/{run_id}/inputs", body, strict=strict)

    # -- what runs WROTE (lineage plan 3, server 0285) ------------------------
    def record_run_outputs(
        self,
        run_id: str,
        outputs: list[dict],
        *,
        coverage: dict | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST the files a run wrote (at most 2,000 per call; each row needs
        its ``observation_id``). The write recorder journals these itself as
        non-blocking ops; this is the direct door for a caller holding its
        own list."""
        body: dict[str, Any] = {"outputs": outputs}
        if coverage is not None:
            body["coverage"] = coverage
        return self.write("POST", f"/v1/runs/{run_id}/outputs", body, strict=strict)

    def run_outputs(self, run_id: str) -> dict:
        """The files a run recorded writing (path, host, hash, when first
        written and last modified), and what the recorder could see."""
        return self.transport.get(f"/v1/runs/{run_id}/outputs")

    def run_upstream(self, run_id: str, *, depth: int = 2) -> dict:
        """What a run built on, ``depth`` hops back: parents, runs it built
        on, and the writers of every file it read."""
        return self.transport.get(f"/v1/runs/{run_id}/upstream", params={"depth": depth})

    def artifact_lineage(self, artifact_id: str) -> dict:
        """Which run wrote a file (or only carried it) and which runs read it."""
        return self.transport.get(f"/v1/artifacts/{artifact_id}/lineage")

    def project_lineage(self, project_id: str, *, limit: int | None = None) -> dict:
        """A project's or experiment's OWN lineage (lineage plan 2, L12/L13/L18):
        its links in and out (stored, then "built on" derived from its runs'
        reads, ``derived: true``), its ``origin``, and its direct children as
        ``nodes``, each with an origin (at most ``limit``, 1-1000; the server's
        default 200). The graph AMONG its runs and files is
        :meth:`experiment_edges`."""
        params = {"limit": limit} if limit is not None else None
        return self.transport.get(f"/v1/projects/{project_id}/lineage", params=params)

    def artifacts_by_hash(self, content_hash: str) -> dict:
        """Every stored copy of these bytes, its writer, and its readers."""
        return self.transport.get(f"/v1/artifacts/by-hash/{content_hash}")

    def paper_edges(self, project_id: str) -> list[dict]:
        """Every discovery edge among one project's papers, in one call.

        The whole chain, not one paper's parents: reading it per paper would be
        a request per card, and the shape a reader wants is the graph anyway.
        """
        return self.transport.get(f"/v1/projects/{project_id}/paper-edges")

    def remove_edge(self, edge_id: str, *, strict: bool | None = None) -> dict | None:
        """DELETE /v1/edges/{id} — take back an edge that was wrong.

        Discovery edges are somebody's recollection of how they got somewhere,
        so being wrong is a normal outcome rather than an exceptional one, and a
        graph nobody can correct is one people stop trusting.
        """
        return self.write("DELETE", f"/v1/edges/{edge_id}", None, strict=strict)

    # -- execution records (fold #7) ---------------------------------------
    def execution_record(
        self,
        *,
        code: dict | None = None,
        deps: dict | None = None,
        hardware: dict | None = None,
        settings: dict | None = None,
        paths: dict | None = None,
    ) -> dict:
        """POST /v1/execution-records (content-addressed, idempotent). Returns
        {content_hash, ...}."""
        model = ExecutionRecordCreate(
            code=code or {},
            deps=deps or {},
            hardware=hardware or {},
            settings=settings or {},
            paths=paths or {},
        )
        return self.transport.post(
            "/v1/execution-records", model.model_dump(mode="json"), idempotent=True
        )

    def get_execution_record(self, content_hash: str) -> dict:
        return self.transport.get(f"/v1/execution-records/{content_hash}")

    # -- experiment versions (fold #6) -------------------------------------
    def experiment_version(
        self,
        experiment_id: str,
        *,
        label: str | None = None,
        as_of: str | None = None,
        exclude_run_ids: list[str] | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """POST /v1/projects/{id}/versions - mint an immutable launch-time manifest
        (a snapshot of the experiment's runs). This replaces the removed run-level
        `promote`; Probe Research rejected promotion tiers."""
        model = ExperimentVersionMint(
            label=label, as_of=as_of, exclude_run_ids=exclude_run_ids or []
        )
        return self.write(
            "POST",
            f"/v1/projects/{experiment_id}/versions",
            model.model_dump(mode="json", exclude_none=True),
            strict=strict,
        )

    def list_experiment_versions(self, experiment_id: str) -> list[dict]:
        return self.transport.get(f"/v1/projects/{experiment_id}/versions")

    def get_experiment_version(self, experiment_id: str, version: int | str) -> dict:
        return self.transport.get(f"/v1/projects/{experiment_id}/versions/{version}")

    def move_run(self, run_id: str, *, project_id: str, group_id: str | None = None) -> dict:
        """PATCH /v1/runs/{id} with a new home: file a floating run, or refile one.

        ``project_id`` is a project or an experiment (an experiment IS a project
        row); ``group_id`` must be a sweep group inside that experiment. The
        server moves the run in one transaction and re-indexes it.

        The answer must SHOW the run in its new home. A server that predates
        filing ignores `project_id` in a run PATCH and answers 200 with the run
        where it was, so a move that did nothing would read as done; that is
        refused (``CapabilityUnavailable``), as the unfiled listing is.

        A run moved into an EXPERIMENT answers with the experiment in
        ``experiment_id`` and its parent (the run's home project) in
        ``project_id`` (0238): either field naming the wanted id is the move."""
        body: dict = {"project_id": project_id}
        if group_id is not None:
            body["group_id"] = group_id
        row = self.transport.patch(f"/v1/runs/{run_id}", body)
        row = row if isinstance(row, dict) else {}
        landed = _same_id(row.get("project_id"), project_id) or _same_id(row.get("experiment_id"), project_id)
        if not landed or (group_id is not None and not _same_id(row.get("group_id"), group_id)):
            raise errors.CapabilityUnavailable(
                "run_filing",
                "this server cannot file runs yet: it answered the move with the run where it was. "
                "Upgrade the backend before filing runs.",
            )
        return row

    def list_runs(
        self,
        *,
        experiment_id: str | None = None,
        project_id: str | None = None,
        direct: bool = False,
        tags: list[str] | None = None,
        unfiled: bool = False,
        **params,
    ) -> Page:
        """``project_id`` returns ALL the project's runs — project-direct AND
        experiment-attached (0054); ``direct=True`` narrows to experiment-less
        runs only; ``unfiled=True`` lists FLOATING runs, filed nowhere yet (the
        caller's own; every one for an admin)."""
        query = dict(params)
        if experiment_id is not None:
            query["experiment_id"] = experiment_id
        if project_id is not None:
            query["project_id"] = project_id
        if direct:
            query["direct"] = "true"
        if unfiled:
            query["unfiled"] = "true"
        tags = canonical_tags(tags) if tags else None
        if tags:
            query["tags"] = tags
        page = self.transport.get_page("/v1/runs", params=query or None)
        if tags and page.items:
            # Same refuse-rather-than-mislabel contract as the 0054 guard below.
            self._verify_tags_filter(tags, page.items, "GET /v1/runs")
        # A pre-0054 backend IGNORES unknown query params and returns the
        # unscoped list — a confident wrong answer presented as project-scoped.
        # Its rows also predate the project_id field, which is how we can tell:
        # refuse rather than mislabel. (An empty page proves nothing and passes.)
        if (project_id is not None or direct) and page.items and "project_id" not in page.items[0]:
            raise errors.NotFoundError(
                "this research-os backend predates GET /v1/runs?project_id= "
                "(0054): it ignored the filter and returned unscoped runs. "
                "Upgrade the backend before relying on project-scoped listings."
            )
        # Same refusal for floating runs: a backend that predates them drops
        # `unfiled`, and its answer is a page of FILED runs. Any row with a home
        # (or with no project_id key at all) proves the filter was not applied.
        if unfiled and any(
            not isinstance(row, dict) or row.get("project_id") is not None or "project_id" not in row
            for row in page.items
        ):
            raise errors.CapabilityUnavailable(
                "floating_runs",
                "this research-os backend predates floating runs: it ignored "
                "GET /v1/runs?unfiled=true and returned filed runs.",
            )
        return page

    def unfiled_runs(self, *, limit: int = 200) -> dict:
        """How many floating runs wait to be filed, and how old the oldest is.

        ``{"count": n, "more": bool, "oldest_created_at": iso | None,
        "oldest_age_s": float | None}``; ``more`` means the count stopped at
        ``limit``. Raises CapabilityUnavailable on a backend that ignores the
        filter, so a caller can say "unknown" instead of a wrong number."""
        page = self.list_runs(unfiled=True, limit=limit)
        items = [row for row in page.items or [] if isinstance(row, dict)]
        stamps = sorted(str(row["created_at"]) for row in items if row.get("created_at"))
        oldest = stamps[0] if stamps else None
        age: float | None = None
        if oldest:
            try:
                from datetime import datetime, timezone

                born = datetime.fromisoformat(oldest.replace("Z", "+00:00"))
                if born.tzinfo is None:
                    born = born.replace(tzinfo=timezone.utc)
                age = max(0.0, (datetime.now(timezone.utc) - born).total_seconds())
            except ValueError:
                age = None
        return {
            "count": len(items),
            "more": bool(page.next_cursor),
            "oldest_created_at": oldest,
            "oldest_age_s": age,
        }

    def list_run_artifacts(
        self,
        run_id: str,
        *,
        kind: str | None = None,
        step_from: int | None = None,
        step_to: int | None = None,
        name: str | None = None,
        scope: str | None = None,
    ) -> list[dict]:
        """List a run's artifacts, optionally server-filtered by kind and/or an
        inclusive step window — e.g. sandbox states around a collapse:
        ``list_run_artifacts(run_id, kind="sandbox_state", step_from=599, step_to=601)``.

        ``scope`` controls inheritance (default ``own`` = this run only): ``all`` also
        returns the run's experiment- and project-level artifacts, ``inherited`` only
        those parent levels. On a non-``own`` scope each row carries ``source_level`` and
        rows are ordered nearest-wins, so a ``name`` lookup resolves to the closest level."""
        params = {
            key: value
            for key, value in {
                "kind": kind,
                "step_from": step_from,
                "step_to": step_to,
                "name": name,
                "scope": scope,
            }.items()
            if value is not None
        }
        return read_artifact_rows(
            lambda query: self.transport.request(
                "GET", f"/v1/runs/{run_id}/artifacts", params=query, idempotent=True
            ),
            params,
        )

    def move_artifact(self, artifact_id: str, *, level: str, target_id: str | None = None) -> dict:
        """Move an artifact vertically along its own run->experiment->project chain.

        Promote up (``level`` above the artifact's current anchor) derives the target
        from its chain; demote down needs a ``target_id`` that sits inside the current
        subtree. A file (workspace/shared) or a lateral target is a 422; an identical
        artifact already at the destination is a 409. The artifact keeps its id."""
        body: dict = {"level": level}
        if target_id is not None:
            body["target_id"] = target_id
        return self.transport.post(f"/v1/artifacts/{artifact_id}/move", body)

    def list_experiment_artifacts(self, experiment_id: str) -> list[dict]:
        return self.transport.get(f"/v1/projects/{experiment_id}/artifacts")

    # --- project code sources (0134) ----------------------------------------
    #
    # The commit timeline is read THROUGH GitHub by the backend (ETag cache,
    # honest ok/stale/unavailable states) — these methods proxy the read; no
    # history is mirrored anywhere.

    # -- project references (0153) -------------------------------------------
    #
    # LATERAL edges, not containment. `parent_project_id` says "this is part
    # of that"; a reference says "this drew on that" — the relation a review
    # feeding a training run actually has. Cycles are legal, depth is
    # unbounded, and none of the subtree machinery applies.

    def add_project_reference(self, project_id: str, to_project_id: str) -> None:
        """Record that ``project_id`` REFERENCES ``to_project_id``.

        Idempotent, and DIRECTED: A->B and B->A are different statements, and
        adding one does not add the other.
        """
        self.transport.post(
            f"/v1/projects/{project_id}/references",
            {"to_project_id": to_project_id},
        )

    def remove_project_reference(self, project_id: str, to_project_id: str) -> None:
        """Drop one directed edge; the opposite direction is untouched."""
        self.transport.delete(f"/v1/projects/{project_id}/references/{to_project_id}")

    # -- papers (0152) -------------------------------------------------------
    #
    # The literature a `research` project was built from. Project-anchored and
    # only project-anchored; an experiment-level anchor stays unbuilt until a
    # surface asks for one. NO DEDUPE: two adds of one ``source_url`` make two
    # rows, because the server cannot decide what identity means for a paper
    # with an arXiv URL, a DOI landing page, or a caller-local path.

    def add_paper(
        self,
        project_id: str,
        *,
        title: str,
        source_url: str,
        authors: str | None = None,
        repo_url: str | None = None,
        summary_md: str | None = None,
        discrepancies_md: str | None = None,
        tags: list[str] | None = None,
        lineage: dict | None = None,
    ) -> dict:
        """Record one paper against a project.

        ``tags`` are the CONCEPTS this paper is about in your own vocabulary --
        the same reader-authored list projects, experiments and runs carry, and
        the axis a forty-paper review is grouped on. They are not the
        provider's ``extracted_categories``: those are arXiv's taxonomy and the
        server owns them.

        ``title`` remains reviewer-authored. ``source_url`` is required and may
        be an HTTP(S) URL or a path on the recording client's machine.
        Provider extraction is stored separately and never rewrites the title
        or summary. ``discrepancies_md`` is what nothing else captures: what
        the released repo does that the paper does not say. Adding counts as
        activity on the project; editing and removing deliberately do not.

        ``lineage`` records HOW YOU GOT TO THIS PAPER, and it mirrors the wire
        shape exactly rather than flattening into keyword arguments, because the
        distinction that matters cannot survive being flattened::

            lineage=None                       nobody asked -> stays UNKNOWN
            lineage={"via": None}              you looked, there was no parent
            lineage={"via": "<paper id>",      you followed that paper to this one
                     "provenance": "observed_call",
                     "reason": "its references"}

        Passing nothing and passing ``{"via": None}`` are DIFFERENT answers. In
        Python they would collapse into the same ``via=None`` argument, which is
        the whole reason this is one parameter and not three.

        ``provenance`` is required whenever ``via`` names a paper, and has no
        default anywhere in the stack: a provenance the client picked would be a
        claim nobody made. Use ``observed_call`` when a tool call handed you the
        parent (``find_papers(mode="similar", expand="references")`` already knew
        it), ``provider_citation`` when you found it in a reference list,
        ``human`` when a person said so, ``inferred`` when a model concluded it
        after the fact. Every one of them records YOUR path through the
        literature; whether one paper's bibliography names another is a
        ``cites`` link the server reads on its own (:meth:`paper_citations`,
        :meth:`citation_graph`), never something this edge asserts.

        Answer at ADD TIME. Two turns later this is a guess.
        """
        body = {
            key: value
            for key, value in {
                "authors": authors,
                "repo_url": repo_url,
                "summary_md": summary_md,
                "discrepancies_md": discrepancies_md,
                "tags": tags,
                # `is not None` on the OBJECT, never on `via` inside it -- the
                # presence of the object is what says "I looked".
                "lineage": lineage,
            }.items()
            if value is not None
        }
        body["title"] = title
        body["source_url"] = source_url
        row = self.transport.post(f"/v1/projects/{project_id}/papers", body)
        if tags is not None:
            # A pre-0176 backend drops `tags` from the body and answers 201 with
            # an untagged paper -- the 0066 write failure, one entity later.
            self._verify_tags_written(tags, row, "POST /v1/projects/{id}/papers")
        return row

    def list_papers(
        self,
        project_id: str,
        *,
        cursor: str | None = None,
        limit: int | None = None,
        tags: list[str] | None = None,
    ):
        """One project's papers, newest first. Returns a cursor ``Page``.

        ``tags`` narrows by CONTAINMENT: a paper must carry every tag named, not
        any of them — the same AND semantics the project, experiment and run
        listings use, so one mental model covers all four.
        """
        query: dict = {}
        if cursor is not None:
            query["cursor"] = cursor
        if limit is not None:
            query["limit"] = limit
        tags = canonical_tags(tags) if tags else None
        if tags:
            query["tags"] = tags
        page = self.transport.get_page(f"/v1/projects/{project_id}/papers", params=query or None)
        if tags and page.items:
            # A pre-0176 backend IGNORES the filter and returns every paper in
            # the project, which the caller would then read as "these are the
            # retrieval ones". Refuse rather than mislabel.
            self._verify_tags_filter(tags, page.items, "GET /v1/projects/{id}/papers")
        return page

    def get_paper(self, paper_id: str) -> dict:
        return self.transport.get(f"/v1/papers/{paper_id}")

    def update_paper(
        self,
        paper_id: str,
        *,
        title: str | None = None,
        authors: str | None = None,
        source_url: str | None = None,
        repo_url: str | None = None,
        summary_md: str | None = None,
        discrepancies_md: str | None = None,
        tags: list[str] | None = None,
    ) -> dict:
        """Field-replace: an omitted field is untouched, ``""`` clears it —
        except ``title`` and ``source_url``, which are required and cannot be
        emptied (an empty replacement is a 422).

        ``tags`` replaces the WHOLE list (``[]`` clears it), which is the tag
        contract on every entity. To add or drop one tag without knowing the
        rest, read the paper first — that read-modify-write is what the CLI's
        ``probe paper tag`` verb does."""
        body = {
            key: value
            for key, value in {
                "title": title,
                "authors": authors,
                "source_url": source_url,
                "repo_url": repo_url,
                "summary_md": summary_md,
                "discrepancies_md": discrepancies_md,
                "tags": tags,
            }.items()
            if value is not None
        }
        row = self.transport.patch(f"/v1/papers/{paper_id}", body)
        if tags is not None:
            self._verify_tags_written(tags, row, "PATCH /v1/papers/{id}")
        return row

    def remove_paper(self, paper_id: str) -> None:
        self.transport.delete(f"/v1/papers/{paper_id}")

    # -- citation links (citation graph, Track C) --------------------------
    #
    # `cites` is a fact about the LITERATURE: "paper A's reference list names
    # work B", proven only by an id printed in the bibliography entry or
    # deposited by the publisher -- never a title match or a provider's guess.
    # It is not `discovered_via` (`add_paper(lineage=...)`), which records YOUR
    # path through the literature. The server reads both views from its own
    # tables; nothing here calls a provider. A team the server has not switched
    # on reads `state: "disabled"` with no nodes or links.

    def citation_graph(
        self,
        project_id: str,
        *,
        suggested: int | None = None,
        directions: Iterable[str] | str | None = None,
        min_links: int | None = None,
        include_discovery: bool | None = None,
        include_unresolved: bool | None = None,
    ) -> dict:
        """GET /v1/projects/{id}/citation-graph -- the project's papers, the
        works they cite or are cited by, and the ``cites`` edges among them.

        Returns the ``CitationGraphOut`` shape (``probe.models``): ``state``
        (``ok`` | ``partial`` | ``pending``; only a server older than the
        citation flag's removal also answers ``disabled``), ``nodes`` (each
        ``primary`` is one of the project's papers with its fetch status;
        each ``suggested`` is a work the papers link to that the project has
        not recorded), ``edges`` (``cites``, each with the bibliography entries
        that prove it) and ``completeness`` (what was cut, counted).

        Every argument left ``None`` takes the server's default:
        ``suggested`` -- how many suggested works to return, ranked by how many
        of THIS project's papers link to each (50, max 200, 0 for none; never
        padded). ``directions`` -- ``reference`` (what the papers cite),
        ``citer`` (who cites them), or both (default). ``min_links`` -- a
        suggested work needs at least this many linking papers (1).
        ``include_discovery`` -- also return the ``discovered_via`` edges
        among the papers, verbatim and never relabelled ``cites`` (False).
        ``include_unresolved`` -- also return each paper's bibliography entries
        that printed no id (False).
        """
        params: dict[str, Any] = {}
        if suggested is not None:
            params["suggested"] = suggested
        if directions is not None:
            chosen = directions.split(",") if isinstance(directions, str) else list(directions)
            params["directions"] = ",".join(
                _citation_direction(d) for d in chosen if str(d).strip()
            )
        if min_links is not None:
            params["min_links"] = min_links
        if include_discovery is not None:
            params["include_discovery"] = include_discovery
        if include_unresolved is not None:
            params["include_unresolved"] = include_unresolved
        return self.transport.get(
            f"/v1/projects/{project_id}/citation-graph", params=params or None
        )

    def paper_citations(
        self,
        paper_id: str,
        *,
        direction: str | None = None,
        include_unresolved: bool | None = None,
        limit: int | None = None,
    ) -> dict:
        """GET /v1/papers/{id}/citations -- every citation link row of one
        paper with its proof, and how each fetch ended.

        Returns the ``PaperCitationsOut`` shape (``probe.models``): ``state``,
        ``keys`` (the paper's own ids the rows were read for), ``sync`` (the
        per-direction status and counts), ``reference_lists`` (one entry per
        bibliography read: source, owner key, exact url, status, counts),
        ``links`` and ``truncated``. Each link names the bibliography that
        proves it (``list_source``, ``list_owner_key``, ``list_url``,
        ``ordinal``) and HOW (``resolution``: ``printed_id`` in the entry,
        ``publisher_id`` deposited by the publisher, or ``unresolved`` -- an
        entry with no id, kept as text and never an edge).

        ``direction`` -- ``reference`` or ``citer``; both when ``None``.
        ``include_unresolved`` -- the server default is True here: this is the
        view that explains why a reference did not become an edge.
        ``limit`` -- at most this many rows (server default 500, max 2000).
        """
        params: dict[str, Any] = {}
        if direction is not None:
            params["direction"] = _citation_direction(direction)
        if include_unresolved is not None:
            params["include_unresolved"] = include_unresolved
        if limit is not None:
            params["limit"] = limit
        return self.transport.get(f"/v1/papers/{paper_id}/citations", params=params or None)

    def refresh_paper_citations(self, paper_id: str) -> dict:
        """POST /v1/papers/{id}/citations/refresh -- re-read this paper's
        bibliographies and re-nominate its citers now. Answers 202
        (``{"status": "queued"}``); the job runs on the server.

        Needs write access to the paper's project. Refused, never queued:
        429 (``RosError`` with ``status == 429`` and ``retry_after`` set) while
        a refresh for the paper is already queued or within an hour of its
        last fetch -- the lists are third-party documents and asking twice
        cannot make them newer; 409 (``ConflictError``) with ``detail.code ==
        "generation_paused"`` when the team's page generation is paused (only
        a server older than the citation flag's removal also answers 409
        ``citations_disabled``). A plain non-idempotent POST: an
        answer from the server (a 429 included) is never retried, and nothing
        is queued offline -- a refresh is a request to act now. Only a connect
        failure that never reached the server is retried, as for every request.
        """
        return self.transport.post(f"/v1/papers/{paper_id}/citations/refresh")

    def list_project_code_sources(self, project_id: str) -> list[dict]:
        """The project's attached repositories (repo/branch/directory rows)."""
        return self.transport.get(f"/v1/projects/{project_id}/code-sources")

    def attach_project_code_source(
        self,
        project_id: str,
        *,
        repo: str,
        ref: str | None = None,
        path_prefix: str = "",
        start_sha: str | None = None,
        start_at: str | None = None,
        add_readme_embed: bool = False,
        via: str = "cli",
        reason: str | None = None,
    ) -> dict:
        """Attach a GitHub repository (and branch) to a project.

        Grants no access an installation (or public visibility) has not already
        granted; the backend resolves the repo through the covering
        installation's token or unauthenticated for public repos. ``via`` is
        attribution ('cli' from scripts, 'agent' from an agent acting alone —
        which then REQUIRES ``reason``, rendered next to the attribution)."""
        body = {
            key: value
            for key, value in {
                "repo": repo,
                "ref": ref,
                "path_prefix": path_prefix,
                "start_sha": start_sha,
                "start_at": start_at,
                "add_readme_embed": add_readme_embed,
                "via": via,
                "reason": reason,
            }.items()
            if value not in (None, "", False)
        }
        body["repo"] = repo
        return self.transport.post(f"/v1/projects/{project_id}/code-sources", body)

    def detach_project_code_source(self, project_id: str, source_id: str) -> None:
        self.transport.delete(f"/v1/projects/{project_id}/code-sources/{source_id}")

    def confirm_project_code_source(self, project_id: str, source_id: str) -> dict:
        """suggested -> active (the one-click yes to a snapshot's suggestion)."""
        return self.transport.post(
            f"/v1/projects/{project_id}/code-sources/{source_id}/confirm", {}
        )

    def patch_project_code_source(
        self,
        project_id: str,
        source_id: str,
        *,
        ref: str | None = None,
        path_prefix: str | None = None,
        start_sha: str | None = None,
        start_at: str | None = None,
    ) -> dict:
        """Edit a source's branch/directory/start bound (the backend re-resolves)."""
        body = {
            key: value
            for key, value in {
                "ref": ref,
                "path_prefix": path_prefix,
                "start_sha": start_sha,
                "start_at": start_at,
            }.items()
            if value is not None
        }
        return self.transport.patch(f"/v1/projects/{project_id}/code-sources/{source_id}", body)

    def sync_project_code_source(self, project_id: str, source_id: str) -> dict:
        """Re-check the branch tip now (heals a `missing` source when it is back)."""
        return self.transport.post(f"/v1/projects/{project_id}/code-sources/{source_id}/sync", {})

    def mark_project_commit(
        self, project_id: str, sha: str, *, excluded: bool, source_id: str | None = None
    ) -> None:
        """Exclude a commit from the timeline (or bring it back). A display
        verdict, never history editing — include_excluded still lists it."""
        body: dict[str, object] = {"excluded": excluded}
        if source_id:
            body["source_id"] = source_id
        self.transport.post(f"/v1/projects/{project_id}/commits/{sha}/mark", body)

    # --- W&B account selection and project-owned history --------------------

    def create_wandb_account(self, *, api_key: str) -> dict:
        """Connect W&B credentials without creating a workspace or source binding.

        Uses the W&B-specific account contract; credentials never enter the
        durable write queue, including when the server is unavailable.
        """
        # Account credentials are intentional authentication input, not captured
        # research data: bypass its redactor as well as its fail-open journal.
        return self.transport.post(
            "/v1/integrations/wandb/accounts", {"credentials": {"api_key": api_key}}
        )

    def reconnect_wandb_account(self, connection_id: str, *, api_key: str) -> dict:
        """Replace credentials on the same account, retaining its source identity."""
        return self.transport.post(
            f"/v1/integrations/wandb/accounts/{connection_id}/reconnect",
            {"credentials": {"api_key": api_key}},
        )

    def rename_wandb_account(self, connection_id: str, *, name: str) -> dict:
        """Rename a saved account.

        Allowed on a DISCONNECTED one too -- that is the row whose name is
        doing the most work, its key being gone.
        """
        return self.transport.patch(
            f"/v1/integrations/wandb/accounts/{connection_id}", {"name": name}
        )

    def disconnect_wandb_account(self, connection_id: str) -> None:
        """Disconnect credentials while retaining imported records and attachments."""
        self.transport.delete(f"/v1/integrations/wandb/accounts/{connection_id}")

    def list_mirror_connections(self) -> list[dict]:
        """Connected accounts; credentials are managed in Integrations."""
        return self.transport.get("/v1/integrations/mirror/connections")

    def list_mirror_scope_options(self, connection_id: str) -> list[dict]:
        return self.transport.get(
            f"/v1/integrations/mirror/connections/{connection_id}/scope-options"
        )

    def list_project_wandb_sources(self, project_id: str) -> list[dict]:
        return self.transport.get(f"/v1/projects/{project_id}/wandb-sources")

    def attach_project_wandb_source(
        self, project_id: str, *, connection_id: str, external_id: str
    ) -> dict:
        """Reuse the canonical source attachment; new attachments start paused.

        Strict writes never enter the generic outbox. Callers retaining an
        admission intent must receive either the actual receipt or an error.
        """
        return self.write(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources",
            {"connection_id": connection_id, "external_id": external_id},
            strict=True,
        )

    def patch_project_wandb_source(
        self, project_id: str, attachment_id: str, *, sync_enabled: bool, expected_revision: int
    ) -> dict:
        return self.write(
            "PATCH",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}",
            {"sync_enabled": sync_enabled, "expected_revision": expected_revision},
            strict=True,
        )

    def detach_project_wandb_source(self, project_id: str, attachment_id: str) -> None:
        self.write(
            "DELETE", f"/v1/projects/{project_id}/wandb-sources/{attachment_id}", strict=True
        )

    def list_experiment_wandb_sources(self, experiment_id: str) -> list[dict]:
        return self.transport.get(f"/v1/projects/{experiment_id}/wandb-sources")

    def attach_experiment_wandb_source(
        self, experiment_id: str, *, connection_id: str, external_id: str
    ) -> dict:
        """Reuse the canonical source attachment; new attachments start paused.

        Strict writes never enter the generic outbox. Callers retaining an
        admission intent must receive either the actual receipt or an error.
        """
        return self.write(
            "POST",
            f"/v1/projects/{experiment_id}/wandb-sources",
            {"connection_id": connection_id, "external_id": external_id},
            strict=True,
        )

    def patch_experiment_wandb_source(
        self, experiment_id: str, attachment_id: str, *, sync_enabled: bool, expected_revision: int
    ) -> dict:
        return self.write(
            "PATCH",
            f"/v1/projects/{experiment_id}/wandb-sources/{attachment_id}",
            {"sync_enabled": sync_enabled, "expected_revision": expected_revision},
            strict=True,
        )

    def detach_experiment_wandb_source(self, experiment_id: str, attachment_id: str) -> None:
        self.write(
            "DELETE",
            f"/v1/projects/{experiment_id}/wandb-sources/{attachment_id}",
            strict=True,
        )

    def launch_project_wandb_backfill(
        self, project_id: str, attachment_id: str, *, idempotency_key: str
    ) -> dict:
        return self.write(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills",
            {"idempotency_key": idempotency_key},
            strict=True,
        )

    def list_project_wandb_backfills(
        self, project_id: str, attachment_id: str, *, cursor: str | None = None, limit: int = 25
    ) -> dict:
        return self.transport.get(
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills",
            params={"limit": limit, **({"cursor": cursor} if cursor else {})},
        )

    def get_project_wandb_backfill(self, project_id: str, attachment_id: str, job_id: str) -> dict:
        return self.transport.get(
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills/{job_id}"
        )

    def cancel_project_wandb_backfill(
        self, project_id: str, attachment_id: str, job_id: str
    ) -> dict:
        return self.write(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills/{job_id}/cancel",
            {},
            strict=True,
        )

    def retry_project_wandb_backfill(
        self, project_id: str, attachment_id: str, job_id: str, *, idempotency_key: str
    ) -> dict:
        return self.write(
            "POST",
            f"/v1/projects/{project_id}/wandb-sources/{attachment_id}/backfills/{job_id}/retry",
            {"idempotency_key": idempotency_key},
            strict=True,
        )

    def list_project_pulls(self, project_id: str, **filters: object) -> dict:
        """One page of pull requests targeting the attached branch (proxied)."""
        params = {key: value for key, value in filters.items() if value is not None}
        return self.transport.get(f"/v1/projects/{project_id}/pulls", params=params)

    def list_project_releases(self, project_id: str, **filters: object) -> dict:
        """The repository's releases (proxied; headers only)."""
        params = {key: value for key, value in filters.items() if value is not None}
        return self.transport.get(f"/v1/projects/{project_id}/releases", params=params)

    def list_project_commits(self, project_id: str, **filters: object) -> dict:
        """One page of the proxied commit timeline: ``{state, source, items,
        cursor}``. ``state`` is honest — 'stale' is real data with degraded
        freshness, 'unavailable' means GitHub could not answer, never an empty
        history."""
        params = {key: value for key, value in filters.items() if value is not None}
        return self.transport.get(f"/v1/projects/{project_id}/commits", params=params)

    def get_project_commit(self, project_id: str, sha: str, source_id: str | None = None) -> dict:
        """One commit in full (message body, files, stats, linked runs)."""
        params = {"source_id": source_id} if source_id else None
        return self.transport.get(f"/v1/projects/{project_id}/commits/{sha}", params=params)

    def get_run_code(self, run_id: str) -> dict:
        """The run panel's answer: the commit the run's snapshot was BASED ON
        (nearest pushed ancestor — provenance, never the exact tree)."""
        return self.transport.get(f"/v1/runs/{run_id}/code")

    def compare_run_code(self, run_id: str, to: str) -> dict:
        """What changed in code between two runs (integrations-v2 phase 6).

        ``base`` in the answer is the OLDER run whichever way this call named
        them (``swapped`` says when they were reordered); ``commits`` reads
        oldest-first from STORED link rows only — mismatched repos come back
        as a named ``state``, never an error."""
        return self.transport.get(f"/v1/runs/{run_id}/code/compare", params={"to": to})

    def get_experiment_code(self, experiment_id: str) -> dict:
        """What changed in the repo between an experiment's runs: the
        project's sources (inherited — there is no experiment-level attach),
        each run's stored ``owner/repo@sha``, and the per-repo commit window.
        Stored rows only; the backend never asks GitHub on this read."""
        return self.transport.get(f"/v1/projects/{experiment_id}/code")

    def list_project_artifacts(self, project_id: str) -> list[dict]:
        """Project-wide shared data (fold #22) — the sibling of the experiment read.

        Written as its own literal call site rather than routed through
        :meth:`list_anchored`, for the same reason every anchored route above is:
        the contract-parity guard resolves paths from the AST."""
        return self.transport.get(f"/v1/projects/{project_id}/artifacts")

    # -- the project's notes file ------------------------------------------
    # One markdown document per project that agents read and write. Deliberately NOT
    # a schema: an earlier attempt gave notes a kind vocabulary
    # (intent/decision/observation/...), supersession and an authority field, and
    # nothing server-side validated, aggregated or grouped by any of it -- eight
    # kinds bought one list filter. Prose is what people actually write.
    #
    # It is a COLUMN on the project (research-os 0094), not an artifact. The artifact
    # version was the first implementation and it was wrong twice over: artifact
    # identity is anchor+name+content_hash, so every edit appended a new row and a
    # project's artifact list filled with copies of one file; and reading a paragraph
    # cost three round trips (list -> presign -> R2 GET). The column rides along on
    # the project row, so an orienting caller gets the notes with NO extra request.

    def get_project_notes(self, project_id: str) -> str | None:
        """The project's notes, or None when nobody has written any.

        Note that `GET /v1/projects/{id}` already returns this, so a caller that
        holds the project row should read `row["notes"]` rather than call here --
        the point of the column is that the text costs no second request."""
        return self.get_project(project_id).get("notes")

    def _set_project_notes(self, project_id: str, text: str) -> str:
        """Replace the project's notes and return what the server actually stored.

        The read-back is not belt-and-braces. `ProjectPatch` does not forbid extra
        fields, so a backend PREDATING 0094 accepts `notes`, ignores it, and answers
        200 -- the write vanishes and the caller is told it succeeded. Returning the
        stored value makes that detectable instead of silent."""
        # sync=True: the read-back below is the only thing that catches a
        # backend which accepts the field, ignores it and answers 200. A
        # queued write skips that check entirely, so under async the guard
        # would never run. These are one-shot metadata writes, not loop
        # traffic, so paying the round trip costs nothing that matters.
        queued = self.write(
            "PATCH",
            f"/v1/projects/{project_id}",
            # force: this door replaces a whole document with no version in hand
            # (`probe notes write <file>`), and the server now REFUSES an
            # unguarded replace. Saying it explicitly is the honest spelling of
            # what this verb has always done; `probe notes checkout`/`push` is
            # the door that actually merges.
            {"notes": text, "force": True},
            sync=True,
            raise_permanent=True,
        )
        from .redaction import default_scrub

        expected = default_scrub(text)
        if queued is None:
            # Journaled (async mode) or fail-open-spooled: nothing reached the server,
            # so there is nothing to read back. Verifying here would report a failure
            # for a write that is simply still in the outbox.
            return expected
        stored = self.get_project(project_id).get("notes")
        if stored != expected:
            raise errors.RosError(
                "the server did not store the notes: this backend predates the "
                "projects.notes column (research-os 0094) and silently ignored the "
                "field. Upgrade the backend."
            )
        return stored

    def query_sql(
        self,
        *,
        sql: str | None = None,
        tables: list[str] | None = None,
        max_rows: int | None = None,
    ) -> dict:
        """``POST /v1/sql``: schema discovery (omit ``sql``) or one read-only SELECT.

        The server enforces the caller's tenant and visibility, a closed set of
        tables, functions and constructs, a 5s statement timeout and a result
        budget. ``tables`` is discovery only: full columns for just those.
        """
        body: dict[str, Any] = {}
        if sql is not None:
            body["sql"] = sql
        if tables is not None:
            body["tables"] = tables
        if max_rows is not None:
            body["max_rows"] = max_rows
        return self.transport.post("/v1/sql", body)

    # -- captured coding-agent sessions ---------------------------------------

    def session_work(self, session_id: str, *, limit: int | None = None) -> dict:
        """``GET /v1/sessions/{id}/work`` — everything one captured session
        touched, grouped by entity type.

        An unknown well-formed id answers EMPTY rather than 404 (the route is
        deliberately not an oracle for another product's ids), so absence of
        work is not proof the session never existed -- the transcript read is
        the existence check.
        """
        params = {"limit": limit} if limit is not None else None
        return self.transport.get(f"/v1/sessions/{session_id}/work", params=params)

    def session_created(self, session_id: str) -> dict:
        """``GET /v1/sessions/{id}/created`` — the ids of every project,
        experiment and run that session CREATED (research-os 0291), not merely
        touched: ``{session_id, project_ids, run_ids, truncated}``. An unknown
        well-formed id answers empty, as ``session_work`` does."""
        return self.transport.get(f"/v1/sessions/{session_id}/created")

    def session_transcript(self, session_id: str, *, source: str = "claude_code") -> dict:
        """``GET /v1/sessions/{id}/transcript`` — the complete normalized
        transcript captured for one session.

        ``source`` names the agent that recorded it (``claude_code`` /
        ``codex``) and is part of the document's identity, not a filter: the
        same id under the wrong source 404s. The content is the normalized,
        secret-gated document the engine indexed, not the agent's raw local
        JSONL -- the capture pipeline strips bookkeeping payloads first.
        """
        return self.transport.get(
            f"/v1/sessions/{session_id}/transcript", params={"source": source}
        )

    #: NO "trial". `PATCH /v1/trials/{id}` accepts the same notes writes and this
    #: client deliberately never sends them -- see `_NOTE_TARGETS` in the CLI for
    #: the reasoning. `update_trial` reaches that route for title and description,
    #: so the parity check still covers it.
    NOTES_ENTITIES = ("project", "experiment", "run", "group", "artifact")

    def _write_notes(
        self, entity: str, entity_id: str, body: dict, *, strict: bool = False, sync: bool = False
    ) -> dict | None:
        """`strict=True` for an EDIT, and it is not a preference.

        The default write path is fail-open: a failed request is journaled and
        the drainer replays it. It is wrong for an edit, whose characteristic
        failure is a 409 saying `old_text` matched zero times or twice -- a
        permanent refusal the caller was told about. Journaling it would replay
        the refusal forever, or worse, land it later against a document where
        the text has since become unique, applying an edit the caller believes
        was rejected.

        An APPEND is fail-open but never queues a refusal, which is what
        `raise_permanent` means here. This used to say an append "fails only
        transiently" and that was false: a document at MAX_DOCUMENT_NOTES
        refuses every further append with a 422 naming the cap, permanently. The
        SDK swallowed it, the CLI printed "appended to <kind> notes" and exited
        0, and the paragraph went to the outbox to be dead-lettered -- so an
        agent kept appending to a document that had stopped accepting anything,
        one silent success at a time, and read its own dead letters afterwards
        as a broken outbox. A network blip still queues, which is the case the
        fail-open path was built for.

        RETURNS the PATCH response so the caller can read the headroom the server
        published on it, or None when the write was journaled rather than sent --
        the same None ``Client.write`` already returns, meaning "no server has
        seen this yet", never "the document is fine".
        """
        # Every notes door, not just the append: `strict` already covers the
        # edit, and a PATCH the server refuses outright is never worth queueing
        # whichever field carried it.
        #
        # Spelled out per entity rather than through a {entity: segment} map, and
        # test_parity is why: it reads these call sites STATICALLY to prove every
        # path the client calls is one the backend declares. A computed path is
        # invisible to that check, which would take five real routes out of its
        # coverage and hand it one phantom `/v1/{route}` instead.
        # `sync` is SEPARATE from `strict` and not implied by it: strict decides
        # whether a refusal is journaled, sync decides whether the request is
        # made at all. A replace needs both -- under `async_writes` a journaled
        # replace drains later against a `base_version` that has since moved and
        # dead-letters, after the caller was told it shipped.
        kw = {"strict": strict, "raise_permanent": True, "sync": sync}
        if entity == "project":
            return self.write("PATCH", f"/v1/projects/{entity_id}", body, **kw)
        if entity == "experiment":
            return self.write("PATCH", f"/v1/projects/{entity_id}", body, **kw)
        if entity == "run":
            return self.write("PATCH", f"/v1/runs/{entity_id}", body, **kw)
        if entity == "group":
            return self.write("PATCH", f"/v1/groups/{entity_id}", body, **kw)
        if entity == "artifact":
            return self.write("PATCH", f"/v1/artifacts/{entity_id}", body, **kw)
        raise errors.RosError(
            f"{entity!r} carries no notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def _replace_notes(
        self,
        entity: str,
        entity_id: str,
        text: str,
        *,
        base_version: int | None,
        op_key: str,
    ) -> dict | None:
        """Replace an entity's whole note, pinned to the version it was read at.

        THE FILE-MODEL WRITE. `base_version` is the `notes_version` the document
        was checked out at; the server refuses with a 409 carrying the current
        version and NO body when the head has moved, and the caller re-reads
        through the READ door to merge. `None` is `--force`: replace whatever is
        there. `op_key` identifies a retry after a lost response as a replay --
        the server does not act on it yet (TODOS.md), so it is not yet a
        guarantee against a duplicate.

        strict=True, and not as a preference: a 409 here is a permanent refusal
        the caller was told about, and journaling it would replay that refusal
        forever -- or land it later against a document that has since moved
        again. See `_write_notes`.
        """
        body: dict = {"notes": text, "op_key": op_key}
        if base_version is None:
            # Say it out loud. An omitted `base_version` is exactly what the
            # server refuses, so a silent omission is not a force -- it is a 422.
            body["force"] = True
        else:
            body["base_version"] = base_version
        # sync=True, and NOT covered by strict: under `async_writes` the write
        # would be journaled without touching the network and return None, so
        # `push` would read version 0, commit a base at 0 and print "pushed",
        # while nothing had been sent. The queued replace would later drain
        # against a stale base_version and dead-letter -- the edit lost after
        # the caller was told it shipped.
        return self._write_notes(entity, entity_id, body, strict=True, sync=True)

    def list_sub_notes(self, entity: str, entity_id: str) -> dict:
        """Titles + fullness for an entity's sub-notes. NO bodies — the list
        is for choosing; `get_sub_note` is the document read."""
        if entity == "project":
            return self.transport.get(f"/v1/projects/{entity_id}/sub-notes")
        if entity == "experiment":
            return self.transport.get(f"/v1/projects/{entity_id}/sub-notes")
        if entity == "run":
            return self.transport.get(f"/v1/runs/{entity_id}/sub-notes")
        if entity == "group":
            return self.transport.get(f"/v1/groups/{entity_id}/sub-notes")
        if entity == "artifact":
            return self.transport.get(f"/v1/artifacts/{entity_id}/sub-notes")
        raise errors.RosError(
            f"{entity!r} carries no sub-notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def get_sub_note(self, sub_note_id: str) -> dict:
        """One sub-note WITH its body and headroom (`remaining_chars`,
        `limit_chars` — the write responses deliberately omit the body)."""
        return self.transport.get(f"/v1/sub-notes/{sub_note_id}")

    def _create_sub_note(
        self, entity: str, entity_id: str, title: str, body: str = ""
    ) -> dict | None:
        """Create a titled sub-note. STRICT, never journaled — creation is not
        idempotent: titles are non-unique by design, so a create whose response
        was lost and then replayed is a second tab, not a retry, and the
        duplicate immediately makes every title-addressed write ambiguous.
        Refusals (blank title, the 20-per-entity cap) raise for the
        `_write_notes` reason: a refusal replayed later is the same no."""
        payload = {"title": title, "body": body}
        kw = {"strict": True, "raise_permanent": True}
        if entity == "project":
            return self.write("POST", f"/v1/projects/{entity_id}/sub-notes", payload, **kw)
        if entity == "experiment":
            return self.write("POST", f"/v1/projects/{entity_id}/sub-notes", payload, **kw)
        if entity == "run":
            return self.write("POST", f"/v1/runs/{entity_id}/sub-notes", payload, **kw)
        if entity == "group":
            return self.write("POST", f"/v1/groups/{entity_id}/sub-notes", payload, **kw)
        if entity == "artifact":
            return self.write("POST", f"/v1/artifacts/{entity_id}/sub-notes", payload, **kw)
        raise errors.RosError(
            f"{entity!r} carries no sub-notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def _write_sub_note_by_title(
        self, entity: str, entity_id: str, body: dict, *, strict: bool = False
    ) -> dict | None:
        """The title-addressed write. `strict=True` for an edit — same contract,
        same reasoning, as `_write_notes`."""
        kw = {"strict": strict, "raise_permanent": True}
        if entity == "project":
            return self.write("PATCH", f"/v1/projects/{entity_id}/sub-notes", body, **kw)
        if entity == "experiment":
            return self.write("PATCH", f"/v1/projects/{entity_id}/sub-notes", body, **kw)
        if entity == "run":
            return self.write("PATCH", f"/v1/runs/{entity_id}/sub-notes", body, **kw)
        if entity == "group":
            return self.write("PATCH", f"/v1/groups/{entity_id}/sub-notes", body, **kw)
        if entity == "artifact":
            return self.write("PATCH", f"/v1/artifacts/{entity_id}/sub-notes", body, **kw)
        raise errors.RosError(
            f"{entity!r} carries no sub-notes; expected one of {', '.join(self.NOTES_ENTITIES)}"
        )

    def _replace_sub_note_by_title(
        self,
        entity: str,
        entity_id: str,
        title: str,
        text: str,
        *,
        base_version: int | None = None,
        op_key: str = "",
    ) -> dict | None:
        """Replace a sub-note's body addressed by TITLE, not id.

        The title travels IN the write and the server resolves it at apply time,
        exactly once or refused with the count. That resolution is the door's
        whole reason to exist: a client-side resolve-then-write cannot be replayed
        safely, and an ambiguous title must refuse rather than pick.

        Spelled out per entity for the same reason `_write_notes` is: test_parity
        reads these call sites statically, and a computed path is invisible to it.
        """
        body: dict = {"note_title": title, "body": text}
        if op_key:
            body["op_key"] = op_key
        if base_version is None:
            body["force"] = True
        else:
            body["base_version"] = base_version
        kw = {"strict": True, "sync": True, "raise_permanent": True}
        if entity == "project":
            return self.write("PATCH", f"/v1/projects/{entity_id}/sub-notes", body, **kw)
        if entity == "experiment":
            return self.write("PATCH", f"/v1/projects/{entity_id}/sub-notes", body, **kw)
        if entity == "run":
            return self.write("PATCH", f"/v1/runs/{entity_id}/sub-notes", body, **kw)
        if entity == "group":
            return self.write("PATCH", f"/v1/groups/{entity_id}/sub-notes", body, **kw)
        if entity == "artifact":
            return self.write("PATCH", f"/v1/artifacts/{entity_id}/sub-notes", body, **kw)
        raise ValueError(f"unknown notes carrier: {entity}")

    def _replace_sub_note(
        self, sub_note_id: str, text: str, *, base_version: int | None, op_key: str
    ) -> dict | None:
        """Replace ONE sub-note's whole body, pinned to the version it was read at.

        Id-addressed, like rename and delete: the title-addressed door exists so
        a write can resolve at APPLY time and survive a queue, and this write
        never queues (strict=True -- a 409 is a permanent refusal the caller was
        told about). The CLI has already resolved the title through the list read.
        """
        body: dict = {"body": text, "op_key": op_key}
        if base_version is None:
            body["force"] = True
        else:
            body["base_version"] = base_version
        return self.write(
            "PATCH",
            f"/v1/sub-notes/{sub_note_id}",
            body,
            strict=True,
            sync=True,
            raise_permanent=True,
        )

    def _rename_sub_note(self, sub_note_id: str, title: str) -> dict | None:
        return self.write(
            "PATCH",
            f"/v1/sub-notes/{sub_note_id}",
            {"title": title},
            strict=True,
            raise_permanent=True,
        )

    def _delete_sub_note(self, sub_note_id: str) -> None:
        """Hard delete; the sub-note's history cascades with it. Direct, never
        journaled — a delete is confirmed interactively and must not land
        later against a tab someone kept using."""
        self.transport.delete(f"/v1/sub-notes/{sub_note_id}")

    def list_notes(
        self,
        *,
        query: str | None = None,
        cursor: str | None = None,
        limit: int = 100,
        include_sub_notes: bool = False,
    ) -> dict:
        """One page of the tenant-wide notes catalog: `{items, next_cursor}`.

        The DISCOVERY read, and the only one that answers a question no
        per-entity read can: which documents across the tenant are close to their
        cap. Every row carries `chars` and `limit_chars`, so a sweep is one page
        of this instead of one fetch per entity -- sizing 52 documents used to
        cost 52 API calls, which is why nobody did it and why
        `assignment-modeling` sat refused at 99,992 of 100,000 for a day.

        Rows are bounded by construction: an `excerpt` capped at 280 characters,
        never a body. `query` searches note bodies, titles and project /
        experiment / run ancestor titles LITERALLY (not wildcards).

        `limit` IS LOAD-BEARING, not a tuning knob. A bare `GET /v1/notes` with
        no query, cursor or limit returns the dashboard's lazy tree -- ROOT
        branches only, with children fetched per expansion -- so a sweep made
        without one would silently see only top-level documents and report
        "nothing is near full" about everything nested beneath them. Passing a
        limit selects the flat, keyset-paged listing, which is the one that
        walks every carrier in the tenant.

        This route was on `test_parity`'s permanent NOT_CLIENT_SURFACE list, with
        the reason "agents read and edit a known note through its owning entity".
        That reason held while the row carried no length -- the catalog told a
        client nothing it could not get from the entity. `chars`/`limit_chars`
        made it false, so the entry is gone rather than reworded.
        """
        params: dict[str, object] = {"limit": limit}
        if query is not None:
            params["query"] = query
        if cursor is not None:
            params["cursor"] = cursor
        if include_sub_notes:
            # Opt-in (0146): sub-note rows join the flat listing and the search
            # results. A server that predates the flag drops the unknown param
            # and answers the pre-0146 shape — degraded to the old sweep, never
            # an error.
            params["include_sub_notes"] = "true"
        return self.transport.get("/v1/notes", params=params)

    # ---------------------------------------------------------------- team note

    def get_team_note(self) -> dict:
        """The team's shared document: `{body, version, updated_at, updated_by,
        remaining_chars}`. Never 404s -- a team that has written nothing has an
        empty document at version 0.

        THE SYNC CLIENT USUALLY DOES NOT CALL THIS. `get_team_note_brief` already
        carries `version` AND `truncated`, so a brief that is not truncated IS
        the whole document -- which is the case for any note under
        BRIEF_MAX_CHARS. The file seed costs one request in the common case and
        falls back here only for a document large enough to be sliced.
        """
        return self.transport.get("/v1/team-note")

    def get_team_note_brief(self) -> dict:
        """The bounded slice a session is briefed with: `{text, truncated,
        version}`. What the SessionStart hook injects, and cheap enough to ask
        for mid-session when you want the current briefing without the document."""
        return self.transport.get("/v1/team-note/brief")

    def sync_team_note(self, body: str, *, base_version: int) -> dict:
        """THE AGENT WRITE: the whole document, plus the version it was edited from.

        Agents do not compose operations against this document any more. A
        session-start hook seeds a local markdown file, the agent edits it like
        any other file, and the session-stop reconcile sends the result here with
        the version it started from. The server merges against that base, so a
        teammate writing while this session worked is an ordinary merge rather
        than a refusal -- and two sides that both only ADDED text both land,
        which is the property the old `append` guaranteed.

        Returns `{state, version, remaining_chars, body?, merged}`. `state` is
        `applied` or `unchanged`; `unchanged` is what a retried reconcile gets
        and mints no version. When `merged` is true the server combined this
        document with someone else's and `body` is the result, which the caller
        must write back to its file so the next base comparison stays honest.

        A 409 carries the merged document WITH conflict markers under
        `merged_body`: write it to the file, resolve, sync again. A 422 names the
        marker lines when the document still has unresolved ones.
        """
        # strict: a 409 here is a REFUSAL carrying a document to act on, not a
        # transient failure to retry blindly.
        # sync=True: the reconcile needs the RESPONSE in hand (the new version,
        # and the merged body when the server combined two edits). Journaling
        # this write for later delivery would hand back None and leave the local
        # base copy pointing at a version that never existed.
        return self.write(
            "POST",
            "/v1/team-note/sync",
            {"body": body, "base_version": base_version},
            strict=True,
            sync=True,
        )

    def append_team_note(self, text: str) -> dict:
        """Add a paragraph at the end of the team note, merged by the SERVER.

        For a caller with no team-note file: the server reads, appends after a
        blank line and stores under its own row lock, so nothing a teammate
        wrote is lost and no version is needed. A caller that HAS the file
        edits it and syncs (`sync_team_note`) instead.

        Returns `{state, version, remaining_chars}`. A 422 names the cap or the
        conflict-marker lines; a 409 carrying `retryable: true` means another
        write landed at the same moment and nothing was stored.
        """
        # strict + sync: never journaled. A refusal replayed later is the same
        # refusal, and a queued write would hand back None instead of the
        # version the caller reports.
        return self.write(
            "POST",
            "/v1/team-note/apply/paragraph",
            {"text": text},
            strict=True,
            sync=True,
            raise_permanent=True,
        )

    def edit_team_note(self, old_text: str, new_text: str) -> dict:
        """Replace one exact piece of the team note, matched by the SERVER.

        `old_text` must occur exactly once; otherwise nothing is written and the
        409's detail carries `match_count`. `new_text=""` deletes it. Same
        return shape and other refusals as `append_team_note`.
        """
        return self.write(
            "POST",
            "/v1/team-note/apply/span",
            {"old_text": old_text, "new_text": new_text},
            strict=True,
            sync=True,
            raise_permanent=True,
        )

    def list_team_note_versions(
        self, *, limit: int | None = None, before: int | None = None
    ) -> dict:
        """History, newest first, WITHOUT bodies (a page of full documents is a
        megabyte). Each row is `{version, created_at, created_by, size_chars}`.

        `before` walks backwards: pass the response's `next_before` to get the
        next page, and stop when it comes back None. History is retained to the
        server's last N versions, so the walk ends at the oldest kept version
        rather than at version 1.
        """
        params = {k: v for k, v in (("limit", limit), ("before", before)) if v is not None}
        return self.transport.get("/v1/team-note/versions", params=params or None)

    def get_team_note_version(self, version: int) -> dict:
        """One past body, so you can see what you are about to restore."""
        return self.transport.get(f"/v1/team-note/versions/{version}")

    def restore_team_note_version(self, version: int) -> dict:
        """Make a past version current again, as a NEW version.

        A restore is an ordinary write, not a rewind: it takes the next version
        number and is itself recorded, so undoing an undo is possible and the
        history never loses the versions being stepped over.
        """
        return self.write("POST", f"/v1/team-note/versions/{version}/restore", {}, strict=True)

    def query_series(self, run_ids: list[str], **kw) -> dict:
        kw.setdefault("source_read_contract", SOURCE_READ_CONTRACT)
        return self.transport.post("/v1/series/query", {"run_ids": run_ids, **kw}, idempotent=True)

    def latest_scalars(
        self,
        run_ids: list[str],
        *,
        keys: list[str] | None = None,
        kind: str | None = None,
    ) -> dict:
        """``POST /v1/series/latest``: cross-run scalar summary (last/min/max per
        series) for run tables — reads the derived series catalog, never raw
        points. POST-for-read, so it retries like a GET. Every run must be live
        and in-tenant; a soft-deleted or unknown one is a 404 before any read.
        Built through the generated ``LatestScalarsRequest``, so the caps (50
        runs, 200 keys) fail client-side instead of as a server 422."""
        model = LatestScalarsRequest(
            run_ids=run_ids, keys=keys, kind=kind, source_read_contract=SOURCE_READ_CONTRACT
        )
        return self.transport.post(
            "/v1/series/latest",
            model.model_dump(mode="json", exclude_none=True),
            idempotent=True,
        )

    def compare(self, **kw):
        """Fetch several runs and their metric series together, aligned on step.

        The read people actually want when they open a comparison: which of these
        configs won. Name the runs with ``run_ids=[...]`` or select them with the
        same filters :meth:`list_runs` takes (``experiment_id=``, ``group_id=``)::

            comparison = client.compare(experiment_id=exp_id, keys=["dockq"])
            aligned = comparison.aligned("dockq")
            for label, values in aligned.values.items():
                plot(aligned.steps, values, label=label)   # or .to_pandas()

        Columns are labelled by the server's petname ``slug``. Runs of
        different lengths keep ``None`` holes rather than being truncated to the
        shortest — differing length is usually the thing being compared.

        A shaping layer over :meth:`query_series`, not a second client: see
        :mod:`probe.sdk.analysis`."""
        from .analysis import compare as _compare

        return _compare(self, **kw)

    def search(
        self,
        query: str,
        *,
        corpus: list[str] | None = None,
        workspace_id: str | None = None,
        project_id: str | None = None,
        top_k: int | None = None,
        exact_limit: int | None = None,
        exact_cursor: str | None = None,
        semantic_cursor: str | None = None,
        exclude_agent_session: str | None = None,
        curated_only: bool | None = None,
        exclude_origin_session: str | None = None,
    ) -> dict:
        """``POST /v1/search`` (workspaces+kb fold-in): one-index exact+semantic search.

        POST-for-read, so it retries like any GET. Returns the sectioned
        per-channel response ``{query, state, exact:{results,cursor,error},
        semantic:{results,cursor,error}}``; a backend that predates the
        endpoint 404s (callers such as the MCP source fall back).

        ``exclude_origin_session`` leaves out the projects, experiments and runs
        that coding-agent session CREATED (work another session created stays,
        wherever it is filed); a server that applied it echoes
        ``origin_exclusion_applied: true`` (absent = it did not)."""
        body: dict[str, Any] = {"query": query}
        optional = {
            "exclude_agent_session": exclude_agent_session,
            "exclude_origin_session": exclude_origin_session,
            "corpus": corpus,
            "workspace_id": workspace_id,
            "project_id": project_id,
            "top_k": top_k,
            "exact_limit": exact_limit,
            "exact_cursor": exact_cursor,
            "semantic_cursor": semantic_cursor,
            # None, not False, so the key is OMITTED unless the caller asked.
            # The filter below drops None; sending an explicit false would make
            # every request body differ from an older client's for no reason.
            "curated_only": curated_only,
        }
        body.update({key: value for key, value in optional.items() if value is not None})
        return self.transport.post("/v1/search", body, idempotent=True)

    def browse(
        self,
        *,
        scope: str | None = None,
        depth: int | None = None,
        status: str | None = None,
        tags: list[str] | None = None,
        workspace_id: str | None = None,
        limit: int | None = None,
        cursor: str | None = None,
        runs_cursor: str | None = None,
        subprojects_cursor: str | None = None,
        continuation_handles: bool | None = None,
        exclude_origin_session: str | None = None,
    ) -> dict:
        """``GET /v1/browse``: the structured "what exists" tree.

        ``continuation_handles=True`` opts into scope-bound positions before
        each fetched list and after every row. It is for bounded consumers
        that may emit fewer rows than the backend fetched. Ordinary calls keep
        the existing response and legacy keyset cursor contract.

        ``tags`` filters the RUNS level, like ``status`` (repeatable; a run
        must carry ALL — 0066). A pre-0066 backend ignores it; browse trees
        carry no per-run tags to verify against, so no guard here — the
        deterministic check is ``list_runs(tags=…)``.

        Where ``search`` ranks by relevance and needs a query, this enumerates
        structure and needs nothing -- the cold-start read. Returns
        ``{projects|experiments|runs, cursor, depth, limit, truncated}`` with
        exactly one level populated at the top, decided by ``scope``.

        ``workspace_id`` scopes the TOP level to one workspace -- the same lens
        ``list_projects(workspace_id=…)`` uses, so browse and the projects list
        can never disagree about what a workspace holds. It is REFUSED with
        ``scope`` (422): a scope has already narrowed to one project or
        experiment, and silently ignoring the workspace would answer a different
        question with a confident 200. A pre-0193 backend has no such parameter
        and IGNORES it, returning the whole tenant -- so treat a suspiciously
        wide answer as a version skew, not as a workspace holding everything.

        A backend that predates the endpoint 404s; callers fall back honestly
        rather than presenting an empty tree as "nothing exists".

        ``exclude_origin_session`` leaves out, at every level, the work that
        coding-agent session created (as :meth:`search`); echoed as
        ``origin_exclusion_applied: true`` by a server that applied it.
        """
        params: dict[str, Any] = {}
        optional = {
            "scope": scope,
            "depth": depth,
            "status": status,
            "tags": canonical_tags(tags) if tags else None,
            "workspace_id": workspace_id,
            "limit": limit,
            "cursor": cursor,
            # 0148: per-LEVEL continuation for the project scope's side lists
            # (from a prior response's `cursors`). Tokens are level-specific;
            # a project-scope token means nothing on another scope and the
            # server refuses it there.
            "runs_cursor": runs_cursor,
            "subprojects_cursor": subprojects_cursor,
            "continuation_handles": continuation_handles,
            "exclude_origin_session": exclude_origin_session,
        }
        params.update({k: v for k, v in optional.items() if v is not None})
        return self.transport.get("/v1/browse", params=params or None)

    # -- the open web (app/websearch) ---------------------------------------
    #
    # THE ONE FAMILY HERE THAT READS TEXT THIS LAB DID NOT WRITE. Everything
    # else on this client returns the tenant's own record; these three return
    # whatever a stranger published on a page they control. The narrowing that
    # matters happens at the backend boundary (app/websearch/service.py drops
    # raw HTML, caps page text, and spells `recency` itself rather than passing
    # a model's string into the upstream query) -- so these methods are thin ON
    # PURPOSE and must stay that way. A convenience here that widened what may
    # be sent would be re-opening a door somebody deliberately narrowed.
    #
    # NOT `idempotent=True`, unlike `search` above, and this is the one place
    # these three differ from every other POST-for-read on this client. HTTP
    # idempotent is not the same as FREE. `transport._RETRYABLE` is
    # {502, 503, 504}, which is exactly what `app/websearch/router.py` maps a
    # provider failure onto, so the retry would fire on precisely the wrong
    # cases: a 503 IS "over quota or rate limited, try later" (retrying 200ms
    # later is the one response guaranteed not to help), and a 502 or 504 can
    # follow a Firecrawl call that already completed and was already billed --
    # so the retry buys a second charge for an answer nobody reads. Marking
    # them idempotent additionally re-enables ReadTimeout retry, which the
    # transport excludes by default precisely because the request already
    # landed.
    #
    # Connect errors still retry (see `replayable` in transport.py): those never
    # reached the server, so they cost nothing and lose nothing.
    #
    # Only the arguments the caller SET are sent. The three request models are
    # `extra="forbid"` but their defaults are the backend's business, and a
    # client that echoed its own copy of `limit=5` would pin a value the
    # deployment is entitled to move. The MCP tool layer honours this too --
    # its `limit`/`expand` parameters default to None, not to a mirror of the
    # backend's current default.

    def search_web(
        self,
        query: str,
        *,
        limit: int | None = None,
        category: str | None = None,
        recency: str | None = None,
        include_domains: list[str] | None = None,
        exclude_domains: list[str] | None = None,
        include_content: bool | None = None,
    ) -> dict:
        """``POST /v1/web/search`` — web search, via the backend's Firecrawl key.

        Returns ``{query, state, results:[{title,url,snippet,text?}],
        credits_used}``. ``state`` is ``"empty"`` when the provider answered
        with nothing, which is an ANSWER and not a failure.

        ``include_domains`` and ``exclude_domains`` are mutually exclusive and
        the backend 422s on the pair rather than silently dropping one.
        """
        body: dict[str, Any] = {"query": query}
        optional = {
            "limit": limit,
            "category": category,
            "recency": recency,
            "include_domains": include_domains,
            "exclude_domains": exclude_domains,
            "include_content": include_content,
        }
        body.update({k: v for k, v in optional.items() if v is not None})
        return self.transport.post("/v1/web/search", body)

    def find_papers(
        self,
        mode: str,
        *,
        query: str | None = None,
        paper_id: str | None = None,
        limit: int | None = None,
        authors: str | None = None,
        categories: str | None = None,
        published_from: str | None = None,
        published_to: str | None = None,
        expand: str | None = None,
    ) -> dict:
        """``POST /v1/web/papers`` — the research literature, three ways.

        ``mode`` picks which question: ``search`` ranks abstracts, ``read``
        opens one paper (with ``query``, returns the passages answering it),
        ``similar`` expands from one paper along ``expand``.

        The backend REFUSES arguments the chosen mode cannot read rather than
        ignoring them, so a `paper_id` sent with ``mode="search"`` is a 422 and
        never a quietly different answer. Nothing is re-validated here: two
        copies of that table would drift, and the endpoint's copy is the one
        that decides.
        """
        body: dict[str, Any] = {"mode": mode}
        optional = {
            "query": query,
            "paper_id": paper_id,
            "limit": limit,
            "authors": authors,
            "categories": categories,
            "published_from": published_from,
            "published_to": published_to,
            "expand": expand,
        }
        body.update({k: v for k, v in optional.items() if v is not None})
        return self.transport.post("/v1/web/papers", body)

    def read_page(self, url: str) -> dict:
        """``POST /v1/web/read`` — one page as text.

        Returns ``{url, state, title, text, truncated}``. ``truncated`` is
        load-bearing: long pages are cut to the deployment's per-page ceiling,
        and a caller that ignores the flag presents a fragment as the document.
        """
        return self.transport.post("/v1/web/read", {"url": url})

    # -- passive / batch push ----------------------------------------------
    def ingest(
        self,
        *,
        experiment_slug: str,
        project_slug: str,
        run: dict,
        batch_id: str | None = None,
        execution_record: dict | None = None,
        spans: list[dict] | None = None,
        metrics: list[dict] | None = None,
        artifacts: list[dict] | None = None,
        strict: bool | None = None,
    ) -> dict | None:
        """One idempotent push (bearer ingest token + optional HMAC). Keyed on
        ``(customer_id, run.source, run.external_id)`` with ``batch_id`` dedup.

        Built through the generated ``IngestRunRequest`` (the backend now declares
        this body in its OpenAPI schema), so a malformed run/span/metric/artifact
        fails client-side instead of as a server 422.

        The ingest path is where the fold-in fields actually pin server-side:
        ``run['foreign_keys']`` (per-key new-wins merge), ``execution_record``
        (pins ``run.env_ref``), and per-metric ``dimensions``."""
        model = IngestRunRequest(
            experiment_slug=experiment_slug,
            run=run,
            project_slug=project_slug,
            batch_id=batch_id,
            execution_record=execution_record,
            spans=spans or [],
            metrics=metrics or [],
            artifacts=artifacts or [],
        )
        body = model.model_dump(mode="json", exclude_none=True)
        return self.write("POST", "/ingest/v1/runs", body, strict=strict)

    # -- composed SDK surfaces --------------------------------------------
    @property
    def events(self):
        """Read the backend append-only lifecycle+structure events log (read-only)."""
        if self._events is None:
            from .events import EventsReadClient

            self._events = EventsReadClient(self)
        return self._events


# Late import to avoid a cycle at module load (Run needs Client, Client returns Run).
from .run import Run  # noqa: E402
