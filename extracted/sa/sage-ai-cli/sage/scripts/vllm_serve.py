"""Launch a vLLM server for high-throughput multi-user serving.

vLLM only matters when you're serving more than one concurrent request —
on a single-user laptop, llama.cpp/Ollama is faster start-to-finish.
Where vLLM wins:
  - Continuous batching (10x+ throughput for concurrent users)
  - PagedAttention (less KV memory waste)
  - OpenAI-compatible HTTP API

Requires CUDA + a model in HF format (not GGUF). On a CPU/Apple-Silicon
laptop this script will tell you it's not the right tool.

Examples:
    python -m sage.scripts.vllm_serve --model qwen3-coder-next --port 8000
    python -m sage.scripts.vllm_serve --model Qwen/Qwen2.5-Coder-7B --dry-run
"""

from __future__ import annotations

import argparse
import importlib.util
import platform
import shutil
import subprocess
import sys

__all__ = ["have_vllm", "have_cuda", "launch_command", "main"]


def have_vllm() -> bool:
    return importlib.util.find_spec("vllm") is not None


def have_cuda() -> bool:
    return shutil.which("nvidia-smi") is not None


def launch_command(model: str, *, port: int = 8000, max_model_len: int = 16384,
                   tensor_parallel_size: int = 1) -> list[str]:
    """Build the `python -m vllm.entrypoints.openai.api_server` invocation."""
    return [
        sys.executable, "-m", "vllm.entrypoints.openai.api_server",
        "--model", model,
        "--port", str(port),
        "--max-model-len", str(max_model_len),
        "--tensor-parallel-size", str(tensor_parallel_size),
    ]


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--model", required=True)
    p.add_argument("--port", type=int, default=8000)
    p.add_argument("--max-model-len", type=int, default=16384)
    p.add_argument("--tensor-parallel-size", type=int, default=1)
    p.add_argument("--dry-run", action="store_true", help="Print the command, don't run")
    args = p.parse_args(argv)

    if not have_cuda():
        sysname = platform.system()
        msg = f"vLLM needs an NVIDIA GPU; nvidia-smi not found on {sysname}.\n"
        if sysname == "Darwin":
            msg += "→ Use Ollama or llama.cpp on Apple Silicon (already optimal)."
        print(msg, file=sys.stderr)
        if not args.dry_run:
            return 2
    if not have_vllm():
        print("vLLM not installed. Try:\n    pip install vllm", file=sys.stderr)
        if not args.dry_run:
            return 3

    cmd = launch_command(
        args.model, port=args.port, max_model_len=args.max_model_len,
        tensor_parallel_size=args.tensor_parallel_size,
    )
    print("Launch:", " ".join(cmd))
    if args.dry_run:
        return 0
    return subprocess.call(cmd)


if __name__ == "__main__":
    sys.exit(main())
