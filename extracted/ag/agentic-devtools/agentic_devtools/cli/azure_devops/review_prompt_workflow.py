"""State-backed entry points for review prompt generation."""

import json
import sys

from ...state import get_state_dir, get_value
from .review_prompt_generation import generate_review_prompts
from .review_prompt_tracking import _detect_unchanged_files, _persist_processing_paths_to_review_state


def generate_review_prompts_from_state() -> None:
    """Background-task entry point that generates prompts for current PR state."""
    pr_id_raw = get_value("pull_request_id")
    if not pr_id_raw:
        print("Error: pull_request_id is required in state", file=sys.stderr)
        sys.exit(1)

    pull_request_id = int(pr_id_raw)
    details_path = get_state_dir() / "temp-get-pull-request-details-response.json"
    if not details_path.exists():
        print(f"Error: PR details file not found: {details_path}", file=sys.stderr)
        print("Run get_pull_request_details first.", file=sys.stderr)
        sys.exit(1)

    with open(details_path, encoding="utf-8") as f:
        pr_details = json.load(f)

    unchanged_files = _detect_unchanged_files(pull_request_id, pr_details)
    _prompts_generated, _skipped_reviewed, _skipped_not_on_branch, prompts_dir, _skipped_files = (
        generate_review_prompts(
            pull_request_id,
            pr_details,
            unchanged_files=unchanged_files,
        )
    )
    _persist_processing_paths_to_review_state(pull_request_id, prompts_dir)
