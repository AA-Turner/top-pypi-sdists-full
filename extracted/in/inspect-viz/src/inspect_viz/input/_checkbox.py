from typing import Any

from .._core import Component, Data, Param, Selection
from ._params import column_validated
from ._util import input_component


def checkbox(
    data: Data | None = None,
    *,
    label: str | None = None,
    target: Param | Selection | None = None,
    field: str | None = None,
    checked: bool = False,
    values: tuple[str | float | bool | None, str | float | bool | None] = (True, False),
) -> Component:
    """Checkbox.

    Checkboxes have a `target` which is either a `Param` or `Selection`. In the latter case,
    the `field` parameter determines the data column name to use within generated selection
    clause predicates (defaulting to `column`). If no `target` is specified then the data
    source's selection is used as the target.

    The `values` tuple enables you to determine what value is communicated to the target
    for checked and unchecked states (by default, this is `True` and `False`).

    Args:
       data: The data source (required when specifying the `field` parameter to target a data source selection).
       label: A text label for the input (required)
       target: A `Param` or `Selection` that this checkbox should interact with (use `values` to customize the values that are used in the `target`).
       field: The data column name to use within generated selection clause predicates (required if `target` is not a `Param`).
       checked: Should the checkbox be in the checked state by default.
       values: What value is communicated to the target for checked and unchecked states.
    """
    config: dict[str, Any] = {
        "input": "checkbox",
        "checked": checked,
        "values": values,
    }

    if label is None:
        raise ValueError("You must specify a 'label' for checkboxes.")
    config["label"] = label

    if target is not None:
        config["as"] = target
    elif data is not None:
        config["as"] = data.selection
    else:
        raise ValueError(
            "You must pass either a 'data' or 'target` parameter to specify the checkbox value target."
        )

    if isinstance(config["as"], Selection):
        if field is None:
            raise ValueError("You must specify a 'field' when `target' is a selection.")
        config["field"] = column_validated(data, field)

    return input_component(config=config)
