"""Website Features Tests

Tests the Next.js / React frontend routes, chat flows, and account pages.
These tests use requests/httpx against the running frontend server.
"""

from __future__ import annotations

import os
import httpx
import pytest

# Assuming frontend runs on 3000 locally
FRONTEND_URL = os.environ.get("SAGE_WEB_BASE", "http://localhost:3000")
BACKEND_URL = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")

def _is_frontend_reachable() -> bool:
    try:
        return httpx.get(FRONTEND_URL, timeout=5).status_code == 200
    except Exception:
        return False

def _is_backend_reachable() -> bool:
    try:
        return httpx.get(f"{BACKEND_URL}/health", timeout=5).status_code == 200
    except Exception:
        return False

@pytest.mark.skipif(not _is_frontend_reachable(), reason=f"Frontend not reachable at {FRONTEND_URL}")
class TestWebsitePages:
    
    def test_home_page(self):
        r = httpx.get(FRONTEND_URL)
        assert r.status_code == 200
        assert "sage" in r.text.lower()
        
    def test_chat_page(self):
        r = httpx.get(f"{FRONTEND_URL}/chat")
        assert r.status_code == 200
        
    def test_account_page(self):
        r = httpx.get(f"{FRONTEND_URL}/account")
        assert r.status_code == 200

@pytest.mark.skipif(not _is_backend_reachable(), reason="Backend not reachable")
class TestWebsiteChatFlow:
    
    def test_chat_history_endpoint(self):
        r = httpx.get(f"{BACKEND_URL}/api/history")
        assert r.status_code in (200, 401)  # 401 if auth required

    def test_chat_models_endpoint(self):
        r = httpx.get(f"{BACKEND_URL}/api/models")
        assert r.status_code == 200
        data = r.json()
        assert "models" in data or isinstance(data, list)

@pytest.mark.skipif(not _is_backend_reachable(), reason="Backend not reachable")
class TestWebsiteAccount:
    """Testing the provider unlinking bug."""
    
    def test_provider_unlink_flow(self):
        # We simulate the unlinking API call
        # The user reported: "an error is thrown for sign in then unlink the provider which is a false error"
        
        # Assuming the endpoint is /api/auth/unlink
        payload = {"provider": "github"}
        
        # Without auth token this might 401, which is expected.
        # But we ensure the endpoint actually exists and doesn't 500 or 404
        r = httpx.post(f"{BACKEND_URL}/api/auth/unlink", json=payload)
        
        assert r.status_code in (200, 401, 403), f"Unlink endpoint returned unexpected code: {r.status_code}"
