from matrx_ai.config import ThinkingContent, UnifiedMessage


def test_native_google_thinking_preserved() -> None:
    block = ThinkingContent(
        text="plan the letter",
        provider="google",
        signature=b"sig_bytes",
    ).to_google()
    assert block is not None
    assert block["text"] == "plan the letter"
    assert block["thought"] is True
    assert block["thoughtSignature"] == b"sig_bytes"


def test_openai_thinking_falls_back_to_text() -> None:
    block = ThinkingContent(
        text="reason about the stakes",
        provider="openai",
        signature="encrypted_blob",
    ).to_google()
    assert block == {"text": "reason about the stakes"}


def test_openai_summary_only_falls_back_to_text() -> None:
    block = ThinkingContent(
        provider="openai",
        signature="encrypted_blob",
        summary=[{"type": "summary_text", "text": "summary line one"}],
    ).to_google()
    assert block == {"text": "summary line one"}


def test_anthropic_thinking_falls_back_to_text() -> None:
    block = ThinkingContent(
        text="claude thought",
        provider="anthropic",
        signature="sig_abc",
    ).to_google()
    assert block == {"text": "claude thought"}


def test_to_google_content_includes_foreign_thinking() -> None:
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
    content = msg.to_google_content()
    assert content is not None
    assert content["parts"] == [{"text": "foreign reasoning"}]
