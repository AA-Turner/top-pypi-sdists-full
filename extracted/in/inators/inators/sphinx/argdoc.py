# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

"""
Autodoc docstring processor for functions that can be called with a single
:class:`~argparse.ArgumentParser` object (and usually register one or more
command-line arguments with the parser).

The processor looks for a comment line in the docstring that starts with
``.. argdoc`` and replaces it with a command-line interface documentation by
invoking the function on an empty :class:`~argparse.ArgumentParser` object and
then formatting the parser's brief usage and argument help messages.

The comment line can end in an expression that safely evaluates to a dictionary
(with :func:`ast.literal_eval`). The dictionary will be treated as keyword
arguments to be passed to the function when invoked.

Example
    .. code-block:: python

        def add_foo_argument(parser):
            '''
            Add ``--foo`` command-line argument to ``parser``.
            .. argdoc
            '''
            parser.add_argument('--foo', help='foo argument')

See the :mod:`inators.arg` module for functions that use such CLI documentation.

To use the docstring processor, ``conf.py`` shall list it among the extensions:

.. code-block:: python

    extensions = [
        'sphinx.ext.autodoc',
        'inators.sphinx.argdoc',
    ]
"""

import argparse
import ast
import re
import textwrap


def argdoc(app, what, name, obj, options, lines):
    if what != 'function':
        return

    pattern = re.compile(r'^(?P<indent>\s*)\.\.\s+argdoc(?:\s*|\s+(?P<kwargs>\S.*))?$')
    orig_lines = lines[:]
    for i, line in enumerate(orig_lines):
        match = pattern.fullmatch(line)
        if match:
            indent, kwargs = match.group('indent', 'kwargs')
            kwargs = ast.literal_eval(kwargs) if kwargs else {}
            parser = argparse.ArgumentParser(prog='', add_help=False)
            obj(parser, **kwargs)
            replacement = textwrap.dedent("""

                Command-line interface
                    .. code-block:: none

            """) + textwrap.indent(parser.format_help(), ' ' * 8)
            replacement = textwrap.indent(replacement, indent).splitlines()
            lines[i:i + 1] = replacement[:]
            break

    # make sure there is a blank line at the end
    if lines and lines[-1]:
        lines.append('')


def setup(app):
    app.connect('autodoc-process-docstring', argdoc)

    return {
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
