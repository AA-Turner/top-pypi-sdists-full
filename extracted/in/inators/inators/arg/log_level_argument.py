# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import argparse

from .add_argument import add_argument
from .. import log


def add_log_level_argument(
        parser,
        short_alias='-l',
        long_alias=(),
        *,
        metavar='LEVEL',
        choices=sorted(log.levels.keys(), key=lambda k: log.levels[k]),
        default='INFO',
        help='verbosity level of diagnostic messages (%(choices)s; default: %(default)s)',
        verbose_alias=('-v', '--verbose'),
        verbose_const='DEBUG',
        verbose_help='verbose mode (alias for --log-level %(const)s)',
        quiet_alias=('-q', '--quiet'),
        quiet_const='DISABLE',
        quiet_help='quiet mode (alias for --log-level %(const)s)'
):
    """
    Add a ``--log-level`` command-line argument to ``parser``.

    The default processing of the added argument is implemented in
    :func:`process_log_level_argument`.

    :param ~argparse.ArgumentParser parser: The parser to add the argument to.
    :param short_alias: Override the default short flag alias for
        ``--log-level``.
    :type short_alias: str or list(str) or tuple(str)
    :param long_alias: Add long option alias(es) for ``--log-level``.
    :type long_alias: str or list(str) or tuple(str)
    :param str metavar: Override the default argument name in usage messages.
    :param list(str) choices: Override the default list of accepted log level
        names (see :mod:`inators.log`).
    :param str default: Override the default log level name to use if
        ``--log-level`` is not given on the command line.
    :param str help: Override the default description of ``--log-level``.
    :param verbose_alias: Override the default list of short flag and long
        option aliases for ``--log-level DEBUG``. If empty, the alias
        command-line arguments are not added to the parser.
    :type verbose_alias: str or list(str) or tuple(str)
    :param str verbose_const: Override the default log level name to be set by
        the verbose aliases.
    :param str verbose_help: Override the default description of the verbose
        aliases.
    :param quiet_alias: Override the default list of short flag and long option
        aliases for ``--log-level DISABLE``. If empty, the alias command-line
        arguments are not added to the parser.
    :type quiet_alias: str or list(str) or tuple(str)
    :param str quiet_const: Override the default log level name to be set by the
        quiet aliases.
    :param str quiet_help: Override the default description of the quiet
        aliases.

    .. argdoc
    """

    add_argument(parser, short_alias, '--log-level', long_alias,
                 metavar=metavar, choices=choices, default=default, help=help)
    if verbose_alias:
        add_argument(parser, verbose_alias,
                     dest='log_level', action='store_const', default=argparse.SUPPRESS,
                     const=verbose_const, help=verbose_help)
    if quiet_alias:
        add_argument(parser, quiet_alias,
                     dest='log_level', action='store_const', default=argparse.SUPPRESS,
                     const=quiet_const, help=quiet_help)


def process_log_level_argument(args, logger):
    """
    Set the log level of ``logger`` to the numeric value associated with the log
    level name set in ``args.log_level``. The mapping happens using
    :data:`inators.log.levels`, i.e., :data:`~inators.log.TRACE` and
    :data:`~inators.log.DISABLE` are also supported.

    This implements the default processing of the ``--log-level`` command-line
    argument added by :func:`add_log_level_argument`.

    :param args: A namespace object populated by
        :meth:`argparse.ArgumentParser.parse_args`.
    :param ~logging.Logger logger: A logger to configure.
    """

    logger.setLevel(log.levels[args.log_level])
