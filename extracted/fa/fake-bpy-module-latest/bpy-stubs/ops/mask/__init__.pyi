import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums
import bpy.types
import mathutils

def add_feather_vertex(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add vertex to feather

    :param location: Location, Location of vertex in normalized space (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_feather_vertex_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    MASK_OT_add_feather_vertex: dict[str, typing.Any] | None = {},
    MASK_OT_slide_point: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new vertex to feather and slide it

    :param MASK_OT_add_feather_vertex: Add Feather Vertex, Add vertex to feather (optional, `bpy.ops.mask.add_feather_vertex` keyword arguments)
    :param MASK_OT_slide_point: Slide Point, Slide control points (optional, `bpy.ops.mask.slide_point` keyword arguments)
    :return: Result of the operator call.
    """

def add_vertex(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add vertex to active spline

    :param location: Location, Location of vertex in normalized space (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def add_vertex_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    MASK_OT_add_vertex: dict[str, typing.Any] | None = {},
    MASK_OT_slide_point: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new vertex and slide it

    :param MASK_OT_add_vertex: Add Vertex, Add vertex to active spline (optional, `bpy.ops.mask.add_vertex` keyword arguments)
    :param MASK_OT_slide_point: Slide Point, Slide control points (optional, `bpy.ops.mask.slide_point` keyword arguments)
    :return: Result of the operator call.
    """

def copy_splines(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected splines to the internal clipboard

    :return: Result of the operator call.
    """

def cyclic_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle cyclic for selected splines

    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected control points or splines

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected control points and segments between them

    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    MASK_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate mask and move

    :param MASK_OT_duplicate: Duplicate Mask, Duplicate selected control points and segments between them (optional, `bpy.ops.mask.duplicate` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def feather_weight_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset the feather weight to zero

    :return: Result of the operator call.
    """

def handle_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["AUTO", "VECTOR", "ALIGNED", "ALIGNED_DOUBLESIDE", "FREE"]
    | None = "AUTO",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set type of handles for selected control points

    :param type: Type, Spline type (optional)
    :return: Result of the operator call.
    """

def hide_view_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reveal temporarily hidden mask layers

    :param select: Select, (optional)
    :return: Result of the operator call.
    """

def hide_view_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Temporarily hide mask layers

    :param unselected: Unselected, Hide unselected rather than selected layers (optional)
    :return: Result of the operator call.
    """

def layer_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the active layer up/down in the list

    :param direction: Direction, Direction to move the active layer (optional)
    :return: Result of the operator call.
    """

def layer_new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new mask layer for masking

    :param name: Name, Name of new mask layer (optional, never None)
    :return: Result of the operator call.
    """

def layer_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove mask layer

    :return: Result of the operator call.
    """

def new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create new mask

    :param name: Name, Name of new mask (optional, never None)
    :return: Result of the operator call.
    """

def normals_make_consistent(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Recalculate the direction of selected handles

    :return: Result of the operator call.
    """

def parent_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear the masks parenting

    :return: Result of the operator call.
    """

def parent_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the masks parenting

    :return: Result of the operator call.
    """

def paste_splines(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste splines from the internal clipboard

    :return: Result of the operator call.
    """

def primitive_circle_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    size: float | None = 100.0,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new circle-shaped spline

    :param size: Size, Size of new primitive (in [-inf, inf], optional)
    :param location: Location, Location of new primitive (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def primitive_square_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    size: float | None = 100.0,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new square-shaped spline

    :param size: Size, Size of new primitive (in [-inf, inf], optional)
    :param location: Location, Location of new primitive (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    deselect: bool | None = False,
    toggle: bool | None = False,
    deselect_all: bool | None = False,
    select_passthrough: bool | None = False,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select spline points

    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :param deselect: Deselect, Remove from selection (optional)
    :param toggle: Toggle Selection, Toggle the selection (optional)
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
    :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected (optional)
    :param location: Location, Location of vertex in normalized space (array of 2 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change selection of all curve points

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
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select curve points using box selection

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
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select curve points using circle selection

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
        :return: Result of the operator call.
    """

def select_lasso(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    path: bpy.types.bpy_prop_collection[bpy.types.OperatorMousePath] | None = None,
    use_smooth_stroke: bool | None = False,
    smooth_stroke_factor: float | None = 0.75,
    smooth_stroke_radius: int | None = 35,
    mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select curve points using lasso selection

        :param path: Path, (optional)
        :param use_smooth_stroke: Stabilize Stroke, Selection lags behind mouse and follows a smoother path (optional)
        :param smooth_stroke_factor: Smooth Stroke Factor, Higher values give a smoother stroke (in [0.5, 0.99], optional)
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
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect spline points at the boundary of each selection region

    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all curve points linked to already selected ones

    :return: Result of the operator call.
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select all points linked to the curve under the mouse cursor

    :param deselect: Deselect, (optional)
    :return: Result of the operator call.
    """

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select more spline points connected to initial selection

    :return: Result of the operator call.
    """

def shape_key_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove mask shape keyframe for active mask layer at the current frame

    :return: Result of the operator call.
    """

def shape_key_feather_reset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset feather weights on all selected points animation values

    :return: Result of the operator call.
    """

def shape_key_insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert mask shape keyframe for active mask layer at the current frame

    :return: Result of the operator call.
    """

def shape_key_rekey(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    location: bool | None = True,
    feather: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Recalculate animation data on selected points for frames selected in the dopesheet

    :param location: Location, (optional)
    :param feather: Feather, (optional)
    :return: Result of the operator call.
    """

def slide_point(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    slide_feather: bool | None = False,
    is_new_point: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Slide control points

    :param slide_feather: Slide Feather, First try to slide feather instead of vertex (optional)
    :param is_new_point: Slide New Point, Newly created vertex is being slid (optional)
    :return: Result of the operator call.
    """

def slide_spline_curvature(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Slide a point on the spline to define its curvature

    :return: Result of the operator call.
    """

def switch_direction(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Switch direction of selected splines

    :return: Result of the operator call.
    """
