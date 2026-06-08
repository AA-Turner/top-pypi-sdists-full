import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_12(tmp_path):
    prompt = "Implement binary search in Python."
    verify_cli_with_rubric(prompt, tmp_path)
