import argparse
import functools

from joinem._dataframe_cli import _add_parser_base, _run_dataframe_cli

from .._version import __version__ as downstream_version

from ._unpack_data_packed import unpack_data_packed


def _create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        add_help=False,
        allow_abbrev=False,
        description="Unpack data with dstream buffer and counter serialized "
        "into a single hexadecimal data field.",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    _add_parser_base(
        parser=parser,
        dfcli_module="downstream.dataframe.unpack_data_packed",
        dfcli_version=downstream_version,
    )
    parser.add_argument(
        "--mp-context",
        default="spawn",
        type=str,
        help="Multiprocessing start method. " 'Default "spawn".',
    )
    parser.add_argument(
        "--mp-pool-size",
        default=1,
        type=int,
        help="Number of worker processes for parity computation. "
        "Default 1 (sequential, no multiprocessing overhead).",
    )
    return parser


if __name__ == "__main__":
    parser = _create_parser()
    args, __ = parser.parse_known_args()

    _run_dataframe_cli(
        base_parser=parser,
        output_dataframe_op=functools.partial(
            unpack_data_packed,
            mp_context=args.mp_context,
            mp_pool_size=args.mp_pool_size,
        ),
    )
