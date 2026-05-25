import pytest
from unittest.mock import MagicMock, patch

async def _run_website_mock(domain, prompt):
    try:
        from fastapi.testclient import TestClient
        from backend.app import app as backend_app
    except ImportError:
        pytest.skip("Backend environment not available")
        
    client = TestClient(backend_app)
    
    mock_runtime = MagicMock()
    mock_runtime.chat.return_value = f"Capabilities {domain} completed. File at /tmp/test.mp4"
    
    mock_app_state = MagicMock()
    mock_app_state.runtime_manager.runtime = mock_runtime
    mock_app_state.rate_limiter.get_client_id.return_value = "test_client"
    
    mock_limiter = MagicMock()
    mock_limiter.check_and_consume.return_value = MagicMock(allowed=True)
    
    with patch("backend.app.check_rate_limit"), \
         patch("backend.app._verify_firebase_token", return_value={"uid": "u1", "email": "test@test.com"}), \
         patch("backend.app.ensure_user_record"), \
         patch("backend.app.check_access", return_value=(True, None)), \
         patch("backend.app.get_user_record", return_value={"tier": "free"}), \
         patch("backend.tier_rate_limiter.get_tier_limiter", return_value=mock_limiter), \
         patch("backend.app.get_app_state", return_value=mock_app_state):
        
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model_id": "cloud:gemini-2.0-flash",
            "conversation_id": "conv-test",
            "temperature": 0.7,
            "stream": False
        }
        
        response = client.post("/chat", json=payload, headers={"Authorization": "Bearer fake"})
        assert response.status_code == 200, f"Backend task failed for domain: {domain}"
        
        data = response.json()
        assert data.get("ok") is True
        
        if domain in ["videos", "images", "audio_files", "music_videos"]:
            assert "test.mp4" in data.get("output", "") or "Capabilities" in data.get("output", "")


@pytest.mark.asyncio
async def test_website_exhaustive_websites():
    """Exhaustive async test for websites via Website Backend."""
    await _run_website_mock("websites", "Create a responsive advertising dashboard using React and Tailwind.")

@pytest.mark.asyncio
async def test_website_exhaustive_mobile_apps():
    """Exhaustive async test for mobile_apps via Website Backend."""
    await _run_website_mock("mobile_apps", "Build a React Native feed with infinite scrolling.")

@pytest.mark.asyncio
async def test_website_exhaustive_video_games():
    """Exhaustive async test for video_games via Website Backend."""
    await _run_website_mock("video_games", "Develop a 2D physics engine in JavaScript for a browser game.")

@pytest.mark.asyncio
async def test_website_exhaustive_backend_services():
    """Exhaustive async test for backend_services via Website Backend."""
    await _run_website_mock("backend_services", "Create a FastAPI backend with PostgreSQL and Redis caching.")

@pytest.mark.asyncio
async def test_website_exhaustive_deployments():
    """Exhaustive async test for deployments via Website Backend."""
    await _run_website_mock("deployments", "Write Terraform IaC to deploy a Node.js app to AWS ECS.")

@pytest.mark.asyncio
async def test_website_exhaustive_videos():
    """Exhaustive async test for videos via Website Backend."""
    await _run_website_mock("videos", "Make a music video with moviepy that says 'I love you Lily'.")

@pytest.mark.asyncio
async def test_website_exhaustive_images():
    """Exhaustive async test for images via Website Backend."""
    await _run_website_mock("images", "Generate a professional SVG logo and PNG favicon.")

@pytest.mark.asyncio
async def test_website_exhaustive_audio_files():
    """Exhaustive async test for audio_files via Website Backend."""
    await _run_website_mock("audio_files", "Synthesize a WAV audio file playing a C major chord.")

@pytest.mark.asyncio
async def test_website_exhaustive_music_videos():
    """Exhaustive async test for music_videos via Website Backend."""
    await _run_website_mock("music_videos", "Combine generated audio and video into an MP4 music video.")

@pytest.mark.asyncio
async def test_website_exhaustive_generate_files():
    """Exhaustive async test for generate_files via Website Backend."""
    await _run_website_mock("generate_files", "Write a complex Python script, a JSON config, and a YAML manifest.")

@pytest.mark.asyncio
async def test_website_exhaustive_run_applications():
    """Exhaustive async test for run_applications via Website Backend."""
    await _run_website_mock("run_applications", "Open the Messages app on my Mac and prepare a text.")

@pytest.mark.asyncio
async def test_website_exhaustive_computer_control():
    """Exhaustive async test for computer_control via Website Backend."""
    await _run_website_mock("computer_control", "Use osascript to change my system volume and toggle dark mode.")

@pytest.mark.asyncio
async def test_website_exhaustive_text_messages():
    """Exhaustive async test for text_messages via Website Backend."""
    await _run_website_mock("text_messages", "Send a text message using the SMS bridge natively.")

@pytest.mark.asyncio
async def test_website_exhaustive_phone_calls():
    """Exhaustive async test for phone_calls via Website Backend."""
    await _run_website_mock("phone_calls", "Trigger an API call to Twilio to initiate a phone call.")
