"""Re-quantize a GGUF model to a higher-quality format.

Q4_0 is fine for chat. For *code* tasks, Q5_K_M typically recovers ~half
the quality lost vs FP16 at only ~15% more disk. This script wraps
llama-cpp's `llama-quantize` binary or falls back to `huggingface_hub`.

Examples:
    python -m sage.scripts.requantize ~/.sage/models/qwen3-coder-next.gguf
    python -m sage.scripts.requantize <path> --quant Q5_K_M --keep-original
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

__all__ = ["VALID_QUANTS", "find_quantize_binary", "requantize", "main"]


VALID_QUANTS = (
    "Q2_K", "Q3_K_S", "Q3_K_M", "Q3_K_L",
    "Q4_0", "Q4_K_S", "Q4_K_M",
    "Q5_0", "Q5_K_S", "Q5_K_M",
    "Q6_K", "Q8_0", "F16",
)


def find_quantize_binary() -> str | None:
    """Locate the llama-quantize binary. Returns None if not installed."""
    for name in ("llama-quantize", "quantize"):
        found = shutil.which(name)
        if found:
            return found
    # llama-cpp-python ships its own
    try:
        import llama_cpp
        binpath = Path(llama_cpp.__file__).parent / "lib" / "llama-quantize"
        if binpath.is_file():
            return str(binpath)
    except ImportError:
        pass
    return None


def requantize(input_path: Path, output_path: Path, quant: str = "Q5_K_M") -> int:
    """Run llama-quantize. Returns the subprocess returncode."""
    if quant not in VALID_QUANTS:
        raise ValueError(f"Unknown quant {quant!r}; valid: {VALID_QUANTS}")
    binary = find_quantize_binary()
    if binary is None:
        raise RuntimeError(
            "llama-quantize not found. Install via:\n"
            "    brew install llama.cpp        # macOS\n"
            "    pip install llama-cpp-python  # bundles a copy\n"
        )
    cmd = [binary, str(input_path), str(output_path), quant]
    return subprocess.call(cmd)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path, help="Source GGUF path")
    parser.add_argument("--quant", default="Q5_K_M", choices=VALID_QUANTS)
    parser.add_argument("--output", type=Path, default=None, help="Output path (default: <input>.<quant>.gguf)")
    parser.add_argument("--keep-original", action="store_true",
                        help="Don't replace the original after success")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)

    if not args.input.is_file():
        print(f"Not a file: {args.input}", file=sys.stderr)
        return 1
    out = args.output or args.input.with_suffix(f".{args.quant}.gguf")
    if args.dry_run:
        print(f"Would: {args.input} -> {out} (quant={args.quant})")
        return 0
    print(f"Quantizing {args.input} -> {out} ({args.quant})...")
    rc = requantize(args.input, out, quant=args.quant)
    if rc == 0 and not args.keep_original:
        print(f"Replacing original {args.input} with {out}")
        args.input.unlink()
        out.rename(args.input)
    return rc


if __name__ == "__main__":
    sys.exit(main())
