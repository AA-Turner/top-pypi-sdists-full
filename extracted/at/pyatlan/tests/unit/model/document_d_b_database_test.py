import pytest

from pyatlan.model.assets import DocumentDBDatabase
from tests.unit.model.constants import (
    DOCUMENTDB_CONNECTION_QUALIFIED_NAME,
    DOCUMENTDB_CONNECTOR_TYPE,
    DOCUMENTDB_DATABASE_NAME,
    DOCUMENTDB_DATABASE_QUALIFIED_NAME,
)


@pytest.mark.parametrize(
    "name, connection_qualified_name, message",
    [
        (None, DOCUMENTDB_CONNECTION_QUALIFIED_NAME, "name is required"),
        (DOCUMENTDB_DATABASE_NAME, None, "connection_qualified_name is required"),
    ],
)
def test_creator_with_missing_parameters_raise_value_error(
    name: str, connection_qualified_name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DocumentDBDatabase.creator(
            name=name, connection_qualified_name=connection_qualified_name
        )


def test_creator():
    sut = DocumentDBDatabase.creator(
        name=DOCUMENTDB_DATABASE_NAME,
        connection_qualified_name=DOCUMENTDB_CONNECTION_QUALIFIED_NAME,
    )

    assert sut.name == DOCUMENTDB_DATABASE_NAME
    assert sut.connection_qualified_name == DOCUMENTDB_CONNECTION_QUALIFIED_NAME
    assert sut.qualified_name == DOCUMENTDB_DATABASE_QUALIFIED_NAME
    assert sut.connector_name == DOCUMENTDB_CONNECTOR_TYPE


@pytest.mark.parametrize(
    "qualified_name, name, message",
    [
        (None, DOCUMENTDB_DATABASE_NAME, "qualified_name is required"),
        (DOCUMENTDB_DATABASE_QUALIFIED_NAME, None, "name is required"),
    ],
)
def test_updater_with_invalid_parameter_raises_value_error(
    qualified_name: str, name: str, message: str
):
    with pytest.raises(ValueError, match=message):
        DocumentDBDatabase.updater(qualified_name=qualified_name, name=name)


def test_updater():
    sut = DocumentDBDatabase.updater(
        qualified_name=DOCUMENTDB_DATABASE_QUALIFIED_NAME, name=DOCUMENTDB_DATABASE_NAME
    )

    assert sut.qualified_name == DOCUMENTDB_DATABASE_QUALIFIED_NAME
    assert sut.name == DOCUMENTDB_DATABASE_NAME


def test_trim_to_required():
    sut = DocumentDBDatabase.updater(
        qualified_name=DOCUMENTDB_DATABASE_QUALIFIED_NAME, name=DOCUMENTDB_DATABASE_NAME
    ).trim_to_required()

    assert sut.qualified_name == DOCUMENTDB_DATABASE_QUALIFIED_NAME
    assert sut.name == DOCUMENTDB_DATABASE_NAME
