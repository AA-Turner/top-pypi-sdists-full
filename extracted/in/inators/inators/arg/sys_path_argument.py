# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import sys

from .add_argument import add_argument


def add_sys_path_argument(
        parser,
        short_alias=(),
        long_alias=(),
        *,
        metavar='DIR',
        help='add directory to the search path for Python modules (may be specified multiple times)'
):
    """
    Add a ``--sys-path`` command-line argument to ``parser``.

    The default processing of the added argument is implemented in
    :func:`process_sys_path_argument`.

    :param ~argparse.ArgumentParser parser: The parser to add the argument to.
    :param short_alias: Add short flag alias(es) for ``--sys-path``.
    :type short_alias: str or list(str) or tuple(str)
    :param long_alias: Add long option alias(es) for ``--sys-path``.
    :type long_alias: str or list(str) or tuple(str)
    :param str metavar: Override the default argument name in usage messages.
    :param str help: Override the default description of ``--sys-path``.

    .. argdoc
    """

    add_argument(parser, short_alias, '--sys-path', long_alias,
                 action='append', default=[],
                 metavar=metavar, help=help)


def process_sys_path_argument(args):
    """
    Append all unique elements in ``args.sys_path`` to :data:`sys.path`.

    This implements the default processing of the ``--sys-path`` command-line
    argument added by :func:`add_sys_path_argument`.

    :param args: A namespace object populated by
        :meth:`argparse.ArgumentParser.parse_args`.
    """

    for path in args.sys_path:
        if path not in sys.path:
            sys.path.append(path)
