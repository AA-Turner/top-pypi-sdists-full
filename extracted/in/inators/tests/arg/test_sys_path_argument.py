# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest
import sys

from inators import arg as inators_arg

from common_arg import _test_add_argument, MockNamespace


@pytest.mark.parametrize('func_args, func_kwargs, sys_argv, exp', [
    ([], {}, [], {'sys_path': []}),
    ([], {}, ['--sys-path', 'foo'], {'sys_path': ['foo']}),
    ([], {}, ['--sys-path', 'foo', '--sys-path', 'bar'], {'sys_path': ['foo', 'bar']}),
    (['-L'], {}, ['-L', 'foo'], {'sys_path': ['foo']}),
    ([(), '--pythonpath'], {}, ['--pythonpath', 'foo'], {'sys_path': ['foo']}),
    ([], {'short_alias': '-L'}, ['-L', 'foo'], {'sys_path': ['foo']}),
    ([], {'long_alias': '--pythonpath'}, ['--pythonpath', 'foo'], {'sys_path': ['foo']}),
])
def test_add_sys_path_argument(func_args, func_kwargs, sys_argv, exp):
    _test_add_argument(inators_arg.add_sys_path_argument, func_args, func_kwargs, sys_argv, exp)


@pytest.mark.parametrize('add_paths, exp_added_paths', [
    ([], []),
    ([sys.path[0]], []),
    (['foo'], ['foo']),
    (['foo', 'foo'], ['foo']),
    (['bar', 'baz'], ['bar', 'baz']),
])
def test_process_sys_path_argument(add_paths, exp_added_paths):
    orig_sys_path = sys.path[:]
    args = MockNamespace(sys_path=add_paths)
    inators_arg.process_sys_path_argument(args)
    added_paths = [path for path in sys.path if path not in orig_sys_path]
    sys.path[:] = orig_sys_path
    assert added_paths == exp_added_paths
