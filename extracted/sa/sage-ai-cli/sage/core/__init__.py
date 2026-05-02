"""Sage core modules.

This package contains the core functionality for SAGE:
- Discovery: File and project discovery
- Task prioritization: Intelligent task ordering
- Prompts: System prompts and templates
- Validation: Code and content validation
- Shell: Safe shell execution utilities
- Project: Project structure detection
- Languages: Language and framework detection
- Commands: Safe command execution
- Dependencies: Dependency graph management
- Awareness: Repository awareness tracking
- Diagnostics: LSP and static analysis
- Prioritization: Autopolit task prioritization
- Security: Security auditing
- Swarm: Multi-agent orchestration
- Tools: Tool execution framework
- Checkpoint: Time travel checkpoint management

Enhanced modules (P0-P3 improvements):
- Errors: Unified error handling with actionable guidance
- Tokens: Token estimation, caching, and cost tracking
- Tasks: Task state machine and inter-task communication
- PromptSystem: Dynamic prompts, few-shot selection, A/B testing
- ToolExecutor: Enhanced tool execution with transactions
- Context: Semantic summarization and conversation branching
- CLIUtils: Output modes, config wizard, analytics dashboard
- GitIntegration: Git operations and workflow templates
- Enterprise: Audit logging, circuit breakers, DAG workflows

SAGE Agent Behavior Fixes (P0-P4 from failure analysis):
- RequestClassifier: Task type detection and output format enforcement
- ContextPersistence: Context preservation across turns
- GroundedSearch: Actual search execution and file verification
- ToolValidation: Tool execution validation and chaining
- ResponseGenerator: Response quality validation and concrete output
- AgentBehavior: Unified controller enforcing correct behavior
"""

from sage.core.agent_behavior import (
    AgentBehaviorController,
    AgentState,
    create_agent_controller,
    process_user_request,
)
from sage.core.awareness import (
    AwarenessContext,
    RepoAwareness,
    ScanCoverage,
    build_awareness_context,
)
from sage.core.checkpoint import (
    Checkpoint,
    CheckpointManager,
    FileChange,
    RestoreResult,
)
from sage.core.cli_utils import (
    AnalyticsDashboard,
    ConfigWizard,
    HelpSystem,
    ModelSelector,
    OutputHandler,
    OutputMode,
)

# ============================================================================
# Items 81-280: New Roadmap Modules
# ============================================================================
# Codebase Analyzer (Items 81-120)
from sage.core.codebase_analyzer import (
    CIConfig,
    CodeAnalysisResult,
    CodeAnalyzer,
    CodeComplexityMetrics,
    ContextBuilder,
    ContextWindow,
    DependencyInfo,
    Framework as CodebaseFramework,
    ModuleInfo,
    ProjectAnalysis,
    ProjectManifest as CodebaseManifest,
    ProjectStructureAnalyzer,
    ProjectType as CodebaseProjectType,
    TestFrameworkInfo,
)
from sage.core.commands import (
    ALLOWED_EXECUTABLES,
    BLOCKED_PATTERNS,
    DANGEROUS_FLAGS,
    CommandCategory,
    CommandResult,
    CommandRisk,
    CommandValidation,
    ParsedCommand,
    build_build_command,
    build_lint_command,
    build_test_command,
    execute_argv,
    execute_command,
    get_allowed_commands,
    is_command_allowed,
    parse_command,
    validate_command,
)
from sage.core.context import (
    BranchingConversation,
    ConversationBranch,
    ConversationSearch,
    ImportanceLevel,
    ImportanceRanker,
    SemanticTrimmer,
)
from sage.core.context_persistence import (
    ContextPersistenceManager,
    ConversationContext,
    FileReference,
    OriginalRequest,
    TaskProgress,
    create_context,
    load_or_create_context,
)
from sage.core.dependencies import (
    DependencyGraph,
    FileNode as DepFileNode,
    ImportInfo,
    get_imports_for_file,
)
from sage.core.diagnostics import (
    Diagnostic,
    DiagnosticResult,
    DiagnosticsClient,
    DiagnosticSeverity,
)
from sage.core.discovery import (
    DiscoveryResult,
    FileDiscovery,
    ProjectInfo,
    discover_files,
    discover_modules,
)
from sage.core.enterprise import (
    ApprovalRequest,
    ApprovalStatus,
    ApprovalWorkflow,
    AuditEntry,
    AuditLogger,
    CircuitBreaker,
    CircuitState,
    DAGNode,
    DAGWorkflowEngine,
    LogLevel,
    Metric,
    MetricsCollector,
    MetricType,
    NotificationChannel,
    NotificationManager,
    PolicyEngine,
    StructuredLogger,
)

# P0-P3 Enhanced modules
from sage.core.errors import (
    ErrorCategory,
    ErrorFormatter,
    ErrorGuidance,
    ErrorHandler,
    ErrorSeverity,
    SageError,
    SageException,
)
from sage.core.git_integration import (
    CommitMessage,
    CommitMessageGenerator,
    Git,
    WorkflowManager,
    WorkflowStep,
)
from sage.core.grounded_search import (
    FileReferenceValidator,
    GroundedSearch,
    SearchCommandExecutor,
    SearchQuery,
    SearchResponse,
    SearchResult,
    find_files_matching,
    search_codebase,
    verify_file_exists,
)

# New P1-P3 modules
from sage.core.languages import (
    BuildTool,
    DetectionResult,
    Framework,
    Language,
    LanguageInfo,
    PackageManager,
    ProjectManifest,
    TestFramework,
    detect_build_command,
    detect_format_command,
    detect_frameworks,
    detect_languages,
    detect_lint_command,
    detect_project_manifest,
    detect_test_framework,
    detect_type_check_command,
    get_language_for_extension,
    get_syntax_check_command,
)

# List Generator (Items 121-160)
from sage.core.list_generator import (
    ListFormatter,
    ListItem,
    ListItemQuality,
    ListQualityValidator,
    ProgressiveListBuilder,
)
from sage.core.plugin_system import (
    AIPluginPlanner,
    ImportedSkillAdapter,
    PluginCapability,
    PluginErrorType,
    PluginExecutor,
    PluginInvocation,
    PluginInvocationResult,
    PluginRegistry,
    build_default_plugin_registry,
    build_imported_skill_adapters,
)
from sage.core.prioritization import (
    AutopolitState,
    CIFailureAnalyzer,
    FlakeyTestTracker,
    PrioritizedTask as AutopolitTask,
    TaskPrioritizer as AutopolitPrioritizer,
)
from sage.core.project import (
    PROJECT_MARKERS,
    SKIP_DIRS,
    command_from_project_root,
    default_project_root,
    detect_runnable_files,
    detect_test_files,
    discover_npm_script,
    discover_project_full_test_command,
    discover_project_root_for_file,
    discover_project_test_command,
    discover_python_test_command,
    discover_workspace_project_roots,
    project_root_score,
    validation_command_for_written_files,
)
from sage.core.prompt_system import (
    ABTest,
    ABTestManager,
    DynamicPromptBuilder,
    FewShotExample,
    FewShotSelector,
    PromptCompressor,
    PromptGuard,
    PromptVersion,
)
from sage.core.prompts import (
    AGENT_SYSTEM_PROMPT_TEMPLATE,
    CHAIN_OF_THOUGHT_INSTRUCTIONS,
    LOCAL_AGENT_SYSTEM_PROMPT_TEMPLATE,
    build_agent_system_prompt,
)

# P1-12: Hard guardrail exceptions - these MUST stop execution
from sage.core.renderer import (
    FabricationViolation,
    GroundingViolation,
    HardGuardrailViolation,
    ToolSyntaxViolation,
)

# SAGE Agent Behavior Fixes (P0-P4)
from sage.core.request_classifier import (
    ClassifiedRequest,
    OutputFormat as RequestOutputFormat,
    RequestClassifier,
    RequestExpander,
    RequestType,
    ResponseValidation,
    ResponseValidator,
    classify_request,
    expand_request,
    validate_response as validate_request_response,
)
from sage.core.response_generator import (
    ConcreteResponseBuilder,
    ProgressTracker,
    ResponseQualityIssue,
    ResponseQualityValidator,
    ResponseValidationResult,
    check_response_quality,
    validate_response,
)

# ============================================================================
# 400-Item Roadmap Implementation (P0-P3)
# ============================================================================
# P0 Critical Items 1-130: Request Understanding, Output Enforcement, Instructions
from sage.core.roadmap_p0_implementation import (
    ClassifiedRequestV2,
    # Items 51-70: Code Generation Blocking
    CodeBlockerV2,
    ComplianceValidator,
    ExtractedInstruction,
    # Items 121-130: Follow-Through Validation
    FollowThroughValidator,
    # Items 91-120: Instruction Compliance
    InstructionExtractor,
    ListEnforcerV2,
    # Items 71-90: List Format Enforcement
    ListValidationResult,
    OutputFormatV2,
    # Integrated P0 System
    P0CriticalSystem,
    PipelineTypeV2,
    QuantityParser,
    # Items 1-20: Quantity Detection
    QuantityResult,
    RequestClassifierV2,
    # Items 21-50: Enhanced Request Classification
    RequestTypeV2,
    # Convenience functions
    classify_request_v2,
    get_quantity,
    should_block_code,
    strip_code_from_response,
    validate_response_v2,
)

# P1 Items 131-280: Response Quality, Structure, Codebase Analysis, Tool Orchestration
from sage.core.roadmap_p1_implementation import (
    CodebaseAnalyzer as RoadmapCodebaseAnalyzer,
    # Items 181-230: Codebase Analysis (with alias to avoid conflict)
    CodebaseContext,
    ContextWindowManager,
    FileReferenceValidator as RoadmapFileRefValidator,
    QualityAssessment,
    QualityDimension,
    ResponseDeduplicator,
    ResponseQualityAssessor,
    # Items 131-150: Response Quality Assessment
    ResponseQualityLevel,
    # Items 151-180: Response Structure Analysis
    ResponseSection,
    ResponseStructureAnalyzer,
    SearchStrategySelector,
    ToolCall as RoadmapToolCall,
    ToolOrchestrator as RoadmapToolOrchestrator,
    ToolSequence,
    # Items 231-280: Tool Orchestration
    ToolType as RoadmapToolType,
    ToolUsageTracker as RoadmapToolUsageTracker,
    analyze_codebase,
    # Convenience functions
    assess_response_quality,
    deduplicate_list,
    plan_tool_sequence,
    validate_file_references,
)

# P2/P3 Items 281-400: UX, Reliability, Caching, Metrics
from sage.core.roadmap_p2_p3_implementation import (
    # Items 321-360: Error Handling and Retry (with aliases)
    ErrorCategory as RoadmapErrorCategory,
    ErrorHandler as RoadmapErrorHandler,
    FeatureFlags,
    GracefulDegradation as RoadmapGracefulDegradation,
    IncrementalProcessor as RoadmapIncrementalProcessor,
    MetricsCollector as RoadmapMetricsCollector,
    OutputFormatter as RoadmapOutputFormatter,
    # Items 281-320: Progress Tracking and Output (with aliases)
    ProgressPhase as RoadmapProgressPhase,
    ProgressState as RoadmapProgressState,
    ProgressTracker as RoadmapProgressTracker,
    RetryPolicy as RoadmapRetryPolicy,
    SageError as RoadmapSageError,
    # Items 361-400: Caching, Metrics, Feature Flags
    SmartCache as RoadmapSmartCache,
    StreamingOutput as RoadmapStreamingOutput,
    create_cache,
    create_error_handler,
    create_metrics_collector,
    # Convenience functions
    create_progress_tracker,
    create_retry_policy,
    format_progress,
    with_retry,
)
from sage.core.security import (
    SecurityAuditor,
    SecurityFinding,
    SecuritySeverity,
)
from sage.core.shell import (
    extract_bash_blocks,
    extract_scoped_prefix,
    read_file_context,
    resolve_scoped_directory,
    run_shell,
    safe_shell_exec,
    sanitize_shell_block,
    shell_quote,
    strip_search_comment,
)
from sage.core.swarm import (
    ModelProfile,
    SwarmOrchestrator,
    SwarmResult,
    SwarmTask,
    TaskType as SwarmTaskType,
)
from sage.core.task_priority import (
    CheckClass,
    PrioritizedTask,
    TaskCategory,
    TaskPrioritizer,
)
from sage.core.tasks import (
    RetryHandler,
    Task,
    TaskBus,
    TaskEvent,
    TaskManager,
    TaskPriority,
    TaskProgressDisplay,
    TaskResult,
    TaskState,
    TaskTransition,
    VALID_TRANSITIONS,
    create_progress_display,
    create_task_manager,
)
from sage.core.tokens import (
    CacheEntry,
    CostTracker,
    GenerationCache,
    TokenEstimate,
    TokenEstimator,
    UsageRecord,
)
from sage.core.tool_executor import (
    FileTransaction,
    ResourceMonitor,
    ResourceUsage,
    SafeShellExecutor,
    ToolChain,
)

# Tool Orchestrator (Items 161-200)
from sage.core.tool_orchestrator import (
    FileMetadata,
    FileReadStrategy,
    QueryAnalyzer,
    ReadRequest,
    ReadResult,
    SearchEngine,
    SearchQuery as OrchestratorSearchQuery,
    SearchResult as OrchestratorSearchResult,
    SearchStrategy,
    SmartFileReader,
    ToolCall as OrchestratorToolCall,
    ToolOrchestrator,
    ToolResult as OrchestratorToolResult,
    ToolType as OrchestratorToolType,
    ToolUsageTracker,
)
from sage.core.tool_validation import (
    ToolCall,
    ToolChain as ValidationToolChain,
    ToolExecutionValidator,
    ToolExecutor as ValidationToolExecutor,
    ToolOutputParser,
    ToolSelectionHeuristics,
    ToolStatus,
    ToolType as ValidationToolType,
    execute_tool,
    validate_tool_execution,
)
from sage.core.tools import (
    FileReadTool,
    FileWriteTool,
    SearchTool,
    ShellTool,
    ToolContext,
    ToolExecutor,
    ToolResult,
    ToolType,
    WebFetchTool,
)

# UX and Reliability (Items 201-280)
from sage.core.ux_reliability import (
    CacheEntry as UXCacheEntry,
    CacheStrategy,
    ErrorCategory as UXErrorCategory,
    ErrorHandler as UXErrorHandler,
    GracefulDegradation,
    IncrementalProcessor,
    MetricsCollector as UXMetricsCollector,
    OutputFormatter as UXOutputFormatter,
    ProgressPhase,
    ProgressState,
    ProgressTracker as UXProgressTracker,
    QualityAssurance,
    RetryPolicy,
    SageError as UXSageError,
    SmartCache,
    StreamingOutput,
    TestFramework as UXTestFramework,
)
from sage.core.validation import (
    COMMON_PACKAGES,
    LIKELY_HALLUCINATED_PATTERNS,
    STDLIB_MODULES,
    extract_imports_from_python,
    is_garbage_content,
    is_likely_hallucinated_code,
    module_exists_in_codebase,
    pending_modules_for_files,
    pre_validate_content,
    validate_imports_in_content,
    validate_json_syntax,
    validate_python_syntax,
)

__all__ = [
    # Discovery
    "FileDiscovery",
    "DiscoveryResult",
    "ProjectInfo",
    "discover_files",
    "discover_modules",
    # Task prioritization (original)
    "TaskPrioritizer",
    "TaskCategory",
    "CheckClass",
    "PrioritizedTask",
    # Prompts
    "CHAIN_OF_THOUGHT_INSTRUCTIONS",
    "AGENT_SYSTEM_PROMPT_TEMPLATE",
    "LOCAL_AGENT_SYSTEM_PROMPT_TEMPLATE",
    "build_agent_system_prompt",
    # Validation
    "validate_python_syntax",
    "validate_json_syntax",
    "pre_validate_content",
    "extract_imports_from_python",
    "pending_modules_for_files",
    "module_exists_in_codebase",
    "validate_imports_in_content",
    "is_likely_hallucinated_code",
    "is_garbage_content",
    "STDLIB_MODULES",
    "COMMON_PACKAGES",
    "LIKELY_HALLUCINATED_PATTERNS",
    # Shell utilities
    "extract_scoped_prefix",
    "resolve_scoped_directory",
    "run_shell",
    "shell_quote",
    "extract_bash_blocks",
    "sanitize_shell_block",
    "strip_search_comment",
    "read_file_context",
    # Project discovery
    "detect_test_files",
    "detect_runnable_files",
    "discover_workspace_project_roots",
    "project_root_score",
    "default_project_root",
    "discover_npm_script",
    "discover_python_test_command",
    "discover_project_test_command",
    "discover_project_full_test_command",
    "discover_project_root_for_file",
    "command_from_project_root",
    "validation_command_for_written_files",
    "PROJECT_MARKERS",
    "SKIP_DIRS",
    # Languages and frameworks (P1)
    "Language",
    "PackageManager",
    "TestFramework",
    "BuildTool",
    "Framework",
    "LanguageInfo",
    "ProjectManifest",
    "DetectionResult",
    "detect_languages",
    "detect_project_manifest",
    "detect_test_framework",
    "detect_build_command",
    "detect_lint_command",
    "detect_format_command",
    "detect_type_check_command",
    "detect_frameworks",
    "get_syntax_check_command",
    "get_language_for_extension",
    # Safe commands (P0)
    "CommandCategory",
    "CommandRisk",
    "ParsedCommand",
    "CommandResult",
    "CommandValidation",
    "parse_command",
    "validate_command",
    "execute_command",
    "execute_argv",
    "is_command_allowed",
    "get_allowed_commands",
    "build_test_command",
    "build_lint_command",
    "build_build_command",
    "ALLOWED_EXECUTABLES",
    "BLOCKED_PATTERNS",
    "DANGEROUS_FLAGS",
    # Dependencies (P0)
    "DepFileNode",
    "ImportInfo",
    "DependencyGraph",
    "get_imports_for_file",
    # Awareness (P0)
    "ScanCoverage",
    "RepoAwareness",
    "AwarenessContext",
    "build_awareness_context",
    # Diagnostics (P1)
    "Diagnostic",
    "DiagnosticSeverity",
    "DiagnosticResult",
    "DiagnosticsClient",
    # Prioritization (P1)
    "AutopolitTask",
    "AutopolitPrioritizer",
    "AutopolitState",
    "FlakeyTestTracker",
    "CIFailureAnalyzer",
    # Security (P3)
    "SecurityFinding",
    "SecurityAuditor",
    "SecuritySeverity",
    # Swarm (P3)
    "SwarmTaskType",
    "SwarmTask",
    "ModelProfile",
    "SwarmOrchestrator",
    "SwarmResult",
    # Tools (P3)
    "ToolType",
    "ToolResult",
    "ToolContext",
    "ToolExecutor",
    "FileWriteTool",
    "FileReadTool",
    "ShellTool",
    "SearchTool",
    "WebFetchTool",
    # P1-12: Hard Guardrail Exceptions
    "HardGuardrailViolation",
    "GroundingViolation",
    "ToolSyntaxViolation",
    "FabricationViolation",
    # Checkpoint (P0)
    "FileChange",
    "Checkpoint",
    "CheckpointManager",
    "RestoreResult",
    # Errors - P0-11 to P0-20
    "ErrorCategory",
    "ErrorSeverity",
    "ErrorGuidance",
    "SageError",
    "SageException",
    "ErrorHandler",
    "ErrorFormatter",
    # Tokens - P1-21 to P1-23
    "TokenEstimate",
    "TokenEstimator",
    "CacheEntry",
    "GenerationCache",
    "UsageRecord",
    "CostTracker",
    # Tasks - P1-24 to P1-27
    "TaskState",
    "TaskPriority",
    "Task",
    "TaskEvent",
    "TaskBus",
    "TaskManager",
    # Prompt System - P1-28 to P1-35
    "FewShotExample",
    "FewShotSelector",
    "PromptGuard",
    "PromptVersion",
    "ABVariant",
    "ABTest",
    "ABTestManager",
    "PromptCompressor",
    "DynamicPromptBuilder",
    # Tool Executor - P1-36 to P1-50
    "ResourceUsage",
    "ResourceMonitor",
    "ToolChain",
    "SafeShellExecutor",
    "RateLimiter",
    "FileTransaction",
    "ToolRetryPolicy",
    "EnhancedToolExecutor",
    # Context - P1-51 to P1-60
    "ImportanceLevel",
    "ImportanceRanker",
    "ConversationBranch",
    "BranchingConversation",
    "SemanticTrimmer",
    "ContextSearcher",
    "ContextManager",
    # CLI Utils - P2-61 to P2-80
    "OutputFormat",
    "OutputHandler",
    "ConfigWizard",
    "ModelSelector",
    "CommandPalette",
    "AnalyticsDashboard",
    "HelpSystem",
    "ProgressReporter",
    # Git Integration - P2-81 to P2-105
    "ConflictStrategy",
    "Git",
    "CommitMessage",
    "CommitMessageGenerator",
    "MergeResult",
    "GitMerger",
    "WorkflowStep",
    "WorkflowManager",
    "GitHooksManager",
    # Enterprise - P3-106 to P3-125
    "LogLevel",
    "StructuredLogger",
    "AuditEvent",
    "AuditLogger",
    "CircuitState",
    "CircuitBreaker",
    "MetricType",
    "Metric",
    "MetricsCollector",
    "NotificationChannel",
    "NotificationManager",
    "PolicyRule",
    "PolicyEngine",
    "ApprovalStatus",
    "ApprovalRequest",
    "ApprovalWorkflow",
    "DAGNode",
    "DAGWorkflowEngine",
    # Request Classifier - P0-1 to P0-3
    "RequestType",
    "RequestOutputFormat",
    "ClassifiedRequest",
    "RequestClassifier",
    "RequestExpander",
    "ResponseValidation",
    "ResponseValidator",
    "classify_request",
    "expand_request",
    "validate_request_response",
    # Context Persistence - P0-4, P3-61 to P3-80
    "OriginalRequest",
    "TaskProgress",
    "FileReference",
    "ConversationContext",
    "ContextPersistenceManager",
    "create_context",
    "load_or_create_context",
    # Grounded Search - P1-21 to P1-40
    "SearchResult",
    "SearchQuery",
    "SearchResponse",
    "GroundedSearch",
    "FileReferenceValidator",
    "SearchCommandExecutor",
    "search_codebase",
    "verify_file_exists",
    "find_files_matching",
    # Tool Validation - P4-81 to P4-100
    "ValidationToolType",
    "ToolStatus",
    "ToolCall",
    "ValidationToolChain",
    "ToolExecutionValidator",
    "ValidationToolExecutor",
    "ToolOutputParser",
    "ToolSelectionHeuristics",
    "execute_tool",
    "validate_tool_execution",
    # Response Generator - P2-41 to P2-60
    "ResponseQualityIssue",
    "ResponseValidationResult",
    "ResponseQualityValidator",
    "ConcreteResponseBuilder",
    "ProgressTracker",
    "validate_response",
    "check_response_quality",
    # Agent Behavior Controller
    "AgentState",
    "AgentBehaviorController",
    "create_agent_controller",
    "process_user_request",
    # ============================================================================
    # Items 81-280: New Roadmap Exports
    # ============================================================================
    # Codebase Analyzer (Items 81-120)
    "CodebaseProjectType",
    "CodebaseFramework",
    "CodebaseManifest",
    "TestFrameworkInfo",
    "CIConfig",
    "DependencyInfo",
    "ModuleInfo",
    "ProjectAnalysis",
    "ProjectStructureAnalyzer",
    "CodeComplexityMetrics",
    "CodeAnalysisResult",
    "CodeAnalyzer",
    "ContextWindow",
    "ContextBuilder",
    # List Generator (Items 121-160)
    "ListItem",
    "ProgressiveListBuilder",
    "ListItemQuality",
    "ListQualityValidator",
    "ListFormatter",
    # Tool Orchestrator (Items 161-200)
    "SearchStrategy",
    "OrchestratorSearchQuery",
    "OrchestratorSearchResult",
    "SearchEngine",
    "QueryAnalyzer",
    "FileReadStrategy",
    "ReadRequest",
    "FileMetadata",
    "ReadResult",
    "SmartFileReader",
    "OrchestratorToolType",
    "OrchestratorToolCall",
    "OrchestratorToolResult",
    "ToolOrchestrator",
    "ToolUsageTracker",
    # UX and Reliability (Items 201-280)
    "ProgressPhase",
    "ProgressState",
    "UXProgressTracker",
    "StreamingOutput",
    "UXOutputFormatter",
    "UXErrorCategory",
    "UXSageError",
    "UXErrorHandler",
    "RetryPolicy",
    "GracefulDegradation",
    "CacheStrategy",
    "UXCacheEntry",
    "SmartCache",
    "IncrementalProcessor",
    "UXMetricsCollector",
    "QualityAssurance",
    "UXTestFramework",
    # ============================================================================
    # 400-Item Roadmap Implementation (P0-P3)
    # ============================================================================
    # P0 Critical Items 1-130
    "QuantityResult",
    "QuantityParser",
    "RequestTypeV2",
    "OutputFormatV2",
    "PipelineTypeV2",
    "ClassifiedRequestV2",
    "RequestClassifierV2",
    "CodeBlockerV2",
    "ListValidationResult",
    "ListEnforcerV2",
    "InstructionExtractor",
    "ExtractedInstruction",
    "ComplianceValidator",
    "FollowThroughValidator",
    "P0CriticalSystem",
    "classify_request_v2",
    "validate_response_v2",
    "get_quantity",
    "should_block_code",
    "strip_code_from_response",
    # P1 Items 131-280
    "ResponseQualityLevel",
    "QualityDimension",
    "QualityAssessment",
    "ResponseQualityAssessor",
    "ResponseSection",
    "ResponseStructureAnalyzer",
    "ResponseDeduplicator",
    "CodebaseContext",
    "RoadmapCodebaseAnalyzer",
    "RoadmapFileRefValidator",
    "ContextWindowManager",
    "RoadmapToolType",
    "RoadmapToolCall",
    "ToolSequence",
    "RoadmapToolOrchestrator",
    "SearchStrategySelector",
    "RoadmapToolUsageTracker",
    "assess_response_quality",
    "analyze_codebase",
    "plan_tool_sequence",
    "validate_file_references",
    "deduplicate_list",
    # P2/P3 Items 281-400
    "RoadmapProgressPhase",
    "RoadmapProgressState",
    "RoadmapProgressTracker",
    "RoadmapStreamingOutput",
    "RoadmapOutputFormatter",
    "RoadmapErrorCategory",
    "RoadmapSageError",
    "RoadmapErrorHandler",
    "RoadmapRetryPolicy",
    "with_retry",
    "RoadmapGracefulDegradation",
    "RoadmapSmartCache",
    "RoadmapIncrementalProcessor",
    "RoadmapMetricsCollector",
    "FeatureFlags",
    "create_progress_tracker",
    "create_error_handler",
    "create_retry_policy",
    "create_cache",
    "create_metrics_collector",
    "format_progress",
    # Plugin system
    "PluginErrorType",
    "PluginCapability",
    "PluginInvocation",
    "PluginInvocationResult",
    "PluginRegistry",
    "PluginExecutor",
    "AIPluginPlanner",
    "ImportedSkillAdapter",
    "build_imported_skill_adapters",
    "build_default_plugin_registry",
]
