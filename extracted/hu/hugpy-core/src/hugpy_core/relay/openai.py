# LIFTED from legacy hugpy (read-only reference):
#   _finish_reason <- py/services/hugpy_server/src/hugpy_server/app/routes/v1_routes.py:448 (verbatim)
#   _usage_block   <- py/services/hugpy_server/src/hugpy_server/app/routes/v1_helpers.py:380-400 (verbatim)
#   _openai_error  <- v1_routes.py:102 (without request diagnostics / structured causes)
#   completion_kwargs <- v1_helpers.py:_completion_kwargs 86 (messages, model, request_id,
#                       max_tokens, temperature, top_p, alloc; drops images/tools/chunks)
"""OpenAI chat.completions request/response shapes."""
from __future__ import annotations

import uuid

from flask import jsonify


def finish_reason(reason: str | None) -> str:
    return {"max_tokens": "length"}.get(reason or "stop", reason or "stop")


def usage_block(usage) -> dict:
    """Shape a DoneEvent usage dict into the OpenAI `usage` object.

    Real counts when the engine/runner reported them; the historical all-None
    shape when genuinely unavailable (old worker builds, error paths) — a
    missing count must never crash or omit the key, OpenAI SDKs expect it.
    """
    if not isinstance(usage, dict):
        usage = {}

    def _int(key):
        v = usage.get(key)
        return v if isinstance(v, int) else None

    prompt = _int("prompt_tokens")
    completion = _int("completion_tokens")
    total = _int("total_tokens")
    if total is None and prompt is not None and completion is not None:
        total = prompt + completion
    return {"prompt_tokens": prompt, "completion_tokens": completion,
            "total_tokens": total}


def openai_error(message: str, status: int, err_type: str = "invalid_request_error"):
    """The OpenAI-shaped error body."""
    return jsonify({"error": {"message": message, "type": err_type, "code": status}}), status


def completion_kwargs(payload: dict) -> dict:
    """Translate an OpenAI chat.completions payload into worker kwargs."""
    messages = payload.get("messages")
    if not messages:
        raise ValueError("'messages' is required")
    model = payload.get("model")
    if isinstance(model, str) and model.strip().lower() in ("", "default"):
        model = None
    kwargs = {
        "messages": messages,
        "model_key": model,
        "request_id": f"v1-{uuid.uuid4().hex}",
        "task": payload.get("task") or "chat",
    }
    max_tokens = payload.get("max_tokens") or payload.get("max_completion_tokens")
    if max_tokens:
        kwargs["max_new_tokens"] = int(max_tokens)
    if payload.get("temperature") is not None:
        kwargs["temperature"] = float(payload["temperature"])
    if payload.get("top_p") is not None:
        kwargs["top_p"] = float(payload["top_p"])
    if isinstance(payload.get("alloc"), dict) and payload["alloc"]:
        kwargs["alloc"] = payload["alloc"]
    # per-call pair knobs (operator 2026-10-06: a harness that can only name a model
    # still reaches every option the wrapper has — the wrapper's headless console
    # turns `model@options` into these). Layered OVER the pair's own knobs in
    # relay.worker_payload; never `blocked` (a block is the operator's, not a call's).
    if isinstance(payload.get("knobs"), dict) and payload["knobs"]:
        kwargs["knobs"] = {k: v for k, v in payload["knobs"].items() if k != "blocked"}
    from hugpy_core.brain.intent import stamp
    kwargs["metadata"] = stamp(payload.get("metadata"), payload.get("intent"))
    return kwargs
