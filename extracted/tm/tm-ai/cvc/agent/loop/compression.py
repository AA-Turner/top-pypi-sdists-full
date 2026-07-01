"""Context window compression.

When prompt token count nears the model's context limit, this module
compresses old conversation turns by summarizing routine messages while
preserving structural elements (tool_call_id pairing, decisions, code).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


@dataclass
class CompressionConfig:
    target_ratio: float = 0.5          # compress to 50% of current size
    trigger_ratio: float = 0.85        # trigger when >= 85% of model limit
    keep_recent: int = 10              # always keep last N messages verbatim
    smart: bool = True                 # preserve decisions/code/architecture
    tool_result_max_chars: int = 2000  # truncate old tool results above this


# Hints used by smart mode to decide what NOT to summarize.
_PRESERVE_KEYWORDS = (
    "decision", "decided", "architecture", "design",
    "error", "fix", "bug", "TODO", "FIXME",
    "```", "def ", "class ", "function", "import ",
)


def _looks_important(text: str) -> bool:
    if not text:
        return False
    low = text.lower()
    return any(k.lower() in low for k in _PRESERVE_KEYWORDS)


@dataclass
class CompressionResult:
    messages: List[Dict[str, Any]]
    original_tokens: int
    compressed_tokens: int
    summary_text: str = ""
    skipped: bool = False
    reason: str = ""


SummarizeFn = Callable[[List[Dict[str, Any]]], str]


class ContextCompressor:
    def __init__(
        self,
        config: Optional[CompressionConfig] = None,
        summarize_fn: Optional[SummarizeFn] = None,
        token_counter: Optional[Callable[[str], int]] = None,
    ):
        self.config = config or CompressionConfig()
        self._summarize = summarize_fn
        self._count = token_counter or self._default_count

    @staticmethod
    def _default_count(text: str) -> int:
        # Cheap heuristic: ~4 chars/token.
        return max(1, len(text or "") // 4)

    def _msg_tokens(self, msg: Dict[str, Any]) -> int:
        content = msg.get("content")
        if isinstance(content, str):
            return self._count(content)
        if isinstance(content, list):
            total = 0
            for blk in content:
                if isinstance(blk, dict):
                    total += self._count(str(blk.get("text", ""))) or self._count(str(blk))
                else:
                    total += self._count(str(blk))
            return total
        return self._count(str(content or ""))

    def total_tokens(self, messages: List[Dict[str, Any]]) -> int:
        return sum(self._msg_tokens(m) for m in messages)

    def should_compress(self, prompt_tokens: int, model_context_limit: int) -> bool:
        if model_context_limit <= 0:
            return False
        return prompt_tokens >= int(self.config.trigger_ratio * model_context_limit)

    # ─────────────────────────────────────────────
    def compress(
        self,
        messages: List[Dict[str, Any]],
        *,
        system_prompt: Optional[str] = None,
    ) -> CompressionResult:
        original = self.total_tokens(messages)
        if len(messages) <= self.config.keep_recent + 2:
            return CompressionResult(
                messages=messages, original_tokens=original,
                compressed_tokens=original, skipped=True,
                reason="too few messages to compress",
            )

        keep_n = self.config.keep_recent
        recent = messages[-keep_n:]
        old = messages[:-keep_n]

        # Preserve important messages even from the "old" segment.
        preserved: List[Dict[str, Any]] = []
        summarizable: List[Dict[str, Any]] = []
        for m in old:
            content = m.get("content")
            text = content if isinstance(content, str) else str(content)
            if self.config.smart and _looks_important(text):
                preserved.append(m)
            else:
                summarizable.append(m)

        # Tool-call/result pairing: if we keep an assistant message with
        # tool_calls, we must keep matching tool results (and vice versa).
        preserved = self._repair_tool_pairing(preserved, summarizable)

        # Truncate old tool results in summarizable set.
        for m in summarizable:
            if m.get("role") == "tool":
                c = m.get("content")
                if isinstance(c, str) and len(c) > self.config.tool_result_max_chars:
                    m["content"] = c[: self.config.tool_result_max_chars] + f"\n[truncated {len(c) - self.config.tool_result_max_chars} chars]"

        # Build summary.
        summary_text = ""
        if summarizable:
            if self._summarize is not None:
                try:
                    summary_text = self._summarize(summarizable)
                except Exception as e:  # noqa: BLE001
                    summary_text = f"[summarization failed: {e}; {len(summarizable)} messages dropped]"
            else:
                summary_text = self._naive_summary(summarizable)

        new_messages: List[Dict[str, Any]] = []
        if summary_text:
            new_messages.append({
                "role": "system",
                "content": f"[COMPRESSED CONTEXT — {len(summarizable)} earlier messages]\n{summary_text}",
            })
        new_messages.extend(preserved)
        new_messages.extend(recent)

        compressed = self.total_tokens(new_messages)
        return CompressionResult(
            messages=new_messages,
            original_tokens=original,
            compressed_tokens=compressed,
            summary_text=summary_text,
        )

    # ─────────────────────────────────────────────
    @staticmethod
    def _naive_summary(messages: List[Dict[str, Any]]) -> str:
        roles = {}
        for m in messages:
            roles[m.get("role", "?")] = roles.get(m.get("role", "?"), 0) + 1
        parts = [f"{n} {r}" for r, n in roles.items()]
        return f"Earlier exchange compressed: {', '.join(parts)}."

    @staticmethod
    def _repair_tool_pairing(
        preserved: List[Dict[str, Any]],
        summarizable: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """If an assistant message in `preserved` has tool_calls, ensure the
        corresponding tool results are also preserved (move from summarizable).
        """
        needed_ids: set[str] = set()
        for m in preserved:
            for tc in m.get("tool_calls", []) or []:
                tid = tc.get("id") if isinstance(tc, dict) else None
                if tid:
                    needed_ids.add(tid)
        if not needed_ids:
            return preserved
        tail: List[Dict[str, Any]] = []
        keep_summarizable: List[Dict[str, Any]] = []
        for m in summarizable:
            if m.get("role") == "tool" and m.get("tool_call_id") in needed_ids:
                tail.append(m)
            else:
                keep_summarizable.append(m)
        # mutate the input list in place to drop moved items
        summarizable[:] = keep_summarizable
        return preserved + tail


__all__ = ["CompressionConfig", "CompressionResult", "ContextCompressor"]
