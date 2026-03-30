import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new cache

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_bake(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        bake: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake physics

        :param execution_context:
        :param undo:
        :param bake: Bake, (optional)
        :return: Result of the operator call.
        """

class _CLS_bake_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        bake: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake all physics simulations in the current scene

        :param execution_context:
        :param undo:
        :param bake: Bake, (optional)
        :return: Result of the operator call.
        """

class _CLS_bake_from_cache(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake from cache

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_bake(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete physics bake

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_bake_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete all baked caches of all objects in the current scene

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_remove(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete current cache

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

add: _CLS_add

bake: _CLS_bake

bake_all: _CLS_bake_all

bake_from_cache: _CLS_bake_from_cache

free_bake: _CLS_free_bake

free_bake_all: _CLS_free_bake_all

remove: _CLS_remove
