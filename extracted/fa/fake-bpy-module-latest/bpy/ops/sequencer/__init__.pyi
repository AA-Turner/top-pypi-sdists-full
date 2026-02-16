import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums
import mathutils

def add_scene_strip_from_scene_asset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    asset_library_type: Literal[bpy.stub_internal.rna_enums.AssetLibraryTypeItems]
    | None = "LOCAL",
    asset_library_identifier: str | None = "",
    relative_asset_identifier: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a strip using a duplicate of this scene asset as the source

    :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
    :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
    :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
    :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
    :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
    :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
    :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
    :param asset_library_type: Asset Library Type, (optional)
    :param asset_library_identifier: Asset Library Identifier, (optional, never None)
    :param relative_asset_identifier: Relative Asset Identifier, (optional, never None)
    :return: Result of the operator call.
    """

def box_blade(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
    type: typing.Literal["SOFT", "HARD"] | None = "SOFT",
    ignore_selection: bool | None = True,
    ignore_connections: bool | None = False,
    remove_gaps: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Draw a box around the parts of strips you want to cut away

        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :param type: Type, The type of split operation to perform on strips (optional)
        :param ignore_selection: Ignore Selection, In box blade mode, make cuts to all strips, even if they are not selected (optional)
        :param ignore_connections: Ignore Connections, Dont propagate split to connected strips (optional)
        :param remove_gaps: Remove Gaps, In box blade mode, close gaps between cut strips, rippling later strips on the same channel (optional)
        :return: Result of the operator call.
    """

def change_effect_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "CROSS",
        "ADD",
        "SUBTRACT",
        "ALPHA_OVER",
        "ALPHA_UNDER",
        "GAMMA_CROSS",
        "MULTIPLY",
        "WIPE",
        "GLOW",
        "COLOR",
        "SPEED",
        "MULTICAM",
        "ADJUSTMENT",
        "GAUSSIAN_BLUR",
        "TEXT",
        "COLORMIX",
    ]
    | None = "CROSS",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Replace effect strip with another that takes the same number of inputs

        :param type: Type, Strip effect type (optional)

    CROSS
    Crossfade -- Fade out of one video, fading into another.

    ADD
    Add -- Add together color channels from two videos.

    SUBTRACT
    Subtract -- Subtract one strips color from another.

    ALPHA_OVER
    Alpha Over -- Blend alpha on top of another video.

    ALPHA_UNDER
    Alpha Under -- Blend alpha below another video.

    GAMMA_CROSS
    Gamma Crossfade -- Crossfade with color correction.

    MULTIPLY
    Multiply -- Multiply color channels from two videos.

    WIPE
    Wipe -- Sweep a transition line across the frame.

    GLOW
    Glow -- Add blur and brightness to light areas.

    COLOR
    Color -- Add a simple color strip.

    SPEED
    Speed -- Timewarp video strips, modifying playback speed.

    MULTICAM
    Multicam Selector -- Control active camera angles.

    ADJUSTMENT
    Adjustment Layer -- Apply nondestructive effects.

    GAUSSIAN_BLUR
    Gaussian Blur -- Soften details along axes.

    TEXT
    Text -- Add a simple text strip.

    COLORMIX
    Color Mix -- Combine two strips using blend modes.
        :return: Result of the operator call.
    """

def change_path(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    directory: str | None = "",
    files=None,
    hide_props_region: bool | None = True,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
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
    relative_path: bool | None = True,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: str | None = "",
    use_placeholders: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

        :param filepath: File Path, Path to file (optional, never None)
        :param directory: Directory, Directory of the file (optional, never None)
        :param files: Files, (optional)
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
        :param use_placeholders: Use Placeholders, Use placeholders for missing frames of the strip (optional)
        :return: Result of the operator call.
    """

def change_scene(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    scene: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change Scene assigned to Strip

    :param scene: Scene, (optional)
    :return: Result of the operator call.
    """

def connect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    toggle: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Link selected strips together for simplified group selection

    :param toggle: Toggle, Toggle strip connections (optional)
    :return: Result of the operator call.
    """

def copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected strips to the internal clipboard

    :return: Result of the operator call.
    """

def crossfade_sounds(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Do cross-fading volume animation of two selected sound strips

    :return: Result of the operator call.
    """

def cursor_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set 2D cursor location

    :param location: Location, Cursor location in normalized preview coordinates (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def deinterlace_selected_movies(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deinterlace all selected movie sources

    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    delete_data: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected strips from the sequencer

    :param delete_data: Delete Data, After removing the Strip, delete the associated data also (optional)
    :return: Result of the operator call.
    """

def disconnect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unlink selected strips so that they can be selected individually

    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    linked: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate the selected strips

    :param linked: Linked, Duplicate strip but not strip data, linking to the original data (optional)
    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    SEQUENCER_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_seq_slide: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected strips and move them

    :param SEQUENCER_OT_duplicate: Duplicate Strips, Duplicate the selected strips (optional, `bpy.ops.sequencer.duplicate` keyword arguments)
    :param TRANSFORM_OT_seq_slide: Sequence Slide, Slide a sequence strip in time (optional, `bpy.ops.transform.seq_slide` keyword arguments)
    :return: Result of the operator call.
    """

def duplicate_move_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    SEQUENCER_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_seq_slide: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected strips, but not their data, and move them

    :param SEQUENCER_OT_duplicate: Duplicate Strips, Duplicate the selected strips (optional, `bpy.ops.sequencer.duplicate` keyword arguments)
    :param TRANSFORM_OT_seq_slide: Sequence Slide, Slide a sequence strip in time (optional, `bpy.ops.transform.seq_slide` keyword arguments)
    :return: Result of the operator call.
    """

def effect_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "CROSS",
        "ADD",
        "SUBTRACT",
        "ALPHA_OVER",
        "ALPHA_UNDER",
        "GAMMA_CROSS",
        "MULTIPLY",
        "WIPE",
        "GLOW",
        "COLOR",
        "SPEED",
        "MULTICAM",
        "ADJUSTMENT",
        "GAUSSIAN_BLUR",
        "TEXT",
        "COLORMIX",
    ]
    | None = "CROSS",
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    length: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    color: collections.abc.Sequence[float] | mathutils.Color | None = (0.0, 0.0, 0.0),
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an effect to the sequencer, most are applied on top of existing strips

        :param type: Type, Sequencer effect type (optional)

    CROSS
    Crossfade -- Fade out of one video, fading into another.

    ADD
    Add -- Add together color channels from two videos.

    SUBTRACT
    Subtract -- Subtract one strips color from another.

    ALPHA_OVER
    Alpha Over -- Blend alpha on top of another video.

    ALPHA_UNDER
    Alpha Under -- Blend alpha below another video.

    GAMMA_CROSS
    Gamma Crossfade -- Crossfade with color correction.

    MULTIPLY
    Multiply -- Multiply color channels from two videos.

    WIPE
    Wipe -- Sweep a transition line across the frame.

    GLOW
    Glow -- Add blur and brightness to light areas.

    COLOR
    Color -- Add a simple color strip.

    SPEED
    Speed -- Timewarp video strips, modifying playback speed.

    MULTICAM
    Multicam Selector -- Control active camera angles.

    ADJUSTMENT
    Adjustment Layer -- Apply nondestructive effects.

    GAUSSIAN_BLUR
    Gaussian Blur -- Soften details along axes.

    TEXT
    Text -- Add a simple text strip.

    COLORMIX
    Color Mix -- Combine two strips using blend modes.
        :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
        :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
        :param length: Length, Length of the strip in frames, or the length of each strip if multiple are added (in [-inf, inf], optional)
        :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
        :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
        :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
        :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
        :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
        :param color: Color, Initialize the strip with this color (array of 3 items, in [0, 1], optional)
        :return: Result of the operator call.
    """

def enable_proxies(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    proxy_25: bool | None = False,
    proxy_50: bool | None = False,
    proxy_75: bool | None = False,
    proxy_100: bool | None = False,
    overwrite: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enable selected proxies on all selected Movie and Image strips

    :param proxy_25: 25%, (optional)
    :param proxy_50: 50%, (optional)
    :param proxy_75: 75%, (optional)
    :param proxy_100: 100%, (optional)
    :param overwrite: Overwrite, (optional)
    :return: Result of the operator call.
    """

def export_subtitles(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    hide_props_region: bool | None = True,
    check_existing: bool | None = True,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
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
    filemode: int | None = 8,
    display_type: typing.Literal[
        "DEFAULT", "LIST_VERTICAL", "LIST_HORIZONTAL", "THUMBNAIL"
    ]
    | None = "DEFAULT",
    sort_method: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Export .srt file containing text strips

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

def fades_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    duration_seconds: float | None = 1.0,
    type: typing.Literal["IN_OUT", "IN", "OUT", "CURSOR_FROM", "CURSOR_TO"]
    | None = "IN_OUT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Adds or updates a fade animation for either visual or audio strips

        :param duration_seconds: Fade Duration, Duration of the fade in seconds (in [0.01, inf], optional)
        :param type: Fade Type, Fade in, out, both in and out, to, or from the current frame. Default is both in and out (optional)

    IN_OUT
    Fade In and Out -- Fade selected strips in and out.

    IN
    Fade In -- Fade in selected strips.

    OUT
    Fade Out -- Fade out selected strips.

    CURSOR_FROM
    From Current Frame -- Fade from the time cursor to the end of overlapping strips.

    CURSOR_TO
    To Current Frame -- Fade from the start of strips under the time cursor to the current frame.
        :return: Result of the operator call.
    """

def fades_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Removes fade animation from selected strips

    :return: Result of the operator call.
    """

def gap_insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frames: int | None = 10,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert gap at current frame to first strips at the right, independent of selection or locked state of strips

    :param frames: Frames, Frames to insert after current strip (in [0, inf], optional)
    :return: Result of the operator call.
    """

def gap_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove gap at current frame to first strip at the right, independent of selection or locked state of strips

    :param all: All Gaps, Do all gaps to right of current frame (optional)
    :return: Result of the operator call.
    """

def image_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    directory: str | None = "",
    files=None,
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
    relative_path: bool | None = True,
    show_multiview: bool | None = False,
    use_multiview: bool | None = False,
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
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    length: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    fit_method: Literal[bpy.stub_internal.rna_enums.StripScaleMethodItems]
    | None = "FIT",
    set_view_transform: bool | None = True,
    image_import_type: typing.Literal["DETECT", "SEQUENCE", "INDIVIDUAL"]
    | None = "DETECT",
    use_sequence_detection: bool | None = True,
    use_placeholders: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an image or image sequence to the sequencer

        :param directory: Directory, Directory of the file (optional, never None)
        :param files: Files, (optional)
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
        :param relative_path: Relative Path, Select the file relative to the blend file (optional)
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
        :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
        :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
        :param length: Length, Length of the strip in frames, or the length of each strip if multiple are added (in [-inf, inf], optional)
        :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
        :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
        :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
        :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
        :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
        :param fit_method: Fit Method, Mode for fitting the image to the canvas (optional)
        :param set_view_transform: Set View Transform, Set appropriate view transform based on media color space (optional)
        :param image_import_type: Import As, Mode for importing selected images (optional)

    DETECT
    Auto Detect -- Add images as individual strips, unless their filenames match Blenders numbered sequence pattern, in which case they are grouped into a single image sequence.

    SEQUENCE
    Image Sequence -- Import all selected images as a single image sequence. The sequence of images does not have to match Blenders numbered sequence pattern, so placeholders cannot be inferred.

    INDIVIDUAL
    Individual Images -- Add each selected image as an individual strip.
        :param use_sequence_detection: Detect Sequences, Automatically detect animated sequences in selected images (based on file names) (optional)
        :param use_placeholders: Use Placeholders, Reserve placeholder frames for missing frames of the image sequence (optional)
        :return: Result of the operator call.
    """

def images_separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    length: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """On image sequence strips, it returns a strip for each image

    :param length: Length, Length of each frame (in [1, inf], optional)
    :return: Result of the operator call.
    """

def lock(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock strips so they cannot be transformed

    :return: Result of the operator call.
    """

def mask_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    mask: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a mask strip to the sequencer

    :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
    :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
    :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
    :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
    :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
    :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
    :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
    :param mask: Mask, (optional)
    :return: Result of the operator call.
    """

def meta_make(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Group selected strips into a meta-strip

    :return: Result of the operator call.
    """

def meta_separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Put the contents of a meta-strip back in the sequencer

    :return: Result of the operator call.
    """

def meta_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle a meta-strip (to edit enclosed strips)

    :return: Result of the operator call.
    """

def movie_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    directory: str | None = "",
    files=None,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = True,
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
    relative_path: bool | None = True,
    show_multiview: bool | None = False,
    use_multiview: bool | None = False,
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
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    fit_method: Literal[bpy.stub_internal.rna_enums.StripScaleMethodItems]
    | None = "FIT",
    set_view_transform: bool | None = True,
    adjust_playback_rate: bool | None = True,
    sound: bool | None = True,
    use_framerate: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a movie strip to the sequencer

        :param filepath: File Path, Path to file (optional, never None)
        :param directory: Directory, Directory of the file (optional, never None)
        :param files: Files, (optional)
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
        :param relative_path: Relative Path, Select the file relative to the blend file (optional)
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
        :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
        :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
        :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
        :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
        :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
        :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
        :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
        :param fit_method: Fit Method, Mode for fitting the image to the canvas (optional)
        :param set_view_transform: Set View Transform, Set appropriate view transform based on media color space (optional)
        :param adjust_playback_rate: Adjust Playback Rate, Play at normal speed regardless of scene FPS (optional)
        :param sound: Sound, Load sound with the movie (optional)
        :param use_framerate: Set Scene Frame Rate, Set frame rate of the current scene to the frame rate of the movie (optional)
        :return: Result of the operator call.
    """

def movieclip_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    clip: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a movieclip strip to the sequencer

    :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
    :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
    :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
    :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
    :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
    :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
    :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
    :param clip: Clip, (optional)
    :return: Result of the operator call.
    """

def mute(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mute (un)selected strips

    :param unselected: Unselected, Mute unselected rather than selected strips (optional)
    :return: Result of the operator call.
    """

def offset_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear strip in/out offsets from the start and end of content

    :return: Result of the operator call.
    """

def paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    keep_offset: bool | None = False,
    x: int | None = 0,
    y: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste strips from the internal clipboard

    :param keep_offset: Keep Offset, Keep strip offset relative to the current frame when pasting (optional)
    :param x: X, (in [-inf, inf], optional)
    :param y: Y, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def preview_duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    SEQUENCER_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected strips and move them

    :param SEQUENCER_OT_duplicate: Duplicate Strips, Duplicate the selected strips (optional, `bpy.ops.sequencer.duplicate` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def preview_duplicate_move_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    SEQUENCER_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected strips, but not their data, and move them

    :param SEQUENCER_OT_duplicate: Duplicate Strips, Duplicate the selected strips (optional, `bpy.ops.sequencer.duplicate` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def reassign_inputs(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reassign the inputs for the effect strip

    :return: Result of the operator call.
    """

def rebuild_proxy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rebuild all selected proxies and timecode indices

    :return: Result of the operator call.
    """

def refresh_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Refresh the sequencer editor

    :return: Result of the operator call.
    """

def reload(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    adjust_length: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reload strips in the sequencer

    :param adjust_length: Adjust Length, Adjust length of strips to their data length (optional)
    :return: Result of the operator call.
    """

def rename_channel(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def rendersize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set render size and aspect from active strip

    :return: Result of the operator call.
    """

def retiming_add_freeze_frame_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    SEQUENCER_OT_retiming_freeze_frame_add: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_seq_slide: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add freeze frame and move it

    :param SEQUENCER_OT_retiming_freeze_frame_add: Add Freeze Frame, Add freeze frame (optional, `bpy.ops.sequencer.retiming_freeze_frame_add` keyword arguments)
    :param TRANSFORM_OT_seq_slide: Sequence Slide, Slide a sequence strip in time (optional, `bpy.ops.transform.seq_slide` keyword arguments)
    :return: Result of the operator call.
    """

def retiming_add_transition_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    SEQUENCER_OT_retiming_transition_add: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_seq_slide: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add smooth transition between 2 retimed segments and change its duration

    :param SEQUENCER_OT_retiming_transition_add: Add Speed Transition, Add smooth transition between 2 retimed segments (optional, `bpy.ops.sequencer.retiming_transition_add` keyword arguments)
    :param TRANSFORM_OT_seq_slide: Sequence Slide, Slide a sequence strip in time (optional, `bpy.ops.transform.seq_slide` keyword arguments)
    :return: Result of the operator call.
    """

def retiming_freeze_frame_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    duration: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add freeze frame

    :param duration: Duration, Duration of freeze frame segment (in [0, inf], optional)
    :return: Result of the operator call.
    """

def retiming_key_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    timeline_frame: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add retiming Key

    :param timeline_frame: Timeline Frame, Frame where key will be added (in [0, inf], optional)
    :return: Result of the operator call.
    """

def retiming_key_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected retiming keys from the sequencer

    :return: Result of the operator call.
    """

def retiming_reset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset strip retiming

    :return: Result of the operator call.
    """

def retiming_segment_speed_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    speed: float | None = 100.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set speed of retimed segment

    :param speed: Speed, New speed of retimed segment (in [0.001, inf], optional)
    :return: Result of the operator call.
    """

def retiming_show(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show retiming keys in selected strips

    :return: Result of the operator call.
    """

def retiming_transition_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    duration: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add smooth transition between 2 retimed segments

    :param duration: Duration, Duration of freeze frame segment (in [0, inf], optional)
    :return: Result of the operator call.
    """

def sample(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    size: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use mouse to sample color in current frame

    :param size: Sample Size, (in [1, 128], optional)
    :return: Result of the operator call.
    """

def scene_frame_range_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update frame range of scene strip

    :return: Result of the operator call.
    """

def scene_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    scene: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a strip re-using this scene as the source

    :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
    :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
    :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
    :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
    :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
    :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
    :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
    :param scene: Scene, (optional)
    :return: Result of the operator call.
    """

def scene_strip_add_new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    type: typing.Literal["NEW", "EMPTY", "LINK_COPY", "FULL_COPY"] | None = "NEW",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a strip using a new scene as the source

        :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
        :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
        :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
        :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
        :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
        :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
        :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
        :param type: Type, (optional)

    NEW
    New -- Add new Strip with a new empty Scene with default settings.

    EMPTY
    Copy Settings -- Add a new Strip, with an empty scene, and copy settings from the current scene.

    LINK_COPY
    Linked Copy -- Add a Strip and link in the collections from the current scene (shallow copy).

    FULL_COPY
    Full Copy -- Add a Strip and make a full copy of the current scene.
        :return: Result of the operator call.
    """

def select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    wait_to_deselect_others: bool | None = False,
    use_select_on_click: bool | None = False,
    mouse_x: int | None = 0,
    mouse_y: int | None = 0,
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
    deselect_all: bool | None = False,
    select_passthrough: bool | None = False,
    center: bool | None = False,
    linked_handle: bool | None = False,
    linked_time: bool | None = False,
    side_of_frame: bool | None = False,
    ignore_connections: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select a strip (last selected becomes the "active strip")

    :param wait_to_deselect_others: Wait to Deselect Others, (optional)
    :param use_select_on_click: Act on Click, Instead of selecting on mouse press, wait to see if theres drag event. Otherwise select on mouse release (optional)
    :param mouse_x: Mouse X, (in [-inf, inf], optional)
    :param mouse_y: Mouse Y, (in [-inf, inf], optional)
    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :param deselect: Deselect, Remove from selection (optional)
    :param toggle: Toggle Selection, Toggle the selection (optional)
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
    :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected (optional)
    :param center: Center, Use the object center when selecting, in edit mode used to extend object selection (optional)
    :param linked_handle: Linked Handle, Select handles next to the active strip (optional)
    :param linked_time: Linked Time, Select other strips or handles at the same time, or all retiming keys after the current in retiming mode (optional)
    :param side_of_frame: Side of Frame, Select all strips on same side of the current frame as the mouse cursor (optional)
    :param ignore_connections: Ignore Connections, Select strips individually whether or not they are connected (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select or deselect all strips

        :param action: Action, Selection action to execute (optional)

    TOGGLE
    Toggle -- Toggle selection for all elements.

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.

    INVERT
    Invert -- Invert selection of all elements.
        :return: Result of the operator call.
    """

def select_box(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
    tweak: bool | None = False,
    include_handles: bool | None = False,
    ignore_connections: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select strips using box selection

        :param xmin: X Min, (in [-inf, inf], optional)
        :param xmax: X Max, (in [-inf, inf], optional)
        :param ymin: Y Min, (in [-inf, inf], optional)
        :param ymax: Y Max, (in [-inf, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :param tweak: Tweak, Make box select pass through to sequence slide when the cursor is hovering on a strip (optional)
        :param include_handles: Select Handles, Select the strips and their handles (optional)
        :param ignore_connections: Ignore Connections, Select strips individually whether or not they are connected (optional)
        :return: Result of the operator call.
    """

def select_circle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    x: int | None = 0,
    y: int | None = 0,
    radius: int | None = 25,
    wait_for_input: bool | None = True,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
    ignore_connections: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select strips using circle selection

        :param x: X, (in [-inf, inf], optional)
        :param y: Y, (in [-inf, inf], optional)
        :param radius: Radius, (in [1, inf], optional)
        :param wait_for_input: Wait for Input, (optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :param ignore_connections: Ignore Connections, Select strips individually whether or not they are connected (optional)
        :return: Result of the operator call.
    """

def select_grouped(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "TYPE", "TYPE_BASIC", "TYPE_EFFECT", "DATA", "EFFECT", "EFFECT_LINK", "OVERLAP"
    ]
    | None = "TYPE",
    extend: bool | None = False,
    use_active_channel: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all strips grouped by various properties

        :param type: Type, (optional)

    TYPE
    Type -- Shared strip type.

    TYPE_BASIC
    Global Type -- All strips of same basic type (graphical or sound).

    TYPE_EFFECT
    Effect Type -- Shared strip effect type (if active strip is not an effect one, select all non-effect strips).

    DATA
    Data -- Shared data (scene, image, sound, etc.).

    EFFECT
    Effect -- Shared effects.

    EFFECT_LINK
    Effect/Linked -- Other strips affected by the active one (sharing some time, and below or effect-assigned).

    OVERLAP
    Overlap -- Overlapping time.
        :param extend: Extend, Extend selection instead of deselecting everything first (optional)
        :param use_active_channel: Same Channel, Only consider strips on the same channel as the active one (optional)
        :return: Result of the operator call.
    """

def select_handle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    wait_to_deselect_others: bool | None = False,
    use_select_on_click: bool | None = False,
    mouse_x: int | None = 0,
    mouse_y: int | None = 0,
    ignore_connections: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select strip handle

    :param wait_to_deselect_others: Wait to Deselect Others, (optional)
    :param use_select_on_click: Act on Click, Instead of selecting on mouse press, wait to see if theres drag event. Otherwise select on mouse release (optional)
    :param mouse_x: Mouse X, (in [-inf, inf], optional)
    :param mouse_y: Mouse Y, (in [-inf, inf], optional)
    :param ignore_connections: Ignore Connections, Select strips individually whether or not they are connected (optional)
    :return: Result of the operator call.
    """

def select_handles(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    side: typing.Literal[
        "LEFT", "RIGHT", "BOTH", "LEFT_NEIGHBOR", "RIGHT_NEIGHBOR", "BOTH_NEIGHBORS"
    ]
    | None = "BOTH",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select gizmo handles on the sides of the selected strip

    :param side: Side, The side of the handle that is selected (optional)
    :return: Result of the operator call.
    """

def select_lasso(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path=None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select strips using lasso selection

        :param path: Path, (optional)
        :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path (optional)
        :param smooth_stroke_factor: Smooth Stroke Factor, Higher values gives a smoother stroke (in [0.5, 0.99], optional)
        :param smooth_stroke_radius: Smooth Stroke Radius, Minimum distance from last point before selection continues (in [10, 200], optional)
        :param mode: Mode, (optional)

    SET
    Set -- Set a new selection.

    ADD
    Extend -- Extend existing selection.

    SUB
    Subtract -- Subtract existing selection.
        :return: Result of the operator call.
    """

def select_less(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Shrink the current selection of adjacent selected strips

    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all strips adjacent to the current selection

    :return: Result of the operator call.
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select a chain of linked strips nearest to the mouse pointer

    :param extend: Extend, Extend the selection (optional)
    :return: Result of the operator call.
    """

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select more strips adjacent to the current selection

    :return: Result of the operator call.
    """

def select_side(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    side: typing.Literal["MOUSE", "LEFT", "RIGHT", "BOTH", "NO_CHANGE"] | None = "BOTH",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select strips on the nominated side of the selected strips

    :param side: Side, The side to which the selection is applied (optional)
    :return: Result of the operator call.
    """

def select_side_of_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    side: typing.Literal["LEFT", "RIGHT", "CURRENT"] | None = "LEFT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select strips relative to the current frame

        :param extend: Extend, Extend the selection (optional)
        :param side: Side, (optional)

    LEFT
    Left -- Select to the left of the current frame.

    RIGHT
    Right -- Select to the right of the current frame.

    CURRENT
    Current Frame -- Select intersecting with the current frame.
        :return: Result of the operator call.
    """

def set_range_to_strips(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    preview: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the frame range to the selected strips start and end

    :param preview: Preview, Set the preview range instead (optional)
    :return: Result of the operator call.
    """

def slip(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    offset: float | None = 0.0,
    slip_keyframes: bool | None = False,
    use_cursor_position: bool | None = False,
    ignore_connections: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Slip the contents of selected strips

    :param offset: Offset, Offset to the data of the strip (in [-inf, inf], optional)
    :param slip_keyframes: Slip Keyframes, Move the keyframes alongside the media (optional)
    :param use_cursor_position: Use Cursor Position, Slip strips under mouse cursor instead of all selected strips (optional)
    :param ignore_connections: Ignore Connections, Do not slip connected strips if using cursor position (optional)
    :return: Result of the operator call.
    """

def snap(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frame: int | None = 0,
    side: typing.Literal["LEFT", "RIGHT"] | None = "LEFT",
    keep_offset: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap strips to the current frame, using the active strip as the anchor, and the mouse cursor relative to the playhead to determine the side of the playhead to snap to

    :param frame: Frame, Frame where selected strips will be snapped (in [-inf, inf], optional)
    :param side: Snap Side, Which side of the playhead strips should snap to when no handles are selected (optional)
    :param keep_offset: Keep Offset, Whether the selection should be snapped as a whole or by each individual strip (optional)
    :return: Result of the operator call.
    """

def sound_strip_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str | None = "",
    directory: str | None = "",
    files=None,
    check_existing: bool | None = False,
    filter_blender: bool | None = False,
    filter_backup: bool | None = False,
    filter_image: bool | None = False,
    filter_movie: bool | None = False,
    filter_python: bool | None = False,
    filter_font: bool | None = False,
    filter_sound: bool | None = True,
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
    move_strips: bool | None = True,
    frame_start: int | None = 0,
    channel: int | None = 1,
    replace_sel: bool | None = True,
    overlap: bool | None = False,
    overlap_shuffle_override: bool | None = False,
    skip_locked_or_muted_channels: bool | None = True,
    cache: bool | None = False,
    mono: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a sound strip to the sequencer

        :param filepath: File Path, Path to file (optional, never None)
        :param directory: Directory, Directory of the file (optional, never None)
        :param files: Files, (optional)
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
        :param move_strips: Move Strips, Automatically begin translating strips with the mouse after adding them to the timeline (optional)
        :param frame_start: Start Frame, Start frame of the strip (in [-inf, inf], optional)
        :param channel: Channel, Channel to place this strip into (in [1, 128], optional)
        :param replace_sel: Replace Selection, Deselect previously selected strips after add operation completes (optional)
        :param overlap: Allow Overlap, Dont correct overlap on new strips (optional)
        :param overlap_shuffle_override: Override Overlap Shuffle Behavior, Use the overlap_mode tool settings to determine how to shuffle overlapping strips (optional)
        :param skip_locked_or_muted_channels: Skip Locked or Muted Channels, Add strips to muted or locked channels when adding movie strips (optional)
        :param cache: Cache, Cache the sound in memory (optional)
        :param mono: Mono, Merge all the sounds channels into one (optional)
        :return: Result of the operator call.
    """

def split(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frame: int | None = 0,
    channel: int | None = 0,
    type: typing.Literal["SOFT", "HARD"] | None = "SOFT",
    use_cursor_position: bool | None = False,
    side: typing.Literal["MOUSE", "LEFT", "RIGHT", "BOTH", "NO_CHANGE"]
    | None = "MOUSE",
    ignore_selection: bool | None = False,
    ignore_connections: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split the selected strips in two

    :param frame: Frame, Frame where selected strips will be split (in [-inf, inf], optional)
    :param channel: Channel, Channel in which strip will be cut (in [-inf, inf], optional)
    :param type: Type, The type of split operation to perform on strips (optional)
    :param use_cursor_position: Use Cursor Position, Split at position of the cursor instead of current frame (optional)
    :param side: Side, The side that remains selected after splitting (optional)
    :param ignore_selection: Ignore Selection, Make cut even if strip is not selected preserving selection state after cut (optional)
    :param ignore_connections: Ignore Connections, Dont propagate split to connected strips (optional)
    :return: Result of the operator call.
    """

def split_multicam(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    camera: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split multicam strip and select camera

    :param camera: Camera, (in [1, 32], optional)
    :return: Result of the operator call.
    """

def strip_color_tag_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    color: Literal[bpy.stub_internal.rna_enums.StripColorItems] | None = "NONE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set a color tag for the selected strips

    :param color: Color Tag, (optional)
    :return: Result of the operator call.
    """

def strip_jump(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    next: bool | None = True,
    center: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move frame to previous edit point

    :param next: Next Strip, (optional)
    :param center: Use Strip Center, (optional)
    :return: Result of the operator call.
    """

def strip_modifier_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a modifier to the strip

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def strip_modifier_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["REPLACE", "APPEND"] | None = "REPLACE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy modifiers of the active strip to all selected strips

        :param type: Type, (optional)

    REPLACE
    Replace -- Replace modifiers in destination.

    APPEND
    Append -- Append active modifiers to selected strips.
        :return: Result of the operator call.
    """

def strip_modifier_equalizer_redefine(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    graphs: typing.Literal["SIMPLE", "DOUBLE", "TRIPLE"] | None = "SIMPLE",
    name: str | None = "Name",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Redefine equalizer graphs

        :param graphs: Graphs, Number of graphs (optional)

    SIMPLE
    Unique -- One unique graphical definition.

    DOUBLE
    Double -- Graphical definition in 2 sections.

    TRIPLE
    Triplet -- Graphical definition in 3 sections.
        :param name: Name, Name of modifier to redefine (optional, never None)
        :return: Result of the operator call.
    """

def strip_modifier_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "Name",
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move modifier up and down in the stack

        :param name: Name, Name of modifier to remove (optional, never None)
        :param direction: Type, (optional)

    UP
    Up -- Move modifier up in the stack.

    DOWN
    Down -- Move modifier down in the stack.
        :return: Result of the operator call.
    """

def strip_modifier_move_to_index(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    modifier: str | None = "",
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the strip modifiers index in the stack so it evaluates after the set number of others

    :param modifier: Modifier, Name of the modifier to edit (optional, never None)
    :param index: Index, The index to move the modifier to (in [0, inf], optional)
    :return: Result of the operator call.
    """

def strip_modifier_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "Name",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove a modifier from the strip

    :param name: Name, Name of modifier to remove (optional, never None)
    :return: Result of the operator call.
    """

def strip_modifier_set_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    modifier: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Activate the strip modifier to use as the context

    :param modifier: Modifier, Name of the strip modifier to edit (optional, never None)
    :return: Result of the operator call.
    """

def strip_transform_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    property: typing.Literal["POSITION", "SCALE", "ROTATION", "ALL"] | None = "ALL",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset image transformation to default value

        :param property: Property, Strip transform property to be reset (optional)

    POSITION
    Position -- Reset strip transform location.

    SCALE
    Scale -- Reset strip transform scale.

    ROTATION
    Rotation -- Reset strip transform rotation.

    ALL
    All -- Reset strip transform location, scale and rotation.
        :return: Result of the operator call.
    """

def strip_transform_fit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    fit_method: Literal[bpy.stub_internal.rna_enums.StripScaleMethodItems]
    | None = "FIT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param fit_method: Fit Method, Mode for fitting the image to the canvas (optional)
    :return: Result of the operator call.
    """

def swap(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    side: typing.Literal["LEFT", "RIGHT"] | None = "RIGHT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap active strip with strip to the right or left

    :param side: Side, Side of the strip to swap (optional)
    :return: Result of the operator call.
    """

def swap_data(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap 2 sequencer strips

    :return: Result of the operator call.
    """

def swap_inputs(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap the two inputs of the effect strip

    :return: Result of the operator call.
    """

def text_cursor_move(
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
    ]
    | None = "LINE_BEGIN",
    select_text: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move cursor in text

    :param type: Type, Where to move cursor to, to make a selection (optional)
    :param select_text: Select Text, Select text while moving cursor (optional)
    :return: Result of the operator call.
    """

def text_cursor_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select_text: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set cursor position in text

    :param select_text: Select Text, Select text while moving cursor (optional)
    :return: Result of the operator call.
    """

def text_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["NEXT_OR_SELECTION", "PREVIOUS_OR_SELECTION"]
    | None = "NEXT_OR_SELECTION",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete text at cursor position

    :param type: Type, Which part of the text to delete (optional)
    :return: Result of the operator call.
    """

def text_deselect_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect all characters

    :return: Result of the operator call.
    """

def text_edit_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy text to clipboard

    :return: Result of the operator call.
    """

def text_edit_cut(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cut text to clipboard

    :return: Result of the operator call.
    """

def text_edit_mode_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle text editing

    :return: Result of the operator call.
    """

def text_edit_paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste text from clipboard

    :return: Result of the operator call.
    """

def text_insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    string: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert text at cursor position

    :param string: String, String to be inserted at cursor position (optional, never None)
    :return: Result of the operator call.
    """

def text_line_break(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert line break at cursor position

    :return: Result of the operator call.
    """

def text_select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all characters

    :return: Result of the operator call.
    """

def unlock(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unlock strips so they can be transformed

    :return: Result of the operator call.
    """

def unmute(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unmute (un)selected strips

    :param unselected: Unselected, Unmute unselected rather than selected strips (optional)
    :return: Result of the operator call.
    """

def view_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """View all the strips in the sequencer

    :return: Result of the operator call.
    """

def view_all_preview(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Zoom preview to fit in the area

    :return: Result of the operator call.
    """

def view_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the view to the current frame

    :return: Result of the operator call.
    """

def view_ghost_border(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the boundaries of the border used for offset view

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def view_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Zoom the sequencer on the selected strips

    :return: Result of the operator call.
    """

def view_zoom_ratio(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 1.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change zoom ratio of sequencer preview

    :param ratio: Ratio, Zoom ratio, 1.0 is 1:1, higher is zoomed in, lower is zoomed out (in [-inf, inf], optional)
    :return: Result of the operator call.
    """
