"""this process's connection (root options) and the Probe clients built from it: direct or queued (--sync/--async), outbox journals, drainer kick, and the report of writes that did not land."""

from __future__ import annotations
import time
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ..sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from .. import __version__
from ..foundation.request_identity.request_identity import client_version_headers
from ..sdk.settings.settings import resolve
from ..sdk import session_marker
from ..foundation.request_identity.surface import Surface


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
    #: `--directed` anywhere after `probe` (stripped before the parser runs by
    #: `write_gate.split_directed`): the researcher asked for this write. The
    #: commands whose server write records it read it here (`summary push`,
    #: `visuals set`).
    directed: bool = False


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


def _client_class():
    """`Client`: a stand-in a test put there, else the SDK's."""
    if Client is not None:
        return Client
    from ..sdk.client.client import Client as sdk_client

    return sdk_client


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
    client = _client_class()(
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
    command as `queued` rather than recorded (`sdk/values/write_outcome.py`)."""
    from ..sdk.values import write_outcome

    is_queued = bool(entry.get("queued"))
    n = _UNDELIVERED.add(entry)
    if not _UNDELIVERED.due(is_queued):
        return
    line = (write_outcome.queued_line if is_queued else write_outcome.not_queued_line)(
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
    from ..sdk.delivery.journal.journal import Journal

    return Journal(_conn.spool_dir)


def _outbox_journals() -> list:
    """This process's outbox first, then every other one of this user on this
    machine (`Journal.discover`: ``rank-*`` dirs, the ``$TMPDIR`` fallback),
    unless ``--spool-dir`` names one (plan 1.5)."""
    from ..sdk.delivery.journal.journal import Journal

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
    from ..sdk.settings.settings import resolve

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


def _kick_drainer() -> None:
    from . import outbox_worker

    try:
        outbox_worker.maybe_spawn(_conn.spool_dir)
    except Exception:  # noqa: BLE001 -- delivery is best-effort; run end is the barrier
        pass


def begin_command(
    *, base_url: str | None = None, spool_dir: str | None = None, write_mode: bool | None = None
) -> None:
    """The per-command connection state, set before a command runs: by the root
    callback from its options, and by `probe.core` (which calls a command's
    function directly) with none of them."""
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
