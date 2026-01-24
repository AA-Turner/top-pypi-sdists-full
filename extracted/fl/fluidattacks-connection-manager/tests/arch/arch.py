from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from fa_purity import FrozenList
from fluidattacks_etl_utils.typing import (
    Dict,
    FrozenSet,
    NoReturn,
    TypeVar,
)

_T = TypeVar("_T")


def raise_or_return(item: _T | Exception) -> _T | NoReturn:
    if isinstance(item, Exception):
        raise item
    return item


def _module(path: str) -> FullPathModule | NoReturn:
    return raise_or_return(FullPathModule.from_raw(path))


_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "fluidattacks_connection_manager": (
        ("_connection", "_common"),
        "_utils",
    ),
    "fluidattacks_connection_manager._connection": (
        "_setup",
        "_core",
    ),
}


def project_dag() -> DagMap:
    return raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {}
    return {_module(k): frozenset(_module(i) for i in v) for k, v in _raw.items()}
