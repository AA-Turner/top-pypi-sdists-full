import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def actionzone(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    modifier: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Handle area action zones for mouse actions/gestures

    :param modifier: Modifier, Modifier state (in [0, 2], optional)
    :return: Result of the operator call.
    """

def animation_cancel(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    restore_frame: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cancel animation, returning to the original frame

    :param restore_frame: Restore Frame, Restore the frame when animation was initialized (optional)
    :return: Result of the operator call.
    """

def animation_play(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    reverse: bool | None = False,
    sync: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Play animation

    :param reverse: Play in Reverse, Animation is played backwards (optional)
    :param sync: Sync, Drop frames to maintain framerate (optional)
    :return: Result of the operator call.
    """

def animation_step(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Step through animation by position

    :return: Result of the operator call.
    """

def area_close(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Close selected area

    :return: Result of the operator call.
    """

def area_dupli(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected area into new window

    :return: Result of the operator call.
    """

def area_join(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    source_xy: collections.abc.Sequence[int] | None = (0, 0),
    target_xy: collections.abc.Sequence[int] | None = (0, 0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Join selected areas into new window

    :param source_xy: Source location, (array of 2 items, in [-inf, inf], optional)
    :param target_xy: Target location, (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def area_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    x: int | None = 0,
    y: int | None = 0,
    delta: int | None = 0,
    snap: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move selected area edges

    :param x: X, (in [-inf, inf], optional)
    :param y: Y, (in [-inf, inf], optional)
    :param delta: Delta, (in [-inf, inf], optional)
    :param snap: Snapping, Enable snapping (optional)
    :return: Result of the operator call.
    """

def area_options(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Operations for splitting and merging

    :return: Result of the operator call.
    """

def area_split(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["HORIZONTAL", "VERTICAL"] | None = "HORIZONTAL",
    factor: float | None = 0.5,
    cursor: collections.abc.Sequence[int] | None = (0, 0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split selected area into new windows

    :param direction: Direction, (optional)
    :param factor: Factor, (in [0, 1], optional)
    :param cursor: Cursor, (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def area_swap(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    cursor: collections.abc.Sequence[int] | None = (0, 0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap selected areas screen positions

    :param cursor: Cursor, (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def back_to_previous(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Revert back to the original screen layout, before fullscreen area overlay

    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete active screen

    :return: Result of the operator call.
    """

def drivers_editor_show(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show drivers editor in a separate window

    :return: Result of the operator call.
    """

def frame_jump(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    end: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Jump to first/last frame in frame range

    :param end: Last Frame, Jump to the last frame of the frame range (optional)
    :return: Result of the operator call.
    """

def frame_offset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    delta: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move current frame forward/backward by a given number

    :param delta: Delta, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def header_toggle_menus(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Expand or collapse the header pull-down menus

    :return: Result of the operator call.
    """

def info_log_show(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show info log in a separate window

    :return: Result of the operator call.
    """

def keyframe_jump(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    next: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Jump to previous/next keyframe

    :param next: Next Keyframe, (optional)
    :return: Result of the operator call.
    """

def marker_jump(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    next: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Jump to previous/next marker

    :param next: Next Marker, (optional)
    :return: Result of the operator call.
    """

def new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new screen

    :return: Result of the operator call.
    """

def quadview_size(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Resize Quad View areas

    :return: Result of the operator call.
    """

def redo_last(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Display parameters for last action performed

    :return: Result of the operator call.
    """

def region_blend(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Blend in and out overlapping region

    :return: Result of the operator call.
    """

def region_context_menu(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Display region context menu

    :return: Result of the operator call.
    """

def region_flip(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle the regions alignment (left/right or top/bottom)

    :return: Result of the operator call.
    """

def region_quadview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split selected area into camera, front, right, and top views

    :return: Result of the operator call.
    """

def region_scale(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Scale selected area

    :return: Result of the operator call.
    """

def region_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    region_type: Literal[bpy.stub_internal.rna_enums.RegionTypeItems] | None = "WINDOW",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide or unhide the region

    :param region_type: Region Type, Type of the region to toggle (optional)
    :return: Result of the operator call.
    """

def repeat_history(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Display menu for previous actions performed

    :param index: Index, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def repeat_last(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Repeat last action

    :return: Result of the operator call.
    """

def screen_full_area(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_hide_panels: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle display selected area as fullscreen/maximized

    :param use_hide_panels: Hide Panels, Hide all the panels (Focus Mode) (optional)
    :return: Result of the operator call.
    """

def screen_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    delta: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cycle through available screens

    :param delta: Delta, (in [-1, 1], optional)
    :return: Result of the operator call.
    """

def screenshot(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Capture a picture of the whole Blender window

        :param filepath: File Path, Path to file (optional, never None)
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
        :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
        :param filter_blender: Filter .blend files, (optional)
        :param filter_backup: Filter .blend files, (optional)
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

def screenshot_area(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Capture a picture of an editor

        :param filepath: File Path, Path to file (optional, never None)
        :param hide_props_region: Hide Operator Properties, Collapse the region displaying the operator settings (optional)
        :param check_existing: Check Existing, Check and warn on overwriting existing files (optional)
        :param filter_blender: Filter .blend files, (optional)
        :param filter_backup: Filter .blend files, (optional)
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

def space_context_cycle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["PREV", "NEXT"] | None = "NEXT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cycle through the editor context by activating the next/previous one

    :param direction: Direction, Direction to cycle through (optional)
    :return: Result of the operator call.
    """

def space_type_set_or_cycle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    space_type: Literal[bpy.stub_internal.rna_enums.SpaceTypeItems] | None = "EMPTY",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the space type or cycle subtype

    :param space_type: Type, (optional)
    :return: Result of the operator call.
    """

def spacedata_cleanup(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove unused settings for invisible editors

    :return: Result of the operator call.
    """

def time_jump(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    backward: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Jump forward/backward by a given number of frames or seconds

    :param backward: Backwards, Jump backwards in time (optional)
    :return: Result of the operator call.
    """

def userpref_show(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    section: Literal[bpy.stub_internal.rna_enums.PreferenceSectionItems]
    | None = "INTERFACE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Edit user preferences and system settings

    :param section: Section to activate in the Preferences (optional)
    :return: Result of the operator call.
    """

def workspace_cycle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["PREV", "NEXT"] | None = "NEXT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cycle through workspaces

    :param direction: Direction, Direction to cycle through (optional)
    :return: Result of the operator call.
    """
