from __future__ import (
    annotations,
)

from dataclasses import (
    dataclass,
)

from arch_lint import (
    _utils,
)
from arch_lint._full_path import (
    FullPathModule,
)

from ._dag import (
    DAG,
)


@dataclass(frozen=True)
class _DagMap:
    items: dict[FullPathModule, DAG]


@dataclass(frozen=True)
class DagMap:
    """Defines a map between a module and its associated dag."""

    _inner: _DagMap

    def get(self, module: FullPathModule) -> DAG | None:
        return self._inner.items.get(module)

    def all_dags(self) -> frozenset[DAG]:
        return frozenset(self._inner.items.values())

    @staticmethod
    def new(
        raw: dict[str, tuple[tuple[str, ...] | str, ...]],
    ) -> DagMap | Exception:
        result: dict[FullPathModule, DAG] = {}

        def _process(key: str, value: tuple[tuple[str, ...] | str, ...]) -> None | Exception:
            parent = FullPathModule.from_raw(key)
            if isinstance(parent, Exception):
                return parent
            _parent = parent
            _items = _utils.transform_items(
                value,
                lambda i: _utils.transform_items(_utils.to_tuple(i), _parent.assert_child),
            )
            if isinstance(_items, Exception):
                return _items
            items = _utils.transform_items(_items, lambda s: _utils.assert_set(s, lambda x: str(x)))
            if isinstance(items, Exception):
                return items
            dag = DAG.from_full_paths(items)
            if isinstance(dag, Exception):
                return dag
            result[parent] = dag
            return None

        for key, value in raw.items():
            _result = _process(key, value)
            if isinstance(_result, Exception):
                return _result
        return DagMap(_DagMap(result))
