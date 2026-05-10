"""Pre-warm Ollama models so the first prompt isn't penalized by load time.

Cold-loading a 30B model into RAM takes 5-10 seconds — every conversation
starts with that delay unless the model is already resident. Ollama
exposes a `keep_alive` parameter on every API call; setting it to a long
duration (or invoking the API once on session start) keeps the model hot.

Two helpers:
  - `prewarm(model)`         — fire-and-forget loader call
  - `keep_alive_kwargs(...)` — adds `keep_alive` to an Ollama API payload
"""

from __future__ import annotations

import json

__all__ = ["DEFAULT_KEEP_ALIVE", "keep_alive_kwargs", "prewarm"]


DEFAULT_KEEP_ALIVE = "30m"


def keep_alive_kwargs(payload: dict, *, duration: str = DEFAULT_KEEP_ALIVE) -> dict:
    """Return a shallow copy of `payload` with keep_alive injected."""
    out = dict(payload)
    out["keep_alive"] = duration
    return out


def prewarm(model: str, *, host: str = "http://127.0.0.1:11434",
            duration: str = DEFAULT_KEEP_ALIVE, timeout: float = 30.0) -> bool:
    """Force Ollama to load the model into RAM. Returns True on success.

    The trick: a chat completion with `messages: []` and a tiny
    `max_tokens` is enough to trigger the load without generating output.
    """
    try:
        import httpx
    except ImportError:
        return False
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": "ping"}],
        "stream": False,
        "options": {"num_predict": 1},
        "keep_alive": duration,
    }
    try:
        with httpx.Client(timeout=timeout) as client:
            r = client.post(f"{host}/api/chat", content=json.dumps(payload))
            return r.status_code == 200
    except Exception:
        return False
