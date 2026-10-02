"""Bounded, scrubbed crash reports for the SDK, carried as diagnostic spans.

Nothing in the client recorded a traceback before this module. ``fluent._excepthook``
received ``(exc_type, exc, tb)`` and kept exactly one bit of it -- ``"canceled"`` vs
``"failed"`` -- then dropped the rest on the floor. So when a customer's training
workers died inside Probe's write path, the only evidence that survived was the run's
status, which says *that* it broke and never *why*.

WHY A SPAN, NOT A VENDOR ERROR TRACKER
``POST /v1/runs/{run_ref}/spans`` is already client-writable, run-scoped and
tenant-isolated; ``span_type`` is free-form and ``attributes``/``coords`` are open
dicts. That buys four things no third-party tracker can:

* the report lands ON THE RUN -- the object you open when you ask what happened to
  seed 7 -- instead of in a separate system keyed to nothing you can join;
* it lands at the run's COORDINATE (``Run.span`` merges the ambient ``unit()``
  context), so N simultaneously-dying workers become N diagnostics at N coords
  under one run, which is the shape these incidents actually have;
* it never leaves the customer's install, so self-hosted deployments keep their own
  diagnostics and ``tests/selfhost/test_egress.py`` stays green;
* it adds NO dependency to a training process -- which is the blast radius that
  caused the incident this module exists to explain.

EVERYTHING HERE IS BEST-EFFORT AND MUST NEVER RAISE. A diagnostic that breaks a
teardown repeats the original sin in a more embarrassing place, so every public
entry point swallows unconditionally and the caps below are enforced before any
value reaches a payload rather than after.
"""

from __future__ import annotations

import collections
import json
import os
import platform
import re
import threading
import time
import traceback
from typing import Any

from .redaction import default_scrub, scrub_text

#: Frames kept per traceback. Deep recursion is the pathological case: a
#: RecursionError carries ~1000 near-identical frames, and the interesting ones
#: are the boundary at each end, never the middle.
MAX_FRAMES = 24
#: Chained causes walked (``raise ... from exc``). transport.py raises
#: ``TransportError(...) from exc``, so the httpx error that actually names the
#: failure -- ConnectTimeout vs ReadTimeout vs ConnectionRefused -- lives one link
#: down. A report that stops at the head loses the entire diagnosis.
MAX_CHAIN = 5
MAX_MESSAGE_CHARS = 512
MAX_TEXT_CHARS = 256
#: Per-field caps for the transport ring buffer and span naming.
MAX_PATH_CHARS = 120
MAX_ERROR_CHARS = 200
MAX_SPAN_NAME_CHARS = 128

#: Read once, as a module constant, so a test can flip it without setting
#: `os.name` globally -- doing that makes pathlib hand back WindowsPath and
#: takes the rest of the suite with it.
_IS_WINDOWS = os.name == "nt"
#: Whole-payload ceiling. A span write that 413s or stalls because a diagnostic
#: was large would be this module causing the class of outage it reports on.
MAX_REPORT_BYTES = 16_384

SPAN_TYPE = "diagnostic"

#: The package root. Frames under it are ours and are reported in full (this is
#: Apache-2.0 code); everything else is the caller's and is reduced to a
#: positional placeholder -- see :func:`_frames`.
_PKG_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

#: Run ids are server-minted UUIDs. Validated anyway, in BOTH directions: the id
#: is interpolated into a filename and into a request path, and it arrives from
#: a JSON file on disk in the sweep case. A breadcrumb carrying `../../x` would
#: otherwise place, delete, or POST outside where it belongs.
_RUN_ID_RE = re.compile(
    r"\A[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\Z"
)


def _valid_run_id(run_id: Any) -> bool:
    return isinstance(run_id, str) and bool(_RUN_ID_RE.match(run_id))


_OFF = frozenset({"off", "0", "false", "no", "disabled"})
_ON = frozenset({"on", "1", "true", "yes", "enabled"})


def disabled() -> bool:
    """Whether diagnostics are suppressed. ``PROBE_DIAGNOSTICS`` decides; when it
    is unset, ``PROBE_TELEMETRY=off`` also suppresses.

    The two knobs are NOT the same category and the precedence is the whole point.
    A diagnostic span goes to the customer's own backend, in their own tenant,
    attached to their own run -- the same category as a metric, and not the vendor
    phone-home ``PROBE_TELEMETRY`` was built to govern (see
    ``sdk/_telemetry_core.telemetry_disabled``).

    Deferring to it anyway when nobody said otherwise is the safe reading of
    "stop sending things": over-honoring an opt-out is never the wrong error.
    But it cannot be the LAST word, because the population that sets
    ``PROBE_TELEMETRY=off`` -- privacy-conscious, self-hosted, enterprise -- is
    exactly the population whose incidents cannot be reproduced in-house, and
    silently stripping their crash reports would leave the next outage as
    undiagnosable as the one this module was written for. So an explicit
    ``PROBE_DIAGNOSTICS`` wins in BOTH directions, and a customer who wants
    diagnostics without analytics can say so in one variable.
    """
    precise = (os.environ.get("PROBE_DIAGNOSTICS") or "").strip().lower()
    if precise in _OFF:
        return True
    if precise in _ON:
        return False
    return (os.environ.get("PROBE_TELEMETRY") or "").strip().lower() in _OFF


def _clip(value: Any, limit: int = MAX_TEXT_CHARS) -> str:
    text = value if isinstance(value, str) else str(value)
    if len(text) <= limit:
        return text
    return text[:limit] + f"...<+{len(text) - limit} chars>"


def _is_ours(filename: str) -> bool:
    try:
        return os.path.abspath(filename).startswith(_PKG_ROOT + os.sep)
    except Exception:
        return False


def _frames(tb: Any) -> tuple[list[dict], int]:
    """Frames as ``(kept, elided)``, Probe frames in full and caller frames as
    positional placeholders.

    The placeholder is the point. Dropping caller frames entirely would collapse
    the stack and lose the ONE thing a crash report has to answer -- where our
    code and their code meet -- while keeping them would put their module paths,
    and with them their unreleased project's structure, in a payload we render in
    a dashboard. A ``{"probe": false}`` entry holds the position without holding
    anything of theirs.

    Both ends are kept when the stack overflows ``MAX_FRAMES``: the boundary is at
    the ends, and the middle of a 1000-frame recursion is noise.
    """
    try:
        extracted = traceback.extract_tb(tb)
    except Exception:
        return [], 0

    total = len(extracted)
    if total > MAX_FRAMES:
        head = MAX_FRAMES // 2
        chosen = list(extracted[:head]) + list(extracted[total - (MAX_FRAMES - head) :])
        elided = total - len(chosen)
    else:
        chosen = list(extracted)
        elided = 0

    frames: list[dict] = []
    for f in chosen:
        if _is_ours(f.filename or ""):
            frames.append(
                {
                    "probe": True,
                    # Package-relative: the absolute path leaks the customer's
                    # filesystem layout (usernames, cluster mount points) and
                    # tells us nothing the relative path does not.
                    "file": os.path.relpath(os.path.abspath(f.filename), _PKG_ROOT),
                    "line": f.lineno,
                    "func": f.name,
                    "code": _clip(f.line or ""),
                }
            )
        else:
            frames.append({"probe": False})
    return frames, elided


#: Exception types whose message is, by construction, a value out of the
#: caller's data rather than prose an author wrote. `KeyError('OPENAI_API_KEY')`
#: carries a dict key; `KeyError('patient_4417')` carries a record id. No
#: pattern-scrubber can separate those from a harmless one, because the message
#: has no structure to key on -- it IS the datum. So the type is reported and
#: the message is not, which still names the failure without carrying a payload
#: we were never meant to see.
_OPAQUE_MESSAGE_TYPES = (KeyError, IndexError)


def _message_for(exc: BaseException) -> str:
    if isinstance(exc, _OPAQUE_MESSAGE_TYPES):
        return "<redacted: lookup key>"
    return scrub_text(exc, max_chars=MAX_MESSAGE_CHARS)


def _chain(exc: BaseException | None) -> list[dict]:
    """The exception and its causes, head first.

    ``__cause__`` (explicit ``raise ... from``) is preferred over ``__context__``
    (incidental "during handling of the above"), matching how Python itself
    prints a chain.
    """
    chain: list[dict] = []
    seen: set[int] = set()
    current = exc
    while current is not None and len(chain) < MAX_CHAIN:
        if id(current) in seen:  # a self-referential __context__ would spin forever
            break
        seen.add(id(current))
        try:
            frames, elided = _frames(current.__traceback__)
            entry: dict[str, Any] = {
                "type": type(current).__name__,
                "module": type(current).__module__,
                # scrub_text, NOT _clip. The frame filter keeps caller CODE out
                # of a report, and the message channel walked straight around it:
                # KeyError names its key, FileNotFoundError names its path, and
                # an assertion prints whatever the author interpolated. Verified
                # leaking before this call existed.
                "message": _message_for(current),
                "frames": frames,
            }
            if elided:
                entry["frames_elided"] = elided
            # The typed fields off errors.RosError: status is what separates "the
            # backend refused us" from "we never reached it", which is the first
            # fork in any triage of this class of failure.
            status = getattr(current, "status", None)
            if isinstance(status, int):
                entry["status"] = status
            chain.append(entry)
        except Exception:
            break
        current = current.__cause__ or current.__context__
    return chain


def _environment() -> dict:
    env: dict[str, Any] = {}
    try:
        from .. import __version__

        env["sdk_version"] = __version__
    except Exception:
        pass
    try:
        env["python"] = platform.python_version()
        env["platform"] = platform.system()
    except Exception:
        pass
    return env


def build_report(
    exc: BaseException | None,
    *,
    client: Any = None,
    extra: dict | None = None,
    run_id: str | None = None,
) -> dict:
    """A scrubbed, bounded diagnostic payload. Never raises.

    The result is safe to hand straight to ``Run.span(attributes=...)``: it is
    already scrubbed through :func:`~probe.sdk.redaction.default_scrub` and
    already inside :data:`MAX_REPORT_BYTES`.
    """
    report: dict[str, Any] = {"schema": 1}
    try:
        report["environment"] = _environment()
        if exc is not None:
            report["exception"] = _chain(exc)
            from .failure_context import read

            if context := read(exc, run_id):
                report["context"] = context
        if client is not None:
            report["client"] = _client_state(client)
        recent = recent_transport(_base_of(client) if client is not None else None)
        if recent:
            # The durations are the point, not just the failures: a stall throws
            # nothing, so this is the only place it is visible.
            report["transport"] = recent
        if extra:
            report["extra"] = extra
        report = default_scrub(report)
        report = _fit(report)
    except Exception:
        return {"schema": 1, "degraded": "report construction failed"}
    return report


def _base_of(client: Any) -> str | None:
    """The backend this client talks to, as the transport-log partition key."""
    try:
        return getattr(getattr(client, "settings", None), "base_url", None)
    except Exception:
        return None


def _client_state(client: Any) -> dict:
    """The delivery-path state a reader needs to tell a transport failure from a
    delivery-path failure.

    ``async_writes`` matters most: once it defaults on, a failed write journals
    instead of raising, so the run quietly stops receiving metrics while training
    continues -- a silent failure where there used to be a loud one. A report that
    does not say which mode was in force cannot distinguish the two.
    """
    state: dict[str, Any] = {}
    for attr in ("async_writes", "fail_open"):
        try:
            value = getattr(client, attr, None)
            if isinstance(value, bool):
                state[attr] = value
        except Exception:
            continue
    try:
        exporter = getattr(client, "_exporter", None)
        if exporter is not None:
            state["exporter_alive"] = bool(getattr(exporter, "alive", False))
    except Exception:
        pass
    return state


def _fit(report: dict) -> dict:
    """Bring the payload inside :data:`MAX_REPORT_BYTES`.

    Sheds in order of what is least the diagnosis: the two genuinely unbounded
    fields first (``extra`` is arbitrary caller kwargs, ``transport`` is 32
    entries), then frame source lines, then caller placeholders, then chain
    links from the tail. The head of the chain and the exception types carry the
    answer and are the last things to go; when even they do not fit, the report
    is REPLACED by an honest marker rather than truncated, because half a JSON
    document is worse than none.

    The marker is stamped BEFORE each measurement, not after. Adding it
    afterwards let a report pass the check at N bytes and then leave the
    function at N plus the marker -- over the very budget it had just satisfied.
    """
    import copy

    def size(obj: dict) -> int:
        return len(json.dumps(obj, default=str).encode("utf-8", "replace"))

    if size(report) <= MAX_REPORT_BYTES:
        return report

    # A copy: _fit used to mutate its caller's dict while sometimes returning a
    # different object, so `sweep` recorded the un-shed original as what it sent.
    report = copy.deepcopy(report)

    def fits(marker: str) -> bool:
        report["truncated"] = marker
        if size(report) <= MAX_REPORT_BYTES:
            return True
        del report["truncated"]
        return False

    if report.pop("extra", None) is not None and fits("extra"):
        return report
    if report.pop("transport", None) is not None and fits("transport"):
        return report

    chain = report.get("exception") or []
    for link in chain:
        for frame in link.get("frames") or []:
            frame.pop("code", None)
    if fits("frame source"):
        return report

    for link in chain:
        link["frames"] = [f for f in (link.get("frames") or []) if f.get("probe")]
    if fits("caller frames"):
        return report

    popped = False
    while len(chain) > 1 and size(report) > MAX_REPORT_BYTES:
        chain.pop()
        popped = True
    # Only claim it when it happened: a hard-exit report carries no exception at
    # all, so this tier popped nothing and still stamped "chain".
    if popped and fits("chain"):
        return report

    return {
        "schema": 1,
        "degraded": "report exceeded size budget",
        "environment": report.get("environment", {}),
    }


def emit(run: Any, report: dict, *, name: str | None = None) -> None:
    """Write one diagnostic span. Never raises, never blocks on delivery policy.

    ``strict=False`` is not decoration: it routes the write through the fail-open
    branch of ``Client.write``, so a diagnostic that cannot be delivered journals
    to the outbox instead of throwing inside a teardown path that is, by
    construction, already handling a failure.
    """
    if disabled() or run is None:
        return
    try:
        run.span(
            SPAN_TYPE,
            name=_clip(name or "diagnostic", MAX_SPAN_NAME_CHARS),
            status="failed",
            attributes=report,
            strict=False,
            # Must never hold the run's close. finish() refuses to mark a run
            # terminal while any of its ops are undelivered, so a diagnostic the
            # server rejects would leave the run `running` for the reaper --
            # the report changing the outcome it reports on.
            blocking=False,
        )
    except Exception:
        pass


def report_exception(run: Any, exc: BaseException | None, **kw: Any) -> None:
    """Build and emit in one call. Never raises."""
    if disabled() or run is None:
        return
    try:
        client = getattr(run, "_client", None)
        report = build_report(exc, client=client, extra=kw or None, run_id=getattr(run, "id", None))
        emit(run, report, name=type(exc).__name__ if exc is not None else None)
    except Exception:
        pass


# ---------------------------------------------------------------------------
# Swallowed exceptions: the evidence fail-open used to delete
# ---------------------------------------------------------------------------
# The client has ~248 `except Exception` bodies. Fail-open is the right contract
# for nearly all of them -- telemetry must not kill a training run -- but the
# bodies were also DELETING the diagnosis, which is how an incident becomes
# "the data stopped arriving and nobody knows why". These sites keep failing
# open and stop being silent.
#
# Two hard constraints separate this from `report_exception`:
#
#   1. VOLUME. A swallow inside a training loop can fire on every step. An
#      unbounded reporter would turn one broken machine into a beacon and
#      re-create the cost fail-open exists to avoid.
#   2. NO RUN. Many swallow sites (CLI command paths, journal writes before a
#      run exists) have nothing to hang a span on.

#: How long ONE site stays quiet after reporting. Cross-process (a stamp file on
#: the journal dir), because the workload this must survive is a training loop
#: shelling out to `probe log` per step -- every in-memory budget resets on each
#: of those, so N commands would mean N reports.
SWALLOW_REPORT_INTERVAL_S = 6 * 3600.0

#: Reports per site within ONE process, on top of the cross-process throttle.
#: Bounds the in-process SDK case (`import probe` in a training script, where the
#: same interpreter can hit a swallow site thousands of times) without a stat per
#: call. The file stamp is what bounds the shell-out case.
MAX_SWALLOWED_PER_SITE = 3

_swallowed_counts: dict[str, int] = {}


def _swallow_budget(site: str) -> bool:
    """Whether `site` may report once more IN THIS PROCESS. Not thread-safe by
    choice: the failure mode of a race here is one extra report, and a lock on a
    fail-open path is a worse trade than an occasional duplicate."""
    seen = _swallowed_counts.get(site, 0)
    if seen >= MAX_SWALLOWED_PER_SITE:
        return False
    _swallowed_counts[site] = seen + 1
    return True


def capture_swallowed(
    exc: BaseException,
    *,
    site: str,
    run: Any = None,
    base_url: str | None = None,
    spool_dir: str | None = None,
    surface: str = "sdk",
) -> bool:
    """Report an exception that was caught and deliberately NOT re-raised.

    Additive by construction: the caller has already recovered, and this must
    never change that. Returns whether a report was sent, for tests.

    `site` is a stable hand-written label for the swallow LOCATION
    (``"client.enqueue_dropped"``, ``"client.lease_renew"``). It is the grouping
    key, the throttle key, AND a property on the wire -- it must be a literal,
    never an f-string carrying an id, which would defeat the throttle and split
    one issue into thousands.

    `base_url` is the backend the CALLER is talking to, and it is what gates the
    no-run leg against the self-host egress contract. The SDK resolves its
    backend from `probe.init(base_url=...)` or a named context, neither of which
    the CLI config file reflects -- so letting `report_crash` fall back to that
    config would gate on a backend this process may not be using. Omitting it
    means the report is suppressed, not guessed.

    Routes to whichever channel can carry it: a run-scoped swallow becomes a
    diagnostic span on that run (stays in the customer's own tenant, joins the
    other diagnostics for that run); one without a run rides the PostHog
    `$exception` pipe as a HANDLED report.
    """
    if disabled():
        return False
    try:
        if not _swallow_budget(site):
            return False
        if run is not None:
            report_exception(run, exc, swallowed_at=site)
            return True
        if not base_url:
            return False  # unknown backend: fail closed, never guess hosted
        from probe._shared import telemetry as telemetry_mod

        if not telemetry_mod.report_due(
            spool_dir, f"swallow-{site}", interval_s=SWALLOW_REPORT_INTERVAL_S
        ):
            return False
        telemetry_mod.report_crash(
            exc, surface=surface, base_url=base_url, handled=True, site=site
        )
        return True
    except Exception:
        return False  # a reporter that raises into a swallow site is a new bug


# ---------------------------------------------------------------------------
# Hard kills: the breadcrumb sweep
# ---------------------------------------------------------------------------
# SIGKILL, the OOM killer, a NCCL collective timeout tearing the process down,
# and a segfault all skip `atexit` entirely, so the exit-hook path above never
# fires for them -- and they are a large share of how training workers actually
# die. A detached reporter subprocess does not fix it either: there is no moment
# at which a SIGKILLed process gets to send anything.
#
# So invert it. Drop a breadcrumb on disk when a run opens, remove it on a clean
# close, and have the NEXT client sweep whatever is left behind. A breadcrumb
# whose pid is gone is a process that died without closing its run, which is
# exactly the population the exit hook cannot see. The report arrives late, from
# a different process, which for a postmortem is the difference between late and
# never.

_BREADCRUMB_SUFFIX = ".crash.json"
#: Breadcrumbs read per sweep. A crash-looping job can leave thousands; the
#: sweep runs on the `init()` path, so it must stay cheap and bounded.
MAX_SWEEP = 8
#: Past this age a breadcrumb is swept regardless of what `_pid_alive` says.
#: Long enough that a legitimately long-running sibling run is never mistaken
#: for a corpse; short enough that evidence is not stranded for a week.
STALE_AFTER_SECONDS = 24 * 3600
#: Sweeps a single undeliverable breadcrumb may survive before it is dropped.
MAX_ORPHAN_ATTEMPTS = 3


def _breadcrumb_dir(client: Any) -> str | None:
    """The journal directory. Diagnostics live beside the outbox on purpose:
    it is already per-context, already isolated in tests, and already the
    directory whose survival the durable write path depends on."""
    try:
        directory = getattr(getattr(client, "journal", None), "dir", None)
        return str(directory) if directory else None
    except Exception:
        return None


def _has_disk_headroom(directory: str) -> bool:
    """Whether the outbox's reserved free space is intact.

    Reuses the journal's floor (`journal.free_floor`) rather than
    inventing a second floor: the reason that floor exists -- this directory
    sits beside training checkpoints -- applies identically to a breadcrumb.
    Unknown answers as True; refusing to write on a stat failure would disable
    the feature for a condition we cannot even confirm.
    """
    try:
        import shutil

        from .journal import free_floor

        floor = free_floor(directory)
        if not floor:
            return True
        return shutil.disk_usage(directory).free >= floor
    except Exception:
        return True


def _write_private(path: str, text: str) -> None:
    """0o600 atomic write, via the SDK's existing durable helper.

    Imported lazily: diagnostics is imported by transport, and transport is
    imported by half the SDK -- a module-level import here would widen the
    import graph for a function most processes never call.
    """
    from .durable import write_text_atomic

    write_text_atomic(path, text, mode=0o600)


def arm(client: Any, run_id: str, *, extra: dict | None = None) -> None:
    """Drop this run's crash breadcrumb. Never raises."""
    if disabled():
        return
    try:
        directory = _breadcrumb_dir(client)
        if not directory or not _valid_run_id(run_id):
            return
        if not _has_disk_headroom(directory):
            # journal.py gates blob staging on the same floor because this
            # directory sits next to training checkpoints. Diagnostics must not
            # be what consumes the headroom the outbox deliberately reserves.
            return
        # 0o700, matching journal.py: "queue contents are research data" and a
        # breadcrumb sits in the same directory carrying the same class of thing.
        os.makedirs(directory, mode=0o700, exist_ok=True)
        try:
            os.chmod(directory, 0o700)  # mkdir mode is masked by umask
        except OSError:
            pass
        payload = {
            "run_id": run_id,
            "pid": os.getpid(),
            # A pid is only meaningful on the host that issued it, and the
            # journal defaults to ~/.local/state/probe/outbox -- a shared NFS
            # home on any ordinary SLURM or k8s cluster. Without this, node B
            # finds node A's breadcrumb, gets ProcessLookupError for a pid that
            # is happily training on A, files a crash against a LIVE run, and
            # then deletes the evidence.
            "host": _host_identity(),
            "environment": _environment(),
            "client": _client_state(client),
        }
        if extra:
            payload["extra"] = extra
        path = os.path.join(directory, f"{run_id}{_BREADCRUMB_SUFFIX}")
        # write_text_atomic, not a hand-rolled `path + ".tmp"`: its temp sibling
        # is randomly named and opened O_EXCL, so a pre-planted symlink at a
        # guessable temp path cannot redirect the write. Guessable is the
        # operative word -- the run id is in the run's own dashboard URL.
        _write_private(path, json.dumps(default_scrub(payload)))
        global _ACTIVE_BREADCRUMB, _FIRST_INCIDENT
        _ACTIVE_BREADCRUMB = (path, run_id, _base_of(client))
        _FIRST_INCIDENT = None  # a new run starts a new incident history
    except Exception:
        pass


def disarm(client: Any, run_id: str) -> None:
    """Remove the breadcrumb after a clean close. Never raises."""
    global _ACTIVE_BREADCRUMB
    # Only the owner disarms. fluent supports concurrently scoped runs, so a
    # worker thread closing run A was silently killing run B's refresh -- B kept
    # its file but stopped recording transport state, which is the entire value
    # of the breadcrumb.
    if _ACTIVE_BREADCRUMB is not None and _ACTIVE_BREADCRUMB[1] == run_id:
        _ACTIVE_BREADCRUMB = None
    try:
        directory = _breadcrumb_dir(client)
        if not directory or not _valid_run_id(run_id):
            return
        os.unlink(os.path.join(directory, f"{run_id}{_BREADCRUMB_SUFFIX}"))
    except Exception:
        pass


def _host_identity() -> str:
    """Hostname plus, where available, the boot id -- so a rebooted host does
    not read as the same process table it had before."""
    try:
        import socket

        host = socket.gethostname()
    except Exception:
        host = "unknown"
    try:
        with open("/proc/sys/kernel/random/boot_id", encoding="utf-8") as fh:
            return f"{host}:{fh.read().strip()[:12]}"
    except Exception:
        return host


def _pid_alive(pid: int) -> bool:
    """Whether a pid is still running.

    Treated as ALIVE whenever the answer is not a clean "no": a false negative
    files a crash report for a healthy run, which is worse than missing one.
    """
    if _IS_WINDOWS:
        # NOT a liveness probe on Windows. CPython documents that any sig other
        # than CTRL_C_EVENT/CTRL_BREAK_EVENT routes to TerminateProcess, so
        # `os.kill(pid, 0)` KILLS the process with exit code 0. sweep() runs on
        # every probe.init(), so this would have had a second training process
        # silently terminate its live siblings. Fall back to the age rule.
        return True
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except Exception:
        # PermissionError (another user's pid) and pid namespaces land here.
        # "Alive" is the safe direction for a single check -- a false negative
        # files a crash against a healthy run -- and STALE_AFTER_SECONDS is what
        # keeps that from being permanent.
        return True


def sweep(client: Any) -> list[dict]:
    """Report and clear breadcrumbs left by processes that are gone.

    Returns the reports filed, for tests and for callers that want to log them.
    Never raises. Breadcrumbs belonging to LIVE pids are left alone -- a
    concurrent run on the same journal is the normal case, not a crash.
    """
    if disabled():
        return []
    filed: list[dict] = []
    try:
        directory = _breadcrumb_dir(client)
        if not directory or not os.path.isdir(directory):
            return []
        # OLDEST FIRST, not lexicographic. `sorted()` by name pinned the same
        # MAX_SWEEP entries every pass, so a handful of breadcrumbs that always
        # read as alive -- a pid owned by another user raises PermissionError,
        # and a pid namespace makes the integer live in a sibling container --
        # would starve every genuinely dead one behind them, forever, silently.
        entries = []
        for n in os.listdir(directory):
            if not n.endswith(_BREADCRUMB_SUFFIX):
                continue
            full = os.path.join(directory, n)
            try:
                entries.append((os.path.getmtime(full), full))
            except OSError:
                continue
        entries.sort()
        for mtime, path in entries[:MAX_SWEEP]:
            try:
                with open(path, encoding="utf-8") as fh:
                    crumb = json.load(fh)
            except Exception:
                # Unreadable or torn: drop it rather than re-reading it forever.
                _unlink(path)
                continue
            # Age overrides liveness. `_pid_alive` answers "alive" whenever it
            # cannot get a clean no, which is the right default for a single
            # check and an unbounded one across time: without a ceiling a
            # breadcrumb that never resolves is never filed and never removed.
            if crumb.get("host") and crumb["host"] != _host_identity():
                # Another machine's crumb. Not sweepable and NOT a crash: its
                # pid means nothing here. Leave it for the host that owns it.
                continue
            stale = (time.time() - mtime) > STALE_AFTER_SECONDS
            pid = crumb.get("pid")
            if not stale and isinstance(pid, int) and _pid_alive(pid):
                continue
            run_id = crumb.get("run_id")
            if not _valid_run_id(run_id):
                _unlink(path)
                continue
            report = {
                "schema": 1,
                "kind": "hard_exit",
                # No exception and no traceback by construction: the process was
                # killed rather than raising. What it died OF is not knowable
                # from here -- what IS knowable is that it never closed its run,
                # and the delivery state it was in when it stopped.
                "detail": "process exited without closing the run (signal, OOM, or hard kill)",
                "environment": crumb.get("environment", {}),
                "client": crumb.get("client", {}),
                "pid": pid,
            }
            if crumb.get("first_incident"):
                report["first_incident"] = crumb["first_incident"]
            if crumb.get("transport"):
                # What the transport was doing when the process stopped
                # existing. For a kill with no traceback this is the only
                # evidence there is.
                report["transport"] = crumb["transport"]
            if crumb.get("extra"):
                report["extra"] = crumb["extra"]
            if _post_orphan(client, run_id, report):
                filed.append(report)
                _unlink(path)
            else:
                # Do NOT unlink. Unlinking regardless destroyed the evidence
                # with nothing recorded anywhere and no retry -- and the thing
                # that makes the append fail (a full disk) is exactly the thing
                # that makes the next attempt worth having. Bounded so a
                # permanently-undeliverable crumb cannot be swept forever.
                attempts = int(crumb.get("attempts") or 0) + 1
                if attempts >= MAX_ORPHAN_ATTEMPTS:
                    _unlink(path)
                else:
                    crumb["attempts"] = attempts
                    try:
                        _write_private(path, json.dumps(default_scrub(crumb)))
                    except Exception:
                        pass
    except Exception:
        pass
    return filed


def _unlink(path: str) -> None:
    try:
        os.unlink(path)
    except Exception:
        pass


def _post_orphan(client: Any, run_id: str, report: dict) -> bool:
    """JOURNAL an orphan's diagnostic span. Never touches the network.

    Not via `Run.span`: the run handle died with its process, and rebuilding one
    would re-open a run this very report says is over. The span endpoint is the
    same one `Run.span` posts to, so the record is identical either way.

    And not via `client.write` either, which was the first shape and was wrong in
    the worst possible place. `write` goes straight to the transport when
    `async_writes` is off, at a 30s timeout, with no budget across the loop --
    so a sweep of 8 breadcrumbs could add minutes to `probe.init()`. The
    population holding 8 stale breadcrumbs is precisely the population whose
    backend is unreachable, and a crash-looping job pays it on every restart, on
    every rank. Appending to the journal hands delivery to the drainer and keeps
    init off the network entirely.
    """
    try:
        import uuid

        client.journal.append_http(
            "POST",
            f"/v1/runs/{run_id}/spans",
            {
                "spans": [
                    {
                        "id": str(uuid.uuid4()),
                        "span_type": SPAN_TYPE,
                        "name": "hard_exit",
                        "status": "failed",
                        "attributes": _fit(report),
                    }
                ]
            },
            blocking=False,
        )
        return True
    except Exception:
        return False


# ---------------------------------------------------------------------------
# The transport ring buffer
# ---------------------------------------------------------------------------
# The suspected kill path in the ProSeCo incident throws NO exception. A stalled
# endpoint parks a synchronous write for the whole timeout; in distributed
# training that trips a collective and every rank dies together, with the
# traceback in the customer's code and nothing raised in ours. No error tracker
# on the market sees that, because there is no error -- there is only a DURATION.
#
# So record durations, not just failures. The buffer is bounded and in memory;
# what makes it survive a hard kill is that an incident refreshes the breadcrumb,
# so a SIGKILLed worker leaves behind the last thing its transport was doing.

#: Requests retained. Deep enough to show a pattern, shallow enough that the
#: whole buffer fits a bounded report several times over.
TRANSPORT_LOG_SIZE = 32
#: A request at or above this is reported as a stall. Well under the 30s read
#: timeout on purpose: by 30s a collective has usually already given up, so a
#: threshold set at the timeout would only ever confirm deaths after the fact.
STALL_SECONDS = 5.0
#: Floor between incident-driven breadcrumb rewrites. A hard failure loop can
#: produce thousands of incidents a second and this runs on the write path.
_REFRESH_MIN_INTERVAL = 5.0

_TRANSPORT_LOG: collections.deque = collections.deque(maxlen=TRANSPORT_LOG_SIZE)
_ACTIVE_BREADCRUMB: tuple[str, str, str | None] | None = None  # (path, run_id, base)
#: The first stall or error seen since the breadcrumb was armed, kept forever.
#: The rolling window is 32 entries -- well under a second of a training loop --
#: and the refresh is last-writer-wins, so by the time a process is killed the
#: window holds the tail of the cascade and has long evicted the stall that
#: STARTED it. That first one is the diagnosis.
_FIRST_INCIDENT: dict | None = None
#: The request currently on the wire, if any. Not in the ring buffer: it has no
#: outcome yet, and it is replaced rather than appended.
_INFLIGHT: dict | None = None
_LAST_REFRESH = 0.0
_REFRESH_LOCK = threading.Lock()


def record_transport(
    method: str,
    path: str,
    *,
    seconds: float,
    status: int | None = None,
    error: str | None = None,
    base: str | None = None,
) -> None:
    """Note one request's outcome. Never raises, never blocks.

    Called from the transport's hot path, so it does no I/O except on an
    incident, and even then at most once per `_REFRESH_MIN_INTERVAL`.
    """
    try:
        stalled = seconds >= STALL_SECONDS
        entry: dict[str, Any] = {
            "m": method,
            "p": _clip(path, MAX_PATH_CHARS),
            "ms": round(seconds * 1000),
        }
        if base:
            # One process can hold clients for two backends (a self-hosted
            # install plus hosted, or two workspaces). The buffer is shared, so
            # without this stamp a report written to ONE of them carried the
            # other's request history.
            entry["base"] = base
        if status is not None:
            entry["status"] = status
        if error:
            entry["error"] = scrub_text(error, max_chars=MAX_ERROR_CHARS)
        if stalled:
            entry["stalled"] = True
        _TRANSPORT_LOG.append(entry)  # deque.append is atomic under the GIL
        if stalled or error:
            global _FIRST_INCIDENT
            if _FIRST_INCIDENT is None:
                _FIRST_INCIDENT = dict(entry)
            if not disabled():
                _refresh_breadcrumb()
    except Exception:
        pass


def begin_transport(method: str, path: str, *, base: str | None = None) -> None:
    """Mark a request as in flight, and persist the mark.

    Without this the ring buffer only ever learns about requests that RETURNED
    or RAISED -- so the one case the whole feature exists for, a request that
    hangs until the process is SIGKILLed, left no trace at all and the
    breadcrumb preserved the last COMPLETED request instead of the hanging one.
    A stall that is killed rather than timed out is still the diagnosis.
    """
    try:
        if disabled():
            return
        global _INFLIGHT
        _INFLIGHT = {"m": method, "p": _clip(path, MAX_PATH_CHARS), "inflight": True}
        if base:
            _INFLIGHT["base"] = base
        _refresh_breadcrumb()
    except Exception:
        pass


def end_transport() -> None:
    try:
        global _INFLIGHT
        _INFLIGHT = None
    except Exception:
        pass


def recent_transport(base: str | None = None) -> list[dict]:
    """The buffer, oldest first, with any in-flight request last.

    ``base`` restricts it to one backend. Pass it whenever the result is going
    to be WRITTEN somewhere -- a report delivered to one tenant must not carry
    another tenant's request history.
    """
    try:
        entries = list(_TRANSPORT_LOG)
        inflight = _INFLIGHT
        if inflight is not None:
            entries.append(dict(inflight))
        if base:
            entries = [e for e in entries if e.get("base") in (None, base)]
        return entries
    except Exception:
        return []


def _refresh_breadcrumb() -> None:
    """Rewrite the active breadcrumb with the current transport buffer.

    This is what turns an in-memory ring buffer into hard-kill evidence: the
    file on disk is the only thing that outlives a SIGKILL, so an incident is
    the moment worth paying an fsync-ish cost to persist one.
    """
    global _LAST_REFRESH
    try:
        active = _ACTIVE_BREADCRUMB
        if active is None:
            return
        now = time.monotonic()
        # Throttle BEFORE acquiring, and never wait for the lock. Checking it
        # inside meant every thread recording an error had to first queue behind
        # whichever thread was mid-write -- so the "at most once per interval"
        # claim bounded duplicate I/O while leaving the BLOCKING unbounded, on a
        # journal dir that is an NFS home on most clusters. A refresh that loses
        # this race is one that was about to be throttled anyway.
        if now - _LAST_REFRESH < _REFRESH_MIN_INTERVAL:
            return
        if not _REFRESH_LOCK.acquire(blocking=False):
            return
        try:
            if now - _LAST_REFRESH < _REFRESH_MIN_INTERVAL:
                return
            _LAST_REFRESH = now
            path, _run_id, base = active
            try:
                with open(path, encoding="utf-8") as fh:
                    crumb = json.load(fh)
            except Exception:
                return
            crumb["transport"] = recent_transport(base)
            if _FIRST_INCIDENT is not None:
                # Written every time but never CHANGED: it is the entry the
                # rolling window will have evicted by the time anyone reads this.
                crumb["first_incident"] = _FIRST_INCIDENT
            if not _has_disk_headroom(os.path.dirname(path)):
                return
            _write_private(path, json.dumps(default_scrub(crumb)))
        finally:
            _REFRESH_LOCK.release()
    except Exception:
        pass


def _reset_after_fork() -> None:
    """Re-arm module state in a forked child.

    A child forked while `_REFRESH_LOCK` was held inherits it LOCKED with no
    thread alive to release it, so the child's first stall or error would block
    forever -- and a deadlock is not an exception, so nothing here would catch
    it. torch's DataLoader with num_workers>0 forks exactly this way, from a
    process where the exporter and heartbeat threads are both live and both
    reach `record_transport`.

    The breadcrumb is dropped rather than inherited: it belongs to the parent's
    run, and a child rewriting it would race the parent for the same file.
    """
    global _REFRESH_LOCK, _ACTIVE_BREADCRUMB, _LAST_REFRESH
    _REFRESH_LOCK = threading.Lock()
    _ACTIVE_BREADCRUMB = None
    _LAST_REFRESH = 0.0
    _TRANSPORT_LOG.clear()
    globals()["_INFLIGHT"] = None
    globals()["_FIRST_INCIDENT"] = None


if hasattr(os, "register_at_fork"):  # POSIX only; a no-op on Windows
    os.register_at_fork(after_in_child=_reset_after_fork)
