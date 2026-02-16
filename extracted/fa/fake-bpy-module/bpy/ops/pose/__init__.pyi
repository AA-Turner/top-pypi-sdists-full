import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def armature_apply(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    selected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Apply the current pose as the new rest pose

    :param selected: Selected Only, Only apply the selected bones (with propagation to children) (optional)
    :return: Result of the operator call.
    """

def autoside_names(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    axis: typing.Literal["XAXIS", "YAXIS", "ZAXIS"] | None = "XAXIS",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Automatically renames the selected bones according to which side of the target axis they fall on

        :param axis: Axis, Axis to tag names with (optional)

    XAXIS
    X-Axis -- Left/Right.

    YAXIS
    Y-Axis -- Front/Back.

    ZAXIS
    Z-Axis -- Top/Bottom.
        :return: Result of the operator call.
    """

def blend_to_neighbor(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Blend from current position to previous or next keyframe

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

def blend_with_rest(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make the current pose more similar to, or further away from, the rest pose

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

def breakdown(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a suitable breakdown pose on the current frame

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

def constraint_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: Literal[bpy.stub_internal.rna_enums.ConstraintTypeItems] | None = "CHILD_OF",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a constraint to the active bone

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def constraint_add_with_targets(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: Literal[bpy.stub_internal.rna_enums.ConstraintTypeItems] | None = "CHILD_OF",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a constraint to the active bone, with target (where applicable) set to the selected Objects/Bones

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def constraints_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear all constraints from the selected bones

    :return: Result of the operator call.
    """

def constraints_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy constraints to other selected bones

    :return: Result of the operator call.
    """

def copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the current pose of the selected bones to the internal clipboard

    :return: Result of the operator call.
    """

def flip_names(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    do_strip_numbers: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Flips (and corrects) the axis suffixes of the names of selected bones

    :param do_strip_numbers: Strip Numbers, Try to remove right-most dot-number from flipped names.Warning: May result in incoherent naming in some cases(optional)
    :return: Result of the operator call.
    """

def hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Tag selected bones to not be visible in Pose Mode

    :param unselected: Unselected, (optional)
    :return: Result of the operator call.
    """

def ik_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    with_targets: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add an IK Constraint to the active Bone. The target can be a selected bone or object

    :param with_targets: With Targets, Assign IK Constraint with targets derived from the select bones/objects (optional)
    :return: Result of the operator call.
    """

def ik_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all IK Constraints from selected bones

    :return: Result of the operator call.
    """

def loc_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset locations of selected bones to their default values

    :return: Result of the operator call.
    """

def paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    flipped: bool | None = False,
    selected_mask: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste the stored pose on to the current pose

    :param flipped: Flipped on X-Axis, Paste the stored pose flipped on to current pose (optional)
    :param selected_mask: On Selected Only, Only paste the stored pose on to selected bones in the current pose (optional)
    :return: Result of the operator call.
    """

def paths_calculate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    display_type: Literal[bpy.stub_internal.rna_enums.MotionpathDisplayTypeItems]
    | None = "RANGE",
    range: Literal[bpy.stub_internal.rna_enums.MotionpathRangeItems] | None = "SCENE",
    bake_location: Literal[bpy.stub_internal.rna_enums.MotionpathBakeLocationItems]
    | None = "HEADS",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Calculate paths for the selected bones

    :param display_type: Display Type, (optional)
    :param range: Computation Range, (optional)
    :param bake_location: Bake Location, Which point on the bones is used when calculating paths (optional)
    :return: Result of the operator call.
    """

def paths_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_selected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param only_selected: Only Selected, Only clear motion paths of selected bones (optional)
    :return: Result of the operator call.
    """

def paths_range_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update frame range for motion paths from the Scenes current frame range

    :return: Result of the operator call.
    """

def paths_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Recalculate paths for bones that already have them

    :return: Result of the operator call.
    """

def propagate(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy selected aspects of the current pose to subsequent poses already keyframed

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

def push(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Exaggerate the current pose in regards to the breakdown pose

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

def quaternions_flip(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Flip quaternion values to achieve desired rotations, while maintaining the same orientations

    :return: Result of the operator call.
    """

def relax(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make the current pose more similar to its breakdown pose

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

def reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reveal all bones hidden in Pose Mode

    :param select: Select, (optional)
    :return: Result of the operator call.
    """

def rot_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset rotations of selected bones to their default values

    :return: Result of the operator call.
    """

def rotation_mode_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: Literal[bpy.stub_internal.rna_enums.ObjectRotationModeItems]
    | None = "QUATERNION",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the rotation representation used by selected bones

    :param type: Rotation Mode, (optional)
    :return: Result of the operator call.
    """

def scale_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset scaling of selected bones to their default values

    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle selection status of all bones

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

def select_constraint_target(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select bones used as targets for the currently selected bones

    :return: Result of the operator call.
    """

def select_grouped(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all visible bones grouped by similar properties

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

def select_hierarchy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["PARENT", "CHILD"] | None = "PARENT",
    extend: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select immediate parent/children of selected bones

    :param direction: Direction, (optional)
    :param extend: Extend, Extend the selection (optional)
    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all bones linked by connected parent/child relationships from the current selection

    :return: Result of the operator call.
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select bones linked by connected parent/child relationships under the mouse cursor

    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :return: Result of the operator call.
    """

def select_mirror(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_active: bool | None = False,
    extend: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mirror the bone selection

    :param only_active: Active Only, Only operate on the active bone (optional)
    :param extend: Extend, Extend the selection (optional)
    :return: Result of the operator call.
    """

def select_parent(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select bones that are parents of the currently selected bones

    :return: Result of the operator call.
    """

def selection_set_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new empty Selection Set

    :return: Result of the operator call.
    """

def selection_set_add_and_assign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new Selection Set with the currently selected bones

    :return: Result of the operator call.
    """

def selection_set_assign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add selected bones to Selection Set

    :return: Result of the operator call.
    """

def selection_set_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected Selection Set(s) to the clipboard

    :return: Result of the operator call.
    """

def selection_set_delete_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all Selection Sets from this Armature

    :return: Result of the operator call.
    """

def selection_set_deselect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove Selection Set bones from current selection

    :return: Result of the operator call.
    """

def selection_set_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the active Selection Set up/down the list of sets

    :param direction: Move Direction, Direction to move the active Selection Set: UP (default) or DOWN (optional)
    :return: Result of the operator call.
    """

def selection_set_paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new Selection Set(s) from the clipboard

    :return: Result of the operator call.
    """

def selection_set_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove a Selection Set from this Armature

    :return: Result of the operator call.
    """

def selection_set_remove_bones(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the selected bones from all Selection Sets

    :return: Result of the operator call.
    """

def selection_set_select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    selection_set_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select the bones from this Selection Set

    :param selection_set_index: Selection Set Index, Which Selection Set to select; -1 uses the active Selection Set (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def selection_set_unassign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected bones from Selection Set

    :return: Result of the operator call.
    """

def transforms_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset location, rotation, and scaling of selected bones to their default values

    :return: Result of the operator call.
    """

def user_transforms_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_selected: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset pose bone transforms to keyframed state

    :param only_selected: Only Selected, Only visible/selected bones (optional)
    :return: Result of the operator call.
    """

def visual_transform_apply(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Apply final constrained position of pose bones to their transform

    :return: Result of the operator call.
    """
