"""Strict schemas for externally supplied model and policy metadata."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Literal, TypeVar

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
    field_validator,
    model_validator,
)

from .errors import TurnBundleError

_HEX_64_PATTERN = r"^[0-9a-f]{64}$"
_SchemaT = TypeVar("_SchemaT", bound=BaseModel)


def _validate_relative_path(value: str) -> str:
    path = Path(value)
    if not value or path.is_absolute() or ".." in path.parts:
        raise ValueError("path must be safe and relative")
    return value


class BundleFile(BaseModel):
    """One checksummed file declared by an ONNX bundle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str
    size_bytes: int = Field(ge=0)
    sha256: str = Field(pattern=_HEX_64_PATTERN)

    _safe_path = field_validator("path")(_validate_relative_path)


class BundleManifest(BaseModel):
    """Versioned integrity boundary for a self-contained ONNX bundle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    format: Literal["kugel-turn-onnx"]
    schema_version: Literal[1]
    source_checkpoint_sha256: str = Field(pattern=_HEX_64_PATTERN)
    audio_precision: str = Field(min_length=1)
    fusion_precision: str = Field(min_length=1)
    algorithm: str = Field(min_length=1)
    input_feature_frames: int = Field(gt=0)
    files: tuple[BundleFile, ...] = Field(min_length=1)

    @model_validator(mode="after")
    def validate_declared_files(self) -> "BundleManifest":
        paths = [item.path for item in self.files]
        if len(paths) != len(set(paths)):
            raise ValueError("manifest contains duplicate file paths")
        required = {
            "audio.onnx",
            "config.json",
            "feature_extractor/preprocessor_config.json",
            "fusion.onnx",
            "tokenizer/tokenizer.json",
            "tokenizer/tokenizer_config.json",
        }
        missing = required - set(paths)
        if missing:
            raise ValueError(f"manifest omits required files: {sorted(missing)}")
        return self


class TurnModelConfig(BaseModel):
    """Architecture values consumed by the customer runtime."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    audio_encoder_name: str = Field(min_length=1)
    lm_name: str = Field(min_length=1)
    sample_rate: int = Field(gt=0)
    audio_window_s: float = Field(gt=0)
    encoder_frames_per_s: int = Field(gt=0)
    num_audio_tokens: int = Field(gt=0)
    audio_encoder_dim: int = Field(gt=0)
    whisper_input_frames: int = Field(gt=0)
    adapter_hidden_dim: int = Field(gt=0)
    lm_hidden_dim: int = Field(gt=0)
    max_text_tokens: int = Field(gt=0)
    classes: tuple[str, ...] = Field(min_length=2)

    @model_validator(mode="after")
    def validate_runtime_contract(self) -> "TurnModelConfig":
        expected_classes = ("complete", "incomplete", "backchannel", "wait")
        if self.classes != expected_classes:
            raise ValueError(
                f"unsupported class order {self.classes}; expected {expected_classes}"
            )
        if self.whisper_input_frames % 2:
            raise ValueError("whisper_input_frames must be even")
        return self

    @property
    def window_samples(self) -> int:
        """Number of mono samples in the rolling audio window."""
        return int(round(self.sample_rate * self.audio_window_s))


class VariantMetadata(BaseModel):
    """One downloadable entry in the Hugging Face variant index."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    path: str
    status: str = Field(min_length=1)
    audio_precision: str | None = None
    fusion_precision: str | None = None
    size_bytes: int | None = Field(default=None, ge=0)
    sha256: str | None = Field(default=None, pattern=_HEX_64_PATTERN)

    _safe_path = field_validator("path")(_validate_relative_path)


class VariantIndex(BaseModel):
    """Versioned index used to select a customer-safe bundle."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1]
    recommended: str
    variants: tuple[VariantMetadata, ...] = Field(min_length=1)

    _safe_recommended = field_validator("recommended")(_validate_relative_path)

    @model_validator(mode="after")
    def validate_recommended_variant(self) -> "VariantIndex":
        paths = [variant.path for variant in self.variants]
        if len(paths) != len(set(paths)):
            raise ValueError("variant index contains duplicate paths")
        if self.recommended not in paths:
            raise ValueError("recommended variant is absent from variants")
        return self

    def resolve(self, variant: str) -> VariantMetadata:
        """Resolve ``recommended`` or an exact indexed path without fallback."""
        requested = self.recommended if variant == "recommended" else variant
        for item in self.variants:
            if item.path == requested:
                if not item.path.startswith("onnx/"):
                    raise TurnBundleError(
                        f"variant {requested!r} is not an ONNX customer bundle"
                    )
                return item
        raise TurnBundleError(
            f"unknown turn-detection variant {variant!r}; available ONNX variants: "
            + ", ".join(
                item.path for item in self.variants if item.path.startswith("onnx/")
            )
        )


class LanguagePolicy(BaseModel):
    """One language's measured endpoint policy."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    threshold: float = Field(ge=0.0, le=1.0)
    action_delay_ms: int = Field(ge=0)
    timeout_ms: int = Field(gt=0)


class TurnPolicy(BaseModel):
    """Versioned policy paired with one exact model variant."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    schema_version: Literal[1]
    model: str
    preset: str = Field(min_length=1)
    score_after_silence_ms: int = Field(ge=0)
    end_turn_probability: Literal["complete"]
    languages: dict[Literal["de", "en", "es", "it", "nl"], LanguagePolicy]

    _safe_model = field_validator("model")(_validate_relative_path)

    @model_validator(mode="after")
    def validate_timing(self) -> "TurnPolicy":
        expected = {"de", "en", "es", "it", "nl"}
        if set(self.languages) != expected:
            raise ValueError(
                f"policy languages must be exactly {sorted(expected)}, "
                f"got {sorted(self.languages)}"
            )
        for language, policy in self.languages.items():
            if policy.action_delay_ms < self.score_after_silence_ms:
                raise ValueError(
                    f"{language} action_delay_ms precedes score_after_silence_ms"
                )
            if policy.timeout_ms < policy.action_delay_ms:
                raise ValueError(f"{language} timeout_ms precedes action_delay_ms")
        return self


def load_schema(path: Path, schema: type[_SchemaT]) -> _SchemaT:
    """Load and validate an external JSON file with a typed error boundary."""
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        return schema.model_validate(raw)
    except (OSError, json.JSONDecodeError, ValidationError) as exc:
        raise TurnBundleError(f"invalid {schema.__name__} at {path}: {exc}") from exc
