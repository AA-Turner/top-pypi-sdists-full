import pytest
from sqlparse.sql import Parenthesis

from collate_sqllineage.core.models import (
    Column,
    Location,
    Path,
    Schema,
    SubQuery,
    Table,
)
from collate_sqllineage.exceptions import SQLLineageException


def test_repr_dummy():
    assert repr(Schema())
    assert repr(Table(""))
    assert repr(Table("a.b.c"))
    assert repr(SubQuery(Parenthesis(), Parenthesis().value, ""))
    assert repr(Column("a.b"))
    assert repr(Path(""))
    with pytest.raises(SQLLineageException):
        Table("a.b.c.d")
    with pytest.warns(Warning):
        Table("a.b", Schema("c"))


def test_hash_eq():
    assert Schema("a") == Schema("a")
    assert len({Schema("a"), Schema("a")}) == 1
    assert Table("a") == Table("a")
    assert len({Table("a"), Table("a")}) == 1


def test_of_dummy():
    with pytest.raises(NotImplementedError):
        Column.of("")
    with pytest.raises(NotImplementedError):
        Table.of("")
    with pytest.raises(NotImplementedError):
        SubQuery.of("", None)


class TestLocationInit:
    """
    Tests for Location.__init__ parsing.

    These tests assert on str(location) directly (not on Location == Location equality)
    so that they catch regressions in the schema/name splitting logic, not just
    confirm that two objects constructed identically are equal.
    """

    def test_unqualified_stage(self):
        assert str(Location("@STAGE_01")) == "<default>.stage_01"

    def test_schema_qualified_stage(self):
        assert str(Location("@SCHEMA_01.STAGE_01")) == "schema_01.stage_01"

    def test_db_schema_qualified_stage(self):
        # 3-part: db.schema.stage — all three parts must appear in the output
        assert str(Location("@DB_01.SCHEMA_01.STAGE_01")) == "db_01.schema_01.stage_01"

    def test_unqualified_stage_with_subpath(self):
        # subpath must be stripped; only the stage name is the entity identity
        assert str(Location("@STAGE_01/data/2024/")) == "<default>.stage_01"

    def test_schema_qualified_stage_with_subpath(self):
        assert (
            str(Location("@SCHEMA_01.STAGE_01/data/file.csv")) == "schema_01.stage_01"
        )

    def test_db_schema_qualified_stage_with_subpath(self):
        # 3-part stage + file subpath with dots — the primary regression case:
        # ".csv" must not be confused with a schema separator
        assert (
            str(Location("@DB_01.SCHEMA_01.STAGE_01/data/2024/export.csv"))
            == "db_01.schema_01.stage_01"
        )

    def test_subpath_with_multiple_dots_in_filename(self):
        # dots in filename (e.g. archive.2024.csv) must not inflate the schema dot count
        assert (
            str(Location("@DB_01.SCHEMA_01.STAGE_01/path/archive.2024.csv"))
            == "db_01.schema_01.stage_01"
        )

    def test_too_many_qualifiers_raises(self):
        # more than db.schema as the qualifier prefix is invalid
        with pytest.raises(SQLLineageException):
            Location("@A.B.C.D")

    def test_too_many_qualifiers_with_subpath_raises(self):
        # same validation must apply when a subpath is present
        with pytest.raises(SQLLineageException):
            Location("@A.B.C.D/path/file.csv")

    def test_unquoted_slash_treated_as_subpath_separator(self):
        # an unquoted "/" (which cannot legally appear in a Snowflake identifier)
        # is still treated as a subpath separator
        assert str(Location("@MY/STAGE")) == "<default>.my"

    def test_quoted_stage_name_with_slash(self):
        # quoted identifier: "/" is part of the stage name, not a subpath separator
        assert (
            str(Location('@LINEAGE_TEST_DB.STAGING."STG_001/WITH_SLASH"'))
            == "lineage_test_db.staging.stg_001/with_slash"
        )

    def test_quoted_stage_name_with_dot(self):
        # quoted identifier: "." is part of the stage name, not a schema separator
        assert (
            str(Location('@LINEAGE_TEST_DB.STAGING."STG_002.WITH_DOT"'))
            == "lineage_test_db.staging.stg_002.with_dot"
        )

    def test_quoted_stage_name_with_slash_and_subpath(self):
        # quoted stage name with "/" followed by an actual subpath after the closing quote
        assert (
            str(Location('@LINEAGE_TEST_DB.STAGING."STG_001/WITH_SLASH"/data/file.csv'))
            == "lineage_test_db.staging.stg_001/with_slash"
        )

    def test_quoted_stage_name_with_dot_and_subpath(self):
        assert (
            str(Location('@LINEAGE_TEST_DB.STAGING."STG_002.WITH_DOT"/data/file.csv'))
            == "lineage_test_db.staging.stg_002.with_dot"
        )
