import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def create(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create an object collection from selected objects

    :param name: Name, Name of the new collection (optional, never None)
    :return: Result of the operator call.
    """

def export_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Invoke all configured exporters on this collection

    :return: Result of the operator call.
    """

def exporter_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add exporter to the exporter list

    :param name: Name, FileHandler idname (optional, never None)
    :return: Result of the operator call.
    """

def exporter_export(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Invoke the export operation

    :param index: Index, Exporter index (in [0, inf], optional)
    :return: Result of the operator call.
    """

def exporter_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move exporter up or down in the exporter list

    :param direction: Direction, Direction to move the active exporter (optional)
    :return: Result of the operator call.
    """

def exporter_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove exporter from the exporter list

    :param index: Index, Exporter index (in [0, inf], optional)
    :return: Result of the operator call.
    """

def objects_add_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add selected objects to one of the collections the active-object is part of. Optionally add to "All Collections" to ensure selected objects are included in the same collections as the active object

    :param collection: Collection, The collection to add other selected objects to (optional)
    :return: Result of the operator call.
    """

def objects_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected objects from a collection

    :param collection: Collection, The collection to remove this object from (optional)
    :return: Result of the operator call.
    """

def objects_remove_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the object from an object collection that contains the active object

    :param collection: Collection, The collection to remove other selected objects from (optional)
    :return: Result of the operator call.
    """

def objects_remove_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected objects from all collections

    :return: Result of the operator call.
    """
