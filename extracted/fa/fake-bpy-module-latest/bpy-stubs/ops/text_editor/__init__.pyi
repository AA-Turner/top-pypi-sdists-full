import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove a Text Editor Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """
