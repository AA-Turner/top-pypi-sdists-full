import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the material settings and nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new material

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
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste the material settings and nodes

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

copy: _CLS_copy

new: _CLS_new

paste: _CLS_paste
