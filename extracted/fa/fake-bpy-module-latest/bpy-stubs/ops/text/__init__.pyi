import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_autocomplete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Show a list of used text in the open document

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_comment_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["TOGGLE", "COMMENT", "UNCOMMENT"] | None = "TOGGLE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param type: Type, Add or remove comments (optional)
        :return: Result of the operator call.
        """

class _CLS_convert_whitespace(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["SPACES", "TABS"] | None = "SPACES",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Convert whitespaces by type

        :param execution_context:
        :param undo:
        :param type: Type, Type of whitespace to convert to (optional)
        :return: Result of the operator call.
        """

class _CLS_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy selected text to clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_cursor_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        x: int | None = 0,
        y: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set cursor position

        :param execution_context:
        :param undo:
        :param x: X, (in [-inf, inf], optional)
        :param y: Y, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_cut(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Cut selected text to clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "NEXT_CHARACTER", "PREVIOUS_CHARACTER", "NEXT_WORD", "PREVIOUS_WORD"
        ]
        | None = "NEXT_CHARACTER",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete text by cursor position

        :param execution_context:
        :param undo:
        :param type: Type, Which part of the text to delete (optional)
        :return: Result of the operator call.
        """

class _CLS_duplicate_line(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate the current line

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_find(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Find specified text

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_find_set_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Find specified text and set as selected

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_indent(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Indent selected text

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_indent_or_autocomplete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Indent selected text or autocomplete

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_insert(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        text: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Insert text at cursor position

        :param execution_context:
        :param undo:
        :param text: Text, Text to insert at the cursor position (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_jump(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        line: int | None = 1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Jump cursor to line

        :param execution_context:
        :param undo:
        :param line: Line, Line number to jump to (in [1, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_jump_to_file_at_point(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        filepath: str = "",
        line: int | None = 0,
        column: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Jump to a file for the text editor

        :param execution_context:
        :param undo:
        :param filepath: Filepath, (optional, never None)
        :param line: Line, Line to jump to (in [0, inf], optional)
        :param column: Column, Column to jump to (in [0, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_line_break(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Insert line break at cursor position

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_line_number(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """The current line number

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_make_internal(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make active text file internal

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "LINE_BEGIN",
            "LINE_END",
            "FILE_TOP",
            "FILE_BOTTOM",
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

        :param execution_context:
        :param undo:
        :param type: Type, Where to move cursor to (optional)
        :return: Result of the operator call.
        """

class _CLS_move_lines(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "DOWN",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the currently selected line(s) up/down

        :param execution_context:
        :param undo:
        :param direction: Direction, (optional)
        :return: Result of the operator call.
        """

class _CLS_move_select(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "LINE_BEGIN",
            "LINE_END",
            "FILE_TOP",
            "FILE_BOTTOM",
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

        :param execution_context:
        :param undo:
        :param type: Type, Where to move cursor to, to make a selection (optional)
        :return: Result of the operator call.
        """

class _CLS_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new text data-block

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_open(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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
        filter_python: bool | None = True,
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
        relative_path: bool | None = True,
        display_type: typing.Literal[
            "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
        ]
        | None = "DEFAULT",
        sort_method: typing.Literal[
            "DEFAULT",
            "FILE_SORT_ALPHA",
            "FILE_SORT_EXTENSION",
            "FILE_SORT_TIME",
            "FILE_SORT_SIZE",
            "ASSET_CATALOG",
        ]
        | None = "",
        internal: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Open a new text data-block

                :param execution_context:
                :param undo:
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

        DEFAULT
        Default -- Automatically determine sort method for files.

        FILE_SORT_ALPHA
        Name -- Sort the file list alphabetically.

        FILE_SORT_EXTENSION
        Extension -- Sort the file list by extension/type.

        FILE_SORT_TIME
        Modified Date -- Sort files by modification time.

        FILE_SORT_SIZE
        Size -- Sort files by size.

        ASSET_CATALOG
        Asset Catalog -- Sort the asset list so that assets in the same catalog are kept together. Within a single catalog, assets are ordered by name. The catalogs are in order of the flattened catalog hierarchy..
                :param internal: Make Internal, Make text file internal after loading (optional)
                :return: Result of the operator call.
        """

class _CLS_overwrite_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle overwrite while typing

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_paste(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        selection: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste text from clipboard

        :param execution_context:
        :param undo:
        :param selection: Selection, Paste text selected elsewhere rather than copied (X11/Wayland only) (optional)
        :return: Result of the operator call.
        """

class _CLS_reload(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reload active text data-block from its file

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_replace(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        all: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Replace text with the specified text

        :param execution_context:
        :param undo:
        :param all: Replace All, Replace all occurrences (optional)
        :return: Result of the operator call.
        """

class _CLS_replace_set_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Replace text with specified text and set as selected

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_resolve_conflict(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        resolution: typing.Literal["IGNORE", "RELOAD", "SAVE", "MAKE_INTERNAL"]
        | None = "IGNORE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """When external text is out of sync, resolve the conflict

        :param execution_context:
        :param undo:
        :param resolution: Resolution, How to solve conflict due to differences in internal and external text (optional)
        :return: Result of the operator call.
        """

class _CLS_run_script(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Run active script

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_save(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Save active text data-block

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_save_as(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        filepath: str = "",
        hide_props_region: bool | None = True,
        check_existing: bool | None = True,
        filter_blender: bool | None = False,
        filter_backup: bool | None = False,
        filter_image: bool | None = False,
        filter_movie: bool | None = False,
        filter_python: bool | None = True,
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
        """Save active text file with options

                :param execution_context:
                :param undo:
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

class _CLS_scroll(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        lines: int | None = 1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param lines: Lines, Number of lines to scroll (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_scroll_bar(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        lines: int | None = 1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param lines: Lines, Number of lines to scroll (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_select_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select all text

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_line(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select text by line

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_word(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select word under cursor

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set text selection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_start_find(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Start searching text

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_to_3d_object(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        split_lines: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create 3D text object from active text data-block

        :param execution_context:
        :param undo:
        :param split_lines: Split Lines, Create one object per line in the text (optional)
        :return: Result of the operator call.
        """

class _CLS_unindent(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Unindent selected text

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_unlink(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Unlink active text data-block

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_update_shader(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Update users of this shader, such as custom cameras and script nodes, with its new sockets and options

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

autocomplete: _CLS_autocomplete

comment_toggle: _CLS_comment_toggle

convert_whitespace: _CLS_convert_whitespace

copy: _CLS_copy

cursor_set: _CLS_cursor_set

cut: _CLS_cut

delete: _CLS_delete

duplicate_line: _CLS_duplicate_line

find: _CLS_find

find_set_selected: _CLS_find_set_selected

indent: _CLS_indent

indent_or_autocomplete: _CLS_indent_or_autocomplete

insert: _CLS_insert

jump: _CLS_jump

jump_to_file_at_point: _CLS_jump_to_file_at_point

line_break: _CLS_line_break

line_number: _CLS_line_number

make_internal: _CLS_make_internal

move: _CLS_move

move_lines: _CLS_move_lines

move_select: _CLS_move_select

new: _CLS_new

open: _CLS_open

overwrite_toggle: _CLS_overwrite_toggle

paste: _CLS_paste

reload: _CLS_reload

replace: _CLS_replace

replace_set_selected: _CLS_replace_set_selected

resolve_conflict: _CLS_resolve_conflict

run_script: _CLS_run_script

save: _CLS_save

save_as: _CLS_save_as

scroll: _CLS_scroll

scroll_bar: _CLS_scroll_bar

select_all: _CLS_select_all

select_line: _CLS_select_line

select_word: _CLS_select_word

selection_set: _CLS_selection_set

start_find: _CLS_start_find

to_3d_object: _CLS_to_3d_object

unindent: _CLS_unindent

unlink: _CLS_unlink

update_shader: _CLS_update_shader
