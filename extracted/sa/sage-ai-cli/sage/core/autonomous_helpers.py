from __future__ import annotations
import json as _json
import importlib
import logging
import os
import platform
import re
import shlex
import shutil
import signal
import subprocess
import sys
import threading
import time
from collections import Counter
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Annotated, Any

import typer

# Set up logger for SAGE
logger = logging.getLogger("sage")


def _ollama_pull_subprocess_timeout() -> float | None:
    """Seconds for `ollama pull` subprocess.run(..., timeout=...). None = no limit.

    Large downloads plus SHA256 verification on slow disks can exceed fixed windows.
    Set SAGE_OLLAMA_PULL_TIMEOUT_SEC to a positive number to cap (seconds); unset or 0 = unlimited.
    """
    raw = os.environ.get("SAGE_OLLAMA_PULL_TIMEOUT_SEC", "").strip()
    if not raw:
        return None
    try:
        sec = float(raw)
    except ValueError:
        return None
    if sec <= 0:
        return None
    return sec

from sage import __version__
from sage.codegen import (
    CodeAnalyzer,
    CodeValidator,
    StyleEnforcer,
)
from sage.config import (
    SageConfig,
    get_config_value,
    load_config,
    save_config,
    set_config_value,
)
from sage.core import renderer
from sage.core.ai_orchestration import AIOrchestrator
from sage.core.codebase_analyzer import (
    CodeAnalyzer as RepoCodeAnalyzer,
    analyze_project as _analyze_project_structure,
)
from sage.core.commands import (
    execute_command as _execute_command,
)
from sage.core.credentials import (
    bootstrap_project_credentials as _bootstrap_project_credentials,
    detect_target_cloud_provider as _detect_target_cloud_provider,
    normalize_cloud_provider as _normalize_cloud_provider,
)
from sage.core.context_persistence import (
    ContextPersistenceManager,
    TaskProgress,
)
from sage.core.discovery import (
    FileDiscovery,
)
from sage.core.engine import ConversationEngine
from sage.core.list_generator import (
    dedupe_numbered_list_items as _dedupe_numbered_list_items,
    extract_list_item_count as _extract_list_item_count,
    extract_list_items_detailed as _extract_list_items_detailed,
)
from sage.core.phd_agent import (
    AgentResult,
    PhDAgent,
    PhDAgentUI,
)
from sage.core.context_management import ContextCompactor
from sage.core.procedural_workflow import (
    ProceduralWorkflowOrchestrator,
    WorkflowResult,
    ExecutionPhase,
    PlanTask,
    ExecutionPlan,
    LearningEntry,
    IntelligentExecutionEngine,
    QualityGate,
    IncrementalValidator,
    FreeModelRouter,
    SelfHealingSystem,
    _has_errors,
    _summarize_test_output,
    _detect_broken_test_files,
    _detect_repetition,
    _discover_project_modules,
    _build_smart_error_context,
    _cleanup_broken_tests,
    _compute_response_hash,
    FailureLoopDetector,
)
# Back-compat alias — earlier callers / tests imported `_FailureLoopDetector`
# from sage.main directly. Keep working without forcing a rename across the
# rest of the codebase.
_FailureLoopDetector = FailureLoopDetector
from sage.core.project import (
    command_from_project_root as _command_from_project_root,
    default_project_root as _default_project_root,
    detect_runnable_files as _detect_runnable_files,
    discover_project_full_test_command as _discover_project_full_test_command,
    discover_project_test_command as _discover_project_test_command,
    validation_command_for_written_files as _validation_command_for_written_files,
)
from sage.core.prompts import (
    build_agent_system_prompt,
)
from sage.core.p0_request_classification import (
    ClassifiedRequestV2 as _ClassifiedRequest,
    RequestClassifierV2 as _RequestClassifier,
    RequestTypeV2 as _RequestType,
)
from sage.core.request_classifier import (
    EvidenceTracker as _EvidenceTracker,
    SynthesisGate as _SynthesisGate,
    validate_response as _validate_classified_response,
)
from sage.core.router import ProviderRouter
from sage.core.shell import (
    DockerSandbox,
    extract_bash_blocks as _extract_bash_blocks,
    extract_scoped_prefix as _extract_scoped_prefix,
    get_test_error_summary as _get_test_error_summary,
    has_test_errors as _has_test_errors,
    parse_test_output as _parse_test_output,
    portable_grep as _portable_grep,
    read_file_context as _read_file_context,
    resolve_scoped_directory as _resolve_scoped_directory,
    run_readonly_shell as _run_readonly_shell,
    run_shell as _run_shell,
    sanitize_shell_block as _sanitize_shell_block,
    shell_quote as _shell_quote,
    strip_search_comment as _strip_search_comment,
)
from sage.core.checkpoint import Checkpoint, CheckpointManager
from sage.core.security import SecurityFinding, SecurityAuditor
from sage.core.dependencies import FileNode, DependencyGraph
from sage.core.swarm import TaskType, SwarmTask, SwarmOrchestrator
from sage.core.updater import CLIAutoUpdater
from sage.core.task_priority import (
    TaskPrioritizer,
)
from sage.core.tdd import (
    TDDGate,
    _RetryProgressTracker,
    _normalize_retry_signature,
    validate_code_write as _validate_code_write,
)
from sage.core.tasks import TaskExecutionManager
from sage.core.controller import ControllerModel
from sage.core.memory import ProjectMemory
from sage.core.validation import (
    detect_hallucinated_duplicate as _detect_hallucinated_duplicate,
    extract_imports_from_python as _extract_imports_from_python,
    _find_actual_test_directory,
    is_garbage_content as _is_garbage_content,
    is_likely_hallucinated_code as _is_likely_hallucinated_code,
    module_exists_in_codebase as _module_exists_in_codebase,
    pending_modules_for_files as _pending_modules_for_files,
    pre_validate_content as _pre_validate_content,
    validate_file_path_against_codebase as _validate_file_path_against_codebase,
    validate_imports_in_content as _validate_imports_in_content,
)
from sage.execution import (
    AdaptiveExecutionEngine,
    ExecutionTask,
    RetryConfig,
    RetryStrategy,
    SmartRetryHandler,
    TaskPriority,
    TaskStatus,
)
from sage.models.catalog import (
    CATALOG_BY_NAME,
    MODEL_CATALOG,
    OLLAMA_CATALOG,
    OLLAMA_BY_NAME,
    get_ollama_models_by_category,
    get_recommended_models,
    get_recommended_ollama_models,
    refresh_catalog_from_remote,
    search_catalog,
    search_ollama_catalog,
)

# Kick off a background fetch of the canonical catalog (gs://sage-ai-models/
# catalog.json) so users always see the latest models without a SAGE upgrade.
# 1-hour local cache; failure is silent (hardcoded catalog stays as floor).
# Disable with SAGE_OFFLINE=1 in air-gapped / CI environments.
if not os.environ.get("SAGE_OFFLINE"):
    try:
        refresh_catalog_from_remote(background=True)
    except Exception:
        pass
from sage.models.downloader import (
    delete_model,
    download_model,
    is_downloaded,
    iter_unregistered_gguf_files,
    list_downloaded,
    list_ollama_pulled_models,
    register_model,
)
from sage.providers.base import Message, ModelInfo, ProviderBase
from sage.providers.gemini import GeminiProvider
from sage.providers.llama_cpp import LlamaCppProvider
from sage.providers.openai_compat import (
    OllamaProvider,
    build_openai_compat_providers,
)

# ══════════════════════════════════════════════════════════════════════════════
# ENHANCED AI CAPABILITIES - Advanced reasoning, code generation, and execution
# ══════════════════════════════════════════════════════════════════════════════
from sage.reasoning import (
    ChainOfThoughtReasoner,
    ErrorDiagnosis,
    ReasoningContext,
    SelfReflectionEngine,
)

# ══════════════════════════════════════════════════════════════════════════════
# RECOVERY PROMPT - Used when streaming is rejected due to invalid tool syntax
# ══════════════════════════════════════════════════════════════════════════════


_TOOL_FORMAT_RECOVERY_PROMPT = """
Your previous response was REJECTED. You MUST fix this NOW.

CRITICAL RULES:
1. Start your response with READ: or SEARCH: commands IMMEDIATELY
2. Do NOT list what you will do - just DO IT
3. Do NOT generate numbered lists until AFTER you have read files
4. Do NOT fabricate content - READ files first, then analyze

CORRECT RESPONSE FORMAT:
READ: sage/main.py
READ: backend/app.py
SEARCH: **/*.py

[After reading, then provide analysis based on what you found]

WRONG (WILL BE REJECTED AGAIN):
- "I will read..." ❌
- "Let me analyze..." ❌
- "1. Issue A, 2. Issue B..." without reading files first ❌
- Plans or explanations before executing tools ❌

START YOUR RESPONSE WITH: READ: <actual_file_path>
""".strip()

# ══════════════════════════════════════════════════════════════════════════════
# REQUEST CLASSIFICATION STATE - Enforces correct behavior per request type
# ══════════════════════════════════════════════════════════════════════════════

# Global request classifier instance (thread-local in production)
_request_classifier = _RequestClassifier()

# Current request classification - ENFORCED during file writing
_current_classification: _ClassifiedRequest | None = None

# When True, the classifier will mark every request as IMPLEMENTATION mode so
# FILE: writes are not rejected as "MODE VIOLATION". Used by `sage run --prompt`
# (the SMS bridge entry point) where there's no human in the loop to "approve
# implementation" — the texted task IS the approval.
_force_implementation_mode: bool = False

# Current working directory - Used for session persistence across turns
_current_cwd: Path | None = None

_llama_cpp_runtime_bootstrap_attempted = False
_llama_cpp_runtime_bootstrap_error: str | None = None


def _set_current_cwd(cwd: Path) -> None:
    """Set the current working directory for session persistence."""
    global _current_cwd
    _current_cwd = cwd


def _get_current_cwd() -> Path | None:
    """Get the current working directory."""
    return _current_cwd


def _run_startup_context(cwd: Path) -> None:
    """`.env` gitignore / optional GitHub secret sync + git (and optional CI) hints."""
    try:
        from sage.core.env_sync import run_startup_env_maintenance

        for msg in run_startup_env_maintenance(cwd):
            renderer.info(msg)
    except Exception as exc:
        logger.debug("Startup env maintenance skipped: %s", exc)
    try:
        from sage.core.startup_hints import run_startup_devops_hints

        for msg in run_startup_devops_hints(cwd):
            renderer.info(msg)
    except Exception as exc:
        logger.debug("Startup devops hints skipped: %s", exc)


def _classify_and_store_request(user_input: str) -> _ClassifiedRequest:
    """Classify user request and store for enforcement during response processing.

    Also resets the evidence tracker for the new request.
    Also sets the session mode for cross-turn persistence.
    """
    from sage.main import _add_session_pending_task, _set_session_mode
    global _current_classification
    _current_classification = _request_classifier.classify(user_input)

    # SMS bridge / non-interactive override: when --prompt is set, the user
    # has explicitly requested an action over a channel where they can't
    # follow up with "yes, implement it". Force IMPLEMENTATION classification
    # so FILE: writes don't get rejected as "MODE VIOLATION: read-only analysis".
    if _force_implementation_mode and _current_classification is not None:
        try:
            _current_classification.read_only = False
            _current_classification.request_type = _RequestType.IMPLEMENTATION
        except Exception:
            pass  # Object may be immutable in some classifier versions; safe to ignore.

    # Ensure is_informational is set for all classification objects (V1/V2 compatibility)
    if not hasattr(_current_classification, "is_informational"):
        try:
            # Fallback for V1 or incomplete objects
            is_info = False
            if hasattr(_current_classification, "request_type"):
                rtype = _current_classification.request_type
                # Handle both Enum and string types
                tname = rtype.name if hasattr(rtype, "name") else str(rtype)
                is_info = any(k in tname.upper() for k in ["QUESTION", "SUMMARY", "EXPLANATION"])
            setattr(_current_classification, "is_informational", is_info)
        except:
            pass

    # Reset evidence tracker for the new request
    _reset_evidence_tracker()

    # CRITICAL: Set session mode based on classification for cross-turn persistence
    cwd = _get_current_cwd()
    if cwd:
        if _current_classification.read_only:
            _set_session_mode(cwd, "analysis")
        else:
            # Implementation mode - also requires TDD
            _set_session_mode(cwd, "implementation")
            # If this is FIX_ALL or IMPLEMENTATION type, store the request as pending
            if _current_classification.request_type in (
                _RequestType.FIX_ALL,
                _RequestType.IMPLEMENTATION,
                _RequestType.MULTI_STEP,
            ):
                if getattr(_current_classification, "requires_tdd", False):
                    # Store the implementation request for TDD tracking
                    _add_session_pending_task(
                        cwd,
                        {
                            "request": user_input[:500],  # Truncate for storage
                            "type": _current_classification.request_type.name,
                            "requires_tdd": True,
                            "status": "pending",
                            "created_at": datetime.now().isoformat(timespec="seconds"),
                        },
                    )

    return _current_classification


def _get_current_classification() -> _ClassifiedRequest | None:
    """Get the current request classification for enforcement."""
    return _current_classification


def _clear_classification() -> None:
    """Clear the current classification after request is complete."""
    global _current_classification
    _current_classification = None


# ══════════════════════════════════════════════════════════════════════════════
# EVIDENCE TRACKING STATE - Tracks verified file reads and searches for grounding
# ══════════════════════════════════════════════════════════════════════════════

# Global evidence tracker instance - tracks file reads and searches per request
_evidence_tracker: _EvidenceTracker | None = None

# Global synthesis gate instance - blocks synthesis without sufficient evidence
_synthesis_gate = _SynthesisGate(require_any_evidence=True)


def _reset_evidence_tracker() -> _EvidenceTracker:
    """Reset and return a fresh evidence tracker for a new request."""
    global _evidence_tracker
    _evidence_tracker = _EvidenceTracker()
    return _evidence_tracker


def _get_evidence_tracker() -> _EvidenceTracker | None:
    """Get the current evidence tracker."""
    return _evidence_tracker


def _record_file_read(filepath: str, success: bool = True) -> None:
    """Record a file read attempt on the current evidence tracker."""
    if _evidence_tracker is not None:
        _evidence_tracker.record_file_read(filepath, success)


def _record_search(pattern: str, results: list[str]) -> None:
    """Record a search and its results on the current evidence tracker."""
    if _evidence_tracker is not None:
        _evidence_tracker.record_search(pattern, results)


def _check_synthesis_gate() -> tuple[bool, str]:
    """Check if synthesis should be allowed based on collected evidence."""
    if _evidence_tracker is None:
        return False, "No evidence tracker initialized"
    return _synthesis_gate.check(_evidence_tracker)


# ══════════════════════════════════════════════════════════════════════════════
# MULTI-AGENT SWARM - Orchestrator-Worker pattern with model routing
# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# THREAD SAFETY HELPERS
# ══════════════════════════════════════════════════════════════════════════════


def _is_main_thread() -> bool:
    """Check if the current thread is the main thread.

    Returns:
        True if running on the main thread, False otherwise
    """
    return threading.current_thread() == threading.main_thread()


@dataclass
class AutonomousCommandOptions:
    """Parsed options for autonomous runtime commands."""

    max_cycles: int | None = None
    use_intelligent: bool = False
    focus: str = ""
    max_workers: int = 3
    model: str | None = None
    keep_current_model: bool = False


@dataclass
class AutoOrgRoleSpec:
    """A dependency-aware autonomous role for /autoorg."""

    id: str
    name: str
    task_type: TaskType
    focus: str
    dependencies: list[str] = field(default_factory=list)


@dataclass
class AutoFleetSubtask:
    """A subtask for /autofleet parallel execution."""

    id: str
    name: str
    description: str
    task_type: TaskType
    dependencies: list[str] = field(default_factory=list)
    completed: bool = False
    result: str | None = None
    error: str | None = None


def _decompose_task_for_fleet(
    task: str,
    max_subtasks: int = 8,
) -> list[AutoFleetSubtask]:
    """Break down a single task into parallelizable subtasks for /autofleet.

    Args:
        task: The task description to decompose
        max_subtasks: Maximum number of subtasks to create

    Returns:
        List of AutoFleetSubtask objects representing the decomposed task
    """
    task_lower = task.lower()
    subtasks: list[AutoFleetSubtask] = []

    # Planning subtask is always first
    subtasks.append(
        AutoFleetSubtask(
            id="analyze",
            name="Analysis & Planning",
            description=f"Analyze requirements and create implementation plan for: {task}",
            task_type=TaskType.ARCHITECTURE,
            dependencies=[],
        )
    )

    # Detect task patterns to create appropriate subtasks
    has_implementation = any(
        kw in task_lower
        for kw in ["implement", "create", "build", "add", "develop", "write", "make"]
    )
    has_testing = any(kw in task_lower for kw in ["test", "testing", "tdd", "coverage"])
    has_docs = any(kw in task_lower for kw in ["document", "doc", "readme", "comment"])
    has_fix = any(kw in task_lower for kw in ["fix", "bug", "error", "issue", "debug"])
    has_refactor = any(kw in task_lower for kw in ["refactor", "improve", "optimize", "clean"])
    has_security = any(kw in task_lower for kw in ["security", "auth", "login", "encrypt"])
    has_api = any(kw in task_lower for kw in ["api", "endpoint", "route", "rest", "graphql"])
    has_ui = any(kw in task_lower for kw in ["ui", "frontend", "component", "page", "view"])
    has_data = any(kw in task_lower for kw in ["database", "data", "model", "schema", "migration"])

    # Add appropriate implementation subtasks
    if has_data:
        subtasks.append(
            AutoFleetSubtask(
                id="data",
                name="Data Layer Implementation",
                description=f"Implement data models, database schemas, and migrations for: {task}",
                task_type=TaskType.IMPLEMENTATION,
                dependencies=["analyze"],
            )
        )

    if has_api:
        subtasks.append(
            AutoFleetSubtask(
                id="api",
                name="API Implementation",
                description=f"Implement API endpoints and business logic for: {task}",
                task_type=TaskType.IMPLEMENTATION,
                dependencies=["analyze"] + (["data"] if has_data else []),
            )
        )

    if has_ui:
        subtasks.append(
            AutoFleetSubtask(
                id="ui",
                name="UI Implementation",
                description=f"Implement frontend components and UI for: {task}",
                task_type=TaskType.IMPLEMENTATION,
                dependencies=["analyze"] + (["api"] if has_api else []),
            )
        )

    if has_implementation and not (has_api or has_ui or has_data):
        subtasks.append(
            AutoFleetSubtask(
                id="core",
                name="Core Implementation",
                description=f"Implement core functionality for: {task}",
                task_type=TaskType.IMPLEMENTATION,
                dependencies=["analyze"],
            )
        )

    if has_fix:
        subtasks.append(
            AutoFleetSubtask(
                id="fix",
                name="Bug Fix",
                description=f"Identify and fix issues for: {task}",
                task_type=TaskType.IMPLEMENTATION,
                dependencies=["analyze"],
            )
        )

    if has_refactor:
        subtasks.append(
            AutoFleetSubtask(
                id="refactor",
                name="Code Refactoring",
                description=f"Refactor and optimize code for: {task}",
                task_type=TaskType.REVIEW,
                dependencies=["analyze"],
            )
        )

    if has_security:
        subtasks.append(
            AutoFleetSubtask(
                id="security",
                name="Security Implementation",
                description=f"Implement security measures for: {task}",
                task_type=TaskType.SECURITY,
                dependencies=["analyze"],
            )
        )

    # Always add testing and documentation if not too many subtasks
    impl_deps = [s.id for s in subtasks if s.task_type == TaskType.IMPLEMENTATION]
    if not impl_deps:
        impl_deps = ["analyze"]

    if has_testing or len(subtasks) < max_subtasks:
        subtasks.append(
            AutoFleetSubtask(
                id="testing",
                name="Testing & Validation",
                description=f"Write comprehensive tests for: {task}",
                task_type=TaskType.TESTING,
                dependencies=impl_deps,
            )
        )

    if has_docs or len(subtasks) < max_subtasks:
        subtasks.append(
            AutoFleetSubtask(
                id="docs",
                name="Documentation",
                description=f"Document the implementation for: {task}",
                task_type=TaskType.DOCUMENTATION,
                dependencies=impl_deps + (["testing"] if has_testing else []),
            )
        )

    # Handle edge case: max_subtasks=1 means only analyze
    if max_subtasks <= 1:
        return [subtasks[0]]

    # Limit middle subtasks (keep analyze and leave room for integrate)
    # We need at least 2 slots: analyze and integrate
    if len(subtasks) > max_subtasks - 1:
        # Keep analyze (first) and trim middle subtasks
        subtasks = [subtasks[0]] + subtasks[1 : max_subtasks - 1]

    # Integration subtask - always last
    all_prior = [s.id for s in subtasks]
    subtasks.append(
        AutoFleetSubtask(
            id="integrate",
            name="Integration & Verification",
            description=f"Integrate all components and verify everything works for: {task}",
            task_type=TaskType.REVIEW,
            dependencies=all_prior,
        )
    )

    return subtasks


@dataclass
class AutoOrgBusinessBrief:
    """Normalized business brief for /autoorg autonomous execution."""

    raw_message: str
    mission: str
    is_business_build: bool
    business_type: str
    service_domains: list[str] = field(default_factory=list)
    browser_workflows: list[str] = field(default_factory=list)
    sensitive_operations: list[str] = field(default_factory=list)
    success_tracks: list[str] = field(default_factory=list)
    capability_highlights: list[str] = field(default_factory=list)


def _autoorg_keyword_hits(
    text: str,
    keyword_map: dict[str, tuple[str, ...]],
) -> list[str]:
    """Return matching semantic labels for a block of text."""
    lowered = text.lower()
    hits: list[str] = []
    for label, keywords in keyword_map.items():
        if any(keyword in lowered for keyword in keywords):
            hits.append(label)
    return hits


def _select_relevant_autoorg_capabilities(
    mission: str,
    service_domains: list[str],
    browser_workflows: list[str],
    capability_catalog: list[dict[str, object]] | None = None,
    *,
    max_items: int = 6,
) -> list[str]:
    """Pick capability highlights relevant to the current business brief."""
    if not capability_catalog:
        return []

    domain_keywords: dict[str, tuple[str, ...]] = {
        "payments": ("payment", "billing", "invoice", "checkout", "subscription", "stripe"),
        "identity": ("auth", "identity", "login", "oauth", "token", "clerk", "auth0", "supabase"),
        "analytics": (
            "analytics",
            "tracking",
            "warehouse",
            "metric",
            "mixpanel",
            "amplitude",
            "ga4",
        ),
        "crm": ("crm", "sales", "lead", "hubspot", "salesforce", "pipeline", "outreach"),
        "scheduling": ("calendar", "schedule", "booking", "appointment", "meeting", "calendly"),
        "communications": ("email", "sms", "notification", "slack", "discord", "support", "chat"),
        "advertising": ("ads", "advertising", "campaign", "meta", "google", "tiktok", "linkedin"),
        "commerce": ("commerce", "store", "shop", "ecommerce", "catalog", "inventory"),
        "mobile_release": ("mobile", "ios", "android", "app store", "play store", "testflight"),
        "browser_ops": ("browser", "portal", "dashboard", "web", "playwright", "puppeteer", "form"),
        "developer_platforms": (
            "api",
            "sdk",
            "github",
            "vercel",
            "cloudflare",
            "aws",
            "gcp",
            "supabase",
            "firebase",
        ),
    }

    search_terms = set(
        re.findall(
            r"[a-z0-9_.:+-]{3,}",
            " ".join([mission, *service_domains, *browser_workflows]).lower(),
        )
    )
    for domain in service_domains:
        search_terms.update(domain_keywords.get(domain, ()))
    for workflow in browser_workflows:
        search_terms.update(re.findall(r"[a-z0-9_.:+-]{3,}", workflow.lower()))

    ranked: list[tuple[int, str]] = []
    for capability in capability_catalog:
        key = str(capability.get("key") or capability.get("capability_name") or "").strip()
        description = str(capability.get("description", "")).strip()
        tags = capability.get("tags", [])
        tag_text = " ".join(str(tag) for tag in tags) if isinstance(tags, list) else str(tags)
        haystack = f"{key} {description} {tag_text}".lower()
        score = sum(1 for term in search_terms if term in haystack)
        if key.startswith("claude.") and ".mcp." in key:
            score += 1
        if any(term in haystack for term in ("browser", "playwright", "puppeteer", "web")):
            score += 2
        if score > 0:
            ranked.append((score, f"{key}: {description or 'Imported capability'}"))

    ranked.sort(key=lambda item: (-item[0], item[1]))
    seen: set[str] = set()
    selected: list[str] = []
    for _, item in ranked:
        if item in seen:
            continue
        seen.add(item)
        selected.append(item)
        if len(selected) >= max_items:
            break

    if selected:
        return selected

    fallback = [
        f"{str(capability.get('key') or capability.get('capability_name') or '').strip()}: "
        f"{str(capability.get('description', '')).strip() or 'Imported capability'}"
        for capability in capability_catalog
        if ".mcp." in str(capability.get("key", "")).lower()
    ]
    return fallback[:max_items]


def _build_autoorg_business_brief(
    message: str,
    capability_catalog: list[dict[str, object]] | None = None,
) -> AutoOrgBusinessBrief:
    """Derive a richer business brief from the initial /autoorg message."""
    normalized = (
        message.strip()
        or "Create, launch, and grow this business responsibly with minimal user interruption."
    )
    lowered = normalized.lower()

    business_type_map: dict[str, tuple[str, ...]] = {
        "saas": ("saas", "software", "platform", "app", "api", "developer tool"),
        "agency": ("agency", "consulting", "consultancy", "service business", "freelance"),
        "commerce": ("store", "shop", "ecommerce", "marketplace", "catalog"),
        "media": ("newsletter", "content", "media", "community", "creator"),
        "mobile": ("ios", "android", "mobile app", "app store", "play store"),
    }
    service_domain_map: dict[str, tuple[str, ...]] = {
        "payments": (
            "payment",
            "billing",
            "invoice",
            "subscription",
            "checkout",
            "pricing",
            "revenue",
            "stripe",
        ),
        "identity": (
            "auth",
            "identity",
            "login",
            "signin",
            "sign up",
            "signup",
            "oauth",
            "account",
            "sso",
        ),
        "analytics": ("analytics", "tracking", "metrics", "dashboard", "telemetry", "warehouse"),
        "crm": (
            "sales",
            "crm",
            "leads",
            "pipeline",
            "prospect",
            "outreach",
            "customer acquisition",
        ),
        "scheduling": (
            "appointment",
            "appointments",
            "calendar",
            "booking",
            "meeting",
            "schedule",
            "scheduler",
        ),
        "communications": ("email", "sms", "support", "chat", "slack", "discord", "notification"),
        "advertising": (
            "ads",
            "advertising",
            "campaign",
            "brand",
            "audience",
            "growth",
            "acquisition",
        ),
        "commerce": ("commerce", "store", "shop", "catalog", "inventory", "fulfillment"),
        "mobile_release": (
            "ios",
            "android",
            "mobile app",
            "app store",
            "play store",
            "testflight",
            "submission",
        ),
        "browser_ops": (
            "browser",
            "dashboard",
            "portal",
            "form",
            "submit",
            "application",
            "listing",
            "web",
        ),
        "developer_platforms": (
            "api",
            "sdk",
            "github",
            "vercel",
            "cloudflare",
            "aws",
            "gcp",
            "firebase",
            "supabase",
        ),
    }
    browser_workflow_map: dict[str, tuple[str, ...]] = {
        "service signups and account setup": (
            "sign up",
            "signup",
            "create account",
            "onboard",
            "register",
        ),
        "authenticated dashboard setup": ("login", "sign in", "dashboard", "portal", "admin"),
        "API key retrieval and integration setup": (
            "api key",
            "token",
            "credential",
            "secret",
            "oauth",
        ),
        "mobile app submission workflows": (
            "mobile app",
            "app store",
            "play store",
            "submit mobile",
            "testflight",
            "submission",
        ),
        "form fills and partner applications": (
            "form",
            "application",
            "listing",
            "directory",
            "submit",
        ),
    }
    sensitive_map: dict[str, tuple[str, ...]] = {
        "credentials": ("password", "credential", "login", "account"),
        "api keys": ("api key", "token", "secret", "oauth"),
        "payment approvals": ("payment method", "card", "billing", "invoice", "purchase"),
        "identity verification": ("mfa", "2fa", "otp", "captcha", "verification", "attestation"),
        "store submissions": ("app store", "play store", "developer account", "review submission"),
    }
    success_track_map: dict[str, tuple[str, ...]] = {
        "build a real product": ("build", "product", "app", "platform", "tool"),
        "launch successfully": ("launch", "ship", "go live", "release", "publish"),
        "acquire customers": ("customers", "growth", "marketing", "audience", "adoption"),
        "create revenue": ("sales", "pricing", "revenue", "billing", "monetize"),
        "operate reliably": ("ops", "automation", "support", "reliability", "scale", "thrive"),
    }

    business_type = next(
        (
            label
            for label, keywords in business_type_map.items()
            if any(keyword in lowered for keyword in keywords)
        ),
        "business",
    )
    service_domains = _autoorg_keyword_hits(lowered, service_domain_map)
    browser_workflows = _autoorg_keyword_hits(lowered, browser_workflow_map)
    sensitive_operations = _autoorg_keyword_hits(lowered, sensitive_map)
    success_tracks = _autoorg_keyword_hits(lowered, success_track_map)

    is_business_build = any(
        keyword in lowered
        for keyword in (
            "business",
            "startup",
            "company",
            "launch",
            "grow",
            "thrive",
            "customers",
            "revenue",
            "marketing",
            "sales",
            "brand",
            "agency",
            "store",
            "product",
        )
    )

    if not success_tracks and is_business_build:
        success_tracks = [
            "build a real product",
            "launch successfully",
            "acquire customers",
            "create revenue",
            "operate reliably",
        ]

    capability_highlights = _select_relevant_autoorg_capabilities(
        normalized,
        service_domains,
        browser_workflows,
        capability_catalog,
    )

    return AutoOrgBusinessBrief(
        raw_message=normalized,
        mission=normalized,
        is_business_build=is_business_build,
        business_type=business_type,
        service_domains=service_domains,
        browser_workflows=browser_workflows,
        sensitive_operations=sensitive_operations,
        success_tracks=success_tracks,
        capability_highlights=capability_highlights,
    )


def _format_autoorg_business_brief(brief: AutoOrgBusinessBrief) -> str:
    """Create a compact operator-readable summary of the business brief."""
    sections = [
        f"Mission: {brief.mission}",
        f"Business type: {brief.business_type}",
    ]
    if brief.service_domains:
        sections.append(f"Service domains: {', '.join(brief.service_domains)}")
    if brief.browser_workflows:
        sections.append(f"Browser/operator workflows: {', '.join(brief.browser_workflows)}")
    if brief.success_tracks:
        sections.append(f"Success tracks: {', '.join(brief.success_tracks)}")
    if brief.sensitive_operations:
        sections.append(f"Sensitive operations: {', '.join(brief.sensitive_operations)}")
    if brief.capability_highlights:
        sections.append(
            "Relevant integrations:\n"
            + "\n".join(f"- {item}" for item in brief.capability_highlights)
        )
    return "\n".join(sections)


def _autoorg_worker_operating_policy() -> str:
    """Shared operating policy for AutoOrg workers."""
    return (
        "## AUTOORG AUTONOMY POLICY\n"
        "- Operate without asking the user for more input unless you hit a real blocker.\n"
        "- Real blockers are limited to: missing credentials/API keys, MFA/CAPTCHA, payment approvals, "
        "legal attestation/identity verification, destructive irreversible actions, or missing third-party access.\n"
        "- If blocked, ask only the minimum specific question needed and keep moving on other parallelizable work.\n"
        "- Never hardcode, print, or commit secrets. Prefer env vars, .env.example updates, secure config plumbing, and operator notes.\n"
        "- For browser or third-party tasks, use available integrations/capabilities when possible. If direct execution is unavailable, "
        "prepare the code, config, runbook, checklist, and exact human handoff rather than pretending the action is complete.\n"
        "- Handle sensitive information carefully and minimize exposure in logs, code, and prompts.\n"
    )


def _autoorg_response_requests_user_input(response: str) -> bool:
    """Detect premature user questions from autonomous workers."""
    lowered = response.lower()
    request_phrases = (
        "please provide",
        "can you provide",
        "could you provide",
        "please confirm",
        "do you want me to",
        "what would you like",
        "i need you to",
        "i need the user to",
        "please share",
    )
    blocker_terms = (
        "credential",
        "password",
        "api key",
        "token",
        "secret",
        "mfa",
        "2fa",
        "captcha",
        "verification code",
        "one-time code",
        "payment approval",
        "billing approval",
        "legal name",
        "tax id",
        "attestation",
        "developer account",
        "app store",
        "play store",
    )
    has_real_tool_output = bool(re.search(r"(?m)^(READ|SEARCH|RUN|FILE):\s*\S", response))
    if has_real_tool_output:
        return False
    if not any(phrase in lowered for phrase in request_phrases):
        return False
    return not any(term in lowered for term in blocker_terms)


def _parse_autonomous_command_args(
    arg: str,
    *,
    default_use_intelligent: bool = False,
    default_workers: int = 3,
) -> AutonomousCommandOptions:
    """Parse shared command-line options for /autopolit and /autoorg.

    Supported patterns:
    - /autopolit 5 --smart fix auth flow
    - /autopolit --model llama_cpp:qwen2.5-coder-3b improve tests
    - /autoorg --workers 4 launch this project
    """
    options = AutonomousCommandOptions(
        use_intelligent=default_use_intelligent,
        max_workers=default_workers,
    )
    if not arg.strip():
        return options

    tokens = shlex.split(arg)
    focus_parts: list[str] = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        if token == "--classic":
            options.use_intelligent = False
        elif token in {"--smart", "--v2"}:
            options.use_intelligent = True
        elif token in {"--workers", "-w"}:
            i += 1
            if i >= len(tokens):
                raise ValueError("Missing value for --workers")
            try:
                options.max_workers = int(tokens[i])
            except ValueError as exc:
                raise ValueError("--workers must be a positive integer") from exc
            if options.max_workers <= 0:
                raise ValueError("--workers must be a positive integer")
        elif token == "--model":
            i += 1
            if i >= len(tokens):
                raise ValueError("Missing value for --model")
            options.model = tokens[i]
        elif token == "--keep-model":
            options.keep_current_model = True
        else:
            if options.max_cycles is None:
                try:
                    maybe_cycles = int(token)
                except ValueError:
                    maybe_cycles = None
                if maybe_cycles is not None:
                    if maybe_cycles <= 0:
                        raise ValueError("max-cycles must be a positive integer")
                    options.max_cycles = maybe_cycles
                    i += 1
                    continue
            focus_parts.append(token)
        i += 1

    options.focus = " ".join(focus_parts).strip()
    return options


def _plan_autoorg_roles(
    goal: str,
    capability_catalog: list[dict[str, object]] | None = None,
) -> list[AutoOrgRoleSpec]:
    """Plan dependency-aware autonomous roles for /autoorg."""
    brief = _build_autoorg_business_brief(goal, capability_catalog)
    normalized_goal = brief.mission
    goal_lower = normalized_goal.lower()

    roles: list[AutoOrgRoleSpec] = [
        AutoOrgRoleSpec(
            id="plan",
            name="Strategy Lead",
            task_type=TaskType.ARCHITECTURE,
            focus=(
                f"Clarify the mission, identify the highest-leverage milestones, and break "
                f"'{normalized_goal}' into execution-ready work for the rest of the organization."
            ),
        ),
        AutoOrgRoleSpec(
            id="engineering",
            name="Engineering",
            task_type=TaskType.IMPLEMENTATION,
            focus=(
                f"Own the technical delivery for '{normalized_goal}'. Build or improve the code, "
                "tests, tooling, and product behavior needed to move the mission forward."
            ),
            dependencies=["plan"],
        ),
        AutoOrgRoleSpec(
            id="integrations",
            name="Integrations & Platform Ops",
            task_type=TaskType.IMPLEMENTATION,
            focus=(
                f"Own third-party service integration architecture for '{normalized_goal}'. "
                "Connect the product to the right external platforms, secrets plumbing, "
                "deployment services, operational workflows, and API/provider adapters. "
                "Prefer env-first configuration, secure secret handling, and resilient integration setup."
            ),
            dependencies=["plan"],
        ),
        AutoOrgRoleSpec(
            id="quality",
            name="Quality & QA",
            task_type=TaskType.TESTING,
            focus=(
                f"Create or improve tests, validation, verification, and release confidence for "
                f"'{normalized_goal}'."
            ),
            dependencies=["engineering", "integrations"],
        ),
        AutoOrgRoleSpec(
            id="security",
            name="Security & Reliability",
            task_type=TaskType.SECURITY,
            focus=(
                f"Audit the work for '{normalized_goal}' for security, reliability, CI, and "
                "production-readiness risks."
            ),
            dependencies=["engineering", "integrations"],
        ),
        AutoOrgRoleSpec(
            id="docs",
            name="Documentation",
            task_type=TaskType.DOCUMENTATION,
            focus=(
                f"Update the documentation, onboarding notes, launch notes, and operator guidance "
                f"needed for '{normalized_goal}'."
            ),
            dependencies=["engineering", "integrations"],
        ),
    ]

    needs_business_roles = brief.is_business_build

    if brief.is_business_build:
        roles.insert(
            1,
            AutoOrgRoleSpec(
                id="product",
                name="Product & Offer Design",
                task_type=TaskType.ARCHITECTURE,
                focus=(
                    f"Turn '{normalized_goal}' into a compelling, execution-ready offer. "
                    "Define product scope, user journey, differentiation, roadmap, and the minimum lovable experience."
                ),
                dependencies=["plan"],
            ),
        )

    if needs_business_roles:
        roles.extend(
            [
                AutoOrgRoleSpec(
                    id="marketing",
                    name="Marketing",
                    task_type=TaskType.DOCUMENTATION,
                    focus=(
                        f"Create or improve positioning, messaging, launch assets, campaigns, "
                        f"and audience-facing copy for '{normalized_goal}'."
                    ),
                    dependencies=["plan"],
                ),
                AutoOrgRoleSpec(
                    id="sales",
                    name="Sales",
                    task_type=TaskType.REVIEW,
                    focus=(
                        f"Create sales collateral, pricing narratives, outreach sequences, and "
                        f"follow-up motions that help turn '{normalized_goal}' into revenue."
                    ),
                    dependencies=["marketing"],
                ),
                AutoOrgRoleSpec(
                    id="ops",
                    name="Operations",
                    task_type=TaskType.ARCHITECTURE,
                    focus=(
                        f"Own the operating cadence for '{normalized_goal}': planning, execution "
                        "checklists, appointments, handoffs, scheduling, and business process support."
                    ),
                    dependencies=["plan", "integrations"],
                ),
                AutoOrgRoleSpec(
                    id="customer",
                    name="Customer Success",
                    task_type=TaskType.REVIEW,
                    focus=(
                        f"Design onboarding, support, feedback, retention, and account management "
                        f"motions that help '{normalized_goal}' keep customers successful."
                    ),
                    dependencies=["marketing", "ops"],
                ),
            ]
        )

    if brief.browser_workflows:
        operator_dependencies = ["integrations"]
        if brief.is_business_build:
            operator_dependencies.append("ops")
        roles.append(
            AutoOrgRoleSpec(
                id="operator",
                name="Browser & Service Operator",
                task_type=TaskType.REVIEW,
                focus=(
                    f"Own browser-mediated workflows for '{normalized_goal}', including service signups, "
                    "dashboard setup, API key retrieval, portal configuration, listings, submissions, "
                    "and exact handoffs for human-only checkpoints. Work autonomously until blocked by "
                    "credentials, MFA/CAPTCHA, approvals, or legally human-only attestations."
                ),
                dependencies=operator_dependencies,
            )
        )

    if "mobile_release" in brief.service_domains or any(
        keyword in goal_lower for keyword in ("app store", "play store", "testflight", "mobile app")
    ):
        launch_dependencies = ["engineering", "quality", "ops"]
        if any(role.id == "operator" for role in roles):
            launch_dependencies.append("operator")
        roles.append(
            AutoOrgRoleSpec(
                id="launch",
                name="Launch & Submission",
                task_type=TaskType.REVIEW,
                focus=(
                    f"Prepare '{normalized_goal}' for launch across release channels, submissions, "
                    "store metadata, operational checklists, and final go-live coordination."
                ),
                dependencies=launch_dependencies,
            )
        )

    if brief.sensitive_operations or any(
        domain in brief.service_domains for domain in ("payments", "identity", "mobile_release")
    ):
        compliance_deps = ["plan", "integrations"]
        roles.append(
            AutoOrgRoleSpec(
                id="compliance",
                name="Compliance & Trust",
                task_type=TaskType.SECURITY,
                focus=(
                    f"Handle the trust, privacy, approvals, credential-flow, and compliance posture "
                    f"needed for '{normalized_goal}', including safe handling of sensitive operations."
                ),
                dependencies=compliance_deps,
            )
        )

    integration_dependencies = [role.id for role in roles if role.id != "plan"]
    roles.append(
        AutoOrgRoleSpec(
            id="integrate",
            name="Integration Lead",
            task_type=TaskType.REVIEW,
            focus=(
                f"Integrate the outputs for '{normalized_goal}', resolve cross-role conflicts, "
                "and produce the next cohesive step for the whole project."
            ),
            dependencies=integration_dependencies,
        )
    )

    return roles


def _parse_autoorg_repl_args(arg: str) -> tuple[str, bool, bool, bool]:
    """Parse `/autoorg ...` REPL arguments into task text and flags."""
    if not arg.strip():
        return "", False, False, True
    try:
        tokens = shlex.split(arg)
    except ValueError as exc:
        raise ValueError(f"Invalid quoting: {exc}") from exc
    plan_only = False
    dry_run = False
    parallel = True
    focus_parts: list[str] = []
    for token in tokens:
        if token in ("--plan", "-p"):
            plan_only = True
        elif token in ("--dry-run", "-n"):
            dry_run = True
        elif token == "--parallel":
            parallel = True
        elif token == "--no-parallel":
            parallel = False
        else:
            focus_parts.append(token)
    return (" ".join(focus_parts).strip(), plan_only, dry_run, parallel)


def _run_repl_autoorg_flow(
    *,
    task: str,
    plan_only: bool,
    dry_run: bool,
    parallel: bool,
    cfg: SageConfig,
    router: ProviderRouter,
    ai_orchestrator: AIOrchestrator,
) -> None:
    """Run multi-step AI orchestration from the agent REPL (replaces removed `sage autoorg`)."""
    from sage.core.model_selector import ModelSelector

    renderer.header("Auto-Orchestration")
    renderer.info(f"Task: {task}")
    renderer.console.print()

    decomposer = ai_orchestrator.decomposition_engine

    renderer.info("Analyzing task...")
    try:
        decomposition = decomposer.decompose(task)
    except Exception as e:
        renderer.error(f"Failed to analyze task: {e}")
        return

    renderer.header("Execution Plan")
    steps = decomposition.subtasks
    if not steps:
        renderer.warning("No steps identified for this task")
        return

    all_models: list = []
    for provider in router._providers.values():
        if provider.is_available():
            all_models.extend(provider.list_models())

    model_selector = ModelSelector(all_models)

    for i, step in enumerate(steps, start=1):
        step_desc = str(step)

        best_model, task_analysis = model_selector.select(step_desc)
        model_name = best_model.id if best_model else cfg.default_model

        renderer.info(f"  {i}. [action] {step_desc}")
        renderer.info(f"     Model: {model_name} ({task_analysis.task_type.name.lower()})")

    renderer.console.print()

    if plan_only:
        renderer.success("Plan complete (--plan mode, not executing)")
        return

    if dry_run:
        renderer.success("Dry run complete (no changes made)")
        return

    if not parallel:
        renderer.info("(Sequential execution — parallel orchestration not yet implemented)")

    renderer.header("Executing Plan")

    success_count = 0
    fail_count = 0

    # Build the multi-model orchestrator so each step actually USES its
    # picked model (the ModelSelector above was previously cosmetic).
    from sage.core.multi_model_orchestration import MultiModelOrchestrator
    mmo = MultiModelOrchestrator(router=router)

    for i, step in enumerate(steps, start=1):
        step_desc = str(step)

        # Pick the right model for this specific subtask
        best_model, _task_analysis = model_selector.select(step_desc)
        step_model_id = best_model.id if best_model else None

        renderer.info(f"Step {i}/{len(steps)}: {step_desc}")
        if step_model_id:
            renderer.info(f"  → using {step_model_id}")

        try:
            # Multi-model path: run through the picked model directly.
            # Falls back to the orchestrator's default if no model picked.
            if step_model_id:
                sub_result = mmo.run_subtask(desc=step_desc)
                ok = sub_result.ok
                if ok:
                    renderer.success(f"  ✓ Completed ({sub_result.model_used})")
                    success_count += 1
                else:
                    renderer.error(f"  ✗ Failed: {sub_result.error}")
                    fail_count += 1
            else:
                result = ai_orchestrator.execute_step(step_desc)
                ok = True
                if isinstance(result, dict):
                    ok = bool(result.get("success", True))
                if ok:
                    renderer.success("  ✓ Completed")
                    success_count += 1
                else:
                    err = (
                        result.get("error", "Unknown error") if isinstance(result, dict) else "Unknown error"
                    )
                    renderer.error(f"  ✗ Failed: {err}")
                    fail_count += 1

        except KeyboardInterrupt:
            renderer.warning("\nInterrupted — stopping auto-orchestration.")
            return
        except Exception as e:
            renderer.error(f"  ✗ Error: {e}")
            fail_count += 1

    renderer.console.print()
    renderer.header("Summary")
    renderer.info(f"  Completed: {success_count}/{len(steps)}")
    if fail_count > 0:
        renderer.warning(f"  Failed: {fail_count}")
    else:
        renderer.success("All steps completed successfully!")


# ══════════════════════════════════════════════════════════════════════════════
# DOCKER SANDBOX - Isolated execution environment for verified TDD
# ══════════════════════════════════════════════════════════════════════════════


# ══════════════════════════════════════════════════════════════════════════════
# DOCKER SANDBOX - Isolated execution environment for verified TDD
# ══════════════════════════════════════════════════════════════════════════════

import atexit
import uuid


@dataclass
class SandboxResult:
    """Result from sandbox execution."""

    exit_code: int
    stdout: str
    stderr: str
    duration: float
    command: str
    timed_out: bool = False

    # DockerSandbox, TDDGate, and TaskExecutionManager have been migrated to sage.core
    # ControllerModel and ProjectMemory have been migrated to sage.core
    # Classes are now imported from sage.core.controller and sage.core.memory


# ══════════════════════════════════════════════════════════════════════════════
# CONTEXT COMPACTION - Automatic summarization at 90% capacity
# ══════════════════════════════════════════════════════════════════════════════


def _get_msg_content(msg) -> str:
    """Get content from a message, whether it's a dict or Message dataclass."""
    if hasattr(msg, "content"):
        return msg.content
    elif isinstance(msg, dict):
        return msg.get("content", "")
    return ""


def _get_msg_role(msg) -> str:
    """Get role from a message, whether it's a dict or Message dataclass."""
    if hasattr(msg, "role"):
        return msg.role
    elif isinstance(msg, dict):
        return msg.get("role", "")
    return ""


def _msg_to_dict(msg) -> dict:
    """Convert a Message dataclass or dict to a dict."""
    if hasattr(msg, "role") and hasattr(msg, "content"):
        return {"role": msg.role, "content": msg.content}
    elif isinstance(msg, dict):
        return msg
    return {"role": "", "content": ""}


# ══════════════════════════════════════════════════════════════════════════════
# LSP INTEGRATION - Language Server Protocol for real-time diagnostics
# ══════════════════════════════════════════════════════════════════════════════


@dataclass
class LSPDiagnostic:
    """A diagnostic from the language server."""

    file: str
    line: int
    column: int
    severity: str  # error, warning, info, hint
    message: str
    source: str  # pyright, typescript, rust-analyzer, etc.


class LSPClient:
    """Language Server Protocol client for real-time error detection.

    Detects "red squiggles" before running tests:
    - Type errors
    - Syntax errors
    - Import errors
    - Unused variables
    """

    # Language server commands for different languages
    LSP_SERVERS = {
        ".py": {
            "cmd": ["pyright", "--outputjson"],
            "name": "pyright",
        },
        ".ts": {
            "cmd": ["npx", "typescript", "--noEmit"],
            "name": "typescript",
        },
        ".tsx": {
            "cmd": ["npx", "typescript", "--noEmit"],
            "name": "typescript",
        },
        ".rs": {
            "cmd": ["cargo", "check", "--message-format=json"],
            "name": "rust-analyzer",
        },
        ".go": {
            "cmd": ["go", "vet", "./..."],
            "name": "go-vet",
        },
    }

    def __init__(self, cwd: Path):
        self.cwd = cwd
        self._available_servers: dict[str, bool] = {}
        self._check_servers()

    def _check_servers(self) -> None:
        """Check which language servers are available."""
        for ext, config in self.LSP_SERVERS.items():
            cmd = config["cmd"][0]
            try:
                result = subprocess.run(
                    ["which", cmd] if cmd != "npx" else ["which", "npx"],
                    capture_output=True,
                    timeout=5,
                )
                self._available_servers[ext] = result.returncode == 0
            except Exception:
                self._available_servers[ext] = False

    def check_file(self, filepath: str) -> list[LSPDiagnostic]:
        """Check a file for diagnostics."""
        full_path = self.cwd / filepath
        if not full_path.exists():
            return []

        ext = full_path.suffix.lower()
        if ext not in self.LSP_SERVERS or not self._available_servers.get(ext, False):
            return []

        config = self.LSP_SERVERS[ext]

        if ext == ".py":
            return self._check_python(filepath)
        elif ext in {".ts", ".tsx"}:
            return self._check_typescript(filepath)
        elif ext == ".rs":
            return self._check_rust(filepath)
        elif ext == ".go":
            return self._check_go(filepath)

        return []

    def _check_python(self, filepath: str) -> list[LSPDiagnostic]:
        """Check Python file with pyright."""
        diagnostics = []
        try:
            result = subprocess.run(
                ["pyright", "--outputjson", filepath],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.cwd,
            )
            if result.stdout:
                data = _json.loads(result.stdout)
                for diag in data.get("generalDiagnostics", []):
                    severity = diag.get("severity", "error")
                    if severity == 1:
                        severity = "error"
                    elif severity == 2:
                        severity = "warning"
                    else:
                        severity = "info"

                    diagnostics.append(
                        LSPDiagnostic(
                            file=filepath,
                            line=diag.get("range", {}).get("start", {}).get("line", 0) + 1,
                            column=diag.get("range", {}).get("start", {}).get("character", 0),
                            severity=severity,
                            message=diag.get("message", ""),
                            source="pyright",
                        )
                    )
        except Exception as e:
            logger.debug(f"Pyright check failed: {e}")
            pass
        return diagnostics

    def _check_typescript(self, filepath: str) -> list[LSPDiagnostic]:
        """Check TypeScript file."""
        diagnostics = []
        try:
            result = subprocess.run(
                ["npx", "tsc", "--noEmit", filepath],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.cwd,
            )
            # Parse tsc output
            for line in result.stdout.split("\n"):
                match = re.match(r"(.+)\((\d+),(\d+)\): (error|warning) TS\d+: (.+)", line)
                if match:
                    diagnostics.append(
                        LSPDiagnostic(
                            file=match.group(1),
                            line=int(match.group(2)),
                            column=int(match.group(3)),
                            severity=match.group(4),
                            message=match.group(5),
                            source="typescript",
                        )
                    )
        except Exception as e:
            logger.debug(f"TypeScript check failed: {e}")
            pass
        return diagnostics

    def _check_rust(self, filepath: str) -> list[LSPDiagnostic]:
        """Check Rust file with cargo check."""
        diagnostics = []
        try:
            result = subprocess.run(
                ["cargo", "check", "--message-format=json"],
                capture_output=True,
                text=True,
                timeout=60,
                cwd=self.cwd,
            )
            for line in result.stdout.split("\n"):
                if not line.strip():
                    continue
                try:
                    msg = _json.loads(line)
                    if msg.get("reason") == "compiler-message":
                        diag = msg.get("message", {})
                        spans = diag.get("spans", [])
                        if spans:
                            span = spans[0]
                            diagnostics.append(
                                LSPDiagnostic(
                                    file=span.get("file_name", filepath),
                                    line=span.get("line_start", 0),
                                    column=span.get("column_start", 0),
                                    severity=diag.get("level", "error"),
                                    message=diag.get("message", ""),
                                    source="rust-analyzer",
                                )
                            )
                except Exception as e:
                    logger.debug(f"Rust diagnostic parse failed: {e}")
                    pass
        except Exception as e:
            logger.debug(f"Rust check failed: {e}")
            pass
        return diagnostics

    def _check_go(self, filepath: str) -> list[LSPDiagnostic]:
        """Check Go file with go vet."""
        diagnostics = []
        try:
            result = subprocess.run(
                ["go", "vet", filepath],
                capture_output=True,
                text=True,
                timeout=30,
                cwd=self.cwd,
            )
            for line in result.stderr.split("\n"):
                match = re.match(r"(.+):(\d+):(\d+): (.+)", line)
                if match:
                    diagnostics.append(
                        LSPDiagnostic(
                            file=match.group(1),
                            line=int(match.group(2)),
                            column=int(match.group(3)),
                            severity="error",
                            message=match.group(4),
                            source="go-vet",
                        )
                    )
        except Exception as e:
            logger.debug(f"Go check failed: {e}")
            pass
        return diagnostics

    def check_files(self, filepaths: list[str]) -> list[LSPDiagnostic]:
        """Check multiple files."""
        all_diags = []
        for fp in filepaths:
            all_diags.extend(self.check_file(fp))
        return all_diags

    def format_diagnostics(self, diagnostics: list[LSPDiagnostic]) -> str:
        """Format diagnostics for display."""
        if not diagnostics:
            return "✅ No LSP diagnostics"

        icons = {
            "error": "🔴",
            "warning": "🟡",
            "info": "🔵",
            "hint": "⚪",
        }

        lines = ["🔍 LSP Diagnostics:"]
        for d in diagnostics[:20]:
            icon = icons.get(d.severity, "⚪")
            lines.append(f"  {icon} {d.file}:{d.line}:{d.column} — {d.message}")

        return "\n".join(lines)

    def has_errors(self, diagnostics: list[LSPDiagnostic]) -> bool:
        """Check if there are any errors."""
        return any(d.severity == "error" for d in diagnostics)


# ── Typer App Setup ──────────────────────────────────────────

app = typer.Typer(
    name="sage",
    help="Sage AI coding assistant",
    no_args_is_help=False,
    add_completion=False,
)

config_app = typer.Typer(help="Manage configuration")
# New user-facing commands (search/image/schedule/integrate/daemon) live
# in sage/cli/new_commands.py to keep main.py manageable. The sub-typer's
# top-level commands (search, image) and subcommand groups (schedule,
# integrate, daemon) get merged into the root app namespace.
try:
    from sage.cli.new_commands import app as _new_commands_app
    # Merge top-level commands by registering each individually so they
    # appear as `sage search` / `sage image`, not `sage <sub>` namespace.
    for _cmd_info in _new_commands_app.registered_commands:
        app.registered_commands.append(_cmd_info)
    # Subcommand groups (schedule, integrate, daemon) come through as
    # registered_groups — keep them grouped.
    for _grp in _new_commands_app.registered_groups:
        app.registered_groups.append(_grp)
except Exception:
    # If anything in the new commands module fails to import (missing
    # optional dep, etc.), don't kill the whole CLI — the existing
    # commands keep working.
    pass

app.add_typer(config_app, name="config")

secrets_app = typer.Typer(help="Secrets and .env file hygiene")
app.add_typer(secrets_app, name="secrets")

sms_app = typer.Typer(help="Message bridge — control any SAGE computer from iMessage or Google Messages")
app.add_typer(sms_app, name="sms")

# Wave 1-4 extensions: RAG, web search, project detect, auto-pick model, finetune, corpus
try:
    from sage.cli_extensions import register as _register_extensions
    _register_extensions(app)
except Exception:  # pragma: no cover - extensions are optional
    pass


