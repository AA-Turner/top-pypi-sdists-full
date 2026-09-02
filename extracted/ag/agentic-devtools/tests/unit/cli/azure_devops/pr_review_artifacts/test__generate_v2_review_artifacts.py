"""Tests for _generate_v2_review_artifacts (full orchestration)."""

import json
from unittest.mock import patch

from agentic_devtools.cli.azure_devops.pr_review_artifacts import _generate_v2_review_artifacts

_MODULE = "agentic_devtools.cli.azure_devops.pr_review_artifacts"

_CONFIG = {
    "enabled": True,
    "defaultDepth": "deep",
    "deepGlobs": ["**/auth/**", "**/*.sql"],
    "lightGlobs": ["**/*.md", "**/*.lock"],
    "minDiffLinesForDeep": 20,
    "maxDeepModelCalls": 30,
    "maxDeepTotalChangedLines": 2000,
    "maxReviewMinutes": 60,
}

_PR_DETAILS = {
    "pullRequest": {
        "title": "T",
        "description": "d",
        "lastMergeSourceCommit": {"commitId": "abc123def456"},
    },
    "files": [
        {
            "path": "/src/a.py",
            "changeType": "M",
            "addedLineCount": 3,
            "removedLineCount": 1,
            "isBinary": False,
            "addedLines": [],
        }
    ],
}


def _state(values):
    def _get(key, default=None):
        return values.get(key, default)

    return _get


class TestGenerateV2ReviewArtifactsInner:
    def test_generates_all_artifacts(self, tmp_path):
        prompts_dir = tmp_path / "pr"
        prompts_dir.mkdir()
        (prompts_dir / "file-a.md").write_text("PROMPT", encoding="utf-8")
        (prompts_dir / "queue.json").write_text(
            json.dumps({"pending": [{"path": "/src/a.py", "normalizedPath": "/src/a.py", "promptFile": "file-a.md"}]}),
            encoding="utf-8",
        )
        values = {"review.commit_hash_short": "abc123def456", "jira.issue_key": "J-1"}
        with (
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(f"{_MODULE}.load_triage_config", return_value=_CONFIG),
        ):
            _generate_v2_review_artifacts(1, _PR_DETAILS, prompts_dir)

        manifest = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["budget"] is not None
        assert manifest["triage"]["enabled"] is True
        assert (prompts_dir / "pr-context.md").exists()
        answers = list((prompts_dir / "answers").glob("*.answer.json"))
        assert len(answers) == 1
        queue = json.loads((prompts_dir / "queue.json").read_text(encoding="utf-8"))
        assert "reviewDepth" in queue["pending"][0]

    def test_falls_back_to_extracted_commit_hash_for_manifest_short_hash(self, tmp_path):
        prompts_dir = tmp_path / "pr"
        prompts_dir.mkdir()
        (prompts_dir / "file-a.md").write_text("PROMPT", encoding="utf-8")
        (prompts_dir / "queue.json").write_text(
            json.dumps({"pending": [{"path": "/src/a.py", "normalizedPath": "/src/a.py", "promptFile": "file-a.md"}]}),
            encoding="utf-8",
        )
        values = {"review.commit_hash_short": "", "jira.issue_key": "J-1"}
        pr_details = {
            **_PR_DETAILS,
            "pullRequest": {
                **_PR_DETAILS["pullRequest"],
                "lastMergeSourceCommit": {"commitId": "1234567890abcdef1234567890abcdef12345678"},
            },
        }
        with (
            patch(f"{_MODULE}.get_value", side_effect=_state(values)),
            patch(f"{_MODULE}.resolve_repo_root", return_value=str(tmp_path)),
            patch(f"{_MODULE}.load_review_focus_areas", return_value=None),
            patch(f"{_MODULE}.load_triage_config", return_value=_CONFIG),
        ):
            _generate_v2_review_artifacts(1, pr_details, prompts_dir)

        manifest = json.loads((prompts_dir / "manifest.json").read_text(encoding="utf-8"))
        assert manifest["commitHash"] == "1234567890abcdef1234567890abcdef12345678"
        assert manifest["commitHashShort"] == "1234567890ab"
