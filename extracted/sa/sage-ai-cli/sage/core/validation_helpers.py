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


def _write_file(
    filepath_str: str,
    content: str,
    cwd: Path,
    protected_files: set[str] | None = None,
) -> str | None:
    """Safely write a file under *cwd*. Returns the relative path or None.

    Rejects:
    - Language tag names without extensions (e.g., 'bash', 'python')
    - Files without any extension or directory component
    - Path traversal attacks
    - Files in the protected set (SAGE/runtime internals and repo metadata)
    - Files with syntax errors (Python, JSON)
    - Files that appear truncated or incomplete
    """
    if Path(filepath_str).name == "__init__.py":
        content = ""
    from sage.main import _INVALID_FILENAMES
    candidate = (filepath_str or "").strip()
    if Path(candidate).is_absolute() or candidate.startswith("~"):
        renderer.debug_warning(f"Rejected absolute filename: {candidate}")
        return None

    cwd_str = str(cwd)
    if filepath_str.startswith(cwd_str):
        filepath_str = filepath_str[len(cwd_str) :].lstrip("/")
    if filepath_str.startswith("/"):
        renderer.debug_warning(f"Rejected absolute filename: {filepath_str}")
        return None
    filepath_str = filepath_str.lstrip("/")

    # Reject bare language tags (model wrote "FILE: bash")
    if filepath_str.lower() in _INVALID_FILENAMES:
        renderer.debug_warning(f"Rejected invalid filename: {filepath_str}")
        return None

    # Reject files with no extension and no directory (likely a mistake)
    if "/" not in filepath_str and "." not in filepath_str:
        renderer.debug_warning(f"Rejected filename without extension: {filepath_str}")
        return None

    # Block overwriting protected files (runtime internals / repo metadata)
    if protected_files and filepath_str in protected_files:
        renderer.debug_warning(f"Blocked overwrite of existing file: {filepath_str}")
        return None

    # PRE-VALIDATION: Check content before writing
    is_valid, error = _pre_validate_content(filepath_str, content)
    if not is_valid:
        renderer.debug_warning(f"Rejected {filepath_str}: {error}")
        return None

    try:
        target = (cwd / filepath_str).resolve()
        if not str(target).startswith(str(cwd.resolve())):
            renderer.warning(f"Path traversal blocked: {filepath_str}")
            return None
    except (ValueError, OSError):
        return None
    try:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

        # ══════════════════════════════════════════════════════════════════════════
        # PROOF OF EXECUTION: Verify file was actually written
        # This prevents hallucinated "file written" claims
        # ══════════════════════════════════════════════════════════════════════════
        if not target.exists():
            renderer.error(
                f"❌ EXECUTION VERIFICATION FAILED: {filepath_str} does not exist after write"
            )
            return None

        # Verify content was written correctly (check file size)
        actual_size = target.stat().st_size
        expected_size = len(content.encode("utf-8"))
        if actual_size == 0 and expected_size > 0:
            renderer.error(f"❌ EXECUTION VERIFICATION FAILED: {filepath_str} is empty after write")
            return None

        # For non-trivial files, verify first bytes match
        if expected_size > 10:
            actual_content = target.read_text(encoding="utf-8", errors="replace")
            if actual_content[:50] != content[:50]:
                renderer.error(f"❌ EXECUTION VERIFICATION FAILED: {filepath_str} content mismatch")
                return None

        return filepath_str
    except OSError as exc:
        renderer.warning(f"Could not write {filepath_str}: {exc}")
        return None


def _build_session_protected_files(cwd: Path) -> set[str]:
    """Return files that should never be mutated by the assistant runtime.

    Sources of protection:
    1. System directories (.git, node_modules, etc.) — always protected.
    2. .sageprotect files anywhere in the tree — each line is a path or glob
       pattern (relative to that file's directory) that sage will refuse to write.
       Create one with: echo "auth.js" > src/firebase/.sageprotect
    """
    protected: set[str] = set()
    protected_roots = {
        ".git", ".sage", ".venv", "venv", "__pycache__",
        "node_modules", ".pytest_cache", ".mypy_cache", "dist", "build",
    }

    for root_name in protected_roots:
        root_path = cwd / root_name
        if root_path.exists():
            if root_path.is_file():
                protected.add(root_name)
            else:
                for root, _, files in os.walk(root_path):
                    for f in files:
                        p = Path(root) / f
                        try:
                            protected.add(p.relative_to(cwd).as_posix())
                        except ValueError:
                            continue

    # Load .sageprotect files — walk the whole tree once
    try:
        for protect_file in cwd.rglob(".sageprotect"):
            base = protect_file.parent
            try:
                for line in protect_file.read_text(encoding="utf-8").splitlines():
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    # Support both exact paths and simple globs
                    for match in base.glob(line):
                        try:
                            protected.add(match.relative_to(cwd).as_posix())
                        except ValueError:
                            pass
            except OSError:
                pass
    except Exception:
        pass

    return protected


def _clean_manifest_line(line: str) -> str:
    """Clean a manifest line by stripping markdown list prefixes and wrapping quotes/backticks."""
    line = line.strip()
    # Strip leading markdown list markers: e.g. "- ", "* ", "1. ", "10. ", etc.
    import re
    cleaned = re.sub(r'^([-*+]\s+|\d+\.\s+)', '', line)
    # Strip any backticks or quotes
    cleaned = cleaned.strip("`'\" ")
    return cleaned


def _extract_and_write_files(
    output: str,
    cwd: Path,
    protected_files: set[str] | None = None,
    files_read: set[str] | None = None,
    failed_writes: dict[str, str] | None = None,
) -> list[str]:
    """Parse model output for file blocks and write them to disk.

    Recognizes:
      1. FILE: path/to/file.ext\\n```\\ncontent\\n```
      2. ```path/to/file.ext\\ncontent\\n```

    protected_files: set of relative paths that should not be overwritten
        (for example `.git/` or `.sage/` internals).
    files_read: set of paths that have been READ (enforces READ-before-write for existing files).
    Rejects garbage code (empty functions, no assertions in tests, placeholders).

    ENFORCEMENT: If the current request is classified as read-only (ANALYSIS, LIST_GENERATION,
    QUESTION, SEARCH), ALL FILE: blocks are rejected to prevent accidental code generation.
    """
    from sage.main import _add_session_file_read, _failure_loop_detector, _get_current_classification, _normalize_workspace_relative_path, _record_file_read
    written: list[str] = []
    seen: set[str] = set()
    files_read = files_read or set()

    # Patterns to match FILE: blocks in order of specificity
    file_block_patterns = [
        # Pattern 1: FILE: path\n```lang\ncontent\n``` (most common)
        r"FILE:\s*(\S+)\s*\n```[^\n]*\n(.*?)```",
        # Pattern 2: FILE: path (with optional colon after path)\n```content```
        r"FILE:\s*([^\n:]+?)(?::\s*)?\n```[^\n]*\n(.*?)```",
        # Pattern 3: **FILE:** path\n```content``` (markdown bold)
        r"\*\*FILE:\*\*\s*(\S+)\s*\n```[^\n]*\n(.*?)```",
        # Pattern 4: `FILE: path`\n```content``` (inline code)
        r"`FILE:\s*(\S+)`\s*\n```[^\n]*\n(.*?)```",
        # Pattern 5: ### FILE: path\n```content``` (header style)
        r"#+\s*FILE:\s*(\S+)\s*\n```[^\n]*\n(.*?)```",
        # Pattern 6 (FALLBACK): FENCE-LESS
        r"FILE:\s*([^\n]+)\n(.*?)(?=\nFILE:|\Z)",
    ]

    # ══════════════════════════════════════════════════════════════════════════
    # CRITICAL ENFORCEMENT: Block file writes for read-only request types
    # BUT still extract and display list/analysis content from the response
    # ══════════════════════════════════════════════════════════════════════════
    classification = _get_current_classification()
    if classification and classification.read_only:
        if classification.request_type == _RequestType.LIST_GENERATION:
            output = _dedupe_numbered_list_items(output)
        # Count actual valid file blocks that would be written
        file_count = 0
        seen_test: set[str] = set()
        for pattern in file_block_patterns:
            for m in re.finditer(pattern, output, re.DOTALL):
                raw_fp = m.group(1).strip().rstrip(":")
                
                # Skip if there is non-whitespace preceding text on the same line (e.g. '1. FILE:')
                line_start = output.rfind("\n", 0, m.start()) + 1
                preceding_text = output[line_start:m.start()].strip()
                if preceding_text:
                    continue
                
                # Path must not contain spaces or typical conversational characters
                if " " in raw_fp or any(c in raw_fp for c in ["*", "?", "\"", "<", ">", "|", "!", "(", ")"]):
                    continue

                fp = _normalize_workspace_relative_path(raw_fp, cwd)
                if fp in seen_test:
                    continue
                seen_test.add(fp)

                # Skip invalid paths or path traversals
                if fp.startswith("../") or fp.startswith("/") or fp.startswith("~") or fp == "..":
                    continue

                content = m.group(2).strip()
                # If there's content and a valid file name (with extension)
                if content and "." in Path(fp).name:
                    is_garbage, _ = _is_garbage_content(fp, content)
                    if not is_garbage:
                        file_count += 1

        if file_count > 0:
            # HARD ENFORCEMENT: Mode boundary violation is an error, not a warning
            renderer.error(
                f"❌ MODE VIOLATION: {file_count} FILE: block(s) REJECTED — "
                f"request type is {classification.request_type.name} (read-only analysis). "
                "The user asked for analysis/listing, not code changes. "
                "Implementation requires explicit user approval."
            )
            # Track this as a mode violation for failure loop detection
            _failure_loop_detector.record_error(
                f"mode_violation:file_blocks_in_{classification.request_type.name}"
            )

        # CRITICAL FIX: For LIST_GENERATION, extract and display the list content
        # even though we're not writing any files
        if classification.request_type == _RequestType.LIST_GENERATION:
            # Use unified extraction for consistent counting across SAGE
            item_count = _extract_list_item_count(output)
            detailed_items = _extract_list_items_detailed(output)

            if item_count > 0 and renderer.is_verbose():
                renderer.info(f"📋 Extracted {item_count} list items from response")
                if item_count > 10 and detailed_items:
                    first_items = [d["content"][:40] for d in detailed_items[:5]]
                    last_items = [d["content"][:40] for d in detailed_items[-3:]]
                    renderer.info(f"   First items: {', '.join(first_items)}...")
                    renderer.info(f"   Last items: ...{', '.join(last_items)}")

        return []  # Return empty - no files written for read-only requests

    pending_filepaths: list[str] = []
    for pattern in file_block_patterns:
        for m in re.finditer(pattern, output, re.DOTALL):
            raw_fp = m.group(1).strip().rstrip(":")
            
            # Skip if there is non-whitespace preceding text on the same line (e.g. '1. FILE:')
            line_start = output.rfind("\n", 0, m.start()) + 1
            preceding_text = output[line_start:m.start()].strip()
            if preceding_text:
                continue
            
            # Path must not contain spaces or typical conversational characters
            if " " in raw_fp or any(c in raw_fp for c in ["*", "?", "\"", "<", ">", "|", "!", "(", ")"]):
                continue

            pending_filepaths.append(_normalize_workspace_relative_path(raw_fp, cwd))
    pending_modules = _pending_modules_for_files(pending_filepaths)

    # ── Greenfield detection ─────────────────────────────────────────────────
    # Check BEFORE any writes happen. If the workspace has < 15 source files
    # we are scaffolding a new project. In that case:
    #   1. Skip directory-existence validation — ALL dirs are new by definition
    #   2. Skip suspicious-import and import-existence checks — modules haven't
    #      been written yet; rejecting them creates an impossible chicken-and-egg
    #      situation where nothing ever gets written.
    # This check runs once per batch and is NOT re-evaluated as files are
    # written, preventing the "first file creates dir → blocks all siblings" bug.
    _skip_patterns = {".git", "node_modules", "__pycache__", ".sage", ".env", "dist", "build"}
    _src_count = 0
    try:
        for _item in cwd.rglob("*"):
            if _item.is_file() and not any(p in _item.parts for p in _skip_patterns):
                if _item.suffix in {".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java"}:
                    _src_count += 1
                    if _src_count >= 15:
                        break
    except Exception:
        pass
    _is_greenfield_batch = _src_count < 15

    for pattern in file_block_patterns:
        for m in re.finditer(pattern, output, re.DOTALL):
            raw_fp = m.group(1).strip().rstrip(":")  # Remove trailing colon if present
            
            # Skip if there is non-whitespace preceding text on the same line (e.g. '1. FILE:')
            line_start = output.rfind("\n", 0, m.start()) + 1
            preceding_text = output[line_start:m.start()].strip()
            if preceding_text:
                continue
            
            # Path must not contain spaces or typical conversational characters
            if " " in raw_fp or any(c in raw_fp for c in ["*", "?", "\"", "<", ">", "|", "!", "(", ")"]):
                continue

            fp = _normalize_workspace_relative_path(raw_fp, cwd)
            from sage.core.tools import strip_markdown_fences
            content = strip_markdown_fences(m.group(2))
            if fp in seen:
                continue
            seen.add(fp)

            if fp.startswith("../") or fp.startswith("/") or fp.startswith("~") or fp == "..":
                renderer.debug_warning(f"REJECTED FILE PATH '{fp}': path traversal/absolute paths")
                continue

            # ══════════════════════════════════════════════════════════════════════════
            # VALIDATE FILE PATH AGAINST ACTUAL CODEBASE STRUCTURE
            # Skip for greenfield batches — directory-existence checks cause a
            # chicken-and-egg problem: the first file creates a dir, then every
            # subsequent file in any new subdir is blocked by "dir doesn't exist".
            # ══════════════════════════════════════════════════════════════════════════
            if not _is_greenfield_batch:
                is_valid_path, path_error = _validate_file_path_against_codebase(fp, cwd)
                if not is_valid_path:
                    renderer.debug_warning(f"REJECTED FILE PATH '{fp}': {path_error}")
                    continue

            # Enforce READ-before-write for existing files
            normalized_fp = fp[2:] if fp.startswith("./") else fp
            target_path = cwd / normalized_fp
            if target_path.exists() and normalized_fp not in files_read:
                _read_file_context(normalized_fp, cwd, max_lines=80)
                _record_file_read(normalized_fp, success=True)
                files_read.add(normalized_fp)
                _add_session_file_read(cwd, normalized_fp)

            # Check for garbage content
            is_garbage, reason = _is_garbage_content(fp, content)
            if is_garbage:
                renderer.debug_warning(f"File {fp} contains placeholder/garbage: {reason} (writing for validation)...")

            # Validate imports for ALL Python files (not just tests)
            if fp.endswith(".py"):
                # Skip hallucination + import checks for greenfield batches.
                # In a new project, ALL internal modules are "missing" by
                # definition — rejecting them makes writing a project impossible.
                if not _is_greenfield_batch:
                    is_hallucinated, hallucination_reason = _is_likely_hallucinated_code(
                        content,
                        cwd,
                        pending_modules=pending_modules,
                    )
                    if is_hallucinated:
                        renderer.debug_warning(
                            f"REJECTED {fp}: {hallucination_reason}. "
                            "Check AVAILABLE MODULES list before importing!"
                        )
                        if failed_writes is not None:
                            failed_writes[fp] = hallucination_reason
                        continue

                    is_valid, missing = _validate_imports_in_content(
                        content,
                        cwd,
                        pending_modules=pending_modules,
                    )
                    if not is_valid:
                        err_msg = f"imports non-existent modules: {', '.join(missing)}"
                        if "test_" in fp or fp.startswith("tests/"):
                            renderer.debug_warning(
                                f"REJECTED test file {fp}: {err_msg}. "
                                "Use SEARCH: to find actual modules in this codebase first."
                            )
                        else:
                            renderer.debug_warning(
                                f"REJECTED {fp}: {err_msg}. "
                                "Either the modules don't exist or you need to create them first."
                            )
                        if failed_writes is not None:
                            failed_writes[fp] = err_msg
                        continue

            # Check for hallucinated duplicates of existing files
            is_duplicate, duplicate_reason = _detect_hallucinated_duplicate(fp, content, cwd)
            if is_duplicate:
                renderer.debug_warning(f"REJECTED {fp}: {duplicate_reason}")
                if failed_writes is not None:
                    failed_writes[fp] = duplicate_reason
                continue

            # PRE-VALIDATION check before write
            is_valid, error = _pre_validate_content(fp, content)
            if not is_valid:
                renderer.debug_warning(f"REJECTED {fp}: {error}")
                if failed_writes is not None:
                    failed_writes[fp] = error
                continue

            # Strip SCAFFOLD_COMPLETE signal if it was accidentally captured
            # as file content by the fenceless pattern (happens when the model
            # outputs SCAFFOLD_COMPLETE between two FILE: blocks with no fence).
            content_stripped = content.strip()
            if content_stripped == "SCAFFOLD_COMPLETE":
                content = ""  # treat as empty file (e.g. __init__.py)

            result = _write_file(fp, content, cwd, protected_files=protected_files)
            if result:
                written.append(result)

    if written:
        return written

    # Pattern 2 (fallback): ```filename.ext\ncontent\n```
    lang_tags = {
        "python",
        "javascript",
        "typescript",
        "bash",
        "sh",
        "json",
        "yaml",
        "yml",
        "toml",
        "html",
        "css",
        "sql",
        "go",
        "rust",
        "java",
        "c",
        "cpp",
        "ruby",
        "php",
        "jsx",
        "tsx",
    }
    for m in re.finditer(r"```(\S+)\s*\n(.*?)```", output, re.DOTALL):
        tag = m.group(1).strip()
        content = m.group(2)
        if tag.lower() in lang_tags:
            continue
        if "." not in tag and "/" not in tag:
            continue
        if tag in seen:
            continue
        seen.add(tag)

        tag = _normalize_workspace_relative_path(tag, cwd)

        # Enforce READ-before-write for existing files
        normalized_tag = tag[2:] if tag.startswith("./") else tag
        target_path = cwd / normalized_tag
        if target_path.exists() and normalized_tag not in files_read:
            _read_file_context(normalized_tag, cwd, max_lines=80)
            _record_file_read(normalized_tag, success=True)
            files_read.add(normalized_tag)
            _add_session_file_read(cwd, normalized_tag)

        # Check for garbage content
        is_garbage, reason = _is_garbage_content(tag, content)
        if is_garbage:
            renderer.debug_warning(f"File {tag} contains placeholder/garbage: {reason} (writing for validation)...")

        # Validate imports for Python test files before writing
        if tag.endswith(".py") and ("test_" in tag or tag.startswith("tests/")):
            is_valid, missing = _validate_imports_in_content(
                content,
                cwd,
                pending_modules=pending_modules,
            )
            if not is_valid:
                err_msg = f"imports non-existent modules: {', '.join(missing)}"
                renderer.debug_warning(
                    f"Rejected test file {tag}: {err_msg}. "
                    "Use SEARCH: to find actual modules in this codebase first."
                )
                if failed_writes is not None:
                    failed_writes[tag] = err_msg
                continue

        # PRE-VALIDATION check before write
        is_valid, error = _pre_validate_content(tag, content)
        if not is_valid:
            renderer.debug_warning(f"REJECTED {tag}: {error}")
            if failed_writes is not None:
                failed_writes[tag] = error
            continue

        result = _write_file(tag, content, cwd, protected_files=protected_files)
        if result:
            written.append(result)

    return written


# NOTE: Prompt templates moved to sage/core/prompts.py (P3-71)


def _run_validation_command(cmd: str, cwd: Path, timeout: int = 120) -> tuple[str, str]:
    """Run a validation command, falling back from `python -m pytest` to `pytest`."""
    output = _run_shell(cmd, cwd, timeout=timeout)
    if "No module named pytest" in output and "python -m pytest" in cmd:
        cmd = cmd.replace("python -m pytest", "pytest", 1)
        output = _run_shell(cmd, cwd, timeout=timeout)
    return cmd, output


def _syntax_precheck(written: list[str], cwd: Path) -> tuple[bool, str]:
    """Pre-check syntax of written files before running tests.

    Returns (all_ok, error_details).
    This catches errors early before slower test runs.
    """

    errors = []
    for filepath in written:
        full_path = cwd / filepath
        if not full_path.exists():
            continue

        # Python syntax check
        if filepath.endswith(".py"):
            result = _run_shell(
                f'python -m py_compile "{filepath}"',
                cwd,
                timeout=10,
            )
            # Filter out pytest-cov/coverage warnings that aren't actual syntax errors
            is_real_error = (
                result.strip()
                and ("SyntaxError" in result or "exit code: 1" in result)
                and "pytest-cov" not in result
                and "COV_CORE" not in result
            )
            if is_real_error:
                # Get more detailed error with line number
                detail_result = _run_shell(
                    f'python -c "import ast; ast.parse(open({shlex.quote(filepath)}).read())"',
                    cwd,
                    timeout=10,
                )
                # Only record if ast.parse also fails (confirms real syntax error)
                if "SyntaxError" in detail_result or "Error" in detail_result:
                    errors.append(f"SYNTAX ERROR in {filepath}:\n{detail_result}")

        # JavaScript/TypeScript basic check
        elif filepath.endswith((".js", ".ts", ".jsx", ".tsx")):
            # Check for obvious syntax errors using node --check if available
            result = _run_shell(
                f'node --check "{filepath}" 2>&1 || echo "exit code: $?"',
                cwd,
                timeout=10,
            )
            if "SyntaxError" in result or "Unexpected" in result:
                errors.append(f"SYNTAX ERROR in {filepath}:\n{result}")

        # JSON validation
        elif filepath.endswith(".json"):
            result = _run_shell(
                f'python -c "import json; json.load(open({shlex.quote(filepath)}))"',
                cwd,
                timeout=5,
            )
            if "Error" in result or "exit code" in result:
                errors.append(f"INVALID JSON in {filepath}:\n{result}")

        # YAML validation
        elif filepath.endswith((".yml", ".yaml")):
            result = _run_shell(
                f'python -c "import yaml; yaml.safe_load(open({shlex.quote(filepath)}))"',
                cwd,
                timeout=5,
            )
            if "Error" in result or "exit code" in result:
                errors.append(f"INVALID YAML in {filepath}:\n{result}")

    if errors:
        return False, "\n\n".join(errors)
    return True, ""


def _auto_validate(written: list[str], cwd: Path) -> str | None:
    """Run automatic validation on written files. Returns (cmd, output) or None.

    Validation order:
    0. Garbage / Placeholder check
    1. Syntax pre-check (fast, catches obvious errors)
    2. Project-specific validation (pytest, npm test, etc.)
    3. Fallback syntax-only check if no test framework found
    """
    # Step 0: Garbage / Placeholder check
    for fp in written:
        target = cwd / fp
        if target.exists():
            try:
                content = target.read_text(encoding="utf-8")
                is_garbage, reason = _is_garbage_content(fp, content)
                if is_garbage:
                    return "code completeness check", f"File '{fp}' is incomplete: {reason}. Write the complete implementation without placeholder stubs."
            except Exception:
                pass

    # Step 1: Fast syntax pre-check
    syntax_ok, syntax_errors = _syntax_precheck(written, cwd)
    if not syntax_ok:
        return "syntax pre-check", syntax_errors

    # Step 2: Project-specific validation
    validation_cmd = _validation_command_for_written_files(written, cwd)
    if validation_cmd:
        return _run_validation_command(validation_cmd, cwd, timeout=120)

    # Step 3: Fallback - at least check Python files compile
    runnable = _detect_runnable_files(written)
    if runnable:
        checks = []
        for f in runnable:
            result = _run_shell(
                f'python -c "import ast; ast.parse(open({shlex.quote(f)}).read())"',
                cwd,
                timeout=10,
            )
            if "exit code" in result or "Error" in result:
                checks.append(f"{f}: {result}")
        if checks:
            return "python syntax check", "\n".join(checks)

    return None


# ══════════════════════════════════════════════════════════════════════════════
# IMPLEMENTATION INTEGRITY - Phantom Implementation Detection
# ══════════════════════════════════════════════════════════════════════════════


def _detect_phantom_implementation(
    response_text: str, files_written: list[str], is_implementation_request: bool
) -> tuple[bool, str]:
    """Detect if response claims implementation but didn't actually write files.

    Args:
        response_text: The model's response
        files_written: List of files actually written
        is_implementation_request: Whether this was an implementation request

    Returns:
        Tuple of (is_phantom, reason)
    """
    if not is_implementation_request:
        return False, ""

    # Check for implementation claims
    impl_claims = [
        "implementation complete",
        "implemented",
        "i've implemented",
        "i have implemented",
        "code is now ready",
        "tests pass",
        "all tests pass",
    ]

    response_lower = response_text.lower()
    has_claim = any(claim in response_lower for claim in impl_claims)

    # Check for code snippets
    has_code_snippets = (
        "```python" in response_text
        or "```javascript" in response_text
        or "```typescript" in response_text
    )

    # If claims implementation or shows code but wrote no files, it's phantom
    if (has_claim or has_code_snippets) and len(files_written) == 0:
        return True, "claimed implementation but no files written"

    return False, ""


def _validate_implementation_response(
    response_text: str, files_written: list[str], is_implementation_request: bool
) -> tuple[bool, str]:
    """Validate that implementation responses contain FILE: blocks or RUN: commands.

    Args:
        response_text: The model's response
        files_written: List of files actually written
        is_implementation_request: Whether this was an implementation request

    Returns:
        Tuple of (is_valid, reason)
    """
    if not is_implementation_request:
        return True, ""

    has_file_blocks = "FILE:" in response_text
    has_run_commands = "RUN:" in response_text
    has_read_commands = "READ:" in response_text
    has_code_snippets = bool(
        re.search(r"```(?:python|javascript|typescript|tsx?|jsx?)", response_text)
    )

    if has_code_snippets and not has_file_blocks:
        return (
            False,
            "Implementation response included code fences without FILE: blocks",
        )

    # Implementation must have FILE: blocks or RUN: commands (not just READ:)
    if not has_file_blocks and not has_run_commands:
        # Check if it's just planning/analysis
        if has_read_commands:
            return True, ""  # Just reading/researching is okay

        return (
            False,
            "Implementation response must contain FILE: blocks or RUN: commands with actual code",
        )

    if has_run_commands and not has_file_blocks and not has_read_commands:
        return (
            False,
            "Implementation response ran commands but did not provide FILE: blocks with actual code",
        )

    return True, ""


def _validate_tdd_compliance(
    response_text: str, files_written: list[str], is_implementation_request: bool
) -> tuple[bool, str]:
    """Validate that TDD claims are backed by actual file writes.

    Args:
        response_text: The model's response
        files_written: List of files actually written
        is_implementation_request: Whether this was an implementation request

    Returns:
        Tuple of (is_compliant, reason)
    """
    if not is_implementation_request:
        return True, ""

    # Check for TDD claims
    tdd_claims = [
        "tdd",
        "test-driven",
        "tests first",
        "write tests",
        "created test",
    ]

    response_lower = response_text.lower()
    claims_tdd = any(claim in response_lower for claim in tdd_claims)

    if claims_tdd and len(files_written) == 0:
        return (
            False,
            "Response claimed TDD process but no files were written (no FILE: blocks executed)",
        )

    # If claims TDD, should have test files
    if claims_tdd and len(files_written) > 0:
        has_test_files = any("test" in f.lower() for f in files_written)
        if not has_test_files:
            return False, "Claimed TDD but no test files were written"

    return True, ""


# =============================================================================
# BEHAVIORAL VALIDATION - Fixes for SAGE run behavioral bugs
# =============================================================================


def _detect_tool_description_vs_execution(response: str) -> tuple[bool, list[str]]:
    """Detect when model describes tools instead of executing them.

    P1-8: This function now delegates to renderer._detect_bad_streaming_patterns
    for the core pattern detection, reducing duplication.

    Args:
        response: The model's response text

    Returns:
        Tuple of (is_descriptive, list of mentioned tools)
        is_descriptive is True if tools are mentioned in prose, not executed
    """
    from sage.main import _extract_tool_commands_structured
    # Strip <think>/<thinking> blocks before validation. Reasoning models
    # (qwen3, deepseek-r1) emit a multi-paragraph "Let me check..." plan
    # inside <think>...</think>. That's NOT the response — it's the model's
    # internal trace. Validating against it produces false positives where
    # the actual response was fine but the thinking trace narrated tools
    # instead of using them.
    from sage.core.thinking_filter import strip_thinking_blocks
    response = strip_thinking_blocks(response)
    structured_calls = _extract_tool_commands_structured(response)

    # P1-8: Use centralized pattern detection from renderer
    # This avoids duplicating tool_refusal, nonstandard_tool, and argumentative patterns
    is_bad, reason = renderer._detect_bad_streaming_patterns(
        response,
        tool_calls=structured_calls,
    )
    if is_bad:
        # Map the reason to a category for backwards compatibility
        if "refusal" in reason.lower() or "cannot" in reason.lower():
            return True, ["TOOL_REFUSAL"]
        elif "syntax" in reason.lower() or "non-standard" in reason.lower():
            return True, ["NONSTANDARD_TOOL_SYNTAX"]
        elif "argumentative" in reason.lower() or "approval" in reason.lower():
            return True, ["ARGUMENTATIVE_BEHAVIOR"]
        elif "described tool" in reason.lower():
            return True, ["DESCRIBED_TOOL"]
        else:
            # Generic bad pattern
            return True, ["BAD_PATTERN"]

    # Check for introductory descriptive phrases before tool commands
    # E.g., "I will read these files:", "by reading the following files:", "Let me investigate by reading:"
    intro_patterns = [
        r"(?:will|going to|need to|plan to)\s+(?:read|search|run|execute|investigate)",
        r"(?:let me|let's|i'm going to|i am going to)\s+(?:read|search|run|execute|investigate)",
        r"(?:investigate|analyze|examine)\s+(?:by|through)\s+(?:read|search|run)",
        r"by\s+(?:reading|searching|running|executing)",
    ]

    intro_matches = []
    for pattern in intro_patterns:
        intro_matches.extend(list(re.finditer(pattern, response, re.MULTILINE | re.IGNORECASE)))

    # Tools at start of line (actual execution format)
    execution_pattern = r"^\s*(READ|SEARCH|RUN):\s*(.+)$"
    execution_matches = list(re.finditer(execution_pattern, response, re.MULTILINE))

    # Collect ALL tool commands (not just unique types)
    mentioned_tools = []
    for match in execution_matches:
        tool_type = match.group(1).upper()
        mentioned_tools.append(tool_type)

    # UPDATED LOGIC: Only flag as descriptive if:
    # 1. There are intro phrases but NO execution commands (model only describes)
    # 2. OR there are vastly more intro phrases than actual commands (5:1 ratio)
    # If there are actual READ:/SEARCH:/RUN: commands, let them execute
    if len(execution_matches) == 0:
        # No execution commands at all - this is descriptive if there's any intro text
        is_descriptive = len(intro_matches) > 0
    elif len(intro_matches) > len(execution_matches) * 5:
        # Way more description than execution - still problematic
        is_descriptive = True
    else:
        # Has actual commands - allow even with some preamble
        is_descriptive = False

    return is_descriptive, mentioned_tools


def _detect_repetitive_filler(response: str) -> tuple[bool, float]:
    """Detect repetitive filler content in numbered lists.

    Args:
        response: The model's response text

    Returns:
        Tuple of (is_filler, repetition_score)
        is_filler is True if response contains high repetition
        repetition_score is 0.0 to 1.0 indicating level of repetition
    """
    # Strip reasoning-model thinking blocks — qwen3 often produces a long
    # numbered plan inside <think>...</think> that would otherwise trip
    # the filler detector and force a retry.
    from sage.core.thinking_filter import strip_thinking_blocks
    response = strip_thinking_blocks(response)
    # Extract numbered list items
    item_pattern = r"^\s*\d+\.\s+(.+)$"
    items = re.findall(item_pattern, response, re.MULTILINE)

    if len(items) < 5:
        return False, 0.0

    # Normalize items (remove variable parts)
    normalized_items = []
    for item in items:
        # Extract the template by removing specific words and single letters
        # E.g., "Implement basic logging for X" -> "Implement basic logging for"
        # E.g., "Implement X for Y" -> "Implement X for X"
        normalized = re.sub(
            r"\b(debugging|informational|tracing|performance|security|audit|user|system|config|deployment|maintenance|restart|health|resource|memory|CPU|network|database|external|message|file|packet|dependency)\b",
            "X",
            item,
            flags=re.IGNORECASE,
        )
        # Also normalize single capital letters or very short words that are likely variables
        normalized = re.sub(r"\b[A-Z]\b", "X", normalized)
        normalized = re.sub(
            r"\b(for|the|in|on|at|to|of)\s+[a-z]{1,2}\b", "for X", normalized, flags=re.IGNORECASE
        )
        normalized_items.append(normalized.lower().strip())

    # Count unique vs total
    unique_count = len(set(normalized_items))
    total_count = len(normalized_items)

    repetition_score = 1.0 - (unique_count / total_count)

    # Also check for template repetition (same prefix)
    prefixes = [item.split()[:4] for item in normalized_items if len(item.split()) >= 4]
    unique_prefixes = len(set(tuple(p) for p in prefixes))
    prefix_repetition = 1.0 - (unique_prefixes / len(prefixes)) if prefixes else 0.0

    # High repetition if either metric is high
    combined_score = max(repetition_score, prefix_repetition)

    is_filler = combined_score > 0.7

    return is_filler, combined_score


# =============================================================================
# CODE-OUTPUT INTEGRITY GUARDS
# =============================================================================
#
# Two failure modes seen in production with free-tier Qwen-family models on
# OpenRouter (qwen3-coder:free) and Qwen-derived ggufs (DeepSeek-R1-Distill-
# Qwen). The model bleeds Chinese identifiers into Python/TS output and/or
# emits aider-style search/replace markers that sage doesn't parse.
#
# Both produce code that won't even import. Letting them through wastes
# the user's tokens AND time, so we reject hard and force a retry.


# CJK Unicode ranges (Hangul/Hiragana/Katakana/Han) — anything from these
# blocks inside a Python/TS/JS *identifier* (function/class/variable name
# or import target) is a sign the model has language-drifted. Inside
# string literals or comments this is fine and common (user-facing strings,
# internationalization). We only fail when it appears in code structure.
_NON_ASCII_LETTER_RE = re.compile(r"[぀-ゟ゠-ヿ一-鿿가-힯㐀-䶿]")

# Match identifiers / imports that contain a CJK letter. The lookahead
# anchors on common syntactic positions: function/class definitions,
# imports, variable assignments, attribute access.
_NON_ASCII_IDENTIFIER_RE = re.compile(
    r"""
    (?:
        # Python: `def name(`, `class Name:`, `from name import`, `import name`
        ^\s*(?:def|class|from|import)\s+[\w.]*[぀-ゟ゠-ヿ一-鿿가-힯㐀-䶿][\w.]*
        |
        # TS/JS: `function name(`, `const name =`, `class Name`, `import { name }`
        ^\s*(?:function|const|let|var|class|interface|type|enum)\s+[\w$]*[぀-ゟ゠-ヿ一-鿿가-힯㐀-䶿][\w$]*
        |
        # Generic: `<ident>(` or `<ident>.<thing>` where ident contains CJK
        \b[\w$]*[぀-ゟ゠-ヿ一-鿿가-힯㐀-䶿][\w$]*\s*(?:\(|\.|=)
    )
    """,
    re.MULTILINE | re.VERBOSE,
)

# Extract fenced code blocks + sage FILE: blocks. Anything inside these is
# "code"; everything else is prose where CJK is allowed (the model may
# describe Chinese-language features in a user-facing string, for example).
_CODE_BLOCK_RE = re.compile(r"```[\w-]*\n(.*?)\n```", re.DOTALL)
_FILE_BLOCK_RE = re.compile(r"^FILE:\s*\S+\s*\n(.*?)(?=^FILE:|\Z)", re.DOTALL | re.MULTILINE)


def _detect_non_english_code_identifiers(response: str) -> tuple[bool, list[str]]:
    """Detect CJK identifiers in fenced or FILE: code blocks.

    Returns (has_violations, sample_offenders). Sample is capped at 5 to
    keep the error message readable. We only scan code regions because
    user-facing string literals and i18n labels are legitimate places for
    non-ASCII text; an *identifier* is not.
    """
    code_regions: list[str] = []
    code_regions.extend(_CODE_BLOCK_RE.findall(response))
    code_regions.extend(_FILE_BLOCK_RE.findall(response))

    if not code_regions:
        return False, []

    offenders: list[str] = []
    for code in code_regions:
        for match in _NON_ASCII_IDENTIFIER_RE.finditer(code):
            snippet = match.group(0).strip()
            # Trim trailing punctuation for readable error messages
            snippet = snippet.rstrip("(.=")
            if snippet and snippet not in offenders:
                offenders.append(snippet)
                if len(offenders) >= 5:
                    return True, offenders

    return bool(offenders), offenders


# Aider/Cursor-style diff markers. Sage uses FILE: blocks, not these.
# When a model emits them, the diff cannot be applied — the user sees
# "code" that never actually lands on disk.
_AIDER_SEARCH_RE = re.compile(r"^<{5,}\s*SEARCH\s*$", re.MULTILINE)
_AIDER_REPLACE_RE = re.compile(r"^>{5,}\s*REPLACE\s*$", re.MULTILINE)


def _detect_aider_style_diff_garbage(response: str) -> bool:
    """True if the model used `<<<<<<< SEARCH … >>>>>>> REPLACE` markers.

    Sage's edit protocol is `FILE: path` followed by the whole file
    content (not a diff). Some free-tier Qwen-derived models emit the
    aider/Cursor search/replace format instead, which sage cannot apply.
    Catching this early lets us retry with explicit guidance.
    """
    return bool(_AIDER_SEARCH_RE.search(response) and _AIDER_REPLACE_RE.search(response))


# =============================================================================
# SIMPLE Q&A MODE - Detect non-agent prompts (P0-2)
# =============================================================================


def _is_simple_qa_prompt(prompt: str) -> bool:
    """Detect if a prompt is a simple Q&A that should NOT get agent treatment.

    P0-2: Simple questions like "what is 2+2?" should NOT:
    - Get task templates injected
    - Have grounding requirements
    - Use agent tool protocols

    Args:
        prompt: The user's input prompt

    Returns:
        True if this is a simple Q&A prompt, False if it looks like an agent task
    """
    from sage.main import _is_explicit_resume_request
    if _is_explicit_resume_request(prompt):
        return False

    prompt_lower = prompt.lower().strip()

    # ── Greetings and conversational openers ────────────────────────────────
    # These must NEVER trigger agent tool use.
    GREETINGS = {
        "hello", "hi", "hey", "howdy", "sup", "yo", "greetings",
        "good morning", "good afternoon", "good evening", "good night",
        "hello!", "hi!", "hey!", "hey there", "hello there",
        "what's up", "what's good", "how are you", "how are you?",
        "how's it going", "how's it going?", "how do you do",
        "nice to meet you", "pleased to meet you",
        "thanks", "thank you", "thank you!", "thanks!",
        "ok", "okay", "cool", "got it", "great", "awesome", "nice",
        "sounds good", "perfect", "wonderful", "excellent",
        "bye", "goodbye", "see you", "later", "take care",
        "yes", "no", "sure", "absolutely", "definitely",
    }
    if prompt_lower.strip().rstrip("!.?") in GREETINGS:
        return True
    # Single word or very short casual message (≤ 4 words, no agent indicators)
    words = prompt_lower.split()
    _AGENT_WORDS = re.compile(
        r"(?:fix|debug|implement|create|build|deploy|refactor|read|analyze|"
        r"examine|review|look at|check|update|modify|change|delete|remove|"
        r"run|execute|install|upgrade|migrate|test|search|find|list|show me)\s"
    )
    if len(words) <= 4 and not re.search(r"\.\w{1,5}\b", prompt_lower) and not _AGENT_WORDS.search(prompt_lower):
        return True

    # Simple Q&A indicators (questions that need quick answers)
    simple_qa_patterns = [
        # Math questions
        r"^what\s+is\s+\d+\s*[\+\-\*\/×÷]\s*\d+",
        r"^\d+\s*[\+\-\*\/×÷]\s*\d+\s*[=?]?",
        # Simple factual questions
        r"^what(?:'s| is| are) the (?:capital|population|name|meaning|definition)",
        r"^what does .+ mean",
        r"^who (?:is|was|are|were) ",
        r"^when (?:is|was|did) ",
        r"^where (?:is|are|was|were) ",
        r"^how (?:do|does|can) (?:i|you|one|we) (?:say|print|write|spell)",
        r"^explain\s+(?:what|how|why|the concept of)?\s*",
        r"^define\s+",
        r"^what is (?:a|an|the) (?:\w+\s+){0,2}(?:\?)?$",
        # Conversational questions
        r"^(?:can|could|would|will) you (?:help|tell|show|explain)",
        r"^(?:do|does) (?:sage|you) (?:support|know|understand|have)",
        r"^(?:what|which) (?:models?|languages?|features?) (?:do you|does sage|are)",
        r"^(?:are|is) you(?:r| able| capable)",
        r"^(?:help|assist) (?:me|with)?",
        # Simple code questions (not requiring file access)
        r"^how do i print .+ in (?:python|javascript|java|c\+\+|ruby|go)",
        r"^what(?:'s| is) the syntax for",
    ]

    # Agent task indicators (should NOT be treated as simple Q&A)
    agent_task_patterns = [
        # File/codebase operations
        r"(?:read|analyze|examine|review|look at|check|fix|update|modify|change|refactor)\s+(?:the\s+)?(?:file|code|codebase|project|repo)",
        r"(?:in|from)\s+\w+\.(?:py|js|ts|java|go|rb|rs|cpp|c|h)",
        r"\.py\b|\.js\b|\.ts\b|\.java\b|\.go\b|\.rb\b|\.rs\b",  # File extensions
        # Multi-step tasks
        r"(?:implement|create|build|develop|add|write)\s+(?:a\s+)?(?:new\s+)?(?:feature|function|class|module|component|system)",
        r"list\s+\d+\s+(?:improvements|issues|bugs|problems)",
        # Investigation/analysis tasks
        r"analyze\s+(?:the\s+)?(?:codebase|project|structure)",
        r"find\s+(?:all|any|the)\s+(?:bugs|issues|problems|errors)",
        # Agent-style commands
        r"^(?:fix|debug|refactor|optimize|test|deploy)",
    ]

    # Check for simple Q&A patterns
    for pattern in simple_qa_patterns:
        if re.search(pattern, prompt_lower):
            # But also verify no agent task patterns are present
            has_agent_task = any(re.search(p, prompt_lower) for p in agent_task_patterns)
            if not has_agent_task:
                return True

    # Check if it's a very short question (likely simple)
    words = prompt_lower.split()
    if len(words) <= 10 and prompt_lower.endswith("?"):
        has_agent_task = any(re.search(p, prompt_lower) for p in agent_task_patterns)
        if not has_agent_task:
            return True

    return False


_SIMPLE_QA_SYSTEM_PROMPT = (
    "You are SAGE AI, a helpful AI assistant. "
    "CRITICAL: Respond conversationally and directly. "
    "NEVER use READ:, SEARCH:, RUN:, FILE:, or any tool commands. "
    "NEVER read files, list files, or search the codebase. "
    "For greetings like 'Hello' or 'Hi', just greet the user back warmly. "
    "For questions, answer directly from your knowledge. "
    "No XML tags, no plans, no workflow narration. "
    "If the user asks for exact output, return exactly that and nothing else."
)
_SIMPLE_QA_TIMEOUTS = {
    "ollama": 45.0,
    "llama_cpp": 60.0,
}
def _load_single_turn_timeouts() -> dict[str, float]:
    """Load per-provider timeouts, allowing env-var overrides.

    Defaults are generous for large local models (qwen3-coder-next is 51 GB and
    can take 60-90 s to emit its first planning token).
    Override with SAGE_OLLAMA_TIMEOUT / SAGE_LLAMA_TIMEOUT (seconds).
    """
    def _env_float(key: str, default: float) -> float:
        raw = os.environ.get(key, "").strip()
        try:
            v = float(raw)
            return v  # 0 or negative means "no timeout"
        except ValueError:
            return default

    return {
        "ollama": _env_float("SAGE_OLLAMA_TIMEOUT", 0),   # 0 = no timeout for Ollama
        "llama_cpp": _env_float("SAGE_LLAMA_TIMEOUT", 0), # 0 = no timeout for local GGUF
    }

_SINGLE_TURN_AGENT_TIMEOUTS = _load_single_turn_timeouts()


def _build_simple_qa_messages(
    prompt: str,
    system_prompt: str | None = None,
    history: list[Message] | None = None,
) -> list[Message]:
    """Build a lightweight direct-answer prompt for simple Q&A."""
    effective_system = _SIMPLE_QA_SYSTEM_PROMPT
    if system_prompt and system_prompt.strip():
        effective_system = f"{system_prompt.strip()}\n\n{_SIMPLE_QA_SYSTEM_PROMPT}"

    messages: list[Message] = [Message(role="system", content=effective_system)]
    if history:
        messages.extend(history[-4:])
    messages.append(Message(role="user", content=prompt))
    return messages


def _show_paste_indicator(text: str) -> None:
    """Print `[ Text pasted: N lines, M characters ]` whenever input is
    multi-line or large.

    This is a UX nicety so the user can immediately confirm the terminal
    did NOT truncate their paste. Below the thresholds we stay silent —
    short prompts don't need this signal.

    Uses `renderer.console.print` directly (NOT `renderer.info`) so the
    indicator shows in clean/normal mode too — `renderer.info` is
    verbose-mode-only and would suppress this critical signal.
    """
    if not text:
        return
    line_count = text.count("\n") + 1
    char_count = len(text)
    is_multiline = line_count > 1
    is_large = char_count >= 500
    if not (is_multiline or is_large):
        return
    if is_multiline:
        msg = f"[ Text pasted: {line_count:,} lines, {char_count:,} characters ]"
    else:
        msg = f"[ Text pasted: {char_count:,} characters ]"
    renderer.console.print(f"[dim cyan]{msg}[/dim cyan]")


# Models known to be too slow on typical local hardware for build mode.
# Build pipeline does 30+ LLM calls per project — even a 5-min/call model
# means 2.5 hours per project. We auto-swap to a faster alternative.
_SLOW_BUILD_MODELS: tuple[str, ...] = (
    "qwen3-coder-next",
    "qwen3-coder:30b",
    "qwen2.5-coder:32b",
    "deepseek-r1:70b",
    "llama3.3:70b",
    "qwen2.5:72b",
)

# Preferred fast local models for build mode, in order of preference.
_FAST_BUILD_MODELS: tuple[str, ...] = (
    "devstral:latest",
    "devstral",
    "qwen2.5-coder:14b",
    "qwen2.5-coder:7b",
    "llama3.2:latest",
    "llama3.2",
    "codellama:13b",
    "codellama:7b",
)


def _pick_build_model(current_model_id: str) -> tuple[str, str | None]:
    """Pick the best model for the build pipeline.

    Returns (model_id_to_use, reason_if_swapped). If the current model is
    fast enough, returns it unchanged with reason=None. Otherwise picks
    the fastest available local model and returns a short user-facing
    explanation.
    """
    from sage.main import _ollama_local_models
    if not current_model_id.startswith("ollama:"):
        return current_model_id, None
    bare = current_model_id.split(":", 1)[1]
    bare_no_tag = bare.split(":", 1)[0]
    is_slow = any(
        slow in bare.lower() or slow in bare_no_tag.lower()
        for slow in _SLOW_BUILD_MODELS
    )
    if not is_slow:
        return current_model_id, None
    available = _ollama_local_models()
    if not available:
        return current_model_id, None
    for fast in _FAST_BUILD_MODELS:
        if fast in available or fast.split(":", 1)[0] in available:
            new_id = f"ollama:{fast}"
            return new_id, (
                f"Build mode needs ~30 LLM calls per project. "
                f"`{current_model_id}` averages 5–13 min/call on typical local "
                f"hardware which exhausts the ollama timeout. Switching to "
                f"`{new_id}` (~20–60 s/call) for the build."
            )
    return current_model_id, None


# ---------------------------------------------------------------------------
# Autonomous commands (/autopolit, /autofleet, /autoorg)
# ---------------------------------------------------------------------------


def _autonomous_progress(line: str) -> None:
    """Print autonomous-loop progress directly to the console (bypasses
    verbose-mode gating so the user always sees iteration markers)."""
    renderer.console.print(f"[dim cyan]{line}[/dim cyan]")


def _autonomous_generate_factory(
    router, model_id: str, temp: float, tokens: int, model_locked: bool
):
    """Build a generate(prompt) -> str closure for autonomous loops."""

    def _gen(prompt: str) -> str:
        messages = _build_simple_qa_messages(prompt)
        return router.generate(
            messages, model_id, temp, tokens, lock_provider=model_locked
        )

    return _gen


def _run_autopolit_command(
    message: str | None,
    *,
    cwd: Path,
    sage_agent,
    router,
    model_id: str,
    temp: float,
    tokens: int,
    model_locked: bool,
) -> None:
    """REPL entry point for `/autopolit [message]`.

    Runs the agent loop indefinitely, one iteration at a time, until the
    user presses Ctrl-C or creates `.sage/AUTO-STOP`. Without a message,
    sage self-directs: codebase analysis → TDD improvement → repeat.
    """
    from sage.core.autonomous import run_autopolit_loop, LoopState

    renderer.console.print(
        f"[bold cyan]/autopolit[/bold cyan] starting — "
        f"focus: [bold]{message or '(self-directed code improvement)'}[/bold]"
    )
    renderer.console.print(
        "[dim]Stop with Ctrl-C. Or `touch ./.sage/AUTO-STOP` from another shell.[/dim]"
    )

    def _iteration(prompt: str, state: LoopState) -> dict:
        # Single in-process agent turn. Catches the agent's own errors so
        # the loop continues. The sage_agent already handles tool execution
        # so files get written / tests get run inside one call.
        try:
            sage_agent.execute_task_prompt(prompt, save_history=True)
            return {
                "iteration": state.iteration,
                "response_hash": f"iter-{state.iteration}-{int(time.time())}",
                "success": True,
            }
        except KeyboardInterrupt:
            raise
        except Exception as exc:
            return {"iteration": state.iteration, "error": str(exc)}

    try:
        run_autopolit_loop(
            task=message,
            project_root=cwd,
            run_one_iteration=_iteration,
            progress=_autonomous_progress,
            iteration_delay_seconds=0.5,
        )
    except KeyboardInterrupt:
        renderer.console.print("\n[yellow]/autopolit cancelled. Sage is still running.[/yellow]")


def _run_autofleet_command(
    message: str | None,
    *,
    cwd: Path,
    router,
    model_id: str,
    temp: float,
    tokens: int,
    model_locked: bool,
    cfg,
) -> None:
    """REPL entry point for `/autofleet [message]`.

    Each iteration decomposes the focus into multiple subtasks and runs
    them in parallel threads (one model call per thread, optionally with
    different models picked by MultiModelOrchestrator). Repeats forever
    until cancelled.
    """
    from sage.core.autonomous import run_autofleet_loop, LoopState

    renderer.console.print(
        f"[bold cyan]/autofleet[/bold cyan] starting — "
        f"focus: [bold]{message or '(self-directed code improvement)'}[/bold]"
    )
    renderer.console.print(
        "[dim]Stop with Ctrl-C. Or `touch ./.sage/AUTO-STOP` from another shell.[/dim]"
    )

    generate = _autonomous_generate_factory(router, model_id, temp, tokens, model_locked)

    def _decompose(task: str | None, state: LoopState) -> list[str]:
        # Ask the model to decompose the focus into 4 parallel subtasks.
        focus = task or "self-directed improvement of this codebase"
        decomp_prompt = (
            f"Decompose this work into EXACTLY 4 parallel subtasks for iteration "
            f"{state.iteration}. Each subtask must be independently completable "
            f"and non-overlapping with the others.\n\n"
            f"Focus: {focus}\n\n"
            f"Output 4 lines, one subtask per line, no numbering, no prose. "
            f"Each line is a complete instruction a subagent will follow."
        )
        try:
            text = generate(decomp_prompt)
        except Exception:
            return [
                f"Add or improve tests for the most critical untested module "
                f"(iteration {state.iteration})",
                f"Find and fix one security issue or unsafe pattern "
                f"(iteration {state.iteration})",
                f"Improve error handling in one user-facing surface "
                f"(iteration {state.iteration})",
                f"Improve docs/README for one weak area "
                f"(iteration {state.iteration})",
            ]
        lines = [ln.strip("- *0123456789. \t") for ln in text.splitlines()]
        lines = [ln for ln in lines if len(ln) > 20][:4]
        return lines if lines else [focus]

    def _run_subtask(sub: str, state: LoopState) -> dict:
        try:
            response = generate(sub)
            return {
                "subtask": sub,
                "response_hash": str(hash(response)),
                "ok": True,
            }
        except Exception as exc:
            return {"subtask": sub, "error": str(exc)}

    try:
        run_autofleet_loop(
            task=message,
            project_root=cwd,
            decompose=_decompose,
            run_one_subtask=_run_subtask,
            progress=_autonomous_progress,
            max_workers=4,
            iteration_delay_seconds=0.5,
        )
    except KeyboardInterrupt:
        renderer.console.print("\n[yellow]/autofleet cancelled. Sage is still running.[/yellow]")


def _run_autoorg_command(
    message: str | None,
    *,
    cwd: Path,
    router,
    model_id: str,
    temp: float,
    tokens: int,
    model_locked: bool,
) -> None:
    """REPL entry point for `/autoorg [message]`.

    Each iteration spawns one subagent per organisational role (product,
    staff engineer, QA, security, devops, docs) running in parallel.
    Repeats forever until cancelled.
    """
    from sage.core.autonomous import run_autoorg_loop, LoopState

    renderer.console.print(
        f"[bold cyan]/autoorg[/bold cyan] starting — "
        f"focus: [bold]{message or '(self-directed organisation-wide improvement)'}[/bold]"
    )
    renderer.console.print(
        "[dim]Stop with Ctrl-C. Or `touch ./.sage/AUTO-STOP` from another shell.[/dim]"
    )

    generate = _autonomous_generate_factory(router, model_id, temp, tokens, model_locked)

    def _run_role(role: str, prompt: str, state: LoopState) -> dict:
        try:
            response = generate(prompt)
            return {"role": role, "response_hash": str(hash(response)), "ok": True}
        except Exception as exc:
            return {"role": role, "error": str(exc)}

    try:
        run_autoorg_loop(
            task=message,
            project_root=cwd,
            run_one_role=_run_role,
            progress=_autonomous_progress,
            max_workers=6,
            iteration_delay_seconds=0.5,
        )
    except KeyboardInterrupt:
        renderer.console.print("\n[yellow]/autoorg cancelled. Sage is still running.[/yellow]")


def _route_to_principal_pipeline(
    user_input: str,
    base_out_dir: Path,
    router,
    model_id: str,
    temp: float,
    tokens: int,
    model_locked: bool,
    system_prompt: str | None,
    *,
    legacy_plans: bool = False,
    no_review: bool = False,
) -> dict | None:
    """Route a build-style prompt through the principal pipeline.

    If the prompt contains a single build task, generates ONE project at
    base_out_dir. If the prompt looks like multiple stacked build tasks
    (e.g. "Build a FastAPI app... Build a Go service... Build an Android
    app..."), generates EACH sub-task into its own labelled subfolder.

    Default path uses the new dynamic spec-driven builder. Pass
    `legacy_plans=True` to fall back to the hardcoded `plan_*()` plans
    in `principal_engineer` (rollback safety net).

    Returns a combined report dict, or None if the prompt isn't a build
    request at all.
    """
    from sage.core.dynamic_builder import build_project_dynamic
    from sage.core.principal_builder import BuildIncomplete, build_project_principal
    from sage.core.principal_engineer import (
        build_project,
        decompose_multi_build_request,
        looks_like_build_request,
    )

    if not looks_like_build_request(user_input):
        return None

    def _print_log(msg: str) -> None:
        if not renderer.is_clean():
            renderer.console.print(msg)

    def _build_progress(msg: str) -> None:
        if not renderer.is_clean():
            renderer.console.print(f"[dim]{msg}[/dim]")

    # ── Always save the user input to a text file alongside the build ──
    # Goes into a hidden .sage/ subdir so the project root stays clean —
    # sage scaffolds INTO the user's repo without cluttering it with
    # internal artifacts.
    import time
    base_out_dir = base_out_dir.resolve()
    base_out_dir.mkdir(parents=True, exist_ok=True)
    sage_dir = base_out_dir / ".sage"
    sage_dir.mkdir(parents=True, exist_ok=True)
    ts = time.strftime("%Y%m%d-%H%M%S")
    saved_input = sage_dir / f"INPUT-{ts}.txt"
    saved_input.write_text(user_input, encoding="utf-8")
    if len(user_input) >= 1500:
        renderer.console.print(
            f"[cyan]Saved your {len(user_input):,}-char input to "
            f"{saved_input}[/cyan]"
        )

    # Auto-swap to a faster local model if the current one is too slow for
    # the build pipeline's volume of LLM calls.
    effective_model, swap_reason = _pick_build_model(model_id)
    if swap_reason:
        _print_log(f"[yellow]{swap_reason}[/yellow]")

    # Extend ollama timeout floor for build mode — per-file LLM calls on a
    # large local model can run 5+ min. Don't lower an existing higher value.
    _existing_timeout = os.environ.get("SAGE_OLLAMA_TIMEOUT", "")
    try:
        if not _existing_timeout or float(_existing_timeout) < 1200:
            os.environ["SAGE_OLLAMA_TIMEOUT"] = "1200"
    except ValueError:
        os.environ["SAGE_OLLAMA_TIMEOUT"] = "1200"

    def _generate(p: str) -> str:
        messages = _build_simple_qa_messages(p, system_prompt=system_prompt)
        res = router.generate(
            messages, effective_model, temp, tokens, lock_provider=False
        )
        if res and (res.strip().startswith("Error:") or "invalid argument values" in res.lower()):
            raise ValueError(res.strip())
        return res

    sub_tasks = decompose_multi_build_request(user_input)
    base_out_dir = base_out_dir.resolve()

    def _run_build(task: str, out_dir: Path) -> dict:
        """Dispatch to the principal-grade builder or legacy fallback."""
        if legacy_plans:
            return build_project(task, out_dir, _generate, progress=_build_progress)
        # Default: principal builder (bootstrap + architecture + multi-file
        # features + review pass + verify loop). Replaces the older
        # build_project_dynamic which is retained for its test surface.
        try:
            report = build_project_principal(
                task, out_dir, _generate, progress=_build_progress,
                enable_review=not no_review,
            )
        except BuildIncomplete as exc:
            # The heal loop exhausted its retries with install or tests
            # still failing. Surface a clear failure to the user — DO NOT
            # report this as a successful build.
            renderer.console.print(
                f"[red]✗ Build failed after heal loop: {exc}[/red]\n"
                f"[yellow]See {out_dir}/.sage/BUILD_REPORT.json for details. "
                f"Sage refused to declare success on a non-installing project.[/yellow]"
            )
            report = exc.report
        return {
            "stack": (
                f"{report.stack.get('frontend') or 'none'} + "
                f"{report.stack.get('backend') or 'none'}"
            ),
            "out_dir": report.out_dir,
            "files": [{"path": p, "score": None} for p in [report.title]],
            "file_count": report.file_count,
            "template_count": 0,
            "llm_count": report.file_count,
            "integrity_fixes": 0,
            "lint_fixes": 0,
            "review_failures": sum(
                1 for s in report.review_scores.values() if s < 7.0
            ),
            "install_ok": report.install_ok,
            "build_ok": report.build_ok,
            "runs_ok": report.runs_ok,
            "tests_ok": report.tests_ok,
            "stuck_features": report.stuck_features,
            "feature_count": report.feature_count,
            "bootstrap_results": report.bootstrap_results,
            "review_scores": report.review_scores,
        }

    if len(sub_tasks) == 1:
        _print_log(
            f"[bold]Build mode[/bold] → {base_out_dir} "
            f"({'legacy plans' if legacy_plans else 'dynamic'})"
        )
        report = _run_build(sub_tasks[0][1], base_out_dir)
        if legacy_plans:
            _print_log(
                f"[green]Generated {len(report['files'])} files "
                f"({report['template_count']} from templates, "
                f"{report['llm_count']} from LLM, "
                f"{report.get('integrity_fixes', 0)} integrity fixes, "
                f"{report.get('lint_fixes', 0)} lint fixes)[/green]"
            )
        else:
            _print_log(
                f"[green]Generated {report['file_count']} files across "
                f"{report['feature_count']} features. "
                f"install_ok={report['install_ok']} build_ok={report['build_ok']} runs_ok={report['runs_ok']} tests_ok={report['tests_ok']}"
                f"{' STUCK=' + ','.join(report['stuck_features']) if report['stuck_features'] else ''}"
                "[/green]"
            )
        _print_log(f"Project at: [cyan]{report['out_dir']}[/cyan]")
        return report

    _print_log(
        f"[bold]Build mode[/bold] → {len(sub_tasks)} sub-projects under {base_out_dir}"
    )
    base_out_dir.mkdir(parents=True, exist_ok=True)
    combined: dict = {
        "stack": "multi",
        "out_dir": str(base_out_dir),
        "sub_projects": [],
        "files": [],
        "template_count": 0,
        "llm_count": 0,
        "integrity_fixes": 0,
        "lint_fixes": 0,
        "review_failures": 0,
    }
    for idx, (label, sub_task) in enumerate(sub_tasks, start=1):
        sub_dir = base_out_dir / f"{idx:02d}-{label}"
        _print_log(f"\n[bold cyan]── Project {idx}/{len(sub_tasks)}: {label}[/bold cyan]")
        try:
            report = _run_build(sub_task, sub_dir)
        except Exception as exc:
            renderer.warning(f"Project {idx} ({label}) failed: {exc}")
            combined["sub_projects"].append(
                {"label": label, "out_dir": str(sub_dir), "error": str(exc)}
            )
            continue
        file_count = report.get("file_count", len(report.get("files", [])))
        combined["sub_projects"].append(
            {
                "label": label,
                "stack": report["stack"],
                "out_dir": report["out_dir"],
                "file_count": file_count,
            }
        )
        if isinstance(report.get("files"), list):
            combined["files"].extend(report["files"])
        for key in ("template_count", "llm_count", "integrity_fixes",
                    "lint_fixes", "review_failures"):
            combined[key] += report.get(key, 0)
        _print_log(
            f"[green]  ✓ {label}: {file_count} files at {report['out_dir']}[/green]"
        )

    _print_log(
        f"\n[bold green]All {len(sub_tasks)} projects generated under {base_out_dir}[/bold green]"
    )
    return combined


def _get_single_turn_agent_timeout(provider_name: str) -> float:
    """Return a user-friendly timeout for hidden non-stream agent turns."""
    return _SINGLE_TURN_AGENT_TIMEOUTS.get(provider_name, 60.0)


def _run_callable_with_timeout(
    fn: Callable[[], str],
    timeout_seconds: float,
    timeout_message: str,
) -> str:
    """Run a blocking callable with an optional timeout.

    timeout_seconds <= 0 disables the timeout completely (wait forever).
    """
    if timeout_seconds <= 0:
        # No timeout — call directly and wait as long as needed
        return fn()

    if (
        hasattr(signal, "SIGALRM")
        and threading.current_thread() is threading.main_thread()
    ):
        previous_handler = signal.getsignal(signal.SIGALRM)

        def _handle_timeout(_signum: int, _frame: Any) -> None:
            raise renderer.StreamingTimeoutError(timeout_message)

        try:
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, timeout_seconds)
            return fn()
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, previous_handler)

    result: dict[str, str] = {}
    error: dict[str, Exception] = {}
    done = threading.Event()

    def _runner() -> None:
        try:
            result["value"] = fn()
        except Exception as exc:  # pragma: no cover - exercised via caller behavior
            error["exc"] = exc
        finally:
            done.set()

    thread = threading.Thread(target=_runner, daemon=True)
    thread.start()
    if not done.wait(timeout_seconds):
        raise renderer.StreamingTimeoutError(timeout_message)
    if "exc" in error:
        raise error["exc"]
    return result["value"]


def _should_ground_ask_response(prompt: str) -> bool:
    """Determine if a prompt in ask mode needs grounding (file reads).

    P1-1: If the prompt references specific files or codebase content,
    the response should be grounded by actually reading those files.

    Args:
        prompt: The user's input prompt

    Returns:
        True if response should be grounded with file reads, False otherwise
    """
    prompt_lower = prompt.lower()

    # Patterns that indicate file/code grounding is needed
    grounding_patterns = [
        # Explicit file references
        r"(?:read|look at|examine|check|analyze|review)\s+\S+\.\w+",  # "read main.py"
        r"\b\w+\.(?:py|js|ts|java|go|rb|rs|cpp|c|h|md|json|yaml|yml|toml)\b",  # File extensions
        # Codebase references
        r"in\s+(?:the\s+)?(?:codebase|project|repo|repository)",
        r"(?:this|the|our)\s+(?:codebase|project|code)",
        # Function/class references that need verification
        r"what\s+does\s+(?:the\s+)?(?:\w+\s+)?(?:function|method|class)\s+\w+\s+do",
        r"how\s+does\s+(?:\w+\s+){0,2}work\s+(?:in|within|inside)",
        # Request to read specific things
        r"(?:tell me|explain|describe)\s+what\s+(?:is\s+in|happens in)\s+",
    ]

    for pattern in grounding_patterns:
        if re.search(pattern, prompt_lower):
            return True

    return False


def _is_investigation_only_response(response: str) -> bool:
    """True when the response is still gathering evidence rather than making findings.

    Some weaker models prepend a short plan before issuing valid READ:/SEARCH:/RUN:
    commands. If the response contains real tool commands and no substantive
    findings yet, we should let the tools execute instead of rejecting it as an
    incomplete analysis list.
    """
    response = renderer.normalize_tool_command_syntax(response)
    has_executable_tool_commands = bool(
        re.search(r"^\s*(READ|SEARCH|RUN):\s*\S", response, re.MULTILINE)
    )
    if not has_executable_tool_commands:
        return False
    if "FILE:" in response:
        return False

    response_lower = response.lower()

    analysis_claim_patterns = [
        "after analyzing the",
        "after reviewing the",
        "after examining the",
        "i found these",
        "i identified these",
        "my analysis shows",
        "the analysis reveals",
        "i've identified",
        "i have identified",
    ]
    if any(pattern in response_lower for pattern in analysis_claim_patterns):
        return False

    if re.search(r"\bP[0-3]\b", response):
        return False

    if re.search(r"[a-z_][a-z0-9_/]*\.(?:py|js|ts|go|java|cpp|c|h|rb|php|rs|md):\d+", response):
        return False

    # Distinguish a numbered investigation plan from numbered findings.
    numbered_items = re.findall(r"^\s*\d+[.)\]]\s+(.+)$", response, re.MULTILINE)
    if numbered_items:
        finding_markers = (
            "issue",
            "problem",
            "bug",
            "risk",
            "improvement",
            "recommend",
            "fix",
            "refactor",
            "optimiz",
            "vulnerab",
            "perf",
            "maintain",
        )
        if any(
            any(marker in item.lower() for marker in finding_markers) for item in numbered_items
        ):
            return False

    return True


def _validate_context_gathering(
    response: str, files_read: list[str], is_analysis_request: bool
) -> tuple[bool, str]:
    """Validate that model gathered context when claiming it lacks info.

    FAIL-CLOSED: This validation is strict. When the model admits uncertainty,
    it must NOT then proceed to fabricate concrete recommendations.

    Args:
        response: The model's response text
        files_read: List of files that were actually read
        is_analysis_request: Whether this was an analysis request

    Returns:
        Tuple of (is_valid, reason)
    """
    if not is_analysis_request:
        return True, ""

    response_lower = response.lower()
    has_executable_tool_commands = bool(
        re.search(r"^\s*(READ|SEARCH|RUN):\s*\S", response, re.MULTILINE)
    )
    num_recommendations = len(re.findall(r"^\s*\d+[.)\]]\s+", response, re.MULTILINE))
    analysis_claim_patterns = [
        "after analyzing the",
        "after reviewing the",
        "after examining the",
        "i found these",
        "i identified these",
        "my analysis shows",
        "the analysis reveals",
        "i've identified",
        "i have identified",
    ]
    claims_analysis = any(pattern in response_lower for pattern in analysis_claim_patterns)

    # Investigation-first responses are valid for read-only analysis, even before
    # any READ actually executes. This lets the runtime accept real tool commands
    # instead of rejecting the model for gathering context.
    if _is_investigation_only_response(response):
        return True, ""

    # Phrases indicating lack of context
    no_context_phrases = [
        "no file references available",
        "without prior context",
        "cannot provide specific",
        "lack of context",
        "without reading",
        "without analyzing",
        "no context",
        "insufficient information",
        "without reading the actual",
        "i would need to",
        "i cannot proceed without",
        "need more information",
        "cannot determine without",
        # P1-B: Additional uncertainty patterns for fail-closed
        "don't have access to",
        "do not have access to",
        "haven't seen the",
        "have not seen the",
        "without access to",
        "unable to view",
        "cannot view the",
    ]

    claims_no_context = any(phrase in response_lower for phrase in no_context_phrases)

    if claims_no_context and len(files_read) == 0:
        # Check which specific phrase was found for better error message
        found_phrase = next(
            (phrase for phrase in no_context_phrases if phrase in response_lower), "lack of context"
        )
        return False, f"Response claimed lack of context ('{found_phrase}') but no files read"

    # FAIL-CLOSED: Detect "proceed by assuming" pattern - this is hallucination
    assumption_patterns = [
        "proceed by assuming",
        "will assume",
        "assuming the",
        "let me assume",
        "i'll assume",
        "based on assumptions",
        "without actual context",
        "cannot execute",
        "cannot perform",
        "unable to execute",
        "cannot read the",
        "cannot access the",
        # P1-3: Additional patterns for fail-closed grounding
        "based on my understanding",
        "based on common patterns",
        "based on typical",
        "based on general",
        "in my experience",
        "generally speaking",
        "typically this would",
    ]
    makes_assumptions = any(pattern in response_lower for pattern in assumption_patterns)
    if makes_assumptions:
        found_pattern = next((p for p in assumption_patterns if p in response_lower), "assumptions")
        return False, (
            f"Response contains assumption-based reasoning ('{found_pattern}'). "
            "Do NOT assume or fabricate. Use READ: and SEARCH: commands to get ACTUAL context."
        )

    # P1-B: Detect unsupported claims of analysis
    if claims_analysis and len(files_read) == 0:
        found_pattern = next(
            (p for p in analysis_claim_patterns if p in response_lower), "analysis claim"
        )
        return False, (
            f"Response claims analysis ('{found_pattern}') but no files were read. "
            "You must use READ: commands to actually analyze files before making claims."
        )

    # FAIL-CLOSED: Count recommendations vs files read
    # STRICT: Any numbered list without file reads is suspect
    # P1-B: Lowered threshold - ANY significant list without file reads is suspect
    if num_recommendations >= 3 and len(files_read) == 0:
        return False, (
            f"Generated {num_recommendations} recommendations but read ZERO files. "
            "You MUST use READ: commands to examine actual code before making recommendations. "
            "Start with: READ: <relevant_file.py>"
        )

    if num_recommendations >= 20 and len(files_read) < 3:
        return False, (
            f"Generated {num_recommendations} recommendations but only read {len(files_read)} files. "
            "Large recommendation lists require reading multiple files first."
        )

    if num_recommendations >= 50 and len(files_read) < 5:
        return False, (
            f"Generated {num_recommendations} recommendations but only read {len(files_read)} files. "
            "Very large recommendation lists require substantial file reading."
        )

    # FAIL-CLOSED: Detect hallucinated file paths in recommendations
    # If response mentions specific file paths that weren't read, it's hallucinating
    mentioned_files = re.findall(r"[\w/]+\.(?:py|js|ts|go|java|rs|c|cpp|h)\b", response)
    if mentioned_files and len(files_read) == 0:
        # Mentions specific files but read nothing - likely hallucinating
        # Ignore files that only appear as actual READ: commands in an investigation step.
        commanded_files = set(
            re.findall(
                r"^\s*READ:\s*([\w./-]+\.(?:py|js|ts|go|java|rs|c|cpp|h))\s*$",
                response,
                re.MULTILINE,
            )
        )
        unique_mentioned = set(mentioned_files) - commanded_files
        if len(unique_mentioned) > 3:  # Multiple specific files mentioned
            return False, (
                f"Response mentions {len(unique_mentioned)} specific files but no files were read. "
                "Use READ: commands to verify file contents before referencing them."
            )

    return True, ""


def _validate_readonly_mode(
    response: str, user_request: str, is_analysis_request: bool
) -> tuple[bool, str]:
    """Validate that model respects read-only mode for analysis requests.

    Args:
        response: The model's response text
        user_request: The original user request
        is_analysis_request: Whether this is a read-only analysis request

    Returns:
        Tuple of (is_compliant, reason)
    """
    if not is_analysis_request:
        return True, ""

    # Imperative verbs indicating implementation (not analysis)
    implementation_verbs = [
        r"\b(implement|create|build|develop|add|write|code|design|construct)\b",
    ]

    # Check for imperative implementation language
    response_lower = response.lower()

    # Extract numbered list items
    item_pattern = r"^\s*\d+\.\s+(.+)$"
    items = re.findall(item_pattern, response, re.MULTILINE)

    if not items:
        return True, ""

    # Check if response has specific file references (file.py:line_number)
    # If yes, implementation verbs are OK as recommendations with context
    file_reference_pattern = r"[a-z_][a-z0-9_/]*\.(py|js|ts|go|java|cpp|c|h|rb|php|rs|md):\d+"
    has_file_references = bool(re.search(file_reference_pattern, response_lower))

    if has_file_references:
        # Has specific file:line references, so implementation verbs are recommendations not claims
        return True, ""

    # No file references - check for implementation verbs
    implementation_count = 0
    for item in items[:10]:
        item_lower = item.lower()
        for verb_pattern in implementation_verbs:
            if re.search(verb_pattern, item_lower):
                implementation_count += 1
                break

    # If majority of items use implementation verbs WITHOUT file references, it's not analysis
    if implementation_count >= len(items[:10]) * 0.6:
        return (
            False,
            "Response uses implementation language (implement/create/add) instead of analysis language for a read-only request",
        )

    return True, ""


def _validate_tool_usage_for_analysis(
    response: str, files_read: list[str], search_executed: bool, num_recommendations: int
) -> tuple[bool, str]:
    """Validate that analysis responses actually performed analysis.

    Args:
        response: The model's response text
        files_read: List of files that were read
        search_executed: Whether any SEARCH commands were executed
        num_recommendations: Number of recommendations in response

    Returns:
        Tuple of (is_valid, reason)
    """
    # If requesting many recommendations, should have read files
    min_files_for_recommendations = max(1, num_recommendations // 20)

    if num_recommendations >= 10 and len(files_read) == 0 and not search_executed:
        return (
            False,
            f"Requested {num_recommendations} recommendations but no files read - no analysis performed",
        )

    if num_recommendations >= 20 and len(files_read) < min_files_for_recommendations:
        return (
            False,
            f"Requested {num_recommendations} recommendations but only {len(files_read)} files read - insufficient analysis effort",
        )

    return True, ""


def _count_numbered_list_items(text: str) -> int:
    """Count numbered markdown-style list items in a response."""
    return len(re.findall(r"^\s*\d+[.)\]]\s+", text, re.MULTILINE))


def _looks_like_actionable_numbered_list(text: str, min_items: int = 3) -> bool:
    """Return True when a response looks like a usable numbered task/findings list."""
    return _count_numbered_list_items(text) >= min_items


def _collect_analysis_validation_violations(
    response: str,
    task_prompt: str,
    classification: _ClassifiedRequest,
    current_files_read: list[str],
) -> tuple[list[str], bool]:
    """Collect read-only analysis validation violations for synthesis-quality checks."""
    violations: list[str] = []
    investigation_only = _is_investigation_only_response(response)

    is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(response)
    if is_descriptive and not investigation_only:
        if "TOOL_REFUSAL" in mentioned_tools:
            violations.append(
                "CRITICAL: You falsely claimed tools cannot be executed. "
                "This is WRONG. READ:, SEARCH:, and RUN: commands WILL execute. "
                "Write actual tool commands instead of refusing."
            )
        else:
            violations.append(
                f"You described tools ({', '.join(mentioned_tools[:3])}) instead of executing them."
            )

    is_filler, repetition_score = _detect_repetitive_filler(response)
    if is_filler:
        violations.append(
            f"Your response contains repetitive template-based content (score: {repetition_score:.2f}). "
            "Provide specific, varied recommendations with real file citations."
        )

    if not investigation_only:
        is_valid_context, context_reason = _validate_context_gathering(
            response, current_files_read, is_analysis_request=True
        )
        if not is_valid_context:
            violations.append(
                f"Context gathering issue: {context_reason}. "
                "Use grounded repo evidence before making claims."
            )

    is_readonly_compliant, readonly_reason = _validate_readonly_mode(
        response, task_prompt, is_analysis_request=True
    )
    if not is_readonly_compliant:
        violations.append(
            f"Read-only mode violation: {readonly_reason}. "
            "This is an analysis request - use observation language, not implementation claims."
        )

    quantity_expected = classification.quantity_required or 0
    if quantity_expected > 0 and not investigation_only:
        is_valid_effort, effort_reason = _validate_tool_usage_for_analysis(
            response, current_files_read, False, quantity_expected
        )
        if not is_valid_effort:
            violations.append(
                f"Insufficient analysis effort: {effort_reason}. "
                f"For {quantity_expected} requested items, analyze more of the repo first."
            )

    if not investigation_only and _requires_grounded_file_citations(task_prompt, classification):
        grounded_refs = _extract_grounded_file_references(response, current_files_read)
        min_citations = 5 if classification.request_type == _RequestType.LIST_GENERATION else 3
        if len(grounded_refs) < min_citations:
            violations.append(
                "Grounded analysis requires explicit citations to real project files. "
                f"Only {len(grounded_refs)} verified file references were found; need at least {min_citations}. "
                "Reference actual files you examined, ideally with line numbers."
            )
        specific_repo_refs = [ref for ref in grounded_refs if "/" in ref or re.search(r":\d", ref)]
        if len(specific_repo_refs) < 2:
            violations.append(
                "Broad codebase analysis must cite specific subproject or source files, "
                "not only generic root-level metadata like README or package manifests. "
                "Reference at least two concrete repo paths, ideally with line numbers."
            )

    return violations, investigation_only


def _build_context_aware_validation_retry_prompt(
    *,
    task_prompt: str,
    cwd: Path,
    violations: list[str],
    current_files_read: list[str],
    is_analysis: bool,
) -> str:
    """Build a retry prompt that matches whether grounded evidence already exists."""
    from sage.main import _sample_workspace_paths
    violations_text = "\n".join(f"{i + 1}. {v}" for i, v in enumerate(violations))

    if is_analysis and current_files_read:
        sample_citations = ", ".join(sorted(current_files_read)[:5])
        return (
            "❌ YOUR PREVIOUS FINAL ANALYSIS WAS REJECTED - DO NOT REPEAT IT\n\n"
            f"WHAT WENT WRONG:\n{violations_text}\n\n"
            "You ALREADY have grounded evidence from verified file reads in this repo.\n"
            "Do NOT restart with READ:/SEARCH: commands unless you truly need one more missing fact.\n"
            "Instead, regenerate the FINAL analysis now.\n\n"
            "RULES:\n"
            "1. Output a grounded prioritized findings list.\n"
            "2. For each item, use `Evidence:`, `Impact:`, and `Recommendation:` lines.\n"
            "3. Cite real verified files, with line numbers when available from the evidence.\n"
            "4. Base every claim on gathered evidence only.\n"
            "5. Do NOT include FILE: blocks, code, tests, or implementation steps.\n"
            "6. Do NOT describe tools or plans.\n"
            f"7. Cite files such as: {sample_citations}\n\n"
            f"Original request: {task_prompt}"
        )

    if not is_analysis and current_files_read:
        sample_paths = ", ".join(sorted(current_files_read)[:5])
        return (
            "❌ YOUR PREVIOUS IMPLEMENTATION RESPONSE WAS REJECTED - DO NOT REPEAT IT\n\n"
            f"WHAT WENT WRONG:\n{violations_text}\n\n"
            "You ALREADY have verified workspace evidence from earlier READ:/SEARCH: commands.\n"
            "Do NOT ask the user to provide file contents, outputs, or permission to continue.\n"
            "Continue the implementation directly now.\n\n"
            "RULES:\n"
            "1. Use the verified files you already examined as your grounding.\n"
            "2. If behavior changes are needed, write failing tests FIRST using FILE: blocks.\n"
            "3. Then write the implementation using FILE: blocks.\n"
            "4. Add RUN: commands for the relevant tests.\n"
            "5. Do NOT answer with prose-only plans, assumptions, or requests for more context.\n"
            f"6. Verified files include: {sample_paths}\n\n"
            f"Original request: {task_prompt}"
        )

    retry_examples = (
        "\n".join(f"READ: {path}" for path in _sample_workspace_paths(cwd, 2))
        if _sample_workspace_paths(cwd, 2)
        else "SEARCH: *.py"
    )
    retry_right_example = (
        f"RIGHT: 'READ: {_sample_workspace_paths(cwd, 1)[0]}'\n\n"
        if _sample_workspace_paths(cwd, 1)
        else "RIGHT: 'SEARCH: *.py'\n\n"
    )
    return (
        f"❌ YOUR PREVIOUS RESPONSE WAS REJECTED - DO NOT REPEAT IT\n\n"
        f"WHAT WENT WRONG:\n{violations_text}\n\n"
        "═══════════════════════════════════════════════════════════\n"
        "CRITICAL: YOUR VERY FIRST LINE MUST BE A TOOL COMMAND\n"
        "═══════════════════════════════════════════════════════════\n\n"
        f"DO THIS NOW (copy exactly):\n{retry_examples}\n\n"
        "RULES YOU MUST FOLLOW:\n"
        "1. Start IMMEDIATELY with READ: or SEARCH: - NO introductory text\n"
        "2. Do NOT say 'I will read' - just write 'READ: filename'\n"
        "3. Do NOT say 'cannot execute' or 'assuming' - the commands WILL execute\n"
        "4. WAIT for file contents before making ANY recommendations\n"
        "5. Each recommendation must cite specific file:line numbers\n\n"
        "WRONG: 'I will investigate by reading the files...'\n"
        f"{retry_right_example}"
        f"Original request: {task_prompt}"
    )


def _extract_grounded_file_references(
    response: str,
    verified_files: list[str] | set[str],
) -> set[str]:
    """Return verified project files explicitly cited in the response."""
    normalized_verified = {
        path.strip().strip("`").lstrip("./")
        for path in verified_files
        if path and path.strip().strip("`").lstrip("./")
    }
    if not normalized_verified:
        return set()

    referenced: set[str] = set()
    for path in normalized_verified:
        escaped = re.escape(path)
        if re.search(rf"(?<![\w/.-])`?{escaped}`?(?::\d+|#L\d+)?(?![\w/.-])", response):
            referenced.add(path)

    basename_to_paths: dict[str, list[str]] = {}
    for path in normalized_verified:
        basename_to_paths.setdefault(Path(path).name, []).append(path)

    for basename, paths in basename_to_paths.items():
        if len(paths) != 1:
            continue
        escaped = re.escape(basename)
        if re.search(rf"(?<![\w/.-])`?{escaped}`?(?::\d+|#L\d+)?(?![\w/.-])", response):
            referenced.add(paths[0])

    return referenced


def _requires_grounded_file_citations(
    task_prompt: str,
    classification: _ClassifiedRequest | None,
) -> bool:
    """Return True when a read-only analysis response must cite verified files."""
    from sage.main import _should_seed_recursive_analysis_context
    if not classification or not classification.read_only:
        return False
    if classification.request_type not in {_RequestType.ANALYSIS, _RequestType.LIST_GENERATION}:
        return False
    return _should_seed_recursive_analysis_context(task_prompt, classification)


def _validate_analysis_response(
    response: str,
    user_request: str,
    files_read: list[str],
    search_executed: bool = False,
    num_recommendations: int = 0,
) -> tuple[bool, list[str]]:
    """Comprehensive validation of analysis response.

    Args:
        response: The model's response text
        user_request: The original user request
        files_read: List of files that were read
        search_executed: Whether any SEARCH commands were executed
        num_recommendations: Number of recommendations in response

    Returns:
        Tuple of (is_valid, list of violation messages)
    """
    violations = []

    # Extract number from user request if not provided
    if num_recommendations == 0:
        # Try to extract number from requests like "list 100 items"
        num_match = re.search(r"(\d+)\s+items?|list\s+(\d+)", user_request.lower())
        if num_match:
            num_recommendations = int(num_match.group(1) or num_match.group(2))

    # Check for tool description vs execution
    is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(response)
    if is_descriptive:
        violations.append(
            f"Model described tools ({', '.join(mentioned_tools)}) instead of executing them"
        )

    # Check for repetitive filler (also detect "... (N more items)" pattern)
    filler_placeholder = re.search(
        r"\.\.\.\s*\(\s*\d+\s+more\s+(?:similar\s+)?items?\s*\)", response.lower()
    )
    is_filler, repetition_score = _detect_repetitive_filler(response)
    if is_filler or filler_placeholder:
        if filler_placeholder:
            violations.append("Response contains filler placeholder instead of actual content")
        else:
            violations.append(
                f"Response contains repetitive filler content (repetition score: {repetition_score:.2f})"
            )

    # Check context gathering
    is_analysis = (
        "analyze" in user_request.lower()
        or "list" in user_request.lower()
        or "review" in user_request.lower()
    )
    context_valid, context_reason = _validate_context_gathering(response, files_read, is_analysis)
    if not context_valid:
        violations.append(context_reason)

    # Check read-only mode compliance
    readonly_valid, readonly_reason = _validate_readonly_mode(response, user_request, is_analysis)
    if not readonly_valid:
        violations.append(readonly_reason)

    # Check tool usage
    if num_recommendations > 0:
        tool_usage_valid, tool_usage_reason = _validate_tool_usage_for_analysis(
            response, files_read, search_executed, num_recommendations
        )
        if not tool_usage_valid:
            violations.append(tool_usage_reason)

    is_valid = len(violations) == 0
    return is_valid, violations


# =============================================================================
# Runtime Validation Integration
# =============================================================================


