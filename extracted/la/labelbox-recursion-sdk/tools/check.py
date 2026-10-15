"""Run the independent Python SDK's complete qualification through uv."""

from __future__ import annotations

import hashlib
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
GENERATED_ROOT = PACKAGE_ROOT / "src/recursion_sdk/_generated"
DISTRIBUTION_ROOT = PACKAGE_ROOT / "dist"
DISTRIBUTION_NAME = "labelbox-recursion-sdk"
NORMALIZED_DISTRIBUTION_NAME = DISTRIBUTION_NAME.replace("-", "_")
UV_PROJECT_COMMAND = (
    "uv",
    "run",
    "--locked",
    "--project",
    str(PACKAGE_ROOT),
    "--group",
    "dev",
    "--no-sync",
)


def run(*arguments: str) -> None:
    print(f"+ {shlex.join(arguments)}", flush=True)
    subprocess.run(arguments, cwd=PACKAGE_ROOT, check=True)


def generated_fingerprints() -> dict[str, str]:
    return {
        str(path.relative_to(GENERATED_ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(GENERATED_ROOT.rglob("*"))
        if path.is_file() and path.suffix in {".py", ".json"}
    }


def main() -> None:
    generator = str(PACKAGE_ROOT / "tools/generate.py")
    run(*UV_PROJECT_COMMAND, "--script", generator)
    original = generated_fingerprints()
    if not original:
        raise RuntimeError("Generation produced no Python SDK artifacts")
    run(*UV_PROJECT_COMMAND, "--script", generator)
    if generated_fingerprints() != original:
        raise RuntimeError("Python SDK generation is not deterministic")
    run(*UV_PROJECT_COMMAND, "ruff", "check", "src", "tools", "tests")
    run(*UV_PROJECT_COMMAND, "ruff", "format", "--check", "src", "tools", "tests")
    run(*UV_PROJECT_COMMAND, "mypy")
    run(*UV_PROJECT_COMMAND, "pytest")
    if DISTRIBUTION_ROOT.exists():
        shutil.rmtree(DISTRIBUTION_ROOT)
    run("uv", "build", "--project", str(PACKAGE_ROOT), "--out-dir", str(DISTRIBUTION_ROOT))
    wheels = list(DISTRIBUTION_ROOT.glob(f"{NORMALIZED_DISTRIBUTION_NAME}-*.whl"))
    source_archives = list(DISTRIBUTION_ROOT.glob(f"{NORMALIZED_DISTRIBUTION_NAME}-*.tar.gz"))
    if len(wheels) != 1 or len(source_archives) != 1:
        raise RuntimeError("Expected exactly one wheel and one source distribution")
    with tempfile.TemporaryDirectory(prefix=".wheel-check-", dir=DISTRIBUTION_ROOT) as directory:
        runtime_root = Path(directory)
        requirements = runtime_root / "requirements.txt"
        run(
            "uv",
            "export",
            "--locked",
            "--project",
            str(PACKAGE_ROOT),
            "--no-default-groups",
            "--no-emit-project",
            "--output-file",
            str(requirements),
        )
        wheel = wheels[0]
        wheel_hash = hashlib.sha256(wheel.read_bytes()).hexdigest()
        with requirements.open("a") as output:
            output.write(f"\n{DISTRIBUTION_NAME} @ {wheel.as_uri()} --hash=sha256:{wheel_hash}\n")
        environment = runtime_root / "environment"
        run("uv", "venv", "--no-project", "--python", sys.executable, str(environment))
        interpreter = environment / (
            "Scripts/python.exe" if sys.platform == "win32" else "bin/python"
        )
        run(
            "uv",
            "pip",
            "install",
            "--python",
            str(interpreter),
            "--require-hashes",
            "--requirements",
            str(requirements),
        )
        run(
            "uv",
            "run",
            "--no-project",
            "--offline",
            "--python",
            str(interpreter),
            "--script",
            str(PACKAGE_ROOT / "tools/verify_distribution.py"),
            str(wheel),
            str(source_archives[0]),
        )


if __name__ == "__main__":
    main()
