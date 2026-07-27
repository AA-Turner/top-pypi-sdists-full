import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_composite_video(tmp_path):
    """Verify exhaustive MP4 composite music video creation via SMS."""
    prompt = "Combine generated audio and video into an MP4 music video."
    verify_sms_with_rubric(prompt, tmp_path)
