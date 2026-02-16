import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def active_frame_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete the active Grease Pencil frame(s)

    :param all: Delete all, Delete active keyframes of all layers (optional)
    :return: Result of the operator call.
    """

def bake_grease_pencil_animation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frame_start: int | None = 1,
    frame_end: int | None = 250,
    step: int | None = 1,
    only_selected: bool | None = False,
    frame_target: int | None = 1,
    project_type: typing.Literal["KEEP", "FRONT", "SIDE", "TOP", "VIEW", "CURSOR"]
    | None = "KEEP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bake Grease Pencil object transform to Grease Pencil keyframes

        :param frame_start: Start Frame, The start frame (in [1, 100000], optional)
        :param frame_end: End Frame, The end frame of animation (in [1, 100000], optional)
        :param step: Step, Step between generated frames (in [1, 100], optional)
        :param only_selected: Only Selected Keyframes, Convert only selected keyframes (optional)
        :param frame_target: Target Frame, Destination frame (in [1, 100000], optional)
        :param project_type: Projection Type, (optional)

    KEEP
    No Reproject.

    FRONT
    Front -- Reproject the strokes using the X-Z plane.

    SIDE
    Side -- Reproject the strokes using the Y-Z plane.

    TOP
    Top -- Reproject the strokes using the X-Y plane.

    VIEW
    View -- Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using Cursor Stroke Placement.

    CURSOR
    Cursor -- Reproject the strokes using the orientation of 3D cursor.
        :return: Result of the operator call.
    """

def brush_stroke(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    stroke=None,
    mode: typing.Literal["NORMAL", "INVERT"] | None = "NORMAL",
    brush_toggle: typing.Literal["None", "SMOOTH", "ERASE", "MASK"] | None = "None",
    pen_flip: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Draw a new stroke in the active Grease Pencil object

        :param stroke: Stroke, (optional)
        :param mode: Stroke Mode, Action taken when a paint stroke is made (optional)

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.
        :param brush_toggle: Temporary Brush Toggle Type, Brush to use for duration of stroke (optional)

    None
    None -- Apply brush normally.

    SMOOTH
    Smooth -- Switch to smooth brush for duration of stroke.

    ERASE
    Erase -- Switch to erase brush for duration of stroke.

    MASK
    Mask -- Switch to mask brush for duration of stroke.
        :param pen_flip: Pen Flip, Whether a tablets eraser mode is being used (optional)
        :return: Result of the operator call.
    """

def caps_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["ROUND", "FLAT", "START", "END"] | None = "ROUND",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change curve caps mode (rounded or flat)

        :param type: Type, (optional)

    ROUND
    Rounded -- Set as default rounded.

    FLAT
    Flat.

    START
    Toggle Start.

    END
    Toggle End.
        :return: Result of the operator call.
    """

def clean_loose(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    limit: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove loose points

    :param limit: Limit, Number of points to consider stroke as loose (in [1, inf], optional)
    :return: Result of the operator call.
    """

def convert_curve_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: Literal[bpy.stub_internal.rna_enums.CurvesTypeItems] | None = "POLY",
    threshold: float | None = 0.01,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Convert type of selected curves

    :param type: Type, (optional)
    :param threshold: Threshold, The distance that the resulting points are allowed to be within (in [0, 100], optional)
    :return: Result of the operator call.
    """

def copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected Grease Pencil points or strokes to the internal clipboard

    :return: Result of the operator call.
    """

def cyclical_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["CLOSE", "OPEN", "TOGGLE"] | None = "TOGGLE",
    subdivide_cyclic_segment: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Close or open the selected stroke adding a segment from last to first point

    :param type: Type, (optional)
    :param subdivide_cyclic_segment: Match Point Density, Add point in the new segment to keep the same density (optional)
    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["ALL", "STROKES", "FILLS"] | None = "ALL",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected strokes or points

        :param mode: Mode, The kind of strokes or fills to delete (optional)

    ALL
    All -- Delete all selected strokes or points.

    STROKES
    Only Strokes -- Delete only strokes and not fills.

    FILLS
    Only Fills -- Delte only fills and not strokes.
        :return: Result of the operator call.
    """

def delete_breakdown(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove breakdown frames generated by interpolating between two Grease Pencil frames

    :return: Result of the operator call.
    """

def delete_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["ACTIVE_FRAME", "ALL_FRAMES"] | None = "ACTIVE_FRAME",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete Grease Pencil Frame(s)

        :param type: Type, Method used for deleting Grease Pencil frames (optional)

    ACTIVE_FRAME
    Active Frame -- Deletes current frame in the active layer.

    ALL_FRAMES
    All Active Frames -- Delete active frames for all layers.
        :return: Result of the operator call.
    """

def dissolve(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["POINTS", "BETWEEN", "UNSELECT"] | None = "POINTS",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected points without splitting strokes

        :param type: Type, Method used for dissolving stroke points (optional)

    POINTS
    Dissolve -- Dissolve selected points.

    BETWEEN
    Dissolve Between -- Dissolve points between selected points.

    UNSELECT
    Dissolve Unselect -- Dissolve all unselected points.
        :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate the selected points

    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    GREASE_PENCIL_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make copies of the selected Grease Pencil strokes and move them

    :param GREASE_PENCIL_OT_duplicate: Duplicate, Duplicate the selected points (optional, `bpy.ops.grease_pencil.duplicate` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def erase_box(
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
    """Erase points in the box region

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def erase_lasso(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path=None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Erase points in the lasso region

    :param path: Path, (optional)
    :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path (optional)
    :param smooth_stroke_factor: Smooth Stroke Factor, Higher values gives a smoother stroke (in [0.5, 0.99], optional)
    :param smooth_stroke_radius: Smooth Stroke Radius, Minimum distance from last point before selection continues (in [10, 200], optional)
    :return: Result of the operator call.
    """

def extrude(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude the selected points

    :return: Result of the operator call.
    """

def extrude_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    GREASE_PENCIL_OT_extrude: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude selected points and move them

    :param GREASE_PENCIL_OT_extrude: Extrude Stroke Points, Extrude the selected points (optional, `bpy.ops.grease_pencil.extrude` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def fill(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    invert: bool | None = False,
    precision: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Fill with color the shape formed by strokes

    :param invert: Invert, Find boundary of unfilled instead of filled regions (optional)
    :param precision: Precision, Use precision movement for extension lines (optional)
    :return: Result of the operator call.
    """

def frame_clean_duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    selected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove any keyframe that is a duplicate of the previous one

    :param selected: Selected, Only delete selected keyframes (optional)
    :return: Result of the operator call.
    """

def frame_duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make a copy of the active Grease Pencil frame(s)

    :param all: Duplicate all, Duplicate active keyframes of all layer (optional)
    :return: Result of the operator call.
    """

def insert_blank_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all_layers: bool | None = False,
    duration: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert a blank frame on the current scene frame

    :param all_layers: All Layers, Insert a blank frame in all editable layers (optional)
    :param duration: Duration, (in [0, 1048574], optional)
    :return: Result of the operator call.
    """

def interpolate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    shift: float | None = 0.0,
    layers: typing.Literal["ACTIVE", "ALL"] | None = "ACTIVE",
    exclude_breakdowns: bool | None = False,
    use_selection: bool | None = False,
    flip: typing.Literal["NONE", "FLIP", "AUTO"] | None = "AUTO",
    smooth_steps: int | None = 1,
    smooth_factor: float | None = 0.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interpolate Grease Pencil strokes between frames

    :param shift: Shift, Bias factor for which frame has more influence on the interpolated strokes (in [-1, 1], optional)
    :param layers: Layer, Layers included in the interpolation (optional)
    :param exclude_breakdowns: Exclude Breakdowns, Exclude existing Breakdowns keyframes as interpolation extremes (optional)
    :param use_selection: Use Selection, Use only selected strokes for interpolating (optional)
    :param flip: Flip Mode, Invert destination stroke to match start and end with source stroke (optional)
    :param smooth_steps: Iterations, Number of times to smooth newly created strokes (in [1, 3], optional)
    :param smooth_factor: Smooth, Amount of smoothing to apply to interpolated strokes, to reduce jitter/noise (in [0, 2], optional)
    :return: Result of the operator call.
    """

def interpolate_sequence(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    step: int | None = 1,
    layers: typing.Literal["ACTIVE", "ALL"] | None = "ACTIVE",
    exclude_breakdowns: bool | None = False,
    use_selection: bool | None = False,
    flip: typing.Literal["NONE", "FLIP", "AUTO"] | None = "AUTO",
    smooth_steps: int | None = 1,
    smooth_factor: float | None = 0.0,
    type: typing.Literal[
        "LINEAR",
        "CUSTOM",
        "SINE",
        "QUAD",
        "CUBIC",
        "QUART",
        "QUINT",
        "EXPO",
        "CIRC",
        "BACK",
        "BOUNCE",
        "ELASTIC",
    ]
    | None = "LINEAR",
    easing: Literal[bpy.stub_internal.rna_enums.BeztripleInterpolationEasingItems]
    | None = "EASE_IN",
    back: float | None = 1.702,
    amplitude: float | None = 0.15,
    period: float | None = 0.15,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Generate in-betweens to smoothly interpolate between Grease Pencil frames

        :param step: Step, Number of frames between generated interpolated frames (in [1, 1048574], optional)
        :param layers: Layer, Layers included in the interpolation (optional)
        :param exclude_breakdowns: Exclude Breakdowns, Exclude existing Breakdowns keyframes as interpolation extremes (optional)
        :param use_selection: Use Selection, Use only selected strokes for interpolating (optional)
        :param flip: Flip Mode, Invert destination stroke to match start and end with source stroke (optional)
        :param smooth_steps: Iterations, Number of times to smooth newly created strokes (in [1, 3], optional)
        :param smooth_factor: Smooth, Amount of smoothing to apply to interpolated strokes, to reduce jitter/noise (in [0, 2], optional)
        :param type: Type, Interpolation method to use the next time Interpolate Sequence is run (optional)

    LINEAR
    Linear -- Straight-line interpolation between A and B (i.e. no ease in/out).

    CUSTOM
    Custom -- Custom interpolation defined using a curve map.

    SINE
    Sinusoidal -- Sinusoidal easing (weakest, almost linear but with a slight curvature).

    QUAD
    Quadratic -- Quadratic easing.

    CUBIC
    Cubic -- Cubic easing.

    QUART
    Quartic -- Quartic easing.

    QUINT
    Quintic -- Quintic easing.

    EXPO
    Exponential -- Exponential easing (dramatic).

    CIRC
    Circular -- Circular easing (strongest and most dynamic).

    BACK
    Back -- Cubic easing with overshoot and settle.

    BOUNCE
    Bounce -- Exponentially decaying parabolic bounce, like when objects collide.

    ELASTIC
    Elastic -- Exponentially decaying sine wave, like an elastic band.
        :param easing: Easing, Which ends of the segment between the preceding and following Grease Pencil frames easing interpolation is applied to (optional)
        :param back: Back, Amount of overshoot for back easing (in [0, inf], optional)
        :param amplitude: Amplitude, Amount to boost elastic bounces for elastic easing (in [0, inf], optional)
        :param period: Period, Time between bounces for elastic easing (in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def join_fills(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Join selected strokes into one fill to create holes

    :return: Result of the operator call.
    """

def join_selection(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["JOINSTROKES", "SPLITCOPY", "SPLIT"] | None = "JOINSTROKES",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """New stroke from selected points/strokes

        :param type: Type, Defines how the operator will behave on the selection in the active layer (optional)

    JOINSTROKES
    Join Strokes -- Join the selected strokes into one stroke.

    SPLITCOPY
    Split and Copy -- Copy the selected points to a new stroke.

    SPLIT
    Split -- Split the selected point to a new stroke.
        :return: Result of the operator call.
    """

def layer_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    layer: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the active Grease Pencil layer

    :param layer: Grease Pencil Layer, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def layer_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    new_layer_name: str | None = "Layer",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new Grease Pencil layer in the active object

    :param new_layer_name: Name, Name of the new layer (optional, never None)
    :return: Result of the operator call.
    """

def layer_duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    empty_keyframes: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make a copy of the active Grease Pencil layer

    :param empty_keyframes: Empty Keyframes, Add Empty Keyframes (optional)
    :return: Result of the operator call.
    """

def layer_duplicate_object(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_active: bool | None = True,
    mode: typing.Literal["ALL", "ACTIVE"] | None = "ALL",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make a copy of the active Grease Pencil layer to selected object

    :param only_active: Only Active, Copy only active Layer, uncheck to append all layers (optional)
    :param mode: Mode, (optional)
    :return: Result of the operator call.
    """

def layer_group_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    new_layer_group_name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new Grease Pencil layer group in the active object

    :param new_layer_group_name: Name, Name of the new layer group (optional, never None)
    :return: Result of the operator call.
    """

def layer_group_color_tag(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    color_tag: typing.Literal[
        "NONE",
        "COLOR1",
        "COLOR2",
        "COLOR3",
        "COLOR4",
        "COLOR5",
        "COLOR6",
        "COLOR7",
        "COLOR8",
    ]
    | None = "COLOR1",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change layer group icon

    :param color_tag: Color Tag, (optional)
    :return: Result of the operator call.
    """

def layer_group_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    keep_children: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove Grease Pencil layer group in the active object

    :param keep_children: Keep children nodes, Keep the children nodes of the group and only delete the group itself (optional)
    :return: Result of the operator call.
    """

def layer_hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide selected/unselected Grease Pencil layers

    :param unselected: Unselected, Hide unselected rather than selected layers (optional)
    :return: Result of the operator call.
    """

def layer_isolate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    affect_visibility: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make only active layer visible/editable

    :param affect_visibility: Affect Visibility, Also affect the visibility (optional)
    :return: Result of the operator call.
    """

def layer_lock_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    lock: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock all Grease Pencil layers to prevent them from being accidentally modified

    :param lock: Lock Value, Lock/Unlock all layers (optional)
    :return: Result of the operator call.
    """

def layer_mask_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new layer as masking

    :param name: Layer, Name of the layer (optional, never None)
    :return: Result of the operator call.
    """

def layer_mask_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove Layer Mask

    :return: Result of the operator call.
    """

def layer_mask_reorder(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reorder the active Grease Pencil mask layer up/down in the list

    :param direction: Direction, (optional)
    :return: Result of the operator call.
    """

def layer_merge(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["ACTIVE", "GROUP", "ALL"] | None = "ACTIVE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Combine layers based on the mode into one layer

        :param mode: Mode, (optional)

    ACTIVE
    Active -- Combine the active layer with the layer just below (if it exists).

    GROUP
    Group -- Combine layers in the active group into a single layer.

    ALL
    All -- Combine all layers into a single layer.
        :return: Result of the operator call.
    """

def layer_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the active Grease Pencil layer or Group

    :param direction: Direction, (optional)
    :return: Result of the operator call.
    """

def layer_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the active Grease Pencil layer

    :return: Result of the operator call.
    """

def layer_reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show all Grease Pencil layers

    :return: Result of the operator call.
    """

def material_copy_to_object(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_active: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Append Materials of the active Grease Pencil to other object

    :param only_active: Only Active, Append only active material, uncheck to append all materials (optional)
    :return: Result of the operator call.
    """

def material_hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    invert: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide active/inactive Grease Pencil material(s)

    :param invert: Invert, Hide inactive materials instead of the active one (optional)
    :return: Result of the operator call.
    """

def material_isolate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    affect_visibility: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle whether the active material is the only one that is editable and/or visible

    :param affect_visibility: Affect Visibility, In addition to toggling the editability, also affect the visibility (optional)
    :return: Result of the operator call.
    """

def material_lock_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock all Grease Pencil materials to prevent them from being accidentally modified

    :return: Result of the operator call.
    """

def material_lock_unselected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock any material not used in any selected stroke

    :return: Result of the operator call.
    """

def material_lock_unused(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock and hide any material not used

    :return: Result of the operator call.
    """

def material_reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unhide all hidden Grease Pencil materials

    :return: Result of the operator call.
    """

def material_select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select/Deselect all Grease Pencil strokes using current material

    :param deselect: Deselect, Unselect strokes (optional)
    :return: Result of the operator call.
    """

def material_unlock_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unlock all Grease Pencil materials so that they can be edited

    :return: Result of the operator call.
    """

def move_to_layer(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    target_layer_name: str | None = "",
    target_group_name: str | None = "",
    add_new_layer: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move selected strokes to another layer

    :param target_layer_name: Name, Target Grease Pencil Layer (optional, never None)
    :param target_group_name: Target Group, Group to add the new layer to (optional, never None)
    :param add_new_layer: New Layer, Move selection to a new layer (optional)
    :return: Result of the operator call.
    """

def outline(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["VIEW", "FRONT", "SIDE", "TOP", "CURSOR", "CAMERA"]
    | None = "VIEW",
    radius: float | None = 0.01,
    offset_factor: float | None = -1.0,
    corner_subdivisions: int | None = 2,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Convert selected strokes to perimeter

    :param type: Projection Mode, (optional)
    :param radius: Radius, (in [0, 10], optional)
    :param offset_factor: Offset Factor, (in [-1, 1], optional)
    :param corner_subdivisions: Corner Subdivisions, (in [0, 10], optional)
    :return: Result of the operator call.
    """

def paintmode_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    back: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enter/Exit paint mode for Grease Pencil strokes

    :param back: Return to Previous Mode, Return to previous mode (optional)
    :return: Result of the operator call.
    """

def paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["ACTIVE", "LAYER"] | None = "ACTIVE",
    paste_back: bool | None = False,
    keep_world_transform: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste Grease Pencil points or strokes from the internal clipboard to the active layer

    :param type: Type, (optional)
    :param paste_back: Paste on Back, Add pasted strokes behind all strokes (optional)
    :param keep_world_transform: Keep World Transform, Keep the world transform of strokes from the clipboard unchanged (optional)
    :return: Result of the operator call.
    """

def pen(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
    deselect_all: bool | None = False,
    select_passthrough: bool | None = False,
    extrude_point: bool | None = False,
    extrude_handle: typing.Literal["AUTO", "VECTOR"] | None = "VECTOR",
    delete_point: bool | None = False,
    insert_point: bool | None = False,
    move_segment: bool | None = False,
    select_point: bool | None = False,
    move_point: bool | None = False,
    cycle_handle_type: bool | None = False,
    size: float | None = 0.01,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct and edit splines

    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :param deselect: Deselect, Remove from selection (optional)
    :param toggle: Toggle Selection, Toggle the selection (optional)
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
    :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected (optional)
    :param extrude_point: Extrude Point, Add a point connected to the last selected point (optional)
    :param extrude_handle: Extrude Handle Type, Type of the extruded handle (optional)
    :param delete_point: Delete Point, Delete an existing point (optional)
    :param insert_point: Insert Point, Insert Point into a curve segment (optional)
    :param move_segment: Move Segment, Delete an existing point (optional)
    :param select_point: Select Point, Select a point or its handles (optional)
    :param move_point: Move Point, Move a point or its handles (optional)
    :param cycle_handle_type: Cycle Handle Type, Cycle between all four handle types (optional)
    :param size: Size, Diameter of new points (in [0, inf], optional)
    :return: Result of the operator call.
    """

def primitive_arc(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    subdivision: int | None = 62,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "ARC",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create predefined Grease Pencil stroke arcs

    :param subdivision: Subdivisions, Number of subdivisions per segment (in [0, inf], optional)
    :param type: Type, Type of shape (optional)
    :return: Result of the operator call.
    """

def primitive_box(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    subdivision: int | None = 3,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "BOX",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create predefined Grease Pencil stroke boxes

    :param subdivision: Subdivisions, Number of subdivisions per segment (in [0, inf], optional)
    :param type: Type, Type of shape (optional)
    :return: Result of the operator call.
    """

def primitive_circle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    subdivision: int | None = 94,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "CIRCLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create predefined Grease Pencil stroke circles

    :param subdivision: Subdivisions, Number of subdivisions per segment (in [0, inf], optional)
    :param type: Type, Type of shape (optional)
    :return: Result of the operator call.
    """

def primitive_curve(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    subdivision: int | None = 62,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "CURVE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create predefined Grease Pencil stroke curve shapes

    :param subdivision: Subdivisions, Number of subdivisions per segment (in [0, inf], optional)
    :param type: Type, Type of shape (optional)
    :return: Result of the operator call.
    """

def primitive_line(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    subdivision: int | None = 6,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "LINE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create predefined Grease Pencil stroke lines

    :param subdivision: Subdivisions, Number of subdivisions per segment (in [0, inf], optional)
    :param type: Type, Type of shape (optional)
    :return: Result of the operator call.
    """

def primitive_polyline(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    subdivision: int | None = 6,
    type: typing.Literal["BOX", "LINE", "POLYLINE", "CIRCLE", "ARC", "CURVE"]
    | None = "POLYLINE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create predefined Grease Pencil stroke polylines

    :param subdivision: Subdivisions, Number of subdivisions per segment (in [0, inf], optional)
    :param type: Type, Type of shape (optional)
    :return: Result of the operator call.
    """

def relative_layer_mask_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["ABOVE", "BELOW"] | None = "ABOVE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mask active layer with layer above or below

    :param mode: Mode, Which relative layer (above or below) to use as a mask (optional)
    :return: Result of the operator call.
    """

def remove_fill_guides(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["ACTIVE_FRAME", "ALL_FRAMES"] | None = "ALL_FRAMES",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all the strokes that were created from the fill tool as guides

    :param mode: Mode, (optional)
    :return: Result of the operator call.
    """

def reorder(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["TOP", "UP", "DOWN", "BOTTOM"] | None = "TOP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the display order of the selected strokes

    :param direction: Direction, (optional)
    :return: Result of the operator call.
    """

def reproject(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["FRONT", "SIDE", "TOP", "VIEW", "SURFACE", "CURSOR"]
    | None = "VIEW",
    keep_original: bool | None = False,
    offset: float | None = 0.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reproject the selected strokes from the current viewpoint as if they had been newly drawn (e.g. to fix problems from accidental 3D cursor movement or accidental viewport changes, or for matching deforming geometry)

        :param type: Projection Type, (optional)

    FRONT
    Front -- Reproject the strokes using the X-Z plane.

    SIDE
    Side -- Reproject the strokes using the Y-Z plane.

    TOP
    Top -- Reproject the strokes using the X-Y plane.

    VIEW
    View -- Reproject the strokes to end up on the same plane, as if drawn from the current viewpoint using Cursor Stroke Placement.

    SURFACE
    Surface -- Reproject the strokes on to the scene geometry, as if drawn using Surface placement.

    CURSOR
    Cursor -- Reproject the strokes using the orientation of 3D cursor.
        :param keep_original: Keep Original, Keep original strokes and create a copy before reprojecting (optional)
        :param offset: Surface Offset, (in [0, 10], optional)
        :return: Result of the operator call.
    """

def reset_uvs(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset UV transformation to default values

    :return: Result of the operator call.
    """

def sculpt_paint(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    stroke=None,
    mode: typing.Literal["NORMAL", "INVERT"] | None = "NORMAL",
    brush_toggle: typing.Literal["None", "SMOOTH", "ERASE", "MASK"] | None = "None",
    pen_flip: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Sculpt strokes in the active Grease Pencil object

        :param stroke: Stroke, (optional)
        :param mode: Stroke Mode, Action taken when a paint stroke is made (optional)

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.
        :param brush_toggle: Temporary Brush Toggle Type, Brush to use for duration of stroke (optional)

    None
    None -- Apply brush normally.

    SMOOTH
    Smooth -- Switch to smooth brush for duration of stroke.

    ERASE
    Erase -- Switch to erase brush for duration of stroke.

    MASK
    Mask -- Switch to mask brush for duration of stroke.
        :param pen_flip: Pen Flip, Whether a tablets eraser mode is being used (optional)
        :return: Result of the operator call.
    """

def sculptmode_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    back: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enter/Exit sculpt mode for Grease Pencil strokes

    :param back: Return to Previous Mode, Return to previous mode (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select all visible strokes

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

def select_alternate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect_ends: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select alternated points in strokes with already selected points

    :param deselect_ends: Deselect Ends, (De)select the first and last point of each stroke (optional)
    :return: Result of the operator call.
    """

def select_by_stroke_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["STROKE", "FILL"] | None = "STROKE",
    deselect: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select/Deselect all strokes or fills

    :param type: Type, (optional)
    :param deselect: Deselect, Unselect strokes (optional)
    :return: Result of the operator call.
    """

def select_ends(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    amount_start: int | None = 0,
    amount_end: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select end points of strokes

    :param amount_start: Amount Start, Number of points to select from the start (in [0, inf], optional)
    :param amount_end: Amount End, Number of points to select from the end (in [0, inf], optional)
    :return: Result of the operator call.
    """

def select_fill(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all curves in a fill

    :return: Result of the operator call.
    """

def select_less(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Shrink the selection by one point

    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all points in curves with any point selection

    :return: Result of the operator call.
    """

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Grow the selection by one point

    :return: Result of the operator call.
    """

def select_random(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Selects random points from the current strokes selection

        :param ratio: Ratio, Portion of items to select randomly (in [0, 1], optional)
        :param seed: Random Seed, Seed for the random number generator (in [0, inf], optional)
        :param action: Action, Selection action to execute (optional)

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :return: Result of the operator call.
    """

def select_similar(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["LAYER", "MATERIAL", "VERTEX_COLOR", "RADIUS", "OPACITY"]
    | None = "LAYER",
    threshold: float | None = 0.1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all strokes with similar characteristics

    :param mode: Mode, (optional)
    :param threshold: Threshold, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["SELECTED", "MATERIAL", "LAYER"] | None = "SELECTED",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Separate the selected geometry into a new Grease Pencil object

        :param mode: Mode, (optional)

    SELECTED
    Selection -- Separate selected geometry.

    MATERIAL
    By Material -- Separate by material.

    LAYER
    By Layer -- Separate by layer.
        :return: Result of the operator call.
    """

def separate_fills(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    individual: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Separate the selected strokes from current fill

    :param individual: Individual, Create a separate fill for each individual stroke (optional)
    :return: Result of the operator call.
    """

def set_active_material(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the selected stroke material as the active material

    :return: Result of the operator call.
    """

def set_corner_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    corner_type: typing.Literal["ROUND", "FLAT", "SHARP"] | None = "SHARP",
    miter_angle: float | None = 0.785398,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the corner type of the selected points

    :param corner_type: Corner Type, (optional)
    :param miter_angle: Miter Cut Angle, All corners sharper than the Miter angle will be cut flat (in [0, 3.14159], optional)
    :return: Result of the operator call.
    """

def set_curve_resolution(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    resolution: int | None = 12,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set resolution of selected curves

    :param resolution: Resolution, The resolution to use for each curve segment (in [0, 10000], optional)
    :return: Result of the operator call.
    """

def set_curve_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: Literal[bpy.stub_internal.rna_enums.CurvesTypeItems] | None = "POLY",
    use_handles: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set type of selected curves

    :param type: Type, Curve type (optional)
    :param use_handles: Handles, Take handle information into account in the conversion (optional)
    :return: Result of the operator call.
    """

def set_handle_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["AUTO", "VECTOR", "ALIGN", "FREE_ALIGN", "TOGGLE_FREE_ALIGN"]
    | None = "AUTO",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the handle type for Bézier curves

        :param type: Type, (optional)

    AUTO
    Auto -- The location is automatically calculated to be smooth.

    VECTOR
    Vector -- The location is calculated to point to the next/previous control point.

    ALIGN
    Align -- The location is constrained to point in the opposite direction as the other handle.

    FREE_ALIGN
    Free -- The handle can be moved anywhere, and does not influence the points other handle.

    TOGGLE_FREE_ALIGN
    Toggle Free/Align -- Replace Free handles with Align, and all Align with Free handles.
        :return: Result of the operator call.
    """

def set_material(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    slot: typing.Literal["DEFAULT"] | None = "DEFAULT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set active material

    :param slot: Material Slot, (optional)
    :return: Result of the operator call.
    """

def set_selection_mode(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: Literal[bpy.stub_internal.rna_enums.GreasePencilSelectmodeItems]
    | None = "POINT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the selection mode for Grease Pencil strokes

    :param mode: Mode, (optional)
    :return: Result of the operator call.
    """

def set_start_point(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select which point is the beginning of the curve

    :return: Result of the operator call.
    """

def set_stroke_type(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["STROKE", "FILL", "BOTH"] | None = "STROKE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the stroke type (stroke, fill, or both) of the selected strokes

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def set_uniform_opacity(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    opacity_stroke: float | None = 1.0,
    opacity_fill: float | None = 0.5,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set all stroke points to same opacity

    :param opacity_stroke: Stroke Opacity, (in [0, 1], optional)
    :param opacity_fill: Fill Opacity, (in [0, 1], optional)
    :return: Result of the operator call.
    """

def set_uniform_thickness(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    thickness: float | None = 0.1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set all stroke points to same thickness

    :param thickness: Thickness, Thickness (in [0, 1000], optional)
    :return: Result of the operator call.
    """

def snap_cursor_to_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap cursor to center of selected points

    :return: Result of the operator call.
    """

def snap_to_cursor(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_offset: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap selected points/strokes to the cursor

    :param use_offset: With Offset, Offset the entire stroke instead of selected points only (optional)
    :return: Result of the operator call.
    """

def snap_to_grid(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Snap selected points to the nearest grid points

    :return: Result of the operator call.
    """

def stroke_material_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    material: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Assign the active material slot to the selected strokes

    :param material: Material, Name of the material (optional, never None)
    :return: Result of the operator call.
    """

def stroke_merge_by_distance(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    threshold: float | None = 0.001,
    use_unselected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Merge points by distance

    :param threshold: Threshold, (in [0, 100], optional)
    :param use_unselected: Unselected, Use whole stroke, not only selected points (optional)
    :return: Result of the operator call.
    """

def stroke_reset_vertex_color(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset vertex color for all or selected strokes

    :param mode: Mode, (optional)
    :return: Result of the operator call.
    """

def stroke_simplify(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    factor: float | None = 0.01,
    length: float | None = 0.05,
    distance: float | None = 0.01,
    steps: int | None = 1,
    mode: typing.Literal["FIXED", "ADAPTIVE", "SAMPLE", "MERGE"] | None = "FIXED",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Simplify selected strokes

        :param factor: Factor, (in [0, 100], optional)
        :param length: Length, (in [0, 100], optional)
        :param distance: Distance, (in [0, 100], optional)
        :param steps: Steps, (in [0, 50], optional)
        :param mode: Mode, Method used for simplifying stroke points (optional)

    FIXED
    Fixed -- Delete alternating vertices in the stroke, except extremes.

    ADAPTIVE
    Adaptive -- Use a Ramer-Douglas-Peucker algorithm to simplify the stroke preserving main shape.

    SAMPLE
    Sample -- Re-sample the stroke with segments of the specified length.

    MERGE
    Merge -- Simplify the stroke by merging vertices closer than a given distance.
        :return: Result of the operator call.
    """

def stroke_smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    iterations: int | None = 10,
    factor: float | None = 1.0,
    smooth_ends: bool | None = False,
    keep_shape: bool | None = False,
    smooth_position: bool | None = True,
    smooth_radius: bool | None = True,
    smooth_opacity: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Smooth selected strokes

    :param iterations: Iterations, (in [1, 100], optional)
    :param factor: Factor, (in [0, 1], optional)
    :param smooth_ends: Smooth Endpoints, (optional)
    :param keep_shape: Keep Shape, (optional)
    :param smooth_position: Position, (optional)
    :param smooth_radius: Radius, (optional)
    :param smooth_opacity: Opacity, (optional)
    :return: Result of the operator call.
    """

def stroke_split(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split selected points to a new stroke

    :return: Result of the operator call.
    """

def stroke_subdivide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    number_cuts: int | None = 1,
    only_selected: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Subdivide between continuous selected points of the stroke adding a point half way between them

    :param number_cuts: Number of Cuts, (in [1, 32], optional)
    :param only_selected: Selected Points, Smooth only selected points in the stroke (optional)
    :return: Result of the operator call.
    """

def stroke_subdivide_smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    GREASE_PENCIL_OT_stroke_subdivide: dict[str, typing.Any] | None = {},
    GREASE_PENCIL_OT_stroke_smooth: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Subdivide strokes and smooth them

    :param GREASE_PENCIL_OT_stroke_subdivide: Subdivide Stroke, Subdivide between continuous selected points of the stroke adding a point half way between them (optional, `bpy.ops.grease_pencil.stroke_subdivide` keyword arguments)
    :param GREASE_PENCIL_OT_stroke_smooth: Smooth Stroke, Smooth selected strokes (optional, `bpy.ops.grease_pencil.stroke_smooth` keyword arguments)
    :return: Result of the operator call.
    """

def stroke_switch_direction(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change direction of the points of the selected strokes

    :return: Result of the operator call.
    """

def stroke_trim(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path=None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete stroke points in between intersecting strokes

    :param path: Path, (optional)
    :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path (optional)
    :param smooth_stroke_factor: Smooth Stroke Factor, Higher values gives a smoother stroke (in [0.5, 0.99], optional)
    :param smooth_stroke_radius: Smooth Stroke Radius, Minimum distance from last point before selection continues (in [10, 200], optional)
    :return: Result of the operator call.
    """

def texture_gradient(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xstart: int | None = 0,
    xend: int | None = 0,
    ystart: int | None = 0,
    yend: int | None = 0,
    flip: bool | None = False,
    cursor: int | None = 5,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Draw a line to set the fill material gradient for the selected strokes

    :param xstart: X Start, (in [-inf, inf], optional)
    :param xend: X End, (in [-inf, inf], optional)
    :param ystart: Y Start, (in [-inf, inf], optional)
    :param yend: Y End, (in [-inf, inf], optional)
    :param flip: Flip, (optional)
    :param cursor: Cursor, Mouse cursor style to use during the modal operator (in [0, inf], optional)
    :return: Result of the operator call.
    """

def trace_image(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    target: typing.Literal["NEW", "SELECTED"] | None = "NEW",
    radius: float | None = 0.01,
    threshold: float | None = 0.5,
    turnpolicy: typing.Literal[
        "FOREGROUND", "BACKGROUND", "LEFT", "RIGHT", "MINORITY", "MAJORITY", "RANDOM"
    ]
    | None = "MINORITY",
    mode: typing.Literal["SINGLE", "SEQUENCE"] | None = "SINGLE",
    use_current_frame: bool | None = True,
    frame_number: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extract Grease Pencil strokes from image

        :param target: Target Object, Target Grease Pencil (optional)
        :param radius: Radius, (in [0.001, 1], optional)
        :param threshold: Color Threshold, Determine the lightness threshold above which strokes are generated (in [0, 1], optional)
        :param turnpolicy: Turn Policy, Determines how to resolve ambiguities during decomposition of bitmaps into paths (optional)

    FOREGROUND
    Foreground -- Prefers to connect foreground components.

    BACKGROUND
    Background -- Prefers to connect background components.

    LEFT
    Left -- Always take a left turn.

    RIGHT
    Right -- Always take a right turn.

    MINORITY
    Minority -- Prefers to connect the color that occurs least frequently in the local neighborhood of the current position.

    MAJORITY
    Majority -- Prefers to connect the color that occurs most frequently in the local neighborhood of the current position.

    RANDOM
    Random -- Choose pseudo-randomly.
        :param mode: Mode, Determines if trace simple image or full sequence (optional)

    SINGLE
    Single -- Trace the current frame of the image.

    SEQUENCE
    Sequence -- Trace full sequence.
        :param use_current_frame: Start At Current Frame, Trace Image starting in current image frame (optional)
        :param frame_number: Trace Frame, Used to trace only one frame of the image sequence, set to zero to trace all (in [0, 9999], optional)
        :return: Result of the operator call.
    """

def vertex_brush_stroke(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    stroke=None,
    mode: typing.Literal["NORMAL", "INVERT"] | None = "NORMAL",
    brush_toggle: typing.Literal["None", "SMOOTH", "ERASE", "MASK"] | None = "None",
    pen_flip: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Draw on vertex colors in the active Grease Pencil object

        :param stroke: Stroke, (optional)
        :param mode: Stroke Mode, Action taken when a paint stroke is made (optional)

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.
        :param brush_toggle: Temporary Brush Toggle Type, Brush to use for duration of stroke (optional)

    None
    None -- Apply brush normally.

    SMOOTH
    Smooth -- Switch to smooth brush for duration of stroke.

    ERASE
    Erase -- Switch to erase brush for duration of stroke.

    MASK
    Mask -- Switch to mask brush for duration of stroke.
        :param pen_flip: Pen Flip, Whether a tablets eraser mode is being used (optional)
        :return: Result of the operator call.
    """

def vertex_color_brightness_contrast(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    brightness: float | None = 0.0,
    contrast: float | None = 0.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Adjust vertex color brightness/contrast

    :param mode: Mode, (optional)
    :param brightness: Brightness, (in [-1, 1], optional)
    :param contrast: Contrast, (in [-1, 1], optional)
    :return: Result of the operator call.
    """

def vertex_color_hsv(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    h: float | None = 0.5,
    s: float | None = 1.0,
    v: float | None = 1.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Adjust vertex color HSV values

    :param mode: Mode, (optional)
    :param h: Hue, (in [0, 1], optional)
    :param s: Saturation, (in [0, 2], optional)
    :param v: Value, (in [0, 2], optional)
    :return: Result of the operator call.
    """

def vertex_color_invert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Invert RGB values

    :param mode: Mode, (optional)
    :return: Result of the operator call.
    """

def vertex_color_levels(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    offset: float | None = 0.0,
    gain: float | None = 1.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Adjust levels of vertex colors

    :param mode: Mode, (optional)
    :param offset: Offset, Value to add to colors (in [-1, 1], optional)
    :param gain: Gain, Value to multiply colors by (in [0, inf], optional)
    :return: Result of the operator call.
    """

def vertex_color_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["STROKE", "FILL", "BOTH"] | None = "BOTH",
    factor: float | None = 1.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set active color to all selected vertex

    :param mode: Mode, (optional)
    :param factor: Factor, Mix Factor (in [0, 1], optional)
    :return: Result of the operator call.
    """

def vertex_group_normalize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Normalize weights of the active vertex group

    :return: Result of the operator call.
    """

def vertex_group_normalize_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    lock_active: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Normalize the weights of all vertex groups, so that for each vertex, the sum of all weights is 1.0

    :param lock_active: Lock Active, Keep the values of the active group while normalizing others (optional)
    :return: Result of the operator call.
    """

def vertex_group_smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    factor: float | None = 0.5,
    repeat: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Smooth the weights of the active vertex group

    :param factor: Factor, (in [0, 1], optional)
    :param repeat: Iterations, (in [1, 10000], optional)
    :return: Result of the operator call.
    """

def vertexmode_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    back: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enter/Exit vertex paint mode for Grease Pencil strokes

    :param back: Return to Previous Mode, Return to previous mode (optional)
    :return: Result of the operator call.
    """

def weight_brush_stroke(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    stroke=None,
    mode: typing.Literal["NORMAL", "INVERT"] | None = "NORMAL",
    brush_toggle: typing.Literal["None", "SMOOTH", "ERASE", "MASK"] | None = "None",
    pen_flip: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Draw weight on stroke points in the active Grease Pencil object

        :param stroke: Stroke, (optional)
        :param mode: Stroke Mode, Action taken when a paint stroke is made (optional)

    NORMAL
    Regular -- Apply brush normally.

    INVERT
    Invert -- Invert action of brush for duration of stroke.
        :param brush_toggle: Temporary Brush Toggle Type, Brush to use for duration of stroke (optional)

    None
    None -- Apply brush normally.

    SMOOTH
    Smooth -- Switch to smooth brush for duration of stroke.

    ERASE
    Erase -- Switch to erase brush for duration of stroke.

    MASK
    Mask -- Switch to mask brush for duration of stroke.
        :param pen_flip: Pen Flip, Whether a tablets eraser mode is being used (optional)
        :return: Result of the operator call.
    """

def weight_invert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Invert the weight of active vertex group

    :return: Result of the operator call.
    """

def weight_sample(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the weight of the Draw tool to the weight of the vertex under the mouse cursor

    :return: Result of the operator call.
    """

def weight_toggle_direction(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle Add/Subtract for the weight paint draw tool

    :return: Result of the operator call.
    """

def weightmode_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    back: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enter/Exit weight paint mode for Grease Pencil strokes

    :param back: Return to Previous Mode, Return to previous mode (optional)
    :return: Result of the operator call.
    """
