from argparse import ArgumentParser, Namespace

from tololib.const import DEFAULT_PORT, DEFAULT_RETRY_COUNT, DEFAULT_RETRY_TIMEOUT

from ..client import ToloClient
from .common import Command


class DiscoverCommand(Command):
    def __init__(self, argument_parser: ArgumentParser) -> None:
        super().__init__(argument_parser)
        argument_parser.add_argument("-p", "--port", default=DEFAULT_PORT, type=int)
        argument_parser.add_argument("--broadcast-address", default="255.255.255.255", type=str)
        argument_parser.add_argument("--retry-count", default=DEFAULT_RETRY_COUNT, type=int)
        argument_parser.add_argument("--retry-timeout", default=DEFAULT_RETRY_TIMEOUT, type=float)

    def __call__(self, args: Namespace) -> int:
        tolo_devices = list(
            ToloClient.discover(
                broadcast_address=args.broadcast_address,
                port=args.port,
                timeout=args.retry_timeout,
                max_retries=args.retry_count,
            )
        )

        if len(tolo_devices) == 0:
            return 1

        for remote, status in tolo_devices:
            print(f"Found TOLO device at {remote[0]}:{remote[1]}")

        return 0
