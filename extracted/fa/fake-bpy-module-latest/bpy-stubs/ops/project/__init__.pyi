import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class add_variable(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        variable_type: typing.Literal["STRING", "FILEPATH", "INTEGER", "FLOAT"]
        | None = "STRING",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new variable to the current project

        :param execution_context:
        :param undo:
        :param variable_type: variable_type, (optional)
        :return: Result of the operator call.
        """

class asset_library_add(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        directory: str = "",
        filter_folder: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Register a directory to be used by the Asset Browser and other places showing assets,
        as source of assets within the current project.

                :param execution_context:
                :param undo:
                :param directory: Asset Library Directory, (optional, never None)
                :param filter_folder: Filter folders, (optional)
                :return: Result of the operator call.
        """

class asset_library_remove(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        index: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Deregister an asset library so that its directory will no longer show up in
        Asset Browsers and other places showing assets.

                :param execution_context:
                :param undo:
                :param index: Index, (in [-inf, inf], optional)
                :return: Result of the operator call.
        """

class move_variable(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN"] | None = "UP",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Move the active variable up or down in the list of variables

        :param execution_context:
        :param undo:
        :param direction: direction, (optional)
        :return: Result of the operator call.
        """

class new_project(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        directory: str = "",
        filter_folder: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create a new project

        :param execution_context:
        :param undo:
        :param directory: Project Root, (optional, never None)
        :param filter_folder: Filter folders, (optional)
        :return: Result of the operator call.
        """

class open_blend_in_project(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        filepath: str = "",
        filter_folder: bool | None = True,
        filter_blender: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Opens a blend file, but only if its inside of a project.

        :param execution_context:
        :param undo:
        :param filepath: Blend file path, (optional, never None)
        :param filter_folder: Filter folders, (optional)
        :param filter_blender: Filter blend files, (optional)
        :return: Result of the operator call.
        """

class remove_variable(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove the active variable from the current project

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class save_project(bpy.ops._BPyOpsSubModOp):
    def __new__(
        cls,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Save the current project to disk

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """
