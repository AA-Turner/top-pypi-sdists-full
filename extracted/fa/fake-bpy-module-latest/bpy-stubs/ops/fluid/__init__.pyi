import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def bake_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Entire Fluid Simulation

    :return: Result of the operator call.
    """

def bake_data(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Fluid Data

    :return: Result of the operator call.
    """

def bake_guides(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Fluid Guiding

    :return: Result of the operator call.
    """

def bake_mesh(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Fluid Mesh

    :return: Result of the operator call.
    """

def bake_noise(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Fluid Noise

    :return: Result of the operator call.
    """

def bake_particles(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Fluid Particles

    :return: Result of the operator call.
    """

def free_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Free Entire Fluid Simulation

    :return: Result of the operator call.
    """

def free_data(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Free Fluid Data

    :return: Result of the operator call.
    """

def free_guides(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Free Fluid Guiding

    :return: Result of the operator call.
    """

def free_mesh(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Free Fluid Mesh

    :return: Result of the operator call.
    """

def free_noise(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Free Fluid Noise

    :return: Result of the operator call.
    """

def free_particles(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Free Fluid Particles

    :return: Result of the operator call.
    """

def pause_bake(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Pause Bake

    :return: Result of the operator call.
    """

def preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove a Fluid Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """
