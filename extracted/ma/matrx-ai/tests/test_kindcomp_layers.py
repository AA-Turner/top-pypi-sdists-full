"""kindcomp_* ``target`` (shape layers): mine / organization / shared.

The fake layer table behaves like the REAL one is allowed to: it hands back every
row to any reader (RLS lets coworkers and platform admins see user rows) and its
write-gate trigger refuses a signed-in non-author -- but a write with NO signed-in
person passes untouched. So these tests only stay green when the tool (a) writes
inside the person's session and (b) states the audience itself.
"""

from __future__ import annotations

import contextlib
from contextvars import ContextVar
from types import SimpleNamespace
from typing import Any
from uuid import uuid4

import pytest

from matrx_ai import _ext
from matrx_ai.tools.implementations import kind_component, kind_layer
from matrx_ai.tools.models import ToolContext

GOOD_SRC = "export default function C({ props }) { return <p>{props.data.title}</p>; }"

_session_user: ContextVar[str | None] = ContextVar("session_user", default=None)


class World:
    """One shared 'database' + the person currently calling."""

    def __init__(self) -> None:
        self.rows: list[SimpleNamespace] = []
        self.shared_touched = False
        self.privileged_writes = 0
        self.person = str(uuid4())
        self.org = str(uuid4())
        self.members: set[tuple[str, str]] = set()  # (person, org)
        self.admins: set[tuple[str, str]] = set()


def org_row_visible(w: World, row: Any) -> bool:
    """RLS: an org view is readable by members of that org only (privileged = everything)."""
    who = _session_user.get()
    if who is None or row.audience_organization_id is None:
        return True
    return (who, str(row.audience_organization_id)) in w.members


def org_write_refused(w: World, audience_org: Any, who: str | None) -> bool:
    """The write-gate trigger: org views are written by that org's owners/admins only."""
    return bool(who and audience_org and (who, str(audience_org)) not in w.admins)


class Query:
    def __init__(self, rows: list[Any]) -> None:
        self._rows = rows

    async def all(self) -> list[Any]:
        return list(self._rows)


def make_layer_model(w: World):
    class FakeLayer:
        @classmethod
        def filter(cls, **kw: Any) -> Query:
            # RLS shows other people's user rows too: audience kwargs do NOT narrow here.
            kw = {k: v for k, v in kw.items() if not k.startswith("audience_")}
            return Query(
                [
                    r
                    for r in w.rows
                    if all(getattr(r, k) == v for k, v in kw.items()) and org_row_visible(w, r)
                ]
            )

        @classmethod
        async def get_or_none(cls, use_cache=False, id=None):  # noqa: A002
            return next((r for r in w.rows if str(r.id) == str(id) and org_row_visible(w, r)), None)

        @classmethod
        async def create_item(cls, **p: Any):
            who = _session_user.get()
            if who is None:
                w.privileged_writes += 1  # the trigger would LET THIS THROUGH
            if org_write_refused(w, p.get("audience_organization_id"), who):
                raise RuntimeError(
                    "42501 Only an owner or admin of the organization can change its view."
                )
            if who is not None and p.get("audience_user_id") and p["audience_user_id"] != who:
                raise RuntimeError(
                    "42501 Only the person a personal view belongs to can change it."
                )
            defaults = dict(
                id=uuid4(), semver="1.0.0", version=1, deleted_at=None, sort_order=100,
                pinned_kind_version=None, notes=None, is_active=True, audience_user_id=None,
                audience_organization_id=None, props_transform=None, created_by=who,
            )  # fmt: skip
            row = SimpleNamespace(**{**defaults, **p})
            w.rows.append(row)
            return row

        @classmethod
        async def update_where(cls, flt: dict[str, Any], **values: Any):
            who = _session_user.get()
            row = next(r for r in w.rows if str(r.id) == flt["id"])
            if org_write_refused(w, row.audience_organization_id, who):
                raise RuntimeError(
                    "42501 Only an owner or admin of the organization can change its view."
                )
            if who is None:
                w.privileged_writes += 1
            elif row.audience_user_id and row.audience_user_id != who:
                raise RuntimeError(
                    "42501 Only the person a personal view belongs to can change it."
                )
            for k, v in values.items():
                setattr(row, k, v)
            return SimpleNamespace(rows_affected=1)

    return FakeLayer


class FakeShared:
    @classmethod
    def filter(cls, **_k: Any):
        raise AssertionError("the layer path must never read kind_component")

    @classmethod
    async def get_or_none(cls, **_k: Any):
        raise AssertionError("the layer path must never read kind_component")

    @classmethod
    async def update_where(cls, *_a: Any, **_k: Any):
        raise AssertionError("the layer path must never write kind_component")

    create_item = update_where


@pytest.fixture
def world(monkeypatch: pytest.MonkeyPatch) -> World:
    w = World()
    layer = make_layer_model(w)

    @contextlib.asynccontextmanager
    async def session(_ctx=None):
        token = _session_user.set(w.person)
        try:
            yield
        finally:
            _session_user.reset(token)

    monkeypatch.setitem(_ext._registry, "acting_as_caller", session)
    models = {"KindComponentLayer": layer, "KindComponent": FakeShared}
    monkeypatch.setattr(kind_layer, "get_db_model", lambda n: models[n])
    monkeypatch.setattr(kind_component, "get_db_model", lambda n: models[n])

    async def no_definition(_ref, _ctx):  # unregistered kind: no definition anywhere
        return None, SimpleNamespace(error=SimpleNamespace(error_type="not_found"))

    monkeypatch.setattr(kind_layer, "resolve_kind", no_definition)

    async def ok_source(_s):
        return None, True

    monkeypatch.setattr(kind_component, "_refuse_broken_source", ok_source)
    monkeypatch.setattr(kind_layer, "ctx_user_id", lambda _c: w.person)
    monkeypatch.setattr(kind_layer, "ctx_org_id", lambda _c: w.org)
    monkeypatch.setattr(kind_component, "ctx_user_id", lambda _c: w.person)
    return w


def ctx() -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name="test")


async def make_mine(slug: str = "never_registered_kind") -> str:
    r = await kind_component.kindcomp_create_component(
        {
            "kind": slug,
            "component_key": "my_card",
            "component_source": GOOD_SRC,
            "target": "mine",
        },
        ctx(),
    )
    assert r.success, r.error
    return r.output.component_id


@pytest.mark.asyncio
async def test_mine_writes_a_layer_row_as_the_person_for_an_unregistered_slug(world: World) -> None:
    cid = await make_mine()
    row = world.rows[0]
    assert str(row.id) == cid
    assert row.kind == "never_registered_kind"  # keyed by slug; no definition exists
    assert row.audience_user_id == world.person
    assert row.audience_organization_id is None
    assert str(row.organization_id) == world.org
    assert world.privileged_writes == 0  # written inside the person's session


@pytest.mark.asyncio
async def test_a_second_view_for_the_same_audience_is_an_update_not_a_create(world: World) -> None:
    await make_mine()
    r = await kind_component.kindcomp_create_component(
        {
            "kind": "never_registered_kind",
            "component_key": "other",
            "component_source": GOOD_SRC,
            "target": "mine",
        },
        ctx(),
    )
    assert not r.success and r.error.error_type == "validation"
    assert len(world.rows) == 1


@pytest.mark.asyncio
async def test_another_person_cannot_read_or_change_my_view(world: World) -> None:
    cid = await make_mine()
    world.person = str(uuid4())  # a coworker now calls; RLS would hand them the row
    for call, args in (
        (kind_component.kindcomp_get_code, {"component_id": cid}),
        (
            kind_component.kindcomp_update_code,
            {"component_id": cid, "updates": {"component_source": GOOD_SRC + " "}},
        ),
        (
            kind_component.kindcomp_patch_code,
            {"component_id": cid, "patches": [{"old_string": "p>", "new_string": "div>"}]},
        ),
        (
            kind_component.kindcomp_update_settings,
            {"component_id": cid, "settings": {"notes": "x"}},
        ),
    ):
        res = await call({**args, "target": "mine"}, ctx())
        assert not res.success and res.error.error_type == "not_found", call.__name__
    before = world.rows[0].component_source
    assert world.rows[0].component_source == before and world.rows[0].notes is None


@pytest.mark.asyncio
async def test_context_lists_only_my_own_rows_and_never_a_coworkers(world: World) -> None:
    mine = await make_mine()
    other = str(uuid4())
    world.rows.append(
        SimpleNamespace(
            id=uuid4(), kind="never_registered_kind", platform="web", role="output",
            audience_user_id=other, audience_organization_id=None, component_key="theirs",
            source="db", component_source="x", props_transform=None, config={},
            pinned_kind_version=None, is_active=True, sort_order=100, semver="1.0.0",
            notes=None, deleted_at=None, version=1, organization_id=world.org,
        )
    )  # fmt: skip
    r = await kind_component.kindcomp_get_context(
        {"kind": "never_registered_kind", "target": "mine", "sample": {"title": "t"}}, ctx()
    )
    assert r.success, r.error
    assert r.output.component_ids == [mine]
    assert r.output.summary.kind == "never_registered_kind"
    assert r.output.json_schema is not None  # inferred from the on-screen sample


@pytest.mark.asyncio
async def test_organization_target_needs_an_org_and_stamps_the_audience(world: World) -> None:
    base = {"kind": "k_org", "component_key": "c", "component_source": GOOD_SRC}
    r = await kind_component.kindcomp_create_component({**base, "target": "organization"}, ctx())
    assert not r.success and r.error.error_type == "validation"
    org = str(uuid4())
    world.admins.add((world.person, org))
    r = await kind_component.kindcomp_create_component(
        {**base, "target": "organization", "organization_id": org}, ctx()
    )
    assert r.success, r.error
    row = world.rows[0]
    assert row.audience_organization_id == org and row.audience_user_id is None
    assert str(row.organization_id) == org


@pytest.mark.asyncio
async def test_my_view_id_is_not_reachable_through_the_organization_target(world: World) -> None:
    cid = await make_mine()
    r = await kind_component.kindcomp_get_code(
        {"component_id": cid, "target": "organization", "organization_id": str(uuid4())}, ctx()
    )
    assert not r.success and r.error.error_type == "not_found"


@pytest.mark.asyncio
async def test_shared_target_still_takes_the_shared_path(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    """target omitted == 'shared': resolve_kind + the edit gate + kind_component, never the layer."""
    seen: list[str] = []
    kind = SimpleNamespace(id=uuid4(), kind="k", organization_id=uuid4())

    async def fake_resolve(ref, _c):
        seen.append(ref)
        return kind, None

    async def allow(_k, _c):
        return None

    class Shared:
        @classmethod
        def filter(cls, **_k):
            return Query([])

        @classmethod
        async def update_where(cls, *_a, **_k):
            return []

        @classmethod
        async def create_item(cls, **p):
            assert "kind_definition_id" in p and "audience_user_id" not in p
            return SimpleNamespace(id=uuid4(), semver="1.0.0")

    monkeypatch.setattr(kind_component, "resolve_kind", fake_resolve)
    monkeypatch.setattr(kind_component, "ensure_can_edit_kind", allow)
    monkeypatch.setattr(kind_component, "get_db_model", lambda _n: Shared)
    r = await kind_component.kindcomp_create_component(
        {"kind": "k", "component_key": "c", "component_source": GOOD_SRC}, ctx()
    )
    assert r.success, r.error
    assert seen == ["k"] and world.rows == []


@pytest.mark.asyncio
async def test_bad_target_is_refused_loudly(world: World) -> None:
    r = await kind_component.kindcomp_get_context({"kind": "k", "target": "mine"}, ctx())
    assert r.success  # sanity: mine is fine
    from matrx_ai.tools.implementations.kind_layer import target_refusal

    assert target_refusal({"target": "everyone"}).error.error_type == "validation"


@pytest.mark.asyncio
async def test_no_person_session_means_refusal_not_a_privileged_write(
    world: World, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setitem(_ext._registry, "acting_as_caller", None)
    r = await kind_component.kindcomp_create_component(
        {"kind": "k", "component_key": "c", "component_source": GOOD_SRC, "target": "mine"}, ctx()
    )
    assert not r.success and world.rows == [] and world.privileged_writes == 0


@pytest.mark.asyncio
async def test_owner_updates_patches_and_settings_run_in_the_persons_session(world: World) -> None:
    cid = await make_mine()
    row = world.rows[0]
    r = await kind_component.kindcomp_update_code(
        {"component_id": cid, "updates": {"component_source": GOOD_SRC + "\n"}, "target": "mine"},
        ctx(),
    )
    assert r.success, r.error
    r = await kind_component.kindcomp_patch_code(
        {
            "component_id": cid,
            "patches": [{"old_string": "<p>", "new_string": "<div>"}, {"old_string": "</p>", "new_string": "</div>"}],
            "target": "mine",
        },
        ctx(),
    )  # fmt: skip
    assert r.success, r.error
    r = await kind_component.kindcomp_update_settings(
        {"component_id": cid, "settings": {"is_active": False}, "target": "mine"}, ctx()
    )
    assert r.success, r.error
    assert "<div>" in row.component_source and row.is_active is False
    assert world.privileged_writes == 0  # no write ever left the person's session
    bad = await kind_component.kindcomp_update_settings(
        {"component_id": cid, "settings": {"is_default": True}, "target": "mine"}, ctx()
    )
    assert not bad.success and bad.error.error_type == "validation"


# ── organization target: who may read / write is the DATABASE's answer ────────


async def org_view(world: World, org: str) -> str:
    """An org view authored by an admin of ``org``; returns its id."""
    admin = world.person
    world.members.add((admin, org))
    world.admins.add((admin, org))
    r = await kind_component.kindcomp_create_component(
        {"kind": "k_org", "component_key": "c", "component_source": GOOD_SRC,
         "target": "organization", "organization_id": org},
        ctx(),
    )  # fmt: skip
    assert r.success, r.error
    return r.output.component_id


def become(world: World, org: str, role: str) -> None:
    world.person = str(uuid4())
    if role in ("member", "admin"):
        world.members.add((world.person, org))
    if role == "admin":
        world.admins.add((world.person, org))


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["nonmember", "member"])
async def test_org_create_is_refused_for_anyone_who_is_not_an_org_admin(
    world: World, role: str
) -> None:
    org = str(uuid4())
    become(world, org, role)
    r = await kind_component.kindcomp_create_component(
        {"kind": "k_org", "component_key": "c", "component_source": GOOD_SRC,
         "target": "organization", "organization_id": org},
        ctx(),
    )  # fmt: skip
    assert not r.success and r.error.error_type == "no_access"
    assert world.rows == [] and world.privileged_writes == 0


@pytest.mark.asyncio
@pytest.mark.parametrize("role", ["nonmember", "member"])
async def test_org_update_code_is_refused_for_non_admins(world: World, role: str) -> None:
    org = str(uuid4())
    cid = await org_view(world, org)
    original = world.rows[0].component_source
    become(world, org, role)
    r = await kind_component.kindcomp_update_code(
        {"component_id": cid, "updates": {"component_source": GOOD_SRC + "//x"},
         "target": "organization", "organization_id": org},
        ctx(),
    )  # fmt: skip
    # a non-member cannot even see the row; a member sees it and the trigger refuses the write
    expected = "not_found" if role == "nonmember" else "no_access"
    assert not r.success and r.error.error_type == expected
    assert world.rows[0].component_source == original and world.privileged_writes == 0


@pytest.mark.asyncio
@pytest.mark.parametrize(("role", "sees"), [("nonmember", 0), ("member", 1), ("admin", 1)])
async def test_org_get_context_lists_what_the_database_lets_that_person_read(
    world: World, role: str, sees: int
) -> None:
    org = str(uuid4())
    await org_view(world, org)
    become(world, org, role)
    r = await kind_component.kindcomp_get_context(
        {"kind": "k_org", "target": "organization", "organization_id": org}, ctx()
    )
    assert r.success, r.error
    assert len(r.output.component_ids) == sees


@pytest.mark.asyncio
async def test_an_org_admin_can_update_the_org_view(world: World) -> None:
    org = str(uuid4())
    cid = await org_view(world, org)
    become(world, org, "admin")
    r = await kind_component.kindcomp_update_code(
        {"component_id": cid, "updates": {"component_source": GOOD_SRC + "//ok"},
         "target": "organization", "organization_id": org},
        ctx(),
    )  # fmt: skip
    assert r.success, r.error
    assert world.rows[0].component_source.endswith("//ok")
