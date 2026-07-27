"""Install + verify orchestrator.

Discovers every project under a root directory and runs the appropriate
toolchain (install → build → run → test → lint) against each one.
Captures stdout+stderr per step in structured `StepResult` records the
verify loop in `build_project` can feed back to the LLM for fixes.

This module is the answer to the user's complaint that "neither the
frontend nor backend was installed by sage in order to test and run the
code" and "How can sage test its code if it never installed its code."

────────────────────────────────────────────────────────────────────────
HONESTY CONTRACT — read before changing anything in here
────────────────────────────────────────────────────────────────────────
Every command in this module REALLY EXECUTES. There is no environment
variable, no test mode, and no "simulate" branch that short-circuits a
step and reports success. Two such shortcuts existed historically and
were removed; do not reintroduce them.

`tests_ok` is True ONLY when a real test runner was invoked, exited zero,
AND executed at least one test. Specifically it is FALSE when:

  * no test files were produced,
  * no test runner/script is configured,
  * the runner binary is absent,
  * the runner exits non-zero,
  * the runner exits ZERO but collected/executed ZERO tests.

That last case is the important one. `pytest` exits 5, `go test ./...`
exits 0 with "[no test files]", `cargo test` exits 0 with "running 0
tests", and `swift test` exits 0 with "Executed 0 tests" — all of which
previously read as success. A suite that ran nothing has proven nothing.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


ProjectKind = Literal[
    "python", "node", "go", "rust", "java", "kotlin", "ruby", "swift",
    "dart", "cpp", "csharp", "static-web",
]


@dataclass
class DiscoveredProject:
    kind: ProjectKind
    root: Path
    extras: dict[str, str] = field(default_factory=dict)


@dataclass
class StepResult:
    name: str
    ok: bool
    log: str
    duration_s: float
    returncode: int = 0
    # Number of tests the runner actually executed. None = not a test step
    # or the count could not be determined from the runner's output.
    tests_collected: int | None = None
    # True when this record was synthesized rather than produced by running
    # a command. Synthetic records are never allowed to assert that tests
    # passed — see `verify_project`.
    synthetic: bool = False


# Substring markers used to classify a step by name. Kept as module
# constants so `VerifyReport` and `verify_project` can never disagree
# about what counts as a test step.
_INSTALL_TERMS = ("install", "tidy", "restore", "pub get")
_BUILD_TERMS = ("build", "compile", "make")
_RUN_TERMS = ("run check", "start check", "import check", "load check")
_TEST_TERMS = ("test", "pytest", "rspec", "ctest")


def _matches(name: str, terms: tuple[str, ...]) -> bool:
    lowered = name.lower()
    return any(term in lowered for term in terms)


def is_test_step(name: str) -> bool:
    """True when a step name denotes a test-execution step."""
    return _matches(name, _TEST_TERMS)


@dataclass
class VerifyReport:
    project: DiscoveredProject
    steps: list[StepResult]

    @property
    def install_ok(self) -> bool | None:
        for s in self.steps:
            if _matches(s.name, _INSTALL_TERMS):
                return s.ok
        return None

    @property
    def build_ok(self) -> bool | None:
        for s in self.steps:
            if _matches(s.name, _BUILD_TERMS) and not is_test_step(s.name):
                return s.ok
        return None

    @property
    def runs_ok(self) -> bool | None:
        for s in self.steps:
            if _matches(s.name, _RUN_TERMS):
                return s.ok
        return None

    @property
    def tests_ok(self) -> bool:
        """True ONLY if a real test runner ran and executed at least one test.

        Deliberately returns `bool`, never `None`: "we don't know whether
        the tests passed" is not a defensible way to report success, and
        callers used to aggregate `None` into a green result.
        """
        test_steps = [s for s in self.steps if is_test_step(s.name)]
        if not test_steps:
            # No test step at all — nothing was verified.
            return False
        for s in test_steps:
            if s.synthetic:
                # A synthesized record never proves a test ran.
                return False
            if not s.ok:
                return False
            if s.tests_collected is not None and s.tests_collected <= 0:
                # Runner exited clean but executed nothing.
                return False
        return True

    @property
    def tests_collected(self) -> int:
        """Total tests executed across every test step in this project."""
        return sum(
            s.tests_collected or 0
            for s in self.steps
            if is_test_step(s.name) and s.tests_collected is not None
        )

    @property
    def all_ok(self) -> bool:
        return all(s.ok for s in self.steps) and self.tests_ok


# Directories we always skip when discovering projects — they contain
# *installed* packages, not source projects.
_SKIP_DIRS: frozenset[str] = frozenset(
    {
        "node_modules", "venv", ".venv", "env", ".env", "build", "dist",
        ".git", ".pytest_cache", ".mypy_cache", ".ruff_cache",
        "__pycache__", ".next", ".expo", "target", "out", "bin",
    }
)


# ──────────────────────── discovery ────────────────────────────────────


def discover_projects(root: Path) -> list[DiscoveredProject]:
    """Walk `root` and return one DiscoveredProject per detected sub-project.

    Detection markers (in priority order, first hit wins per directory):
      - package.json        → node
      - pyproject.toml      → python
      - requirements.txt    → python
      - go.mod              → go
      - Cargo.toml          → rust
      - pom.xml / build.gradle* → java/kotlin
      - index.html (and nothing else) → static-web

    Skips any directory inside `_SKIP_DIRS` (notably node_modules, venv).
    Multiple markers in the same directory produce ONE project — we pick
    the most specific.
    """
    root = root.resolve()
    found: list[DiscoveredProject] = []
    seen_roots: set[Path] = set()

    for dirpath, dirnames, filenames in os.walk(root):
        # Prune skipped dirs in-place so os.walk doesn't recurse into them
        dirnames[:] = [d for d in dirnames if d not in _SKIP_DIRS and not d.startswith(".")]

        here = Path(dirpath)
        if here in seen_roots:
            continue

        kind: ProjectKind | None = None
        if "package.json" in filenames:
            kind = "node"
        elif "pyproject.toml" in filenames or "requirements.txt" in filenames:
            kind = "python"
        elif "go.mod" in filenames:
            kind = "go"
        elif "Cargo.toml" in filenames:
            kind = "rust"
        elif "pubspec.yaml" in filenames:
            kind = "dart"
        elif "Package.swift" in filenames:
            kind = "swift"
        elif "CMakeLists.txt" in filenames or "Makefile" in filenames or "makefile" in filenames:
            kind = "cpp"
        elif any(f.endswith(".csproj") for f in filenames):
            kind = "csharp"
        elif "pom.xml" in filenames or any(
            f.startswith("build.gradle") for f in filenames
        ):
            # Distinguish java and kotlin by looking for .kt files under this directory
            has_kt = False
            for sub_dirpath, _, sub_filenames in os.walk(dirpath):
                if any(f.endswith(".kt") for f in sub_filenames):
                    has_kt = True
                    break
            kind = "kotlin" if has_kt else "java"
        elif here == root and "index.html" in filenames:
            # A hand-written static site: real HTML, no build tooling. Only
            # recognised at the top level so nested template dirs inside a
            # node/python project don't spawn a second project.
            kind = "static-web"
        if kind:
            found.append(DiscoveredProject(kind=kind, root=here))
            seen_roots.add(here)

    return found


# ──────────────────────── step runner ──────────────────────────────────


def run_step(
    name: str,
    cmd: list[str],
    *,
    cwd: Path,
    timeout: int = 600,
    env: dict[str, str] | None = None,
) -> StepResult:
    """Run a shell command and capture the result. Never raises.

    The command ALWAYS executes. There is no mock/simulate path.
    """
    full_env = os.environ.copy()
    if env:
        full_env.update(env)

    start = time.monotonic()
    try:
        proc = subprocess.run(
            cmd,
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=full_env,
            check=False,
        )
        log = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        return StepResult(
            name=name,
            ok=proc.returncode == 0,
            log=log,
            duration_s=time.monotonic() - start,
            returncode=proc.returncode,
        )
    except FileNotFoundError as exc:
        return StepResult(
            name=name,
            ok=False,
            log=f"command not found: {exc}",
            duration_s=time.monotonic() - start,
            returncode=127,
        )
    except NotADirectoryError as exc:
        return StepResult(
            name=name,
            ok=False,
            log=f"working directory is not usable: {exc}",
            duration_s=time.monotonic() - start,
            returncode=127,
        )
    except subprocess.TimeoutExpired:
        return StepResult(
            name=name,
            ok=False,
            log=f"timeout after {timeout}s",
            duration_s=time.monotonic() - start,
            returncode=124,
        )
    except Exception as exc:  # noqa: BLE001 — verification must NEVER crash
        return StepResult(
            name=name,
            ok=False,
            log=f"unexpected error: {exc}",
            duration_s=time.monotonic() - start,
            returncode=1,
        )


# ──────────────────────── test-count extraction ────────────────────────
#
# Every runner reports "I ran nothing" differently, and most of them do it
# with exit code 0. These parsers turn the runner's own output into a
# number so `tests_ok` can refuse to call an empty run a pass.

_PYTEST_COLLECTED = re.compile(r"collected\s+(\d+)\s+items?")
_PYTEST_TALLY = re.compile(r"(\d+)\s+(?:passed|failed|error|errors|xfailed|xpassed)")
_JEST_TOTAL = re.compile(r"Tests:.*?(\d+)\s+total", re.DOTALL)
_VITEST_TOTAL = re.compile(r"Tests\s+(?:\d+\s+failed\s*\|\s*)?(\d+)\s+passed")
_BUN_TOTAL = re.compile(r"(\d+)\s+pass")
_CARGO_RUNNING = re.compile(r"running\s+(\d+)\s+tests?")
_GO_OK_PKG = re.compile(r"^(?:ok|FAIL)\s+\S+", re.MULTILINE)
_GO_NO_TESTS = re.compile(r"^\?\s+\S+\s+\[no test files\]", re.MULTILINE)
_SWIFT_EXECUTED = re.compile(r"Executed\s+(\d+)\s+tests?")
_CTEST_TOTAL = re.compile(r"Total Tests:\s*(\d+)")
_DOTNET_TALLY = re.compile(r"(?:Passed|Failed|Skipped)!?\s*-?\s*.*?total:\s*(\d+)", re.IGNORECASE)
_RSPEC_EXAMPLES = re.compile(r"(\d+)\s+examples?,")
_DART_TALLY = re.compile(r"\+(\d+)")


def count_tests_executed(runner: str, log: str, returncode: int) -> int | None:
    """Best-effort count of tests a runner actually executed.

    Returns 0 when the output positively states nothing ran, a positive
    count when it can be parsed, and None when the format is unknown (in
    which case `tests_ok` falls back to the exit code alone).
    """
    r = runner.lower()
    text = log or ""

    if "pytest" in r:
        # Exit code 5 is pytest's dedicated "no tests were collected".
        if returncode == 5 or "no tests ran" in text.lower():
            return 0
        m = _PYTEST_COLLECTED.search(text)
        if m:
            return int(m.group(1))
        tally = sum(int(x) for x in _PYTEST_TALLY.findall(text))
        if tally:
            return tally
        return None

    if "bun test" in r:
        m = _BUN_TOTAL.search(text)
        return int(m.group(1)) if m else None

    if "npm test" in r or "jest" in r or "vitest" in r or "yarn test" in r:
        low = text.lower()
        if "no tests found" in low or "no test files found" in low:
            return 0
        m = _JEST_TOTAL.search(text) or _VITEST_TOTAL.search(text)
        if m:
            return int(m.group(1))
        # node's built-in runner
        m = re.search(r"^#\s*tests\s+(\d+)", text, re.MULTILINE)
        if m:
            return int(m.group(1))
        return None

    if "cargo test" in r:
        totals = [int(x) for x in _CARGO_RUNNING.findall(text)]
        if totals:
            return sum(totals)
        return None

    if "go test" in r:
        # `go test ./...` exits 0 when every package has no test files.
        if _GO_NO_TESTS.search(text) and not _GO_OK_PKG.search(text):
            return 0
        if "no test files" in text and not _GO_OK_PKG.search(text):
            return 0
        ran = len(re.findall(r"^\s*--- (?:PASS|FAIL|SKIP):", text, re.MULTILINE))
        if ran:
            return ran
        if _GO_OK_PKG.search(text):
            return None  # packages passed but verbose counts unavailable
        return 0

    if "swift test" in r:
        m = _SWIFT_EXECUTED.search(text)
        if m:
            return int(m.group(1))
        if "no tests found" in text.lower():
            return 0
        return None

    if "ctest" in r:
        low = text.lower()
        if "no tests were found" in low:
            return 0
        m = _CTEST_TOTAL.search(text)
        return int(m.group(1)) if m else None

    if "dotnet test" in r:
        low = text.lower()
        if "no test is available" in low:
            return 0
        m = _DOTNET_TALLY.search(text)
        return int(m.group(1)) if m else None

    if "rspec" in r:
        m = _RSPEC_EXAMPLES.search(text)
        return int(m.group(1)) if m else None

    if "dart test" in r or "flutter test" in r:
        low = text.lower()
        if "no tests ran" in low or "no tests were found" in low:
            return 0
        nums = [int(x) for x in _DART_TALLY.findall(text)]
        return max(nums) if nums else None

    return None


def run_test_step(
    name: str,
    cmd: list[str],
    *,
    cwd: Path,
    timeout: int = 600,
    env: dict[str, str] | None = None,
) -> StepResult:
    """Run a test command and record how many tests actually executed.

    A zero exit code with zero tests executed is downgraded to a FAILURE —
    a suite that ran nothing has proven nothing.
    """
    res = run_step(name, cmd, cwd=cwd, timeout=timeout, env=env)
    collected = count_tests_executed(name, res.log, res.returncode)
    res.tests_collected = collected
    if res.ok and collected is not None and collected <= 0:
        res.ok = False
        res.log = (
            f"ZERO TESTS EXECUTED. `{' '.join(cmd)}` exited {res.returncode} but ran no "
            "tests, so nothing was verified. A test suite must contain at least one "
            "executable test.\n\n" + res.log
        )
    return res


def missing_tests_step(kind: str, reason: str) -> StepResult:
    """A failing, clearly-labelled stand-in for an absent test suite.

    `verify_project` must always emit a test step so `tests_ok` is
    well-defined, but a project with no tests must NEVER be green.
    """
    return StepResult(
        name=f"{kind} test (NO TESTS RUN)",
        ok=False,
        log=(
            f"tests_ok=False: {reason}\n"
            "sage requires that it writes native tests for its own output, runs them, "
            "and that they pass. No test run happened here, so there is nothing to pass."
        ),
        duration_s=0.0,
        returncode=1,
        tests_collected=0,
        synthetic=True,
    )


# ──────────────────────── per-language verify ──────────────────────────


def _has_script(package_json: Path, script: str) -> bool:
    try:
        data = json.loads(package_json.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return script in (data.get("scripts") or {})


def _script_body(package_json: Path, script: str) -> str:
    try:
        data = json.loads(package_json.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return ""
    return str((data.get("scripts") or {}).get(script) or "")


def _run_background_check(
    name: str,
    cmd: list[str],
    cwd: Path,
    timeout: float = 3.0,
    env: dict[str, str] | None = None,
) -> StepResult:
    # Find a free port dynamically to prevent port collisions (EADDRINUSE)
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            free_port = s.getsockname()[1]
    except Exception:
        free_port = 8999  # fallback

    start = time.monotonic()
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    full_env["PORT"] = str(free_port)

    # Rewrite uvicorn --port parameter if present
    new_cmd = list(cmd)
    for idx, arg in enumerate(new_cmd):
        if arg == "--port" and idx + 1 < len(new_cmd):
            new_cmd[idx + 1] = str(free_port)
        elif arg.startswith("--port="):
            new_cmd[idx] = f"--port={free_port}"

    preexec = None
    if hasattr(os, "setsid"):
        preexec = os.setsid

    try:
        proc = subprocess.Popen(
            new_cmd,
            cwd=cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=full_env,
            preexec_fn=preexec,
        )

        time.sleep(timeout)

        returncode = proc.poll()
        if returncode is None:
            import signal
            terminated = False
            if hasattr(os, "killpg") and hasattr(os, "getpgid") and preexec is not None:
                try:
                    pgid = os.getpgid(proc.pid)
                    os.killpg(pgid, signal.SIGTERM)
                    proc.wait(timeout=2.0)
                    terminated = True
                except Exception:
                    pass

            if not terminated:
                proc.terminate()
                try:
                    proc.wait(timeout=2.0)
                except subprocess.TimeoutExpired:
                    if hasattr(os, "killpg") and hasattr(os, "getpgid") and preexec is not None:
                        try:
                            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                            proc.wait()
                            terminated = True
                        except Exception:
                            pass
                    if not terminated:
                        proc.kill()
                        proc.wait()

            return StepResult(
                name=name,
                ok=True,
                log="Server started successfully and remained active.",
                duration_s=time.monotonic() - start,
                returncode=0,
            )
        else:
            stdout, stderr = proc.communicate()
            log = (stdout or "") + ("\n" + stderr if stderr else "")
            return StepResult(
                name=name,
                ok=returncode == 0,
                log=f"Server exited early with code {returncode}.\nLog output:\n{log}",
                duration_s=time.monotonic() - start,
                returncode=returncode,
            )
    except FileNotFoundError as exc:
        return StepResult(
            name=name,
            ok=False,
            log=f"Command not found: {exc}",
            duration_s=time.monotonic() - start,
            returncode=127,
        )
    except Exception as exc:
        return StepResult(
            name=name,
            ok=False,
            log=f"Unexpected error starting server: {exc}",
            duration_s=time.monotonic() - start,
            returncode=1,
        )


def _python_test_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for pattern in ("**/test_*.py", "**/*_test.py"):
        for p in root.glob(pattern):
            if any(part in _SKIP_DIRS for part in p.parts):
                continue
            out.append(p)
    return out


def _verify_python(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    has_req = (root / "requirements.txt").exists()
    has_pyproject = (root / "pyproject.toml").exists()

    # Create local virtual env to isolate project dependencies
    venv_dir = root / ".venv"
    if not venv_dir.exists() and (has_req or has_pyproject):
        try:
            subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], capture_output=True, check=False)
        except Exception:
            pass

    # Determine pip and python paths
    pip_bin = str(venv_dir / "bin" / "pip") if venv_dir.exists() else None
    python_bin = str(venv_dir / "bin" / "python") if venv_dir.exists() else sys.executable
    if venv_dir.exists() and not Path(python_bin).exists():
        python_bin = sys.executable

    pip = [pip_bin] if pip_bin else [sys.executable, "-m", "pip"]

    # 1. Install runtime deps
    if has_req:
        steps.append(
            run_step(
                "pip install",
                pip + ["install", "-r", "requirements.txt", "--quiet"],
                cwd=root,
                timeout=900,
            )
        )
    if has_pyproject:
        steps.append(
            run_step(
                "pip install -e .[dev]",
                pip + ["install", "-e", ".[dev]", "--quiet"],
                cwd=root,
                timeout=900,
            )
        )

    # Set up PYTHONPATH environment variable
    python_path_dirs = [str(root)]
    if root.name == "backend":
        python_path_dirs.append(str(root.parent))
    if (root / "app").exists():
        python_path_dirs.append(str(root / "app"))

    # Append local venv site-packages so import/test runners can find dependencies
    if venv_dir.exists():
        venv_site = venv_dir / "lib" / f"python{sys.version_info.major}.{sys.version_info.minor}" / "site-packages"
        if venv_site.exists():
            python_path_dirs.append(str(venv_site))

    existing_pythonpath = os.environ.get("PYTHONPATH", "")
    if existing_pythonpath:
        python_path_dirs.append(existing_pythonpath)

    python_env = {"PYTHONPATH": os.pathsep.join(python_path_dirs)}

    # 2. Compile check (syntax check)
    steps.append(
        run_step(
            "python compile",
            [python_bin, "-m", "compileall", "-q", "."],
            cwd=root,
            env=python_env,
        )
    )

    # 3. Import and Runnable check
    main_py = root / "app" / "main.py"
    import_mod = "app.main"
    if not main_py.exists():
        main_py = root / "main.py"
        import_mod = "main"

    if main_py.exists():
        # First check imports
        steps.append(
            run_step(
                "python import check",
                [python_bin, "-c", f"import {import_mod}"],
                cwd=root,
                timeout=15,
                env=python_env,
            )
        )

        # Second, try starting the server if uvicorn is used
        has_uvicorn = False
        try:
            req_content = ""
            if (root / "requirements.txt").exists():
                req_content += (root / "requirements.txt").read_text("utf-8")
            if (root / "pyproject.toml").exists():
                req_content += (root / "pyproject.toml").read_text("utf-8")
            if "uvicorn" in req_content.lower():
                has_uvicorn = True
        except Exception:
            pass

        if has_uvicorn:
            steps.append(
                _run_background_check(
                    "python server start check",
                    [python_bin, "-m", "uvicorn", f"{import_mod}:app", "--host", "127.0.0.1", "--port", "8999"],
                    cwd=root,
                    timeout=3.0,
                    env=python_env,
                )
            )
        else:
            steps.append(
                _run_background_check(
                    "python script run check",
                    [python_bin, str(main_py.relative_to(root))],
                    cwd=root,
                    timeout=3.0,
                    env=python_env,
                )
            )

    # 4. Run tests. No test files means tests_ok=False — never "not required".
    test_files = _python_test_files(root)
    if not test_files:
        steps.append(
            missing_tests_step(
                project.kind,
                f"no test files found under {root} (looked for test_*.py and *_test.py)",
            )
        )
    else:
        probe = run_step(
            "pytest availability probe",
            [python_bin, "-m", "pytest", "--version"],
            cwd=root, timeout=120, env=python_env,
        )
        runner_bin = python_bin
        if not probe.ok:
            # Fall back to the interpreter running sage, which is known to
            # have pytest, before declaring the runner absent.
            probe2 = run_step(
                "pytest availability probe (host interpreter)",
                [sys.executable, "-m", "pytest", "--version"],
                cwd=root, timeout=120, env=python_env,
            )
            if probe2.ok:
                runner_bin = sys.executable
            else:
                steps.append(
                    missing_tests_step(
                        project.kind,
                        f"{len(test_files)} test file(s) exist but pytest is not installed "
                        f"in {python_bin} or {sys.executable}. Runner log:\n{probe.log[-400:]}",
                    )
                )
                runner_bin = None
        if runner_bin is not None:
            steps.append(
                run_test_step(
                    "pytest",
                    [runner_bin, "-m", "pytest", "-q"],
                    cwd=root,
                    env=python_env,
                )
            )

    # 5. Lint
    ruff_paths = [
        root / ".venv" / "bin" / "ruff",
        root / "venv" / "bin" / "ruff",
        root / ".venv" / "Scripts" / "ruff.exe",
        root / "venv" / "Scripts" / "ruff.exe",
        root / ".venv" / "Scripts" / "ruff",
        root / "venv" / "Scripts" / "ruff",
    ]
    if shutil.which("ruff") or any(p.exists() for p in ruff_paths):
        steps.append(run_step("ruff check", ["ruff", "check", "."], cwd=root, env=python_env))
    return steps


def _node_test_files(root: Path) -> list[Path]:
    out: list[Path] = []
    for pattern in (
        "**/*.test.js", "**/*.test.ts", "**/*.test.jsx", "**/*.test.tsx",
        "**/*.spec.js", "**/*.spec.ts", "**/*.spec.jsx", "**/*.spec.tsx",
    ):
        for p in root.glob(pattern):
            if any(part in _SKIP_DIRS for part in p.parts):
                continue
            out.append(p)
    return out


# npm's default placeholder test script — running it proves nothing.
_NPM_PLACEHOLDER = re.compile(r"no test specified|exit\s+1\s*$", re.IGNORECASE)


def _verify_node(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    pkg = root / "package.json"

    # Detect if Bun is the target runtime
    is_bun = False
    if shutil.which("bun"):
        if (root / "bun.lockb").exists() or (root / "bun.lock").exists() or (root / "bunfig.toml").exists():
            is_bun = True
        else:
            try:
                pkg_data = json.loads(pkg.read_text("utf-8", errors="replace"))
                if "bun" in pkg_data.get("packageManager", ""):
                    is_bun = True
                else:
                    scripts = pkg_data.get("scripts", {})
                    if any("bun" in str(v) for v in scripts.values()):
                        is_bun = True
            except Exception:
                pass

    pm = "bun" if is_bun else "npm"

    # 1. Install
    if is_bun:
        steps.append(
            run_step(
                "bun install",
                ["bun", "install"],
                cwd=root,
                timeout=1200,
            )
        )
    else:
        steps.append(
            run_step(
                "npm install",
                ["npm", "install", "--no-audit", "--no-fund"],
                cwd=root,
                timeout=1200,
            )
        )

    # 2. Build check
    if _has_script(pkg, "build"):
        steps.append(run_step(f"{pm} build", [pm, "run", "build"], cwd=root, timeout=600))

    # 3. Runnable check
    run_cmd = None
    if _has_script(pkg, "start"):
        run_cmd = [pm, "run", "start"]
    elif _has_script(pkg, "dev"):
        run_cmd = [pm, "run", "dev"]

    if run_cmd:
        steps.append(
            _run_background_check(
                f"{pm} server start check",
                run_cmd,
                cwd=root,
                timeout=4.0,
            )
        )
    else:
        # Check if there is a main file entrypoint to check compilation/loading
        main_entry = None
        for fn in ("index.js", "main.js", "src/index.ts", "src/main.ts"):
            if (root / fn).exists():
                main_entry = fn
                break
        if main_entry:
            steps.append(run_step("node load check", ["node", main_entry], cwd=root, timeout=15))
        else:
            steps.append(
                StepResult(
                    name=f"{pm} server start check (not required)",
                    ok=True,
                    log="No 'start' or 'dev' script, and no main entrypoint found in package.json",
                    duration_s=0.0,
                    synthetic=True,
                )
            )

    # 4. Test — a missing or placeholder script is a FAILURE, not a pass.
    test_files = _node_test_files(root)
    if not _has_script(pkg, "test"):
        steps.append(
            missing_tests_step(
                project.kind,
                f"package.json has no \"test\" script ({len(test_files)} test file(s) on disk). "
                "Add a real test script (jest/vitest/node --test) so the suite can run.",
            )
        )
    elif _NPM_PLACEHOLDER.search(_script_body(pkg, "test").strip()):
        steps.append(
            missing_tests_step(
                project.kind,
                'package.json "test" script is npm\'s placeholder '
                f'({_script_body(pkg, "test")!r}) — it runs no tests.',
            )
        )
    elif not test_files:
        steps.append(
            missing_tests_step(
                project.kind,
                'a "test" script is configured but no *.test.* / *.spec.* files exist to run.',
            )
        )
    elif is_bun:
        steps.append(run_test_step("bun test", ["bun", "test"], cwd=root))
    else:
        # `--watchAll=false` is a jest/react-scripts flag. Passing it
        # unconditionally BREAKS every other runner ("node: bad option:
        # --watchAll=false" with `node --test`, and likewise for mocha/ava/
        # vitest), which turned a genuinely passing suite into a failure.
        # Only add it when the configured script really is jest-based.
        _script = _script_body(pkg, "test").lower()
        _deps: dict = {}
        try:
            _pkg_data = json.loads(pkg.read_text("utf-8", errors="replace"))
            _deps = {
                **_pkg_data.get("devDependencies", {}),
                **_pkg_data.get("dependencies", {}),
            }
        except Exception:
            pass
        _is_jest = (
            "jest" in _script
            or "react-scripts" in _script
            or ("jest" in _deps and "vitest" not in _script)
        )
        _test_cmd = ["npm", "test", "--silent"]
        if _is_jest and "--watchall" not in _script:
            _test_cmd += ["--", "--watchAll=false"]
        # CI=1 is the conventional signal that keeps every JS runner out of
        # interactive watch mode.
        steps.append(run_test_step("npm test", _test_cmd, cwd=root, env={"CI": "1"}))

    # 5. Typecheck
    if _has_script(pkg, "typecheck"):
        steps.append(run_step(f"{pm} typecheck", [pm, "run", "typecheck"], cwd=root))

    # 6. Lint
    if _has_script(pkg, "lint"):
        steps.append(run_step(f"{pm} lint", [pm, "run", "lint"], cwd=root))

    return steps


def _verify_go(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    if not shutil.which("go"):
        steps.append(StepResult("go mod tidy", False, "go toolchain not found in PATH", 0.0, 127))
        steps.append(missing_tests_step(project.kind, "the go toolchain is not installed, so `go test` could not run"))
        return steps
    steps.append(run_step("go mod tidy", ["go", "mod", "tidy"], cwd=root))
    steps.append(run_step("go build", ["go", "build", "./..."], cwd=root))
    # -v so per-test RUN/PASS lines are available for counting; `go test`
    # exits 0 for packages with no test files at all.
    steps.append(run_test_step("go test", ["go", "test", "-v", "./..."], cwd=root))
    return steps


def _verify_rust(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    if not shutil.which("cargo"):
        steps.append(StepResult("cargo build", False, "cargo not found in PATH", 0.0, 127))
        steps.append(missing_tests_step(project.kind, "cargo is not installed, so `cargo test` could not run"))
        return steps
    steps.append(run_step("cargo build", ["cargo", "build", "--quiet"], cwd=root, timeout=900))
    # NOT --quiet: we need the "running N tests" lines to detect an empty suite.
    steps.append(run_test_step("cargo test", ["cargo", "test"], cwd=root, timeout=900))
    return steps


def _verify_java(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    if (root / "pom.xml").exists():
        if shutil.which("mvn"):
            steps.append(run_step("mvn compile", ["mvn", "compile"], cwd=root))
            steps.append(run_test_step("mvn test", ["mvn", "test"], cwd=root))
        else:
            steps.append(StepResult("mvn compile", False, "mvn command not found in path", 0.0, 127))
            steps.append(missing_tests_step(project.kind, "maven is not installed, so `mvn test` could not run"))
    elif root.is_dir() and any(f.startswith("build.gradle") for f in os.listdir(root)):
        gradlew = root / "gradlew"
        cmd_prefix = [str(gradlew)] if gradlew.exists() else ["gradle"]
        if gradlew.exists() and not os.access(gradlew, os.X_OK):
            try:
                os.chmod(gradlew, 0o755)
            except Exception:
                pass
        steps.append(run_step("gradle build", cmd_prefix + ["build", "-x", "test"], cwd=root))
        steps.append(run_test_step("gradle test", cmd_prefix + ["test"], cwd=root))
    else:
        steps.append(StepResult("java build", False, "No pom.xml or build.gradle found", 0.0, 1))
        steps.append(missing_tests_step(project.kind, "no maven/gradle project was found to run tests from"))

    return steps


def _verify_kotlin(project: DiscoveredProject) -> list[StepResult]:
    return _verify_java(project)


def _verify_ruby(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    if not shutil.which("bundle"):
        steps.append(StepResult("bundle install", False, "bundle command not found in path", 0.0, 127))
        steps.append(missing_tests_step(project.kind, "bundler is not installed, so the ruby suite could not run"))
        return steps

    steps.append(run_step("bundle install", ["bundle", "install"], cwd=root, timeout=600))
    if (root / "spec").is_dir():
        steps.append(run_test_step("rspec", ["bundle", "exec", "rspec"], cwd=root))
    elif (root / "Rakefile").exists():
        steps.append(run_test_step("rake test", ["bundle", "exec", "rake", "test"], cwd=root))
    elif (root / "test").is_dir():
        steps.append(
            run_test_step("ruby test", ["bundle", "exec", "rake", "test"], cwd=root)
        )
    else:
        steps.append(
            missing_tests_step(project.kind, "no spec/ or test/ directory and no Rakefile — nothing to run")
        )

    return steps


def _verify_swift(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    if not shutil.which("swift"):
        steps.append(StepResult("swift build", False, "swift command not found in path", 0.0, 127))
        steps.append(missing_tests_step(project.kind, "the swift toolchain is not installed"))
        return steps

    steps.append(run_step("swift build", ["swift", "build"], cwd=root, timeout=900))
    tests_dir = root / "Tests"
    if not tests_dir.is_dir():
        steps.append(
            missing_tests_step(
                project.kind,
                "no Tests/ directory — SwiftPM has no test target to run",
            )
        )
    else:
        steps.append(run_test_step("swift test", ["swift", "test"], cwd=root, timeout=900))
    return steps


def _verify_dart(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    is_flutter = False
    try:
        pubspec = root / "pubspec.yaml"
        if pubspec.exists():
            content = pubspec.read_text(encoding="utf-8", errors="replace")
            if "sdk: flutter" in content or "flutter:" in content:
                is_flutter = True
    except Exception:
        pass

    tool = "flutter" if is_flutter else "dart"

    if not shutil.which(tool):
        steps.append(StepResult(f"{tool} pub get", False, f"{tool} command not found in path", 0.0, 127))
        steps.append(missing_tests_step(project.kind, f"{tool} is not installed, so `{tool} test` could not run"))
        return steps

    steps.append(run_step(f"{tool} pub get", [tool, "pub", "get"], cwd=root, timeout=600))
    if not (root / "test").is_dir():
        steps.append(missing_tests_step(project.kind, "no test/ directory — nothing for `dart test` to run"))
    else:
        steps.append(run_test_step(f"{tool} test", [tool, "test"], cwd=root))

    return steps


def _verify_cpp(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    if (root / "CMakeLists.txt").exists():
        if not shutil.which("cmake"):
            steps.append(StepResult("cmake configure", False, "cmake command not found in path", 0.0, 127))
            steps.append(missing_tests_step(project.kind, "cmake is not installed, so ctest could not run"))
            return steps
        build_dir = root / "build"
        build_dir.mkdir(exist_ok=True)
        steps.append(run_step("cmake configure", ["cmake", ".."], cwd=build_dir))
        steps.append(run_step("cmake build", ["cmake", "--build", "."], cwd=build_dir))
        cmake_txt = ""
        try:
            cmake_txt = (root / "CMakeLists.txt").read_text("utf-8", errors="replace")
        except OSError:
            pass
        if "add_test" not in cmake_txt and "enable_testing" not in cmake_txt:
            steps.append(
                missing_tests_step(
                    project.kind,
                    "CMakeLists.txt declares neither enable_testing() nor add_test() — "
                    "ctest would find no tests",
                )
            )
        else:
            steps.append(run_test_step("ctest", ["ctest", "--output-on-failure"], cwd=build_dir))
    elif (root / "Makefile").exists() or (root / "makefile").exists():
        if not shutil.which("make"):
            steps.append(StepResult("make", False, "make command not found in path", 0.0, 127))
            steps.append(missing_tests_step(project.kind, "make is not installed"))
            return steps
        steps.append(run_step("make", ["make"], cwd=root))
        makefile = root / "Makefile" if (root / "Makefile").exists() else root / "makefile"
        body = ""
        try:
            body = makefile.read_text("utf-8", errors="replace")
        except OSError:
            pass
        if not re.search(r"^\.?test\s*:", body, re.MULTILINE) and not re.search(r"^test:", body, re.MULTILINE):
            steps.append(
                missing_tests_step(project.kind, "Makefile declares no `test` target — nothing to run")
            )
        else:
            steps.append(run_test_step("make test", ["make", "test"], cwd=root))
    else:
        steps.append(StepResult("cpp build", False, "No CMakeLists.txt or Makefile found", 0.0, 1))
        steps.append(missing_tests_step(project.kind, "no CMake/Make build was found, so no tests could run"))

    return steps


def _verify_csharp(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root

    if not shutil.which("dotnet"):
        steps.append(StepResult("dotnet build", False, "dotnet command not found in path", 0.0, 127))
        steps.append(missing_tests_step(project.kind, "the dotnet SDK is not installed, so `dotnet test` could not run"))
        return steps

    steps.append(run_step("dotnet build", ["dotnet", "build"], cwd=root, timeout=900))
    steps.append(run_test_step("dotnet test", ["dotnet", "test"], cwd=root, timeout=900))
    return steps


_HTML_TAG = re.compile(r"<\s*(html|body|main|div|section|h1|p|script)\b", re.IGNORECASE)


def _verify_static_web(project: DiscoveredProject) -> list[StepResult]:
    """A hand-written static site: no package.json, just HTML/CSS/JS.

    install/build are genuinely not applicable, but the HTML is still
    checked for real structure, and the absence of a test runner is
    reported as a FAILURE rather than waved through.
    """
    steps: list[StepResult] = []
    root = project.root
    html_files = [
        p for p in root.rglob("*.html")
        if not any(part in _SKIP_DIRS for part in p.parts)
    ]

    problems: list[str] = []
    for p in sorted(html_files):
        try:
            text = p.read_text("utf-8", errors="replace")
        except OSError as exc:
            problems.append(f"{p.name}: unreadable ({exc})")
            continue
        if not text.strip():
            problems.append(f"{p.name}: file is empty")
            continue
        if not _HTML_TAG.search(text):
            problems.append(f"{p.name}: contains no HTML elements at all")
            continue
        for tag in ("html", "body"):
            opens = len(re.findall(rf"<\s*{tag}\b", text, re.IGNORECASE))
            closes = len(re.findall(rf"<\s*/\s*{tag}\s*>", text, re.IGNORECASE))
            if opens and opens != closes:
                problems.append(f"{p.name}: <{tag}> opened {opens}x but closed {closes}x")

    steps.append(
        StepResult(
            name="html compile (structure check)",
            ok=not problems and bool(html_files),
            log="\n".join(problems) if problems else f"{len(html_files)} HTML file(s) structurally valid",
            duration_s=0.0,
            returncode=0 if (not problems and html_files) else 1,
        )
    )
    steps.append(
        StepResult(
            name="html load check",
            ok=bool(html_files) and not problems,
            log=(
                f"index.html present and parseable"
                if html_files and not problems
                else "no loadable HTML entrypoint"
            ),
            duration_s=0.0,
            returncode=0 if (html_files and not problems) else 1,
        )
    )

    js_tests = [
        p for p in root.rglob("*")
        if p.is_file()
        and not any(part in _SKIP_DIRS for part in p.parts)
        and re.search(r"\.(test|spec)\.(js|mjs|ts)$", p.name)
    ]
    if js_tests and shutil.which("node"):
        steps.append(
            run_test_step(
                "node test", ["node", "--test"], cwd=root, timeout=300,
            )
        )
    elif js_tests and not shutil.which("node"):
        steps.append(
            missing_tests_step(
                project.kind,
                f"{len(js_tests)} test file(s) found but node is not installed to run them",
            )
        )
    else:
        steps.append(
            missing_tests_step(
                project.kind,
                "static site has no test runner: no *.test.js / *.spec.js files and no "
                "package.json test script. Add a node --test suite (or a package.json) so "
                "the page's behaviour is actually asserted.",
            )
        )
    return steps


_VERIFIERS = {
    "python": _verify_python,
    "node": _verify_node,
    "go": _verify_go,
    "rust": _verify_rust,
    "java": _verify_java,
    "kotlin": _verify_kotlin,
    "ruby": _verify_ruby,
    "swift": _verify_swift,
    "dart": _verify_dart,
    "cpp": _verify_cpp,
    "csharp": _verify_csharp,
    "static-web": _verify_static_web,
}


def verify_project(project: DiscoveredProject) -> list[StepResult]:
    """Run install + build + run + test + lint for ONE project.

    All four quadrant slots are always represented in the returned steps so
    `VerifyReport` can report on each. install/build/run may legitimately be
    "not applicable" for some project kinds and are synthesized as passing
    in that case. The TEST slot is NEVER synthesized as passing: a project
    with no test run is reported as a FAILURE.
    """
    fn = _VERIFIERS.get(project.kind)
    if not fn:
        steps = [
            StepResult(
                name=f"{project.kind} verifier",
                ok=False,
                log=f"no verifier registered for {project.kind}",
                duration_s=0.0,
                returncode=1,
            )
        ]
    else:
        steps = fn(project)

    has_install = any(_matches(s.name, _INSTALL_TERMS) for s in steps)
    has_build = any(_matches(s.name, _BUILD_TERMS) and not is_test_step(s.name) for s in steps)
    has_run = any(_matches(s.name, _RUN_TERMS) for s in steps)
    has_test = any(is_test_step(s.name) for s in steps)

    if not has_install:
        steps.append(
            StepResult(
                name=f"{project.kind} install (not required)",
                ok=True,
                log="No install step required for this project kind",
                duration_s=0.0,
                synthetic=True,
            )
        )
    if not has_build:
        steps.append(
            StepResult(
                name=f"{project.kind} build (not required)",
                ok=True,
                log="No build step required for this project kind",
                duration_s=0.0,
                synthetic=True,
            )
        )
    if not has_run:
        steps.append(
            StepResult(
                name=f"{project.kind} run check (not required)",
                ok=True,
                log="No run check required for this project kind",
                duration_s=0.0,
                synthetic=True,
            )
        )
    if not has_test:
        # NEVER a passing placeholder. A verifier that produced no test step
        # verified no tests, and that is a failure.
        steps.append(
            missing_tests_step(
                project.kind,
                f"the {project.kind} verifier produced no test step, so no tests were run",
            )
        )

    return steps


def verify_all(root: Path, *, include_media: bool = True) -> list[VerifyReport]:
    """Discover every project under `root` and verify each.

    When `include_media` is set and media assets are present, one extra
    report of kind "media" is appended whose test step is the real
    magic-byte/container verification from `sage.core.media_verify`. That
    makes a 0-byte or wrong-format asset fail the quadrant instead of being
    invisible to it.
    """
    reports: list[VerifyReport] = []
    for project in discover_projects(root):
        steps = verify_project(project)
        reports.append(VerifyReport(project=project, steps=steps))

    if include_media:
        media_report = verify_media_report(root)
        if media_report is not None:
            reports.append(media_report)

    return reports


def verify_media_report(root: Path) -> VerifyReport | None:
    """Verify every media asset under `root` as a quadrant report.

    Returns None when there are no media assets to check.
    """
    from sage.core.media_verify import verify_media_assets

    start = time.monotonic()
    checks = verify_media_assets(root)
    if not checks:
        return None

    failed = [c for c in checks if not c.ok]
    lines = [str(c) for c in checks]
    project = DiscoveredProject(kind="media", root=Path(root))  # type: ignore[arg-type]
    steps = [
        StepResult(
            name="media install (not required)",
            ok=True,
            log="Media assets have no dependencies to install",
            duration_s=0.0,
            synthetic=True,
        ),
        StepResult(
            name="media build (magic-byte + container check)",
            ok=not failed,
            log="\n".join(lines),
            duration_s=time.monotonic() - start,
            returncode=0 if not failed else 1,
        ),
        StepResult(
            name="media run check (decodable)",
            ok=not failed,
            log=(
                f"{len(checks)} asset(s) decodable"
                if not failed
                else f"{len(failed)} asset(s) are not decodable:\n"
                + "\n".join(str(c) for c in failed)
            ),
            duration_s=0.0,
            returncode=0 if not failed else 1,
        ),
        StepResult(
            name="media asset test (structural verification)",
            ok=not failed,
            log=(
                f"all {len(checks)} media asset(s) verified: correct magic bytes, "
                "non-trivial size, parseable container\n" + "\n".join(lines)
                if not failed
                else f"{len(failed)}/{len(checks)} media asset(s) FAILED verification:\n"
                + "\n".join(str(c) for c in failed)
            ),
            duration_s=0.0,
            returncode=0 if not failed else 1,
            tests_collected=len(checks),
        ),
    ]
    return VerifyReport(project=project, steps=steps)


__all__ = [
    "DiscoveredProject",
    "ProjectKind",
    "StepResult",
    "VerifyReport",
    "count_tests_executed",
    "discover_projects",
    "is_test_step",
    "missing_tests_step",
    "run_step",
    "run_test_step",
    "verify_all",
    "verify_media_report",
    "verify_project",
]
