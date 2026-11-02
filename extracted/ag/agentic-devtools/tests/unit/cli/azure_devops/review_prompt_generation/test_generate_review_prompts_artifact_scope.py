"""Tests for review-prompt artifact directory selection."""

from unittest.mock import patch

from agentic_devtools.cli.azure_devops import review_prompt_generation


class TestGenerateReviewPromptsArtifactScope:
    def test_unsafe_commit_hash_falls_back_to_pr_directory(self, tmp_path, capsys):
        pr_details = {
            "files": [{"path": "/src/file.ts", "changeType": "edit"}],
            "threads": [],
        }

        with (
            patch.object(review_prompt_generation, "get_state_dir", return_value=tmp_path),
            patch.object(
                review_prompt_generation,
                "get_value",
                side_effect=lambda key, *args, **kwargs: "../../evil" if key == "review.commit_hash_short" else None,
            ),
            patch.object(review_prompt_generation, "set_value"),
        ):
            _, _, _, prompts_dir, _ = review_prompt_generation.generate_review_prompts(
                pull_request_id=42,
                pr_details=pr_details,
            )

        assert prompts_dir == tmp_path / "pull-request-review" / "PR42"
        assert "unsafe" in capsys.readouterr().err
