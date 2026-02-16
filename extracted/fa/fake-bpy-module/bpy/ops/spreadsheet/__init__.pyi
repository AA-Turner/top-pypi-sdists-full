import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def add_row_filter_rule(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a filter to remove rows from the displayed data

    :return: Result of the operator call.
    """

def change_spreadsheet_data_source(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    component_type: int | None = 0,
    attribute_domain_type: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change visible data source in the spreadsheet

    :param component_type: Component Type, (in [0, 32767], optional)
    :param attribute_domain_type: Attribute Domain Type, (in [0, 32767], optional)
    :return: Result of the operator call.
    """

def fit_column(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Resize a spreadsheet column to the width of the data

    :return: Result of the operator call.
    """

def remove_row_filter_rule(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove a row filter from the rules

    :param index: Index, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def reorder_columns(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the order of columns

    :return: Result of the operator call.
    """

def resize_column(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Resize a spreadsheet column

    :return: Result of the operator call.
    """

def toggle_pin(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Turn on or off pinning

    :return: Result of the operator call.
    """
