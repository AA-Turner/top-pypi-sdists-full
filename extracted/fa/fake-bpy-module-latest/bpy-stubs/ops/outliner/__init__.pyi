import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.ops
import bpy.stub_internal.rna_enums

class _CLS_action_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        action: str | None = "",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Change the active action used

        :param execution_context:
        :param undo:
        :param action: Action, (optional)
        :return: Result of the operator call.
        """

class _CLS_animdata_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "CLEAR_ANIMDATA", "SET_ACT", "CLEAR_ACT", "REFRESH_DRIVERS", "CLEAR_DRIVERS"
        ]
        | None = "CLEAR_ANIMDATA",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

                :param execution_context:
                :param undo:
                :param type: Animation Operation, (optional)

        CLEAR_ANIMDATA
        Clear Animation Data -- Remove this animation data container.

        SET_ACT
        Set Action.

        CLEAR_ACT
        Unlink Action.

        REFRESH_DRIVERS
        Refresh Drivers.

        CLEAR_DRIVERS
        Clear Drivers.
                :return: Result of the operator call.
        """

class _CLS_clear_filter(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear the search filter

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_color_tag_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        color: typing.Literal[bpy.stub_internal.rna_enums.CollectionColorItems]
        | None = "NONE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set a color tag for the selected collections

        :param execution_context:
        :param undo:
        :param color: Color Tag, (optional)
        :return: Result of the operator call.
        """

class _CLS_collection_disable(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Disable viewport display in the view layers

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_disable_render(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Do not render this collection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drag to move to collection in Outliner

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_duplicate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Recursively duplicate the collection, all its children, objects and object data

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_duplicate_linked(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Recursively duplicate the collection, all its children and objects, with linked object data

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_enable(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Enable viewport display in the view layers

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_enable_render(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Render the collection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_exclude_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Include collection in the active view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_exclude_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Exclude collection from the active view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_hide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Hide the collection in this view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_hide_inside(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Hide all the objects and collections inside the collection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_hierarchy_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete selected collection hierarchies

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_holdout_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear masking of collection in the active view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_holdout_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Mask collection in the active view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_indirect_only_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear collection contributing only indirectly in the view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_indirect_only_set(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Set collection to only contribute indirectly (through shadows and reflections) in the view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_instance(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Instance selected collections to active scene

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_isolate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        extend: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Hide all but this collection and its parents

        :param execution_context:
        :param undo:
        :param extend: Extend, Extend current visible collections (optional)
        :return: Result of the operator call.
        """

class _CLS_collection_link(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Link selected collections to active scene

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_new(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        nested: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add a new collection inside selected collection

        :param execution_context:
        :param undo:
        :param nested: Nested, Add as child of selected collection (optional)
        :return: Result of the operator call.
        """

class _CLS_collection_objects_deselect(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Deselect objects in collection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_objects_select(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Select objects in collection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_show(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Show the collection in this view layer

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_collection_show_inside(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Show all the objects and collections inside the collection

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_constraint_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["ENABLE", "DISABLE", "DELETE"] | None = "ENABLE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param type: Constraint Operation, (optional)
        :return: Result of the operator call.
        """

class _CLS_data_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["DEFAULT"] | None = "DEFAULT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param type: Data Operation, (optional)
        :return: Result of the operator call.
        """

class _CLS_datastack_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy or reorder modifiers, constraints, and effects

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        hierarchy: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete selected objects and collections

        :param execution_context:
        :param undo:
        :param hierarchy: Hierarchy, Delete child objects and collections (optional)
        :return: Result of the operator call.
        """

class _CLS_drivers_add_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add drivers to selected items

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_drivers_delete_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete drivers assigned to selected items

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_expanded_toggle(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Expand/Collapse all items

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_hide(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Hide selected objects and collections

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_highlight_update(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Update the item highlight based on the current mouse position

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_id_copy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Copy the selected data-blocks to the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_id_delete(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Delete the ID under cursor

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_id_linked_relocate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Replace the active linked ID (and its dependencies if any) by another one, from the same or a different library

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_id_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "UNLINK",
            "LOCAL",
            "SINGLE",
            "DELETE",
            "REMAP",
            "COPY",
            "PASTE",
            "ADD_FAKE",
            "CLEAR_FAKE",
            "RENAME",
            "SELECT_LINKED",
        ]
        | None = "UNLINK",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """General data-block management operations

                :param execution_context:
                :param undo:
                :param type: ID Data Operation, (optional)

        UNLINK
        Unlink.

        LOCAL
        Make Local.

        SINGLE
        Make Single User.

        DELETE
        Delete.

        REMAP
        Remap Users -- Make all users of selected data-blocks to use instead current (clicked) one.

        COPY
        Copy.

        PASTE
        Paste.

        ADD_FAKE
        Add Fake User -- Ensure data-block gets saved even if it isnt in use (e.g. for motion and material libraries).

        CLEAR_FAKE
        Clear Fake User.

        RENAME
        Rename.

        SELECT_LINKED
        Select Linked.
                :return: Result of the operator call.
        """

class _CLS_id_paste(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Paste data-blocks from the internal clipboard

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_id_remap(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        id_type: typing.Literal[bpy.stub_internal.rna_enums.IdTypeItems]
        | None = "OBJECT",
        old_id: int | None = 0,
        new_id: int | None = 0,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param id_type: ID Type, (optional)
        :param old_id: Old ID, Old IDs session uid to remap data from (in [-inf, inf], optional)
        :param new_id: New ID, New IDs session uid to remap all selected IDs users to (in [-inf, inf], optional)
        :return: Result of the operator call.
        """

class _CLS_item_activate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        extend: bool | None = False,
        extend_range: bool | None = False,
        deselect_all: bool | None = False,
        recurse: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Handle mouse clicks to select and activate items

        :param execution_context:
        :param undo:
        :param extend: Extend, Extend selection for activation (optional)
        :param extend_range: Extend Range, Select a range from active element (optional)
        :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
        :param recurse: Recurse, Select objects recursively from active element (optional)
        :return: Result of the operator call.
        """

class _CLS_item_drag_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drag and drop element to another place

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_item_openclose(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        all: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle whether item under cursor is open or closed

        :param execution_context:
        :param undo:
        :param all: All, Close or open all items (optional)
        :return: Result of the operator call.
        """

class _CLS_item_rename(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        use_active: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Rename the active element

        :param execution_context:
        :param undo:
        :param use_active: Use Active, Rename the active item, rather than the one the mouse is over (optional)
        :return: Result of the operator call.
        """

class _CLS_keyingset_add_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Add selected items (blue-gray rows) to active Keying Set

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_keyingset_remove_selected(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Remove selected items (blue-gray rows) from active Keying Set

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_lib_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["DELETE", "RELOCATE", "RELOAD"] | None = "DELETE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

                :param execution_context:
                :param undo:
                :param type: Library Operation, (optional)

        DELETE
        Delete -- Delete this library and all its items.

        RELOCATE
        Relocate -- Select a new path for this library, and reload all its data.

        RELOAD
        Reload -- Reload all data from this library.
                :return: Result of the operator call.
        """

class _CLS_lib_relocate(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Relocate the library under cursor

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_liboverride_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "OVERRIDE_LIBRARY_CREATE_HIERARCHY",
            "OVERRIDE_LIBRARY_RESET",
            "OVERRIDE_LIBRARY_CLEAR_SINGLE",
        ]
        | None = "OVERRIDE_LIBRARY_CREATE_HIERARCHY",
        selection_set: typing.Literal["SELECTED", "CONTENT", "SELECTED_AND_CONTENT"]
        | None = "SELECTED",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Create, reset or clear library override hierarchies

                :param execution_context:
                :param undo:
                :param type: Library Override Operation, (optional)

        OVERRIDE_LIBRARY_CREATE_HIERARCHY
        Make -- Create a local override of the selected linked data-blocks, and their hierarchy of dependencies.

        OVERRIDE_LIBRARY_RESET
        Reset -- Reset the selected local overrides to their linked references values.

        OVERRIDE_LIBRARY_CLEAR_SINGLE
        Clear -- Delete the selected local overrides and relink their usages to the linked data-blocks if possible, else reset them and mark them as non editable.
                :param selection_set: Selection Set, Over which part of the tree items to apply the operation (optional)

        SELECTED
        Selected -- Apply the operation over selected data-blocks only.

        CONTENT
        Content -- Apply the operation over content of the selected items only (the data-blocks in their sub-tree).

        SELECTED_AND_CONTENT
        Selected & Content -- Apply the operation over selected data-blocks and all their dependencies.
                :return: Result of the operator call.
        """

class _CLS_liboverride_troubleshoot_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "OVERRIDE_LIBRARY_RESYNC_HIERARCHY",
            "OVERRIDE_LIBRARY_RESYNC_HIERARCHY_ENFORCE",
            "OVERRIDE_LIBRARY_DELETE_HIERARCHY",
        ]
        | None = "OVERRIDE_LIBRARY_RESYNC_HIERARCHY",
        selection_set: typing.Literal["SELECTED", "CONTENT", "SELECTED_AND_CONTENT"]
        | None = "SELECTED",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Advanced operations over library override to help fix broken hierarchies

                :param execution_context:
                :param undo:
                :param type: Library Override Troubleshoot Operation, (optional)

        OVERRIDE_LIBRARY_RESYNC_HIERARCHY
        Resync -- Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies.

        OVERRIDE_LIBRARY_RESYNC_HIERARCHY_ENFORCE
        Resync Enforce -- Rebuild the selected local overrides from their linked references, as well as their hierarchies of dependencies, enforcing these hierarchies to match the linked data (i.e. ignoring existing overrides on data-blocks pointer properties).

        OVERRIDE_LIBRARY_DELETE_HIERARCHY
        Delete -- Delete the selected local overrides (including their hierarchies of override dependencies) and relink their usages to the linked data-blocks.
                :param selection_set: Selection Set, Over which part of the tree items to apply the operation (optional)

        SELECTED
        Selected -- Apply the operation over selected data-blocks only.

        CONTENT
        Content -- Apply the operation over content of the selected items only (the data-blocks in their sub-tree).

        SELECTED_AND_CONTENT
        Selected & Content -- Apply the operation over selected data-blocks and all their dependencies.
                :return: Result of the operator call.
        """

class _CLS_material_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drag material to object in Outliner

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_modifier_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["APPLY", "DELETE", "TOGVIS", "TOGREN"] | None = "APPLY",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

        :param execution_context:
        :param undo:
        :param type: Modifier Operation, (optional)
        :return: Result of the operator call.
        """

class _CLS_object_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal[
            "SELECT", "DESELECT", "SELECT_HIERARCHY", "REMAP", "RENAME"
        ]
        | None = "SELECT",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Undocumented, consider contributing.

                :param execution_context:
                :param undo:
                :param type: Object Operation, (optional)

        SELECT
        Select.

        DESELECT
        Deselect.

        SELECT_HIERARCHY
        Select Hierarchy.

        REMAP
        Remap Users -- Make all users of selected data-blocks to use instead a new chosen one.

        RENAME
        Rename.
                :return: Result of the operator call.
        """

class _CLS_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Context menu for item operations

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_orphans_manage(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Open a window to manage unused data

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_orphans_purge(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        do_local_ids: bool | None = True,
        do_linked_ids: bool | None = True,
        do_recursive: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Clear all orphaned data-blocks without any users from the file

        :param execution_context:
        :param undo:
        :param do_local_ids: Local Data-blocks, Include unused local data-blocks into deletion (optional)
        :param do_linked_ids: Linked Data-blocks, Include unused linked data-blocks into deletion (optional)
        :param do_recursive: Recursive Delete, Recursively check for indirectly unused data-blocks, ensuring that no orphaned data-blocks remain after execution (optional)
        :return: Result of the operator call.
        """

class _CLS_parent_clear(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drag to clear parent in Outliner

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_parent_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drag to parent in Outliner

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_scene_drop(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Drag object to scene in Outliner

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_scene_operation(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        type: typing.Literal["DELETE"] | None = "DELETE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Context menu for scene operations

        :param execution_context:
        :param undo:
        :param type: Scene Operation, (optional)
        :return: Result of the operator call.
        """

class _CLS_scroll_page(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        up: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Scroll page up or down

        :param execution_context:
        :param undo:
        :param up: Up, Scroll up one page (optional)
        :return: Result of the operator call.
        """

class _CLS_select_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"]
        | None = "TOGGLE",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Toggle the Outliner selection of items

                :param execution_context:
                :param undo:
                :param action: Action, Selection action to execute (optional)

        TOGGLE
        Toggle -- Toggle selection for all elements.

        SELECT
        Select -- Select all elements.

        DESELECT
        Deselect -- Deselect all elements.

        INVERT
        Invert -- Invert selection of all elements.
                :return: Result of the operator call.
        """

class _CLS_select_box(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        tweak: bool | None = False,
        xmin: int | None = 0,
        xmax: int | None = 0,
        ymin: int | None = 0,
        ymax: int | None = 0,
        wait_for_input: bool | None = True,
        mode: typing.Literal["SET", "ADD", "SUB"] | None = "SET",
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Use box selection to select tree elements

                :param execution_context:
                :param undo:
                :param tweak: Tweak, Tweak gesture from empty space for box selection (optional)
                :param xmin: X Min, (in [-inf, inf], optional)
                :param xmax: X Max, (in [-inf, inf], optional)
                :param ymin: Y Min, (in [-inf, inf], optional)
                :param ymax: Y Max, (in [-inf, inf], optional)
                :param wait_for_input: Wait for Input, (optional)
                :param mode: Mode, (optional)

        SET
        Set -- Set a new selection.

        ADD
        Extend -- Extend existing selection.

        SUB
        Subtract -- Subtract existing selection.
                :return: Result of the operator call.
        """

class _CLS_select_walk(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        direction: typing.Literal["UP", "DOWN", "LEFT", "RIGHT"] | None = "UP",
        extend: bool | None = False,
        toggle_all: bool | None = False,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Use walk navigation to select tree elements

        :param execution_context:
        :param undo:
        :param direction: Walk Direction, Select/Deselect element in this direction (optional)
        :param extend: Extend, Extend selection on walk (optional)
        :param toggle_all: Toggle All, Toggle open/close hierarchy (optional)
        :return: Result of the operator call.
        """

class _CLS_show_active(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Open up the tree and adjust the view so that the active object is shown centered

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_show_hierarchy(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Open all object entries and close all others

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_show_one_level(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
        *,
        open: bool | None = True,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Expand/collapse all entries by one level

        :param execution_context:
        :param undo:
        :param open: Open, Expand all entries one level deep (optional)
        :return: Result of the operator call.
        """

class _CLS_start_filter(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Start entering filter text

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

class _CLS_unhide_all(bpy.ops._BPyOpsSubModOp):
    def __call__(
        self,
        execution_context: int | str | None = None,
        undo: bool | None = None,
        /,
    ) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
        """Unhide all objects and collections

        :param execution_context:
        :param undo:
        :return: Result of the operator call.
        """

action_set: _CLS_action_set

animdata_operation: _CLS_animdata_operation

clear_filter: _CLS_clear_filter

collection_color_tag_set: _CLS_collection_color_tag_set

collection_disable: _CLS_collection_disable

collection_disable_render: _CLS_collection_disable_render

collection_drop: _CLS_collection_drop

collection_duplicate: _CLS_collection_duplicate

collection_duplicate_linked: _CLS_collection_duplicate_linked

collection_enable: _CLS_collection_enable

collection_enable_render: _CLS_collection_enable_render

collection_exclude_clear: _CLS_collection_exclude_clear

collection_exclude_set: _CLS_collection_exclude_set

collection_hide: _CLS_collection_hide

collection_hide_inside: _CLS_collection_hide_inside

collection_hierarchy_delete: _CLS_collection_hierarchy_delete

collection_holdout_clear: _CLS_collection_holdout_clear

collection_holdout_set: _CLS_collection_holdout_set

collection_indirect_only_clear: _CLS_collection_indirect_only_clear

collection_indirect_only_set: _CLS_collection_indirect_only_set

collection_instance: _CLS_collection_instance

collection_isolate: _CLS_collection_isolate

collection_link: _CLS_collection_link

collection_new: _CLS_collection_new

collection_objects_deselect: _CLS_collection_objects_deselect

collection_objects_select: _CLS_collection_objects_select

collection_show: _CLS_collection_show

collection_show_inside: _CLS_collection_show_inside

constraint_operation: _CLS_constraint_operation

data_operation: _CLS_data_operation

datastack_drop: _CLS_datastack_drop

delete: _CLS_delete

drivers_add_selected: _CLS_drivers_add_selected

drivers_delete_selected: _CLS_drivers_delete_selected

expanded_toggle: _CLS_expanded_toggle

hide: _CLS_hide

highlight_update: _CLS_highlight_update

id_copy: _CLS_id_copy

id_delete: _CLS_id_delete

id_linked_relocate: _CLS_id_linked_relocate

id_operation: _CLS_id_operation

id_paste: _CLS_id_paste

id_remap: _CLS_id_remap

item_activate: _CLS_item_activate

item_drag_drop: _CLS_item_drag_drop

item_openclose: _CLS_item_openclose

item_rename: _CLS_item_rename

keyingset_add_selected: _CLS_keyingset_add_selected

keyingset_remove_selected: _CLS_keyingset_remove_selected

lib_operation: _CLS_lib_operation

lib_relocate: _CLS_lib_relocate

liboverride_operation: _CLS_liboverride_operation

liboverride_troubleshoot_operation: _CLS_liboverride_troubleshoot_operation

material_drop: _CLS_material_drop

modifier_operation: _CLS_modifier_operation

object_operation: _CLS_object_operation

operation: _CLS_operation

orphans_manage: _CLS_orphans_manage

orphans_purge: _CLS_orphans_purge

parent_clear: _CLS_parent_clear

parent_drop: _CLS_parent_drop

scene_drop: _CLS_scene_drop

scene_operation: _CLS_scene_operation

scroll_page: _CLS_scroll_page

select_all: _CLS_select_all

select_box: _CLS_select_box

select_walk: _CLS_select_walk

show_active: _CLS_show_active

show_hierarchy: _CLS_show_hierarchy

show_one_level: _CLS_show_one_level

start_filter: _CLS_start_filter

unhide_all: _CLS_unhide_all
