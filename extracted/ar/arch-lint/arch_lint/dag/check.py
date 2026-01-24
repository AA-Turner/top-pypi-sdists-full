from collections.abc import Callable
from pathlib import (
    Path,
)

from arch_lint import (
    _utils,
)
from arch_lint.error import (
    BrokenArch,
)
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)

from ._dag import (
    DAG,
)
from ._dag_map import (
    DagMap,
)


def _chain_exist(
    graph: ImportGraph,
    importer: frozenset[FullPathModule],
    imported: frozenset[FullPathModule],
) -> tuple[FullPathModule, FullPathModule] | None:
    for s in importer:
        for t in imported:
            if graph.chain_exists(s, t, True):
                return (s, t)
    return None


def _independence(
    graph: ImportGraph,
    modules: frozenset[FullPathModule],
) -> tuple[FullPathModule, FullPathModule] | None:
    for m in modules:
        checks = modules - frozenset([m])
        for c in checks:
            if graph.chain_exists(m, c, True):
                return (m, c)
    return None


def _check_independence(
    graph: ImportGraph,
    modules: frozenset[FullPathModule],
) -> None:
    result = _independence(graph, modules)
    if result:
        msg = (
            "Broken DAG same lvl modules should be independent "
            f"{result[0].module} -> {result[1].module}"
        )
        raise BrokenArch(
            msg,
        )


def _check_dag_over_modules(
    graph: ImportGraph,
    lower: frozenset[FullPathModule],
    upper: frozenset[FullPathModule],
) -> None:
    _chain = _chain_exist(graph, lower, upper)
    if _chain:
        importer = _chain[0]
        imported = _chain[1]
        specific = graph.find_shortest_chain(importer, imported)
        msg = (
            "Broken DAG with illegal import "
            f"{importer.module} -> {imported.module} i.e. chain {specific}"
        )
        raise BrokenArch(msg)


def dag_completeness(dag: DAG, graph: ImportGraph, parent: FullPathModule) -> None:
    children = graph.find_children(parent)
    missing = children - dag.all_modules
    if len(children) > 1 and missing:
        relative = ",".join(d.name for d in missing)
        msg = f"Missing children modules of `{parent}` at DAG i.e. {relative}"
        raise BrokenArch(msg)


def dag_completeness_from_set(
    dag: DAG,
    expected: frozenset[FullPathModule],
    raise_if_excess: bool,
) -> None:
    diff = expected - dag.all_modules
    if diff:
        relative = ",".join(d.name for d in diff)
        msg = f"Missing root modules i.e. {relative}"
        raise BrokenArch(msg)
    diff_2 = dag.all_modules - expected
    if diff_2 and raise_if_excess:
        relative_2 = ",".join(d.name for d in diff_2)
        msg = f"Not listed modules i.e. {relative_2}"
        raise BrokenArch(msg)


def dag_completeness_from_dir(
    dag: DAG,
    dir_path: Path,
    raise_if_excess: bool,
    parent: FullPathModule | None,
    path_filter: Callable[[Path], bool] = lambda _: True,
) -> None:
    """
    Check a DAG object completeness.

    The elements of the `dir_path` are the complete expected list of modules.

    - `dir_path` children are transformed into FullPathModule
    using children name as the module name.
    - if `parent` is provided then the FullPathModule object from
    `dir_path` children will be expected to be children of `parent`
    - `path_filter` used to filter the children of `dir_path` that
    will be transformed
    """

    def _to_module(raw: str) -> FullPathModule | Exception:
        if parent:
            return parent.assert_child(raw)
        return FullPathModule.from_raw(raw)

    if dir_path.is_dir():
        expected = _utils.transform_sets(
            frozenset(p.name for p in filter(path_filter, dir_path.iterdir())),
            _to_module,
        )
        if isinstance(expected, Exception):
            raise expected
        return dag_completeness_from_set(dag, expected, raise_if_excess)
    msg = "Expected a dir path"
    raise BrokenArch(msg)


def dag_map_completeness(
    dag_map: DagMap,
    graph: ImportGraph,
    parent: FullPathModule,
) -> None:
    """
    Check a DAG object completeness.

    - all modules should have all their children listed when having >1 children.
    """
    parent_dag = dag_map.get(parent)
    children = graph.find_children(parent)
    if not parent_dag and len(children) > 1:
        msg = f"Missing module at DagMap i.e. {parent}"
        raise BrokenArch(msg)
    if parent_dag:
        dag_completeness(parent_dag, graph, parent)
    for c in children:
        dag = dag_map.get(c)
        if not dag and len(graph.find_children(c)) > 1:
            msg = f"Missing module at DagMap i.e. {c}"
            raise BrokenArch(msg)
        if dag:
            dag_completeness(dag, graph, c)
        dag_map_completeness(dag_map, graph, c)


def check_dag(
    dag: DAG,
    graph: ImportGraph,
) -> None:
    """
    Check DAG compliance.

    - firsts items are at higher layers
    - latest items are at lower layers
    - a module form a layer cannot import modules from layers >= than itself
    """
    for n, c in enumerate(dag.layers):
        _check_independence(graph, c)
        for lower_modules in dag.layers[n + 1 :]:
            _check_dag_over_modules(
                graph,
                lower_modules,
                c,
            )


def check_dag_map(
    dag_map: DagMap,
    graph: ImportGraph,
) -> None:
    for d in dag_map.all_dags():
        check_dag(d, graph)
