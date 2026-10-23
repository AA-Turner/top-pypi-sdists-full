from collections.abc import Set
from dataclasses import FrozenInstanceError
from unittest.mock import MagicMock

import pytest

from pydantic import TypeAdapter, ValidationError

from snowflake.core._identifiers import (
    FQN,
    CanonicalName,
    Identifier,
    IdentifierString,
    QualifiedIdentifier,
    is_identifier_like,
    quote_name,
)
from snowflake.core.exceptions import InvalidIdentifierError


def test_fqn_emits_deprecation_warning() -> None:
    with pytest.warns(DeprecationWarning, match="QualifiedIdentifier"):
        FQN(name="name", database="db", schema="schema")


def test_attributes():
    with pytest.warns(DeprecationWarning):
        fqn = FQN(name="object_name", database="database_name", schema="schema_name")
    assert fqn.database == "database_name"
    assert fqn.schema == "schema_name"
    assert fqn.name == "object_name"


@pytest.mark.parametrize(
    ("name", "database", "schema", "identifier"),
    [
        ("name", "db", "schema", "db.schema.name"),
        ('"my_object"', "db", "schema", 'db.schema."my_object"'),
        ("name", None, "schema", "schema.name"),
        ("name", None, None, "name"),
        ("name", "db", None, "db.PUBLIC.name"),
        ("name(float, string)", "db", None, "db.PUBLIC.name(float, string)"),
    ],
)
def test_identifier(name, database, schema, identifier):
    with pytest.warns(DeprecationWarning):
        fqn = FQN(name=name, database=database, schema=schema)
    assert fqn.identifier == identifier


def test_eq():
    with pytest.warns(DeprecationWarning):
        fqn1 = FQN(name="name", database="db", schema="schema")
        fqn2 = FQN(name="name", database="db", schema="schema")
    assert fqn1 == fqn2
    assert fqn2 == fqn1


def test_neq():
    with pytest.warns(DeprecationWarning):
        fqn1 = FQN(name="name", database="db", schema="schema")
        fqn2 = FQN(name="other-name", database="db", schema="schema")
    assert fqn1 != fqn2
    assert fqn2 != fqn1


def test_eq_with_different_type():
    with pytest.warns(DeprecationWarning):
        fqn = FQN(name="name", database="db", schema="schema")
    assert fqn != "db.schema.name"


def test_set_database():
    with pytest.warns(DeprecationWarning):
        fqn = FQN(name="name", database="db", schema="schema")
    fqn.set_database("foo")
    assert fqn.database == "foo"


def test_set_schema():
    with pytest.warns(DeprecationWarning):
        fqn = FQN(name="name", database="db", schema="schema")
    fqn.set_schema("foo")
    assert fqn.schema == "foo"


def test_set_name():
    with pytest.warns(DeprecationWarning):
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
    with pytest.warns(DeprecationWarning):
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
    with pytest.warns(DeprecationWarning):
        fqn = FQN.from_string("name").using_connection(connection)
    assert fqn.identifier == "database_test.test_schema.name"


def test_to_dict():
    with pytest.warns(DeprecationWarning):
        fqn = FQN(name="name", database="db", schema="schema")
    assert fqn.to_dict() == {"name": "name", "database": "db", "schema": "schema"}


@pytest.mark.parametrize(
    ("name", "keep_case", "expected"),
    [
        # Already quoted names - should return as-is
        ('"already_quoted"', False, '"already_quoted"'),
        ('"already_quoted"', True, '"already_quoted"'),
        ('"MyName"', False, '"MyName"'),
        ('"MyName"', True, '"MyName"'),
        # Unquoted case-insensitive identifiers (simple identifiers)
        # With keep_case=False, should uppercase and quote
        ("simple_id", False, '"SIMPLE_ID"'),
        ("simple_id123", False, '"SIMPLE_ID123"'),
        ("_privatevar", False, '"_PRIVATEVAR"'),
        ("var_with_$dollar", False, '"VAR_WITH_$DOLLAR"'),
        # Unquoted case-insensitive identifiers
        # With keep_case=True, should quote without uppercasing
        ("simple_id", True, '"simple_id"'),
        ("simple_id123", True, '"simple_id123"'),
        ("_privatevar", True, '"_privatevar"'),
        # Names with special characters that require quoting and escaping
        ("name-with-hyphens", False, '"name-with-hyphens"'),
        ("name.with.dots", False, '"name.with.dots"'),
        ("name with spaces", False, '"name with spaces"'),
        # Names with double quotes inside - need escaping
        ('name"with"quotes', False, '"name""with""quotes"'),
        ('name"with"quotes', True, '"name""with""quotes"'),
        ('"ANOTHER   ""NAME""WITH   ""QUOTES"""', False, '"ANOTHER   ""NAME""WITH   ""QUOTES"""'),
        # Mixed case simple identifiers - with keep_case
        ("MySimpleName", False, '"MYSIMPLENAME"'),
        ("MySimpleName", True, '"MySimpleName"'),
        # Single character names
        ("a", False, '"A"'),
        ("A", False, '"A"'),
        ("_", False, '"_"'),
    ],
)
def test_quote_name_parametrized(name: str, keep_case: bool, expected: str) -> None:
    """Exercise :func:`~snowflake.core._identifiers.quote_name` across identifier forms."""
    result = quote_name(name, keep_case=keep_case)
    assert result == expected


@pytest.mark.parametrize(
    ("identifier", "expected"),
    [
        ("FOO", "FOO"),
        ("foo", "FOO"),
        ('"FOO"', "FOO"),
        ('"foo"', "foo"),
        ('"foo 1"', "foo 1"),
        ('"""foo"""', '"foo"'),
        ('"""FOO"""', '"FOO"'),
        ("Foo", "FOO"),
        ("FOO1", "FOO1"),
        ("Foo1", "FOO1"),
        ('"a""b"', 'a"b'),
    ],
)
def test_canonical_name_resolve_from_identifier_valid(identifier: str, expected: str) -> None:
    assert CanonicalName.resolve_from_identifier(identifier) == CanonicalName(expected)
    assert CanonicalName.resolve_from_identifier(Identifier(identifier)) == CanonicalName(expected)


@pytest.mark.parametrize(
    "identifier",
    [
        "1FOO",
        "FOO 1",
        'foo"bar',
        '"a"b"',
        '"foo"bar"',
        '"a" "b"',
    ],
)
def test_canonical_name_resolve_from_identifier_invalid(identifier: str) -> None:
    with pytest.raises(ValueError, match="is not a valid SQL identifier"):
        CanonicalName.resolve_from_identifier(identifier)


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        ("foo", "FOO", True),
        ("foo", '"FOO"', True),
        ('"foo"', "foo", False),
        ('"a""b"', '"a""b"', True),
        ('"""a "" b"""', '"""a "" b"""', True),
    ],
)
def test_identifier_eq(left: str, right: str, expected: bool) -> None:
    assert (Identifier(left) == Identifier(right)) is expected


@pytest.mark.parametrize("inputted_value", ("foo", "FOO", "fOo", '"a FOO "" name"'))
def test_identifier_preserves_original_spelling(inputted_value: str) -> None:
    identifier = Identifier(inputted_value)

    assert str(identifier) == inputted_value
    assert identifier.to_identifier_string() == IdentifierString(inputted_value)
    assert identifier.to_identifier_string() == inputted_value


def test_is_identifier_like() -> None:
    assert is_identifier_like("foo")
    assert is_identifier_like(Identifier("foo"))
    assert is_identifier_like(IdentifierString("foo"))
    assert not is_identifier_like(CanonicalName("foo"))
    assert not is_identifier_like(42)


def test_identifier_string_is_a_plain_str_at_runtime() -> None:
    spelling = IdentifierString("foo")
    # For usage as a bind parameter value in the Snowflake connector,
    # it's crucial that the type be a plain string at runtime.
    # cursor.execute("SELECT ?", (CustomType(),)) fails for a custom class CustomType
    # because the connector doesn't support serializing custom types.
    assert type(spelling) is str
    assert IdentifierString(spelling) is spelling


@pytest.mark.parametrize("inputted_value", ("foo", "FOO", "fOo", '"a FOO "" name"'))
def test_identifier_to_identifier_string_from_str_or_identifier(inputted_value: str) -> None:
    assert Identifier(inputted_value).to_identifier_string() == inputted_value
    assert Identifier(Identifier(inputted_value)).to_identifier_string() == inputted_value
    assert type(Identifier(inputted_value).to_identifier_string()) is str


def test_identifier_to_identifier_string_from_canonical_name() -> None:
    assert Identifier.from_canonical_name(CanonicalName("lowercase")).to_identifier_string() == '"lowercase"'


def test_identifier_to_identifier_string_rejects_invalid_type() -> None:
    with pytest.raises(TypeError):
        Identifier(42).to_identifier_string()  # type: ignore[arg-type]
    with pytest.raises(TypeError):
        Identifier(CanonicalName("foo"))  # type: ignore[arg-type]


def test_identifier_does_not_compare_equal_to_string() -> None:
    identifier = Identifier("foo")
    assert (identifier == "foo") is False
    assert identifier != "foo"
    assert (identifier == None) is False  # noqa: E711
    assert identifier in ["a", identifier]
    assert identifier not in ["foo"]


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        "1FOO",
        "FOO 1",
        'foo"bar',
        '"a"b"',
        '"a" "b"',
    ],
)
def test_identifier_rejects_invalid_sql_identifier(invalid_identifier: str) -> None:
    with pytest.raises(ValueError, match="is not a valid SQL identifier"):
        Identifier(invalid_identifier)


def test_identifier_from_canonical_name_quotes_when_needed() -> None:
    identifier = Identifier.from_canonical_name(CanonicalName("1foo"))
    assert str(identifier) == '"1foo"'
    assert CanonicalName.resolve_from_identifier(identifier) == CanonicalName("1foo")


@pytest.mark.parametrize(
    "equivalent_identifiers",
    (
        ("foo", '"FOO"'),
        ("BaR", '"BAR"'),
        ('"""a "" b"""', '"""a "" b"""'),
    ),
)
def test_identifier_hash_membership(equivalent_identifiers: tuple[str, str]) -> None:
    left, right = equivalent_identifiers
    assert Identifier(left) in {Identifier(right)}


def test_identifier_is_frozen() -> None:
    identifier = Identifier("foo")
    with pytest.raises(FrozenInstanceError):
        identifier._original_spelling = "bar"  # type: ignore[misc]


def test_identifier_reuses_existing_instance() -> None:
    identifier = Identifier("A")
    assert Identifier(identifier) is identifier


@pytest.mark.parametrize(
    ("inputted_value", "expected_quoted"),
    [
        ("foo", '"FOO"'),
        ("FOO", '"FOO"'),
        ("fOo", '"FOO"'),
        ('"FOO"', '"FOO"'),
        ('"foo"', '"foo"'),
        ('"a FOO "" name"', '"a FOO "" name"'),
        ('"""a "" b"""', '"""a "" b"""'),
    ],
)
def test_identifier_with_quoted_spelling(inputted_value: str, expected_quoted: str) -> None:
    identifier = Identifier(inputted_value)
    quoted = identifier.with_quoted_spelling()
    assert isinstance(quoted, Identifier)
    assert str(quoted) == expected_quoted
    assert str(quoted).startswith('"') and str(quoted).endswith('"')
    assert quoted == identifier
    assert quote_name(inputted_value) == expected_quoted


@pytest.mark.parametrize(
    "equivalent_spellings",
    [
        ("foo", "FOO", "fOo", '"FOO"'),
        ('"foo"',),
        ('"a FOO "" name"',),
        ('"""a "" b"""',),
    ],
)
def test_identifier_with_normalized_spelling(equivalent_spellings: tuple[str, ...]) -> None:
    identifiers = [Identifier(spelling) for spelling in equivalent_spellings]
    normalized = [identifier.with_normalized_spelling() for identifier in identifiers]
    quoted = [identifier.with_quoted_spelling() for identifier in identifiers]
    for original, with_normalized, with_quoted in zip(identifiers, normalized, quoted, strict=True):
        assert isinstance(with_normalized, Identifier)
        assert with_normalized == original
        assert with_normalized == with_quoted
        assert str(with_normalized) == str(with_quoted)
    assert len({str(value) for value in normalized}) == 1


@pytest.mark.parametrize(
    ("left", "right", "expected"),
    [
        (CanonicalName("FOO"), CanonicalName("FOO"), True),
        (CanonicalName("FOO"), CanonicalName("BAR"), False),
    ],
)
def test_canonical_name_eq(left: CanonicalName, right: CanonicalName, expected: bool) -> None:
    assert (left == right) is expected


@pytest.mark.parametrize(
    "other",
    [
        "FOO",
        42,
    ],
)
def test_canonical_name_does_not_compare_equal_to_other_types(other: object) -> None:
    canonical = CanonicalName("FOO")
    assert (canonical == other) is False
    assert canonical != other
    assert canonical in [other, canonical]


@pytest.mark.parametrize(
    ("name1", "name2", "should_equal"),
    [
        ("FOO", "FOO", True),
        ("FOO", "BAR", False),
    ],
)
def test_canonical_name_hash(name1: str, name2: str, should_equal: bool) -> None:
    hash1 = hash(CanonicalName(name1))
    hash2 = hash(CanonicalName(name2))
    if should_equal:
        assert hash1 == hash2
    else:
        assert hash1 != hash2


def test_canonical_name_hash_membership() -> None:
    assert CanonicalName("FOO") in {CanonicalName("FOO")}


def test_canonical_name_add() -> None:
    assert CanonicalName("FOO") + CanonicalName("BAR") == CanonicalName("FOOBAR")
    assert CanonicalName("foo") + CanonicalName("Bar") == CanonicalName("fooBar")


def test_canonical_name_pydantic_core_schema() -> None:
    adapter = TypeAdapter(CanonicalName)
    assert adapter.validate_python("foo") == CanonicalName("foo")
    existing = CanonicalName("bar")
    assert adapter.validate_python(existing) is existing
    with pytest.raises(ValidationError):
        adapter.validate_python(123)


@pytest.mark.parametrize(
    "other",
    [
        "BAR",
        Identifier("BAR"),
        42,
    ],
)
def test_canonical_name_add_not_implemented_for_other_types(other: object) -> None:
    with pytest.raises(TypeError):
        CanonicalName("FOO") + other


@pytest.mark.parametrize(
    ("canonical", "allowed_idents"),
    [
        ("FOO", {'"FOO"', "FOO", "foo"}),
        ("my col", {'"my col"'}),
        ('foo"bar', {'"foo""bar"'}),
        ("lowercase", {'"lowercase"'}),
    ],
)
def test_canonical_name_to_identifier(
    canonical: str,
    allowed_idents: Set[str],
) -> None:
    c = CanonicalName(canonical)
    ident = c.to_identifier_string()
    assert isinstance(ident, str)
    assert ident in allowed_idents
    assert CanonicalName.resolve_from_identifier(ident) == c


def test_qualified_identifier_attributes() -> None:
    qi = QualifiedIdentifier(name="object_name", database="database_name", schema="schema_name")
    assert qi.name == Identifier("object_name")
    assert qi.schema == Identifier("schema_name")
    assert qi.database == Identifier("database_name")


def test_qualified_identifier_construction_from_identifier() -> None:
    qi = QualifiedIdentifier(
        name=Identifier("name"),
        schema=Identifier("schema"),
        database=Identifier("db"),
    )
    assert qi.name == Identifier("name")
    assert qi.schema == Identifier("schema")
    assert qi.database == Identifier("db")


@pytest.mark.parametrize(
    ("name", "schema", "database", "expected"),
    [
        ("name", "schema", "db", "db.schema.name"),
        ('"my_object"', "schema", "db", 'db.schema."my_object"'),
        ("name", "schema", None, "schema.name"),
        ("name", None, None, "name"),
        ("name", None, "db", "db..name"),
    ],
)
def test_qualified_identifier_str(
    name: str,
    schema: str | None,
    database: str | None,
    expected: str,
) -> None:
    qi = QualifiedIdentifier(name=name, schema=schema, database=database)
    assert str(qi) == expected


@pytest.mark.parametrize(
    "invalid_identifier",
    [
        "1FOO",
        "FOO 1",
        'foo"bar',
        "name(float, string)",
    ],
)
def test_qualified_identifier_rejects_invalid_components(invalid_identifier: str) -> None:
    with pytest.raises(ValueError, match="is not a valid SQL identifier"):
        QualifiedIdentifier(name=invalid_identifier)
    with pytest.raises(ValueError, match="is not a valid SQL identifier"):
        QualifiedIdentifier(name="name", schema=invalid_identifier)
    with pytest.raises(ValueError, match="is not a valid SQL identifier"):
        QualifiedIdentifier(name="name", database=invalid_identifier)


def test_qualified_identifier_rejects_invalid_type() -> None:
    with pytest.raises(TypeError):
        QualifiedIdentifier(name=42)  # type: ignore[arg-type]


def test_qualified_identifier_is_frozen() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    with pytest.raises(FrozenInstanceError):
        qi._name = Identifier("other")  # type: ignore[misc]


def test_qualified_identifier_with_name() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    updated = qi.with_name("other")
    assert updated.name == Identifier("other")
    assert updated.schema == qi.schema
    assert updated.database == qi.database
    assert qi.name == Identifier("name")


def test_qualified_identifier_with_schema() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    updated = qi.with_schema("other")
    assert updated.schema == Identifier("other")
    assert updated.with_schema(None).schema is None
    assert qi.schema == Identifier("schema")


def test_qualified_identifier_with_database() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    updated = qi.with_database("other")
    assert updated.database == Identifier("other")
    assert updated.with_database(None).database is None
    assert qi.database == Identifier("db")


def test_qualified_identifier_with_quoted_spelling() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    quoted = qi.with_quoted_spelling()
    assert str(quoted.name) == '"NAME"'
    assert quoted.schema is not None and str(quoted.schema) == '"SCHEMA"'
    assert quoted.database is not None and str(quoted.database) == '"DB"'
    assert quoted == qi


def test_qualified_identifier_with_normalized_spelling() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    normalized = qi.with_normalized_spelling()
    assert normalized == qi.with_quoted_spelling()
    assert normalized == qi


def test_qualified_identifier_using_connection() -> None:
    connection = MagicMock(database="database_test", schema="test_schema")
    qi = QualifiedIdentifier.from_string("name").using_connection(connection)
    assert str(qi) == "database_test.test_schema.name"
    already_qualified = QualifiedIdentifier.from_string("db.schema.name").using_connection(connection)
    assert str(already_qualified) == "db.schema.name"


def test_qualified_identifier_eq_by_snowflake_identity() -> None:
    left = QualifiedIdentifier(name="foo", schema="bar", database="baz")
    right = QualifiedIdentifier(name='"FOO"', schema='"BAR"', database='"BAZ"')
    assert left == right
    assert hash(left) == hash(right)


def test_qualified_identifier_neq() -> None:
    left = QualifiedIdentifier(name="name", schema="schema", database="db")
    right = QualifiedIdentifier(name="other", schema="schema", database="db")
    assert left != right


def test_qualified_identifier_does_not_compare_equal_to_string() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    assert (qi == "db.schema.name") is False
    assert qi != "db.schema.name"


def test_qualified_identifier_hash_membership() -> None:
    left = QualifiedIdentifier(name="foo", schema="bar", database="baz")
    right = QualifiedIdentifier(name='"FOO"', schema='"BAR"', database='"BAZ"')
    assert left in {right}
    assert left in {right: "value"}


def test_qualified_identifier_to_dict() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    assert qi.to_dict() == {"name": "name", "schema": "schema", "database": "db"}
    assert QualifiedIdentifier(name="name").to_dict() == {
        "name": "name",
        "schema": None,
        "database": None,
    }


def test_qualified_identifier_repr() -> None:
    qi = QualifiedIdentifier(name="name", schema="schema", database="db")
    assert repr(qi) == (
        "QualifiedIdentifier(name=Identifier('name'), schema=Identifier('schema'), database=Identifier('db'))"
    )


@pytest.mark.parametrize(
    ("identifier_str", "expected"),
    [
        ("db.schema.name", "db.schema.name"),
        ("DB.SCHEMA.NAME", "DB.SCHEMA.NAME"),
        ("schema.name", "schema.name"),
        ("name", "name"),
        ("db..name", "db..name"),
        ('"name with space"', '"name with space"'),
        ('"dot.db"."dot.schema"."dot.name"', '"dot.db"."dot.schema"."dot.name"'),
        ('"dot.db".schema."dot.name"', '"dot.db".schema."dot.name"'),
        ('db.schema."dot.name"', 'db.schema."dot.name"'),
        ('"dot.db".schema."DOT.name"', '"dot.db".schema."DOT.name"'),
        ('"abc""this is in nested quotes"""', '"abc""this is in nested quotes"""'),
    ],
)
def test_qualified_identifier_from_string(identifier_str: str, expected: str) -> None:
    qi = QualifiedIdentifier.from_string(identifier_str)
    assert str(qi) == expected


def test_qualified_identifier_from_string_double_dot() -> None:
    qi = QualifiedIdentifier.from_string("db..name")
    assert qi.database == Identifier("db")
    assert qi.schema is None
    assert qi.name == Identifier("name")


@pytest.mark.parametrize(
    "identifier_str",
    [
        "db.schema.name.foo",
        "schema. name",
        "name with space",
        'dot.db."dot.schema"."dot.name"',
        '"dot.db.schema."dot.name"',
        "db.schema.function(string, int, variant)",
        'db.schema."fun tion"(string, int, variant)',
    ],
)
def test_qualified_identifier_from_string_fails(identifier_str: str) -> None:
    with pytest.raises(InvalidIdentifierError) as err:
        QualifiedIdentifier.from_string(identifier_str)
    assert str(err.value) == f"'{identifier_str}' is not a valid identifier."
