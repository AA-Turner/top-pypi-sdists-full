"""DESIGN survives the trip through the real Postgres enum type.

`project_repositories.layer` is a native Postgres enum (`repositorylayer`) built
from the member *names*, while `repositories.layer` is a plain varchar of the
lowercase *values*, and the API speaks values. A new member therefore has to
exist in three places at once, and SQLite can prove none of it: there the column
compiles to a bare VARCHAR with no CHECK constraint, so every one of these
assertions passes on an unmigrated database.

That is the whole reason this file is Postgres-only. A test for this that ran on
SQLite would be a test that cannot fail.
"""

import pytest
from sqlalchemy import text

from src.domain.project import RepositoryLayer


class TestDesignIsARealEnumMember:
    def test_the_type_accepts_the_new_label(self, pg_session):
        """The migration ran, and it ran as ALTER TYPE rather than silently."""
        assert (
            pg_session.execute(text("SELECT 'DESIGN'::repositorylayer")).scalar()
            == "DESIGN"
        )

    def test_every_python_member_exists_in_the_database_type(self, pg_session):
        """Catches the half-applied change: a member added to one side only.

        Asserting the whole set rather than just DESIGN, because the failure this
        guards against is generic -- somebody adds a member and forgets the
        migration -- and only shows up as a write that 500s in production.
        """
        in_db = {
            row[0]
            for row in pg_session.execute(
                text(
                    "SELECT enumlabel FROM pg_enum e "
                    "JOIN pg_type t ON t.oid = e.enumtypid "
                    "WHERE t.typname = 'repositorylayer'"
                )
            )
        }
        missing = {m.name for m in RepositoryLayer} - in_db
        assert not missing, f"members with no database label: {sorted(missing)}"

    def test_the_name_is_stored_and_the_value_is_spoken(self, pg_session):
        """The divergence that makes this enum awkward, pinned in one assertion.

        Postgres stores `DESIGN`; the CLI, the API body and `repositories.layer`
        all say `design`. Code that assumes either one is *the* spelling breaks
        on the other side of the seam.
        """
        assert RepositoryLayer.DESIGN.name == "DESIGN"
        assert RepositoryLayer.DESIGN.value == "design"
        stored = pg_session.execute(
            # CAST(...) rather than `:label::repositorylayer`: SQLAlchemy's text()
            # reads the `::` immediately after a bind parameter as part of the
            # parameter name and the statement never compiles.
            text("SELECT CAST(:label AS repositorylayer)"),
            {"label": RepositoryLayer.DESIGN.name},
        ).scalar()
        assert stored == "DESIGN"

    def test_the_lowercase_value_is_not_a_valid_label(self, pg_session):
        """Proves the previous test is asserting something real.

        If Postgres accepted both spellings the name/value distinction would be
        cosmetic and the seam would not need guarding. It does not.
        """
        with pytest.raises(Exception):
            pg_session.execute(text("SELECT 'design'::repositorylayer")).scalar()
