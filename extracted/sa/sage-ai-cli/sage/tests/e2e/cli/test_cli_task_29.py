import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_29(tmp_path):
    prompt = "Create a simple HTML form with input fields."
    verify_cli_with_rubric(prompt, tmp_path)
