"""Model Matrix Web Tests — every AI model tested via the web `/api/chat` endpoint.

Each cloud model is given a prompt via the REST API used by the React frontend,
and we validate the streaming response. NO MOCKS.
"""

from __future__ import annotations

import os
import json
import httpx
import pytest

BACKEND_URL = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TIMEOUT = 120

ALL_CLOUD_MODELS = [
    "cloud:qwen3-coder",
    "cloud:llama-3-2",
    "cloud:deepseek-r1-7b",
    "cloud:gemma-4",
    "cloud:phi-4-reasoning",
    "cloud:mistral-small",
    "cloud:yi-coder-9b",
    "cloud:llava-llama-3",
]


def _is_backend_reachable() -> bool:
    try:
        return httpx.get(f"{BACKEND_URL}/health", timeout=5).status_code == 200
    except Exception:
        return False


pytestmark = pytest.mark.skipif(
    not _is_backend_reachable(),
    reason=f"Backend not reachable at {BACKEND_URL}",
)


class TestModelMatrixWeb:
    @pytest.mark.parametrize("model_id", ALL_CLOUD_MODELS)
    def test_chat_endpoint(self, model_id: str):
        """Test the /api/chat streaming endpoint for each model."""
        payload = {
            "model_id": model_id,
            "messages": [{"role": "user", "content": "What is 8 multiplied by 7? Answer with just the number."}],
            "temperature": 0.1,
            "max_tokens": 100,
        }
        
        # The frontend uses Server-Sent Events (SSE) or streaming chunks
        with httpx.Client(timeout=TIMEOUT) as client:
            with client.stream("POST", f"{BACKEND_URL}/api/chat", json=payload) as r:
                assert r.status_code == 200
                full_content = ""
                for chunk in r.iter_text():
                    # Parse SSE lines if it's SSE, otherwise just append
                    if chunk.startswith("data: "):
                        try:
                            data = json.loads(chunk[6:])
                            if "choices" in data and len(data["choices"]) > 0:
                                delta = data["choices"][0].get("delta", {})
                                full_content += delta.get("content", "")
                        except Exception:
                            full_content += chunk
                    else:
                        full_content += chunk
                        
                assert len(full_content) > 0, f"{model_id} returned empty stream"
                assert "56" in full_content, f"{model_id} failed math check via Web API: {full_content[:100]}"
