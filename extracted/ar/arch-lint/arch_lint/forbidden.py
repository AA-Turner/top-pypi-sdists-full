from arch_lint.error import (
    BrokenArch,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)


def unauthorized_imports(
    forbidden: FullPathModule,
    allowlist: frozenset[FullPathModule],
    graph: ImportGraph,
) -> frozenset[FullPathModule]:
    illegal = graph.find_modules_that_directly_import(forbidden) - allowlist

    def _is_not_parent_of_allowed(module: FullPathModule) -> bool:
        return not any(module.is_descendant_of(a) for a in allowlist)

    return frozenset(filter(_is_not_parent_of_allowed, illegal))


def check_forbidden(
    forbidden_allow_list: dict[FullPathModule, frozenset[FullPathModule]],
    graph: ImportGraph,
) -> None:
    for forbidden, allowlist in forbidden_allow_list.items():
        illegal = unauthorized_imports(forbidden, allowlist, graph)
        if illegal:
            _illegal = frozenset(i.module for i in illegal)
            msg = (
                f"Forbidden module `{forbidden.module}` "
                f"imported by unauthorized modules i.e. {_illegal}"
            )
            raise BrokenArch(msg)
