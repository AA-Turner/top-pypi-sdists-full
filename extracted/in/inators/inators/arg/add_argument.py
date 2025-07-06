# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.


def add_argument(parser, *args, **kwargs):
    """
    Utility function that helps write other ``add_FOO_argument`` functions.

    It collects all argument names from its positional arguments (by also
    looking into :class:`list` and :class:`tuple` arguments) and then calls
    :meth:`~argparse.ArgumentParser.add_argument` on ``parser`` with the
    collected names and all additional keyword arguments.

    Example
        Assuming that ``--foo FOO`` is a command-line argument that is used by
        many tools, with a typical abbreviation of ``-f FOO``, a usual default
        value of ``xyz``, and a widely-accepted meaningful help description, it
        may be beneficial to have a common function that registers such an
        argument with an :class:`~argparse.ArgumentParser` (to avoid
        copy-pasting). It may also be useful, however, to allow some
        customization, should some tools need to deviate a bit from the typical
        usage. Then, an ``add_foo_argument`` function can be implemented with
        the help of :func:`inators.arg.add_argument`:

        .. code-block:: python

            import argparse
            from inators import arg

            # This is the common code, reused by many.
            def add_foo_argument(
                    parser,
                    short_alias='-f',
                    long_alias=(),
                    *,
                    metavar='FOO',
                    default='xyz',
                    help='set foo (default: %(default)s)'
            ):
                arg.add_argument(parser, short_alias, '--foo', long_alias,
                                 metavar=metavar, default=default, help=help)

            # This is how to make use of the function above.
            parser = argparse.ArgumentParser()
            add_foo_argument(parser)  # if the default names, values, and descriptions are all good
            # or:
            add_foo_argument(parser, short_alias=[])  # to disallow the default short flag alias
            # or:
            add_foo_argument(parser, default='abc')  # to change the default default value
    """

    _args = []
    for arg in args:
        if isinstance(arg, (list, tuple)):
            _args.extend(arg)
        else:
            _args.append(arg)
    parser.add_argument(*_args, **kwargs)
