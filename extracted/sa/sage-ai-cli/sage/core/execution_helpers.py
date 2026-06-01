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


class _RequestExecutionContext:
    """Tracks execution context for a request to enable validation."""

    def __init__(self, task_prompt: str | None = None, cloud_provider: str = ""):
        self.task_prompt = task_prompt or ""
        self.cloud_provider = cloud_provider
        self.files_read: list[str] = []
        self.files_written: list[str] = []
        self.commands_executed: list[tuple[str, str, int]] = []  # (command, output, exit_code)
        self.search_executed: bool = False
        self.analysis_failed_closed: bool = False
        self.analysis_failure_message: str = ""

    def record_file_read(self, file_path: str):
        """Record that a file was read."""
        if file_path not in self.files_read:
            self.files_read.append(file_path)

    def record_file_written(self, file_path: str):
        """Record that a file was written."""
        if file_path not in self.files_written:
            self.files_written.append(file_path)

    def record_command(self, command: str, output: str, exit_code: int):
        """Record that a command was executed."""
        self.commands_executed.append((command, output, exit_code))

    def record_search(self):
        """Record that a search was executed."""
        self.search_executed = True


# Global context for tracking current request execution
_current_execution_context: _RequestExecutionContext | None = None


def _get_execution_context() -> _RequestExecutionContext | None:
    """Get the current execution context if one is active."""
    return _current_execution_context


def _track_files_read() -> list[str]:
    """Get list of files read in current execution context."""
    ctx = _get_execution_context()
    return ctx.files_read if ctx else []


def _track_files_written() -> list[str]:
    """Get list of files written in current execution context."""
    ctx = _get_execution_context()
    return ctx.files_written if ctx else []


def _get_current_task_prompt() -> str:
    """Get the active task prompt for the current execution context."""
    ctx = _get_execution_context()
    return ctx.task_prompt if ctx else ""


def _did_analysis_fail_closed() -> bool:
    """Return True when the current read-only analysis already failed closed."""
    ctx = _get_execution_context()
    return bool(ctx and ctx.analysis_failed_closed)


def _emit_grounded_analysis_failure(cwd: Path, detail: str) -> str:
    """Print/store a fail-closed analysis message once per request."""
    from sage.main import _add_to_conversation_memory, _add_to_output_history, _build_grounded_analysis_failure_message
    fail_closed_message = _build_grounded_analysis_failure_message(detail)
    ctx = _get_execution_context()
    already_emitted = bool(
        ctx and ctx.analysis_failed_closed and ctx.analysis_failure_message == fail_closed_message
    )
    if ctx:
        ctx.analysis_failed_closed = True
        ctx.analysis_failure_message = fail_closed_message

    if not already_emitted:
        renderer.print_assistant_response(fail_closed_message, markup=False)
        current_task_prompt = _get_current_task_prompt()
        if current_task_prompt:
            _add_to_output_history(cwd, fail_closed_message, current_task_prompt)
        _add_to_conversation_memory(cwd, "assistant", fail_closed_message)

    return fail_closed_message


def _execute_read_command(file_path: str) -> str | None:
    """Execute a READ command and return content or None if failed."""
    from sage.main import _add_session_file_read, _get_current_cwd
    try:
        path = Path(file_path)
        if not path.exists():
            return None
        content = path.read_text("utf-8", errors="replace")

        # Track that this file was read (in-memory context)
        ctx = _get_execution_context()
        if ctx:
            ctx.record_file_read(file_path)

        # CRITICAL: Also persist to session state for cross-turn memory
        cwd = _get_current_cwd()
        if cwd:
            _add_session_file_read(cwd, file_path)

        return content
    except Exception:
        return None


def _execute_file_write_and_verify(
    file_path: str, content: str, verify_content: bool = False
) -> None:
    """Write a file and verify it was actually written.

    Args:
        file_path: Path to write to
        content: Content to write
        verify_content: If True, verify content matches what was written

    Raises:
        Exception: If verification fails
    """
    from pathlib import Path

    # Write the file
    path = Path(file_path)
    if path.name == "__init__.py":
        content = ""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

    # Track the write
    ctx = _get_execution_context()
    if ctx:
        ctx.record_file_written(file_path)

    # Verify file exists
    if not path.exists():
        raise Exception(f"File write verification failed: {file_path} does not exist after write")

    # Optionally verify content
    if verify_content:
        actual_content = path.read_text("utf-8", errors="replace")
        if actual_content != content:
            raise Exception(f"File content mismatch: {file_path} content does not match expected")


def _execute_command_and_verify(command: str) -> tuple[str, int]:
    """Execute a command and verify the output makes sense.

    Args:
        command: Command to execute

    Returns:
        Tuple of (output, exit_code)

    Raises:
        Exception: If verification fails (e.g., pytest output for non-existent files)
    """
    import subprocess

    from sage.core.commands import run_shell

    # Execute the command — run_shell prefers Git Bash / WSL on Windows so
    # POSIX idioms work the same as on Linux/macOS.
    try:
        result = run_shell(command, timeout=300)
        output = result.stdout + result.stderr
        exit_code = result.returncode
    except subprocess.TimeoutExpired:
        output = "Command timed out"
        exit_code = 124
    except Exception as e:
        output = f"Command failed: {e}"
        exit_code = 1

    # Track the command execution
    ctx = _get_execution_context()
    if ctx:
        ctx.record_command(command, output, exit_code)

    # Verify command makes sense
    # If it's a pytest command, verify test files exist
    if "pytest" in command:
        # Extract file paths from pytest command
        import re

        file_patterns = re.findall(r"tests?/[\w/]+\.py", command)
        for file_path in file_patterns:
            if not Path(file_path).exists():
                raise Exception(
                    f"Command verification failed: pytest output references non-existent test file {file_path}"
                )

    return output, exit_code


def _execute_request_with_validation(
    user_request: str,
    is_implementation_request: bool = False,
    requires_tdd: bool = False,
    max_retries: int = 3,
) -> str:
    """Execute a request with validation and retry on failure.

    This is the main entry point for runtime validation integration.
    It wraps request execution with validation checks and automatic retry
    with feedback when validation fails.

    Args:
        user_request: The user's request
        is_implementation_request: Whether this is an implementation request
        requires_tdd: Whether TDD compliance is required
        max_retries: Maximum number of retries on validation failure

    Returns:
        The validated response

    Raises:
        Exception: If max retries exceeded or validation fails critically
    """
    from sage.main import _detect_phantom_implementation, _detect_repetitive_filler, _detect_tool_description_vs_execution, _validate_analysis_response, _validate_implementation_response, _validate_tdd_compliance
    global _current_execution_context

    attempt = 0
    validation_feedback = ""

    while attempt <= max_retries:
        # Create new execution context for this attempt
        _current_execution_context = _RequestExecutionContext(
            task_prompt=user_request,
            cloud_provider=_detect_target_cloud_provider(user_request),
        )

        # Build prompt (include validation feedback if this is a retry)
        # P1-4: Stateful constrained recovery - retries are more restrictive
        if attempt == 0:
            prompt = user_request
        else:
            # P1-4: Constrained recovery - explicitly require tool commands only
            prompt = f"""{user_request}

⚠️ CONSTRAINED RECOVERY MODE (attempt {attempt + 1}/{max_retries + 1})

Your previous response was REJECTED for:
{validation_feedback}

CRITICAL CONSTRAINT: Your next response MUST:
1. START with READ: or SEARCH: commands - NO preamble, NO prose
2. Use ONLY actual tool commands (READ: file.py, SEARCH: pattern)
3. Do NOT apologize, explain, or discuss - JUST execute tools
4. Do NOT make assumptions or provide generic advice

EXAMPLE OF CORRECT FORMAT:
READ: sage/main.py
READ: sage/core/tools.py
SEARCH: def validate

INCORRECT (will be rejected):
"I apologize for the confusion. Let me try again..."
"I'll now read the files..."
"Based on my understanding..."

Your response MUST start with a READ: or SEARCH: command directly."""

        # Call LLM (will be simulated in tests)
        response = _call_llm(prompt)

        # Get execution context (using helper functions that can be simulated)
        files_read = _track_files_read()
        files_written = _track_files_written()

        # Get search status from context if available
        ctx = _get_execution_context()
        search_executed = ctx.search_executed if ctx else False

        # Detect request type
        is_analysis = "analyze" in user_request.lower() or "list" in user_request.lower()

        # Extract number of recommendations from request
        import re

        num_match = re.search(
            r"(\d+)\s+(?:items?|improvements?|recommendations?)", user_request.lower()
        )
        num_recommendations = int(num_match.group(1)) if num_match else 0

        # Validate response
        violations = []

        # Check tool description vs execution
        is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(response)
        if is_descriptive:
            violations.append(
                f"Response describes tools ({', '.join(mentioned_tools[:3])}) instead of executing them. "
                "Tool commands (READ:, SEARCH:, RUN:) must be at the start of the response, not wrapped in prose."
            )

        # Check for repetitive filler
        is_filler, repetition_score = _detect_repetitive_filler(response)
        if is_filler:
            violations.append(
                f"Response contains repetitive filler content (repetition score: {repetition_score:.2f}). "
                "Provide varied, specific recommendations instead of template-based items."
            )

        # Validate analysis requests
        if is_analysis:
            is_valid, analysis_violations = _validate_analysis_response(
                response, user_request, files_read, search_executed, num_recommendations
            )
            violations.extend(analysis_violations)

        # Validate implementation requests
        if is_implementation_request:
            # Check for phantom implementation
            is_phantom, phantom_reason = _detect_phantom_implementation(
                response, files_written, is_implementation_request
            )
            if is_phantom:
                violations.append(phantom_reason)

            # Validate implementation response
            impl_valid, impl_reason = _validate_implementation_response(
                response, files_written, is_implementation_request
            )
            if not impl_valid:
                violations.append(impl_reason)

            # Check TDD compliance if required
            if requires_tdd:
                tdd_valid, tdd_reason = _validate_tdd_compliance(
                    response, files_written, is_implementation_request
                )
                if not tdd_valid:
                    violations.append(tdd_reason)

        # If no violations, accept response
        if not violations:
            _current_execution_context = None
            return response

        # Prepare feedback for retry
        validation_feedback = "\n".join(f"- {v}" for v in violations)
        attempt += 1

    # Max retries exceeded
    _current_execution_context = None
    raise Exception(
        f"Max retries exceeded ({max_retries}). "
        f"Response validation failed with: {validation_feedback}"
    )


def _file_exists(file_path: str) -> bool:
    """Check if a file exists."""
    return Path(file_path).exists()


def _simple_write_file(file_path: str, content: str) -> bool:
    """Write a file without validation. Returns True on success.

    Note: This is a simpler utility function. For validated writes, use
    _write_file() which includes protected file checks and validation.
    """
    try:
        path = Path(file_path)
        if path.name == "__init__.py":
            content = ""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return True
    except Exception:
        return False


def _read_file(file_path: str) -> str:
    """Read a file and return its content."""
    return Path(file_path).read_text("utf-8", errors="replace")


def _run_shell_command_helper(command: str) -> tuple[str, int]:
    """Run a command and return (output, exit_code)."""
    from sage.core.commands import run_shell

    try:
        result = run_shell(command, timeout=300)
        return result.stdout + result.stderr, result.returncode
    except Exception as e:
        return str(e), 1


def _call_llm(prompt: str) -> str:
    """Simulate LLM call for testing. Override in tests."""
    # This is a test hook - real implementation would call actual LLM
    return ""


def _default_test_command(cwd: Path) -> str:
    """Pick a sensible default pytest command for the current project."""
    project_root = _default_project_root(cwd)
    inner = _discover_project_test_command(project_root)
    if inner:
        return _command_from_project_root(project_root, inner, cwd)
    return "python -m pytest -v --tb=short"


def _full_project_test_command(cwd: Path) -> str:
    """Pick a full-project validation command for the current project."""
    project_root = _default_project_root(cwd)
    inner = _discover_project_full_test_command(project_root)
    if inner:
        return _command_from_project_root(project_root, inner, cwd)
    return "python -m pytest -v --tb=short"


def _resolve_implementation_test_command(cwd: Path, task_prompt: str, fallback: str) -> str:
    """Use frontend Vitest when the task is clearly about Vite/Firebase/auth UI (not only pytest)."""
    t = (task_prompt or "").lower()
    p = cwd.resolve()
    fe_pkg = p / "ai-platform" / "frontend" / "package.json"
    alt_pkg = p / "frontend" / "package.json"
    has_fe = fe_pkg.is_file() or alt_pkg.is_file()
    if not has_fe:
        return fallback
    if any(
        k in t
        for k in (
            "firebase",
            "vite",
            "frontend",
            "react",
            "auth",
            "sign in",
            "signin",
            "google",
            "apple",
            "password",
            "forgot",
            ".env",
            "vitest",
            "npm test",
            "login",
        )
    ):
        if fe_pkg.is_file():
            return "cd ai-platform/frontend && npm test -- --run"
        return "cd frontend && npm test -- --run"
    return fallback


def _implementation_archetype_hints(task_prompt: str) -> str:
    """Extra constraints so weak models stop stalling on common coding-task shapes."""
    t = (task_prompt or "").lower()
    parts: list[str] = []
    if any(
        k in t
        for k in (
            "firebase",
            "vite",
            "auth domain",
            "sign in",
            "signin",
            "google",
            "apple",
            "password",
            "forgot",
            ".env",
            "oauth",
        )
    ):
        parts.append(
            "**Web / Firebase auth:** Work under `ai-platform/frontend/` (not a root-level `web/` folder). "
            "`READ:` `ai-platform/frontend/src/firebase/auth.js`, `firebaseEnv.js`, `Login.jsx`, `AuthContext.jsx` first. "
            "Put secrets only in `ai-platform/frontend/.env` (copy from `.env.example`); never paste real keys into chat. "
            "**Production:** `VITE_*` are inlined at `npm run build` / Docker `frontend-build`. Cloud Run runtime env vars alone "
            "do **not** fix a bundle built without keys — CI must pass `--build-arg VITE_FIREBASE_*` to `docker build` "
            "(see `ai-platform/.github/workflows/deploy.yml` or `.github/workflows/deploy-cloud-run.yml`). "
            "On **`sage run`**, SAGE updates `.gitignore` for `.env` automatically; set **`SAGE_SYNC_SECRETS_TO_GITHUB=1`** "
            "(and `gh auth login`) to also push matching keys from your local `.env` to GitHub Actions secrets."
        )
    if any(
        k in t
        for k in (
            "sage cli",
            "sage-ai",
            "openrouter",
            "groq",
            "gemini",
            "anthropic",
            "api key",
            "credential",
            "missing key",
            "invalid api key",
            "401",
            "403",
            "~/.sage",
            "config.json",
        )
    ):
        parts.append(
            "**SAGE CLI / provider keys:** Cloud providers expect env vars (see `sage/core/credentials.py`, "
            "`sage/config.py`). Match the provider name to `SAGE_*_API_KEY` / `*_API_KEY`; fix loading or docs in-code — "
            "still use `FILE:` blocks so changes persist."
        )
    return "\n\n".join(parts)


def _suggest_target_paths_for_task(cwd: Path, task_prompt: str) -> str:
    """Return paths that ACTUALLY EXIST in the current workspace relevant to the task.

    IMPORTANT: Only suggest paths that exist on disk.  Never inject hardcoded
    paths from a different project — that causes the model to write files with
    wrong paths (e.g. sage-ai paths appearing in an advertisement_platform repo).
    """
    t = (task_prompt or "").lower()
    p = cwd.resolve()
    lines: list[str] = []

    # Detect greenfield / new-project tasks — no paths exist yet, skip hints
    _greenfield_kws = [
        "full platform", "full project", "full app", "full stack", "from scratch",
        "brand new", "new platform", "new project", "monorepo", "entire platform",
        "build a ", "create a ",
    ]
    if sum(1 for k in _greenfield_kws if k in t) >= 1 or len(task_prompt) > 600:
        return ""  # Greenfield: no existing files to hint at

    # Only suggest files that are verified to exist in THIS workspace
    auth_keywords = ("firebase", "vite", "auth", "sign in", "signin", "password",
                     ".env", "oauth", "login")
    if any(x in t for x in auth_keywords):
        candidates = [
            "src/firebase/auth.js", "src/firebase/auth.ts",
            "frontend/src/firebase/auth.js", "frontend/src/firebase/auth.ts",
            "src/auth.js", "src/auth.ts",
            "frontend/.env", "frontend/.env.example",
            ".env", ".env.example",
        ]
        for rel in candidates:
            if (p / rel).is_file():
                lines.append(f"- {rel}")

    sage_keywords = ("sage cli", "sage-ai", "openrouter", "groq", "gemini",
                     "anthropic", "api key", "credential", "missing key", "~/.sage")
    if any(x in t for x in sage_keywords):
        for rel in ("sage/core/credentials.py", "sage/config.py",
                    "sage/main.py", "core/credentials.py"):
            if (p / rel).is_file():
                lines.append(f"- {rel}")

    # Generic fallback: scan top-level structure of the ACTUAL project
    if not lines:
        try:
            top = sorted(
                r.relative_to(p)
                for r in p.iterdir()
                if not r.name.startswith(".") and r.name not in ("node_modules", "__pycache__")
            )
            lines = [f"- {r}" for r in top[:10]]
        except Exception:
            pass

    return "\n".join(lines[:12])


def _build_implementation_completion_nudge(
    task_prompt: str,
    test_command: str,
    attempt: int,
    max_rounds: int,
    *,
    path_hints: str = "",
) -> str:
    """Hard nudge for models that only produce prose and never emit FILE: blocks."""
    # Detect greenfield — completely different nudge needed
    _gf_kws = [
        "full platform", "full project", "full app", "full stack", "from scratch",
        "brand new", "new platform", "new project", "monorepo", "entire platform",
        "entire project", "end-to-end", "all features", "complete platform",
        "build a ", "create a ",
    ]
    _is_gf = sum(1 for k in _gf_kws if k in task_prompt.lower()) >= 1 or len(task_prompt) > 600

    if _is_gf:
        return f"""SAGE ENFORCEMENT — NEW PROJECT SCAFFOLD (attempt {attempt}/{max_rounds})

You are building a **brand-new project from scratch**. No files exist yet — you must CREATE them all.

Your previous response contained only prose/markdown. That is NOT how SAGE saves files.
The ONLY way to create files is the `FILE:` block format shown below.

Start writing the project files NOW using this exact format:

FILE: package.json
```json
{{
  "name": "advertisement-platform",
  ...complete file contents...
}}
```

FILE: services/backend/pyproject.toml
```toml
...complete file contents...
```

FILE: services/backend/app/main.py
```python
...complete file contents...
```

RULES:
- Start with root config files (package.json, pyproject.toml, docker-compose.yml, etc.)
- Then backend source, then frontend source, then tests LAST
- Every FILE: block must contain COMPLETE file contents — no stubs or TODOs
- Do NOT write architecture docs or markdown — ONLY FILE: blocks
- After writing as many files as fit in this response, more batches will be requested

Begin with the root config files now.
"""

    hint_block = (
        f"\nExisting paths in this project you may need to edit:\n{path_hints}\n"
        if path_hints.strip()
        else "\n"
    )
    arch = _implementation_archetype_hints(task_prompt)
    arch_block = f"\n{arch}\n\n" if arch.strip() else ""
    return f"""SAGE ENFORCEMENT — attempt {attempt}/{max_rounds}

You must **change the codebase** for this request. So far, **no `FILE:` blocks** were written, so **no files were saved** on disk.
{hint_block}{arch_block}
In your next reply, do all of the following (this is the only way SAGE applies your work):

1. **Emit one or more `FILE:` blocks** (each must be: `FILE: <relative path>` on its own line, then a full fenced code block with the **complete** file content — not a snippet).

2. **Run the project’s tests** on its own line:
`RUN: {test_command}`

3. If tests fail, **fix** using new `FILE:` blocks and `RUN: ` again. Do not claim the task is complete until the test run shows **passing** output.

**Valid shape (copy this structure; use real paths and full file bodies):**
FILE: path/relative/to/repo.js
```javascript
// entire file contents here
```
RUN: {test_command}

Do not answer with only `READ:`, `SEARCH:`, or prose. The user’s task:
---
{task_prompt}
---
"""


def _collect_autopolit_priority_hints(cwd: Path, max_items: int = 6) -> list[str]:
    """Collect whole-codebase risk signals to guide autopolit task choice."""
    findings: list[tuple[int, str]] = []

    def _read_text(path: Path) -> str:
        try:
            return path.read_text("utf-8", errors="replace")
        except OSError:
            return ""

    project_root = _default_project_root(cwd)
    deploy_yml = project_root / ".github" / "workflows" / "deploy.yml"
    backend_app = project_root / "backend" / "app.py"
    pyproject = project_root / "pyproject.toml"
    sage_main = project_root / "sage" / "main.py"
    sage_tests = project_root / "sage" / "tests"

    deploy_text = _read_text(deploy_yml)
    if "--allow-unauthenticated" in deploy_text:
        findings.append(
            (10, "Deployment risk: production deploy is configured as unauthenticated.")
        )

    backend_text = _read_text(backend_app)
    if 'allow_origins=["*"]' in backend_text or 'allow_origins=["*",' in backend_text:
        findings.append((20, "API exposure risk: backend CORS currently allows any origin."))

    pyproject_text = _read_text(pyproject)
    if sage_tests.exists() and "sage/tests" not in pyproject_text:
        findings.append(
            (
                15,
                "Validation gap: default pytest discovery does not include sage/tests.",
            )
        )

    main_text = _read_text(sage_main)
    if main_text:
        line_count = len(main_text.splitlines())
        if line_count >= 8000:
            findings.append(
                (
                    40,
                    f"Maintainability hotspot: sage/main.py is {line_count} lines long.",
                )
            )

        broad_excepts = len(re.findall(r"except Exception", main_text))
        if broad_excepts >= 25:
            findings.append(
                (
                    35,
                    f"Reliability hotspot: sage/main.py has {broad_excepts} broad exception handlers.",
                )
            )

        shell_true_uses = len(re.findall(r"shell=True", main_text))
        if shell_true_uses:
            findings.append(
                (
                    30,
                    f"Command execution risk: sage/main.py uses shell=True {shell_true_uses} times.",
                )
            )

    source_exts = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java"}
    large_files: list[tuple[int, str]] = []

    from sage.core.project import safe_walk, SKIP_DIRS

    # Optimization: Use safe_walk for efficiency
    for path in safe_walk(project_root, skip_dirs=SKIP_DIRS | {".sage"}):
        if path.suffix.lower() not in source_exts:
            continue
        try:
            rel = path.relative_to(project_root)
        except ValueError:
            continue

        try:
            large_files.append(
                (
                    len(path.read_text("utf-8", errors="replace").splitlines()),
                    rel.as_posix(),
                )
            )
        except OSError:
            continue
    for lines, rel in sorted(large_files, reverse=True)[:3]:
        if lines >= 500:
            findings.append((50, f"Large-file hotspot: {rel} is {lines} lines."))

    findings.sort(key=lambda item: (item[0], item[1]))
    return [message for _, message in findings[:max_items]]


def _response_describes_code_without_file_blocks(response: str) -> bool:
    """Detect code-change narratives that never emit executable FILE blocks."""
    # Strip thinking blocks first — qwen3-style models describe their plan
    # inside <think>...</think>. That trace isn't a "narrative", it's the
    # model's internal reasoning. Don't penalize it.
    from sage.core.thinking_filter import strip_thinking_blocks
    response = strip_thinking_blocks(response)
    if "FILE:" in response:
        return False

    path_listing = re.search(
        r"(?m)^\s*(?:#+\s*)?(?:[\w.-]+/)+[\w.-]+\.(?:py|js|ts|tsx|jsx|json|toml|ya?ml|sh|md|sql|go|rs|java|css|html)\s*$",
        response,
    )
    has_change_sections = any(
        marker in response for marker in ("Code Changes", "Tests Written", "Final Status")
    )
    has_fenced_code = response.count("```") >= 2
    return bool(path_listing and (has_change_sections or has_fenced_code))


# ══════════════════════════════════════════════════════════════════════════════
# GLOBAL INSTANCES
# ══════════════════════════════════════════════════════════════════════════════


# Global failure loop detector instance
_failure_loop_detector = FailureLoopDetector()


def _should_stop_autopolit_cycle(cycle_history: list[dict]) -> tuple[bool, str]:
    """Determine if autopilot should stop based on cycle history.

    Args:
        cycle_history: List of dicts with 'response' and 'success' keys

    Returns:
        Tuple of (should_stop, reason)
    """
    if len(cycle_history) < 3:
        return False, ""

    # Check for identical responses in last 3 cycles
    recent_responses = [cycle["response"] for cycle in cycle_history[-3:]]
    recent_hashes = [_compute_response_hash(r) for r in recent_responses]

    if len(set(recent_hashes)) == 1:
        return True, "Autopilot is repeating identical responses"

    # Check for repeated failures
    recent_failures = sum(1 for cycle in cycle_history[-3:] if not cycle.get("success", False))
    if recent_failures >= 3:
        return True, "Too many consecutive failures"

    return False, ""


def _validate_implementation_claim(response: str) -> tuple[bool, str]:
    """Validate that implementation claims have FILE: blocks.

    Args:
        response: The LLM response text

    Returns:
        Tuple of (is_valid, reason)
    """
    # Check for implementation claims
    impl_claims = [
        "i've implemented",
        "i have implemented",
        "implementation complete",
        "implemented the",
        "created the implementation",
        "built the feature",
    ]

    response_lower = response.lower()
    has_impl_claim = any(claim in response_lower for claim in impl_claims)

    if not has_impl_claim:
        return True, ""  # No claim made

    # Check for FILE: blocks
    has_file_blocks = "FILE:" in response or "file:" in response

    if not has_file_blocks:
        return False, "Response claims implementation but has no FILE: blocks"

    return True, ""


def _validate_completion_claim(response: str) -> bool:
    """Check if completion claim has evidence (code or execution results).

    Args:
        response: The LLM response text

    Returns:
        True if completion claim has evidence, False otherwise
    """
    completion_claims = ["done!", "complete!", "all done", "finished", "completed"]

    response_lower = response.lower()
    has_completion_claim = any(claim in response_lower for claim in completion_claims)

    if not has_completion_claim:
        return True  # No claim made

    # Check for evidence
    has_file_blocks = "FILE:" in response
    has_run_commands = "RUN:" in response
    has_results = "RESULT:" in response

    return has_file_blocks or has_run_commands or has_results


def _validate_test_claim(response: str, test_output: str) -> bool:
    """Validate that test passing claims match actual test output.

    Args:
        response: The LLM response text
        test_output: Actual test execution output

    Returns:
        True if claims are accurate, False if misleading
    """
    # Check for "tests passing" claims
    passing_claims = [
        "tests are passing",
        "all tests pass",
        "tests pass",
        "tests passing",
        "green",
        "✓",
    ]

    response_lower = response.lower()
    claims_passing = any(claim in response_lower for claim in passing_claims)

    if not claims_passing:
        return True  # No claim made

    # Parse actual test results (use simple schema which has is_success)
    result = _parse_test_output_simple(test_output)

    # Claim is accurate only if tests actually passed
    return result["is_success"]


def _validate_test_files_exist(response: str, cwd: Path) -> tuple[bool, str]:
    """Verify that test files mentioned in response actually exist.

    PROOF OF EXECUTION: Prevents hallucinated test file claims.

    Args:
        response: The LLM response text
        cwd: Current working directory

    Returns:
        Tuple of (is_valid, reason)
    """
    # Extract test file paths from response
    test_file_patterns = [
        r"tests?/test_[\w/]+\.py",
        r"tests?/[\w/]+_test\.py",
        r"test_[\w/]+\.py",
    ]

    mentioned_test_files = []
    for pattern in test_file_patterns:
        matches = re.findall(pattern, response)
        mentioned_test_files.extend(matches)

    if not mentioned_test_files:
        return True, ""  # No test files mentioned

    # Check if mentioned test files exist
    missing_files = []
    for test_file in mentioned_test_files:
        test_path = cwd / test_file.lstrip("./")
        if not test_path.exists():
            missing_files.append(test_file)

    if missing_files:
        return False, f"Test files mentioned but don't exist: {', '.join(missing_files[:3])}"

    return True, ""


def _validate_execution_claim(
    response: str,
    executed_commands: list[tuple[str, str, int]],
    files_written: list[str],
    cwd: Path,
) -> tuple[bool, str]:
    """Validate that execution claims match actual execution results.

    PROOF OF EXECUTION: Cross-references claims with actual results.

    Args:
        response: The LLM response text
        executed_commands: List of (command, output, exit_code) tuples
        files_written: List of files actually written
        cwd: Current working directory

    Returns:
        Tuple of (is_valid, reason)
    """
    response_lower = response.lower()

    # Check for pytest success claims
    pytest_success_claims = ["tests pass", "all tests pass", "pytest passed", "tests are green"]
    claims_pytest_success = any(claim in response_lower for claim in pytest_success_claims)

    if claims_pytest_success:
        # Find pytest executions
        pytest_executions = [
            (cmd, out, code) for cmd, out, code in executed_commands if "pytest" in cmd.lower()
        ]

        if not pytest_executions:
            return False, "Claims tests passed but no pytest commands were actually executed"

        # Check if any pytest actually passed
        any_passed = False
        for cmd, output, exit_code in pytest_executions:
            if exit_code == 0:
                any_passed = True
                break

        if not any_passed:
            return (
                False,
                "Claims tests passed but all pytest executions failed (non-zero exit code)",
            )

    # Check for file creation claims
    file_creation_claims = ["created file", "wrote file", "generated file"]
    claims_file_creation = any(claim in response_lower for claim in file_creation_claims)

    if claims_file_creation and len(files_written) == 0:
        return False, "Claims files were created but no files were actually written"

    # Check for specific file claims
    mentioned_files = re.findall(
        r'(?:created|wrote|generated)\s+[`"]?([a-z_][\w/]*\.[a-z]+)[`"]?', response_lower
    )
    for mentioned_file in mentioned_files:
        if mentioned_file not in files_written:
            file_path = cwd / mentioned_file
            if not file_path.exists():
                return False, f"Claims to have created {mentioned_file} but file doesn't exist"

    return True, ""


def _parse_test_result_accurately(test_output: str) -> dict:
    """Parse test output accurately, handling edge cases.

    Args:
        test_output: Raw test execution output

    Returns:
        Dict with passed, failed, and overall_success keys
    """
    import re

    # Look for pytest-style summary
    # "===== 5 failed, 10 passed ====="
    # "===== 0 passed ====="

    passed = 0
    failed = 0

    # Match "N passed"
    passed_match = re.search(r"(\d+)\s+passed", test_output)
    if passed_match:
        passed = int(passed_match.group(1))

    # Match "N failed"
    failed_match = re.search(r"(\d+)\s+failed", test_output)
    if failed_match:
        failed = int(failed_match.group(1))

    return {"passed": passed, "failed": failed, "overall_success": failed == 0 and passed > 0}


def _parse_test_output_simple(test_output: str) -> dict:
    """Parse test output to extract basic results (simple schema).

    NOTE: This is a simplified parser. For full schema including
    has_collection_errors, use _parse_test_output from shell.py.

    Returns:
        Dict with total_passed, total_failed, is_success
    """
    result = _parse_test_result_accurately(test_output)

    return {
        "total_passed": result["passed"],
        "total_failed": result["failed"],
        "is_success": result["overall_success"],
    }


# NOTE: Do NOT override _parse_test_output here!
# The import from shell.py (line 185) provides the rich parser with has_collection_errors.
# The TDD gate (line 1803) requires the rich schema.
# For tests that need the simple schema, use _parse_test_output_simple directly.


def _get_simple_test_result(test_output: str) -> dict:
    """Alias for test files that expect the simple schema.

    Returns: Dict with total_passed, total_failed, is_success
    """
    return _parse_test_output_simple(test_output)


def _validate_file_path_in_workspace(file_path: Path, workspace: Path) -> tuple[bool, str]:
    """Validate that file path is within workspace (no traversal).

    Args:
        file_path: The file path to validate
        workspace: The workspace root directory

    Returns:
        Tuple of (is_valid, reason)
    """
    try:
        # Resolve both paths to absolute
        file_abs = file_path.resolve() if not file_path.is_absolute() else file_path
        workspace_abs = workspace.resolve()

        # For relative paths, make them relative to workspace
        if not file_path.is_absolute():
            file_abs = (workspace_abs / file_path).resolve()

        # Check if file is within workspace
        try:
            file_abs.relative_to(workspace_abs)
            return True, ""
        except ValueError:
            return False, f"Path {file_path} is outside workspace {workspace}"

    except Exception as e:
        return False, f"Invalid path: {e}"


def _normalize_file_path(file_path: Path, workspace: Path) -> Path:
    """Normalize file path to be relative to workspace.

    Args:
        file_path: File path (absolute or relative)
        workspace: Workspace root directory

    Returns:
        Relative path from workspace
    """
    try:
        file_abs = file_path.resolve() if not file_path.is_absolute() else file_path
        workspace_abs = workspace.resolve()

        # If file is absolute and within workspace, make it relative
        if file_path.is_absolute():
            try:
                return file_abs.relative_to(workspace_abs)
            except ValueError:
                # Not within workspace, return as-is
                return file_path

        # Already relative
        return file_path

    except Exception:
        return file_path


def _validate_retry_has_evidence(original_response: str, retry_response: str) -> bool:
    """Check if retry response has new tool usage (evidence of investigation).

    Args:
        original_response: The original response text
        retry_response: The retry response text

    Returns:
        True if retry has new tool commands, False otherwise
    """
    # Extract tool commands from both responses
    original_tools = _extract_tool_command_names(original_response)
    retry_tools = _extract_tool_command_names(retry_response)

    # Retry should have new tool commands
    new_tools = set(retry_tools) - set(original_tools)

    return len(new_tools) > 0 or len(retry_tools) > len(original_tools)


def _extract_tool_command_names(response: str) -> list[str]:
    """Extract tool command names from response.

    Returns:
        List of tool command names like ["READ", "SEARCH"]
    """
    import re

    tool_pattern = r"^\s*(?:-|\*|•)?\s*(READ|SEARCH|RUN|FILE):\s*"
    matches = re.findall(tool_pattern, response, re.MULTILINE | re.IGNORECASE)

    return [m.upper() for m in matches]


def _response_has_tool_results(response: str) -> bool:
    """Check if response contains tool execution results.

    Args:
        response: The response text

    Returns:
        True if response has RESULT: blocks
    """
    return "RESULT:" in response or "result:" in response.lower()


def _extract_tool_commands_robust(response: str) -> list[dict]:
    """Extract tool commands from response, handling indentation and bullets.

    Args:
        response: The response text

    Returns:
        List of dicts with 'command' and 'args' keys
    """
    import re

    commands = []

    # Pattern matches: optional indent/bullet + command + colon + args
    # Examples:
    #   READ: file.py
    #   - READ: file.py
    #   •  SEARCH: pattern
    #       READ: file.py
    pattern = r"^\s*(?:-|\*|•|\d+\.|\d+\))?\s*(READ|SEARCH|RUN|FILE):\s*(.+)$"

    for line in response.split("\n"):
        match = re.match(pattern, line, re.IGNORECASE)
        if match:
            command = match.group(1).upper()
            args = match.group(2).strip()
            commands.append({"command": command, "args": args})

    return commands


def _validate_list_generation_result(
    response: str, extracted_list: list, expected_min_items: int = 1
) -> tuple[bool, str]:
    """Validate that list generation produced non-empty results.

    Args:
        response: The LLM response text
        extracted_list: The extracted list items
        expected_min_items: Minimum expected items

    Returns:
        Tuple of (is_valid, reason)
    """
    # Check for completion claims
    completion_claims = [
        "found all",
        "complete",
        "done",
        "finished the analysis",
        "that's all",
    ]

    response_lower = response.lower()
    claims_complete = any(claim in response_lower for claim in completion_claims)

    if claims_complete and len(extracted_list) < expected_min_items:
        return (
            False,
            f"Response claims completion but list is empty (expected {expected_min_items}+ items)",
        )

    return True, ""


def _validate_list_items_exist(
    listed_files: list[str], workspace: Path
) -> tuple[list[str], list[str]]:
    """Validate that listed files actually exist.

    Args:
        listed_files: List of file paths mentioned
        workspace: Workspace root directory

    Returns:
        Tuple of (valid_files, invalid_files)
    """
    valid_files = []
    invalid_files = []

    for file_path in listed_files:
        full_path = workspace / file_path
        if full_path.exists():
            valid_files.append(file_path)
        else:
            invalid_files.append(file_path)

    return valid_files, invalid_files


def _handle_context_overflow(
    context: str,
    max_tokens: int,
    preserve_file_writes: bool = True,
    preserve_tool_results: bool = True,
) -> str:
    """Handle context overflow by smart truncation preserving important content.

    Args:
        context: The full context string
        max_tokens: Maximum tokens allowed
        preserve_file_writes: Whether to preserve FILE: blocks
        preserve_tool_results: Whether to preserve RESULT: blocks

    Returns:
        Truncated context that fits within max_tokens
    """
    import re

    # Extract important blocks to preserve
    preserved_blocks = []

    if preserve_file_writes:
        # Extract FILE: blocks
        file_blocks = re.findall(
            r"FILE:.*?(?=\n(?:FILE:|SEARCH:|READ:|RUN:|$))", context, re.DOTALL
        )
        preserved_blocks.extend(file_blocks)

    if preserve_tool_results:
        # Extract RESULT: blocks
        result_blocks = re.findall(
            r"RESULT:.*?(?=\n(?:FILE:|SEARCH:|READ:|RUN:|$))", context, re.DOTALL
        )
        preserved_blocks.extend(result_blocks)

    # Build truncated context
    # Keep last portion of context + preserved blocks
    preserved_text = "\n\n".join(preserved_blocks)

    # Rough token estimation (4 chars = 1 token)
    preserved_size = len(preserved_text) // 4
    remaining_tokens = max_tokens - preserved_size

    if remaining_tokens > 0:
        # Keep last portion of context
        context_size = remaining_tokens * 4
        truncated_context = context[-context_size:]

        return truncated_context + "\n\n" + preserved_text
    else:
        # Just return preserved blocks
        return preserved_text


