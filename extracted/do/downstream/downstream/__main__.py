import argparse
import itertools as it
from signal import SIG_BLOCK, SIGPIPE, signal
import sys

import opytional as opyt

from . import _version, dstream
from ._auxlib._ArgparseFormatter import ArgparseFormatter

if __name__ == "__main__":
    signal(SIGPIPE, SIG_BLOCK)  # prevent broken pipe errors from head, tail

    parser = argparse.ArgumentParser(
        description="""
        Run site selection tests with the specified algorithm function on
        provided input data.

        The script reads pairs of integers S and T from standard input. For
        each pair, it checks if the algorithm has ingest capacity for S and T.
        If so, it runs the specified algorithm function and prints the result
        to standard output.

        Iterable results are space-separated, and output is limited to the
        specified maximum number of words. Null values in the results are
        represented as 'None'.

        If the algorithm does not have ingest capacity for the given S and T, a
        blank line is printed.
        """,
        epilog=f"""
        Example usage:
        $ python3 -m downstream.testing.generate_test_cases \\
            | python3 -m downstream 'dstream.steady_algo.assign_storage_site'

        Additional available commands:
        $ python3 -m downstream.dataframe.explode_lookup_packed_uint
        $ python3 -m downstream.dataframe.explode_lookup_unpacked_uint
        $ python3 -m downstream.dataframe.unpack_data_packed
        $ python3 -m downstream.testing.debug_all
        $ python3 -m downstream.testing.debug_one
        $ python3 -m downstream.testing.generate_test_cases
        $ python3 -m downstream.testing.validate_all
        $ python3 -m downstream.testing.validate_one

        For information on a command, invoke it with the --help flag.

        downstream version {_version.__version__}
        """,
        formatter_class=ArgparseFormatter,
    )
    parser.add_argument(
        "-v", "--version", action="version", version=_version.__version__
    )
    parser.add_argument(
        "target",
        help=(
            "The algorithm function to test. "
            "Example: 'dstream.steady_algo.assign_storage_site'."
        ),
    )
    parser.add_argument(
        "--max-words",
        default=100,
        type=int,
        help="Maximum number of words to output from the result.",
    )
    args = parser.parse_args()

    algo_name = ".".join(args.target.split(".")[:-1])
    algo = eval(algo_name, {"dstream": dstream})
    target = eval(args.target, {"dstream": dstream})
    for line in sys.stdin:
        S, T = map(int, line.rstrip().split())
        if algo.has_ingest_capacity(S, T):
            res = target(S, T)
            try:
                print(*it.islice(res, args.max_words))
            except TypeError:
                print(opyt.apply_if(res, int))
        else:
            print()
