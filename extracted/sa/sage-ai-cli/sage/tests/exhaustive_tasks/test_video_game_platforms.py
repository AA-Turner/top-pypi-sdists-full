import pytest
from sage.tests.rubric_checker import verify_cli_with_rubric

@pytest.mark.parametrize("platform", ["phaser_arcade", "unity_controller", "godot_movement"])
def test_game_framework_generation(platform):
    """Verify game platform tasks are written cleanly and comply with the grading rubric."""
    prompt = f"Implement a complete {platform} video game player movement script."
    verify_cli_with_rubric(prompt)
