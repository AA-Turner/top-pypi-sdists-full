# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from pytest import raises
from six import PY2


def test_with_non_ascii_bytes_and_without_encoding(harness):
    harness.fs.www.mk(('index.spt', """
        [------------------]
        text = u'א'
        [------------------] text/plain
        %(text)s
    """, 'utf8'))
    if PY2:
        with raises(UnicodeDecodeError):
            harness.hit('/')
    else:
        output = harness.hit('/')
        assert output.text.strip() == 'א'

def test_non_ascii_bytes_work_with_encoding(harness):
    expected = 'א'.encode('utf8')
    actual = harness.simple(("""
        # encoding=utf8
        [------------------]
        text = u'א'
        [------------------]
        %(text)s
    """, 'utf8')).body.strip()
    assert actual == expected

def test_the_exec_machinery_handles_two_encoding_lines_properly(harness):
    expected = 'א'.encode('utf8')
    actual = harness.simple(("""\
        # encoding=utf8
        # encoding=ascii
        [------------------]
        text = u'א'
        [------------------]
        %(text)s
    """, 'utf8')).body.strip()
    assert actual == expected
