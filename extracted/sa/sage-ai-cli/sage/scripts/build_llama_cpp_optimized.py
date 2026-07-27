"""Rebuild llama-cpp-python with platform-optimal native flags.

The pip-published llama-cpp-python wheels are conservative — they target
the lowest-common-denominator CPU and skip Metal on macOS in some configs.
A native rebuild with the right CMAKE_ARGS unlocks 30-50% prefill speedups.

Examples:
    python -m sage.scripts.build_llama_cpp_optimized
    python -m sage.scripts.build_llama_cpp_optimized --dry-run
    python -m sage.scripts.build_llama_cpp_optimized --cuda
"""

from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys

__all__ = ["pick_cmake_flags", "build_command", "main"]


def pick_cmake_flags(*, force_cuda: bool = False, force_cpu: bool = False) -> list[str]:
    """Choose the best CMAKE_ARGS flag set for this machine."""
    if force_cpu:
        return ["-DGGML_NATIVE=ON"]
    if force_cuda:
        return ["-DGGML_CUDA=ON", "-DGGML_NATIVE=ON"]
    sysname = platform.system()
    machine = platform.machine()
    if sysname == "Darwin" and machine == "arm64":
        # Metal + Accelerate framework — Apple Silicon optimal
        return [
            "-DGGML_METAL=ON",
            "-DGGML_METAL_EMBED_LIBRARY=ON",
            "-DGGML_NATIVE=ON",
            "-DGGML_ACCELERATE=ON",
        ]
    if sysname == "Linux":
        # Try CUDA if nvidia-smi is present, else native CPU
        try:
            r = subprocess.run(["nvidia-smi"], capture_output=True, timeout=5)
            if r.returncode == 0:
                return ["-DGGML_CUDA=ON", "-DGGML_NATIVE=ON"]
        except (FileNotFoundError, subprocess.TimeoutExpired):
            pass
        return ["-DGGML_NATIVE=ON", "-DGGML_BLAS=ON"]
    if sysname == "Windows":
        return ["-DGGML_NATIVE=ON"]
    return ["-DGGML_NATIVE=ON"]


def build_command(flags: list[str]) -> tuple[list[str], dict]:
    """Return (argv, env) for the install command."""
    env = dict(os.environ)
    env["CMAKE_ARGS"] = " ".join(flags)
    env["FORCE_CMAKE"] = "1"
    argv = [
        sys.executable, "-m", "pip", "install",
        "--upgrade", "--force-reinstall", "--no-cache-dir",
        "--no-binary", "llama-cpp-python",
        "llama-cpp-python",
    ]
    return argv, env


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="Print the command without running it")
    parser.add_argument("--cuda", action="store_true", help="Force CUDA build")
    parser.add_argument("--cpu", action="store_true", help="Force pure CPU build")
    args = parser.parse_args(argv)

    flags = pick_cmake_flags(force_cuda=args.cuda, force_cpu=args.cpu)
    cmd, env = build_command(flags)
    print(f"CMAKE_ARGS={env['CMAKE_ARGS']}")
    print("Command: " + " ".join(cmd))
    if args.dry_run:
        return 0
    return subprocess.call(cmd, env=env)


if __name__ == "__main__":
    sys.exit(main())
