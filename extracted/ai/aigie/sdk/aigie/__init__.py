"""
Aigie SDK - Production-Grade AI Agent Infrastructure

95% of AI agents never reach production due to context drift, tool errors, and
runtime instability. Aigie provides the infrastructure that makes autonomous AI
reliable and production-grade.

Unlike traditional observability tools that only monitor, Aigie:
- DETECTS context drift and errors before they impact users
- FIXES issues automatically through self-healing workflows
- PREVENTS failures with predictive intervention

Core Features:
- @traceable decorator for automatic tracing
- LLM auto-instrumentation (OpenAI, Anthropic, Gemini)
- Token counting and cost tracking
- Prompt management with versioning
- Online evaluation scoring
- Context propagation for nested traces
- Streaming support for generators

Reliability Features (Unique to Aigie):
- Context drift detection
- Auto-error correction
- Production guardrails
- Self-healing workflows
- Reliability scoring

Usage:
    import aigie
    aigie.init("https://your-kytte-instance.com/api", "your-kytte-token")

    # Use decorator for automatic tracing
    @aigie.traceable(run_type="agent")
    async def my_agent(query: str):
        return await process(query)
"""

import sys
from typing import TYPE_CHECKING, Any

# Core exports (always available)
__all__ = [
    # Client
    "Aigie",
    "Config",
    "init",
    "shutdown",
    "get_aigie",
    "sdk_status",
    # Integration Registry (LiteLLM-style patching)
    "patch",
    "unpatch",
    "is_patched",
    "is_integration_available",
    "list_integrations",
    "list_integration_names",
    "get_patched_integrations",
    "register_integration",
    "patch_all",
    # Exceptions (comprehensive hierarchy)
    "AigieError",
    "ContextDriftDetected",
    "TopicDriftDetected",
    "BehaviorDriftDetected",
    "QualityDriftDetected",
    "RemediationFailed",
    "RemediationRejected",
    "RetryExhausted",
    "TraceBufferError",
    "TraceContextError",
    "InterceptionBlocked",
    "InterceptionRetryRequested",
    "ConfigurationError",
    "IntegrationError",
    "IntegrationNotFoundError",
    "IntegrationNotInstalledError",
    "BackendError",
    "BackendConnectionError",
    "RateLimitError",
    "AuthenticationError",
    "WebhookError",
    # Callbacks (LiteLLM-style)
    "GenericWebhookCallback",
    "BaseCallback",
    "CallbackEvent",
    "CallbackEventType",
    "create_webhook",
    # Context managers
    "TraceContext",
    "SpanContext",
    # Decorators (v3)
    "traceable",
    "trace",
    "create_traceable",
    "set_debug_mode",
    # Trace enrichment
    "get_current_trace",
    "update_current_trace",
    # Context propagation (new!)
    "tracing_context",
    "get_current_trace_context",
    "get_current_span_context",
    "is_tracing_enabled",
    "set_tracing_enabled",
    # Wrappers (new!)
    "wrap_openai",
    "wrap_anthropic",
    "wrap_gemini",
    "wrap_bedrock",
    "create_traced_bedrock",
    "wrap_cohere",
    "create_traced_cohere",
    # Unified Signal Reporter
    "SignalReporter",
    "Signal",
    "SignalBatch",
    "SignalMetrics",
    "SignalSeverity",
    "DriftType",
    "get_signal_reporter",
    "set_signal_reporter",
    # Health Monitor
    "HealthMonitor",
    "HealthStatus",
    "HealthConfig",
    "HealthMetrics",
    "DegradationLevel",
    "ServiceStatus",
    "ServiceHealth",
    "get_health_monitor",
    "set_health_monitor",
    # Compression
    "Compressor",
    "is_compression_available",
    # Buffer
    "EventBuffer",
    # W3C Trace Context
    "W3CTraceContext",
    "extract_trace_context",
    "inject_trace_context",
    # Evaluation
    "EvaluationResult",
    # Component-level evaluation (new!)
    "observe",
    # Streaming
    "StreamingSpan",
    # Evaluations API (NEW!)
    "EvaluationsClient",
    "EvaluationType",
    "EvaluationTemplate",
    "EvaluationScore",
    "EvaluationJob",
    "EvaluationRequest",
    "evaluate",
    # Judges API (NEW!)
    "JudgesClient",
    "JudgeType",
    "Judge",
    "JudgeResult",
    "JudgeConfig",
    "judge",
    "judge_all",
    # Datasets
    "DatasetsClient",
    "Dataset",
    "DatasetExample",
    "DatasetRunResult",
    "DatasetRunSummary",
    # Sessions
    "SessionManager",
    "SessionAnalytics",
    "Session",
    "SessionMessage",
    "create_session_manager",
    # Cost Tracking (Gap Fix)
    "extract_usage_from_response",
    "extract_and_calculate_cost",
    "calculate_cost",
    "add_model_pricing",
    "get_supported_models",
    "get_model_pricing",
    "CostAggregator",
    "UsageMetadata",
    "CostBreakdown",
    # Summary Evaluators (Gap Fix)
    "SummaryEvaluator",
    "AccuracySummaryEvaluator",
    "PrecisionSummaryEvaluator",
    "AverageScoreSummaryEvaluator",
    "PassRateSummaryEvaluator",
    "CostSummaryEvaluator",
    "LatencySummaryEvaluator",
    "run_summary_evaluators",
    "create_standard_summary_evaluators",
    "RunData",
    "SummaryEvaluationResult",
    "SummaryEvaluatorFunction",
    # Guardrails (SLA Production Runtime)
    "BaseGuardrail",
    "GuardrailChain",
    "GuardrailResult",
    "GuardrailAction",
    "GuardrailRemediationNeeded",
    "PIIDetector",
    "ToxicityDetector",
    "HallucinationDetector",
    "PromptInjectionDetector",
    # Pytest Integration (Gap Fix)
    "AigieTestCase",
    "aigie_assert",
    "assert_test",
    # UUID v7 (Gap Fix)
    "uuidv7",
    "extract_timestamp",
    "is_valid_uuidv7",
    "uuidv7_to_datetime",
    "compare_uuidv7",
    "generate_batch_uuidv7",
    "uuidv7_with_timestamp",
    "get_uuidv7_age",
    # Query API (Feature Parity)
    "QueryAPI",
    "TraceAPI",
    "ObservationsAPI",
    "SessionsAPI",
    "ScoresAPI",
    "Trace",
    "Observation",
    "ObservationType",
    "TraceFilter",
    "PaginatedResponse",
    # Human Annotations (Feature Parity)
    "AnnotationsAPI",
    "AnnotationQueue",
    "Annotation",
    "AnnotationType",
    "AnnotationTask",
    # Playground (Feature Parity)
    "Playground",
    "PromptRegistry",
    "PromptTemplate",
    "PlaygroundRun",
    "ComparisonResult",
    "ModelConfig",
    "ModelProvider",
    "create_playground",
    # Agent Graph View (Feature Parity)
    "AgentGraph",
    "GraphBuilder",
    "GraphNode",
    "GraphEdge",
    "NodeType",
    "EdgeType",
    "NodeStatus",
    "ExecutionPath",
    "GraphMetrics",
    "create_graph",
    "create_graph_builder",
    # Alerting (Feature Parity)
    "AlertManager",
    "AlertRule",
    "AlertEvent",
    "AlertCondition",
    "AlertSeverity",
    "AlertStatus",
    "MetricType",
    "ComparisonOperator",
    "AggregationWindow",
    "NotificationChannel",
    "SlackChannel",
    "EmailChannel",
    "WebhookChannel",
    "PagerDutyChannel",
    "create_alert_manager",
    # Span Replay (Feature Parity)
    "SpanReplay",
    "CapturedSpan",
    "ReplayResult",
    "ReplayExperiment",
    "ReplayStatus",
    "create_span_replay",
    # Leaderboards (Feature Parity)
    "LeaderboardManager",
    "Leaderboard",
    "LeaderboardEntry",
    "ComparisonPair",
    "EloRating",
    "RankingMetric",
    "AggregationType",
    "create_leaderboard_manager",
    "create_model_leaderboard",
    "create_prompt_leaderboard",
    # License Management (Self-Hosted)
    "LicenseValidator",
    "LicenseInfo",
    "UsageSummary",
    "LicenseError",
    "LicenseExpiredError",
    "LicenseRevokedError",
    "LicenseLimitExceededError",
    # Telemetry (SDK Feature Tracking)
    "track_feature",
    "record_error",
    "FeatureTracker",
    "ErrorCollector",
    # Agent Observability (new!)
    "LoopDetectedError",
    # Agent Framework
    "Agent",
    "RunContext",
    "Message",
    "ModelRetry",
    "get_current_context",
    "get_current_context_or_none",
    "set_current_context",
    "reset_current_context",
    "run_context",
    "AgentResult",
    "StreamedRunResult",
    "UsageInfo",
    "UnifiedError",
    "Tool",
    "ToolCall",
    "ToolResult",
    "ToolRegistry",
    "tool",
    "create_tool_registry",
    "execute_tool",
    "tools_to_openai_functions",
    "tools_to_anthropic_tools",
    "type_to_json_schema",
    "generate_json_schema",
    # Types (trace/span data structures)
    "TraceStatus",
    "SpanStatus",
    "SpanType",
    "ObservationLevel",
    "FailureCategory",
    "TokenUsage",
    "TraceResponse",
    "SpanResponse",
    # Platform API Clients
    "AnalyticsClient",
    "DashboardStats",
    "TimeSeriesPoint",
    "WorkflowStats",
    "ErrorSummary",
    "ErrorCluster",
    "CostAnalytics",
    "AgentStats",
    "WorkflowsClient",
    "WorkflowDefinition",
    "WorkflowExecution",
    "RecommendationsClient",
    "TraceRecommendation",
    "WorkflowRecommendation",
    "ImpactAnalysis",
    "LearningClient",
    "LearningStats",
    "LearningPattern",
    "FeedbackEntry",
    "EvalStats",
]

__version__ = "0.3.4"


# Lazy imports for performance
def __getattr__(name: str) -> Any:  # noqa: C901, PLR0911, PLR0912
    """
    Lazy import implementation for faster load times.

    Modules are only imported when actually used, reducing cold start penalty.
    """
    # Core client
    if name == "Aigie":
        from aigie.client import Aigie

        return Aigie

    if name == "Config":
        from aigie.config import Config

        return Config

    if name == "init":
        from aigie.client import init

        return init

    if name == "shutdown":
        from aigie.client import shutdown

        return shutdown

    if name == "get_aigie":
        from aigie.client import get_aigie

        return get_aigie

    if name == "sdk_status":

        def _sdk_status() -> dict:
            from aigie.client import get_aigie

            instance = get_aigie()
            if instance is None:
                return {
                    "initialized": False,
                    "error": "SDK not initialized. Call aigie.init() first.",
                }
            return instance.sdk_status()

        return _sdk_status

    # Context managers
    if name == "TraceContext":
        from aigie.trace import TraceContext

        return TraceContext

    if name == "SpanContext":
        from aigie.span import SpanContext

        return SpanContext

    if name == "no_retention":
        from aigie.tracing.retention import no_retention

        return no_retention

    if name == "no_retention_async":
        from aigie.tracing.retention import no_retention_async

        return no_retention_async

    # Decorators (v3)
    if name in ("traceable", "trace"):
        from aigie.decorators_v3 import traceable

        return traceable

    # Enhanced decorator utilities
    if name == "create_traceable":
        from aigie.decorators_v3 import create_traceable

        return create_traceable

    if name == "set_debug_mode":
        from aigie.decorators_v3 import set_debug_mode

        return set_debug_mode

    # Context propagation
    if name == "get_current_trace":
        from aigie.trace import get_current_trace

        return get_current_trace

    if name == "update_current_trace":
        from aigie.trace import update_current_trace

        return update_current_trace

    if name == "tracing_context":
        from aigie.context_manager import tracing_context

        return tracing_context

    if name == "get_current_trace_context":
        from aigie.context_manager import get_current_trace_context

        return get_current_trace_context

    if name == "get_current_span_context":
        from aigie.context_manager import get_current_span_context

        return get_current_span_context

    if name == "is_tracing_enabled":
        from aigie.context_manager import is_tracing_enabled

        return is_tracing_enabled

    if name == "set_tracing_enabled":
        from aigie.context_manager import set_tracing_enabled

        return set_tracing_enabled

    # Wrappers
    if name == "wrap_openai":
        from aigie.wrappers import wrap_openai

        return wrap_openai

    if name == "wrap_anthropic":
        from aigie.wrappers import wrap_anthropic

        return wrap_anthropic

    if name == "wrap_gemini":
        from aigie.wrappers import wrap_gemini

        return wrap_gemini

    if name == "wrap_bedrock":
        from aigie.wrappers_bedrock import wrap_bedrock

        return wrap_bedrock

    if name == "create_traced_bedrock":
        from aigie.wrappers_bedrock import create_traced_bedrock

        return create_traced_bedrock

    if name == "wrap_cohere":
        from aigie.wrappers_cohere import wrap_cohere

        return wrap_cohere

    if name == "create_traced_cohere":
        from aigie.wrappers_cohere import create_traced_cohere

        return create_traced_cohere

    # Unified Signal Reporter
    if name == "SignalReporter":
        from aigie.signals import SignalReporter

        return SignalReporter

    if name == "Signal":
        from aigie.signals import Signal

        return Signal

    if name == "SignalBatch":
        from aigie.signals import SignalBatch

        return SignalBatch

    if name == "SignalMetrics":
        from aigie.signals import SignalMetrics

        return SignalMetrics

    if name == "SignalSeverity":
        from aigie.signals import SignalSeverity

        return SignalSeverity

    if name == "DriftType":
        from aigie.signals import DriftType

        return DriftType

    if name == "get_signal_reporter":
        from aigie.signals import get_signal_reporter

        return get_signal_reporter

    if name == "set_signal_reporter":
        from aigie.signals import set_signal_reporter

        return set_signal_reporter

    # Health Monitor
    if name == "HealthMonitor":
        from aigie.health import HealthMonitor

        return HealthMonitor

    if name == "HealthStatus":
        from aigie.health import HealthStatus

        return HealthStatus

    if name == "HealthConfig":
        from aigie.health import HealthConfig

        return HealthConfig

    if name == "HealthMetrics":
        from aigie.health import HealthMetrics

        return HealthMetrics

    if name == "DegradationLevel":
        from aigie.health import DegradationLevel

        return DegradationLevel

    if name == "ServiceStatus":
        from aigie.health import ServiceStatus

        return ServiceStatus

    if name == "ServiceHealth":
        from aigie.health import ServiceHealth

        return ServiceHealth

    if name == "get_health_monitor":
        from aigie.health import get_health_monitor

        return get_health_monitor

    if name == "set_health_monitor":
        from aigie.health import set_health_monitor

        return set_health_monitor

    # Compression
    if name == "Compressor":
        from aigie.compression import Compressor

        return Compressor

    if name == "is_compression_available":
        from aigie.compression import is_compression_available

        return is_compression_available

    # Buffer
    if name == "EventBuffer":
        from aigie.buffer import EventBuffer

        return EventBuffer

    # W3C Trace Context
    if name == "W3CTraceContext":
        from aigie.context import TraceContext as W3CTraceContext

        return W3CTraceContext

    if name == "extract_trace_context":
        from aigie.context import extract_trace_context

        return extract_trace_context

    if name == "inject_trace_context":
        from aigie.context import inject_trace_context

        return inject_trace_context

    # Prompts
    # Evaluation
    if name == "EvaluationResult":
        from aigie.evaluation import EvaluationResult

        return EvaluationResult

    # Metrics (new!)
    # Component-level evaluation (new!)
    if name == "observe":
        from aigie.observe import observe

        return observe

    # Streaming
    if name == "StreamingSpan":
        from aigie.streaming import StreamingSpan

        return StreamingSpan

    # Evaluations API (NEW!)
    if name == "EvaluationsClient":
        from aigie.evaluations import EvaluationsClient

        return EvaluationsClient

    if name == "EvaluationType":
        from aigie.evaluations import EvaluationType

        return EvaluationType

    if name == "EvaluationTemplate":
        from aigie.evaluations import EvaluationTemplate

        return EvaluationTemplate

    if name == "EvaluationScore":
        from aigie.evaluations import EvaluationScore

        return EvaluationScore

    if name == "EvaluationJob":
        from aigie.evaluations import EvaluationJob

        return EvaluationJob

    if name == "EvaluationRequest":
        from aigie.evaluations import EvaluationRequest

        return EvaluationRequest

    if name == "evaluate":
        from aigie.evaluations import evaluate

        return evaluate

    # Judges API (NEW!)
    if name == "JudgesClient":
        from aigie.judges import JudgesClient

        return JudgesClient

    if name == "JudgeType":
        from aigie.judges import JudgeType

        return JudgeType

    if name == "Judge":
        from aigie.judges import Judge

        return Judge

    if name == "JudgeResult":
        from aigie.judges import JudgeResult

        return JudgeResult

    if name == "JudgeConfig":
        from aigie.judges import JudgeConfig

        return JudgeConfig

    if name == "judge":
        from aigie.judges import judge

        return judge

    if name == "judge_all":
        from aigie.judges import judge_all

        return judge_all

    # Phase 2: Datasets
    if name == "DatasetsClient":
        from aigie.datasets import DatasetsClient

        return DatasetsClient

    if name == "Dataset":
        from aigie.datasets import Dataset

        return Dataset

    if name == "DatasetExample":
        from aigie.datasets import DatasetExample

        return DatasetExample

    if name == "DatasetRunResult":
        from aigie.datasets import DatasetRunResult

        return DatasetRunResult

    if name == "DatasetRunSummary":
        from aigie.datasets import DatasetRunSummary

        return DatasetRunSummary

    # Phase 2: Sessions
    if name == "SessionManager":
        from aigie.sessions import SessionManager

        return SessionManager

    if name == "SessionAnalytics":
        from aigie.sessions import SessionAnalytics

        return SessionAnalytics

    if name == "Session":
        from aigie.sessions import Session

        return Session

    if name == "SessionMessage":
        from aigie.sessions import SessionMessage

        return SessionMessage

    if name == "create_session_manager":
        from aigie.sessions import create_session_manager

        return create_session_manager

    # Enhanced batch evaluation
    # Experiments API
    # Optional: Sync client
    if name == "AigieSync":
        try:
            from aigie.sync_client import AigieSync

            return AigieSync
        except ImportError as exc:
            raise ImportError("Sync client not available. Use Aigie (async) instead.") from exc

    # Cost Tracking (Gap Fix)
    if name == "extract_usage_from_response":
        from aigie.cost_tracking import extract_usage_from_response

        return extract_usage_from_response

    if name == "extract_and_calculate_cost":
        from aigie.cost_tracking import extract_and_calculate_cost

        return extract_and_calculate_cost

    if name == "calculate_cost":
        from aigie.cost_tracking import calculate_cost

        return calculate_cost

    if name == "add_model_pricing":
        from aigie.cost_tracking import add_model_pricing

        return add_model_pricing

    if name == "get_supported_models":
        from aigie.cost_tracking import get_supported_models

        return get_supported_models

    if name == "get_model_pricing":
        from aigie.cost_tracking import get_model_pricing

        return get_model_pricing

    if name == "CostAggregator":
        from aigie.cost_tracking import CostAggregator

        return CostAggregator

    if name == "UsageMetadata":
        from aigie.cost_tracking import UsageMetadata

        return UsageMetadata

    if name == "CostBreakdown":
        from aigie.cost_tracking import CostBreakdown

        return CostBreakdown

    # Summary Evaluators (Gap Fix)
    if name == "SummaryEvaluator":
        from aigie.summary_evaluators import SummaryEvaluator

        return SummaryEvaluator

    if name == "AccuracySummaryEvaluator":
        from aigie.summary_evaluators import AccuracySummaryEvaluator

        return AccuracySummaryEvaluator

    if name == "PrecisionSummaryEvaluator":
        from aigie.summary_evaluators import PrecisionSummaryEvaluator

        return PrecisionSummaryEvaluator

    if name == "AverageScoreSummaryEvaluator":
        from aigie.summary_evaluators import AverageScoreSummaryEvaluator

        return AverageScoreSummaryEvaluator

    if name == "PassRateSummaryEvaluator":
        from aigie.summary_evaluators import PassRateSummaryEvaluator

        return PassRateSummaryEvaluator

    if name == "CostSummaryEvaluator":
        from aigie.summary_evaluators import CostSummaryEvaluator

        return CostSummaryEvaluator

    if name == "LatencySummaryEvaluator":
        from aigie.summary_evaluators import LatencySummaryEvaluator

        return LatencySummaryEvaluator

    if name == "run_summary_evaluators":
        from aigie.summary_evaluators import run_summary_evaluators

        return run_summary_evaluators

    if name == "create_standard_summary_evaluators":
        from aigie.summary_evaluators import create_standard_summary_evaluators

        return create_standard_summary_evaluators

    if name == "RunData":
        from aigie.summary_evaluators import RunData

        return RunData

    if name == "SummaryEvaluationResult":
        from aigie.summary_evaluators import SummaryEvaluationResult

        return SummaryEvaluationResult

    if name == "SummaryEvaluatorFunction":
        from aigie.summary_evaluators import SummaryEvaluatorFunction

        return SummaryEvaluatorFunction

    # Safety Metrics (Gap Fix)
    # Guardrails (SLA Production Runtime)
    if name == "BaseGuardrail":
        from aigie.guardrails import BaseGuardrail

        return BaseGuardrail

    if name == "GuardrailChain":
        from aigie.guardrails import GuardrailChain

        return GuardrailChain

    if name == "GuardrailResult":
        from aigie.guardrails import GuardrailResult

        return GuardrailResult

    if name == "GuardrailAction":
        from aigie.guardrails import GuardrailAction

        return GuardrailAction

    if name == "GuardrailRemediationNeeded":
        from aigie.guardrails import GuardrailRemediationNeeded

        return GuardrailRemediationNeeded

    if name == "PIIDetector":
        from aigie.guardrails import PIIDetector

        return PIIDetector

    if name == "ToxicityDetector":
        from aigie.guardrails import ToxicityDetector

        return ToxicityDetector

    if name == "HallucinationDetector":
        from aigie.guardrails import HallucinationDetector

        return HallucinationDetector

    if name == "PromptInjectionDetector":
        from aigie.guardrails import PromptInjectionDetector

        return PromptInjectionDetector

    # Pytest Integration (Gap Fix)
    if name == "AigieTestCase":
        from aigie.pytest_plugin import AigieTestCase

        return AigieTestCase

    if name == "aigie_assert":
        from aigie.pytest_plugin import aigie_assert

        return aigie_assert

    if name == "assert_test":
        from aigie.pytest_plugin import assert_test

        return assert_test

    # UUID v7 (Gap Fix)
    if name == "uuidv7":
        from aigie.uuid7 import uuidv7

        return uuidv7

    if name == "extract_timestamp":
        from aigie.uuid7 import extract_timestamp

        return extract_timestamp

    if name == "is_valid_uuidv7":
        from aigie.uuid7 import is_valid_uuidv7

        return is_valid_uuidv7

    if name == "uuidv7_to_datetime":
        from aigie.uuid7 import uuidv7_to_datetime

        return uuidv7_to_datetime

    if name == "compare_uuidv7":
        from aigie.uuid7 import compare_uuidv7

        return compare_uuidv7

    if name == "generate_batch_uuidv7":
        from aigie.uuid7 import generate_batch_uuidv7

        return generate_batch_uuidv7

    if name == "uuidv7_with_timestamp":
        from aigie.uuid7 import uuidv7_with_timestamp

        return uuidv7_with_timestamp

    if name == "get_uuidv7_age":
        from aigie.uuid7 import get_uuidv7_age

        return get_uuidv7_age

    # Sampling System (Gap Fix)
    # Query API (Feature Parity)
    if name == "QueryAPI":
        from aigie.query_api import QueryAPI

        return QueryAPI

    if name == "TraceAPI":
        from aigie.query_api import TraceAPI

        return TraceAPI

    if name == "ObservationsAPI":
        from aigie.query_api import ObservationsAPI

        return ObservationsAPI

    if name == "SessionsAPI":
        from aigie.query_api import SessionsAPI

        return SessionsAPI

    if name == "ScoresAPI":
        from aigie.query_api import ScoresAPI

        return ScoresAPI

    if name == "Trace":
        from aigie.query_api import Trace

        return Trace

    if name == "Observation":
        from aigie.query_api import Observation

        return Observation

    if name == "ObservationType":
        from aigie.query_api import ObservationType

        return ObservationType

    if name == "TraceFilter":
        from aigie.query_api import TraceFilter

        return TraceFilter

    if name == "PaginatedResponse":
        from aigie.query_api import PaginatedResponse

        return PaginatedResponse

    # DataFrame Export Functions
    if name == "traces_to_dataframe":
        from aigie.query_api import traces_to_dataframe

        return traces_to_dataframe

    if name == "observations_to_dataframe":
        from aigie.query_api import observations_to_dataframe

        return observations_to_dataframe

    # Human Annotations (Feature Parity)
    if name == "AnnotationsAPI":
        from aigie.annotations import AnnotationsAPI

        return AnnotationsAPI

    if name == "AnnotationQueue":
        from aigie.annotations import AnnotationQueue

        return AnnotationQueue

    if name == "Annotation":
        from aigie.annotations import Annotation

        return Annotation

    if name == "AnnotationType":
        from aigie.annotations import AnnotationType

        return AnnotationType

    if name == "AnnotationTask":
        from aigie.annotations import AnnotationTask

        return AnnotationTask

    # Playground (Feature Parity)
    if name == "Playground":
        from aigie.playground import Playground

        return Playground

    if name == "PromptRegistry":
        from aigie.playground import PromptRegistry

        return PromptRegistry

    if name == "PromptTemplate":
        from aigie.playground import PromptTemplate

        return PromptTemplate

    if name == "PlaygroundRun":
        from aigie.playground import PlaygroundRun

        return PlaygroundRun

    if name == "ComparisonResult":
        from aigie.playground import ComparisonResult

        return ComparisonResult

    if name == "ModelConfig":
        from aigie.playground import ModelConfig

        return ModelConfig

    if name == "ModelProvider":
        from aigie.playground import ModelProvider

        return ModelProvider

    if name == "create_playground":
        from aigie.playground import create_playground

        return create_playground

    # Agent Graph View (Feature Parity)
    if name == "AgentGraph":
        from aigie.graph_view import AgentGraph

        return AgentGraph

    if name == "GraphBuilder":
        from aigie.graph_view import GraphBuilder

        return GraphBuilder

    if name == "GraphNode":
        from aigie.graph_view import GraphNode

        return GraphNode

    if name == "GraphEdge":
        from aigie.graph_view import GraphEdge

        return GraphEdge

    if name == "NodeType":
        from aigie.graph_view import NodeType

        return NodeType

    if name == "EdgeType":
        from aigie.graph_view import EdgeType

        return EdgeType

    if name == "NodeStatus":
        from aigie.graph_view import NodeStatus

        return NodeStatus

    if name == "ExecutionPath":
        from aigie.graph_view import ExecutionPath

        return ExecutionPath

    if name == "GraphMetrics":
        from aigie.graph_view import GraphMetrics

        return GraphMetrics

    if name == "create_graph":
        from aigie.graph_view import create_graph

        return create_graph

    if name == "create_graph_builder":
        from aigie.graph_view import create_graph_builder

        return create_graph_builder

    # Alerting (Feature Parity)
    if name == "AlertManager":
        from aigie.alerting import AlertManager

        return AlertManager

    if name == "AlertRule":
        from aigie.alerting import AlertRule

        return AlertRule

    if name == "AlertEvent":
        from aigie.alerting import AlertEvent

        return AlertEvent

    if name == "AlertCondition":
        from aigie.alerting import AlertCondition

        return AlertCondition

    if name == "AlertSeverity":
        from aigie.alerting import AlertSeverity

        return AlertSeverity

    if name == "AlertStatus":
        from aigie.alerting import AlertStatus

        return AlertStatus

    if name == "MetricType":
        from aigie.alerting import MetricType

        return MetricType

    if name == "ComparisonOperator":
        from aigie.alerting import ComparisonOperator

        return ComparisonOperator

    if name == "AggregationWindow":
        from aigie.alerting import AggregationWindow

        return AggregationWindow

    if name == "NotificationChannel":
        from aigie.alerting import NotificationChannel

        return NotificationChannel

    if name == "SlackChannel":
        from aigie.alerting import SlackChannel

        return SlackChannel

    if name == "EmailChannel":
        from aigie.alerting import EmailChannel

        return EmailChannel

    if name == "WebhookChannel":
        from aigie.alerting import WebhookChannel

        return WebhookChannel

    if name == "PagerDutyChannel":
        from aigie.alerting import PagerDutyChannel

        return PagerDutyChannel

    if name == "create_alert_manager":
        from aigie.alerting import create_alert_manager

        return create_alert_manager

    # Span Replay (Feature Parity)
    if name == "SpanReplay":
        from aigie.span_replay import SpanReplay

        return SpanReplay

    if name == "CapturedSpan":
        from aigie.span_replay import CapturedSpan

        return CapturedSpan

    if name == "ReplayResult":
        from aigie.span_replay import ReplayResult

        return ReplayResult

    if name == "ReplayExperiment":
        from aigie.span_replay import ReplayExperiment

        return ReplayExperiment

    if name == "ReplayStatus":
        from aigie.span_replay import ReplayStatus

        return ReplayStatus

    if name == "create_span_replay":
        from aigie.span_replay import create_span_replay

        return create_span_replay

    # Leaderboards (Feature Parity)
    if name == "LeaderboardManager":
        from aigie.leaderboards import LeaderboardManager

        return LeaderboardManager

    if name == "Leaderboard":
        from aigie.leaderboards import Leaderboard

        return Leaderboard

    if name == "LeaderboardEntry":
        from aigie.leaderboards import LeaderboardEntry

        return LeaderboardEntry

    if name == "ComparisonPair":
        from aigie.leaderboards import ComparisonPair

        return ComparisonPair

    if name == "EloRating":
        from aigie.leaderboards import EloRating

        return EloRating

    if name == "RankingMetric":
        from aigie.leaderboards import RankingMetric

        return RankingMetric

    if name == "AggregationType":
        from aigie.leaderboards import AggregationType

        return AggregationType

    if name == "create_leaderboard_manager":
        from aigie.leaderboards import create_leaderboard_manager

        return create_leaderboard_manager

    if name == "create_model_leaderboard":
        from aigie.leaderboards import create_model_leaderboard

        return create_model_leaderboard

    if name == "create_prompt_leaderboard":
        from aigie.leaderboards import create_prompt_leaderboard

        return create_prompt_leaderboard

    # License Management (Self-Hosted)
    if name == "LicenseValidator":
        from aigie.licensing import LicenseValidator

        return LicenseValidator

    if name == "LicenseInfo":
        from aigie.licensing import LicenseInfo

        return LicenseInfo

    if name == "UsageSummary":
        from aigie.licensing import UsageSummary

        return UsageSummary

    if name == "LicenseError":
        from aigie.licensing import LicenseError

        return LicenseError

    if name == "LicenseExpiredError":
        from aigie.licensing import LicenseExpiredError

        return LicenseExpiredError

    if name == "LicenseRevokedError":
        from aigie.licensing import LicenseRevokedError

        return LicenseRevokedError

    if name == "LicenseLimitExceededError":
        from aigie.licensing import LicenseLimitExceededError

        return LicenseLimitExceededError

    # Telemetry (SDK Feature Tracking)
    if name == "track_feature":
        from aigie.licensing import track_feature

        return track_feature

    if name == "record_error":
        from aigie.licensing import record_error

        return record_error

    if name == "FeatureTracker":
        from aigie.licensing import FeatureTracker

        return FeatureTracker

    if name == "ErrorCollector":
        from aigie.licensing import ErrorCollector

        return ErrorCollector

    # Agent Observability (new!)
    if name == "LoopDetectedError":
        from aigie.exceptions import LoopDetectedError

        return LoopDetectedError

    # Agent Framework
    if name == "Agent":
        from aigie.agent import Agent

        return Agent

    if name == "RunContext":
        from aigie.run_context import RunContext

        return RunContext

    if name == "Message":
        from aigie.run_context import Message

        return Message

    if name == "ModelRetry":
        from aigie.run_context import ModelRetry

        return ModelRetry

    if name == "get_current_context":
        from aigie.run_context import get_current_context

        return get_current_context

    if name == "get_current_context_or_none":
        from aigie.run_context import get_current_context_or_none

        return get_current_context_or_none

    if name == "set_current_context":
        from aigie.run_context import set_current_context

        return set_current_context

    if name == "reset_current_context":
        from aigie.run_context import reset_current_context

        return reset_current_context

    if name == "run_context":
        from aigie.run_context import run_context

        return run_context

    if name == "AgentResult":
        from aigie.result import AgentResult

        return AgentResult

    if name == "StreamedRunResult":
        from aigie.result import StreamedRunResult

        return StreamedRunResult

    if name == "UsageInfo":
        from aigie.result import UsageInfo

        return UsageInfo

    if name == "UnifiedError":
        from aigie.result import UnifiedError

        return UnifiedError

    if name == "Tool":
        from aigie.tools import Tool

        return Tool

    if name == "ToolCall":
        from aigie.tools import ToolCall

        return ToolCall

    if name == "ToolResult":
        from aigie.tools import ToolResult

        return ToolResult

    if name == "ToolRegistry":
        from aigie.tools import ToolRegistry

        return ToolRegistry

    if name == "tool":
        from aigie.tools import tool

        return tool

    if name == "create_tool_registry":
        from aigie.tools import create_tool_registry

        return create_tool_registry

    if name == "execute_tool":
        from aigie.tools import execute_tool

        return execute_tool

    if name == "tools_to_openai_functions":
        from aigie.tools import tools_to_openai_functions

        return tools_to_openai_functions

    if name == "tools_to_anthropic_tools":
        from aigie.tools import tools_to_anthropic_tools

        return tools_to_anthropic_tools

    if name == "type_to_json_schema":
        from aigie.schemas import type_to_json_schema

        return type_to_json_schema

    if name == "generate_json_schema":
        from aigie.schemas import generate_json_schema

        return generate_json_schema

    # Types (for type hints and validation)
    if name == "TraceStatus":
        from aigie.types import TraceStatus

        return TraceStatus

    if name == "SpanStatus":
        from aigie.types import SpanStatus

        return SpanStatus

    if name == "SpanType":
        from aigie.types import SpanType

        return SpanType

    if name == "ObservationLevel":
        from aigie.types import ObservationLevel

        return ObservationLevel

    if name == "FailureCategory":
        from aigie.types import FailureCategory

        return FailureCategory

    if name == "TokenUsage":
        from aigie.types import TokenUsage

        return TokenUsage

    if name == "TraceResponse":
        from aigie.types import TraceResponse

        return TraceResponse

    if name == "SpanResponse":
        from aigie.types import SpanResponse

        return SpanResponse

    # Platform API Clients - Analytics
    if name == "AnalyticsClient":
        from aigie.analytics import AnalyticsClient

        return AnalyticsClient

    if name == "DashboardStats":
        from aigie.analytics import DashboardStats

        return DashboardStats

    if name == "TimeSeriesPoint":
        from aigie.analytics import TimeSeriesPoint

        return TimeSeriesPoint

    if name == "WorkflowStats":
        from aigie.analytics import WorkflowStats

        return WorkflowStats

    if name == "ErrorSummary":
        from aigie.analytics import ErrorSummary

        return ErrorSummary

    if name == "ErrorCluster":
        from aigie.analytics import ErrorCluster

        return ErrorCluster

    if name == "CostAnalytics":
        from aigie.analytics import CostAnalytics

        return CostAnalytics

    if name == "AgentStats":
        from aigie.analytics import AgentStats

        return AgentStats

    # Platform API Clients - Workflows
    if name == "WorkflowsClient":
        from aigie.workflows import WorkflowsClient

        return WorkflowsClient

    if name == "WorkflowDefinition":
        from aigie.workflows import WorkflowDefinition

        return WorkflowDefinition

    if name == "WorkflowExecution":
        from aigie.workflows import WorkflowExecution

        return WorkflowExecution

    # Platform API Clients - Recommendations
    if name == "RecommendationsClient":
        from aigie.recommendations import RecommendationsClient

        return RecommendationsClient

    if name == "TraceRecommendation":
        from aigie.recommendations import TraceRecommendation

        return TraceRecommendation

    if name == "WorkflowRecommendation":
        from aigie.recommendations import WorkflowRecommendation

        return WorkflowRecommendation

    if name == "ImpactAnalysis":
        from aigie.recommendations import ImpactAnalysis

        return ImpactAnalysis

    # Platform API Clients - Learning
    if name == "LearningClient":
        from aigie.learning import LearningClient

        return LearningClient

    if name == "LearningStats":
        from aigie.learning import LearningStats

        return LearningStats

    if name == "LearningPattern":
        from aigie.learning import LearningPattern

        return LearningPattern

    if name == "FeedbackEntry":
        from aigie.learning import FeedbackEntry

        return FeedbackEntry

    if name == "EvalStats":
        from aigie.learning import EvalStats

        return EvalStats

    # Integration Registry (LiteLLM-style patching)
    if name == "patch":
        from aigie.integrations.registry import patch

        return patch

    if name == "unpatch":
        from aigie.integrations.registry import unpatch

        return unpatch

    if name == "is_patched":
        from aigie.integrations.registry import is_patched

        return is_patched

    if name == "is_integration_available":
        from aigie.integrations.registry import is_integration_available

        return is_integration_available

    if name == "list_integrations":
        from aigie.integrations.registry import list_integrations

        return list_integrations

    if name == "list_integration_names":
        from aigie.integrations.registry import list_integration_names

        return list_integration_names

    if name == "get_patched_integrations":
        from aigie.integrations.registry import get_patched_integrations

        return get_patched_integrations

    if name == "register_integration":
        from aigie.integrations.registry import register_integration

        return register_integration

    if name == "patch_all":
        from aigie.integrations.registry import patch_all

        return patch_all

    # Exceptions
    if name == "AigieError":
        from aigie.exceptions import AigieError

        return AigieError

    if name == "ContextDriftDetected":
        from aigie.exceptions import ContextDriftDetected

        return ContextDriftDetected

    if name == "TopicDriftDetected":
        from aigie.exceptions import TopicDriftDetected

        return TopicDriftDetected

    if name == "BehaviorDriftDetected":
        from aigie.exceptions import BehaviorDriftDetected

        return BehaviorDriftDetected

    if name == "QualityDriftDetected":
        from aigie.exceptions import QualityDriftDetected

        return QualityDriftDetected

    if name == "RemediationFailed":
        from aigie.exceptions import RemediationFailed

        return RemediationFailed

    if name == "RemediationRejected":
        from aigie.exceptions import RemediationRejected

        return RemediationRejected

    if name == "RetryExhausted":
        from aigie.exceptions import RetryExhausted

        return RetryExhausted

    if name == "TraceBufferError":
        from aigie.exceptions import TraceBufferError

        return TraceBufferError

    if name == "TraceContextError":
        from aigie.exceptions import TraceContextError

        return TraceContextError

    if name == "InterceptionBlocked":
        from aigie.exceptions import InterceptionBlocked

        return InterceptionBlocked

    if name == "InterceptionRetryRequested":
        from aigie.exceptions import InterceptionRetryRequested

        return InterceptionRetryRequested

    if name == "ConfigurationError":
        from aigie.exceptions import ConfigurationError

        return ConfigurationError

    if name == "IntegrationError":
        from aigie.exceptions import IntegrationError

        return IntegrationError

    if name == "IntegrationNotFoundError":
        from aigie.exceptions import IntegrationNotFoundError

        return IntegrationNotFoundError

    if name == "IntegrationNotInstalledError":
        from aigie.exceptions import IntegrationNotInstalledError

        return IntegrationNotInstalledError

    if name == "BackendError":
        from aigie.exceptions import BackendError

        return BackendError

    if name == "BackendConnectionError":
        from aigie.exceptions import BackendConnectionError

        return BackendConnectionError

    if name == "RateLimitError":
        from aigie.exceptions import RateLimitError

        return RateLimitError

    if name == "AuthenticationError":
        from aigie.exceptions import AuthenticationError

        return AuthenticationError

    if name == "WebhookError":
        from aigie.exceptions import WebhookError

        return WebhookError

    # Callbacks
    if name == "GenericWebhookCallback":
        from aigie.callbacks import GenericWebhookCallback

        return GenericWebhookCallback

    if name == "BaseCallback":
        from aigie.callbacks import BaseCallback

        return BaseCallback

    if name == "CallbackEvent":
        from aigie.callbacks import CallbackEvent

        return CallbackEvent

    if name == "CallbackEventType":
        from aigie.callbacks import CallbackEventType

        return CallbackEventType

    if name == "create_webhook":
        from aigie.callbacks.generic_webhook import create_webhook

        return create_webhook

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Type checking support
if TYPE_CHECKING:
    from aigie.alerting import (
        AggregationWindow,
        AlertCondition,
        AlertEvent,
        AlertManager,
        AlertRule,
        AlertSeverity,
        AlertStatus,
        ComparisonOperator,
        EmailChannel,
        MetricType,
        NotificationChannel,
        PagerDutyChannel,
        SlackChannel,
        WebhookChannel,
        create_alert_manager,
    )
    from aigie.analytics import (
        AgentStats,
        AnalyticsClient,
        CostAnalytics,
        DashboardStats,
        ErrorCluster,
        ErrorSummary,
        TimeSeriesPoint,
        WorkflowStats,
    )
    from aigie.annotations import (
        Annotation,
        AnnotationQueue,
        AnnotationsAPI,
        AnnotationTask,
        AnnotationType,
    )
    from aigie.buffer import EventBuffer
    from aigie.callbacks import (
        BaseCallback,
        CallbackEvent,
        CallbackEventType,
        GenericWebhookCallback,
    )
    from aigie.callbacks.generic_webhook import create_webhook
    from aigie.client import Aigie
    from aigie.compression import Compressor, is_compression_available
    from aigie.config import Config
    from aigie.context import TraceContext as W3CTraceContext
    from aigie.context import extract_trace_context, inject_trace_context
    from aigie.context_manager import (
        get_current_span_context,
        get_current_trace_context,
        is_tracing_enabled,
        set_tracing_enabled,
        tracing_context,
    )
    from aigie.cost_tracking import (
        CostAggregator,
        CostBreakdown,
        UsageMetadata,
        add_model_pricing,
        calculate_cost,
        extract_and_calculate_cost,
        extract_usage_from_response,
        get_model_pricing,
        get_supported_models,
    )
    from aigie.decorators_v3 import create_traceable, set_debug_mode, trace, traceable
    from aigie.evaluation import EvaluationResult
    from aigie.evaluations import (
        EvaluationJob,
        EvaluationRequest,
        EvaluationsClient,
        EvaluationScore,
        EvaluationTemplate,
        EvaluationType,
        evaluate,
    )
    from aigie.exceptions import (
        AigieError,
        AuthenticationError,
        BackendConnectionError,
        BackendError,
        BehaviorDriftDetected,
        ConfigurationError,
        ContextDriftDetected,
        IntegrationError,
        IntegrationNotFoundError,
        IntegrationNotInstalledError,
        InterceptionBlocked,
        InterceptionRetryRequested,
        LoopDetectedError,
        QualityDriftDetected,
        RateLimitError,
        RemediationFailed,
        RemediationRejected,
        RetryExhausted,
        TopicDriftDetected,
        TraceBufferError,
        TraceContextError,
        WebhookError,
    )
    from aigie.graph_view import (
        AgentGraph,
        EdgeType,
        ExecutionPath,
        GraphBuilder,
        GraphEdge,
        GraphMetrics,
        GraphNode,
        NodeStatus,
        NodeType,
        create_graph,
        create_graph_builder,
    )
    from aigie.guardrails import (
        BaseGuardrail,
        GuardrailAction,
        GuardrailChain,
        GuardrailRemediationNeeded,
        GuardrailResult,
        HallucinationDetector,
        PIIDetector,
        PromptInjectionDetector,
        ToxicityDetector,
    )
    from aigie.integrations.registry import (
        get_patched_integrations,
        is_integration_available,
        is_patched,
        list_integration_names,
        list_integrations,
        patch,
        patch_all,
        register_integration,
        unpatch,
    )
    from aigie.judges import (
        Judge,
        JudgeConfig,
        JudgeResult,
        JudgesClient,
        JudgeType,
        judge,
        judge_all,
    )
    from aigie.leaderboards import (
        AggregationType,
        ComparisonPair,
        EloRating,
        Leaderboard,
        LeaderboardEntry,
        LeaderboardManager,
        RankingMetric,
        create_leaderboard_manager,
        create_model_leaderboard,
        create_prompt_leaderboard,
    )
    from aigie.learning import (
        EvalStats,
        FeedbackEntry,
        LearningClient,
        LearningPattern,
        LearningStats,
    )
    from aigie.licensing import (
        LicenseError,
        LicenseExpiredError,
        LicenseInfo,
        LicenseLimitExceededError,
        LicenseRevokedError,
        LicenseValidator,
        UsageSummary,
    )
    from aigie.observe import observe
    from aigie.playground import (
        ComparisonResult,
        ModelConfig,
        ModelProvider,
        Playground,
        PlaygroundRun,
        PromptRegistry,
        PromptTemplate,
        create_playground,
    )
    from aigie.pytest_plugin import AigieTestCase, aigie_assert, assert_test
    from aigie.query_api import (
        Observation,
        ObservationsAPI,
        ObservationType,
        PaginatedResponse,
        QueryAPI,
        ScoresAPI,
        SessionsAPI,
        Trace,
        TraceAPI,
        TraceFilter,
    )
    from aigie.recommendations import (
        ImpactAnalysis,
        RecommendationsClient,
        TraceRecommendation,
        WorkflowRecommendation,
    )
    from aigie.span import SpanContext
    from aigie.span_replay import (
        CapturedSpan,
        ReplayExperiment,
        ReplayResult,
        ReplayStatus,
        SpanReplay,
        create_span_replay,
    )
    from aigie.streaming import StreamingSpan
    from aigie.summary_evaluators import (
        AccuracySummaryEvaluator,
        AverageScoreSummaryEvaluator,
        CostSummaryEvaluator,
        LatencySummaryEvaluator,
        PassRateSummaryEvaluator,
        PrecisionSummaryEvaluator,
        RunData,
        SummaryEvaluationResult,
        SummaryEvaluator,
        SummaryEvaluatorFunction,
        create_standard_summary_evaluators,
        run_summary_evaluators,
    )
    from aigie.trace import TraceContext
    from aigie.uuid7 import (
        compare_uuidv7,
        extract_timestamp,
        generate_batch_uuidv7,
        get_uuidv7_age,
        is_valid_uuidv7,
        uuidv7,
        uuidv7_to_datetime,
        uuidv7_with_timestamp,
    )
    from aigie.workflows import WorkflowDefinition, WorkflowExecution, WorkflowsClient
    from aigie.wrappers import wrap_anthropic, wrap_gemini, wrap_openai
    from aigie.wrappers_bedrock import create_traced_bedrock, wrap_bedrock
    from aigie.wrappers_cohere import create_traced_cohere, wrap_cohere


# ============================================================================
# Module-level Configuration (LiteLLM-style)
# ============================================================================
# These variables provide a simple way to configure Aigie without creating
# an Aigie instance. Set these before using any tracing functions.
#
# Usage:
#     import aigie
#     aigie.kytte_token = "your-token"
#     aigie.kytte_url = "https://your-kytte-instance.com/api"
#     aigie.init()  # Uses module-level settings
#
# These are read by init() when no explicit parameters are provided.

import os as _os  # noqa: E402

# Canonical Kytte platform configuration
kytte_token: str = _os.getenv("KYTTE_TOKEN", _os.getenv("AIGIE_TOKEN", ""))
kytte_url: str = _os.getenv("KYTTE_URL", _os.getenv("AIGIE_URL", ""))

# DEPRECATED: Use kytte_token / kytte_url instead. Kept for backward compatibility.
api_key: str = _os.getenv("AIGIE_API_KEY", "")
api_url: str = _os.getenv("AIGIE_API_URL", "")

# Debug mode
debug: bool = _os.getenv("AIGIE_DEBUG", "").lower() in ("true", "1", "yes")

# Tracing configuration
enabled: bool = True  # Set to False to disable all tracing

# Default callbacks (populated when callbacks are added at module level)
_module_callbacks: list = []


def add_callback(callback: Any) -> None:
    """
    Add a callback at module level.

    This callback will be added to the global Aigie instance when init() is called.

    Usage:
        import aigie
        from aigie.callbacks import GenericWebhookCallback

        webhook = GenericWebhookCallback(endpoint="https://my-service.com/logs")
        aigie.add_callback(webhook)
    """
    _module_callbacks.append(callback)
