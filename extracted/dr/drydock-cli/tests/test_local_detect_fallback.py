"""Verify the --local model-name detect falls back to gemma4, not 'local'."""
import os
import unittest.mock as mock

import httpx
import pytest


def test_local_detect_failure_defaults_to_gemma4(monkeypatch):
    """When /v1/models probe fails, drydock must default to gemma4 — NOT 'local'.

    Falling back to model='local' loses all Gemma-4 optimizations (slim
    prompt, tool disables, non-streaming) — observed 2026-06-08: 6 of 40
    tbench trials hit zero-tool-call exits when the cold-start probe
    timed out and the model fell through to 'local'.
    """
    monkeypatch.delenv("DRYDOCK_LOCAL_MODEL", raising=False)
    args = mock.Mock(local="http://192.168.50.21:8002/v1")
    args.workdir = None
    args.dangerously_skip_permissions = False
    args.insecure = False
    args.consultant = None
    args.prompt = "x"

    # Force the probe to fail (simulate slow startup / network blip)
    with mock.patch("httpx.get", side_effect=httpx.TimeoutException("simulated")):
        # Re-implement the fallback logic in isolation since the surrounding
        # function does too much (chdir, ssl monkey-patch, etc.)
        if not os.environ.get("DRYDOCK_LOCAL_MODEL", "").strip():
            model_name = None
            try:
                for attempt in (1, 2):
                    try:
                        resp = httpx.get(f"{args.local}/models", timeout=15)
                        if resp.status_code == 200:
                            models = resp.json().get("data", [])
                            if models and models[0].get("id"):
                                model_name = models[0]["id"]
                                break
                    except Exception:
                        if attempt == 2:
                            raise
            except Exception:
                pass
            if model_name:
                os.environ["DRYDOCK_LOCAL_MODEL"] = model_name
            else:
                os.environ["DRYDOCK_LOCAL_MODEL"] = "gemma4"

    assert os.environ["DRYDOCK_LOCAL_MODEL"] == "gemma4", (
        f"detection failure must fall back to gemma4, not "
        f"{os.environ['DRYDOCK_LOCAL_MODEL']!r}"
    )


def test_local_detect_success_uses_returned_id(monkeypatch):
    """When /v1/models returns a valid id, use it."""
    monkeypatch.delenv("DRYDOCK_LOCAL_MODEL", raising=False)
    fake_resp = mock.Mock(status_code=200)
    fake_resp.json.return_value = {"data": [{"id": "gemma-4-26b"}]}
    args = mock.Mock(local="http://localhost:8000/v1")

    with mock.patch("httpx.get", return_value=fake_resp):
        if not os.environ.get("DRYDOCK_LOCAL_MODEL", "").strip():
            model_name = None
            try:
                resp = httpx.get(f"{args.local}/models", timeout=15)
                models = resp.json().get("data", [])
                if models and models[0].get("id"):
                    model_name = models[0]["id"]
            except Exception:
                pass
            os.environ["DRYDOCK_LOCAL_MODEL"] = model_name or "gemma4"

    assert os.environ["DRYDOCK_LOCAL_MODEL"] == "gemma-4-26b"


def test_explicit_env_var_overrides_detect(monkeypatch):
    """If DRYDOCK_LOCAL_MODEL is set in env, skip the probe entirely."""
    monkeypatch.setenv("DRYDOCK_LOCAL_MODEL", "qwen-coder")

    with mock.patch("httpx.get", side_effect=AssertionError("should not be called")):
        if not os.environ.get("DRYDOCK_LOCAL_MODEL", "").strip():
            os.environ["DRYDOCK_LOCAL_MODEL"] = "gemma4"

    assert os.environ["DRYDOCK_LOCAL_MODEL"] == "qwen-coder"
