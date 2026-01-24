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
    "snowflake_client": (
        "_factory",
        "_core",
    ),
    "snowflake_client._core": (
        "connection",
        "cursor",
        ("query", "clients"),
    ),
    "snowflake_client._factory": (("schema", "table", "connection", "cursor")),
    "snowflake_client._factory.table": (
        ("_methods", "_new"),
        ("_encode", "_assert"),
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
