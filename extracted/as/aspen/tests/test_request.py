from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from six import text_type

from aspen.http.request import Path, Querystring


# Path
# ====

def test_path_starts_empty():
    path = Path("/bar.html")
    assert path == {}, path

def test_path_has_raw_set():
    path = Path("/bar.html")
    assert path.raw == "/bar.html", path.raw

def test_path_raw_is_unicode():
    path = Path("/bar.html")
    assert isinstance(path.raw, text_type)

def test_path_has_decoded_set():
    path = Path("/b%c3%a4r.html")
    assert path.decoded == "/b\u00e4r.html", path.decoded

def test_path_decoded_is_unicode():
    path = Path("/bar.html")
    assert isinstance(path.decoded, text_type)

def test_path_unquotes_and_decodes_UTF_8():
    path = Path("/%e2%98%84.html")
    assert path.decoded == "/\u2604.html", path.decoded

def test_path_doesnt_unquote_plus():
    path = Path("/+%2B.html")
    assert path.decoded == "/++.html", path.decoded

def test_path_has_parts():
    path = Path("/foo/bar.html")
    assert path.parts == ['foo', 'bar.html']


# Path params
# ===========

def _extract_params(path):
#    return dispatcher.extract_rfc2396_params(path.lstrip('/').split('/'))
    params = [ segment.params for segment in path.parts ]
    segments = [ str(segment) for segment in path.parts ]
    return ( segments, params )

def test_extract_path_params_with_none():
    path = Path("/foo/bar")
    actual = _extract_params(path)
    expected = (['foo', 'bar'], [{}, {}])
    assert actual == expected

def test_extract_path_params_simple():
    path = Path("/foo;a=1;b=2;c/bar;a=2;b=1")
    actual = _extract_params(path)
    expected = (['foo', 'bar'], [{'a':['1'], 'b':['2'], 'c':['']}, {'a':['2'], 'b':['1']}])
    assert actual == expected

def test_extract_path_params_complex():
    path = Path("/foo;a=1;b=2,3;c;a=2;b=4/bar;a=2,ab;b=1")
    actual = _extract_params(path)
    expected = (['foo', 'bar'], [{'a':['1','2'], 'b':['2,3', '4'], 'c':['']}, {'a':[ '2,ab' ], 'b':['1']}])
    assert actual == expected

def test_path_params_api():
    path = Path("/foo;a=1;b=2;b=3;c/bar;a=2,ab;b=1")
    parts, params = (['foo', 'bar'], [{'a':['1'], 'b':['2', '3'], 'c':['']}, {'a':[ '2,ab' ], 'b':['1']}])
    assert path.parts == parts, path.parts
    assert path.parts[0].params == params[0]
    assert path.parts[1].params == params[1]


# Querystring
# ===========

def test_querystring_starts_full():
    querystring = Querystring("baz=buz")
    assert querystring == {'baz': ['buz']}, querystring

def test_querystring_has_raw_set():
    querystring = Querystring("baz=buz")
    assert querystring.raw == "baz=buz", querystring.raw

def test_querystring_raw_is_unicode():
    querystring = Querystring("baz=buz")
    assert isinstance(querystring.raw, text_type)

def test_querystring_has_decoded_set():
    querystring = Querystring("baz=buz")
    assert querystring.decoded == "baz=buz", querystring.decoded

def test_querystring_decoded_is_unicode():
    querystring = Querystring("baz=buz")
    assert isinstance(querystring.decoded, text_type)

def test_querystring_unquotes_and_decodes_UTF_8():
    querystring = Querystring("baz=%e2%98%84")
    assert querystring.decoded == "baz=\u2604", querystring.decoded

def test_querystring_comes_out_UTF_8():
    querystring = Querystring("baz=%e2%98%84")
    assert querystring['baz'] == "\u2604", querystring['baz']

def test_querystring_doesnt_choke_on_bad_unicode():
    querystring = Querystring("baz%e2%98=%e2%98")
    assert querystring['baz\ufffd'] == '\ufffd'

def test_querystring_unquotes_plus():
    querystring = Querystring("baz=+%2B")
    assert querystring.decoded == "baz= +", querystring.decoded
    assert querystring['baz'] == " +"
