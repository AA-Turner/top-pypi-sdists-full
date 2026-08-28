"""The durability seam: the ``StateStore`` protocol, its key grammar and its lifetimes.

Normative source: ``_contracts/09-tobe-engine-architecture.md`` §4 (**D6**).

Three rules, each of which exists because the current engine breaks it:

1. **Nothing reaches for state any other way.**  A primitive holding a plain
   ``self._counts`` dict is a review defect, because it is invisible to a future Redis
   backing.  ``09`` §4.
2. **State keys are deterministic** (**PY-9**).  ``engine_session.py:499`` namespaces
   tracker state by ``str(hash(stream_key) % 1000000)``; ``hash()`` on a ``str`` is salted
   per process, so the namespace changes on every restart and no state can ever be
   recovered across one.  :func:`make_key` and :func:`stable_namespace` are the two
   sanctioned ways to derive a key, and both are pure functions of their inputs.
3. **Window-scoped and persistent state are distinguished at write time**
   (:class:`Lifetime`).  Today the distinction exists but is implicit in which method
   clears which field (``base_processor.py:126-131,182``), and getting it backwards is
   the single most common bug in custom code (``09`` §4 rule 2,
   ``ml-applications/guidelines/examples/04-queue-service-time/logic.py``).

🔒 Totals still mean "since last restart" (**FROZEN-4**).  This interface makes durability
*possible* later; it does not make it *safe* -- that needs a backend conversation.

Only :class:`~matrice_analytics.engine.state.memory.InMemoryStateStore` implements this
today.  A Redis implementation is a later drop-in behind the same protocol (backlog
**T6** decides the key granularity).
"""

from __future__ import annotations

import hashlib
from enum import Enum
from typing import Any, Iterator, Protocol, runtime_checkable

__all__ = [
    "KEY_SEPARATOR",
    "Lifetime",
    "StateKeyError",
    "StateLifetimeError",
    "StateStore",
    "escape_component",
    "make_key",
    "scope_key",
    "stable_namespace",
]


KEY_SEPARATOR = "/"
"""The one separator in the key grammar ``<camera_id>/<app_id>/<zone>/<primitive>/<name>``.

``09`` §4.  A component that contains the separator is escaped rather than rejected --
zone names are operator-drawn in the streaming UI and we do not control them.
"""


class StateKeyError(ValueError):
    """A key component is empty, blank or not a string.

    Loud rather than lenient: an empty component silently collapses two different scopes
    onto the same key (``cam1//zone`` and ``cam1/zone`` differ by one character), and the
    resulting cross-camera state bleed is invisible until the numbers are wrong.
    """


class StateLifetimeError(ValueError):
    """A key was written once as window-scoped and once as persistent.

    A key whose lifetime changes mid-run is precisely the ambiguity this module exists to
    remove (``09`` §4 rule 2), so it is an error rather than a last-write-wins race.
    """


class Lifetime(str, Enum):
    """When a key is cleared -- declared at write time, never inferred.

    ``09`` §4 rule 2: *window sums clear at window end; cumulative totals clear only on
    full reset*.  Today that distinction lives in which method happens to clear which
    field; here it is a property of the key itself, so
    :meth:`StateStore.end_window` and :meth:`StateStore.clear` cannot disagree about it.

    :attr:`PERSISTENT` is the default for a bare
    :meth:`~StateStore.set`.  That is deliberate: a value silently *surviving* a window
    boundary is a visible, debuggable wrong number, whereas a value silently *vanishing*
    at one presents as "the analytics are flaky".  Window scoping is opt-in and explicit.
    """

    WINDOW = "window"
    """Cleared by :meth:`StateStore.end_window` -- a measurement *of* the window.

    Per-window counters, sums and event lists.  Carrying one over double-counts.
    """

    PERSISTENT = "persistent"
    """Cleared only by :meth:`StateStore.clear` -- a fact about the world.

    Cumulative totals (FROZEN-4: "since last restart"), open track sessions, and anything
    whose clock must keep running across a window boundary.
    """


def escape_component(part: object) -> str:
    """Make one key component safe to join with :data:`KEY_SEPARATOR`.

    Injective: ``%`` becomes ``%25`` and ``/`` becomes ``%2F``, so two distinct zone names
    can never collide on one key.  Deterministic across processes (**PY-9**) -- no
    ``hash()``, no ``id()``, no iteration order.

    Args:
        part: The component, e.g. a camera id or an operator-drawn zone name.

    Returns:
        The escaped component.

    Raises:
        StateKeyError: The component is not a string, or is empty/whitespace.
    """
    if not isinstance(part, str):
        raise StateKeyError(
            f"state key component must be a string, got {type(part).__name__} ({part!r}); "
            "components are joined into a stable key and must not depend on repr()"
        )
    if not part.strip():
        raise StateKeyError(
            "state key component must be non-empty; an empty component collapses two "
            "different scopes onto one key and silently mixes state between them"
        )
    return part.replace("%", "%25").replace(KEY_SEPARATOR, "%2F")


def make_key(*parts: str) -> str:
    """Join components into a state key.

    Each argument is exactly **one** component and is escaped
    (:func:`escape_component`); a ``/`` inside an argument does not create a new level.

    Args:
        *parts: The components, outermost first.

    Returns:
        e.g. ``make_key("cam-1", "ppe", "Zone/A", "detect", "total")`` ->
        ``"cam-1/ppe/Zone%2FA/detect/total"``.

    Raises:
        StateKeyError: No components were given, or one is empty.
    """
    if not parts:
        raise StateKeyError("make_key() needs at least one component")
    return KEY_SEPARATOR.join(escape_component(part) for part in parts)


def scope_key(camera_id: str, app_id: str, zone: str, primitive: str) -> str:
    """Build the canonical four-level scope prefix from ``09`` §4.

    ``<camera_id>/<app_id>/<zone>/<primitive>``.  A value name appended to this gives the
    full five-level key.  The level order is what decides whether a future Redis backing
    is one key per camera or many (backlog **T6**), so it is fixed here rather than at
    each call site.

    Args:
        camera_id: The camera this session belongs to.
        app_id: ``manifest.app.id``.
        zone: A zone name, or ``"global"`` for single-bucket apps (never ``"__global__"``
            -- **PY-6**).
        primitive: The pipeline *stage* name, which is the primitive name unless the
            manifest gave the stage an explicit ``name:``.

    Returns:
        The escaped prefix.
    """
    return make_key(camera_id, app_id, zone, primitive)


def stable_namespace(key: str, digits: int = 6) -> str:
    """A short, deterministic numeric namespace derived from ``key``.

    The fix for **PY-9**.  ``engine_session.py:499`` uses ``str(hash(stream_key) % 1000000)``;
    ``hash()`` on a ``str`` is ``PYTHONHASHSEED``-salted, so the tracker namespace changes on
    every process start and nothing keyed by it survives a restart.  This uses ``hashlib``,
    so the same key gives the same namespace in every process, forever.

    Prefer the key itself (``09`` §4 rule 1).  This exists only for the callers that need a
    bounded-length token -- if you are choosing, choose :func:`make_key`.

    Args:
        key: Any stable identifier, e.g. the output of :func:`make_key`.
        digits: Length of the returned decimal token.

    Returns:
        A zero-padded decimal string of exactly ``digits`` characters.

    Raises:
        StateKeyError: ``key`` is empty or ``digits`` is not positive.
    """
    escape_component(key)  # reuse the emptiness/type check and its message
    if digits <= 0:
        raise StateKeyError(f"stable_namespace(digits={digits}) must be positive")
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()
    return str(int(digest, 16) % (10**digits)).zfill(digits)


@runtime_checkable
class StateStore(Protocol):
    """Every piece of primitive state goes through this, without exception (**D6**).

    ``09`` §4 gives four methods -- :meth:`get`, :meth:`set`, :meth:`incr`,
    :meth:`scoped`.  Three more are declared here because the doc's second rule ("``reset()``
    semantics are explicit") cannot be honoured without them: :meth:`end_window` and
    :meth:`clear` are the two *different* clears that ``base_processor.py`` conflates, and
    :meth:`keys` makes which-is-which assertable in a test.

    :attr:`prefix` and :meth:`full_key` are here because a store's **scope identity** is
    contractual, not incidental: the **PY-9** fix in
    :class:`~matrice_analytics.engine.primitives.track.Track` derives its track-id namespace
    from :attr:`prefix`, and a protocol that did not promise it would leave that fix resting
    on a ``getattr`` against whatever object it was handed.

    The ``lifetime=`` keyword on the two writers is optional and defaults to
    "whatever this key already is, else :attr:`Lifetime.PERSISTENT`", so the four-method
    surface in ``09`` §4 is source-compatible: ``state.set("completed", [])`` means exactly
    what an app author expects it to mean.

    Implementations are **not** thread-safe and do not need to be: a session is single
    threaded and a primitive that spawns a thread is a pathology being actively removed
    (``09`` §6, **PY-15**).
    """

    # -- scope identity -----------------------------------------------------

    @property
    def prefix(self) -> str:
        """This view's absolute key prefix, ``""`` at the root.

        Part of the contract rather than an implementation detail because it is the only
        **stable** name a primitive has for *where it is* -- and the fix for **PY-9** needs
        exactly that.  ``track`` seeds its id namespace with
        :func:`stable_namespace` over this prefix
        (``engine_session.py:499`` used ``hash(stream_key)``, which ``PYTHONHASHSEED``
        re-salts every process start); the prefix already encodes camera, app, zone and
        stage, so two scopes cannot collide and one scope gets the same seed forever.

        A backend that has no textual prefix must still answer with a stable string for its
        scope -- ``""`` only at the root -- because callers derive identity from it, not
        just log lines.
        """
        ...

    def full_key(self, key: str) -> str:
        """The absolute key a relative ``key`` resolves to, i.e. ``prefix`` + ``key``.

        Contractual for two reasons: determinism (**PY-9**) is a property worth asserting on
        directly, and a log line naming the absolute key is the difference between a
        five-minute and a five-hour debug session.  Escapes ``key`` as one component
        (:func:`escape_component`), so the result is always a valid key in the grammar.

        Raises:
            StateKeyError: ``key`` is not a non-empty string.
        """
        ...

    # -- values -------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Read ``key`` relative to this scope, or ``default`` when unset."""
        ...

    def set(self, key: str, value: Any, *, lifetime: Lifetime | None = None) -> None:
        """Write ``key`` relative to this scope.

        Args:
            key: The value name, relative to this scope.
            value: Any Python object.  In-memory today; a durable backing will need it to
                be serialisable, which is a good reason to keep it plain now.
            lifetime: :attr:`Lifetime.WINDOW` for a measurement of the current window,
                :attr:`Lifetime.PERSISTENT` for a fact that outlives it.  ``None`` keeps the
                key's existing lifetime, defaulting to
                :attr:`Lifetime.PERSISTENT` for a new key.
        """
        ...

    def incr(self, key: str, by: float = 1, *, lifetime: Lifetime | None = None) -> float:
        """Add ``by`` to a numeric key and return the new value."""
        ...

    def delete(self, key: str) -> None:
        """Remove ``key`` from this scope.  A missing key is not an error."""
        ...

    def scoped(self, prefix: str) -> "StateStore":
        """A view one level deeper, sharing the same backing.

        ``prefix`` is a single component and is escaped, so
        ``store.scoped(camera_id).scoped(app_id).scoped(zone).scoped(stage)`` reproduces
        :func:`scope_key`.
        """
        ...

    def end_window(self) -> None:
        """Clear every :attr:`Lifetime.WINDOW` key in this scope's subtree.

        The aggregation-window boundary.  Cumulative totals survive (**FROZEN-4**).
        """
        ...

    def clear(self) -> None:
        """Clear **everything** in this scope's subtree -- a full reset.

        Not the window boundary.  Calling this on the 60 s tick is the bug ``09`` §4 rule 2
        is written to prevent.
        """
        ...

    def keys(self, lifetime: Lifetime | None = None) -> Iterator[str]:
        """Iterate the keys in this scope's subtree, relative to this scope.

        Args:
            lifetime: Restrict to one lifetime, or ``None`` for all of them.

        Yields:
            Keys in insertion order, which is deterministic (**PY-9** in spirit: nothing
            here depends on a salted hash).
        """
        ...
