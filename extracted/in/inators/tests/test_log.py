# Copyright (c) 2021 Renata Hodovan, Akos Kiss.
#
# Licensed under the BSD 3-Clause License
# <LICENSE.rst or https://opensource.org/licenses/BSD-3-Clause>.
# This file may not be copied, modified, or distributed except
# according to those terms.

import io
import logging
import pytest

from inators import log as inators_log


@pytest.mark.parametrize('level, value', [
    ('TRACE', inators_log.TRACE),
    ('DEBUG', logging.DEBUG),
    ('INFO', logging.INFO),
    ('WARNING', logging.WARNING),
    ('ERROR', logging.ERROR),
    ('CRITICAL', logging.CRITICAL),
    ('DISABLE', inators_log.DISABLE),
])
def test_level_names(level, value):
    assert inators_log.levels[level] == value


@pytest.mark.parametrize('logger_level, msg_level, enabled', [
    (inators_log.TRACE, inators_log.TRACE, True),
    (inators_log.TRACE, logging.DEBUG, True),
    (logging.DEBUG, inators_log.TRACE, False),
    (inators_log.DISABLE, inators_log.TRACE, False),
    (inators_log.DISABLE, logging.CRITICAL, False),
])
def test_level_values(logger_level, msg_level, enabled):
    logger = logging.getLogger('{}.logger{}'.format(__name__, logger_level))
    logger.setLevel(logger_level)
    assert logger.isEnabledFor(msg_level) == enabled


@pytest.mark.parametrize('logger_level, msg, output', [
    (inators_log.TRACE, u'foo', u'foo\n'),
    (inators_log.DEBUG, u'bar', u''),
    (inators_log.DISABLE, u'baz', u''),
])
def test_trace(logger_level, msg, output):
    logger = inators_log.getLogger('{}.trace'.format(__name__))
    logger.setLevel(logger_level)
    stream = io.StringIO()
    logger.addHandler(logging.StreamHandler(stream=stream))
    logger.trace(msg)
    assert stream.getvalue() == output
