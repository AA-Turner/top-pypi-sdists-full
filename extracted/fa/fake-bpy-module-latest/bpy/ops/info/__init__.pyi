import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def report_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy selected reports to clipboard

    :return: Result of the operator call.
    """

def report_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected reports

    :return: Result of the operator call.
    """

def report_replay(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Replay selected reports

    :return: Result of the operator call.
    """

def reports_display_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update the display of reports in Blender UI (internal use)

    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "SELECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change selection of all visible reports

        :param action: Action, Selection action to execute (optional)

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :return: Result of the operator call.
    """

def select_box(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle box selection

        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :return: Result of the operator call.
    """

def select_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    report_index: int | None = 0,
    extend: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select reports by index

    :param report_index: Report, Index of the report (in [0, inf], optional)
    :param extend: Extend, Extend report selection (optional)
    :return: Result of the operator call.
    """
