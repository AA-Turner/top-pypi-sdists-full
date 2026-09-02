"""RLS tenant isolation, exercised under a role that cannot bypass it.

These assertions are meaningless on SQLite (no RLS, no roles, no `SET LOCAL`) and
meaningless as `postgres` (`rolbypassrls = true`), which is why they live here and
depend on the Postgres fixtures rather than the default test session.

Every deny-check is paired with a positive control. An earlier draft of the
cross-tenant write check "passed" because it used `INSERT .. SELECT` from a row
the caller could not see: zero rows inserted, no error raised, indistinguishable
from a policy refusal. A refusal is only evidence if the same statement succeeds
for a caller who should be allowed.
"""

from __future__ import annotations

import os
import re
import subprocess

import pytest
from sqlalchemy import text
from sqlmodel import Session

from src.domain import Organization, OrganizationMembership, Project, User
from src.domain.organization import OrganizationRole
from src.domain.summary import Attribution, Summary, SummaryItem, SummaryType
from src.domain.user_identity import IdentityPlatform, MatchSource, UserIdentity

# The whole security layer is one migration now (PF-399): role, schema, the
# SECURITY DEFINER helpers, RLS enablement, every policy, views and grants. It
# was previously three ranges spread across months, which is why this file used
# to stitch them together and regex out a superseded statement.
RLS_REVISION_RANGE = "aaaa0000base:aaaa0002rlsgaps"

# Ranges *after* that migration which define a policy as it now stands. Every one of
# them has to be listed, or this suite silently installs a superseded policy and then
# tests it: the `github_sync_history` entry below was missing for the length of #650's
# review, so the only RLS suite in the repo was building the pre-#650 policy and no
# test covered the one that ships. The failure mode is worse than a gap -- the next
# person writes a test against the old policy, finds it failing on correct code, and
# "fixes" the migration to match. A range whose policy a *later* migration has since
# replaced is removed rather than left in place; see the note below.
#
# Only the **policy statements** from these ranges are replayed (see
# `_policy_statements`): they also carry schema DDL, and `pg_engine` has already
# applied the whole chain.
POLICY_REVISION_RANGES = (
    # #658: github_sync_history_tenant keyed on organization_id alone.
    #
    # **#650's range (`e3b8c2470f19:f1a0c6b47d38`) was listed here and had to be
    # removed, not merely left in front of this one.** It re-keyed the same policy
    # onto `organization_id` while keeping a second branch on
    # `github_org_registration_id`; #658 dropped that column, so replaying #650's
    # `CREATE POLICY` against the migrated schema raises `UndefinedColumn` and the
    # fixture dies before it reaches the statement that supersedes it. So this tuple
    # holds the ranges that define the policies **as they now stand** -- a
    # superseded entry is dropped from it, not stacked.
    "a7d4f2091c63:b4e9d1a72f05",
)

INSERT_PROJECT = (
    "insert into projects (id, name, alias, description, organization_id, "
    "created_at, updated_at, status, priority, tags) "
    "values (:id, :id, :id, 'x', :org, now(), now(), 'PLANNING', 'MEDIUM', '[]')"
)

ORG_A, ORG_B = "rls-org-a", "rls-org-b"
USER_A, USER_B, USER_PLATFORM = "rls-user-a", "rls-user-b", "rls-user-plat"


def _render(revision_range: str) -> str:
    """One migration range's SQL, generated offline (no connection)."""
    # Rendered against the **Postgres** dialect, not whatever `env.py` resolves
    # by default. Offline mode never connects, but it does pick a dialect from
    # the URL -- and with none set, `env.py` falls back to local SQLite, whose
    # dialect cannot express `ALTER ... CONSTRAINT` and raises
    # `NotImplementedError` mid-render. Earlier ranges happened to contain only
    # DDL SQLite could render, so this went unnoticed until a range carried a
    # constraint change; the failure then arrives as a fixture error on every
    # test in the file, naming a dialect nobody chose. `pg_engine` has already
    # resolved by the time this runs, so a Postgres URL is known to exist.
    from tests.conftest import POSTGRES_TEST_URL

    proc = subprocess.run(
        ["uv", "run", "alembic", "upgrade", revision_range, "--sql"],
        capture_output=True,
        text=True,
        env={
            **os.environ,
            "ENVIRONMENT": os.getenv("ENVIRONMENT", "local"),
            "MIGRATION_DATABASE_URL": POSTGRES_TEST_URL,
        },
    )
    if proc.returncode != 0 or "CREATE POLICY" not in proc.stdout:
        # Deliberately a failure, not a skip. This is only reached once `pg_engine`
        # has resolved, i.e. Postgres *is* reachable -- so nothing here is
        # environmental, and a skip would hide the policies going untested.
        pytest.fail(
            f"could not render {revision_range} offline "
            f"(rc={proc.returncode}): {proc.stderr[-400:]}"
        )
    return "\n".join(
        line
        for line in proc.stdout.splitlines()
        if line.strip() not in ("BEGIN;", "COMMIT;")
        and not line.startswith("UPDATE alembic_version")
    )


def _policy_statements(sql: str) -> str:
    """Only the policy statements out of a rendered range.

    A migration that changes a policy also carries the schema change that made the
    change necessary -- ADD COLUMN, ALTER COLUMN -- and `pg_engine` has already run
    the entire chain, so replaying that DDL here would fail on columns that exist.
    The policies are the only part wanted: this module drops the `innoday` schema,
    which cascade-drops every policy calling its helpers, and then rebuilds the
    policy layer from the migrations that define it.

    Split on `;` because a policy body contains none. `DROP POLICY IF EXISTS` is
    kept along with `CREATE POLICY`, which is what lets a later range supersede an
    earlier one in place.
    """
    kept = [stmt.strip() for stmt in sql.split(";") if " POLICY " in stmt.upper()]
    if not kept:
        pytest.fail("a range listed in POLICY_REVISION_RANGES changed no policy")
    return ";\n".join(kept) + ";"


def _policies_created_in(sql: str) -> set:
    """Names of the policies a rendered range creates."""
    return set(re.findall(r"CREATE POLICY\s+(\w+)\s+ON\s", sql, flags=re.IGNORECASE))


def _drop_superseded(baseline_sql: str, superseded: set) -> str:
    """The security migration's SQL, minus policies a later range re-creates.

    **Ordering stopped being enough once a superseded policy named a dropped
    column.** The security migration's `github_sync_history_tenant` keyed on
    `github_org_registration_id`; #658 dropped that column, so replaying that
    statement raises `UndefinedColumn` -- and because the whole script reaches
    Postgres as one query, the failure lands before the statement that would have
    replaced it ever runs. Every test in this module then errors at fixture setup,
    naming a column no test here is interested in.

    Removing it is right rather than a workaround: a later range in
    `POLICY_REVISION_RANGES` creates that policy, so the version being replaced
    contributes nothing to the text under test. Only the `CREATE POLICY` goes -- the
    range's `ALTER TABLE ... ENABLE ROW LEVEL SECURITY` must stay, since a policy on
    a table with RLS off is enforced against nobody.

    Matched as a whole statement (`CREATE POLICY name ON ... ;`), which is safe for
    the reason `_policy_statements` gives -- a policy body contains no `;` -- and
    leaves this range's PL/pgSQL function bodies, which do, untouched.
    """
    for name in sorted(superseded):
        pattern = re.compile(
            r"CREATE POLICY\s+" + re.escape(name) + r"\s+ON\s[^;]*;",
            flags=re.IGNORECASE,
        )
        baseline_sql, replaced = pattern.subn("", baseline_sql)
        if not replaced:
            pytest.fail(
                f"{name} is created by a range in POLICY_REVISION_RANGES but by no "
                f"statement in {RLS_REVISION_RANGE} -- either that range invents a "
                f"policy from nothing, or the name has drifted"
            )
    return baseline_sql


def _policy_sql() -> str:
    """The tenant-isolation policies as they stand today.

    The security migration first (PF-399 collapsed three ranges into one, which is
    why this no longer stitches them together), then the policy statements from every
    later migration that re-keyed one. Order is the point: a later range drops the
    policy the security migration installed and creates the current one in its place,
    so the text under test is the text that ships.

    The security migration's own version of a re-keyed policy is **removed** rather
    than merely overridden -- see `_drop_superseded` for why ordering alone stopped
    being sufficient.
    """
    later = [_policy_statements(_render(rng)) for rng in POLICY_REVISION_RANGES]
    superseded = set()
    for sql in later:
        superseded |= _policies_created_in(sql)
    parts = [_drop_superseded(_render(RLS_REVISION_RANGE), superseded)]
    parts.extend(later)
    return "\n".join(parts)


def _purge(engine) -> None:
    """Remove this module's rows. Runs as `postgres`, which bypasses RLS.

    Called on setup as well as teardown so a run interrupted mid-module does not
    poison the next one with a primary-key clash.
    """
    with engine.begin() as conn:
        # FK order: items -> summaries -> projects.
        conn.execute(text("delete from summary_items where id like 'rls-%'"))
        conn.execute(text("delete from summaries where id like 'rls-%'"))
        conn.execute(text("delete from user_identity where id like 'rls-%'"))
        conn.execute(text("delete from github_sync_history where id like 'rls-%'"))
        conn.execute(text("delete from projects where id like 'rls-%'"))
        conn.execute(text("delete from organization_memberships where id like 'rls-%'"))
        conn.execute(text("delete from users where id like 'rls-%'"))
        conn.execute(text("delete from organizations where id like 'rls-%'"))


@pytest.fixture(scope="module")
def rls_db(pg_engine):
    """Enable RLS on every table and install the policies, then seed two tenants."""
    with pg_engine.begin() as conn:
        tables = [
            row[0]
            for row in conn.execute(
                text(
                    "select c.relname from pg_class c "
                    "join pg_namespace n on n.oid = c.relnamespace "
                    "where n.nspname = 'public' and c.relkind = 'r'"
                )
            ).all()
        ]
        for table in tables:
            conn.execute(text(f'ALTER TABLE "{table}" ENABLE ROW LEVEL SECURITY'))
        conn.execute(text("DROP SCHEMA IF EXISTS innoday CASCADE"))
        conn.execute(text(_policy_sql()))

    _purge(pg_engine)

    with Session(pg_engine) as session:
        session.add(Organization(id=ORG_A, name="Alpha", alias="rls-alpha"))
        session.add(Organization(id=ORG_B, name="Beta", alias="rls-beta"))
        for uid, platform in (
            (USER_A, False),
            (USER_B, False),
            (USER_PLATFORM, True),
        ):
            session.add(
                User(
                    id=uid,
                    email=f"{uid}@example.com",
                    full_name=uid,
                    is_platform_member=platform,
                )
            )
        session.commit()
        for uid, org in ((USER_A, ORG_A), (USER_B, ORG_B)):
            session.add(
                OrganizationMembership(
                    id=f"rls-m-{uid}",
                    user_id=uid,
                    organization_id=org,
                    role=OrganizationRole.ADMIN,
                    is_active=True,
                )
            )
        for pid, org in (("rls-proj-a", ORG_A), ("rls-proj-b", ORG_B)):
            session.add(
                Project(
                    id=pid, name=pid, alias=pid, description="x", organization_id=org
                )
            )
        session.commit()
        # One summary per tenant, and one item hanging off each. The items are
        # the interesting half: `summary_items` has no organization_id, so its
        # policy reaches the tenant through `summary_id` -- see
        # 20260806_110000_summaries_rls_policies.py.
        for sid, pid, org in (
            ("rls-sum-a", "rls-proj-a", ORG_A),
            ("rls-sum-b", "rls-proj-b", ORG_B),
        ):
            session.add(
                Summary(
                    id=sid,
                    organization_id=org,
                    project_id=pid,
                    window_spec="",
                    summary_type=SummaryType.STATUS,
                    body_markdown="x",
                    motivational_quote="x",
                )
            )
        session.commit()
        for iid, sid in (("rls-item-a", "rls-sum-a"), ("rls-item-b", "rls-sum-b")):
            session.add(
                SummaryItem(id=iid, summary_id=sid, attribution=Attribution.NONE)
            )
        session.commit()
        # One claimed handle per tenant. Like `summary_items` this table has no
        # organization_id, but unlike it the parent is nullable: a NULL
        # `project_id` is a *global* handle belonging to no tenant, which is why
        # the policy's read and write halves differ. The global row here is
        # user A's, so B reading it is the read case and B writing one for A is
        # the write case.
        for iid, pid, uid, handle in (
            ("rls-ident-a", "rls-proj-a", USER_A, "rls-handle-a"),
            ("rls-ident-b", "rls-proj-b", USER_B, "rls-handle-b"),
            ("rls-ident-global", None, USER_A, "rls-handle-global"),
        ):
            session.add(
                UserIdentity(
                    id=iid,
                    user_id=uid,
                    project_id=pid,
                    platform=IdentityPlatform.GITHUB,
                    handle=handle,
                    match_source=MatchSource.MANUAL,
                )
            )
        session.commit()

    yield pg_engine

    _purge(pg_engine)
    with pg_engine.begin() as conn:
        conn.execute(text("DROP SCHEMA IF EXISTS innoday CASCADE"))


def _as_app(engine, claim: str, sql: str, params: dict | None = None):
    """Run `sql` as `innoday_app` with `claim` as the identity, then roll back."""
    with engine.connect() as conn:
        conn.execute(
            text("select set_config('innoday.user_id', :uid, true)"), {"uid": claim}
        )
        conn.execute(text("SET LOCAL ROLE innoday_app"))
        try:
            return conn.execute(text(sql), params or {}).all()
        finally:
            conn.rollback()


def _app_insert(engine, claim: str, org: str, row_id: str) -> str:
    try:
        with engine.connect() as conn:
            conn.execute(
                text("select set_config('innoday.user_id', :uid, true)"), {"uid": claim}
            )
            conn.execute(text("SET LOCAL ROLE innoday_app"))
            conn.execute(text(INSERT_PROJECT), {"org": org, "id": row_id})
            landed = conn.execute(
                text("select count(*) from projects where id = :i"), {"i": row_id}
            ).scalar()
            conn.rollback()
            return "inserted" if landed == 1 else f"dropped ({landed})"
    except Exception as exc:  # noqa: BLE001 - the message is the assertion
        if "row-level security" in str(exc):
            return "refused"
        return f"{exc.__class__.__name__}: {exc}"[:120]


def test_app_role_cannot_bypass_rls(rls_db):
    """The whole suite is vacuous if the role bypasses RLS, so assert it first."""
    with rls_db.connect() as conn:
        assert (
            conn.execute(
                text("select rolbypassrls from pg_roles where rolname = 'innoday_app'")
            ).scalar()
            is False
        )


# Scoped to this module's fixtures so the assertions hold on a database that
# already has unrelated rows (a developer's local Postgres, not just fresh CI).
OUR_PROJECTS = "select id from projects where id like 'rls-proj-%' order by id"


def test_members_see_only_their_own_org(rls_db):
    assert [r[0] for r in _as_app(rls_db, USER_A, OUR_PROJECTS)] == ["rls-proj-a"]
    assert [r[0] for r in _as_app(rls_db, USER_B, OUR_PROJECTS)] == ["rls-proj-b"]


def test_platform_member_sees_every_org(rls_db):
    assert [r[0] for r in _as_app(rls_db, USER_PLATFORM, OUR_PROJECTS)] == [
        "rls-proj-a",
        "rls-proj-b",
    ]


def test_absent_claim_denies_everything(rls_db):
    """Deny-by-default: an unset GUC must not read as "no filter"."""
    assert _as_app(rls_db, "", OUR_PROJECTS) == []
    assert _as_app(rls_db, "", "select id from organizations") == []


def test_cross_tenant_write_is_refused(rls_db):
    # Control first: the same statement must succeed for the owning tenant,
    # otherwise a refusal below proves nothing.
    assert _app_insert(rls_db, USER_A, ORG_A, "rls-control") == "inserted"
    assert _app_insert(rls_db, USER_A, ORG_B, "rls-evil") == "refused"
    assert _app_insert(rls_db, "", ORG_A, "rls-noclaim") == "refused"


OUR_ITEMS = "select id from summary_items where id like 'rls-item-%' order by id"

INSERT_ITEM = (
    "insert into summary_items (id, summary_id, attribution, rank, "
    "no_work_detected) values (:id, :sum, 'NONE', 0, false)"
)


def _app_insert_item(engine, claim: str, summary_id: str, row_id: str) -> str:
    """Same shape as `_app_insert`, against the indirect policy."""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("select set_config('innoday.user_id', :uid, true)"), {"uid": claim}
            )
            conn.execute(text("SET LOCAL ROLE innoday_app"))
            conn.execute(text(INSERT_ITEM), {"id": row_id, "sum": summary_id})
            landed = conn.execute(
                text("select count(*) from summary_items where id = :i"), {"i": row_id}
            ).scalar()
            conn.rollback()
            return "inserted" if landed == 1 else f"dropped ({landed})"
    except Exception as exc:  # noqa: BLE001 - the message is the assertion
        if "row-level security" in str(exc):
            return "refused"
        return f"{exc.__class__.__name__}: {exc}"[:120]


def test_summary_items_isolate_through_their_summary(rls_db):
    """The newer, indirect policy shape: no organization_id on the table at all.

    `summary_items_tenant` decides tenancy by looking the row's `summary_id` up
    in `summaries`. That subquery runs under the caller's own permissions, so an
    isolation bug here would not look like a leak in `summaries` -- it would look
    like `summary_items` having no opinion. Hence its own case.
    """
    assert [r[0] for r in _as_app(rls_db, USER_A, OUR_ITEMS)] == ["rls-item-a"]
    assert [r[0] for r in _as_app(rls_db, USER_B, OUR_ITEMS)] == ["rls-item-b"]
    assert [r[0] for r in _as_app(rls_db, USER_PLATFORM, OUR_ITEMS)] == [
        "rls-item-a",
        "rls-item-b",
    ]
    assert _as_app(rls_db, "", OUR_ITEMS) == []


def test_cross_tenant_summary_item_write_is_refused(rls_db):
    """WITH CHECK, not just USING -- writing into another tenant's summary.

    Control first, as everywhere in this module: a refusal only means something
    if the identical statement lands for the tenant who owns the summary.
    """
    assert _app_insert_item(rls_db, USER_A, "rls-sum-a", "rls-item-control") == (
        "inserted"
    )
    assert _app_insert_item(rls_db, USER_A, "rls-sum-b", "rls-item-evil") == "refused"
    assert _app_insert_item(rls_db, "", "rls-sum-a", "rls-item-noclaim") == "refused"


def test_security_definer_helpers_are_not_public(rls_db):
    """Postgres grants EXECUTE to PUBLIC by default; these must not keep it."""
    with rls_db.connect() as conn:
        for fn in (
            "innoday.is_platform_member()",
            "innoday.member_org_ids()",
            "innoday.current_user_id()",
        ):
            assert (
                conn.execute(
                    text("select has_function_privilege('public', :fn, 'EXECUTE')"),
                    {"fn": fn},
                ).scalar()
                is False
            ), f"{fn} is callable by PUBLIC"


def test_claim_and_role_do_not_outlive_the_transaction(rls_db):
    """The pooler recycles connections; a leaked claim is a cross-tenant read."""
    with rls_db.connect() as conn:
        conn.execute(
            text("select set_config('innoday.user_id', :uid, true)"), {"uid": USER_A}
        )
        conn.execute(text("SET LOCAL ROLE innoday_app"))
        conn.rollback()
        assert conn.execute(
            text("select current_setting('innoday.user_id', true)")
        ).scalar() in (None, "")
        assert conn.execute(text("select current_user")).scalar() != "innoday_app"


OUR_IDENTITIES = "select id from user_identity where id like 'rls-ident-%' order by id"

INSERT_IDENTITY = (
    "insert into user_identity (id, user_id, project_id, platform, handle, "
    "match_source, created_at, updated_at) "
    "values (:id, :uid, :pid, 'GITHUB', :handle, 'MANUAL', now(), now())"
)


def _app_insert_identity(engine, claim, *, user_id, project_id, row_id) -> str:
    try:
        with engine.connect() as conn:
            conn.execute(
                text("select set_config('innoday.user_id', :uid, true)"), {"uid": claim}
            )
            conn.execute(text("SET LOCAL ROLE innoday_app"))
            conn.execute(
                text(INSERT_IDENTITY),
                {
                    "id": row_id,
                    "uid": user_id,
                    "pid": project_id,
                    "handle": f"h-{row_id}",
                },
            )
            landed = conn.execute(
                text("select count(*) from user_identity where id = :i"), {"i": row_id}
            ).scalar()
            conn.rollback()
            return "inserted" if landed == 1 else f"dropped ({landed})"
    except Exception as exc:  # noqa: BLE001 - the message is the assertion
        if "row-level security" in str(exc):
            return "refused"
        return f"{exc.__class__.__name__}: {exc}"[:120]


def test_user_identity_isolates_through_its_project(rls_db):
    """`user_identity` shipped with no RLS at all -- neither enabled nor a policy.

    It is the third indirect shape in this module, and the awkward one: the
    parent is *nullable*, and a NULL `project_id` is a global handle belonging
    to no tenant. Project-scoped rows are org-isolated; the global row is
    readable by any resolved caller, because
    `IdentityResolutionService.resolve` maps a handle to whoever owns it and a
    lookup restricted to the owner would answer "unmapped" for everyone else.
    """
    assert [r[0] for r in _as_app(rls_db, USER_A, OUR_IDENTITIES)] == [
        "rls-ident-a",
        "rls-ident-global",
    ]
    # B sees its own project row and the global one -- but never A's project row.
    assert [r[0] for r in _as_app(rls_db, USER_B, OUR_IDENTITIES)] == [
        "rls-ident-b",
        "rls-ident-global",
    ]
    assert [r[0] for r in _as_app(rls_db, USER_PLATFORM, OUR_IDENTITIES)] == [
        "rls-ident-a",
        "rls-ident-b",
        "rls-ident-global",
    ]
    # Deny-by-default: an unset claim is not "no filter", and it must not make
    # the global row visible either.
    assert _as_app(rls_db, "", OUR_IDENTITIES) == []


def test_cross_tenant_identity_write_is_refused(rls_db):
    """Control first, as everywhere in this module."""
    assert (
        _app_insert_identity(
            rls_db, USER_A, user_id=USER_A, project_id="rls-proj-a", row_id="rls-i-ctl"
        )
        == "inserted"
    )
    assert (
        _app_insert_identity(
            rls_db, USER_A, user_id=USER_A, project_id="rls-proj-b", row_id="rls-i-evil"
        )
        == "refused"
    )
    assert (
        _app_insert_identity(
            rls_db, "", user_id=USER_A, project_id="rls-proj-a", row_id="rls-i-noclaim"
        )
        == "refused"
    )


def test_a_global_handle_may_only_be_claimed_for_yourself(rls_db):
    """Read and write diverge for `project_id IS NULL`, deliberately.

    A global row is visible to everyone (above), but claiming a platform-wide
    handle *on someone else's behalf* has no caller and would be a hole.
    """
    assert (
        _app_insert_identity(
            rls_db, USER_A, user_id=USER_A, project_id=None, row_id="rls-i-mine"
        )
        == "inserted"
    )
    assert (
        _app_insert_identity(
            rls_db, USER_B, user_id=USER_A, project_id=None, row_id="rls-i-theirs"
        )
        == "refused"
    )


def test_the_user_identity_migration_enables_rls_as_well_as_adding_a_policy(rls_db):
    """The fixture force-enables RLS on every table, so it cannot catch a
    migration that adds a policy and forgets `ENABLE ROW LEVEL SECURITY` --
    and a policy on a table with RLS off is enforced against nobody. Assert it
    against the migration's own rendered SQL instead."""
    sql = _render(RLS_REVISION_RANGE)
    assert "ALTER TABLE user_identity ENABLE ROW LEVEL SECURITY" in sql
    assert "CREATE POLICY user_identity_tenant ON user_identity" in sql
    # The trap CLAUDE.md names: auth.uid() is NULL for CLI-token auth, so a
    # policy keyed on it reads as a guarantee and matches nothing.
    assert "auth.uid()" not in sql
    assert "innoday.current_user_id()" in sql


INSERT_SYNC_HISTORY = (
    "insert into github_sync_history (id, organization_id, project_id, started_at, "
    "status, repositories_synced, repositories_created, repositories_updated, "
    "repositories_failed, readmes_synced) "
    "values (:id, :org, :proj, now(), 'failed', 1, 0, 0, 0, 0)"
)


def _app_insert_sync_history(
    engine, claim: str, *, org: str, project: str | None, row_id: str
) -> str:
    """Same shape as `_app_insert`, against the github_sync_history policy."""
    try:
        with engine.connect() as conn:
            conn.execute(
                text("select set_config('innoday.user_id', :uid, true)"), {"uid": claim}
            )
            conn.execute(text("SET LOCAL ROLE innoday_app"))
            conn.execute(
                text(INSERT_SYNC_HISTORY),
                {"id": row_id, "org": org, "proj": project},
            )
            landed = conn.execute(
                text("select count(*) from github_sync_history where id = :i"),
                {"i": row_id},
            ).scalar()
            conn.rollback()
            return "inserted" if landed == 1 else f"dropped ({landed})"
    except Exception as exc:  # noqa: BLE001 - the message is the assertion
        if "row-level security" in str(exc):
            return "refused"
        return f"{exc.__class__.__name__}: {exc}"[:120]


def test_a_project_sync_row_isolates_on_its_organization(rls_db):
    """`github_sync_history` keyed on the organization, which is its only key.

    The policy used to key entirely on `github_org_registration_id`. A project sync
    has no registration in scope -- `connect_github_organization` creates that row
    only when a user is attributable, and syncs perfectly well without one -- so
    every row it writes had NULL there. Under RLS a NULL `IN (subquery)` yields NULL
    rather than true, so the `WITH CHECK` failed and the **INSERT was refused**: the
    day `INNODAY_RLS_ENFORCE` is switched on, every project sync would have raised a
    policy violation from the code whose only job is to record that a sync failed.
    #658 then dropped that column and the policy branch reading it, so
    `organization_id` is the only key there is.

    Both halves are asserted for the reason this module's docstring gives. The
    positive control is the property the migration exists to provide -- a member of
    the organization can write the row at all. The refusals are what make it
    isolation rather than an open door, and the org key is now the *only* thing
    standing between the two.
    """
    assert (
        _app_insert_sync_history(
            rls_db, USER_A, org=ORG_A, project="rls-proj-a", row_id="rls-hist-mine"
        )
        == "inserted"
    )
    assert (
        _app_insert_sync_history(
            rls_db, USER_B, org=ORG_A, project="rls-proj-a", row_id="rls-hist-theirs"
        )
        == "refused"
    )
    assert (
        _app_insert_sync_history(
            rls_db, "", org=ORG_A, project="rls-proj-a", row_id="rls-hist-noclaim"
        )
        == "refused"
    )
    # A platform member writes across tenants by design, and asserting it here keeps
    # the refusals above from being read as "nobody can write this table".
    assert (
        _app_insert_sync_history(
            rls_db,
            USER_PLATFORM,
            org=ORG_B,
            project="rls-proj-b",
            row_id="rls-hist-plat",
        )
        == "inserted"
    )
