"""Pipecat frame-name tables and payload helpers (pure; no Pipecat import).

Keyed on ``type(frame).__name__`` rather than on the classes themselves so this module stays
importable without Pipecat installed, and so a frame renamed upstream fails a table test
instead of an import. This is the *class* name — every Pipecat frame also carries an instance
``name`` attribute (``"TranscriptionFrame#3"``), which is NOT what we match on.

``is_rejected`` is deliberately subclass-blind for anything not named exactly in ``REJECTED``:
it also drops any frame whose class name ends in ``AudioRawFrame`` (e.g. Pipecat's
``UserAudioRawFrame``/``SpeechOutputAudioRawFrame``, both subclasses of the base audio frames),
since those still arrive per audio chunk. A differently-suffixed high-volume subclass added
upstream would not be caught by either rule.
"""

from __future__ import annotations

from typing import Any

from aigie.tracing.llm_metadata import normalize_provider

_BASE_META = {"framework": "pipecat", "type": "pipecat"}

# Dropped before any other work. These arrive per audio chunk — tens of
# thousands per call — and the observer queue is unbounded.
REJECTED: frozenset[str] = frozenset(
    {
        "AudioRawFrame",
        "InputAudioRawFrame",
        "OutputAudioRawFrame",
        "TTSAudioRawFrame",
        "BotSpeakingFrame",
        "InterimTranscriptionFrame",
        "HeartbeatFrame",
        "UserSpeakingFrame",
    }
)

CONVERSATION_START: frozenset[str] = frozenset({"StartFrame"})
CONVERSATION_END: frozenset[str] = frozenset({"EndFrame", "StopFrame", "CancelFrame"})
# Pushed by Pipecat when the user barges in on a live bot response. A
# SystemFrame broadcast both upstream and downstream, so more than one
# (possibly distinct) instance arrives per conceptual interruption — the
# handler that reacts to it must be idempotent on its own, not rely on the
# per-hop frame.id dedupe upstream in on_push_frame.
INTERRUPTION: frozenset[str] = frozenset({"InterruptionFrame"})
LLM_START: frozenset[str] = frozenset({"LLMFullResponseStartFrame"})
LLM_CONTEXT: frozenset[str] = frozenset({"LLMContextFrame"})
LLM_TEXT: frozenset[str] = frozenset({"LLMTextFrame"})
METRICS: frozenset[str] = frozenset({"MetricsFrame"})
LLM_END: frozenset[str] = frozenset({"LLMFullResponseEndFrame"})
TTS_START: frozenset[str] = frozenset({"TTSStartedFrame"})
TTS_TEXT: frozenset[str] = frozenset({"TTSTextFrame"})
TTS_END: frozenset[str] = frozenset({"TTSStoppedFrame"})
ERROR: frozenset[str] = frozenset({"ErrorFrame", "FatalErrorFrame"})
FUNCTION_CALL_STARTED: frozenset[str] = frozenset({"FunctionCallInProgressFrame"})
FUNCTION_CALL_RESULT: frozenset[str] = frozenset({"FunctionCallResultFrame"})
FUNCTION_CALL_CANCEL: frozenset[str] = frozenset({"FunctionCallCancelFrame"})

# LLM service class name → provider slug. An unlisted service (Pipecat has
# ~30 packages) simply gets no metadata.provider — see provider_for's docstring.
_PROVIDERS: dict[str, str] = {
    "OpenAILLMService": "openai",
    "AnthropicLLMService": "anthropic",
    "GoogleLLMService": "gemini",
    "AWSBedrockLLMService": "bedrock",
    "AzureLLMService": "azure",
    "GroqLLMService": "groq",
    "CerebrasLLMService": "cerebras",
    "FireworksLLMService": "fireworks",
    "TogetherLLMService": "together",
    "DeepSeekLLMService": "deepseek",
    "GrokLLMService": "xai",
    "MistralLLMService": "mistral",
    # STT/TTS service classes, grepped from pipecat/services/*/stt.py and
    # tts.py. Deliberately excludes locally-run/open-weight services with no
    # billing vendor to attribute to (e.g. WhisperSTTService, MoonshineSTTService,
    # KokoroTTSService, PiperTTSService, XTTSService, PocketTTSService,
    # FunASRSTTService) — there is no provider slug to guess there, so they
    # correctly fall through to None, same as an unmapped service.
    "DeepgramSTTService": "deepgram",
    "DeepgramTTSService": "deepgram",
    "DeepgramHttpTTSService": "deepgram",
    "AzureSTTService": "azure",
    "AzureTTSService": "azure",
    "AzureHttpTTSService": "azure",
    "CartesiaSTTService": "cartesia",
    "CartesiaTTSService": "cartesia",
    "CartesiaHttpTTSService": "cartesia",
    "AssemblyAISTTService": "assemblyai",
    "AWSTranscribeSTTService": "aws",
    "AWSPollyTTSService": "aws",
    "GroqSTTService": "groq",
    "GroqTTSService": "groq",
    "ElevenLabsSTTService": "elevenlabs",
    "ElevenLabsRealtimeSTTService": "elevenlabs",
    "ElevenLabsTTSService": "elevenlabs",
    "ElevenLabsHttpTTSService": "elevenlabs",
    "OpenAISTTService": "openai",
    "OpenAIRealtimeSTTService": "openai",
    "OpenAITTSService": "openai",
    "GladiaSTTService": "gladia",
    "GoogleSTTService": "gemini",
    "GoogleHttpTTSService": "gemini",
    "GoogleTTSService": "gemini",
    "GeminiTTSService": "gemini",
    "NvidiaSTTService": "nvidia",
    "NvidiaSegmentedSTTService": "nvidia",
    "NvidiaTTSService": "nvidia",
    "MistralSTTService": "mistral",
    "MistralTTSService": "mistral",
    "SpeechmaticsSTTService": "speechmatics",
    "SpeechmaticsTTSService": "speechmatics",
    "SonioxSTTService": "soniox",
    "SonioxTTSService": "soniox",
    "SmallestSTTService": "smallest",
    "SmallestTTSService": "smallest",
    "SarvamSTTService": "sarvam",
    "SarvamHttpTTSService": "sarvam",
    "SarvamTTSService": "sarvam",
    "XAISTTService": "xai",
    "XAIHttpTTSService": "xai",
    "XAITTSService": "xai",
    "TogetherSTTService": "together",
    "TogetherTTSService": "together",
    "FalSTTService": "fal",
    "RimeTTSService": "rime",
    "RimeHttpTTSService": "rime",
    "RimeNonJsonTTSService": "rime",
    "LmntTTSService": "lmnt",
    "NeuphonicTTSService": "neuphonic",
    "NeuphonicHttpTTSService": "neuphonic",
    "InworldTTSService": "inworld",
    "InworldHttpTTSService": "inworld",
    "ResembleAITTSService": "resemble_ai",
    "MiniMaxHttpTTSService": "minimax",
    "HumeTTSService": "hume",
}


def is_rejected(frame_name: str) -> bool:
    return frame_name in REJECTED or frame_name.endswith("AudioRawFrame")


def interruption_settled(open_spans: dict[str, str]) -> bool:
    """True once neither an ``llm`` nor a ``tts`` span is still open.

    Gates when ``_Boundary.interrupted`` may be cleared. A single barge-in can
    leave both lanes open at once (streaming TTS starts before the LLM's own
    response frame ends), so the flag must survive until whichever closes
    last has had a chance to read it — clearing it the moment the first one
    closes would let the second one wrongly close as "success".
    """
    return "llm" not in open_spans and "tts" not in open_spans


def clear_interrupted_if_settled(boundary: Any) -> None:
    """Drop the barge-in flag once neither lane can still read it.

    Both `_llm.on_llm_end` and `_media.on_tts_stopped` must clear it the same
    way, so the rule lives here rather than being written out in each.
    """
    if boundary.interrupted and interruption_settled(boundary.open_spans):
        boundary.interrupted = False


def is_barge_in(open_spans: dict[str, str]) -> bool:
    """True when an ``InterruptionFrame`` actually cut something off.

    Pipecat pushes one at the start of every user turn — the real order is
    ``UserStartedSpeakingFrame``, ``InterruptionFrame``,
    ``LLMFullResponseStartFrame`` — to stop bot speech whether or not any is
    playing. Treating every frame as a barge-in therefore marked every ordinary
    turn "interrupted", since the flag was still set when that turn's own llm
    span closed. Only a span that is already open can be cut off.
    """
    return not interruption_settled(open_spans)


def truncate(value: Any, limit: int) -> Any:
    if not isinstance(value, str):
        return value
    return value[:limit]


def provider_for(processor_name: str) -> str | None:
    """Resolve a provider slug from a Pipecat processor name.

    Processor names arrive as ``"OpenAILLMService#0"`` — the instance suffix is
    stripped before lookup. Exact-match only: a prefix-matching fallback would
    invent wrong attributions, and a wrong provider is worse than none — clause
    A only requires ``metadata.provider`` on spans we price, and a misattributed
    provider silently corrupts cost-by-provider splits.
    """
    base = processor_name.split("#", 1)[0]
    # Through normalize_provider so this integration reports the same vocabulary
    # as every other one: a vendor must not appear as two slugs depending on which
    # framework produced the span, or cost-by-provider rollups double-count it.
    return normalize_provider(_PROVIDERS.get(base))


def usage_mapping(metrics_data: Any) -> dict[str, Any] | None:
    """Normalize Pipecat ``LLMUsageMetricsData`` into a usage mapping.

    Cache fields are read explicitly, never derived: Pipecat documents that
    ``total_tokens`` is gross while ``prompt_tokens`` may be net of the prompt
    cache, so ``total != prompt + completion`` in general.
    """
    usage = getattr(metrics_data, "value", None)
    if usage is None:
        return None
    mapping: dict[str, Any] = {
        "prompt_tokens": getattr(usage, "prompt_tokens", 0),
        "completion_tokens": getattr(usage, "completion_tokens", 0),
        "total_tokens": getattr(usage, "total_tokens", 0),
    }
    for attr in ("cache_read_input_tokens", "cache_creation_input_tokens"):
        value = getattr(usage, attr, None)
        if value is not None:
            mapping[attr] = value
    return mapping


def _with_source(meta: dict[str, Any], usage_data: Any) -> dict[str, Any]:
    """Add the model and provider a usage object came from, when it reports them.

    An empty model string (real DeepgramHttpTTSService emits one) means "no model
    reported" — recorded as absent rather than as a blank value.
    """
    model = getattr(usage_data, "model", None)
    if model:
        meta["model"] = model
    provider = provider_for(getattr(usage_data, "processor", "") or "")
    if provider:
        meta["provider"] = provider
    return meta


def stt_metadata(usage_data: Any) -> dict[str, Any]:
    """Normalize Pipecat ``STTUsageMetricsData`` into STT span metadata.

    A locally-run/open-weight STT service (e.g. ``WhisperSTTService``) has no
    billing vendor to attribute to, so ``provider_for`` leaves it unmapped and
    this simply carries no ``provider`` key — the same documented fallback as
    any other unlisted service, not a bug here.
    """
    value = getattr(usage_data, "value", None)
    audio_seconds = getattr(value, "audio_seconds", None)
    meta: dict[str, Any] = {}
    if audio_seconds is not None:
        meta["audio_seconds"] = audio_seconds
    return _with_source(meta, usage_data)


def error_from_frame(frame: Any) -> BaseException:
    """Build the exception to fail a span with from an ``ErrorFrame``.

    Prefers the frame's own ``exception`` (a real traceback) over synthesizing
    one from the ``error`` string, which is only ever a human-readable summary.
    """
    exception: BaseException | None = getattr(frame, "exception", None)
    if exception is not None:
        return exception
    return RuntimeError(getattr(frame, "error", "pipecat error"))


def tts_metadata(usage_data: Any) -> dict[str, Any]:
    """Normalize Pipecat ``TTSUsageMetricsData`` into TTS span metadata.

    Unlike the LLM/STT usage objects, ``value`` here is a plain character
    count rather than a nested object.
    """
    value = getattr(usage_data, "value", None)
    meta: dict[str, Any] = {}
    if isinstance(value, (int, float)):
        meta["character_count"] = value
    return _with_source(meta, usage_data)


def usage_totals(
    stt_audio_seconds_total: float, tts_character_count_total: float
) -> dict[str, Any]:
    """Shape the conversation-level usage sums for the root's metadata.

    Omitted rather than zero when nothing accumulated — the same
    documented-default convention as everywhere else in this module.
    """
    totals: dict[str, Any] = {}
    if stt_audio_seconds_total:
        totals["stt_audio_seconds_total"] = stt_audio_seconds_total
    if tts_character_count_total:
        totals["tts_character_count_total"] = tts_character_count_total
    return totals
