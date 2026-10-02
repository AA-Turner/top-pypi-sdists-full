"""The disposable world the generated seo door contract runs inside.

This is the per-feature half of the generated-contract system: ``db/generate_door_contract_test.py``
emits the assertions from the structured door rules in the database, and this module
supplies the ONE world their ``{placeholders}`` name — two tenants, a brand / site /
pages / topical map each, a foreign page covering one of our topics, and a facet value
on both sides.

It is deliberately NOT a second seeding routine: it reuses
``test_topical_map_door_contract._seed`` verbatim, so the hand-written contract and the
generated one always describe the same world, and a change to the world is made once.

Every id is created inside the caller's transaction and the caller always rolls back.
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path
from typing import Any

_HERE = Path(__file__).resolve().parent


def _contract_module() -> Any:
    """Load the hand-written contract module by path (tests are not a package)."""
    if "matrx_seo_door_contract_src" in sys.modules:
        return sys.modules["matrx_seo_door_contract_src"]
    spec = importlib.util.spec_from_file_location(
        "matrx_seo_door_contract_src", _HERE / "test_topical_map_door_contract.py"
    )
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules["matrx_seo_door_contract_src"] = mod
    spec.loader.exec_module(mod)
    return mod


def dsn() -> str | None:
    return _contract_module()._dsn()


def seed(cur: Any) -> dict[str, str]:
    """Seed the world and return it FLAT — the placeholder names the doors declare.

    ``{map}``/``{site}``/``{page}``/``{brand}``/``{own_value}``/``{user}`` are ours;
    ``{foreign_map}``/``{foreign_site}``/``{foreign_page}``/``{foreign_brand}``/
    ``{foreign_value}`` belong to a tenant this caller is not a member of.
    """
    mod = _contract_module()
    from matrx_orm.pytest_lock_guard import apply_ceilings

    apply_ceilings(cur)
    # Seeding writes to iam.organizations, whose new-user trigger competes with whatever
    # else is writing right now; the ceiling's default lock_timeout is short for PROBES.
    cur.execute("set local lock_timeout = '20s'")
    world = mod._seed(cur)
    mod._claims(cur, None)

    flat: dict[str, str] = {k: str(v) for k, v in world.me.items()}
    for key, value in world.foreign.items():
        flat[f"foreign_{key}"] = str(value)
    for slug, tid in world.topics.items():
        flat[f"topic_{slug}"] = str(tid)

    # ``{value_rule}`` / ``{foreign_value_rule}`` — one seo.keyword_class_rule per
    # tenant, on that tenant's own site. Added 2026-09-17 with migration 0802, which
    # gave seo.fn_value_rule_sync_meaning an access decision it never had: without a
    # rule on each side of the fence the generated contract cannot ask a foreign id and
    # an invented one the same question.
    for key, site_key, org_key, user_key in (
        ("value_rule", "site", "org", "user"),
        ("foreign_value_rule", "foreign_site", "foreign_org", "foreign_user"),
    ):
        site = flat.get(site_key)
        org = flat.get(org_key)
        if not site or not org:
            continue
        # `keyword_class_rule_owned` requires a creator on any non-template rule; the
        # tenant's own user if the world named one, otherwise whoever created the org.
        cur.execute(
            """
            insert into seo.keyword_class_rule
              (name, pattern, match_kind, target_class, site_id, organization_id,
               auto_apply, created_by)
            values (%s, 'door-contract', 'contains', 'money', %s::uuid, %s::uuid, false,
                    coalesce(%s::uuid, (select o.created_by from iam.organizations o
                                         where o.id = %s::uuid)))
            returning id
            """,
            (f"door contract {key}", site, org, flat.get(user_key), org),
        )
        flat[key] = str(cur.fetchone()[0])

    # ``{pack}`` / ``{foreign_pack}`` — one `internal` seo.starter_pack per tenant. Added
    # 2026-09-17 with migration 0850, which made seo.starter_pack_preview decide on its
    # pack argument: a pack of a tenant the caller is not in must answer exactly as an
    # invented id, and the contract can only ask that with a real foreign pack to hand.
    for key, org_key, user_key in (
        ("pack", "org", "user"),
        ("foreign_pack", "foreign_org", "foreign_user"),
    ):
        org = flat.get(org_key)
        if not org:
            continue
        _claims_as(cur, flat.get(user_key))
        cur.execute(
            """
            insert into seo.starter_pack
              (slug, name, industry, organization_id, published_to_web, created_by)
            values (%s, %s, 'door-contract', %s::uuid, false, %s::uuid)
            returning id
            """,
            (f"door-contract-{key}-{org[:8]}", f"door contract {key}", org, flat.get(user_key)),
        )
        flat[key] = str(cur.fetchone()[0])
        # one meaning item, so the OWNER's preview is not the same empty answer a
        # stranger gets — the identical-answer test needs a legal call that differs.
        cur.execute(
            """
            insert into seo.starter_pack_item
              (pack_id, item_kind, label, value, dimension_slug, dimension_scope, organization_id,
               created_by)
            values (%s::uuid, 'meaning', 'door contract audience', 'business', 'audience_type',
                    'platform', %s::uuid, %s::uuid)
            """,
            (flat[key], org, flat.get(user_key)),
        )
    _claims_as(cur, None)
    return flat


def _claims_as(cur: Any, user_id: str | None) -> None:
    """The world's own seeding identity: rows a tenant OWNS are created as that tenant."""
    _contract_module()._claims(cur, user_id)
