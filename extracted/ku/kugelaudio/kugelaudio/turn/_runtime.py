"""NumPy preprocessing and qualified ONNX Runtime CPU inference."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Literal, Protocol, cast

import numpy as np
from numpy.typing import NDArray

from ._bundle import VerifiedBundle, verify_bundle
from ._schema import TurnModelConfig
from .errors import TurnAudioError, TurnBundleError, TurnDependencyError

FloatArray = NDArray[np.float32]
IntArray = NDArray[np.int64]


class OrtSession(Protocol):
    """Subset of ``onnxruntime.InferenceSession`` consumed by the SDK."""

    def run(
        self,
        output_names: list[str] | None,
        input_feed: dict[str, np.ndarray],
    ) -> list[np.ndarray]: ...


class FeatureBatch(Protocol):
    """NumPy output returned by ``WhisperFeatureExtractor``."""

    input_features: np.ndarray


class FeatureExtractor(Protocol):
    """Whisper feature-extraction call used by the runtime."""

    def __call__(
        self,
        raw_speech: list[FloatArray],
        *,
        sampling_rate: int,
        return_tensors: Literal["np"],
    ) -> FeatureBatch: ...


class Tokenizer(Protocol):
    """Tokenizer behavior required by the Qwen fusion graph."""

    padding_side: str
    truncation_side: str

    def apply_chat_template(
        self,
        conversation: Sequence[Mapping[str, str]],
        *,
        tokenize: bool,
        add_generation_prompt: bool,
    ) -> str: ...

    def __call__(
        self,
        text: list[str],
        *,
        add_special_tokens: bool,
        padding: bool,
        truncation: bool,
        max_length: int,
        return_tensors: Literal["np"],
    ) -> Mapping[str, np.ndarray]: ...


@dataclass(frozen=True, slots=True)
class TurnProbabilities:
    """Calibrated probabilities returned by the four-class model."""

    complete: float
    incomplete: float
    backchannel: float
    wait: float

    def as_dict(self) -> dict[str, float]:
        """Return the stable class-name mapping used for telemetry."""
        return {
            "complete": self.complete,
            "incomplete": self.incomplete,
            "backchannel": self.backchannel,
            "wait": self.wait,
        }


class TurnPredictor:
    """One shared, CPU-only predictor over a verified ONNX bundle."""

    def __init__(
        self,
        bundle: VerifiedBundle,
        tokenizer: Tokenizer,
        feature_extractor: FeatureExtractor,
        audio_session: OrtSession,
        fusion_session: OrtSession,
    ) -> None:
        self.bundle = bundle
        self.config = bundle.config
        self.tokenizer = tokenizer
        self.feature_extractor = feature_extractor
        self.audio_session = audio_session
        self.fusion_session = fusion_session
        self.tokenizer.padding_side = "left"
        self.tokenizer.truncation_side = "left"

    @classmethod
    def from_bundle(
        cls,
        bundle_dir: str | Path,
        *,
        cpu_threads: int = 4,
    ) -> "TurnPredictor":
        """Verify and load a bundle using only ONNX's CPU execution provider."""
        return cls.from_verified_bundle(
            verify_bundle(bundle_dir), cpu_threads=cpu_threads
        )

    @classmethod
    def from_verified_bundle(
        cls,
        bundle: VerifiedBundle,
        *,
        cpu_threads: int = 4,
    ) -> "TurnPredictor":
        """Load already-verified model files into CPU sessions."""
        if cpu_threads <= 0:
            raise TurnBundleError(f"cpu_threads must be positive, got {cpu_threads}")
        if sys.version_info < (3, 11):
            raise TurnDependencyError(
                "Local turn detection requires Python 3.11 or newer for the "
                "qualified ONNX Runtime packages."
            )
        try:
            # RISK: MatMulNBits output shifts by ~0.3 probability points when
            # ONNX Runtime initializes without PyTorch's native CPU runtime in
            # the process. Quality gates used the PyTorch-loaded environment;
            # remove this import only after a full no-PyTorch requalification.
            import torch
            import onnxruntime as ort
            from transformers import AutoTokenizer, WhisperFeatureExtractor
        except ImportError as exc:
            raise TurnDependencyError(
                'Turn detection needs optional dependencies; install "kugelaudio[turn-detection]".'
            ) from exc

        _ = torch.__version__

        options = ort.SessionOptions()
        options.intra_op_num_threads = cpu_threads
        options.inter_op_num_threads = 1
        options.graph_optimization_level = ort.GraphOptimizationLevel.ORT_ENABLE_ALL
        providers = ["CPUExecutionProvider"]
        try:
            audio_session = cast(
                OrtSession,
                ort.InferenceSession(
                    str(bundle.path / "audio.onnx"), options, providers=providers
                ),
            )
            fusion_session = cast(
                OrtSession,
                ort.InferenceSession(
                    str(bundle.path / "fusion.onnx"), options, providers=providers
                ),
            )
            # Third-party factories are untyped; cast once at the boundary.
            tokenizer = cast(
                Tokenizer,
                AutoTokenizer.from_pretrained(
                    bundle.path / "tokenizer", local_files_only=True
                ),
            )
            feature_extractor = cast(
                FeatureExtractor,
                WhisperFeatureExtractor.from_pretrained(
                    bundle.path / "feature_extractor", local_files_only=True
                ),
            )
        except (OSError, RuntimeError, ValueError) as exc:
            raise TurnBundleError(
                f"failed to load ONNX bundle {bundle.path}: {exc}"
            ) from exc
        return cls(bundle, tokenizer, feature_extractor, audio_session, fusion_session)

    def predict_proba(
        self,
        audio: FloatArray,
        *,
        transcript: str = "",
        sample_rate: int = 16000,
    ) -> TurnProbabilities:
        """Score mono float32 PCM; padding/truncation follows the eight-second model contract."""
        window = _prepare_audio(audio, sample_rate=sample_rate, config=self.config)
        features = self.feature_extractor(
            [window], sampling_rate=self.config.sample_rate, return_tensors="np"
        )
        input_features = np.asarray(features.input_features, dtype=np.float32)
        frames = self.bundle.manifest.input_feature_frames
        if input_features.ndim != 3 or input_features.shape[-1] < frames:
            raise TurnBundleError(
                f"feature extractor returned shape {input_features.shape}; "
                f"bundle requires at least {frames} frames"
            )
        input_ids, attention_mask = _tokenize_transcript(
            self.tokenizer, transcript=transcript, config=self.config
        )
        audio_outputs = self.audio_session.run(
            None, {"input_features": input_features[..., :frames]}
        )
        if len(audio_outputs) != 1:
            raise TurnBundleError(
                f"audio graph returned {len(audio_outputs)} outputs; expected exactly one"
            )
        audio_embeds = np.asarray(audio_outputs[0], dtype=np.float32)
        fusion_outputs = self.fusion_session.run(
            None,
            {
                "input_ids": input_ids,
                "attention_mask": attention_mask,
                "audio_embeds": audio_embeds,
            },
        )
        if len(fusion_outputs) != 1:
            raise TurnBundleError(
                f"fusion graph returned {len(fusion_outputs)} outputs; expected exactly one"
            )
        logits = np.asarray(fusion_outputs[0], dtype=np.float32)
        expected_shape = (1, len(self.config.classes))
        if logits.shape != expected_shape:
            raise TurnBundleError(
                f"fusion graph returned logits {logits.shape}; expected {expected_shape}"
            )
        probabilities = _softmax(logits[0])
        return TurnProbabilities(*[float(value) for value in probabilities])


def _prepare_audio(
    audio: FloatArray,
    *,
    sample_rate: int,
    config: TurnModelConfig,
) -> FloatArray:
    """Validate and apply the model's documented rolling-window semantics."""
    array = np.asarray(audio)
    if array.dtype != np.float32:
        raise TurnAudioError(f"audio dtype must be float32, got {array.dtype}")
    if array.ndim != 1:
        raise TurnAudioError(
            f"audio must be mono with shape [samples], got {array.shape}"
        )
    if array.size == 0:
        raise TurnAudioError("audio must contain at least one sample")
    if sample_rate != config.sample_rate:
        raise TurnAudioError(
            f"audio sample_rate must be {config.sample_rate}, got {sample_rate}; "
            "resample explicitly before inference"
        )
    if not np.isfinite(array).all():
        raise TurnAudioError("audio contains NaN or infinite samples")
    peak = float(np.max(np.abs(array)))
    if peak > 1.0:
        raise TurnAudioError(
            f"float32 audio must be normalized to [-1, 1], peak={peak}"
        )
    samples = config.window_samples
    if array.size > samples:
        return np.ascontiguousarray(array[-samples:])
    if array.size < samples:
        return np.pad(array, (samples - array.size, 0)).astype(np.float32, copy=False)
    return np.ascontiguousarray(array)


def _tokenize_transcript(
    tokenizer: Tokenizer,
    *,
    transcript: str,
    config: TurnModelConfig,
) -> tuple[IntArray, IntArray]:
    """Apply the training-time single-user chat format and left truncation."""
    text = transcript.strip()
    if not text:
        empty = np.zeros((1, 0), dtype=np.int64)
        return empty, empty.copy()
    formatted = tokenizer.apply_chat_template(
        [{"role": "user", "content": text}],
        tokenize=False,
        add_generation_prompt=False,
    )
    encoded = tokenizer(
        [formatted],
        add_special_tokens=False,
        padding=True,
        truncation=True,
        max_length=config.max_text_tokens,
        return_tensors="np",
    )
    try:
        input_ids = np.asarray(encoded["input_ids"], dtype=np.int64)
        attention_mask = np.asarray(encoded["attention_mask"], dtype=np.int64)
    except KeyError as exc:
        raise TurnBundleError(
            f"tokenizer omitted required output {exc.args[0]!r}"
        ) from exc
    if input_ids.ndim != 2 or attention_mask.shape != input_ids.shape:
        raise TurnBundleError(
            f"tokenizer returned incompatible shapes ids={input_ids.shape}, "
            f"mask={attention_mask.shape}"
        )
    return input_ids, attention_mask


def _softmax(logits: FloatArray) -> FloatArray:
    """Numerically stable float32 softmax."""
    shifted = logits - np.max(logits)
    exponentials = np.exp(shifted).astype(np.float32, copy=False)
    denominator = float(np.sum(exponentials))
    if not np.isfinite(denominator) or denominator <= 0:
        raise TurnBundleError(f"invalid softmax denominator {denominator}")
    return exponentials / denominator
