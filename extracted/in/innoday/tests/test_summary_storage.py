"""Storage guarantees for `summaries` / `summary_items` (PF-398).

The uniqueness assertions run against Postgres rather than the default in-memory
SQLite session: they are about partial unique indexes and about how NULL behaves
inside one, and the whole point of the two-index design is a Postgres rule
(NULLs never compare equal) that a different engine may or may not share. A test
that passes on SQLite would prove nothing about the database this deploys on.
"""

from __future__ import annotations

import uuid

import pytest
from sqlalchemy import text
from sqlalchemy.exc import IntegrityError

from src.domain.organization import Organization
from src.domain.project import Project
from src.domain.summary import Attribution, Summary, SummaryItem, SummaryType
from src.domain.user import User


def _suffix() -> str:
    return uuid.uuid4().hex[:12]


@pytest.fixture
def scope(pg_session):
    """An org, a project and a user to hang summaries off."""
    tag = _suffix()
    org = Organization(id=f"sum-org-{tag}", name=f"Org {tag}", alias=f"sum-{tag}")
    pg_session.add(org)
    project = Project(
        id=f"sum-proj-{tag}",
        name=f"Project {tag}",
        alias=f"sum-proj-{tag}",
        organization_id=org.id,
        description="storage fixture",
    )
    user = User(
        id=f"sum-user-{tag}", email=f"{tag}@example.com", full_name=f"User {tag}"
    )
    pg_session.add(project)
    pg_session.add(user)
    pg_session.flush()
    return org, project, user


def _summary(org, project, **overrides) -> Summary:
    fields = dict(
        organization_id=org.id,
        project_id=project.id,
        summary_type=SummaryType.SCRUM,
        window_spec="3d",
        body_markdown="what happened",
        motivational_quote="keep going",
    )
    fields.update(overrides)
    return Summary(**fields)


class TestLiveUniqueness:
    def test_two_live_team_summaries_are_refused(self, pg_session, scope):
        """The NULL-user case -- the one a plain UNIQUE would silently allow.

        Both rows have `user_id IS NULL`, and in Postgres two NULLs never compare
        equal, so `UNIQUE(project_id, user_id, summary_type, window_spec)` would
        accept the second without complaint. `uq_summaries_live_team` exists
        precisely so it cannot.
        """
        org, project, _ = scope
        pg_session.add(_summary(org, project))
        pg_session.flush()

        pg_session.add(_summary(org, project))
        with pytest.raises(IntegrityError):
            pg_session.flush()

    def test_two_live_summaries_for_one_user_are_refused(self, pg_session, scope):
        org, project, user = scope
        pg_session.add(
            _summary(org, project, summary_type=SummaryType.PERSONAL, user_id=user.id)
        )
        pg_session.flush()

        pg_session.add(
            _summary(org, project, summary_type=SummaryType.PERSONAL, user_id=user.id)
        )
        with pytest.raises(IntegrityError):
            pg_session.flush()

    def test_a_superseded_summary_frees_the_slot(self, pg_session, scope):
        """Re-running supersedes rather than overwrites, so history survives.

        Note the order: the old row is pointed at the replacement *before* the
        replacement is inserted. That is the only order the immediate unique
        index permits, and it is what the deferred self-FK exists to allow --
        the UPDATE names an id that does not exist until the next statement.
        """
        org, project, _ = scope
        first = _summary(org, project)
        pg_session.add(first)
        pg_session.flush()

        second = _summary(org, project)
        first.superseded_by_id = second.id
        pg_session.flush()
        pg_session.add(second)
        pg_session.flush()

        assert pg_session.get(Summary, first.id).superseded_by_id == second.id
        assert pg_session.get(Summary, second.id).superseded_by_id is None

    def test_a_different_window_is_a_different_slot(self, pg_session, scope):
        """`window_spec` is the cache key, so '3d' and '1w' do not collide."""
        org, project, _ = scope
        pg_session.add(_summary(org, project, window_spec="3d"))
        pg_session.add(_summary(org, project, window_spec="1w"))
        pg_session.flush()  # no IntegrityError

    def test_the_team_summary_and_a_user_summary_coexist(self, pg_session, scope):
        org, project, user = scope
        pg_session.add(_summary(org, project))
        pg_session.add(_summary(org, project, user_id=user.id))
        pg_session.flush()  # no IntegrityError

    def test_windowless_rows_are_exempt(self, pg_session, scope):
        """The board-scoped append path writes `window_spec=''` and must keep working.

        Those rows are a history log with nothing to key uniqueness on -- see the
        note in src/domain/summary.py. Both indexes exclude them explicitly, so
        the exemption is a condition in the index rather than a NULL quietly
        slipping past one.
        """
        org, project, _ = scope
        for _ in range(3):
            pg_session.add(
                _summary(org, project, summary_type=SummaryType.STATUS, window_spec="")
            )
        pg_session.flush()  # no IntegrityError

    def test_omitting_window_spec_is_refused(self, pg_session, scope):
        """The exemption must be asked for, never handed out by forgetting.

        `''` exempts a row from *both* live-uniqueness indexes. While the field
        carried `default=""`, a caller who simply omitted the kwarg got that
        exemption silently -- the row inserted fine and no rule applied to it,
        which is indistinguishable from the rule being broken. With no default
        the omission is a NOT NULL violation, so the only way to the sentinel is
        to write it.
        """
        org, project, _ = scope
        fields = dict(
            organization_id=org.id,
            project_id=project.id,
            summary_type=SummaryType.SCRUM,
            body_markdown="what happened",
            motivational_quote="keep going",
        )
        assert "window_spec" not in fields
        pg_session.add(Summary(**fields))
        with pytest.raises(IntegrityError) as exc:
            pg_session.flush()
        assert "window_spec" in str(exc.value)

    def test_a_summary_cannot_supersede_itself(self, pg_session, scope):
        """Self-supersession empties a slot rather than replacing its occupant.

        The deferred self-FK is satisfied by a self-reference, so nothing but
        `ck_summaries_no_self_supersede` refuses it. The row would still exist
        and still be the only summary for its scope+window, yet no query for the
        live one -- `superseded_by_id IS NULL` -- would ever return it.
        """
        org, project, _ = scope
        summary = _summary(org, project)
        pg_session.add(summary)
        pg_session.flush()

        summary.superseded_by_id = summary.id
        with pytest.raises(IntegrityError) as exc:
            pg_session.flush()
        assert "ck_summaries_no_self_supersede" in str(exc.value)


class TestSummaryItems:
    def test_an_item_needs_neither_a_ticket_nor_a_mapped_user(self, pg_session, scope):
        """Unassigned tickets and unmapped assignees are first-class, not errors."""
        org, project, _ = scope
        summary = _summary(org, project)
        pg_session.add(summary)
        pg_session.flush()

        item = SummaryItem(
            summary_id=summary.id,
            assignee_display="A. Lice",
            attribution=Attribution.CODE,
            repo="innoday",
            branch="PF-398-summary-storage",
            pr_url="https://github.com/havilandsoftware/innoday/pull/1",
            pr_state="open",
            body_markdown="opened the PR",
            rank=1,
        )
        pg_session.add(item)
        pg_session.flush()

        stored = pg_session.get(SummaryItem, item.id)
        assert stored.ticket_id is None
        assert stored.assignee_user_id is None
        assert stored.assignee_display == "A. Lice"
        assert stored.attribution is Attribution.CODE
        assert stored.no_work_detected is False

    def test_no_work_detected_is_recordable(self, pg_session, scope):
        """ "Nothing happened" is an answer, and it needs a row to live in."""
        org, project, user = scope
        summary = _summary(org, project, user_id=user.id)
        pg_session.add(summary)
        pg_session.flush()

        item = SummaryItem(
            summary_id=summary.id,
            assignee_user_id=user.id,
            attribution=Attribution.NONE,
            no_work_detected=True,
        )
        pg_session.add(item)
        pg_session.flush()
        pg_session.expire(item)

        stored = pg_session.get(SummaryItem, item.id)
        assert stored.no_work_detected is True
        assert stored.assignee_user_id == user.id
        assert stored.ticket_id is None


# The complete NOT NULL set of each table, as the migrations build it. Stated
# exhaustively rather than as a sample, so the assertion below fails on a column
# that quietly *gains* or *loses* NOT NULL as well as on one that was forgotten.
NOT_NULL_COLUMNS = {
    "summaries": {
        "id",
        "organization_id",
        "project_id",
        "window_spec",
        "summary_type",
        "motivational_quote",
        "generated_by",
        "token_usage",
        "generation_time_ms",
        "created_at",
    },
    "summary_items": {
        "id",
        "summary_id",
        "attribution",
        "rank",
        "no_work_detected",
    },
}

MODELS = {"summaries": Summary, "summary_items": SummaryItem}


class TestModelMatchesTheDatabase:
    def test_required_columns_are_not_nullable_in_the_database(self, pg_engine):
        """Read the real Postgres schema, not the model's opinion of it.

        This used to assert only against `model.__table__.columns[...].nullable`
        -- which is the model checking itself, and therefore cannot detect the
        exact failure CLAUDE.md's "`sa_column=` silently drops NOT NULL" section
        is about: model and migration disagreeing, so the fixtures build a schema
        more permissive than production and accept rows the deploy rejects.
        `information_schema` is the only side of that comparison with authority.
        """
        with pg_engine.connect() as conn:
            for table, expected in NOT_NULL_COLUMNS.items():
                rows = conn.execute(
                    text(
                        "SELECT column_name FROM information_schema.columns "
                        "WHERE table_schema = 'public' AND table_name = :t "
                        "AND is_nullable = 'NO'"
                    ),
                    {"t": table},
                ).all()
                assert rows, f"{table} not found in information_schema"
                assert {r[0] for r in rows} == expected, (
                    f"{table}'s NOT NULL columns in Postgres differ from what "
                    f"this test pins"
                )

    def test_the_model_agrees_with_the_database(self):
        """The other half of the comparison: metadata must match the same set.

        The fixtures call `SQLModel.metadata.create_all`, so this is the schema
        every non-Postgres test in the suite actually runs against. Pinned to the
        same constant as the query above, so the two cannot drift apart silently.
        """
        for table, expected in NOT_NULL_COLUMNS.items():
            columns = MODELS[table].__table__.columns
            actual = {c.name for c in columns if c.nullable is False}
            assert actual == expected, f"{table}'s model nullability has drifted"

    def test_ticket_id_is_indexed(self):
        """Per-ticket history is a primary read path, not an occasional one."""
        indexed = {
            tuple(c.name for c in index.columns)
            for index in SummaryItem.__table__.indexes
        }
        assert ("ticket_id",) in indexed


class TestContributorsQueryRunsOnPostgres:
    """`contributors_by_project` selected the whole `User` entity under DISTINCT.

    Postgres has no equality operator for `json` -- only for `jsonb` -- and `users`
    carries two `json` columns (`notification_preferences`, `ui_preferences`). So
    DISTINCT over the entity died with:

        could not identify an equality operator for type json

    SQLite has no such restriction, so the whole suite passed while the dashboard
    500'd for the first organization whose tickets had assignees. This test has to
    live on the Postgres engine or it cannot fail.
    """

    def test_contributors_by_project_does_not_die_on_distinct(self, pg_engine):
        from uuid import uuid4

        from sqlmodel import Session as SQLSession

        from src.domain.organization import Organization
        from src.domain.project import Project
        from src.domain.ticket import Ticket, TicketStatus
        from src.domain.user import User
        from src.routers.webui.data import contributors_by_project

        with SQLSession(pg_engine) as session:
            # A unique alias: `organizations.alias` is uniquely indexed and this
            # Postgres database persists across runs, so a fixed one passes once
            # and then fails on every subsequent run for the wrong reason.
            org = Organization(
                id=str(uuid4()),
                name="Distinct Co",
                alias=f"dc{str(uuid4())[:8]}",
            )
            user = User(
                id=str(uuid4()),
                email=f"{uuid4()}@example.com",
                full_name="Ada Lovelace",
                # The columns that broke it. Non-empty, so they are really compared.
                notification_preferences={"email": True},
                ui_preferences={"theme": "dark"},
            )
            session.add(org)
            session.add(user)
            session.commit()

            project = Project(
                id=str(uuid4()),
                organization_id=org.id,
                alias=f"D{str(uuid4())[:6]}".upper(),
                name="Distinct Project",
                description="d",
            )
            session.add(project)
            session.commit()

            # Two assigned tickets, so DISTINCT genuinely has rows to deduplicate.
            for n in range(2):
                session.add(
                    Ticket(
                        summary=f"assigned {n}",
                        organization_id=org.id,
                        project_id=project.id,
                        status=TicketStatus.TODO,
                        assigned_to=user.id,
                    )
                )
            session.commit()

            people = contributors_by_project(session, [project.id])

        assert [c.name for c in people[project.id]] == ["Ada Lovelace"], (
            "one contributor, deduplicated across two tickets"
        )
