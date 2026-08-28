"""``InMemoryStateStore`` -- the only :class:`~.store.StateStore` implementation for now.

``_contracts/09-tobe-engine-architecture.md`` §4 (**D6**): *durable state is out of scope;
the interface exists, the implementation doesn't*.  Everything nevertheless goes through
the seam, so a Redis backing is a later drop-in rather than a rewrite of every primitive.

The class is deliberately dull.  The only two interesting properties are the ones ``09``
§4 demands and the current engine lacks:

* keys are deterministic strings (**PY-9**), never ``hash()`` of anything;
* :meth:`InMemoryStateStore.end_window` and :meth:`InMemoryStateStore.clear` are different
  operations, distinguished by the :class:`~.store.Lifetime` recorded at write time rather
  than by which caller happened to invoke which method
  (``base_processor.py:126-131,182``).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Iterator

from matrice_analytics.engine.state.store import (
    KEY_SEPARATOR,
    Lifetime,
    StateLifetimeError,
    escape_component,
)

__all__ = ["InMemoryStateStore"]


@dataclass(slots=True)
class _Cell:
    """One stored value and the lifetime it was written with."""

    value: Any
    lifetime: Lifetime


class InMemoryStateStore:
    """A process-local :class:`~.store.StateStore`.

    A scoped view shares the parent's backing dict and only prepends a prefix, so a write
    through a view is visible from the root and :meth:`clear` on a view touches only that
    view's subtree.

    Insertion order is preserved (plain ``dict``), which makes :meth:`keys` -- and
    therefore every test that asserts on reset semantics -- deterministic.

    Example:
        >>> root = InMemoryStateStore()
        >>> stage = root.for_primitive("cam-1", "ppe_compliance", "global", "detect")
        >>> stage.set("total", 3, lifetime=Lifetime.WINDOW)
        >>> stage.incr("seen_ever", 3)
        3.0
        >>> stage.full_key("total")
        'cam-1/ppe_compliance/global/detect/total'
        >>> root.end_window()
        >>> stage.get("total"), stage.get("seen_ever")
        (None, 3.0)
    """

    __slots__ = ("_cells", "_prefix")

    def __init__(self, prefix: str = "") -> None:
        """Create a root store.

        Args:
            prefix: An optional root prefix, escaped as a single component.  Views are
                made with :meth:`scoped`, not by passing a joined string here.
        """
        self._cells: dict[str, _Cell] = {}
        self._prefix: str = escape_component(prefix) if prefix else ""

    # -- construction -------------------------------------------------------

    @classmethod
    def _view(cls, cells: dict[str, _Cell], prefix: str) -> "InMemoryStateStore":
        """Build a view over an existing backing without copying it."""
        view = cls.__new__(cls)
        view._cells = cells
        view._prefix = prefix
        return view

    def scoped(self, prefix: str) -> "InMemoryStateStore":
        """A view one level deeper.  ``prefix`` is one component and is escaped."""
        component = escape_component(prefix)
        joined = f"{self._prefix}{KEY_SEPARATOR}{component}" if self._prefix else component
        return self._view(self._cells, joined)

    def for_primitive(
        self, camera_id: str, app_id: str, zone: str, primitive: str
    ) -> "InMemoryStateStore":
        """The canonical ``<camera_id>/<app_id>/<zone>/<primitive>`` scope (``09`` §4).

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
        return self.scoped(camera_id).scoped(app_id).scoped(zone).scoped(primitive)

    # -- keys ---------------------------------------------------------------

    @property
    def prefix(self) -> str:
        """This view's absolute prefix, ``""`` at the root.

        See :attr:`~.store.StateStore.prefix`: this is the scope identity ``track`` seeds
        its id namespace from (**PY-9**), so it is a protocol member rather than an
        implementation detail of this class.
        """
        return self._prefix

    def full_key(self, key: str) -> str:
        """The absolute key a relative ``key`` resolves to.

        See :meth:`~.store.StateStore.full_key`.  Contractual because determinism is a
        property worth asserting on directly, and because a log line naming the absolute
        key is the difference between a five-minute and a five-hour debug session.
        """
        component = escape_component(key)
        return f"{self._prefix}{KEY_SEPARATOR}{component}" if self._prefix else component

    def _subtree(self) -> list[str]:
        """Absolute keys under this view, in insertion order."""
        if not self._prefix:
            return list(self._cells)
        marker = self._prefix + KEY_SEPARATOR
        return [key for key in self._cells if key.startswith(marker)]

    def keys(self, lifetime: Lifetime | None = None) -> Iterator[str]:
        """Keys in this subtree, relative to this view (see :meth:`~.store.StateStore.keys`)."""
        cut = len(self._prefix) + 1 if self._prefix else 0
        for key in self._subtree():
            if lifetime is None or self._cells[key].lifetime is lifetime:
                yield key[cut:]

    # -- reads --------------------------------------------------------------

    def get(self, key: str, default: Any = None) -> Any:
        """Read ``key``, or ``default`` when unset."""
        cell = self._cells.get(self.full_key(key))
        return default if cell is None else cell.value

    def lifetime_of(self, key: str) -> Lifetime | None:
        """The lifetime ``key`` was written with, or ``None`` if it is unset.

        Exists so a test -- or a reviewer -- can check that a per-window measurement was
        actually declared as one, which is the mistake ``09`` §4 rule 2 is about.
        """
        cell = self._cells.get(self.full_key(key))
        return None if cell is None else cell.lifetime

    # -- writes -------------------------------------------------------------

    def _resolve_lifetime(self, absolute: str, requested: Lifetime | None) -> Lifetime:
        """Pick the lifetime for a write, refusing to change an established one."""
        existing = self._cells.get(absolute)
        if requested is None:
            return existing.lifetime if existing is not None else Lifetime.PERSISTENT
        if existing is not None and existing.lifetime is not requested:
            raise StateLifetimeError(
                f"state key {absolute!r} was written as {existing.lifetime.value!r} and is "
                f"now being written as {requested.value!r}. A key's lifetime decides "
                f"whether end_window() clears it; changing it mid-run is the implicit "
                f"window-vs-cumulative confusion that 09 §4 rule 2 exists to remove. Use "
                f"two keys."
            )
        return requested

    def set(self, key: str, value: Any, *, lifetime: Lifetime | None = None) -> None:
        """Write ``key`` (see :meth:`~.store.StateStore.set`)."""
        absolute = self.full_key(key)
        self._cells[absolute] = _Cell(value, self._resolve_lifetime(absolute, lifetime))

    def incr(self, key: str, by: float = 1, *, lifetime: Lifetime | None = None) -> float:
        """Add ``by`` to a numeric key and return the new value.

        Raises:
            TypeError: The key holds a non-numeric value.  Silently replacing it would
                turn a type error into a wrong number, which is strictly worse.
        """
        absolute = self.full_key(key)
        resolved = self._resolve_lifetime(absolute, lifetime)
        cell = self._cells.get(absolute)
        current: float = 0.0
        if cell is not None:
            if isinstance(cell.value, bool) or not isinstance(cell.value, (int, float)):
                raise TypeError(
                    f"incr({key!r}) needs a numeric value; {absolute!r} currently holds "
                    f"{cell.value!r} ({type(cell.value).__name__})"
                )
            current = float(cell.value)
        updated = current + float(by)
        self._cells[absolute] = _Cell(updated, resolved)
        return updated

    def delete(self, key: str) -> None:
        """Remove ``key``.  A missing key is not an error."""
        self._cells.pop(self.full_key(key), None)

    # -- the two different clears (09 §4 rule 2) ----------------------------

    def end_window(self) -> None:
        """Clear :attr:`~.store.Lifetime.WINDOW` keys in this subtree; keep the rest.

        This is the 60-second aggregation boundary.  Cumulative totals survive it, because
        the backend's rollup formula assumes they only reset when the process does
        (**FROZEN-4**).
        """
        for key in self._subtree():
            if self._cells[key].lifetime is Lifetime.WINDOW:
                del self._cells[key]

    def clear(self) -> None:
        """Clear everything in this subtree -- a full reset, not a window boundary."""
        for key in self._subtree():
            del self._cells[key]

    # -- introspection ------------------------------------------------------

    def __len__(self) -> int:
        """Number of keys in this subtree."""
        return len(self._subtree())

    def __contains__(self, key: object) -> bool:
        return isinstance(key, str) and self.full_key(key) in self._cells

    def __repr__(self) -> str:
        return f"InMemoryStateStore(prefix={self._prefix!r}, keys={len(self)})"
