import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def case_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    case: typing.Literal["LOWER", "UPPER"] | None = "LOWER",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set font case

    :param case: Case, Lower or upper case (optional)
    :return: Result of the operator call.
    """

def case_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle font case

    :return: Result of the operator call.
    """

def change_character(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    delta: int | None = 1,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change font character code

    :param delta: Delta, Number to increase or decrease character code with (in [-255, 255], optional)
    :return: Result of the operator call.
    """

def change_spacing(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    delta: float | None = 1.0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change font spacing

    :param delta: Delta, Amount to decrease or increase character spacing with (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "NEXT_CHARACTER",
        "PREVIOUS_CHARACTER",
        "NEXT_WORD",
        "PREVIOUS_WORD",
        "SELECTION",
        "NEXT_OR_SELECTION",
        "PREVIOUS_OR_SELECTION",
    ]
    | None = "PREVIOUS_CHARACTER",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete text by cursor position

    :param type: Type, Which part of the text to delete (optional)
    :return: Result of the operator call.
    """

def line_break(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert line break at cursor position

    :return: Result of the operator call.
    """

def move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "LINE_BEGIN",
        "LINE_END",
        "TEXT_BEGIN",
        "TEXT_END",
        "PREVIOUS_CHARACTER",
        "NEXT_CHARACTER",
        "PREVIOUS_WORD",
        "NEXT_WORD",
        "PREVIOUS_LINE",
        "NEXT_LINE",
        "PREVIOUS_PAGE",
        "NEXT_PAGE",
    ]
    | None = "LINE_BEGIN",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move cursor to position type

    :param type: Type, Where to move cursor to (optional)
    :return: Result of the operator call.
    """

def move_select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "LINE_BEGIN",
        "LINE_END",
        "TEXT_BEGIN",
        "TEXT_END",
        "PREVIOUS_CHARACTER",
        "NEXT_CHARACTER",
        "PREVIOUS_WORD",
        "NEXT_WORD",
        "PREVIOUS_LINE",
        "NEXT_LINE",
        "PREVIOUS_PAGE",
        "NEXT_PAGE",
    ]
    | None = "LINE_BEGIN",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the cursor while selecting

    :param type: Type, Where to move cursor to, to make a selection (optional)
    :return: Result of the operator call.
    """

def open(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = True,
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
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "THUMBNAIL",
    sort_method: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Load a new font from a file

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
        :param relative_path: Relative Path, Select the file relative to the blend file (optional)
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

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all text

    :return: Result of the operator call.
    """

def select_word(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select word under cursor

    :return: Result of the operator call.
    """

def selection_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set cursor selection

    :return: Result of the operator call.
    """

def style_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    style: typing.Literal["BOLD", "ITALIC", "UNDERLINE", "SMALL_CAPS"] | None = "BOLD",
    clear: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set font style

    :param style: Style, Style to set selection to (optional)
    :param clear: Clear, Clear style rather than setting it (optional)
    :return: Result of the operator call.
    """

def style_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    style: typing.Literal["BOLD", "ITALIC", "UNDERLINE", "SMALL_CAPS"] | None = "BOLD",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle font style

    :param style: Style, Style to set selection to (optional)
    :return: Result of the operator call.
    """

def text_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy selected text to clipboard

    :return: Result of the operator call.
    """

def text_cut(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cut selected text to clipboard

    :return: Result of the operator call.
    """

def text_insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    text: str = "",
    accent: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert text at cursor position

    :param text: Text, Text to insert at the cursor position (optional, never None)
    :param accent: Accent Mode, Next typed character will strike through previous, for special character input (optional)
    :return: Result of the operator call.
    """

def text_insert_unicode(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert Unicode Character

    :return: Result of the operator call.
    """

def text_paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    selection: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste text from clipboard

    :param selection: Selection, Paste text selected elsewhere rather than copied (X11/Wayland only) (optional)
    :return: Result of the operator call.
    """

def text_paste_from_file(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = False,
    filter_text: bool | None = True,
    filter_archive: bool | None = False,
    filter_btx: bool | None = False,
    filter_alembic: bool | None = False,
    filter_usd: bool | None = False,
    filter_obj: bool | None = False,
    filter_volume: bool | None = False,
    filter_folder: bool | None = True,
    filter_blenlib: bool | None = False,
    filemode: int | None = 9,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste contents from file

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

def textbox_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new text box

    :return: Result of the operator call.
    """

def textbox_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the text box

    :param index: Index, The current text box (in [0, inf], optional)
    :return: Result of the operator call.
    """

def unlink(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unlink active font data-block

    :return: Result of the operator call.
    """
