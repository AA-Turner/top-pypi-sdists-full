"""Live E2E for sage's Cloud Run AI models.

Hits each Cloud Run URL listed in model_servers/model_registry.json with
the exact payload sage's CloudRuntime builds. Confirms:

  - 200 (not 422 — that's the regression we just fixed)
  - Non-empty `choices[0].message.content`

Skipped by default — Cloud Run cold starts are 30-60s and we don't want
CI hitting paid GPUs every push. Opt in with::

    SAGE_E2E_CLOUD_LIVE=1 pytest sage/tests/test_e2e_cloud_models_live.py -v --no-cov

The user's 2026-05-16 report ("On the website I am receiving HTTP errors
for the cloud AI models 422") was specifically a CLI shadowing bug that
also crashed llama_cpp. This file is the durable proof that the cloud
models accept the canonical sage payload — if it ever regresses, this
test fails loudly on every opted-in run.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import httpx
import pytest


_REGISTRY = (
    Path(__file__).resolve().parent.parent.parent
    / "model_servers" / "model_registry.json"
)


def _live_models() -> list[tuple[str, str]]:
    """Return [(name, url)] for every model with a non-null URL."""
    if not _REGISTRY.exists():
        return []
    data = json.loads(_REGISTRY.read_text())
    return [
        (k, v) for k, v in data.items()
        if isinstance(v, str) and v.startswith("https://")
    ]


_LIVE = _live_models()


@pytest.mark.skipif(
    os.environ.get("SAGE_E2E_CLOUD_LIVE") != "1",
    reason="Set SAGE_E2E_CLOUD_LIVE=1 to hit live Cloud Run models.",
)
@pytest.mark.parametrize("model_name,url", _LIVE)
def test_cloud_model_accepts_canonical_payload(model_name: str, url: str) -> None:
    """Every live cloud model must accept sage's canonical request shape.

    Exact payload is what CloudRuntime._build_payload produces in
    backend/runtimes/cloud_runtime.py. If sage starts adding a new field,
    update this test and the runtime in the same change.
    """
    payload = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": "Reply with exactly the word: ok"}
        ],
        "temperature": 0.0,
        "max_tokens": 8,
        "stream": False,
    }
    # Cloud Run scale-to-zero means cold start can take 60-180s for the
    # larger models (Phi-4 14B, Yi 16K, vision encoders). On top of that,
    # running all 7 models in sequence can transiently exceed the project's
    # L4 GPU quota when several pods cold-start at once. Retry transient
    # 5xx + ReadTimeout with backoff before failing the test.
    timeout = httpx.Timeout(connect=10.0, read=360.0, write=10.0, pool=10.0)
    import time as _time
    response = None
    with httpx.Client(timeout=timeout) as client:
        for attempt in range(3):
            try:
                response = client.post(f"{url}/v1/chat/completions", json=payload)
            except httpx.ReadTimeout:
                _time.sleep(45 * (attempt + 1))
                continue
            if response.status_code < 500 or response.status_code == 422:
                break
            _time.sleep(45 * (attempt + 1))
    assert response is not None, f"{model_name}: all 3 attempts timed out"

    assert response.status_code != 422, (
        f"{model_name} returned 422 — the canonical sage payload is no "
        f"longer accepted by the deployed Cloud Run server. Body: "
        f"{response.text[:500]}"
    )
    response.raise_for_status()

    body = response.json()
    content = (body.get("choices") or [{}])[0].get("message", {}).get("content")
    assert isinstance(content, str) and content.strip(), (
        f"{model_name} returned an empty completion — model is reachable "
        f"but generation is failing. Body: {body}"
    )
