import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums
import mathutils

def bbone_resize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | mathutils.Vector | None = (1.0, 1.0, 1.0),
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Scale selected bendy bones display size

    :param value: Display Size, (array of 3 items, in [-inf, inf], optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def bend(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | None = (0.0),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    gpencil_strokes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Bend selected items between the 3D cursor and the mouse

    :param value: Angle, (array of 1 items, in [-inf, inf], optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def create_orientation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    use_view: bool | None = False,
    use: bool | None = False,
    overwrite: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create transformation orientation from selection

    :param name: Name, Name of the new custom orientation (optional, never None)
    :param use_view: Use View, Use the current view instead of the active object to create the new orientation (optional)
    :param use: Use After Creation, Select orientation after its creation (optional)
    :param overwrite: Overwrite Previous, Overwrite previously created orientation with same name (optional)
    :return: Result of the operator call.
    """

def delete_orientation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete transformation orientation

    :return: Result of the operator call.
    """

def edge_bevelweight(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    snap: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the bevel weight of edges

    :param value: Factor, (in [-1, 1], optional)
    :param snap: Use Snapping Options, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def edge_crease(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    snap: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the crease of edges

    :param value: Factor, (in [-1, 1], optional)
    :param snap: Use Snapping Options, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def edge_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    single_side: bool | None = False,
    use_even: bool | None = False,
    flipped: bool | None = False,
    use_clamp: bool | None = True,
    mirror: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    correct_uv: bool | None = True,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Slide an edge loop along a mesh

    :param value: Factor, (in [-10, 10], optional)
    :param single_side: Single Side, (optional)
    :param use_even: Even, Make the edge loop match the shape of the adjacent edge loop (optional)
    :param flipped: Flipped, When Even mode is active, flips between the two adjacent edge loops (optional)
    :param use_clamp: Clamp, Clamp within the edge extents (optional)
    :param mirror: Mirror Editing, (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param correct_uv: Correct UVs, Correct UV coordinates when transforming (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def from_gizmo(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Transform selected items by mode type

    :return: Result of the operator call.
    """

def mirror(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    gpencil_strokes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mirror selected items around one or more axes

    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def push_pull(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Push/Pull selected items

    :param value: Distance, (in [-inf, inf], optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def resize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | mathutils.Vector | None = (1.0, 1.0, 1.0),
    mouse_dir_constraint: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    gpencil_strokes: bool | None = False,
    texture_space: bool | None = False,
    remove_on_cancel: bool | None = False,
    use_duplicated_keyframes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Scale (resize) selected items

    :param value: Scale, (array of 3 items, in [-inf, inf], optional)
    :param mouse_dir_constraint: Mouse Directional Constraint, (array of 3 items, in [-inf, inf], optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param texture_space: Edit Texture Space, Edit object data texture space (optional)
    :param remove_on_cancel: Remove on Cancel, Remove elements on cancel (optional)
    :param use_duplicated_keyframes: Duplicated Keyframes, Transform duplicated keyframes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def rotate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    orient_axis: typing.Literal[bpy.stub_internal.rna_enums.AxisXyzItems] | None = "Z",
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    gpencil_strokes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rotate selected items

    :param value: Angle, (in [-inf, inf], optional)
    :param orient_axis: Axis, (optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def rotate_normal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    orient_axis: typing.Literal[bpy.stub_internal.rna_enums.AxisXyzItems] | None = "Z",
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rotate custom normal of selected items

    :param value: Angle, (in [-inf, inf], optional)
    :param orient_axis: Axis, (optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def select_orientation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    orientation: str | None = "GLOBAL",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select transformation orientation

    :param orientation: Orientation, Transformation orientation (optional)
    :return: Result of the operator call.
    """

def seq_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0),
    use_restore_handle_selection: bool | None = False,
    snap: bool | None = False,
    texture_space: bool | None = False,
    remove_on_cancel: bool | None = False,
    use_duplicated_keyframes: bool | None = False,
    view2d_edge_pan: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Slide a sequence strip in time

    :param value: Offset, (array of 2 items, in [-inf, inf], optional)
    :param use_restore_handle_selection: Restore Handle Selection, Restore handle selection after tweaking (optional)
    :param snap: Use Snapping Options, (optional)
    :param texture_space: Edit Texture Space, Edit object data texture space (optional)
    :param remove_on_cancel: Remove on Cancel, Remove elements on cancel (optional)
    :param use_duplicated_keyframes: Duplicated Keyframes, Transform duplicated keyframes (optional)
    :param view2d_edge_pan: Edge Pan, Enable edge panning in 2D view (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def shear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    angle: float | None = 0.0,
    orient_axis: typing.Literal[bpy.stub_internal.rna_enums.AxisXyzItems] | None = "Z",
    orient_axis_ortho: typing.Literal[bpy.stub_internal.rna_enums.AxisXyzItems]
    | None = "X",
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    gpencil_strokes: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Shear selected items along the given axis

    :param angle: Angle, (in [-inf, inf], optional)
    :param orient_axis: Axis, (optional)
    :param orient_axis_ortho: Axis Ortho, (optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def shrink_fatten(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    use_even_offset: bool | None = False,
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Shrink/fatten selected vertices along normals

    :param value: Offset, (in [-inf, inf], optional)
    :param use_even_offset: Offset Even, Scale the offset to give more even thickness (optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def skin_resize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | mathutils.Vector | None = (1.0, 1.0, 1.0),
    orient_type: str | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: str | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Scale selected vertices skin radii

    :param value: Scale, (array of 3 items, in [-inf, inf], optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def tilt(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Tilt selected control vertices of 3D curve

    :param value: Angle, (in [-inf, inf], optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def tosphere(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    gpencil_strokes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move selected items outward in a spherical shape around geometric center

    :param value: Factor, (in [0, 1], optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def trackball(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | None = (0.0, 0.0),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    gpencil_strokes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Trackball style rotation of selected items

    :param value: Angle, (array of 2 items, in [-inf, inf], optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def transform(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal[bpy.stub_internal.rna_enums.TransformModeTypeItems]
    | None = "TRANSLATION",
    value: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
        0.0,
    ),
    orient_axis: typing.Literal[bpy.stub_internal.rna_enums.AxisXyzItems] | None = "Z",
    orient_type: typing.Literal[bpy.stub_internal.rna_enums.TransformOrientationItems]
    | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: typing.Literal[
        bpy.stub_internal.rna_enums.TransformOrientationItems
    ]
    | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    snap_align: bool | None = False,
    snap_normal: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    gpencil_strokes: bool | None = False,
    texture_space: bool | None = False,
    remove_on_cancel: bool | None = False,
    use_duplicated_keyframes: bool | None = False,
    center_override: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
    use_automerge_and_split: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Transform selected items by mode type

    :param mode: Mode, (optional)
    :param value: Values, (array of 4 items, in [-inf, inf], optional)
    :param orient_axis: Axis, (optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param snap_align: Align with Point Normal, (optional)
    :param snap_normal: Normal, (array of 3 items, in [-inf, inf], optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param texture_space: Edit Texture Space, Edit object data texture space (optional)
    :param remove_on_cancel: Remove on Cancel, Remove elements on cancel (optional)
    :param use_duplicated_keyframes: Duplicated Keyframes, Transform duplicated keyframes (optional)
    :param center_override: Center Override, Force using this center value (when set) (array of 3 items, in [-inf, inf], optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :param use_automerge_and_split: Auto Merge & Split, Forces the use of Auto Merge and Split (optional)
    :return: Result of the operator call.
    """

def translate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
    orient_type: typing.Literal[bpy.stub_internal.rna_enums.TransformOrientationItems]
    | None = "GLOBAL",
    orient_matrix: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = ((0.0, 0.0, 0.0), (0.0, 0.0, 0.0), (0.0, 0.0, 0.0)),
    orient_matrix_type: typing.Literal[
        bpy.stub_internal.rna_enums.TransformOrientationItems
    ]
    | None = "GLOBAL",
    constraint_axis: collections.abc.Sequence[bool] | None = (False, False, False),
    mirror: bool | None = False,
    use_proportional_edit: bool | None = False,
    proportional_edit_falloff: typing.Literal[
        bpy.stub_internal.rna_enums.ProportionalFalloffItems
    ]
    | None = "SMOOTH",
    proportional_size: float | None = 1.0,
    use_proportional_connected: bool | None = False,
    use_proportional_projected: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    snap_align: bool | None = False,
    snap_normal: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    gpencil_strokes: bool | None = False,
    cursor_transform: bool | None = False,
    texture_space: bool | None = False,
    remove_on_cancel: bool | None = False,
    use_duplicated_keyframes: bool | None = False,
    view2d_edge_pan: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
    use_automerge_and_split: bool | None = False,
    translate_origin: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move selected items

    :param value: Move, (array of 3 items, in [-inf, inf], optional)
    :param orient_type: Orientation, Transformation orientation (optional)
    :param orient_matrix: Matrix, (multi-dimensional array of 3 * 3 items, in [-inf, inf], optional)
    :param orient_matrix_type: Matrix Orientation, (optional)
    :param constraint_axis: Constraint Axis, (array of 3 items, optional)
    :param mirror: Mirror Editing, (optional)
    :param use_proportional_edit: Proportional Editing, (optional)
    :param proportional_edit_falloff: Proportional Falloff, Falloff type for proportional editing mode (optional)
    :param proportional_size: Proportional Size, (in [1e-06, inf], optional)
    :param use_proportional_connected: Connected, (optional)
    :param use_proportional_projected: Projected (2D), (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param snap_align: Align with Point Normal, (optional)
    :param snap_normal: Normal, (array of 3 items, in [-inf, inf], optional)
    :param gpencil_strokes: Edit Grease Pencil, Edit selected Grease Pencil strokes (optional)
    :param cursor_transform: Transform Cursor, (optional)
    :param texture_space: Edit Texture Space, Edit object data texture space (optional)
    :param remove_on_cancel: Remove on Cancel, Remove elements on cancel (optional)
    :param use_duplicated_keyframes: Duplicated Keyframes, Transform duplicated keyframes (optional)
    :param view2d_edge_pan: Edge Pan, Enable edge panning in 2D view (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :param use_automerge_and_split: Auto Merge & Split, Forces the use of Auto Merge and Split (optional)
    :param translate_origin: Translate Origin, Translate origin instead of selection (optional)
    :return: Result of the operator call.
    """

def vert_crease(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    snap: bool | None = False,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the crease of vertices

    :param value: Factor, (in [-1, 1], optional)
    :param snap: Use Snapping Options, (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def vert_slide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: float | None = 0.0,
    use_even: bool | None = False,
    flipped: bool | None = False,
    use_clamp: bool | None = True,
    direction: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    mirror: bool | None = False,
    snap: bool | None = False,
    snap_elements: set[typing.Literal[bpy.stub_internal.rna_enums.SnapElementItems]]
    | None = {"INCREMENT"},
    use_snap_project: bool | None = False,
    snap_target: typing.Literal[bpy.stub_internal.rna_enums.SnapSourceItems]
    | None = "CLOSEST",
    use_snap_self: bool | None = True,
    use_snap_edit: bool | None = True,
    use_snap_nonedit: bool | None = True,
    use_snap_selectable: bool | None = False,
    snap_point: collections.abc.Sequence[float] | mathutils.Vector | None = (
        0.0,
        0.0,
        0.0,
    ),
    correct_uv: bool | None = True,
    release_confirm: bool | None = False,
    use_accurate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Slide a vertex along a mesh

    :param value: Factor, (in [-10, 10], optional)
    :param use_even: Even, Make the edge loop match the shape of the adjacent edge loop (optional)
    :param flipped: Flipped, When Even mode is active, flips between the two adjacent edge loops (optional)
    :param use_clamp: Clamp, Clamp within the edge extents (optional)
    :param direction: Slide Direction, World-space direction (array of 3 items, in [-inf, inf], optional)
    :param mirror: Mirror Editing, (optional)
    :param snap: Use Snapping Options, (optional)
    :param snap_elements: Snap to Elements, (optional)
    :param use_snap_project: Project Individual Elements, (optional)
    :param snap_target: Snap Base, Point on source that will snap to target (optional)
    :param use_snap_self: Target: Include Active, (optional)
    :param use_snap_edit: Target: Include Edit, (optional)
    :param use_snap_nonedit: Target: Include Non-Edited, (optional)
    :param use_snap_selectable: Target: Exclude Non-Selectable, (optional)
    :param snap_point: Point, (array of 3 items, in [-inf, inf], optional)
    :param correct_uv: Correct UVs, Correct UV coordinates when transforming (optional)
    :param release_confirm: Confirm on Release, Always confirm operation when releasing button (optional)
    :param use_accurate: Accurate, Use accurate transformation (optional)
    :return: Result of the operator call.
    """

def vertex_random(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    offset: float | None = 0.0,
    uniform: float | None = 0.0,
    normal: float | None = 0.0,
    seed: int | None = 0,
    wait_for_input: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Randomize vertices

    :param offset: Amount, Distance to offset (in [-inf, inf], optional)
    :param uniform: Uniform, Increase for uniform offset distance (in [0, 1], optional)
    :param normal: Normal, Align offset direction to normals (in [0, 1], optional)
    :param seed: Random Seed, Seed for the random number generator (in [0, 10000], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def vertex_warp(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    warp_angle: float | None = 6.28319,
    offset_angle: float | None = 0.0,
    min: float | None = -1.0,
    max: float | None = 1.0,
    viewmat: collections.abc.Sequence[collections.abc.Sequence[float]]
    | mathutils.Matrix
    | None = (
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
        (0.0, 0.0, 0.0, 0.0),
    ),
    center: collections.abc.Sequence[float] | mathutils.Vector | None = (0.0, 0.0, 0.0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Warp vertices around the cursor

    :param warp_angle: Warp Angle, Amount to warp about the cursor (in [-inf, inf], optional)
    :param offset_angle: Offset Angle, Angle to use as the basis for warping (in [-inf, inf], optional)
    :param min: Min, (in [-inf, inf], optional)
    :param max: Max, (in [-inf, inf], optional)
    :param viewmat: Matrix, (multi-dimensional array of 4 * 4 items, in [-inf, inf], optional)
    :param center: Center, (array of 3 items, in [-inf, inf], optional)
    :return: Result of the operator call.
    """
