"""Tests for resolve_review_artifact_dir_name helper."""

import json
import os
from contextlib import contextmanager
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.helpers import resolve_review_artifact_dir_name


class TestResolveReviewArtifactDirName:
    """Tests for resolve_review_artifact_dir_name."""

    def test_returns_commit_hash_when_valid(self):
        """Returns the commit hash unchanged when it is a valid dir segment."""
        result = resolve_review_artifact_dir_name(123, "abc12345")
        assert result == "abc12345"

    def test_strips_whitespace_from_valid_commit_hash(self, capsys):
        """Leading/trailing whitespace is stripped from the returned segment."""
        result = resolve_review_artifact_dir_name(123, " deadbeef ")
        assert result == "deadbeef"
        # No warning should be emitted for a value that's safe after stripping
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_returns_str_when_valid(self):
        """Return type is always str."""
        result = resolve_review_artifact_dir_name(123, "abc12345")
        assert isinstance(result, str)

    def test_coerces_non_str_int_to_str(self):
        """A valid integer value is coerced to str without TypeError."""
        result = resolve_review_artifact_dir_name(99, 12345678)
        assert result == "12345678"
        assert isinstance(result, str)

    def test_falls_back_to_pr_id_when_none(self, capsys):
        """Returns PR<id> fallback when commit_hash_short is None."""
        result = resolve_review_artifact_dir_name(99999, None)
        assert result == "PR99999"
        captured = capsys.readouterr()
        assert "PR99999" in captured.err
        assert "not set" in captured.err

    def test_falls_back_to_pr_id_when_empty_string(self, capsys):
        """Returns PR<id> fallback when commit_hash_short is empty string."""
        result = resolve_review_artifact_dir_name(42, "")
        assert result == "PR42"
        captured = capsys.readouterr()
        assert "PR42" in captured.err

    def test_falls_back_to_pr_id_when_whitespace_only(self, capsys):
        """Whitespace-only values are treated as absent after stripping."""
        result = resolve_review_artifact_dir_name(42, "   ")
        assert result == "PR42"
        captured = capsys.readouterr()
        assert "PR42" in captured.err
        assert "not set" in captured.err

    def test_falls_back_to_pr_id_when_unsafe_path_traversal(self, capsys):
        """Returns PR<id> fallback when commit_hash_short contains '..'."""
        result = resolve_review_artifact_dir_name(12345, "../evil")
        assert result == "PR12345"
        captured = capsys.readouterr()
        assert "PR12345" in captured.err
        assert "unsafe" in captured.err

    def test_uses_repr_formatting_for_unsafe_value(self, capsys):
        """Unsafe value is printed with repr() to prevent log injection."""
        result = resolve_review_artifact_dir_name(1, "line1\nline2")
        assert result == "PR1"
        captured = capsys.readouterr()
        # The repr of the unsafe value must appear (with quotes and escaped newline),
        # not the raw value — this ensures log injection is actually prevented.
        assert "'line1\\nline2'" in captured.err

    def test_falls_back_to_pr_id_when_unsafe_slash(self, capsys):
        """Returns PR<id> fallback when commit_hash_short contains '/'."""
        result = resolve_review_artifact_dir_name(7, "a/b")
        assert result == "PR7"
        captured = capsys.readouterr()
        assert "unsafe" in captured.err

    def test_falls_back_to_pr_id_when_unsafe_colon(self, capsys):
        """Returns PR<id> fallback when commit_hash_short contains ':'."""
        result = resolve_review_artifact_dir_name(7, "C:evil")
        assert result == "PR7"
        captured = capsys.readouterr()
        assert "unsafe" in captured.err

    def test_falls_back_when_coerced_value_is_unsafe(self, capsys):
        """Values that coerce to an unsafe segment must warn and use PR fallback."""

        class UnsafeAfterCoercion:
            def __str__(self):
                return "../deadbeef"

        result = resolve_review_artifact_dir_name(321, UnsafeAfterCoercion())
        assert result == "PR321"
        captured = capsys.readouterr()
        assert "unsafe" in captured.err
        assert "PR321" in captured.err

    def test_recovers_from_review_state_and_backfills_state(self, tmp_path, capsys):
        """When state key is absent, resolves from review-state.json and self-heals state."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {
            "prId": 25553,
            "commitHash": "2fea8cdf46c81234567890abcdef1234",
        }
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")

        captured_state: dict = {}

        @contextmanager
        def _fake_rmw():
            yield captured_state

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.helpers.read_modify_write_state", new=_fake_rmw),
        ):
            result = resolve_review_artifact_dir_name(25553, None)

        assert result == "2fea8cdf46c8"
        assert captured_state.get("review", {}).get("commit_hash_short") == "2fea8cdf46c8"
        assert capsys.readouterr().err == ""

    def test_backfill_merges_into_existing_review_dict(self, tmp_path, capsys):
        """When 'review' is already a dict in state, backfill updates it without replacing it."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")

        captured_state: dict = {"review": {"other_key": "preserved"}}

        @contextmanager
        def _fake_rmw():
            yield captured_state

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.helpers.read_modify_write_state", new=_fake_rmw),
        ):
            result = resolve_review_artifact_dir_name(25553, None)

        assert result == "2fea8cdf46c8"
        assert captured_state["review"]["commit_hash_short"] == "2fea8cdf46c8"
        assert captured_state["review"]["other_key"] == "preserved"
        assert capsys.readouterr().err == ""

    def test_backfill_preserves_existing_safe_hash(self, tmp_path, capsys):
        """Backfill should not overwrite a safe hash written concurrently by another process."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")

        captured_state: dict = {"review": {"commit_hash_short": "3fea8cdf46c8"}}

        @contextmanager
        def _fake_rmw():
            yield captured_state

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.helpers.read_modify_write_state", new=_fake_rmw),
        ):
            result = resolve_review_artifact_dir_name(25553, None)

        assert result == "3fea8cdf46c8"
        assert captured_state["review"]["commit_hash_short"] == "3fea8cdf46c8"
        assert capsys.readouterr().err == ""

    def test_recovers_from_existing_artifact_directory_when_review_state_unavailable(self, tmp_path, capsys):
        """Falls back to commit-scoped artifact directory discovery before PR fallback."""
        artifacts_root = tmp_path / "pull-request-review"
        older = artifacts_root / "2fea8cdf46c8"
        newer = artifacts_root / "3fea8cdf46c8"
        older.mkdir(parents=True)
        newer.mkdir(parents=True)
        (older / "manifest.json").write_text('{"pullRequestId": 7}', encoding="utf-8")
        (newer / "queue.json").write_text('{"pullRequestId": 7}', encoding="utf-8")
        os.utime(older, (1_000_000_000, 1_000_000_000))
        os.utime(newer, (1_000_000_100, 1_000_000_100))

        captured_state: dict = {}

        @contextmanager
        def _fake_rmw():
            yield captured_state

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.helpers.read_modify_write_state", new=_fake_rmw),
        ):
            result = resolve_review_artifact_dir_name(7, "")

        assert result == "3fea8cdf46c8"
        assert captured_state.get("review", {}).get("commit_hash_short") == "3fea8cdf46c8"
        assert capsys.readouterr().err == ""

    def test_ignores_unverified_or_mismatched_artifact_directories(self, tmp_path):
        """Artifact discovery must verify ownership before selecting by mtime."""
        artifacts_root = tmp_path / "pull-request-review"
        mismatched = artifacts_root / "2fea8cdf46c8"
        unverified = artifacts_root / "3fea8cdf46c8"
        mismatched.mkdir(parents=True)
        unverified.mkdir(parents=True)
        (mismatched / "manifest.json").write_text('{"pullRequestId": 99}', encoding="utf-8")
        (unverified / "files-on-branch.json").write_text('{"files": ["a.py"]}', encoding="utf-8")
        os.utime(mismatched, (1_000_000_200, 1_000_000_200))
        os.utime(unverified, (1_000_000_300, 1_000_000_300))

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(7, "", warn=False) == "PR7"

    def test_rejects_directory_when_any_marker_belongs_to_different_pr(self, tmp_path):
        """A directory is rejected when any readable marker belongs to a different PR."""
        artifacts_root = tmp_path / "pull-request-review"
        mixed = artifacts_root / "2fea8cdf46c8"
        mixed.mkdir(parents=True)
        # manifest matches but queue belongs to a different PR
        (mixed / "manifest.json").write_text('{"pullRequestId": 7}', encoding="utf-8")
        (mixed / "queue.json").write_text('{"pullRequestId": 99}', encoding="utf-8")
        os.utime(mixed, (1_000_000_200, 1_000_000_200))

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(7, "", warn=False) == "PR7"

    def test_falls_back_when_review_state_pr_id_is_not_an_integer(self, tmp_path):
        """Invalid review-state prId should not crash fallback resolution."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": "not-an-int", "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(25553, None, warn=False) == "PR25553"

    def test_falls_back_when_review_state_pr_id_is_boolean(self, tmp_path):
        """Boolean review-state prId values must not be treated as numeric ownership."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": True, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(1, None, warn=False) == "PR1"

    def test_falls_back_when_review_state_pr_id_is_float(self, tmp_path):
        """Float review-state prId values must not be treated as numeric ownership."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 7.0, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(7, None, warn=False) == "PR7"

    def test_falls_back_when_review_state_pr_id_does_not_match(self, tmp_path):
        """Mismatched PR IDs in review-state.json must not be used."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 10, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(11, None, warn=False) == "PR11"

    def test_falls_back_when_review_state_commit_hash_is_not_string(self, tmp_path):
        """Non-string commitHash in review-state.json is treated as missing."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": 123}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(25553, None, warn=False) == "PR25553"

    def test_falls_back_when_review_state_commit_hash_prefix_is_not_hex(self, tmp_path):
        """Path-safe but non-hex review-state prefixes must be rejected."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "not-a-hash-value"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
        ):
            assert resolve_review_artifact_dir_name(25553, None, warn=False) == "PR25553"

    def test_falls_back_when_artifact_discovery_only_has_invalid_candidates(self, tmp_path):
        """Discovery ignores non-dirs, invalid names, and dirs without marker files."""
        artifacts_root = tmp_path / "pull-request-review"
        artifacts_root.mkdir(parents=True)
        (artifacts_root / "2fea8cdf46c8").write_text("not a dir", encoding="utf-8")
        invalid_name_dir = artifacts_root / "not-a-hash"
        invalid_name_dir.mkdir()
        (invalid_name_dir / "manifest.json").write_text("{}", encoding="utf-8")
        no_marker_dir = artifacts_root / "3fea8cdf46c8"
        no_marker_dir.mkdir()
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(7, "", warn=False) == "PR7"

    def test_falls_back_when_artifact_manifest_is_not_a_dict(self, tmp_path):
        """Manifest payloads that are not JSON objects are ignored."""
        artifacts_root = tmp_path / "pull-request-review"
        candidate = artifacts_root / "2fea8cdf46c8"
        candidate.mkdir(parents=True)
        (candidate / "manifest.json").write_text('["not-a-dict"]', encoding="utf-8")
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(7, "", warn=False) == "PR7"

    def test_falls_back_when_artifact_manifest_pr_id_is_not_int(self, tmp_path):
        """Manifest ownership with non-integer PR IDs must be ignored."""
        artifacts_root = tmp_path / "pull-request-review"
        candidate = artifacts_root / "2fea8cdf46c8"
        candidate.mkdir(parents=True)
        (candidate / "manifest.json").write_text('{"pullRequestId": "bad"}', encoding="utf-8")
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(7, "", warn=False) == "PR7"

    def test_falls_back_when_artifact_manifest_pr_id_is_boolean(self, tmp_path):
        """Boolean pullRequestId values must not satisfy ownership checks."""
        artifacts_root = tmp_path / "pull-request-review"
        candidate = artifacts_root / "2fea8cdf46c8"
        candidate.mkdir(parents=True)
        (candidate / "manifest.json").write_text('{"pullRequestId": true}', encoding="utf-8")
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(1, "", warn=False) == "PR1"

    def test_falls_back_when_artifact_manifest_pr_id_is_float(self, tmp_path):
        """Float pullRequestId values must not satisfy ownership checks."""
        artifacts_root = tmp_path / "pull-request-review"
        candidate = artifacts_root / "2fea8cdf46c8"
        candidate.mkdir(parents=True)
        (candidate / "manifest.json").write_text('{"pullRequestId": 7.0}', encoding="utf-8")
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(7, "", warn=False) == "PR7"

    def test_falls_back_when_artifact_candidate_stat_fails(self, tmp_path):
        """OSError while reading candidate metadata should be ignored."""
        artifacts_root = tmp_path / "pull-request-review"
        candidate = artifacts_root / "2fea8cdf46c8"
        candidate.mkdir(parents=True)
        (candidate / "manifest.json").write_text('{"pullRequestId": 7}', encoding="utf-8")
        candidate_calls = {"count": 0}

        def _stat_side_effect(self, *args, **kwargs):
            if self == candidate:
                candidate_calls["count"] += 1
                if candidate_calls["count"] > 1:
                    raise OSError("boom")
            return original_stat(self, *args, **kwargs)

        original_stat = __import__("pathlib").Path.stat
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("pathlib.Path.stat", autospec=True, side_effect=_stat_side_effect),
        ):
            assert resolve_review_artifact_dir_name(7, None, warn=False) == "PR7"

    def test_continues_when_state_backfill_fails_for_none_input(self, tmp_path):
        """Best-effort state backfill must not block successful recovery (None input)."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.read_modify_write_state", side_effect=RuntimeError("lock")
            ),
        ):
            assert resolve_review_artifact_dir_name(25553, None) == "2fea8cdf46c8"

    def test_continues_when_state_backfill_fails_for_empty_string_input(self, tmp_path):
        """Best-effort state backfill must not block successful recovery (empty input)."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
            patch(
                "agentic_devtools.cli.azure_devops.helpers.read_modify_write_state", side_effect=RuntimeError("lock")
            ),
        ):
            assert resolve_review_artifact_dir_name(25553, "") == "2fea8cdf46c8"

    def test_no_warning_when_valid(self, capsys):
        """No stderr warning is emitted when commit_hash_short is valid."""
        resolve_review_artifact_dir_name(5, "deadbeef")
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_no_warning_when_warn_false_and_absent(self, capsys):
        """No warning is emitted when warn=False, even when commit_hash_short is absent."""
        result = resolve_review_artifact_dir_name(42, None, warn=False)
        assert result == "PR42"
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_no_warning_when_warn_false_and_unsafe(self, capsys):
        """No warning is emitted when warn=False, even when commit_hash_short is unsafe."""
        result = resolve_review_artifact_dir_name(7, "../evil", warn=False)
        assert result == "PR7"
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_no_warning_when_warn_false_and_empty_string(self, capsys):
        """No warning is emitted when warn=False, even when commit_hash_short is empty string."""
        result = resolve_review_artifact_dir_name(7, "", warn=False)
        assert result == "PR7"
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_no_warning_when_warn_false_and_whitespace_only(self, capsys):
        """No warning is emitted when warn=False with whitespace-only commit_hash_short."""
        result = resolve_review_artifact_dir_name(7, "   ", warn=False)
        assert result == "PR7"
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_allow_discovery_false_skips_fallback_recovery(self, tmp_path):
        """Scaffold callers can disable fallback discovery and force PR-id fallback."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(25553, None, warn=False, allow_discovery=False) == "PR25553"

    def test_allow_discovery_false_warns_when_warn_true(self, tmp_path, capsys):
        """Disabling discovery still emits the usual absent-hash warning when warn=True."""
        with patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path):
            assert resolve_review_artifact_dir_name(25553, None, allow_discovery=False) == "PR25553"
        captured = capsys.readouterr()
        assert "PR25553" in captured.err
        assert "not set" in captured.err

    def test_integer_zero_is_not_treated_as_absent(self, capsys):
        """Integer 0 is falsy but should be coerced to '0' (not treated as absent)."""
        # is_safe_dir_segment("0") → True, so the result should be "0", not "PR<id>"
        result = resolve_review_artifact_dir_name(99, 0)
        assert result == "0"
        # No "not set" warning should be emitted
        captured = capsys.readouterr()
        assert "not set" not in captured.err

    def test_falls_back_when_str_raises(self, capsys):
        """Falls back to PR<id> when str(commit_hash_short) raises, matching the docstring."""

        class BadStr:
            def __str__(self):
                raise RuntimeError("__str__ not allowed")

        result = resolve_review_artifact_dir_name(55, BadStr())
        assert result == "PR55"
        captured = capsys.readouterr()
        assert "PR55" in captured.err
        assert "could not be coerced" in captured.err

    def test_no_warning_when_str_raises_and_warn_false(self, capsys):
        """No warning when str() raises and warn=False."""

        class BadStr:
            def __str__(self):
                raise RuntimeError("__str__ not allowed")

        result = resolve_review_artifact_dir_name(55, BadStr(), warn=False)
        assert result == "PR55"
        captured = capsys.readouterr()
        assert captured.err == ""

    def test_safe_repr_fallback_when_reprlib_raises(self, capsys):
        """When reprlib.repr() itself raises, _safe_repr falls back to type name."""
        from unittest.mock import patch

        class UnsafeValue:
            def __str__(self):
                raise RuntimeError("no str")

        # Patch reprlib.repr to simulate a pathological environment where it raises.
        with patch(
            "agentic_devtools.cli.azure_devops.helpers.reprlib.repr",
            side_effect=RuntimeError("repr exploded"),
        ):
            result = resolve_review_artifact_dir_name(77, UnsafeValue())

        assert result == "PR77"
        captured = capsys.readouterr()
        # Warning must mention the fallback
        assert "PR77" in captured.err

    def test_backfill_false_suppresses_state_write_when_review_state_succeeds(self, tmp_path):
        """backfill=False returns the discovered hash without persisting it to state."""
        review_dir = tmp_path / "reviews"
        review_dir.mkdir(parents=True)
        payload = {"prId": 25553, "commitHash": "2fea8cdf46c81234567890abcdef1234"}
        (review_dir / "review-state.json").write_text(json.dumps(payload), encoding="utf-8")

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.review_state.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.helpers.read_modify_write_state") as rmw_mock,
        ):
            result = resolve_review_artifact_dir_name(25553, None, backfill=False)

        assert result == "2fea8cdf46c8"
        rmw_mock.assert_not_called()

    def test_backfill_false_suppresses_state_write_when_artifact_dir_succeeds(self, tmp_path):
        """backfill=False discovers via artifact directory scan without persisting to state."""
        artifacts_root = tmp_path / "pull-request-review"
        candidate = artifacts_root / "3fea8cdf46c8"
        candidate.mkdir(parents=True)
        (candidate / "queue.json").write_text('{"pullRequestId": 7}', encoding="utf-8")

        with (
            patch("agentic_devtools.cli.azure_devops.helpers.get_state_dir", return_value=tmp_path),
            patch("agentic_devtools.cli.azure_devops.helpers.read_modify_write_state") as rmw_mock,
        ):
            result = resolve_review_artifact_dir_name(7, "", backfill=False)

        assert result == "3fea8cdf46c8"
        rmw_mock.assert_not_called()
