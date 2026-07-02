"""Model Matrix SMS Tests — every AI model tested via the SMS bridge webhook.

Each cloud model is given a simple prompt after a `@model <id>` switch,
and we validate a non-empty, non-error response. NO MOCKS.
"""

from __future__ import annotations

import os
import httpx
import pytest

BACKEND_URL = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TEST_EMAIL = "test-sms-model-matrix@sageworksai.com"
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


def _webhook(text: str) -> httpx.Response:
    payload = {
        "text": text,
        "from": TEST_EMAIL,
        "device_type": "apple",
    }
    return httpx.post(f"{BACKEND_URL}/sms/webhook", json=payload, timeout=TIMEOUT)


pytestmark = pytest.mark.skipif(
    not _is_backend_reachable(),
    reason=f"Backend not reachable at {BACKEND_URL}",
)


class TestModelMatrixSMS:
    @pytest.mark.parametrize("model_id", ALL_CLOUD_MODELS)
    def test_model_switch_and_math(self, model_id: str):
        """Switch to the model and ask a math question."""
        # 1. Switch model
        r_switch = _webhook(f"@model {model_id}")
        assert r_switch.status_code == 200
        output_switch = r_switch.json().get("output", r_switch.json().get("reply", ""))
        assert model_id in output_switch or "model" in output_switch.lower()

        # 2. Ask question
        r_ask = _webhook("@ask What is 9 multiplied by 6? Answer with just the number.")
        assert r_ask.status_code == 200
        output_ask = r_ask.json().get("output", r_ask.json().get("reply", ""))
        assert len(output_ask) > 0
        assert "54" in output_ask, f"{model_id} failed math check via SMS: {output_ask[:100]}"
