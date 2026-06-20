"""Install + verify orchestrator.

Discovers every project under a root directory and runs the appropriate
toolchain (install → test → lint → typecheck → format) against each one.
Captures stdout+stderr per step in structured `StepResult` records the
verify loop in `build_project` can feed back to the LLM for fixes.

This module is the answer to the user's complaint that "neither the
frontend nor backend was installed by sage in order to test and run the
code" and "How can sage test its code if it never installed its code."
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal


ProjectKind = Literal["python", "node", "go", "rust", "java", "kotlin", "ruby", "swift", "dart", "cpp", "csharp"]


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


@dataclass
class VerifyReport:
    project: DiscoveredProject
    steps: list[StepResult]

    @property
    def install_ok(self) -> bool | None:
        for s in self.steps:
            name_lower = s.name.lower()
            if "install" in name_lower or "tidy" in name_lower or "restore" in name_lower:
                return s.ok
        return None

    @property
    def build_ok(self) -> bool | None:
        for s in self.steps:
            name_lower = s.name.lower()
            if any(term in name_lower for term in {"build", "compile", "make"}):
                return s.ok
        return None

    @property
    def runs_ok(self) -> bool | None:
        for s in self.steps:
            name_lower = s.name.lower()
            if any(term in name_lower for term in {"run check", "start check", "import check"}):
                return s.ok
        return None

    @property
    def tests_ok(self) -> bool | None:
        for s in self.steps:
            name_lower = s.name.lower()
            if any(term in name_lower for term in {"test", "pytest", "rspec", "ctest"}):
                return s.ok
        return None

    @property
    def all_ok(self) -> bool:
        return all(s.ok for s in self.steps)


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
    """Run a shell command and capture the result. Never raises."""
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    
    if os.environ.get("SAGE_TESTING") == "1" and os.environ.get("SAGE_REAL_COMMANDS") != "1":
        return StepResult(
            name=name,
            ok=True,
            log="[SAGE_TESTING] Mocked execution of command: " + " ".join(cmd),
            duration_s=0.01,
            returncode=0,
        )
            
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


# ──────────────────────── per-language verify ──────────────────────────


def _has_script(package_json: Path, script: str) -> bool:
    try:
        data = json.loads(package_json.read_text("utf-8"))
    except (OSError, json.JSONDecodeError):
        return False
    return script in (data.get("scripts") or {})


def _run_background_check(
    name: str,
    cmd: list[str],
    cwd: Path,
    timeout: float = 3.0,
    env: dict[str, str] | None = None,
) -> StepResult:
    if os.environ.get("SAGE_TESTING") == "1" and os.environ.get("SAGE_REAL_COMMANDS") != "1":
        return StepResult(
            name=name,
            ok=True,
            log="[SAGE_TESTING] Mocked background execution of command: " + " ".join(cmd),
            duration_s=0.01,
            returncode=0,
        )
        
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

    # 4. Run tests (only if tests directory or test files exist)
    has_test_files = any(root.glob("**/test_*.py")) or any(root.glob("**/*_test.py"))
    if has_test_files:
        res_step = run_step(
            "pytest",
            [sys.executable, "-m", "pytest", "-q"],
            cwd=root,
            env=python_env,
        )
        # pytest exit code 5 means no tests were collected, which is fine, but code 0 is success
        if res_step.returncode in (0, 5):
            res_step = StepResult(res_step.name, True, res_step.log, res_step.duration_s, res_step.returncode)
        steps.append(res_step)

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
                )
            )


    # 4. Test (only if defined)
    if _has_script(pkg, "test"):
        if is_bun:
            steps.append(run_step("bun test", ["bun", "test"], cwd=root))
        else:
            _is_vitest = False
            try:
                _pkg_data = json.loads(pkg.read_text("utf-8", errors="replace"))
                _deps = {
                    **_pkg_data.get("devDependencies", {}),
                    **_pkg_data.get("dependencies", {}),
                }
                _is_vitest = "vitest" in _deps
            except Exception:
                pass
            _test_cmd = (
                ["npm", "test", "--silent"]
                if _is_vitest
                else ["npm", "test", "--silent", "--", "--watchAll=false"]
            )
            steps.append(run_step("npm test", _test_cmd, cwd=root))

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
    steps.append(run_step("go mod tidy", ["go", "mod", "tidy"], cwd=root))
    steps.append(run_step("go build", ["go", "build", "./..."], cwd=root))
    steps.append(run_step("go test", ["go", "test", "./..."], cwd=root))
    return steps


def _verify_rust(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    steps.append(run_step("cargo build", ["cargo", "build", "--quiet"], cwd=root))
    steps.append(run_step("cargo test", ["cargo", "test", "--quiet"], cwd=root))
    return steps


def _verify_java(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    
    if (root / "pom.xml").exists():
        if shutil.which("mvn"):
            steps.append(run_step("mvn compile", ["mvn", "compile"], cwd=root))
            steps.append(run_step("mvn test", ["mvn", "test"], cwd=root))
        else:
            steps.append(StepResult("mvn compile", False, "mvn command not found in path", 0.0, 127))
    elif any(f.startswith("build.gradle") for f in os.listdir(root)):
        gradlew = root / "gradlew"
        cmd_prefix = [str(gradlew)] if gradlew.exists() else ["gradle"]
        if gradlew.exists() and not os.access(gradlew, os.X_OK):
            try:
                os.chmod(gradlew, 0o755)
            except Exception:
                pass
        steps.append(run_step("gradle build", cmd_prefix + ["build", "-x", "test"], cwd=root))
        steps.append(run_step("gradle test", cmd_prefix + ["test"], cwd=root))
    else:
        steps.append(StepResult("java build", False, "No pom.xml or build.gradle found", 0.0, 1))
        
    return steps


def _verify_kotlin(project: DiscoveredProject) -> list[StepResult]:
    return _verify_java(project)


def _verify_ruby(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    
    if shutil.which("bundle"):
        steps.append(run_step("bundle install", ["bundle", "install"], cwd=root, timeout=600))
        if (root / "Rakefile").exists():
            steps.append(run_step("rake test", ["bundle", "exec", "rake", "test"], cwd=root))
        elif (root / "spec").is_dir():
            steps.append(run_step("rspec", ["bundle", "exec", "rspec"], cwd=root))
        else:
            steps.append(run_step("ruby test", ["ruby", "-Ilib:test", "test/test_*.rb"], cwd=root))
    else:
        steps.append(StepResult("bundle install", False, "bundle command not found in path", 0.0, 127))
        
    return steps


def _verify_swift(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    
    if shutil.which("swift"):
        steps.append(run_step("swift build", ["swift", "build"], cwd=root, timeout=600))
        steps.append(run_step("swift test", ["swift", "test"], cwd=root))
    else:
        steps.append(StepResult("swift build", False, "swift command not found in path", 0.0, 127))
        
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
    
    if shutil.which(tool):
        steps.append(run_step(f"{tool} pub get", [tool, "pub", "get"], cwd=root, timeout=600))
        steps.append(run_step(f"{tool} test", [tool, "test"], cwd=root))
    else:
        steps.append(StepResult(f"{tool} pub get", False, f"{tool} command not found in path", 0.0, 127))
        
    return steps


def _verify_cpp(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    
    if (root / "CMakeLists.txt").exists():
        build_dir = root / "build"
        build_dir.mkdir(exist_ok=True)
        if shutil.which("cmake"):
            steps.append(run_step("cmake configure", ["cmake", ".."], cwd=build_dir))
            steps.append(run_step("cmake build", ["cmake", "--build", "."], cwd=build_dir))
            steps.append(run_step("ctest", ["ctest"], cwd=build_dir))
        else:
            steps.append(StepResult("cmake configure", False, "cmake command not found in path", 0.0, 127))
    elif (root / "Makefile").exists() or (root / "makefile").exists():
        if shutil.which("make"):
            steps.append(run_step("make", ["make"], cwd=root))
            steps.append(run_step("make test", ["make", "test"], cwd=root))
        else:
            steps.append(StepResult("make", False, "make command not found in path", 0.0, 127))
    else:
        steps.append(StepResult("cpp build", False, "No CMakeLists.txt or Makefile found", 0.0, 1))
        
    return steps


def _verify_csharp(project: DiscoveredProject) -> list[StepResult]:
    steps: list[StepResult] = []
    root = project.root
    
    if shutil.which("dotnet"):
        steps.append(run_step("dotnet build", ["dotnet", "build"], cwd=root, timeout=600))
        steps.append(run_step("dotnet test", ["dotnet", "test"], cwd=root))
    else:
        steps.append(StepResult("dotnet build", False, "dotnet command not found in path", 0.0, 127))
        
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
}


def verify_project(project: DiscoveredProject) -> list[StepResult]:
    """Run install + test + lint for ONE project. Steps gated on tool/script availability."""
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

    # Post-process to ensure all 4 verification checks are represented
    has_install = False
    has_build = False
    has_run = False
    has_test = False

    for s in steps:
        name_lower = s.name.lower()
        if "install" in name_lower or "tidy" in name_lower or "restore" in name_lower:
            has_install = True
        if any(term in name_lower for term in {"build", "compile", "make"}):
            has_build = True
        if any(term in name_lower for term in {"run check", "start check", "import check"}):
            has_run = True
        if any(term in name_lower for term in {"test", "pytest", "rspec", "ctest"}):
            has_test = True

    if not has_install:
        steps.append(
            StepResult(
                name=f"{project.kind} install (not required)",
                ok=True,
                log="No install step required for this project kind",
                duration_s=0.0,
            )
        )
    if not has_build:
        steps.append(
            StepResult(
                name=f"{project.kind} build (not required)",
                ok=True,
                log="No build step required for this project kind",
                duration_s=0.0,
            )
        )
    if not has_run:
        steps.append(
            StepResult(
                name=f"{project.kind} run check (not required)",
                ok=True,
                log="No run check required for this project kind",
                duration_s=0.0,
            )
        )
    if not has_test:
        steps.append(
            StepResult(
                name=f"{project.kind} test (not required)",
                ok=True,
                log="No test suite configured for this project kind",
                duration_s=0.0,
            )
        )

    return steps


def verify_all(root: Path) -> list[VerifyReport]:
    """Discover every project under `root` and verify each."""
    reports: list[VerifyReport] = []
    for project in discover_projects(root):
        steps = verify_project(project)
        reports.append(VerifyReport(project=project, steps=steps))
    return reports


__all__ = [
    "DiscoveredProject",
    "ProjectKind",
    "StepResult",
    "VerifyReport",
    "discover_projects",
    "run_step",
    "verify_all",
    "verify_project",
]
