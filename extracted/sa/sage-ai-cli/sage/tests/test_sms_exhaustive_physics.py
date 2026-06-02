import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_exhaustive_physics(tmp_path):
    """Verify exhaustive 2D physics engine JavaScript browser game creation via SMS."""
    prompt = "Develop a 2D physics engine in JavaScript for a browser game."
    verify_sms_with_rubric(prompt, tmp_path)
