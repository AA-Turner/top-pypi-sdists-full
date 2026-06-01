"""
Cost tracking for Pipecat voice pipelines.

Provides pricing information and cost calculation for voice services
(STT, TTS, LLM) commonly used in Pipecat applications.
"""


# STT pricing per minute of audio
STT_PRICING: dict[str, dict[str, float]] = {
    # Deepgram
    "deepgram-nova-2": {"per_minute": 0.0043},
    "deepgram-nova": {"per_minute": 0.0043},
    "deepgram-enhanced": {"per_minute": 0.0145},
    "deepgram-base": {"per_minute": 0.0048},
    "deepgram-whisper": {"per_minute": 0.0048},
    # OpenAI Whisper
    "whisper-1": {"per_minute": 0.006},
    "openai-whisper": {"per_minute": 0.006},
    # Google
    "google-speech-to-text": {"per_minute": 0.024},
    "google-chirp": {"per_minute": 0.016},
    # Azure
    "azure-speech-to-text": {"per_minute": 0.016},
    # AssemblyAI
    "assemblyai": {"per_minute": 0.00025 * 60},  # $0.00025/second
    # Default
    "default": {"per_minute": 0.006},
}

# TTS pricing per 1M characters
TTS_PRICING: dict[str, dict[str, float]] = {
    # ElevenLabs
    "elevenlabs-multilingual-v2": {"per_1m_chars": 180.0},
    "elevenlabs-turbo-v2": {"per_1m_chars": 90.0},
    "elevenlabs-turbo-v2.5": {"per_1m_chars": 90.0},
    "elevenlabs": {"per_1m_chars": 180.0},
    # OpenAI TTS
    "tts-1": {"per_1m_chars": 15.0},
    "tts-1-hd": {"per_1m_chars": 30.0},
    "openai-tts": {"per_1m_chars": 15.0},
    # Google
    "google-text-to-speech": {"per_1m_chars": 16.0},
    "google-wavenet": {"per_1m_chars": 16.0},
    "google-neural2": {"per_1m_chars": 16.0},
    # Azure
    "azure-text-to-speech": {"per_1m_chars": 15.0},
    "azure-neural": {"per_1m_chars": 15.0},
    # Amazon Polly
    "polly-standard": {"per_1m_chars": 4.0},
    "polly-neural": {"per_1m_chars": 16.0},
    # Cartesia
    "cartesia": {"per_1m_chars": 15.0},
    # PlayHT
    "playht": {"per_1m_chars": 15.0},
    # XTTS
    "xtts": {"per_1m_chars": 0.0},  # Open source, self-hosted
    # Default
    "default": {"per_1m_chars": 15.0},
}

# LLM pricing per 1M tokens (input/output)
LLM_PRICING: dict[str, dict[str, float]] = {
    # OpenAI
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "gpt-4o-realtime": {"input": 5.00, "output": 20.00},
    "gpt-4-turbo": {"input": 10.00, "output": 30.00},
    "gpt-4": {"input": 30.00, "output": 60.00},
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    # Anthropic
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "claude-3-5-haiku": {"input": 1.00, "output": 5.00},
    "claude-3-opus": {"input": 15.00, "output": 75.00},
    "claude-3-sonnet": {"input": 3.00, "output": 15.00},
    # Google
    "gemini-2.0-flash": {"input": 0.075, "output": 0.30},
    "gemini-1.5-pro": {"input": 1.25, "output": 5.00},
    "gemini-1.5-flash": {"input": 0.075, "output": 0.30},
    # Groq (fast inference)
    "llama-3.1-70b": {"input": 0.59, "output": 0.79},
    "llama-3.1-8b": {"input": 0.05, "output": 0.08},
    "mixtral-8x7b": {"input": 0.24, "output": 0.24},
    # Fireworks
    "fireworks-llama-3.1-70b": {"input": 0.90, "output": 0.90},
    # Together
    "together-llama-3.1-70b": {"input": 0.88, "output": 0.88},
    # Default
    "default": {"input": 2.00, "output": 8.00},
}


def get_stt_pricing(model_id: str | None) -> float:
    """
    Get STT pricing per minute of audio.

    Args:
        model_id: STT model identifier

    Returns:
        Price per minute in USD
    """
    if not model_id:
        return STT_PRICING["default"]["per_minute"]

    model_id_lower = model_id.lower()

    # Try exact match
    if model_id_lower in STT_PRICING:
        return STT_PRICING[model_id_lower]["per_minute"]

    # Try partial matches
    for key, pricing in STT_PRICING.items():
        if key in model_id_lower or model_id_lower in key:
            return pricing["per_minute"]

    return STT_PRICING["default"]["per_minute"]


def get_tts_pricing(model_id: str | None) -> float:
    """
    Get TTS pricing per 1M characters.

    Args:
        model_id: TTS model identifier

    Returns:
        Price per 1M characters in USD
    """
    if not model_id:
        return TTS_PRICING["default"]["per_1m_chars"]

    model_id_lower = model_id.lower()

    # Try exact match
    if model_id_lower in TTS_PRICING:
        return TTS_PRICING[model_id_lower]["per_1m_chars"]

    # Try partial matches
    for key, pricing in TTS_PRICING.items():
        if key in model_id_lower or model_id_lower in key:
            return pricing["per_1m_chars"]

    return TTS_PRICING["default"]["per_1m_chars"]


def get_llm_pricing(model_id: str | None) -> tuple[float, float]:
    """
    Get LLM pricing (input/output per 1M tokens).

    Args:
        model_id: LLM model identifier

    Returns:
        Tuple of (input_price, output_price) per 1M tokens
    """
    if not model_id:
        pricing = LLM_PRICING["default"]
        return pricing["input"], pricing["output"]

    model_id_lower = model_id.lower()

    # Try exact match
    if model_id_lower in LLM_PRICING:
        pricing = LLM_PRICING[model_id_lower]
        return pricing["input"], pricing["output"]

    # Try partial matches
    for key, pricing in LLM_PRICING.items():
        if key in model_id_lower or model_id_lower in key:
            return pricing["input"], pricing["output"]

    pricing = LLM_PRICING["default"]
    return pricing["input"], pricing["output"]


def calculate_stt_cost(
    model_id: str | None,
    audio_duration_seconds: float = 0,
) -> float:
    """
    Calculate STT cost.

    Args:
        model_id: STT model identifier
        audio_duration_seconds: Duration of audio in seconds

    Returns:
        Cost in USD
    """
    price_per_minute = get_stt_pricing(model_id)
    minutes = audio_duration_seconds / 60.0
    return minutes * price_per_minute


def calculate_tts_cost(
    model_id: str | None,
    characters: int = 0,
) -> float:
    """
    Calculate TTS cost.

    Args:
        model_id: TTS model identifier
        characters: Number of characters synthesized

    Returns:
        Cost in USD
    """
    price_per_1m = get_tts_pricing(model_id)
    return (characters / 1_000_000) * price_per_1m


def calculate_llm_cost(
    model_id: str | None,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> float:
    """
    Calculate LLM cost.

    Args:
        model_id: LLM model identifier
        input_tokens: Number of input tokens
        output_tokens: Number of output tokens

    Returns:
        Cost in USD
    """
    input_price, output_price = get_llm_pricing(model_id)
    input_cost = (input_tokens / 1_000_000) * input_price
    output_cost = (output_tokens / 1_000_000) * output_price
    return input_cost + output_cost


def calculate_turn_cost(
    stt_model: str | None = None,
    tts_model: str | None = None,
    llm_model: str | None = None,
    audio_duration_seconds: float = 0,
    tts_characters: int = 0,
    input_tokens: int = 0,
    output_tokens: int = 0,
) -> dict[str, float]:
    """
    Calculate total cost for a voice conversation turn.

    Args:
        stt_model: STT model identifier
        tts_model: TTS model identifier
        llm_model: LLM model identifier
        audio_duration_seconds: Duration of input audio
        tts_characters: Number of characters for TTS
        input_tokens: LLM input tokens
        output_tokens: LLM output tokens

    Returns:
        Dict with cost breakdown
    """
    stt_cost = calculate_stt_cost(stt_model, audio_duration_seconds)
    tts_cost = calculate_tts_cost(tts_model, tts_characters)
    llm_cost = calculate_llm_cost(llm_model, input_tokens, output_tokens)

    return {
        "stt_cost": stt_cost,
        "tts_cost": tts_cost,
        "llm_cost": llm_cost,
        "total_cost": stt_cost + tts_cost + llm_cost,
    }


class VoiceCostTracker:
    """
    Tracks costs across voice conversation turns.

    Provides per-service and per-model cost breakdown.
    """

    def __init__(self):
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
        """
        Add a turn's usage to the tracker.

        Returns:
            Dict with cost breakdown for this turn
        """
        costs = calculate_turn_cost(
            stt_model=stt_model,
            tts_model=tts_model,
            llm_model=llm_model,
            audio_duration_seconds=audio_duration_seconds,
            tts_characters=tts_characters,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
        )

        # Update totals
        self._stt_cost += costs["stt_cost"]
        self._tts_cost += costs["tts_cost"]
        self._llm_cost += costs["llm_cost"]
        self._total_cost += costs["total_cost"]

        self._total_audio_seconds += audio_duration_seconds
        self._total_tts_characters += tts_characters
        self._total_input_tokens += input_tokens
        self._total_output_tokens += output_tokens
        self._turn_count += 1

        # Track by model
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
        """Total cost in USD."""
        return self._total_cost

    @property
    def stt_cost(self) -> float:
        """Total STT cost in USD."""
        return self._stt_cost

    @property
    def tts_cost(self) -> float:
        """Total TTS cost in USD."""
        return self._tts_cost

    @property
    def llm_cost(self) -> float:
        """Total LLM cost in USD."""
        return self._llm_cost

    def get_costs_by_model(self) -> dict[str, dict[str, float]]:
        """Get cost breakdown by model."""
        return self._by_model.copy()

    def get_summary(self) -> dict[str, any]:
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
            "total_tokens": self._total_input_tokens + self._total_output_tokens,
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
