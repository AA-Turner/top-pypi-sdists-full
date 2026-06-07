import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_bridge_task_14(tmp_path):
    """Verify exhaustive task creation via SMS: Create a simple Makefile for a C program...."""
    prompt = "Create a simple Makefile for a C program."
    verify_sms_with_rubric(prompt, tmp_path)
