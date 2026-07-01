"""
cvc.cli — Command-line interface for the Cognitive Version Control system.

A beautiful, developer-friendly CLI powered by Rich.

Usage:
    cvc setup                  Interactive first-time configuration
    cvc gateway start          Start the CVC Gateway (proxy + dashboard)
    cvc init                   Initialise a .cvc/ directory in the current project
    cvc status                 Show current branch, HEAD, and branch list
    cvc log                    Show commit history for the active branch
    cvc commit -m "message"    Create a manual cognitive commit
    cvc branch <name>          Create and switch to a new branch
    cvc merge <source>         Merge source branch into the active branch
    cvc restore <hash>         Restore context to a previous commit
    cvc install-hooks          Install Git hooks for VCS synchronisation
    cvc capture-snapshot       Capture CVC state linked to current Git commit
    cvc doctor                 Health check for your CVC environment
"""

from __future__ import annotations
from cvc._subprocess_compat import HIDDEN_KW
from typing import Any


import json
import logging
import os
import shutil
import sys
from pathlib import Path

import click
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

if sys.platform == "win32":
    # Force UTF-8 codepage in Windows CMD/PowerShell to prevent ASCII block mojibake
    os.system("chcp 65001 >nul 2>&1")
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

console = Console()


# ---------------------------------------------------------------------------
# Dynamic provider choice list (used by @click.Choice on --provider flags)
# ---------------------------------------------------------------------------
# Must be defined before any @main.command() that references it, because
# Click evaluates the decorator at import time. The function reads from
# cvc.setup.registry which combines hand-written specs with the
# Hermes-catalog wrappers (zai, kimi, stepfun, alibaba, arcee, gmi,
# ollama-cloud, huggingface, xai, …).

def _setup_provider_choice() -> list[str]:
    """Build the dynamic Click.Choice list from cvc.setup.registry
    so `cvc setup --provider zai` (or any new provider) is accepted.
    Falls back to the legacy 11-provider list if the registry import fails.
    """
    try:
        from cvc.setup import list_provider_specs_all
        keys = [s.key for s in list_provider_specs_all()]
        # Always include legacy aliases that show up in --provider as a convenience.
        for alias in ("passthrough", "copilot"):
            if alias not in keys:
                keys.append(alias)
        return sorted(set(keys))
    except Exception:
        return ["anthropic", "openai", "google", "vertex", "ollama", "lmstudio",
                "github", "copilot", "nvidia", "minimax", "passthrough"]


# ---------------------------------------------------------------------------
# Branding
# ---------------------------------------------------------------------------

LOGO = """[bold #CC3333]
 ██████╗ ██╗   ██╗  ██████╗
██╔════╝ ██║   ██║ ██╔════╝
██║      ██║   ██║ ██║     
██║      ╚██╗ ██╔╝ ██║     
╚██████╗  ╚████╔╝  ╚██████╗
 ╚═════╝   ╚═══╝    ╚═════╝[/bold #CC3333]"""

TAGLINE = "[#8B7070]Cognitive Version Control — Git for the AI Agents[/#8B7070]"

try:
    from cvc import __version__ as VERSION
except ImportError:
    VERSION = "1.4.81"


def _banner(subtitle: str = "") -> None:
    """Print the CVC banner with custom top border (Meena center, version right)."""
    from rich.box import Box as _Box

    # ── Custom top border: ── Meena ──────── v1.x.x ──
    tw = console.width or 80
    ver = f" v{VERSION} "
    meena = " Meena "
    inner = tw - 2  # space between ╭ and ╮

    pad_spaces = max(0, (inner - 27) // 2)
    pad = " " * pad_spaces
    padded_logo = "\n".join(pad + line if line.strip() else line for line in LOGO.split("\n"))

    content = f"{padded_logo}\n\n[center]{TAGLINE}[/center]"
    if subtitle:
        content += f"\n\n[center][bold #E8D0D0]{subtitle}[/bold #E8D0D0][/center]"

    center = inner // 2
    m_start = max(center - len(meena) // 2, 1)
    m_end = m_start + len(meena)
    v_start = max(inner - len(ver), m_end + 1)

    top = Text()
    top.append("╭", style="#8B0000")
    top.append("─" * m_start, style="#8B0000")
    top.append(meena, style="bold #CC3333")
    gap = v_start - m_end
    top.append("─" * max(gap, 1), style="#8B0000")
    top.append(ver, style="bold #FF4444")
    remaining = inner - v_start - len(ver)
    top.append("─" * max(remaining, 0), style="#8B0000")
    top.append("╮", style="#8B0000")
    console.print(top)

    # Body + bottom border via Panel with no-top-border custom box
    _NO_TOP_BOX = _Box(
        "│  │\n"
        "│  │\n"
        "├──┤\n"
        "│  │\n"
        "├──┤\n"
        "│  │\n"
        "├──┤\n"
        "╰──╯\n"
    )
    console.print(
        Panel(
            content,
            box=_NO_TOP_BOX,
            border_style="#8B0000",
            padding=(1, 4),
            width=tw,
            subtitle="[#8B7070]Time Machine for AI Agents[/#8B7070]",
            subtitle_align="center",
        ),
        highlight=False,
    )
    console.print()


def _success(msg: str) -> None:
    console.print(f"  [bold #55AA55]✓[/bold #55AA55] {msg}")


def _error(msg: str) -> None:
    console.print(f"  [bold red]✗[/bold red] {msg}")


def _warn(msg: str) -> None:
    console.print(f"  [bold #CCAA44]![/bold #CCAA44] {msg}")


def _info(msg: str) -> None:
    console.print(f"  [dim]→[/dim] {msg}")


def _hint(msg: str) -> None:
    console.print()
    console.print(
        Panel(
            msg,
            border_style="#5C1010",
            title="[bold #8B7070]Hint[/bold #8B7070]",
            padding=(0, 2),
        )
    )


def _setup_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.WARNING
    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(name)s] %(levelname)s — %(message)s",
        datefmt="%H:%M:%S",
    )


def _get_config():
    from cvc.core.models import CVCConfig
    return CVCConfig.for_project()


def _get_engine():
    from cvc.core.database import ContextDatabase
    from cvc.operations.engine import CVCEngine
    config = _get_config()
    config.ensure_dirs()
    db = ContextDatabase(config)
    return CVCEngine(config, db), db


# ---------------------------------------------------------------------------
# IDE Auto-Detection & Auto-Configuration
# ---------------------------------------------------------------------------

def _get_ide_config_paths() -> dict[str, dict]:
    """Return known install/config paths for detectable IDEs per platform."""
    if sys.platform == "win32":
        appdata = Path(os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming"))
        return {
            "vscode": {
                "name": "Visual Studio Code",
                "icon": "💎",
                "settings": appdata / "Code" / "User" / "settings.json",
                "command": "code",
                "can_auto_config": True,
                "auth_type": "byok",
            },
            "cursor": {
                "name": "Cursor",
                "icon": "🖱️",
                "settings": appdata / "Cursor" / "User" / "settings.json",
                "command": "cursor",
                "can_auto_config": False,
                "auth_type": "api_key_override",
            },
            "windsurf": {
                "name": "Windsurf",
                "icon": "🏄",
                "settings": appdata / "Windsurf" / "User" / "settings.json",
                "command": "windsurf",
                "can_auto_config": False,
                "auth_type": "account_auth",
            },
        }
    elif sys.platform == "darwin":
        support = Path.home() / "Library" / "Application Support"
        return {
            "vscode": {
                "name": "Visual Studio Code",
                "icon": "💎",
                "settings": support / "Code" / "User" / "settings.json",
                "command": "code",
                "can_auto_config": True,
                "auth_type": "byok",
            },
            "cursor": {
                "name": "Cursor",
                "icon": "🖱️",
                "settings": support / "Cursor" / "User" / "settings.json",
                "command": "cursor",
                "can_auto_config": False,
                "auth_type": "api_key_override",
            },
            "windsurf": {
                "name": "Windsurf",
                "icon": "🏄",
                "settings": support / "Windsurf" / "User" / "settings.json",
                "command": "windsurf",
                "can_auto_config": False,
                "auth_type": "account_auth",
            },
        }
    else:  # Linux
        config_home = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        return {
            "vscode": {
                "name": "Visual Studio Code",
                "icon": "💎",
                "settings": config_home / "Code" / "User" / "settings.json",
                "command": "code",
                "can_auto_config": True,
                "auth_type": "byok",
            },
            "cursor": {
                "name": "Cursor",
                "icon": "🖱️",
                "settings": config_home / "Cursor" / "User" / "settings.json",
                "command": "cursor",
                "can_auto_config": False,
                "auth_type": "api_key_override",
            },
            "windsurf": {
                "name": "Windsurf",
                "icon": "🏄",
                "settings": config_home / "Windsurf" / "User" / "settings.json",
                "command": "windsurf",
                "can_auto_config": False,
                "auth_type": "account_auth",
            },
        }


def _detect_ides() -> dict[str, dict]:
    """Detect installed IDEs by checking config directories and PATH."""
    ide_paths = _get_ide_config_paths()
    detected = {}
    for ide_key, info in ide_paths.items():
        found = False
        reason = ""
        # Check if config directory exists (indicates installation)
        settings_dir = info["settings"].parent
        if settings_dir.exists():
            found = True
            reason = "config found"
        # Check if command is on PATH
        cmd = info.get("command")
        if cmd and shutil.which(cmd):
            found = True
            reason = "installed"
        if found:
            detected[ide_key] = {**info, "reason": reason}
    return detected


def _auto_configure_vscode(settings_path: Path, endpoint: str, model: str) -> bool:
    """
    Auto-configure VS Code Copilot BYOK to route through CVC proxy.

    Writes ``github.copilot.chat.customOAIModels`` into the user-level
    settings.json so Copilot can use CVC as an OpenAI-compatible provider.
    Returns True on success.
    """
    settings: dict = {}
    if settings_path.exists():
        try:
            raw = settings_path.read_text(encoding="utf-8")
            settings = json.loads(raw)
        except (json.JSONDecodeError, OSError):
            return False  # JSONC, permissions, etc.

    custom_models = settings.get("github.copilot.chat.customOAIModels", {})
    custom_models["cvc-proxy"] = {
        "name": f"CVC Proxy ({model})",
        "url": f"{endpoint}/v1/chat/completions",
        "toolCalling": True,
        "vision": False,
        "thinking": False,
        "maxInputTokens": 128000,
        "maxOutputTokens": 8192,
        "requiresAPIKey": True,
    }
    settings["github.copilot.chat.customOAIModels"] = custom_models

    try:
        settings_path.parent.mkdir(parents=True, exist_ok=True)
        settings_path.write_text(json.dumps(settings, indent=4), encoding="utf-8")
        return True
    except OSError:
        return False


def _run_ide_detection(model: str, endpoint: str = "http://127.0.0.1:13421") -> dict[str, dict]:
    """
    Detect IDEs and auto-configure where possible.

    Called at the end of ``setup`` to wire up detected IDEs automatically.
    Returns the detection results dict.
    """
    console.print("[bold #CC3333]  Detecting installed IDEs…[/bold #CC3333]")
    console.print()

    detected = _detect_ides()

    if not detected:
        _info("No IDEs auto-detected. Run [bold]cvc connect[/bold] for manual setup guides.")
        console.print()
        return detected

    for ide_key, ide_info in detected.items():
        _success(
            f"{ide_info['icon']}  [bold]{ide_info['name']}[/bold] detected  "
            f"[dim]({ide_info['reason']})[/dim]"
        )

        if ide_key == "vscode" and ide_info.get("can_auto_config"):
            ok = _auto_configure_vscode(ide_info["settings"], endpoint, model)
            if ok:
                _success("   → Copilot BYOK auto-configured with CVC proxy")
                _info("   Select [bold]CVC Proxy[/bold] in the Copilot model picker")
                _info("   Or run [bold]cvc mcp[/bold] for native Copilot MCP integration")
                ide_info["configured"] = True
            else:
                _warn("   → Could not auto-configure (settings.json may have comments)")
                _info("   Run [bold]cvc connect vscode[/bold] for manual steps")
                ide_info["configured"] = False

        elif ide_key == "cursor":
            _info("   → Open [bold]Cursor Settings → Models[/bold]")
            _info(f"   → Override OpenAI Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]")
            _info("   → API Key → [#CC3333]cvc[/#CC3333]")
            _info("   → Or add CVC as an MCP server: [bold]cvc connect cursor[/bold]")
            ide_info["configured"] = "manual"

        elif ide_key == "windsurf":
            _info("   → Windsurf uses account-based auth (no API override)")
            _info("   → Use CVC via MCP: run [bold]cvc mcp[/bold]")
            _info("   → Add to Windsurf MCP config: [bold]cvc connect windsurf[/bold]")
            ide_info["configured"] = "mcp"

    console.print()
    return detected


# ---------------------------------------------------------------------------
# Click Group (entry point)
# ---------------------------------------------------------------------------

class CvcGroup(click.Group):
    """Custom group that shows help in a styled format."""

    def format_help(self, ctx, formatter):
        """Override to use Rich-styled help."""
        _banner()

        # Commands table
        table = Table(
            box=box.ROUNDED,
            border_style="dim",
            show_header=True,
            header_style="bold #CC3333",
            padding=(0, 2),
        )
        table.add_column("Command", style="bold white", width=22)
        table.add_column("Description", style="dim white")

        cmds = [
            ("agent", "Interactive AI coding agent (like Claude Code)"),
            ("launch <tool>", "Auto-launch any AI tool through CVC"),
            ("up", "One-command start (setup + init + gateway)"),
            ("setup", "Interactive first-time setup"),
            ("login", "Sign in to CVC using Google or GitHub"),
            ("logout", "Sign out from CVC"),
            ("whoami", "Show currently logged-in user"),
            ("gateway start", "Start the CVC Gateway (proxy + dashboard)"),
            ("gateway status", "Check Gateway & service health"),
            ("gateway stop", "Stop the Gateway"),
            ("connect", "Connect your AI tool to CVC"),
            ("mcp", "Start CVC as an MCP server"),
            ("recall \"query\"", "Search ALL past conversations (NL search)"),
            ("context --show", "Display stored conversation content"),
            ("export --markdown", "Export conversation as shareable Markdown"),
            ("inject <project>", "Cross-project context transfer"),
            ("diff <hash1> <hash2>", "Knowledge / decision diff between commits"),
            ("stats", "Analytics dashboard (tokens, costs, patterns)"),
            ("compact --smart", "AI-powered context compression"),
            ("timeline", "ASCII timeline of all AI interactions"),
            ("sync push/pull", "Push/pull AI context to team remote"),
            ("audit", "Security audit trail (compliance-ready)"),
            ("sessions", "View Time Machine session history"),
            ("init", "Initialise .cvc/ in your project"),
            ("status", "Show branch, HEAD, context size"),
            ("log", "View commit history"),
            ("commit -m '...'", "Create a cognitive checkpoint"),
            ("branch <name>", "Create an exploration branch"),
            ("merge <branch>", "Semantic merge into active branch"),
            ("restore <hash>", "Time-travel to a previous state"),
            ("install-hooks", "Install Git ↔ CVC sync hooks"),
            ("doctor", "Health check your environment"),
            ("update", "Update CVC to the latest version"),
            ("config set", "Set a configuration value"),
            ("ignore <path>", "Add path to .cvcignore"),
            ("open / ui", "Open CVC dashboard in browser"),
            ("clean", "Purge cache and temporary data"),
            ("uninstall", "Completely remove CVC"),
            ("cognome init", "Bootstrap COGNOME substrate"),
            ("cognome status", "Show COGNOME state & stats"),
            ("cognome compile", "Compile an Engram for a query"),
            ("cognome enable/disable", "Toggle Engram injection"),
            ("cognome audit", "View Engram compilation audit trail"),
            ("cognome cache-prune", "Evict stale cached Engrams"),
        ]
        for cmd, desc in cmds:
            table.add_row(cmd, desc)

        console.print(
            Panel(
                table,
                border_style="#8B0000",
                title="[bold white]Commands[/bold white]",
                padding=(1, 1),
            )
        )

        # Quick start hint
        console.print()
        console.print(
            Panel(
                "[bold #E8D0D0]Get started in 10 seconds:[/bold #E8D0D0]\n\n"
                "  [#CC3333]$[/#CC3333] cvc agent              [#8B7070]# Interactive AI agent right here in your terminal[/#8B7070]\n"
                "  [#CC3333]$[/#CC3333] cvc launch claude      [#8B7070]# Zero-config: launches Claude Code through CVC[/#8B7070]\n"
                "  [#CC3333]$[/#CC3333] cvc launch aider       [#8B7070]# Zero-config: launches Aider through CVC[/#8B7070]\n"
                "  [#CC3333]$[/#CC3333] cvc up                 [#8B7070]# One command: setup + init + gateway[/#8B7070]\n\n"
                "[bold #E8D0D0]Or step by step:[/bold #E8D0D0]\n\n"
                "  [#CC3333]$[/#CC3333] cvc setup              [#8B7070]# Pick your provider & model[/#8B7070]\n"
                "  [#CC3333]$[/#CC3333] cvc gateway start      [#8B7070]# Start the Gateway (proxy + dashboard)[/#8B7070]\n"
                "  [#CC3333]$[/#CC3333] cvc mcp                [#8B7070]# Start MCP server (auth-based IDEs)[/#8B7070]\n"
                "  [#CC3333]$[/#CC3333] cvc connect            [#8B7070]# Wire up Cursor, Cline, Claude Code…[/#8B7070]",
                border_style="#5C1010",
                title="[bold #55AA55]Quick Start[/bold #55AA55]",
                padding=(1, 2),
            )
        )

        console.print(
            "\n  [dim]Run[/dim] [bold]cvc <command> --help[/bold] [dim]for details on any command.[/dim]\n"
        )


@click.group(cls=CvcGroup, invoke_without_command=True)
@click.option("-v", "--verbose", is_flag=True, help="Enable debug logging.")
@click.version_option(VERSION, prog_name="cvc")
@click.pass_context
def main(ctx: click.Context, verbose: bool) -> None:
    """CVC — Cognitive Version Control: Git for the AI Mind."""
    _setup_logging(verbose)

    # ─── Enforce Login ───────────────────────────────────────────────────
    from cvc.auth import get_current_user

    excluded_commands = ["login", "logout", "whoami", "help"]
    if ctx.invoked_subcommand not in excluded_commands:
        if not get_current_user():
            _banner(subtitle="Authentication Required\n\nPlease log in to continue using CVC.")
            from cvc.auth import login_flow
            try:
                login_flow()
            except Exception:
                pass

            # If they aborted login, exit
            if not get_current_user():
                from rich.console import Console
                Console().print("\n[bold red]✗ Authentication required to use CVC.[/bold red]")
                raise SystemExit(1)

    if ctx.invoked_subcommand is not None:
        return  # A subcommand was given — Click handles it

    from cvc.core.models import get_global_config_dir

    gc_path = get_global_config_dir() / "config.json"

    if not gc_path.exists():
        # ─── First run — setup then straight into the agent ──────────────
        _banner(subtitle="Welcome to CVC!\n\nLooks like this is your first time here.\nLet's get you set up — it takes about 30 seconds.")
        ctx.invoke(setup, first_run=True)
        # After setup, fall through to launch the agent

    # ─── Launch the agent directly ───────────────────────────────────────
    ctx.invoke(agent)


# ---------------------------------------------------------------------------
# setup (guided first-time configuration)
# ---------------------------------------------------------------------------

MODEL_CATALOG = {
    "anthropic": [
        ("claude-opus-4-8", "Anthropic's flagship model — 1M context, high autonomy (Jan 2026)", "$5/$25 per MTok"),
        ("claude-sonnet-4-6", "Best speed/intelligence balance — 1M context, thinking", "$3/$15 per MTok"),
        ("claude-haiku-4-5", "Fastest model with near-frontier intelligence — 200k context", "$1/$5 per MTok"),
        ("claude-3-5-sonnet-20241022", "Claude 3.5 Sonnet — industry standard developer tool", "$3/$15 per MTok"),
        ("claude-3-5-haiku-20241022", "Claude 3.5 Haiku — extremely fast reasoning", "$0.80/$4 per MTok"),
        ("claude-3-opus-20240229", "Claude 3 Opus — legacy heavyweight reasoning", "$15/$75 per MTok"),
    ],
    "openai": [
        ("gpt-5.3", "Newest flagship — best reasoning & coding", "Frontier"),
        ("gpt-5.2", "Previous flagship — coding & agentic tasks", "Frontier"),
        ("gpt-5-mini", "Fast & cost-efficient GPT-5", "Mid-tier"),
        ("gpt-4o", "GPT-4o — high speed multimodal flagship", "$2.50/$10 per MTok"),
        ("gpt-4o-mini", "GPT-4o Mini — fast & cost-efficient", "$0.15/$0.60 per MTok"),
        ("o3-mini", "o3 Mini — latest generation lightweight reasoning", "$1.10/$4.40 per MTok"),
        ("o1", "o1 — frontier reasoning & complex math/STEM", "$15/$60 per MTok"),
        ("o1-mini", "o1 Mini — fast math & coding reasoning", "$3/$12 per MTok"),
    ],
    "google": [
        ("gemini-3.5-flash", "Gemini 3.5 Flash — Sustained frontier performance, 1M context (GA)", "Standard"),
        ("gemini-3.1-pro", "Gemini 3.1 Pro — Deep reasoning & coding, 1M context (GA)", "Premium"),
        ("gemini-3.1-flash-lite", "Gemini 3.1 Flash-Lite — Stable, low-cost high-volume (GA)", "Economy"),
        ("gemini-3.1-pro-preview", "Gemini 3.1 Pro — Refined thinking & agentic (Preview)", "Premium"),
        ("gemini-3-flash-preview", "Gemini 3 Flash — Fast thinking (Preview)", "Standard"),
        ("gemini-2.5-flash", "Gemini 2.5 Flash — GA stable", "Standard"),
        ("gemini-2.5-pro", "Gemini 2.5 Pro — GA stable, 1M context", "Premium"),
        ("gemini-1.5-flash", "Gemini 1.5 Flash — Highly efficient", "Economy"),
        ("gemini-1.5-pro", "Gemini 1.5 Pro — 2M context", "Standard"),
    ],
    # Confirmed tools badge on Ollama library as of Feb 2026
    "ollama": [
        ("qwen2.5-coder:7b", "Best 7B coding — 11M+ pulls, tools ✓", "~4 GB"),
        ("qwen3:14b", "Qwen3 — thinking + non-thinking modes, tools ✓", "~9 GB"),
        ("qwen3-coder:30b", "Agentic coder — MoE, 256K context, tools ✓", "~19 GB"),
        ("devstral:24b", "Mistral best open-source coding agent, tools ✓", "~14 GB"),
        ("deepseek-r1:8b", "DeepSeek-R1 — reasoning + tool calling", "~5 GB"),
        ("mistral-small3.2:24b", "Improved function calling + vision, tools ✓", "~15 GB"),
        ("qwq:32b", "QwQ deep reasoning + tool calling", "~20 GB"),
        ("llama3.3:70b", "Meta Llama 3.3 — powerful general model, tools ✓", "~40 GB"),
    ],
    "lmstudio": [
        ("qwen2.5-coder-32b-instruct", "Best local coding — native tools", "~18 GB"),
        ("qwen3-14b", "Qwen3 14B — thinking mode + tool calling", "~9 GB"),
        ("devstral-small-2505", "Mistral agentic coding model, tool calling", "~14 GB"),
        ("deepseek-r1-distill-qwen-32b", "Reasoning + coding, chain-of-thought", "~18 GB"),
        ("gemma-3-27b-it", "Google Gemma 3 27B instruction tuned", "~15 GB"),
        ("mistral-small-3.2-24b-instruct", "Improved function calling over 3.1", "~13 GB"),
    ],
    "vertex": [
        # Gemini 3.x — Preview (billing-enabled, production-ready) — April 2026
        ("gemini-3.1-pro-preview",        "Gemini 3.1 Pro — most advanced reasoning & agentic coding (Preview)", "Premium"),
        ("gemini-3-flash-preview",        "Gemini 3 Flash — best multimodal + complex agentic tasks (Preview)",   "Standard"),
        ("gemini-3.1-flash-lite-preview", "Gemini 3.1 Flash-Lite — lowest cost, high-volume (Preview)",           "Economy"),
        # Gemini 2.5 — GA stable channel
        ("gemini-2.5-pro",                "Gemini 2.5 Pro — GA stable, complex reasoning, 1M context",            "Premium"),
        ("gemini-2.5-flash",              "Gemini 2.5 Flash — GA stable, best price-performance balance",          "Standard"),
        ("gemini-2.5-flash-lite",         "Gemini 2.5 Flash-Lite — GA stable, ultra-efficient",                    "Economy"),
        # Legacy / Partner
        ("gemini-2.0-flash",              "Gemini 2.0 Flash — GA legacy, reliable tool calling",                   "Standard"),
        ("mistral-large@latest",          "Mistral Large — Vertex AI Model Garden (MaaS)",                         "Standard"),
    ],
    # NVIDIA NIM — free-tier + paid models via integrate.api.nvidia.com
    # https://integrate.api.nvidia.com — OpenAI-compatible, no data retention on free tier
    "nvidia": [
        ("nvidia/nemotron-3-super-120b-instruct",     "Nemotron 3 Super 120B — 262K context, free tier",         "Free"),
        ("moonshotai/kimi-k2-instruct",               "Kimi K2 — 1T MoE, 128K context, free tier",               "Free"),
        ("minimaxai/minimax-m2",                      "MiniMax M2 via NVIDIA NIM — 456B MoE, 200K context",     "Free"),
        ("meta/llama-3.1-70b-instruct",               "Llama 3.1 70B — open weights, free tier",                 "Free"),
        ("meta/llama-3.1-405b-instruct",              "Llama 3.1 405B — flagship open, free tier",               "Free"),
        ("nvidia/llama-3.3-nemotron-super-49b-v1",    "Nemotron Super 49B v1 — reasoning + tools",               "Free"),
    ],
    # MiniMax M-series — https://platform.minimax.io/docs/guides/models-intro
    # OpenAI-compatible, supports reasoning_split (chain-of-thought isolation)
    # Pricing from https://platform.minimax.io/docs/guides/pricing-paygo (Jun 2026)
    "minimax": [
        # Current Models
        ("MiniMax-M3",               "MiniMax M3 — flagship, 1M context, multimodal, agentic (Jun 2026)",    "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.7",             "MiniMax M2.7 — recursive self-improvement, 200K context",                "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.7-highspeed",   "MiniMax M2.7 Highspeed — 2x faster, same quality",                       "$0.60/$2.40 per MTok"),
        # Legacy Models
        ("MiniMax-M2.5",             "MiniMax M2.5 — SOTA coding/agent, 200K context (Feb 2026)",               "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.5-highspeed",   "MiniMax M2.5 Highspeed — 2x faster, same quality",                       "$0.60/$2.40 per MTok"),
        ("MiniMax-M2.1",             "MiniMax M2.1 — polyglot programming, 200K context (Dec 2025)",           "$0.30/$1.20 per MTok"),
        ("MiniMax-M2.1-highspeed",   "MiniMax M2.1 Highspeed — 2x faster, same quality",                       "$0.60/$2.40 per MTok"),
        ("MiniMax-M2",               "MiniMax M2 — original agentic-era release, 200K context (Oct 2025)",     "$0.30/$1.20 per MTok"),
    ],
    "passthrough": [],  # No models — CVC doesn't call any LLM; tool uses its own key
}


@main.command()
@click.option(
    "--provider",
    type=click.Choice(_setup_provider_choice(), case_sensitive=False),
    default=None,
    help="LLM provider (uses config default if omitted).",
)
@click.option("--model", default="", help="Model override.")
@click.option("--api-key", default="", help="API key override.")
@click.option(
    "--no-think",
    "no_think",
    is_flag=True,
    default=False,
    help=(
        "Disable model reasoning/thinking phase for fastest responses. "
        "Forces MINIMAL (Flash) or LOW (Pro) thinking on Gemini 3 models. "
        "Tradeoff: lower response quality on complex tasks."
    ),
)
@click.option(
    "--allowedTools",
    "allowed_tools",
    multiple=True,
    help="Tool patterns to allow (e.g. 'Bash(npm run *)' or 'read_file'). Repeatable.",
)
@click.option(
    "--disallowedTools",
    "disallowed_tools",
    multiple=True,
    help="Tool patterns to deny (e.g. 'bash' or 'Edit(/secrets/*)'). Repeatable.",
)
@click.option(
    "-p", "--print",
    "print_mode",
    default=None,
    type=str,
    help="Non-interactive mode: send a single prompt and print the response. Exits after.",
)
@click.option(
    "--max-turns",
    "max_turns",
    default=0,
    type=int,
    help="Maximum tool-use turns in non-interactive (--print) mode. 0 = unlimited.",
)
@click.option(
    "-c", "--continue",
    "continue_session",
    is_flag=True,
    default=False,
    help="Resume the most recent session instead of starting fresh.",
)
@click.option(
    "-r", "--resume",
    "resume_id",
    default=None,
    type=str,
    help="Resume a specific session by ID or name.",
)
@click.option(
    "--autopilot",
    "autopilot",
    type=click.Choice(["on", "yolo"], case_sensitive=False),
    default=None,
    help="Start with autopilot enabled: 'on' (persistent) or 'yolo' (full auto).",
)
def agent(provider: str | None, model: str, api_key: str, no_think: bool,
          allowed_tools: tuple[str, ...], disallowed_tools: tuple[str, ...],
          print_mode: str | None, max_turns: int,
          continue_session: bool, resume_id: str | None,
          autopilot: str | None) -> None:
    """Interactive AI coding agent — Claude Code on steroids with Time Machine."""
    from cvc.core.models import GlobalConfig

    gc = GlobalConfig.load()

    # Resolve provider
    prov = provider or gc.provider
    if not prov:
        console.print(
            "[bold red]No provider configured.[/bold red] Run [bold]cvc setup[/bold] first, "
            "or pass [bold]--provider[/bold]."
        )
        raise SystemExit(1)

    # Resolve model
    mdl = model or gc.model or ""

    # Resolve API key
    key = api_key or gc.api_keys.get(prov, "") or ""
    if prov not in ("ollama", "lmstudio") and not key:
        console.print(
            f"[bold red]No API key for {prov}.[/bold red] Run [bold]cvc setup[/bold] first, "
            "or pass [bold]--api-key[/bold]."
        )
        raise SystemExit(1)

    from cvc.agent import run_agent

    run_agent(
        provider=prov,
        model=mdl,
        api_key=key,
        no_think=no_think,
        allowed_tools=list(allowed_tools) if allowed_tools else None,
        disallowed_tools=list(disallowed_tools) if disallowed_tools else None,
        print_mode=print_mode,
        max_turns=max_turns,
        continue_session=continue_session,
        resume_id=resume_id,
        autopilot=autopilot,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Setup
# ═══════════════════════════════════════════════════════════════════════════════


@main.command()
@click.option(
    "--provider",
    type=click.Choice(_setup_provider_choice(), case_sensitive=False),
    prompt=False,
    help="LLM provider (interactive prompt if omitted).",
)
@click.option("--model", default="", help="Model override (uses provider default if empty).")
@click.option("--api-key", default="", help="API key (prompted interactively if omitted).")
def setup(provider: str | None, model: str, api_key: str, first_run: bool = False) -> None:
    """Interactive first-time setup — pick your provider, model, and go."""
    from cvc.adapters import PROVIDER_DEFAULTS
    from cvc.core.models import CVCConfig, GlobalConfig, get_global_config_dir

    # Only show banner if not a first run (first run already showed it)
    if not first_run:
        _banner("Setup Wizard")

    # Set when the user enters the menu loop (existing config). Used
    # below to skip first-run-only prompts (IDE detection, daemon
    # install, manual gateway start). Default = False (first run).
    _entering_menu = False

    # ─── Detect existing configuration ───────────────────────────────────
    gc_file = get_global_config_dir() / "config.json"
    existing_gc = GlobalConfig.load()
    # Only treat as "existing" if the config file actually exists on disk
    # (GlobalConfig has defaults like provider="anthropic", so bool(provider)
    # would always be True even on a fresh install)
    has_existing = gc_file.exists() and bool(existing_gc.provider)

    if has_existing and not provider and not first_run:
        # Show current config summary and let user choose
        _entering_menu = True  # used below to skip first-run-only prompts
        masked_keys = {}
        for prov, key in existing_gc.api_keys.items():
            if key and len(key) > 12:
                masked_keys[prov] = key[:8] + "…" + key[-4:]
            elif key:
                masked_keys[prov] = "●●●●"

        current_info = (
            f"  Provider   [bold #CC3333]{existing_gc.provider}[/bold #CC3333]\n"
            f"  Model      [bold #CC3333]{existing_gc.model}[/bold #CC3333]"
        )
        if masked_keys:
            keys_str = ", ".join(f"{p}: {m}" for p, m in masked_keys.items())
            current_info += f"\n  API Keys   [dim]{keys_str}[/dim]"

        console.print(
            Panel(
                current_info,
                border_style="#5C1010",
                title="[bold #55AA55]Existing Configuration Found[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        console.print()

        from cvc.agent.menus import arrow_select
        setup_options = [
            ("Start Fresh", 1),
            ("Change Provider", 2),
            ("Change Model", 3),
            ("Update API Key", 4),
            ("Reset Everything", 5),
            ("Setup Channels", 6),
            ("Tune Agent Capabilities", 7),
        ]
        setup_descs = [
            "Reconfigure everything from scratch",
            "Switch to a different LLM provider",
            "Keep provider, pick a different model",
            "Replace or add an API key",
            "Delete all config and start over",
            "Configure Telegram / Discord / Slack / WhatsApp / Matrix / Email / Webhook",
            "Edit iteration budgets, timeouts, tenacity, etc.",
        ]


        def _channels_installed_count() -> int:
            """Quick count of how many channels the user has actually
            configured (non-empty config dict in settings)."""
            try:
                from cvc.integrations.bootstrap import get_registry
                reg = get_registry()
                count = 0
                for name in reg.list_names():
                    cfg_path = _channels_config_path_for(name)
                    if cfg_path.exists() and cfg_path.stat().st_size > 0:
                        count += 1
                return count
            except Exception:
                return 0


        channels_installed = _channels_installed_count()
        if channels_installed > 0:
            setup_descs[5] = (
                f"Manage your {channels_installed} configured channel(s) "
                "— Telegram / Discord / Slack / WhatsApp / Matrix / Email / Webhook"
            )
        # OUTER LOOP — the wizard stays alive after each action. The
        # user comes back to this menu until they pick "Done / Exit"
        # (action 8) or hit Ctrl+C at the menu itself. Sub-flows
        # like Channels and Tune Agent Capabilities also return to
        # this menu when they're done (or cancelled). This is the
        # fix for "Ctrl+C should go back to the main options, not
        # out of the wizard entirely".
        while True:
            try:
                action = arrow_select(
                    "What would you like to do?",
                    setup_options,
                    descriptions=setup_descs,
                    default=0,
                )
            except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
                # Ctrl+C at the main menu → leave the wizard cleanly,
                # no traceback. Same as picking "Done / Exit".
                console.print()
                _info("Setup wizard closed.")
                return

            if action is None or action == 8:
                # Esc / "Done / Exit" → leave the wizard cleanly.
                console.print()
                _info("Setup wizard closed.")
                return
            console.print()

            if action == 5:
                # Reset everything
                config_dir = get_global_config_dir()
                config_file = config_dir / "config.json"
                if config_file.exists():
                    config_file.unlink()
                    _success(f"Deleted global config → [dim]{config_file}[/dim]")
                # Reset the existing_gc so the wizard runs fresh
                existing_gc = GlobalConfig()
                _info("Starting fresh setup…")
                console.print()
            elif action == 3:
                # Change model only — jump straight to model selection
                provider = existing_gc.provider
                _success(f"Provider: [bold]{provider}[/bold]  [dim](keeping current)[/dim]")
                console.print()

                defaults = PROVIDER_DEFAULTS[provider]
                chosen_model = existing_gc.model

                console.print("[bold #CC3333]  Pick a new model[/bold #CC3333]")
                console.print()

                if provider == "github":
                    console.print("[dim]Fetching available Copilot models...[/dim]")
                    oauth_token = existing_gc.api_keys.get("github")
                    if not oauth_token:
                        _error("No GitHub Copilot authentication found. Please run 'cvc setup' and choose 'Change Provider' to re-authenticate.")
                        console.print()
                        continue

                    import httpx

                    from cvc.agent.providers.github_auth import fetch_copilot_token
                    token_data = fetch_copilot_token(oauth_token)
                    if not token_data:
                        _error("Failed to fetch Copilot token. You may need an active Copilot subscription, or your auth expired. Please re-authenticate.")
                        console.print()
                        continue

                    copilot_token = token_data.get("token")
                    proxy_ep = token_data.get("endpoints", {}).get("api", "https://api.individual.githubcopilot.com")

                    try:
                        resp = httpx.get(
                            f"{proxy_ep.rstrip('/')}/models",
                            headers={
                                "Authorization": f"Bearer {copilot_token}",
                                "Accept": "application/json",
                                "editor-version": "vscode/1.93.0",
                                "editor-plugin-version": "copilot-chat/0.20.0"
                            },
                            timeout=10.0
                        )
                        resp.raise_for_status()
                        models_data = resp.json().get("data", [])
                        models = []
                        for m in models_data:
                            if m.get("policy", {}).get("state") == "disabled":
                                continue
                            mid = m["id"].lower()
                            if "3.5" in mid or "3-5" in mid or "opus-3" in mid:
                                continue
                            models.append((m["id"], m.get("name", m["id"]), "Copilot Tier"))
                        if not models:
                            _error("No models found for this Copilot account.")
                            console.print()
                            continue
                    except Exception as e:
                        _error(f"Failed to fetch Copilot models: {e}")
                        console.print()
                        continue

                    from cvc.agent.menus import arrow_select
                    m_opts = [(mid, mid) for mid, desc, tier in models]
                    m_descs = [f"{desc} ({tier})" for mid, desc, tier in models]
                    new_model_choice = arrow_select("Pick a model", m_opts, descriptions=m_descs)
                    if new_model_choice is None:
                        console.print("  [bold red]Model selection is required.[/bold red]")
                        console.print()
                        continue
                    chosen_model = new_model_choice

                elif provider == "vertex":
                    # Try to fetch models from user's Vertex AI project using ADC
                    from cvc.adapters.vertex import (
                        VERTEX_MODELS,
                        fetch_vertex_models,
                        get_vertex_credentials,
                    )
                    try:
                        _creds, adc_project = get_vertex_credentials()
                        v_project = existing_gc.vertex_project_id or adc_project
                    except Exception:
                        v_project = existing_gc.vertex_project_id
                    v_location = existing_gc.vertex_location or "us-central1"
                    if v_project:
                        console.print("[dim]Fetching models from your Vertex AI project...[/dim]")
                        fetched = fetch_vertex_models(v_project, v_location, timeout=8.0)
                        models = fetched if fetched else VERTEX_MODELS
                    else:
                        models = VERTEX_MODELS

                    from cvc.agent.menus import arrow_select
                    m_opts = [(mid, mid) for mid, desc, tier in models]
                    m_descs = [f"{desc} ({tier})" for mid, desc, tier in models]
                    new_model_choice = arrow_select("Pick a model", m_opts, descriptions=m_descs)
                    if new_model_choice is None:
                        console.print("  [bold red]Model selection is required.[/bold red]")
                        console.print()
                        continue
                    chosen_model = new_model_choice

                else:
                    models = MODEL_CATALOG.get(provider, [])
                    table = Table(box=box.ROUNDED, border_style="dim", show_header=True, header_style="bold #CC3333")
                    table.add_column("#", style="bold", width=3)
                    table.add_column("Model ID", style="#CC3333")
                    table.add_column("Description")
                    table.add_column("Tier", style="dim", justify="right")
                    table.add_column("", width=3)
                    for i, (mid, desc, tier) in enumerate(models, 1):
                        marker = "[bold #55AA55]●[/bold #55AA55]" if mid == chosen_model else " "
                        table.add_row(str(i), mid, desc, tier, marker)
                    console.print(Panel(table, border_style="#8B0000", title=f"[bold white]{provider.title()} Models[/bold white]", padding=(1, 1)))

                    model_choice = click.prompt("  Enter number or model ID", default="", show_default=False).strip()
                    if model_choice:
                        if model_choice.isdigit() and 1 <= int(model_choice) <= len(models):
                            chosen_model = models[int(model_choice) - 1][0]
                        else:
                            chosen_model = model_choice

                # Save with updated model
                api_keys = dict(existing_gc.api_keys)
                gc = GlobalConfig(
                    provider=provider,
                    model=chosen_model,
                    api_keys=api_keys,
                    vertex_project_id=existing_gc.vertex_project_id,
                    vertex_location=existing_gc.vertex_location,
                )
                gc_path = gc.save()
                _success(f"Model updated to [bold]{chosen_model}[/bold]")
                _success(f"Config saved → [dim]{gc_path}[/dim]")
                console.print()
                continue  # back to the main menu

            elif action == 4:
                # Update API key only
                provider = existing_gc.provider
                _success(f"Provider: [bold]{provider}[/bold]")
                console.print()

                defaults = PROVIDER_DEFAULTS[provider]
                env_key = defaults.get("env_key", "")
                if not env_key:
                    # Fallback for providers not in PROVIDER_DEFAULTS (catalog-only
                    # providers like zai, kimi, stepfun, alibaba, …): read the
                    # primary env var from the CVC ProviderProfile instead.
                    try:
                        from cvc.providers.hermes_catalog import env_key_for_provider
                        env_key = env_key_for_provider(provider)
                    except Exception:
                        env_key = ""

                if provider in ("ollama", "lmstudio"):
                    _success(f"{provider.title()} doesn't need an API key — it runs locally!")
                    console.print()
                    continue

                key_urls = {
                    "anthropic": "https://console.anthropic.com/settings/keys",
                    "openai": "https://platform.openai.com/api-keys",
                    "google": "https://aistudio.google.com/apikey",
                }
                url = key_urls.get(provider, "")
                if url:
                    console.print(f"  [dim]Get your key →[/dim] [bold underline]{url}[/bold underline]")
                    console.print()

                new_key = click.prompt("  Paste your new API key", hide_input=True).strip()
                if new_key:
                    api_keys = dict(existing_gc.api_keys)
                    api_keys[provider] = new_key
                    gc = GlobalConfig(provider=provider, model=existing_gc.model, api_keys=api_keys)
                    gc_path = gc.save()
                    _success("API key updated!")
                    _success(f"Config saved → [dim]{gc_path}[/dim]")
                else:
                    _warn("No key entered. Nothing changed.")
                console.print()
                continue  # back to the main menu

            elif action == 6:
                # Setup / manage Channels — Telegram, Discord, Slack,
                # WhatsApp, Matrix, Email, Webhook. The user picks a channel
                # from a submenu, then gets prompts driven by the adapter's
                # config_schema. Saved config is written to
                # ``~/.cvc/channels/<name>.yaml`` and picked up by the
                # gateway on next start.
                #
                # Ctrl+C / Escape at any sub-prompt → return to the
                # MAIN menu (which is now wrapped in a loop), not to
                # the terminal. That's what makes the wizard feel
                # safe: cancellation unwinds one level, not all the
                # way out.
                try:
                    console.print("[bold #CC3333]  Channels[/bold #CC3333]")
                    console.print(
                        "  [dim]Every inbound channel message becomes a CVC cognitive commit. "
                        "Configure any one — or several — to talk to CVC from there.[/dim]"
                    )
                    console.print()

                    from cvc.integrations.setup import (
                        list_channels_for_setup,
                        run_channel_setup,
                        channels_config_path as _channels_config_path_for,
                        read_channels_config_from_path as _read_channels_config,
                        save_channels_config_to_path as _save_channels_config_to_path,
                        save_channels_config as _save_channels_config,
                        schema_for as _schema_for,
                        truncate_for_display as _truncate_for_display,
                        WizardCancelled as _WizardCancelled,
                    )

                    channels = list_channels_for_setup()
                    if not channels:
                        _warn("No channels are registered. Check the gateway logs for import errors.")
                        console.print()
                        continue

                    # Submenu: pick a channel, or back out.
                    # IMPORTANT: do NOT pass channel descriptions here.
                    chan_options = [(f"{display}  [dim]({name})[/dim]", name)
                                    for name, display, _ in channels]
                    from cvc.agent.menus import arrow_select as _arrow_select
                    chan_options_full = [("← Back to main menu", "__back__")] + chan_options

                    while True:
                        console.print()
                        try:
                            chosen = _arrow_select(
                                "Which channel do you want to set up?",
                                chan_options_full,
                                descriptions=None,
                                default=0,
                            )
                        except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
                            _info("Cancelled — returning to main menu.")
                            console.print()
                            break  # exit channel sub-loop, then `continue` outer

                        if chosen is None or chosen == "__back__":
                            _info("Returning to main menu.")
                            console.print()
                            break

                        console.print()
                        display = next((d for n, d, _ in channels if n == chosen), chosen)
                        desc = next((d for n, _, d in channels if n == chosen), "")
                        if desc:
                            console.print(f"  [dim]{desc}[/dim]")
                            console.print()
                        console.print(f"[bold #CC3333]  {display} setup[/bold #CC3333]")
                        console.print()

                        cfg_path = _channels_config_path_for(chosen)
                        existing = _read_channels_config(cfg_path)
                        if existing:
                            masked_keys = sorted(k for k in existing if any(
                                s.get("secret") and s["key"] == k for s in _schema_for(chosen)
                            ))
                            _info(f"Existing config: [dim]{cfg_path}[/dim]")
                            for k, v in existing.items():
                                marker = " ●●●●" if k in masked_keys else ""
                                _info(f"  • {k}: {_truncate_for_display(v)}{marker}")
                            console.print()
                            try:
                                reconfigure = click.confirm(
                                    f"  Reconfigure {display}?",
                                    default=False,
                                )
                            except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
                                _info("Cancelled — returning to main menu.")
                                console.print()
                                break
                            if not reconfigure:
                                _info(f"  Keeping existing {display} config.")
                                console.print()
                                continue

                        try:
                            cfg = run_channel_setup(chosen, existing=existing or None)
                        except (_WizardCancelled, KeyboardInterrupt, EOFError):
                            _info("Cancelled — returning to main menu.")
                            console.print()
                            break
                        if not cfg:
                            _warn(f"No configuration captured for {chosen}.")
                            console.print()
                            continue

                        try:
                            _save_channels_config_to_path(cfg_path, cfg)
                            _success(
                                f"{display} settings saved → [dim]{cfg_path}[/dim]"
                            )
                            try:
                                from cvc.agent.settings import save_project_settings
                                save_project_settings(Path.home(), f"channels.{chosen}.enabled", True)
                                _info(
                                    f"Channel [bold]{chosen}[/bold] is now [bold green]enabled[/bold green] "
                                    f"for the next gateway start."
                                )
                            except Exception as e:  # noqa: BLE001
                                _warn(f"Could not flip the enable flag automatically: {e}")
                        except Exception as e:  # noqa: BLE001
                            _error(f"Failed to save {chosen} config: {e}")
                        console.print()
                except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
                    # Catch-all: stray Ctrl+C at any depth → back to menu.
                    _info("Cancelled — returning to main menu.")
                    console.print()
                continue

            elif action == 7:
                # Tune Agent Capabilities — interactive editor for every tunable.
                from cvc.core.agent_config import (
                    CvcAgentConfig,
                    TUNABLES,
                    reload_agent_config,
                    sections,
                )

                cfg = CvcAgentConfig.load()
                console.print(
                    Panel(
                        f"[bold white]Tune every agent tunable. Press [bold #CC3333]Enter[/bold #CC3333] to keep the current value.[/bold white]\n"
                        f"[dim]Config file: {cfg.path()}[/dim]",
                        border_style="#8B0000",
                        padding=(0, 2),
                    )
                )
                console.print()

                from rich.prompt import Prompt
                modified = False
                for section_label, field_names in sections():
                    console.print(f"[bold #CC3333]  {section_label}[/bold #CC3333]")
                    for fname in field_names:
                        meta = TUNABLES[fname]
                        current = getattr(cfg, fname)
                        rng = ""
                        if meta.minimum is not None or meta.maximum is not None:
                            lo = "" if meta.minimum is None else f"{meta.minimum:g}"
                            hi = "" if meta.maximum is None else f"{meta.maximum:g}"
                            rng = f" [dim]({lo}–{hi})[/dim]"
                        console.print(f"    [dim]{meta.help}[/dim]")
                        while True:
                            raw = Prompt.ask(
                                f"    [white]{meta.label}[/white]{rng}",
                                default=str(current),
                                show_default=True,
                            ).strip()
                            if raw == "" or raw == str(current):
                                break
                            try:
                                cfg.set_field(fname, raw)
                                modified = True
                                break
                            except ValueError as exc:
                                console.print(f"      [red]✗ {exc}[/red]")
                    console.print()

                if modified:
                    saved = cfg.save()
                    _success(f"Saved → [dim]{saved}[/dim]")
                    # Hot-reload in the running process (if gateway is in-proc).
                    try:
                        reload_agent_config()
                        from cvc.gateway import _refresh_agent_budgets
                        _refresh_agent_budgets()
                    except Exception:
                        pass
                    _info("Restart the gateway (cvc gateway) to apply changes everywhere.")
                else:
                    _info("No changes made.")
                console.print()
                continue

            elif action == 2:
                # Change provider — break out of the menu loop and fall
                # through to the full wizard below. Setting provider=None
                # makes the wizard's "if not provider:" branch fire the
                # provider picker (the very thing the user came here for).
                provider = None  # Will prompt for provider below
                # Preserve existing api_keys so the wizard only asks for the
                # new provider's key (it overwrites existing_gc.api_keys
                # with the same dict). Without this, the wizard would
                # silently drop keys for other providers.
                _info("Select a new provider below…")
                console.print()
                break  # exit the menu loop, fall into the wizard below

            elif action == 1:
                # Start Fresh — same fall-through as Change Provider, but
                # the wizard will also reset api_keys (full wipe).
                _info("Starting fresh setup — clearing existing API keys…")
                console.print()
                break  # exit the menu loop, fall into the wizard below

            # action == 1 (Start Fresh) or action == 2 (Change Provider)
            # both `break` out above and fall through to the full wizard below

        console.print(
            Panel(
                "[bold white]This wizard will configure CVC in 5 quick steps.[/bold white]\n"
                "Your settings are saved globally — works across all projects.",
                border_style="#8B0000",
                padding=(0, 2),
            )
        )
        console.print()

        # ─── Capability tour: show users every CVC feature so nothing is hidden ──
        if first_run or os.environ.get("CVC_SETUP_SHOW_TOUR", "1") != "0":
            from cvc.setup import list_feature_specs
            from cvc.setup.features import feature_categories

            feats = list_feature_specs()
            cats = feature_categories()
            cat_titles = {
                "core":          "🧠 Core",
                "agent":         "🤖 Agent",
                "hive":          "👑 Hive (Core 4 Team)",
                "dashboard":     "🖥  Dashboard",
                "mcp":           "🔌 MCP / IDE",
                "integration":   "🔗 Integrations",
                "observability": "📡 Observability",
            }
            tour_lines = []
            for cat in cats:
                title = cat_titles.get(cat, cat.capitalize())
                tour_lines.append(f"[bold #CC3333]{title}[/bold #CC3333]")
                for f in feats:
                    if f.category != cat:
                        continue
                    marker = "●" if f.default_enabled else "○"
                    tour_lines.append(f"  [#55AA55]{marker}[/#55AA55] [bold]{f.name}[/bold] — [dim]{f.description}[/dim]")
                tour_lines.append("")
            console.print(
                Panel(
                    "\n".join(tour_lines).rstrip(),
                    border_style="#2A5C2A",
                    title=f"[bold #55AA55]Everything CVC ships with — {len(feats)} capabilities[/bold #55AA55]",
                    padding=(1, 2),
                )
            )
            console.print(
                "[dim]All features above are installed.  This wizard configures the LLM provider; "
                "the rest light up automatically as you use them.  Set "
                "[bold]CVC_SETUP_SHOW_TOUR=0[/bold] to hide this overview.[/dim]"
            )
            console.print()

    # ─── Step 1: Provider Selection ──────────────────────────────────────
    console.print("[bold #CC3333]  STEP 1 of 5[/bold #CC3333]  [bold white]Choose your LLM provider[/bold white]")
    console.print()

    if not provider:
        # ── Single source of truth: cvc/setup/registry.py ──
        # Adding a new provider there makes it appear here automatically.
        from cvc.setup import list_provider_specs_all
        from cvc.agent.menus import arrow_select

        # Show ALL providers — hand-written PLUS the ~25 Hermes-catalog
        # providers wrapped via cvc.providers.hermes_catalog. The user
        # sees one unified menu, no separate "advanced" submenu.
        specs = list_provider_specs_all()

        # Minimal one-line-per-provider rendering. Each option is just:
        #   <Display Name>  ⭐  free
        # No inline descriptions — they wrap and obscure how many providers exist.
        # Description for the highlighted provider is shown below the menu via
        # arrow_select's footer hint (one row, fixed height, no wrapping).
        prov_options = []
        prov_descs = []
        for s in specs:
            badges = []
            if s.recommended:
                badges.append("⭐")
            if s.free_tier:
                badges.append("free")
            if s.local:
                badges.append("local")
            label = s.display_name
            if badges:
                label = f"{label}  {' · '.join(badges)}"
            prov_options.append((label, s.key))
            prov_descs.append("")  # suppress inline description — keeps each provider on its own line

        provider = arrow_select(
            f"Choose your LLM provider  ({len(specs)} available)",
            prov_options,
            descriptions=prov_descs,
        )
        if provider is None:
            return

    _success(f"Provider: [bold]{provider}[/bold]")
    console.print()

    defaults = PROVIDER_DEFAULTS.get(provider, {})
    chosen_model = model or defaults.get("model", "")

    # ─── Passthrough: skip model/key steps — just save config and done ───
    if provider == "passthrough":
        console.print(
            Panel(
                "  [bold #55AA55]Passthrough mode selected.[/bold #55AA55]\n\n"
                "  CVC will capture all AI conversations and save them to [bold].cvc/[/bold]\n"
                "  [bold]without[/bold] needing its own API key.\n\n"
                "  Your AI tool (Claude Code, Copilot, etc.) uses its own\n"
                "  subscription or API key as normal.\n\n"
                "  [dim]CVC agent features (cvc agent, semantic merge) require\n"
                "  a provider configured later via [bold]cvc setup[/bold].[/dim]",
                border_style="#2A5C2A",
                title="[bold #55AA55]Passthrough Mode[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        console.print()

        # Skip to Step 4 (Telegram) — save passthrough config
        _success("Provider: [bold]passthrough[/bold]")
        _success("No API key required!")
        console.print()

        # Jump straight to save
        gc_existing = GlobalConfig.load()
        gc = GlobalConfig(
            provider="passthrough",
            model="",
            api_keys=dict(gc_existing.api_keys),
        )
        gc_path = gc.save()
        _success(f"Global config saved → [dim]{gc_path}[/dim]")
        config = CVCConfig.for_project(project_root=Path.cwd(), provider="passthrough", model="")
        config.ensure_dirs()
        from cvc.core.database import ContextDatabase
        ContextDatabase(config)
        _success(f"Project initialised → [dim]{config.cvc_root}[/dim]")
        console.print()
        console.print(
            Panel(
                "  [#CC3333]$[/#CC3333] cvc launch claude      [dim]# Launch Claude Code through CVC[/dim]\n"
                "  [#CC3333]$[/#CC3333] cvc launch aider        [dim]# Launch Aider through CVC[/dim]\n"
                "  [#CC3333]$[/#CC3333] cvc gateway start       [dim]# Start CVC Gateway manually[/dim]\n"
                "  [#CC3333]$[/#CC3333] cvc log                 [dim]# See captured conversations[/dim]\n\n"
                "  To enable CVC's own AI features later:\n"
                "  [#CC3333]$[/#CC3333] cvc setup --provider anthropic",
                border_style="#2A5C2A",
                title="[bold #55AA55]✓ Ready — Run cvc launch to start[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        console.print()
        return

    # ─── Step 2: Model Selection ─────────────────────────────────────────
    if provider == "github":
        console.print("[bold #CC3333]  STEP 2 of 5[/bold #CC3333]  [bold white]Authentication[/bold white]")
        console.print()
        console.print("[bold cyan]Authenticating with GitHub Copilot to fetch available models...[/bold cyan]")
        import httpx

        from cvc.agent.providers.github_auth import fetch_copilot_token, perform_device_flow

        oauth_token = perform_device_flow()
        if not oauth_token:
            _error("GitHub Copilot authentication failed.")
            return

        console.print()
        console.print("[bold #CC3333]  STEP 3 of 5[/bold #CC3333]  [bold white]Pick a model[/bold white]")
        console.print()
        console.print("[dim]Fetching available Copilot models...[/dim]")
        token_data = fetch_copilot_token(oauth_token)
        if not token_data:
            _error("Failed to fetch Copilot token. You may need an active Copilot subscription.")
            return

        copilot_token = token_data.get("token")
        proxy_ep = token_data.get("endpoints", {}).get("api", "https://api.individual.githubcopilot.com")

        try:
            resp = httpx.get(
                f"{proxy_ep.rstrip('/')}/models",
                headers={
                    "Authorization": f"Bearer {copilot_token}",
                    "Accept": "application/json",
                    "editor-version": "vscode/1.93.0",
                    "editor-plugin-version": "copilot-chat/0.20.0"
                },
                timeout=10.0
            )
            resp.raise_for_status()
            models_data = resp.json().get("data", [])
            models = []
            for m in models_data:
                if m.get("policy", {}).get("state") == "disabled":
                    continue
                mid = m["id"].lower()
                if "3.5" in mid or "3-5" in mid or "opus-3" in mid:
                    continue
                models.append((m["id"], m.get("name", m["id"]), "Copilot Tier"))
            if not models:
                _error("No models found for this Copilot account.")
                return
        except Exception as e:
            _error(f"Failed to fetch Copilot models: {e}")
            return

        api_key = oauth_token

    elif provider == "vertex":
        # ── Vertex AI — authenticate via gcloud ADC, auto-detect project ──
        console.print("[bold #CC3333]  STEP 2 of 5[/bold #CC3333]  [bold white]Google Cloud Authentication[/bold white]")
        console.print()
        console.print(
            Panel(
                "  Vertex AI uses [bold]Google Cloud Application Default Credentials[/bold].\n\n"
                "  CVC will check if you're already authenticated via gcloud.\n"
                "  If not, it will open a browser for you to log in.\n\n"
                "  [dim]Prerequisite:[/dim] [bold]gcloud[/bold] CLI must be installed.\n"
                "  [bold underline]https://cloud.google.com/sdk/docs/install[/bold underline]",
                border_style="#4285F4",
                title="[bold #4285F4]Google Cloud Setup[/bold #4285F4]",
                padding=(1, 2),
            )
        )
        console.print()

        # Check if gcloud is installed
        import shutil
        if not shutil.which("gcloud"):
            _error(
                "gcloud CLI not found. Install it from:\n"
                "  https://cloud.google.com/sdk/docs/install"
            )
            return

        # Try to get existing ADC credentials
        from cvc.adapters.vertex import VERTEX_MODELS, fetch_vertex_models, get_vertex_credentials
        try:
            creds, adc_project = get_vertex_credentials()
            _success(f"Already authenticated!  Project: [bold]{adc_project or '(not set)'}[/bold]")
        except RuntimeError:
            # Need to login — run gcloud auth application-default login
            _info("No credentials found. Opening browser to log in...")
            console.print()
            import subprocess
            result = subprocess.run(
                ["gcloud", "auth", "application-default", "login"],
                capture_output=False,
                            **HIDDEN_KW,
            )
            if result.returncode != 0:
                _error("Authentication failed. Please try again.")
                return
            try:
                creds, adc_project = get_vertex_credentials()
                _success(f"Authenticated!  Project: [bold]{adc_project or '(not set)'}[/bold]")
            except RuntimeError as exc:
                _error(str(exc))
                return

        vertex_project_id = adc_project
        if not vertex_project_id:
            vertex_project_id = click.prompt("  Enter your GCP Project ID").strip()
            if not vertex_project_id:
                _error("Project ID is required for Vertex AI.")
                return

        vertex_location_input = click.prompt(
            "  Enter your GCP region/location",
            default="us-central1",
            show_default=True,
        ).strip()
        vertex_location = vertex_location_input or "us-central1"

        _success(f"Project: [bold]{vertex_project_id}[/bold]  Location: [bold]{vertex_location}[/bold]")
        console.print()

        console.print("[bold #CC3333]  STEP 3 of 5[/bold #CC3333]  [bold white]Pick a model[/bold white]")
        console.print()

        console.print("[dim]Fetching models from your Vertex AI project...[/dim]")
        fetched = fetch_vertex_models(vertex_project_id, vertex_location, timeout=8.0)
        if fetched:
            models = fetched
            _success(f"Found [bold]{len(models)}[/bold] models in your Vertex AI project")
        else:
            models = VERTEX_MODELS
            _info("Could not auto-fetch models — showing curated Vertex AI model list")
        console.print()

        # No API key needed — ADC handles auth
        api_key = ""

    else:
        console.print("[bold #CC3333]  STEP 2 of 5[/bold #CC3333]  [bold white]Pick a model[/bold white]")
        console.print()
        # Look up model list: legacy hardcoded MODEL_CATALOG first, then
        # Hermes catalog fallback for providers added via cvc.providers.hermes_catalog
        # (zai, kimi, stepfun, alibaba, arcee, gmi, ollama-cloud, …).
        models = MODEL_CATALOG.get(provider, [])
        if not models and provider not in ("passthrough",):
            try:
                from cvc.providers.hermes_catalog import models_for_provider
                catalog_models = models_for_provider(provider, limit=20)
                if catalog_models:
                    models = [(m, m, "Catalog") for m in catalog_models]
            except Exception:
                pass

    if provider != "github":
        table = Table(
            box=box.ROUNDED,
            border_style="dim",
            show_header=True,
            header_style="bold #CC3333",
        )
        table.add_column("#", style="bold", width=3)
        table.add_column("Model ID", style="#CC3333")
        table.add_column("Description")
        table.add_column("Tier", style="dim", justify="right")
        table.add_column("", width=3)

        for i, (mid, desc, tier) in enumerate(models, 1):
            # Don't pre-select any model for first-time users
            marker = " "
            table.add_row(str(i), mid, desc, tier, marker)

        console.print(
            Panel(table, border_style="#8B0000", title=f"[bold white]{provider.title()} Models[/bold white]", padding=(1, 1))
        )

    if not model and models:
        from cvc.agent.menus import arrow_select
        m_opts = [(mid, mid) for mid, desc, tier in models]
        m_descs = [f"{desc} ({tier})" for mid, desc, tier in models]
        chosen_model = arrow_select("Pick a model", m_opts, descriptions=m_descs)
        if chosen_model is None:
            console.print("  [bold red]Model selection is required.[/bold red]")
            return
    elif not model and not models and provider not in ("passthrough",):
        # Catalog lookup returned nothing (provider like arcee/azure-foundry
        # doesn't publish models.dev; the user knows their model id).
        # Fall back to the registered provider default, or prompt for free input.
        default = ""
        try:
            from cvc.providers.hermes_catalog import registry_snapshot_for_dashboard
            snap = registry_snapshot_for_dashboard(force_refresh=False)
            for prov in snap.get("providers", []):
                if prov.get("id") == provider and prov.get("models"):
                    default = prov["models"][0].get("id", "")
                    break
        except Exception:
            pass
        if not default:
            try:
                from cvc.providers.base import get_provider
                prof = get_provider(provider)
                if prof and prof.fallback_models:
                    default = prof.fallback_models[0]
            except Exception:
                pass
        typed = click.prompt(
            "  No catalog models for this provider — type the model id to use",
            default=default,
            show_default=bool(default),
        ).strip()
        if not typed:
            console.print("  [bold red]Model selection is required.[/bold red]")
            return
        chosen_model = typed

    _success(f"Model: [bold]{chosen_model}[/bold]")
    console.print()

    # ─── Step 3: API Key ─────────────────────────────────────────────────
    if provider not in ("github", "vertex"):
        # github: OAuth token collected above; vertex: key already collected in Step 2 flow
        console.print("[bold #CC3333]  STEP 3 of 5[/bold #CC3333]  [bold white]API Key[/bold white]")
        console.print()

        env_key = defaults.get("env_key", "")
        if not env_key:
            # Fallback for providers not in PROVIDER_DEFAULTS (catalog-only
            # providers like zai, kimi, stepfun, alibaba, …): read the
            # primary env var from the CVC ProviderProfile instead.
            try:
                from cvc.providers.hermes_catalog import env_key_for_provider
                env_key = env_key_for_provider(provider)
            except Exception:
                env_key = ""

        if provider == "ollama":
            _success("No API key needed for Ollama — it runs locally!")
            console.print()
            console.print(
                Panel(
                    f"Ollama runs automatically in the background on Windows/macOS.\n"
                    f"Just make sure the model is downloaded:\n\n"
                    f"  [#CC3333]$[/#CC3333] ollama pull {chosen_model}\n\n"
                    f"[dim]Linux only:[/dim] if Ollama isn't running as a service, start it with:\n"
                    f"  [dim]$ ollama serve[/dim]",
                    border_style="#6B2020",
                    title="[bold #AA6666]Local Setup — Ollama[/bold #AA6666]",
                    padding=(1, 2),
                )
            )
        elif provider == "lmstudio":
            _success("No API key needed for LM Studio — it runs locally!")
            console.print()
            console.print(
                Panel(
                    f"Make sure LM Studio is running with a model loaded:\n\n"
                    f"  1. Open LM Studio\n"
                    f"  2. Go to [bold]Developer → Local Server[/bold]\n"
                    f"  3. Load model [bold]{chosen_model}[/bold] and click [bold]Start Server[/bold]\n"
                    f"  4. Default URL: http://localhost:1234",
                    border_style="#6B2020",
                    title="[bold #AA6666]Local Setup — LM Studio[/bold #AA6666]",
                    padding=(1, 2),
                )
            )
        else:
            # Check env var first
            env_val = os.environ.get(env_key, "") if env_key else ""
            # Then check saved config
            from cvc.core.models import GlobalConfig as GC_Check
            existing_gc = GC_Check.load()
            saved_key = existing_gc.api_keys.get(provider, "")

            if api_key:
                # Passed via --api-key flag
                pass
            elif env_val:
                masked = env_val[:8] + "…" + env_val[-4:]
                _success(f"Found in environment: [bold]{env_key}[/bold] ({masked})")
                console.print("  [dim]Using environment variable — no need to enter it again.[/dim]")
                api_key = ""  # Don't store; env takes precedence
            elif saved_key:
                masked = saved_key[:8] + "…" + saved_key[-4:]
                _success(f"Found saved key ({masked})")
                console.print("  [dim]Using previously saved key. Press Enter to keep it.[/dim]")

                new_key = click.prompt(
                    "  Paste new key (or Enter to keep existing)",
                    default="",
                    hide_input=True,
                    show_default=False,
                ).strip()

                api_key = new_key if new_key else saved_key
            else:
                _warn(f"No API key found for [bold]{provider}[/bold]")

                # Provider-specific instructions
                key_urls = {
                    "anthropic": "https://console.anthropic.com/settings/keys",
                    "openai": "https://platform.openai.com/api-keys",
                    "google": "https://aistudio.google.com/apikey",
                }
                url = key_urls.get(provider, "")
                console.print()
                if url:
                    console.print(f"  [dim]Get your key →[/dim] [bold underline]{url}[/bold underline]")
                console.print()

                if not api_key:
                    api_key = click.prompt(
                        "  Paste your API key",
                        hide_input=True,
                    ).strip()

                if api_key:
                    _success("API key saved!")
                else:
                    _warn("No key entered. You can set it later via env var or re-run setup.")

        console.print()

    # ─── Step 4: Telegram Integration (Optional) ─────────────────────────
    console.print("[bold #CC3333]  STEP 4 of 5[/bold #CC3333]  [bold white]Telegram Integration (Optional)[/bold white]")
    console.print()

    tg_enabled = False
    tg_token = ""
    tg_allowed = []

    # Canonical source-of-truth: ``~/.cvc/channels/telegram.yaml``.
    # This is the per-user file CVC creates on a fresh install — every
    # user who runs ``cvc setup`` writes their bot token there. It is
    # project-isolated (in $HOME), so distributing the CVC package never
    # leaks any user's secret.
    #
    # For backwards compatibility with older CVC versions that wrote to
    # ``<project>/.env`` (a leak bug), we also check that legacy file.
    # If found, we migrate it to the canonical location on the spot and
    # delete the .env entry. This protects any user who installed an
    # older CVC version from being stuck with a broken setup.
    from cvc.integrations.setup import (
        read_channels_config as _read_ch_cfg,
        save_channels_config as _save_ch_cfg,
    )

    tg_already_configured = False
    existing_user_tg = _read_ch_cfg("telegram")
    if existing_user_tg.get("bot_token") and existing_user_tg.get("allowlist"):
        tg_already_configured = True
        _success(
            "Telegram is already configured! "
            "[dim](~/.cvc/channels/telegram.yaml)[/dim]"
        )
    else:
        # Legacy migration path — old CVC versions wrote to
        # ``<project>/.env``. Pull the values out, save them to the
        # canonical channels file, and remove the .env entries. The
        # .env file itself is left in place (other keys may live there)
        # but the Telegram secrets are scrubbed from it.
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            try:
                content = env_path.read_text(encoding="utf-8")
                legacy_token = None
                legacy_users = None
                kept_lines: list[str] = []
                for line in content.splitlines():
                    if line.startswith("TELEGRAM_BOT_TOKEN="):
                        legacy_token = line.split("=", 1)[1].strip()
                    elif line.startswith("TELEGRAM_ALLOWED_USERS="):
                        legacy_users = line.split("=", 1)[1].strip()
                    else:
                        kept_lines.append(line)
                if legacy_token and legacy_users:
                    users = [
                        int(x.strip())
                        for x in legacy_users.split(",")
                        if x.strip().isdigit()
                    ]
                    if users:
                        _save_ch_cfg(
                            "telegram",
                            {
                                "bot_token": legacy_token,
                                "allowlist": [str(u) for u in users],
                                "parse_mode": "markdownv2",
                                "stream_edits": True,
                            },
                        )
                        # Scrub the secrets from .env but leave other keys.
                        env_path.write_text(
                            "\n".join(kept_lines) + "\n", encoding="utf-8"
                        )
                        _success(
                            "Migrated Telegram config from legacy .env → "
                            "[dim]~/.cvc/channels/telegram.yaml[/dim]"
                        )
                        tg_already_configured = True
            except Exception as _mig_exc:  # noqa: BLE001
                logging.warning("legacy .env migration failed: %s", _mig_exc)


    if not tg_already_configured:
        console.print("  [dim]You can connect a Telegram bot to control CVC remotely.[/dim]")
        tg_enabled = click.confirm("  Do you want to set up Telegram integration now?", default=False)

        if tg_enabled:
            console.print("  [dim]1. Message @BotFather on Telegram to create a bot[/dim]")
            console.print("  [dim]2. Copy the HTTP API Token[/dim]")
            tg_token = click.prompt("  Paste Bot Token", hide_input=True).strip()

            console.print()
            console.print("  [dim]To restrict access, CVC needs your numeric Telegram User ID.[/dim]")
            console.print("  [dim]You can get it by messaging @raw_data_bot or @userinfobot on Telegram.[/dim]")
            users_input = click.prompt("  Enter your numeric User ID", default="").strip()
            if users_input:
                for x in users_input.split(","):
                    x = x.strip()
                    if x.isdigit():
                        tg_allowed.append(int(x))
            if tg_token and tg_allowed:
                _success("Telegram configuration collected!")
            else:
                _warn("Incomplete Telegram configuration. Integration will be disabled.")
                tg_enabled = False
    # Build api_keys dict: preserve existing keys, update current provider
    gc_existing = GlobalConfig.load()
    api_keys = dict(gc_existing.api_keys)  # Copy existing
    if api_key:
        api_keys[provider] = api_key

    gc = GlobalConfig(
        provider=provider,
        model=chosen_model,
        api_keys=api_keys,
        vertex_project_id=locals().get("vertex_project_id", gc_existing.vertex_project_id),
        vertex_location=locals().get("vertex_location", gc_existing.vertex_location),
    )
    gc_path = gc.save()
    _success(f"Global config saved → [dim]{gc_path}[/dim]")

    # ── v3.1.0 — Mirror the GlobalConfig to ~/.cvc/config.yaml so the
    # gateway's unified-core chat (which reads from `config.yaml`)
    # actually picks up the provider/model the user just selected. This
    # closes the gap where `cvc setup` wrote to `config.json` and the
    # gateway never saw the new values. We preserve any pre-existing
    # gateway-specific keys (e.g. `telegram`, `skills.external_dirs`)
    # and only update the provider/model fields.
    _sync_global_to_gateway_yaml(provider, chosen_model, api_keys)

    # Initialise .cvc in current directory
    config = CVCConfig.for_project(project_root=Path.cwd(), provider=provider, model=chosen_model)
    config.ensure_dirs()

    from cvc.core.database import ContextDatabase
    ContextDatabase(config)
    _success(f"Project initialised → [dim]{config.cvc_root}[/dim]")

    # ── Phase 1B: chat-channel intent prompt ─────────────────────────
    #
    # If the user didn't configure a channel inside the wizard
    # (e.g. they only set up provider/model/API-key, or the wizard
    # ran non-interactively), offer it as the very next step before
    # any IDE-install or first-run-only flow. The question lives
    # AFTER the summary panel so it doesn't interrupt the "CVC is
    # Ready" celebration — but BEFORE any auto-install/launch
    # prompts so the user knows channels exist at all.
    #
    # Why now and not later: 80% of new users want a chat channel
    # (Telegram especially), and they don't know to look for it
    # inside "cvc setup → Setup Channels". Surfacing the choice
    # here is the difference between "easy install" and "I have
    # to read the docs to figure out channels exist".
    if not tg_enabled:
        try:
            from cvc.integrations.setup import (
                list_channels_for_setup,
                channels_config_path,
            )
            configured_channels = [
                name for name, _, _ in list_channels_for_setup()
                if channels_config_path(name).exists()
                and channels_config_path(name).stat().st_size > 0
            ]
        except Exception:
            configured_channels = []

        if not configured_channels:
            console.print()
            console.print(
                Panel(
                    "[bold white]Talk to CVC from anywhere.[/bold white]\n\n"
                    "CVC can plug into Telegram, Discord, Slack, WhatsApp, "
                    "Matrix, Email, and Webhooks. Every channel is one command "
                    "away — and a chat channel is the easiest way to use CVC "
                    "from your phone.\n\n"
                    "[dim]Recommended for first-time users: Telegram. Free, "
                    "5-minute setup, works everywhere.[/dim]",
                    border_style="#8B0000",
                    title="[bold #CC3333]Set up a chat channel?[/bold #CC3333]",
                    padding=(1, 2),
                )
            )
            try:
                want_channel = click.confirm(
                    "  Configure a chat channel now?",
                    default=True,
                )
            except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
                want_channel = False

            if want_channel:
                # Hand off to channel-setup. We don't call it as a
                # subprocess — invoking the Click command directly
                # keeps the user in the same terminal, same Rich
                # console, same theme. ``standalone_mode=False``
                # prevents Click from calling sys.exit() so we can
                # return control here for the post-setup flow.
                try:
                    from cvc.cli import channel_setup_cmd
                    # Build a fresh Click context so flags resolve
                    # cleanly even though we're not in a top-level
                    # invocation.
                    _ctx = click.Context(channel_setup_cmd)
                    _ctx.invoked_subcommand = None
                    # No channel arg → user gets the interactive picker.
                    channel_setup_cmd.main(
                        args=[],
                        standalone_mode=False,
                    )
                except click.exceptions.Exit as _exit_exc:
                    # Channel-setup returned a non-zero exit code
                    # (e.g. user cancelled at the picker, or
                    # validation failed). Don't abort the rest of
                    # the setup — just skip the rest of the
                    # channel flow and continue.
                    if _exit_exc.exit_code != 0:
                        _info(
                            "Channel setup exited; you can re-run "
                            "anytime with `cvc channel-setup <name>`."
                        )
                except Exception as _chan_exc:  # noqa: BLE001
                    # Don't let a bug in channel-setup break the
                    # rest of cvc setup. Log and continue.
                    _warn(
                        f"Channel setup encountered an issue: {_chan_exc}\n"
                        "You can run `cvc channel-setup <name>` yourself later."
                    )
            else:
                _info(
                    "No problem — run `cvc channel-setup telegram` "
                    "(or any channel) anytime to add one."
                )

    if tg_enabled and tg_token and tg_allowed:
        from cvc.agent.settings import save_project_settings
        # Save enabled flag globally so it applies everywhere
        save_project_settings(Path.home(), "telegram.enabled", True)
        save_project_settings(Path.cwd(), "telegram.enabled", True)

        # Save SECRETS to the canonical per-user channels file, NOT to
        # ``<project>/.env``. Writing secrets to a project-root .env was
        # a leak bug — it would ship with the project on any clone or
        # distribution. The canonical location is ``~/.cvc/channels/<name>.yaml``
        # (per-user, isolated from any project). The gateway loads this
        # file at startup and the registry-driven Telegram adapter reads
        # it from there.
        from cvc.integrations.setup import save_channels_config as _save_ch
        _channels_path = _save_ch(
            "telegram",
            {
                "bot_token": tg_token,
                "allowlist": [str(u) for u in tg_allowed],
                "parse_mode": "markdownv2",
                "stream_edits": True,
            },
        )
        _success(
            "Telegram integration settings saved! "
            f"Secrets stored at [dim]{_channels_path}[/dim]"
        )

    console.print()

    # ─── Summary ─────────────────────────────────────────────────────────
    key_display = "[#55AA55]● saved[/#55AA55]"
    if provider in ("ollama", "lmstudio"):
        key_display = "[dim]not needed[/dim]"
    elif not api_key and os.environ.get(env_key, ""):
        key_display = "[#55AA55]● from env[/#55AA55]"
    elif not api_key:
        key_display = "[red]● missing[/red]"

    console.print(
        Panel(
            f"  Provider   [bold #CC3333]{provider}[/bold #CC3333]\n"
            f"  Model      [bold #CC3333]{chosen_model}[/bold #CC3333]\n"
            f"  API Key    {key_display}\n"
            f"  Config     [dim]{gc_path}[/dim]\n"
            f"  Database   [dim]{config.db_path}[/dim]\n"
            f"  Objects    [dim]{config.objects_dir}[/dim]",
            border_style="#5C1010",
            title="[bold #55AA55]✓ CVC is Ready[/bold #55AA55]",
            padding=(1, 2),
        )
    )

        # ─── First-run-only section (skipped when entering via the menu) ───
    # When the user picks Change Provider or Start Fresh from the main
    # menu, the gateway/IDE/daemon are already configured. Re-running
    # IDE detection or re-asking about the daemon is annoying. Only show
    # this section on the true first-run path (no existing config).
    if not _entering_menu:
    # ─── IDE Auto-Detection & Configuration ─────────────────────────────
        _run_ide_detection(chosen_model)

        # ─── Offer to install daemon (auto-start on boot) ────────────────────
        from cvc.agent.menus import arrow_confirm

        console.print(
            Panel(
                "  The CVC daemon keeps the gateway running in the background\n"
                "  and auto-starts it whenever you restart your computer.\n\n"
                "  [dim]macOS: launchd  |  Linux: systemd  |  Windows: Task Scheduler[/dim]",
                border_style="#5C1010",
                title="[bold #CC3333]Auto-Start Daemon[/bold #CC3333]",
                padding=(1, 2),
            )
        )
        console.print()
        install_daemon_now = arrow_confirm(
            "Install the CVC daemon (auto-start gateway on boot)?", default_yes=True
        )

        if install_daemon_now:
            from cvc.daemon import install_daemon
            result_msg = install_daemon()
            _success(result_msg)
            console.print()

            # Gateway is now running via the daemon — open dashboard
            import time

            import httpx
            endpoint = "http://127.0.0.1:13421"
            console.print("  [dim]Waiting for gateway to start...[/dim]")
            deadline = time.time() + 10.0
            gateway_up = False
            while time.time() < deadline:
                try:
                    r = httpx.get(f"{endpoint}/health", timeout=1.0)
                    if r.status_code == 200:
                        gateway_up = True
                        break
                except Exception:
                    time.sleep(0.5)

            if gateway_up:
                _success(f"Gateway is running at [bold]{endpoint}[/bold]")
                import webbrowser
                webbrowser.open(endpoint)
            else:
                _warn("Gateway is starting up... it may take a few seconds.")
                _hint(f"Open [bold]{endpoint}[/bold] in your browser.")

            console.print()
            console.print(
                Panel(
                    "  [#55AA55]Daemon installed![/#55AA55] The CVC Gateway will auto-start on boot.\n\n"
                    "  [#CC3333]$[/#CC3333] cvc gateway status      [dim]# Check gateway status[/dim]\n"
                    "  [#CC3333]$[/#CC3333] cvc daemon status       [dim]# Check daemon status[/dim]\n"
                    "  [#CC3333]$[/#CC3333] cvc daemon uninstall    [dim]# Remove auto-start[/dim]\n"
                    "  [#CC3333]$[/#CC3333] cvc connect             [dim]# Tool-specific setup guides[/dim]",
                    border_style="#2A5C2A",
                    title="[bold #55AA55]Setup Complete[/bold #55AA55]",
                    padding=(1, 2),
                )
            )
            console.print()
        else:
            # No daemon — offer to start gateway manually
            start_now = arrow_confirm("Start the CVC gateway now?", default_yes=True)

            if start_now:
                console.print()
                click.get_current_context().invoke(gateway_start, host="127.0.0.1", port=13421, proxy_port=13421, no_browser=False, log=False)
            else:
                console.print()
                console.print(
                    Panel(
                        "  [#CC3333]$[/#CC3333] cvc gateway start       [dim]# Start the unified CVC Gateway[/dim]\n"
                        "  [#CC3333]$[/#CC3333] cvc daemon install      [dim]# Install auto-start daemon later[/dim]\n"
                        "  [#CC3333]$[/#CC3333] cvc connect             [dim]# Tool-specific setup guides[/dim]\n"
                        "  [#CC3333]$[/#CC3333] [dim]Point your agent → http://127.0.0.1:13421/v1/chat/completions[/dim]",
                        border_style="#5C1010",
                        title="[bold #8B7070]When You're Ready[/bold #8B7070]",
                        padding=(1, 2),
                    )
                )
                console.print()


# ---------------------------------------------------------------------------
# Connection guides (shared between `serve` and `connect`)
# ---------------------------------------------------------------------------

TOOL_GUIDES: dict[str, dict[str, str | list[str]]] = {
    # ── IDEs ──────────────────────────────────────────────────────────────
    "vscode": {
        "name": "Visual Studio Code",
        "icon": "💎",
        "category": "IDE",
        "steps": [
            "[bold]VS Code GitHub Copilot uses GitHub login authentication.[/bold]",
            "The native Copilot agent cannot be redirected to a custom endpoint.",
            "However, VS Code supports [bold]3 ways[/bold] to use CVC:",
            "",
            "[bold #CC3333]Option 1: Copilot BYOK (Bring Your Own Key)[/bold #CC3333]",
            "  Available on Copilot Individual plans (Free, Pro, Pro+):",
            "  1. [bold]Ctrl+Shift+P[/bold] → [bold]Chat: Manage Language Models[/bold]",
            "  2. Select [bold]OpenAI Compatible[/bold] as provider",
            "  3. Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "  4. API Key → [#CC3333]cvc[/#CC3333]  [dim](any non-empty string)[/dim]",
            "  5. Select model → [#CC3333]{model}[/#CC3333]",
            "",
            "[bold #CC3333]Option 2: MCP Server (Works with native Copilot)[/bold #CC3333]",
            "  Add to VS Code settings.json or .vscode/mcp.json:",
            '     [#CC3333]{{"mcp": {{"servers": {{"cvc": {{"command": "cvc", "args": ["mcp"]}}}}}}}}[/#CC3333]',
            "  CVC tools will be available as MCP tools in Copilot agent mode.",
            "",
            "[bold #CC3333]Option 3: Extensions (Continue.dev / Cline)[/bold #CC3333]",
            "  Install from VS Code Marketplace and configure with:",
            "  Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "  API Key → [#CC3333]cvc[/#CC3333]",
            "",
            "[dim]BYOK is not available on Copilot Business/Enterprise plans.[/dim]",
            "[dim]For Enterprise, use MCP or an extension instead.[/dim]",
        ],
    },
    "antigravity": {
        "name": "Antigravity (Google)",
        "icon": "🚀",
        "category": "IDE",
        "steps": [
            "[bold]Antigravity uses Google account authentication[/bold] — you cannot",
            "override the LLM API endpoint directly. Use CVC via [bold]MCP[/bold] instead.",
            "",
            "[bold #CC3333]Option 1: MCP Server (Recommended)[/bold #CC3333]",
            "  1. Click [bold]⋯[/bold] in Antigravity's agent panel → [bold]Manage MCP Servers[/bold]",
            "  2. Click [bold]View raw config[/bold]",
            "  3. Add the CVC MCP server:",
            "",
            '     [#CC3333]{{"mcpServers": {{"cvc": {{"command": "cvc", "args": ["mcp"]}}}}}}[/#CC3333]',
            "",
            "  4. The CVC tools (commit, branch, merge, restore, status, log)",
            "     will appear as available tools in Antigravity's agent.",
            "",
            "[bold #CC3333]Option 2: Continue.dev Extension[/bold #CC3333]",
            "  Antigravity is Code OSS-based and supports Open VSX extensions.",
            "  Install [bold]Continue.dev[/bold] from Open VSX and configure:",
            "     Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "     API Key  → [#CC3333]cvc[/#CC3333]",
            "     Model    → [#CC3333]{model}[/#CC3333]",
            "",
            "[dim]Antigravity's native Gemini agent uses Google auth internally.[/dim]",
            "[dim]MCP is the only way to add CVC to the native agent flow.[/dim]",
        ],
    },
    "cursor": {
        "name": "Cursor",
        "icon": "🖱️",
        "category": "IDE",
        "steps": [
            "[bold]Cursor supports API key + base URL override.[/bold]",
            "",
            "  1. Open Cursor → Settings (⚙️) → [bold]Models[/bold]",
            "  2. Click [bold]Add OpenAI API Key[/bold] → paste [#CC3333]cvc[/#CC3333]",
            "  3. Enable [bold]Override OpenAI Base URL[/bold] → set to:",
            "     [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "  4. Select your model and start coding!",
            "",
            "[bold #CC3333]Alternative: MCP Server[/bold #CC3333]",
            "  You can also add CVC as an MCP server in Cursor:",
            "  Settings → MCP Servers → Add:",
            '     [#CC3333]{{"cvc": {{"command": "cvc", "args": ["mcp"]}}}}[/#CC3333]',
            "",
            "[dim]Note: Cursor's built-in models use subscription auth internally.[/dim]",
            "[dim]The override route above replaces those with CVC-proxied calls.[/dim]",
        ],
    },
    "windsurf": {
        "name": "Windsurf",
        "icon": "🏄",
        "category": "IDE",
        "steps": [
            "[bold]Windsurf uses account-based authentication[/bold] — you cannot",
            "override the LLM API endpoint directly. Use CVC via [bold]MCP[/bold].",
            "",
            "[bold #CC3333]MCP Server (Recommended)[/bold #CC3333]",
            "  1. Open Windsurf → click [bold]⋯[/bold] in Cascade panel",
            "  2. Go to [bold]MCP Settings[/bold] → [bold]Configure[/bold]",
            "  3. Add the CVC MCP server:",
            "",
            '     [#CC3333]{{"mcpServers": {{"cvc": {{"command": "cvc", "args": ["mcp"]}}}}}}[/#CC3333]',
            "",
            "  4. CVC tools (commit, branch, merge, restore, status, log)",
            "     will be available to Windsurf's Cascade agent.",
            "",
            "[dim]Windsurf (formerly Codeium) is now owned by OpenAI.[/dim]",
            "[dim]The built-in Cascade agent authenticates via Windsurf account.[/dim]",
            "[dim]MCP is the supported way to extend its capabilities.[/dim]",
        ],
    },
    # ── IDE Extensions ────────────────────────────────────────────────────
    "vscode-continue": {
        "name": "Continue.dev (VS Code)",
        "icon": "🔄",
        "category": "IDE Extension",
        "steps": [
            "Install [bold]Continue[/bold] extension from VS Code Marketplace",
            "Open [bold]~/.continue/config.yaml[/bold] and add:",
            "",
            "  [#CC3333]models:[/#CC3333]",
            "    [#CC3333]- name: CVC Proxy[/#CC3333]",
            "      [#CC3333]provider: openai[/#CC3333]",
            "      [#CC3333]model: {model}[/#CC3333]",
            "      [#CC3333]apiBase: {endpoint}/v1[/#CC3333]",
            "      [#CC3333]apiKey: cvc[/#CC3333]",
            "",
            "Restart VS Code → select [bold]CVC Proxy[/bold] in Continue",
        ],
    },
    "vscode-cline": {
        "name": "Cline / Roo (VS Code)",
        "icon": "🤖",
        "category": "IDE Extension",
        "steps": [
            "Install [bold]Cline[/bold] extension from VS Code Marketplace",
            "Click the ⚙️ icon in the Cline panel",
            "Set API Provider → [bold]OpenAI Compatible[/bold]",
            "Set Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "Set API Key → [#CC3333]cvc[/#CC3333]  [dim](any non-empty string)[/dim]",
            "Set Model ID → [#CC3333]{model}[/#CC3333]",
            "Click [bold]Verify[/bold] → done!",
        ],
    },
    "vscode-copilot": {
        "name": "GitHub Copilot (BYOK)",
        "icon": "🐙",
        "category": "IDE Extension",
        "steps": [
            "Open VS Code → [bold]Chat: Manage Language Models[/bold] (Ctrl+Shift+P)",
            "Select [bold]OpenAI Compatible[/bold] as provider",
            "Set Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "Set API Key → [#CC3333]cvc[/#CC3333]  [dim](any non-empty string)[/dim]",
            "Select model → [#CC3333]{model}[/#CC3333]",
            "[dim]Note: BYOK is for Copilot Individual plans only (not Business/Enterprise)[/dim]",
        ],
    },
    # ── CLI Tools ─────────────────────────────────────────────────────────
    "claude-code": {
        "name": "Claude Code CLI",
        "icon": "🟠",
        "category": "CLI Tool",
        "steps_unix": [
            "[bold]Claude Code now works natively with CVC![/bold]",
            "CVC serves the Anthropic Messages API at [bold]/v1/messages[/bold],",
            "so Claude Code works without any format translation.",
            "",
            "[bold #CC3333]Quick start:[/bold #CC3333]",
            "",
            "  [#CC3333]export ANTHROPIC_BASE_URL=\"{endpoint}\"[/#CC3333]",
            "  [#CC3333]claude[/#CC3333]",
            "",
            "Your existing ANTHROPIC_API_KEY is passed through to the",
            "upstream Anthropic API. CVC intercepts the conversation for",
            "cognitive versioning and forwards everything else.",
            "",
            "[bold #CC3333]Or add to ~/.claude/settings.json:[/bold #CC3333]",
            "",
            "  [#CC3333]{{[/#CC3333]",
            "    [#CC3333]\"env\": {{[/#CC3333]",
            "      [#CC3333]\"ANTHROPIC_BASE_URL\": \"{endpoint}\"[/#CC3333]",
            "    [#CC3333]}}[/#CC3333]",
            "  [#CC3333]}}[/#CC3333]",
            "",
            "[dim]Auth pass-through: CVC forwards your API key to Anthropic.[/dim]",
            "[dim]No need to store your key in CVC — just set ANTHROPIC_API_KEY.[/dim]",
        ],
        "steps_win": [
            "[bold]Claude Code now works natively with CVC![/bold]",
            "CVC serves the Anthropic Messages API at [bold]/v1/messages[/bold].",
            "",
            "[bold #CC3333]Quick start:[/bold #CC3333]",
            "",
            "  [#CC3333]$env:ANTHROPIC_BASE_URL = \"{endpoint}\"[/#CC3333]",
            "  [#CC3333]claude[/#CC3333]",
            "",
            "Your existing ANTHROPIC_API_KEY is passed through to the",
            "upstream Anthropic API. CVC intercepts the conversation for",
            "cognitive versioning and forwards everything else.",
            "",
            "[dim]Auth pass-through: CVC forwards your API key to Anthropic.[/dim]",
            "[dim]No need to store your key in CVC — just set ANTHROPIC_API_KEY.[/dim]",
        ],
    },
    "gemini-cli": {
        "name": "Gemini CLI",
        "icon": "💠",
        "category": "CLI Tool",
        "steps_unix": [
            "Gemini CLI uses settings files for configuration.",
            "Edit [bold]~/.gemini/settings.json[/bold] and add:",
            "",
            "  [#CC3333]{{[/#CC3333]",
            "    [#CC3333]\"model\": {{[/#CC3333]",
            "      [#CC3333]\"name\": \"{model}\"[/#CC3333]",
            "    [#CC3333]}}[/#CC3333]",
            "  [#CC3333]}}[/#CC3333]",
            "",
            "Then set the API endpoint via environment variable:",
            "",
            "  [#CC3333]export GEMINI_API_BASE_URL=\"{endpoint}/v1\"[/#CC3333]",
            "  [#CC3333]export GEMINI_API_KEY=\"your-key\"[/#CC3333]",
            "  [#CC3333]gemini[/#CC3333]",
            "",
            "[dim]Custom base URL support may require Gemini CLI v2+.[/dim]",
            "[dim]Check: https://github.com/google-gemini/gemini-cli[/dim]",
        ],
        "steps_win": [
            "Gemini CLI uses settings files for configuration.",
            "Edit [bold]%USERPROFILE%\\.gemini\\settings.json[/bold] and add:",
            "",
            "  [#CC3333]{{[/#CC3333]",
            "    [#CC3333]\"model\": {{[/#CC3333]",
            "      [#CC3333]\"name\": \"{model}\"[/#CC3333]",
            "    [#CC3333]}}[/#CC3333]",
            "  [#CC3333]}}[/#CC3333]",
            "",
            "Then set the API endpoint via environment variable:",
            "",
            "  [#CC3333]$env:GEMINI_API_BASE_URL = \"{endpoint}/v1\"[/#CC3333]",
            "  [#CC3333]$env:GEMINI_API_KEY = \"your-key\"[/#CC3333]",
            "  [#CC3333]gemini[/#CC3333]",
            "",
            "[dim]Custom base URL support may require Gemini CLI v2+.[/dim]",
            "[dim]Check: https://github.com/google-gemini/gemini-cli[/dim]",
        ],
    },
    "kiro-cli": {
        "name": "Kiro CLI (Amazon)",
        "icon": "🦊",
        "category": "CLI Tool",
        "steps_unix": [
            "Kiro CLI from Amazon uses custom agents + MCP servers.",
            "Create a custom agent config to route through CVC:",
            "",
            "  Edit [bold]~/.kiro/settings.json[/bold]:",
            "",
            "  [#CC3333]{{[/#CC3333]",
            "    [#CC3333]\"model_provider\": \"openai\",[/#CC3333]",
            "    [#CC3333]\"model\": \"{model}\",[/#CC3333]",
            "    [#CC3333]\"base_url\": \"{endpoint}/v1\",[/#CC3333]",
            "    [#CC3333]\"api_key\": \"cvc\"[/#CC3333]",
            "  [#CC3333]}}[/#CC3333]",
            "",
            "Or use the Kiro Gateway for OpenAI-compatible routing:",
            "",
            "  [#CC3333]export OPENAI_API_BASE=\"{endpoint}/v1\"[/#CC3333]",
            "  [#CC3333]export OPENAI_API_KEY=\"cvc\"[/#CC3333]",
            "  [#CC3333]kiro[/#CC3333]",
            "",
            "[dim]See: https://kiro.dev/docs/cli/[/dim]",
        ],
        "steps_win": [
            "Kiro CLI from Amazon uses custom agents + MCP servers.",
            "Create a custom agent config to route through CVC:",
            "",
            "  Edit [bold]%USERPROFILE%\\.kiro\\settings.json[/bold]:",
            "",
            "  [#CC3333]{{[/#CC3333]",
            "    [#CC3333]\"model_provider\": \"openai\",[/#CC3333]",
            "    [#CC3333]\"model\": \"{model}\",[/#CC3333]",
            "    [#CC3333]\"base_url\": \"{endpoint}/v1\",[/#CC3333]",
            "    [#CC3333]\"api_key\": \"cvc\"[/#CC3333]",
            "  [#CC3333]}}[/#CC3333]",
            "",
            "Or use environment variables:",
            "",
            "  [#CC3333]$env:OPENAI_API_BASE = \"{endpoint}/v1\"[/#CC3333]",
            "  [#CC3333]$env:OPENAI_API_KEY = \"cvc\"[/#CC3333]",
            "  [#CC3333]kiro[/#CC3333]",
            "",
            "[dim]See: https://kiro.dev/docs/cli/[/dim]",
        ],
    },
    "aider": {
        "name": "Aider CLI",
        "icon": "🛠️",
        "category": "CLI Tool",
        "steps_unix": [
            "Set the environment variables:",
            "",
            "  [#CC3333]export OPENAI_API_BASE={endpoint}/v1[/#CC3333]",
            "  [#CC3333]export OPENAI_API_KEY=cvc[/#CC3333]",
            "",
            "Then start Aider:",
            "",
            "  [#CC3333]aider --model openai/{model}[/#CC3333]",
        ],
        "steps_win": [
            "Set the environment variables:",
            "",
            "  [#CC3333]$env:OPENAI_API_BASE = \"{endpoint}/v1\"[/#CC3333]",
            "  [#CC3333]$env:OPENAI_API_KEY = \"cvc\"[/#CC3333]",
            "",
            "Then start Aider:",
            "",
            "  [#CC3333]aider --model openai/{model}[/#CC3333]",
        ],
    },
    # ── Web Interface ─────────────────────────────────────────────────────
    "open-webui": {
        "name": "Open WebUI",
        "icon": "🌐",
        "category": "Web Interface",
        "steps": [
            "Open WebUI → [bold]Settings → Connections[/bold]",
            "Click [bold]+ Add Connection[/bold]",
            "URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "API Key → [#CC3333]cvc[/#CC3333]  [dim](any non-empty string)[/dim]",
            "Save → the CVC model will appear in the model dropdown",
        ],
    },
    # ── Cloud IDE ─────────────────────────────────────────────────────────
    "firebase-studio": {
        "name": "Firebase Studio",
        "icon": "🔥",
        "category": "Cloud IDE",
        "steps": [
            "Firebase Studio is Google's cloud IDE built on Code OSS.",
            "It uses Gemini natively but supports Open VSX extensions.",
            "To route AI through CVC:",
            "",
            "  1. Start CVC with [bold]--host 0.0.0.0[/bold] (or use a tunnel)",
            "  2. Open your Firebase Studio workspace",
            "  3. Install [bold]Continue.dev[/bold] or [bold]Cline[/bold] from Open VSX",
            "  4. Configure the extension with:",
            "     Base URL → [bold #CC3333]{endpoint}/v1[/bold #CC3333]",
            "     API Key  → [#CC3333]cvc[/#CC3333]",
            "     Model    → [#CC3333]{model}[/#CC3333]",
            "",
            "[bold #CC3333]Alternative: MCP Server[/bold #CC3333]",
            "  If your Firebase Studio workspace has terminal access:",
            '  Add CVC as an MCP server in [bold].vscode/mcp.json[/bold]',
            "",
            "[dim]Firebase Studio does not support direct API endpoint override.[/dim]",
            "[dim]Use extensions or MCP for custom model routing.[/dim]",
        ],
    },
    # ── CLI Tools (additional) ────────────────────────────────────────────
    "codex-cli": {
        "name": "OpenAI Codex CLI",
        "icon": "⌨️",
        "category": "CLI Tool",
        "steps_unix": [
            "[bold]Codex CLI supports custom model providers.[/bold]",
            "Add CVC as a proxy provider in your config:",
            "",
            "[bold #CC3333]Option 1: Environment variables[/bold #CC3333]",
            "",
            "  [#CC3333]export OPENAI_API_BASE={endpoint}/v1[/#CC3333]",
            "  [#CC3333]export OPENAI_API_KEY=cvc[/#CC3333]",
            "  [#CC3333]codex[/#CC3333]",
            "",
            "[bold #CC3333]Option 2: Config file (~/.codex/config.toml)[/bold #CC3333]",
            "",
            "  [#CC3333]model_provider = \"cvc\"[/#CC3333]",
            "",
            "  [#CC3333][model_providers.cvc][/#CC3333]",
            "  [#CC3333]name = \"CVC Proxy\"[/#CC3333]",
            '  [#CC3333]base_url = "{endpoint}"[/#CC3333]',
            '  [#CC3333]env_key = "OPENAI_API_KEY"[/#CC3333]',
            "",
            "Your API key is passed through to the upstream provider.",
            "",
            "[dim]Works with: codex, codex --provider openai, and custom providers.[/dim]",
        ],
        "steps_win": [
            "[bold]Codex CLI supports custom model providers.[/bold]",
            "",
            "[bold #CC3333]Option 1: Environment variables[/bold #CC3333]",
            "",
            "  [#CC3333]$env:OPENAI_API_BASE = \"{endpoint}/v1\"[/#CC3333]",
            "  [#CC3333]$env:OPENAI_API_KEY = \"cvc\"[/#CC3333]",
            "  [#CC3333]codex[/#CC3333]",
            "",
            "[bold #CC3333]Option 2: Config file (~/.codex/config.toml)[/bold #CC3333]",
            "",
            "  [#CC3333]model_provider = \"cvc\"[/#CC3333]",
            "",
            "  [#CC3333][model_providers.cvc][/#CC3333]",
            "  [#CC3333]name = \"CVC Proxy\"[/#CC3333]",
            '  [#CC3333]base_url = "{endpoint}"[/#CC3333]',
            '  [#CC3333]env_key = "OPENAI_API_KEY"[/#CC3333]',
            "",
            "[dim]Works with: codex, codex --provider openai, and custom providers.[/dim]",
        ],
    },
}


def _format_tool_guide(tool_key: str, endpoint: str, model: str) -> Panel:
    """Format a single tool's connection guide as a Rich Panel."""
    guide = TOOL_GUIDES[tool_key]
    name = guide["name"]
    icon = guide["icon"]

    # Pick platform-specific steps for CLI tools
    if sys.platform == "win32" and "steps_win" in guide:
        steps = guide["steps_win"]
    elif "steps_unix" in guide:
        steps = guide["steps_unix"]
    else:
        steps = guide.get("steps", [])

    # Format steps with endpoint/model placeholders
    formatted = []
    for step in steps:
        line = str(step).format(endpoint=endpoint, model=model)
        formatted.append(f"  {line}")

    return Panel(
        "\n".join(formatted),
        border_style="dim cyan",
        title=f"[bold white]{icon} {name}[/bold white]",
        title_align="left",
        padding=(1, 2),
    )


# ---------------------------------------------------------------------------
# serve (DEPRECATED — use `cvc gateway start`)
# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# v3.1.0 — Gateway YAML bridge
# ---------------------------------------------------------------------------

def _sync_global_to_gateway_yaml(
    provider: str,
    model: str,
    api_keys: dict[str, str] | None = None,
) -> Path:
    """Mirror the GlobalConfig to ``~/.cvc/config.yaml`` so the gateway
    sees the same provider/model the user just picked in ``cvc setup``.

    Why this exists:
      The dashboard's unified-core chat reads ``~/.cvc/config.yaml``
      (the schema used by the legacy gateway) — keys like
      ``primary_provider`` and ``default_model``. The Python setup
      wizard (this CLI) writes to ``GlobalConfig`` which lives in
      ``~/.cvc/config.json``. Two separate files, two separate worlds.
      This helper keeps the YAML view in sync with the JSON view.

    Behaviour:
      - Loads the existing YAML if present (preserves ``telegram``,
        ``skills.external_dirs``, and any other gateway-specific keys).
      - Sets / overwrites ``primary_provider`` and ``default_model``.
      - Writes the result back atomically (write to .tmp + rename).
      - Returns the path of the written file.
    """
    import yaml as _yaml

    yaml_path = Path.home() / ".cvc" / "config.yaml"
    yaml_path.parent.mkdir(parents=True, exist_ok=True)

    existing: dict = {}
    if yaml_path.exists():
        try:
            existing = _yaml.safe_load(yaml_path.read_text(encoding="utf-8")) or {}
            if not isinstance(existing, dict):
                existing = {}
        except Exception:
            _warn(f"Existing {yaml_path.name} was unreadable; rewriting with new values.")
            existing = {}

    existing["primary_provider"] = provider
    existing["default_model"] = model
    existing["version"] = existing.get("version", 1)

    # v3.1.3 — Persist API keys in config.yaml so the gateway can read
    # them at startup. Previously the keys only lived in config.json,
    # and the gateway's _resolve_provider_config() only read env vars,
    # so the dashboard always showed "Setup Required" until the user
    # manually exported the key in their shell. Storing them in the
    # gateway config means `cvc setup` is enough — no shell export
    # required, no restarts of parent terminals to pick up new env.
    #
    # Keys are stored under a new `api_keys:` top-level key (not
    # mixed into the legacy primary_provider/default_model keys, which
    # the dashboard reads as a different schema). The gateway reads
    # this key as a fallback after env vars and before built-in default.
    if api_keys:
        # Merge: don't drop keys the user previously stored here.
        existing_api_keys = existing.get("api_keys") or {}
        if not isinstance(existing_api_keys, dict):
            existing_api_keys = {}
        for k, v in api_keys.items():
            if v:  # never store empty strings
                existing_api_keys[k] = v
        existing["api_keys"] = existing_api_keys

    # Atomic write: write to .tmp, then rename. Avoids partial writes
    # if the process is killed mid-flush.
    tmp_path = yaml_path.with_suffix(".yaml.tmp")
    try:
        tmp_path.write_text(
            _yaml.safe_dump(existing, sort_keys=False, default_flow_style=False),
            encoding="utf-8",
        )
        tmp_path.replace(yaml_path)
    except Exception as exc:
        _warn(f"Failed to write {yaml_path}: {exc}")
        return yaml_path

    _success(f"Gateway config synced → [dim]{yaml_path}[/dim]")
    return yaml_path


@main.command(hidden=True)
@click.option("--host", default="127.0.0.1", help="Bind host.")
@click.option("--port", default=19333, type=int, help="Bind port.")
@click.option("--reload", "do_reload", is_flag=True, help="Enable auto-reload for development.")
def serve(host: str, port: int, do_reload: bool) -> None:
    """[DEPRECATED] Start the CVC Cognitive Proxy server.

    This command is deprecated. Use 'cvc gateway start' instead.
    The gateway now includes the proxy functionality with multi-workspace support.
    """
    _banner("Proxy Server (Deprecated)")

    console.print(
        Panel(
            "  [bold #CCAA44]⚠  The 'cvc serve' command is deprecated.[/bold #CCAA44]\n\n"
            "  The CVC Gateway now includes all proxy functionality with\n"
            "  multi-workspace support. Use:\n\n"
            "    [bold #CC3333]cvc gateway start[/bold #CC3333]\n\n"
            "  Then launch your AI tools with:\n\n"
            "    [bold #CC3333]cvc launch claude[/bold #CC3333]\n"
            "    [bold #CC3333]cvc launch aider[/bold #CC3333]\n\n"
            "  The gateway will handle workspace routing automatically.",
            border_style="#CCAA44",
            title="[bold #CCAA44]Deprecated[/bold #CCAA44]",
            padding=(1, 2),
        )
    )
    console.print()
    _warn("Redirecting to 'cvc gateway start --log'…")
    console.print()

    import uvicorn
    uvicorn.run(
        "cvc.gateway:app",
        host=host,
        port=13421,
        reload=do_reload,
        log_level="info",
    )


# ---------------------------------------------------------------------------
# connect (interactive tool connection wizard)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--host", default="127.0.0.1", help="Gateway host.")
@click.option("--port", default=13421, type=int, help="Gateway port.")
@click.argument("tool", required=False, default=None)
def connect(tool: str | None, host: str, port: int) -> None:
    """Show how to connect your AI tool to CVC.

    Run without arguments for an interactive picker, or specify a tool:

      cvc connect vscode
      cvc connect antigravity
      cvc connect cursor
      cvc connect windsurf
      cvc connect cline
      cvc connect claude-code
      cvc connect codex-cli
      cvc connect gemini-cli
      cvc connect kiro-cli
      cvc connect aider
      cvc connect open-webui
      cvc connect firebase-studio
      cvc connect --all
    """
    config = _get_config()
    endpoint = f"http://{host}:{port}"
    model = config.model

    _banner("Connect Your Tools")

    # Show the universal connection info first
    console.print(
        Panel(
            f"  [bold white]CVC Gateway Endpoint[/bold white]\n\n"
            f"  Base URL   [bold #CC3333]{endpoint}/v1[/bold #CC3333]\n"
            f"  API Key    [#CC3333]cvc[/#CC3333]  [dim](any non-empty string — CVC handles auth)[/dim]\n"
            f"  Model      [#CC3333]{model}[/#CC3333]\n\n"
            f"  [dim]CVC exposes a fully OpenAI-compatible API.[/dim]\n"
            f"  [dim]Any tool that supports custom OpenAI endpoints will work.[/dim]",
            border_style="#8B0000",
            title="[bold white]Universal Connection Info[/bold white]",
            padding=(1, 2),
        )
    )
    console.print()

    if tool and tool == "--all":
        # Show all guides
        for key in TOOL_GUIDES:
            console.print(_format_tool_guide(key, endpoint, model))
            console.print()
        return

    if tool:
        # Direct tool specified
        key = tool.lower().replace(" ", "-")
        # Allow shorthand lookups
        aliases = {
            "code": "vscode",
            "vs-code": "vscode",
            "visual-studio-code": "vscode",
            "continue": "vscode-continue",
            "continue.dev": "vscode-continue",
            "cline": "vscode-cline",
            "roo": "vscode-cline",
            "copilot": "vscode-copilot",
            "claude": "claude-code",
            "claude-cli": "claude-code",
            "gemini": "gemini-cli",
            "kiro": "kiro-cli",
            "webui": "open-webui",
            "openwebui": "open-webui",
            "firebase": "firebase-studio",
            "idx": "firebase-studio",
            "windsurf": "windsurf",
            "codeium": "windsurf",
            "codex": "codex-cli",
            "openai-codex": "codex-cli",
        }
        key = aliases.get(key, key)

        if key in TOOL_GUIDES:
            console.print(_format_tool_guide(key, endpoint, model))
        else:
            _error(f"Unknown tool: [bold]{tool}[/bold]")
            _info(f"Available: {', '.join(TOOL_GUIDES.keys())}")
        return

    # ─── Interactive picker ───────────────────────────────────────────────
    categories = {
        "IDE": [],
        "IDE Extension": [],
        "CLI Tool": [],
        "Web Interface": [],
        "Cloud IDE": [],
    }
    for key, guide in TOOL_GUIDES.items():
        cat = guide.get("category", "Other")
        if cat in categories:
            categories[cat].append((key, guide))

    # Build numbered list grouped by category
    all_items: list[tuple[str, dict]] = []
    colors = {"IDE": "#CC3333", "IDE Extension": "#CC6666", "CLI Tool": "#AA8844", "Web Interface": "#AA6666", "Cloud IDE": "red"}

    for cat, items in categories.items():
        if not items:
            continue
        color = colors.get(cat, "white")
        console.print(f"  [{color}]{cat}[/{color}]")
        for key, guide in items:
            idx = len(all_items) + 1
            all_items.append((key, guide))
            console.print(
                f"    [{color}]{idx}[/{color}]  {guide['icon']}  [bold]{guide['name']}[/bold]"
            )
        console.print()

    console.print(f"    [dim]{len(all_items) + 1}[/dim]  📋  [bold]Show all guides at once[/bold]")
    console.print()

    from cvc.agent.menus import arrow_select
    guide_options = [(guide['name'], idx) for idx, (key, guide) in enumerate(all_items)]
    guide_options.append(("Show all guides at once", -1))
    choice = arrow_select("Pick a tool", guide_options, default=0)

    console.print()

    if choice is None:
        return
    if choice == -1:
        # Show all
        for key in TOOL_GUIDES:
            console.print(_format_tool_guide(key, endpoint, model))
            console.print()
    else:
        key, _ = all_items[choice]
        console.print(_format_tool_guide(key, endpoint, model))

    console.print()


# ---------------------------------------------------------------------------
# init
# ---------------------------------------------------------------------------

@main.command()
@click.option("--path", default=".", help="Project root to initialise.")
def init(path: str) -> None:
    """Initialise a .cvc/ directory in the project."""
    from cvc.core.models import CVCConfig

    project_root = Path(path).resolve()
    config = CVCConfig.for_project(project_root=project_root)
    config.ensure_dirs()

    from cvc.core.database import ContextDatabase
    db = ContextDatabase(config)

    # Report vector store status
    vector_status = "[#55AA55]● enabled[/#55AA55]" if db.vectors.available else "[#CC3333]✗ unavailable[/#CC3333]"
    chroma_count = 0
    if db.vectors.available and db.vectors._collection:
        chroma_count = db.vectors._collection.count()

    console.print(
        Panel(
            f"  Directory  [bold]{config.cvc_root}[/bold]\n"
            f"  Database   [dim]{config.db_path}[/dim]\n"
            f"  Objects    [dim]{config.objects_dir}[/dim]\n"
            f"  Vectors    {vector_status}  [dim]{config.chroma_persist_dir}[/dim]\n"
            f"  Embeddings [dim]{chroma_count} indexed[/dim]",
            border_style="#5C1010",
            title="[bold #55AA55]✓ Initialised[/bold #55AA55]",
            padding=(1, 2),
        )
    )
    _hint("Run [bold]cvc setup[/bold] for guided provider configuration.")


# ---------------------------------------------------------------------------
# status
# ---------------------------------------------------------------------------

@main.command()
def status() -> None:
    """Show CVC status: active branch, HEAD, branches."""
    engine, db = _get_engine()
    config = engine.config

    head_short = (engine.head_hash or "—")[:12]
    ctx_messages = engine.context_window
    ctx_size = len(ctx_messages)

    # Break down by role
    user_msgs = sum(1 for m in ctx_messages if m.role == "user")
    assistant_msgs = sum(1 for m in ctx_messages if m.role == "assistant")
    tool_msgs = sum(1 for m in ctx_messages if m.role == "tool")
    system_msgs = sum(1 for m in ctx_messages if m.role == "system")

    # Build context detail string
    if ctx_size > 0:
        ctx_detail = (
            f"[bold]{ctx_size}[/bold] messages  "
            f"[dim]({user_msgs} user, {assistant_msgs} assistant, "
            f"{tool_msgs} tool, {system_msgs} system)[/dim]"
        )
    else:
        ctx_detail = "[dim]0 messages — start a chat with [bold]cvc chat[/bold][/dim]"

    # Count total commits
    commits = db.index.list_commits(branch=engine.active_branch, limit=9999)
    commit_count = len(commits)

    # Check persistent cache
    cache_file = config.cvc_root / "context_cache.json"
    cache_status = "[#55AA55]●[/#55AA55] active" if cache_file.exists() else "[dim]○ none[/dim]"

    # Header info
    console.print(
        Panel(
            f"  Agent      [bold]{config.agent_id}[/bold]\n"
            f"  Branch     [bold #CC3333]{engine.active_branch}[/bold #CC3333]\n"
            f"  HEAD       [bold #CCAA44]{head_short}[/bold #CCAA44]\n"
            f"  Context    {ctx_detail}\n"
            f"  Commits    [bold]{commit_count}[/bold]\n"
            f"  Cache      {cache_status}\n"
            f"  Provider   [dim]{config.provider} / {config.model}[/dim]",
            border_style="#8B0000",
            title="[bold white]CVC Status[/bold white]",
            padding=(1, 2),
        )
    )

    branches = db.index.list_branches()
    if branches:
        table = Table(
            box=box.ROUNDED,
            border_style="dim",
            show_header=True,
            header_style="bold #CC3333",
        )
        table.add_column("", width=3)
        table.add_column("Branch", style="bold")
        table.add_column("HEAD", style="#CCAA44")
        table.add_column("Status")
        for b in branches:
            is_active = b.name == engine.active_branch
            marker = "[bold #55AA55]●[/bold #55AA55]" if is_active else "[dim]○[/dim]"
            name_style = "bold #CC3333" if is_active else "white"
            status_style = "green" if b.status.value == "active" else "dim"
            table.add_row(
                marker,
                f"[{name_style}]{b.name}[/{name_style}]",
                b.head_hash[:12],
                f"[{status_style}]{b.status.value}[/{status_style}]",
            )
        console.print(table)

    db.close()


# ---------------------------------------------------------------------------
# log
# ---------------------------------------------------------------------------

TYPE_ICONS = {
    "checkpoint": ">>",
    "analysis": "**",
    "generation": "++",
    "rollback": "<<",
    "merge": "<>",
    "anchor": "##",
}


@main.command()
@click.option("-n", "--limit", default=20, type=int, help="Max commits to show.")
@click.option("--agent", "agent_id", default=None, help="Filter by agent ID.")
@click.option("--squad", default=None, help="Filter by squad name.")
@click.option("--target", "target_agent_id", default=None, help="Filter by target agent ID.")
def log(limit: int, agent_id: str | None, squad: str | None, target_agent_id: str | None) -> None:
    """Show commit history for the active branch."""
    engine, db = _get_engine()

    # Use agent-filtered queries when a hive mind filter is given
    if agent_id:
        commits = db.index.list_commits_by_agent(agent_id, limit=limit)
        title_suffix = f"agent={agent_id}"
    elif squad:
        commits = db.index.list_commits_by_squad(squad, limit=limit)
        title_suffix = f"squad={squad}"
    elif target_agent_id:
        commits = db.index.list_commits_by_target(target_agent_id, limit=limit)
        title_suffix = f"target={target_agent_id}"
    else:
        commits = None
        title_suffix = engine.active_branch

    if commits is not None:
        entries = [
            {
                "hash": c.commit_hash,
                "short": c.short_hash,
                "type": c.commit_type.value,
                "message": c.message,
                "timestamp": c.metadata.timestamp,
                "parents": c.parent_hashes,
                "is_delta": c.is_delta,
                "agent_id": c.metadata.agent_id,
                "squad": c.metadata.squad or "",
            }
            for c in commits
        ]
    else:
        entries = engine.log(limit=limit)

    if not entries:
        _warn("No commits found.")
        if not (agent_id or squad or target_agent_id):
            _hint("Create your first commit: [bold]cvc commit -m \"initial state\"[/bold]")
        db.close()
        return

    table = Table(
        box=box.ROUNDED,
        border_style="dim",
        show_header=True,
        header_style="bold #CC3333",
        title=f"[bold white]Commit Log[/bold white] [dim]— {title_suffix}[/dim]",
        title_style="",
    )
    table.add_column("", width=2)
    table.add_column("Hash", style="#CCAA44", width=12)
    table.add_column("Type", style="#CC3333", width=12)
    table.add_column("Message", ratio=1)
    # Show agent column when filtering by squad or target
    if squad or target_agent_id:
        table.add_column("Agent", style="cyan", width=14)
    table.add_column("D", width=3, justify="center")

    for i, e in enumerate(entries):
        icon = TYPE_ICONS.get(e["type"], ">")
        delta = "[dim]d[/dim]" if e["is_delta"] else "[#55AA55]●[/#55AA55]"
        msg = e["message"][:55]
        if len(e["message"]) > 55:
            msg += "…"
        row = [icon, e["short"], e["type"], msg]
        if squad or target_agent_id:
            row.append(e.get("agent_id", ""))
        row.append(delta)
        table.add_row(*row)

    console.print(table)
    console.print(f"  [dim]{len(entries)} commit(s) shown[/dim]\n")
    db.close()


# ---------------------------------------------------------------------------
# commit
# ---------------------------------------------------------------------------

@main.command()
@click.option("-m", "--message", required=True, help="Commit message.")
@click.option(
    "-t", "--type", "commit_type",
    default="checkpoint",
    type=click.Choice(["checkpoint", "analysis", "generation"], case_sensitive=False),
    help="Commit type.",
)
@click.option("--tag", "tags", multiple=True, help="Tags (can be repeated).")
def commit(message: str, commit_type: str, tags: tuple[str, ...]) -> None:
    """Create a cognitive commit (save the agent's brain state)."""
    from cvc.core.models import CVCCommitRequest

    engine, db = _get_engine()
    result = engine.commit(
        CVCCommitRequest(message=message, commit_type=commit_type, tags=list(tags))
    )

    if result.success:
        short_hash = (result.commit_hash or "")[:12]
        console.print(
            Panel(
                f"  [bold]{message}[/bold]\n"
                f"  Hash     [#CCAA44]{short_hash}[/#CCAA44]\n"
                f"  Type     [#CC3333]{commit_type}[/#CC3333]\n"
                f"  Branch   [dim]{engine.active_branch}[/dim]",
                border_style="#5C1010",
                title="[bold #55AA55]✓ Committed[/bold #55AA55]",
                padding=(1, 2),
            )
        )
    else:
        _error(result.message)

    db.close()


# ---------------------------------------------------------------------------
# branch
# ---------------------------------------------------------------------------

@main.command()
@click.argument("name", required=False)
@click.option("-d", "--description", default="", help="Branch purpose/description.")
def branch(name: str | None, description: str) -> None:
    """List branches (no args) or create/switch to a new exploration branch."""
    from cvc.core.models import CVCBranchRequest

    engine, db = _get_engine()

    # No name → list mode
    if not name:
        branches = db.index.list_branches()
        if not branches:
            _info("No branches yet.")
            db.close()
            return

        from rich.table import Table
        table = Table(
            title=f"[bold #CC3333]Branches[/bold #CC3333]  ({len(branches)} total)",
            border_style="#5C1010",
            title_justify="left",
            show_lines=False,
        )
        table.add_column("", width=2)
        table.add_column("Name", style="bold")
        table.add_column("HEAD", style="#CCAA44")
        table.add_column("Status", style="dim")
        table.add_column("Parent", style="dim")
        table.add_column("Description", style="dim", overflow="fold")

        for b in branches:
            marker = "[bold #55AA55]●[/bold #55AA55]" if b.name == engine.active_branch else " "
            head = (b.head_hash or "")[:12] or "—"
            status_val = getattr(b.status, "value", str(b.status))
            table.add_row(
                marker,
                b.name,
                head,
                status_val,
                b.parent_branch or "—",
                b.description or "",
            )

        console.print(table)
        _hint("Create: [bold]cvc branch <name>[/bold]   Switch: [bold]cvc restore <hash>[/bold]")
        db.close()
        return

    result = engine.branch(CVCBranchRequest(name=name, description=description))

    if result.success:
        console.print(
            Panel(
                f"  [bold #CC3333]{name}[/bold #CC3333]\n"
                f"  From     [dim]{engine.active_branch}[/dim]\n"
                f"  HEAD     [#CCAA44]{(result.commit_hash or '')[:12]}[/#CCAA44]",
                border_style="#5C1010",
                title="[bold #55AA55]✓ Branch Created[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        if description:
            _info(f"Description: {description}")
    else:
        _error(result.message)

    db.close()


# ---------------------------------------------------------------------------
# merge
# ---------------------------------------------------------------------------

@main.command()
@click.argument("source_branch")
@click.option("--target", default="main", help="Target branch (default: main).")
def merge(source_branch: str, target: str) -> None:
    """Merge a branch into the target (semantic three-way merge)."""
    from cvc.core.models import CVCMergeRequest

    engine, db = _get_engine()
    result = engine.merge(CVCMergeRequest(source_branch=source_branch, target_branch=target))

    if result.success:
        console.print(
            Panel(
                f"  [bold]{source_branch}[/bold] → [bold #CC3333]{target}[/bold #CC3333]\n"
                f"  Commit   [#CCAA44]{(result.commit_hash or '')[:12]}[/#CCAA44]",
                border_style="#5C1010",
                title="[bold #55AA55]✓ Merged[/bold #55AA55]",
                padding=(1, 2),
            )
        )
    else:
        _error(result.message)
        _hint("Check branch names with [bold]cvc status[/bold].")

    db.close()


# ---------------------------------------------------------------------------
# restore
# ---------------------------------------------------------------------------

@main.command()
@click.argument("commit_hash")
def restore(commit_hash: str) -> None:
    """Time-travel: restore the agent's brain to a previous state."""
    from cvc.core.models import CVCRestoreRequest

    engine, db = _get_engine()
    result = engine.restore(CVCRestoreRequest(commit_hash=commit_hash))

    if result.success:
        console.print(
            Panel(
                f"  Restored to [#CCAA44]{commit_hash[:12]}[/#CCAA44]\n"
                f"  Branch   [dim]{engine.active_branch}[/dim]",
                border_style="#5C1010",
                title="[bold #55AA55]✓ Time-Travelled[/bold #55AA55]",
                padding=(1, 2),
            )
        )
    else:
        _error(result.message)
        _hint(
            "Use [bold]cvc log[/bold] to find valid commit hashes.\n"
            "Both full and short (12-char) hashes work."
        )

    db.close()


# ---------------------------------------------------------------------------
# VCS hooks
# ---------------------------------------------------------------------------

@main.command("install-hooks")
def install_hooks() -> None:
    """Install Git hooks for CVC ↔ Git synchronisation."""
    engine, db = _get_engine()
    from cvc.vcs.bridge import VCSBridge

    bridge = VCSBridge(engine.config, db)
    result = bridge.install_hooks()

    lines = []
    for hook, path in result.items():
        lines.append(f"  {hook}  [dim]→ {path}[/dim]")

    console.print(
        Panel(
            "\n".join(lines),
            border_style="#5C1010",
            title="[bold #55AA55]✓ Hooks Installed[/bold #55AA55]",
            padding=(1, 2),
        )
    )
    _info("CVC will now auto-sync with Git commits and checkouts.")
    db.close()


@main.command("capture-snapshot")
@click.option("--git-sha", default=None, help="Git SHA to link (auto-detected if omitted).")
def capture_snapshot(git_sha: str | None) -> None:
    """Capture CVC state linked to the current Git commit."""
    engine, db = _get_engine()
    from cvc.vcs.bridge import VCSBridge

    bridge = VCSBridge(engine.config, db)
    result = bridge.capture_snapshot(git_sha)

    if "error" in result:
        _error(result["error"])
    else:
        console.print(
            Panel(
                f"  Git    [dim]{result['git_sha'][:12]}[/dim]\n"
                f"  CVC    [#CCAA44]{result['cvc_hash'][:12]}[/#CCAA44]",
                border_style="#5C1010",
                title="[bold #55AA55]✓ Snapshot Captured[/bold #55AA55]",
                padding=(1, 2),
            )
        )

    db.close()


@main.command("restore-for-checkout")
@click.option("--git-sha", required=True, help="Git SHA being checked out.")
def restore_for_checkout(git_sha: str) -> None:
    """Restore CVC state corresponding to a Git checkout (called by hook)."""
    engine, db = _get_engine()
    from cvc.vcs.bridge import VCSBridge

    bridge = VCSBridge(engine.config, db)
    cvc_hash = bridge.restore_for_checkout(git_sha)

    if cvc_hash:
        from cvc.core.models import CVCRestoreRequest
        result = engine.restore(CVCRestoreRequest(commit_hash=cvc_hash))
        if result.success:
            _success(f"Restored CVC state: [#CCAA44]{cvc_hash[:12]}[/#CCAA44]")

    db.close()


# ---------------------------------------------------------------------------
# recall (natural language search across all conversations)
# ---------------------------------------------------------------------------

@main.command()
@click.argument("query")
@click.option("-n", "--limit", default=10, type=int, help="Max results to return.")
@click.option("--deep/--no-deep", default=True, help="Search inside conversation content (slower but thorough).")
def recall(query: str, limit: int, deep: bool) -> None:
    """Search across ALL past conversations using natural language.

    \b
    Uses CVC's three-tier search:
      1. Semantic vector search (Tier 3, if Chroma is enabled)
      2. Commit message text search (Tier 1, always available)
      3. Deep content search (scans actual conversation messages)

    \b
    Examples:
      cvc recall "how did we implement auth?"
      cvc recall "database migration" --limit 5
      cvc recall "error handling" --no-deep
    """
    from datetime import datetime

    engine, db = _get_engine()

    console.print()
    console.print(
        f"  [bold #CC3333]Searching[/bold #CC3333] [dim]for:[/dim] "
        f"[bold white]\"{query}\"[/bold white]"
    )

    search_sources = []
    if db.vectors.available:
        search_sources.append("[#55AA55]semantic[/#55AA55]")
    search_sources.append("[#CCAA44]message[/#CCAA44]")
    if deep:
        search_sources.append("[#CC3333]deep content[/#CC3333]")
    console.print(f"  [dim]Sources:[/dim] {' + '.join(search_sources)}")
    console.print()

    results = engine.recall(query, limit=limit, deep=deep)

    if not results:
        _warn("No conversations found matching your query.")
        _hint(
            "Tips:\n"
            "• Try broader search terms\n"
            "• Use [bold]--deep[/bold] to search inside conversation content\n"
            "• Check [bold]cvc log[/bold] to see available commits"
        )
        db.close()
        return

    # Display results
    for i, r in enumerate(results, 1):
        ts = datetime.fromtimestamp(r["timestamp"])
        date_str = ts.strftime("%Y-%m-%d %H:%M")

        # Source badge
        src = r["relevance_source"]
        if src == "semantic":
            badge = "[bold #55AA55]SEMANTIC[/bold #55AA55]"
        elif src == "message":
            badge = "[bold #CCAA44]MESSAGE[/bold #CCAA44]"
        else:
            badge = "[bold #CC3333]CONTENT[/bold #CC3333]"

        # Distance indicator
        dist = r["distance"]
        if dist < 0.3:
            relevance = "[bold #55AA55]●●●[/bold #55AA55] High"
        elif dist < 0.6:
            relevance = "[bold #CCAA44]●●○[/bold #CCAA44] Medium"
        else:
            relevance = "[bold #CC3333]●○○[/bold #CC3333] Low"

        # Build result panel content
        content_lines = [
            f"  [dim]Commit[/dim]    [#CCAA44]{r['short_hash']}[/#CCAA44]  "
            f"[dim]{r['commit_type']}[/dim]",
            f"  [dim]Date[/dim]      {date_str}",
            f"  [dim]Source[/dim]    {badge}  {relevance}",
        ]
        if r["provider"] or r["model"]:
            content_lines.append(
                f"  [dim]Model[/dim]     "
                f"[#CC3333]{r.get('provider', '')}/{r.get('model', '')}[/#CC3333]"
            )

        # Show message
        msg = r["message"]
        if len(msg) > 120:
            msg = msg[:117] + "…"
        content_lines.append(f"  [dim]Message[/dim]   {msg}")

        # Show matching conversation excerpts
        matching = r.get("matching_messages", [])
        if matching:
            content_lines.append("")
            content_lines.append("  [bold white]Matching excerpts:[/bold white]")
            for mm in matching[:3]:
                role = mm["role"].upper()
                excerpt = mm["content"][:200]
                if len(mm["content"]) > 200:
                    excerpt += "…"
                content_lines.append(f"    [dim]{role}:[/dim] {excerpt}")

        console.print(
            Panel(
                "\n".join(content_lines),
                border_style="#5C1010" if i == 1 else "dim",
                title=f"[bold white]#{i}[/bold white]",
                title_align="left",
                padding=(0, 1),
            )
        )

    console.print(f"\n  [dim]{len(results)} result(s) found[/dim]")
    _hint(
        "View full context: [bold]cvc context --show --commit <hash>[/bold]\n"
        "Export as Markdown: [bold]cvc export --markdown --commit <hash>[/bold]"
    )
    console.print()
    db.close()


# ---------------------------------------------------------------------------
# context (display stored conversation content)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--show", is_flag=True, help="Display the full stored conversation content.")
@click.option("--commit", "commit_hash", default=None, help="Show context for a specific commit (default: current HEAD).")
@click.option("-n", "--limit", default=0, type=int, help="Limit number of messages shown (0 = all).")
@click.option("--role", default=None, type=click.Choice(["user", "assistant", "system", "tool"]), help="Filter by message role.")
def context(show: bool, commit_hash: str | None, limit: int, role: str | None) -> None:
    """Display stored conversation context.

    \b
    Without --show: displays a summary (count, roles, size)
    With    --show: displays the full conversation content

    \b
    Examples:
      cvc context               # Quick summary of current context
      cvc context --show        # Show the full conversation
      cvc context --show --commit abc123  # Show a specific commit's conversation
      cvc context --show --role user      # Show only user messages
      cvc context --show -n 20           # Show last 20 messages
    """
    from datetime import datetime

    engine, db = _get_engine()

    if commit_hash:
        # Load context from a specific commit
        commit = db.index.get_commit(commit_hash)
        if commit is None:
            _error(f"Commit '{commit_hash}' not found.")
            _hint("Use [bold]cvc log[/bold] to find valid commit hashes.")
            db.close()
            return
        blob = db.retrieve_blob(commit.commit_hash)
        if blob is None:
            _error(f"Could not reconstruct blob for commit '{commit_hash}'.")
            db.close()
            return
        messages = blob.messages
        context_source = f"commit {commit.commit_hash[:12]}"
        reasoning = blob.reasoning_trace
        token_count = blob.token_count
    else:
        # Use current context window
        messages = engine.context_window
        context_source = f"HEAD ({(engine.head_hash or '—')[:12]})"
        reasoning = engine._reasoning_trace
        token_count = sum(len(m.content.split()) for m in messages)

    # Apply role filter
    if role:
        messages = [m for m in messages if m.role == role]

    # Apply limit
    if limit > 0:
        messages = messages[-limit:]

    if not show:
        # Summary mode (existing behavior enhanced)
        total = len(messages)
        user_count = sum(1 for m in messages if m.role == "user")
        assistant_count = sum(1 for m in messages if m.role == "assistant")
        tool_count = sum(1 for m in messages if m.role == "tool")
        system_count = sum(1 for m in messages if m.role == "system")

        console.print(
            Panel(
                f"  [dim]Source[/dim]       {context_source}\n"
                f"  [dim]Messages[/dim]     [bold]{total}[/bold]\n"
                f"  [dim]  User[/dim]       {user_count}\n"
                f"  [dim]  Assistant[/dim]  {assistant_count}\n"
                f"  [dim]  Tool[/dim]       {tool_count}\n"
                f"  [dim]  System[/dim]     {system_count}\n"
                f"  [dim]Tokens[/dim]       ~{token_count}",
                border_style="#5C1010",
                title="[bold white]Context Summary[/bold white]",
                padding=(1, 2),
            )
        )
        _hint("Use [bold]cvc context --show[/bold] to view the actual conversation content.")
        db.close()
        return

    # Full conversation display
    if not messages:
        _warn("No messages in context.")
        _hint("Start a conversation with [bold]cvc agent[/bold] or create a commit.")
        db.close()
        return

    console.print()
    console.print(
        f"  [bold #CC3333]Context[/bold #CC3333] [dim]from[/dim] {context_source}  "
        f"[dim]({len(messages)} messages)[/dim]"
    )
    console.print()

    role_styles = {
        "system": ("#8B7070", "⚙️"),
        "user": ("#55AA55", "👤"),
        "assistant": ("#CC3333", "🤖"),
        "tool": ("#CCAA44", "🔧"),
    }

    for i, msg in enumerate(messages, 1):
        style, emoji = role_styles.get(msg.role, ("#888888", "❓"))
        ts = datetime.fromtimestamp(msg.timestamp)
        time_str = ts.strftime("%H:%M:%S")

        # Truncate very long messages for display
        content = msg.content
        truncated = False
        if len(content) > 2000:
            content = content[:2000]
            truncated = True

        header = f"{emoji} [bold {style}]{msg.role.upper()}[/bold {style}]  [dim]{time_str}[/dim]"

        panel_content = content
        if truncated:
            panel_content += f"\n\n[dim]… ({len(msg.content) - 2000} more chars)[/dim]"

        console.print(
            Panel(
                panel_content,
                border_style=style,
                title=header,
                title_align="left",
                padding=(0, 2),
            )
        )

    # Show reasoning trace if present
    if reasoning:
        console.print(
            Panel(
                reasoning[:1000] + ("…" if len(reasoning) > 1000 else ""),
                border_style="#8B7070",
                title="[bold #8B7070]Reasoning Trace[/bold #8B7070]",
                title_align="left",
                padding=(0, 2),
            )
        )

    console.print(f"\n  [dim]{len(messages)} message(s) displayed[/dim]\n")
    db.close()


# ---------------------------------------------------------------------------
# export (conversation to shareable formats)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--markdown", "as_markdown", is_flag=True, help="Export as shareable Markdown file.")
@click.option("--commit", "commit_hash", default=None, help="Commit hash to export (default: HEAD).")
@click.option("-o", "--output", "output_path", default=None, help="Output file path (auto-generated if omitted).")
def export(as_markdown: bool, commit_hash: str | None, output_path: str | None) -> None:
    """Export a commit's conversation as a shareable file.

    \b
    Perfect for code reviews — share the AI's reasoning with your team.

    \b
    Examples:
      cvc export --markdown                      # Export HEAD as Markdown
      cvc export --markdown --commit abc123       # Export specific commit
      cvc export --markdown -o review.md          # Custom output filename
    """
    engine, db = _get_engine()

    if not as_markdown:
        _warn("Please specify an export format.")
        _hint("Currently supported: [bold]--markdown[/bold]\n\nExample: [bold]cvc export --markdown[/bold]")
        db.close()
        return

    try:
        md_content, resolved_hash = engine.export_markdown(commit_hash)
    except ValueError as exc:
        _error(str(exc))
        _hint("Use [bold]cvc log[/bold] to find valid commit hashes.")
        db.close()
        return

    # Determine output path
    if output_path is None:
        short = resolved_hash[:12]
        output_path = f"cvc-export-{short}.md"

    out = Path(output_path)
    out.write_text(md_content, encoding="utf-8")

    # Stats
    lines_count = md_content.count("\n")
    size_kb = len(md_content.encode("utf-8")) / 1024

    console.print(
        Panel(
            f"  [dim]Commit[/dim]    [#CCAA44]{resolved_hash[:12]}[/#CCAA44]\n"
            f"  [dim]Format[/dim]    Markdown\n"
            f"  [dim]File[/dim]      [bold]{out.resolve()}[/bold]\n"
            f"  [dim]Size[/dim]      {size_kb:.1f} KB ({lines_count} lines)",
            border_style="#5C1010",
            title="[bold #55AA55]✓ Exported[/bold #55AA55]",
            padding=(1, 2),
        )
    )
    _hint(
        "Share this file during code reviews so your team can\n"
        "see exactly what the AI reasoned about."
    )
    console.print()
    db.close()


# ---------------------------------------------------------------------------
# inject (cross-project context transfer)
# ---------------------------------------------------------------------------

@main.command()
@click.argument("source_project")
@click.option("--query", "-q", required=True, help="Natural language query to find relevant conversations.")
@click.option("-n", "--limit", default=5, type=int, help="Max conversations to pull from source.")
def inject(source_project: str, query: str, limit: int) -> None:
    """Pull relevant conversations from another project into this one.

    \b
    Cross-project context transfer — no other tool does this.
    Search another project's CVC history and inject the matching
    conversations into your current project as context.

    \b
    Examples:
      cvc inject ../auth-service --query "JWT token handling"
      cvc inject /projects/api --query "database migration patterns" -n 3
      cvc inject ../shared-lib -q "error handling middleware"
    """
    source_path = Path(source_project).resolve()

    if not source_path.is_dir():
        _error(f"Directory not found: {source_path}")
        return

    if not (source_path / ".cvc").is_dir():
        _error(f"No .cvc/ directory found at: {source_path}")
        _hint(
            f"Make sure the source project has CVC initialised:\n"
            f"  [bold]cd {source_path} && cvc init[/bold]"
        )
        return

    engine, db = _get_engine()

    console.print()
    console.print(
        f"  [bold #CC3333]Injecting context[/bold #CC3333]\n"
        f"  [dim]From[/dim]     [bold]{source_path.name}[/bold] [dim]({source_path})[/dim]\n"
        f"  [dim]Query[/dim]    [bold white]\"{query}\"[/bold white]\n"
        f"  [dim]Limit[/dim]    {limit} conversations"
    )
    console.print()

    result = engine.inject_from_project(source_path, query, limit=limit)

    if result.success:
        detail = result.detail
        console.print(
            Panel(
                f"  [dim]Source[/dim]              [bold]{detail.get('source_project', '')}[/bold]\n"
                f"  [dim]Query[/dim]               \"{detail.get('query', '')}\"\n"
                f"  [dim]Matching commits[/dim]    {detail.get('matching_commits', 0)}\n"
                f"  [dim]Messages injected[/dim]   [bold #55AA55]{detail.get('injected_messages', 0)}[/bold #55AA55]\n"
                f"  [dim]Commit[/dim]              [#CCAA44]{(result.commit_hash or '')[:12]}[/#CCAA44]",
                border_style="#5C1010",
                title="[bold #55AA55]✓ Context Injected[/bold #55AA55]",
                padding=(1, 2),
            )
        )

        # Show which commits were searched
        searched = detail.get("commits_searched", [])
        if searched:
            console.print("  [dim]Commits searched:[/dim]")
            for sh in searched:
                console.print(f"    [dim]→[/dim] [#CCAA44]{sh}[/#CCAA44]")
            console.print()

        _hint(
            "The injected context is now part of your conversation.\n"
            "View it: [bold]cvc context --show[/bold]\n"
            "Your agent will use this context in future responses."
        )
    else:
        _error(result.message)
        _hint(
            "Tips:\n"
            "• Make sure the source project has CVC commits\n"
            "• Try broader search terms\n"
            "• Check with: [bold]cd <source> && cvc log[/bold]"
        )

    console.print()
    db.close()


# ---------------------------------------------------------------------------
# diff (knowledge / decision diff between commits)
# ---------------------------------------------------------------------------

@main.command()
@click.argument("hash_a")
@click.argument("hash_b", required=False, default=None)
def diff(hash_a: str, hash_b: str | None) -> None:
    """Show knowledge/decision differences between two commits.

    \b
    Compare what changed between two cognitive commits — messages added
    or removed, reasoning trace changes, source file changes, and
    metadata differences.

    If only one hash is given, compares against HEAD.

    \b
    Examples:
      cvc diff abc123 def456       # Compare two commits
      cvc diff abc123              # Compare commit against HEAD
    """
    engine, db = _get_engine()

    try:
        result = engine.diff(hash_a, hash_b)
    except ValueError as exc:
        _error(str(exc))
        _hint("Use [bold]cvc log[/bold] to find valid commit hashes.")
        db.close()
        return

    ca = result["commit_a"]
    cb = result["commit_b"]

    console.print()
    console.print(
        Panel(
            f"  [dim]From[/dim]  [#CCAA44]{ca['short']}[/#CCAA44]  {ca['message'][:60]}\n"
            f"  [dim]To  [/dim]  [#CCAA44]{cb['short']}[/#CCAA44]  {cb['message'][:60]}",
            border_style="#5C1010",
            title="[bold #CC3333]◈ Cognitive Diff[/bold #CC3333]",
            padding=(1, 2),
        )
    )

    # Messages diff
    msgs = result["messages"]
    msg_table = Table(
        box=box.SIMPLE,
        border_style="dim",
        show_header=False,
        padding=(0, 1),
    )
    msg_table.add_column("", width=3)
    msg_table.add_column("Detail")

    msg_table.add_row("[dim]Common[/dim]", f"{msgs['common_count']} messages unchanged")
    msg_table.add_row("[#55AA55]+[/#55AA55]", f"[#55AA55]{msgs['added_count']} messages added[/#55AA55]")
    msg_table.add_row("[red]−[/red]", f"[red]{msgs['removed_count']} messages removed[/red]")

    console.print(
        Panel(msg_table, border_style="dim", title="[bold]Messages[/bold]", padding=(0, 1))
    )

    # Show added messages (preview)
    if msgs["added"]:
        console.print("  [bold #55AA55]+ Added messages:[/bold #55AA55]")
        for m in msgs["added"][:5]:
            preview = m["content"][:120].replace("\n", " ")
            console.print(f"    [#55AA55]+ [{m['role']}][/#55AA55] {preview}")
        if len(msgs["added"]) > 5:
            console.print(f"    [dim]… and {len(msgs['added']) - 5} more[/dim]")
        console.print()

    if msgs["removed"]:
        console.print("  [bold red]− Removed messages:[/bold red]")
        for m in msgs["removed"][:5]:
            preview = m["content"][:120].replace("\n", " ")
            console.print(f"    [red]− [{m['role']}][/red] {preview}")
        if len(msgs["removed"]) > 5:
            console.print(f"    [dim]… and {len(msgs['removed']) - 5} more[/dim]")
        console.print()

    # Source files
    sf = result["source_files"]
    if sf["added"] or sf["removed"] or sf["modified"]:
        console.print("  [bold]Source Files:[/bold]")
        for f in sf["added"]:
            console.print(f"    [#55AA55]+ {f}[/#55AA55]")
        for f in sf["removed"]:
            console.print(f"    [red]− {f}[/red]")
        for f in sf["modified"]:
            console.print(f"    [#CCAA44]~ {f}[/#CCAA44]")
        console.print()

    # Reasoning trace
    rt = result["reasoning_trace"]
    if rt["changed"]:
        console.print("  [bold #CCAA44]⚡ Reasoning trace changed[/bold #CCAA44]")
        if rt["from"]:
            console.print(f"    [dim]From:[/dim] {rt['from'][:100]}…")
        if rt["to"]:
            console.print(f"    [dim]To:  [/dim] {rt['to'][:100]}…")
        console.print()

    # Metadata changes
    meta = result["metadata_changes"]
    if meta:
        console.print("  [bold]Metadata changes:[/bold]")
        for field, vals in meta.items():
            console.print(
                f"    {field}: [red]{vals['from']}[/red] → [#55AA55]{vals['to']}[/#55AA55]"
            )
        console.print()

    # Token delta
    td = result["token_delta"]
    if td > 0:
        console.print(f"  [dim]Token delta:[/dim] [#55AA55]+{td}[/#55AA55]")
    elif td < 0:
        console.print(f"  [dim]Token delta:[/dim] [red]{td}[/red]")
    else:
        console.print("  [dim]Token delta:[/dim] 0 (unchanged)")
    console.print()

    db.close()


# ---------------------------------------------------------------------------
# stats (analytics dashboard)
# ---------------------------------------------------------------------------

@main.command()
def stats() -> None:
    """Show an analytics dashboard for your CVC project.

    \b
    Displays aggregate statistics across all commits:
    total tokens, costs, message counts, commit types,
    providers/models used, most-discussed files, and timing patterns.

    \b
    Examples:
      cvc stats
    """
    engine, db = _get_engine()
    result = engine.stats()

    if result.get("total_commits", 0) == 0:
        _warn("No commits found. Create some commits first.")
        db.close()
        return

    console.print()

    # Header
    console.print(
        Panel(
            f"  [dim]Commits[/dim]      [bold]{result['total_commits']}[/bold]\n"
            f"  [dim]Messages[/dim]     [bold]{result['total_messages']}[/bold]\n"
            f"  [dim]Tokens[/dim]       [bold]{result['total_tokens']:,}[/bold]\n"
            f"  [dim]Est. Cost[/dim]    [bold]${result['estimated_cost_usd']:.4f}[/bold]\n"
            f"  [dim]Avg Size[/dim]     [bold]{result['average_commit_size']:.1f}[/bold] messages/commit\n"
            f"  [dim]Branch[/dim]       [bold]{result['current_branch']}[/bold] ({result['current_context_messages']} msgs in context)",
            border_style="#5C1010",
            title="[bold #CC3333]📊 CVC Analytics Dashboard[/bold #CC3333]",
            padding=(1, 2),
        )
    )

    # Time span
    ts = result.get("time_span", {})
    if ts:
        console.print(
            f"  [dim]Period[/dim]    {ts.get('first_commit', '?')} → {ts.get('last_commit', '?')}"
            f"  ({ts.get('span_days', 0)} days, {ts.get('commits_per_day', 0)} commits/day)"
        )
        console.print()

    # Tables side by side
    # Commit types
    ct = result.get("commit_types", {})
    if ct:
        type_table = Table(
            box=box.SIMPLE,
            border_style="dim",
            title="[bold]Commit Types[/bold]",
            title_style="bold",
            show_header=True,
            header_style="dim",
        )
        type_table.add_column("Type", style="bold")
        type_table.add_column("Count", justify="right")
        for t, c in ct.items():
            type_table.add_row(t, str(c))
        console.print(type_table)

    # Messages by role
    mr = result.get("messages_by_role", {})
    if mr:
        role_table = Table(
            box=box.SIMPLE,
            border_style="dim",
            title="[bold]Messages by Role[/bold]",
            title_style="bold",
            show_header=True,
            header_style="dim",
        )
        role_table.add_column("Role", style="bold")
        role_table.add_column("Count", justify="right")
        for r, c in mr.items():
            role_table.add_row(r, str(c))
        console.print(role_table)

    # Providers & Models
    providers = result.get("providers", {})
    models = result.get("models", {})
    if providers or models:
        pm_table = Table(
            box=box.SIMPLE,
            border_style="dim",
            title="[bold]Providers & Models[/bold]",
            title_style="bold",
            show_header=True,
            header_style="dim",
        )
        pm_table.add_column("Provider/Model", style="bold")
        pm_table.add_column("Commits", justify="right")
        for p, c in providers.items():
            pm_table.add_row(f"[#CC3333]{p}[/#CC3333]", str(c))
        for m, c in models.items():
            pm_table.add_row(f"  └ {m}", str(c))
        console.print(pm_table)

    # Branches
    br = result.get("branches", {})
    if br:
        console.print(
            f"  [bold]Branches:[/bold] {br['total']} total "
            f"({br['active']} active, {br['merged']} merged)"
        )
        branch_names = br.get("names", [])
        if branch_names:
            for bn in branch_names[:10]:
                marker = " [#55AA55]◄[/#55AA55]" if bn == result.get("current_branch") else ""
                console.print(f"    [dim]→[/dim] {bn}{marker}")
        console.print()

    # Top files
    tf = result.get("top_files", {})
    if tf:
        file_table = Table(
            box=box.SIMPLE,
            border_style="dim",
            title="[bold]Most Referenced Files[/bold]",
            title_style="bold",
            show_header=True,
            header_style="dim",
        )
        file_table.add_column("File", style="bold")
        file_table.add_column("Refs", justify="right")
        for f, c in list(tf.items())[:10]:
            file_table.add_row(f, str(c))
        console.print(file_table)

    # Peak hours
    ph = result.get("peak_hours", [])
    if ph:
        console.print("  [bold]Peak Coding Hours:[/bold]")
        for item in ph:
            h = item["hour"]
            c = item["commits"]
            bar = "█" * min(c, 30)
            console.print(f"    [dim]{h:02d}:00[/dim]  {bar} ({c})")
        bd = result.get("busiest_day", "N/A")
        console.print(f"    [dim]Busiest day:[/dim] [bold]{bd}[/bold]")
        console.print()

    # Tags
    tags = result.get("top_tags", {})
    if tags:
        tag_str = ", ".join(f"[#CCAA44]{t}[/#CCAA44]({c})" for t, c in tags.items())
        console.print(f"  [bold]Tags:[/bold] {tag_str}")
        console.print()

    db.close()


# ---------------------------------------------------------------------------
# compact (AI-powered context compression)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--smart/--no-smart", default=True, help="Use smart heuristic compression (default: smart).")
@click.option("--keep-recent", "-k", default=10, type=int, help="Number of recent messages to always keep.")
@click.option("--target-ratio", "-r", default=0.5, type=float, help="Target compression ratio (0.0-1.0).")
def compact(smart: bool, keep_recent: int, target_ratio: float) -> None:
    """Compress your context window to reduce token usage.

    \b
    Smart compression preserves important messages (decisions, code,
    architecture notes) while summarising routine conversation.

    \b
    Modes:
      --smart       Heuristic analysis: keeps decisions + code + recent (default)
      --no-smart    Simple truncation: keeps only the N most recent messages

    \b
    Examples:
      cvc compact --smart                    # Smart compression (default)
      cvc compact --no-smart --keep-recent 5 # Keep only last 5 messages
      cvc compact -k 20                      # Keep 20 recent messages
    """
    engine, db = _get_engine()

    original = len(engine.context_window)
    original_tokens = sum(len(m.content.split()) for m in engine.context_window)

    console.print()
    console.print(
        f"  [bold #CC3333]Compacting context[/bold #CC3333]\n"
        f"  [dim]Mode[/dim]      {'Smart (heuristic)' if smart else 'Simple truncation'}\n"
        f"  [dim]Current[/dim]   {original} messages (~{original_tokens} tokens)\n"
        f"  [dim]Keep[/dim]      {keep_recent} recent messages"
    )
    console.print()

    result = engine.compact(smart=smart, keep_recent=keep_recent, target_ratio=target_ratio)

    if result.success:
        detail = result.detail
        ratio = detail.get("compression_ratio", 1.0)
        pct = (1 - ratio) * 100

        console.print(
            Panel(
                f"  [dim]Before[/dim]       {detail.get('original_messages', '?')} messages ({detail.get('original_tokens', '?')} tokens)\n"
                f"  [dim]After[/dim]        {detail.get('final_messages', '?')} messages ({detail.get('final_tokens', '?')} tokens)\n"
                f"  [dim]Saved[/dim]        [bold #55AA55]{pct:.0f}%[/bold #55AA55] token reduction\n"
                f"  [dim]Mode[/dim]         {detail.get('mode', '?')}\n"
                + (
                    f"  [dim]Preserved[/dim]    {detail.get('important_preserved', 0)} important messages\n"
                    f"  [dim]Summarised[/dim]   {detail.get('summarised_chunks', 0)} chunks\n"
                    if detail.get("mode") == "smart" else ""
                )
                + (
                    f"  [dim]Commit[/dim]       [#CCAA44]{(result.commit_hash or '')[:12]}[/#CCAA44]"
                    if result.commit_hash else ""
                ),
                border_style="#5C1010",
                title="[bold #55AA55]✓ Compacted[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        _hint("Your context window is now smaller. Future LLM calls will use fewer tokens.")
    else:
        _warn(result.message)

    console.print()
    db.close()


# ---------------------------------------------------------------------------
# timeline (ASCII timeline of all AI interactions)
# ---------------------------------------------------------------------------

@main.command()
@click.option("-n", "--limit", default=30, type=int, help="Maximum commits to show.")
def timeline(limit: int) -> None:
    """Show an ASCII timeline of all AI interactions.

    \b
    Displays a beautiful visual timeline across all branches,
    showing commits, merges, branch points, and provider/model info.

    \b
    Examples:
      cvc timeline             # Show last 30 commits
      cvc timeline -n 50       # Show last 50 commits
    """
    engine, db = _get_engine()
    result = engine.timeline(limit=limit)

    if result.get("total_commits", 0) == 0:
        _warn("No commits found.")
        db.close()
        return

    console.print()

    # Branch legend
    branches = result.get("branches", [])
    if branches:
        branch_str = "  ".join(
            f"[bold {'#55AA55' if b['is_active'] else '#CCAA44'}]{b['name']}[/bold {'#55AA55' if b['is_active'] else '#CCAA44'}]"
            f"{'◄' if b['is_active'] else ''}"
            for b in branches
        )
        console.print(f"  [dim]Branches:[/dim] {branch_str}")
        console.print()

    # Timeline
    events = result.get("events", [])

    # Assign branch colors for visual distinction
    branch_colors = ["#CC3333", "#55AA55", "#CCAA44", "#5599CC", "#AA55AA", "#CC8844"]
    branch_color_map: dict[str, str] = {}
    for i, b in enumerate(branches):
        branch_color_map[b["name"]] = branch_colors[i % len(branch_colors)]

    TYPE_ICONS = {
        "checkpoint": "●",
        "analysis": "◎",
        "generation": "◉",
        "rollback": "↺",
        "merge": "⊕",
        "anchor": "◆",
    }

    for event in events:
        icon = TYPE_ICONS.get(event["type"], event.get("icon", "●"))
        primary_branch = event["branches"][0] if event["branches"] else "?"
        color = branch_color_map.get(primary_branch, "#CC3333")

        # Branch indicator line
        if event.get("is_merge"):
            parents = event.get("parents", [])
            console.print(
                f"  [{color}]  ╔═══╗[/{color}]"
            )
            line_prefix = f"  [{color}]  ║ {icon} ║[/{color}]"
        elif event.get("is_branch_point"):
            line_prefix = f"  [{color}]  ├─{icon}─┤[/{color}]"
        else:
            line_prefix = f"  [{color}]  │ {icon} │[/{color}]"

        # Build the main line
        short = event["short"]
        msg = event["message"][:50]
        time_str = event["time_str"]
        provider = event.get("provider", "")
        model = event.get("model", "")
        pm_str = ""
        if provider and model:
            pm_str = f" [dim]({provider}/{model})[/dim]"
        elif provider:
            pm_str = f" [dim]({provider})[/dim]"

        tags = event.get("tags", [])
        tag_str = ""
        if tags:
            tag_str = " " + " ".join(f"[#CCAA44]#{t}[/#CCAA44]" for t in tags[:3])

        branch_labels = ""
        if len(event["branches"]) > 1:
            branch_labels = " [dim](" + ", ".join(event["branches"]) + ")[/dim]"

        console.print(
            f"{line_prefix}  [#CCAA44]{short}[/#CCAA44]  {msg}"
            f"  [dim]{time_str}[/dim]{pm_str}{tag_str}{branch_labels}"
        )

        if event.get("is_merge"):
            console.print(
                f"  [{color}]  ╚═══╝[/{color}]"
            )

    # Footer connector
    last_event = events[-1] if events else None
    if last_event:
        primary = last_event["branches"][0] if last_event["branches"] else "?"
        color = branch_color_map.get(primary, "#CC3333")
        console.print(f"  [{color}]  │   │[/{color}]")
        console.print(f"  [{color}]  ╰───╯[/{color}]  [dim]({result['total_commits']} commits total)[/dim]")

    console.print()
    db.close()


# ---------------------------------------------------------------------------
# sync (push/pull context to remote repository)
# ---------------------------------------------------------------------------

@main.command()
@click.argument("action", type=click.Choice(["push", "pull", "status", "remote"], case_sensitive=False))
@click.argument("remote_path", required=False, default=None)
@click.option("--name", "-n", default="origin", help="Remote name (default: origin).")
@click.option("--branch", "-b", default=None, help="Branch to sync (default: active branch).")
def sync(action: str, remote_path: str | None, name: str, branch: str | None) -> None:
    """Push/pull cognitive context to a remote repository.

    \b
    Share AI knowledge across teams. Like git push/pull but for
    AI conversation context, decisions, and reasoning.

    \b
    Actions:
      push     Push local commits to a remote CVC repository
      pull     Pull remote commits into local repository
      status   Show sync status with configured remotes
      remote   Add/show a named remote (requires path argument)

    \b
    Examples:
      cvc sync push /shared/team-cvc                  # Push to shared dir
      cvc sync pull /shared/team-cvc                  # Pull from shared dir
      cvc sync push //server/share/cvc --name team    # Named remote
      cvc sync pull //server/share/cvc --name team
      cvc sync remote /shared/team-cvc --name origin  # Register a remote
      cvc sync status                                 # Show sync status
    """
    engine, db = _get_engine()

    if action == "status":
        result = engine.sync_status(remote_name=name)
        console.print()

        if not result.get("configured"):
            _warn("No sync remotes configured.")
            _hint(
                "Set up a remote:\n"
                "  [bold]cvc sync push /path/to/shared/repo[/bold]\n"
                "  [bold]cvc sync remote /path/to/shared/repo --name origin[/bold]"
            )
        else:
            remotes = result.get("remotes", [])
            remote_table = Table(
                box=box.ROUNDED,
                border_style="dim",
                show_header=True,
                header_style="bold #CC3333",
                title="[bold]Sync Remotes[/bold]",
            )
            remote_table.add_column("Name", style="bold")
            remote_table.add_column("Path")
            remote_table.add_column("Last Push", style="#55AA55")
            remote_table.add_column("Last Pull", style="#CCAA44")
            remote_table.add_column("Last Sync")

            from datetime import datetime
            for r in remotes:
                last_sync = ""
                if r.get("last_sync_at"):
                    try:
                        last_sync = datetime.fromtimestamp(r["last_sync_at"]).strftime("%Y-%m-%d %H:%M")
                    except Exception:
                        last_sync = "?"
                remote_table.add_row(
                    r["name"],
                    r["remote_path"],
                    (r.get("last_push_hash") or "—")[:12],
                    (r.get("last_pull_hash") or "—")[:12],
                    last_sync or "—",
                )
            console.print(remote_table)
        console.print()
        db.close()
        return

    if action == "remote":
        if not remote_path:
            _error("Remote path is required.")
            _hint("Usage: [bold]cvc sync remote /path/to/repo --name origin[/bold]")
            db.close()
            return

        resolved = Path(remote_path).resolve()
        db.index.upsert_remote(name, str(resolved))
        _success(f"Registered remote '[bold]{name}[/bold]' → {resolved}")
        console.print()
        db.close()
        return

    # push or pull
    if not remote_path:
        # Try to use the named remote
        remote_info = db.index.get_remote(name)
        if remote_info:
            remote_path = remote_info["remote_path"]
        else:
            _error("Remote path is required (or configure a named remote first).")
            _hint(
                "Usage: [bold]cvc sync push /path/to/shared/repo[/bold]\n"
                "   or: [bold]cvc sync remote /path --name origin[/bold] first"
            )
            db.close()
            return

    console.print()
    console.print(
        f"  [bold #CC3333]Syncing ({action})[/bold #CC3333]\n"
        f"  [dim]Remote[/dim]    [bold]{name}[/bold] ({remote_path})\n"
        f"  [dim]Branch[/dim]    {branch or engine.active_branch}"
    )
    console.print()

    if action == "push":
        result = engine.sync_push(remote_path, remote_name=name, branch=branch)
    else:
        result = engine.sync_pull(remote_path, remote_name=name, branch=branch)

    if result.success:
        detail = result.detail
        console.print(
            Panel(
                f"  [dim]Remote[/dim]     [bold]{detail.get('remote_name', name)}[/bold]\n"
                f"  [dim]Path[/dim]       {detail.get('remote_path', remote_path)}\n"
                f"  [dim]Commits[/dim]    [bold #55AA55]{detail.get('pushed_commits', detail.get('pulled_commits', 0))}[/bold #55AA55]\n"
                f"  [dim]Blobs[/dim]      {detail.get('pushed_blobs', detail.get('pulled_blobs', 0))}\n"
                f"  [dim]HEAD[/dim]       [#CCAA44]{(detail.get('head_hash', detail.get('remote_head', ''))[:12])}[/#CCAA44]",
                border_style="#5C1010",
                title=f"[bold #55AA55]✓ Sync {action.title()} Complete[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        _hint(f"Your team can now {'pull' if action == 'push' else 'use'} this context.")
    else:
        _error(result.message)

    console.print()
    db.close()


# ---------------------------------------------------------------------------
# audit (security audit trail)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--type", "-t", "event_type", default=None,
              type=click.Choice(["commit", "merge", "restore", "compact", "inject", "sync_push", "sync_pull"], case_sensitive=False),
              help="Filter by event type.")
@click.option("--risk", "-r", default=None,
              type=click.Choice(["low", "medium", "high", "critical"], case_sensitive=False),
              help="Filter by risk level.")
@click.option("--since", "-s", "since_days", default=None, type=int, help="Show events from last N days.")
@click.option("-n", "--limit", default=30, type=int, help="Max events to show.")
@click.option("--export-json", is_flag=True, help="Export audit log as JSON file.")
@click.option("--export-csv", is_flag=True, help="Export audit log as CSV file.")
@click.option("--summary", is_flag=True, help="Show summary dashboard only.")
def audit(event_type: str | None, risk: str | None, since_days: int | None,
          limit: int, export_json: bool, export_csv: bool, summary: bool) -> None:
    """Security audit trail of every AI-generated code decision.

    \b
    Enterprise-grade compliance: every AI interaction is logged with
    who, what, when, which model, risk level, and affected files.

    \b
    Features:
      • Complete audit trail of all AI decisions
      • Risk-level classification (low/medium/high/critical)
      • Code generation tracking
      • Compliance scoring
      • Export to JSON/CSV for compliance reporting

    \b
    Examples:
      cvc audit                           # View recent audit events
      cvc audit --summary                 # Compliance dashboard
      cvc audit --risk high               # Filter high-risk events
      cvc audit --type commit --since 7   # Commits from last 7 days
      cvc audit --export-json             # Export for compliance review
      cvc audit --export-csv              # Export as spreadsheet
    """
    engine, db = _get_engine()

    export_format = None
    if export_json:
        export_format = "json"
    elif export_csv:
        export_format = "csv"

    result = engine.audit(
        event_type=event_type,
        risk_level=risk,
        since_days=since_days,
        limit=limit,
        export_format=export_format,
    )

    console.print()

    # Summary dashboard
    audit_summary = result.get("summary", {})
    score = result.get("compliance_score", 100)
    assessment = result.get("risk_assessment", "")

    # Compliance score color
    if score >= 90:
        score_color = "#55AA55"
        score_icon = "✓"
    elif score >= 70:
        score_color = "#CCAA44"
        score_icon = "⚠"
    else:
        score_color = "red"
        score_icon = "✗"

    console.print(
        Panel(
            f"  [dim]Total Events[/dim]       [bold]{audit_summary.get('total_events', 0)}[/bold]\n"
            f"  [dim]Compliance Score[/dim]   [{score_color}][bold]{score_icon} {score}%[/bold][/{score_color}]\n"
            f"  [dim]Assessment[/dim]         {assessment}\n"
            f"  [dim]Code Gen Events[/dim]    {audit_summary.get('code_generation_events', 0)}\n"
            f"  [dim]Total Tokens[/dim]       {audit_summary.get('total_tokens_audited', 0):,}",
            border_style="#5C1010",
            title="[bold #CC3333]🛡️ Security Audit Dashboard[/bold #CC3333]",
            padding=(1, 2),
        )
    )

    if summary:
        # Show breakdowns
        by_type = audit_summary.get("events_by_type", {})
        if by_type:
            type_table = Table(
                box=box.SIMPLE, border_style="dim",
                title="[bold]Events by Type[/bold]", show_header=True, header_style="dim",
            )
            type_table.add_column("Type", style="bold")
            type_table.add_column("Count", justify="right")
            for t, c in by_type.items():
                type_table.add_row(t, str(c))
            console.print(type_table)

        by_risk = audit_summary.get("events_by_risk", {})
        if by_risk:
            risk_colors = {"low": "#55AA55", "medium": "#CCAA44", "high": "red", "critical": "bold red"}
            risk_table = Table(
                box=box.SIMPLE, border_style="dim",
                title="[bold]Events by Risk Level[/bold]", show_header=True, header_style="dim",
            )
            risk_table.add_column("Risk", style="bold")
            risk_table.add_column("Count", justify="right")
            for r, c in by_risk.items():
                color = risk_colors.get(r, "white")
                risk_table.add_row(f"[{color}]{r}[/{color}]", str(c))
            console.print(risk_table)

        by_provider = audit_summary.get("events_by_provider", {})
        if by_provider:
            console.print("  [bold]By Provider:[/bold]")
            for p, c in by_provider.items():
                console.print(f"    [dim]→[/dim] {p}: {c}")
            console.print()

        console.print()
        db.close()
        return

    # Event list
    events = result.get("events", [])
    if not events:
        _warn("No audit events found matching your filters.")
        _hint("Events are recorded automatically. Try: [bold]cvc commit -m 'test'[/bold] first.")
        console.print()
        db.close()
        return

    RISK_ICONS = {"low": "[#55AA55]○[/#55AA55]", "medium": "[#CCAA44]◐[/#CCAA44]", "high": "[red]●[/red]", "critical": "[bold red]◉[/bold red]"}
    EVENT_ICONS = {
        "commit": "💾", "merge": "🔀", "restore": "⏪",
        "compact": "📦", "inject": "💉", "sync_push": "⬆️", "sync_pull": "⬇️",
    }

    event_table = Table(
        box=box.ROUNDED,
        border_style="dim",
        show_header=True,
        header_style="bold #CC3333",
        title="[bold]Audit Trail[/bold]",
    )
    event_table.add_column("", width=3)
    event_table.add_column("Time", style="dim", width=16)
    event_table.add_column("Event", style="bold", width=10)
    event_table.add_column("Commit", style="#CCAA44", width=12)
    event_table.add_column("Agent", width=8)
    event_table.add_column("Provider", width=12)
    event_table.add_column("Risk", width=8)
    event_table.add_column("Code", width=4)

    for e in events:
        risk_icon = RISK_ICONS.get(e.get("risk_level", "low"), "?")
        evt_icon = EVENT_ICONS.get(e.get("event_type", ""), "📋")
        code_flag = "[#55AA55]✓[/#55AA55]" if e.get("code_generated") else "[dim]—[/dim]"
        event_table.add_row(
            risk_icon,
            e.get("time_str", "?"),
            f"{evt_icon} {e.get('event_type', '?')}",
            (e.get("commit_hash") or "—")[:12],
            e.get("agent_id", "?"),
            e.get("provider", "—") or "—",
            e.get("risk_level", "?"),
            code_flag,
        )

    console.print(event_table)

    # Export notification
    export_path = result.get("export_path")
    if export_path:
        console.print()
        _success(f"Exported audit log to [bold]{export_path}[/bold]")
        _hint("Share this file with your compliance team for review.")

    console.print()
    db.close()


# ---------------------------------------------------------------------------
# mcp (MCP server mode for auth-based IDEs)
# ---------------------------------------------------------------------------

@main.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"], case_sensitive=False),
    default="stdio",
    help="MCP transport: stdio (default) or sse.",
)
@click.option("--host", default="127.0.0.1", help="SSE transport bind host.")
@click.option("--port", default=8001, type=int, help="SSE transport bind port.")
def mcp(transport: str, host: str, port: int) -> None:
    """Start CVC as an MCP server for AI agent IDEs.

    MCP (Model Context Protocol) lets authentication-based IDEs like
    Antigravity, Windsurf, GitHub Copilot (native), and Cursor use
    CVC's cognitive versioning without API endpoint redirection.

    The IDE's built-in agent calls CVC tools (commit, branch, merge,
    restore, status, log) through the MCP protocol.

    \b
    Transports:
      stdio  — IDE launches 'cvc mcp' as a subprocess (default)
      sse    — HTTP Server-Sent Events on localhost:8001

    \b
    IDE configuration examples:

      VS Code (settings.json):
        "mcp": {"servers": {"cvc": {"command": "cvc", "args": ["mcp"]}}}

      Antigravity / Windsurf / Cursor (MCP config):
        {"mcpServers": {"cvc": {"command": "cvc", "args": ["mcp"]}}}
    """
    from cvc.mcp_server import run_mcp_sse, run_mcp_stdio

    if transport == "sse":
        _banner("MCP Server (SSE)")
        console.print(
            Panel(
                f"  Transport  [bold #CC3333]SSE[/bold #CC3333]\n"
                f"  Endpoint   [bold #CC3333]http://{host}:{port}/sse[/bold #CC3333]\n"
                f"  Messages   [bold #CC3333]http://{host}:{port}/messages[/bold #CC3333]",
                border_style="#5C1010",
                title="[bold #55AA55]MCP Server[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        console.print()
        run_mcp_sse(host=host, port=port)
    else:
        # stdio transport — no banner (stdout is the protocol channel)
        run_mcp_stdio()


# ---------------------------------------------------------------------------
# doctor (system health check)
# ---------------------------------------------------------------------------

@main.command()
def doctor() -> None:
    """Check your CVC installation and environment."""
    from cvc.adapters import PROVIDER_DEFAULTS
    from cvc.core.models import GlobalConfig, discover_cvc_root, get_global_config_dir

    _banner("System Check")

    checks: list[tuple[str, bool, str]] = []

    # Python version
    py = sys.version.split()[0]
    py_ok = sys.version_info >= (3, 11)
    checks.append(("Python", py_ok, f"{py}  {'✓ 3.11+' if py_ok else '✗ Need 3.11+'}"))

    # Global config
    gc_dir = get_global_config_dir()
    gc_exists = (gc_dir / "config.json").exists()
    gc = GlobalConfig.load()  # Returns defaults if file missing
    if gc_exists:
        checks.append(("Global config", True, f"{gc_dir}  (provider={gc.provider})"))
    else:
        checks.append(("Global config", False, "Not found — run: cvc setup"))

    # .cvc directory (project-level)
    project_root = discover_cvc_root()
    if project_root:
        checks.append(("Project .cvc/", True, f"Found at {project_root / '.cvc'}"))
    else:
        checks.append(("Project .cvc/", False, "Not found — run: cvc init"))

    # Git
    try:
        import subprocess
        subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, check=True, **HIDDEN_KW)
        checks.append(("Git repository", True, "Found"))
    except Exception:
        checks.append(("Git repository", False, "Not a Git repo (VCS bridge won't work)"))

    # Provider API keys (check env + stored)
    for prov, defaults in PROVIDER_DEFAULTS.items():
        env_key_name = defaults.get("env_key", "")
        if env_key_name:
            has_env = bool(os.environ.get(env_key_name))
            has_stored = bool(gc.api_keys.get(prov)) if gc_exists else False
            if has_env:
                checks.append((f"{prov.title()} key", True, f"{env_key_name} ● env var set"))
            elif has_stored:
                checks.append((f"{prov.title()} key", True, "● saved in global config"))
            else:
                checks.append((f"{prov.title()} key", False, f"{env_key_name} ○ not set"))

    # Ollama
    try:
        import httpx
        r = httpx.get("http://localhost:11434/api/tags", timeout=2)
        models = [m["name"] for m in r.json().get("models", [])]
        checks.append(("Ollama", True, f"Running — {len(models)} model(s) loaded"))
    except Exception:
        checks.append(("Ollama", False, "Not running (optional)"))

    # Display results
    table = Table(
        box=box.ROUNDED,
        border_style="dim",
        show_header=True,
        header_style="bold #CC3333",
    )
    table.add_column("", width=3)
    table.add_column("Check", style="bold")
    table.add_column("Status")

    for name, ok, detail in checks:
        icon = "[#55AA55]✓[/#55AA55]" if ok else "[red]✗[/red]"
        table.add_row(icon, name, detail)

    console.print(table)
    console.print()

    all_ok = all(ok for _, ok, _ in checks[:3])  # Python + global config + .cvc/
    if all_ok:
        _success("CVC is ready to go!")
    else:
        _warn("Some checks failed. See details above.")

    console.print()


# ---------------------------------------------------------------------------
# launch (zero-config auto-launch for any AI tool)
# ---------------------------------------------------------------------------

@main.command()
@click.argument("tool", required=False, default=None)
@click.option("--host", default="127.0.0.1", help="Gateway bind host.")
@click.option("--port", default=13421, type=int, help="Gateway bind port.")
@click.option("--no-time-machine", is_flag=True, help="Disable aggressive auto-commit.")
@click.argument("extra_args", nargs=-1, type=click.UNPROCESSED)
def launch(tool: str | None, host: str, port: int, no_time_machine: bool, extra_args: tuple[str, ...]) -> None:
    """Zero-config auto-launch: start any AI tool through CVC.

    \b
    Examples:
      cvc launch claude       # Launch Claude Code CLI with CVC
      cvc launch aider        # Launch Aider through CVC proxy
      cvc launch codex        # Launch OpenAI Codex CLI through CVC
      cvc launch cursor       # Open Cursor with CVC auto-configured
      cvc launch code         # Open VS Code with Copilot BYOK configured

    CVC automatically:
      1. Starts the Gateway daemon (if not running)
      2. Registers the current workspace with the Gateway
      3. Configures the tool's environment variables / config files
      4. Launches the tool — every conversation is time-machined
    """
    from cvc.launcher import exec_tool, launch_tool, list_launchable_tools, resolve_tool

    _banner("Time Machine Launcher")

    # If no tool specified, show interactive picker
    if tool is None:
        tools = list_launchable_tools()

        console.print("  [bold white]Pick an AI tool to launch through CVC:[/bold white]\n")

        # Group by kind
        cli_tools = [t for t in tools if t["kind"] == "cli"]
        ide_tools = [t for t in tools if t["kind"] == "ide"]

        idx = 1
        index_map: dict[int, str] = {}

        if cli_tools:
            console.print("  [bold #CC3333]CLI Tools[/bold #CC3333]")
            for t in cli_tools:
                status = "[#55AA55]●[/#55AA55]" if t["installed"] else "[red]○[/red]"
                console.print(
                    f"    [#CC3333]{idx}[/#CC3333]  {status}  [bold]{t['name']}[/bold]  "
                    f"[dim]({t['binary']})[/dim]"
                )
                index_map[idx] = t["key"]
                idx += 1
            console.print()

        if ide_tools:
            console.print("  [bold #CCAA44]IDEs[/bold #CCAA44]")
            for t in ide_tools:
                status = "[#55AA55]●[/#55AA55]" if t["installed"] else "[red]○[/red]"
                console.print(
                    f"    [#CCAA44]{idx}[/#CCAA44]  {status}  [bold]{t['name']}[/bold]  "
                    f"[dim]({t['binary']})[/dim]"
                )
                index_map[idx] = t["key"]
                idx += 1
            console.print()

        console.print("  [dim]● = installed   ○ = not found on PATH[/dim]")
        console.print()

        from cvc.agent.menus import arrow_select
        launch_opts = []
        for idx_key in sorted(index_map.keys()):
            tool_key = index_map[idx_key]
            for t in cli_tools + ide_tools:
                if t["key"] == tool_key:
                    status_mark = "●" if t["installed"] else "○"
                    launch_opts.append((f"{status_mark} {t['name']} ({t['binary']})", tool_key))
                    break
            else:
                launch_opts.append((tool_key, tool_key))
        choice_val = arrow_select("Pick a tool", launch_opts, default=0)
        if choice_val is None:
            return
        tool = choice_val
        console.print()

    # Resolve alias
    resolved = resolve_tool(tool)
    if resolved is None:
        _error(f"Unknown tool: [bold]{tool}[/bold]")
        _info("Run [bold]cvc launch[/bold] (no arguments) to see available tools.")
        return

    console.print(f"  [bold]Launching[/bold] [#CC3333]{resolved}[/#CC3333] through CVC…")
    console.print()

    time_machine = not no_time_machine

    result = launch_tool(
        resolved,
        host=host,
        port=port,
        extra_args=list(extra_args) if extra_args else None,
        time_machine=time_machine,
    )

    # Handle tuple return (CLI tools return (report, cmd, env))
    cmd = None
    child_env = None
    if isinstance(result, tuple):
        result, cmd, child_env = result

    if not result["success"]:
        _error(result.get("error", "Launch failed"))
        return

    # Show what happened
    steps = result.get("steps", [])
    if "auto_passthrough_config" in steps:
        _success("Auto-configured CVC in [bold]passthrough mode[/bold] (no API key needed)")
    if "auto_init" in steps:
        _success("Auto-initialised .cvc/ in current directory")
    if "gateway_running" in steps:
        _success(f"CVC Gateway running at [bold #CC3333]{result['endpoint']}[/bold #CC3333]")
    if "workspace_registered" in steps:
        ws_id = result.get("workspace_id", "")
        _success(f"Workspace registered: [bold #CC3333]{ws_id}[/bold #CC3333]")

    if time_machine:
        _success("Time Machine mode: [bold]ON[/bold] (auto-commit every 3 turns)")

    # Show env overrides
    env_overrides = result.get("env_overrides", {})
    if env_overrides:
        for k, v in env_overrides.items():
            _info(f"[dim]{k}[/dim] = [#CC3333]{v}[/#CC3333]")

    # Show auto-config results
    auto_config = result.get("auto_config", {})
    for action in auto_config.get("actions", []):
        _success(action)
    if "manual_step" in auto_config:
        _warn(auto_config["manual_step"])

    console.print()

    # For CLI tools, exec into the tool
    if cmd and child_env:
        console.print(
            Panel(
                f"  [bold white]{result['tool']}[/bold white] is launching…\n"
                f"  [dim]All conversations flow through CVC automatically.[/dim]\n"
                f"  [dim]Use /cvc commands or CVC tools for version control.[/dim]",
                border_style="#5C1010",
                title="[bold #55AA55]Time Machine Active[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        console.print()
        exit_code = exec_tool(cmd, child_env)
        raise SystemExit(exit_code)
    else:
        # IDE was launched
        console.print(
            Panel(
                f"  [bold white]{result['tool']}[/bold white] has been opened.\n"
                f"  [dim]CVC proxy is running in the background.[/dim]\n"
                f"  [dim]Conversations will be auto-saved by the Time Machine.[/dim]",
                border_style="#5C1010",
                title="[bold #55AA55]Time Machine Active[/bold #55AA55]",
                padding=(1, 2),
            )
        )
        console.print()


# ---------------------------------------------------------------------------
# up (one-command start: setup + init + serve)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--host", default="127.0.0.1", help="Gateway bind host.")
@click.option("--port", default=13421, type=int, help="Gateway bind port.")
@click.option("--time-machine/--no-time-machine", default=True, help="Enable Time Machine auto-commit.")
def up(host: str, port: int, time_machine: bool) -> None:
    """One-command start: setup (if needed) + init (if needed) + gateway.

    \b
    This is the fastest way to get CVC running:
      $ cvc up

    If CVC hasn't been set up yet, it runs the setup wizard first.
    If the current project has no .cvc/, it initialises one.
    Then it starts the Gateway with Time Machine enabled.
    """
    from cvc.core.models import CVCConfig, GlobalConfig, discover_cvc_root, get_global_config_dir

    _banner("One-Command Start")

    # Step 1: Check setup
    gc_path = get_global_config_dir() / "config.json"
    if not gc_path.exists():
        console.print("  [#CCAA44]First-time setup required.[/#CCAA44]")
        console.print()
        click.get_current_context().invoke(setup)
        console.print()
        # Re-check after setup
        if not gc_path.exists():
            _error("Setup was not completed. Run [bold]cvc setup[/bold] manually.")
            return

    gc = GlobalConfig.load()
    _success(f"Config: [bold]{gc.provider}[/bold] / [bold]{gc.model}[/bold]")

    # Step 2: Check init
    project_root = discover_cvc_root()
    if project_root is None:
        config = CVCConfig.for_project(project_root=Path.cwd())
        config.ensure_dirs()
        from cvc.core.database import ContextDatabase
        ContextDatabase(config).close()
        _success(f"Initialised .cvc/ at [dim]{Path.cwd()}[/dim]")
    else:
        _success(f"Project CVC found at [dim]{project_root}[/dim]")

    # Step 3: Set Time Machine env
    if time_machine:
        os.environ["CVC_TIME_MACHINE"] = "1"
        _success("Time Machine mode: [bold]ON[/bold]")

    console.print()

    # Step 4: Start the Gateway
    click.get_current_context().invoke(gateway_start, host=host, port=port, proxy_port=port, no_browser=False, log=True)


# ---------------------------------------------------------------------------
# sessions (view Time Machine session history)
# ---------------------------------------------------------------------------

@main.command()
@click.option("--host", default="127.0.0.1", help="Gateway host.")
@click.option("--port", default=13421, type=int, help="Gateway port.")
def sessions(host: str, port: int) -> None:
    """View Time Machine session history.

    Shows all agent sessions tracked by the CVC Gateway, including
    which tool was used, message counts, and auto-commit stats.

    The Gateway must be running for this command to work.
    """
    from datetime import datetime

    import httpx

    _banner("Session History")

    endpoint = f"http://{host}:{port}"

    try:
        r = httpx.get(f"{endpoint}/cvc/sessions", timeout=5.0)
        r.raise_for_status()
        data = r.json()
    except httpx.ConnectError:
        _error(f"CVC Gateway is not running on {endpoint}")
        _hint("Start the gateway: [bold]cvc gateway start[/bold] or [bold]cvc up[/bold]")
        return
    except Exception as exc:
        _error(f"Failed to fetch sessions: {exc}")
        return

    # Config info
    tm_status = "[bold #55AA55]ON[/bold #55AA55]" if data.get("time_machine") else "[dim]OFF[/dim]"
    interval = data.get("auto_commit_interval", "?")
    console.print(
        Panel(
            f"  Time Machine    {tm_status}\n"
            f"  Auto-commit     every [bold]{interval}[/bold] assistant turns\n"
            f"  Session timeout [dim]{data.get('session_timeout_seconds', '?')}s[/dim]",
            border_style="#8B0000",
            title="[bold white]Configuration[/bold white]",
            padding=(0, 2),
        )
    )
    console.print()

    session_list = data.get("sessions", [])
    if not session_list:
        _warn("No sessions recorded yet.")
        _info("Sessions are tracked when tools send requests through the proxy.")
        return

    table = Table(
        box=box.ROUNDED,
        border_style="dim",
        show_header=True,
        header_style="bold #CC3333",
    )
    table.add_column("#", width=4)
    table.add_column("Tool", style="#CC3333", width=12)
    table.add_column("Started", width=20)
    table.add_column("Messages", justify="right", width=10)
    table.add_column("Commits", justify="right", width=10)
    table.add_column("Status", width=10)

    for s in session_list:
        started = datetime.fromtimestamp(s["started_at"]).strftime("%Y-%m-%d %H:%M") if s.get("started_at") else "?"
        status_str = "[bold #55AA55]active[/bold #55AA55]" if s.get("active") else "[dim]ended[/dim]"
        table.add_row(
            str(s.get("id", "?")),
            s.get("tool", "?"),
            started,
            str(s.get("messages", 0)),
            str(s.get("commits", 0)),
            status_str,
        )

    console.print(table)
    console.print(f"\n  [dim]{len(session_list)} session(s) total[/dim]\n")


# ── Docs (Input Grounding) ──────────────────────────────────────────────

@main.group()
def docs() -> None:
    """API documentation tools for input grounding (anti-hallucination)."""
    pass


@docs.command("search")
@click.argument("query")
def docs_search(query: str) -> None:
    """Search for available API documentation."""
    from rich import box
    from rich.console import Console
    from rich.table import Table

    console = Console()
    try:
        from cvc.agent.api_docs import search_docs
        results = search_docs(query)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not results:
        console.print(f"[yellow]No documentation found matching '{query}'.[/yellow]")
        return

    table = Table(box=box.ROUNDED, title=f"Docs matching '{query}'", border_style="dim")
    table.add_column("ID", style="bold cyan")
    table.add_column("Title", style="white")
    for r in results[:30]:
        table.add_row(r["id"], r.get("title", "—"))
    console.print(table)


@docs.command("get")
@click.argument("doc_id")
@click.option("--lang", "-l", default="python", help="Language variant.")
@click.option("--section", "-s", default=None, help="Fetch only a specific section.")
def docs_get(doc_id: str, lang: str, section: str | None) -> None:
    """Fetch API documentation by ID."""
    from rich.console import Console
    from rich.markdown import Markdown

    console = Console()
    try:
        from cvc.agent.api_docs import fetch_doc
        content = fetch_doc(doc_id, language=lang, section=section)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not content:
        console.print(f"[yellow]No documentation found for '{doc_id}'.[/yellow]")
        return

    console.print(Markdown(content))


@docs.command("annotate")
@click.argument("doc_id")
@click.argument("note")
def docs_annotate(doc_id: str, note: str) -> None:
    """Save a note/gotcha about an API doc for future reference."""
    from rich.console import Console

    console = Console()
    try:
        from cvc.agent.api_docs import annotate_doc
        annotate_doc(doc_id, note)
        console.print(f"[green]Annotation saved for '{doc_id}'.[/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


@docs.command("detect")
@click.option("--workspace", "-w", default=".", help="Workspace path to scan.")
def docs_detect(workspace: str) -> None:
    """Auto-detect APIs used by the project and show available docs."""
    from pathlib import Path

    from rich import box
    from rich.console import Console
    from rich.table import Table

    console = Console()
    try:
        from cvc.agent.api_docs import detect_project_apis
        apis = detect_project_apis(Path(workspace))
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        return

    if not apis:
        console.print("[yellow]No known APIs detected in this project.[/yellow]")
        return

    table = Table(box=box.ROUNDED, title="Detected APIs", border_style="dim")
    table.add_column("Package", style="bold cyan")
    table.add_column("Doc ID", style="white")
    for entry in apis:
        table.add_row(entry["package"], entry["doc_id"])
    console.print(table)


@docs.command("import")
@click.argument("path", type=click.Path(exists=True))
@click.argument("doc_id")
def docs_import(path: str, doc_id: str) -> None:
    """Import a local markdown file as API documentation."""
    from pathlib import Path

    from rich.console import Console

    console = Console()
    try:
        from cvc.agent.api_docs import import_doc
        content = Path(path).read_text(encoding="utf-8")
        import_doc(doc_id, content)
        console.print(f"[green]Imported '{path}' as '{doc_id}'.[/green]")
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")


# ── Authentication ─────────────────────────────────────────────────────────

@main.command("login")
def auth_login() -> None:
    """Sign in to CVC using Google or GitHub."""
    from cvc.auth import login_flow
    login_flow()

@main.command("auth")
def auth_cmd() -> None:
    """Re-authenticate to CVC using Google or GitHub."""
    from cvc.auth import login_flow
    login_flow()


@main.command("logout")
def auth_logout() -> None:
    """Sign out from CVC."""
    from cvc.auth import logout
    logout()


@main.command("update")
def update_cvc() -> None:
    """Update CVC to the latest version.

    One command. Live-installs in front of the user. Ends with the
    final "Updated CVC vA -> vB" line in the same terminal.

    On macOS / Linux this is a simple synchronous pipe -- Unix lets you
    unlink a running binary, so the file-lock issue does not exist.

    On Windows the running cvc.exe holds a file lock on its own DLLs,
    which blocks `uv tool install` from replacing them. We MUST die
    before the install can succeed.

    The pattern is "parent dies, replacer inherits the console":

    1. We write a replacer PS1 to a stable location under %LOCALAPPDATA%.
    2. We spawn it with CREATE_NEW_PROCESS_GROUP, inheriting stdio so
       its output streams to the user's terminal.
    3. We exit IMMEDIATELY (no `replacer.wait()` -- that would deadlock
       against the file lock). This releases the file lock on the venv.
    4. The shell prompt comes back ~1s after our exit. The replacer is
       meanwhile sleeping 2s and then starts the install. By the time
       the install runs, the parent is dead and the file lock is
       released. The user sees their prompt appear, then the install
       output appears (overwriting the prompt visually in PowerShell).
    5. On success the replacer prints the green "Updated CVC vA -> vB"
       line and exits 0.

    Why we can't block on `replacer.wait()`:
    If we did, the parent (us) stays alive in `replacer.wait()`. The
    replacer then tries to run `uv tool install` but the parent's
    file handles on the venv DLLs are still open, so uv can't replace
    them. The install hangs forever. The user has to Ctrl-C.

    Why a 2s sleep in the replacer:
    It gives the parent (us) time to die and the OS to close the file
    handles. 2s is enough on every machine we've seen. If not, the
    install will fail and the user can simply run `cvc update` again.
    """
    import os
    import subprocess
    import sys
    from pathlib import Path

    console.print("\n[bold #CC3333]CVC Update[/bold #CC3333]\n")
    console.print("[bold]* Installing CVC...[/bold]\n")

    if sys.platform != "win32":
        # macOS / Linux: synchronous pipe. The installer's own output
        # (Write-Host / Write-CvcInfo calls) streams straight to the
        # user's terminal because stdin/stdout/stderr are inherited.
        rc = subprocess.call(
            ["bash", "-c", "set -o pipefail; curl -fsSL https://jaimeena.com/cvc/install.sh | bash"]
        )
        if rc != 0:
            console.print(f"\n[bold red]Update failed with exit code {rc}.[/bold red]")
            console.print("[dim]Manual fallback: curl -fsSL https://jaimeena.com/cvc/install.sh | bash[/dim]")
            raise SystemExit(1)
        return

    # ------------------------------------------------------------------
    # Windows: parent-dies, replacer-inherits-console pattern.
    # ------------------------------------------------------------------

    launcher_dir = Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "cvc" / "update"
    launcher_dir.mkdir(parents=True, exist_ok=True)
    replacer_ps1 = launcher_dir / "cvc-update-replacer.ps1"

    # Capture the current version BEFORE we exit, so the replacer can
    # include it in the final summary even though it's running fresh
    # code by then.
    before_version = None
    try:
        from cvc import __version__ as _v
        before_version = str(_v)
    except Exception:
        pass

    # The replacer body -- PowerShell. Runs after this cvc.exe exits.
    # Output is streamed to the user's terminal (the parent's console
    # is inherited) so the user sees a single continuous stream:
    #
    #   * Installing CVC...
    #   [shell prompt returns briefly]
    #   Preparing update (releasing file lock)...
    #   Downloading installer...
    #   Running installer...
    #   ...
    #   Updated CVC v2.91.29 -> v2.91.31
    #   <prompt>
    #
    # NOTE on backticks: We cannot embed literal backticks in the Python
    # source string because bash (which runs the test command) treats
    # them as command substitution. The PowerShell we need requires
    # backtick-r and backtick-n inside the [Console]::Write call, so we
    # build those with chr(96) at runtime -- same effect, no bash trap.
    _BT = chr(96)  # backtick character, used by PowerShell escapes
    replacer_body = (
        '$ErrorActionPreference = "Continue"\n'
        '$oldVersion = $env:CVC_OLD_VERSION\n'
        '\n'
        'function Fail($msg) { Write-Host $msg -ForegroundColor Red; exit 1 }\n'
        'function Info($msg) { Write-Host $msg -ForegroundColor Cyan }\n'
        'function Ok($msg)   { Write-Host $msg -ForegroundColor Green }\n'
        '\n'
        '# 0. Clear the line. The parent cvc.exe just died and the user\'s\n'
        '#    shell prompt has come back ("PS C:\\Users\\jk422>" in the\n'
        '#    console). We are about to print our own output, but if we\n'
        '#    do not first overwrite the prompt line, the user sees\n'
        '#    "PS C:\\Users\\jk422>Preparing update..." which looks like\n'
        '#    a corrupt terminal. The [Console]::Write below returns the\n'
        '#    cursor to column 0, writes 120 spaces to overwrite even long\n'
        '#    prompts, then re-positions. Works on PowerShell 5.1 and 7+\n'
        '#    in both classic and Windows Terminal.\n'
        f'[Console]::Write("{_BT}r" + (" " * 120) + "{_BT}r")\n'
        '\n'
        '# 1. Wait for the parent cvc.exe to exit and release the file\n'
        '#    lock on the venv DLLs. 2s is enough on every machine\n'
        '#    we have seen.\n'
        'Info "Preparing update (releasing file lock)..."\n'
        'Start-Sleep -Seconds 2\n'
        '\n'
        '# 2. Self-heal pass. If the venv is half-broken (missing\n'
        '#    pyvenv.cfg or missing cvc.exe entrypoint), nuke the tool\n'
        '#    dir so the install below can create a clean one.\n'
        '$toolRoot = Join-Path $env:APPDATA "uv\\tools\\tm-ai"\n'
        'if (Test-Path $toolRoot) {\n'
        '    $pyvenv   = Join-Path $toolRoot "pyvenv.cfg"\n'
        '    $entryExe = Join-Path (Join-Path $toolRoot "Scripts") "cvc.exe"\n'
        '    $broken = (-not (Test-Path $pyvenv)) -or (-not (Test-Path $entryExe))\n'
        '    if ($broken) {\n'
        '        Info "Detected half-broken CVC install -- cleaning up before reinstall"\n'
        '        $removed = $false\n'
        '        for ($i = 0; $i -lt 3; $i++) {\n'
        '            try { Remove-Item $toolRoot -Recurse -Force -ErrorAction Stop; $removed = $true; break }\n'
        '            catch { Start-Sleep -Milliseconds 500 }\n'
        '        }\n'
        '        if (-not $removed) {\n'
        '            Write-Host "Warning: could not fully remove broken venv -- uv will overwrite what it can." -ForegroundColor Yellow\n'
        '        }\n'
        '    }\n'
        '}\n'
        '$staleShim = Join-Path $env:USERPROFILE ".local\\bin\\cvc.exe.old"\n'
        'if (Test-Path $staleShim) {\n'
        '    try { Remove-Item $staleShim -Force -ErrorAction SilentlyContinue } catch {}\n'
        '}\n'
        '\n'
        '# 3. Download the live installer from the website and run it.\n'
        '#    Output streams live to the user\'s terminal (we inherited\n'
        '#    the parent\'s console when we were spawned).\n'
        '#\n'
        '#    IMPORTANT: fetch install.bat, NOT install.ps1. The website\n'
        '#    serves a tiny PowerShell wrapper for the .bat URL (any\n'
        '#    PowerShell user-agent). The wrapper does the actual\n'
        '#    install.ps1 download via `irm -OutFile` and then runs it\n'
        '#    with `& $ps1` so `#` comments are parsed correctly. If\n'
        '#    we fetched install.ps1 directly and ran it via iex, PS\n'
        '#    5.1 would throw "ObjectNotFound (#:String)" on the first\n'
        '#    comment line -- looks like a fatal error to the user even\n'
        '#    though the rest of the script runs fine.\n'
        '$wrapperUrl = "https://jaimeena.com/cvc/install.bat"\n'
        '$wrapperPath = Join-Path $env:TEMP "cvc-update-wrapper.ps1"\n'
        'try {\n'
        '    Info "Downloading installer..."\n'
        '    irm $wrapperUrl -OutFile $wrapperPath -ErrorAction Stop\n'
        '} catch {\n'
        '    Fail ("Failed to download installer: {0}" -f $_.Exception.Message)\n'
        '}\n'
        'if (-not (Test-Path $wrapperPath)) { Fail "Downloaded installer not found at $wrapperPath" }\n'
        '# The wrapper fetches the real installer to $env:TEMP\\cvc-install.ps1\n'
        '# and runs it via `& $ps1`. We track that path so we can verify\n'
        '# the real installer actually ran (and didn\'t get short-circuited).\n'
        '$ps1 = Join-Path $env:TEMP "cvc-install.ps1"\n'
        '\n'
        '# Run the installer. Its Write-Host output appears directly in\n'
        '# the user\'s terminal. install.ps1 ends with a Write-Host, which\n'
        '# leaves $LASTEXITCODE at -1 on PowerShell 5.1 even on success --\n'
        '# treat -1 as 0 when the script ran to completion.\n'
        'Info "Running installer..."\n'
        '$rc = 0\n'
        'try {\n'
        '    & $ps1\n'
        '    if ($LASTEXITCODE -ne 0 -and $LASTEXITCODE -ne -1) { $rc = $LASTEXITCODE }\n'
        '} catch {\n'
        '    Fail ("Installer crashed: {0}" -f $_.Exception.Message)\n'
        '}\n'
        '\n'
        '# 4. Print the final summary. We re-run cvc --version in a fresh\n'
        '#    interpreter (it picks up the newly installed code from disk)\n'
        '#    and diff against $oldVersion captured before the install.\n'
        'Write-Host ""\n'
        '$cvcExe = Get-Command cvc -ErrorAction SilentlyContinue\n'
        '$newVersion = ""\n'
        'if ($cvcExe) {\n'
        '    try { $newVersion = (& $cvcExe.Source --version 2>$null | Select-Object -First 1) -replace \'[^0-9.]\',\'\' } catch {}\n'
        '}\n'
        'if ($newVersion) {\n'
        '    if ($oldVersion -and $oldVersion -ne $newVersion) {\n'
        '        Ok ("Updated CVC v{0} -> v{1}" -f $oldVersion, $newVersion)\n'
        '    } elseif ($oldVersion) {\n'
        '        Ok ("CVC v{0} is up to date." -f $newVersion)\n'
        '    } else {\n'
        '        Ok ("CVC v{0} installed." -f $newVersion)\n'
        '    }\n'
        '}\n'
        'if ($rc -ne 0) { exit $rc }\n'
        'exit 0\n'
    )

    replacer_ps1.write_bytes(b"\xef\xbb\xbf" + replacer_body.encode("utf-8"))

    env = os.environ.copy()
    env["CVC_OLD_VERSION"] = before_version or ""

    # Spawn the replacer in a new process group so it survives our exit,
    # inheriting stdio so the install output streams to the user's
    # terminal. We do NOT call `replacer.wait()` because:
    #
    #   (a) If we did, the parent (us) stays alive in `wait()`. The
    #       replacer then can't `uv tool install` because the parent's
    #       file handles on the venv DLLs are still open. DEADLOCK --
    #       the user sees "Installing CVC..." forever.
    #
    #   (b) The replacer handles its own lifecycle. It exits when the
    #       install finishes. We exit NOW. The shell prompt comes back
    #       ~1s after our exit, then the replacer's first output
    #       appears 2-3s after that. Visually it looks like one
    #       continuous stream (PowerShell redraws the line on output).
    #
    # Use `os._exit(0)` (not `SystemExit`) to skip Python's cleanup
    # which can hang on Windows when file handles are still open.
    subprocess.Popen(
        [
            "powershell", "-NoProfile", "-ExecutionPolicy", "Bypass",
            "-File", str(replacer_ps1),
        ],
        env=env,
        creationflags=getattr(subprocess, "CREATE_NEW_PROCESS_GROUP", 0),
    )
    # Flush our output before dying so the user sees the header
    # before the shell prompt comes back.
    try:
        sys.stdout.flush()
        sys.stderr.flush()
    except Exception:
        pass
    # Hard exit -- no Python cleanup, no atexit handlers, nothing
    # that could hold a file handle open.
    os._exit(0)


@main.command("whoami")
def auth_whoami() -> None:
    """Show currently logged-in user."""
    from rich.panel import Panel

    from cvc.auth import get_current_user
    user = get_current_user()
    if user:
        content = (
            f"[bold]Name:[/bold] {user.get('display_name', 'Unknown')}\n"
            f"[bold]Email:[/bold] {user.get('email', 'Unknown')}\n"
            f"[bold]Provider:[/bold] {user.get('provider', 'Unknown').capitalize()}"
        )
        console.print(Panel(content, title="[bold #55AA55]Authenticated User[/bold #55AA55]", border_style="#55AA55", expand=False))
    else:
        console.print("Not logged in. Run [bold]cvc login[/bold] to authenticate.")


# ======================================================================
# AGENT CONFIG — scriptable tunables (mirrors `cvc setup` → Tune Agent)
# ======================================================================

@main.group("agent-config", invoke_without_command=True)
@click.pass_context
def agent_config_grp(ctx: click.Context) -> None:
    """Inspect and edit CVC agent tunables (iteration budgets, timeouts, tenacity, …)."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(agent_config_show)


@agent_config_grp.command("show")
def agent_config_show() -> None:
    """Print every tunable with current value, default, and range."""
    from cvc.core.agent_config import CvcAgentConfig, TUNABLES, sections
    cfg = CvcAgentConfig.load()
    defaults = CvcAgentConfig()  # fresh instance = factory defaults
    console.print(f"[dim]Config file: {cfg.path()}[/dim]\n")
    for section_label, fields in sections():
        console.print(f"[bold #CC3333]{section_label}[/bold #CC3333]")
        for fname in fields:
            meta = TUNABLES[fname]
            cur = getattr(cfg, fname)
            default = getattr(defaults, fname)
            marker = "" if cur == default else "  [yellow]*[/yellow]"
            rng = ""
            if meta.minimum is not None or meta.maximum is not None:
                lo = "" if meta.minimum is None else f"{meta.minimum:g}"
                hi = "" if meta.maximum is None else f"{meta.maximum:g}"
                rng = f" [dim]({lo}–{hi})[/dim]"
            console.print(f"  [white]{fname:<32}[/white] = [bold]{cur}[/bold]  [dim](default {default}){rng}[/dim]{marker}")
            console.print(f"     [dim]{meta.help}[/dim]")
        console.print()


@agent_config_grp.command("set")
@click.argument("key")
@click.argument("value")
def agent_config_set(key: str, value: str) -> None:
    """Set a single tunable: `cvc agent-config set max_agent_iterations 120`."""
    from cvc.core.agent_config import CvcAgentConfig, TUNABLES, reload_agent_config
    if key not in TUNABLES:
        _error(f"Unknown tunable: {key}")
        console.print("[dim]Run `cvc agent-config show` to list valid keys.[/dim]")
        raise SystemExit(1)
    cfg = CvcAgentConfig.load()
    try:
        cfg.set_field(key, value)
    except ValueError as exc:
        _error(str(exc))
        raise SystemExit(1)
    saved = cfg.save()
    _success(f"{key} = {getattr(cfg, key)}   [dim]→ {saved}[/dim]")
    try:
        reload_agent_config()
        from cvc.gateway import _refresh_agent_budgets
        _refresh_agent_budgets()
    except Exception:
        pass


@agent_config_grp.command("reset")
@click.option("--yes", is_flag=True, help="Skip confirmation.")
def agent_config_reset(yes: bool) -> None:
    """Reset every tunable back to its default."""
    from cvc.core.agent_config import CvcAgentConfig, reload_agent_config
    if not yes:
        from rich.prompt import Confirm
        if not Confirm.ask("Reset all agent tunables to defaults?", default=False):
            return
    cfg = CvcAgentConfig()  # fresh defaults
    saved = cfg.save()
    _success(f"Reset to defaults → [dim]{saved}[/dim]")
    try:
        reload_agent_config()
        from cvc.gateway import _refresh_agent_budgets
        _refresh_agent_budgets()
    except Exception:
        pass


@agent_config_grp.command("edit")
def agent_config_edit() -> None:
    """Open the TOML config in $EDITOR."""
    import os, subprocess
    from cvc.core.agent_config import CvcAgentConfig, reload_agent_config
    cfg = CvcAgentConfig.load()
    path = cfg.path()
    if not path.exists():
        cfg.save()  # write defaults so the user has something to edit
    editor = os.environ.get("EDITOR") or os.environ.get("VISUAL") or "nano"
    subprocess.call([editor, str(path)], **HIDDEN_KW)
    try:
        reload_agent_config()
        from cvc.gateway import _refresh_agent_budgets
        _refresh_agent_budgets()
        _success("Reloaded.")
    except Exception as exc:
        _warn(f"Reloaded with warning: {exc}")


@agent_config_grp.command("path")
def agent_config_path() -> None:
    """Print the absolute path of the agent config TOML."""
    from cvc.core.agent_config import CvcAgentConfig
    click.echo(str(CvcAgentConfig.path()))


# ======================================================================
# AGENTS — Hive Mind agent management
# ======================================================================

@main.group()
def agents() -> None:
    """Manage hive mind agents."""
    pass


@agents.command("list")
@click.option("--squad", default=None, help="Filter by squad name.")
@click.option("--rank", default=None, help="Filter by rank.")
def agents_list(squad: str | None, rank: str | None) -> None:
    """List all registered agents."""
    from cvc.core.database import IndexDB
    from cvc.core.models import discover_cvc_root
    root = discover_cvc_root()
    if root is None:
        console.print("[red]No .cvc/ found. Run 'cvc init' first.[/red]")
        return
    db = IndexDB(root / ".cvc" / "cvc.db")
    try:
        agents_list_data = db.list_agents(squad=squad, rank=rank)
        if not agents_list_data:
            console.print("[dim]No agents registered.[/dim]")
            return
        from rich.table import Table
        table = Table(title="Hive Mind Agents")
        table.add_column("Agent ID", style="bold cyan")
        table.add_column("Name")
        table.add_column("Role")
        table.add_column("Rank", style="yellow")
        table.add_column("Squad", style="green")
        table.add_column("Status")
        for a in agents_list_data:
            table.add_row(
                a["agent_id"], a.get("name", ""), a.get("role", ""),
                a.get("rank", ""), a.get("squad", ""), a.get("status", ""),
            )
        console.print(table)
    finally:
        db.close()


@agents.command("add")
@click.argument("agent_id")
@click.option("--name", default=None, help="Display name.")
@click.option("--role", default=None, help="Agent role (e.g. specialist, captain).")
@click.option("--rank", default=None, help="Hierarchical rank.")
@click.option("--squad", default=None, help="Squad assignment.")
def agents_add(agent_id: str, name: str | None, role: str | None, rank: str | None, squad: str | None) -> None:
    """Register a new agent in the hive mind."""
    from cvc.core.database import IndexDB
    from cvc.core.models import discover_cvc_root
    root = discover_cvc_root()
    if root is None:
        console.print("[red]No .cvc/ found. Run 'cvc init' first.[/red]")
        return
    db = IndexDB(root / ".cvc" / "cvc.db")
    try:
        db.insert_agent(agent_id=agent_id, name=name, role=role, rank=rank, squad=squad)
        console.print(f"[green]Registered agent[/green] [bold]{agent_id}[/bold]")
        if squad:
            console.print(f"  Squad: [cyan]{squad}[/cyan]")
        if rank:
            console.print(f"  Rank: [yellow]{rank}[/yellow]")
    finally:
        db.close()


@agents.command("remove")
@click.argument("agent_id")
def agents_remove(agent_id: str) -> None:
    """Remove an agent from the hive mind."""
    from cvc.core.database import IndexDB
    from cvc.core.models import discover_cvc_root
    root = discover_cvc_root()
    if root is None:
        console.print("[red]No .cvc/ found. Run 'cvc init' first.[/red]")
        return
    db = IndexDB(root / ".cvc" / "cvc.db")
    try:
        if db.delete_agent(agent_id):
            console.print(f"[green]Removed agent[/green] [bold]{agent_id}[/bold]")
        else:
            console.print(f"[red]Agent '{agent_id}' not found.[/red]")
    finally:
        db.close()


# ======================================================================
# GATEWAY — Browser-based dashboard & service manager
# ======================================================================

@main.group()
def gateway() -> None:
    """Manage the CVC Gateway dashboard."""
    pass


@gateway.command("start")
@click.option("--host", default="127.0.0.1", help="Gateway bind host.")
@click.option("--port", default=13421, type=int, help="Gateway bind port.")
@click.option("--proxy-port", default=13421, type=int, help="(Ignored, kept for backward compat) Proxy is now built into the gateway.")
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically.")
@click.option("--log", is_flag=True, help="Run in foreground and show live logs.")
def gateway_start(host: str, port: int, proxy_port: int, no_browser: bool, log: bool) -> None:
    """Start the CVC Gateway (unified proxy + dashboard).

    \b
    Launches the CVC Gateway at http://localhost:13421 that provides:
    - Workspace-routed LLM proxy (replaces 'cvc serve')
    - Management dashboard for monitoring all CVC subsystems
    - Multi-workspace support for concurrent projects

    \b
    Examples:
      cvc gateway start               # Start on default port 13421
      cvc gateway start --port 4000   # Use a custom port
      cvc gateway start --log         # Run in foreground with live logs
    """
    import httpx

    _banner("Gateway Dashboard")

    # NOTE: We deliberately do NOT auto-invoke `cvc setup` here. The user ran
    # `cvc gateway start` to start the gateway — not to configure their LLM.
    # If they haven't completed setup yet, the gateway still starts; the
    # dashboard chat will surface a "no provider configured" message in the
    # UI, and the user can run `cvc setup` in another terminal when ready.
    # This matches `cvc launch` and every other gateway-adjacent command.

    # ── Optional non-blocking hint if setup hasn't been completed ─────────
    # Keep this lightweight — single line, easy to ignore, no interactive
    # prompts. The whole point: never block gateway startup on setup.
    try:
        from cvc.core.models import GlobalConfig as _GC
        from cvc.core.models import get_global_config_dir as _gcdir
        _gc_file = _gcdir() / "config.json"
        _gc_existing = _GC.load() if _gc_file.exists() else None
        _needs_setup = (
            _gc_existing is None
            or not _gc_existing.provider
            or _gc_existing.provider == "passthrough"
        )
        if _needs_setup:
            console.print(
                Panel(
                    "  [bold]No LLM provider configured yet.[/bold]\n\n"
                    "  The dashboard will start, but chat won't work until you\n"
                    "  run [bold #CC3333]cvc setup[/bold #CC3333] in another terminal.",
                    border_style="#5C1010",
                    title="[bold #CC3335]Heads up[/bold #CC3335]",
                    padding=(1, 2),
                )
            )
            console.print()
    except Exception as _e:  # noqa: BLE001
        # Never let the hint itself break gateway startup.
        import logging as _logging
        _logging.getLogger("cvc.cli").debug("first-run hint skipped: %s", _e)

    # Re-enable daemon if it was paused by a previous gateway stop
    try:
        from cvc.daemon import resume_daemon
        resume_daemon()
    except Exception:
        pass

    endpoint = f"http://{host}:{port}"

    # Check if already running
    try:
        r = httpx.get(f"{endpoint}/health", timeout=1.0)
        if r.status_code == 200:
            _success(f"Gateway is already running at [bold]{endpoint}[/bold]")
            if not no_browser:
                import webbrowser
                webbrowser.open(endpoint)
            return
    except Exception:
        pass

    console.print(
        Panel(
            f"  Dashboard   [bold #CC3333]{endpoint}[/bold #CC3333]\n"
            f"  LLM Proxy   [bold #CC3333]{endpoint}/ws/{{workspace_id}}/v1/...[/bold #CC3333]\n\n"
            f"  [dim]The gateway provides both the dashboard AND the LLM proxy.\n"
            f"  Workspaces are registered dynamically via 'cvc launch'.\n"
            f"  No separate proxy process needed.[/dim]",
            border_style="#5C1010",
            title="[bold #55AA55]Starting Gateway[/bold #55AA55]",
            padding=(1, 2),
        )
    )

    # NOTE: gateway boot path is below — uvicorn child is spawned a few lines
    # down. The CLI used to claim "Dashboard started" *before* the port was
    # actually bound, which on Windows (cold-import 15-45 s) shows the user
    # "can't reach this page" until uvicorn finally comes up. We now:
    #   1. Spawn the child first.
    #   2. Block on /health for up to 90 s with a Rich progress spinner.
    #   3. Only THEN open the browser and print the "Dashboard ready" line.
    # Browser-opener is removed from here; it now runs inline after readiness.

    import os
    import subprocess
    import sys

    # Pre-load dotenv ONLY for non-secret, non-Telegram keys (PATH tweaks,
    # workspace config, etc.). Telegram bot token / allowlist MUST come
    # from the per-user channels file at ``~/.cvc/channels/telegram.yaml``
    # — see ``cvc/integrations/setup.py``. We deliberately do NOT load
    # ``TELEGRAM_BOT_TOKEN`` / ``TELEGRAM_ALLOWED_USERS`` from the local
    # ``.env`` here, because shipping a project-root ``.env`` would leak
    # secrets on distribution. The legacy ``.env`` path is still honored
    # for one release as a migration aid: if those keys ARE present, the
    # gateway will warn the user to run ``cvc setup`` to migrate them.
    try:
        from dotenv import load_dotenv
        env_path = Path.cwd() / ".env"
        if env_path.exists():
            # Strip Telegram keys before loading so they never enter
            # os.environ from a project-root file. The channels yaml
            # is the single source-of-truth for Telegram secrets.
            _env_content = env_path.read_text(encoding="utf-8")
            _scrubbed = "\n".join(
                line for line in _env_content.splitlines()
                if not line.startswith(
                    ("TELEGRAM_BOT_TOKEN=", "TELEGRAM_ALLOWED_USERS=")
                )
            )
            if _scrubbed.strip():
                from io import StringIO
                load_dotenv(stream=StringIO(_scrubbed))
    except Exception:
        pass

    log_level = "info" if log else "warning"

    # v3.3.12 — Cold-boot flash guard. On Windows, the HKCU\...\Run
    # registry entry fires the autostart command on every logon, and
    # Windows itself can re-fire the entry if the first attempt exits
    # non-zero (because the env or PATH isn't fully set during early
    # boot, or because the pythonw.exe wrapper exits before uvicorn
    # binds the port). Each re-fire spawns a new console window →
    # "millions of flashes". Two cheap pre-flight checks make the
    # second-and-later invocations silent no-ops:
    #
    #   1. The port is already bound → another instance is healthy,
    #      just open the browser and exit. (Unix + Windows.)
    #   2. A PID file exists and the PID is alive → the child from
    #      a previous launch is still running; print a one-liner and
    #      exit. (Cross-platform.)
    #
    # We check #1 before #2 because if uvicorn is up, we want to
    # reuse it even if the PID file went stale.
    import socket as _socket
    try:
        with _socket.create_connection((host, port), timeout=0.5):
            # Port is already serving — a previous launch succeeded.
            console.print(
                f"\n  [bold #55AA55]Gateway already running at[/bold #55AA55] "
                f"[bold #CC3333]{endpoint}[/bold #CC3333]  "
                f"[dim](reusing the existing instance)[/dim]\n"
            )
            if not no_browser:
                import webbrowser
                try:
                    webbrowser.open(endpoint)
                except Exception:
                    pass
            return
    except OSError:
        pass  # port not bound, proceed to spawn

    try:
        from cvc.daemon import _pid_alive, read_pid_file
        existing_pid = read_pid_file()
        if existing_pid and _pid_alive(existing_pid):
            # PID file says a child is alive. Don't double-spawn.
            console.print(
                f"\n  [bold #55AA55]Gateway already running[/bold #55AA55] "
                f"[dim](pid {existing_pid}; re-launching would clash)[/dim]\n"
            )
            if not no_browser:
                import webbrowser
                try:
                    webbrowser.open(endpoint)
                except Exception:
                    pass
            return
    except Exception:
        pass  # no pid helper yet, fall through to spawn

    # Write PID file so gateway stop can reliably find the process
    from cvc.daemon import remove_pid_file, write_pid_file
    code = (
        f"import os, sys; "
        f"sys.path.insert(0, ''); "
        f"from cvc.daemon import write_pid_file; "
        f"write_pid_file(); "
        f"import uvicorn; "
        f"uvicorn.run('cvc.gateway:app', host='{host}', port={port}, log_level='{log_level}')"
    )

    exe = sys.executable
    if not log and sys.platform == "win32":
        pythonw_path = os.path.join(sys.prefix, "Scripts", "pythonw.exe")
        if os.path.exists(pythonw_path):
            exe = pythonw_path
        elif exe.lower().endswith("python.exe"):
            exe = exe[:-10] + "pythonw.exe"
    cmd = [exe, "-c", code]

    if log:
        write_pid_file(os.getpid())
        # Foreground mode: kick off a background thread that waits for
        # readiness then opens the browser. The foreground process itself
        # streams uvicorn logs, so we cannot block here.
        if not no_browser:
            import threading
            import time as _t

            import httpx as _httpx

            def _open_when_ready() -> None:
                deadline = _t.time() + 90.0
                while _t.time() < deadline:
                    try:
                        r = _httpx.get(f"{endpoint}/health", timeout=1.5)
                        if r.status_code < 500:
                            import webbrowser
                            webbrowser.open(endpoint)
                            return
                    except Exception:
                        pass
                    _t.sleep(0.4)

            threading.Thread(target=_open_when_ready, daemon=True).start()

        console.print(
            f"\n  [dim]Gateway booting at[/dim] [bold #CC3333]{endpoint}[/bold #CC3333]"
            "  [dim](browser will open when ready; Ctrl+C to stop)[/dim]\n"
        )
        try:
            subprocess.run(cmd, env=os.environ.copy(), **HIDDEN_KW)
        except KeyboardInterrupt:
            pass
        finally:
            remove_pid_file()
    else:
        kwargs = {}
        if sys.platform == "win32":
            CREATE_NO_WINDOW = getattr(subprocess, "CREATE_NO_WINDOW", 0x08000000)
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP | CREATE_NO_WINDOW

            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            startupinfo.wShowWindow = subprocess.SW_HIDE
            kwargs["startupinfo"] = startupinfo
        else:
            kwargs["start_new_session"] = True

        # Surface startup crashes to a persistent err log instead of silently
        # discarding them. Without this, missing deps / import errors at boot
        # are invisible (Popen returns 0, port never opens). See 2.22.1 hotfix.
        err_log_path = Path.home() / ".cvc" / "gateway.err.log"
        try:
            from datetime import datetime as _dt
            err_log_path.parent.mkdir(parents=True, exist_ok=True)
            err_fh = open(err_log_path, "a", buffering=1)
            err_fh.write(f"\n--- gateway start {_dt.now().isoformat()} ---\n")
        except Exception:
            err_fh = subprocess.DEVNULL  # type: ignore[assignment]

        proc = subprocess.Popen(
            cmd,
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=err_fh,
            env=os.environ.copy(),
            **kwargs,
        )
        # Write the child PID so gateway stop can find it
        write_pid_file(proc.pid)

        # ---- Readiness gate ----------------------------------------------
        # The dashboard opens against /health, so we block here until /health
        # answers (or until we conclude the child crashed). Cold-start budget
        # is generous because on Windows the first uvicorn import + workspace
        # bootstrap can take 30-60 s (chromadb, sentence-transformers, etc.).
        # Previously the CLI announced "Dashboard started" immediately and a
        # background thread polled for only 10 s, so users hit "can't reach
        # this page" until the port actually bound.
        import time as _t

        import httpx as _httpx
        try:
            from rich.progress import Progress, SpinnerColumn, TextColumn
        except Exception:
            Progress = None  # type: ignore[assignment]

        READY_BUDGET_S = 90.0
        POLL_INTERVAL_S = 0.4
        health_url = f"{endpoint}/health"

        def _is_ready() -> bool:
            try:
                r = _httpx.get(health_url, timeout=1.5)
                return r.status_code < 500
            except Exception:
                return False

        def _child_alive() -> bool:
            return proc.poll() is None

        ready = False
        deadline = _t.time() + READY_BUDGET_S

        if Progress is not None:
            with Progress(
                SpinnerColumn(),
                TextColumn("[dim]Starting CVC Gateway… this can take up to a minute on first boot[/dim]"),
                console=console,
                transient=True,
            ) as _pr:
                _pr.add_task("boot", total=None)
                while _t.time() < deadline:
                    if not _child_alive():
                        break
                    if _is_ready():
                        ready = True
                        break
                    _t.sleep(POLL_INTERVAL_S)
        else:
            while _t.time() < deadline:
                if not _child_alive():
                    break
                if _is_ready():
                    ready = True
                    break
                _t.sleep(POLL_INTERVAL_S)

        if not ready:
            if not _child_alive():
                console.print(
                    f"\n  [bold red]Gateway crashed during startup.[/bold red]"
                    f"\n  [dim]See[/dim] [bold]{err_log_path}[/bold] [dim]for the traceback,[/dim]"
                    f"\n  [dim]or run[/dim] [bold]cvc gateway start --log[/bold] [dim]to watch boot live.[/dim]\n"
                )
            else:
                console.print(
                    f"\n  [bold yellow]Gateway is still booting after {int(READY_BUDGET_S)}s.[/bold yellow]"
                    f"\n  [dim]It will likely come up shortly — refresh[/dim] [bold #CC3333]{endpoint}[/bold #CC3333] [dim]in a moment.[/dim]"
                    f"\n  [dim]If it never loads, check[/dim] [bold]{err_log_path}[/bold]\n"
                )
            return

        # Ready — now safe to open the browser and tell the user.
        if not no_browser:
            try:
                import webbrowser
                webbrowser.open(endpoint)
            except Exception:
                pass

        console.print(
            f"\n  [dim]Dashboard ready at[/dim] [bold #CC3333]{endpoint}[/bold #CC3333]"
        )
        console.print(
            "  [dim]The gateway is running in the background. You can safely close this terminal.[/dim]\n"
        )


@gateway.command("status")
@click.option("--host", default="127.0.0.1", help="Gateway host.")
@click.option("--port", default=13421, type=int, help="Gateway port.")
def gateway_status(host: str, port: int) -> None:
    """Check the status of the CVC Gateway and managed services."""
    import httpx

    _banner("Gateway Status")

    endpoint = f"http://{host}:{port}"
    try:
        r = httpx.get(f"{endpoint}/health", timeout=5.0)
        r.raise_for_status()
        data = r.json()
    except httpx.ConnectError:
        _error(f"Gateway is not running on {endpoint}")
        _hint("Start the gateway: [bold]cvc gateway start[/bold]")
        return
    except Exception as exc:
        _error(f"Failed to reach gateway: {exc}")
        return

    _success(f"Gateway is [bold]running[/bold] on {endpoint}")

    # Fetch service details
    try:
        r = httpx.get(f"{endpoint}/api/gateway/services", timeout=5.0)
        services = r.json()
    except Exception:
        services = {}

    if services:
        table = Table(
            box=box.ROUNDED,
            border_style="dim",
            show_header=True,
            header_style="bold #CC3333",
        )
        table.add_column("Service", style="bold")
        table.add_column("Status")
        table.add_column("PID")
        table.add_column("Port")
        table.add_column("Uptime")

        for name, svc in services.items():
            status = svc.get("status", "unknown")
            status_style = {
                "running": "#55AA55",
                "stopped": "red",
                "paused": "#CCAA44",
            }.get(status, "dim")

            table.add_row(
                name,
                f"[{status_style}]{status}[/{status_style}]",
                str(svc.get("pid", "-")),
                str(svc.get("port", "-")),
                svc.get("uptime", "-"),
            )

        console.print()
        console.print(table)

    console.print()


@gateway.command("stop")
@click.option("--host", default="127.0.0.1", help="Gateway host.")
@click.option("--port", default=13421, type=int, help="Gateway port.")
def gateway_stop(host: str, port: int) -> None:
    """Stop any running CVC Gateway process."""
    from cvc.daemon import kill_gateway_process

    _banner("Gateway Stop")

    # Check if gateway is actually running first
    is_running = False
    try:
        import httpx
        r = httpx.get(f"http://{host}:{port}/health", timeout=3.0)
        if r.status_code == 200:
            is_running = True
    except Exception:
        pass

    # Also check PID file even if health check fails
    from cvc.daemon import read_pid_file
    pid_from_file = read_pid_file()
    if not is_running and not pid_from_file:
        _error(f"Gateway is not running on http://{host}:{port}")
        return

    # Kill all gateway processes (PID file + port scan + SIGTERM → SIGKILL)
    killed = kill_gateway_process(port)

    if killed:
        _success(f"Gateway stopped (PID {', '.join(str(p) for p in killed)}).")
    else:
        _error("Could not find gateway process. It may have already exited.")
        return

    # Verify it's actually dead
    import time
    time.sleep(0.5)
    try:
        import httpx
        r = httpx.get(f"http://{host}:{port}/health", timeout=2.0)
        if r.status_code == 200:
            _warn("Gateway is still responding — retrying with force kill...")
            kill_gateway_process(port)
            time.sleep(1.0)
            try:
                r2 = httpx.get(f"http://{host}:{port}/health", timeout=2.0)
                if r2.status_code == 200:
                    _error("Gateway is still running. Try killing it manually.")
                    return
            except Exception:
                pass
            _success("Gateway force-stopped successfully.")
    except Exception:
        pass  # Connection refused = gateway is dead = success


@gateway.command("restart")
@click.option("--host", default="127.0.0.1", help="Gateway bind host.")
@click.option("--port", default=13421, type=int, help="Gateway bind port.")
@click.option("--proxy-port", default=13421, type=int, help="Proxy bind port (deprecated, uses gateway port).", hidden=True)
@click.option("--no-browser", is_flag=True, help="Don't open browser automatically.")
@click.option("--log", is_flag=True, help="Run in foreground and show live logs.")
@click.pass_context
def gateway_restart(ctx, host: str, port: int, proxy_port: int, no_browser: bool, log: bool) -> None:
    """Restart the CVC Gateway (stop then start)."""
    _banner("Gateway Restart")

    # Try stopping first
    try:
        ctx.invoke(gateway_stop, host=host, port=port)
        import time
        time.sleep(1)
    except Exception:
        pass

    # Then start
    ctx.invoke(gateway_start, host=host, port=port, proxy_port=proxy_port, no_browser=no_browser, log=log)


# ---------------------------------------------------------------------------
# daemon (auto-start management)
# ---------------------------------------------------------------------------


@main.group()
def daemon() -> None:
    """Manage the CVC auto-start daemon."""
    pass


@daemon.command("install")
@click.option("--host", default="127.0.0.1", help="Gateway bind host.")
@click.option("--port", default=13421, type=int, help="Gateway bind port.")
def daemon_install(host: str, port: int) -> None:
    """Install the CVC daemon to auto-start the gateway on boot."""
    from cvc.daemon import install_daemon

    _banner("Daemon Install")

    msg = install_daemon(host, port)
    _success(msg)
    console.print()
    _hint("The gateway will now start automatically when you log in.")
    _hint("Use [bold]cvc daemon status[/bold] to check, [bold]cvc daemon uninstall[/bold] to remove.")
    console.print()


@daemon.command("uninstall")
def daemon_uninstall() -> None:
    """Remove the CVC auto-start daemon."""
    from cvc.daemon import uninstall_daemon

    _banner("Daemon Uninstall")

    msg = uninstall_daemon()
    _success(msg)
    console.print()


@daemon.command("status")
def daemon_status_cmd() -> None:
    """Check whether the CVC daemon is installed and the gateway is running."""
    from cvc.daemon import daemon_status

    _banner("Daemon Status")

    status = daemon_status()

    if status["installed"]:
        _success(f"Daemon is [bold]installed[/bold] via {status['method']}")
        console.print(f"  [dim]Config: {status['config_path']}[/dim]")
    else:
        _warn("Daemon is [bold]not installed[/bold]")
        _hint("Install with: [bold]cvc daemon install[/bold]")

    console.print()

    if status["gateway_running"]:
        _success(f"Gateway is [bold]running[/bold] (PID {status['gateway_pid']})")
    else:
        _warn("Gateway is [bold]not running[/bold]")

    console.print()


@daemon.group("sofia")
def daemon_sofia() -> None:
    """Manage the Sofia voice-agent auto-start daemon (macOS launchd)."""
    pass


@daemon_sofia.command("install")
@click.option("--host", default="127.0.0.1", help="CVC Gateway host.")
@click.option("--port", default=13421, type=int, help="CVC Gateway port.")
def daemon_sofia_install(host: str, port: int) -> None:
    """Install ~/Library/LaunchAgents/com.cvc.sofia.plist so Sofia auto-starts on login."""
    from cvc.daemon import install_sofia_launchd

    _banner("Sofia Daemon Install")
    msg = install_sofia_launchd(host=host, port=port)
    if "failed" in msg.lower():
        _warn(msg)
    else:
        _success(msg)
        _hint("Sofia will auto-start on the next login.")
        _hint("Use [bold]cvc daemon sofia status[/bold] to verify.")
    console.print()


@daemon_sofia.command("uninstall")
def daemon_sofia_uninstall() -> None:
    """Remove ~/Library/LaunchAgents/com.cvc.sofia.plist."""
    from cvc.daemon import uninstall_sofia_launchd

    _banner("Sofia Daemon Uninstall")
    msg = uninstall_sofia_launchd()
    _success(msg)
    console.print()


@daemon_sofia.command("status")
def daemon_sofia_status_cmd() -> None:
    """Check whether the Sofia launchd daemon is installed."""
    from cvc.daemon import sofia_daemon_status

    _banner("Sofia Daemon Status")
    status = sofia_daemon_status()
    if status["installed"]:
        _success(f"Sofia daemon is [bold]installed[/bold] via {status['method']}")
        console.print(f"  [dim]Config: {status['config_path']}[/dim]")
    else:
        _warn("Sofia daemon is [bold]not installed[/bold]")
        _hint("Install with: [bold]cvc daemon sofia install[/bold]")
        _hint("Or run [bold]cvc voice-setup[/bold] and choose to install it during setup.")
    console.print()


@main.group("config", invoke_without_command=True)
@click.pass_context
def config_group(ctx: click.Context) -> None:
    """Manage CVC global configuration."""
    if ctx.invoked_subcommand is None:
        # default to show
        ctx.invoke(config_show)

@config_group.command("set")
@click.argument("key")
@click.argument("value")
def config_set(key: str, value: str) -> None:
    """Set a configuration value in ~/.cvc/config.json."""
    import json
    from pathlib import Path
    config_file = Path.home() / ".cvc" / "config.json"
    config = {}
    if config_file.exists():
        with open(config_file, "r") as f:
            try:
                config = json.load(f)
            except json.JSONDecodeError:
                pass
    config[key] = value
    config_file.parent.mkdir(parents=True, exist_ok=True)
    with open(config_file, "w") as f:
        json.dump(config, f, indent=2)
    console.print(f"[bold #55AA55]✓[/bold #55AA55] Set [bold]{key}[/bold] = {value}")


_SECRET_KEY_HINTS = ("key", "token", "secret", "password", "api")


def _redact(value: Any) -> Any:
    if isinstance(value, str) and len(value) > 8:
        return value[:4] + "…" + value[-4:]
    return "•••"


@config_group.command("show")
@click.option("--reveal", is_flag=True, help="Show secret values in full (default: redacted).")
@click.option("--key", "key_filter", default=None, help="Show only a single key.")
def config_show(reveal: bool, key_filter: str | None) -> None:
    """Show the global config from ~/.cvc/config.json (secrets redacted)."""
    import json
    from pathlib import Path
    from rich.table import Table

    config_file = Path.home() / ".cvc" / "config.json"
    if not config_file.exists():
        _info("No config yet. Set values with [bold]cvc config set KEY VALUE[/bold].")
        return

    try:
        with open(config_file, "r") as f:
            cfg = json.load(f)
    except (json.JSONDecodeError, OSError) as e:
        _error(f"Could not read config: {e}")
        return

    if not isinstance(cfg, dict) or not cfg:
        _info("Config file is empty.")
        return

    if key_filter:
        if key_filter not in cfg:
            _error(f"Key not found: {key_filter}")
            return
        cfg = {key_filter: cfg[key_filter]}

    table = Table(
        title=f"[bold #CC3333]Config[/bold #CC3333]  [dim]{config_file}[/dim]",
        border_style="#5C1010",
        title_justify="left",
        show_lines=False,
    )
    table.add_column("Key", style="bold")
    table.add_column("Value", overflow="fold")

    for k in sorted(cfg.keys()):
        v = cfg[k]
        is_secret = any(h in k.lower() for h in _SECRET_KEY_HINTS)
        if is_secret and not reveal:
            display = f"[dim]{_redact(v)}[/dim]"
        elif isinstance(v, (dict, list)):
            display = json.dumps(v, indent=2)
        else:
            display = str(v)
        table.add_row(k, display)

    console.print(table)
    if not reveal:
        _hint("Reveal secrets: [bold]cvc config show --reveal[/bold]")


@main.command("tools")
@click.option("--names-only", is_flag=True, help="Print just tool names (machine-readable).")
def tools_cmd(names_only: bool) -> None:
    """List all tools available to the CVC agent."""
    from rich.table import Table
    try:
        from cvc.agent.tools import AGENT_TOOLS
    except Exception as e:
        _error(f"Could not load agent tools: {e}")
        return

    names = [t["function"]["name"] for t in AGENT_TOOLS if "function" in t]

    if names_only:
        for n in names:
            click.echo(n)
        return

    table = Table(
        title=f"[bold #CC3333]Agent Tools[/bold #CC3333]  ({len(names)} registered)",
        border_style="#5C1010",
        title_justify="left",
        show_lines=False,
    )
    table.add_column("Name", style="bold #CCAA44")
    table.add_column("Description", overflow="fold")

    for t in AGENT_TOOLS:
        fn = t.get("function", {})
        name = fn.get("name", "—")
        desc = (fn.get("description") or "").strip().split("\n")[0]
        if len(desc) > 110:
            desc = desc[:107] + "..."
        table.add_row(name, desc)

    console.print(table)


@main.group("workspace", invoke_without_command=True)
@click.pass_context
def workspace_group(ctx: click.Context) -> None:
    """Manage CVC workspaces (multi-project registry)."""
    if ctx.invoked_subcommand is None:
        ctx.invoke(workspace_list)


@workspace_group.command("list")
def workspace_list() -> None:
    """List all known CVC workspaces."""
    from rich.table import Table
    try:
        from cvc.workspace_manager import WorkspaceManager
    except Exception as e:
        _error(f"Could not load workspace manager: {e}")
        return

    wm = WorkspaceManager()
    workspaces = wm.list_workspaces()

    if not workspaces:
        _info("No workspaces registered yet.")
        _hint("Open one with [bold]cvc init[/bold] or [bold]cvc status[/bold] inside a project.")
        return

    workspaces.sort(key=lambda w: w.get("last_accessed", 0), reverse=True)

    table = Table(
        title=f"[bold #CC3333]Workspaces[/bold #CC3333]  ({len(workspaces)} total)",
        border_style="#5C1010",
        title_justify="left",
        show_lines=False,
    )
    table.add_column("", width=2)
    table.add_column("Name", style="bold")
    table.add_column("Branch", style="#CCAA44")
    table.add_column("Commits", justify="right", style="dim")
    table.add_column("Path", style="dim", overflow="fold")

    import datetime
    for w in workspaces:
        marker = "[bold #55AA55]●[/bold #55AA55]" if w.get("active") else (
            "[bold #CCAA44]○[/bold #CCAA44]" if w.get("open") else " "
        )
        table.add_row(
            marker,
            w.get("name", "?"),
            w.get("branch", "main"),
            str(w.get("commit_count", 0)),
            w.get("path", ""),
        )

    console.print(table)
    _hint("[dim]● = active   ○ = open   (blank) = registered[/dim]")

@main.command("ignore")
@click.argument("path")
def ignore_cmd(path: str) -> None:
    """Automatically append a file or directory to .cvcignore."""
    from pathlib import Path
    ignore_file = Path(".cvcignore")
    if not ignore_file.exists():
        ignore_file.touch()
    with open(ignore_file, "a") as f:
        f.write(f"\n{path}")
    console.print(f"[bold #55AA55]✓[/bold #55AA55] Added [bold]{path}[/bold] to .cvcignore")

@main.command("ui")
def ui_cmd() -> None:
    """Open the CVC dashboard in the default web browser."""
    import webbrowser
    console.print("[bold #55AA55]Opening CVC UI at http://localhost:13421[/bold #55AA55]")
    webbrowser.open("http://localhost:13421")

@main.command("open")
def open_cmd() -> None:
    """Alias for 'cvc ui' to open the CVC dashboard."""
    ui_cmd()

# v2.91.51 — `cvc setup-ui`
#
# Build the Vite dashboard bundle into `cvc/web_dist/`. This MUST be run
# before publishing to PyPI, otherwise the wheel ships a stale web UI
# (a complete v2.91.49 fix went out as v2.91.50 with the OLD web dist
# because the user forgot this step). Auto-installs node_modules on first
# run. Idempotent — safe to re-run.
#
# Adds the JS+CSS bundle hash to stdout so the user can confirm a
# genuinely new dist was built (the old version's hash was
# `index-DTk6PUWi.js`; v2.91.49 rebuilt it to `index-DWLrxGf9.js`).
@main.command("setup-ui")
@click.option("--skip-install", is_flag=True,
              help="Skip `npm install` even if node_modules is missing.")
def setup_ui_cmd(skip_install: bool) -> None:
    """Build the CVC dashboard (Vite) into cvc/web_dist/."""
    import subprocess as _sp
    from pathlib import Path as _Path

    repo_root = _Path(__file__).resolve().parent.parent
    web_dir = repo_root / "cvc" / "web"
    if not (web_dir / "package.json").exists():
        console.print(
            f"[bold red]✗[/bold red] Could not find CVC web source at {web_dir}. "
            "Are you running from a source checkout?"
        )
        raise SystemExit(1)

    node_modules = web_dir / "node_modules"
    if not skip_install and not node_modules.exists():
        console.print("[dim]Installing npm dependencies (first run)…[/dim]")
        try:
            # shell=True on Windows because subprocess.Popen with a
            # bare `npm` and cwd= can't find the .cmd shim otherwise.
            _sp.run(
                "npm install" if sys.platform == "win32" else ["npm", "install"],
                cwd=str(web_dir), check=True, shell=(sys.platform == "win32"),
            )
        except FileNotFoundError:
            console.print(
                "[bold red]✗[/bold red] `npm` not found on PATH. "
                "Install Node.js 18+ and re-run."
            )
            raise SystemExit(1)
        except _sp.CalledProcessError as exc:
            console.print(f"[bold red]✗[/bold red] npm install failed: {exc}")
            raise SystemExit(1)

    console.print("[dim]Building dashboard (npm run build)…[/dim]")
    try:
        _sp.run(
            "npm run build" if sys.platform == "win32" else ["npm", "run", "build"],
            cwd=str(web_dir), check=True, shell=(sys.platform == "win32"),
        )
    except _sp.CalledProcessError as exc:
        console.print(f"[bold red]✗[/bold red] npm run build failed: {exc}")
        raise SystemExit(1)

    # Report what we just built so the user can verify against the wheel.
    dist_dir = repo_root / "cvc" / "web_dist"
    if not dist_dir.exists():
        console.print(f"[bold red]✗[/bold red] build completed but {dist_dir} not found")
        raise SystemExit(1)
    js_assets = sorted((dist_dir / "assets").glob("index-*.js"))
    if js_assets:
        latest = js_assets[-1]
        size_mb = latest.stat().st_size / (1024 * 1024)
        console.print(
            f"[bold #55AA55]✓[/bold #55AA55] Built "
            f"[bold]{latest.name}[/bold] ({size_mb:.2f} MB) into [bold]cvc/web_dist/[/bold]"
        )
    else:
        console.print("[bold #55AA55]✓[/bold #55AA55] Dashboard built.")

    # v2.91.51 — emit a warning if the user is about to publish a stale dist
    # (i.e. they ran setup-ui, then accidentally reused a wheel that was
    # built BEFORE this rebuild).
    console.print(
        "[dim]When publishing: run `cvc setup-ui` immediately before "
        "`python -m build` to ensure the wheel includes this build.[/dim]"
    )

@main.command("clean")
@click.option("--force", is_flag=True, help="Force clean without prompt")
def clean_cmd(force: bool) -> None:
    """Safely purge old cognitive checkpoints or temporary chat sessions."""
    import shutil
    from pathlib import Path
    cache_dir = Path.home() / ".cvc" / "cache"
    if cache_dir.exists():
        if force or click.confirm(f"Are you sure you want to clear {cache_dir}?"):
            shutil.rmtree(cache_dir)
            console.print("[bold #55AA55]✓[/bold #55AA55] Cache cleared successfully.")
    else:
        console.print("[dim]No cache found to clean.[/dim]")

@main.command("clear-cache")
@click.option("--force", is_flag=True, help="Force clean without prompt")
def clear_cache_cmd(force: bool) -> None:
    """Alias for 'cvc clean'."""
    clean_cmd(force=force)

@main.command("uninstall")
def uninstall_cmd() -> None:
    """Completely remove CVC installation and its global binaries."""
    import shutil
    from pathlib import Path
    if click.confirm("Are you sure you want to completely uninstall CVC and remove ~/.cvc?", abort=True):
        cvc_dir = Path.home() / ".cvc"
        if cvc_dir.exists():
            shutil.rmtree(cvc_dir)
            console.print("[bold #55AA55]✓[/bold #55AA55] Removed ~/.cvc directory.")
        console.print("[bold #CC3333]Note:[/bold #CC3333] To remove the executable completely, please run:")
        console.print("  [dim]uv tool uninstall tm-ai[/dim]  or  [dim]pip uninstall tm-ai[/dim]")

@main.command("install-daemon")
def install_daemon_cmd() -> None:
    """Install the CVC gateway as a background daemon (launchd, systemd, or Windows Registry) and configure environment."""
    import os
    import platform
    import shutil
    import sys
    from pathlib import Path

    os_name = platform.system().lower()
    home = Path.home()

    cvc_bin = shutil.which("cvc")
    if cvc_bin:
        exe_cmd = f'"{cvc_bin}" gateway start --no-browser --log'
        plist_args = f"""        <string>{cvc_bin}</string>
        <string>gateway</string>
        <string>start</string>
        <string>--no-browser</string>
        <string>--log</string>"""
    else:
        exe_path = sys.executable or "python"
        exe_cmd = f'"{exe_path}" -m cvc.cli gateway start --no-browser --log'
        plist_args = f"""        <string>{exe_path}</string>
        <string>-m</string>
        <string>cvc.cli</string>
        <string>gateway</string>
        <string>start</string>
        <string>--no-browser</string>
        <string>--log</string>"""

    console.print("[bold cyan]Installing CVC gateway daemon...[/bold cyan]")

    def append_env_linux_mac():
        env_line = 'export ANTHROPIC_BASE_URL="http://127.0.0.1:13421/ws/default/v1"\n'
        for shell_rc in [".zshrc", ".bashrc"]:
            rc_path = home / shell_rc
            try:
                content = ""
                if rc_path.exists():
                    content = rc_path.read_text(encoding="utf-8")
                if "ANTHROPIC_BASE_URL" not in content:
                    with rc_path.open("a", encoding="utf-8") as f:
                        if content and not content.endswith("\n"):
                            f.write("\n")
                        f.write(env_line)
                    console.print(f"[bold green]✓[/bold green] Appended ANTHROPIC_BASE_URL to ~/{shell_rc}")
            except Exception as e:
                console.print(f"[bold yellow]⚠ Could not update {shell_rc}: {e}[/bold yellow]")

    if os_name == "darwin":
        plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.cvc.gateway</string>
    <key>ProgramArguments</key>
    <array>
{plist_args}
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>{home}/.cvc/gateway.log</string>
    <key>StandardErrorPath</key>
    <string>{home}/.cvc/gateway.log</string>
</dict>
</plist>
"""
        la_dir = home / "Library" / "LaunchAgents"
        la_dir.mkdir(parents=True, exist_ok=True)
        plist_path = la_dir / "com.cvc.gateway.plist"
        plist_path.write_text(plist_content, encoding="utf-8")
        os.system(f"launchctl load -w {plist_path} >/dev/null 2>&1")
        console.print("[bold green]✓[/bold green] Installed launchd daemon (com.cvc.gateway.plist)")
        append_env_linux_mac()

    elif os_name == "linux":
        service_content = f"""[Unit]
Description=CVC Gateway Daemon
After=network.target

[Service]
ExecStart={exe_cmd.replace('"', '')}
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
"""
        sd_dir = home / ".config" / "systemd" / "user"
        sd_dir.mkdir(parents=True, exist_ok=True)
        service_path = sd_dir / "sofia.service"
        service_path.write_text(service_content, encoding="utf-8")
        os.system("systemctl --user daemon-reload >/dev/null 2>&1")
        os.system("systemctl --user enable sofia.service >/dev/null 2>&1")
        os.system("systemctl --user start sofia.service >/dev/null 2>&1")
        console.print("[bold green]✓[/bold green] Installed systemd user service (sofia.service)")
        append_env_linux_mac()

    elif os_name == "windows":
        import winreg
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        try:
            cmd = exe_cmd
            # If using fallback python, maybe use pythonw
            if not cvc_bin and exe_path.lower().endswith("python.exe"):
                pythonw = exe_path[:-10] + "pythonw.exe"
                if os.path.exists(pythonw):
                    cmd = f'"{pythonw}" -m cvc.cli gateway start --no-browser --log'

            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.SetValueEx(key, "CVCGateway", 0, winreg.REG_SZ, cmd)
            winreg.CloseKey(key)
            console.print(f"[bold green]✓[/bold green] Added CVC Gateway to Windows Registry ({key_path})")

            os.system('setx ANTHROPIC_BASE_URL "http://127.0.0.1:13421/ws/default/v1" >nul 2>&1')
            console.print("[bold green]✓[/bold green] Set ANTHROPIC_BASE_URL environment variable via setx")
        except Exception as e:
            console.print(f"[bold red]Failed to update Windows registry: {e}[/bold red]")

    else:
        console.print(f"[bold yellow]Unsupported OS for automated daemon install: {os_name}[/bold yellow]")

    console.print("\\n[bold cyan]Install complete![/bold cyan] The gateway will now run automatically.")

@main.command("uninstall-daemon")
def uninstall_daemon_cmd() -> None:
    """Remove the CVC gateway background daemon."""
    import os
    import platform
    from pathlib import Path

    os_name = platform.system().lower()
    home = Path.home()

    console.print("[bold cyan]Uninstalling CVC gateway daemon...[/bold cyan]")

    if os_name == "darwin":
        plist_path = home / "Library" / "LaunchAgents" / "com.cvc.gateway.plist"
        if plist_path.exists():
            os.system(f"launchctl unload -w {plist_path} >/dev/null 2>&1")
            plist_path.unlink()
            console.print("[bold green]✓[/bold green] Removed launchd daemon.")
        else:
            console.print("[bold yellow]Daemon not found.[/bold yellow]")

    elif os_name == "linux":
        service_path = home / ".config" / "systemd" / "user" / "sofia.service"
        os.system("systemctl --user stop sofia.service >/dev/null 2>&1")
        os.system("systemctl --user disable sofia.service >/dev/null 2>&1")
        if service_path.exists():
            service_path.unlink()
            console.print("[bold green]✓[/bold green] Removed systemd service.")
        else:
            console.print("[bold yellow]Daemon not found.[/bold yellow]")

    elif os_name == "windows":
        import winreg
        key_path = r"Software\\Microsoft\\Windows\\CurrentVersion\\Run"
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_SET_VALUE)
            winreg.DeleteValue(key, "CVCGateway")
            winreg.CloseKey(key)
            console.print("[bold green]✓[/bold green] Removed from Windows Registry.")
        except FileNotFoundError:
            console.print("[bold yellow]Registry key not found.[/bold yellow]")
        except Exception as e:
            console.print(f"[bold red]Failed: {e}[/bold red]")

    else:
        console.print(f"[bold yellow]Unsupported OS: {os_name}[/bold yellow]")


# ---------------------------------------------------------------------------
# cognome — COGNOME Layer 1 (the smart librarian)
# ---------------------------------------------------------------------------

@main.group()
def cognome() -> None:
    """COGNOME substrate — compile minimal Engrams from the Merkle DAG."""


@cognome.command("compile")
@click.argument("query")
@click.option(
    "--budget", "-b",
    type=int,
    default=1200,
    show_default=True,
    help="Hard ceiling on preamble tokens.",
)
@click.option(
    "--branch",
    default=None,
    help="Restrict candidates to this branch's ancestry.",
)
@click.option(
    "--show/--no-show",
    default=True,
    help="Print the compiled preamble.",
)
def cognome_compile(query: str, budget: int, branch: str | None, show: bool) -> None:
    """
    Compile an Engram for QUERY and print stats + preamble.

    This is the inspector for COGNOME Layer 1: pure heuristic compilation,
    no training, no LLM call.  Use it to see what context would be sent
    for a given query and how much of a token saving it represents.
    """
    engine, _db = _get_engine()
    engram = engine.cognome.compile(query, budget_tokens=budget, branch=branch)

    saved_pct = round(engram.compression_ratio * 100, 1)
    stats = Table(
        box=box.ROUNDED,
        border_style="dim",
        show_header=False,
        padding=(0, 2),
    )
    stats.add_column(style="bold white")
    stats.add_column(style="dim white")
    stats.add_row("Query", _truncate_cli(engram.query, 80))
    stats.add_row("Noemata", str(engram.noeme_count))
    stats.add_row("Tokens",
                  f"{engram.token_estimate} / {engram.budget_tokens} budget")
    stats.add_row("Baseline",
                  f"{engram.baseline_token_estimate} tokens (raw candidates)")
    stats.add_row("Compression", f"{saved_pct}% smaller than baseline")
    stats.add_row("Engram hash", engram.engram_hash[:16] + "…")
    stats.add_row("Sources",
                  ", ".join(c[:8] for c in engram.source_commits[:6])
                  + (" …" if len(engram.source_commits) > 6 else ""))
    console.print(
        Panel(
            stats,
            border_style="#5C1010",
            title="[bold #CC3333]COGNOME Engram (L1)[/bold #CC3333]",
            padding=(1, 1),
        )
    )

    if show and engram.preamble:
        console.print(
            Panel(
                engram.preamble,
                border_style="dim",
                title="[dim]preamble[/dim]",
                padding=(1, 2),
            )
        )


def _truncate_cli(text: str, max_chars: int) -> str:
    text = " ".join((text or "").split())
    return text if len(text) <= max_chars else text[: max_chars - 1].rstrip() + "…"


@cognome.command("init")
def cognome_init() -> None:
    """Bootstrap the COGNOME substrate for this workspace (idempotent)."""
    engine, _db = _get_engine()
    status = engine.cognome.init()
    console.print(
        Panel(
            f"[bold green]✓[/bold green] COGNOME initialised\n"
            f"  Layer: {status.active_layer}  |  Budget: {status.budget_tokens} tokens  |  Enabled: {status.enabled}",
            border_style="#5C1010",
            title="[bold #CC3333]COGNOME[/bold #CC3333]",
        )
    )


@cognome.command("status")
def cognome_status() -> None:
    """Show the current COGNOME status."""
    engine, _db = _get_engine()
    s = engine.cognome.status()

    if not s.initialised:
        console.print("[yellow]COGNOME not initialised. Run:[/yellow] cvc cognome init")
        return

    stats = Table(box=box.ROUNDED, border_style="dim", show_header=False, padding=(0, 2))
    stats.add_column(style="bold white")
    stats.add_column(style="dim white")
    stats.add_row("Initialised", "✓" if s.initialised else "✗")
    stats.add_row("Enabled", "[green]yes[/green]" if s.enabled else "[red]no[/red]")
    stats.add_row("Active layer", s.active_layer)
    stats.add_row("Version", str(s.version))
    stats.add_row("Budget", f"{s.budget_tokens} tokens")
    stats.add_row("Total compiles", str(s.total_compiles))
    stats.add_row("Tokens saved", f"{s.total_tokens_saved:,}")
    stats.add_row("Cached engrams", str(s.cached_engrams))
    if s.last_compile_at:
        import datetime
        stats.add_row("Last compile", datetime.datetime.fromtimestamp(s.last_compile_at).strftime("%Y-%m-%d %H:%M:%S"))
    if s.last_train_at:
        import datetime
        stats.add_row("Last L2 train", datetime.datetime.fromtimestamp(s.last_train_at).strftime("%Y-%m-%d %H:%M:%S"))
    console.print(
        Panel(stats, border_style="#5C1010", title="[bold #CC3333]COGNOME Status[/bold #CC3333]", padding=(1, 1))
    )


@cognome.command("enable")
def cognome_enable() -> None:
    """Enable COGNOME Engram injection."""
    engine, _db = _get_engine()
    engine.cognome.enable()
    console.print("[bold green]✓[/bold green] COGNOME [green]enabled[/green]")


@cognome.command("disable")
def cognome_disable() -> None:
    """Disable COGNOME Engram injection (context compilation paused)."""
    engine, _db = _get_engine()
    engine.cognome.disable()
    console.print("[bold yellow]⏸[/bold yellow] COGNOME [yellow]disabled[/yellow]")


@cognome.command("audit")
@click.option("--limit", "-n", type=int, default=20, show_default=True, help="Max entries to show.")
def cognome_audit(limit: int) -> None:
    """Show recent Engram compilations (audit trail)."""
    engine, _db = _get_engine()
    entries = engine.cognome.audit(limit=limit)

    if not entries:
        console.print("[dim]No COGNOME audit entries yet.[/dim]")
        return

    tbl = Table(box=box.ROUNDED, border_style="dim", show_header=True, header_style="bold #CC3333", padding=(0, 1))
    tbl.add_column("Hash", style="bold white", width=14)
    tbl.add_column("Query", style="dim white", max_width=40)
    tbl.add_column("Tokens", justify="right")
    tbl.add_column("Saved", justify="right")
    tbl.add_column("Comp%", justify="right")
    tbl.add_column("Uses", justify="right")
    tbl.add_column("Sources", style="dim")

    for e in entries:
        saved = max(0, e.baseline_tokens - e.token_estimate)
        tbl.add_row(
            e.engram_hash[:12] + "…",
            _truncate_cli(e.query, 38),
            str(e.token_estimate),
            str(saved),
            f"{e.compression * 100:.0f}%",
            str(e.use_count),
            ", ".join(c[:8] for c in e.source_commits[:3]) + ("…" if len(e.source_commits) > 3 else ""),
        )

    console.print(
        Panel(tbl, border_style="#5C1010", title="[bold #CC3333]COGNOME Audit[/bold #CC3333]", padding=(1, 1))
    )


@cognome.command("cache-prune")
@click.option("--max-age", type=int, default=7, show_default=True, help="Max age in days.")
@click.option("--max-entries", type=int, default=200, show_default=True, help="Max cache entries to keep.")
def cognome_cache_prune(max_age: int, max_entries: int) -> None:
    """Evict stale or excess cached Engrams."""
    engine, _db = _get_engine()
    count = engine.cognome.prune_cache(max_age_days=max_age, max_entries=max_entries)
    console.print(f"[bold green]✓[/bold green] Pruned {count} stale Engrams from cache")


# ---------------------------------------------------------------------------
# handoff — cross-session / cross-workspace portable memory (Phase 4)
# ---------------------------------------------------------------------------

@main.group()
def handoff() -> None:
    """Export/import a portable summary of the current session.

    Use ``cvc handoff export`` at the end of one session and
    ``cvc handoff import <file>`` at the start of the next (or in a
    different workspace) to carry intent forward without touching
    the Merkle DAG.
    """


@handoff.command("export")
@click.option(
    "--out", "-o",
    type=click.Path(dir_okay=False, writable=True, path_type=Path),
    default=None,
    help="Output file path (default: .cvc-handoff.json in the current dir).",
)
@click.option(
    "--brief", "-b",
    default="",
    help="Free-form brief to include (shown at the top of the handoff).",
)
@click.option(
    "--max-turns", type=int, default=20, show_default=True,
    help="Max recent user turns to include.",
)
def handoff_export(out: Path | None, brief: str, max_turns: int) -> None:
    """Write a portable handoff snapshot to disk."""
    from cvc.operations.cognome_runtime import CognomeRuntime
    from cvc.operations.handoff import DEFAULT_FILENAME

    engine, _db = _get_engine()
    runtime = CognomeRuntime.for_engine(engine)
    pkg = runtime.export_handoff(brief=brief, max_turns=max_turns)
    dest = out or (Path.cwd() / DEFAULT_FILENAME)
    pkg.write_to(dest)
    console.print(
        Panel(
            f"[bold green]✓[/bold green] Handoff written\n"
            f"  file: [cyan]{dest}[/cyan]\n"
            f"  turns: {len(pkg.recent_turns)}  |  commits: {len(pkg.recent_commits)}\n"
            f"  source: {pkg.source_workspace}",
            border_style="#5C1010",
            title="[bold #CC3333]CVC Handoff · export[/bold #CC3333]",
        )
    )


@handoff.command("import")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def handoff_import(path: Path) -> None:
    """Stage a handoff snapshot for the next chat turn in this workspace."""
    from cvc.operations.cognome_runtime import CognomeRuntime
    from cvc.operations.handoff import HandoffPackage

    try:
        pkg = HandoffPackage.read_from(path)
    except Exception as exc:
        console.print(f"[bold red]✗ Failed to read handoff:[/bold red] {exc}")
        return
    engine, _db = _get_engine()
    runtime = CognomeRuntime.for_engine(engine)
    runtime.import_handoff(pkg)
    console.print(
        Panel(
            f"[bold green]✓[/bold green] Handoff staged\n"
            f"  source: [cyan]{pkg.source_workspace}[/cyan]\n"
            f"  branch: {pkg.source_branch or '-'}  |  turns: {len(pkg.recent_turns)}\n"
            f"  will be injected into the NEXT chat turn (one-shot)",
            border_style="#5C1010",
            title="[bold #CC3333]CVC Handoff · import[/bold #CC3333]",
        )
    )


@handoff.command("show")
@click.argument("path", type=click.Path(exists=True, dir_okay=False, path_type=Path))
def handoff_show(path: Path) -> None:
    """Print a handoff file as the synthetic system message it will produce."""
    from cvc.operations.handoff import HandoffPackage

    try:
        pkg = HandoffPackage.read_from(path)
    except Exception as exc:
        console.print(f"[bold red]✗ Failed to read handoff:[/bold red] {exc}")
        return
    console.print(
        Panel(
            pkg.render_system_message(),
            border_style="#5C1010",
            title="[bold #CC3333]Handoff preview[/bold #CC3333]",
        )
    )


@main.command("voice-setup")
@click.option("--first-run", is_flag=True, hidden=True, help="Treat as a first-time run (show welcome banner).")
def voice_setup(first_run: bool) -> None:
    """Interactive voice & AI configuration wizard.

    Configures your display name, LLM provider/model/API key, TTS backend
    (with live test), and wake word settings, then writes ~/.cvc/config.yaml.

    Run again at any time to update individual settings.
    """
    from cvc.setup_wizard import run_wizard

    run_wizard(first_run=first_run)


# ─────────────────────────────────────────────────────────────────────────────
# `cvc channel-setup` — single-purpose entry point for channel configuration.
#
# This is the canonical path for a user who already has CVC running and
# just wants to (re)configure one chat channel — Telegram today, Discord /
# Slack / WhatsApp / Matrix / Email / Webhook tomorrow, whatever the
# adapters register. It runs the same schema-driven wizard as
# ``cvc setup → Setup Channels`` (option 6), but without forcing the user
# through the provider/model/API-key gauntlet first.
#
# Usage:
#   cvc channel-setup                  # interactive channel picker
#   cvc channel-setup telegram         # jump straight to Telegram
#   cvc channel-setup discord          # jump straight to Discord (when ready)
#   cvc channel-setup --list           # list every available channel
#   cvc channel-setup telegram --reset # delete the saved config first
#   cvc channel-setup telegram --no-restart  # don't bounce the gateway
#
# The config is saved to ``~/.cvc/channels/<name>.yaml`` (per-user,
# isolated from the project repo) and live-validated before save
# (Telegram calls ``Bot.get_me()`` so bad tokens fail LOUDLY here
# instead of at gateway startup).
# ─────────────────────────────────────────────────────────────────────────────

_CHANNEL_RESTART_HELP = (
    "Restart the CVC gateway on success so the new config is picked up "
    "immediately. Pass --no-restart in CI or when you'll restart later "
    "yourself."
)


@main.command("channel-setup")
@click.argument(
    "channel",
    required=False,
    default=None,
    metavar="CHANNEL",
)
@click.option(
    "--list",
    "list_channels",
    is_flag=True,
    help="Print every channel registered with the gateway and exit.",
)
@click.option(
    "--reset",
    is_flag=True,
    help="Delete the saved config for CHANNEL before running the wizard.",
)
@click.option(
    "--no-restart/--restart",
    default=True,
    help=_CHANNEL_RESTART_HELP,
)
@click.pass_context
def channel_setup_cmd(
    ctx: click.Context,
    channel: str | None,
    list_channels: bool,
    reset: bool,
    no_restart: bool,
) -> None:
    """Configure one chat channel (Telegram, Discord, Slack, WhatsApp, etc.) without re-running the full provider/model wizard.

    \b
    Examples:
      cvc channel-setup                 # interactive picker
      cvc channel-setup telegram        # jump straight to Telegram
      cvc channel-setup --list          # show every available channel
      cvc channel-setup telegram --reset   # wipe saved config and start over

    The wizard is schema-driven — every adapter declares its fields in
    config_schema, and the prompts are generated automatically. Telegram
    tokens are validated live with a real Bot API ``get_me()`` call before
    anything is written to disk.
    """
    from cvc.integrations.setup import (
        list_channels_for_setup,
        run_channel_setup,
        channels_config_path,
        read_channels_config_from_path,
        save_channels_config,
        WizardCancelled as _WC2,
    )

    # ── --list: enumerate channels and exit cleanly ──────────────────
    if list_channels:
        rows = list_channels_for_setup()
        if not rows:
            _warn("No channels are registered. Check the gateway logs for import errors.")
            ctx.exit(1)
            return
        console.print(f"[bold #CC3333]  Available channels[/bold #CC3333]")
        console.print()
        for name, display, desc in rows:
            cfg_path = channels_config_path(name)
            installed = "✓ configured" if cfg_path.exists() and cfg_path.stat().st_size > 0 else "— not configured"
            console.print(f"  [bold]{name}[/bold]  [dim]({display})[/dim]  [{('#55AA55' if '✓' in installed else '#888888')}]{installed}[/]")
            if desc:
                console.print(f"      [dim]{desc}[/dim]")
        console.print()
        console.print("  [dim]Run `cvc channel-setup <name>` to configure one.[/dim]")
        return

    # ── No channel arg → interactive picker ──────────────────────────
    if channel is None:
        rows = list_channels_for_setup()
        if not rows:
            _warn("No channels are registered. Check the gateway logs for import errors.")
            ctx.exit(1)
            return
        from cvc.agent.menus import arrow_select
        options = [("← Cancel", "__cancel__")] + [
            (f"{display}  [dim]({name})[/dim]", name) for name, display, _ in rows
        ]
        console.print()
        console.print("  [dim]Pick a channel to configure.[/dim]")
        try:
            picked = arrow_select("Which channel?", options, descriptions=None, default=0)
        except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
            _info("Cancelled.")
            return
        if picked is None or picked == "__cancel__":
            _info("Cancelled.")
            return
        channel = picked

    # ── Normalize the channel name ──────────────────────────────────
    if not channel:
        _error("No channel selected.")
        return
    channel = channel.strip().lower()
    valid_names = {n for n, _, _ in list_channels_for_setup()}
    if channel not in valid_names:
        _error(f"Unknown channel: {channel!r}")
        console.print()
        console.print("  [dim]Run `cvc channel-setup --list` to see what's available.[/dim]")
        ctx.exit(2)
        return

    cfg_path = channels_config_path(channel)

    # ── --reset: wipe existing config first ────────────────────────
    if reset:
        if cfg_path.exists():
            try:
                cfg_path.unlink()
                _success(f"Removed existing config: [dim]{cfg_path}[/dim]")
            except OSError as exc:
                _error(f"Could not delete {cfg_path}: {exc}")
                ctx.exit(1)
                return
        else:
            _info(f"No existing config at {cfg_path} — nothing to reset.")

    # ── Drive the wizard (same code path as option 6 menu) ──────────
    existing = read_channels_config_from_path(cfg_path)
    console.print()
    console.print(f"[bold #CC3333]  {channel} setup[/bold #CC3333]")
    if existing:
        _info(f"Existing config: [dim]{cfg_path}[/dim]")
        console.print("  [dim]Press Enter at each prompt to keep the current value.[/dim]")
        console.print()
    else:
        _info(f"Saving to: [dim]{cfg_path}[/dim]")
        console.print()

    try:
        cfg = run_channel_setup(channel, existing=existing or None)
    except _WC2:
        _info("Cancelled — nothing was saved.")
        return

    if not cfg:
        _warn("No configuration captured. Nothing saved.")
        return

    try:
        save_channels_config(channel, cfg)
    except Exception as exc:  # noqa: BLE001
        _error(f"Failed to save config: {exc}")
        ctx.exit(1)
        return

    _success(f"Saved → [dim]{cfg_path}[/dim]")

    # Flip the global enable flag so the gateway picks it up on next start.
    try:
        from cvc.agent.settings import save_project_settings
        save_project_settings(Path.home(), f"channels.{channel}.enabled", True)
    except Exception as exc:  # noqa: BLE001
        _warn(f"Could not flip the enable flag automatically: {exc}")

    # ── Restart the gateway so the new config is live NOW ───────────
    if no_restart:
        _info(
            "Restart the gateway yourself (e.g. `cvc gateway restart`) "
            "to pick up the new config."
        )
        return

    console.print()
    _info("Restarting the gateway to pick up the new config…")
    import subprocess as _sp
    import sys as _sys
    try:
        # Subprocess-based restart so the new config is picked up by
        # a fresh process. This works for any install layout (source
        # venv, wheel, system pip). We capture output so the user
        # sees what happened; on failure we surface the error.
        _proc = _sp.run(
            [_sys.executable, "-m", "cvc.cli", "gateway", "restart", "--no-browser"],
            cwd=str(Path.cwd()),
            capture_output=True,
            text=True,
            timeout=30,
        )
        if _proc.returncode == 0:
            _success("Gateway restarted — new config is live.")
        else:
            _warn(
                f"Gateway restart exited with code {_proc.returncode}.\n"
                f"  stdout: {_proc.stdout.strip()[:200]}\n"
                f"  stderr: {_proc.stderr.strip()[:200]}\n"
                "Run `cvc gateway restart` yourself to retry."
            )
            return
    except _sp.TimeoutExpired:
        _warn("Gateway restart timed out after 30s. Run `cvc gateway restart` yourself.")
        return
    except Exception as exc:  # noqa: BLE001
        _warn(
            f"Automatic restart failed: {exc}. "
            "Run `cvc gateway restart` yourself to apply the new config."
        )
        return

    # ── Phase 2B: post-restart 'test now' round-trip ───────────────
    #
    # After the gateway restarts with the new channel config, poll
    # the channel status endpoint for a few seconds. If the channel
    # is healthy we tell the user "your bot is live — go message
    # it on Telegram". If something went wrong we tell them exactly
    # what (which the gateway's getMe() backstop should already
    # have caught) and how to fix it. This closes the loop: the
    # user no longer has to wonder whether the bot is actually
    # working — we tell them before they leave the terminal.
    console.print()
    _info("Confirming your bot is live…")
    import time as _time
    import urllib.request
    import json as _json
    healthy = False
    bot_info: dict = {}
    last_err = ""
    for attempt in range(8):  # ~4s total — gateway needs a moment to init
        _time.sleep(0.5)
        try:
            with urllib.request.urlopen(
                "http://127.0.0.1:13421/api/channels", timeout=2
            ) as resp:
                data = _json.loads(resp.read().decode("utf-8", errors="replace"))
            ch_data = next(
                (c for c in data.get("channels", []) if c.get("name") == channel),
                None,
            )
            if ch_data is not None:
                bot_info = ch_data
                last_err = ch_data.get("last_error") or ""
                if ch_data.get("healthy"):
                    healthy = True
                    break
        except Exception:
            pass

    if healthy:
        # Pull the bot's @username from the adapter info (set by
        # the gateway-side getMe() backstop).
        bot_username = (
            bot_info.get("info", {}).get("bot_username")
            or bot_info.get("info", {}).get("username")
            or f"@{channel}_bot"
        )
        console.print(
            Panel(
                f"[bold #55AA55]✓ Your bot is live.[/bold #55AA55]\n\n"
                f"  Channel:  [bold]{channel}[/bold]\n"
                f"  Status:   [bold]healthy[/bold], polling for messages\n"
                f"  Allowlist: [bold]{bot_info.get('info', {}).get('allowlist_size', 0)}[/bold] user(s)\n\n"
                f"[bold white]→ Open Telegram and message your bot now.[/bold white]\n"
                f"  It should respond within a few seconds. If it doesn't, run "
                f"`cvc doctor {channel}` to diagnose.",
                border_style="#55AA55",
                title="[bold #55AA55]✓ Channel configured[/bold #55AA55]",
                padding=(1, 2),
            )
        )
    else:
        # Channel didn't come up healthy. Surface what we know.
        console.print()
        _error(f"Channel didn't come up healthy after restart.")
        if last_err:
            console.print(f"  [dim]Gateway says:[/dim] {last_err}")
        console.print()
        console.print(
            f"  [dim]Run [bold cyan]cvc doctor {channel}[/bold cyan] for a full diagnosis.[/dim]"
        )


# ─────────────────────────────────────────────────────────────────────────────
# `cvc doctor <channel>` — diagnose channel issues end-to-end.
#
# Layer 3 of the "three layers of validation" architecture:
#   layer 1: wizard's live getMe() (catches typos at save)
#   layer 2: gateway startup getMe() (catches drift between save and start)
#   layer 3: this command — runs on demand, fixes EVERY common failure
#
# The doctor runs a sequence of checks against a configured channel,
# reports each as ✅/⚠️/❌ with a precise diagnosis, and proposes
# a one-line fix the user can run. It also tries to auto-remediate
# the safe cases (e.g. an empty allowlist prompts for the user's ID).
# Designed to answer the question "why isn't my bot responding?"
# without forcing the user to read gateway logs.
# ─────────────────────────────────────────────────────────────────────────────


@main.command("doctor")
@click.argument(
    "channel",
    required=False,
    default=None,
    metavar="CHANNEL",
)
@click.option(
    "--fix",
    "auto_fix",
    is_flag=True,
    help="Auto-remediate safe issues (prompt for missing values).",
)
@click.pass_context
def doctor_cmd(
    ctx: click.Context,
    channel: str | None,
    auto_fix: bool,
) -> None:
    """Diagnose why a chat channel isn't working.

    \b
    Examples:
      cvc doctor              # diagnose every configured channel
      cvc doctor telegram     # diagnose Telegram specifically
      cvc doctor telegram --fix   # also auto-fix safe issues

    Checks performed (Telegram):
      1. Config file exists at ~/.cvc/channels/telegram.yaml
      2. python-telegram-bot package is installed
      3. bot_token is present and well-formed
      4. bot_token is LIVE (live getMe() call to Telegram)
      5. allowlist is non-empty and well-formed
      6. gateway reports the channel as healthy

    For each check, prints ✅ / ⚠️ / ❌ with a precise diagnosis and
    a one-line fix command. Exits non-zero if any ❌ is found so it
    can be wired into CI / monitoring later.
    """
    from cvc.integrations.setup import (
        channels_config_path,
        read_channels_config_from_path,
    )

    # ── Pick which channels to diagnose ─────────────────────────────
    if channel is not None:
        channels_to_check = [channel.strip().lower()]
    else:
        # No arg → every channel with a non-empty config yaml.
        channels_to_check = []
        if channels_config_path("telegram").exists():
            channels_to_check.append("telegram")
        # Future: detect other channels the same way.

    if not channels_to_check:
        _warn("No channels configured yet. Run `cvc channel-setup <name>` first.")
        ctx.exit(1)
        return

    overall_ok = True
    for ch_name in channels_to_check:
        ok = _doctor_run_channel(ctx, ch_name, auto_fix)
        overall_ok = overall_ok and ok

    if not overall_ok:
        ctx.exit(1)


def _doctor_run_channel(ctx: click.Context, channel: str, auto_fix: bool) -> bool:
    """Run all doctor checks for one channel. Returns True if everything passes."""
    from cvc.integrations.setup import (
        channels_config_path,
        read_channels_config_from_path,
    )

    cfg_path = channels_config_path(channel)
    console.print()
    console.print(
        Panel(
            f"[bold white]Diagnosing [bold #CC3333]{channel}[/bold #CC3333][/bold white]",
            border_style="#5C1010",
            padding=(0, 2),
        )
    )

    checks_passed = 0
    checks_total = 0
    has_failure = False

    def _emit(status: str, label: str, detail: str, fix: str = "") -> None:
        nonlocal has_failure
        if status == "ok":
            icon = "[bold #55AA55]✓[/bold #55AA55]"
        elif status == "warn":
            icon = "[bold #CCAA33]⚠[/bold #CCAA33]"
        else:  # fail
            icon = "[bold #CC3333]✗[/bold #CC3333]"
            has_failure = True
        line = f"  {icon} [bold]{label}[/bold]"
        if detail:
            line += f"  [dim]{detail}[/dim]"
        console.print(line)
        if fix:
            console.print(f"      [dim]Fix:[/dim] [bold cyan]{fix}[/bold cyan]")

    # ── Check 1: config file exists ─────────────────────────────────
    checks_total += 1
    if not cfg_path.exists():
        _emit(
            "fail",
            f"Config file missing",
            f"Expected at {cfg_path}",
            fix=f"cvc channel-setup {channel}",
        )
        return False
    _emit(
        "ok",
        "Config file exists",
        str(cfg_path),
    )
    checks_passed += 1

    # ── Check 2: python-telegram-bot installed ──────────────────────
    if channel == "telegram":
        checks_total += 1
        try:
            import telegram  # noqa: F401
            _emit("ok", "python-telegram-bot installed", f"v{telegram.__version__}")
            checks_passed += 1
        except ImportError:
            _emit(
                "fail",
                "python-telegram-bot not installed",
                "The Telegram adapter can't load without this package",
                fix="pip install 'python-telegram-bot[webhooks]>=22.0'",
            )
            return False

    # ── Check 3: load config + check required fields ────────────────
    cfg = read_channels_config_from_path(cfg_path)
    checks_total += 1
    if not cfg:
        _emit(
            "fail",
            "Config file is empty or unreadable",
            "It exists but has no data",
            fix=f"cvc channel-setup {channel} --reset",
        )
        return False
    _emit(
        "ok",
        "Config file is readable",
        f"{len(cfg)} field(s)",
    )
    checks_passed += 1

    # ── Check 4: bot_token present + well-formed ────────────────────
    token = (cfg.get("bot_token") or "").strip()
    checks_total += 1
    if not token:
        _emit(
            "fail",
            "bot_token is missing or empty",
            "Every Telegram channel needs a valid bot token",
            fix=f"cvc channel-setup {channel} --reset",
        )
        return False
    if ":" not in token or not token.split(":", 1)[0].isdigit():
        _emit(
            "fail",
            "bot_token doesn't match Telegram format",
            f"Got {len(token)} chars; expected `<bot_id>:<secret>`",
            fix="Get a fresh token from @BotFather on Telegram (/revoke → /token).",
        )
        return False
    _emit(
        "ok",
        "bot_token is well-formed",
        f"{token.split(':', 1)[0]}…",
    )
    checks_passed += 1

    # ── Check 5: live getMe() — the most important check ───────────
    if channel == "telegram":
        checks_total += 1
        try:
            import asyncio
            from telegram import Bot as _TgBot

            async def _call() -> str:
                bot = _TgBot(token=token)
                try:
                    me = await bot.get_me()
                    return f"@{getattr(me, 'username', '?')} (id {getattr(me, 'id', '?')})"
                finally:
                    try:
                        await bot.shutdown()
                    except Exception:
                        pass

            try:
                info = asyncio.run(_call())
            except RuntimeError:
                # Already in an event loop — run in a thread.
                import threading
                box: list = []

                def _runner() -> None:
                    loop = asyncio.new_event_loop()
                    try:
                        asyncio.set_event_loop(loop)
                        box.append(loop.run_until_complete(_call()))
                    finally:
                        loop.close()

                t = threading.Thread(target=_runner, daemon=True)
                t.start()
                t.join(timeout=15)
                info = box[0] if box else "(timeout)"

            if info == "(timeout)":
                _emit(
                    "fail",
                    "Telegram getMe() timed out",
                    "Could not reach Telegram's API within 15s",
                    fix="Check your internet connection. If it persists, Telegram may be having an outage.",
                )
            else:
                _emit(
                    "ok",
                    "bot_token is LIVE",
                    f"Bot is {info}",
                )
                checks_passed += 1
        except Exception as exc:  # noqa: BLE001
            err = str(exc).strip() or exc.__class__.__name__
            _emit(
                "fail",
                "Telegram rejected the bot_token",
                err,
                fix=f"cvc channel-setup {channel} --reset  (then paste a fresh token)",
            )
            return False

    # ── Check 6: allowlist present and well-formed ──────────────────
    if channel == "telegram":
        checks_total += 1
        allowlist = cfg.get("allowlist") or []
        if not allowlist:
            if auto_fix:
                try:
                    raw_id = click.prompt(
                        "  Enter your numeric Telegram user ID (message @userinfobot to find it)",
                        default="",
                    ).strip()
                    if raw_id.isdigit():
                        from cvc.integrations.setup import save_channels_config
                        cfg["allowlist"] = [raw_id]
                        save_channels_config(channel, cfg)
                        _emit(
                            "ok",
                            "Allowlist populated",
                            f"Added user {raw_id}",
                        )
                        checks_passed += 1
                    else:
                        _emit(
                            "fail",
                            "Allowlist is empty",
                            "User ID must be a number",
                            fix=f"cvc channel-setup {channel} --reset",
                        )
                except (KeyboardInterrupt, EOFError, click.exceptions.Abort):
                    _emit(
                        "fail",
                        "Allowlist is empty",
                        "Cancelled before entering user ID",
                        fix=f"cvc channel-setup {channel} --reset",
                    )
            else:
                _emit(
                    "fail",
                    "Allowlist is empty",
                    "No users can talk to the bot until you add at least one",
                    fix=f"cvc doctor {channel} --fix   (will prompt for your ID)",
                )
        else:
            # Validate each entry is numeric (or -100… for groups).
            bad = [
                x for x in allowlist
                if not str(x).lstrip("-").isdigit()
            ]
            if bad:
                _emit(
                    "fail",
                    f"Allowlist has {len(bad)} invalid entries",
                    f"Non-numeric: {bad[:3]}{'…' if len(bad) > 3 else ''}",
                    fix=f"cvc channel-setup {channel} --reset",
                )
            else:
                _emit(
                    "ok",
                    f"Allowlist has {len(allowlist)} valid entr{'y' if len(allowlist) == 1 else 'ies'}",
                    f"First: {allowlist[0]}",
                )
                checks_passed += 1

    # ── Check 7: gateway reports channel healthy ────────────────────
    checks_total += 1
    try:
        import urllib.request
        import json as _json
        with urllib.request.urlopen("http://127.0.0.1:13421/api/channels", timeout=2) as resp:
            data = _json.loads(resp.read().decode("utf-8", errors="replace"))
        ch_data = next(
            (c for c in data.get("channels", []) if c.get("name") == channel),
            None,
        )
        if ch_data is None:
            _emit(
                "warn",
                "Channel not registered with gateway",
                "It may be disabled in settings.json",
                fix=f"Check `channels.{channel}.enabled` in ~/.cvc/settings.json",
            )
        elif not ch_data.get("healthy"):
            last_err = ch_data.get("last_error") or "(no error message)"
            _emit(
                "fail",
                "Gateway reports channel UNHEALTHY",
                last_err,
                fix=f"cvc gateway restart  (or run `cvc doctor {channel}` again after fixing the config)",
            )
        else:
            _emit(
                "ok",
                "Gateway reports channel healthy",
                f"polling={ch_data.get('info', {}).get('polling')}, "
                f"allowlist_size={ch_data.get('info', {}).get('allowlist_size')}",
            )
            checks_passed += 1
    except Exception as exc:  # noqa: BLE001
        _emit(
            "warn",
            "Gateway not reachable",
            f"Could not query /api/channels: {exc}",
            fix="Is the gateway running? Try `cvc gateway start`.",
        )

    # ── Summary ────────────────────────────────────────────────────
    console.print()
    if has_failure:
        console.print(
            f"  [bold #CC3333]✗ {channel} has {checks_total - checks_passed} issue(s)[/bold #CC3333]"
        )
    else:
        console.print(
            f"  [bold #55AA55]✓ {channel} is healthy — {checks_passed}/{checks_total} checks passed[/bold #55AA55]"
        )
    return not has_failure


# ── Subgroup registration ────────────────────────────────────────────


@main.group()
def voice() -> None:
    """Set up local offline voice transcription (free, no API key)."""


@voice.command("install")
def voice_install_cmd() -> None:
    """Install faster-whisper for offline browser voice input.

    After this completes, the web composer's mic button transcribes audio
    locally on the gateway — no Google/OpenAI/Groq account required, and it
    works on every browser (Edge/Chrome/Brave/Safari/Firefox).
    """
    import subprocess as _sp
    import sys as _sys
    import shutil as _shutil

    try:
        import faster_whisper  # noqa: F401
        click.secho("✓ faster-whisper already installed.", fg="green")
        return
    except Exception:
        pass

    uv = _shutil.which("uv")
    if uv:
        cmd = [uv, "pip", "install", "--python", _sys.executable, "faster-whisper>=1.0.0"]
    else:
        cmd = [_sys.executable, "-m", "pip", "install", "--upgrade", "faster-whisper>=1.0.0"]
    click.secho(f"$ {' '.join(cmd)}", fg="cyan")
    rc = _sp.call(cmd)
    if rc != 0:
        click.secho(f"Install failed (exit {rc}).", fg="red", err=True)
        raise SystemExit(rc)
    click.secho("✓ Installed. Voice input ready. Reload the web UI.", fg="green")


@voice.command("status")
def voice_status_cmd() -> None:
    """Show installed STT providers."""
    try:
        import faster_whisper  # noqa: F401
        local = True
    except Exception:
        local = False
    rows = [
        ("local_whisper (offline, free)", "✓" if local else "—"),
        ("GROQ_API_KEY", "✓" if os.environ.get("GROQ_API_KEY") else "—"),
        ("OPENAI_API_KEY", "✓" if os.environ.get("OPENAI_API_KEY") else "—"),
        ("GOOGLE_API_KEY", "✓" if (os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")) else "—"),
    ]
    for name, mark in rows:
        click.echo(f"  {mark}  {name}")
    if not local:
        click.echo("\nRun  cvc voice install  to enable free offline voice.")


try:
    from cvc.cli_copilot import copilot_group
    main.add_command(copilot_group)
except Exception:  # noqa: BLE001 — never block CLI on optional subcommand
    pass

try:
    from cvc.cli_auth import auth_group
    main.add_command(auth_group)
except Exception:  # noqa: BLE001
    pass

try:
    from cvc.cli_providers import providers_group, credentials_group
    main.add_command(providers_group)
    main.add_command(credentials_group)
except Exception:  # noqa: BLE001
    pass

try:
    from cvc.cli_loop import loop_group
    main.add_command(loop_group)
except Exception:  # noqa: BLE001
    pass

try:
    from cvc.cli_trajectory import trajectory_group
    main.add_command(trajectory_group)
except Exception:  # noqa: BLE001
    pass

try:
    from cvc.cli_team import team_group
    main.add_command(team_group)
except Exception:  # noqa: BLE001
    pass

try:
    from cvc.cli_skills import skills_group
    main.add_command(skills_group)
except Exception:  # noqa: BLE001
    pass


if __name__ == "__main__":
    main()
