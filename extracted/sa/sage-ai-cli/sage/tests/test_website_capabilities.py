import pytest
import re
from fastapi.testclient import TestClient
from backend.app import app as backend_app
from backend.prompt_engine import clear_cache

@pytest.fixture(autouse=True)
def reload_prompts():
    clear_cache()
from sage.core.content_validator import validate_content


def verify_website_capability(domain, prompt):
    client = TestClient(backend_app)
    
    payload = {
        "messages": [{"role": "user", "content": prompt}],
        "model_id": "cloud:qwen3-coder",
        "conversation_id": "conv-test",
        "temperature": 0.7,
        "max_tokens": 8192,
        "stream": False
    }
    
    response = client.post("/chat", json=payload, headers={"Authorization": "Bearer test-token"})
    assert response.status_code == 200, f"Backend task failed for domain: {domain}, output: {response.text}"
    
    data = response.json()
    assert data.get("ok") is True
    
    output = data.get("output", "")
    assert output, "Backend returned empty response"
    
    # Verify no raw color/ANSI sequences are present in JSON response
    assert "\x1b" not in output, f"JSON response contains raw escape codes:\n{output}"
    assert "\u001b" not in output, f"JSON response contains raw escape codes:\n{output}"
    
    # Verify specific details of the output format based on domain
    if domain == "websites":
        assert "FILE: index.html" in output or "FILE: frontend/index.html" in output or "FILE: App.js" in output or "FILE: App.tsx" in output
        assert "dashboard" in output.lower() or "portfolio" in output.lower() or "website" in output.lower()
    elif domain == "mobile_apps":
        assert "FILE: ItemListScreen.tsx" in output or "FILE: frontend/ItemListScreen.tsx" in output or "FILE: App.js" in output or "FILE: App.tsx" in output or "FILE: FeedScreen.tsx" in output or "FILE: FeedScreen.js" in output
        assert "React Native" in output or "import { View" in output or "from 'react-native'" in output

    elif domain == "backend_services":
        assert "FILE: main.py" in output or "FILE: backend/main.py" in output
        assert "FastAPI" in output or "import fastapi" in output or "from fastapi" in output


def test_website_exhaustive_websites():
    """Exhaustive test for websites via Website Backend."""
    verify_website_capability("websites", "Create a responsive advertising dashboard using React and Tailwind.")


def test_website_exhaustive_mobile_apps():
    """Exhaustive test for mobile_apps via Website Backend."""
    verify_website_capability("mobile_apps", "Build a React Native feed with infinite scrolling.")


def test_website_exhaustive_video_games():
    """Exhaustive test for video_games via Website Backend."""
    verify_website_capability("video_games", "Develop a 2D physics engine in JavaScript for a browser game.")


def test_website_exhaustive_backend_services():
    """Exhaustive test for backend_services via Website Backend."""
    verify_website_capability("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.")


def test_website_exhaustive_deployments():
    """Exhaustive test for deployments via Website Backend."""
    verify_website_capability("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.")


def test_website_exhaustive_videos():
    """Exhaustive test for videos via Website Backend."""
    verify_website_capability("videos", "Make a music video with moviepy that says 'I love you Lily'.")


def test_website_exhaustive_images():
    """Exhaustive test for images via Website Backend."""
    verify_website_capability("images", "Generate a professional SVG logo and PNG favicon.")


def test_website_exhaustive_audio_files():
    """Exhaustive test for audio_files via Website Backend."""
    verify_website_capability("audio_files", "Synthesize a WAV audio file playing a C major chord.")


def test_website_exhaustive_music_videos():
    """Exhaustive test for music_videos via Website Backend."""
    verify_website_capability("music_videos", "Combine generated audio and video into an MP4 music video.")


def test_website_exhaustive_generate_files():
    """Exhaustive test for generate_files via Website Backend."""
    verify_website_capability("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.")


def test_website_exhaustive_run_applications():
    """Exhaustive test for run_applications via Website Backend."""
    verify_website_capability("run_applications", "Open the Messages app on my Mac and prepare a text.")


def test_website_exhaustive_computer_control():
    """Exhaustive test for computer_control via Website Backend."""
    verify_website_capability("computer_control", "Use osascript to change my system volume and toggle dark mode.")


def test_website_exhaustive_text_messages():
    """Exhaustive test for text_messages via Website Backend."""
    verify_website_capability("text_messages", "Send a text message using the SMS bridge natively.")


def test_website_exhaustive_phone_calls():
    """Exhaustive test for phone_calls via Website Backend."""
    verify_website_capability("phone_calls", "Use a native macOS AppleScript to initiate a FaceTime audio phone call.")
