"""Generated tool / bundle / shape-tools skills (chat-agent-skills lane F): deterministic, short,
linked to their source, found by search only (never carried by a tool set)."""

from __future__ import annotations

from matrx_ai.skills.coverage import (
    BundleFacts,
    ShapeFacts,
    ToolFacts,
    body_limit,
    build_bundle_skill,
    build_shape_tools_skill,
    build_tool_skill,
    description_limit,
    params_of,
    to_parsed_skill,
    wire,
)

CATALOG = ToolFacts(
    id="t-cat",
    name="service_status",
    description="Check whether an online service is having an outage right now.",
    parameters={"type": "object", "required": ["service"], "properties": {"service": {"type": "string", "description": "The service to check."}}},
    source_kind="catalog",
    display_name="Is this service down?",
    job_key="service_status",
    summary="Check whether an online service is having an outage right now.",
    output_kind="service_status",
    side_effect_class="paid_read",
)
MCP = ToolFacts(
    id="t-mcp",
    name="mcp.cal.users-get_user",
    description="Use: Fetch profile for a user by URI.\nWhen: User asks about another person's account.\nNeeds: User URI.\nAvoid: Calling this without a known URI.",
    parameters={"uri": {"type": "string", "required": True, "description": "User URI."}},
    source_kind="mcp_discovered",
    mcp_server_slug="cal",
    mcp_server_name="Calendar",
    listers=("bundle:list_cal",),
)
NATIVE = ToolFacts(
    id="t-nat",
    name="org_team_list",
    description="The organization's teams: id, name and member count. Read it before renaming a team." + " Long." * 400,
    parameters={"organization_id": {"type": "string", "format": "uuid", "required": True}, "include_archived": {"type": "boolean", "default": False}},
    source_kind="native",
)


def test_both_stored_parameter_shapes_are_read():
    assert [(p.name, p.required) for p in params_of(CATALOG.parameters)] == [("service", True)]
    assert [(p.name, p.required) for p in params_of(NATIVE.parameters)] == [("organization_id", True), ("include_archived", False)]


def test_a_tool_skill_is_short_specific_and_linked():
    for t in (CATALOG, MCP, NATIVE):
        g = build_tool_skill(t)
        assert len(g.body) <= body_limit(), (t.name, len(g.body))
        assert len(g.description) <= description_limit() and g.description.startswith("Use "), g.description
        assert g.allowed_tools == (t.id,) and g.link["tool_definition_id"] == t.id
        assert f"`{wire(t.name)}`" in g.body and "## How to get it" in g.body
        assert '"__kind": ""' not in g.body


def test_how_to_get_follows_the_source():
    assert "`use_tool`" in build_tool_skill(CATALOG).body and "job_key `service_status`" in build_tool_skill(CATALOG).body
    assert "`bundle__list_cal`" in build_tool_skill(MCP).body
    assert "`load_tools`" in build_tool_skill(NATIVE).body


def test_mcp_labelled_fields_become_trigger_and_pitfall():
    g = build_tool_skill(MCP)
    assert g.description.startswith("Use when user asks about another person's account")
    assert "Calling this without a known URI" in g.body


def test_same_source_same_bytes():
    assert build_tool_skill(CATALOG).source_hash == build_tool_skill(CATALOG).source_hash
    changed = ToolFacts(**{**CATALOG.__dict__, "summary": "Something else entirely."})
    assert build_tool_skill(changed).source_hash != build_tool_skill(CATALOG).source_hash


def test_combinations_name_every_member_and_how_to_load_them():
    b = build_bundle_skill(BundleFacts(id="b1", name="cal", description="Calendar tools.", lister_id="l1", lister_name="bundle:list_cal", members=(MCP,), mcp_server_slug="cal", mcp_server_name="Calendar"))
    assert "`mcp__cal__users-get_user`" in b.body and "`bundle__list_cal`" in b.body
    assert b.link["tool_definition_id"] == "l1" and b.link["tool_definition_ids"] == ["t-mcp"]
    s = build_shape_tools_skill(ShapeFacts(id="k1", kind="service_status", label="Service status", description=None, producers=(CATALOG,)))
    assert "`service_status`" in s.body and s.link["kind_definition_id"] == "k1" and "find_tools" in s.body


def test_never_carried_by_a_tool_set():
    """Search only: a generated skill must never declare attach_with_tools (that would put its
    body into every run holding the tool, changing prompts)."""
    p = to_parsed_skill(build_tool_skill(CATALOG))
    assert "attach_with_tools" not in p.extra_config
    assert p.extra_config["tool_definition_id"] == "t-cat" and p.ingested_from == "skill_coverage"
