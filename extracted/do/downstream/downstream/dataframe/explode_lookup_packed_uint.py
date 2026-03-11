import argparse
import functools
import logging

from joinem._dataframe_cli import _add_parser_base, _run_dataframe_cli

from .._version import __version__ as downstream_version
from ._explode_lookup_packed import explode_lookup_packed


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=False,
        allow_abbrev=False,
        description="Explode downstream-curated data from hexidecimal "
        "serialization of downstream buffers and counters to "
        "one-data-item-per-row, applying downstream lookup to identify origin "
        "time `Tbar` of each item.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _add_parser_base(
        parser=parser,
        dfcli_module="downstream.dataframe.explode_lookup_packed_uint",
        dfcli_version=downstream_version,
    )
    parser.add_argument(
        "--mp-context",
        default="thread",
        type=str,
        help="Deprecated. Previously selected the multiprocessing "
        'start method; now ignored. Default "thread".',
    )
    parser.add_argument(
        "--mp-pool-size",
        default=1,
        type=int,
        help="Number of worker threads for parity computation. "
        "Default 1 (sequential, no threading overhead).",
    )
    return parser


if __name__ == "__main__":
    logging.basicConfig(
        datefmt="%Y-%m-%d %H:%M:%S",
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.INFO,
    )
    parser = _create_parser()
    args, __ = parser.parse_known_args()

    _run_dataframe_cli(
        base_parser=parser,
        output_dataframe_op=functools.partial(
            explode_lookup_packed,
            mp_context=args.mp_context,
            mp_pool_size=args.mp_pool_size,
            value_type="uint64",
        ),
    )
