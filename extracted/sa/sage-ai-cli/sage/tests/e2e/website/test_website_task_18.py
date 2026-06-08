import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_18(tmp_path):
    prompt = "Write a basic Flask application with one route."
    verify_website_with_rubric(prompt, tmp_path)
