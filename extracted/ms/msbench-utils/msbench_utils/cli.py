import os
import argparse
import sys
from .reporter import Reporter

def parse_warning(s: str):
    """
    Parse a warning string of format TYPE[:MESSAGE[:TRACE]]
    into its components.
    """
    parts = s.split(":", 2)
    return {
        "type": parts[0],
        "message": parts[1] if len(parts) > 1 and parts[1] else None,
        "trace": parts[2] if len(parts) > 2 and parts[2] else None
    }

def main():
    default_output = os.getenv("OUTPUT_DIR")
    p = argparse.ArgumentParser(
        prog="msbench-report-error",
        description="Write a structured error.json into $OUTPUT_DIR"
    )
    p.add_argument(
        "--output-dir", "-o",
        default=default_output,
        help=(
            "Directory where error.json will be written "
            f"(default: $OUTPUT_DIR={default_output!r})"
        )
    )
    p.add_argument(
        "--type", "-t",
        help="Top-level error code (e.g. AGENT_TIMEOUT, X_FOO). Omit if only warnings"
    )
    p.add_argument("--message", "-m", help="Human-readable message")
    p.add_argument("--trace", help="Optional detailed trace")
    p.add_argument(
        "--warning", "-w",
        action="append", default=[],
        help="Warning entry; format TYPE[:MESSAGE[:TRACE]]. Can be repeated."
    )

    args = p.parse_args()

    if not args.output_dir:
        p.error(
            "No output directory specified. "
            "Please set the OUTPUT_DIR environment variable or pass --output-dir."
        )

    rep = Reporter(output_dir=args.output_dir)
    if args.type:
        rep.set_error(type=args.type, message=args.message, trace=args.trace)
    for wstr in args.warning:
        w = parse_warning(wstr)
        rep.add_warning(type=w["type"], message=w["message"], trace=w["trace"])

    path = rep.write()
    print(f"Wrote error report to {path}")

if __name__ == "__main__":
    main()
