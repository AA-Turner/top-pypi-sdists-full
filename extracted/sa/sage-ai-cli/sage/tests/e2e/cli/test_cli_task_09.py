import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_09(tmp_path):
    prompt = "Generate a JSON schema for a simple user profile."
    verify_cli_with_rubric(prompt, tmp_path)
