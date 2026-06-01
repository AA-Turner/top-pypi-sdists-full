import os
import shutil
import subprocess
import sys
from platform import uname

from .wheel import (
    check_docker,
    get_platform,
    get_python_image,
    get_python_interpreter,
)


def build_executable(
    package: str,
    arch: str,
    libc: str,
    python: str,
    setup: str | None,
    teardown: str | None,
    no_compress: bool,
    lto: bool,
) -> None:
    if not check_docker():
        print("Error: Docker is not available", file=sys.stderr)
        sys.exit(1)

    exename = f"{package}-{arch}-{get_python_interpreter(python)}-{libc}"
    flags: list[str] = [
        "--python-flag=-m",
        "--mode=onefile",
        "--output-dir=build/",
        f"--output-filename=../dist/{exename}",
        f"--include-package-data={package}",
    ]
    if lto:
        flags.append("--lto=yes")

    # Currently unable to do compression in github actions due to memory constraints
    if no_compress:
        flags.append("--onefile-no-compression")

    script = f"""
cd /src
{setup or ""}
mkdir -p build/ dist/
python -m pip install \
  --upgrade \
  --root-user-action=ignore \
  --extra-index-url="https://wheels.eeems.codes" \
  --editable \
  .
NUITKA_RESOURCE_MODE=code mold -run python -m nuitka {" ".join(flags)} {package}
owner=$(stat -c '%u:%g' .)
chown -R "$owner" build/ dist/
# Workaround https://github.com/rust-lang/rust/issues/55120
if [[ "$(patchelf --print-needed "dist/{exename}")" == *"libgcc_s.so.1"* ]]; then
  patchelf --remove-needed libgcc_s.so.1 "dist/{exename}"
fi
{teardown or ""}
"""

    print(f"Building executables for {arch} ({libc}) with Python {python}...")
    docker = shutil.which("docker") or "docker"
    if arch != uname().machine:
        _ = subprocess.run(
            [
                docker,
                "run",
                "--privileged",
                "--rm",
                "tonistiigi/binfmt",
                "--install",
                "all",
            ],
            check=True,
        )

    _ = subprocess.run(
        [
            docker,
            "run",
            "--rm",
            f"--volume={os.getcwd()}:/src",
            f"--platform={get_platform(arch)}",
            get_python_image(python, libc),
            "/bin/sh",
            "-ec",
            script,
        ],
        check=True,
    )

    print(f"Executable built for {arch}")
