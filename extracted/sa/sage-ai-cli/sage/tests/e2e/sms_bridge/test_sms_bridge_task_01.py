import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_01(tmp_path):
    """Verify exhaustive task creation via SMS: Make a music video with moviepy that says 'I love ..."""
    prompt = "Make a music video with moviepy that says 'I love you Lily'."
    verify_sms_with_rubric(prompt, tmp_path)
