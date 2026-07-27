import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_20(tmp_path):
    prompt = "Implement a singly linked list in Python."
    verify_website_with_rubric(prompt, tmp_path)
