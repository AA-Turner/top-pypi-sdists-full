import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_armature_apply(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        selected: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Apply the current pose as the new rest pose

        :param execution_context:
        :param undo:
        :param selected: Selected Only, Only apply the selected bones (with propagation to children) (optional)
        :return: Result of the operator call.
        """

class _CLS_autoside_names(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        axis: typing.Literal["XAXIS", "YAXIS", "ZAXIS"] | None = "XAXIS",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Automatically renames the selected bones according to which side of the target axis they fall on

                :param execution_context:
                :param undo:
                :param axis: Axis, Axis to tag names with (optional)

        XAXIS
        X-Axis -- Left/Right.

        YAXIS
        Y-Axis -- Front/Back.

        ZAXIS
        Z-Axis -- Top/Bottom.
                :return: Result of the operator call.
        """

class _CLS_blend_to_neighbor(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        factor: float | None = 0.5,
        prev_frame: int | None = 0,
        next_frame: int | None = 0,
        channels: typing.Literal["ALL", "LOC", "ROT", "SIZE", "BBONE", "CUSTOM"]
        | None = "ALL",
        axis_lock: typing.Literal["FREE", "X", "Y", "Z"] | None = "FREE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Blend from current position to previous or next keyframe

                :param execution_context:
                :param undo:
                :param factor: Factor, Weighting factor for which keyframe is favored more (in [0, 1], optional)
                :param prev_frame: Previous Keyframe, Frame number of keyframe immediately before the current frame (in [-1048574, 1048574], optional)
                :param next_frame: Next Keyframe, Frame number of keyframe immediately after the current frame (in [-1048574, 1048574], optional)
                :param channels: Channels, Set of properties that are affected (optional)

        ALL
        All Properties -- All properties, including transforms, bendy bone shape, and custom properties.

        LOC
        Location -- Location only.

        ROT
        Rotation -- Rotation only.

        SIZE
        Scale -- Scale only.

        BBONE
        Bendy Bone -- Bendy Bone shape properties.

        CUSTOM
        Custom Properties -- Custom properties.
                :param axis_lock: Axis Lock, Transform axis to restrict effects to (optional)

        FREE
        Free -- All axes are affected.

        X
        X -- Only X-axis transforms are affected.

        Y
        Y -- Only Y-axis transforms are affected.

        Z
        Z -- Only Z-axis transforms are affected.
                :return: Result of the operator call.
        """

class _CLS_blend_with_rest(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        factor: float | None = 0.5,
        prev_frame: int | None = 0,
        next_frame: int | None = 0,
        channels: typing.Literal["ALL", "LOC", "ROT", "SIZE", "BBONE", "CUSTOM"]
        | None = "ALL",
        axis_lock: typing.Literal["FREE", "X", "Y", "Z"] | None = "FREE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make the current pose more similar to, or further away from, the rest pose

                :param execution_context:
                :param undo:
                :param factor: Factor, Weighting factor for which keyframe is favored more (in [0, 1], optional)
                :param prev_frame: Previous Keyframe, Frame number of keyframe immediately before the current frame (in [-1048574, 1048574], optional)
                :param next_frame: Next Keyframe, Frame number of keyframe immediately after the current frame (in [-1048574, 1048574], optional)
                :param channels: Channels, Set of properties that are affected (optional)

        ALL
        All Properties -- All properties, including transforms, bendy bone shape, and custom properties.

        LOC
        Location -- Location only.

        ROT
        Rotation -- Rotation only.

        SIZE
        Scale -- Scale only.

        BBONE
        Bendy Bone -- Bendy Bone shape properties.

        CUSTOM
        Custom Properties -- Custom properties.
                :param axis_lock: Axis Lock, Transform axis to restrict effects to (optional)

        FREE
        Free -- All axes are affected.

        X
        X -- Only X-axis transforms are affected.

        Y
        Y -- Only Y-axis transforms are affected.

        Z
        Z -- Only Z-axis transforms are affected.
                :return: Result of the operator call.
        """

class _CLS_breakdown(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        factor: float | None = 0.5,
        prev_frame: int | None = 0,
        next_frame: int | None = 0,
        channels: typing.Literal["ALL", "LOC", "ROT", "SIZE", "BBONE", "CUSTOM"]
        | None = "ALL",
        axis_lock: typing.Literal["FREE", "X", "Y", "Z"] | None = "FREE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a suitable breakdown pose on the current frame

                :param execution_context:
                :param undo:
                :param factor: Factor, Weighting factor for which keyframe is favored more (in [0, 1], optional)
                :param prev_frame: Previous Keyframe, Frame number of keyframe immediately before the current frame (in [-1048574, 1048574], optional)
                :param next_frame: Next Keyframe, Frame number of keyframe immediately after the current frame (in [-1048574, 1048574], optional)
                :param channels: Channels, Set of properties that are affected (optional)

        ALL
        All Properties -- All properties, including transforms, bendy bone shape, and custom properties.

        LOC
        Location -- Location only.

        ROT
        Rotation -- Rotation only.

        SIZE
        Scale -- Scale only.

        BBONE
        Bendy Bone -- Bendy Bone shape properties.

        CUSTOM
        Custom Properties -- Custom properties.
                :param axis_lock: Axis Lock, Transform axis to restrict effects to (optional)

        FREE
        Free -- All axes are affected.

        X
        X -- Only X-axis transforms are affected.

        Y
        Y -- Only Y-axis transforms are affected.

        Z
        Z -- Only Z-axis transforms are affected.
                :return: Result of the operator call.
        """

class _CLS_constraint_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[bpy.stub_internal.rna_enums.ConstraintTypeItems]
        | None = "CHILD_OF",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a constraint to the active bone

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_constraint_add_with_targets(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[bpy.stub_internal.rna_enums.ConstraintTypeItems]
        | None = "CHILD_OF",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a constraint to the active bone, with target (where applicable) set to the selected Objects/Bones

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_constraints_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear all constraints from the selected bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_constraints_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy constraints to other selected bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the current pose of the selected bones to the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_flip_names(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        do_strip_numbers: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Flips (and corrects) the axis suffixes of the names of selected bones

        :param execution_context:
        :param undo:
        :param do_strip_numbers: Strip Numbers, Try to remove right-most dot-number from flipped names.Warning: May result in incoherent naming in some cases(optional)
        :return: Result of the operator call.
        """

class _CLS_hide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        unselected: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Tag selected bones to not be visible in Pose Mode

        :param execution_context:
        :param undo:
        :param unselected: Unselected, (optional)
        :return: Result of the operator call.
        """

class _CLS_ik_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        with_targets: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add an IK Constraint to the active Bone. The target can be a selected bone or object

        :param execution_context:
        :param undo:
        :param with_targets: With Targets, Assign IK Constraint with targets derived from the select bones/objects (optional)
        :return: Result of the operator call.
        """

class _CLS_ik_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove all IK Constraints from selected bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_loc_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset locations of selected bones to their default values

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
        flipped: bool | None = False,
        selected_mask: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste the stored pose on to the current pose

        :param execution_context:
        :param undo:
        :param flipped: Flipped on X-Axis, Paste the stored pose flipped on to current pose (optional)
        :param selected_mask: On Selected Only, Only paste the stored pose on to selected bones in the current pose (optional)
        :return: Result of the operator call.
        """

class _CLS_paths_calculate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        display_type: typing.Literal[
            bpy.stub_internal.rna_enums.MotionpathDisplayTypeItems
        ]
        | None = "RANGE",
        range: typing.Literal[bpy.stub_internal.rna_enums.MotionpathRangeItems]
        | None = "SCENE",
        bake_location: typing.Literal[
            bpy.stub_internal.rna_enums.MotionpathBakeLocationItems
        ]
        | None = "HEADS",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Calculate paths for the selected bones

        :param execution_context:
        :param undo:
        :param display_type: Display Type, (optional)
        :param range: Computation Range, (optional)
        :param bake_location: Bake Location, Which point on the bones is used when calculating paths (optional)
        :return: Result of the operator call.
        """

class _CLS_paths_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        only_selected: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param only_selected: Only Selected, Only clear motion paths of selected bones (optional)
        :return: Result of the operator call.
        """

class _CLS_paths_range_update(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Update frame range for motion paths from the Scenes current frame range

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_paths_update(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Recalculate paths for bones that already have them

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_propagate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        mode: typing.Literal[
            "NEXT_KEY",
            "LAST_KEY",
            "BEFORE_FRAME",
            "BEFORE_END",
            "SELECTED_KEYS",
            "SELECTED_MARKERS",
        ]
        | None = "NEXT_KEY",
        end_frame: float | None = 250.0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy selected aspects of the current pose to subsequent poses already keyframed

                :param execution_context:
                :param undo:
                :param mode: Terminate Mode, Method used to determine when to stop propagating pose to keyframes (optional)

        NEXT_KEY
        To Next Keyframe -- Propagate pose to first keyframe following the current frame only.

        LAST_KEY
        To Last Keyframe -- Propagate pose to the last keyframe only (i.e. making action cyclic).

        BEFORE_FRAME
        Before Frame -- Propagate pose to all keyframes between current frame and Frame property.

        BEFORE_END
        Before Last Keyframe -- Propagate pose to all keyframes from current frame until no more are found.

        SELECTED_KEYS
        On Selected Keyframes -- Propagate pose to all selected keyframes.

        SELECTED_MARKERS
        On Selected Markers -- Propagate pose to all keyframes occurring on frames with Scene Markers after the current frame.
                :param end_frame: End Frame, Frame to stop propagating frames to (for Before Frame mode) (in [1.17549e-38, inf], optional)
                :return: Result of the operator call.
        """

class _CLS_push(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        factor: float | None = 0.5,
        prev_frame: int | None = 0,
        next_frame: int | None = 0,
        channels: typing.Literal["ALL", "LOC", "ROT", "SIZE", "BBONE", "CUSTOM"]
        | None = "ALL",
        axis_lock: typing.Literal["FREE", "X", "Y", "Z"] | None = "FREE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Exaggerate the current pose in regards to the breakdown pose

                :param execution_context:
                :param undo:
                :param factor: Factor, Weighting factor for which keyframe is favored more (in [0, 1], optional)
                :param prev_frame: Previous Keyframe, Frame number of keyframe immediately before the current frame (in [-1048574, 1048574], optional)
                :param next_frame: Next Keyframe, Frame number of keyframe immediately after the current frame (in [-1048574, 1048574], optional)
                :param channels: Channels, Set of properties that are affected (optional)

        ALL
        All Properties -- All properties, including transforms, bendy bone shape, and custom properties.

        LOC
        Location -- Location only.

        ROT
        Rotation -- Rotation only.

        SIZE
        Scale -- Scale only.

        BBONE
        Bendy Bone -- Bendy Bone shape properties.

        CUSTOM
        Custom Properties -- Custom properties.
                :param axis_lock: Axis Lock, Transform axis to restrict effects to (optional)

        FREE
        Free -- All axes are affected.

        X
        X -- Only X-axis transforms are affected.

        Y
        Y -- Only Y-axis transforms are affected.

        Z
        Z -- Only Z-axis transforms are affected.
                :return: Result of the operator call.
        """

class _CLS_quaternions_flip(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Flip quaternion values to achieve desired rotations, while maintaining the same orientations

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_relax(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        factor: float | None = 0.5,
        prev_frame: int | None = 0,
        next_frame: int | None = 0,
        channels: typing.Literal["ALL", "LOC", "ROT", "SIZE", "BBONE", "CUSTOM"]
        | None = "ALL",
        axis_lock: typing.Literal["FREE", "X", "Y", "Z"] | None = "FREE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Make the current pose more similar to its breakdown pose

                :param execution_context:
                :param undo:
                :param factor: Factor, Weighting factor for which keyframe is favored more (in [0, 1], optional)
                :param prev_frame: Previous Keyframe, Frame number of keyframe immediately before the current frame (in [-1048574, 1048574], optional)
                :param next_frame: Next Keyframe, Frame number of keyframe immediately after the current frame (in [-1048574, 1048574], optional)
                :param channels: Channels, Set of properties that are affected (optional)

        ALL
        All Properties -- All properties, including transforms, bendy bone shape, and custom properties.

        LOC
        Location -- Location only.

        ROT
        Rotation -- Rotation only.

        SIZE
        Scale -- Scale only.

        BBONE
        Bendy Bone -- Bendy Bone shape properties.

        CUSTOM
        Custom Properties -- Custom properties.
                :param axis_lock: Axis Lock, Transform axis to restrict effects to (optional)

        FREE
        Free -- All axes are affected.

        X
        X -- Only X-axis transforms are affected.

        Y
        Y -- Only Y-axis transforms are affected.

        Z
        Z -- Only Z-axis transforms are affected.
                :return: Result of the operator call.
        """

class _CLS_reveal(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        select: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reveal all bones hidden in Pose Mode

        :param execution_context:
        :param undo:
        :param select: Select, (optional)
        :return: Result of the operator call.
        """

class _CLS_rot_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset rotations of selected bones to their default values

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_rotation_mode_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[bpy.stub_internal.rna_enums.ObjectRotationModeItems]
        | None = "QUATERNION",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the rotation representation used by selected bones

        :param execution_context:
        :param undo:
        :param type: Rotation Mode, (optional)
        :return: Result of the operator call.
        """

class _CLS_scale_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset scaling of selected bones to their default values

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
        """Toggle selection status of all bones

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

class _CLS_select_constraint_target(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select bones used as targets for the currently selected bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select_grouped(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        extend: bool | None = False,
        type: typing.Literal[
            "COLLECTION",
            "COLOR",
            "KEYINGSET",
            "CHILDREN",
            "CHILDREN_IMMEDIATE",
            "PARENT",
            "SIBLINGS",
        ]
        | None = "COLLECTION",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select all visible bones grouped by similar properties

                :param execution_context:
                :param undo:
                :param extend: Extend, Extend selection instead of deselecting everything first (optional)
                :param type: Type, (optional)

        COLLECTION
        Collection -- Same collections as the active bone.

        COLOR
        Color -- Same color as the active bone.

        KEYINGSET
        Keying Set -- All bones affected by active Keying Set.

        CHILDREN
        Children -- Select all children of currently selected bones.

        CHILDREN_IMMEDIATE
        Immediate Children -- Select direct children of currently selected bones.

        PARENT
        Parents -- Select the parents of currently selected bones.

        SIBLINGS
        Siblings -- Select all bones that have the same parent as currently selected bones.
                :return: Result of the operator call.
        """

class _CLS_select_hierarchy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["PARENT", "CHILD"] | None = "PARENT",
        extend: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select immediate parent/children of selected bones

        :param execution_context:
        :param undo:
        :param direction: Direction, (optional)
        :param extend: Extend, Extend the selection (optional)
        :return: Result of the operator call.
        """

class _CLS_select_linked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select all bones linked by connected parent/child relationships from the current selection

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
        extend: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select bones linked by connected parent/child relationships under the mouse cursor

        :param execution_context:
        :param undo:
        :param extend: Extend, Extend selection instead of deselecting everything first (optional)
        :return: Result of the operator call.
        """

class _CLS_select_mirror(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        only_active: bool | None = False,
        extend: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Mirror the bone selection

        :param execution_context:
        :param undo:
        :param only_active: Active Only, Only operate on the active bone (optional)
        :param extend: Extend, Extend the selection (optional)
        :return: Result of the operator call.
        """

class _CLS_select_parent(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select bones that are parents of the currently selected bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new empty Selection Set

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_add_and_assign(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new Selection Set with the currently selected bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_assign(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add selected bones to Selection Set

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the selected Selection Set(s) to the clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_delete_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove all Selection Sets from this Armature

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_deselect(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove Selection Set bones from current selection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the active Selection Set up/down the list of sets

        :param execution_context:
        :param undo:
        :param direction: Move Direction, Direction to move the active Selection Set: UP (default) or DOWN (optional)
        :return: Result of the operator call.
        """

class _CLS_selection_set_paste(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new Selection Set(s) from the clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove a Selection Set from this Armature

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_remove_bones(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove the selected bones from all Selection Sets

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_selection_set_select(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        selection_set_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select the bones from this Selection Set

        :param execution_context:
        :param undo:
        :param selection_set_index: Selection Set Index, Which Selection Set to select; -1 uses the active Selection Set (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_selection_set_unassign(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove selected bones from Selection Set

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_transforms_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset location, rotation, and scaling of selected bones to their default values

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_user_transforms_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        only_selected: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset pose bone transforms to keyframed state

        :param execution_context:
        :param undo:
        :param only_selected: Only Selected, Only visible/selected bones (optional)
        :return: Result of the operator call.
        """

class _CLS_visual_transform_apply(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Apply final constrained position of pose bones to their transform

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

armature_apply: _CLS_armature_apply

autoside_names: _CLS_autoside_names

blend_to_neighbor: _CLS_blend_to_neighbor

blend_with_rest: _CLS_blend_with_rest

breakdown: _CLS_breakdown

constraint_add: _CLS_constraint_add

constraint_add_with_targets: _CLS_constraint_add_with_targets

constraints_clear: _CLS_constraints_clear

constraints_copy: _CLS_constraints_copy

copy: _CLS_copy

flip_names: _CLS_flip_names

hide: _CLS_hide

ik_add: _CLS_ik_add

ik_clear: _CLS_ik_clear

loc_clear: _CLS_loc_clear

paste: _CLS_paste

paths_calculate: _CLS_paths_calculate

paths_clear: _CLS_paths_clear

paths_range_update: _CLS_paths_range_update

paths_update: _CLS_paths_update

propagate: _CLS_propagate

push: _CLS_push

quaternions_flip: _CLS_quaternions_flip

relax: _CLS_relax

reveal: _CLS_reveal

rot_clear: _CLS_rot_clear

rotation_mode_set: _CLS_rotation_mode_set

scale_clear: _CLS_scale_clear

select_all: _CLS_select_all

select_constraint_target: _CLS_select_constraint_target

select_grouped: _CLS_select_grouped

select_hierarchy: _CLS_select_hierarchy

select_linked: _CLS_select_linked

select_linked_pick: _CLS_select_linked_pick

select_mirror: _CLS_select_mirror

select_parent: _CLS_select_parent

selection_set_add: _CLS_selection_set_add

selection_set_add_and_assign: _CLS_selection_set_add_and_assign

selection_set_assign: _CLS_selection_set_assign

selection_set_copy: _CLS_selection_set_copy

selection_set_delete_all: _CLS_selection_set_delete_all

selection_set_deselect: _CLS_selection_set_deselect

selection_set_move: _CLS_selection_set_move

selection_set_paste: _CLS_selection_set_paste

selection_set_remove: _CLS_selection_set_remove

selection_set_remove_bones: _CLS_selection_set_remove_bones

selection_set_select: _CLS_selection_set_select

selection_set_unassign: _CLS_selection_set_unassign

transforms_clear: _CLS_transforms_clear

user_transforms_clear: _CLS_user_transforms_clear

visual_transform_apply: _CLS_visual_transform_apply
