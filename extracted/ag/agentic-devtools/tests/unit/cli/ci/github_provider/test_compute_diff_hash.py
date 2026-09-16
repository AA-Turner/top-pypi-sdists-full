"""Tests for GitHubActionsProvider.compute_diff_hash."""

import hashlib
from unittest.mock import patch

import pytest

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider


def _git_stub(responses: dict, *, patch_id_output: str = "", patch_id_exc: Exception | None = None):
    """Build a ``_run_git`` side effect from an args→output mapping.

    ``patch_id_exc``, when given, is raised by the ``git patch-id`` invocation.
    """

    def side_effect(args, *, stdin_text=None):
        key = tuple(args)
        if key == ("patch-id", "--verbatim"):
            assert stdin_text is not None
            if patch_id_exc is not None:
                raise patch_id_exc
            return patch_id_output
        if key in responses:
            result = responses[key]
            if isinstance(result, Exception):
                raise result
            return result
        if len(key) == 3 and key[0] == "merge-base":
            return "mergebase123\n"
        if len(key) == 2 and key[0] == "show" and isinstance(key[1], str) and ":" in key[1]:
            _, _, suffix = key[1].partition(":")
            origin_key = ("show", f"origin/main:{suffix}")
            if origin_key in responses:
                result = responses[origin_key]
                if isinstance(result, Exception):
                    raise result
                return result
        raise RuntimeError(f"unexpected: {args}")

    return side_effect


class TestComputeDiffHash:
    """Tests for compute_diff_hash method."""

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_uses_pinned_base_sha_without_refetching_branch(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n+new line"
        mock_run_git.side_effect = _git_stub(
            {
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "base-sha...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123", base_sha="base-sha")

        assert result is not None
        mock_run_git.assert_any_call(["diff", "-U1", "base-sha...abc123"])
        assert not any(call.args[0] == ["fetch", "origin", "main"] for call in mock_run_git.call_args_list)

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_patch_id_of_diff(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n+new line"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_appends_location_fingerprint_for_ambiguous_repeated_context(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_distinguishes_distant_repeated_context(self, mock_run_git) -> None:
        file_contents = "context\nold\ncontext\n" + "filler\n" * 10 + "context\nold\ncontext\n"
        common_commands = {
            ("fetch", "origin", "main"): "",
            ("cat-file", "-e", "abc123^{commit}"): "",
            ("show", "mergebase123:foo.py"): file_contents,
        }
        provider = GitHubActionsProvider(repo="owner/repo")

        def run_with_hunk(line: int) -> str | None:
            mock_run_git.side_effect = _git_stub(
                {
                    **common_commands,
                    ("diff", "-U1", "origin/main...abc123"): (
                        "diff --git a/foo.py b/foo.py\n"
                        "--- a/foo.py\n"
                        "+++ b/foo.py\n"
                        f"@@ -{line},3 +{line},3 @@\n"
                        " context\n-old\n+new\n context\n"
                    ),
                },
                patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
            )
            return provider.compute_diff_hash(base_branch="main", sha="abc123")

        first = run_with_hunk(2)
        second = run_with_hunk(15)

        assert first is not None
        assert second is not None
        assert first != second

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_reads_merge_base_tree(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        mock_run_git.assert_any_call(["merge-base", "abc123", "origin/main"])
        mock_run_git.assert_any_call(["show", "mergebase123:foo.py"])

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_merge_base_lookup_fails(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("merge-base", "abc123", "origin/main"): RuntimeError("merge-base failed"),
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_keeps_location_fingerprint_stable_when_base_gains_duplicate_elsewhere(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -6,3 +6,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        first_base = "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n"
        second_base = f"{first_base}context\nold\ncontext\nomega\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): first_base,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        first_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): second_base,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        second_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert first_result is not None
        assert second_result is not None
        assert first_result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")
        assert first_result == second_result

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_keeps_duplicate_before_target_stable(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -6,3 +6,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        first_base = "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n"
        second_base = f"context\nold\ncontext\nomega\n{first_base}"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): first_base,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        first_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        second_diff_output = diff_output.replace("@@ -6,3 +6,3 @@", "@@ -10,3 +10,3 @@")
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): second_diff_output,
                ("show", "mergebase123:foo.py"): second_base,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        second_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert first_result == second_result

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_rejects_moved_duplicate_occurrence(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        provider = GitHubActionsProvider(repo="owner/repo")
        before_base = "prefix\ncontext\nold\ncontext\nmiddle\ncontext\nold\ncontext\nsuffix\n"
        after_base = "prefix\nmiddle\ncontext\nold\ncontext\nsuffix\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): before_base,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        before_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        after_diff_output = diff_output.replace("@@ -2,3 +2,3 @@", "@@ -3,3 +3,3 @@")
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): after_diff_output,
                ("show", "mergebase123:foo.py"): after_base,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        after_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert before_result is not None
        assert after_result is not None
        assert before_result != after_result

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_uses_preceding_anchor_when_suffixes_match(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -5,3 +5,3 @@\n shared\n-old\n+new\n shared\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "alpha\nshared\nold\nshared\nbeta\nshared\nold\nshared\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_drops_candidate_with_left_boundary_mismatch(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -3 +3 @@\n-old\n+new\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "old\nx\nold\nx\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_drops_candidate_with_left_context_mismatch(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -5 +5 @@\n-old\n+new\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "A\nold\nx\nB\nold\nx\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_fails_closed_for_ambiguous_right_context(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -3 +3 @@\n-old\n+new\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): "x\nold\nold\nold\nold\ny\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_fingerprint_uses_linear_search_for_repeated_removed_lines(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -1,4 +1,1 @@\n-a\n-b\n-a\n-c\n+new\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): "a\nb\na\nb\na\nc\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result == "patch-id:1045a6f6deadbeef"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_location_fingerprint_exceeds_work_budget(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -501 +501 @@\n-old\n+new\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): "\n".join(["old"] * 1001) + "\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_candidate_search_exceeds_work_budget(self, mock_run_git) -> None:
        removed_lines = "\n".join("-old" for _ in range(113))
        diff_output = (
            f"diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -1,113 +1,1 @@\n{removed_lines}\n+new\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "mergebase123:foo.py"): "\n".join(["old"] * 1001) + "\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_parses_quoted_git_paths_for_location_digest(self, mock_run_git) -> None:
        diff_output = (
            'diff --git "a/caf\\303\\251\\tname.py" "b/caf\\303\\251\\tname.py"\n'
            '--- "a/caf\\303\\251\\tname.py"\n'
            '+++ "b/caf\\303\\251\\tname.py"\n'
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                (
                    "show",
                    "origin/main:café\tname.py",
                ): "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_handles_surrogateescaped_git_paths_in_location_digest(self, mock_run_git) -> None:
        surrogate_path = b"caf\xe9.py".decode("utf-8", errors="surrogateescape")
        diff_output = (
            'diff --git "a/caf\\351.py" "b/caf\\351.py"\n'
            '--- "a/caf\\351.py"\n'
            '+++ "b/caf\\351.py"\n'
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                (
                    "show",
                    f"origin/main:{surrogate_path}",
                ): "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_disambiguates_repeated_multi_change_hunks_with_interleaved_context(self, mock_run_git) -> None:
        diff_output_first = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -1,6 +1,6 @@\n"
            " context\n"
            "-old1\n"
            "+new1\n"
            " middle\n"
            "-old2\n"
            "+new2\n"
            " context\n"
        )
        diff_output_second = diff_output_first.replace("@@ -1,6 +1,6 @@", "@@ -6,6 +6,6 @@")
        base_file = "context\nold1\nmiddle\nold2\ncontext\ncontext\nold1\nmiddle\nold2\ncontext\n"

        provider = GitHubActionsProvider(repo="owner/repo")
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output_first,
                ("show", "origin/main:foo.py"): base_file,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        first_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output_second,
                ("show", "origin/main:foo.py"): base_file,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        second_result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert first_result is not None
        assert second_result is not None
        assert first_result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")
        assert second_result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")
        assert first_result != second_result

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_preserves_trailing_space_in_git_path_headers(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/space  b/space \n"
            "--- a/space \t\n"
            "+++ b/space \t\n"
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:space "): "alpha\ncontext\nold\ncontext\nbeta\ncontext\nold\ncontext\ngamma\n",
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|loc-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_git_path_header_quote_is_unterminated(self, mock_run_git) -> None:
        diff_output = 'diff --git a/foo.py b/foo.py\n--- "a/foo.py\n+++ b/foo.py\n@@ -1 +1 @@\n-old\n+new\n'
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_git_path_header_has_dangling_escape(self, mock_run_git) -> None:
        diff_output = 'diff --git a/foo.py b/foo.py\n--- "a/foo\\"\n+++ b/foo.py\n@@ -1 +1 @@\n-old\n+new\n'
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_git_path_header_has_unknown_escape(self, mock_run_git) -> None:
        diff_output = 'diff --git a/foo.py b/foo.py\n--- "a/foo\\q.py"\n+++ b/foo.py\n@@ -1 +1 @@\n-old\n+new\n'
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_keeps_patch_id_for_created_file_without_old_location(self, mock_run_git) -> None:
        diff_output = "diff --git a/created.py b/created.py\n--- /dev/null\n+++ b/created.py\n@@ -0,0 +1 @@\n+new\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:created.py"): RuntimeError("blob unavailable"),
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result == "patch-id:1045a6f6deadbeef"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_ambiguous_location_file_lookup_fails(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -2,3 +2,3 @@\n"
            " context\n"
            "-old\n"
            "+new\n"
            " context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): RuntimeError("blob unavailable"),
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_appends_location_fingerprint_for_insert_only_hunk(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n--- a/foo.py\n+++ b/foo.py\n@@ -2,1 +2,2 @@\n context\n+new\n context\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "context\ncontext\n",
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result == "patch-id:1045a6f6deadbeef"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_location_candidates_cannot_be_resolved(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -1,3 +1,4 @@\n"
            " ctx\n"
            "-old\n"
            "+new\n"
            "+new_extra\n"
            " tail\n"
            "\\ No newline at end of file\n"
            "\n"
            "@@ -4,4 +5,4 @@\n"
            " ctx\n"
            "-old2\n"
            "+new2\n"
            " ctx\n"
            " tail\n"
            "diff --git a/baz.py b/baz.py\n"
            "--- a/baz.py\n"
            "+++ b/baz.py\n"
            "@@ -1,4 +1,2 @@\n"
            " ctx\n"
            "-olda\n"
            "-oldb\n"
            "-oldc\n"
            "+new\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "old\ntail\nctx\nold2\nctx\ntail\n",
                ("show", "origin/main:baz.py"): "ctx\n",
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_location_digest_reuses_cached_file_and_filters_mismatched_after_context(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/foo.py b/foo.py\n"
            "--- a/foo.py\n"
            "+++ b/foo.py\n"
            "@@ -5,3 +5,3 @@\n"
            " ctx\n"
            "-old\n"
            "+new\n"
            " ctx\n"
            "@@ -2,3 +2,3 @@\n"
            " ctx\n"
            "-old\n"
            "+new2\n"
            " ctx\n"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:foo.py"): "ctx\nold\nwrong\nctx\nold\nctx\n",
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result == "patch-id:1045a6f6deadbeef"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_diff_hunk_lacks_file_headers(self, mock_run_git) -> None:
        diff_output = "diff --git a/foo.py b/foo.py\n@@ -1,2 +1,2 @@\n-old\n+new\n?metadata\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_keeps_patch_id_when_text_diff_has_no_hunks(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): "diff --git a/foo.py b/foo.py\n",
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result == "patch-id:1045a6f6deadbeef"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_passes_diff_to_patch_id_verbatim_on_stdin(self, mock_run_git) -> None:
        """``--verbatim`` is required — ``--stable`` collides on whitespace-only edits."""
        diff_output = "diff --git a/foo.py b/foo.py\n+  spaced  "
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
            },
            patch_id_output="ed1721a8 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        provider.compute_diff_hash(base_branch="main", sha="abc123")

        mock_run_git.assert_any_call(["patch-id", "--verbatim"], stdin_text=diff_output)

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_sha256_fingerprint_when_diff_is_empty(self, mock_run_git) -> None:
        """An empty diff returns a stable sha256 fingerprint for rebase invariance."""
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): "",
            },
            patch_id_output="\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("sha256:")
        # Two calls with the same (empty) diff must produce the same fingerprint.
        assert result == provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_fetch_base_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = RuntimeError("network failure")
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="failed to fetch base branch main"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_returns_none_when_sha_unavailable_and_targeted_fetch_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "deadbeef^{commit}"): RuntimeError("unknown object"),
                ("fetch", "--no-tags", "origin", "deadbeef"): RuntimeError("sha not found"),
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="deadbeef")

        assert result is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fetches_sha_when_not_locally_available(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): RuntimeError("not available"),
                ("fetch", "--no-tags", "origin", "abc123"): "",
                ("diff", "-U1", "origin/main...abc123"): "some diff content",
            },
            patch_id_output="cafebabe 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result == "patch-id:cafebabe"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_git_diff_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): RuntimeError("diff command failed"),
            }
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git diff origin/main...abc123 failed"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_patch_id_fails(self, mock_run_git) -> None:
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): "diff --git a/foo.py b/foo.py\n+x",
            },
            patch_id_exc=RuntimeError("patch-id unavailable"),
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git patch-id --verbatim failed"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_includes_raw_binary_fingerprint_when_diff_has_binary_marker(self, mock_run_git) -> None:
        """Binary marker diffs include a raw-object fingerprint to avoid collisions."""
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("diff", "--numstat", "-z", "origin/main...abc123"): "-\t-\timage.png\0",
                ("diff", "--raw", "--no-abbrev", "-z", "origin/main...abc123"): (
                    ":100644 100644 1111111111111111111111111111111111111111 "
                    "2222222222222222222222222222222222222222 M\0image.png\0"
                ),
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result is not None
        assert result.startswith("patch-id:1045a6f6deadbeef|raw-sha256:")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_binary_fingerprint_ignores_unrelated_text_raw_entries(self, mock_run_git) -> None:
        diff_output = (
            "diff --git a/image.png b/image.png\n"
            "Binary files a/image.png and b/image.png differ\n"
            "diff --git a/text.py b/text.py\n"
            "--- a/text.py\n+++ b/text.py\n@@ -1 +1 @@\n-old\n+new\n"
        )
        binary_raw = (
            ":100644 100644 1111111111111111111111111111111111111111 "
            "2222222222222222222222222222222222222222 M\0image.png\0"
        )
        raw_diff_output = (
            binary_raw + ":100644 100644 aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa "
            "bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb M\0text.py\0"
        )
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("show", "origin/main:text.py"): "old\n",
                ("diff", "--numstat", "-z", "origin/main...abc123"): ("-\t-\t\0image.png\0" + "1\t1\t\0text.py\0"),
                ("diff", "--raw", "--no-abbrev", "-z", "origin/main...abc123"): raw_diff_output,
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        expected = hashlib.sha256(binary_raw.encode()).hexdigest()
        assert result == (f"patch-id:1045a6f6deadbeef|raw-sha256:{expected}")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_binary_numstat_cannot_be_read(self, mock_run_git) -> None:
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("diff", "--numstat", "-z", "origin/main...abc123"): RuntimeError("numstat failed"),
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git diff --numstat origin/main...abc123 failed"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_binary_numstat_has_no_paths(self, mock_run_git) -> None:
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("diff", "--numstat", "-z", "origin/main...abc123"): "-\t-\t\0",
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.compute_diff_hash(base_branch="main", sha="abc123") is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_for_malformed_or_nonbinary_numstat_records(self, mock_run_git) -> None:
        """Malformed records and text-only numstat entries do not produce binary fingerprints."""
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        provider = GitHubActionsProvider(repo="owner/repo")

        for numstat in ("malformed\0", "1\t1\ttext.py\0", "-\t-\t\0"):
            mock_run_git.side_effect = _git_stub(
                {
                    ("fetch", "origin", "main"): "",
                    ("cat-file", "-e", "abc123^{commit}"): "",
                    ("diff", "-U1", "origin/main...abc123"): diff_output,
                    ("diff", "--numstat", "-z", "origin/main...abc123"): numstat,
                },
                patch_id_output="1045a6f6deadbeef 0000\n",
            )
            assert provider.compute_diff_hash(base_branch="main", sha="abc123") is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_binary_raw_record_is_invalid(self, mock_run_git) -> None:
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        provider = GitHubActionsProvider(repo="owner/repo")

        for raw_diff in ("not raw\0image.png\0", ":100644 100644 old new M\0\0"):
            mock_run_git.side_effect = _git_stub(
                {
                    ("fetch", "origin", "main"): "",
                    ("cat-file", "-e", "abc123^{commit}"): "",
                    ("diff", "-U1", "origin/main...abc123"): diff_output,
                    ("diff", "--numstat", "-z", "origin/main...abc123"): "-\t-\t\0image.png\0",
                    ("diff", "--raw", "--no-abbrev", "-z", "origin/main...abc123"): raw_diff,
                },
                patch_id_output="1045a6f6deadbeef 0000\n",
            )
            assert provider.compute_diff_hash(base_branch="main", sha="abc123") is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_fails_closed_when_binary_raw_path_is_not_matched(self, mock_run_git) -> None:
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("diff", "--numstat", "-z", "origin/main...abc123"): "-\t-\t\0image.png\0",
                ("diff", "--raw", "--no-abbrev", "-z", "origin/main...abc123"): (
                    ":100644 100644 old old2 M\0other.png\0"
                ),
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        assert provider.compute_diff_hash(base_branch="main", sha="abc123") is None

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_matches_both_paths_in_binary_rename_raw_record(self, mock_run_git) -> None:
        diff_output = "diff --git a/old.bin b/new.bin\nBinary files a/old.bin and b/new.bin differ\n"
        raw_diff = ":100644 100644 oldsha newsha R100\0old.bin\0new.bin\0"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("diff", "--numstat", "-z", "origin/main...abc123"): "-\t-\t\0old.bin\0new.bin\0",
                ("diff", "--raw", "--no-abbrev", "-z", "origin/main...abc123"): raw_diff,
            },
            patch_id_output="1045a6f6deadbeef 0000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        result = provider.compute_diff_hash(base_branch="main", sha="abc123")

        assert result == f"patch-id:1045a6f6deadbeef|raw-sha256:{hashlib.sha256(raw_diff.encode()).hexdigest()}"

    @patch.object(GitHubActionsProvider, "_run_git")
    def test_raises_runtime_error_when_raw_diff_fails_for_binary_marker(self, mock_run_git) -> None:
        """Binary-marker diffs fail closed if supplemental raw diff cannot be computed."""
        diff_output = "diff --git a/image.png b/image.png\nBinary files a/image.png and b/image.png differ\n"
        mock_run_git.side_effect = _git_stub(
            {
                ("fetch", "origin", "main"): "",
                ("cat-file", "-e", "abc123^{commit}"): "",
                ("diff", "-U1", "origin/main...abc123"): diff_output,
                ("diff", "--numstat", "-z", "origin/main...abc123"): "-\t-\t\0image.png\0",
                ("diff", "--raw", "--no-abbrev", "-z", "origin/main...abc123"): RuntimeError("raw diff failed"),
            },
            patch_id_output="1045a6f6deadbeef 0000000000000000000000000000000000000000\n",
        )
        provider = GitHubActionsProvider(repo="owner/repo")

        with pytest.raises(RuntimeError, match="git diff --raw -z origin/main...abc123 failed"):
            provider.compute_diff_hash(base_branch="main", sha="abc123")
