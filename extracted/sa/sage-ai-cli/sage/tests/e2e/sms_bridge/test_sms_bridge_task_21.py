import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_21(tmp_path):
    prompt = "Create a basic nginx.conf template."
    verify_sms_with_rubric(prompt, tmp_path)
