import pytest

from pydantic_core._pydantic_core import ValidationError

from tests.utils import unquote


pytestmark = [pytest.mark.usefixtures("backup_database_schema")]


def test_iter(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter()]
    assert temp_schema.name.upper() in schema_names
    assert unquote(temp_schema_case_sensitive.name) in schema_names


def test_iter_like(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter(like="test_schema%")]
    assert temp_schema.name.upper() in schema_names
    assert unquote(temp_schema_case_sensitive.name) in schema_names


def test_iter_starts_with(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter(starts_with="Test_schema")]
    assert temp_schema.name.upper() not in schema_names
    assert unquote(temp_schema_case_sensitive.name) not in schema_names

    schema_names = [s.name for s in schemas.iter(starts_with="TEST_SCHEMA")]
    assert temp_schema.name.upper() in schema_names
    assert unquote(temp_schema_case_sensitive.name) not in schema_names


# The limit keyword is required for the from keyword to function, limit=10 was chosen arbitrarily
# as it does not affect the test
def test_iter_from_name(schemas, temp_schema, temp_schema_case_sensitive):
    schema_names = [s.name for s in schemas.iter(limit=10, from_name="test_schema")]
    assert temp_schema.name.upper() not in schema_names
    assert unquote(temp_schema_case_sensitive.name) in schema_names


def test_iter_limit(schemas):
    data = list(schemas.iter(limit=10))
    assert len(data) <= 10

    with pytest.raises(ValidationError):
        list(schemas.iter(limit=10001))
