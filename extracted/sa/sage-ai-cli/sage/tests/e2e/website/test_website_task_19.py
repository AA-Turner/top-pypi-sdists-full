import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_19(tmp_path):
    prompt = "Generate a basic README.md markdown template."
    verify_website_with_rubric(prompt, tmp_path)
