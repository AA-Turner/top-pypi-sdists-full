from arch_lint.dag import (
    DagMap,
)
from arch_lint.graph import (
    FullPathModule,
)
from fa_purity import (
    FrozenList,
)

from fluidattacks_integrates_dal._typing import (
    Dict,
    FrozenSet,
)

root = FullPathModule.assert_module("fluidattacks_integrates_dal")
_dag: Dict[str, FrozenList[FrozenList[str] | str]] = {
    "fluidattacks_integrates_dal": (
        "_cli",
        "list_groups",
        "clients",
        "client",
        ("core", "utils"),
        "_logger",
        "_typing",
    ),
    "fluidattacks_integrates_dal.clients": (("group", "organization"),),
}


def project_dag() -> DagMap:
    item = DagMap.new(_dag)
    if isinstance(item, Exception):
        raise item
    return item


def forbidden_allowlist() -> Dict[FullPathModule, FrozenSet[FullPathModule]]:
    _raw: Dict[str, FrozenSet[str]] = {}
    return {
        FullPathModule.assert_module(k): frozenset(FullPathModule.assert_module(i) for i in v)
        for k, v in _raw.items()
    }
