import pytest
from sage.tests.rubric_checker import (
    verify_cli_with_rubric,
    verify_sms_with_rubric,
    verify_website_with_rubric
)

TASKS = [
    ("ANDROID-01", "Build BLE-based proximity scanner in Kotlin for ANDROID-01"),
    ("IOS-02", "Create ARKit virtual furniture app in Swift for IOS-02"),
    ("REACT-N-03", "Implement cross-platform video streaming client for REACT-N-03"),
    ("FLUT-04", "Build real-time multiplayer tic-tac-toe in Flutter/Dart for FLUT-04"),
    ("UNITY-05", "Create Unity puzzle game with Ray-casted interaction for UNITY-05"),
    ("UNREAL-06", "Build open-world demo in Unreal Engine C++ for UNREAL-06"),
    ("GODOT-07", "Implement Godot platformer cellular automata level generator for GODOT-07"),
    ("XNA-08", "Create retro-style shooter in MonoGame/C# for XNA-08"),
    ("HTML5-09", "Build Svelte double-pendulum WebAssembly simulation for HTML5-09"),
    ("VR-10", "Develop Oculus Quest VR painting app in Unity for VR-10")
]

@pytest.mark.parametrize("task_id, prompt", TASKS)
def test_platforms_mobile_game_cli(task_id, prompt):
    """Test SAGE CLI interface for mobile and game platforms."""
    verify_cli_with_rubric(prompt)

@pytest.mark.parametrize("task_id, prompt", TASKS)
def test_platforms_mobile_game_sms(task_id, prompt, tmp_path):
    """Test SAGE SMS bridge interface for mobile and game platforms."""
    verify_sms_with_rubric(prompt, tmp_path)

@pytest.mark.parametrize("task_id, prompt", TASKS)
def test_platforms_mobile_game_website(task_id, prompt):
    """Test SAGE website interface for mobile and game platforms."""
    verify_website_with_rubric(prompt)
