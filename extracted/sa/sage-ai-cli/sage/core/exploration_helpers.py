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


def _build_prompt_reader(cwd: Path) -> Callable[[str], str]:
    """Build an input reader with arrow-key history when available.

    Uses prompt_toolkit in interactive terminals. Pastes are detected via
    `Keys.BracketedPaste`:
      - The actual text is stashed in a per-reader registry.
      - A compact placeholder `[Pasted text N characters]` is inserted
        into the visible buffer so the prompt stays clean and the user
        can keep typing after it.
      - When the user hits Enter, the reader expands every placeholder
        back to its real text before returning. Downstream code sees the
        full content; the terminal only ever displayed the placeholder.

    Falls back to Rich input in non-interactive/test environments.
    """
    from sage.core.session_helpers import _load_prompt_history
    if sys.stdin.isatty() and sys.stdout.isatty():
        try:
            import os
            # Suppress "WARNING: your terminal doesn't support cursor position requests (CPR)."
            # This often happens in environments like PyCharm, Warp, or pseudoterminals.
            os.environ["PROMPT_TOOLKIT_NO_CPR"] = "1"

            from prompt_toolkit import PromptSession
            from prompt_toolkit.history import InMemoryHistory
            from prompt_toolkit.key_binding import KeyBindings
            from prompt_toolkit.keys import Keys

            history = InMemoryHistory()
            for item in _load_prompt_history(cwd):
                text = (item.get("prompt") or "").strip()
                if text:
                    history.append_string(text)

            paste_registry: dict[str, str] = {}
            paste_fired_flag = [False]

            kb = KeyBindings()

            @kb.add(Keys.BracketedPaste)
            def _on_bracketed_paste(event) -> None:  # type: ignore[no-untyped-def]
                data = event.data or ""
                char_count = len(data)
                line_count = len(data.splitlines())
                # Tiny pastes (e.g. a URL, a single word) get inserted verbatim —
                # no placeholder needed because there's no display burden.
                if char_count < 200 and line_count <= 5:
                    event.current_buffer.insert_text(data)
                    return
                # Replace large pastes with a compact placeholder so the
                # prompt line stays uncluttered and the user can append.
                placeholder = f"[Pasted {line_count} lines]"
                paste_registry[placeholder] = data
                paste_fired_flag[0] = True

                try:
                    from pathlib import Path
                    import time
                    import random
                    pastes_dir = Path.home() / ".sage" / "pastes"
                    pastes_dir.mkdir(parents=True, exist_ok=True)
                    timestamp = int(time.time())
                    rand_id = random.randint(1000, 9999)
                    paste_file = pastes_dir / f"paste_{timestamp}_{rand_id}.txt"
                    paste_file.write_text(data, encoding="utf-8")
                except Exception:
                    pass

                event.current_buffer.insert_text(placeholder)

            session = PromptSession(
                history=history,
                key_bindings=kb,
                enable_open_in_editor=True,
            )

            def reader(prompt_text: str) -> str:
                paste_fired_flag[0] = False
                text = session.prompt(prompt_text)
                # Expand every placeholder back to its actual pasted text.
                if paste_registry and "[Pasted " in text:
                    for placeholder, real in list(paste_registry.items()):
                        if placeholder in text:
                            text = text.replace(placeholder, real)
                            del paste_registry[placeholder]
                return text

            reader.last_paste_fired = (  # type: ignore[attr-defined]
                lambda: paste_fired_flag[0]
            )
            return reader
        except Exception as e:  # pragma: no cover
            logger.debug(f"PromptSession initialization failed: {e}")  # pragma: no cover
            pass  # pragma: no cover
    return lambda prompt_text: renderer.console.input(prompt_text)


def _build_cli_task_todos(
    read_only: bool, plan: ExecutionPlan | None = None, is_informational: bool = False
) -> list[dict]:
    """Build the bottom-dock todo list for the main SAGE task loop."""
    if plan and plan.tasks:
        return [
            {"key": task.id, "content": task.description, "status": task.status}
            for task in plan.tasks
        ]

    # Priority: Informational tasks (2 steps)
    if is_informational:
        return [
            {
                "key": "analyze",
                "content": "Analyzing informational request...",
                "status": "in_progress",
            },
            {"key": "respond", "content": "Synthesizing general knowledge...", "status": "pending"},
        ]

    # Read-only analysis (3 steps)
    if read_only:
        return [
            {
                "key": "analyze",
                "content": "Analyzing request and repository",
                "status": "in_progress",
            },
            {"key": "respond", "content": "Synthesizing final findings", "status": "pending"},
        ]
    return [
        {"key": "analyze", "content": "Analyzing task...", "status": "in_progress"},
        {"key": "plan", "content": "Decomposing into subtasks", "status": "pending"},
        {"key": "execute", "content": "Executing implementation", "status": "pending"},
    ]


def _set_cli_task_stage(todos: list[dict], key: str) -> list[dict]:
    """Advance the dock todo list to the requested stage."""
    if not any(todo.get("key") == key for todo in todos):
        return todos
    current_reached = False
    for todo in todos:
        todo_key = todo.get("key")
        if todo_key == key:
            todo["status"] = "in_progress"
            current_reached = True
        elif current_reached:
            if todo.get("status") != "completed":
                todo["status"] = "pending"
        else:
            todo["status"] = "completed"
    return todos


def _complete_cli_task_todos(todos: list[dict]) -> list[dict]:
    """Mark every dock todo as completed."""
    for todo in todos:
        todo["status"] = "completed"
    return todos


_STEP_PATTERNS = re.compile(
    r"""
    (?:^|\n)                          # Start of line
    (?:
        (?:\*{0,2})\s*                # Optional bold markers
        (?:step\s*)?                  # Optional "Step" prefix
        (\d+)                         # Step number
        [.):\-]\s*                    # Delimiter
        (?:\*{0,2})\s*               # Optional trailing bold
        (.+?)                         # Step description
        (?=\n|$)                      # End of line
    )
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _extract_steps_from_response(text: str) -> list[str]:
    """Parse a model response for a numbered step list.

    Returns step descriptions in order, or [] if no clear multi-step plan was found.
    Only triggers when the model emits ≥2 consecutive numbered items so we don't
    false-positive on stray numbered sentences.
    """
    matches = _STEP_PATTERNS.findall(text)
    if len(matches) < 2:
        return []

    # Verify the numbers are actually sequential starting from 1
    try:
        nums = [int(m[0]) for m in matches]
    except (ValueError, IndexError):
        return []

    if nums[0] != 1:
        return []

    # Accept if at least the first few numbers are sequential (model may add extras)
    sequential = all(nums[i] == nums[i - 1] + 1 for i in range(1, min(len(nums), 5)))
    if not sequential:
        return []

    return [m[1].strip().rstrip("*").strip() for m in matches]


def _scan_project_context_with_files(
    cwd: Path,
    max_tree: int = 40,
    max_config_chars: int = 400,
    max_source_files: int = 10,
    max_source_lines: int = 60,
) -> tuple[str, list[str]]:
    """Scan the project directory and return compact context plus previewed files.

    Reads the file tree, detects languages, git status, config files,
    and the first N lines of key source files for deep codebase context.
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
    ext_map = {
        ".py": "Python",
        ".js": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript/React",
        ".jsx": "React",
        ".rs": "Rust",
        ".go": "Go",
        ".java": "Java",
        ".c": "C",
        ".cpp": "C++",
        ".rb": "Ruby",
        ".sh": "Shell",
        ".html": "HTML",
        ".css": "CSS",
        ".json": "JSON",
        ".yaml": "YAML",
        ".yml": "YAML",
        ".toml": "TOML",
        ".md": "Markdown",
    }

    all_files: list[str] = []
    source_files: list[Path] = []
    lang_counts: dict[str, int] = {}

    # Faster scanning: use git ls-files if possible, otherwise use a limited walk
    is_git = False
    try:
        git_check = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(cwd),
            capture_output=True,
            text=True,
            timeout=2,
            stderr=subprocess.DEVNULL,
        )
        is_git = git_check.returncode == 0
    except Exception:
        pass

    if is_git:
        try:
            git_files = subprocess.check_output(
                ["git", "ls-files"], cwd=str(cwd), text=True, timeout=5, stderr=subprocess.DEVNULL
            ).splitlines()
            for f_str in git_files:
                p = cwd / f_str
                if not p.is_file():
                    continue  # pragma: no cover
                all_files.append(f_str)
                ext = p.suffix.lower()
                if ext in ext_map:
                    lang = ext_map[ext]
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1
                if ext in source_exts:
                    source_files.append(p)
        except Exception:
            is_git = False  # Fallback to manual scan if git ls-files fails

    if not is_git:
        # Manual scan with early directory skipping
        for root, dirs, files in os.walk(cwd):
            # Skip hidden and excluded directories
            dirs[:] = [d for d in dirs if not d.startswith(".") and d not in skip_dirs]
            root_path = Path(root)
            for f in files:
                if f.startswith("."):
                    continue
                p = root_path / f
                try:
                    rel = p.relative_to(cwd)
                except ValueError:  # pragma: no cover
                    continue  # pragma: no cover

                f_str = rel.as_posix()
                all_files.append(f_str)
                ext = p.suffix.lower()
                if ext in ext_map:
                    lang = ext_map[ext]
                    lang_counts[lang] = lang_counts.get(lang, 0) + 1
                if ext in source_exts:
                    source_files.append(p)

                # Safety limit for non-git repos
                if len(all_files) > 2000:
                    break
            if len(all_files) > 2000:
                break

    sorted_langs = sorted(lang_counts.items(), key=lambda x: -x[1])
    primary_lang = sorted_langs[0][0] if sorted_langs else "Unknown"

    # Git context
    git_info = ""
    try:
        branch = subprocess.check_output(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            text=True,
            cwd=str(cwd),
            timeout=5,
            stderr=subprocess.DEVNULL,
        ).strip()
        status = subprocess.check_output(
            ["git", "status", "--short"],
            text=True,
            cwd=str(cwd),
            timeout=5,
            stderr=subprocess.DEVNULL,
        ).strip()
        git_info = f"Branch: {branch}"
        if status:
            git_info += f"\nChanged:\n{status}"
    except Exception:
        git_info = "(not a git repo)"

    # Config files
    config_names = [
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "requirements.txt",
        "Makefile",
        "Dockerfile",
    ]
    configs = []
    for cf in config_names:
        cf_path = cwd / cf
        if cf_path.exists():
            try:
                configs.append(f"--- {cf} ---\n{cf_path.read_text('utf-8')[:max_config_chars]}")
            except Exception as e:
                logger.debug(f"Failed to read config file {cf}: {e}")
                pass

    # Read key source files for deep codebase understanding
    source_previews: list[str] = []
    previewed_files: list[str] = []
    # Prioritize entry points, main files, and smaller files
    priority_names = {"main", "app", "index", "cli", "__init__", "server", "config"}

    def _sort_key(p: Path) -> tuple:
        stem = p.stem.lower()
        is_priority = 0 if stem in priority_names else 1
        return (is_priority, p.stat().st_size)

    try:
        source_files.sort(key=_sort_key)
    except OSError:
        pass

    for sf in source_files[:max_source_files]:
        try:
            rel = sf.relative_to(cwd)
            lines = sf.read_text("utf-8", errors="replace").splitlines()[:max_source_lines]
            if lines:
                previewed_files.append(rel.as_posix())
                numbered = "\n".join(f"{i + 1:>4}| {l}" for i, l in enumerate(lines))
                source_previews.append(f"--- {rel} (first {len(lines)} lines) ---\n{numbered}")
        except Exception:
            pass

    parts = [
        f"CWD: {cwd}",
        f"Lang: {primary_lang} | {', '.join(f'{l}({n})' for l, n in sorted_langs[:5])}",
        f"Git: {git_info}",
        f"Files ({len(all_files)}):",
    ]
    for f in all_files[:max_tree]:
        parts.append(f"  {f}")
    if len(all_files) > max_tree:
        parts.append(f"  ... +{len(all_files) - max_tree} more")
    if configs:
        parts.append("Config:")
        parts.extend(configs)
    if source_previews:
        parts.append("\nKey source files:")
        parts.extend(source_previews)
    return "\n".join(parts), previewed_files


def _scan_project_context(
    cwd: Path,
    max_tree: int = 40,
    max_config_chars: int = 400,
    max_source_files: int = 10,
    max_source_lines: int = 60,
) -> str:
    """Scan the project directory and return a compact context string."""
    context, _ = _scan_project_context_with_files(
        cwd,
        max_tree=max_tree,
        max_config_chars=max_config_chars,
        max_source_files=max_source_files,
        max_source_lines=max_source_lines,
    )
    return context


def _iter_full_analysis_file_paths(cwd: Path) -> list[str]:
    """Return repo files that broad read-only analysis should inspect.

    Includes relevant dotfiles and hidden project directories like `.github`,
    while excluding generated, virtualenv, VCS, and binary-heavy paths.
    """
    excluded_dirs = {
        ".git",
        ".venv",
        "venv",
        "node_modules",
        "__pycache__",
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
        ".sage",
        "conversation_logs",
        "logs",
        "tmp",
        "temp",
    }
    excluded_suffixes = {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".avif",
        ".pdf",
        ".zip",
        ".gz",
        ".tar",
        ".db",
        ".sqlite",
        ".sqlite3",
        ".so",
        ".dylib",
        ".dll",
        ".a",
        ".o",
        ".pyc",
        ".class",
        ".jar",
        ".ico",
        ".icns",
        ".mp3",
        ".mp4",
        ".mov",
        ".wav",
        ".woff",
        ".woff2",
        ".ttf",
        ".otf",
        ".eot",
    }
    allowed_hidden_dirs = {
        ".github",
        ".claude",
    }
    always_include_names = {
        "Dockerfile",
        "Makefile",
        "README",
        "README.md",
        "README.rst",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
        "pnpm-lock.yaml",
        "yarn.lock",
        "Cargo.toml",
        "go.mod",
        "requirements.txt",
        "requirements-dev.txt",
        "setup.py",
        "setup.cfg",
        ".gitignore",
        ".gitattributes",
        ".editorconfig",
        ".env.example",
    }
    likely_text_suffixes = {
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
        ".h",
        ".hpp",
        ".rb",
        ".sh",
        ".zsh",
        ".bash",
        ".md",
        ".rst",
        ".txt",
        ".json",
        ".toml",
        ".yaml",
        ".yml",
        ".ini",
        ".cfg",
        ".conf",
        ".css",
        ".html",
        ".sql",
        ".graphql",
        ".gql",
        ".prisma",
        ".svg",
    }

    file_paths: list[str] = []
    # Optimization: Use safe_walk instead of rglob("*") to avoid hangs in non-git repos
    from sage.core.project import safe_walk

    for path in safe_walk(cwd, skip_dirs=excluded_dirs, include_hidden=True):
        if not path.is_file():
            continue
        try:
            rel = path.relative_to(cwd)
        except ValueError:
            continue

        # Check for hidden directories that aren't explicitly allowed
        hidden_dirs = [
            part
            for part in rel.parts[:-1]
            if part.startswith(".") and part not in allowed_hidden_dirs
        ]
        if hidden_dirs:
            continue

        # skip_dirs is already handled by safe_walk's implementation,
        # but we double check for parts in excluded_dirs just in case of nested exclusions
        if any(part in excluded_dirs for part in rel.parts):
            continue  # pragma: no cover

        if path.suffix.lower() in excluded_suffixes:
            continue
        try:
            if path.stat().st_size > 200_000:
                continue
        except OSError:
            continue

        if path.name in always_include_names or path.suffix.lower() in likely_text_suffixes:
            file_paths.append(rel.as_posix())

    return sorted(file_paths)


def _collect_full_readonly_file_coverage(
    cwd: Path,
    *,
    is_local: bool,
    files_read: set[str],
    execution_ledger: Any,
) -> str:
    """Read a prioritized slice of eligible project files for broad analysis.

    Small projects are still covered exhaustively. Larger repositories are capped
    to keep local-model analysis responsive instead of stalling before the model
    can synthesize findings.
    """
    from sage.cli_core import _record_file_read
    from sage.core.tools import ToolCall, ToolType

    all_paths = _iter_full_analysis_file_paths(cwd)
    if not all_paths:
        return ""  # pragma: no cover

    per_file_line_limit = 6 if is_local else 10
    max_total_chars = 28_000 if is_local else 55_000
    max_read_files = 180 if is_local else 320
    included_sections: list[str] = []
    omitted_paths: list[str] = []
    total_chars = 0
    read_count = 0

    priority_dir_names = {
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
        ".github",
    }
    priority_file_names = {
        "README.md",
        "README.rst",
        "README",
        "pyproject.toml",
        "package.json",
        "Cargo.toml",
        "go.mod",
        "requirements.txt",
        "Dockerfile",
        "Makefile",
        ".gitignore",
    }

    def _excerpt_priority(path_str: str) -> tuple[int, int, str]:
        path = Path(path_str)
        parts = path.parts
        name = path.name
        suffix = path.suffix.lower()
        rank = 5
        if name in priority_file_names:
            rank = 0
        elif any(part in priority_dir_names for part in parts):
            rank = 1
        elif suffix in {".py", ".js", ".ts", ".tsx", ".jsx", ".rs", ".go", ".java", ".sh"}:
            rank = 2  # pragma: no cover
        elif suffix in {".md", ".toml", ".json", ".yaml", ".yml", ".ini", ".cfg", ".conf"}:
            rank = 3  # pragma: no cover
        elif any(part.startswith(".") for part in parts if part not in {".github"}):
            rank = 6  # pragma: no cover
        return (rank, len(parts), path_str)

    excerpt_order = sorted(all_paths, key=_excerpt_priority)
    selected_paths = excerpt_order[:max_read_files]
    truncated_count = max(0, len(all_paths) - len(selected_paths))

    for rel_path in selected_paths:
        content = _read_file_context(rel_path, cwd, max_lines=per_file_line_limit)
        if content is None:
            continue
        read_count += 1
        if rel_path not in files_read:
            files_read.add(rel_path)
            _record_file_read(rel_path, success=True)
            execution_ledger.record_execution(
                ToolCall(
                    tool_type=ToolType.READ,
                    arguments={"path": rel_path},
                    validated=True,
                ),
                success=True,
            )

    for rel_path in selected_paths:
        content = _read_file_context(rel_path, cwd, max_lines=per_file_line_limit)
        if content is None:
            continue
        candidate = f"--- {rel_path} ---\n{content}\n"
        if total_chars + len(candidate) <= max_total_chars:
            included_sections.append(candidate)
            total_chars += len(candidate)
        else:
            omitted_paths.append(rel_path)  # pragma: no cover

        parts = [
            "FULL FILE COVERAGE:",
            (
                "SAGE recursively READ a prioritized set of eligible text/config/source/test files "
                f"under the current project root. Total files read: {read_count}."
            ),
            (
                "Excerpts below prioritize likely entrypoints, config, CI, tests, and core source files. "
                "Additional verified files are listed afterward."
            ),
        ]
    if truncated_count:
        parts.append(  # pragma: no cover
            "Coverage was capped for responsiveness on this broad analysis request. "
            f"Verified prioritized files: {read_count} of {len(all_paths)} eligible files."
        )
    if included_sections:
        parts.append("Included file excerpts:")
        parts.extend(included_sections)
    if omitted_paths:
        parts.append(  # pragma: no cover
            "Additional files were also READ by SAGE but are listed without content here due "  # pragma: no cover
            "prompt budget limits:"  # pragma: no cover
        )  # pragma: no cover
        parts.extend(f"- {path}" for path in omitted_paths)  # pragma: no cover
    return "\n".join(parts)


def _build_verified_file_coverage_summary(
    verified_files: set[str] | list[str],
    *,
    max_files: int = 40,
) -> str:
    """Build a compact summary of verified file reads for synthesis prompts."""
    normalized = sorted({str(path).strip() for path in verified_files if str(path).strip()})
    if not normalized:
        return ""

    shown = normalized[:max_files]
    parts = [
        "VERIFIED FILE COVERAGE SUMMARY:",
        f"SAGE already READ {len(normalized)} verified project files for this request.",
        "Use only these verified paths when citing repo-wide findings.",
        "Sample verified files:",
    ]
    parts.extend(f"- {path}" for path in shown)
    if len(normalized) > max_files:
        parts.append(f"- ... +{len(normalized) - max_files} more verified files")
    return "\n".join(parts)


def _build_seeded_readonly_synthesis_prompt(
    base_prompt: str,
    *,
    seeded_recursive_analysis_context: str,
    seeded_shell_inventory_context: str,
    seeded_full_file_coverage_context: str,
    verified_files: set[str] | list[str],
    is_local: bool,
) -> str:
    """Build a compact grounded synthesis prompt for read-only repo analysis.

    Local models benefit from smaller, code-heavy context. When SAGE already has
    recursive code previews plus a verified file list, omit verbose shell
    inventory to keep synthesis responsive.
    """
    seeded_parts: list[str] = []
    if seeded_recursive_analysis_context:
        seeded_parts.append(
            "## AUTO-COLLECTED RECURSIVE CODEBASE CONTEXT\n" f"{seeded_recursive_analysis_context}"
        )

    verified_file_summary = _build_verified_file_coverage_summary(
        verified_files,
        max_files=25 if is_local else 40,
    )

    include_shell_inventory = bool(
        seeded_shell_inventory_context
        and (not is_local or (not seeded_recursive_analysis_context and not verified_file_summary))
    )
    if include_shell_inventory:
        seeded_parts.append(
            "## AUTO-COLLECTED SHELL INVENTORY\n" f"{seeded_shell_inventory_context}"
        )

    if verified_file_summary:
        seeded_parts.append(verified_file_summary)
    elif seeded_full_file_coverage_context:
        seeded_parts.append(
            "## AUTO-COLLECTED FULL FILE COVERAGE\n" f"{seeded_full_file_coverage_context}"
        )

    if not seeded_parts:
        return base_prompt

    seeded_parts.append(
        "## FINAL ANALYSIS FORMAT RULES\n"
        "Output a numbered findings list only.\n"
        "Use this shape for each finding:\n"
        "1. <Short issue title>\n"
        "Evidence: <verified file paths; add line numbers when you have them>\n"
        "Impact: <why this matters>\n"
        "Recommendation: <what should change>\n\n"
        "Rules:\n"
        "- Keep claims tied to the verified files above.\n"
        "- Do not rely only on root metadata files like README.md, package.json, requirements.txt, or pyproject.toml.\n"
        "- Cite at least two concrete subproject or source paths across the whole response.\n"
        "- If a point is an inference, say so explicitly and name the file(s) it is based on.\n"
        "Do NOT include implementation steps, FILE: blocks, or tests."
    )

    return "\n\n".join(seeded_parts + [base_prompt])


def _build_grounded_analysis_failure_message(detail: str | None = None) -> str:
    """Return a user-facing fail-closed message for broad analysis requests."""
    fallback_detail = (
        "The model could not produce a validated, file-grounded analysis response in time. "
        "Try narrowing the request or switching to a stronger model."
    )
    return "## Could not complete grounded analysis\n\n" + (detail or fallback_detail)


def _is_actionable_analysis_path(path: str) -> bool:
    """Return True for repo-owned source paths that should drive broad analysis findings."""
    normalized = str(path).strip().lstrip("./")
    if not normalized:
        return False

    rel_path = Path(normalized)
    skip_parts = {
        ".git",
        ".hg",
        ".svn",
        ".venv",
        "venv",
        "env",
        "node_modules",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".ruff_cache",
        ".tox",
        ".nox",
        "dist",
        "build",
        "htmlcov",
        ".next",
        ".cache",
        "coverage",
        "target",
        "site-packages",
        "vendor",
        "third_party",
        "test-results",
    }
    if any(part in skip_parts or part.startswith(".") for part in rel_path.parts[:-1]):
        return False

    lower = normalized.lower()
    if lower.startswith("tests/") or "/tests/" in lower:
        return False
    if rel_path.name.startswith("test_"):
        return False
    if rel_path.name.startswith("."):
        return False
    return True


def _build_deterministic_readonly_analysis_fallback(
    task_prompt: str,
    cwd: Path,
) -> str | None:
    """Build a grounded broad-analysis fallback from SAGE's deterministic repo analyzers."""
    try:
        project_analysis = _analyze_project_structure(cwd)
        code_analysis = RepoCodeAnalyzer(cwd).analyze()
    except Exception as exc:
        logger.warning("Broad analysis fallback unavailable: %s", exc)
        return None

    findings: list[tuple[str, str, str, str]] = []
    seen_titles: set[str] = set()

    def add_finding(
        severity: str,
        title: str,
        evidence: str,
        recommendation: str,
    ) -> None:
        if title in seen_titles:
            return  # pragma: no cover
        findings.append((severity, title, evidence, recommendation))
        seen_titles.add(title)

    complexity_candidates = [
        (path, metrics)
        for path, metrics in code_analysis.complexity.items()
        if _is_actionable_analysis_path(path)
        and (metrics.lines_of_code >= 800 or metrics.cyclomatic_complexity >= 120)
    ]
    complexity_candidates.sort(
        key=lambda item: (
            item[1].cyclomatic_complexity,
            item[1].lines_of_code,
            item[1].functions,
            item[1].classes,
        ),
        reverse=True,
    )
    for path, metrics in complexity_candidates[:2]:
        severity = (
            "P1"
            if (metrics.lines_of_code >= 1500 or metrics.cyclomatic_complexity >= 250)
            else "P2"
        )
        add_finding(
            severity,
            f"Reduce the monolithic surface area in `{path}`",
            (
                f"`{path}` has {metrics.lines_of_code} non-blank lines, "
                f"{metrics.functions} top-level functions, {metrics.classes} classes, "
                f"and cyclomatic complexity {metrics.cyclomatic_complexity}."
            ),
            (
                "Split this file by responsibility so runtime orchestration, API handlers, "
                "or UI state do not keep accumulating in one hotspot."
            ),
        )

    error_candidates = [
        (file_path, line, message)
        for file_path, line, message in code_analysis.error_handling_issues
        if _is_actionable_analysis_path(file_path)
    ]
    if error_candidates:
        error_counts = Counter(file_path for file_path, _, _ in error_candidates)
        hottest_file, issue_count = error_counts.most_common(1)[0]
        first_line, first_message = next(
            (line, message)
            for file_path, line, message in error_candidates
            if file_path == hottest_file
        )
        add_finding(
            "P1" if issue_count >= 3 else "P2",
            f"Stop swallowing runtime failures in `{hottest_file}:{first_line}`",
            (
                f"SAGE's static analysis flagged {issue_count} exception-handling issues in "
                f"`{hottest_file}`; the first finding at line {first_line} is: {first_message}."
            ),
            "Replace silent or overly broad exception handlers with narrower catches plus logging or re-raise context.",
        )

    security_candidates = [
        (file_path, line, message)
        for file_path, line, message in code_analysis.security_issues
        if _is_actionable_analysis_path(file_path)
    ]
    if security_candidates:
        file_path, line, message = security_candidates[0]
        add_finding(
            "P1",
            f"Address security-sensitive code in `{file_path}:{line}`",
            f"`{file_path}:{line}` was flagged by the built-in security scan: {message}.",
            (
                "Review the data flow at this call site and replace it with a safer "
                "pattern before layering on new features."
            ),
        )

    unused_import_candidates = [
        (file_path, import_name, line)
        for file_path, import_name, line in code_analysis.unused_imports
        if _is_actionable_analysis_path(file_path)
    ]
    if unused_import_candidates:
        import_counts = Counter(file_path for file_path, _, _ in unused_import_candidates)
        hottest_file, unused_count = import_counts.most_common(1)[0]
        first_import, first_line = next(
            (import_name, line)
            for file_path, import_name, line in unused_import_candidates
            if file_path == hottest_file
        )
        add_finding(
            "P2",
            f"Clean up stale dependencies in `{hottest_file}`",
            (
                f"The analyzer found {unused_count} apparently unused imports in `{hottest_file}`; "
                f"one early example is `{first_import}` at line {first_line}."
            ),
            "Prune dead imports and unreachable branches so future reviews are about real behavior instead of residue.",
        )

    ci_config = project_analysis.ci_config
    if not (ci_config and ci_config.platform):
        analyzed_files = len(
            [path for path in code_analysis.complexity if _is_actionable_analysis_path(path)]
        )
        if analyzed_files >= 10:
            add_finding(
                "P2",
                "Add a first-class CI signal for repo-wide regressions",
                (
                    "The project analyzer did not detect a standard CI workflow definition "
                    "even though this repo has a large multi-subproject surface area."
                ),
                "Add an automated lint-and-test workflow so broad refactors do not rely on manual validation.",
            )

    if not findings:
        return None

    intro = (
        "## Grounded Fallback Analysis\n\n"
        "Model synthesis did not complete cleanly for this broad review, so SAGE generated "
        "the findings below from its built-in static repo analyzers.\n"
    )
    if task_prompt:
        intro += f"Scope: {task_prompt.strip()}\n\n"

    lines = [intro.rstrip(), ""]
    for index, (severity, title, evidence, recommendation) in enumerate(findings[:5], start=1):
        lines.append(f"{index}. {severity} - {title}")
        lines.append(f"Evidence: {evidence}")
        lines.append(f"Recommendation: {recommendation}")
        lines.append("")

    return "\n".join(lines).strip()


# NOTE: Shell utilities (_extract_scoped_prefix, _resolve_scoped_directory,
# _run_shell, _read_file_context, _extract_bash_blocks) moved to sage/core/shell.py


def _is_valid_file_path(path_arg: str) -> bool:
    """Validate that a path argument looks like a real file path, not garbage text.

    This prevents the model from outputting prose as READ: arguments like:
    "READ: The previous interaction was a directive to perform an analysis..."

    Also detects garbage like:
    "ai-platform/backend/ai-platform/backend/ai-platform/backend/..."

    Returns True if the argument appears to be a valid file path.
    """
    # Remove backticks that may wrap the path
    path = path_arg.strip().strip("`").strip()

    if not path:
        return False

    # Reject paths that are too long (typical OS limit is 255 chars for filename)
    if len(path) > 255:
        return False

    # Reject repetitive garbage paths like "ai-platform/backend/ai-platform/backend/..."
    # Single segment repetition: foo/foo/foo/
    if re.search(r"([\w-]+/)(\1){2,}", path):
        return False

    # Multi-segment repetition: dir1/dir2/dir1/dir2/
    if re.search(r"(([\w-]+/){1,3})(\1){1,}", path):
        return False

    # Check for excessive repetition of any path segment (5+ times)
    if "/" in path:
        path_parts = path.split("/")  # pragma: no cover
        for part in set(path_parts):  # pragma: no cover
            if part and len(part) > 2 and path_parts.count(part) >= 5:  # pragma: no cover
                return False  # pragma: no cover

    # Reject paths that start with common prose patterns (case insensitive)
    prose_starts = (
        "the ",
        "i ",
        "let ",
        "based on",
        "according to",
        "as ",
        "this ",
        "here ",
        "now ",
        "first ",
        "then ",
        "next ",
        "please ",
        "you ",
        "we ",
        "my ",
        "our ",
        "your ",
        "it ",
        "that ",
        "which ",
        "what ",
        "when ",
        "where ",
        "why ",
        "how ",
        "if ",
        "for ",
        "to ",
        "from ",
        "with ",
        "about ",
        "into ",
        "through ",
        "during ",
        "before ",
        "after ",
        "above ",
        "below ",
        "between ",
        "under ",
        "again ",
        "further ",
        "once ",
        "just ",
        "also ",
        "even ",
        "still ",
        "already ",
        "always ",
    )
    path_lower = path.lower()
    if any(path_lower.startswith(start) for start in prose_starts):
        return False

    # Reject paths with multiple consecutive spaces (suggests prose)
    if "  " in path:
        return False

    # Reject paths with common sentence patterns
    sentence_patterns = (
        " is ",
        " are ",
        " was ",
        " were ",
        " will ",
        " would ",
        " could ",
        " should ",
        " may ",
        " might ",
        " must ",
        " can ",
        " has ",
        " have ",
        " had ",
        " do ",
        " does ",
        " did ",
        " be ",
        " been ",
        " being ",
        " and ",
        " but ",
        " or ",
        " so ",
        " because ",
        " although ",
    )
    if any(pattern in path_lower for pattern in sentence_patterns):
        return False  # pragma: no cover

    # A valid path should contain at least one of: /, \, ., or look like a simple filename
    # Simple filenames: word characters with optional extension
    has_path_chars = "/" in path or "\\" in path or "." in path
    looks_like_filename = re.match(r"^[\w\-]+(\.\w+)?$", path) is not None

    if not has_path_chars and not looks_like_filename:
        # If it has spaces but no path chars, likely prose
        if " " in path:
            return False

    return True


def _normalize_workspace_relative_path(path_arg: str, cwd: Path) -> str:
    """Normalize a model-provided path (READ/FILE/etc) to be relative to the active workspace.

    Handles common mismatch cases:
    - Running from repo root vs running from the ai-platform subdirectory
    - Model referencing platform/... when the directory is ai-platform/...
    """
    raw = (path_arg or "").strip().strip("`").strip()
    if not raw:
        return raw

    if raw.startswith("./"):
        raw = raw[2:]
    if raw.startswith("../") or raw == "..":
        return raw
    if raw.startswith("/") or raw.startswith("~"):
        return raw
    ai_prefix = "ai-platform/"
    platform_prefix = "platform/"

    cwd_name = cwd.name
    has_ai_platform_child = (cwd / "ai-platform").is_dir()

    if raw.startswith(ai_prefix):
        if cwd_name == "ai-platform":
            return raw[len(ai_prefix) :]
        return raw

    if raw.startswith(platform_prefix):
        rest = raw[len(platform_prefix) :]
        if cwd_name == "ai-platform":
            return rest
        if has_ai_platform_child:
            return f"ai-platform/{rest}"
        return raw

    return raw


def _strip_inline_description(cmd: str) -> str:
    """Strip a trailing English description in parentheses from a shell command.

    Models sometimes emit `RUN: ls -laR | head -200 (list top 200 lines)`. The
    bare `(...)` is invalid shell — bash sees it as a subshell with unquoted
    bare words and aborts with a syntax error. We strip the annotation when
    the parenthetical content looks like prose (multi-word, no shell
    metacharacters) while leaving real shell parens alone (`find . \\( ... \\)`,
    `$(date)`, `(cd /tmp && ls)`).
    """
    cmd = cmd.rstrip()
    if not cmd.endswith(")") or "(" not in cmd:
        return cmd
    depth = 0
    open_idx = -1
    for i in range(len(cmd) - 1, -1, -1):
        ch = cmd[i]
        if ch == ")":
            depth += 1
        elif ch == "(":
            depth -= 1
            if depth == 0:
                open_idx = i
                break
    if open_idx < 0:
        return cmd  # pragma: no cover
    # An escaped paren (find . \( ... \)) is shell grouping — keep it.
    if open_idx > 0 and cmd[open_idx - 1] == "\\":
        return cmd
    inside = cmd[open_idx + 1 : -1]
    # Shell metacharacters inside → it's real shell, not prose.
    if re.search(r"[|;&<>$`=\\]", inside):
        return cmd
    # A single bare token like `(verbose)` is ambiguous (could be a flag-ish
    # annotation OR a subshell). Don't strip — too risky.
    if " " not in inside.strip():
        return cmd
    before = cmd[:open_idx].rstrip()
    if not before:
        return cmd
    return before


def _extract_tool_commands(text: str) -> list[tuple[str, str]]:
    """Extract READ:, SEARCH:, and RUN: tool commands from model output.

    Returns list of (tool_type, argument) tuples.
    Validates that READ: arguments look like actual file paths.
    """
    # Strip reasoning-model thinking blocks so we don't try to extract
    # tool commands the model only *talked about* inside <think>.
    from sage.core.thinking_filter import strip_thinking_blocks
    text = strip_thinking_blocks(text)
    text = renderer.normalize_tool_command_syntax(text)
    commands: list[tuple[str, str]] = []
    for m in re.finditer(r"^\s*(?:[-*]\s*)?(READ|SEARCH|RUN):\s*(.+)$", text, re.MULTILINE):
        tool_type = m.group(1).upper()
        arg = m.group(2).strip()
        if tool_type == "RUN":
            arg = _strip_inline_description(arg)
        if arg:
            # For READ commands, validate the path looks legitimate
            if tool_type == "READ" and not _is_valid_file_path(arg):
                # Skip invalid paths - they're likely model garbage
                continue
            commands.append((tool_type, arg))
    return commands


def _extract_tool_commands_structured(text: str) -> list:
    """Extract tool commands as structured ToolCall objects.

    P0-D: This is the structured tool integration point.
    Converts text-based tool commands to typed ToolCall objects
    that can be validated and tracked in the ExecutionLedger.

    Args:
        text: Model output containing tool commands

    Returns:
        List of ToolCall objects
    """
    from sage.core.tools import ToolCall, ToolType

    text = renderer.normalize_tool_command_syntax(text)
    calls: list[ToolCall] = []

    # P1-2: Require at least one non-whitespace character after the colon
    # This prevents blank commands like "READ:" from being parsed
    for m in re.finditer(r"^\s*(?:[-*]\s*)?(READ|SEARCH|RUN):\s*(\S.*)$", text, re.MULTILINE):
        tool_type_str = m.group(1).upper()
        arg = m.group(2).strip()
        if tool_type_str == "RUN":
            arg = _strip_inline_description(arg)

        # P1-2: Double-check for blank/empty arguments
        if not arg or arg.upper() in ("READ:", "SEARCH:", "RUN:"):
            continue

        # For READ commands, validate the path looks legitimate
        if tool_type_str == "READ" and not _is_valid_file_path(arg):
            continue

        # Map to ToolType
        tool_type_map = {
            "READ": ToolType.READ,
            "SEARCH": ToolType.SEARCH,
            "RUN": ToolType.RUN,
        }
        tool_type = tool_type_map.get(tool_type_str)


        # Build arguments based on tool type
        if tool_type == ToolType.READ:
            arguments = {"path": arg}
        elif tool_type == ToolType.SEARCH:
            arguments = {"pattern": arg}
        elif tool_type == ToolType.RUN:
            arguments = {"command": arg}


        calls.append(
            ToolCall(
                tool_type=tool_type,
                arguments=arguments,
                validated=False,
                source_line=m.group(0).strip(),
            )
        )

    return calls


# NOTE: _sanitize_shell_block and _strip_search_comment moved to sage/core/shell.py


def _discover_project_paths(
    cwd: Path,
    pattern: str,
    max_results: int = 40,
) -> list[str]:
    """Return file-path matches for glob-style SEARCH patterns."""
    matches: list[str] = []
    skip_dirs = {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        "dist",
        "build",
        ".pytest_cache",
        ".mypy_cache",
        ".sage",
    }

    # Optimization: Use safe_walk for efficiency if pattern is simple or broad
    from sage.core.project import safe_walk

    if pattern in {"*", "**/*"}:
        for path in safe_walk(cwd, skip_dirs=skip_dirs):
            try:
                rel = path.relative_to(cwd)
                matches.append(rel.as_posix())
                if len(matches) >= max_results:
                    break  # pragma: no cover
            except (ValueError, OSError):
                continue
        return sorted(matches)

    try:
        candidates = sorted(cwd.rglob(pattern))
    except (OSError, ValueError, re.error):
        return matches

    for candidate in candidates:
        if not candidate.is_file():
            continue  # pragma: no cover
        rel = candidate.relative_to(cwd)
        if any(part in skip_dirs or part.startswith(".") for part in rel.parts):
            continue  # pragma: no cover
        matches.append(rel.as_posix())
        if len(matches) >= max_results:
            break  # pragma: no cover
    return matches


def _split_search_patterns(pattern: str) -> list[str]:
    """Split a SEARCH expression into one or more concrete patterns."""
    cleaned = pattern.strip()
    if not cleaned:
        return []
    if any(ch in cleaned for ch in "*?[]"):
        return [cleaned]

    raw_parts = [cleaned]
    if re.search(r"\s+(?:OR|or)\s+", cleaned):
        raw_parts = re.split(r"\s+(?:OR|or)\s+", cleaned)
    elif "|" in cleaned and not any(ch in cleaned for ch in "(){}[]"):
        raw_parts = cleaned.split("|")

    parts: list[str] = []
    seen: set[str] = set()
    for part in raw_parts:
        normalized = part.strip().strip('"').strip("'").strip()
        if normalized and normalized not in seen:
            parts.append(normalized)
            seen.add(normalized)
    return parts or [cleaned]


def _tool_context_needs_more_investigation(tool_context: str) -> bool:
    """Return True when tool output is too weak to support grounded analysis."""
    sections = [section.strip() for section in tool_context.split("\n\n") if section.strip()]
    if not sections:
        return True

    negative_markers = (
        "file not found or empty",
        "no matches found",
        "no path matches found",
        "error:",
        "outside workspace",
        "scoped directory not found",
        "empty command",
        "no results found",
    )
    positive_markers = (
        "File: ",
        "Directory: ",
        "Search results for ",
        "Path matches for ",
        "Output:\n",
    )

    has_positive_signal = any(
        any(marker in section for marker in positive_markers) for section in sections
    )
    all_negative = all(
        any(marker in section.lower() for marker in negative_markers) for section in sections
    )
    return all_negative or not has_positive_signal


def _build_readonly_response_retry_prompt(
    response: str,
    classification: _ClassifiedRequest | None,
    *,
    verified_files: set[str] | None = None,
    cumulative_item_count: int | None = None,
) -> str | None:
    """Build a continuation prompt when a read-only response is incomplete or weak."""
    if not classification or not classification.read_only:
        return None

    # P0-1: Use cumulative count if provided, otherwise extract from current response
    if cumulative_item_count is not None:
        numbered_items = cumulative_item_count
    else:
        # Use unified extraction for consistent counting
        numbered_items = _extract_list_item_count(response)

    if (
        classification.request_type == _RequestType.LIST_GENERATION
        and classification.quantity_required
        and numbered_items < classification.quantity_required
    ):
        remaining = classification.quantity_required - numbered_items
        next_item = numbered_items + 1
        return (
            f"CONTINUE immediately from item {next_item}. You have {numbered_items} items, need {classification.quantity_required} total ({remaining} more).\n\n"
            f"CRITICAL: Output ONLY numbered list items starting with '{next_item}. ' — no explanations, no meta-commentary.\n"
            f"Do NOT explain why you can't continue. Do NOT ask for more context. Just generate items.\n\n"
            f"Start your response with:\n{next_item}. "
        )

    validation = _validate_classified_response(
        response,
        classification,
        verified_files=verified_files or set(),
    )
    if not validation.should_retry:
        return None  # pragma: no cover

    retry_prompt = (
        validation.retry_prompt or "Regenerate your response with the required corrections."
    )
    grounding_rules = (
        "\nGROUNDING RULES:\n"
        "- Reference only files or code locations supported by verified READ:/SEARCH: results.\n"
        "- If you do not have enough evidence for a claim, say so explicitly instead of inventing facts.\n"
        "- Keep the response read-only: no FILE: blocks, tests, or implementation steps.\n"
    )
    return retry_prompt + grounding_rules


def _build_readonly_exploration_nudge(
    phase_name: str,
    classification: _ClassifiedRequest | None,
    *,
    has_verified_files: bool,
) -> str | None:
    """Ask the model to issue concrete investigation commands before analysis claims."""
    if not classification or not classification.read_only:
        return None
    if phase_name not in {"planning", "analysis"}:
        return None
    if has_verified_files:
        return None

    return (
        "This is read-only analysis and you have not gathered grounded evidence yet.\n"
        "Issue concrete investigation commands now before making substantive claims.\n"
        "Rules:\n"
        "1. Use READ: on real files (not directories unless you need a listing).\n"
        "2. Use SEARCH: with one pattern per line (no OR combinations on one line).\n"
        "3. Use RUN: only for safe read-only commands.\n"
        "4. Prefer bash discovery commands like RUN: ls -laR | head -200, RUN: find . -maxdepth 2 -type d | head -80, and RUN: rg --files . | head -120 when you need repo-wide context.\n"
        "5. After commands run, base findings only on verified results."
    )


# Track consecutive failed reads to provide helpful feedback
_consecutive_failed_reads: list[str] = []
_max_failed_reads_before_help = 3


def _format_read_batch_summary(paths: list[str], max_preview: int = 3) -> str:
    """Summarize consecutive READ operations without flooding the terminal."""
    if not paths:
        return "📄 0 files"
    if len(paths) == 1:
        return f"📄 {paths[0]}"

    preview = ", ".join(paths[:max_preview])
    remaining = len(paths) - min(len(paths), max_preview)
    if remaining > 0:
        preview += f" (+{remaining} more)"
    return f"📚 {len(paths)} files: {preview}"


def _execute_tool_commands(
    commands: list[tuple[str, str]],
    cwd: Path,
    *,
    files_read: set[str] | None = None,
    execution_ledger: Any | None = None,
) -> list[str]:
    """Execute tool commands and return results as context strings.

    Also records evidence via the global evidence tracker for synthesis gating.
    """
    from sage.cli_core import _add_session_file_read, _get_project_file_listing, _record_file_read, _record_search
    global _consecutive_failed_reads

    results: list[str] = []
    pending_successful_reads: list[str] = []

    def _flush_read_summary() -> None:
        if not pending_successful_reads:
            return
        renderer.phase("reading", _format_read_batch_summary(pending_successful_reads))
        pending_successful_reads.clear()

    for tool_type, arg in commands:
        if tool_type != "READ":
            _flush_read_summary()

        if tool_type == "READ":
            # Clean up path (remove ./, leading/trailing whitespace, backticks)
            clean_arg = arg.strip().strip("`").strip()
            if clean_arg.startswith("./"):
                clean_arg = clean_arg[2:]  # pragma: no cover
            clean_arg = _normalize_workspace_relative_path(clean_arg, cwd)

            read_bases: list[Path] = [cwd]
            pr = _default_project_root(cwd).resolve()
            root = cwd.resolve()
            if pr != root and str(pr).startswith(str(root) + os.sep):
                read_bases.append(pr)  # pragma: no cover

            content: str | None = None
            for base in read_bases:
                content = _read_file_context(clean_arg, base, max_lines=200)
                if content:
                    break
            if content:
                pending_successful_reads.append(clean_arg)
                results.append(content)
                # Record successful file read as evidence
                _record_file_read(clean_arg, success=True)
                if files_read is not None:
                    files_read.add(clean_arg)  # pragma: no cover
                _add_session_file_read(cwd, clean_arg)
                if execution_ledger is not None:
                    from sage.core.tools import ToolCall, ToolType

                    execution_ledger.record_execution(
                        ToolCall(
                            tool_type=ToolType.READ,
                            arguments={"path": clean_arg},
                            validated=True,
                        ),
                        success=True,
                    )
                # Reset failed reads counter on success
                _consecutive_failed_reads = []
            else:
                _consecutive_failed_reads.append(clean_arg)
                # Record failed file read
                _record_file_read(clean_arg, success=False)
                if execution_ledger is not None:
                    from sage.core.tools import ToolCall, ToolType

                    execution_ledger.record_execution(
                        ToolCall(
                            tool_type=ToolType.READ,
                            arguments={"path": clean_arg},
                            validated=True,
                        ),
                        success=False,
                    )

                # If too many consecutive failures, provide helpful file listing
                if len(_consecutive_failed_reads) >= _max_failed_reads_before_help:
                    # Get actual project files
                    actual_files = _get_project_file_listing(cwd, max_files=30)
                    results.append(
                        f"[READ {clean_arg}: file not found]\n\n"
                        f"⚠️ You have guessed {len(_consecutive_failed_reads)} non-existent paths in a row.\n"
                        f"STOP GUESSING. Here are the ACTUAL files in this project:{actual_files}\n\n"
                        f"Use ONLY paths from this list. Do NOT invent paths like 'src/main.py' or 'src/utils/config.py'."
                    )
                    _consecutive_failed_reads = []  # Reset after showing help
                else:
                    results.append(f"[READ {clean_arg}: file not found or empty]")
        elif tool_type == "SEARCH":
            scope, pattern = _extract_scoped_prefix(arg)
            pattern = _strip_search_comment(pattern)
            pattern = _normalize_workspace_relative_path(pattern, cwd)
            search_cwd = cwd
            if scope:
                search_cwd, error = _resolve_scoped_directory(scope, cwd)
                if error:
                    results.append(error)
                    continue
            if any(ch in pattern for ch in "*?[]"):
                renderer.phase(
                    "searching",
                    f"🔍 {pattern}" if not scope else f"🔍 {scope}: {pattern}",
                )
                matches = _discover_project_paths(search_cwd, pattern)
                if matches:
                    results.append(
                        f"Path matches for '{pattern}'"
                        + (f" in {scope}" if scope else "")
                        + ":\n"
                        + "\n".join(matches)
                    )
                    # Record successful glob search as evidence
                    _record_search(pattern, matches)
                    if execution_ledger is not None:
                        from sage.core.tools import ToolCall, ToolType

                        execution_ledger.record_execution(
                            ToolCall(
                                tool_type=ToolType.SEARCH,
                                arguments={"pattern": pattern},
                                validated=True,
                            ),
                            success=True,
                        )
                else:
                    results.append(
                        f"[SEARCH '{pattern}'"
                        + (f" in {scope}" if scope else "")
                        + ": no path matches found]"
                    )
                    # Record empty search
                    _record_search(pattern, [])
                    if execution_ledger is not None:
                        from sage.core.tools import ToolCall, ToolType

                        execution_ledger.record_execution(
                            ToolCall(
                                tool_type=ToolType.SEARCH,
                                arguments={"pattern": pattern},
                                validated=True,
                            ),
                            success=False,
                        )
                continue
            search_patterns = _split_search_patterns(pattern)
            if len(search_patterns) > 1:
                renderer.phase(
                    "searching",
                    (
                        f"🔍 any of: {', '.join(search_patterns[:3])}"
                        if not scope
                        else f"🔍 {scope}: any of {', '.join(search_patterns[:3])}"
                    ),
                )
                combined: list[str] = []
                for term in search_patterns:
                    lines_result = _portable_grep(term, search_cwd, max_results=20).strip()
                    if lines_result:
                        combined.append(f"[term: {term}]\n{lines_result}")
                if combined:
                    results.append(
                        f"Search results for any of {search_patterns}"
                        + (f" in {scope}" if scope else "")
                        + ":\n"
                        + "\n".join(combined)
                    )
                    # Record successful multi-pattern search as evidence
                    # Extract file paths from grep results
                    found_files = []
                    for line in "\n".join(combined).splitlines():
                        if ":" in line and not line.startswith("[term:"):
                            file_part = line.split(":")[0].lstrip("./")  # pragma: no cover
                            if file_part and file_part not in found_files:  # pragma: no cover
                                found_files.append(file_part)  # pragma: no cover
                    _record_search(f"any of {search_patterns}", found_files)
                    if execution_ledger is not None:
                        from sage.core.tools import ToolCall, ToolType

                        execution_ledger.record_execution(
                            ToolCall(
                                tool_type=ToolType.SEARCH,
                                arguments={"pattern": f"any of {search_patterns}"},
                                validated=True,
                            ),
                            success=True,
                        )
                else:
                    results.append(
                        f"[SEARCH any of {search_patterns}"
                        + (f" in {scope}" if scope else "")
                        + ": no matches found]"
                    )
                    # Record empty search
                    _record_search(f"any of {search_patterns}", [])
                    if execution_ledger is not None:
                        from sage.core.tools import ToolCall, ToolType

                        execution_ledger.record_execution(
                            ToolCall(
                                tool_type=ToolType.SEARCH,
                                arguments={"pattern": f"any of {search_patterns}"},
                                validated=True,
                            ),
                            success=False,
                        )
                continue
            renderer.phase(
                "searching",
                f"🔍 {pattern}" if not scope else f"🔍 {scope}: {pattern}",
            )
            search_result = _portable_grep(
                pattern, search_cwd, files_only=True, max_results=20
            )
            if search_result.strip():
                # Also grab matching lines for context
                lines_result = _portable_grep(pattern, search_cwd, max_results=40)
                results.append(
                    f"Search results for '{pattern}'"
                    + (f" in {scope}" if scope else "")
                    + f":\n{lines_result}"
                )
                # Record successful search as evidence
                found_files = [
                    f.strip().lstrip("./") for f in search_result.strip().splitlines() if f.strip()
                ]
                _record_search(pattern, found_files)
                if execution_ledger is not None:
                    from sage.core.tools import ToolCall, ToolType

                    execution_ledger.record_execution(
                        ToolCall(
                            tool_type=ToolType.SEARCH,
                            arguments={"pattern": pattern},
                            validated=True,
                        ),
                        success=True,
                    )
            else:
                results.append(
                    f"[SEARCH '{pattern}'"
                    + (f" in {scope}" if scope else "")
                    + ": no matches found]"
                )
                # Record empty search
                _record_search(pattern, [])
                if execution_ledger is not None:
                    from sage.core.tools import ToolCall, ToolType

                    execution_ledger.record_execution(
                        ToolCall(
                            tool_type=ToolType.SEARCH,
                            arguments={"pattern": pattern},
                            validated=True,
                        ),
                        success=False,
                    )
        elif tool_type == "RUN":
            scope, command = _extract_scoped_prefix(arg)
            run_cmd = command if scope else arg
            label = (run_cmd or arg)[:60]
            renderer.phase(
                "running",
                f"⚡ {label}" if not scope else f"⚡ {scope}: {label}",
            )
            with renderer.status_spinner(
                (
                    f"Running: {label[:60]}..."
                    if not scope
                    else f"Running in {scope}: {label[:60]}..."
                ),
                "executing",
            ):
                output = _run_shell(run_cmd, cwd, timeout=60)
            renderer.print_shell_output(output)
            results.append(f"[RUN: {arg}]\nOutput:\n{output}")
            if execution_ledger is not None:
                from sage.core.tools import ToolCall, ToolType

                execution_ledger.record_execution(
                    ToolCall(
                        tool_type=ToolType.RUN,
                        arguments={"command": arg},
                        validated=True,
                    ),
                    success=not _has_errors(output),
                    output=output,
                )
        elif tool_type in ("FETCH", "WEB"):
            url = arg.strip().strip("`").strip()
            renderer.phase("fetching", f"🌐 {url}")
            with renderer.status_spinner(f"Fetching: {url[:60]}...", "executing"):
                try:
                    from sage.core.tools import ToolContext, WebFetchTool

                    ctx = ToolContext(cwd=cwd)
                    fetcher = WebFetchTool(ctx)
                    fetch_result = fetcher.fetch(url)
                    if fetch_result.success:
                        output = fetch_result.output or ""
                        results.append(f"[FETCH: {url}]\nContent:\n{output}")
                    else:
                        results.append(f"[FETCH: {url}] Error: {fetch_result.error}")
                except Exception as e:
                    results.append(f"[FETCH: {url}] Error: {str(e)}")

            if execution_ledger is not None:
                from sage.core.tools import ToolCall, ToolType

                execution_ledger.record_execution(
                    ToolCall(
                        tool_type=ToolType.WEB_FETCH,
                        arguments={"url": url},
                        validated=True,
                    ),
                    success=fetch_result.success if "fetch_result" in locals() else False,
                    output=output if "output" in locals() else "",
                )
    _flush_read_summary()
    return results


# NOTE: _shell_quote moved to sage/core/shell.py


# Names that are language tags, not real filenames — reject these
_INVALID_FILENAMES = {
    "bash",
    "sh",
    "shell",
    "python",
    "javascript",
    "typescript",
    "java",
    "ruby",
    "go",
    "rust",
    "c",
    "cpp",
    "html",
    "css",
    "sql",
    "json",
    "yaml",
    "yml",
    "toml",
    "xml",
    "text",
    "txt",
    "markdown",
    "md",
    "jsx",
    "tsx",
    "php",
    "perl",
    "swift",
    "kotlin",
    "scala",
    "r",
    "dockerfile",
    "makefile",
}


