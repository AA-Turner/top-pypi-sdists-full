import os
import sys
import pytest
from sage.core.sms_bridge import SAGEMessageBridge, SMSConfig
from pathlib import Path


def verify_sms_capability(domain, prompt, tmp_path):
    # Set up SMS Configuration pointing to our isolated temp path
    cfg = SMSConfig(
        computer_name="TestPC",
        working_dir=str(tmp_path),
        model="cloud:qwen3-coder"
    )
    
    # Standard media output target path
    tmp_vid = os.path.join(tmp_path, "generated_media.mp4")
    if os.path.exists(tmp_vid):
        os.remove(tmp_vid)
    tmp_img = os.path.join(tmp_path, "logo.svg")
    if os.path.exists(tmp_img):
        os.remove(tmp_img)

    # Initialize the real bridge structure
    bridge = SAGEMessageBridge(cfg, token="fake", api_base="http://fake")
    
    # Configure PYTHONPATH environment so the spawned subprocess finds our modules
    project_root = str(Path(__file__).resolve().parents[2])
    os.environ["PYTHONPATH"] = os.path.pathsep.join(filter(None, [
        project_root,
        os.environ.get("PYTHONPATH", "")
    ]))

    try:
        # Run the actual CLI subprocess task loop
        output = bridge._run_sage_task(prompt, mode="agent")
        
        from sage.tests.rubric_checker import check_grading_rubric, is_ignored
        generated_files = [
            f for f in Path(tmp_path).glob("**/*")
            if f.is_file()
            and not is_ignored(f, Path(tmp_path))
            and not f.name.endswith(".pyc")
        ]
        
        check_grading_rubric(output, generated_files)

    finally:
        for p in [tmp_vid, tmp_img]:
            if os.path.exists(p):
                try:
                    os.remove(p)
                except OSError:
                    pass


def test_sms_exhaustive_websites(tmp_path):
    """Exhaustive test for websites via SMS Bridge."""
    verify_sms_capability("websites", "Create a responsive advertising dashboard using React and Tailwind.", tmp_path)


def test_sms_exhaustive_mobile_apps(tmp_path):
    """Exhaustive test for mobile_apps via SMS Bridge."""
    verify_sms_capability("mobile_apps", "Build a React Native feed with infinite scrolling.", tmp_path)


def test_sms_exhaustive_video_games(tmp_path):
    """Exhaustive test for video_games via SMS Bridge."""
    verify_sms_capability("video_games", "Develop a 2D physics engine in JavaScript for a browser game.", tmp_path)


def test_sms_exhaustive_backend_services(tmp_path):
    """Exhaustive test for backend_services via SMS Bridge."""
    verify_sms_capability("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.", tmp_path)


def test_sms_exhaustive_deployments(tmp_path):
    """Exhaustive test for deployments via SMS Bridge."""
    verify_sms_capability("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.", tmp_path)


def test_sms_exhaustive_videos(tmp_path):
    """Exhaustive test for videos via SMS Bridge."""
    verify_sms_capability("videos", "Make a music video with moviepy that says 'I love you Lily'.", tmp_path)


def test_sms_exhaustive_images(tmp_path):
    """Exhaustive test for images via SMS Bridge."""
    verify_sms_capability("images", "Generate a professional SVG logo and PNG favicon.", tmp_path)


def test_sms_exhaustive_audio_files(tmp_path):
    """Exhaustive test for audio_files via SMS Bridge."""
    verify_sms_capability("audio_files", "Synthesize a WAV audio file playing a C major chord.", tmp_path)


def test_sms_exhaustive_music_videos(tmp_path):
    """Exhaustive test for music_videos via SMS Bridge."""
    verify_sms_capability("music_videos", "Combine generated audio and video into an MP4 music video.", tmp_path)


def test_sms_exhaustive_generate_files(tmp_path):
    """Exhaustive test for generate_files via SMS Bridge."""
    verify_sms_capability("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.", tmp_path)


def test_sms_exhaustive_run_applications(tmp_path):
    """Exhaustive test for run_applications via SMS Bridge."""
    verify_sms_capability("run_applications", "Open the Messages app on my Mac and prepare a text.", tmp_path)


def test_sms_exhaustive_computer_control(tmp_path):
    """Exhaustive test for computer_control via SMS Bridge."""
    verify_sms_capability("computer_control", "Use osascript to change my system volume and toggle dark mode.", tmp_path)


def test_sms_exhaustive_text_messages(tmp_path):
    """Exhaustive test for text_messages via SMS Bridge."""
    verify_sms_capability("text_messages", "Send a text message using the SMS bridge natively.", tmp_path)


def test_sms_exhaustive_phone_calls(tmp_path):
    """Exhaustive test for phone_calls via SMS Bridge."""
    verify_sms_capability("phone_calls", "Trigger an API call to Twilio to initiate a phone call.", tmp_path)
