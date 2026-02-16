import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def entry_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    list_path: str | None = "",
    active_index_path: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an entry to the list after the current active item

    :param list_path: list_path, (optional, never None)
    :param active_index_path: active_index_path, (optional, never None)
    :return: Result of the operator call.
    """

def entry_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    list_path: str | None = "",
    active_index_path: str | None = "",
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move an entry in the list up or down

        :param list_path: list_path, (optional, never None)
        :param active_index_path: active_index_path, (optional, never None)
        :param direction: Direction, (optional)

    UP
    UP -- UP.

    DOWN
    DOWN -- DOWN.
        :return: Result of the operator call.
    """

def entry_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    list_path: str | None = "",
    active_index_path: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the selected entry from the list

    :param list_path: list_path, (optional, never None)
    :param active_index_path: active_index_path, (optional, never None)
    :return: Result of the operator call.
    """
