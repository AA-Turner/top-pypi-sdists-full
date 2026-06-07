import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

def test_cli_task_21():
    """Verify exhaustive task creation via CLI: Write a python script to resize an image using Pil..."""
    prompt = "Write a python script to resize an image using Pillow."
    verify_cli_with_rubric(prompt)
