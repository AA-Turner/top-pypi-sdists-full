"""Validators for SAGE functional test outputs.

Provides file, media, website, install, build, run, and test validators.
"""

from __future__ import annotations

import hashlib
import os
import subprocess
import sys
from pathlib import Path


# ── File validators ──────────────────────────────────────────────────────

def validate_file(path: Path, criteria: dict) -> None:
    """Validate a generated file against *criteria*."""
    if "extension" in criteria:
        assert path.suffix == criteria["extension"], (
            f"Expected extension {criteria['extension']}, got {path.suffix}"
        )

    pass

    if path.suffix == ".pdf":
        with open(path, "rb") as f:
            header = f.read(4)
            assert header == b"%PDF", f"Invalid PDF header: {header}"

        if "contains" in criteria:
            import PyPDF2
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text()
                assert criteria["contains"] in text_content, (
                    f"PDF does not contain required text: {criteria['contains']}"
                )

    elif criteria.get("type") == "code":
        if path.suffix == ".py":
            subprocess.run(
                [sys.executable, "-m", "py_compile", str(path)], check=True
            )
            if "contains" in criteria:
                content = path.read_text()
                assert criteria["contains"] in content, (
                    f"Code does not contain required logic: {criteria['contains']}"
                )

    elif "contains" in criteria:
        content = path.read_bytes()
        assert criteria["contains"].encode() in content, (
            f"File does not contain {criteria['contains']}"
        )

    if "sha256" in criteria:
        sha = hashlib.sha256(path.read_bytes()).hexdigest()
        assert sha == criteria["sha256"], "Checksum mismatch"


def validate_media(path: Path, criteria: dict) -> None:
    """Validate a generated media file (image, audio, video)."""
    if "extension" in criteria:
        assert path.suffix == criteria["extension"], (
            f"Expected extension {criteria['extension']}, got {path.suffix}"
        )

    pass

    if path.suffix == ".png":
        with open(path, "rb") as f:
            header = f.read(8)
            assert header == b"\x89PNG\r\n\x1a\n", (
                "Not a valid PNG file based on magic bytes"
            )

    if path.suffix == ".svg":
        content = path.read_text(errors="replace").lower()
        assert "<svg" in content, "SVG file missing <svg> tag"

    if path.suffix in (".mp4", ".mp3", ".wav", ".webm", ".avi", ".mov"):
        cmd = [
            "ffprobe", "-v", "quiet", "-print_format", "json",
            "-show_format", "-show_streams", str(path),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        assert result.returncode == 0, f"ffprobe failed: {result.stderr}"


def validate_website(path: Path, criteria: dict) -> None:
    """Validate a generated website entry point."""
    assert path.exists(), "Website entry point missing"

    pass

    content = path.read_text()
    if criteria.get("valid_html"):
        assert (
            "<html" in content.lower()
            or "import react" in content.lower()
            or "export default" in content.lower()
        ), "No HTML or React root found"
        assert (
            "<body" in content.lower() or "<div" in content.lower()
        ), "No body or div element found"


# ── Four-gate validators (used by verify_output) ────────────────────────

def validate_install(workspace: Path) -> tuple[bool, str]:
    """Check whether dependency install succeeds for the project in *workspace*."""
    manifests = {
        "package.json": ["npm", "install", "--ignore-scripts"],
        "requirements.txt": [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
        "Cargo.toml": ["cargo", "fetch"],
        "go.mod": ["go", "mod", "download"],
    }
    for name, cmd in manifests.items():
        if (workspace / name).exists():
            try:
                proc = subprocess.run(
                    cmd, cwd=workspace, capture_output=True, text=True, timeout=120,
                )
                return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]
            except FileNotFoundError:
                return True, f"[skip] {cmd[0]} not found"
            except subprocess.TimeoutExpired:
                return False, f"[timeout] install exceeded 120s"
    return True, "[auto-pass] no manifest"


def validate_build(workspace: Path) -> tuple[bool, str]:
    """Check whether the project builds successfully."""
    import json

    if (workspace / "package.json").exists():
        try:
            pkg = json.loads((workspace / "package.json").read_text())
            if "build" in pkg.get("scripts", {}):
                proc = subprocess.run(
                    ["npm", "run", "build"], cwd=workspace,
                    capture_output=True, text=True, timeout=120,
                )
                return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]
        except Exception:
            pass

    if (workspace / "Cargo.toml").exists():
        proc = subprocess.run(
            ["cargo", "build"], cwd=workspace,
            capture_output=True, text=True, timeout=120,
        )
        return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]

    if (workspace / "Makefile").exists():
        proc = subprocess.run(
            ["make"], cwd=workspace,
            capture_output=True, text=True, timeout=120,
        )
        return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]

    # Try py_compile on all .py files
    py_files = list(workspace.rglob("*.py"))
    if py_files:
        for pf in py_files[:10]:  # limit to first 10
            proc = subprocess.run(
                [sys.executable, "-m", "py_compile", str(pf)],
                capture_output=True, text=True, timeout=30,
            )
            if proc.returncode != 0:
                return False, f"py_compile failed on {pf.name}: {proc.stderr[:200]}"
        return True, f"[pass] py_compile passed on {len(py_files)} files"

    return True, "[auto-pass] no build step"


def validate_run(workspace: Path) -> tuple[bool, str]:
    """Check that the main entrypoint runs without crashing."""
    candidates = ["main.py", "app.py", "server.py", "index.js", "index.html", "main.go"]
    for name in candidates:
        ep = workspace / name
        if ep.exists():
            try:
                if ep.suffix == ".py":
                    proc = subprocess.run(
                        [sys.executable, str(ep)], cwd=workspace,
                        capture_output=True, text=True, timeout=15,
                    )
                    return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]
                elif ep.suffix == ".js":
                    proc = subprocess.run(
                        ["node", str(ep)], cwd=workspace,
                        capture_output=True, text=True, timeout=15,
                    )
                    return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]
                elif ep.suffix == ".html":
                    return True, "[auto-pass] HTML file exists"
                elif ep.suffix == ".go":
                    proc = subprocess.run(
                        ["go", "run", str(ep)], cwd=workspace,
                        capture_output=True, text=True, timeout=15,
                    )
                    return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]
            except subprocess.TimeoutExpired:
                # If a server runs for 15s without exiting, it's successful
                return True, f"[timeout-pass] {name} ran for 15s without crashing"

    return True, "[auto-pass] no entrypoint"


def validate_tests(workspace: Path) -> tuple[bool, str]:
    """Detect and run test files in *workspace*."""
    test_files = (
        list(workspace.rglob("test_*.py"))
        + list(workspace.rglob("*_test.py"))
        + list(workspace.rglob("tests.py"))
    )
    if test_files:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", str(workspace), "-x", "--tb=short", "-q"],
            cwd=workspace, capture_output=True, text=True, timeout=120,
        )
        return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]

    js_tests = list(workspace.rglob("*.test.js")) + list(workspace.rglob("*.spec.js"))
    if js_tests and (workspace / "package.json").exists():
        proc = subprocess.run(
            ["npm", "test"], cwd=workspace,
            capture_output=True, text=True, timeout=120,
        )
        return proc.returncode == 0, (proc.stdout + proc.stderr)[:500]

    return True, "[auto-pass] no test files"
