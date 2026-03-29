import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def execute_preset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    menu_idname: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Load a preset

    :param filepath: filepath, (optional, never None)
    :param menu_idname: Menu ID Name, ID name of the menu this was called from (optional, never None)
    :return: Result of the operator call.
    """

def python_file_run(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Run Python file

    :param filepath: Path, (optional, never None)
    :return: Result of the operator call.
    """

def reload(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reload scripts

    :return: Result of the operator call.
    """
