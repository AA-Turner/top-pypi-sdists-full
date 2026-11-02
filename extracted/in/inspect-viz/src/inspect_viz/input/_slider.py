from typing import Any, Literal

from inspect_viz._util.marshall import dict_remove_none

from .._core import Component, Data, Param, Selection
from ._params import data_params, label_param
from ._util import input_component


def slider(
    data: Data | None = None,
    *,
    filter_by: Selection | None = None,
    label: str | None = None,
    column: str | None = None,
    field: str | None = None,
    target: Param | Selection | None = None,
    select: Literal["point", "interval"] | None = None,
    value: float | tuple[float, float] | None = None,
    min: float | None = None,
    max: float | None = None,
    step: float | None = None,
    width: float = 150,
) -> Component:
    """Select input widget.

    Args:
       data: The data source for this widget. Used in conjunction with the `column` property. The minimum and maximum values of the column determine the slider range.
       filter_by: A selection to filter the data source indicated by the `data` property.
       label: A text label for this input (optional).
       column: The name of a database column whose values determine the slider range. Used in conjunction with the `data` property. The minimum and maximum values of the column determine the slider range.
       field: The database column name to use within generated selection clause predicates. Defaults to the `column` property.
       target: A `Param` or `Selection` that this select input should update. For a `Param`, the selected value is set to be the new param value. For a `Selection`, a predicate that does an equality check (for `select=="point"`) or range check (for `select=="interval"`).
       select: The type of selection clause predicate to generate when `selection` is specified. If `'point'` (the default for a single value), the selection predicate is an equality check for the slider value. If `'interval'` (the default for a pair of values), the predicate checks the slider value interval.
       value: The initial slider value. Either a single numeric value or a tuple of two values representing a range.
       min: The minumum slider value.
       max: The maximum slider value.
       step: The slider step, the amount to increment between consecutive values.
       width: The width of the slider in screen pixels (defaults to 200)
    """
    # resolve selection mode
    select = select or ("interval" if isinstance(value, tuple) else "point")

    # value must correspond to selection mode
    if value is not None:
        if select == "interval" and not isinstance(value, tuple):
            raise ValueError(
                "slider `value` must be a tuple for interval selection mode"
            )
        if select == "point" and not isinstance(value, float | int):
            raise ValueError("slider 'value' must be a number for point selection")

    # base config
    config: dict[str, Any] = dict_remove_none(
        {
            "input": "slider",
            "select": select,
            "value": value,
            "min": min,
            "max": max,
            "step": step,
            "width": width,
        }
    )
    config = (
        config
        | label_param(label)
        | data_params(data, column, target, field, filter_by)
    )

    # validate that we have a target
    if "as" not in config:
        if not target:
            raise ValueError("You must pass a 'target' value for a slider input")
        else:
            config["as"] = target

    # if we don't have data then we need a min and max
    if "from" not in config:
        if "min" not in config or "max" not in config:
            raise ValueError(
                "slider: you must pass a 'min' and 'max' if no 'data' parameter is provided."
            )

    # return widget
    return input_component(config=config)
