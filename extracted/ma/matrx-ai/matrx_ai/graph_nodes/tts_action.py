"""``ai.text_to_speech`` — voice synthesis via the UnifiedAIClient pipeline.

Unlike ``ai.transcribe`` (which uses the catalog STT execution channel),
TTS routes through the same ``execute_ai_request`` path as chat — the
model_id determines the provider (ElevenLabs / Google / Groq / OpenAI /
XAI / etc.) via the UnifiedConfig → endpoint map.

Returned shape surfaces audio by reference (path / base64 / URL) rather
than shoving megabytes through the channel system. The underlying
providers already write to temp files or return URLs; we propagate
whatever comes back, picking the most usable field.

Declared IDEMPOTENT: the same (model, text, voice, settings) will
render the same audio for deterministic providers. Non-deterministic
providers (some ElevenLabs voices with randomness) can override via
``re_execute_on_resume=True`` on the node.
"""

from __future__ import annotations

from typing import Any

from matrx_graph.actions import register_node
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras
from pydantic import BaseModel, ConfigDict, Field, JsonValue

from matrx_ai.graph_nodes.shared import AiUsage, _extract_usage


class TextToSpeechInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    model: str = Field(
        min_length=1,
        description=(
            "TTS model id. Example: 'eleven_v3', "
            "'playai-tts' (Groq), 'gemini-2.5-flash-preview-tts' (Google)."
        ),
        json_schema_extra=field_extras(widget="model_picker"),
    )
    text: str = Field(
        min_length=1,
        description="Text to synthesize.",
        json_schema_extra=field_extras(widget="textarea", multiline_rows=5),
    )
    voice: str | None = Field(
        default=None,
        description=(
            "Provider-specific voice id. ElevenLabs voice_id, Groq voice name, "
            "etc. Leaves provider default when None."
        ),
    )
    format: str = Field(
        default="mp3",
        description="Audio format: mp3, wav, opus, pcm, etc. (provider-dependent).",
    )
    speed: float | None = Field(
        default=None,
        ge=0.25,
        le=4.0,
        description="Playback rate. None keeps provider default.",
    )
    metadata: dict[str, JsonValue] = Field(default_factory=dict)


class TextToSpeechOutput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # THE IDENTITY RULE (same as GeneratedImage in image_action.py): ``file_id``
    # is the durable handle a node output carries. Every TTS provider class
    # persists the audio through ``save_media_envelope_async`` and KNOWS the id
    # at that moment — this node used to drop it and emit the URL alone, so a
    # consumer reading the output after the signature expired had nothing to
    # re-mint from.
    file_id: str | None = Field(
        default=None,
        description=(
            "cld_files id of the generated audio — the durable handle. Pass this "
            "between nodes and re-mint any URL from it; never store a signed URL."
        ),
    )
    audio_path: str | None = Field(
        default=None, description="Local temp path, when the provider wrote a file."
    )
    audio_url: str | None = Field(
        default=None,
        description=(
            "DURABLE playable URL — a CDN/public/external link that outlives this "
            "row. Null for personal audio, whose only URL expires: resolve one "
            "from file_id at the moment you need it."
        ),
    )
    audio_cdn_url: str | None = Field(
        default=None, description="Permanent CDN URL, present only when the audio is public."
    )
    audio_b64: str | None = Field(
        default=None,
        description="Base64-encoded audio bytes, when nothing else is available.",
    )
    mime_type: str | None = Field(
        default=None, description="Canonical MIME type of the encoded audio."
    )
    duration_seconds: float = Field(
        default=0.0, description="Audio duration in seconds, when it is known."
    )
    model: str = Field(description="TTS model id that produced the audio.")
    # Canonical usage shape shared by every matrx-ai graph action (same type
    # the failure path already emits under details["usage"]).
    usage: AiUsage = Field(default_factory=AiUsage)


class _AudioRefs(BaseModel):
    """What one TTS response yielded — identity first, then the ways to play it."""

    model_config = ConfigDict(extra="forbid")

    file_id: str | None = None
    path: str | None = None
    url: str | None = None
    b64: str | None = None
    mime: str | None = None
    duration_seconds: float | None = None


def _audio_refs_from_blocks(response: Any) -> _AudioRefs | None:
    """Preferred shape: a ``UnifiedResponse`` carrying ``AudioContent`` blocks.

    Every TTS provider class (ElevenLabs / Groq / OpenAI / xAI) persists the
    bytes through ``save_media_envelope_async`` and builds an ``AudioContent``
    with ``file_id`` + ``url`` + ``duration_ms``. Reading only the dict dump
    below is how the id got dropped — the block is where the identity lives.
    """
    from matrx_ai.config.media_config import AudioContent

    messages = getattr(response, "messages", None) or []
    for msg in messages:
        content = getattr(msg, "content", None) or []
        for block in content:
            if isinstance(block, AudioContent):
                metadata = block.metadata or {}
                duration = None
                if block.duration_ms is not None:
                    duration = block.duration_ms / 1000.0
                return _AudioRefs(
                    file_id=block.file_id,
                    path=metadata.get("path"),
                    url=block.url,
                    b64=block.base64_data,
                    mime=block.mime_type,
                    duration_seconds=duration,
                )
    return None


def _pick_audio_refs(response: Any) -> _AudioRefs:
    """Scan a unified response for audio references.

    Block-first (identity-carrying), dict-probe as the fallback for any
    provider path not yet wired through ``AudioContent``.
    """
    from_blocks = _audio_refs_from_blocks(response)
    if from_blocks is not None:
        return from_blocks

    file_id: str | None = None
    audio_path: str | None = None
    audio_url: str | None = None
    audio_b64: str | None = None
    mime: str | None = None

    # Response objects vary by provider; dict-dump then probe known keys.
    dump: dict[str, Any] = {}
    for attr in ("model_dump", "dict", "to_dict"):
        method = getattr(response, attr, None)
        if callable(method):
            try:
                candidate = method()
                if isinstance(candidate, dict):
                    dump = candidate
                    break
            except Exception:
                pass

    # Top-level probes
    if isinstance(dump.get("file_id"), str):
        file_id = dump["file_id"]
    for key in ("audio_path", "file_path", "local_path"):
        if isinstance(dump.get(key), str):
            audio_path = dump[key]
            break
    for key in ("audio_url", "url", "remote_url"):
        if isinstance(dump.get(key), str):
            audio_url = dump[key]
            break
    for key in ("audio_b64", "audio_base64", "audio_data"):
        if isinstance(dump.get(key), str):
            audio_b64 = dump[key]
            break
    if isinstance(dump.get("mime_type"), str):
        mime = dump["mime_type"]
    elif isinstance(dump.get("content_type"), str):
        mime = dump["content_type"]

    # Deeper probe: provider may stuff content blocks in `content` / `messages`
    content = dump.get("content") or dump.get("messages") or []
    if isinstance(content, list):
        for block in content:
            if not isinstance(block, dict):
                continue
            btype = block.get("type", "")
            if "audio" in btype:
                file_id = file_id or block.get("file_id")
                audio_path = audio_path or block.get("path") or block.get("file_path")
                audio_url = audio_url or block.get("url")
                audio_b64 = audio_b64 or block.get("data") or block.get("base64")
                mime = mime or block.get("mime_type") or block.get("content_type")

    return _AudioRefs(
        file_id=file_id,
        path=audio_path,
        url=audio_url,
        b64=audio_b64,
        mime=mime,
    )


@register_node(
    name="ai.text_to_speech",
    display_name="Text to Speech",
    description="Turn written text into natural-sounding audio.",
    category=NodeCategory.LLM,
    determinism=ActionTier.IDEMPOTENT,
    input_schema=TextToSpeechInput,
    output_schema=TextToSpeechOutput,
    # Seed: matrx-frontend migrations/content_ir_seed_media_io_kinds.sql
    # (schema derived from TextToSpeechOutput — keep the two in lockstep).
    output_kind="generated_audio",
    icon="audio-lines",
    tags=("ai", "audio", "tts", "voice"),
)
async def ai_text_to_speech(
    ctx: NodeExecutionContext, inputs: TextToSpeechInput
) -> NodeResult[TextToSpeechOutput]:
    _ = ctx

    try:
        from matrx_files import is_durable_media_url

        from matrx_ai.config import UnifiedConfig
        from matrx_ai.orchestrator.executor import execute_ai_request

        config_payload: dict[str, Any] = {
            "model": inputs.model,
            "messages": [{"role": "user", "content": inputs.text}],
        }
        if inputs.voice:
            config_payload["voice"] = inputs.voice
        if inputs.format:
            config_payload["audio_format"] = inputs.format
        if inputs.speed is not None:
            config_payload["speed"] = inputs.speed

        config = UnifiedConfig.from_dict(config_payload)

        completed = await execute_ai_request(
            config,
            max_iterations=1,
            max_retries_per_iteration=2,
            metadata=inputs.metadata or None,
        )

        response = getattr(completed, "final_response", None)
        refs = _pick_audio_refs(response)

        usage_raw = getattr(completed, "total_usage", None)
        # One canonical extractor (shared with the failure path below) — the
        # old hand-rolled loop read a non-existent ``totals`` attribute off
        # AggregatedUsage and silently reported empty usage.
        usage = _extract_usage(usage_raw)

        # The AudioContent block's own duration_ms is authoritative; the run
        # metadata is the fallback for the dict-probe path.
        duration = refs.duration_seconds or 0.0
        if not duration:
            meta = getattr(completed, "metadata", {}) or {}
            for key in ("duration_seconds", "audio_duration", "duration"):
                v = meta.get(key)
                if isinstance(v, int | float):
                    duration = float(v)
                    break

        if not (refs.file_id or refs.path or refs.url or refs.b64):
            # Paid call with no artifact — fail with the billed usage in
            # details so the scheduler's cost settlement records the spend.
            return failure(
                "tts_failed",
                f"ai.text_to_speech: provider returned no audio for model '{inputs.model}'.",
                details={
                    "model": inputs.model,
                    "usage": _extract_usage(usage_raw).model_dump(mode="json"),
                },
            )

        return success(
            TextToSpeechOutput(
                file_id=refs.file_id,
                audio_path=refs.path,
                # This output is written to workflow.node_outcome and replayed
                # days later, so only a DURABLE url may ride it — the expiring
                # one is dropped, not labelled. One classifier (matrx_files)
                # decides; file_id is what a consumer re-mints from.
                audio_url=refs.url if is_durable_media_url(refs.url) else None,
                audio_cdn_url=refs.url if is_durable_media_url(refs.url) else None,
                audio_b64=refs.b64,
                mime_type=refs.mime,
                duration_seconds=duration,
                model=inputs.model,
                usage=usage,
            )
        )
    except Exception as e:
        return failure(
            "tts_failed",
            f"{type(e).__name__}: {e}",
            details={"model": inputs.model},
        )
