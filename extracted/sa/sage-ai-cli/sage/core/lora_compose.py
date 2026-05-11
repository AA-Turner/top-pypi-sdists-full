"""Item #13 — Per-task LoRA composition."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

__all__ = ["AdapterStack", "compose_adapters"]


@dataclass
class AdapterStack:
    adapters: list[Path] = field(default_factory=list)


def compose_adapters(*,
                     project_adapter: Path | None = None,
                     style_adapter: Path | None = None,
                     framework_adapter: Path | None = None) -> AdapterStack:
    adapters: list[Path] = []
    for a in (project_adapter, style_adapter, framework_adapter):
        if a is not None:
            adapters.append(a)
    return AdapterStack(adapters=adapters)
