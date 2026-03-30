import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums
import bpy.types

class _CLS_bake_keys(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add keyframes on every frame between the selected keyframes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_clean(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        threshold: float | None = 0.001,
        channels: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Simplify F-Curves by removing closely spaced keyframes

        :param execution_context:
        :param undo:
        :param threshold: Threshold, (in [0, inf], optional)
        :param channels: Channels, (optional)
        :return: Result of the operator call.
        """

class _CLS_clickselect(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        wait_to_deselect_others: bool | None = False,
        use_select_on_click: bool | None = False,
        mouse_x: int | None = 0,
        mouse_y: int | None = 0,
        extend: bool | None = False,
        deselect_all: bool | None = False,
        column: bool | None = False,
        channel: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select keyframes by clicking on them

        :param execution_context:
        :param undo:
        :param wait_to_deselect_others: Wait to Deselect Others, (optional)
        :param use_select_on_click: Act on Click, Instead of selecting on mouse press, wait to see if theres drag event. Otherwise select on mouse release (optional)
        :param mouse_x: Mouse X, (in [-inf, inf], optional)
        :param mouse_y: Mouse Y, (in [-inf, inf], optional)
        :param extend: Extend Select, Toggle keyframe selection instead of leaving newly selected keyframes only (optional)
        :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
        :param column: Column Select, Select all keyframes that occur on the same frame as the one under the mouse (optional)
        :param channel: Only Channel, Select all the keyframes in the channel under the mouse (optional)
        :return: Result of the operator call.
        """

class _CLS_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy selected keyframes to the internal clipboard

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
        """Remove all selected keyframes

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
        """Make a copy of all selected keyframes

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
        ACTION_OT_duplicate: dict[str, typing.Any] | None = {},
        TRANSFORM_OT_transform: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make a copy of all selected keyframes and move them

        :param execution_context:
        :param undo:
        :param ACTION_OT_duplicate: Duplicate Keyframes, Make a copy of all selected keyframes (optional, `bpy.ops.action.duplicate` keyword arguments)
        :param TRANSFORM_OT_transform: Transform, Transform selected items by mode type (optional, `bpy.ops.transform.transform` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_easing_type(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            bpy.stub_internal.rna_enums.BeztripleInterpolationEasingItems
        ]
        | None = "AUTO",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set easing type for the F-Curve segments starting from the selected keyframes

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_extrapolation_type(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["CONSTANT", "LINEAR", "MAKE_CYCLIC", "CLEAR_CYCLIC"]
        | None = "CONSTANT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set extrapolation mode for selected F-Curves

                :param execution_context:
                :param undo:
                :param type: Type, (optional)

        CONSTANT
        Constant Extrapolation -- Values on endpoint keyframes are held.

        LINEAR
        Linear Extrapolation -- Straight-line slope of end segments are extended past the endpoint keyframes.

        MAKE_CYCLIC
        Make Cyclic (F-Modifier) -- Add Cycles F-Modifier if one does not exist already.

        CLEAR_CYCLIC
        Clear Cyclic (F-Modifier) -- Remove Cycles F-Modifier if not needed anymore.
                :return: Result of the operator call.
        """

class _CLS_frame_jump(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the current frame to the average frame value of selected keyframes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_handle_type(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[bpy.stub_internal.rna_enums.KeyframeHandleTypeItems]
        | None = "FREE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set type of handle for selected keyframes

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_interpolation_type(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            bpy.stub_internal.rna_enums.BeztripleInterpolationModeItems
        ]
        | None = "CONSTANT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set interpolation mode for the F-Curve segments starting from the selected keyframes

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_keyframe_insert(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["ALL", "SEL", "GROUP"] | None = "ALL",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Insert keyframes for the specified channels

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_keyframe_type(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[bpy.stub_internal.rna_enums.BeztripleKeyframeTypeItems]
        | None = "KEYFRAME",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set type of keyframe for the selected keyframes

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_markers_make_local(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move selected scene markers to the active Action as local pose markers

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_mirror(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["CFRA", "XAXIS", "MARKER"] | None = "CFRA",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Flip selected keyframes over the selected mirror line

                :param execution_context:
                :param undo:
                :param type: Type, (optional)

        CFRA
        By Times Over Current Frame -- Flip times of selected keyframes using the current frame as the mirror line.

        XAXIS
        By Values Over Zero Value -- Flip values of selected keyframes (i.e. negative values become positive, and vice versa).

        MARKER
        By Times Over First Selected Marker -- Flip times of selected keyframes using the first selected marker as the reference point.
                :return: Result of the operator call.
        """

class _CLS_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create new action

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
        offset: typing.Literal[bpy.stub_internal.rna_enums.KeyframePasteOffsetItems]
        | None = "START",
        merge: typing.Literal[bpy.stub_internal.rna_enums.KeyframePasteMergeItems]
        | None = "MIX",
        flipped: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste keyframes from the internal clipboard for the selected channels, starting on the current frame

        :param execution_context:
        :param undo:
        :param offset: Offset, Paste time offset of keys (optional)
        :param merge: Type, Method of merging pasted keys and existing (optional)
        :param flipped: Flipped, Paste keyframes from mirrored bones if they exist (optional)
        :return: Result of the operator call.
        """

class _CLS_previewrange_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set Preview Range based on extents of selected Keyframes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_push_down(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Push action down on to the NLA stack as a new strip

        :param execution_context:
        :param undo:
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
        """Toggle selection of all keyframes

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
        axis_range: bool | None = False,
        xmin: int | None = 0,
        xmax: int | None = 0,
        ymin: int | None = 0,
        ymax: int | None = 0,
        wait_for_input: bool | None = True,
        mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
        tweak: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select all keyframes within the specified region

                :param execution_context:
                :param undo:
                :param axis_range: Axis Range, (optional)
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
                :param tweak: Tweak, Operator has been activated using a click-drag event (optional)
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
        """Select keyframe points using circle selection

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

class _CLS_select_column(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        mode: typing.Literal["KEYS", "CFRA", "MARKERS_COLUMN", "MARKERS_BETWEEN"]
        | None = "KEYS",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select all keyframes on the specified frame(s)

        :param execution_context:
        :param undo:
        :param mode: Mode, (optional)
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
        """Select keyframe points using lasso selection

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

class _CLS_select_leftright(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        mode: typing.Literal["CHECK", "LEFT", "RIGHT"] | None = "CHECK",
        extend: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select keyframes to the left or the right of the current frame

        :param execution_context:
        :param undo:
        :param mode: Mode, (optional)
        :param extend: Extend Select, (optional)
        :return: Result of the operator call.
        """

class _CLS_select_less(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Deselect keyframes on ends of selection islands

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
        """Select keyframes occurring in the same F-Curves as selected ones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_more(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select keyframes beside already selected ones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_snap(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "CFRA", "NEAREST_FRAME", "NEAREST_SECOND", "NEAREST_MARKER"
        ]
        | None = "CFRA",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Snap selected keyframes to the times specified

                :param execution_context:
                :param undo:
                :param type: Type, (optional)

        CFRA
        Selection to Current Frame -- Snap selected keyframes to the current frame.

        NEAREST_FRAME
        Selection to Nearest Frame -- Snap selected keyframes to the nearest (whole) frame (use to fix accidental subframe offsets).

        NEAREST_SECOND
        Selection to Nearest Second -- Snap selected keyframes to the nearest second.

        NEAREST_MARKER
        Selection to Nearest Marker -- Snap selected keyframes to the nearest marker.
                :return: Result of the operator call.
        """

class _CLS_stash(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        create_new: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Store this action in the NLA stack as a non-contributing strip for later use

        :param execution_context:
        :param undo:
        :param create_new: Create New Action, Create a new action once the existing one has been safely stored (optional)
        :return: Result of the operator call.
        """

class _CLS_stash_and_create(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Store this action in the NLA stack as a non-contributing strip for later use, and create a new action

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
        *,
        force_delete: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Unlink this action from the active action slot (and/or exit Tweak Mode)

        :param execution_context:
        :param undo:
        :param force_delete: Force Delete, Clear Fake User and remove copy stashed in this data-blocks NLA stack (optional)
        :return: Result of the operator call.
        """

class _CLS_view_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset viewable area to show full keyframe range

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_frame(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the view to the current frame

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_view_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset viewable area to show selected keyframes range

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

bake_keys: _CLS_bake_keys

clean: _CLS_clean

clickselect: _CLS_clickselect

copy: _CLS_copy

delete: _CLS_delete

duplicate: _CLS_duplicate

duplicate_move: _CLS_duplicate_move

easing_type: _CLS_easing_type

extrapolation_type: _CLS_extrapolation_type

frame_jump: _CLS_frame_jump

handle_type: _CLS_handle_type

interpolation_type: _CLS_interpolation_type

keyframe_insert: _CLS_keyframe_insert

keyframe_type: _CLS_keyframe_type

markers_make_local: _CLS_markers_make_local

mirror: _CLS_mirror

new: _CLS_new

paste: _CLS_paste

previewrange_set: _CLS_previewrange_set

push_down: _CLS_push_down

select_all: _CLS_select_all

select_box: _CLS_select_box

select_circle: _CLS_select_circle

select_column: _CLS_select_column

select_lasso: _CLS_select_lasso

select_leftright: _CLS_select_leftright

select_less: _CLS_select_less

select_linked: _CLS_select_linked

select_more: _CLS_select_more

snap: _CLS_snap

stash: _CLS_stash

stash_and_create: _CLS_stash_and_create

unlink: _CLS_unlink

view_all: _CLS_view_all

view_frame: _CLS_view_frame

view_selected: _CLS_view_selected
