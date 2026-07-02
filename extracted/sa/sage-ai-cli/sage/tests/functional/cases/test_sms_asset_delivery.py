"""SMS Asset Delivery Tests

Verifies the rule: "coding files should keep the files on the local computer 
not the mobile app since logically coding files are useless on a mobile phone 
but any file asset like a document, video, image, audio file they should 
return the final outputted file to the mobile phone."
"""

from __future__ import annotations

import os
import json
import httpx
import pytest

BACKEND_URL = os.environ.get("SAGE_API_BASE", "http://127.0.0.1:8091")
TEST_EMAIL = "test-sms-assets@sageworksai.com"
TIMEOUT = 120
MODEL = "cloud:qwen3-coder"

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

class TestSMSAssetDelivery:
    
    def test_coding_task_returns_verification(self):
        """Coding tasks should leave files locally and return a verification message."""
        r = _webhook(f"@run Build a python script that prints hello world. --model {MODEL}")
        assert r.status_code == 200
        data = r.json()
        output = data.get("output", data.get("reply", ""))
        
        # Should not contain massive code blocks, but should contain verification
        assert len(output) < 500, "Output seems too long, might contain code instead of verification"
        assert "complete" in output.lower() or "saved" in output.lower() or "done" in output.lower()
        # Should not have attachments
        assert not data.get("attachments"), "Coding tasks should not return file attachments"

    def test_document_asset_returns_file(self):
        """Document tasks should return the file as an attachment to the mobile phone."""
        r = _webhook(f"@run Write a short poem about AI and save it as poem.txt. --model {MODEL}")
        assert r.status_code == 200
        data = r.json()
        
        # Check if the backend detected an asset and attached it
        # This depends on how the webhook formats responses with files.
        # Often it includes an 'attachments' list or an asset URL.
        attachments = data.get("attachments", [])
        has_asset_url = "http" in data.get("reply", "") and (".txt" in data.get("reply", ""))
        
        assert attachments or has_asset_url, "Document asset was not returned to the mobile phone"

    def test_image_asset_returns_file(self):
        """Image tasks should return the image as an attachment."""
        r = _webhook(f"@run Create a simple red square SVG and save it as square.svg. --model {MODEL}")
        assert r.status_code == 200
        data = r.json()
        
        attachments = data.get("attachments", [])
        has_asset_url = "http" in data.get("reply", "") and (".svg" in data.get("reply", ""))
        
        assert attachments or has_asset_url, "Image asset was not returned to the mobile phone"
