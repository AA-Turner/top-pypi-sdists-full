import pytest
from sage.tests.rubric_checker import verify_website_with_rubric

def test_website_task_21():
    """Verify exhaustive task creation via Website: Write a python script to resize an image using Pil..."""
    prompt = "Write a python script to resize an image using Pillow."
    verify_website_with_rubric(prompt)
