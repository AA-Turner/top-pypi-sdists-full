#!/usr/bin/env python3
"""Drydock install smoke test — runs inside a clean container.

Steps:
1. Verify Python + pip work
2. Install drydock-cli from PyPI
3. Verify `drydock --version` and `--help` exit 0
4. Write a config pointing at the host llama.cpp endpoint
5. Spawn drydock via pexpect, send a trivial prompt, assert a response

Exit code 0 on full success. Prints structured [RESULT] line at the end.

Env overrides:
- DRYDOCK_VERSION       — pin a specific version (default: latest)
- LLAMACPP_URL          — model endpoint (default: http://host.docker.internal:8001/v1)
- LLAMACPP_MODEL        — model name (default: gemma4)
- SMOKE_TIMEOUT_S       — TUI response timeout (default: 90)
- VERBOSE               — extra logging
"""
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

VERSION = os.environ.get("DRYDOCK_VERSION", "")  # blank = latest
LLAMACPP_URL = os.environ.get("LLAMACPP_URL", "http://host.docker.internal:8001/v1")
LLAMACPP_MODEL = os.environ.get("LLAMACPP_MODEL", "gemma4")
SMOKE_TIMEOUT_S = int(os.environ.get("SMOKE_TIMEOUT_S", "90"))
VERBOSE = os.environ.get("VERBOSE", "") not in ("", "0", "false")

OS_LABEL = os.environ.get("OS_LABEL", "unknown")


def log(msg: str) -> None:
    print(f"[smoke] {msg}", flush=True)


def vlog(msg: str) -> None:
    if VERBOSE:
        print(f"[smoke verbose] {msg}", flush=True)


def step_install() -> tuple[bool, str]:
    """pip install drydock-cli, optionally pinned."""
    log("Installing drydock-cli...")
    pkg = "drydock-cli"
    if VERSION:
        pkg = f"drydock-cli=={VERSION}"
    proc = subprocess.run(
        ["pip", "install", "--no-cache-dir", pkg],
        capture_output=True, text=True, timeout=180,
    )
    if proc.returncode != 0:
        return False, proc.stderr[-2000:]
    return True, pkg


def step_version() -> tuple[bool, str]:
    log("Verifying drydock --version...")
    proc = subprocess.run(
        ["drydock", "--version"],
        capture_output=True, text=True, timeout=15,
    )
    if proc.returncode != 0:
        return False, f"rc={proc.returncode} stderr={proc.stderr[-500:]}"
    return True, proc.stdout.strip()


def step_help() -> tuple[bool, str]:
    log("Verifying drydock --help...")
    proc = subprocess.run(
        ["drydock", "--help"],
        capture_output=True, text=True, timeout=15,
    )
    if proc.returncode != 0:
        return False, f"rc={proc.returncode}"
    if "Usage" not in proc.stdout and "usage" not in proc.stdout.lower():
        return False, "no 'usage' in help output"
    return True, "help ok"


def step_network() -> tuple[bool, str]:
    """Verify the container can reach the host llama.cpp endpoint."""
    log(f"Checking network reach to {LLAMACPP_URL}/models ...")
    import urllib.request
    import urllib.error
    try:
        req = urllib.request.Request(f"{LLAMACPP_URL}/models")
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.load(r)
        names = []
        for m in data.get("data", []) or data.get("models", []):
            n = m.get("id") or m.get("name")
            if n:
                names.append(n)
        if LLAMACPP_MODEL not in names:
            return False, f"model {LLAMACPP_MODEL!r} not in {names!r}"
        return True, f"reachable, models={names}"
    except (urllib.error.URLError, OSError) as e:
        return False, f"unreachable: {e}"


def step_config() -> tuple[bool, str]:
    """Write a minimal config pointing at the host llama.cpp."""
    log("Writing config...")
    config_dir = Path.home() / ".drydock"
    config_dir.mkdir(exist_ok=True)
    config_path = config_dir / "config.toml"
    config = f"""active_model = "local"
auto_approve = true
enable_telemetry = false
enable_update_checks = false
enable_auto_update = false
disable_welcome_banner_animation = true
api_timeout = 60.0

[[providers]]
name = "llamacpp"
api_base = "{LLAMACPP_URL}"
api_key_env_var = ""
api_style = "openai"
backend = "generic"

[[models]]
name = "{LLAMACPP_MODEL}"
provider = "llamacpp"
alias = "local"
"""
    config_path.write_text(config)
    # Pre-trust the cwd so first-launch trust dialog doesn't block pexpect.
    trusted = config_dir / "trusted_folders.toml"
    trusted.write_text(f'trusted = ["{Path.cwd()}"]\n')
    return True, str(config_path)


def step_smoke_prompt() -> tuple[bool, str]:
    """Spawn drydock via pexpect, send a trivial prompt, assert a response.

    drydock is interactive (no headless mode by design). pexpect is the
    standard way to drive it — same approach the test_harness uses.
    """
    try:
        import pexpect
    except ImportError:
        # Install pexpect on the fly — it's tiny and a hard dep for the test
        log("Installing pexpect for the smoke step...")
        subprocess.run(["pip", "install", "--quiet", "pexpect"],
                       check=True, timeout=60)
        import pexpect

    log(f"Spawning drydock TUI (timeout {SMOKE_TIMEOUT_S}s)...")
    workdir = Path.cwd()
    child = pexpect.spawn(
        "drydock",
        cwd=str(workdir),
        encoding="utf-8",
        timeout=SMOKE_TIMEOUT_S,
        env={
            **os.environ,
            # Make sure drydock doesn't try to update itself mid-test
            "DRYDOCK_DISABLE_UPDATES": "1",
            # Disable banner animation for cleaner pexpect output
            "TERM": "dumb",
        },
    )

    # Common pexpect patterns to look for
    READY_PATTERNS = [
        "Type a message",
        "How can I help",
        ">",          # prompt indicator
        "│",          # textual border char
        pexpect.TIMEOUT,
    ]

    try:
        # Wait for TUI to be ready
        idx = child.expect(READY_PATTERNS, timeout=30)
        vlog(f"TUI ready signal idx={idx} (pattern matched)")
        time.sleep(2)  # let TUI settle

        # Send the smoke prompt
        prompt = "what is 2+2? Answer in one word."
        log(f"Sending prompt: {prompt!r}")
        child.sendline(prompt)

        # Wait for a model response containing "4" or "four"
        idx = child.expect(
            [r"4", r"four", r"Four", r"FOUR", pexpect.TIMEOUT, pexpect.EOF],
            timeout=SMOKE_TIMEOUT_S,
        )
        if idx >= 4:
            # capture some of the buffer for diagnosis
            buf_tail = (child.before or "")[-600:].replace("\n", " | ")
            return False, f"no 4/four response in {SMOKE_TIMEOUT_S}s; buf_tail={buf_tail!r}"

        vlog(f"Response matched pattern idx={idx}")

        # Clean exit
        child.sendcontrol("c")
        time.sleep(0.5)
        child.sendcontrol("d")
        child.expect(pexpect.EOF, timeout=10)
        return True, "smoke ok"
    except pexpect.TIMEOUT:
        buf_tail = (child.before or "")[-600:].replace("\n", " | ")
        return False, f"timeout; buf_tail={buf_tail!r}"
    except pexpect.EOF:
        buf_tail = (child.before or "")[-600:].replace("\n", " | ")
        return False, f"drydock exited early; buf_tail={buf_tail!r}"
    finally:
        try:
            child.close(force=True)
        except Exception:
            pass


def main() -> int:
    start = time.time()
    results: dict[str, tuple[bool, str]] = {}

    # Step 1: install
    ok, detail = step_install()
    results["install"] = (ok, detail)
    if not ok:
        log(f"FATAL install failed: {detail[-400:]}")
        emit_result(results, start)
        return 1

    # Step 2: version
    ok, detail = step_version()
    results["version"] = (ok, detail)

    # Step 3: help
    ok, detail = step_help()
    results["help"] = (ok, detail)

    # Step 4: network reach
    ok, detail = step_network()
    results["network"] = (ok, detail)

    # Step 5: config
    ok, detail = step_config()
    results["config"] = (ok, detail)

    # Step 6: smoke prompt (only if network + config ok)
    if results["network"][0] and results["config"][0]:
        ok, detail = step_smoke_prompt()
        results["smoke"] = (ok, detail)
    else:
        results["smoke"] = (False, "skipped — network or config failed earlier")

    return emit_result(results, start)


def emit_result(results: dict[str, tuple[bool, str]], start: float) -> int:
    elapsed = time.time() - start
    all_pass = all(ok for ok, _ in results.values())
    status = "PASS" if all_pass else "FAIL"
    parts = []
    for step, (ok, detail) in results.items():
        if ok:
            parts.append(f"{step}=ok")
        else:
            short = detail[:40].replace(" ", "_")
            parts.append(f"{step}=FAIL({short})")
    print(f"\n[RESULT] {OS_LABEL} {status}  " + " ".join(parts) + f"  elapsed={elapsed:.1f}s")
    if not all_pass:
        print("\n=== failure details ===")
        for step, (ok, detail) in results.items():
            if not ok:
                print(f"  {step}: {detail[:500]}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    sys.exit(main())
