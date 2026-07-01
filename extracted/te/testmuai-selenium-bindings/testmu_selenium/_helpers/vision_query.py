"""V3 Selenium-binding vision query helper.

Answers a vision query (presence / visibility / visual read) for the current
page and returns the result cast to the requested type. Mirrors the V2
vision-query path: the answer is computed from the untagged viewport
screenshot (no tagify), routed through the automind /v1/heal/vision endpoint
via Heal.vision_query(), and read from the response's ``vision_query`` field.

The generated test code calls this positionally:
    set_var("x", testmu_selenium.visionQuery("Is X visible?", "bool"))
so the driver is resolved from the active session rather than passed in.
"""

from testmu_selenium._heal import Heal
from testmu_selenium._helpers.driver import get_driver
from testmu_selenium._helpers.smart_wait import SmartWait


def _cast_value(value, return_type):
    """Cast the automind answer to the requested result type.

    The endpoint returns a JSON-native value (bool/number/string); the string
    branches make casting robust if it ever comes back as text.
    """
    if return_type == "bool":
        if isinstance(value, bool):
            return value
        return str(value).strip().lower() in ("true", "1", "yes")
    if return_type == "number":
        if isinstance(value, (int, float)):
            return float(value)
        s = str(value).strip()
        try:
            return float(s)
        except ValueError:
            filtered = "".join(c for c in s if c.isdigit() or c == ".")
            return float(filtered) if filtered else 0.0
    return "" if value is None else str(value)


def visionQuery(description, return_type, *, driver=None):
    """Run a vision query and return its answer cast to ``return_type``.

    Args:
        description: Natural-language query, e.g. "Check if 'hihi' is present".
        return_type: "bool" | "number" | "str".
        driver: Optional override; defaults to the active session driver.
    """
    driver = driver or get_driver()
    SmartWait(driver).smart_wait(is_vision=True)

    # Resolve ${param}/{{var}} templates before the description is placed into
    # current_action (operation_intent + queried_value) and sent to the analyzer.
    from testmu_selenium._vars import var
    description = var(description)

    # The automind /v1/heal endpoints hard-subscript operation_id /
    # instruction_id and read the query from
    # sub_instruction_obj.operation_dict.queried_value (see
    # _action_textual_query._direct_textual_read). Mirror that shape for vision;
    # ids are empty in standalone/live execution (no per-step ids to thread).
    current_action = {
        "operation_type": "VISION_QUERY",
        "operation_intent": description,
        "instruction_id": "",
        "operation_id": "",
        # use_query_v2 selects the automind vision model on /v1/heal/vision
        # (True -> gpt-4.1-mini, the V3 vision model; False -> gpt-4o). Kept True
        # for parity with the V3 vision template (VISION_QUERY_TEMPLATE_V2).
        "use_query_v2": True,
        "version": "v3",
        "result_type": return_type,
        "result_hint": "",
        "selector": [],
        "frame_info": [],
        "sub_instruction_obj": {
            "operation_dict": {
                "queried_value": description,
                "result_type": return_type,
            },
        },
    }

    resp = Heal(current_action, driver).vision_query()
    if resp is None:
        raise RuntimeError("visionQuery: no response from /v1/heal/vision")

    data = resp.json()
    if isinstance(data, dict) and data.get("error"):
        raise RuntimeError(f"visionQuery failed: {data['error']}")

    raw = data.get("vision_query") if isinstance(data, dict) else None
    if raw is None:
        raise RuntimeError(f"visionQuery response missing 'vision_query': {data}")

    return _cast_value(raw, return_type)
