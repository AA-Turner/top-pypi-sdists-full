from __future__ import annotations

from dataclasses import dataclass, field
from math import isfinite
from typing import Any, Literal

Acceleration = Literal["auto", "pytorch", "tensorrt"]
RequestedControl = Literal[
    "auto",
    "adaptive",
    "prefer_freshness",
    "balanced",
    "prefer_robustness",
    "ultra_aggressive",
]
Control = Literal[
    "adaptive",
    "prefer_freshness",
    "balanced",
    "prefer_robustness",
    "ultra_aggressive",
]
# "on" asks for the model's own RTC; "inference_time" and "train_time" ask for one kind.
Rtc = Literal["auto", "off", "on", "inference_time", "train_time"]
RtcMode = Literal["off", "inference_time", "train_time"]
RequestedCalibration = Literal[
    "auto", "off", "fast", "default", "rtc_graph", "extended"
]
Calibration = Literal["off", "fast", "default", "rtc_graph", "extended"]
Backend = Literal["pytorch", "tensorrt", "jax"]
ResolvedRtc = Literal["off", "on"]
ShapeMode = Literal["bucketed", "exact", "off"]
QueueStrategy = Literal["method_o", "method_p"]

_ACCELERATION_VALUES = frozenset(("auto", "pytorch", "tensorrt"))
_CONTROL_VALUES = frozenset(
    ("adaptive", "prefer_freshness", "balanced", "prefer_robustness", "ultra_aggressive")
)
_REQUESTED_CONTROL_VALUES = _CONTROL_VALUES | {"auto"}
RTC_KINDS = frozenset(("inference_time", "train_time"))
_RTC_VALUES = frozenset(("auto", "off", "on")) | RTC_KINDS
_RTC_MODE_VALUES = frozenset(("off",)) | RTC_KINDS
# The RTC kind each wire contract serves (control plane capabilities.RTC_CONTRACT_KINDS).
RTC_CONTRACT_KINDS: dict[str, str] = {
    "isaac05_late_bound_prefix_v1": "train_time",
    "dynamic_full_horizon_v1": "inference_time",
    "fixed_ratio_v1": "inference_time",
    "calibrated_static": "inference_time",
}
_CALIBRATION_VALUES = frozenset(("off", "fast", "default", "rtc_graph", "extended"))
_REQUESTED_CALIBRATION_VALUES = _CALIBRATION_VALUES | {"auto"}
_BACKEND_VALUES = frozenset(("pytorch", "tensorrt", "jax"))
_RESOLVED_RTC_VALUES = frozenset(("off", "on"))
_SHAPE_MODE_VALUES = frozenset(("bucketed", "exact", "off"))
_QUEUE_STRATEGY_VALUES = frozenset(("method_o", "method_p"))


def _require_value(field_name: str, value: str, valid: frozenset[str]) -> None:
    if value not in valid:
        allowed = ", ".join(sorted(valid))
        raise ValueError(f"{field_name} must be one of {allowed}")


@dataclass(frozen=True)
class OptimizationConfig:
    acceleration: Acceleration | None = "auto"
    control: RequestedControl | None = "auto"
    rtc: Rtc | None = "auto"
    calibration: RequestedCalibration | None = "auto"

    def __post_init__(self) -> None:
        acceleration = "auto" if self.acceleration is None else self.acceleration
        control = "auto" if self.control is None else self.control
        rtc = "auto" if self.rtc is None else self.rtc
        calibration = "auto" if self.calibration is None else self.calibration
        _require_value("acceleration", acceleration, _ACCELERATION_VALUES)
        _require_value("control", control, _REQUESTED_CONTROL_VALUES)
        _require_value("rtc", rtc, _RTC_VALUES)
        _require_value("calibration", calibration, _REQUESTED_CALIBRATION_VALUES)
        object.__setattr__(self, "acceleration", acceleration)
        object.__setattr__(self, "control", control)
        object.__setattr__(self, "rtc", rtc)
        object.__setattr__(self, "calibration", calibration)

    @classmethod
    def from_wire(cls, data: dict[str, Any] | None) -> OptimizationConfig:
        if data is None:
            return cls()
        return cls(
            acceleration=data.get("acceleration", "auto"),
            control=data.get("control", "auto"),
            rtc=data.get("rtc", "auto"),
            calibration=data.get("calibration", "auto"),
        )

    def to_wire(self) -> dict[str, str]:
        return {
            "acceleration": str(self.acceleration),
            "control": str(self.control),
            "rtc": str(self.rtc),
            "calibration": str(self.calibration),
        }


@dataclass(frozen=True)
class ResolvedOptimizationConfig:
    backend: Backend = "pytorch"
    control: Control | Literal["balanced"] = "balanced"
    rtc: ResolvedRtc = "off"
    calibration: Calibration = "default"
    rtc_contract: str | None = None
    shape_mode: ShapeMode = "bucketed"
    cuda_graph: bool = False
    queue_strategy: QueueStrategy = "method_o"
    capability_fingerprint: str = "backend=pytorch;rtc=off;shape=bucketed"
    tensorrt_artifact_fingerprint: str | None = None
    tensorrt_artifact_id: str | None = None
    warnings: tuple[str, ...] = field(default_factory=tuple)
    action_hz: float | None = None
    chunk_size: int | None = None
    action_dim: int | None = None
    action_space: str | None = None
    hold_behavior: str | None = None
    execution_horizon: int | None = None
    # The served RTC kind, when the server reports it (absent from older servers and
    # while RTC is off); see effective_rtc_mode.
    rtc_mode: RtcMode | None = None

    def __post_init__(self) -> None:
        _require_value("backend", self.backend, _BACKEND_VALUES)
        _require_value("control", self.control, _CONTROL_VALUES)
        _require_value("rtc", self.rtc, _RESOLVED_RTC_VALUES)
        if self.rtc_mode is not None:
            _require_value("rtc_mode", self.rtc_mode, _RTC_MODE_VALUES)
        _require_value("calibration", self.calibration, _CALIBRATION_VALUES)
        _require_value("shape_mode", self.shape_mode, _SHAPE_MODE_VALUES)
        _require_value("queue_strategy", self.queue_strategy, _QUEUE_STRATEGY_VALUES)
        object.__setattr__(self, "warnings", tuple(str(warning) for warning in self.warnings))
        if self.action_hz is not None and (
            not isfinite(float(self.action_hz)) or float(self.action_hz) <= 0.0
        ):
            raise ValueError("action_hz must be finite and positive when provided")
        if self.chunk_size is not None and int(self.chunk_size) <= 0:
            raise ValueError("chunk_size must be positive when provided")
        if self.execution_horizon is not None and (
            type(self.execution_horizon) is not int
            or type(self.chunk_size) is not int
            or not 1 <= self.execution_horizon <= self.chunk_size
        ):
            raise ValueError("execution_horizon must be an integer from 1 to chunk_size")
        if self.action_dim is not None and int(self.action_dim) <= 0:
            raise ValueError("action_dim must be positive when provided")

    @classmethod
    def from_wire(cls, data: dict[str, Any] | None) -> ResolvedOptimizationConfig:
        if data is None:
            return cls()
        return cls(
            backend=data.get("backend", "pytorch"),
            control=data.get("control", "balanced"),
            rtc=data.get("rtc", "off"),
            calibration=data.get("calibration", "default"),
            rtc_contract=data.get("rtc_contract"),
            shape_mode=data.get("shape_mode", "bucketed"),
            cuda_graph=bool(data.get("cuda_graph", False)),
            queue_strategy=data.get("queue_strategy", "method_o"),
            capability_fingerprint=data.get(
                "capability_fingerprint", "backend=pytorch;rtc=off;shape=bucketed"
            ),
            tensorrt_artifact_fingerprint=data.get("tensorrt_artifact_fingerprint"),
            tensorrt_artifact_id=data.get("tensorrt_artifact_id"),
            warnings=tuple(data.get("warnings") or ()),
            action_hz=data.get("action_hz"),
            chunk_size=data.get("chunk_size"),
            action_dim=data.get("action_dim"),
            action_space=data.get("action_space"),
            hold_behavior=data.get("hold_behavior"),
            execution_horizon=data.get("execution_horizon"),
            # A kind this SDK does not know yet is dropped, never fatal.
            rtc_mode=(
                data.get("rtc_mode") if data.get("rtc_mode") in _RTC_MODE_VALUES else None
            ),
        )

    @property
    def effective_rtc_mode(self) -> str | None:
        """off, inference_time or train_time; None for an RTC contract this SDK does not know."""
        if self.rtc != "on":
            return "off"
        if self.rtc_mode is not None:
            return self.rtc_mode
        return RTC_CONTRACT_KINDS.get(self.rtc_contract or "")

    def to_wire(self) -> dict[str, Any]:
        result = {
            "backend": self.backend,
            "control": self.control,
            "rtc": self.rtc,
            "calibration": self.calibration,
            "rtc_contract": self.rtc_contract,
            "shape_mode": self.shape_mode,
            "cuda_graph": self.cuda_graph,
            "queue_strategy": self.queue_strategy,
            "capability_fingerprint": self.capability_fingerprint,
            "tensorrt_artifact_fingerprint": self.tensorrt_artifact_fingerprint,
            "tensorrt_artifact_id": self.tensorrt_artifact_id,
            "warnings": list(self.warnings),
            "action_hz": self.action_hz,
            "chunk_size": self.chunk_size,
            "action_dim": self.action_dim,
            "action_space": self.action_space,
            "hold_behavior": self.hold_behavior,
        }
        if self.execution_horizon is not None:
            result["execution_horizon"] = self.execution_horizon
        if self.rtc_mode is not None:
            result["rtc_mode"] = self.rtc_mode
        return result
