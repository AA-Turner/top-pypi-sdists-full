#!/usr/bin/env python3

"""Example for fancy logging"""

import logging
from argparse import ArgumentParser

from trickkiste.logging_helper import (
    apply_common_logging_cli_args,
    set_log_levels,
    setup_logging,
)


def log() -> logging.Logger:
    """Returns the logger instance to use here"""
    return logging.getLogger("trickkiste.fancylogging")


def long_function_name() -> None:
    """Just a function with a longer name"""
    log().info("info from function")


def main() -> None:
    """Runs this"""
    parser = ArgumentParser(__doc__)
    apply_common_logging_cli_args(parser)
    args = parser.parse_args()

    setup_logging(
        log(),
        level=args.log_level,
        # show_level = False,
        # show_time = False,
        show_name=14,
        show_callstack=40,
        show_funcname=25,
        show_tid=7,
        show_linenumber=True,
        file_path=args.log_file,
    )

    set_log_levels("DEBUG")
    set_log_levels(logging.DEBUG)
    set_log_levels((log(), "DEBUG"))
    set_log_levels(("trickkiste", "INFO"), (log(), "DEBUG"))

    logging.getLogger().debug("getLogger (debug)")
    logging.getLogger().info("getLogger (info)")
    logging.getLogger().warning("getLogger (warning)")
    logging.getLogger().error("getLogger (error)")

    logging.getLogger("trickkiste").debug("debug")
    logging.getLogger("trickkiste").info("info")
    logging.getLogger("trickkiste").warning("warning")
    logging.getLogger("trickkiste").error("error")

    log().debug("debug")
    log().info("info")
    log().warning("warning")
    log().error("error")

    logging.getLogger("other.module").debug("only shown with level=ALL_DEBUG")
    logging.getLogger("other.module").info("only shown with level=ALL_DEBUG")
    logging.getLogger("other.module").warning("this is visible")
    logging.getLogger("other.module").error("this is also visible")

    long_function_name()


if __name__ == "__main__":
    main()
