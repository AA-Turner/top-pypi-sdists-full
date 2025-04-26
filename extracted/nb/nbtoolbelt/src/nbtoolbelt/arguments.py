"""
Functions for command-line argument parsing

Copyright (c) 2017 - Eindhoven University of Technology, The Netherlands

This software is made available under the terms of the MIT License.
"""

import argparse
from pathlib import Path
from typing import List, Iterable

from .config import load_config_file
from .notebook_io import read_nb
from .printing import print_namespace
from .punching import SourceChadsProcessor

TEST = False


class TestAction(argparse.Action, argparse.Namespace):
    """Action to test the action mechanism,
    by printing the parameter values received in constructor and call methods.
    """
    def __init__(self, option_strings, dest, **kwargs):
        """Invoked when argument is configured in argument parser.
        Some/all parameters of ``add_argument`` are passed on via ``kwargs`` and
        are stored in ``self``.
        """
        super().__init__(option_strings, dest, **kwargs)
        print('TestAction.__init__(option_strings={}, dest={}, **kwargs)'.format(option_strings, dest))
        print('  kwargs={}'.format(kwargs))

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        """Invoked when argument is encountered during parsing.

        .. note:: **Modifies**: ``ns``

        :param parser: parser at work
        :param namespace: namespace to inspect/modify
        :param values: value for triggering option (already processed)
        :param option_string: option that triggered the action
        """
        items = [values, option_string]
        print('TestAction.__call__(parser, namespace, values={}, option_string={})'.format(*items))
        print_namespace(namespace, 'namespace')
        print_namespace(self, 'self')


class LoadConfigFile(argparse.Action):
    """Action to take when parsing a configuration file option.
    """
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        """Load configuration file for tool mentioned in dest.

        .. note:: **Modifies**: ``namespace``

        :param parser: parser at work
        :param namespace: namespace to inspect/modify
        :param values: value for triggering option (already processed)
        :param option_string: option that triggered the action
        """
        load_config_file(self.const, namespace, values, True)
        if hasattr(namespace, self.dest):
            delattr(namespace, self.dest)  # clean up the namespace; attribute 'config' is not used


class ExtendAction(argparse.Action):
    """Extend current list for option with parsed list.

    .. note:: **Assumption**:
      Option is already present in namespace (from embedded config file read in ``__init__()``).
    """

    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, ns, values, option_string=None):
        """Extend dest in ns with values.

        .. note:: **Modifies**: ``ns``
        """
        getattr(ns, self.dest).extend(values)


class NegatableAction(argparse.Action):
    """Add the supplied positive options and negative versions as well.
    Inspired by ``nbshow``.
    """

    def __init__(self, option_strings, dest, default=None, required=False, help=None):
        opts = []
        for opt in option_strings:
            if len(opt) == 2 and opt[0] == '-':
                if not opt[1].islower():
                    raise ValueError('Single character flags should be lower-case for NegatableAction')
                opts.append(opt)
                opts.append(opt.upper())
            elif opt[:2] == '--':
                opts.append(opt)
                opts.append('--no-' + opt[2:])
            else:
                ValueError('Could not turn option "%s" into an NegatableAction option.')

        # Put positives first, negatives last:
        opts = opts[0::2] + opts[1::2]

        super().__init__(
            opts, dest, nargs=0, const=None,
            default=default, required=required,
            help=help)

    def __call__(self, parser, ns, values, option_string=None):
        """Store bool derived from option_string into dest of ns.

        .. note:: **Modifies**: ``ns``
        """
        if len(option_string) == 2:
            setattr(ns, self.dest, option_string[1].islower())
        else:
            setattr(ns, self.dest, option_string[2:2 + len('no')] != 'no')


class LoadSourceFile(argparse.Action):
    """Action to take when parsing a source file option.
    """
    def __init__(self, option_strings, dest, **kwargs):
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None) -> None:
        """Load source file into namespace.source_chads.

        .. note:: **Modifies**: ``namespace``

        :param parser: parser at work
        :param namespace: namespace to inspect/modify
        :param values: value for triggering option (already processed)
        :param option_string: option that triggered the action
        """
        # read notebook whose file name is in values
        setattr(namespace, self.dest, values)
        nb = read_nb(Path(values), namespace)
        if nb is None:
            raise AssertionError('Could not read source chads')
        freq = SourceChadsProcessor(nb, namespace, values).punch_nb()
        # TODO: report freq in JSON output
        if namespace.debug or not namespace.source_chads:
            print('{} chads loaded from source notebook "{}".'
                  .format(freq['holes'], values))
        if TEST:
            import pprint
            pprint.pprint(getattr(namespace, self.dest))


def split_csv(arg: str) -> List[str]:
    """Split comma-separated values into a list.

    :param arg: argument to split
    :return: list of separated valued
    """
    return arg.split(',')  # returning list, and not set, to allow reading from JSON config file


def join_csv(s: Iterable[str]) -> str:
    """Join strings in list to comma-separated values.
    Inverse of ``split_csv``.

    :param s: list to join
    :return: joined csv string
    """
    return ','.join(s)


def quote_help(s: str) -> str:
    """Double percent signs, and quote newlines.
    This is needed in help for argparse.
    """
    return s.replace('%', '%%').replace('\n', '\\n')
