import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_07(tmp_path):
    prompt = "Write a SQL query to join a 'users' and 'orders' table."
    verify_website_with_rubric(prompt, tmp_path)
