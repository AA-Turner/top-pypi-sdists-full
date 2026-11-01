"""Build every client view of the records: the SDK's Python models and packages/core's TypeScript."""

from .codegen import TARGETS, Codegen, Target, main

__all__ = ["TARGETS", "Codegen", "Target", "main"]
