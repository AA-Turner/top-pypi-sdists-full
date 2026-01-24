#!/usr/bin/env python3
#
# Copyright (c) 2012-2025 Snowflake Computing Inc. All rights reserved.
#

import argparse
import logging
import threading

from snowflake.snowpark_connect.utils.spcs_logger import setup_spcs_logger

if __name__ == "__main__":
    from snowflake.snowpark_connect.server import start_session
    from snowflake.snowpark_connect.utils.snowpark_connect_logging import (
        ensure_logger_has_handler,
    )

    parser = argparse.ArgumentParser()
    # Connection options are mutually exclusive
    connection_group = parser.add_mutually_exclusive_group()
    connection_group.add_argument("--tcp-port", type=int)
    connection_group.add_argument("--unix-domain-socket", type=str)

    # Logging options are independent
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument(
        "--disable-spcs-log-format",
        action="store_true",
        help="Disable SPCS (Snowpark Container Services) log format",
    )
    parser.add_argument(
        "--disable-signal-handlers",
        action="store_true",
        help="Disable signal handlers (SIGTERM, SIGINT, SIGHUP) for graceful shutdown",
    )

    args = parser.parse_args()
    unix_domain_socket = args.unix_domain_socket
    tcp_port = args.tcp_port
    if not unix_domain_socket and not tcp_port:
        tcp_port = 15002  # default spark connect server port

    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG

    # Configure other loggers - clear handlers first for clean setup
    loggers_to_configure = [
        "snowflake.snowpark",
        "snowflake.connector",
        "snowflake.connector.connection",
        "snowflake_connect_server",
    ]
    # Set up the logger based on environment
    if not args.disable_spcs_log_format:
        # Initialize SPCS log format when running in Snowpark Container Services (default)
        logger = setup_spcs_logger(
            log_level=log_level,
            enable_console_output=False,  # Shows human-readable logs to stderr
        )
    else:
        for logger_name in loggers_to_configure:
            target_logger = logging.getLogger(logger_name)
            target_logger.handlers.clear()
            configured_logger = ensure_logger_has_handler(
                logger_name, log_level, force_level=True
            )
        # Get the logger for use in signal handlers
        logger = logging.getLogger("snowflake_connect_server")

    # Create stop_event and optionally set up signal handlers in start_server
    stop_event = threading.Event()

    start_session(
        is_daemon=False,
        tcp_port=tcp_port,
        unix_domain_socket=unix_domain_socket,
        stop_event=stop_event,
        _add_signal_handler=(not args.disable_signal_handlers),
    )
