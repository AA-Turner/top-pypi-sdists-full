# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

from .add_argument import add_argument


def add_version_argument(
        parser,
        short_alias=(),
        long_alias=(),
        *,
        version
):
    """
    Add a ``--version`` command-line argument to ``parser``.

    :param ~argparse.ArgumentParser parser: The parser to add the argument to.
    :param short_alias: Add short flag alias(es) for ``--version``.
    :type short_alias: str or list(str) or tuple(str)
    :param long_alias: Add long option alias(es) for ``--version``.
    :type long_alias: str or list(str) or tuple(str)
    :param str version: The version string to show.

    .. argdoc {'version':'0.0.0'}
    """

    add_argument(parser, short_alias, '--version', long_alias,
                 action='version',
                 version='%(prog)s {version}'.format(version=version))
