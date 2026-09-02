"""
Claude API client using the official Anthropic SDK.
"""

import logging
import os
from typing import Any, Dict, List, Optional

from anthropic import AsyncAnthropic

logger = logging.getLogger(__name__)

DEFAULT_MODEL = "claude-sonnet-4-6"
DEFAULT_MAX_TOKENS = 4096


class ClaudeAPI:
    """Thin wrapper around AsyncAnthropic for InnoDay AI features."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        max_tokens: int = DEFAULT_MAX_TOKENS,
        temperature: float = 0.7,
        organization_alias: Optional[str] = None,
    ):
        resolved_key = api_key or os.getenv("CLAUDE_API_KEY")
        if not resolved_key:
            raise ValueError(
                "Claude API key is required. Set CLAUDE_API_KEY in your environment."
            )

        self._client = AsyncAnthropic(api_key=resolved_key)
        self.model = model
        self.max_tokens = max_tokens
        self.temperature = temperature

    def is_configured(self) -> bool:
        return self._client is not None

    async def _complete(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Core completion — single user turn, returns text."""
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "messages": [{"role": "user", "content": prompt}],
        }
        if system:
            kwargs["system"] = system
        response = await self._client.messages.create(**kwargs)
        return response.content[0].text

    # ------------------------------------------------------------------
    # Public methods used by callers
    # ------------------------------------------------------------------

    async def generate_response(
        self,
        prompt: str,
        system: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Generate a response to a single prompt."""
        return await self._complete(prompt, system=system, max_tokens=max_tokens)

    async def generate_completion(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
    ) -> str:
        """Generate a completion (alias for generate_response with system_prompt kwarg)."""
        return await self._complete(prompt, system=system_prompt, max_tokens=max_tokens)

    async def summarize_text(
        self,
        text: str,
        max_length: Optional[int] = None,
        system: Optional[str] = None,
    ) -> str:
        """Summarize a block of text."""
        length_hint = (
            f" Keep the summary under {max_length} characters." if max_length else ""
        )
        prompt = f"Summarize the following text concisely.{length_hint}\n\n{text}"
        return await self._complete(prompt, system=system)

    async def summarize_conversation(
        self,
        messages: List[Dict[str, Any]],
        max_length: Optional[int] = None,
        include_action_items: bool = True,
        template: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Summarize a list of conversation messages.

        Returns a dict with keys: summary, key_points, action_items, unresolved_items.
        """
        formatted = "\n".join(
            (
                f"[{m.get('role', 'user').upper()}] {m.get('content', m)}"
                if isinstance(m, dict)
                else str(m)
            )
            for m in messages
        )

        length_hint = (
            f" Keep the summary under {max_length} characters." if max_length else ""
        )
        action_hint = " Include a list of action items." if include_action_items else ""
        base_instructions = template or prompt or "Summarize the key points."

        system = (
            "You are summarizing a conversation. Return a JSON object with keys: "
            "summary (string), key_points (list), action_items (list), unresolved_items (list)."
        )
        user_prompt = f"{base_instructions}{length_hint}{action_hint}\n\nConversation:\n{formatted}"

        raw = await self._complete(user_prompt, system=system)

        import json

        try:
            # Strip markdown fences if present
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            return json.loads(text)
        except (json.JSONDecodeError, IndexError):
            return {
                "summary": raw,
                "key_points": [],
                "action_items": [],
                "unresolved_items": [],
            }

    async def chat(
        self,
        messages: List[Dict[str, Any]],
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        system: Optional[str] = None,
    ) -> str:
        """Multi-turn chat with a list of {role, content} messages."""
        kwargs: Dict[str, Any] = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "messages": messages,
        }
        if system:
            kwargs["system"] = system
        response = await self._client.messages.create(**kwargs)
        return response.content[0].text
