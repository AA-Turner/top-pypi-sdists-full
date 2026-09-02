import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import _bpy_types
import bl_ui.space_userpref
import bpy.types

class PROJECT_HT_header(_bpy_types.Header):
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_MT_add_variable(_bpy_types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_MT_editor_menus(_bpy_types.Menu):
    bl_idname: typing.Any
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_MT_save_load(_bpy_types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_MT_view(_bpy_types.Menu):
    bl_label: typing.Any
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_PT_main(_bpy_types.Panel, bl_ui.space_userpref.CenterAlignMixIn):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_centered(context, layout) function.
    """

    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    bl_translation_context: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw_centered(self, context, layout) -> None:
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_PT_main_unset(_bpy_types.Panel, bl_ui.space_userpref.CenterAlignMixIn):
    """Base class for panels to center align contents with some horizontal margin.
    Deriving classes need to implement a draw_centered(context, layout) function.
    """

    bl_category: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw_centered(self, context, layout) -> None:
        """

        :param context:
        :param layout:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_PT_navigation_bar(_bpy_types.Panel):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_PT_save_project(_bpy_types.Panel):
    bl_label: typing.Any
    bl_options: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_PT_variables(_bpy_types.Panel):
    bl_category: typing.Any
    bl_label: typing.Any
    bl_region_type: typing.Any
    bl_rna: typing.Any
    bl_space_type: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw(self, context) -> None:
        """

        :param context:
        """

class PROJECT_UL_variables(_bpy_types.UIList):
    bl_rna: typing.Any
    id_data: typing.Any

    def bl_rna_get_subclass(self) -> bpy.types.Struct:
        """

        :return: The RNA type or default when not found.
        """

    def bl_rna_get_subclass_py(self) -> typing.Any:
        """

        :return: The class or default when not found.
        """

    def draw_item(
        self, context, layout, data, item, icon, active_data, active_propname
    ) -> None:
        """

        :param context:
        :param layout:
        :param data:
        :param item:
        :param icon:
        :param active_data:
        :param active_propname:
        """
