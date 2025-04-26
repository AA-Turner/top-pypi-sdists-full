#!/usr/bin/env python
# -*- coding: utf-8 -*-
###############################################################################
# (c) Copyright 2018 CERN                                                     #
#                                                                             #
# This software is distributed under the terms of the GNU General Public      #
# Licence version 3 (GPL Version 3), copied verbatim in the file "LICENSE".   #
#                                                                             #
# In applying this licence, CERN does not waive the privileges and immunities #
# granted to it by virtue of its status as an Intergovernmental Organization  #
# or submit itself to any jurisdiction.                                       #
###############################################################################
from __future__ import print_function
from __future__ import absolute_import
__author__ = "Marco Clemencic <marco.clemencic@cern.ch>"

import os
import sys

assert sys.version_info >= (2, 7), "Python 2.7 required"

import logging

from string import Template

__all__ = []

# Prepare the search path for environment XML files
path = ['.']
if 'ENVXMLPATH' in os.environ:
    path.extend(os.environ['ENVXMLPATH'].split(os.pathsep))

from . import Control

try:
    from pkg_resources import get_distribution, DistributionNotFound
    try:
        __version__ = get_distribution(__name__).version
    except DistributionNotFound:  # pragma: no cover
        # package is not installed
        __version__ = 'unknown'
except ImportError:  # pragma: no cover
    # we are not using setuptools
    __version__ = 'unkown'


class EnvError(RuntimeError):
    '''
    Simple class to wrap errors in the environment configuration.
    '''
    pass


def splitNameValue(name_value):
    """split the "NAME=VALUE" string into the tuple ("NAME", "VALUE")
    replacing '[:]' with os.pathsep in VALUE"""
    if '=' not in name_value:
        raise EnvError("Invalid variable argument '%s'." % name_value)
    n, v = name_value.split('=', 1)
    return n, v.replace('[:]', os.pathsep)


class Script(object):
    '''
    Environment Script class used to control the logic of the script and allow
    extensions.
    '''
    __usage__ = "Usage: %(prog)s [OPTION]... [NAME=VALUE]... [COMMAND [ARG ...]]"
    __desc__ = "Set each NAME to VALUE in the environment and run COMMAND."
    __epilog__ = (
        "The operations are performed in the order they appear on the "
        "command line. If no COMMAND is provided, print the resulting "
        "environment. (Note: this command is modeled after the Unix "
        "command 'env', see \"man env\")")

    def __init__(self, args=None, prog=None):
        '''
        Initializes the script instance parsing the command line arguments (or
        the explicit arguments provided).
        '''
        self.prog = prog or os.path.basename(sys.argv[0])
        self.parser = None
        self.args = None
        self.control = None
        self.log = None
        self.env = {}
        # Run the core code of the script
        self._prepare_parser()
        self._parse_args(args)
        self._check_args()

    def _prepare_parser(self, version=None):
        '''
        Prepare an OptionParser instance used to analyze the command line
        options and arguments.
        '''
        import argparse
        parser = argparse.ArgumentParser(
            prog=self.prog,
            usage=self.__usage__,
            description=self.__desc__,
            epilog=self.__epilog__)
        self.log = logging.getLogger(parser.prog)

        parser.add_argument(
            '--version',
            action='version',
            version=version or '%(prog)s {}'.format(__version__))

        class OperationAction(argparse.Action):
            '''
            Append to the list of actions the tuple (action, (<args>, ...)).
            '''

            def __init__(self, option_strings, dest, **kwargs):
                dest = 'actions'
                kwargs['nargs'] = 1

                self.operation = [
                    op[2:] for op in option_strings if op.startswith('--')
                ][0]
                if self.operation == 'xml':
                    self.operation = 'loadXML'
                super(OperationAction, self).__init__(option_strings, dest,
                                                      **kwargs)

            def __call__(self, parser, namespace, values, option_string):
                value = values[0]
                if self.operation not in ('unset', 'loadXML'):
                    try:
                        value = splitNameValue(value)
                    except EnvError:
                        parser.error(
                            ("Invalid value for option %s: '%s', it "
                             "requires NAME=VALUE.") % (option_string, value))
                else:
                    value = (value, )
                namespace.actions.append((self.operation, value))

        parser.add_argument(
            'command',
            nargs=argparse.REMAINDER,
            metavar='COMMAND [ARG ...]',
            help='command to execute, if not spcified, print the environment')
        parser.add_argument(
            "-i",
            "--ignore-environment",
            action="store_true",
            help="start with an empty environment")
        parser.add_argument(
            "-u",
            "--unset",
            metavar="NAME",
            action=OperationAction,
            help="remove variable from the environment")
        parser.add_argument(
            "-s",
            "--set",
            metavar="NAME=VALUE",
            action=OperationAction,
            help="set the variable NAME to VALUE")
        parser.add_argument(
            "-a",
            "--append",
            metavar="NAME=VALUE",
            action=OperationAction,
            help="append VALUE to the variable NAME (with a '%s' as separator)"
            % os.pathsep)
        parser.add_argument(
            "-p",
            "--prepend",
            metavar="NAME=VALUE",
            action=OperationAction,
            help="prepend VALUE to the variable NAME "
            "(with a '%s' as separator)" % os.pathsep)
        parser.add_argument(
            "-x",
            "--xml",
            action=OperationAction,
            help="XML file describing the changes to the environment")
        parser.add_argument(
            "--sh",
            action="store_const",
            const="sh",
            dest="shell",
            help="Print the changes to the environment as shell commands for "
            "'sh'-derived shells.")
        parser.add_argument(
            "--csh",
            action="store_const",
            const="csh",
            dest="shell",
            help="Print the changes to the environment as shell commands for "
            "'csh'-derived shells.")
        parser.add_argument(
            "--py",
            action="store_const",
            const="py",
            dest="shell",
            help="Print the changes to the environment as Python dictionary.")
        parser.add_argument(
            "-A",
            "--all",
            action="store_true",
            help="Print all variables, instead of just the changes, "
            "with --sh, --csh and --py.")

        parser.add_argument(
            '--verbose',
            action='store_const',
            const=logging.INFO,
            dest='log_level',
            help='print more information')
        parser.add_argument(
            '--debug',
            action='store_const',
            const=logging.DEBUG,
            dest='log_level',
            help='print debug messages')
        parser.add_argument(
            '--quiet',
            action='store_const',
            const=logging.WARNING,
            dest='log_level',
            help='print only warning messages (default)')

        parser.set_defaults(
            actions=[], ignore_environment=False, log_level=logging.WARNING)

        self.parser = parser

    def _parse_args(self, args=None):
        '''
        Parse the command line arguments.
        '''
        self.args = self.parser.parse_args(args)

        # set the logging level
        logging.basicConfig(level=self.args.log_level)

        # find the (implicit) 'set' arguments in the list of arguments
        # and put the rest in the command
        i = 0
        try:
            for i, a in enumerate(self.args.command):
                self.args.actions.append(('set', splitNameValue(a)))
        except EnvError:
            i -= 1
        self.args.command = self.args.command[(i + 1):]

    def _check_args(self):
        '''
        Check consistency of command line options and arguments.
        '''
        if self.args.shell and self.args.command:
            self.parser.error(
                "Invalid arguments: --%s cannot be used with a command." %
                self.args.shell)

    def _makeEnv(self):
        '''
        Generate a dictionary of the environment variables after applying all
        the required actions.
        '''
        # prepare the environment control instance
        control = Control.Environment()
        if not self.args.ignore_environment:
            control.presetFromSystem()

        # apply all the actions
        for action, args in self.args.actions:
            getattr(control, action)(*args)

        # extract the result env dictionary
        env = control.vars()

        # set the library search path correctly for the non-Linux platforms
        if "LD_LIBRARY_PATH" in env:
            # replace LD_LIBRARY_PATH with the corresponding one on other systems
            if sys.platform.startswith("win"):
                other = "PATH"
            else:
                other = None
            if other:
                if other in env:
                    env[other] = env[other] + \
                        os.pathsep + env["LD_LIBRARY_PATH"]
                else:
                    env[other] = env["LD_LIBRARY_PATH"]
                del env["LD_LIBRARY_PATH"]

        self.env = env

    def dump(self):
        '''
        Print to standard output the final environment in the required format.
        '''
        if not self.args.shell or self.args.all:
            # 'env' behaviour: print the whole environment
            env = self.env
        else:
            # special dumps: print only the diffs
            env = dict((name, value)
                       for name, value in sorted(self.env.items())
                       if os.environ.get(name) != value)

        if self.args.shell == 'py':
            from pprint import pprint
            pprint(env)
        else:
            template = {
                'sh': "export {0}='{1}'",
                'csh': "setenv {0} '{1}';"
            }.get(self.args.shell, "{0}={1}")
            print('\n'.join(
                template.format(name, value)
                for name, value in sorted(env.items())))

    def expandEnvVars(self, iterable):
        '''
        Return a copy of iterable where all the elements have the environment
        variables expanded.

        >>> s = Script([])
        >>> s.env = {'A': '1', 'B': 'test'}
        >>> s.expandEnvVars(['$A', '${B}-$A', '$DUMMY-$A', '$$B'])
        ['1', 'test-1', '$DUMMY-1', '$B']
        '''
        return [Template(elem).safe_substitute(self.env) for elem in iterable]

    def runCmd(self):
        '''
        Execute a command in the modified environment and return the exit code.
        '''
        from subprocess import Popen
        cmd = self.expandEnvVars(self.args.command)
        try:
            proc = Popen(cmd, env=self.env)
        except OSError as x:
            print(
                '{0}: {1}: {2}'.format(sys.argv[0], cmd[0], x.strerror),
                file=sys.stderr)
            sys.exit(127)
        while proc.poll() is None:
            try:
                proc.wait()
            except KeyboardInterrupt:
                self.log.fatal(
                    'KeyboardInterrupt, '
                    'waiting for subprocess %d to end', proc.pid)
        rc = proc.returncode
        # There is a mismatch between Popen return code and sys.exit argument in
        # case of signal.
        # E.g. Popen returns -6 that is translated to 250 instead of 134
        return rc if rc >= 0 else 128 - rc

    def main(self):
        '''
        Main function of the script.
        '''
        self._makeEnv()
        if not self.args.command:
            self.dump()
        else:
            sys.exit(self.runCmd())


def main():
    Script().main()
