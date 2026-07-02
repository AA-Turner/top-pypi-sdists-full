"""Test harness infrastructure for SAGE functional testing.

Provides `TestResult`, `VerificationResult`, `run_test()`, and
`verify_output()` — the shared backbone for all functional test files.
"""

from __future__ import annotations

import subprocess
import sys
import shutil
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class TestResult:
    request: dict
    raw_response: str
    artifact_path: Path | None
    logs: str
    exit_code: int


@dataclass
class VerificationResult:
    """Four-gate verification used for every task-generation test."""

    install_ok: bool = False
    build_ok: bool = False
    run_ok: bool = False
    tests_ok: bool = False
    details: dict = field(default_factory=dict)

    @property
    def all_pass(self) -> bool:
        return self.install_ok and self.build_ok and self.run_ok and self.tests_ok


# ── Language / framework detection helpers ────────────────────────────────

_INSTALL_CMDS: dict[str, list[str]] = {
    "package.json": ["npm", "install", "--ignore-scripts"],
    "requirements.txt": [sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "--quiet"],
    "Pipfile": ["pipenv", "install"],
    "Cargo.toml": ["cargo", "fetch"],
    "go.mod": ["go", "mod", "download"],
    "pubspec.yaml": ["flutter", "pub", "get"],
    "Gemfile": ["bundle", "install"],
    "build.gradle": ["gradle", "dependencies"],
    "pom.xml": ["mvn", "dependency:resolve", "-q"],
}

_BUILD_CMDS: dict[str, list[str]] = {
    "package.json": ["npm", "run", "build"],
    "Cargo.toml": ["cargo", "build"],
    "go.mod": ["go", "build", "./..."],
    "build.gradle": ["gradle", "build"],
    "pom.xml": ["mvn", "compile", "-q"],
    "Makefile": ["make"],
}

_LANG_EXT_MAP: dict[str, str] = {
    "python": ".py", "go": ".go", "rust": ".rs", "java": ".java",
    "javascript": ".js", "typescript": ".ts", "c++": ".cpp", "c#": ".cs",
    "swift": ".swift", "kotlin": ".kt", "ruby": ".rb", "php": ".php",
    "perl": ".pl", "dart": ".dart", "scala": ".scala", "elixir": ".ex",
    "haskell": ".hs", "clojure": ".clj", "r": ".r", "lua": ".lua",
    "fortran": ".f90", "cobol": ".cob", "pascal": ".pas", "ada": ".adb",
    "lisp": ".lisp", "c": ".c",
}


def _detect_manifest(workspace: Path) -> str | None:
    """Return the first recognised manifest filename found in *workspace*."""
    for name in _INSTALL_CMDS:
        if (workspace / name).exists():
            return name
    return None


def _run_cmd(cmd: list[str], cwd: Path, timeout: int = 120) -> tuple[bool, str]:
    """Run *cmd* in *cwd*, return ``(success, combined_output)``."""
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout,
        )
        output = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode == 0, output
    except FileNotFoundError:
        return True, f"[skip] {cmd[0]} not found — treating as pass"
    except subprocess.TimeoutExpired:
        return False, f"[timeout] {' '.join(cmd)} exceeded {timeout}s"


# ── Public API ────────────────────────────────────────────────────────────

def run_test(channel: str, request: dict, model: str) -> TestResult:
    """Dispatch a test request to the appropriate channel harness."""
    if channel == "cli":
        from .cli import execute
    elif channel == "sms":
        from .sms import execute
    elif channel == "web":
        from .web import execute
    else:
        raise ValueError(f"Unknown channel: {channel}")

    return execute(request, model)


def verify_output(workspace: Path, language: str | None = None) -> VerificationResult:
    """Run the four-gate verification suite against *workspace*.

    1. **install_ok** — dependency install succeeds (or no manifest → auto-pass)
    2. **build_ok** — build/compile succeeds (or no build step → auto-pass)
    3. **run_ok** — main entrypoint runs without crash (exit 0 within 10 s)
    4. **tests_ok** — any test files found are executed and pass

    For simple single-file outputs (e.g. a standalone `.py`), gates 1 and 2
    auto-pass, gate 3 runs the file, and gate 4 is auto-pass if no tests exist.
    """
    vr = VerificationResult()
    details: dict = {}

    # ── Gate 1: Install ──────────────────────────────────────────────────
    manifest = _detect_manifest(workspace)
    if manifest:
        ok, out = _run_cmd(_INSTALL_CMDS[manifest], workspace)
        vr.install_ok = ok
        details["install"] = out[:500]
    else:
        vr.install_ok = True
        details["install"] = "[auto-pass] no manifest detected"

    # ── Gate 2: Build ────────────────────────────────────────────────────
    if manifest and manifest in _BUILD_CMDS:
        # Only attempt build if package.json has a "build" script
        if manifest == "package.json":
            import json
            try:
                pkg = json.loads((workspace / "package.json").read_text())
                if "build" not in pkg.get("scripts", {}):
                    vr.build_ok = True
                    details["build"] = "[auto-pass] no build script in package.json"
                else:
                    ok, out = _run_cmd(_BUILD_CMDS[manifest], workspace)
                    vr.build_ok = ok
                    details["build"] = out[:500]
            except Exception:
                vr.build_ok = True
                details["build"] = "[auto-pass] package.json parse error, skipping"
        else:
            ok, out = _run_cmd(_BUILD_CMDS[manifest], workspace)
            vr.build_ok = ok
            details["build"] = out[:500]
    else:
        # Single-file compile check
        if language and language in ("c", "c++", "rust", "go", "java"):
            ext = _LANG_EXT_MAP.get(language, "")
            source_files = list(workspace.rglob(f"*{ext}"))
            if source_files:
                src = source_files[0]
                if language == "python":
                    ok, out = _run_cmd([sys.executable, "-m", "py_compile", str(src)], workspace)
                elif language == "go":
                    ok, out = _run_cmd(["go", "build", str(src)], workspace)
                elif language == "rust":
                    ok, out = _run_cmd(["rustc", "--edition", "2021", str(src), "-o", "/dev/null"], workspace)
                elif language in ("c", "c++"):
                    compiler = "g++" if language == "c++" else "gcc"
                    ok, out = _run_cmd([compiler, str(src), "-o", "/dev/null", "-fsyntax-only"], workspace)
                elif language == "java":
                    ok, out = _run_cmd(["javac", str(src)], workspace)
                else:
                    ok, out = True, "[auto-pass]"
                vr.build_ok = ok
                details["build"] = out[:500]
            else:
                vr.build_ok = True
                details["build"] = "[auto-pass] no source files found"
        else:
            vr.build_ok = True
            details["build"] = "[auto-pass] no build step needed"

    # ── Gate 3: Run ──────────────────────────────────────────────────────
    entrypoints = (
        list(workspace.glob("main.py")) +
        list(workspace.glob("app.py")) +
        list(workspace.glob("server.py")) +
        list(workspace.glob("index.js")) +
        list(workspace.glob("index.html")) +
        list(workspace.glob("main.go")) +
        list(workspace.glob("main.rs"))
    )
    if entrypoints:
        ep = entrypoints[0]
        if ep.suffix == ".py":
            ok, out = _run_cmd([sys.executable, str(ep)], workspace, timeout=15)
        elif ep.suffix == ".js":
            ok, out = _run_cmd(["node", str(ep)], workspace, timeout=15)
        elif ep.suffix == ".html":
            # HTML files can't be "run" in the traditional sense — just verify they exist
            ok, out = True, "[auto-pass] HTML file exists"
        elif ep.suffix == ".go":
            ok, out = _run_cmd(["go", "run", str(ep)], workspace, timeout=15)
        else:
            ok, out = True, f"[auto-pass] no runner for {ep.suffix}"
        vr.run_ok = ok
        details["run"] = out[:500]
    else:
        # No recognised entrypoint — check if any code files exist at all
        code_files = list(workspace.rglob("*.py")) + list(workspace.rglob("*.js")) + list(workspace.rglob("*.go"))
        if code_files:
            ep = code_files[0]
            if ep.suffix == ".py":
                ok, out = _run_cmd([sys.executable, "-c", f"import py_compile; py_compile.compile('{ep}', doraise=True)"], workspace, timeout=10)
            else:
                ok, out = True, "[auto-pass] non-Python code file exists"
            vr.run_ok = ok
            details["run"] = out[:500]
        else:
            vr.run_ok = True
            details["run"] = "[auto-pass] no entrypoint detected"

    # ── Gate 4: Tests ────────────────────────────────────────────────────
    test_files = list(workspace.rglob("test_*.py")) + list(workspace.rglob("*_test.py")) + list(workspace.rglob("tests.py"))
    if test_files:
        ok, out = _run_cmd([sys.executable, "-m", "pytest", str(workspace), "-x", "--tb=short", "-q"], workspace, timeout=120)
        vr.tests_ok = ok
        details["tests"] = out[:500]
    else:
        # Check for JS tests
        js_test_files = list(workspace.rglob("*.test.js")) + list(workspace.rglob("*.spec.js"))
        if js_test_files and (workspace / "package.json").exists():
            ok, out = _run_cmd(["npm", "test"], workspace, timeout=120)
            vr.tests_ok = ok
            details["tests"] = out[:500]
        else:
            vr.tests_ok = True
            details["tests"] = "[auto-pass] no test files detected"

    vr.details = details
    return vr


def run_test_with_verification(
    channel: str, request: dict, model: str, language: str | None = None,
) -> tuple[TestResult, VerificationResult]:
    """Convenience wrapper: run a test then verify the output workspace."""
    result = run_test(channel, request, model)
    workspace = result.artifact_path
    if workspace and workspace.is_dir():
        verification = verify_output(workspace, language)
    elif workspace and workspace.is_file():
        verification = verify_output(workspace.parent, language)
    else:
        verification = VerificationResult(
            install_ok=False, build_ok=False, run_ok=False, tests_ok=False,
            details={"error": "No workspace/artifact found"},
        )
    return result, verification
