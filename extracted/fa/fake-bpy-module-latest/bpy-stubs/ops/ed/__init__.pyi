import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def flush_edits(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Flush edit data from active editing modes

    :return: Result of the operator call.
    """

def lib_id_fake_user_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Save this data-block even if it has no users

    :return: Result of the operator call.
    """

def lib_id_generate_preview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create an automatic preview for the selected data-block

    :return: Result of the operator call.
    """

def lib_id_generate_preview_from_object(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a preview for this asset by rendering the active object

    :return: Result of the operator call.
    """

def lib_id_load_custom_preview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = True,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = False,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    show_multiview: bool | None = False,
    use_multiview: bool | None = False,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Choose an image to help identify the data-block visually

        :param filepath: File Path, Path to file (optional, never None)
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
        :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
        :param filter_blender: Filter .blend files, (optional)
        :param filter_backup: Filter backup .blend files, (optional)
        :param filter_image: Filter image files, (optional)
        :param filter_movie: Filter movie files, (optional)
        :param filter_python: Filter Python files, (optional)
        :param filter_font: Filter font files, (optional)
        :param filter_sound: Filter sound files, (optional)
        :param filter_text: Filter text files, (optional)
        :param filter_archive: Filter archive files, (optional)
        :param filter_btx: Filter btx files, (optional)
        :param filter_alembic: Filter Alembic files, (optional)
        :param filter_usd: Filter USD files, (optional)
        :param filter_obj: Filter OBJ files, (optional)
        :param filter_volume: Filter OpenVDB volume files, (optional)
        :param filter_folder: Filter folders, (optional)
        :param filter_blenlib: Filter Blender IDs, (optional)
        :param filemode: File Browser Mode, The setting for the file browser mode to load a .blend file, a library or a special file (in [1, 9], optional)
        :param show_multiview: Enable Multi-View, (optional)
        :param use_multiview: Use Multi-View, (optional)
        :param display_type: Display Type, (optional)

    DEFAULT
    Default -- Automatically determine display type for files.

    LIST_VERTICAL
    Short List -- Display files as short list.

    LIST_HORIZONTAL
    Long List -- Display files as a detailed list.

    THUMBNAIL
    Thumbnails -- Display files as thumbnails.
        :param sort_method: File sorting mode, (optional)
        :return: Result of the operator call.
    """

def lib_id_override_editable_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set if this library override data-block can be edited

    :return: Result of the operator call.
    """

def lib_id_remove_preview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the preview of this data-block

    :return: Result of the operator call.
    """

def lib_id_unlink(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove a usage of a data-block, clearing the assignment

    :return: Result of the operator call.
    """

def redo(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Redo previous action

    :return: Result of the operator call.
    """

def undo(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undo previous action

    :return: Result of the operator call.
    """

def undo_history(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    item: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undo or redo specific action in history

    :param item: Item, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def undo_push(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    message: str = "Add an undo step *function may be moved*",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an undo state (internal use only)

    :param message: Undo Message, (optional, never None)
    :return: Result of the operator call.
    """

def undo_redo(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undo and redo previous action

    :return: Result of the operator call.
    """
