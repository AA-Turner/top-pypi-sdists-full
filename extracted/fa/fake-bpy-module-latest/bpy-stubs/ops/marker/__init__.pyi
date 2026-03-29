import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new time marker

    :return: Result of the operator call.
    """

def camera_bind(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bind the selected camera to a marker on the current frame

    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected time marker(s)

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frames: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected time marker(s)

    :param frames: Frames, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def make_links_scene(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    scene: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy selected markers to another scene

    :param scene: Scene, (optional)
    :return: Result of the operator call.
    """

def move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frames: int | None = 0,
    tweak: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move selected time marker(s)

    :param frames: Frames, (in [-inf, inf], optional)
    :param tweak: Tweak, Operator has been activated using a click-drag event (optional)
    :return: Result of the operator call.
    """

def rename(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "RenamedMarker",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rename first selected time marker

    :param name: Name, New name for marker (optional, never None)
    :return: Result of the operator call.
    """

def select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    wait_to_deselect_others: bool | None = False,
    use_select_on_click: bool | None = False,
    mouse_x: int | None = 0,
    mouse_y: int | None = 0,
    extend: bool | None = False,
    camera: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select time marker(s)

    :param wait_to_deselect_others: Wait to Deselect Others, (optional)
    :param use_select_on_click: Act on Click, Instead of selecting on mouse press, wait to see if theres drag event. Otherwise select on mouse release (optional)
    :param mouse_x: Mouse X, (in [-inf, inf], optional)
    :param mouse_y: Mouse Y, (in [-inf, inf], optional)
    :param extend: Extend, Extend the selection (optional)
    :param camera: Camera, Select the camera (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change selection of all time markers

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
    tweak: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all time markers using box selection

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
        :param tweak: Tweak, Operator has been activated using a click-drag event (optional)
        :return: Result of the operator call.
    """

def select_leftright(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["LEFT", "RIGHT"] | None = "LEFT",
    extend: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select markers on and left/right of the current frame

    :param mode: Mode, (optional)
    :param extend: Extend Select, (optional)
    :return: Result of the operator call.
    """
