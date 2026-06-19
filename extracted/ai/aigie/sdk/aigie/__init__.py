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

    # Score traces for quality monitoring
    from aigie import score
    await score(trace_id, "accuracy", 0.95)

    # Manage prompts with versioning
    from aigie import Prompt
    prompt = Prompt.chat(
        name="research_agent",
        messages=[{"role": "system", "content": "You are helpful."}]
    )
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
    "set_global_mask_fn",
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
    # Gateway (Real-Time Validation)
    "GatewayClient",
    "GatewayConnectionState",
    "ToolCallMiddleware",
    "ToolCallResult",
    "PreExecutionRequest",
    "PreExecutionResponse",
    "GatewayDecision",
    "ValidationSignal",
    "SignalType",
    "InterventionSignal",
    "FallbackMode",
    "FallbackStrategy",
    "InterventionHandler",
    "BlockHandler",
    "ModifyHandler",
    "DelayHandler",
    "EscalateHandler",
    "HandlerChain",
    "HandlerResult",
    "InterventionType",
    "ExecutionBlockedError",
    "InterventionHandlerError",
    # Checkpoint API
    "CheckpointManager",
    "Checkpoint",
    "CheckpointStatus",
    "CheckpointType",
    "CheckpointConfig",
    "CheckpointMetrics",
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
    # Prompts
    "Prompt",
    "PromptManager",
    "PromptFormat",
    "TextPrompt",
    "ChatPrompt",
    "get_prompt_manager",
    "register_prompt",
    "get_prompt",
    # Evaluation
    "EvaluationHook",
    "Evaluator",
    "EvaluationResult",
    "ScoreType",
    "Score",
    "ScoreDataType",
    "ScoreManager",
    "get_score_manager",
    "score",
    "feedback",
    # Metrics (new!)
    "BaseMetric",
    "DriftDetectionMetric",
    "RecoverySuccessMetric",
    "CheckpointValidityMetric",
    "NestedAgentHealthMetric",
    "ProductionReliabilityMetric",
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
    # Phase 2 Features
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
    # Phase 3 Features
    # Enhanced batch evaluation
    "enhanced_batch_evaluate",
    "generate_batch_report",
    "export_batch_results",
    "export_batch_results_to_csv",
    "BatchProgress",
    "TestCaseResult",
    "BatchStatistics",
    "BatchEvaluationResult",
    # Experiments API
    "ExperimentsClient",
    "create_experiments_client",
    "generate_experiment_report",
    "ExperimentVariant",
    "VariantResult",
    "VariantStatistics",
    "WinnerInfo",
    "ExperimentResult",
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
    # Safety Metrics (Gap Fix)
    "PIILeakageEvaluator",
    "ToxicityEvaluator",
    "BiasEvaluator",
    "PromptInjectionEvaluator",
    "JailbreakEvaluator",
    "RedTeamScanner",
    "create_safety_evaluators",
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
    # Sampling System (Gap Fix)
    "Sampler",
    "SamplingConfig",
    "AdaptiveConfig",
    "create_smart_sampler",
    "create_adaptive_sampler",
    "create_importance_function",
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
    "LoopDetector",
    "TracingLoopDetector",
    "LoopAction",
    "LoopState",
    "LoopDetectionResult",
    "GoalTracker",
    "TracingGoalTracker",
    "Goal",
    "Step",
    "StepStatus",
    "Deviation",
    "DeviationType",
    "PlanMetrics",
    "ExecutionCycle",
    "CyclePhase",
    "PhaseContext",
    "PhaseResult",
    "CycleMetrics",
    "MultiCycleExecutor",
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
    "WorkflowStep",
    "RecommendationsClient",
    "TraceRecommendation",
    "WorkflowRecommendation",
    "ImpactAnalysis",
    "LearningClient",
    "LearningStats",
    "LearningPattern",
    "FeedbackEntry",
    "EvalStats",
    "RemediationClient",
    "RemediationJob",
    "QueueStats",
    "AutonomousPreview",
    "HallucinationDetection",
    "ControlLoopStatus",
    # Autonomous v2
    "AutonomousRuntime",
]

__version__ = "0.2.46"


# Lazy imports for performance
def __getattr__(name: str) -> Any:  # noqa: C901, PLR0911, PLR0912
    """
    Lazy import implementation for faster load times.

    Modules are only imported when actually used, reducing cold start penalty.
    """
    # Autonomous v2
    if name == "AutonomousRuntime":
        from aigie.autonomous.runtime import AutonomousRuntime

        return AutonomousRuntime

    # Core client
    if name == "Aigie":
        from .client import Aigie

        return Aigie

    if name == "Config":
        from .config import Config

        return Config

    if name == "init":
        from .client import init

        return init

    if name == "shutdown":
        from .client import shutdown

        return shutdown

    if name == "get_aigie":
        from .client import get_aigie

        return get_aigie

    if name == "sdk_status":

        def _sdk_status() -> dict:
            from .client import get_aigie

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
        from .trace import TraceContext

        return TraceContext

    if name == "SpanContext":
        from .span import SpanContext

        return SpanContext

    if name == "no_retention":
        from aigie.tracing.retention import no_retention

        return no_retention

    if name == "no_retention_async":
        from aigie.tracing.retention import no_retention_async

        return no_retention_async

    # Decorators (v3)
    if name in ("traceable", "trace"):
        from .decorators_v3 import traceable

        return traceable

    # Enhanced decorator utilities
    if name == "create_traceable":
        from .decorators_v3 import create_traceable

        return create_traceable

    if name == "set_global_mask_fn":
        from .decorators_v3 import set_global_mask_fn

        return set_global_mask_fn

    if name == "set_debug_mode":
        from .decorators_v3 import set_debug_mode

        return set_debug_mode

    # Context propagation
    if name == "get_current_trace":
        from .trace import get_current_trace

        return get_current_trace

    if name == "update_current_trace":
        from .trace import update_current_trace

        return update_current_trace

    if name == "tracing_context":
        from .context_manager import tracing_context

        return tracing_context

    if name == "get_current_trace_context":
        from .context_manager import get_current_trace_context

        return get_current_trace_context

    if name == "get_current_span_context":
        from .context_manager import get_current_span_context

        return get_current_span_context

    if name == "is_tracing_enabled":
        from .context_manager import is_tracing_enabled

        return is_tracing_enabled

    if name == "set_tracing_enabled":
        from .context_manager import set_tracing_enabled

        return set_tracing_enabled

    # Wrappers
    if name == "wrap_openai":
        from .wrappers import wrap_openai

        return wrap_openai

    if name == "wrap_anthropic":
        from .wrappers import wrap_anthropic

        return wrap_anthropic

    if name == "wrap_gemini":
        from .wrappers import wrap_gemini

        return wrap_gemini

    if name == "wrap_bedrock":
        from .wrappers_bedrock import wrap_bedrock

        return wrap_bedrock

    if name == "create_traced_bedrock":
        from .wrappers_bedrock import create_traced_bedrock

        return create_traced_bedrock

    if name == "wrap_cohere":
        from .wrappers_cohere import wrap_cohere

        return wrap_cohere

    if name == "create_traced_cohere":
        from .wrappers_cohere import create_traced_cohere

        return create_traced_cohere

    # Gateway (Real-Time Validation)
    if name == "GatewayClient":
        from .gateway import GatewayClient

        return GatewayClient

    if name == "GatewayConnectionState":
        from .gateway import GatewayConnectionState

        return GatewayConnectionState

    if name == "ToolCallMiddleware":
        from .gateway import ToolCallMiddleware

        return ToolCallMiddleware

    if name == "ToolCallResult":
        from .gateway import ToolCallResult

        return ToolCallResult

    if name == "PreExecutionRequest":
        from .gateway import PreExecutionRequest

        return PreExecutionRequest

    if name == "PreExecutionResponse":
        from .gateway import PreExecutionResponse

        return PreExecutionResponse

    if name == "GatewayDecision":
        from .gateway import GatewayDecision

        return GatewayDecision

    if name == "ValidationSignal":
        from .gateway import ValidationSignal

        return ValidationSignal

    if name == "SignalType":
        from .gateway import SignalType

        return SignalType

    if name == "InterventionSignal":
        from .gateway import InterventionSignal

        return InterventionSignal

    if name == "FallbackMode":
        from .gateway import FallbackMode

        return FallbackMode

    if name == "FallbackStrategy":
        from .gateway import FallbackStrategy

        return FallbackStrategy

    if name == "InterventionHandler":
        from .gateway import InterventionHandler

        return InterventionHandler

    if name == "BlockHandler":
        from .gateway import BlockHandler

        return BlockHandler

    if name == "ModifyHandler":
        from .gateway import ModifyHandler

        return ModifyHandler

    if name == "DelayHandler":
        from .gateway import DelayHandler

        return DelayHandler

    if name == "EscalateHandler":
        from .gateway import EscalateHandler

        return EscalateHandler

    if name == "HandlerChain":
        from .gateway import HandlerChain

        return HandlerChain

    if name == "HandlerResult":
        from .gateway import HandlerResult

        return HandlerResult

    if name == "InterventionType":
        from .gateway import InterventionType

        return InterventionType

    if name == "ExecutionBlockedError":
        from .gateway import ExecutionBlockedError

        return ExecutionBlockedError

    if name == "InterventionHandlerError":
        from .gateway import InterventionHandlerError

        return InterventionHandlerError

    # Checkpoint API
    if name == "CheckpointManager":
        from .checkpoint import CheckpointManager

        return CheckpointManager

    if name == "Checkpoint":
        from .checkpoint import Checkpoint

        return Checkpoint

    if name == "CheckpointStatus":
        from .checkpoint import CheckpointStatus

        return CheckpointStatus

    if name == "CheckpointType":
        from .checkpoint import CheckpointType

        return CheckpointType

    if name == "CheckpointConfig":
        from .checkpoint import CheckpointConfig

        return CheckpointConfig

    if name == "CheckpointMetrics":
        from .checkpoint import CheckpointMetrics

        return CheckpointMetrics

    # Unified Signal Reporter
    if name == "SignalReporter":
        from .signals import SignalReporter

        return SignalReporter

    if name == "Signal":
        from .signals import Signal

        return Signal

    if name == "SignalBatch":
        from .signals import SignalBatch

        return SignalBatch

    if name == "SignalMetrics":
        from .signals import SignalMetrics

        return SignalMetrics

    if name == "SignalSeverity":
        from .signals import SignalSeverity

        return SignalSeverity

    if name == "DriftType":
        from .signals import DriftType

        return DriftType

    if name == "get_signal_reporter":
        from .signals import get_signal_reporter

        return get_signal_reporter

    if name == "set_signal_reporter":
        from .signals import set_signal_reporter

        return set_signal_reporter

    # Health Monitor
    if name == "HealthMonitor":
        from .health import HealthMonitor

        return HealthMonitor

    if name == "HealthStatus":
        from .health import HealthStatus

        return HealthStatus

    if name == "HealthConfig":
        from .health import HealthConfig

        return HealthConfig

    if name == "HealthMetrics":
        from .health import HealthMetrics

        return HealthMetrics

    if name == "DegradationLevel":
        from .health import DegradationLevel

        return DegradationLevel

    if name == "ServiceStatus":
        from .health import ServiceStatus

        return ServiceStatus

    if name == "ServiceHealth":
        from .health import ServiceHealth

        return ServiceHealth

    if name == "get_health_monitor":
        from .health import get_health_monitor

        return get_health_monitor

    if name == "set_health_monitor":
        from .health import set_health_monitor

        return set_health_monitor

    # Compression
    if name == "Compressor":
        from .compression import Compressor

        return Compressor

    if name == "is_compression_available":
        from .compression import is_compression_available

        return is_compression_available

    # Buffer
    if name == "EventBuffer":
        from .buffer import EventBuffer

        return EventBuffer

    # W3C Trace Context
    if name == "W3CTraceContext":
        from .context import TraceContext as W3CTraceContext

        return W3CTraceContext

    if name == "extract_trace_context":
        from .context import extract_trace_context

        return extract_trace_context

    if name == "inject_trace_context":
        from .context import inject_trace_context

        return inject_trace_context

    # Prompts
    if name == "Prompt":
        from .prompts import Prompt

        return Prompt

    if name == "PromptManager":
        from .prompts import PromptManager

        return PromptManager

    if name == "PromptFormat":
        from .prompts import PromptFormat

        return PromptFormat

    if name == "TextPrompt":
        from .prompts import TextPrompt

        return TextPrompt

    if name == "ChatPrompt":
        from .prompts import ChatPrompt

        return ChatPrompt

    if name == "get_prompt_manager":
        from .prompts import get_prompt_manager

        return get_prompt_manager

    if name == "register_prompt":
        from .prompts import register_prompt

        return register_prompt

    if name == "get_prompt":
        from .prompts import get_prompt

        return get_prompt

    # Evaluation
    if name == "EvaluationHook":
        from .evaluation import EvaluationHook

        return EvaluationHook

    if name == "Evaluator":
        from .evaluation import Evaluator

        return Evaluator

    if name == "EvaluationResult":
        from .evaluation import EvaluationResult

        return EvaluationResult

    if name == "ScoreType":
        from .evaluation import ScoreType

        return ScoreType

    if name == "Score":
        from .evaluation import Score

        return Score

    if name == "ScoreDataType":
        from .evaluation import ScoreDataType

        return ScoreDataType

    if name == "ScoreManager":
        from .evaluation import ScoreManager

        return ScoreManager

    if name == "get_score_manager":
        from .evaluation import get_score_manager

        return get_score_manager

    if name == "score":
        from .evaluation import score

        return score

    if name == "feedback":
        from .evaluation import feedback

        return feedback

    # Metrics (new!)
    if name == "BaseMetric":
        from .metrics.base import BaseMetric

        return BaseMetric

    if name == "DriftDetectionMetric":
        from .metrics.drift import DriftDetectionMetric

        return DriftDetectionMetric

    if name == "RecoverySuccessMetric":
        from .metrics.recovery import RecoverySuccessMetric

        return RecoverySuccessMetric

    if name == "CheckpointValidityMetric":
        from .metrics.checkpoint import CheckpointValidityMetric

        return CheckpointValidityMetric

    if name == "NestedAgentHealthMetric":
        from .metrics.nested import NestedAgentHealthMetric

        return NestedAgentHealthMetric

    if name == "ProductionReliabilityMetric":
        from .metrics.reliability import ProductionReliabilityMetric

        return ProductionReliabilityMetric

    # Component-level evaluation (new!)
    if name == "observe":
        from .observe import observe

        return observe

    # Streaming
    if name == "StreamingSpan":
        from .streaming import StreamingSpan

        return StreamingSpan

    # Evaluations API (NEW!)
    if name == "EvaluationsClient":
        from .evaluations import EvaluationsClient

        return EvaluationsClient

    if name == "EvaluationType":
        from .evaluations import EvaluationType

        return EvaluationType

    if name == "EvaluationTemplate":
        from .evaluations import EvaluationTemplate

        return EvaluationTemplate

    if name == "EvaluationScore":
        from .evaluations import EvaluationScore

        return EvaluationScore

    if name == "EvaluationJob":
        from .evaluations import EvaluationJob

        return EvaluationJob

    if name == "EvaluationRequest":
        from .evaluations import EvaluationRequest

        return EvaluationRequest

    if name == "evaluate":
        from .evaluations import evaluate

        return evaluate

    # Judges API (NEW!)
    if name == "JudgesClient":
        from .judges import JudgesClient

        return JudgesClient

    if name == "JudgeType":
        from .judges import JudgeType

        return JudgeType

    if name == "Judge":
        from .judges import Judge

        return Judge

    if name == "JudgeResult":
        from .judges import JudgeResult

        return JudgeResult

    if name == "JudgeConfig":
        from .judges import JudgeConfig

        return JudgeConfig

    if name == "judge":
        from .judges import judge

        return judge

    if name == "judge_all":
        from .judges import judge_all

        return judge_all

    # Phase 2: Datasets
    if name == "DatasetsClient":
        from .datasets import DatasetsClient

        return DatasetsClient

    if name == "Dataset":
        from .datasets import Dataset

        return Dataset

    if name == "DatasetExample":
        from .datasets import DatasetExample

        return DatasetExample

    if name == "DatasetRunResult":
        from .datasets import DatasetRunResult

        return DatasetRunResult

    if name == "DatasetRunSummary":
        from .datasets import DatasetRunSummary

        return DatasetRunSummary

    # Phase 2: Sessions
    if name == "SessionManager":
        from .sessions import SessionManager

        return SessionManager

    if name == "SessionAnalytics":
        from .sessions import SessionAnalytics

        return SessionAnalytics

    if name == "Session":
        from .sessions import Session

        return Session

    if name == "SessionMessage":
        from .sessions import SessionMessage

        return SessionMessage

    if name == "create_session_manager":
        from .sessions import create_session_manager

        return create_session_manager

    # Enhanced batch evaluation
    if name == "enhanced_batch_evaluate":
        from .batch_evaluation import enhanced_batch_evaluate

        return enhanced_batch_evaluate

    if name == "generate_batch_report":
        from .batch_evaluation import generate_batch_report

        return generate_batch_report

    if name == "export_batch_results":
        from .batch_evaluation import export_batch_results

        return export_batch_results

    if name == "export_batch_results_to_csv":
        from .batch_evaluation import export_batch_results_to_csv

        return export_batch_results_to_csv

    if name == "BatchProgress":
        from .batch_evaluation import BatchProgress

        return BatchProgress

    if name == "TestCaseResult":
        from .batch_evaluation import TestCaseResult

        return TestCaseResult

    if name == "BatchStatistics":
        from .batch_evaluation import BatchStatistics

        return BatchStatistics

    if name == "BatchEvaluationResult":
        from .batch_evaluation import BatchEvaluationResult

        return BatchEvaluationResult

    # Experiments API
    if name == "ExperimentsClient":
        from .experiments import ExperimentsClient

        return ExperimentsClient

    if name == "create_experiments_client":
        from .experiments import create_experiments_client

        return create_experiments_client

    if name == "generate_experiment_report":
        from .experiments import generate_experiment_report

        return generate_experiment_report

    if name == "ExperimentVariant":
        from .experiments import ExperimentVariant

        return ExperimentVariant

    if name == "VariantResult":
        from .experiments import VariantResult

        return VariantResult

    if name == "VariantStatistics":
        from .experiments import VariantStatistics

        return VariantStatistics

    if name == "WinnerInfo":
        from .experiments import WinnerInfo

        return WinnerInfo

    if name == "ExperimentResult":
        from .experiments import ExperimentResult

        return ExperimentResult

    # Optional: Sync client
    if name == "AigieSync":
        try:
            from .sync_client import AigieSync

            return AigieSync
        except ImportError as exc:
            raise ImportError("Sync client not available. Use Aigie (async) instead.") from exc

    # Cost Tracking (Gap Fix)
    if name == "extract_usage_from_response":
        from .cost_tracking import extract_usage_from_response

        return extract_usage_from_response

    if name == "extract_and_calculate_cost":
        from .cost_tracking import extract_and_calculate_cost

        return extract_and_calculate_cost

    if name == "calculate_cost":
        from .cost_tracking import calculate_cost

        return calculate_cost

    if name == "add_model_pricing":
        from .cost_tracking import add_model_pricing

        return add_model_pricing

    if name == "get_supported_models":
        from .cost_tracking import get_supported_models

        return get_supported_models

    if name == "get_model_pricing":
        from .cost_tracking import get_model_pricing

        return get_model_pricing

    if name == "CostAggregator":
        from .cost_tracking import CostAggregator

        return CostAggregator

    if name == "UsageMetadata":
        from .cost_tracking import UsageMetadata

        return UsageMetadata

    if name == "CostBreakdown":
        from .cost_tracking import CostBreakdown

        return CostBreakdown

    # Summary Evaluators (Gap Fix)
    if name == "SummaryEvaluator":
        from .summary_evaluators import SummaryEvaluator

        return SummaryEvaluator

    if name == "AccuracySummaryEvaluator":
        from .summary_evaluators import AccuracySummaryEvaluator

        return AccuracySummaryEvaluator

    if name == "PrecisionSummaryEvaluator":
        from .summary_evaluators import PrecisionSummaryEvaluator

        return PrecisionSummaryEvaluator

    if name == "AverageScoreSummaryEvaluator":
        from .summary_evaluators import AverageScoreSummaryEvaluator

        return AverageScoreSummaryEvaluator

    if name == "PassRateSummaryEvaluator":
        from .summary_evaluators import PassRateSummaryEvaluator

        return PassRateSummaryEvaluator

    if name == "CostSummaryEvaluator":
        from .summary_evaluators import CostSummaryEvaluator

        return CostSummaryEvaluator

    if name == "LatencySummaryEvaluator":
        from .summary_evaluators import LatencySummaryEvaluator

        return LatencySummaryEvaluator

    if name == "run_summary_evaluators":
        from .summary_evaluators import run_summary_evaluators

        return run_summary_evaluators

    if name == "create_standard_summary_evaluators":
        from .summary_evaluators import create_standard_summary_evaluators

        return create_standard_summary_evaluators

    if name == "RunData":
        from .summary_evaluators import RunData

        return RunData

    if name == "SummaryEvaluationResult":
        from .summary_evaluators import SummaryEvaluationResult

        return SummaryEvaluationResult

    if name == "SummaryEvaluatorFunction":
        from .summary_evaluators import SummaryEvaluatorFunction

        return SummaryEvaluatorFunction

    # Safety Metrics (Gap Fix)
    if name == "PIILeakageEvaluator":
        from .safety_metrics import PIILeakageEvaluator

        return PIILeakageEvaluator

    if name == "ToxicityEvaluator":
        from .safety_metrics import ToxicityEvaluator

        return ToxicityEvaluator

    if name == "BiasEvaluator":
        from .safety_metrics import BiasEvaluator

        return BiasEvaluator

    if name == "PromptInjectionEvaluator":
        from .safety_metrics import PromptInjectionEvaluator

        return PromptInjectionEvaluator

    if name == "JailbreakEvaluator":
        from .safety_metrics import JailbreakEvaluator

        return JailbreakEvaluator

    if name == "RedTeamScanner":
        from .safety_metrics import RedTeamScanner

        return RedTeamScanner

    if name == "create_safety_evaluators":
        from .safety_metrics import create_safety_evaluators

        return create_safety_evaluators

    # Guardrails (SLA Production Runtime)
    if name == "BaseGuardrail":
        from .guardrails import BaseGuardrail

        return BaseGuardrail

    if name == "GuardrailChain":
        from .guardrails import GuardrailChain

        return GuardrailChain

    if name == "GuardrailResult":
        from .guardrails import GuardrailResult

        return GuardrailResult

    if name == "GuardrailAction":
        from .guardrails import GuardrailAction

        return GuardrailAction

    if name == "GuardrailRemediationNeeded":
        from .guardrails import GuardrailRemediationNeeded

        return GuardrailRemediationNeeded

    if name == "PIIDetector":
        from .guardrails import PIIDetector

        return PIIDetector

    if name == "ToxicityDetector":
        from .guardrails import ToxicityDetector

        return ToxicityDetector

    if name == "HallucinationDetector":
        from .guardrails import HallucinationDetector

        return HallucinationDetector

    if name == "PromptInjectionDetector":
        from .guardrails import PromptInjectionDetector

        return PromptInjectionDetector

    # Pytest Integration (Gap Fix)
    if name == "AigieTestCase":
        from .pytest_plugin import AigieTestCase

        return AigieTestCase

    if name == "aigie_assert":
        from .pytest_plugin import aigie_assert

        return aigie_assert

    if name == "assert_test":
        from .pytest_plugin import assert_test

        return assert_test

    # UUID v7 (Gap Fix)
    if name == "uuidv7":
        from .uuid7 import uuidv7

        return uuidv7

    if name == "extract_timestamp":
        from .uuid7 import extract_timestamp

        return extract_timestamp

    if name == "is_valid_uuidv7":
        from .uuid7 import is_valid_uuidv7

        return is_valid_uuidv7

    if name == "uuidv7_to_datetime":
        from .uuid7 import uuidv7_to_datetime

        return uuidv7_to_datetime

    if name == "compare_uuidv7":
        from .uuid7 import compare_uuidv7

        return compare_uuidv7

    if name == "generate_batch_uuidv7":
        from .uuid7 import generate_batch_uuidv7

        return generate_batch_uuidv7

    if name == "uuidv7_with_timestamp":
        from .uuid7 import uuidv7_with_timestamp

        return uuidv7_with_timestamp

    if name == "get_uuidv7_age":
        from .uuid7 import get_uuidv7_age

        return get_uuidv7_age

    # Sampling System (Gap Fix)
    if name == "Sampler":
        from .sampling import Sampler

        return Sampler

    if name == "SamplingConfig":
        from .sampling import SamplingConfig

        return SamplingConfig

    if name == "AdaptiveConfig":
        from .sampling import AdaptiveConfig

        return AdaptiveConfig

    if name == "create_smart_sampler":
        from .sampling import create_smart_sampler

        return create_smart_sampler

    if name == "create_adaptive_sampler":
        from .sampling import create_adaptive_sampler

        return create_adaptive_sampler

    if name == "create_importance_function":
        from .sampling import create_importance_function

        return create_importance_function

    # Query API (Feature Parity)
    if name == "QueryAPI":
        from .query_api import QueryAPI

        return QueryAPI

    if name == "TraceAPI":
        from .query_api import TraceAPI

        return TraceAPI

    if name == "ObservationsAPI":
        from .query_api import ObservationsAPI

        return ObservationsAPI

    if name == "SessionsAPI":
        from .query_api import SessionsAPI

        return SessionsAPI

    if name == "ScoresAPI":
        from .query_api import ScoresAPI

        return ScoresAPI

    if name == "Trace":
        from .query_api import Trace

        return Trace

    if name == "Observation":
        from .query_api import Observation

        return Observation

    if name == "ObservationType":
        from .query_api import ObservationType

        return ObservationType

    if name == "TraceFilter":
        from .query_api import TraceFilter

        return TraceFilter

    if name == "PaginatedResponse":
        from .query_api import PaginatedResponse

        return PaginatedResponse

    # DataFrame Export Functions
    if name == "traces_to_dataframe":
        from .query_api import traces_to_dataframe

        return traces_to_dataframe

    if name == "observations_to_dataframe":
        from .query_api import observations_to_dataframe

        return observations_to_dataframe

    # Human Annotations (Feature Parity)
    if name == "AnnotationsAPI":
        from .annotations import AnnotationsAPI

        return AnnotationsAPI

    if name == "AnnotationQueue":
        from .annotations import AnnotationQueue

        return AnnotationQueue

    if name == "Annotation":
        from .annotations import Annotation

        return Annotation

    if name == "AnnotationType":
        from .annotations import AnnotationType

        return AnnotationType

    if name == "AnnotationTask":
        from .annotations import AnnotationTask

        return AnnotationTask

    # Playground (Feature Parity)
    if name == "Playground":
        from .playground import Playground

        return Playground

    if name == "PromptRegistry":
        from .playground import PromptRegistry

        return PromptRegistry

    if name == "PromptTemplate":
        from .playground import PromptTemplate

        return PromptTemplate

    if name == "PlaygroundRun":
        from .playground import PlaygroundRun

        return PlaygroundRun

    if name == "ComparisonResult":
        from .playground import ComparisonResult

        return ComparisonResult

    if name == "ModelConfig":
        from .playground import ModelConfig

        return ModelConfig

    if name == "ModelProvider":
        from .playground import ModelProvider

        return ModelProvider

    if name == "create_playground":
        from .playground import create_playground

        return create_playground

    # Agent Graph View (Feature Parity)
    if name == "AgentGraph":
        from .graph_view import AgentGraph

        return AgentGraph

    if name == "GraphBuilder":
        from .graph_view import GraphBuilder

        return GraphBuilder

    if name == "GraphNode":
        from .graph_view import GraphNode

        return GraphNode

    if name == "GraphEdge":
        from .graph_view import GraphEdge

        return GraphEdge

    if name == "NodeType":
        from .graph_view import NodeType

        return NodeType

    if name == "EdgeType":
        from .graph_view import EdgeType

        return EdgeType

    if name == "NodeStatus":
        from .graph_view import NodeStatus

        return NodeStatus

    if name == "ExecutionPath":
        from .graph_view import ExecutionPath

        return ExecutionPath

    if name == "GraphMetrics":
        from .graph_view import GraphMetrics

        return GraphMetrics

    if name == "create_graph":
        from .graph_view import create_graph

        return create_graph

    if name == "create_graph_builder":
        from .graph_view import create_graph_builder

        return create_graph_builder

    # Alerting (Feature Parity)
    if name == "AlertManager":
        from .alerting import AlertManager

        return AlertManager

    if name == "AlertRule":
        from .alerting import AlertRule

        return AlertRule

    if name == "AlertEvent":
        from .alerting import AlertEvent

        return AlertEvent

    if name == "AlertCondition":
        from .alerting import AlertCondition

        return AlertCondition

    if name == "AlertSeverity":
        from .alerting import AlertSeverity

        return AlertSeverity

    if name == "AlertStatus":
        from .alerting import AlertStatus

        return AlertStatus

    if name == "MetricType":
        from .alerting import MetricType

        return MetricType

    if name == "ComparisonOperator":
        from .alerting import ComparisonOperator

        return ComparisonOperator

    if name == "AggregationWindow":
        from .alerting import AggregationWindow

        return AggregationWindow

    if name == "NotificationChannel":
        from .alerting import NotificationChannel

        return NotificationChannel

    if name == "SlackChannel":
        from .alerting import SlackChannel

        return SlackChannel

    if name == "EmailChannel":
        from .alerting import EmailChannel

        return EmailChannel

    if name == "WebhookChannel":
        from .alerting import WebhookChannel

        return WebhookChannel

    if name == "PagerDutyChannel":
        from .alerting import PagerDutyChannel

        return PagerDutyChannel

    if name == "create_alert_manager":
        from .alerting import create_alert_manager

        return create_alert_manager

    # Span Replay (Feature Parity)
    if name == "SpanReplay":
        from .span_replay import SpanReplay

        return SpanReplay

    if name == "CapturedSpan":
        from .span_replay import CapturedSpan

        return CapturedSpan

    if name == "ReplayResult":
        from .span_replay import ReplayResult

        return ReplayResult

    if name == "ReplayExperiment":
        from .span_replay import ReplayExperiment

        return ReplayExperiment

    if name == "ReplayStatus":
        from .span_replay import ReplayStatus

        return ReplayStatus

    if name == "create_span_replay":
        from .span_replay import create_span_replay

        return create_span_replay

    # Leaderboards (Feature Parity)
    if name == "LeaderboardManager":
        from .leaderboards import LeaderboardManager

        return LeaderboardManager

    if name == "Leaderboard":
        from .leaderboards import Leaderboard

        return Leaderboard

    if name == "LeaderboardEntry":
        from .leaderboards import LeaderboardEntry

        return LeaderboardEntry

    if name == "ComparisonPair":
        from .leaderboards import ComparisonPair

        return ComparisonPair

    if name == "EloRating":
        from .leaderboards import EloRating

        return EloRating

    if name == "RankingMetric":
        from .leaderboards import RankingMetric

        return RankingMetric

    if name == "AggregationType":
        from .leaderboards import AggregationType

        return AggregationType

    if name == "create_leaderboard_manager":
        from .leaderboards import create_leaderboard_manager

        return create_leaderboard_manager

    if name == "create_model_leaderboard":
        from .leaderboards import create_model_leaderboard

        return create_model_leaderboard

    if name == "create_prompt_leaderboard":
        from .leaderboards import create_prompt_leaderboard

        return create_prompt_leaderboard

    # License Management (Self-Hosted)
    if name == "LicenseValidator":
        from .licensing import LicenseValidator

        return LicenseValidator

    if name == "LicenseInfo":
        from .licensing import LicenseInfo

        return LicenseInfo

    if name == "UsageSummary":
        from .licensing import UsageSummary

        return UsageSummary

    if name == "LicenseError":
        from .licensing import LicenseError

        return LicenseError

    if name == "LicenseExpiredError":
        from .licensing import LicenseExpiredError

        return LicenseExpiredError

    if name == "LicenseRevokedError":
        from .licensing import LicenseRevokedError

        return LicenseRevokedError

    if name == "LicenseLimitExceededError":
        from .licensing import LicenseLimitExceededError

        return LicenseLimitExceededError

    # Telemetry (SDK Feature Tracking)
    if name == "track_feature":
        from .licensing import track_feature

        return track_feature

    if name == "record_error":
        from .licensing import record_error

        return record_error

    if name == "FeatureTracker":
        from .licensing import FeatureTracker

        return FeatureTracker

    if name == "ErrorCollector":
        from .licensing import ErrorCollector

        return ErrorCollector

    # Agent Observability (new!)
    if name == "LoopDetector":
        from .agents import LoopDetector

        return LoopDetector

    if name == "TracingLoopDetector":
        from .agents import TracingLoopDetector

        return TracingLoopDetector

    if name == "LoopAction":
        from .agents import LoopAction

        return LoopAction

    if name == "LoopState":
        from .agents import LoopState

        return LoopState

    if name == "LoopDetectionResult":
        from .agents import LoopDetectionResult

        return LoopDetectionResult

    if name == "GoalTracker":
        from .agents import GoalTracker

        return GoalTracker

    if name == "TracingGoalTracker":
        from .agents import TracingGoalTracker

        return TracingGoalTracker

    if name == "Goal":
        from .agents import Goal

        return Goal

    if name == "Step":
        from .agents import Step

        return Step

    if name == "StepStatus":
        from .agents import StepStatus

        return StepStatus

    if name == "Deviation":
        from .agents import Deviation

        return Deviation

    if name == "DeviationType":
        from .agents import DeviationType

        return DeviationType

    if name == "PlanMetrics":
        from .agents import PlanMetrics

        return PlanMetrics

    if name == "ExecutionCycle":
        from .agents import ExecutionCycle

        return ExecutionCycle

    if name == "CyclePhase":
        from .agents import CyclePhase

        return CyclePhase

    if name == "PhaseContext":
        from .agents import PhaseContext

        return PhaseContext

    if name == "PhaseResult":
        from .agents import PhaseResult

        return PhaseResult

    if name == "CycleMetrics":
        from .agents import CycleMetrics

        return CycleMetrics

    if name == "MultiCycleExecutor":
        from .agents import MultiCycleExecutor

        return MultiCycleExecutor

    if name == "LoopDetectedError":
        from .exceptions import LoopDetectedError

        return LoopDetectedError

    # Agent Framework
    if name == "Agent":
        from .agent import Agent

        return Agent

    if name == "RunContext":
        from .run_context import RunContext

        return RunContext

    if name == "Message":
        from .run_context import Message

        return Message

    if name == "ModelRetry":
        from .run_context import ModelRetry

        return ModelRetry

    if name == "get_current_context":
        from .run_context import get_current_context

        return get_current_context

    if name == "get_current_context_or_none":
        from .run_context import get_current_context_or_none

        return get_current_context_or_none

    if name == "set_current_context":
        from .run_context import set_current_context

        return set_current_context

    if name == "reset_current_context":
        from .run_context import reset_current_context

        return reset_current_context

    if name == "run_context":
        from .run_context import run_context

        return run_context

    if name == "AgentResult":
        from .result import AgentResult

        return AgentResult

    if name == "StreamedRunResult":
        from .result import StreamedRunResult

        return StreamedRunResult

    if name == "UsageInfo":
        from .result import UsageInfo

        return UsageInfo

    if name == "UnifiedError":
        from .result import UnifiedError

        return UnifiedError

    if name == "Tool":
        from .tools import Tool

        return Tool

    if name == "ToolCall":
        from .tools import ToolCall

        return ToolCall

    if name == "ToolResult":
        from .tools import ToolResult

        return ToolResult

    if name == "ToolRegistry":
        from .tools import ToolRegistry

        return ToolRegistry

    if name == "tool":
        from .tools import tool

        return tool

    if name == "create_tool_registry":
        from .tools import create_tool_registry

        return create_tool_registry

    if name == "execute_tool":
        from .tools import execute_tool

        return execute_tool

    if name == "tools_to_openai_functions":
        from .tools import tools_to_openai_functions

        return tools_to_openai_functions

    if name == "tools_to_anthropic_tools":
        from .tools import tools_to_anthropic_tools

        return tools_to_anthropic_tools

    if name == "type_to_json_schema":
        from .schemas import type_to_json_schema

        return type_to_json_schema

    if name == "generate_json_schema":
        from .schemas import generate_json_schema

        return generate_json_schema

    # Types (for type hints and validation)
    if name == "TraceStatus":
        from .types import TraceStatus

        return TraceStatus

    if name == "SpanStatus":
        from .types import SpanStatus

        return SpanStatus

    if name == "SpanType":
        from .types import SpanType

        return SpanType

    if name == "ObservationLevel":
        from .types import ObservationLevel

        return ObservationLevel

    if name == "FailureCategory":
        from .types import FailureCategory

        return FailureCategory

    if name == "TokenUsage":
        from .types import TokenUsage

        return TokenUsage

    if name == "TraceResponse":
        from .types import TraceResponse

        return TraceResponse

    if name == "SpanResponse":
        from .types import SpanResponse

        return SpanResponse

    # Platform API Clients - Analytics
    if name == "AnalyticsClient":
        from .analytics import AnalyticsClient

        return AnalyticsClient

    if name == "DashboardStats":
        from .analytics import DashboardStats

        return DashboardStats

    if name == "TimeSeriesPoint":
        from .analytics import TimeSeriesPoint

        return TimeSeriesPoint

    if name == "WorkflowStats":
        from .analytics import WorkflowStats

        return WorkflowStats

    if name == "ErrorSummary":
        from .analytics import ErrorSummary

        return ErrorSummary

    if name == "ErrorCluster":
        from .analytics import ErrorCluster

        return ErrorCluster

    if name == "CostAnalytics":
        from .analytics import CostAnalytics

        return CostAnalytics

    if name == "AgentStats":
        from .analytics import AgentStats

        return AgentStats

    # Platform API Clients - Workflows
    if name == "WorkflowsClient":
        from .workflows import WorkflowsClient

        return WorkflowsClient

    if name == "WorkflowDefinition":
        from .workflows import WorkflowDefinition

        return WorkflowDefinition

    if name == "WorkflowExecution":
        from .workflows import WorkflowExecution

        return WorkflowExecution

    if name == "WorkflowStep":
        from .workflows import WorkflowStep

        return WorkflowStep

    # Platform API Clients - Recommendations
    if name == "RecommendationsClient":
        from .recommendations import RecommendationsClient

        return RecommendationsClient

    if name == "TraceRecommendation":
        from .recommendations import TraceRecommendation

        return TraceRecommendation

    if name == "WorkflowRecommendation":
        from .recommendations import WorkflowRecommendation

        return WorkflowRecommendation

    if name == "ImpactAnalysis":
        from .recommendations import ImpactAnalysis

        return ImpactAnalysis

    # Platform API Clients - Learning
    if name == "LearningClient":
        from .learning import LearningClient

        return LearningClient

    if name == "LearningStats":
        from .learning import LearningStats

        return LearningStats

    if name == "LearningPattern":
        from .learning import LearningPattern

        return LearningPattern

    if name == "FeedbackEntry":
        from .learning import FeedbackEntry

        return FeedbackEntry

    if name == "EvalStats":
        from .learning import EvalStats

        return EvalStats

    # Platform API Clients - Remediation
    if name == "RemediationClient":
        from .remediation import RemediationClient

        return RemediationClient

    if name == "RemediationJob":
        from .remediation import RemediationJob

        return RemediationJob

    if name == "QueueStats":
        from .remediation import QueueStats

        return QueueStats

    if name == "AutonomousPreview":
        from .remediation import AutonomousPreview

        return AutonomousPreview

    if name == "HallucinationDetection":
        from .remediation import HallucinationDetection

        return HallucinationDetection

    if name == "ControlLoopStatus":
        from .remediation import ControlLoopStatus

        return ControlLoopStatus

    # Integration Registry (LiteLLM-style patching)
    if name == "patch":
        from .integrations.registry import patch

        return patch

    if name == "unpatch":
        from .integrations.registry import unpatch

        return unpatch

    if name == "is_patched":
        from .integrations.registry import is_patched

        return is_patched

    if name == "is_integration_available":
        from .integrations.registry import is_integration_available

        return is_integration_available

    if name == "list_integrations":
        from .integrations.registry import list_integrations

        return list_integrations

    if name == "list_integration_names":
        from .integrations.registry import list_integration_names

        return list_integration_names

    if name == "get_patched_integrations":
        from .integrations.registry import get_patched_integrations

        return get_patched_integrations

    if name == "register_integration":
        from .integrations.registry import register_integration

        return register_integration

    if name == "patch_all":
        from .integrations.registry import patch_all

        return patch_all

    # Exceptions
    if name == "AigieError":
        from .exceptions import AigieError

        return AigieError

    if name == "ContextDriftDetected":
        from .exceptions import ContextDriftDetected

        return ContextDriftDetected

    if name == "TopicDriftDetected":
        from .exceptions import TopicDriftDetected

        return TopicDriftDetected

    if name == "BehaviorDriftDetected":
        from .exceptions import BehaviorDriftDetected

        return BehaviorDriftDetected

    if name == "QualityDriftDetected":
        from .exceptions import QualityDriftDetected

        return QualityDriftDetected

    if name == "RemediationFailed":
        from .exceptions import RemediationFailed

        return RemediationFailed

    if name == "RemediationRejected":
        from .exceptions import RemediationRejected

        return RemediationRejected

    if name == "RetryExhausted":
        from .exceptions import RetryExhausted

        return RetryExhausted

    if name == "TraceBufferError":
        from .exceptions import TraceBufferError

        return TraceBufferError

    if name == "TraceContextError":
        from .exceptions import TraceContextError

        return TraceContextError

    if name == "InterceptionBlocked":
        from .exceptions import InterceptionBlocked

        return InterceptionBlocked

    if name == "InterceptionRetryRequested":
        from .exceptions import InterceptionRetryRequested

        return InterceptionRetryRequested

    if name == "ConfigurationError":
        from .exceptions import ConfigurationError

        return ConfigurationError

    if name == "IntegrationError":
        from .exceptions import IntegrationError

        return IntegrationError

    if name == "IntegrationNotFoundError":
        from .exceptions import IntegrationNotFoundError

        return IntegrationNotFoundError

    if name == "IntegrationNotInstalledError":
        from .exceptions import IntegrationNotInstalledError

        return IntegrationNotInstalledError

    if name == "BackendError":
        from .exceptions import BackendError

        return BackendError

    if name == "BackendConnectionError":
        from .exceptions import BackendConnectionError

        return BackendConnectionError

    if name == "RateLimitError":
        from .exceptions import RateLimitError

        return RateLimitError

    if name == "AuthenticationError":
        from .exceptions import AuthenticationError

        return AuthenticationError

    if name == "WebhookError":
        from .exceptions import WebhookError

        return WebhookError

    # Callbacks
    if name == "GenericWebhookCallback":
        from .callbacks import GenericWebhookCallback

        return GenericWebhookCallback

    if name == "BaseCallback":
        from .callbacks import BaseCallback

        return BaseCallback

    if name == "CallbackEvent":
        from .callbacks import CallbackEvent

        return CallbackEvent

    if name == "CallbackEventType":
        from .callbacks import CallbackEventType

        return CallbackEventType

    if name == "create_webhook":
        from .callbacks.generic_webhook import create_webhook

        return create_webhook

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


# Type checking support
if TYPE_CHECKING:
    from .agents import (
        CycleMetrics,
        CyclePhase,
        Deviation,
        DeviationType,
        ExecutionCycle,
        Goal,
        GoalTracker,
        LoopAction,
        LoopDetectionResult,
        LoopDetector,
        LoopState,
        MultiCycleExecutor,
        PhaseContext,
        PhaseResult,
        PlanMetrics,
        Step,
        StepStatus,
        TracingGoalTracker,
        TracingLoopDetector,
    )
    from .alerting import (
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
    from .analytics import (
        AgentStats,
        AnalyticsClient,
        CostAnalytics,
        DashboardStats,
        ErrorCluster,
        ErrorSummary,
        TimeSeriesPoint,
        WorkflowStats,
    )
    from .annotations import (
        Annotation,
        AnnotationQueue,
        AnnotationsAPI,
        AnnotationTask,
        AnnotationType,
    )
    from .batch_evaluation import (
        BatchEvaluationResult,
        BatchProgress,
        BatchStatistics,
        TestCaseResult,
        enhanced_batch_evaluate,
        export_batch_results,
        export_batch_results_to_csv,
        generate_batch_report,
    )
    from .buffer import EventBuffer
    from .callbacks import (
        BaseCallback,
        CallbackEvent,
        CallbackEventType,
        GenericWebhookCallback,
    )
    from .callbacks.generic_webhook import create_webhook
    from .client import Aigie
    from .compression import Compressor, is_compression_available
    from .config import Config
    from .context import (
        TraceContext as W3CTraceContext,
    )
    from .context import (
        extract_trace_context,
        inject_trace_context,
    )
    from .context_manager import (
        get_current_span_context,
        get_current_trace_context,
        is_tracing_enabled,
        set_tracing_enabled,
        tracing_context,
    )
    from .cost_tracking import (
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
    from .decorators_v3 import (
        create_traceable,
        set_debug_mode,
        set_global_mask_fn,
        trace,
        traceable,
    )
    from .evaluation import EvaluationHook, EvaluationResult, Evaluator, ScoreType
    from .evaluations import (
        EvaluationJob,
        EvaluationRequest,
        EvaluationsClient,
        EvaluationScore,
        EvaluationTemplate,
        EvaluationType,
        evaluate,
    )
    from .exceptions import (
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
    from .experiments import (
        ExperimentResult,
        ExperimentsClient,
        ExperimentVariant,
        VariantResult,
        VariantStatistics,
        WinnerInfo,
        create_experiments_client,
        generate_experiment_report,
    )
    from .graph_view import (
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
    from .guardrails import (
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
    from .integrations.registry import (
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
    from .judges import (
        Judge,
        JudgeConfig,
        JudgeResult,
        JudgesClient,
        JudgeType,
        judge,
        judge_all,
    )
    from .leaderboards import (
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
    from .learning import (
        EvalStats,
        FeedbackEntry,
        LearningClient,
        LearningPattern,
        LearningStats,
    )
    from .licensing import (
        LicenseError,
        LicenseExpiredError,
        LicenseInfo,
        LicenseLimitExceededError,
        LicenseRevokedError,
        LicenseValidator,
        UsageSummary,
    )
    from .metrics.base import BaseMetric
    from .metrics.checkpoint import CheckpointValidityMetric
    from .metrics.drift import DriftDetectionMetric
    from .metrics.nested import NestedAgentHealthMetric
    from .metrics.recovery import RecoverySuccessMetric
    from .metrics.reliability import ProductionReliabilityMetric
    from .observe import observe
    from .playground import (
        ComparisonResult,
        ModelConfig,
        ModelProvider,
        Playground,
        PlaygroundRun,
        PromptRegistry,
        PromptTemplate,
        create_playground,
    )
    from .prompts import Prompt, PromptManager
    from .pytest_plugin import (
        AigieTestCase,
        aigie_assert,
        assert_test,
    )
    from .query_api import (
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
    from .recommendations import (
        ImpactAnalysis,
        RecommendationsClient,
        TraceRecommendation,
        WorkflowRecommendation,
    )
    from .remediation import (
        AutonomousPreview,
        ControlLoopStatus,
        HallucinationDetection,
        QueueStats,
        RemediationClient,
        RemediationJob,
    )
    from .safety_metrics import (
        BiasEvaluator,
        JailbreakEvaluator,
        PIILeakageEvaluator,
        PromptInjectionEvaluator,
        RedTeamScanner,
        ToxicityEvaluator,
        create_safety_evaluators,
    )
    from .sampling import (
        AdaptiveConfig,
        Sampler,
        SamplingConfig,
        create_adaptive_sampler,
        create_importance_function,
        create_smart_sampler,
    )
    from .span import SpanContext
    from .span_replay import (
        CapturedSpan,
        ReplayExperiment,
        ReplayResult,
        ReplayStatus,
        SpanReplay,
        create_span_replay,
    )
    from .streaming import StreamingSpan
    from .summary_evaluators import (
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
    from .trace import TraceContext
    from .uuid7 import (
        compare_uuidv7,
        extract_timestamp,
        generate_batch_uuidv7,
        get_uuidv7_age,
        is_valid_uuidv7,
        uuidv7,
        uuidv7_to_datetime,
        uuidv7_with_timestamp,
    )
    from .workflows import (
        WorkflowDefinition,
        WorkflowExecution,
        WorkflowsClient,
        WorkflowStep,
    )
    from .wrappers import wrap_anthropic, wrap_gemini, wrap_openai
    from .wrappers_bedrock import create_traced_bedrock, wrap_bedrock
    from .wrappers_cohere import create_traced_cohere, wrap_cohere


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
