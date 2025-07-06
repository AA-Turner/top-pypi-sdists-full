# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import argparse
import pytest


class MockArgumentParserExit(Exception):
    pass


class MockArgumentParserError(Exception):
    pass


class MockArgumentParser(argparse.ArgumentParser):

    def exit(self, status=0, message=None):
        raise MockArgumentParserError(message) if status else MockArgumentParserExit(message)


def _test_add_argument(add_argument_func, func_args, func_kwargs, sys_argv, exp):
    parser = MockArgumentParser()
    add_argument_func(parser, *func_args, **func_kwargs)

    if isinstance(exp, type):
        with pytest.raises(exp):
            parser.parse_args(sys_argv)
    else:
        args = parser.parse_args(sys_argv)
        for key, value in exp.items():
            assert getattr(args, key) == value


class MockNamespace(object):

    def __init__(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)
