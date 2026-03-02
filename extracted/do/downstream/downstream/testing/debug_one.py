import argparse
import subprocess
import sys

from .. import _version
from .._auxlib._ArgparseFormatter import ArgparseFormatter

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description=(
            "Debug a target downstream algorithm implementation by comparing "
            "output against a reference implementation for selected test cases."
        ),
        epilog=f"downstream version {_version.__version__}",
        formatter_class=ArgparseFormatter,
    )
    parser.add_argument(
        "command",
        help="The command to test. Example: 'python3 ./my_program'",
    )
    parser.add_argument(
        "target",
        help=(
            "The algorithm function to test. "
            "Example: 'dstream.steady_algo.assign_storage_site'"
        ),
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

    script = rf"""
set -e
test_cases=(
    # Edge cases for S (powers of 2)
    "1 0"      # Minimum S
    "1 1"
    "1 4095"
    "2 0"
    "2 4095"
    "4 0"
    "4 4095"
    "8 0"
    "8 4095"
    "16 0"
    "16 4095"
    "32 0"
    "32 4095"
    "64 0"
    "64 4095"
    "128 0"
    "128 4095"
    "256 0"
    "256 4095"
    "512 0"
    "512 4095"
    "1024 0"
    "1024 4095"
    "2048 0"
    "2048 4095"
    "4096 0"
    "4096 4095"
    "8192 0"
    "8192 4095"
    "16384 0"
    "16384 4095"
    "32768 0"
    "32768 4095"
    "65536 0"
    "65536 4095"
    "131072 0"
    "131072 4095"
    "262144 0"
    "262144 4095"
    "524288 0"
    "524288 4095"
    "1048576 0"
    "1048576 4095"

    # Edge cases for T
    "1 4094"
    "2 4094"
    "4 4094"
    "8 4094"
    "16 4094"
    "32 4094"
    "1048576 4094"

    # Random cases with T < 100
    "1 50"
    "2 75"
    "4 25"
    "8 99"
    "16 12"
    "32 87"
    "64 42"
    "128 63"
    "256 91"
    "512 33"
    "1024 77"
    "2048 15"
    "4096 88"
    "8192 44"
    "16384 66"
    "32768 92"
    "65536 28"
    "131072 95"
    "262144 71"
    "524288 83"
    "1048576 97"

    # Random capacity bound tests
    "1 1"
    "2 3"
    "4 7"
    "8 15"
    "16 31"
    "32 63"
    "64 127"
    "128 255"
    "256 511"
    "512 1023"
    "1024 2047"
    "2048 4095"

    # Mid-range cases
    "16 1000"
    "32 2000"
    "64 3000"
    "128 2500"
    "256 1500"
    "512 3500"
    "1024 2750"
    "2048 1750"
    "4096 3250"

    # Special case combinations
    "1 4095"    # Min S, max T
    "1048576 0" # Max S, min T
    "524288 2048" # Large S, mid T
    "256 4000"    # Mid S, high T
    "16 100"      # Small S, low T
    "4096 3000"   # Mid-high S, mid-high T
    "32768 1500"  # High S, mid T
    "8 4090"      # Small S, near-max T
    "131072 50"   # High S, low T
    "64 3500"     # Low-mid S, high T

    # Additional random cases
    "4 2047"
    "32 1023"
    "128 3071"
    "512 2559"
    "2048 3583"
    "8192 1535"
    "32768 3839"
    "131072 2303"
    "524288 3967"
    "16 4031"
    "64 2815"
    "256 3327"
    "1024 1791"
    "4096 3711"
    "16384 2047"
    "65536 3455"
    "262144 1279"
    "1048576 3967"
    "1 3790218436"

    # Multiples of 3 (for 3-chunk hybrid algos)
    "24 0"
    "24 4095"
    "24 50"
    "24 1000"
    "48 0"
    "48 4095"
    "48 50"
    "48 1000"
    "96 0"
    "96 4095"
    "96 50"
    "96 1000"
)

line1="-----------------------------------------------------------------"
line2="%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%"
target="# {args.target} "

printf "\n%s\n" "${{line2}}"
printf "%s%s\n" "${{target}}" "${{line1:((${{#target}} + 2))}} #"
printf "%s\n" "${{line2}}"
printf "%-20s | %-20s | %-20s\n" "Test Case S, T" "Reference Output" "Command Output"
printf "%s\n" "${{line1}}"

EXITCODE=0
for test_case in "${{test_cases[@]}}"; do
    ref_output="$(echo "${{test_case}}" | $1 $3 2>/dev/null || echo "ERROR")"
    test_output="$(echo "${{test_case}}" | $2 $3 2>/dev/null || echo "ERROR")"

    printf "%-20s | %-20s | %-20s" \
        "${{test_case}}" \
        "${{ref_output:0:20}}" \
        "${{test_output:0:20}}"

    if [ "${{ref_output}}" != "${{test_output}}" ]; then
        printf " <- MISMATCH\n"
        ((++EXITCODE))
    else
        printf [OK]"\n"
    fi
done

exit ${{EXITCODE}}
"""
    result = subprocess.run(
        [
            "bash",
            "-c",
            script,
            sys.argv[0],
            args.reference,
            args.command,
            args.target,
        ],
    )
    sys.exit(result.returncode)
