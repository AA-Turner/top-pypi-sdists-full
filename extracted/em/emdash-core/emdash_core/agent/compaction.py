"""Context compaction for managing LLM context size.

Provides utilities for compressing large payloads to fit within
token limits while preserving essential information.
"""

from typing import Any, Optional


class LLMCompactor:
    """Compacts payloads to fit within LLM context limits.

    Uses LLM-based summarization to compress large sections of context
    while preserving the most important information.

    Example:
        compactor = LLMCompactor(provider)

        payload = {
            "evidence": "Very long evidence text...",
            "claims": "Long claims list...",
        }

        compacted = compactor.compact_payload(payload, goal="Find auth bugs")
    """

    def __init__(
        self,
        provider: Any,
        max_section_tokens: int = 4000,
        max_total_tokens: int = 16000,
    ):
        """Initialize the compactor.

        Args:
            provider: LLM provider for summarization
            max_section_tokens: Max tokens per section
            max_total_tokens: Max total tokens for payload
        """
        self.provider = provider
        self.max_section_tokens = max_section_tokens
        self.max_total_tokens = max_total_tokens

    def compact_payload(
        self,
        payload: dict[str, str],
        goal: str,
    ) -> dict[str, str]:
        """Compact a payload to fit within token limits.

        Args:
            payload: Dict of section name to content
            goal: Research goal for context

        Returns:
            Dict with compacted sections
        """
        # Estimate tokens (rough: 4 chars per token)
        total_chars = sum(len(v) for v in payload.values())
        estimated_tokens = total_chars // 4

        if estimated_tokens <= self.max_total_tokens:
            return payload

        # Need to compact - prioritize sections
        compacted = {}
        remaining_budget = self.max_total_tokens

        # Priority order for sections
        priority = ["claims", "evidence", "questions", "gaps", "entities", "prior_claims"]

        for key in priority:
            if key not in payload:
                continue

            content = payload[key]
            section_tokens = len(content) // 4

            if section_tokens > self.max_section_tokens:
                # Summarize this section
                compacted[key] = self._summarize_section(key, content, goal)
            else:
                compacted[key] = content

            remaining_budget -= len(compacted[key]) // 4

            if remaining_budget <= 0:
                break

        # Copy any remaining sections that fit
        for key, value in payload.items():
            if key not in compacted:
                if len(value) // 4 <= remaining_budget:
                    compacted[key] = value
                    remaining_budget -= len(value) // 4

        return compacted

    def _summarize_section(
        self,
        section_name: str,
        content: str,
        goal: str,
    ) -> str:
        """Summarize a section using the LLM.

        Args:
            section_name: Name of the section
            content: Content to summarize
            goal: Research goal for context

        Returns:
            Summarized content
        """
        try:
            prompt = f"""Summarize this {section_name} section concisely.
Keep the most important information relevant to the goal: {goal}

Content:
{content[:8000]}  # Limit input

Provide a concise summary that preserves key facts and references."""

            messages = [{"role": "user", "content": prompt}]
            response = self.provider.chat(messages)

            return response.content or content[:2000]

        except Exception:
            # Fallback: truncate
            return content[: self.max_section_tokens * 4]

    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text.

        Args:
            text: Text to estimate

        Returns:
            Estimated token count
        """
        # Rough estimate: 4 chars per token on average
        return len(text) // 4
