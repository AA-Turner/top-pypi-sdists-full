import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_01():
    """Verify exhaustive task creation via Website: Make a music video with moviepy that says 'I love ..."""
    prompt = "Make a music video with moviepy that says 'I love you Lily'."
    verify_website_with_rubric(prompt)
