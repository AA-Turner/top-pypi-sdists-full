# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import sys

from .add_argument import add_argument


def add_sys_recursion_limit_argument(
        parser,
        short_alias=(),
        long_alias=(),
        *,
        metavar='NUM',
        default=sys.getrecursionlimit(),
        help='override maximum depth of the Python interpreter stack (default: %(default)d)'
):
    """
    add_sys_recursion_limit_argument(parser, short_alias=(), long_alias=(), *, metavar='NUM', default=sys.getrecursionlimit(), help='override maximum depth of the Python interpreter stack (default: %(default)d)')

    Add a ``--sys-recursion-limit`` command-line argument to ``parser``.

    The default processing of the added argument is implemented in
    :func:`process_sys_recursion_limit_argument`.

    :param ~argparse.ArgumentParser parser: The parser to add the argument to.
    :param short_alias: Add short flag alias(es) for ``--sys-recursion-limit``.
    :type short_alias: str or list(str) or tuple(str)
    :param long_alias: Add long option alias(es) for ``--sys-recursion-limit``.
    :type long_alias: str or list(str) or tuple(str)
    :param str metavar: Override the default argument name in usage messages.
    :param int default: Override the default depth value to use if
        ``--sys-recursion-limit`` is not given on the command line.
    :param str help: Override the default description of
        ``--sys-recursion-limit``.

    .. argdoc
    """
    # NOTE: The first line of the docstring (i.e., the documented signature)
    #   must be kept in sync with the actual signature of the function!

    add_argument(parser, short_alias, '--sys-recursion-limit', long_alias,
                 type=int,
                 metavar=metavar, default=default, help=help)


def process_sys_recursion_limit_argument(args):
    """
    Set the maximum depth of the Python interpreter stack to
    ``args.sys_recursion_limit`` (using :func:`sys.setrecursionlimit`).

    This implements the default processing of the ``--sys-recursion-limit``
    command-line argument added by :func:`add_sys_recursion_limit_argument`.

    :param args: A namespace object populated by
        :meth:`argparse.ArgumentParser.parse_args`.
    """

    sys.setrecursionlimit(args.sys_recursion_limit)
