import pytest
from unittest.mock import MagicMock, patch

# Import mocks from other exhaustive tests to keep it DRY
from sage.tests.exhaustive_tasks.test_frontend_web_frameworks import FRONTEND_MOCKS
from sage.tests.exhaustive_tasks.test_backend_web_frameworks import BACKEND_MOCKS
from sage.tests.exhaustive_tasks.test_mobile_app_frameworks import MOBILE_MOCKS
from sage.tests.exhaustive_tasks.test_video_game_platforms import GAME_MOCKS
from sage.tests.exhaustive_tasks.test_programming_languages_core import CORE_MOCKS
from sage.tests.exhaustive_tasks.test_asset_creation_and_media import ASSET_MOCKS

# Construct the tasks list programmatically
ALL_TASKS = []

for key, val in FRONTEND_MOCKS.items():
    ALL_TASKS.append((
        "frontend",
        key,
        f"Implement a complete {key} application with state management and layouts.",
        val
    ))

for key, val in BACKEND_MOCKS.items():
    ALL_TASKS.append((
        "backend",
        key,
        f"Implement a complete {key} backend service with routing and DB persistence.",
        val
    ))

for key, val in MOBILE_MOCKS.items():
    ALL_TASKS.append((
        "mobile",
        key,
        f"Implement a complete {key} mobile component with lists and navigation.",
        val
    ))

for key, val in GAME_MOCKS.items():
    ALL_TASKS.append((
        "game",
        key,
        f"Implement a complete {key} video game player movement script.",
        val
    ))

for key, val in CORE_MOCKS.items():
    ALL_TASKS.append((
        "core_lang",
        key,
        f"Implement a complete, production-ready {key} module for concurrency or data management.",
        val
    ))

for key, val in ASSET_MOCKS.items():
    ALL_TASKS.append((
        "asset",
        key,
        f"Create a complete asset file for {key} extension.",
        val
    ))

@pytest.mark.asyncio
@pytest.mark.parametrize("category,key,prompt,mock_output", ALL_TASKS)
async def test_website_exhaustive_task(category, key, prompt, mock_output):
    """Verify that the Website chat API handles the task correctly and returns exact output."""
    try:
        from fastapi.testclient import TestClient
        from backend.app import app as backend_app
    except ImportError:
        pytest.skip("Backend environment not available")
        
    client = TestClient(backend_app)
    
    mock_runtime = MagicMock()
    mock_runtime.chat.return_value = mock_output
    
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
        assert response.status_code == 200, f"Backend chat request failed for category: {category}, key: {key}"
        
        data = response.json()
        assert data.get("ok") is True
        assert data.get("output", "") == mock_output
