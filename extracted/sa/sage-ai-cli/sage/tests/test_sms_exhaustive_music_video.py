import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

def test_sms_exhaustive_music_video(tmp_path):
    """Verify exhaustive moviepy music video 'I love you Lily' creation via SMS."""
    prompt = "Make a music video with moviepy that says 'I love you Lily'."
    verify_sms_with_rubric(prompt, tmp_path)
