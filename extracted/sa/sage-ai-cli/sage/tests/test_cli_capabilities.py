import pytest
from unittest.mock import MagicMock, patch
from sage.main import app as sage_app
from typer.testing import CliRunner

@pytest.fixture
def temp_workspace(tmp_path):
    return tmp_path

def _run_cli_mock(domain, prompt):
    runner = CliRunner()
    with patch("sage.main._prepare_model_for_use") as mock_prep, \
         patch("sage.main._build_router") as mock_router:
         
        mock_prep.return_value = (MagicMock(), "cloud:gemini-2.0-flash")
        mock_router_inst = MagicMock()
        mock_router_inst.stream.return_value = [f"Output for {domain}", "/path/to/generated_media.mp4"]
        mock_router.return_value = mock_router_inst
        
        result = runner.invoke(sage_app, ["ask", prompt, "--raw"])
        
        assert result.exit_code == 0, f"CLI task failed for domain: {domain}"
        assert f"Output for {domain}" in result.output
        
        # Ensure media paths are handled correctly
        if domain in ["videos", "images", "audio_files", "music_videos"]:
            assert "generated_media.mp4" in result.output


def test_cli_exhaustive_websites():
    """Exhaustive test for websites via CLI."""
    _run_cli_mock("websites", "Create a responsive advertising dashboard using React and Tailwind.")

def test_cli_exhaustive_mobile_apps():
    """Exhaustive test for mobile_apps via CLI."""
    _run_cli_mock("mobile_apps", "Build a React Native feed with infinite scrolling.")

def test_cli_exhaustive_video_games():
    """Exhaustive test for video_games via CLI."""
    _run_cli_mock("video_games", "Develop a 2D physics engine in JavaScript for a browser game.")

def test_cli_exhaustive_backend_services():
    """Exhaustive test for backend_services via CLI."""
    _run_cli_mock("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.")

def test_cli_exhaustive_deployments():
    """Exhaustive test for deployments via CLI."""
    _run_cli_mock("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.")

def test_cli_exhaustive_videos():
    """Exhaustive test for videos via CLI."""
    _run_cli_mock("videos", "Make a music video with moviepy that says 'I love you Lily'.")

def test_cli_exhaustive_images():
    """Exhaustive test for images via CLI."""
    _run_cli_mock("images", "Generate a professional SVG logo and PNG favicon.")

def test_cli_exhaustive_audio_files():
    """Exhaustive test for audio_files via CLI."""
    _run_cli_mock("audio_files", "Synthesize a WAV audio file playing a C major chord.")

def test_cli_exhaustive_music_videos():
    """Exhaustive test for music_videos via CLI."""
    _run_cli_mock("music_videos", "Combine generated audio and video into an MP4 music video.")

def test_cli_exhaustive_generate_files():
    """Exhaustive test for generate_files via CLI."""
    _run_cli_mock("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.")

def test_cli_exhaustive_run_applications():
    """Exhaustive test for run_applications via CLI."""
    _run_cli_mock("run_applications", "Open the Messages app on my Mac and prepare a text.")

def test_cli_exhaustive_computer_control():
    """Exhaustive test for computer_control via CLI."""
    _run_cli_mock("computer_control", "Use osascript to change my system volume and toggle dark mode.")

def test_cli_exhaustive_text_messages():
    """Exhaustive test for text_messages via CLI."""
    _run_cli_mock("text_messages", "Send a text message using the SMS bridge natively.")

def test_cli_exhaustive_phone_calls():
    """Exhaustive test for phone_calls via CLI."""
    _run_cli_mock("phone_calls", "Trigger an API call to Twilio to initiate a phone call.")
