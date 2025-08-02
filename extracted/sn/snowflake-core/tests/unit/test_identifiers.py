from unittest.mock import MagicMock

import pytest

from snowflake.core._identifiers import FQN
from snowflake.core.exceptions import InvalidIdentifierError


def test_attributes():
    fqn = FQN(name="object_name", database="database_name", schema="schema_name")
    assert fqn.database == "database_name"
    assert fqn.schema == "schema_name"
    assert fqn.name == "object_name"


@pytest.mark.parametrize(
    "fqn, identifier",
    [
        (FQN(name="name", database="db", schema="schema"), "db.schema.name"),
        (FQN(name='"my_object"', database="db", schema="schema"), 'db.schema."my_object"'),
        (FQN(name="name", database=None, schema="schema"), "schema.name"),
        (FQN(name="name", database=None, schema=None), "name"),
        (FQN(name="name", database="db", schema=None), "db.PUBLIC.name"),
        (FQN(name="name(float, string)", database="db", schema=None), "db.PUBLIC.name(float, string)"),
    ],
)
def test_identifier(fqn, identifier):
    assert fqn.identifier == identifier


def test_eq():
    fqn1 = FQN(name="name", database="db", schema="schema")
    fqn2 = FQN(name="name", database="db", schema="schema")
    assert fqn1 == fqn2
    assert fqn2 == fqn1


def test_neq():
    fqn1 = FQN(name="name", database="db", schema="schema")
    fqn2 = FQN(name="other-name", database="db", schema="schema")
    assert fqn1 != fqn2
    assert fqn2 != fqn1


def test_eq_with_different_type():
    assert FQN(name="name", database="db", schema="schema") != "db.schema.name"


def test_set_database():
    fqn = FQN(name="name", database="db", schema="schema")
    fqn.set_database("foo")
    assert fqn.database == "foo"


def test_set_schema():
    fqn = FQN(name="name", database="db", schema="schema")
    fqn.set_schema("foo")
    assert fqn.schema == "foo"


def test_set_name():
    fqn = FQN(name="name", database="db", schema="schema")
    fqn.set_name("foo")
    assert fqn.name == "foo"


@pytest.mark.parametrize(
    "fqn_str, identifier",
    [
        ("db.schema.name", "db.schema.name"),
        ("DB.SCHEMA.NAME", "DB.SCHEMA.NAME"),
        ("schema.name", "schema.name"),
        ("name", "name"),
        ('"name with space"', '"name with space"'),
        ('"dot.db"."dot.schema"."dot.name"', '"dot.db"."dot.schema"."dot.name"'),
        ('"dot.db".schema."dot.name"', '"dot.db".schema."dot.name"'),
        ('db.schema."dot.name"', 'db.schema."dot.name"'),
        ('"dot.db".schema."DOT.name"', '"dot.db".schema."DOT.name"'),
        # Nested quotes
        ('"abc""this is in nested quotes"""', '"abc""this is in nested quotes"""'),
        # Callables
        ("db.schema.function(string, int, variant)", "db.schema.function"),
        ('db.schema."fun tion"(string, int, variant)', 'db.schema."fun tion"'),
    ],
)
def test_from_string(fqn_str, identifier):
    fqn = FQN.from_string(fqn_str)
    assert fqn.identifier == identifier
    if fqn.signature:
        assert fqn.signature == "(string, int, variant)"


@pytest.mark.parametrize(
    "fqn_str",
    [
        "db.schema.name.foo",
        "schema. name",
        "name with space",
        'dot.db."dot.schema"."dot.name"',
        '"dot.db.schema."dot.name"',
    ],
)
def test_from_string_fails_if_pattern_does_not_match(fqn_str):
    with pytest.raises(InvalidIdentifierError) as err:
        FQN.from_string(fqn_str)

    assert str(err.value) == f"'{fqn_str}' is not a valid identifier."


def test_using_connection():
    connection = MagicMock(database="database_test", schema="test_schema")
    fqn = FQN.from_string("name").using_connection(connection)
    assert fqn.identifier == "database_test.test_schema.name"


def test_to_dict():
    fqn = FQN(name="name", database="db", schema="schema")
    assert fqn.to_dict() == {"name": "name", "database": "db", "schema": "schema"}
