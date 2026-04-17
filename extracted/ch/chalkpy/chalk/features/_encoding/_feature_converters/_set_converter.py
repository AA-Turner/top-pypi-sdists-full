from __future__ import annotations

from typing import (
    Any,
    Callable,
    ClassVar,
    Dict,
    Sequence,
    Tuple,
)

import pyarrow as pa

from ._list_converter import ListFeatureConverter
from ._base import FeatureConverter

# pyright: reportPrivateUsage=false, reportIncompatibleMethodOverride=false, reportMissingSuperCall=false, reportReturnType=false, reportUnnecessaryCast=false


class SetFeatureConverter(ListFeatureConverter):
    """Feature converter for Set[T], FrozenSet[T], and Tuple[T, ...].

    Subclasses ListFeatureConverter, inheriting all pyarrow/protobuf/JSON/coercion
    infrastructure.  The only additions are:
      - _sort: whether to sort the primitive list (True for set/frozenset)
      - _wrap_fn: the constructor used when converting primitive→rich (set/frozenset/tuple)

    Use :meth:`new` to obtain a (possibly cached) instance.
    """

    _set_cache: ClassVar[Dict[Tuple[Any, Any, bool], "SetFeatureConverter"]] = {}
    _sort: bool
    _wrap_fn: Callable

    @classmethod
    def new(
        cls,
        rich_type: type,
        default: "Any | ellipsis",
        is_nullable: bool,
        name: str = "",
        item_converter: "FeatureConverter | None" = None,
    ) -> "SetFeatureConverter":
        """Factory with caching for simple defaults (None / ...)."""
        from typing_extensions import get_args, get_origin
        import builtins

        origin = get_origin(rich_type)
        _sort = origin in (builtins.set, builtins.frozenset)
        _wrap_fn: Callable = (
            builtins.frozenset if origin is builtins.frozenset
            else builtins.tuple if origin is builtins.tuple
            else builtins.set
        )

        if item_converter is None:
            args = get_args(rich_type)
            item_rich_type = args[0] if args else ...
            from ._factory import make_feature_converter as _make_fc
            item_converter = _make_fc(name=None, is_nullable=True, rich_type=item_rich_type)

        if default is None or default is ...:
            key = (rich_type, default, is_nullable)
            cached = cls._set_cache.get(key)
            if cached is not None:
                return cached
            inst = cls.__new__(cls)
            ListFeatureConverter.__init__(inst, item_converter, default, is_nullable, list_rich_type=rich_type)
            inst._sort = _sort
            inst._wrap_fn = _wrap_fn
            cls._set_cache[key] = inst
            return inst

        inst = cls.__new__(cls)
        ListFeatureConverter.__init__(inst, item_converter, default, is_nullable, list_rich_type=rich_type)
        inst._sort = _sort
        inst._wrap_fn = _wrap_fn
        return inst

    # ── overrides ────────────────────────────────────────────────────────────

    def has_nontrivial_rich_type(self) -> bool:
        return True

    def _to_primitive(self, value: Any) -> list:
        result = super()._to_primitive(value)
        return sorted(result) if self._sort else result

    def from_primitive_to_rich(self, value: "list | None") -> Any:
        result = super().from_primitive_to_rich(value)
        return None if result is None else self._wrap_fn(result)

    def from_pyarrow_to_rich(self, values: "pa.Array | pa.ChunkedArray", /) -> Sequence[Any]:
        raw = super().from_pyarrow_to_rich(values)
        return [None if v is None else self._wrap_fn(v) for v in raw]

    def from_json_to_rich(self, value: Any) -> Any:
        result = super().from_json_to_rich(value)
        return None if result is None else self._wrap_fn(result)
