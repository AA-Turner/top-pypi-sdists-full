"""
Cost tracking for LiveKit Agents voice pipelines.

Provides pricing information and cost calculation for voice services
(STT, TTS, LLM) commonly used in LiveKit Agents applications.

LiveKit Agents supports 60+ plugin integrations including:
- STT: Deepgram, OpenAI Whisper, Google, Azure, AssemblyAI
- TTS: Cartesia, ElevenLabs, OpenAI, Google, PlayHT
- LLM: OpenAI, Anthropic, Google Gemini, Groq, Together
- Realtime: OpenAI Realtime API, Gemini Live
"""

from typing import Any

# STT pricing per minute of audio
STT_PRICING: dict[str, dict[str, float]] = {
    # Deepgram (most common with LiveKit)
    "deepgram/nova-3": {"per_minute": 0.0043},
    "deepgram/nova-2": {"per_minute": 0.0043},
    "deepgram-nova-2": {"per_minute": 0.0043},
    "deepgram-nova": {"per_minute": 0.0043},
    "deepgram-enhanced": {"per_minute": 0.0145},
    "deepgram-base": {"per_minute": 0.0048},
    # OpenAI Whisper
    "whisper-1": {"per_minute": 0.006},
    "openai-whisper": {"per_minute": 0.006},
    # Google
    "google-speech-to-text": {"per_minute": 0.024},
    "google-chirp": {"per_minute": 0.016},
    # Azure
    "azure-speech-to-text": {"per_minute": 0.016},
    # AssemblyAI
    "assemblyai": {"per_minute": 0.015},
    # Default
    "default": {"per_minute": 0.006},
}

# TTS pricing per 1M characters
TTS_PRICING: dict[str, dict[str, float]] = {
    # Cartesia (most common with LiveKit)
    "cartesia/sonic-3": {"per_1m_chars": 15.0},
    "cartesia/sonic-2": {"per_1m_chars": 15.0},
    "cartesia": {"per_1m_chars": 15.0},
    # ElevenLabs
    "elevenlabs-multilingual-v2": {"per_1m_chars": 180.0},
    "elevenlabs-turbo-v2.5": {"per_1m_chars": 90.0},
    "elevenlabs": {"per_1m_chars": 180.0},
    # OpenAI TTS
    "tts-1": {"per_1m_chars": 15.0},
    "tts-1-hd": {"per_1m_chars": 30.0},
    "openai-tts": {"per_1m_chars": 15.0},
    # Google
    "google-text-to-speech": {"per_1m_chars": 16.0},
    # PlayHT
    "playht": {"per_1m_chars": 15.0},
    # Default
    "default": {"per_1m_chars": 15.0},
}

# LLM pricing per 1M tokens (input/output)
LLM_PRICING: dict[str, dict[str, float]] = {
    # OpenAI
    "gpt-4.1": {"input": 2.00, "output": 8.00},
    "gpt-4.1-mini": {"input": 0.40, "output": 1.60},
    "gpt-4.1-nano": {"input": 0.10, "output": 0.40},
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o-realtime": {"input": 5.00, "output": 20.00},
    # Anthropic
    "claude-sonnet-4-5": {"input": 3.00, "output": 15.00},
    "claude-haiku-4-5": {"input": 1.00, "output": 5.00},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    # Google
    "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
    "gemini-2.5-pro": {"input": 1.25, "output": 10.00},
    "gemini-2.5-flash": {"input": 0.15, "output": 0.60},
    # Groq
    "llama-3.3-70b": {"input": 0.59, "output": 0.79},
    "llama-3.1-8b": {"input": 0.05, "output": 0.08},
    # Default
    "default": {"input": 2.00, "output": 8.00},
}


def get_stt_pricing(model_id: str | None) -> float:
    """Get STT pricing per minute of audio."""
    if not model_id:
        return STT_PRICING["default"]["per_minute"]

    model_lower = model_id.lower()
    if model_lower in STT_PRICING:
        return STT_PRICING[model_lower]["per_minute"]

    for key, pricing in STT_PRICING.items():
        if key in model_lower or model_lower in key:
            return pricing["per_minute"]

    return STT_PRICING["default"]["per_minute"]


def get_tts_pricing(model_id: str | None) -> float:
    """Get TTS pricing per 1M characters."""
    if not model_id:
        return TTS_PRICING["default"]["per_1m_chars"]

    model_lower = model_id.lower()
    if model_lower in TTS_PRICING:
        return TTS_PRICING[model_lower]["per_1m_chars"]

    for key, pricing in TTS_PRICING.items():
        if key in model_lower or model_lower in key:
            return pricing["per_1m_chars"]

    return TTS_PRICING["default"]["per_1m_chars"]


def get_llm_pricing(model_id: str | None) -> tuple[float, float]:
    """Get LLM pricing (input/output per 1M tokens)."""
    if not model_id:
        p = LLM_PRICING["default"]
        return p["input"], p["output"]

    model_lower = model_id.lower()
    if model_lower in LLM_PRICING:
        p = LLM_PRICING[model_lower]
        return p["input"], p["output"]

    for key, pricing in LLM_PRICING.items():
        if key in model_lower or model_lower in key:
            return pricing["input"], pricing["output"]

    p = LLM_PRICING["default"]
    return p["input"], p["output"]


def calculate_stt_cost(model_id: str | None, audio_duration_seconds: float = 0) -> float:
    """Calculate STT cost in USD."""
    return (audio_duration_seconds / 60.0) * get_stt_pricing(model_id)


def calculate_tts_cost(model_id: str | None, characters: int = 0) -> float:
    """Calculate TTS cost in USD."""
    return (characters / 1_000_000) * get_tts_pricing(model_id)


def calculate_llm_cost(
    model_id: str | None, input_tokens: int = 0, output_tokens: int = 0
) -> float:
    """Calculate LLM cost in USD."""
    inp, out = get_llm_pricing(model_id)
    return (input_tokens / 1_000_000) * inp + (output_tokens / 1_000_000) * out


def calculate_turn_cost(
    stt_model: str | None = None,
    tts_model: str | None = None,
    llm_model: str | None = None,
    audio_duration_seconds: float = 0,
    tts_characters: int = 0,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> dict[str, float]:
    """Calculate total cost for a voice conversation turn."""
    stt = calculate_stt_cost(stt_model, audio_duration_seconds)
    tts = calculate_tts_cost(tts_model, tts_characters)
    llm = calculate_llm_cost(llm_model, input_tokens, output_tokens)
    return {"stt_cost": stt, "tts_cost": tts, "llm_cost": llm, "total_cost": stt + tts + llm}


def get_livekit_agents_cost(
    model: str | None = None,
    input_tokens: int = 0,
    output_tokens: int = 0,
    audio_duration_seconds: float = 0,
    tts_characters: int = 0,
    stt_model: str | None = None,
    tts_model: str | None = None,
) -> dict[str, Any]:
    """
    Calculate costs for a LiveKit Agents interaction.

    Convenience function matching the pattern of other integrations' cost functions.
    """
    costs = calculate_turn_cost(
        stt_model=stt_model,
        tts_model=tts_model,
        llm_model=model,
        audio_duration_seconds=audio_duration_seconds,
        tts_characters=tts_characters,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
    )
    costs["input_tokens"] = input_tokens
    costs["output_tokens"] = output_tokens
    return costs


class VoiceCostTracker:
    """Tracks costs across voice conversation turns."""

    def __init__(self) -> None:
        self._total_cost: float = 0.0
        self._stt_cost: float = 0.0
        self._tts_cost: float = 0.0
        self._llm_cost: float = 0.0
        self._total_audio_seconds: float = 0.0
        self._total_tts_characters: int = 0
        self._total_input_tokens: int = 0
        self._total_output_tokens: int = 0
        self._turn_count: int = 0
        self._by_model: dict[str, dict[str, float]] = {}

    def add_turn(
        self,
        stt_model: str | None = None,
        tts_model: str | None = None,
        llm_model: str | None = None,
        audio_duration_seconds: float = 0,
        tts_characters: int = 0,
        input_tokens: int = 0,
        output_tokens: int = 0,
    ) -> dict[str, float]:
        """Add a turn's usage to the tracker."""
        costs = calculate_turn_cost(
            stt_model=stt_model,
            tts_model=tts_model,
            llm_model=llm_model,
            audio_duration_seconds=audio_duration_seconds,
            tts_characters=tts_characters,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )
        self._stt_cost += costs["stt_cost"]
        self._tts_cost += costs["tts_cost"]
        self._llm_cost += costs["llm_cost"]
        self._total_cost += costs["total_cost"]
        self._total_audio_seconds += audio_duration_seconds
        self._total_tts_characters += tts_characters
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._turn_count += 1

        for model_id, model_cost, service in [
            (stt_model, costs["stt_cost"], "stt"),
            (tts_model, costs["tts_cost"], "tts"),
            (llm_model, costs["llm_cost"], "llm"),
        ]:
            if model_id and model_cost > 0:
                key = f"{service}:{model_id}"
                if key not in self._by_model:
                    self._by_model[key] = {"cost": 0.0, "count": 0}
                self._by_model[key]["cost"] += model_cost
                self._by_model[key]["count"] += 1

        return costs

    @property
    def total_cost(self) -> float:
        return self._total_cost

    def get_summary(self) -> dict[str, Any]:
        """Get full cost tracking summary."""
        return {
            "total_cost": self._total_cost,
            "stt_cost": self._stt_cost,
            "tts_cost": self._tts_cost,
            "llm_cost": self._llm_cost,
            "total_audio_seconds": self._total_audio_seconds,
            "total_tts_characters": self._total_tts_characters,
            "total_input_tokens": self._total_input_tokens,
            "total_output_tokens": self._total_output_tokens,
            "turn_count": self._turn_count,
            "avg_cost_per_turn": self._total_cost / self._turn_count if self._turn_count > 0 else 0,
            "by_model": self._by_model,
        }

    def reset(self) -> None:
        """Reset all tracked costs."""
        self._total_cost = 0.0
        self._stt_cost = 0.0
        self._tts_cost = 0.0
        self._llm_cost = 0.0
        self._total_audio_seconds = 0.0
        self._total_tts_characters = 0
        self._total_input_tokens = 0
        self._total_output_tokens = 0
        self._turn_count = 0
        self._by_model = {}
