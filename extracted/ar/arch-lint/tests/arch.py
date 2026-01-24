from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)

_dag: dict[str, tuple[tuple[str, ...] | str, ...]] = {
    "arch_lint": (
        ("dag", "forbidden", "private"),
        "graph",
        "_full_path",
        ("error", "_utils"),
    ),
    "arch_lint.dag": (
        "check",
        "_dag_map",
        "_dag",
    ),
}


def project_dag() -> DagMap:
    result = DagMap.new(_dag)
    if isinstance(result, Exception):
        raise result
    return result


def forbidden_allowlist() -> dict[FullPathModule, frozenset[FullPathModule]]:
    _raw: dict[str, frozenset[str]] = {
        "grimp": frozenset(["arch_lint.graph"]),
    }
    return {
        FullPathModule.assert_module(k): frozenset(FullPathModule.assert_module(i) for i in v)
        for k, v in _raw.items()
    }
