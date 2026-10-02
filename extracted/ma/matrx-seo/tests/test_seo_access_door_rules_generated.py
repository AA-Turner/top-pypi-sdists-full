"""GENERATED — do not edit. Regenerate with:

    uv run python db/generate_door_contract_test.py \
        --schema seo --like 'gsc_backfill_status,fn_brand_identity_sync_meaning,fn_value_rule_sync_meaning,starter_pack_site_status,starter_pack_preview' --out packages/matrx-seo/tests/test_seo_access_door_rules_generated.py --world matrx_seo_door_world

The contract below is not this file's opinion: every line of it is read from
``platform.client_callable_door.argument_rules`` and ``.contract_probe``, the
structured door rules migration 0796 made queryable. A door that changes its
declaration changes this file; a door whose BODY stops honouring its declaration
makes this file go red, by name.

What it asserts, per door:
  * the legal call works (the control);
  * every declared NULL rule — ``{"sqlstate": …, "says": …}`` raises that code and the
    sentence carries the declared ``says`` phrase; ``{"means"/"default": …}`` does NOT raise, because NULL is a
    value the body reads;
  * every entity-id argument decides ACCESS BEFORE EXISTENCE: another tenant's real id
    and an invented uuid answer with the same SQLSTATE, the same message, the declared
    SQLSTATE, and neither echoes the id back.

Live database, ONE transaction, ALWAYS rolled back. The world is seeded by
``matrx_seo_door_world`` and every probe runs inside a savepoint as a signed-in
caller who is not a member of the other tenant.

Run:  uv run pytest packages/matrx-seo/tests/test_seo_access_door_rules_generated.py
"""

# ruff: noqa: E501  — the probes are SQL and verbatim failure sentences

from __future__ import annotations

import json
import uuid
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any

import pytest

psycopg = pytest.importorskip("psycopg")

from matrx_seo_door_world import dsn as _dsn, seed as _seed  # noqa: E402

SCHEMA = 'seo'

# The declarations, verbatim from the database at generation time.
CONTRACT: dict[str, Any] = json.loads(
    r"""
{
 "fn_brand_identity_sync_meaning": {
  "args": [
   {
    "access": "viewer",
    "entity": "web_site",
    "foreign": {
     "note": "gsc_site_access_denied, decided before existence",
     "same_as_invented": true,
     "sqlstate": "42501"
    },
    "foreign_value": "{foreign_site}",
    "invented_value": "{invented}",
    "legal": "{site}",
    "name": "p_site_id",
    "null_outcome": null,
    "null_rule": {
     "says": "p_site_id",
     "sqlstate": "22023"
    },
    "type": "uuid"
   }
  ]
 },
 "fn_value_rule_sync_meaning": {
  "args": [
   {
    "access": "viewer",
    "entity": "seo_keyword_class_rule",
    "foreign": {
     "note": "value_rule_access_denied, decided before existence",
     "same_as_invented": true,
     "sqlstate": "42501"
    },
    "foreign_value": "{foreign_value_rule}",
    "invented_value": "{invented}",
    "legal": "{value_rule}",
    "name": "p_rule_id",
    "null_outcome": null,
    "null_rule": {
     "says": "p_rule_id",
     "sqlstate": "22023"
    },
    "type": "uuid"
   }
  ]
 },
 "gsc_backfill_status": {
  "args": [
   {
    "access": "viewer",
    "entity": "web_site",
    "foreign": {
     "note": "gsc_site_access_denied, decided before existence",
     "same_as_invented": true,
     "sqlstate": "42501"
    },
    "foreign_value": "{foreign_site}",
    "invented_value": "{invented}",
    "legal": "{site}",
    "name": "p_site_id",
    "null_outcome": null,
    "null_rule": {
     "says": "p_site_id",
     "sqlstate": "22023"
    },
    "type": "uuid"
   }
  ]
 },
 "starter_pack_preview": {
  "args": [
   {
    "access": "viewer",
    "entity": "web_site",
    "foreign": {
     "same_as_invented": true,
     "sqlstate": "42501"
    },
    "foreign_value": "{foreign_site}",
    "invented_value": "{invented}",
    "legal": "{site}",
    "name": "p_site_id",
    "null_outcome": null,
    "null_rule": {},
    "type": "uuid"
   },
   {
    "access": "decided before existence (0850)",
    "entity": "seo_starter_pack",
    "foreign": {
     "not_a_leak": true,
     "note": "0850: iam.has_access(seo_starter_pack, viewer) before any read; an unreadable pack answers the empty preview exactly like an invented id",
     "same_as_invented": true
    },
    "foreign_value": "{foreign_pack}",
    "invented_value": "{invented}",
    "legal": "{pack}",
    "name": "p_pack_id",
    "null_outcome": null,
    "null_rule": {},
    "type": "uuid"
   },
   {
    "access": null,
    "entity": null,
    "foreign": {
     "not_an_id": true
    },
    "foreign_value": null,
    "invented_value": null,
    "legal": "2026-06-01",
    "name": "p_start",
    "null_outcome": null,
    "null_rule": {},
    "type": "date"
   },
   {
    "access": null,
    "entity": null,
    "foreign": {
     "not_an_id": true
    },
    "foreign_value": null,
    "invented_value": null,
    "legal": "2026-09-01",
    "name": "p_end",
    "null_outcome": null,
    "null_rule": {},
    "type": "date"
   },
   {
    "access": null,
    "entity": null,
    "foreign": {
     "not_a_leak": true,
     "note": "filter over the (now gated) pack's own items"
    },
    "foreign_value": null,
    "invented_value": null,
    "legal": null,
    "name": "p_item_ids",
    "null_outcome": null,
    "null_rule": {},
    "type": "uuid[]"
   },
   {
    "access": null,
    "entity": null,
    "foreign": {
     "not_an_id": true
    },
    "foreign_value": null,
    "invented_value": null,
    "legal": 3,
    "name": "p_sample",
    "null_outcome": null,
    "null_rule": {},
    "type": "integer"
   }
  ]
 },
 "starter_pack_site_status": {
  "args": [
   {
    "access": "viewer",
    "entity": "web_site",
    "foreign": {
     "same_as_invented": true,
     "sqlstate": "42501"
    },
    "foreign_value": "{foreign_site}",
    "invented_value": "{invented}",
    "legal": "{site}",
    "name": "p_site_id",
    "null_outcome": null,
    "null_rule": {},
    "type": "uuid"
   },
   {
    "access": "viewer",
    "entity": "seo_starter_pack",
    "foreign": {
     "note": "seo_pack_not_found",
     "same_as_invented": true,
     "sqlstate": "P0001"
    },
    "foreign_value": "{foreign_pack}",
    "invented_value": "{invented}",
    "legal": "{pack}",
    "name": "p_pack_id",
    "null_outcome": null,
    "null_rule": {},
    "type": "uuid"
   }
  ]
 }
}
"""
)


@pytest.fixture(scope="module")
def db() -> Iterator[tuple[Any, dict[str, str]]]:
    dsn = _dsn()
    if dsn is None:
        pytest.skip("SUPABASE_MATRIX_* not set: this contract needs the live database")
    conn = psycopg.connect(dsn, autocommit=False, prepare_threshold=None)
    try:
        cur = conn.cursor()
        world = _seed(cur)
        yield cur, world
    finally:
        conn.rollback()  # ALWAYS: nothing this test writes survives it
        conn.close()


@dataclass
class Outcome:
    ok: bool
    code: str | None
    message: str
    rows: list | None = None


def _resolve(value: Any, world: dict[str, str]) -> Any:
    """Fill the {placeholders} the declaration stored with this run's own ids."""
    if not isinstance(value, str):
        return value
    out = value
    for key, actual in world.items():
        out = out.replace("{" + key + "}", actual)
    out = out.replace("{invented}", str(uuid.uuid4()))
    out = out.replace("{invented_text}", "nope-" + uuid.uuid4().hex[:10])
    return out


def _call(cur: Any, world: dict[str, str], fn: str, args: list[dict], values: dict) -> Outcome:
    sql = "select {}.{}({})::text".format(
        SCHEMA, fn, ", ".join(f"%s::{a['type']}" for a in args)
    )
    cur.execute("savepoint probe")
    try:
        try:
            cur.execute("set local role authenticated")
            cur.execute(
                "select set_config('request.jwt.claims', %s, true)",
                (json.dumps({"sub": world["user"], "role": "authenticated"}),),
            )
            cur.execute(sql, [values[a["name"]] for a in args])
            rows = cur.fetchall()
        except psycopg.Error as exc:
            cur.execute("rollback to savepoint probe")
            return Outcome(False, exc.sqlstate, exc.diag.message_primary or str(exc))
        cur.execute("rollback to savepoint probe")
        return Outcome(True, None, "", rows)
    finally:
        cur.execute("reset role")


def _scrub(text: str, token: Any) -> str:
    """Blank the id the caller itself passed, so two refusals can be compared."""
    for piece in str(token).replace('"', " ").replace(",", " ").split():
        piece = piece.strip("[]{}: ")
        if len(piece) >= 8:
            text = text.replace(piece, "<TOKEN>")
    return text


def _legal(world: dict[str, str], args: list[dict]) -> dict[str, Any]:
    return {a["name"]: _resolve(a["legal"], world) for a in args}


def _ids(spec: dict) -> list[str]:
    return [a["name"] for a in spec["args"] if a["entity"] and a["foreign"].get("sqlstate")]


def _same(spec: dict) -> list[str]:
    """Entity arguments whose rule promises the SAME ANSWER for a foreign and an invented
    id — a read that answers empty for both — rather than a refusal."""
    return [
        a["name"]
        for a in spec["args"]
        if a["entity"]
        and not a["foreign"].get("sqlstate")
        and a["foreign"].get("not_a_leak")
        and a["foreign"].get("same_as_invented")
    ]


def _nulls(spec: dict) -> list[str]:
    return [a["name"] for a in spec["args"] if a["null_rule"]]


@pytest.mark.parametrize("fn", sorted(CONTRACT))
def test_the_legal_call_works(db, fn: str) -> None:
    """The control. Without it, every refusal below could be a broken fixture."""
    cur, world = db
    spec = CONTRACT[fn]
    got = _call(cur, world, fn, spec["args"], _legal(world, spec["args"]))
    assert got.ok, f"{fn}: the owner's own legal call failed: {got.code} {got.message}"


@pytest.mark.parametrize(
    "fn,arg",
    sorted((fn, a) for fn, s in CONTRACT.items() for a in _nulls(s)),
)
def test_the_declared_null_rule_is_what_the_body_does(db, fn: str, arg: str) -> None:
    cur, world = db
    spec = CONTRACT[fn]
    rule = next(a for a in spec["args"] if a["name"] == arg)["null_rule"]
    values = _legal(world, spec["args"])
    values[arg] = None
    got = _call(cur, world, fn, spec["args"], values)

    if "sqlstate" in rule:
        assert not got.ok, (
            f"{fn}.{arg}: the door declares NULL is refused with {rule['sqlstate']}, "
            "and the call was ACCEPTED"
        )
        assert got.code == rule["sqlstate"], (
            f"{fn}.{arg}: declared NULL rule {rule['sqlstate']}, body answered "
            f"{got.code} {got.message}"
        )
        # THE REFUSAL IS A SENTENCE FOR A PERSON, NOT A STACK TRACE (ruled 2026-09-23, lane
        # ARGS-RULED-2). It never has to carry a parameter name. What the door DECLARES is the
        # phrase its sentence carries — `null_rule.says` — and that is what is matched, beside
        # the SQLSTATE. A rule with a SQLSTATE and no `says` is an incomplete declaration, and
        # it fails by name rather than being waved through on the code alone.
        says = rule.get("says")
        assert says, (
            f"{fn}.{arg}: the NULL rule declares {rule['sqlstate']} but no `says` — declare "
            f"the phrase the refusal sentence carries (it answered: {got.message})"
        )
        assert says in got.message, (
            f"{fn}.{arg}: the door declares its NULL refusal says {says!r}; it said "
            f"{got.message!r}"
        )
    else:
        meaning = rule.get("means") or rule.get("default")
        outcome = next(a for a in spec["args"] if a["name"] == arg).get("null_outcome") or {}
        if outcome.get("sqlstate"):
            assert got.code == outcome["sqlstate"], (
                f"{fn}.{arg}: NULL means {meaning!r}, and in this world that legally hits "
                f"{outcome['sqlstate']} ({outcome.get('why')}) — the body answered "
                f"{got.code} {got.message}"
            )
        else:
            assert got.ok, (
                f"{fn}.{arg}: the door declares NULL MEANS {meaning!r}, so the call must "
                f"proceed — it raised {got.code} {got.message}"
            )


@pytest.mark.parametrize(
    "fn,arg",
    sorted((fn, a) for fn, s in CONTRACT.items() for a in _ids(s)),
)
def test_a_foreign_id_and_an_invented_id_answer_alike(db, fn: str, arg: str) -> None:
    """THE ORACLE TEST. A real id the caller may not see and a uuid that names no row
    must be indistinguishable, or a stranger can ask the database which ids exist."""
    cur, world = db
    spec = CONTRACT[fn]
    rule = next(a for a in spec["args"] if a["name"] == arg)
    declared = rule["foreign"]["sqlstate"]

    foreign_values = _legal(world, spec["args"])
    foreign_token = _resolve(rule["foreign_value"], world)
    foreign_values[arg] = foreign_token
    foreign = _call(cur, world, fn, spec["args"], foreign_values)

    invented_values = _legal(world, spec["args"])
    invented_token = _resolve(rule["invented_value"], world)
    invented_values[arg] = invented_token
    invented = _call(cur, world, fn, spec["args"], invented_values)

    assert not foreign.ok, f"{fn}.{arg}: another tenant's {rule['entity']} was ACCEPTED"
    assert not invented.ok, f"{fn}.{arg}: an invented id was ACCEPTED"
    assert foreign.code == invented.code, (
        f"{fn}.{arg}: existence oracle — foreign answers {foreign.code}, "
        f"invented answers {invented.code}"
    )
    # A refusal may quote back the id the CALLER just passed — that discloses nothing.
    # What it may never do is differ in any other way, so both messages are compared with
    # the caller's own token blanked out.
    assert _scrub(foreign.message, foreign_token) == _scrub(invented.message, invented_token), (
        f"{fn}.{arg}: existence oracle — foreign says {foreign.message!r}, "
        f"invented says {invented.message!r}"
    )
    assert foreign.code == declared, (
        f"{fn}.{arg}: the door declares {declared} for an id the caller may not see; "
        f"the body answered {foreign.code} {foreign.message}"
    )
    # …and it may never carry an id belonging to the OTHER tenant that the caller did
    # not pass: that is the leak the scrub above must not be allowed to hide.
    leaked = [
        key
        for key, value in world.items()
        if key.startswith("foreign_") and value in foreign.message and value not in str(foreign_token)
    ]
    assert not leaked, f"{fn}.{arg}: the refusal carries the other tenant's {leaked}"


@pytest.mark.parametrize(
    "fn,arg",
    sorted((fn, a) for fn, s in CONTRACT.items() for a in _same(s)),
)
def test_a_foreign_id_and_an_invented_id_answer_identically(db, fn: str, arg: str) -> None:
    """THE ORACLE TEST, for a READ that answers empty rather than refusing. A real id the
    caller may not see and a uuid that names no row must produce the same outcome, row for
    row — so a stranger learns nothing, not even that the id exists."""
    cur, world = db
    spec = CONTRACT[fn]
    rule = next(a for a in spec["args"] if a["name"] == arg)

    foreign_values = _legal(world, spec["args"])
    foreign_token = _resolve(rule["foreign_value"], world)
    foreign_values[arg] = foreign_token
    foreign = _call(cur, world, fn, spec["args"], foreign_values)

    invented_values = _legal(world, spec["args"])
    invented_token = _resolve(rule["invented_value"], world)
    invented_values[arg] = invented_token
    invented = _call(cur, world, fn, spec["args"], invented_values)

    assert foreign.ok == invented.ok and foreign.code == invented.code, (
        f"{fn}.{arg}: existence oracle — foreign answers {foreign.code} {foreign.message!r}, "
        f"invented answers {invented.code} {invented.message!r}"
    )
    if foreign.ok:
        assert foreign.rows == invented.rows, (
            f"{fn}.{arg}: existence oracle — a foreign id and an invented id answer differently: "
            f"{str(foreign.rows)[:300]} vs {str(invented.rows)[:300]}"
        )
    else:
        assert _scrub(foreign.message, foreign_token) == _scrub(invented.message, invented_token), (
            f"{fn}.{arg}: existence oracle — foreign says {foreign.message!r}, "
            f"invented says {invented.message!r}"
        )
    # …and the legal call must not be the same empty answer, or this test proves nothing —
    # UNLESS the rule DECLARES, with its reason, that today the owner is refused too
    # (`foreign.owner_refused_too`: a door a pending ruling keeps shut for everybody). Then the
    # contract executes THAT claim, and the day the door opens this test goes red and names the
    # token to remove, so the declaration cannot outlive the ruling that ends it.
    legal = _call(cur, world, fn, spec["args"], _legal(world, spec["args"]))
    why_shut = rule["foreign"].get("owner_refused_too")
    if why_shut:
        assert legal.ok and legal.rows == foreign.rows, (
            f"{fn}.{arg}: the rule declares the owner is refused too ({why_shut}), and the "
            f"owner's legal call now answers differently — the door opened: remove "
            f"foreign.owner_refused_too from its argument_rules and regenerate. Owner got "
            f"{str(legal.rows)[:200]}"
        )
    else:
        assert legal.ok and legal.rows != foreign.rows, (
            f"{fn}.{arg}: the owner's legal call answers exactly what a stranger gets — "
            f"the fixture is empty or the door is dead"
        )


def test_every_declared_entity_argument_is_covered() -> None:
    """The generator's own claim: no entity id declared in the contract above is
    missing an oracle case. A door that gains an argument and is not regenerated
    fails `--check`, not this — this catches a generator that quietly dropped one."""
    for fn, spec in CONTRACT.items():
        declared = {a["name"] for a in spec["args"] if a["entity"]}
        tested = set(_ids(spec)) | set(_same(spec))
        undeclared = declared - tested
        assert not undeclared, (
            f"{fn}: entity arguments {sorted(undeclared)} name an entity and carry neither a "
            "foreign SQLSTATE nor a same-as-invented promise, so nothing proves they are not "
            "existence oracles"
        )
