"""``python -m matrice_common.diagnostics`` — print one memory snapshot.

Designed for ops to drop into an SSH session and capture the same evidence
chain we had to assemble by hand during the Jetson-Thor leak incident.
"""

from __future__ import annotations

import argparse
import json
import sys
import time

from .memory import delta, format_table, snapshot


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--json",
        action="store_true",
        help="emit a JSON dict instead of the human-readable table",
    )
    parser.add_argument(
        "--watch",
        type=float,
        default=None,
        metavar="SECONDS",
        help="re-sample every N seconds and print the delta",
    )
    args = parser.parse_args(argv)

    snap = snapshot()
    if args.json:
        sys.stdout.write(json.dumps(snap.to_dict(), default=str) + "\n")
    else:
        sys.stdout.write(format_table(snap) + "\n")
    sys.stdout.flush()

    if args.watch is None:
        return 0

    prev = snap
    try:
        while True:
            time.sleep(args.watch)
            cur = snapshot()
            d = delta(prev, cur)
            sys.stdout.write("\n--- delta ---\n")
            if args.json:
                sys.stdout.write(json.dumps(d.to_dict(), default=str) + "\n")
            else:
                sys.stdout.write(format_table(d) + "\n")
            sys.stdout.flush()
            prev = cur
    except KeyboardInterrupt:
        return 0


if __name__ == "__main__":
    sys.exit(main())
