#!/usr/bin/env python3
"""PW Agent — CLI coding assistant powered by your Ollama GPUs via PastaWater."""

import argparse
import os
import sys
import time
import requests

from rich.console import Console
from rich.panel import Panel
from prompt_toolkit import prompt as pt_prompt
from prompt_toolkit import PromptSession
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import Completer, Completion, PathCompleter
from prompt_toolkit.formatted_text import HTML, FormattedText
from prompt_toolkit.key_binding import KeyBindings

from llm_client import LLMClient
from agent import Agent, get_model_warning
from config import (
    load_config, save_config, has_config, DEFAULT_CONFIG_DIR,
    get_active_instance, add_instance, remove_instance,
    instance_key_for_brain, instance_key_for_cloud,
)


VERSION = "1.50.35"
console = Console()

BANNER = """[bold cyan]
 ╔═══════════════════════════════════════════════╗
 ║  PW Agent v{version}                              ║
 ║  Coding assistant on your own GPUs           ║
 ╚═══════════════════════════════════════════════╝
[/bold cyan]"""

HELP_TEXT = """[dim]
Commands:
  /add FILE     Add a file to context (@file also works)
  /plan         Switch to Plan mode (read-only analysis)
  /build        Switch to Build mode (full read/write access)
  /think        Toggle thinking mode (Ctrl+T shortcut; defaults ON on thinking-capable models)
  /thinking     Show last reasoning block
  /memory       MemPalace — list / recall <q> / curate / forget <id> / prune (try /memory help)
  /clear        Clear conversation history
  /commit       Generate commit message and commit
  /diff         Show unstaged changes
  /skills       List available skills (auto-loaded based on query)
  /skill <name> Manually load a skill into the conversation
  /index        Index project codebase for semantic search
  /forget       Clear the codebase index
  /voice [on|off] Toggle continuous voice mode (auto-speak responses)
  /say <text>   One-off TTS via fleet audio service
  /remember <fact>  Save a fact to your global cross-project profile
  /profile      Show what pw-agent remembers about you globally
  /forget-me    Wipe the global profile
  /train [sub]  LoRA fine-tuning prep — prep | status | recipe
  /fleet        List sibling pw-agent instances on this machine
  /hooks        Show configured shell hooks (~/.pw-agent/hooks/)
  /mcp [sub]    Manage MCP servers — list | add | remove | reload | tools
  /models       Show all fleet GPUs and active models
  /instances    List saved connections
  /connect      Add a new cloud or local connection
  /use N        Switch instance (0=local, 1-5=cloud slot)
  /disconnect N Remove instance (0=local, N=cloud slot)
  /refresh      Re-detect model (if changed on GPU Setup)
  /update       Update pw-agent to latest version
  /config       Show saved config
  /logout       Clear all saved config
  /quit         Exit (or Ctrl+D)

Flags: -y/--yes (auto-approve), --no-think (disable reasoning at launch), -c/--continue (resume), -p "prompt" (one-shot), --instance N, --output-format [text|stream-json|json]
[/dim]"""
# ─── First-run interactive setup ──────────────────────────────────────────────

_EMBED_MODEL_MARKERS = ("embed", "bge-", "-bge", "e5-", "-e5", "gte-", "-gte", "nomic-embed")


def _is_embed_model(name: str) -> bool:
    """Embedding-only models (nomic-embed-text, bge-*, e5-*, gte-*) should
    never be auto-picked as the chat model — they return empty strings when
    sent /api/chat prompts. Filter conservatively by common marker substrings."""
    n = (name or "").lower()
    return any(m in n for m in _EMBED_MODEL_MARKERS)


def _filter_chat_models(models: list[str]) -> list[str]:
    """Drop embed-only models from a list when we're picking a chat model."""
    return [m for m in models if not _is_embed_model(m)]


def _pick_model(models: list[str]) -> str:
    """Let user pick from a list of models. Returns chosen model name."""
    models = _filter_chat_models(models) or models
    if len(models) == 1:
        console.print(f"  [green]✓ Using: {models[0]}[/green]")
        return models[0]
    console.print("  [bold]Available models:[/bold]")
    for i, m in enumerate(models, 1):
        console.print(f"    [cyan]{i}[/cyan] — {m}")
    console.print()
    pick = pt_prompt(f"  Choose model [1-{len(models)}]: ").strip()
    try:
        return models[int(pick) - 1]
    except (ValueError, IndexError):
        return models[0]


def _add_local_brain(cfg: dict, existing_keys: set, brain: dict | None = None) -> tuple[dict, str, dict] | None:
    """Add a local brain connection. Auto-scans if no brain provided."""
    if not brain:
        console.print("\n  [dim]Scanning for local brain...[/dim]")
        brains = scan_local_brains()
        if not brains:
            console.print("  [red]No local brain found.[/red]")
            console.print("  [dim]Start PastaWater brain or Ollama first.[/dim]")
            return None
        brain = brains[0]

    key = instance_key_for_brain(brain["url"])
    if key in existing_keys:
        console.print(f"  [dim]Local brain on port {brain['port']} already added.[/dim]")
        return None

    console.print(f"  [green]✓ Found brain on port {brain['port']}[/green]")

    # Always require PW token — even for local Ollama
    console.print()
    console.print("  [dim]PastaWater account required.[/dim]")
    console.print("  [dim]Get your token from:[/dim] [underline cyan]https://pastawater.io/settings?tab=cli[/underline cyan]")
    console.print()
    pw_token = pt_prompt("  Paste your PW token: ").strip()
    if not pw_token:
        console.print("  [red]No token provided.[/red]")
        return None

    # Validate the token against PastaWater API
    try:
        resp = requests.get(
            "https://pastawater.io/api/user/byog/slots",
            headers={"Authorization": f"Bearer {pw_token}"},
            timeout=10,
        )
        if resp.status_code == 401:
            console.print("  [red]✗ Invalid token. Sign up at pastawater.io[/red]")
            return None
        if resp.status_code != 200:
            console.print(f"  [red]✗ Token validation failed ({resp.status_code})[/red]")
            return None
        console.print("  [green]✓ Token verified[/green]")
    except Exception as e:
        console.print(f"  [red]✗ Could not verify token: {e}[/red]")
        return None

    # Fetch models from brain (with auth if needed)
    if brain.get("needs_key"):
        try:
            resp = requests.get(
                f"{brain['url']}/api/tags",
                headers={"Authorization": f"Bearer {pw_token}"},
                timeout=10,
            )
            if resp.status_code == 200:
                brain["models"] = [m["name"] for m in resp.json().get("models", [])]
        except Exception:
            pass

    all_models = brain["models"]
    if not all_models:
        console.print("  [yellow]No models loaded. Start an LLM on GPU Setup first.[/yellow]")
        return None

    instance: dict = {"mode": "brain", "brain_url": brain["url"]}
    if pw_token:
        instance["token"] = pw_token
    instance["model"] = _pick_model(all_models)
    instance["name"] = f"Local ({instance['model']})"
    cfg = add_instance(cfg, key, instance)
    console.print(f"  [green]✓ Added: {instance['name']}[/green]")
    return cfg, key, instance


def _add_cloud(cfg: dict, existing_keys: set) -> tuple[dict, str, dict] | None:
    """Add a cloud connection via PastaWater token."""
    console.print()
    console.print("  [dim]Get your token from:[/dim] [underline cyan]https://pastawater.io/settings?tab=cli[/underline cyan]")
    console.print()
    token = pt_prompt("  Paste your PW token: ").strip()
    if not token:
        console.print("  [red]No token provided.[/red]")
        return None

    console.print(f"\n  [dim]Connecting to PastaWater...[/dim]")
    temp_client = LLMClient(token=token)
    devices = temp_client.list_devices()

    if not devices:
        console.print("  [yellow]⚠ No GPUs with LLM running found.[/yellow]")
        console.print("  [dim]Start an LLM model on https://pastawater.io/gpu-setup first.[/dim]")
        return None

    available = [d for d in devices if instance_key_for_cloud(d["slot"]) not in existing_keys]
    if not available:
        console.print("  [dim]All available GPUs are already added.[/dim]")
        return None

    console.print(f"  [green]✓ Found {len(available)} new GPU(s) with LLM:[/green]\n")
    for i, d in enumerate(available, 1):
        console.print(f"    [cyan]{i}[/cyan] — [bold]{d['device_name']}[/bold]  {d['gpu']} ({d['vram_gb']}GB)  [dim]{d['llm_model']}[/dim]")
    console.print()

    if len(available) == 1:
        chosen = available[0]
        console.print(f"  [green]✓ Auto-selected: {chosen['device_name']}[/green]")
    else:
        pick = pt_prompt(f"  Choose GPU [1-{len(available)}]: ").strip()
        try:
            chosen = available[int(pick) - 1]
        except (ValueError, IndexError):
            chosen = available[0]

    key = instance_key_for_cloud(chosen["slot"])
    instance = {
        "mode": "cloud",
        "name": f"{chosen['device_name']} ({chosen['gpu']})",
        "token": token,
        "slot": chosen["slot"],
        "device_id": chosen["device_id"],
        "device_name": chosen["device_name"],
        "model": chosen["llm_model"],
    }
    cfg = add_instance(cfg, key, instance)
    console.print(f"  [green]✓ Added: {instance['name']}[/green]")
    return cfg, key, instance


def add_connection(cfg: dict) -> tuple[dict, str, dict] | None:
    """Interactive flow to add a new connection. Always shows choice menu."""
    existing_keys = set(cfg.get("instances", {}).keys())

    # Scan for local brain in background to show status
    local_brains = scan_local_brains()
    local_available = local_brains and instance_key_for_brain(local_brains[0]["url"]) not in existing_keys

    console.print()
    console.print("  [bold]How do you want to connect?[/bold]")
    console.print(f"  [cyan]1[/cyan] — Local GPU [dim](direct to Ollama on this machine{', detected!' if local_available else ''})[/dim]")
    console.print("  [cyan]2[/cyan] — PastaWater Cloud [dim](remote GPUs via API token)[/dim]")
    console.print()
    mode = pt_prompt("  Choose [1/2]: ").strip()

    if mode == "1":
        return _add_local_brain(cfg, existing_keys, local_brains[0] if local_brains else None)
    else:
        return _add_cloud(cfg, existing_keys)


def run_setup() -> dict:
    """First-run setup. Returns config dict with at least one instance."""
    console.print()
    console.print(Panel(
        "[bold]Welcome to PW Agent![/bold]\n\n"
        "Let's connect you to your GPU fleet.\n"
        "This only takes a few seconds.",
        border_style="cyan",
        padding=(1, 2),
    ))

    cfg: dict = {"config_dir": DEFAULT_CONFIG_DIR, "instances": {}}
    result = add_connection(cfg)
    if result:
        cfg = result[0]
    path = save_config(cfg, DEFAULT_CONFIG_DIR)
    console.print(f"\n  [dim]Config saved to {path}[/dim]\n")
    return cfg


# ─── GPU listing ──────────────────────────────────────────────────────────────

def _ordered_instances(instances: dict) -> list[tuple[str, dict]]:
    """Return instances ordered with local/direct first, then cloud slots in slot order.

    This ensures local GPU instances always show as #0 regardless of insertion order,
    and cloud instances keep their actual slot numbers (matching the GPU Setup page).
    """
    local_items = []
    cloud_items = []
    for k, inst in instances.items():
        mode = inst.get("mode", "")
        if mode in ("brain", "direct"):
            local_items.append((k, inst))
        else:
            cloud_items.append((k, inst))
    # Sort cloud items by slot number
    cloud_items.sort(key=lambda kv: kv[1].get("slot", 999))
    return local_items + cloud_items


def _instance_display_number(inst: dict, idx_among_locals: int = 0) -> str:
    """Return the stable display number for an instance.

    - Local/direct instances: "0" (first), "0b", "0c" for extras
    - Cloud instances: their actual slot number (1, 2, 3...)
    """
    mode = inst.get("mode", "")
    if mode in ("brain", "direct"):
        if idx_among_locals == 0:
            return "0"
        return f"0{chr(ord('b') + idx_among_locals - 1)}"
    return str(inst.get("slot", "?"))


def refresh_status(status_obj, client, cfg, args, agent):
    """Update the status object with current agent/client/config state."""
    inst = get_active_instance(cfg)
    model = client.model or inst.get("model", "unknown")
    name = inst.get("name", "unknown")
    
    # Store raw text for the FormattedText renderer
    status_obj["engine_text"] = f"🧠 {model}"
    status_obj["hardware_text"] = f"🖥️ {name}"
    status_obj["mode_text"] = "⚙️ PLAN" if agent.plan_mode else "⚙️ BUILD"

    flags = []
    if args.yes:
        flags.append("⚡ AUTO-APPROVE")
    if agent.thinking:
        flags.append("🧠 THINKING")
    status_obj["flag_text"] = " | ".join(flags)

    # For spinner status bar — needs 3+ parts for colored rendering
    mode = "PLAN" if agent.plan_mode else "BUILD"
    bar_parts = [model, name, mode]
    if agent.thinking:
        bar_parts.append("🧠 THINKING")
    agent.status_text = " | ".join(bar_parts)


def do_refresh(client, cfg, status_obj, args, agent, silent=False):
    """Re-detect model for the current client and sync with config."""
    if client.direct_mode:
        try:
            headers = {"Authorization": f"Bearer {client.token}"} if client.token else {}
            brain_key = headers.get("Authorization", "")
            # Also try controller API key header (brain uses X-Controller-API-Key)
            ctrl_headers = dict(headers)
            if client.token:
                ctrl_headers["X-Controller-API-Key"] = client.token

            # Strategy: try 3 sources in priority order
            #   1. /status → llm_current_model — brain's own tracked ACTIVE
            #      chat model (set by set_ollama_model). Authoritative.
            #   2. /api/ps — models resident in VRAM. Multiple can be loaded
            #      (chat + embed), and order is unstable — so we prefer the
            #      one matching client.model when available, else any non-embed.
            #   3. /api/tags — every model ever pulled. Last resort.
            running_model = None

            # 1. /api/ps — actual VRAM state. Ground truth. /status's
            # llm_current_model is a tracked-state cache that goes stale
            # when the user loads a model outside set_ollama_model.
            ps_chat_models = []
            try:
                ps_resp = requests.get(
                    f"{client.brain_url}/api/ps",
                    headers=headers, timeout=5,
                )
                if ps_resp.status_code == 200:
                    ps_chat_models = [m for m in ps_resp.json().get("models", []) if not _is_embed_model(m.get("name", ""))]
                    if len(ps_chat_models) == 1:
                        running_model = ps_chat_models[0].get("name")
            except Exception:
                pass

            # 2. /status — only to disambiguate when multiple chat models loaded
            if not running_model and len(ps_chat_models) > 1:
                try:
                    status_resp = requests.get(
                        f"{client.brain_url}/status",
                        headers=ctrl_headers, timeout=5,
                    )
                    if status_resp.status_code == 200:
                        llm_model = status_resp.json().get("llm_current_model")
                        if llm_model and not _is_embed_model(llm_model):
                            if any(m.get("name") == llm_model for m in ps_chat_models):
                                running_model = llm_model
                except Exception:
                    pass
                if not running_model and ps_chat_models:
                    running_model = ps_chat_models[0].get("name")

            # 3. /api/tags — all pulled models (fallback, picks first alphabetically)
            if not running_model:
                resp = requests.get(
                    f"{client.brain_url}/api/tags",
                    headers=headers, timeout=5,
                )
                if resp.status_code == 200:
                    available = _filter_chat_models([m["name"] for m in resp.json().get("models", [])])
                    if available:
                        running_model = available[0]

            if running_model:
                old = client.model
                client.model = running_model
                inst = get_active_instance(cfg)
                if inst:
                    inst["model"] = client.model
                    inst["name"] = f"Local ({client.model})"
                    save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                if not silent:
                    if old != client.model:
                        console.print(f"  [green]✓ Model changed: {old} → {client.model}[/green]")
                    else:
                        console.print(f"  [dim]Model unchanged: {client.model}[/dim]")
                refresh_status(status_obj, client, cfg, args, agent)
            elif not silent:
                console.print("  [yellow]No models found on brain.[/yellow]")
        except Exception as e:
            if not silent: console.print(f"  [red]✗ {e}[/red]")
    else:
        # Cloud mode
        temp = LLMClient(token=client.token, api_url=client.api_url)
        devices = temp.list_devices()
        if devices:
            for d in devices:
                if d["slot"] == client.slot:
                    old = client.model
                    client.model = d["llm_model"]
                    inst = get_active_instance(cfg)
                    if inst:
                        inst["model"] = client.model
                        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                    if not silent:
                        if old != client.model:
                            console.print(f"  [green]✓ Model changed: {old} → {client.model}[/green]")
                        else:
                            console.print(f"  [dim]Model unchanged: {client.model}[/dim]")
                    refresh_status(status_obj, client, cfg, args, agent)
                    return True
        elif not silent:
            console.print("  [yellow]No GPUs with LLM found.[/yellow]")
    return False


def _heal_embed_pollution(cfg) -> int:
    """Self-heal: scrub embedding-model names from saved instance configs.
    Old sessions where pw-agent's auto-detect picked nomic-embed-text left
    embed model ids in `inst["model"]` — chatting against them returns
    empty strings. Reset to a safe chat default. Runs unconditionally on
    every startup; cheap."""
    updated = 0
    for key, inst in cfg.get("instances", {}).items():
        m = str(inst.get("model", "")).lower()
        if m and _is_embed_model(m):
            inst["model"] = "qwen3-coder:30b"  # sane chat default
            # Also fix the stale 'Local (nomic-embed-text:latest)' display name
            old_name = str(inst.get("name", ""))
            if "embed" in old_name.lower() or "nomic" in old_name.lower():
                dev = inst.get("device_name") or key
                inst["name"] = dev
            updated += 1
    if updated:
        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
    return updated


def refresh_all_instances(cfg, client_template):
    """Update model info for ALL saved cloud instances."""
    instances = cfg.get("instances", {})
    if not instances:
        return

    # Defense-in-depth: scrub any embed-model pollution on every refresh.
    # Runs regardless of cloud/local to self-heal old sessions.
    _heal_embed_pollution(cfg)

    # We only auto-refresh cloud instances because they are easy to bulk-query
    # Local brains are skipped to avoid timeouts/wait times
    temp_client = LLMClient(token=client_template.token, api_url=client_template.api_url)
    devices = temp_client.list_devices()

    if not devices:
        return

    updated_count = 0
    for key, inst in instances.items():
        if inst.get("mode") == "cloud":
            slot = inst.get("slot")
            device = next((d for d in devices if d["slot"] == slot), None)
            if device:
                old_model = inst.get("model")
                new_model = device.get("llm_model")
                # Never overwrite saved model with an embed-only value
                if new_model and old_model != new_model and not _is_embed_model(new_model):
                    inst["model"] = new_model
                    updated_count += 1
                # Heal stale 'Local (...)' names carried over from pre-cloud configs.
                device_name = device.get("device_name") or ""
                gpu = device.get("gpu") or ""
                if device_name and str(inst.get("name", "")).startswith("Local ("):
                    inst["name"] = f"{device_name} ({gpu})" if gpu else device_name
                    inst["device_name"] = device_name
                    updated_count += 1

    if updated_count > 0:
        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
        return updated_count
    return 0


def print_models(client: LLMClient):
    """Print a table of all fleet GPUs and their LLM status."""
    from rich.table import Table

    devices = client.list_devices()
    if not devices:
        console.print("  [yellow]No GPUs with LLM running found.[/yellow]")
        return

    table = Table(
        title="Active Engines on Your Fleet",
        title_style="bold white",
        border_style="dim",
        show_lines=False,
        pad_edge=False,
        padding=(0, 2),
    )
    table.add_column("Slot", style="cyan", width=5)
    table.add_column("GPU", style="white")
    table.add_column("Model", style="bold")
    table.add_column("VRAM", style="dim", justify="right")
    table.add_column("Status", justify="right")

    for d in devices:
        is_active = d["device_id"] == client.device_id
        status = "[bold green]● Active[/bold green]" if is_active else "[dim]Idle[/dim]"
        model_display = d["llm_model"] or "—"
        table.add_row(
            str(d["slot"]),
            f"{d['device_name']}\n[dim]{d['gpu']}[/dim]",
            model_display,
            f"{d['vram_gb']}GB",
            status,
        )

    console.print()
    console.print(table)
    console.print("\n  [dim]Type /switch <slot> to change active engine.[/dim]\n")


def check_for_update() -> str | None:
    """Check PyPI for a NEWER version. Returns new version string or None.

    Compares semantically — only suggests an update when PyPI is strictly
    greater than the installed VERSION, so a locally-built dev version
    that's ahead of PyPI doesn't get flagged as needing a downgrade.
    """
    def _parse(v: str) -> tuple:
        try:
            return tuple(int(x) for x in v.split(".") if x.isdigit())
        except Exception:
            return (0,)
    try:
        resp = requests.get("https://pypi.org/pypi/pw-agent/json", timeout=5)
        if resp.status_code == 200:
            latest = resp.json()["info"]["version"]
            if _parse(latest) > _parse(VERSION):
                return latest
    except Exception:
        pass
    return None


def do_update() -> bool:
    """Update pw-agent to latest. Detects install method and uses the right tool."""
    import subprocess
    import shutil

    # Detect dev install (editable / pip install -e)
    egg_link = os.path.join(os.path.dirname(__file__), "pw_agent.egg-info")
    if os.path.exists(egg_link):
        # Dev install — reinstall from local source
        src_dir = os.path.dirname(os.path.abspath(__file__))
        console.print(f"  [dim]Dev install detected. Reinstalling from {src_dir}...[/dim]")
        result = subprocess.run(
            ["pip", "install", "-e", src_dir, "--break-system-packages", "--no-deps"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            console.print(f"  [green]✓ Reinstalled from source![/green] [dim]Restart pw-agent to use the new version.[/dim]")
            return True
        console.print(f"  [red]✗ Failed: {result.stderr[:200]}[/red]")
        return False

    console.print("  [dim]Updating pw-agent...[/dim]")

    # Detect if running from pipx venv
    is_pipx = "pipx" in (sys.prefix or "") or "pipx" in (sys.executable or "")

    if is_pipx or shutil.which("pipx"):
        result = subprocess.run(
            ["pipx", "upgrade", "pw-agent", "--force", "--pip-args=--no-cache-dir"],
            capture_output=True, text=True, timeout=60,
        )
        if result.returncode == 0:
            console.print(f"  [green]✓ Updated![/green] [dim]Restart pw-agent to use the new version.[/dim]")
            return True

    # Fallback to pip
    for cmd in [
        ["pip", "install", "--upgrade", "--no-cache-dir", "--break-system-packages", "pw-agent"],
        ["pip3", "install", "--upgrade", "--no-cache-dir", "--break-system-packages", "pw-agent"],
        ["pip", "install", "--upgrade", "--no-cache-dir", "pw-agent"],
    ]:
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            if result.returncode == 0:
                console.print(f"  [green]✓ Updated![/green] [dim]Restart pw-agent to use the new version.[/dim]")
                return True
        except FileNotFoundError:
            continue

    console.print(f"  [red]✗ Update failed. Try manually: pipx upgrade pw-agent[/red]")
    return False


def scan_local_brains() -> list[dict]:
    """Scan common ports for local Ollama/brain instances.
    Returns list of {"url": ..., "port": ..., "models": [...], "needs_key": bool}."""
    import requests
    found = []
    for port in [41789, 11434, 8080, 11435]:
        url = f"http://localhost:{port}"
        try:
            resp = requests.get(f"{url}/api/tags", timeout=2)
            if resp.status_code == 200:
                models = [m["name"] for m in resp.json().get("models", [])]
                found.append({"url": url, "port": port, "models": models, "needs_key": False})
            elif resp.status_code == 401:
                # Brain with auth — detected but needs API key to list models
                found.append({"url": url, "port": port, "models": [], "needs_key": True})
        except Exception:
            # Also check if it's a brain by hitting /health (no auth needed)
            try:
                resp = requests.get(f"{url}/health", timeout=2)
                if resp.status_code == 200 and "version" in resp.text:
                    found.append({"url": url, "port": port, "models": [], "needs_key": True})
            except Exception:
                pass
    return found


def detect_brain_url() -> str | None:
    """Check if there's a local brain running. Returns first found URL."""
    brains = scan_local_brains()
    return brains[0]["url"] if brains else None
    return None


# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="PW Agent — CLI coding assistant powered by your Ollama GPUs",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--token", default=os.environ.get("PW_TOKEN"), help="PastaWater API token (or PW_TOKEN env)")
    parser.add_argument("--model", default=None, help="Ollama model name")
    parser.add_argument("--api-url", default=os.environ.get("PW_API_URL", "https://pastawater.io"), help="PastaWater API URL")
    parser.add_argument("--brain", default=os.environ.get("PW_BRAIN_URL", ""), help="Direct brain URL")
    parser.add_argument("--no-stream", action="store_true", help="Disable streaming output")
    parser.add_argument("--stream", action="store_true", help="In -p mode, flush tokens to stdout as they generate (like Claude/codex/gemini CLIs)")
    parser.add_argument("--max-iterations", dest="max_iterations", type=int, default=50, metavar="N", help="Max tool-call turns per prompt (default 50; raise for long autonomous tasks)")
    parser.add_argument("--instance", type=int, default=None, metavar="N", help="Use instance N (from /instances list)")
    parser.add_argument("--setup", action="store_true", help="Re-run first-time setup")
    parser.add_argument("-p", "--print", dest="one_shot", metavar="PROMPT", help="Non-interactive: send prompt, print response, exit")
    parser.add_argument("-y", "--yes", action="store_true", help="Auto-approve all tool actions (no confirmation prompts)")
    # Thinking defaults ON for thinking-capable models (qwen3.5, qwen3.6,
    # gemma4). Users can toggle at runtime with Ctrl+T / /think, or disable
    # at launch with --no-think. Caveat: Ollama has open bugs where
    # think:false returns empty content on some paths — see ollama #14793.
    parser.add_argument("--think", action="store_true", help=argparse.SUPPRESS)  # legacy, default is ON
    parser.add_argument("--no-think", dest="no_think", action="store_true", help="Launch with reasoning disabled (default: on for thinking-capable models)")
    parser.add_argument("--big-ctx", dest="big_ctx", action="store_true", help="Request the model's native context (allows Ollama CPU offload — slower but huge context)")
    parser.add_argument("--num-ctx", dest="num_ctx", type=int, default=None, metavar="N", help="Override context window size (tokens). Passed directly to Ollama num_ctx.")
    parser.add_argument("--session-id", dest="session_id", default=None, metavar="ID", help="Session ID for persistent history. Same ID across -p invocations resumes context automatically.")
    parser.add_argument("-c", "--continue", dest="resume", action="store_true", help="Resume the latest session in this directory")
    parser.add_argument("--output-format", choices=["text", "stream-json", "json"], default="text",
                        help="Output format for -p mode: text (default), stream-json (Claude-compatible NDJSON), json (single JSON object)")
    parser.add_argument("--mcp-server", action="store_true", help="Run as an MCP server (JSON-RPC over stdio) instead of an interactive REPL")
    parser.add_argument("subcommand", nargs="?", default=None, help=argparse.SUPPRESS)
    parser.add_argument("--version", action="version", version=f"pw-agent {VERSION}")

    args = parser.parse_args()

    # ─── MCP server mode (pw-agent serve-mcp) ─────────────────────────
    # Flips pw-agent into an MCP server that other clients (Cursor,
    # Claude Desktop) can connect to via JSON-RPC over stdio.
    if args.mcp_server or args.subcommand == "serve-mcp":
        from mcp_server import run_mcp_server
        # Try to build a client for chat_with_fleet — best-effort
        client_for_mcp = None
        try:
            cfg = load_config()
            if args.token:
                client_for_mcp = LLMClient(token=args.token, model=args.model or "", api_url=args.api_url)
            elif args.brain:
                client_for_mcp = LLMClient(brain_url=args.brain, model=args.model or "")
            else:
                inst = get_active_instance(cfg)
                if inst:
                    if inst.get("mode") in ("brain", "direct"):
                        client_for_mcp = LLMClient(brain_url=inst.get("brain_url", ""), token=inst.get("token", ""), model=inst.get("model", ""))
                    else:
                        client_for_mcp = LLMClient(
                            token=inst.get("token", ""),
                            device_id=inst.get("device_id", ""),
                            slot=inst.get("slot", 0),
                            model=inst.get("model", ""),
                            api_url=args.api_url,
                        )
        except Exception:
            pass  # MCP server still works without a client; chat_with_fleet just errors
        run_mcp_server(client=client_for_mcp)
        return

    # In one-shot mode (-p), suppress all UI chrome for clean piped output
    quiet = bool(args.one_shot)

    if not quiet:
        console.print(BANNER.format(version=VERSION))

    # ─── Session start hooks ──────────────────────────────────────────
    if not quiet:
        try:
            from hooks import run_hook as _run_hook
            _, hook_banner = _run_hook("session_start", {"version": VERSION, "cwd": os.getcwd()})
            if hook_banner:
                console.print(f"  [dim]🪝 {hook_banner}[/dim]")
        except Exception:
            pass

    # ─── Check for updates (non-blocking) ─────────────────────────────
    if not quiet:
        latest = check_for_update()
        if latest:
            console.print(f"  [yellow]Update available: v{VERSION} → v{latest}[/yellow]  [dim]Run /update to install[/dim]")

    # ─── Load or run setup ────────────────────────────────────────────
    cfg = load_config()

    # Self-heal: scrub any embed-model pollution left in saved configs from
    # older pw-agent versions where auto-detect would grab nomic-embed-text.
    try:
        _heal_embed_pollution(cfg)
    except Exception:
        pass

    if args.setup or (not cfg.get("instances") and not args.token and not args.brain):
        cfg = run_setup()

    # ─── Build client from active instance or CLI args ────────────────
    def build_client_from_instance(inst: dict) -> LLMClient | None:
        """Create an LLMClient from an instance config."""
        if inst.get("mode") in ("brain", "direct"):
            return LLMClient(brain_url=inst.get("brain_url", ""), token=inst.get("token", ""), model=inst.get("model", ""))
        elif inst.get("mode") == "cloud":
            return LLMClient(
                token=inst.get("token", ""),
                device_id=inst.get("device_id", ""),
                slot=inst.get("slot", 0),
                model=inst.get("model", ""),
                api_url=args.api_url,
            )
        return None

    # CLI args override config
    if args.brain:
        # --brain accepts either a URL (http://host:port) OR a saved-instance
        # name/key (e.g. "local-wsl", "mishka-vm", "jugnau"). When given a name,
        # resolve to that instance's brain_url + token so the user doesn't have
        # to pass --token separately.
        brain_arg = args.brain.strip()
        resolved_token = args.token or ""
        saved_model = ""
        if not (brain_arg.startswith("http://") or brain_arg.startswith("https://")):
            instances = cfg.get("instances", {})
            needle = brain_arg.lower()
            # Prefer instances that actually have a brain_url (mode in
            # brain/direct), since --brain is meaningless for cloud slots.
            candidates = [
                (k, _i) for k, _i in instances.items()
                if _i.get("brain_url") and (
                    needle in k.lower()
                    or needle in str(_i.get("name", "")).lower()
                    or needle in str(_i.get("device_name", "")).lower()
                )
            ]
            if not candidates:
                console.print(f"[red]No brain instance matches '{brain_arg}'. Pass a URL or run /instances to see saved names.[/red]")
                sys.exit(1)
            match = candidates[0][1]
            brain_arg = match["brain_url"]
            resolved_token = resolved_token or match.get("token", "")
            saved_model = match.get("model", "") or ""
        # Priority: explicit --model flag → saved instance's model → first
        # chat model in /api/tags. Previously we skipped step 2, which meant
        # `pw-agent --brain wsl` ended up with an empty model whenever
        # Ollama only had nomic-embed-text loaded (embed-filter stripped it).
        model = args.model or saved_model or ""
        if not model:
            try:
                hdrs = {"Authorization": f"Bearer {resolved_token}"} if resolved_token else {}
                resp = requests.get(f"{brain_arg}/api/tags", headers=hdrs, timeout=5)
                models = _filter_chat_models([m["name"] for m in resp.json().get("models", [])])
                if models:
                    model = models[0]
            except Exception:
                pass
        client = LLMClient(brain_url=brain_arg, model=model, token=resolved_token)
        console.print(f"  [dim]Mode: Direct brain ({brain_arg})[/dim]")
    elif args.token:
        client = LLMClient(token=args.token, model=args.model or "", api_url=args.api_url)
        console.print(f"  [dim]Mode: PastaWater cloud (CLI token)[/dim]")
    else:
        # --instance N flag to pick a specific instance
        # 0 = local (first brain/direct instance, matches /use 0 semantics)
        # 1..N = cloud slot N
        if args.instance is not None:
            instances = cfg.get("instances", {})
            inst = None
            if args.instance == 0:
                # Find first local (brain/direct) instance, same as /use 0
                for k, candidate in instances.items():
                    if candidate.get("mode") in ("brain", "direct"):
                        inst = candidate
                        break
                if not inst:
                    console.print("[red]Instance 0 (local) not configured. Use /connect to add one.[/red]")
                    sys.exit(1)
            else:
                # Cloud slot N — find by slot number
                for k, candidate in instances.items():
                    if candidate.get("mode") == "cloud" and candidate.get("slot") == args.instance:
                        inst = candidate
                        break
                if not inst:
                    console.print(f"[red]Instance {args.instance} (cloud slot {args.instance}) not found.[/red]")
                    sys.exit(1)
        else:
            inst = get_active_instance(cfg)

        if not inst:
            console.print("[red]No connection configured. Run: pw-agent --setup[/red]")
            sys.exit(1)
        client = build_client_from_instance(inst)
        if not client:
            console.print("[red]Invalid instance config. Run: pw-agent --setup[/red]")
            sys.exit(1)
        mode_label = inst.get("name", inst.get("mode", "unknown"))
        if not quiet:
            console.print(f"  [dim]Instance: {mode_label}[/dim]")

    # ─── Verify PW token is valid ────────────────────────────────────
    # Prefer client.token (covers --brain by-name resolution where we filled in
    # the saved instance's token), then fall back to inst's token, then CLI arg.
    token_to_check = client.token or (inst.get("token", "") if not args.brain else "") or (args.token or "")
    if not token_to_check:
        console.print("[red]PastaWater account required. Run: pw-agent --setup[/red]")
        sys.exit(1)
    try:
        vresp = requests.get(
            "https://pastawater.io/api/user/byog/slots",
            headers={"Authorization": f"Bearer {token_to_check}"},
            timeout=10,
        )
        if vresp.status_code == 401:
            console.print("[red]Token expired or revoked. Run: pw-agent --setup[/red]")
            sys.exit(1)
    except Exception:
        pass  # Offline — allow if token exists, will fail on actual API call

    # ─── Test connection + re-detect model ──────────────────────────
    if not quiet:
        console.print("  [dim]Connecting...[/dim]")

    # For brain mode, re-detect what model is actually available
    if client.direct_mode:
        try:
            resp = requests.get(
                f"{client.brain_url}/api/tags",
                headers={"Authorization": f"Bearer {client.token}"} if client.token else {},
                timeout=5,
            )
            if resp.status_code == 200:
                available = _filter_chat_models([m["name"] for m in resp.json().get("models", [])])
                if available and client.model not in available:
                    old = client.model
                    client.model = available[0]
                    if not quiet:
                        console.print(f"  [yellow]Model changed: {old} → {client.model}[/yellow]")
                    # Update saved config
                    inst = get_active_instance(cfg)
                    if inst:
                        inst["model"] = client.model
                        inst["name"] = f"Local ({client.model})"
                        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
        except Exception:
            pass

    ok, msg = client.test_connection()
    if ok:
        if not quiet:
            console.print(f"  [green]✓ {msg}[/green]")
    else:
        console.print(f"  [yellow]⚠ {msg}[/yellow]")
        # Try other instances instead of exiting
        other_instances = {k: v for k, v in cfg.get("instances", {}).items() if k != cfg.get("active")}
        connected = False
        for name, other_inst in other_instances.items():
            other_client = build_client_from_instance(other_inst)
            if other_client:
                other_ok, other_msg = other_client.test_connection()
                if other_ok:
                    console.print(f"  [green]✓ Switched to {name}: {other_msg}[/green]")
                    client = other_client
                    inst = other_inst
                    cfg["active"] = name
                    save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                    connected = True
                    break
        if not connected:
            console.print("  [dim]No instances available. Use /connect or /instances to configure.[/dim]")
            if quiet:
                sys.exit(1)

    cwd = os.getcwd()
    if not quiet:
        console.print(f"  [dim]Working directory: {cwd}[/dim]")

    # ─── Auto-refresh model on startup ────────────────────────────────
    # Local/brain instances can get stale if the model was changed via
    # the dashboard. Auto-detect the running model on connect. Runs even
    # in quiet/one-shot mode — otherwise pw-agent sends /api/chat with
    # the stale config model name and forces Ollama to swap away from
    # whatever the user actually loaded.
    if client:
        try:
            if client.direct_mode:
                # Detect actual running model: /status → /api/ps → /api/tags.
                # /status (set by brain's set_ollama_model) is the AUTHORITATIVE
                # "which chat model is active" value. /api/ps just lists what
                # happens to be in VRAM and its order is unstable — multiple
                # chat models can coexist (gemma + qwen) so we can't assume
                # models[0] is "the" active one.
                running_model = None
                ctrl_headers = dict(client.session.headers)
                if client.token:
                    ctrl_headers["X-Controller-API-Key"] = client.token

                # 1. /api/ps — what's ACTUALLY in VRAM right now. Ground
                # truth. Don't trust /status's llm_current_model — it's the
                # brain's last tracked set_ollama_model call which goes
                # stale when the user loads a model another way.
                ps_chat_models = []
                try:
                    ps_resp = client.session.get(f"{client.brain_url}/api/ps", timeout=5)
                    if ps_resp.status_code == 200:
                        ps_chat_models = [m for m in ps_resp.json().get("models", []) if not _is_embed_model(m.get("name", ""))]
                        if len(ps_chat_models) == 1:
                            running_model = ps_chat_models[0].get("name")
                except Exception:
                    pass

                # 2. /status — only used to disambiguate when /api/ps shows
                # multiple chat models loaded (which one is "active"?).
                if not running_model and len(ps_chat_models) > 1:
                    try:
                        sr = client.session.get(f"{client.brain_url}/status", headers=ctrl_headers, timeout=5)
                        if sr.status_code == 200:
                            llm_model = sr.json().get("llm_current_model")
                            if llm_model and not _is_embed_model(llm_model):
                                # Only trust /status if it points to a model that's actually loaded
                                if any(m.get("name") == llm_model for m in ps_chat_models):
                                    running_model = llm_model
                    except Exception:
                        pass
                    # Still nothing matched? Just pick first /api/ps entry
                    if not running_model and ps_chat_models:
                        running_model = ps_chat_models[0].get("name")

                # 3. /api/tags — every pulled model (last resort)
                if not running_model:
                    try:
                        resp = client.session.get(f"{client.brain_url}/api/tags", timeout=5)
                        if resp.status_code == 200:
                            models = _filter_chat_models([m["name"] for m in resp.json().get("models", [])])
                            if models:
                                running_model = models[0]
                    except Exception:
                        pass
                if running_model and client.model != running_model:
                    old = client.model
                    client.model = running_model
                    inst = get_active_instance(cfg)
                    if inst:
                        inst["model"] = client.model
                        inst["name"] = f"Local ({client.model})"
                        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                    if not quiet:
                        console.print(f"  [dim]Model synced: {old} → {client.model}[/dim]")
            else:
                # Cloud mode — bulk-refresh all saved cloud instances
                updated = refresh_all_instances(cfg, client)
                if updated:
                    # Re-read our own model after refresh
                    inst = get_active_instance(cfg)
                    if inst and inst.get("model") != client.model:
                        client.model = inst["model"]
        except Exception:
            pass  # Best-effort — don't block startup

    # ─── Model quality warning ────────────────────────────────────────
    warning = get_model_warning(client.model)
    if warning and not quiet:
        console.print(f"  [yellow]{warning}[/yellow]")

    # ─── Auto-approve mode ────────────────────────────────────────────
    if args.yes:
        import tools as _tools
        _tools.AUTO_APPROVE = True
        if not quiet:
            console.print("  [bold red]⚠ Auto-approve mode — agent can modify files without asking[/bold red]")

    # ─── Resolve thinking default ─────────────────────────────────────
    # ON by default for thinking-capable models; OFF if --no-think flag
    # or if the model doesn't support it anyway. Ctrl+T flips at runtime.
    from agent import model_supports_thinking
    thinking_default = model_supports_thinking(client.model) and not args.no_think

    # ─── Status bar info ──────────────────────────────────────────────
    status = {"engine_text": "", "hardware_text": "", "mode_text": "", "flag_text": ""}
    # Create temp agent to refresh status
    temp_agent = Agent(client, plan_mode=False, thinking=thinking_default, big_ctx=args.big_ctx, max_iterations=args.max_iterations)
    refresh_status(status, client, cfg, args, temp_agent)

    # Startup hint for thinking-capable models
    if not quiet and model_supports_thinking(client.model):
        if thinking_default:
            console.print("  [dim]🧠 Thinking ON — /think or Ctrl+T to toggle, --no-think to disable at launch[/dim]")
        else:
            console.print("  [dim]🧠 Thinking OFF (via --no-think) — /think or Ctrl+T to re-enable[/dim]")

    # ─── Initialize MemPalace memory (project + global tiers) ────────
    mem_store = None
    global_mem = None
    try:
        from memory import MemoryStore
        # Use the brain URL for Ollama embeddings (direct mode) or localhost
        ollama_url = client.brain_url if client.direct_mode else "http://localhost:11434"
        mem_auth = getattr(client, "token", "") or ""
        mem_store = MemoryStore(cwd, ollama_url=ollama_url, scope="project", auth_token=mem_auth)
        global_mem = MemoryStore(cwd, ollama_url=ollama_url, scope="global", auth_token=mem_auth)
        if not quiet:
            parts = []
            if mem_store.size > 0:
                parts.append(f"{mem_store.size} project memories")
            if global_mem.size > 0:
                parts.append(f"{global_mem.size} global facts")
            if parts:
                console.print(f"  [dim]📚 Loaded {', '.join(parts)}[/dim]")
            # Passive growth warning — nothing auto-cleans, but nudge the
            # user when the store gets big so they can /memory clean or prune.
            warn = mem_store.growth_warning()
            if warn:
                console.print(f"  [yellow]⚠  {warn}[/yellow]")
    except Exception:
        pass  # Memory is optional — works without it

    session_id = getattr(args, "session_id", None) or ""
    num_ctx_override = getattr(args, "num_ctx", None)

    # ─── One-shot mode (-p "prompt") ──────────────────────────────────
    if args.one_shot:
        output_format = getattr(args, "output_format", "text")
        # Stream chunks to stdout when --stream (text) or when stream-json
        # (always — the NDJSON event schema is only useful streaming).
        # Plain --output-format json still buffers to a single object.
        stream_tokens = (bool(args.stream) and output_format == "text") or output_format == "stream-json"
        agent = Agent(client, stream=stream_tokens, status_text=temp_agent.status_text, thinking=thinking_default, quiet=True, memory_store=mem_store, output_format=output_format, big_ctx=args.big_ctx, max_iterations=args.max_iterations, session_id=session_id, num_ctx_override=num_ctx_override)
        agent.global_memory = global_mem
        # Auto-resume when --session-id or -c is given. Dispatchers (e.g.
        # CallByte) call pw-agent -p "<turn>" repeatedly; passing the same
        # --session-id each time gives the model full prior-turn memory
        # without the dispatcher re-pasting the entire transcript.
        if session_id or args.resume:
            from config import load_session as _load_session
            prev = _load_session(cwd, session_id=session_id)
            if prev:
                agent.load_session(prev)
        agent.run(args.one_shot)
        # Add a trailing newline after streamed text so the next shell
        # prompt doesn't glue onto the model's last token. stream-json
        # already ends every event with \n so no extra needed there.
        if stream_tokens and output_format == "text":
            try:
                sys.stdout.write("\n")
                sys.stdout.flush()
            except Exception:
                pass
        return

    # ─── Resume previous session ──────────────────────────────────────
    agent = Agent(client, stream=not args.no_stream, status_text=temp_agent.status_text, thinking=thinking_default, memory_store=mem_store, big_ctx=args.big_ctx, max_iterations=args.max_iterations, session_id=session_id, num_ctx_override=num_ctx_override)
    agent.global_memory = global_mem

    # Clean up the fleet heartbeat file on exit
    if agent.fleet:
        import atexit
        atexit.register(agent.fleet.cleanup)

    # ─── Start MCP servers (background) ───────────────────────────────
    if agent.mcp:
        try:
            results = agent.mcp.start_all()
            if results and not quiet:
                ok_count = sum(1 for ok, _ in results.values() if ok)
                if ok_count > 0:
                    tool_count = sum(len(c.tools) for c in agent.mcp.clients.values())
                    console.print(f"  [dim]🔌 MCP: {ok_count}/{len(results)} server(s), {tool_count} tool(s) loaded[/dim]")
                for name, (ok, msg) in results.items():
                    if not ok:
                        console.print(f"  [yellow]MCP {name}: {msg}[/yellow]")
        except Exception as e:
            if not quiet:
                console.print(f"  [dim]MCP startup skipped: {e}[/dim]")
    from config import load_session
    prev = load_session(cwd, session_id=session_id)

    if args.resume or session_id:
        if prev:
            agent.load_session(prev)
            console.print(f"  [green]✓ Resumed session ({len(agent.conversation)} messages)[/green]")
        else:
            console.print("  [yellow]⚠ No previous session found to resume. Starting fresh.[/yellow]")
    elif prev:
        console.print("  [dim]Found a previous session. Run with [bold]-c[/bold] to resume.[/dim]")

    console.print(HELP_TEXT)

    history_file = os.path.join(cfg.get("config_dir", DEFAULT_CONFIG_DIR), "history")
    os.makedirs(os.path.dirname(history_file), exist_ok=True)

    def _bottom_toolbar():
        import shutil
        width = shutil.get_terminal_size().columns
        border = "━" * width
        
        fragments = [
            # Line 1: Top Border
            ('fg:#475569', border + '\n'),
            # Line 2: Metrics
            ('', '  '), 
            ('fg:#22D3EE bold', status["engine_text"]),
            ('fg:#475569', '    │    '), 
            ('fg:#4ADE80 bold', status["hardware_text"]),
            ('fg:#475569', '    │    '), 
            ('fg:#FBBF24 bold', status["mode_text"]),
        ]
        
        if status["flag_text"]:
            fragments.append(('fg:#475569', '    │    '))
            fragments.append(('fg:#C084FC bold', status["flag_text"]))

        # Thinking toggle (only shown for thinking-capable models).
        # Thinking defaults ON; users can flip it off to test non-thinking
        # output (subject to Ollama bugs for some models). Badge reflects
        # current runtime state, not the model's capability.
        from agent import model_supports_thinking
        if model_supports_thinking(client.model):
            fragments.append(('fg:#475569', '    │    '))
            if agent.thinking:
                fragments.append(('fg:#E879F9 bold', '🧠 Think: ON'))
            else:
                fragments.append(('fg:#64748B', '🧠 Think: OFF'))
            fragments.append(('fg:#475569', '    │    '))
            fragments.append(('fg:#64748B', 'Ctrl+T: toggle'))

        fragments.append(('', '\n'))
        # Line 3: Bottom padding
        fragments.append(('', ' '))

        return FormattedText(fragments)

    # Key bindings — Ctrl+T toggles thinking at runtime for models that
    # reason (qwen3.5, qwen3.6, gemma4). No-op + message for non-thinking
    # models since there's nothing to toggle.
    kb = _key_bindings()

    @kb.add("c-t")
    def _toggle_thinking(event):
        from agent import model_supports_thinking
        if model_supports_thinking(client.model):
            agent.thinking = not agent.thinking
            refresh_status(status, client, cfg, args, agent)
            event.app.invalidate()

    session = PromptSession(
        history=FileHistory(history_file),
        auto_suggest=AutoSuggestFromHistory(),
        completer=PwCompleter(),
        complete_while_typing=False,
        key_bindings=kb,
        bottom_toolbar=_bottom_toolbar,
    )

    while True:
        try:
            # Pre-fill with typeahead text if user typed during generation
            prefill = agent.typeahead or ""
            agent.typeahead = ""
            user_input = session.prompt(
                [("class:prompt", "❯ ")],
                style=_prompt_style(),
                default=prefill,
            ).strip()
        except KeyboardInterrupt:
            if agent.conversation:
                console.print("\n  [dim]Press Ctrl+C again to exit. Saving session...[/dim]")
                try:
                    agent._auto_save()
                except KeyboardInterrupt:
                    console.print("  [dim]Save interrupted, exiting.[/dim]")
                    sys.exit(0)
                try:
                    session.prompt(
                        [("class:prompt", "❯ ")],
                        style=_prompt_style(),
                    )
                    # User typed something instead of Ctrl+C — continue
                    continue
                except (KeyboardInterrupt, EOFError):
                    console.print("  [dim]Session saved. Bye![/dim]")
                    break
            else:
                console.print("\n[dim]Bye![/dim]")
                break
        except EOFError:
            if agent.conversation:
                agent._auto_save()
                console.print("\n  [dim]Session saved. Bye![/dim]")
            else:
                console.print("\n[dim]Bye![/dim]")
            break

        if not user_input:
            continue

        while user_input.endswith("\\"):
            try:
                cont = session.prompt([("class:continuation", "… ")], style=_prompt_style())
                user_input = user_input[:-1] + "\n" + cont
            except (KeyboardInterrupt, EOFError):
                break

        # @file shorthand → /add file
        if user_input.startswith("@") and not user_input.startswith("@@"):
            filepath = user_input[1:].strip()
            if filepath:
                agent.add_file(filepath)
            continue

        if user_input.startswith("/"):
            parts = user_input.split(maxsplit=1)
            cmd = parts[0].lower()
            cmd_arg = parts[1].strip() if len(parts) > 1 else ""

            if cmd in ("/plan", "/p"):
                agent.plan_mode = True
                refresh_status(status, client, cfg, args, agent)
                console.print("  [bold cyan]Mode switched to PLAN (read-only analysis)[/bold cyan]")
                continue

            if cmd in ("/build", "/b"):
                agent.plan_mode = False
                refresh_status(status, client, cfg, args, agent)
                console.print("  [bold green]Mode switched to BUILD (full read/write access)[/bold green]")
                continue

            if cmd in ("/think", "/t"):
                from agent import model_supports_thinking
                if not model_supports_thinking(client.model):
                    console.print(f"  [yellow]{client.model} doesn't have built-in reasoning — nothing to toggle[/yellow]")
                else:
                    agent.thinking = not agent.thinking
                    if agent.thinking:
                        console.print("  [bold magenta]🧠 Thinking ON — model will reason before answering[/bold magenta]")
                    else:
                        console.print("  [dim]🧠 Thinking OFF — expect possible empty responses on Qwen3.x (Ollama bug #14793)[/dim]")
                    refresh_status(status, client, cfg, args, agent)
                continue

            if cmd == "/rag":
                arg = (cmd_arg or "").strip().lower()
                if arg in ("off", "disable"):
                    agent.rag_enabled = False
                    console.print("  [yellow]Codebase RAG OFF — no automatic code chunk injection[/yellow]")
                elif arg in ("on", "enable"):
                    agent.rag_enabled = True
                    console.print("  [green]Codebase RAG ON[/green]")
                else:
                    state = "ON" if agent.rag_enabled else "OFF"
                    console.print(f"  Codebase RAG: [bold]{state}[/bold]  ([dim]/rag on|off[/dim])")
                continue

            if cmd in ("/ctx", "/context"):
                from agent import _get_context_limit
                agent.big_ctx = not agent.big_ctx
                limit = _get_context_limit(client.model, big_ctx=agent.big_ctx)
                if agent.big_ctx:
                    console.print(f"  [bold yellow]Big context ON[/bold yellow] — requesting {limit:,} tokens (Ollama may offload to CPU → slower)")
                else:
                    console.print(f"  [dim]Big context OFF — using safe {limit:,} tokens (fits fully in VRAM)[/dim]")
                refresh_status(status, client, cfg, args, agent)
                continue

            if cmd == "/thinking":
                if not agent.last_thinking:
                    console.print("  [dim]No thinking to show yet[/dim]")
                else:
                    lines = agent.last_thinking.split("\n")
                    console.print(f"\n  [dim]🧠 Reasoning ({len(lines)} lines):[/dim]")
                    for line in lines:
                        if line.strip():
                            console.print(f"  [dim]│ {line[:120]}[/dim]")
                    console.print(f"  [dim]└─────[/dim]\n")
                continue

            if cmd == "/fleet":
                from fleet import list_fleet, format_fleet
                with console.status("[cyan]Querying fleet (local + broker)...", spinner="dots"):
                    states = list_fleet(client=client)
                console.print(f"\n[#afafff]{format_fleet(states, client=client)}[/#afafff]\n")
                continue

            if cmd == "/train":
                # LoRA training prep — extract dataset + emit recipe
                from lora_prep import write_training_assets, status
                sub = cmd_arg.split()[0].lower() if cmd_arg else "prep"

                if sub in ("status", "info"):
                    meta = status(cwd)
                    if not meta:
                        console.print("  [dim]No training assets yet. Run /train prep to create them.[/dim]")
                    else:
                        from datetime import datetime
                        created = datetime.fromtimestamp(meta.get("created_at", 0)).strftime("%Y-%m-%d %H:%M")
                        console.print(f"\n  [bold cyan]🎓 Training assets[/bold cyan]")
                        console.print(f"  [dim]  Output: {meta.get('out_dir', '?')}[/dim]")
                        console.print(f"  [dim]  Created: {created}[/dim]")
                        console.print(f"  [dim]  Base model: {meta.get('base_model', '?')}[/dim]")
                        console.print(f"  [dim]  Train pairs: {meta.get('train_pairs', 0)}[/dim]")
                        console.print(f"  [dim]  Eval pairs: {meta.get('eval_pairs', 0)}[/dim]\n")
                elif sub in ("prep", "extract", "build"):
                    console.print(f"  [dim]Walking project + extracting function/class chunks...[/dim]")
                    try:
                        with console.status("[cyan]Extracting training data...", spinner="dots"):
                            stats = write_training_assets(cwd)
                        console.print(f"  [green]✓ Built training dataset[/green] [dim]({stats['chunks']} chunks → {stats['train']} train + {stats['eval']} eval)[/dim]")
                        console.print(f"  [dim]  Output dir: {stats['out_dir']}[/dim]")
                        console.print(f"  [dim]  Recipe: {stats['recipe_path']}[/dim]")
                        console.print(f"  [dim]  Run /train recipe to view the next steps.[/dim]")
                    except Exception as e:
                        console.print(f"  [red]Prep failed: {e}[/red]")
                elif sub == "recipe":
                    meta = status(cwd)
                    if not meta:
                        console.print("  [yellow]No training assets yet. Run /train prep first.[/yellow]")
                    else:
                        recipe_path = os.path.join(meta["out_dir"], "recipe.md")
                        if os.path.exists(recipe_path):
                            with open(recipe_path, "r") as f:
                                content = f.read()
                            console.print(f"\n[#afafff]{content}[/#afafff]\n")
                        else:
                            console.print(f"  [red]Recipe file missing: {recipe_path}[/red]")
                else:
                    console.print(f"  [yellow]Unknown /train subcommand: {sub}[/yellow]")
                    console.print("  [dim]Available: prep, status, recipe[/dim]")
                continue

            if cmd == "/remember":
                # Add a fact to the global cross-project memory
                if not cmd_arg:
                    console.print("  [yellow]Usage: /remember <fact about you, your role, or how you want to work>[/yellow]")
                    continue
                if not agent.global_memory:
                    console.print("  [red]Global memory not available[/red]")
                    continue
                ok = agent.global_memory.add(cmd_arg, source="user", tags=["profile"])
                if ok:
                    console.print(f"  [green]✓ Saved to global memory[/green] [dim]({agent.global_memory.size} facts total)[/dim]")
                else:
                    console.print(f"  [dim]Already remembered.[/dim]")
                continue

            if cmd == "/profile":
                # Show what we remember about the user globally
                if not agent.global_memory or agent.global_memory.size == 0:
                    console.print("  [dim]No global facts yet. Use /remember to add some.[/dim]")
                    console.print("  [dim]Examples:[/dim]")
                    console.print("  [dim]  /remember I prefer concise responses[/dim]")
                    console.print("  [dim]  /remember I'm a senior Go engineer[/dim]")
                    console.print("  [dim]  /remember Always run tests before committing[/dim]")
                    continue
                console.print(f"\n  [bold cyan]🪪 User profile ({agent.global_memory.size} facts)[/bold cyan]")
                for u in agent.global_memory.units:
                    preview = u.content[:120].replace("\n", " ")
                    console.print(f"  [dim]  • {preview}[/dim]")
                console.print()
                continue

            if cmd == "/forget-me":
                # Wipe the global profile
                if not agent.global_memory:
                    continue
                size = agent.global_memory.size
                # Wipe by removing files and re-creating empty
                import shutil
                if os.path.exists(agent.global_memory.store_path):
                    shutil.rmtree(agent.global_memory.store_path)
                from memory import MemoryStore
                ollama_url = client.brain_url if client.direct_mode else "http://localhost:11434"
                agent.global_memory = MemoryStore(cwd, ollama_url=ollama_url, scope="global", auth_token=(getattr(client, 'token', '') or ''))
                console.print(f"  [dim]Cleared global profile ({size} facts removed)[/dim]")
                continue

            if cmd == "/voice":
                # Toggle continuous voice mode (auto-speak final answers)
                arg = cmd_arg.strip().lower() if cmd_arg else ""
                if arg in ("on", "true", "1", "yes"):
                    agent.voice_mode = True
                elif arg in ("off", "false", "0", "no"):
                    agent.voice_mode = False
                else:
                    agent.voice_mode = not agent.voice_mode
                from voice import get_playback_command
                player = get_playback_command()
                if agent.voice_mode:
                    if not player:
                        console.print("  [yellow]⚠ No audio player found. Install ffplay/mpv/aplay/afplay.[/yellow]")
                        agent.voice_mode = False
                    else:
                        console.print(f"  [bold green]🔊 Voice mode ON[/bold green] [dim](player: {player[0]})[/dim]")
                        console.print("  [dim]Every assistant response will be spoken via fleet TTS.[/dim]")
                else:
                    console.print("  [dim]🔇 Voice mode OFF[/dim]")
                continue

            if cmd == "/say":
                # One-off TTS
                if not cmd_arg:
                    console.print("  [yellow]Usage: /say <text>[/yellow]")
                    continue
                from voice import speak_text
                console.print(f"  [dim]🔊 Speaking...[/dim]")
                result = speak_text(cmd_arg, client)
                if result.startswith("Error:"):
                    console.print(f"  [red]{result}[/red]")
                else:
                    console.print(f"  [dim]{result}[/dim]")
                continue

            if cmd == "/index":
                # Index (or reindex) the project codebase
                if not agent.codebase:
                    console.print("  [red]Codebase index not available[/red]")
                    continue
                force = cmd_arg.strip() in ("force", "-f", "--force", "rebuild")
                # Tell the user where embeddings will run
                if agent.codebase._use_cloud_embed():
                    console.print(f"  [dim]Indexing project files via fleet (broker → active brain Ollama)...[/dim]")
                else:
                    console.print(f"  [dim]Indexing project files via local Ollama...[/dim]")
                try:
                    with console.status("[cyan]Walking files + embedding chunks...", spinner="dots"):
                        stats = agent.codebase.index(force=force)
                    console.print(f"  [green]✓ Indexed {stats['files_indexed']} files[/green] [dim]({stats['chunks_added']} new chunks, {stats['chunks_skipped']} skipped, total {agent.codebase.size})[/dim]")
                    if stats["errors"] > 0:
                        console.print(f"  [yellow]{stats['errors']} chunks failed to embed[/yellow]")
                        if stats.get("last_error"):
                            console.print(f"  [dim]  reason: {stats['last_error']}[/dim]")
                        if not agent.codebase._use_cloud_embed():
                            console.print(f"  [dim]  hint: pull nomic-embed-text on your Ollama (ollama pull nomic-embed-text)[/dim]")
                except Exception as e:
                    console.print(f"  [red]Index failed: {e}[/red]")
                continue

            if cmd == "/forget":
                # Wipe the codebase index for this project
                if not agent.codebase:
                    console.print("  [red]Codebase index not available[/red]")
                    continue
                size = agent.codebase.size
                agent.codebase.clear()
                console.print(f"  [dim]Cleared codebase index ({size} chunks removed)[/dim]")
                continue

            if cmd == "/mcp":
                if not agent.mcp:
                    console.print("  [dim]MCP not initialized.[/dim]")
                    continue
                # Subcommands: list (default), add, remove, reload
                sub_parts = cmd_arg.split(maxsplit=2) if cmd_arg else []
                sub_cmd = sub_parts[0] if sub_parts else "list"

                if sub_cmd in ("", "list", "ls"):
                    cfg_mcp = agent.mcp.load_config()
                    servers = cfg_mcp.get("servers", {})
                    if not servers:
                        console.print("\n  [dim]No MCP servers configured.[/dim]")
                        console.print("  [dim]Add one: /mcp add <name> <command> [args...][/dim]")
                        console.print(f"  [dim]Config: {agent.mcp.config_path}[/dim]\n")
                    else:
                        console.print(f"\n  [bold cyan]🔌 {len(servers)} MCP server(s) configured[/bold cyan]")
                        for name, srv in servers.items():
                            running = "[green]●[/green]" if name in agent.mcp.clients else "[dim]○[/dim]"
                            tools_count = len(agent.mcp.clients[name].tools) if name in agent.mcp.clients else 0
                            cmd_str = f"{srv.get('command', '')} {' '.join(srv.get('args', []))}".strip()
                            console.print(f"  {running} [cyan]{name}[/cyan] [dim]({tools_count} tools)[/dim]")
                            console.print(f"      [dim]{cmd_str}[/dim]")
                        console.print()
                elif sub_cmd == "add":
                    if len(sub_parts) < 3:
                        console.print("  [yellow]Usage: /mcp add <name> <command> [args...][/yellow]")
                        console.print("  [dim]Example: /mcp add filesystem npx -y @modelcontextprotocol/server-filesystem /tmp[/dim]")
                    else:
                        name = sub_parts[1]
                        rest_parts = sub_parts[2].split()
                        srv_cmd = rest_parts[0]
                        srv_args = rest_parts[1:]
                        agent.mcp.add_server(name, srv_cmd, srv_args)
                        console.print(f"  [green]✓ Added MCP server: {name}[/green]")
                        console.print(f"  [dim]Restart pw-agent or run /mcp reload to start it[/dim]")
                elif sub_cmd in ("remove", "rm", "delete"):
                    if len(sub_parts) < 2:
                        console.print("  [yellow]Usage: /mcp remove <name>[/yellow]")
                    else:
                        name = sub_parts[1]
                        if agent.mcp.remove_server(name):
                            if name in agent.mcp.clients:
                                agent.mcp.clients[name].stop()
                                del agent.mcp.clients[name]
                                agent._mcp_tools_cache = []
                            console.print(f"  [dim]Removed MCP server: {name}[/dim]")
                        else:
                            console.print(f"  [red]No such MCP server: {name}[/red]")
                elif sub_cmd == "reload":
                    agent.mcp.stop_all()
                    results = agent.mcp.start_all()
                    agent._mcp_tools_cache = []
                    ok_count = sum(1 for ok, _ in results.values() if ok)
                    console.print(f"  [green]✓ Reloaded MCP — {ok_count}/{len(results)} server(s)[/green]")
                    for name, (ok, msg) in results.items():
                        if not ok:
                            console.print(f"  [yellow]{name}: {msg}[/yellow]")
                elif sub_cmd == "tools":
                    tools = agent.mcp.list_tools()
                    if not tools:
                        console.print("  [dim]No MCP tools loaded.[/dim]")
                    else:
                        console.print(f"\n  [bold cyan]🔌 {len(tools)} MCP tool(s) available[/bold cyan]")
                        for t in tools:
                            console.print(f"  [cyan]{t['name']}[/cyan]")
                            desc = t.get("description", "")[:100]
                            console.print(f"    [dim]{desc}[/dim]")
                        console.print()
                else:
                    console.print(f"  [yellow]Unknown /mcp subcommand: {sub_cmd}[/yellow]")
                    console.print("  [dim]Available: list, add, remove, reload, tools[/dim]")
                continue

            if cmd == "/hooks":
                from hooks import list_hooks, EVENTS, DEFAULT_HOOKS_DIR, HOOKS_CONFIG_FILE
                cfg_hooks = list_hooks()
                total = sum(len(v) for v in cfg_hooks.values())
                if total == 0:
                    console.print(f"\n  [dim]No hooks configured.[/dim]")
                    console.print(f"  [dim]Drop executable scripts in {DEFAULT_HOOKS_DIR}/<event_name>[/dim]")
                    console.print(f"  [dim]Or list them in {HOOKS_CONFIG_FILE}[/dim]")
                    console.print(f"  [dim]Events: {', '.join(EVENTS)}[/dim]\n")
                else:
                    console.print(f"\n  [bold cyan]🪝 {total} hook(s) configured[/bold cyan]")
                    for ev, paths in cfg_hooks.items():
                        if paths:
                            console.print(f"  [cyan]{ev}[/cyan]")
                            for p in paths:
                                console.print(f"    [dim]→ {p}[/dim]")
                    console.print()
                continue

            if cmd == "/skills":
                if not agent.skills:
                    console.print("  [dim]No skills loaded.[/dim]")
                    console.print("  [dim]Add skills to ~/.pw-agent/skills/<name>/SKILL.md[/dim]")
                else:
                    console.print(f"\n  [bold cyan]🎯 {len(agent.skills)} skill(s) available[/bold cyan]")
                    for s in agent.skills:
                        loaded = " [green]●[/green]" if s.id in agent.loaded_skill_ids else ""
                        desc = s.description if len(s.description) <= 80 else s.description[:77] + "..."
                        console.print(f"  [cyan]{s.name}[/cyan]{loaded}  [dim]{desc}[/dim]")
                    console.print(f"  [dim]Use /skill <name> to load a skill manually.[/dim]\n")
                continue

            if cmd == "/skill":
                if not cmd_arg:
                    console.print("  [yellow]Usage: /skill <name>[/yellow]")
                    continue
                from skills import get_skill_by_name
                skill = get_skill_by_name(cmd_arg, agent.skills)
                if not skill:
                    console.print(f"  [red]Skill not found: {cmd_arg}[/red]")
                    console.print("  [dim]Run /skills to see what's available.[/dim]")
                else:
                    if skill.id in agent.loaded_skill_ids:
                        console.print(f"  [dim]Skill '{skill.name}' already loaded this session.[/dim]")
                    agent.loaded_skill_ids.add(skill.id)
                    body = skill.body[:6000]
                    agent.conversation.append({
                        "role": "tool_result",
                        "content": f"[Skill manually loaded: {skill.name}]\n\n{body}",
                    })
                    console.print(f"  [green]✓ Loaded skill: {skill.name}[/green] [dim]({len(body)} chars)[/dim]")
                continue

            if cmd == "/stats":
                if not getattr(agent, "turn_stats", None):
                    console.print("  [dim]No turns recorded yet. Send a message first.[/dim]")
                    continue
                s = agent.turn_stats[-1]
                total = s["total_tokens"] or 1
                def pct(x): return f"{100*x/total:.0f}%"
                console.print()
                console.print(f"  [bold cyan]📊 Last turn — {total:,} tokens[/bold cyan]  [dim]model={s['model']}  slim={'yes' if s['use_slim'] else 'no'}[/dim]")
                console.print(f"    System prompt    : {s['system_core_tokens']:>6,}  ({pct(s['system_core_tokens'])})  [dim]MCP tools={s['mcp_tool_count']}[/dim]")
                console.print(f"    Retrieved memory : {s['memory_ctx_tokens']:>6,}  ({pct(s['memory_ctx_tokens'])})  [dim]{s['mem_hits']} hits, avg sim {s['mem_avg_sim']}[/dim]")
                console.print(f"    Retrieved code   : {s['codebase_ctx_tokens']:>6,}  ({pct(s['codebase_ctx_tokens'])})  [dim]{s['code_hits']} hits, avg sim {s['code_avg_sim']}[/dim]")
                console.print(f"    History          : {s['history_tokens']:>6,}  ({pct(s['history_tokens'])})  [dim]{s['truncated']} msgs truncated[/dim]")
                if s.get("duplicate_calls"):
                    console.print(f"    [yellow]Duplicate tool calls caught: {s['duplicate_calls']}[/yellow]")
                console.print(f"  [dim]Type /waste to see specific fixes[/dim]")
                console.print()
                continue

            if cmd == "/waste":
                if not getattr(agent, "turn_stats", None):
                    console.print("  [dim]No turns recorded yet — /waste needs at least one conversation turn.[/dim]")
                    continue
                stats = agent.turn_stats
                last = stats[-1]
                findings = []

                # 1) Low-similarity retrieved memory — bloat without benefit
                if last["mem_hits"] >= 3 and last["mem_avg_sim"] < 0.6 and last["memory_ctx_tokens"] > 400:
                    findings.append((
                        "Low-quality memory retrieval",
                        f"{last['mem_hits']} memory units injected at avg sim {last['mem_avg_sim']:.2f} — mostly noise costing {last['memory_ctx_tokens']} tokens.",
                        "Bump MIN_SIMILARITY in memory.py to 0.65 or run /memory prune."
                    ))

                # 2) Low-similarity retrieved code
                if last["code_hits"] >= 3 and last["code_avg_sim"] < 0.6 and last["codebase_ctx_tokens"] > 600:
                    findings.append((
                        "Low-quality code retrieval",
                        f"{last['code_hits']} chunks injected at avg sim {last['code_avg_sim']:.2f} — costing {last['codebase_ctx_tokens']} tokens.",
                        "Raise MIN_SIMILARITY_AUTO in codebase_index.py to 0.65 or use /refresh on the index."
                    ))

                # 3) Fat system prompt relative to a small-context model
                # Rough assumption: small models have 8-16K safe context
                if last["system_core_tokens"] > 3500:
                    findings.append((
                        "Heavy system prompt",
                        f"System prompt is {last['system_core_tokens']} tokens before any retrieval. MCP tools={last['mcp_tool_count']}.",
                        "Disable MCP servers you don't need via /mcp. Small models choke past ~3K system tokens."
                    ))

                # 4) Duplicate tool calls caught (recent turns)
                dup_total = sum(t.get("duplicate_calls", 0) for t in stats[-5:])
                if dup_total >= 2:
                    findings.append((
                        "Model is looping on tools",
                        f"{dup_total} duplicate tool calls caught across the last {min(5, len(stats))} turns.",
                        f"Try a larger chat model. {last['model']} may be too small for this task."
                    ))

                # 5) Heavy truncation suggests long session, time to summarize
                trunc_total = sum(t.get("truncated", 0) for t in stats[-5:])
                if trunc_total >= 8:
                    findings.append((
                        "Frequent history truncation",
                        f"{trunc_total} messages dropped from history in the last {min(5, len(stats))} turns.",
                        "Session is running long — /clear to start fresh, or /memory curate to lock in what you learned first."
                    ))

                # 6) Code context added but model seems small
                if last["codebase_ctx_tokens"] > 2000 and "4b" in last["model"].lower():
                    findings.append((
                        "Big code context on small model",
                        f"Injected {last['codebase_ctx_tokens']} code tokens into a 4B model — likely won't reason over all of it.",
                        f"Run /use with a larger model (qwen3-coder:30b, gemma4:26b) when code chunks matter."
                    ))

                console.print()
                if not findings:
                    console.print("  [green]✓ No waste detected in the last turn.[/green]")
                else:
                    console.print(f"  [bold yellow]⚠ {len(findings)} waste patterns detected[/bold yellow]")
                    for title, body, fix in findings:
                        console.print(f"\n  [yellow]• {title}[/yellow]")
                        console.print(f"    [dim]{body}[/dim]")
                        console.print(f"    [cyan]→ {fix}[/cyan]")
                console.print()
                continue

            if cmd == "/memory":
                sub_parts = cmd_arg.split(maxsplit=1) if cmd_arg else []
                sub = (sub_parts[0].lower() if sub_parts else "")
                sub_arg = (sub_parts[1] if len(sub_parts) > 1 else "")

                # Quick toggles — work even if no memory store is loaded
                if sub in ("off", "disable"):
                    agent.memory_enabled = False
                    console.print("  [yellow]Memory auto-inject OFF — saved facts won't be added to prompts[/yellow]")
                    continue
                if sub in ("on", "enable"):
                    agent.memory_enabled = True
                    console.print("  [green]Memory auto-inject ON[/green]")
                    continue
                if sub == "status":
                    state = "ON" if agent.memory_enabled else "OFF"
                    size = agent.memory.size if agent.memory else 0
                    console.print(f"  Memory auto-inject: [bold]{state}[/bold] · {size} stored units")
                    continue

                if not agent.memory:
                    console.print("  [dim]Memory not available[/dim]")
                    continue

                if sub == "prune":
                    # Wipe entire store. Backup first so it's recoverable.
                    import shutil
                    if agent.memory.size == 0:
                        console.print("  [dim]Already empty[/dim]")
                        continue
                    backup_dir = f"{agent.memory.store_path}.backup-{int(time.time())}"
                    try:
                        shutil.copytree(agent.memory.store_path, backup_dir)
                    except Exception as e:
                        console.print(f"  [red]Backup failed: {e}[/red]")
                        continue
                    for fname in ("units.json", "vectors.npy", "index.json"):
                        fpath = os.path.join(agent.memory.store_path, fname)
                        if os.path.exists(fpath):
                            os.remove(fpath)
                    agent.memory.units = []
                    agent.memory.vectors = None
                    console.print(f"  [green]✓ Pruned all memories[/green]")
                    console.print(f"  [dim]Backup: {backup_dir}[/dim]")
                    continue

                if sub == "clean":
                    # Drop units older than N days (default 30). Keeps vectors
                    # aligned with units so retrieval stays consistent.
                    try:
                        days = int(sub_arg) if sub_arg else 30
                    except ValueError:
                        console.print("  [yellow]Usage: /memory clean [days]  (default 30)[/yellow]")
                        continue
                    if agent.memory.size == 0:
                        console.print("  [dim]Nothing to clean[/dim]")
                        continue
                    cutoff = time.time() - days * 86400
                    keep_idx = [i for i, u in enumerate(agent.memory.units) if u.timestamp >= cutoff]
                    dropped = agent.memory.size - len(keep_idx)
                    if dropped == 0:
                        console.print(f"  [dim]No memories older than {days} days[/dim]")
                        continue
                    agent.memory.units = [agent.memory.units[i] for i in keep_idx]
                    if agent.memory.vectors is not None and len(agent.memory.vectors) == len(keep_idx) + dropped:
                        import numpy as _np
                        agent.memory.vectors = agent.memory.vectors[keep_idx]
                    agent.memory._save()
                    console.print(f"  [green]✓ Dropped {dropped} memories older than {days}d[/green] [dim]({agent.memory.size} remaining)[/dim]")
                    continue

                if sub == "size":
                    s = agent.memory.size_summary()
                    mb = s["disk_bytes"] / (1024 * 1024)
                    console.print(f"  [bold]{s['units']}[/bold] memories · [bold]{mb:.1f} MB[/bold] on disk · oldest [bold]{s['age_days']}d[/bold] ago")
                    warn = agent.memory.growth_warning()
                    if warn:
                        console.print(f"  [yellow]⚠ {warn}[/yellow]")
                    continue

                if sub == "recall":
                    # Show what would be injected for a query
                    if not sub_arg:
                        console.print("  [yellow]Usage: /memory recall <query>[/yellow]")
                        continue
                    hits = agent.memory.retrieve(sub_arg, top_k=8)
                    if not hits:
                        console.print(f"  [dim]No hits above similarity threshold for: {sub_arg}[/dim]")
                        continue
                    console.print(f"\n  [bold cyan]🔍 {len(hits)} retrieval hits for: {sub_arg}[/bold cyan]")
                    for u, score in hits:
                        preview = u.content[:120].replace("\n", " ")
                        console.print(f"  [dim][{score:.3f}][/dim] [bold]{u.source}[/bold]  {preview}")
                    console.print()
                    continue

                if sub == "forget":
                    # Remove a specific unit by id prefix
                    if not sub_arg:
                        console.print("  [yellow]Usage: /memory forget <id-prefix>[/yellow]")
                        continue
                    needle = sub_arg.strip().lower()
                    matches = [(i, u) for i, u in enumerate(agent.memory.units) if u.id.lower().startswith(needle)]
                    if not matches:
                        console.print(f"  [yellow]No unit id starts with '{needle}'[/yellow]")
                        continue
                    if len(matches) > 1:
                        console.print(f"  [yellow]Ambiguous — {len(matches)} matches:[/yellow]")
                        for _, u in matches:
                            console.print(f"  [dim]  {u.id}  {u.content[:80]}[/dim]")
                        continue
                    idx, unit = matches[0]
                    import numpy as _np
                    agent.memory.units.pop(idx)
                    if agent.memory.vectors is not None and len(agent.memory.vectors) > idx:
                        agent.memory.vectors = _np.delete(agent.memory.vectors, idx, axis=0)
                    agent.memory._save()
                    console.print(f"  [green]✓ Forgot[/green] [{unit.source}] {unit.content[:80]}")
                    continue

                if sub == "reembed":
                    # Re-generate vectors for all units (useful when units were
                    # stored before the embed model was available)
                    if agent.memory.size == 0:
                        console.print("  [dim]Nothing to re-embed[/dim]")
                        continue
                    console.print(f"  [dim]Re-embedding {agent.memory.size} units...[/dim]")
                    contents = [u.content for u in agent.memory.units]
                    vecs = agent.memory._embed(contents)
                    if vecs is None:
                        console.print("  [red]Embed model unavailable — start Ollama and pull nomic-embed-text first[/red]")
                        continue
                    agent.memory.vectors = vecs
                    agent.memory._embed_dim = vecs.shape[1]
                    agent.memory._save()
                    console.print(f"  [green]✓ Re-embedded {len(vecs)} units (dim={vecs.shape[1]}, model={agent.memory._embed_model})[/green]")
                    continue

                if sub == "curate":
                    # Trigger session-end extraction on the current conversation now
                    if not agent.conversation:
                        console.print("  [dim]Nothing to curate — conversation is empty[/dim]")
                        continue
                    console.print("  [dim]Extracting durable facts...[/dim]")
                    try:
                        from memory import extract_durable_memories
                        facts = extract_durable_memories(agent.conversation, agent.client)
                        if not facts:
                            console.print("  [dim]No durable facts found in this session[/dim]")
                            continue
                        console.print(f"  [green]✓ Extracted {len(facts)} candidates[/green]")
                        for f in facts:
                            console.print(f"  [dim]  [{f['source']}] {f['content'][:100]}[/dim]")
                        counts = agent.memory.dedup_and_store(facts, client=agent.client)
                        parts = [f"{v} {k}" for k, v in counts.items() if v]
                        console.print(f"  [green]→ {', '.join(parts) if parts else 'no changes'}[/green]")
                    except Exception as e:
                        console.print(f"  [red]Curation failed: {e}[/red]")
                    continue

                if sub in ("help", "?"):
                    console.print("\n  [bold]/memory commands:[/bold]")
                    console.print("    [cyan]/memory[/cyan]                  — list recent units")
                    console.print("    [cyan]/memory recall <query>[/cyan]   — show what retrieval would inject")
                    console.print("    [cyan]/memory curate[/cyan]           — extract facts from current session now")
                    console.print("    [cyan]/memory reembed[/cyan]          — re-generate vectors for stored units")
                    console.print("    [cyan]/memory size[/cyan]             — show stored unit count + disk usage")
                    console.print("    [cyan]/memory clean [days][/cyan]     — drop units older than N days (default 30)")
                    console.print("    [cyan]/memory forget <id>[/cyan]      — remove a specific unit")
                    console.print("    [cyan]/memory prune[/cyan]            — wipe entire store (backup created)")
                    console.print()
                    continue

                # Default: list units
                if agent.memory.size == 0:
                    console.print("  [dim]No memories stored yet — run a session and they'll be extracted at the end[/dim]")
                    continue

                console.print(f"\n  [bold cyan]📚 MemPalace — {agent.memory.size} knowledge units[/bold cyan]")
                console.print(f"  [dim]Store: {agent.memory.store_path}[/dim]")
                recent = sorted(agent.memory.units, key=lambda u: u.timestamp, reverse=True)[:15]
                for u in recent:
                    age = int(time.time() - u.timestamp)
                    if age < 60: age_str = f"{age}s"
                    elif age < 3600: age_str = f"{age // 60}m"
                    elif age < 86400: age_str = f"{age // 3600}h"
                    else: age_str = f"{age // 86400}d"
                    preview = u.content[:90].replace("\n", " ")
                    console.print(f"  [dim]{u.id}[/dim] [bold]{u.source:<13}[/bold] {preview} [dim]({age_str})[/dim]")
                if agent.memory.size > 15:
                    console.print(f"  [dim]  ... and {agent.memory.size - 15} more — /memory recall <query> to search[/dim]")
                console.print()
                continue

            if cmd in ("/quit", "/exit", "/q"):
                console.print("[dim]Bye![/dim]")
                break
            elif cmd == "/help":
                console.print(HELP_TEXT)
            elif cmd == "/clear":
                agent.reset()
            elif cmd == "/add":
                if cmd_arg:
                    agent.add_file(cmd_arg)
                else:
                    console.print("  [yellow]Usage: /add <filepath>[/yellow]")
            elif cmd == "/diff":
                import subprocess
                result = subprocess.run(["git", "diff"], capture_output=True, text=True, timeout=10)
                if result.stdout.strip():
                    console.print(f"\n{result.stdout[:3000]}")
                else:
                    console.print("  [dim]No unstaged changes.[/dim]")
            elif cmd == "/commit":
                # Ask the LLM to generate a commit message from the diff
                import subprocess
                diff = subprocess.run(["git", "diff", "--staged"], capture_output=True, text=True, timeout=10)
                if not diff.stdout.strip():
                    diff = subprocess.run(["git", "diff"], capture_output=True, text=True, timeout=10)
                if not diff.stdout.strip():
                    console.print("  [dim]No changes to commit.[/dim]")
                else:
                    agent.run(f"Generate a concise git commit message for this diff, then run `git add -A && git commit -m \"<message>\"`. Here's the diff:\n\n```\n{diff.stdout[:3000]}\n```")
            elif cmd in ("/models", "/gpus", "/slots", "/model"):
                print_models(client)
            elif cmd == "/instances":
                instances = cfg.get("instances", {})
                if not instances:
                    console.print("  [dim]No saved instances.[/dim]")
                else:
                    active_key = cfg.get("active", "")
                    console.print()
                    local_idx = 0
                    for k, inst in _ordered_instances(instances):
                        is_local = inst.get("mode") in ("brain", "direct")
                        num = _instance_display_number(inst, local_idx if is_local else 0)
                        if is_local:
                            local_idx += 1
                        marker = " [green]◀ active[/green]" if k == active_key else ""
                        mode = "[cyan]local[/cyan]" if is_local else f"[indigo]slot {inst.get('slot', '?')}[/indigo]"
                        # Cloud instances: always prefer device_name over 'name' field —
                        # 'name' can be stale (e.g., "Local (...)") from older configs.
                        if is_local:
                            display_name = inst.get("name", k)
                        else:
                            display_name = inst.get("device_name") or inst.get("name", k)
                        console.print(f"  [bold]{num}[/bold] — {display_name}  {mode}  [dim]{inst.get('model', '')}[/dim]{marker}")
                    console.print()
            elif cmd == "/connect":
                result = add_connection(cfg)
                if result:
                    cfg = result[0]
                    save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                    # Switch to the new instance
                    inst = result[2]
                    new_client = build_client_from_instance(inst)
                    if new_client:
                        client = new_client
                        agent.client = client
                        # Auto-refresh to get latest model
                        do_refresh(client, cfg, status, args, agent, silent=True)
                        console.print(f"  [green]✓ Switched to: {inst.get('name', '')}[/green]")
            elif cmd == "/use":
                if not cmd_arg:
                    console.print("  [yellow]Usage: /use <number>  (0=local, 1-5=cloud slot)[/yellow]")
                    continue

                instances = cfg.get("instances", {})
                arg = cmd_arg.strip().lower()

                # /use 0 or /use local → switch to local brain
                if arg in ("0", "local"):
                    local_key = None
                    for k, inst in instances.items():
                        if inst.get("mode") in ("brain", "direct"):
                            local_key = k
                            break
                    if not local_key:
                        console.print("  [red]No local instance configured. Use /connect to add one.[/red]")
                    else:
                        cfg["active"] = local_key
                        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                        inst = instances[local_key]
                        new_client = build_client_from_instance(inst)
                        if new_client:
                            client = new_client
                            agent.client = client
                            do_refresh(client, cfg, status, args, agent, silent=True)
                            console.print(f"  [green]✓ Switched to local: {inst.get('name', local_key)}[/green]")
                    continue

                # /use N → switch to cloud slot N (matches GPU Setup page)
                try:
                    target_slot = int(arg)
                except ValueError:
                    console.print("  [yellow]Usage: /use <number>  (0=local, 1-5=cloud slot)[/yellow]")
                    continue

                # Look for a saved cloud instance with this slot number
                cloud_key = None
                for k, inst in instances.items():
                    if inst.get("mode") not in ("brain", "direct") and inst.get("slot") == target_slot:
                        cloud_key = k
                        break

                if cloud_key:
                    # Saved instance found — switch to it
                    cfg["active"] = cloud_key
                    save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                    inst = instances[cloud_key]
                    new_client = build_client_from_instance(inst)
                    if new_client:
                        client = new_client
                        agent.client = client
                        do_refresh(client, cfg, status, args, agent, silent=True)
                        console.print(f"  [green]✓ Switched to slot {target_slot}: {inst.get('name', cloud_key)}[/green]")
                elif not client.direct_mode:
                    # Not saved but maybe live on the fleet — try direct slot switch
                    devices = client.list_devices()
                    target = next((d for d in devices if d["slot"] == target_slot), None)
                    if not target:
                        console.print(f"  [red]Slot {target_slot} not found or has no LLM running.[/red]")
                    else:
                        client.slot = target_slot
                        client.device_id = target["device_id"]
                        client.model = target["llm_model"]
                        do_refresh(client, cfg, status, args, agent, silent=True)
                        console.print(f"  [green]✓ Switched to slot {target_slot}: {target['llm_model']} on {target['gpu']}[/green]")
                else:
                    console.print(f"  [red]Slot {target_slot} not found. Run /instances to see available.[/red]")
            elif cmd == "/disconnect":
                instances = cfg.get("instances", {})
                if not cmd_arg:
                    console.print("  [yellow]Usage: /disconnect <number>  (0=local, N=cloud slot)[/yellow]")
                else:
                    # Use same numbering as /use: 0=local, N=slot N
                    arg = cmd_arg.strip().lower()
                    key = None
                    if arg in ("0", "local"):
                        for k, inst in instances.items():
                            if inst.get("mode") in ("brain", "direct"):
                                key = k
                                break
                    else:
                        try:
                            slot = int(arg)
                            for k, inst in instances.items():
                                if inst.get("mode") not in ("brain", "direct") and inst.get("slot") == slot:
                                    key = k
                                    break
                        except ValueError:
                            pass
                    if not key:
                        console.print(f"  [red]Instance not found: {cmd_arg}[/red]")
                        continue
                    try:
                        name = instances[key].get("name", key)
                        cfg = remove_instance(cfg, key)
                        save_config(cfg, cfg.get("config_dir", DEFAULT_CONFIG_DIR))
                        console.print(f"  [dim]Removed: {name}[/dim]")
                        
                        # Re-sync if active changed
                        inst = get_active_instance(cfg)
                        if inst:
                            new_client = build_client_from_instance(inst)
                            if new_client:
                                client = new_client
                                agent.client = client
                                refresh_status(status, client, cfg, args, agent)
                                console.print(f"  [dim]Switched to: {inst.get('name', '')}[/dim]")
                    except (ValueError, IndexError):
                        console.print(f"  [red]Invalid instance number. Run /instances to see list.[/red]")
            elif cmd == "/refresh":
                with console.status("[cyan]Refreshing fleet model info...", spinner="dots"):
                    # 1. Update ALL saved cloud instances in the background
                    updated = refresh_all_instances(cfg, client)
                    if updated:
                        console.print(f"  [green]✓ Updated {updated} saved instance(s)[/green]")
                    
                    # 2. Deep refresh current active client
                    do_refresh(client, cfg, status, args, agent)
            elif cmd == "/update":
                if do_update():
                    console.print("[dim]Bye![/dim]")
                    break
            elif cmd == "/config":
                active = get_active_instance(cfg)
                console.print(f"\n  [cyan]Active:[/cyan] {cfg.get('active', 'none')}")
                console.print(f"  [cyan]Mode:[/cyan] {active.get('mode', 'none')}")
                console.print(f"  [cyan]Model:[/cyan] {active.get('model', 'none')}")
                console.print(f"  [cyan]Instances:[/cyan] {len(cfg.get('instances', {}))}")
                console.print()
            elif cmd == "/logout":
                from config import _config_path
                path = _config_path(cfg.get("config_dir", ""))
                if os.path.exists(path):
                    os.remove(path)
                    console.print("  [dim]Config cleared. Run pw-agent --setup to reconfigure.[/dim]")
                else:
                    console.print("  [dim]No config found.[/dim]")
            else:
                console.print(f"  [yellow]Unknown command: {cmd}[/yellow]")
            continue

        agent.run(user_input)
        console.print()


class PwCompleter(Completer):
    """Tab-completes slash commands and file paths after /add or @."""

    COMMANDS = [
        ("/help", "Show help"),
        ("/add", "Add file to context"),
        ("/plan", "Switch to Plan mode (read-only)"),
        ("/build", "Switch to Build mode (read/write)"),
        ("/think", "Toggle thinking mode (Ctrl+T)"),
        ("/thinking", "Show last reasoning block"),
        ("/ctx", "Toggle big-context mode (native ctx, CPU offload)"),
        ("/rag", "Toggle codebase RAG auto-inject (/rag off to save context)"),
        ("/memory off", "Disable memory auto-inject for this session"),
        ("/memory", "MemPalace ops (list/recall/curate/forget/prune)"),
        ("/skills", "List loaded skills"),
        ("/skill", "Load a skill by name"),
        ("/index", "Index codebase for semantic search"),
        ("/forget", "Clear codebase index"),
        ("/voice", "Toggle voice mode (auto-speak responses)"),
        ("/say", "One-off TTS via fleet"),
        ("/remember", "Save fact to global cross-project profile"),
        ("/profile", "Show your global user profile"),
        ("/forget-me", "Wipe the global profile"),
        ("/train", "LoRA training prep (prep/status/recipe)"),
        ("/fleet", "List sibling pw-agent instances"),
        ("/hooks", "List configured shell hooks"),
        ("/mcp", "Manage MCP servers"),
        ("/clear", "Clear conversation"),
        ("/commit", "Git commit with AI message"),
        ("/diff", "Show git diff"),
        ("/models", "Show fleet GPUs"),
        ("/instances", "List saved connections"),
        ("/connect", "Add new connection"),
        ("/use", "Switch instance (0=local, N=slot)"),
        ("/disconnect", "Remove instance (0=local, N=slot)"),
        ("/refresh", "Re-detect model"),
        ("/update", "Update to latest version"),
        ("/config", "Show config"),
        ("/logout", "Clear saved config"),
        ("/quit", "Exit"),
    ]

    def __init__(self):
        self._path_completer = PathCompleter(expanduser=True)

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        # Slash command completion
        if text.startswith("/"):
            for cmd, desc in self.COMMANDS:
                if cmd.startswith(text):
                    yield Completion(cmd, start_position=-len(text), display_meta=desc)

            # File path after /add
            if text.startswith("/add "):
                sub_doc = document.__class__(text[5:], cursor_position=len(text) - 5)
                for c in self._path_completer.get_completions(sub_doc, complete_event):
                    yield c

            # Instance number after /use: 0=local, 1-5=cloud slot
            if text.startswith("/use "):
                partial = text[5:]
                # 0 = local
                if "0".startswith(partial) or "local".startswith(partial):
                    yield Completion("0", start_position=-len(partial), display_meta="Local GPU")
                if "local".startswith(partial):
                    yield Completion("local", start_position=-len(partial), display_meta="Local GPU")
                # 1-9 = cloud slot numbers
                for n in range(1, 10):
                    s = str(n)
                    if s.startswith(partial):
                        yield Completion(s, start_position=-len(partial), display_meta=f"Slot {n}")
            return

        # @file path completion
        if text.startswith("@"):
            sub_doc = document.__class__(text[1:], cursor_position=len(text) - 1)
            for c in self._path_completer.get_completions(sub_doc, complete_event):
                yield c


def _key_bindings():
    """Custom key bindings — Tab accepts auto-suggestion, Ctrl+C clears line."""
    kb = KeyBindings()

    @kb.add("tab")
    def _(event):
        buf = event.app.current_buffer
        suggestion = buf.suggestion
        if suggestion:
            buf.insert_text(suggestion.text)
        elif buf.complete_state:
            buf.complete_next()
        else:
            buf.start_completion()

    @kb.add("c-c")
    def _(event):
        """Ctrl+C: if text in buffer → clear it. If empty → raise KeyboardInterrupt (exit flow)."""
        buf = event.app.current_buffer
        if buf.text.strip():
            # Text present — clear the line (like Claude Code)
            buf.reset()
        else:
            # Empty buffer — let KeyboardInterrupt bubble up to the exit handler
            event.app.exit(exception=KeyboardInterrupt)

    return kb


def _prompt_style():
    from prompt_toolkit.styles import Style
    return Style.from_dict({
        "prompt": "ansibrightcyan bold",
        "continuation": "ansigray",
        "bottom-toolbar": "noreverse bg:default", # Stop inversion and allow transparency
    })


if __name__ == "__main__":
    main()
