import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_27(tmp_path):
    """Verify exhaustive task creation via SMS: Create a basic nginx configuration file...."""
    prompt = "Create a basic nginx configuration file."
    verify_sms_with_rubric(prompt, tmp_path)
