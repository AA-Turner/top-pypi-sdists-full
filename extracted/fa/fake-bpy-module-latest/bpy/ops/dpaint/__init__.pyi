import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def bake(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake dynamic paint image sequence surface

    :return: Result of the operator call.
    """

def output_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    output: typing.Literal["A", "B"] | None = "A",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove Dynamic Paint output data layer

    :param output: Output Toggle, (optional)
    :return: Result of the operator call.
    """

def surface_slot_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new Dynamic Paint surface slot

    :return: Result of the operator call.
    """

def surface_slot_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the selected surface slot

    :return: Result of the operator call.
    """

def type_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: Literal[bpy.stub_internal.rna_enums.PropDynamicpaintTypeItems]
    | None = "CANVAS",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle whether given type is active or not

    :param type: Type, (optional)
    :return: Result of the operator call.
    """
