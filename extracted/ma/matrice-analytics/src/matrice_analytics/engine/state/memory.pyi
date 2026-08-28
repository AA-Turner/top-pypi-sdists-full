"""Auto-generated stub for module: memory."""
from typing import Any

# Classes
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

