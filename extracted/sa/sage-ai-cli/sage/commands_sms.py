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


from sage.core.autonomous_helpers import sms_app
@sms_app.command("setup")
def sms_setup() -> None:
    """Guided setup — bridge email, computer name, authorized phone contacts."""
    from sage.core.sms_bridge import run_setup_wizard
    run_setup_wizard()


@sms_app.command("start")
def sms_start(
    directory: Annotated[
        str | None,
        typer.Option("--dir", "-d", help="Working directory for tasks"),
    ] = None,
    model: Annotated[
        str | None,
        typer.Option("--model", "-m", help="Override AI model"),
    ] = None,
    name: Annotated[
        str | None,
        typer.Option("--name", "-n", help="Override this computer's routing name"),
    ] = None,
    foreground: Annotated[
        bool,
        typer.Option("--foreground", "-f", help="Run in foreground (default: background daemon)"),
    ] = False,
) -> None:
    """Start the bridge daemon in the background — requires sage login."""
    from sage.main import _sms_process_alive
    import shutil
    import subprocess as _sp
    from sage.core.sms_bridge import SMSConfig, SAGEMessageBridge, SMS_PID_FILE, SMS_LOG_FILE, _load_sage_token

    cfg = SMSConfig.load()
    if cfg is None:
        renderer.error("Not configured. Run: sage sms setup")
        raise typer.Exit(1)

    if directory:
        cfg.working_dir = str(Path(directory).expanduser().resolve())
    if model:
        cfg.model = model
    if name:
        cfg.computer_name = name

    try:
        token, api_base = _load_sage_token()
    except RuntimeError as exc:
        renderer.error(str(exc))
        raise typer.Exit(1)

    # ── Foreground mode: run bridge directly (used by daemon re-exec) ──────────
    if foreground:
        SMS_PID_FILE.parent.mkdir(parents=True, exist_ok=True)
        SMS_PID_FILE.write_text(str(os.getpid()))
        bridge = SAGEMessageBridge(cfg, token, api_base)
        try:
            bridge.run()
        except KeyboardInterrupt:
            pass
        return

    # ── Background daemon mode (default) ───────────────────────────────────────
    # Check if already running
    if SMS_PID_FILE.exists():
        try:
            pid = int(SMS_PID_FILE.read_text().strip())
        except ValueError:
            SMS_PID_FILE.unlink(missing_ok=True)
        else:
            if _sms_process_alive(pid):
                # P0 Security: ensure the running bridge belongs to the CURRENT user.
                # If the user logged out and into another account, we must restart.
                try:
                    from sage.core.cli_auth import get_uid_from_token
                    current_uid = get_uid_from_token(token)
                    # We can't easily query the background process's token, but we
                    # can assume if we're here and things feel 'mixed up', a restart is safest.
                    # For now, let's just always stop-and-start if explicitly called,
                    # OR just warn the user.
                    renderer.console.print(f"[yellow]Bridge already running[/yellow] (pid {pid})")
                    renderer.console.print(f"  [dim]Account: {api_base}[/dim]")
                    renderer.console.print(f"  To restart with current user: [bold]sage sms stop && sage sms start[/bold]")
                    return
                except Exception:
                    pass
                return
            SMS_PID_FILE.unlink(missing_ok=True)

    # Build re-exec command, forwarding any overrides
    if sys.platform == "win32":
        cmd = [sys.executable, "-m", "sage", "sms", "start", "--foreground"]
    else:
        sage_bin = shutil.which("sage") or sys.executable
        cmd = (
            [sage_bin, "sms", "start", "--foreground"]
            if sage_bin != sys.executable
            else [sys.executable, "-m", "sage", "sms", "start", "--foreground"]
        )
    if directory: cmd += ["--dir", cfg.working_dir]
    if model:     cmd += ["--model", cfg.model]
    if name:      cmd += ["--name", cfg.computer_name]

    SMS_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    if sys.platform == "win32":
        # WMI Win32_Process.Create breaks away from any parent Job Object or console tree on Windows,
        # ensuring the daemon survives parent CLI exit in all Windows environments.
        # Inside the child process, self._log_fp opens SMS_LOG_FILE directly and writes all log lines.
        quoted_args = []
        for x in cmd:
            if " " in x or "\\" in x or "/" in x:
                quoted_args.append(f'"{x}"')
            else:
                quoted_args.append(x)
        cmd_str = " ".join(quoted_args)
        ps_script = (
            f"$res = Invoke-CimMethod -ClassName Win32_Process -MethodName Create "
            f"-Arguments @{{ CommandLine = '{cmd_str}' }}; "
            f"if ($res.ReturnValue -eq 0) {{ echo $res.ProcessId }} else {{ exit $res.ReturnValue }}"
        )
        try:
            r = _sp.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True, text=True, check=True, timeout=10
            )
            child_pid = None
            for line in reversed(r.stdout.strip().splitlines()):
                if line.strip().isdigit():
                    child_pid = int(line.strip())
                    break
            if child_pid is None:
                raise ValueError("No PID returned from WMI CreateProcess")
            class MockProc:
                def __init__(self, pid):
                    self.pid = pid
            proc = MockProc(child_pid)
        except Exception as exc:
            # Fallback to standard Popen if WMI fails (should not happen on modern Windows)
            log_fp = open(SMS_LOG_FILE, "a")
            proc = _sp.Popen(
                cmd,
                stdout=log_fp,
                stderr=_sp.STDOUT,
                creationflags=0x00000008 | 0x08000000,
                close_fds=False,
            )
    else:
        log_fp = open(SMS_LOG_FILE, "a")
        proc = _sp.Popen(cmd, stdout=log_fp, stderr=_sp.STDOUT, start_new_session=True)
    SMS_PID_FILE.write_text(str(proc.pid))

    renderer.console.print("\n[bold green]✦ SAGE Message Bridge started[/bold green]")
    renderer.console.print(f"  Computer : [bold cyan]{cfg.computer_name}[/bold cyan]")
    renderer.console.print(f"  Dir      : [cyan]{cfg.working_dir}[/cyan]")
    renderer.console.print(f"  Model    : [cyan]{cfg.model or 'default'}[/cyan]")
    renderer.console.print(f"  PID      : [dim]{proc.pid}[/dim]")
    renderer.console.print(f"  Logs     : [dim]{SMS_LOG_FILE}[/dim]")
    renderer.console.print()
    renderer.console.print("  [dim]Stop with:[/dim]  [bold]sage sms stop[/bold]")
    renderer.console.print("  [dim]Tail logs:[/dim]  [bold]tail -f ~/.sage/sms.log[/bold]")
    renderer.console.print()


@sms_app.command("stop")
def sms_stop() -> None:
    """Stop the running bridge daemon on this computer."""
    from sage.main import _sms_process_alive, _sms_terminate_process
    from sage.core.sms_bridge import SMS_PID_FILE

    if not SMS_PID_FILE.exists():
        renderer.warning("Bridge not running (no PID file).")
        return
    try:
        pid = int(SMS_PID_FILE.read_text().strip())
    except ValueError:
        SMS_PID_FILE.unlink(missing_ok=True)
        renderer.warning("Stale PID file removed.")
        return

    if not _sms_process_alive(pid):
        SMS_PID_FILE.unlink(missing_ok=True)
        renderer.warning("Bridge already stopped.")
        return

    if _sms_terminate_process(pid):
        SMS_PID_FILE.unlink(missing_ok=True)
        renderer.success(f"Bridge stopped (pid {pid})")
    else:
        renderer.error(
            f"Could not terminate pid {pid}. "
            "Try running PowerShell as Administrator, or end the process "
            "in Task Manager and run `sage sms start` again."
        )


@sms_app.command("logs")
def sms_logs() -> None:
    """Tail the bridge log file (live output — Ctrl-C to stop)."""
    from sage.core.sms_bridge import SMS_LOG_FILE

    if not SMS_LOG_FILE.exists():
        renderer.console.print(f"No log file yet. Start the bridge first: [bold]sage sms start[/bold]")
        return

    renderer.console.print(f"[dim]Tailing {SMS_LOG_FILE} — Ctrl-C to stop[/dim]\n")
    # Pure-Python tail-f. The previous implementation shelled out to
    # `tail -f`, which doesn't exist on Windows (cmd/PowerShell). This
    # works the same on macOS, Linux, and Windows: print the last ~200
    # lines for context, then poll for new bytes every 0.5s.
    try:
        # Show the tail (last ~200 lines) so the user has context
        # immediately, matching `tail -f` behavior.
        with SMS_LOG_FILE.open("r", encoding="utf-8", errors="replace") as f:
            try:
                f.seek(0, 2)            # end
                size = f.tell()
                # Read up to last 64 KB (cheap, plenty for ~200 lines)
                f.seek(max(0, size - 65536))
                tail = f.read()
                # Drop a possibly-partial first line if we mid-line-seeked
                if size > 65536 and "\n" in tail:
                    tail = tail.split("\n", 1)[1]
                lines = tail.splitlines()[-200:]
                for line in lines:
                    renderer.console.print(line, highlight=False)
            except Exception:
                pass

        # Now follow.
        with SMS_LOG_FILE.open("r", encoding="utf-8", errors="replace") as f:
            f.seek(0, 2)  # seek to end
            while True:
                line = f.readline()
                if line:
                    renderer.console.print(line.rstrip("\n"), highlight=False)
                else:
                    time.sleep(0.5)
    except KeyboardInterrupt:
        pass


@sms_app.command("test-imessage")
def sms_test_imessage(
    recipient: Annotated[str, typer.Argument(help="Email or phone number to test")],
    text: Annotated[str, typer.Option("--text", "-t", help="Test message text")] = "Test iMessage from SAGE",
) -> None:
    """Manually test iMessage delivery from this Mac to a specific handle."""
    if platform.system() != "Darwin":
        renderer.error("iMessage testing is only supported on macOS.")
        raise typer.Exit(1)
        
    from sage.core.sms_bridge import _send_imessage
    
    renderer.console.print(f"\n[bold blue]Testing iMessage delivery...[/bold blue]")
    renderer.console.print(f"Handle: [cyan]{recipient}[/cyan]")
    renderer.console.print(f"Text:   {text}\n")
    
    with renderer.console.status("[bold yellow]Dispatching and verifying...[/bold yellow]"):
        success = _send_imessage(recipient, text)
        
    if success:
        renderer.console.print(f"\n✅ [bold green]SUCCESS![/bold green] iMessage was successfully sent and verified in chat.db.")
        renderer.console.print(f"Recipent [cyan]{recipient}[/cyan] should receive it momentarily.")
    else:
        renderer.console.print(f"\n❌ [bold red]FAILURE![/bold red] Delivery could not be verified.")
        renderer.console.print("[dim]Common fixes:[/dim]")
        renderer.console.print("  1. Ensure Messages.app is [bold]signed into iCloud[/bold].")
        renderer.console.print("  2. Ensure the recipient's handle is [bold]iMessage-capable[/bold].")
        renderer.console.print("  3. Grant Sage CLI [bold]Full Disk Access[/bold] in System Settings → Privacy & Security.")
        renderer.console.print("  4. Try a different format (e.g. phone with/without country code).")
    
    renderer.console.print()


@sms_app.command("status")
def sms_status() -> None:
    """Show this computer's bridge status and your account-wide devices/contacts."""
    from sage.main import _sms_backend, _sms_process_alive
    from sage.core.sms_bridge import SMSConfig, SMS_PID_FILE

    cfg = SMSConfig.load()
    if cfg is None:
        renderer.warning("Not configured. Run: sage sms setup")
        return

    running = False
    if SMS_PID_FILE.exists():
        try:
            pid = int(SMS_PID_FILE.read_text().strip())
            running = _sms_process_alive(pid)
        except ValueError:
            pass

    dot = "[green]●[/green]" if running else "[yellow]○[/yellow]"
    renderer.console.print(f"\n{dot} [{cfg.computer_name}]  Bridge: [cyan]messages@sageworksai.com[/cyan]")
    renderer.console.print(f"   Dir: [cyan]{cfg.working_dir}[/cyan]  Model: [cyan]{cfg.model or 'default'}[/cyan]\n")

    try:
        be = _sms_backend()
        computers = be.list_computers()
        contacts = be.list_contacts()
        renderer.console.print(f"[bold]Your computers ({len(computers)}):[/bold]")
        for c in computers:
            indicator = "[green]●[/green]" if c["computer_name"] == cfg.computer_name and running else "○"
            renderer.console.print(f"  {indicator} [cyan]@{c['computer_name']}[/cyan]  bridge: {c.get('bridge_email','')}  last: {c.get('last_seen','?')[:19]}")
        renderer.console.print()
        renderer.console.print(f"[bold]Authorized contacts ({len(contacts)}):[/bold]")
        for ct in contacts:
            renderer.console.print(f"  {ct['email']}  [dim]{ct.get('label','')}[/dim]")
        renderer.console.print()
    except Exception as exc:
        renderer.warning(f"Could not fetch account data: {exc}")


@sms_app.command("devices")
def sms_devices() -> None:
    """List all computers registered to your SAGE account."""
    from sage.main import _sms_backend
    try:
        be = _sms_backend()
        computers = be.list_computers()
    except RuntimeError as exc:
        renderer.error(str(exc)); raise typer.Exit(1)

    if not computers:
        renderer.console.print("No computers registered. Run: sage sms start")
        return

    renderer.console.print(f"\n[bold]Your SAGE computers ({len(computers)}):[/bold]\n")
    for c in computers:
        renderer.console.print(
            f"  [cyan]@{c['computer_name']}[/cyan]"
            f"  id={c['computer_id']}"
            f"  last_seen={c.get('last_seen','?')[:19]}"
        )
    renderer.console.print()
    renderer.console.print("[dim]Route a task: @name: your task  |  Broadcast: @all: git status[/dim]\n")


@sms_app.command("unregister")
def sms_unregister(
    computer_id: Annotated[str, typer.Argument(help="computer_id from `sage sms devices`")],
) -> None:
    """Remove a computer from your account (run sage sms devices to find the ID)."""
    from sage.main import _sms_backend
    import httpx as _httpx
    try:
        be = _sms_backend()
        be.remove_computer(computer_id)
        renderer.success(f"Removed computer {computer_id}")
    except RuntimeError as exc:
        renderer.error(str(exc)); raise typer.Exit(1)
    except _httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            renderer.error(f"Computer not found: {computer_id}")
        else:
            renderer.error(str(exc))
        raise typer.Exit(1)
    except Exception as exc:
        renderer.error(str(exc)); raise typer.Exit(1)


@sms_app.command("test")
def sms_test() -> None:
    """Verify bridge connectivity and trigger a test announcement to all contacts."""
    from sage.main import _sms_backend
    from sage.core.sms_bridge import SMSConfig

    cfg = SMSConfig.load()
    if cfg is None:
        renderer.error("Not configured. Run: sage sms setup")
        raise typer.Exit(1)

    try:
        be = _sms_backend()
        added = be.sync_provider_contacts()
        if added:
            for a in added:
                renderer.console.print(f"  [dim]Auto-registered {a['provider']} contact: {a['email']}[/dim]")
        contacts = be.contact_emails()

        # Pre-flight: check that the bridge is actually running. iMessage and
        # KDE Connect delivery require the WebSocket to be open.
        online_now = []
        for _ in range(3): # Wait up to 3s for background bridge to connect
            ps = be.poller_status()
            online_now = ps.get("online_computers", [])
            if online_now: break
            time.sleep(1)

        if not online_now:
            renderer.warning(
                "Bridge not running on this account — only email delivery will fire.\n"
                "Run `sage sms start` (in another terminal) BEFORE `sage sms test` "
                "to exercise iMessage and KDE Connect."
            )

        # Trigger a real announcement — backend fans out to email + iMessage +
        # KDE Connect for every configured contact and returns by-method counts.
        result = be.announce(cfg.computer_name)
        
        by_method = result.get("by_method", {}) if isinstance(result, dict) else {}
        n_email      = by_method.get("email", 0)
        n_imessage   = by_method.get("imessage", 0)
        n_kde        = by_method.get("kdeconnect", 0)
        n_skipped    = by_method.get("skipped_untagged", 0)

        # Fallback for iMessage if WS not connected but we are on darwin
        if not online_now and sys.platform == "darwin":
            from sage.core.sms_bridge import _send_imessage
            announce_text = (
                f"✅ [{cfg.computer_name}] SAGE is online and ready.\n"
                f"Send me any task and I'll run it on your computer.\n"
                f"Reply @help to see available commands."
            )
            for c in contacts:
                # Fallback works for direct iCloud emails AND phone number contacts
                is_imessage_target = (
                    "@icloud.com" in c or "@me.com" in c or "@mac.com" in c or
                    c.startswith("phone:")
                )
                if is_imessage_target:
                    target = c.replace("phone:", "")
                    if _send_imessage(target, f"[SAGE — {cfg.computer_name}] {announce_text}"):
                        n_imessage += 1

    except RuntimeError as exc:
        renderer.error(str(exc)); raise typer.Exit(1)

    renderer.success(f"Backend connection OK  [{cfg.computer_name}]")

    renderer.console.print("\n[bold]Test announcement delivery:[/bold]")
    renderer.console.print(f"  📧 Email:        [{('green' if n_email else 'dim')}]{n_email}[/]")
    renderer.console.print(f"  💬 iMessage:     [{('green' if n_imessage else 'dim')}]{n_imessage}[/]")
    renderer.console.print(f"  📱 KDE Connect:  [{('green' if n_kde else 'dim')}]{n_kde}[/]")
    if n_skipped:
        renderer.console.print(
            f"  [yellow]⚠ {n_skipped} phone contact(s) had no device tag — re-add with "
            f"--device apple|android to enable iMessage/KDE Connect delivery.[/yellow]"
        )

    if not contacts:
        renderer.warning("No contacts registered. Run: sage sms contacts add <phone-or-email>")
        return

    # Deduplicate and enrich display
    all_contacts = be.list_contacts()
    unique_contacts = {}
    for c in all_contacts:
        email = c.get("email")
        if not email: continue
        if email not in unique_contacts:
            unique_contacts[email] = c
            
    renderer.console.print(f"\n[bold]Authorized contacts ({len(unique_contacts)}):[/bold]")
    for email, data in unique_contacts.items():
        dev = data.get("device_type")
        tag = f" [[cyan]{dev}[/cyan]]" if dev else ""
        renderer.console.print(f"  [cyan]{email}[/cyan]{tag}")
    renderer.console.print(
        f"\n[dim]Email [bold]messages@sageworksai.com[/bold] from any of the above, "
        "or text from a tagged phone, to send a task.[/dim]\n"
        "[dim]Run [bold]sage sms diagnose[/bold] if anything's missing.[/dim]\n"
    )


@sms_app.command("test-imessage")
def sms_test_imessage(recipient: str = typer.Argument(..., help="Phone (+1XXXXXXXXXX) or iCloud email")) -> None:
    """Send a test iMessage directly from this Mac to diagnose delivery issues.

    Use this to verify that Messages.app can reach a specific address before
    adding it as a contact.  Try both the phone number AND iCloud email for
    the same person to see which handle works.

    Examples:
      sage sms test-imessage +14085073140
      sage sms test-imessage jane@icloud.com
    """
    import sys
    if sys.platform != "darwin":
        renderer.error("iMessage is only available on macOS.")
        raise typer.Exit(1)

    from sage.core.sms_bridge import _send_imessage, _imessage_max_rowid
    renderer.console.print(f"[bold]Testing iMessage delivery to:[/bold] {recipient}")
    renderer.console.print("[dim]Sending via Messages.app (osascript)...[/dim]")

    test_text = "SAGE iMessage test — if you see this, delivery is working ✅"
    before = _imessage_max_rowid()
    ok = _send_imessage(recipient, test_text)

    if ok:
        renderer.success(f"iMessage delivered to {recipient}")
        renderer.console.print("[dim]The recipient should have received the test message.[/dim]")
    else:
        renderer.error(f"iMessage to {recipient} FAILED")
        renderer.console.print(
            "\n[bold]Troubleshooting steps:[/bold]\n"
            "  1. Open Messages.app and sign in with your Apple ID\n"
            "  2. In Messages → Preferences → iMessage, verify the account is active\n"
            "  3. Try sending a message to this address manually in Messages.app\n"
            "  4. If the address is a phone number, ensure the recipient has iMessage\n"
            "     enabled (blue bubble, not green SMS)\n"
            "  5. If the address is an @icloud.com email, ensure the recipient has\n"
            "     this email enabled as an iMessage handle in their device settings\n"
            f"  6. Try the other handle — phone instead of email or vice versa\n"
        )
        raise typer.Exit(1)


@sms_app.command("kde-takeover")
def sms_kde_takeover() -> None:
    """Replace the OS KDE Connect daemon with SAGE's parallel listener.

    The macOS Mac App Store build of KDE Connect has a broken DBus
    registration that prevents inbound SMS from being read by anything
    outside its own GUI. SAGE's listener handles both inbound AND outbound
    SMS, but it can't run alongside the OS daemon (port 1716 conflict).

    This command:
      1. Asks KDE Connect.app to quit
      2. Restarts the SAGE bridge so its listener can bind to port 1716
      3. Prints the one-time pairing instructions for your Android phone

    To revert: open KDE Connect.app from /Applications and restart the bridge.
    """
    import subprocess as _sp
    import time as _t
    import sys
    from sage.core.kdeconnect_listener import _stop_os_daemon

    renderer.console.print("\n[bold]SAGE — KDE Connect Takeover[/bold]\n")
    # Quit GUI/App cleanly if possible
    if sys.platform == "darwin":
        quit_script = 'tell application "KDE Connect" to quit'
        try:
            _sp.run(["osascript", "-e", quit_script],
                    capture_output=True, timeout=10)
        except Exception as exc:
            renderer.warning(f"Couldn't quit KDE Connect.app via AppleScript: {exc}")
        
        # Kill GUI app if still running
        try:
            _sp.run(["pkill", "-x", "kdeconnect-app"], capture_output=True, timeout=5)
        except Exception:
            pass
    elif sys.platform == "win32":
        try:
            from sage.core.kdeconnect_listener import _win32_kill_process_by_name
            _win32_kill_process_by_name("kdeconnect-app.exe")
        except Exception:
            pass
    else:
        try:
            _sp.run(["pkill", "-x", "kdeconnect-app"], capture_output=True, timeout=5)
        except Exception:
            pass

    # Stop the daemon cross-platform
    renderer.console.print("[dim]Stopping OS daemon…[/dim]")
    stopped = _stop_os_daemon()
    if not stopped:
        renderer.warning("OS kdeconnectd could not be stopped or is still running.")
    _t.sleep(2)

    # Verify port 1716 is now free
    import socket as _s
    sock = _s.socket(_s.AF_INET, _s.SOCK_DGRAM)
    try:
        sock.bind(("0.0.0.0", 1716))
        sock.close()
        renderer.success("Port 1716 free — OS daemon stopped")
    except OSError as exc:
        sock.close()
        renderer.error(
            f"Port 1716 still in use ({exc}). Quit KDE Connect manually "
            "from the menu bar or task manager, then run this command again."
        )
        raise typer.Exit(1)

    # Step 2: restart bridge so it picks up port 1716
    renderer.console.print("[dim]Restarting bridge…[/dim]")
    try:
        _sp.run(["sage", "sms", "stop"], capture_output=True, timeout=10)
        _t.sleep(2)
        _sp.run(["sage", "sms", "start"], capture_output=True, timeout=15)
        _t.sleep(5)
    except Exception as exc:
        renderer.error(f"Bridge restart failed: {exc}")
        raise typer.Exit(1)

    revert_msg = ""
    if sys.platform == "darwin":
        revert_msg = "open /Applications/KDE Connect.app"
    elif sys.platform == "win32":
        revert_msg = "open KDE Connect from the Start Menu"
    else:
        revert_msg = "start KDE Connect from your applications menu"

    renderer.success("Bridge restarted with KDE Connect listener.")
    renderer.console.print(
        "\n[bold]Next:[/bold]\n"
        "  1. On your Android phone, open the [bold]KDE Connect[/bold] app.\n"
        "  2. Under [bold]Available devices[/bold], tap [bold]'SAGE Bridge'[/bold].\n"
        "  3. Tap [bold]Pair[/bold] — SAGE auto-accepts on this end.\n"
        "  4. Send any text from your Android — sage will reply to your phone.\n"
        f"\n[dim]To revert: {revert_msg} and restart "
        "the bridge.[/dim]\n"
    )


@sms_app.command("allow-firewall")
def sms_allow_firewall() -> None:
    """Open Windows Firewall on TCP+UDP 1716 so KDE Connect inbound works.

    Adds two inbound allow rules to Windows Defender Firewall:
      • TCP 1716  — phone reconnects to SAGE
      • UDP 1716  — phone discovery broadcasts reach SAGE

    Requires elevation (UAC prompt). On macOS / Linux this is a no-op
    since neither blocks 1716 by default for the user's listening
    process.

    Without these rules, kdeconnectd's own firewall exception covers
    only `kdeconnectd.exe`, NOT the Python process that takes over the
    port — so SAGE binds 1716 successfully but the phone's traffic
    never reaches it.
    """
    if sys.platform != "win32":
        renderer.success(
            f"No firewall changes needed on {sys.platform} — "
            "the kernel doesn't block inbound on 1716 by default for user processes."
        )
        return

    # Use netsh (every Windows build has it; PowerShell may be Constrained
    # Language Mode on locked-down boxes). ShellExecuteW with "runas" verb
    # triggers the UAC prompt — the only non-admin way to elevate from a
    # non-admin shell on Windows.
    rules = [
        ('SAGE KDE Connect TCP', 'TCP'),
        ('SAGE KDE Connect UDP', 'UDP'),
    ]
    netsh_cmds = []
    for name, proto in rules:
        netsh_cmds.append(
            f'netsh advfirewall firewall delete rule name="{name}" >nul 2>&1 & '
            f'netsh advfirewall firewall add rule name="{name}" '
            f'dir=in protocol={proto} localport=1716 action=allow profile=any'
        )
    cmd_payload = " & ".join(netsh_cmds) + " & echo. & echo Done. & pause"

    renderer.console.print(
        "\n[bold]Adding Windows Firewall rules for KDE Connect (port 1716)…[/bold]\n"
        "[dim]Click 'Yes' on the UAC prompt that appears.[/dim]\n"
    )

    try:
        import ctypes
        # ShellExecuteW returns >32 on success. SW_SHOWNORMAL = 1.
        ret = ctypes.windll.shell32.ShellExecuteW(
            None,           # parent HWND
            "runas",        # request elevation
            "cmd.exe",
            f"/c {cmd_payload}",
            None,           # cwd
            1,              # SW_SHOWNORMAL
        )
        if int(ret) <= 32:
            renderer.error(
                f"Couldn't trigger UAC prompt (ShellExecuteW returned {ret}). "
                "Run this in an Administrator PowerShell instead:\n\n"
                '  netsh advfirewall firewall add rule name="SAGE KDE Connect TCP" '
                'dir=in protocol=TCP localport=1716 action=allow\n'
                '  netsh advfirewall firewall add rule name="SAGE KDE Connect UDP" '
                'dir=in protocol=UDP localport=1716 action=allow'
            )
            raise typer.Exit(1)
    except Exception as exc:
        renderer.error(f"Couldn't add firewall rules: {exc}")
        raise typer.Exit(1)

    renderer.success(
        "Firewall command launched. After the elevated window closes, "
        "restart the bridge: sage sms stop && sage sms start"
    )


@sms_app.command("diagnose")
def sms_diagnose() -> None:
    """Run health checks across the bridge — auth, WS, contacts, native delivery paths.

    Prints a green/yellow/red status for each capability so you can see at a
    glance whether SMS, iMessage, KDE Connect, and the bridge inbox are all
    wired up correctly.
    """
    from sage.main import _sms_backend, _sms_process_alive
    import platform
    import shutil as _sh
    from sage.core.sms_bridge import (
        SMSConfig, _find_kdeconnect_cli, _send_imessage,
    )
    from sage.core.cli_auth import load_auth, _jwt_exp
    import time as _time

    OK   = "[bold green]✓[/bold green]"
    WARN = "[bold yellow]![/bold yellow]"
    BAD  = "[bold red]✗[/bold red]"

    def line(mark: str, msg: str, hint: str = "") -> None:
        renderer.console.print(f"  {mark} {msg}")
        if hint:
            renderer.console.print(f"      [dim]{hint}[/dim]")

    renderer.console.print("\n[bold]SAGE Message Bridge — Diagnostics[/bold]\n")
    renderer.console.print(
        "[dim]Tip: SAGE receives [bold]email[/bold] (not SMS) at messages@sageworksai.com.[/dim]\n"
        "[dim]Send from your phone's email app (Gmail / Apple Mail) — texting that[/dim]\n"
        "[dim]address only works on a few carriers and silently fails on most.[/dim]\n"
    )

    # ── 1. Auth + token freshness ──────────────────────────────────────────────
    auth = load_auth()
    if not auth:
        line(BAD, "Not logged in", "Run: sage login")
        return
    jwt_exp = _jwt_exp(auth.get("id_token", ""))
    seconds_left = int(jwt_exp - _time.time()) if jwt_exp else 0
    if seconds_left > 60:
        line(OK, f"Logged in as {auth.get('email')}  (token: {seconds_left}s left)")
    elif auth.get("refresh_token"):
        line(WARN, f"Token near expiry ({seconds_left}s) — auto-refresh on next call")
    else:
        line(BAD, "Token expired and no refresh token", "Run: sage login")

    # ── 2. Backend connectivity + contacts ─────────────────────────────────────
    try:
        be = _sms_backend()
        contacts = be.list_contacts()
        line(OK, f"Backend reachable  ({len(contacts)} contact(s) registered)")
    except Exception as exc:
        line(BAD, f"Backend connection failed: {exc}", "Check internet, then: sage login")
        return

    # ── 3. Bridge config ───────────────────────────────────────────────────────
    cfg = SMSConfig.load()
    if cfg:
        line(OK, f"Bridge config: {cfg.computer_name}  →  {cfg.working_dir}")
    else:
        line(WARN, "No bridge config", "Run: sage sms setup")

    # ── 4. Contact health ──────────────────────────────────────────────────────
    phone_contacts = [c for c in contacts if c.get("email", "").startswith("phone:")]
    untagged = [c for c in phone_contacts if not c.get("device_type")]
    if untagged:
        line(WARN,
             f"{len(untagged)} phone contact(s) have no device tag — "
             "fallbacks (iMessage/KDE Connect) will not fire",
             "Re-add with --device apple|android, or remove + re-add")
        for c in untagged[:5]:
            renderer.console.print(f"        • {c.get('display', c.get('email'))}")
    else:
        line(OK, f"All phone contacts tagged ({len(phone_contacts)} total)")

    # ── 5. Native delivery paths ───────────────────────────────────────────────
    has_apple = any(c.get("device_type") == "apple" for c in phone_contacts)
    has_android = any(c.get("device_type") == "android" for c in phone_contacts)

    # Apple → iMessage (only meaningful on macOS)
    if has_apple:
        if platform.system() == "Darwin":
            applescript_ok = bool(_sh.which("osascript"))
            messages_app   = os.path.exists("/System/Applications/Messages.app") or \
                             os.path.exists("/Applications/Messages.app")
            if not (applescript_ok and messages_app):
                line(BAD, "iMessage path broken on this Mac",
                     "Open Messages.app, sign into iCloud, enable iMessage in Settings → Messages")
            else:
                # ── iMessage DB (Full Disk Access) check ──
                db_path = os.path.expanduser("~/Library/Messages/chat.db")
                if not os.path.exists(db_path):
                     line(WARN, "iMessage database missing", "Messages.app may never have been used on this Mac.")
                else:
                    try:
                        import sqlite3
                        with sqlite3.connect(f"file:{db_path}?mode=ro", uri=True, timeout=1) as db:
                            db.execute("SELECT 1 FROM message LIMIT 1")
                        line(OK, "iMessage verification active (Full Disk Access granted)")
                    except Exception:
                        line(WARN, "iMessage verification disabled (Full Disk Access missing)",
                             "Sage can send iMessages, but cannot verify if they arrived. "
                             "Fix: System Settings → Privacy & Security → Full Disk Access → add your terminal app")
                
                import subprocess as _sp
                probe = (
                    'tell application "Messages"\n'
                    '    try\n'
                    '        get name of (1st service whose service type = iMessage)\n'
                    '        return "ok"\n'
                    '    on error errMsg number errNum\n'
                    '        return "err " & errNum & ": " & errMsg\n'
                    '    end try\n'
                    'end tell'
                )
                try:
                    r = _sp.run(["osascript", "-e", probe],
                                capture_output=True, text=True, timeout=5)
                    out = (r.stdout or "").strip()
                except Exception as exc:
                    out = f"err: {exc}"

                if out == "ok":
                    line(OK, "iMessage path: Messages.app responding to AppleScript")
                elif "1743" in out or "not allowed" in out.lower():
                    line(BAD, "AppleScript not allowed to control Messages.app",
                         "System Settings → Privacy & Security → Automation → "
                         "enable Messages for your terminal app (Terminal / iTerm). "
                         "Then quit and re-open the terminal.")
                else:
                    line(WARN, f"Messages.app probe returned: {out or '(empty)'}",
                         "Open Messages.app once and ensure iMessage is signed in.")
        else:
            line(WARN, "iMessage requires macOS — Apple-tagged contacts won't deliver from this OS",
                 "Run a SAGE bridge on a Mac, or remove --device apple from those contacts")

    # Android → KDE Connect. We rely on `--list-available` which goes through
    # the network discovery fallback and works even when DBus activation fails
    # (the case on the Mac App Store build).
    if has_android:
        from sage.core.sms_bridge import _find_kdeconnect_cli, _kdeconnectd_running
        kdc = _find_kdeconnect_cli()
        if not kdc:
            line(BAD, "KDE Connect not installed",
                 "macOS: Mac App Store 'KDE Connect'  |  "
                 "Linux: apt install kdeconnect  |  "
                 "Windows: Microsoft Store 'KDE Connect'")
        else:
            ok, reason = _kdeconnectd_running()
            if ok:
                try:
                    import subprocess as _sp
                    r = _sp.run([kdc, "--list-available", "--id-only"],
                                capture_output=True, text=True, timeout=5)
                    paired = []
                    for line_str in (r.stdout or "").splitlines():
                        line_str = line_str.strip()
                        if not line_str or "devices found" in line_str.lower() or " " in line_str:
                            continue
                        paired.append(line_str)
                    if paired:
                        line(OK, f"KDE Connect: {len(paired)} paired+reachable device(s)")
                    else:
                        line(WARN, f"KDE Connect: no paired+reachable device(s) online",
                             "Open the KDE Connect GUI app on your computer and phone, and ensure they are paired on the same Wi-Fi.")
                except Exception as exc:
                    line(WARN, f"KDE Connect probe failed: {exc}")
            else:
                line(BAD, f"KDE Connect: {reason}",
                     "Open the KDE Connect GUI app and ensure your Android phone is paired+reachable on the same Wi-Fi")

    if not phone_contacts:
        line(WARN, "No phone contacts registered",
             "sage sms contacts add <phone> --device apple|android")

    # ── Inbound from Android (RCS detection) ───────────────────────────────────
    # If the user has Android-tagged contacts and we see only RCS service in
    # chat.db with is_from_me=1 (outbound), inbound from those numbers won't
    # arrive — RCS messages aren't forwarded by iPhone Text Message Forwarding.
    import re
    if has_android and platform.system() == "Darwin":
        chat_db = os.path.expanduser("~/Library/Messages/chat.db")
        if os.path.exists(chat_db):
            try:
                import sqlite3 as _sql
                with _sql.connect(f"file:{chat_db}?mode=ro", uri=True, timeout=2) as _db:
                    rcs_problem_numbers = []
                    # Check the last 30 days of activity per Android contact.
                    # If there's been outbound RCS but no inbound in that window,
                    # iPhone Text Message Forwarding isn't relaying inbound.
                    cutoff_apple_epoch = (_time.time() - 30 * 86400 - 978307200) * 1_000_000_000
                    for c in phone_contacts:
                        if c.get("device_type") != "android":
                            continue
                        digits = re.sub(r"\D", "", (c.get("email") or "").replace("phone:", ""))
                        if len(digits) == 11 and digits.startswith("1"):
                            digits = digits[1:]
                        if len(digits) != 10:
                            continue
                        e164 = f"+1{digits}"
                        cur = _db.execute("""
                            SELECT m.service, m.is_from_me
                              FROM message m JOIN handle h ON m.handle_id = h.ROWID
                             WHERE h.id = ? AND m.date > ?
                          ORDER BY m.date DESC LIMIT 30
                        """, (e164, int(cutoff_apple_epoch)))
                        rows = cur.fetchall()
                        if not rows:
                            continue
                        recent_inbound = [r for r in rows if r[1] == 0]
                        recent_outbound = [r for r in rows if r[1] == 1]
                        # Outbound exists but ZERO inbound in last 30d AND
                        # outbound is RCS-only → iPhone is using RCS, no relay.
                        if recent_outbound and not recent_inbound and \
                           all(r[0] == "RCS" for r in recent_outbound):
                            rcs_problem_numbers.append(e164)
                    if rcs_problem_numbers:
                        line(BAD,
                             f"RCS detected for {', '.join(rcs_problem_numbers)} — "
                             "inbound from these numbers will NOT reach SAGE",
                             "iPhone Text Message Forwarding doesn't relay RCS. "
                             "Fix on the Android phone: Google Messages → tap the "
                             "conversation → ⋮ menu → Details → toggle 'Chat features' OFF. "
                             "Then re-send the message — it'll go as plain SMS.")
                    else:
                        line(OK, "Android inbound path: SMS history present, no RCS-only blockers")
            except Exception as exc:
                line(WARN, f"Could not check chat.db for RCS: {exc}")

    # ── 6. Backend IMAP poller health ──────────────────────────────────────────
    try:
        ps = be.poller_status()
        if ps.get("error"):
            line(WARN, f"Couldn't reach backend poller status: {ps['error']}")
        elif not ps.get("imap_connected"):
            # Brief disconnects (<30s) are normal — the IDLE timeout fires every
            # ~25s and triggers a NOOP+reconnect cycle. Only alarm if the gap is
            # genuinely long.
            err_at = ps.get("last_error_at") or 0
            err = ps.get("last_error") or "unknown"
            gap = _time.time() - err_at if err_at else 999
            if gap < 30:
                line(WARN, f"IMAP poller reconnecting (gap {int(gap)}s, last: {err})")
            else:
                line(BAD, f"Backend IMAP poller DISCONNECTED for {int(gap)}s (last error: {err})",
                     "Inbound mail is queued but not being processed. "
                     "Re-deploy or contact support.")
        else:
            connected_at = ps.get("imap_connected_at")
            uptime = int(_time.time() - connected_at) if connected_at else 0
            stats = (f"processed={ps.get('messages_processed', 0)} "
                     f"dispatched={ps.get('tasks_dispatched', 0)} "
                     f"uptime={uptime}s")
            line(OK, f"Backend IMAP poller connected  ({stats})")
            last_msg = ps.get("last_message_at")
            if last_msg:
                ago = int(_time.time() - last_msg)
                line(OK, f"Last inbound message: {ago}s ago  (from: {ps.get('last_message_from','?')})")
            online = ps.get("online_computers", [])
            if online:
                line(OK, f"Online CLIs (server view): {', '.join(online)}")
            else:
                line(WARN, "Backend sees no online CLIs for this account",
                     "Ensure `sage sms start` is running on at least one computer")
    except Exception as exc:
        line(WARN, f"Couldn't query backend poller: {exc}")

    # ── 7. Bridge process ──────────────────────────────────────────────────────
    from sage.core.sms_bridge import SMS_PID_FILE
    if SMS_PID_FILE.exists():
        try:
            pid = int(SMS_PID_FILE.read_text().strip())
        except ValueError:
            line(WARN, "Bridge PID file unparseable", "Run: sage sms start")
        else:
            if _sms_process_alive(pid):
                line(OK, f"Bridge daemon running  (pid {pid})")
            else:
                line(WARN, "Bridge PID file stale", "Run: sage sms start")
    else:
        line(WARN, "Bridge daemon not running", "Run: sage sms start")

    renderer.console.print()


# ── sage sms contacts subgroup ─────────────────────────────────────────────────

sms_contacts_app = typer.Typer(help="Manage authorized phone contacts for your SAGE account")
sms_app.add_typer(sms_contacts_app, name="contacts")


@sms_contacts_app.command("list")
def sms_contacts_list() -> None:
    """List all phone contacts authorized to send commands to your SAGE computers."""
    from sage.main import _sms_backend
    try:
        contacts = _sms_backend().list_contacts()
    except RuntimeError as exc:
        renderer.error(str(exc)); raise typer.Exit(1)

    if not contacts:
        renderer.console.print("No contacts. Add with: sage sms contacts add <email>")
        return

    renderer.console.print(f"\n[bold]Authorized contacts ({len(contacts)}):[/bold]\n")
    for c in contacts:
        display  = c.get("display") or c.get("email", "")
        stored   = c.get("email", "")
        label_   = c.get("label", "")
        provider = c.get("provider", "")
        device   = (c.get("device_type") or "").lower()
        # Show a short provider tag so Google + Apple with the same email
        # are visually distinct in the list.
        provider_tag = ""
        if provider == "google.com":
            provider_tag = "[bold blue][Google][/bold blue] "
        elif provider == "apple.com":
            provider_tag = "[bold]\\[Apple][/bold] "
        # Device tag shows which fallback path SAGE will use for phone contacts
        device_tag = ""
        if device == "apple":
            device_tag = "  [bold]\\[iPhone → iMessage][/bold]"
        elif device == "android":
            device_tag = "  [bold green]\\[Android → KDE Connect][/bold green]"
        if stored.startswith("phone:"):
            suffix = device_tag or "  [dim](no device tag — fallbacks disabled)[/dim]"
            renderer.console.print(f"  {provider_tag}[cyan]{display}[/cyan]  [dim]{label_}[/dim]{suffix}")
        else:
            renderer.console.print(f"  {provider_tag}[cyan]{display}[/cyan]  [dim]{label_}[/dim]")
    renderer.console.print()


@sms_contacts_app.command("add")
def sms_contacts_add(
    email: Annotated[str, typer.Argument(help="Email address OR phone number (e.g. 4085553210)")],
    label: Annotated[str, typer.Option("--label", "-l", help='Label, e.g. "My iPhone"')] = "",
    device: Annotated[
        str,
        typer.Option(
            "--device", "-d",
            help='Phone OS for SMS fallback routing: "apple" or "android". Prompts if not given for phone numbers.',
        ),
    ] = "",
) -> None:
    """Add an authorized contact — accepts email addresses or phone numbers.

    For phone numbers, SAGE prompts whether the phone is Apple or Android so
    the SMS-bounce fallback can pick the right delivery path:
      - apple   → iMessage from this Mac (when Apple ID is linked)
      - android → KDE Connect SMS via paired Android phone
    """
    from sage.main import _sms_backend
    import re as _re
    raw = email.strip()
    is_phone = bool(_re.match(r"^[\+\d\s\-\(\)]+$", raw)) and len(_re.sub(r"\D", "", raw)) >= 7

    device_clean = device.strip().lower() if device else ""
    if is_phone and device_clean not in ("apple", "android"):
        renderer.console.print(
            "\n[bold]Is this phone iPhone (Apple) or Android?[/bold] "
            "[dim](Used for SMS fallback when carriers block email-to-SMS.)[/dim]"
        )
        try:
            answer = renderer.console.input("  → apple / android: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            renderer.console.print()
            raise typer.Exit(1)
        if answer in ("a", "apple", "iphone", "ios"):
            device_clean = "apple"
        elif answer in ("g", "android", "google"):
            device_clean = "android"
        else:
            renderer.error("Please answer 'apple' or 'android'.")
            raise typer.Exit(1)

    try:
        result = _sms_backend().add_contact(raw, label, device_clean if is_phone else "")
        stored  = result.get("email", "")
        display = result.get("display") or stored
        lbl     = result.get("label", "")
        dev     = result.get("device_type", "")
        if stored.startswith("phone:"):
            tag = ""
            if dev == "apple":
                tag = " [bold blue][Apple — iMessage fallback][/bold blue]"
            elif dev == "android":
                tag = " [bold green][Android — KDE Connect fallback][/bold green]"
            renderer.success(f"Added: {display}  ({lbl}){tag}")
            renderer.console.print(
                "  [dim]Matches texts from any carrier (Verizon, T-Mobile, AT&T, etc.)[/dim]"
            )
        else:
            renderer.success(f"Added: {display}  ({lbl})")
    except RuntimeError as exc:
        renderer.error(str(exc)); raise typer.Exit(1)
    except Exception as exc:
        renderer.error(str(exc))


@sms_contacts_app.command("remove")
def sms_contacts_remove(
    email: Annotated[str, typer.Argument(help="Email address or phone number to remove")],
) -> None:
    """Remove an authorized contact — they will no longer be able to control SAGE.

    Phone numbers can be passed in any common format and will be normalized
    before being sent (e.g. "+1 (408) 507-3140", "408-507-3140", "4085073140"
    all match the same contact).
    """
    from sage.main import _sms_backend
    import httpx as _httpx
    import re as _re

    # Normalize phone-shaped input to bare 10 digits so the URL is deterministic
    # and the server sees a clean canonical value.
    raw = email.strip()
    digits = _re.sub(r"\D", "", raw)
    if len(digits) == 11 and digits.startswith("1"):
        digits = digits[1:]
    target = digits if len(digits) == 10 else raw.lower()

    try:
        _sms_backend().remove_contact(target)
        renderer.success(f"Removed: {email}")
    except RuntimeError as exc:
        renderer.error(str(exc)); raise typer.Exit(1)
    except _httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            renderer.error(f"Contact not found: {email}")
        else:
            renderer.error(str(exc))
        raise typer.Exit(1)
    except Exception as exc:
        renderer.error(str(exc)); raise typer.Exit(1)


@sms_contacts_app.command("clear")
def sms_contacts_clear(
    force: Annotated[bool, typer.Option("--force", "-f", help="Skip confirmation prompt")] = False,
) -> None:
    """Remove ALL authorized contacts from this account."""
    from sage.main import _sms_backend

    try:
        be = _sms_backend()
        contacts = be.list_contacts()
    except Exception as exc:
        renderer.error(f"Could not fetch contacts: {exc}")
        raise typer.Exit(1)

    if not contacts:
        renderer.info("Contact list is already empty.")
        return

    if not force:
        renderer.console.print(f"\n[bold red]WARNING:[/bold red] This will remove [bold]{len(contacts)}[/bold] authorized contacts.")
        if not typer.confirm("Are you sure you want to clear ALL contacts?"):
            renderer.info("Cancelled.")
            return

    count = 0
    with renderer.console.status("[bold yellow]Clearing contacts...[/bold yellow]"):
        for c in contacts:
            email = c.get("email")
            if not email:
                continue
            try:
                # Backend remove_contact handles both phone: and plain email
                be.remove_contact(email)
                count += 1
            except Exception as exc:
                renderer.warning(f"Failed to remove {email}: {exc}")

    renderer.success(f"Cleared {count} contacts. Your list is now empty.")


