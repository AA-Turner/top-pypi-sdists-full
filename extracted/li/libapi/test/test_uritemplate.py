from __future__ import annotations

from pytest import mark, param

from libapi.uritemplate import URITemplate

values = {
    'var': 'value',
    'hello': 'hello world!',
    'hello_enc': 'hello%20world%21',
    'one': '1% rule',
    'three': 3,
    'path': 'usr/bin/env',
    'zero_length': '',
    'nil': None,
    'unused': 'unused',
}


@mark.parametrize(
    'a, b',
    [
        # Simple String Expansion: {var}
        param('{var}', 'value', id='var'),
        param('{var}{var}', 'valuevalue', id='var_twice'),
        param('{hello}', 'hello%20world%21', id='hello'),
        param('{hello_enc}', 'hello%2520world%2521', id='hello_encoded'),
        param('{one}', '1%25%20rule', id='one'),
        param('{three}', '3', id='three'),
        param('{path}', 'usr%2Fbin%2Fenv', id='path'),
        param('{zero_length}', '', id='zero_length'),
        param('{nil}', '', id='nil'),
        param('{undef}', '', id='undef'),
    ],
)
def test_expand(a: str, b: str):
    assert URITemplate(a).expand(values) == b


@mark.parametrize(
    'a, b',
    [
        # Reserved Expansion: {+var}
        param('{+var}', 'value', id='var'),
        param('{+var}{+var}', 'valuevalue', id='var_twice'),
        param('{+hello}', 'hello%20world!', id='hello'),
        param('{+hello_enc}', 'hello%20world%21', id='hello_encoded'),
        param('{+one}', '1%25%20rule', id='one'),
        param('{+three}', '3', id='three'),
        param('{+path}', 'usr/bin/env', id='path'),
        param('{+zero_length}', '', id='zero_length'),
        param('{+nil}', '', id='nil'),
        param('{+undef}', '', id='undef'),
    ],
)
def test_expand_reserved(a: str, b: str):
    assert URITemplate(a).expand(values) == b


@mark.parametrize(
    'a, b',
    [
        # Fragment Expansion: {#var}
        param('{#var}', '#value', id='var'),
        param('{#var}{#var}', '#value#value', id='var_twice'),
        param('{#hello}', '#hello%20world!', id='hello'),
        param('{#hello_enc}', '#hello%20world%21', id='hello_encoded'),
        param('{#one}', '#1%25%20rule', id='one'),
        param('{#three}', '#3', id='three'),
        param('{#path}', '#usr/bin/env', id='path'),
        param('{#zero_length}', '#', id='zero_length'),
        param('{#nil}', '', id='nil'),
        param('{#undef}', '', id='undef'),
    ],
)
def test_expand_fragment(a: str, b: str):
    assert URITemplate(a).expand(values) == b


@mark.parametrize(
    'a, b',
    [
        # Simple String Expansion: {var}
        param('{zero_length}', '', id='zero_length'),
        param('{nil}', '{nil}', id='nil'),
        param('{undef}', '{undef}', id='undef'),
        param('{var}{nil}', 'value{nil}', id='var_nil'),
        param('{var}{undef}', 'value{undef}', id='var_undef'),
        # Reserved Expansion: {+var}
        param('{+zero_length}', '', id='zero_length_reserved'),
        param('{+nil}', '{+nil}', id='nil_reserved'),
        param('{+undef}', '{+undef}', id='undef_reserved'),
        param('{+var}{+nil}', 'value{+nil}', id='var_nil_reserved'),
        param('{+var}{+undef}', 'value{+undef}', id='var_undef_reserved'),
        # Fragment Expansion: {#var}
        param('{#zero_length}', '#', id='zero_length_fragment'),
        param('{#nil}', '{#nil}', id='nil_fragment'),
        param('{#undef}', '{#undef}', id='undef_fragment'),
        param('{#var}{#nil}', '#value{#nil}', id='var_nil_fragment'),
        param('{#var}{#undef}', '#value{#undef}', id='var_undef_fragment'),
    ],
)
def test_expand_partial(a: str, b: str):
    assert URITemplate(a).expand(values, partial=True) == b
