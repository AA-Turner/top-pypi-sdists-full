"""Tests for the GitHub hierarchy lookup adapter."""

import base64
import json
from typing import Any
from unittest.mock import patch

import pytest

from agentic_devtools.cli.speckit.resolve_hierarchy import GitHubHierarchyLookup


def _lookup() -> GitHubHierarchyLookup:
    return GitHubHierarchyLookup("owner/repo", "main", "token")


class TestGitHubHierarchyLookup:
    def test_validates_repository_and_ref(self) -> None:
        for repo, ref in [
            ("owner", "main"),
            ("owner/repo/extra", "main"),
            ("owner/../repo", "main"),
            ("owner/repo", " "),
            ("owner/repo?x=y", "main"),
            ("owner%2Frepo/repo", "main"),
            ("owner/repo#frag", "main"),
            ("owner/repo/", "main"),
        ]:
            with pytest.raises(ValueError):
                GitHubHierarchyLookup(repo, ref, "")

    def test_json_api_decodes_objects_and_rejects_invalid_responses(self) -> None:
        lookup = _lookup()
        with patch(
            "agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call",
            return_value='{"value": 1}',
        ) as api_call:
            assert lookup._json_api("/endpoint") == {"value": 1}
        assert api_call.call_args.kwargs["token"] == "token"

        for response in ("not-json", "[]"):
            with patch("agentic_devtools.cli.speckit.resolve_hierarchy._gh_api_call", return_value=response):
                with pytest.raises((json.JSONDecodeError, RuntimeError)):
                    lookup._json_api("/endpoint")

    def test_fetches_issue(self) -> None:
        lookup = _lookup()
        with patch.object(lookup, "_json_api", return_value={"number": 42}) as api_call:
            assert lookup.fetch_issue(42) == {"number": 42}
            api_call.assert_called_once_with("/repos/owner/repo/issues/42")

    def test_fetches_parent_or_rejects_invalid_graphql_shapes(self) -> None:
        lookup = _lookup()
        response: dict[str, Any] = {
            "data": {"repository": {"issue": {"parent": {"number": 10, "repository": {"nameWithOwner": "o/r"}}}}}
        }
        with patch.object(lookup, "_json_api", return_value=response):
            assert lookup.fetch_parent(42) == {"number": 10, "repository": {"nameWithOwner": "o/r"}}
        with patch.object(lookup, "_json_api", return_value={"data": {"repository": {"issue": {"parent": None}}}}):
            assert lookup.fetch_parent(42) is None
        for response in (
            {},
            {"data": {"repository": {"issue": {"parent": "invalid"}}}},
            # Missing/invalid parent number.
            {"data": {"repository": {"issue": {"parent": {"repository": {"nameWithOwner": "o/r"}}}}}},
            {"data": {"repository": {"issue": {"parent": {"number": 0, "repository": {"nameWithOwner": "o/r"}}}}}},
            # Missing/invalid parent repository name.
            {"data": {"repository": {"issue": {"parent": {"number": 10}}}}},
            {"data": {"repository": {"issue": {"parent": {"number": 10, "repository": {"nameWithOwner": ""}}}}}},
            # Non-empty GraphQL errors accompanying a partial response must be rejected.
            {
                "errors": [{"message": "Something went wrong"}],
                "data": {"repository": {"issue": {"parent": None}}},
            },
        ):
            with patch.object(lookup, "_json_api", return_value=response):
                with pytest.raises(RuntimeError):
                    lookup.fetch_parent(42)

    def test_fetch_tree_handles_missing_specs_and_returns_blob_paths(self) -> None:
        lookup = _lookup()
        missing_specs = [
            {"object": {"sha": "ref"}},
            {"tree": {"sha": "commit"}},
            {"tree": []},
        ]
        with patch.object(lookup, "_json_api", side_effect=missing_specs):
            assert lookup.fetch_tree() == ([], False)

        tree_response = [
            {"object": {"sha": "ref"}},
            {"tree": {"sha": "commit"}},
            {"tree": [{"path": "specs", "type": "tree", "sha": "specs-tree"}]},
            {
                "tree": [
                    {"path": "42-demo/spec.md", "type": "blob"},
                    {"path": "42-demo/hierarchy.yml", "type": "blob"},
                    {"path": "folder", "type": "tree"},
                    {"path": 12, "type": "blob"},
                ],
                "truncated": True,
            },
        ]
        with patch.object(lookup, "_json_api", side_effect=tree_response):
            assert lookup.fetch_tree() == (
                ["specs/42-demo/spec.md", "specs/42-demo/hierarchy.yml"],
                True,
            )

    def test_fetch_tree_rejects_incomplete_specs_tree_response(self) -> None:
        lookup = _lookup()
        responses = [
            {"object": {"sha": "ref"}},
            {"tree": {"sha": "commit"}},
            {"tree": [{"path": "specs", "type": "tree", "sha": "specs-tree"}]},
            {"tree": None},
        ]
        with patch.object(lookup, "_json_api", side_effect=responses):
            with pytest.raises(RuntimeError, match="tree"):
                lookup.fetch_tree()
        invalid_responses: tuple[tuple[object, ...], ...] = (
            ({},),
            ({"object": {"sha": "ref"}}, {"tree": {}}),
        )
        for response_sequence in invalid_responses:
            with patch.object(lookup, "_json_api", side_effect=response_sequence):
                with pytest.raises(RuntimeError, match="incomplete"):
                    lookup.fetch_tree()

    def test_fetches_and_decodes_only_a_unique_hierarchy_file(self) -> None:
        lookup = _lookup()
        assert lookup.fetch_hierarchy(["specs/1/hierarchy.yml"], 42) == ([], None)
        duplicate_paths = ["specs/42-a/hierarchy.yml", "specs/42-b/hierarchy.yml"]
        assert lookup.fetch_hierarchy(duplicate_paths, 42) == (duplicate_paths, None)

        encoded = base64.b64encode(b"level: task\n").decode()
        with patch.object(lookup, "_json_api", return_value={"encoding": "base64", "content": encoded}):
            assert lookup.fetch_hierarchy(["specs/42-demo/hierarchy.yml"], 42) == (
                ["specs/42-demo/hierarchy.yml"],
                "level: task\n",
            )
        with patch.object(lookup, "_json_api", return_value={"encoding": "utf-8", "content": "level: task"}):
            with pytest.raises(RuntimeError, match="base64"):
                lookup.fetch_hierarchy(["specs/42-demo/hierarchy.yml"], 42)
        invalid_utf8 = base64.b64encode(b"\xff").decode()
        with patch.object(lookup, "_json_api", return_value={"encoding": "base64", "content": invalid_utf8}):
            with pytest.raises(RuntimeError, match="decoded"):
                lookup.fetch_hierarchy(["specs/42-demo/hierarchy.yml"], 42)

    def test_search_paths_collects_pages_and_fails_closed_on_bad_results(self) -> None:
        lookup = _lookup()
        with patch.object(
            lookup,
            "_json_api",
            side_effect=[
                {"default_branch": "main"},
                {"items": [{"path": "specs/42/spec.md"}]},
            ],
        ):
            assert lookup.search_paths("spec.md") == ["specs/42/spec.md"]
        with patch.object(
            lookup,
            "_json_api",
            side_effect=[
                {"default_branch": "main"},
                {"items": [{"path": "specs/first/spec.md"}] * 100},
                {"items": []},
            ],
        ):
            assert len(lookup.search_paths("spec.md")) == 100
        for response, message in [
            ({"items": [], "incomplete_results": True}, "incomplete"),
            ({"items": None}, "items list"),
        ]:
            with patch.object(lookup, "_json_api", side_effect=[{"default_branch": "main"}, response]):
                with pytest.raises(RuntimeError, match=message):
                    lookup.search_paths("spec.md")
        with patch.object(
            lookup,
            "_json_api",
            side_effect=[{"default_branch": "main"}, *[{"items": [{}] * 100} for _ in range(10)]],
        ):
            with pytest.raises(RuntimeError, match="1000-result"):
                lookup.search_paths("spec.md")

    def test_search_paths_fails_closed_when_requested_ref_is_not_default_branch(self) -> None:
        lookup = GitHubHierarchyLookup("owner/repo", "feature-branch", "token")
        with patch.object(lookup, "_json_api", return_value={"default_branch": "main"}) as api_call:
            with pytest.raises(RuntimeError, match="default branch"):
                lookup.search_paths("spec.md")
        api_call.assert_called_once_with("/repos/owner/repo")
