import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_color_add(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new color to active palette

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_color_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove active color from palette

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_color_move(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["UP", "DOWN"] | None = "UP",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the active Color up/down in the list

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

class _CLS_extract_from_image(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        threshold: int | None = 1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Extract all colors used in Image and create a Palette

        :param execution_context:
        :param undo:
        :param threshold: Threshold, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_join(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        palette: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Join Palette Swatches

        :param execution_context:
        :param undo:
        :param palette: Palette, Name of the Palette (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new palette

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_sort(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["HSV", "SVH", "VHS", "LUMINANCE"] | None = "HSV",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Sort Palette Colors

        :param execution_context:
        :param undo:
        :param type: Type, (optional)
        :return: Result of the operator call.
        """

color_add: _CLS_color_add

color_delete: _CLS_color_delete

color_move: _CLS_color_move

extract_from_image: _CLS_extract_from_image

join: _CLS_join

new: _CLS_new

sort: _CLS_sort
