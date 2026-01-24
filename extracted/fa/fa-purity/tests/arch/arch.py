from typing import (
    TypeVar,
)

from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)

from fa_purity import (
    FrozenList,
)

_dag: dict[str, FrozenList[FrozenList[str] | str]] = {
    "fa_purity": (
        ("date_time", "lock", "json"),
        "_transform",
        "_core",
        "_bug",
    ),
    "fa_purity._core": (
        "unsafe",
        "stream",
        "pure_iter",
        "iter_factory",
        "maybe",
        ("frozen", "result", "cmd"),
        "bool",
        ("coproduct", "unit"),
        "utils",
    ),
    "fa_purity._core.stream": (
        "_factory",
        "_core",
    ),
    "fa_purity._core.pure_iter": (
        "_factory",
        "_core",
    ),
    "fa_purity._transform": (
        ("stream", "pure_iter"),
        ("cmd", "cmd_smash"),
        ("result", "result_smash"),
        "coproduct",
    ),
    "fa_purity.json": (
        "_transform",
        "_core",
    ),
    "fa_purity.json._core": (
        "value",
        "primitive",
    ),
    "fa_purity.json._transform": (
        "value",
        "primitive",
    ),
    "fa_purity.json._transform.primitive": (
        "_transform",
        "_factory",
    ),
    "fa_purity.json._transform.value": (
        "_transform",
        "_factory",
    ),
    "fa_purity.json._transform.value._factory": (
        "_unfolded_factory",
        "_jval_factory",
        "_common",
    ),
}
_T = TypeVar("_T")


def raise_or_return(item: Exception | _T) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


def project_dag() -> DagMap:
    return raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> dict[FullPathModule, frozenset[FullPathModule]]:
    _raw: dict[str, frozenset[str]] = {}
    return {
        raise_or_return(FullPathModule.from_raw(k)): frozenset(
            raise_or_return(FullPathModule.from_raw(i)) for i in v
        )
        for k, v in _raw.items()
    }
