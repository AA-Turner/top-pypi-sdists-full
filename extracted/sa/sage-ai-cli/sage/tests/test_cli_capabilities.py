import os
import re
import pytest
from typer.testing import CliRunner
from sage.cli_core import app as sage_app
from pathlib import Path
from sage.core.content_validator import validate_content


def verify_cli_capability(domain, prompt):
    runner = CliRunner()
    
    # We run SAGE in an isolated filesystem environment so it doesn't pollute the repo.
    with runner.isolated_filesystem():
        # Pass --model option to ensure it uses the local openrouter provider
        result = runner.invoke(sage_app, [
            "ask", prompt, 
            "--raw", 
            "--agent",
            "--model", "cloud:qwen3-coder"
        ])
        
        # Assertions
        assert result.exit_code == 0, f"CLI task failed for domain: {domain}\nOutput: {result.output}"
        
        from sage.tests.rubric_checker import check_grading_rubric, is_ignored
        generated_files = [
            f for f in Path(".").glob("**/*")
            if f.is_file() 
            and not is_ignored(f, Path("."))
            and not f.name.endswith(".pyc")
        ]
        
        check_grading_rubric(result.output, generated_files)



@pytest.mark.timeout(900)
def test_cli_exhaustive_websites():
    """Exhaustive test for websites via CLI."""
    verify_cli_capability("websites", "Create a responsive advertising dashboard using React and Tailwind.")


def test_cli_exhaustive_mobile_apps():
    """Exhaustive test for mobile_apps via CLI."""
    verify_cli_capability("mobile_apps", "Build a React Native feed with infinite scrolling.")


@pytest.mark.timeout(900)
def test_cli_exhaustive_video_games():
    """Exhaustive test for video_games via CLI."""
    verify_cli_capability("video_games", "Develop a 2D physics engine in JavaScript for a browser game.")


def test_cli_exhaustive_backend_services():
    """Exhaustive test for backend_services via CLI."""
    verify_cli_capability("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.")


def test_cli_exhaustive_deployments():
    """Exhaustive test for deployments via CLI."""
    verify_cli_capability("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.")


def test_cli_exhaustive_videos():
    """Exhaustive test for videos via CLI."""
    verify_cli_capability("videos", "Make a music video with moviepy that says 'I love you Lily'.")


def test_cli_exhaustive_images():
    """Exhaustive test for images via CLI."""
    verify_cli_capability("images", "Generate a professional SVG logo and PNG favicon.")


def test_cli_exhaustive_audio_files():
    """Exhaustive test for audio_files via CLI."""
    verify_cli_capability("audio_files", "Synthesize a WAV audio file playing a C major chord.")


def test_cli_exhaustive_music_videos():
    """Exhaustive test for music_videos via CLI."""
    verify_cli_capability("music_videos", "Combine generated audio and video into an MP4 music video.")


def test_cli_exhaustive_generate_files():
    """Exhaustive test for generate_files via CLI."""
    verify_cli_capability("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.")


def test_cli_exhaustive_run_applications():
    """Exhaustive test for run_applications via CLI."""
    verify_cli_capability("run_applications", "Open the Messages app on my Mac and prepare a text.")


def test_cli_exhaustive_computer_control():
    """Exhaustive test for computer_control via CLI."""
    verify_cli_capability("computer_control", "Use osascript to change my system volume and toggle dark mode.")


def test_cli_exhaustive_text_messages():
    """Exhaustive test for text_messages via CLI."""
    verify_cli_capability("text_messages", "Send a text message using the SMS bridge natively.")


def test_cli_exhaustive_phone_calls():
    """Exhaustive test for phone_calls via CLI."""
    verify_cli_capability("phone_calls", "Use a native macOS AppleScript to initiate a FaceTime audio phone call.")
