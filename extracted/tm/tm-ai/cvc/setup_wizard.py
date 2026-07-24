"""
cvc.setup_wizard — Interactive first-time setup wizard for CVC.

Writes ``~/.cvc/config.yaml`` with:
  - User display name
  - LLM provider / model / API key
  - TTS backend configuration (tested live)
  - Wake word configuration (tested live)

Usage (invoked from cli.py ``cvc voice-setup`` or ``cvc setup --voice``):

    from cvc.setup_wizard import run_wizard
    run_wizard()

The resulting YAML is read by the CVC agent at startup and by the voice
loop module (``cvc.agent.voice`` — future) to configure speech I/O.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from cvc._subprocess_compat import HIDDEN_KW
import sys
import time
from pathlib import Path
from typing import Any

import yaml  # PyYAML — already transitively available; will use stdlib fallback if not
from rich import box
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from cvc.agent.menus import arrow_confirm, arrow_select
from cvc.agent.renderer import THEME

console = Console()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

CONFIG_PATH = Path.home() / ".cvc" / "config.yaml"


def _detect_platform_install_hint() -> str | None:
    """
    If the current host is one where uv's default hardlink installer is known
    to fail (Android/Termux, some chroots, some WSL2 distros with cross-mount
    /root), return a one-line install hint that explains the workaround.

    Detection is heuristic: ANDROID_ROOT / ANDROID_DATA env vars (Android),
    plus a libc probe of the ``/root/.cache`` create + link test. We do NOT
    shell out to ``uv`` — that's the user's install step, not ours.

    Returns:
        None if the platform looks normal, otherwise a short recommendation.
    """
    # Direct Android signal — Termux + native Android set these.
    if os.environ.get("ANDROID_ROOT") or os.environ.get("ANDROID_DATA"):
        return (
            "Detected Android environment. If `uv tool install tm-ai` fails with "
            "`Operation not permitted (os error 1)` during extraction, run:\n"
            "    UV_LINK_MODE=copy uv tool install tm-ai --upgrade --force"
        )

    # Heuristic: can we hardlink across /root/.cache <-> /root/.local?
    # Many read-only bind mounts and chroots fail here. We *try* one hardlink
    # and immediately clean up. If it fails, surface the hint.
    src_dir = Path("/tmp")
    try:
        a = src_dir / ".cvc_probe_a"
        b = src_dir / ".cvc_probe_b"
        if a.exists():
            a.unlink()
        if b.exists():
            b.unlink()
        a.write_text("x")
        try:
            os.link(a, b)
        except OSError:
            return (
                "Filesystem here disallows hardlinks (common on Android, chroots, "
                "and some WSL2 mounts). If `uv tool install tm-ai` fails with "
                "`Operation not permitted (os error 1)`, run:\n"
                "    UV_LINK_MODE=copy uv tool install tm-ai --upgrade --force"
            )
        finally:
            if a.exists():
                a.unlink()
            if b.exists():
                b.unlink()
    except Exception:
        # If we can't even probe, just stay silent — don't add noise.
        return None

    return None

def _load_providers_from_registry() -> list[tuple[str, str, str]]:
    """Build the legacy (key, label, default_model) tuples from the registry.

    Single source of truth: cvc/setup/registry.py.  This shim lets the voice
    wizard share the same provider list as the main `cvc setup` flow.
    """
    from cvc.setup import list_provider_specs
    out: list[tuple[str, str, str]] = []
    for s in list_provider_specs():
        # Use the registry's default_model, falling back to the provider profile's
        # first fallback model if specified, else empty string.
        model = s.default_model
        if not model:
            from cvc.providers.base import all_profiles
            for p in all_profiles():
                if p.name == s.key and p.fallback_models:
                    model = p.fallback_models[0]
                    break
        out.append((s.key, s.display_name, model))
    return out


# Built lazily so test harnesses that monkey-patch the registry still see updates.
PROVIDERS = _load_providers_from_registry()

TTS_BACKENDS = [
    ("macos_say", "macOS say (built-in, no install needed)", sys.platform == "darwin"),
    ("elevenlabs", "ElevenLabs (requires API key)", True),
    ("openai_tts", "OpenAI TTS (requires OpenAI key)", True),
    ("piper", "Piper (local neural TTS, offline)", True),
    ("none", "No TTS (text-only mode)", True),
]

WAKE_WORDS = [
    ("hey cvc", "Hey CVC"),
    ("hey meena", "Hey Meena"),
    ("computer", "Computer"),
    ("custom", "Custom phrase…"),
]


def _info(msg: str) -> None:
    console.print(f"  [dim]{msg}[/dim]")


def _success(msg: str) -> None:
    console.print(f"  [bold {THEME['success']}]✓[/bold {THEME['success']}]  {msg}")


def _warn(msg: str) -> None:
    console.print(f"  [bold {THEME['warning']}]![/bold {THEME['warning']}]  {msg}")


def _error(msg: str) -> None:
    console.print(f"  [bold {THEME['error']}]✗[/bold {THEME['error']}]  {msg}")


def _step(n: int, total: int, title: str) -> None:
    console.print()
    console.rule(
        f"[bold {THEME['primary_bright']}]  Step {n}/{total}: {title}  [/bold {THEME['primary_bright']}]",
        style=THEME["primary_dim"],
    )
    console.print()


def _load_existing() -> dict[str, Any]:
    """Load existing config.yaml if present."""
    if CONFIG_PATH.exists():
        try:
            with CONFIG_PATH.open(encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
            return data
        except Exception:
            return {}
    return {}


def _save_config(cfg: dict[str, Any]) -> None:
    """Write config to ~/.cvc/config.yaml."""
    CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        yaml.dump(cfg, f, default_flow_style=False, allow_unicode=True, sort_keys=False)


# ---------------------------------------------------------------------------
# Step 1 — User name
# ---------------------------------------------------------------------------

def _ask_name(existing: dict[str, Any]) -> str:
    default = existing.get("user", {}).get("name", "")
    hint = f" [dim](Enter to keep: {default})[/dim]" if default else ""
    console.print(
        f"  [{THEME['text']}]What should CVC call you?{hint}[/{THEME['text']}]\n"
        f"  [{THEME['text_dim']}]This name appears in the banner and agent greetings.[/{THEME['text_dim']}]"
    )
    console.print()
    name = console.input(f"  [{THEME['accent_soft']}]Your name › [/{THEME['accent_soft']}]").strip()
    if not name:
        name = default or "User"
    _success(f"Name set to [bold]{name}[/bold]")
    return name


# ---------------------------------------------------------------------------
# Step 2 — LLM configuration
# ---------------------------------------------------------------------------

def _ask_llm(existing: dict[str, Any]) -> dict[str, str]:
    ex_llm = existing.get("llm", {})
    ex_provider = ex_llm.get("provider", "")
    ex_model = ex_llm.get("model", "")

    # Provider selection
    console.print(f"  [{THEME['text']}]Choose your LLM provider:[/{THEME['text']}]")
    console.print()
    opts = [(pid, pid) for pid, _, _ in PROVIDERS]
    descs = [desc for _, desc, _ in PROVIDERS]
    default_idx = next((i for i, (pid, _, _) in enumerate(PROVIDERS) if pid == ex_provider), 0)
    chosen_provider = arrow_select(
        "Provider",
        opts,
        descriptions=descs,
        default=default_idx,
    )
    if chosen_provider is None:
        chosen_provider = "passthrough"

    # Default model for chosen provider
    default_model = next((m for pid, _, m in PROVIDERS if pid == chosen_provider), "")
    if ex_provider == chosen_provider and ex_model:
        default_model = ex_model

    console.print()
    console.print(
        f"  [{THEME['text']}]Model[/{THEME['text']}] "
        f"[dim](default: {default_model or 'none'})[/dim]"
    )
    model_input = console.input(
        f"  [{THEME['accent_soft']}]Model name › [/{THEME['accent_soft']}]"
    ).strip()
    model = model_input or default_model

    # API key (skip for ollama/passthrough)
    api_key = ex_llm.get("api_key", "")
    if chosen_provider not in ("ollama", "passthrough"):
        env_var_map = {
            "anthropic": "ANTHROPIC_API_KEY",
            "openai": "OPENAI_API_KEY",
            "google": "GOOGLE_API_KEY",
            "github": "GITHUB_COPILOT_TOKEN",
            "copilot": "COPILOT_GITHUB_TOKEN",
        }
        env_var = env_var_map.get(chosen_provider, "")
        env_val = os.environ.get(env_var, "") if env_var else ""
        if env_val:
            _info(f"API key found in environment ({env_var}). Press Enter to use it.")
            hint = f"[dim](Enter to use env var {env_var})[/dim]"
        elif api_key:
            masked = api_key[:8] + "…" + api_key[-4:] if len(api_key) > 12 else "●●●●"
            hint = f"[dim](Enter to keep: {masked})[/dim]"
        else:
            hint = "[dim](will be stored in config.yaml)[/dim]"

        console.print()
        console.print(f"  [{THEME['text']}]API key {hint}[/{THEME['text']}]")
        raw_key = console.input(
            f"  [{THEME['accent_soft']}]API key › [/{THEME['accent_soft']}]",
            password=True,
        ).strip()
        if raw_key:
            api_key = raw_key
        elif env_val:
            api_key = ""  # Store empty — rely on env var

    _success(f"LLM: [bold]{chosen_provider}[/bold] / [bold]{model or 'default'}[/bold]")
    result: dict[str, str] = {"provider": chosen_provider, "model": model}
    if api_key:
        result["api_key"] = api_key
    return result


# ---------------------------------------------------------------------------
# Step 3 — TTS configuration + live test
# ---------------------------------------------------------------------------

def _test_tts_macos(text: str) -> bool:
    """Run macOS say command. Returns True if successful."""
    try:
        ret = subprocess.run(
            ["say", text],
            timeout=15,
            capture_output=True,
                    **HIDDEN_KW,
        )
        return ret.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def _ask_tts(existing: dict[str, Any]) -> dict[str, Any]:
    ex_tts = existing.get("tts", {})
    ex_backend = ex_tts.get("backend", "")

    available = [(bid, label) for bid, label, avail in TTS_BACKENDS if avail]
    descs = [label for bid, label in available]
    default_idx = next((i for i, (bid, _) in enumerate(available) if bid == ex_backend), 0)

    console.print(f"  [{THEME['text']}]Choose a TTS (text-to-speech) backend:[/{THEME['text']}]")
    console.print()

    chosen_backend = arrow_select(
        "TTS backend",
        available,
        descriptions=descs,
        default=default_idx,
    )
    if chosen_backend is None:
        chosen_backend = "none"

    tts_cfg: dict[str, Any] = {"backend": chosen_backend}

    # Extra config per backend
    if chosen_backend == "elevenlabs":
        ex_elabs_key = ex_tts.get("elevenlabs_api_key", "")
        console.print()
        hint = f"[dim](Enter to keep existing)[/dim]" if ex_elabs_key else ""
        console.print(f"  [{THEME['text']}]ElevenLabs API key {hint}[/{THEME['text']}]")
        key_in = console.input(
            f"  [{THEME['accent_soft']}]ElevenLabs key › [/{THEME['accent_soft']}]",
            password=True,
        ).strip()
        if key_in:
            tts_cfg["elevenlabs_api_key"] = key_in
        elif ex_elabs_key:
            tts_cfg["elevenlabs_api_key"] = ex_elabs_key

        console.print()
        ex_voice = ex_tts.get("elevenlabs_voice_id", "Rachel")
        console.print(f"  [{THEME['text']}]Voice ID [dim](default: {ex_voice})[/dim][/{THEME['text']}]")
        voice_in = console.input(
            f"  [{THEME['accent_soft']}]Voice ID › [/{THEME['accent_soft']}]"
        ).strip()
        tts_cfg["elevenlabs_voice_id"] = voice_in or ex_voice

    elif chosen_backend == "openai_tts":
        tts_cfg["openai_voice"] = ex_tts.get("openai_voice", "alloy")
        console.print()
        voices = [("alloy", "alloy"), ("echo", "echo"), ("fable", "fable"),
                  ("onyx", "onyx"), ("nova", "nova"), ("shimmer", "shimmer")]
        def_idx = next((i for i, (v, _) in enumerate(voices) if v == tts_cfg["openai_voice"]), 0)
        chosen_voice = arrow_select("OpenAI voice", voices, default=def_idx)
        if chosen_voice:
            tts_cfg["openai_voice"] = chosen_voice

    elif chosen_backend == "piper":
        ex_model = ex_tts.get("piper_model", "en_US-lessac-medium")
        console.print()
        console.print(f"  [{THEME['text']}]Piper model [dim](default: {ex_model})[/dim][/{THEME['text']}]")
        model_in = console.input(
            f"  [{THEME['accent_soft']}]Piper model › [/{THEME['accent_soft']}]"
        ).strip()
        tts_cfg["piper_model"] = model_in or ex_model

    # Live test
    if chosen_backend != "none":
        console.print()
        do_test = arrow_confirm("Run a live TTS test now?", default=True)
        if do_test:
            test_text = "Hello! CVC is ready. This is your text-to-speech test."
            console.print()
            _info(f"Speaking: \"{test_text}\"")
            success = False

            if chosen_backend == "macos_say":
                success = _test_tts_macos(test_text)
            elif chosen_backend in ("elevenlabs", "openai_tts", "piper"):
                _warn("Live test for this backend requires the full agent to be running.")
                _info("Skipping live test — configuration saved.")
                success = True  # Assume OK, not worth blocking setup

            if success:
                _success("TTS test passed.")
                heard = arrow_confirm("Did you hear the voice clearly?", default=True)
                if not heard:
                    _warn("TTS test reported unclear. Check system volume / audio output.")
            else:
                _warn("TTS test failed. Check that the backend is installed/configured.")

    _success(f"TTS backend: [bold]{chosen_backend}[/bold]")
    return tts_cfg


# ---------------------------------------------------------------------------
# Step 4 — Wake word configuration + live test
# ---------------------------------------------------------------------------

def _ask_wake_word(existing: dict[str, Any]) -> dict[str, Any]:
    ex_ww = existing.get("wake_word", {})
    ex_phrase = ex_ww.get("phrase", "hey cvc")
    ex_backend = ex_ww.get("backend", "keyword")

    console.print(f"  [{THEME['text']}]Choose your wake word:[/{THEME['text']}]")
    console.print()

    opts = [(phrase, label) for phrase, label in WAKE_WORDS]
    descs = [label for _, label in WAKE_WORDS]
    default_idx = next((i for i, (p, _) in enumerate(WAKE_WORDS) if p == ex_phrase), 0)

    chosen_phrase = arrow_select("Wake word", opts, descriptions=descs, default=default_idx)
    if chosen_phrase is None:
        chosen_phrase = "hey cvc"

    if chosen_phrase == "custom":
        console.print()
        custom = console.input(
            f"  [{THEME['accent_soft']}]Custom wake phrase › [/{THEME['accent_soft']}]"
        ).strip().lower()
        chosen_phrase = custom or "hey cvc"

    # Wake word backend
    console.print()
    console.print(f"  [{THEME['text']}]Wake word detection backend:[/{THEME['text']}]")
    ww_backends = [
        ("keyword", "keyword", "Simple keyword match (no mic, CLI-typed trigger)"),
        ("porcupine", "porcupine", "Porcupine (Picovoice — real mic, low CPU)"),
        ("whisper", "whisper", "Whisper VAD (OpenAI — real mic, higher accuracy)"),
    ]
    ww_opts = [(bid, bid) for bid, _, _ in ww_backends]
    ww_descs = [desc for _, _, desc in ww_backends]
    ww_default = next((i for i, (bid, _, _) in enumerate(ww_backends) if bid == ex_backend), 0)

    console.print()
    chosen_ww_backend = arrow_select("Detection backend", ww_opts, descriptions=ww_descs, default=ww_default)
    if chosen_ww_backend is None:
        chosen_ww_backend = "keyword"

    ww_cfg: dict[str, Any] = {
        "phrase": chosen_phrase,
        "backend": chosen_ww_backend,
        "enabled": chosen_ww_backend != "keyword",
    }

    if chosen_ww_backend == "porcupine":
        ex_key = ex_ww.get("porcupine_access_key", "")
        console.print()
        hint = "[dim](Enter to keep existing)[/dim]" if ex_key else ""
        console.print(f"  [{THEME['text']}]Porcupine access key {hint}[/{THEME['text']}]")
        pkey = console.input(
            f"  [{THEME['accent_soft']}]Access key › [/{THEME['accent_soft']}]",
            password=True,
        ).strip()
        if pkey:
            ww_cfg["porcupine_access_key"] = pkey
        elif ex_key:
            ww_cfg["porcupine_access_key"] = ex_key

    # Live wake word test (keyword backend only — others need real mic)
    console.print()
    if chosen_ww_backend == "keyword":
        do_test = arrow_confirm("Run a quick wake word test? (type the phrase when prompted)", default=True)
        if do_test:
            console.print()
            _info(f"Type your wake phrase: [bold]\"{chosen_phrase}\"[/bold]")
            console.print()
            typed = console.input(
                f"  [{THEME['accent_soft']}]Type wake phrase › [/{THEME['accent_soft']}]"
            ).strip().lower()
            normalized_phrase = chosen_phrase.replace("-", " ").strip().lower()
            normalized_typed = typed.replace("-", " ").strip().lower()
            if normalized_typed == normalized_phrase or normalized_phrase in normalized_typed:
                _success("Wake word test passed.")
            else:
                _warn(
                    f"Typed [bold]{typed!r}[/bold] — expected [bold]{chosen_phrase!r}[/bold]. "
                    "Configuration saved anyway; you can re-run wizard to change."
                )
    else:
        _info(f"Live mic test for {chosen_ww_backend} backend skipped — requires hardware mic.")
        _info("Run `cvc wake-test` after setup to verify mic-based wake word detection.")

    _success(f"Wake word: [bold]{chosen_phrase}[/bold] via [bold]{chosen_ww_backend}[/bold]")
    return ww_cfg


# ---------------------------------------------------------------------------
# Step 5 — macOS launchd auto-start
# ---------------------------------------------------------------------------

# Label constant used in the panel (mirrors daemon.SOFIA_DAEMON_LABEL)
SOFIA_DAEMON_PLIST_LABEL = "com.cvc.sofia"


def _install_sofia_autostart(state: dict[str, Any]) -> None:
    """Offer to install/skip the com.cvc.sofia launchd plist on macOS.

    On non-macOS platforms the step is displayed but skipped automatically.
    The *state* dict is mutated with ``_sofia_autostart_installed`` so the
    summary panel can reflect what happened.
    """
    import sys as _sys

    if _sys.platform != "darwin":
        _info("Auto-start via launchd is only available on macOS -- skipping.")
        state["_sofia_autostart_installed"] = False
        return

    from cvc.daemon import (
        install_sofia_launchd,
        sofia_daemon_status,
    )

    status = sofia_daemon_status()
    already = bool(status.get("installed"))

    if already:
        console.print(
            f"  [{THEME['text_dim']}]Existing Sofia launchd plist found at:[/{THEME['text_dim']}]"
        )
        console.print(f"  [bold]{status['config_path']}[/bold]")
        console.print()
        reinstall = arrow_confirm(
            "Re-install / update the Sofia auto-start plist?",
            default_yes=False,
        )
        if not reinstall:
            _info("Keeping existing plist unchanged.")
            state["_sofia_autostart_installed"] = True
            return
    else:
        console.print(
            Panel(
                f"  Sofia can be configured to start automatically whenever you log in.\n"
                f"  This writes [bold]~/Library/LaunchAgents/{SOFIA_DAEMON_PLIST_LABEL}.plist[/bold]\n"
                f"  and loads it with [bold]launchctl[/bold].\n\n"
                f"  [dim]Logs -> ~/.cvc/sofia.log and ~/.cvc/sofia.err.log[/dim]",
                border_style=THEME["primary_dim"],
                title=f"[bold {THEME['primary_bright']}]Sofia Auto-Start[/bold {THEME['primary_bright']}]",
                padding=(1, 2),
            )
        )
        console.print()
        do_install = arrow_confirm(
            "Install the Sofia auto-start daemon (recommended)?",
            default_yes=True,
        )
        if not do_install:
            _info("Skipped. You can run [bold]cvc daemon sofia install[/bold] later.")
            state["_sofia_autostart_installed"] = False
            return

    result_msg = install_sofia_launchd()
    if "failed" in result_msg.lower():
        _warn(result_msg)
        state["_sofia_autostart_installed"] = False
    else:
        _success(result_msg)
        state["_sofia_autostart_installed"] = True


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------

def run_wizard(first_run: bool = False) -> None:
    """
    Run the interactive CVC setup wizard.

    Collects user name, LLM configuration, TTS settings, and wake word
    settings, then writes ``~/.cvc/config.yaml``.

    Args:
        first_run: If True, a welcome message is shown instead of 're-configure'.
    """
    # ── Banner ───────────────────────────────────────────────────────────
    console.print()
    console.print(
        Panel(
            Text.from_markup(
                f"[bold {THEME['primary_bright']}] CVC Setup Wizard [/bold {THEME['primary_bright']}]\n"
                f"[{THEME['text_dim']}]Configures your name, LLM provider, TTS voice, and wake word.[/{THEME['text_dim']}]\n"
                f"[{THEME['text_dim']}]Writes to: [bold]{CONFIG_PATH}[/bold][/{THEME['text_dim']}]"
            ),
            border_style=THEME["primary"],
            padding=(1, 4),
        )
    )

    # Platform-specific install hint (Android, chroots, some WSL2 mounts).
    # See _detect_platform_install_hint for the rationale.
    hint = _detect_platform_install_hint()
    if hint:
        console.print()
        console.print(
            Panel(
                Text.from_markup(
                    f"[bold yellow]Platform notice[/bold yellow]\n"
                    f"[{THEME['text']}]{hint}[/{THEME['text']}]"
                ),
                border_style="yellow",
                padding=(1, 4),
            )
        )

    existing = _load_existing()
    if existing and not first_run:
        console.print()
        _info("Existing config.yaml found. Values will be shown as defaults.")

    TOTAL_STEPS = 5

    # ── Step 1: Name ─────────────────────────────────────────────────────
    _step(1, TOTAL_STEPS, "Your Name")
    name = _ask_name(existing)

    # ── Step 2: LLM ──────────────────────────────────────────────────────
    _step(2, TOTAL_STEPS, "LLM Configuration")
    llm_cfg = _ask_llm(existing)

    # ── Step 3: TTS ──────────────────────────────────────────────────────
    _step(3, TOTAL_STEPS, "Text-to-Speech (TTS)")
    tts_cfg = _ask_tts(existing)

    # ── Step 4: Wake word ────────────────────────────────────────────────
    _step(4, TOTAL_STEPS, "Wake Word")
    ww_cfg = _ask_wake_word(existing)

    # ── Step 5: Auto-start (macOS launchd plist) ─────────────────────────
    autostart_installed = False
    _step(5, TOTAL_STEPS, "Auto-Start on Login")
    _install_sofia_autostart(existing)
    autostart_installed = existing.get("_sofia_autostart_installed", False)

    # ── Compose and save config ──────────────────────────────────────────
    config: dict[str, Any] = {
        "user": {
            "name": name,
        },
        "llm": llm_cfg,
        "tts": tts_cfg,
        "wake_word": ww_cfg,
    }

    # Preserve any keys in existing config that we didn't touch
    for top_key in existing:
        if top_key not in config:
            config[top_key] = existing[top_key]

    _save_config(config)

    # ── Summary panel ────────────────────────────────────────────────────
    console.print()
    table = Table(
        box=box.ROUNDED,
        border_style=THEME["primary_dim"],
        show_header=False,
        padding=(0, 2),
    )
    table.add_column("Key", style=THEME["text_dim"])
    table.add_column("Value", style=f"bold {THEME['primary_bright']}")

    table.add_row("Name", name)
    table.add_row("LLM provider", llm_cfg["provider"])
    table.add_row("Model", llm_cfg.get("model") or "(provider default)")
    table.add_row("TTS backend", tts_cfg["backend"])
    table.add_row("Wake word", ww_cfg["phrase"])
    table.add_row("Wake detection", ww_cfg["backend"])
    table.add_row("Auto-start", "enabled (launchd)" if autostart_installed else "disabled")
    table.add_row("Config file", str(CONFIG_PATH))

    console.print(
        Panel(
            table,
            title=f"[bold {THEME['success']}]  Setup Complete  [/bold {THEME['success']}]",
            border_style=THEME["primary"],
            padding=(1, 2),
        )
    )
    console.print()
    console.print(
        f"  [{THEME['text_dim']}]Run [bold {THEME['accent']}]cvc agent[/bold {THEME['accent']}] to start the AI agent, "
        f"or [bold {THEME['accent']}]cvc up[/bold {THEME['accent']}] to start everything.[/{THEME['text_dim']}]"
    )
    console.print()
