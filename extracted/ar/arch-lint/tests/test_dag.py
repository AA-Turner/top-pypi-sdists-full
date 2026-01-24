import pytest

from arch_lint.dag import (
    DagMap,
)
from arch_lint.dag.check import (
    check_dag_map,
)
from arch_lint.error import BrokenArch
from arch_lint.graph import (
    ImportGraph,
)

root = "mock_module"


def _build_project_dag(
    raw: dict[str, tuple[tuple[str, ...] | str, ...]],
) -> DagMap:
    result = DagMap.new(raw)
    if isinstance(result, Exception):
        raise result
    return result


def test_dag() -> None:
    graph = ImportGraph.build_graph(root, True)
    project_dag = _build_project_dag(
        {
            "mock_module.dag_check.layers": ("foo2", "foo1"),
        },
    )
    check_dag_map(project_dag, graph)


def test_dag_fail() -> None:
    graph = ImportGraph.build_graph(root, False)
    project_dag = _build_project_dag(
        {
            "mock_module.dag_check.layers": ("foo1", "foo2"),
        },
    )
    with pytest.raises(BrokenArch) as err:
        check_dag_map(project_dag, graph)
    assert str(err.value) == (
        "Broken DAG with illegal import mock_module.dag_check.layers.foo2 "
        "-> mock_module.dag_check.layers.foo1 "
        "i.e. chain (mock_module.dag_check.layers.foo2, "
        "mock_module.dag_check.layers.foo1)"
    )


def test_dag_fail_independence() -> None:
    graph = ImportGraph.build_graph(root, False)
    project_dag = _build_project_dag(
        {
            "mock_module.dag_check.layers": (("foo2", "foo1"),),
        },
    )
    with pytest.raises(BrokenArch) as err:
        check_dag_map(project_dag, graph)
    assert str(err.value) == (
        "Broken DAG same lvl modules should be independent "
        "mock_module.dag_check.layers.foo2 -> "
        "mock_module.dag_check.layers.foo1"
    )
