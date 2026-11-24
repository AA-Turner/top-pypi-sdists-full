"""A visitor Action's input never names a target (P3-HOSTS T11, design §5 "Declaration rule").

A signed-out visitor on an outside page runs ONE Action through an embed token, as the organization's visitor actor
(an organization member). The fence is the declaration: the Action's targets are fixed by what it is ("add a lead
to the organization's lead table"), never chosen by whoever presses the button. ``visitor_input_problems`` is that
rule; the visitor door refuses at admission any Action it answers for. Each banned shape is refused by name; a plain
contact-form input is admitted.
"""

from __future__ import annotations

from typing import Any
from uuid import UUID

import pytest
from pydantic import BaseModel, ConfigDict, Json

from matrx_graph.actions import declare_action, run_action
from matrx_graph.actions.doors import DOORS, visitor_input_problems
from matrx_graph.actions.engines import DOOR_AUTHORITY
from matrx_graph.actions import ActionRegistry
from matrx_graph.nodes import NodeRegistry


class ContactNote(BaseModel):
    """The plain input a visitor's button sends: words, an address to reply to, a count."""

    name: str
    email: str
    message: str
    seats: int = 1
    subscribe: bool = False
    topics: list[str] = []


class Inner(BaseModel):
    record_id: str


def _one(field: str, annotation: Any) -> type[BaseModel]:
    return type("Shape", (BaseModel,), {"__annotations__": {field: annotation}})


BANNED: list[tuple[str, type[BaseModel], str]] = [
    ("a UUID-typed field", _one("contact", UUID), "contact is a UUID"),
    ("a field named id", _one("id", str), "id names a target (an id)"),
    ("a *_id field", _one("lead_id", str), "lead_id names a target (an id)"),
    ("a camelCase *Id field", _one("leadId", str), "leadId names a target (an id)"),
    ("a table name", _one("table_name", str), "table_name names a target (table)"),
    ("a record name", _one("record", str), "record names a target (record)"),
    ("an organization", _one("organization", str), "organization names a target (org)"),
    ("a file", _one("attachment_file", str), "attachment_file names a target (file)"),
    ("a path", _one("save_path", str), "save_path names a target (path)"),
    ("a url", _one("callback_url", str), "callback_url names a target (url)"),
    ("an organisation", _one("organisation", str), "organisation names a target (org)"),
    ("a uri", _one("target_uri", str), "target_uri names a target (uri)"),
    ("a link", _one("link", str), "link names a target (link)"),
    ("an href", _one("href_value", str), "href_value names a target (href)"),
    ("a folder", _one("save_folder", str), "save_folder names a target (folder)"),
    ("a dir", _one("output_dir", str), "output_dir names a target (dir)"),
    ("a dict", _one("extra", dict), "extra is an open object (dict)"),
    ("a typed dict", _one("extra", dict[str, str]), "extra is an open object (dict)"),
    ("Any", _one("payload", Any), "payload is typed Any"),
    ("JSON", _one("payload", Json), "payload is untyped JSON"),
    ("an optional UUID", _one("contact", UUID | None), "contact is a UUID"),
    ("a list of UUIDs", _one("contacts", list[UUID]), "contacts is a UUID"),
    ("a nested model naming a record", _one("about", Inner), "about.record_id names a target (an id)"),
    ("an open object model", type("Open", (BaseModel,), {"model_config": ConfigDict(extra="allow")}),
     "(input) accepts extra fields (an open object)"),
]


@pytest.mark.parametrize("why, shape, problem", BANNED, ids=[b[0] for b in BANNED])
def test_each_banned_shape_is_refused_by_name(why: str, shape: type[BaseModel], problem: str) -> None:
    assert problem in visitor_input_problems(shape), (why, visitor_input_problems(shape))


def test_a_plain_text_input_is_admitted() -> None:
    assert visitor_input_problems(ContactNote) == []


def test_the_visitor_door_is_declared_and_carries_workflow_authority() -> None:
    assert "visitor" in DOORS
    # Not ``approved``: the organization's rule resolver still runs; an explicit off still wins.
    assert DOOR_AUTHORITY["visitor"] == "workflow"


@pytest.mark.asyncio
async def test_an_action_declares_the_visitor_door_and_runs_through_it() -> None:
    actions = ActionRegistry()

    class Ack(BaseModel):
        heard: str

    @declare_action(
        name="outside_sample.leave_note", description="Leave a note", input_schema=ContactNote, output_schema=Ack,
        doors={"visitor"}, action_registry=actions, node_registry=NodeRegistry(),
    )
    async def leave_note(app, input: ContactNote) -> Ack:  # noqa: ANN001
        return Ack(heard=input.message)

    spec = actions.get("outside_sample.leave_note")
    assert spec.door_names()["visitor"] == "/actions/visitor/outside_sample.leave_note/run"
    out = await run_action(spec, {"name": "Ana", "email": "ana@example.com", "message": "hi"}, app=None, door="visitor")
    assert out.heard == "hi"
