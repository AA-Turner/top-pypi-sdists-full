import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def align(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Align selected bones to the active bone (or to their parent)

    :return: Result of the operator call.
    """

def assign_to_collection(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection_index: int | None = -1,
    new_collection_name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Assign all selected bones to a collection, or unassign them, depending on whether the active bone is already assigned or not

    :param collection_index: Collection Index, Index of the collection to assign selected bones to. When the operator should create a new bone collection, use new_collection_name to define the collection name, and set this parameter to the parent index of the new bone collection (in [-1, inf], optional)
    :param new_collection_name: Name, Name of a to-be-added bone collection. Only pass this if you want to create a new bone collection and assign the selected bones to it. To assign to an existing collection, do not include this parameter and use collection_index (optional, never None)
    :return: Result of the operator call.
    """

def autoside_names(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["XAXIS", "YAXIS", "ZAXIS"] | None = "XAXIS",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Automatically renames the selected bones according to which side of the target axis they fall on

        :param type: Axis, Axis to tag names with (optional)

    XAXIS
    X-Axis -- Left/Right.

    YAXIS
    Y-Axis -- Front/Back.

    ZAXIS
    Z-Axis -- Top/Bottom.
        :return: Result of the operator call.
    """

def bone_primitive_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "Bone",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new bone located at the 3D cursor

    :param name: Name, Name of the newly created bone (optional, never None)
    :return: Result of the operator call.
    """

def calculate_roll(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "POS_X",
        "POS_Z",
        "GLOBAL_POS_X",
        "GLOBAL_POS_Y",
        "GLOBAL_POS_Z",
        "NEG_X",
        "NEG_Z",
        "GLOBAL_NEG_X",
        "GLOBAL_NEG_Y",
        "GLOBAL_NEG_Z",
        "ACTIVE",
        "VIEW",
        "CURSOR",
    ]
    | None = "POS_X",
    axis_flip: bool | None = False,
    axis_only: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Automatically fix alignment of select bones axes

    :param type: Type, (optional)
    :param axis_flip: Flip Axis, Negate the alignment axis (optional)
    :param axis_only: Shortest Rotation, Ignore the axis direction, use the shortest rotation to align (optional)
    :return: Result of the operator call.
    """

def click_extrude(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new bone going from the last selected joint to the mouse position

    :return: Result of the operator call.
    """

def collection_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new bone collection

    :return: Result of the operator call.
    """

def collection_assign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add selected bones to the chosen bone collection

    :param name: Bone Collection, Name of the bone collection to assign this bone to; empty to assign to the active bone collection (optional, never None)
    :return: Result of the operator call.
    """

def collection_create_and_assign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new bone collection and assign all selected bones

    :param name: Bone Collection, Name of the bone collection to create (optional, never None)
    :return: Result of the operator call.
    """

def collection_deselect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect bones of active Bone Collection

    :return: Result of the operator call.
    """

def collection_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN"] | None = "UP",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change position of active Bone Collection in list of Bone collections

    :param direction: Direction, Direction to move the active Bone Collection towards (optional)
    :return: Result of the operator call.
    """

def collection_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the active bone collection

    :return: Result of the operator call.
    """

def collection_remove_unused(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all bone collections that have neither bones nor children. This is done recursively, so bone collections that only have unused children are also removed

    :return: Result of the operator call.
    """

def collection_select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select bones in active Bone Collection

    :return: Result of the operator call.
    """

def collection_show_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show all bone collections

    :return: Result of the operator call.
    """

def collection_unassign(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected bones from the active bone collection

    :param name: Bone Collection, Name of the bone collection to unassign this bone from; empty to unassign from the active bone collection (optional, never None)
    :return: Result of the operator call.
    """

def collection_unassign_named(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str | None = "",
    bone_name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unassign the named bone from this bone collection

    :param name: Bone Collection, Name of the bone collection to unassign this bone from; empty to unassign from the active bone collection (optional, never None)
    :param bone_name: Bone Name, Name of the bone to unassign from the collection; empty to use the active bone (optional, never None)
    :return: Result of the operator call.
    """

def collection_unsolo_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear the solo setting on all bone collections

    :return: Result of the operator call.
    """

def copy_bone_color_to_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    bone_type: typing.Literal["EDIT", "POSE"] | None = "EDIT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the bone color of the active bone to all selected bones

        :param bone_type: Type, (optional)

    EDIT
    Bone -- Copy Bone colors from the active bone to all selected bones.

    POSE
    Pose Bone -- Copy Pose Bone colors from the active pose bone to all selected pose bones.
        :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected bones from the armature

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def dissolve(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Dissolve selected bones from the armature

    :return: Result of the operator call.
    """

def duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    do_flip_names: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make copies of the selected bones within the same armature

    :param do_flip_names: Flip Names, Try to flip names of the bones, if possible, instead of adding a number extension (optional)
    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ARMATURE_OT_duplicate: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make copies of the selected bones within the same armature and move them

    :param ARMATURE_OT_duplicate: Duplicate Selected Bone(s), Make copies of the selected bones within the same armature (optional, `bpy.ops.armature.duplicate` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def extrude(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    forked: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create new bones from the selected joints

    :param forked: Forked, (optional)
    :return: Result of the operator call.
    """

def extrude_forked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ARMATURE_OT_extrude: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create new bones from the selected joints and move them

    :param ARMATURE_OT_extrude: Extrude, Create new bones from the selected joints (optional, `bpy.ops.armature.extrude` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def extrude_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ARMATURE_OT_extrude: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create new bones from the selected joints and move them

    :param ARMATURE_OT_extrude: Extrude, Create new bones from the selected joints (optional, `bpy.ops.armature.extrude` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def fill(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add bone between selected joint(s) and/or 3D cursor

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
    """Tag selected bones to not be visible in Edit Mode

    :param unselected: Unselected, Hide unselected rather than selected (optional)
    :return: Result of the operator call.
    """

def move_to_collection(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    collection_index: int | None = -1,
    new_collection_name: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move bones to a collection

    :param collection_index: Collection Index, Index of the collection to move selected bones to. When the operator should create a new bone collection, do not include this parameter and pass new_collection_name (in [-1, inf], optional)
    :param new_collection_name: Name, Name of a to-be-added bone collection. Only pass this if you want to create a new bone collection and move the selected bones to it. To move to an existing collection, do not include this parameter and use collection_index (optional, never None)
    :return: Result of the operator call.
    """

def parent_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["CLEAR", "DISCONNECT"] | None = "CLEAR",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the parent-child relationship between selected bones and their parents

    :param type: Clear Type, What way to clear parenting (optional)
    :return: Result of the operator call.
    """

def parent_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["CONNECTED", "OFFSET"] | None = "CONNECTED",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the active bone as the parent of the selected bones

    :param type: Parent Type, Type of parenting (optional)
    :return: Result of the operator call.
    """

def reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reveal all bones hidden in Edit Mode

    :param select: Select, (optional)
    :return: Result of the operator call.
    """

def roll_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    roll: float | None = 0.0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear roll for selected bones

    :param roll: Roll, (in [-6.28319, 6.28319], optional)
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

def select_less(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect those bones at the boundary of each selection region

    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all_forks: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all bones linked by parent/child connections to the current selection

    :param all_forks: All Forks, Follow forks in the parents chain (optional)
    :return: Result of the operator call.
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect: bool | None = False,
    all_forks: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select bones linked by parent/child connections under the mouse cursor

    :param deselect: Deselect, (optional)
    :param all_forks: All Forks, Follow forks in the parents chain (optional)
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

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select those bones connected to the initial selection

    :return: Result of the operator call.
    """

def select_similar(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "CHILDREN",
        "CHILDREN_IMMEDIATE",
        "SIBLINGS",
        "LENGTH",
        "DIRECTION",
        "PREFIX",
        "SUFFIX",
        "BONE_COLLECTION",
        "COLOR",
        "SHAPE",
    ]
    | None = "LENGTH",
    threshold: float | None = 0.1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select similar bones by property types

    :param type: Type, (optional)
    :param threshold: Threshold, (in [0, 1], optional)
    :return: Result of the operator call.
    """

def separate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Isolate selected bones into a separate armature

    :return: Result of the operator call.
    """

def shortest_path_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select shortest path between two bones

    :return: Result of the operator call.
    """

def split(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Split off selected bones from connected unselected bones

    :return: Result of the operator call.
    """

def subdivide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    number_cuts: int | None = 1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Break selected bones into chains of smaller bones

    :param number_cuts: Number of Cuts, (in [1, 1000], optional)
    :return: Result of the operator call.
    """

def switch_direction(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the direction that a chain of bones points in (head and tail swap)

    :return: Result of the operator call.
    """

def symmetrize(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["NEGATIVE_X", "POSITIVE_X"] | None = "NEGATIVE_X",
    copy_bone_colors: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enforce symmetry, make copies of the selection or use existing

    :param direction: Direction, Which sides to copy from and to (when both are selected) (optional)
    :param copy_bone_colors: Bone Colors, Copy colors to existing bones (optional)
    :return: Result of the operator call.
    """
