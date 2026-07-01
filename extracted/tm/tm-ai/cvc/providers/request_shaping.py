"""Request-shaping helpers (upstream parity).

Combines:
  - 1.2 build_api_kwargs_extras hook    (per-model extras injection)
  - 1.7 codex_responses API mode        (GPT-5/Codex new shape)
  - 1.8 reasoning/thinking config       (effort levels, xhigh→high normalize)
  - 1.9 anthropic prompt caching        (System+3 cache_control strategy)
"""
from __future__ import annotations

from typing import Any, Optional

# ── 1.8 Reasoning ────────────────────────────────────────────────────

# Per-model reasoning catalog.  effort = minimal | low | medium | high
# (xhigh is normalized → high since most providers reject it)
REASONING_CATALOG: dict[str, dict[str, Any]] = {
    # OpenAI
    "gpt-5":          {"effort": "high",   "supported": True},
    "gpt-5-codex":    {"effort": "high",   "supported": True},
    "o1":             {"effort": "high",   "supported": True},
    "o1-mini":        {"effort": "medium", "supported": True},
    "o3":             {"effort": "high",   "supported": True},
    "o3-mini":        {"effort": "medium", "supported": True},
    # Anthropic — uses "thinking" not "reasoning"
    "claude-sonnet-4.6": {"thinking_budget": 16000, "supported": True},
    "claude-opus-4.6":   {"thinking_budget": 32000, "supported": True},
    "claude-sonnet-4-6": {"thinking_budget": 16000, "supported": True},
    "claude-opus-4-6":   {"thinking_budget": 32000, "supported": True},
    # Google
    "gemini-3-pro-preview":      {"effort": "high",   "supported": True},
    "gemini-3-flash-preview":    {"effort": "medium", "supported": True},
    "gemini-3.1-pro-preview":    {"effort": "high",   "supported": True},
    # Nvidia Nemotron (reasoning-tuned)
    "nvidia/nemotron-3-super-120b-instruct": {"effort": "high", "supported": True},
}

_VALID_EFFORTS = {"minimal", "low", "medium", "high"}


def normalize_effort(effort: str) -> str:
    """xhigh → high; clamp to valid set; default 'medium'."""
    if not effort:
        return "medium"
    e = effort.lower().strip()
    if e in ("xhigh", "extra-high", "extreme"):
        return "high"
    if e in _VALID_EFFORTS:
        return e
    return "medium"


def get_reasoning_config(model: str, override_effort: Optional[str] = None) -> Optional[dict[str, Any]]:
    """Look up reasoning config for a model. Returns None if unsupported."""
    cat = REASONING_CATALOG.get(model)
    if not cat or not cat.get("supported"):
        return None

    if "thinking_budget" in cat:
        return {"thinking_budget": cat["thinking_budget"]}

    effort = normalize_effort(override_effort or cat.get("effort", "medium"))
    return {"effort": effort}


# ── 1.9 Anthropic prompt caching (System+3) ──────────────────────────

def apply_anthropic_cache_control(messages: list[dict[str, Any]],
                                   system: Optional[str] = None) -> tuple[list[dict[str, Any]], Optional[Any]]:
    """Apply Anthropic's `cache_control: ephemeral` markers using System+3 strategy.

    Strategy (upstream parity):
      - System prompt: marked as cache breakpoint #1
      - Last 3 user/tool messages: each marked as cache breakpoint (max 4 total)

    Returns (mutated_messages, mutated_system_blocks).
    System is converted to block-form when caching is applied so cache_control
    can attach to it.
    """
    # Convert system → blocks if present
    sys_blocks: Optional[list[dict[str, Any]]] = None
    if system:
        sys_blocks = [{
            "type": "text",
            "text": system,
            "cache_control": {"type": "ephemeral"},
        }]

    # Find indices of last 3 user/tool messages
    target_indices: list[int] = []
    for i in range(len(messages) - 1, -1, -1):
        if messages[i].get("role") in ("user", "tool"):
            target_indices.append(i)
            if len(target_indices) >= 3:
                break

    out: list[dict[str, Any]] = []
    for idx, msg in enumerate(messages):
        msg = dict(msg)  # shallow copy
        if idx in target_indices:
            content = msg.get("content")
            if isinstance(content, str):
                msg["content"] = [{
                    "type": "text",
                    "text": content,
                    "cache_control": {"type": "ephemeral"},
                }]
            elif isinstance(content, list) and content:
                # Mark last block in the list
                new_content = list(content)
                last = dict(new_content[-1])
                last["cache_control"] = {"type": "ephemeral"}
                new_content[-1] = last
                msg["content"] = new_content
        out.append(msg)
    return out, sys_blocks


# ── 1.7 Codex Responses API mode ─────────────────────────────────────

def to_codex_responses_payload(model: str,
                                messages: list[dict[str, Any]],
                                tools: Optional[list[dict]] = None,
                                reasoning: Optional[dict] = None,
                                max_output_tokens: int = 4096) -> dict[str, Any]:
    """Convert chat-completions style → codex_responses /v1/responses payload shape.

    GPT-5/Codex use the new Responses API:
      {
        "model": "...",
        "input": [{"type":"message","role":"user","content":[{"type":"input_text","text":"..."}]}, ...],
        "tools": [...],
        "reasoning": {"effort": "high"},
        "max_output_tokens": 4096,
      }
    """
    input_items: list[dict[str, Any]] = []
    for m in messages:
        role = m.get("role", "user")
        content = m.get("content", "")
        if role == "system":
            # Responses API: system → instructions field handled separately; emit as input_text
            input_items.append({
                "type": "message",
                "role": "system",
                "content": [{"type": "input_text", "text": content if isinstance(content, str) else str(content)}],
            })
        elif role == "tool":
            input_items.append({
                "type": "function_call_output",
                "call_id": m.get("tool_call_id", ""),
                "output": content if isinstance(content, str) else str(content),
            })
        else:
            text = content if isinstance(content, str) else str(content)
            input_items.append({
                "type": "message",
                "role": role,
                "content": [{"type": "input_text" if role == "user" else "output_text", "text": text}],
            })

    payload: dict[str, Any] = {
        "model": model,
        "input": input_items,
        "max_output_tokens": max_output_tokens,
    }
    if tools:
        payload["tools"] = tools
    if reasoning:
        payload["reasoning"] = reasoning
    return payload


# ── 1.2 build_api_kwargs_extras hook ─────────────────────────────────

def build_api_kwargs_extras(provider: str,
                             model: str,
                             messages: list[dict[str, Any]],
                             base_kwargs: dict[str, Any],
                             *,
                             reasoning_effort: Optional[str] = None,
                             enable_cache: bool = True) -> dict[str, Any]:
    """Compute provider/model-specific extras (reasoning, cache, headers).

    Returns a dict of EXTRA kwargs to merge into the API call. Does not mutate base_kwargs.

    Result keys may include:
      - extra_body: dict (for OpenAI-compat reasoning injection)
      - extra_headers: dict
      - cache_messages: list[dict]   (rewritten messages with cache_control)
      - cache_system_blocks: list[dict]  (system as blocks)
      - thinking: dict (anthropic native)
    """
    extras: dict[str, Any] = {}
    provider = provider.lower()

    # ── Reasoning ──
    rc = get_reasoning_config(model, override_effort=reasoning_effort)
    if rc:
        if "thinking_budget" in rc:
            # Anthropic native shape
            if provider == "anthropic":
                extras["thinking"] = {
                    "type": "enabled",
                    "budget_tokens": rc["thinking_budget"],
                }
            # Anthropic-via-Copilot doesn't currently accept thinking — skip
        elif "effort" in rc:
            extras["extra_body"] = {"reasoning": {"effort": rc["effort"]}}

    # ── Anthropic prompt caching (System+3) ──
    if enable_cache and provider == "anthropic":
        sys_text = None
        # base_kwargs may have system as str
        if isinstance(base_kwargs.get("system"), str):
            sys_text = base_kwargs["system"]
        new_msgs, sys_blocks = apply_anthropic_cache_control(messages, system=sys_text)
        extras["cache_messages"] = new_msgs
        if sys_blocks:
            extras["cache_system_blocks"] = sys_blocks

    return extras


__all__ = [
    "REASONING_CATALOG",
    "normalize_effort",
    "get_reasoning_config",
    "apply_anthropic_cache_control",
    "to_codex_responses_payload",
    "build_api_kwargs_extras",
]
