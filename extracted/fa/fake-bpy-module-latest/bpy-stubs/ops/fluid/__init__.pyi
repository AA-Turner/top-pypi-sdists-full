import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_bake_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake Entire Fluid Simulation

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_bake_data(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake Fluid Data

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_bake_guides(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake Fluid Guiding

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_bake_mesh(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake Fluid Mesh

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_bake_noise(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake Fluid Noise

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_bake_particles(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Bake Fluid Particles

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Free Entire Fluid Simulation

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_data(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Free Fluid Data

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_guides(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Free Fluid Guiding

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_mesh(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Free Fluid Mesh

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_noise(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Free Fluid Noise

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_free_particles(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Free Fluid Particles

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_pause_bake(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Pause Bake

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_preset_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        name: str = "",
        remove_name: bool | None = False,
        remove_active: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add or remove a Fluid Preset

        :param execution_context:
        :param undo:
        :param name: Name, Name of the preset, used to make the path name (optional, never None)
        :param remove_name: remove_name, (optional)
        :param remove_active: remove_active, (optional)
        :return: Result of the operator call.
        """

bake_all: _CLS_bake_all

bake_data: _CLS_bake_data

bake_guides: _CLS_bake_guides

bake_mesh: _CLS_bake_mesh

bake_noise: _CLS_bake_noise

bake_particles: _CLS_bake_particles

free_all: _CLS_free_all

free_data: _CLS_free_data

free_guides: _CLS_free_guides

free_mesh: _CLS_free_mesh

free_noise: _CLS_free_noise

free_particles: _CLS_free_particles

pause_bake: _CLS_pause_bake

preset_add: _CLS_preset_add
