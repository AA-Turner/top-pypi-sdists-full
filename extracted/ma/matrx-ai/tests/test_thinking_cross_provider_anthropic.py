from matrx_ai.config import ThinkingContent, UnifiedMessage


def test_native_anthropic_thinking_preserved() -> None:
    block = ThinkingContent(
        text="plan the letter",
        provider="anthropic",
        signature="sig_abc",
    ).to_anthropic()
    assert block is not None
    assert block["type"] == "thinking"
    assert block["thinking"] == "plan the letter"
    assert block["signature"] == "sig_abc"


def test_openai_thinking_falls_back_to_text() -> None:
    block = ThinkingContent(
        text="reason about the stakes",
        provider="openai",
        signature="encrypted_blob",
    ).to_anthropic()
    assert block == {"type": "text", "text": "reason about the stakes"}


def test_openai_summary_only_falls_back_to_text() -> None:
    block = ThinkingContent(
        provider="openai",
        signature="encrypted_blob",
        summary=[{"type": "summary_text", "text": "summary line one"}],
    ).to_anthropic()
    assert block == {"type": "text", "text": "summary line one"}


def test_google_thinking_falls_back_to_text() -> None:
    block = ThinkingContent(
        text="gemini thought",
        provider="google",
        signature=b"bytes",
    ).to_anthropic()
    assert block == {"type": "text", "text": "gemini thought"}


def test_to_anthropic_blocks_includes_foreign_thinking() -> None:
    msg = UnifiedMessage(
        role="assistant",
        content=[
            ThinkingContent(
                text="foreign reasoning",
                provider="openai",
                signature="encrypted",
            )
        ],
    )
    blocks = msg.to_anthropic_blocks()
    assert blocks == [{"type": "text", "text": "foreign reasoning"}]
