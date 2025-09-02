"""
Python3 script to search for an IPv4, IPv6, or MAC address in multiple IP Fabric's tables and prints the output.
"""

import argparse
import json
import logging
from typing import Union

from ipfabric import IPFClient
from ipfabric.models.global_search import RouteTableSearch
from ipfabric.scripts.shared import shared_args, load_env

try:
    from rich.console import Console

    CONSOLE = Console()
except ImportError:
    CONSOLE = None

logging.basicConfig(format="%(levelname)s: %(message)s")

LOGGER = logging.getLogger("ipf_route_search")


def main() -> dict[str, dict[str, Union[str, list]]]:
    load_env()
    arg_parser = argparse.ArgumentParser(
        description="Search IPv4 or IPv6 Route tables for an Address or Subnet.",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
IPv4 and IPv6 Route or Next Hop IP:
    `=|eq`: Route (CIDR) or Next Hop IP exactly matches.
    `IP|ip`: IP is contained within Routed subnet or Next Hop IP matches.

IPv4 and IPv6 Next Hop IP:
    `cidr|CIDR`: Next Hop IP is contained within subnet.

IPv4 Route CIDR Searching:
    `>|gt`: CIDR is strict supernet (10.0.0.0/24 -> 10.0.0.0/[8..23], 0.0.0.0/0)
    `>=|gte`: CIDR is supernet (10.0.0.0/24 -> 10.0.0.0/[8..24], 0.0.0.0/0)
    `<|lt`: CIDR is strict subnet (10.0.0.0/24 -> 10.0.0.0/[25..32])
    `<|lte`: CIDR is subnet (10.0.0.0/24 -> 10.0.0.0/[24..32])
    `@|sect`: CIDR overlaps (10.0.0.0/24 -> 10.0.0.0/[8..32], 0.0.0.0/0)
    `!@|nsect`: CIDR does not overlap (10.0.0.0/24 -> 10.1.0.0/24)
""",
    )
    arg_parser.add_argument(
        "address",
        help="IPv4 or IPv6 Address/CIDR to search for.",
    )
    arg_parser.add_argument(
        "-o",
        "--operator",
        help="Default 'eq'",
        default="eq",
    )
    arg_parser.add_argument(
        "-d",
        "--default-route",
        help='Include "0.0.0.0/0" routes.',
        action="store_true",
        default=False,
    )
    arg_parser.add_argument(
        "-n",
        "--next-hop",
        help="Search Next Hop IP instead of Route.",
        action="store_true",
        default=False,
    )
    args = shared_args(arg_parser, "ipf_route_search")

    ipf = IPFClient(snapshot_id=args.snapshot, base_url=args.base_url, auth=args.auth)
    ipf._client.headers["user-agent"] += "; ipf_route_search"
    rs = RouteTableSearch(client=ipf)
    print_results(rs.search(args.address, args.operator, args.next_hop, not args.default_route), args)


def rich_print(result: dict, count: bool = False):
    CONSOLE.print(f"\n{result['menu']}: {str(len(result['data']))}" if count else f"\n{result['menu']}")
    CONSOLE.print(result["url"], style=f"link {result['url']}")
    if not count:
        json_str = json.dumps(result["data"], indent=4)
        CONSOLE.print(json_str)


def py_print(result: dict, count: bool = False):
    print(f"\n{result['menu']}: {str(len(result['data']))}" if count else f"\n{result['menu']}")
    print(result["url"])
    if not count:
        print(json.dumps(result["data"], indent=4))


def print_results(results: dict, args: argparse.Namespace):
    global CONSOLE
    if args.rich_disable:
        CONSOLE = None
    if not results["data"]:
        msg = "\nNo routes found."
        CONSOLE.print(msg) if CONSOLE else LOGGER.error(msg)
        exit(1)
    if args.json:
        CONSOLE.print(json.dumps(results, indent=4)) if CONSOLE else print(json.dumps(results, indent=4))
    elif CONSOLE:
        rich_print(results, args.count)
    else:
        py_print(results, args.count)


if __name__ == "__main__":
    main()
