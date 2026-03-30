import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums
import bpy.types
import mathutils

class _CLS_add_feather_vertex(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        location: collections.abc.Sequence[float] | mathutils.Vector | None = (
            0.0,
            0.0,
        ),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add vertex to feather

        :param execution_context:
        :param undo:
        :param location: Location, Location of vertex in normalized space (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_feather_vertex_slide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        MASK_OT_add_feather_vertex: dict[str, typing.Any] | None = {},
        MASK_OT_slide_point: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new vertex to feather and slide it

        :param execution_context:
        :param undo:
        :param MASK_OT_add_feather_vertex: Add Feather Vertex, Add vertex to feather (optional, `bpy.ops.mask.add_feather_vertex` keyword arguments)
        :param MASK_OT_slide_point: Slide Point, Slide control points (optional, `bpy.ops.mask.slide_point` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_add_vertex(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        location: collections.abc.Sequence[float] | mathutils.Vector | None = (
            0.0,
            0.0,
        ),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add vertex to active spline

        :param execution_context:
        :param undo:
        :param location: Location, Location of vertex in normalized space (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_add_vertex_slide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        MASK_OT_add_vertex: dict[str, typing.Any] | None = {},
        MASK_OT_slide_point: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new vertex and slide it

        :param execution_context:
        :param undo:
        :param MASK_OT_add_vertex: Add Vertex, Add vertex to active spline (optional, `bpy.ops.mask.add_vertex` keyword arguments)
        :param MASK_OT_slide_point: Slide Point, Slide control points (optional, `bpy.ops.mask.slide_point` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_copy_splines(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the selected splines to the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_cyclic_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle cyclic for selected splines

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
        confirm: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete selected control points or splines

        :param execution_context:
        :param undo:
        :param confirm: Confirm, Prompt for confirmation (optional)
        :return: Result of the operator call.
        """

class _CLS_duplicate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate selected control points and segments between them

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_duplicate_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        MASK_OT_duplicate: dict[str, typing.Any] | None = {},
        TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate mask and move

        :param execution_context:
        :param undo:
        :param MASK_OT_duplicate: Duplicate Mask, Duplicate selected control points and segments between them (optional, `bpy.ops.mask.duplicate` keyword arguments)
        :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_feather_weight_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset the feather weight to zero

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_handle_type_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["AUTO", "VECTOR", "ALIGNED", "ALIGNED_DOUBLESIDE", "FREE"]
        | None = "AUTO",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set type of handles for selected control points

        :param execution_context:
        :param undo:
        :param type: Type, Spline type (optional)
        :return: Result of the operator call.
        """

class _CLS_hide_view_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        select: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reveal temporarily hidden mask layers

        :param execution_context:
        :param undo:
        :param select: Select, (optional)
        :return: Result of the operator call.
        """

class _CLS_hide_view_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        unselected: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Temporarily hide mask layers

        :param execution_context:
        :param undo:
        :param unselected: Unselected, Hide unselected rather than selected layers (optional)
        :return: Result of the operator call.
        """

class _CLS_layer_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the active layer up/down in the list

        :param execution_context:
        :param undo:
        :param direction: Direction, Direction to move the active layer (optional)
        :return: Result of the operator call.
        """

class _CLS_layer_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new mask layer for masking

        :param execution_context:
        :param undo:
        :param name: Name, Name of new mask layer (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_layer_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove mask layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_move_to_layer(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        target_layer_name: str = "",
        add_new_layer: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the active spline to layer

        :param execution_context:
        :param undo:
        :param target_layer_name: Name, Target Mask Layer (optional, never None)
        :param add_new_layer: New Layer, Move selection to a new layer (optional)
        :return: Result of the operator call.
        """

class _CLS_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create new mask

        :param execution_context:
        :param undo:
        :param name: Name, Name of new mask (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_normals_make_consistent(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Recalculate the direction of selected handles

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_parent_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear the masks parenting

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_parent_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the masks parenting

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_paste_splines(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste splines from the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_primitive_circle_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        size: float | None = 100.0,
        location: collections.abc.Sequence[float] | mathutils.Vector | None = (
            0.0,
            0.0,
        ),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new circle-shaped spline

        :param execution_context:
        :param undo:
        :param size: Size, Size of new primitive (in [-inf, inf], optional)
        :param location: Location, Location of new primitive (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_primitive_square_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        size: float | None = 100.0,
        location: collections.abc.Sequence[float] | mathutils.Vector | None = (
            0.0,
            0.0,
        ),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new square-shaped spline

        :param execution_context:
        :param undo:
        :param size: Size, Size of new primitive (in [-inf, inf], optional)
        :param location: Location, Location of new primitive (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_select(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        extend: bool | None = False,
        deselect: bool | None = False,
        toggle: bool | None = False,
        deselect_all: bool | None = False,
        select_passthrough: bool | None = False,
        location: collections.abc.Sequence[float] | mathutils.Vector | None = (
            0.0,
            0.0,
        ),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select spline points

        :param execution_context:
        :param undo:
        :param extend: Extend, Extend selection instead of deselecting everything first (optional)
        :param deselect: Deselect, Remove from selection (optional)
        :param toggle: Toggle Selection, Toggle the selection (optional)
        :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
        :param select_passthrough: Only Select Unselected, Ignore the select action when the element is already selected (optional)
        :param location: Location, Location of vertex in normalized space (array of 2 items, in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_select_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"]
        | None = "TOGGLE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Change selection of all curve points

                :param execution_context:
                :param undo:
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

class _CLS_select_box(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

                :param execution_context:
                :param undo:
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

class _CLS_select_circle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

                :param execution_context:
                :param undo:
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

class _CLS_select_lasso(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
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

                :param execution_context:
                :param undo:
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

class _CLS_select_less(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Deselect spline points at the boundary of each selection region

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_linked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select all curve points linked to already selected ones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_linked_pick(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        deselect: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """(De)select all points linked to the curve under the mouse cursor

        :param execution_context:
        :param undo:
        :param deselect: Deselect, (optional)
        :return: Result of the operator call.
        """

class _CLS_select_more(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select more spline points connected to initial selection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_shape_key_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove mask shape keyframe for active mask layer at the current frame

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_shape_key_feather_reset(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset feather weights on all selected points animation values

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_shape_key_insert(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Insert mask shape keyframe for active mask layer at the current frame

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_shape_key_rekey(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        location: bool | None = True,
        feather: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Recalculate animation data on selected points for frames selected in the dopesheet

        :param execution_context:
        :param undo:
        :param location: Location, (optional)
        :param feather: Feather, (optional)
        :return: Result of the operator call.
        """

class _CLS_slide_point(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        slide_feather: bool | None = False,
        is_new_point: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Slide control points

        :param execution_context:
        :param undo:
        :param slide_feather: Slide Feather, First try to slide feather instead of vertex (optional)
        :param is_new_point: Slide New Point, Newly created vertex is being slid (optional)
        :return: Result of the operator call.
        """

class _CLS_slide_spline_curvature(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Slide a point on the spline to define its curvature

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_switch_direction(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Switch direction of selected splines

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

add_feather_vertex: _CLS_add_feather_vertex

add_feather_vertex_slide: _CLS_add_feather_vertex_slide

add_vertex: _CLS_add_vertex

add_vertex_slide: _CLS_add_vertex_slide

copy_splines: _CLS_copy_splines

cyclic_toggle: _CLS_cyclic_toggle

delete: _CLS_delete

duplicate: _CLS_duplicate

duplicate_move: _CLS_duplicate_move

feather_weight_clear: _CLS_feather_weight_clear

handle_type_set: _CLS_handle_type_set

hide_view_clear: _CLS_hide_view_clear

hide_view_set: _CLS_hide_view_set

layer_move: _CLS_layer_move

layer_new: _CLS_layer_new

layer_remove: _CLS_layer_remove

move_to_layer: _CLS_move_to_layer

new: _CLS_new

normals_make_consistent: _CLS_normals_make_consistent

parent_clear: _CLS_parent_clear

parent_set: _CLS_parent_set

paste_splines: _CLS_paste_splines

primitive_circle_add: _CLS_primitive_circle_add

primitive_square_add: _CLS_primitive_square_add

select: _CLS_select

select_all: _CLS_select_all

select_box: _CLS_select_box

select_circle: _CLS_select_circle

select_lasso: _CLS_select_lasso

select_less: _CLS_select_less

select_linked: _CLS_select_linked

select_linked_pick: _CLS_select_linked_pick

select_more: _CLS_select_more

shape_key_clear: _CLS_shape_key_clear

shape_key_feather_reset: _CLS_shape_key_feather_reset

shape_key_insert: _CLS_shape_key_insert

shape_key_rekey: _CLS_shape_key_rekey

slide_point: _CLS_slide_point

slide_spline_curvature: _CLS_slide_spline_curvature

switch_direction: _CLS_switch_direction
