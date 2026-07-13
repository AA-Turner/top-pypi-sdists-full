import pytest
from sage.tests.rubric_checker import verify_sms_with_rubric

# Real cloud API calls — integration only.
pytestmark = [
    pytest.mark.timeout(900),
    pytest.mark.integration,
]


@pytest.mark.parametrize("platform", ["phaser_arcade", "unity_controller", "godot_movement"])
def test_game_framework_generation_sms(platform, tmp_path):
    """Verify video game player movement scripts via SMS."""
    prompt = f"Implement a complete {platform} video game player movement script."
    verify_sms_with_rubric(prompt, tmp_path)
