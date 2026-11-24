"""``wire_names.resolve_tool_reference``: the plain name, the wire name, or either behind a provider namespace
(OpenAI models write ``functions.skill`` in a gateway's job_key, 2026-11-19) resolve to the internal name, only
ever among the given candidates."""

from __future__ import annotations

import pytest

from matrx_ai.config.wire_names import resolve_tool_reference, strip_provider_namespace

CANDIDATES = ["skill", "find_tools", "bundle:list_google", "functions_helper"]


@pytest.mark.parametrize(
    ("reference", "expected"),
    [
        ("skill", "skill"),
        (" skill ", "skill"),
        ("functions.skill", "skill"),
        ("functions__skill", "skill"),
        ("functions:skill", "skill"),
        ("bundle__list_google", "bundle:list_google"),
        ("functions.bundle:list_google", "bundle:list_google"),
        ("functions.bundle__list_google", "bundle:list_google"),
        ("functions_helper", "functions_helper"),  # a real name that only starts like a namespace stays itself
        ("functions", None),
        ("functions.shell", None),  # never a name outside the candidates
        ("write-release", None),
        ("", None),
    ],
)
def test_reference_resolution(reference, expected):
    assert resolve_tool_reference(reference, CANDIDATES) == expected


def test_strip_takes_off_one_namespace_only():
    assert strip_provider_namespace("functions.functions.skill") == "functions.skill"
    assert strip_provider_namespace("tools.skill") == "tools.skill"
