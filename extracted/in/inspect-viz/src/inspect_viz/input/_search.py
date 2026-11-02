from typing import Any, Literal

from inspect_viz._core.param import Param

from .._core import Component, Data, Selection
from ._params import column_validated, label_param
from ._util import input_component


def search(
    data: Data,
    *,
    filter_by: Selection | None = None,
    column: str | None = None,
    field: str | None = None,
    target: Param | Selection | None = None,
    type: Literal["contains", "prefix", "suffix", "regexp"] | None = None,
    label: str | None = None,
    placeholder: str | None = None,
    width: float | None = None,
) -> Component:
    """Text search input widget

    Args:
       data: The data source for input selections (used in conjunction with the `column` property).
       filter_by: A selection to filter the data source indicated by the `data` property.
       column: TThe name of a database column from which to pull valid search results. The unique column values are used as search autocomplete values. Used in conjunction with the `data` property.
       field: The data column name to use within generated selection clause predicates. Defaults to the `column` property.
       target:  A `Param` or `Selection` that this search box should update. For a `Param`, the textbox value is set as the new param value. For a `Selection`, a predicate based on the `type` option will be added to the selection.
       type: The type of text search query to perform. One of:
          - `"contains"` (default): the query string may appear anywhere in the text
          - `"prefix"`: the query string must appear at the start of the text
          - `"suffix"`: the query string must appear at the end of the text
          - `"regexp"`: the query string is a regular expression the text must match
       label: A text label for this input (optional).
       placeholder: Placeholder text for empty search box.
       width: Width in pixels (defaults to 150).
    """
    config: dict[str, Any] = {"input": "search"} | label_param(label)

    if type is not None:
        config["type"] = type

    if placeholder is not None:
        config["placeholder"] = placeholder

    # set data table and as_
    config["from"] = data.table
    config["as"] = target or data.selection

    # validate and set column
    if column is None:
        raise ValueError("You must pass a `column` value along with `data`")
    config["column"] = column_validated(data, column)

    # set field (optional, defaults to column)
    if field is not None:
        config["field"] = column_validated(data, field)

    # set filter_by
    if filter_by is not None:
        config["filterBy"] = filter_by

    # set width
    if width is not None:
        config["width"] = width

    # return widget
    return input_component(config=config)
