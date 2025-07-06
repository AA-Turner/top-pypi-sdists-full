# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest
import textwrap

from inators import sphinx as inators_sphinx


def add_foo_argument(parser):
    '''
    Add ``--foo`` command-line argument to ``parser``.
    .. argdoc
    '''
    parser.add_argument('--foo', help='foo argument')

add_foo_argument.argdoc = '''
    Add ``--foo`` command-line argument to ``parser``.


    Command-line interface
        .. code-block:: none

            usage: [--foo FOO]

            optional arguments:
              --foo FOO  foo argument

    '''

def add_bar_argument(parser, *, bar):
    '''
    Add ``--bar`` command-line argument to ``parser``.
    .. argdoc {'bar': 42}
    '''
    parser.add_argument('--bar', default=bar, help='bar argument (default: %(default)s)')

add_bar_argument.argdoc = '''
    Add ``--bar`` command-line argument to ``parser``.


    Command-line interface
        .. code-block:: none

            usage: [--bar BAR]

            optional arguments:
              --bar BAR  bar argument (default: 42)

    '''


@pytest.mark.parametrize('add_argument', [
    add_foo_argument,
    add_bar_argument,
])
def test_argdoc(add_argument):
    lines = textwrap.dedent(add_argument.__doc__).splitlines()
    inators_sphinx.argdoc.argdoc(None, type(add_argument).__name__, add_argument.__name__, add_argument, None, lines)
    assert lines == textwrap.dedent(add_argument.argdoc).splitlines()
