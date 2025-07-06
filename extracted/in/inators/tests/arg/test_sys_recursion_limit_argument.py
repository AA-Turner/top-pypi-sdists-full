# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest
import sys

from inators import arg as inators_arg

from common_arg import _test_add_argument, MockArgumentParserError, MockNamespace


@pytest.mark.parametrize('func_args, func_kwargs, sys_argv, exp', [
    ([], {}, [], {'sys_recursion_limit': sys.getrecursionlimit()}),
    ([], {}, ['--sys-recursion-limit', '42'], {'sys_recursion_limit': 42}),
    ([], {}, ['--sys-recursion-limit', 'foo'], MockArgumentParserError),
    (['-R'], {}, ['-R', '42'], {'sys_recursion_limit': 42}),
    ([(), '--stacksize'], {}, ['--stacksize', '42'], {'sys_recursion_limit': 42}),
    ([], {'short_alias': '-R'}, ['-R', '42'], {'sys_recursion_limit': 42}),
    ([], {'long_alias': '--stacksize'}, ['--stacksize', '42'], {'sys_recursion_limit': 42}),
    ([], {'default': 42}, [], {'sys_recursion_limit': 42}),
])
def test_add_sys_recursion_limit_argument(func_args, func_kwargs, sys_argv, exp):
    _test_add_argument(inators_arg.add_sys_recursion_limit_argument, func_args, func_kwargs, sys_argv, exp)


@pytest.mark.parametrize('arg_limit', [
    sys.getrecursionlimit() + 1,
])
def test_process_sys_recursion_limit_argument(arg_limit):
    orig_limit = sys.getrecursionlimit()
    args = MockNamespace(sys_recursion_limit=arg_limit)
    inators_arg.process_sys_recursion_limit_argument(args)
    new_limit = sys.getrecursionlimit()
    sys.setrecursionlimit(orig_limit)
    assert new_limit == arg_limit
