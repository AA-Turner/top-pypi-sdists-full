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
    """Add a new workspace by duplicating the current one or appending one from the user configuration

    :return: Result of the operator call.
    """

def append_activate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    idname: str | None = "",
    filepath: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Append a workspace and make it the active one in the current window

    :param idname: Identifier, Name of the workspace to append and activate (optional, never None)
    :param filepath: Filepath, Path to the library (optional, never None, blend relative // prefix supported)
    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete the active workspace

    :return: Result of the operator call.
    """

def delete_all_others(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete all workspaces except this one

    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new workspace

    :return: Result of the operator call.
    """

def reorder_to_back(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reorder workspace to be last in the list

    :return: Result of the operator call.
    """

def reorder_to_front(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reorder workspace to be first in the list

    :return: Result of the operator call.
    """

def scene_pin_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remember the last used scene for the current workspace and switch to it whenever this workspace is activated again

    :return: Result of the operator call.
    """
