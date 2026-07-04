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


from sage.core.autonomous_helpers import app, config_app
@app.command()
def models(
    ollama: Annotated[bool, typer.Option("--ollama", help="Show all Ollama models available to pull")] = False,
    category: Annotated[
        str | None,
        typer.Option(
            "--category",
            "-c",
            help="Filter Ollama models by category (coding, reasoning, general, vision, small, embedding)",
        ),
    ] = None,
    search: Annotated[
        str | None,
        typer.Option("--search", "-s", help="Search Ollama catalog by keyword"),
    ] = None,
    all_models: Annotated[
        bool, typer.Option("--all", help="Show ALL models (no truncation)")
    ] = False,
    details: Annotated[
        bool,
        typer.Option(
            "--details", help="Show full descriptions with pros/cons per model"
        ),
    ] = False,
    provider: Annotated[
        str | None,
        typer.Option(
            "--provider",
            "-p",
            help="Filter by provider (ollama, openrouter, llama_cpp, gemini, groq, …)",
        ),
    ] = None,
    filter_kw: Annotated[
        str | None,
        typer.Option(
            "--filter",
            "-f",
            help="Filter models by keyword (matches id + name + description)",
        ),
    ] = None,
) -> None:
    """List available models from all configured providers.

    Examples:
      sage models                              List active models (top 45)
      sage models --all                        Show ALL models, no truncation
      sage models --details                    Show pros/cons for each model
      sage models --provider openrouter        Only OpenRouter models
      sage models -p ollama -f coder           Local Ollama models matching 'coder'
      sage models --ollama                     Show all Ollama models available to pull
      sage models --ollama -c coding           Coding-focused pullable Ollama models
      sage models --ollama -s deepseek         Search Ollama catalog
    """
    from sage.cli_core import _build_router
    if ollama or category or search:
        _show_ollama_catalog(category=category, search_query=search)
        return

    from sage.models.downloader import list_downloaded
    from sage.models.catalog import get_full_catalog
    from rich.table import Table

    cfg = load_config()
    router = _build_router(cfg)
    locally_loaded = router.list_all_models()
    downloaded_names = {name for name, _ in list_downloaded()}
    gcs_models = [m for m in get_full_catalog() if m.backend == "gguf"]

    # Apply --provider and --filter
    def _matches(m) -> bool:
        if provider and m.provider.lower() != provider.lower():
            return False
        if filter_kw:
            kw = filter_kw.lower()
            haystack = f"{m.id} {m.name} {getattr(m, 'description', '') or ''}".lower()
            if kw not in haystack:
                return False
        return True

    locally_loaded = [m for m in locally_loaded if _matches(m)]

    # ── Section 1: Locally loaded / configured models ──────────
    if locally_loaded:
        title = "Available Models"
        if provider:
            title += f" (provider={provider})"
        if filter_kw:
            title += f" (filter={filter_kw!r})"
        renderer.console.print(f"[bold]{title}[/bold]")
        if all_models:
            renderer.console.print("[dim](showing ALL — no truncation)[/dim]\n")
        else:
            renderer.console.print()
        renderer.print_model_table(
            [
                {
                    "id": m.id, "provider": m.provider, "name": m.name,
                    "local": m.local,
                    "description": getattr(m, "description", "") or "",
                    "pros": getattr(m, "pros", "") or "",
                    "cons": getattr(m, "cons", "") or "",
                }
                for m in locally_loaded
            ],
            show_all=all_models,
            show_details=details,
        )
        renderer.info(f"\nDefault: {cfg.default_model}\n")

    # ── Section 2: Downloaded but not yet registered ─────────────
    unregistered = [n for n in downloaded_names if not any(m.id == n for m in locally_loaded)]
    if unregistered:
        renderer.console.print(f"[bold]Downloaded but not registered[/bold] (run: sage train <name>):")
        for n in unregistered:
            renderer.console.print(f"  [yellow]{n}[/yellow]")
        renderer.console.print()

    # ── Section 3: Full GCS catalog ──────────────────────────────
    if gcs_models:
        tbl = Table(
            "Name", "Size", "Family", "Status",
            title=f"GCS Catalog — {len(gcs_models)} models available",
            show_header=True,
            header_style="bold cyan",
            min_width=60,
        )
        # Downloaded first, then alphabetical
        sorted_models = sorted(
            gcs_models,
            key=lambda m: (0 if m.name in downloaded_names else 1, m.display_name.lower()),
        )
        for m in sorted_models:
            if m.name in downloaded_names:
                status = "[green]downloaded ✓[/green]"
            else:
                status = "[dim]available[/dim]"
            tbl.add_row(m.name, f"{m.size_gb:.1f} GB", m.family, status)
        renderer.console.print(tbl)
        renderer.console.print()
        downloaded_count = sum(1 for m in gcs_models if m.name in downloaded_names)
        if downloaded_count:
            renderer.console.print(f"  [green]{downloaded_count} model(s) downloaded and ready.[/green]")
        renderer.console.print(
            "  [dim]sage pull <name>[/dim]   — download any model above\n"
            "  [dim]sage pull --list[/dim]   — full catalog with descriptions\n"
            "  [dim]sage pull --search <q>[/dim]  — search by name"
        )


def _try_install_ollama() -> bool:
    """Best-effort install of the Ollama runtime on the current OS.

    Returns True if Ollama is now available (already installed or successfully
    installed by us), False if the user needs to install it manually.
    """
    if shutil.which("ollama") or (
        sys.platform == "win32" and shutil.which("ollama.exe")
    ):
        return True

    renderer.info("Ollama not found — attempting to install it for you...")
    try:
        if sys.platform == "win32":
            if shutil.which("winget"):
                rc = subprocess.run(
                    ["winget", "install", "--id", "Ollama.Ollama", "-e",
                     "--accept-package-agreements", "--accept-source-agreements"],
                    check=False,
                ).returncode
                return rc == 0
        elif sys.platform == "darwin":
            if shutil.which("brew"):
                rc = subprocess.run(["brew", "install", "ollama"], check=False).returncode
                return rc == 0
        else:
            # Linux / WSL — use the official installer when curl + sh are present.
            if shutil.which("curl") and shutil.which("sh"):
                rc = subprocess.run(
                    "curl -fsSL https://ollama.com/install.sh | sh",
                    shell=True,
                    check=False,
                ).returncode
                return rc == 0
    except Exception as exc:
        logger.debug("Ollama auto-install failed: %s", exc)

    renderer.warning("Could not install Ollama automatically.")
    for line in _ollama_install_hint().splitlines():
        renderer.info(f"  {line}")
    return False


@app.command()
def install() -> None:
    """Set up Sage on a fresh machine — installs the Ollama runtime if missing
    and pulls the default models. Safe to re-run; already-installed pieces are
    skipped.

    Steps:
    - Install Ollama via the platform's package manager when needed
      (winget on Windows, brew on macOS, install.sh on Linux).
    - Download the 3 best GGUF models (~30 GB, optional offline use).
    - Pull the 8 best Ollama models for daily use.
    """
    from sage.models.catalog import DEFAULT_OLLAMA_MODELS, get_default_models

    renderer.header("Installing Sage AI — Best Models")
    renderer.info(f"  Detected platform: {platform.system()} ({platform.machine()})")
    renderer.info("")

    # Step 0: Ensure Ollama is installed (cross-platform).
    ollama_ready = _try_install_ollama()

    # Step 1: Download default GGUF models
    defaults = get_default_models()
    renderer.info(f"[1/2] Downloading {len(defaults)} best GGUF models...")
    for m in defaults:
        if is_downloaded(m):
            renderer.success(f"  {m.display_name} ({m.params}) — already downloaded")
            continue
        renderer.info(f"  Downloading {m.display_name} ({m.size_gb} GB)...")
        try:
            download_model(m, progress_callback=lambda dl, tot: None)
            register_model(m)
            renderer.success(f"  {m.display_name} — done!")
        except Exception as exc:
            renderer.error(f"  {m.display_name} — failed: {exc}")

    # Step 2: Pull default Ollama models
    renderer.info(f"\n[2/2] Pulling {len(DEFAULT_OLLAMA_MODELS)} best Ollama models...")
    if not ollama_ready:
        renderer.warning("  Ollama is not installed — skipping Ollama model pulls.")
        renderer.info("  After installing Ollama, re-run: sage install")
    else:
        for model_name in DEFAULT_OLLAMA_MODELS:
            renderer.info(f"  Pulling {model_name}...")
            try:
                result = subprocess.run(
                    [_ollama_exe(), "pull", model_name],
                    check=False,
                    timeout=_ollama_pull_subprocess_timeout(),
                )
                if result.returncode == 0:
                    renderer.success(f"  {model_name} — done!")
                else:
                    renderer.error(f"  {model_name} — ollama pull failed")
            except FileNotFoundError:
                renderer.warning("  Ollama not installed — skipping remaining models")
                for line in _ollama_install_hint().splitlines():
                    renderer.info(f"  {line}")
                break
            except subprocess.TimeoutExpired:
                renderer.error(
                    f"  {model_name} — timed out (see SAGE_OLLAMA_PULL_TIMEOUT_SEC; unset for no limit)"
                )

    # ── Wave 5+ auto-bootstrap: optional deps, RAG, prewarm, default-pick.
    # Heavy phases (finetune, full datasets) opt-in only.
    try:
        from sage.core.bootstrap import BootstrapOptions, run_bootstrap
        renderer.info("")
        renderer.info("Running post-install bootstrap (RAG, prewarm, optional deps)…")
        result = run_bootstrap(BootstrapOptions(
            pull_models=False,         # already done above
            build_llama_cpp=False,     # opt-in via `sage ext bootstrap --build-llama-cpp`
            mirror_datasets=False,     # opt-in (large network)
            finetune=False,
            quiet=True,
        ))
        for p in result.phases:
            if p.status == "ok":
                renderer.success(f"  {p.name}: {p.detail}")
            elif p.status == "failed":
                renderer.warning(f"  {p.name}: {p.detail}")
    except Exception as exc:
        renderer.warning(f"  bootstrap skipped: {exc}")

    renderer.info("")
    renderer.header("Setup Complete!")
    renderer.info("  Default model: qwen2.5-coder-7b (best local coding model)")
    renderer.info("  Run: sage chat    — to start chatting")
    renderer.info("  Run: sage ext bootstrap --finetune  — kick off project-aware fine-tune")
    renderer.info("  Run: sage models  — to see all available models")
    renderer.info("  Run: sage pull    — to download more models")
    renderer.info("")
    renderer.info("  All inference runs locally on your machine — no API keys needed.")


@app.command()
def update(
    check_only: Annotated[
        bool,
        typer.Option(
            "--check",
            help="Only check whether a newer SAGE AI CLI version is available",
        ),
    ] = False,
) -> None:
    """Update SAGE AI to the latest published CLI release."""
    from sage.cli_core import _perform_cli_update

    if not _perform_cli_update(check_only=check_only):
        raise typer.Exit(1)


@app.command("sync")
def sync_ollama_to_gcs(
    models: Annotated[
        list[str] | None,
        typer.Argument(help="Specific Ollama model names to sync (e.g. qwen3:8b). Omit to sync all local models."),
    ] = None,
    bucket: Annotated[
        str, typer.Option("--bucket", help="GCS bucket name")
    ] = "sage-ai-models",
    keep: Annotated[
        bool, typer.Option("--keep", help="Keep local Ollama copy after upload (default: delete to free disk)")
    ] = False,
    force: Annotated[
        bool, typer.Option("--force", help="Re-upload even if model is already in GCS")
    ] = False,
) -> None:
    """Sync local Ollama models to GCS — pull → extract GGUF → upload → delete.

    For each locally pulled Ollama model that is NOT yet in the GCS GGUF bucket:
      1. Locate the GGUF blob inside ~/.ollama/models/blobs/
      2. Upload it to gs://sage-ai-models/gguf/<model>.gguf
      3. Update gs://sage-ai-models/catalog.json so the website sees it
      4. Remove the local Ollama copy (unless --keep)

    Running `sage pull ollama:<name>` also calls this automatically.

    Examples:
      sage sync                     Sync every pulled Ollama model
      sage sync qwen3:8b            Sync only qwen3:8b
      sage sync llama3.2 qwen3 --keep   Sync but keep local copies
    """
    from sage.models.ollama_gcs_sync import (
        sync_model as gcs_sync,
        sync_all as gcs_sync_all,
        SyncError as GCSSyncError,
    )

    delete_after = not keep

    if models:
        results = []
        for m in models:
            renderer.info(f"\n[{m}]")
            try:
                r = gcs_sync(
                    m,
                    bucket=bucket,
                    pull_if_missing=False,
                    delete_after_upload=delete_after,
                    skip_if_exists=not force,
                    log=renderer.info,
                )
                results.append(r)
            except GCSSyncError as exc:
                renderer.error(f"  ✗ {exc}")
                results.append({"model": m, "uploaded": False, "error": str(exc)})
    else:
        results = gcs_sync_all(
            bucket=bucket,
            delete_after_upload=delete_after,
            skip_if_exists=not force,
            log=renderer.info,
        )

    uploaded = [r for r in results if r.get("uploaded")]
    skipped  = [r for r in results if r.get("skipped")]
    failed   = [r for r in results if r.get("error")]

    renderer.console.print()
    renderer.success(f"Sync complete: {len(uploaded)} uploaded, {len(skipped)} already in GCS, {len(failed)} failed.")
    if uploaded:
        renderer.info("Models will appear on the SAGE website within ~1 hour (catalog cache TTL).")
    if failed:
        for r in failed:
            renderer.error(f"  ✗ {r['model']}: {r.get('error', 'unknown error')}")


@app.command("sync-catalog")
def sync_catalog(
    force: Annotated[
        bool,
        typer.Option("--force", "-f", help="Bypass the local 1-hour cache"),
    ] = False,
) -> None:
    """Refresh the local model catalog from the canonical GCS catalog.json.

    Sage already does this in the background on every startup (1-hour cache).
    Use this command to force an immediate refresh — e.g. after a new model
    just dropped on the Ollama library or a new GGUF was uploaded to the
    sage-ai-models bucket.
    """
    from sage.models.catalog import refresh_catalog_from_remote

    renderer.info("Refreshing model catalog from GCS...")
    added = refresh_catalog_from_remote(background=False, force=force)

    if added > 0:
        renderer.success(f"Added {added} new model(s) to the local catalog.")
    else:
        renderer.info("Catalog is already up to date.")
    renderer.info(f"Total models available: {len(MODEL_CATALOG)}")


@app.command()
def pull(
    model_name: Annotated[
        str | None,
        typer.Argument(help="Model to download from GCS (e.g. 'qwen3-8b', 'qwen2.5-coder-3b')"),
    ] = None,
    list_available: Annotated[
        bool, typer.Option("--list", "-l", help="List all downloadable GGUF models")
    ] = False,
    search: Annotated[
        str | None, typer.Option("--search", "-s", help="Search catalog by keyword")
    ] = None,
    recommended: Annotated[
        bool,
        typer.Option("--recommended", "-r", help="Show recommended starter models"),
    ] = False,
    all_models: Annotated[
        bool,
        typer.Option("--all", help="Download all GGUF models from GCS (~30 GB total)"),
    ] = False,
    all_gguf: Annotated[
        bool,
        typer.Option("--all-gguf", help="Download all GGUF models from GCS"),
    ] = False,
) -> None:
    """Download a GGUF model from the GCS bucket — no API key, no Ollama needed.

    Models are downloaded as GGUF files directly from Google Cloud Storage
    and run locally via llama.cpp. Works on Windows, Linux, and macOS.

    Examples:
      sage pull --list                  List all downloadable models
      sage pull qwen3-8b                Download Qwen 3 8B (5 GB)
      sage pull qwen2.5-coder-3b        Download Qwen 2.5 Coder 3B (1.8 GB)
      sage pull llama3.2-3b             Download Llama 3.2 3B (1.9 GB)
      sage pull --search code           Search for coding models
      sage pull --recommended           Show recommended starter models
      sage pull --all                   Download all GGUF models (~30 GB)
    """
    from rich.progress import (
        BarColumn,
        DownloadColumn,
        Progress,
        TimeRemainingColumn,
        TransferSpeedColumn,
    )

    # ── Batch download modes ────────────────────────────────
    # `sage pull` is GCS-GGUF-only (Ollama was dropped in 92c79f9). `--all` /
    # `--all-gguf` still trigger a bulk download of every GGUF in the catalog;
    # individual `sage pull ollama:<name>` invocations are redirected to the
    # GGUF equivalent further down.
    if all_models or all_gguf:
        gguf_models = [m for m in MODEL_CATALOG if m.backend == "gguf"]
        total_gb = sum(m.size_gb for m in gguf_models)
        renderer.info(
            f"Downloading {len(gguf_models)} GGUF models (~{total_gb:.0f} GB total)..."
        )
        for i, m in enumerate(gguf_models, 1):
            if is_downloaded(m):
                renderer.info(f"  [{i}/{len(gguf_models)}] {m.name} — already downloaded")
                continue
            renderer.info(
                f"  [{i}/{len(gguf_models)}] Downloading {m.name} ({m.size_gb:.1f} GB)..."
            )
            try:
                with Progress(
                    "[progress.description]{task.description}",
                    BarColumn(),
                    DownloadColumn(),
                    TransferSpeedColumn(),
                    TimeRemainingColumn(),
                ) as prog:
                    task_id = prog.add_task(m.display_name, total=None)

                    def _cb(downloaded: int, total: int | None) -> None:
                        if total:
                            prog.update(task_id, completed=downloaded, total=total)

                    download_model(m, progress_callback=_cb)
                renderer.success(f"  {m.name} downloaded")
            except Exception as exc:
                renderer.error(f"  {m.name} failed: {exc}")

        renderer.success("\nBatch download complete!")
        return

    if list_available or (model_name is None and not search and not recommended):
        # Show full catalog
        entries = []
        for m in MODEL_CATALOG:
            if m.backend == "ollama":
                status = ""  # Ollama models checked at runtime
                size_str = m.params if m.params else "cloud"
            else:
                status = "[green]downloaded[/green]" if is_downloaded(m) else ""
                size_str = f"{m.size_gb:.1f} GB"
            entries.append(
                {
                    "name": m.name,
                    "size": size_str,
                    "params": m.params,
                    "family": m.family,
                    "description": m.description,
                    "status": status,
                }
            )
        renderer.print_catalog_table(entries)
        gguf_count = len([m for m in MODEL_CATALOG if m.backend == "gguf"])
        ollama_count = len([m for m in MODEL_CATALOG if m.backend == "ollama"])
        renderer.info(
            f"\n{len(MODEL_CATALOG)} models ({gguf_count} GGUF + {ollama_count} Ollama). "
            "Download with: sage pull <name>"
        )
        renderer.info("Recommended: sage pull qwen2.5-coder-3b (GGUF) or sage pull qwen3 (Ollama)")
        return

    if recommended:
        recs = get_recommended_models()
        entries = []
        for m in recs:
            status = "[green]downloaded[/green]" if is_downloaded(m) else ""
            entries.append(
                {
                    "name": m.name,
                    "size": f"{m.size_gb:.1f} GB",
                    "params": m.params,
                    "family": m.family,
                    "description": m.description,
                    "status": status,
                }
            )
        renderer.print_catalog_table(entries)
        return

    if search:
        results = search_catalog(search)
        if not results:
            renderer.warning(f"No models matching '{search}'")
            raise typer.Exit(1)
        entries = []
        for m in results:
            status = "[green]downloaded[/green]" if is_downloaded(m) else ""
            entries.append(
                {
                    "name": m.name,
                    "size": f"{m.size_gb:.1f} GB",
                    "params": m.params,
                    "family": m.family,
                    "description": m.description,
                    "status": status,
                }
            )
        renderer.print_catalog_table(entries)
        return

    # Download a specific model
    # Try exact match, then ollama: prefix, then a sync catalog refresh.
    cat_model = _resolve_catalog_model(model_name)
    if not cat_model:
        # Try fuzzy search
        results = search_catalog(model_name)
        if results:
            renderer.warning(f"Model '{model_name}' not found. Did you mean:")
            for m in results[:5]:
                if m.backend == "ollama":
                    renderer.info(f"  sage pull {m.name}  — {m.display_name} (Ollama)")
                else:
                    renderer.info(f"  sage pull {m.name}  — {m.display_name} ({m.size_gb:.1f} GB)")
        else:
            renderer.error(
                f"Model '{model_name}' not found. Run 'sage pull --list' to see available models."
            )
        raise typer.Exit(1)

    # ── Ollama model: pull → extract GGUF blob → upload to GCS → optional delete ──
    if cat_model.backend == "ollama":
        from sage.models.ollama_gcs_sync import sync_model as gcs_sync, SyncError as GCSSyncError

        ollama_name = cat_model.name.removeprefix("ollama:")
        renderer.info(
            f"Pulling {cat_model.display_name} from Ollama, uploading GGUF to GCS…\n"
            f"  This downloads the model locally, extracts the GGUF weights,\n"
            f"  uploads them to gs://sage-ai-models/gguf/, and updates catalog.json.\n"
        )

        try:
            result = gcs_sync(
                ollama_name,
                bucket="sage-ai-models",
                pull_if_missing=True,
                delete_after_upload=True,  # free local disk after verified upload
                skip_if_exists=False,      # always re-sync on explicit pull
                log=renderer.info,
            )
        except GCSSyncError as exc:
            renderer.error(f"Sync failed: {exc}")
            raise typer.Exit(1)

        if result.get("uploaded"):
            renderer.success(
                f"{cat_model.display_name} uploaded to GCS.\n"
                f"  It will appear in 'sage pull --list' and on the SAGE website within ~1 hour.\n"
                f"  Local Ollama copy removed to free disk space."
            )
        elif result.get("skipped"):
            renderer.info(f"{cat_model.display_name} is already in GCS.")
        raise typer.Exit(0)

    # ── GGUF model: download from HuggingFace ─────────────
    if is_downloaded(cat_model):
        renderer.success(f"{cat_model.display_name} is already downloaded.")
        renderer.info(f"Run with: sage run --model {cat_model.name}")
        return

    renderer.info(f"Downloading {cat_model.display_name} ({cat_model.size_gb:.1f} GB)...")
    renderer.info(f"From: {cat_model.url[:80]}...")
    renderer.console.print()

    with Progress(
        "[progress.description]{task.description}",
        BarColumn(bar_width=40),
        "[progress.percentage]{task.percentage:>3.0f}%",
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        console=renderer.console,
    ) as progress:
        task = progress.add_task(f"Downloading {cat_model.name}", total=None)

        def on_progress(downloaded: int, total: int) -> None:
            progress.update(task, total=total, completed=downloaded)

        try:
            path = download_model(cat_model, progress_callback=on_progress)
        except Exception as exc:
            renderer.error(f"Download failed: {exc}")
            raise typer.Exit(2)

    # Auto-register in config
    register_model(cat_model)
    renderer.print_download_complete(
        cat_model.display_name,
        str(path),
        cat_model.size_gb,
    )


# ── Sage system prompt baked into trained Ollama variants ────
# ── System prompt with few-shot examples to close the cloud/local gap ───────
# Few-shot examples are the highest-impact single addition for small models:
# they demonstrate the exact behaviour expected rather than just describing it.
def _ollama_exe() -> str:
    """Return the ollama executable name for the current platform.

    On Windows, Ollama installs to %LOCALAPPDATA%\\Programs\\Ollama\\ollama.exe.
    shutil.which() finds it as long as that directory is in PATH (the installer
    adds it automatically).  Fallback to bare 'ollama' so subprocess still
    tries to find it via PATH resolution.
    """
    if sys.platform == "win32":
        found = shutil.which("ollama.exe") or shutil.which("ollama")
        return found or "ollama"
    return shutil.which("ollama") or "ollama"


def _ollama_install_hint() -> str:
    """Platform-aware install instructions for Ollama.

    SAGE's default model is local (Ollama), so when it isn't installed we tell
    the user exactly how to fix it on their OS instead of just printing
    'ollama serve' (which doesn't help if the binary isn't there yet).
    """
    if sys.platform == "win32":
        return (
            "Install Ollama:\n"
            "  • Recommended: winget install Ollama.Ollama\n"
            "  • Or download the installer from https://ollama.com/download/windows\n"
            "After install, open a new terminal and run: ollama serve"
        )
    if sys.platform == "darwin":
        return (
            "Install Ollama:\n"
            "  • Recommended: brew install ollama\n"
            "  • Or download from https://ollama.com/download/mac\n"
            "Then run: ollama serve"
        )
    # Linux + everything else
    return (
        "Install Ollama:\n"
        "  • One-liner: curl -fsSL https://ollama.com/install.sh | sh\n"
        "  • Or see https://ollama.com/download/linux\n"
        "Then run: ollama serve"
    )


_SAGE_TRAIN_SYSTEM_PROMPT = """\
You are SAGE, an expert full-stack coding and DevOps assistant. Think step by
step before answering. When given a problem, identify root causes and execute
the complete fix — do not stop at analysis.

## Core rules
1. NEVER invent file paths, function names, or API details you have not read.
2. If you have not read a file, say "I need to read that first." Then use READ:.
3. Do NOT write FILE: blocks unless the user says: fix / implement / write / change / create.
4. Always verify with READ:/SEARCH: before making claims about code.
5. Vite/React frontend: ALWAYS use import.meta.env.VITE_* — NEVER process.env.VITE_*.
6. When writing code: output COMPLETE file contents in FILE: blocks, never partial diffs.
7. When a task requires multiple steps (secrets → deploy → verify), do ALL steps.

## Commands
READ: path/to/file          — read a file before discussing it
SEARCH: pattern             — search the codebase
RUN: shell command          — run a command and use its output
FILE: path/to/file.ext      — write a complete file (only when asked to implement)
```lang
complete contents
```

## Firebase config → environment variable mapping
When a user provides a Firebase config object (JS or JSON format), map each
field to the correct VITE_ environment variable name:

  apiKey            → VITE_FIREBASE_API_KEY
  authDomain        → VITE_FIREBASE_AUTH_DOMAIN
  projectId         → VITE_FIREBASE_PROJECT_ID
  storageBucket     → VITE_FIREBASE_STORAGE_BUCKET
  messagingSenderId → VITE_FIREBASE_MESSAGING_SENDER_ID
  appId             → VITE_FIREBASE_APP_ID
  measurementId     → VITE_FIREBASE_MEASUREMENT_ID

Example input the user might paste:
  const firebaseConfig = {
    apiKey: "AIzaSyXXX",
    authDomain: "myapp.firebaseapp.com",
    ...
  };

Your response: extract each value and map it, then proceed with the fix.

## Production deployment pipeline (this project)
When the user says "fix the website", "upload env vars", or "deploy", the
full sequence is:

  Step 1 — Set GitHub Actions secrets (so CI/CD builds with the correct keys):
    RUN: gh secret set VITE_FIREBASE_API_KEY --body "VALUE"
    RUN: gh secret set VITE_FIREBASE_AUTH_DOMAIN --body "VALUE"
    ... (one command per variable)

  Step 2 — Set Google Cloud Run environment variables (runtime env):
    RUN: gcloud run services update SERVICE_NAME --region us-central1 \
           --set-env-vars "KEY1=VAL1,KEY2=VAL2,..."

  Step 3 — Trigger a new deployment so the new build bakes vars into bundle:
    RUN: gh workflow run ci.yml --ref main
    OR:  git commit --allow-empty -m "chore: trigger deploy" && git push

  Step 4 — Verify the deployment succeeded:
    RUN: gh run list --limit 3
    RUN: curl -s https://YOUR_SERVICE_URL/health

CRITICAL: Vite inlines VITE_* vars at BUILD TIME. Setting them only on Cloud
Run at runtime does NOT fix the browser bundle. You must trigger a new build.

## Firebase Auth domain errors
If the error is "auth/unauthorized-domain", the Cloud Run domain is not in
Firebase's authorized domains list. Fix it with:
  RUN: TOKEN=$(gcloud auth print-access-token --project=PROJECT_ID)
  RUN: curl -s -X PATCH \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -H "x-goog-user-project: PROJECT_ID" \
    -d '{"authorizedDomains":["localhost","YOUR_DOMAIN.run.app"]}' \
    "https://identitytoolkit.googleapis.com/admin/v2/projects/PROJECT_ID/config?updateMask=authorizedDomains"

## Reading the current project config
Before fixing any deployment issue, read these files to understand the project:
  READ: .github/workflows/deploy.yml  OR  ai-platform/.github/workflows/deploy.yml
  READ: frontend/.env.example         (shows expected variable names)
  RUN: gh secret list                 (shows which secrets are already set)
  RUN: gcloud run services describe SERVICE --region us-central1 --format="value(status.url)"

## Thinking pattern for "fix the website" tasks
1. What is the error? (read logs, error messages)
2. What is missing? (secrets not set? build not triggered? domain not authorized?)
3. What values do I have? (user provided config? existing .env?)
4. Map values → correct variable names
5. Set secrets (GitHub + Cloud Run)
6. Trigger build and verify

## Examples of correct behaviour

### Example 1 — Firebase config pasted by user, not mapped
User: Fix the website auth. Here's the Firebase config:
  const firebaseConfig = {
    apiKey: "AIzaSyABC123",
    authDomain: "myapp.firebaseapp.com",
    projectId: "myapp-123",
    appId: "1:999:web:abc"
  };
Assistant:
I can see the Firebase config. Let me map the values and set them as secrets.
RUN: gh secret set VITE_FIREBASE_API_KEY --body "AIzaSyABC123"
RUN: gh secret set VITE_FIREBASE_AUTH_DOMAIN --body "myapp.firebaseapp.com"
RUN: gh secret set VITE_FIREBASE_PROJECT_ID --body "myapp-123"
RUN: gh secret set VITE_FIREBASE_APP_ID --body "1:999:web:abc"
Now trigger a new build so Vite bakes these into the bundle:
RUN: gh workflow run ci.yml --ref main

### Example 2 — analysis (no FILE: needed)
User: What does is_downloaded do?
Assistant: I need to read that file first.
READ: sage/models/downloader.py
[reads file]
`is_downloaded` checks whether a GGUF file exists on disk with size > 0.

### Example 3 — code fix
User: Fix the bug where process.env is used instead of import.meta.env in auth.js
Assistant:
READ: frontend/src/firebase/auth.js
[reads file — sees process.env.VITE_FIREBASE_API_KEY on line 5]
The bug is on line 5. Fixing:
FILE: frontend/src/firebase/auth.js
```javascript
// complete corrected file using import.meta.env.VITE_FIREBASE_API_KEY
```

### Example 4 — multi-step production fix
User: Upload all the .env variables to GitHub and Google Cloud Run
Assistant:
Let me read the current .env and workflow files first.
READ: frontend/.env
READ: .github/workflows/deploy.yml
[reads both — sees VITE_FIREBASE_* values and SERVICE_NAME]
Setting GitHub secrets:
RUN: gh secret set VITE_FIREBASE_API_KEY --body "AIzaSyXXX"
RUN: gh secret set VITE_FIREBASE_AUTH_DOMAIN --body "myapp.firebaseapp.com"
[... all secrets ...]
Setting Cloud Run environment:
RUN: gcloud run services update sage-ai --region us-central1 --set-env-vars "VITE_FIREBASE_API_KEY=AIzaSyXXX,..."
Triggering new build:
RUN: gh workflow run ci.yml --ref main
Verifying:
RUN: gh run list --limit 3

## Platform-aware command generation
Before running ANY shell command, confirm the OS from the injected
"Runtime environment" section in your context. Then use the RIGHT commands:

Windows (win32):
  List files:    dir
  Read file:     type filename.txt
  Find text:     findstr "pattern" file
  Python:        py or python  (NEVER python3)
  Copy:          copy src dst
  Delete:        del filename
  Make dir:      mkdir dirname
  Find program:  where program
  Environment:   %VARIABLE_NAME%

macOS (darwin):
  List files:    ls -la
  Read file:     cat filename
  Find text:     grep -r "pattern" .
  Python:        python3  (NEVER bare python)
  Package mgr:   brew install <pkg>
  Environment:   $VARIABLE_NAME

Linux:
  List files:    ls -la
  Read file:     cat filename
  Find text:     grep -r "pattern" .
  Python:        python3  (NEVER bare python)
  Package mgr:   apt/dnf/yum/apk install <pkg> (whichever is available)
  Environment:   $VARIABLE_NAME

NEVER use Unix commands on Windows. NEVER use cmd.exe commands on macOS/Linux.
If unsure of the platform, run: RUN: python -c "import sys; print(sys.platform)"
"""

# ── Cross-platform hardware detection ────────────────────────────────────────

def _detect_ram_gb() -> float:
    """Return total system RAM in GB — works on macOS, Linux, and Windows."""
    try:
        import psutil
        return psutil.virtual_memory().total / 1e9
    except ImportError:
        pass
    try:
        if sys.platform == "darwin":
            import subprocess as _sp
            out = _sp.check_output(["sysctl", "-n", "hw.memsize"], timeout=3)
            return int(out.strip()) / 1e9
        if sys.platform.startswith("linux"):
            with open("/proc/meminfo") as f:
                for line in f:
                    if line.startswith("MemTotal"):
                        return int(line.split()[1]) / 1e6
        if sys.platform == "win32":
            import ctypes
            class _MEMSTATUS(ctypes.Structure):
                _fields_ = [("dwLength", ctypes.c_ulong), ("dwMemoryLoad", ctypes.c_ulong),
                             ("ullTotalPhys", ctypes.c_ulonglong), ("ullAvailPhys", ctypes.c_ulonglong),
                             *[(f"_x{i}", ctypes.c_ulonglong) for i in range(6)]]
            ms = _MEMSTATUS()
            ms.dwLength = ctypes.sizeof(_MEMSTATUS)
            ctypes.windll.kernel32.GlobalMemoryStatusEx(ctypes.byref(ms))
            return ms.ullTotalPhys / 1e9
    except Exception:
        pass
    return 8.0  # safe conservative default


def _detect_performance_cores() -> int:
    """Return the number of physical performance cores — works cross-platform."""
    # Apple Silicon: use perflevel0 (P-cores only)
    if sys.platform == "darwin":
        try:
            import subprocess as _sp
            out = _sp.check_output(
                ["sysctl", "-n", "hw.perflevel0.logicalcpu"], timeout=3
            )
            n = int(out.strip())
            if n > 0:
                return n
        except Exception:
            pass
    # Linux: try to read physical core count from /proc/cpuinfo
    if sys.platform.startswith("linux"):
        try:
            cores: set[str] = set()
            with open("/proc/cpuinfo") as f:
                for line in f:
                    if line.startswith("core id"):
                        cores.add(line.split(":")[1].strip())
            if cores:
                return len(cores)
        except Exception:
            pass
    # Windows and fallback: half of logical CPUs (approximates physical cores)
    logical = os.cpu_count() or 4
    return max(1, logical // 2)


def _detect_has_gpu() -> bool:
    """Return True if a hardware GPU is available (Metal, CUDA, or ROCm).

    Uses hardware-level detection so it works even when Python runs under
    Rosetta emulation (Anaconda x86_64 on Apple Silicon reports x86_64 for
    platform.machine() but the GPU is still present and available).
    """
    if sys.platform == "darwin":
        # Check actual hardware for Apple Silicon — works even under Rosetta
        try:
            out = subprocess.check_output(
                ["sysctl", "-n", "hw.optional.arm64"], timeout=3,
                stderr=subprocess.DEVNULL,
            ).strip()
            if out == b"1":
                return True
        except Exception:
            pass
        # Older Intel Macs with Metal support (Metal 1+)
        try:
            out = subprocess.check_output(
                ["system_profiler", "SPDisplaysDataType"], timeout=5,
                stderr=subprocess.DEVNULL,
            ).decode(errors="replace")
            if "Metal" in out:
                return True
        except Exception:
            pass
    # NVIDIA CUDA (Linux, Windows)
    try:
        subprocess.run(["nvidia-smi"], capture_output=True, timeout=5, check=False)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    # AMD ROCm (Linux)
    try:
        subprocess.run(["rocm-smi"], capture_output=True, timeout=5, check=False)
        return True
    except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
        pass
    return False


# ── Model-size-aware parameter profiles ──────────────────────────────────────
#
# num_gpu:    Force all transformer layers onto the GPU. 99 = "all layers".
#             Works for Metal (Apple), CUDA (NVIDIA), and ROCm (AMD).
#             Omitted when no GPU is detected — CPU inference is the fallback.
#
# num_thread: CPU threads used for tokenisation and sampling. Matched to
#             physical performance cores; excess hyperthreads add contention.
#
# num_batch:  Prompt-processing batch size. Larger = faster prefill at the
#             cost of peak RAM. Scaled to available system RAM.
#
# num_ctx:    Context window. Longer = better reasoning, more RAM. Capped
#             so the model fits within available RAM headroom.
#
# mirostat 2: Adaptive sampler — keeps quality stable over long responses.
def _model_params_for_size(size_gb: float) -> dict[str, str]:
    """Return hardware-optimised Modelfile PARAMETER lines based on model + system."""
    ram_gb = _detect_ram_gb()
    threads = _detect_performance_cores()
    has_gpu = _detect_has_gpu()

    # Batch size: larger RAM → bigger prefill batches → faster first-token time
    if ram_gb >= 32:
        batch = "512"
    elif ram_gb >= 16:
        batch = "256"
    else:
        batch = "128"

    # Base params shared across all size classes
    base: dict[str, str] = {
        "num_thread": str(threads),
        "num_batch": batch,
        "mirostat": "2",
    }
    if has_gpu:
        base["num_gpu"] = "99"  # push all layers to GPU when one is available

    # Model-size-specific tuning
    headroom = ram_gb * 0.6  # leave 40% for OS and other apps
    if size_gb >= 30:  # large: qwen3-coder-next, llama3.3
        # May exceed RAM — keep context small to reduce swapping
        ctx = "8192" if size_gb > headroom else "16384"
        return {**base,
                "temperature": "0.1", "top_k": "20", "top_p": "0.9",
                "repeat_penalty": "1.05", "num_ctx": ctx,
                "mirostat_eta": "0.1", "mirostat_tau": "4.0"}
    elif size_gb >= 7:  # medium: gemma4, llama3.1-8b
        ctx = "16384" if size_gb < headroom else "8192"
        return {**base,
                "temperature": "0.1", "top_k": "10", "top_p": "0.9",
                "repeat_penalty": "1.1", "num_ctx": ctx,
                "mirostat_eta": "0.1", "mirostat_tau": "5.0"}
    else:  # small: llama3.2, qwen2.5-coder-*
        return {**base,
                "temperature": "0.1", "top_k": "10", "top_p": "0.85",
                "repeat_penalty": "1.15", "num_ctx": "8192",
                "mirostat_eta": "0.2", "mirostat_tau": "5.0"}


def _get_model_size_gb(base_name: str) -> float:
    """Estimate model size in GB from Ollama metadata."""
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=3.0)
        if r.status_code == 200:
            for m in r.json().get("models", []):
                name = (m.get("name") or "").split(":")[0]
                if name == base_name:
                    size_bytes = m.get("size", 0)
                    return size_bytes / (1024 ** 3)
    except Exception:
        pass
    return 2.0  # safe default — use small-model params


def _train_ollama_model(base_name: str, force: bool = False) -> bool:
    """Train an Ollama model in-place by recreating it with the sage Modelfile.

    Updates the model under its original name — no renaming, no new variants.
    Bakes in: model-size parameters, few-shot examples, platform-specific
    command guidance for the machine this is running on so the model always
    generates correct commands for the current OS.
    Re-running is idempotent: the model is always overwritten with the latest config.
    """
    from sage.config import load_config
    from sage.core.prompts import platform_context_section
    from sage.core.speculative import speculative_for_ollama

    size_gb = _get_model_size_gb(base_name)
    params = _model_params_for_size(size_gb)
    param_lines = "\n".join(f"PARAMETER {k} {v}" for k, v in params.items())

    # Speculative decoding hint (C10b): when cfg.speculative_draft_model is
    # configured for Ollama, bake `PARAMETER draft_model <name>` into the
    # Modelfile. Ollama uses this for speculative decoding at runtime —
    # the user gets a 2-3x speedup with no further wiring required.
    try:
        draft = speculative_for_ollama(load_config())
    except Exception:
        draft = None
    if draft:
        param_lines += f"\nPARAMETER draft_model {draft}"

    # Combine the static training prompt with the current platform context.
    # This makes the trained model immediately correct for this machine's OS.
    combined_prompt = _SAGE_TRAIN_SYSTEM_PROMPT.rstrip() + "\n" + platform_context_section().strip()

    modelfile_content = (
        f"FROM {base_name}\n\n"
        f"{param_lines}\n\n"
        f'SYSTEM """{combined_prompt}"""\n'
    )

    modelfile_dir = Path.home() / ".sage" / "modelfiles"
    modelfile_dir.mkdir(parents=True, exist_ok=True)
    modelfile_path = modelfile_dir / f"{base_name}.modelfile"
    modelfile_path.write_text(modelfile_content)

    try:
        result = subprocess.run(
            [_ollama_exe(), "create", base_name, "-f", str(modelfile_path)],
            capture_output=True, text=True, timeout=120,
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _get_pulled_ollama_names() -> list[str]:
    """Return base names of all locally-pulled Ollama models."""
    try:
        import httpx
        r = httpx.get("http://127.0.0.1:11434/api/tags", timeout=3.0)
        if r.status_code != 200:
            return []
        models = r.json().get("models") or []
        return [m["name"].split(":")[0] for m in models if isinstance(m, dict) and m.get("name")]
    except Exception:
        return []


def _resolve_catalog_model(model_id: str):
    """Resolve a user-typed model name to a CatalogModel.

    Catalog refresh from GCS happens on a background thread at startup, so
    a fast command (`sage train gemma4`) can race past it before the new
    entry lands in CATALOG_BY_NAME. We also accept a bare name when only
    the ``ollama:`` variant is registered, mirroring `sage pull`'s
    behaviour.

    Order:
      1. Exact match in the in-memory catalog.
      2. Synchronous refresh from gs://sage-ai-models/catalog.json and
         retry the exact lookup. The GCS catalog often has a bare GGUF
         entry (``filename: gemma4.gguf``) that the hardcoded catalog
         lacks — that's the one local files match against, so we must
         try this before falling back to ``ollama:`` which has an empty
         filename.
      3. ``ollama:<name>`` fallback (used by `sage pull`'s ollama path).
    """
    found = CATALOG_BY_NAME.get(model_id)
    if found is not None:
        return found

    try:
        from sage.models.catalog import refresh_catalog_from_remote
        refresh_catalog_from_remote(background=False)
    except Exception:
        pass

    found = CATALOG_BY_NAME.get(model_id)
    if found is not None:
        return found

    if not model_id.startswith("ollama:"):
        return CATALOG_BY_NAME.get(f"ollama:{model_id}")
    return None


@app.command("train-all")
def train_all(
    limit: Annotated[
        int | None,
        typer.Option("--limit", "-n", help="Cap number of models to train"),
    ] = None,
    force: Annotated[
        bool,
        typer.Option("--force", help="Re-train even if already trained"),
    ] = False,
) -> None:
    """Register all downloaded GGUF models for sage usage."""
    ok = 0
    skipped = 0
    failed: list[str] = []

    # ── GGUF: register any downloaded files ───────────────────
    downloaded_gguf = [m for m in MODEL_CATALOG if m.backend == "gguf" and is_downloaded(m)]
    if downloaded_gguf:
        renderer.console.print(f"\n[bold]Registering {len(downloaded_gguf)} GGUF model(s)[/bold]...")
        for model in downloaded_gguf:
            cfg = load_config()
            if model.name in cfg.models and not force:
                skipped += 1
                continue
            try:
                register_model(model)
                ok += 1
                renderer.success(f"  Registered: {model.display_name}")
            except Exception as exc:
                failed.append(f"{model.name}: {exc}")

    renderer.console.print()
    renderer.console.print(
        f"Done. [green]trained={ok}[/green] skipped={skipped} "
        f"{'[red]' if failed else ''}failed={len(failed)}{'[/red]' if failed else ''}"
    )
    if failed:
        for item in failed:
            renderer.warning(item)
        raise typer.Exit(2)


@app.command("train")
def train_model(
    model_id: Annotated[
        str,
        typer.Argument(help="GGUF model to register (e.g. qwen3-8b, qwen2.5-coder-3b)"),
    ],
    force: Annotated[
        bool,
        typer.Option("--force", help="Re-register even if already registered"),
    ] = False,
) -> None:
    """Register a downloaded GGUF model for sage usage.

    Download models first with: sage pull <name>
    """
    cat_model = _resolve_catalog_model(model_id)

    if cat_model is None:
        renderer.error(f"Unknown model: {model_id!r}. Run: sage pull --list to see available models.")
        raise typer.Exit(1)

    # ── GGUF: register in config ─────────────────────────────
    if not is_downloaded(cat_model):
        renderer.error(
            f"Model {model_id!r} is not downloaded. "
            "Download it first with: sage pull <model-name>"
        )
        raise typer.Exit(1)
    cfg = load_config()
    register_key = cat_model.name
    if register_key in cfg.models and not force:
        renderer.console.print(f"Already registered: {register_key} (use --force to re-register)")
        return
    try:
        register_model(cat_model)
        renderer.success(f"Registered: {cat_model.display_name}")
    except Exception as exc:
        renderer.error(f"Failed to register {model_id}: {exc}")
        raise typer.Exit(1)


@app.command("use")
def use_model(
    model_id: Annotated[
        str,
        typer.Argument(
            help="Model name to use (e.g. qwen3-8b, qwen2.5-coder-3b, or llama_cpp:qwen2.5-coder-3b)"
        ),
    ],
) -> None:
    """Set the default GGUF model Sage will use.

    Download models first with: sage pull <name>
    """
    from sage.cli_core import _set_last_used_model
    cfg = load_config()

    # Resolve bare name to llama_cpp: prefix
    if ":" not in model_id:
        if model_id in cfg.models:
            resolved = f"llama_cpp:{model_id}"
        else:
            gguf_model = _resolve_catalog_model(model_id)
            if gguf_model and gguf_model.backend == "gguf" and is_downloaded(gguf_model):
                resolved = f"llama_cpp:{gguf_model.name}"
            else:
                renderer.error(
                    f"Model {model_id!r} not found or not downloaded. "
                    "Run: sage pull --list  to see available models.\n"
                    "Download with: sage pull <name>"
                )
                raise typer.Exit(1)
    else:
        resolved = model_id

    cfg.default_model = resolved
    save_config(cfg)
    _set_last_used_model(Path.cwd(), resolved)
    renderer.success(f"Default model set to: {resolved}")


@app.command("rm")
def remove_model(
    model_names: Annotated[list[str], typer.Argument(help="Model name(s) to remove (space-separated)")],
) -> None:
    """Remove one or more downloaded GGUF models and free disk space.

    Examples:
      sage rm qwen2.5-coder-3b
      sage rm llama_cpp:qwen2.5-coder-3b llama_cpp:tinyllama-1.1b
    """
    ok = 0
    failed: list[str] = []

    for raw in model_names:
        name = raw.removeprefix("llama_cpp:").split(":")[0]
        if delete_model(name) or delete_model(raw):
            renderer.success(f"Removed: {raw}")
            ok += 1
        else:
            renderer.warning(f"Not found: {raw}")
            failed.append(raw)

    renderer.console.print()
    renderer.console.print(f"Done. removed={ok} not_found={len(failed)}")
    if failed:
        raise typer.Exit(1)


# ── Config subcommands ──────────────────────────────────────


@config_app.command("show")
def config_show() -> None:
    """Show current configuration."""
    cfg = load_config()
    # Mask API keys for display
    display = cfg.to_dict()
    for key in display.get("api_keys", {}):
        val = display["api_keys"][key]
        if val and len(val) > 8:
            display["api_keys"][key] = val[:4] + "..." + val[-4:]
    renderer.print_config(display)


@config_app.command("set")
def config_set(
    key: Annotated[str, typer.Argument(help="Config key (e.g. api_keys.gemini, default_model)")],
    value: Annotated[str, typer.Argument(help="Value to set")],
) -> None:
    """Set a configuration value."""
    try:
        set_config_value(key, value)
        renderer.success(f"Set {key}")
    except KeyError as exc:
        renderer.error(str(exc))
        raise typer.Exit(1)


@config_app.command("get")
def config_get(
    key: Annotated[str, typer.Argument(help="Config key to read")],
) -> None:
    """Get a configuration value."""
    try:
        val = get_config_value(key)
        renderer.console.print(val)
    except KeyError as exc:
        renderer.error(str(exc))
        raise typer.Exit(1)


@config_app.command("init")
def config_init() -> None:
    """Create default config file at ~/.sage/config.json."""
    cfg = SageConfig()
    save_config(cfg)
    renderer.success("Config created at ~/.sage/config.json")
    renderer.console.print()
    renderer.info("Quick start (no setup needed):")
    renderer.info(
        "  sage run                            # Start coding with pre-trained free models"
    )
    renderer.info("  sage models                         # See all available providers/models")
    renderer.console.print()
    renderer.info("Optional: add your own keys/providers:")
    renderer.info("  sage config set api_keys.gemini    YOUR_KEY  # Google AI Studio")
    renderer.info("  sage config set api_keys.groq      YOUR_KEY  # console.groq.com")
    renderer.info("  sage config set api_keys.cerebras  YOUR_KEY  # cloud.cerebras.ai")
    renderer.info("Optional local offline model: sage pull qwen2.5-coder-3b")


# ── Version callback ────────────────────────────────────────


def _version_callback(value: bool) -> None:
    if value:
        renderer.console.print(f"sage {__version__}")
        raise typer.Exit()


@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Annotated[
        bool | None,
        typer.Option("--version", "-v", callback=_version_callback, is_eager=True),
    ] = None,
) -> None:
    """Sage — local-first AI coding assistant."""
    from sage.cli_core import run
    _stdout_encoding = getattr(sys.stdout, "encoding", None) or ""
    _encoding_is_modern = _stdout_encoding.lower().replace("-", "") in ("utf8", "utf-8", "utf16", "utf32", "cp65001")
    if (
        os.environ.get("NO_COLOR")
        or os.environ.get("SAGE_NO_COLOR")
        or os.environ.get("SAGE_ASCII")
        or os.environ.get("TERM") in (None, "", "dumb")
        or not sys.stdout.isatty()
        or not _encoding_is_modern
    ):
        renderer.set_no_color(True)
    # ── Auth gate ──────────────────────────────────────────────────────────
    # Exempt: login/logout/whoami always allowed.
    # Exempt: --help / -h anywhere in argv (Typer processes help before command body,
    #         but the main callback still fires first with resilient_parsing=True).
    _AUTH_EXEMPT = {"login", "logout", "whoami", "update"}
    cmd = ctx.invoked_subcommand
    _wants_help = "--help" in sys.argv or "-h" in sys.argv or getattr(ctx, "resilient_parsing", False)

    if cmd is not None and cmd not in _AUTH_EXEMPT and not _wants_help:
        if os.environ.get("SAGE_TESTING") == "1":
            return
        from sage.core.cli_auth import load_auth, _is_expired, _refresh_token
        auth = load_auth()
        if auth is None:
            renderer.error(
                "[bold]Login required.[/bold]\n\n"
                "  Run: [cyan]sage login[/cyan]\n\n"
                "  Don't have an account? Sign up at https://sageworksai.com\n"
                "  Browser AI on the website is always free."
            )
            raise typer.Exit(1)
        # Silently refresh token if expired (non-blocking)
        try:
            if _is_expired(auth):
                _refresh_token(auth)
        except Exception:
            pass  # token refresh failing is non-fatal

    if ctx.invoked_subcommand is None and not version:
        ctx.invoke(run)


# ── Auth commands ─────────────────────────────────────────────────────────────

@app.command("login")
def login_cmd() -> None:
    """Log in to SAGE AI via your browser.

    Opens the SAGE website where you can sign in with:
      • Google
      • Apple
      • Email / password

    After you log in, the token is sent back to the CLI automatically.
    Required for CLI usage (Starter plan or higher).
    Browser AI on the website is always free.
    """
    from sage.core.cli_auth import login, load_auth, clear_auth, _is_expired, _refresh_token

    existing = load_auth()
    if existing and existing.get("email"):
        # Verify the token is actually usable — not just that the file exists.
        # Empty/missing refresh_token means we can't re-authenticate silently.
        has_refresh = bool(existing.get("refresh_token"))
        token_ok = has_refresh and not _is_expired(existing)

        if not token_ok and has_refresh:
            # Try refreshing
            try:
                existing = _refresh_token(existing)
                token_ok = True
            except Exception:
                token_ok = False

        if token_ok:
            print(f"Already logged in as {existing['email']} (plan: {existing.get('tier','?')})")
            print("Run 'sage logout' first to switch accounts.")
            return

        # Stale auth (no refresh token or refresh failed) — clear and re-login
        print(f"Session expired for {existing.get('email','unknown')} — re-authenticating...")
        clear_auth()

    try:
        auth = login()
        renderer.console.print()
        renderer.success(f"Logged in as [cyan]{auth['email']}[/cyan]  (plan: [bold]{auth.get('tier','free')}[/bold])")
        if auth.get("tier") == "free":
            renderer.warning(
                "You are on the Free plan — CLI requires Starter ($19/mo) or higher.\n"
                "  Upgrade at: https://sageworksai.com  (Billing tab)"
            )
    except KeyboardInterrupt:
        renderer.info("\nLogin cancelled.")
    except Exception as exc:
        renderer.error(str(exc))
        raise typer.Exit(1)


@app.command("logout")
def logout_cmd() -> None:
    """Log out of your SAGE account."""
    from sage.core.cli_auth import logout, load_auth
    from sage.cli_core import _sms_terminate_process
    from sage.core.sms_bridge import SMS_PID_FILE
    
    auth = load_auth()
    if auth is None:
        renderer.info("Not logged in.")
        return

    # Critical: Stop the SMS bridge if it's running.
    # This prevents the old session from bleeding into the next user's login.
    if SMS_PID_FILE.exists():
        try:
            pid = int(SMS_PID_FILE.read_text().strip())
            if _sms_terminate_process(pid):
                renderer.info("Stopped active SMS bridge.")
            if SMS_PID_FILE.exists():
                SMS_PID_FILE.unlink()
        except Exception:
            pass

    logout()
    renderer.success(f"Logged out of {auth.get('email', 'account')}.")


@app.command("whoami")
def whoami_cmd() -> None:
    """Show the currently logged-in SAGE account."""
    from sage.core.cli_auth import whoami
    info = whoami()
    if info is None:
        renderer.warning("Not logged in. Run: sage login")
        return
    renderer.console.print(f"  Email:  [cyan]{info['email']}[/cyan]")
    renderer.console.print(f"  Plan:   [bold]{info['tier']}[/bold]")


_LLAMA_CPP_ERROR_PATTERNS: tuple[tuple[str, str], ...] = (
    # Mac: Xcode CLT not installed / pointed at wrong location.
    (
        "xcrun: error: invalid active developer path",
        "Xcode Command Line Tools are missing or misconfigured. Run "
        "`xcode-select --install` (accept the GUI prompt), or if Xcode is "
        "installed point CLT at it with `sudo xcode-select -s "
        "/Applications/Xcode.app/Contents/Developer`. Then re-run sage fix-llama-cpp.",
    ),
    (
        "fatal error: 'Foundation/Foundation.h' file not found",
        "macOS SDK headers aren't reachable — Xcode Command Line Tools missing or "
        "out of date. Run `xcode-select --install` and retry.",
    ),
    # Linux: missing CUDA toolkit.
    (
        "No CMAKE_CUDA_COMPILER could be found",
        "CUDA toolkit not found. Install it (e.g. `sudo apt install nvidia-cuda-toolkit` "
        "on Ubuntu) and ensure `nvcc` is on PATH, or rerun without CUDA: "
        "`CMAKE_ARGS='-DGGML_BLAS=ON' sage fix-llama-cpp` for CPU-only.",
    ),
    # Generic: missing C/C++ compiler.
    (
        "No CMAKE_C_COMPILER could be found",
        "No C compiler detected by CMake. macOS: `xcode-select --install`. "
        "Ubuntu/Debian: `sudo apt install build-essential`. Fedora: "
        "`sudo dnf install gcc gcc-c++`. Windows: install Visual Studio Build Tools.",
    ),
    (
        "No CMAKE_CXX_COMPILER could be found",
        "No C++ compiler detected by CMake. macOS: `xcode-select --install`. "
        "Ubuntu/Debian: `sudo apt install build-essential`. Fedora: "
        "`sudo dnf install gcc-c++`.",
    ),
    # Missing cmake / ninja itself.
    (
        "CMake was unable to find a build program",
        "cmake found no buildable backend (ninja/make). Install one: macOS "
        "`brew install ninja`, Ubuntu/Debian `sudo apt install ninja-build`.",
    ),
    # PEP 668 externally-managed-environment.
    (
        "externally-managed-environment",
        "Your system Python (PEP 668) refuses pip installs. Install sage via "
        "pipx instead (`brew install pipx && pipx install sage-ai-cli`), then "
        "re-run fix-llama-cpp. Or use a venv. Avoid --break-system-packages.",
    ),
    # Apple Metal toolchain.
    (
        "metal_library_compilation_failed",
        "Metal shader compilation failed. This usually means stale Xcode CLT — "
        "run `softwareupdate --install -a` to update macOS, then "
        "`sudo xcode-select --reset` to clear the developer-path cache. "
        "If problems persist, fall back to Ollama: `sage use ollama:gemma4`.",
    ),
    # Ninja stopped (user's case) — fallback advisory.
    (
        "ninja: build stopped",
        "ninja stopped compiling. The exact cause is usually a few lines up "
        "in the pip output. Common Mac fix: `xcode-select --install` (or "
        "`sudo xcode-select --reset`). Common Linux fix: install matching "
        "system libs (build-essential, libssl-dev). If reaches you nowhere, "
        "use the Ollama backend instead: `sage use ollama:gemma4`.",
    ),
)


def _diagnose_llama_cpp_failure(output: str) -> list[str]:
    """Scan captured pip/cmake/ninja output for known failure patterns.

    Returns a list of actionable hint strings (often just one). Empty list
    means no known pattern matched — the caller should fall back to a
    generic "see pip output above" message.

    Patterns are checked in priority order: the more specific the pattern,
    the earlier it lives in `_LLAMA_CPP_ERROR_PATTERNS`. Multiple matches
    are allowed because a single failure can trigger several signatures
    (e.g. "ninja stopped" plus the upstream "xcrun: error").
    """
    if not output:
        return []
    hints: list[str] = []
    seen: set[str] = set()
    for needle, advice in _LLAMA_CPP_ERROR_PATTERNS:
        if needle in output and advice not in seen:
            hints.append(advice)
            seen.add(advice)
    return hints


@app.command("fix-llama-cpp")
def fix_llama_cpp_cmd(
    yes: Annotated[
        bool,
        typer.Option("--yes", "-y", help="Skip confirmation prompt and run immediately"),
    ] = False,
) -> None:
    """Rebuild llama-cpp-python from source with GPU acceleration for this machine.

    Use this when local GGUF models fail to load with errors like:
      • "Failed to create llama_context"
      • "ggml_metal_library_init: error"
      • "Metal library compilation failed"
      • "CUDA error: ..."

    What this does (per platform):
      • macOS:   GGML_METAL=ON + GGML_METAL_EMBED_LIBRARY=ON + GGML_ACCELERATE=OFF
                  (pre-compiles Metal shaders at build time, avoids vecLib clash)
      • Linux:   GGML_CUDA=ON if nvcc found, else GGML_HIPBLAS for ROCm,
                  else GGML_BLAS for OpenBLAS CPU acceleration
      • Windows: GGML_CUDA=ON if nvcc found, else uses prebuilt wheel

    Skipped automatically when Python's architecture doesn't match the
    hardware (e.g. x86_64 Python under Rosetta on arm64 Mac) — the build
    can't possibly produce a working binary in that case.

    Takes ~5-10 minutes. Requires cmake + native compiler (Xcode/gcc/MSVC).
    Falls back gracefully on failure: Ollama backend continues to work.
    """
    import os, platform, shutil, subprocess

    plat = sys.platform
    py_arch = platform.machine()  # what THIS python process sees as its arch

    # Architecture-mismatch guard. On macOS, an x86_64 Python running under
    # Rosetta on arm64 hardware will report `platform.machine() == 'x86_64'`
    # because Rosetta translates the syscall. So we can't compare py_arch to
    # platform.uname().machine — they'll both lie. The reliable check is
    # `sysctl sysctl.proc_translated` from inside this process: returns "1"
    # iff we're running under Rosetta. On Linux/Windows the check is N/A
    # (no equivalent translation layer for our case).
    rosetta = False
    if plat == "darwin":
        try:
            r = subprocess.run(
                ["sysctl", "-n", "sysctl.proc_translated"],
                capture_output=True, text=True, timeout=2,
            )
            rosetta = r.stdout.strip() == "1"
        except Exception:
            rosetta = False
    if rosetta:
        renderer.error(
            f"This Python ({py_arch}) is running under Rosetta translation on "
            "Apple Silicon hardware. Rebuilding llama-cpp-python in this "
            "environment will fail (vecLib/__m128i clash with the arm64 SDK), "
            "and even if it succeeded the binary couldn't take advantage of "
            "the GPU."
        )
        renderer.info(
            "Fix: install an arm64 native Python. On macOS the easiest path is "
            "Homebrew (`brew install python@3.12`) — its Python is arm64 by "
            "default on Apple Silicon. Then re-run `sage fix-llama-cpp`."
        )
        renderer.info(
            "Workaround (no Python migration needed): use the Ollama backend, "
            "which handles GPU acceleration outside of Python: "
            "`sage use ollama:gemma4` (or whichever model you've pulled)."
        )
        raise typer.Exit(code=2)

    # Pick CMAKE_ARGS for this platform + GPU.
    cmake_args: str
    if plat == "darwin":
        # GGML_NATIVE=OFF + GGML_CPU_REPACK=OFF: Apple clang on arm64 rejects
        # `-mcpu=native` which llama.cpp adds when GGML_NATIVE is on. Disabling
        # native-CPU detection costs us a small tuning bonus (NEON is still
        # used; that's the actual ARM SIMD path) but is necessary for the
        # build to complete on macOS 26+ SDKs.
        cmake_args = (
            "-DGGML_METAL=ON -DGGML_METAL_EMBED_LIBRARY=ON "
            "-DGGML_ACCELERATE=OFF -DGGML_BLAS=OFF "
            "-DGGML_NATIVE=OFF -DGGML_CPU_REPACK=OFF "
            # Skip optional binaries that pull in cpp-httplib + TLS — those
            # have an arm64 link mismatch (httplib::tls::get_cert_der)
            # on macOS 26 SDK and we don't need them for Python bindings.
            "-DLLAMA_CURL=OFF -DLLAMA_BUILD_SERVER=OFF "
            "-DLLAMA_BUILD_EXAMPLES=OFF -DLLAMA_BUILD_TESTS=OFF"
        )
        backend = "Apple Metal (GPU)"
    elif plat.startswith("linux"):
        if shutil.which("nvcc") or os.path.exists("/usr/local/cuda/bin/nvcc"):
            cmake_args = "-DGGML_CUDA=ON"
            backend = "NVIDIA CUDA (GPU)"
        elif shutil.which("hipcc"):
            cmake_args = "-DGGML_HIPBLAS=ON"
            backend = "AMD ROCm (GPU)"
        else:
            cmake_args = "-DGGML_BLAS=ON -DGGML_BLAS_VENDOR=OpenBLAS"
            backend = "OpenBLAS (CPU)"
    elif plat == "win32":
        if shutil.which("nvcc"):
            cmake_args = "-DGGML_CUDA=ON"
            backend = "NVIDIA CUDA (GPU)"
        else:
            renderer.warning(
                "No CUDA detected on Windows. The PyPI wheel is already CPU-only — "
                "rebuilding from source rarely helps. Use Ollama for GPU."
            )
            raise typer.Exit(code=0)
    else:
        renderer.error(f"Unsupported platform: {plat}")
        raise typer.Exit(code=2)

    if not shutil.which("cmake"):
        renderer.error(
            "cmake is required to rebuild llama-cpp-python. Install it:\n"
            "  macOS:   brew install cmake\n"
            "  Ubuntu:  sudo apt install cmake\n"
            "  Fedora:  sudo dnf install cmake\n"
            "  Windows: winget install Kitware.CMake"
        )
        raise typer.Exit(code=2)

    renderer.console.print(
        f"\nWill rebuild [bold]llama-cpp-python[/bold] for [cyan]{backend}[/cyan]."
    )
    renderer.console.print(f"  CMAKE_ARGS = [dim]{cmake_args}[/dim]")
    renderer.console.print("  Build takes ~5-10 minutes. Disk + CPU-intensive.")
    renderer.console.print(
        "  Falls back to Ollama on failure (your bridge keeps working).\n"
    )

    if not yes:
        try:
            confirm = input("Proceed? [y/N] ").strip().lower()
        except (KeyboardInterrupt, EOFError):
            confirm = "n"
        if confirm not in ("y", "yes"):
            renderer.info("Skipped. Re-run with --yes to bypass confirmation.")
            raise typer.Exit(code=0)

    # Run the build via pip with proper CMAKE_ARGS.
    # IMPORTANT: scrub env vars that can silently force the wrong target
    # arch. Specifically `CC` and `CXX` set in user shell profiles often
    # point at Homebrew GCC (e.g. /usr/local/bin/g++-14 = x86_64), which
    # CMake honors over its own toolchain detection — producing an x86_64
    # dylib that arm64 Python can't dlopen. Let CMake pick Apple clang.
    env = {**os.environ, "CMAKE_ARGS": cmake_args}
    for var in ("CC", "CXX", "ARCHFLAGS", "CFLAGS", "CXXFLAGS",
                "CMAKE_C_COMPILER", "CMAKE_CXX_COMPILER"):
        env.pop(var, None)
    # On macOS, force the build to target the running Python's arch. Without
    # this, environment leakage (Conda, x86_64 GCC on PATH, etc.) can silently
    # build for the wrong arch and the resulting dylib fails to load.
    if plat == "darwin":
        env["CMAKE_OSX_ARCHITECTURES"] = py_arch
        env["ARCHFLAGS"] = f"-arch {py_arch}"
        env["CMAKE_ARGS"] = (
            f"{cmake_args} -DCMAKE_OSX_ARCHITECTURES={py_arch}"
        )
    cmd = [
        sys.executable, "-m", "pip", "install",
        "--upgrade", "--force-reinstall", "--no-cache-dir",
        "--no-binary", "llama-cpp-python",
        "llama-cpp-python",
    ]
    renderer.info(
        f"Running pip install (target arch: {py_arch})… this is the long step."
    )
    # Tee output: live to the user's terminal AND captured into a buffer so
    # `_diagnose_llama_cpp_failure` can scan for known error signatures
    # without forcing the user to re-read 200+ lines of build noise.
    captured: list[str] = []
    proc = subprocess.Popen(
        cmd,
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
    )
    assert proc.stdout is not None
    for line in proc.stdout:
        sys.stdout.write(line)
        sys.stdout.flush()
        captured.append(line)
    rc = proc.wait()
    if rc != 0:
        renderer.error("Rebuild failed.")
        hints = _diagnose_llama_cpp_failure("".join(captured))
        if hints:
            renderer.console.print()
            renderer.console.print("[bold]Diagnosis (specific to your output):[/bold]")
            for hint in hints:
                renderer.console.print(f"  • {hint}")
        else:
            renderer.info(
                "Common causes: missing Xcode (macOS), missing CUDA toolkit (Linux), "
                "Python arch mismatch with hardware. Ollama backend keeps working."
            )
        raise typer.Exit(code=rc)

    renderer.success("✓ llama-cpp-python rebuilt successfully.")
    renderer.info("Test: sage use llama_cpp:gemma4 (or whichever GGUF you have)")


# ══════════════════════════════════════════════════════════════════════════════
# SMS / MESSAGE BRIDGE
# User-scoped: authorized contacts and device registry live in the SAGE backend.
# Requires sage login. Works with iMessage and Google Messages (no carrier config).
# ══════════════════════════════════════════════════════════════════════════════

def _sms_backend():
    """Load the SAGE backend client using the current auth token."""
    from sage.core.sms_bridge import SAGEBackend, _load_sage_token
    token, base = _load_sage_token()
    return SAGEBackend(token, base)


def _sms_process_alive(pid: int) -> bool:
    """Cross-platform "is this PID still running?" check.

    On Windows, we use in-process Win32 Toolhelp snapshots to query the active PID
    extremely quickly without calling slow and potentially hung CLI commands like tasklist.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes

            class PROCESSENTRY32(ctypes.Structure):
                _fields_ = [
                    ("dwSize", wintypes.DWORD),
                    ("cntUsage", wintypes.DWORD),
                    ("th32ProcessID", wintypes.DWORD),
                    ("th32DefaultHeapID", ctypes.c_size_t),
                    ("th32ModuleID", wintypes.DWORD),
                    ("cntThreads", wintypes.DWORD),
                    ("th32ParentProcessID", wintypes.DWORD),
                    ("pcPriClassBase", wintypes.LONG),
                    ("dwFlags", wintypes.DWORD),
                    ("szExeFile", ctypes.c_char * 260)
                ]

            CreateToolhelp32Snapshot = ctypes.windll.kernel32.CreateToolhelp32Snapshot
            CreateToolhelp32Snapshot.argtypes = [wintypes.DWORD, wintypes.DWORD]
            CreateToolhelp32Snapshot.restype = wintypes.HANDLE
            Process32First = ctypes.windll.kernel32.Process32First
            Process32First.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
            Process32First.restype = wintypes.BOOL
            Process32Next = ctypes.windll.kernel32.Process32Next
            Process32Next.argtypes = [wintypes.HANDLE, ctypes.POINTER(PROCESSENTRY32)]
            Process32Next.restype = wintypes.BOOL
            CloseHandle = ctypes.windll.kernel32.CloseHandle
            CloseHandle.argtypes = [wintypes.HANDLE]
            CloseHandle.restype = wintypes.BOOL

            TH32CS_SNAPPROCESS = 0x00000002
            hSnapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
            found = False
            if hSnapshot != -1:
                pe = PROCESSENTRY32()
                pe.dwSize = ctypes.sizeof(PROCESSENTRY32)
                retval = Process32First(hSnapshot, ctypes.byref(pe))
                while retval:
                    if pe.th32ProcessID == pid:
                        found = True
                        break
                    retval = Process32Next(hSnapshot, ctypes.byref(pe))
                CloseHandle(hSnapshot)
            return found
        except Exception:
            return False
    try:
        os.kill(pid, 0)
        return True
    except (OSError, ProcessLookupError, PermissionError):
        return False


def _sms_terminate_process(pid: int) -> bool:
    """Cross-platform "terminate this PID" — equivalent of SIGTERM.

    On Windows, we use the Win32 TerminateProcess API directly to kill the target PID
    instantly, bypassing the potentially slow taskkill command.
    """
    if sys.platform == "win32":
        try:
            import ctypes
            from ctypes import wintypes
            OpenProcess = ctypes.windll.kernel32.OpenProcess
            OpenProcess.argtypes = [wintypes.DWORD, wintypes.BOOL, wintypes.DWORD]
            OpenProcess.restype = wintypes.HANDLE
            TerminateProcess = ctypes.windll.kernel32.TerminateProcess
            TerminateProcess.argtypes = [wintypes.HANDLE, wintypes.UINT]
            TerminateProcess.restype = wintypes.BOOL
            CloseHandle = ctypes.windll.kernel32.CloseHandle
            CloseHandle.argtypes = [wintypes.HANDLE]
            CloseHandle.restype = wintypes.BOOL

            PROCESS_TERMINATE = 0x0001
            hProcess = OpenProcess(PROCESS_TERMINATE, False, pid)
            if hProcess:
                ok = TerminateProcess(hProcess, 1)
                CloseHandle(hProcess)
                return bool(ok)
            return False
        except Exception:
            return False
    try:
        import signal as _signal
        os.kill(pid, _signal.SIGTERM)
        return True
    except ProcessLookupError:
        return False
    except Exception:
        return False


