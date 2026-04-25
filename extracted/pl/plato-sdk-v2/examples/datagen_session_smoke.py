"""End-to-end smoke test for DatagenSession against a real sim.

Walks the full happy path:

    1. Launch DatagenSession on Chronos against ``aureus``
    2. ``send_message`` to ask the agent to insert some data
    3. Verify via ``call_tool("db", "select_context", ...)``
    4. Print the public sim URL
    5. Open Playwright, run ``session.login(...)`` to drop a logged-in
       browser context onto the sim
    6. Block on stdin so the user can poke around in the browser
    7. ``stop_conversation`` (so end-of-loop verifiers run if any) +
       ``close``

Usage::

    export PLATO_API_KEY=...
    export ANTHROPIC_API_KEY=...   # used by the agent inside the world
    cd python-sdk
    uv run --python 3.12 python examples/datagen_session_smoke.py

Optional env vars::

    PLATO_SIM=aureus               # sim to attach (default: aureus)
    PLATO_PROMPT="..."             # custom prompt to send (default below)
    PLATO_WORLD_PACKAGE=...        # pin a specific structured-execution
                                   # build (e.g. ``...:dev`` after `plato
                                   # world publish` from worlds/structured-execution)
    PLATO_ALLOW_PRERELEASE=1       # required when WORLD_PACKAGE is a
                                   # prerelease tag

If you've published a dev build of structured-execution to test these
changes end-to-end, set ``PLATO_WORLD_PACKAGE`` to that build's tag and
``PLATO_ALLOW_PRERELEASE=1``.
"""

from __future__ import annotations

import json
import logging
import os
import subprocess
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

from plato.v2 import DatagenSession, Env, Plato

_CLAUDE_KEYCHAIN_SERVICE = "Claude Code-credentials"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(name)s] %(levelname)s %(message)s",
)
logger = logging.getLogger("agent_smoke")


SIM = os.environ.get("PLATO_SIM", "aureus")
PROMPT = os.environ.get(
    "PLATO_PROMPT",
    # Default prompt assumes only vm + functions MCPs (no db). For DB
    # inserts, pass mcps_override or use Env.artifact() so build_launch_config
    # can fetch db_config.
    f"Use the vm tools to list containers running in the {SIM} env "
    "(call vm.get_containers), then pick one and run `hostname` and "
    "`whoami` inside it via vm.exec. Report the container name, hostname, "
    "and user in 2 short bullets.",
)


def _discover_claude_credentials() -> tuple[str, str] | None:
    """Find Claude credentials the same way ``plato pm`` does.

    Discovery order (matches ``python-sdk/plato/cli/pm.py:_get_claude_credentials``):

    1. macOS Keychain entry ``Claude Code-credentials`` (written by ``claude``
       login on darwin)
    2. ``~/.claude/.credentials.json`` (written by ``claude`` login on any
       platform)
    3. ``ANTHROPIC_API_KEY`` env var

    Returns ``(config_key, value)`` ready to drop into the agent config, or
    None if nothing was found.
    """
    if sys.platform == "darwin":
        try:
            r = subprocess.run(
                ["security", "find-generic-password", "-s", _CLAUDE_KEYCHAIN_SERVICE, "-w"],
                capture_output=True,
                text=True,
                timeout=5,
            )
            if r.returncode == 0 and r.stdout.strip():
                creds = json.loads(r.stdout.strip())
                logger.info("Using Claude OAuth from macOS Keychain")
                return "claude_oauth_credentials", json.dumps(creds, separators=(",", ":"))
        except (FileNotFoundError, PermissionError, subprocess.TimeoutExpired, json.JSONDecodeError):
            pass

    creds_path = Path.home() / ".claude" / ".credentials.json"
    if creds_path.exists():
        try:
            creds = json.loads(creds_path.read_text())
            if creds.get("claudeAiOauth"):
                logger.info("Using Claude OAuth from %s", creds_path)
                return "claude_oauth_credentials", json.dumps(creds, separators=(",", ":"))
        except (PermissionError, json.JSONDecodeError):
            pass

    key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if key:
        logger.info("Using ANTHROPIC_API_KEY from env")
        return "anthropic_api_key", key

    return None


def _agent_config_from_env() -> dict | None:
    """Build an ``agent`` block for the launch config, or None if no creds."""
    found = _discover_claude_credentials()
    if found is None:
        return None
    cred_key, cred_val = found
    return {
        "package": "claude-code",
        "config": {
            "model_name": "anthropic/claude-opus-4-6",
            "max_turns": 30,
            cred_key: cred_val,
        },
    }


def main() -> int:
    api_key = os.environ.get("PLATO_API_KEY")
    if not api_key:
        sys.exit("PLATO_API_KEY is required")
    agent_cfg = _agent_config_from_env()
    if agent_cfg is None:
        logger.warning(
            "No Claude credentials found in macOS Keychain, "
            "~/.claude/.credentials.json, or ANTHROPIC_API_KEY. "
            "send_message will fail with 'No authentication configured' "
            "inside the world. Run `claude` to log in."
        )

    world_kwargs: dict = {}
    if os.environ.get("PLATO_WORLD_PACKAGE"):
        world_kwargs["world_package"] = os.environ["PLATO_WORLD_PACKAGE"]
    if os.environ.get("PLATO_ALLOW_PRERELEASE"):
        world_kwargs["allow_prerelease"] = True
    if agent_cfg is not None:
        world_kwargs["agent_config"] = agent_cfg

    plato = Plato(api_key=api_key)
    try:
        logger.info("Launching DatagenSession against sim=%s ...", SIM)
        session: DatagenSession = DatagenSession.from_envs(
            http_client=plato._http,
            api_key=api_key,
            envs=[Env.simulator(SIM, alias=SIM)],
            **world_kwargs,
        )
        logger.info("Session up: %s", session.session_id)
        logger.info("Runtime REST URL: %s", session._runtime_connect_url)

        # ---- 2. Drive the agent ------------------------------------------
        logger.info("Sending prompt to agent (this can take a few minutes)…")
        resp = session.send_message(PROMPT, timeout=900.0)
        logger.info(
            "Agent response: success=%s iteration=%s chronos_session=%s",
            resp.success,
            resp.iteration,
            resp.chronos_session_id,
        )
        if resp.error:
            logger.warning("Agent error: %s", resp.error)

        # ---- 3. Independently verify via call_tool -----------------------
        env = session.get_env(SIM)
        if env is None:
            logger.error("get_env(%s) returned None — aborting", SIM)
            return 1
        logger.info("Listing tools on env %s ...", SIM)
        tools = env.list_tools()
        logger.info("Tools available: %s", [f"{t['mcp']}.{t['op']}" for t in tools])

        if any(t["mcp"] == "vm" and t["op"] == "get_containers" for t in tools):
            try:
                containers = env.tools.vm.get_containers()
                logger.info("vm.get_containers result: %s", str(containers)[:500])
            except Exception as exc:
                logger.warning("call_tool vm.get_containers failed: %s", exc)

        # ---- 4. Public URL ------------------------------------------------
        urls = session.get_public_url()
        sim_url = urls.get(SIM)
        logger.info("==> Public URL for %s: %s", SIM, sim_url)

        # ---- 5. Playwright login + open the sim ---------------------------
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)
            try:
                logger.info("Running session.login() in Playwright …")
                login = session.login(browser=browser, dataset="base")
                page = login.pages.get(SIM)
                if page is None and login.pages:
                    page = next(iter(login.pages.values()))
                if page is not None and sim_url:
                    page.goto(sim_url)
                    logger.info("Browser pointed at %s", sim_url)
                logger.info(
                    "Browser is open. Inspect the data you just inserted. Press <Enter> here to tear down the session."
                )
                input()
            finally:
                browser.close()

        # ---- 6. Graceful shutdown ----------------------------------------
        logger.info("stop_conversation() — graceful loop exit …")
        try:
            session.stop_conversation()
        except Exception as exc:
            logger.warning("stop_conversation failed (may already be done): %s", exc)
        logger.info("close()")
        session.close()
    finally:
        plato.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
