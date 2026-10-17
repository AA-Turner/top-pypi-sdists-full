"""Exact-token multi-turn rollout contracts and environment-local sidecar."""

from fireworks.training.sdk.tito._types import (
    TITOTurn,
    TITOError,
    TITORenderer,
    TITOCallRecord,
    TITOCallResult,
    TITOParseError,
    TITOPromptMode,
    TITOChatRequest,
    TITODistribution,
    TITOMetricSummary,
    TITOSegmentResult,
    TITOParsedAssistant,
    TITOResponseAttempt,
    TITOIncrementalPrompt,
    TrajectoryDriftPolicy,
    TITOTrajectoryArtifact,
    TITOTrajectoryEndpoint,
    TITOIncrementalRenderer,
    normalize_openai_tool_arguments,
)
from fireworks.training.sdk.tito._engine import TITOEventObserver
from fireworks.training.sdk.tito._sidecar import TITOSidecar
from fireworks.training.sdk.tito._failure_trace import TITOFailureTraceConfig, dump_tito_failure_trace

__all__ = [
    "TITOCallRecord",
    "TITOCallResult",
    "TITOChatRequest",
    "TITODistribution",
    "TITOError",
    "TITOParseError",
    "TITOFailureTraceConfig",
    "dump_tito_failure_trace",
    "TITOEventObserver",
    "TITOIncrementalPrompt",
    "TITOIncrementalRenderer",
    "TITOMetricSummary",
    "TITOParsedAssistant",
    "TITOPromptMode",
    "TITORenderer",
    "TITOResponseAttempt",
    "TITOSegmentResult",
    "TITOSidecar",
    "TITOTrajectoryEndpoint",
    "TITOTrajectoryArtifact",
    "TITOTurn",
    "TrajectoryDriftPolicy",
    "normalize_openai_tool_arguments",
]
