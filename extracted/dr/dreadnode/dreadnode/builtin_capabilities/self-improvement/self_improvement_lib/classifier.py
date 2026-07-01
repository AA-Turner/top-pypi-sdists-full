"""Classify agent failures into kinds that inform self-improvement decisions."""

import enum
import re
from dataclasses import dataclass

from dreadnode.agents.events import GenerationError, ToolError


class FailureKind(enum.Enum):
    TOOL_MISUSE = "tool_misuse"
    TOOL_CRASH = "tool_crash"
    UNKNOWN_TOOL = "unknown_tool"
    GENERATION_FORMAT = "format"
    GENERATION_REFUSAL = "refusal"
    CONTEXT_OVERFLOW = "context"
    RATE_LIMIT = "rate_limit"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class ClassifiedFailure:
    kind: FailureKind
    message: str
    subject: str | None
    worth_learning_from: bool
    sample: str


_UNKNOWN_TOOL_PATTERNS = (
    re.compile(r"no tool named", re.IGNORECASE),
    re.compile(r"unknown tool", re.IGNORECASE),
    re.compile(r"tool .* not found", re.IGNORECASE),
)

_MISUSE_PATTERNS = (
    re.compile(r"missing required", re.IGNORECASE),
    re.compile(r"invalid argument", re.IGNORECASE),
    re.compile(r"validation error", re.IGNORECASE),
    re.compile(r"type error", re.IGNORECASE),
)


def classify_tool_error(event: ToolError) -> ClassifiedFailure:
    message = str(event.error)
    tool = event.tool_call.name
    for pattern in _UNKNOWN_TOOL_PATTERNS:
        if pattern.search(message):
            return ClassifiedFailure(FailureKind.UNKNOWN_TOOL, message, tool, True, message[:500])
    for pattern in _MISUSE_PATTERNS:
        if pattern.search(message):
            return ClassifiedFailure(FailureKind.TOOL_MISUSE, message, tool, True, message[:500])
    return ClassifiedFailure(FailureKind.TOOL_CRASH, message, tool, False, message[:500])


def classify_generation_error(event: GenerationError) -> ClassifiedFailure:
    message = str(event.error)
    model = event.generator.model if event.generator else None
    lower = message.lower()
    if "context" in lower and ("exceed" in lower or "too long" in lower or "token" in lower):
        return ClassifiedFailure(FailureKind.CONTEXT_OVERFLOW, message, model, False, message[:500])
    if "rate" in lower and "limit" in lower:
        return ClassifiedFailure(FailureKind.RATE_LIMIT, message, model, False, message[:500])
    if "invalid" in lower and ("format" in lower or "json" in lower):
        return ClassifiedFailure(FailureKind.GENERATION_FORMAT, message, model, True, message[:500])
    return ClassifiedFailure(FailureKind.UNKNOWN, message, model, False, message[:500])
