"""The grounding judge talks to the ``llm_provider`` seam — never a provider SDK.

grounding.py used to hold a raw ``AsyncAnthropic`` client and hand-manage
sampling policy (it ended up omitting ``temperature`` for EVERY model, losing
determinism, plus a dead capability probe). It now goes through the injected
seam, which inverts the old contract:

  - the judge ASKS for ``temperature=0`` (determinism is what a fact-checker
    wants), and
  - the PROVIDER drops it on routes that reject it (the adaptive Anthropic
    models 400 on any sampling param).

So the invariant under test is no longer "never send temperature" — it is
"always go through the seam, and never branch on a model name here".

The other thing worth protecting: per-claim progress is REAL. Verdicts are
parsed out of the streaming JSON array as each object's tokens complete, not
faked in a burst after the call.
"""

from __future__ import annotations

from typing import Any

import matrx_rag.grounding as grounding
import pytest

_JUDGE_JSON = (
    '[{"claim_index": 1, "verdict": "supported", "confidence": 0.9, '
    '"supporting_chunk_ids": ["c1"], "reasoning": "ok"}]'
)


class _ChatOnlyProvider:
    """A provider implementing ONLY chat() — e.g. a custom matrx-local adapter.
    Exercises the degrade path."""

    def __init__(self, *, stream_in_pieces: list[str] | None = None) -> None:
        self.calls: list[dict[str, Any]] = []
        self._pieces = stream_in_pieces

    async def chat(self, messages, **kwargs: Any) -> str:
        self.calls.append({"method": "chat", "messages": messages, **kwargs})
        if kwargs.get("purpose") == "grounding_judge":
            return _JUDGE_JSON
        return '["claim one", "claim two"]'


class _FakeProvider(_ChatOnlyProvider):
    """Stands in for an injected streaming LLMProvider. Records every call."""

    async def chat_stream(self, messages, *, on_delta, **kwargs: Any) -> str:
        self.calls.append(
            {"method": "chat_stream", "messages": messages, "on_delta": on_delta, **kwargs}
        )
        pieces = self._pieces or [_JUDGE_JSON]
        for piece in pieces:
            await on_delta(piece)
        return "".join(pieces)


@pytest.fixture
def provider(monkeypatch):
    p = _FakeProvider()
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)
    return p


async def test_extract_claims_goes_through_the_seam(provider):
    claims = await grounding.extract_claims("The sky is blue. Water is wet.")

    assert claims == ["claim one", "claim two"]
    call = provider.calls[0]
    assert call["method"] == "chat"
    assert call["purpose"] == "grounding_claim_extract"
    # The package sends no instructions (wave 17): the host provider owns them per purpose.
    assert [m["role"] for m in call["messages"]] == ["user"]


async def test_judge_streams_and_asks_for_determinism(provider):
    verdicts = await grounding.judge_claims(
        ["The sky is blue."],
        [{"chunk_id": "c1", "content_text": "The sky is blue on clear days."}],
    )

    assert len(verdicts) == 1
    assert verdicts[0].verdict == "supported"
    call = provider.calls[0]
    assert call["method"] == "chat_stream"  # streaming path, not a batch call
    assert call["purpose"] == "grounding_judge"
    # We DO ask for temperature=0 now; dropping it is the provider's job.
    assert call["temperature"] == 0


async def test_on_verdict_fires_as_tokens_arrive_not_after(monkeypatch):
    """Real incremental progress: the verdict lands while the stream is still
    open, and is NOT emitted a second time when the call returns."""
    # Split the JSON so the object only completes on the 2nd-to-last piece.
    head, tail = _JUDGE_JSON[:40], _JUDGE_JSON[40:]
    p = _FakeProvider(stream_in_pieces=[head, tail, "   "])
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)

    fired: list[tuple[int, str]] = []

    async def _on_verdict(idx, verdict):
        fired.append((idx, verdict.verdict))

    verdicts = await grounding.judge_claims(
        ["The sky is blue."],
        [{"chunk_id": "c1", "content_text": "The sky is blue on clear days."}],
        on_verdict=_on_verdict,
    )

    assert fired == [(0, "supported")]  # fired exactly once, mid-stream
    assert verdicts[0].verdict == "supported"  # authoritative result unchanged


async def test_degrades_to_chat_when_provider_cannot_stream(monkeypatch):
    """A provider implementing only chat() still produces verdicts (progress
    just arrives in one batch) — it must never crash or silently drop them."""
    p = _ChatOnlyProvider()
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)
    assert not hasattr(p, "chat_stream")

    fired: list[int] = []

    async def _on_verdict(idx, verdict):
        fired.append(idx)

    verdicts = await grounding.judge_claims(
        ["The sky is blue."],
        [{"chunk_id": "c1", "content_text": "The sky is blue on clear days."}],
        on_verdict=_on_verdict,
    )

    assert p.calls[0]["method"] == "chat"
    assert fired == [0]
    assert verdicts[0].verdict == "supported"


async def test_a_judge_that_never_ran_is_not_reported_as_a_hallucination(monkeypatch):
    """THE dangerous failure: a misconfigured provider makes every claim score
    `unsupported` / 0.0 faithfulness, which reads as "the model hallucinated".
    "We could not check" and "the answer is wrong" are different facts."""

    class _BrokenProvider:
        async def chat(self, messages, **kwargs):
            if kwargs.get("purpose") == "grounding_judge":
                raise RuntimeError("matrx-rag's DEFAULT LLM provider is OpenAI-only")
            return '["the sky is blue"]'

    monkeypatch.setattr(grounding, "get_llm_provider", lambda: _BrokenProvider())

    report = await grounding.verify_grounded(
        answer="The sky is blue.",
        retrieved=[{"chunk_id": "c1", "content_text": "The sky is blue."}],
    )

    # The report says WHY it is empty, instead of silently blaming the answer.
    assert report.error is not None
    assert "OpenAI-only" in report.error
    assert all("NOT VERIFIED" in c.reasoning for c in report.claims)


async def test_judge_survives_a_malformed_claim_index(monkeypatch):
    """The delta callback runs inside the provider's streaming loop, so an
    exception escaping it aborts the already-PAID judge call. A model emitting
    `"claim_index": null` must not cost us the whole verification."""
    bad = '[{"claim_index": null, "verdict": "supported", "confidence": 0.9}]'
    p = _FakeProvider(stream_in_pieces=[bad])
    monkeypatch.setattr(grounding, "get_llm_provider", lambda: p)

    async def _on_verdict(idx, verdict):  # pragma: no cover
        raise AssertionError("should not fire for a malformed index")

    # Must not raise — the call completes and the final parse still runs.
    verdicts = await grounding.judge_claims(
        ["The sky is blue."],
        [{"chunk_id": "c1", "content_text": "The sky is blue."}],
        on_verdict=_on_verdict,
    )
    assert len(verdicts) == 1


def test_no_provider_sdk_is_imported_by_grounding():
    """The whole point: matrx-rag stays provider-agnostic. Checked against the
    AST (real import statements), not the source text — prose mentioning a
    vendor is fine; importing one is not."""
    import ast
    from matrx_utils.source_guard import stable_source

    tree = ast.parse(stable_source(grounding))
    imported: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imported.update(a.name.split(".")[0] for a in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imported.add(node.module.split(".")[0])

    for sdk in ("anthropic", "openai", "google", "groq", "cohere"):
        assert sdk not in imported, f"grounding.py must not import the {sdk} SDK — use the seam"

    # And the raw-client helpers are gone for good.
    assert not hasattr(grounding, "_client")
    assert not hasattr(grounding, "_sampling_kwargs")
