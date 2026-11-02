"""HUD (hud.ai): set up once, then `--hud` records and grades robot rollouts there.

`dreamscale integrations hud setup` installs the hud CLI if needed, asks for a HUD
API key (opening the key page), verifies it, saves it with `hud set` for the hud
CLI and in ~/.dreamscale/config.toml, which `--hud` reads.
"""

from __future__ import annotations

import getpass
import os
import shutil
import subprocess
import sys
import webbrowser
from collections.abc import Callable
from typing import Any

import httpx

from dreamscale import errors
from dreamscale.config import load_config, save_config

NAME = "hud"
KEYS_URL = "https://hud.ai/project/api-keys"
API_KEY_ENV = "HUD_API_KEY"
SETUP_COMMAND = "dreamscale integrations hud setup"
# The hud CLI and its Python package support Python 3.11 and 3.12.
CLI_PYTHON = "3.12"


def _error(code, problem, cause, fix):
    return errors.DreamscaleError(errors.ErrorInfo(code, problem, cause, fix))


def saved_api_key() -> str | None:
    return load_config().integrations.get(NAME, {}).get("api_key") or None


def api_key() -> str | None:
    """HUD_API_KEY from the environment wins, as in the hud CLI; then the saved key."""
    return os.environ.get(API_KEY_ENV) or saved_api_key()


def verify_key(key: str, *, get: Callable[..., Any] = httpx.get) -> dict:
    """The key's HUD identity (name, team_name, ...), or an actionable error."""
    base = os.environ.get("HUD_API_URL", "https://api.hud.ai").rstrip("/")
    try:
        response = get(
            f"{base}/v2/auth/me", headers={"Authorization": f"Bearer {key}"}, timeout=15
        )
    except httpx.HTTPError as exc:
        raise _error(
            "hud_unreachable",
            "could not reach HUD to check the key",
            f"{type(exc).__name__}: {exc}",
            f"check this computer's network connection, then rerun `{SETUP_COMMAND}`",
        ) from exc
    if response.status_code in (401, 403):
        raise _error(
            "hud_key_rejected",
            "HUD rejected that API key",
            "it was mistyped, revoked, or belongs to another HUD environment",
            f"create a new key at {KEYS_URL} and rerun `{SETUP_COMMAND}`",
        )
    if response.status_code != 200:
        raise _error(
            "hud_unreachable",
            "HUD could not check the key",
            f"HUD answered HTTP {response.status_code}",
            f"rerun `{SETUP_COMMAND}` in a minute",
        )
    return response.json()


def hud_cli(
    *,
    print_fn: Callable[[str], None] = print,
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> list[str]:
    """The hud CLI's command, installing it with uv when it is missing."""
    found = which("hud")
    if found:
        return [found]
    uv = os.environ.get("UV") or which("uv")
    if uv is not None:
        command = [uv, "tool", "install", "hud", "--python", CLI_PYTHON]
        print_fn(f"Installing the hud CLI (one time): {' '.join(command)}")
        if run(command, check=False).returncode == 0:
            bin_dir = run(
                [uv, "tool", "dir", "--bin"], check=False, capture_output=True, text=True
            ).stdout.strip()
            # uv's tool bin directory may not be on PATH yet in this shell.
            fallback = os.path.join(bin_dir, "hud") if bin_dir else None
            installed = which("hud") or (
                fallback if fallback and os.path.exists(fallback) else None
            )
            if installed:
                print_fn("✓ hud CLI installed")
                return [installed]
    # The `hud` extra ships the same CLI inside Dreamscale's environment.
    print_fn("Using the hud CLI bundled with Dreamscale.")
    return [sys.executable, "-m", "hud.cli"]


def run_setup(
    *,
    api_key: str | None = None,
    print_fn: Callable[[str], None] = print,
    key_input_fn: Callable[[str], str] = getpass.getpass,
    open_browser: Callable[[str], bool] = webbrowser.open,
    get: Callable[..., Any] = httpx.get,
    which: Callable[[str], str | None] = shutil.which,
    run: Callable[..., subprocess.CompletedProcess] = subprocess.run,
) -> dict:
    """Connect this computer to HUD. Returns the key's HUD identity."""
    cli = hud_cli(print_fn=print_fn, which=which, run=run)
    current = saved_api_key()
    key = (api_key or "").strip()
    if not key:
        if current:
            key = key_input_fn(
                "HUD is already set up. Paste a new HUD API key, or press Enter to keep it: "
            ).strip() or current
        else:
            print_fn(f"Create a HUD API key: {KEYS_URL}")
            try:
                opened = open_browser(KEYS_URL)
            except Exception:
                opened = False
            print_fn("✓ opened your browser" if opened else "Open the URL above to continue.")
            key = key_input_fn("HUD API key: ").strip()
    key = key.strip("'\"")  # pasted with its quotes from a .env file
    if not key:
        raise _error(
            "hud_key_missing", "no HUD API key entered", "the prompt was left empty",
            f"create a key at {KEYS_URL} and paste it when asked",
        )
    identity = verify_key(key, get=get)
    who = identity.get("email") or identity.get("name") or "your account"
    team = identity.get("team_name")
    print_fn(f"✓ key verified: {who}" + (f" ({team})" if team else ""))
    result = run([*cli, "set", f"{API_KEY_ENV}={key}"], check=False, capture_output=True)
    if result.returncode != 0:
        raise _error(
            "hud_set_failed",
            "the hud CLI could not save the key",
            f"`hud set` exited with status {result.returncode}",
            f"run `hud set {API_KEY_ENV}=<key>` yourself, then rerun `{SETUP_COMMAND}`",
        )
    config = load_config()
    config.integrations[NAME] = {**config.integrations.get(NAME, {}), "api_key": key}
    save_config(config)
    print_fn("✓ HUD connected. Add --hud to record and grade a rollout:")
    print_fn("  dreamscale run yam --model molmoact2-bimanual-yam --hud")
    return identity
