# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import logging
import pytest

from inators import arg as inators_arg
from inators import log as inators_log

from common_arg import _test_add_argument, MockArgumentParserError, MockNamespace


@pytest.mark.parametrize('func_args, func_kwargs, sys_argv, exp', [
    ([], {}, [], {'log_level': 'INFO'}),
    ([], {}, ['--log-level', 'WARNING'], {'log_level': 'WARNING'}),
    ([], {}, ['-l', 'WARNING'], {'log_level': 'WARNING'}),
    ([], {}, ['--verbose'], {'log_level': 'DEBUG'}),
    ([], {}, ['-v'], {'log_level': 'DEBUG'}),
    ([], {}, ['--quiet'], {'log_level': 'DISABLE'}),
    ([], {}, ['-q'], {'log_level': 'DISABLE'}),
    ([], {}, ['--log-level', 'FOO'], MockArgumentParserError),
    ([()], {}, ['-l', 'WARNING'], MockArgumentParserError),
    ([(), '--logging'], {}, ['--logging', 'WARNING'], {'log_level': 'WARNING'}),
    ([], {'short_alias': ()}, ['-l', 'WARNING'], MockArgumentParserError),
    ([], {'long_alias': '--logging'}, ['--logging', 'WARNING'], {'log_level': 'WARNING'}),
    ([], {'choices': ['INFO']}, ['--log-level', 'DEBUG'], MockArgumentParserError),
    ([], {'default': 'WARNING'}, [], {'log_level': 'WARNING'}),
    ([], {'verbose_alias': ()}, ['--verbose'], MockArgumentParserError),
    ([], {'verbose_const': 'TRACE'}, ['--verbose'], {'log_level': 'TRACE'}),
    ([], {'quiet_alias': ()}, ['--quiet'], MockArgumentParserError),
    ([], {'quiet_const': 'CRITICAL'}, ['--quiet'], {'log_level': 'CRITICAL'}),
])
def test_add_log_level_argument(func_args, func_kwargs, sys_argv, exp):
    _test_add_argument(inators_arg.add_log_level_argument, func_args, func_kwargs, sys_argv, exp)


@pytest.mark.parametrize('level_name, exp_level_value', [
    ('TRACE', inators_log.TRACE),
    ('INFO', logging.INFO),
    ('DISABLE', inators_log.DISABLE),
])
def test_process_log_level_argument(level_name, exp_level_value):
    args = MockNamespace(log_level=level_name)
    logger = logging.getLogger('{}.logger{}'.format(__name__, level_name))
    inators_arg.process_log_level_argument(args, logger)
    assert logger.getEffectiveLevel() == exp_level_value
