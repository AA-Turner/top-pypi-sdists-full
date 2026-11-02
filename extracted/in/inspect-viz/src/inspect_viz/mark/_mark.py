import json
from typing import Any, Sequence, TypeAlias, cast

from pydantic import JsonValue

from inspect_viz.mark._options import MarkOptions

from .._core.component import Component
from .._util.marshall import snake_to_camel

HIDDEN_USER_CHANNEL = "_user_channels"
HIDDEN_SHIFT_TEXT = "_shift_overlapping_text"


class Mark(Component):
    """Plot mark (create marks using mark functions, e.g. `dot()`, `bar_x()`, etc.)."""

    def __init__(
        self,
        type: str,
        config: dict[str, JsonValue],
        options: MarkOptions,
        defaults: MarkOptions | None = None,
    ) -> None:
        # resolve options against defaults
        resolved_options: dict[str, Any] = mark_options_to_camel(
            defaults or {}
        ) | mark_options_to_camel(options)

        # capture channel information and pass it along
        # as a hidden channel
        if "channels" in options:
            # channels implies tip
            if "tip" not in resolved_options:
                resolved_options["tip"] = True

            channels_json = json.dumps(options.get("channels", {}))

            # Note - even though the types indicate a string must be passed through, a list will actually go through with a simple static value
            resolved_options["channels"] = resolved_options.get("channels", {})
            resolved_options["channels"][HIDDEN_USER_CHANNEL] = cast(
                Any, [channels_json]
            )

        # set line_width for tip if necessary
        INFINITE_LINE = 1000000000
        tip = resolved_options.get("tip")
        if tip is True:
            resolved_options["tip"] = {"lineWidth": INFINITE_LINE}
        elif isinstance(tip, dict):
            tip["lineWidth"] = INFINITE_LINE

        # if shift_overlapping_text is set, add a hidden channel
        # to indicate that text should be shifted
        if "shift_overlapping_text" in options:
            resolved_options["channels"] = resolved_options.get("channels", {})
            resolved_options["channels"][HIDDEN_SHIFT_TEXT] = cast(
                Any, [options["shift_overlapping_text"]]
            )
            resolved_options.pop("shiftOverlappingText", None)

        super().__init__({"mark": type} | config | resolved_options)


def mark_options_to_camel(options: MarkOptions) -> dict[str, Any]:
    mark_options = {snake_to_camel(key): value for key, value in options.items()}
    if "tip" in mark_options and isinstance(mark_options["tip"], dict):
        mark_options["tip"] = {
            snake_to_camel(key): value for key, value in mark_options["tip"].items()
        }
    return mark_options


Marks: TypeAlias = Mark | Sequence[Mark | Sequence[Mark]]
"""Set of marks to add to a plot."""
