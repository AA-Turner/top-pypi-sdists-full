"""Foundation primitives shared by every manager and rich domain object (§5.4).

* :class:`_Manager` — base for managers; holds the shared engine, owns the
  error-mapping boundary (:meth:`_call`), and declares the capability hooks that
  rich objects delegate to.
* :class:`ClientHaving` — manager-binding mixin: carries ``_mgr`` and the zero-copy
  :meth:`_bind` that turns a generated DTO instance into its rich subclass.
* :class:`Page` — auto-paging iterator.
* :class:`Readable` / :class:`Archivable` / :class:`Shareable` / :class:`Taggable` /
  :class:`Classifiable` — object-level capability mixins whose methods delegate to
  their manager's hooks. Read/archive are v3-backed; access/control-tags/infosec are
  v2-backed (the manager dispatches by resource kind).
"""

from __future__ import annotations

import copy
import json
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Generic, TypeVar

import urllib3.exceptions
from pydantic import BaseModel

from istari_digital_client.sdk._exceptions import (
    APIConnectionError,
    DetachedInstanceError,
    IstariError,
    NotFoundError,
    OpenApiException,
    PermissionDeniedError,
)

from istari_digital_client.sdk._exceptions import map_api_error

if TYPE_CHECKING:
    from enum import Enum

    from istari_digital_client.sdk._engine import _Engine

T = TypeVar("T")
E = TypeVar("E", bound="Enum")


# Generated read endpoints all start with one of these; anything else is treated
# as a mutation for listing-cache invalidation. Allowlisting reads (not
# denylisting writes) is the safe default: an unrecognised verb over-clears (a
# harmless cache miss) rather than serving stale data after a write.
_READ_PREFIXES = ("get_", "list_", "search_")


def _is_read_call(fn: Callable[..., Any]) -> bool:
    """True if ``fn`` is a read-only generated endpoint (see ``_READ_PREFIXES``)."""
    return getattr(fn, "__name__", "").startswith(_READ_PREFIXES)


def coerce_enum(enum_cls: type[E], value: Any, *, param: str) -> Any:
    """Resolve ``value`` to a member of ``enum_cls`` case-insensitively.

    The generated client validates enum-valued params against the enum's *exact*
    value casing, so a plain string in the wrong case (``"ACTIVE"`` vs
    ``"active"``, ``"completed"`` vs ``"Completed"``) is rejected before the
    request is ever sent — and, worse, several of the enums this facade exposes
    disagree on casing (resource types are lowercase, job statuses are
    title-case). Weak models do not reliably reproduce the documented casing, so
    the facade accepts any case and maps it to the right member itself.

    ``None`` and values already of ``enum_cls`` pass through unchanged. An
    unrecognised value raises ``ValueError`` naming the valid options.
    """
    if value is None or isinstance(value, enum_cls):
        return value
    wanted = str(value).strip().lower()
    for member in enum_cls:
        if str(member.value).lower() == wanted:
            return member
    valid = ", ".join(str(m.value) for m in enum_cls)
    raise ValueError(f"{param} must be one of {valid} (case-insensitive); got {value!r}")


def _detached_manager() -> "_DetachedManager":
    """Pickle/copy factory: always resolve back to the shared sentinel."""
    return _DETACHED


class _DetachedManager:
    """Stand-in ``_mgr`` for objects detached by copy/serialization.

    A rich object's real manager holds a live client (connection pools, auth) and
    cannot survive :func:`copy.deepcopy`/``model_copy(deep=True)``/:mod:`pickle`.
    Those paths replace ``_mgr`` with this sentinel so the object keeps all of its
    data while any server-backed verb fails loudly with :class:`DetachedInstanceError`
    instead of a cryptic ``AttributeError``. It is a stateless singleton, so copying
    or pickling it is trivial and shares nothing.
    """

    __slots__ = ()

    def __reduce__(self) -> tuple[Any, tuple[()]]:
        return (_detached_manager, ())

    def __copy__(self) -> "_DetachedManager":
        return self

    def __deepcopy__(self, memo: Any) -> "_DetachedManager":
        return self

    def __getattr__(self, name: str) -> Any:
        # Let dunder probes (copy/pickle machinery) fail normally; raise a clear
        # error only for real manager-hook access (``_archive``, ``_read_contents`` …).
        if name.startswith("__") and name.endswith("__"):
            raise AttributeError(name)
        raise DetachedInstanceError(
            "This object is detached from its Istari client (it was copied or "
            "deserialized, e.g. handed between pipeline tasks). Re-fetch it via "
            "its manager (for example istari.jobs.get(id)) to perform server "
            "operations on it."
        )


_DETACHED = _DetachedManager()


def _detached_getstate(self: Any) -> dict[str, Any]:
    """``__getstate__`` that swaps transient manager refs for the sentinel.

    Reuses pydantic's own state, then replaces every name in ``_TRANSIENT_ATTRS``
    so copy/pickle never traverse the live client graph.
    """
    state = BaseModel.__getstate__(self)
    transient = type(self)._TRANSIENT_ATTRS
    d = state.get("__dict__")
    if d and any(k in d for k in transient):
        d = {**d, **{k: _DETACHED for k in transient if k in d}}
        state = {**state, "__dict__": d}
    return state


def _detached_deepcopy(self: Any, memo: Any = None) -> Any:
    # ``memo`` is optional because pydantic's model_copy(deep=True) calls this
    # with no argument, while copy.deepcopy passes the memo dict.
    cls: Any = type(self)
    new = cls.__new__(cls)
    new.__setstate__(copy.deepcopy(self.__getstate__(), memo))
    return new


def _detached_copy(self: Any) -> Any:
    cls: Any = type(self)
    new = cls.__new__(cls)
    new.__setstate__(copy.copy(self.__getstate__()))
    return new


class _Manager:
    """Base for managers: shared engine, error-mapping boundary, capability hooks."""

    def __init__(self, engine: _Engine) -> None:
        """Store the shared engine that holds the generated API handles."""
        self._engine = engine

    def _call(self, fn: Callable[..., T], /, *args: Any, **kwargs: Any) -> T:
        """Invoke a generated endpoint, mapping errors to ``IstariError``.

        ``OpenApiException`` maps by HTTP status; raw urllib3 transport failures
        (connection refused, DNS, connect/read timeout) map to ``APIConnectionError``
        so a network outage never surfaces a raw ``urllib3`` exception.

        When the opt-in listing cache is active, any *mutating* endpoint clears it
        after succeeding — the single chokepoint every manager write flows through,
        so one guard here busts stale listings for every write path.
        """
        try:
            result = fn(*args, **kwargs)
        except OpenApiException as exc:
            raise map_api_error(exc) from exc
        except urllib3.exceptions.HTTPError as exc:
            raise APIConnectionError(str(exc)) from exc
        cache = getattr(self._engine, "listing_cache", None)
        if cache is not None and not _is_read_call(fn):
            cache.clear()
        return result

    # --- Wrong-kind id self-healing (shared by every manager) --------------
    #
    # Callers routinely hand a manager the wrong *kind* of id — most often a
    # v2 *file* id where a v3 *resource* id is expected (the ai-chat backend
    # lists a system's tracked files and feeds those ids straight into resource
    # and job calls). The registry answers a wrong-kind id on a resource/job
    # route with a misleading **403**, not a 404, so the mistake reads as "you
    # don't have access" and the caller gives up. These helpers let any manager
    # treat a 403/404 as a cue to resolve the id and retry, so a wrong id fixes
    # itself no matter which call it was passed to.

    def _resource_id_from_file_id(self, candidate: str) -> str | None:
        """Best-effort: treat ``candidate`` as a v2 *file* id, return its resource id.

        Returns the resolved resource id, or ``None`` if the id is not a readable
        file or the file has no ``resource_id`` (a known nullable data gap). Any
        lookup failure yields ``None`` so the caller re-raises its original error
        rather than a confusing file-lookup error.
        """
        try:
            file = self._call(self._engine.v2_api.get_file, candidate)
        except IstariError:
            return None
        resource_id = getattr(file, "resource_id", None)
        if resource_id and resource_id != candidate:
            return resource_id
        return None

    def _call_healing_id(
        self, fn: Callable[..., T], resource_id: str, /, *args: Any, **kwargs: Any
    ) -> T:
        """Call ``fn(resource_id, *args, **kwargs)``, self-healing a wrong-kind id.

        On a 403/404 — the registry's misleading answer to a wrong-kind id — try
        to resolve ``resource_id`` as a file id to its owning resource id and
        retry the call once with the resolved id. Re-raises the original error if
        the id cannot be healed, so genuine permission/not-found errors surface
        unchanged.
        """
        try:
            return self._call(fn, resource_id, *args, **kwargs)
        except (PermissionDeniedError, NotFoundError):
            resolved = self._resource_id_from_file_id(resource_id)
            if resolved is None:
                raise
            return self._call(fn, resolved, *args, **kwargs)

    def _paginate(
        self,
        fetch: Callable[[str | None], Any],
        bind: Callable[[Any], T],
    ) -> "Page[T]":
        """Turn a cursor-paginated endpoint into an auto-paging :class:`Page`.

        ``fetch(cursor)`` returns one generated ``CursorPage*`` (``.items`` /
        ``.total`` / ``.next_page``); ``bind`` maps each raw item to its rich type.
        """

        def make(cursor: str | None, seen: frozenset[str]) -> "Page[T]":
            raw = fetch(cursor)
            items = [bind(item) for item in raw.items]
            # Stop before scheduling a cursor we've already requested on this path.
            # A genuine last page reports a falsy next_page; a broken endpoint can
            # instead cycle — either self-referentially (a -> a) or across several
            # tokens (a -> b -> a) — which, on empty pages, would loop next_page()
            # forever (iteration, or a bounded take() that never reaches its count).
            # ``seen`` holds the cursors already fetched leading here; revisiting any
            # of them terminates. It is threaded immutably (not a shared mutable set)
            # so re-iterating a Page re-walks fully instead of stopping early.
            nxt_cursor = raw.next_page
            has_next = (
                bool(nxt_cursor)
                and nxt_cursor != cursor  # self-reference (a -> a), caught this level
                and nxt_cursor not in seen  # multi-cursor cycle (a -> b -> a)
            )
            next_seen = seen | {cursor} if cursor is not None else seen
            nxt = (lambda: make(nxt_cursor, next_seen)) if has_next else None
            return Page(items, fetch_next=nxt, total=raw.total)

        return make(None, frozenset())

    def _paginate_offset(
        self,
        fetch: Callable[[int], Any],
        bind: Callable[[Any], T],
        start_page: int = 1,
    ) -> "Page[T]":
        """Turn an offset-paginated endpoint into an auto-paging :class:`Page`.

        ``fetch(page_num)`` returns one generated offset page (``.items`` /
        ``.total`` / ``.pages``); ``bind`` maps each raw item to its rich type.
        ``start_page`` specifies which page to start from (default 1).
        """

        def make(page_num: int) -> "Page[T]":
            raw = fetch(page_num)
            items = [bind(item) for item in (raw.items or [])]
            nxt = (lambda p=page_num + 1: make(p)) if page_num < raw.pages else None
            return Page(items, fetch_next=nxt, total=raw.total)

        return make(start_page)

    # Capability hooks — a manager whose objects use a capability mixin overrides the
    # ones it supports; the default makes an unwired capability fail loudly.
    def _read_contents(self, obj: Any) -> bytes:
        raise NotImplementedError

    def _archive(self, obj: Any, *, reason: str | None = None) -> None:
        raise NotImplementedError

    def _restore(self, obj: Any, *, reason: str | None = None) -> None:
        raise NotImplementedError

    def _create_access(
        self, obj: Any, *, subject_type: str, subject_id: str, relation: str
    ) -> Any:
        raise NotImplementedError

    def _update_access(
        self, obj: Any, *, subject_type: str, subject_id: str, relation: str
    ) -> Any:
        raise NotImplementedError

    def _remove_access(self, obj: Any, *, subject_type: str, subject_id: str) -> None:
        raise NotImplementedError

    def _list_access(self, obj: Any) -> list[Any]:
        raise NotImplementedError

    def _add_control_tags(
        self, obj: Any, tag_ids: list[str], *, reason: str | None = None
    ) -> list[Any]:
        raise NotImplementedError

    def _remove_control_tags(
        self, obj: Any, tag_ids: list[str], *, reason: str | None = None
    ) -> list[Any]:
        raise NotImplementedError

    def _list_control_tags(self, obj: Any) -> list[Any]:
        raise NotImplementedError

    def _assign_infosec_level(self, obj: Any, *, level: str) -> Any:
        raise NotImplementedError

    def _related_resources(
        self, obj: Any, *, relationship: str | None = None, direction: str = "outgoing"
    ) -> list[Any]:
        raise NotImplementedError


class ClientHaving:
    """Manager-binding mixin for rich domain objects.

    Rich types subclass their generated DTO plus this mixin plus capability mixins.
    ``_mgr`` is injected by the manager that produces the object via :meth:`_bind`
    (never a pydantic field), so it is never ``None`` in practice.

    ``_mgr`` holds a live client (connection pools, auth) and must not ride along
    when an object is copied or serialized — that would deep-copy/pickle the whole
    client graph (which explodes on unpicklable resources like locks, or silently
    duplicates auth state). :meth:`__init_subclass__` therefore stamps detach-safe
    ``__getstate__``/``__deepcopy__``/``__copy__`` onto every concrete rich class
    (stamping is required because pydantic's ``BaseModel`` precedes this mixin in
    the MRO, so an override defined here would never win). The copied/deserialized
    object keeps all of its data but is *detached*: its ``_mgr`` becomes the
    :data:`_DETACHED` sentinel and any server-backed verb raises
    :class:`DetachedInstanceError`. Re-attach with :meth:`_rebind`.
    """

    _mgr: _Manager
    #: Attribute names holding live manager references, swapped for the detached
    #: sentinel on copy/serialize. Subclasses that inject extra manager refs
    #: (e.g. Branch's ``_systems_mgr``) override this to include them.
    _TRANSIENT_ATTRS: ClassVar[frozenset[str]] = frozenset({"_mgr"})

    def __init_subclass__(cls, **kwargs: Any) -> None:
        """Stamp detach-safe state hooks onto each concrete rich class."""
        super().__init_subclass__(**kwargs)
        cls.__getstate__ = _detached_getstate  # type: ignore[method-assign]
        cls.__deepcopy__ = _detached_deepcopy  # type: ignore[attr-defined]
        cls.__copy__ = _detached_copy  # type: ignore[attr-defined]

    @classmethod
    def _bind(cls, dto: Any, *, mgr: _Manager) -> Any:
        """Bind a generated DTO instance to its manager, in place (zero-copy).

        Safety: rebinding requires ``cls`` to be a compatible subclass of the
        original DTO type or have structurally compatible fields. Incompatible
        rebinding may produce silently broken objects.
        """
        dto.__class__ = cls
        object.__setattr__(dto, "_mgr", mgr)
        return dto

    def _rebind(self, *, mgr: _Manager) -> Any:
        """Re-attach a live manager to a detached object, in place.

        Use on an object produced by copy/deserialization to make its
        server-backed verbs work again. Returns ``self`` for chaining.
        """
        object.__setattr__(self, "_mgr", mgr)
        return self


class Page(Generic[T]):
    """Auto-paging sequence over a collection.

    Iterating a Page — a ``for`` loop, ``list(page)``, or a comprehension —
    walks EVERY item across ALL pages, one request per page, and can time out on
    a large collection. To get a bounded result without walking everything, use:

    - ``take(n)`` — up to ``n`` items, fetching only as many pages as needed
      (the safe answer to "I just want N results");
    - ``first()`` — the first item (or ``None``), using only the current page;
    - ``.items`` — the current page's items only.

    Pass ``size=`` to the originating ``list()`` call to set the page size, so
    ``list(size=n).take(n)`` (or ``list(size=n).items``) is a single request.
    ``total`` is the full server-side count when the endpoint reports it;
    ``has_next()`` / ``next_page()`` walk pages explicitly.
    """

    def __init__(
        self,
        items: list[T],
        *,
        fetch_next: Callable[[], "Page[T] | None"] | None = None,
        total: int | None = None,
    ) -> None:
        """Wrap one page of already-bound ``items`` plus a next-page fetcher."""
        self._items = items
        self._fetch_next = fetch_next
        self.total = total

    @property
    def items(self) -> list[T]:
        """The items on the current page."""
        return self._items

    def has_next(self) -> bool:
        """Return whether another page is available."""
        return self._fetch_next is not None

    def next_page(self) -> "Page[T] | None":
        """Fetch the next page, or ``None`` if this is the last one."""
        return self._fetch_next() if self._fetch_next is not None else None

    def take(self, n: int) -> list[T]:
        """Return up to ``n`` items, fetching only as many pages as needed.

        The bounded, safe way to get "just N results": iterating a Page walks
        every page (one request each) and can time out, whereas ``take`` stops as
        soon as it has ``n`` items (or the data runs out), costing at most
        ``ceil(n / page_size)`` requests. Returns fewer than ``n`` only when the
        collection is smaller; ``n <= 0`` returns ``[]``. Pair with ``size=`` on
        the originating ``list()`` to also cap the page size
        (``list(size=n).take(n)`` is a single request).
        """
        if n <= 0:
            return []
        out: list[T] = []
        page: "Page[T] | None" = self
        while page is not None:
            out.extend(page._items[: n - len(out)])
            if len(out) >= n:
                break
            page = page.next_page()
        return out

    def first(self) -> "T | None":
        """Return the first item, or ``None`` if the collection is empty.

        Uses only the current page — no additional request.
        """
        return self._items[0] if self._items else None

    def __iter__(self) -> Iterator[T]:
        page: "Page[T] | None" = self
        while page is not None:
            yield from page._items
            page = page.next_page()


class Readable:
    """Capability: read the content of a content-token-backed object."""

    _mgr: _Manager

    def read_bytes(self) -> bytes:
        """Download this model/artifact/file's content as raw bytes.

        Aliases: download
        """
        return self._mgr._read_contents(self)

    def read_contents(self) -> bytes:
        """Alias of read_bytes() — download the content as raw bytes."""
        return self._mgr._read_contents(self)

    def read_text(self, encoding: str = "utf-8") -> str:
        """Read this resource's content as decoded text.

        Returns the whole file as a single string. For a large file, prefer to
        compute or search over the text in code — count matches, filter, extract the
        section you need — rather than passing the entire string around; the full
        content is here when you genuinely need it.
        """
        return self.read_bytes().decode(encoding)

    def read_json(self, encoding: str = "utf-8") -> Any:
        """Read this resource's content parsed as JSON."""
        return json.loads(self.read_bytes().decode(encoding))

    def copy_to(self, dest: str | Path) -> Path:
        """Download this resource's content to a local file path and return it."""
        path = Path(dest)
        path.write_bytes(self.read_bytes())
        return path


class Archivable:
    """Capability: archive / restore an object."""

    _mgr: _Manager

    def archive(self, reason: str | None = None) -> None:
        """Archive (soft-delete) this resource so it drops out of default listings.

        Mutates: true

        Aliases: delete remove
        """
        self._mgr._archive(self, reason=reason)

    def restore(self, reason: str | None = None) -> None:
        """Restore this object from the archive.

        Mutates: true

        **Note**: This method mutates backend state but does **not** return a
        refreshed object. The return type is explicitly ``None``. If you need
        the updated object after restore, call the manager's ``get()`` or
        ``restore(id)`` method, which returns a freshly-bound instance.
        """
        self._mgr._restore(self, reason=reason)


class Shareable:
    """Capability: manage who can access an object (delegates to manager hooks)."""

    _mgr: _Manager

    def create_access(
        self, *, subject_id: str, relation: str, subject_type: str = "user"
    ) -> Any:
        """Share this resource — grant a user or group access (viewer/editor/owner) by id.

        Mutates: true

        Aliases: share grant give provide permission
        """
        return self._mgr._create_access(
            self, subject_type=subject_type, subject_id=subject_id, relation=relation
        )

    def update_access(
        self, *, subject_id: str, relation: str, subject_type: str = "user"
    ) -> Any:
        """Change an existing subject's access relation.

        Mutates: true
        """
        return self._mgr._update_access(
            self, subject_type=subject_type, subject_id=subject_id, relation=relation
        )

    def remove_access(self, *, subject_id: str, subject_type: str = "user") -> None:
        """Revoke a subject's access.

        Mutates: true
        """
        self._mgr._remove_access(self, subject_type=subject_type, subject_id=subject_id)

    def list_access(self) -> list[Any]:
        """List who has access to this object and at what level.

        Answers "who has access", "what access does <user> have", and "at what
        level" — for a resource, job, or system. Returns one access relationship
        per subject (user or group) with the relation granted (viewer / editor /
        owner). Use this to see who can reach a specific object rather than
        listing every user.

        Aliases: permissions who access access-level role sharing shared-with
        """
        return self._mgr._list_access(self)


class Taggable:
    """Capability: control tags (delegates to manager hooks, dispatched by kind)."""

    _mgr: _Manager

    def add_control_tags(
        self, tag_ids: list[str], *, reason: str | None = None
    ) -> list[Any]:
        """Tag this resource — apply control tags by id.

        Mutates: true

        Aliases: tag label
        """
        return self._mgr._add_control_tags(self, tag_ids, reason=reason)

    def remove_control_tags(
        self, tag_ids: list[str], *, reason: str | None = None
    ) -> list[Any]:
        """Untag this resource — remove control tags by id.

        Mutates: true

        Aliases: untag
        """
        return self._mgr._remove_control_tags(self, tag_ids, reason=reason)

    def list_control_tags(self) -> list[Any]:
        """List this resource's tags (control taggings).

        Aliases: labels
        """
        return self._mgr._list_control_tags(self)


class Classifiable:
    """Capability: infosec level (delegates to manager hooks)."""

    _mgr: _Manager
    infosec_level: Any

    def assign_infosec_level(self, level: str) -> Any:
        """Classify this resource — set its security / sensitivity (infosec) level by id.

        Mutates: true

        Aliases: classify secure set
        """
        return self._mgr._assign_infosec_level(self, level=level)

    def get_infosec_level(self) -> Any:
        """Return this object's current infosec level (a readable field), if any.

        Aliases: classification level
        """
        return self.infosec_level


__all__ = [
    "Archivable",
    "Classifiable",
    "ClientHaving",
    "Page",
    "Readable",
    "Shareable",
    "Taggable",
    "coerce_enum",
]
