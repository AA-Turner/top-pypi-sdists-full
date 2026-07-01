"""visionQuery resolves ${param}/{{var}} in its description at runtime.

The V3 binding has no resolver downstream of the description, so an unresolved
"${test_param}"/"{{var}}" would reach /v1/heal/vision literally. visionQuery
resolves the template via var() at entry, so operation_intent + queried_value
carry the resolved text. Mirrors the V2 runtime template resolution behaviour (params/vars resolved before the vision call).
"""
from unittest.mock import MagicMock, patch


def test_visionQuery_resolves_param_and_variable_in_description():
    from testmu_selenium._helpers.vision_query import visionQuery
    from testmu_selenium._vars import _test_params, set_var, clear_state

    clear_state()
    _test_params["p"] = "zeeshan"
    set_var("v", "world")
    try:
        with patch("testmu_selenium._helpers.vision_query.SmartWait", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.get_driver", return_value=MagicMock()), \
             patch("testmu_selenium._helpers.vision_query.Heal") as m_heal:
            m_heal.return_value.vision_query.return_value.json.return_value = {"vision_query": "ok"}
            visionQuery("Check ${p} and {{v}}", "string")

        current_action = m_heal.call_args.args[0]
        assert current_action["operation_intent"] == "Check zeeshan and world"
        assert (
            current_action["sub_instruction_obj"]["operation_dict"]["queried_value"]
            == "Check zeeshan and world"
        )
    finally:
        clear_state()
