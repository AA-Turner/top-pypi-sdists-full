"""
Audio Preprocessing for Unified Config

Handles automatic transcription of audio content when the auto_transcribe flag is set
OR when the target API doesn't support native audio input (automatic fallback).
"""

from __future__ import annotations

from matrx_utils import vcprint

from matrx_ai.config import (
    AudioContent,
    MessageList,
    TextContent,
    TokenUsage,
    UnifiedMessage,
)


async def preprocess_audio_in_messages(
    messages: MessageList,
    debug: bool = False,
    *,
    supports_audio_input: bool,
) -> tuple[MessageList, list[TokenUsage]]:
    """
    Preprocess messages to handle auto-transcription of audio content.

    Audio is transcribed when:
    1. auto_transcribe=True (explicitly requested by user)
    2. the model doesn't accept native audio input (automatic fallback)

    After transcription:
    1. Audio is replaced with TextContent containing the transcription
    2. Metadata about the original audio is preserved
    3. Usage for transcription API calls is tracked

    Args:
        messages: MessageList to preprocess
        debug: Enable debug logging
        supports_audio_input: the target model's declared audio-input capability
            (``ResolvedModelCapabilities.supports_audio_input``)

    Returns:
        Tuple of (MessageList with audio transcribed, List of TokenUsage for transcriptions)
    """
    processed_messages = []
    transcription_usage_list = []

    for message in messages.to_list():
        processed_content = []

        for content in message.content:
            # Check if this audio needs transcription
            should_transcribe = False
            transcribe_reason = None

            if isinstance(content, AudioContent):
                if content.auto_transcribe:
                    # User explicitly requested transcription
                    should_transcribe = True
                    transcribe_reason = "explicit"
                elif not supports_audio_input:
                    # Model doesn't accept audio - automatic fallback
                    should_transcribe = True
                    transcribe_reason = "fallback"
                    # Mark the content so the async catalog STT path runs.
                    content.auto_transcribe = True

            if should_transcribe:
                # Transcribe audio
                if debug:
                    if transcribe_reason == "explicit":
                        vcprint(
                            f"Auto-transcribing audio from: {content.url or content.file_uri or 'base64 data'}",
                            "Audio Preprocessing",
                            color="cyan",
                        )
                    else:  # fallback
                        vcprint(
                            f"⚠️ API doesn't support audio - transcribing as fallback: {content.url or content.file_uri or 'base64 data'}",
                            "Audio Preprocessing",
                            color="yellow",
                        )

                try:
                    transcription = await content.get_transcription_async()

                    if transcription:
                        # Create text content with transcription
                        text_content = TextContent(
                            text=f"[Audio Transcription]: {transcription}",
                            metadata={
                                "original_type": "audio",
                                "transcription_metadata": content.metadata.get("transcription", {}),
                                "audio_source": content.url or content.file_uri or "base64",
                            },
                        )
                        processed_content.append(text_content)

                        # Track transcription usage (only if not from cache)
                        transcription_metadata = content.metadata.get("transcription", {})
                        from_cache = transcription_metadata.get("from_cache", False)
                        usage_data = transcription_metadata.get("usage", {})

                        matrx_model_name = str(
                            usage_data.get("matrx_model_name") or content.transcription_model
                        )
                        duration_seconds = 0.0

                        if usage_data and not from_cache:
                            # Create TokenUsage for transcription
                            # STT is billed by audio duration rather than tokens.
                            # We'll represent it as "input tokens" for tracking purposes
                            duration_seconds = usage_data.get("billed_duration", 0)

                            from matrx_ai.processing.audio.stt import (
                                duration_to_stt_input_units,
                            )

                            usage_basis = str(usage_data.get("usage_basis") or "")
                            duration_as_tokens = duration_to_stt_input_units(
                                usage_basis, duration_seconds
                            )

                            model_from_usage = usage_data.get("model")
                            if not model_from_usage:
                                vcprint(
                                    f"⚠️  WARNING: STT usage missing model name for response_id: {usage_data.get('response_id')}",
                                    color="red",
                                )
                                vcprint(
                                    "USING THE REQUESTED CATALOG MODEL AS THE USAGE MODEL",
                                    color="yellow",
                                )
                                model_from_usage = matrx_model_name

                            usage = TokenUsage(
                                input_tokens=duration_as_tokens,
                                output_tokens=0,  # Transcription doesn't have "output tokens"
                                cached_input_tokens=0,
                                matrx_model_name=matrx_model_name,
                                provider_model_name=model_from_usage,
                                api=str(usage_data.get("api") or "stt"),
                                offering_id=str(usage_data.get("offering_id") or ""),
                                offering_route="preferred",
                                response_id=None,
                                metadata={
                                    "duration_seconds": usage_data.get("duration_seconds", 0),
                                    "billed_duration": duration_seconds,
                                    "file_size_mb": usage_data.get("file_size_mb", 0),
                                    "language": usage_data.get("language"),
                                    "operation": usage_data.get("operation", "transcription"),
                                    "usage_basis": usage_basis,
                                    "response_format": usage_data.get("response_format"),
                                    "audio_source": content.url or content.file_uri or "base64",
                                },
                            )
                            transcription_usage_list.append(usage)
                        elif from_cache and debug:
                            vcprint(
                                "✓ Using cached transcription (no API call)",
                                "Audio Preprocessing",
                                color="blue",
                            )

                        if debug:
                            vcprint(
                                f"✓ Audio transcribed successfully ({len(transcription)} characters, {duration_seconds:.1f}s)",
                                "Audio Preprocessing",
                                color="green",
                            )
                            print("--------------------------------")
                            print(transcription)
                            print("--------------------------------")
                    else:
                        # Transcription failed, skip audio
                        vcprint(
                            "⚠️ Audio transcription failed - audio will be skipped",
                            "Audio Preprocessing",
                            color="yellow",
                        )

                except Exception as e:
                    vcprint(
                        f"⚠️ Audio transcription error: {str(e)} - audio will be skipped",
                        "Audio Preprocessing",
                        color="yellow",
                    )
            else:
                # Keep content as-is
                processed_content.append(content)

        # Create new message with processed content
        processed_messages.append(
            UnifiedMessage(
                role=message.role,
                content=processed_content,
                id=message.id,
                name=message.name,
                timestamp=message.timestamp,
                metadata=message.metadata,
            )
        )

    return MessageList(_messages=processed_messages), transcription_usage_list


def should_preprocess_audio(messages: MessageList, *, supports_audio_input: bool) -> bool:
    """
    Check if any messages contain audio that needs transcription.

    Audio needs transcription if:
    1. auto_transcribe=True (explicitly requested)
    2. the model doesn't accept native audio input (automatic fallback)

    Args:
        messages: MessageList to check
        supports_audio_input: the target model's declared audio-input capability

    Returns:
        True if preprocessing is needed, False otherwise
    """
    for message in messages.to_list():
        for content in message.content:
            if isinstance(content, AudioContent):
                # Needs transcription if explicitly requested OR the model can't hear
                if content.auto_transcribe or not supports_audio_input:
                    return True
    return False
