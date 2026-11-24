"""A result cut by ``self_bounded_result`` must still validate against its tool's closed result kind.

Red before: ``SkillToolResult`` / ``WorkflowRunStatus`` (closed, ``extra="forbid"``) rejected the
``more_available`` and ``size_note`` keys the wrapper adds, filed as ``tool_output_contract_drift``
(class sec_b1ae4f60). The three keys are now declared once (``SelfBoundedFields``).
"""

import json

import pytest

from matrx_ai.tools.kinds import result_kind_model
from matrx_ai.tools.kinds.bounded import SelfBoundedFields
from matrx_ai.tools.output_caps import SELF_BOUNDED_KEYS, bound_owned_output

#: Tools wrapped in ``self_bounded_result`` that declare a closed result kind.
BOUNDED_TOOLS_WITH_KINDS = ("skill", "workflow_run", "workflow_catalog")


def test_the_fragment_declares_exactly_the_keys_the_wrapper_adds():
    assert set(SelfBoundedFields.model_fields) == set(SELF_BOUNDED_KEYS)
    body, bounded = bound_owned_output({"hints": [{"id": f"r{i}", "b": "x" * 2000} for i in range(100)]})
    assert bounded and set(SELF_BOUNDED_KEYS) <= set(body)


@pytest.mark.parametrize("tool", BOUNDED_TOOLS_WITH_KINDS)
def test_a_cut_result_validates_against_the_tool_kind(tool):
    model = result_kind_model(tool)
    assert model is not None
    assert set(SELF_BOUNDED_KEYS) <= set(model.model_fields), f"{tool} kind does not declare the bounded keys"
    schema = model.model_json_schema()
    assert schema.get("additionalProperties") is False
    assert set(SELF_BOUNDED_KEYS) <= set(schema["properties"])
    payload = {model.model_fields["kind_"].alias: model.kind_slug, "truncated": True, "more_available": True, "size_note": "CUT TO FIT"}
    model.model_validate(json.loads(json.dumps(payload)))
