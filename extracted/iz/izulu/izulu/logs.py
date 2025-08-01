from __future__ import annotations

import collections
import copy
import functools
import types
import typing as t

from izulu import _utils


class BaseLogEvent(collections.UserString):
    __template__: t.ClassVar[str] = "Unspecified error"

    __cls_store: t.ClassVar[_utils.Store] = _utils.Store(
        fields=frozenset(),
        const_hints=types.MappingProxyType(dict()),
        inst_hints=types.MappingProxyType(dict()),
        consts=types.MappingProxyType(dict()),
        defaults=frozenset(),
    )

    def __init_subclass__(cls, **kwargs: t.Any) -> None:
        super().__init_subclass__(**kwargs)
        fields = frozenset(_utils.iter_fields(cls.__template__))
        const_hints, inst_hints = _utils.split_cls_hints(cls)
        consts = _utils.get_cls_defaults(cls, const_hints)
        defaults = _utils.get_cls_defaults(cls, inst_hints)
        cls.__cls_store = _utils.Store(
            fields=fields,
            const_hints=types.MappingProxyType(const_hints),
            inst_hints=types.MappingProxyType(inst_hints),
            consts=types.MappingProxyType(consts),
            defaults=frozenset(defaults),
        )

    def __init__(self, **kwargs: t.Any) -> None:
        self.__kwargs = kwargs.copy()
        self.__populate_attrs()
        self.data = self.__class__.__name__

    def __populate_attrs(self) -> None:
        """Set hinted kwargs as exception attributes"""
        for k, v in self.__kwargs.items():
            if k in self.__cls_store.inst_hints:
                setattr(self, k, v)

    def __process_template(self, data: dict[str, t.Any]) -> str:
        """Format the error template from provided data (kwargs & defaults)"""
        kwargs = self.__cls_store.consts.copy()
        kwargs.update(data)
        return _utils.format_template(self.__template__, kwargs)

    def _hook(
        self, store: _utils.Store, kwargs: dict[str, t.Any], msg: str
    ) -> str:
        return msg

    def __repr__(self) -> str:
        kwargs = _utils.join_kwargs(**self.as_dict())
        return f"{self.__module__}.{self.__class__.__qualname__}({kwargs})"

    def __copy__(self):
        return type(self)(**self.as_dict())

    def __deepcopy__(self, memo: dict[int, t.Any]):
        _id = id(self)
        if _id not in memo:
            kwargs = {
                k: copy.deepcopy(v, memo) for k, v in self.as_dict().items()
            }
            memo[_id] = type(self)(**kwargs)
        return memo[_id]

    def __reduce__(self) -> tuple[t.Any, ...]:
        return functools.partial(self.__class__, **self.as_dict()), tuple()

    def as_str(self) -> str:
        """Represent error as exception type with message"""
        return f"{self.__class__.__qualname__}: {self}"

    def as_kwargs(self) -> dict[str, t.Any]:
        """Return the copy of original kwargs used to initialize the error"""
        return self.__kwargs.copy()

    def as_dict(self, wide: bool = False) -> dict[str, t.Any]:
        """
        Represent error as dict of fields including default values

        By default, only *instance* data and defaults are provided.

        :param bool wide: if `True` *class* defaults will be included in result
        """
        d = self.__kwargs.copy()
        for field in self.__cls_store.defaults:
            d.setdefault(field, getattr(self, field))
        if wide:
            for field, const in self.__cls_store.consts.items():
                d.setdefault(field, const)
        return d
