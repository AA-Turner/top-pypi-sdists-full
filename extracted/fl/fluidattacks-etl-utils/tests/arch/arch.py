from typing import (
    TypeVar,
)

from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)

_T = TypeVar("_T")


def raise_or_return(item: _T | Exception) -> _T:
    if isinstance(item, Exception):
        raise item
    return item


def _module(path: str) -> FullPathModule:
    return raise_or_return(FullPathModule.from_raw(path))


_dag: dict[str, tuple[tuple[str, ...] | str, ...]] = {
    "fluidattacks_etl_utils": (
        "secrets",
        (
            "natural",
            "smash",
            "decode",
            "process",
            "parallel",
            "retry",
            "mutable",
            "env_var",
            "paginate",
            "date_range",
            "unit_helpers",
            "table_utils",
            "handle_errors",
        ),
        "typing",
        "bug",
    ),
    "fluidattacks_etl_utils.secrets": (
        ("_integrates", "_snowflake", "_zoho_leads"),
        "_core",
    ),
}


def project_dag() -> DagMap:
    return raise_or_return(DagMap.new(_dag))


def forbidden_allowlist() -> dict[FullPathModule, frozenset[FullPathModule]]:
    _raw: dict[str, frozenset[str]] = {
        "os": frozenset({"fluidattacks_etl_utils.env_var"}),
    }
    return {_module(k): frozenset(_module(i) for i in v) for k, v in _raw.items()}
