import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_add_point(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        location: collections.abc.Sequence[int] | None = (0, 0),
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add New Paint Curve Point

        :param execution_context:
        :param undo:
        :param location: Location, Location of vertex in area space (array of 2 items, in [0, 32767], optional)
        :return: Result of the operator call.
        """

class _CLS_add_point_slide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        PAINTCURVE_OT_add_point: dict[str, typing.Any] | None = {},
        PAINTCURVE_OT_slide: dict[str, typing.Any] | None = {},
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add new curve point and slide it

        :param execution_context:
        :param undo:
        :param PAINTCURVE_OT_add_point: Add New Paint Curve Point, Add New Paint Curve Point (optional, `bpy.ops.paintcurve.add_point` keyword arguments)
        :param PAINTCURVE_OT_slide: Slide Paint Curve Point, Select and slide paint curve point (optional, `bpy.ops.paintcurve.slide` keyword arguments)
        :return: Result of the operator call.
        """

class _CLS_cursor(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Place cursor

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_delete_point(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove Paint Curve Point

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_draw(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Draw curve

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
        """Add new paint curve

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_select(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        location: collections.abc.Sequence[int] | None = (0, 0),
        toggle: bool | None = False,
        extend: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select a paint curve point

        :param execution_context:
        :param undo:
        :param location: Location, Location of vertex in area space (array of 2 items, in [0, 32767], optional)
        :param toggle: Toggle, (De)select all (optional)
        :param extend: Extend, Extend selection (optional)
        :return: Result of the operator call.
        """

class _CLS_slide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        align: bool | None = False,
        select: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select and slide paint curve point

        :param execution_context:
        :param undo:
        :param align: Align Handles, Aligns opposite point handle during transform (optional)
        :param select: Select, Attempt to select a point handle before transform (optional)
        :return: Result of the operator call.
        """

add_point: _CLS_add_point

add_point_slide: _CLS_add_point_slide

cursor: _CLS_cursor

delete_point: _CLS_delete_point

draw: _CLS_draw

new: _CLS_new

select: _CLS_select

slide: _CLS_slide
