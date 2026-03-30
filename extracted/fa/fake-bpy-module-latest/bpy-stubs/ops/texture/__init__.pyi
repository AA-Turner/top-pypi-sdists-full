import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new texture

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_slot_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the material texture settings and nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_slot_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["UP", "DOWN"] | None = "UP",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move texture slots up and down

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_slot_paste(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste the texture settings and nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

new: _CLS_new

slot_copy: _CLS_slot_copy

slot_move: _CLS_slot_move

slot_paste: _CLS_slot_paste
