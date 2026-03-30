import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums
import bpy.types

class _CLS_package_disable(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Turn off this extension

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_package_install(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        repo_directory: str = "",
        repo_index: int | None = -1,
        pkg_id: str = "",
        enable_on_install: bool | None = True,
        url: str = "",
        do_legacy_replace: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Download and install the extension

        :param execution_context:
        :param undo:
        :param repo_directory: Repo Directory, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :param pkg_id: Package ID, (optional, never None)
        :param enable_on_install: Enable on Install, Enable after installing (optional)
        :param url: URL, (optional, never None)
        :param do_legacy_replace: Do Legacy Replace, (optional)
        :return: Result of the operator call.
        """

class _CLS_package_install_files(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        filter_glob: str = "*.zip;*.py",
        directory: str = "",
        files: bpy.types.bpy_prop_collection[bpy.types.OperatorFileListElement]
        | None = None,
        filepath: str = "",
        repo: str | None = "",
        enable_on_install: bool | None = True,
        target: str | None = "",
        overwrite: bool | None = True,
        url: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Install extensions from files into a locally managed repository

        :param execution_context:
        :param undo:
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

class _CLS_package_install_marked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        enable_on_install: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param enable_on_install: Enable on Install, Enable after installing (optional)
        :return: Result of the operator call.
        """

class _CLS_package_mark_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_mark_clear_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_package_mark_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_mark_set_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_package_obsolete_marked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Zeroes package versions, useful for development - to test upgrading

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_package_show_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_show_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_show_settings(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_theme_disable(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Reset to the default theme if this theme is active

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_theme_enable(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        pkg_id: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Turn on this theme

        :param execution_context:
        :param undo:
        :param pkg_id: Package ID, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_package_uninstall(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        repo_directory: str = "",
        repo_index: int | None = -1,
        pkg_id: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Disable and uninstall the extension

        :param execution_context:
        :param undo:
        :param repo_directory: Repo Directory, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :param pkg_id: Package ID, (optional, never None)
        :return: Result of the operator call.
        """

class _CLS_package_uninstall_marked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_package_uninstall_system(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_package_upgrade_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_active_only: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Upgrade installed extensions to their latest version from remote repositories

        :param execution_context:
        :param undo:
        :param use_active_only: Active Only, Only upgrade the active repository (optional)
        :return: Result of the operator call.
        """

class _CLS_repo_enable_from_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_repo_lock_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Lock repositories - to test locking

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_repo_refresh_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_active_only: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Refresh extension & legacy add-ons, reloading modules & meta-data (similar to restarting)

        :param execution_context:
        :param undo:
        :param use_active_only: Active Only, Only refresh the active repository (optional)
        :return: Result of the operator call.
        """

class _CLS_repo_sync(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        repo_directory: str = "",
        repo_index: int | None = -1,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param repo_directory: Repo Directory, (optional, never None)
        :param repo_index: Repo Index, (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_repo_sync_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_active_only: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Refresh the list of extensions for all the remote repositories

        :param execution_context:
        :param undo:
        :param use_active_only: Active Only, Only sync the active repository (optional)
        :return: Result of the operator call.
        """

class _CLS_repo_unlock(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove the repository file-system lock

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_repo_unlock_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Unlock repositories - to test unlocking

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_status_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_status_clear_errors(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_userpref_allow_online(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Allow internet access. Blender may access configured online extension repositories. Installed third party add-ons may access the internet for their own functionality

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_userpref_allow_online_popup(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Allow internet access. Blender may access configured online extension repositories. Installed third party add-ons may access the internet for their own functionality

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_userpref_show_for_update(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Open extensions preferences

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_userpref_show_online(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Show system preferences "Network" panel to allow online access

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_userpref_tags_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        value: bool | None = False,
        data_path: str = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set the value of all tags

        :param execution_context:
        :param undo:
        :param value: Value, Enable or disable all tags (optional)
        :param data_path: Data Path, (optional, never None)
        :return: Result of the operator call.
        """

package_disable: _CLS_package_disable

package_install: _CLS_package_install

package_install_files: _CLS_package_install_files

package_install_marked: _CLS_package_install_marked

package_mark_clear: _CLS_package_mark_clear

package_mark_clear_all: _CLS_package_mark_clear_all

package_mark_set: _CLS_package_mark_set

package_mark_set_all: _CLS_package_mark_set_all

package_obsolete_marked: _CLS_package_obsolete_marked

package_show_clear: _CLS_package_show_clear

package_show_set: _CLS_package_show_set

package_show_settings: _CLS_package_show_settings

package_theme_disable: _CLS_package_theme_disable

package_theme_enable: _CLS_package_theme_enable

package_uninstall: _CLS_package_uninstall

package_uninstall_marked: _CLS_package_uninstall_marked

package_uninstall_system: _CLS_package_uninstall_system

package_upgrade_all: _CLS_package_upgrade_all

repo_enable_from_drop: _CLS_repo_enable_from_drop

repo_lock_all: _CLS_repo_lock_all

repo_refresh_all: _CLS_repo_refresh_all

repo_sync: _CLS_repo_sync

repo_sync_all: _CLS_repo_sync_all

repo_unlock: _CLS_repo_unlock

repo_unlock_all: _CLS_repo_unlock_all

status_clear: _CLS_status_clear

status_clear_errors: _CLS_status_clear_errors

userpref_allow_online: _CLS_userpref_allow_online

userpref_allow_online_popup: _CLS_userpref_allow_online_popup

userpref_show_for_update: _CLS_userpref_show_for_update

userpref_show_online: _CLS_userpref_show_online

userpref_tags_set: _CLS_userpref_tags_set
