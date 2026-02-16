import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the material settings and nodes

    :return: Result of the operator call.
    """

def new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new material

    :return: Result of the operator call.
    """

def paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste the material settings and nodes

    :return: Result of the operator call.
    """
