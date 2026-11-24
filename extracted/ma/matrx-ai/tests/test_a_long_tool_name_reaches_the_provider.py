"""A tool whose wire name runs past the providers' 64 characters is still offered and still dispatched.

Live 2026-11-06: 11 of 2,517 tool rows, all connector tools (``mcp.calendly.event_types-update_event_type_availability_schedule``),
turned into 65+ characters at ``.`` -> ``__``, so the provider boundary dropped them on every request and no agent could
ever call them. Their names come from someone else's server, so "rename the tool" was never available.
"""

from __future__ import annotations

from matrx_ai.config.wire_names import is_wire_safe, resolve_wire_name, to_wire_name

CALENDLY = "mcp.calendly.event_types-update_event_type_availability_schedule"
SIBLING = "mcp.calendly.event_types-update_event_type_availability_schedule_v2"
PLAIN_LONG = "a_plain_tool_name_with_no_namespace_that_runs_well_past_the_sixty_four_characters"


def test_a_long_name_has_a_wire_form_the_provider_accepts():
    assert is_wire_safe(to_wire_name(CALENDLY))
    assert is_wire_safe(to_wire_name(PLAIN_LONG))


def test_the_wire_form_is_stable_and_idempotent():
    wire = to_wire_name(CALENDLY)
    assert to_wire_name(CALENDLY) == wire
    assert to_wire_name(wire) == wire


def test_two_long_names_sharing_a_prefix_stay_two_tools():
    assert to_wire_name(CALENDLY) != to_wire_name(SIBLING)


def test_the_model_calling_the_short_form_reaches_the_real_tool():
    assert resolve_wire_name(to_wire_name(CALENDLY), [SIBLING, CALENDLY]) == CALENDLY
    assert resolve_wire_name(to_wire_name(PLAIN_LONG), ["other", PLAIN_LONG]) == PLAIN_LONG


def test_a_name_that_fits_is_written_exactly_as_before():
    assert to_wire_name("bundle:list_supabase") == "bundle__list_supabase"
    assert to_wire_name("mcp.docker-hub.listRepositoryTags") == "mcp__docker-hub__listRepositoryTags"
    assert to_wire_name("shell") == "shell"
    assert resolve_wire_name("shell", ["shell"]) is None
    assert resolve_wire_name("bundle__list_supabase", ["bundle:list_supabase"]) == "bundle:list_supabase"
