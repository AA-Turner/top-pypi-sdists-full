import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums
import mathutils

def cyclic_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["CYCLIC_U", "CYCLIC_V"] | None = "CYCLIC_U",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make active spline closed/open loop

    :param direction: Direction, Direction to make surface cyclic in (optional)
    :return: Result of the operator call.
    """

def de_select_first(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select first of visible part of each NURBS

    :return: Result of the operator call.
    """

def de_select_last(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select last of visible part of each NURBS

    :return: Result of the operator call.
    """

def decimate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 1.0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Simplify selected curves

    :param ratio: Ratio, (in [0, 1], optional)
    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["VERT", "SEGMENT"] | None = "VERT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected control points or segments

    :param type: Type, Which elements to delete (optional)
    :return: Result of the operator call.
    """

def dissolve_verts(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected control points, correcting surrounding handles

    :return: Result of the operator call.
    """

def draw(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    error_threshold: float | None = 0.0,
    fit_method: typing.Literal[bpy.stub_internal.rna_enums.CurveFitMethodItems]
    | None = "REFIT",
    corner_angle: float | None = 1.22173,
    use_cyclic: bool | None = True,
    stroke=None,
    wait_for_input: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Draw a freehand spline

    :param error_threshold: Error, Error distance threshold (in object units) (in [0, 10], optional)
    :param fit_method: Fit Method, (optional)
    :param corner_angle: Corner Angle, (in [0, 3.14159], optional)
    :param use_cyclic: Cyclic, (optional)
    :param stroke: Stroke, (optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected control points

    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    CURVE_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate curve and move

    :param CURVE_OT_duplicate: Duplicate Curve, Duplicate selected control points (optional, `bpy.ops.curve.duplicate` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def extrude(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal[bpy.stub_internal.rna_enums.TransformModeTypeItems]
    | None = "TRANSLATION",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude selected control point(s)

    :param mode: Mode, (optional)
    :return: Result of the operator call.
    """

def extrude_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    CURVE_OT_extrude: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude curve and move result

    :param CURVE_OT_extrude: Extrude, Extrude selected control point(s) (optional, `bpy.ops.curve.extrude` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def handle_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "AUTOMATIC", "VECTOR", "ALIGNED", "FREE_ALIGN", "TOGGLE_FREE_ALIGN"
    ]
    | None = "AUTOMATIC",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set type of handles for selected control points

    :param type: Type, Spline type (optional)
    :return: Result of the operator call.
    """

def hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide (un)selected control points

    :param unselected: Unselected, Hide unselected rather than selected (optional)
    :return: Result of the operator call.
    """

def make_segment(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Join two curves by their selected ends

    :return: Result of the operator call.
    """

def match_texture_space(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Match texture space to objects bounding box

    :return: Result of the operator call.
    """

def normals_make_consistent(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    calc_length: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Recalculate the direction of selected handles

    :param calc_length: Length, Recalculate handle length (optional)
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
    close_spline: bool | None = True,
    close_spline_method: typing.Literal["OFF", "ON_PRESS", "ON_CLICK"] | None = "OFF",
    toggle_vector: bool | None = False,
    cycle_handle_type: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
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
        :param move_segment: Move Segment, Move an existing curve segment (optional)
        :param select_point: Select Point, Select a point or its handles (optional)
        :param move_point: Move Point, Move a point or its handles (optional)
        :param close_spline: Close Spline, Make a spline cyclic by clicking endpoints (optional)
        :param close_spline_method: Close Spline Method, The condition for close spline to activate (optional)

    OFF
    None.

    ON_PRESS
    On Press -- Move handles after closing the spline.

    ON_CLICK
    On Click -- Spline closes on release if not dragged.
        :param toggle_vector: Toggle Vector, Toggle between Vector and Auto handles (optional)
        :param cycle_handle_type: Cycle Handle Type, Cycle between all four handle types (optional)
        :return: Result of the operator call.
    """

def primitive_bezier_circle_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a Bézier Circle

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_bezier_curve_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a Bézier Curve

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_circle_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a Nurbs Circle

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_curve_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a Nurbs Curve

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def primitive_nurbs_path_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
    enter_editmode: bool | None = False,
    align: typing.Literal["WORLD", "VIEW", "CURSOR"] | None = "WORLD",
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    rotation: collections.abc.Sequence[float] | mathutils.Euler | None = (
        0.0,
        0.0,
        0.0,
    ),
    scale: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Construct a Path

        :param radius: Radius, (in [0, inf], optional)
        :param enter_editmode: Enter Edit Mode, Enter edit mode when adding this object (optional)
        :param align: Align, The alignment of the new object (optional)

    WORLD
    World -- Align the new object to the world.

    VIEW
    View -- Align the new object to the view.

    CURSOR
    3D Cursor -- Use the 3D cursor orientation for the new object.
        :param location: Location, Location for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param rotation: Rotation, Rotation for the newly added object (array of 3 items, in [-inf, inf], optional)
        :param scale: Scale, Scale for the newly added object (array of 3 items, in [-inf, inf], optional)
        :return: Result of the operator call.
    """

def radius_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    radius: float | None = 1.0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set per-point radius which is used for bevel tapering

    :param radius: Radius, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reveal hidden control points

    :param select: Select, (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select all control points

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

def select_less(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect control points at the boundary of each selection region

    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all control points linked to the current selection

    :return: Result of the operator call.
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all control points linked to already selected ones

    :param deselect: Deselect, Deselect linked control points rather than selecting them (optional)
    :return: Result of the operator call.
    """

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select control points at the boundary of each selection region

    :return: Result of the operator call.
    """

def select_next(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select control points following already selected ones along the curves

    :return: Result of the operator call.
    """

def select_nth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    skip: int | None = 1,
    nth: int | None = 1,
    offset: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect every Nth point starting from the active one

    :param skip: Deselected, Number of deselected elements in the repetitive sequence (in [1, inf], optional)
    :param nth: Selected, Number of selected elements in the repetitive sequence (in [1, inf], optional)
    :param offset: Offset, Offset from the starting point (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def select_previous(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select control points preceding already selected ones along the curves

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
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Randomly select some control points

        :param ratio: Ratio, Portion of items to select randomly (in [0, 1], optional)
        :param seed: Random Seed, Seed for the random number generator (in [0, inf], optional)
        :param action: Action, Selection action to execute (optional)

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :return: Result of the operator call.
    """

def select_row(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select a row of control points including active one. Successive use on the same point switches between U/V directions

    :return: Result of the operator call.
    """

def select_similar(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["TYPE", "RADIUS", "WEIGHT", "DIRECTION"] | None = "WEIGHT",
    compare: typing.Literal["EQUAL", "GREATER", "LESS"] | None = "EQUAL",
    threshold: float | None = 0.1,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select similar curve points by property type

    :param type: Type, (optional)
    :param compare: Compare, (optional)
    :param threshold: Threshold, (in [0, inf], optional)
    :return: Result of the operator call.
    """

def separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Separate selected points from connected unselected points into a new object

    :return: Result of the operator call.
    """

def shade_flat(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set shading to flat

    :return: Result of the operator call.
    """

def shade_smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set shading to smooth

    :return: Result of the operator call.
    """

def shortest_path_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select shortest path between two selections

    :return: Result of the operator call.
    """

def smooth(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Flatten angles of selected points

    :return: Result of the operator call.
    """

def smooth_radius(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interpolate radii of selected points

    :return: Result of the operator call.
    """

def smooth_tilt(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interpolate tilt of selected points

    :return: Result of the operator call.
    """

def smooth_weight(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interpolate weight of selected points

    :return: Result of the operator call.
    """

def spin(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    center: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    axis: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Extrude selected boundary row around pivot point and current view axis

    :param center: Center, Center in global view space (array of 3 items, in [-inf, inf], optional)
    :param axis: Axis, Axis in global view space (array of 3 items, in [-1, 1], optional)
    :return: Result of the operator call.
    """

def spline_type_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["POLY", "BEZIER", "NURBS"] | None = "POLY",
    use_handles: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set type of active spline

    :param type: Type, Spline type (optional)
    :param use_handles: Handles, Use handles when converting Bézier curves into polygons (optional)
    :return: Result of the operator call.
    """

def spline_weight_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    weight: float | None = 1.0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set softbody goal weight for selected points

    :param weight: Weight, (in [0, 1], optional)
    :return: Result of the operator call.
    """

def split(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split off selected points from connected unselected points

    :return: Result of the operator call.
    """

def subdivide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    number_cuts: int | None = 1,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Subdivide selected segments

    :param number_cuts: Number of Cuts, (in [1, 1000], optional)
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

def tilt_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear the tilt of selected control points

    :return: Result of the operator call.
    """

def vertex_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    location: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new control point (linked to only selected end-curve one, if any)

    :param location: Location, Location to add new vertex at (array of 3 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """
