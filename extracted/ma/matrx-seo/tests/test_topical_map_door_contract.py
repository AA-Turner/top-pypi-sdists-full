"""The door contract of the 23 client-callable ``seo.*map*`` functions.

WHAT THIS CATCHES (name the break before the body):
  * a door body whose guard SKIPS on NULL — ``IF jsonb_typeof(p) <> 'array'`` is
    NULL for a NULL argument, not true — and then does destructive work
    (round 3: ``replace_map_section(map,'locations',NULL)`` retired live topics,
    ``set_page_map_topics(page,NULL)`` deleted a page's coverage edges);
  * a door whose error for ANOTHER TENANT'S id differs from its error for an id
    that does not exist (an existence oracle);
  * a reader that hands back another tenant's association payload or row id
    (round 3: ``map_topic_associations`` returned a foreign page's id and the
    ``reason`` its mapper wrote);
  * a door row in ``platform.client_callable_door`` whose declared NULL /
    FOREIGN rule is not what the body does, or that does not name an argument;
  * a reader that COUNTS what it will not show (round 17: ``map_topic_associations``
    appended ``{type, hidden: n}`` per kind, a number a stranger could raise on
    another company's topic) — the round-18 test below holds every reader's bytes
    equal in a world with and without rows the caller cannot open.

The TABLE below is the contract: per door, per argument, a legal value, the NULL
rule, and a foreign-vs-invented probe. The door row declares the same rules in
its ``reason`` (``NULL RULES: … | FOREIGN: …``) and the test holds the two equal,
so a generated door and a generated test cannot drift apart.

Live database, ONE transaction, ALWAYS rolled back. It seeds its own disposable
world (two users, two organizations, brand/site/pages/map each, a foreign page
covering one of our topics with a planted payload) and runs every probe as a
signed-in user (``set local role authenticated`` + JWT claims) inside a savepoint.

Run:  uv run pytest packages/matrx-seo/tests/test_topical_map_door_contract.py
"""

# ruff: noqa: E501  — the probes are SQL statements and verbatim failure sentences

from __future__ import annotations

import json
import os
import re
import uuid
from collections.abc import Callable, Iterator
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest

psycopg = pytest.importorskip("psycopg")

MARKER = "FOREIGN-SECRET-REASON"
ACTOR_SYSTEM = "seo-topical-map-door-contract-test"


# ─────────────────────────────────────────────────────────────────────────────
# Connection
# ─────────────────────────────────────────────────────────────────────────────


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
    me: dict[str, str]
    foreign: dict[str, str]
    topics: dict[str, str]
    foreign_ids: list[str] = field(default_factory=list)

    def __getattr__(self, key: str) -> str:  # W.map, W.site … are OUR ids
        try:
            return self.me[key]
        except KeyError as exc:
            raise AttributeError(key) from exc


def _one(cur: Any, sql: str, args: tuple | dict | None = None) -> Any:
    cur.execute(sql, args)
    return cur.fetchone()[0]


def _claims(cur: Any, user_id: str | None) -> None:
    value = json.dumps({"sub": user_id, "role": "authenticated"}) if user_id else ""
    cur.execute("select set_config('request.jwt.claims', %s, true)", (value,))


def _seed_tenant(cur: Any, tag: str) -> dict[str, str]:
    user = str(uuid.uuid4())
    _claims(cur, None)  # a user row is created by the server lane, never "as" a previous user
    cur.execute(
        "insert into auth.users (id, email, aud, role, instance_id, raw_app_meta_data) values "  # matrx-fixture:rollback-only rolled back in finally
        "(%s, %s, 'authenticated', 'authenticated', '00000000-0000-0000-0000-000000000000', jsonb_build_object('test_fixture', jsonb_build_object('suite', 'rolled-back-suite', 'purpose', 'account inside a rolled-back transaction', 'expires_at', '2026-10-01T00:00:00Z')))",
        (user, f"tm-door-contract-{user}@example.invalid"),  # matrx-fixture:rollback-only rolled back in finally
    )
    _claims(cur, user)  # created_by is stamped from the claims: the user OWNS what follows
    org = _one(
        cur,
        "insert into iam.organizations (name, slug, abbreviation) values (%s, %s, %s) returning id",
        (f"TM door contract {tag} {user}", f"tm-door-{tag.lower()}-{user}", f"TM{tag}"),
    )
    brand = _one(
        cur,
        "insert into web.brand (organization_id, name) values (%s, %s) returning id",
        (org, f"TMDC brand {tag}"),
    )
    host = f"tmdc-{tag.lower()}-{user[:8]}.invalid"
    site = _one(
        cur,
        "insert into web.site (organization_id, name, root_url, domain, brand_id) values (%s,%s,%s,%s,%s) returning id",
        (org, f"TMDC site {tag}", f"https://{host}", host, brand),
    )
    pages = []
    for n in (1, 2):
        pid = str(uuid.uuid4())
        url = f"https://{host}/p{n}"
        cur.execute(
            "insert into web.page (id, organization_id, site_id, url, url_hash, provenance, canonical_page_id) "
            "values (%s, %s, %s, %s, md5(%s), 'manual', %s)",
            (pid, org, site, url, url, pid),
        )
        pages.append(pid)
    tmap = _one(
        cur,
        "insert into seo.topical_map (organization_id, brand_id, name) values (%s,%s,%s) returning id",
        (org, brand, f"TMDC map {tag}"),
    )
    return {
        "user": user,
        "org": str(org),
        "brand": str(brand),
        "site": str(site),
        "page": pages[0],
        "page2": pages[1],
        "map": str(tmap),
    }


def _seed(cur: Any) -> World:
    cur.execute("select set_config('app.actor_system', %s, true)", (ACTOR_SYSTEM,))
    me = _seed_tenant(cur, "A")
    foreign = _seed_tenant(cur, "F")
    _claims(cur, None)  # the edges below are server-lane writes (the kind a DB-side job makes)

    topics: dict[str, str] = {}

    def topic(map_id: str, org: str, slug: str, parent: str | None, status: str = "active") -> str:
        tid = _one(
            cur,
            "insert into seo.map_topic (organization_id, map_id, slug, name, parent_id, status) values (%s,%s,%s,%s,%s,%s) returning id",
            (org, map_id, slug, slug.title(), topics.get(parent) if parent else None, status),
        )
        return str(tid)

    for slug, parent, status in (
        ("alpha", None, "active"),
        ("alpha-kid", "alpha", "active"),
        ("beta", None, "active"),
        ("sect", None, "active"),
        ("sect-a", "sect", "active"),
        ("sect-b", "sect", "active"),
        # ROUND 19: `rejected` is what happens to a PROPOSAL. A world with no
        # proposal in it cannot test the rejection door at all.
        ("prop", None, "proposed"),
    ):
        topics[slug] = topic(me["map"], me["org"], slug, parent, status)
    foreign_topic = topic(foreign["map"], foreign["org"], "foreign-only", None)

    def edge(
        src_t: str,
        src: str,
        tgt_t: str,
        tgt: str,
        org: str,
        role: str | None,
        payload: dict | None = None,
    ) -> str:
        return str(
            _one(
                cur,
                "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
                "values (%s,%s,%s,%s,%s,%s,%s,%s::jsonb) returning id",
                (
                    src_t,
                    src,
                    tgt_t,
                    tgt,
                    org,
                    role,
                    "map_topic_coverage" if payload else None,
                    json.dumps(payload) if payload else None,
                ),
            )
        )

    edge("web_site", me["site"], "seo_topical_map", me["map"], me["org"], "uses")
    # A foreign site bound to OUR map: sites_using_map must never name it.
    foreign_uses = edge(
        "web_site", foreign["site"], "seo_topical_map", me["map"], foreign["org"], "uses"
    )
    for page, slug in ((me["page"], "alpha"), (me["page2"], "alpha"), (me["page2"], "sect-b")):
        edge(
            "web_page",
            page,
            "seo_map_topic",
            topics[slug],
            me["org"],
            "covers",
            {"confidence": 70, "source": "agent", "reason": "own reason"},
        )
    # THE PLANT: another tenant's page covering our topic, with a payload only its mapper wrote.
    foreign_edge = edge(
        "web_page",
        foreign["page"],
        "seo_map_topic",
        topics["alpha"],
        foreign["org"],
        "covers",
        {"confidence": 90, "source": "human", "reason": MARKER},
    )

    region = _one(
        cur,
        "select id from seo.map_facet where key = 'region' and deleted_at is null order by created_at limit 1",
    )
    foreign_facet = _one(
        cur,
        "insert into seo.map_facet (organization_id, key, label, applies_to) values (%s, 'tmdc_foreign_facet', 'Foreign facet', 'both') returning id",
        (foreign["org"],),
    )
    own_value = _one(
        cur,
        "insert into seo.map_facet_value (organization_id, facet_id, brand_id, slug, name, ref_type, ref_id) "
        "values (%s,%s,%s,'tmdc-own','Own value','web_site',%s) returning id",
        (me["org"], region, me["brand"], me["site"]),
    )
    foreign_value = _one(
        cur,
        "insert into seo.map_facet_value (organization_id, facet_id, brand_id, slug, name, ref_type, ref_id) "
        "values (%s,%s,%s,'tmdc-foreign-val','Foreign value','web_site',%s) returning id",
        (foreign["org"], region, foreign["brand"], foreign["site"]),
    )
    edge("seo_map_topic", topics["beta"], "seo_map_facet_value", str(own_value), me["org"], "facet")
    edge("web_page", me["page"], "seo_map_facet_value", str(own_value), me["org"], "facet")

    me["own_value"] = str(own_value)
    foreign["value"] = str(foreign_value)
    return World(
        me=me,
        foreign=foreign,
        topics=topics,
        foreign_ids=[
            foreign["user"],
            foreign["org"],
            foreign["brand"],
            foreign["site"],
            foreign["page"],
            foreign["page2"],
            foreign["map"],
            str(foreign_value),
            str(foreign_facet),
            foreign_topic,
            foreign_edge,
            foreign_uses,
        ],
    )


@pytest.fixture(scope="module")
def db() -> Iterator[tuple[Any, World]]:
    dsn = _dsn()
    if dsn is None:
        pytest.skip("SUPABASE_MATRIX_* not set: the door contract needs the live database")
    conn = psycopg.connect(dsn, autocommit=False, prepare_threshold=None)
    try:
        cur = conn.cursor()
        # THE CEILINGS, first statement in the transaction (production outage
        # 2026-09-15). This fixture is ONE module-scoped transaction full of
        # savepoints: between probes it sits `idle in transaction` holding
        # whatever it has taken, and one such session — this suite's, after a
        # `rollback to savepoint r18call` — was blocker (a) that night. With no
        # timeouts set it could sit there until a human found it. These bound it:
        # lock_timeout so it can never JOIN a queue, statement_timeout so no probe
        # runs away, idle_in_transaction_session_timeout so an abandoned run ends
        # itself, and an application_name that says which pytest process it is.
        # Transaction-local, so nothing leaks onto the pooled connection.
        # Any probe needing longer says SET LOCAL for itself and wins.
        from matrx_orm.pytest_lock_guard import apply_ceilings

        apply_ceilings(cur)
        # REHEARSING A HELD MIGRATION AGAINST THIS SUITE. A file that needs a
        # chair-step confirmation runs only when a command NAMES it
        # (--confirm-chair-step <file>), so until the owning session applies it its
        # bodies are not live and every test written against them is red for a reason
        # that is not a defect. MATRX_APPLY_SQL runs one .sql file INSIDE this
        # transaction — which is rolled back like everything else here — so
        # "green after" is a command anyone can re-run, not a claim:
        #   MATRX_APPLY_SQL=packages/matrx-seo/matrx_seo/migrations/<file>.sql \
        #     uv run pytest packages/matrx-seo/tests/test_topical_map_door_contract.py
        pending = os.environ.get("MATRX_APPLY_SQL")
        if pending:
            cur.execute(Path(pending).read_text(encoding="utf-8"))
        world = _seed(cur)
        yield cur, world
    finally:
        conn.rollback()  # ALWAYS: nothing this test writes survives it
        conn.close()


# ─────────────────────────────────────────────────────────────────────────────
# The table
# ─────────────────────────────────────────────────────────────────────────────

V = Callable[[World], Any]
Expect = Callable[[Any, World], bool] | str | None


@dataclass
class Null:
    """What NULL means for one argument.

    kind '22023'           -> the call raises 22023 naming the argument; nothing changes.
    kind 'MEANS'/'DEFAULT' -> NULL is a value. ``expect`` is None (the call succeeds),
                              'ERR:xxxxx' (it raises that code — the NULL was read as
                              the declared value and hit a real rule), a SQL effect
                              (true afterwards), or a callable on the decoded output.
    ``override`` replaces other arguments' legal values for this probe only.
    """

    kind: str
    expect: Expect = None
    override: dict[str, V] = field(default_factory=dict)


@dataclass
class Foreign:
    """Another tenant's token vs an invented one: the outcomes must be identical.

    ``code`` is the SQLSTATE both must raise, or 'SAME' (identical outcome of any kind).
    ``build`` turns the token into the argument value.
    """

    code: str
    foreign: V
    invented: V
    build: Callable[[World, str], Any] = lambda _w, tok: tok


@dataclass
class Arg:
    name: str
    type: str
    legal: V
    null: Null
    foreign: Foreign | None = None


def _inv(_w: World) -> str:
    return str(uuid.uuid4())


def _nope(_w: World) -> str:
    return f"nope-{uuid.uuid4().hex[:10]}"


def MAP(level_code: str = "42501") -> Foreign:
    return Foreign(level_code, lambda w: w.foreign["map"], _inv)


SLUG = Foreign("P0002", lambda _w: "foreign-only", _nope)
E22 = Null("22023")


def _j(v: Any) -> str:
    return json.dumps(v)


def _visible_assoc(out: Any, _w: World) -> bool:
    # Round 18: the foreign page covering alpha is ABSENT — no row, no count, no marker.
    return (
        sorted(a["item"]["id"] for a in out if a["item"]["type"] == "web_page")
        == sorted([_w.page, _w.page2])
        and not any("hidden" in a["item"] for a in out)
    )


def _alpha_pages(out: Any, _w: World) -> bool:
    nodes = {n["data"]["slug"]: n["data"] for n in out["nodes"] if n["type"] == "topic"}
    return (
        nodes["alpha"]["page_count"] == 2
        and nodes["sect-b"]["page_count"] == 1
        and nodes["beta"]["page_count"] == 0
    )


DOORS: dict[str, list[Arg]] = {
    "create_map_facet_values": [
        Arg(
            "p_brand_id",
            "uuid",
            lambda w: w.brand,
            E22,
            Foreign("42501", lambda w: w.foreign["brand"], _inv),
        ),
        Arg(
            "p_facet_key",
            "text",
            lambda _w: "region",
            E22,
            Foreign("P0002", lambda _w: "tmdc_foreign_facet", _nope),
        ),
        Arg(
            "p_values",
            "jsonb",
            lambda _w: _j([{"slug": "tmdc-new", "name": "New"}]),
            E22,
            Foreign(
                "42501",
                lambda w: w.foreign["site"],
                _inv,
                lambda _w, tok: _j(
                    [{"slug": "tmdc-ref", "name": "R", "ref_type": "web_site", "ref_id": tok}]
                ),
            ),
        ),
    ],
    # ─────────────────────────────────────────────────────────────────────────
    # ROUND 19 — the page-intent surface. Same three questions as every door
    # above: what does a legal call do, what does each argument's NULL mean, and
    # is another tenant's token distinguishable from an invented one.
    # ─────────────────────────────────────────────────────────────────────────
    "list_map_history": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        # ROUND 22: the default is {rejected,retired} — NOT every status. `prop`
        # is proposed, so it is listed by the legal call and must VANISH when the
        # argument is omitted. Asserting nothing here let a default of "all" pass.
        Arg(
            "p_status",
            "text[]",
            lambda _w: ["proposed"],
            Null("DEFAULT", lambda out, _w: "prop" not in [i["slug"] for i in out["items"]]),
        ),
        Arg("p_limit", "integer", lambda _w: 5, Null("DEFAULT")),
        Arg("p_offset", "integer", lambda _w: 0, Null("DEFAULT")),
    ],
    "list_page_intents": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            # The disposition and state filters are EXACT-MATCH against a page's
            # intent, and this world has no intent edge at all (the one the round-19
            # readers use is planted later, in _plant_world) — so with their legal
            # values in place the answer is [] whatever p_site_id means, and the
            # probe could never see its own meaning. Clear them for this probe only:
            # NULL disposition and NULL state are "every disposition" and "every
            # state", which is what the door declares.
            Null(
                "MEANS",
                lambda out, w: sorted(i["page"]["id"] for i in out["items"])
                == sorted([w.page, w.page2]),
                # Clear EVERY other filter so this probe sees the whole page set
                # of the sites the caller may view — and so the foreign page,
                # which covers alpha from a site the caller cannot view, is the
                # thing whose absence is being asserted.
                {
                    "p_topic_slug": lambda _w: None,
                    "p_disposition": lambda _w: None,
                    "p_state": lambda _w: None,
                },
            ),
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
        # ROUND 22: these three asserted NOTHING — `Null("MEANS")` with no expect
        # passes on any output that does not raise, so a filter that silently
        # ignored its argument, or one that dropped every row, read as correct.
        # Each now states what its NULL means and is checked against it.
        Arg(
            "p_topic_slug",
            "text",
            # sect-b deliberately: it carries ONE page, so NULL must WIDEN the set
            # to both. With `alpha` (which carries both) the probe could not tell
            # a filter that works from one that is ignored.
            lambda _w: "sect-b",
            # NULL = every topic.
            Null(
                "MEANS",
                lambda out, w: sorted(i["page"]["id"] for i in out["items"])
                == sorted([w.page, w.page2]),
                {"p_disposition": lambda _w: None, "p_state": lambda _w: None},
            ),
            SLUG,
        ),
        Arg(
            "p_disposition",
            "text",
            lambda _w: "keep",
            # NULL = every disposition, INCLUDING a page with no intent at all —
            # the legal value `keep` matches nothing in this world, so this
            # probe fails the moment the filter stops being dropped.
            # The topic filter stays on `sect-b`, which page2 alone covers: NULL
            # here must widen from "pages whose intent says keep" (none) to
            # "every page on sect-b", not to every page in the map.
            Null("MEANS", lambda out, w: [i["page"]["id"] for i in out["items"]] == [w.page2],
                 {"p_state": lambda _w: None}),
        ),
        Arg(
            "p_state",
            "text",
            lambda _w: "proposed",
            Null("MEANS", lambda out, w: [i["page"]["id"] for i in out["items"]] == [w.page2],
                 {"p_disposition": lambda _w: None}),
        ),
        Arg("p_limit", "integer", lambda _w: 5, Null("DEFAULT")),
        Arg("p_offset", "integer", lambda _w: 0, Null("DEFAULT")),
    ],
    "list_topic_gaps": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            # NULL = the sites the caller may view. beta carries a keyword and no
            # page and no planned page, so it is a gap in both readings.
            Null("MEANS", lambda out, _w: "beta" in [i["slug"] for i in out["items"]]),
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
    ],
    "reject_map_topics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_slugs",
            "text[]",
            lambda _w: ["prop"],
            E22,
            Foreign("P0002", lambda _w: "foreign-only", _nope, lambda _w, t: [t]),
        ),
        Arg("p_on_attachments", "text", lambda _w: "error", Null("DEFAULT")),
    ],
    "set_page_intents": [
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            E22,
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
        Arg(
            "p_items",
            "jsonb",
            lambda w: _j([{"page_id": w.page, "topic_slug": "alpha", "disposition": "keep"}]),
            E22,
            Foreign(
                "SAME",
                lambda w: w.foreign["page"],
                _inv,
                lambda _w, t: _j([{"page_id": t, "topic_slug": "alpha", "disposition": "keep"}]),
            ),
        ),
        Arg("p_source", "text", lambda _w: "human", E22),
    ],
    "map_diagnostics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            Null("MEANS", lambda out, w: out["sites_using_map"] == [w.site]),
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
        Arg("p_limit", "integer", lambda _w: 5, Null("DEFAULT")),
    ],
    "map_dry_run": [
        Arg("p_function", "text", lambda _w: "move_map_topic", E22),
        Arg(
            "p_args",
            "jsonb",
            lambda w: _j([w.map, "alpha-kid", "beta"]),
            E22,
            Foreign(
                "42501",
                lambda w: w.foreign["map"],
                _inv,
                lambda _w, tok: _j([tok, "alpha-kid", None]),
            ),
        ),
    ],
    "map_facet_value_ref": [
        Arg(
            "p_value_id",
            "uuid",
            lambda w: w.own_value,
            E22,
            Foreign("42501", lambda w: w.foreign["value"], _inv),
        ),
    ],
    "map_graph": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_group_by",
            "text",
            lambda _w: "region",
            Null(
                "MEANS", lambda out, _w: not any(n["type"] == "facet_value" for n in out["nodes"])
            ),
            Foreign("SAME", lambda _w: "tmdc_foreign_facet", _nope),
        ),
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            Null("MEANS", _alpha_pages),
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
    ],
    "map_outline": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_focus_slug", "text", lambda _w: "alpha", Null("MEANS"), SLUG),
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            Null("MEANS"),
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
        Arg("p_overrides", "jsonb", lambda _w: "{}", Null("DEFAULT")),
    ],
    "map_topic_associations": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_slug", "text", lambda _w: "alpha", E22, SLUG),
        Arg("p_kinds", "text[]", lambda _w: ["pages"], Null("MEANS", _visible_assoc)),
    ],
    "map_topic_facets": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_slug", "text", lambda _w: "beta", E22, SLUG),
    ],
    "map_tree": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_root_slug",
            "text",
            lambda _w: "alpha",
            Null("MEANS", lambda out, _w: out["root"] is None and out["total_topics"] == 7),
            SLUG,
        ),
        Arg("p_depth", "integer", lambda _w: 2, Null("MEANS")),
        Arg("p_include", "text[]", lambda _w: ["associations", "counts"], Null("DEFAULT")),
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            Null("MEANS"),
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
    ],
    "merge_map_topics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_from_slugs",
            "text[]",
            lambda _w: ["beta"],
            E22,
            Foreign("P0002", lambda _w: "foreign-only", _nope, lambda _w, t: [t]),
        ),
        Arg("p_into_slug", "text", lambda _w: "sect", E22, SLUG),
    ],
    "move_map_topic": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_slug", "text", lambda _w: "alpha-kid", E22, SLUG),
        Arg(
            "p_new_parent_slug",
            "text",
            lambda _w: "beta",
            Null(
                "MEANS",
                "select parent_id is null from seo.map_topic where map_id = %(map)s and slug = 'alpha-kid'",
            ),
            SLUG,
        ),
    ],
    "patch_map_topics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_edits",
            "jsonb",
            lambda _w: _j([{"slug": "beta", "name": "Beta two"}]),
            E22,
            Foreign(
                "SAME",
                lambda _w: "foreign-only",
                _nope,
                lambda _w, t: _j([{"slug": t, "name": "x"}]),
            ),
        ),
    ],
    "replace_map_section": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        # NULL = the ROOT level: the legal children would retire alpha (which has
        # coverage) under on_removed 'error' — so the NULL provably meant "root".
        Arg("p_parent_slug", "text", lambda _w: "sect", Null("MEANS", "ERR:23514"), SLUG),
        Arg(
            "p_children",
            "jsonb",
            lambda _w: _j([{"slug": "sect-a", "name": "A"}, {"slug": "sect-b", "name": "B"}]),
            E22,
        ),
        # NULL = the default 'error': dropping sect-b (which has coverage) must refuse.
        Arg(
            "p_on_removed",
            "text",
            lambda _w: "error",
            Null(
                "DEFAULT",
                "ERR:23514",
                {"p_children": lambda _w: _j([{"slug": "sect-a", "name": "A"}])},
            ),
        ),
    ],
    "retire_map_topics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_slugs",
            "text[]",
            lambda _w: ["sect-a"],
            E22,
            Foreign("P0002", lambda _w: "foreign-only", _nope, lambda _w, t: [t]),
        ),
        Arg(
            "p_on_attachments",
            "text",
            lambda _w: "error",
            Null("DEFAULT", "ERR:23514", {"p_slugs": lambda _w: ["sect-b"]}),
        ),
        # NULL = the default true: retiring `sect` lifts sect-a to the root.
        Arg(
            "p_lift_children",
            "boolean",
            lambda _w: True,
            Null(
                "DEFAULT",
                "select parent_id is null from seo.map_topic where map_id = %(map)s and slug = 'sect-a'",
                {"p_slugs": lambda _w: ["sect"]},
            ),
        ),
    ],
    "search_map_topics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg(
            "p_query",
            "text",
            lambda _w: "alph",
            E22,
            Foreign("SAME", lambda _w: "foreign-only", _nope),
        ),
        Arg("p_limit", "integer", lambda _w: 10, Null("DEFAULT")),
    ],
    "set_map_topic_facet": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_slug", "text", lambda _w: "beta", E22, SLUG),
        Arg(
            "p_facet_key",
            "text",
            lambda _w: "region",
            E22,
            Foreign("P0002", lambda _w: "tmdc_foreign_facet", _nope),
        ),
        Arg(
            "p_value_slug",
            "text",
            lambda _w: "tmdc-own",
            Null(
                "MEANS",
                "select not exists (select 1 from platform.associations a where a.source_type = 'seo_map_topic' "
                "and a.source_id = %(beta)s and a.target_type = 'seo_map_facet_value' and a.deleted_at is null)",
            ),
            Foreign("P0002", lambda _w: "tmdc-foreign-val", _nope),
        ),
        # ROUND 24: a facet edge says WHO set it, so a robot can never silently
        # replace a person's value. Required, no default — a default is how a robot
        # writes as a person by forgetting to say who it is.
        Arg("p_source", "text", lambda _w: "human", E22),
    ],
    "set_page_map_facet": [
        Arg(
            "p_page_id",
            "uuid",
            lambda w: w.page,
            E22,
            Foreign("42501", lambda w: w.foreign["page"], _inv),
        ),
        Arg(
            "p_facet_key",
            "text",
            lambda _w: "region",
            E22,
            Foreign("P0002", lambda _w: "tmdc_foreign_facet", _nope),
        ),
        Arg(
            "p_value_slug",
            "text",
            lambda _w: "tmdc-own",
            Null(
                "MEANS",
                "select not exists (select 1 from platform.associations a where a.source_type = 'web_page' "
                "and a.source_id = %(page)s and a.target_type = 'seo_map_facet_value' and a.deleted_at is null)",
            ),
            Foreign("P0002", lambda _w: "tmdc-foreign-val", _nope),
        ),
        # ROUND 24 — see the note on set_map_topic_facet above.
        Arg("p_source", "text", lambda _w: "human", E22),
    ],
    "set_page_map_topics": [
        Arg(
            "p_page_id",
            "uuid",
            lambda w: w.page,
            E22,
            Foreign("42501", lambda w: w.foreign["page"], _inv),
        ),
        Arg(
            "p_topics",
            "jsonb",
            lambda _w: _j([{"slug": "alpha"}]),
            E22,
            Foreign("SAME", lambda _w: "foreign-only", _nope, lambda _w, t: _j([{"slug": t}])),
        ),
        Arg("p_source", "text", lambda _w: "agent", E22),
    ],
    "set_pages_map_topics": [
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            E22,
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
        Arg(
            "p_items",
            "jsonb",
            lambda w: _j([{"page_id": w.page, "topics": [{"slug": "alpha"}]}]),
            E22,
            Foreign(
                "SAME",
                lambda w: w.foreign["page"],
                _inv,
                lambda _w, t: _j([{"page_id": t, "topics": []}]),
            ),
        ),
        Arg("p_source", "text", lambda _w: "agent", E22),
    ],
    "set_site_map": [
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            E22,
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
    ],
    "site_map_id": [
        Arg(
            "p_site_id",
            "uuid",
            lambda w: w.site,
            E22,
            Foreign("42501", lambda w: w.foreign["site"], _inv),
        ),
    ],
    "split_map_topic": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_slug", "text", lambda _w: "beta", E22, SLUG),
        Arg("p_children", "jsonb", lambda _w: _j([{"slug": "beta-a", "name": "Beta A"}]), E22),
    ],
    "upsert_map_topics": [
        Arg("p_map_id", "uuid", lambda w: w.map, E22, MAP()),
        Arg("p_tree", "jsonb", lambda _w: _j([{"slug": "gamma", "name": "Gamma"}]), E22),
    ],
}


# ─────────────────────────────────────────────────────────────────────────────
# The runner
# ─────────────────────────────────────────────────────────────────────────────


@dataclass
class Outcome:
    ok: bool
    text: str  # the result as text, or the error message
    code: str | None = None
    effect: Any = None
    state: str | None = None

    def decoded(self) -> Any:
        try:
            return json.loads(self.text)
        except (TypeError, ValueError):
            return self.text


STATE_SQL = """
select md5(jsonb_build_object(
  'topics', (select jsonb_agg(jsonb_build_array(t.slug, t.status, t.name, p.slug) order by t.slug)
               from seo.map_topic t left join seo.map_topic p on p.id = t.parent_id
              where t.map_id = %(map)s and t.deleted_at is null),
  'edges',  (select jsonb_agg(jsonb_build_array(a.source_type, a.source_id, a.target_type, a.target_id, a.role, a.payload) order by a.id)
               from platform.associations a
              where a.deleted_at is null
                and (a.source_id = any(%(watched)s::uuid[]) or a.target_id = any(%(watched)s::uuid[]))),
  'values', (select jsonb_agg(jsonb_build_array(v.slug, v.name, v.ref_id) order by v.slug)
               from seo.map_facet_value v where v.brand_id = %(brand)s and v.deleted_at is null)
)::text)
"""


def _params(w: World) -> dict[str, Any]:
    watched = [w.map, w.site, w.page, w.page2, *w.topics.values()]
    return {**w.me, **w.topics, "watched": watched}


def _run(
    cur: Any,
    w: World,
    fn: str,
    args: list[Arg],
    values: dict[str, Any],
    effect_sql: str | None = None,
) -> Outcome:
    sql = "select seo.{}({})::text".format(fn, ", ".join(f"%s::{a.type}" for a in args))
    params = _params(w)
    cur.execute("savepoint probe")
    try:
        try:
            cur.execute("set local role authenticated")
            _claims(cur, w.me["user"])
            cur.execute(sql, [values[a.name] for a in args])
            text = cur.fetchone()[0]
        except psycopg.Error as exc:
            cur.execute("rollback to savepoint probe")
            return Outcome(False, exc.diag.message_primary or str(exc), exc.sqlstate)
        cur.execute("reset role")
        effect = _one(cur, effect_sql, params) if effect_sql else None
        state = _one(cur, STATE_SQL, params)
        cur.execute("rollback to savepoint probe")
        return Outcome(True, text if text is not None else "null", None, effect, state)
    finally:
        cur.execute("reset role")


def _baseline_state(cur: Any, w: World) -> str:
    return _one(cur, STATE_SQL, _params(w))


def _scrub(text: str, *tokens: str) -> str:
    for tok in tokens:
        if tok:
            text = text.replace(tok, "<TOKEN>")
    return text


def _leaks(text: str, w: World, allowed: tuple[str, ...] = ()) -> list[str]:
    found = [MARKER] if MARKER in text else []
    return found + [i for i in w.foreign_ids if i in text and i not in allowed]


def _legal(w: World, args: list[Arg]) -> dict[str, Any]:
    return {a.name: a.legal(w) for a in args}


# ─────────────────────────────────────────────────────────────────────────────
# The tests
# ─────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("fn", sorted(DOORS))
def test_door_null_and_foreign_contract(db: tuple[Any, World], fn: str) -> None:
    cur, w = db
    args = DOORS[fn]
    failures: list[str] = []
    before = _baseline_state(cur, w)

    legal = _run(cur, w, fn, args, _legal(w, args))
    if not legal.ok:
        failures.append(f"legal call failed: {legal.code} {legal.text}")
    elif leaks := _leaks(legal.text, w):
        failures.append(f"legal call output leaks {leaks}")

    for arg in args:
        values = (
            _legal(w, args) | {k: f(w) for k, f in arg.null.override.items()} | {arg.name: None}
        )
        effect_sql = (
            arg.null.expect
            if isinstance(arg.null.expect, str) and not arg.null.expect.startswith("ERR:")
            else None
        )
        out = _run(cur, w, fn, args, values, effect_sql)
        where = f"{arg.name}=NULL"
        if leaks := _leaks(out.text, w):
            failures.append(f"{where}: output leaks {leaks}")
        if arg.null.kind == "22023":
            if out.ok:
                changed = " AND CHANGED STATE (destructive)" if out.state != before else ""
                failures.append(f"{where}: declared 22023 but succeeded{changed}: {out.text[:160]}")
            elif out.code != "22023" or arg.name not in out.text:
                failures.append(
                    f"{where}: declared 22023 naming {arg.name}, got {out.code} {out.text!r}"
                )
            continue
        expect = arg.null.expect
        if isinstance(expect, str) and expect.startswith("ERR:"):
            if out.ok or out.code != expect[4:]:
                failures.append(
                    f"{where}: declared {arg.null.kind}, expected {expect}, got {out.code} {out.text[:160]!r}"
                )
        elif not out.ok:
            failures.append(
                f"{where}: declared {arg.null.kind}, but raised {out.code} {out.text!r}"
            )
        elif isinstance(expect, str) and out.effect is not True:
            failures.append(f"{where}: declared {arg.null.kind}, effect not observed ({expect})")
        elif callable(expect) and not expect(out.decoded(), w):
            failures.append(
                f"{where}: declared {arg.null.kind}, output does not show it: {out.text[:400]}"
            )

    for arg in args:
        probe = arg.foreign
        if probe is None:
            continue
        tok_f, tok_i = probe.foreign(w), probe.invented(w)
        f_out = _run(cur, w, fn, args, _legal(w, args) | {arg.name: probe.build(w, tok_f)})
        i_out = _run(cur, w, fn, args, _legal(w, args) | {arg.name: probe.build(w, tok_i)})
        where = f"{arg.name}=foreign"
        if leaks := _leaks(f_out.text, w, allowed=(tok_f,)):
            failures.append(f"{where}: output leaks {leaks}")
        same = (f_out.ok, f_out.code, _scrub(f_out.text, tok_f)) == (
            i_out.ok,
            i_out.code,
            _scrub(i_out.text, tok_i),
        )
        if not same:
            failures.append(
                f"{where}: foreign and invented differ (oracle): "
                f"foreign={f_out.code} {_scrub(f_out.text, tok_f)[:200]!r} / invented={i_out.code} {_scrub(i_out.text, tok_i)[:200]!r}"
            )
        elif probe.code != "SAME" and (f_out.ok or f_out.code != probe.code):
            failures.append(
                f"{where}: expected {probe.code} for both, got {f_out.code} {f_out.text[:160]!r}"
            )

    assert _baseline_state(cur, w) == before, "probes leaked state out of their savepoints"
    assert not failures, f"seo.{fn} breaks its door contract:\n  " + "\n  ".join(failures)


_RULES = re.compile(r"NULL RULES: (?P<null>.*?) \| FOREIGN: (?P<foreign>.*?)(?: \||$)", re.S)


def _parse_rules(block: str) -> dict[str, str]:
    rules: dict[str, str] = {}
    for part in block.split(";"):
        name, _, rule = part.strip().partition("=")
        rules[name.strip()] = rule.strip()
    return rules


def test_door_rows_declare_what_the_table_enforces(db: tuple[Any, World]) -> None:
    cur, _w = db
    cur.execute(
        "select function_name, identity_args, reason from platform.client_callable_door "
        "where schema_name = 'seo' and function_name = any(%s)",
        (sorted(DOORS),),
    )
    rows = {r[0]: (r[1], r[2]) for r in cur.fetchall()}
    failures: list[str] = []
    assert sorted(rows) == sorted(DOORS), f"door rows missing: {sorted(set(DOORS) - set(rows))}"
    for fn, args in sorted(DOORS.items()):
        identity, reason = rows[fn]
        declared_names = [a.strip().split(" ")[0] for a in identity.split(",")]
        if declared_names != [a.name for a in args]:
            failures.append(
                f"{fn}: identity_args {declared_names} != table {[a.name for a in args]}"
            )
        m = _RULES.search(reason or "")
        if not m:
            failures.append(f"{fn}: reason carries no 'NULL RULES: … | FOREIGN: …' declaration")
            continue
        nulls, foreigns = _parse_rules(m["null"]), _parse_rules(m["foreign"])
        for a in args:
            if a.name not in (reason or ""):
                failures.append(f"{fn}: reason never names {a.name}")
            declared = nulls.get(a.name, "<absent>")
            head = declared.split(" ")[0]
            if head != a.null.kind:
                failures.append(
                    f"{fn}.{a.name}: door says NULL -> {declared!r}, table enforces {a.null.kind}"
                )
            f_declared = foreigns.get(a.name, "<absent>")
            f_expected = a.foreign.code if a.foreign else "NONE"
            if f_declared != f_expected:
                failures.append(
                    f"{fn}.{a.name}: door says FOREIGN -> {f_declared!r}, table enforces {f_expected}"
                )
    assert not failures, "door declarations disagree with the contract:\n  " + "\n  ".join(failures)


# ─────────────────────────────────────────────────────────────────────────────
# ROUND 18 — NO HIDDEN COUNTS. Every reader's output is BLIND to rows the caller
# cannot open: not listed, not counted, not hinted at. The proof is byte
# equality — the same call, in a world with those rows and in a world without
# them, returns the same bytes.
#
# Two kinds of unopenable row are planted, because they fail differently:
#   * ANOTHER TENANT'S (a foreign page covering our topic) — a stranger controls
#     it, so a count of it is a signal a stranger can raise;
#   * OUR OWN ORGANISATION'S, unviewable by THIS caller (a site created inside
#     the txn that neither caller has viewer on, its page, and a keyword row on
#     it) — the keyword-site rule and the resolver rule both run here.
# Both are read by two callers: the map's owner, and a viewer-shared non-owner
# (viewer on the map and on our site, member of no organisation).
# ─────────────────────────────────────────────────────────────────────────────

SAMEORG_MARKER = "SAMEORG-SECRET-REASON"


@dataclass
class Hidden:
    viewer: str  # a second signed-in user: viewer on the map and on OUR site, member of nothing
    brand: str  # same org, created by the server lane: neither caller may view it
    site: str
    page: str
    keyword_visible: str  # public keyword, filed on OUR site -> always listed
    keyword_hidden: str  # public keyword, filed on the unviewable site -> must vanish
    foreign_edges: list[str]  # the base world's foreign plants, removable for the clean state

    @property
    def ids(self) -> list[str]:
        return [self.brand, self.site, self.page, self.keyword_hidden]


def _srv(cur: Any, sql: str, args: tuple | None = None) -> Any:
    """A server-lane write (no signed-in identity), the way a DB-side job writes."""
    _claims(cur, None)
    cur.execute(sql, args)
    return cur.fetchone()[0] if cur.description else None


def _as(cur: Any, user: str, sql: str, args: tuple | None = None) -> str:
    """One call as a signed-in user, ALWAYS rolled back: readers and writers alike."""
    cur.execute("savepoint r18call")
    try:
        cur.execute("set local role authenticated")
        _claims(cur, user)
        cur.execute(sql, args)
        out = cur.fetchone()[0]
        return "null" if out is None else str(out)
    except psycopg.Error as exc:
        return f"ERR {exc.sqlstate} {exc.diag.message_primary}"
    finally:
        cur.execute("rollback to savepoint r18call")
        cur.execute("reset role")
        _claims(cur, None)


def _plant_world(cur: Any, w: World) -> Hidden:
    tag = uuid.uuid4().hex[:8]
    brand = str(
        _srv(
            cur,
            "insert into web.brand (organization_id, name) values (%s, %s) returning id",
            (w.me["org"], f"TMDC hidden brand {tag}"),
        )
    )
    host = f"tmdc-hidden-{tag}.invalid"
    site = str(
        _srv(
            cur,
            "insert into web.site (organization_id,name,root_url,domain,brand_id) values (%s,%s,%s,%s,%s) returning id",
            (w.me["org"], f"TMDC hidden site {tag}", f"https://{host}", host, brand),
        )
    )
    page = str(uuid.uuid4())
    _srv(
        cur,
        "insert into web.page (id,organization_id,site_id,url,url_hash,provenance,canonical_page_id) "
        "values (%s,%s,%s,%s,md5(%s),'manual',%s)",
        (page, w.me["org"], site, f"https://{host}/h", f"https://{host}/h", page),
    )
    viewer = str(uuid.uuid4())
    _srv(
        cur,
        "insert into auth.users (id, email, aud, role, instance_id, raw_app_meta_data) values "  # matrx-fixture:rollback-only rolled back in finally
        "(%s,%s,'authenticated','authenticated','00000000-0000-0000-0000-000000000000', jsonb_build_object('test_fixture', jsonb_build_object('suite', 'rolled-back-suite', 'purpose', 'account inside a rolled-back transaction', 'expires_at', '2026-10-01T00:00:00Z')))",
        (viewer, f"tm-door-contract-viewer-{viewer}@example.invalid"),  # matrx-fixture:rollback-only rolled back in finally
    )
    _srv(
        cur,
        "insert into iam.permissions (resource_type, resource_id, granted_to_user_id, permission_level, created_by, status) "
        "values ('seo_topical_map',%s,%s,'viewer',%s,'active'),('web_site',%s,%s,'viewer',%s,'active')",
        (w.map, viewer, w.me["user"], w.site, viewer, w.me["user"]),
    )
    # PUBLIC keywords: the resolver lets anyone signed in open them, so a keyword
    # edge can only be hidden by the SITE its row names — which is the rule under test.
    kw_vis, kw_hid = (
        str(
            _srv(
                cur,
                "insert into seo.keyword (organization_id, phrase, normalized_phrase, language, published_to_web, published_to_web_at) "
                "values (%s,%s,%s,'en',true,now()) returning id",
                (w.me["org"], f"tmdc {label} {tag}", f"tmdc {label} {tag}"),
            )
        )
        for label in ("visible", "hidden")
    )
    _srv(
        cur,
        "insert into seo.site_keyword_value (organization_id, site_id, keyword_id, topic_id, workflow_status) "
        "values (%s,%s,%s,%s,'candidate')",
        (w.me["org"], w.site, kw_vis, w.topics["beta"]),
    )
    # ROUND 19: OUR OWN intent, so `intents` below is never a vacuous pass — the
    # clean world must SHOW an intent before its absence can prove anything.
    _srv(
        cur,
        "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
        "values ('web_page',%s,'seo_map_topic',%s,%s,'intent','map_page_intent',%s::jsonb) returning id",
        (
            w.me["page"],
            w.topics["alpha"],
            w.me["org"],
            json.dumps({"disposition": "keep", "state": "proposed", "source": "mapper"}),
        ),
    )
    foreign_edges = [
        i
        for i in w.foreign_ids
        if _srv(cur, "select exists (select 1 from platform.associations a where a.id = %s)", (i,))
    ]
    return Hidden(viewer, brand, site, page, kw_vis, kw_hid, foreign_edges)


def _apply_state(cur: Any, w: World, h: Hidden, foreign: bool, same_org: bool) -> None:
    """Seed (or unseed) the unopenable rows. Server lane: no client write rules involved."""
    if not foreign:
        _srv(cur, "delete from platform.associations where id = any(%s::uuid[])", (h.foreign_edges,))
    else:
        _srv(
            cur,
            "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
            "values ('web_page',%s,'seo_map_topic',%s,%s,'covers','map_topic_coverage',%s::jsonb) returning id",
            (
                w.foreign["page2"],
                w.topics["sect-b"],
                w.foreign["org"],
                json.dumps({"confidence": 91, "source": "human", "reason": MARKER}),
            ),
        )
        # ROUND 19: another tenant's page declaring where it is going, on OUR
        # topic. seo.list_page_intents must read identically without it.
        _srv(
            cur,
            "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
            "values ('web_page',%s,'seo_map_topic',%s,%s,'intent','map_page_intent',%s::jsonb) returning id",
            (
                w.foreign["page"],
                w.topics["alpha"],
                w.foreign["org"],
                json.dumps({"disposition": "redirect", "into_page_id": w.foreign["page2"],
                            "state": "proposed", "source": "human", "note": MARKER}),
            ),
        )
    if same_org:
        for slug in ("alpha", "sect-b"):
            _srv(
                cur,
                "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
                "values ('web_page',%s,'seo_map_topic',%s,%s,'covers','map_topic_coverage',%s::jsonb) returning id",
                (
                    h.page,
                    w.topics[slug],
                    w.me["org"],
                    json.dumps({"confidence": 77, "source": "agent", "reason": SAMEORG_MARKER}),
                ),
            )
        _srv(
            cur,
            "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role) "
            "values ('web_site',%s,'seo_topical_map',%s,%s,'uses') returning id",
            (h.site, w.map, w.me["org"]),
        )
        _srv(
            cur,
            "insert into seo.site_keyword_value (organization_id, site_id, keyword_id, topic_id, workflow_status) "
            "values (%s,%s,%s,%s,'candidate') returning id",
            (w.me["org"], h.site, h.keyword_hidden, w.topics["beta"]),
        )
        _srv(
            cur,
            "insert into plan.node (site_id, node_type, slug, label, organization_id, topic_id) "
            "values (%s,'article','tmdc-hidden-plan','TMDC hidden plan',%s,%s) returning id",
            (h.site, w.me["org"], w.topics["beta"]),
        )
    # The facet value's ref: a row the caller cannot open, or (clean) no ref at all.
    ref = w.foreign["site"] if foreign else (h.site if same_org else None)
    _srv(
        cur,
        "update seo.map_facet_value set ref_type = %s, ref_id = %s where id = %s returning id",
        ("web_site" if ref else None, ref, w.own_value),
    )


def _readers(w: World) -> list[tuple[str, str, tuple]]:
    m = w.map
    return [
        ("assoc:alpha", "select seo.map_topic_associations(%s,'alpha',NULL)::text", (m,)),
        ("assoc:beta", "select seo.map_topic_associations(%s,'beta',NULL)::text", (m,)),
        ("assoc:sect-b", "select seo.map_topic_associations(%s,'sect-b',NULL)::text", (m,)),
        ("facets:beta", "select seo.map_topic_facets(%s,'beta')::text", (m,)),
        ("facet_value_ref", "select seo.map_facet_value_ref(%s)::text", (w.own_value,)),
        (
            "tree",
            "select seo.map_tree(%s,NULL,NULL,'{associations,counts,facets,path,status,description}'::text[],NULL)::text",
            (m,),
        ),
        ("graph", "select seo.map_graph(%s,'region',NULL)::text", (m,)),
        ("outline", "select seo.map_outline(%s,NULL,NULL,'{}'::jsonb)", (m,)),
        ("outline:alpha", "select seo.map_outline(%s,'alpha',NULL,'{}'::jsonb)", (m,)),
        ("diagnostics", "select seo.map_diagnostics(%s,NULL,25)::text", (m,)),
        ("search", "select seo.search_map_topics(%s,'',25)::text", (m,)),
        # ROUND 19 (3): the page-intent surface. `intents` is the one that can
        # leak the most — it renders another tenant's page, its intent payload
        # and its redirect destination if it renders anything it should not.
        ("intents", "select seo.list_page_intents(%s,NULL,NULL,NULL,NULL,200,0)::text", (m,)),
        ("gaps", "select seo.list_topic_gaps(%s,NULL)::text", (m,)),
        (
            "history",
            "select seo.list_map_history(%s,'{proposed,rejected,retired}'::text[],200,0)::text",
            (m,),
        ),
        # ROUND 19 (1): seo.v_map_topic_stats read DIRECTLY as the signed-in user
        # (security_invoker view, no definer counting) — the RLS on the base
        # tables (platform.associations, web.page) is the only thing standing
        # between a stranger's coverage and this number.
        (
            "stats",
            "select coalesce(jsonb_agg(row_to_json(v)::jsonb order by v.topic_id, v.site_id), '[]'::jsonb)::text "
            "from seo.v_map_topic_stats v where v.map_id = %s",
            (m,),
        ),
        # ROUND 19 (2): the 23514 attachment-rule refusal of retire_map_topics and
        # replace_map_section reports attachment COUNTS in its message. Those
        # counts are scoped by seo._tm_attachments to the topic's OWN organisation
        # (definer, no RLS) — a deliberate exception, because the retire gate must
        # see attachments the caller cannot individually open. Only a FOREIGN
        # organisation's attachment must never move this number; see
        # OWN_ORG_VISIBLE_READERS below for how that is checked.
        (
            "retire:sect-b",
            "select seo.retire_map_topics(%s, ARRAY['sect-b']::text[], 'error', true)::text",
            (m,),
        ),
        (
            "replace:sect",
            "select seo.replace_map_section(%s, 'sect', %s::jsonb, 'error')::text",
            (m, _j([{"slug": "sect-a", "name": "A"}])),
        ),
    ]


# These readers report counts scoped to the CALLER'S OWN organisation on purpose
# (seo._tm_attachments runs SECURITY DEFINER and is not RLS-filtered) — the retire
# gate must see every attachment in its own org, even one the caller individually
# cannot open. So "+same-org" and "+both" are exempt from the blind-equality check
# below; what must still hold is that a FOREIGN organisation's row never moves them:
# "+foreign" must read exactly like "clean", and "+both" exactly like "+same-org".
OWN_ORG_VISIBLE_READERS = {"retire:sect-b", "replace:sect"}

STATES = {"clean": (False, False), "+foreign": (True, False), "+same-org": (False, True), "+both": (True, True)}


@pytest.mark.parametrize("caller", ["owner", "viewer-shared non-owner"])
def test_readers_are_blind_to_rows_the_caller_cannot_open(
    db: tuple[Any, World], caller: str
) -> None:
    cur, w = db
    cur.execute("savepoint r18")
    try:
        h = _plant_world(cur, w)
        user = w.me["user"] if caller == "owner" else h.viewer

        # NEVER A VACUOUS PASS (1): the planted rows really are unopenable by this
        # caller, and the rows we expect to SEE really are openable.
        access = json.loads(
            _as(
                cur,
                user,
                "select jsonb_build_object('map', iam.has_access('seo_topical_map',%s,'viewer'),"
                "'our_site', iam.has_access('web_site',%s,'viewer'),"
                "'hidden_site', iam.has_access('web_site',%s,'viewer'),"
                "'hidden_page', iam.has_access('web_page',%s,'viewer'),"
                "'foreign_site', iam.has_access('web_site',%s,'viewer'))::text",
                (w.map, w.site, h.site, h.page, w.foreign["site"]),
            )
        )
        assert access == {
            "map": True,
            "our_site": True,
            "hidden_site": False,
            "hidden_page": False,
            "foreign_site": False,
        }, f"{caller}: the probe world is not what the test assumes: {access}"

        states: dict[str, dict[str, str]] = {}
        for name, (foreign, same_org) in STATES.items():
            cur.execute("savepoint r18state")
            _apply_state(cur, w, h, foreign, same_org)
            out = {n: _as(cur, user, sql, args) for n, sql, args in _readers(w)}
            if caller == "owner" and not same_org:
                # A WRITER's report is a reader too: merging must not count another
                # organisation's attachments back to the editor.
                out["merge:alpha->beta"] = _as(
                    cur, user, "select seo.merge_map_topics(%s,'{alpha}'::text[],'beta')::text", (w.map,)
                )
            states[name] = out
            cur.execute("rollback to savepoint r18state")

        base = states["clean"]
        # NEVER A VACUOUS PASS (2): in the clean world this caller DOES see their own
        # rows through the very readers under test.
        alpha = json.loads(base["assoc:alpha"])
        # ROUND 19: a page reaches a topic by TWO roles now — `covers` (where it sits
        # today) and `intent` (where it is going) — so w.page legitimately appears
        # twice on alpha. Name the role, or this counts one page as two.
        assert sorted(
            a["item"]["id"]
            for a in alpha
            if a["item"]["type"] == "web_page" and a["association"].get("role") == "covers"
        ) == sorted([w.page, w.page2]), (
            f"{caller}: clean world shows no own pages covering alpha: {base['assoc:alpha'][:400]}"
        )
        assert [
            a["item"]["id"]
            for a in alpha
            if a["item"]["type"] == "web_page" and a["association"].get("role") == "intent"
        ] == [w.page], (
            f"{caller}: clean world shows no own INTENT edge on alpha, so hiding a foreign "
            f"one through this reader would prove nothing: {base['assoc:alpha'][:400]}"
        )
        beta_kinds = [a["item"].get("id") for a in json.loads(base["assoc:beta"])]
        assert h.keyword_visible in beta_kinds, (
            f"{caller}: clean world shows no keyword edge on beta (the keyword-site rule would be "
            f"untested): {base['assoc:beta'][:400]}"
        )
        intents = json.loads(base["intents"])
        assert sorted(i["page"]["id"] for i in intents["items"]) == sorted([w.page, w.page2]), (
            f"{caller}: clean world shows the wrong page set through list_page_intents: {base['intents'][:400]}"
        )
        assert any(
            i["page"]["id"] == w.page and (i.get("intent") or {}).get("disposition") == "keep"
            for i in intents["items"]
        ), f"{caller}: clean world shows no intent at all, so hiding one proves nothing: {base['intents'][:400]}"
        assert "beta" in [g["slug"] for g in json.loads(base["gaps"])["items"]], (
            f"{caller}: clean world reports no gap, so a hidden planned page could not move it: {base['gaps'][:400]}"
        )
        assert "prop" in [h["slug"] for h in json.loads(base["history"])["items"]], (
            f"{caller}: clean world's history is empty, so it proves nothing: {base['history'][:400]}"
        )
        cur.execute("savepoint r18ref")
        _srv(cur, "update seo.map_facet_value set ref_type='web_site', ref_id=%s where id=%s", (w.site, w.own_value))
        visible_ref = _as(cur, user, "select seo.map_facet_value_ref(%s)::text", (w.own_value,))
        cur.execute("rollback to savepoint r18ref")
        assert w.site in visible_ref, (
            f"{caller}: a ref the caller CAN open is not rendered, so a NULL ref proves nothing: {visible_ref}"
        )
        # v_map_topic_stats is security_invoker: unlike the SECURITY DEFINER doors
        # above, "pages" here is gated by platform.associations' own org-membership
        # RLS, which this disposable world never grants — so page_count is 0 for
        # everyone, everywhere, and proves nothing. site_keyword_value's RLS is
        # site-permission-based instead, so the visible keyword on beta IS the
        # forcing function: it must show up here exactly as it does everywhere else.
        stats = json.loads(base["stats"])
        assert any(
            r["topic_id"] == w.topics["beta"] and r["site_id"] == w.site and r["keyword_count"] == 1 for r in stats
        ), f"{caller}: clean world shows no own keyword_count on beta via v_map_topic_stats: {base['stats'][:400]}"
        if caller == "owner":
            # NEVER A VACUOUS PASS (3): the attachment rule really is what refuses
            # these two calls in the clean world — an editor, with attachments
            # present. A different refusal (e.g. access) would make the "moved by
            # a foreign row" check below pass on two calls that never reached the
            # counting code at all.
            assert base["retire:sect-b"].startswith("ERR 23514"), (
                f"clean world doesn't hit retire_map_topics' attachment rule: {base['retire:sect-b'][:300]}"
            )
            assert base["replace:sect"].startswith("ERR 23514"), (
                f"clean world doesn't hit replace_map_section's attachment rule: {base['replace:sect'][:300]}"
            )

        failures: list[str] = []
        for name, out in states.items():
            for reader, text in out.items():
                if SAMEORG_MARKER in text or MARKER in text:
                    failures.append(f"{name}/{reader}: leaks a payload written by someone else")
                for i in h.ids + w.foreign_ids:
                    if i in text:
                        failures.append(f"{name}/{reader}: leaks the id of a row the caller cannot open ({i})")
                if reader in OWN_ORG_VISIBLE_READERS:
                    # own-organisation attachments are meant to move this reader
                    # (the retire gate needs them); only a FOREIGN one must not.
                    expected = base[reader] if name in ("clean", "+foreign") else states["+same-org"][reader]
                    if text != expected:
                        failures.append(
                            f"{name}/{reader}: a foreign-organisation row moved this own-org-scoped count\n"
                            f"      expected: {expected[:300]}\n"
                            f"      got:      {text[:300]}"
                        )
                elif name != "clean" and text != base[reader]:
                    failures.append(
                        f"{name}/{reader}: output differs from the world WITHOUT those rows\n"
                        f"      without: {base[reader][:300]}\n"
                        f"      with:    {text[:300]}"
                    )
        assert not failures, (
            f"seo readers are not blind to what {caller} cannot open:\n  " + "\n  ".join(failures)
        )
    finally:
        _claims(cur, None)
        cur.execute("rollback to savepoint r18")


# ═════════════════════════════════════════════════════════════════════════════
# ROUND 22 — THE TWO CLASSES THE SUITE WAS BLIND TO.
#
# The round-7 verifier planted two defects and this file stayed GREEN through
# both, which means it was not testing them at all:
#   (B) the dedupe removed from seo._tm_page_perf — nothing here ever planted a
#       seo.search_performance_daily row or asserted a click total, so the
#       traffic numbers were never checked against anything;
#   (C) `rejected` dropped from seo._tm_topics' exclusion — the world never HELD
#       a rejected topic, because every door probe rolls back to `savepoint
#       probe` the moment it finishes.
# Both now have a test that plants the state and asserts the number.
#
# Run one of them against a planted defect with:
#   MATRX_PLANT_DEFECT=dedupe|rejected uv run pytest packages/matrx-seo/tests/...
# which replaces the live body INSIDE the test transaction (and rolls it back),
# so the proof that a test can fail is a command, not a claim.
# ═════════════════════════════════════════════════════════════════════════════

PLANTED_DEFECTS = {
    # The dedupe gone: every re-ingestion of the same day is summed again.
    "dedupe": """
CREATE OR REPLACE FUNCTION seo._tm_page_perf(p_page_ids uuid[], p_days integer)
 RETURNS jsonb LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'pg_catalog' AS $f$
  SELECT COALESCE(jsonb_object_agg(a.page_id, jsonb_build_object('clicks', a.clicks, 'impressions', a.impressions)), '{}'::jsonb)
    FROM (SELECT d.page_id, sum(d.clicks)::bigint AS clicks, sum(d.impressions)::bigint AS impressions
            FROM seo.search_performance_daily d
           WHERE d.page_id = ANY(p_page_ids)
             AND d.date >= (CURRENT_DATE - (GREATEST(1, COALESCE(p_days, 28)) - 1))
           GROUP BY d.page_id) a;
$f$;""",
    # `rejected` dropped from the tree loader's exclusion: every reader shows it.
    "rejected": """
CREATE OR REPLACE FUNCTION seo._tm_topics(p_map_id uuid, p_site_id uuid)
 RETURNS jsonb LANGUAGE sql STABLE SECURITY DEFINER SET search_path TO 'pg_catalog' AS $f$
  WITH RECURSIVE vis AS (
    SELECT CASE WHEN p_site_id IS NULL THEN seo._tm_visible_sites(p_map_id, NULL) ELSE ARRAY[p_site_id] END AS sites
  ), tr AS (
    SELECT t.id, t.parent_id, t.slug, t.name, t.description, t.status, t.sort_order, 0 AS depth,
           ARRAY[t.id] AS path, ARRAY[lpad(t.sort_order::text,8,'0')||' '||t.slug] AS spath, t.layout
      FROM seo.map_topic t
     WHERE t.map_id = p_map_id AND t.parent_id IS NULL AND t.deleted_at IS NULL
       AND t.status NOT IN ('retired')
    UNION ALL
    SELECT t.id, t.parent_id, t.slug, t.name, t.description, t.status, t.sort_order, tr.depth+1,
           tr.path||t.id, tr.spath||(lpad(t.sort_order::text,8,'0')||' '||t.slug), t.layout
      FROM seo.map_topic t JOIN tr ON t.parent_id = tr.id
     WHERE t.deleted_at IS NULL AND t.status NOT IN ('retired') AND tr.depth < 200
  )
  SELECT COALESCE(jsonb_agg(to_jsonb(x) ORDER BY x.spath), '[]'::jsonb)
    FROM (SELECT tr.id, tr.parent_id, tr.slug, tr.name, tr.description, tr.status, tr.sort_order, tr.depth,
                 tr.path, tr.spath, tr.layout,
                 COALESCE(s.page_count,0) AS page_count, COALESCE(s.planned_count,0) AS planned_count,
                 COALESCE(s.keyword_count,0) AS keyword_count
            FROM tr LEFT JOIN LATERAL (
              SELECT sum(v.page_count)::int AS page_count, sum(v.planned_count)::int AS planned_count,
                     sum(v.keyword_count)::int AS keyword_count
                FROM seo.v_map_topic_stats v, vis
               WHERE v.topic_id = tr.id
                 AND (v.site_id = ANY(vis.sites) OR (p_site_id IS NULL AND v.site_id IS NULL))) s ON true) x;
$f$;""",
}


def _plant_defect_if_asked(cur: Any) -> str | None:
    name = os.environ.get("MATRX_PLANT_DEFECT")
    if not name:
        return None
    if name not in PLANTED_DEFECTS:
        raise AssertionError(
            f"MATRX_PLANT_DEFECT={name!r} is not one of {sorted(PLANTED_DEFECTS)}"
        )
    _claims(cur, None)
    cur.execute(PLANTED_DEFECTS[name])
    return name


def _page(cur: Any, w: World, tag: str) -> str:
    """A third page on OUR site, made by the server lane."""
    pid = str(uuid.uuid4())
    cur.execute("select domain from web.site where id = %s", (w.site,))
    host = cur.fetchone()[0]
    url = f"https://{host}/{tag}"
    _srv(
        cur,
        "insert into web.page (id,organization_id,site_id,url,url_hash,provenance,canonical_page_id) "
        "values (%s,%s,%s,%s,md5(%s),'manual',%s)",
        (pid, w.me["org"], w.site, url, url, pid),
    )
    return pid


def test_traffic_is_deduplicated_windowed_and_knob_driven(db: tuple[Any, World]) -> None:
    """The click totals beside a page are CHECKED, not merely present.

    Every collection run re-ingests the same day, so the same (page, provider,
    date) exists four or five times, each row carrying that whole day's clicks.
    A plain SUM reports about five times the real traffic — on the one screen
    whose job is finding pages with NO traffic. This plants exactly that shape
    and asserts the arithmetic, in both places the number surfaces.
    """
    cur, w = db
    cur.execute("savepoint r22perf")
    try:
        planted = _plant_defect_if_asked(cur)
        page = _page(cur, w, "traffic")
        _srv(
            cur,
            "insert into platform.associations (source_type,source_id,target_type,target_id,organization_id,role,payload_kind,payload) "
            "values ('web_page',%s,'seo_map_topic',%s,%s,'covers','map_topic_coverage',%s::jsonb)",
            (page, w.topics["beta"], w.me["org"], json.dumps({"confidence": 80, "source": "agent", "reason": "t"})),
        )
        run = _srv(
            cur,
            "insert into seo.collection_run (organization_id, created_by, provider, capability, operation, "
            "target_ref, observation_period, settings_hash, idempotency_key) "
            "values (%s,%s,'gsc','search_performance','fetch',%s,'daily',%s,%s) returning id",
            (w.me["org"], w.me["user"], w.site, uuid.uuid4().hex, uuid.uuid4().hex),
        )

        def obs(provider: str, profile: str, day_offset: int, clicks: int, impressions: int, seq: int) -> None:
            _srv(
                cur,
                "insert into seo.search_performance_daily "
                "(organization_id, created_by, run_id, provider, dedup_key, site_id, page_id, date, "
                " dimension_profile, clicks, impressions, created_at) "
                "values (%s,%s,%s,%s,%s,%s,%s, current_date - %s, %s,%s,%s, now() + (%s || ' seconds')::interval) "
                "returning id",
                (w.me["org"], w.me["user"], run, provider, uuid.uuid4().hex, w.site, page,
                 day_offset, profile, clicks, impressions, seq),
            )

        # THE DUPLICATE INGEST: one day, five runs, rising clicks. The FRESHEST
        # row is the truth (10 / 100); a plain SUM would say 20 / 200.
        for seq, (clicks, impr) in enumerate([(1, 10), (2, 20), (3, 30), (4, 40), (10, 100)]):
            obs("gsc", "page", 0, clicks, impr, seq)
        # A second day inside the window, ingested once.
        obs("gsc", "page", 5, 5, 50, 0)
        # Bing counts too: the question is "does anyone arrive from search".
        obs("bing_webmaster", "page", 0, 3, 30, 0)
        # The per-query breakdown of clicks already counted above: never summed.
        obs("gsc", "query_page", 0, 999, 9990, 0)
        # Outside the 28-day window: excluded now, included when the knob moves.
        obs("gsc", "page", 200, 777, 7770, 0)

        expected_clicks, expected_impressions = 10 + 5 + 3, 100 + 50 + 30

        got = json.loads(
            _as(cur, w.me["user"], "select seo.list_page_intents(%s,%s,NULL,NULL,NULL,200,0)::text", (w.map, w.site))
        )
        row = next(i for i in got["items"] if i["page"]["id"] == page)
        assert got["performance_window_days"] == 28, got["performance_window_days"]
        assert (row["page"]["clicks"], row["page"]["impressions"]) == (expected_clicks, expected_impressions), (
            f"list_page_intents traffic is wrong (planted={planted}): got "
            f"{row['page']['clicks']}/{row['page']['impressions']}, expected "
            f"{expected_clicks}/{expected_impressions}. Five re-ingestions of one day are ONE day."
        )

        # The SAME number through the other door: seo._tm_item, per-item, inside
        # map_topic_associations. The two paths must never disagree.
        assoc = json.loads(
            _as(cur, w.me["user"], "select seo.map_topic_associations(%s,'beta',NULL)::text", (w.map,))
        )
        item = next(a["item"] for a in assoc if a["item"].get("id") == page)
        assert (item["clicks"], item["impressions"]) == (expected_clicks, expected_impressions), (
            f"_tm_item traffic disagrees with list_page_intents (planted={planted}): {item}"
        )
        assert item["performance_window_days"] == 28

        # THE WINDOW IS A KNOB, and the knob is READ: widen it and the 200-day-old
        # observation arrives. A hard-coded 28 fails right here.
        _srv(
            cur,
            "insert into platform.knob_override (feature, key, scope_kind, scope_id, organization_id, value) "
            "values ('seo.topical_map','performance_window_days','organization',%s,%s,'365'::jsonb) returning feature",
            (w.me["org"], w.me["org"]),
        )
        widened = json.loads(
            _as(cur, w.me["user"], "select seo.list_page_intents(%s,%s,NULL,NULL,NULL,200,0)::text", (w.map, w.site))
        )
        wrow = next(i for i in widened["items"] if i["page"]["id"] == page)
        assert widened["performance_window_days"] == 365, widened["performance_window_days"]
        assert wrow["page"]["clicks"] == expected_clicks + 777, (
            f"the performance window is not driven by its knob (planted={planted}): {wrow['page']}"
        )
    finally:
        _claims(cur, None)
        cur.execute("rollback to savepoint r22perf")


def test_a_hidden_topic_never_hides_its_page(db: tuple[Any, World]) -> None:
    """A topic can be hidden. A page can never be.

    `rejected` and `retired` both take a topic out of every topic reader — that
    is what they are for. The defect the round-7 verifier found is that the PAGE
    attached to such a topic went with it: not listed as covered, not listed as
    uncovered, not counted in the one number built to find unmapped pages. It
    simply stopped existing. This plants both hidden states, holds them (the door
    probes roll back, so the world never used to contain one), and asserts both
    halves: the topic is gone from every reader and present in the history, and
    the page is still listed with no current topics and counted as being on no
    topic.
    """
    cur, w = db
    cur.execute("savepoint r22hidden")
    try:
        _plant_defect_if_asked(cur)
        pages = {}
        for slug, status in (("hidden-rej", "proposed"), ("hidden-ret", "active")):
            tid = _srv(
                cur,
                "insert into seo.map_topic (organization_id, map_id, slug, name, status) "
                "values (%s,%s,%s,%s,%s) returning id",
                (w.me["org"], w.map, slug, slug, status),
            )
            # The page is NOT named after the topic: migration 22 correctly lists this page
            # as "on no topic" once its topic is hidden, so a URL containing the slug would
            # make the blanket "slug not in blob" check fire on the page, not on a leaked topic.
            page = _page(cur, w, {"hidden-rej": "orphan-one", "hidden-ret": "orphan-two"}[slug])
            _srv(
                cur,
                "insert into platform.associations (source_type,source_id,target_type,target_id,organization_id,role,payload_kind,payload) "
                "values ('web_page',%s,'seo_map_topic',%s,%s,'covers','map_topic_coverage',%s::jsonb)",
                (page, str(tid), w.me["org"], json.dumps({"confidence": 60, "source": "agent", "reason": "h"})),
            )
            pages[slug] = page
        # Hide them through the DOORS, the way a person would.
        assert not _as(
            cur, w.me["user"], "select seo.reject_map_topics(%s,'{hidden-rej}'::text[],'reject')::text", (w.map,)
        ).startswith("ERR")
        assert not _as(
            cur, w.me["user"], "select seo.retire_map_topics(%s,'{hidden-ret}'::text[],'retire',true)::text", (w.map,)
        ).startswith("ERR")
        # _as rolls its own call back, so hide them for real in this savepoint.
        _srv(cur, "update seo.map_topic set status='rejected' where map_id=%s and slug='hidden-rej'", (w.map,))
        _srv(cur, "update seo.map_topic set status='retired' where map_id=%s and slug='hidden-ret'", (w.map,))

        def as_me(sql: str, args: tuple) -> Any:
            return json.loads(_as(cur, w.me["user"], sql, args))

        # 1. THE TOPIC IS GONE from every topic reader.
        tree = as_me(
            "select seo.map_tree(%s,NULL::text,NULL::integer,'{counts,status}'::text[],NULL::uuid)::text", (w.map,)
        )
        outline = _as(cur, w.me["user"], "select seo.map_outline(%s,NULL,NULL,'{}'::jsonb)", (w.map,))
        graph = as_me("select seo.map_graph(%s,NULL::text,NULL::uuid)::text", (w.map,))
        search = as_me("select seo.search_map_topics(%s,'hidden-',25)::text", (w.map,))
        diag = as_me("select seo.map_diagnostics(%s,%s,200)::text", (w.map, w.site))
        gaps = as_me("select seo.list_topic_gaps(%s,%s)::text", (w.map, w.site))
        for label, blob in (
            ("map_tree", json.dumps(tree)), ("map_outline", outline), ("map_graph", json.dumps(graph)),
            ("search_map_topics", json.dumps(search)),
            # `retired_with_attachments` is the ONE place a hidden topic is named on
            # purpose — it exists to tell an editor that retiring left something
            # behind — so it is excluded from the blanket check and asserted
            # positively below.
            ("map_diagnostics", json.dumps({k: v for k, v in diag.items() if k != "retired_with_attachments"})),
            ("list_topic_gaps", json.dumps(gaps)),
        ):
            for slug in ("hidden-rej", "hidden-ret"):
                assert slug not in blob, f"{label} shows the {slug} topic, which every reader must hide: {blob[:400]}"
        # The by-slug INSPECTORS are deliberately not the same as the topic
        # LISTINGS above. A `rejected` topic is a proposal that was never real and
        # round 19 declares it absent — the same P0002 an invented slug gets. A
        # `retired` topic stays inspectable on purpose: map_diagnostics reports
        # retired_with_attachments, and an editor told "this retired topic still
        # holds a page" must be able to list that page in order to move it.
        assert _as(
            cur, w.me["user"], "select seo.map_topic_associations(%s,'hidden-rej',NULL)::text", (w.map,)
        ).startswith("ERR P0002"), "a rejected topic is still reachable by slug"
        still = _as(
            cur, w.me["user"], "select seo.map_topic_associations(%s,'hidden-ret',NULL)::text", (w.map,)
        )
        assert pages["hidden-ret"] in still, (
            "a retired topic must stay inspectable by slug, or map_diagnostics' "
            f"retired_with_attachments names something nobody can open: {still[:300]}"
        )

        assert [r["slug"] for r in diag["retired_with_attachments"]] == ["hidden-ret"], (
            "map_diagnostics must still tell an editor that retiring hidden-ret left a page "
            f"behind: {diag['retired_with_attachments']}"
        )

        # 2. THE HISTORY REMEMBERS IT — rejecting is never losing.
        hist = as_me("select seo.list_map_history(%s,NULL::text[],200,0)::text", (w.map,))
        by_slug = {i["slug"]: i for i in hist["items"]}
        assert by_slug.keys() >= {"hidden-rej", "hidden-ret"}, f"history lost them: {list(by_slug)}"
        assert by_slug["hidden-rej"]["status"] == "rejected"
        assert by_slug["hidden-ret"]["status"] == "retired"

        # 3. THE PAGE IS STILL THERE — round 22. This is the verifier's defect.
        intents = as_me("select seo.list_page_intents(%s,%s,NULL,NULL,NULL,500,0)::text", (w.map, w.site))
        listed = {i["page"]["id"]: i for i in intents["items"]}
        for slug, page in pages.items():
            assert page in listed, (
                f"the page whose only topic is {slug} VANISHED from list_page_intents. "
                f"A topic can be hidden; a page can never be."
            )
            assert listed[page]["current_topics"] == [], (
                f"the page on the hidden {slug} topic still reports a current topic: {listed[page]['current_topics']}"
            )
        sample = {s["page_id"] for s in diag["pages_on_no_topic_sample"]}
        for slug, page in pages.items():
            assert page in sample, (
                f"the page whose only topic is {slug} is not counted as being on no topic — "
                f"the one number built to find unmapped pages cannot see it."
            )

        # 4. A HIDDEN TOPIC IS NOT A DESTINATION — the same P0002 an invented slug gets.
        for slug in ("hidden-rej", "hidden-ret", "nope-nothing-here"):
            out = _as(
                cur,
                w.me["user"],
                "select seo.set_page_intents(%s,%s::jsonb,'human')::text",
                (w.site, json.dumps([{"page_id": w.page, "disposition": "move", "topic_slug": slug}])),
            )
            assert "not found in this site" in out, f"set_page_intents accepted {slug} as a destination: {out[:300]}"
            moved = _as(
                cur, w.me["user"], "select seo.move_map_topic(%s,'alpha-kid',%s)::text", (w.map, slug)
            )
            assert moved.startswith("ERR P0002"), (
                f"move_map_topic accepted {slug} as a parent — a live branch under a hidden "
                f"parent disappears with it: {moved[:300]}"
            )
    finally:
        _claims(cur, None)
        cur.execute("rollback to savepoint r22hidden")


# ═════════════════════════════════════════════════════════════════════════════
# ROUND 23 — PRECEDENCE. human > agent > mapper.
#
# The verifier proved that a mapper write to a (page, topic) pair a PERSON held
# silently rewrote the person's row: the DELETE that clears a re-run is scoped to
# the writing source, but the upsert behind it had no source in its conflict key,
# because there is one row per (page, topic, covers) and `source` lives in the
# payload. Ninety batches of a page mapper could erase an afternoon of somebody's
# decisions and report success.
#
# These probes hold a human row and drive every robot at it. The assertion is
# BYTE EQUALITY of the person's payload, not "it looks right".
# ═════════════════════════════════════════════════════════════════════════════

HUMAN_MARK = "Planted by a person, and it had better still be here"


def _as_kept(cur: Any, user: str, sql: str, args: tuple | None = None) -> str:
    """One call as a signed-in user whose EFFECT SURVIVES, for a test that needs
    to write and then look. The caller owns the savepoint around it."""
    try:
        cur.execute("set local role authenticated")
        _claims(cur, user)
        cur.execute(sql, args)
        out = cur.fetchone()[0]
        return "null" if out is None else str(out)
    except psycopg.Error as exc:
        return f"ERR {exc.sqlstate} {exc.diag.message_primary}"
    finally:
        cur.execute("reset role")
        _claims(cur, None)


def test_a_persons_edge_is_never_overwritten(db: tuple[Any, World]) -> None:
    cur, w = db
    cur.execute("savepoint r23")
    try:
        def covers_payload() -> Any:
            return _srv(
                cur,
                "select payload from platform.associations where source_type='web_page' and source_id=%s "
                "and target_type='seo_map_topic' and target_id=%s and role='covers'",
                (w.page, w.topics["alpha"]),
            )

        def intent_payload() -> Any:
            return _srv(
                cur,
                "select payload from platform.associations where source_type='web_page' and source_id=%s "
                "and target_type='seo_map_topic' and role='intent' and deleted_at is null",
                (w.page,),
            )

        # ── COVERS ───────────────────────────────────────────────────────────
        _srv(
            cur,
            "update platform.associations set payload = %s::jsonb "
            "where source_type='web_page' and source_id=%s and target_type='seo_map_topic' "
            "and target_id=%s and role='covers'",
            (json.dumps({"confidence": 100, "source": "human", "reason": HUMAN_MARK}), w.page, w.topics["alpha"]),
        )
        human_row = covers_payload()
        assert human_row["source"] == "human", human_row

        for robot in ("mapper", "agent"):
            out = json.loads(
                _as_kept(
                    cur, w.me["user"],
                    "select seo.set_page_map_topics(%s,%s::jsonb,%s)::text",
                    (w.page, json.dumps([{"slug": "alpha", "confidence": 61, "reason": f"{robot} says so"}]), robot),
                )
            )
            assert covers_payload() == human_row, (
                f"a {robot} write OVERWROTE the person's covers edge: {covers_payload()}"
            )
            assert out["kept_existing"] == [{"slug": "alpha", "kept_existing": "human"}], (
                f"a {robot} write left the person's edge alone but did not SAY so — not an error, "
                f"not silence: {out}"
            )
            assert out["covers"] == 0, out

        # A person always wins.
        won = json.loads(
            _as_kept(
                cur, w.me["user"],
                "select seo.set_page_map_topics(%s,%s::jsonb,'human')::text",
                (w.page, json.dumps([{"slug": "alpha", "confidence": 90, "reason": "a person changed their mind"}])),
            )
        )
        assert won["kept_existing"] == [] and won["covers"] == 1, won
        assert covers_payload()["reason"] == "a person changed their mind", covers_payload()

        # And the reverse rung: a HUMAN over a MAPPER row wins too.
        _srv(
            cur,
            "update platform.associations set payload = %s::jsonb where source_type='web_page' and source_id=%s "
            "and target_type='seo_map_topic' and target_id=%s and role='covers'",
            (json.dumps({"confidence": 20, "source": "mapper", "reason": "robot wrote this"}), w.page, w.topics["alpha"]),
        )
        over = json.loads(
            _as_kept(
                cur, w.me["user"],
                "select seo.set_page_map_topics(%s,%s::jsonb,'human')::text",
                (w.page, json.dumps([{"slug": "alpha", "confidence": 100, "reason": HUMAN_MARK}])),
            )
        )
        assert over["kept_existing"] == [] and covers_payload()["source"] == "human", (over, covers_payload())
        # An AGENT may take a MAPPER row — the ladder has three rungs, not two.
        up = json.loads(
            _as_kept(
                cur, w.me["user"],
                "select seo.set_page_map_topics(%s,%s::jsonb,'agent')::text",
                (w.page, json.dumps([{"slug": "alpha", "confidence": 55, "reason": "agent"}])),
            )
        )
        assert up["kept_existing"] == [{"slug": "alpha", "kept_existing": "human"}], up
        _srv(
            cur,
            "update platform.associations set payload = %s::jsonb where source_type='web_page' and source_id=%s "
            "and target_type='seo_map_topic' and target_id=%s and role='covers'",
            (json.dumps({"confidence": 20, "source": "mapper", "reason": "robot"}), w.page, w.topics["alpha"]),
        )
        assert json.loads(
            _as_kept(
                cur, w.me["user"], "select seo.set_page_map_topics(%s,%s::jsonb,'agent')::text",
                (w.page, json.dumps([{"slug": "alpha", "confidence": 55, "reason": "agent"}])),
            )
        )["covers"] == 1, "an agent must be able to take a mapper's row"

        # ── INTENTS ──────────────────────────────────────────────────────────
        def plant_intent(source: str, state: str) -> Any:
            _srv(
                cur,
                "delete from platform.associations where source_type='web_page' and source_id=%s "
                "and target_type='seo_map_topic' and role='intent'",
                (w.page,),
            )
            _srv(
                cur,
                "insert into platform.associations (source_type,source_id,target_type,target_id,organization_id,role,payload_kind,payload) "
                "values ('web_page',%s,'seo_map_topic',%s,%s,'intent','map_page_intent',%s::jsonb) returning id",
                (w.page, w.topics["alpha"], w.me["org"],
                 json.dumps({"disposition": "keep", "state": state, "source": source, "note": HUMAN_MARK})),
            )
            return intent_payload()

        def write_intent(source: str) -> Any:
            return json.loads(
                _as_kept(
                    cur, w.me["user"],
                    "select seo.set_page_intents(%s,%s::jsonb,%s)::text",
                    (w.site,
                     json.dumps([{"page_id": w.page, "topic_slug": "alpha", "disposition": "delete", "state": "proposed"}]),
                     source),
                )
            )

        held = plant_intent("human", "proposed")
        for robot in ("mapper", "agent"):
            out = write_intent(robot)
            assert intent_payload() == held, f"a {robot} write replaced the person's intent: {intent_payload()}"
            assert out["kept"] == 1 and out["set"] == 0, out
            assert out["results"][0]["kept_existing"] == {"source": "human", "state": "proposed"}, out["results"][0]
            assert out["results"][0]["ok"] is True, "a kept item is not a failure"

        # The SIGNED-OFF lock: an AGENT intent a person accepted is not replaced
        # by another agent — equal rank, so only the state rule can save it.
        for state in ("accepted", "done"):
            held = plant_intent("agent", state)
            out = write_intent("agent")
            assert intent_payload() == held, (
                f"an agent replaced an intent already {state}: {intent_payload()}"
            )
            assert out["results"][0]["kept_existing"] == {"source": "agent", "state": state}, out["results"][0]
            # A person may always change their mind.
            assert write_intent("human")["set"] == 1, f"a human could not replace an {state} intent"
            assert intent_payload()["disposition"] == "delete", intent_payload()
    finally:
        _claims(cur, None)
        cur.execute("rollback to savepoint r23")


def test_a_human_write_names_the_human(db: tuple[Any, World]) -> None:
    """🚨 `source='human'` IS THE TOP OF THE PRECEDENCE LADDER, SO IT MUST NAME SOMEBODY.

    Round 23 made `human` outrank every robot AND lock the pair against them. A write
    claiming that rank with no authenticated person behind it is an unattributable veto:
    nobody can be asked why, and no robot may ever undo it.

    The census that produced this rule (2026-09-17, live): 5,555 `covers` edges and 330
    `intent` edges, with `created_by` set on 0 of the covers and 77 of the intents. NO
    map edge had ever recorded a person, because both writers are SECURITY DEFINER and
    neither INSERT listed the column — so the door would have written an anonymous
    `human` veto for anybody who asked.

    Both halves are asserted on BOTH writers, because they are one rule in two places:
      * an unauthenticated `human` write is refused 42501;
      * an authenticated one succeeds AND records auth.uid() in created_by.
    A non-human source with no caller is deliberately still allowed — a robot has no
    person, and requiring one would stop the mapper.
    """
    cur, w = db
    cur.execute("savepoint humanactor")
    try:
        page, site, topic_slug = w.page, w.site, "alpha"

        # ── 1. the anonymous human write, on both writers ──────────────────────
        _claims(cur, None)
        for sql, args in (
            (
                "select seo.set_page_intents(%s::uuid, %s::jsonb, 'human')",
                (site, _j([{"page_id": page, "disposition": "keep", "topic_slug": topic_slug}])),
            ),
            (
                "select seo.set_page_map_topics(%s::uuid, %s::jsonb, 'human')",
                (page, _j([{"slug": topic_slug, "confidence": 90}])),
            ),
        ):
            cur.execute("savepoint anonhuman")
            try:
                cur.execute(sql, args)
                raised = None
            except psycopg.Error as exc:
                raised = exc
            cur.execute("rollback to savepoint anonhuman")
            assert raised is not None, f"an anonymous `human` write was ADMITTED by {sql}"
            assert raised.sqlstate == "42501", (
                f"{sql} answered {raised.sqlstate}: {raised}"
            )

        # ── 2. the authenticated human write records the person ───────────────
        _claims(cur, w.user)
        cur.execute(
            "select seo.set_page_intents(%s::uuid, %s::jsonb, 'human')",
            (site, _j([{"page_id": page, "disposition": "keep", "topic_slug": topic_slug}])),
        )
        assert cur.fetchone()[0]["set"] == 1

        cur.execute(
            "select seo.set_page_map_topics(%s::uuid, %s::jsonb, 'human')",
            (page, _j([{"slug": topic_slug, "confidence": 90}])),
        )
        assert cur.fetchone()[0]["ok"] is True

        for role in ("intent", "covers"):
            actor = _one(
                cur,
                "select a.created_by from platform.associations a "
                " where a.source_type='web_page' and a.source_id=%s::uuid "
                "   and a.target_type='seo_map_topic' and a.role=%s and a.deleted_at is null "
                " order by a.created_at desc limit 1",
                (page, role),
            )
            assert str(actor) == str(w.user), (
                f"the {role} edge a person wrote does not name that person — "
                "created_by is the only thing that makes a human veto answerable"
            )

        # ── 3. the rule fires on SOURCE, not on everybody ─────────────────────
        # A robot's write must still go through: requiring a person for `mapper` would
        # stop the page mapper dead. Note this stays AUTHENTICATED on purpose — a caller
        # with no jwt cannot pass either door's access check in the first place, so the
        # `human` rule is the SECOND gate, reachable only by a caller that has access
        # and still names nobody (a service or platform-admin lane). Dropping the claims
        # here would test the access check again and prove nothing about this rule.
        out = _one(
            cur,
            "select seo.set_page_map_topics(%s::uuid, %s::jsonb, 'mapper')",
            (page, _j([{"slug": topic_slug, "confidence": 60}])),
        )
        assert out["ok"] is True, (
            "requiring a person for a ROBOT's write would stop the page mapper"
        )
    finally:
        _claims(cur, w.user)
        cur.execute("rollback to savepoint humanactor")


def test_a_facet_collision_is_answered_never_thrown(db: tuple[Any, World]) -> None:
    """🚨 ONE VALUE PER (ROW, FACET) IS A FACT (0809), AND THE DOOR NEVER SAYS 23505.

    Round 27 proved a robot's facet write could destroy a person's older value because
    nothing made (row, facet) unique; 0809 built the partial unique index concurrently,
    and round 28 makes the writers answer a collision the way they answer a lost rank
    test — `{ok:true, kept_existing:{source, value, reason}}` — instead of letting a
    SQLSTATE reach a client.

    THE PLANT. Inside one call the DELETE precedes the INSERT, so the only real collision
    is a RACE between two writers, which a single transaction cannot stage. What it CAN
    stage is the same index conflict by another road: an edge whose payload names this
    facet but whose target value belongs to ANOTHER facet. The door's DELETE clears by the
    value's facet, so it misses that edge; the INSERT then lands on the same
    (row, role, payload facet) key and the index refuses it. Before round 28 that was a
    raw 23505 to the caller — the RED half of this test, asserted on the index directly.
    """
    cur, w = db
    cur.execute("savepoint facetcollision")
    try:
        _claims(cur, None)
        tier_value = _one(
            cur,
            "select v.id from seo.map_facet_value v join seo.map_facet f on f.id = v.facet_id "
            "where f.key = 'tier' and v.slug = 'core' and v.deleted_at is null limit 1",
        )
        assert tier_value, "the built-in tier facet value 'core' must exist"
        own_value = _one(
            cur,
            "select id from seo.map_facet_value where brand_id = %s and slug = 'tmdc-own' and deleted_at is null",
            (w.brand,),
        )
        # RED, on the index itself: two sourced edges naming facet 'region' on one page
        # are refused by the database — the fact 0809 made.
        cur.execute("savepoint plant")
        cur.execute(
            "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
            "values ('web_page', %s, 'seo_map_facet_value', %s, %s, 'facet', 'map_facet_assignment', "
            "%s::jsonb)",
            (w.page, tier_value, w.me["org"], _j({"source": "agent", "facet": "region"})),
        )
        raised = None
        try:
            cur.execute(
                "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
                "values ('web_page', %s, 'seo_map_facet_value', %s, %s, 'facet', 'map_facet_assignment', "
                "%s::jsonb)",
                (w.page, own_value, w.me["org"], _j({"source": "mapper", "facet": "region"})),
            )
        except psycopg.Error as exc:
            raised = exc
        cur.execute("rollback to savepoint plant")
        assert raised is not None and raised.sqlstate == "23505", (
            "two facet edges of one facet landed on one page — index associations_one_facet_value_per_row is missing or invalid"
        )

        # GREEN, through the door: the plant that the DELETE cannot clear, then a mapper
        # write of the region facet. The index refuses the INSERT; the door answers.
        cur.execute(
            "insert into platform.associations (source_type, source_id, target_type, target_id, organization_id, role, payload_kind, payload) "
            "values ('web_page', %s, 'seo_map_facet_value', %s, %s, 'facet', 'map_facet_assignment', %s::jsonb)",
            (w.page, tier_value, w.me["org"], _j({"source": "agent", "facet": "region"})),
        )
        out = _as(
            cur, w.user,
            "select seo.set_page_map_facet(%s::uuid, 'region', 'tmdc-own', 'mapper')::text",
            (w.page,),
        )
        assert not out.startswith("ERR"), f"the door surfaced a database error to the caller: {out}"
        answer = json.loads(out)
        assert answer.get("ok") is True and "kept_existing" in answer, (
            f"a collision must be answered as kept_existing, got {answer}"
        )
        assert answer["kept_existing"]["source"] == "agent"
    finally:
        _claims(cur, w.user)
        cur.execute("rollback to savepoint facetcollision")
