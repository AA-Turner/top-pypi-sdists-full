import logging
import os
from argparse import ArgumentParser, Namespace
from pathlib import Path

import dotenv

from ipfabric.tools.shared import valid_snapshot


def load_env():
    dotenv.load_dotenv(dotenv.find_dotenv(usecwd=True) or Path("~").expanduser().joinpath(".env"))


def check_snapshot_arg(snapshot: str) -> str:
    if snapshot.lower() in ["last", "prev", "lastlocked"]:
        snapshot = "$" + snapshot
    snapshot = valid_snapshot(snapshot).strip("'")
    return snapshot


def get_auth_from_args_or_env(args):
    """
    Determine the authentication method based on args or environment variables.
    """
    if args.token:
        return args.token
    if args.username and args.password:
        return args.username, args.password
    if os.getenv("IPF_TOKEN"):
        return os.getenv("IPF_TOKEN")
    if os.getenv("IPF_USERNAME") and os.getenv("IPF_PASSWORD"):
        return os.getenv("IPF_USERNAME"), os.getenv("IPF_PASSWORD")
    else:
        raise ValueError("Authentication details must be provided as an argument or set as an environment variable.")


def base_args(arg_parser: ArgumentParser) -> ArgumentParser:
    arg_parser.add_argument(
        "-s",
        "--snapshot",
        help="Snapshot to use which can be a UUID or one of ['last', 'prev', 'lastLocked']"
        "with or without `$` for *nix compatability.",
        default="$last",
    )
    arg_parser.add_argument(
        "-b",
        "--base-url",
        default=os.getenv("IPF_URL", None),
        help="Base URL for IPFabric API or IPF_URL env variable.",
    )
    arg_parser.add_argument("-t", "--token", help="IP Fabric API Token or IPF_TOKEN env variable.")
    arg_parser.add_argument(
        "-u",
        "--username",
        help="IP Fabric username (requires --password) or IPF_USERNAME env variable.",
    )
    arg_parser.add_argument("-p", "--password", help="IP Fabric password or IPF_PASSWORD env variable.")
    return arg_parser


def parse_base_args(args: Namespace) -> Namespace:
    if not args.base_url:
        raise ValueError("Base URL must be provided as an argument or set as an environment variable (IPF_URL).")
    args.snapshot = check_snapshot_arg(args.snapshot)
    setattr(args, "auth", get_auth_from_args_or_env(args))
    return args


def shared_args(arg_parser: ArgumentParser, logger_name: str) -> Namespace:
    arg_parser = base_args(arg_parser)
    arg_parser.add_argument(
        "-c",
        "--count",
        help="Print count of rows instead of the actual data.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-v",
        "--verbose",
        help="Verbose output will enable debugging and print all tables even if no data.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-j",
        "--json",
        help="Enable JSON output which will also print all tables even if no data.",
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-R",
        "--rich-disable",
        help="Disable rich formatting if installed. Useful for sending JSON output to jq.",
        action="store_true",
        default=False,
    )
    args = arg_parser.parse_args()

    logger = logging.getLogger(logger_name)
    if args.verbose:
        logger.setLevel(logging.DEBUG)
        logging.getLogger("ipfabric").setLevel(logging.DEBUG)
        logger.debug("Logging level set to DEBUG")

    args = parse_base_args(args)
    logger.debug(f"Snapshot ID selected: {args.snapshot}")
    return args
