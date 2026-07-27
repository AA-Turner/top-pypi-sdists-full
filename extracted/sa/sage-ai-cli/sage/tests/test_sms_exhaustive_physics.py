import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_physics(tmp_path):
    """Verify exhaustive 2D physics engine JavaScript browser game creation via SMS."""
    prompt = "Develop a 2D physics engine in JavaScript for a browser game."
    verify_sms_with_rubric(prompt, tmp_path)
