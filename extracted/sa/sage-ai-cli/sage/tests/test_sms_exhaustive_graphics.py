import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_exhaustive_graphics(tmp_path):
    """Verify exhaustive professional SVG logo and PNG favicon creation via SMS."""
    prompt = "Generate a professional SVG logo and PNG favicon."
    verify_sms_with_rubric(prompt, tmp_path)
