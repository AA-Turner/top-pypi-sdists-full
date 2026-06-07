import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_01():
    """Verify exhaustive task creation via CLI: Make a music video with moviepy that says 'I love ..."""
    prompt = "Make a music video with moviepy that says 'I love you Lily'."
    verify_cli_with_rubric(prompt)
