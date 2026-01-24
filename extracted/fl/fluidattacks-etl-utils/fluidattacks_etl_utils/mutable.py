from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
    field,
)
from typing import (
    Generic,
    TypeVar,
)

from fa_purity import (
    Cmd,
    CmdUnwrapper,
    FrozenDict,
    Maybe,
)

_K = TypeVar("_K")
_V = TypeVar("_V")


@dataclass(frozen=True)
class _Private:
    pass


@dataclass(frozen=True)
class MutableMap(Generic[_K, _V]):
    _private: _Private = field(repr=False, hash=False, compare=False)
    _inner: dict[_K, _V]

    @staticmethod
    def new() -> Cmd[MutableMap[_K, _V]]:
        return Cmd.wrap_impure(lambda: MutableMap(_Private(), {}))

    def get(self, key: _K) -> Cmd[Maybe[_V]]:
        def _action() -> Maybe[_V]:
            if key in self._inner:
                return Maybe.some(self._inner[key])
            return Maybe.empty()

        return Cmd.wrap_impure(_action)

    def get_or(self, key: _K, if_not_exist: Cmd[_V]) -> Cmd[_V]:
        return self.get(key).bind(
            lambda m: m.map(lambda v: Cmd.wrap_value(v)).value_or(if_not_exist),
        )

    def override(self, key: _K, value: _V) -> Cmd[None]:
        def _action() -> None:
            self._inner[key] = value

        return Cmd.wrap_impure(_action)

    def get_or_create(self, key: _K, value: Cmd[_V]) -> Cmd[_V]:
        return self.get(key).bind(
            lambda m: m.map(lambda v: Cmd.wrap_value(v)).value_or(
                value.bind(lambda v: self.override(key, v).map(lambda _: v)),
            ),
        )

    def add_or(self, key: _K, value: _V, if_exist: Cmd[None]) -> Cmd[None]:
        def _action(unwrapper: CmdUnwrapper) -> None:
            if key not in self._inner:
                self._inner[key] = value
            else:
                unwrapper.act(if_exist)

        return Cmd.new_cmd(_action)

    def update(self, items: FrozenDict[_K, _V]) -> Cmd[None]:
        return Cmd.wrap_impure(lambda: self._inner.update(items))

    def freeze(self) -> Cmd[FrozenDict[_K, _V]]:
        return Cmd.wrap_impure(lambda: FrozenDict(self._inner))
