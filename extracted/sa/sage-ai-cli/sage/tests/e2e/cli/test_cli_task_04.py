import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_04(tmp_path):
    prompt = "Create a Dockerfile for a basic Node.js application."
    verify_cli_with_rubric(prompt, tmp_path)
