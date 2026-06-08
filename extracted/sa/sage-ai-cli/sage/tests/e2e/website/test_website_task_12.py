import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_12(tmp_path):
    prompt = "Implement binary search in Python."
    verify_website_with_rubric(prompt, tmp_path)
