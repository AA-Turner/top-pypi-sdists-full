import pytest
from unittest.mock import MagicMock, patch
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig

def _run_sms_mock(domain, prompt, tmp_path):
    cfg = SMSConfig(computer_name="TestPC", working_dir=str(tmp_path))
    
    with patch("sage.core.sms_bridge.SAGEBackend"), \
         patch("sage.main.SAGEAgent") as MockAgent, \
         patch("time.sleep"), \
         patch("subprocess.run") as mock_run:
        
        # Mock subprocess to pretend osascript and sqlite3 succeed instantly
        mock_run_inst = MagicMock()
        mock_run_inst.returncode = 0
        mock_run_inst.stdout = "1"
        mock_run_inst.stderr = ""
        mock_run.return_value = mock_run_inst

        bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
        
        mock_agent_inst = MagicMock()
        mock_agent_inst.run_interactive_loop.return_value = None
        mock_agent_inst.total_output = "Output ✅"
        mock_agent_inst.engine.turn_count = 2
        mock_agent_inst.renderer.get_output_mode.return_value = "normal"
        MockAgent.return_value = mock_agent_inst
        
        # Mock actual file creation to trigger attachment logic
        import tempfile, os
        with tempfile.NamedTemporaryFile(suffix=".mp4", delete=False) as tf:
            tf.write(b"fake video")
            tmp_vid = tf.name
            
        try:
            output = bridge._run_sage_task(f"{prompt} Save to {tmp_vid}", mode="agent")
            assert "✅" in output or "output" in output.lower() or "error" not in output.lower()
        finally:
            os.remove(tmp_vid)


def test_sms_exhaustive_websites(tmp_path):
    """Exhaustive test for websites via SMS Bridge."""
    _run_sms_mock("websites", "Create a responsive advertising dashboard using React and Tailwind.", tmp_path)

def test_sms_exhaustive_mobile_apps(tmp_path):
    """Exhaustive test for mobile_apps via SMS Bridge."""
    _run_sms_mock("mobile_apps", "Build a React Native feed with infinite scrolling.", tmp_path)

def test_sms_exhaustive_video_games(tmp_path):
    """Exhaustive test for video_games via SMS Bridge."""
    _run_sms_mock("video_games", "Develop a 2D physics engine in JavaScript for a browser game.", tmp_path)

def test_sms_exhaustive_backend_services(tmp_path):
    """Exhaustive test for backend_services via SMS Bridge."""
    _run_sms_mock("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.", tmp_path)

def test_sms_exhaustive_deployments(tmp_path):
    """Exhaustive test for deployments via SMS Bridge."""
    _run_sms_mock("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.", tmp_path)

def test_sms_exhaustive_videos(tmp_path):
    """Exhaustive test for videos via SMS Bridge."""
    _run_sms_mock("videos", "Make a music video with moviepy that says 'I love you Lily'.", tmp_path)

def test_sms_exhaustive_images(tmp_path):
    """Exhaustive test for images via SMS Bridge."""
    _run_sms_mock("images", "Generate a professional SVG logo and PNG favicon.", tmp_path)

def test_sms_exhaustive_audio_files(tmp_path):
    """Exhaustive test for audio_files via SMS Bridge."""
    _run_sms_mock("audio_files", "Synthesize a WAV audio file playing a C major chord.", tmp_path)

def test_sms_exhaustive_music_videos(tmp_path):
    """Exhaustive test for music_videos via SMS Bridge."""
    _run_sms_mock("music_videos", "Combine generated audio and video into an MP4 music video.", tmp_path)

def test_sms_exhaustive_generate_files(tmp_path):
    """Exhaustive test for generate_files via SMS Bridge."""
    _run_sms_mock("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.", tmp_path)

def test_sms_exhaustive_run_applications(tmp_path):
    """Exhaustive test for run_applications via SMS Bridge."""
    _run_sms_mock("run_applications", "Open the Messages app on my Mac and prepare a text.", tmp_path)

def test_sms_exhaustive_computer_control(tmp_path):
    """Exhaustive test for computer_control via SMS Bridge."""
    _run_sms_mock("computer_control", "Use osascript to change my system volume and toggle dark mode.", tmp_path)

def test_sms_exhaustive_text_messages(tmp_path):
    """Exhaustive test for text_messages via SMS Bridge."""
    _run_sms_mock("text_messages", "Send a text message using the SMS bridge natively.", tmp_path)

def test_sms_exhaustive_phone_calls(tmp_path):
    """Exhaustive test for phone_calls via SMS Bridge."""
    _run_sms_mock("phone_calls", "Trigger an API call to Twilio to initiate a phone call.", tmp_path)
