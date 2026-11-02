"""Framework-independent normalization of Lightning scalar values."""

import json
import math
import re
from argparse import Namespace
from collections.abc import Mapping


class LightningScalars:
    """Convert scalar tensors and metric names without importing Torch."""

    @staticmethod
    def parameter(value: object) -> str:
        """Encode hyperparameters as stable text."""
        try:
            return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True, allow_nan=False)
        except (TypeError, ValueError):
            return str(value)

    @staticmethod
    def metric(value: object) -> float | None:
        """Read finite Python or scalar tensor values."""
        selected = value
        if not isinstance(selected, int | float):
            item = getattr(selected, "item", None)
            if not callable(item):
                return None
            try:
                selected = item()
            except (RuntimeError, TypeError, ValueError):
                return None
        if isinstance(selected, bool) or not isinstance(selected, int | float):
            return None
        scalar = float(selected)
        if not math.isfinite(scalar):
            raise ValueError("Training metrics must be finite")
        return scalar

    @staticmethod
    def name(value: str) -> str:
        """Normalize hierarchical metric names for durable storage."""
        segments: list[str] = []
        for raw in value.strip().lower().split("/"):
            segment = re.sub(r"[^a-z0-9_.-]+", "_", raw).strip("_.-") or "metric"
            if not segment[0].isalpha():
                segment = f"metric_{segment}"
            segments.append(segment)
        return "/".join(segments)

    @staticmethod
    def parameters(value: object) -> dict[str, str]:
        """Normalize mappings and argparse namespaces into text parameters."""
        values = vars(value) if isinstance(value, Namespace) else value
        if not isinstance(values, Mapping):
            raise TypeError("Lightning hyperparameters must be a mapping or Namespace")
        return {str(name): LightningScalars.parameter(item) for name, item in values.items()}
