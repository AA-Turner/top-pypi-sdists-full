"""Auto-generated stub for module: bootstrap."""
from typing import Any, Dict, Optional

from .response import CallFailure
from .transport import _rpc_data

# Constants
ACTION_DETAILS_PATH: str
ENV_ACTION_ID: str
ENV_ACTION_ID_BARE: str
ENV_LICENSE_KEY: str
USR_SRC: str
logger: Any

# Functions
def attach_session(session: Any = None) -> Any:
    """
    The session a client should ride on: the caller's, the process's, or ``None``.
    
        What every client in this package does at construction, in one place, because there are
        three of them and the shape below is easy to get subtly wrong.
    
        A client built on a machine with **no platform SDK** constructs successfully and has no
        session, rather than raising at construction. That is the intended outcome: an
        analytics-only container should be able to build one of these and skip the
        backend-dependent work, not die for want of a package it never meant to use.
    
        **Missing credentials are not the same as a missing SDK, and this does not conflate them.**
        An SDK that is absent means the caller never intended to reach the platform, so it
        degrades. Credentials that are absent mean the caller *did* intend to and cannot, so
        :func:`open_session` raises and that raise travels -- a silent ``None`` there would be
        reported three frames later as a missing session rather than as a missing key.
    
        **Why the import is inside the function.** The usual shape is a module-level
        ``try: from ... import Session`` with a ``Session = None`` fallback, and it has to be right
        in both halves -- the name bound on failure *and* every use checking it. Of the six sites
        in this repository that guard this import, two are broken in exactly that way: one never
        binds the name, so it raises ``NameError``; another sets its availability flag outside the
        ``try``, so the flag is always true and the call raises ``TypeError: 'NoneType' object is
        not callable``. Both surface far from the missing package. Importing here has no name to
        bind and no flag to keep in step, so neither mistake is available.
    
        Args:
            session: A session the caller already holds. Returned untouched -- a client handed one
                opens nothing of its own, which is what lets a test run with no platform at all.
            what: What the session is for, named in the log line and in any failure, so a reader
                sees which client wanted it.
    
        Returns:
            The session, or ``None`` when ``matrice_common`` is not importable.
    
        Raises:
            CallFailure: The SDK is present but no session could be opened -- no credentials in
                this process, or the exchange itself failed.
    """
    ...
def get_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, from every source there is.
    
        The four sources, cheapest first:
    
        1. ``$MATRICE_ACTION_ID`` -- an operator setting it means it,
        2. ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read,
        3. ``sys.argv`` -- py_compute launches every action container as
           ``python3 <entrypoint>.py <action_record_id> <port>``,
        4. the filesystem -- the working directory's name, its parents', then ``/usr/src``.
    
        The first three are :func:`resolve_action_id` and cost nothing. The fourth is
        :func:`scrape_action_id`, walks directories, and matches a looser shape, so it runs only
        when the first three have all missed -- which on a correctly launched container is never.
    
        Args:
            env: The environment to read. Defaults to the process's own.
            argv: The argument list to read. Defaults to the process's own.
    
        Returns:
            The id, or ``None`` when no source knew it. ``None`` is a refusal, not a default:
            a caller that invented one would read a different worker's record.
    """
    ...
def get_action_record(action_id: Optional[str] = None) -> Dict[str, Any]:
    """
    This worker's action record: one round trip on the first call, memory after that.
    
        ``action_id`` defaults to :func:`resolve_action_id` -- the action this container was
        launched as, which is the one every caller in it wants. Passing an id asks about a
        different action and gets its own entry. ``session`` lets a caller that already holds one
        read the record on it rather than on the process session; entries are keyed by action id
        alone, because the document does not depend on who read it.
    
        Raises :class:`~.response.CallFailure` when no id can be resolved, rather than answering
        with an empty record: a caller handed ``{}`` goes looking for a backend that dropped every
        field, when the fault is a container launched without its id.
    
        Read once and then kept for the life of the process, because the record describes a launch
        that has already finished -- reading it again cannot tell this process anything new -- and
        because every consumer wants the same one. A container running one usecase across forty
        cameras builds forty instances at startup, each needing ``jobParams``; without this that is
        forty GETs of one document through a connection pool of twenty, on the slowest path a
        container has. They arrive together, hence the same double-checked locking as
        :func:`get_session`. A failure is **not** kept, so a container that starts before the
        platform will answer recovers on the next call instead of stranding every camera in it.
        There is deliberately no every-call counterpart, for the same reason there is a cache at
        all: a session can go bad, a finished launch cannot.
    
        Returns the document as a plain ``dict``, deliberately untyped: this is the cache of what
        the platform said at launch, while the response models declare a fixed set of fields and
        rewrite some of the values they keep. Typing it here would drop a field the platform adds,
        at the one place whose whole purpose is to report what the container was handed. A caller wanting the
        typed view builds the model from this return value, and that order matters: building a
        model replaces only the outermost mapping and keeps the nested values exactly as they
        arrive, so a model built from the stored record would hand back objects that record still
        holds.
    
        **Every caller gets its own copy of the whole document, nested values included.** Copying
        only the outer dictionary is not enough here: every field callers read lives inside
        ``jobParams`` or ``actionDetails``, and those would still be the stored objects, so one
        caller editing a list in there would change what the next forty read. Copying all the way
        down is possible because the document holds nothing but dictionaries, lists, strings and
        numbers. A read-only view (``types.MappingProxyType``) is the obvious cheaper answer and
        the wrong one: it is not a ``dict``, so a caller that checks ``isinstance(..., dict)``
        before reading would reject it and substitute an empty document.
    
        Copying is affordable *because the call count is single-digit per consumer and nothing on
        the frame path reaches this*, and that condition matters because the cost is not flat: it
        tracks what ``actionDetails`` and ``jobParams`` carry, not how many fields the record has.
        A bare record copies in tens of microseconds, one carrying a site's camera list and zone
        polygons in hundreds. Forty consumers at startup is milliseconds; the same call in a
        per-frame loop is seconds per ten thousand frames. A caller needing it in a loop should
        read it once and hold it, and this docstring is the only thing that will say so.
    
        The reason to copy at all is a known one rather than a precaution: nothing here notices
        when the platform's ``status`` moves on, so the stored record is already out of date in
        that one field by design, and copying is what stops a caller correcting it by writing the
        new value onto a document every other consumer is reading.
    """
    ...
def get_session(what: str = 'the platform session') -> Any:
    """
    The process's one ``matrice_common`` session, built on first use.
    
        Lazy because a container that never needs the platform should never pay for a session, and
        should not fail at import time for want of credentials it does not use. Built once per
        *process*, not per caller: sessions are built from the same two environment variables
        wherever they are opened, so a second one is the same handle at the cost of another
        credential exchange.
    
        Thread-safe under the double-checked pattern -- the fast path is a bare read once the
        session exists, and the lock is taken only while the process is still cold.
    
        A failure is **not** kept: ``_SESSION`` is assigned only on success, so a container that
        starts before its credentials are mounted recovers on the next call instead of being stuck
        with the first error for its lifetime.
    """
    ...
def license_key(env: Optional[Any[str, str]] = None) -> str:
    """
    The deployment's licence key, or ``""`` when it has none.
    
        The cheapest thing in this module: one environment read, no ``argv``, no filesystem and no
        session. It is here rather than with the single route that sends it for the same reason
        :func:`resolve_action_id` is -- both answer *what was this container handed at startup?*, and
        a route that read its own credential would be resolving something it was supposed to be given.
    
        ``""`` is a real answer and not a fault. A deployment without a licence is the ordinary
        unlicensed case, and the caller's business is to take the other route rather than to report a
        misconfiguration -- which is why this returns a blank instead of raising, unlike everything
        else here. Keeping that decision at the call site is what makes the alternative visible.
    """
    ...
def open_session(what: str) -> Any:
    """
    A ``matrice_common`` session from the container's own credentials.
    
        Imported lazily, exactly as ``PostProcessingConfigClient.__init__`` does, so this module stays
        importable in an image with no platform SDK.
    
        Opens a **new** session every call. Callers that want one session for the life of the process
        use :func:`get_session` instead; this one stays uncached so that a caller who needs a session
        independent of anyone else's -- or a test that needs two -- can still get one.
    
        Credentials come from ``matrice_common.resolve_credentials``, which is the same three-tier
        order ``Session.__init__`` itself applies: an explicit argument, then the SDK's in-process
        registry, then the environment. Reading ``os.environ`` directly -- as this did until now --
        sees only the last of the three, so a container whose credentials were published to the
        registry by an SDK entry point was refused for want of variables it never needed to export.
        That is reachable rather than theoretical: ``Session`` used to copy explicit keys back into
        ``os.environ`` and deliberately stopped, because the environment is inherited by every
        subprocess and captured by most crash reporters.
    """
    ...
def resolve_action_id(env: Optional[Any[str, str]] = None, argv: Optional[Any[str]] = None) -> Optional[str]:
    """
    The action record id for this worker, from the three sources that cost nothing.
    
        Three sources, no I/O. ``$MATRICE_ACTION_ID`` first, because an operator setting it means it,
        then ``$ACTION_ID`` -- the bare name the Go services and the ENV_ID_ACTIONS images read, and the
        only one some py_compute launch paths emitted. Then ``sys.argv``: py_compute launches every
        action container as ``python3 <entrypoint>.py <action_record_id> <port>``, so the id is the
        first argument that looks like an ObjectId. Matching on shape rather than position keeps this
        from mistaking a port or a flag for an id.
    
        A malformed value in either env var falls through rather than erroring, so a truncated id does
        not mask a good one in argv.
    
        .. note::
           :func:`get_action_id` is the fuller answer: the same three sources and then a
           filesystem scrape. This one is kept because it is what every current caller expects
           and because *"no I/O"* is a property some of them rely on -- a truthiness probe that
           only wants to know whether a lookup is possible should not walk ``/usr/src`` to find
           out.
    """
    ...
def scrape_action_id(cwd: Optional[Any] = None, usr_src: Optional[Any] = None) -> Optional[str]:
    """
    The action id read off the filesystem, when nothing else knew it.
    
        py_compute names a container's working directory after the action it is running, and the
        image keeps a directory per action under ``/usr/src``. So the id is often sitting in a
        path name even on a container whose environment lost it -- which is the case this exists
        for, and the reason four modules grew their own copy of this.
    
        The working directory is checked first, then each of its parents outward, then the
        children of ``/usr/src``. Nearest-first: a worker running inside its own action's
        directory should answer with that action, not with whichever ``/usr/src`` entry happens
        to be listed first.
    
        **This one touches the filesystem**, which is why it is separate from
        :func:`resolve_action_id` rather than folded into it. A failure in either walk is
        non-fatal and falls through to the next: an unlinked working directory raises ``OSError``
        from ``Path.cwd()``, and ``/usr/src`` does not exist outside the container image.
    
        **It matches a looser shape than the other sources**, and deliberately: eight or more hex
        characters rather than a full 24-character ObjectId. That is what all four existing copies
        match, reproduced rather than tightened, because tightening it would change the behaviour
        of every caller being migrated onto this. The cost is real -- an eight-character hex
        directory name that is *not* an action id will be returned as one, and the read that
        follows will fail against the platform rather than here. It is the last source for that
        reason.
    
        Args:
            cwd: The directory to start from. Defaults to the process's own.
            usr_src: The image's action directory. Defaults to ``/usr/src``.
    
        Returns:
            The first candidate that looks like an id, or ``None``.
    """
    ...
