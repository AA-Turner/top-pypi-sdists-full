"""Packaging metadata regression tests for agentic-devtools."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from packaging.requirements import Requirement
from packaging.specifiers import SpecifierSet
from packaging.version import Version

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib  # type: ignore[no-redef]


def _load_project_metadata() -> dict[str, Any]:
    pyproject_path = Path(__file__).resolve().parent.parent / "pyproject.toml"
    return tomllib.loads(pyproject_path.read_text(encoding="utf-8"))


def test_python_314_is_the_minimum_supported_runtime() -> None:
    """Package metadata requires Python 3.14 and does not depend on tomli."""
    metadata = _load_project_metadata()
    project = metadata["project"]
    dependencies = [Requirement(dep) for dep in project["dependencies"]]

    classifiers = project["classifiers"]
    assert project["requires-python"] == ">=3.14"
    assert "Programming Language :: Python :: 3" in classifiers
    assert "Programming Language :: Python :: 3 :: Only" in classifiers
    assert "Programming Language :: Python :: 3.14" in classifiers
    assert not any(
        classifier.startswith("Programming Language :: Python :: 3.")
        and classifier != "Programming Language :: Python :: 3.14"
        for classifier in classifiers
    )
    assert all(requirement.name != "tomli" for requirement in dependencies)

    dev_dependencies = {
        requirement.name: requirement
        for requirement in (Requirement(dep) for dep in project["optional-dependencies"]["dev"])
    }
    assert dev_dependencies["ruff"].specifier == SpecifierSet(">=0.14.0")
    assert dev_dependencies["mypy"].specifier == SpecifierSet(">=1.19.0")

    tools = metadata["tool"]
    assert tools["ruff"]["target-version"] == "py314"
    assert tools["mypy"]["python_version"] == "3.14"


def test_langgraph_dependency_is_bounded_to_the_current_major() -> None:
    """langgraph is capped to the currently tested major version."""
    metadata = _load_project_metadata()
    dependencies = metadata["project"]["dependencies"]

    reqs = [Requirement(dep) for dep in dependencies]
    langgraph_req = next((r for r in reqs if r.name == "langgraph"), None)

    assert langgraph_req is not None, "langgraph must be a declared dependency"
    assert {(specifier.operator, specifier.version) for specifier in langgraph_req.specifier} == {
        (">=", "0.2.0"),
        ("<", "2"),
    }, "langgraph must stay pinned to the tested major range (>=0.2.0,<2)"


def test_langchain_extra_is_removed() -> None:
    """The langchain extra no longer exists because the base install already covers it."""
    metadata = _load_project_metadata()
    optional_dependencies = metadata["project"]["optional-dependencies"]

    assert "langchain" not in optional_dependencies


def test_langchain_core_is_declared_as_direct_dependency() -> None:
    """langchain-core is declared directly so imports are not relying on a transitive dependency."""
    metadata = _load_project_metadata()
    dependencies = metadata["project"]["dependencies"]

    langchain_core_dep = next((dep for dep in dependencies if dep.startswith("langchain-core")), None)

    assert langchain_core_dep is not None, "langchain-core must be a direct dependency"
    specifier = SpecifierSet(langchain_core_dep.removeprefix("langchain-core"))
    # Representative `langgraph<2` base-stack resolution that must remain installable.
    assert Version("1.5.4") in specifier, "langchain-core range must allow the LangGraph<2 base stack"
