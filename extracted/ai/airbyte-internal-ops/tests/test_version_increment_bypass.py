# Copyright (c) 2025 Airbyte, Inc., all rights reserved.

"""Tests for skipping CheckVersionIncrement when only unreleased files changed."""

import subprocess
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from airbyte_ops_mcp.airbyte_repo.list_connectors import (
    get_changed_files,
    get_file_at_merge_base,
)
from airbyte_ops_mcp.connector_qa.checks.version import (
    CheckVersionIncrement,
    _is_production_path,
)
from airbyte_ops_mcp.connector_qa.models import CheckStatus

_VERSION_MODULE = "airbyte_ops_mcp.connector_qa.checks.version.CheckVersionIncrement"
_CONNECTOR_DIR = "airbyte-integrations/connectors/source-mock"


@pytest.fixture
def mock_connector(tmp_path):
    return MagicMock(
        code_directory=str(tmp_path),
        technical_name="source-mock",
        metadata={"dockerImageTag": "1.0.0"},
    )


@pytest.mark.parametrize(
    "path, expected",
    [
        pytest.param("unit_tests/test_streams.py", False, id="unit-tests"),
        pytest.param("unit_tests/__init__.py", False, id="unit-tests-init"),
        pytest.param("integration_tests/config.json", False, id="integration-tests"),
        pytest.param("acceptance-test-config.yml", False, id="acceptance-config"),
        pytest.param("README.md", False, id="readme"),
        pytest.param("AGENTS.md", False, id="agents-md"),
        pytest.param("CLAUDE.md", False, id="claude-md"),
        pytest.param("CONTRIBUTING.md", False, id="contributing"),
        pytest.param("erd/source.dbml", False, id="erd"),
        pytest.param("src/test/java/Foo.java", False, id="java-tests"),
        pytest.param("src/test-integration/java/Foo.java", False, id="java-it"),
        pytest.param("metadata.yaml", True, id="metadata"),
        pytest.param("manifest.yaml", True, id="manifest"),
        pytest.param("source_mock/source.py", True, id="source-code"),
        pytest.param("pyproject.toml", True, id="pyproject"),
        pytest.param(".dockerignore", True, id="dockerignore"),
        pytest.param("build.gradle", True, id="gradle"),
        pytest.param("src/main/java/Foo.java", True, id="java-main"),
        pytest.param("unit_tests_helper.py", True, id="prefix-is-not-dir"),
        pytest.param("docs/README.md", True, id="nested-readme"),
    ],
)
def test_is_production_path(path, expected):
    assert _is_production_path(path) is expected


@pytest.mark.parametrize(
    "changed_files, expected_in_message",
    [
        pytest.param(
            ["acceptance-test-config.yml", "unit_tests/test_x.py"],
            "unit_tests/test_x.py",
            id="tests-only",
        ),
        pytest.param(
            ["AGENTS.md", "CLAUDE.md", "CONTRIBUTING.md"],
            "AGENTS.md",
            id="connector-docs-only",
        ),
    ],
)
@patch(f"{_VERSION_MODULE}._get_master_metadata")
@patch(f"{_VERSION_MODULE}._get_changed_files")
def test_test_only_change_skips(
    mock_changed, mock_master, mock_connector, changed_files, expected_in_message
):
    """A change limited to tests needs no version increment."""
    mock_changed.return_value = changed_files

    result = CheckVersionIncrement()._run(mock_connector)

    assert result.status == CheckStatus.SKIPPED
    assert "No production code changed" in result.message
    assert expected_in_message in result.message
    mock_master.assert_not_called()


@pytest.mark.parametrize(
    "changed_files",
    [
        pytest.param(["unit_tests/test_x.py", "manifest.yaml"], id="mixed"),
        pytest.param(["metadata.yaml"], id="metadata-only"),
        pytest.param([], id="no-changes-detected"),
        pytest.param(None, id="changes-unknown"),
    ],
)
@patch(f"{_VERSION_MODULE}._get_master_metadata")
@patch(f"{_VERSION_MODULE}._get_changed_files")
def test_other_changes_still_require_increment(
    mock_changed, mock_master, mock_connector, changed_files
):
    """Anything else, including an undetermined diff, keeps the existing check."""
    mock_changed.return_value = changed_files
    mock_master.return_value = {"dockerImageTag": "1.0.0"}

    result = CheckVersionIncrement()._run(mock_connector)

    assert result.status == CheckStatus.FAILED
    assert "was not incremented" in result.message


def _git(cwd: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=cwd, check=True, capture_output=True)


def _changed_files(connector_dir: Path) -> list[str] | None:
    connector = MagicMock(code_directory=connector_dir)
    return CheckVersionIncrement._get_changed_files(
        connector, CheckVersionIncrement._get_merge_base(connector)
    )


@pytest.fixture
def repo(tmp_path, monkeypatch):
    """A repo whose `origin/master` holds one connector, checked out on a branch."""
    monkeypatch.delenv("GITHUB_BASE_REF", raising=False)
    connector_dir = tmp_path / _CONNECTOR_DIR
    (connector_dir / "unit_tests").mkdir(parents=True)
    (connector_dir / "manifest.yaml").write_text("version: 1\n")
    (connector_dir / "unit_tests" / "test_x.py").write_text("")
    (tmp_path / "README.md").write_text("")
    _git(tmp_path, "init", "-q", "-b", "master")
    _git(tmp_path, "add", ".")
    _git(
        tmp_path,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "init",
    )
    _git(tmp_path, "update-ref", "refs/remotes/origin/master", "HEAD")
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    return tmp_path


def test_get_changed_files_from_git(repo):
    """Committed, uncommitted and untracked changes are all reported."""
    connector_dir = repo / _CONNECTOR_DIR
    (connector_dir / "unit_tests" / "test_x.py").write_text("x = 1\n")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "test change",
    )
    (connector_dir / "acceptance-test-config.yml").write_text("")
    (repo / "README.md").write_text("outside the connector\n")

    changed = _changed_files(connector_dir)

    assert changed == ["acceptance-test-config.yml", "unit_tests/test_x.py"]


def test_get_changed_files_keeps_non_ascii_paths_verbatim(repo):
    """Git would quote non-ASCII paths, which then never match the bypass list."""
    connector_dir = repo / _CONNECTOR_DIR
    (connector_dir / "unit_tests" / "test_café.py").write_text("")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "non-ascii test",
    )
    (connector_dir / "unit_tests" / "test_naïve.py").write_text("")

    changed = _changed_files(connector_dir)

    assert changed == ["unit_tests/test_café.py", "unit_tests/test_naïve.py"]
    assert not any(_is_production_path(path) for path in changed)


def test_get_changed_files_reports_both_sides_of_a_move(repo):
    """Moving released code into a test directory is not a test-only change."""
    connector_dir = repo / _CONNECTOR_DIR
    _git(connector_dir, "mv", "manifest.yaml", "unit_tests/manifest.yaml")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "move",
    )

    changed = _changed_files(connector_dir)

    assert changed == ["manifest.yaml", "unit_tests/manifest.yaml"]


def test_get_changed_files_prefers_upstream(repo):
    """On a fork checkout, `upstream` is the base, not the fork's own master."""
    connector_dir = repo / _CONNECTOR_DIR
    # A test change that upstream master already has, but the fork's master lacks.
    (connector_dir / "unit_tests" / "test_x.py").write_text("x = 1\n")
    _git(repo, "add", ".")
    _git(
        repo,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        "upstream change",
    )
    _git(repo, "update-ref", "refs/remotes/upstream/master", "HEAD")
    (connector_dir / "manifest.yaml").write_text("version: 2\n")

    changed = _changed_files(connector_dir)

    assert changed == ["manifest.yaml"]


def test_get_changed_files_without_base_branch(repo, monkeypatch):
    """A base branch that was not fetched means the changes are unknown."""
    monkeypatch.setenv("GITHUB_BASE_REF", "main")

    changed = _changed_files(repo / _CONNECTOR_DIR)

    assert changed is None


def test_get_changed_files_helper_raises_on_unknown_base_ref(repo):
    """The helper never falls back to a plain diff, so callers can fail closed."""
    with pytest.raises(subprocess.CalledProcessError):
        get_changed_files(repo / _CONNECTOR_DIR, "origin/main")


def test_get_changed_files_outside_git(tmp_path):
    assert _changed_files(tmp_path) is None


_BASE_METADATA = """\
data:
  dockerImageTag: 1.0.0
  dockerRepository: airbyte/source-mock
  documentationUrl: https://docs.airbyte.com/integrations/sources/mock
  tags:
    - language:manifest-only
    - cdk:low-code
  ab_internal:
    sl: 100
    ql: 100
  connectorTestSuitesOptions:
    - suite: unitTests
  externalDocumentationUrls:
    - title: API reference
      url: https://example.com/api
      type: api_reference
metadataSpecVersion: "1.0"
"""


def _commit(cwd: Path, message: str) -> None:
    _git(cwd, "add", "-A")
    _git(
        cwd,
        "-c",
        "user.name=test",
        "-c",
        "user.email=test@example.com",
        "commit",
        "-q",
        "-m",
        message,
    )


@pytest.fixture
def metadata_repo(tmp_path, monkeypatch):
    """A connector with a metadata.yaml on `origin/master`, checked out on a branch."""
    monkeypatch.delenv("GITHUB_BASE_REF", raising=False)
    connector_dir = tmp_path / _CONNECTOR_DIR
    (connector_dir / "unit_tests").mkdir(parents=True)
    (connector_dir / "manifest.yaml").write_text("version: 1\n")
    (connector_dir / "metadata.yaml").write_text(_BASE_METADATA)
    (connector_dir / "unit_tests" / "test_x.py").write_text("")
    _git(tmp_path, "init", "-q", "-b", "master")
    _commit(tmp_path, "init")
    _git(tmp_path, "update-ref", "refs/remotes/origin/master", "HEAD")
    _git(tmp_path, "checkout", "-q", "-b", "feature")
    return connector_dir


def _edit_metadata(connector_dir: Path, old: str, new: str) -> None:
    path = connector_dir / "metadata.yaml"
    text = path.read_text()
    assert old in text
    path.write_text(text.replace(old, new))


def _run_check(connector_dir: Path):
    connector = MagicMock(
        code_directory=connector_dir,
        technical_name="source-mock",
        metadata={"dockerImageTag": "1.0.0"},
    )
    with patch(
        f"{_VERSION_MODULE}._get_master_metadata",
        return_value={"dockerImageTag": "1.0.0"},
    ) as mock_master:
        return CheckVersionIncrement()._run(connector), mock_master


_NEW_DOC_URL = """\
    - title: API reference
      url: https://example.com/api
      type: api_reference
    - title: Changelog
      url: https://example.com/changelog
      type: api_release_history
"""
_OLD_DOC_URL = """\
    - title: API reference
      url: https://example.com/api
      type: api_reference
"""


@pytest.mark.parametrize(
    "edits, expected_fields",
    [
        pytest.param(
            [(_OLD_DOC_URL, _NEW_DOC_URL)], "externalDocumentationUrls", id="docs-urls"
        ),
        pytest.param(
            [
                (
                    "    - suite: unitTests\n",
                    "    - suite: unitTests\n    - suite: liveTests\n",
                )
            ],
            "connectorTestSuitesOptions",
            id="test-suites",
        ),
        pytest.param(
            [("    - cdk:low-code\n", "    - cdk:low-code\n    - keyword:crm\n")],
            "tags",
            id="keyword-tag",
        ),
        pytest.param(
            [("    - cdk:low-code\n", "    - keyword:crm\n    - cdk:low-code\n")],
            "tags",
            id="keyword-tag-between-released-tags",
        ),
        pytest.param(
            [
                (_OLD_DOC_URL, _NEW_DOC_URL),
                ("    - suite: unitTests\n", "    - suite: integrationTests\n"),
            ],
            "externalDocumentationUrls, connectorTestSuitesOptions",
            id="several-fields",
        ),
    ],
)
def test_unreleased_metadata_change_skips(metadata_repo, edits, expected_fields):
    """A metadata.yaml change limited to unreleased fields needs no increment."""
    for old, new in edits:
        _edit_metadata(metadata_repo, old, new)

    result, mock_master = _run_check(metadata_repo)

    assert result.status == CheckStatus.SKIPPED
    assert f"metadata.yaml changes only {expected_fields}," in result.message
    mock_master.assert_not_called()


def test_unreleased_metadata_and_test_change_skips(metadata_repo):
    """Tests and unreleased metadata fields together still need no increment."""
    _edit_metadata(metadata_repo, _OLD_DOC_URL, _NEW_DOC_URL)
    (metadata_repo / "unit_tests" / "test_x.py").write_text("x = 1\n")
    _commit(metadata_repo, "docs urls and tests")

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.SKIPPED
    assert "metadata.yaml, unit_tests/test_x.py" in result.message


def test_metadata_comment_only_change_skips(metadata_repo):
    _edit_metadata(metadata_repo, "data:\n", "# A comment.\ndata:\n")

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.SKIPPED
    assert "metadata.yaml changes no field" in result.message


def test_metadata_compared_with_merge_base_not_master_tip(metadata_repo):
    """A release on master after the branch point is not this branch's change."""
    _edit_metadata(metadata_repo, _OLD_DOC_URL, _NEW_DOC_URL)
    _commit(metadata_repo, "docs urls")
    repo_root = metadata_repo.parents[2]
    _git(repo_root, "checkout", "-q", "master")
    _edit_metadata(metadata_repo, "dockerImageTag: 1.0.0", "dockerImageTag: 1.0.1")
    _commit(repo_root, "release")
    _git(repo_root, "update-ref", "refs/remotes/origin/master", "HEAD")
    _git(repo_root, "checkout", "-q", "feature")

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.SKIPPED


def test_metadata_compared_with_the_same_base_as_the_file_list(metadata_repo):
    """On a fork checkout, metadata.yaml is compared with `upstream` too."""
    repo_root = metadata_repo.parents[2]
    _git(repo_root, "checkout", "-q", "master")
    # A released change that upstream master has, but the fork's master lacks.
    _edit_metadata(
        metadata_repo, "integrations/sources/mock\n", "integrations/sources/mock-v2\n"
    )
    _commit(repo_root, "upstream release")
    _git(repo_root, "update-ref", "refs/remotes/upstream/master", "HEAD")
    _git(repo_root, "checkout", "-q", "-B", "feature")
    _edit_metadata(metadata_repo, _OLD_DOC_URL, _NEW_DOC_URL)

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.SKIPPED
    assert "metadata.yaml changes only externalDocumentationUrls," in result.message


@pytest.mark.parametrize(
    "old, new",
    [
        pytest.param(
            "    - language:manifest-only\n",
            "    - language:python\n",
            id="language-tag",
        ),
        pytest.param("    - cdk:low-code\n", "    - cdk:python\n", id="cdk-tag"),
        pytest.param("    sl: 100\n", "    sl: 300\n", id="ab-internal"),
        pytest.param(
            "integrations/sources/mock\n",
            "integrations/sources/mock-v2\n",
            id="documentation-url",
        ),
        pytest.param(
            'metadataSpecVersion: "1.0"\n',
            'metadataSpecVersion: "1.1"\n',
            id="outside-data",
        ),
        pytest.param(
            "  tags:\n",
            "  resourceRequirements:\n    jobSpecific: []\n  tags:\n",
            id="new-released-field",
        ),
        pytest.param(
            "    - language:manifest-only\n    - cdk:low-code\n",
            "    - cdk:low-code\n    - language:manifest-only\n",
            id="released-tags-reordered",
        ),
        pytest.param(
            "  tags:\n",
            "  releasedTags: []\n  tags:\n",
            id="field-named-released-tags",
        ),
    ],
)
def test_released_metadata_change_still_requires_increment(metadata_repo, old, new):
    """A released field, even next to unreleased ones, keeps the check."""
    _edit_metadata(metadata_repo, _OLD_DOC_URL, _NEW_DOC_URL)
    _edit_metadata(metadata_repo, old, new)

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.FAILED
    assert "was not incremented" in result.message


def test_unreleased_metadata_and_code_change_still_requires_increment(metadata_repo):
    _edit_metadata(metadata_repo, _OLD_DOC_URL, _NEW_DOC_URL)
    (metadata_repo / "manifest.yaml").write_text("version: 2\n")

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.FAILED
    assert "was not incremented" in result.message


def test_new_metadata_file_still_requires_increment(metadata_repo):
    """A metadata.yaml missing from the base branch is a new connector."""
    repo_root = metadata_repo.parents[2]
    _git(repo_root, "checkout", "-q", "master")
    _git(metadata_repo, "rm", "-q", "metadata.yaml")
    _commit(repo_root, "no metadata")
    _git(repo_root, "update-ref", "refs/remotes/origin/master", "HEAD")
    _git(repo_root, "checkout", "-q", "-B", "feature")
    (metadata_repo / "metadata.yaml").write_text(_BASE_METADATA)

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.FAILED


def test_deleted_metadata_file_still_requires_increment(metadata_repo):
    (metadata_repo / "metadata.yaml").unlink()

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.FAILED


@pytest.mark.parametrize(
    "content",
    [
        pytest.param("data: [unclosed\n", id="invalid-yaml"),
        pytest.param("- not a mapping\n", id="not-a-mapping"),
        pytest.param("metadataSpecVersion: '1.0'\n", id="no-data"),
    ],
)
def test_unparseable_metadata_still_requires_increment(metadata_repo, content):
    (metadata_repo / "metadata.yaml").write_text(content)

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.FAILED


def test_unknown_base_branch_still_requires_increment(metadata_repo, monkeypatch):
    _edit_metadata(metadata_repo, _OLD_DOC_URL, _NEW_DOC_URL)
    monkeypatch.setenv("GITHUB_BASE_REF", "main")

    result, _ = _run_check(metadata_repo)

    assert result.status == CheckStatus.FAILED


def test_get_file_at_merge_base(metadata_repo):
    (metadata_repo / "manifest.yaml").write_text("version: 2\n")
    _commit(metadata_repo, "change")

    assert get_file_at_merge_base(metadata_repo, "manifest.yaml", "origin/master") == (
        "version: 1\n"
    )
    assert (
        get_file_at_merge_base(metadata_repo, "missing.yaml", "origin/master") is None
    )
    with pytest.raises(subprocess.CalledProcessError):
        get_file_at_merge_base(metadata_repo, "manifest.yaml", "origin/main")
