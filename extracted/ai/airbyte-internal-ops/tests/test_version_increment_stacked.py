# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

"""Tests for stacked PR version baselines and their retrieval fallbacks."""

import subprocess
from contextlib import ExitStack
from unittest.mock import MagicMock, patch

import pytest
import requests

from airbyte_ops_mcp.connector_qa.checks.version import CheckVersionIncrement
from airbyte_ops_mcp.connector_qa.models import CheckStatus

_MODULE = "airbyte_ops_mcp.connector_qa.checks.version"


@pytest.fixture
def connector(tmp_path):
    return MagicMock(
        code_directory=str(tmp_path),
        technical_name="source-test",
        metadata={"dockerImageTag": "5.2.1"},
    )


@pytest.mark.parametrize(
    "baseline,current,status,message",
    [
        ("5.2.0", "5.2.1", CheckStatus.PASSED, "properly incremented"),
        ("5.2.0", "5.2.2", CheckStatus.FAILED, "skips a version"),
        ("5.2.0", "5.1.3", CheckStatus.FAILED, "lower than"),
        ("5.2.0", "5.2.0", CheckStatus.FAILED, "not incremented"),
        ("5.2.1-rc.1", "5.3.0-rc.1", CheckStatus.FAILED, "different major"),
        ("5.2.1-rc.1", "5.2.2", CheckStatus.FAILED, "next stable version"),
    ],
)
def test_stacked_comparisons(
    connector, monkeypatch, baseline, current, status, message
):
    monkeypatch.setenv("GITHUB_BASE_REF", "feature/parent")
    connector.metadata["dockerImageTag"] = current
    with ExitStack() as stack:
        stack.enter_context(patch(f"{_MODULE}.get_merge_base", return_value=None))
        stack.enter_context(
            patch(
                f"{_MODULE}.subprocess.run",
                return_value=MagicMock(stdout=f"data:\n  dockerImageTag: {baseline}\n"),
            )
        )
        get = stack.enter_context(patch(f"{_MODULE}.requests.get"))
        result = CheckVersionIncrement()._run(connector)
    assert result.status == status
    assert message in result.message
    if status == CheckStatus.FAILED:
        assert "Base branch feature/parent" in result.message
        assert "Master" not in result.message
    get.assert_not_called()


def test_stacked_registry_override_change(connector, monkeypatch):
    monkeypatch.setenv("GITHUB_BASE_REF", "parent")
    connector.metadata = {
        "dockerImageTag": "5.2.0",
        "registryOverrides": {"cloud": {"dockerImageTag": "5.1.2"}},
    }
    with ExitStack() as stack:
        stack.enter_context(patch(f"{_MODULE}.get_merge_base", return_value=None))
        stack.enter_context(
            patch(
                f"{_MODULE}.subprocess.run",
                return_value=MagicMock(stdout="data:\n  dockerImageTag: 5.2.0\n"),
            )
        )
        result = CheckVersionIncrement()._run(connector)
    assert result.status == CheckStatus.SKIPPED
    assert "registryOverrides" in result.message


@pytest.mark.parametrize("base_ref", [None, "", "master", "main"])
def test_unstacked_uses_master(connector, monkeypatch, base_ref):
    if base_ref is None:
        monkeypatch.delenv("GITHUB_BASE_REF", raising=False)
    else:
        monkeypatch.setenv("GITHUB_BASE_REF", base_ref)
    with ExitStack() as stack:
        stack.enter_context(
            patch.object(CheckVersionIncrement, "_get_merge_base", return_value=None)
        )
        master = stack.enter_context(
            patch.object(
                CheckVersionIncrement,
                "_get_master_metadata",
                return_value={"dockerImageTag": "5.1.2"},
            )
        )
        git = stack.enter_context(patch(f"{_MODULE}.subprocess.run"))
        result = CheckVersionIncrement()._run(connector)
    assert result.status == CheckStatus.FAILED
    assert "Master version is 5.1.2" in result.message
    master.assert_called_once_with(connector)
    git.assert_not_called()


@pytest.mark.parametrize("source", ["upstream", "origin", "http", "master"])
def test_baseline_fallback_order(connector, monkeypatch, source):
    monkeypatch.setenv("GITHUB_BASE_REF", "feature/parent")
    metadata = {"dockerImageTag": "5.2.0"}
    failure = subprocess.CalledProcessError(128, "git")
    found = MagicMock(stdout="data:\n  dockerImageTag: 5.2.0\n")
    effects = {
        "upstream": [found],
        "origin": [failure, found],
        "http": [failure, failure],
        "master": [failure, failure],
    }
    with ExitStack() as stack:
        git = stack.enter_context(
            patch(f"{_MODULE}.subprocess.run", side_effect=effects[source])
        )
        get = stack.enter_context(
            patch(
                f"{_MODULE}.requests.get",
                return_value=MagicMock(
                    ok=source == "http", text="data:\n  dockerImageTag: 5.2.0\n"
                ),
            )
        )
        master = stack.enter_context(
            patch.object(
                CheckVersionIncrement, "_get_master_metadata", return_value=None
            )
        )
        result = CheckVersionIncrement()._get_baseline_metadata(connector)
    assert result == (
        (None, "master") if source == "master" else (metadata, "feature/parent")
    )
    assert "upstream/feature/parent:./metadata.yaml" in git.call_args_list[0].args[0]
    if source != "upstream":
        assert "origin/feature/parent:./metadata.yaml" in git.call_args_list[1].args[0]
    assert get.call_count == int(source in {"http", "master"})
    assert master.call_count == int(source == "master")
    if get.called:
        assert "/feature/parent/" in get.call_args.args[0]


@pytest.mark.parametrize("content", ["", "data: null", "not: [valid"])
def test_invalid_base_metadata_falls_back(connector, monkeypatch, content):
    monkeypatch.setenv("GITHUB_BASE_REF", "parent")
    with ExitStack() as stack:
        stack.enter_context(
            patch(f"{_MODULE}.subprocess.run", return_value=MagicMock(stdout=content))
        )
        stack.enter_context(
            patch(
                f"{_MODULE}.requests.get", return_value=MagicMock(ok=True, text=content)
            )
        )
        stack.enter_context(
            patch.object(
                CheckVersionIncrement,
                "_get_master_metadata",
                return_value={"dockerImageTag": "5.1.2"},
            )
        )
        assert CheckVersionIncrement()._get_baseline_metadata(connector) == (
            {"dockerImageTag": "5.1.2"},
            "master",
        )


def test_network_failure_falls_back(connector, monkeypatch):
    monkeypatch.setenv("GITHUB_BASE_REF", "parent")
    with ExitStack() as stack:
        stack.enter_context(patch(f"{_MODULE}.subprocess.run", side_effect=OSError))
        stack.enter_context(
            patch(f"{_MODULE}.requests.get", side_effect=requests.ConnectionError)
        )
        stack.enter_context(
            patch.object(
                CheckVersionIncrement, "_get_master_metadata", return_value=None
            )
        )
        assert CheckVersionIncrement()._get_baseline_metadata(connector) == (
            None,
            "master",
        )
