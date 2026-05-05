import pytest

from pyjsg.jsglib.loader import is_valid


def test_default_context():
    from ShExJSG import Schema

    schema = Schema()
    schema.start = "blabla"
    assert is_valid(schema)
