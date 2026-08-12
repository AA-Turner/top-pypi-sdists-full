"""Packaging for the NX terminal CLI.

Installs the `nx` and `nxplora` commands. NX is the model layer built by
Nexplora; this client authenticates against the nexplora-v2 gateway and
streams responses. No provider keys ship with this package.
"""

from setuptools import setup

setup(
    name="nxplora",
    version="0.15.264",
    description="NX — the operator. Terminal CLI for the Nexplora model layer.",
    long_description=(
        "NX is an AI Operating System for business operators, built by Nexplora. "
        "This CLI signs in with your Nexplora account (OAuth device flow or API "
        "key) and streams NX responses in your terminal. Routing, billing, and "
        "model access are handled by the Nexplora gateway."
    ),
    long_description_content_type="text/markdown",
    author="Nexplora",
    url="https://nexplora.ai",
    license="Proprietary",
    py_modules=["chat_ui","nx_cli","nx_intent","nx_slash_menu","nx_terminal","welcome","nx_data","nx_storage","nx_rag","nx_routing","nx_prompts","nx_key_pool","nx_vpn","nx_executor","nx_mcp","nx_mcp_hub","nx_mcp_manager","nx_mcp_security","nx_mcp_sandbox","nx_skills_import","nx_obfuscate","nx_canvas","nx_autoconnect","nx_brain_local","nx_channels","nx_channel_actions","nx_channel_tools","nx_integrations_directory","nx_oauth_endpoints","nx_mcp_oauth","nx_mcp_client","nx_mcp_tools","nx_vault_sync","nx_cloud_dispatch","nx_ebay_tools","nx_council","nx_agents","risk_tiers","autonomy_loop","nx_code_gate","nx_loop","nx_message","nx_proof_gate","nx_creator","nx_tool_sandbox","nx_verify","nx_detectors","nx_drift_monitor","nx_browse","nx_worlds","nx_bundled_skills","nx_tool_manifest","nx_background","nx_computer","nx_desktop","nx_harness","nx_mission","nx_phone","nx_keystore","nx_inbox","nx_daemon"],
    python_requires=">=3.8",
    # Windows port (0.15.240): secret storage no longer shells out to macOS `security` —
    # it routes through nx_keystore (keyring: Windows Credential Locker / Linux Secret
    # Service) on every non-darwin platform, macOS keeping its native Keychain path.
    # URL launch is webbrowser (cross-platform); iMessage is gated macOS-only with an
    # honest message; input already goes through prompt_toolkit with an msvcrt fallback;
    # chmod 0o600 is a harmless no-op on Windows. pynput / computer-control stays
    # darwin-only (its marker below). Cross-platform paths are covered by
    # tests/test_cross_platform.py; real-Windows smoke verification is still advised.
    platforms=["macos", "linux", "windows"],
    classifiers=[
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
    ],
    # Core deps — required for NX to boot and run a basic REPL turn.
    install_requires=[
        "httpx>=0.27.0",
        "requests>=2.28.0",
        # MX lookup for /supply email provider auto-detection (custom domains on Google
        # Workspace / Microsoft 365). Pure-Python + cross-platform (Windows included) — no
        # shelling out to dig/nslookup.
        "dnspython>=2.0.0",
        "rich>=13.0.0",
        "textual>=0.80.0",
        "prompt_toolkit>=3.0.0",
        "supabase>=2.0.0",
        "keyring>=24.0.0",
        "cryptography>=42.0.0",
        # $browse ships with NX — the web agent drives the operator's own system Chrome via
        # Playwright's `channel="chrome"` (no browser download; it uses installed Chrome). The pip
        # package carries its own driver, so `$browse` works on a plain install with zero extra steps.
        "playwright>=1.40",
        # control_computer's precise mouse/keyboard backend ships too — pynput is pip-installable (same macOS
        # CGEvent path as cliclick), so NO `brew install cliclick`. macOS-only (that's the only OS computer-control
        # supports today; pynput on Linux would pull X11). osascript stays the built-in last-resort fallback.
        "pynput>=1.7; sys_platform == 'darwin'",
    ],
    # RAG extras — heavy ML deps. nx_rag.py soft-imports every one of these
    # and falls back gracefully when they're missing, so a lean install
    # still works for everyone who doesn't use `/skills` or `/memory` search.
    extras_require={
        "rag": [
            "sentence-transformers",
            "turbovec",
            "rank-bm25",
            "flashrank",
        ],
        # `browse` is now CORE (playwright moved to install_requires) — kept as an empty no-op so any
        # existing `pip install nxplora[browse]` keeps working. The only optional piece is the bundled-
        # chromium fallback for machines with no Chrome: `playwright install chromium` (channel="chrome" needs none).
        "browse": [],
    },
    entry_points={
        "console_scripts": [
            "nx=nx_cli:main",
            "nxplora=nx_cli:main",
        ],
    },
)
