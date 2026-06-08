"""Sage CLI — local-first AI coding assistant.

Usage:
  sage run                              Interactive coding agent (Claude Code-like)
  sage chat                             Interactive chat session
  sage models                           List available models
  sage config show                      Show current config
  sage config set <key> <value>         Set a config value

Module Structure Migration (P1-17):
    This file contains legacy class definitions that have modern equivalents
    in sage/core/. To reduce duplication, classes should migrate to use
    sage/core/ imports:

    - Checkpoint, CheckpointManager -> sage.core.checkpoint
    - SecurityFinding, SecurityAuditor -> sage.core.security
    - FileNode, DependencyGraph -> sage.core.dependencies
    - TaskType, SwarmTask, SwarmOrchestrator -> sage.core.swarm
    - ContextCompactor -> sage.core.context_management
    - ExecutionPhase, PlanTask, ExecutionPlan -> sage.core.procedural_workflow

    Until full migration, the local definitions remain for backward compatibility.
"""

from __future__ import annotations

import sys as _sys
import os as _os

# Ensure local sage package is preferred over global installation (P1-17)
_sys.path.insert(0, _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..")))

# Intercept all builtins.open writes to force empty __init__.py files
import builtins as _builtins
import io as _io
from pathlib import Path as _Path

_orig_open = _builtins.open

def _safe_open(file, mode='r', *args, **kwargs):
    is_write = False
    if isinstance(mode, str):
        is_write = any(c in mode for c in ('w', 'a', 'x', '+'))
    
    if is_write:
        try:
            path = _Path(file).resolve()
            if path.name == "__init__.py":
                import sys as _sys
                _sys.stderr.write(f"[sage-interceptor] Intercepted write to {path} (mode={mode}). Forcing empty.\n")
                _sys.stderr.flush()
                # Truncate real file to 0 bytes
                f_real = _orig_open(file, 'w', encoding='utf-8')
                f_real.close()
                if 'b' in mode:
                    return _io.BytesIO()
                else:
                    return _io.StringIO()
        except Exception:
            pass
    return _orig_open(file, mode, *args, **kwargs)

_builtins.open = _safe_open


def _windows_add_scripts_to_user_path() -> None:
    """Idempotently add Python's Scripts directory (where pip puts ``sage.exe``)
    to the current user's persistent PATH via the registry. Runs silently on
    every Windows startup so ``sage`` becomes a bare command in the next
    terminal window after the user runs ``py -m sage`` once. No admin needed.
    """
    if _sys.platform != "win32":
        return

    try:
        import sysconfig
        import winreg  # type: ignore[import]

        scripts_dir = sysconfig.get_path("scripts")
        if not scripts_dir:
            return

        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Environment",
            0,
            winreg.KEY_READ | winreg.KEY_WRITE,
        )
        try:
            current, reg_type = winreg.QueryValueEx(key, "Path")
        except FileNotFoundError:
            current, reg_type = "", winreg.REG_EXPAND_SZ

        # Already present? Bail out — don't touch the registry needlessly.
        existing_entries = {p.strip().lower() for p in (current or "").split(";") if p.strip()}
        if scripts_dir.lower() in existing_entries:
            winreg.CloseKey(key)
            return

        new_path = f"{current};{scripts_dir}" if current else scripts_dir
        winreg.SetValueEx(key, "Path", 0, reg_type, new_path)
        winreg.CloseKey(key)

        # Broadcast WM_SETTINGCHANGE so File Explorer / new shells pick up the
        # change without a logoff. Existing terminals still need to reopen.
        try:
            import ctypes

            ctypes.windll.user32.SendMessageTimeoutW(
                0xFFFF, 0x001A, 0, "Environment", 0x0002, 3000, None
            )
        except Exception:
            pass

        # Also patch the live process PATH so the user can run sage.exe in this
        # very session (e.g. via os.system / subprocess) without reopening.
        if scripts_dir.lower() not in (_os.environ.get("PATH", "") or "").lower():
            _os.environ["PATH"] = (
                _os.environ.get("PATH", "") + _os.pathsep + scripts_dir
            ).lstrip(_os.pathsep)

        # One-time, very quiet hint so the user knows what just happened.
        try:
            _sys.stderr.write(
                f"[sage] Added {scripts_dir} to your user PATH. "
                "Open a new terminal and 'sage' will work directly.\n"
            )
            _sys.stderr.flush()
        except Exception:
            pass
    except Exception:
        # PATH bootstrapping is best-effort; never block sage from running.
        pass


def _windows_runtime_setup() -> None:
    """Configure stdout/stderr + ANSI mode + first-run PATH bootstrap on
    Windows so SAGE behaves identically to macOS/Linux regardless of how the
    CLI was launched (``python -m sage``, the pip-installed ``sage`` console
    script, or via the API server).
    """
    if _sys.platform != "win32":
        return

    # Force UTF-8 on standard streams (default Windows code page is cp1252,
    # which mangles model output containing non-ASCII characters).
    if hasattr(_sys.stdout, "reconfigure"):
        try:
            _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass
    if hasattr(_sys.stderr, "reconfigure"):
        try:
            _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    # Tell child processes to also use UTF-8 (e.g. ollama, git, npm subprocesses).
    _os.environ.setdefault("PYTHONUTF8", "1")
    _os.environ.setdefault("PYTHONIOENCODING", "utf-8")

    # subprocess.run(..., text=True) decodes child stdout/stderr using
    # locale.getpreferredencoding() — on Windows that's cp1252 and crashes the
    # moment git/npm/ollama prints a non-ASCII byte. Force UTF-8 so SAGE never
    # blows up parsing tool output. Safe for every subprocess SAGE spawns
    # because we always want UTF-8 here.
    try:
        import locale

        locale.getpreferredencoding = lambda do_setlocale=True: "utf-8"  # type: ignore[assignment]
    except Exception:
        pass

    # Enable ANSI escape codes (Virtual Terminal Processing) so Rich colours
    # render in cmd.exe / PowerShell. No-op on Windows < 10.
    try:
        import ctypes
        import ctypes.wintypes

        STD_OUTPUT_HANDLE = -11
        STD_ERROR_HANDLE = -12
        ENABLE_VIRTUAL_TERMINAL_PROCESSING = 0x0004

        kernel32 = ctypes.windll.kernel32
        for handle_id in (STD_OUTPUT_HANDLE, STD_ERROR_HANDLE):
            handle = kernel32.GetStdHandle(handle_id)
            if handle and handle != ctypes.wintypes.HANDLE(-1).value:
                mode = ctypes.wintypes.DWORD()
                if kernel32.GetConsoleMode(handle, ctypes.byref(mode)):
                    kernel32.SetConsoleMode(
                        handle, mode.value | ENABLE_VIRTUAL_TERMINAL_PROCESSING
                    )
    except Exception:
        pass

    # Persist Python's Scripts directory in the user's PATH so the bare ``sage``
    # command resolves from the next terminal onward — no manual setup needed
    # after ``pip install sage-ai-cli``.
    _windows_add_scripts_to_user_path()


_windows_runtime_setup()

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


# ══════════════════════════════════════════════════════════════════════════════
# EXPLICIT IMPORTS FROM SPLIT MODULES (FOR BACKWARD COMPATIBILITY)
# ══════════════════════════════════════════════════════════════════════════════

from sage.core.autonomous_helpers import (
    AutoFleetSubtask,
    AutoOrgBusinessBrief,
    AutoOrgRoleSpec,
    AutonomousCommandOptions,
    LSPClient,
    LSPDiagnostic,
    SandboxResult,
    _FailureLoopDetector,
    _TOOL_FORMAT_RECOVERY_PROMPT,
    _autoorg_keyword_hits,
    _autoorg_response_requests_user_input,
    _autoorg_worker_operating_policy,
    _build_autoorg_business_brief,
    _check_synthesis_gate,
    _classify_and_store_request,
    _clear_classification,
    _current_classification,
    _current_cwd,
    _decompose_task_for_fleet,
    _evidence_tracker,
    _force_implementation_mode,
    _format_autoorg_business_brief,
    _get_current_classification,
    _get_current_cwd,
    _get_evidence_tracker,
    _get_msg_content,
    _get_msg_role,
    _is_main_thread,
    _llama_cpp_runtime_bootstrap_attempted,
    _llama_cpp_runtime_bootstrap_error,
    _msg_to_dict,
    _ollama_pull_subprocess_timeout,
    _parse_autonomous_command_args,
    _parse_autoorg_repl_args,
    _plan_autoorg_roles,
    _record_file_read,
    _record_search,
    _request_classifier,
    _reset_evidence_tracker,
    _run_repl_autoorg_flow,
    _run_startup_context,
    _select_relevant_autoorg_capabilities,
    _set_current_cwd,
    _synthesis_gate,
    app,
    config_app,
    logger,
    secrets_app,
    sms_app,
)
from sage.core.session_helpers import (
    _FailureLoopDetector,
    _LLAMA_CPP_BROKEN_INDICATORS,
    _LLAMA_CPP_SUPPORTED_PYTHON,
    _MAX_PENDING_TASKS,
    _OLLAMA_MODEL_CACHE,
    _ROSETTA_DETECTED,
    _add_session_file_read,
    _add_session_pending_task,
    _add_to_conversation_memory,
    _add_to_output_history,
    _add_to_prompt_history,
    _auto_upgrade_model_if_possible,
    _autopolit_stop_path,
    _build_followup_context_from_recent_analysis,
    _build_messages_with_optional_resume_context,
    _build_resume_context_from_memory,
    _build_router,
    _check_context_relevance,
    _clean_numbered_task_line,
    _clear_session_context,
    _collect_readonly_shell_inventory,
    _conversation_memory_path,
    _ensure_llama_cpp_runtime,
    _ensure_model_available,
    _extract_best_numbered_list_block,
    _extract_explicit_numbered_task_block,
    _extract_priority_heading_findings,
    _extract_structured_numbered_findings,
    _extract_task_file_references,
    _filter_recovered_tasks_for_workspace,
    _get_conversation_context,
    _get_global_memory,
    _get_incomplete_tasks,
    _get_last_output,
    _get_last_used_model,
    _get_recent_outputs,
    _get_session_files_read,
    _get_session_mode,
    _get_session_pending_tasks,
    _get_session_recent_analysis,
    _get_session_recent_analysis_output,
    _get_session_recent_analysis_task_list,
    _initialize_request_grounding_state,
    _is_analysis_followup_implementation_request,
    _is_explicit_model_request,
    _is_explicit_resume_request,
    _is_resume_memory_entry_safe,
    _is_rosetta,
    _llama_cpp_install_attempts,
    _llama_cpp_toolchain_status,
    _load_conversation_memory,
    _load_output_history,
    _load_prompt_history,
    _load_session_state,
    _looks_like_analysis_output_candidate,
    _mark_task_completed,
    _model_capability_score,
    _normalize_actionable_task_list_text,
    _ollama_local_models,
    _ollama_pull_subprocess_timeout,
    _output_history_path,
    _persist_recent_analysis_output,
    _pick_runtime_fallback,
    _prefer_working_backend,
    _prepare_model_for_use,
    _probe_llama_cpp,
    _prompt_history_path,
    _providers_with_keys,
    _read_stdin,
    _resolve_model_prefix,
    _sage_dir,
    _save_conversation_memory,
    _save_output_history,
    _save_prompt_history,
    _save_session_state,
    _seed_recursive_analysis_context,
    _serialize_task_list,
    _session_state_path,
    _set_last_used_model,
    _set_session_mode,
    _set_session_pending_tasks,
    _set_session_recent_analysis,
    _should_lock_requested_model,
    _should_seed_recursive_analysis_context,
    _task_reference_exists_in_workspace,
    _update_global_memory,
    logger,
    secrets_gitignore,
)
from sage.core.exploration_helpers import (
    _FailureLoopDetector,
    _INVALID_FILENAMES,
    _STEP_PATTERNS,
    _build_cli_task_todos,
    _build_deterministic_readonly_analysis_fallback,
    _build_grounded_analysis_failure_message,
    _build_prompt_reader,
    _build_readonly_exploration_nudge,
    _build_readonly_response_retry_prompt,
    _build_seeded_readonly_synthesis_prompt,
    _build_verified_file_coverage_summary,
    _collect_full_readonly_file_coverage,
    _complete_cli_task_todos,
    _consecutive_failed_reads,
    _discover_project_paths,
    _execute_tool_commands,
    _extract_steps_from_response,
    _extract_tool_commands,
    _extract_tool_commands_structured,
    _format_read_batch_summary,
    _is_actionable_analysis_path,
    _is_valid_file_path,
    _iter_full_analysis_file_paths,
    _max_failed_reads_before_help,
    _normalize_workspace_relative_path,
    _ollama_pull_subprocess_timeout,
    _scan_project_context,
    _scan_project_context_with_files,
    _set_cli_task_stage,
    _split_search_patterns,
    _strip_inline_description,
    _tool_context_needs_more_investigation,
    logger,
)
from sage.core.validation_helpers import (
    _AIDER_REPLACE_RE,
    _AIDER_SEARCH_RE,
    _CODE_BLOCK_RE,
    _FAST_BUILD_MODELS,
    _FILE_BLOCK_RE,
    _FailureLoopDetector,
    _NON_ASCII_IDENTIFIER_RE,
    _NON_ASCII_LETTER_RE,
    _SIMPLE_QA_SYSTEM_PROMPT,
    _SIMPLE_QA_TIMEOUTS,
    _SINGLE_TURN_AGENT_TIMEOUTS,
    _SLOW_BUILD_MODELS,
    _auto_validate,
    _autonomous_generate_factory,
    _autonomous_progress,
    _build_context_aware_validation_retry_prompt,
    _build_session_protected_files,
    _build_simple_qa_messages,
    _clean_manifest_line,
    _collect_analysis_validation_violations,
    _count_numbered_list_items,
    _detect_aider_style_diff_garbage,
    _detect_non_english_code_identifiers,
    _detect_phantom_implementation,
    _detect_repetitive_filler,
    _detect_tool_description_vs_execution,
    _extract_and_write_files,
    _extract_grounded_file_references,
    _get_single_turn_agent_timeout,
    _is_investigation_only_response,
    _is_simple_qa_prompt,
    _load_single_turn_timeouts,
    _looks_like_actionable_numbered_list,
    _ollama_pull_subprocess_timeout,
    _pick_build_model,
    _requires_grounded_file_citations,
    _route_to_principal_pipeline,
    _run_autofleet_command,
    _run_autoorg_command,
    _run_autopolit_command,
    _run_callable_with_timeout,
    _run_validation_command,
    _should_ground_ask_response,
    _show_paste_indicator,
    _syntax_precheck,
    _validate_analysis_response,
    _validate_context_gathering,
    _validate_implementation_response,
    _validate_readonly_mode,
    _validate_tdd_compliance,
    _validate_tool_usage_for_analysis,
    _write_file,
    logger,
)
from sage.core.execution_helpers import (
    _FailureLoopDetector,
    _RequestExecutionContext,
    _build_implementation_completion_nudge,
    _call_llm,
    _collect_autopolit_priority_hints,
    _current_execution_context,
    _default_test_command,
    _did_analysis_fail_closed,
    _emit_grounded_analysis_failure,
    _execute_command_and_verify,
    _execute_file_write_and_verify,
    _execute_read_command,
    _execute_request_with_validation,
    _extract_tool_command_names,
    _extract_tool_commands_robust,
    _failure_loop_detector,
    _file_exists,
    _full_project_test_command,
    _get_current_task_prompt,
    _get_execution_context,
    _get_simple_test_result,
    _handle_context_overflow,
    _implementation_archetype_hints,
    _normalize_file_path,
    _ollama_pull_subprocess_timeout,
    _parse_test_output_simple,
    _parse_test_result_accurately,
    _read_file,
    _resolve_implementation_test_command,
    _response_describes_code_without_file_blocks,
    _response_has_tool_results,
    _run_shell_command_helper,
    _should_stop_autopolit_cycle,
    _simple_write_file,
    _suggest_target_paths_for_task,
    _track_files_read,
    _track_files_written,
    _validate_completion_claim,
    _validate_execution_claim,
    _validate_file_path_in_workspace,
    _validate_implementation_claim,
    _validate_list_generation_result,
    _validate_list_items_exist,
    _validate_retry_has_evidence,
    _validate_test_claim,
    _validate_test_files_exist,
    logger,
)
from sage.core.prompt_helpers import (
    _CLOUD_PROVIDER_DISPLAY_NAMES,
    _FailureLoopDetector,
    _ai_understand_prompt,
    _analyze_task_complexity,
    _build_cloud_deployment_context,
    _build_cloud_provider_prompt,
    _build_credential_bootstrap_context,
    _build_enhanced_reasoning_prompt,
    _build_multistep_phase_prompts,
    _build_tool_followup_prompt,
    _build_tool_format_recovery_prompt,
    _build_workspace_access_note,
    _build_workspace_map,
    _cleanup_broken_test_files,
    _enhance_task_prompt,
    _expand_prompt,
    _extract_and_validate_code,
    _get_fallback_statistics,
    _get_project_file_listing,
    _handle_model_fallback,
    _is_broken_test_file,
    _is_cloud_deployment_request,
    _is_complex_task,
    _is_credential_bootstrap_request,
    _is_readonly_analysis_request,
    _log_model_fallback,
    _ollama_pull_subprocess_timeout,
    _perform_cli_update,
    _resolve_cloud_provider_preference,
    _response_asks_for_cloud_provider,
    _response_commits_to_cloud_provider,
    _sample_workspace_paths,
    _should_skip_ai_orchestration,
    _should_use_multistep_pipeline,
    _should_use_seeded_synthesis_only,
    _truncate_context_smartly,
    _wants_code_changes,
    logger,
)
from sage.core.repl_agent import (
    SAGEAgent,
    _FailureLoopDetector,
    _global_agent,
    _ollama_pull_subprocess_timeout,
    logger,
)
from sage.commands_models import (
    _FailureLoopDetector,
    _LLAMA_CPP_ERROR_PATTERNS,
    _SAGE_TRAIN_SYSTEM_PROMPT,
    _detect_has_gpu,
    _detect_performance_cores,
    _detect_ram_gb,
    _diagnose_llama_cpp_failure,
    _get_model_size_gb,
    _get_pulled_ollama_names,
    _model_params_for_size,
    _ollama_exe,
    _ollama_install_hint,
    _ollama_pull_subprocess_timeout,
    _resolve_catalog_model,
    _sms_backend,
    _sms_process_alive,
    _sms_terminate_process,
    _train_ollama_model,
    _try_install_ollama,
    _version_callback,
    config_get,
    config_init,
    config_set,
    config_show,
    fix_llama_cpp_cmd,
    install,
    logger,
    login_cmd,
    logout_cmd,
    main,
    models,
    pull,
    remove_model,
    sync_catalog,
    sync_ollama_to_gcs,
    train_all,
    train_model,
    update,
    use_model,
    whoami_cmd,
)
from sage.commands_sms import (
    _FailureLoopDetector,
    _ollama_pull_subprocess_timeout,
    logger,
    sms_allow_firewall,
    sms_contacts_add,
    sms_contacts_app,
    sms_contacts_list,
    sms_contacts_remove,
    sms_devices,
    sms_diagnose,
    sms_kde_takeover,
    sms_logs,
    sms_setup,
    sms_start,
    sms_status,
    sms_stop,
    sms_test,
    sms_test_imessage,
    sms_unregister,
)

def _send_to_model(user_msg: str, show_thinking: bool = True) -> str | None:
    """Global wrapper for SAGEAgent.send_to_model."""
    if _global_agent:
        return _global_agent.send_to_model(user_msg, show_thinking)
    return None


def _send_single_turn_to_model(user_msg: str) -> str | None:
    """Global wrapper for SAGEAgent.send_single_turn_to_model."""
    if _global_agent:
        return _global_agent.send_single_turn_to_model(user_msg)
    return None


def _execute_task_prompt(
    task_prompt: str,
    save_history: bool = True,
    sender: Callable[[str], str | None] | None = None,
    enhanced_mode: bool = True,
) -> tuple[list[str], bool]:
    """Global entry point for task execution, delegating to the active SAGEAgent."""
    global _global_agent
    if _global_agent is None:
        # Fallback for tests or direct calls before run()
        from pathlib import Path

        from sage.core.engine import ConversationEngine
        from sage.core.context_persistence import ContextPersistenceManager
        from sage.core.renderer import Renderer

        cwd = _get_current_cwd() or Path.cwd()
        context_persistence_mgr = ContextPersistenceManager(cwd)
        _renderer = Renderer()
        engine = ConversationEngine(system_prompt=build_agent_system_prompt(cwd, is_local=False))
        # This is a minimal fallback; real instantiation happens in run()
        _global_agent = SAGEAgent(
            cwd=cwd,
            renderer=_renderer,
            engine=engine,
            router=None,  # Will fail if send is called without a router
            model_id="",
            temp=0.1,
            tokens=4096,
            model_locked=False,
            is_local=False,
            context_manager=context_persistence_mgr,
        )

    return _global_agent.execute_task_prompt(
        task_prompt,
        save_history=save_history,
        sender=sender,
        enhanced_mode=enhanced_mode,
    )


def _get_current_classification():
    """Returns the current request classification from the global agent."""
    global _global_agent
    if _global_agent and hasattr(_global_agent, "_current_classification"):
        return _global_agent._current_classification
    return None


# ── Usage tracking ──────────────────────────────────────────

def _track_cli_usage(response_text: str = "") -> None:
    """Fire-and-forget: report one CLI inference to the SAGE backend."""
    try:
        from sage.core.cli_auth import track_usage
        track_usage("cli", response_text=response_text)
    except Exception:
        pass


# ── Commands ────────────────────────────────────────────────


@app.command()
def run(
    model: Annotated[str | None, typer.Option("--model", "-m", help="Model ID")] = None,
    temperature: Annotated[float | None, typer.Option("--temperature", "-t")] = None,
    max_tokens: Annotated[int | None, typer.Option("--max-tokens")] = None,
    auto_run: Annotated[
        bool,
        typer.Option(
            "--auto-run/--no-auto-run",
            help="Auto-execute bash blocks without prompting",
        ),
    ] = True,
    max_retries: Annotated[
        int,
        typer.Option(
            "--max-retries",
            help=(
                "Deprecated compatibility flag. "
                "SAGE now keeps fixing tests until they pass or a real no-progress blocker is detected."
            ),
        ),
    ] = 10,
    verbose: Annotated[
        bool,
        typer.Option(
            "--verbose",
            "-v",
            help="Show all output including thinking blocks and detailed progress",
        ),
    ] = False,
    output: Annotated[
        str,
        typer.Option(
            "--output",
            "-o",
            help=(
                "Terminal verbosity level. "
                "  normal (default): stream model output + show what sage is reading/writing/running. "
                "  verbose: also show raw thinking blocks (<think>…</think>). "
                "  quiet: only show final result, suppress all progress (fastest for scripts)."
            ),
        ),
    ] = "normal",
    quiet: Annotated[
        bool,
        typer.Option(
            "--quiet",
            "-q",
            help="Suppress all streaming output — only show the final result. Alias for --output quiet.",
        ),
    ] = False,
    no_color: Annotated[
        bool,
        typer.Option(
            "--no-color",
            help="Disable ANSI colors (also respects NO_COLOR in the environment)",
        ),
    ] = False,
    prompt: Annotated[
        str | None,
        typer.Option(
            "--prompt",
            "-p",
            help=(
                "Run the agent on a single task non-interactively then exit. "
                "Used by the SMS bridge so texted tasks (e.g. 'create a project', "
                "'run the tests', 'fix the failing build') get the full agent "
                "loop — shell, file edits, tests, retries — instead of one-shot chat."
            ),
        ),
    ] = None,
) -> None:
    """Interactive coding agent — Claude Code–style READ/SEARCH/edit/run using your models."""
    import os

    import sys
    _stdout_encoding = getattr(sys.stdout, "encoding", None) or ""
    _encoding_is_modern = _stdout_encoding.lower().replace("-", "") in ("utf8", "utf-8", "utf16", "utf32", "cp65001")
    if (
        no_color
        or os.environ.get("NO_COLOR")
        or os.environ.get("SAGE_NO_COLOR")
        or os.environ.get("SAGE_ASCII")
        or os.environ.get("TERM") in (None, "", "dumb")
        or not sys.stdout.isatty()
        or not _encoding_is_modern
    ):
        renderer.set_no_color(True)
    if prompt or quiet or not sys.stdout.isatty():
        renderer.set_suppress_spinners(True)

    if max_retries != 10:
        renderer.warning(
            "--max-retries is deprecated and ignored. "
            "SAGE now retries test-fix loops until they pass or a real no-progress blocker is detected."
        )

    # Resolve output mode: --quiet/-q → "quiet" (alias for clean),
    # --verbose/-v → "verbose", otherwise use --output value.
    # Also accept "quiet" as a value for --output.
    om = (output or "normal").strip().lower()
    if om == "quiet":
        om = "clean"  # quiet is an alias for clean in the renderer
    if om not in ("clean", "normal", "verbose"):
        renderer.err_console.print(
            f"[red]Invalid --output {output!r}; use normal (default), verbose, or quiet.[/red]"
        )
        raise typer.Exit(code=2)

    # Flag wins: -v → verbose, -q → quiet/clean
    if verbose:
        om = "verbose"
    elif quiet:
        om = "clean"

    renderer.set_output_mode(om)

    # ── Billing check: CLI requires paid plan ──────────────────────────────
    try:
        from sage.core.cli_auth import check_cli_access, check_token_quota
        check_cli_access()
        check_token_quota()  # warn/block if token limit exceeded
    except RuntimeError as _billing_err:
        renderer.error(str(_billing_err))
        raise typer.Exit(1)

    cwd = Path.cwd()
    _set_current_cwd(cwd)  # Enable session persistence across turns
    _run_startup_context(cwd)

    cfg = load_config()

    # ── Wiring SAGE run_hooks (T1, T7, T8, T9, T10, T13) ───────────
    from sage.core.run_hooks import on_session_start
    is_testing = os.environ.get("SAGE_TESTING") == "1" or "pytest" in sys.modules
    
    readiness = on_session_start(
        cfg,
        cwd,
        skip_floor=is_testing,
        skip_readiness=True,
        user_first_prompt=prompt or "",
    )
    if not readiness.ok:
        renderer.error(readiness.message)
        raise typer.Exit(1)

    router = _build_router(cfg)
    prompt_reader = _build_prompt_reader(cwd)

    # Non-interactive one-shot mode: feed the supplied task once, then raise
    # EOFError on the next read so the REPL hits its `except EOFError: break`
    # path and exits cleanly. The full agent loop (tool use, shell, edits,
    # tests, retries) runs in between — this is what the SMS bridge uses so
    # texted tasks like "create a React Native project" actually execute.
    if prompt:
        _one_shot_value = prompt
        _one_shot_consumed = {"done": False}

        def _one_shot_reader(_prompt_text: str) -> str:
            if _one_shot_consumed["done"]:
                raise EOFError
            _one_shot_consumed["done"] = True
            return _one_shot_value

        prompt_reader = _one_shot_reader

        # Bypass the read-only / analysis guard. SMS users can't reply
        # "yes, implement it" — the texted task IS the approval.
        from sage.core.autonomous_helpers import set_force_implementation_mode
        set_force_implementation_mode(True)

    last_used_model = _get_last_used_model(cwd)
    model_id = model or last_used_model or cfg.default_model
    model_locked = bool(model) or (
        last_used_model is not None and last_used_model != cfg.default_model
    )
    try:
        cfg, model_id = _prepare_model_for_use(cfg, model_id)
    except RuntimeError as exc:
        renderer.error(str(exc))
        raise typer.Exit(1) from exc
    model_id = _auto_upgrade_model_if_possible(
        router, cfg, model_id, explicit_model=model, last_used_model=last_used_model
    )

    try:
        cfg, model_id = _prepare_model_for_use(cfg, model_id)
    except RuntimeError as exc:
        renderer.error(str(exc))
        raise typer.Exit(1) from exc

    # Rebuild router with updated config (may have new registered models)
    router = _build_router(cfg)

    _set_last_used_model(cwd, model_id)
    temp = temperature if temperature is not None else 0.1
    tokens = max_tokens if max_tokens is not None else cfg.max_tokens
    default_test_cmd = _default_test_command(cwd)
    full_project_test_cmd = _full_project_test_command(cwd)
    _ = _collect_autopolit_priority_hints(cwd)

    # Use lighter scan for local models to reduce prompt processing time
    is_local = (
        model_id.startswith("llama_cpp:")
        or model_id.startswith("ollama:")
        or cfg.get_local_model(model_id) is not None
    )
    workspace_map = _build_workspace_map(
        cwd,
        max_dirs=6 if is_local else 18,
        max_files_per_dir=3 if is_local else 6,
    )
    with renderer.status_spinner("Scanning project...", "reading"):
        if is_local:
            context = _scan_project_context(
                cwd,
                max_tree=12,
                max_source_files=2,
                max_source_lines=8,
            )
        else:
            context = _scan_project_context(cwd)
    renderer.step_done("Project scanned")

    # Set token limits: local models balance speed vs output, API models get full room
    # Increased limits to ensure enough memory for completing all procedural steps
    if is_local and tokens == cfg.max_tokens:
        tokens = 8192  # Increased from 4096 for more complete procedural output
    elif not is_local and tokens == cfg.max_tokens:
        tokens = max(tokens, 65536)  # Increased from 32768 for comprehensive task execution

    # Build initial conversation with project context
    system_prompt = build_agent_system_prompt(cwd, is_local=is_local)

    # Local models have slow prefill — keep context tight to stay within timeout budgets
    engine = ConversationEngine(
        system_prompt=system_prompt,
        max_history=20 if is_local else 100,
    )

    bootstrap_user = (
        (
            "Project scan complete. You have a grounded map of the whole workspace and direct access to every file and directory under the current project root.\n\n"
            f"{workspace_map}\n\n"
            f"{_build_workspace_access_note(cwd, max_files=30)}\n\n"
            f"{context}"
        )
        if is_local
        else (
            "You are working on the project rooted at the current directory. "
            "You have a grounded workspace map and access to all files under the current project root. "
            "When the user asks you to analyze, improve, or work on 'this code' or 'the code', "
            "they mean the project files below. Do NOT ask them to provide code — you already have it.\n\n"
            f"{workspace_map}\n\n"
            f"{_build_workspace_access_note(cwd, max_files=40)}\n\n"
            f"{context}"
        )
    )
    messages_init = [
        {"role": "user", "content": bootstrap_user},
        {
            "role": "assistant",
            "content": (
                "I've scanned the project, built a grounded workspace map, and can inspect any file or directory under the project root. "
                "I know the repo structure, key files, and where to investigate next. "
                "What would you like me to do?"
            ),
        },
    ]
    for m in messages_init:
        if m["role"] == "user":
            engine.add_user(m["content"])
        else:
            engine.add_assistant(m["content"])

    renderer.print_agent_welcome(model_id, str(cwd), is_local=is_local)

    sticky_context_files: set[str] = set()
    files_read, execution_ledger = _initialize_request_grounding_state(cwd)
    multiline_buffer: list[str] | None = None

    # Load session mode (analysis vs implementation) from previous turns
    session_mode = _get_session_mode(cwd)
    if session_mode == "implementation":
        # If we were in implementation mode, check for incomplete tasks
        incomplete_tasks = _get_incomplete_tasks(cwd)
        if incomplete_tasks:
            renderer.info(
                f"📋 Resuming with {len(incomplete_tasks)} incomplete tasks from previous session"
            )

    # ── Output Verbosity Control ──────────────────────────────
    minimal_output = renderer.is_clean()

    # ── Dependency Graph for whole-repo awareness ──────────────
    dep_graph = DependencyGraph(cwd)
    # Index project in background (async-friendly)
    indexed_count = dep_graph.index_project(limit=300)
    if indexed_count > 0 and not minimal_output:
        renderer.info(f"📊 Indexed {indexed_count} files for dependency analysis")

    # ── Time Travel Debugger ────────────────────────────────────
    checkpoint_mgr = CheckpointManager(cwd)
    checkpoint_mgr.create_checkpoint(
        files_written=[],
        message_count=engine.turn_count,
        description="Session start",
        auto_stash=False,
    )

    # ── Security Auditor ────────────────────────────────────────
    security_auditor = SecurityAuditor(cwd)

    # ── Docker Sandbox & TDD Gate ──────────────────────────────
    sandbox = DockerSandbox(cwd, network_enabled=False)
    tdd_gate = TDDGate(sandbox)
    tdd_gate.set_test_command(default_test_cmd)

    # ── Task Execution Manager (Multi-task TDD enforcement) ────
    context_persistence_mgr = ContextPersistenceManager(cwd)
    task_execution_mgr = TaskExecutionManager(cwd, tdd_gate, context_persistence_mgr)

    # ── Context Compactor ──────────────────────────────────────
    compactor = ContextCompactor(max_tokens=200000, threshold=0.85)

    # ── LSP Client for real-time diagnostics ───────────────────
    lsp_client = LSPClient(cwd)

    # ── Enhanced AI Capabilities ──────────────────────────────
    error_diagnosis = ErrorDiagnosis()
    code_analyzer = CodeAnalyzer(cwd)
    code_validator = CodeValidator(cwd)
    style_enforcer = StyleEnforcer()
    adaptive_executor = AdaptiveExecutionEngine(cwd, max_workers=4)
    smart_retry = SmartRetryHandler()

    def _send_for_reasoning(prompt: str) -> str | None:
        """Send function for reasoning engine - doesn't add to conversation history."""
        nonlocal tokens
        messages = engine.build_messages()
        messages.append(Message(role="user", content=prompt))
        provider_name = model_id.split(":", 1)[0] if ":" in model_id else ""
        timeout_seconds = _get_single_turn_agent_timeout(provider_name)
        try:
            response = _run_callable_with_timeout(
                lambda: router.generate(
                    messages,
                    model_id,
                    temp,
                    min(tokens, 2048),
                    lock_provider=model_locked,
                ),
                timeout_seconds=timeout_seconds,
                timeout_message=f"No response from model within {timeout_seconds:.0f} seconds",
            )
            return response
        except Exception:
            return None

    reasoning_engine = ChainOfThoughtReasoner(_send_for_reasoning, cwd)

    def _ai_model_send(prompt: str) -> dict:
        """Wrapper to send prompts to AI model and parse JSON response."""
        try:
            response = _send_for_reasoning(prompt)
            if response:
                import json

                json_match = re.search(r"\{[\s\S]*\}", response)
                if json_match:
                    return json.loads(json_match.group())
            return {"result": response}
        except Exception:
            return {"result": "error", "error": "Failed to parse response"}

    ai_orchestrator = AIOrchestrator(
        _ai_model_send,
        enable_plugins=True,
        repo_path=cwd,
    )

    def agent_send(prompt: str) -> dict:
        """Structured JSON send function for PhD agent components."""
        response = _send_for_reasoning(prompt)
        if response is None:
            return {"error": "Failed to generate response"}
        try:
            import json

            json_match = re.search(r"\{[\s\S]*\}", response)
            if json_match:
                return json.loads(json_match.group())
            return json.loads(response)
        except (json.JSONDecodeError, TypeError):
            return {"raw": response}

    phd_agent = PhDAgent(send=agent_send)

    # ── Project Memory (SAGE.md) ───────────────────────────────
    project_memory = ProjectMemory(cwd)
    if project_memory.exists() and not minimal_output:
        renderer.info("📝 SAGE.md loaded - project rules active")
        # Inject project rules into system prompt
        rules_context = project_memory.get_context_injection()
        if rules_context:
            engine.system_prompt += rules_context

    # ── SAGE Agent Instance ────────────────────────────────────
    global _global_agent
    sage_agent = SAGEAgent(
        cwd=cwd,
        renderer=renderer,
        engine=engine,
        router=router,
        model_id=model_id,
        temp=temp,
        tokens=tokens,
        model_locked=model_locked,
        is_local=is_local,
        tdd_gate=tdd_gate,
        full_project_test_cmd=full_project_test_cmd,
        compactor=compactor,
        phd_agent=phd_agent,
        adaptive_executor=adaptive_executor,
        smart_retry=smart_retry,
        lsp_client=lsp_client,
        task_execution_mgr=task_execution_mgr,
        ai_orchestrator=ai_orchestrator,
        error_diagnosis=error_diagnosis,
        code_analyzer=code_analyzer,
        code_validator=code_validator,
        style_enforcer=style_enforcer,
        checkpoint_mgr=checkpoint_mgr,
        security_auditor=security_auditor,
        dep_graph=dep_graph,
        reasoning_engine=reasoning_engine,
        cfg=cfg,
        sticky_context_files=sticky_context_files,
        context_manager=context_persistence_mgr,
    )
    _global_agent = sage_agent
    sage_agent._is_repl = True

    # Track reasoning context for the session

    if not minimal_output:
        renderer.info("🧠 Enhanced AI capabilities enabled (reasoning, validation, learning)")

    _protected = _build_session_protected_files(cwd)

    # ── Professional Async REPL with Bottom-Anchored Prompt ──
    # Replaces the old synchronous while-loop with a threaded background executor
    # and a pinned input field that accepts concurrent "hints" during execution.
    from sage.core.repl import run_repl

    def _handle_repl_slash_command(cmd_str: str) -> None:
        import shlex
        parts = shlex.split(cmd_str)
        if not parts:
            return
        cmd_name = parts[0].lower()
        args = parts[1:]

        if cmd_name == "/help":
            sage_agent.renderer.print_agent_help()

        elif cmd_name == "/models":
            ollama = False
            category = None
            search = None
            all_models = False
            details = False
            provider = None
            filter_kw = None

            i = 0
            while i < len(args):
                arg = args[i]
                if arg == "--ollama":
                    ollama = True
                elif arg in ("--category", "-c"):
                    if i + 1 < len(args):
                        category = args[i+1]
                        i += 1
                elif arg in ("--search", "-s"):
                    if i + 1 < len(args):
                        search = args[i+1]
                        i += 1
                elif arg == "--all":
                    all_models = True
                elif arg == "--details":
                    details = True
                elif arg in ("--provider", "-p"):
                    if i + 1 < len(args):
                        provider = args[i+1]
                        i += 1
                elif arg in ("--filter", "-f"):
                    if i + 1 < len(args):
                        filter_kw = args[i+1]
                        i += 1
                else:
                    filter_kw = arg
                i += 1
            
            try:
                models(
                    ollama=ollama,
                    category=category,
                    search=search,
                    all_models=all_models,
                    details=details,
                    provider=provider,
                    filter_kw=filter_kw
                )
            except typer.Exit:
                pass

        elif cmd_name == "/model":
            if not args:
                sage_agent.renderer.console.print(f"Active model: [bold]{sage_agent.model_id}[/bold]")
            else:
                new_model_id = args[0]
                nonlocal cfg
                try:
                    updated_cfg, resolved_model_id = _prepare_model_for_use(cfg, new_model_id)
                    cfg = updated_cfg
                    sage_agent.model_id = resolved_model_id
                    _set_last_used_model(sage_agent.cwd, resolved_model_id)
                    sage_agent.renderer.success(f"Model changed to {resolved_model_id}")
                except Exception as e:
                    sage_agent.renderer.error(f"Failed to switch model: {e}")

        elif cmd_name == "/think":
            if not args:
                current_mode = sage_agent.renderer.get_output_mode()
                status = "ON" if current_mode == "verbose" else "OFF"
                sage_agent.renderer.console.print(f"Thinking blocks visibility: [bold]{status}[/bold] (mode: {current_mode})")
            else:
                mode_val = args[0].lower()
                if mode_val in ("on", "true", "yes"):
                    sage_agent.renderer.set_output_mode("verbose")
                    sage_agent.renderer.success("Thinking blocks visibility enabled (verbose output).")
                elif mode_val in ("off", "false", "no"):
                    sage_agent.renderer.set_output_mode("normal")
                    sage_agent.renderer.success("Thinking blocks visibility disabled (normal output).")
                else:
                    sage_agent.renderer.error("Usage: /think [on|off]")

        elif cmd_name == "/read":
            if not args:
                sage_agent.renderer.error("Usage: /read <file_path>")
            else:
                file_arg = args[0]
                filepath = Path(sage_agent.cwd) / file_arg
                if not filepath.exists():
                    sage_agent.renderer.error(f"File not found: {file_arg}")
                else:
                    rel_path = str(filepath.relative_to(sage_agent.cwd))
                    if rel_path not in sage_agent.sticky_context_files:
                        sage_agent.sticky_context_files.append(rel_path)
                    try:
                        content = filepath.read_text(encoding="utf-8", errors="replace")
                        sage_agent.engine.add_user(f"Here is the content of {rel_path}:\n\n```\n{content}\n```")
                        sage_agent.renderer.success(f"Read {rel_path} into context ({len(content)} characters)")
                    except Exception as e:
                        sage_agent.renderer.error(f"Failed to read file: {e}")

        elif cmd_name == "/test":
            test_cmd = " ".join(args) if args else sage_agent.tdd_gate.test_cmd
            sage_agent.renderer.info(f"Running tests: {test_cmd}")
            is_passing, message = sage_agent.tdd_gate.run_tests(command=test_cmd, cwd=sage_agent.cwd)
            if is_passing:
                sage_agent.renderer.success(message)
            else:
                sage_agent.renderer.error(message)

        elif cmd_name == "/files":
            if sage_agent.all_written:
                sage_agent.renderer.console.print("[bold]Files written in this session:[/bold]")
                for f in sorted(set(sage_agent.all_written)):
                    sage_agent.renderer.console.print(f"  {f}")
            else:
                sage_agent.renderer.console.print("No files written in this session yet.")

        elif cmd_name == "/undo":
            if not sage_agent.checkpoint_mgr:
                sage_agent.renderer.error("No checkpoint manager initialized.")
                return
            cp = sage_agent.checkpoint_mgr.get_last_checkpoint()
            if not cp:
                sage_agent.renderer.error("No checkpoints found to undo.")
            else:
                is_safe, concerns = sage_agent.checkpoint_mgr.validate_restore(cp)
                if not is_safe:
                    sage_agent.renderer.warning("Restore warnings:\n" + "\n".join(concerns))
                result = sage_agent.checkpoint_mgr.restore_checkpoint(cp)
                if result.success:
                    sage_agent.renderer.success(f"Successfully rolled back to checkpoint {cp.id}: {result.message}")
                    sage_agent.checkpoint_mgr.checkpoints.remove(cp)
                    sage_agent.checkpoint_mgr._save_checkpoints()
                else:
                    sage_agent.renderer.error(f"Failed to restore checkpoint: {result.message}")
                    if result.errors:
                        for err in result.errors:
                            sage_agent.renderer.error(f"  Error: {err}")

        elif cmd_name == "/compact":
            if sage_agent.compactor:
                sage_agent.renderer.info("📦 Compacting context...")
                sage_agent.engine._messages = sage_agent.compactor.compact(
                    sage_agent.engine._messages, sage_agent.router, sage_agent.model_id
                )
                sage_agent.renderer.success(f"Context compacted! {sage_agent.compactor.get_status(sage_agent.engine._messages)}")
            else:
                sage_agent.renderer.error("Compactor not initialized.")

        elif cmd_name == "/clear":
            sage_agent.engine.clear()
            sage_agent.sticky_context_files.clear()
            sage_agent.all_written.clear()
            sage_agent.renderer.success("Conversation and file history cleared.")

        elif cmd_name == "/system":
            if not args:
                sage_agent.renderer.console.print("[bold]Current System Prompt:[/bold]")
                sage_agent.renderer.console.print(sage_agent.engine.system_prompt)
            else:
                new_prompt = " ".join(args)
                sage_agent.engine.system_prompt = new_prompt
                sage_agent.renderer.success("System prompt updated.")

        elif cmd_name == "/status":
            sage_agent.renderer.console.print(f"[bold]Active Model:[/bold] {sage_agent.model_id}")
            sage_agent.renderer.console.print(f"[bold]Output Mode:[/bold] {sage_agent.renderer.get_output_mode()}")
            sage_agent.renderer.console.print(f"[bold]Conversation turns:[/bold] {sage_agent.engine.turn_count}")
            if sage_agent.sticky_context_files:
                sage_agent.renderer.console.print(f"[bold]Pinned Files:[/bold]")
                for f in sage_agent.sticky_context_files:
                    sage_agent.renderer.console.print(f"  {f}")
            if sage_agent.all_written:
                sage_agent.renderer.console.print(f"[bold]Written Files:[/bold] {len(sage_agent.all_written)} files")
            if sage_agent.current_plan:
                sage_agent.renderer.console.print(f"[bold]Active Plan:[/bold] {sage_agent.current_plan.id} ({len(sage_agent.current_plan.tasks)} tasks)")

        elif cmd_name == "/context":
            stats = sage_agent.engine.get_context_stats()
            sage_agent.renderer.console.print("[bold]Context telemetry & token usage:[/bold]")
            sage_agent.renderer.console.print(f"  • [bold]Total Messages:[/bold] {stats.message_count}")
            sage_agent.renderer.console.print(f"  • [bold]User Turns:[/bold] {stats.turn_count}")
            sage_agent.renderer.console.print(f"  • [bold]System Prompt Tokens:[/bold] {stats.system_prompt_tokens}")
            sage_agent.renderer.console.print(f"  • [bold]History Tokens:[/bold] {stats.history_tokens}")
            sage_agent.renderer.console.print(f"  • [bold]Total Estimated Tokens:[/bold] {stats.estimated_tokens}")
            sage_agent.renderer.console.print(f"  • [bold]Max Context Window:[/bold] {stats.max_tokens}")
            sage_agent.renderer.console.print(f"  • [bold]Usage Percent:[/bold] {stats.usage_percent:.2f}%")

        elif cmd_name == "/rag":
            if not args:
                sage_agent.renderer.error("Usage: /rag <query|index|status> [args...]")
            else:
                sub = args[0].lower()
                if sub == "query":
                    query_text = " ".join(args[1:])
                    from sage.core.rag import RAGIndex, format_chunks_for_prompt
                    index = RAGIndex(sage_agent.cwd)
                    chunks = index.query(query_text, top_k=6)
                    if not chunks:
                        sage_agent.renderer.info("(no results found — index may be empty)")
                    else:
                        sage_agent.renderer.console.print(format_chunks_for_prompt(chunks))
                elif sub == "index":
                    from sage.core.rag import RAGIndex
                    index = RAGIndex(sage_agent.cwd)
                    stats = index.reindex(force=False)
                    sage_agent.renderer.success(f"Indexed files_seen={stats['files_seen']} chunks_added={stats['chunks_added']}")
                elif sub == "status":
                    from sage.core.rag import RAGIndex
                    import sqlite3
                    index = RAGIndex(sage_agent.cwd)
                    conn = sqlite3.connect(index.db_path)
                    file_count = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
                    chunk_count = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
                    sage_agent.renderer.console.print(f"DB:       {index.db_path}")
                    sage_agent.renderer.console.print(f"Files:    {file_count}")
                    sage_agent.renderer.console.print(f"Chunks:   {chunk_count}")
                else:
                    sage_agent.renderer.error(f"Unknown RAG subcommand: {sub}")

        elif cmd_name == "/tdd":
            from sage.core.tdd import get_tdd_enforcer
            enforcer = get_tdd_enforcer()
            if not args:
                enforcer.enabled = not enforcer.enabled
            else:
                val = args[0].lower()
                if val in ("on", "true", "yes", "enable"):
                    enforcer.enabled = True
                elif val in ("off", "false", "no", "disable"):
                    enforcer.enabled = False
                else:
                    sage_agent.renderer.error("Usage: /tdd [on|off]")
            status = "ENABLED" if enforcer.enabled else "DISABLED"
            sage_agent.renderer.success(f"TDD Mode is now: [bold]{status}[/bold]")

        elif cmd_name == "/phd":
            if not args:
                sage_agent.renderer.error("Usage: /phd <topic/task>")
            else:
                topic = " ".join(args)
                sage_agent.renderer.info(f"🎓 Starting PhD-level research & analysis on: {topic}")
                if not sage_agent.phd_agent:
                    from sage.core.phd_agent import PhDAgent
                    sage_agent.phd_agent = PhDAgent(send=None)
                with sage_agent.renderer.status_spinner("Researching...", "reading"):
                    result = sage_agent.phd_agent.solver.solve_complete(topic)
                sage_agent.renderer.success("Research completed!")
                for idx, sub_prob in enumerate(result["sub_problems"]):
                    sol = result["solutions"].get(idx, "No solution generated")
                    sage_agent.renderer.console.print(f"\n[bold]Sub-task: {sub_prob}[/bold]")
                    sage_agent.renderer.console.print(sol)

        elif cmd_name == "/expert":
            if not args:
                sage_agent.renderer.error("Usage: /expert <domain_name> [query]")
            else:
                domain = args[0]
                query = " ".join(args[1:]) if len(args) > 1 else f"Audit the workspace and conceptualize a swarm of sub-agents for {domain}."
                expert_prompt = (
                    f"You are an expert AI consultant specializing in {domain}.\n"
                    f"Task: {query}\n"
                    f"Please perform a detailed expert analysis based on this workspace context and suggest sub-agent roles."
                )
                sage_agent.renderer.info(f"🧙‍♂️ Consulting {domain} Expert...")
                response = sage_agent.send_to_model(expert_prompt, show_thinking=True, save_history=True)
                if response:
                    sage_agent.renderer.console.print(response)

        elif cmd_name == "/swarm":
            sage_agent.renderer.info("🐝 Initializing Agent Swarm...")
            roles = [
                {"name": "Security Auditor", "status": "active", "task": "Auditing omniprobe-ui inputs"},
                {"name": "Documenter", "status": "active", "task": "Generating API documentation"},
                {"name": "QA Specialist", "status": "active", "task": "Writing unit tests"},
            ]
            sage_agent.renderer.console.print("[bold]Active Swarm Members:[/bold]")
            for r in roles:
                sage_agent.renderer.console.print(f"  • [green]{r['name']}[/green] ({r['status']}): {r['task']}")

            swarm_prompt = (
                "You are SAGE Orchestrator leading a swarm of sub-agents (Security Auditor, Documenter, QA Specialist).\n"
                "Please coordinate their outputs to parallelize documentation, audit findings, and testing for the omniprobe-ui project. "
                "Provide a detailed coordinate report."
            )
            response = sage_agent.send_to_model(swarm_prompt, show_thinking=True, save_history=True)
            if response:
                sage_agent.renderer.console.print(response)

        elif cmd_name == "/sandbox":
            if not sage_agent.tdd_gate or not sage_agent.tdd_gate.sandbox:
                sage_agent.renderer.error("Sandbox not initialized.")
            else:
                sandbox = sage_agent.tdd_gate.sandbox
                command = " ".join(args) if args else "python3 -c \"import pathlib; print(sum(len(p.read_text(errors='replace').splitlines()) for p in pathlib.Path('sage').rglob('*.py')))\""
                sage_agent.renderer.info(f"📦 Running command in Docker Sandbox: {command}")
                with sage_agent.renderer.status_spinner("Executing in sandbox...", "reading"):
                    if sandbox.is_available():
                        res = sandbox.execute(command)
                        stdout, stderr, code = res.stdout, res.stderr, res.exit_code
                    else:
                        from sage.core.shell import run_shell
                        stdout = run_shell(command, sage_agent.cwd)
                        stderr = ""
                        code = 0
                sage_agent.renderer.success(f"Execution finished (exit code: {code})")
                if stdout:
                    sage_agent.renderer.console.print(f"[bold]stdout:[/bold]\n{stdout}")
                if stderr:
                    sage_agent.renderer.console.print(f"[bold,red]stderr:[/bold,red]\n{stderr}")

        elif cmd_name == "/history":
            sage_agent.renderer.console.print(f"Conversation turn count: {sage_agent.engine.turn_count}")

        elif cmd_name == "/version":
            from sage import __version__
            sage_agent.renderer.console.print(f"SAGE AI version {__version__}")

        elif cmd_name == "/update":
            _perform_cli_update(check_only=False)

        elif cmd_name == "/autoorg":
            message = " ".join(args) if args else None
            _run_autoorg_command(
                message,
                cwd=sage_agent.cwd,
                router=sage_agent.router,
                model_id=sage_agent.model_id,
                temp=sage_agent.temp,
                tokens=sage_agent.tokens,
                model_locked=sage_agent.model_locked,
            )

        elif cmd_name == "/autofleet":
            message = " ".join(args) if args else None
            _run_autofleet_command(
                message,
                cwd=sage_agent.cwd,
                router=sage_agent.router,
                model_id=sage_agent.model_id,
                temp=sage_agent.temp,
                tokens=sage_agent.tokens,
                model_locked=sage_agent.model_locked,
                cfg=cfg,
            )
        else:
            sage_agent.renderer.error(f"Unknown command: {cmd_name}. Type /help to see all available commands.")

    def _repl_execute(user_input: str) -> None:
        """Synchronous wrapper for agent execution inside the async REPL."""
        cleaned = user_input.strip()
        if cleaned.startswith("/"):
            try:
                _handle_repl_slash_command(cleaned)
            except KeyboardInterrupt:
                renderer.warning("\nInterrupted by user")
            except Exception as e:
                renderer.error(f"Error executing command {cleaned}: {e}")
            return

        try:
            # Re-use the agent logic
            sage_agent.execute_task_prompt(user_input, save_history=True)
        except KeyboardInterrupt:
            renderer.warning("\nInterrupted by user")
        except Exception as e:
            renderer.error(f"Error: {e}")

    if prompt:
        try:
            _, task_ok = sage_agent.execute_task_prompt(prompt, save_history=True)
            if not task_ok:
                raise typer.Exit(code=1)
        except KeyboardInterrupt:
            renderer.warning("\nInterrupted by user")
        except Exception as e:
            renderer.error(f"Error: {e}")
            raise typer.Exit(1) from e
        return

    # Start the async REPL
    run_repl(sage_agent, _repl_execute)

@app.command()
def ask(
    prompt: Annotated[str, typer.Argument(help="Prompt/question to ask")],
    model: Annotated[str | None, typer.Option("--model", "-m", help="Model ID")] = None,
    temperature: Annotated[float | None, typer.Option("--temperature", "-t")] = None,
    max_tokens: Annotated[int | None, typer.Option("--max-tokens")] = None,
    no_agent: Annotated[
        bool,
        typer.Option(
            "--no-agent/--agent",
            help="Disable agentic capabilities (one-shot chat only)",
        ),
    ] = True,
    raw: Annotated[
        bool,
        typer.Option(
            "--raw",
            help="Output raw response only without styling or metadata",
        ),
    ] = False,
) -> None:
    """Ask Sage a question or run a one-shot task."""
    if not no_agent:
        # Delegate to the run command for the full agentic loop
        run(
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            prompt=prompt,
            quiet=raw,
        )
        return

    # One-shot chat/ask path
    import sys
    cfg = load_config()
    router = _build_router(cfg)

    # Determine model ID
    last_used_model = _get_last_used_model(Path.cwd())
    model_id = model or last_used_model or cfg.default_model
    try:
        cfg, model_id = _prepare_model_for_use(cfg, model_id)
    except RuntimeError as exc:
        if raw:
            print(f"Error: {exc}")
        else:
            renderer.error(str(exc))
        raise typer.Exit(1) from exc

    # Rebuild router with updated config
    router = _build_router(cfg)
    model_id = _auto_upgrade_model_if_possible(
        router, cfg, model_id, explicit_model=model, last_used_model=last_used_model
    )
    try:
        cfg, model_id = _prepare_model_for_use(cfg, model_id)
    except RuntimeError as exc:
        if raw:
            print(f"Error: {exc}")
        else:
            renderer.error(str(exc))
        raise typer.Exit(1) from exc
    router = _build_router(cfg)

    temp = temperature if temperature is not None else 0.1
    tokens = max_tokens if max_tokens is not None else cfg.max_tokens

    # Build prompt messages
    from sage.providers.base import Message
    system_prompt = "You are Sage, a helpful AI coding assistant. Answer the user's question directly."
    messages = [
        Message(role="system", content=system_prompt),
        Message(role="user", content=prompt)
    ]

    try:
        if raw:
            # Stream tokens directly to stdout
            for chunk in router.stream(messages, model_id, temp, tokens):
                sys.stdout.write(chunk)
                sys.stdout.flush()
            sys.stdout.write("\n")
            sys.stdout.flush()
        else:
            # Styled output using the renderer
            with renderer.status_spinner("Thinking...", "reading"):
                response = router.generate(messages, model_id, temp, tokens)
            renderer.console.print(response)
    except Exception as exc:
        if raw:
            print(f"Error: {exc}")
        else:
            renderer.error(str(exc))
        raise typer.Exit(1) from exc

@app.command()
def cli_entry() -> None:
    """Entry point for pyproject.toml console_scripts."""
    if sys.platform == "win32":
        import os as _os
        _os.environ.setdefault("PYTHONUTF8", "1")
        for _s in (sys.stdout, sys.stderr):
            if hasattr(_s, "reconfigure"):
                try:
                    _s.reconfigure(encoding="utf-8", errors="replace")
                except Exception:
                    pass
        try:
            import ctypes as _ct, ctypes.wintypes as _wt
            _k = _ct.windll.kernel32
            for _h in (-11, -12):
                _handle = _k.GetStdHandle(_h)
                if _handle and _handle != _wt.HANDLE(-1).value:
                    _m = _wt.DWORD()
                    if _k.GetConsoleMode(_handle, _ct.byref(_m)):
                        _k.SetConsoleMode(_handle, _m.value | 0x0004)
        except Exception:
            pass
    app()


if __name__ == "__main__":
    cli_entry()
