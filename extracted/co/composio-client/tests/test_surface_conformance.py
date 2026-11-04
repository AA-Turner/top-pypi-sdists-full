"""The released-surface conformance gate, run against the source tree.

``scripts/check_surface_conformance.py`` is the gate itself. CI points it at
the built wheel after ``uv build``, which is the run that
can see a packaging mistake. This module runs the same comparison against the
importable package, so the loop is short during development, and — more
importantly — pins that the comparison would actually *fail* on a surface that
does not conform. A both-directions check that cannot fail is a check that
asserts nothing.
"""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path
from types import ModuleType
from typing import Any

import pytest


def _load_checker() -> ModuleType:
    path = Path(__file__).resolve().parents[1] / "scripts" / "check_surface_conformance.py"
    spec = importlib.util.spec_from_file_location("_surface_conformance", path)
    assert spec is not None and spec.loader is not None
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


checker = _load_checker()


@pytest.fixture
def surface() -> dict[str, Any]:
    return checker.dump_surface()


def test_the_source_tree_conforms(surface: dict[str, Any]) -> None:
    assert checker.check_surface(surface) == []


def test_every_covered_operation_is_callable(surface: dict[str, Any]) -> None:
    """The forward direction, spelled out: all 116 covered operations resolve."""
    paths = {tuple(path) for path in surface["sync"]}
    assert ("tool_router", "session", "create") in paths
    assert ("tool_router", "session", "config_history") in paths
    assert ("tool_router", "session", "files", "create_download_url") in paths
    # One from each of the depths the widened forest reaches.
    assert ("tools", "execute") in paths
    assert ("_internal", "logs", "tools", "list") in paths
    assert ("org", "owner", "project", "regenerate_api_key") in paths
    assert len(paths) == 116


def test_a_missing_accessor_is_reported(surface: dict[str, Any]) -> None:
    broken = dict(surface)
    broken["sync"] = [path for path in surface["sync"] if path[-1] != "create"]
    problems = checker.check_surface(broken)
    assert any("has no callable at tool_router.session.create" in problem for problem in problems)


def test_an_uncovered_accessor_is_reported(surface: dict[str, Any]) -> None:
    """The reverse direction: a method the record does not list fails the gate.

    Now that coverage *is* the released-surface record, an uncovered accessor is
    necessarily one the record has never held — a hand-added method, or a
    generator that invented a name. That is the accident this direction exists
    for, and it is the only one left that can produce it.
    """
    broken = dict(surface)
    broken["sync"] = [*surface["sync"], ["tool_router", "session", "hand_added"]]
    problems = checker.check_surface(broken)
    assert any(
        "tool_router.session.hand_added is callable but is not a covered operation" in problem
        for problem in problems
    )


def test_a_sync_async_divergence_is_reported(surface: dict[str, Any]) -> None:
    broken = dict(surface)
    broken["async"] = surface["async"][:-1]
    assert any("different accessor trees" in problem for problem in checker.check_surface(broken))


def test_wheel_introspection_refreshes_an_overwritten_artifact(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    command: list[str] = []

    def run(args: list[str], **_: Any) -> subprocess.CompletedProcess[str]:
        command.extend(args)
        return subprocess.CompletedProcess(
            args,
            0,
            stdout='{"module": "wheel", "sync": [], "async": []}',
            stderr="",
        )

    monkeypatch.setattr(checker.subprocess, "run", run)
    checker.surface_from_wheel(tmp_path / "composio_client-2.0.0-py3-none-any.whl")

    refresh = command.index("--refresh-package")
    assert command[refresh : refresh + 2] == ["--refresh-package", "composio-client"]


@pytest.mark.parametrize(
    ("camel", "snake"),
    [
        ("create", "create"),
        ("configHistory", "config_history"),
        ("executeMeta", "execute_meta"),
        ("toolRouter", "tool_router"),
        # The initialism cases: a naive per-capital split gives
        # `create_download_u_r_l` and `regenerate_a_p_i_key`.
        ("createDownloadURL", "create_download_url"),
        ("createUploadURL", "create_upload_url"),
        ("regenerateAPIKey", "regenerate_api_key"),
        ("retrieveToolExecution", "retrieve_tool_execution"),
        ("createPresignedURL", "create_presigned_url"),
        ("listInstances", "list_instances"),
    ],
)
def test_record_names_convert_to_python_names(camel: str, snake: str) -> None:
    assert checker.snake_case(camel) == snake
