import pytest

from arch_lint.error import BrokenArch
from arch_lint.graph import (
    FullPathModule,
    ImportGraph,
)
from arch_lint.private import (
    check_private,
)

root = "mock_module"


def test_private_check_case_1() -> None:
    graph = ImportGraph.build_graph(root, False)
    check_private(
        graph,
        FullPathModule.assert_module("mock_module.private_import.ok_case_1"),
    )


def test_private_check_case_2() -> None:
    graph = ImportGraph.build_graph(root, False)
    check_private(
        graph,
        FullPathModule.assert_module("mock_module.private_import.ok_case_2"),
    )


def test_private_check_fail_case_1() -> None:
    graph = ImportGraph.build_graph(root, False)
    with pytest.raises(BrokenArch) as err:
        check_private(
            graph,
            FullPathModule.assert_module("mock_module.private_import.fail_case_1"),
        )
    assert str(err.value) == (
        "Illegal import of private module "
        "mock_module.private_import.fail_case_1.main "
        "-> mock_module.private_import.fail_case_1.layer1._private"
    )


def test_private_check_fail_case_2() -> None:
    graph = ImportGraph.build_graph(root, False)
    with pytest.raises(BrokenArch) as err:
        check_private(
            graph,
            FullPathModule.assert_module("mock_module.private_import.fail_case_2"),
        )
    assert str(err.value) == (
        "Illegal import of private module "
        "mock_module.private_import.fail_case_2.foo2._private "
        "-> mock_module.private_import.fail_case_2.foo1._private"
    )
