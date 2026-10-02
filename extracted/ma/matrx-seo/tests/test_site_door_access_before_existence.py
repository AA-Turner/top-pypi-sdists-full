"""Every site-gated ``seo`` door decides ACCESS BEFORE EXISTENCE.

WHAT THIS CATCHES (name the break before the body):
  * a door that answers one thing for a REAL site the caller may not see and
    another for an INVENTED uuid — an existence oracle. Until 0790 that was the
    whole ``seo.gsc_assert_site_editor`` / ``seo.gsc_assert_site_access`` class:
    ``P0002 gsc_site_not_found: <id>`` was raised before the access check, so a
    stranger could enumerate which site ids exist through any of the 136 doors
    that lean on those two helpers;
  * a door whose NULL site id is anything but ``22023`` naming the argument —
    the seven page-mapper doors DECLARED ``p_site_id=22023`` in their
    ``platform.client_callable_door`` rows while four raised a bare ``P0001``
    and three had no guard at all and fell through to ``gsc_site_not_found:
    <NULL>``;
  * a class fix that was only applied to the doors somebody remembered: the
    table below carries eight NON-mapper doors, on both helpers, so the fix is
    proven at the helper and not assumed.

Live database, ONE transaction, ALWAYS rolled back. It seeds its own disposable
world (two users, two organizations, brand/site/page each) and runs every probe
as a signed-in user (``set local role authenticated`` + JWT claims) inside a
savepoint, exactly like ``test_topical_map_door_contract.py``.

Run:  uv run pytest packages/matrx-seo/tests/test_site_door_access_before_existence.py
"""

# ruff: noqa: E501  — the probes are SQL statements and verbatim failure sentences

from __future__ import annotations

import json
import os
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import pytest

psycopg = pytest.importorskip("psycopg")

ACTOR_SYSTEM = "seo-site-door-access-before-existence-test"
INVENTED = "00000000-0000-4000-8000-0000000d0001"


def _dsn() -> str | None:
    if "SUPABASE_MATRIX_HOST" not in os.environ:
        env_file = Path(__file__).resolve().parents[3] / ".env"
        if env_file.exists():
            from dotenv import load_dotenv

            load_dotenv(env_file)
    keys = ("HOST", "PORT", "DATABASE_NAME", "USER", "PASSWORD")
    if any(f"SUPABASE_MATRIX_{k}" not in os.environ for k in keys):
        return None
    return psycopg.conninfo.make_conninfo(
        host=os.environ["SUPABASE_MATRIX_HOST"],
        port=os.environ["SUPABASE_MATRIX_PORT"],
        dbname=os.environ["SUPABASE_MATRIX_DATABASE_NAME"],
        user=os.environ["SUPABASE_MATRIX_USER"],
        password=os.environ["SUPABASE_MATRIX_PASSWORD"],
        sslmode="require",
        connect_timeout=20,
    )


# ─────────────────────────────────────────────────────────────────────────────
# The disposable world
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class World:
    user: str
    site: str
    page: str
    foreign_site: str


def _one(cur: Any, sql: str, args: tuple | None = None) -> Any:
    cur.execute(sql, args)
    return cur.fetchone()[0]


def _claims(cur: Any, user_id: str | None) -> None:
    value = json.dumps({"sub": user_id, "role": "authenticated"}) if user_id else ""
    cur.execute("select set_config('request.jwt.claims', %s, true)", (value,))


def _seed_tenant(cur: Any, tag: str) -> dict[str, str]:
    user = str(uuid.uuid4())
    _claims(cur, None)
    cur.execute(
        "insert into auth.users (id, email, aud, role, instance_id, raw_app_meta_data) values "  # matrx-fixture:rollback-only rolled back in finally
        "(%s, %s, 'authenticated', 'authenticated', '00000000-0000-0000-0000-000000000000', jsonb_build_object('test_fixture', jsonb_build_object('suite', 'rolled-back-suite', 'purpose', 'account inside a rolled-back transaction', 'expires_at', '2026-10-01T00:00:00Z')))",
        (user, f"site-door-abe-{user}@example.invalid"),  # matrx-fixture:rollback-only rolled back in finally
    )
    _claims(cur, user)  # created_by is stamped from the claims: this user OWNS what follows
    org = _one(
        cur,
        "insert into iam.organizations (name, slug, abbreviation) values (%s,%s,%s) returning id",
        (f"ABE {tag} {user}", f"abe-{tag.lower()}-{user}", f"AB{tag}"),
    )
    brand = _one(
        cur,
        "insert into web.brand (organization_id, name) values (%s,%s) returning id",
        (org, f"ABE brand {tag}"),
    )
    host = f"abe-{tag.lower()}-{user[:8]}.invalid"
    site = _one(
        cur,
        "insert into web.site (organization_id, name, root_url, domain, brand_id) "
        "values (%s,%s,%s,%s,%s) returning id",
        (org, f"ABE site {tag}", f"https://{host}", host, brand),
    )
    page_id = str(uuid.uuid4())
    url = f"https://{host}/p1"
    cur.execute(
        "insert into web.page (id, organization_id, site_id, url, url_hash, provenance, canonical_page_id) "
        "values (%s,%s,%s,%s, md5(%s), 'manual', %s)",
        (page_id, org, site, url, url, page_id),
    )
    return {"user": user, "org": str(org), "site": str(site), "page": page_id}


@pytest.fixture(scope="module")
def db() -> Iterator[tuple[Any, World]]:
    dsn = _dsn()
    if dsn is None:
        pytest.skip("SUPABASE_MATRIX_* not set: this contract needs the live database")
    conn = psycopg.connect(dsn, autocommit=False, prepare_threshold=None)
    try:
        cur = conn.cursor()
        from matrx_orm.pytest_lock_guard import apply_ceilings

        apply_ceilings(cur)
        # Seeding inserts into iam.organizations, whose new-user trigger competes
        # with whatever else is writing right now; the ceiling's default
        # lock_timeout is deliberately short for PROBES, and the doctrine says a
        # statement that needs longer says so for itself.
        cur.execute("set local lock_timeout = '20s'")
        cur.execute("select set_config('app.actor_system', %s, true)", (ACTOR_SYSTEM,))
        me = _seed_tenant(cur, "A")
        foreign = _seed_tenant(cur, "F")
        _claims(cur, None)
        yield (
            cur,
            World(
                user=me["user"], site=me["site"], page=me["page"], foreign_site=foreign["site"]
            ),
        )
    finally:
        conn.rollback()  # ALWAYS: nothing this test writes survives it
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# The table: door -> (sql template, the extra arguments after the site id)
#
# `{site}` is the only placeholder. Every door here takes a web.site id as its
# first argument and reaches it through one of the two helpers.
# ─────────────────────────────────────────────────────────────────────────────

MAPPER_DOORS: dict[str, str] = {
    # editor lane
    "fn_refresh_page_mapping_queue": "select * from seo.fn_refresh_page_mapping_queue({site}, 28)",
    "fn_claim_page_mapping_batch": "select * from seo.fn_claim_page_mapping_batch({site}, 1, 3, 30)",
    "fn_complete_page_mapping_batch": "select * from seo.fn_complete_page_mapping_batch({site}, '{{}}'::uuid[], null, 3, false, '[]'::jsonb)",
    # access lane
    "fn_page_mapping_counts": "select * from seo.fn_page_mapping_counts({site})",
    "page_mapping_status": "select * from seo.page_mapping_status({site})",
    "page_mapping_wanted_topics": "select * from seo.page_mapping_wanted_topics({site}, 25)",
    "fn_page_mapping_settled_since": "select * from seo.fn_page_mapping_settled_since({site}, now() - interval '1 day')",
}

# The census says the two helpers carry 136 other doors. These eight are the
# proof that the fix is at the HELPER: five readers and one writer on the access
# lane, one writer on the editor lane, and one door outside the `seo` schema.
OTHER_DOORS: dict[str, str] = {
    "gsc_perf_freshness": "select * from seo.gsc_perf_freshness({site})",
    "gsc_site_kw_guidelines": "select * from seo.gsc_site_kw_guidelines({site})",
    "gsc_brand_identity": "select * from seo.gsc_brand_identity({site})",
    "gsc_location_readiness": "select * from seo.gsc_location_readiness({site})",
    "gsc_site_meaning_health": "select * from seo.gsc_site_meaning_health({site})",
    "gsc_value_rule_health": "select * from seo.gsc_value_rule_health({site})",
    "gsc_set_site_kw_guidelines": "select seo.gsc_set_site_kw_guidelines({site}, 'abe probe')",
    "web_site_offerings": "select * from web.site_offerings({site})",
}

ALL_DOORS: dict[str, str] = {**MAPPER_DOORS, **OTHER_DOORS}


@dataclass
class Outcome:
    ok: bool
    code: str | None
    message: str


def _as_me(cur: Any, w: World, sql: str) -> Outcome:
    cur.execute("savepoint probe")
    try:
        try:
            cur.execute("set local role authenticated")
            _claims(cur, w.user)
            cur.execute(sql)
            cur.fetchall()
        except psycopg.Error as exc:
            cur.execute("rollback to savepoint probe")
            return Outcome(False, exc.sqlstate, exc.diag.message_primary or str(exc))
        cur.execute("rollback to savepoint probe")
        return Outcome(True, None, "")
    finally:
        cur.execute("reset role")


def _sql(template: str, site: str | None) -> str:
    return template.format(site="null::uuid" if site is None else f"'{site}'::uuid")


@pytest.mark.parametrize("door", sorted(ALL_DOORS))
def test_null_site_is_22023_naming_the_argument(db: tuple[Any, World], door: str) -> None:
    cur, w = db
    got = _as_me(cur, w, _sql(ALL_DOORS[door], None))
    assert not got.ok, f"{door}: a NULL site id was accepted"
    assert got.code == "22023", f"{door}: NULL site answered {got.code} {got.message}, wanted 22023"
    assert "p_site_id" in got.message, (
        f"{door}: the 22023 does not name the argument: {got.message}"
    )


@pytest.mark.parametrize("door", sorted(ALL_DOORS))
def test_foreign_and_invented_site_answer_alike(db: tuple[Any, World], door: str) -> None:
    """THE ORACLE TEST. A real site the caller may not see and a uuid that names
    no row at all must be indistinguishable — same SQLSTATE, byte-identical
    message. Anything else lets a stranger ask the database which ids exist."""
    cur, w = db
    template = ALL_DOORS[door]
    foreign = _as_me(cur, w, _sql(template, w.foreign_site))
    invented = _as_me(cur, w, _sql(template, INVENTED))

    assert not foreign.ok, f"{door}: another tenant's site id was ACCEPTED"
    assert not invented.ok, f"{door}: an invented site id was ACCEPTED"
    assert foreign.code == invented.code, (
        f"{door}: existence oracle — foreign id answers {foreign.code}, "
        f"invented id answers {invented.code}"
    )
    assert foreign.message == invented.message, (
        f"{door}: existence oracle — foreign id says {foreign.message!r}, "
        f"invented id says {invented.message!r}"
    )
    assert foreign.code == "42501", (
        f"{door}: a refusal must be 42501, got {foreign.code} {foreign.message}"
    )
    assert w.foreign_site not in foreign.message and INVENTED not in invented.message, (
        f"{door}: the refusal echoes the id back, which tells the two cases apart: {foreign.message!r}"
    )


@pytest.mark.parametrize("door", sorted(ALL_DOORS))
def test_the_legal_call_still_works(db: tuple[Any, World], door: str) -> None:
    """The class fix is only a fix if the success path is untouched."""
    cur, w = db
    got = _as_me(cur, w, _sql(ALL_DOORS[door], w.site))
    assert got.ok, f"{door}: the owner's own legal call failed: {got.code} {got.message}"
