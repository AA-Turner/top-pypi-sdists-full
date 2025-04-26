import pytest

from snowflake.core.exceptions import NotFoundError
from snowflake.core.schema import Schema
from tests.utils import random_string


pytestmark = pytest.mark.usefixtures("backup_database_schema")


def test_drop(schemas):
    comment = "my comment"
    new_schema = Schema(
        name=random_string(5, "test_schema_"),
        comment=comment,
    )
    s = schemas.create(new_schema)
    try:
        assert s.fetch().comment == comment
    finally:
        s.drop()
    s.undrop()

    try:
        assert s.fetch().comment == comment
    finally:
        s.drop()

    with pytest.raises(
        NotFoundError,
    ):
        s.fetch()

    # Should not error
    s.drop(if_exists=True)

    s = schemas.create(new_schema)
    try:
        assert s.fetch().comment == comment
    finally:
        s.drop()
