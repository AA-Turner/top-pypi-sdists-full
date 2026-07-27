import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


def test_sms_exhaustive_audio(tmp_path):
    """Verify exhaustive WAV audio C major chord synthesis via SMS."""
    prompt = "Synthesize a WAV audio file playing a C major chord."
    verify_sms_with_rubric(prompt, tmp_path)
