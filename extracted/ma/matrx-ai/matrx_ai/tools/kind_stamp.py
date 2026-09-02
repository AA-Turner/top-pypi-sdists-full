"""THE RUNTIME HALF of the tool-result kind measure, for PACKAGE-hosted tools.

The package twin of ``aidream/tools/_kind_stamp.py`` (which this package may
never import): a multiplexed dispatcher's success branches build plain dicts,
and the tool's single entry point funnels its successful output through
``stamp_result_kind``. The model validates the branch's keys
(``additionalProperties:false`` — a branch key the kind forgot IS a defect)
and its dump carries ``__kind``, which ``ToolExecutor.execute`` verifies
against the live catalog.

Loud, not fatal: a payload the declared model refuses is logged and returned
UNSTAMPED — the executor's declared-kind enforcement then records the miss on
the result, exactly the posture the trace batch pinned. ONE funnel
(KIND_TOOL_LEDGER): ``sql`` carried the first inline copy; it and every later
package tool route through here.
"""

from __future__ import annotations

import logging

from pydantic import ValidationError

from matrx_ai.tools.models import ToolResult

logger = logging.getLogger(__name__)


def stamp_result_kind(result: ToolResult, model_cls: type) -> ToolResult:
    if not result.success or not isinstance(result.output, dict) or "__kind" in result.output:
        return result
    try:
        result.output = model_cls(**result.output).model_dump(mode="json")
    except ValidationError as exc:
        logger.warning(
            "[%s] RESULT_KIND_REFUSED: success payload does not fit declared kind %r: %s (call=%r)",
            result.tool_name or model_cls.__name__,
            getattr(model_cls, "kind_slug", "?"),
            str(exc).splitlines()[0][:200],
            result.call_id,
        )
    return result


__all__ = ["stamp_result_kind"]
