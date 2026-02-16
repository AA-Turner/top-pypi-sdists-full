import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def add_target(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a target to the constraint

    :return: Result of the operator call.
    """

def apply(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    report: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Apply constraint and remove from the stack

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :param report: Report, Create a notification after the operation (optional)
        :return: Result of the operator call.
    """

def childof_clear_inverse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear inverse correction for Child Of constraint

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def childof_set_inverse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set inverse correction for Child Of constraint

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    report: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate constraint at the same position in the stack

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :param report: Report, Create a notification after the operation (optional)
        :return: Result of the operator call.
    """

def copy_to_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy constraint to other selected objects/bones

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    report: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove constraint from constraint stack

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :param report: Report, Create a notification after the operation (optional)
        :return: Result of the operator call.
    """

def disable_keep_transform(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the influence of this constraint to zero while trying to maintain the objects transformation. Other active constraints can still influence the final transformation

    :return: Result of the operator call.
    """

def followpath_path_animate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    frame_start: int | None = 1,
    length: int | None = 100,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add default animation for path used by constraint if it isnt animated already

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :param frame_start: Start Frame, First frame of path animation (in [-1048574, 1048574], optional)
        :param length: Length, Number of frames that path animation should take (in [0, 1048574], optional)
        :return: Result of the operator call.
    """

def limitdistance_reset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset limiting distance for Limit Distance Constraint

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def move_down(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move constraint down in constraint stack

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def move_to_index(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the constraints position in the list so it evaluates after the set number of others

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :param index: Index, The index to move the constraint to (in [0, inf], optional)
        :return: Result of the operator call.
    """

def move_up(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move constraint up in constraint stack

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def normalize_target_weights(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Normalize weights of all target bones

    :return: Result of the operator call.
    """

def objectsolver_clear_inverse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear inverse correction for Object Solver constraint

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def objectsolver_set_inverse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set inverse correction for Object Solver constraint

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """

def remove_target(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    index: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the target from the constraint

    :param index: index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def stretchto_reset(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    constraint: str | None = "",
    owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset original length of bone for Stretch To Constraint

        :param constraint: Constraint, Name of the constraint to edit (optional, never None)
        :param owner: Owner, The owner of this constraint (optional)

    OBJECT
    Object -- Edit a constraint on the active object.

    BONE
    Bone -- Edit a constraint on the active bone.
        :return: Result of the operator call.
    """
