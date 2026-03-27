"""Unit tests for spec_linkage — branch/PR association for spec artifacts (#1018)."""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch

import pytest

from anteroom.services.spec_linkage import (
    GitLink,
    add_git_link,
    detect_current_branch,
    get_spec_links,
    link_branch_to_spec,
    link_pr_to_spec,
    parse_git_links,
    remove_git_link,
    unlink_from_spec,
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def db(tmp_path: Path) -> Any:
    """Create a real DB via init_db for spec linkage tests."""
    from anteroom.db import init_db

    return init_db(tmp_path / "test.db")


VALID_SPEC_YAML = """\
requirements: |
  Must support widgets.
design: |
  Use the widget parser pattern.
tasks:
  - id: t1
    summary: Implement widget parser
"""


def _create_spec_artifact(db: Any) -> dict[str, Any]:
    """Helper to create a spec artifact for testing."""
    from anteroom.services.spec_service import create_spec

    return create_spec(db, "ns", "feat", VALID_SPEC_YAML)


# ---------------------------------------------------------------------------
# detect_current_branch
# ---------------------------------------------------------------------------


class TestDetectCurrentBranch:
    def test_detect_branch_in_git_repo(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "issue-42-add-api\n"
        with patch("anteroom.services.spec_linkage.subprocess.run", return_value=mock_result):
            assert detect_current_branch() == "issue-42-add-api"

    def test_detect_branch_not_git_repo(self) -> None:
        with patch("anteroom.services.spec_linkage.subprocess.run", side_effect=FileNotFoundError):
            assert detect_current_branch() is None

    def test_detect_branch_detached_head(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 0
        mock_result.stdout = "HEAD\n"
        with patch("anteroom.services.spec_linkage.subprocess.run", return_value=mock_result):
            assert detect_current_branch() is None

    def test_detect_branch_timeout(self) -> None:
        with patch(
            "anteroom.services.spec_linkage.subprocess.run",
            side_effect=subprocess.TimeoutExpired(cmd="git", timeout=5),
        ):
            assert detect_current_branch() is None

    def test_detect_branch_nonzero_exit(self) -> None:
        mock_result = MagicMock()
        mock_result.returncode = 128
        mock_result.stdout = ""
        with patch("anteroom.services.spec_linkage.subprocess.run", return_value=mock_result):
            assert detect_current_branch() is None


# ---------------------------------------------------------------------------
# parse_git_links
# ---------------------------------------------------------------------------


class TestParseGitLinks:
    def test_parse_git_links_empty(self) -> None:
        assert parse_git_links({}) == []

    def test_parse_git_links_valid(self) -> None:
        metadata = {
            "git_links": [
                {
                    "id": "abc",
                    "type": "branch",
                    "ref": "main",
                    "url": None,
                    "linked_at": "2025-01-01T00:00:00",
                    "linked_by": "user1",
                    "auto": True,
                },
                {
                    "id": "def",
                    "type": "pr",
                    "ref": "42",
                    "url": "https://github.com/org/repo/pull/42",
                    "linked_at": "2025-01-02T00:00:00",
                    "linked_by": None,
                    "auto": False,
                },
            ]
        }
        links = parse_git_links(metadata)
        assert len(links) == 2
        assert links[0].type == "branch"
        assert links[0].ref == "main"
        assert links[0].auto is True
        assert links[1].type == "pr"
        assert links[1].ref == "42"
        assert links[1].url == "https://github.com/org/repo/pull/42"

    def test_parse_git_links_malformed(self) -> None:
        assert parse_git_links({"git_links": "not-a-list"}) == []
        assert parse_git_links({"git_links": [42, None, "bad"]}) == []
        assert parse_git_links({"git_links": [{"id": "ok", "type": "branch"}]}) == [
            GitLink(id="ok", type="branch", ref="", url=None, linked_at="", linked_by=None, auto=False)
        ]


# ---------------------------------------------------------------------------
# add_git_link / remove_git_link
# ---------------------------------------------------------------------------


class TestAddGitLink:
    def _make_link(self, *, link_type: str = "branch", ref: str = "main", link_id: str = "link-1") -> GitLink:
        return GitLink(
            id=link_id,
            type=link_type,
            ref=ref,
            url=None,
            linked_at="2025-01-01T00:00:00",
            linked_by=None,
            auto=False,
        )

    def test_add_git_link_new(self) -> None:
        link = self._make_link()
        result = add_git_link({}, link)
        assert len(result["git_links"]) == 1
        assert result["git_links"][0]["ref"] == "main"

    def test_add_git_link_deduplication(self) -> None:
        link = self._make_link()
        meta = add_git_link({}, link)
        link2 = self._make_link(link_id="link-2")
        result = add_git_link(meta, link2)
        assert len(result["git_links"]) == 1  # Not added again

    def test_add_git_link_different_type_same_ref(self) -> None:
        branch_link = self._make_link(link_type="branch", ref="42")
        pr_link = self._make_link(link_type="pr", ref="42", link_id="link-2")
        meta = add_git_link({}, branch_link)
        result = add_git_link(meta, pr_link)
        assert len(result["git_links"]) == 2

    def test_add_git_link_immutability(self) -> None:
        original: dict[str, Any] = {"existing_key": "value"}
        link = self._make_link()
        result = add_git_link(original, link)
        assert "git_links" not in original
        assert "git_links" in result


class TestRemoveGitLink:
    def test_remove_git_link(self) -> None:
        meta: dict[str, Any] = {"git_links": [{"id": "abc", "type": "branch", "ref": "main"}]}
        result = remove_git_link(meta, "abc")
        assert result["git_links"] == []

    def test_remove_git_link_nonexistent(self) -> None:
        meta: dict[str, Any] = {"git_links": [{"id": "abc", "type": "branch", "ref": "main"}]}
        result = remove_git_link(meta, "does-not-exist")
        assert len(result["git_links"]) == 1

    def test_remove_git_link_immutability(self) -> None:
        original: dict[str, Any] = {"git_links": [{"id": "abc", "type": "branch", "ref": "main"}]}
        remove_git_link(original, "abc")
        assert len(original["git_links"]) == 1  # Original unchanged


# ---------------------------------------------------------------------------
# DB-backed operations (real DB via init_db)
# ---------------------------------------------------------------------------


class TestLinkBranchToSpec:
    def test_link_branch_to_spec(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        result = link_branch_to_spec(db, art["fqn"], "issue-42-widgets")
        assert result is not None
        links = parse_git_links(result["metadata"])
        assert len(links) == 1
        assert links[0].type == "branch"
        assert links[0].ref == "issue-42-widgets"
        assert links[0].auto is False

    def test_link_branch_auto(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        result = link_branch_to_spec(db, art["fqn"], "auto-branch", auto=True)
        assert result is not None
        links = parse_git_links(result["metadata"])
        assert links[0].auto is True

    def test_link_branch_deduplication(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        link_branch_to_spec(db, art["fqn"], "issue-42-widgets")
        result = link_branch_to_spec(db, art["fqn"], "issue-42-widgets")
        assert result is not None
        links = parse_git_links(result["metadata"])
        assert len(links) == 1  # Not duplicated

    def test_link_branch_nonexistent_spec(self, db: Any) -> None:
        result = link_branch_to_spec(db, "@ns/spec/nonexistent", "some-branch")
        assert result is None

    def test_link_branch_non_spec_artifact(self, db: Any) -> None:
        from anteroom.services import artifact_storage

        artifact_storage.create_artifact(db, "@ns/skill/x", "skill", "ns", "x", "content")
        result = link_branch_to_spec(db, "@ns/skill/x", "some-branch")
        assert result is None


class TestLinkPrToSpec:
    def test_link_pr_to_spec(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        result = link_pr_to_spec(db, art["fqn"], "123", pr_url="https://github.com/org/repo/pull/123")
        assert result is not None
        links = parse_git_links(result["metadata"])
        assert len(links) == 1
        assert links[0].type == "pr"
        assert links[0].ref == "123"
        assert links[0].url == "https://github.com/org/repo/pull/123"

    def test_link_pr_nonexistent_spec(self, db: Any) -> None:
        result = link_pr_to_spec(db, "@ns/spec/nonexistent", "99")
        assert result is None


class TestUnlinkFromSpec:
    def test_unlink_from_spec(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        linked = link_branch_to_spec(db, art["fqn"], "issue-42-widgets")
        assert linked is not None
        links = parse_git_links(linked["metadata"])
        link_id = links[0].id

        result = unlink_from_spec(db, art["fqn"], link_id)
        assert result is not None
        remaining = parse_git_links(result["metadata"])
        assert len(remaining) == 0

    def test_unlink_nonexistent_link(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        result = unlink_from_spec(db, art["fqn"], "no-such-link-id")
        assert result is not None  # Succeeds, just no change

    def test_unlink_nonexistent_spec(self, db: Any) -> None:
        result = unlink_from_spec(db, "@ns/spec/nonexistent", "some-id")
        assert result is None


class TestGetSpecLinks:
    def test_get_spec_links_empty(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        links = get_spec_links(db, art["fqn"])
        assert links == []

    def test_get_spec_links_with_data(self, db: Any) -> None:
        art = _create_spec_artifact(db)
        link_branch_to_spec(db, art["fqn"], "branch-a")
        link_pr_to_spec(db, art["fqn"], "55", pr_url="https://example.com/pr/55")
        links = get_spec_links(db, art["fqn"])
        assert len(links) == 2
        types = {lnk.type for lnk in links}
        assert types == {"branch", "pr"}

    def test_get_spec_links_nonexistent(self, db: Any) -> None:
        links = get_spec_links(db, "@ns/spec/nonexistent")
        assert links == []
