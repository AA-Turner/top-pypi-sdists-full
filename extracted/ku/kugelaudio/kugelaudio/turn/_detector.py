"""VAD-gated endpointing policy over the shared ONNX predictor."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from threading import RLock
import time
from typing import Literal, Protocol

import numpy as np
from numpy.typing import NDArray

from ._bundle import DEFAULT_REPO_ID, DEFAULT_REVISION, download_bundle
from ._runtime import TurnPredictor, TurnProbabilities
from ._schema import LanguagePolicy, TurnPolicy, load_schema
from .errors import (
    TurnAudioError,
    TurnBundleError,
    TurnStateError,
    UnsupportedTurnLanguageError,
)

TurnLanguage = Literal["de", "en", "es", "it", "nl"]


class ProbabilityPredictor(Protocol):
    """Inference boundary used by independent conversation sessions."""

    def predict_proba(
        self,
        audio: NDArray[np.float32],
        *,
        transcript: str = "",
        sample_rate: int = 16000,
    ) -> TurnProbabilities: ...


class TurnDecisionReason(str, Enum):
    """Machine-readable reason for an endpoint-policy result."""

    INSUFFICIENT_SILENCE = "insufficient_silence"
    EVIDENCE_CHANGED = "evidence_changed"
    MODEL_ACTION_DELAY = "model_action_delay"
    MODEL_HOLD = "model_hold"
    MODEL_COMPLETE = "model_complete"
    TIMEOUT = "timeout"


@dataclass(frozen=True, slots=True)
class TurnDecision:
    """One endpoint-policy result for the current silence span."""

    end_turn: bool
    reason: TurnDecisionReason
    silence_ms: int
    probabilities: TurnProbabilities | None = None
    inference_ms: float | None = None
    transcript: str = ""
    threshold: float | None = None


class TurnDetector:
    """One loaded model shared by independent per-conversation sessions."""

    def __init__(
        self,
        predictor: ProbabilityPredictor,
        policy: TurnPolicy,
        *,
        variant_path: str,
    ) -> None:
        if policy.model != variant_path:
            raise TurnBundleError(
                f"policy targets {policy.model!r}, but loaded variant is {variant_path!r}"
            )
        self.predictor = predictor
        self.policy = policy
        self.variant_path = variant_path

    @classmethod
    def from_pretrained(
        cls,
        *,
        repo_id: str = DEFAULT_REPO_ID,
        variant: str = "recommended",
        revision: str = DEFAULT_REVISION,
        token: str | bool | None = None,
        cache_dir: str | Path | None = None,
        local_files_only: bool = False,
        cpu_threads: int = 4,
    ) -> "TurnDetector":
        """Acquire the immutable model revision and load one shared CPU runtime."""
        downloaded = download_bundle(
            repo_id=repo_id,
            variant=variant,
            revision=revision,
            token=token,
            cache_dir=cache_dir,
            local_files_only=local_files_only,
        )
        policy = load_schema(downloaded.policy_path, TurnPolicy)
        predictor = TurnPredictor.from_verified_bundle(
            downloaded.bundle, cpu_threads=cpu_threads
        )
        return cls(predictor, policy, variant_path=downloaded.variant_path)

    def create_session(
        self,
        language: TurnLanguage,
        *,
        action_delay_ms: int | None = None,
        timeout_ms: int = 10_000,
    ) -> "TurnSession":
        """Create cheap conversation state while sharing the loaded model weights.

        ``action_delay_ms`` overrides the calibrated delay for applications that
        prefer committing a confident completion as soon as the first score is
        available. ``timeout_ms`` is the fallback for turns the model does not
        classify as complete and defaults to ten seconds.
        """
        try:
            language_policy = self.policy.languages[language]
        except KeyError as exc:
            raise UnsupportedTurnLanguageError(
                f"unsupported turn-detection language {language!r}; "
                f"available: {', '.join(sorted(self.policy.languages))}"
            ) from exc
        effective_action_delay_ms = (
            language_policy.action_delay_ms
            if action_delay_ms is None
            else action_delay_ms
        )
        if effective_action_delay_ms < self.policy.score_after_silence_ms:
            raise TurnStateError(
                "action_delay_ms cannot precede score_after_silence_ms: "
                f"{effective_action_delay_ms} < {self.policy.score_after_silence_ms}"
            )
        if timeout_ms <= 0:
            raise TurnStateError(f"timeout_ms must be positive, got {timeout_ms}")
        if timeout_ms < effective_action_delay_ms:
            raise TurnStateError(
                "timeout_ms cannot precede action_delay_ms: "
                f"{timeout_ms} < {effective_action_delay_ms}"
            )
        language_policy = language_policy.model_copy(
            update={
                "action_delay_ms": effective_action_delay_ms,
                "timeout_ms": timeout_ms,
            }
        )
        return TurnSession(
            self.predictor,
            language_policy,
            score_after_silence_ms=self.policy.score_after_silence_ms,
        )


class TurnSession:
    """Audio, transcript, and endpoint state for one live user turn."""

    def __init__(
        self,
        predictor: ProbabilityPredictor,
        policy: LanguagePolicy,
        *,
        score_after_silence_ms: int,
    ) -> None:
        self._predictor = predictor
        self._policy = policy
        self._score_after_silence_ms = score_after_silence_ms
        self._sample_rate = 16000
        self._window_samples = 128000
        self._audio = np.empty(0, dtype=np.float32)
        self._transcript = ""
        self._scored_transcript = ""
        self._last_silence_ms = 0
        self._probabilities: TurnProbabilities | None = None
        self._model_complete = False
        self._ended = False
        self._evidence_version = 0
        self._silence_version = 0
        self._lock = RLock()

    @property
    def has_audio(self) -> bool:
        """Whether the active turn contains audio evidence that can be scored."""
        with self._lock:
            return self._audio.size > 0

    def push_audio(
        self,
        audio: NDArray[np.float32],
        *,
        sample_rate: int = 16000,
    ) -> None:
        """Append explicitly normalized mono float32 PCM to the rolling window."""
        array = _validate_audio_chunk(audio, sample_rate=sample_rate)
        with self._lock:
            self._ensure_active()
            combined = np.concatenate((self._audio, array))
            self._audio = np.ascontiguousarray(combined[-self._window_samples :])

    def push_pcm16(self, pcm: bytes, *, sample_rate: int = 16000) -> None:
        """Explicitly decode little-endian signed PCM16 into normalized float32."""
        if not pcm:
            raise TurnAudioError("PCM16 audio must contain at least one sample")
        if len(pcm) % 2:
            raise TurnAudioError(f"PCM16 byte length must be even, got {len(pcm)}")
        audio = np.frombuffer(pcm, dtype="<i2").astype(np.float32) / 32768.0
        self.push_audio(audio, sample_rate=sample_rate)

    def update_transcript(self, transcript: str) -> None:
        """Replace the live ASR transcript without invalidating an active score."""
        with self._lock:
            self._ensure_active()
            self._transcript = transcript

    def observe_silence(self, duration_ms: int) -> TurnDecision:
        """Evaluate one monotonically increasing VAD silence duration."""
        return self._observe_silence(duration_ms, reset_on_end=False)

    def observe_silence_and_reset(self, duration_ms: int) -> TurnDecision:
        """Evaluate silence and atomically reset when the policy ends the turn."""
        return self._observe_silence(duration_ms, reset_on_end=True)

    def _observe_silence(
        self,
        duration_ms: int,
        *,
        reset_on_end: bool,
    ) -> TurnDecision:
        with self._lock:
            self._ensure_active()
            if duration_ms < 0:
                raise TurnStateError(
                    f"duration_ms must be non-negative, got {duration_ms}"
                )
            if duration_ms < self._last_silence_ms:
                raise TurnStateError(
                    f"silence duration moved backwards: {duration_ms} < {self._last_silence_ms}; "
                    "call speech_resumed() when VAD detects speech"
                )
            self._last_silence_ms = duration_ms
            if duration_ms < self._score_after_silence_ms:
                return TurnDecision(
                    False,
                    TurnDecisionReason.INSUFFICIENT_SILENCE,
                    duration_ms,
                    transcript=self._transcript,
                    threshold=self._policy.threshold,
                )
            if self._probabilities is not None:
                decision = self._evaluate_cached_decision(duration_ms)
                if reset_on_end and decision.end_turn:
                    self._reset_turn_locked()
                return decision
            if self._audio.size == 0:
                raise TurnAudioError(
                    "cannot score a turn before push_audio() or push_pcm16()"
                )
            audio = self._audio
            transcript = self._transcript
            evidence_version = self._evidence_version
            silence_version = self._silence_version

        inference_started_at = time.perf_counter()
        probabilities = self._predictor.predict_proba(
            audio,
            transcript=transcript,
            sample_rate=self._sample_rate,
        )
        inference_ms = (time.perf_counter() - inference_started_at) * 1000

        with self._lock:
            if (
                evidence_version != self._evidence_version
                or silence_version != self._silence_version
            ):
                return TurnDecision(
                    False,
                    TurnDecisionReason.EVIDENCE_CHANGED,
                    duration_ms,
                    inference_ms=inference_ms,
                    transcript=self._transcript,
                    threshold=self._policy.threshold,
                )
            self._ensure_active()
            self._probabilities = probabilities
            self._scored_transcript = transcript
            self._model_complete = probabilities.complete >= self._policy.threshold
            decision = self._evaluate_cached_decision(
                duration_ms,
                inference_ms=inference_ms,
            )
            if reset_on_end and decision.end_turn:
                self._reset_turn_locked()
            return decision

    def _evaluate_cached_decision(
        self,
        duration_ms: int,
        *,
        inference_ms: float | None = None,
    ) -> TurnDecision:
        """Evaluate timing for a score while ``self._lock`` is held."""
        if self._probabilities is None:
            raise TurnStateError(
                "cannot evaluate endpoint timing without a model score"
            )
        if self._model_complete:
            if duration_ms >= self._policy.action_delay_ms:
                self._ended = True
                return TurnDecision(
                    True,
                    TurnDecisionReason.MODEL_COMPLETE,
                    duration_ms,
                    self._probabilities,
                    inference_ms,
                    self._scored_transcript,
                    self._policy.threshold,
                )
            return TurnDecision(
                False,
                TurnDecisionReason.MODEL_ACTION_DELAY,
                duration_ms,
                self._probabilities,
                inference_ms,
                self._scored_transcript,
                self._policy.threshold,
            )
        if duration_ms >= self._policy.timeout_ms:
            self._ended = True
            return TurnDecision(
                True,
                TurnDecisionReason.TIMEOUT,
                duration_ms,
                self._probabilities,
                inference_ms,
                self._scored_transcript,
                self._policy.threshold,
            )
        return TurnDecision(
            False,
            TurnDecisionReason.MODEL_HOLD,
            duration_ms,
            self._probabilities,
            inference_ms,
            self._scored_transcript,
            self._policy.threshold,
        )

    def speech_resumed(self) -> None:
        """Cancel a pending endpoint while retaining the current turn context."""
        with self._lock:
            self._ensure_active()
            self._last_silence_ms = 0
            self._probabilities = None
            self._scored_transcript = ""
            self._model_complete = False
            self._silence_version += 1

    def _ensure_active(self) -> None:
        if self._ended:
            raise TurnStateError(
                "turn already ended; call reset_turn() before processing the next user turn"
            )

    def reset_turn(self) -> None:
        """Clear all conversation state after handing the completed turn downstream."""
        with self._lock:
            self._reset_turn_locked()

    def _reset_turn_locked(self) -> None:
        self._audio = np.empty(0, dtype=np.float32)
        self._transcript = ""
        self._scored_transcript = ""
        self._last_silence_ms = 0
        self._probabilities = None
        self._model_complete = False
        self._ended = False
        self._evidence_version += 1
        self._silence_version += 1


def _validate_audio_chunk(
    audio: NDArray[np.float32], *, sample_rate: int
) -> NDArray[np.float32]:
    """Reject implicit resampling, downmixing, clipping, or dtype conversion."""
    array = np.asarray(audio)
    if array.dtype != np.float32:
        raise TurnAudioError(f"audio dtype must be float32, got {array.dtype}")
    if array.ndim != 1:
        raise TurnAudioError(
            f"audio must be mono with shape [samples], got {array.shape}"
        )
    if array.size == 0:
        raise TurnAudioError("audio must contain at least one sample")
    if sample_rate != 16000:
        raise TurnAudioError(
            f"audio sample_rate must be 16000, got {sample_rate}; resample explicitly"
        )
    if not np.isfinite(array).all():
        raise TurnAudioError("audio contains NaN or infinite samples")
    peak = float(np.max(np.abs(array)))
    if peak > 1.0:
        raise TurnAudioError(
            f"float32 audio must be normalized to [-1, 1], peak={peak}"
        )
    return np.ascontiguousarray(array)
