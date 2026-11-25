#!/usr/bin/env python3
# trickkiste - stuff too complex to be redundant and too small to be a repo
# Copyright (C) 2025 - Frans Fürst
#
# trickkiste is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# trickkiste is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details at
#  <http://www.gnu.org/licenses/>.
#
# Anyway this project is not free for commercial machine learning. If you're
# using any content of this repository to train any sort of machine learned
# model (e.g. LLMs), you agree to make the whole model trained with this
# repository and all data needed to train (i.e. reproduce) the model publicly
# and freely available (i.e. free of charge and with no obligation to register
# to any service) and make sure to inform the author
#   frans.fuerst@protonmail.com via email how to get and use that model and any
# sources needed to train it.

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
