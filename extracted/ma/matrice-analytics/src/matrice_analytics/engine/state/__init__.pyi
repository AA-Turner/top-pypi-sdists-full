"""Stub file for engine.state directory."""
from typing import Any

# Constants
KEY_SEPARATOR: str = ...  # From store

# Functions
# From store
def escape_component(part: Any) -> str:
    """
    Make one key component safe to join with :data:`KEY_SEPARATOR`.
    
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
    ...

# From store
def make_key(*parts: Any) -> str:
    """
    Join components into a state key.
    
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
    ...

# From store
def scope_key(camera_id: str, app_id: str, zone: str, primitive: str) -> str:
    """
    Build the canonical four-level scope prefix from ``09`` §4.
    
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
    ...

# From store
def stable_namespace(key: str, digits: int = 6) -> str:
    """
    A short, deterministic numeric namespace derived from ``key``.
    
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
    ...

# Classes
# From memory
class InMemoryStateStore:
    # A process-local :class:`~.store.StateStore`.
    #
    #     A scoped view shares the parent's backing dict and only prepends a prefix, so a write
    #     through a view is visible from the root and :meth:`clear` on a view touches only that
    #     view's subtree.
    #
    #     Insertion order is preserved (plain ``dict``), which makes :meth:`keys` -- and
    #     therefore every test that asserts on reset semantics -- deterministic.
    #
    #     Example:
    #         >>> root = InMemoryStateStore()
    #         >>> stage = root.for_primitive("cam-1", "ppe_compliance", "global", "detect")
    #         >>> stage.set("total", 3, lifetime=Lifetime.WINDOW)
    #         >>> stage.incr("seen_ever", 3)
    #         3.0
    #         >>> stage.full_key("total")
    #         'cam-1/ppe_compliance/global/detect/total'
    #         >>> root.end_window()
    #         >>> stage.get("total"), stage.get("seen_ever")
    #         (None, 3.0)

    def __init__(self: Any, prefix: str = '') -> None:
        """
        Create a root store.
        
                Args:
                    prefix: An optional root prefix, escaped as a single component.  Views are
                        made with :meth:`scoped`, not by passing a joined string here.
        """
        ...

    def clear(self: Any) -> None:
        """
        Clear everything in this subtree -- a full reset, not a window boundary.
        """
        ...

    def delete(self: Any, key: str) -> None:
        """
        Remove ``key``.  A missing key is not an error.
        """
        ...

    def end_window(self: Any) -> None:
        """
        Clear :attr:`~.store.Lifetime.WINDOW` keys in this subtree; keep the rest.
        
                This is the 60-second aggregation boundary.  Cumulative totals survive it, because
                the backend's rollup formula assumes they only reset when the process does
                (**FROZEN-4**).
        """
        ...

    def for_primitive(self: Any, camera_id: str, app_id: str, zone: str, primitive: str) -> 'Any':
        """
        The canonical ``<camera_id>/<app_id>/<zone>/<primitive>`` scope (``09`` §4).
        
                Sugar for four :meth:`scoped` calls, kept in one place so the level *order* -- the
                thing backlog **T6** will reason about when choosing Redis key granularity -- is
                decided once rather than at every session setup.
        
                Args:
                    camera_id: The camera this session belongs to.
                    app_id: ``manifest.app.id``.
                    zone: A zone name or ``"global"`` (never ``"__global__"`` -- **PY-6**).
                    primitive: The pipeline stage name.
        
                Returns:
                    The scoped view a primitive is constructed with.
        """
        ...

    def full_key(self: Any, key: str) -> str:
        """
        The absolute key a relative ``key`` resolves to.
        
                See :meth:`~.store.StateStore.full_key`.  Contractual because determinism is a
                property worth asserting on directly, and because a log line naming the absolute
                key is the difference between a five-minute and a five-hour debug session.
        """
        ...

    def get(self: Any, key: str, default: Any = None) -> Any:
        """
        Read ``key``, or ``default`` when unset.
        """
        ...

    def incr(self: Any, key: str, by: float = 1) -> float:
        """
        Add ``by`` to a numeric key and return the new value.
        
                Raises:
                    TypeError: The key holds a non-numeric value.  Silently replacing it would
                        turn a type error into a wrong number, which is strictly worse.
        """
        ...

    def keys(self: Any, lifetime: Any | None = None) -> Any[str]:
        """
        Keys in this subtree, relative to this view (see :meth:`~.store.StateStore.keys`).
        """
        ...

    def lifetime_of(self: Any, key: str) -> Any | None:
        """
        The lifetime ``key`` was written with, or ``None`` if it is unset.
        
                Exists so a test -- or a reviewer -- can check that a per-window measurement was
                actually declared as one, which is the mistake ``09`` §4 rule 2 is about.
        """
        ...

    def prefix(self: Any) -> str:
        """
        This view's absolute prefix, ``""`` at the root.
        
                See :attr:`~.store.StateStore.prefix`: this is the scope identity ``track`` seeds
                its id namespace from (**PY-9**), so it is a protocol member rather than an
                implementation detail of this class.
        """
        ...

    def scoped(self: Any, prefix: str) -> 'Any':
        """
        A view one level deeper.  ``prefix`` is one component and is escaped.
        """
        ...

    def set(self: Any, key: str, value: Any) -> None:
        """
        Write ``key`` (see :meth:`~.store.StateStore.set`).
        """
        ...


# From store
class Lifetime:
    # When a key is cleared -- declared at write time, never inferred.
    #
    #     ``09`` §4 rule 2: *window sums clear at window end; cumulative totals clear only on
    #     full reset*.  Today that distinction lives in which method happens to clear which
    #     field; here it is a property of the key itself, so
    #     :meth:`StateStore.end_window` and :meth:`StateStore.clear` cannot disagree about it.
    #
    #     :attr:`PERSISTENT` is the default for a bare
    #     :meth:`~StateStore.set`.  That is deliberate: a value silently *surviving* a window
    #     boundary is a visible, debuggable wrong number, whereas a value silently *vanishing*
    #     at one presents as "the analytics are flaky".  Window scoping is opt-in and explicit.

    PERSISTENT: str
    WINDOW: str


# From store
class StateKeyError:
    # A key component is empty, blank or not a string.
    #
    #     Loud rather than lenient: an empty component silently collapses two different scopes
    #     onto the same key (``cam1//zone`` and ``cam1/zone`` differ by one character), and the
    #     resulting cross-camera state bleed is invisible until the numbers are wrong.

    ...

# From store
class StateLifetimeError:
    # A key was written once as window-scoped and once as persistent.
    #
    #     A key whose lifetime changes mid-run is precisely the ambiguity this module exists to
    #     remove (``09`` §4 rule 2), so it is an error rather than a last-write-wins race.

    ...

# From store
class StateStore:
    # Every piece of primitive state goes through this, without exception (**D6**).
    #
    #     ``09`` §4 gives four methods -- :meth:`get`, :meth:`set`, :meth:`incr`,
    #     :meth:`scoped`.  Three more are declared here because the doc's second rule ("``reset()``
    #     semantics are explicit") cannot be honoured without them: :meth:`end_window` and
    #     :meth:`clear` are the two *different* clears that ``base_processor.py`` conflates, and
    #     :meth:`keys` makes which-is-which assertable in a test.
    #
    #     :attr:`prefix` and :meth:`full_key` are here because a store's **scope identity** is
    #     contractual, not incidental: the **PY-9** fix in
    #     :class:`~matrice_analytics.engine.primitives.track.Track` derives its track-id namespace
    #     from :attr:`prefix`, and a protocol that did not promise it would leave that fix resting
    #     on a ``getattr`` against whatever object it was handed.
    #
    #     The ``lifetime=`` keyword on the two writers is optional and defaults to
    #     "whatever this key already is, else :attr:`Lifetime.PERSISTENT`", so the four-method
    #     surface in ``09`` §4 is source-compatible: ``state.set("completed", [])`` means exactly
    #     what an app author expects it to mean.
    #
    #     Implementations are **not** thread-safe and do not need to be: a session is single
    #     threaded and a primitive that spawns a thread is a pathology being actively removed
    #     (``09`` §6, **PY-15**).

    def clear(self: Any) -> None:
        """
        Clear **everything** in this scope's subtree -- a full reset.
        
                Not the window boundary.  Calling this on the 60 s tick is the bug ``09`` §4 rule 2
                is written to prevent.
        """
        ...

    def delete(self: Any, key: str) -> None:
        """
        Remove ``key`` from this scope.  A missing key is not an error.
        """
        ...

    def end_window(self: Any) -> None:
        """
        Clear every :attr:`Lifetime.WINDOW` key in this scope's subtree.
        
                The aggregation-window boundary.  Cumulative totals survive (**FROZEN-4**).
        """
        ...

    def full_key(self: Any, key: str) -> str:
        """
        The absolute key a relative ``key`` resolves to, i.e. ``prefix`` + ``key``.
        
                Contractual for two reasons: determinism (**PY-9**) is a property worth asserting on
                directly, and a log line naming the absolute key is the difference between a
                five-minute and a five-hour debug session.  Escapes ``key`` as one component
                (:func:`escape_component`), so the result is always a valid key in the grammar.
        
                Raises:
                    StateKeyError: ``key`` is not a non-empty string.
        """
        ...

    def get(self: Any, key: str, default: Any = None) -> Any:
        """
        Read ``key`` relative to this scope, or ``default`` when unset.
        """
        ...

    def incr(self: Any, key: str, by: float = 1) -> float:
        """
        Add ``by`` to a numeric key and return the new value.
        """
        ...

    def keys(self: Any, lifetime: Any | None = None) -> Any[str]:
        """
        Iterate the keys in this scope's subtree, relative to this scope.
        
                Args:
                    lifetime: Restrict to one lifetime, or ``None`` for all of them.
        
                Yields:
                    Keys in insertion order, which is deterministic (**PY-9** in spirit: nothing
                    here depends on a salted hash).
        """
        ...

    def prefix(self: Any) -> str:
        """
        This view's absolute key prefix, ``""`` at the root.
        
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

    def scoped(self: Any, prefix: str) -> 'Any':
        """
        A view one level deeper, sharing the same backing.
        
                ``prefix`` is a single component and is escaped, so
                ``store.scoped(camera_id).scoped(app_id).scoped(zone).scoped(stage)`` reproduces
                :func:`scope_key`.
        """
        ...

    def set(self: Any, key: str, value: Any) -> None:
        """
        Write ``key`` relative to this scope.
        
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


from . import memory, store