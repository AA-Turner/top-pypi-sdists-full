import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_23(tmp_path):
    prompt = "Generate a basic package.json file."
    verify_website_with_rubric(prompt, tmp_path)
