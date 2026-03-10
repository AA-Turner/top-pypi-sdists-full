import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def color_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new color to active palette

    :return: Result of the operator call.
    """

def color_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active color from palette

    :return: Result of the operator call.
    """

def color_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the active Color up/down in the list

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def extract_from_image(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    threshold: int | None = 1,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extract all colors used in Image and create a Palette

    :param threshold: Threshold, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def join(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    palette: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Join Palette Swatches

    :param palette: Palette, Name of the Palette (optional, never None)
    :return: Result of the operator call.
    """

def new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new palette

    :return: Result of the operator call.
    """

def sort(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["HSV", "SVH", "VHS", "LUMINANCE"] | None = "HSV",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Sort Palette Colors

    :param type: Type, (optional)
    :return: Result of the operator call.
    """
