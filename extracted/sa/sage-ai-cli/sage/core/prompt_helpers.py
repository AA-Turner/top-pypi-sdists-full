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


def _truncate_context_smartly(messages: list[dict], max_tokens: int) -> list[dict]:
    """Smart truncation of message context preserving recent and important messages.

    Args:
        messages: List of message dicts with role and content
        max_tokens: Maximum tokens allowed

    Returns:
        Truncated list of messages
    """

    # Rough token estimation (4 chars = 1 token)
    def estimate_tokens(msg: dict) -> int:
        return len(str(msg.get("content", ""))) // 4

    # Always keep system message and last 2 messages
    if len(messages) <= 3:
        return messages

    system_msg = messages[0] if messages[0].get("role") == "system" else None
    recent_msgs = messages[-2:]
    middle_msgs = messages[1:-2] if system_msg else messages[:-2]

    # Calculate tokens
    system_tokens = estimate_tokens(system_msg) if system_msg else 0
    recent_tokens = sum(estimate_tokens(m) for m in recent_msgs)
    remaining_tokens = max_tokens - system_tokens - recent_tokens

    # Add middle messages that fit, prioritizing those with FILE: blocks
    kept_middle = []
    for msg in reversed(middle_msgs):
        msg_tokens = estimate_tokens(msg)
        if msg_tokens <= remaining_tokens:
            # Prioritize messages with FILE: blocks
            if "FILE:" in str(msg.get("content", "")):
                kept_middle.insert(0, msg)
                remaining_tokens -= msg_tokens

    # Build final message list
    result = []
    if system_msg:
        result.append(system_msg)
    result.extend(kept_middle)
    result.extend(recent_msgs)

    return result


def _handle_model_fallback(requested_model: str, fallback_model: str, reason: str) -> None:
    """Handle model fallback by warning user.

    Args:
        requested_model: The model that was requested
        fallback_model: The fallback model being used
        reason: Reason for fallback
    """
    # Use the global renderer instance
    renderer.warning(
        f"⚠️  Model fallback: {requested_model} → {fallback_model}\n"
        f"   Reason: {reason}\n"
        f"   Note: Response quality may be affected"
    )

    _log_model_fallback(requested_model, fallback_model, reason)


def _log_model_fallback(requested: str, actual: str, reason: str) -> None:
    """Log model fallback event.

    Args:
        requested: Requested model ID
        actual: Actual model ID used
        reason: Reason for fallback
    """
    logger.warning(f"Model fallback: requested={requested}, actual={actual}, reason={reason}")


def _get_fallback_statistics() -> dict:
    """Get statistics on model fallback frequency.

    Returns:
        Dict with total_fallbacks and fallback_rate
    """
    # This would track fallbacks in memory or persistent storage
    # For now, return empty stats
    return {"total_fallbacks": 0, "fallback_rate": 0.0}


def _is_broken_test_file(filepath: str, error_output: str) -> bool:
    """Determine if a test file should be deleted due to persistent errors.

    A test file is considered broken if:
    1. It's a test file (in tests/ directory or starts with test_)
    2. The error output mentions import errors for this file
    3. The file imports modules that don't exist
    """
    # Must be a test file
    if not (filepath.startswith("tests/") or "test_" in filepath):
        return False

    # Must be mentioned in import errors
    filename = Path(filepath).name
    filepath_in_error = filepath in error_output or filename in error_output

    # Check for import-related errors mentioning this file
    import_errors = [
        "ImportError",
        "ModuleNotFoundError",
        "cannot import name",
        "No module named",
        "attempted relative import",
    ]
    has_import_error = any(err in error_output for err in import_errors)

    return filepath_in_error and has_import_error


def _cleanup_broken_test_files(cwd: Path, error_output: str) -> list[str]:
    """Flag broken test files with persistent import errors without deleting them.

    Returns a list of candidate file paths that need human or model review.
    """
    flagged = []

    # Find test files mentioned in errors
    test_dirs = [cwd / "tests", cwd / "tests" / "sage"]
    for test_dir in test_dirs:
        if not test_dir.exists():
            continue
        for test_file in test_dir.glob("test_*.py"):
            rel_path = str(test_file.relative_to(cwd))
            if _is_broken_test_file(rel_path, error_output):
                flagged.append(rel_path)

    return flagged


def _is_complex_task(task: str) -> bool:
    """Heuristic: does this task benefit from multi-step decomposition?

    Complex tasks have multiple sub-objectives, mention multiple files,
    or use words suggesting multi-part work. Simple tasks (explain X,
    fix typo, rename Y) don't need decomposition overhead.
    """
    lower = task.lower()
    # Multi-part indicators
    multi_indicators = [
        " and ",
        " then ",
        " also ",
        " with tests",
        "add a .* and",
        "create .* including",
        "implement",
        "build",
        "refactor",
        "migrate",
    ]
    score = sum(1 for pat in multi_indicators if re.search(pat, lower))
    # Long prompts are usually complex
    if len(task.split()) > 25:
        score += 1
    # Mentions multiple files
    file_mentions = re.findall(r"[\w/]+\.(?:py|js|ts|go|rs|java)\b", task)
    if len(file_mentions) >= 2:
        score += 1
    return score >= 2


def _should_use_multistep_pipeline(
    task: str,
    *,
    classification: _ClassifiedRequest | None = None,
    is_local_model: bool = False,
) -> bool:
    """Route complex local tasks into a model-driven multistep pipeline."""
    from sage.cli_core import _get_current_classification, _should_seed_recursive_analysis_context
    if not is_local_model:
        return False

    effective_classification = classification or _get_current_classification()
    if effective_classification and effective_classification.read_only:
        if _should_seed_recursive_analysis_context(task, effective_classification):
            return True
        if effective_classification.request_type == _RequestType.LIST_GENERATION:
            return True
        if len(task.split()) > 20:
            return True

    return _is_complex_task(task)


def _should_use_seeded_synthesis_only(
    task_prompt: str,
    classification: _ClassifiedRequest | None,
    seeded_full_file_coverage_context: str,
) -> bool:
    """Use synthesis-only for broad local analysis when SAGE already read the repo."""
    from sage.cli_core import _should_seed_recursive_analysis_context
    return bool(
        classification
        and classification.read_only
        and seeded_full_file_coverage_context
        and _should_seed_recursive_analysis_context(task_prompt, classification)
    )


def _should_skip_ai_orchestration(
    task_prompt: str,
    classification: _ClassifiedRequest | None,
    *,
    is_local: bool,
) -> bool:
    """Skip pre-analysis orchestration when SAGE already gathered broad local evidence."""
    from sage.cli_core import _should_seed_recursive_analysis_context
    return bool(
        is_local
        and classification
        and classification.read_only
        and _should_seed_recursive_analysis_context(task_prompt, classification)
    )


def _get_project_file_listing(cwd: Path, max_files: int = 50) -> str:
    """Get a compact listing of verified project files for discovery.

    This helps the model know what files exist before trying to read them,
    preventing it from guessing filenames based on conventions.
    """
    skip_dirs = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        ".cache",
        "target",
        ".tox",
        "egg-info",
        ".eggs",
        ".mypy_cache",
        ".pytest_cache",
        "htmlcov",
    }
    source_exts = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".rs",
        ".go",
        ".java",
        ".c",
        ".cpp",
        ".rb",
        ".sh",
    }
    config_files = {
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "requirements.txt",
        "setup.py",
    }

    files: list[str] = []
    # Optimization: Use safe_walk for efficiency in large non-git directories
    from sage.core.project import safe_walk

    for p in safe_walk(cwd, skip_dirs=skip_dirs):
        try:
            rel = p.relative_to(cwd)
            # Include source files and config files
            if p.suffix.lower() in source_exts or p.name in config_files:
                files.append(str(rel))
                if len(files) >= max_files + 100:  # Scan slightly more than needed for counting
                    break
        except (ValueError, OSError):
            continue

    if not files:
        return ""

    listing = "\n".join(f"  - {f}" for f in files[:max_files])
    more = f"\n  ... and {len(files) - max_files} more files" if len(files) >= max_files else ""
    return (
        "\n\nVERIFIED WORKSPACE PATHS (examples from the current project root):\n"
        f"{listing}{more}"
    )


def _sample_workspace_paths(cwd: Path, max_files: int = 3) -> list[str]:
    """Return a few representative, real paths from the current workspace."""
    skip_dirs = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        ".cache",
        "target",
        ".tox",
        "egg-info",
        ".eggs",
        ".mypy_cache",
        ".pytest_cache",
        "htmlcov",
    }
    priority_names = {
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "README.md",
        "Makefile",
        "Dockerfile",
    }
    source_exts = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".rs",
        ".go",
        ".java",
        ".c",
        ".cpp",
        ".rb",
        ".sh",
    }
    stem_priority = {"main", "app", "index", "cli", "server", "config", "__init__"}

    candidates: list[tuple[tuple[int, int, int, str], str]] = []
    # Optimization: Use safe_walk for efficiency
    from sage.core.project import safe_walk

    for path in safe_walk(cwd, skip_dirs=skip_dirs):
        try:
            rel = path.relative_to(cwd)
            score = (
                0 if rel.name in priority_names else 1,
                (
                    0
                    if path.suffix.lower() in source_exts and path.stem.lower() in stem_priority
                    else 1
                ),
                len(rel.parts),
                rel.as_posix(),
            )
            candidates.append((score, rel.as_posix()))
            # Limit candidates to keep sorting fast in huge dirs
            if len(candidates) >= 1000:
                break
        except ValueError:
            continue

    candidates.sort(key=lambda item: item[0])
    return [path for _, path in candidates[:max_files]]


def _build_workspace_map(
    cwd: Path,
    *,
    max_dirs: int = 16,
    max_files_per_dir: int = 5,
) -> str:
    """Build a compact workspace map so models understand the repo layout."""
    skip_dirs = {
        ".git",
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        "dist",
        "build",
        ".next",
        ".cache",
        "target",
        ".tox",
        "egg-info",
        ".eggs",
        ".mypy_cache",
        ".pytest_cache",
        "htmlcov",
    }
    source_exts = {
        ".py",
        ".js",
        ".ts",
        ".tsx",
        ".jsx",
        ".rs",
        ".go",
        ".java",
        ".c",
        ".cpp",
        ".rb",
        ".sh",
        ".css",
        ".html",
        ".sql",
    }
    config_names = {
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "requirements.txt",
        "setup.py",
        "Dockerfile",
        "docker-compose.yml",
        "Makefile",
        "README.md",
    }
    important_dir_names = {
        "src",
        "app",
        "apps",
        "sage",
        "backend",
        "frontend",
        "lib",
        "libs",
        "tests",
        "test",
        "scripts",
        "docs",
        "config",
    }

    from collections import defaultdict

    top_level_dirs: set[str] = set()
    top_level_files: list[str] = []
    config_files: list[str] = []
    dir_counts: dict[str, int] = {}
    dir_samples: dict[str, list[str]] = defaultdict(list)
    source_dirs: set[str] = set()
    test_dirs: set[str] = set()
    config_dirs: set[str] = set()
    total_files = 0
    source_files = 0
    test_files = 0

    # Use os.walk for efficiency and early directory skipping
    for root, dirs, files in os.walk(cwd):
        # Skip hidden and excluded directories
        dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
        root_path = Path(root)

        for f in sorted(files):
            p = root_path / f
            try:
                rel = p.relative_to(cwd)
            except ValueError:
                continue

            if f.startswith("."):
                continue

            rel_str = rel.as_posix()
            if p.is_dir():
                # Note: os.walk separates dirs and files, but we check p.is_dir()
                # just in case, though it shouldn't be needed here.
                if len(rel.parts) == 1:
                    top_level_dirs.add(rel_str)
                continue
            if not p.is_file():
                continue

            total_files += 1
            parent = rel.parent.as_posix() if rel.parent != Path(".") else "."

            # Handle top level dirs from parent perspective
            if len(rel.parts) > 1:
                top_level_dirs.add(rel.parts[0])

            dir_counts[parent] = dir_counts.get(parent, 0) + 1
            if len(dir_samples[parent]) < max_files_per_dir:
                dir_samples[parent].append(rel.name)

            suffix = p.suffix.lower()
            if suffix in source_exts:
                source_files += 1
                source_dirs.add(parent)
            if p.name.startswith("test_") or any(part in {"tests", "test"} for part in rel.parts):
                test_files += 1
                test_dirs.add(parent)
            if (
                p.name in config_names or suffix in {".toml", ".json", ".yaml", ".yml", ".ini"}
            ) and len(config_files) < 12:
                config_files.append(rel_str)
                config_dirs.add(parent)
            if len(rel.parts) == 1 and len(top_level_files) < 12:
                top_level_files.append(rel_str)

            # Safety limit for workspace map scanning
            if total_files > 5000:
                break
        if total_files > 5000:
            break

    def _score_directory(directory: str) -> tuple[int, int, str]:
        depth = 0 if directory == "." else directory.count("/") + 1
        score = dir_counts.get(directory, 0)
        name = directory.split("/")[-1] if directory != "." else "."
        data_like_names = {"data", "content", "metadata", "uploads", "cache", "generated"}
        if directory == ".":
            score += 1000
        if directory in source_dirs:
            score += 25
        if directory in test_dirs:
            score += 20
        if directory in config_dirs:
            score += 18
        if name in important_dir_names:
            score += 15
        if (
            name in data_like_names
            and directory not in source_dirs
            and directory not in test_dirs
            and directory not in config_dirs
        ):
            score -= 25
        if (
            directory != "."
            and directory not in source_dirs
            and directory not in test_dirs
            and directory not in config_dirs
            and name not in important_dir_names
        ):
            score -= 10
        if depth == 1:
            score += 10
        elif depth > 2:
            score -= (depth - 2) * 5
        return (-score, depth, directory)

    candidate_dirs = {
        directory
        for directory in dir_counts
        if directory == "."
        or directory in source_dirs
        or directory in test_dirs
        or directory in config_dirs
        or directory.count("/") == 0
        or directory.split("/")[-1] in important_dir_names
    }
    candidate_dirs.update(top_level_dirs)
    highlighted_dirs = sorted(candidate_dirs, key=_score_directory)[:max_dirs]

    lines = [
        "WORKSPACE MAP:",
        f"Project root: {cwd}",
        f"Visible files: {total_files} | source files: {source_files} | test files: {test_files}",
    ]
    if top_level_dirs:
        lines.append("Top-level directories: " + ", ".join(sorted(top_level_dirs)[:12]))
    if top_level_files:
        lines.append("Top-level files: " + ", ".join(top_level_files[:12]))
    if config_files:
        lines.append("Key config files: " + ", ".join(config_files[:10]))
    if highlighted_dirs:
        lines.append("Directory snapshots:")
        for directory in highlighted_dirs:
            display = "." if directory == "." else f"{directory}/"
            sample_files = dir_samples.get(directory, [])
            lines.append(f"  - {display} ({dir_counts.get(directory, 0)} files)")
            if sample_files:
                lines.append(f"    sample: {', '.join(sample_files)}")
    lines.append(
        "You may READ any file or directory under the project root. Use SEARCH: to discover additional paths before making claims."
    )
    return "\n".join(lines)


def _build_workspace_access_note(cwd: Path, max_files: int = 40) -> str:
    """Explain the workspace root and provide verified starting paths."""
    listing = _get_project_file_listing(cwd, max_files=max_files)
    examples = _sample_workspace_paths(cwd, max_files=3)
    example_lines = "\n".join(f"READ: {path}" for path in examples)
    if not example_lines:
        example_lines = "SEARCH: *.py"
    return (
        f"Project root: {cwd}\n"
        "You may READ any file or directory inside this root and any child directory under it.\n"
        "Use the verified paths below to start exploring; if you need more files, use SEARCH: first.\n"
        "For bash-based discovery on read-only tasks, prefer safe RUN: commands like:\n"
        "RUN: ls -laR | head -200\n"
        "RUN: find . -maxdepth 2 -type d | head -80\n"
        "RUN: rg --files . | head -120\n"
        f"{listing}\n\n"
        f"Example valid start:\n{example_lines}"
    )


def _build_tool_format_recovery_prompt(cwd: Path) -> str:
    """Build a dynamic tool-format recovery prompt using real workspace paths."""
    return (
        "Your previous response was REJECTED. You MUST fix this NOW.\n\n"
        "CRITICAL RULES:\n"
        "1. Start your response with READ: or SEARCH: commands IMMEDIATELY\n"
        "2. Do NOT list what you will do - just DO IT\n"
        "3. Do NOT generate numbered lists until AFTER you have read files\n"
        "4. Do NOT fabricate content - READ files first, then analyze\n\n"
        f"{_build_workspace_access_note(cwd, max_files=25)}\n\n"
        "WRONG (WILL BE REJECTED AGAIN):\n"
        '- "I will read..." ❌\n'
        '- "Let me analyze..." ❌\n'
        '- "1. Issue A, 2. Issue B..." without reading files first ❌\n'
        "- Plans or explanations before executing tools ❌\n\n"
        "START YOUR RESPONSE WITH: READ: <actual_file_path>"
    )


def _build_multistep_phase_prompts(
    task_prompt: str,
    classification: _ClassifiedRequest | None = None,
    cwd: Path | None = None,
) -> list[tuple[str, str]]:
    """Build phase prompts so the model owns planning and task reasoning."""
    from sage.cli_core import _get_current_classification
    effective_classification = classification or _get_current_classification()

    # Informational tasks get a direct, two-phase research and response path (P3-71)
    if effective_classification and effective_classification.is_informational:
        return [
            (
                "analysis",
                (
                    f"## INFORMATIONAL RESEARCH\n"
                    f"TASK: {task_prompt}\n\n"
                    "Gather key facts and information about this topic from your internal knowledge. "
                    "Focus on accuracy and providing a comprehensive overview. "
                    "Do NOT use codebase tools (READ:, SEARCH:, RUN:, FILE:)."
                ),
            ),
            (
                "synthesis",
                (
                    f"## INFORMATIONAL RESPONSE\n"
                    f"TASK: {task_prompt}\n\n"
                    "Now provide the final, detailed answer to the user. "
                    "Incorporate the findings you just gathered to provide a well-structured response. "
                    "Do NOT use codebase tools."
                ),
            ),
        ]

    # Get actual file listing for discovery (prevents model from guessing filenames)
    file_listing = ""
    if cwd:
        file_listing = _get_project_file_listing(cwd)

    if effective_classification and effective_classification.read_only:
        quantity_instruction = ""
        if effective_classification.quantity_required:
            quantity_instruction = (
                f" Target at least {effective_classification.quantity_required} distinct items"
                " if the user asked for a long ranked list."
            )

        return [
            (
                "planning",
                (
                    f"# VERIFIED WORKSPACE ACCESS\n"
                    f"{_build_workspace_access_note(cwd, max_files=40) if cwd else file_listing}\n\n"
                    "⚠️ CRITICAL: Do NOT guess conventional paths like 'src/main.py' if you have not "
                    "verified them. Start from real paths in this workspace and use SEARCH: to discover more.\n\n"
                    f"TASK: {task_prompt}\n\n"
                    f"START YOUR RESPONSE WITH READ: COMMANDS IMMEDIATELY.\n"
                    f"No preamble. No 'I will read'. Just output the READ: commands.\n\n"
                    f"Example correct start:\n"
                    f"{chr(10).join(f'READ: {path}' for path in _sample_workspace_paths(cwd, 2)) if cwd and _sample_workspace_paths(cwd, 2) else 'SEARCH: *.py'}\n\n"
                    "For repo-wide discovery, safe bash inventory commands like RUN: ls -laR | head -200, "
                    "RUN: find . -maxdepth 2 -type d | head -80, and RUN: rg --files . | head -120 are encouraged.\n\n"
                    "After reading files, provide a brief analysis plan (2-4 steps). "
                    "Do NOT write code, tests, or FILE: blocks."
                ),
            ),
            (
                "analysis",
                (
                    f"TASK: {task_prompt}\n\n"
                    "Continue the read-only investigation. Use READ:, SEARCH:, and safe RUN: "
                    "commands if needed to gather evidence. READ files, not directories. "
                    "Use one SEARCH pattern per line instead of combining terms with OR on a single line. "
                    "Focus on root causes, risks, and "
                    "priority." + quantity_instruction + " Do NOT write code or tests."
                ),
            ),
            (
                "synthesis",
                (
                    f"TASK: {task_prompt}\n\n"
                    "Now synthesize the final analysis. Produce a grounded, prioritized response "
                    "based on the evidence you gathered. "
                    "Format the final answer as a numbered findings list, with one primary issue "
                    "per numbered item. "
                    "Use this structure for each item: title, `Evidence:`, `Impact:`, then `Recommendation:`. "
                    "Reference only files or code locations that were explicitly verified during your investigation. "
                    "Include line numbers when they are available from verified evidence, but do not invent them. "
                    "If the user asked for a long list, number every item clearly and do not stop early. "
                    "If evidence is insufficient for some claims, say so plainly instead of guessing. "
                    "Do NOT write code, tests, or writable file blocks."
                ),
            ),
        ]

    # ── Greenfield / large-scope detection ──────────────────────────────────
    # For new full-project scaffolds the 4-phase TDD pipeline is wrong:
    #   1. planning → nothing to read in an empty directory
    #   2. analysis → "don't write code yet" wastes context tokens
    #   3. testing  → writes tests that import non-existent modules → immediate failures
    #   4. implementation → context window is crowded; model produces prose, not 500 files
    #
    # Instead: 2 phases — plan the structure, then scaffold EVERYTHING (config +
    # implementation + tests) in one response.  Tests are written LAST so every
    # module they import already exists in the same response.
    _greenfield_signals = [
        "full platform", "full project", "full app", "full stack",
        "from scratch", "brand new", "new platform", "new project",
        "new application", "build a ", "create a ", "entire platform",
        "entire project", "entire application", "end-to-end",
        "monorepo", "all features", "complete platform",
    ]
    task_lower = task_prompt.lower()
    _listing = _get_project_file_listing(cwd, max_files=1) if cwd else ""
    _is_workspace_empty = not _listing
    _is_greenfield = (
        sum(1 for s in _greenfield_signals if s in task_lower) >= 1
        or len(task_prompt) > 600
        or _is_workspace_empty
    )

    if _is_greenfield:
        workspace_note = (
            f"# WORKSPACE\n{_build_workspace_access_note(cwd, max_files=20)}\n\n"
            if cwd else ""
        )
        return [
            (
                "planning",
                (
                    f"TASK: {task_prompt}\n\n"
                    "⚠️ THIS IS A BRAND-NEW GREENFIELD PROJECT. The workspace is EMPTY.\n"
                    "Do NOT issue READ:, SEARCH:, or RUN: commands — there is NOTHING to explore.\n\n"
                    "Your ONLY job: output a FILE_MANIFEST listing EVERY file to be created for the project.\n\n"
                    "Provide a clean, logical project layout suitable for this task.\n"
                    "In your response, define the structure, then output FILE_MANIFEST: followed by a list of relative file paths (one path per line) for all configuration, source code, and test files required for a complete, production-ready, fully working implementation.\n\n"
                    "CRITICAL RULES:\n"
                    "- Only include files that you will implement. Do not include files you won't write.\n"
                    "- Every file in the manifest must be written completely with no placeholders or TODOs.\n"
                    "- Output FILE_MANIFEST: one path per line. No code. No READ:/SEARCH:. ONLY the list."
                ),
            ),
            (
                "implementation",
                (
                    f"TASK: {task_prompt}\n\n"
                    "Now write the FIRST BATCH of files using FILE: blocks.\n\n"
                    "Output complete file contents with NO placeholders, NO stubs, and NO '// TODO' comments.\n"
                    "Start with the configuration/manifest files and core database/utility files first, and continue until all files are fully written."
                ),
            ),
        ]

    return [
        (
            "planning",
            (
                f"# VERIFIED WORKSPACE ACCESS\n"
                f"{_build_workspace_access_note(cwd, max_files=40) if cwd else file_listing}\n\n"
                "⚠️ IMPORTANT: Start from verified paths in this workspace. "
                "If you need more files under the current root, use SEARCH: first instead of guessing names.\n\n"
                f"TASK: {task_prompt}\n\n"
                "Break this into 2-4 concrete implementation steps. "
                "For each step, say what file(s) to create/modify. "
                "Use READ: commands to examine any existing files you need to understand first.\n"
                "Format:\n"
                "STEP 1: <description> — <file(s)>\n"
                "STEP 2: <description> — <file(s)>\n"
                "...\n\n"
                "START with READ: commands to explore the codebase. Example:\n"
                + (
                    "\n".join(f"READ: {path}" for path in _sample_workspace_paths(cwd, 2))
                    if cwd and _sample_workspace_paths(cwd, 2)
                    else "SEARCH: *.py"
                )
            ),
        ),
        (
            "analysis",
            (
                f"TASK: {task_prompt}\n\n"
                "Before writing tests or code, analyze the relevant files you just read. "
                "Identify the exact lines to change and the logic required. "
                "Use READ:, SEARCH:, and RUN: commands if you need more context. "
                "Focus on understanding the root cause and edge cases. "
                "Do NOT write code or tests yet."
            ),
        ),
        (
            "testing",
            (
                "Now write the TEST files for this task. Based on your plan and analysis above, "
                "create test files that verify the expected behavior.\n\n"
                "⚠️ IMPORTANT: Ensure your tests cover the specific issues identified in previous analysis. "
                "Tests should fail without the fix and pass with it (TDD).\n\n"
                "RULES:\n"
                "- Output ONLY test files using FILE: blocks\n"
                "- Import from modules that ACTUALLY EXIST in this project\n"
                "- Each test should be runnable independently\n"
                "- Do NOT write implementation files yet — only tests\n"
            ),
        ),
        (
            "implementation",
            (
                "Now write the IMPLEMENTATION files to make the tests pass. "
                "Based on your plan and the tests you wrote, create/modify the source files.\n\n"
                "⚠️ CRITICAL: You MUST write REAL, functional code. No placeholders, no TODOs, "
                "no partial implementations, and no simulated logic (unless it's a stub for a missing external service).\n"
                "If you are fixing issues found during analysis, ensure your code explicitly addresses "
                "the root causes identified.\n\n"
                "RULES:\n"
                "- Output implementation files using FILE: blocks with COMPLETE contents\n"
                "- Make sure imports match what exists in the project\n"
                "- Do NOT rewrite the test files — only implementation files\n"
                "- Use RUN: to run the tests after writing the files\n"
            ),
        ),
    ]


def _build_tool_followup_prompt(
    tool_context: str,
    classification: _ClassifiedRequest | None = None,
    cwd: Path | None = None,
) -> str:
    """Build a mode-aware follow-up prompt after READ/SEARCH/RUN commands."""
    from sage.cli_core import _get_current_classification, _get_current_task_prompt, _tool_context_needs_more_investigation
    effective_classification = classification or _get_current_classification()

    if effective_classification and effective_classification.read_only:
        if _tool_context_needs_more_investigation(tool_context):
            workspace_note = ""
            if cwd is not None:
                workspace_note = "\n\n" + _build_workspace_access_note(cwd, max_files=30)
            return (
                f"Here are the results of your tool commands:\n\n{tool_context}\n\n"
                "Your previous investigation commands did not produce enough grounded evidence yet. "
                "Issue corrected READ:/SEARCH:/RUN: commands before making substantive claims.\n"
                "Rules:\n"
                "1. READ files, not directories.\n"
                "2. Use one SEARCH pattern per line; do not combine terms with OR on a single line.\n"
                "3. If a tool failed or returned no matches, acknowledge that and correct the command.\n"
                "4. Do not claim facts unless they are explicitly supported by the tool results above.\n"
                "5. If evidence remains insufficient after another pass, say so plainly instead of guessing."
                f"{workspace_note}"
            )

        quantity_instruction = ""
        if effective_classification.quantity_required:
            quantity_instruction = (
                f" Provide at least {effective_classification.quantity_required} distinct items"
                " if the request asked for a long ranked list."
            )

        return (
            f"Here are the results of your tool commands:\n\n{tool_context}\n\n"
            "Now continue with your analysis. Synthesize concrete, evidence-based findings from "
            "these results."
            f"{quantity_instruction} "
            "Only claim facts explicitly supported by the tool results above. "
            "If evidence is incomplete, say so and issue more specific READ:/SEARCH: commands instead of guessing. "
            "Do NOT write writable file blocks, code, tests, or implementation steps unless the user "
            "explicitly asked for code changes."
        )

    # Detect simple update/replacement tasks that don't need TDD
    task_prompt_lower = (_get_current_task_prompt() or "").lower()
    is_simple_update = any(kw in task_prompt_lower for kw in (
        "update", "replace", "rename", "change the", "switch", "swap", "upgrade",
        "domain", "url", "variable", "config", "constant", "string",
    )) and not any(kw in task_prompt_lower for kw in (
        "feature", "function", "class", "implement", "add", "build", "create",
    ))

    if is_simple_update:
        return (
            f"Here are the results of your tool commands:\n\n{tool_context}\n\n"
            "Now apply the change.\n"
            "You have the exact file contents from the tool results above.\n"
            "Output FILE: blocks with the complete updated file contents.\n"
            "Do NOT write tests for simple string/config replacements.\n"
            "Do NOT ask for confirmation — just make the change.\n"
        )

    # Detect greenfield so we don't re-inject TDD instructions mid-scaffold
    _task_lower = (_get_current_task_prompt() or "").lower()
    _greenfield_kws = [
        "full platform", "full project", "full app", "full stack", "from scratch",
        "brand new", "new platform", "new project", "monorepo", "entire platform",
        "entire project", "end-to-end", "all features", "complete platform",
        "build a ", "create a ",
    ]
    _is_greenfield_followup = (
        sum(1 for k in _greenfield_kws if k in _task_lower) >= 1
        or len(_task_lower) > 600
        or (cwd is not None and not _get_project_file_listing(cwd, max_files=15))
    )

    if _is_greenfield_followup:
        return (
            f"Here are the results of your tool commands:\n\n{tool_context}\n\n"
            "Continue scaffolding the project. Output the next batch of FILE: blocks.\n"
            "RULES:\n"
            "- Config and implementation files BEFORE any test files\n"
            "- Test files only after all modules they import are already written\n"
            "- Every FILE: block must contain COMPLETE file contents — no stubs\n"
            "- Do NOT re-explain the architecture — just output FILE: blocks\n"
        )

    return (
        f"Here are the results of your tool commands:\n\n{tool_context}\n\n"
        "Now continue with your implementation.\n"
        "You already have real workspace evidence from the tool results above.\n"
        "Do NOT ask the user to provide file contents, outputs, or confirmation.\n"
        "If this task involves new logic or changed behavior:\n"
        "1. Write the implementation FILE: blocks first.\n"
        "2. Write tests that import from the implementation you just wrote.\n"
        "3. Use RUN: commands for the relevant tests.\n"
        "4. Do NOT answer with prose-only plans or assumptions.\n"
        "For simple updates (config, strings, domain changes), just output FILE: blocks directly.\n"
    )


def _wants_code_changes(lower: str) -> bool:
    """Heuristic: user wants implementation, patches, or explicit fixes (not review-only)."""
    if re.search(
        r"\b(no code|don't write code|analysis only|read[- ]only|do not implement)\b",
        lower,
    ):
        return False
    if re.search(
        r"\b(and|then)\s+(fix|implement|refactor|patch|change|update)\b",
        lower,
    ):
        return True
    if re.search(r"\bfix\s+(this|that|the|it|bugs?|dockerfile)\b", lower):
        return True
    if re.search(r"\b(implement|refactor|patch)\b", lower):
        return True
    if re.search(
        r"\b(write|add|create|change|update)\s+(a\s+|the\s+|this\s+|those\s+)?(feature|function|class|file|tests?)\b",
        lower,
    ):
        return True
    return False


def _is_credential_bootstrap_request(prompt: str) -> bool:
    """True when the task likely needs real secret or service bootstrap work."""
    lower = prompt.lower()
    triggers = (
        "secret",
        "credential",
        "api key",
        "token",
        ".env",
        "environment variable",
        "env var",
        "database url",
        "database",
        "postgres",
        "sqlite",
        "redis",
        "auth",
        "deploy",
        "deployment",
        "cloud",
        "gcloud",
        "gcp",
        "aws",
        "azure",
        "cloudflare",
        "vercel",
        "railway",
        "render",
        "fly.io",
        "fly ",
    )
    return any(trigger in lower for trigger in triggers)


_CLOUD_PROVIDER_DISPLAY_NAMES: dict[str, str] = {
    "gcp": "Google Cloud",
    "aws": "AWS",
    "azure": "Azure",
    "cloudflare": "Cloudflare",
    "vercel": "Vercel",
    "railway": "Railway",
    "render": "Render",
    "flyio": "Fly.io",
}


def _is_cloud_deployment_request(prompt: str) -> bool:
    """True when the request is about hosting or deploying to a cloud target."""
    lower = prompt.lower()
    return any(
        trigger in lower
        for trigger in (
            "deploy",
            "deployment",
            "ship it",
            "push to prod",
            "production",
            "hosting",
            "host this",
            "publish",
            "release",
            "cloud run",
            "aws",
            "gcloud",
            "gcp",
            "azure",
            "vercel",
            "railway",
            "render",
            "fly.io",
            "cloudflare",
        )
    )


def _build_cloud_provider_prompt() -> str:
    """Prompt shown when SAGE needs the user's preferred deployment target."""
    return (
        "[cyan]Preferred cloud provider for this deployment "
        "[gcp/aws/azure/cloudflare/vercel/railway/render/fly/blank to skip]: [/cyan]"
    )


def _resolve_cloud_provider_preference(
    prompt: str,
    cfg: SageConfig | None = None,
    *,
    prompt_user: Callable[[str], str] | None = None,
) -> str:
    """Resolve the target cloud provider from the request, config, or user input."""
    requested = _detect_target_cloud_provider(prompt)
    if requested:
        return requested

    saved_preference = _normalize_cloud_provider(getattr(cfg, "preferred_cloud", "") or "")
    if saved_preference:
        return saved_preference

    if not _is_cloud_deployment_request(prompt) or prompt_user is None:
        return ""

    raw_answer = prompt_user(_build_cloud_provider_prompt()).strip()
    provider = _normalize_cloud_provider(raw_answer)
    if not provider:
        return ""

    if cfg is not None and getattr(cfg, "preferred_cloud", "") != provider:
        cfg.preferred_cloud = provider
        try:
            save_config(cfg)
        except Exception as exc:
            logger.warning("Could not persist preferred cloud provider %s: %s", provider, exc)
        else:
            renderer.info(
                f"Saved preferred cloud provider: "
                f"{_CLOUD_PROVIDER_DISPLAY_NAMES.get(provider, provider)}"
            )
    return provider


def _build_cloud_deployment_context(prompt: str, cloud_provider: str = "") -> str:
    """Return deployment guidance that is specific to the chosen cloud target."""
    if not _is_cloud_deployment_request(prompt):
        return ""

    provider = _normalize_cloud_provider(cloud_provider)
    if not provider:
        return (
            "## CLOUD DEPLOYMENT TARGET\n"
            "No cloud provider has been confirmed yet.\n"
            "Before you write provider-specific deployment files or commands, ask the user which cloud they want "
            "(for example: gcp/gcloud, aws, azure, cloudflare, vercel, railway, render, or fly).\n"
            "Do NOT guess a cloud vendor and do NOT mix multiple providers in one deployment plan.\n"
        )

    label = _CLOUD_PROVIDER_DISPLAY_NAMES.get(provider, provider)
    return (
        "## CONFIRMED CLOUD DEPLOYMENT TARGET\n"
        f"Target provider: {label}\n"
        "Act as a senior cloud deployment engineer for this provider only.\n"
        "Use the provider's native deployment services, IAM/auth model, regions, secrets handling, networking, "
        "managed databases, observability, rollback, and cost-safe defaults.\n"
        "Do NOT mix guidance, file formats, CLIs, or services from other clouds unless the user explicitly asks for multi-cloud.\n"
    )


def _response_asks_for_cloud_provider(response: str) -> bool:
    """Return True when the model is explicitly asking the user to choose a cloud."""
    lower = response.lower()
    question_markers = (
        "which cloud",
        "what cloud",
        "preferred cloud provider",
        "choose a cloud provider",
        "which provider",
        "do you want this on aws",
        "do you want this on gcp",
        "do you want this on azure",
        "gcp or aws",
        "aws or gcp",
    )
    return "?" in response and any(marker in lower for marker in question_markers)


def _response_commits_to_cloud_provider(response: str) -> str:
    """Detect when a response has committed to a specific cloud deployment target."""
    provider = _detect_target_cloud_provider(response)
    if provider:
        return provider

    provider_patterns: dict[str, tuple[str, ...]] = {
        "gcp": (r"cloudbuild\.ya?ml", r"\bgcloud\b", r"cloud run", r"app\.ya?ml"),
        "aws": (r"\baws\b", r"\becs\b", r"cloudformation", r"apprunner", r"lambda"),
        "azure": (r"\baz\b", r"azure", r"\bbicep\b", r"azurewebsites\.net"),
        "cloudflare": (r"wrangler\.toml", r"cloudflare", r"\bworkers\b"),
        "vercel": (r"vercel\.json", r"\bvercel\b"),
        "railway": (r"railway\.json", r"\brailway\b"),
        "render": (r"render\.ya?ml", r"\brender\b"),
        "flyio": (r"fly\.toml", r"fly\.io", r"\bflyctl\b"),
    }
    for provider_name, patterns in provider_patterns.items():
        if any(re.search(pattern, response, re.IGNORECASE) for pattern in patterns):
            return provider_name
    return ""


def _build_credential_bootstrap_context(
    cwd: Path,
    prompt: str,
    cfg: SageConfig | None = None,
    *,
    preferred_cloud: str = "",
) -> str:
    """Bootstrap `.env` files securely and return a prompt-safe summary."""
    if not _is_credential_bootstrap_request(prompt):
        return ""

    project_root = _default_project_root(cwd)
    config_api_keys = (cfg.api_keys if cfg else {}) or {}

    try:
        result = _bootstrap_project_credentials(
            project_root,
            request_text=prompt,
            config_api_keys=config_api_keys,
            preferred_cloud=preferred_cloud,
        )
    except Exception as exc:
        logger.warning("Credential bootstrap failed for %s: %s", project_root, exc)
        return (
            "## SECURE CREDENTIAL BOOTSTRAP\n"
            "SAGE could not safely bootstrap credentials automatically for this request.\n"
            "Do NOT invent any secret values. Wire env loading correctly and report the exact missing variables instead.\n"
        )

    return result.prompt_summary()


def _is_readonly_analysis_request(user_input: str) -> bool:
    """True for audit / review / prioritized findings without edits or execution."""
    lower = user_input.lower().strip()
    if _wants_code_changes(lower):
        return False
    analysis_markers = (
        "analyze",
        "review",
        "audit",
        "assess",
        "what needs",
        "what's wrong",
        "what is wrong",
        "priorit",
        "list ",
        "recommendations",
        "suggestions",
        "code review",
        "strengths",
        "weaknesses",
        "gaps",
        "areas for improvement",
    )
    return any(m in lower for m in analysis_markers)


def _expand_prompt(user_input: str) -> str:
    """Expand user prompts with detailed instructions for the model.

    Detects the type of request and adds specific guidance so that smaller
    models can produce high-quality results comparable to larger models.
    """
    from sage.cli_core import _get_current_classification
    lower = user_input.lower().strip()

    # ── Multi-item fix / "fix all" requests → task-list workflow ─────────────
    # Checked BEFORE read-only analysis so "address all items in the list" is
    # not mistakenly classified as analysis due to the word "list".
    multi_fix_triggers = [
        "fix all",
        "fix each",
        "fix every",
        "fix these",
        "fix those",
        "address all",
        "address each",
        "address these",
        "resolve all",
        "resolve each",
        "resolve these",
        "implement all",
        "implement each",
        "implement these",
        "apply all",
        "all of these",
        "every item",
        "every point",
        "all the points",
        "all the items",
        "all points",
        "all items",
    ]
    for trigger in multi_fix_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS — TASK-LIST WORKFLOW (MANDATORY):\n"
                "You have multiple items to fix. You MUST follow this workflow:\n\n"
                "## STEP 1: Build a numbered task list\n"
                "List every distinct task derived from the request, numbered 1..N.\n"
                "For each, state: one-line description, file(s) involved, status [PENDING].\n"
                "Print the full task list before starting any work.\n\n"
                "## STEP 2: Execute tasks ONE AT A TIME, in order\n"
                "For each task:\n"
                "  a) Print: '--- Task K/N: <description> [IN PROGRESS] ---'\n"
                "  b) READ: every file you plan to modify (MANDATORY — never guess file contents)\n"
                "  c) Write the fix/implementation using FILE: blocks with COMPLETE contents\n"
                "  d) Write or update tests (FILE: tests/...) if the change involves code logic\n"
                "  e) RUN: the relevant test/validation command\n"
                "  f) If the test fails, debug and retry before moving to the next task\n"
                "  g) Print: '--- Task K/N: <description> [DONE] ---'\n\n"
                "## STEP 3: Final summary\n"
                "After all tasks, print the full task list with updated statuses:\n"
                "  [DONE], [FAILED], or [SKIPPED] for each.\n"
                "Report how many passed, failed, or were skipped.\n\n"
                "## HARD RULES\n"
                "- Do NOT skip tasks or stop early. Complete EVERY item.\n"
                "- READ: files BEFORE modifying them — never hallucinate file contents.\n"
                "- If a task fails after 3 retries, mark it [FAILED] and move to the next.\n"
                "- Do NOT run destructive commands (docker build, training, deploy) unless the task specifically requires it.\n"
            )

    # ── Read-only analysis / review (no unsolicited code, tests, or builds) ──
    # Use the current classification for better enforcement
    classification = _get_current_classification()

    if classification and classification.read_only:
        # Build enforcement instructions based on classification
        quantity_instruction = ""
        if classification.quantity_required:
            qty = classification.quantity_required
            quantity_instruction = (
                f"\n## QUANTITY REQUIREMENT (MANDATORY)\n"
                f"You MUST provide AT LEAST {qty} distinct items in your response.\n"
                f"If you cannot find {qty} items, provide as many as you can with clear justification.\n"
                f"DO NOT stop at 3-5 items when the user asked for {qty}+.\n"
                f"Number each item clearly: 1., 2., 3., ... up to {qty}+.\n"
            )

        return (
            f"{user_input}\n\n"
            "## CRITICAL: READ-ONLY ANALYSIS MODE\n"
            "This request is classified as READ-ONLY ANALYSIS. You MUST:\n"
            "1. NEVER write FILE: blocks — they will be REJECTED by the system.\n"
            "2. NEVER create tests, patches, or implementation code.\n"
            "3. NEVER run destructive commands (docker build, training, deploys).\n"
            "4. Use READ:/SEARCH: to explore the codebase BEFORE making claims.\n"
            "5. Reference ONLY files that you have verified exist via SEARCH: or READ:.\n"
            "6. Include concrete file paths, and line numbers only when verified evidence gives them to you.\n"
            f"{quantity_instruction}\n"
            "## OUTPUT FORMAT\n"
            "Provide a prioritized list with:\n"
            "- Severity (P0/P1/P2/P3)\n"
            "- File path, plus a line number when you have one from verified evidence\n"
            "- Specific issue description\n"
            "- Concrete recommendation\n"
            "- Estimated effort (optional)\n\n"
            "You may offer implementation help after the findings list, but do NOT start implementing unprompted.\n"
            "DO NOT start implementing unprompted."
        )

    # Fallback to old logic if no classification
    if _is_readonly_analysis_request(user_input):
        return (
            f"{user_input}\n\n"
            "INSTRUCTIONS (read-only analysis mode):\n"
            "1. Answer from the project context already provided. Do NOT write or modify code.\n"
            "2. Do NOT create tests, patches, or FILE: blocks unless the user explicitly asked you to implement or fix something.\n"
            "3. Do NOT run docker, training, builds, deploys, or other destructive/slow commands.\n"
            "4. Use READ:/SEARCH: only if you must verify a specific claim against the repo; prefer the supplied context.\n"
            "5. Deliver a prioritized list: severity, blast radius, concrete recommendation, and file paths to inspect.\n"
            "6. If something requires reading files you do not have, say what you would read — do not invent file contents.\n"
            "7. End by asking whether the user wants implementation help next — do not start implementing unprompted."
        )

    # ── Vague improvement / fix requests (implementation-oriented) ─────────────
    vague_impl_triggers = [
        "improve this",
        "improve the code",
        "make it better",
        "refactor this",
        "refactor the code",
        "fix this",
        "fix the code",
        "fix bugs",
        "what can be improved",
        "look at this",
        "check this",
    ]
    for trigger in vague_impl_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS: You have the full codebase. Follow these steps:\n"
                "1. Identify the most impactful issues first: blockers, security risks, failing tests, CI/release gaps, then reliability/code quality\n"
                "2. Prioritize by severity and blast radius, not convenience or cosmetics\n"
                "3. READ: every file you plan to modify BEFORE writing changes (MANDATORY)\n"
                "4. For each fix, write or update tests that expose the issue (FILE: tests/test_improvement_N.py)\n"
                "5. Write the fix (FILE: path/to/fixed_file.py)\n"
                "6. Include ```bash blocks to run the relevant validation\n"
                "Reference specific files and line numbers from the project context."
            )

    # ── Deployment requests ────────────────────────────────
    deploy_triggers = [
        "deploy",
        "deployment",
        "ship it",
        "push to prod",
        "production",
        "hosting",
        "publish",
        "release",
    ]
    for trigger in deploy_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS: Create a complete deployment setup:\n"
                "1. Detect the tech stack from the project files\n"
                "2. If the user has not specified a cloud provider, ask them to choose one before writing provider-specific deployment files\n"
                "3. Write a Dockerfile if the project doesn't have one\n"
                "4. Write a deployment config for the confirmed provider only (for example: Cloud Run, ECS/App Runner, Azure App Service, Fly.io, Vercel, Railway, Render)\n"
                "5. Add pre-deploy validation, health checks, logs, and rollback steps\n"
                "6. Write a deploy script (scripts/deploy.sh) that automates the process with the provider's official CLI/IaC flow\n"
                "7. Reuse the real `.env` SAGE bootstrapped outside the model; do NOT invent keys or passwords\n"
                "8. Create or update `.env.example` with the same variable names but blank/redacted values only\n"
                "9. Update .gitignore to exclude .env and other sensitive files\n"
                "10. If the app needs a database/cache/service, create the concrete service config and wire it to the existing env vars\n"
                "11. Stay provider-native: do NOT mix AWS/GCP/Azure/Vercel/etc. patterns in the same deployment plan unless the user asked for multi-cloud\n"
                "12. Include ```bash blocks to validate the deployment locally and with the provider CLI\n"
                "Use FILE: blocks for every file."
            )

    # ── CI/CD requests ─────────────────────────────────────
    ci_triggers = [
        "ci/cd",
        "ci cd",
        "pipeline",
        "github action",
        "gitlab ci",
        "continuous",
    ]
    for trigger in ci_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS: Create a CI/CD pipeline:\n"
                "1. Detect the tech stack and test framework\n"
                "2. Write .github/workflows/ci.yml (or equivalent) with fail-fast lint, test, and build stages\n"
                "3. Cache dependencies when the platform supports it\n"
                "4. Block merges when validation fails\n"
                "5. Add a deployment stage only after validation passes if requested\n"
                "6. Create any missing test scripts\n"
                "Use FILE: blocks for every file."
            )

    # ── Secret/env management ──────────────────────────────
    secret_triggers = [
        "secret",
        "env var",
        "environment variable",
        "api key",
        "credential",
        ".env",
    ]
    for trigger in secret_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS: Set up secure configuration with real credential handling:\n"
                "1. Reuse the real `.env` file SAGE bootstrapped outside the model; do NOT invent or print secret values\n"
                "2. Create or update `.env.example` with the same variable names but blank/redacted values only\n"
                "3. Write a config loader that reads from env vars, prefers `.env` for local runs, and fails clearly for missing external credentials\n"
                "4. If the app needs a local database/cache/service, create the concrete service config and wire it to the env vars already in `.env`\n"
                "5. Add `.env` and `.env.local` to .gitignore\n"
                "6. Write tests for the config loader and service bootstrap\n"
                "7. NEVER fabricate third-party API keys; if one is still missing, report the exact env var and acquisition URL\n"
                "NEVER put real secrets in code. Use FILE: blocks for every file."
            )

    # ── Docker requests ────────────────────────────────────
    docker_triggers = ["docker", "container", "containerize"]
    for trigger in docker_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS: Create Docker setup:\n"
                "1. Write a Dockerfile optimized for the project's tech stack\n"
                "2. Write docker-compose.yml if the app has services (db, cache, etc.)\n"
                "3. Write .dockerignore\n"
                "4. Include ```bash blocks to build and test the image\n"
                "Use FILE: blocks for every file."
            )

    # ── Database requests ──────────────────────────────────
    db_triggers = ["database", "migration", "schema", "sql", "orm", "model"]
    for trigger in db_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS:\n"
                "1. Check what database/ORM the project uses\n"
                "2. Reuse the real `.env` SAGE bootstrapped for database credentials/URLs; do NOT invent fake DSNs\n"
                "3. If the project needs a local DB service, create the concrete service config (or a real SQLite setup) and wire it to `.env`\n"
                "4. Write migration files if needed\n"
                "5. Write model/schema code\n"
                "6. Write tests with a real test database configuration\n"
                "7. Include ```bash blocks to run migrations and tests\n"
                "Use FILE: blocks for every file."
            )

    # ── Testing requests ───────────────────────────────────
    test_triggers = [
        "write test",
        "add test",
        "test coverage",
        "unit test",
        "integration test",
    ]
    for trigger in test_triggers:
        if trigger in lower:
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS:\n"
                "1. Identify what needs testing from the project files\n"
                "2. Write comprehensive tests covering: happy path, edge cases, error cases\n"
                "3. Include ```bash blocks to run the tests\n"
                "Use FILE: blocks for every test file."
            )

    # ── Build/create from scratch ──────────────────────────
    # Detect large greenfield requests (new full platforms / apps) by looking for
    # multiple major components described in the prompt.  For these we must NOT
    # write tests-first — the implementation doesn't exist yet so any test that
    # imports from it will immediately fail with ModuleNotFoundError, triggering
    # an infinite fix loop.  Instead we scaffold everything together in one pass.
    _greenfield_signals = [
        "full platform", "full project", "full app", "full stack",
        "from scratch", "brand new", "new platform", "new project",
        "new application", "build a", "create a", "entire platform",
        "entire project", "entire application", "end-to-end",
        "monorepo", "all features", "complete platform",
    ]
    _large_scope = sum(
        1 for s in _greenfield_signals if s in lower
    ) >= 1 or len(lower) > 600  # very long prompt = multi-component request
    build_triggers = [
        "create",
        "build",
        "make",
        "add",
        "implement",
        "write",
        "set up",
        "setup",
    ]
    for trigger in build_triggers:
        if trigger in lower and len(lower) > len(trigger) + 5:  # Only if there's substance
            if _large_scope:
                return (
                    f"{user_input}\n\n"
                    "INSTRUCTIONS — FULL PROJECT SCAFFOLD (do NOT write tests before implementation):\n"
                    "1. List every component / layer that needs to be built.\n"
                    "2. Output ALL files in a single response using FILE: blocks:\n"
                    "   a. Project config files first (package.json, pyproject.toml, Dockerfile, etc.)\n"
                    "   b. Implementation files (complete, working code — not stubs)\n"
                    "   c. Test files LAST, after every module they import already exists\n"
                    "3. Every FILE: block must contain COMPLETE file contents — no '# TODO', no placeholders.\n"
                    "4. Tests must only import modules that are also output in this same response.\n"
                    "5. Include a ```bash block at the end to install deps and run the full test suite.\n"
                    "CRITICAL: Never write tests that import a module you haven't also written in this response."
                )
            return (
                f"{user_input}\n\n"
                "INSTRUCTIONS: Think step by step:\n"
                "1. What exactly needs to be built? List the components.\n"
                "2. What existing code can you build on? Check the project files.\n"
                "3. Write the implementation files first (complete, working code)\n"
                "4. Write tests that import from the implementation files you just wrote\n"
                "5. Include ```bash blocks to verify everything works\n"
                "Use FILE: blocks for every file.\n"
                "CRITICAL: Tests must only import modules that exist in the project or that you are also writing."
            )

    return user_input


def _ai_understand_prompt(
    raw_input: str,
    cwd: Path,
    send_fn: Callable[[str], str | None],
) -> str:
    """Use the AI model to understand and expand a vague user prompt.

    Performs a single hidden turn:
    - Corrects spelling/grammar
    - Identifies true intent from brief/ambiguous input
    - Gathers codebase context (file tree, recent changes) automatically
    - Produces a clear, actionable task description for the coding agent

    Returns the expanded prompt, or the original if anything fails.
    The result is never shown to the user directly — it becomes the task
    that the agent works from.
    """
    # Skip enhancement for already-detailed prompts (> 40 words)
    if len(raw_input.split()) > 40:
        return raw_input

    # Build a lightweight codebase snapshot for context
    try:
        # Top-level structure
        ls_out = _run_shell(r"find . -maxdepth 3 -type f | grep -v '__pycache__\|.git\|node_modules\|.gguf\|.pyc' | head -80", cwd, timeout=5)
        # Recent git changes (what's been worked on)
        git_recent = _run_shell("git log --oneline -8 2>/dev/null || echo 'no git'", cwd, timeout=5)
        # Active file count by type
        type_summary = _run_shell(
            r"find . -maxdepth 4 -type f | grep -oE '\.[^./]+$' | sort | uniq -c | sort -rn | head -15 2>/dev/null",
            cwd, timeout=5
        )
        codebase_snapshot = (
            f"Project file tree (sample):\n{ls_out[:1500]}\n\n"
            f"Recent commits:\n{git_recent}\n\n"
            f"File types:\n{type_summary}"
        ).strip()
    except Exception:
        codebase_snapshot = "(codebase context unavailable)"

    meta_prompt = (
        "You are a task clarification system for SAGE, an autonomous coding agent.\n\n"
        f"The user typed: \"{raw_input}\"\n\n"
        f"Codebase context:\n{codebase_snapshot}\n\n"
        "Your job:\n"
        "1. Fix any spelling or grammar errors in the user's request\n"
        "2. Understand what the user truly wants, even from very brief or vague input\n"
        "3. Infer the relevant files, components, or systems from the codebase context\n"
        "4. Write a clear, specific, actionable task description (3-6 sentences) that a "
        "coding agent can execute directly without asking follow-up questions\n\n"
        "Rules:\n"
        "- Output ONLY the enhanced task description — no preamble, no 'Sure!', no explanation\n"
        "- Include specific file paths or component names inferred from the codebase context\n"
        "- If the request is already clear, output it verbatim (corrected spelling only)\n"
        "- Never invent requirements not implied by the user's words\n"
        "- Keep it under 100 words"
    )

    try:
        enhanced = send_fn(meta_prompt)
        if enhanced and enhanced.strip() and len(enhanced.strip()) > len(raw_input):
            # Sanity check: result should not be wildly different from original intent
            original_words = set(raw_input.lower().split())
            enhanced_words = set(enhanced.lower().split())
            # At least a few words should overlap (guards against hallucinated task switches)
            overlap = original_words & enhanced_words
            if len(overlap) >= min(2, len(original_words)):
                return enhanced.strip()
    except Exception:
        pass

    return raw_input


def _enhance_task_prompt(user_input: str) -> str:
    """Always enhance task prompts before model execution."""
    expanded = _expand_prompt(user_input)
    if expanded != user_input:
        return expanded

    # Check if this is a list generation request
    user_lower = user_input.lower()
    is_list_request = bool(re.search(r"\b(list|enumerate|identify|find)\s+\d+\b", user_lower))

    if is_list_request:
        return (
            f"{user_input}\n\n"
            "INSTRUCTIONS:\n"
            "1. Gather evidence FIRST using READ:/SEARCH: commands on actual project files.\n"
            "2. Every item MUST include specific file paths and line numbers (e.g., file.py:123).\n"
            "3. Base ALL findings on verified evidence from file reads and searches.\n"
            "4. No generic advice - only cite specific code locations you've examined.\n"
            "5. Reference ONLY files verified via READ:/SEARCH: - no invented paths.\n"
            "6. This is read-only analysis: no FILE: blocks, tests, or code changes.\n"
        )

    if _is_readonly_analysis_request(user_input):
        return (
            f"{user_input}\n\n"
            "INSTRUCTIONS:\n"
            "1. Restate the task goal in one sentence.\n"
            "2. This is read-only analysis: no FILE:, no tests, no implementation unless the user explicitly asked.\n"
            "3. Use READ:/SEARCH: to examine files and verify claims with specific file:line references.\n"
            "4. Base findings on evidence from actual file contents, not assumptions.\n"
        )
    return (
        f"{user_input}\n\n"
        "INSTRUCTIONS:\n"
        "1. Restate the task goal in one sentence.\n"
        "2. Identify constraints and assumptions.\n"
        "3. Use READ:/SEARCH: before edits and prefer minimal, verifiable changes.\n"
        "4. Validate with tests or runnable commands.\n"
        "5. If writing code, emit complete FILE: blocks.\n"
    )


def _build_enhanced_reasoning_prompt(user_input: str, context: dict[str, Any] | None = None) -> str:
    """Build an enhanced prompt with chain-of-thought reasoning structure.

    This encourages the model to think through problems systematically.
    """
    reasoning_template = f"""## Task Analysis

**User Request:** {user_input}

Before implementing, think through this systematically:

### 1. UNDERSTAND
- What is the core objective?
- What are the explicit requirements?
- What are the implicit requirements?
- What would success look like?

### 2. ANALYZE
- What constraints exist?
- What assumptions am I making?
- What could go wrong?
- What edge cases exist?

### 3. PLAN
- What files need to be read first?
- What is the sequence of changes?
- What tests should be written first (TDD)?
- How will I verify success?

### 4. EXECUTE
Follow the plan with:
- READ: commands to understand existing code
- FILE: blocks for all changes (complete files only)
- RUN: commands to validate

### 5. VALIDATE
- Run tests after every change
- Fix any failures immediately
- Verify the solution meets all requirements

---

If the user asked only for analysis, review, or prioritized recommendations (no implementation), answer in prose with READ:/SEARCH: only if needed — skip FILE:, TDD, and RUN:.

Otherwise execute this task: start with READ: commands to understand the codebase, then proceed with TDD.
"""
    return reasoning_template


def _analyze_task_complexity(user_input: str) -> tuple[str, bool]:
    """Analyze task complexity to determine if enhanced reasoning is needed.

    Returns (complexity_level, needs_reasoning).
    """
    input_lower = user_input.lower()

    # Keywords indicating complex tasks
    complex_keywords = [
        "implement",
        "create",
        "build",
        "design",
        "architect",
        "refactor",
        "optimize",
        "integrate",
        "migrate",
        "add feature",
        "full",
        "complete",
        "comprehensive",
        "system",
        "framework",
    ]

    # Keywords indicating simple tasks
    simple_keywords = [
        "fix typo",
        "rename",
        "format",
        "lint",
        "simple",
        "quick",
        "small",
        "minor",
        "update comment",
        "add comment",
    ]

    # Check for simple tasks first
    if any(kw in input_lower for kw in simple_keywords):
        return "simple", False

    # Check for complex tasks
    if any(kw in input_lower for kw in complex_keywords):
        return "complex", True

    # Check word count - longer requests are often more complex
    word_count = len(user_input.split())
    if word_count > 50:
        return "complex", True

    return "medium", True


def _extract_and_validate_code(
    response: str,
    cwd: Path,
    code_validator: CodeValidator,
) -> tuple[list[str], list[str]]:
    """Extract code from response and validate it.

    Returns (valid_files, errors).
    """
    files: list[str] = []
    errors: list[str] = []

    # Extract FILE: blocks
    file_pattern = r"FILE:\s*(\S+)\s*\n```[^\n]*\n(.*?)```"
    for match in re.finditer(file_pattern, response, re.DOTALL):
        filepath = match.group(1).strip()
        content = match.group(2)

        # Determine language from extension
        ext = Path(filepath).suffix.lower()
        language_map = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".go": "go",
        }
        language = language_map.get(ext, "unknown")

        # Validate the code
        validation = code_validator.validate(content, language, filepath)

        if validation.valid:
            files.append(filepath)
        else:
            errors.extend(validation.errors)
            for warning in validation.warnings:
                errors.append(f"Warning in {filepath}: {warning}")

    return files, errors


def _perform_cli_update(*, check_only: bool = False, from_repl: bool = False) -> bool:
    """Check for and optionally apply the latest SAGE CLI update."""

    updater = CLIAutoUpdater()
    version = updater.check_for_update(force=True)

    if check_only:
        if version.update_available:
            renderer.success(f"SAGE AI update available: v{version.current} -> v{version.latest}")
            return True
        renderer.success(f"SAGE AI is already up to date (v{version.current}).")
        return True

    if not version.update_available:
        renderer.success(f"SAGE AI is already up to date (v{version.current}).")
        return True

    renderer.info(f"Updating SAGE AI from v{version.current} to v{version.latest}...")
    result = updater.ensure_latest()
    if result.ok:
        if result.scheduled:
            renderer.warning(result.message)
            if from_repl:
                renderer.info(
                    "Exit SAGE (`/exit`) so the updater can replace sage.exe."
                )
            else:
                renderer.info("Exiting now so the updater can finish.")
        else:
            renderer.success(result.message)
            if from_repl and result.updated:
                renderer.warning("Restart SAGE to load the updated CLI runtime in this session.")
        return True

    renderer.error(result.message)
    return False


# ── Agent Orchestration ──────────────────────────────────────


