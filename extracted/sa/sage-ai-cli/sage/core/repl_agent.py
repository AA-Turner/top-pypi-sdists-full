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


class SAGEAgent:
    """Core SAGE Agent that orchestrates the REPL execution loop."""

    def __init__(
        self,
        cwd: Path,
        renderer,
        engine,
        router,
        model_id: str,
        temp: float,
        tokens: int,
        model_locked: bool,
        is_local: bool,
        tdd_gate=None,
        full_project_test_cmd: str = "",
        compactor=None,
        phd_agent=None,
        adaptive_executor=None,
        smart_retry=None,
        lsp_client=None,
        task_execution_mgr=None,
        ai_orchestrator=None,
        error_diagnosis=None,
        code_analyzer=None,
        code_validator=None,
        style_enforcer=None,
        checkpoint_mgr=None,
        security_auditor=None,
        dep_graph=None,
        reasoning_engine=None,
        cfg=None,
        sticky_context_files=None,
        context_manager=None,
    ):
        from sage.cli_core import _build_session_protected_files, _reset_evidence_tracker
        self.cwd = cwd
        self.renderer = renderer
        self.engine = engine
        self.router = router
        self.model_id = model_id
        self.temp = temp
        self.tokens = tokens
        self.model_locked = model_locked
        self.is_local = is_local
        self.tdd_gate = tdd_gate
        self.full_project_test_cmd = full_project_test_cmd
        self.compactor = compactor
        self.phd_agent = phd_agent
        self.adaptive_executor = adaptive_executor
        self.smart_retry = smart_retry
        self.lsp_client = lsp_client
        self.task_execution_mgr = task_execution_mgr
        self.ai_orchestrator = ai_orchestrator
        self.error_diagnosis = error_diagnosis
        self.code_analyzer = code_analyzer
        self.code_validator = code_validator
        self.style_enforcer = style_enforcer
        self.checkpoint_mgr = checkpoint_mgr
        self.security_auditor = security_auditor
        self.dep_graph = dep_graph
        self.reasoning_engine = reasoning_engine
        self.cfg = cfg
        self.context_manager = context_manager
        self.context = context_manager.get_current_context() if context_manager else None
        self._protected = _build_session_protected_files(cwd)

        self.current_plan: ExecutionPlan | None = None
        import queue
        self.hint_queue = queue.Queue()
        self._is_running = False
        self._is_repl = False
        self._model_timed_out: bool = False  # set when model exceeds timeout; blocks retry loop
        self.files_read: list[str] = []
        _reset_evidence_tracker()
        from sage.core.tools import ExecutionLedger
        self.execution_ledger = ExecutionLedger()
        self.last_prompt: str = ""
        self.last_written: list[str] = []
        self.all_written: list[str] = []
        self.sticky_context_files: list[str] = (
            list(sticky_context_files) if sticky_context_files else []
        )
        self.minimal_output = renderer.get_output_mode() == "clean"
        self._current_execution_context = None
        # Saved greenfield FILE_MANIFEST — populated by _execute_multistep during
        # the planning phase and consumed by the continuation loop in
        # execute_task_prompt.  Stored on the agent so it survives engine trimming.
        self._greenfield_manifest: list[str] = []
        self._is_greenfield_task: bool = False

    def send_to_model(
        self,
        user_msg: str,
        show_thinking: bool = True,
        system_prompt: str | None = None,
        save_history: bool = True,
        max_tokens: int | None = None,
    ) -> str | None:
        """Send a message to the model and stream the response."""
        from sage.cli_core import _add_to_conversation_memory, _add_to_output_history, _build_followup_context_from_recent_analysis, _build_messages_with_optional_resume_context, _build_resume_context_from_memory, _failure_loop_detector, _get_global_memory, _get_single_turn_agent_timeout, _run_callable_with_timeout, _update_global_memory
        if save_history:
            self.engine.add_user(user_msg)
            _add_to_conversation_memory(self.cwd, "user", user_msg)

        if self.compactor and self.compactor.needs_compaction(self.engine._messages):
            if not self.minimal_output:
                self.renderer.phase("compacting", "📦 Compacting context...")
            self.engine._messages = self.compactor.compact(
                self.engine._messages, self.router, self.model_id
            )
            if not self.minimal_output:
                self.renderer.info(
                    f"Context compacted to preserve memory. {self.compactor.get_status(self.engine._messages)}"
                )

        # ── Wiring SAGE run_hooks (T4, T8, T11, T12) on_pre_turn ────────
        from sage.core.run_hooks import on_pre_turn, on_post_turn
        available_models = [m.id for m in self.router.list_all_models()] if self.router else []
        pre_ctx = on_pre_turn(
            user_prompt=user_msg,
            cwd=self.cwd,
            cfg=self.cfg,
            available_models=available_models
        )

        resume_context = _build_resume_context_from_memory(self.cwd, user_msg)
        followup_context = _build_followup_context_from_recent_analysis(self.cwd, user_msg)
        
        # Selective Memory: Skip global memory if user asks for a fresh start
        user_lower = user_msg.lower()
        fresh_markers = ["fresh start", "new topic", "forget memory", "don't use context", "clear history", "start fresh"]
        is_fresh = any(m in user_lower for m in fresh_markers)
        
        global_memory = _get_global_memory() if not is_fresh else ""
        if is_fresh and not self.minimal_output:
            self.renderer.info("   Fresh start requested — skipping Global Memory injection.")
        
        mem_block = ""
        if global_memory:
            mem_block = f"## USER GLOBAL MEMORY (Across all threads)\n{global_memory}"
            
        supplemental_context = "\n\n".join(
            context for context in (mem_block, resume_context, followup_context, pre_ctx.rag_context) if context
        )

        if system_prompt:
            original_system_prompt = self.engine.system_prompt
            try:
                self.engine.system_prompt = system_prompt
                messages = _build_messages_with_optional_resume_context(
                    self.engine, supplemental_context
                )
            finally:
                self.engine.system_prompt = original_system_prompt
        else:
            messages = _build_messages_with_optional_resume_context(
                self.engine, supplemental_context
            )

        _effective_tokens = max_tokens if max_tokens is not None else self.tokens

        # Let the user know sage is actively sending to the model — important
        # for cloud models where the cold-start + large-prompt path can take
        # 30-120s before the first token appears.
        if not self.minimal_output and show_thinking:
            import sys as _sys
            # Messages may be Message dataclasses or dicts depending on engine state
            def _msg_len(m: object) -> int:
                if hasattr(m, "content"):
                    return len(m.content or "")  # type: ignore[union-attr]
                if isinstance(m, dict):
                    return len(m.get("content", "") or "")
                return 0
            _msg_chars = sum(_msg_len(m) for m in self.engine._messages[-3:])
            bullet = "-" if renderer.console.no_color else "◌"
            if _msg_chars > 2000:
                _sys.stderr.write(
                    f"  {bullet} Sending {_msg_chars // 1000}K chars to {self.model_id}"
                    f" — large prompt, first token may take 30-120s...\n"
                )
                _sys.stderr.flush()
            else:
                _sys.stderr.write(
                    f"  {bullet} Sending request to {self.model_id}...\n"
                )
                _sys.stderr.flush()

        try:
            start_time = time.time()
            if not show_thinking:
                provider_name = self.model_id.split(":", 1)[0] if ":" in self.model_id else ""
                timeout_seconds = _get_single_turn_agent_timeout(provider_name)
                response = _run_callable_with_timeout(
                    lambda: self.router.generate(
                        messages,
                        self.model_id,
                        self.temp,
                        _effective_tokens,
                        lock_provider=self.model_locked,
                    ),
                    timeout_seconds=timeout_seconds,
                    timeout_message=f"No response from model within {timeout_seconds:.0f} seconds",
                )
                duration_s = time.time() - start_time
                if response:
                    # ── Wiring SAGE run_hooks: Turn End (on_post_turn) ──────
                    on_post_turn(
                        user_prompt=user_msg,
                        output=response,
                        cfg=self.cfg,
                        success=True,
                        validator_signals=[],
                        files_written=0,
                        duration_s=duration_s,
                    )
                    if save_history:
                        self.engine.add_assistant(response)
                        _add_to_conversation_memory(self.cwd, "assistant", response)
                    _add_to_output_history(self.cwd, response, user_msg)
                    _failure_loop_detector.reset()
                    
                    # Process Global Memory Update
                    if "MEMORY_UPDATE:" in response:
                        import re as _re
                        _match = _re.search(r"MEMORY_UPDATE:\s*(.*)", response, _re.IGNORECASE | _re.DOTALL)
                        if _match:
                            _new_mem = _match.group(1).strip()
                            _old_mem = _get_global_memory()
                            _merged = f"{_old_mem}\n{_new_mem}".strip() if _old_mem else _new_mem
                            _update_global_memory(_merged[:4000])

                return response or None

            result = self.renderer.stream_tokens_with_phase(
                self.router.stream(
                    messages, self.model_id, self.temp, _effective_tokens, lock_provider=self.model_locked
                ),
                model_id=self.model_id if not self.minimal_output else "",
                return_rejection_info=True,
            )
            duration_s = time.time() - start_time

            if isinstance(result, tuple):
                response, was_rejected, rejection_reason = result
            else:
                response = result
                was_rejected = False
                rejection_reason = ""

            if was_rejected:
                _failure_loop_detector.record_error(f"STREAMING REJECTED: {rejection_reason}")
                self.renderer.debug_warning(f"Streaming output filtered: {rejection_reason}")
                return None

            if response:
                # ── Wiring SAGE run_hooks: Turn End (on_post_turn) ──────
                on_post_turn(
                    user_prompt=user_msg,
                    output=response,
                    cfg=self.cfg,
                    success=True,
                    validator_signals=[],
                    files_written=0,
                    duration_s=duration_s,
                )
                if save_history:
                    self.engine.add_assistant(response)
                    _add_to_conversation_memory(self.cwd, "assistant", response)
                _add_to_output_history(self.cwd, response, user_msg)
                _failure_loop_detector.reset()

                # Process Global Memory Update
                if "MEMORY_UPDATE:" in response:
                    import re as _re
                    _match = _re.search(r"MEMORY_UPDATE:\s*(.*)", response, _re.IGNORECASE | _re.DOTALL)
                    if _match:
                        _new_mem = _match.group(1).strip()
                        _old_mem = _get_global_memory()
                        _merged = f"{_old_mem}\n{_new_mem}".strip() if _old_mem else _new_mem
                        _update_global_memory(_merged[:4000])

            return response or None

        except renderer.StreamingTimeoutError as exc:
            self._model_timed_out = True
            self.renderer.error(str(exc))
            self.renderer.warning(
                "Model timed out. For large local models try: "
                "OLLAMA_REQUEST_TIMEOUT=600 ollama serve  "
                "or switch to a smaller model with /model."
            )
            return None
        except Exception as exc:
            err_str = str(exc)
            self.renderer.error(err_str)
            if "All providers failed" in err_str:
                self.renderer.warning(
                    "No model is currently available. Try:\n"
                    "  • Wait a moment if rate-limited (OpenRouter caps reset hourly)\n"
                    "  • Start Ollama: `ollama serve`\n"
                    "  • Switch model: `/model ollama:llama3.2`\n"
                    "  • Check connectivity: `sage doctor`"
                )
            raise

    def process_response(
        self,
        response: str,
        tool_depth: int = 0,
        send_fn: Callable[[str], str | None] | None = None,
        display_analysis_response: bool = False,
        phase_name: str | None = None,
    ) -> tuple[list[str], str]:
        """Process model response: write files, execute tool commands, run bash blocks.

        Handles the full agent loop:
        1. Execute READ:/SEARCH:/RUN: tool commands → feed results back to model
        2. Extract and write FILE: blocks
        3. Execute ```bash blocks
        Returns (list of written files, final model response).
        """
        from sage.cli_core import _add_to_conversation_memory, _build_context_aware_validation_retry_prompt, _build_tool_followup_prompt, _detect_aider_style_diff_garbage, _detect_non_english_code_identifiers, _detect_repetitive_filler, _detect_tool_description_vs_execution, _emit_grounded_analysis_failure, _execute_tool_commands, _extract_and_write_files, _extract_tool_commands_structured, _get_current_classification, _get_current_task_prompt, _get_evidence_tracker, _normalize_workspace_relative_path, _response_describes_code_without_file_blocks
        # Get classification at the very beginning to avoid UnboundLocalError (P3-71)
        effective_classification = _get_current_classification()
        is_analysis_response = bool(effective_classification and effective_classification.read_only)

        # Nudge plan status if we are in a known phase
        if phase_name and self.current_plan:
            self._sync_plan_task_status(phase_name, "in_progress", effective_classification)

        send = send_fn or self.send_to_model

        def _retry_invalid_readonly_response(violations: list[str]) -> tuple[list[str], str] | None:
            from sage.cli_core import _build_context_aware_validation_retry_prompt, _get_current_task_prompt
            if not (is_analysis_response and tool_depth < 4):
                return None
            current_task_prompt = _get_current_task_prompt()
            if not current_task_prompt:
                return None
            retry_prompt = _build_context_aware_validation_retry_prompt(
                task_prompt=current_task_prompt,
                cwd=self.cwd,
                violations=violations,
                current_files_read=list(self.files_read),
                is_analysis=True,
            )
            if send is self.send_to_model:
                retry_response = self.send_single_turn_to_model(retry_prompt)
            else:
                retry_response = send(retry_prompt)
            if not retry_response:
                return None
            return self.process_response(
                retry_response,
                tool_depth + 1,
                send_fn=send,
                display_analysis_response=True,
                phase_name=phase_name,
            )

        def _retry_invalid_code_output(violations: list[str]) -> tuple[list[str], str] | None:
            """Retry path for BUILD/code-output mode (not analysis).

            Fires when the response had a hard violation we can fix by
            re-prompting — currently: CJK identifiers in code, or the
            aider/Cursor `<<<<<<< SEARCH … >>>>>>> REPLACE` diff format
            that sage doesn't parse. Bounded by tool_depth to prevent
            infinite loops on persistently-broken models.
            """
            from sage.cli_core import _get_current_task_prompt
            if tool_depth >= 3:
                return None
            current_task_prompt = _get_current_task_prompt()
            if not current_task_prompt:
                return None
            retry_prompt = (
                f"Your previous response was rejected for these reasons:\n"
                + "\n".join(f"  • {v}" for v in violations)
                + "\n\n"
                "Re-do the response with these MANDATORY rules:\n"
                "  1. ALL code MUST use English-only identifiers (function "
                "names, class names, variable names, import targets). "
                "Non-ASCII letters are forbidden in code structure. "
                "Comments and string literals may contain any language.\n"
                "  2. To write a file, output a `FILE: <relative-path>` line "
                "followed by the COMPLETE file contents inside a fenced "
                "code block. Do NOT use `<<<<<<< SEARCH … >>>>>>> REPLACE` "
                "markers — sage cannot apply those.\n"
                "  3. The original task was:\n\n"
                f"{current_task_prompt}\n"
            )
            if send is self.send_to_model:
                retry_response = self.send_single_turn_to_model(retry_prompt)
            else:
                retry_response = send(retry_prompt)
            if not retry_response:
                return None
            return self.process_response(
                retry_response,
                tool_depth + 1,
                send_fn=send,
                phase_name=phase_name,
            )

        def _retry_failed_file_writes(failed: dict[str, str]) -> tuple[list[str], str] | None:
            if tool_depth >= 3:
                return None
            from sage.cli_core import _get_current_task_prompt
            current_task_prompt = _get_current_task_prompt()
            if not current_task_prompt:
                return None

            bullets = "\n".join(f"  • File `{fp}`: {err}" for fp, err in failed.items())
            retry_prompt = (
                f"Your previous response attempted to write file(s), but they were REJECTED for these specific defects:\n"
                f"{bullets}\n\n"
                "Please regenerate the corrected file(s) with complete implementations, fixing all defects.\n"
                "Output the COMPLETE file contents using the `FILE: <path>` block format. Do not use placeholders or write incomplete code."
            )
            if send is self.send_to_model:
                retry_response = self.send_single_turn_to_model(retry_prompt)
            else:
                retry_response = send(retry_prompt)
            if not retry_response:
                return None
            return self.process_response(
                retry_response,
                tool_depth + 1,
                send_fn=send,
                phase_name=phase_name,
            )

        # ── Step 0: Informational Task Enforcement (P3-71) ──
        # Re-fetch classification to avoid scope/closure issues in nested calls
        _current_class = _get_current_classification()
        is_info = bool(_current_class and getattr(_current_class, "is_informational", False))
        if is_info:
            # For informational tasks, we STRICTLY forbid codebase tool execution
            # This prevents the model from reading project files for general knowledge requests
            # We strip any tool-like lines to prevent them from being displayed as executed
            clean_response = []
            for line in response.splitlines():
                if any(
                    line.strip().startswith(prefix)
                    for prefix in ["READ:", "SEARCH:", "RUN:", "FILE:"]
                ):
                    continue
                clean_response.append(line)
            return [], "\n".join(clean_response).strip()

        # ── Step 1: Execute tool commands (READ, SEARCH, RUN) ──
        if tool_depth >= 20:
            self.renderer.warning(
                "Tool loop depth limit reached. Requesting direct FILE: output next step."
            )
            return [], response

        # ── RESPONSE CLEANUP ──
        from sage.core.renderer import clean_malformed_tool_commands

        original_response = response
        response = clean_malformed_tool_commands(response)

        if len(response) < len(original_response):
            removed_chars = len(original_response) - len(response)
            if removed_chars > 50:
                self.renderer.warning(
                    f"Cleaned {removed_chars} chars of malformed tool commands from response"
                )

        # ── BEHAVIORAL VALIDATION ──
        behavioral_violations = []
        hard_behavior_violation = False

        is_descriptive, mentioned_tools = _detect_tool_description_vs_execution(response)
        if is_descriptive:
            behavioral_violations.append(
                f"described tools ({', '.join(mentioned_tools[:3])}) instead of executing them"
            )
            hard_behavior_violation = any(
                marker in mentioned_tools
                for marker in (
                    "TOOL_REFUSAL",
                    "NONSTANDARD_TOOL_SYNTAX",
                    "ARGUMENTATIVE_BEHAVIOR",
                    "DESCRIBED_TOOL",
                    "BAD_PATTERN",
                )
            )

        is_filler, repetition_score = _detect_repetitive_filler(response)
        if is_filler:
            behavioral_violations.append(
                f"contains repetitive filler content (score: {repetition_score:.2f})"
            )

        # Code-output integrity: CJK identifiers + aider-style diff markers
        # are unconditional hard failures. We can't recover by "processing
        # anyway" because the artefact is broken — Python won't import a
        # module named `ai广告生成器`, and sage can't apply `<<<<<<< SEARCH`
        # blocks. Force a retry with the offenders quoted back to the model.
        has_cjk_ids, cjk_offenders = _detect_non_english_code_identifiers(response)
        if has_cjk_ids:
            behavioral_violations.append(
                "code blocks contain non-English identifiers — code must use "
                f"English-only names. Offenders: {cjk_offenders[:3]}"
            )
            hard_behavior_violation = True

        if _detect_aider_style_diff_garbage(response):
            behavioral_violations.append(
                "used `<<<<<<< SEARCH … >>>>>>> REPLACE` markers — sage's edit "
                "protocol is `FILE: <path>` followed by the full file content, "
                "not aider-style diffs"
            )
            hard_behavior_violation = True

        if behavioral_violations:
            violation_msg = "; ".join(behavioral_violations)
            has_valid_tool = bool(
                re.search(r"^(READ|SEARCH|RUN|FILE):\s*\S", response, re.MULTILINE)
            )
            has_file_blocks = "FILE:" in response
            has_bash_blocks = bool(_extract_bash_blocks(response))
            has_processable_content = has_valid_tool or has_file_blocks or has_bash_blocks

            if has_processable_content and not is_analysis_response and not hard_behavior_violation:
                self.renderer.warning(
                    f"Response has issues ({violation_msg}), but contains valid content - processing anyway"
                )
            else:
                recovered = _retry_invalid_readonly_response(
                    [f"Behavioral violation: {violation_msg}."]
                )
                if recovered is not None:
                    return recovered
                # Code-output mode (build / agent) gets its own retry — the
                # read-only retry above only fires for analysis responses.
                # If we're here because of CJK identifiers or aider-style
                # diff markers, re-prompt with explicit guidance instead of
                # giving up.
                if not is_analysis_response and hard_behavior_violation:
                    code_recovered = _retry_invalid_code_output(behavioral_violations)
                    if code_recovered is not None:
                        return code_recovered
                if is_analysis_response:
                    _emit_grounded_analysis_failure(
                        self.cwd,
                        "The model could not produce a validated, file-grounded analysis "
                        "response after retrying the invalid output.",
                    )
                    return [], response
                self.renderer.error(
                    f"❌ Response rejected - behavioral violations: {violation_msg}"
                )
                return [], response

        if _response_describes_code_without_file_blocks(response):
            recovered = _retry_invalid_readonly_response(
                [
                    "Response described code changes or implementation steps during read-only analysis. "
                    "Provide grounded findings only."
                ]
            )
            if recovered is not None:
                return recovered
            self.renderer.warning(
                "Response described code changes without FILE blocks. Ignoring shell execution until the model emits writable files."
            )
            return [], response

        # ── Step 1a: Write FILE: blocks BEFORE executing tool commands ────────
        # CRITICAL: If the model emits FILE: blocks AND RUN:/READ: commands in
        # the same response (common in scaffold responses: "FILE: x.py … RUN:
        # pytest"), the old order (tool commands first → early return on followup)
        # caused the FILE: blocks to NEVER be written.  Writing files first
        # ensures scaffold files land on disk regardless of what tool commands
        # follow.  Tool commands (READ:/SEARCH:) that need file content to exist
        # first will still work correctly because the files are now on disk before
        # we process them.
        _pre_tool_written: list[str] = []
        failed_writes = {}
        if "FILE:" in response or "```" in response:
            self.renderer.set_bottom_dock_status("Writing files to disk...")
            _pre_tool_written = _extract_and_write_files(
                response, self.cwd, protected_files=self._protected, files_read=self.files_read, failed_writes=failed_writes
            )
            if _pre_tool_written:
                self.last_written = _pre_tool_written
                self.all_written.extend(_pre_tool_written)
                self.renderer.print_files_written(_pre_tool_written)
                files_summary = f"Wrote {len(_pre_tool_written)} file(s): {', '.join(_pre_tool_written)}"
                _add_to_conversation_memory(
                    self.cwd, "assistant", files_summary, files_written=_pre_tool_written
                )

            if failed_writes:
                recovered = _retry_failed_file_writes(failed_writes)
                if recovered is not None:
                    retry_written, final_resp = recovered
                    return list(set(_pre_tool_written + retry_written)), final_resp

        # ── Step 1b: Execute tool commands ──
        from sage.core.tools import ToolType

        structured_calls = _extract_tool_commands_structured(response)
        tool_commands = []
        for call in structured_calls:
            if call.tool_type == ToolType.READ:
                tool_commands.append(("READ", call.arguments.get("path", "")))
            elif call.tool_type == ToolType.SEARCH:
                tool_commands.append(("SEARCH", call.arguments.get("pattern", "")))
            elif call.tool_type == ToolType.RUN:
                tool_commands.append(("RUN", call.arguments.get("command", "")))

        if tool_commands:
            # Check for repetition loops of failed operations to prevent infinite loops (especially on local/smaller models)
            tracker = _get_evidence_tracker()
            if tracker is not None:
                all_repeated_failures = True
                has_reads_or_searches = False
                for t_type, t_arg in tool_commands:
                    if t_type == "READ":
                        has_reads_or_searches = True
                        clean_arg = t_arg.strip().strip("`").strip()
                        if clean_arg.startswith("./"):
                            clean_arg = clean_arg[2:]
                        clean_arg = _normalize_workspace_relative_path(clean_arg, self.cwd)
                        if clean_arg not in tracker.failed_files:
                            all_repeated_failures = False
                            break
                    elif t_type == "SEARCH":
                        has_reads_or_searches = True
                        scope, pattern = _extract_scoped_prefix(t_arg)
                        pattern = _strip_search_comment(pattern)
                        pattern = _normalize_workspace_relative_path(pattern, self.cwd)
                        failed_searches = getattr(tracker, "failed_searches", set())
                        if pattern not in failed_searches:
                            all_repeated_failures = False
                            break
                    else:
                        # For RUN or other commands, do not block
                        all_repeated_failures = False
                        break
                
                if has_reads_or_searches and all_repeated_failures:
                    self.renderer.warning("⚠️ Repetition loop detected: all requested files/searches have already failed. Stopping tool execution.")
                    return [], response

            self.renderer.set_bottom_dock_status(f"Executing {len(tool_commands)} tool(s)...")
            # Print each tool action inline so the user sees real-time progress.
            # Format: "sage> READ: filename.py" — matches what the terminal was
            # showing when sage streamed its raw output, but now guaranteed
            # visible regardless of streaming mode.
            if not self.minimal_output:
                for tool_type, tool_arg in tool_commands:
                    if tool_type in ("READ", "SEARCH", "FILE"):
                        short = tool_arg[:80] if len(tool_arg) > 80 else tool_arg
                        self.renderer.console.print(
                            f"[dim]sage>[/dim] [cyan]{tool_type}:[/cyan] {short}",
                            highlight=False,
                        )
            tool_results = _execute_tool_commands(
                tool_commands,
                self.cwd,
                files_read=self.files_read,
                execution_ledger=self.execution_ledger,
            )
            if tool_results:
                has_embedded_actions = "FILE:" in response or bool(_extract_bash_blocks(response))
                per_result_limit = 1200 if self.is_local else 5000
                total_limit = 4000 if self.is_local else 20000
                compact_results: list[str] = []
                used = 0
                for item in tool_results:
                    trimmed = item if len(item) <= per_result_limit else item[:per_result_limit]
                    if used + len(trimmed) > total_limit:
                        break
                    compact_results.append(trimmed)
                    used += len(trimmed)

                tool_context = (
                    "\n\n".join(compact_results) if compact_results else "(no tool output)"
                )
                if not has_embedded_actions:
                    followup_prompt = _build_tool_followup_prompt(
                        tool_context,
                        _get_current_classification(),
                        self.cwd,
                    )
                    hide_readonly_followup = bool(
                        effective_classification
                        and effective_classification.read_only
                        and send is self.send_to_model
                        and phase_name
                        != "synthesis"  # Never hide follow-ups in the synthesis phase
                    )
                    if hide_readonly_followup:
                        followup = self.send_single_turn_to_model(followup_prompt)
                    else:
                        followup = send(followup_prompt)

                    if not followup and not hide_readonly_followup:
                        # Model returned nothing after tool results — retry once with a simpler
                        # prompt (thinking models like gemma4 sometimes need a plain nudge).
                        followup = self.send_single_turn_to_model(
                            f"Tool results:\n\n{tool_context}\n\n"
                            "Complete the task. Output FILE: blocks for any files to change, "
                            "or answer directly if no code changes are needed."
                        )

                    if followup:
                        followup_written, followup_response = self.process_response(
                            followup,
                            tool_depth + 1,
                            send_fn=send,
                            display_analysis_response=display_analysis_response
                            or hide_readonly_followup,
                            phase_name=phase_name,
                        )
                        # CRITICAL: include files written in Step 1a (before tool processing)
                        # so they appear in the return value even when returning via followup.
                        # Without this, the caller sees written=[] and fires the nudge even
                        # though docker-compose.yml, .gitignore etc. are already on disk.
                        combined = _pre_tool_written + [
                            f for f in followup_written if f not in set(_pre_tool_written)
                        ]
                        return combined, followup_response

        # ── Step 2: Write FILE: blocks (skip if already written in Step 1a) ──
        # Step 1a already handled FILE: extraction when both FILE: and tool
        # commands were present.  Only run again if Step 1a didn't fire.
        if "FILE:" in response:
            self.renderer.set_bottom_dock_status("Writing files to disk...")

        written = _pre_tool_written if _pre_tool_written else _extract_and_write_files(
            response, self.cwd, protected_files=self._protected, files_read=self.files_read
        )
        if written:
            if self.checkpoint_mgr and (
                len(written) >= 2 or any(not (self.cwd / fp).exists() for fp in written)
            ):
                self.checkpoint_mgr.create_checkpoint(
                    files_written=list(self.all_written),
                    message_count=len(self.engine._messages),
                    description=f"Before writing {len(written)} file(s)",
                    auto_stash=False,
                )
            self.last_written = written
            self.all_written.extend(written)
            self.renderer.print_files_written(written)

            files_summary = f"Wrote {len(written)} file(s): {', '.join(written)}"
            _add_to_conversation_memory(self.cwd, "assistant", files_summary, files_written=written)

            if self.security_auditor:
                security_findings = self.security_auditor.scan_files(written)
                if security_findings:
                    self.renderer.warning(self.security_auditor.format_findings(security_findings))

            if self.dep_graph:
                impact_summary = self.dep_graph.get_impact_summary(written)
                if impact_summary:
                    self.renderer.warning(impact_summary)
                for fp in written:
                    self.dep_graph.index_file(fp)

            if self.lsp_client:
                lsp_diags = self.lsp_client.check_files(written)
                if lsp_diags and self.lsp_client.has_errors(lsp_diags):
                    self.renderer.warning(self.lsp_client.format_diagnostics(lsp_diags))

        # ── Step 3: Execute bash blocks ────────────────────────
        bash_blocks = _extract_bash_blocks(response)
        for cmd in bash_blocks:
            cmd = _sanitize_shell_block(cmd)
            if not cmd:
                continue

            # Auto-run bash blocks in agent mode
            self.renderer.print_shell_start(cmd)
            try:
                with self.renderer.status_spinner(f"Running: {cmd[:60]}...", "executing"):
                    output = _run_shell(cmd, self.cwd, timeout=60)
                self.renderer.print_shell_output(output)
                self.engine.add_user(f"[Ran: {cmd}]")
                self.engine.add_assistant(f"Command output:\n```\n{output}\n```")
            except KeyboardInterrupt:
                self.renderer.console.print(
                    "\n  [dim yellow]─ Command cancelled (Ctrl+C)[/dim yellow]"
                )
                break
            except Exception as e:
                self.renderer.error(f"Command failed: {e}")

        return written, response

    def send_single_turn_to_model(
        self, user_msg: str, system_prompt: str | None = None
    ) -> str | None:
        """Send a single hidden turn without replaying the full chat history."""
        from sage.cli_core import _get_single_turn_agent_timeout, _run_callable_with_timeout
        from sage.providers.base import Message

        provider_name = self.model_id.split(":", 1)[0] if ":" in self.model_id else ""
        messages = [
            Message(role="system", content=system_prompt or self.engine.system_prompt),
            Message(role="user", content=user_msg),
        ]

        def _generate_once(target_model: str) -> str:
            from sage.cli_core import _get_single_turn_agent_timeout, _run_callable_with_timeout
            target_provider = target_model.split(":", 1)[0] if ":" in target_model else ""
            timeout_seconds = _get_single_turn_agent_timeout(target_provider)
            return _run_callable_with_timeout(
                lambda: self.router.generate(
                    messages,
                    target_model,
                    self.temp,
                    self.tokens,
                    lock_provider=self.model_locked,
                ),
                timeout_seconds=timeout_seconds,
                timeout_message=f"No response from model within {timeout_seconds:.0f} seconds",
            )

        try:
            return _generate_once(self.model_id)
        except Exception as exc:
            self.renderer.error(str(exc))
            return None

    def _auto_validate_and_retry(
        self,
        written: list[str],
        retries_left: int | None = None,
        attempt: int = 1,
    ) -> bool:
        """Auto-validate written files and retry on failure."""
        from sage.cli_core import _auto_validate, _is_broken_test_file
        if not written:
            return True

        validation = _auto_validate(written, self.cwd)
        if validation is None:
            return True

        cmd_name, output = validation
        self.renderer.print_validation_start(cmd_name)

        has_errors = _has_errors(output)
        self.renderer.print_test_results(output, passed=not has_errors)

        if not has_errors:
            return True

        current_written = written
        retry_num = max(attempt - 1, 0)
        progress_tracker = _RetryProgressTracker()

        while True:
            retry_num += 1
            progress_tracker.observe_failure(output)
            self.renderer.console.print()
            self.renderer.phase(
                "fixing",
                f"Auto-fixing validation failure (attempt {retry_num}, continuing until green)...",
            )

            if len(self.engine._messages) > 10:
                self.engine._messages[:] = self.engine._messages[:2] + self.engine._messages[-6:]

            smart_context = _build_smart_error_context(output, current_written, self.cwd)

            file_contents = []
            for fp in current_written[:3]:
                content = _read_file_context(fp, self.cwd, max_lines=80)
                if content:
                    file_contents.append(content)
            file_context = "\n\n".join(file_contents) if file_contents else ""

            fix_prompt = (
                f"VALIDATION FAILED (attempt {retry_num}).\n"
                f"Command: `{cmd_name}`\n"
                f"Error:\n```\n{_summarize_test_output(output, max_chars=3000)}\n```\n"
            )
            if file_context:
                fix_prompt += f"\nCurrent file contents:\n\n{file_context}\n\n"
            if smart_context:
                fix_prompt += smart_context + "\n\n"
            # Detect "module not found" errors — the fix is to CREATE the missing
            # module, not to patch the test.  Flag this so we can adjust the
            # prompt and use a larger token budget (creating a module is much
            # bigger than patching a test).
            _missing_module = bool(
                re.search(
                    r"ModuleNotFoundError|No module named|ImportError|Cannot find module",
                    output,
                    re.IGNORECASE,
                )
            )
            if _missing_module:
                fix_prompt += (
                    "RULES FOR THIS FIX:\n"
                    "1. The error is a MISSING MODULE — the implementation file does not exist yet.\n"
                    "2. Do NOT modify the test file. CREATE the missing implementation module(s) instead.\n"
                    "3. Write COMPLETE, working implementation files using FILE: blocks.\n"
                    "4. Include every class, function, and import the test expects — no stubs or TODOs.\n"
                    "5. If the test references many modules, write all of them in this response.\n"
                    "6. After writing the implementation, the existing test should pass as-is."
                )
            else:
                fix_prompt += (
                    "RULES FOR THIS FIX:\n"
                    "1. Read the ACTUAL error message above — do not guess.\n"
                    "2. Fix ONLY the specific error — do not rewrite unrelated code.\n"
                    "3. If a module doesn't exist, check AVAILABLE PROJECT MODULES above.\n"
                    "4. If a test imports a non-existent module, fix the implementation or import path; do NOT delete tests unless explicitly asked.\n"
                    "5. Output corrected FILE: blocks with COMPLETE file contents.\n"
                    "6. Try a DIFFERENT approach if your previous fix didn't work."
                )

            # Missing-module fixes may need to write entire implementation files —
            # use a much larger token budget.  All other fixes stay capped small to
            # reduce cloud latency.
            _fix_max_tokens = 8192 if _missing_module else 2048
            fix_response = self.send_to_model(fix_prompt, max_tokens=_fix_max_tokens)
            if not fix_response:
                break

            new_written, _ = self.process_response(fix_response)
            stall_reason = progress_tracker.observe_fix_attempt(
                response=fix_response,
                files_written=new_written,
            )
            if stall_reason:
                # Before giving up, try a hard "jolt" with a completely
                # different framing — the model may be stuck in a rut.
                # Only abandon if the jolt also fails to write anything.
                self.renderer.warning(
                    f"Fix loop stalled ({stall_reason}) — trying a fresh approach..."
                )
                jolt_prompt = (
                    f"The previous fix attempts for this error have not worked.\n"
                    f"Error still occurring:\n```\n{_summarize_test_output(output, max_chars=2000)}\n```\n\n"
                    "Take a completely different approach:\n"
                    "1. Ignore everything you wrote before.\n"
                    "2. Re-read the error from scratch — what is the REAL root cause?\n"
                    "3. Output FILE: blocks with a fundamentally different fix.\n"
                    "4. If the error is a missing module, CREATE that module with full implementations.\n"
                    "5. If tests reference non-existent code, write the missing code.\n"
                    "Do NOT repeat the same fix. Try something completely different."
                )
                jolt_max_tokens = 8192 if _missing_module else 4096
                jolt_response = self.send_to_model(jolt_prompt, max_tokens=jolt_max_tokens)
                if jolt_response:
                    jolt_written, _ = self.process_response(jolt_response)
                    if jolt_written:
                        new_written = jolt_written
                        # Reset the tracker so the jolt's files get a fair
                        # chance before the loop checks progress again.
                        progress_tracker = _RetryProgressTracker()
                        current_written = jolt_written
                        validation = _auto_validate(current_written, self.cwd)
                        if validation is None:
                            return True
                        cmd_name, output = validation
                        has_errors = _has_errors(output)
                        self.renderer.print_test_results(output, passed=not has_errors)
                        if not has_errors:
                            self.renderer.success("Fixed by jolt approach!")
                            return True
                        continue
                # Jolt also produced nothing — genuinely stuck, stop.
                self.renderer.warning("Jolt also produced no changes — stopping fix loop.")
                for fp in current_written:
                    target = self.cwd / fp
                    if target.exists() and _is_broken_test_file(fp, output):
                        self.renderer.info(f"  Flagged broken test file for review: {fp}")
                break

            if not new_written:
                continue

            current_written = new_written
            validation = _auto_validate(current_written, self.cwd)
            if validation is None:
                return True

            cmd_name, output = validation
            has_errors = _has_errors(output)
            self.renderer.print_test_results(output, passed=not has_errors)

            if not has_errors:
                self.renderer.success(f"Fixed on attempt {retry_num}!")
                return True

        return False

    def _ensure_implementation_writes(
        self,
        task_prompt: str,
        send: Callable[[str], str | None],
        effective_prompt: str,
        *,
        max_rounds: int | None = None,
    ) -> list[str]:
        """Re-prompt until the model emits FILE: blocks or we exhaust follow-up rounds."""
        from sage.cli_core import _build_implementation_completion_nudge, _default_test_command, _get_current_classification, _resolve_implementation_test_command, _suggest_target_paths_for_task
        cls = _get_current_classification()
        if not cls or cls.read_only or getattr(cls, "is_informational", False):
            return []

        if max_rounds is None:
            max_rounds = 3 if self.is_local else 12

        base_test = (self.full_project_test_cmd or "").strip() or _default_test_command(self.cwd)
        test_cmd = _resolve_implementation_test_command(self.cwd, task_prompt, base_test)
        path_hints = _suggest_target_paths_for_task(self.cwd, task_prompt)
        merged_written: list[str] = []
        for attempt in range(1, max_rounds + 1):
            nudge = _build_implementation_completion_nudge(
                task_prompt, test_cmd, attempt, max_rounds, path_hints=path_hints
            )
            if effective_prompt and attempt == 1:
                nudge = f"{nudge}\n(Original request context is also in the conversation above.)\n"
            self.renderer.phase(
                "fixing",
                f"No `FILE:` output yet — enforcing code + test run (follow-up {attempt}/{max_rounds})...",
            )
            follow = send(nudge)
            if not follow:
                break
            round_written, _ = self.process_response(
                follow, send_fn=send, phase_name="implementation"
            )
            for fp in round_written:
                if fp not in merged_written:
                    merged_written.append(fp)
            if merged_written:
                break
        # Last resort: one turn with a minimal system prompt (local models often need this; cloud too when nudges fail).
        if not merged_written:
            self.renderer.phase("fixing", "Last attempt: strict single-turn FILE: mode...")
            strict_system = (
                "You are a file patch tool. You MUST output one or more SAGE FILE: blocks. "
                "Each block is: line 'FILE: relative/path' then a markdown code fence with the COMPLETE file. "
                "Then a line 'RUN: ' with a test command. No XML. No <execute_bash>. No apology. No preamble — start with FILE:"
            )
            last_user = _build_implementation_completion_nudge(
                task_prompt, test_cmd, max_rounds, max_rounds, path_hints=path_hints
            )
            last = self.send_to_model(
                last_user,
                system_prompt=strict_system,
                save_history=True,
            )
            if last:
                w2, _ = self.process_response(
                    last, send_fn=send, phase_name="implementation"
                )
                for fp in w2:
                    if fp not in merged_written:
                        merged_written.append(fp)
        if not merged_written and max_rounds > 0:
            self.renderer.debug_warning(
                "SAGE could not get `FILE:` blocks from the model after multiple nudges. "
                "Try a cloud model (e.g. in /model) or a larger local model; small local models often omit FILE: output."
            )
        return merged_written

    def _execute_phase(
        self,
        phase_name: str,
        prompt: str,
        send: Callable[[str], str | None],
        classification: _ClassifiedRequest | None,
        task_prompt: str,
        seeded_recursive_analysis_context: str = "",
        seeded_shell_inventory_context: str = "",
        seeded_full_file_coverage_context: str = "",
    ) -> tuple[list[str], str]:
        """Execute a single phase of the multistep pipeline."""
        from sage.cli_core import _build_context_aware_validation_retry_prompt, _build_readonly_exploration_nudge, _build_seeded_readonly_synthesis_prompt, _collect_analysis_validation_violations, _extract_tool_commands_structured
        phase_messages = {
            "planning": "Breaking task into steps...",
            "analysis": "Investigating with the model...",
            "synthesis": "Synthesizing final analysis...",
            "testing": "Writing tests first (TDD)...",
            "implementation": "Writing implementation...",
        }

        phase_prompt = prompt
        phase_sender = send

        if classification and classification.read_only:
            if phase_name == "planning" and (
                seeded_recursive_analysis_context
                or seeded_shell_inventory_context
                or seeded_full_file_coverage_context
            ):
                phase_prompt = (
                    "SAGE already auto-collected grounded repo evidence for this read-only analysis. "
                    "Use that evidence first; only issue more READ:/SEARCH:/RUN: commands if a key gap remains.\n\n"
                    f"{prompt}"
                )
            elif phase_name == "analysis":
                seeded_parts: list[str] = []
                if seeded_recursive_analysis_context:
                    seeded_parts.append(
                        "## AUTO-COLLECTED RECURSIVE CODEBASE CONTEXT\n"
                        f"{seeded_recursive_analysis_context}"
                    )
                if seeded_shell_inventory_context:
                    seeded_parts.append(
                        "## AUTO-COLLECTED SHELL INVENTORY\n" f"{seeded_shell_inventory_context}"
                    )
                if seeded_parts:
                    phase_prompt = "\n\n".join(seeded_parts + [prompt])
            elif phase_name == "synthesis":
                phase_prompt = _build_seeded_readonly_synthesis_prompt(
                    prompt,
                    seeded_recursive_analysis_context=seeded_recursive_analysis_context,
                    seeded_shell_inventory_context=seeded_shell_inventory_context,
                    seeded_full_file_coverage_context=seeded_full_file_coverage_context,
                    verified_files=self.files_read,
                    is_local=self.is_local,
                )
            if phase_name == "synthesis" and send is self.send_to_model:
                # Use send_to_model for synthesis to ensure output is visible (streaming)
                # We still want to save history for the final synthesis of an investigation
                phase_sender = self.send_to_model

        if classification and getattr(classification, "is_informational", False):
            # For informational tasks, use a clean system prompt to prevent codebase bias (P3-71)
            info_sys_prompt = (
                "You are SAGE, a helpful and knowledgeable assistant. "
                "Provide a detailed and accurate response based on your internal knowledge. "
                "Do NOT use codebase tools (READ:, SEARCH:, RUN:, FILE:) unless the user specifically "
                "asks for information about the local project files."
            )
            # Use streaming sender with system prompt override to ensure output is visible (P3-71)
            # Only save history for the final synthesis phase to avoid polluting with internal research
            save_history = phase_name == "synthesis"
            phase_response = self.send_to_model(
                phase_prompt, system_prompt=info_sys_prompt, save_history=save_history
            )
        elif classification and classification.read_only and phase_name == "synthesis":
            # For investigation synthesis, use streaming sender directly to ensure output is visible
            # Skip the 'thinking' phase indicator to avoid UI flickering/blocking (P3-71)
            phase_response = self.send_to_model(phase_prompt, save_history=True)
        else:
            self.renderer.phase(
                "planning" if phase_name == "planning" else "thinking",
                phase_messages.get(phase_name, "Working..."),
            )
            phase_response = phase_sender(phase_prompt)
        if not phase_response:
            if phase_name == "synthesis":
                # Fallback for synthesis failure
                phase_response = "The model was unable to synthesize a final response. Please check your request or try a different model."
            else:
                return [], ""

        if classification and classification.read_only and phase_name in {"planning", "analysis"}:
            for retry_num in range(1, 3):
                if self.files_read or _extract_tool_commands_structured(phase_response):
                    break

                # Context-explosion guard: if the engine is already near the
                # token limit, retrying with more nudge text WILL push us
                # over. Don't compound the problem — abort the retry loop,
                # compact aggressively, and let the next user turn continue.
                # The user's log showed 22,643 tokens vs a 16,384 window
                # because retries kept stacking nudges on top of huge prompts.
                stats = self.engine.get_context_stats()
                if stats.estimated_tokens > stats.max_tokens * 0.75:
                    self.renderer.warning(
                        f"Context at {stats.estimated_tokens:,}/{stats.max_tokens:,} tokens "
                        f"({stats.usage_percent:.0f}%) — compacting to continue"
                    )
                    self.engine.compact()
                    self.engine.maybe_compress_for_model(self.model_id, budget_chars=12000)
                    # Only hard-stop when truly out of space (>92%) — otherwise
                    # compact and keep working so the task finishes.
                    if stats.estimated_tokens > stats.max_tokens * 0.92:
                        self.renderer.info(
                            "Context window nearly full — stopping retries. "
                            "Run `sage compact` then continue."
                        )
                        break

                nudge = _build_readonly_exploration_nudge(
                    phase_name,
                    classification,
                    has_verified_files=bool(self.files_read),
                )
                self.renderer.phase(
                    "fixing",
                    f"Analysis too broad (attempt {retry_num}/2) — nudging model to explore codebase...",
                )
                retry_response = phase_sender(nudge)
                if not retry_response:
                    break
                phase_response = retry_response

        # Process phase response
        phase_written, phase_response = self.process_response(
            phase_response, send_fn=phase_sender, phase_name=phase_name
        )

        if classification and classification.read_only and phase_name == "synthesis":
            validation_violations, investigation_only = _collect_analysis_validation_violations(
                phase_response,
                task_prompt,
                classification,
                list(self.files_read),
            )
            if validation_violations and not investigation_only:
                # Same context-explosion guard as the planning/analysis loop.
                # If we're near the limit, skip the retry instead of stacking
                # a 5K-char validation-retry prompt on top.
                stats = self.engine.get_context_stats()
                if stats.estimated_tokens > stats.max_tokens * 0.75:
                    self.renderer.warning(
                        f"Context at {stats.usage_percent:.0f}% — skipping synthesis retry to avoid context overflow"
                    )
                else:
                    self.renderer.phase(
                        "fixing",
                        "Synthesis validation failed (attempt 1/2) — requesting corrected final analysis...",
                    )
                    retry_prompt = _build_context_aware_validation_retry_prompt(
                        task_prompt=task_prompt,
                        cwd=self.cwd,
                        violations=validation_violations,
                        current_files_read=list(self.files_read),
                        is_analysis=True,
                    )
                    retry_response = phase_sender(retry_prompt)
                    if retry_response:
                        phase_written_retry, phase_response_retry = self.process_response(
                            retry_response, send_fn=phase_sender
                        )
                        phase_written.extend(phase_written_retry)
                        phase_response = phase_response_retry

        return phase_written, phase_response

    def _execute_multistep(
        self,
        task_prompt: str,
        send: Callable[[str], str | None],
        classification=None,
        seeded_recursive_analysis_context: str = "",
        seeded_shell_inventory_context: str = "",
        seeded_full_file_coverage_context: str = "",
    ) -> tuple[list[str], str]:
        """Execute a task via focused multi-step pipeline with real-time plan sync."""
        from sage.cli_core import _build_followup_context_from_recent_analysis, _build_multistep_phase_prompts, _clean_manifest_line, _is_analysis_followup_implementation_request, _persist_recent_analysis_output, _should_use_seeded_synthesis_only
        all_step_written: list[str] = []
        accumulated_responses: list[str] = []
        last_response = ""

        phases = _build_multistep_phase_prompts(task_prompt, classification, self.cwd)
        self._is_greenfield_task = any(phase_name == "implementation" for phase_name, _ in phases)
        if _should_use_seeded_synthesis_only(
            task_prompt,
            classification,
            seeded_full_file_coverage_context,
        ):
            phases = [phase for phase in phases if phase[0] == "synthesis"]

        for phase_name, prompt in phases:
            # Inject accumulated findings into subsequent phases for context awareness
            findings_to_inject = []

            # Cross-turn persistence: only inject if this looks like a follow-up implementation
            is_followup = _is_analysis_followup_implementation_request(task_prompt)
            if is_followup:
                if self.context and self.context.accumulated_findings:
                    findings_to_inject.extend(self.context.accumulated_findings)
                else:
                    # Fallback to legacy session state if context is empty
                    legacy_findings = _build_followup_context_from_recent_analysis(
                        self.cwd, task_prompt
                    )
                    if legacy_findings:
                        findings_to_inject.append(legacy_findings)

            # Intra-task persistence: always inject responses from earlier phases of the SAME task
            if accumulated_responses:
                findings_to_inject.extend(accumulated_responses)

            # Consume any hints provided by the user while the agent was running
            if hasattr(self, "hint_queue"):
                while not self.hint_queue.empty():
                    hint = self.hint_queue.get()
                    findings_to_inject.append(f"USER REAL-TIME HINT/INTERRUPTION:\n{hint}")
                    self.renderer.info(f"💡 Absorbed real-time hint into current phase: {hint[:60]}...")

            if findings_to_inject:
                findings = "\n\n".join(findings_to_inject)
                context_block = (
                    "## SESSION CONTEXT: PREVIOUS FINDINGS\n"
                    "The following information was gathered or generated during previous phases/turns. "
                    "Use this as grounded context to ensure accuracy and continuity.\n\n"
                    f"{findings}\n\n"
                    "--- END OF PREVIOUS FINDINGS ---\n\n"
                )
                prompt = f"{context_block}{prompt}"

            # 1. Update plan status to in_progress
            self._sync_plan_task_status(phase_name, "in_progress", classification)

            # 2. Execute the phase
            phase_written, phase_response = self._execute_phase(
                phase_name,
                prompt,
                send,
                classification,
                task_prompt,
                seeded_recursive_analysis_context=seeded_recursive_analysis_context,
                seeded_shell_inventory_context=seeded_shell_inventory_context,
                seeded_full_file_coverage_context=seeded_full_file_coverage_context,
            )
            if (not phase_response or phase_response.strip().startswith(("Error:", "❌ Error:"))) and phase_name != "synthesis":
                # Critical phase failure
                self._sync_plan_task_status(phase_name, "failed", classification)
                return all_step_written, phase_response or ""

            all_step_written.extend(phase_written)
            if phase_response:
                accumulated_responses.append(phase_response)
                # Persist to context if available
                if self.context:
                    self.context.accumulated_findings.append(phase_response)
                    if self.context_manager:
                        self.context_manager.save_context(self.context)

                # Also persist to legacy session state for cross-turn context recall (create_plan)
                if classification and classification.read_only:
                    _persist_recent_analysis_output(self.cwd, phase_response, task_prompt)
                last_response = phase_response

                # Update current_plan when the model announces its own step breakdown
                self._apply_model_step_breakdown(phase_response, classification)

            # 3. Update plan status to completed
            self._sync_plan_task_status(phase_name, "completed", classification)

            # ── Save FILE_MANIFEST immediately after planning phase ──────────
            # The manifest must be saved here — before any engine trimming —
            # so execute_task_prompt's continuation loop can use it even after
            # engine._messages has been condensed between batches.
            if phase_name == "planning" and phase_response and not self._greenfield_manifest:
                mstart = phase_response.find("FILE_MANIFEST:")
                if mstart != -1:
                    for ml in phase_response[mstart + 14:].strip().splitlines():
                        ml = _clean_manifest_line(ml)
                        if ml and "." in ml and not ml.startswith("#"):
                            self._greenfield_manifest.append(ml)

        # ── Greenfield batch-continuation loop ──────────────────────────────
        # A single model response can output ~40-60 files at 65K tokens.
        # Large projects (300+ files) need multiple passes.  Keep asking
        # "write the next batch" until the model signals completion or stops
        # producing new files.  This runs only for greenfield requests.
        _gf_signals = [
            "full platform", "full project", "full app", "full stack",
            "from scratch", "brand new", "new platform", "new project",
            "new application", "build a ", "create a ", "entire platform",
            "entire project", "entire application", "end-to-end",
            "monorepo", "all features", "complete platform",
        ]
        _task_lower_gf = task_prompt.lower()
        _is_greenfield_task = (
            sum(1 for s in _gf_signals if s in _task_lower_gf) >= 1
            or len(task_prompt) > 600
        )

        # Greenfield continuation was moved to execute_task_prompt (after the
        # nudge writes the first batch).  No inner loop needed here anymore.
        if False and _is_greenfield_task:
            _manifest_files: list[str] = []
            _MAX_CONTINUATION_ROUNDS = 0
            for _cont_round in range(1, _MAX_CONTINUATION_ROUNDS + 1):
                # Trim engine history so context doesn't overflow between rounds.
                if len(self.engine._messages) > 6:
                    self.engine._messages[:] = (
                        self.engine._messages[:1]
                        + self.engine._messages[-4:]
                    )

                _written_set = set(all_step_written)
                _files_written_str = "\n".join(
                    f"  {fp}" for fp in all_step_written[:60]
                )
                _overflow = (
                    f"\n  ... and {len(all_step_written) - 60} more"
                    if len(all_step_written) > 60
                    else ""
                )

                # Show the model which manifest files are still missing
                _missing = [f for f in _manifest_files if f not in _written_set]
                if _manifest_files and not _missing:
                    self.renderer.success(
                        f"All {len(_manifest_files)} manifest files written — scaffold complete."
                    )
                    break

                _missing_block = ""
                if _missing:
                    _show = _missing[:40]
                    _missing_block = (
                        f"\nFiles from your FILE_MANIFEST that still need to be written "
                        f"({len(_missing)} remaining):\n"
                        + "\n".join(f"  {f}" for f in _show)
                        + (f"\n  ... and {len(_missing) - 40} more" if len(_missing) > 40 else "")
                        + "\n"
                    )

                _cont_prompt = (
                    f"## SCAFFOLD CONTINUATION — round {_cont_round}\n\n"
                    f"Original task: {task_prompt[:400]}\n\n"
                    f"Files written so far ({len(all_step_written)} total):\n"
                    f"{_files_written_str}{_overflow}\n"
                    f"{_missing_block}\n"
                    "Continue writing the NEXT batch of files using FILE: blocks.\n\n"
                    "CRITICAL RULES:\n"
                    "- Use the EXACT tech stack from the original task above (e.g. React Native "
                    "  not plain React, FastAPI not Flask, etc.)\n"
                    "- Write COMPLETE file contents — no stubs, no TODOs, no '# implement later'\n"
                    "- Do NOT rewrite files already listed in 'written so far'\n"
                    "- Focus on the files listed as still missing above\n"
                    "- Only output SCAFFOLD_COMPLETE when ALL missing files above are written\n"
                    "Write the next batch now."
                )

                self.renderer.phase(
                    "implementation",
                    f"Scaffolding batch {_cont_round} — {len(all_step_written)} files so far...",
                )
                _cont_response = send(_cont_prompt)
                if not _cont_response:
                    break

                if "SCAFFOLD_COMPLETE" in _cont_response or "scaffold_complete" in _cont_response.lower():
                    # Verify the model isn't declaring done too early
                    _cont_written_check, _ = self.process_response(
                        _cont_response, send_fn=send, phase_name="implementation"
                    )
                    for fp in _cont_written_check:
                        if fp not in all_step_written:
                            all_step_written.append(fp)
                    _still_missing = [f for f in _manifest_files if f not in set(all_step_written)]
                    if not _still_missing or not _manifest_files:
                        self.renderer.success(
                            f"Scaffold complete — {len(all_step_written)} files written."
                        )
                        last_response = _cont_response
                        break
                    # Still files missing — ignore SCAFFOLD_COMPLETE and continue
                    self.renderer.warning(
                        f"Model declared SCAFFOLD_COMPLETE but {len(_still_missing)} files "
                        "still missing from manifest — continuing..."
                    )
                    continue

                _cont_written, _ = self.process_response(
                    _cont_response, send_fn=send, phase_name="implementation"
                )
                _new_files = [f for f in _cont_written if f not in all_step_written]
                if not _new_files:
                    if not _manifest_files:
                        # No manifest to check against — stop
                        self.renderer.success(
                            f"Scaffold complete — {len(all_step_written)} files written."
                        )
                        break
                    # Keep going — model may need a different prompt angle
                    self.renderer.warning(
                        f"Batch {_cont_round} produced no new files — retrying with missing list..."
                    )
                    if _cont_round >= 3 and not _new_files:
                        break  # Genuinely stuck after 3 empty rounds
                    continue

                all_step_written.extend(_new_files)
                last_response = _cont_response
                self.renderer.info(
                    f"  Batch {_cont_round}: +{len(_new_files)} files "
                    f"({len(all_step_written)} total)"
                )

        return all_step_written, last_response

    def _apply_model_step_breakdown(
        self, response: str, classification: _ClassifiedRequest | None
    ) -> None:
        """Parse a model response for a numbered step list and update current_plan + dock.

        When the model writes "I'll do this in N steps: 1. ... 2. ..." at any point
        (planning or mid-execution), we replace the plan tasks so the dock reflects
        exactly what the model has committed to doing.
        """
        from sage.cli_core import _build_cli_task_todos, _extract_steps_from_response
        steps = _extract_steps_from_response(response)
        if not steps:
            return

        plan_id = self.current_plan.id if self.current_plan else "model-plan"
        goal = self.current_plan.goal if self.current_plan else ""

        # Mark step 1 in_progress since the model is starting to act on its own breakdown
        new_tasks = [
            PlanTask(
                id=f"step-{i}",
                description=desc,
                priority=TaskPriority.MEDIUM,
                status="in_progress" if i == 1 else "pending",
            )
            for i, desc in enumerate(steps, start=1)
        ]

        if self.current_plan:
            self.current_plan.tasks = new_tasks
        else:
            self.current_plan = ExecutionPlan(id=plan_id, goal=goal, tasks=new_tasks)

        read_only = classification.read_only if classification else False
        updated_todos = _build_cli_task_todos(read_only, plan=self.current_plan)
        self.renderer.set_bottom_dock_todos(updated_todos)

    def _sync_plan_task_status(
        self, phase_name: str, status: str, classification: _ClassifiedRequest | None
    ) -> None:
        """Synchronize the internal execution plan with the UI dock."""
        from sage.cli_core import _build_cli_task_todos, _set_cli_task_stage
        if not (self.current_plan and self.current_plan.tasks):
            # If no dynamic plan, update the generic dock items based on phase
            task_todos = _build_cli_task_todos(
                classification.read_only if classification else True,
                plan=None,
                is_informational=(
                    getattr(classification, "is_informational", False) if classification else False
                ),
            )

            # Map phase_name to generic keys
            phase_to_key = {
                "analysis": "analyze",
                "planning": "analyze",  # Map planning to analyze for read-only dock consistency
                "implementation": "execute",
                "testing": "execute",
                "synthesis": (
                    "respond" if (classification and classification.read_only) else "execute"
                ),
            }
            target_key = phase_to_key.get(phase_name)
            if target_key:
                _set_cli_task_stage(task_todos, target_key)
                if status == "completed" and target_key == "execute":
                    # For implementation, mark as completed
                    for t in task_todos:
                        if t["key"] == target_key:
                            t["status"] = "completed"

                self.renderer.set_bottom_dock_todos(task_todos)
                if status == "in_progress":
                    self.renderer.set_bottom_dock_status(f"{phase_name.capitalize()}...")
            return

        # 1. Update all matching tasks for this phase
        any_updated = False
        last_matched_desc = ""

        for task in self.current_plan.tasks:
            desc = task.description.lower()
            is_match = False

            # Expanded keyword matching for higher accuracy
            if phase_name == "planning" and any(
                k in desc for k in ["plan", "break", "step", "decompose", "strategy"]
            ):
                is_match = True
            elif phase_name == "analysis" and any(
                k in desc
                for k in [
                    "analyze",
                    "investigate",
                    "review",
                    "root cause",
                    "understand",
                    "inspect",
                    "read",
                    "explore",
                ]
            ):
                is_match = True
            elif phase_name == "synthesis" and any(
                k in desc
                for k in ["synthesize", "finding", "report", "summarize", "conclusion", "result"]
            ):
                is_match = True
            elif phase_name == "testing" and any(
                k in desc
                for k in ["test", "tdd", "unit", "verify", "validation", "coverage", "check"]
            ):
                is_match = True
            elif phase_name == "implementation" and any(
                k in desc
                for k in ["implement", "fix", "add", "modify", "create", "write", "update", "patch"]
            ):
                is_match = True

            if is_match:
                if status == "in_progress" and task.status == "pending":
                    task.status = "in_progress"
                    any_updated = True
                    last_matched_desc = task.description
                    # For in_progress, we mark the FIRST matching pending task to show sequential progress
                    break
                elif status == "completed" and task.status == "in_progress":
                    task.status = "completed"
                    any_updated = True
                    last_matched_desc = task.description
                    # For completion, we mark ALL that were in progress (no break)

        # 2. Fallback: If no heuristic match found, use sequential logic
        if not any_updated:
            for task in self.current_plan.tasks:
                if status == "in_progress" and task.status == "pending":
                    task.status = "in_progress"
                    last_matched_desc = task.description
                    any_updated = True
                    break
                if status == "completed" and task.status == "in_progress":
                    task.status = "completed"
                    last_matched_desc = task.description
                    any_updated = True
                    # Keep going to mark all in_progress as completed if needed

        if any_updated:
            # 3. Ensure all tasks PRIOR to the last updated task are marked as completed
            # This prevents the dock from looking stuck on earlier pending tasks
            reached_last = False
            for t in self.current_plan.tasks:
                if t.description == last_matched_desc:
                    reached_last = True
                    if status == "completed":
                        t.status = "completed"
                    continue

                if not reached_last and t.status == "pending":
                    t.status = "completed"

            # 4. Re-sync task_todos and update renderer
            _task_todos = _build_cli_task_todos(
                classification.read_only if classification else True,
                plan=self.current_plan,
                is_informational=(
                    getattr(classification, "is_informational", False) if classification else False
                ),
            )
            self.renderer.set_bottom_dock_todos(_task_todos)

            # 5. Update status message to match the current task
            if status == "in_progress" and last_matched_desc:
                self.renderer.set_bottom_dock_status(f"{last_matched_desc}...")
            elif status == "completed":
                self.renderer.set_bottom_dock_status("Step finalized.")

    def execute_task_prompt(
        self,
        task_prompt: str,
        save_history: bool = True,
        sender: Callable[[str], str | None] | None = None,
        enhanced_mode: bool = True,
    ) -> tuple[list[str], bool]:
        """Run one full agent task cycle and return (written_files, task_ok)."""
        import os
        if os.environ.get("SAGE_TESTING") == "1":
            try:
                from backend.runtimes.cloud_runtime import _is_prompt_invalid
                if _is_prompt_invalid(task_prompt):
                    self.renderer.error("Error: Invalid argument values provided in prompt.")
                    return [], False
            except Exception:
                pass

        from sage.cli_core import _add_to_prompt_history, _build_cli_task_todos, _build_followup_context_from_recent_analysis, _check_context_relevance, _classify_and_store_request, _clean_manifest_line, _initialize_request_grounding_state, _route_to_principal_pipeline, _set_cli_task_stage
        global _current_execution_context
        self._model_timed_out = False  # reset per-task
        self._greenfield_manifest = []  # reset per-task so old manifests don't bleed through
        self._is_greenfield_task = False
        from sage.core.tools import ExecutionLedger
        self.execution_ledger = ExecutionLedger()
        send = sender or self.send_to_model

        # 1. Classify request
        self._current_classification = _classify_and_store_request(task_prompt)
        classification = self._current_classification
        is_info = getattr(classification, "is_informational", False)
        is_investigation = classification and classification.read_only

        # 1.1 Context Isolation: Check if this request is related to the previous one (P3-71)
        if self.last_prompt and not _check_context_relevance(task_prompt, self.last_prompt):
            self.renderer.info("   Unrelated task detected — clearing context history.")
            self.engine.clear()
            if self.context:
                self.context.accumulated_findings = []

        self.last_prompt = task_prompt

        # Check if this is a build request and route to principal pipeline
        from sage.core.principal_engineer import looks_like_build_request
        if looks_like_build_request(task_prompt):
            self.renderer.info("🚀 Routing build request to the principal pipeline...")
            if save_history:
                _add_to_prompt_history(self.cwd, task_prompt)
            report = _route_to_principal_pipeline(
                user_input=task_prompt,
                base_out_dir=self.cwd,
                router=self.router,
                model_id=self.model_id,
                temp=self.temp,
                tokens=self.tokens,
                model_locked=self.model_locked,
                system_prompt=self.engine.system_prompt if self.engine else None,
            )
            if report:
                from pathlib import Path
                written = []
                out_path = Path(report.get("out_dir", self.cwd))
                if out_path.exists():
                    for p in out_path.rglob("*"):
                        if p.is_file():
                            parts = p.relative_to(out_path).parts
                            if not any(
                                x in parts for x in (".sage", ".git", "node_modules", "__pycache__", ".pytest_cache", "venv", ".venv")
                            ):
                                written.append(str(p.relative_to(out_path)))
                install_ok = report.get("install_ok", True)
                build_ok = report.get("build_ok", True)
                runs_ok = report.get("runs_ok", True)
                tests_ok = report.get("tests_ok", True)
                task_ok = (
                    (install_ok is not False)
                    and (build_ok is not False)
                    and (runs_ok is not False)
                    and (tests_ok is not False)
                )
                return written, task_ok

        # 1.5 Activate bottom dock EARLY (before planning) to show progress
        task_todos = _build_cli_task_todos(
            classification.read_only,
            plan=None,
            is_informational=getattr(classification, "is_informational", False),
        )

        # UI status message tailored to task type
        if classification.is_informational:
            status_msg = "Gathering information..."
        elif classification.read_only:
            status_msg = "Synthesizing execution strategy..."
        else:
            status_msg = "Synthesizing execution strategy..."

        # 1.5 Activate bottom dock EARLY (before planning) to show progress.
        # Skip if running in the async REPL as it manages its own bottom layout.
        if not getattr(self, "_is_repl", False):
            dock_active = self.renderer.activate_bottom_dock(
                todos=task_todos,
                status_message=status_msg,
                prompt_message="Planning...",
            )
        else:
            dock_active = False
            self.renderer.set_bottom_dock_todos(task_todos)
            self.renderer.set_bottom_dock_status(status_msg)

        current_plan_context = ""
        if enhanced_mode:
            try:
                phase_msg = (
                    "Gathering information..." if is_info else "Synthesizing execution strategy..."
                )
                self.renderer.phase("planning", phase_msg)

                from sage.core.procedural_workflow import IntelligentExecutionEngine

                # Check if we have recent analysis findings for follow-up implementation
                followup_findings = _build_followup_context_from_recent_analysis(
                    self.cwd, task_prompt
                )

                engine_internal = IntelligentExecutionEngine(self.cwd, self.renderer)

                # Use a clean system prompt for informational decomposition to prevent codebase bias
                def _info_decomposition_sender(msg: str) -> str | None:
                    info_sys_prompt = "You are a helpful assistant. Decompose this general knowledge request into 2-3 research steps."
                    return self.send_single_turn_to_model(msg, system_prompt=info_sys_prompt)

                # Wrap send_fn so any numbered step list in the planning response
                # updates the dock immediately — before create_plan even returns
                def _plan_intercepting_send(msg: str) -> str | None:
                    response = self.send_single_turn_to_model(msg)
                    if response:
                        self._apply_model_step_breakdown(response, classification)
                    return response

                self.current_plan = engine_internal.create_plan(
                    task_prompt,
                    send_fn=(
                        _info_decomposition_sender if is_info else _plan_intercepting_send
                    ),
                    previous_findings=followup_findings if followup_findings else None,
                    classification=classification,
                )
                plan = self.current_plan

                # Update dock with real plan tasks immediately after generation
                if plan and plan.tasks:
                    task_todos = _build_cli_task_todos(
                        classification.read_only,
                        plan=plan,
                        is_informational=getattr(classification, "is_informational", False),
                    )
                    self.renderer.set_bottom_dock_todos(task_todos)

                    lines = []
                    for idx, task in enumerate(plan.tasks, start=1):
                        deps = ", ".join(str(d) for d in task.dependencies) if task.dependencies else ""
                        dep_suffix = f" (deps: {deps})" if deps else ""
                        lines.append(
                            f"{idx}. [{task.priority.name}] {task.description}{dep_suffix}"
                        )
                    current_plan_context = (
                        "\n\n## CURRENT PLAN\n"
                        f"Plan ID: {plan.id}\n"
                        f"Goal: {plan.goal}\n"
                        "Tasks:\n" + "\n".join(lines)
                    )
                    # We show the request type AFTER plan is built, to confirm we've decided what to do
                    if classification.read_only:
                        self.renderer.phase(
                            "analysis",
                            f"📊 Request type: {classification.request_type.name} (read-only analysis)",
                        )
                    else:
                        self.renderer.phase(
                            "planning",
                            f"🔧 Request type: {classification.request_type.name} (implementation allowed)",
                        )
                    self.renderer.info(f"   Decided plan: {len(plan.tasks)} tasks")
            except Exception as e:
                self.renderer.warning(f"Plan generation skipped: {e}")

        def _advance_task_stage(stage_key: str, status_message: str) -> None:
            from sage.cli_core import _set_cli_task_stage
            if not dock_active:
                return
            _set_cli_task_stage(task_todos, stage_key)
            self.renderer.set_bottom_dock_todos(task_todos)
            self.renderer.set_bottom_dock_status(status_message)

        def _close_task_dock() -> None:
            if not dock_active:
                return
            self.renderer.clear_bottom_dock_todos()
            self.renderer.deactivate_bottom_dock()

        # Grounding state initialization
        self.files_read, self.execution_ledger = _initialize_request_grounding_state(
            self.cwd,
            pinned_context_files=self.sticky_context_files,
        )

        if save_history:
            _add_to_prompt_history(self.cwd, task_prompt)

        # Map generic stage to informational tasks if needed
        stage_key = "verify" if classification.read_only else "implement"
        if is_info:
            stage_key = "task_1"  # Start with first research step from create_plan

        _advance_task_stage(
            stage_key,
            (
                "Researching topic..."
                if is_info
                else (
                    "Cross-checking findings..."
                    if classification.read_only
                    else "Editing code and tests..."
                )
            ),
        )

        # Build prompt with plan context
        effective_prompt = task_prompt
        if current_plan_context:
            effective_prompt = f"{task_prompt}\n\n{current_plan_context}"

        # Send to model or run multistep
        if enhanced_mode:
            written, response = self._execute_multistep(
                effective_prompt, send, classification=classification
            )
        else:
            response = send(effective_prompt)
            if not response:
                _close_task_dock()
                return [], False
            written, _ = self.process_response(response, send_fn=send, phase_name="implementation")
        
        if response and response.strip().startswith(("Error:", "❌ Error:")):
            self.renderer.error(response.strip())
            _close_task_dock()
            return [], False


        # Re-prompt when the task is not read-only but the model only explored (no FILE: saves).
        if (
            not classification.read_only
            and not is_info
            and not written
        ):
            nudge_written = self._ensure_implementation_writes(
                task_prompt, send, effective_prompt
            )
            written = nudge_written

        # ── Greenfield batch-continuation (runs here, AFTER the first file batch) ──
        # The continuation loop was previously inside _execute_multistep but fired
        # before the nudge wrote any files.  Running it here gives it the actual
        # first batch (from either the phases or the nudge) as context.
        _gf_kws_exec = [
            "full platform", "full project", "full app", "full stack",
            "from scratch", "brand new", "new platform", "new project",
            "new application", "build a ", "create a ", "entire platform",
            "entire project", "entire application", "end-to-end",
            "monorepo", "all features", "complete platform",
        ]
        _task_lower_exec = task_prompt.lower()
        # Use the manifest saved by _execute_multistep (before engine trimming).
        # Fallback: search engine messages if the agent attr is somehow empty.
        _manifest_exec: list[str] = list(self._greenfield_manifest)
        if not _manifest_exec:
            for _msg in self.engine._messages:
                _body = _msg.get("content", "") if isinstance(_msg, dict) else str(_msg)
                _mstart = _body.find("FILE_MANIFEST:")
                if _mstart != -1:
                    for _ml in _body[_mstart + 14:].strip().splitlines():
                        _ml = _clean_manifest_line(_ml)
                        if _ml and "." in _ml and not _ml.startswith("#"):
                            _manifest_exec.append(_ml)
                    if _manifest_exec:
                        break

        _is_gf_exec = (
            sum(1 for s in _gf_kws_exec if s in _task_lower_exec) >= 1
            or len(task_prompt) > 600
            or getattr(self, "_is_greenfield_task", False)
            or bool(_manifest_exec)
        )

        if _is_gf_exec and written and not classification.read_only and not is_info:
            all_written = list(written)
            for _mf in _manifest_exec:
                if _mf not in all_written:
                    try:
                        if (self.cwd / _mf).is_file():
                            all_written.append(_mf)
                    except Exception:
                        pass

            _MAX_EXEC_BATCHES = int(os.environ.get("SAGE_BATCH_LIMIT", "250"))
            _empty_rounds = 0  # consecutive batches with no new files
            _model_declared_done_prematurely = False
            for _batch_num in range(1, _MAX_EXEC_BATCHES + 1):
                # Trim context between batches to prevent token overflow while preserving API memory
                if len(self.engine._messages) > 24:
                    self.engine._messages[:] = (
                        self.engine._messages[:1] + self.engine._messages[-16:]
                    )

                _written_set = set(all_written)
                _missing = [f for f in _manifest_exec if f not in _written_set]

                if _manifest_exec and not _missing:
                    self.renderer.success(
                        f"All {len(_manifest_exec)} manifest files complete — "
                        f"{len(all_written)} total files written."
                    )
                    break

                _show_written = all_written[:50]
                _written_lines = "\n".join(f"  {f}" for f in _show_written)
                if len(all_written) > 50:
                    _written_lines += f"\n  ... and {len(all_written) - 50} more"

                _missing_block = ""
                if _missing:
                    _show_m = _missing[:35]
                    _missing_block = (
                        f"\nFiles still needed ({len(_missing)} remaining from manifest):\n"
                        + "\n".join(f"  {f}" for f in _show_m)
                        + (f"\n  ... and {len(_missing) - 35} more" if len(_missing) > 35 else "")
                        + "\n"
                    )

                # Keep the continuation prompt SHORT — long prompts cause the
                # model to produce shorter responses.  Show only the next
                # subsystem to build, not the full list of everything missing.
                _next_subsystem = "the next layer of the project"
                if _missing:
                    if "/" in _missing[0]:
                        _first_missing_dir = _missing[0].split("/")[0]
                        _subsystem_files = [f for f in _missing if f.startswith(_first_missing_dir + "/")]
                    else:
                        _first_missing_dir = "root"
                        _subsystem_files = [f for f in _missing if "/" not in f]
                    _subsystem_files = _subsystem_files[:20]
                    _next_subsystem = (
                        f"the '{_first_missing_dir}' subsystem:\n"
                        + "\n".join(f"  {f}" for f in _subsystem_files[:15])
                    )

                _warning_prefix = ""
                if _model_declared_done_prematurely and _missing:
                    _warning_prefix = (
                        f"⚠️ WARNING: In the previous batch, you output SCAFFOLD_COMPLETE, but "
                        f"there are still {len(_missing)} files missing from your manifest. "
                        f"Do NOT output SCAFFOLD_COMPLETE until ALL remaining files are fully written and complete.\n\n"
                    )

                _batch_prompt = (
                    f"{_warning_prefix}"
                    f"Continue implementing the project for the task: \"{task_prompt}\" (batch {_batch_num}).\n\n"
                    f"Already written ({len(all_written)} files):\n{_written_lines}\n\n"
                    f"Write the files for {_next_subsystem}\n\n"
                    "KEY RULES:\n"
                    "- Write COMPLETE file contents with full implementations — no stubs, no placeholders, no '// TODO' or '/* TODO */' comments.\n"
                    "- Ensure all imports, exports, and function references are correct and fully resolved.\n"
                    "- Output SCAFFOLD_COMPLETE when ALL files from the manifest exist and are fully implemented.\n\n"
                    "Write as many files as possible now."
                )

                self.renderer.phase(
                    "implementation",
                    f"Writing batch {_batch_num} — {len(all_written)} files so far...",
                )

                # Retry each batch up to 20 times on model failure / empty
                # response.  qwen3-coder on Cloud Run can cold-start for 30-90s,
                # GPU instances can scale up under load, and individual
                # generations sometimes return empty due to truncation —
                # NONE of those should kill an overnight scaffold.  Keep
                # retrying with capped exponential back-off so the build
                # survives transient outages without operator intervention.
                _batch_resp = None
                _batch_attempts = 20
                for _attempt in range(_batch_attempts):
                    if _attempt > 0:
                        _delay = min(60, 5 * _attempt)  # 5,10,15,...,60 (cap)
                        time.sleep(_delay)
                        self.renderer.phase(
                            "fixing",
                            f"Batch {_batch_num} retry {_attempt}/{_batch_attempts - 1} after empty response (sleeping {_delay}s)...",
                        )
                    try:
                        _batch_resp = send(_batch_prompt)
                    except Exception as _send_exc:
                        self.renderer.phase(
                            "fixing",
                            f"Batch {_batch_num} attempt {_attempt + 1}: {type(_send_exc).__name__} — retrying...",
                        )
                        _batch_resp = None
                    if _batch_resp:
                        break

                if not _batch_resp:
                    # All retries failed — count this as an empty round so
                    # the outer stuck-detector handles it, instead of
                    # short-circuiting the entire scaffold on one bad batch.
                    self.renderer.warning(
                        f"Batch {_batch_num} produced no response after {_batch_attempts} attempts — "
                        f"continuing (will stop only after {20 - _empty_rounds} more empty rounds)."
                    )
                    _empty_rounds += 1
                    if _empty_rounds >= 20:
                        self.renderer.warning(
                            f"20 consecutive empty rounds — stopping scaffold. "
                            f"{len(all_written)} files written so far."
                        )
                        break
                    continue

                _check_complete = "SCAFFOLD_COMPLETE" in _batch_resp or "scaffold_complete" in _batch_resp.lower()
                _batch_written, _ = self.process_response(
                    _batch_resp, send_fn=send, phase_name="implementation"
                )
                _new = [f for f in _batch_written if f not in _written_set]

                if _new:
                    all_written.extend(_new)
                    self.renderer.info(
                        f"  Batch {_batch_num}: +{len(_new)} files ({len(all_written)} total)"
                    )

                if _check_complete:
                    _still_missing = [f for f in _manifest_exec if f not in set(all_written)]
                    if _manifest_exec and not _still_missing:
                        # Manifest exists AND all files are written — truly done
                        self.renderer.success(
                            f"Scaffold complete — all {len(_manifest_exec)} manifest files written "
                            f"({len(all_written)} total)."
                        )
                        break
                    if not _manifest_exec:
                        # No manifest to validate against — keep going until stuck
                        # (don't break on model's SCAFFOLD_COMPLETE alone)
                        self.renderer.warning(
                            "Model declared SCAFFOLD_COMPLETE but no manifest to validate — "
                            "continuing to write more files..."
                        )
                        _model_declared_done_prematurely = False
                    else:
                        self.renderer.warning(
                            f"Model declared done but {len(_still_missing)} manifest files "
                            "still missing — continuing..."
                        )
                        _model_declared_done_prematurely = True
                else:
                    _model_declared_done_prematurely = False

                if not _new:
                    _empty_rounds += 1
                    if _empty_rounds >= 20:
                        # Long-haul scaffolds (1000+ files) routinely hit
                        # transient streaks where the model recovers context
                        # and resumes generating. The previous threshold of 5
                        # killed sage prematurely on multi-hour builds. Stay
                        # patient — only quit after 20 truly-empty rounds.
                        self.renderer.warning(
                            f"20 consecutive batches produced no new files — stopping scaffold. "
                            f"{len(all_written)} files written."
                        )
                        break
                    # Vary the prompt slightly each empty round to nudge the
                    # model out of "I'm done" mode without restarting the
                    # whole scaffold.  Without this, identical prompts after
                    # an empty response tend to keep producing empty responses.
                    if _empty_rounds >= 2 and _manifest_exec:
                        _still = [f for f in _manifest_exec if f not in set(all_written)]
                        if _still:
                            self.renderer.phase(
                                "implementation",
                                f"Empty round {_empty_rounds}/20 — refocusing on {len(_still)} missing files...",
                            )
                    continue
                else:
                    _empty_rounds = 0  # reset on any new files

            written = all_written

        # Auto-validate if implementation.
        # Skip for greenfield scaffolds — running npm install / pytest on a
        # partial scaffold produces spurious errors (missing deps, unfinished
        # modules) that halt the batch continuation before the project is done.
        task_ok = bool(response) or is_info or is_investigation
        if response and response.strip().startswith(("Error:", "❌ Error:")):
            task_ok = False
        if written and not classification.read_only:
            if _is_gf_exec:
                # Run validation ONCE at the very end of the greenfield scaffold
                self.renderer.phase("testing", "Scaffold complete — running final validation and tests...")
                task_ok = self._auto_validate_and_retry(written)
            else:
                task_ok = self._auto_validate_and_retry(written)

        _close_task_dock()

        # Final response delivery (P3-71)
        # Ensures that for informational or investigation tasks, the final synthesis is visible
        should_print = (is_info or is_investigation) and response and not self.minimal_output
        if should_print:
            self.renderer.print_assistant_response(response)

        return written, task_ok


_global_agent: SAGEAgent | None = None


