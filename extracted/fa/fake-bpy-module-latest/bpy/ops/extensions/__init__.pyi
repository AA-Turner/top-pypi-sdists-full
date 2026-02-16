import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def package_disable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Turn off this extension

    :return: Result of the operator call.
    """

def package_install(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    repo_directory: str | None = "",
    repo_index: int | None = -1,
    pkg_id: str | None = "",
    enable_on_install: bool | None = True,
    url: str | None = "",
    do_legacy_replace: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Download and install the extension

    :param repo_directory: Repo Directory, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :param pkg_id: Package ID, (optional, never None)
    :param enable_on_install: Enable on Install, Enable after installing (optional)
    :param url: URL, (optional, never None)
    :param do_legacy_replace: Do Legacy Replace, (optional)
    :return: Result of the operator call.
    """

def package_install_files(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filter_glob: str | None = "*.zip;*.py",
    directory: str | None = "",
    files=None,
    filepath: str | None = "",
    repo: str | None = "",
    enable_on_install: bool | None = True,
    target: str | None = "",
    overwrite: bool | None = True,
    url: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Install extensions from files into a locally managed repository

    :param filter_glob: filter_glob, (optional, never None)
    :param directory: Directory, (optional, never None)
    :param files: files, (optional)
    :param filepath: filepath, (optional, never None)
    :param repo: User Repository, The user repository to install extensions into (optional)
    :param enable_on_install: Enable on Install, Enable after installing (optional)
    :param target: Legacy Target Path, Path to install legacy add-on packages to (optional)
    :param overwrite: Legacy Overwrite, Remove existing add-ons with the same ID (optional)
    :param url: URL, (optional, never None)
    :return: Result of the operator call.
    """

def package_install_marked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    enable_on_install: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param enable_on_install: Enable on Install, Enable after installing (optional)
    :return: Result of the operator call.
    """

def package_mark_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_mark_clear_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def package_mark_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_mark_set_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def package_obsolete_marked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Zeroes package versions, useful for development - to test upgrading

    :return: Result of the operator call.
    """

def package_show_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_show_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_show_settings(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_theme_disable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset to the default theme if this theme is active

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_theme_enable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    pkg_id: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Turn on this theme

    :param pkg_id: Package ID, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def package_uninstall(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    repo_directory: str | None = "",
    repo_index: int | None = -1,
    pkg_id: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Disable and uninstall the extension

    :param repo_directory: Repo Directory, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :param pkg_id: Package ID, (optional, never None)
    :return: Result of the operator call.
    """

def package_uninstall_marked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def package_uninstall_system(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def package_upgrade_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_active_only: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Upgrade installed extensions to their latest version from remote repositories

    :param use_active_only: Active Only, Only upgrade the active repository (optional)
    :return: Result of the operator call.
    """

def repo_enable_from_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def repo_lock_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Lock repositories - to test locking

    :return: Result of the operator call.
    """

def repo_refresh_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_active_only: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Refresh extension & legacy add-ons, reloading modules & meta-data (similar to restarting)

    :param use_active_only: Active Only, Only refresh the active repository (optional)
    :return: Result of the operator call.
    """

def repo_sync(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    repo_directory: str | None = "",
    repo_index: int | None = -1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param repo_directory: Repo Directory, (optional, never None)
    :param repo_index: Repo Index, (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def repo_sync_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_active_only: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Refresh the list of extensions for all the remote repositories

    :param use_active_only: Active Only, Only sync the active repository (optional)
    :return: Result of the operator call.
    """

def repo_unlock(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the repository file-system lock

    :return: Result of the operator call.
    """

def repo_unlock_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unlock repositories - to test unlocking

    :return: Result of the operator call.
    """

def status_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def status_clear_errors(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :return: Result of the operator call.
    """

def userpref_allow_online(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Allow internet access. Blender may access configured online extension repositories. Installed third party add-ons may access the internet for their own functionality

    :return: Result of the operator call.
    """

def userpref_allow_online_popup(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Allow internet access. Blender may access configured online extension repositories. Installed third party add-ons may access the internet for their own functionality

    :return: Result of the operator call.
    """

def userpref_show_for_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Open extensions preferences

    :return: Result of the operator call.
    """

def userpref_show_online(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show system preferences "Network" panel to allow online access

    :return: Result of the operator call.
    """

def userpref_tags_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    value: bool | None = False,
    data_path: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the value of all tags

    :param value: Value, Enable or disable all tags (optional)
    :param data_path: Data Path, (optional, never None)
    :return: Result of the operator call.
    """
