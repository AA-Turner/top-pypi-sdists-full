"""A speech take that is far too small for its text is a truncated response, never a take.

2026-10-19: ``gpt-4o-mini-tts`` answered HTTP 200 for a 556-character script after the call had sat open for
~300 s, and the body held only its first chunk: 2,688 bytes (0.168 s of mp3). The adapter treated any
non-empty body as the finished take, billed all 556 characters, stored the file and called it made. The
same request sent again produced 36 s / 581 KB. The input, voice, format and absent ``instructions`` were all
correct on the wire; only the delivery was cut short.

The floor below is deliberately far under every real encoding (speech runs ~15 characters a second; the
thinnest OpenAI format, opus, is still hundreds of bytes a second), so only a response that cannot hold the
text trips it. Pure; no I/O.
"""

from __future__ import annotations

#: Real takes measure 700-1,100 bytes per character (mp3). Even 6 kbps opus at 15 chars/s is 50. This is the floor.
MIN_BYTES_PER_CHARACTER = 20


class TruncatedSpeechError(RuntimeError):
    """The provider answered, was billed for the whole text, and returned far too little audio."""


def truncated_take_reason(audio_size_bytes: int, characters: int) -> str | None:
    """Why ``audio_size_bytes`` cannot be the whole take for ``characters`` of text, or ``None`` when it can."""
    floor = max(1, characters) * MIN_BYTES_PER_CHARACTER
    if audio_size_bytes >= floor:
        return None
    return (
        f"the audio is {audio_size_bytes} bytes for {characters} characters of text; "
        f"a complete take is at least {floor} bytes, so the response was cut off"
    )


def raise_if_truncated_take(
    *,
    provider: str,
    audio_size_bytes: int,
    characters: int,
    usage: object | None = None,
) -> None:
    """The ONE accept-point check every speech adapter runs on a paid audio body, before storage.

    A body that cannot hold its text raises :class:`TruncatedSpeechError` carrying a retryable
    ``incomplete_response`` classification and (when given) the billed usage, so the run's own retry buys
    a fresh take, the spend is recorded once, and the stub is never stored or cached. Returns ``None`` for a
    plausible take.
    """
    cut_off = truncated_take_reason(audio_size_bytes, characters)
    if cut_off is None:
        return
    from matrx_ai.providers.errors import RetryableError, attach_billed_usage

    truncated = TruncatedSpeechError(f"{provider} speech: {cut_off}")
    truncated.error_info = RetryableError(  # type: ignore[attr-defined]
        error_type="incomplete_response",
        message=str(truncated),
        retry_after=2.0,
        is_retryable=True,
        user_message=f"The voice from {provider} was cut off before it finished.",
        details={
            "provider": provider,
            "modality": "audio",
            "audio_bytes": audio_size_bytes,
            "characters": characters,
        },
    )
    if usage is not None:
        attach_billed_usage(truncated, usage)  # type: ignore[arg-type]
    raise truncated
