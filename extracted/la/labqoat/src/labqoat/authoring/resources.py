"""Portable compute resource declarations."""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
import re

from labqoat.json_document import JsonDocument


@dataclass(frozen=True, slots=True, kw_only=True)
class Resources:
    """Resource quantities and optional selectors for one worker or replica."""

    cpu_millicores: int = 1000
    memory_mb: int = 1024
    gpu_count: int = 0
    ephemeral_storage_mb: int | None = None
    gpu_memory_mb: int | None = None
    gpu_model: str | None = None
    exact: bool = False
    spot: bool = False

    def __post_init__(self) -> None:
        """Validate portable quantities; the owning environment checks enforceability."""
        self._quantity("cpu_millicores", self.cpu_millicores, 1)
        self._quantity("memory_mb", self.memory_mb, 1)
        self._quantity("gpu_count", self.gpu_count, 0)
        if self.ephemeral_storage_mb is not None:
            self._quantity("ephemeral_storage_mb", self.ephemeral_storage_mb, 1)
        if self.gpu_memory_mb is not None:
            self._quantity("gpu_memory_mb", self.gpu_memory_mb, 1)
        if not isinstance(self.exact, bool) or not isinstance(self.spot, bool):
            raise ValueError("exact and spot must be booleans")
        if self.spot and self.gpu_count == 0:
            raise ValueError("spot applies to GPU requests only")
        self._gpu_request()

    def _gpu_request(self) -> None:
        """Require constrained GPUs, reject GPU selectors on CPU requests and name model-neutral intent."""
        if self.gpu_model is not None:
            self._validate_gpu_model()
        constrained = self.gpu_model is not None or self.gpu_memory_mb is not None
        if constrained != (self.gpu_count > 0):
            raise ValueError("GPU requests require a positive count and a model or minimum per-device memory")
        if constrained and self.gpu_model is None:
            object.__setattr__(self, "gpu_model", "any")

    def _validate_gpu_model(self) -> None:
        """Wildcard selection requires a memory floor; other values name concrete hardware."""
        expected = "gpu must be a bare model name from `lab compute offerings`, such as 't4' or 'h100', or 'any'"
        if not isinstance(self.gpu_model, str):
            raise ValueError(f"{expected}; got {self.gpu_model!r}")
        model = self.gpu_model.strip().lower().replace(" ", "-")
        if model in ("cheapest", "close") or re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", model) is None:
            raise ValueError(f"{expected}; got {self.gpu_model!r}")
        if model == "any" and self.gpu_memory_mb is None:
            raise ValueError("gpu='any' requires gpu_memory (minimum per-device MiB)")

    @staticmethod
    def _quantity(name: str, value: int, minimum: int) -> None:
        """Reject booleans, nonintegers, and quantities below their semantic minimum."""
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{name} must be an integer")
        if value < minimum:
            raise ValueError(f"{name} must be at least {minimum}")

    def to_dict(self) -> JsonDocument:
        """Return the canonical API resource mapping."""
        document = JsonDocument({"cpu_millicores": self.cpu_millicores, "memory_mb": self.memory_mb})
        if self.gpu_count > 0:
            document["gpu_count"] = self.gpu_count
        optional = {
            "ephemeral_storage_mb": self.ephemeral_storage_mb,
            "gpu_memory_mb": self.gpu_memory_mb,
            "gpu_model": self.gpu_model,
        }
        for name, value in optional.items():
            if value is not None:
                document[name] = value
        if self.exact:
            document["exact"] = True
        if self.spot:
            document["spot"] = True
        return document

    @classmethod
    def from_value(cls, value: object) -> Resources:
        """Normalize an existing typed declaration or mapping."""
        if isinstance(value, cls):
            return value
        if not isinstance(value, Mapping):
            raise ValueError("resources must be a mapping")
        unknown = set(value) - {
            "cpu_millicores",
            "memory_mb",
            "gpu_count",
            "ephemeral_storage_mb",
            "gpu_memory_mb",
            "gpu_model",
            "exact",
            "spot",
        }
        if unknown:
            raise ValueError(f"unsupported resource fields: {', '.join(sorted(str(item) for item in unknown))}")
        return cls(
            cpu_millicores=value.get("cpu_millicores", 1000),
            memory_mb=value.get("memory_mb", 1024),
            gpu_count=value.get("gpu_count", 0),
            ephemeral_storage_mb=value.get("ephemeral_storage_mb"),
            gpu_memory_mb=value.get("gpu_memory_mb"),
            gpu_model=value.get("gpu_model"),
            exact=value.get("exact", False),
            spot=value.get("spot", False),
        )
