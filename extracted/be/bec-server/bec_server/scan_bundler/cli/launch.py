# Description: Launch the scan bundler.
# This script is the entry point for the Scan Bundler. It is called either
# by the bec-scan-bundler entry point or directly from the command line.
import threading

from bec_lib.bec_service import parse_cmdline_args
from bec_lib.logger import bec_logger
from bec_lib.redis_connector import RedisConnector
from bec_server import scan_bundler

logger = bec_logger.logger
bec_logger.level = bec_logger.LOGLEVEL.INFO


def main():
    """
    Launch the scan bundler.
    """
    _, _, config = parse_cmdline_args()

    sb = scan_bundler.ScanBundler(config, RedisConnector)

    try:
        event = threading.Event()
        logger.success("Started ScanBundler")
        event.wait()
    except KeyboardInterrupt:
        sb.shutdown()


if __name__ == "__main__":
    main()
