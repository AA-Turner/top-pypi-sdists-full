import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_rule_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[bpy.stub_internal.rna_enums.BoidruleTypeItems]
        | None = "GOAL",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a boid rule to the current boid state

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_rule_del(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete current boid rule

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_rule_move_down(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move boid rule down in the list

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_rule_move_up(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move boid rule up in the list

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_state_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a boid state to the particle system

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_state_del(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete current boid state

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_state_move_down(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move boid state down in the list

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_state_move_up(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move boid state up in the list

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

rule_add: _CLS_rule_add

rule_del: _CLS_rule_del

rule_move_down: _CLS_rule_move_down

rule_move_up: _CLS_rule_move_up

state_add: _CLS_state_add

state_del: _CLS_state_del

state_move_down: _CLS_state_move_down

state_move_up: _CLS_state_move_up
