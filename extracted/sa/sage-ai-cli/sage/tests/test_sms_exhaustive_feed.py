import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_feed(tmp_path):
    """Verify exhaustive React Native infinite scroll feed creation via SMS."""
    prompt = "Build a React Native feed with infinite scrolling."
    verify_sms_with_rubric(prompt, tmp_path)
