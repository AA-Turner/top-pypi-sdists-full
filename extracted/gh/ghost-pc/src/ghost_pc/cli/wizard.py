"""Interactive setup wizard using questionary + rich."""

from __future__ import annotations

import shutil
import subprocess
import sys

import questionary
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from ghost_pc._node import find_node, find_npm, get_node_env
from ghost_pc.config.schema import GHOST_HOME, GhostConfig

console = Console()


def run_wizard() -> None:
    """Step-by-step interactive setup flow."""
    # 1. Banner
    console.print(
        Panel.fit(
            "[bold cyan]GhostPC Setup Wizard[/]\n"
            "[dim]This will guide you through configuring GhostPC.[/]",
            subtitle="v0.1.0",
        )
    )
    console.print()

    # 2. Prerequisites check (auto, no prompts)
    _check_prerequisites()

    # Load existing config or start fresh
    cfg = GhostConfig.load()

    # 3. Gemini API key
    cfg = _prompt_api_key(cfg)

    # 4. Model tier (Flash vs Pro)
    cfg = _prompt_model_tier(cfg)

    # 5. Browser automation method
    cfg = _prompt_browser_method(cfg)

    # 6. Optional feature groups
    cfg = _prompt_feature_groups(cfg)

    # 7. Allowed WhatsApp numbers
    cfg = _prompt_allowed_numbers(cfg)

    # 8. Advanced settings
    cfg = _prompt_advanced_settings(cfg)

    # 9. Install bridge
    _install_bridge(cfg)

    # 10. WhatsApp pairing (optional)
    _prompt_whatsapp_pairing(cfg)

    # 11. Windows autostart (optional, Windows-only)
    cfg = _prompt_autostart(cfg)

    # 12. Save config
    cfg.setup_completed = True
    cfg.save()

    # 13. Summary
    _print_summary(cfg)


def _check_prerequisites() -> None:
    """Check prerequisites and print status."""
    console.print("[bold]Checking prerequisites...[/]\n")

    # Python version
    py_ver = sys.version_info
    if py_ver >= (3, 12):
        console.print(f"  [green]OK[/]  Python {py_ver.major}.{py_ver.minor}.{py_ver.micro}")
    else:
        console.print(f"  [red]FAIL[/]  Python {py_ver.major}.{py_ver.minor} — need 3.12+")

    # Platform
    if sys.platform == "win32":
        console.print("  [green]OK[/]  Windows platform")
    else:
        console.print("  [yellow]WARN[/]  Not Windows — desktop control will be limited")

    # Node.js (checks bundled location first, then system PATH)
    node_path = find_node()
    if node_path:
        try:
            result = subprocess.run(
                [node_path, "--version"], capture_output=True, text=True, timeout=5
            )
            version = result.stdout.strip()
            console.print(f"  [green]OK[/]  Node.js {version}")
        except (subprocess.SubprocessError, OSError):
            console.print("  [yellow]WARN[/]  Node.js found but version check failed")
    else:
        console.print("  [red]FAIL[/]  Node.js not found — install from https://nodejs.org")

    # npm
    if find_npm():
        console.print("  [green]OK[/]  npm available")
    else:
        console.print("  [red]FAIL[/]  npm not found")

    console.print()


def _prompt_api_key(cfg: GhostConfig) -> GhostConfig:
    """Prompt for Gemini API key."""
    console.print("[bold]Gemini API Key[/]")
    console.print("[dim]Get one at https://aistudio.google.com/apikey[/]\n")

    default = cfg.gemini_api_key or ""
    hint = " (press Enter to keep current)" if default else ""

    key = questionary.password(
        f"Enter your Gemini API key{hint}:",
    ).ask()

    if key is None:
        # User cancelled (Ctrl+C)
        raise SystemExit(1)

    if key:
        cfg.gemini_api_key = key
    elif not default:
        console.print("[yellow]No API key set — you can add it later with ghost config set[/]")

    # Validate the key
    if cfg.gemini_api_key:
        console.print("[dim]Validating API key...[/]", end=" ")
        if _validate_api_key(cfg.gemini_api_key):
            console.print("[green]Valid![/]")
        else:
            console.print("[red]Could not validate[/]")
            use_anyway = questionary.confirm("Use this key anyway?", default=True).ask()
            if not use_anyway:
                cfg.gemini_api_key = ""

    console.print()
    return cfg


def _validate_api_key(api_key: str) -> bool:
    """Validate API key by listing models."""
    try:
        from google import genai

        client = genai.Client(api_key=api_key)
        # Just try to list models — if it works, the key is valid
        next(iter(client.models.list()))
        return True
    except Exception:
        return False


def _prompt_allowed_numbers(cfg: GhostConfig) -> GhostConfig:
    """Prompt for allowed WhatsApp numbers."""
    console.print("[bold]Allowed WhatsApp Numbers[/]")
    console.print("[dim]Comma-separated, with country code (e.g. +1234567890,+9876543210)[/]\n")

    current = ",".join(cfg.allowed_numbers) if cfg.allowed_numbers else ""
    hint = " (press Enter to keep current)" if current else ""

    numbers_str = questionary.text(
        f"Allowed numbers{hint}:",
        default=current,
    ).ask()

    if numbers_str is None:
        raise SystemExit(1)

    if numbers_str.strip():
        numbers = [n.strip() for n in numbers_str.split(",") if n.strip()]
        # Validate format
        invalid = [n for n in numbers if not n.startswith("+")]
        if invalid:
            console.print(f"[yellow]Warning: These numbers don't start with '+': {invalid}[/]")
            fix = questionary.confirm("Continue anyway?", default=False).ask()
            if not fix:
                return _prompt_allowed_numbers(cfg)
        cfg.allowed_numbers = numbers

    console.print()
    return cfg


def _prompt_model_tier(cfg: GhostConfig) -> GhostConfig:
    """Prompt for model tier — Flash (fast/cheap) vs Pro (premium reasoning)."""
    console.print("[bold]Model Tier[/]")
    console.print("[dim]Flash is fast and cheap. Pro has stronger reasoning but costs more.[/]\n")

    choices = [
        questionary.Choice("Flash (fast, cheap — recommended)", value="flash"),
        questionary.Choice("Pro (premium reasoning, higher cost)", value="pro"),
    ]

    tier = questionary.select(
        "Which model tier?",
        choices=choices,
        default="flash" if cfg.model_tier == "flash" else "pro",
    ).ask()

    if tier is None:
        raise SystemExit(1)

    cfg.model_tier = tier

    # Apply tier → model name mapping
    from ghost_pc.config.settings import _resolve_model_tier

    model, cu_model = _resolve_model_tier(tier)
    cfg.gemini_model = model
    cfg.gemini_computer_use_model = cu_model

    console.print(f"  [green]OK[/]  Using {tier} tier → {model}")
    console.print()
    return cfg


def _prompt_browser_method(cfg: GhostConfig) -> GhostConfig:
    """Prompt for browser automation method."""
    console.print("[bold]Browser Automation[/]")
    console.print("[dim]How should GhostPC interact with web browsers?[/]\n")

    choices = [
        questionary.Choice(
            "Vision only (Gemini CU, no extra deps — recommended)",
            value="vision",
        ),
        questionary.Choice(
            "CDP (Playwright, needs Chrome with --remote-debugging-port=9222)",
            value="cdp",
        ),
        questionary.Choice(
            "Browser Use (hybrid DOM+Vision, fastest for web tasks)",
            value="browser-use",
        ),
    ]

    method = questionary.select(
        "Browser automation method?",
        choices=choices,
        default=cfg.browser_method,
    ).ask()

    if method is None:
        raise SystemExit(1)

    cfg.browser_method = method

    if method == "cdp":
        console.print("  [dim]Tip: Launch Chrome with:[/] chrome.exe --remote-debugging-port=9222")
    elif method == "browser-use":
        console.print("  [dim]Tip: Install with:[/] pip install browser-use")

    console.print()
    return cfg


def _prompt_feature_groups(cfg: GhostConfig) -> GhostConfig:
    """Multi-select which optional feature groups to install."""
    console.print("[bold]Optional Features[/]")
    console.print("[dim]Select which extras to install (Space to toggle, Enter to confirm).[/]\n")

    # Map display names to pip extra names
    feature_choices = [
        questionary.Choice(
            "Desktop automation (pywinauto + pywin32 for UIA/COM)",
            value="desktop",
            checked="desktop" in cfg.installed_extras,
        ),
        questionary.Choice(
            "Browser automation (Playwright for CDP)",
            value="browser",
            checked="browser" in cfg.installed_extras,
        ),
        questionary.Choice(
            "Voice control (edge-tts + sounddevice)",
            value="voice",
            checked="voice" in cfg.installed_extras,
        ),
        questionary.Choice(
            "OCR (rapidocr-onnxruntime, cross-platform text recognition)",
            value="ocr",
            checked="ocr" in cfg.installed_extras,
        ),
    ]

    selected = questionary.checkbox(
        "Which features do you want?",
        choices=feature_choices,
    ).ask()

    if selected is None:
        raise SystemExit(1)

    if not selected:
        console.print("  [dim]No extras selected. You can install them later with pip.[/]")
        console.print()
        return cfg

    cfg.installed_extras = selected

    # Install the selected extras
    console.print(f"\n  [dim]Installing extras: {', '.join(selected)}...[/]")
    extras_str = ",".join(selected)
    pip_spec = f"ghost-pc[{extras_str}]"

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", pip_spec],
            capture_output=True,
            text=True,
            timeout=300,
        )
        if result.returncode == 0:
            console.print(f"  [green]OK[/]  Installed ghost-pc[{extras_str}]")
        else:
            # Show last line of stderr for context
            err_lines = result.stderr.strip().splitlines()
            last_err = err_lines[-1] if err_lines else "unknown error"
            console.print(f"  [red]FAIL[/]  pip install failed: {last_err}")
            console.print(f"  [dim]Run manually: pip install '{pip_spec}'[/]")
    except subprocess.TimeoutExpired:
        console.print("  [red]FAIL[/]  pip install timed out")
        console.print(f"  [dim]Run manually: pip install '{pip_spec}'[/]")
    except OSError as exc:
        console.print(f"  [red]FAIL[/]  pip error: {exc}")

    console.print()
    return cfg


def _prompt_advanced_settings(cfg: GhostConfig) -> GhostConfig:
    """Optionally customize streaming settings."""
    customize = questionary.confirm(
        "Customize advanced settings (port, FPS, quality)?", default=False
    ).ask()

    if customize is None:
        raise SystemExit(1)

    if not customize:
        console.print()
        return cfg

    # Stream port
    port_str = questionary.text("Stream port:", default=str(cfg.stream_port)).ask()
    if port_str is not None:
        cfg.stream_port = int(port_str)

    # FPS
    fps_str = questionary.text("Screen capture FPS:", default=str(cfg.screen_fps)).ask()
    if fps_str is not None:
        cfg.screen_fps = int(fps_str)

    # Quality
    quality_str = questionary.text("JPEG quality (1-100):", default=str(cfg.jpeg_quality)).ask()
    if quality_str is not None:
        cfg.jpeg_quality = int(quality_str)

    console.print()
    return cfg


def _install_bridge(cfg: GhostConfig) -> None:
    """Copy bundled bridge files and run npm install."""
    console.print("[bold]Installing WhatsApp bridge...[/]\n")

    bridge_dir = cfg.get_bridge_dir()
    bridge_dir.mkdir(parents=True, exist_ok=True)

    # Copy bundled bridge files
    try:
        from ghost_pc._bridge import get_bundled_bridge_path

        src_dir = get_bundled_bridge_path()
        if src_dir is None:
            console.print(
                "  [yellow]WARN[/]  Bundled bridge not found — "
                "copy bridge/ manually to " + str(bridge_dir)
            )
            console.print()
            return

        import shutil as sh

        for filename in ("index.js", "package.json"):
            src_file = src_dir / filename
            dst_file = bridge_dir / filename
            if src_file.exists():
                sh.copy2(src_file, dst_file)
                console.print(f"  [green]OK[/]  Copied {filename}")
            else:
                console.print(f"  [yellow]WARN[/]  {filename} not found in bundle")

        # Copy pre-bundled node_modules if available (installer build)
        src_node_modules = src_dir / "node_modules"
        if src_node_modules.is_dir():
            dst_node_modules = bridge_dir / "node_modules"
            if not dst_node_modules.exists():
                console.print("  [dim]Copying dependencies...[/]")
                sh.copytree(src_node_modules, dst_node_modules)
            console.print("  [green]OK[/]  Bridge ready")
            console.print()
            return

    except ImportError:
        console.print(
            "  [yellow]WARN[/]  Bridge bundle not available — "
            "copy bridge/ manually to " + str(bridge_dir)
        )
        console.print()
        return

    # Fallback: run npm install (pip/dev installs without pre-bundled deps)
    npm_path = find_npm()
    if npm_path:
        console.print("  [dim]Downloading dependencies...[/]")
        try:
            result = subprocess.run(
                [npm_path, "install", "--production"],
                cwd=str(bridge_dir),
                capture_output=True,
                text=True,
                timeout=120,
                env=get_node_env(),
            )
            if result.returncode == 0:
                console.print("  [green]OK[/]  Bridge ready")
            else:
                console.print(f"  [red]FAIL[/]  npm install failed: {result.stderr.strip()}")
        except subprocess.TimeoutExpired:
            console.print("  [red]FAIL[/]  Download timed out")
        except OSError as exc:
            console.print(f"  [red]FAIL[/]  npm install error: {exc}")
    else:
        console.print("  [yellow]WARN[/]  npm not found — cannot install bridge dependencies")

    console.print()


def _prompt_whatsapp_pairing(cfg: GhostConfig) -> None:
    """Optionally pair WhatsApp now."""
    pair_now = questionary.confirm("Pair WhatsApp now?", default=False).ask()

    if pair_now is None:
        raise SystemExit(1)

    if not pair_now:
        console.print("[dim]You can pair later by running ghost start.[/]\n")
        return

    console.print("[dim]Starting WhatsApp bridge for pairing...[/]")
    console.print("[dim]Scan the QR code with WhatsApp on your phone.[/]")
    console.print("[dim]Press Ctrl+C when done.[/]\n")

    bridge_dir = cfg.get_bridge_dir()
    index_js = bridge_dir / "index.js"

    if not index_js.exists():
        console.print("[red]Bridge not installed. Run ghost setup again.[/]\n")
        return

    node_path = find_node()
    if not node_path:
        console.print("[red]Node.js not found. Please reinstall GhostPC.[/]\n")
        return

    env = {
        **get_node_env(),
        "GHOST_CREDENTIALS_DIR": str(cfg.get_credentials_dir()),
    }

    try:
        proc = subprocess.Popen(
            [node_path, str(index_js)],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=env,
        )
        console.print("[dim]Waiting for QR code... (Ctrl+C to stop)[/]")
        proc.wait(timeout=120)
    except KeyboardInterrupt:
        if proc.poll() is None:
            proc.terminate()
        console.print("\n[yellow]Pairing stopped.[/]")
    except subprocess.TimeoutExpired:
        if proc.poll() is None:
            proc.terminate()
        console.print("[yellow]Pairing timed out.[/]")

    console.print()


def _prompt_autostart(cfg: GhostConfig) -> GhostConfig:
    """Optionally set up Windows autostart."""
    if sys.platform != "win32":
        return cfg

    autostart = questionary.confirm("Auto-start GhostPC on login?", default=False).ask()

    if autostart is None:
        raise SystemExit(1)

    if autostart:
        try:
            if getattr(sys, "frozen", False):
                ghost_cmd = sys.executable
            else:
                ghost_cmd = shutil.which("ghost") or "ghost"
            subprocess.run(
                [
                    "schtasks",
                    "/Create",
                    "/TN",
                    "GhostPC",
                    "/SC",
                    "ONLOGON",
                    "/RL",
                    "LIMITED",
                    "/TR",
                    f'"{ghost_cmd}" start',
                    "/F",
                ],
                capture_output=True,
                text=True,
                timeout=10,
            )
            cfg.autostart_enabled = True
            console.print("[green]Autostart configured.[/]")
        except (subprocess.SubprocessError, OSError) as exc:
            console.print(f"[red]Failed to set autostart: {exc}[/]")
    else:
        cfg.autostart_enabled = False

    console.print()
    return cfg


def _print_summary(cfg: GhostConfig) -> None:
    """Print a summary of the configuration."""
    table = Table(title="GhostPC Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")

    api_display = cfg.gemini_api_key[:8] + "..." if cfg.gemini_api_key else "[red]Not set[/]"
    table.add_row("API Key", api_display)
    table.add_row("Model Tier", cfg.model_tier)
    table.add_row("Model", cfg.gemini_model)
    table.add_row("Browser Method", cfg.browser_method)
    table.add_row("Allowed Numbers", ", ".join(cfg.allowed_numbers) or "[dim]None[/]")
    table.add_row("Stream Port", str(cfg.stream_port))
    table.add_row("Screen FPS", str(cfg.screen_fps))
    table.add_row("JPEG Quality", str(cfg.jpeg_quality))
    table.add_row("Extras", ", ".join(cfg.installed_extras) or "[dim]None[/]")
    table.add_row("Bridge Dir", str(cfg.get_bridge_dir()))
    table.add_row("Credentials Dir", str(cfg.get_credentials_dir()))
    table.add_row("Config File", str(GHOST_HOME / "config.json"))

    console.print()
    console.print(table)
    console.print()
    console.print("[bold green]Setup complete![/] Run [bold]ghost start[/] to begin.")
    console.print()
