import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new cache

    :return: Result of the operator call.
    """

def bake(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    bake: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake physics

    :param bake: Bake, (optional)
    :return: Result of the operator call.
    """

def bake_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    bake: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake all physics simulations in the current scene

    :param bake: Bake, (optional)
    :return: Result of the operator call.
    """

def bake_from_cache(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake from cache

    :return: Result of the operator call.
    """

def free_bake(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete physics bake

    :return: Result of the operator call.
    """

def free_bake_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete all baked caches of all objects in the current scene

    :return: Result of the operator call.
    """

def remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete current cache

    :return: Result of the operator call.
    """
