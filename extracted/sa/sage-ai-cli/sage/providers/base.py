"""Provider base types (minimal recovery skeleton)."""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass


@dataclass
class Message:
    role: str
    content: str


@dataclass
class ModelInfo:
    id: str
    provider: str
    name: str
    local: bool = False
    description: str = ""
    pros: str = ""
    cons: str = ""


class ProviderBase:
    name: str = "base"

    def is_available(self) -> bool:
        return False

    def list_models(self) -> list[ModelInfo]:
        return []

    def generate(self, messages, model="", temperature=0.7, max_tokens=2048):
        raise NotImplementedError

    def stream(self, messages, model="", temperature=0.7, max_tokens=2048):
        raise NotImplementedError
