import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import _bpy_types
import bpy.types

class AssetLibraryDefinition:
    """AssetLibraryDefinition(name: str, path: str, use_relative_path: bool, import_method: str, uuid: str | None = None)"""

    uuid: typing.Any

class PROJECT_OT_AddVariable(_bpy_types.Operator):
    """Add a new variable to the current project"""

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

    def execute(self, context) -> None:
        """

        :param context:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_AssetLibraryAdd(_bpy_types.Operator):
    """Register a directory to be used by the Asset Browser and other places showing assets,
    as source of assets within the current project.
    """

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
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

    def execute(self, context) -> None:
        """

        :param context:
        """

    def invoke(self, context, event) -> None:
        """

        :param context:
        :param event:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_AssetLibraryRemove(_bpy_types.Operator):
    """Deregister an asset library so that its directory will no longer show up in
    Asset Browsers and other places showing assets.
    """

    bl_idname: typing.Any
    bl_label: typing.Any
    bl_options: typing.Any
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

    def execute(self, context) -> None:
        """

        :param context:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_MoveVariable(_bpy_types.Operator):
    """Move the active variable up or down in the list of variables"""

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

    def execute(self, context) -> None:
        """

        :param context:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_NewProject(_bpy_types.Operator):
    """Create a new project"""

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

    def execute(self, context) -> None:
        """

        :param context:
        """

    def invoke(self, context, event) -> None:
        """

        :param context:
        :param event:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_OpenBlendInProject(_bpy_types.Operator):
    """Opens a blend file, but only if its inside of a project."""

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

    def execute(self, context) -> None:
        """

        :param context:
        """

    def invoke(self, context, event) -> None:
        """

        :param context:
        :param event:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_RemoveVariable(_bpy_types.Operator):
    """Remove the active variable from the current project"""

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

    def execute(self, context) -> None:
        """

        :param context:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class PROJECT_OT_SaveProject(_bpy_types.Operator):
    """Save the current project to disk"""

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

    def execute(self, context) -> None:
        """

        :param context:
        """

    @classmethod
    def poll(cls, context) -> None:
        """

        :param context:
        """

class ProjectConfig:
    """ProjectConfig(schema_version: int, name: str, variables: list[bl_operators.project.ProjectVariable] | None = None, asset_libraries: list[bl_operators.project.AssetLibraryDefinition] | None = None)"""

    asset_libraries: typing.Any
    variables: typing.Any

    @staticmethod
    def new_from_real(project) -> None:
        """Create a ProjectConfig object from an existing real project.

        :param project:
        """

    def populate_real(self, project) -> None:
        """Fills in an existing real projects data from this ProjectConfig object.

        :param project:
        """

class ProjectLoadException:
    """Common base class for all non-exit exceptions."""

    args: typing.Any

class ProjectSaveException:
    """Common base class for all non-exit exceptions."""

    args: typing.Any

class ProjectVariable:
    """ProjectVariable(name: str, type: bl_operators.project.VariableType, value: int | str | float, subtype: bl_operators.project.VariableSubtype | None = None, description: str = )"""

    description: typing.Any
    subtype: typing.Any

    def add_as_real(self, variables) -> None:
        """Adds this as a real variable to the given real project variables list.

        :param variables:
        """

    @staticmethod
    def new_from_real(project_variable) -> None:
        """Create a ProjectVariable config object from an existing real project variable.

        :param project_variable:
        """

class VariableSubtype:
    """Create a collection of name/value pairs.Example enumeration:Access them by:Enumerations can be iterated over, and know how many members they have:Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.
    """

    FILEPATH: typing.Any
    NONE: typing.Any
    name: typing.Any
    value: typing.Any

class VariableType:
    """Create a collection of name/value pairs.Example enumeration:Access them by:Enumerations can be iterated over, and know how many members they have:Methods can be added to enumerations, and members can have their own
    attributes -- see the documentation for details.
    """

    FLOAT: typing.Any
    INTEGER: typing.Any
    STRING: typing.Any
    name: typing.Any
    value: typing.Any

def blend_file_is_in_valid_project(blend_file_path) -> None:
    """Return whether the blend file is inside a valid project or not.True if the blend file is inside a valid project, false if no project is
    found or if the project is invalid.An "invalid project" is one whose TOML config is non-existent or doesnt
    validate. See read_project_toml_config().

    """

def find_and_load_project_for_blend_path(context, blend_path, report=None) -> None:
    """Load the project the blend file is in, or clears the project if none is found.blend_path should be an absolute path.Throws a ProjectLoadException if a project is found but is invalid
    (missing config file, config validation error, etc.).Optionally takes an Operator.report for reporting errors to the user.

    """

def find_project_root_from_blend_file_path(blend_path) -> None:
    """Search for a project root in the parent directories of the given path.Returns the project root if found, or None otherwise."""

def log_project_load_error(blend_path) -> None: ...
def log_project_save_error() -> None: ...
def on_blend_load(blend_path) -> None: ...
def on_blend_save(blend_path) -> None: ...
def on_exit(is_user_exit) -> None: ...
def read_project_toml_config(root_path, report=None) -> None:
    """Read the project config for the given project root path.Throws a ProjectLoadException if no config is found, if the config is
    not readable due to file-system permissions, or if its not a valid
    project config (e.g. contains invalid TOML or doesnt match the schema).Optionally takes an Operator.report for reporting errors to the user.Returns the configuration (ProjectConfig).

    """

def register() -> None: ...
def save_project(project, report=None) -> None:
    """Save the passed project to disk.Throws a ProjectSaveException in any of the following cases:Optionally takes an Operator.report for reporting errors to the user."""

def structure_int_float_str(obj, cl) -> None: ...
def unregister() -> None: ...
