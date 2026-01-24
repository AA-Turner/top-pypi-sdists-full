from __future__ import annotations

from hypothesis import given
from hypothesis.strategies import text
from pytest import mark, param

from libapi.jsonpointer import escape_jsonpointer, unescape_jsonpointer
from libapi.uritemplate import pct_encode


@mark.parametrize(
    'a, b',
    [
        # unreserved = A-Z / a-z / 0-9 / - / . / _ / ~
        param('', '', id='zero-length'),
        param('hello123', 'hello123', id='no-encode'),
        param('hello world', 'hello%20world', id='encode-space'),
        param('1% rule', '1%25%20rule', id='encode-percent'),
        param('hello%20world', 'hello%2520world', id='encode-percent-encoded'),
        param(
            ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
            '%20%21%22%23%24%25%26%27%28%29%2A%2B%2C-.%2F%3A%3B%3C%3D%3E%3F%40%5B%5C%5D%5E_%60%7B%7C%7D~',
            id='encode-special',
        ),
        param('你好', '%E4%BD%A0%E5%A5%BD', id='encode-multibyte'),
    ],
)
def test_pct_encode(a: str, b: str):
    assert pct_encode(a) == b


@mark.parametrize(
    'a, b',
    [
        param('', '', id='zero-length'),
        param('hello123', 'hello123', id='no-encode'),
        param('hello world', 'hello%20world', id='encode-space'),
        param('1% rule', '1%25%20rule', id='encode-percent'),
        param('hello%20world', 'hello%20world', id='encode-percent-encoded'),
        param(
            ' !"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~',
            '%20!%22#$%25&\'()*+,-./:;%3C=%3E?@[%5C]%5E_%60%7B%7C%7D~',
            id='encode-special',
        ),
        param('你好', '%E4%BD%A0%E5%A5%BD', id='encode-multibyte'),
    ],
)
def test_pct_encode_reserved(a: str, b: str):
    assert pct_encode(a, reserved_expansion=True) == b


@mark.parametrize(
    'a, b',
    [
        param('', '', id='zero-length'),
        param('hello world', 'hello world', id='unescaped'),
        param('hello~0/world~1', 'hello~00~1world~01', id='escaped'),
    ],
)
def test_escape_jsonpointer(a: str, b: str):
    assert escape_jsonpointer(a) == b


@mark.parametrize(
    'a, b',
    [
        param('', '', id='zero-length'),
        param('hello world', 'hello world', id='unescaped'),
        param('hello~00~1world~01', 'hello~0/world~1', id='escaped'),
    ],
)
def test_unescape_jsonpointer(a: str, b: str):
    assert unescape_jsonpointer(a) == b


@given(text())
def test_escape_jsonpointer_roundtrip(a: str):
    assert unescape_jsonpointer(escape_jsonpointer(a)) == a
