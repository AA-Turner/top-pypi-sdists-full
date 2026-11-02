"""Tests for _find_reverse_dependent_test_paths."""

from __future__ import annotations

import pytest

from agentic_devtools.cli.checks.changed_files import _find_reverse_dependent_test_paths


def _write_module(root, path: str, content: str) -> None:
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(content, encoding="utf-8")


def test_direct_import_selects_test_outside_colocated_tree(tmp_path) -> None:
    """Selects a cross-tree test that imports the changed product module."""
    _write_module(tmp_path, "agentic_devtools/widget.py", "class Widget: ...\n")
    _write_module(
        tmp_path,
        "tests/unit/other/test_widget_consumer.py",
        "from agentic_devtools.widget import Widget\nimport json\n",
    )

    assert _find_reverse_dependent_test_paths(["agentic_devtools/widget.py"], cwd=tmp_path) == [
        "tests/unit/other/test_widget_consumer.py"
    ]


def test_transitive_relative_import_cycle_selects_test(tmp_path) -> None:
    """Traverses relative imports and terminates when product modules cycle."""
    _write_module(tmp_path, "agentic_devtools/app.py", "from . import middle\n")
    _write_module(tmp_path, "agentic_devtools/middle.py", "from . import app\n")
    _write_module(tmp_path, "tests/unit/test_cycle.py", "from agentic_devtools import middle\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/app.py"], cwd=tmp_path) == ["tests/unit/test_cycle.py"]


def test_relative_test_import_selects_transitive_consumer(tmp_path) -> None:
    """Resolves relative test imports to an intermediate module."""
    _write_module(tmp_path, "agentic_devtools/service.py", "class Service: ...\n")
    _write_module(tmp_path, "tests/helpers.py", "from agentic_devtools import service\n")
    _write_module(tmp_path, "tests/unit/test_relative.py", "from .. import helpers\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/service.py"], cwd=tmp_path) == [
        "tests/unit/test_relative.py"
    ]


def test_reachable_conftest_selects_implicit_fixture_consumers(tmp_path) -> None:
    """Selects only tests in the subtree of an unchanged reachable conftest."""
    _write_module(tmp_path, "agentic_devtools/feature.py", "class Feature: ...\n")
    _write_module(
        tmp_path,
        "tests/unit/feature/conftest.py",
        "from agentic_devtools.feature import Feature\n"
        "import pytest\n"
        "@pytest.fixture\n"
        "def feature(): return Feature()\n",
    )
    _write_module(tmp_path, "tests/unit/feature/test_consumer.py", "def test_uses_fixture(feature): ...\n")
    _write_module(tmp_path, "tests/unit/unrelated/test_other.py", "def test_is_unrelated(): ...\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/feature.py"], cwd=tmp_path) == ["tests/unit/feature"]


def test_reachable_root_conftest_returns_explicit_test_paths(tmp_path) -> None:
    """Expands a reached root conftest to test files, but leaves unrelated changes empty."""
    _write_module(tmp_path, "agentic_devtools/feature.py", "class Feature: ...\n")
    _write_module(tmp_path, "agentic_devtools/unrelated.py", "class Unrelated: ...\n")
    _write_module(
        tmp_path,
        "tests/conftest.py",
        "from agentic_devtools.feature import Feature\n"
        "import pytest\n"
        "@pytest.fixture\n"
        "def feature(): return Feature()\n",
    )
    _write_module(tmp_path, "tests/test_root_consumer.py", "def test_uses_fixture(feature): ...\n")
    _write_module(tmp_path, "tests/unit/other/test_consumer.py", "def test_uses_inherited_fixture(feature): ...\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/feature.py"], cwd=tmp_path) == [
        "tests/test_root_consumer.py",
        "tests/unit/other/test_consumer.py",
    ]
    assert _find_reverse_dependent_test_paths(["agentic_devtools/unrelated.py"], cwd=tmp_path) == []


@pytest.mark.parametrize(
    "import_statement",
    [
        "import agentic_devtools.feature.worker",
        "from agentic_devtools.feature.worker import Worker",
    ],
)
def test_package_initializer_imports_select_transitive_test(tmp_path, import_statement: str) -> None:
    """Includes parent package initializers executed by either dotted import form."""
    _write_module(tmp_path, "agentic_devtools/core.py", "class Core: ...\n")
    _write_module(tmp_path, "agentic_devtools/feature/__init__.py", "from agentic_devtools.core import Core\n")
    _write_module(tmp_path, "agentic_devtools/feature/worker.py", "class Worker: ...\n")
    _write_module(tmp_path, "tests/unit/other/test_worker.py", f"{import_statement}\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/core.py"], cwd=tmp_path) == [
        "tests/unit/other/test_worker.py"
    ]


def test_test_package_initializer_selects_import_free_consumer(tmp_path) -> None:
    """Selects a test whose package initializer imports the changed source."""
    _write_module(tmp_path, "agentic_devtools/core.py", "class Core: ...\n")
    _write_module(tmp_path, "agentic_devtools/unrelated.py", "class Unrelated: ...\n")
    _write_module(tmp_path, "tests/unit/feature/__init__.py", "from agentic_devtools.core import Core\n")
    _write_module(tmp_path, "tests/unit/feature/test_consumer.py", "def test_consumer(): ...\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/core.py"], cwd=tmp_path) == [
        "tests/unit/feature/test_consumer.py"
    ]
    assert _find_reverse_dependent_test_paths(["agentic_devtools/unrelated.py"], cwd=tmp_path) == []


def test_no_reverse_dependent_test_and_unparseable_modules_are_ignored(tmp_path) -> None:
    """Returns no unrelated target when imports are absent or cannot be parsed."""
    _write_module(tmp_path, "agentic_devtools/__init__.py", "")
    _write_module(tmp_path, "agentic_devtools/unused.py", "VALUE = 1\n")
    _write_module(tmp_path, "tests/unit/test_root_import.py", "import agentic_devtools\n")
    _write_module(tmp_path, "tests/unit/test_broken.py", "from (")
    _write_module(tmp_path, "tests/test_invalid_relative.py", "from .. import unavailable\n")

    assert _find_reverse_dependent_test_paths(["agentic_devtools/unused.py"], cwd=tmp_path) == []
    assert _find_reverse_dependent_test_paths(["agentic_devtools/missing.py"], cwd=tmp_path) == []
    assert _find_reverse_dependent_test_paths([], cwd=tmp_path) == []


def test_empty_repository_roots_return_no_targets(tmp_path) -> None:
    """Returns no targets when neither supported Python root exists."""
    assert _find_reverse_dependent_test_paths(["agentic_devtools/app.py"], cwd=tmp_path) == []
