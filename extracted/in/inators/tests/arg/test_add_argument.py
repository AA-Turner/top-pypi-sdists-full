# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import pytest

from inators import arg as inators_arg

from common_arg import _test_add_argument


@pytest.mark.parametrize('func_args, func_kwargs, sys_argv, exp', [
    (['--foo'], {}, ['--foo', '42'], {'foo': '42'}),
    ([('--foo',)], {}, ['--foo', '42'], {'foo': '42'}),
    ([['--foo']], {}, ['--foo', '42'], {'foo': '42'}),
    (['--foo', '--bar'], {}, ['--bar', '42'], {'foo': '42'}),
    ([('--foo', '--bar')], {}, ['--bar', '42'], {'foo': '42'}),
    ([['--foo', '--bar']], {}, ['--bar', '42'], {'foo': '42'}),
    (['--foo', (), ('--bar',), [], ['--baz']], {}, ['--baz', '42'], {'foo': '42'}),
])
def test_add_argument(func_args, func_kwargs, sys_argv, exp):
    _test_add_argument(inators_arg.add_argument, func_args, func_kwargs, sys_argv, exp)
