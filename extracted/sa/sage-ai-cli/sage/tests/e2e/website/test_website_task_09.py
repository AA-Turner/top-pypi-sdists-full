import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_09(tmp_path):
    prompt = "Generate a JSON schema for a simple user profile."
    verify_website_with_rubric(prompt, tmp_path)
