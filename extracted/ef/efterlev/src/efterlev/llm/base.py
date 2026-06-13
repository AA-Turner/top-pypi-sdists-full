"""LLM client protocol + a stub for tests.

`LLMClient` is the minimal call shape every Efterlev agent needs. The
Anthropic v0 implementation lives in `anthropic_client.py`; the Bedrock
v1 implementation will land alongside it behind the same protocol.

`StubLLMClient` is the fixture every agent test uses — it returns canned
responses without hitting the network and records the last prompt so
tests can assert on prompt shape (XML fencing, etc.).
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class LLMMessage:
    """One user-role message to an LLM. Role is implicit at v0: always 'user'."""

    content: str


@dataclass(frozen=True)
class LLMResponse:
    """LLM output paired with the metadata agents need for provenance.

    `model` is the exact model identifier the backend served (not the
    requested alias), so provenance records can pin the responding model.
    `prompt_hash` is the sha256 of `system + messages` as sent; agents
    compute it at call time and pass it through so it's consistent across
    backends.

    `input_tokens` and `output_tokens` (v0.1.9): pulled from the SDK
    response's usage block (Anthropic SDK + Bedrock both return them).
    Persisted on each Claim record so post-hoc cost auditing works
    locally without consulting CloudWatch / Anthropic billing dashboard.
    Defaults to 0 (test stubs / older clients that don't surface usage)
    rather than None to keep arithmetic on aggregates trivial.
    """

    text: str
    model: str
    prompt_hash: str
    input_tokens: int = 0
    output_tokens: int = 0


@runtime_checkable
class LLMClient(Protocol):
    """Call shape every Efterlev agent uses.

    Note on `temperature`: we intentionally do not accept one. Claude Opus 4.7
    and other modern reasoning-trained models reject the parameter outright
    (the API returns 400 "temperature is deprecated for this model"). Our
    agents already parse + validate JSON output strictly via pydantic, so the
    determinism we cared about with temperature=0 is enforced downstream
    anyway.

    `on_chunk`: optional callback invoked per text-delta as the LLM streams.
    Receives the cumulative text-so-far. Used by long-running agents (Gap)
    to surface progress to the user during the ~60-90s wait. Backends that
    don't stream (Bedrock Converse) call `on_chunk` once with the final
    text — the callback shape stays uniform; the granularity differs.
    Added v0.1.86.
    """

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        """Run a single completion. Returns (text, model, prompt_hash)."""
        ...


@dataclass
class StubLLMClient:
    """Test fixture: returns a preset response and records the last call.

    Agents tests inject an instance instead of reaching to the network.
    Set `response_text` before calling; inspect `last_system` / `last_messages`
    after to assert on prompt shape (e.g. that evidence was XML-fenced).
    """

    response_text: str = "{}"
    # Optional per-call response sequence (v0.1.226): when non-empty, call N
    # returns response_texts[N] (clamped to the last entry once exhausted).
    # Lets retry-path tests serve a bad response first and a good one second.
    # `response_text` remains the single-response fast path when unset.
    response_texts: list[str] = field(default_factory=list)
    model: str = "stub-model"
    last_system: str = ""
    last_messages: list[LLMMessage] = field(default_factory=list)
    last_prompt_hash: str = ""
    last_max_tokens: int = 0
    call_count: int = 0

    def complete(
        self,
        *,
        system: str,
        messages: list[LLMMessage],
        model: str,
        max_tokens: int = 4096,
        on_chunk: Callable[[str], None] | None = None,
    ) -> LLMResponse:
        import hashlib

        # v0.1.86: emit the canned response in 8 ~equal chunks so tests can
        # exercise the streaming-progress code path against a stub. Real
        # backends emit far more chunks; the test surface only needs to
        # confirm the callback fires with cumulative-text-so-far semantics.
        if on_chunk is not None and self.response_text:
            chunk_size = max(1, len(self.response_text) // 8)
            cumulative = ""
            for i in range(0, len(self.response_text), chunk_size):
                cumulative += self.response_text[i : i + chunk_size]
                on_chunk(cumulative)

        self.last_system = system
        self.last_messages = list(messages)
        self.last_max_tokens = max_tokens
        text = self.response_text
        if self.response_texts:
            text = self.response_texts[min(self.call_count, len(self.response_texts) - 1)]
        self.call_count += 1
        joined = system + "\n".join(m.content for m in messages)
        prompt_hash = hashlib.sha256(joined.encode("utf-8")).hexdigest()
        self.last_prompt_hash = prompt_hash
        return LLMResponse(text=text, model=self.model, prompt_hash=prompt_hash)
