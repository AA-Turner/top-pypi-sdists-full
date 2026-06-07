import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_21(tmp_path):
    """Verify exhaustive task creation via SMS: Write a python script to resize an image using Pil..."""
    prompt = "Write a python script to resize an image using Pillow."
    verify_sms_with_rubric(prompt, tmp_path)
