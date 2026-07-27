import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_03(tmp_path):
    prompt = "Generate a simple React functional component that renders a button."
    verify_website_with_rubric(prompt, tmp_path)
