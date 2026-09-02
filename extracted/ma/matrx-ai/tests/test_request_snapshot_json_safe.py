"""_json_safe must degrade at the LEAF, never drop the whole object.

The snapshot writer's docstring calls approximate fidelity acceptable, and it
is — but "approximate" meant something specific went wrong here. Because the
dataclass branch used dataclasses.asdict(), which deep-copies every leaf, ONE
un-copyable value anywhere inside a dataclass raised and sent the entire object
to repr(). In production that turned 2,049 of 5,473 response snapshots (37.4%)
into the string "TokenUsage(input_tokens=9443, ...)" where a 13-field object
belonged — a billing-relevant audit record reduced to prose.

It matters twice over: chat.request_snapshot is the conformance corpus the
agent-engine-extraction cutover gates on (CORPUS.md), and a repr string cannot
be compared structurally against anything.
"""

from __future__ import annotations

import dataclasses
import json

from matrx_ai.config.usage_config import TokenUsage
from matrx_ai.orchestrator.executor import _json_safe


class _RefusesDeepcopy:
    """Stands in for a provider SDK object parked inside raw_usage."""

    def __deepcopy__(self, memo):
        raise TypeError("cannot deepcopy SDK object")

    def __repr__(self) -> str:
        return "<SDKUsage>"


def test_asdict_is_what_used_to_fail():
    """The forcing function: if asdict ever stops raising here, this test tells
    you the workaround below is no longer buying anything."""
    usage = TokenUsage(input_tokens=1, output_tokens=2, raw_usage={"sdk": _RefusesDeepcopy()})
    try:
        dataclasses.asdict(usage)
    except TypeError:
        return
    raise AssertionError("asdict no longer raises — re-evaluate the field-walk in _json_safe")


def test_one_uncopyable_leaf_does_not_destroy_its_thirteen_siblings():
    usage = TokenUsage(
        input_tokens=9443,
        output_tokens=61,
        cached_input_tokens=3939,
        matrx_model_name="gemini-3.1-pro-preview",
        api="google",
        raw_usage={"sdk": _RefusesDeepcopy(), "thoughtsTokenCount": 128},
    )

    out = _json_safe(usage)

    assert isinstance(out, dict), "the whole object fell through to repr() again"
    assert {f.name for f in dataclasses.fields(TokenUsage)} == set(out)
    assert out["input_tokens"] == 9443
    assert out["matrx_model_name"] == "gemini-3.1-pro-preview"
    # Only the leaf that could not survive is degraded, and its sibling key in
    # the same nested dict is untouched.
    assert out["raw_usage"] == {"sdk": "<SDKUsage>", "thoughtsTokenCount": 128}
    assert json.dumps(out)


def test_a_clean_dataclass_is_unchanged_by_the_field_walk():
    """No key added, removed, reordered or retyped for the 62.6% that already
    worked — the snapshot writer's stated guarantee."""
    usage = TokenUsage(input_tokens=1, output_tokens=2, matrx_model_name="m")
    assert _json_safe(usage) == _json_safe(dataclasses.asdict(usage))


def test_nested_dataclasses_still_become_dicts():
    @dataclasses.dataclass
    class Inner:
        x: int = 1

    @dataclasses.dataclass
    class Outer:
        inner: Inner = dataclasses.field(default_factory=Inner)
        items: list = dataclasses.field(default_factory=lambda: [Inner(2)])

    assert _json_safe(Outer()) == {"inner": {"x": 1}, "items": [{"x": 2}]}
