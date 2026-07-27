import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_dashboard(tmp_path):
    """Verify exhaustive React/Tailwind advertising dashboard creation via SMS."""
    prompt = "Create a responsive advertising dashboard using React and Tailwind."
    verify_sms_with_rubric(prompt, tmp_path)
