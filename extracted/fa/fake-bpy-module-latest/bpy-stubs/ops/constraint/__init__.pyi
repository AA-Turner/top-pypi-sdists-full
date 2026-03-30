import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_add_target(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a target to the constraint

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_apply(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
        report: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Apply constraint and remove from the stack

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :param report: Report, Create a notification after the operation (optional)
                :return: Result of the operator call.
        """

class _CLS_childof_clear_inverse(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear inverse correction for Child Of constraint

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_childof_set_inverse(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set inverse correction for Child Of constraint

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
        report: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Duplicate constraint at the same position in the stack

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :param report: Report, Create a notification after the operation (optional)
                :return: Result of the operator call.
        """

class _CLS_copy_to_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy constraint to other selected objects/bones

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
        report: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove constraint from constraint stack

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :param report: Report, Create a notification after the operation (optional)
                :return: Result of the operator call.
        """

class _CLS_disable_keep_transform(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the influence of this constraint to zero while trying to maintain the objects transformation. Other active constraints can still influence the final transformation

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_followpath_path_animate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
        frame_start: int | None = 1,
        length: int | None = 100,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add default animation for path used by constraint if it isnt animated already

                :param execution_context:
                :param undo:
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

class _CLS_limitdistance_reset(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset limiting distance for Limit Distance Constraint

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_move_down(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move constraint down in constraint stack

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_move_to_index(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
        index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Change the constraints position in the list so it evaluates after the set number of others

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :param index: Index, The index to move the constraint to (in [0, inf], optional)
                :return: Result of the operator call.
        """

class _CLS_move_up(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move constraint up in constraint stack

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_normalize_target_weights(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Normalize weights of all target bones

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_objectsolver_clear_inverse(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear inverse correction for Object Solver constraint

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_objectsolver_set_inverse(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set inverse correction for Object Solver constraint

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

class _CLS_remove_target(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove the target from the constraint

        :param execution_context:
        :param undo:
        :param index: index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_stretchto_reset(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        constraint: str = "",
        owner: typing.Literal["OBJECT", "BONE"] | None = "OBJECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset original length of bone for Stretch To Constraint

                :param execution_context:
                :param undo:
                :param constraint: Constraint, Name of the constraint to edit (optional, never None)
                :param owner: Owner, The owner of this constraint (optional)

        OBJECT
        Object -- Edit a constraint on the active object.

        BONE
        Bone -- Edit a constraint on the active bone.
                :return: Result of the operator call.
        """

add_target: _CLS_add_target

apply: _CLS_apply

childof_clear_inverse: _CLS_childof_clear_inverse

childof_set_inverse: _CLS_childof_set_inverse

copy: _CLS_copy

copy_to_selected: _CLS_copy_to_selected

delete: _CLS_delete

disable_keep_transform: _CLS_disable_keep_transform

followpath_path_animate: _CLS_followpath_path_animate

limitdistance_reset: _CLS_limitdistance_reset

move_down: _CLS_move_down

move_to_index: _CLS_move_to_index

move_up: _CLS_move_up

normalize_target_weights: _CLS_normalize_target_weights

objectsolver_clear_inverse: _CLS_objectsolver_clear_inverse

objectsolver_set_inverse: _CLS_objectsolver_set_inverse

remove_target: _CLS_remove_target

stretchto_reset: _CLS_stretchto_reset
