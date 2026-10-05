"""`probe` - the Probe Research CLI implementation, built on typer.

Thin wrapper over the SDK. The write path a coding agent (or a shell script) calls
to record experiment data. A data write Probe did not answer is queued in the local
outbox and delivered later (the command says `queued`); one Probe refused fails, exit 1.
Read convenience verbs (`get`, `bundle`) wrap the same read service the MCP tools use.

Connection flags (`--base-url/--token/--ingest-token/--hmac-secret`) are global and
go before the command: `probe --token probe_pat_x log RUN loss=0.1`. `login` also accepts
them directly so `probe login --token ...` works. Config lives in ~/.config/probe/config.json.

Auth: `probe login --device` runs the browser handoff (RFC 8628) and captures the
`probe_pat_...` token; `probe login --token probe_pat_...` is the air-gap paste path.
"""

from __future__ import annotations

import contextlib
import dataclasses
import hashlib
import json
import math
import os
import re
import shlex
import subprocess
import sys
import uuid

from probe.sdk.snapshot import wire_name
import tempfile
import textwrap
import time
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import TYPE_CHECKING, Any, Optional

if TYPE_CHECKING:
    from probe.cli import telemetry as probe_telemetry

import typer
from pydantic import ValidationError

from .. import __version__, errors
from ..client_headers import client_version_headers
from ..models import AnchorLevel, CitationDirection, LineageEntityType, LineageRelation, Scope
from ..sdk.client import _FILE_ANCHORS, Anchor, Client, Rewind
from ..sdk.config import (
    DEFAULT_BASE_URL,
    clear_context,
    config_path,
    current_context_name,
    delete_context,
    load_context,
    load_file,
    resolve,
    save_context,
    use_context,
)
from ..sdk import agent_session, daemon_channel, session_marker
from ..sdk.nonfinite import to_wire as nonfinite_to_wire
from ..sdk.tags import canonical_tags
from ..sdk.device import (
    DeviceLoginError,
    DevicePrompt,
    OnboardingRequired,
    credentials_by_grant,
    device_authorize,
    device_login,
    hostname,
)
from ..sdk.errors import NotFoundError, UnfilteredListing
from ..sdk.filetype import artifact_kind_for, name_with_extension
from ..sdk.hashing import reference_fields
from ..sdk.snapshot import (
    DEFAULT_REFERENCE_OVER_BYTES as _SNAPSHOT_REFERENCE_OVER_BYTES,
)
from ..sdk.snapshot import UNRESOLVED_FALLBACK as _UNRESOLVED_FALLBACK
from ..sdk.surface import Surface
from . import plugin_cli, refs, statusline


# -- global connection state (set by the root callback) ---------------------
@dataclass
class Conn:
    base_url: str | None = None
    spool_dir: str | None = None
    #: Write mode asked for at the ROOT: True (--async), False (--sync), or None
    #: (neither passed). Tri-state on purpose -- False and "not passed" are
    #: different answers now that the default is async, and a plain bool cannot
    #: tell them apart.
    write_mode: bool | None = None


_conn = Conn()


#: THE WRITE-MODE PRECEDENCE, in one place. Highest wins:
#:
#:   1. the subcommand's own --sync/--async      (_resolve_write_mode's argument)
#:   2. the root --sync/--async                  (_conn.write_mode)
#:   3. PROBE_ASYNC                              ) resolved by the SDK, not here
#:   4. the default: async                       ) -- see _default_client
#:   5. the SDK's degradations (no credentials, injected transport) also apply
#:      at layer 3-4 and can turn an unforced async back into sync.
#:
#: Levels 3-5 are deliberately NOT reimplemented here. `Client.__init__` already
#: reads PROBE_ASYNC as a tri-state, defaults to async, and downgrades when
#: nothing could ever drain the journal; duplicating that would give two answers
#: that drift. The CLI resolves only what is its own (the flags), hands the SDK
#: None when neither was passed, and then READS BACK `client.async_writes` to
#: learn what was decided. One resolver, observed rather than re-derived.
def _resolve_write_mode(command_flag: bool | None) -> bool | None:
    """The caller's explicit choice, or None to let the SDK decide.

    A subcommand flag beats the root flag because that is the order a reader
    expects (`probe --async log X --sync` means "sync, and I meant it"), and
    because the root form is the one people set once for a whole session.

    Both options MUST default to None rather than False. A click/typer option
    declared with `default=False` is indistinguishable from one the user never
    typed, so a per-command default of False would silently overwrite the root
    value on every invocation -- the flag would appear to work and would in fact
    pin sync forever.
    """
    return command_flag if command_flag is not None else _conn.write_mode


def write_mode_opt() -> Any:
    """The per-subcommand `--sync/--async`, for the verbs that have both paths.

    Exists at all because `--async` was root-only, and that cost real work: a
    bulk import wrote `probe artifact add ... --async` for every manifest row and
    got "Error: No such option: --async" every time (test_backfill_enqueue_argv).
    Shipping `--sync` root-only would rebuild that trap mirrored, on the flag
    someone reaches for precisely when something has already gone wrong.

    Default None, never False -- see `_resolve_write_mode`.
    """
    return typer.Option(
        None,
        "--async/--sync",
        help="queue and return immediately (default), or --sync to block",
    )


#: Characters that mean a run ref was never going to resolve, whatever the
#: server thinks. Kept deliberately tiny.
_IMPOSSIBLE_IN_A_REF = frozenset({"/", "\\", " ", "\t", "\n"})


def _check_ref_shape(ref: str) -> None:
    """Fail a ref that CANNOT be valid, before it is queued.

    Queued writes exit 0 -- the op is on disk, and whether the server accepts it
    is not known for minutes. That is the intended trade, but it turns a typo
    from an instant non-zero exit into a dead letter nobody is watching. This
    buys back the obvious half of that for free: no network, no round trip, just
    the shapes a run ref can never have.

    Deliberately NOT a slug or UUID validator. Run refs are ids OR server-minted
    petnames (refs.py:49), the petname grammar belongs to the server, and a
    client-side guess at it would reject valid refs the day the server widens it
    -- a much worse failure than the one this prevents. Anything that could
    plausibly resolve is passed straight through.
    """
    if not ref or not ref.strip():
        raise typer.BadParameter("run ref is empty")
    if ref.startswith("-"):
        # The classic: an option typo'd or mis-ordered so the flag itself landed
        # on the positional. Queued, this becomes a 422 minutes later.
        raise typer.BadParameter(
            f"{ref!r} looks like an option, not a run ref — check the argument order"
        )
    if any(character in _IMPOSSIBLE_IN_A_REF for character in ref):
        raise typer.BadParameter(
            f"{ref!r} is not a run ref (it contains a path separator or whitespace)"
        )


# -- enums (choices) --------------------------------------------------------
# `Scope` is not redefined here: it is imported from the generated contract models,
# so `make regen` picks up a new backend scope for free instead of drifting.
class Relation(str, Enum):
    fork = "fork"
    resume = "resume"
    retry = "retry"
    branch = "branch"


class EndStatus(str, Enum):
    completed = "completed"
    failed = "failed"
    crashed = "crashed"
    canceled = "canceled"
    # 0106: uniform with the server enum (any client may set any status). The
    # honest use from a CLI is closing a run you registered but never attached
    # a live logger to -- e.g. a mirror that imported history for a run whose
    # real telemetry lives elsewhere.
    untracked = "untracked"


class RunCorrection(str, Enum):
    """What `run set --status` may record: a FINISHED run's status.

    Not the route's whole vocabulary. `created`/`running` on a finished run skip
    the reopen guard, and the reaper later marks it crashed and emails the
    launcher; `untracked` is the reaper's own verdict, not a correction.
    """

    completed = "completed"
    failed = "failed"
    crashed = "crashed"
    canceled = "canceled"


class Agg(str, Enum):
    mean = "mean"
    sum = "sum"
    min = "min"
    max = "max"
    count = "count"


class AssetMode(str, Enum):
    readonly = "readonly"
    copy = "copy"


# -- helpers ----------------------------------------------------------------
def _kv_pairs(items: list[str] | None, *, cast_float: bool = False) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for item in items or []:
        if "=" not in item:
            raise typer.BadParameter(f"expected key=value, got: {item!r}")
        key, _, raw = item.partition("=")
        if cast_float:
            try:
                out[key] = float(raw)
            except ValueError as exc:
                raise typer.BadParameter(f"metric {key!r} must be numeric, got {raw!r}") from exc
        else:
            try:
                out[key] = json.loads(raw)
            except json.JSONDecodeError:
                out[key] = raw
    return out


def _json_value(raw: str | None) -> dict | None:
    if raw is None:
        return None
    if raw.startswith("@"):
        from pathlib import Path

        raw = Path(raw[1:]).read_text()
    value = json.loads(raw)
    if not isinstance(value, dict):
        raise typer.BadParameter("expected a JSON object")
    return value


def _text_value(raw: str | None) -> str | None:
    """Free text for a `--notes` flag: literal, `@file`, or `-` for stdin.

    A caveat is prose, and prose arrives from a heredoc or a file at least as
    often as from a quoted argument -- `notes write` already reads both, and a
    run's note is the same kind of text. Passing `""` is preserved, not treated
    as absent: that is how the SDK clears a note.
    """
    if raw is None:
        return None
    if raw == "-":
        return sys.stdin.read()
    if raw.startswith("@"):
        return Path(raw[1:]).read_text()
    return raw


#: C1 controls + bidi overrides: the display-manipulation characters JSON
#: leaves raw under ensure_ascii=False. They only ever occur inside string
#: values (JSON structure is ASCII), so re-escaping them keeps the output
#: valid JSON byte-for-byte parse-equivalent.
_DISPLAY_CONTROLS = re.compile("[\u0080-\u009f\u202a-\u202e\u2066-\u2069]")


def _print_json(obj: Any) -> None:
    """One output policy for every read command.

    Pretty on a terminal, compact on a pipe — the same split `jq` and git
    resolve the same way. The audiences differ: a human scans indentation, but
    the common non-TTY reader here is a coding agent whose context window pays
    for every byte, and `indent=2` plus `\\uXXXX` escapes were measured at ~19%
    of a `project list`. Whitespace is the ONLY thing that varies by
    destination: same keys, same values either way, so piping to a file never
    changes what a script sees, only how it is laid out.

    `ensure_ascii=False` in both modes: the JSON spec is UTF-8 and stdout is;
    escaping every non-ASCII character triples its cost for no reader's
    benefit. The narrow exception is display-control characters — C1 controls
    (U+0080–U+009F, single-byte CSI on C1-interpreting terminals) and Unicode
    bidi overrides (U+202A–E, U+2066–69, visual spoofing) — which the old
    ensure_ascii=True default happened to neutralize. Those stay escaped in
    BOTH modes: server rows are multi-writer team data, and a spoofed line
    misleads an agent reading a pipe as surely as a human at a TTY. json.dumps
    already escapes C0, so this closes the set.

    None from a write this command could not deliver is not a success: it
    prints what happened to it (`{"queued": true, "count": 1, "writes": [...]}`,
    still one JSON value) instead of `null`, which reads like the answer of a
    write that landed (lineage plan L14).
    """
    if obj is None and _UNDELIVERED.total:
        obj = _UNDELIVERED.result()
    if sys.stdout.isatty():
        rendered = json.dumps(obj, indent=2, ensure_ascii=False, default=str)
    else:
        rendered = json.dumps(obj, separators=(",", ":"), ensure_ascii=False, default=str)
    rendered = _DISPLAY_CONTROLS.sub(lambda m: "\\u%04x" % ord(m.group()), rendered)
    try:
        print(rendered)
    except UnicodeEncodeError:
        # A legacy non-UTF-8 locale (latin-1, eucJP) cannot encode raw
        # non-ASCII output that ensure_ascii=True used to escape for free.
        # Fall back to full escaping rather than crash the read.
        print(json.dumps(json.loads(rendered), ensure_ascii=True, default=str))


def _select_fields(obj: Any, fields: str | None) -> Any:
    """Project a read down to the named top-level fields (comma-separated).

    The CLI-side answer to response bloat: a `--fields` flag is written ONCE
    into a skill or script and reused, so the selection is authored where a
    mistake is visible immediately — the property that makes declarative field
    selection safe here and unsafe as an MCP query language, where a model
    would re-derive it on every call.

    Applies to the object itself, or to each element of `items` when the read
    is a page envelope (`next_cursor` always survives — a projection must never
    hide that a page was a page). An unknown field is a loud 422-style error,
    never a silently-absent key: `--fields slgu` returning `{}` would read as
    "the run has no slug", which is a claim the projection has no right to make.
    """
    if not fields:
        return obj
    wanted = [f.strip() for f in fields.split(",") if f.strip()]
    if not wanted:
        # `--fields ","` parses to zero names; projecting to nothing would
        # print `{}` for every row — exactly the silent-empty answer this
        # helper exists to forbid.
        raise typer.BadParameter("--fields names no fields")

    def _pick(row: Any) -> Any:
        if not isinstance(row, dict):
            return row
        missing = [f for f in wanted if f not in row]
        if missing:
            raise typer.BadParameter(
                f"unknown field(s) {', '.join(sorted(missing))}; "
                f"this read carries: {', '.join(sorted(row))}"
            )
        return {f: row[f] for f in wanted}

    if isinstance(obj, dict) and isinstance(obj.get("items"), list):
        out = {"items": [_pick(row) for row in obj["items"]]}
        if "next_cursor" in obj:
            out["next_cursor"] = obj["next_cursor"]
        return out
    return _pick(obj)


#: The shared `--fields` option, declared once so every read spells it the same.
_FIELDS_OPTION = typer.Option(
    None,
    "--fields",
    help="only these top-level fields, comma-separated (e.g. slug,name,status)",
)


def _print_link(kind: str, entity_id: str | None) -> None:
    """Echo an entity's dashboard URL to STDERR, if there is one to echo.

    stderr, not stdout, and that is load-bearing: `run start` prints a bare id
    that callers capture (`RUN=$(probe run start ...)`), and `project create`
    prints JSON that gets piped into `jq`. A link on stdout would corrupt both.
    stderr is read by exactly the audiences this is for -- a human at a terminal
    and an agent reading combined command output -- and by no parser.

    Silent when the dashboard origin is unknown (see sdk.links): a link into the
    wrong deployment is worse than no link at all.
    """
    from ..sdk.links import entity_url

    url = entity_url(kind, entity_id)
    if url:
        typer.echo(url, err=True)


def _show_device_prompt(prompt: DevicePrompt) -> None:
    """Print the browser URL + user code for a device-flow approval. One definition,
    reused by every command that mints via the device flow (login, token, mcp).

    FLUSHED for the same reason `tui.Progress.render` is: every caller prints
    this and then blocks polling for an approval that cannot arrive until a
    human reads it. Under a pipe -- an agent's shell tool, a CI log -- an
    unflushed write stays in the buffer for the whole poll, so the caller waits
    on a human who was never shown the code, and the command looks like a hang.
    """
    print(f"  visit: {prompt.verification_uri_complete}", flush=True)
    print(f"  code:  {prompt.user_code}", flush=True)


def _new_client(**kwargs: Any) -> Client:
    """Construct a CLI-owned SDK client with bounded version telemetry."""

    # SYNC is still the default HERE, and this line is load-bearing rather than
    # leftover. It is the default for the ~129 verbs that never opted into a
    # queued path: they read the response (`_print_json(c.foo(...))` prints
    # `null` for a journaled op, because `Client.write` returns None), or they
    # read-modify-write (`probe run tag` PATCHes a whole replacement list, so a
    # queued read-your-writes gap corrupts it). Flipping the default here rather
    # than per-verb would break every one of them at once.
    #
    # The verbs that DO have a queued path use `_default_client` below, which
    # passes nothing and lets the SDK decide. `_async_client` forces async for an
    # explicit `--async`.
    kwargs.setdefault("async_writes", False)
    # A refused write FAILS (lineage plan L14). Fail-open used to catch every
    # server answer, queue it, print `null` and exit 0: a 404, a 422 or a
    # duplicate 409 read as a success nobody could act on, and the daemon's
    # logbook filed it under "Recorded". `raise_permanent` raises what can never
    # succeed later (a 4xx) and still queues what can (no answer, a 5xx, a
    # credential refused for now), which is the delivery fail-open exists for.
    # Set after construction, not passed in: a stand-in `Client` factory that
    # drops keyword arguments must not quietly drop this rule with them.
    raise_permanent = kwargs.pop("raise_permanent", True)
    client = Client(
        surface=Surface.CLI.value,
        client_headers=client_version_headers("cli", __version__),
        **kwargs,
    )
    client.raise_permanent = raise_permanent
    if raise_permanent:
        # Only a client whose refusals fail reports what it queued: the one
        # without (`probe exec`, which carries a job's run) is the SDK's, and
        # its failed writes are the delivery notices' to count. Nor may a lost
        # write there turn the job's exit code into 1 (`main`).
        client.on_undelivered = _report_undelivered
    return client


class _Undelivered:
    """This command's writes that failed and were queued (or lost), for what it
    prints (L14). Reset by the root callback for each command."""

    #: The writes kept for the printed result; the counts cover every one.
    KEPT = 32
    #: After a kind's first line, at most one more per this many seconds, with
    #: the running count (the SDK's delivery notices' rule): a long command
    #: whose every write fails says so a few times, not once per write.
    REPEAT_SECONDS = 300.0

    def __init__(self) -> None:
        self.reset()

    def reset(self) -> None:
        from collections import deque

        self.writes: "deque[dict]" = deque(maxlen=self.KEPT)
        self.queued = 0
        self.lost = 0
        self._printed_at: dict[bool, float] = {}

    @property
    def total(self) -> int:
        return self.queued + self.lost

    def add(self, entry: dict) -> int:
        """Keep `entry`; how many of its kind (queued, or lost) there are now."""
        self.writes.append(dict(entry))
        if entry.get("queued"):
            self.queued += 1
            return self.queued
        self.lost += 1
        return self.lost

    def due(self, queued: bool) -> bool:
        """May a line about this kind print now? Marks it printed when it may."""
        now = time.monotonic()
        last = self._printed_at.get(queued)
        if last is not None and now - last < self.REPEAT_SECONDS:
            return False
        self._printed_at[queued] = now
        return True

    def result(self) -> dict:
        """What a command prints in place of the `null` an undelivered write returned."""
        return {"queued": self.lost == 0, "count": self.total, "writes": [dict(e) for e in self.writes]}

    def word(self) -> str:
        """The delivery word of a write verb's success line."""
        if not self.total:
            return "delivered"
        return "queued" if not self.lost else "not delivered"


_UNDELIVERED = _Undelivered()


def _report_undelivered(entry: dict) -> None:
    """Say on STDERR that a write did not reach Probe (L14): the first of each
    kind (queued, lost) at once, then throttled (`_Undelivered.due`).

    stderr for the same reason as `_print_link`: stdout carries the JSON a
    script parses. The line's prefix is what the Probe daemon reads to file the
    command as `queued` rather than recorded (`sdk/write_outcome.py`)."""
    from ..sdk import write_outcome

    queued = bool(entry.get("queued"))
    n = _UNDELIVERED.add(entry)
    if not _UNDELIVERED.due(queued):
        return
    line = (write_outcome.queued_line if queued else write_outcome.not_queued_line)(
        str(entry.get("method")), str(entry.get("path")), str(entry.get("error")))
    if n > 1:
        line += f" ({n} writes so far)"
    typer.echo(line, err=True)


def _client(*, raise_permanent: bool = True) -> Client:
    # `Client` is a module global so the CLI package can monkeypatch it in tests.
    return _new_client(
        base_url=_conn.base_url,
        spool_dir=_conn.spool_dir,
        raise_permanent=raise_permanent,
    )


def _backfill_client() -> Client:
    """Historical imports cannot attribute their writes to this live session."""
    return _new_client(base_url=_conn.base_url, spool_dir=_conn.spool_dir, attribution="backfill")


def _journal():
    from ..sdk.journal import Journal

    return Journal(_conn.spool_dir)


def _outbox_journals() -> list:
    """This process's outbox first, then every other one of this user on this
    machine (`Journal.discover`: ``rank-*`` dirs, the ``$TMPDIR`` fallback),
    unless ``--spool-dir`` names one (plan 1.5)."""
    from ..sdk.journal import Journal

    current = _journal()
    if _conn.spool_dir:
        return [current]
    journals = [current]
    for directory in Journal.discover():
        if directory != current.dir:
            journals.append(Journal(directory))
    return journals


def _default_client(explicit: bool | None) -> Client:
    """The client for a verb that HAS a queued path, honouring `explicit`.

    `explicit` is `_resolve_write_mode`'s answer: True forces async (and keeps
    refusing without credentials -- F7), False forces sync, None hands the
    decision to the SDK, which reads PROBE_ASYNC, defaults to async, and
    degrades to sync when no credential could ever drain the journal or a
    transport was injected.

    Ask the returned client what it decided (`client.async_writes`) rather than
    re-deriving it. That is what keeps the CLI's printed outcome and the SDK's
    actual behaviour from disagreeing -- the failure mode where a command says
    "queued" and then writes synchronously, or vice versa.
    """
    if explicit is True:
        return _async_client()
    if explicit is False:
        return _client()
    return _new_client(
        base_url=_conn.base_url,
        spool_dir=_conn.spool_dir,
        async_writes=None,
    )


def _async_client() -> Client:
    """A journaling client for the async write paths (9A). Errors early when no
    deliverable credentials exist -- queueing an op nothing can ever deliver
    fails hours later in the drainer, which is the worst place to learn it."""
    from ..sdk.config import resolve

    settings = resolve(base_url=_conn.base_url)
    if not settings.token and not settings.ingest_token:
        raise typer.BadParameter(
            f"--async needs deliverable credentials: sign in ({session_marker.WIZARD_HINT}) "
            "or set PROBE_TOKEN, so the background drainer can authenticate"
        )
    return _new_client(
        base_url=_conn.base_url,
        spool_dir=_conn.spool_dir,
        async_writes=True,
    )


def _async_run(client: Client, run_ref: str):
    """A Run handle that does NOT read the run first: async enqueue must not
    block on (or fail without) the network; the server validates the ref at
    replay (eng review D20-1).

    Its writer epoch is whatever can be known OFFLINE (SDK reliability 1.10):
    the generation `run start` pinned in the bracket's lease, the same pin
    `_run_handle` applies, and otherwise none at all. It used to default to 1,
    which the server fences on any reopened run: every queued point
    dead-lettered, and a queued `run end` would have been refused."""
    from ..sdk.run import Run

    handle = Run(client, {"id": run_ref})
    try:
        from . import run_lock

        pinned = run_lock.lease_write_epoch(run_ref)
        if pinned is not None:
            handle.write_epoch = pinned
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        pass
    return handle


def _kick_drainer() -> None:
    from . import outbox_worker

    try:
        outbox_worker.maybe_spawn(_conn.spool_dir)
    except Exception:  # noqa: BLE001 -- delivery is best-effort; run end is the barrier
        pass


# Commands that must never trigger an upgrade, whatever the terminal looks like.
#
# These are the run-scoped writes a training loop makes. The TTY test alone does
# not cover them: `python train.py` started from a terminal passes its TTY down to
# every child, so `probe log` inside an interactive training run IS a TTY -- the
# check says "a human is present" in precisely the case where the hazard is worst.
#
# `exec` is here for the opposite reason: it does not run INSIDE a training loop,
# it OWNS one. It holds a run-lock flock for the wrapped process's whole life
# (see the exec command), so it is both barred from triggering and protected from
# being triggered on.
#
# Group name, not full path: Typer dispatches `probe run start` through the `run`
# group, and every subcommand under these groups is run-scoped.
_UPDATE_HOT_PATH_COMMANDS = frozenset({"log", "span", "artifact", "run", "exec", "outbox"})

#: The commands that open the setup wizard (`npx probe-research` runs `wizard`).
#: The wizard's own server call (`POST /v1/device-state`) carries the manifest
#: and refreshes the cache, so a detached refresher would be a second request
#: for the same document in the same second.
_WIZARD_COMMANDS = frozenset({"wizard", "install"})

#: How old the wizard's held server answer may be when Diagnose reports it.
_DIAGNOSE_MAX_AGE_S = 30.0


#: Root options that consume the NEXT argv token as their value. Skipping the
#: flag but not its value is how `probe --base-url URL log` resolves to "URL" --
#: which is not in the denylist, so `log` would sail through the gate it exists
#: to stop. Flags (--async, --version) take no value and must NOT be listed.
_ROOT_OPTIONS_WITH_VALUES = frozenset({"--base-url", "--spool-dir"})


def _invoked_command() -> str | None:
    """The top-level command name from argv, or None.

    Read from argv rather than a Typer context because the root callback runs
    before dispatch -- there is no command context yet.

    Conservative by construction: an unrecognized `--opt value` form returns the
    value, which is not a known command, so the denylist does not match and the
    gate falls through to the RUN LOCK. Getting this wrong costs a redundant
    lock scan, never an upgrade into a live run.
    """
    import sys as _sys

    skip_next = False
    for token in _sys.argv[1:]:
        if skip_next:
            skip_next = False
            continue
        if token.startswith("--") and "=" in token:
            continue  # --base-url=URL carries its own value
        if token in _ROOT_OPTIONS_WITH_VALUES:
            skip_next = True
            continue
        if token.startswith("-"):
            continue
        return token
    return None


def _version_notice() -> None:
    """The every-command version check: nudge from cache, refresh in background.

    Same contract as _outbox_notice below -- cheap reads, no network, never
    raises -- because it runs before every command including `probe log` inside
    training loops.

    THE GATE ORDER IS LOAD-BEARING, cheapest and most-likely-to-exit first:

        enabled?          one small read; defaults False, so an install that
                          never opted in touches exactly one file and stops
        cache fresh?      one ~150-byte read; this is where ~99.9% of calls
                          exit, which is what makes the trigger free in a loop
        (spawn refresher) detached; this process NEVER fetches inline. A 3s
                          timeout on the hot path would put a periodic stall
                          inside training loops, attributed to anything but us.
                          Not for the wizard (`_WIZARD_COMMANDS`): its own one
                          server call carries the manifest
        update available? pure comparison, no I/O
        TTY?              cheap, and wrong on its own -- see the denylist above
        denylisted?       frozenset membership
        run in flight?    LAST, because it is the only O(N) check: it scans a
                          directory and probes locks. Never reached unless an
                          upgrade would otherwise be applied right now

    A skip at any of the last three is RECORDED, so `probe doctor` can tell a box
    that is correctly deferring from an auto-updater that has silently died.
    """
    try:
        from probe import version_policy

        if not version_policy.autoupdate_enabled():
            return

        manifest, fetched_at, ok = version_policy.read_cache()
        if (
            not version_policy.cache_is_fresh(fetched_at, ok)
            and _invoked_command() not in _WIZARD_COMMANDS
        ):
            _spawn_version_refresh()

        from . import updater

        latest = isinstance(manifest, dict) and updater.cli_update_available(manifest, __version__)
        if not latest:
            # Cold cache or CLI current: nothing to apply, except a pi package
            # update a running pi deferred, which pi's session start retries.
            _retry_owed_pi_update()
            return

        from . import autoupdate

        typer.echo(
            f"probe {__version__} -> {latest} available (`probe wizard --action update`)",
            err=True,
        )

        if not sys.stdout.isatty() and not _extension_session_start():
            autoupdate.record_skip(autoupdate.SKIP_NOT_A_TTY, available=latest)
            return
        if _invoked_command() in _UPDATE_HOT_PATH_COMMANDS:
            autoupdate.record_skip(autoupdate.SKIP_HOT_PATH_COMMAND, available=latest)
            return

        from . import run_lock

        if run_lock.any_live():
            autoupdate.record_skip(autoupdate.SKIP_RUN_IN_FLIGHT, available=latest)
            return

        if _extension_session_start():
            _spawn_harness_update()
        else:
            _spawn_autoupdate()
    except Exception:  # noqa: BLE001 -- a version check must never break a command
        pass


def _retry_owed_pi_update() -> None:
    """pi's session start, with a pi package update still owed
    (`autoupdate.pi_update_pending`): spawn it, to run once pi exits. No run
    check: it touches pi's package, never the CLI a run imports from."""
    if not _extension_session_start():
        return
    from . import autoupdate

    if autoupdate.pi_update_pending():
        _spawn_harness_update()


def _extension_session_start() -> bool:
    """`probe session initialize` from an extension-family harness (pi): that
    harness's session start, the moment Claude Code's SessionStart hook updates
    from (`hooks/version_check.py`). pi has no hook, and every `probe` call its
    extension makes is off a terminal, so the TTY gate refused all of them and
    pi never auto-updated at all (2026-10-02). The update is detached and waits
    for this command to exit, exactly as it does from a terminal."""
    import sys as _sys

    from probe.harness import FAMILY_EXTENSION, get_registry

    if not hasattr(os, "fork"):
        # Windows: the update cannot detach, so it would run inline and wait
        # for this command to exit -- past the extension's 5 s budget for it.
        return False
    harness = get_registry().find(os.environ.get("PROBE_AGENT"))
    argv = _sys.argv[1:]
    return (
        harness is not None
        and harness.family == FAMILY_EXTENSION
        and _invoked_command() == "session"
        and "initialize" in argv
    )


def _capture_block(session_id: str, *, heal_cwd: str | None) -> dict:
    """The `capture` object every session surface returns.

    `heal_cwd` is None for callers that must NOT heal -- `session initialize`
    is the pi extension's own bridge, called before the extension's own spawn,
    and healing there would take the spawn away from the extension on every
    healthy session.
    """
    from probe.cli import capture_state  # noqa: PLC0415 - keeps CLI startup cheap

    healed = None
    if heal_cwd is not None:
        healed = capture_state.ensure_capture(session_id, heal_cwd)
    state = capture_state.session_capture_state(session_id)

    reason = state.reason
    # THE PROBE KNOWS WHETHER A DAEMON RUNS; ONLY THE HEAL KNOWS WHY NOT.
    # `session_capture_state` reads a pid file, so every refusal it cannot see
    # collapses to `not started` -- an ephemeral session reported a crashed
    # daemon that never existed, where the spec promises `no session file`.
    # When the heal declined for a reason in the shared vocabulary, that
    # reason is the more specific true answer, so it wins. `off` and
    # `not applicable` are deliberately NOT in that vocabulary: the first is
    # carried by `effective`, and the second is not this surface's business.
    if (
        healed is not None
        and not healed.started
        and not state.running
        and healed.reason in capture_state.REASONS
    ):
        reason = healed.reason
    return {"running": state.running, "pid": state.pid, "reason": reason}


def _effective(tracking: bool, capture: dict) -> str:
    """THREE states where the switch has two.

    `tracking` alone cannot distinguish "recording" from "says it is recording
    and nothing is listening", and that second state is the whole reason this
    field exists. The vocabulary is closed and rendered verbatim.
    """
    if not tracking:
        return "off"
    return "tracked" if capture["running"] else "tracked, not capturing session transcript"


def _ensure_capture_notice(invoked_command: str | None) -> None:
    """Start capture if tracking says one should be running. Never fails a command.

    `invoked_command` comes from the root Typer context, not argv: this runs
    before dispatch, and `_invoked_command()`'s argv scan answers for the
    PROCESS (which is `pytest` under the test runner and any wrapper in
    production), not for the command about to run.

    The `session` group is skipped because it owns its own capture decision:
    `status`, `track` and `toggle` heal with the cwd they resolved, and
    `initialize` deliberately abstains (see `_capture_block`). Firing here as
    well would both double the work and OVERRULE that abstention -- the pi
    extension calls `session initialize` immediately before its own spawn.
    """
    if invoked_command == "session":
        return
    try:
        from probe.cli import capture_state  # noqa: PLC0415
        from probe.sdk import agent_session  # noqa: PLC0415

        session_id = agent_session.session_id_from_env()
        if session_id:
            capture_state.ensure_capture(session_id, os.getcwd())
    except Exception:  # noqa: BLE001 - a heal must never break a CLI command
        pass


def _spawn_detached(argv: list[str], env: dict[str, str]) -> None:
    """Launch `argv` fully detached, leaving NO child of ours behind.

    `start_new_session=True` detaches the session but does NOT reparent: the
    process stays our child, so if we never wait for it, its exit status sits in
    the table as a zombie until we exit. That is invisible for `probe ls` and
    real for `probe exec`, which can own a training process for hours.

    So the target daemonizes -- it forks and its first stage exits immediately
    (see version_refresh.main) -- and we reap that first stage right here. The
    real work is carried by the grandchild, which init adopts.
    """
    child = subprocess.Popen(  # noqa: S603 -- our own interpreter, our own module
        argv,
        stdin=subprocess.DEVNULL,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        start_new_session=True,
        close_fds=True,
        env=env,
    )
    try:
        # The first stage forks and exits at once, so this returns immediately.
        # The timeout is a backstop, not a wait: if the fork ever fails and the
        # process runs its work inline, we abandon it rather than block a command.
        child.wait(timeout=10)
    except subprocess.TimeoutExpired:
        pass


def _spawn_version_refresh() -> None:
    """Refresh the manifest in a DETACHED child; never fetch inline.

    The invoking process must not make a network call. `PROBE_VERSION_TIMEOUT` is
    3s, so an inline fetch means one `probe log` in every TTL blocking for up to
    three seconds inside somebody's training loop -- a periodic step-time spike
    that correlates with nothing in their code. This repo has been here before:
    every run-anchored CLI write used to make a network call before the write,
    and it had to be removed.

    The cost is that this invocation compares against the OLD manifest and the
    nudge lands on the NEXT one. That is how update-notifier behaves, for the
    same reason.
    """
    from probe import version_policy

    if not version_policy.claim_refresh():
        return  # somebody is already fetching; a burst of 8 runs makes 1 request
    env = dict(os.environ)
    env[version_policy.REFRESH_OWNER_ENV] = str(os.getpid())
    try:
        _spawn_detached([sys.executable, "-m", "probe.cli.version_refresh"], env)
    except Exception:  # noqa: BLE001
        version_policy.release_refresh()


def _spawn_update(flag: str, *, harness_pid: int | None = None) -> None:
    """Launch version_refresh detached, naming OURSELVES as the pid to outlive.

    The wait is the whole point, and it is why both update triggers share this
    rather than each building the env themselves. The CLI imports lazily
    throughout, so a child that starts replacing the installed tree before this
    process exits would break the very command that spawned it.

    Raises whatever `_spawn_detached` raises; both callers are fail-open and
    swallow it, for different reasons documented at their own sites.
    """
    from . import autoupdate

    env = dict(os.environ)
    env[autoupdate.WAIT_FOR_PID_ENV] = str(os.getpid())
    if harness_pid is not None:
        env[autoupdate.WAIT_FOR_HARNESS_PID_ENV] = str(harness_pid)
    _spawn_detached([sys.executable, "-m", "probe.cli.version_refresh", flag], env)


def _spawn_harness_update() -> None:
    """Apply an update found at an extension harness's session start (pi's).

    The child waits for THAT harness (our parent: pi runs `probe session
    initialize` itself) to exit before it updates, since the update rewrites
    the package folder pi loads from; and it re-checks that an update is still
    due (`--apply-if-newer`), so several pi sessions started while one was
    pending never stack duplicate updates.
    """
    harness_pid = os.getppid()
    if harness_pid <= 1:
        # Our parent is already gone (reparented to init): there is no pi to
        # wait for, and waiting on init would hold the update for hours.
        return
    try:
        _spawn_update("--apply-if-newer", harness_pid=harness_pid)
    except Exception:  # noqa: BLE001 -- fail-open: never block the command
        pass


def _spawn_autoupdate() -> None:
    """Apply the upgrade from the root callback, where an update was found.

    `--apply` rather than `--apply-if-newer`: this path only runs after
    `_version_notice` already compared against the cached manifest, so a second
    comparison in the child would be redundant.
    """
    try:
        _spawn_update("--apply")
    except Exception:  # noqa: BLE001 -- fail-open: never block the command
        pass


def _apply_deferred_update() -> None:
    """Apply an update at the moment a run provably ended. Never raises.

    WHY THIS EXISTS. `_version_notice` finds the update and then refuses it,
    because every command a run-scoped researcher types is on
    `_UPDATE_HOT_PATH_COMMANDS`. That refusal is correct and terminal: nothing
    revisited it, so a researcher who installs via the wizard and never opens a
    new agent session never updated at all. This is the revisit.

    THE GATES, and what each one is actually for:

        enabled?      one small state-file read. Defaults False, so an install
                      that never opted in touches one file and stops.
        any_live()?   the only real safety check here. It is what stops an
                      upgrade landing on a run in ANOTHER process -- an SDK
                      training script holds an flock for its whole life.

    No TTY test, deliberately. `probe exec python train.py > train.log` has a
    non-tty stdout, and that is the shape this fix exists to reach; reusing
    `_version_notice`'s TTY gate here would defeat it silently. Nothing is lost:
    the hazard the TTY test proxies for is a live run, which `any_live()` answers
    directly, and `perform_update` re-checks it again in the child.

    No cache read and no comparison, also deliberately. After a multi-hour run
    the cached manifest is always stale, and refreshing it here would mean
    blocking the command. The child fetches and decides instead
    (`version_refresh --apply-if-newer`).

    THE GUARD IS NOT DECORATION. The exec call site is inside a `finally`, so an
    exception raised here replaces whatever was already propagating -- turning a
    clean run into a traceback, or masking the KeyboardInterrupt from a Ctrl-C'd
    training run. `probe exec` exists to hand back its child's exit code.
    """
    try:
        from probe import version_policy

        if not version_policy.autoupdate_enabled():
            return

        from . import run_lock

        if run_lock.any_live():
            return

        _spawn_update("--apply-if-newer")
    except Exception:  # noqa: BLE001 -- see docstring: must never break the command
        pass


def _outbox_notice() -> None:
    """The every-command outbox banner (2B) + drainer re-kick (3A).

    One stat/read of status.json, no locks, never raises: this runs before
    every command, including `probe log` inside training loops.
    """
    try:
        from ..sdk.journal import Journal, auth_blocked_since

        status = Journal.read_status(_conn.spool_dir)
        if not status:
            return
        failed = status.get("failed") or 0
        pending = status.get("pending") or 0
        blocked = auth_blocked_since(status)
        parts: list[str] = []
        if blocked:
            parts.append(f"auth-blocked since {blocked} — sign in again ({session_marker.WIZARD_HINT})")
        if failed:
            parts.append(f"{failed} dead-lettered")
        if parts or (pending and status.get("paused")):
            if pending:
                parts.append(f"{pending} pending")
            if status.get("paused"):
                parts.append("paused")
            typer.echo(f"outbox: {'; '.join(parts)} — see `probe outbox status`", err=True)
            # Same condition as the banner, on purpose: whatever is worth
            # interrupting a human for is worth the fleet knowing. This is the
            # only place the STANDING condition is ever observed. A worker
            # already running reports the TRANSITION into paused/auth-blocked
            # (outbox_worker exit codes 4 and 3), but `maybe_spawn` will not fork
            # again while either persists -- so without this, a queue that has
            # been wedged since yesterday is reported by nobody. Rate-limited to once per
            # STUCK_REPORT_INTERVAL_S so a training loop shelling out thousands
            # of times still costs one event.
            #
            # Its OWN try/except, inside the function's: emit_outbox_stuck never
            # raises, but the import can, and a telemetry failure that skipped
            # the _kick_drainer() below would turn reporting a stuck queue into
            # causing one.
            try:
                from ..sdk.config import resolve
                from . import telemetry as telemetry_mod

                # The RESOLVED backend, not the config file: `probe --base-url
                # https://probe.internal.corp ...` lives on `_conn.base_url` and
                # never reaches the config, so gating on the config alone let a
                # self-host invocation emit. Only reached when the queue is
                # actually stuck, so the resolve() is off the hot path.
                telemetry_mod.emit_outbox_stuck(
                    status,
                    spool_dir=_conn.spool_dir,
                    base_url=resolve(base_url=_conn.base_url).base_url,
                )
            except Exception:  # noqa: BLE001 -- never let a report block the kick
                pass
        if pending and not status.get("paused") and not blocked:
            _kick_drainer()
    except Exception:  # noqa: BLE001 -- a broken banner must never break a command
        pass


def run_lock_touch_lease(run_id: str, *, write_epoch: int | None = None) -> None:
    """Best-effort lease write; the lease tier must never break the command."""
    try:
        from . import run_lock

        run_lock.touch_lease(run_id, write_epoch=write_epoch)
    except Exception:  # noqa: BLE001
        pass


#: Launchers that SUBMIT and return, keyed by (binary, subcommand). The
#: subcommand is load-bearing: `modal run` BLOCKS until the job finishes while
#: `modal deploy` returns as soon as the app is published, and `ray job submit`
#: returns while a bare `ray ...` may not. Keying on the binary alone sent
#: `modal run` -- the single most common real invocation -- down the hand-off
#: path, where its real exit code was thrown away.
#:
#: `None` as the subcommand means "any", for binaries that always submit.
_SUBMIT_LAUNCHERS: dict[tuple[str, str | None], str] = {
    ("sbatch", None): "sbatch --export=ALL,PROBE_RUN_ID={run_id},PROBE_RUN_EPOCH={epoch} ...",
    (
        "modal",
        "deploy",
    ): 'modal: secrets=[modal.Secret.from_dict({{"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}", "PROBE_API_KEY": ...}})]',
    (
        "ray",
        "submit",
    ): 'ray: runtime_env={{"env_vars": {{"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}}}',
    (
        "ray",
        "job",
    ): 'ray: runtime_env={{"env_vars": {{"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}}}',
    ("kubectl", "apply"): "kubectl: env: PROBE_RUN_ID={run_id}, PROBE_RUN_EPOCH={epoch}",
    ("kubectl", "create"): "kubectl: env: PROBE_RUN_ID={run_id}, PROBE_RUN_EPOCH={epoch}",
}

#: `--launcher NAME` override, for a wrapper this cannot see through.
_LAUNCHER_ALIASES: dict[str, tuple[str, str | None]] = {
    "sbatch": ("sbatch", None),
    "slurm": ("sbatch", None),
    "modal": ("modal", "deploy"),
    "ray": ("ray", "job"),
    "kubectl": ("kubectl", "apply"),
}


def _launcher_name(argv: list[str]) -> str:
    """The launcher `argv` actually invokes, unwrapping the usual prefixes.

    Matching argv[0] alone misses exactly the forms people write: `python -m
    modal run`, `uv run modal run`, `uvx modal run`. The hint that depends on
    this exists FOR those cases, so the detection has to see through them.
    """
    i = 0
    while i < len(argv):
        base = os.path.basename(argv[i]).lower()
        if base in {"uv", "uvx", "poetry", "pdm", "hatch"} and i + 1 < len(argv):
            i += 1
            if os.path.basename(argv[i]).lower() in {"run", "tool"}:
                i += 1
            continue
        if base in {"python", "python3"} and i + 2 < len(argv) and argv[i + 1] == "-m":
            i += 2
            continue
        return base
    return os.path.basename(argv[0]).lower() if argv else ""


def _launcher_key(argv: list[str]) -> tuple[str, str | None]:
    """(binary, first subcommand) after unwrapping, both lowercased."""
    name = _launcher_name(argv)
    rest = [a for a in argv if os.path.basename(a).lower() == name]
    idx = argv.index(rest[0]) if rest else 0
    sub = None
    for token in argv[idx + 1 :]:
        if not token.startswith("-"):
            sub = os.path.basename(token).lower()
            break
    return name, sub


def _submit_template(argv: list[str]) -> str | None:
    key = _launcher_key(argv)
    return _SUBMIT_LAUNCHERS.get(key) or _SUBMIT_LAUNCHERS.get((key[0], None))


def _forwarding_hint(argv: list[str], run_id: str, epoch: int) -> str | None:
    """The line that makes a remote job reachable, or None.

    `PROBE_RUN_ID` does not cross a machine boundary on its own: Modal does not
    forward local env, Ray workers do not inherit the submitter's, Slurm needs
    --export. Printing the exact incantation is cheaper than the researcher
    discovering it from an empty run three hours later. Advisory: never a gate.
    """
    tmpl = _submit_template(argv)
    return tmpl.format(run_id=run_id, epoch=epoch) if tmpl else None


def _is_submit_launcher(argv: list[str]) -> bool:
    return _submit_template(argv) is not None


def _run_handle(client: Client, run_id: str, *, owns_process: bool = False):
    """A handle for a run-scoped CLI write.

    `owns_process` (0205) splits the two very different things this returns.

    The DEFAULT is the lease tier: `probe log`, `probe artifact`, `probe run
    set` -- one short write inside a detached `run start`...`run end` bracket
    with no process of ours alive in between. Such a handle must not beat: it
    would assert ownership for a second and then go silent, and the reaper reads
    that as a process that died.

    `owns_process=True` is the flock tier: `probe exec`, which lives for exactly
    as long as the child it wraps. That process CAN honestly beat for the run's
    whole life, and before 0205 it did not -- so a wrapped child that logged
    nothing for fifteen minutes was reaped mid-flight, which is the failure the
    wrapper existed to prevent. Its beats carry no `attached` flag: holding a
    run open is not the same as the job inside it reporting.
    """
    from ..sdk.run import Run

    # Every run-scoped CLI write funnels through here, which makes it the one
    # place a detached run's auto-update lease can be renewed without anyone
    # having to remember to. A bare `probe run start` ... `probe run end`
    # bracket has no process of ours alive in between, so its claim on the box
    # is a lease -- and this is the traffic that keeps it alive.
    #
    # No-ops for a run holding an flock (SDK, `probe exec`) and skips the write
    # until the lease is half spent, so `probe log` in a training loop does not
    # pay for it. See run_lock.renew_lease_if_stale.
    try:
        from . import run_lock

        run_lock.renew_lease_if_stale(run_id)
    except Exception:  # noqa: BLE001 -- a lock refresh must never break a write
        pass
    if owns_process:
        # Through the SDK's construction boundary so the beat thread, the
        # process-bound flock and the finalizer all come with it.
        handle = client.attach_run(run_id, heartbeat=True, attached=False)
    else:
        handle = Run(client, client.get_run(run_id))
    try:
        from . import run_lock

        # A live lease pins the bracket's writer generation (0185): stamp the
        # epoch `run start` opened under, not the row's current one, so a
        # bracket superseded by a reopen elsewhere fences instead of splicing.
        pinned = run_lock.lease_write_epoch(run_id)
        if pinned is not None:
            handle.write_epoch = pinned
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        pass
    return handle


def _apply_tag_ops(
    current: list[str],
    add: list[str],
    remove: list[str],
    replace: list[str] | None,
) -> list[str]:
    """Compute a ``tag`` verb's replacement list (read-modify-write over the
    server's whole-list-replace PATCH, CONTRACT.md "tags"). ``--set`` wins
    outright; otherwise positional adds append (canonical, deduped) and
    ``--remove`` drops. The same tag in add AND remove is a caller bug — error,
    never a silent tie-break."""
    if replace is not None:
        if add or remove:
            raise typer.BadParameter("--set replaces outright; don't combine it with adds/--remove")
        return canonical_tags(replace)
    add_c = canonical_tags(add)
    remove_c = set(canonical_tags(remove))
    both = [t for t in add_c if t in remove_c]
    if both:
        raise typer.BadParameter(f"tag(s) both added and removed: {', '.join(both)}")
    out = [t for t in canonical_tags(current) if t not in remove_c]
    out.extend(t for t in add_c if t not in out)
    return out


def _tag_flags_given(add, remove, replace) -> bool:
    """Did a `set` verb get any of --add-tag/--remove-tag/--set-tags?"""
    return bool(add) or bool(remove) or replace is not None


def _set_verb_tags(current, add, remove, replace) -> tuple[list[str], bool]:
    """The tag list a `set` verb sends beside its other fields, and whether it
    differs from the stored one -- the `tag` verb's arithmetic, one write.

    The list goes in the body whenever a tag flag was given, changed or not:
    a retried command (the daemon's Idempotency-Key) then sends the same body
    it sent the first time and replays instead of being refused as a
    different request."""
    if replace is not None and (add or remove):
        raise typer.BadParameter(
            "--set-tags replaces the whole list; don't combine it with --add-tag/--remove-tag"
        )
    stored = list(current or [])
    wanted = _apply_tag_ops(stored, add or [], remove or [], replace)
    return wanted, wanted != stored


def _tag_verb_flow(entity_id, current, add, remove, replace, write) -> dict:
    """Shared flow for the three ``tag`` verbs: bare invocation lists, anything
    else is read-modify-write. The changed-check compares against the RAW
    stored list (not its canonical form) so re-tagging a pre-0066 row with its
    own canonical name still writes once and heals the stored form; the write
    callbacks verify the server actually persisted tags (0066 guard)."""
    current = list(current or [])
    if not add and not remove and replace is None:
        return {"id": entity_id, "tags": current}
    wanted = _apply_tag_ops(current, add or [], remove or [], replace)
    if wanted == current:
        return {"id": entity_id, "tags": current}
    result = write(wanted) or {}
    return {"id": result.get("id", entity_id), "tags": result.get("tags", wanted)}


def _version_cb(value: bool) -> None:
    if value:
        typer.echo(f"probe {__version__}")
        raise typer.Exit()


# Typer vendors its own click (`typer._click`, since 0.13). The standalone `click`
# package is a DIFFERENT module object, so `except click.ClickException` matched
# nothing typer raises and every usage error escaped main() as a traceback instead of
# an exit code — silently, on an unpinned typer bump.
#
# `typer.Exit`/`typer.Abort` are public re-exports of whichever click typer uses.
# ClickException — the base of every usage error (BadParameter, NoSuchOption,
# UsageError, ...) — is not re-exported, but it is reachable from BadParameter's MRO
# under either layout, so resolving it here follows typer rather than pinning to one.
ClickException = next(
    (base for base in typer.BadParameter.__mro__ if base.__name__ == "ClickException"),
    # Never expected; the fallback keeps `import probe.cli` working (a StopIteration at
    # import time would make the whole CLI unusable) and degrades to catching nothing.
    type("_NoClickException", (Exception,), {}),
)


# -- app --------------------------------------------------------------------
app = typer.Typer(
    name="probe",
    no_args_is_help=True,
    add_completion=False,
    help=(
        "Probe Research CLI. Run/event/artifact commands upload experiments; "
        "the `hook` group is reserved for deterministic coding-agent adapters."
    ),
)


@app.callback()
def _root(
    ctx: typer.Context,
    base_url: str = typer.Option(None, "--base-url"),
    spool_dir: str = typer.Option(
        None, "--spool-dir", help="outbox journal directory (or PROBE_OUTBOX_DIR)"
    ),
    write_mode: Optional[bool] = typer.Option(
        None,
        "--async/--sync",
        help="queue data writes to the local outbox and return immediately, or "
        "--sync to block until the server answers. Queueing is the DEFAULT for "
        "`log`, `span add` and RUN-anchored `artifact add`; PROBE_ASYNC=0 turns "
        "it off for those. `run end` is the delivery barrier and BLOCKS unless "
        "you pass --async. Every other command is always synchronous. Also "
        "accepted AFTER the subcommand, where it wins.",
    ),
    version: bool = typer.Option(
        False, "--version", callback=_version_cb, is_eager=True, help="show version"
    ),
) -> None:
    # Credentials come from named contexts (`probe login`) or the PROBE_TOKEN /
    # PROBE_INGEST_TOKEN / PROBE_BASE_URL env vars. The old --token/--ingest-token/
    # --hmac-secret overrides were removed (v0.23.0): a secret in argv leaks into
    # shell history and `ps`, and a detached outbox drain could never resolve it.
    _conn.base_url = base_url
    _conn.spool_dir = spool_dir
    # One command's undelivered writes, never a previous one's (in-process
    # callers and tests run several commands in one interpreter).
    _UNDELIVERED.reset()
    # Store the flag VERBATIM, including None for "neither was passed". PROBE_ASYNC
    # is deliberately not read here: `Client.__init__` already parses it as a
    # tri-state (on / off / unrecognised-warns-and-defers) and a second parser
    # here would be a second answer to the same question. See the precedence
    # table above `_resolve_write_mode`.
    _conn.write_mode = write_mode
    _outbox_notice()
    # The CLI's own auto-update trigger. Before this existed, auto-update fired
    # from exactly one place -- the Claude Code plugin's SessionStart hook -- so a
    # user who never started a session never updated, and a headless box never
    # updated at all. Both of these are read-only-and-spawn on the fast path; see
    # _version_notice for why its gate order is what it is.
    _version_notice()
    # Trigger surface B: the one place that runs exactly once per CLI
    # invocation. NOT transport.py's `agent_session_headers()`, which fires
    # per HTTP request and would ask this question many times per command.
    # Bounded internally to one spawn attempt per session per ten minutes.
    _ensure_capture_notice(ctx.invoked_subcommand)


# -- auth -------------------------------------------------------------------
def _finish_website_onboarding(exc: OnboardingRequired) -> None:
    from probe.cli import tui

    # Through `tui.final`: this is the run's last word, and inside the
    # wizard's window a plain print would close with the window.
    if exc.onboarding_url:
        tui.final(f"Complete onboarding on {exc.onboarding_url} first.")
    else:
        tui.final(str(exc))
    tui.final("Then run the install command shown there.")
    raise typer.Exit(0)


@app.command()
def login(
    base_url: str = typer.Option(None, "--base-url"),
    token: str = typer.Option(None, "--token"),
    ingest_token: str = typer.Option(None, "--ingest-token"),
    hmac_secret: str = typer.Option(None, "--hmac-secret"),
    device: bool = typer.Option(
        True,
        "--device/--endpoint-only",
        help="browser-assisted login (the default); --endpoint-only saves the endpoint without minting a token",
    ),
    context: str = typer.Option(
        None, "--context", help="name the context to create or overwrite (default: the active one)"
    ),
) -> None:
    """Log in. Bare ``probe login`` runs the browser handoff (RFC 8628) — approve
    in the dashboard, no token to see or paste.

    Pass ``--token probe_pat_...`` for the air-gap paste path, or
    ``--endpoint-only`` to just save ``--base-url`` without minting a token.

    ``--context staging`` logs in under a named context instead of the active one,
    so several endpoints or tenants can coexist on one machine.
    """
    _login(
        base_url=base_url,
        token=token,
        ingest_token=ingest_token,
        hmac_secret=hmac_secret,
        device=device,
        context=context,
    )


def _login(
    *,
    base_url: str | None,
    token: str | None,
    ingest_token: str | None,
    hmac_secret: str | None,
    device: bool,
    context: str | None,
    open_browser: bool = True,
) -> None:
    """Sign this machine in, and ONLY that: no plugin, capture or rule is touched.

    `probe wizard --action login` with its sign-in flags (a remote GPU box, a
    self-hosted server, an air-gapped paste) and, until it is deleted, `probe
    login`. `device=False` saves the endpoint without minting a token.
    """
    resolved_token = token
    base = base_url or _conn.base_url

    if device and not resolved_token:
        endpoint = resolve(base_url=base).base_url
        print(f"opening {endpoint} for browser approval…" if open_browser
              else f"approve this device at {endpoint}…")

        try:
            resolved_token = device_login(endpoint, on_prompt=_show_device_prompt, open_browser=open_browser)
        except OnboardingRequired as exc:
            _finish_website_onboarding(exc)
        except DeviceLoginError as exc:
            print(f"device login failed: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc

    settings = resolve(
        base_url=base,
        token=resolved_token,
        ingest_token=ingest_token,
        hmac_secret=hmac_secret,
        context=context,
    )
    # None means "leave whatever is already there" in save_context, so an --endpoint-only
    # login never clears a token the user still has.
    updates = {
        "base_url": settings.base_url,
        "token": settings.token or None,
        "ingest_token": settings.ingest_token or None,
        "hmac_secret": settings.hmac_secret or None,
    }
    if settings.token:
        with _new_client(settings=settings) as c:
            who = c.me()
        print(f"logged in to {settings.base_url} as {who.get('email', who)}")
        # Which account this login is, bound to its token (#2041 review): a
        # write queued under it may later go out with a NEWER login of this
        # context only if that login is the same account. None clears a
        # previous login's record.
        from ..sdk.journal import credential_fingerprint, record_account

        # The login this one replaces keeps its record where writes queued under
        # it can still find it (#2041 round 3): the context holds one identity.
        previous = load_context(context).get("identity")
        if isinstance(previous, dict) and previous.get("fingerprint"):
            record_account(
                str(previous["fingerprint"]),
                (previous.get("customer_id"), previous.get("user_id")),
            )
        if isinstance(who, dict) and who.get("customer_id") and who.get("user_id"):
            record_account(
                credential_fingerprint(settings.token, settings.ingest_token),
                (str(who["customer_id"]), str(who["user_id"])),
            )
        updates["identity"] = (
            {
                "fingerprint": credential_fingerprint(settings.token, settings.ingest_token),
                "customer_id": str(who["customer_id"]),
                "user_id": str(who["user_id"]),
            }
            if isinstance(who, dict) and who.get("customer_id") and who.get("user_id")
            else None
        )
    else:
        print(f"saved endpoint {settings.base_url} (no user token set)")
    if context:
        use_context(context)
    path = save_context(updates, name=context)
    print(f"config: {path} (context: {context or current_context_name()})")
    if settings.token:
        # Fresh credentials un-block the outbox: forget any recorded 401/403
        # and wake the drainer so queued writes deliver without further steps.
        try:
            journal = _journal()
            journal.clear_auth_block()
            _kick_drainer()
        except Exception:  # noqa: BLE001 -- login must not fail on outbox hygiene
            pass


@app.command()
def logout() -> None:
    """Stop imports, revoke the calling token, and clear local config."""
    _clear_wizard_imports()
    try:
        with _client() as c:
            c.logout()
        print("token revoked")
    except errors.RosError as exc:
        print(f"revoke skipped ({exc})", file=sys.stderr)
    # The ACTIVE context only. Deleting the whole file would sign the user out of every
    # other endpoint they have configured, which is not what "logout" means.
    name = current_context_name()
    clear_context(name)
    print(f"local config cleared (context: {name})")


@app.command()
def whoami() -> None:
    """Show the current principal."""
    with _client() as c:
        _print_json(c.me())


@app.command()
def backfill(
    folder: str = typer.Argument(None, help="folder to import; omit to pick one interactively"),
    agent: str = typer.Option(
        None,
        "--agent",
        # pi is no longer named: it was here only because the transcripts lane
        # would take it to write summaries, and that lane is gone. The folder
        # importer refuses it -- `resolve_agent` explains why (no shell, so
        # `probe artifact add` has nowhere to run) -- so no lane accepts it now.
        help="claude | codex — omit to use whichever is installed, or be asked",
    ),
    project: str = typer.Option(
        None,
        "--project",
        help="import into this existing project; omit to review proposed projects",
    ),
    source_id: str = typer.Option(
        None,
        "--source-id",
        help="resume a saved source after moving its folder, within the same destination scope",
    ),
    import_changed: bool = typer.Option(
        False,
        "--import-changed",
        help="review changed content for import; may create new artifact identities",
    ),
    import_unverified: bool = typer.Option(
        False,
        "--import-unverified",
        help="review unresolved legacy paths for import after reading the reconciliation report",
    ),
    retry_dead: bool = typer.Option(
        False, "--retry-dead", help="plan files again that failed every attempt on an earlier run"
    ),
    transcripts: bool = typer.Option(
        None,
        "--transcripts/--no-transcripts",
        help="also import this machine's agent sessions (interactive: asked at a gate)",
    ),
    transcripts_only: bool = typer.Option(
        False,
        "--transcripts-only",
        help="import ONLY this machine's agent sessions; read no folder",
    ),
    transcripts_budget_mb: int = typer.Option(
        None, "--transcripts-budget-mb", help="stop after roughly this many MB of sessions"
    ),
) -> None:
    """Import work you have already done: point an agent at a folder.

    It uploads what it finds, describes each artifact, and reports how much of
    the folder it accounted for. Large files (checkpoints, datasets) are
    recorded as references, not copied.

    This is the command the dashboard hands you: `npx probe-research backfill`
    forwards straight here. The same thing is in `probe wizard` under
    `Import research work`.
    """
    from pathlib import Path

    from probe.cli import backfill as backfill_impl
    from probe.cli import setup as wizard
    from probe.cli import tui

    # BEFORE anything else, and for a stronger reason than the wizard has:
    # `npx probe-research backfill` reaches us through an EPHEMERAL `uv tool
    # run` / `pipx run`, and the agent we are about to launch does its work by
    # shelling out to `probe artifact add`. With no persistent binary on PATH
    # every one of those calls fails, so the agent reads the whole folder and
    # lands nothing.
    from probe.cli.bootstrap import ensure_persistent_install

    try:
        chosen = backfill_impl.Agent(agent) if agent else None
    except ValueError:
        raise typer.BadParameter(
            f"unknown agent {agent!r}; expected one of: "
            f"{', '.join(a.value for a in backfill_impl.Agent)}"
        ) from None

    from probe.cli import telemetry as telemetry_mod

    # Pre-bootstrap, like the wizard's `wizard.invoked` (D7/R4): this is the
    # command the dashboard hands out via npx, and a bootstrap death must
    # still enter the funnel.
    tel = telemetry_mod.TelemetryContext.start(
        via=telemetry_mod.Via.COMMAND,
        interactive=wizard.interactive(),
        base_url=resolve(base_url=_conn.base_url).base_url,
    )
    tel.emit(
        telemetry_mod.EVENT_BACKFILL_INVOKED,
        interactive=wizard.interactive(),
    )

    boot = ensure_persistent_install()
    if boot.message:
        print(boot.message)

    # Typer fills these in only when it PARSES the argv. Called directly --
    # which the tests do, and which `--action backfill` effectively does -- the
    # declared defaults arrive as OptionInfo sentinels, so anything that
    # computes with them has to normalise first or multiply a sentinel by 1024.
    budget_mb = transcripts_budget_mb if isinstance(transcripts_budget_mb, int) else None
    budget = budget_mb * 1024 * 1024 if budget_mb else None
    only_transcripts = transcripts_only is True

    # THE DEFAULT DIFFERS BY MODE, deliberately. Interactively the lane offers
    # itself at its own gate, so an unset flag means "ask". Headlessly there is
    # no gate and no one to ask, and uploading a machine's conversation history
    # because a script ran is exactly the scope change this feature exists to
    # make deliberate -- so it stays OFF unless the flag says otherwise.
    want_transcripts = transcripts if isinstance(transcripts, bool) else wizard.interactive()

    if only_transcripts:
        from probe.cli import backfill_transcripts as transcripts_mod

        # NO AGENT IS RESOLVED HERE ANY MORE. This lane used to pick a local
        # coding agent to write summaries with; the digest lane was retired
        # server-side, so the lane uploads and nothing else, and `--agent` is
        # the folder importer's alone.
        lines = transcripts_mod.run_lane(
            client=_backfill_client(),
            interactive=wizard.interactive(),
            budget_bytes=budget,
        )
    else:
        lines = backfill_impl.run(
            client_factory=_backfill_client,
            folder=Path(folder) if folder else None,
            project=project,
            interactive=wizard.interactive(),
            agent=chosen,
            telemetry=tel,
            transcripts=want_transcripts,
            transcripts_budget=budget,
            source_id=source_id if isinstance(source_id, str) else None,
            import_changed=import_changed is True,
            import_unverified=import_unverified is True,
            retry_dead=retry_dead is True,
        )
    if lines:
        tui.page(lines) if wizard.interactive() else print("\n".join(lines))


# `probe update` is HIDDEN, not deleted. The plugin's SessionStart hook spawns
# it, and plugins update on the USER's schedule -- deleting it would silently
# break auto-update on every machine whose plugin has not been refreshed yet.
# New plugin versions call `probe wizard --action update` instead.
@app.command(name="update", hidden=True)
def update_compat(
    check: bool = typer.Option(False, "--check"),
    yes: bool = typer.Option(False, "--yes", "-y"),
    plugin: bool = typer.Option(True, "--plugin/--no-plugin"),
    channel: str = typer.Option(None, "--channel", hidden=True),  # noqa: ARG001 - ignored
) -> None:
    """Deprecated: use `probe wizard` and pick Update."""
    from probe.cli import updater
    from probe.cli.upgrading import perform_update

    base = resolve(base_url=_conn.base_url).base_url
    if check:
        from probe.cli import versions as versions_mod

        try:
            manifest = updater.fetch_latest(base)
        except Exception as exc:  # noqa: BLE001
            print(f"update check failed: {exc}", file=sys.stderr)
            raise typer.Exit(updater.CHECK_ERROR) from exc
        # EVERY component, not just the CLI. This check reported on the CLI alone
        # while the manifest had published `plugin` and `tap` floors for months,
        # so a researcher could run it, read "up to date", and be two months
        # behind on the plugin that does the actual capturing. The exit codes are
        # unchanged -- BEHIND if anything is behind -- because scripts read them.
        rows = versions_mod.compare(manifest)
        for line in versions_mod.render(rows):
            print(line.strip())
        if any(row.behind for row in rows):
            raise typer.Exit(updater.CHECK_BEHIND)
        raise typer.Exit(updater.CHECK_CURRENT)

    from probe.cli import tui

    with tui.working("Updating the CLI and plugins"):
        outcome = perform_update(base_url=base, include_plugin=plugin)
    for line in outcome.lines:
        print(line)
    if outcome.restart_needed:
        print("\nRestart Claude Code to apply the plugin update.")
    raise typer.Exit(0 if outcome.ok else 1)


@app.command()
def doctor() -> None:
    """Read-only diagnostic: what is installed, on, and whether auto-update works.

    Prints the LAST UPDATE ATTEMPT, which is the only way to notice a detached
    auto-updater that has been silently failing.
    """
    # Imported inside the body, not at module scope: cli/__init__ eagerly loads
    # this module, and `probe log` runs inside training loops.
    from probe.cli import doctor as doctor_impl

    print(doctor_impl.render(doctor_impl.collect()))


@app.command(name="install")
def install(
    agent: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--agent",
        help="configure claude, codex, pi, kimi, or both (both = claude+codex; default: choose interactively)",
    ),
    tracking: Optional[bool] = typer.Option(  # noqa: UP007
        None, "--tracking/--no-tracking", help="research tracking skills + read-only MCP search"
    ),
    capture: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--capture/--no-capture",
        help="stream the selected coding agents' sessions to the knowledgebase",
    ),
    auto_update: Optional[bool] = typer.Option(  # noqa: UP007
        None, "--auto-update/--no-auto-update", help="keep the CLI and plugins current"
    ),
    agent_rules: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--agent-rules/--no-agent-rules",
        help="managed Probe block in each selected agent's global instructions",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the prompts"),
    auth_code: str = typer.Argument(
        None, help="one-time 10-character sign-in code from the website"
    ),
) -> None:
    """Set Probe Research up on this device — straight into the guided install.

    `probe wizard` opens on the action menu, which is right when you do not know
    what you want yet and wrong when you do. `npx probe-research install` is the
    sentence someone types when they have already decided, and the launcher
    forwards its arguments verbatim -- so the verb has to exist HERE or it
    reaches typer as an unknown command and exits 2.

    Deliberately a thin alias over `wizard --action configure` rather than its
    own copy of the flow. The install steps, the shared authorization and the
    per-agent apply loop are subtle enough that a second entry point into a
    second implementation is how the two drift.
    """
    wizard(
        agent=agent,
        tracking=tracking,
        capture=capture,
        auto_update=auto_update,
        agent_rules=agent_rules,
        channel=None,
        uninstall=False,
        action="configure",
        folder=None,
        yes=yes,
        experimental=False,
        # Called as a function, so every option is named: an omitted one is a
        # truthy `typer.Option` default, not None.
        token=None,
        base_url=None,
        context=None,
        ingest_token=None,
        hmac_secret=None,
        endpoint_only=False,
        no_browser=False,
        who_records=None,
        auth_code=auth_code,
    )


def _clear_wizard_imports() -> None:
    from probe.cli import import_jobs, tui

    try:
        import_jobs.clear_all()
    except (import_jobs.JobError, OSError) as exc:
        tui.say(f"Could not clear imports: {exc}")
        raise typer.Exit(1) from exc


def _exit_wizard() -> None:
    """Leave the terminal UI; approved imports keep their detached workers."""
    raise typer.Exit(0)


@app.command(name="wizard")
def wizard(
    agent: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--agent",
        help="configure claude, codex, pi, kimi, or both (both = claude+codex; default: choose interactively)",
    ),
    tracking: Optional[bool] = typer.Option(  # noqa: UP007 - typer needs Optional
        None,
        "--tracking/--no-tracking",
        help="research tracking skills + read-only MCP search",
    ),
    capture: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--capture/--no-capture",
        help="stream the selected coding agents' sessions to the knowledgebase",
    ),
    auto_update: Optional[bool] = typer.Option(  # noqa: UP007
        None, "--auto-update/--no-auto-update", help="keep the CLI and plugins current"
    ),
    agent_rules: Optional[bool] = typer.Option(  # noqa: UP007
        None,
        "--agent-rules/--no-agent-rules",
        help="managed Probe block in each selected agent's global instructions",
    ),
    channel: str = typer.Option(  # noqa: ARG001 - compat, see below
        None,
        "--channel",
        hidden=True,
        help="accepted and ignored; there is only one channel",
    ),
    uninstall: bool = typer.Option(
        False,
        "--uninstall",
        help="when turning capture off, also remove the plugin (default: keep it)",
    ),
    action: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--action",
        # Every value here is an `Action`, spelled the way the enum spells it.
        # It used to advertise `remove`, which is not one -- so the flag the
        # help text recommended for an unattended uninstall exited 2.
        help=(
            "skip the menu: recorder | defaults | configure | account | login | logout | settings | "
            "uninstall | import-research | backfill | transcripts | imports | update | diagnose | manual"
        ),
    ),
    folder: str = typer.Option(
        None,
        "--folder",
        help="backfill only: the folder to import, skipping the picker (needed headless)",
    ),
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the menu and prompts"),
    experimental: bool = typer.Option(
        False,
        "--experimental",
        hidden=True,
        help="no longer needed: Defaults › Who records is on the main menu for every team",
    ),
    token: str = typer.Option(
        None, "--token", help="login: sign in with this token, no browser (a remote or air-gapped machine)"
    ),
    base_url: str = typer.Option(None, "--base-url", help="login: the Probe server to sign in to (self-host)"),
    context: str = typer.Option(
        None, "--context", help="login: the saved account to create or overwrite (default: the active one)"
    ),
    ingest_token: str = typer.Option(None, "--ingest-token", help="login: the capture token to save with it"),
    hmac_secret: str = typer.Option(None, "--hmac-secret", help="login: the self-host HMAC secret to save with it"),
    endpoint_only: bool = typer.Option(
        False, "--endpoint-only", help="login: save --base-url without signing in"
    ),
    no_browser: bool = typer.Option(
        False, "--no-browser", help="login: print the approval link instead of opening a browser"
    ),
    who_records: str = typer.Option(
        None, "--who-records", help="recorder: agent | daemon, for every coding agent on this device"
    ),
    auth_code: str = typer.Argument(
        None, help="one-time 10-character sign-in code from the website"
    ),
) -> None:
    """Setup wizard: install and configure Probe Research on this device.

    Interactive by default. Every capability is also a flag, and THE FLAGS ARE
    THE CONTRACT -- the menu is a front end over them. An omitted flag preserves
    whatever is already configured, so `--yes` in CI can never silently revoke
    someone's capture pairing.
    """
    from probe.cli import capture as capture_mod
    from probe.cli import tui

    # D4: a sign-in from before D3 may have left pi's capture off for good.
    capture_mod.clear_stray_pi_killswitch()

    # `--experimental` gated the Who records rows until 0.204.1; still
    # accepted so a script or a habit that passes it keeps working.
    del experimental

    # First, so `--who-records` with a sign-in flag is refused below like any
    # other action rather than signing in and never switching.
    if who_records is not None:
        if who_records not in session_marker.RECORDERS:
            raise typer.BadParameter("--who-records takes agent or daemon")
        if action not in (None, "recorder"):
            raise typer.BadParameter("--who-records goes with --action recorder")
        action = "recorder"

    # SIGN IN ONLY (`--action login` with its flags): nothing is installed or
    # configured, so a GPU box or a self-hosted server gets a login and no
    # plugin, capture or rule it did not ask for (R10). Before the wizard's
    # window, so what it prints stays on the terminal.
    if any((token, base_url, context, ingest_token, hmac_secret, endpoint_only, no_browser)):
        if action not in (None, "login"):
            raise typer.BadParameter(
                "--token, --base-url, --context, --ingest-token, --hmac-secret, --endpoint-only and "
                "--no-browser sign in only: use them with --action login"
            )
        # Anything else asked for would be dropped in silence: say so instead.
        dropped = [
            name
            for name, value in (
                ("--agent", agent),
                ("--tracking/--no-tracking", tracking),
                ("--capture/--no-capture", capture),
                ("--auto-update/--no-auto-update", auto_update),
                ("--agent-rules/--no-agent-rules", agent_rules),
                ("--uninstall", uninstall or None),
                ("--folder", folder),
                ("a sign-in code", auth_code),
            )
            if value is not None
        ]
        if dropped:
            raise typer.BadParameter(
                f"these flags only sign in, so {', '.join(dropped)} would be ignored: "
                "run it separately, without them"
            )
        _login(
            base_url=base_url,
            token=token,
            ingest_token=ingest_token,
            hmac_secret=hmac_secret,
            device=not endpoint_only,
            context=context,
            open_browser=not no_browser,
        )
        return

    # The wizard's screens draw in a window of their own (`tui.window`): the
    # whole terminal, scrolled by the wizard's keys, and the shell's screen
    # put back untouched on the way out. `--yes` draws no screens.
    with tui.window(enabled=not yes):
        _wizard_session(
            agent=agent,
            tracking=tracking,
            capture=capture,
            auto_update=auto_update,
            agent_rules=agent_rules,
            channel=channel,
            uninstall=uninstall,
            action=action,
            folder=folder,
            yes=yes,
            auth_code=auth_code,
            who_records=who_records,
        )


def _wizard_session(
    *,
    agent,
    tracking,
    capture,
    auto_update,
    agent_rules,
    channel,
    uninstall,
    action,
    folder,
    yes,
    auth_code,
    who_records=None,
) -> None:
    """`wizard`, inside its window. See `wizard` for the contract."""
    from probe.cli import actions as actions_mod
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import telemetry as telemetry_mod
    from probe.cli import tui

    # `--channel` is accepted and ignored. Plugins update on the USER's schedule,
    # so a machine whose plugin has not been refreshed still spawns
    # `probe wizard --action update --yes --channel latest`; rejecting the flag
    # would break auto-update on exactly the machines that are behind.
    del channel

    # Direct Python callers receive Typer's argument sentinel as the default.
    install_code = auth_code if isinstance(auth_code, str) else None
    if install_code is not None and not re.fullmatch(r"[A-Z0-9]{10}", install_code):
        raise typer.BadParameter(
            "the sign-in code must contain exactly 10 uppercase letters or digits"
        )

    # Flag validation BEFORE the funnel entry event: a `--agent bogus` typo is
    # a usage error, and emitting first would file it in the funnel's
    # "infrastructure died before wizard.started" bucket.
    explicit_agent_sources: tuple[str, ...] | None = None
    if agent is not None:
        normalized_agent = agent.strip().lower()
        # "both"/"all" keep their EXISTING meaning -- claude_code + codex, the
        # two coding agents this wizard can install a marketplace plugin for
        # (see setup.INSTALLABLE_AGENT_SOURCES). pi is deliberately NOT swept
        # into either alias: it has no plugin for this run to install, only a
        # capture credential to pair (see the pi-only selection scoping
        # below), so silently including it in "both" would promise install
        # work for a run that does something categorically different. pi is
        # reachable only by naming it.
        if normalized_agent in {"both", "all", "claude,codex", "codex,claude"}:
            explicit_agent_sources = ("claude_code", "codex")
        elif normalized_agent in {"claude", "claude_code"}:
            explicit_agent_sources = ("claude_code",)
        elif normalized_agent == "codex":
            explicit_agent_sources = ("codex",)
        elif normalized_agent == "pi":
            explicit_agent_sources = ("pi",)
        elif normalized_agent in {"kimi", plugin_cli.KIMI}:
            explicit_agent_sources = (plugin_cli.KIMI,)
        else:
            raise typer.BadParameter("--agent must be claude, codex, pi, kimi, or both")

    # `wizard.invoked` fires BEFORE the bootstrap below: the ephemeral-npx →
    # persistent install is the most failure-prone distribution step, and a
    # session that dies inside it must still enter the funnel. The raw --action
    # string is clamped to known values — event properties carry enums, never
    # free-form user input (a mis-pasted secret must not ride to the vendor).
    known_actions = {a.value for a in actions_mod.Action}
    tel = telemetry_mod.TelemetryContext.start(
        via=telemetry_mod.Via.WIZARD,
        interactive=wizard.interactive(),
        base_url=resolve(base_url=_conn.base_url).base_url,
    )
    tel.emit(
        telemetry_mod.EVENT_WIZARD_INVOKED,
        invoked_action=(action if action in known_actions else "invalid" if action else None),
        interactive=wizard.interactive(),
    )

    # FIRST among the real work. `npx probe-research` launches us through an
    # EPHEMERAL `uv tool run` / `pipx run`, which leaves no binary behind — and
    # everything below assumes one exists afterwards (`probe doctor`, the
    # plugin's version-check hook, the MCP headers helper).
    from probe.cli.bootstrap import ensure_persistent_install

    # THE WIZARD'S ONE SERVER CALL (`POST /v1/device-state`): the account,
    # every agent's capture key and the version manifest, in one answer. Sent
    # here so it is in flight while the bootstrap and the local checks run.
    # It replaced a `/v1/me`, an unfiled-runs list and a capture check PER
    # AGENT plus a detached manifest fetch -- seven serial calls, nine seconds
    # of spinner on a two-agent machine. Every state read below uses it, and a
    # step that changes state asks again, once.
    from probe.cli import capabilities as capabilities_mod

    def _ask_server() -> capabilities_mod.DeviceStateResolver:
        try:
            # `resolve()`, exactly as `doctor.collect()` resolves the API it
            # reports on: the answer is graded against that server, and its
            # bearer is only ever sent to it.
            settings = resolve()
            request = capabilities_mod.device_state_request(
                settings.base_url, settings.token, wizard.INSTALLABLE_AGENT_SOURCES
            )
        except Exception as exc:  # noqa: BLE001 - the menu must render without it
            return capabilities_mod.answered_already(
                capabilities_mod.DeviceState(
                    capabilities_mod.DeviceStateOutcome.UNREACHABLE, error=str(exc)
                )
            )
        # An older server's answer carries no manifest, and the wizard spawns
        # no detached refresher: fetch it when someone will read the Versions
        # row, or when auto-update will act on it.
        from probe import version_policy

        return capabilities_mod.start_device_state(
            request,
            warm_manifest_on_fallback=(
                wizard.interactive() or version_policy.autoupdate_enabled()
            ),
        )

    device_state = _ask_server()

    boot = ensure_persistent_install()
    if boot.message:
        print(boot.message)

    codex_session = bool(os.environ.get("CODEX_THREAD_ID") or os.environ.get("CODEX_SANDBOX"))
    # `wizard.detectable_sources()`, not a fresh literal and not
    # MARKETPLACE_AGENT_SOURCES filtered by `plugin_cli.available` inline:
    # this asks "which coding agents exist on this machine", and that
    # question now has three possible answers, not two -- pi IS a binary
    # `shutil.which` can find, it just has no MARKETPLACE the way
    # claude_code/codex do (see `detectable_sources`'s docstring for the
    # stale "pi has no CLI" claim this replaces). Calling the shared helper
    # rather than re-deriving this here keeps the step-1 picker
    # (`run_agent_menu`) and this computation from silently drifting apart.
    available_sources = wizard.detectable_sources()
    if explicit_agent_sources is not None:
        agent_defaults = explicit_agent_sources
    elif codex_session and wizard.interactive():
        agent_defaults = ("codex",)
    else:
        # ONE RULE, TTY OR NOT: configure the coding agents this machine has.
        #
        # A headless run used to narrow to `("claude_code",)` here, to "preserve
        # the historical headless default" for scripts that opt into more with
        # `--agent both`. What that actually produced was a SILENT wrong answer
        # on the one path with nobody watching: a Codex user's agent runs
        # `probe install --yes` from a tool call, the wizard configures Claude
        # Code, and every screen it prints says the install succeeded. The
        # narrowing is invisible precisely because the picker and the confirm
        # screen -- the two places that would have named the selection -- are
        # both gated on `interactive()` and never ran.
        #
        # A default that differs by TTY-ness is also a rule nobody can hold: the
        # same command, same machine, same flags, configures a different set of
        # agents depending on whether stdout happens to be a pipe. Scripts that
        # want the old narrow behaviour still get it, and now state it, with
        # `--agent claude`.
        #
        # `codex_session` stays a PRE-TICK, not a pin, and so is scoped to the
        # interactive path above: inside Codex a human sees codex ticked and can
        # untick it. Applied headless it would be the same silent narrowing this
        # branch exists to remove, just landing on a different agent.
        agent_defaults = available_sources or ("claude_code",)

    from contextlib import contextmanager

    @contextmanager
    def _agent_target(source: str):
        """Scope PROBE_AGENT to one operation without leaking it to callers."""
        previous = os.environ.get("PROBE_AGENT")
        os.environ["PROBE_AGENT"] = source
        try:
            yield
        finally:
            if previous is None:
                os.environ.pop("PROBE_AGENT", None)
            else:
                os.environ["PROBE_AGENT"] = previous

    def _collect_agent(source: str, *, fresh: bool = False):
        # `fresh` asks the server again for THIS read: inside an action that
        # runs agent by agent, an earlier agent's step can change what the
        # server would say about the next one.
        state = _ask_server() if fresh else device_state
        with _agent_target(source), doctor_impl.device_state_scope(state):
            return doctor_impl.collect()

    # The action is selected BEFORE an agent. Discover state read-only for the
    # main menu, then collect only the chosen agents after the user picks what
    # they want to do. This keeps the first screen about intent, not plumbing.
    state_sources = explicit_agent_sources or available_sources or agent_defaults
    #
    # The Versions row is graded against the cached manifest, which the one
    # call refreshes (nothing else refreshes it when auto-update is off, so
    # without it the box nothing keeps current could never be told so). An
    # older server that lacks the route gets `warm_manifest()`, as before.
    with tui.working("Checking what's installed on this device"):
        state_caps_by_source = {source: _collect_agent(source) for source in state_sources}
    explicit_flags = any(f is not None for f in (tracking, capture, auto_update, agent_rules))

    tel.emit(
        telemetry_mod.EVENT_WIZARD_STARTED,
        fresh_install=not any(c.configured for c in state_caps_by_source.values()),
        agents_available=sorted(available_sources),
        install_method=state_caps_by_source[state_sources[0]].install_method,
        interactive=wizard.interactive(),
    )

    # ONE GATE IN FRONT OF EVERY EXCHANGE, and it has to be here — above both
    # the entry sign-in below (`probe wizard CODE`) and the guided apply further
    # down (`probe install CODE`), because those are the two doors a code can
    # come through and a gate on one of them is a gate on neither.
    #
    # A website install code carries its own identity: it was minted for
    # whoever was signed in on the website, and redeeming it binds THIS device
    # to that account. On a device that already holds a credential that is an
    # account switch, and it is not reversible from here — the exchange detaches
    # the credentials bound to this device (see the rotation block in the
    # backend's device exchange), so by the time we could name the new account
    # the old one is already gone. Asking afterwards would be asking about
    # something that had already happened.
    #
    # Only when we can NAME the account being replaced (see `prior_account`): an
    # unnameable one is an offline device or a revoked token, and redeeming a
    # code there is a repair rather than a switch.
    if install_code is not None:
        switching_from = wizard.prior_account(state_caps_by_source)
        if (
            switching_from is None
            and resolve().token
            and not any(
                snapshot.api_credential_valid is False
                for snapshot in state_caps_by_source.values()
            )
        ):
            # A credential nobody refused, but the one call could not NAME its
            # account (a slow server, a network urllib could not cross). The
            # switch is irreversible, so ask the old way before deciding that
            # there is nothing to switch from.
            switching_from = doctor_impl.name_account()
            if switching_from:
                state_caps_by_source = {
                    source: dataclasses.replace(snapshot, logged_in_as=switching_from)
                    if snapshot.logged_in_as is None
                    else snapshot
                    for source, snapshot in state_caps_by_source.items()
                }
        if switching_from and not yes:
            if not wizard.interactive():
                # Refuse rather than switch. The same rule the bare-headless
                # guard below applies to capture: a consequence nobody can be
                # shown is a consequence nobody consented to.
                for line in wizard.account_switch_refusal(switching_from):
                    tui.say(line)
                raise typer.Exit(1)
            tui.clear()
            if wizard.run_confirm_account_switch(switching_from) is not True:
                tui.say(f"Left as it was — this device is still signed in as {switching_from}.")
                raise typer.Exit(0)

    # A bare launch signs in before showing the menu. `install CODE` waits for
    # the agent/capability selection so the one-time exchange grants exactly
    # what the user chose. Existing unattended maintenance stays independent.
    menu_entry = action is None and not yes and not explicit_flags
    authenticated_action_entry = (
        action in {"account", "defaults", "settings", "import-research", "recorder"} and not yes
    )
    authenticate_menu = (
        (menu_entry or authenticated_action_entry)
        and wizard.interactive()
        and (
            not resolve(base_url=_conn.base_url).token
            or any(
                snapshot.api_credential_valid is False for snapshot in state_caps_by_source.values()
            )
        )
    )
    if (install_code is not None and action != "configure") or authenticate_menu:
        tui.say(
            "Signing in with the website code…"
            if install_code
            else "Sign in to Probe Research in your browser."
        )
        try:
            signed_in = wizard.sign_in(
                base_url=resolve(base_url=_conn.base_url).base_url,
                sources=state_sources,
                on_prompt=_show_device_prompt,
                prepare_install=bool(available_sources),
                **({"install_code": install_code} if install_code is not None else {}),
            )
        except OnboardingRequired as exc:
            _finish_website_onboarding(exc)
        tel.emit(
            telemetry_mod.EVENT_WIZARD_SIGNED_IN,
            outcome=(
                telemetry_mod.SignInOutcome.SUCCESS
                if signed_in.ok
                else telemetry_mod.SignInOutcome.FAILED
            ),
            via_wizard_entry=True,
        )
        for line in signed_in.lines:
            tui.say(line)
        if not signed_in.ok:
            raise typer.Exit(1)
        install_code = None
        # Signing in changed the account (and may have paired capture): ask again.
        device_state = _ask_server()
        state_caps_by_source = {source: _collect_agent(source) for source in state_sources}

    def _require_account():
        # Every entry and return shares this gate. A removal or revoked token
        # must not reopen an unauthenticated menu, and an explicit sign-out
        # must never start another browser sign-in in the same invocation.
        if not resolve(base_url=_conn.base_url).token or any(
            snapshot.api_credential_valid is False for snapshot in state_caps_by_source.values()
        ):
            tui.say("Sign in to use the wizard. Run `npx probe-research` again.")
            raise typer.Exit(0)

    # A state handed back as `wizard.DefaultChoice`, for the DEFAULTS action to
    # apply without opening its picker. The menu's Defaults row saves on each
    # press itself now, so only a caller that still answers DefaultChoice sets
    # it. Reset on every menu, so it never outlives the choice that set it.
    menu_default: str | None = None
    # The same for the Who records row, which applies the moment it is switched
    # (`wizard.RecorderChoice`); None means Enter on the row. `--who-records`
    # sets it for `--action recorder`, `--yes` included (R7).
    menu_recorder: str | None = who_records

    def _show_main_menu():
        nonlocal menu_default, menu_recorder
        _require_account()
        from probe.cli import import_jobs

        import_jobs.recover_jobs()
        default_before = session_marker.default_session_state()
        picked = wizard.run_action_menu(state_caps_by_source)
        if (
            session_marker.default_session_state() != default_before
            and picked is not actions_mod.Action.DEFAULTS
        ):
            # The Defaults row saves on each press, inside the menu, so it never
            # reaches the pass's own event: count it here as the `defaults`
            # action it is, once per menu -- unless the menu answers DEFAULTS
            # (Enter on the same row), whose pass counts it already.
            tel.emit(
                telemetry_mod.EVENT_WIZARD_ACTION_CHOSEN,
                action=actions_mod.Action.DEFAULTS.value,
                via_flag=False,
            )
        menu_default = None
        menu_recorder = None
        if isinstance(picked, wizard.DefaultChoice):
            menu_default = picked.state
            return actions_mod.Action.DEFAULTS
        if isinstance(picked, wizard.RecorderChoice):
            menu_recorder = picked.value
            return actions_mod.Action.RECORDER
        return picked

    if authenticated_action_entry and wizard.interactive():
        _require_account()

    # Everything the dashboard used to hide in collapsed sections lives here,
    # next to the state it acts on. The main menu is always the first
    # interactive decision, including on a fresh machine; agent and capability
    # selection follow only after the user chooses an action.
    chosen_action = actions_mod.Action.CONFIGURE
    if action is not None:
        try:
            chosen_action = actions_mod.Action(action)
        except ValueError:
            tui.final(
                f"unknown action {action!r}; expected one of: "
                f"{', '.join(a.value for a in actions_mod.Action)}",
                file=sys.stderr,
            )
            raise typer.Exit(2) from None
    elif not yes and not explicit_flags and wizard.interactive():
        tui.clear()
        picked = _show_main_menu()
        if picked is None or picked is tui.BACK:
            _exit_wizard()
        chosen_action = picked
    elif not yes and not explicit_flags and explicit_agent_sources is None:
        # BARE `probe wizard`, HEADLESS: refuse rather than install.
        #
        # `chosen_action` defaults to CONFIGURE, and every screen that would
        # have turned that default into a decision is gated on `interactive()`
        # -- the action menu just above, and `run_confirm_install` further down,
        # which is where the capture disclosure is drawn. So a bare
        # `npx probe-research` from an agent's shell tool skipped BOTH and ran a
        # complete install: tracking, capture, auto-update and agent rules all
        # enabled from FRESH_DEFAULTS, with no menu, no disclosure and no
        # keystroke. It then reported success, which is worse than crashing --
        # capture streams prompts, assistant replies and shell commands off the
        # machine, and the run that enabled it never showed anyone that it had.
        #
        # Refusing is narrow on purpose, and every deliberate caller is already
        # outside it: `probe install` passes `action="configure"`, auto-update
        # spawns `--action update --yes`, and a script that means it says `--yes`,
        # names a capability flag, or names `--agent`. What is left is exactly
        # the case that cannot have been meant -- no verb, no flags, no agent,
        # nobody watching.
        print(
            "probe wizard: refusing to configure without a decision.\n"
            "  Nothing has been changed.\n"
            "  This is the interactive menu, and there is no terminal here to "
            "draw it on.\n"
            "  To install:  probe wizard --action configure\n"
            "  Non-interactively, say what you want: --yes, or --action <name>.",
            file=sys.stderr,
        )
        raise typer.Exit(2)

    base_now = resolve(base_url=_conn.base_url).base_url

    # The menu comes BACK after each action. Dropping the user to a shell once
    # one task finishes is the same "go do it yourself" failure as printing a
    # command: after an update you want doctor, after a removal you often want
    # to turn something else on.
    looping = action is None and not yes and not explicit_flags and wizard.interactive()

    while True:
        if chosen_action is actions_mod.Action.EXIT:
            _exit_wizard()

        # At the convergence point where the action is known for this pass,
        # whether it came from the menu or --action — never inside menu code,
        # which the test suite cannot execute.
        tel.emit(
            telemetry_mod.EVENT_WIZARD_ACTION_CHOSEN,
            action=chosen_action.value,
            via_flag=action is not None,
        )

        # THE GUIDED INSTALL: choose the coding agents (only when this
        # machine offers a choice), then review everything the install turns
        # on and confirm. There is no capability picker -- the install is
        # complete by design (see setup.py's module docstring for what carries
        # the capture disclosure now), and the interactive Install action is
        # FORCE-ON: everything enables, the capture killswitch included, with
        # the disclosure on screen before the confirming keystroke. The flag
        # path is untouched -- an omitted flag on a scripted re-run still
        # PRESERVES.
        shared_selection = None
        install_needs: list[str] | None = None
        install_context: dict | None = None
        install_capture_sources: list[str] | None = None
        guided_install = False
        agent_screen_shown = False
        back_to_menu = False
        while True:
            agent_sources = explicit_agent_sources
            if (
                agent_sources is None
                # A screen that asks a question with one possible answer is a
                # step for nothing: the agent picker only appears when BOTH
                # coding agents are actually on this machine. `--yes` promised
                # to skip the prompts, so it skips this one too.
                and not yes
                and len(available_sources) > 1
                and chosen_action not in actions_mod.IMPORT_ACTIONS
                # Account and settings are device-wide: one config file, not one
                # per agent. Asking which coding agents to configure before
                # "sign out" is a question with no bearing on the answer. The
                # selection still defaults to every agent found here, because
                # the CAPTURE half of an account change is per agent.
                and chosen_action not in actions_mod.DEVICE_ACTIONS
                and wizard.interactive()
            ):
                tui.clear()
                picked_agents = wizard.run_agent_menu(agent_defaults, action=chosen_action)
                if picked_agents is None or picked_agents is tui.BACK:
                    back_to_menu = True
                    break
                agent_sources = picked_agents
                agent_defaults = picked_agents
                agent_screen_shown = True
            elif agent_sources is None:
                # Zero or one agent found (no choice to ask), or a headless
                # call, which has no picker to show. Backfill is
                # agent-independent but _run_wizard_action still needs one
                # capability snapshot for shared account/base-url state.
                #
                # DEVICE actions cover every agent FOUND on the machine, never
                # what the previous action happened to select: `agent_defaults`
                # remembers the last picker answer (and a Codex session pins
                # it to codex), so scoping Settings to it let a device-wide
                # screen report "capture off" while the other agent kept
                # capturing.
                if chosen_action in actions_mod.IMPORT_ACTIONS:
                    agent_sources = agent_defaults[:1]
                elif chosen_action in actions_mod.DEVICE_ACTIONS:
                    agent_sources = available_sources or agent_defaults
                else:
                    agent_sources = agent_defaults

                # SAY WHICH AGENTS, when nothing else on this run will.
                #
                # Interactively the picker or the confirm screen names the
                # selection; headless there is neither, so an implicit choice
                # across a multi-agent machine would otherwise be reported
                # nowhere at all -- and "which agents did that configure?" is
                # exactly the question a caller cannot answer afterwards from a
                # log full of green ticks. Printed only when it is genuinely a
                # choice (more than one agent found, none named on the command
                # line): a one-agent machine has nothing to disambiguate.
                if (
                    not wizard.interactive()
                    and explicit_agent_sources is None
                    and len(available_sources) > 1
                ):
                    print(
                        "configuring every coding agent found on this device: "
                        f"{wizard.agent_label(agent_sources)}"
                        " (pass --agent to choose)",
                        flush=True,
                    )

            # Every action draws from the menu's snapshot rather than
            # re-collecting: the menu loop re-reads state after every action
            # that changes it, so the snapshot is current, and nothing has
            # changed between drawing the menu and this keypress. An agent the
            # snapshot lacks (picked in the agent step) is read through the
            # same server answer, with no new call.
            with tui.working("Checking what's installed on this device") if any(
                source not in state_caps_by_source for source in agent_sources
            ) else contextlib.nullcontext():
                caps_by_source = {
                    source: state_caps_by_source.get(source) or _collect_agent(source)
                    for source in agent_sources
                }
            caps = caps_by_source[agent_sources[0]]
            configured = any(snapshot.configured for snapshot in caps_by_source.values())

            # The SAME condition `_run_wizard_action` used to gate its own copy
            # of these prompts, deliberately -- including `--action configure`
            # (and `probe install`, its alias), which is interactive but does
            # not loop.
            if not (
                chosen_action is actions_mod.Action.CONFIGURE
                and not yes
                and not explicit_flags
                and wizard.interactive()
            ):
                break

            tui.clear()
            # Availability of the agents this run actually SELECTED — not of
            # the machine at large: `probe install --agent codex` on a
            # Claude-only box must get the degraded screen, not a promise of
            # Codex plugins the apply cannot keep. A PARTIAL miss (`--agent
            # both`, one binary present) keeps the full screen but names the
            # absent agent on it, so the screen promises exactly what the
            # apply will do.
            #
            # pi is excluded from this question entirely, not folded into it:
            # "degraded" here measures whether a MARKETPLACE binary the apply
            # needs is missing, and pi's install is a settings.json write
            # that needs no binary at all -- so this filters on
            # wizard.MARKETPLACE_AGENT_SOURCES, NOT the (pi-inclusive)
            # INSTALLABLE_AGENT_SOURCES. Filtering on the latter would make a
            # pi-only interactive run compute plugins_available=False and show
            # the degraded "skipped, install pi and re-run" screen for a run
            # whose install cannot be degraded by any missing binary.
            #
            # `available_sources` itself CAN contain "pi" now (see
            # `detectable_sources`) -- that is what lets a pi-only machine
            # skip this screen family entirely via the `len(available_sources)
            # > 1` gate above, before ever reaching this filter. What must
            # stay true here is narrower: pi must never enter
            # `plugin_promising_sources`, because it is never what
            # "degraded" is measuring.
            plugin_promising_sources = tuple(
                source for source in agent_sources if source in wizard.MARKETPLACE_AGENT_SOURCES
            )
            plugins_available = not plugin_promising_sources or any(
                source in available_sources for source in plugin_promising_sources
            )
            confirmed = wizard.run_confirm_install(
                agent_sources,
                # Omit the skipped agent screen from the progress count.
                step=wizard.STEP_CONFIRM if agent_screen_shown else None,
                plugins_available=plugins_available,
                unavailable=tuple(
                    source for source in plugin_promising_sources if source not in available_sources
                ),
            )
            if confirmed is None:
                _exit_wizard()
            if confirmed is tui.BACK:
                if agent_screen_shown and explicit_agent_sources is None:
                    continue  # re-open the agent screen; the selection is kept
                # `--agent` answered the only earlier step, or there was none.
                # The action menu is the previous screen.
                back_to_menu = True
                break
            guided_install = True
            # FORCE-ON: Install means install. Everything enables -- including
            # re-pairing a killswitched capture, which the confirm screen just
            # disclosed. Scripted paths never reach here; their omitted flags
            # PRESERVE (see resolve_selection).
            #
            # UNLESS the degraded screen was the one shown: it disclosed the
            # CLI and the sign-in and said the plugins are SKIPPED -- so the
            # selection enables exactly that, and everything it did NOT
            # mention is PRESERVED as it stands. Applying the full force-on
            # there would request a capture grant no bullet ever named;
            # applying all-off would be just as undisclosed in the other
            # direction — on a configured machine whose binaries are
            # temporarily missing it would killswitch a live capture and
            # strip the rules a screen that said "skipped" never named.
            # The wizard authenticated before opening the menu. Reuse those
            # credentials, including capture paired but left disabled until
            # this confirmation. Direct installs and older logins can still
            # lack grants; only those need a browser approval here.
            if plugins_available:
                shared_selection = wizard.Selection(
                    tracking=True, capture=True, auto_update=True, agent_rules=True
                )
            else:
                current_union = {
                    capability: any(
                        snapshot.enabled()[capability] for snapshot in caps_by_source.values()
                    )
                    for capability in wizard.Capability
                }
                shared_selection = wizard.Selection(
                    tracking=True,
                    capture=current_union[wizard.Capability.CAPTURE],
                    auto_update=current_union[wizard.Capability.AUTO_UPDATE],
                    agent_rules=current_union[wizard.Capability.AGENT_RULES],
                )
            install_needs = (
                []
                if install_code is None
                and _install_grants_held(caps_by_source, shared_selection, base_url=base_now)
                else wizard.grants_for(shared_selection)
            )
            install_context = wizard.install_client_context(caps_by_source)
            if not plugins_available:
                # The degraded path preserves capture rather than granting it,
                # so the only capture credentials this approval may touch are
                # the ones the device ALREADY holds locally — sign_in's
                # ride-along rule. Without it, an account switch here moved
                # api/mcp to the new team while capture kept uploading to the
                # old one, under a token the new team cannot see or revoke.
                install_capture_sources = (
                    wizard.locally_paired_capture(agent_sources) if shared_selection.capture else []
                )
            else:
                install_capture_sources = list(agent_sources) if shared_selection.capture else []
            break

        if back_to_menu:
            if not looping:
                raise typer.Exit(0)
            tui.clear()
            picked = _show_main_menu()
            if picked is None or picked is tui.BACK:
                _exit_wizard()
            chosen_action = picked
            continue

        if install_code is not None and chosen_action is actions_mod.Action.CONFIGURE:
            # A code always authenticates, including on a configured machine or
            # when all optional tooling capabilities were explicitly declined.
            _aggregate, resolved = _shared_selection(
                caps_by_source,
                tracking=tracking,
                capture=capture,
                auto_update=auto_update,
                agent_rules=agent_rules,
                configured=configured,
            )
            shared_selection = shared_selection or resolved
            install_needs = list(
                dict.fromkeys(["api", "mcp", *wizard.grants_for(shared_selection)])
            )
            install_capture_sources = list(agent_sources) if shared_selection.capture else []
            install_context = wizard.install_client_context(caps_by_source)

        installation_completion = (
            _InstallationCompletion(len(agent_sources))
            if chosen_action is actions_mod.Action.CONFIGURE
            else None
        )
        # Bound here, not in the removal branch below: the completion emit sits
        # outside the if/else that sets it, and an unbound name there would
        # crash the menu loop for every OTHER action.
        uninstall_started_at = None
        if chosen_action is actions_mod.Action.UNINSTALL:
            # BEFORE the confirmation and before anything is torn down: this is
            # the state being removed, and after the per-agent loop it is
            # unreadable by construction.
            #
            # Above the dispatch below, not inside one of its branches: a
            # single-agent removal takes the `len(agent_sources) == 1` path and
            # confirms INSIDE `_run_wizard_action`, which is the ordinary case
            # and the one a branch-local emit missed entirely.
            uninstall_started_at = time.monotonic()
            tel.emit(
                telemetry_mod.EVENT_WIZARD_UNINSTALL_STARTED,
                agent_count=len(agent_sources),
                tracking_installed=caps.tracking_plugin_installed,
                capture_installed=caps.capture_plugin_installed,
                agent_rules_installed=caps.agent_rules_installed,
                was_signed_in=bool(caps.logged_in_as),
                confirmed_via="flag" if yes or not wizard.interactive() else "prompt",
            )
        diagnose_unfiled = None
        if chosen_action is actions_mod.Action.DIAGNOSE:
            # Diagnose reports what is true NOW: ask again when the held answer
            # is old or was not an answer at all (one call, for every agent).
            if device_state.stale(_DIAGNOSE_MAX_AGE_S):
                device_state = _ask_server()
                caps_by_source = {source: _collect_agent(source) for source in agent_sources}
            # It also shows the unfiled-runs count, which the one call does not
            # carry: ask once, when the server answered (the old way already
            # fetched it; offline, it would only wait).
            if device_state().answered:
                diagnose_unfiled = doctor_impl.fetch_unfiled()
            if diagnose_unfiled is not None:
                caps_by_source = {
                    source: dataclasses.replace(snapshot, unfiled_runs=diagnose_unfiled)
                    if snapshot.unfiled_runs is None
                    else snapshot
                    for source, snapshot in caps_by_source.items()
                }
            caps = caps_by_source[agent_sources[0]]
        if chosen_action in actions_mod.DEVICE_ACTIONS:
            # ONCE for the device, and unlabelled: the per-agent loop below
            # would run a browser approval per coding agent and file the result
            # under "Claude Code:", which is the wrong shape for a credential
            # -- or a device-wide default -- that belongs to neither.
            lines = _run_wizard_action(
                chosen_action,
                caps=caps,
                base_now=base_now,
                yes=yes,
                tracking=tracking,
                capture=capture,
                auto_update=auto_update,
                agent_rules=agent_rules,
                uninstall=uninstall,
                configured=configured,
                folder=folder,
                selected_agents=agent_sources,
                caps_by_source=caps_by_source,
                telemetry=tel,
                default_state=menu_default,
                recorder=menu_recorder,
            )
        elif len(agent_sources) == 1:
            with _agent_target(agent_sources[0]):
                lines = _run_wizard_action(
                    chosen_action,
                    caps=caps,
                    base_now=base_now,
                    yes=yes,
                    tracking=tracking,
                    capture=capture,
                    auto_update=auto_update,
                    agent_rules=agent_rules,
                    uninstall=uninstall,
                    configured=configured,
                    folder=folder,
                    # None unless the install steps above already answered --
                    # they own the interactive path now, because they are the
                    # only place that can walk BACK through it.
                    selection_override=shared_selection,
                    authorization_needs=install_needs,
                    capture_sources=install_capture_sources,
                    authorization_context=install_context,
                    progress_header=(
                        wizard.install_apply_header(
                            agent_screen_shown=agent_screen_shown,
                            agent_index=0,
                            agent_count=1,
                            agent_source=agent_sources[0],
                        )
                        if install_context is not None
                        else None
                    ),
                    install_code=install_code,
                    installation_completion=installation_completion,
                    telemetry=tel,
                )
        elif chosen_action is actions_mod.Action.CONFIGURE:
            aggregate, resolved = _shared_selection(
                caps_by_source,
                tracking=tracking,
                capture=capture,
                auto_update=auto_update,
                agent_rules=agent_rules,
                configured=configured,
            )
            # The interactive steps ran ABOVE, where Back can still walk them.
            # What is left here is the headless answer.
            if shared_selection is None:
                shared_selection = resolved
            # Guided installs already checked the saved credentials above.
            shared_needs = (
                install_needs
                if install_needs is not None
                else _needs_for_this_run(
                    wizard.needs_authorization(aggregate, shared_selection), yes=yes
                )
            )
            missing_capture_sources = (
                install_capture_sources
                if install_capture_sources is not None
                else [
                    source
                    for source, snapshot in caps_by_source.items()
                    if shared_selection.capture and not snapshot.capture_token_sources
                ]
            )
            lines = []
            for index, source in enumerate(agent_sources):
                current = _collect_agent(source, fresh=index > 0)
                # A guided run resolved every selected source together. The
                # first apply raises if approval failed; later agents reuse
                # its result even if their identity lookup is unavailable.
                authorization_needs = shared_needs if index == 0 else None
                if index > 0 and install_needs is not None:
                    authorization_needs = []
                with _agent_target(source):
                    result = _run_wizard_action(
                        chosen_action,
                        caps=current,
                        base_now=base_now,
                        yes=True,
                        tracking=tracking,
                        capture=capture,
                        auto_update=auto_update,
                        agent_rules=agent_rules,
                        uninstall=uninstall,
                        configured=configured,
                        folder=folder,
                        selection_override=shared_selection,
                        authorization_needs=authorization_needs,
                        capture_sources=missing_capture_sources,
                        authorization_context=install_context,
                        progress_header=(
                            wizard.install_apply_header(
                                agent_screen_shown=agent_screen_shown,
                                agent_index=index,
                                agent_count=len(agent_sources),
                                agent_source=source,
                            )
                            if install_context is not None
                            else None
                        ),
                        install_code=install_code if index == 0 else None,
                        installation_completion=installation_completion,
                        telemetry=tel,
                    )
                if result:
                    label = wizard.agent_label(source)
                    lines.extend([f"{label}:", *result, ""])
            # Configure streams its own progress; successful calls return no lines.
        else:
            # Diagnostics/removal are source-local. Manual instructions and
            # backfill are agent-independent, so do not duplicate them.
            targets = (
                agent_sources
                if chosen_action
                in {
                    actions_mod.Action.DIAGNOSE,
                    actions_mod.Action.UPDATE,
                    actions_mod.Action.UNINSTALL,
                }
                else agent_sources[:1]
            )
            action_yes = yes
            if chosen_action is actions_mod.Action.UNINSTALL and not yes and wizard.interactive():
                tui.clear()
                if wizard.confirm_removal(agent_sources) is not True:
                    # The one outcome no server-side signal can ever see: the
                    # device is still here, so nothing reports anything.
                    tel.emit(
                        telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                        outcome=telemetry_mod.UninstallOutcome.DECLINED,
                        agent_count=len(agent_sources),
                        duration_seconds=round(time.monotonic() - uninstall_started_at, 3),
                    )
                    return
                action_yes = True
            lines = []
            all_backed_out = True
            for index, source in enumerate(targets):
                # Uninstall revokes each agent's capture key as it goes, and
                # the next agent's answer can change under it (the server
                # state it reads moves). Diagnose and update change nothing
                # the server reports.
                current = _collect_agent(
                    source,
                    fresh=index > 0 and chosen_action is actions_mod.Action.UNINSTALL,
                )
                if diagnose_unfiled is not None and current.unfiled_runs is None:
                    current = dataclasses.replace(current, unfiled_runs=diagnose_unfiled)
                with _agent_target(source):
                    result = _run_wizard_action(
                        chosen_action,
                        caps=current,
                        base_now=base_now,
                        yes=action_yes,
                        tracking=tracking,
                        capture=capture,
                        auto_update=auto_update,
                        agent_rules=agent_rules,
                        uninstall=uninstall,
                        configured=configured,
                        folder=folder,
                        selected_agents=agent_sources,
                        telemetry=tel,
                    )
                if result is not None:
                    all_backed_out = False
                if result:
                    label = wizard.agent_label(source)
                    lines.extend([f"{label}:", *result, ""])
            # Every target said "nothing happened" (today: only backfill's
            # folder/agent back-outs) -- carry the signal through so the menu
            # comes back without the pause or the state re-read.
            if all_backed_out:
                lines = None

        # The ACCOUNT half of Uninstall, ONCE for the device. Everything above
        # runs per coding agent; a credential does not -- there is one config
        # file -- and it has to be released after the LAST agent has published
        # its emptied state, because that registration authenticates with the
        # token being released. `lines is None` is the user declining at the
        # confirmation, which must sign nobody out.
        if chosen_action is actions_mod.Action.UNINSTALL and lines is not None:
            # BEFORE the credential goes. `finish_removal` revokes this
            # device's token and clears it, and the completion event below is
            # emitted after -- so without this it resolves to `machine:<id>`
            # with no person attached, and the one event that says a customer
            # left is dropped by every destination filtering on a known person.
            tel.pin_identity()
            lines = [*lines, *wizard.finish_removal()]
            tel.emit(
                telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                outcome=telemetry_mod.UninstallOutcome.REMOVED,
                agent_count=len(agent_sources),
                # Removal reports its own problems as `! ...` lines and carries
                # on; counting them separates a clean uninstall from one that
                # left something behind. The lines THEMSELVES never ride along
                # -- they name paths.
                warnings=sum(1 for line in lines if line.startswith("!")),
                duration_seconds=(
                    round(time.monotonic() - uninstall_started_at, 3)
                    if uninstall_started_at is not None
                    else None
                ),
            )
        elif chosen_action is actions_mod.Action.UNINSTALL and uninstall_started_at is not None:
            # Every selected agent declined at the per-agent confirmation.
            tel.emit(
                telemetry_mod.EVENT_WIZARD_UNINSTALL_COMPLETED,
                outcome=telemetry_mod.UninstallOutcome.DECLINED,
                agent_count=len(agent_sources),
                duration_seconds=round(time.monotonic() - uninstall_started_at, 3),
            )

        install_code = None
        if chosen_action is actions_mod.Action.IMPORT_RESEARCH:
            # The shared selector and monitor return to the menu even when
            # reached directly with --action import-research.
            looping = True
            action = None
        if chosen_action is actions_mod.Action.SIGN_OUT and lines is not None:
            # None: the confirmation page was answered "stay signed in" --
            # back to the menu, nothing changed.
            if lines:
                tui.final("\n".join(lines))
            raise typer.Exit(0)
        # Inside the menu loop this is a PAGE of the wizard, so it gets the
        # same centred treatment as every prompt. A one-shot `--action` run is
        # command output: printing it plainly leaves the user's scrollback
        # alone, which clearing the screen for a single result would not.
        paged = bool(lines) and looping and wizard.interactive()
        if paged:
            tui.page(
                lines,
                prompt=(
                    "Press enter to continue…"
                    if guided_install
                    else "Press enter to return to the menu…"
                ),
                copyable=chosen_action is actions_mod.Action.DIAGNOSE,
            )
        elif lines:
            tui.final("\n".join(lines))

        # The guided install's OWN completion. `configure_completed` fires once
        # per configure call -- a two-agent install emits two of them and
        # neither says whether the installation as a whole is usable. This
        # fires once, and carries the verdict the dashboard gates on.
        if installation_completion is not None and installation_completion.remaining == 0:
            tel.emit(
                telemetry_mod.EVENT_WIZARD_INSTALL_SETTLED,
                outcome=(
                    telemetry_mod.InstallSettledOutcome.SETTLED
                    if installation_completion.settled
                    else telemetry_mod.InstallSettledOutcome.UNSETTLED
                ),
                agent_count=len(agent_sources),
                guided=bool(guided_install),
            )

        # Offer imports only after every selected agent has finished setup.
        # Failed or canceled installs never reach this point; scripted installs
        # skip the offer. Back leaves the completed install in place.
        imports: set[wizard.BackfillChoice] = set()
        if guided_install:
            picked_imports = _select_and_run_imports(
                caps=caps,
                base_now=base_now,
                folder=folder,
                selected_agents=agent_sources,
                telemetry=tel,
                agent_screen_shown=agent_screen_shown,
                progress_header=lambda fraction: wizard.install_header(
                    wizard.STEP_IMPORTS,
                    agent_screen_shown=agent_screen_shown,
                    fraction=fraction,
                ),
            )
            if picked_imports is tui.BACK:
                looping = True
                action = None
                paged = True
            else:
                imports = picked_imports
        if imports:
            looping = True
            action = None
            paged = True  # The import flow already handled its own pages.

        if (
            guided_install
            and picked_imports is not tui.BACK
            and installation_completion is not None
            and installation_completion.settled
            and installation_completion.remaining == 0
        ):
            from probe.cli import import_jobs_ui, onboarding_complete

            with tui.onboarding(
                lambda: wizard.install_header(
                    wizard.STEP_IMPORTS,
                    agent_screen_shown=agent_screen_shown,
                    fraction=1.0,
                )
            ):
                try:
                    completion = onboarding_complete.show(base_now)
                except KeyboardInterrupt:
                    # Not "back", and not the wizard's Exit either: this is the
                    # last screen of a guided install being walked away from,
                    # which is the drop-off the funnel exists to count.
                    tel.emit(
                        telemetry_mod.EVENT_WIZARD_ONBOARDING_COMPLETED,
                        outcome=telemetry_mod.OnboardingOutcome.ABANDONED,
                        imports_chosen=sorted(str(choice) for choice in imports),
                    )
                    raise
                tel.emit(
                    telemetry_mod.EVENT_WIZARD_ONBOARDING_COMPLETED,
                    outcome=(
                        telemetry_mod.OnboardingOutcome.EXITED
                        if completion == import_jobs_ui.Navigation.EXIT
                        else telemetry_mod.OnboardingOutcome.DASHBOARD_OPENED
                        if completion
                        else telemetry_mod.OnboardingOutcome.RETURNED_TO_MENU
                    ),
                    imports_chosen=sorted(str(choice) for choice in imports),
                )
                if completion:
                    # Approved imports keep running after this UI closes.
                    raise typer.Exit(0)
            looping = True
            action = None
            paged = True

        if not looping:
            raise typer.Exit(0)

        # Re-read state: the action just changed it, and the next choice should
        # be made against what is true now, not what was true on entry.
        # `lines is None` is an action saying NOTHING happened -- a pure
        # back-out. The pause exists so streamed output (configure's progress
        # screen) is not wiped by the menu redraw; stopping a back-out on an
        # empty page to press Enter reads as landing on a broken screen.
        if not paged and lines is not None and wizard.interactive():
            tui.page(
                [actions_mod.ACTION_COPY[chosen_action][0], "", "Finished."],
                prompt="Press enter to return to the menu…",
            )
        # Re-read state ONLY when the action could have changed it. A pure
        # back-out (`lines is None`) changed nothing, and re-collecting costs
        # ~a second per agent -- which turned `‹ Back` into a visible stall
        # between the screen closing and the menu coming back.
        if lines is not None:
            state_sources = tuple(dict.fromkeys((*state_sources, *agent_sources)))
            # Diagnose only READS, so the server's answer still stands.
            if chosen_action is not actions_mod.Action.DIAGNOSE:
                device_state = _ask_server()
            with tui.working("Checking what's installed on this device"):
                state_caps_by_source = {source: _collect_agent(source) for source in state_sources}
        tui.clear()
        picked = _show_main_menu()
        if picked is None or picked is tui.BACK:
            _exit_wizard()
        chosen_action = picked


def _install_grants_held(caps_by_source, selection, *, base_url: str) -> bool:
    """Reuse the selected agents' credentials, independently of installation.

    A disabled capture credential is still authorized: the install confirmation
    enables it. An unavailable identity check is also not a reason to sign in
    again, but an explicitly rejected credential is. Check the actual MCP token
    rather than assuming that every saved API token was minted alongside one.

    If anything is missing, the caller requests the complete selection in one
    approval: the browser can switch accounts, so renewing capture alone could
    leave it belonging to a different account from the saved API/MCP tokens.
    """
    from probe.cli.setup import has_source_capture_grant

    settings = resolve(base_url=base_url)
    if selection.tracking and (
        not settings.token
        or not settings.mcp_token
        or any(caps.api_credential_valid is False for caps in caps_by_source.values())
    ):
        return False
    if selection.capture and not all(
        has_source_capture_grant(source, caps.capture_token_sources)
        and caps.capture_credential_valid is not False
        for source, caps in caps_by_source.items()
    ):
        return False
    if selection.tracking:
        from probe.cli.capabilities import verify_mcp_credential

        return (
            verify_mcp_credential(base_url=settings.base_url, token=settings.mcp_token) is not False
        )
    return True


def _shared_selection(
    caps_by_source,
    *,
    tracking,
    capture,
    auto_update,
    agent_rules,
    configured: bool,
):
    """One capability decision covering every selected agent, plus the snapshot
    it was resolved against.

    Extracted so the interactive steps can be asked ONCE, before the per-agent
    apply loop -- which is what lets `‹ Back` walk them. It has always been
    correct for a single agent too (every `all()`/`any()` over one item is that
    item), so there is no second code path for the common case.

    A feature reads as ENABLED only when every selected agent has it, so a
    partially configured machine visibly offers to finish the gap...
    """
    from probe.cli import setup as wizard

    caps = next(iter(caps_by_source.values()))
    aggregate = dataclasses.replace(
        caps,
        tracking_plugin_installed=all(
            item.tracking_plugin_installed for item in caps_by_source.values()
        ),
        capture_plugin_installed=all(
            item.capture_plugin_installed for item in caps_by_source.values()
        ),
        capture_token_sources=(
            caps.capture_token_sources
            if all(item.capture_on for item in caps_by_source.values())
            else ()
        ),
        capture_killswitched=any(item.capture_killswitched for item in caps_by_source.values()),
        agent_rules_installed=all(item.agent_rules_installed for item in caps_by_source.values()),
        agent_rules_stale=any(item.agent_rules_stale for item in caps_by_source.values()),
        mcp_authenticated=all(
            item.agent_source != "codex" or item.mcp_authenticated is True
            for item in caps_by_source.values()
        ),
        plugins_verified=all(item.plugins_verified for item in caps_by_source.values()),
    )
    # ...but what the boxes come up TICKED as is a different question, and the
    # intersection answers it wrongly. Adding Codex to a machine where Claude
    # Code is already set up makes every `all()` false, so PRESERVE preserves
    # nothing and the menu opens empty -- which the apply path reads, per agent,
    # as "remove the CLI + MCP plugin" and "turn Session capture off" for the
    # agent that HAS them. Preselect from the union: what this device already does.
    union_enabled = {
        capability: any(item.enabled()[capability] for item in caps_by_source.values())
        for capability in wizard.Capability
    }
    return aggregate, wizard.resolve_selection(
        aggregate,
        tracking=tracking,
        capture=capture,
        auto_update=auto_update,
        agent_rules=agent_rules,
        configured=configured,
        current_override=union_enabled,
    )


def _select_and_run_imports(
    *,
    caps,
    base_now,
    folder,
    selected_agents,
    telemetry,
    agent_screen_shown: bool = True,
    progress_header: Callable[[float], Sequence[str]] | None = None,
):
    """Keep Back navigation inside optional imports, after installation."""
    from probe.cli import setup, tui

    from probe.cli import telemetry as telemetry_mod

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    defaults = None
    while True:
        tui.clear()
        imports = setup.run_backfill_offer(
            selected_agents,
            defaults=defaults,
            agent_screen_shown=agent_screen_shown,
            onboarding=progress_header is not None,
            back_to_menu=True,
        )
        # The convergence point for both entry paths -- guided install and the
        # main-menu selector -- and the only place the answer exists as a
        # value. Emitted for EVERY answer including the empty set: skipping is
        # the most common thing to do here, and an event that only fired when a
        # box was ticked would leave the skip completely invisible.
        tel.emit(
            telemetry_mod.EVENT_WIZARD_IMPORTS_CHOSEN,
            choices=(
                sorted(str(choice) for choice in imports)
                if isinstance(imports, (set, frozenset))
                else []
            ),
            choice_count=len(imports) if isinstance(imports, (set, frozenset)) else 0,
            navigation=(
                "quit"
                if imports is None
                else "back"
                if imports is tui.BACK
                else "skip"
                if not imports
                else "continue"
            ),
            onboarding=progress_header is not None,
            offered_again=defaults is not None,
        )
        if imports is None:
            _exit_wizard()
        if imports is tui.BACK or not imports:
            return imports
        completed = set()
        navigation = _run_selected_imports(
            imports,
            caps=caps,
            base_now=base_now,
            folder=folder,
            selected_agents=selected_agents,
            telemetry=telemetry,
            progress_header=progress_header,
            completed=completed,
        )
        if navigation is not tui.BACK:
            return imports
        # Keep the unanswered choices. Lanes already started or explicitly
        # skipped must not run again just because a later page went Back.
        defaults = set(imports) - completed


def _run_selected_imports(
    imports,
    *,
    caps,
    base_now,
    folder,
    selected_agents,
    telemetry,
    progress_header: Callable[[float], Sequence[str]] | None = None,
    completed: set | None = None,
):
    """The same reviewed import lanes for setup and the main-menu selector."""
    from probe.cli import import_jobs_ui, setup, tui
    from probe.cli.actions import Action

    notices: list[str] = []
    show_status = False
    completed = set() if completed is None else completed
    with tui.onboarding(lambda: progress_header(0.0) if progress_header else []):
        if setup.BackfillChoice.PAST_SESSIONS in imports:
            session_lines = _import_past_sessions(
                interactive=True,
                background=True,
                back_to_selection=True,
            )
            if session_lines is tui.BACK:
                return tui.BACK
            completed.add(setup.BackfillChoice.PAST_SESSIONS)
            show_status = session_lines is not None
            if session_lines:
                notices.extend([*session_lines, ""])
        if setup.BackfillChoice.PROJECT_FOLDER in imports:
            folder_lines = _run_wizard_action(
                Action.BACKFILL,
                caps=caps,
                base_now=base_now,
                yes=False,
                tracking=None,
                capture=None,
                auto_update=None,
                agent_rules=None,
                uninstall=False,
                configured=True,
                folder=folder,
                # The selector already asked about session history separately.
                transcripts=False,
                selected_agents=selected_agents,
                telemetry=telemetry,
                back_to_selection=True,
            )
            if folder_lines is tui.BACK:
                return tui.BACK
            completed.add(setup.BackfillChoice.PROJECT_FOLDER)
            show_status = show_status or folder_lines is not None
            if folder_lines:
                notices.extend([*folder_lines, ""])
    if progress_header is not None or not show_status:
        # Setup finishes with the dashboard handoff page, even if imports were
        # skipped. The main-menu import path still opens the live monitor.
        return
    with tui.onboarding(lambda: progress_header(1.0) if progress_header else []):
        navigation = import_jobs_ui.show_imports(
            onboarding=progress_header is not None,
            notices=notices,
        )
    if navigation is import_jobs_ui.Navigation.EXIT:
        _exit_wizard()


def _import_past_sessions(
    *,
    interactive: bool,
    background: bool = False,
    back_to_selection: bool = False,
):
    """Run the transcript import lane.

    Shared by onboarding, the main-menu import selector, and the legacy
    transcript-only command. Each uses the same census, review and receipts.

    It used to resolve a local coding agent to summarize with first. That is
    gone with the server-side digest lane: there is no agent to pick, no
    picker to back out of, and the lane always runs.
    """
    from probe.cli import backfill_transcripts as transcripts_mod

    return transcripts_mod.run_lane(
        client=_backfill_client(),
        interactive=interactive,
        background=background,
        back_to_selection=back_to_selection,
    )


def _run_wizard_action(
    chosen_action,
    *,
    caps,
    base_now: str,
    yes: bool,
    tracking,
    capture,
    auto_update,
    agent_rules,
    uninstall: bool,
    configured: bool,
    folder: str | None = None,
    transcripts: bool | None = None,
    selection_override=None,
    authorization_needs: list[str] | None = None,
    capture_sources: list[str] | None = None,
    authorization_context: dict | None = None,
    progress_header: Callable[[float], Sequence[str]] | None = None,
    selected_agents: tuple[str, ...] | list[str] | None = None,
    caps_by_source: dict | None = None,
    telemetry: "probe_telemetry.TelemetryContext | None" = None,
    install_code: str | None = None,
    installation_completion: _InstallationCompletion | None = None,
    back_to_selection: bool = False,
    default_state: str | None = None,
    recorder: str | None = None,
) -> list[str] | None:
    """Perform ONE action and RETURN its output.

    Returned, not printed, so the caller can decide whether this is a centred
    page of the wizard or plain command output. An empty list means the action
    already streamed (the configure path has to, because a browser approval
    prints a URL you are meant to read while it waits). None means nothing
    happened at all -- a pure back-out -- so the caller skips even the
    "press enter" pause and goes straight back to the menu.
    """
    import time

    from probe.cli import actions as actions_mod
    from probe.cli import capabilities
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli import telemetry as telemetry_mod

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    from probe.cli import tui
    from probe.cli.capabilities import Capability
    from probe.cli.capture import OffMode

    if chosen_action in actions_mod.ACCOUNT_ACTIONS:
        return _run_account_action(
            chosen_action,
            caps=caps,
            base_now=base_now,
            yes=yes,
            sources=tuple(selected_agents or (caps.agent_source,)),
            telemetry=tel,
        )

    if chosen_action is actions_mod.Action.RECORDER:
        return _run_recorder_action(
            yes=yes,
            caps_by_source=caps_by_source,
            base_now=base_now,
            chosen=recorder,
            telemetry=tel,
            agent_rules=agent_rules,
        )

    if chosen_action is actions_mod.Action.DEFAULTS:
        return _run_defaults_action(yes=yes, base_now=base_now, chosen=default_state)

    if chosen_action is actions_mod.Action.SETTINGS:
        return _run_settings_action(
            yes=yes,
            caps_by_source=caps_by_source,
            base_now=base_now,
            telemetry=tel,
        )

    if chosen_action is actions_mod.Action.IMPORT_JOBS:
        from probe.cli import import_jobs, import_jobs_ui

        if not wizard.interactive():
            return [
                f"{job['label']}: {job['state']} ({job['id']})" for job in import_jobs.list_jobs()
            ]
        if import_jobs_ui.show_imports() is import_jobs_ui.Navigation.EXIT:
            _exit_wizard()
        return None

    if chosen_action is actions_mod.Action.DIAGNOSE:
        lines = doctor_impl.render(caps).splitlines()
        notes = actions_mod.troubleshooting(caps)
        if notes:
            lines += ["", "If something is not working:"]
            lines += [f"  - {note}" for note in notes]
        return lines

    if chosen_action is actions_mod.Action.UPDATE:
        from probe.cli.upgrading import perform_update

        # No "Upgrade the CLI now?" gate: picking "Update to the latest
        # version" from the menu IS the answer to that question, and asking it
        # again dropped a bare uncentred prompt into the middle of the wizard.
        # perform_update returns its lines rather than streaming, so without
        # the spinner this sits silent for the whole `uv tool upgrade` +
        # plugin update -- the longest unexplained wait the wizard had.
        with tui.working("Updating the CLI and plugins"):
            outcome = perform_update(base_url=base_now, include_plugin=True)
        lines = list(outcome.lines)
        if outcome.restart_needed:
            agent_name = wizard.agent_label(caps.agent_source)
            lines += ["", f"Restart {agent_name} to apply the plugin update."]
        # The pointer block lives in the researcher's home directory, so no
        # release can reach it: updating the CLI ships new POINTER_BODY wording
        # that the installed block never picks up, and this action -- the one an
        # upgrading machine actually takes -- used to leave it on whatever
        # version it was first written at. Gated on already-installed-and-stale,
        # so a machine that declined the block stays declined; `want=True` here
        # would install one behind the researcher's back.
        #
        # A process cannot write wording it does not have, so the refresh lands
        # on the first invocation AFTER the upgrade, not this one. It converges;
        # it is not instant.
        if caps.agent_rules_stale:
            lines += wizard.apply_agent_rules(True, stale=True)
        lines += _register_local_capabilities(
            doctor_impl.collect(),
            settings=resolve(base_url=base_now),
        )
        return lines

    if chosen_action is actions_mod.Action.MANUAL:
        return [
            *actions_mod.manual_steps(
                base_url=base_now,
                agent_source=selected_agents or caps.agent_source,
            ).splitlines(),
            "",
            *actions_mod.self_host_notes(
                base_url=base_now, mcp_endpoint="https://mcp.research.prbe.ai/mcp"
            ).splitlines(),
        ]

    if chosen_action is actions_mod.Action.UNINSTALL:
        if not yes and wizard.interactive():
            tui.clear()
            if wizard.confirm_removal(caps.agent_source) is not True:
                # None, not []: nothing happened. The caller reads that as a
                # pure back-out -- no "press enter" on an empty page, no state
                # re-read -- and, since this action now ends by signing the
                # device out, it is also what keeps a declined removal from
                # clearing the credentials anyway.
                return None
        # Preserve the credential in memory long enough to report the actual
        # post-removal state. `finish_removal` -- once for the device, after
        # every selected agent has been through here -- revokes it and clears
        # it off the disk, so this is the last pass that can still publish.
        settings_before_removal = resolve(base_url=base_now)
        lines = list(wizard.remove_everything(caps))
        lines += _register_local_capabilities(
            doctor_impl.collect(),
            settings=settings_before_removal,
        )
        return lines

    if chosen_action is actions_mod.Action.IMPORT_RESEARCH:
        if yes or not wizard.interactive():
            raise typer.BadParameter(
                "import-research needs an interactive selection. "
                "Use --action backfill or --action transcripts for a direct import."
            )
        sources = tuple(selected_agents or (caps.agent_source,))
        _select_and_run_imports(
            caps=caps,
            base_now=base_now,
            folder=folder,
            selected_agents=sources,
            telemetry=tel,
        )
        return None  # The monitor already handled returning to the main menu.

    if chosen_action is actions_mod.Action.TRANSCRIPTS:
        # Retained for --action transcripts; the menu uses the shared selector.
        return _import_past_sessions(
            interactive=wizard.interactive(),
            background=wizard.interactive(),
        )

    if chosen_action is actions_mod.Action.BACKFILL:
        from pathlib import Path

        from probe.cli import backfill as backfill_impl

        return backfill_impl.run(
            client_factory=_backfill_client,
            start=Path.cwd(),
            folder=Path(folder) if folder else None,
            interactive=wizard.interactive(),
            background=wizard.interactive(),
            back_to_selection=back_to_selection,
            telemetry=tel,
            # The direct --action backfill path IS `probe backfill`, and the
            # two doors must offer the same thing: without this the command
            # offered the conversations at their gate and the menu silently did
            # not. Interactive-only for the same reason the command is -- the
            # lane's own gate is where consent happens.
            # Onboarding already asked about sessions independently of the
            # folder. Standalone folder imports still offer their own gate.
            transcripts=wizard.interactive() if transcripts is None else transcripts,
        )

    # CONFIGURE. NON-INTERACTIVE, always: the install steps are asked ONCE by
    # `wizard()`, before the per-agent apply loop, and arrive here as
    # `selection_override`. This used to ask them itself -- which meant a
    # two-agent run asked them once per agent, and, worse, that Back could only
    # unwind to the caller (which read it as "quit") because the screen before
    # this one belonged to a different function.
    configure_t0 = time.monotonic()

    def register_configure(current, *, complete=True):
        settings = resolve(base_url=base_now)
        if installation_completion is not None:
            return installation_completion.register(current, settings=settings, complete=complete)
        return _register_local_capabilities(current, settings=settings, complete=complete)

    selection = selection_override or wizard.resolve_selection(
        caps,
        tracking=tracking,
        capture=capture,
        auto_update=auto_update,
        agent_rules=agent_rules,
        configured=configured,
    )
    # pi used to be forced capture-only here. Its three stated reasons -- "no
    # marketplace plugin, no MCP server, no global-instructions file this run
    # could install" -- are no longer true: the packages entry installs the
    # extension, skills AND the MCP manifest together (pi_config), and
    # agent_rules.memory_path() has resolved pi's own ~/.pi/agent/AGENTS.md
    # since #1089. pi reads that file (its --no-context-files flag exists to
    # turn exactly this off), so the tracking block reaches the model.
    #
    # The force was also self-reinforcing: TRACKING is what requests the `mcp`
    # grant, that grant is what writes `mcp_token`, and `mcp_token` is what the
    # extension's own bearer fast path (src/mcpAuth.ts) reads. Refusing
    # tracking guaranteed the token was never minted, so every pi user fell
    # through to /probe-mcp-login's interactive OAuth -- the "Known limitation"
    # the README documents. The limitation WAS this branch.
    steps = wizard.plan(caps, selection)
    mcp_token_drifted = selection.tracking and wizard.codex_mcp_token_drifted()
    if (
        not steps
        and not authorization_needs
        and not mcp_token_drifted
        and not (selection.capture and caps.legacy_capture_plugin_installed)
    ):
        tel.emit(
            telemetry_mod.EVENT_WIZARD_CONFIGURE_STARTED,
            plan_steps=0,
            needs_authorization=False,
            already_configured=configured,
        )
        tel.emit(
            telemetry_mod.EVENT_WIZARD_CONFIGURE_COMPLETED,
            outcome=telemetry_mod.ConfigureOutcome.SUCCESS,
            no_changes=True,
            duration_seconds=int(time.monotonic() - configure_t0),
        )
        return [
            "Already set up the way you asked. Nothing to change.",
            *register_configure(caps),
        ]

    # From here it STREAMS, through a Progress screen that redraws on every
    # state change. Installing a plugin shells out to `claude` and a browser
    # approval prints a URL you are meant to act on while it waits, so this
    # page cannot be buffered -- it is written while it happens. It used to
    # collect every message and print them only after all four steps returned,
    # which showed a blank screen for as long as the subprocesses took.
    # The single retry BUDGET for this run. install_plugin() calls it to ask
    # whether it may try again; the first caller to fail spends it. Per-plugin
    # retries would multiply refreshes by the number of failures, which is how
    # a fix for a 3-minute wait turns into a 30-minute one.
    _retry_budget = [1]

    def _may_retry() -> bool:
        if _retry_budget[0] <= 0:
            return False
        _retry_budget[0] -= 1
        return True

    # THE WORK LIST, built before anything renders. Deliberately NOT `steps`
    # from plan(): the two stopped being 1:1 the moment plan() learned to say
    # "sign in" for a machine whose plugin is already installed. Indexing one
    # by the other's position left the bar pinned at 0/2 while the run did its
    # real work in the authorization phase, which no step covered.
    #
    # The install decision reads the PLUGIN fact, not the composite capability.
    # `caps.tracking_on` is "plugin installed AND logged in", and `capture_on`
    # does not look at the plugin at all -- so a machine with both plugins
    # present but no credential yet read as "both off" and reinstalled both.
    # Measured: `claude plugin install` on an already-installed plugin returns
    # "already installed" and does NOT upgrade it, so that work was pure waste
    # -- and it was the step that failed, on the one path a new user is on.
    needs = (
        authorization_needs
        if authorization_needs is not None
        else _needs_for_this_run(wizard.needs_authorization(caps, selection), yes=yes)
    )
    tel.emit(
        telemetry_mod.EVENT_WIZARD_CONFIGURE_STARTED,
        tracking=selection.tracking,
        capture=selection.capture,
        auto_update=selection.auto_update,
        agent_rules=selection.agent_rules,
        plan_steps=len(steps),
        needs_authorization=bool(needs),
        already_configured=configured,
    )
    # (label, action, gate). `gate` names the capability whose credential this step
    # cannot work without, and is None for steps that need none -- removals,
    # auto-update, the CLAUDE.md block. It is what stops a run whose browser
    # approval failed from installing a plugin that then sits there unauthenticated:
    # the tracking plugin publishes an MCP server, and an unauthenticated connect is
    # answered with a `WWW-Authenticate` challenge that pins Claude Code to OAuth.
    # Turning a capability OFF is deliberately ungated -- refusing to uninstall
    # because a credential could not be minted would trap someone on a plugin they
    # just asked to remove.
    work: list[tuple[str, object, object]] = []

    # Whether the selected agent's own CLI is on this machine. A plugin install
    # shells out to it, so without it the step can only fail — and on the
    # degraded install path the confirm screen has already SAID the plugins
    # are skipped, so failing at them anyway would contradict the screen. The
    # honest step is a skip that names the recovery.
    if caps.agent_source == "pi":
        # pi has no marketplace CLI a plugin-install step could shell out to
        # (see wizard.INSTALLABLE_AGENT_SOURCES) -- there is no "is it on
        # this machine" question to ask here, because nothing below ever
        # attempts a plugin install for pi (apply_capture()/install_plugin()
        # refuse it themselves; see their own pi guards). True rather than
        # False specifically so a pi run never shows the "Skipped ... —
        # Claude Code is not on this machine" message, which used to fire
        # here (via the old ternary's silent claude_code default) for a run
        # that was never about Claude Code at all.
        agent_here = True
        agent_name = wizard.agent_label(caps.agent_source)
    elif caps.agent_source == plugin_cli.KIMI:
        # Kimi Code's plugins are files the wizard writes (kimi_config); it
        # still needs the agent itself on the machine to be worth installing.
        from probe.cli import kimi_config

        agent_here = kimi_config.binary_available()
        agent_name = wizard.agent_label(caps.agent_source)
    else:
        agent_here = caps.codex_available if caps.agent_source == "codex" else caps.claude_available
        agent_name = "Codex" if caps.agent_source == "codex" else "Claude Code"

    def _skip_plugin(what: str):
        return lambda: [
            f"Skipped {what} — {agent_name} is not on this machine. "
            "After installing it, run `probe wizard` and pick “Install Probe”."
        ]

    if selection.tracking and not caps.tracking_plugin_installed:
        if agent_here:
            work.append(
                (
                    "install the CLI + MCP plugin",
                    lambda: wizard.apply_tracking(True, on_retry=_may_retry),
                    Capability.TRACKING,
                )
            )
        else:
            work.append(("skip the CLI + MCP plugin", _skip_plugin("the CLI + MCP plugin"), None))
    elif not selection.tracking and caps.tracking_plugin_installed:
        work.append(("remove the CLI + MCP plugin", lambda: wizard.apply_tracking(False), None))

    if (
        selection.tracking
        and caps.agent_source == "codex"
        and agent_here
        and caps.mcp_authenticated is not True
        # The daemon profile's plugin carries no MCP to log in to.
        and not wizard.daemon_records(caps.agent_source)
    ):
        # `agent_here` gates this like the installs: `codex mcp login` shells
        # out to the absent binary, and a failed step right after a screen
        # that said the coding-agent work is skipped contradicts the screen.
        work.append(
            (
                "authenticate the Codex MCP",
                wizard.apply_codex_mcp_auth,
                Capability.TRACKING,
            )
        )
    elif mcp_token_drifted:
        # THE REPAIR NEEDS ITS OWN SIGNAL, because every other gate on this
        # screen closes in exactly the state that needs repairing:
        #
        #   * needs_authorization() reads `mcp` as held whenever a read token
        #     is saved, stale or not, so a signed-in device never re-enters
        #     authorize() and never reaches the sync inside it.
        #   * the branch above wants `mcp_authenticated is not True`, but
        #     `codex mcp list` answers `bearer_token` for a DEAD header, so
        #     this reads as authenticated precisely when it is not.
        #   * and it wants agent_source == "codex", which a machine running
        #     both agents does not report.
        #
        # `probe doctor` tells people to run this command; before this branch
        # existed the command did nothing for them, which is the doctor/wizard
        # circle this repo has paid for before (see `plan()`'s AGENT_RULES
        # comment). The drift check is two file reads and self-guarding, so it
        # is cheap to ask on every run and a no-op on a healthy machine.
        work.append(
            (
                "re-point the Codex MCP at your current read token",
                wizard.sync_codex_mcp_token,
                Capability.TRACKING,
            )
        )

    if selection.capture and not agent_here and not caps.capture_plugin_installed:
        work.append(
            ("skip the Session capture plugin", _skip_plugin("the Session capture plugin"), None)
        )
    elif selection.capture and (
        not caps.capture_plugin_installed
        or not caps.capture_on
        or caps.legacy_capture_plugin_installed
    ):
        # NOT gated on "plugin absent": the killswitch is cleared here too, and
        # a killswitched machine with the plugin already installed needs that
        # clear or capture stays off while the run reports success.
        # apply_capture skips the install itself when the plugin is present, so
        # this cannot reintroduce the reinstall.
        if caps.agent_source not in wizard.INSTALLABLE_AGENT_SOURCES:
            # pi: capture_plugin_installed is always False here (see
            # capabilities.installed_plugins()'s pi guard), which would
            # otherwise pick "install the Session capture plugin" below --
            # a label starting with "install" is exactly what the
            # marketplace-refresh trigger a few lines down keys on, and
            # apply_capture() itself now refuses any actual plugin install
            # for pi (see its own guard). The work IS real -- clear the
            # killswitch, let the token authorize() already minted take
            # effect -- it is just never a plugin install for pi.
            capture_label = "pair Session capture"
        elif not caps.capture_plugin_installed:
            capture_label = "install the Session capture plugin"
        elif caps.legacy_capture_plugin_installed:
            capture_label = "retire the legacy Session capture plugin"
        else:
            capture_label = "re-enable Session capture"
        work.append(
            (
                capture_label,
                lambda: wizard.apply_capture(caps, True, mode=OffMode.DISABLE, on_retry=_may_retry),
                Capability.CAPTURE,
            )
        )
    elif not selection.capture and (caps.capture_plugin_installed or caps.capture_on):
        work.append(
            (
                "turn Session capture off",
                lambda: wizard.apply_capture(
                    caps,
                    False,
                    mode=OffMode.UNINSTALL if uninstall else OffMode.DISABLE,
                ),
                None,
            )
        )

    if selection.auto_update != caps.auto_update_enabled:
        work.append(
            (
                f"{'enable' if selection.auto_update else 'disable'} automatic updates",
                lambda: wizard.apply_auto_update(selection.auto_update),
                None,
            )
        )
    if (
        selection.agent_rules != caps.agent_rules_installed
        or caps.agent_rules_stale
        or (not selection.agent_rules and wizard.leftover_team_note(caps))
    ):
        work.append(
            (
                f"write the rules into your global {wizard.instruction_files(caps.agent_source)}",
                lambda: wizard.apply_agent_rules(
                    selection.agent_rules, stale=caps.agent_rules_stale
                ),
                None,
            )
        )

    # The refresh is hoisted out of install_plugin (it used to run per plugin,
    # discarding both results), so the CALLER owns it now -- and owning it means
    # actually doing it. Without this the first attempt installs from whatever
    # stale copy is on disk, which is the failure the original comment warned
    # about, and a machine that never added the marketplace fails attempt one
    # every time and is only repaired by the retry.
    #
    # Prepended, not appended: it has to happen BEFORE any install. And only
    # when something is actually being installed -- it is two `claude`
    # subprocesses, and the common re-run installs nothing.
    def _refresh() -> list[str]:
        """Adapts refresh_marketplace's Result to the message list a step returns.

        A failed refresh is REPORTED, not swallowed -- discarding it is what
        made the original bug present as Claude's downstream "not found in
        marketplace". It does not abort the run: the install can still succeed
        from the copy already on disk, and if it does not, the retry gets
        another go at the refresh.
        """
        result = wizard.refresh_marketplace()
        if result is not None and not getattr(result, "ok", True):
            from probe.cli import updater

            # Scrubbed like every other child output we print, and a Mac that
            # cannot run git gets its one-line fix, not Apple's paragraph.
            reason = updater.git_blocker(result.detail) or updater.clean_reason(result.detail)
            return [f"! could not refresh the marketplace: {reason}"]
        return []

    if any(label.startswith("install") for label, action, _ in work if action is not None):
        work.insert(0, ("refresh the plugin marketplace", _refresh, None))

    # The browser approval is REAL WORK and the longest wait in the run -- it
    # blocks on a human in a browser. Leaving it off the list is what made a
    # sign-in-only run sit at 0/2 with nothing moving.
    #
    # It goes FIRST, ahead of the marketplace refresh and both installs. The
    # tracking plugin ships an `.mcp.json` pointing at the hosted MCP, and the
    # credential it serves is the one this step mints -- so installing before
    # signing in publishes a server that provably cannot authenticate, for as
    # long as a human takes to approve it in a browser. Claude Code answering a
    # connect in that window gets a 401 carrying a `WWW-Authenticate` challenge,
    # discovers an authorization server from it, and pins the server to OAuth:
    # the user then has to go to `/mcp` and authenticate a device this very run
    # had already authorized. Credential first, and the window does not exist.
    auth_index = 0 if needs else None
    if needs:
        work.insert(0, (f"sign in ({', '.join(needs)})", None, None))

    tui.clear()
    progress = tui.Progress(
        "This run will:", [label for label, _, _ in work], overall=progress_header
    )
    progress.render()

    skipped: list[str] = []

    def _run_step(index: int, label: str, fn) -> list[str]:
        """Run one apply step, unless the phase has already run out of time.

        The budget refuses to START work; it never interrupts a step already in
        flight. A `claude plugin install` killed mid-write is how a plugin cache
        gets corrupted, so a slow step is allowed to finish on its own timeout.
        """
        if time.monotonic() > deadline:
            skipped.append(label)
            return []
        progress.start(index)
        try:
            out = list(fn())
        except Exception as exc:  # noqa: BLE001 - one bad step must not eat the rest
            progress.finish(index, ok=False)
            progress.note(f"! {label}: {exc}")
            return []
        # A step reports failure in prose, not by raising: the apply_* helpers
        # return "could not install ..." strings. The classifier lives next to
        # the producers in setup.py so a reworded message cannot leave the tick
        # mark disagreeing with the line printed underneath it.
        ok = not any(wizard.reports_failure(m) for m in out)
        progress.finish(index, ok=ok)
        if out:
            progress.note(*out)
        return out

    granted: dict = {}
    if needs:
        # Snapshot BEFORE the mint: the always-browser install re-mints on a
        # signed-in device, and the token being replaced has to be read while
        # it is still the stored one — after `authorize` persists, it is gone
        # locally and can only be revoked from this copy.
        from probe.sdk.config import load_context

        try:
            previous_context = load_context() or {}
        except Exception:  # noqa: BLE001 - an unreadable config just skips the revoke
            previous_context = {}
        progress.start(auth_index)
        progress.note(
            "",
            "Signing in with the website code…"
            if install_code
            else f"One browser approval covers everything listed ({', '.join(needs)}).",
        )
        try:
            granted, auth_messages = wizard.authorize(
                needs,
                base_url=base_now,
                capture_sources=capture_sources,
                client_context=authorization_context,
                on_prompt=lambda prompt: progress.note(
                    f"  visit: {prompt.verification_uri_complete}",
                    f"  code:  {prompt.user_code}",
                ),
                open_browser=True,
                **({"install_code": install_code} if install_code is not None else {}),
            )
        except OnboardingRequired as exc:
            _finish_website_onboarding(exc)
        signed_in_ok = not [g for g in needs if g not in granted]
        progress.finish(auth_index, ok=signed_in_ok)
        if auth_messages:
            progress.note(*auth_messages)
        if install_code is not None and not signed_in_ok:
            raise typer.Exit(1)
        revoked = wizard.revoke_replaced_token(previous_context, granted, base_url=base_now)
        if revoked:
            progress.note(*revoked)
        if install_code is not None and signed_in_ok:
            # THE OTHER HALF of the account-switch gate at the top of `wizard`.
            # That gate could only name the account being replaced — a website
            # code is opaque until it is redeemed — so this is the first point
            # at which the account it selected can be stated at all, and a
            # guided install otherwise finished without ever saying whose data
            # it is now writing. A courtesy, never load-bearing: the credential
            # is already saved, so an endpoint that goes unreachable one call
            # after the exchange costs a line of output and nothing else (the
            # same rule `sign_in` applies to its own version of this line).
            switched_to = wizard.account_email(base_now)
            if switched_to:
                progress.note(f"Signed in as {switched_to}.")
        tel.emit(
            telemetry_mod.EVENT_WIZARD_SIGNED_IN,
            outcome=(
                telemetry_mod.SignInOutcome.SUCCESS
                if signed_in_ok
                else telemetry_mod.SignInOutcome.FAILED
            ),
            grants_needed=len(needs),
        )

    # Started AFTER the approval, not before it. The budget bounds the work this
    # process does; the browser approval is a human deciding, and clocking it
    # against the same 300s would let a slow reader consume the entire budget and
    # leave every install "stopped without starting" -- a run that signed in and
    # installed nothing.
    deadline = time.monotonic() + wizard.PHASE_BUDGET_S

    ungranted: list[str] = []

    for position, (label, action, gate) in enumerate(work):
        if action is None:
            continue  # the authorization step, run above
        # The gate. Installing a plugin whose credential this run tried and failed
        # to mint is how a cancelled browser approval still leaves an `.mcp.json`
        # on disk with nothing behind it -- and an unauthenticated connect is
        # answered with a `WWW-Authenticate` challenge, which pins Claude Code to
        # OAuth. The user is then sent to `/mcp` to authenticate a device that was
        # never authorized at all. Refusing the install leaves the machine in the
        # state it was already in, which is the honest outcome of a refused
        # approval, and `probe wizard` re-run is the repair.
        blocked = (
            wizard.blocked_by_missing_grants(gate, needed=needs, granted=granted)
            if gate is not None
            else []
        )
        if blocked:
            ungranted.append(label)
            progress.finish(position, ok=False)
            progress.note(f"! skipped {label} — no credential for {', '.join(blocked)}.")
            continue
        _run_step(position, label, action)

    if skipped:
        progress.note(
            f"! stopped after {wizard.PHASE_BUDGET_S:.0f}s without starting: "
            f"{', '.join(skipped)}. Re-run `probe wizard` to finish."
        )

    # THE VERDICT. Verify the postcondition rather than trusting the install
    # command: on the run that prompted this fix both installs reported failure
    # while both plugins were in fact present, so believing the exit status
    # would have cried wolf. `plugins.missing()` answers only when it actually
    # managed to look -- an absent `claude` is normal on a GPU pod and must
    # never be reported as a failed install.
    # ONE re-collect, reused. collect() already runs `claude plugin list`, so
    # asking installed_plugins() again would pay for the same subprocess twice.
    after = doctor_impl.collect()
    wanted_plugins = []
    if selection.tracking and not after.tracking_plugin_installed:
        wanted_plugins.append(capabilities.tracking_plugin_name(caps.agent_source))
    if selection.capture and not after.capture_plugin_installed:
        wanted_plugins.append(capabilities.TAP_PLUGIN_NAME)
    # Only names we VERIFIED absent. An unanswerable question is not a negative
    # answer: `claude` missing is normal on a GPU pod and must never read as a
    # failed install.
    absent = wanted_plugins if after.plugins_verified else []

    missing = [grant for grant in needs if grant not in granted]
    runtime_failures: list[str] = []
    if selection.capture and after.capture_credential_valid is False:
        runtime_failures.append("the capture credential is rejected")
    if selection.capture and after.legacy_capture_plugin_installed:
        runtime_failures.append("the legacy Codex capture plugin is still installed")
    if selection.tracking and after.agent_source == "codex" and after.mcp_authenticated is False:
        runtime_failures.append("the Codex MCP is not logged in")

    if missing or absent or runtime_failures:
        # "Restart Claude Code to finish" after a FAILED run reads as success:
        # the user restarts, finds the capability off, and has no idea why.
        reasons = []
        if absent:
            # A gated skip is not a failed install, and saying so sends the user
            # to debug `claude plugin install` when the actual fault was the
            # approval they cancelled two steps earlier. The credential is named
            # separately below; this clause only has to stop claiming an attempt
            # that never happened.
            verb = "were not installed" if ungranted else "did not install"
            reasons.append(f"these plugins {verb}: {', '.join(absent)}")
        if missing:
            reasons.append(f"no credential for: {', '.join(missing)}")
        reasons.extend(runtime_failures)
        tel.emit(
            telemetry_mod.EVENT_WIZARD_CONFIGURE_COMPLETED,
            outcome=telemetry_mod.ConfigureOutcome.FAILED,
            failure_kind=(
                telemetry_mod.ConfigureFailureKind.MISSING_GRANTS
                if missing
                else telemetry_mod.ConfigureFailureKind.PLUGINS_ABSENT
                if absent
                else telemetry_mod.ConfigureFailureKind.RUNTIME
            ),
            steps_skipped=len(skipped),
            duration_seconds=int(time.monotonic() - configure_t0),
        )
        progress.note(
            "", f"Not finished — {'; '.join(reasons)}.", "Re-run `probe wizard` to retry."
        )
        progress.close()
        # complete=False: this run did NOT finish, and the dashboard treats a
        # fresh registration as the install completing. Reporting the observed
        # state here made a failed install advance onboarding to the next step
        # and flip the approval page to Installed.
        for message in register_configure(after, complete=False):
            tui.say(message)
        raise typer.Exit(1)

    if wanted_plugins and not after.plugins_verified:
        # Could not ask. Say so rather than claiming either outcome.
        progress.note(
            "",
            f"Could not confirm the plugins are installed ({wizard.agent_label(caps.agent_source)} did not answer). "
            "Run `probe doctor` to check.",
        )
    tel.emit(
        telemetry_mod.EVENT_WIZARD_CONFIGURE_COMPLETED,
        outcome=(
            telemetry_mod.ConfigureOutcome.UNVERIFIABLE
            if wanted_plugins and not after.plugins_verified
            else telemetry_mod.ConfigureOutcome.SUCCESS
        ),
        tracking_newly_installed=bool(
            selection.tracking
            and not caps.tracking_plugin_installed
            and after.tracking_plugin_installed
        ),
        tracking_already_present=bool(selection.tracking and caps.tracking_plugin_installed),
        capture_newly_installed=bool(
            selection.capture
            and not caps.capture_plugin_installed
            and after.capture_plugin_installed
        ),
        capture_already_present=bool(selection.capture and caps.capture_plugin_installed),
        steps_skipped=len(skipped),
        duration_seconds=int(time.monotonic() - configure_t0),
    )
    progress.note_next(*wizard.restart_notice(caps, selection))
    progress.close()
    for message in register_configure(
        after,
        complete=not skipped and not (wanted_plugins and not after.plugins_verified),
    ):
        tui.say(message)

    return []


def _run_defaults_action(
    *, yes: bool, base_now: str | None = None, chosen: str | None = None
) -> list[str] | None:
    """The main menu's Defaults row: this machine's default for new sessions.

    `chosen` is a state already picked elsewhere (`wizard.DefaultChoice`; the
    menu row itself saves on each press now); without one, the picker opens
    (`run_defaults_menu`), where `→` saves and so does leaving after a change. The states are on / read / off; whether the daemon records is the
    "Who records" setting, which mints and revokes the daemon's key
    (`setup.apply_recorder`).
    """
    from probe.cli import setup as wizard
    from probe.cli import tui

    report = ["Probe in new sessions:", *wizard.describe_settings()]
    if yes or not wizard.interactive():
        # A screen nobody can answer must not answer for them.
        return [*report, "", "`probe session default on|read|off` sets it."]
    # The THREE-valued override, not the boolean one: `PROBE_SESSION_STATE`
    # holds this default down just as hard, and a picker drawn under it would
    # write a value that changes nothing anyone can see (the 0.96.0 rule: a
    # control that cannot do what it says does not get drawn).
    if session_marker.state_env_override() is not None:
        return [*report, "", "Unset that variable to choose the default here."]

    current = wizard.setting_state(session_marker.default_session_state())
    if chosen is not None:
        picked = wizard.setting_state(chosen)
    else:
        tui.clear()
        picked = wizard.run_defaults_menu(current)
    if picked is None or picked is tui.BACK or picked == current:
        return None  # backed out, or chose what it already was: nothing happened
    lines = wizard.apply_settings({wizard.Setting.TRACKING_DEFAULT: picked})
    if chosen is not None and len(lines) == 1 and not wizard.reports_failure(lines[0]):
        # Saved from the menu row with nothing else to say: the menu comes
        # straight back, and the row itself is the confirmation -- it now
        # wears the saved state. A page to press through would be a second
        # confirmation of the one keystroke that already was one.
        return None
    return lines


def _run_settings_action(
    *,
    yes: bool,
    caps_by_source: dict | None = None,
    base_now: str | None = None,
    telemetry=None,
) -> list[str] | None:
    """The settings screen: automatic updates. Who records and what the daemon
    sees are on the main menu's Defaults (`_run_recorder_action`).

    Tracking, capture and the instruction rules had rows here and do not any
    more: Probe is installed whole and removed whole (see setup.py's module
    docstring). The default for new sessions moved to the main menu
    (`_run_defaults_action`). Nothing is written while you toggle; `Set
    settings ›` commits the DIFF.

    Automatic updates applies through the CONFIGURE machinery
    (`_apply_capability_settings`) rather than a bare write, so the toggle and
    an Install are the same code asking for a different end state.
    """
    from probe.cli import setup as wizard
    from probe.cli import tui

    caps_by_source = caps_by_source or {}
    if yes or not wizard.interactive():
        # A screen nobody can answer must not answer for them: report state
        # and name the commands that set things headlessly. The capability
        # rows ride along when the caller had snapshots — read with the SAME
        # predicates the interactive boxes use, so headless and interactive
        # can never describe the same machine differently.
        capability_lines: list[str] = []
        if caps_by_source:
            state = wizard.read_settings(caps_by_source)
            cycles = wizard.cycling_settings()
            recorder = wizard.machine_recorder()
            # Who records is ONE value for the machine; what the daemon sees
            # matters only where it records.
            hidden = {*wizard.RECORDER_SETTINGS}
            if recorder != session_marker.RECORDER_DAEMON:
                hidden.add(wizard.Setting.REASONING_SUMMARIES)
            capability_lines.append(f"  {wizard.RECORDER_ROW_TITLE:<28} {recorder}")
            for setting in wizard.Setting:
                if setting in hidden:
                    continue
                title, _detail = wizard.SETTINGS_COPY[setting]
                if setting in cycles:
                    # Three-valued rows say their WORD, not on/off: "off" here
                    # would be indistinguishable from `read`, which is the one
                    # pair a person reading this block must be able to tell
                    # apart -- one of them still searches the team's history.
                    value = wizard.value_label(setting, wizard.cycle_value(setting, state[setting]))
                else:
                    value = "on" if state[setting] else "off"
                capability_lines.append(f"  {title:<28} {value}")
        return [
            "Settings on this device:",
            *capability_lines,
            *([] if caps_by_source else wizard.describe_settings()),
            "",
            "`probe session default on|read|off` sets the default for new sessions.",
            "`probe wizard --auto-update/--no-auto-update` sets automatic updates.",
            *(
                ["`showThinkingSummaries` (Claude Code's settings.json) and `model_reasoning_summary`",
                 "(Codex's config.toml) are whether the daemon sees the agent's reasoning."]
                if caps_by_source and wizard.Setting.REASONING_SUMMARIES not in hidden
                else []
            ),
        ]

    # The interactive screen without the device's snapshots would draw the
    # Automatic updates box OFF regardless of reality, and a commit would
    # iterate zero agents — a lying screen over a silent no-op. The one
    # production call site always passes them; hold the next one to that.
    if not caps_by_source:
        raise AssertionError("interactive settings needs the device's capability snapshots")

    tui.clear()
    # ONE read feeds both the boxes the screen draws and the diff computed
    # against what comes back. Reading again at apply time would reopen the
    # gap: a config change landing while the prompt sat open would make the
    # screen and the write disagree.
    current = wizard.read_settings(caps_by_source)
    picked = wizard.run_settings_menu(current)
    if picked is None or picked is tui.BACK:
        return None  # backed out: nothing happened, nothing to pause on
    # `Set settings` commits the DIFF, not the picker state: unchanged boxes
    # are not rewritten. An empty diff is a no-op, straight back to the menu.
    # `!=`, not `is not`: a cycling row answers with a STATE NAME, and two equal
    # strings are not required to be the same object -- an identity diff would
    # report every unchanged state as a change and rewrite the config on exit.
    changes = {s: v for s, v in picked.items() if current.get(s) != v}
    if not changes:
        return None
    lines: list[str] = []
    capability_changes = {s: v for s, v in changes.items() if s in wizard.CAPABILITY_SETTINGS}
    if capability_changes:
        lines.extend(
            _apply_capability_settings(
                capability_changes,
                caps_by_source=caps_by_source,
                base_now=base_now or resolve(base_url=_conn.base_url).base_url,
                telemetry=telemetry,
            )
        )
    plain = {s: v for s, v in changes.items() if s not in wizard.CAPABILITY_SETTINGS}
    if plain:
        lines.extend(wizard.apply_settings(plain, caps_by_source=caps_by_source))
    return lines


def _run_recorder_action(
    *,
    yes: bool,
    caps_by_source: dict | None = None,
    base_now: str | None = None,
    chosen: str | None = None,
    telemetry=None,
    agent_rules: bool | None = None,
) -> list[str] | None:
    """The main menu's Who records row: the agent or the Probe daemon, ONE value
    for every coding agent on this device (Richard 2026-09-29).

    `chosen`: the row was switched (`←`/`→`), and the switch applies now, no
    Enter: each agent moves (`setup.apply_recorder`: plugins, the instruction
    block), and moving to the daemon asks for the daemon's own sign-in (the
    browser approval that mints its key) and then its page. A team the daemon
    is not open to (the server's answer) is told so and nothing moves.
    Without `chosen` (Enter on the row): the daemon's page, when it records.

    Every switch reports `wizard.recorder_changed` with how it ended, the
    server's refusal included (#probe-usage pings it).

    `agent_rules` is `--agent-rules/--no-agent-rules` beside `--who-records`:
    it decides each moved agent's instruction block, and None keeps whatever
    each file has (`setup.apply_recorder`).
    """
    from probe.cli import setup as wizard
    from probe.cli import telemetry as telemetry_mod

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    caps_by_source = caps_by_source or {}
    base = base_now or resolve(base_url=_conn.base_url).base_url
    current = wizard.machine_recorder()
    headless = yes or not wizard.interactive()
    if headless and chosen is None:
        return [f"{wizard.RECORDER_ROW_TITLE}: {current}", "",
                "`probe wizard` › Defaults › Who records switches it."]
    daemon = session_marker.RECORDER_DAEMON
    if chosen is None:
        if current != daemon:
            return None
        # Enter on the row while the daemon records also brings along any
        # set-up agent still recording itself: an agent that gained a daemon
        # profile in an update (pi, 2026-10) never moves on its own, because
        # who records decides what leaves the machine.
        behind = [
            source
            for source in wizard.RECORDER_SOURCES
            if source in caps_by_source
            and caps_by_source[source].configured
            and session_marker.recorder(source) != daemon
        ]
        if not behind:
            # Otherwise Enter is the daemon's repair: a key revoked on the
            # dashboard, or libraries gone after an update, have no other way
            # back in the wizard (switching away and back would revoke the key
            # and ask for a second approval).
            repaired = _ensure_daemon(base)
            page = _run_daemon_page(caps_by_source=caps_by_source)
            return [*repaired, *(page or [])] or None
        chosen = daemon
    sources = [source for source in wizard.RECORDER_SOURCES if source in caps_by_source]
    # SAY WHICH AGENTS STAY BEHIND: an agent with no daemon profile, if one is
    # ever set up. A switch that names only the agents it moved reads as "every
    # agent here" -- a customer with pi found out from what was missing
    # (2026-10-02). Only agents Probe is set up for.
    left_alone = [
        f"{wizard.agent_label(source)} keeps recording itself: it has no daemon profile yet."
        for source, snapshot in caps_by_source.items()
        if chosen == daemon and source not in wizard.RECORDER_SOURCES and snapshot.configured
    ]
    # An agent already on the chosen profile is left alone: moving it again
    # would reinstall a plugin its owner may have declined.
    pending = [source for source in sources if session_marker.recorder(source) != chosen]
    # Agents a pre-flight already kept on their profile (and said why).
    held: set[str] = set()
    # A rules flag beside the switch applies to agents already on the profile
    # too, and FIRST: it is a local edit that needs no sign-in, no daemon key
    # and no server's yes, and on a machine already on the daemon
    # `--who-records daemon --no-agent-rules` is the way to take out a block
    # the switch should never have written.
    lines: list[str] = []
    if agent_rules is not None:
        for source in sources:
            if source not in pending:
                lines.extend(wizard.apply_recorder_rules(source, chosen, agent_rules))
    # The rules edit above happened whatever stops the switch below.
    nothing = "Who records did not change" if lines else "nothing changed"
    unchanged = f"{nothing[0].upper()}{nothing[1:]}."
    if chosen == daemon and not resolve(base_url=base).token:
        # A signed-out machine would move every agent onto a profile with no
        # credential to record with. Back to the agent stays open: it is the
        # way off the daemon.
        return [*lines, "Sign in before switching Who records to the daemon (`probe wizard --action login`).",
                unchanged]
    if not sources:
        return ["No coding agent set up on this device has a daemon profile yet.", *left_alone, "Nothing changed."]
    from probe.cli import tui

    started = time.monotonic()

    def _report(outcome: "telemetry_mod.RecorderOutcome", moved: list[str]) -> None:
        tel.emit(
            telemetry_mod.EVENT_WIZARD_RECORDER_CHANGED,
            recorder=chosen,
            outcome=outcome,
            agents=moved,
            agent_count=len(sources),
            duration_seconds=round(time.monotonic() - started, 3),
        )

    if chosen == daemon:
        # The spinner, never a blank screen, while the server answers.
        with tui.working("Checking the Probe daemon is open to your team"):
            offered, note = wizard.daemon_availability(base_url=base)
        if offered is False:
            _report(telemetry_mod.RecorderOutcome.REFUSED_PLAN, [])
            return [*lines, note or wizard.DAEMON_UNAVAILABLE_NOTE, unchanged]
        # The daemon's key (a browser approval, only when missing or refused)
        # and its AI libraries (an install, only when missing, no approval),
        # OUTSIDE the spinner: the approval prints its link and waits on the
        # browser, and the install shows its own output (R12). Headless prints
        # the link and never opens a browser.
        from probe.cli.daemon_cli import ai_libraries

        lines.extend(_ensure_daemon(base, open_browser=not headless))
        if not wizard.companion_token_held():
            _report(telemetry_mod.RecorderOutcome.NO_KEY, [])
            return [*lines, f"! The daemon has no key, so {nothing}."]
        if ai_libraries() is None:
            _report(telemetry_mod.RecorderOutcome.NO_LIBRARIES, [])
            return [*lines, f"! The daemon's AI libraries are missing, so {nothing}."]
        # An agent whose daemon starts from its own capture (pi) pairs it here,
        # outside the spinner below: the approval prints a link to open. Its
        # package is checked (and updated) FIRST: pairing mints its capture
        # token, and a switch that then stopped on an old package would leave
        # it capturing on agent, which it did not do before.
        for source in pending:
            if wizard.needs_capture_pairing(source):
                with tui.working(f"Checking {wizard.agent_label(source)}'s Probe package"):
                    package = wizard.daemon_package_ready(source)
                lines.extend(package.lines)
                if not package.ok:
                    held.add(source)
                    continue
                lines.extend(wizard.pair_capture(source, base_url=base, open_browser=not headless))
    if not pending:
        _report(telemetry_mod.RecorderOutcome.MOVED, sources)
        everyone = "every coding agent here" if not left_alone else wizard.agent_label(tuple(sources))
        return [*lines, f"{wizard.RECORDER_ROW_TITLE}: already {chosen} for {everyone}.", *left_alone]
    # Plugin moves capture their own output, so the spinner owns the screen.
    with tui.working("Moving your coding agents to the daemon" if chosen == daemon
                     else "Moving your coding agents back to recording themselves"):
        for source in pending:
            if source not in held:
                lines.extend(wizard.apply_recorder(caps_by_source[source], chosen, base_url=base, rules=agent_rules))
    lines.extend(left_alone)
    # What each agent's config SAYS now, not which steps ran: `apply_recorder`
    # reports a failure as a line and keeps going.
    moved = [source for source in sources if session_marker.recorder(source) == chosen]
    _report(
        telemetry_mod.RecorderOutcome.MOVED if len(moved) == len(sources)
        else telemetry_mod.RecorderOutcome.PARTIAL if moved
        else telemetry_mod.RecorderOutcome.FAILED,
        moved,
    )
    if chosen == daemon and wizard.machine_recorder() == daemon and not headless:
        page = _run_daemon_page(caps_by_source=caps_by_source)
        lines.extend(page or [])
    return lines


def _needs_for_this_run(needs: list[str], *, yes: bool) -> list[str]:
    from probe.cli import setup as wizard

    return needs if not yes and wizard.interactive() else wizard.headless_needs(needs)


def _ensure_daemon(base: str, *, open_browser: bool = True) -> list[str]:
    """What the Probe daemon needs to record, fetched only where it is missing:
    its key (one browser approval, when none is saved or the server refuses the
    saved one) and its AI libraries (an install, no approval). Call it outside
    any spinner: the approval prints a link and waits on the browser."""
    from probe.cli import setup as wizard
    from probe.cli import tui
    from probe.cli.companion import provision_daemon
    from probe.cli.daemon_cli import ai_libraries

    refused = False
    if wizard.companion_token_held():
        with tui.working("Checking the Probe daemon's key"):
            refused = _daemon_key_refused(base)
    if not refused and wizard.companion_token_held() and ai_libraries() is not None:
        return []
    lines: list[str] = []
    if refused:
        # A refused key is dead weight: dropped first, so a declined approval
        # leaves NO key -- which every caller reads as "nothing moves" -- rather
        # than a saved key the server will not take.
        from probe.sdk.config import save_context

        save_context({"companion_token": None})
        lines.append("The server refuses the Probe daemon's key, so it needs a new one.")
    return [*lines, *provision_daemon(base, open_browser=open_browser)]


def _daemon_key_refused(base: str) -> bool:
    """Whether the server refuses the daemon's saved key (revoked under
    Settings › Connected clients, say). False with no key saved, or when the
    server cannot be reached: an outage is not a reason to mint another key."""
    from probe.sdk.config import load_context

    try:
        token = str((load_context() or {}).get("companion_token") or "")
    except Exception:  # noqa: BLE001 - an unreadable config holds no key
        return False
    if not token:
        return False
    try:
        return _verify(token, base)[0] == "rejected"
    except errors.RosError:  # a 429, a 404, a 5xx after retries: no answer, not a refusal
        return False


def _run_daemon_page(*, caps_by_source: dict) -> list[str] | None:
    """The daemon's page: what the Probe daemon sees (the agents' reasoning
    summaries). Enter on the main menu's Who records row while the daemon
    records, and straight after switching to it. The settings screen's
    machinery on `setup.DAEMON_GROUPS`: a change is written by `Set settings ›`,
    or by leaving the page with `←`/Escape after making it."""
    from probe.cli import setup as wizard
    from probe.cli import tui

    if not caps_by_source:
        return None
    tui.clear()
    current = wizard.read_settings(caps_by_source)
    picked = wizard.run_settings_menu(
        current,
        groups=wizard.DAEMON_GROUPS,
        frame=(
            "The Probe daemon:",
            [f"  {wizard.RECORDER_ROW_TITLE:<28} {wizard.machine_recorder()}"],
            "What should the daemon see?",
        ),
    )
    if picked is None or picked is tui.BACK:
        return None
    changes = {s: v for s, v in picked.items() if current.get(s) != v}
    return wizard.apply_settings(changes, caps_by_source=caps_by_source) if changes else None


def _authorize_companion(base_url: str, *, open_browser: bool = True) -> list[str]:
    """Mint the Probe daemon's own credential through one browser approval.

    Without it the daemon cannot write, and a session in the `daemon` state runs
    DEGRADED -- the agent records, exactly as under `on` -- so a declined or
    failed approval loses nothing; it says so and names the retry.

    The link and code are always printed: the flow blocks polling for an
    approval, and a browser that fails to open (headless, `--no-browser`) would
    otherwise leave the user waiting on a page they were never shown.
    """
    from probe.cli import setup as wizard

    def _prompt(prompt: DevicePrompt) -> None:
        print("Approve the Probe daemon's key in the browser:", flush=True)
        _show_device_prompt(prompt)

    minted, errors = wizard.authorize(
        [wizard.COMPANION_GRANT], base_url=base_url, open_browser=open_browser, on_prompt=_prompt
    )
    if errors or not wizard.companion_token_held():
        return [
            *errors,
            "! The daemon has no key yet, so your agent keeps recording.",
            "  Retry: probe wizard › Who records › daemon.",
        ]
    return ["The Probe daemon has its own key (read + write; deletes go to the trash only)."]


def _apply_capability_settings(
    changes: dict,
    *,
    caps_by_source: dict,
    base_now: str,
    telemetry=None,
) -> list[str]:
    """Apply capability toggles through the CONFIGURE machinery, PER AGENT.

    NEVER a bare `apply_*` call: the CONFIGURE path owns retries, the progress
    screen and the verified postcondition. Reusing it here means a Settings
    toggle and an Install apply are the same code asking for a different end
    state.

    Each agent gets its OWN target: that agent's current state — read with
    `capability_state_for`, the exact predicates the screen's boxes used —
    with only the toggled rows overridden. Committing one box never touches a
    capability that has no box, on ANY agent. The first ship of this screen
    built one union-derived target and applied it to every agent, which meant
    toggling auto-update on a mixed device re-enabled Session capture on the
    agent that had it off, and — because the preserve baseline used
    `enabled()` while the boxes read the plugin facts — uninstalled a
    signed-out machine's tracking plugin.

    No agent is ever asked for a browser approval: grants follow the CHANGES,
    and no row left on this screen needs one. An untouched capability may be
    REPAIRED with credentials already held, never re-granted — deriving the
    needs from the reconciled target is what once turned an unrelated toggle
    into a login prompt.

    A failing agent is CONTAINED: the CONFIGURE path reports failure by
    raising `typer.Exit`, and letting that escape here would kill the whole
    wizard mid-Settings and silently skip the remaining agent. Each agent's
    Exit is caught, reported in its own labelled lines, and the loop continues.
    """
    from probe.cli import actions as actions_mod
    from probe.cli import doctor as doctor_impl
    from probe.cli import setup as wizard
    from probe.cli.capabilities import Capability, agent_target

    wanted = {wizard.SETTING_CAPABILITY[setting]: value for setting, value in changes.items()}
    targets: dict[str, object] = {}
    for source, snapshot in caps_by_source.items():
        state = wizard.capability_state_for(snapshot)
        state.update(wanted)
        targets[source] = wizard.Selection(
            tracking=state[Capability.TRACKING],
            capture=state[Capability.CAPTURE],
            auto_update=state[Capability.AUTO_UPDATE],
            agent_rules=state[Capability.AGENT_RULES],
        )

    lines: list[str] = []
    for source in caps_by_source:
        label = wizard.agent_label(source)
        try:
            with agent_target(source):
                current = doctor_impl.collect()
                result = _run_wizard_action(
                    actions_mod.Action.CONFIGURE,
                    caps=current,
                    base_now=base_now,
                    yes=True,
                    tracking=None,
                    capture=None,
                    auto_update=None,
                    agent_rules=None,
                    uninstall=False,
                    configured=True,
                    selection_override=targets[source],
                    authorization_needs=[],
                    capture_sources=[],
                    telemetry=telemetry,
                )
        except typer.Exit:
            # The configure path already streamed WHAT failed on its progress
            # screen; what must not happen is the whole wizard dying with the
            # other agent unapplied.
            lines.extend(
                [f"{label}:", "! not finished — re-run `probe wizard` › Settings to retry.", ""]
            )
            continue
        if result:
            lines.extend([f"{label}:", *result, ""])
    return lines


def _run_account_action(
    chosen_action,
    *,
    caps,
    base_now: str,
    yes: bool,
    sources: tuple[str, ...],
    telemetry=None,
) -> list[str] | None:
    """Account maintenance flags and the legacy account details screen.

    `sources` is ONLY about capture. The credential half of an account is
    device-wide -- one config file -- so this runs once per wizard pass however
    many coding agents are selected; the capture half is per agent, and that is
    what the list is for.
    """
    from probe.cli import actions as actions_mod
    from probe.cli import setup as wizard
    from probe.cli import telemetry as telemetry_mod
    from probe.cli import tui

    tel = telemetry_mod.null_context() if telemetry is None else telemetry
    saved = wizard.saved_accounts()
    choice = {
        actions_mod.Action.SIGN_IN: wizard.AccountAction.SIGN_IN,
        actions_mod.Action.SIGN_OUT: wizard.AccountAction.SIGN_OUT,
    }.get(chosen_action)

    if choice is None:
        if yes or not wizard.interactive():
            # A screen nobody can answer must not answer for them. Minting a
            # credential or clearing one unasked is the single thing this action
            # may never do on its own, so the flagless headless path REPORTS and
            # names the two flags that decide.
            return [
                "This device's account:",
                *wizard.describe_account(caps, saved=saved),
                "",
                "`probe wizard --action login` signs in; "
                "`probe wizard --action logout` clears the credentials saved here.",
            ]
        tui.clear()
        picked = wizard.run_account_menu(caps, saved=saved)
        if picked is None or picked is tui.BACK or picked is wizard.AccountAction.BACK:
            return None  # backed out: nothing happened, nothing to pause on
        choice = picked

    if choice is wizard.AccountAction.SWITCH:
        tui.clear()
        target = wizard.run_switch_menu(saved)
        if target is None or target is tui.BACK:
            return None
        return wizard.switch_account(target, sources)

    if choice is wizard.AccountAction.REMOVE:
        tui.clear()
        target = wizard.run_switch_menu(saved, removing=True)
        if target is None or target is tui.BACK:
            return None
        tui.clear()
        if wizard.confirm_remove_account(target) is not True:
            return None
        return wizard.remove_account(target)

    if choice is wizard.AccountAction.SIGN_OUT:
        if not yes and wizard.interactive():
            # A confirmation page first (Richard 2026-09-29); anything but a
            # yes is back to the menu with nothing changed.
            tui.clear()
            if wizard.confirm_sign_out(caps.logged_in_as if caps else None) is not True:
                return None
        for line in wizard.sign_out(sources):
            tui.say(line)
        raise typer.Exit(0)

    # SIGN IN. This one streams: the approval URL is only useful WHILE the flow
    # blocks on it, and everything else here returns its lines to be paged after
    # the fact.
    live = tui.interactive()
    heading = "Approve this device in the browser to sign in."

    def _prompt(prompt) -> None:
        details = [
            f"  visit: {prompt.verification_uri_complete}",
            f"  code:  {prompt.user_code}",
        ]
        if live:
            tui.page([heading, "", *details])
        else:
            for line in details:
                tui.say(line)

    if live:
        tui.page([heading, ""])
    else:
        tui.say(heading)
        tui.say()
    try:
        result = wizard.sign_in(
            base_url=base_now,
            sources=sources,
            on_prompt=_prompt,
        )
    except OnboardingRequired as exc:
        _finish_website_onboarding(exc)
    tel.emit(
        telemetry_mod.EVENT_WIZARD_SIGNED_IN,
        outcome=(
            telemetry_mod.SignInOutcome.SUCCESS if result.ok else telemetry_mod.SignInOutcome.FAILED
        ),
        via_account_menu=True,
    )
    if not result.ok and chosen_action is actions_mod.Action.SIGN_IN:
        # `--action login` is a SCRIPTED call, and a caller that cannot see the
        # exit status cannot tell an approved device from a refused one -- it
        # would go on to install plugins against a credential nobody minted.
        # The menu path deliberately does not exit: it returns to the menu,
        # where trying again is one keystroke.
        for line in result.lines:
            tui.say(line)
        raise typer.Exit(1)
    return result.lines


@dataclass
class _InstallationCompletion:
    """Settle one installation only after every selected agent has finished.

    Capability registration also adopts credentials, so intermediate agents
    still report. Their snapshot stays unknown until the final apply succeeds;
    an earlier unverified result keeps the whole installation unsettled.
    """

    remaining: int
    settled: bool = True

    def register(self, caps, *, settings, complete: bool = True) -> list[str]:
        self.remaining -= 1
        self.settled = self.settled and complete
        return _register_local_capabilities(
            caps,
            settings=settings,
            complete=self.settled and self.remaining == 0,
        )


def _register_local_capabilities(caps, *, settings=None, complete: bool = True) -> list[str]:
    """Lazy wrapper so ordinary CLI startup never imports setup-only SDK work."""
    from probe.cli.client_installation import register

    return register(caps, settings=settings, complete=complete)


# `probe setup` must keep working: it is printed on the live connect page, in
# shipped plugin copy, and in every PR description written before the rename.
# Registering the SAME function under both names means the alias can never drift
# from the real command's options.
app.command(name="setup", hidden=True)(wizard)


# -- history import (0108) ---------------------------------------------------
from .import_wandb import import_app  # noqa: E402 -- registration, not use

app.add_typer(import_app, name="import")

# -- the Probe daemon's key and record ----------------------------------------
from .companion import companion_app  # noqa: E402 -- registration, not use

app.add_typer(companion_app, name="companion")

# -- the daemon itself (v2) and the questions it holds for the researcher -----
from .daemon_cli import approvals_cmd, ask_cmd, daemon_app, deny_cmd  # noqa: E402 -- registration, not use

app.add_typer(daemon_app, name="daemon")
app.command("approvals")(approvals_cmd)
app.command("deny")(deny_cmd)
app.command("ask")(ask_cmd)


# -- mcp read credential ----------------------------------------------------
mcp_app = typer.Typer(no_args_is_help=True, help="the read-only credential the MCP surface uses")
app.add_typer(mcp_app, name="mcp")

mcp_token_app = typer.Typer(no_args_is_help=True, help="manage the read-only MCP token")
mcp_app.add_typer(mcp_token_app, name="token")

_READ_ONLY_SCOPES = {"read"}


def _normalize_token(raw: str) -> str:
    """Undo how tokens actually arrive: pasted with `Bearer `, quotes, or a newline."""
    token = raw.strip()
    for _ in range(2):  # e.g. "Bearer probe_pat_x" needs both peels
        if len(token) >= 2 and token[0] == token[-1] and token[0] in "\"'":
            token = token[1:-1].strip()
        if token.lower().startswith("bearer "):
            token = token[7:].strip()
    return token


def _checked_token(raw: str) -> str:
    token = _normalize_token(raw)
    if not token:
        # These used to raise the standalone click's BadParameter to dodge the bug
        # main() now fixes at the root (see the ClickException note above): typer's own
        # BadParameter is caught correctly, so the workaround is gone.
        raise typer.BadParameter("token is empty")
    # No prefix check: the server takes both `ros_pat_` and `probe_pat_`, and the
    # prefix is only a discriminator — real auth is a sha256 lookup.
    if any(c.isspace() or ord(c) < 32 for c in token):
        raise typer.BadParameter("token contains whitespace or control characters")
    return token


def _fingerprint(token: str) -> str:
    """Enough to compare two tokens without printing either."""
    return f"…{token[-4:]} (sha256:{hashlib.sha256(token.encode()).hexdigest()[:8]})"


def _verify(token: str, base_url: str) -> tuple[str, dict | None]:
    """Ask the API who this token is. Returns (state, identity).

    state: ``ok`` | ``rejected`` (definitive 401/403) | ``unreachable`` (blip).
    """
    try:
        with _new_client(base_url=base_url, token=token, fail_open=False) as client:
            return "ok", client.me()
    except (errors.AuthError, errors.ScopeError):  # 401, 403 — both definitive
        return "rejected", None
    except (errors.TransportError, errors.ServerError):
        return "unreachable", None


@mcp_token_app.command("set")
def mcp_token_set(
    token: str = typer.Option(None, "--token", help="paste a read-only token (air-gap path)"),
    allow_write: bool = typer.Option(False, "--allow-write", help="persist even if it can write"),
    verify: bool = typer.Option(
        True, "--verify/--no-verify", help="check the token against /v1/me"
    ),
) -> None:
    """Store the read-only token the MCP uses. Re-run to rotate — it replaces, never appends.

    Bare `probe mcp token set` mints a read-only token in the browser, so nothing is
    pasted and no secret lands in your shell history or `ps` output.
    """
    base = resolve(base_url=_conn.base_url).base_url
    if token is not None:
        # `--token ""` is a mistake to report, not a cue to open a browser.
        secret = _checked_token(token)
    else:
        print(f"opening {base} to mint a read-only token…")
        try:
            # Ask for the `mcp` capability by name. Omitting `grants` takes the
            # server default of `["api"]`, which minted this read-only credential
            # tagged as an API credential under an installation of its own -- so
            # one laptop showed up as two machines, and `installation_role` said
            # nothing true about what the credential could do.
            #
            # `token_name` is the ORDINARY CLI shape on purpose: the server
            # appends " (MCP)" to the credential and names the installation after
            # the bare value, so this yields the same canonical device name every
            # other pairing produces instead of a third spelling of one machine.
            minted = device_authorize(
                base,
                scopes=["read"],
                grants=["mcp"],
                token_name=f"Probe Research CLI · {hostname()}",
                on_prompt=_show_device_prompt,
            )
        except DeviceLoginError as exc:
            print(f"device login failed: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
        # Not device_login(): that returns the response's top-level `token`,
        # which only exists when an `api` grant was requested. With `mcp` alone
        # the credential rides in `grants`.
        credential = credentials_by_grant(minted).get("mcp") or {}
        secret = credential.get("token")
        if not secret:
            print(
                "error: the server did not return an MCP credential. It may predate "
                "the `mcp` grant; upgrade the backend or pass --token.",
                file=sys.stderr,
            )
            raise typer.Exit(1)

    state, identity = _verify(secret, base) if verify else ("skipped", None)
    if state == "rejected":
        # Persisting a token the API already refuses just moves the failure somewhere
        # quieter — the MCP would load its tools and fail every call.
        print("error: the API rejected this token; nothing was saved", file=sys.stderr)
        raise typer.Exit(1)

    scopes = set((identity or {}).get("scopes") or [])
    if scopes and not scopes <= _READ_ONLY_SCOPES and not allow_write:
        print(
            f"error: this token carries {sorted(scopes)}; the MCP credential should be read-only.\n"
            "       Mint a read-only one with `probe mcp token set` (no --token), "
            "or pass --allow-write to override.",
            file=sys.stderr,
        )
        raise typer.Exit(1)

    updates = {"mcp_token": secret}
    if not load_context().get("base_url"):
        updates["base_url"] = base
    path = save_context(updates)

    # Codex holds its own copy of this token in ~/.codex/config.toml. Leaving
    # the old one there is a silent 401 on every Codex call, with a health check
    # that still says authenticated.
    from probe.cli import setup as _wizard

    for line in _wizard.sync_codex_mcp_token():
        print(line)

    who = (identity or {}).get("email") or "unverified"
    # Never report success without saying whether it was actually checked — an
    # unverified write that reads like a verified one is how this broke before.
    note = {
        "ok": f"verified: yes ({who}, scopes={sorted(scopes) or 'unknown'})",
        "unreachable": "verified: no (API unreachable — run `probe mcp status` to recheck)",
        "skipped": "verified: no (--no-verify)",
    }[state]
    print(f"saved mcp_token {_fingerprint(secret)} to {path}\n{note}")
    if scopes and not scopes <= _READ_ONLY_SCOPES:
        print("warning: this token can write; the MCP surface is read-only by design")
    elif state != "ok":
        # The read-only guard runs on the verified path only. Say so, rather than let
        # an unchecked token look like a checked one that passed.
        print("warning: scopes unchecked — this token may be able to write")
    print("Restart any MCP client that is already running, or reconnect it, to pick this up.")


@mcp_token_app.command("unset")
def mcp_token_unset() -> None:
    """Remove the stored read-only MCP token."""
    if not load_context().get("mcp_token"):
        print("no mcp_token stored")
        return
    print(f"removed mcp_token from {save_context({'mcp_token': None})}")


@mcp_app.command("headers")
def mcp_headers() -> None:
    """Emit the MCP Authorization header as JSON (for a client's headers helper)."""
    settings = resolve(base_url=_conn.base_url)
    if not settings.mcp_token:
        print(
            f"no MCP token: set PROBE_MCP_TOKEN, or the wizard's Install mints one ({session_marker.WIZARD_HINT})",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    print(json.dumps({"Authorization": f"Bearer {settings.mcp_token}"}))


@mcp_app.command("env")
def mcp_env() -> None:
    """Print the export line, for MCP clients that only read the environment.

    Prints a secret to stdout. Nothing is written to a shell profile: a tool that
    edits rc files it did not author breaks `export X=$(op read …)` and compound
    statements. Add the line yourself, or use a client that supports a headers helper.
    """
    settings = resolve(base_url=_conn.base_url)
    if not settings.mcp_token:
        print(f"no MCP token: the wizard's Install mints one ({session_marker.WIZARD_HINT})", file=sys.stderr)
        raise typer.Exit(1)
    print(f"export PROBE_MCP_TOKEN={shlex.quote(settings.mcp_token)}")


def _stale_literal_copies(token: str | None) -> list[str]:
    """Places that pin a *different* literal token and would outlive a rotation."""
    path = Path.home() / ".claude.json"
    try:
        servers = json.loads(path.read_text()).get("mcpServers") or {}
    except (OSError, json.JSONDecodeError, AttributeError):
        return []
    stale = []
    for name, cfg in servers.items():
        if not isinstance(cfg, dict):
            continue
        pinned = [
            (cfg.get("env") or {}).get("PROBE_MCP_TOKEN"),
            (cfg.get("headers") or {}).get("Authorization"),
        ]
        for value in pinned:
            if isinstance(value, str) and "pat_" in value and (not token or token not in value):
                stale.append(f"~/.claude.json -> mcpServers.{name}")
                break
    return stale


@mcp_app.command("status")
def mcp_status() -> None:
    """Diagnose the MCP credential: where it comes from, whether it still works."""
    settings = resolve(base_url=_conn.base_url)
    file_token = load_context().get("mcp_token")
    env_token = os.environ.get("PROBE_MCP_TOKEN")
    token = settings.mcp_token

    print(f"config:   {config_path()}")
    print(f"endpoint: {settings.base_url}")
    if not token:
        print(f"token:    none — the wizard's Install mints one ({session_marker.WIZARD_HINT})")
        raise typer.Exit(1)

    source = "environment (PROBE_MCP_TOKEN)" if env_token else "config file"
    print(f"token:    {_fingerprint(token)} from {source}")
    if env_token and file_token and env_token != file_token:
        # The env wins, so a freshly-rotated config token is not what the MCP sends.
        print("          ! the environment and config hold DIFFERENT tokens; the environment wins")
        print(
            f"          config holds {_fingerprint(file_token)} — open a new shell, or unset PROBE_MCP_TOKEN"
        )

    state, identity = _verify(token, settings.base_url)
    if state == "ok":
        scopes = sorted((identity or {}).get("scopes") or [])
        print(f"verify:   ok — {identity.get('email')} scopes={scopes}")
        if set(scopes) - _READ_ONLY_SCOPES:
            print("          ! this token can write; the MCP surface is read-only by design")
    elif state == "rejected":
        print("verify:   REJECTED — the API refuses this token. `probe wizard --action login` "
              "signs in again and replaces it")
    else:
        print("verify:   unknown — the API was unreachable")

    for place in _stale_literal_copies(token):
        print(f"stale:    ! {place} pins a different token and takes precedence over this one")

    if state == "rejected":
        raise typer.Exit(1)


# -- context ----------------------------------------------------------------
context_app = typer.Typer(
    no_args_is_help=True, help="named local contexts: endpoint + credentials + anchors"
)
app.add_typer(context_app, name="context")


def _redact(value: str | None) -> str:
    """Enough of a token to recognize, never enough to use.

    Shows the TAIL, not the head: the head is a shared prefix (`probe_pat_`,
    `ros_pat_`) that identifies nothing, so leading characters spend secret entropy
    to say what every token already says. `context list` output ends up in bug
    reports and CI logs, so this matches `_fingerprint`'s last-4 convention rather
    than inventing a second, weaker redaction rule.
    """
    if not value:
        return "-"
    return f"…{value[-4:]}" if len(value) > 8 else "set"


def _context_row(name: str, ctx: dict, *, active: bool) -> dict:
    anchor = ctx.get("workspace") if isinstance(ctx.get("workspace"), dict) else {}
    return {
        "name": name,
        "active": active,
        "base_url": ctx.get("base_url") or DEFAULT_BASE_URL,
        "token": _redact(ctx.get("token")),
        "mcp_token": _redact(ctx.get("mcp_token")),
        "workspace": anchor.get("id"),
        "project": anchor.get("project"),
    }


@context_app.command("list")
def context_list() -> None:
    """List local contexts. Credentials are shown redacted."""
    data = load_file()
    contexts = data.get("contexts") or {}
    if not contexts:
        print(f"no contexts yet — sign in ({session_marker.WIZARD_HINT})")
        return
    active = current_context_name(data)
    _print_json([_context_row(n, c or {}, active=n == active) for n, c in sorted(contexts.items())])


@context_app.command("show")
def context_show(
    name: str = typer.Argument(None, help="defaults to the active context"),
) -> None:
    """Show one context as it will actually resolve, env overrides included."""
    target = name or current_context_name()
    ctx = load_context(target)
    if not ctx and target not in (load_file().get("contexts") or {}):
        print(f"no such context: {target}", file=sys.stderr)
        raise typer.Exit(1)
    row = _context_row(target, ctx, active=target == current_context_name())
    # Show the resolved view too: an env var silently outranking the file is exactly
    # the confusion this command exists to end.
    settings = resolve(context=target)
    row["resolved"] = {
        "base_url": settings.base_url,
        "workspace": settings.workspace,
        "project": settings.project,
    }
    _print_json(row)


@context_app.command("use")
def context_use(name: str = typer.Argument(..., help="context to make active")) -> None:
    """Switch the active context, creating it empty if it is new."""
    path = use_context(name)
    print(f"active context: {name} ({path})")


@context_app.command("delete")
def context_delete(name: str = typer.Argument(..., help="context to remove")) -> None:
    """Delete a context and its stored credentials."""
    if name not in (load_file().get("contexts") or {}):
        print(f"no such context: {name}", file=sys.stderr)
        raise typer.Exit(1)
    delete_context(name)
    print(f"deleted context {name} (active: {current_context_name()})")


# -- workspaces -------------------------------------------------------------
workspace_app = typer.Typer(
    no_args_is_help=True, help="workspaces — folders for projects and files"
)
app.add_typer(workspace_app, name="workspace")


def _workspace_row(ws: dict) -> dict:
    """Show the same filing-location fields for every workspace."""
    return {
        "id": ws.get("id"),
        "name": ws.get("name"),
        "slug": ws.get("slug"),
        "projects": ws.get("project_count", 0),
    }


@workspace_app.command("list")
def workspace_list(
    raw: bool = typer.Option(False, "--raw", help="full API objects instead of the summary"),
) -> None:
    """List every workspace alphabetically in server order."""
    with _client() as c:
        rows = c.list_workspaces()
        if raw:
            _print_json(rows)
            return
    if not rows:
        print("no workspaces yet — a Default workspace is created on your first write")
        return
    _print_json([_workspace_row(w) for w in rows])


@workspace_app.command("get")
def workspace_get(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
) -> None:
    """Show one workspace."""
    with _client() as c:
        _print_json(c.get_workspace(_ref(c, "workspace", workspace_id).id))


@workspace_app.command("rename")
def workspace_rename(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    name: str = typer.Option(..., "--name", help="new display name"),
) -> None:
    """Rename a workspace. Name is the only editable field.

    The slug stays unchanged. Any team member may rename any workspace.
    """
    with _client() as c:
        _print_json(c.rename_workspace(_ref(c, "workspace", workspace_id).id, name))


@workspace_app.command("create")
def workspace_create(
    slug: str = typer.Argument(..., help="handle for the new workspace, e.g. engineering"),
    name: str | None = typer.Option(None, "--name", help="display label (default: the slug)"),
    use: bool = typer.Option(False, "--use", help="also make it this context's active workspace"),
) -> None:
    """Create a workspace — "engineering", "wandb-imports".

    Anyone on the team can rename it, file into it, and delete it while it is empty.
    Use `--use` to select it for this context, or `--workspace` on a project create.
    With no workspace selected, the server uses the oldest existing workspace.
    """
    with _client() as c:
        ws = c.create_workspace(slug, name)
    if use:
        save_context({"workspace": {"id": str(ws["id"]), "project": None}})
    _print_json(ws)
    if use:
        print(f"active workspace: {ws.get('name')} ({ws['id']}) — project cleared")


@workspace_app.command("delete")
def workspace_delete(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    yes: bool = typer.Option(False, "--yes", "-y", help="skip the confirmation prompt"),
) -> None:
    """Delete an empty workspace.

    The server refuses while it holds projects or files, or an integration targets
    it. Move work out first (`probe project move <project> --workspace <other>`).
    If no workspaces remain, the next write without a workspace creates a Default
    workspace. Deleting the selected workspace clears this context's local pin.
    """
    with _client() as c:
        ws = c.get_workspace(_ref(c, "workspace", workspace_id).id)
        if not yes:
            typer.confirm(f"delete workspace {ws.get('name')} ({ws.get('slug')})?", abort=True)
        c.delete_workspace(str(ws["id"]))
    # Read the saved pin directly: an environment override is still an explicit
    # destination, and must not make deleting another workspace clear this one.
    anchor = load_context().get("workspace")
    pinned_id = anchor.get("id") if isinstance(anchor, dict) else None
    if isinstance(pinned_id, str) and _bare_id(pinned_id) == str(ws["id"]):
        save_context({"workspace": None})
    print(f"deleted workspace {ws.get('name')} ({ws['id']})")


@workspace_app.command("use")
def workspace_use(
    workspace_id: str | None = typer.Argument(
        None, help="workspace slug to make active (or id:<uuid>)"
    ),
    clear: bool = typer.Option(
        False, "--clear", help="forget the active workspace and use the server default"
    ),
) -> None:
    """Set the active workspace for this context, or `--clear` to use the server default.

    Clears the active project either way: a project belongs to exactly one workspace,
    so keeping the old one selected would leave the context pointing at a project that
    is not in the workspace you just switched to.

    `--clear` removes the pin. Writes then carry no workspace, so the server uses
    the oldest existing workspace, creating a Default workspace only if none remain.
    """
    if clear == (workspace_id is not None):
        raise typer.BadParameter("pass a workspace to switch to, or --clear, not both")
    if clear:
        save_context({"workspace": None})
        print("active workspace cleared — writes use the server default workspace")
        return
    with _client() as c:
        ws = c.get_workspace(_ref(c, "workspace", workspace_id).id)
    save_context({"workspace": {"id": str(ws["id"]), "project": None}})
    print(f"active workspace: {ws.get('name')} ({ws['id']}) — project cleared")


# -- projects ---------------------------------------------------------------
project_app = typer.Typer(no_args_is_help=True, help="projects — the top of the data model")
app.add_typer(project_app, name="project")


# ---------------------------------------------------------------------------
# Who may EDIT a workspace (0214)
#
# THE INTERIM ADMIN SURFACE. The dashboard half ships in a later change, so
# until then these commands are the only way to restrict who may edit a
# workspace. Every mutation is owner/admin-only server-side.
#
# NOTHING HERE AFFECTS READS. A restricted workspace stays fully visible to
# every team member; only writes narrow. Say "restricted", never "private".
# ---------------------------------------------------------------------------
group_app = typer.Typer(
    no_args_is_help=True,
    help="access groups — named sets of people a workspace can grant edit access to",
)
app.add_typer(group_app, name="access-group")

writers_app = typer.Typer(
    no_args_is_help=True, help="who may edit a workspace (reads are never restricted)"
)
workspace_app.add_typer(writers_app, name="writers")


@group_app.command("list")
def access_group_list() -> None:
    """Every named group in the team, with its member user ids."""
    with _client() as c:
        _print_json(c.list_access_groups())


@group_app.command("create")
def access_group_create(
    name: str = typer.Argument(..., help='display name, e.g. "Lab"'),
) -> None:
    """Create a group. Owner/admin only."""
    with _client() as c:
        _print_json(c.create_access_group(name))


@group_app.command("rename")
def access_group_rename(
    group_id: str = typer.Argument(..., help="group id"),
    name: str = typer.Option(..., "--name", help="new display name"),
) -> None:
    """Rename a group. The id is what writer lists reference, so this moves nothing."""
    with _client() as c:
        _print_json(c.rename_access_group(group_id, name))


@group_app.command("delete")
def access_group_delete(
    group_id: str = typer.Argument(..., help="group id"),
) -> None:
    """Delete a group, dropping it from every writer list it guards.

    This can only NARROW access: a restricted workspace left with no writers is
    writable by nobody, never by everybody.
    """
    with _client() as c:
        c.delete_access_group(group_id)
    print("deleted")


@group_app.command("add")
def access_group_add(
    group_id: str = typer.Argument(..., help="group id"),
    user_id: str = typer.Argument(..., help="team member's user id"),
) -> None:
    """Add a member. Idempotent; a user may belong to several groups."""
    with _client() as c:
        c.add_access_group_member(group_id, user_id)
    print("added")


@group_app.command("remove")
def access_group_remove(
    group_id: str = typer.Argument(..., help="group id"),
    user_id: str = typer.Argument(..., help="team member's user id"),
) -> None:
    """Remove a member. Idempotent."""
    with _client() as c:
        c.remove_access_group_member(group_id, user_id)
    print("removed")


@writers_app.command("show")
def workspace_writers_show(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
) -> None:
    """Who may edit this workspace. Readable by every member."""
    with _client() as c:
        _print_json(c.get_workspace_writers(_ref(c, "workspace", workspace_id).id))


@writers_app.command("set")
def workspace_writers_set(
    workspace_id: str = typer.Argument(..., help="workspace slug (or id:<uuid>)"),
    user: list[str] = typer.Option([], "--user", help="user id who may edit (repeatable)"),
    group: list[str] = typer.Option([], "--group", help="group id whose members may edit"),
    open_to_everyone: bool = typer.Option(
        False, "--open", help="remove the restriction: every team member may edit again"
    ),
) -> None:
    """Replace the WHOLE write state in one call. Owner/admin only.

    Whole-state rather than add/remove: "restrict this to the lab" as several
    requests can interleave with another admin's and commit a state neither
    asked for.

    `--open` restores the default. Restricting with NO subjects is legal and
    means NOBODY may edit -- which is the point of the explicit mode: removing
    the last writer must narrow access, never widen it.
    """
    mode = "open" if open_to_everyone else "restricted"
    with _client() as c:
        _print_json(
            c.set_workspace_writers(
                _ref(c, "workspace", workspace_id).id,
                mode=mode,
                users=list(user),
                groups=list(group),
            )
        )


def _resolve_workspace(client: Client | None, explicit: str | None) -> str | None:
    """Explicit flag -> PROBE_WORKSPACE -> context, resolved to an id.

    Same provenance rule as :func:`_ambient_project`: an EXPLICIT ref is typed by
    a person, so a bare one is a slug; the ambient value was written by
    ``workspace use`` and is an id. Getting that backwards is how an explicit
    ``--workspace <something>`` would silently address a different workspace.

    ``client`` may be None where the caller has none open and only needs the
    ambient value passed through untouched.
    """
    merged = resolve(workspace=explicit).workspace
    if explicit is None:
        # Machine-written: `workspace use` stores the id. Strip an `id:` prefix if
        # one is there -- the API takes the uuid itself.
        return _bare_id(merged)
    if client is None:  # pragma: no cover - every caller with an explicit ref has one
        return explicit
    return _ref(client, "workspace", explicit).id


def _bare_id(ref: str | None) -> str | None:
    """Strip an `id:` prefix for the API, which takes the uuid itself."""
    if ref is None:
        return None
    bare, _ = refs.split_selector(ref)
    return bare


def _ref(client: Client, kind: str, ref: str) -> refs.Ref:
    """Resolve a ref, reporting both failure modes as CLI errors.

    The one adapter between :mod:`probe.cli.refs` (which raises library errors so
    the SDK and tests can use it) and Typer's exit codes. Ambiguity and absence
    both surface as ``BadParameter``: each means "this ref does not identify one
    thing", and neither is something a retry of the same command fixes.
    """
    if kind not in refs.SLUG_KINDS and kind not in ("run", "workspace"):
        # Kinds with no second spelling (artifacts: no item GET, no by-name
        # index, and a name that is anchor-scoped rather than unique). The id is
        # passed through -- but the verb still routes through here so it gets the
        # same prompt and the same "deleted" line as everything else.
        return refs.Ref(ref, f"{kind} {ref}")
    try:
        if kind == "run":
            return refs.resolve_run(client, ref)
        if kind == "workspace":
            return refs.resolve_workspace(client, ref)
        return refs.resolve(client, kind, ref, project_hint=_active_project_id(kind, ref))
    except (
        UnfilteredListing,
        refs.AmbiguousName,
        refs.NameFilterUnsupported,
        NotFoundError,
    ) as exc:
        raise typer.BadParameter(str(exc)) from None


def _filed_under(target: refs.Ref) -> str | None:
    """The project a resolved experiment ref is filed under, when its row says
    (so the experiment API's routes need no second lookup)."""
    row = target.row if isinstance(target.row, dict) else {}
    project = row.get("project_id")
    return str(project) if project and refs.is_uuid(str(project)) else None


def _active_project_id(kind: str, ref: str) -> str | None:
    """The active project's id, when it costs nothing to know, for an
    experiment SLUG: looking there first answers in one request (refs.resolve
    falls back tenant-wide on a miss). None for anything else, and when the
    active project is stored as a slug (resolving it would be a request of
    its own)."""
    if kind != "experiment" or refs.split_selector(ref)[1] != "slug":
        return None
    try:
        ambient = _ambient_project(None)
    except Exception:  # noqa: BLE001 - a hint only; the lookup works without it
        return None
    if not ambient:
        return None
    bare, how = refs.split_selector(ambient)
    return bare if how == "id" and refs.is_uuid(bare) else None


def _ambient_project(explicit: str | None, **kw) -> str | None:
    """The project ref to use, canonicalising ONLY the ambient one.

    ``from_ambient`` reads a bare UUID as an id, which is right for a value the
    TOOL stored and catastrophically wrong for one a person typed: rewriting an
    explicit ``--project <uuid-shaped-slug>`` to ``id:`` is the original bug, back.
    ``resolve()`` merges flag/env/context into one string and forgets which won,
    so the provenance has to be decided here, before it is lost.
    """
    merged = resolve(project=explicit, **kw).project
    if explicit is not None:
        return explicit  # typed by a person: a bare ref is a slug, full stop.
    return refs.from_ambient(merged)


def _project_id(client: Client, ref: str) -> str:
    """A project SLUG (or ``id:<uuid>``) -> the id every route wants.

    Every ``/v1/projects/{project_id}`` route types the path param as a UUID, so a
    slug reaches the server as a 422 about UUID parsing rather than a lookup, and
    the translation has to happen client-side. Slugs are the handle people
    actually remember, so they are what a bare ref means -- see
    :mod:`probe.cli.refs` for why that is a rule and not a preference.
    """
    return _ref(client, "project", ref).id


def _project_slug(client: Client, ref: str | None) -> str | None:
    """The inverse of :func:`_project_id`, for the slug-resolving paths.

    ``Client.run`` resolves a project by *slug* and raises when it is absent, so
    handing it an id makes the lookup miss a project that genuinely exists. The
    ambient anchor stores an id (stable across renames), so it has to be
    translated on the way in -- as does an explicit ``--project id:<uuid>``.

    A bare ref is returned untouched: it is already a slug by definition now, and
    absence is ``run start``'s to report, whose near-miss guard names the slugs a
    typo was close to. Resolving it here would replace that with a bare
    "not found".
    """
    if ref is None:
        return None
    bare, how = refs.split_selector(ref)
    if how == "slug":
        return bare
    return _ref(client, "project", ref).row.get("slug", bare)


#: How long a run, group, experiment or project stays restorable in the
#: server's trash (`app/teams/deletion_policy.py::TRASH_DAYS`; kept equal by
#: tests/unit/test_trash_days_parity.py). The prompt promises it before the
#: delete; the server's answer then names the exact date.
TRASH_DAYS = 21


def _confirm_delete(
    yes: bool, subject: str, *, cascade: str | None = None, trash: bool = False
) -> None:
    """The one confirmation path for every irreversible delete verb.

    This was spelled by hand in four places and forgotten entirely in a fifth:
    ``artifact delete`` took no ``--yes`` and prompted for nothing, so the flag
    that guards the *cascading* deletes was rejected by the one that deletes
    silently. Passing ``--yes`` there — the habit every other delete teaches —
    failed the whole batch, which is the good outcome; had it been accepted and
    ignored, the artifacts would have been gone before anyone read them.

    A verb that forgets to prompt is indistinguishable from one that decided not
    to, so the decision belongs here rather than being re-made per verb.

    ``cascade`` names what else goes; omit it when nothing else does.

    ``subject`` is the RESOLVED entity (name, handle and id), never the string the
    operator typed. Echoing the ref back asks them to approve their own typo, and
    in the id/slug collision that string is exactly the one that does not say
    which entity is about to go.
    """
    if yes:
        return
    if trash:
        # 0261: a run, experiment or project delete MOVES it to the trash.
        question = f"move {subject} to the trash?"
        if cascade:
            question += f" {cascade}."
        question += (
            f" Probe support can restore it for {TRASH_DAYS} days; "
            "after that it is deleted for good"
        )
        typer.confirm(question, abort=True)
        return
    question = f"permanently delete {subject}?"
    if cascade:
        question += f" {cascade}, and this cannot be undone"
    typer.confirm(question, abort=True)


def _confirmed_delete(
    kind: str,
    ref: str,
    *,
    yes: bool,
    cascade: str | None = None,
    delete_kwargs: dict[str, Any] | None = None,
    trash: bool = False,
) -> None:
    """The whole shape of a delete: resolve, show, confirm, delete by id.

    Every delete verb goes through here so they cannot drift apart on the three
    things that decide whether the right thing dies: which ref forms are accepted,
    what the prompt names, and whether the id or the typed string reaches the
    endpoint. ``run delete`` accepting a petname while ``project delete`` accepted
    a slug and ``experiment delete`` accepted neither is how an operator learns a
    habit from one verb that silently misfires in the next.

    Resolution happens BEFORE the prompt, which is the ordering the confirmation
    is worth anything under.
    """
    with _client() as c:
        target = _ref(c, kind, ref)
        # Promise the trash only where the server has one: before 0261 the
        # same DELETE is permanent, and the prompt must say so.
        trash = trash and c.supports_feature("trash")
        _confirm_delete(yes, target.label, cascade=cascade, trash=trash)
        kwargs = dict(delete_kwargs or {})
        if kind == "experiment" and _filed_under(target):
            kwargs.setdefault("project_id", _filed_under(target))  # saves a lookup
        answer = getattr(c, f"delete_{kind}")(target.id, **kwargs)
    until = answer.get("restorable_until") if trash and isinstance(answer, dict) else None
    if until:
        print(
            f"{target.label} moved to the trash; Probe support can restore it "
            f"until {str(until)[:10]}"
        )
        return
    print(f"{target.label} deleted")


# --- One vocabulary for the things every noun has ----------------------------
#
# These were written per-command, so the same concept had several spellings and
# some of them were wrong: `run set` and `run tag` said "run id" after #173 made
# a bare ref the PETNAME, and only one of the six `--description` flags carried
# any help at all. A constant is not ceremony here -- it is the only way the
# wording stays identical across four nouns and twenty-odd verbs, which is what
# lets someone learn a habit from one verb and use it on the next.
#
# The ref phrasing per kind follows refs.py's "which handle is the name" table,
# and must keep following it: project/experiment are slug-first, runs are
# petname-first-but-either (a petname cannot be UUID-shaped, so it cannot
# collide), artifacts are id-only.
# Factories, not shared instances: a typer.Argument/Option value is bound as a
# function default, and one object reused across signatures is shared mutable
# state that click is free to annotate. A call per signature costs nothing.
DESCRIPTION_HELP = "what this is, in a few words up to 3 sentences"

#: Notes are the CAVEAT, not a second description -- what a later reader should
#: distrust. Prose, so it reads a file or stdin as readily as an argument.
NOTES_HELP = "caveat a later reader needs; literal, @file, or '-' for stdin ('' clears)"

#: Runs read either way on purpose -- see refs.resolve_run.
RUN_REF_HELP = "run slug or id (they cannot collide)"


def slug_ref(kind: str) -> Any:
    """The positional ref for a slug-addressed kind (project, experiment)."""
    return typer.Argument(..., help=f"{kind} slug (or id:<uuid>)")


def run_ref() -> Any:
    return typer.Argument(..., help=RUN_REF_HELP)


def description_opt() -> Any:
    return typer.Option(None, "--description", help=DESCRIPTION_HELP)


def notes_opt() -> Any:
    return typer.Option(None, "--notes", help=NOTES_HELP)


#: Tag changes on a `set` verb: the `tag` verb's add / --remove / --set, spelled
#: so they cannot be mistaken for the other fields `set` takes. They ride in the
#: SAME PATCH as those fields, so an edit that renames and retags is one write
#: that cannot land half.
def add_tag_opt() -> Any:
    return typer.Option(None, "--add-tag", help="add a tag (repeatable)")


def remove_tag_opt() -> Any:
    return typer.Option(None, "--remove-tag", help="remove a tag (repeatable)")


def set_tags_opt() -> Any:
    return typer.Option(
        None, "--set-tags", help="replace the whole tag list (repeatable; --set-tags '' clears)"
    )


#: WHO composed the name and description on this write. One definition, because
#: eight verbs offer it and a help string that drifts between them is a
#: different promise on each.
#:
#: The DEFAULT is resolved in the SDK, not here (`sdk/client.py::_authored_by`),
#: so `probe` and a Python caller answer the question the same way: under a
#: coding agent it is `agent`, and in a bare terminal NOTHING is sent and the
#: server applies the inference it always has.
AUTHORED_BY_HELP = (
    "who composed --name/--description: 'human' LOCKS them against generation "
    "forever (no undo), 'agent' leaves them improvable. Default: agent under a "
    "coding agent, otherwise the server's own inference"
)


class AuthoredBy(str, Enum):
    """Who composed the text on this write.

    Mirrors `app.core.authorship.Authorship` and the generated
    `probe._generated.models.Authorship`; spelled here because this is a typer
    choice surface and the two spellings are pinned together by
    `agent/tests/test_authorship_default.py`.
    """

    human = "human"
    agent = "agent"


def _authored_by_value(choice: "AuthoredBy | None") -> str | None:
    """The wire value for `--authored-by`, or None to let the SDK decide.

    None here does NOT mean "human". It means the caller did not say, and the
    resolution then happens once, in `sdk/client.py::_authored_by` -- so the
    CLI and a Python caller can never answer the question differently.
    """
    return choice.value if choice is not None else None


def authored_by_opt() -> Any:
    return typer.Option(None, "--authored-by", help=AUTHORED_BY_HELP)


def entity_markdown_opt() -> Any:
    return typer.Option(
        None,
        "--summary",
        help=(
            "whole-document Markdown: on a project or experiment a block INSIDE the "
            "Overview page the AI may not rewrite, on a run below the AI Summary; "
            "read first, and check the result CONTAINS what you meant rather than "
            "matching byte-for-byte -- a read answers from the page, which renders "
            "it. Literal, @file, or - for stdin. "
            "A line containing only [README](https://github.com/owner/repo) "
            "embeds that repo's README at that point"
        ),
    )


class ProjectKind(str, Enum):
    """The closed kind vocabulary; the server refuses anything else.

    weights MOVE -> training · frozen weights (sweeps, evals) -> evaluation ·
    papers, design, theory -> research · everything else -> general.
    A SWEEP is an experiment: `experiment` is a STRUCTURAL kind for a leaf
    under one of the four, carrying the question it answers in --description.
    """

    training = "training"
    evaluation = "evaluation"
    research = "research"
    general = "general"
    experiment = "experiment"


#: Old spellings `--kind` still ACCEPTS but no longer offers (Track E, 2026-10-04:
#: `inference` became `evaluation`). Installed skills and agents' habits still
#: type the old word, and refusing it would fail a create the server itself
#: accepts (it bridges `inference` forever, logged `project_kind_bridged`). The
#: CLI translates here, so a current CLI never sends the old spelling and the
#: server's bridge count measures only old CLIs and SDK code passing the string
#: itself -- the callers a future refusal would actually break.
#:
#: Through click's `token_normalize_func` (the `context_settings` below), which
#: the Choice applies to the typed value before matching: the alias resolves to
#: its canonical member while help, the choice list in a usage error and
#: the assistant's synopsis (app/assistant/cli_tool.py reads
#: `param.type.choices`) all keep naming the canonical five only.
LEGACY_PROJECT_KIND_ALIASES = {"inference": ProjectKind.evaluation.value}

_PROJECT_KIND_CONTEXT = {
    "token_normalize_func": lambda token: LEGACY_PROJECT_KIND_ALIASES.get(token, token)
}


@project_app.command("create", context_settings=_PROJECT_KIND_CONTEXT)
def project_create(
    slug: str = typer.Argument(..., help="url-safe identifier, unique per tenant"),
    kind: ProjectKind = typer.Option(
        ...,
        "--kind",
        help=(
            "what the project is FOR; structures its page. weights move ->"
            " training; sweeps/evals -> evaluation; papers/design -> research;"
            " else general"
        ),
    ),
    name: str = typer.Option(
        None, "--name", help="display name; omit it and the row reads as its slug"
    ),
    parent: str = typer.Option(
        None, "--parent", help="file under this project (slug or id:<uuid>)"
    ),
    description: str = description_opt(),
    summary: str = entity_markdown_opt(),
    tag: list[str] = typer.Option(None, "--tag", help="tag at creation (repeatable)"),
    workspace: str = typer.Option(
        None, "--workspace", help="workspace slug (or id:<uuid>); defaults to the active one"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Create a project.

    This is what the CLI was missing: creating a project used to require starting a run,
    which forced an experiment and an invented question into existence alongside it.

    --kind is REQUIRED (0149): the creator declares intent, before content
    exists. --parent files the newborn under an existing project (0148); it
    then lives in the parent's workspace. An explicit --workspace beside
    --parent is SENT, not dropped, so the server refuses a mismatch (422)
    exactly as documented; omitted, the parent's workspace is inherited.
    """
    with _client() as c:
        parent_id = _project_id(c, parent) if parent else None
        created = c.create_project(
            slug,
            name,
            kind=kind.value,
            parent_project_id=parent_id,
            # Only resolve the ambient default when NOT filing under a parent:
            # a parented create with no explicit workspace inherits server-side.
            workspace_id=(_resolve_workspace(c, workspace) if workspace or not parent else None),
            description=description,
            document=_text_value(summary),
            tags=tag or None,
            authored_by=_authored_by_value(authored_by),
        )
    _print_json(created)
    _print_link("project", created.get("id"))


@project_app.command("list")
def project_list(
    workspace: str = typer.Option(
        None, "--workspace", help="workspace slug (or id:<uuid>); defaults to the active one"
    ),
    all_workspaces: bool = typer.Option(
        False, "--all", help="every workspace you can see (ignores --workspace and context)"
    ),
    tag: list[str] = typer.Option(
        None, "--tag", help="filter: project must carry ALL (repeatable)"
    ),
    parent: str = typer.Option(
        None, "--parent", help="only the DIRECT subprojects of this project (slug or id:<uuid>)"
    ),
    limit: int = typer.Option(50, "--limit", min=1, max=200),
    cursor: str = typer.Option(None, "--cursor", help="keyset cursor from a previous page"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """List projects in a workspace, or across all of them with --all.

    `--parent` answers "what is under this project?" -- one level, the same
    direct children the dashboard's Subprojects tab shows. Walk it again on a
    child for the next level; the server caps depth at MAX_PROJECT_DEPTH.
    """
    params: dict[str, Any] = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    # Omitting workspace_id IS "all workspaces" — the server has no all-sentinel, so
    # --all means "send no filter" rather than some magic value.
    with _client() as c:
        # A subproject can only be asked for by its parent, and a tree is one
        # workspace (0148) — so --parent carries the workspace with it and a
        # workspace filter alongside it can only narrow a set that is already
        # correct, or contradict it.
        workspace_id = None if (all_workspaces or parent) else _resolve_workspace(c, workspace)
        parent_id = _project_id(c, parent) if parent else None
        page = c.list_projects(
            workspace_id=workspace_id, tags=tag or None, parent_id=parent_id, **params
        )
    _print_json(_select_fields({"items": page.items, "next_cursor": page.next_cursor}, fields))


@project_app.command("get")
def project_get(
    project_id: str = slug_ref("project"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """Show one project."""
    with _client() as c:
        _print_json(_select_fields(c.get_project(_project_id(c, project_id)), fields))


@project_app.command("contributors")
def project_contributors(
    project_id: str = slug_ref("project"),
    add: str = typer.Option(None, "--add", help="credit this user id"),
    remove: str = typer.Option(None, "--remove", help="drop this user id's direct credit"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """Who worked on this project.

    A project shows up in the workspace of everyone credited here. Credit is
    recorded automatically by writing under the project, including in a
    subproject -- those show `direct: false` with the subproject in
    `via_project_id`. `--add` is for someone who has not written anything yet;
    `--remove` drops a direct credit and is not a ban.
    """
    if add and remove:
        typer.echo("--add and --remove are separate calls; pass one", err=True)
        raise typer.Exit(2)
    with _client() as c:
        pid = _project_id(c, project_id)
        if add:
            _print_json(c.add_project_contributor(pid, add))
            return
        if remove:
            c.remove_project_contributor(pid, remove)
            return
        _print_json(_select_fields({"items": c.list_project_contributors(pid)}, fields))


@project_app.command("use")
def project_use(
    project_id: str = typer.Argument(..., help="project slug to make active (or id:<uuid>)"),
) -> None:
    """Set the active project for this context, so `run start` and friends default to it."""
    with _client() as c:
        proj = c.get_project(_project_id(c, project_id))
    # Pin the project under the workspace that actually owns it, not the ambient one:
    # selecting a project from another workspace should move the anchor, not create a
    # mismatched pair. workspace_id is nullable on legacy rows — fall back to ambient.
    owner = proj.get("workspace_id") or _resolve_workspace(None, None)
    # Stored in the explicit `id:` form: an id survives a rename where a slug does
    # not, but a BARE id would read as a slug when it flows back in as a default.
    save_context(
        {"workspace": {"id": str(owner) if owner else None, "project": f"id:{proj['id']}"}}
    )
    print(f"active project: {proj.get('slug')} ({proj['id']})")


@project_app.command("set")
# `patch` was the original spelling and stays reachable so scripts do not break,
# but it is hidden: experiments, runs and groups all amend with `set`, and an
# agent that learned `experiment set` and guessed `project set` used to get
# `No such command`. One verb is discoverable; the other is a compatibility door.
@project_app.command("patch", hidden=True)
def project_set(
    project_id: str = slug_ref("project"),
    name: str = typer.Option(None, "--name"),
    description: str = description_opt(),
    summary: str = entity_markdown_opt(),
    workspace: str = typer.Option(None, "--workspace", help="not here — use `probe project move`"),
    add_tag: list[str] = add_tag_opt(),
    remove_tag: list[str] = remove_tag_opt(),
    set_tags: list[str] = set_tags_opt(),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Update a project's display fields and tags, in one write."""
    if workspace is not None:
        # Refused on purpose. Re-filing fans out a reindex across every descendant, so
        # it must be the thing you asked for, not a flag that rode along on an edit.
        print(
            "error: --workspace does not belong on `patch` — re-filing a project reindexes\n"
            "       all of its experiments and runs. Use `probe project move` to do that.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    fields = {"name": name, "description": description, "document": _text_value(summary)}
    retagging = _tag_flags_given(add_tag, remove_tag, set_tags)
    if not retagging and all(value is None for value in fields.values()):
        raise typer.BadParameter(
            "pass at least one of --name/--description/--summary/--add-tag/--remove-tag/--set-tags"
        )
    with _client() as c:
        pid = _project_id(c, project_id)
        if retagging:
            current = c.get_project(pid)
            tags, changed = _set_verb_tags(current.get("tags"), add_tag, remove_tag, set_tags)
            if not changed and all(value is None for value in fields.values()):
                _print_json(current)  # the tags already read that way: nothing to write
                return
            fields["tags"] = tags
        _print_json(
            c.update_project(pid, **fields, authored_by=_authored_by_value(authored_by))
        )


@project_app.command("tag")
def project_tag(
    project: str = typer.Argument(..., help="project slug (or id:<uuid>)"),
    add: list[str] = typer.Argument(None, help="tags to add"),
    remove: list[str] = typer.Option(
        None,
        "--remove",
        help="tag to remove; repeatable, ONE tag per flag (a bare word after options is an ADD)",
    ),
    replace: list[str] = typer.Option(
        None, "--set", help="replace the whole list (repeatable; --set '' clears all)"
    ),
) -> None:
    """Tag a project: positional args add, --remove drops, --set replaces; bare lists."""
    with _client() as c:
        pid = _project_id(c, project)
        _print_json(
            _tag_verb_flow(
                pid,
                c.get_project(pid).get("tags"),
                add,
                remove,
                replace,
                lambda wanted: c.update_project(pid, tags=wanted),
            )
        )


@project_app.command("move", context_settings=_PROJECT_KIND_CONTEXT)
def project_move(
    project_id: str = slug_ref("project"),
    parent: str = typer.Option(
        None, "--parent", help="file under this project (slug or id:<uuid>)"
    ),
    top_level: bool = typer.Option(
        False, "--top-level", help="detach: back to a top-level project"
    ),
    workspace: str = typer.Option(
        None, "--workspace", help="destination workspace slug (or id:<uuid>)"
    ),
    kind: ProjectKind = typer.Option(
        None, "--kind", help="also re-declare what the project is for"
    ),
) -> None:
    """Move a project: under a parent, back to top level, or between workspaces.

    Exactly one destination — --parent, --top-level, or --workspace. Filing
    under a parent (0148) re-files the project AND its subtree into the
    parent's workspace (tree = one workspace, owned by the root); the server
    refuses cycles, depth past the cap, and oversized subtree moves. A
    workspace move applies to a top-level project only — a subproject's
    workspace follows its root (409 otherwise) — and reindexes every live
    descendant document in the same transaction. ONE command for all three
    because Typer keeps only the LAST registration of a name: two `move`
    commands shipped once, and the first was silently unreachable.
    """
    destinations = [parent is not None, top_level, workspace is not None]
    if sum(destinations) != 1:
        raise typer.BadParameter("pass exactly one of --parent, --top-level, or --workspace")
    with _client() as c:
        if workspace is not None:
            moved = c.move_project(_project_id(c, project_id), _ref(c, "workspace", workspace).id)
            if kind is not None:
                moved = c.update_project(_project_id(c, project_id), kind=kind.value)
            _print_json(moved)
            return
        kwargs: dict[str, Any] = {}
        if kind is not None:
            kwargs["kind"] = kind.value
        if top_level:
            kwargs["parent_project_id"] = None  # explicit null = detach
        else:
            kwargs["parent_project_id"] = _project_id(c, parent)
        _print_json(c.update_project(_project_id(c, project_id), **kwargs))


@project_app.command("delete")
def project_delete(
    project_id: str = slug_ref("project"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
    recursive: bool = typer.Option(
        False,
        "--recursive",
        help="also delete every SUBPROJECT and everything in them (0148)",
    ),
) -> None:
    """Move a project and everything in it to the trash (Probe support can
    restore it for 21 days, then it is deleted for good). A server without the
    trash deletes it permanently, and the prompt says so.

    A project with live subprojects refuses (409 naming the total blast
    radius) unless --recursive explicitly takes the whole subtree with it.
    """
    _confirmed_delete(
        "project",
        project_id,
        yes=yes,
        cascade=(
            "every experiment, run, metric and file inside it goes too"
            + (", AND every subproject with everything in them" if recursive else "")
        ),
        delete_kwargs={"recursive": True} if recursive else None,
        trash=True,
    )


# -- papers (0152) -----------------------------------------------------------
paper_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "The literature a research project was built from: what each paper "
        "says, the repo read alongside it, and where the two disagree. "
        "Record DURING a review and again at its end."
    ),
)
app.add_typer(paper_app, name="paper")


@paper_app.command("add")
def paper_add(
    project_id: str = slug_ref("project"),
    title: str = typer.Argument(..., help="the paper's title"),
    authors: str = typer.Option(None, "--authors", help='free text, e.g. "Vaswani et al."'),
    source: str = typer.Option(
        ...,
        "--source",
        "--url",
        help="paper URL or local file path (--url remains an alias)",
    ),
    repo: str = typer.Option(None, "--repo", help="the repository read alongside it"),
    summary: str = typer.Option(
        None, "--summary", help="the paper's main idea, in your words (@file.md works)"
    ),
    discrepancies: str = typer.Option(
        None,
        "--discrepancies",
        help="what the repo does that the paper does not say (@file.md works)",
    ),
    tag: list[str] = typer.Option(None, "--tag", help="concept tag (repeatable)"),
    via: str = typer.Option(
        None,
        "--via",
        help=(
            "how you got here: the paper id you followed, or 'none' if you came "
            "to this one directly. Omit only if you genuinely cannot say."
        ),
    ),
    via_provenance: str = typer.Option(
        None,
        "--via-provenance",
        help=(
            "required with --via <id>: observed_call | provider_citation (you found "
            "it in a reference list) | human | inferred"
        ),
    ),
    via_reason: str = typer.Option(
        None, "--via-reason", help="one sentence on why that paper led to this one"
    ),
) -> None:
    """Record one paper against a project.

    The authored title and source are required; `paper update` amends the rest
    later. Provider metadata is captured separately and never rewrites either
    the title or the reviewer's summary.
    --discrepancies is what nothing else captures: censored code, a missing
    ablation, a hyperparameter the repo contradicts.

    --tag is the CONCEPTS this paper is about, in your vocabulary — the axis a
    forty-paper review is grouped on, and the judgement only the reader can
    make. Separate from the provider's own categories, which arrive by
    themselves. Repeat the flag per tag; `paper tag` amends them later.

    NO DEDUPE — two adds of one URL make two rows, so `paper list` first.
    Adding counts as activity on the project; editing and removing do not.

    --via RECORDS THE CHAIN, and it has three answers, not two.
    `--via <paper id>` says you followed that paper to this one.
    `--via none` says you came to this one directly — a bare search, or someone
    handed you the link. OMITTING IT ENTIRELY says you cannot tell, which is a
    different and weaker answer that renders differently.

    Never pass the paper you happened to add last. Read order is not derivation,
    and a chain that quietly encodes it is worse than no chain.

    `--via-provenance provider_citation` means you FOUND this paper in a
    reference list (the parent's, or a provider's list of who cites it). Like
    every --via it records your path through the literature, not the
    literature itself: whether one paper's bibliography names another is a
    `cites` link, which the server reads from the bibliographies on its own
    (`probe paper citations`, `probe paper graph`).
    """
    lineage = None
    if via is not None:
        if via.strip().lower() == "none":
            lineage = {"via": None}
        else:
            # Checked here so the failure names the flag the user typed. The
            # server refuses it too -- this is the friendlier copy of the same
            # rule, never the only one.
            if not via_provenance:
                raise typer.BadParameter(
                    "--via <id> needs --via-provenance: an edge you watched a tool "
                    "make and one a model guessed are different claims, and the "
                    "reader has to be able to tell them apart. Use one of: "
                    "observed_call, provider_citation, human, inferred.",
                    param_hint="--via-provenance",
                )
            lineage = {"via": via, "provenance": via_provenance}
            if via_reason:
                lineage["reason"] = via_reason
    with _client() as c:
        created = c.add_paper(
            _project_id(c, project_id),
            title=title,
            source_url=source,
            authors=authors,
            repo_url=repo,
            summary_md=_text_value(summary),
            discrepancies_md=_text_value(discrepancies),
            tags=list(tag) if tag else None,
            lineage=lineage,
        )
    _print_json(created)


@paper_app.command("edges")
def paper_edges(
    project_id: str = slug_ref("project"),
) -> None:
    """The chain: which paper led to which, across one project's papers.

    Read it before adding a paper you reached by following another one — the
    parent's id is what `--via` takes, and this is where you find it.
    """
    with _client() as c:
        result = c.paper_edges(_project_id(c, project_id))
    _print_json(result)


@paper_app.command("list")
def paper_list(
    project_id: str = slug_ref("project"),
    limit: int = typer.Option(20, "--limit", help="page size (max 50)"),
    tag: list[str] = typer.Option(None, "--tag", help="filter: paper must carry ALL (repeatable)"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """A project's papers, newest first; --tag narrows to a concept."""
    with _client() as c:
        page = c.list_papers(
            _project_id(c, project_id), limit=limit, tags=list(tag) if tag else None
        )
    _print_json(_select_fields(page.items, fields))


@paper_app.command("update")
def paper_update(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
    title: str = typer.Option(None, "--title", help="replace the title"),
    authors: str = typer.Option(None, "--authors", help="replace the author line"),
    source: str = typer.Option(
        None,
        "--source",
        "--url",
        help="replace the paper URL or local file path (--url remains an alias)",
    ),
    repo: str = typer.Option(None, "--repo", help="replace the repository URL"),
    summary: str = typer.Option(None, "--summary", help="replace the summary (@file.md works)"),
    discrepancies: str = typer.Option(
        None, "--discrepancies", help="replace the discrepancies (@file.md works)"
    ),
    tag: list[str] = typer.Option(
        None, "--tag", help="REPLACE the whole tag list (repeatable); `paper tag` amends"
    ),
) -> None:
    """Amend a recorded paper. Omitted fields are untouched; `""` clears any
    except --title and --source, which are required (an empty one is a 422).

    --tag here REPLACES the whole list, like every other `update` verb. Use
    `probe paper tag` to add or drop one tag without restating the rest."""
    with _client() as c:
        updated = c.update_paper(
            paper_id,
            title=title,
            authors=authors,
            source_url=source,
            repo_url=repo,
            summary_md=_text_value(summary),
            discrepancies_md=_text_value(discrepancies),
            tags=list(tag) if tag else None,
        )
    _print_json(updated)


@paper_app.command("tag")
def paper_tag(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
    add: list[str] = typer.Argument(None, help="tags to add"),
    remove: list[str] = typer.Option(
        None,
        "--remove",
        help="tag to remove; repeatable, ONE tag per flag (a bare word after options is an ADD)",
    ),
    replace: list[str] = typer.Option(
        None, "--set", help="replace the whole list (repeatable; --set '' clears all)"
    ),
) -> None:
    """Tag a paper with CONCEPTS: positional args add, --remove drops, --set replaces.

    A bare invocation lists what the paper already carries. This is what makes a
    long reading list groupable — "which of these forty are about retrieval" —
    and it is the one label the reader supplies that the provider cannot: the
    paper's own `extracted_categories` are arXiv's taxonomy, not this lab's.

    Papers take NO author tag. The byline is already the paper's `authors`, and
    whoever recorded it is credited on the project.
    """
    with _client() as c:
        _print_json(
            _tag_verb_flow(
                paper_id,
                c.get_paper(paper_id).get("tags"),
                add,
                remove,
                replace,
                lambda wanted: c.update_paper(paper_id, tags=wanted),
            )
        )


@paper_app.command("remove")
def paper_remove(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
) -> None:
    """Remove a recorded paper."""
    with _client() as c:
        c.remove_paper(paper_id)
    print("removed")


# -- citation links (citation graph, Track C) ---------------------------------
#
# Two READS of what the server already holds: no provider is called. Both print
# a table by default and the server's response with --json.

#: Every display-control character a third-party title or bibliography entry
#: could carry: `_DISPLAY_CONTROLS` (C1 and the bidi embeddings, overrides and
#: isolates `_print_json` escapes), plus C0 and DEL, plus the three bidi MARKS
#: (LRM U+200E, RLM U+200F, ALM U+061C), which reorder a line as surely as an
#: override. Built from the shared class so the two cannot drift. A table cell
#: is one line, so they are removed rather than escaped.
_CITE_CONTROLS = re.compile(
    "[\x00-\x1f\x7f\u200e\u200f\u061c" + _DISPLAY_CONTROLS.pattern[1:-1] + "]"
)

#: Only a server from before the per-tenant citation flag was removed (task
#: C13) answers `state: disabled`; a current one serves every team. Kept so a
#: CLI pointed at such a server says so plainly instead of an empty table.
_CITATIONS_DISABLED = (
    "citation links are not switched on for your team (state: disabled); "
    "nothing has been read for these papers"
)


def _cite_cell(value: Any, width: int | None = None) -> str:
    """One table cell: one line, display controls removed, cut to `width`."""
    if value is None or value == "":
        return "-"
    text = _CITE_CONTROLS.sub("", " ".join(str(value).split()))
    if width is not None and len(text) > width:
        text = text[: width - 1] + "…"
    return text


def _cite_table(headers: list[str], rows: list[list[str]], indent: str = "  ") -> None:
    """Left-aligned columns padded to their widest cell; the last one ragged."""
    widths = [max([len(h), *(len(r[i]) for r in rows)]) for i, h in enumerate(headers)]
    for line in [headers, *rows]:
        cells = [cell.ljust(widths[i]) for i, cell in enumerate(line[:-1])]
        print(indent + "  ".join([*cells, line[-1]]).rstrip())


def _cite_when(value: Any) -> str:
    return str(value)[:10] if value else "never"


def _cite_titled(title: Any, year: Any, width: int = 70) -> str:
    return _cite_cell(f"{title} ({year})" if title and year else title, width)


def _cite_sync_lines(sync: dict | None) -> list[str]:
    """The two fetch statuses of one paper, with their counts."""
    if not sync:
        return ["references: pending · citers: pending (nothing fetched yet)"]
    refs = (
        f"references: {sync.get('references')} · "
        f"{sync.get('references_total') or 0} entries, "
        f"{sync.get('references_linked') or 0} linked · "
        f"fetched {_cite_when(sync.get('references_fetched_at'))}"
    )
    citers = (
        f"citers: {sync.get('citers')} · {sync.get('citers_nominated') or 0} nominated, "
        f"{sync.get('citers_proven') or 0} proven, {sync.get('citers_unchecked') or 0} unchecked"
    )
    if sync.get("citers_not_reconfirmed"):
        citers += f", {sync['citers_not_reconfirmed']} not reconfirmed"
    if sync.get("citers_capped"):
        citers += f", {sync['citers_capped']} dropped at the cap"
    citers += f" · fetched {_cite_when(sync.get('citers_fetched_at'))}"
    lines = [refs, citers]
    if sync.get("stale"):
        lines.append("stale: the paper's ids changed since the last fetch; a refetch is due")
    return lines


def _print_paper_citations(out: dict) -> None:
    state = out.get("state")
    if state == "disabled":
        print(_CITATIONS_DISABLED)
        return
    print(f"paper {out.get('paper_id')} · state: {state}")
    keys = _cite_cell(", ".join(out.get("keys") or []))
    print(f"keys: {'none (no id to read a bibliography for)' if keys == '-' else keys}")
    for line in _cite_sync_lines(out.get("sync")):
        print(line)
    lists = out.get("reference_lists") or []
    if lists:
        print("bibliographies read:")
        _cite_table(
            ["SOURCE", "OWNER", "STATUS", "ENTRIES", "LINKED", "URL"],
            [
                [
                    _cite_cell(item.get("source")),
                    _cite_cell(item.get("owner_key")),
                    _cite_cell(item.get("status")),
                    _cite_cell(item.get("total")),
                    _cite_cell(item.get("linked")),
                    _cite_cell(item.get("url")),
                ]
                for item in lists
            ],
        )
    links = out.get("links") or []
    if not links:
        print("no citation links stored for this paper")
        return
    print()
    rows = []
    for link in links:
        text = _cite_titled(link.get("title"), link.get("year")) if link.get("title") else None
        if text is None:
            text = _cite_cell(link.get("raw_reference"), 70)
        reason = (link.get("detail") or {}).get("reason")
        if link.get("resolution") == "unresolved" and reason:
            text = f"{text} [{_cite_cell(reason)}]"
        rows.append(
            [
                _cite_cell(link.get("direction")),
                _cite_cell(link.get("resolution")),
                _cite_cell(link.get("work_key"), 40),
                _cite_cell(link.get("ordinal")),
                text,
            ]
        )
    _cite_table(["DIRECTION", "PROOF", "WORK", "ENTRY", "TITLE OR ENTRY TEXT"], rows, indent="")
    if out.get("truncated"):
        print(f"truncated: showing {len(links)} rows; raise --limit (max 2000) for the rest")


def _print_citation_graph(out: dict) -> None:
    state = out.get("state")
    if state == "disabled":
        print(_CITATIONS_DISABLED)
        return
    nodes = out.get("nodes") or []
    edges = out.get("edges") or []
    done = out.get("completeness") or {}
    primaries = [n for n in nodes if n.get("kind") == "primary"]
    works = [n for n in nodes if n.get("kind") == "suggested"]
    # Short labels, so an edge reads `P1 cites W3` instead of two uuids.
    label = {n["id"]: f"P{i}" for i, n in enumerate(primaries, 1)}
    label.update({n["id"]: f"W{i}" for i, n in enumerate(works, 1)})
    print(f"project {out.get('project_id')} · state: {state}")
    print(
        f"{done.get('primaries_returned', len(primaries))} of "
        f"{done.get('primaries_total', len(primaries))} papers "
        f"({done.get('primaries_without_id', 0)} without an id, "
        f"{done.get('primaries_pending', 0)} pending) · "
        f"{done.get('suggested_returned', len(works))} of "
        f"{done.get('suggested_candidates', len(works))} suggested works · {len(edges)} edges"
    )
    print(
        f"not linked: {done.get('unresolved_references', 0)} bibliography entries printed no id"
        f" · {done.get('unchecked_citers', 0)} citers unchecked"
        f" · {done.get('not_reconfirmed_citers', 0)} citers not reconfirmed"
    )
    if done.get("truncated"):
        print("truncated: the project has more papers or link rows than one graph reads")
    if not primaries:
        print("no papers in this project")
        return
    print("\nPAPERS")
    rows = []
    for node in primaries:
        sync = node.get("sync") or {}
        stale = " (stale)" if sync.get("stale") else ""
        rows.append(
            [
                label[node["id"]],
                f"{sync.get('references', 'pending')} "
                f"{sync.get('references_linked') or 0}/{sync.get('references_total') or 0}{stale}",
                f"{sync.get('citers', 'pending')} "
                f"{sync.get('citers_proven') or 0}/{sync.get('citers_nominated') or 0}",
                _cite_cell(", ".join(node.get("keys") or []), 40),
                _cite_cell(node.get("paper_id")),
                _cite_titled(node.get("title"), node.get("year"), 60),
            ]
        )
    _cite_table(
        ["#", "REFS LINKED/TOTAL", "CITERS PROVEN/NOMINATED", "KEYS", "PAPER ID", "TITLE"], rows
    )
    if works:
        print("\nSUGGESTED WORKS (ranked by how many of these papers link to each)")
        _cite_table(
            ["#", "LINKS", "CITED BY", "KEY", "TITLE"],
            [
                [
                    label[node["id"]],
                    _cite_cell(node.get("linked_primaries")),
                    _cite_cell(node.get("cited_by_count")),
                    _cite_cell(", ".join(node.get("keys") or []), 40),
                    _cite_titled(node.get("title"), node.get("year"), 60),
                ]
                for node in works
            ],
        )
    if edges:
        print("\nEDGES")
        rows = []
        for edge in edges:
            if edge.get("relation") == "cites":
                evidence = edge.get("evidence") or []
                first = evidence[0] if evidence else {}
                proof = (
                    f"{first.get('direction')} · {first.get('list_source')} "
                    f"#{first.get('ordinal')} · {first.get('resolution')}"
                    if first
                    else "-"
                )
                if len(evidence) > 1:
                    proof += f" (+{len(evidence) - 1} more)"
            else:
                proof = _cite_cell(
                    f"{edge.get('provenance')}: {edge.get('reason')}"
                    if edge.get("reason")
                    else edge.get("provenance"),
                    70,
                )
            rows.append(
                [
                    label.get(edge.get("source"), _cite_cell(edge.get("source"))),
                    _cite_cell(edge.get("relation")),
                    label.get(edge.get("target"), _cite_cell(edge.get("target"))),
                    proof,
                ]
            )
        _cite_table(["SOURCE", "RELATION", "TARGET", "PROOF"], rows)
    unresolved = [(n, n.get("unresolved_references") or []) for n in primaries]
    if any(entries for _, entries in unresolved):
        print("\nUNRESOLVED ENTRIES (no id printed; never an edge)")
        _cite_table(
            ["PAPER", "LIST", "ENTRY", "TEXT"],
            [
                [
                    label[node["id"]],
                    _cite_cell(entry.get("list_owner_key")),
                    _cite_cell(entry.get("ordinal")),
                    _cite_cell(entry.get("raw_reference"), 90),
                ]
                for node, entries in unresolved
                for entry in entries
            ],
        )


@paper_app.command("citations")
def paper_citations(
    paper_id: str = typer.Argument(..., help="paper id (from `probe paper list`)"),
    direction: CitationDirection = typer.Option(
        None,
        "--direction",
        help="reference: what this paper cites; citer: who cites it. Both when omitted.",
    ),
    include_unresolved: bool = typer.Option(
        True,
        "--include-unresolved/--no-include-unresolved",
        help="bibliography entries that printed no id (kept as text, never an edge)",
    ),
    limit: int = typer.Option(
        None, "--limit", min=1, max=2000, help="at most this many rows (server default 500)"
    ),
    as_json: bool = typer.Option(False, "--json", help="print the server's response as JSON"),
) -> None:
    """One paper's citation links, each with the bibliography entry that proves it.

    A `cites` link is a fact about the literature: this paper's reference list
    names that work (`reference`), or that work's list names this paper
    (`citer`). PROOF says how it is known -- `printed_id` (the id is printed in
    the entry), `publisher_id` (the publisher deposited it) or `unresolved` (no
    id: kept as text, never an edge). Nothing is ever linked by a title match.

    Not the same thing as `--via` on `paper add`, which records how YOU got to a
    paper. Read-only: the server fetches bibliographies on its own after a paper
    is recorded.
    """
    with _client() as c:
        out = c.paper_citations(
            paper_id,
            direction=direction.value if direction is not None else None,
            include_unresolved=include_unresolved,
            limit=limit,
        )
    if as_json:
        _print_json(out)
        return
    _print_paper_citations(out)


@paper_app.command("graph")
def paper_graph(
    project: str = typer.Option(
        None,
        "--project",
        help="project slug (or id:<uuid>); defaults to the active one (`probe project use`)",
    ),
    suggested: int = typer.Option(
        None,
        "--suggested",
        min=0,
        max=200,
        help="how many suggested works, ranked by linking papers (server default 50; 0 for none)",
    ),
    direction: CitationDirection = typer.Option(
        None,
        "--direction",
        help="reference: what the papers cite; citer: who cites them. Both when omitted.",
    ),
    min_links: int = typer.Option(
        None,
        "--min-links",
        min=1,
        help="a suggested work needs at least this many of the project's papers linking to it",
    ),
    include_discovery: bool = typer.Option(
        False,
        "--include-discovery",
        help="also show the discovered_via edges among the papers (how you got to each)",
    ),
    include_unresolved: bool = typer.Option(
        False,
        "--include-unresolved",
        help="also list each paper's bibliography entries that printed no id",
    ),
    as_json: bool = typer.Option(False, "--json", help="print the server's response as JSON"),
) -> None:
    """A project's citation graph: its papers, the works they cite or are cited
    by, and the `cites` edges among them.

    SUGGESTED WORKS are works the project has not recorded that its papers link
    to, ranked by how many of THIS project's papers do, then by citation count,
    and capped (never padded). Every `cites` edge carries the bibliography entry
    that proves it: an id printed in the entry or deposited by the publisher,
    never a title match or a provider's guess. To record a suggested work, use
    `probe paper add` with its URL.

    `discovered_via` edges (with --include-discovery) are your path through the
    literature, shown as stored and never as `cites`. Read-only: nothing here
    calls a provider.
    """
    resolved = _ambient_project(project)
    if resolved is None:
        raise typer.BadParameter(
            "no project: pass --project, or set one with `probe project use`",
            param_hint="--project",
        )
    with _client() as c:
        out = c.citation_graph(
            _project_id(c, resolved),
            suggested=suggested,
            directions=[direction.value] if direction is not None else None,
            min_links=min_links,
            include_discovery=include_discovery or None,
            include_unresolved=include_unresolved or None,
        )
    if as_json:
        _print_json(out)
        return
    _print_citation_graph(out)


# -- project references (0153) -----------------------------------------------
reference_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "Lateral links between projects: A references B. Use this when a "
        "review informed a training run, or two efforts share a method — the "
        "relation --parent would claim wrongly. Cycles and any depth are fine."
    ),
)
project_app.add_typer(reference_app, name="reference")


@reference_app.command("add")
def project_reference_add(
    project_id: str = slug_ref("project"),
    to: str = typer.Option(..., "--to", help="the project it references (slug or id:<uuid>)"),
) -> None:
    """Record that this project references another.

    Idempotent and DIRECTED: adding A->B does not add B->A. Neither project
    moves — this is not `--parent`, and nothing is nested by it.
    """
    with _client() as c:
        c.add_project_reference(_project_id(c, project_id), _project_id(c, to))
    print("referenced")


@reference_app.command("remove")
def project_reference_remove(
    project_id: str = slug_ref("project"),
    to: str = typer.Option(..., "--to", help="the referenced project (slug or id:<uuid>)"),
) -> None:
    """Drop one directed edge; the opposite direction stays."""
    with _client() as c:
        c.remove_project_reference(_project_id(c, project_id), _project_id(c, to))
    print("removed")


# -- project code sources (0134) ---------------------------------------------
code_app = typer.Typer(
    no_args_is_help=True,
    help=(
        "The project's attached GitHub repositories. The commit timeline is "
        "read THROUGH GitHub by the backend — nothing is mirrored, so attach "
        "is cheap and detach loses nothing."
    ),
)
project_app.add_typer(code_app, name="code")


@code_app.command("attach")
def project_code_attach(
    project_id: str = slug_ref("project"),
    repo: str = typer.Argument(..., help="owner/name, or a github.com URL"),
    branch: str = typer.Option(
        None, "--branch", help="branch to follow; default: the repo's default branch"
    ),
    path: str = typer.Option(
        "", "--path", help="monorepo subtree, e.g. training/ (empty = whole repo)"
    ),
    start_sha: str = typer.Option(
        None, "--start-sha", help="history starts here (the project's first commit)"
    ),
    start_at: str = typer.Option(
        None, "--start-at", help="ISO timestamp lower bound (alternative to --start-sha)"
    ),
    readme_embed: bool = typer.Option(
        False,
        "--readme-embed",
        help="also add the [README](…) line to the project's Overview document",
    ),
    reason: str = typer.Option(
        None,
        "--reason",
        help=(
            "why this repo is this project's code — required when an agent "
            "attaches on its own judgment; rendered next to the attribution"
        ),
    ),
    via: str = typer.Option(
        "cli",
        "--via",
        help="attribution shown on the source: cli | agent | wizard",
        hidden=True,
    ),
) -> None:
    """Attach a repository (and branch) so its commit timeline shows on the project.

    Attaching grants no access: the repo must already be covered by the team's
    GitHub App installation, or be public. The strongest evidence is a run
    whose code snapshot names this remote — cite it in --reason.
    """
    with _client() as c:
        source = c.attach_project_code_source(
            _project_id(c, project_id),
            repo=repo,
            ref=branch,
            path_prefix=path or "",
            start_sha=start_sha,
            start_at=start_at,
            add_readme_embed=readme_embed,
            via=via if via in ("cli", "agent", "wizard") else "cli",
            reason=reason,
        )
    _print_json(source)


@code_app.command("list")
def project_code_list(
    project_id: str = slug_ref("project"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """The attached repositories, with status (active / suggested / missing / revoked)."""
    with _client() as c:
        _print_json(_select_fields(c.list_project_code_sources(_project_id(c, project_id)), fields))


@code_app.command("detach")
def project_code_detach(
    project_id: str = slug_ref("project"),
    source_id: str = typer.Argument(..., help="code source id (from `project code list`)"),
) -> None:
    """Detach one repository. Loses nothing but the connection — nothing is mirrored."""
    with _client() as c:
        c.detach_project_code_source(_project_id(c, project_id), source_id)
    print("detached")


@code_app.command("confirm")
def project_code_confirm(
    project_id: str = slug_ref("project"),
    source_id: str = typer.Argument(..., help="suggested source id (from `project code list`)"),
) -> None:
    """Confirm a suggested source (one a run's code snapshot volunteered)."""
    with _client() as c:
        _print_json(c.confirm_project_code_source(_project_id(c, project_id), source_id))


@app.command("commits")
def commits(
    project_id: str = typer.Argument(..., help="project slug (or id:<uuid>)"),
    source: str = typer.Option(
        None, "--source", help="code source id, when several repos are attached"
    ),
    cursor: str = typer.Option(None, "--cursor", help="next-page cursor from a previous page"),
    author: str = typer.Option(None, "--author", help="GitHub login filter"),
    path: str = typer.Option(None, "--path", help="only commits touching this path"),
    limit: int = typer.Option(30, "--limit", min=1, max=50),
    include_excluded: bool = typer.Option(
        False, "--include-excluded", help="also show commits a person excluded"
    ),
    sha: str = typer.Option(
        None, "--sha", help="ONE commit in full (message body, files, linked runs)"
    ),
    fields: str = _FIELDS_OPTION,
) -> None:
    """One page of the project's commit timeline, newest first.

    Read THROUGH GitHub with an honest `state`: `stale` is real data GitHub
    could not refresh just now; `unavailable` means no answer (the reason says
    why) — never an empty history. A run count on a row means runs in this
    project were BASED ON that commit (nearest pushed ancestor).
    """
    with _client() as c:
        resolved = _project_id(c, project_id)
        if sha:
            _print_json(_select_fields(c.get_project_commit(resolved, sha, source), fields))
            return
        page = c.list_project_commits(
            resolved,
            source_id=source,
            cursor=cursor,
            author=author,
            path=path,
            limit=limit,
            include_excluded=include_excluded or None,
        )
    _print_json(_select_fields(page, fields))


# -- tokens -----------------------------------------------------------------
token_app = typer.Typer(no_args_is_help=True, help="API tokens (probe_pat_...)")
app.add_typer(token_app, name="token")


@token_app.command("list")
def token_list() -> None:
    """List my live tokens. Secrets are never shown — match on `token_prefix`."""
    with _client() as c:
        _print_json(c.list_tokens())


@token_app.command("create")
def token_create(
    name: str = typer.Option(..., "--name", help="what this token is for, e.g. 'ci-bot'"),
    scope: list[Scope] = typer.Option(
        None,
        "--scope",
        help="repeatable; omit to request read+write+delete (never admin). A token can "
        "never exceed the scopes your role confers.",
    ),
    no_browser: bool = typer.Option(
        False, "--no-browser", help="print the URL instead of opening it"
    ),
) -> None:
    """Mint a token via the browser device flow — approve in the dashboard.

    Minting deliberately requires a human in a browser (a leaked token must not be
    able to mint more tokens), so this prints a URL + code and waits for approval.
    The secret is printed ONCE and never stored; copy it now.
    """
    # PRB-002: the device flow no longer grants admin (the server refuses it), so
    # fail fast with a clear message instead of a round-trip to a 400. Admin
    # tokens must be minted from a signed-in session.
    if scope and Scope.admin in scope:
        print(
            "admin tokens can't be minted from the CLI; mint one from a signed-in session.",
            file=sys.stderr,
        )
        raise typer.Exit(2)
    with _client() as c:
        print(f"opening {c.settings.base_url} for browser approval…")
        try:
            created = c.create_token(
                name,
                scopes=[s.value for s in scope] if scope else None,
                open_browser=not no_browser,
                on_prompt=_show_device_prompt,
            )
        except DeviceLoginError as exc:
            print(f"token creation failed: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc

    # The token is already minted server-side; its plaintext exists exactly once. Read
    # the secret FIRST so a missing name/id (response drift) can't KeyError before it is
    # shown and orphan an unrecoverable token. name/id are decorative — fall back.
    secret = created["token"]
    label = created.get("name", name)
    token_id = created.get("id", "unknown")
    # Shown once, and only here: not via _print_json (which invites piping it to a
    # file) and never written to config.
    print(f"\ntoken {label!r} created (id: {token_id})")
    print(f"\n  {secret}\n")
    print("^ copy it now — this is the only time it is shown.", file=sys.stderr)


@token_app.command("revoke")
def token_revoke(
    token_id: str = typer.Argument(..., help="token id (from `probe token list`)"),
) -> None:
    """Revoke one of my tokens. Revoking a teammate's needs the dashboard."""
    with _client() as c:
        c.revoke_token(token_id)
    print(f"revoked {token_id}")


# -- run lifecycle ----------------------------------------------------------
run_app = typer.Typer(no_args_is_help=True, help="run lifecycle")
app.add_typer(run_app, name="run")


@run_app.command("start")
def run_start(
    experiment: str = typer.Option(
        None,
        "--experiment",
        help="slug of an EXISTING experiment; omit for a PROJECT-DIRECT run (W&B shape)",
    ),
    name: str = typer.Option(
        None,
        "--name",
        help="defaults to the run's slug, or a server petname when there is none, "
        "which a generated title then replaces once the run ends",
    ),
    slug: str = typer.Option(
        None,
        "--slug",
        help="this run's slug; omit and the server mints a petname (a taken one is an error)",
    ),
    description: str = description_opt(),
    project: str = typer.Option(
        None,
        "--project",
        help="project slug (or id:<uuid>); defaults to the active one (`probe project use`)",
    ),
    group: str = typer.Option(None, "--group", help="run group id (see `probe group create`)"),
    source: str = typer.Option("api", "--source"),
    external_id: str = typer.Option(None, "--external-id"),
    config: list[str] = typer.Option(None, "--config", metavar="k=v"),
    tag: list[str] = typer.Option(None, "--tag"),
    rewind_to_step: int = typer.Option(
        None,
        "--rewind-to-step",
        min=0,
        help="relaunch of --external-id from a checkpoint: DISCARD its record "
        "from this step onward and rewrite it (0185). Unlocks a completed "
        "incumbent; without this flag nothing is ever deleted.",
    ),
    intent: str = typer.Option(
        None, "--intent", help="what this run is meant to show (free text, kept in its metadata)"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Open a run inside an EXISTING experiment, or directly under a project.

    This no longer creates the experiment or project. Create them first with
    `probe project create` / `probe experiment create`; an unknown slug now errors
    and names the closest existing ones instead of minting a second identity.
    Without --experiment the run attaches straight to the project (--project or
    the active one) with no experiment at all — the W&B model. With neither and
    no active project it opens FLOATING (daemon v2): the Probe daemon files it,
    or `probe run move` does.
    """
    # This is what makes `probe project use` mean something: without it the ambient
    # project would be stored and displayed but never actually applied to a write.
    # Explicit flag still wins, so scripts never depend on a developer's context.
    resolved_project = _ambient_project(project)
    if rewind_to_step is not None and not external_id:
        # A rewind resumes an EXISTING identity; without the key there is no
        # incumbent to rewind and the flag would silently do nothing.
        raise errors.ValidationError(
            "--rewind-to-step needs --external-id: the rewind targets the "
            "existing run that identity names"
        )
    # 0205, DEPRECATION RELEASE. A bare `run start` opens a row that nothing
    # owns: this process exits immediately, never beats, and the run survives
    # only until the reaper notices. Measured on one tenant: 41 of 41 runs
    # opened this way, 3 with any owner heartbeat, 8 ended 'untracked' ~16
    # minutes into work that was still running. The next release refuses it; for
    # now it warns and creates, so nobody's script breaks on the release that
    # tells them.
    typer.echo(
        "probe: `run start` opens a run nothing owns -- it will be marked "
        "'untracked' once it goes quiet, even if the work is fine.\n"
        "       probe exec [--project P] -- CMD      wrap the process; status from its exit code\n"
        "       probe.init() inside the job          attaches via PROBE_RUN_ID; heartbeats\n"
        "       connect W&B in the dashboard         a connector owns the run\n"
        "       This command is refused in the next release.",
        err=True,
    )
    with _client() as c:
        run = c.run(
            experiment=experiment,
            on_conflict=(Rewind(step=rewind_to_step) if rewind_to_step is not None else "auto"),
            name=name,
            # Omitted = the server mints a petname, unchanged. Naming it is what
            # lets a nightly job address the same run every time.
            slug=slug,
            description=description,
            # run() resolves by SLUG, so an id has to be translated first or the
            # lookup misses and reports a real project as absent.
            project=_project_slug(c, resolved_project),
            group_id=group,
            source=source,
            external_id=external_id,
            config=_kv_pairs(config) if config else None,
            tags=tag or None,
            intent=intent,
            # A CLI-opened run is detached: this process exits immediately and the
            # run is closed later by `probe run end`. Beating here would stop the
            # moment we exit and get the run reaped mid-flight (see heartbeat_run).
            heartbeat=False,
            # Reaches the run AND, through run()'s ensure_* paths, any project or
            # experiment auto-created alongside it.
            authored_by=_authored_by_value(authored_by),
        )
        # Pin this bracket's writer generation in the auto-update lease (0185):
        # every later run-scoped CLI write stamps this epoch, so a bracket
        # superseded by a reopen elsewhere is refused instead of splicing.
        run_lock_touch_lease(run.id, write_epoch=run.write_epoch)
    print(run.id)
    _print_link("run", run.id)


@run_app.command("fork")
def run_fork(
    source: str = typer.Argument(..., help="source run (slug or id:<uuid>)"),
    step: int = typer.Option(
        None, "--step", min=0, help="the checkpoint step this fork continues from"
    ),
    name: str = typer.Option(None, "--name", help="defaults to <source>-fork"),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Open a NEW run continuing SOURCE from --step; SOURCE stays untouched.

    The keep-both alternative to `run start --rewind-to-step`: the fork logs
    from the checkpoint onward under its own identity (parent_relation="fork" +
    fork_of/fork_step foreign keys) and the source keeps its whole curve,
    unmarked — unlike supersede, this is not a correction of anything.
    """
    with _client() as c:
        run = c.fork_run(
            str(_ref(c, "run", source).id),
            step=step,
            name=name,
            # Detached like `run start`: this process exits immediately.
            heartbeat=False,
            authored_by=_authored_by_value(authored_by),
        )
        run_lock_touch_lease(run.id, write_epoch=run.write_epoch)
    print(run.id)
    _print_link("run", run.id)


@run_app.command("child")
def run_child(
    run: str = run_ref(),
    name: str = typer.Option(None, "--name", help="omit it: the server mints a name"),
    description: str = description_opt(),
    # REQUIRED. Defaulted to `fork` until the lineage audit: the four relations
    # mean different things, and a default writes the most common one onto every
    # caller who did not think about it.
    relation: Relation = typer.Option(..., "--relation"),
    source: str = typer.Option("api", "--source"),
    external_id: str = typer.Option(None, "--external-id"),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Open a sub-run under an existing run.

    The child inherits the parent's attachment: its experiment when it has one,
    else its project (a project-direct parent begets a project-direct child), and
    a floating parent (no project yet) begets a floating child.
    """
    # 0205, same rule as `run start` (D30): a child is its own row and the
    # reaper judges it on its own signals. Inheriting the parent's beats would
    # make a dead child read 'running' for as long as the parent lives, which is
    # the hollow row one level down.
    typer.echo(
        "probe: `run child` opens a run nothing owns. Wrap the child's process "
        "with `probe exec`, or let it attach from inside via PROBE_RUN_ID.\n"
        "       This command is refused in the next release.",
        err=True,
    )
    with _client() as c:
        parent = _ref(c, "run", run).row
        common = dict(
            # The parent's ID, not the ref the caller typed. `parent_run_id` is a
            # UUID field, so a petname here reached the server as one and was
            # rejected -- and the row was already in hand to answer it.
            parent_run_id=parent["id"],
            parent_relation=relation.value,
            description=description,
            source=source,
            external_id=external_id,
            heartbeat=False,  # detached, same as `run start`
            authored_by=_authored_by_value(authored_by),
        )
        if parent.get("experiment_id"):
            child = c.create_run(parent["experiment_id"], name, **common)
        elif parent.get("project_id"):
            child = c.create_project_run(parent["project_id"], name, **common)
        elif "project_id" in parent:
            # A FLOATING parent (daemon v2): the child floats with it.
            child = c.create_floating_run(name, **common)
        else:
            # A pre-0054 backend's run rows carry no project_id field at all;
            # a KeyError traceback here would say nothing actionable.
            raise errors.ValidationError(
                f"run {run} reports neither an experiment nor a project — this "
                "research-os backend predates project-direct runs (0054). "
                "Upgrade the backend, or open the child under an experiment "
                "with `probe run start --experiment`."
            )
    print(child.id)


@run_app.command("set")
def run_set(
    run: str = run_ref(),
    name: str = typer.Option(None, "--name"),
    description: str = description_opt(),
    notes: str = notes_opt(),
    status: RunCorrection = typer.Option(
        None,
        "--status",
        help=(
            "correct a finished run's status; start and end times are kept. `failed` "
            "emails the run's launcher. To close a running run, `run end`"
        ),
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Update a run's human title, description, notes or status.

    `--status` corrects a FINISHED run's record and sends no start or end time,
    so the run's duration stays as recorded. Only finished statuses are taken:
    `running` or `created` on a finished run would skip the reopen guard, and
    the reaper would later mark it crashed and email the launcher. `probe run
    end --status` is not the same thing: it stamps the end time NOW, which
    rewrites the duration of a run that finished long ago.

    `--notes` is NOT a second description, and the difference decides which one a
    caveat goes in. A description says what the run IS and is written before it
    runs; notes say what a later reader should DISTRUST about it, and are nearly
    always learned after it finished -- a broken verifier, an environment that
    was not what it claimed, a number that means less than it looks like it does.
    Writing the caveat into the description means destroying the description to
    keep it.

    A run scored 0.0 by a broken harness is the case this exists for: tag it
    (`probe run tag RUN invalid`) so a reader is warned, and write the notes so
    they know why.
    """
    if name is None and description is None and notes is None and status is None:
        raise typer.BadParameter("pass at least one of --name/--description/--notes/--status")
    with _client() as c:
        # PATCH /v1/runs/{run_id} is UUID-typed, so a petname has to be resolved
        # before it is sent -- unresolved it 422s with a raw pydantic uuid dump.
        # Same reason `run delete` resolves; this verb was missed by that pass.
        _print_json(
            c.update_run(
                _ref(c, "run", run).id,
                name=name,
                description=description,
                notes=_text_value(notes),
                status=status.value if status is not None else None,
                authored_by=_authored_by_value(authored_by),
            )
        )


@run_app.command("move")
def run_move(
    run: str = run_ref(),
    to: str = typer.Option(..., "--to", help="the project or experiment to file the run in (slug or id:<uuid>)"),
    group: str = typer.Option(None, "--group", help="a sweep group inside that experiment (group id)"),
) -> None:
    """File a run in a project or experiment (and optionally a sweep group).

    Runs can start with no project -- the SDK opens them floating -- and get filed
    afterwards; a filed run can be refiled the same way. Its metrics, files,
    notes and lineage move with it. Unfiling is not a thing: a run once filed
    always has a home."""
    with _client() as c:
        run_id = _ref(c, "run", run).id
        target = _project_id(c, to)
        _print_json(c.move_run(run_id, project_id=target, group_id=group))


@run_app.command("list")
def run_list(
    experiment: str = typer.Option(None, "--experiment", help="experiment slug (or id:<uuid>)"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    direct: bool = typer.Option(False, "--direct", help="only project-direct runs"),
    tag: list[str] = typer.Option(None, "--tag", help="filter: run must carry ALL (repeatable)"),
    unfiled: bool = typer.Option(
        False, "--unfiled", help="only runs not filed in any project yet (yours; every one for an admin)"
    ),
    limit: int = typer.Option(50, "--limit", min=1, max=200),
    cursor: str = typer.Option(None, "--cursor", help="keyset cursor from a previous page"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """List runs, filterable by experiment, project, and tags (AND semantics)."""
    params: dict[str, Any] = {"limit": limit}
    if cursor:
        params["cursor"] = cursor
    if unfiled and (experiment or project or direct):
        raise typer.BadParameter("--unfiled lists runs with no project: drop --experiment/--project/--direct")
    with _client() as c:
        page = c.list_runs(
            # Resolved, not passed through: experiment_id is a UUID-typed query
            # param, so a slug used to come back as a raw pydantic uuid_parsing
            # dump rather than a listing.
            experiment_id=_ref(c, "experiment", experiment).id if experiment else None,
            project_id=_project_id(c, project) if project else None,
            direct=direct,
            tags=tag or None,
            # Through the SDK's guard: a backend that ignores the filter answers
            # with filed runs, and that is refused rather than listed as unfiled.
            unfiled=unfiled,
            **params,
        )
    _print_json(_select_fields({"items": page.items, "next_cursor": page.next_cursor}, fields))


@run_app.command("tag")
def run_tag(
    run: str = run_ref(),
    add: list[str] = typer.Argument(None, help="tags to add"),
    remove: list[str] = typer.Option(
        None,
        "--remove",
        help="tag to remove; repeatable, ONE tag per flag (a bare word after options is an ADD)",
    ),
    replace: list[str] = typer.Option(
        None, "--set", help="replace the whole list (repeatable; --set '' clears all)"
    ),
) -> None:
    """Tag a run: positional args add, --remove drops, --set replaces; bare lists.

    Read-modify-write over PATCH's whole-list replace (the server normalizes to
    lowercase-kebab and 422s past the caps). Retro-tag runs the SDK is DONE
    with: a still-live run's next push replaces out-of-band edits (last writer
    wins — CONTRACT.md "tags")."""
    with _client() as c:
        handle = _run_handle(c, run)
        # strict=True: an interactive tag edit must fail loudly, never spool a
        # stale whole-list replace for delayed replay (review 2026-07-30).
        _print_json(
            _tag_verb_flow(
                handle.id,
                handle.tags,
                add,
                remove,
                replace,
                lambda wanted: handle.set_tags(wanted, strict=True),
            )
        )


@run_app.command("expect")
def run_expect(
    run: str = run_ref(),
    key: str = typer.Argument(..., help="metric key, e.g. val/acc"),
    minimum: Optional[float] = typer.Option(None, "--min", help="email when a value goes below this"),
    maximum: Optional[float] = typer.Option(None, "--max", help="email when a value goes above this"),
    clear: bool = typer.Option(False, "--clear", help="remove the range declared for KEY"),
) -> None:
    """Declare the range a metric should stay in; Probe emails the run's creator
    the first time a value leaves it.

    For a run already going -- no code change, no restart. A script declares the
    same thing with `probe.expect({...})`. Every value already logged for the key
    is judged too; the same range declared again does not re-send an email."""
    if clear and (minimum is not None or maximum is not None):
        raise typer.BadParameter("--clear takes no --min/--max")
    if not clear and minimum is None and maximum is None:
        raise typer.BadParameter("give --min, --max (or both), or --clear")
    for flag, bound in (("--min", minimum), ("--max", maximum)):
        if bound is not None and not math.isfinite(bound):
            raise typer.BadParameter(f"{flag} must be a finite number")
    if minimum is not None and maximum is not None and minimum > maximum:
        raise typer.BadParameter(f"--min {minimum} is above --max {maximum}")
    with _client() as c:
        handle = _run_handle(c, run)
        # strict=True: an interactive declaration must fail loudly, never spool.
        handle.expect({key: None if clear else (minimum, maximum)}, strict=True)
        _print_json(
            {"run": handle.id, "key": key, "removed": True}
            if clear
            else {"run": handle.id, "key": key, "min": minimum, "max": maximum}
        )


@run_app.command("end")
def run_end(
    run: str = run_ref(),
    status: EndStatus = typer.Option(EndStatus.completed, "--status"),
    flush_timeout: Optional[float] = typer.Option(
        None,
        "--flush-timeout",
        envvar="PROBE_FINISH_TIMEOUT_SEC",
        help="Bounded barrier (F3): keep draining this run's ops up to N "
        "seconds, then queue the close BEHIND whatever remains and exit 0 -- "
        "for jobs that must not hold hardware on a dead API. Dead letters "
        "and auth blocks still exit 2.",
    ),
    write_mode: Optional[bool] = write_mode_opt(),
) -> None:
    """Close a run.

    Synchronous mode is a RUN-SCOPED barrier (T3-A): this run's queued outbox
    ops are delivered first, and the run is not closed while any of them cannot
    be -- unrelated runs' stuck items never block it. Async mode enqueues the
    close as a journal op ORDERED BEHIND everything the run already queued, so
    the run only closes after its data lands; nothing blocks.

    THIS VERB DOES NOT FOLLOW THE ASYNC DEFAULT, and that is the point of it.
    `log`, `span add` and run-anchored `artifact add` queue unless told not to;
    `run end` blocks unless told to queue. It is the only command that verifies
    delivery -- drain this run's ops, refuse to close while any of them cannot
    land, exit 2 -- so a job that ends with it cannot exit 0 with data stuck on
    a disk that is about to be torn down. It also runs ONCE per run, so it was
    never on the hot path the default flip exists to speed up.

    f073194c is why this is spelled out: replacing set_status's strict=True with
    sync= let strict resolve to False for the CLI, and a typo'd run ref then
    journaled, printed success and exited 0 -- the exact opposite of a barrier.
    Making async the default here would reopen that from the other side.
    """
    if _resolve_write_mode(write_mode) is True:
        from ..sdk.durable import now_iso

        with _async_client() as c:
            # set_status, not finish(): finish() flushes synchronously, which is
            # exactly what async mode must not do. Ordering is the barrier here.
            _async_run(c, run).set_status(status.value, ended_at=now_iso())
        _kick_drainer()
        print(f"queued end for {run} -> {status.value} (async)")
        # The run page is already live and shows the close landing, so the link
        # is worth handing back even though the status is still in flight.
        _print_link("run", run)
        return
    from ..sdk.journal import drain
    from ..sdk.run import WAITING_PROMOTE_TIMEOUT

    journal = _journal()
    # Every queue: a PROBE_TOKEN or in-code writer's ops live in their own
    # credential queue (#2035), and the barrier is about the run's RESULT.
    queues = journal.namespaces()
    # This attempt's write epoch, when `run start` pinned one: a write an OLDER
    # attempt queued is refused by the server as superseded, so it never holds
    # this close (#2041 round 5, a rotated PROBE_TOKEN's leftovers).
    try:
        from . import run_lock

        epoch = run_lock.lease_write_epoch(run)
    except Exception:  # noqa: BLE001 -- best-effort, like the lease tier itself
        epoch = None

    def of_run(listing) -> list[dict]:
        return [op for queue in queues for _, op in listing(queue) if op.get("run_ref") == run]

    def queued_of_run() -> list[dict]:
        from ..sdk.journal import _write_epoch_of

        def current(op: dict) -> bool:
            theirs = _write_epoch_of(op)
            return epoch is None or theirs is None or theirs >= epoch

        return [op for op in of_run(lambda q: q.pending()) if current(op)]

    # This run's uploads still waiting for their credential scan must become
    # ops BEFORE the barrier drain, or the drain would pass without them and
    # the close would land ahead of them. Local CPU; seconds.
    for queue in queues:
        if not queue.receipt_enabled:
            queue.promote_for_close(run, timeout=WAITING_PROMOTE_TIMEOUT)
    if flush_timeout is None:
        report = drain(journal, run_ref=run)
    else:
        deadline = time.monotonic() + max(flush_timeout, 0.0)
        while True:
            report = drain(journal, run_ref=run)
            left = queued_of_run()
            newly_dead = of_run(lambda q: q.failed())
            if not left or newly_dead or report.auth_blocked or time.monotonic() >= deadline:
                break
            time.sleep(min(0.25, max(deadline - time.monotonic(), 0.0)))
    dead = of_run(lambda q: q.failed())
    # Anything of this run's still queued after the drain (paused journal, a
    # skipped pass, any future skip condition) also blocks the close -- the
    # barrier promise is about the RESULT, not about which flag tripped.
    still_queued = queued_of_run()
    still_waiting = [
        item for queue in queues if not queue.receipt_enabled for item in queue.waiting_for_close(run)
    ]
    if still_waiting:
        typer.echo(
            f"run {run} NOT closed: {len(still_waiting)} queued upload(s) could not be "
            "prepared for delivery (credential scan). See `probe outbox status`, then "
            "re-run `probe run end`.",
            err=True,
        )
        raise typer.Exit(2)
    if flush_timeout is not None and still_queued and not dead and not report.auth_blocked:
        # Bounded barrier expired on retryable ops only: queue the close
        # BEHIND them (F3) and let the detached worker land everything. Dead
        # letters and auth blocks fall through to exit 2 -- deferring cannot
        # heal a permanent rejection, and a worker never runs auth-blocked.
        with _client() as c:
            _async_run(c, run)._queue_deferred_finish(status.value, None, len(still_queued))
        typer.echo(
            f"end queued for {run} -> {status.value} behind "
            f"{len(still_queued)} pending op(s); the background worker keeps "
            "retrying — `probe outbox watch` to follow",
            err=True,
        )
        _print_link("run", run)
        # The local writer is done even though the close rides the queue; a
        # held lease would only delay an upgrade (the cheap failure mode).
        try:
            from . import run_lock

            run_lock.clear_lease(run)
        except Exception:  # noqa: BLE001 -- an expiring lease is the backstop
            pass
        return
    if report.auth_blocked or report.stopped_transient or dead or still_queued:
        detail = "; ".join(
            report.errors[-3:]
            or [op.get("last_error") or "?" for op in dead[:3]]
            # Held, not failed: queued under a credential this shell does not
            # have (another job's PROBE_TOKEN, #2035) -- that job delivers them.
            or list(getattr(report, "held_reasons", None) or [])[:3]
            or [f"{len(still_queued)} still queued"]
        )
        typer.echo(
            f"run {run} NOT closed: its outbox items could not all be delivered "
            f"({detail}). Fix (see `probe outbox status`), retry dead letters "
            "with `probe outbox retry`, then re-run `probe run end`.",
            err=True,
        )
        raise typer.Exit(2)
    from ..sdk.durable import now_iso as _now_iso

    with _client() as c:
        # set_status, not finish(): the run-scoped barrier above already
        # delivered THIS run's ops; finish() would foreground-drain the whole
        # machine-wide journal — other runs' queued gigabytes — inside this
        # command (red team: 'unrelated runs never block it' held for
        # correctness but not for time).
        # strict=True: `probe run end` without --async is the delivery barrier
        # (mcp/server.py documents it as "delivers that run's queued items or
        # fails loudly"). Without it the CLI client's fail_open=True resolves
        # strict to False, so a TransportError -- or a typo'd run ref's 404 --
        # would journal, print success and exit 0, which is the opposite of a
        # barrier. The lease clear and deferred update below both assume the
        # run really is terminal, so they must not be reached on a failure.
        _run_handle(c, run).set_status(status.value, ended_at=_now_iso(), strict=True)
    # The run is terminal, so release its claim on the box immediately rather
    # than waiting out the lease. Done AFTER set_status and outside the client
    # block: a lease that outlives its run only delays an upgrade, while one
    # dropped before the run actually closed would let an upgrade land on it.
    try:
        from . import run_lock

        run_lock.clear_lease(run)
    except Exception:  # noqa: BLE001 -- an expiring lease is the backstop
        pass
    # The run is terminal and its lease is gone: this is one of exactly two
    # moments where an update that `_version_notice` found and refused can be
    # applied. NOT the queued path above -- that one returns with a detached
    # outbox worker still delivering this run's close, and upgrading the tree
    # under it is the lazy-import hazard the whole design avoids.
    _apply_deferred_update()
    print(f"{run} -> {status.value}")
    # The run just became terminal: this is the moment its page is worth opening,
    # and the last one at which anything is printed about it.
    _print_link("run", run)


@run_app.command("check")
def run_check(
    run: str = run_ref(),
    verify: bool = typer.Option(False, "--verify"),
) -> None:
    """Assess capture completeness (exit 2 if incomplete).

    Default is `unverified`: nothing is obviously absent, which is NOT the same
    as "this run can be rebuilt". `--verify` resolves the recorded code commit
    against its remote and is the only way to earn `complete`.

    `advisories` lists reported-but-not-blocking gaps (notes, inputs-decision,
    legacy runs without launch context).
    """
    with _client() as c:
        result = c.check_run(_ref(c, "run", run).id, verify=verify)
    _print_json(result)
    if result.get("state") == "incomplete":
        raise typer.Exit(2)


def _materialize_record(c: Any, run_id: str, record: dict, dest: str) -> dict:
    """Reconstruct a runnable directory from a reproduction record: restore the
    captured code tree (lockfiles included — they ride in the tree), write the
    inputs-decision artifacts that carry inline content, and drop the full record
    as ``reproduce-manifest.json``.

    An inputs-decision whose content was omitted (too large to inline) is written
    as a ``.omitted`` marker naming the reason rather than skipped — a missing file
    with no note reads as "there was nothing", which is the confident-wrong answer
    the reproduce surface exists to avoid.
    """
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    written: dict[str, Any] = {
        "dest": str(dest_path),
        "code_tree": None,
        "inputs": [],
        "manifest": None,
    }

    env_ref = (record.get("run") or {}).get("env_ref")
    if env_ref:
        result = _restore_captured_tree(c, run_id, env_ref, str(dest_path))
        written["code_tree"] = {
            "n_restored": result["n_restored"],
            "n_unavailable": result["n_unavailable"],
            "tree_matches": result["tree_matches"],
        }
    else:
        written["code_tree"] = "no execution record — code tree not captured"

    for item in record.get("inputs_decision") or []:
        artifact = item.get("artifact") or {}
        name = artifact.get("name") or "inputs-decision.json"
        target = dest_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.get("content") is not None:
            target.write_text(item["content"])
            written["inputs"].append(name)
        elif item.get("content_omitted_reason"):
            marker = dest_path / f"{name}.omitted"
            marker.write_text(str(item["content_omitted_reason"]))
            written["inputs"].append(f"{name}.omitted")

    (dest_path / "reproduce-manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True))
    written["manifest"] = "reproduce-manifest.json"
    return written


@run_app.command("reproduce")
def run_reproduce(
    run: str = run_ref(),
    export: str = typer.Option(
        None,
        "--export",
        help="write the record as a portable JSON bundle (a rendering, not the source of truth)",
    ),
    materialize: str = typer.Option(
        None,
        "--materialize",
        help="reconstruct a runnable directory: restore the code tree + write inputs and the manifest",
    ),
) -> None:
    """Pull the server-assembled reproduction record for a run.

    One read assembles everything reproduction needs — execution record, launch
    context, a copyable restore command, code snapshot, inputs-decision, notes,
    lockfiles, lineage edges, per-span environments, and a completeness verdict.
    It is assembled by research-os (`GET /v1/runs/{id}/reproduce`), not here: the
    backend is the one place that reads every piece together. A run captured before
    capture-core still answers with an honest degraded record, never an error.

    `--export FILE` writes the record as a portable JSON bundle — a rendering you can
    hand off, never the source of truth (that stays the run). `--materialize DIR`
    goes further: it rebuilds the captured code tree and writes the inputs, leaving a
    directory you can run.
    """
    if export and materialize:
        raise typer.BadParameter("pass --export OR --materialize, not both")
    with _client() as c:
        run_id = _ref(c, "run", run).id
        record = c.run_reproduce(run_id)
        if materialize:
            _print_json(_materialize_record(c, run_id, record, materialize))
            return
    if export:
        Path(export).write_text(json.dumps(record, indent=2, sort_keys=True))
        typer.echo(f"wrote {export}")
    else:
        _print_json(record)


@run_app.command("delete")
def run_delete(
    run: str = run_ref(),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
) -> None:
    """Move a run and its telemetry to the trash (Probe support can restore
    it for 21 days, then it is deleted for good). A server without the trash
    deletes it permanently, and the prompt says so."""
    # No --by-* here: a slug is a server-minted petname, so it cannot be
    # UUID-shaped and cannot collide with an id. See refs.resolve_run.
    _confirmed_delete(
        "run", run, yes=yes, cascade="its spans, metrics and files go too", trash=True
    )


@run_app.command("series")
def run_series(run: str = run_ref()) -> None:
    """Per-series summary for a run (key/kind/dimensions + first/last/min/max)."""
    with _client() as c:
        _print_json(c.run_series(_ref(c, "run", run).id))


@run_app.command("metrics")
def run_metrics(
    run: str = run_ref(),
    key: str = typer.Option(None, "--key"),
    kind: str = typer.Option(None, "--kind"),
    limit: int = typer.Option(None, "--limit"),
) -> None:
    """Raw metric points for a run."""
    with _client() as c:
        points = c.run_metrics(_ref(c, "run", run).id, key=key, kind=kind, limit=limit)
        _print_json([nonfinite_to_wire(point) for point in points])


# -- what a run READ, and what it built on (lineage plan L5) ------------------
@run_app.command("inputs")
def run_inputs(run: str = run_ref()) -> None:
    """The files a run READ, as the SDK recorded them.

    Each read carries its `matches`: the run and file version that wrote the
    same bytes (found by content hash; several when more than one run wrote
    them, none when Probe holds no copy), and whether a person dismissed the
    match (`match_dismissed`) or pinned the version really read
    (`match_version_id`) or the run that wrote it (`match_run_id`).
    `coverage` is what the recorder could see, including
    whether it stopped listing (`truncated`). Fix a wrong match with
    `probe run input dismiss|pin|reset`.
    """
    with _client() as c:
        _print_json(c.run_inputs(_ref(c, "run", run).id))


@run_app.command("upstream")
def run_upstream(
    run: str = run_ref(),
    depth: int = typer.Option(2, "--depth", min=1, max=5, help="how many hops back (1-5)"),
) -> None:
    """What a run built on, `--depth` hops back: its parents (retry, fork,
    resume, branch), runs it built on, and the writer of every file it read,
    then the same for each of those. `truncated` says the walk stopped early."""
    with _client() as c:
        _print_json(c.run_upstream(_ref(c, "run", run).id, depth=depth))


run_input_app = typer.Typer(
    no_args_is_help=True,
    help="correct the run a file this run read was matched to (`probe run inputs` lists them)",
)
run_app.add_typer(run_input_app, name="input")

_INPUT_PATH_HELP = "the read's path, as `probe run inputs` lists it"
_INPUT_HASH_HELP = "only the read of these bytes, when the run read the path more than once"


@run_input_app.command("dismiss")
def run_input_dismiss(
    run: str = run_ref(),
    path: str = typer.Argument(..., help=_INPUT_PATH_HELP),
    content_hash: str = typer.Option(None, "--hash", help=_INPUT_HASH_HELP),
) -> None:
    """Drop a read's match: equal bytes, but not what this run built on."""
    _correct_input(run, path, content_hash=content_hash, dismissed=True)


@run_input_app.command("pin")
def run_input_pin(
    run: str = run_ref(),
    path: str = typer.Argument(..., help=_INPUT_PATH_HELP),
    version: str = typer.Option(
        None, "--version", help="the id of the file version really read (`probe artifact versions`)"
    ),
    writer: str = typer.Option(
        None,
        "--writer",
        help="the run that wrote the file (id or slug) -- for a file it only recorded writing, "
        "which has no stored version",
    ),
    content_hash: str = typer.Option(None, "--hash", help=_INPUT_HASH_HELP),
) -> None:
    """Name what a read really was, instead of the derived match: the file
    version (`--version`) or the run that wrote it (`--writer`). One of the
    two; a pin replaces the one before (`reset` undoes it)."""
    if (version is None) == (writer is None):
        raise typer.BadParameter("give --version or --writer (one of the two)")
    _correct_input(run, path, content_hash=content_hash, version_id=version, writer=writer)


@run_input_app.command("reset")
def run_input_reset(
    run: str = run_ref(),
    path: str = typer.Argument(..., help=_INPUT_PATH_HELP),
    content_hash: str = typer.Option(None, "--hash", help=_INPUT_HASH_HELP),
) -> None:
    """Hand a read back to automatic matching (undoes a dismiss or a pin)."""
    _correct_input(run, path, content_hash=content_hash, dismissed=False)


def _correct_input(run: str, path: str, *, writer: str | None = None, **correction: Any) -> None:
    """One read's correction (`PATCH /v1/runs/{id}/inputs`, 204): prints what
    was set, or what happened to a write that could not be delivered.
    ``writer`` (a run ref) is resolved to the id the server pins."""
    with _client() as c:
        run_id = _ref(c, "run", run).id
        if writer is not None:
            correction["writer_run_id"] = _ref(c, "run", writer).id
        c.correct_run_input(run_id, path, **correction)
    done = {"run_id": run_id, "path": path, **{k: v for k, v in correction.items() if v is not None}}
    # Not delivered (queued, or lost with the outbox): print THAT, never the
    # correction as if it were made.
    _print_json(None if _UNDELIVERED.total else done)


# -- exec (process correlation) ---------------------------------------------
_RAW_ARGS = "probe.raw_args"


class _RawArgsCommand(typer.core.TyperCommand):
    """Keeps the args click was handed, before parsing.

    `probe exec -- python train.py` and `probe exec RUN -- python train.py` parse
    alike: click consumes the `--` and binds the first token after it to the
    optional RUN, so the first reads as "wrap run `python`". Only the raw args
    say which side of the `--` the positional came from.
    """

    def parse_args(self, ctx, args):  # type: ignore[override]
        ctx.meta[_RAW_ARGS] = list(args)
        return super().parse_args(ctx, args)


def _positional_after_separator(raw: object, run: str, rest: list[str]) -> bool:
    """Whether click bound RUN from the first token AFTER `--` (so it is the
    command, not a run ref). After it, click leaves every later token in `rest`;
    before it, the whole command after `--` is still in `rest`."""
    if not isinstance(raw, list) or "--" not in raw:
        return False
    at = raw.index("--")
    return raw[at + 1 : at + 2] == [run] and list(rest) == raw[at + 2 :]


@app.command(
    cls=_RawArgsCommand,
    context_settings={"allow_extra_args": True, "ignore_unknown_options": True},
    help="run a command under a run: probe exec [--project P] -- cmd ... (or: probe exec RUN -- cmd ...)",
)
def exec(
    ctx: typer.Context,
    run: str = typer.Argument(None, help="an EXISTING run ref; omit to open one here"),
    cwd: str = typer.Option(None, "--cwd"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="slug of an EXISTING experiment"),
    slug: str = typer.Option(None, "--slug", help="this run's slug; omit for a petname"),
    name: str = typer.Option(None, "--name"),
    description: str = typer.Option(None, "--description"),
    tag: list[str] = typer.Option(None, "--tag"),
    external_id: str = typer.Option(None, "--external-id"),
    config: list[str] = typer.Option(None, "--config", metavar="k=v"),
    parent: str = typer.Option(
        None, "--parent", help="the run this one re-attempts or branches from (id or petname)"
    ),
    relation: Relation = typer.Option(
        None, "--relation", help="retry|resume|fork|branch; required with --parent"
    ),
    intent: str = typer.Option(
        None, "--intent", help="what this run is meant to show (free text, kept in its metadata)"
    ),
    authored_by: AuthoredBy = authored_by_opt(),
    launcher: str = typer.Option(
        None,
        "--launcher",
        help="override launcher detection: modal|ray|sbatch|kubectl for submit-and-return",
    ),
    detached_launcher: bool = typer.Option(
        False,
        "--detached-launcher",
        help="this command SUBMITS and returns; do not treat its exit code as the job's",
    ),
    outputs: str = typer.Option(
        None,
        "--outputs",
        help="the folder whose new/changed files are captured at exit (default: --cwd or the current folder; a relative path is taken from --cwd)",
    ),
    no_capture_outputs: bool = typer.Option(
        False,
        "--no-capture-outputs",
        help="do not capture the command's output files or its printed log (also PROBE_CAPTURE_OUTPUTS=0)",
    ),
) -> None:
    """Execute a command under a run, and OWN that run while it executes.

    This is the honest wrapper. It opens the run (or takes one you already
    opened), beats for as long as the child lives, hands the child
    ``PROBE_RUN_ID`` + ``PROBE_RUN_EPOCH`` so ``probe.init()`` inside it joins
    the SAME run, and closes the run from the child's real exit code.

    BLOCKING vs SUBMIT is the distinction that matters. `python train.py` and
    `modal run` block until the work finishes, so this process's lifetime is the
    run's and its exit code is the job's. `sbatch`, `ray job submit` and `modal
    deploy` return the moment a scheduler accepts the job -- wrapping one of
    those would mark the run completed, exit 0, while the work had not started.
    For those the run is opened AWAITING ATTACH: it lands 'created', owned by
    nobody, and the job's own `probe.init()` becomes its owner when it starts.
    Detection unwraps `python -m` / `uv run` / `uvx`; `--launcher` overrides it
    and `--detached-launcher` covers anything unrecognised.

    CAPTURE: everything the command prints is teed to your terminal and saved
    as the run's `probe/run.log`, and the files it creates or changes in its
    folder (`--outputs`, else `--cwd`, else here) are captured as `outputs/...`
    when it exits -- uploaded up to 64 MB; bigger ones recorded where they live
    on storage that lasts, or listed in `probe/outputs-manifest.json` on a
    throwaway machine. `--no-capture-outputs` turns both off. A submit-and-return
    launcher captures nothing: the job's own `probe.init()` does.

    With no run, no --project/--experiment and no active project, the run opens
    FLOATING (daemon v2): no home yet; the Probe daemon files it, or `probe run
    move` does.
    """
    argv = list(ctx.args)
    if argv and argv[0] == "--":
        argv = argv[1:]
    raw_args = (getattr(ctx, "meta", None) or {}).get(_RAW_ARGS)
    if isinstance(run, str) and _positional_after_separator(raw_args, run, argv):
        # `probe exec -- python train.py`: "python" is the command, not a run.
        argv = [run, *argv]
        run = None
    # Click consumes the `--` separator and then binds the first remaining token
    # to the optional positional, so `probe exec --project p -- python train.py`
    # arrives with run="python" and argv=["train.py"]. Creation flags are the
    # unambiguous signal that the caller is OPENING a run here rather than
    # naming one, so the positional is the start of their command -- put it back.
    # isinstance, not `is not None`: called directly as a Python function (the
    # version-notice tests do) the typer defaults are OptionInfo objects rather
    # than None, and every flag would read as supplied.
    opening_here = any(
        isinstance(v, str) and v
        for v in (project, experiment, slug, name, description, external_id, intent)
    ) or any(isinstance(v, list) and v for v in (tag, config))
    if run is not None and opening_here:
        argv = [run, *argv]
        run = None
    if not argv:
        raise typer.BadParameter("probe exec requires a command after --")

    # Same OptionInfo caution as above: `is True` / isinstance, never truthiness.
    hands_off = detached_launcher is True or (
        launcher.lower() in _LAUNCHER_ALIASES
        if isinstance(launcher, str) and launcher
        else _is_submit_launcher(argv)
    )

    from . import run_lock

    # ONE client, ONE handle, held for the child's whole life. Opening the run
    # through a first client and then re-attaching through a second took the
    # process-bound flock TWICE: `c.run(heartbeat=True)` claims it via
    # _hold_run_lock, Client.close() does not release it (only a terminal
    # set_status does), and flock refuses a second fd in the same process -- so
    # both the explicit acquire and attach's own claim failed silently and
    # `probe exec` ran with no auto-update protection at all, which is the one
    # thing the flock tier exists for.
    #
    # `raise_permanent=False`: this process carries the wrapped job's run --
    # its beats, its console log, its captured outputs -- through the SDK, which
    # must never raise into the job over one refused write (`Client.write`),
    # nor report each failed one on stderr or in its exit code (`_new_client`).
    # Every other verb is a single write a refusal should fail (L14).
    with _client(raise_permanent=False) as c:
        claim = None
        if run is None:
            # An active project (`probe project use`) still wins; with none and
            # no --project/--experiment the run opens FLOATING (daemon v2).
            resolved_project = _ambient_project(project if isinstance(project, str) else None)
            # Parentage is a pair. One half alone is either a relation with no
            # parent to mean it, or a parent with a guessed relation -- and the
            # server stores whatever word arrives as a claim someone reads later.
            if (parent is None) != (relation is None):
                raise typer.BadParameter("--parent and --relation go together")
            # The parent's UUID, not the ref typed: `parent_run_id` is a UUID
            # field, and a petname reaching the server as one is rejected.
            parent_id = _ref(c, "run", parent).row["id"] if parent else None
            # The command rides the run's "run started" message to the daemon,
            # and names the launch the retry detector compares (L6).
            from ..sdk import launch as _launch

            with daemon_channel.launch_command(argv), _launch.launching(
                argv, cwd if isinstance(cwd, str) else None
            ):
                handle = c.run(
                    experiment=experiment if isinstance(experiment, str) else None,
                    project=_project_slug(c, resolved_project) if resolved_project else None,
                    name=name if isinstance(name, str) else None,
                    slug=slug if isinstance(slug, str) else None,
                    description=description if isinstance(description, str) else None,
                    tags=list(tag) if isinstance(tag, list) and tag else None,
                    external_id=external_id if isinstance(external_id, str) else None,
                    config=_kv_pairs(config) if isinstance(config, list) and config else None,
                    intent=intent if isinstance(intent, str) else None,
                    parent_run_id=parent_id,
                    parent_relation=relation.value if relation else None,
                    # A hand-off opens the row for a job that has not started; a
                    # blocking wrap opens it owned, beating from this process.
                    awaiting_attach=hands_off,
                    heartbeat=not hands_off,
                    # `run start`'s own deprecation notice sends people here, so the
                    # command the CLI steers to must be able to say a PERSON wrote
                    # the name. Without it a researcher's own title, typed through
                    # an agent, is stamped `agent` with no override -- on the one
                    # verb they are being told to use.
                    authored_by=_authored_by_value(authored_by),
                    # The server cannot see the difference between a launcher and
                    # the work itself; this is the signal that makes "held open but
                    # nothing inside ever reported" expressible.
                    launcher=True,
                    # This process is the launcher, not the work: it must not tee
                    # or sweep ITSELF. `execute` below captures the child.
                    capture_outputs=False,
                )
            _print_link("run", handle.id)
            # A beating handle already holds the flock; a hand-off holds nothing
            # on purpose. Either way there is no second claim to take.
        else:
            # Wrapping a run someone else opened: this process still owns the
            # child, so it takes the flock tier explicitly.
            claim = None if hands_off else run_lock.acquire(run)
            handle = _run_handle(c, run, owns_process=not hands_off)
        try:
            if hands_off:
                hint = _forwarding_hint(argv, handle.id, handle.write_epoch)
                # The agent session too (audit E2), so the job's runs carry the
                # session tag the Probe daemon finds them by.
                session_lines = "".join(
                    f"\n         {key}={value}"
                    for key, value in agent_session.forwarding_env().items()
                )
                typer.echo(
                    f"probe: run {handle.slug or handle.id} is awaiting attach.\n"
                    f"       forward these into the job or it reports nothing:\n"
                    f"         PROBE_RUN_ID={handle.id}\n"
                    f"         PROBE_RUN_EPOCH={handle.write_epoch}"
                    + session_lines
                    + (f"\n       {hint}" if hint else ""),
                    err=True,
                )
            # finalize=False for a hand-off: this process's exit code belongs to
            # the SUBMITTER, and recording it as the run's is the precise lie
            # this branch exists to avoid.
            result = handle.execute(
                argv,
                cwd=cwd,
                finalize=not hands_off,
                outputs=outputs if isinstance(outputs, str) and outputs else None,
                capture_outputs=False if no_capture_outputs is True else None,
            )
        finally:
            if claim is not None:
                claim.release()
            # The wrapped process is gone and our claim with it. `_version_notice`
            # refused an upgrade at the START of this command (`exec` is on the
            # denylist, correctly), and this is the moment that refusal stops
            # being permanent.
            #
            # Inside the `finally` on purpose: it must run whether the child
            # succeeded, failed, or was Ctrl-C'd, since the run is over either
            # way. That is also why _apply_deferred_update swallows everything --
            # a raise here would replace the propagating exception and corrupt
            # the exit code this command exists to hand back.
            _apply_deferred_update()
    # A child killed by signal N comes back as -N; handed to exit() as is, the
    # OS keeps its low byte (SIGTERM -15 -> 241). Report it the way a shell
    # does, 128+N, so `probe exec` is transparent to whatever reads the code.
    code = result.returncode
    raise typer.Exit(128 - code if code < 0 else code)


@app.command()
def log(
    run: str = typer.Argument(...),
    metric: list[str] = typer.Argument(..., metavar="key=value..."),
    write_mode: Optional[bool] = write_mode_opt(),
    step: int = typer.Option(None, "--step"),
    kind: str = typer.Option("model", "--kind"),
    dim: list[str] = typer.Option(
        None,
        "--dim",
        metavar="k=v",
        help="LOW-CARDINALITY grouping axis (split/seed/rank). Never an id — each "
        "distinct value is its own one-point series, i.e. a tile, not a graph",
    ),
    agg: Agg = typer.Option(
        None, "--agg", help="declare the key's reduce fn for grouped reads (0062)"
    ),
    derived: bool = typer.Option(
        False,
        "--derived",
        help="these values were COMPUTED after the fact, not measured live; needs --producer",
    ),
    producer: str = typer.Option(
        None, "--producer", help="what computed them, e.g. claude-code or score_auc.py"
    ),
    note: str = typer.Option(None, "--note", help="why/how, free text"),
    input_key: list[str] = typer.Option(
        None, "--input", metavar="KEY", help="repeatable; stored series the computation read"
    ),
    code_ref: str = typer.Option(None, "--code-ref", help="repo path / commit / script"),
) -> None:
    """Append metric points. --dim adds series dimensions (fold #9).

    Shape first: a series is (run, kind, key, dims), so every distinct --dim
    combination is a SEPARATE series, and a one-point series renders as a scalar
    tile, not a graph. Only --step makes a curve; spreading values across a
    dimension does not. Budget series ≈ the product of your --dim cardinalities
    and keep it under ~50. This fails SILENTLY — every call succeeds and the
    values are right; the only symptom is an unreadable run page — so check with
    `probe metrics grouped` / the run's series list rather than assuming.

    Per-sample identity (example_id, row id, uuid, filename) has NO door here:
    the SDK puts it in `labels`, and this command has no --label. Log per-item
    detail as an artifact (`probe artifact add`) and leave metrics for the
    handful of numbers a human should see.

    --derived marks the batch as computed rather than measured — the door for
    backfilling a metric onto a run that has already finished. It requires
    --producer and a --step, and records provenance beside the points so a
    reader can always tell a computed curve from a captured one.
    """
    metrics = _kv_pairs(metric, cast_float=True)
    dims = _kv_pairs(dim) if dim else None

    if producer and not derived:
        raise typer.BadParameter("--producer only applies to --derived")
    if derived:
        if not producer:
            raise typer.BadParameter(
                "--derived needs --producer: a computed series without provenance is "
                "indistinguishable from a logged one"
            )
        if step is None:
            raise typer.BadParameter(
                "--derived needs an explicit --step: a backfill lands on steps that "
                "already exist, so there is no counter to auto-increment"
            )
        # Deliberately synchronous: the async outbox carries `log` bodies, and a
        # derived batch is a different shape. A backfill is not on the hot path.
        with _client() as c:
            _run_handle(c, run).log_derived(
                metrics,
                step=step,
                producer=producer,
                note=note,
                # `if input_key` and not `list(...) or None`: typer hands back
                # None, not (), for a repeatable option nobody passed, so the
                # bare list() raised TypeError on every --derived write without
                # --input. The one test covering this path always passed --input.
                inputs=list(input_key) if input_key else None,
                code_ref=code_ref,
                kind=kind,
                dimensions=dims,
                agg=agg.value if agg else None,
            )
        print(f"logged {len(metrics)} derived metric(s) to {run} (producer={producer})")
        return

    _check_ref_shape(run)
    with _default_client(_resolve_write_mode(write_mode)) as c:
        if c.async_writes:
            # `_async_run`, not `_run_handle`: the sync path reads the run first
            # (a GET per write), which is the round trip queueing exists to
            # avoid. The server validates the ref at replay.
            dropped_before = c.dropped_writes
            direct_before = c.direct_sends
            _async_run(c, run).log(
                metrics,
                step=step,
                kind=kind,
                dimensions=dims,
                agg=agg.value if agg else None,
            )
            _fail_if_dropped(c, dropped_before, f"{len(metrics)} metric(s) for {run}")
            if c.direct_sends > direct_before:
                # Below the outbox's free-space floor it went straight to the
                # server instead (plan 1.5): say what happened.
                print(f"logged {len(metrics)} metric(s) to {run} (sent: outbox low on disk)")
                return
            _kick_drainer()
            print(f"logged {len(metrics)} metric(s) to {run} (queued)")
            return
        _run_handle(c, run).log(
            metrics, step=step, kind=kind, dimensions=dims, agg=agg.value if agg else None
        )
        # A sync write the server did not answer is queued (L14): say so, not
        # "delivered" -- the word a script trusts.
        word = _UNDELIVERED.word()
    # The delivery word is ALWAYS present, in both branches. Whether a write
    # queued or landed now depends on credentials, PROBE_ASYNC and a flag that
    # may be on either side of the subcommand -- none of which the caller can see
    # from the outside. A stable `(queued|delivered)` suffix is what lets a
    # script decide deterministically instead of inferring from three shapes.
    print(f"logged {len(metrics)} metric(s) to {run} ({word})")


# -- coordinate reads (below-run coordinates, research-os 0059-0062) ---------
metrics_app = typer.Typer(no_args_is_help=True, help="coordinate-aware metric reads")
app.add_typer(metrics_app, name="metrics")


@metrics_app.command("grouped")
def metrics_grouped(
    run: str = run_ref(),
    key: str = typer.Option(..., "--key"),
    kind: str = typer.Option(None, "--kind"),
    agg: Agg = typer.Option(
        None, "--agg", help="omit for the key's declared reduce fn (else mean)"
    ),
    by: list[str] = typer.Option(
        None, "--by", help="repeatable; one cell per combination of these coordinate axes"
    ),
    where: str = typer.Option(
        None, "--where", metavar="JSON", help='coord filter, e.g. \'{"split": "train"}\''
    ),
    step_bucket: int = typer.Option(None, "--step-bucket"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_rows: int = typer.Option(None, "--max-rows"),
) -> None:
    """Server-side reduce/group over one metric's stepped points (paging followed)."""
    with _client() as c:
        _print_json(
            c.get_metrics_grouped(
                run,
                key,
                kind=kind,
                agg=agg.value if agg else None,
                by=by or None,
                where=_json_value(where),
                step_bucket=step_bucket,
                step_from=step_from,
                step_to=step_to,
                max_rows=max_rows,
            )
        )


@metrics_app.command("wide")
def metrics_wide(
    run: str = run_ref(),
    key: list[str] = typer.Option(None, "--key", help="repeatable; narrow to these keys"),
    kind: str = typer.Option(None, "--kind"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_rows: int = typer.Option(None, "--max-rows"),
) -> None:
    """Step x metric table for a run (the DataFrame pivot; paging followed)."""
    with _client() as c:
        _print_json(
            c.get_metrics_wide(
                run,
                key=key or None,
                kind=kind,
                step_from=step_from,
                step_to=step_to,
                max_rows=max_rows,
            )
        )


@metrics_app.command("export")
def metrics_export(
    run: str = run_ref(),
    key: str = typer.Option(None, "--key"),
    kind: str = typer.Option(None, "--kind"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    limit: int = typer.Option(None, "--limit", help="page size of the keyset walk"),
) -> None:
    """Lossless raw-point export, one JSON point per line.

    NDJSON rather than one array on purpose: the export is the unbounded read,
    and a stream that prints as it pages can be piped without buffering the run.
    """
    with _client() as c:
        for point in c.export_metric_points(
            run, key=key, kind=kind, step_from=step_from, step_to=step_to, limit=limit
        ):
            print(json.dumps(nonfinite_to_wire(point), default=str))


@metrics_app.command("plot")
def metrics_plot(
    run: str = run_ref(),
    key: list[str] = typer.Option(
        None, "--key", help="repeatable; a panel per matching series. Omit for the whole board"
    ),
    kind: str = typer.Option(None, "--kind"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_rows: int = typer.Option(None, "--max-rows"),
    overlay: bool = typer.Option(
        False, "--overlay", help="draw the --keys together on one shared y-axis"
    ),
    width: int = typer.Option(None, "--width", help="plot width in cells (default: the terminal)"),
    height: int = typer.Option(12, "--height", help="plot height in cells"),
    no_color: bool = typer.Option(False, "--no-color", help="never emit ANSI color"),
    plain: bool = typer.Option(False, "--ascii", help="ASCII only: no braille, no box drawing"),
) -> None:
    """Draw a run's curves in this terminal, off the same read `metrics wide` does.

    Bare, it prints the BOARD: every series the run logged, one sparkline each,
    with last/min/max beside it -- the overview you want before choosing what to
    look at. `--key` promotes those series to full panels with axes and ticks.

    `--overlay` puts several keys on ONE canvas, which means one y-axis: curves
    on different scales are still drawn truthfully, but the smaller one flattens
    against the floor, and you are told when that has happened. Two metrics that
    do not share a scale are better read as the two panels you get by default.

    Unlike its siblings here this takes any run ref (a slug as well
    as a uuid) -- it is the verb a human types, not one a script pipes.
    """
    from . import charts

    if overlay and not key:
        raise typer.BadParameter("--overlay needs the --key series it should overlay")
    with _client() as c:
        table = c.get_metrics_wide(
            _ref(c, "run", run).id,
            key=key or None,
            kind=kind,
            step_from=step_from,
            step_to=step_to,
            max_rows=max_rows,
        )
    series = charts.series_from_wide(table)
    # Everything the picture cannot show goes to stderr before it is drawn. A
    # chart is read as the whole truth about a run, so a window that was cut
    # short, a key that matched nothing, or a NaN that could not be given a row
    # has to be said in words -- none of them has a shape on the canvas.
    if table.get("truncated"):
        typer.echo(
            f"PARTIAL: the read stopped at step {table.get('next_step')} -- this is not the "
            "whole curve. Narrow with --step-from/--step-to, or raise --max-rows",
            err=True,
        )
    if key:
        missing = [k for k in key if k not in {c.get("key") for c in table.get("columns") or []}]
        if missing:
            typer.echo(f"no series for: {', '.join(missing)}", err=True)
    nonfinite = [s for s in series if s.dropped]
    if nonfinite:
        typer.echo(
            "non-finite points (NaN/inf) cannot be plotted and are not drawn: "
            + ", ".join(f"{s.label} ({s.dropped})" for s in nonfinite),
            err=True,
        )
    series = [s for s in series if s.points]
    if not series:
        typer.echo(
            "no plottable metric points in that window"
            + (f" for {', '.join(key)}" if key else "")
            + " -- `probe run series RUN` lists what the run logged",
            err=True,
        )
        return
    shape = {
        "width": width,
        "color": False if no_color else None,
        "unicode": False if plain else None,
    }
    if not key:
        print(charts.board(series, **shape))
        return
    if overlay:
        kept, dropped = series[: charts.MAX_OVERLAY], series[charts.MAX_OVERLAY :]
        if dropped:
            # Never silently: a chart that shows six of nine series and says so
            # is a partial read; one that shows six and does not is a wrong one.
            typer.echo(
                f"overlaying the first {charts.MAX_OVERLAY}, dropped: "
                + ", ".join(s.label for s in dropped),
                err=True,
            )
        print(
            charts.panel(
                kept,
                title=" + ".join(s.label for s in kept),
                footer=charts.overlay_footer(kept, unicode=shape["unicode"]),
                height=height,
                **shape,
            )
        )
        return
    for index, item in enumerate(series):
        if index:
            print()
        print(
            charts.panel(
                [item],
                title=item.label,
                footer=charts.summarize(item, unicode=shape["unicode"]),
                height=height,
                **shape,
            )
        )


def _derived_series_points(source: str) -> list[tuple[int, float]]:
    """Read a (step, value) series from a file or stdin.

    Three spellings, because three things produce these and none of them should
    have to reshape for the others:

      JSONL   {"step": 0, "value": 1.2}          one object per line
              [0, 1.2]                            or one pair per line
      JSON    [{"step": 0, "value": 1.2}, ...]   a whole document
              {"0": 1.2, "1": 0.9}                a step -> value map

    Detected by trying the whole document as JSON first and falling back to
    line-by-line, so a single-line JSON array is not mistaken for JSONL.
    """
    text = sys.stdin.read() if source == "-" else Path(source).read_text()

    def pair(item: Any, where: str) -> tuple[int, float]:
        if isinstance(item, dict):
            if "step" not in item or "value" not in item:
                raise typer.BadParameter(f'{where}: needs "step" and "value"')
            step, value = item["step"], item["value"]
        elif isinstance(item, (list, tuple)):
            if len(item) != 2:
                raise typer.BadParameter(f"{where}: a pair is [step, value]")
            step, value = item
        else:
            raise typer.BadParameter(f"{where}: expected an object or a [step, value] pair")
        try:
            return int(step), float(value)
        except (TypeError, ValueError) as exc:
            raise typer.BadParameter(f"{where}: {exc}") from exc

    try:
        document = json.loads(text)
    except json.JSONDecodeError:
        document = None
    if document is not None:
        if isinstance(document, dict):
            # A one-row JSONL file parses as a whole JSON document too, so the
            # point spelling has to be recognised BEFORE the map spelling --
            # otherwise a single {"step": 0, "value": 1.2} is read as a map with
            # the steps "step" and "value" and dies converting them.
            if "step" in document and "value" in document:
                return [pair(document, "the point")]
            # A step -> value map, sorted numerically rather than lexically: JSON
            # object keys are strings, so insertion order puts step 10 before
            # step 2 and the curve reads as written out of order.
            return sorted(pair([step, value], f"step {step!r}") for step, value in document.items())
        if isinstance(document, list):
            return [pair(item, f"item {i}") for i, item in enumerate(document)]
        raise typer.BadParameter("expected a JSON array, a step->value object, or JSONL")

    points: list[tuple[int, float]] = []
    for lineno, raw in enumerate(text.splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        try:
            item = json.loads(line)
        except json.JSONDecodeError as exc:
            raise typer.BadParameter(f"line {lineno}: not JSON: {exc}") from exc
        points.append(pair(item, f"line {lineno}"))
    return points


@metrics_app.command("backfill")
def metrics_backfill(
    run: str = typer.Argument(...),
    key: str = typer.Option(..., "--key", help="the series to write"),
    producer: str = typer.Option(
        ..., "--producer", help="what computed it, e.g. claude-code or score_auc.py"
    ),
    series: str = typer.Option(
        "-",
        "--from",
        metavar="FILE",
        help="JSONL or JSON step/value series; '-' (the default) reads stdin",
    ),
    kind: str = typer.Option("model", "--kind"),
    dim: list[str] = typer.Option(None, "--dim", metavar="k=v"),
    agg: Agg = typer.Option(None, "--agg"),
    note: str = typer.Option(None, "--note", help="why/how, free text"),
    input_key: list[str] = typer.Option(
        None, "--input", metavar="KEY", help="repeatable; stored series the computation read"
    ),
    code_ref: str = typer.Option(None, "--code-ref", help="repo path / commit / script"),
) -> None:
    """Write a whole DERIVED curve in ONE request.

    The batch door beside `probe log --derived`, which takes one step per
    invocation on purpose — the async outbox carries `log` bodies and a derived
    batch is a different shape, so it stayed synchronous and single-step. That is
    fine for a correction and wrong for a backfill: a 20k-step curve through it is
    20k round trips. This is the same provenance, the same series identity, one
    request.

    The series comes from --from FILE or stdin, as JSONL objects
    ({"step": 0, "value": 1.2}), JSONL [step, value] pairs, a JSON array of
    either, or a JSON {step: value} object:

        probe metrics backfill RUN --key eval/auroc --producer score_auc.py \\
            --from curve.jsonl

    Provenance is not optional here for the same reason it is not on --derived:
    a computed series without it is indistinguishable from a measured one.
    """
    points = _derived_series_points(series)
    if not points:
        raise typer.BadParameter(f"no points in {'stdin' if series == '-' else series}")
    dims = _kv_pairs(dim) if dim else None
    with _client() as c:
        _run_handle(c, run).log_derived_series(
            key,
            points,
            producer=producer,
            note=note,
            inputs=list(input_key) if input_key else None,
            code_ref=code_ref,
            kind=kind,
            dimensions=dims,
            agg=agg.value if agg else None,
        )
    steps = f"steps {points[0][0]}..{points[-1][0]}" if len(points) > 1 else f"step {points[0][0]}"
    print(
        f"backfilled {len(points)} derived point(s) of {kind}/{key} to {run} "
        f"({steps}, producer={producer}, 1 request)"
    )


@metrics_app.command("delete")
def metrics_delete(
    run: str = run_ref(),
    key: str = typer.Option(..., "--key"),
    kind: str = typer.Option("model", "--kind"),
    dim: list[str] = typer.Option(None, "--dim", metavar="k=v", help="pin ONE dimension variant"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation"),
) -> None:
    """Delete a DERIVED series and its points.

    The undo for a computed metric that was wrong. Derived only — a logged
    series is the run's captured record and the server refuses (409).

    Omitting --dim addresses the dimension-less series, NOT every variant of the
    key: a key logged per-rank needs the pin.
    """
    dims = _kv_pairs(dim) if dim else None
    label = f"{kind}/{key}" + (f" {dims}" if dims else "")
    _confirm_delete(yes, f"derived series {label} on run {run}")
    with _client() as c:
        c.delete_series(run, key=key, kind=kind, dimensions=dims)
    print(f"deleted derived series {label}")


@app.command()
def coordinates(run: str = run_ref()) -> None:
    """The run's coordinate catalog: every coordinate any fact landed on."""
    with _client() as c:
        _print_json(c.list_run_coordinates(run))


# -- expression views (read-time computed panels, research-os 0088) ---------
# The AUTHORING surface. The dashboard renders, renames and deletes views but
# never composes one: an expression comes from a researcher's agent session or
# their own script, so the door it comes through is here and the SDK's
# `probe.expr`. --spec-file is literally that path — a script writes JSON, this
# uploads it.
# -- statusline -------------------------------------------------------------
# The coding-agent status line is ONE global slot in the agent's settings, with
# no plugin manifest field for it, so getting our segment there means editing a
# file we do not own. That makes it an explicit, reversible command rather than
# something the wizard does silently -- see probe.cli.statusline.
statusline_app = typer.Typer(
    no_args_is_help=True, help="the tracked/untracked segment in Claude Code's status line"
)
app.add_typer(statusline_app, name="statusline")


@statusline_app.command("install")
def statusline_install(
    plugin_root: str = typer.Option(
        None, "--plugin-root", help="the probe-research plugin directory (auto-detected)"
    ),
) -> None:
    """Add the Probe segment to Claude Code's status line, keeping what is there.

    Chains after any existing command rather than replacing it, and feeds both
    sides the status-line payload -- see the module docstring for why a plain
    `a; b` chain silently starves the second command of stdin.
    """
    # Codex HAS a status line, but it is a PICKER over built-in items
    # (`/statusline` — "Select which items to display"; `tui.status_line` is a
    # sequence, and an unrecognised entry is ignored rather than executed). There
    # is no command hook, so no segment can render there — the same information
    # goes out as an on-change NOTICE instead. Turning that on is what `install`
    # means under Codex, so one command does the right thing per agent.
    #
    # Both surfaces, never a refusal: someone may perfectly well be configuring
    # Claude Code from a Codex shell, and picking one on ambient environment
    # would break that. So Codex ADDS the notice rather than replacing the
    # install, and the reply says plainly which surface got what.
    detected = agent_session.detect_agent()
    under_codex = detected is not None and detected.label == "codex"
    notice = str(statusline.enable_notice()) if under_codex else None
    if under_codex:
        print(
            "note: Codex's status line selects from built-in items and cannot run a "
            "command, so this enabled the on-change notice there and configured the "
            "segment for Claude Code.",
            file=sys.stderr,
        )

    root = Path(plugin_root) if plugin_root else statusline.discover_plugin_root()
    if root is None:
        print(
            "could not find the probe-research plugin — install it with "
            "`/plugin install probe-research@research-os-agent`, or pass --plugin-root",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    _print_json({**statusline.install(root), "notice": notice})


@statusline_app.command("uninstall")
def statusline_uninstall() -> None:
    """Remove the Probe segment and the on-change notice, restoring what was wrapped."""
    _print_json({**statusline.uninstall(), "notice_disabled": statusline.disable_notice()})


@statusline_app.command("status")
def statusline_status() -> None:
    """Whether the segment is installed, and what else shares the slot."""
    _print_json({**statusline.status(), "notice_enabled": statusline.notice_enabled()})


@statusline_app.command("show")
def statusline_show(
    session: str = typer.Option(
        None, "--session", help="session id (defaults to this shell's coding-agent session)"
    ),
) -> None:
    """Print the segment this session would render right now.

    The debugging door: it answers "why is it saying untracked" without making
    anyone re-render a status line, and it reads the same marker file the
    renderer does rather than a second code path that could disagree.
    """
    session_id = session or os.environ.get("CLAUDE_CODE_SESSION_ID") or ""
    if not session_id:
        print("no session id: pass --session, or run inside a coding agent", file=sys.stderr)
        raise typer.Exit(1)
    state = session_marker.read(session_id)
    settings = resolve()
    signal = session_marker.tracking_signal(session_id)
    if signal is not None:
        # The session signal is the live state. Do not walk folder defaults
        # after it exists: config changes apply only to new sessions.
        tracking = session_marker.is_tracking(signal)
    else:
        # This is a shell debugging command, not a host hook with a payload, so
        # the process cwd is the best and only cwd it owns.
        tracking, _source = session_marker.resolve_tracking_default(None)
    print(
        session_marker.render(
            state,
            configured=bool(settings.token or settings.mcp_token),
            tracking=tracking,
            live=tracking and session_marker.is_live(state),
        )
    )
    _print_json(
        {
            "session_id": session_id,
            "marker": str(session_marker.marker_path(session_id)),
            "state": state,
        }
    )


# -- session ----------------------------------------------------------------
# The coding-agent conversation, not a Probe run. `untrack` is the off switch
# the track-work skill's explicit `off` drives: a DECLARATION that this conversation
# is not research, which the status line, the refresh hook and the change notice
# all read. Per session, never machine-wide -- a mute button that silenced the
# next conversation too is exactly the surprise nobody wants from one.
session_app = typer.Typer(
    no_args_is_help=True, help="this coding-agent session: is its work being tracked"
)
app.add_typer(session_app, name="session")


def _resolve_agent_session(session: str | None) -> str:
    """This session's id for `probe session ...`, or exit 1 saying so.

    Resolves through the ``AGENTS`` table rather than naming variables here.
    The hardcoded ``CLAUDE_CODE_SESSION_ID or CODEX_THREAD_ID`` this replaces
    is why every `probe session` subcommand exited 1 under pi even though
    ``PI_SESSION_ID`` was in that table: an agent added to the table did not
    become an agent the switch could name. Cursor was in the same position.
    """
    resolved = session or agent_session.session_id_from_env()
    if not resolved:
        print(
            "no session id: pass --session, or run inside a coding agent",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    return resolved


def _require_tracking_state(session_id: str, on: bool) -> None:
    """Fail unless the signal on disk matches the requested state.

    The setter deliberately returns False instead of raising for both invalid
    ids and filesystem failures. A host switch only has an exit code, so
    success must mean the authoritative read-back agrees -- otherwise Pi can
    announce that an opt-out landed while the old value is still active.
    """
    expected = "on" if on else "off"
    if session_marker.tracking_signal(session_id) == expected:
        return
    print(
        f"could not set tracking {expected} for session {session_id}",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _require_state(session_id: str, state: str) -> None:
    """Fail unless the canonical file on disk now reads `state`.

    Same contract as `_require_tracking_state`: the setter returns False rather
    than raising, a host switch only has an exit code, so success must mean the
    authoritative read-back agrees. Announcing that an opt-out landed while the
    old value is still active is the one failure this must never produce.
    """
    if session_marker.session_state(session_id) == state:
        return
    print(
        f"could not set probe state {state} for session {session_id}",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _state_word(state: "str | None") -> "str | None":
    """A state as the WORD this version prints, with None preserved as null.

    Every JSON surface goes through here rather than printing the stored value:
    the config file and the session marker keep the longer `full`/`read-only`
    spellings for the older copies of this client that read them (see
    `session_marker.STATE_LABELS`), and a person reading `probe session status`
    should not have to know that. Readers of this output take both spellings --
    ours here, and pi's `parseState`.
    """
    return None if state is None else session_marker.state_label(state)


def _state_display(session_id: str, state: "str | None") -> "str | None":
    """The state as a PERSON reads it: `on (daemon)` / `read only (daemon)` /
    `off` where the Probe daemon records and reads, else the JSON word. Beside
    `state`, never instead of it -- pi and older hooks parse `state`."""
    if state is None:
        return None
    from probe.cli.daemon_cli import calling_agent

    return session_marker.state_display(
        state, session_marker.daemon_session(session_id, calling_agent())
    )


def _switch_word(session_id: str, value: str) -> str:
    """A typed switch word to the state it STORES, or exit.

    `on` is stored by who records (`session_marker.on_state`). `daemon` is not a
    position of the switch (Richard 2026-09-29): refused with where it is set,
    exit 2, nothing written."""
    from probe.cli.daemon_cli import calling_agent

    wanted = session_marker.normalize_state(value)
    if wanted is None:
        print(_expected_state(value), file=sys.stderr)
        raise typer.Exit(1)
    target = session_marker.switch_target(session_id, wanted, calling_agent())
    if target is None:
        print(session_marker.DAEMON_SWITCH_REFUSAL, file=sys.stderr)
        raise typer.Exit(2)
    return target


def _expected_state(value: object, *, extra: tuple[str, ...] = ()) -> str:
    """The "you typed something else" line, built from the REAL vocabulary.

    One function, so the words a command offers and the words it accepts cannot
    drift apart -- and so a state added to the switch shows up in every error
    message without anyone remembering to go and find them.
    """
    words = [*session_marker.STATE_WORDS, *extra]
    listed = ", ".join(f"'{word}'" for word in words[:-1])
    return f"expected {listed} or '{words[-1]}', got {value!r}"


def _state_block(session_id: str, state: str, *, heal: bool) -> dict:
    """The JSON every state-moving command prints, plus the daemon it owes.

    ONLY a recording state (`full`, `daemon`) is owed a capture daemon --
    `daemon` needs it twice over, since the companion worker is its child.
    `read-only` and `off` both record nothing, so starting one would leave a
    transcript uploader running for a conversation that asked not to be recorded.
    """
    block = {
        "session_id": session_id,
        "state": _state_word(state),
        "label": _state_display(session_id, state),
    }
    if heal and state in session_marker.RECORDING_STATES:
        block["capture"] = _capture_block(session_id, heal_cwd=os.getcwd())
    if state == session_marker.STATE_DAEMON:
        from probe.cli import setup as wizard

        block["daemon"] = _daemon_block(session_id, state)
        if not wizard.companion_token_held():
            block["note"] = (
                "the Probe daemon has no key yet, so the agent keeps recording; Enter on "
                f"Who records in the wizard approves one ({session_marker.WIZARD_HINT})"
            )
    return block


def _daemon_block(session_id: str, state: str) -> "dict | None":
    """The daemon's status in the `daemon` state, else None.

    `status`/`reason` say whether the daemon is recording; `agent_writes` is the
    gate's own list of what stays the agent's (`session_marker.DAEMON_AGENT_WRITES`),
    so an agent asking "may I?" reads the answer rather than the gate's source.
    """
    status = session_marker.daemon_status(session_id, state)
    if status is None:
        return None
    return {
        "status": status[0],
        "reason": status[1],
        "agent_writes": sorted(session_marker.DAEMON_AGENT_WRITES),
        # Allowed only from inside a run's own job (`PROBE_RUN_ID` set).
        "agent_writes_in_run": sorted(session_marker.DAEMON_RUN_WRITES),
        "directed": "add --directed to any other write the researcher asks for",
    }


@session_app.command("state")
def session_state_cmd(
    value: str = typer.Argument(
        None, help="on | read | off \u2014 omit to show the current state"
    ),
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Show or set Probe's state for THIS conversation.

    \b
    on      reads and writes. Records the work as it happens.
    read    reads allowed, records nothing new. Cleanup still works.
    off     no Probe calls at all, and no session-start injections.

    Where the Probe daemon records (`probe wizard` › Defaults › Who
    records), the same three read `on (daemon)` -- stored as `daemon` --,
    `read only (daemon)` and `off`. The daemon is not a position of this
    switch: `daemon` is refused.

    Nothing already recorded is deleted by any of them, and moving back to `on`
    does not backfill the interval that was skipped -- it happened unrecorded,
    and inventing it afterwards would be a worse lie than the gap.

    The words are `on`/`read`/`off`; what lands in the config and the session
    marker is the longer `full`/`read-only`/`off`, because those files are read
    by every other copy of the client on the machine and an older one does not
    know a word this version invented (`session_marker.STATE_LABELS`). Both
    spellings are accepted wherever a state is typed.
    """
    resolved = _resolve_agent_session(session)
    if value is None:
        current = session_marker.session_state(resolved)
        if current is None:
            current, _source = session_marker.resolve_state_default(None)
        _print_json(
            {
                "session_id": resolved,
                "state": _state_word(current),
                "label": _state_display(resolved, current),
            }
        )
        return
    wanted = _switch_word(resolved, value)
    session_marker.set_session_state(resolved, wanted)
    _require_state(resolved, wanted)
    _print_json(_state_block(resolved, wanted, heal=True))


@session_app.command("untrack")
def session_untrack(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Turn recording off for THIS conversation. An alias for `state read`.

    THIS IS NOT THE HARD `off`, and the difference is deliberate. What this
    command has always done -- and always documented -- is "records nothing
    further"; it never gated reads. That is `read-only` exactly, so it keeps
    meaning what it meant for everybody with the phrase in muscle memory or in a
    resumed transcript. The state that also stops reads is reached by naming it:
    `probe session state off`.

    Nothing already recorded is deleted -- the work that landed before this stays
    where it is, because it happened.
    """
    resolved = _resolve_agent_session(session)
    ok = session_marker.set_tracking(resolved, False)
    # No `_capture_block` here, unlike `track` and `toggle`: the guard those
    # two carry ("heal only if the signal now reads on") is unreachable by
    # construction once `_require_tracking_state(resolved, False)` has proven
    # the signal is off, and a branch that can never run is not a safeguard.
    _require_tracking_state(resolved, False)
    _print_json(
        {
            "session_id": resolved,
            "tracking": "off" if ok else "unchanged",
            "state": _state_word(session_marker.session_state(resolved)),
            "note": (
                "already-recorded work is untouched; `probe session track` turns it "
                "back on. Reads still work -- `probe session state off` stops those too"
            ),
        }
    )


@session_app.command("track")
def session_track(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Turn tracking ON for this conversation.

    Explicit, so the status line says `tracking` immediately rather than waiting
    for the first project to land -- which is the point when an agent decides a
    session IS research before it has created anything.
    """
    resolved = _resolve_agent_session(session)
    # `on` is stored by who records: `daemon` where the daemon records (the lean
    # plugin gives the agent nothing to record with, so `full` would record nothing).
    from probe.cli.daemon_cli import calling_agent

    if session_marker.on_state(resolved, calling_agent()) == session_marker.STATE_DAEMON:
        ok = session_marker.set_session_state(resolved, session_marker.STATE_DAEMON)
    else:
        ok = session_marker.set_tracking(resolved, True)
    _require_tracking_state(resolved, True)
    # Tracking just went on, so a daemon is owed. Read back rather than
    # trusting `ok`: `_require_tracking_state` has already proven the signal
    # on disk, and that is the value every other surface will render.
    if session_marker.is_tracking(session_marker.tracking_signal(resolved)):
        _capture_block(resolved, heal_cwd=os.getcwd())
    _print_json(
        {
            "session_id": resolved,
            "tracking": "on" if ok else "unchanged",
            "state": _state_word(session_marker.session_state(resolved)),
        }
    )


@session_app.command("toggle")
def session_toggle(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Toggle this conversation between `on` and `read`.

    \b
        on <---> read        off ---> read

    `off` IS NOT ON THE CYCLE. The bare switch is pressed without reading
    anything, and `off` stops Probe calls entirely -- an agent under it cannot
    find prior work AND cannot know what it missed, so every later answer is
    quietly poorer with nothing to show it. Arriving there by one press too many
    is a cost nobody consented to and nobody can see. `probe session state off`,
    or `/probe off`, is the only way in.

    A press while `off` leaves for `read`: pressing a switch you turned off is
    asking for something to change, and `read` is the smallest change that gives
    back what `off` took away. Getting back to `off` means typing it again.

    "Current" resolves exactly as `status` reports it -- the explicit per-session
    decision when one exists, else this cwd's effective default posture -- so
    advancing never disagrees with what the status line was showing. This is the
    same write the switch's activation hook makes on a bare invocation the
    researcher TYPED, exposed for shells and for reconciling a machine where that
    hook is absent.
    """
    resolved = _resolve_agent_session(session)
    current = session_marker.session_state(resolved)
    if current is None:
        current, _source = session_marker.resolve_state_default(None)
    from probe.cli.daemon_cli import calling_agent

    target = session_marker.next_state(current)
    target = session_marker.switch_target(resolved, target, calling_agent()) or target
    session_marker.set_session_state(resolved, target)
    _require_state(resolved, target)
    block = _state_block(resolved, target, heal=True)
    block["was"] = _state_word(current)
    _print_json(block)


@session_app.command("initialize", hidden=True)
def session_initialize(
    session: str = typer.Option(None, "--session", help="session id"),
    cwd: str = typer.Option(..., "--cwd", help="the host session's initial working directory"),
) -> None:
    """Seed a host session from its initial cwd and return its durable state.

    This is a host-facing bridge for agents whose extension cannot import the
    Python resolver directly. It is deliberately hidden from CLI help: people
    set defaults with `session default` and move a live switch with
    `track|untrack|toggle`.
    """
    resolved = _resolve_agent_session(session)
    agent = _initializing_agent()
    # WHICH PROFILE THIS SESSION RUNS: what the machine's "Who records" says for
    # this agent NOW, written on EVERY start, resume and reload. pi reads its
    # package's skill filter (the profile's install) when it starts, so the
    # session's profile must follow the same moment, not the session's first
    # start. Claude Code and Codex never call this command; their lean plugin
    # writes the mark itself.
    if agent is not None:
        session_marker.mark_session_profile(resolved, session_marker.recorder(agent))
    state = session_marker.session_state(resolved)
    signal = session_marker.tracking_signal(resolved)
    seeded = False
    source = "session"
    if state in (session_marker.STATE_FULL, session_marker.STATE_DAEMON) and agent is not None:
        # An `on` session follows its profile: a session resumed after the
        # researcher switched Who records records the way pi now loads it.
        # `read-only` and `off` are the researcher's own switch and stay.
        target = session_marker.on_state(resolved, agent)
        if target != state and session_marker.set_session_state(resolved, target):
            state = session_marker.session_state(resolved)
            signal = session_marker.tracking_signal(resolved)
    if state is None:
        default, source = session_marker.resolve_state_default(cwd)
        # The same rule as the session-start hook: `on` (or a `daemon` default
        # from before) is stored by who records.
        default = session_marker.seed_state(resolved, default, agent)
        seeded = session_marker.set_session_state_if_absent(resolved, default)
        state = session_marker.session_state(resolved)
        signal = session_marker.tracking_signal(resolved)
        if signal is None:
            print(
                f"could not initialize tracking for session {resolved}",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        if not seeded:
            # Another writer won the atomic publish. Its signal is the answer;
            # the folder value this process resolved is no longer provenance.
            source = "session"

    # heal_cwd=None: this command REPORTS capture and never starts it. The pi
    # extension calls it immediately before its own spawn, so healing here
    # would take that spawn from the extension on every healthy session.
    capture = _capture_block(resolved, heal_cwd=None)
    _print_json(
        {
            "session_id": resolved,
            # `tracking` AND `signal` KEEP THEIR TWO-VALUED MEANING FOREVER.
            # pi's trackingState.ts declares `signal: "on" | "off"` and ships on
            # its own release train, so a machine routinely runs a new CLI
            # against an old extension. Both non-recording states project to
            # `off`, which is TRUE of both and is the strongest thing a
            # two-valued reader can be told. The third value arrives as a NEW
            # field that an old reader simply ignores.
            "tracking": session_marker.is_tracking(signal),
            "signal": signal,
            "state": _state_word(state),
            "seeded": seeded,
            "source": source,
            "capture": capture,
            "effective": _effective(session_marker.is_tracking(signal), capture),
            # NEW, additive (an old extension ignores it): "daemon" when the
            # Probe daemon records and reads for this session, else "agent".
            "profile": session_marker.session_profile(resolved) or session_marker.RECORDER_AGENT,
        }
    )


def _initializing_agent() -> "str | None":
    """The coding agent calling `session initialize`: its session markers when
    this shell has them, else `PROBE_AGENT` when it names a harness. The pi
    extension runs this command with an allowlisted environment that carries
    `PROBE_AGENT=pi` and no PI_* variable (pi sets those only on its bash
    tool's children), so without the second rung every pi session seeded as
    if no agent had called."""
    from probe.cli.daemon_cli import calling_agent
    from probe.harness import get_registry

    detected = calling_agent()
    if detected is not None:
        return detected
    harness = get_registry().find(os.environ.get("PROBE_AGENT"))
    return harness.id if harness is not None and harness.installable else None


@session_app.command("status")
def session_status(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """Whether this conversation is being tracked, and how that was decided."""
    resolved = _resolve_agent_session(session)
    signal = session_marker.tracking_signal(resolved)
    session_state = session_marker.session_state(resolved)
    state = session_marker.read(resolved)
    default = session_marker.default_tracking()
    cwd_default, cwd_default_source = session_marker.resolve_tracking_default(None)
    cwd_state_default, _cwd_state_source = session_marker.resolve_state_default(None)
    if session_state is None:
        session_state = cwd_state_default
    tracking = session_marker.is_tracking(signal) if signal is not None else cwd_default
    machine_source = str(Path(os.path.abspath(os.fspath(session_marker.config_path()))))
    if signal is not None:
        decided_by = "session"
    elif cwd_default_source == "environment":
        decided_by = "environment"
    elif cwd_default_source in ("shipped", machine_source):
        decided_by = "machine default"
    else:
        decided_by = "folder default"
    capture = _capture_block(resolved, heal_cwd=os.getcwd())
    reads_allowed = session_marker.state_allows_reads(session_state)
    _print_json(
        {
            "session_id": resolved,
            "tracking": tracking,
            "state": _state_word(session_state),
            "label": _state_display(resolved, session_state),
            "reads_allowed": reads_allowed,
            # Whether the AGENT may record freely. Under `daemon` with a live
            # lease the daemon records and this is False; degraded, it is True.
            "writes_allowed": session_marker.agent_writes_freely(resolved, session_state),
            "daemon": _daemon_block(resolved, session_state),
            # WHY, not just what. The status line shows two states on purpose, so
            # "off because I said so" and "off because this machine defaults off"
            # look identical there; this is where they separate.
            "decided_by": decided_by,
            "signal": signal,
            "machine_default": "on" if default else "off",
            "machine_default_state": _state_word(session_marker.default_session_state()),
            # Diagnostic only: this is what a NEW session started here would
            # inherit. It does not relabel an existing session signal, which may
            # have been seeded from another directory or changed explicitly.
            "cwd_default": "on" if cwd_default else "off",
            "cwd_default_source": cwd_default_source,
            "project": (state or {}).get("project"),
            "runs": len((state or {}).get("run_ids") or []),
            "running": tracking and session_marker.is_live(state),
            # WHETHER anything is actually listening, and the closed reason
            # when nothing is. `tracking: true` with no daemon is the lie this
            # pair exists to make unsayable.
            "capture": capture,
            "effective": _effective(tracking, capture),
            # Runs opened with no project (daemon v2) that nobody has filed yet.
            # null under `off`, which promises no Probe calls at all.
            "unfiled_runs": _unfiled_runs_block() if reads_allowed else None,
        }
    )


#: `probe session status` is read by agents between steps; a dead endpoint must
#: not park it for the transport's full retry budget.
_UNFILED_STATUS_TIMEOUT_S = 3.0


def _unfiled_runs_block() -> dict:
    """`doctor.unfiled_summary`, bounded in time and never raising.

    A daemon thread, so a request still hanging after the deadline cannot hold
    the process open on exit."""
    import threading

    from .doctor import unfiled_summary

    if not resolve(base_url=_conn.base_url).token:
        return {"state": "unknown", "reason": "not logged in"}
    box: dict = {}

    def look() -> None:
        try:
            with _client() as c:
                box["summary"] = unfiled_summary(c)
        except Exception as exc:  # noqa: BLE001 - a status read never fails on this
            box["summary"] = {"state": "unreadable", "reason": str(exc)[:200] or type(exc).__name__}

    worker = threading.Thread(target=look, name="probe-unfiled-status", daemon=True)
    worker.start()
    worker.join(_UNFILED_STATUS_TIMEOUT_S)
    return box.get("summary") or {"state": "unreadable", "reason": "timed out"}


@session_app.command("default")
def session_default(
    value: str = typer.Argument(
        None,
        help="on | read | off | inherit — omit to show; inherit requires --folder",
    ),
    folder: Path | None = typer.Option(
        None,
        "--folder",
        help="existing directory whose exact tracking override to show or set",
    ),
) -> None:
    """Show or set a new session's tracking default.

    Without --folder, reads or sets the machine default. With --folder, reads
    or sets that folder's override. inherit removes the exact folder override
    so the folder returns to parent or machine inheritance.

    Stored TOP-LEVEL in the probe config, never inside a context: `probe logout`
    replaces a context wholesale, so a preference kept there would be wiped and
    tracking would silently come back on. Top level also keeps the default from
    following whichever tenant is selected, which is not what "all my sessions"
    means.

    A per-session `probe session track|untrack` always wins over this.

    `daemon` is refused: whether the Probe daemon records is `probe wizard
    ` › Defaults › Who records, and a new session's `on` follows it.
    """
    if folder is None and value is None:
        _print_json(
            {
                "machine_default": _state_word(session_marker.default_session_state()),
                "config": str(session_marker.config_path()),
                "note": "per-session `probe session state` overrides this",
            }
        )
        return

    if folder is None:
        wanted = session_marker.normalize_state(value)
        if wanted is None:
            print(_expected_state(value), file=sys.stderr)
            raise typer.Exit(1)
        if wanted == session_marker.STATE_DAEMON:
            print(session_marker.DAEMON_SWITCH_REFUSAL, file=sys.stderr)
            raise typer.Exit(2)

        from ..sdk.config import ConfigUnreadable

        try:
            # Shared with the wizard's Settings screen. It raises rather than
            # writing through a failed read, so a broken config file is reported
            # here, never replaced by just this preference.
            path = session_marker.write_default_state(wanted)
        except (OSError, ValueError, ConfigUnreadable) as exc:
            print(f"could not update {session_marker.config_path()}: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
        _print_json({"machine_default": _state_word(wanted), "config": str(path)})
        return

    target = Path(os.path.abspath(os.fspath(folder)))
    if not target.is_dir():
        print(f"{target} is not an existing directory", file=sys.stderr)
        raise typer.Exit(1)

    if value is not None:
        raw = value.strip().lower()
        if raw == "inherit":
            wanted = None
        else:
            wanted = session_marker.normalize_state(raw)
            if wanted is None:
                print(_expected_state(value, extra=("inherit",)), file=sys.stderr)
                raise typer.Exit(1)
            if wanted == session_marker.STATE_DAEMON:
                print(session_marker.DAEMON_SWITCH_REFUSAL, file=sys.stderr)
                raise typer.Exit(2)

        from ..sdk.config import ConfigUnreadable

        try:
            session_marker.write_folder_state_default(target, wanted)
        except (OSError, ValueError, ConfigUnreadable) as exc:
            path = session_marker.folder_config_path(target)
            print(f"could not update {path}: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc

    ignored_errors: list[str] = []
    folder_override = session_marker._folder_state_override(
        session_marker.folder_config_path(target), ignored_errors
    )
    effective, source = session_marker.resolve_state_default(target, errors=ignored_errors)
    _print_json(
        {
            "folder": str(target),
            "folder_override": _state_word(folder_override),
            "effective_default": _state_word(effective),
            "source": source,
            "ignored_errors": ignored_errors,
        }
    )


views_app = typer.Typer(
    no_args_is_help=True, help="expression views: formulas over a run's logged series"
)
app.add_typer(views_app, name="views")


def _read_spec(spec: str | None, spec_file: str | None) -> dict:
    """Resolve --spec / --spec-file into a validated view spec.

    ``--spec-file -`` reads stdin, so a generator script can pipe straight in
    without a temp file. Validation happens here rather than at the server, so a
    typo names its own field instead of coming back as a 422.
    """
    if (spec is None) == (spec_file is None):
        raise typer.BadParameter("pass exactly one of --spec or --spec-file")
    if spec_file is not None:
        raw = sys.stdin.read() if spec_file == "-" else Path(spec_file).read_text()
    else:
        raw = spec
    try:
        parsed = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise typer.BadParameter(f"spec is not valid JSON: {exc}") from exc

    from probe import expr as expr_module

    try:
        return expr_module.spec(parsed)
    except Exception as exc:  # noqa: BLE001 -- pydantic error text is the message
        raise typer.BadParameter(f"invalid expression spec: {exc}") from exc


@views_app.command("list")
def views_list(run: str = run_ref()) -> None:
    """Every expression view on a run, with its spec and provenance."""
    with _client() as c:
        _print_json(c.list_views(run))


@views_app.command("show")
def views_show(
    run: str = run_ref(),
    view: str = typer.Argument(..., metavar="VIEW", help="view id or name"),
) -> None:
    """One view, by id or by name."""
    with _client() as c:
        views = c.list_views(run)
    for row in views:
        if view in (str(row.get("id")), row.get("name")):
            _print_json(row)
            return
    names = ", ".join(sorted(str(r.get("name")) for r in views)) or "none"
    raise typer.BadParameter(f"no view {view!r} on run {run}; run has: {names}")


@views_app.command("create")
def views_create(
    run: str = run_ref(),
    name: str = typer.Argument(..., help="panel title; unique per run"),
    spec: str = typer.Option(None, "--spec", metavar="JSON", help="inline spec"),
    spec_file: str = typer.Option(
        None, "--spec-file", metavar="PATH", help="spec JSON from a file, or - for stdin"
    ),
) -> None:
    """Save a view. Works on a completed run — a view reads, it never appends."""
    body = _read_spec(spec, spec_file)
    with _client() as c:
        _print_json(c.create_view(run, name, body))


@views_app.command("preview")
def views_preview(
    run: str = run_ref(),
    spec: str = typer.Option(None, "--spec", metavar="JSON"),
    spec_file: str = typer.Option(None, "--spec-file", metavar="PATH", help="or - for stdin"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_points: int = typer.Option(None, "--max-points"),
) -> None:
    """Evaluate a spec WITHOUT saving it.

    Run this before `create`: a spec naming a series the run never logged comes
    back here with `missing_inputs`, instead of being saved as a panel that
    renders empty for everyone who opens the run.
    """
    body = _read_spec(spec, spec_file)
    with _client() as c:
        _print_json(
            c.preview_view(run, body, step_from=step_from, step_to=step_to, max_points=max_points)
        )


@views_app.command("data")
def views_data(
    run: str = run_ref(),
    view_id: str = typer.Argument(...),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    max_points: int = typer.Option(None, "--max-points"),
) -> None:
    """Evaluate a saved view and print its curve.

    Read the whole envelope, not just `points`: `missing_inputs` names series the
    expression referenced that the run has none of, `dropped_nonfinite` counts
    NaN/inf results, and `truncated` says the input scan hit its bound.
    """
    with _client() as c:
        _print_json(
            c.view_data(run, view_id, step_from=step_from, step_to=step_to, max_points=max_points)
        )


@views_app.command("rename")
def views_rename(
    view_id: str = typer.Argument(...),
    name: str = typer.Argument(...),
) -> None:
    """Rename a view. The expression is untouched."""
    with _client() as c:
        _print_json(c.update_view(view_id, name=name))


@views_app.command("update")
def views_update(
    view_id: str = typer.Argument(..., help="view id (`probe views list RUN` shows it)"),
    name: str = typer.Option(None, "--name", help="new name; omit to keep it"),
    spec: str = typer.Option(
        None, "--spec", metavar="JSON", help="new expression; REPLACES the stored one whole"
    ),
    spec_file: str = typer.Option(
        None, "--spec-file", metavar="PATH", help="spec JSON from a file, or - for stdin"
    ),
    expected_updated_at: str = typer.Option(
        None,
        "--expected-updated-at",
        metavar="TIMESTAMP",
        help="the view's updated_at as you read it; refused if it changed since",
    ),
) -> None:
    """Change a view's expression and/or name.

    The spec replaces the stored one whole, so read the view first (`probe views
    list RUN`) and build on what is there. Pass its `updated_at` as
    `--expected-updated-at` and an edit made since you read it is refused rather
    than overwritten; the refusal prints the view as it is now.
    """
    body = _read_spec(spec, spec_file) if (spec is not None or spec_file is not None) else None
    if name is None and body is None:
        raise typer.BadParameter("pass --name, --spec or --spec-file")
    with _client() as c:
        try:
            updated = c.update_view(
                view_id, name=name, spec=body, expected_updated_at=expected_updated_at
            )
        except errors.ConflictError as exc:
            if not (isinstance(exc.detail, dict) and "current" in exc.detail):
                raise  # a name clash, not a moved view: the plain error says it
            print(f"error: {exc}", file=sys.stderr)
            # The view as it stands, so the caller can rebuild its change on it
            # without a second read. null: it was deleted meanwhile.
            current = json.dumps(exc.detail["current"], ensure_ascii=False)
            print(f"current: {current}", file=sys.stderr)
            raise typer.Exit(1) from exc
    _print_json(updated)


@views_app.command("delete")
def views_delete(view_id: str = typer.Argument(...)) -> None:
    """Delete a view. The series it read are untouched."""
    with _client() as c:
        c.delete_view(view_id)
    print(f"deleted view {view_id}")


series_app = typer.Typer(no_args_is_help=True, help="cross-run series reads")
app.add_typer(series_app, name="series")


@series_app.command("latest")
def series_latest(
    runs: list[str] = typer.Argument(..., metavar="RUN..."),
    key: list[str] = typer.Option(None, "--key", help="repeatable; narrow to these keys"),
    kind: str = typer.Option(None, "--kind"),
) -> None:
    """Cross-run scalar summary (last/min/max per series) from the catalog."""
    with _client() as c:
        _print_json(c.latest_scalars(runs, keys=key or None, kind=kind))


# -- spans ------------------------------------------------------------------
span_app = typer.Typer(no_args_is_help=True, help="trajectory spans")
app.add_typer(span_app, name="span")


@span_app.command("add")
def span_add(
    run: str = typer.Argument(...),
    span_type: str = typer.Option(..., "--type"),
    name: str = typer.Option(None, "--name"),
    step: int = typer.Option(None, "--step"),
    provider: str = typer.Option(None, "--provider"),
    external_key: str = typer.Option(None, "--external-key"),
    parent: str = typer.Option(None, "--parent"),
    status: str = typer.Option("running", "--status"),
    attr: list[str] = typer.Option(None, "--attr", metavar="k=v"),
    write_mode: Optional[bool] = write_mode_opt(),
) -> None:
    """Upsert a span."""
    _check_ref_shape(run)
    with _default_client(_resolve_write_mode(write_mode)) as c:
        if c.async_writes:
            handle = _async_run(c, run).span(
                span_type,
                name=name,
                step_index=step,
                provider=provider,
                external_key=external_key,
                parent_span_id=parent,
                status=status,
                attributes=_kv_pairs(attr) if attr else None,
            )
            _kick_drainer()
            # The span id is minted CLIENT-SIDE, so queueing still hands back the
            # real id -- this is the whole reason `span add` can be queued at all
            # while a verb whose id the server mints cannot.
            print(handle)
            return
        span_id = _run_handle(c, run).span(
            span_type,
            name=name,
            step_index=step,
            provider=provider,
            external_key=external_key,
            parent_span_id=parent,
            status=status,
            attributes=_kv_pairs(attr) if attr else None,
        )
    print(span_id)


@span_app.command("list")
def span_list(
    run: str = typer.Argument(...),
    span_type: str = typer.Option(None, "--type"),
    parent: str = typer.Option(None, "--parent"),
    step_from: int = typer.Option(None, "--step-from"),
    step_to: int = typer.Option(None, "--step-to"),
    limit: int = typer.Option(None, "--limit"),
) -> None:
    """Read a run's spans back."""
    with _client() as c:
        _print_json(
            c.run_spans(
                # GET /v1/runs/{run_id}/spans types its path param as a UUID, so a
                # petname reached it as a 422 -- on the one kind whose petname is
                # the handle people are handed. `span add` two commands up already
                # resolves (via _run_handle); this read did not.
                _ref(c, "run", run).id,
                span_type=span_type,
                parent_span_id=parent,
                step_from=step_from,
                step_to=step_to,
                limit=limit,
            )
        )


@span_app.command("get")
def span_get(span_id: str = typer.Argument(...)) -> None:
    """Print one span."""
    with _client() as c:
        _print_json(c.get_span(span_id))


# -- artifacts --------------------------------------------------------------
artifact_app = typer.Typer(no_args_is_help=True, help="artifacts")
app.add_typer(artifact_app, name="artifact")


#: Anchors whose ref has a slug spelling. Runs anchor by id or petname and are
#: resolved server-side; workspaces and the Shared folder have ids only.
_SLUG_ANCHORS = {
    Anchor.PROJECT: "project",
    Anchor.EXPERIMENT: "experiment",
    Anchor.WORKSPACE: "workspace",
}


def _anchor_id_for(client: Client, anchor: Anchor, anchor_id: str | None) -> str | None:
    """Let a project or experiment anchor be named by SLUG, not only by id.

    Every ``/v1/{kind}/{id}`` route types the path param as a UUID, so a slug
    reaches the server as a 422 about UUID parsing. That is survivable for a
    human who can look the id up once; it is not survivable for an agent filing a
    few thousand artifacts, which would have to thread a uuid through every
    command and only has to get it wrong once.

    Slugs are the handle people actually remember -- the same reason
    :func:`_project_id` exists for the project verbs. Experiments were left out
    of this originally, which made ``--project my-slug`` work and ``--experiment
    my-slug`` 422 on the same command line.

    ADDITIVE, never a new gate. An id passes straight through, and so does
    anything that does not resolve: this route already answers a bad anchor with
    a 422, and turning that into a local hard error would reject values that
    were previously fine (an id this caller cannot enumerate). The exact
    ``?slug=`` lookup is used rather than listing, so it is one request and
    correct past 200 rows.
    """
    kind = _SLUG_ANCHORS.get(anchor)
    if kind is None or not anchor_id:
        return anchor_id
    # verify=False: an `id:` ref does not need a round trip to confirm it exists
    # -- it IS the id, and returns without touching the network. That keeps the
    # agent path (thousands of artifacts) at one request for a slug, none for an id.
    #
    # This used to swallow every error and pass the raw ref through, on a
    # "never a gate" rationale that slug-default invalidates: the route types its
    # path param as a UUID, so passing a bare UUID through is not a no-op -- the
    # SERVER reads it as an id and files the upload against whichever project owns
    # it. That is the misresolution this whole grammar exists to end, so a failed
    # lookup is now an error instead of a silent redirect.
    if kind == "workspace":
        # Its own resolver: the listing is complete (unpaginated by contract), so
        # there is no server-side ?slug= to ask for and none is needed.
        return refs.resolve_workspace(client, anchor_id).id
    return refs.resolve(client, kind, anchor_id, verify=False).id


def _pick_anchor(
    *,
    run: str | None,
    project: str | None,
    experiment: str | None,
    workspace: str | None,
    shared: bool,
) -> tuple[Anchor, str | None]:
    """Resolve exactly one anchor from the flags, or fail loudly.

    An artifact hangs off exactly one thing (the DB CHECKs it), so two anchors is a
    mistake worth stopping for rather than silently picking a winner.
    """
    chosen = [
        (Anchor.PROJECT, project),
        (Anchor.EXPERIMENT, experiment),
        (Anchor.WORKSPACE, workspace),
    ]
    given = [(a, v) for a, v in chosen if v is not None]
    if shared:
        given.append((Anchor.SHARED, None))
    if run is not None:
        given.append((Anchor.RUN, run))
    if len(given) > 1:
        names = ", ".join(f"--{a.value}" if a is not Anchor.RUN else "RUN" for a, _ in given)
        raise typer.BadParameter(f"an artifact anchors to exactly one thing; got {names}")
    if not given:
        raise typer.BadParameter(
            "needs an anchor: a RUN argument, or --project/--experiment/--workspace/--shared"
        )
    return given[0]


#: Artifact kinds whose bytes Probe STORES rather than points at.
#:
#: A reference to code is the failure this whole surface exists to avoid. A
#: `file://` pointer resolves on one machine, for as long as that machine and
#: that checkout survive, and nothing downstream can tell a live pointer from a
#: dead one without going and looking -- which is exactly why git referencing
#: was retired from `capture_manifest`. Leaving the same hole open on the manual
#: door would just move it. Scripts are small and storing them is cheap.
#:
#: RUN-anchored by construction: `--kind` is a run-only flag (the project /
#: experiment / workspace upload contract rejects it), so a non-run artifact is
#: always kind "file" and never lands here.
#:
#: BOTH separators, because `--kind` is a free-form string and the repo's own
#: vocabulary carries both spellings -- the SDK writes `code_snapshot` while
#: `app/artifacts/preview.py` matches `code-snapshot`. A set covering one of
#: them is a rule with a typo-shaped hole: `--kind code-snapshot --reference`
#: would record exactly the pointer this exists to prevent.
CODE_KINDS = frozenset(
    {
        "code",
        "code_bytes",
        "code-bytes",
        "code_snapshot",
        "code-snapshot",
        "script",
        "source",
    }
)


def _is_code_kind(kind: str | None) -> bool:
    """Is this the kind of artifact whose bytes Probe stores rather than points at?

    Normalized the way the server normalizes a kind for the same purpose
    (``preview.preview_max_bytes``): stripped and lowercased, so surrounding
    whitespace out of a manifest row cannot walk a code artifact past the rule.
    """
    return (kind or "").strip().lower() in CODE_KINDS


def _reference_after_code_check(
    kind: str, *, reference: bool, path: str | None, allow_missing: bool
) -> bool:
    """The effective ``reference`` flag: never True for a code kind.

    Returns what ``reference`` should actually be, so a code artifact takes the
    upload path even when ``--reference`` was passed.

    REFUSES rather than quietly recording a pointer when the bytes cannot be
    read from here. Falling back to a reference would reintroduce the exact row
    this rule exists to prevent, and do it in the one case nobody is watching.
    """
    if not (reference and _is_code_kind(kind)):
        return reference
    if allow_missing or not path or not os.path.isfile(path):
        raise typer.BadParameter(
            f"--kind {kind} is stored, never referenced, so its bytes have to be "
            f"readable from this host — {path!r} is not. Point it at a readable "
            "file (and drop --allow-missing), or use a non-code --kind if a "
            "pointer is genuinely what you want."
        )
    return False


def _validate_artifact_row(
    anchor: Anchor,
    *,
    path: str | None,
    uri: str | None,
    name: str | None,
    reference: bool,
    hash_content: bool,
    allow_missing: bool,
    kind: str,
    step: int | None,
    span: str | None,
    # Only its truthiness is read, so the caller may hand over either spelling:
    # the CLI's raw `--meta k=v` list or a manifest row's already-parsed object.
    meta: dict | list | None,
) -> str:
    """The usage checks for ONE artifact write, and the name it lands under.

    Shared by the single-file `artifact add` and every `--from-manifest` row so
    the two cannot disagree about what is legal. That matters more than the
    duplication it saves: a manifest is the bulk path, so a rule enforced on the
    command line and not on a row would be discovered a hundred thousand rows
    later, server-side, with no operator watching.

    Raises :class:`typer.BadParameter`. On the command line that aborts, which is
    right for one file; the manifest catches it per row and keeps going.
    """
    resolved = name
    if resolved is None and path:
        resolved = os.path.basename(path)
    if resolved is None:
        raise typer.BadParameter("artifact needs --name (or a path to derive it from)")
    # `--name` REPLACES the basename, and agents pass an identity there, so the
    # extension arrives here already stripped. Put it back from the path the bytes
    # came from -- additive only, and applied at THIS door (not just the SDK's) so
    # the async branch journals the repaired name rather than the bare one.
    resolved = name_with_extension(resolved, path)
    if reference and uri is not None:
        raise typer.BadParameter(
            "--reference derives a file:// pointer from the path; pass --reference OR "
            "--uri, not both"
        )
    if reference and not path:
        raise typer.BadParameter("--reference needs a local file path")
    # The OTHER door to a machine-local code pointer. `--reference` derives a
    # file:// uri from a path; `--uri file://...` states one outright, and
    # closing only the first would leave the rule true in the help text and
    # false in the CLI. Bucket schemes (s3/r2/https) are untouched for every
    # kind -- those name durable storage, and there is no local file to upload
    # in their place. Checked here so the command line and every manifest row
    # get the same answer.
    if uri is not None and _is_code_kind(kind) and str(uri).strip().lower().startswith("file:"):
        raise typer.BadParameter(
            f"--kind {kind} is stored, never referenced, so it cannot be a "
            f"file:// pointer: {uri!r} names a path on one machine. Pass the "
            "local path to upload the bytes, or use a bucket uri (s3://, r2://) "
            "if they already live in durable storage."
        )
    if (hash_content or allow_missing) and not reference:
        raise typer.BadParameter("--hash and --allow-missing only apply to --reference")
    if anchor is not Anchor.RUN:
        if step is not None or kind != "file" or span is not None or meta:
            raise typer.BadParameter(
                f"--kind/--step/--span/--meta are run-only; "
                f"the {anchor.value} upload contract rejects them"
            )
        if (uri is not None or reference) and anchor in _FILE_ANCHORS:
            # Caught here rather than in the SDK so it reads as a usage error instead
            # of an unhandled ValueError traceback: a file IS its bytes, so there is
            # no reference-without-bytes form and the backend declares no such route.
            raise typer.BadParameter(
                f"a {anchor.value} file cannot be a reference (it IS its bytes). "
                "Pass a local path to upload the bytes instead."
            )
    return resolved


def _ping_presign(
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    *,
    digest: str,
    size: int,
    content_type: str | None,
    kind: str | None,
    meta: dict | None,
    notes: str | None = None,
    span_id: str | None,
    step_index: int | None,
    context: dict | None = None,
) -> str | None:
    """The 1A intent ping: a capped, best-effort presign at enqueue so the
    server's pending row (and its reaper) know this upload is coming. Never
    raises and never waits past the cap -- a dead network degrades to
    local-only enqueue, and the drainer re-presigns on every attempt anyway.
    """
    try:
        from ..sdk.transport import Transport

        if context is not None:
            # Same principal as the drain will use (red team: an ambient env
            # token could register the intent row under a different tenant
            # than the one the op's pinned context delivers to).
            from ..sdk.journal import _settings_for_op

            settings = _settings_for_op(context)
        else:
            from ..sdk.config import resolve

            settings = resolve(base_url=_conn.base_url)
        if not settings.token:
            return None
        transport = Transport(
            settings,
            timeout=_PING_TIMEOUT_SECONDS,
            max_retries=_PING_MAX_RETRIES,
            surface=Surface.CLI.value,
            client_headers=client_version_headers("cli", __version__),
        )
        with Client(settings=settings, transport=transport) as ping:
            presign = ping.presign_upload(
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
        return presign.get("artifact_id")
    except Exception:  # noqa: BLE001 -- intent registration is best-effort by design
        return None


_REFERENCE_ROUTES = {
    # An experiment's files answer at its PROJECT address, where a leaf's
    # rows are filed at its own `project_id` (0241). Same list, from the door
    # that survives the cut.
    Anchor.EXPERIMENT: "/v1/projects/{id}/artifacts",
    Anchor.PROJECT: "/v1/projects/{id}/artifacts",
}

#: The 1A intent-ping cap. Load-bearing product behavior (CHANGELOG: "a
#: ~2s-capped presign ping") -- named so the documented cap and the code
#: cannot silently drift.
_PING_TIMEOUT_SECONDS = 2.0
_PING_MAX_RETRIES = 0


def _artifact_enqueue(
    client: Client,
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    *,
    path: str | None,
    uri: str | None,
    reference: bool,
    hash_content: bool,
    allow_missing: bool,
    kind: str,
    step: int | None,
    span: str | None,
    content_type: str | None,
    meta: dict | None,
    notes: str | None = None,
    ping: bool = True,
    require_staged: bool = False,
) -> dict:
    """Journal ONE artifact operation on an already-open async client.

    Split out of :func:`_artifact_add_async` so `--from-manifest` can drive it per
    row: the manifest's whole reason to exist is that opening a client, resolving
    an anchor and starting a process per file is what makes a bulk import cost
    CPU-hours. This function opens nothing, prints nothing, and kicks nothing --
    the caller owns the client and decides when to wake the drainer.

    ``ping=False`` skips the capped presign ping. Intent registration is
    best-effort by contract (the drainer re-presigns on every attempt), and at
    manifest scale a per-row round trip capped at 2s is the very cost the bulk
    path exists to avoid.

    ``require_staged`` refuses to queue an op whose bytes could not be staged,
    returning ``mode="unstaged"`` so the caller can upload synchronously instead.
    Default False keeps the manifest path on its documented trade: at bulk scale
    an unstaged reference is the point, and 200k synchronous fallbacks are not.

    Returns ``{"mode": "reference"|"upload"|"unstaged"|"refused", "op_id":
    str|None, "pinged": bool}``. ``unstaged`` means staging was refused and
    nothing was queued; ``refused`` means the outbox itself could not be written
    and nothing was queued -- both hand the write back to the caller.
    """
    run_ref = anchor_id if anchor is Anchor.RUN else None
    if reference or uri is not None:
        if anchor is Anchor.RUN:
            _async_run(client, anchor_id).log_artifact(
                name,
                path=path,
                uri=uri,
                reference=reference,
                hash_content=hash_content,
                allow_missing=allow_missing,
                kind=kind,
                step_index=step,
                span_id=span,
                content_type=content_type,
                meta=meta,
                notes=notes,
            )
        else:
            if reference:
                fields = reference_fields(
                    path, hash_content=hash_content, allow_missing=allow_missing
                )
                body = {"name": name, "is_reference": True, **fields}
            else:
                body = {"name": name, "uri": uri, "is_reference": True}
            if content_type:
                body["content_type"] = content_type
            if notes:
                # scrub_text, not default_scrub: `notes` is PROSE, and
                # default_scrub redacts by KEY name, which never fires on a key
                # called "notes". The op file outlives the command.
                from ..sdk.redaction import scrub_text

                body["notes"] = scrub_text(notes)
            # `_enqueue`, not `journal.append_http`: this was the last bypass of
            # the never-raises rule the upload path adopted.
            if not client._enqueue("POST", _REFERENCE_ROUTES[anchor].format(id=anchor_id), body):
                return {"mode": "refused", "op_id": None, "pinged": False}
        return {"mode": "reference", "op_id": None, "pinged": False}

    if not path:
        raise typer.BadParameter("needs a file path (--reference, or --uri)")
    if not os.path.isfile(path):
        # A FIFO, device, or procfs stream would block fingerprint/snapshot
        # forever -- async promises bounded enqueue time (codex).
        raise typer.BadParameter(f"{path} is not a regular file")
    from ..sdk.journal import INLINE_HASH_MAX_BYTES

    run_only = anchor is Anchor.RUN
    # Snapshot first, hash the snapshot (inside append_upload): hashing
    # the live file and copying it later would let a same-size rewrite
    # in between poison the content address (codex TOCTOU).
    # `_enqueue_upload`, not `journal.append_upload`: the journal raises on a full
    # or read-only spool (ENOSPC, flock ENOSYS on Lustre/FUSE), and this call site
    # is exactly the one the http-path guard never covered. It also scrubs
    # meta/notes before they reach the ops file, where a failed op keeps them.
    queued = client._enqueue_upload(
        anchor=anchor.value,
        anchor_id=anchor_id,
        name=name,
        src_path=path,
        inline_hash=os.path.getsize(path) <= INLINE_HASH_MAX_BYTES,
        content_type=content_type,
        kind=kind if run_only else None,
        meta=meta if run_only else None,
        # NOT gated on run_only: notes is accepted at every anchor (0095).
        notes=notes,
        span_id=span,
        step_index=step,
        run_ref=run_ref,
        require_staged=require_staged,
    )
    if queued is None:
        # The outbox refused the write and said so in a warning. Hand it back
        # rather than reporting a queue that does not hold it.
        return {"mode": "refused", "op_id": None, "pinged": False}
    if queued["op_id"] is None:
        # require_staged and no headroom: nothing was appended, so the caller's
        # synchronous upload is the only writer. Leaving an op queued here is
        # what would upload the file twice, with the drainer's later read of a
        # rotated src_path winning.
        return {
            "mode": "unstaged",
            "op_id": None,
            "pinged": False,
            "unstaged_reason": queued.get("unstaged_reason"),
        }
    pinged = False
    if ping and queued["blob"] is not None:
        pinged = (
            _ping_presign(
                anchor,
                anchor_id,
                name,
                digest=queued["blob"],
                size=queued["size_bytes"],
                content_type=content_type,
                kind=kind if run_only else None,
                meta=meta if run_only else None,
                notes=notes,
                span_id=span,
                step_index=step,
                context=client.journal.context,
            )
            is not None
        )
    return {"mode": "upload", "op_id": queued["op_id"], "pinged": pinged}


def _artifact_add_async(
    client: Client,
    anchor: Anchor,
    anchor_id: str | None,
    name: str,
    *,
    path: str | None,
    uri: str | None,
    reference: bool,
    hash_content: bool,
    allow_missing: bool,
    kind: str,
    step: int | None,
    span: str | None,
    content_type: str | None,
    meta: dict | None,
    notes: str | None = None,
) -> bool:
    """Queue an artifact operation and return immediately.

    Returns True when the write is queued, False when the caller must upload it
    SYNCHRONOUSLY instead -- staging was refused, or the outbox could not be
    written. False is not an error: it means nothing was enqueued, so the caller
    is now the only writer and must actually do the write.

    Reference/uri forms are pure JSON writes and journal as http ops -- zero
    staging, the fastest path. Byte uploads snapshot into the blob store;
    files at or under the 11A threshold fingerprint inline and fire the capped
    presign ping so the server registers intent, bigger files defer hashing to
    the drainer so return time stays flat.

    Takes the caller's client rather than opening its own: the caller already
    resolved the write mode and holds a client that agrees with it, and opening
    a second one here could disagree with that decision.
    """
    result = _artifact_enqueue(
        client,
        anchor,
        anchor_id,
        name,
        path=path,
        uri=uri,
        reference=reference,
        hash_content=hash_content,
        allow_missing=allow_missing,
        kind=kind,
        step=step,
        span=span,
        content_type=content_type,
        meta=meta,
        notes=notes,
        # The single-file path REFUSES an unstaged op. An unstaged op records
        # src_path and the drainer reads the live file at delivery, so a bare
        # `probe artifact add ckpt.pt` beside a rotating training loop would
        # upload step-1100 bytes under the step-1000 name. Nobody asked for that
        # by typing a bare command. The manifest path keeps the old trade.
        require_staged=True,
    )
    if result["mode"] in ("unstaged", "refused"):
        return False
    _kick_drainer()
    if result["mode"] == "reference":
        print(f"added reference {name!r} (queued)")
        return True
    registered = "intent registered" if result["pinged"] else "intent deferred to drain"
    print(f"added upload {name!r} op={result['op_id']} ({registered}) (queued)")
    return True


def _fail_if_dropped(client: Client, before: int, what: str) -> None:
    """Exit non-zero when the outbox swallowed the write we just handed it.

    `Client._enqueue` fails OPEN by design: a broken outbox must not kill a
    training step, so it records the gap, warns, and returns normally. The bool
    it returns then dies in `write()`, which returns None either way -- so
    without this check the CLI prints "(queued)" for data that reached nothing
    and exits 0. A queued write may be undelivered; it may not be imaginary.
    """
    if client.dropped_writes > before:
        typer.echo(
            f"probe: {what} was NOT queued - the outbox could not be written "
            "(see the warning above). Fix the spool, then re-run; "
            "`probe outbox status` shows what is on disk.",
            err=True,
        )
        raise typer.Exit(2)


@contextlib.contextmanager
def _queue_client_if_possible(explicit: bool | None):
    """Yield a client for the queue path, or None when there is no queue path.

    `explicit is False` means the caller has already ruled queueing out --
    `--sync`, or a non-run anchor taking the synchronous default. Constructing a
    client to ask it a question whose answer is known, and then closing it, is
    pure cost; the synchronous path below opens its own.
    """
    if explicit is False:
        yield None
        return
    client = _default_client(explicit)
    try:
        yield client
    finally:
        client.close()


def _drain_colliding_uploads(anchor: Anchor, anchor_id: str | None, name: str) -> None:
    """Deliver any QUEUED upload for this same (anchor, name) before a direct one.

    A direct upload carries no journal sequence number, so it can land ahead of a
    queued write that was made EARLIER for the same name -- and which of two
    same-name artifacts a later lookup returns is decided by recency at the
    server, not by the order you logged them. Delivering the queued one first
    restores the order the caller actually wrote in.

    Runs before EVERY direct upload, not only the low-disk fallback: `--sync` and
    a credential-degraded session reach the server the same way and invert the
    same order. It is still free on the hot path, because a QUEUED add never gets
    here -- which is what keeps the per-append O(N^2) listdir curve that
    b820e9c8 removed from coming back.

    Best-effort by contract: this improves ordering, it is not a lock. A failure
    to drain must never stop the upload the user asked for.
    """
    # RUN ANCHORS ONLY. Only run-anchored uploads queue by default, only their
    # ops carry the `run_ref` that `drain` scopes on, and only their `anchor_id`
    # is already resolved -- a project or workspace anchor_id here is still a
    # SLUG (`_anchor_id_for` runs later) while the queued op stored a uuid, so
    # the comparison could never match and bought a full queue parse to find
    # nothing, on exactly the anchors this change made always-synchronous.
    if anchor is not Anchor.RUN or not anchor_id:
        return
    try:
        journal = _journal()
        colliding = [
            op
            for queue in journal.namespaces()
            for _, op in queue.pending()
            if (op.get("upload") or {}).get("name") == name
            and (op.get("upload") or {}).get("anchor") == anchor.value
            and (op.get("upload") or {}).get("anchor_id") == anchor_id
            and op.get("run_ref")
        ]
        if not colliding:
            return
        # Scope the drain to the runs those ops belong to. Machine-wide flush is
        # deliberately not used: 747d2a46 removed it from this very path because
        # it dragged a neighbour's whole backlog through one artifact upload.
        from ..sdk.journal import drain

        # wait_for_lock=False: the default BLOCKS on the drain flock until the
        # background worker finishes its whole pass, and a blocked wait is not an
        # exception, so the `except` below would never see it -- an ordering
        # courtesy could hang the upload it exists to precede. Under
        # async-by-default a run's queue routinely holds thousands of ops.
        for run_scope in {op["run_ref"] for op in colliding}:
            drain(journal, run_ref=run_scope, wait_for_lock=False)
    except Exception:  # noqa: BLE001 -- ordering is a courtesy, the upload is the job
        pass


# -- bulk import (--from-manifest) ------------------------------------------
#
# WHY THIS EXISTS. One `probe artifact add` per file costs one Python process
# start, one network slug->id resolution, and -- when an agent is driving -- one
# model turn. At 200k files that is 20-45 CPU-hours before a single byte moves,
# and the resolution traffic is 200k requests for what is one answer. A manifest
# collapses all three: ONE process, ONE resolution per distinct anchor, N rows
# journalled to the outbox for the drainer to deliver.

#: Keys a manifest row may carry. Each is the flag of the same name on
#: `artifact add`, so a row and a command line mean exactly the same thing.
#:
#: An unrecognised key FAILS the row rather than being ignored. A manifest is
#: generated, not typed, so `"file"` where `"path"` was meant is the realistic
#: mistake -- and silently ignoring it enqueues nothing while reporting success,
#: which is the one outcome a bulk importer must never produce.
_MANIFEST_KEYS = frozenset(
    {
        "path",
        "uri",
        "name",
        "notes",
        "kind",
        "step",
        "span",
        "content_type",
        "meta",
        "reference",
        "hash",
        "allow_missing",
        "run",
        "project",
        "experiment",
        "workspace",
        "shared",
    }
)

#: Above this size a manifest row is RECORDED rather than uploaded, unless the
#: row says otherwise. Same constant and same reasoning as the snapshot path: a
#: checkpoint or a dataset shard already sits on a shared volume, and copying
#: tens of GB per row to re-store what is already there is duplication, not
#: reproducibility.
_MANIFEST_REFERENCE_OVER_BYTES = _SNAPSHOT_REFERENCE_OVER_BYTES


def _manifest_field(row: dict, key: str, want: type | tuple[type, ...], label: str):
    """One row field, type-checked. A generated manifest gets types wrong (a
    stringified step, a list where a map belongs) and the error is far more
    useful here than as a 422 the drainer swallows hours later."""
    value = row.get(key)
    if value is None or isinstance(value, want):
        return value
    raise typer.BadParameter(f"{key!r} must be {label}, got {type(value).__name__}")


def _manifest_rows(path: str):
    """Yield ``(lineno, row, error)`` for every non-blank line of a JSONL file.

    Blank lines are skipped and not counted -- a trailing newline is not a row.
    """
    with open(path, encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, 1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                yield lineno, None, f"not JSON: {exc}"
                continue
            if not isinstance(row, dict):
                yield lineno, None, "each line must be a JSON object"
                continue
            yield lineno, row, None


def _plan_manifest_row(
    row: dict,
    *,
    default_anchor: tuple[Anchor, str | None] | None,
    reference_over: int,
) -> dict:
    """Turn one row into the arguments :func:`_artifact_enqueue` takes.

    Deterministic and network-free, so the validation pass and the enqueue pass
    agree without carrying every parsed row in memory. Raises
    :class:`typer.BadParameter` for anything wrong with the row; the caller
    records that against the line number and moves to the next one.
    """
    unknown = sorted(set(row) - _MANIFEST_KEYS)
    if unknown:
        raise typer.BadParameter(
            f"unknown key(s): {', '.join(unknown)}. A row takes {', '.join(sorted(_MANIFEST_KEYS))}"
        )

    row_anchor = any(
        row.get(key) is not None for key in ("run", "project", "experiment", "workspace")
    ) or bool(row.get("shared"))
    if row_anchor:
        anchor, anchor_ref = _pick_anchor(
            run=_manifest_field(row, "run", str, "a string"),
            project=_manifest_field(row, "project", str, "a string"),
            experiment=_manifest_field(row, "experiment", str, "a string"),
            workspace=_manifest_field(row, "workspace", str, "a string"),
            shared=bool(row.get("shared")),
        )
    elif default_anchor is not None:
        anchor, anchor_ref = default_anchor
    else:
        raise typer.BadParameter(
            "needs an anchor: a run/project/experiment/workspace/shared key on the "
            "row, or --project/--experiment/--workspace/--shared on the command"
        )

    path = _manifest_field(row, "path", str, "a string")
    uri = _manifest_field(row, "uri", str, "a string")
    kind = _manifest_field(row, "kind", str, "a string") or "file"
    step = _manifest_field(row, "step", int, "an integer")
    span = _manifest_field(row, "span", str, "a string")
    meta = _manifest_field(row, "meta", dict, "an object")
    # Through _manifest_field like every other key. `bool(row.get(k))` accepted
    # the string "false" as True -- a realistic generator error, since the prompt
    # shows the value as a bare `true|false` token -- and silently recorded a
    # file as a pointer whose bytes are never uploaded.
    reference = bool(_manifest_field(row, "reference", bool, "true or false"))
    hash_content = bool(_manifest_field(row, "hash", bool, "true or false"))
    allow_missing = bool(_manifest_field(row, "allow_missing", bool, "true or false"))
    # A RELATIVE path in a manifest row defaults to being the name, because it
    # IS the structure: `backfill.py` states the contract the dashboard depends
    # on -- "the name is the file's relative path and nothing else", and the
    # folder tree is built by splitting it on '/'. Defaulting to the basename
    # would flatten a whole import into one directory and collide every
    # `config.yaml` in it.
    #
    # An ABSOLUTE path falls back to the basename. It describes where a file
    # sits on the machine that wrote the manifest, which is not a name anyone
    # wants in a dashboard and leaks a local layout into shared data.
    default_name = path if (path and not os.path.isabs(path)) else None
    name = _validate_artifact_row(
        anchor,
        path=path,
        uri=uri,
        name=_manifest_field(row, "name", str, "a string") or default_name,
        reference=reference,
        hash_content=hash_content,
        allow_missing=allow_missing,
        kind=kind,
        step=step,
        span=span,
        meta=meta,
    )

    # A code row is stored, not pointed at, whatever "reference" said. Applied
    # here as well as on the command line because that is this function's whole
    # contract: a rule enforced on one and not the other is discovered a hundred
    # thousand rows later. No per-row print -- the summary reports modes.
    reference = _reference_after_code_check(
        kind, reference=reference, path=path, allow_missing=allow_missing
    )

    if reference:
        if not allow_missing and not os.path.exists(path):
            raise typer.BadParameter(
                f"cannot reference {path!r}: no such file. Set "
                '"allow_missing": true on the row to record it anyway '
                "(e.g. it lives on a mount this host does not see)"
            )
    elif uri is None:
        if not path:
            raise typer.BadParameter('needs "path" (or "reference", or "uri")')
        if not os.path.isfile(path):
            raise typer.BadParameter(f"{path} is not a regular file")
        # Big files are RECORDED, not copied -- see _MANIFEST_REFERENCE_OVER_BYTES.
        # Never for a workspace/Shared row: those anchors have no reference form
        # at all (a file IS its bytes), so promoting one would turn a legal row
        # into an illegal one behind the caller's back.
        #
        # Never for a CODE row either. Size is why a checkpoint is recorded
        # rather than copied; it is not a reason to point at code, and without
        # this a large code row demoted above would be promoted straight back
        # into the reference this rule exists to prevent.
        if (
            anchor not in _FILE_ANCHORS
            and not _is_code_kind(kind)
            and os.path.getsize(path) >= reference_over
        ):
            reference = True

    return {
        "anchor": anchor,
        "anchor_ref": anchor_ref,
        "name": name,
        "path": path,
        "uri": uri,
        "reference": reference,
        "hash_content": hash_content,
        "allow_missing": allow_missing,
        "kind": kind,
        "step": step,
        "span": span,
        "content_type": _manifest_field(row, "content_type", str, "a string"),
        "meta": meta,
        "notes": _manifest_field(row, "notes", str, "a string"),
    }


class _AnchorFailure:
    """A cached anchor-resolution failure.

    Cached for the same reason a success is: a manifest naming one bad project
    slug on every row would otherwise pay one failing round trip per row -- the
    exact cost this command exists to remove, incurred on the error path where
    nobody is measuring it.
    """

    def __init__(self, message: str) -> None:
        self.message = message


def _artifact_add_manifest(
    manifest: str,
    *,
    default_anchor: tuple[Anchor, str | None] | None,
    reference_over: int,
) -> None:
    """Enqueue every row of a JSONL manifest. See the block comment above.

    Two passes over the FILE, not over a list of parsed rows: validation must
    happen before any bytes are staged, and holding 200k parsed rows in memory to
    achieve that trades one resource problem for another. Re-parsing JSON is
    cheap next to the snapshot each row is about to cost. That is also why the
    manifest is a path and not stdin -- a stream cannot be read twice.
    """
    failures: dict[int, dict] = {}
    anchors: dict[tuple[Anchor, str], str | None | _AnchorFailure] = {}
    total = 0

    def fail(lineno: int, message: str) -> None:
        failures[lineno] = {"line": lineno, "error": message}

    # -- pass 1: parse, validate, resolve each distinct anchor exactly once ---
    client: Client | None = None
    try:
        for lineno, row, error in _manifest_rows(manifest):
            total += 1
            if error is not None:
                fail(lineno, error)
                continue
            try:
                plan = _plan_manifest_row(
                    row, default_anchor=default_anchor, reference_over=reference_over
                )
            except ClickException as exc:
                fail(lineno, exc.format_message())
                continue
            except (OSError, ValueError) as exc:
                fail(lineno, str(exc))
                continue

            anchor, ref = plan["anchor"], plan["anchor_ref"]
            if anchor not in _SLUG_ANCHORS or not ref:
                continue
            key = (anchor, ref)
            if key not in anchors:
                if client is None:
                    client = _client()
                try:
                    anchors[key] = _anchor_id_for(client, anchor, ref)
                except Exception as exc:  # noqa: BLE001 -- recorded, not raised
                    anchors[key] = _AnchorFailure(str(exc))
            resolved = anchors[key]
            if isinstance(resolved, _AnchorFailure):
                fail(lineno, resolved.message)
    finally:
        if client is not None:
            client.close()

    # -- pass 2: journal the rows that survived -----------------------------
    enqueued = {"upload": 0, "reference": 0}
    if total > len(failures):
        with _async_client() as c:
            for lineno, row, error in _manifest_rows(manifest):
                if error is not None or lineno in failures:
                    continue
                # Guarded, exactly as pass 1 is. The file list is re-planned
                # here, and a shared research drive is LIVE -- a file deleted
                # between the two passes is the normal case, not a race. Letting
                # BadParameter escape aborted the command at exit 2, abandoning
                # every remaining row and never printing the summary.
                try:
                    plan = _plan_manifest_row(
                        row, default_anchor=default_anchor, reference_over=reference_over
                    )
                except (typer.BadParameter, OSError) as exc:
                    fail(lineno, str(exc))
                    continue
                anchor, ref = plan.pop("anchor"), plan.pop("anchor_ref")
                anchor_id = ref
                if anchor in _SLUG_ANCHORS and ref:
                    anchor_id = anchors[(anchor, ref)]
                name = plan.pop("name")
                try:
                    result = _artifact_enqueue(c, anchor, anchor_id, name, ping=False, **plan)
                except ClickException as exc:
                    fail(lineno, exc.format_message())
                except (OSError, errors.RosError, ValueError) as exc:
                    fail(lineno, str(exc))
                else:
                    if result["mode"] not in enqueued:
                        # "refused"/"unstaged" are row FAILURES, not counters.
                        # _enqueue_upload swallows the OSError this `except` used
                        # to catch, so without this a full spool became a
                        # KeyError that aborted a 200k-row import with no summary.
                        fail(
                            lineno,
                            result.get("unstaged_reason")
                            or "could not be queued (the outbox is not writable)",
                        )
                    else:
                        enqueued[result["mode"]] += 1
        _kick_drainer()

    # Machine-readable and on stdout, because the caller is a script: counts,
    # then every row that did NOT land, with its line number and why. Only the
    # failures are enumerated -- a success list is one line per file, which at
    # manifest scale is a second copy of the manifest nobody asked for.
    _print_json(
        {
            "manifest": manifest,
            "rows": total,
            "enqueued": sum(enqueued.values()),
            "uploads": enqueued["upload"],
            "references": enqueued["reference"],
            "failed": len(failures),
            "anchors_resolved": len(anchors),
            "failures": [failures[line] for line in sorted(failures)],
        }
    )
    if failures:
        # Non-zero so an automated caller notices, AFTER the summary is printed:
        # the whole point is that the good rows landed and these ones did not.
        raise typer.Exit(1)


@artifact_app.command("add")
def artifact_add(
    run: str = typer.Argument(None, help="run id — omit when using an anchor flag"),
    path: str = typer.Argument(None, help="local file to upload"),
    uri: str = typer.Option(None, "--uri", help="record a reference to an existing object"),
    name: str = typer.Option(
        None,
        "--name",
        help="the file's relative path (defaults to its basename). The file's "
        "extension is kept whatever you pass — say what the file IS with --notes",
    ),
    kind: str = typer.Option(
        None,
        "--kind",
        help="run anchor only; default: `plot` for an image (png, jpg, svg, gif, webp), "
        "else `file`",
    ),
    step: int = typer.Option(None, "--step", help="run anchor only"),
    span: str = typer.Option(None, "--span", help="associate with a run span UUID"),
    content_type: str = typer.Option(None, "--content-type"),
    meta: list[str] = typer.Option(None, "--meta", metavar="k=v", help="run anchor only"),
    notes: str = typer.Option(
        None,
        "--notes",
        help="what this file is, what produced it, what it shows — any anchor",
    ),
    project: str = typer.Option(None, "--project", help="anchor to a project slug (or id:<uuid>)"),
    experiment: str = typer.Option(
        None, "--experiment", help="anchor to an experiment slug (or id:<uuid>)"
    ),
    workspace: str = typer.Option(
        None,
        "--workspace",
        help="anchor to a workspace slug (or id:<uuid>) — a file, not an artifact",
    ),
    shared: bool = typer.Option(False, "--shared", help="put it in the team Shared folder"),
    write_mode: Optional[bool] = write_mode_opt(),
    reference: bool = typer.Option(
        False,
        "--reference",
        help="record the file's PATH as a reference (file://) instead of uploading its "
        "bytes — for large files on a shared volume the agent resolves locally",
    ),
    hash_content: bool = typer.Option(
        False,
        "--hash",
        help="also fingerprint a --reference (reads the whole file; enables dedup)",
    ),
    allow_missing: bool = typer.Option(
        False,
        "--allow-missing",
        help="record a --reference even if the path is not visible from this host",
    ),
    from_manifest: str = typer.Option(
        None,
        "--from-manifest",
        metavar="FILE",
        help="bulk import: one JSON object per line, each the row form of these "
        "flags. ONE process, one anchor resolution, N files queued",
    ),
    reference_over: int = typer.Option(
        _MANIFEST_REFERENCE_OVER_BYTES,
        "--reference-over",
        metavar="BYTES",
        help="--from-manifest only: at or over this size a row is RECORDED as a "
        "reference instead of uploaded",
    ),
) -> None:
    """Record an artifact against a run, project, experiment, workspace, or Shared.

    With a path and no --uri/--reference the real upload runs (fingerprint -> presign ->
    PUT -> confirm). With --reference the file's PATH is recorded (file://, bytes NOT
    uploaded) — for a 16GB checkpoint or a shared-volume file an agent resolves locally.
    With --uri it records a reference to an object already in a bucket. References are
    run/project/experiment only — a workspace/Shared file *is* its bytes.

    CODE IS THE EXCEPTION: --kind code/script/source (and the code_bytes /
    code_snapshot kinds the snapshot writes) is always uploaded, never referenced.
    Passing --reference with one of those uploads the bytes and says so; if they
    are not readable from this host it is an error rather than a pointer. A script
    is small, and a pointer to it stops resolving the moment the box or the
    checkout goes away.

    --from-manifest FILE imports many files in one go. Each line is a JSON object
    whose keys are these flags: "path", "name", "uri", "notes", "kind", "step",
    "span", "content_type", "meta", "reference", "hash", "allow_missing", and an
    anchor ("run"/"project"/"experiment"/"workspace"/"shared"). A row without an
    anchor uses the one on the command line. Every distinct anchor is resolved
    ONCE. Rows are queued to the outbox and delivered by the drainer, whether or
    not --async is set — that is the point of the verb. A bad row is reported
    with its line number and does not stop the rest; the summary is JSON on
    stdout and the exit code is non-zero if anything failed.
    """
    if from_manifest is not None:
        if run is not None or path is not None:
            raise typer.BadParameter(
                "--from-manifest takes its rows from the file; drop the positional arguments"
            )
        if write_mode is not None:
            # Refuse rather than ignore: --sync is what someone reaches for when
            # they need the write to have LANDED, and this path always queues.
            raise typer.BadParameter(
                "--from-manifest always queues to the outbox; --async/--sync do not "
                "apply. Use `probe outbox status` to confirm delivery"
            )
        if name is not None or uri is not None or reference:
            raise typer.BadParameter(
                "--name/--uri/--reference are per-ROW in a manifest, not flags. Set "
                "them on the JSON objects instead"
            )
        default_anchor = None
        if project or experiment or workspace or shared:
            default_anchor = _pick_anchor(
                run=None,
                project=project,
                experiment=experiment,
                workspace=workspace,
                shared=shared,
            )
        _artifact_add_manifest(
            from_manifest,
            default_anchor=default_anchor,
            reference_over=reference_over,
        )
        return

    anchored = project or experiment or workspace or shared
    if anchored:
        # With an anchor flag there is no RUN, so the single positional is the path.
        # Shifting here (rather than guessing from the value) keeps `add ./f.bin` and
        # `add RUN ./f.bin` both unambiguous.
        if path is not None:
            # Two positionals means the caller passed RUN *and* an anchor flag. Catch
            # it here: after the shift below `run` is always None, so _pick_anchor's
            # two-anchor check can no longer see the RUN and the id would be silently
            # reinterpreted as a file path (an unhandled FileNotFoundError).
            raise typer.BadParameter(
                "an artifact anchors to exactly one thing; got RUN and an anchor flag. "
                "Drop the RUN argument, or drop the flag."
            )
        path, run = run, None

    anchor, anchor_id = _pick_anchor(
        run=run, project=project, experiment=experiment, workspace=workspace, shared=shared
    )
    if kind is None:
        # The SDK's default, so one PNG is a `plot` whichever door it came in by.
        # Only a run artifact has a kind; every other anchor's contract is `file`.
        kind = artifact_kind_for(name or "", path or uri) if anchor is Anchor.RUN else "file"

    resolved = _validate_artifact_row(
        anchor,
        path=path,
        uri=uri,
        name=name,
        reference=reference,
        hash_content=hash_content,
        allow_missing=allow_missing,
        kind=kind,
        step=step,
        span=span,
        meta=meta,
    )

    was_reference = reference
    reference = _reference_after_code_check(
        kind, reference=reference, path=path, allow_missing=allow_missing
    )
    if was_reference and not reference:
        # Say it out loud on the single-file path: the caller typed --reference
        # and is getting an upload, and a behaviour change nobody is told about
        # is how the next person concludes the flag is broken.
        typer.echo(
            f"--kind {kind} is stored, not referenced: uploading {path} instead of "
            "recording its path.",
            err=True,
        )

    # QUEUE ONLY WHERE A BARRIER EXISTS. `run end` is the one command that
    # verifies delivery, and it drains by run_ref -- so a project-, experiment-,
    # workspace- or shared-anchored upload has no command in anyone's workflow
    # that would force it out. Those anchors keep failing loudly at the moment of
    # the write instead of queueing into a window nothing closes.
    #
    # An explicit --async still opts any anchor in: this changes the DEFAULT, and
    # `probe --async artifact add --project ...` worked yesterday.
    #
    # Costs almost nothing: `_artifact_add_manifest` returned above, so the
    # 200k-file bulk path is already always-queued and untouched either way. What
    # stays synchronous is the single-file non-run add, which is rare by nature.
    effective_mode = _resolve_write_mode(write_mode)
    if effective_mode is None and anchor is not Anchor.RUN:
        effective_mode = False
    # Build a client here ONLY when queueing is actually on the table. A client
    # opened just to be asked "are you async?" and then closed is wasteful in
    # production and wrong under test, where `Client` is monkeypatched to one
    # shared object: closing it closed the very client the synchronous path
    # below then tried to use ("Cannot send a request, as the client has been
    # closed"). `_sync` never reaches this at all.
    with _queue_client_if_possible(effective_mode) as queue_client:
        # An explicit --async is a COMMAND, so it does not get second-guessed by
        # reading the client back; `_async_client` has already refused if nothing
        # could drain the journal. Only the unforced case asks what was resolved.
        if queue_client is not None and (effective_mode is True or queue_client.async_writes):
            if anchor in _SLUG_ANCHORS:
                # Only reachable via an explicit --async now that _SLUG_ANCHORS
                # (project/experiment/workspace) no longer take the default.
                #
                # A queued write must not carry a raw slug into the journal: the
                # drainer POSTs it minutes later, an unresolved slug becomes a 422
                # nobody is watching, and an id/slug collision files the upload
                # against the wrong project with no operator present. Sync and
                # async have to agree on what a ref means.
                #
                # One bounded indexed lookup, and free offline -- _anchor_id_for
                # passes an unresolvable ref straight through rather than gating.
                with _client() as c:
                    anchor_id = _anchor_id_for(c, anchor, anchor_id)
            if _artifact_add_async(
                queue_client,
                anchor,
                anchor_id,
                resolved,
                path=path,
                uri=uri,
                reference=reference,
                hash_content=hash_content,
                allow_missing=allow_missing,
                kind=kind,
                step=step,
                span=span,
                content_type=content_type,
                meta=_kv_pairs(meta) if meta else None,
                notes=notes,
            ):
                return
            # Nothing was queued -- staging was refused, or the outbox could not
            # be written. Fall through and upload synchronously: this process is
            # now the only writer, which is exactly why the enqueue side had to
            # leave no op behind.

    # Every path that reaches the server DIRECTLY passes through here: --sync, a
    # credential-degraded session, a non-run anchor, and the fallback above.
    # Order against anything already queued for this same name before writing.
    _drain_colliding_uploads(anchor, anchor_id, resolved)

    if anchor is Anchor.RUN:
        with _client() as c:
            row = _run_handle(c, anchor_id).log_artifact(
                resolved,
                path=path,
                uri=uri,
                reference=reference,
                hash_content=hash_content,
                allow_missing=allow_missing,
                kind=kind,
                step_index=step,
                span_id=span,
                content_type=content_type,
                meta=_kv_pairs(meta) if meta else None,
                notes=notes,
            )
        upload = (row.get("meta") or {}) if isinstance(row, dict) else {}
        if upload.get("upload") == "failed":
            # The SDK does not raise for a refused or failed upload: it records
            # a pointer and carries on, which is right in a training loop and a
            # lie at a prompt. `(delivered)` and exit 0 read as "the bytes are
            # stored" to every script and agent that runs this command.
            typer.echo(
                f"error: not uploaded ({upload.get('upload_error') or 'the upload failed'}); "
                "a pointer was recorded",
                err=True,
            )
            raise typer.Exit(1)
        word = _UNDELIVERED.word()
        print(f"artifact {resolved!r} recorded on {anchor_id} ({word})")
        return
    with _client() as c:
        anchor_id = _anchor_id_for(c, anchor, anchor_id)
        if reference:
            fields = reference_fields(path, hash_content=hash_content, allow_missing=allow_missing)
            body = {"name": resolved, "is_reference": True, **fields}
            if content_type:
                body["content_type"] = content_type
            if notes:
                body["notes"] = notes
            _print_json(c.create_anchored_reference(anchor, anchor_id, body))
        elif uri is not None:
            body = {"name": resolved, "uri": uri, "is_reference": True}
            if content_type:
                body["content_type"] = content_type
            if notes:
                body["notes"] = notes
            _print_json(c.create_anchored_reference(anchor, anchor_id, body))
        else:
            if not path:
                raise typer.BadParameter("needs a file path (--reference, or --uri)")
            _print_json(
                c.upload_file(
                    anchor,
                    anchor_id,
                    resolved,
                    path,
                    content_type=content_type,
                    notes=notes,
                )
            )


@artifact_app.command("set")
def artifact_set(
    artifact_id: str = typer.Argument(..., metavar="{artifact}", help="artifact id (id:<uuid> or the bare uuid)"),
    notes: str = typer.Option(..., "--notes", help="what this file is, what produced it, what it shows"),
) -> None:
    """Give a file that has no notes yet its one-line note.

    Only an EMPTY note is written here, so nobody's words are replaced; to change
    notes that already exist, `probe notes checkout --artifact <id>`, edit, and
    `probe notes push --artifact <id>`, which merges."""

    artifact = artifact_id.removeprefix("id:")
    with _client() as c:
        row = c.transport.get(f"/v1/artifacts/{artifact}")
        current = (row or {}).get("notes") or ""
        if current.strip():
            if current.strip() == notes.strip():
                _print_json({"id": artifact, "notes": current, "unchanged": True})
                return
            typer.echo(
                "this file already has notes; edit them with `probe notes checkout --artifact "
                f"{artifact}` and `probe notes push --artifact {artifact}`",
                err=True,
            )
            raise typer.Exit(2)
        base = int((row or {}).get("notes_version") or 0)
        _print_json(c._replace_notes("artifact", artifact, notes, base_version=base, op_key=uuid.uuid4().hex))


@artifact_app.command("move")
def artifact_move(
    artifact_id: str = typer.Argument(
        ..., help="artifact id — artifacts have no slug, so this is a UUID"
    ),
    to: AnchorLevel = typer.Option(
        ...,
        "--to",
        help="the level to move it to: run | experiment | project",
    ),
    target: str = typer.Option(
        None,
        "--target",
        metavar="REF",
        help="the entity at --to to land on: a slug, id:<uuid>, or a run petname. "
        "Omit to PROMOTE up this artifact's own chain, where the target follows "
        "from where it already hangs",
    ),
) -> None:
    """Move an artifact to another level, keeping its id.

    Promote up (``--to`` above where it hangs now) needs no ``--target``: the
    destination follows from the artifact's own run -> experiment -> project
    chain. Demoting down needs ``--target``, because a project has many
    experiments and only the caller knows which. A lateral move — one project to
    another — is the same call with ``--to project --target OTHER``.

    WHAT THIS COMMAND DOES NOT DO is decide which of those the server allows.
    The rules live in one place, server-side, and they are moving: lateral is
    landing on the backend now. A client-side copy of them would either reject a
    move the server has just started accepting, or invent a reason of its own for
    one it refuses. So the level and the target go straight through, and a 422 or
    409 is printed exactly as the server worded it.
    """
    with _client() as c:
        target_id = None
        if target is not None:
            if to is AnchorLevel.run:
                target_id = refs.resolve_run(c, target).id
            else:
                target_id = refs.resolve(c, to.value, target).id
        _print_json(c.move_artifact(artifact_id, level=to.value, target_id=target_id))


@artifact_app.command("list")
def artifact_list(
    run: str = typer.Argument(None, help="run id — omit when using an anchor flag"),
    kind: str = typer.Option(None, "--kind", help="run anchor only"),
    step_from: int = typer.Option(None, "--step-from", help="run anchor only"),
    step_to: int = typer.Option(None, "--step-to", help="run anchor only"),
    project: str = typer.Option(None, "--project"),
    experiment: str = typer.Option(None, "--experiment"),
    workspace: str = typer.Option(None, "--workspace"),
    shared: bool = typer.Option(False, "--shared"),
) -> None:
    """List artifacts under an anchor. Run listing is server-filtered by step window."""
    anchor, anchor_id = _pick_anchor(
        run=run, project=project, experiment=experiment, workspace=workspace, shared=shared
    )
    with _client() as c:
        if anchor is Anchor.RUN:
            _print_json(
                c.list_run_artifacts(
                    # UUID-typed route, same as `span list` -- and the run anchor is
                    # the one anchor whose ref is normally typed as a petname.
                    _ref(c, "run", anchor_id).id,
                    kind=kind,
                    step_from=step_from,
                    step_to=step_to,
                )
            )
            return
        if kind or step_from is not None or step_to is not None:
            raise typer.BadParameter(
                f"--kind/--step-from/--step-to are run-only filters; "
                f"the {anchor.value} listing does not accept them"
            )
        _print_json(c.list_anchored(anchor, _anchor_id_for(c, anchor, anchor_id)))


@artifact_app.command("tree")
def artifact_tree(
    run: str = typer.Argument(..., help="run id or petname"),
    prefix: str = typer.Option("", "--prefix", help="folder path; empty is the root"),
    limit: int | None = typer.Option(
        None, "--limit", help="files/folders per level (server max 1000); `truncated` says if cut"
    ),
) -> None:
    """One folder level of a run's artifacts: the files at that path plus each
    child folder with its file count. What the explorer fetches on expand, so a
    run with thousands of captured files costs one small answer per folder."""
    with _client() as c:
        _print_json(c.list_run_artifact_tree(_ref(c, "run", run).id, prefix=prefix, limit=limit))


@artifact_app.command("download")
def artifact_download(
    artifact_id: str = typer.Argument(..., help="artifact id (from `probe artifact list`)"),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        "--to",
        metavar="PATH",
        help="write the bytes here; '-' forces stdout. Omit to write to stdout "
        "(refused at a terminal).",
    ),
    sha256: str = typer.Option(
        None,
        "--sha256",
        metavar="HEX",
        help="expected content_hash; fail (deleting a written file) if the bytes differ",
    ),
    version: int = typer.Option(
        None,
        "--version",
        metavar="N",
        help="fetch this version's bytes instead of the artifact's live content "
        "(from `probe artifact versions`)",
    ),
) -> None:
    """Download an artifact's bytes through a presigned GET.

    To a PATH it streams straight to the file -- never buffering the whole blob,
    which can be model weights -- and prints {dest, size_bytes, sha256}. To stdout it
    buffers in memory so the hash can be checked before a byte is emitted. Pass
    --sha256 to verify the round trip against the content_hash from
    `probe artifact list`; a metadata match alone never proves the blob exists.

    --version resolves a pin: it fetches that exact version's bytes, which is what a
    reproduction needs, rather than whatever the name points at today."""
    to_stdout = output is None or output == "-"
    if to_stdout and output is None and sys.stdout.isatty():
        raise typer.BadParameter(
            "refusing to write binary to a terminal; pass -o PATH, or '-o -' / a "
            "redirect to force stdout"
        )
    with _client() as c:
        try:
            if to_stdout:
                data = (
                    c.download_artifact_version(artifact_id, version)
                    if version is not None
                    else c.download_artifact(artifact_id)
                )
                digest = hashlib.sha256(data).hexdigest()
                if sha256 and digest != sha256:
                    typer.echo(
                        f"sha256 mismatch: expected {sha256}, got {digest} ({len(data)} bytes)",
                        err=True,
                    )
                    raise typer.Exit(1)
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
                typer.echo(f"{artifact_id}  {len(data)} bytes  sha256={digest}", err=True)
                return
            # download_artifact*_to removes its own partial file on a mid-stream failure.
            result = (
                c.download_artifact_version_to(artifact_id, version, output)
                if version is not None
                else c.download_artifact_to(artifact_id, output)
            )
            if sha256 and result["sha256"] != sha256:
                Path(output).unlink(missing_ok=True)
                typer.echo(
                    f"sha256 mismatch: expected {sha256}, got {result['sha256']}; deleted {output}",
                    err=True,
                )
                raise typer.Exit(1)
            _print_json(result)
        except errors.RosError as exc:
            # A reference has no managed blob to download; the server 409s with the
            # pointer so we can show the path instead of the raw error. Read it from
            # where it lives (e.g. the shared volume) -- Probe stores no bytes for it.
            detail = exc.detail if isinstance(exc.detail, dict) else {}
            status = getattr(exc, "status", None)
            # A force-deleted version answers 410 WITH who/when, so a reproduction can
            # tell "deliberately destroyed" apart from "never existed". Say which.
            if status == 410 and version is not None:
                when = detail.get("deleted_at") or "(unknown time)"
                who = detail.get("deleted_by")
                typer.echo(
                    f"artifact {artifact_id} version {version} was deleted at {when}"
                    + (f" by {who}" if who else "")
                    + "\nThe version record survives; its bytes do not.",
                    err=True,
                )
                raise typer.Exit(2)
            if status != 409 or detail.get("reason") != "reference":
                raise
            where = detail.get("local_path") or detail.get("uri") or "(unknown location)"
            host = detail.get("host")
            what = f"artifact {artifact_id}" + (
                f" version {version}" if version is not None else ""
            )
            typer.echo(
                f"{what} is a reference -> {where}"
                + (f" on {host}" if host else "")
                + "\nProbe stores no bytes for it; read it from that path.",
                err=True,
            )
            raise typer.Exit(2)


@artifact_app.command("versions")
def artifact_versions(
    artifact_id: str = typer.Argument(..., help="artifact id (from `probe artifact list`)"),
) -> None:
    """List an artifact's version chain.

    An artifact is a named thing in a container; this is the content history behind
    that name. `origin` says how each version got its bytes: `uploaded` (pushed
    directly) or `pinned` (promoted zero-copy from another artifact). Immutability is
    a property of the version, not the artifact -- renaming or moving the artifact
    never breaks a pin."""
    with _client() as c:
        _print_json(c.list_artifact_versions(artifact_id))


@artifact_app.command("pin-impact")
def artifact_pin_impact(
    artifact_id: str = typer.Argument(..., help="artifact id (from `probe artifact list`)"),
) -> None:
    """Show which projects and experiments pin this artifact's versions.

    Run this before deleting anything: it reports the actual work that would break,
    not a count. `pinned: false` means nothing published depends on it."""
    with _client() as c:
        _print_json(c.artifact_pin_impact(artifact_id))


@artifact_app.command("version-add")
def artifact_version_add(
    artifact_id: str = typer.Argument(..., help="the artifact to append a version to"),
    from_artifact: str = typer.Option(
        None,
        "--from-artifact",
        metavar="ID",
        help="promote another artifact's content ZERO-COPY: pins its hash, uri and "
        "size; the stored object is shared, never re-uploaded",
    ),
    uri: str = typer.Option(
        None, "--uri", help="name the pointer directly instead of promoting an artifact"
    ),
    sha256: str = typer.Option(None, "--sha256", metavar="HEX", help="content_hash for --uri"),
    size_bytes: int = typer.Option(None, "--size-bytes"),
    content_type: str = typer.Option(None, "--content-type"),
    label: str = typer.Option(
        None, "--label", help="an alternate selector for this version (e.g. 'prod')"
    ),
) -> None:
    """Append the next version of an artifact.

    Exactly one source: --from-artifact (zero-copy promotion) or --uri. Appending
    content identical to the artifact's current live content is a no-op that returns
    the existing version, so this is safe to retry."""
    if bool(from_artifact) == bool(uri):
        raise typer.BadParameter("pass exactly one of --from-artifact or --uri")
    with _client() as c:
        _print_json(
            c.create_artifact_version(
                artifact_id,
                from_artifact_id=from_artifact,
                uri=uri,
                content_hash=sha256,
                size_bytes=size_bytes,
                content_type=content_type,
                label=label,
            )
        )


@artifact_app.command("delete")
def artifact_delete(
    artifact_id: str = typer.Argument(..., help="artifact id (no by-name index; ids only)"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
) -> None:
    """PERMANENTLY delete an artifact. Irreversible."""
    _confirmed_delete(
        "artifact",
        artifact_id,
        yes=yes,
        cascade="its stored bytes and version history go with it",
    )


@artifact_app.command("gc-uploads")
def artifact_gc_uploads(
    older_than: str = typer.Option(
        ...,
        "--older-than",
        metavar="TIMESTAMP",
        help="sweep uploads started before this; must carry a timezone, e.g. 2026-07-01T00:00:00Z",
    ),
) -> None:
    """Sweep abandoned (never-confirmed) uploads. Confirmed artifacts are untouched."""
    with _client() as c:
        _print_json(c.gc_uploads(older_than))


# -- shared folder ----------------------------------------------------------
shared_app = typer.Typer(no_args_is_help=True, help="the team's Shared folder")
app.add_typer(shared_app, name="shared")


@shared_app.command("list")
def shared_list() -> None:
    """List the team's Shared files."""
    with _client() as c:
        _print_json(c.list_anchored(Anchor.SHARED))


@shared_app.command("add")
def shared_add(
    path: str = typer.Argument(..., help="local file to upload"),
    name: str = typer.Option(None, "--name", help="defaults to the file's basename"),
    content_type: str = typer.Option(None, "--content-type"),
) -> None:
    """Upload a file straight into the team's Shared folder."""
    resolved = name_with_extension(name or os.path.basename(path), path)
    with _client() as c:
        _print_json(c.upload_file(Anchor.SHARED, None, resolved, path, content_type=content_type))


@shared_app.command("share")
def shared_share(
    artifact_id: str = typer.Argument(..., help="a workspace file id"),
    replace: bool = typer.Option(
        False, "--replace", help="supersede a same-named file already in Shared"
    ),
) -> None:
    """Move one of your workspace files into the team's Shared folder.

    A MOVE, not a copy: the file leaves your workspace listing. Ownership transfers
    and the search index is re-keyed in the same transaction.

    A name already taken in Shared is a 409 — the server never silently supersedes
    someone else's file. Pass --replace to do it deliberately.
    """
    with _client() as c:
        _print_json(c.share_workspace_file(artifact_id, replace=replace))


@shared_app.command("unshare")
def shared_unshare(
    artifact_id: str = typer.Argument(..., help="a shared file id"),
    replace: bool = typer.Option(
        False, "--replace", help="supersede a same-named file in the default workspace"
    ),
) -> None:
    """Move a Shared file into the server default workspace."""
    with _client() as c:
        _print_json(c.unshare_file(artifact_id, replace=replace))


@shared_app.command("download")
def shared_download(
    artifact_id: str = typer.Argument(..., help="a shared file id"),
) -> None:
    """Print a presigned download URL for a Shared file."""
    with _client() as c:
        _print_json(c.download_shared_file(artifact_id))


@shared_app.command("delete")
def shared_delete(
    artifact_id: str = typer.Argument(..., help="a shared file id"),
) -> None:
    """Remove a file from the Shared folder (soft delete; recoverable)."""
    with _client() as c:
        c.delete_shared_file(artifact_id)
    print(f"shared file {artifact_id} deleted")


# -- Trials: the entity, and the Harbor capture that produces them ------------
#
# ONE GROUP, two halves, and they are not parallel. `stage/add/reconcile/export/
# drain/watch/expand` CAPTURE trials out of a Harbor sandbox; `list/get/set` read
# and author the rows that capture produced (research-os 0135). They share a noun
# because they are the same noun -- a second `probe rollout` group would have made
# a researcher learn which word this lab uses for the thing they are looking at,
# and the dashboard already answered that question with "trial".
trial_app = typer.Typer(
    no_args_is_help=True, help="rollout trials: read and author them, and capture Harbor's"
)
app.add_typer(trial_app, name="trial")


@trial_app.command("list")
def trial_list(
    run: str = run_ref(),
    limit: int = typer.Option(None, "--limit", help="rows per page (server max 200)"),
    cursor: str = typer.Option(None, "--cursor", help="continue from a previous page"),
) -> None:
    """List a run's trials, newest step first.

    This is the AUTHORED inventory, not `probe span list --type rollout`: the
    span is what the producer emitted and the trial is the row beside it that
    holds a title, a description and a note. A trial also survives outside a
    bounded span slice, so this finds ones a span listing reports as absent.
    """
    with _client() as c:
        page = c.list_run_trials(_ref(c, "run", run).id, cursor=cursor, limit=limit)
    _print_json({"trials": page.items, "next_cursor": page.next_cursor})


@trial_app.command("get")
def trial_get(
    trial_id: str = typer.Argument(..., help="the trial's rollout span id"),
    fields: str = _FIELDS_OPTION,
) -> None:
    """Show one trial.

    The id is the ROLLOUT SPAN id -- the last segment of a dashboard
    `/runs/<run>/trials/<id>` link, so a URL a teammate pasted works here
    unedited. `probe trial list` is where it comes from otherwise.
    """
    with _client() as c:
        _print_json(_select_fields(c.get_trial(trial_id), fields))


@trial_app.command("set")
def trial_set(
    trial_id: str = typer.Argument(..., help="the trial's rollout span id"),
    name: str = typer.Option(None, "--name"),
    description: str = description_opt(),
) -> None:
    """Give one trial a human title and/or a description.

    Both are STICKY once set: the producer keeps writing its own benchmark name
    on every retry and will not overwrite yours. That is the point of the verb --
    a rollout worth talking about gets a name a person can say, instead of the
    Harbor join key it was born with.

    NO `--notes` here, and there is no notes door for a trial anywhere: it is
    the one research entity with no notes document. A rollout ran once and is
    immutable afterwards, so what went wrong in it goes in `--description`, and
    anything about the harness belongs once on the RUN's notes.
    """
    if name is None and description is None:
        raise typer.BadParameter("pass at least one of --name/--description")
    with _client() as c:
        _print_json(c.update_trial(trial_id, name=name, description=_text_value(description)))


def _trial_result_summary(result: dict) -> dict:
    manifest = result.get("manifest") or {}
    return {
        "trial": result["trial"],
        "span_id": result["span_id"],
        "reward": result["reward"],
        "manifest_artifact_id": manifest.get("id") if isinstance(manifest, dict) else None,
        "files": len(result["files"]),
        "uploaded": sum(1 for item in result["files"] if item.get("uploaded")),
        "trajectory": result.get("trajectory"),
        "capture": result.get("capture"),
    }


@trial_app.command("stage")
def trial_stage(
    trial_dir: str = typer.Argument(..., help="live Harbor trial output directory"),
    destination: str = typer.Option(
        ..., "--to", help="durable destination outside the sandbox (for example a shared PVC)"
    ),
    expect: list[str] = typer.Option(
        None, "--expect", metavar="RELATIVE_PATH", help="repeatable required producer output"
    ),
) -> None:
    """Copy + checksum Harbor's host trial output; performs no network writes."""
    from ..connectors.harbor import stage_trial

    staged = stage_trial(trial_dir, destination, expected_paths=expect or ())
    _print_json(
        {
            "trial_dir": str(staged.trial_dir),
            "ledger": str(staged.ledger.path),
            "durable_collection_complete": staged.durable_collection_complete,
            "completeness": staged.ledger.report(),
        }
    )
    if not staged.durable_collection_complete:
        raise typer.Exit(2)


@trial_app.command("add")
def trial_add(
    run: str = typer.Argument(...),
    trial_dir: str = typer.Argument(..., help="a Harbor trial output directory"),
    step: int = typer.Option(
        None, "--step", help="training step / Miles rollout_id — the join key"
    ),
    env_type: str = typer.Option(
        None, "--env-type", help="opaque environment label (e.g. skypilot-fork)"
    ),
    expand: bool = typer.Option(
        True, "--expand/--no-expand", help="expand a recognized trajectory format into spans"
    ),
    max_spans: int = typer.Option(
        None, "--max-spans", help="eager expansion window (0 = unlimited)"
    ),
) -> None:
    """Capture one Harbor trial: rollout span + reward metric + labeled file
    uploads + a kind=harbor_trial manifest, all keyed by --step."""
    from ..connectors.harbor import capture_trial

    with _client() as c:
        result = capture_trial(
            _run_handle(c, run),
            trial_dir,
            step_index=step,
            environment={"type": env_type} if env_type else None,
            source_mode="cli",
            expand=expand,
            max_trajectory_spans=max_spans,
        )
    _print_json(_trial_result_summary(result))


@trial_app.command("reconcile")
def trial_reconcile(
    run: str = typer.Argument(...),
    trial_dir: str = typer.Argument(..., help="a directory created by `probe trial stage`"),
    step: int = typer.Option(None, "--step", help="override the step recorded in the ledger"),
    env_type: str = typer.Option(None, "--env-type", help="opaque environment label"),
) -> None:
    """Retry unconfirmed staged bytes and publish the latest completeness manifest."""
    from ..connectors.harbor import reconcile_staged_trial

    kwargs: dict[str, Any] = {
        "environment": {"type": env_type} if env_type else None,
        "source_mode": "cli-reconcile",
    }
    if step is not None:
        kwargs["step_index"] = step
    with _client() as client:
        result = reconcile_staged_trial(_run_handle(client, run), trial_dir, **kwargs)
    _print_json(_trial_result_summary(result))


@trial_app.command("export")
def trial_export(
    request: str = typer.Argument(..., help="a probe-harbor-export/1 export-request.json"),
    run: Optional[str] = typer.Option(None, "--run", help="later-resolved Probe run ID"),
) -> None:
    """Consume one durable Miles/Harbor export request; retry safe."""
    from ..connectors.harbor_export import consume_export_request

    try:
        with _client() as client:
            result = consume_export_request(client, request, run_id=run)
    except Exception as exc:
        typer.echo(f"export failed (staged bytes retained): {type(exc).__name__}: {exc}", err=True)
        raise typer.Exit(1) from exc
    _print_json(result)


@trial_app.command("drain")
def trial_drain(
    capture_root: str = typer.Argument(..., help="root containing export-request.json files"),
    run: Optional[str] = typer.Option(None, "--run", help="later-resolved Probe run ID"),
) -> None:
    """Retry every non-completed Miles/Harbor export request below a capture root."""
    from ..connectors.harbor_export import drain_export_requests

    with _client() as client:
        result = drain_export_requests(client, capture_root, run_id=run)
    _print_json(result)
    if result["failed"]:
        raise typer.Exit(2)


@trial_app.command("watch")
def trial_watch(
    capture_root: str = typer.Argument(..., help="root containing export-request.json files"),
    interval: float = typer.Option(5.0, "--interval", min=0.1, help="poll interval in seconds"),
    once: bool = typer.Option(False, "--once", help="drain once and exit (deployment smoke check)"),
    run: Optional[str] = typer.Option(None, "--run", help="later-resolved Probe run ID"),
) -> None:
    """Continuously export newly staged Harbor trials from a durable capture root."""
    from ..connectors.harbor_export import drain_export_requests
    from ._watch import watch

    with _client() as client:
        watch(
            lambda: drain_export_requests(client, capture_root, run_id=run),
            interval=interval,
            once=once,
            report=_print_json,
        )


@trial_app.command("expand")
def trial_expand(
    run: str = typer.Argument(...),
    manifest_id: str = typer.Argument(..., help="a kind=harbor_trial manifest artifact id"),
    max_spans: int = typer.Option(
        0, "--max-spans", help="eager expansion window (default 0 = full)"
    ),
) -> None:
    """Retroactively expand a captured trial's stored trajectory into spans —
    e.g. after a parser for its format shipped. Idempotent (deterministic span
    ids), so re-running only upserts."""
    from ..connectors.atif import expand_trajectory

    with _client() as c:
        manifests = {a["id"]: a for a in c.list_run_artifacts(run, kind="harbor_trial")}
        manifest = manifests.get(manifest_id)
        if manifest is None:
            typer.echo(f"no kind=harbor_trial artifact {manifest_id} on run {run}", err=True)
            raise typer.Exit(1)
        meta = manifest.get("meta") or {}
        traj_entry = next(
            (
                f
                for f in meta.get("files") or []
                if f.get("role") == "trajectory" and f.get("artifact_id")
            ),
            None,
        )
        if traj_entry is None:
            typer.echo("manifest has no uploaded trajectory file", err=True)
            raise typer.Exit(1)
        doc = json.loads(c.transport.get_url(c.presign_download(traj_entry["artifact_id"])))
        report = expand_trajectory(
            _run_handle(c, run),
            doc,
            root_span_id=str(manifest["span_id"]),
            trial=(meta.get("trial") or {}).get("name") or manifest.get("name"),
            step_index=manifest.get("step_index"),
            max_spans=max_spans,
        )
    _print_json(report)


# -- link / snapshot / flush / reads ----------------------------------------
@app.command()
def link(
    run: str = typer.Argument(...),
    set_pairs: list[str] = typer.Option(..., "--set", metavar="k=v"),
) -> None:
    """Attach foreign keys (stored under metadata.foreign_keys)."""
    keys = _kv_pairs(set_pairs)
    with _client() as c:
        _run_handle(c, run).link(**keys)
    print(f"linked {', '.join(keys)} to {run}")


@app.command()
def snapshot(
    run: str = typer.Argument(...),
    cwd: str = typer.Option(None, "--cwd"),
    venv: str = typer.Option(
        None, "--venv", help="virtualenv to record; auto-detected from --cwd otherwise"
    ),
    no_env: bool = typer.Option(False, "--no-env"),
    no_gpu: bool = typer.Option(False, "--no-gpu"),
    no_upload: bool = typer.Option(
        False, "--no-upload", help="do NOT store the bytes git cannot supply"
    ),
    max_upload_mb: int = typer.Option(
        256, "--max-upload-mb", help="refuse (never truncate) above this size"
    ),
    include: list[str] = typer.Option(
        None,
        "--include",
        metavar="GLOB",
        help="also capture paths git ignores (datasets, checkpoints, out-of-tree configs)",
    ),
    reference_over_mb: int = typer.Option(
        100,
        "--reference-over-mb",
        help="above this, record where a file lives instead of copying it",
    ),
) -> None:
    """Non-disruptive code + env capture.

    Every captured file has its BYTES stored as an artifact row on the run (one per
    file, deduped by content; `PROBE_CODE_STORAGE=archive` stores one `code-bytes`
    archive instead), because a sha256 verifies a file you already have rather
    than producing one you do not.
    Files a pushed remote could supply are uploaded too: git referencing is retired,
    since a pointer that outlives its remote is indistinguishable from a live one.
    `--no-upload` skips the upload, and the run is then not reproducible from the
    record alone.

    The exception is size. Above `--reference-over-mb` a file's path, host and
    sha256 are recorded instead of copied — a base checkpoint is not duplicated
    into every run of a sweep. The commit and remote are still recorded, as
    provenance no byte depends on.

    The dependency set comes from the PROJECT's virtualenv, not this CLI's. `probe`
    is normally a uv-tool install with its own interpreter, so recording the
    packages of the process you are reading this from would describe typer and rich
    rather than torch and transformers.
    """
    with _client() as c:
        snap = _run_handle(c, run).snapshot(
            cwd=cwd,
            include_env=not no_env,
            include_gpu=not no_gpu,
            venv=venv,
            # The CLI is never the process that runs the code.
            detect_venv=True,
            upload=not no_upload,
            max_upload_bytes=max_upload_mb * 1024 * 1024,
            include=list(include) if include else None,
            reference_over_bytes=reference_over_mb * 1024 * 1024,
        )
    m = snap["manifest"]
    cb = snap.get("code_bytes") or {}
    g = snap.get("git")
    if g:
        # Provenance only: read, never written (no shadow ref since plan 2.6).
        head = (g.get("head") or "")[:12] or "no commits yet"
        dirty = ", uncommitted changes" if g.get("dirty") else ""
        print(f"snapshot of {g.get('branch') or 'detached HEAD'} @ {head}{dirty}")
    else:
        print(f"snapshot (no git repo) — {len(m['entries'])} files")
    if snap.get("git_error"):
        print(f"      git unreadable ({snap['git_error']}); captured as a plain directory")
    skipped = m.get("skipped") or []
    if skipped:
        # A COUNT, never a path or a value -- naming it `secrets` made CodeQL
        # read the printed integer as the credential itself, and it read that
        # way to humans too. Printed with or without git: a skip inside a repo
        # (a withheld config, a tracked `.env`) is no less a gap in the record.
        n_credential_shaped = sum(1 for s in skipped if s["reason"] == "secret")
        n_content = sum(1 for s in skipped if s.get("found_in") == "content")
        n_slow = sum(1 for s in skipped if s.get("found_in") == "scan_time")
        note = f", {n_credential_shaped} credential-shaped" if n_credential_shaped else ""
        if n_content:
            note += f", {n_content} withheld for their content"
        if n_slow:
            note += f", {n_slow} withheld: scan ran out of time"
        print(f"      skipped {len(skipped)} paths (excluded by policy{note})")
    base = m["base_commit"][:12] if m["base_commit"] else "no pushed base"
    # The count that used to lead this line was `n_git_referenced` -- files
    # NOT captured, printed as if they were. It is structurally 0 now, so say
    # what is in the record instead, and keep the commit as the provenance it is.
    print(f"code: {len(m['entries'])} files, provenance {base}")
    if cb.get("uploaded") and cb.get("storage") == "artifacts":
        print(
            f"      {cb['n_files']} stored as files ({cb.get('n_uploaded', 0)} uploaded, "
            f"{cb.get('n_deduped', 0)} already held)"
        )
        if cb.get("pending_upload"):
            names = ", ".join(f"{u['path']} ({u['reason']})" for u in cb.get("unstored") or [])
            print(f"      {cb['pending_upload']} NOT stored: {names}")
    elif cb.get("uploaded"):
        print(
            f"      {cb['n_files']} uploaded ({cb['size_bytes'] / 1e6:.2f} MB, "
            f"{cb['archive_sha256'][:12]})"
        )
        if cb.get("pending_upload"):
            names = ", ".join(cb.get("drifted") or [])
            print(
                f"      {cb['pending_upload']} NOT stored (changed or vanished during "
                f"capture): {names}"
            )
    elif cb.get("pending_upload"):
        print(
            f"      {cb['pending_upload']} NOT stored ({cb.get('reason')}) — "
            "this run is not reproducible from the record alone"
        )
    for e in m.get("entries") or []:
        if e.get("source") == "reference":
            print(
                f"      referenced (too large to copy): {e['path']}  "
                f"{e['size'] / 1e6:.0f} MB on {e.get('host')}"
            )
    deps = snap.get("deps") or {}
    prov = snap.get("env_provenance") or {}
    if deps.get("packages") is not None:
        source = prov.get("venv") or prov.get("python_executable")
        print(
            f"env: {deps['package_count']} packages, python {deps['python']}"
            f" ({prov.get('resolved_via')}: {source})"
        )
    elif prov.get("resolved_via") == _UNRESOLVED_FALLBACK:
        # Loud, because the alternative to a wrong dependency list is an ABSENT
        # one, and absence that prints nothing is how a run reaches the record
        # looking captured. Says what to do, not just what happened.
        print(
            "env: NOT captured — no virtualenv found for this project, and this "
            f"CLI's own interpreter ({prov.get('python_executable')}) is outside "
            "it. Recording its packages would describe the CLI, not the "
            "experiment. Pass --venv PATH, or activate the environment the code "
            "runs in, then re-run `probe snapshot`.",
            file=sys.stderr,
        )


def _snapshot_ref_verdicts(refs: list[tuple[str, str]]) -> dict[str, str | None]:
    """ref -> None when its run's code is stored on Probe (safe to delete), else
    why the ref is kept.

    A shadow commit may be the only copy of a dirty tree whose upload failed
    (D10). The run's `code_snapshot` row records how many files never reached
    Probe (`meta.n_pending_upload`, what SURVIVED the upload), so only a row
    that says 0 lets its ref go. No row, a row without the count, a ref name
    that is not a run id, or a run this account cannot see all keep the ref: an
    unknown is not a zero.
    """
    import uuid

    from ..sdk.errors import NotFoundError, ScopeError, ValidationError
    from ..sdk.snapshot import SNAPSHOT_REFS_PREFIX

    verdicts: dict[str, str | None] = {}
    ids: dict[str, str] = {}
    for ref, _sha in refs:
        run_id = ref[len(SNAPSHOT_REFS_PREFIX) :]
        try:
            ids[ref] = str(uuid.UUID(run_id))
        except ValueError:
            verdicts[ref] = "not a run id, so its upload cannot be checked"
    if not ids:
        return verdicts
    try:
        c = _client()
    except Exception as exc:  # noqa: BLE001 -- no credentials is an answer, not a crash
        return verdicts | {ref: f"could not check its upload ({type(exc).__name__})" for ref in ids}
    stop: str | None = None
    with c:
        for ref, run_id in ids.items():
            if stop:
                verdicts[ref] = stop
                continue
            try:
                rows = c.list_run_artifacts(run_id, kind="code_snapshot") or []
            except (NotFoundError, ScopeError, ValidationError):
                verdicts[ref] = "run not found under this account, so its upload cannot be checked"
                continue
            except Exception as exc:  # noqa: BLE001 -- offline, auth, 5xx: stop asking
                stop = f"could not check its upload ({type(exc).__name__})"
                verdicts[ref] = stop
                continue
            rows = rows.get("items", rows) if isinstance(rows, dict) else rows
            counts = [(r.get("meta") or {}).get("n_pending_upload") for r in rows]
            ints = [n for n in counts if isinstance(n, int) and not isinstance(n, bool)]
            if not rows:
                verdicts[ref] = "no code-snapshot record on Probe: its upload may never have landed"
            elif any(n > 0 for n in ints):
                verdicts[ref] = f"{max(ints)} file(s) of its code never reached Probe"
            elif len(ints) != len(counts):
                verdicts[ref] = "its code-snapshot record predates upload accounting"
            else:
                verdicts[ref] = None
    return verdicts


@app.command("snapshot-prune-refs")
def snapshot_prune_refs(
    cwd: str = typer.Option(".", "--cwd", help="a directory inside the repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="list the refs and what would happen; delete nothing"),
    bundle: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--bundle",
        help="back every ref up to this git bundle (outside the repo) first, then delete them all",
    ),
    force: bool = typer.Option(
        False, "--force", help="also delete refs whose run's upload is unfinished or could not be checked"
    ),
) -> None:
    """Delete the `refs/probe/snapshots/*` refs earlier Probe versions wrote.

    Each is a shadow commit of the working tree at a run's start, untracked files
    included (a `.env` among them), and `git push --mirror` publishes them. Probe
    no longer writes them (plan 2.6) and never deletes them on its own (D10).

    One may be the only copy of a dirty tree whose upload failed, so by default
    a ref is deleted only when its run's code-snapshot record on Probe says every
    file was stored; the rest are kept and listed with the reason. `--bundle
    FILE` backs every ref up first and then deletes them all; `--force` deletes
    them all as they are. Every line prints `<ref> <sha>`: `git update-ref <ref>
    <sha>` restores one until git's gc removes the objects, and `git fetch FILE
    'refs/probe/snapshots/*:refs/probe/snapshots/*'` restores from a bundle.
    """
    from ..sdk.snapshot import (
        SnapshotError,
        _repo_check,
        bundle_snapshot_refs,
        old_snapshot_refs,
        prune_snapshot_refs,
    )

    in_repo, reason = _repo_check(cwd)
    if not in_repo:
        # git's own reason (no git binary, "dubious ownership"), not a guess.
        print(
            f"error: {reason or os.path.abspath(cwd) + ' is not inside a git repository'}",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    refs = old_snapshot_refs(cwd)
    if not refs:
        print("no refs/probe/snapshots/* refs in this repository")
        return
    # A bundle is the backup, so with one every ref may go unchecked.
    verdicts = {} if (force or bundle) else _snapshot_ref_verdicts(refs)
    doomed = [(ref, sha) for ref, sha in refs if verdicts.get(ref) is None]
    kept = [(ref, sha, verdicts[ref]) for ref, sha in refs if verdicts.get(ref) is not None]
    go, stay = ("would delete", "would keep") if dry_run else ("deleted", "kept")
    if not dry_run:
        try:
            if bundle:
                bundle_snapshot_refs(cwd, [ref for ref, _ in refs], bundle)
                print(
                    f"backed up {len(refs)} ref(s) to {bundle}; restore with "
                    f"git fetch {bundle} 'refs/probe/snapshots/*:refs/probe/snapshots/*'"
                )
            prune_snapshot_refs(cwd, doomed)
        except SnapshotError as exc:
            print(f"error: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
    for ref, sha in doomed:
        print(f"{go} {ref} {sha}")
    for ref, sha, why in kept:
        print(f"{stay} {ref} {sha}  ({why})")
    summary = f"{go} {len(doomed)} ref(s)"
    if kept:
        summary += (
            f"; {stay} {len(kept)} whose code may exist nowhere else. `--bundle FILE` "
            "backs them up and deletes them; `--force` deletes them as they are"
        )
    print(summary + (" (dry run; nothing changed)" if dry_run else ""))
    if doomed and not dry_run:
        print(
            "Undo one with `git update-ref <ref> <sha>` (each line above) until git's gc "
            "removes the objects, which for old refs can be the next automatic gc."
        )
    if kept and not dry_run:
        raise typer.Exit(1)


@app.command("snapshot-show")
def snapshot_show(
    run: str = typer.Argument(...),
    pending_only: bool = typer.Option(False, "--pending-only"),
) -> None:
    """Print a run's captured code manifest, one file per line.

    `git` files are retrievable with `git cat-file blob <blob>` from the recorded
    remote; `blob` files are the ones git cannot supply, stored as the run's
    per-file capture rows ("captured") or in its `code-bytes` archive (runs captured
    before 0193, with `PROBE_CODE_STORAGE=archive`, or against a server without the
    batch doors).

    `--pending-only` means GENUINELY UNAVAILABLE, not `source == "blob"`. The
    manifest's `n_pending_upload` is a CLASSIFICATION count -- "git cannot supply
    this, someone must upload it" (sdk.snapshot.capture_manifest says so in as
    many words) -- and it is frozen into the execution record at capture, before
    the upload it is counting. Reading it as work-remaining is what made this
    command report 6 files pending on a run whose code-bytes archive held all six
    and whose restore verified every one of them. What the upload actually did is
    recorded on the `code-snapshot` artifact, so that is what this reconciles
    against.
    """
    with _client() as c:
        # One read for both: `list_run_artifacts` is UUID-typed, and the handle
        # already resolved a petname to get here.
        data = _run_handle(c, run).data
        record = c.transport.get(f"/v1/execution-records/{data['env_ref']}")
        # A run captured by an older SDK, or one whose upload genuinely failed,
        # has no code-bytes row -- and that is exactly the case where "pending"
        # is the true answer rather than a stale label.
        row = _code_bytes_row(c, str(data["id"]))
        capture = _capture_rows(c, str(data["id"]))
    # Two ways bytes can be stored. Per-file capture rows (0193) name every
    # file they hold by (path, sha256) and only a `complete` row is stored.
    # The archive names what it holds (`meta.paths`): a run whose tree drifted
    # during capture stores most files and lists the rest as unstored, so
    # "there is an archive" is not "every file is in it". An older row with no
    # `paths` key predates that accounting and holds everything (None = all).
    stored_files = {(r.get("name"), r.get("content_hash")) for r in capture}
    listed = (row.get("meta") or {}).get("paths") if row else None
    stored_paths = set(listed) if listed is not None else None
    manifest = ((record or {}).get("code") or {}).get("manifest") or {}
    entries = manifest.get("entries") or []
    print(f"base_commit {manifest.get('base_commit')}  remote {manifest.get('remote')}")
    print(f"tree_sha256 {manifest.get('tree_sha256')}")
    classified = 0
    n_stored = 0
    n_files = 0
    for e in entries:
        source = e.get("source")
        is_blob = source == "blob"
        classified += is_blob
        as_file = is_blob and ((wire_name(e.get("path") or ""), e.get("sha256")) in stored_files)
        in_archive = (
            is_blob and bool(row) and (stored_paths is None or e.get("path") in stored_paths)
        )
        stored = as_file or in_archive
        n_stored += stored
        n_files += as_file
        if pending_only and not (is_blob and not stored):
            continue
        if source == "git":
            # Legacy: manifests captured before git referencing was retired.
            ref = e.get("blob", "-")
        elif source == "reference":
            # NOT in code-bytes and not awaiting upload -- it was deliberately
            # left where it lives. Printing "code-bytes" here (which is what the
            # old else-branch did) claimed Probe held bytes it has never held.
            ref = f"offsite on {e.get('host', '?')}"
        elif source == "withheld":
            # Held a credential at capture: never uploaded, and small ones carry
            # no sha256 (it could be brute-forced back to a password).
            ref = f"withheld ({e.get('reason', 'secret')})"
        else:
            ref = "captured" if as_file else ("code-bytes" if stored else "needs-upload")
        print(f"  {source:<9} {ref:<40} {(e.get('sha256') or '')[:12]} {e.get('path')}")
    n_git = manifest.get("n_git_referenced", 0)
    n_offsite = sum(1 for e in entries if e.get("source") == "reference")
    where = (
        "as files"
        if n_files and n_files == n_stored
        else (
            f"{n_files} as files, {n_stored - n_files} in code-bytes"
            if n_files
            else "in code-bytes"
        )
    )
    summary = f"{n_stored} stored {where}, {classified - n_stored} pending upload"
    if n_offsite:
        summary += f", {n_offsite} referenced offsite"
    if n_git:
        summary += f", {n_git} git-referenced (legacy)"
    print(summary)


def _capture_rows(c: Client, run_id: str) -> list[dict]:
    """The run's complete per-file capture rows (0193); see sdk.restore."""
    from ..sdk.restore import capture_rows

    return capture_rows(c, run_id)


def _code_bytes_row(c: Client, run_id: str) -> dict | None:
    """The run's uploaded `code-bytes` archive, or None if its bytes never landed.

    Same read `_restore_captured_tree` does before it can rebuild anything, and
    the same normalisation: `list_run_artifacts` answers a bare list on some
    routes and a paged object on others.
    """
    rows = c.list_run_artifacts(run_id, kind="code_bytes") or []
    rows = rows.get("items", rows) if isinstance(rows, dict) else rows
    # A fail-open upload failure leaves a REFERENCE row pointing at a tmp file
    # the SDK deleted; that is a pointer, not stored bytes.
    rows = [r for r in rows if not r.get("is_reference")]
    return rows[0] if rows else None


def _restore_captured_tree(
    c: Any, run_id: str, env_ref: str, dest: str, *, verify_only: bool = False
) -> dict:
    """Rebuild a run's captured working tree into ``dest`` from its execution
    record's code manifest plus the run's per-file capture rows and/or its uploaded ``code-bytes`` archive.

    Shared by ``snapshot-restore`` and ``run reproduce --materialize`` so both fetch,
    verify, and write bytes exactly one way — every file is checked against the
    sha256 the manifest recorded, and a mismatch is reported UNAVAILABLE rather than
    written. Lockfiles ride in the tree here; they are not written from the reproduce
    record's `lockfiles` list, which carries path+sha256 for VISIBILITY, not bytes.
    Returns the ``restore_snapshot`` result dict.
    """
    from ..sdk.restore import restore_snapshot

    record = c.transport.get(f"/v1/execution-records/{env_ref}")
    manifest = ((record or {}).get("code") or {}).get("manifest") or {}

    # Per-file capture rows (0193) AND the code-bytes archive, whichever the
    # run holds: a file is taken from the rows first, then from the archive, so
    # a run snapshotted under both storages (the default flip, a partial
    # capture re-run as an archive) restores every byte Probe has.
    from ..sdk.restore import capture_blob_fetch

    rows = _capture_rows(c, run_id)
    blob_fetch = (
        capture_blob_fetch(c, rows, warn=lambda m: print(m, file=sys.stderr)) if rows else None
    )

    archive = None
    tmp = None
    row = _code_bytes_row(c, run_id)
    if row:
        tmp = tempfile.NamedTemporaryFile(prefix="probe-code-", suffix=".tar.gz", delete=False)
        tmp.close()
        try:
            c.download_artifact_to(row["id"], tmp.name)
            archive = tmp.name
        except Exception as exc:  # noqa: BLE001 -- reported per file by restore_snapshot
            print(f"warning: could not download code-bytes: {exc}", file=sys.stderr)

    try:
        return restore_snapshot(
            manifest, dest, archive_path=archive, blob_fetch=blob_fetch, verify_only=verify_only
        )
    finally:
        if tmp is not None:
            try:
                os.unlink(tmp.name)
            except OSError:
                pass


@app.command("snapshot-restore")
def snapshot_restore(
    run: str = typer.Argument(...),
    dest: str = typer.Argument(None, help="directory to rebuild into; omit with --verify-only"),
    verify_only: bool = typer.Option(
        False, "--verify-only", help="resolve and hash everything, write nothing"
    ),
) -> None:
    """Rebuild a run's captured working tree, or say exactly what is missing.

    Files git can supply are fetched from the recorded remote; the rest come from
    the run's per-file capture rows, then from its `code-bytes` archive when one
    exists. Every file is verified against the sha256
    the manifest recorded — a mismatch is reported UNAVAILABLE and never written,
    so this cannot hand back a tree that only looks right.

    Exits non-zero if any file could not be produced.
    """
    if not verify_only and not dest:
        raise typer.BadParameter("DEST is required unless --verify-only is passed")

    with _client() as c:
        handle = _run_handle(c, run)
        env_ref = handle.data.get("env_ref")
        if not env_ref:
            print(f"error: run {run} has no execution record to restore", file=sys.stderr)
            raise typer.Exit(1)
        result = _restore_captured_tree(c, handle.id, env_ref, dest or ".", verify_only=verify_only)

    for f in result["files"]:
        if f["status"] == "unavailable":
            print(f"  MISSING {f['path']}  ({f['reason']})")
    for r in result.get("referenced") or []:
        print(f"  OFF-PLATFORM {r['path']}  -> {r['uri']} on {r['host']}")
    verb = "verified" if verify_only else "restored"
    ref = (
        f", {result['n_referenced']} referenced off-platform" if result.get("n_referenced") else ""
    )
    print(f"{result['n_restored']} {verb}, {result['n_unavailable']} unavailable{ref}")
    print(f"tree_sha256 {result['tree_sha256']} matches={result['tree_matches']}")
    if result["n_unavailable"]:
        raise typer.Exit(1)


# -- outbox (the async write journal) ---------------------------------------
outbox_app = typer.Typer(no_args_is_help=True, help="the durable async write outbox")
app.add_typer(outbox_app, name="outbox")


def _fold_drain_reports(parts: list) -> Any:
    """One report for `drain --all`. One journal's comes back untouched; for
    more, EVERY field folds -- counts add, flags OR, lists merge without
    repeats, sets and dicts merge, an optional value keeps its first -- so a
    field a later change adds to `DrainReport` (#2041's ``credential_held`` and
    ``held_reasons``) reaches the output instead of being dropped by a copy of
    the six this command used to know."""
    import dataclasses

    if len(parts) == 1:
        return parts[0]
    combined = type(parts[0])()
    for part in parts:
        for spec in dataclasses.fields(combined):
            mine, theirs = getattr(combined, spec.name), getattr(part, spec.name)
            if theirs is None:
                continue
            if isinstance(theirs, bool):
                setattr(combined, spec.name, mine or theirs)
            elif isinstance(theirs, set):
                setattr(combined, spec.name, (mine or set()) | theirs)
            elif spec.default is None:
                # Optional: auth_status/auth_message/auth_context stay ONE
                # refusal's, never a mix of two.
                if mine is None:
                    setattr(combined, spec.name, theirs)
            elif isinstance(theirs, list):
                mine.extend(item for item in theirs if item not in mine)
            elif isinstance(theirs, dict):
                for key, value in theirs.items():
                    mine.setdefault(key, value)
            elif isinstance(theirs, (int, float)):
                setattr(combined, spec.name, mine + theirs)
    return combined


def _drain_foreground(run_ref: str | None = None, *, every_dir: bool = False) -> None:
    """Shared body of `probe outbox drain` and its `probe flush` alias.
    ``every_dir``: every outbox of this user on this machine (plan 1.5)."""
    from ..sdk.journal import drain, prune_credential_queues

    journals = _outbox_journals() if every_dir else [_journal()]
    parts = []
    for journal in journals:
        try:  # idle credential queues (#2041 round 3); never fails the drain
            prune_credential_queues(journal.dir)
        except Exception:  # noqa: BLE001
            pass
        part = drain(journal, run_ref=run_ref)
        parts.append(part)
        if every_dir and len(journals) > 1:
            print(
                f"{journal.dir}: delivered {part.delivered}; "
                f"{part.dead_lettered} dead-lettered; {part.remaining} remaining"
            )
    report = _fold_drain_reports(parts)
    scope = f" for run {run_ref}" if run_ref else ""
    print(
        f"delivered {report.delivered}{scope}; "
        f"{report.dead_lettered} dead-lettered; {report.remaining} remaining"
    )
    if report.credential_held or getattr(report, "close_held", 0):
        # The drain's own reasons: "another job's PROBE_TOKEN" is one of
        # several, and naming it for a re-login it cannot match misled people
        # (#2041 re-review).
        reasons = getattr(report, "held_reasons", None) or [
            "queued with a credential this shell does not have (another job's PROBE_TOKEN, "
            "or a token passed in code)"
        ]
        permanent = getattr(report, "permanently_held", 0)
        typer.echo(
            f"{report.credential_held + getattr(report, 'close_held', 0)} kept: {reasons[0]}"
            + "".join(f"\n  also: {reason}" for reason in reasons[1:])
            + (
                f"\n  ({permanent} of them no credential here will send: "
                "`probe outbox discard --held` drops those)"
                if permanent
                else ""
            ),
            err=True,
        )
    if report.auth_blocked:
        typer.echo(
            f"auth-blocked: {report.errors[-1] if report.errors else '401/403'} "
            f"— sign in again ({session_marker.WIZARD_HINT}); queued items were kept",
            err=True,
        )
    elif report.stopped_transient and report.errors:
        typer.echo(f"stopped on transient failure: {report.errors[-1]}", err=True)
    elif report.errors:
        # Dead-letter-only failures: every cause still reaches stderr.
        typer.echo(f"dead-lettered: {report.errors[-1]}", err=True)
    for message in report.errors[:-1] if report.errors else []:
        typer.echo(f"  {message}", err=True)
    if not report.clean:
        raise typer.Exit(2)


def _auth_blocked_since(status: dict) -> str | None:
    from ..sdk.journal import auth_blocked_since

    return auth_blocked_since(status)


@outbox_app.command("status")
def outbox_status(
    verbose: bool = typer.Option(False, "--verbose", help="list every queued/failed op"),
    run: Optional[str] = typer.Option(None, "--run", help="scope counts and ops to one run"),
) -> None:
    """Outbox summary. Exit 0 when everything is delivered, 2 otherwise."""
    journal = _journal()
    pending = [item for namespace in journal.namespaces() for item in namespace.pending()]
    failed = [item for namespace in journal.namespaces() for item in namespace.failed()]
    pending.sort(key=lambda item: item[1].get("enqueued_at") or "")
    if run is not None:
        pending = [(p, op) for p, op in pending if op.get("run_ref") == run]
        failed = [(p, op) for p, op in failed if op.get("run_ref") == run]
    from ..sdk.journal import Journal

    status = Journal.read_status(journal.dir) or {}
    others = _outbox_journals()[1:]
    summary = {
        "dir": str(journal.dir),
        **({"run": run} if run is not None else {}),
        "pending": len(pending),
        # Uploads queued before their credential scan: they become pending ops
        # once the worker (or `probe run end`) has scanned them.
        "waiting": len(journal.waiting(run_ref=run)),
        "failed": len(failed),
        "paused": journal.paused,
        # The queue-wide block, or a credential the drain set aside (#2041).
        "auth_blocked_since": _auth_blocked_since(status),
        "oldest_pending": pending[0][1].get("enqueued_at") if pending else None,
        "last_error": status.get("last_error"),
        # Ops the journal declined to stage because the disk was near full. They
        # still deliver -- the drainer reads the source in place -- but they now
        # depend on that source still existing at drain time, which is a fact an
        # operator should be able to see rather than infer from a dead letter.
        "unstaged_low_disk": status.get("unstaged_low_disk"),
    }
    producers = journal.producer_report()
    if producers:
        summary["producers"] = [
            {
                "producer_id": p.get("producer_id"),
                "role": p.get("role"),
                "last_sequence": p.get("last_sequence"),
                # A FLOOR, written after the op file is unlinked. Beside
                # last_sequence it answers the only question worth asking of a
                # writer that has gone away: did what it queued actually land.
                "delivered": p.get("delivered"),
                "state": p.get("state"),
                "gaps": p.get("gaps") or [],
            }
            for p in producers
        ]
    if verbose:

        def row(op: dict, state: str) -> dict:
            return {
                "op_id": op.get("op_id"),
                "state": state,
                "kind": op.get("kind"),
                "run_ref": op.get("run_ref"),
                "detail": (
                    f"{op.get('method')} {op.get('path')}"
                    if op.get("kind") == "http"
                    else (op.get("upload") or {}).get("name")
                ),
                "attempts": op.get("attempts"),
                "last_error": op.get("last_error"),
            }

        summary["ops"] = [row(op, "pending") for _, op in pending] + [
            row(op, "failed") for _, op in failed
        ]
    undelivered = bool(pending or failed or summary["waiting"])
    if others:
        # Every other outbox of this user on this machine: a distributed job's
        # `rank-*` queues and the $TMPDIR fallback used to be invisible here
        # (plan 1.5). Banner-grade counts (status.json), never a parse.
        dirs = [
            {
                "dir": str(summary["dir"]),
                "pending": summary["pending"],
                "failed": summary["failed"],
                "waiting": summary["waiting"],
            }
        ]
        for other in others:
            counts = Journal.read_status(other.dir) or {}
            dirs.append(
                {
                    "dir": str(other.dir),
                    "pending": int(counts.get("pending") or 0),
                    "failed": int(counts.get("failed") or 0),
                    "waiting": int(counts.get("waiting") or 0),
                }
            )
        summary["dirs"] = dirs
        summary["total"] = {
            key: sum(entry[key] for entry in dirs) for key in ("pending", "failed", "waiting")
        }
        undelivered = undelivered or any(summary["total"].values())
    _print_json(summary)
    if undelivered:
        raise typer.Exit(2)


@outbox_app.command("drain")
def outbox_drain(
    run: Optional[str] = typer.Option(None, "--run", help="drain only this run's ops"),
    every_dir: bool = typer.Option(
        False, "--all", help="every outbox on this machine (rank-* dirs, the $TMPDIR fallback)"
    ),
) -> None:
    """Deliver everything queued, in order, and wait for it (the sync barrier)."""
    _drain_foreground(run, every_dir=every_dir)


@outbox_app.command("watch")
def outbox_watch(
    interval: float = typer.Option(5.0, "--interval", min=0.1),
    once: bool = typer.Option(False, "--once", help="drain once and exit"),
) -> None:
    """Continuously drain the outbox in the foreground."""
    from ..sdk.journal import drain
    from ._watch import watch

    journal = _journal()

    def one_pass() -> dict:
        report = drain(journal)
        # Adapt to the shared watch contract: {"counts": {...}, "failed": [...]}.
        return {
            "counts": {"completed": report.delivered, "failed": report.dead_lettered},
            "failed": report.errors if not report.clean else [],
            "remaining": report.remaining,
            "auth_blocked": report.auth_blocked,
        }

    watch(one_pass, interval=interval, once=once, report=_print_json)


@outbox_app.command("retry")
def outbox_retry(
    op_id: Optional[str] = typer.Argument(None, help="a dead-lettered op id (omit for all)"),
    run: Optional[str] = typer.Option(None, "--run", help="requeue only this run's dead letters"),
    every_dir: bool = typer.Option(
        False, "--all", help="every outbox on this machine (rank-* dirs, the $TMPDIR fallback)"
    ),
) -> None:
    """Requeue dead-lettered op(s) and kick the drainer."""
    from ..sdk import outbox_worker

    moved = 0
    for journal in _outbox_journals() if every_dir else [_journal()]:
        moved += journal.retry_failed(op_id, run_ref=run)
        # An explicit retry is a statement that the blocker (often credentials)
        # was dealt with -- forget the auth block so the drainer spawns again.
        journal.clear_auth_block()
        if every_dir:
            try:
                outbox_worker.maybe_spawn(str(journal.dir))
            except Exception:  # noqa: BLE001 -- best-effort; `drain --all` is the barrier
                pass
    _kick_drainer()
    print(f"requeued {moved} op(s)")
    if op_id is not None and moved == 0:
        raise typer.Exit(1)


@outbox_app.command("discard")
def outbox_discard(
    op_id: Optional[str] = typer.Argument(
        None, help="a dead-lettered op id (omit to discard ALL dead letters)"
    ),
    held: bool = typer.Option(
        False,
        "--held",
        help="instead: discard queued writes no credential here will send (a login whose "
        "account is unknown or another account's, or a refused login still stored)",
    ),
    credential: Optional[str] = typer.Option(
        None,
        "--credential",
        help="with --held: also discard the queued writes of this credential fingerprint "
        "(as `probe outbox drain` prints it), e.g. a PROBE_TOKEN job that is gone",
    ),
) -> None:
    """Tombstone dead letters into discarded/ (covers quarantined-corrupt
    files retry can never requeue). Their staged bytes are freed.

    `--held` tombstones QUEUED writes instead: those no credential on this
    machine will send as things stand (`probe outbox drain` says why). Another
    job's `PROBE_TOKEN` writes are left for that job, unless `--credential`
    names that credential's fingerprint."""
    if credential is not None and not held:
        raise typer.BadParameter("--credential goes with --held")
    if held:
        if op_id is not None:
            raise typer.BadParameter("--held discards every held write; it takes no op id")
        moved = _journal().discard_held(credential=credential)
        print(f"discarded {moved} held write(s)")
        return
    moved = _journal().discard_failed(op_id)
    print(f"discarded {moved} op(s)")
    if op_id is not None and moved == 0:
        raise typer.Exit(1)


@outbox_app.command("pause")
def outbox_pause() -> None:
    """Suspend background delivery (the outbox's own switch, not the capture
    killswitch). Enqueues still work; nothing drains until `resume`."""
    _journal().pause()
    print("outbox paused")


@outbox_app.command("resume")
def outbox_resume() -> None:
    """Resume background delivery and kick the drainer."""
    journal = _journal()
    journal.resume()
    journal.clear_auth_block()
    _kick_drainer()
    print("outbox resumed")


@app.command()
def flush() -> None:
    """Deliver everything queued and wait (alias of `probe outbox drain`)."""
    _drain_foreground()


@app.command("sync")
def sync_offline(
    directory: Optional[Path] = typer.Argument(
        None,
        help="an offline run's folder, or a folder of them (e.g. copied off an "
        "air-gapped node); default: this machine's offline outbox",
    ),
    list_only: bool = typer.Option(False, "--list", help="show offline runs and their state; send nothing"),
    project: Optional[str] = typer.Option(
        None,
        "--project",
        help="file the run in this project instead of the recorded one (a run whose "
        "folder is named, or whose create was refused)",
    ),
    experiment: Optional[str] = typer.Option(
        None,
        "--experiment",
        help="file the run in this experiment instead of the recorded one (same scope as --project)",
    ),
    on_conflict: Optional[str] = typer.Option(
        None,
        "--on-conflict",
        help="`supersede`: deliver a run whose external_id another run already has as "
        "<id>-rN, a retry linked to it (same scope as --project); `error` refuses",
    ),
    allow_mismatch: bool = typer.Option(
        False,
        "--allow-mismatch",
        help="deliver a run whose folder you name even though it was recorded against "
        "another server URL, or (team unknown) under another login context",
    ),
) -> None:
    """Deliver runs recorded with PROBE_MODE=offline (plan 2.12), with the current login.

    Each run is created on the server (safe to repeat: a run synced twice, or
    from two copies of its folder, is one run), then every write it recorded,
    then its close. Looks in the outbox's `offline/` and in every torchrun/SLURM
    rank's `rank-*/offline/`. Exit 0 when everything found is synced, 2 when
    something is not, 1 when no offline run was found at all. Every write is one
    request (a 1M-step run is ~1M POSTs): the outbox's coalesced drain does not
    merge an offline run's writes yet."""
    from ..sdk import offline

    root = directory if directory is not None else (Path(_conn.spool_dir) if _conn.spool_dir else None)
    dirs = offline.find_offline_dirs(root)
    if not dirs:
        # Loud, never an empty success: a run recorded under a rank's outbox,
        # another $HOME or another machine looks exactly like "nothing to do".
        if list_only:
            _print_json([])
        places = ", ".join(str(p) for p in offline.search_places(root))
        typer.echo(
            f"probe sync: no offline runs found (looked in {places}). A run recorded "
            "on another machine or under another outbox syncs from a copy of its "
            "folder: `probe sync <dir>` (or --spool-dir / PROBE_OUTBOX_DIR).",
            err=True,
        )
        raise typer.Exit(1)
    if list_only:
        described = [offline.describe(d) for d in dirs]
        _print_json(described)
        if any(d["state"] != "synced" for d in described):
            raise typer.Exit(2)
        return
    if on_conflict is not None and on_conflict not in ("error", "supersede"):
        typer.echo("probe sync: --on-conflict takes `error` or `supersede`", err=True)
        raise typer.Exit(2)
    amending = project is not None or experiment is not None or on_conflict is not None
    # The re-filing flags change a run's identity or home, so they apply to
    # EVERY run only when DIR names that one run's folder; in a scan they fix
    # only the runs whose create the server already refused.
    named = directory is not None and len(dirs) == 1 and dirs[0] == Path(directory).expanduser()
    results = []
    with _client() as c:
        try:
            offline.require_server(c)
        except errors.CapabilityUnavailable as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(2) from None
        for d in dirs:
            try:
                results.append(
                    offline.sync_dir(
                        d,
                        c,
                        project=project,
                        experiment=experiment,
                        on_conflict=on_conflict,
                        amend_all=named,
                        # Delivering into another server or login is a choice
                        # about ONE run: never granted to a whole scan.
                        allow_mismatch=allow_mismatch and named,
                    )
                )
            except errors.RosError as exc:
                results.append({"dir": str(d), "state": "refused", "clean": False, "errors": [str(exc)]})
    _print_json(results)
    for result in results:
        for message in [*(result.get("warnings") or []), *(result.get("errors") or [])]:
            typer.echo(f"{result.get('key') or result['dir']}: {message}", err=True)
    if allow_mismatch and not named:
        typer.echo(
            "probe sync: --allow-mismatch applies only to a run whose folder you name "
            "(`probe sync <dir> --allow-mismatch`); it changed nothing here.",
            err=True,
        )
    if amending and not any(r.get("amended") for r in results):
        typer.echo(
            "probe sync: --project/--experiment/--on-conflict changed nothing: they apply to "
            "a run whose folder you name (`probe sync <dir>`), or to one whose create the "
            "server refused.",
            err=True,
        )
    if not all(r.get("clean") for r in results):
        raise typer.Exit(2)


@app.command()
def get(run: str = run_ref(), fields: str = _FIELDS_OPTION) -> None:
    """Print a run."""
    with _client() as c:
        _print_json(_select_fields(c.get_run(run), fields))


# `probe get` is a bare verb that silently means "a RUN", while every other noun
# reads with `<noun> get`. Someone who learned `project get` looks for `run get`
# and does not find it. Both spellings work now; the top-level one stays because
# it is the older habit and is in scripts.
@run_app.command("get")
def run_get(run: str = run_ref(), fields: str = _FIELDS_OPTION) -> None:
    """Show one run."""
    with _client() as c:
        _print_json(_select_fields(c.get_run(run), fields))


@app.command()
def bundle(run: str = typer.Argument(...)) -> None:
    """Print a run bundle (run + series + artifacts)."""
    with _client() as c:
        _print_json(c.run_bundle(run))


# -- the project's notes file -------------------------------------------------
# One markdown file per project, read and written as text. This replaced a
# structured `probe note` command group whose kind vocabulary
# (intent/decision/observation/...), supersession and authority field were never
# validated or grouped by anything server-side -- eight kinds bought one list filter.
# Prose is what people write; a fixed filename is the only thing that needed inventing.
notes_app = typer.Typer(
    no_args_is_help=True,
    help="notes on any entity (free-text markdown), main note and titled sub-notes",
)
app.add_typer(notes_app, name="notes")

rules_app = typer.Typer(
    no_args_is_help=True, help="the managed Probe block in your agent's memory file"
)
app.add_typer(rules_app, name="agent-rules")


@rules_app.command("refresh")
def agent_rules_refresh() -> None:
    """Rewrite the managed block when it is older than this CLI.

    THE MIGRATION CHANNEL for a file no release can reach. The block lives in the
    researcher's own CLAUDE.md or AGENTS.md, so a release that changes what the
    block should say cannot change what it does say -- every machine keeps
    instructing its agent with whatever was installed the day the wizard last
    ran.

    THE AUTOMATIC CHANNEL IS `notes sync`, not this command and not a hook. This
    docstring used to claim the session-start hook called this; it never did, in
    any shipped plugin, so bumping POINTER_VERSION corrected nothing and the
    block only ever moved when somebody ran this by hand. Wiring a hook would
    have repeated the fault it was fixing -- hooks ship in the PLUGIN, so the fix
    would reach a machine only after a plugin release AND a session restart. The
    team-note sync is CLI-side, already fires on every Stop, and already holds
    each instruction file's lock, so `refresh_pointer` rides it and lands with
    the CLI. This command stays as the explicit, inspectable path.

    THREE THINGS IT WILL NOT DO. It will not install a block into a file that
    never had one: that is the wizard's moment, with the researcher's consent,
    and a hook that adds instructions to somebody's memory file uninvited is a
    different act from keeping an existing one current. It will not touch a file
    whose markers are damaged, because the only safe response to "I cannot tell
    which bytes are mine" is to leave all of them alone. And it holds a lock
    while it works, because the block rewrite is a whole-file read-modify-write
    and several agent sessions can share one home directory.
    """
    from ..sdk.durable import file_lock
    from . import agent_rules
    from .team_note_file import instruction_lock_path

    path = agent_rules.memory_path()
    try:
        # THE SAME LOCK the note sync takes, keyed on the file. This used to
        # take a single global `agent-rules.lock` while the note sync took a
        # per-file one -- two writers of one file serialising against different
        # locks, which is no lock at all for a whole-file read-modify-write.
        with file_lock(instruction_lock_path(path)):
            installed = agent_rules.installed_version(path)
            state = agent_rules.refresh_pointer(path)
            if state != agent_rules.POINTER_REFRESHED:
                _print_json({"path": str(path), "state": state, "changed": False})
                return
            changed = True
    except agent_rules.DamagedBlock as exc:
        print(f"left {path} alone: {exc}", file=sys.stderr)
        _print_json({"path": str(path), "state": "damaged", "changed": False})
        raise typer.Exit(2) from None
    except (OSError, UnicodeDecodeError) as exc:
        print(f"could not update {path}: {exc}", file=sys.stderr)
        _print_json({"path": str(path), "state": "unwritable", "changed": False})
        raise typer.Exit(1) from None
    _print_json(
        {
            "path": str(path),
            "state": "refreshed",
            "changed": changed,
            "from_version": installed,
            "to_version": agent_rules.POINTER_VERSION,
        }
    )


def _notes_project(client: Client, project: str | None) -> tuple[str, str]:
    """(project_id, label) for a notes read/write. Explicit beats the active one."""
    resolved = _ambient_project(project, base_url=_conn.base_url)
    if not resolved:
        raise typer.BadParameter(
            "pass --project, or set an active project with `probe project use <slug>`"
        )
    return _project_id(client, resolved), _project_slug(client, resolved) or resolved


def _entity_notes_row(client: Client, kind: str, entity_id: str) -> dict:
    """The whole entity row, one explicit branch per kind — the parity check
    reads paths statically, so no f-string may compute its segment.

    Returns the ROW, not just its `notes`: the headroom pair the read advisory
    is derived from travels beside the document, and re-fetching to get it would
    double every `notes show`.
    """
    if kind == "project":
        return client.get_project(entity_id)
    if kind == "experiment":
        # The project-address read, on purpose: the experiment API's detail
        # carries the notes but not their headroom pair (`notes_limit_chars`,
        # `notes_remaining_chars`), which the read advisory and the over-cap
        # refusal below need; and an experiment's notes are still WRITTEN there
        # (`_replace_notes`) until the experiment API takes every notes verb.
        return client.get_experiment_leaf(entity_id)
    if kind == "run":
        return client.get_run(entity_id)
    if kind == "group":
        return client.get_group(entity_id)
    return client.transport.get(f"/v1/artifacts/{entity_id}")


@notes_app.command("show")
def notes_show(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
    note: str = typer.Option(
        None, "--note", help="print this titled SUB-NOTE instead (title, or id:<uuid>)"
    ),
) -> None:
    """Print an entity's notes — the main note, or one titled sub-note.

    Empty output means none were ever written. Historically project-only; the
    carrier flags arrived with sub-notes (0146) because a sub-note is reached
    through its entity and a reader should not need a different verb per kind.
    """
    with _client() as c:
        kind, entity_id, label = _note_target(
            c,
            project=project,
            experiment=experiment,
            run=run,
            group=group,
            artifact=artifact,
        )
        if note is not None:
            found = _resolve_sub_note_by_title(c, kind, entity_id, note)
            document = c.get_sub_note(found["id"])
            text = document.get("body") or None
            label = f"{label} › {note}"
        else:
            document = _entity_notes_row(c, kind, entity_id)
            text = document.get("notes")
    if text is None or text == "":
        print(f"{label} has no notes yet", file=sys.stderr)
        return
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    # STDERR, beside the document rather than inside it: stdout is the note and
    # a script pipes it. Same channel and same reasoning as the write-path
    # headroom line, which this is the READ half of.

    # A SUB-NOTE spells the headroom pair `remaining_chars`/`limit_chars` while
    # the shared reader is written against the entity spelling, so an unadapted
    # sub-note read is silently advisory-free. `_sub_note_row_for_headroom`
    # exists for exactly this and is a no-op on an entity row.
    from ..sdk.notes import read_advisory

    document = _sub_note_row_for_headroom(document)
    advisory = read_advisory(document, version=document.get("notes_version"))
    if advisory is not None:
        print(f"{label}: {advisory}", file=sys.stderr)


@notes_app.command("checkout")
def notes_checkout(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    steal: bool = typer.Option(
        False, "--steal", help="take the file even though it has unpushed edits"
    ),
) -> None:
    """Pull an entity's note to a file you can edit with ordinary tools.

    Prints the path. Edit that file the way you edit any markdown -- exact-match
    edits, not a re-typed document -- then `probe notes push`.

    The file lives in the state directory at 0600, not the working directory: a
    note keeps customer and commercial facts verbatim and a work tree is one
    `git add -A` from committing them. `push` finds it from the same
    `--run`/`--project` flag, so there is no path to remember.
    """
    from . import notes_file
    from ..sdk.config import resolve

    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run, group=group, artifact=artifact
        )
        if note is not None:
            found = _resolve_sub_note_by_title(c, kind, entity_id, note)
            row = c.get_sub_note(found["id"])
            body, version = row.get("body") or "", row.get("notes_version") or 0
            where = notes_file.paths_for(
                resolve(base_url=_conn.base_url), kind, entity_id, found["id"]
            )
            label = f"{label} \u203a {note}"
        else:
            row = _entity_notes_row(c, kind, entity_id)
            body, version = row.get("notes") or "", row.get("notes_version") or 0
            where = notes_file.paths_for(resolve(base_url=_conn.base_url), kind, entity_id)

    refusal = notes_file.claim(where, steal=steal)
    if refusal is not None:
        print(refusal, file=sys.stderr)
        raise typer.Exit(2)
    report = notes_file.checkout(where, body=body, version=version)
    print(f"checked out {kind} note ({label}) v{version}", file=sys.stderr)
    payload = {"target": kind, "label": label, "path": str(where.document), "version": version}
    if note is not None:
        # The title a script asked for, echoed back: a caller addressing a
        # sub-note needs to know WHICH document it got, and `label` glues the
        # entity and title together for humans rather than for `jq`.
        payload["note"] = note
    _print_json({**payload, **_headroom_fields(_sub_note_row_for_headroom(row))})
    # THE ADVISORY RIDES THE READ, which is the only point it can change what you
    # do. On the push it would arrive after the editing work was already done.
    # Through the SHARED reporter, so checkout says "warning:" exactly the way
    # every other notes surface does -- a second spelling of the same signal is
    # a second thing to grep for.
    _report_notes_headroom(_sub_note_row_for_headroom(row), kind, label)
    # The path is in the JSON above and on stderr below. It must NOT also go to
    # stdout as a bare line: `_print_json` exists so `probe notes checkout | jq`
    # works, and trailing text breaks exactly that.
    print(str(report.detail), file=sys.stderr)


@notes_app.command("push")
def notes_push(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    force: bool = typer.Option(
        False, "--force", help="replace the server's document without merging"
    ),
) -> None:
    """Send the checked-out file back, merging if the note moved meanwhile.

    Exit 2 means a conflict was written into the file, or there was nothing safe
    to send: resolve the markers and push again. `--force` skips the merge and
    replaces whatever is on the server -- an operator escape hatch, never a step
    in a routine, because it deletes anything written since you checked out.
    """
    from . import notes_file
    from ..sdk.config import resolve

    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run, group=group, artifact=artifact
        )
        settings = resolve(base_url=_conn.base_url)
        if note is not None:
            found = _resolve_sub_note_by_title(c, kind, entity_id, note)
            sub_id = found["id"]
            where = notes_file.paths_for(settings, kind, entity_id, sub_id)
            label = f"{label} \u203a {note}"

            def send(text, base_version, op_key):
                row = c._replace_sub_note(sub_id, text, base_version=base_version, op_key=op_key)
                return (row or {}).get("notes_version", 0)

            def fetch():
                row = c.get_sub_note(sub_id)
                return row.get("body") or "", row.get("notes_version") or 0
        else:
            where = notes_file.paths_for(settings, kind, entity_id)

            def send(text, base_version, op_key):
                row = c._replace_notes(
                    kind, entity_id, text, base_version=base_version, op_key=op_key
                )
                return (row or {}).get("notes_version", 0)

            def fetch():
                row = _entity_notes_row(c, kind, entity_id)
                return row.get("notes") or "", row.get("notes_version") or 0

        report = notes_file.push(where, send=send, fetch=fetch, label=f"{kind} note", force=force)

    _print_json(
        {
            "target": kind,
            "label": label,
            "pushed": report.pushed,
            "merged": report.merged,
            "conflicted": report.conflicted,
            "version": report.version,
            "detail": report.detail,
        }
    )
    if report.detail:
        print(f"{label}: {report.detail}", file=sys.stderr)
    if report.pushed:
        print(f"pushed {kind} note ({label}) v{report.version}", file=sys.stderr)
        return
    # Exit 2 means SOMEONE HAS TO LOOK, matching `notes sync`, which exits 2 only
    # on a conflict. Nothing-to-do ("no local edits", "nothing checked out") is a
    # clean 0: a hook that treats a no-op as a failure is worse than useless. A
    # clean local merge is also 0 -- it succeeded, and its own detail says to push
    # again.
    raise typer.Exit(2 if report.conflicted else 0)


@notes_app.command("write")
def notes_write(
    file: str = typer.Argument(None, help="file to upload; omit or '-' to read stdin"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
) -> None:
    """Replace the project's whole notes document.

    `--append` is gone with the span verbs (0.388.0.0). It sent `notes_append`,
    which the server now refuses -- a flag that always fails is worse than no
    flag. To ADD to a document without overwriting anyone, use the file model:
    `probe notes checkout` then `probe notes push`, which merges.

    This door replaces, and it carries no version, so it forces. Use it for a
    document you are authoring outright, not for adding a paragraph to one
    somebody else is also writing.
    """
    text = sys.stdin.read() if file in (None, "-") else Path(file).read_text()
    with _client() as c:
        project_id, label = _notes_project(c, project)
        # The replace verb, so the response carries the headroom this command
        # used to print only from the deleted `notes append`. It forces because
        # this door has no version in hand -- checkout/push is the one that merges.
        row = c._replace_notes(
            "project", project_id, text, base_version=None, op_key=uuid.uuid4().hex
        )
        stored = text
    print(f"wrote notes on project {label}", file=sys.stderr)
    # The stored length, not the document. Echoing the whole thing back on stdout
    # made `notes write` unpipeable and buried the one fact a caller wants, which is
    # that the server holds what was sent -- `notes show` is how you read it.
    _print_json({"project": label, "chars": len(stored), **_headroom_fields(row)})
    # A write door that cannot say the document is filling up makes fullness
    # invisible on the door people actually use.
    _report_notes_headroom(row, "project", label)


# ---------------------------------------------------------------- notes, everywhere
#
# `notes show|write` above are PROJECT-scoped and stay that way -- the project's
# notes are the default destination and every shipped script calls them bare.
# What follows is the same document model on every other carrier (0124), plus the
# TEAM note (0125), through target flags rather than five parallel verb groups.

#: Every entity that carries notes, and how to resolve one from a CLI flag.
#: The TEAM note is not one of them: a session that has its file edits it and
#: syncs (`probe notes sync`, and the hooks that call it). Only `notes append`
#: and `notes edit` take `--team`, for a caller with no file, and they reach the
#: server-computed team-note writes rather than anything resolved here.
#: A TRIAL is deliberately absent, though `PATCH /v1/trials/{id}` takes the same
#: three notes writes and the dashboard offers the editor. Every carrier here is
#: something the agent CREATED, which is what gives it a moment to annotate;
#: a trial is materialized by a database trigger on any rollout span (0135), and
#: there is one per rollout, so a 500-rollout run would offer 500 documents for
#: an observation that belongs once on the run. Agents READ trial notes
#: (`probe trial get`); people write them in the dashboard.
_NOTE_TARGETS = ("project", "experiment", "run", "group", "artifact")


def _sub_note_row_for_headroom(row: object) -> object:
    """Adapt a sub-note write/read response to the entity-notes headroom keys.

    Sub-note responses spell the pair `remaining_chars`/`limit_chars` (the row
    prices itself); the shared fullness helpers read the entity spelling. A
    None row (journaled write) passes through — no server saw it, so there is
    no fullness to adapt.
    """
    if not isinstance(row, dict):
        return row
    adapted = dict(row)
    if "remaining_chars" in adapted and "notes_remaining_chars" not in adapted:
        adapted["notes_remaining_chars"] = adapted["remaining_chars"]
    if "limit_chars" in adapted and "notes_limit_chars" not in adapted:
        adapted["notes_limit_chars"] = adapted["limit_chars"]
    return adapted


def _sub_notes_supported(exc: errors.RosError) -> None:
    """Map a ROUTE-shaped 404 to the honest self-host answer.

    The hosted backend always has these routes; a self-hosted server one
    release behind answers FastAPI's bare `Not Found` — which is not "no such
    note", it is "no such door". Saying so beats handing the caller an id hunt.
    An ENTITY 404 names what is missing ("run not found", "no sub-note
    titled ...") and passes through untouched.
    """
    if exc.status == 404 and str(exc.detail or "").strip() == "Not Found":
        # A bare `Not Found` is a ROUTE miss, and there are two ways to miss a
        # route: a server without it, or a request that never reached it (a
        # malformed id spliced into the path lands here too, against a fully
        # current server). Name both rather than diagnose confidently.
        print(
            "error: the sub-notes route answered a bare 404 — this server may "
            "predate sub-notes (self-hosted needs research-os >= 0.231.0.0; "
            "hosted backends already have them), or the target id may be "
            "malformed (check `--group`/`--artifact` values)",
            file=sys.stderr,
        )
        raise typer.Exit(1) from exc


def _sub_note_id_ref(note: str) -> str | None:
    """The uuid inside an `id:<uuid>` --note value, or None for a plain title.

    The escape hatch for duplicated titles: titles are legal to duplicate
    (tabs key on id), so every command that refuses an ambiguous title must
    also take the id the refusal printed — otherwise the advised repair
    (`probe notes rename`) resolves through the same refusal and the
    duplicates are unreachable from the CLI entirely.
    """
    if note.startswith("id:"):
        return note[3:].strip()
    return None


def _resolve_sub_note_by_title(client: Client, kind: str, entity_id: str, title: str) -> dict:
    """The one sub-note `title` (or `id:<uuid>`) names, via the list read.

    For the ID-ADDRESSED commands (show/rename/delete), which need the id in
    hand. Writes never come here — append/edit send the title IN the request
    and the server resolves at apply time, which is what lets them queue.
    Same exactly-once contract, spoken client-side: zero matches lists what
    exists, two-plus lists the ids. An `id:<uuid>` value resolves through the
    SAME entity-scoped list, so an id from some other entity is a miss here,
    never a cross-entity read that mislabels its output.
    """
    try:
        page = client.list_sub_notes(kind, entity_id)
    except errors.RosError as exc:
        _sub_notes_supported(exc)
        raise
    id_ref = _sub_note_id_ref(title)
    if id_ref is not None:
        matches = [row for row in page.get("sub_notes", []) if row.get("id") == id_ref]
        if len(matches) == 1:
            return matches[0]
        print(
            f"error: no sub-note with id {id_ref!r} on this {kind} "
            "(`probe notes list` shows its sub-notes and their ids)",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    matches = [row for row in page.get("sub_notes", []) if row.get("title") == title.strip()]
    if len(matches) == 1:
        return matches[0]
    if not matches:
        titles = [row.get("title") for row in page.get("sub_notes", [])]
        print(
            f"error: no sub-note titled {title!r} on this {kind}; "
            f"existing titles: {titles or '(none)'}",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    ids = [row.get("id") for row in matches]
    print(
        f"error: {len(matches)} sub-notes are titled {title!r}: {ids}. "
        "Address one as `--note id:<uuid>`, or rename one first "
        "(`probe notes rename --note id:<uuid> --to ...`).",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _note_target(
    client: Client,
    *,
    project: str | None,
    experiment: str | None,
    run: str | None,
    group: str | None,
    artifact: str | None,
) -> tuple[str, str, str]:
    """(kind, id, label) for a notes write. Exactly one target, or the default.

    Refusing two targets rather than picking one: "wrote the note" is the same
    sentence whichever entity received it, so a silent preference order would
    put prose on the wrong row and say nothing.
    """
    chosen = [
        (kind, value)
        for kind, value in (
            ("experiment", experiment),
            ("run", run),
            ("group", group),
            ("artifact", artifact),
        )
        if value is not None
    ]
    if project is not None:
        chosen.append(("project", project))
    if len(chosen) > 1:
        raise typer.BadParameter(
            "pass exactly one of --project/--experiment/--run/--group/--artifact"
        )
    if not chosen:
        # No flag at all: the project, which is what `notes` has always meant.
        project_id, label = _notes_project(client, None)
        return "project", project_id, label
    kind, value = chosen[0]
    if kind == "project":
        project_id, label = _notes_project(client, value)
        return "project", project_id, label
    if kind == "run":
        # Runs resolve by petname OR id -- the one polymorphic ref in the CLI.
        return "run", refs.resolve_run(client, value).id, value
    if kind == "experiment":
        return "experiment", refs.resolve(client, "experiment", value).id, value
    # Groups and artifacts have no slug form: the server answers a bad id.
    return kind, value, value


def _headroom_fields(row: object) -> dict[str, int]:
    """The fullness numbers for a write's JSON, or `{}` when there are none.

    Empty rather than nulls, and the difference is load-bearing for a caller
    piping this into `jq`: a write that was JOURNALED reached no server, so there
    is no fullness to report, and emitting `"remaining": null` invites a reader to
    treat absent as zero. A key that is not there cannot be misread as a number.

    `stored_chars`, not `chars`. These commands have printed `chars` since they
    shipped and it means the size of the CHUNK the caller sent; the document's
    own length is a different number and must not silently take that key.
    """
    from ..sdk.notes import notes_fullness

    fullness = notes_fullness(row)
    if fullness is None:
        return {}
    remaining, limit = fullness
    return {"remaining": remaining, "limit": limit, "stored_chars": limit - remaining}


def _notes_write(kind: str, label: str, write):
    """Run a notes write; on a CAP REFUSAL, add the advice the 422 cannot carry.

    The 422 says "appending would exceed the 4000-character notes limit" and
    stops. That is the moment a writer most needs to know what to do, and it is
    the one path that never reaches `_report_notes_headroom` -- the advice rides
    the SUCCESS response, and there is no success. So the wall used to be the
    least informative state in the whole feature.

    Matched on the server's own wording rather than on the status code, because
    `Client.write` raises RosError for every 4xx and only this one means "the
    document is closed until you compact it".
    """
    from ..sdk.notes import full_note_message

    try:
        return write()
    except errors.RosError as exc:
        if "notes limit" not in str(exc):
            raise
        print(f"error: {exc}", file=sys.stderr)
        for line in textwrap.wrap(full_note_message(kind, label), width=76):
            print(f"       {line}", file=sys.stderr)
        raise typer.Exit(1) from exc


def _report_notes_headroom(row: object, kind: str, label: str) -> None:
    """Say on STDERR that this document is filling up, on the success path.

    The piece that would have caught `assignment-modeling`, which sat at 99,992
    of 100,000 characters while every append was being refused: a cap is only a
    budget if you can see it coming down. Stderr, beside the "appended to ..."
    line, so it never enters the JSON a script parses.

    Silent when the write was journaled or the backend is too old to publish the
    numbers -- `headroom_warning` returns None rather than guessing, because a
    client-side cap table would let this print a fullness the server never said.
    """
    from ..sdk.notes import headroom_warning

    message = headroom_warning(row, kind=kind, label=label)
    if message is not None:
        print(f"warning: {message}", file=sys.stderr)


@notes_app.command("list")
def notes_list(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
) -> None:
    """List an entity's titled sub-notes: title, fullness, when. No bodies —
    `probe notes show --note <title>` reads one."""
    with _client() as c:
        kind, entity_id, label = _note_target(
            c,
            project=project,
            experiment=experiment,
            run=run,
            group=group,
            artifact=artifact,
        )
        try:
            page = c.list_sub_notes(kind, entity_id)
        except errors.RosError as exc:
            _sub_notes_supported(exc)
            raise
    _print_json(
        {
            "target": kind,
            "label": label,
            "limit_count": page.get("limit_count"),
            "sub_notes": [
                {
                    "id": row.get("id"),
                    "title": row.get("title"),
                    "stored_chars": row.get("chars"),
                    "limit": row.get("limit_chars"),
                    "updated_at": row.get("updated_at"),
                }
                for row in page.get("sub_notes", [])
            ],
        }
    )


@notes_app.command("create")
def notes_create(
    title: str = typer.Option(..., "--title", help="the new sub-note's tab label"),
    file: str = typer.Argument(
        None, help="optional starting body; omit for a titled empty tab, '-' for stdin"
    ),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
) -> None:
    """Create a titled sub-note. Duplicate titles are legal (tabs key on id)
    but a title-addressed write to a duplicated title is refused — check
    `probe notes list` first rather than collecting rename chores."""
    body = ""
    if file is not None:
        body = sys.stdin.read() if file == "-" else Path(file).read_text()
    with _client() as c:
        kind, entity_id, label = _note_target(
            c,
            project=project,
            experiment=experiment,
            run=run,
            group=group,
            artifact=artifact,
        )
        try:
            row = _notes_write(
                kind,
                f"{label} › {title}",
                lambda: c._create_sub_note(kind, entity_id, title, body),
            )
        except errors.RosError as exc:
            _sub_notes_supported(exc)
            raise
    row = _sub_note_row_for_headroom(row)
    print(f"created {kind} sub-note {title!r} ({label})", file=sys.stderr)
    payload = {"target": kind, "label": label, "title": title, "chars": len(body)}
    if isinstance(row, dict):
        payload["id"] = row.get("id")
    _print_json({**payload, **_headroom_fields(row)})


# ------------------------------------------------- notes append / edit, no file
#
# The file model (checkout, edit, push) needs a file system and a second step. An
# agent that can only pass arguments -- the dashboard assistant, a sandboxed tool
# -- adds or corrects a note with these two instead. The text is ALWAYS literal:
# no `@file`, no `-` for stdin, so a command can never send a file it names.
#
# The server has no append or span edit any more (0.388.0.0), so both read the
# note, change its text here, and replace it pinned to the version they read
# (`base_version`, the `notes push` contract). If someone wrote in between, the
# server refuses with 409 and the change is applied again to the new text.

#: Reads-and-retries before giving up on a note that keeps moving. Each attempt
#: is a fresh read, so this runs out only under a continuous stream of writes.
_NOTE_REWRITE_ATTEMPTS = 5


def _note_carrier(
    c: Client,
    *,
    project: str | None,
    experiment: str | None,
    run: str | None,
    group: str | None,
    artifact: str | None,
    note: str | None,
) -> tuple[str, str, str | None, str]:
    """(kind, entity id, sub-note id or None, label) for a text-only write."""
    kind, entity_id, label = _note_target(
        c, project=project, experiment=experiment, run=run, group=group, artifact=artifact
    )
    if note is None:
        return kind, entity_id, None, label
    try:
        found = _resolve_sub_note_by_title(c, kind, entity_id, note)
    except errors.RosError as exc:
        _sub_notes_supported(exc)
        raise
    return kind, entity_id, found["id"], f"{label} › {note}"


def _send_note(
    c: Client, kind: str, entity_id: str, sub_id: str | None, text: str, version: int
) -> dict | None:
    """Replace one note pinned to `version`: the main note, or a sub-note by id."""
    op_key = uuid.uuid4().hex
    if sub_id is not None:
        return c._replace_sub_note(sub_id, text, base_version=version, op_key=op_key)
    return c._replace_notes(kind, entity_id, text, base_version=version, op_key=op_key)


def _stored_form(field: str, text: str) -> str:
    """`text` as Probe would store it under `field`.

    The client (`Client.write`) and the server (`app/security/content_guard.py`)
    both run the credential scrubber over every write body, so this is what lands.
    Some rules rewrite a span; some rewrite the WHOLE value to `<redacted>`.
    Applied until it stops changing, because it runs more than once on the way.
    """
    from ..sdk.redaction import default_scrub

    for _ in range(3):
        scrubbed = default_scrub({field: text})[field]
        if scrubbed == text:
            break
        text = scrubbed
    return text


def _is_version(value: object) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _refuse_scrubbed_old(old: str) -> None:
    """Refuse an `--old` the scrubber would rewrite (the server scrubs `old_text`
    before matching it, so it would match the `<redacted>` text instead)."""
    if _stored_form("old_text", old) != old:
        print(
            "error: --old holds text Probe's credential scrubber rewrites, so it would "
            "match the wrong text; nothing was written. Match a nearby piece of the note "
            "instead.",
            file=sys.stderr,
        )
        raise typer.Exit(1)


def _read_note(
    c: Client, kind: str, entity_id: str, sub_id: str | None
) -> tuple[dict, str, object]:
    """(row, document, notes_version) for the main note or one sub-note.

    Raises ValueError for a reply that is not Probe's JSON row."""
    row = c.get_sub_note(sub_id) if sub_id is not None else _entity_notes_row(c, kind, entity_id)
    if not isinstance(row, dict):
        raise ValueError(f"the reply was not a {kind} note")
    if sub_id is not None:
        return _sub_note_row_for_headroom(row), row.get("body") or "", row.get("notes_version")
    return row, row.get("notes") or "", row.get("notes_version")


@dataclass(frozen=True)
class _Unconfirmed:
    """Why a write's reply did not confirm it, and whether it can still land.

    `may_still_land`: the request reached Probe and nobody saw it finish -- a
    timeout, a reply lost after sending, a 502/504 from the ingress. The CLI
    gives up after 30 s and the server keeps working for up to 300 s, and a
    read is not blocked by the write's row lock, so a note that reads unchanged
    NOW can still change. Only when the app itself answered (a redirect, a
    non-JSON 200, its own 500/503) does unchanged mean nothing was written."""

    why: str
    may_still_land: bool


#: A reply with no version: a redirect, or a 200 that is not Probe's JSON.
_NO_VERSION_REPLY = _Unconfirmed("Probe's reply did not say what it stored", False)

#: Gateway answers: the ingress gave up on the app, which may still be working.
_GATEWAY_STATUSES = frozenset({502, 504})


def _settle_unconfirmed(
    read, base: int, sent: str, what: str, *, why: _Unconfirmed, shown: str
) -> dict:
    """A write whose reply did not confirm it. Never sent again: read the note.

    One version on with exactly the text sent is this write, landed. The same
    version is nothing written only when the app answered; after a timeout it
    is "not there yet". Anything else may be this write or someone else's, and
    only a person reading the note can tell. `read()` returns
    (row, document, version); `shown` is the command that prints the note.
    """
    try:
        row, document, version = read()
    except (errors.RosError, ValueError) as exc:
        # ValueError: a reply that was not JSON (an ingress page).
        print(
            f"error: {why.why}; the {what} could not be re-read ({exc}), so the write may "
            f"have landed. Read it (`{shown}`) before running this again.",
            file=sys.stderr,
        )
        raise typer.Exit(1) from None
    if version == base + 1 and document == sent:
        print(f"{why.why}; the {what} shows this write landed", file=sys.stderr)
        return row
    if version == base and why.may_still_land:
        print(
            f"error: {why.why}; the {what} does not show this write yet, but Probe may still "
            f"be applying it. Read it (`{shown}`) in a few minutes, before running this again.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    if version == base:
        print(
            f"error: {why.why}; the {what} is unchanged, so nothing was written. Run it again.",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    print(
        f"error: {why.why}; the {what} changed meanwhile, so this write may have landed. "
        f"Read it (`{shown}`) before running this again.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _unconfirmed_reason(exc: errors.RosError) -> _Unconfirmed | None:
    """Why a failed write MAY have landed, or None when it surely did not.

    A connection that never reached Probe wrote nothing. A timeout, a reply
    lost after sending or a gateway 502/504 may still land; a 5xx the app
    answered itself (500, 503) did not write."""
    if isinstance(exc, errors.TransportError):
        if getattr(exc, "unreachable", False):
            return None
        return _Unconfirmed(f"the reply was lost ({exc})", True)
    if isinstance(exc, errors.ServerError):
        if exc.status in _GATEWAY_STATUSES:
            return _Unconfirmed(f"Probe's gateway gave up waiting ({exc})", True)
        return _Unconfirmed(f"Probe answered with an error ({exc})", False)
    return None


def _refuse_over_cap(row: object, text: str, kind: str, label: str, *, appending: bool) -> None:
    """Refuse, before sending, a note the server would refuse for its length.

    Uses the cap the READ published (`notes_limit_chars`); a server too old to
    publish it answers for itself."""
    from ..sdk.notes import full_note_message, notes_fullness

    fullness = notes_fullness(row)
    if fullness is None or len(text) <= fullness[1]:
        return
    limit = fullness[1]
    if appending:
        print(
            f"error: appending would exceed the {limit:,}-character notes limit; "
            "nothing was written",
            file=sys.stderr,
        )
        for line in textwrap.wrap(full_note_message(kind, label), width=76):
            print(f"       {line}", file=sys.stderr)
    else:
        print(
            f"error: the edit would leave the {kind} note ({label}) at {len(text):,} "
            f"characters, over its {limit:,}-character limit; nothing was written",
            file=sys.stderr,
        )
    raise typer.Exit(1)


def _rewrite_note(
    c: Client,
    kind: str,
    entity_id: str,
    sub_id: str | None,
    label: str,
    change: Callable[[str], tuple[str, str, str]],
    *,
    appending: bool,
) -> dict:
    """Read the note, `change` its text, replace it pinned to the version read.

    `change(document)` returns (kept before, new text, kept after) and refuses
    by raising (an edit whose `--old` does not match once). On a stale-version
    409 the note is read again and `change` runs on the new text, so a
    concurrent writer's words are kept, never overwritten.

    Nothing already in the note may change except what the caller asked for,
    and the scrubber every write passes through can change it: a note holding
    text it would rewrite is refused, and so is new text whose scrub would
    rewrite the rest of the note. A reply that does not confirm the write is
    settled by reading the note, never by sending it again."""
    field = "body" if sub_id is not None else "notes"
    what = f"{kind} note ({label})"

    def read() -> tuple[dict, str, object]:
        return _read_note(c, kind, entity_id, sub_id)

    for _ in range(_NOTE_REWRITE_ATTEMPTS):
        try:
            row, document, version = read()
        except ValueError:
            # Not JSON: an ingress page answered the read, not Probe.
            print(
                f"error: reading the {what} did not return Probe's answer; nothing was "
                "written.",
                file=sys.stderr,
            )
            raise typer.Exit(1) from None
        if not _is_version(version):
            print(
                f"error: Probe did not say which version of the {what} it read, so a "
                "write could overwrite someone else's; nothing was written.",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        if _stored_form(field, document) != document:
            print(
                f"error: the {what} holds text Probe's credential scrubber would rewrite, "
                "and saving the note would rewrite it; nothing was written. Review it with "
                "`probe notes checkout`, then `probe notes push`.",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        before, middle, after = change(document)
        text = before + middle + after
        sent = _stored_form(field, text)
        if not (
            sent.startswith(before)
            and sent.endswith(after)
            and len(sent) >= len(before) + len(after)
        ):
            print(
                f"error: the new text holds something Probe's credential scrubber would "
                f"rewrite, and the rewrite would change the rest of the {what} too; nothing "
                "was written. Leave the credential-shaped text out.",
                file=sys.stderr,
            )
            raise typer.Exit(1)
        _refuse_over_cap(row, sent, kind, label, appending=appending)
        try:
            written = _notes_write(
                kind, label, lambda: _send_note(c, kind, entity_id, sub_id, text, version)
            )
        except errors.ConflictError as exc:
            # `stale_replace`: the document moved since the read. Any other 409
            # is a refusal this loop cannot fix.
            if isinstance(exc.detail, dict) and "notes_version" in exc.detail:
                continue
            raise
        except errors.RosError as exc:
            why = _unconfirmed_reason(exc)
            if why is None:
                raise
            return _settle_unconfirmed(
                read, version, sent, what, why=why, shown="probe notes show"
            )
        written = _sub_note_row_for_headroom(written)
        if not (isinstance(written, dict) and _is_version(written.get("notes_version"))):
            return _settle_unconfirmed(
                read, version, sent, what, why=_NO_VERSION_REPLY, shown="probe notes show"
            )
        return written
    print(
        f"error: the {what} kept changing while this wrote; nothing was written. "
        "Run it again.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


# The TEAM note is different: the server keeps two writes that compute the change
# itself under the note's row lock (`POST /v1/team-note/apply/paragraph|span`),
# so nothing is merged here. The note IS read first, for its version and text:
# that is what settles a write whose reply was lost. A session that has the
# team-note file edits it and `probe notes sync`s instead; these are for a
# caller with no file.

_TEAM_LABEL = "team note"


def _team_only(team: bool, **targets: object) -> None:
    """Refuse `--team` beside an entity flag or `--note`: one note per write."""
    if team and any(value is not None for value in targets.values()):
        raise typer.BadParameter(
            "--team writes the team note; drop --project/--experiment/--run/--group/"
            "--artifact/--note"
        )


def _team_topped_up(body: str, text: str) -> str:
    """The server's append (`app/team_notes/service.py::_topped_up`)."""
    return f"{body.rstrip()}\n\n{text.strip()}\n" if body.strip() else f"{text.strip()}\n"


def _write_team_note(
    c: Client, write: Callable[[], dict | None], expected: Callable[[str], str]
) -> dict:
    """Run a team-note write, retrying the one refusal that wrote nothing and
    says so (`retryable`: another write landed at the same instant).

    `expected(body)` is what the server stores when it applies this write to
    `body`; with the version read just before, it settles a reply that did not
    confirm the write. A credential that cannot read the note still writes, but
    such a reply is then reported as possibly landed."""
    for _ in range(_NOTE_REWRITE_ATTEMPTS):
        base: tuple[int, str] | None = None
        try:
            head = c.get_team_note()
        except (errors.ScopeError, ValueError):
            # No read scope, or a reply that was not JSON: write anyway, but a
            # reply that does not confirm the write cannot be settled.
            head = None
        if isinstance(head, dict) and _is_version(head.get("version")):
            base = (head["version"], head.get("body") or "")

        def read() -> tuple[dict, str, object]:
            row = c.get_team_note()
            if not isinstance(row, dict):
                raise ValueError("the reply was not a team note")
            return row, row.get("body") or "", row.get("version")

        def settle(why: _Unconfirmed) -> dict:
            if base is None:
                print(
                    f"error: {why.why}, and the {_TEAM_LABEL} could not be read before the "
                    "write to check against; the write may have landed. Read it (`probe "
                    "notes team`) before running this again.",
                    file=sys.stderr,
                )
                raise typer.Exit(1)
            return _settle_unconfirmed(
                read, base[0], expected(base[1]), _TEAM_LABEL, why=why, shown="probe notes team"
            )

        try:
            row = write()
        except errors.ConflictError as exc:
            if isinstance(exc.detail, dict) and exc.detail.get("retryable") is True:
                continue
            raise
        except errors.RosError as exc:
            why = _unconfirmed_reason(exc)
            if why is None:
                raise
            return settle(why)
        if not (isinstance(row, dict) and _is_version(row.get("version"))):
            return settle(_NO_VERSION_REPLY)
        return row
    print(
        "error: the team note kept changing while this wrote; nothing was written. "
        "Run it again.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _team_payload(row: dict, **fields: object) -> dict:
    payload: dict[str, Any] = {"target": "team", "label": _TEAM_LABEL, **fields}
    payload["version"] = row.get("version")
    if isinstance(row.get("remaining_chars"), int):
        payload["remaining"] = row["remaining_chars"]
    return payload


def _refuse_edit_match(found: int, kind: str, label: str) -> None:
    """The refusal for an `--old` that does not match exactly once."""
    if found == 0:
        why = "matches nothing", "Copy it exactly from `probe notes show`"
    else:
        why = f"matches {found} places", "Add surrounding text until it matches once"
    print(
        f"error: --old {why[0]} in the {kind} note ({label}); nothing was "
        f"written. {why[1]}.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


@notes_app.command("append")
def notes_append(
    text: str = typer.Option(..., "--text", help="the paragraph to add, as literal text"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    team: bool = typer.Option(False, "--team", help="the TEAM note instead of an entity's"),
) -> None:
    """Add a paragraph to the end of a note: an entity's, one sub-note, or the team note.

    The text is taken literally (no @file, no stdin). It lands after a blank
    line, and anything a teammate wrote meanwhile is kept.
    """
    if not text.strip():
        raise typer.BadParameter("--text is empty")
    _team_only(
        team, project=project, experiment=experiment, run=run, group=group,
        artifact=artifact, note=note,
    )
    if team:
        stored = _stored_form("text", text)
        with _client() as c:
            row = _write_team_note(
                c,
                lambda: c.append_team_note(text),
                lambda body: _team_topped_up(body, stored),
            )
        print(f"appended to the {_TEAM_LABEL}", file=sys.stderr)
        _print_json(_team_payload(row, chars=len(text)))
        return
    from ..sdk.notes import append_to_document

    def change(document: str) -> tuple[str, str, str]:
        joined = append_to_document(document, text)
        return joined[: len(joined) - len(text)], text, ""

    with _client() as c:
        kind, entity_id, sub_id, label = _note_carrier(
            c, project=project, experiment=experiment, run=run, group=group,
            artifact=artifact, note=note,
        )
        row = _rewrite_note(c, kind, entity_id, sub_id, label, change, appending=True)
    print(f"appended to {kind} note ({label})", file=sys.stderr)
    payload: dict[str, Any] = {"target": kind, "label": label}
    if note is not None:
        payload["note"] = note
    payload.update({"chars": len(text), "version": row.get("notes_version")})
    _print_json({**payload, **_headroom_fields(row)})
    _report_notes_headroom(row, kind, label)


@notes_app.command("edit")
def notes_edit(
    old: str = typer.Option(..., "--old", help="the exact text to replace; must match once"),
    new: str = typer.Option(..., "--new", help="what replaces it ('' deletes it)"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    team: bool = typer.Option(False, "--team", help="the TEAM note instead of an entity's"),
) -> None:
    """Replace one exact piece of a note: an entity's, one sub-note, or the team note.

    `--old` must appear exactly once, character for character; otherwise
    nothing is written and the command fails. Both values are literal text
    (no @file, no stdin).
    """
    if not old:
        raise typer.BadParameter("--old is empty")
    _team_only(
        team, project=project, experiment=experiment, run=run, group=group,
        artifact=artifact, note=note,
    )
    _refuse_scrubbed_old(old)
    if team:
        stored_new = _stored_form("new_text", new)
        with _client() as c:
            try:
                row = _write_team_note(
                    c,
                    lambda: c.edit_team_note(old, new),
                    lambda body: body.replace(old, stored_new, 1),
                )
            except errors.ConflictError as exc:
                found = exc.detail.get("match_count") if isinstance(exc.detail, dict) else None
                if not isinstance(found, int):
                    raise
                _refuse_edit_match(found, "team", _TEAM_LABEL)
        print(f"edited the {_TEAM_LABEL}", file=sys.stderr)
        _print_json(_team_payload(row, removed=len(old), added=len(new)))
        return
    from ..sdk.notes import edit_match_count

    with _client() as c:
        kind, entity_id, sub_id, label = _note_carrier(
            c, project=project, experiment=experiment, run=run, group=group,
            artifact=artifact, note=note,
        )

        def change(document: str) -> tuple[str, str, str]:
            found = edit_match_count(document, old)
            if found != 1:
                _refuse_edit_match(found, kind, label)
            at = document.index(old)
            return document[:at], new, document[at + len(old) :]

        row = _rewrite_note(c, kind, entity_id, sub_id, label, change, appending=False)
    print(f"edited {kind} note ({label})", file=sys.stderr)
    payload: dict[str, Any] = {"target": kind, "label": label}
    if note is not None:
        payload["note"] = note
    payload.update(
        {"removed": len(old), "added": len(new), "version": row.get("notes_version")}
    )
    _print_json({**payload, **_headroom_fields(row)})
    # An edit is also how a note is compacted, so this line going quiet is how a
    # caller sees that a compaction worked.
    _report_notes_headroom(row, kind, label)


@notes_app.command("rename")
def notes_rename(
    note: str = typer.Option(..., "--note", help="the sub-note's current title, or id:<uuid>"),
    to: str = typer.Option(..., "--to", help="its new title"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
) -> None:
    """Rename a sub-note. Records no version — history tracks documents, not
    labels — and it is also how a duplicated title gets un-ambiguous again."""
    with _client() as c:
        kind, entity_id, label = _note_target(
            c,
            project=project,
            experiment=experiment,
            run=run,
            group=group,
            artifact=artifact,
        )
        row = _resolve_sub_note_by_title(c, kind, entity_id, note)
        c._rename_sub_note(row["id"], to)
    print(f"renamed {kind} sub-note {note!r} -> {to!r} ({label})", file=sys.stderr)
    _print_json({"target": kind, "label": label, "id": row.get("id"), "title": to})


@notes_app.command("delete")
def notes_delete(
    note: str = typer.Option(..., "--note", help="the sub-note's title, or id:<uuid>"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    group: str = typer.Option(None, "--group", help="group id"),
    artifact: str = typer.Option(None, "--artifact", help="artifact id"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
) -> None:
    """Permanently delete a sub-note AND its version history. Requires a
    credential with the `delete` scope, like every other delete here."""
    with _client() as c:
        kind, entity_id, label = _note_target(
            c,
            project=project,
            experiment=experiment,
            run=run,
            group=group,
            artifact=artifact,
        )
        row = _resolve_sub_note_by_title(c, kind, entity_id, note)
        if not yes:
            if not typer.confirm(
                f"permanently delete {kind} sub-note {note!r} ({label}) and its history?"
            ):
                raise typer.Exit(1)
            # The prompt may have sat open while another session renamed or
            # removed this id; a confirm given for title X must not destroy a
            # document that is now something else. Re-read before acting.
            try:
                current = c.get_sub_note(row["id"])
            except errors.RosError as exc:
                if exc.status == 404:
                    print("error: that sub-note was deleted meanwhile", file=sys.stderr)
                    raise typer.Exit(1) from exc
                raise
            if _sub_note_id_ref(note) is None and current.get("title") != note.strip():
                print(
                    f"error: that sub-note is now titled {current.get('title')!r} — "
                    "re-run against the current title (or `--note id:...`)",
                    file=sys.stderr,
                )
                raise typer.Exit(1)
        c._delete_sub_note(row["id"])
    print(f"deleted {kind} sub-note {note!r} ({label})", file=sys.stderr)
    _print_json({"target": kind, "label": label, "id": row.get("id"), "deleted": True})


#: One sweep reads at most this many pages of the catalog. 100 is the route's
#: per-page maximum, so this is 2,000 documents -- far above the largest tenant
#: today (52) and bounded on purpose: an unbounded walk is a command that gets
#: slower every month without anyone deciding it should. When the cap is reached
#: the report SAYS so, because a truncated sweep that reads as complete is worse
#: than no sweep -- "nothing is near full" would be a claim it never checked.
_NOTES_STATUS_MAX_PAGES = 20
_NOTES_STATUS_PAGE_SIZE = 100


def _notes_status_row(item: dict) -> dict | None:
    """One catalog item as a fullness row, or None if it carries no sizes.

    A backend older than these fields answers without `chars`, and a row with no
    size cannot be ranked by fullness. Dropped rather than defaulted to zero,
    which would sort a document of unknown size to the bottom of a report whose
    whole job is finding the full ones.
    """
    chars, limit = item.get("chars"), item.get("limit_chars")
    if not isinstance(chars, int) or not isinstance(limit, int) or limit <= 0:
        return None
    ancestors = [a.get("title") or "" for a in item.get("ancestors") or []]
    return {
        "kind": item.get("kind"),
        "id": item.get("id"),
        "title": item.get("title"),
        "path": " / ".join([*ancestors, item.get("title") or ""]),
        "chars": chars,
        "limit": limit,
        "remaining": max(0, limit - chars),
        # floor, matching probe.sdk.notes: never print 100% for a document that
        # still accepts a write.
        "percent": math.floor(100 * chars / limit),
        "updated_at": item.get("updated_at"),
    }


@notes_app.command("status")
def notes_status(
    above: float = typer.Option(
        0.0, "--above", min=0.0, max=100.0, help="only report documents at least this % full"
    ),
) -> None:
    """How full every notes document in this team is -- the fullness sweep.

    TENANT-WIDE, and deliberately without the --project/--run/--artifact flags the
    other `notes` verbs take. One entity's headroom already rides on that entity's
    own read (`notes_remaining_chars` and `notes_limit_chars` on the project,
    experiment, run, group and artifact responses), so the question only this
    command can answer is the cross-entity one: WHICH documents are close to
    refusing writes. Answering it used to mean one API fetch per entity, which is
    why nobody did it -- and why a project sat at 99,992 of 100,000 characters,
    refusing every append, for a day.

    Documents are listed fullest first. Writes are refused AT the cap, not near
    it, so a document at 100% is one that has already been losing writes.
    """
    from ..sdk.notes import NOTES_WARN_FRACTION

    rows: list[dict] = []
    cursor: str | None = None
    truncated = False
    with _client() as c:
        for page_number in range(_NOTES_STATUS_MAX_PAGES):
            # The limit is what selects the FLAT listing over the dashboard's
            # lazy tree; without it this would sweep root branches only. See
            # Client.list_notes.
            page = c.list_notes(
                cursor=cursor,
                limit=_NOTES_STATUS_PAGE_SIZE,
                # A sub-note can refuse writes at ITS cap while every main note
                # has room; a sweep that cannot see them reports "nothing is
                # near full" about the very documents losing writes.
                include_sub_notes=True,
            )
            for item in page.get("items") or []:
                row = _notes_status_row(item)
                if row is not None:
                    rows.append(row)
            cursor = page.get("next_cursor")
            if not cursor:
                break
            truncated = page_number == _NOTES_STATUS_MAX_PAGES - 1

    rows.sort(key=lambda r: (-r["percent"], -r["chars"]))
    warn_at = 100 * (1 - NOTES_WARN_FRACTION)
    near_full = [r for r in rows if r["percent"] >= warn_at]
    shown = [r for r in rows if r["percent"] >= above]

    for row in shown:
        mark = "!" if row["percent"] >= warn_at else " "
        print(
            f"{mark} {row['percent']:3d}%  {row['chars']:>7,}/{row['limit']:<7,}  "
            f"{row['kind']:<10} {row['path']}",
            file=sys.stderr,
        )
    summary = f"{len(rows)} notes documents, {len(near_full)} at or above {warn_at:.0f}% full"
    if truncated:
        summary += (
            f" -- STOPPED after {_NOTES_STATUS_MAX_PAGES * _NOTES_STATUS_PAGE_SIZE} documents; "
            "more exist and were not read"
        )
    print(summary, file=sys.stderr)
    _print_json(
        {
            "scanned": len(rows),
            "truncated": truncated,
            "warn_at_percent": warn_at,
            "near_full": len(near_full),
            "documents": shown,
        }
    )


@notes_app.command("team")
def notes_team(
    brief: bool = typer.Option(
        False, "--brief", help="the bounded slice a session is briefed with"
    ),
) -> None:
    """Print the team's shared note -- the working memory every session starts with.

    `--brief` prints the injected slice instead of the document: the curated head
    plus the newest appends, which is what an agent session actually receives.
    """
    with _client() as c:
        payload = c.get_team_note_brief() if brief else c.get_team_note()
    text = payload.get("text" if brief else "body") or ""
    if not text:
        print("the team note is empty", file=sys.stderr)
        return
    sys.stdout.write(text if text.endswith("\n") else text + "\n")


@notes_app.command("audit-advisory")
def notes_audit_advisory(
    source: str = typer.Option(
        "claude_code", "--source", help="which harness's block to measure against"
    ),
    force: bool = typer.Option(False, "--force", help="answer even in an automated session"),
    peek: bool = typer.Option(
        False, "--peek", help="print the line without claiming this machine's audit"
    ),
) -> None:
    """Print the team note's audit line, or nothing. FOR HOOKS, not for humans.

    THE PROMPT IS THE CHANNEL. This line used to be written into the rendered
    block in `CLAUDE.md` / `AGENTS.md`, where every session of that harness read
    it -- including the ones nobody is sitting in. An audit dispatched into
    `claude -p` or `codex exec` asks for a background agent that run cannot
    spawn, on behalf of a researcher who is not there to see the result. So the
    line moved to the UserPromptSubmit hook, which fires only when a prompt is
    submitted, and this command is what that hook calls.

    LOCAL ONLY, because it runs on a prompt-submit budget: the note off disk and
    the LAST render's measurements out of `health.json`. No network, no render.

    Silent unless the note is actually due, and silent in an automated session
    (`--force` overrides, for testing). Exit status is 0 either way: a hook that
    saw a non-zero exit would report a failure where the answer is just "no".

    ONE SESSION PER MACHINE. Printing the line claims the machine's audit lease
    (`claim_audit_dispatch`), and while another session holds it this prints
    nothing -- otherwise every session on the box spawns its own auditor before
    the first one stamps the note. The hook names its session in
    `PROBE_NOTE_AUDIT_SESSION`, which lets the holder be told again if the first
    telling never arrived. `--peek` looks without claiming, so a person checking
    the line does not silence the next real dispatch.
    """
    from ..sdk.config import resolve
    from . import team_note_file

    if not force and team_note_file.session_is_automated():
        return
    advisory = team_note_file.advisory_for_source(source, settings=resolve(base_url=_conn.base_url))
    holder = os.environ.get(team_note_file.AUDIT_SESSION_ENV) or None
    if advisory and not peek and not team_note_file.claim_audit_dispatch(holder=holder):
        return
    if advisory:
        sys.stdout.write(advisory if advisory.endswith("\n") else advisory + "\n")


@notes_app.command("sync")
def notes_sync(
    push_only: bool = typer.Option(
        False, "--push-only", help="send local edits and stop; do not refresh the file"
    ),
    pull_only: bool = typer.Option(
        False,
        "--pull-only",
        help="refresh the file only; send nothing",
    ),
) -> None:
    """Reconcile the local team-note file with the server.

    THIS IS HOW AGENTS WRITE THE TEAM NOTE NOW. The session-start hook seeds
    `~/.local/state/probe/team-note/probe-team-note.md` -- ONE file per machine,
    shared by every harness on it, NOT a `memory/` directory -- you edit it like
    any other markdown, and this command sends the result. The session hooks call
    it for you; running it by hand is for when you want the round trip immediately.

    It reconciles like git: fetch the server's head, MERGE it into the file
    (markers on a real conflict), then push what came out. Merging is what lets
    a session that could not push earlier catch up without either side's text
    being dropped -- overwriting the file and refusing to sync are both losses.

    Copies that are not ours to send -- a leftover per-harness document from the
    old layout, or one written under another credential -- are parked beside
    where they were found, never deleted and never uploaded, and named in the
    output.

    Exit status is 0 for anything that settled and 2 for a conflict, so a hook
    can tell "nothing to do" from "a human needs to look at this".
    """
    from ..sdk.config import resolve
    from . import team_note_file

    settings = resolve(base_url=_conn.base_url)
    where = team_note_file.paths_for(settings)
    text: str | None = None
    with _client() as c:
        if push_only:
            report = team_note_file.push(c, where)
        elif pull_only:
            # Refresh without sending. No hook uses this any more -- the session
            # hooks reconcile or push unconditionally -- but it stays as the
            # manual escape hatch for taking the team's copy without offering
            # your own, e.g. when a local file is known to be junk.
            report, text = team_note_file.pull(c, where)
        else:
            report, text = team_note_file.reconcile(c, where)

    # RENDER AFTER THE NETWORK, OUTSIDE THE CLIENT. This is what actually puts
    # the note in front of an agent: the instruction files are read by the
    # harness before any hook of ours runs, so the copy a session sees is the
    # one the PREVIOUS sync left behind. Rendering here, from the text we just
    # fetched, is what keeps both harnesses saying the same thing.
    #
    # A fetch that failed leaves `text` None, and then we render NOTHING rather
    # than re-rendering a local copy that may be older than the block already
    # installed. Replacing current content with staler content is the one
    # irreversible mistake available here.
    render = team_note_file.RenderReport()
    if text is not None:
        render = team_note_file.render_blocks(text, settings=settings)

    _print_json(
        {
            "document": str(where.document),
            "version": report.version,
            "pushed": report.pushed,
            "pulled": report.pulled,
            "merged": report.merged,
            "conflicted": report.conflicted,
            "detail": report.detail,
            "rendered": list(render.written),
            "rendered_pointer_only": list(render.pointer_only),
            "render_unchanged": list(render.unchanged),
            "render_opted_out": [*render.opted_out, *render.removed],
            "render_failures": list(render.failures),
        }
    )
    for failure in render.failures:
        print(f"team-note block: {failure}", file=sys.stderr)
    if report.conflicted:
        print(report.detail, file=sys.stderr)
        raise typer.Exit(2)


@app.command()
def events(run: str = run_ref()) -> None:
    """Read the backend lifecycle events for a run (fold #10, read-only)."""
    with _client() as c:
        _print_json(c.events.for_run(run))


# -- experiment maintenance ---------------------------------------------------
experiment_app = typer.Typer(no_args_is_help=True, help="experiment maintenance")
app.add_typer(experiment_app, name="experiment")

#: Why every experiment tag flag is refused. The server keeps an experiment's
#: tags read-only since the light experiments gave it its own record (R3), and
#: the experiment API carries none -- so a tag write could only ever fail there.
_EXPERIMENT_TAGS_READ_ONLY = (
    "an experiment's tags are read-only since experiments moved to their own record; "
    "tag the project instead (`probe project tag`), or say it in the question or notes"
)


@experiment_app.command("create")
def experiment_create(
    slug: str = typer.Argument(..., help="url-safe identifier, unique per tenant"),
    question: str = typer.Option(..., "--question", help="what you expect this to show"),
    name: str = typer.Option(
        None, "--name", help="display name; omit it and the row reads as its slug"
    ),
    project: str = typer.Option(
        None, "--project", help="project slug; defaults to the active one (`probe project use`)"
    ),
    description: str = description_opt(),
    summary: str = entity_markdown_opt(),
    #: RETIRED with the light experiments: declared so it can be REFUSED with
    #: the reason (Typer's "no such option" reads as a typo).
    tag: list[str] = typer.Option(
        None, "--tag", help="RETIRED: an experiment's tags are read-only", hidden=True
    ),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Create an experiment in a project.

    The counterpart to `probe project create`. Both exist because `probe run start`
    no longer creates its parents: it used to get-or-create the whole chain, so a
    typo'd slug minted a second identity instead of erroring, and an omitted
    question minted a permanent `[auto]` placeholder.

    `--question` is required here for that reason — this is the moment you know
    what you are testing, and nothing later goes back to fill it in.
    """
    if tag:
        raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY, param_hint="--tag")
    resolved_project = _ambient_project(project)
    if not resolved_project:
        raise errors.ValidationError(
            "pass --project, or set an active project with `probe project use`"
        )
    with _client() as c:
        # Same resolver as `run start`, so "no such project" is one error with
        # one exit code, and the message names the SLUG that was looked up rather
        # than the raw ambient value (which is an id).
        project_id = c.resolve_or_raise("project", _project_slug(c, resolved_project))["id"]
        created = c.create_experiment(
            slug,
            name,
            question=question,
            project_id=project_id,
            description=description,
            document=_text_value(summary),
            authored_by=_authored_by_value(authored_by),
        )
    _print_json(created)
    _print_link("experiment", created.get("id"))


@experiment_app.command("reproduce")
def experiment_reproduce(
    experiment_id: str = slug_ref("experiment"),
    version: int = typer.Option(
        None, "--version", help="pin against a minted experiment version (else live rows)"
    ),
) -> None:
    """Pull per-run reproduction summaries for an experiment.

    A MAP, not N full assemblies: each summary carries a `reproduce_url` — drill
    into one run with `probe run reproduce RUN`. `--version N` reads a frozen
    `experiment freeze` manifest instead of the live run set.
    """
    with _client() as c:
        _print_json(
            c.experiment_reproduce(_ref(c, "experiment", experiment_id).id, version=version)
        )


@experiment_app.command("freeze")
def experiment_freeze(
    experiment_id: str = slug_ref("experiment"),
    label: str = typer.Option(None, "--label", help="a human name for this frozen manifest"),
) -> None:
    """Freeze the experiment: mint an immutable version pinning its current run set.

    An ergonomic alias for `probe version create` — the moment you publish or hand
    off an experiment, this pins exactly which runs and artifacts it comprised, so
    `experiment reproduce --version N` resolves against that manifest forever. No
    new backend: it mints the same `experiment_versions` row.
    """
    with _client() as c:
        _print_json(c.experiment_version(_ref(c, "experiment", experiment_id).id, label=label))


@experiment_app.command("get")
def experiment_get(experiment_id: str = slug_ref("experiment")) -> None:
    """Show one experiment.

    Experiments were the only addressable kind with NO read verb: projects,
    workspaces, runs and groups all had one, and `experiment list` was the whole
    surface. Reading one back after a `set` meant listing its siblings and
    filtering by eye.
    """
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        _print_json(c.get_experiment(target.id, project_id=_filed_under(target)))


@experiment_app.command("set")
def experiment_set(
    experiment_id: str = slug_ref("experiment"),
    question: str = typer.Option(None, "--question", help="replace the question"),
    name: str = typer.Option(None, "--name"),
    #: 0231: RETIRED, and declared so it can be REFUSED. Deleting the option
    #: makes Typer answer "no such option", which reads as a typo; this says
    #: what happened and which flag replaced it.
    description: str = typer.Option(
        None,
        "--description",
        help="RETIRED: an experiment's description is now its --question",
        hidden=True,
    ),
    summary: str = entity_markdown_opt(),
    #: RETIRED with the light experiments, like --description above.
    add_tag: list[str] = typer.Option(None, "--add-tag", hidden=True),
    remove_tag: list[str] = typer.Option(None, "--remove-tag", hidden=True),
    set_tags: list[str] = typer.Option(None, "--set-tags", hidden=True),
    authored_by: AuthoredBy = authored_by_opt(),
) -> None:
    """Amend an experiment's question, name or visible Markdown, in one command."""
    if description is not None:
        raise typer.BadParameter(
            "an experiment's description was replaced by its QUESTION (0231). Use "
            "--question for what the experiment is testing, or --summary for prose "
            "about it -- which is where existing descriptions were moved."
        )
    if _tag_flags_given(add_tag, remove_tag, set_tags):
        raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY)
    fields = {"question": question, "name": name, "document": _text_value(summary)}
    if all(value is None for value in fields.values()):
        raise typer.BadParameter("pass at least one of --question/--name/--summary")
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        result = c.update_experiment(
            target.id,
            **fields,
            authored_by=_authored_by_value(authored_by),
                project_id=_filed_under(target),
        )
    _print_json(result)


@experiment_app.command("move")
def experiment_move(
    experiment_id: str = slug_ref("experiment"),
    to: str = typer.Option(..., "--to", help="the project to move it to (slug or id:<uuid>)"),
) -> None:
    """Move an experiment, with its runs, files and groups, to another project.

    One write on the server: everything filed under the experiment follows it
    in the same statement. Needs edit access on both projects. The experiment
    keeps its id and slug; address it under the new project afterwards.
    """
    with _client() as c:
        target = _ref(c, "experiment", experiment_id)
        _print_json(
            c.move_experiment(
                target.id,
                _project_id(c, to),
                from_project_id=_filed_under(target),
            )
        )


@experiment_app.command("list")
def experiment_list(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    #: RETIRED with the light experiments: an experiment's tags are read-only
    #: and the experiment list filters on none.
    tag: list[str] = typer.Option(None, "--tag", hidden=True),
    limit: int = typer.Option(50, "--limit", min=1, max=200),
    cursor: str = typer.Option(None, "--cursor", help="next_cursor from a previous page"),
) -> None:
    """List a project's experiments, newest first; without --project, every project's.

    Without --project this reads every project's list (one request each), so
    naming the project is faster.
    """
    if tag:
        raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY, param_hint="--tag")
    with _client() as c:
        page = c.list_experiments(
            project_id=_project_id(c, project) if project else None,
            limit=limit,
            cursor=cursor or None,
        )
    _print_json({"items": page.items, "next_cursor": page.next_cursor})


@experiment_app.command("tag", hidden=True)
def experiment_tag(
    experiment_id: str = slug_ref("experiment"),
    add: list[str] = typer.Argument(None, help="tags to add"),
    remove: list[str] = typer.Option(None, "--remove", help="tag to remove"),
    replace: list[str] = typer.Option(None, "--set", help="replace the whole list"),
) -> None:
    """RETIRED: an experiment's tags are read-only since it moved to its own record."""
    raise typer.BadParameter(_EXPERIMENT_TAGS_READ_ONLY)


@experiment_app.command("delete")
def experiment_delete(
    experiment_id: str = slug_ref("experiment"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
) -> None:
    """Move an experiment and its runs to the trash (Probe support can
    restore it for 21 days, then it is deleted for good). A server without the
    trash deletes it permanently, and the prompt says so."""
    _confirmed_delete(
        "experiment",
        experiment_id,
        yes=yes,
        cascade="every run, metric and file inside it goes too",
        trash=True,
    )


@experiment_app.command("edges")
def experiment_edges(experiment_id: str = slug_ref("experiment")) -> None:
    """Print every lineage edge under an experiment.

    Takes the slug, like `experiment get` and every other verb here: this was the
    one that still demanded a raw UUID, so the handle people are given rejected
    them on exactly one command. A bare UUID now needs the `id:` spelling the
    slug-default rule asks for everywhere else (refs.py), and says so.
    """
    with _client() as c:
        _print_json(c.experiment_edges(_ref(c, "experiment", experiment_id).id))


# -- run groups (sweeps / ensembles) ----------------------------------------
group_app = typer.Typer(
    no_args_is_help=True, help="run groups: sweeps, ensembles, distributed runs"
)
app.add_typer(group_app, name="group")


@group_app.command("create")
def group_create(
    experiment_id: str = typer.Argument(...),
    name: str = typer.Option(..., "--name"),
    kind: str = typer.Option("group", "--kind", help="e.g. sweep, ensemble"),
    spec: str = typer.Option(
        None, "--spec", metavar="JSON|@file", help="e.g. a sweep search space"
    ),
    notes: str = notes_opt(),
) -> None:
    """Create a run group. Pass the printed id to `probe run start --group`.

    Put free text in `--notes`, never in `--name`: the name is part of the
    group's uniqueness key within the experiment, so a description appended to it
    mints a SECOND group rather than annotating the one it describes.
    """
    with _client() as c:
        result = c.create_group(
            experiment_id, name, kind=kind, spec=_json_value(spec), notes=_text_value(notes)
        )
    _print_json(result)


@group_app.command("list")
def group_list(experiment_id: str = typer.Argument(...)) -> None:
    """List an experiment's run groups."""
    with _client() as c:
        _print_json(c.list_groups(experiment_id))


@group_app.command("get")
def group_get(group_id: str = typer.Argument(...)) -> None:
    """Print one run group."""
    with _client() as c:
        _print_json(c.get_group(group_id))


@group_app.command("set")
def group_set(
    group_id: str = typer.Argument(...),
    name: str = typer.Option(None, "--name"),
    spec: str = typer.Option(None, "--spec", metavar="JSON|@file"),
    notes: str = notes_opt(),
) -> None:
    """Update a run group's name, spec and/or notes.

    Notes are usually written HERE rather than at create: what a sweep or a
    campaign was actually testing, and what it concluded, is known once it has
    run. The spec says what was varied; the notes say what came of it.
    """
    if name is None and spec is None and notes is None:
        raise typer.BadParameter("pass at least one of --name/--spec/--notes")
    with _client() as c:
        result = c.update_group(
            group_id, name=name, spec=_json_value(spec), notes=_text_value(notes)
        )
    _print_json(result)


# -- lineage edges (fold #2) ------------------------------------------------
#: `edge add` end types named by slug (or `id:<uuid>`), resolved like `run move
#: --to`. An experiment IS a `projects` row, so the server stores both as the
#: one end type `project` (0278); the CLI keeps both words so a person can say
#: which they mean.
_PROJECT_END_TYPES = ("experiment", "project")

#: What `--source`/`--target` accept, in the order the help lists them.
_EDGE_END_TYPES = " | ".join(
    [*(t.value for t in LineageEntityType if t.value not in _PROJECT_END_TYPES), *_PROJECT_END_TYPES]
)

edge_app = typer.Typer(
    no_args_is_help=True,
    help=f"lineage edges ({_EDGE_END_TYPES.replace(' | ', '/')})",
)
app.add_typer(edge_app, name="edge")


def _edge_end(client: Client, end_type: str, ref: str) -> tuple[str, str]:
    """One `edge add` end as the server takes it: `experiment:`/`project:` by
    slug or `id:<uuid>` -> (`project`, its id); every other type's id as typed."""
    if end_type in _PROJECT_END_TYPES:
        return LineageEntityType.project.value, _ref(client, end_type, ref).id
    return end_type, ref


@edge_app.command("add")
def edge_add(
    source: str = typer.Option(
        ..., "--source", metavar="type:ref", help=f"type: {_EDGE_END_TYPES}"
    ),
    relation: str = typer.Option(
        ..., "--relation", help=" | ".join(r.value for r in LineageRelation)
    ),
    target: str = typer.Option(
        ..., "--target", metavar="type:ref", help=f"type: {_EDGE_END_TYPES}"
    ),
    provenance: str = typer.Option(
        None,
        "--provenance",
        help=(
            "how the edge is known: observed_call | human | inferred, plus, on a "
            "paper edge (where it is required), provider_citation: you found the "
            "paper in a reference list. Whether one paper's bibliography names "
            "another is a `cites` link (`probe paper citations`), not an edge."
        ),
    ),
    reason: str = typer.Option(None, "--reason", help="one sentence on why this edge exists"),
    evidence: list[str] = typer.Option(
        None,
        "--evidence",
        metavar="EVENT_ID",
        help="repeatable: the id of a session event this edge rests on "
        "(<stream>:<offset>:<index>, as the transcript shows it)",
    ),
) -> None:
    """Add a lineage edge.

    --source/--target are `type:ref`, with type in
    run|artifact|artifact_version|paper|experiment|project. A run, file or
    paper is named by its id; an experiment or project by its slug, or
    `id:<uuid>` (as `run move --to` takes it). Both are stored as the end type
    `project`: an experiment IS a project.

    A run may have more than one parent (forked_from, resumed_from,
    retried_from, branched_from): the first stays the run's parent, the others
    are added as edges. `supersedes` (between runs, projects and experiments)
    says the source's result replaces the target's; it is not a parent.

    A project or experiment end takes `derived_from` or `supersedes` (to or
    from a run, project or experiment) or `informed_by` (-> a paper), never a
    run's parent or a file relation.

    A PAPER edge REQUIRES --provenance: `discovered_via` (paper -> paper: source
    is the paper that was found, target the one it was found from) or
    `informed_by` (run, artifact or project -> the paper it drew on). Most of the time
    you want `probe paper add --via` instead, which records the paper and its
    discovery edge in one call; this verb is for correcting the graph
    afterwards.

    An edge that already exists is not an error: it prints that edge's id with
    `"already_linked": true` and exits 0. Any other refusal exits 1 with the
    server's reason.
    """
    st, _, sid = source.partition(":")
    tt, _, tid = target.partition(":")
    if not sid or not tid:
        raise typer.BadParameter("source/target must be `type:ref`")
    # Checked here so the failure names the flag rather than arriving as a 422
    # from the server. The server refuses it too -- this is the friendlier copy
    # of the same rule, never the only one.
    if (st == "paper" or tt == "paper") and not provenance:
        raise typer.BadParameter(
            "a paper edge needs --provenance: an edge you watched a tool make "
            "and one a model guessed are different claims, and the reader has "
            "to be able to tell them apart. Use one of: observed_call, "
            "provider_citation, human, inferred.",
            param_hint="--provenance",
        )
    meta = {"evidence": _edge_evidence(evidence)} if evidence else None
    with _client() as c:
        st, sid = _edge_end(c, st, sid)
        tt, tid = _edge_end(c, tt, tid)
        try:
            result = c.add_edge(
                source_type=st,
                source_id=sid,
                relation=relation,
                target_type=tt,
                target_id=tid,
                meta=meta,
                provenance=provenance,
                reason=reason,
            )
        except errors.ConflictError as exc:
            # The same edge (same ends, same relation) is already there: what
            # the caller wanted holds, so it is not a failure -- but it says so
            # and names the edge, rather than printing a row it did not write.
            # Any other 409 (a second genealogy parent) is a refusal: exit 1.
            from ..sdk.journal import edge_already_exists

            if not (exc.existing_id and edge_already_exists(exc)):
                raise
            linked: dict[str, Any] = {"already_linked": True, "id": exc.existing_id}
            # What this call carried beyond the edge itself stays on neither
            # edge: the one there keeps its own (the outbox's rule too).
            unapplied = [flag for flag, value in (("--reason", reason), ("--evidence", evidence),
                                                  ("--provenance", provenance)) if value]
            if unapplied:
                linked["applied"] = False
                typer.echo(f"probe: the edge already existed; its {', '.join(unapplied)} "
                           f"{'was' if len(unapplied) == 1 else 'were'} not applied to it", err=True)
            _print_json(linked)
            return
    _print_json(result)


#: A session event id as the Probe daemon's transcript shows it:
#: `<stream>:<offset>:<index>` (`probe/daemon/events.py`).
_EVENT_ID = re.compile(r"\S+:\d+:\d+")


def _edge_evidence(events: list[str]) -> list[dict]:
    """`--evidence` as `meta.evidence`: `{session, event}` per event id.

    An event id is local to one session's transcript, so it is stored with the
    session it came from, or the audit could not open it (lineage plan R7):
    the daemon's session (`PROBE_DAEMON_SESSION`), else the coding agent's own.
    With neither, the id names nothing anyone can open: a usage error."""
    session = os.environ.get("PROBE_DAEMON_SESSION") or agent_session.session_id_from_env()
    if not session:
        raise typer.BadParameter(
            "an event id is only meaningful with the session it came from, and this shell names "
            "none (no PROBE_DAEMON_SESSION, no coding-agent session): drop --evidence, or run it "
            "from the session",
            param_hint="--evidence",
        )
    out: list[dict] = []
    for raw in events:
        event = raw.strip()
        if not _EVENT_ID.fullmatch(event):
            raise typer.BadParameter(
                f"{raw!r} is not an event id: <stream>:<offset>:<index>, as the transcript shows it",
                param_hint="--evidence",
            )
        out.append({"session": session, "event": event})
    return out


@edge_app.command("remove")
def edge_remove(
    edge_id: str = typer.Argument(..., help="the edge id"),
) -> None:
    """Remove one lineage edge.

    The correction half of `edge add`. Matters most for paper discovery edges:
    they record how a reader got from one paper to another, so being wrong is an
    ordinary outcome, and a chain nobody can fix stops being believed.

    A run's PARENT is an edge too (forked_from, resumed_from, retried_from,
    branched_from), and a run may have several: removing its first parent makes
    the next-oldest one its parent, or clears it when none is left. A wrong
    parent is fixed by removing it and adding the right one. A wrong match on a
    file the run read is corrected instead with `probe run input dismiss|pin`.
    """
    with _client() as c:
        result = c.remove_edge(edge_id)
    _print_json(result)


# -- experiment versions (fold #6) ------------------------------------------
version_app = typer.Typer(no_args_is_help=True, help="immutable experiment version manifests")
app.add_typer(version_app, name="version")

# W&B import. Its own module because it owns a third-party dependency the rest of
# the CLI does not have: `wandb` is optional, and its absence must degrade the
# import rather than break `probe log`.
from .wandb_import import app as wandb_app  # noqa: E402

app.add_typer(wandb_app, name="wandb")


@version_app.command("create")
def version_create(
    experiment_id: str = typer.Argument(...),
    label: str = typer.Option(None, "--label"),
) -> None:
    """Mint an immutable experiment version (launch-time manifest)."""
    with _client() as c:
        result = c.experiment_version(experiment_id, label=label)
    _print_json(result)


@version_app.command("list")
def version_list(experiment_id: str = typer.Argument(...)) -> None:
    """List an experiment's versions."""
    with _client() as c:
        _print_json(c.list_experiment_versions(experiment_id))


# -- entrypoint -------------------------------------------------------------
#: Printed under `error: ...` when Probe refused the credential itself and the
#: Probe daemon ran the command (`PROBE_DAEMON_SESSION` is set). The daemon reads
#: this exact line as "my key was refused": it stops and hands the session back
#: (`probe/daemon/tools.py`). A 401, or a 403 naming a gone team or membership;
#: a 403 for a missing scope is an ordinary failure (`sdk/key_refusal.py`).
from ..sdk.key_refusal import KEY_REFUSED_LINE, credential_refused  # noqa: E402 -- kept beside its use


def _key_refused(exc: errors.RosError) -> bool:
    if isinstance(exc, (errors.WorkspaceLockedError, errors.UnroutableEndpointError)):
        return False
    return isinstance(exc, (errors.AuthError, errors.ScopeError)) and credential_refused(exc.status, str(exc))


def main(argv: list[str] | None = None) -> int:
    """Run the CLI, returning a process exit code (never calls sys.exit itself)."""
    from . import write_gate

    # A harness that puts no session id in its shells (Kimi Code): find the
    # session from the harness process before the write gate reads it.
    agent_session.adopt_harness_process_session()
    args, directed = write_gate.split_directed(sys.argv[1:] if argv is None else argv)
    refused = write_gate.refusal(args, directed=directed)
    if refused:
        child = write_gate.exec_child(args)
        if child is not None:
            state = session_marker.session_state(agent_session.session_id_from_env() or "")
            print(
                write_gate.EXEC_UNRECORDED.format(state=session_marker.state_label(state)),
                file=sys.stderr,
            )
            try:
                os.execvp(child[0], child)
            except OSError as exc:
                print(f"could not run {child[0]!r}: {exc}", file=sys.stderr)
                return 127
        print(refused, file=sys.stderr)
        return write_gate.EXIT_REFUSED
    try:
        result = app(args=args, prog_name="probe", standalone_mode=False)
        # NB: --help/--version/explicit typer.Exit don't raise here — click catches
        # Exit internally (standalone_mode=False) and RETURNS the code, so it flows
        # through the `return result` below. The except clauses catch what actually
        # propagates: usage errors (ClickException), Abort, model ValidationError.
    except typer.Exit as exc:  # defensive: a typer.Exit that does propagate
        return int(exc.exit_code)
    except typer.Abort:
        print("aborted", file=sys.stderr)
        return 1
    except ClickException as exc:  # usage / bad-parameter errors
        exc.show()
        return exc.exit_code or 2
    except ValidationError as exc:
        # A CLI string that fails the generated model's validation is a usage error,
        # not a crash: `--older-than 2026-07-01` is valid ISO 8601 but not an aware
        # datetime, and `--id abc` is not a UUID. Report it like one (exit 2).
        for err in exc.errors():
            field = ".".join(str(p) for p in err["loc"]) or exc.title
            print(f"error: invalid {field}: {err['msg']}", file=sys.stderr)
        return 2
    except errors.LimitReachedError as exc:
        # Handled ahead of RosError because a plan refusal is the one error here
        # that is not a mistake. The generic branch would print a single line that
        # reads like a failure; this one has to say what the ceiling is, that the
        # existing work is safe, and how to lift it -- the CTA is the whole reason
        # the limit exists.
        print(f"error: {exc}", file=sys.stderr)
        if exc.current is not None and exc.maximum is not None:
            print(f"       at {exc.current} of {exc.maximum}.", file=sys.stderr)
        print(
            "       Nothing was deleted and everything already recorded stays readable.",
            file=sys.stderr,
        )
        # The server's message already ENDS with the booking link, because it has
        # to stand alone for any client that does not special-case 402 (including
        # this CLI's own generic RosError branch). Printing our own copy under it
        # put the same URL on screen twice, which reads like a mistake rather than
        # emphasis. Only add the line when the message somehow lacks the link.
        if exc.booking_url and exc.booking_url not in str(exc):
            print(f"       Book 30 minutes: {exc.booking_url}", file=sys.stderr)
        return 1
    except errors.RosError as exc:
        print(f"error: {exc}", file=sys.stderr)
        if os.environ.get("PROBE_DAEMON_SESSION") and _key_refused(exc):
            print(KEY_REFUSED_LINE, file=sys.stderr)
        return 1
    except OSError as exc:
        # A bad local path is a usage error, not a crash. The upload commands take a
        # path and hash it before any request, and the anchored path is strict (no
        # fail-open spool to absorb it), so a typo would otherwise print a traceback.
        print(f"error: {exc}", file=sys.stderr)
        return 1
    except SystemExit as exc:  # defensive: coerce any stray SystemExit to a code
        code = exc.code
        if isinstance(code, int):
            return code
        if code is not None:
            print(str(code), file=sys.stderr)
            return 1
        return 0
    except Exception as exc:
        # Everything a user can do wrong has a branch above, so reaching here
        # means a BUG. Report it, then RE-RAISE: the traceback is what the
        # operator debugs from, and swallowing it to file a report would trade
        # their diagnosis for ours.
        from probe.cli import telemetry as telemetry_mod

        telemetry_mod.report_crash(exc, surface="cli", base_url=_conn.base_url)
        raise
    code = result if isinstance(result, int) else 0
    if code == 0 and _UNDELIVERED.lost:
        # A write that reached neither Probe nor the outbox: the command did
        # not do its job, whatever it printed (`_report_undelivered` said so).
        return 1
    return code


if __name__ == "__main__":
    raise SystemExit(main())
