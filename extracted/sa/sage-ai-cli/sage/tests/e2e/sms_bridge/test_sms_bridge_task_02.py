import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_02(tmp_path):
    prompt = "Build a basic HTML landing page with a header and footer."
    verify_sms_with_rubric(prompt, tmp_path)
