import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric, verify_sms_with_rubric, verify_website_with_rubric

@pytest.mark.parametrize("platform", ["phaser_arcade", "unity_controller", "godot_movement"])
def test_game_framework_generation(platform):
    """Verify game platform tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {platform} video game player movement script."
    verify_cli_with_rubric(prompt)


@pytest.mark.parametrize("platform", ["phaser_arcade", "unity_controller", "godot_movement"])
def test_game_framework_generation_sms(platform, tmp_path):
    """Verify game platform tasks via SMS bridge."""
    prompt = f"Implement a complete {platform} video game player movement script."
    verify_sms_with_rubric(prompt, tmp_path)


@pytest.mark.parametrize("platform", ["phaser_arcade", "unity_controller", "godot_movement"])
def test_game_framework_generation_website(platform):
    """Verify game platform tasks via website backend."""
    prompt = f"Implement a complete {platform} video game player movement script."
    verify_website_with_rubric(prompt)
