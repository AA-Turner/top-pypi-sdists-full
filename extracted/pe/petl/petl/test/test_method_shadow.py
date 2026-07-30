"""
Regression tests for Table subclasses whose stored ``header`` argument
shadowed the inherited ``Table.header()`` method, so calling the fluent
``.header()`` raised ``TypeError: '...' object is not callable``.

See issue #555 (fixed the same collision on ``fromdicts``) and PR #697.
"""

from __future__ import absolute_import, print_function, division


import json as _json
from tempfile import NamedTemporaryFile


import pytest


import petl as etl
from petl.compat import PY2
from petl.test.helpers import eq_


def _csvfile(text):
    f = NamedTemporaryFile(mode='w', suffix='.csv', delete=False, newline='')
    f.write(text)
    f.close()
    return f.name


def _textfile(text):
    f = NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
    f.write(text)
    f.close()
    return f.name


def _jsonfile(obj):
    f = NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    f.write(_json.dumps(obj))
    f.close()
    return f.name


@pytest.mark.skipif(PY2, reason='NamedTemporaryFile newline kwarg is Python 3 only')
def test_fromcsv_header():
    t = etl.fromcsv(_csvfile('foo,bar\r\n1,2\r\n'))
    eq_(('foo', 'bar'), t.header())


def test_fromtext_header():
    t = etl.fromtext(_textfile('line one\nline two\n'))
    eq_(('lines',), t.header())


def test_fromjson_header():
    t = etl.fromjson(_jsonfile([{'foo': 1, 'bar': 2}]), header=['foo', 'bar'])
    eq_(('foo', 'bar'), t.header())


def test_fromcolumns_header():
    t = etl.fromcolumns([[1, 2], [3, 4]], ['a', 'b'])
    eq_(('a', 'b'), t.header())


def test_cat_header():
    a = etl.wrap([['foo', 'bar'], [1, 2]])
    b = etl.wrap([['foo', 'baz'], [3, 4]])
    t = etl.cat(a, b, header=['foo', 'bar', 'baz'])
    eq_(('foo', 'bar', 'baz'), t.header())


def test_pushheader_header():
    t = etl.pushheader(etl.wrap([[1, 2]]), ['foo', 'bar'])
    eq_(('foo', 'bar'), t.header())


def test_setheader_header():
    t = etl.setheader(etl.wrap([['foo', 'bar'], [1, 2]]), ['a', 'b'])
    eq_(('a', 'b'), t.header())


def test_rowmap_header():
    src = etl.wrap([['foo', 'bar'], [1, 2]])
    t = etl.rowmap(src, lambda row: [row[0]], header=['foo'])
    eq_(('foo',), t.header())


def test_rowmapmany_header():
    src = etl.wrap([['foo', 'bar'], [1, 2]])
    t = etl.rowmapmany(src, lambda row: [[row[0]]], header=['foo'])
    eq_(('foo',), t.header())


def test_rowgroupmap_header():
    src = etl.wrap([['foo', 'bar'], [1, 2]])
    t = etl.rowgroupmap(src, 'foo', lambda k, rows: [[k]], header=['foo'])
    eq_(('foo',), t.header())


def test_rowreduce_header():
    src = etl.wrap([['foo', 'bar'], [1, 2]])
    t = etl.rowreduce(src, 'foo', lambda k, rows: [k], header=['foo'])
    eq_(('foo',), t.header())


def test_mergesort_header():
    a = etl.wrap([['foo', 'bar'], [1, 2]])
    b = etl.wrap([['foo', 'bar'], [3, 4]])
    t = etl.mergesort(a, b, key='foo')
    eq_(('foo', 'bar'), t.header())


def test_validate_header():
    src = etl.wrap([['foo', 'bar'], [1, 2]])
    t = etl.validate(src, header=['foo', 'bar'])
    eq_(('name', 'row', 'field', 'value', 'error'), t.header())


def test_method_matches_function_form():
    # the fluent method must agree with the etl.header() function
    t = etl.fromcolumns([[1, 2]], ['a'])
    eq_(etl.header(t), t.header())
