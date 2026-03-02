import argparse
import subprocess
import sys
import warnings

from .. import _version
from .._auxlib._ArgparseFormatter import ArgparseFormatter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Debug a downstream implementation against selected reference "
            "test cases. This script does not test hybrid algorithms --- use "
            "debug_one to test these directly."
        ),
        epilog=f"downstream version {_version.__version__}",
        formatter_class=ArgparseFormatter,
    )
    parser.add_argument(
        "command",
        help="The command to test. Example: 'python3 ./my_program'",
    )
    parser.add_argument(
        "--reference",
        default="python3 -O -m downstream",
        help="Reference command to validate against.",
    )
    parser.add_argument(
        "-v", "--version", action="version", version=_version.__version__
    )
    args = parser.parse_args()

    script = r"""
pv=$(which pv && echo "--size $((17*512))" || echo "cat")

EXITCODE=0
for algo in \
    "dstream.steady_algo" \
    "dstream.stretched_algo" \
    "dstream.tilted_algo" \
; do
    for func in \
        "assign_storage_site" \
        "has_ingest_capacity" \
        "lookup_ingest_times" \
    ; do
        target="${algo}.${func}"
        echo "target=${target}"
        python3 -m downstream.testing.debug_one \
            "$2" "${target}" --reference "$1" | ${pv} | grep -v "OK"
        status=${PIPESTATUS[0]}

        if [ ${status} != 0 ]; then
            ((EXITCODE+=status))
        else
            echo "ALL OK"
        fi

        echo
    done
done
exit $EXITCODE
"""

if __name__ == "__main__":
    warnings.warn(
        "downstream.testing.debug_all should NOT be used in automated "
        "tests, as the suite of algorithms tested may change over time. "
        "Instead, use downstream.testing.validate_one to test specific "
        "algorithms explicitly.",
    )
    result = subprocess.run(
        [
            "bash",
            "-c",
            script,
            sys.argv[0],
            args.reference,
            args.command,
        ],
    )
    sys.exit(result.returncode)
