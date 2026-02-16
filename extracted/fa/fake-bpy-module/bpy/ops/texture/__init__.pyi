import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new texture

    :return: Result of the operator call.
    """

def slot_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the material texture settings and nodes

    :return: Result of the operator call.
    """

def slot_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move texture slots up and down

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def slot_paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the texture settings and nodes

    :return: Result of the operator call.
    """
