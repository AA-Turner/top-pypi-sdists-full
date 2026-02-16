import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def action_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: str | None = "",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the active action used

    :param action: Action, (optional)
    :return: Result of the operator call.
    """

def animdata_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[
        "CLEAR_ANIMDATA", "SET_ACT", "CLEAR_ACT", "REFRESH_DRIVERS", "CLEAR_DRIVERS"
    ]
    | None = "CLEAR_ANIMDATA",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

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

def clear_filter(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear the search filter

    :return: Result of the operator call.
    """

def collection_color_tag_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    color: Literal[bpy.stub_internal.rna_enums.CollectionColorItems] | None = "NONE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set a color tag for the selected collections

    :param color: Color Tag, (optional)
    :return: Result of the operator call.
    """

def collection_disable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Disable viewport display in the view layers

    :return: Result of the operator call.
    """

def collection_disable_render(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Do not render this collection

    :return: Result of the operator call.
    """

def collection_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drag to move to collection in Outliner

    :return: Result of the operator call.
    """

def collection_duplicate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Recursively duplicate the collection, all its children, objects and object data

    :return: Result of the operator call.
    """

def collection_duplicate_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Recursively duplicate the collection, all its children and objects, with linked object data

    :return: Result of the operator call.
    """

def collection_enable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enable viewport display in the view layers

    :return: Result of the operator call.
    """

def collection_enable_render(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Render the collection

    :return: Result of the operator call.
    """

def collection_exclude_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Include collection in the active view layer

    :return: Result of the operator call.
    """

def collection_exclude_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Exclude collection from the active view layer

    :return: Result of the operator call.
    """

def collection_hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide the collection in this view layer

    :return: Result of the operator call.
    """

def collection_hide_inside(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide all the objects and collections inside the collection

    :return: Result of the operator call.
    """

def collection_hierarchy_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected collection hierarchies

    :return: Result of the operator call.
    """

def collection_holdout_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear masking of collection in the active view layer

    :return: Result of the operator call.
    """

def collection_holdout_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mask collection in the active view layer

    :return: Result of the operator call.
    """

def collection_indirect_only_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear collection contributing only indirectly in the view layer

    :return: Result of the operator call.
    """

def collection_indirect_only_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set collection to only contribute indirectly (through shadows and reflections) in the view layer

    :return: Result of the operator call.
    """

def collection_instance(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Instance selected collections to active scene

    :return: Result of the operator call.
    """

def collection_isolate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide all but this collection and its parents

    :param extend: Extend, Extend current visible collections (optional)
    :return: Result of the operator call.
    """

def collection_link(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Link selected collections to active scene

    :return: Result of the operator call.
    """

def collection_new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    nested: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new collection inside selected collection

    :param nested: Nested, Add as child of selected collection (optional)
    :return: Result of the operator call.
    """

def collection_objects_deselect(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect objects in collection

    :return: Result of the operator call.
    """

def collection_objects_select(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select objects in collection

    :return: Result of the operator call.
    """

def collection_show(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show the collection in this view layer

    :return: Result of the operator call.
    """

def collection_show_inside(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show all the objects and collections inside the collection

    :return: Result of the operator call.
    """

def constraint_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["ENABLE", "DISABLE", "DELETE"] | None = "ENABLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param type: Constraint Operation, (optional)
    :return: Result of the operator call.
    """

def data_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DEFAULT"] | None = "DEFAULT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param type: Data Operation, (optional)
    :return: Result of the operator call.
    """

def datastack_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy or reorder modifiers, constraints, and effects

    :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    hierarchy: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected objects and collections

    :param hierarchy: Hierarchy, Delete child objects and collections (optional)
    :return: Result of the operator call.
    """

def drivers_add_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add drivers to selected items

    :return: Result of the operator call.
    """

def drivers_delete_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete drivers assigned to selected items

    :return: Result of the operator call.
    """

def expanded_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Expand/Collapse all items

    :return: Result of the operator call.
    """

def hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide selected objects and collections

    :return: Result of the operator call.
    """

def highlight_update(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update the item highlight based on the current mouse position

    :return: Result of the operator call.
    """

def id_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the selected data-blocks to the internal clipboard

    :return: Result of the operator call.
    """

def id_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete the ID under cursor

    :return: Result of the operator call.
    """

def id_linked_relocate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Replace the active linked ID (and its dependencies if any) by another one, from the same or a different library

    :return: Result of the operator call.
    """

def id_operation(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """General data-block management operations

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

def id_paste(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste data-blocks from the internal clipboard

    :return: Result of the operator call.
    """

def id_remap(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    id_type: Literal[bpy.stub_internal.rna_enums.IdTypeItems] | None = "OBJECT",
    old_id: int | None = 0,
    new_id: int | None = 0,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param id_type: ID Type, (optional)
    :param old_id: Old ID, Old IDs session uid to remap data from (in [-inf, inf], optional)
    :param new_id: New ID, New IDs session uid to remap all selected IDs users to (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def item_activate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    extend_range: bool | None = False,
    deselect_all: bool | None = False,
    recurse: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Handle mouse clicks to select and activate items

    :param extend: Extend, Extend selection for activation (optional)
    :param extend_range: Extend Range, Select a range from active element (optional)
    :param deselect_all: Deselect On Nothing, Deselect all when nothing under the cursor (optional)
    :param recurse: Recurse, Select objects recursively from active element (optional)
    :return: Result of the operator call.
    """

def item_drag_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drag and drop element to another place

    :return: Result of the operator call.
    """

def item_openclose(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle whether item under cursor is enabled or closed

    :param all: All, Close or open all items (optional)
    :return: Result of the operator call.
    """

def item_rename(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_active: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rename the active element

    :param use_active: Use Active, Rename the active item, rather than the one the mouse is over (optional)
    :return: Result of the operator call.
    """

def keyingset_add_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add selected items (blue-gray rows) to active Keying Set

    :return: Result of the operator call.
    """

def keyingset_remove_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected items (blue-gray rows) from active Keying Set

    :return: Result of the operator call.
    """

def lib_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DELETE", "RELOCATE", "RELOAD"] | None = "DELETE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

        :param type: Library Operation, (optional)

    DELETE
    Delete -- Delete this library and all its items.

    RELOCATE
    Relocate -- Select a new path for this library, and reload all its data.

    RELOAD
    Reload -- Reload all data from this library.
        :return: Result of the operator call.
    """

def lib_relocate(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Relocate the library under cursor

    :return: Result of the operator call.
    """

def liboverride_operation(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create, reset or clear library override hierarchies

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

def liboverride_troubleshoot_operation(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Advanced operations over library override to help fix broken hierarchies

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

def material_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drag material to object in Outliner

    :return: Result of the operator call.
    """

def modifier_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["APPLY", "DELETE", "TOGVIS", "TOGREN"] | None = "APPLY",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

    :param type: Modifier Operation, (optional)
    :return: Result of the operator call.
    """

def object_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["SELECT", "DESELECT", "SELECT_HIERARCHY", "REMAP", "RENAME"]
    | None = "SELECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undocumented, consider contributing.

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

def operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Context menu for item operations

    :return: Result of the operator call.
    """

def orphans_manage(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Open a window to manage unused data

    :return: Result of the operator call.
    """

def orphans_purge(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    do_local_ids: bool | None = True,
    do_linked_ids: bool | None = True,
    do_recursive: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear all orphaned data-blocks without any users from the file

    :param do_local_ids: Local Data-blocks, Include unused local data-blocks into deletion (optional)
    :param do_linked_ids: Linked Data-blocks, Include unused linked data-blocks into deletion (optional)
    :param do_recursive: Recursive Delete, Recursively check for indirectly unused data-blocks, ensuring that no orphaned data-blocks remain after execution (optional)
    :return: Result of the operator call.
    """

def parent_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drag to clear parent in Outliner

    :return: Result of the operator call.
    """

def parent_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drag to parent in Outliner

    :return: Result of the operator call.
    """

def scene_drop(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Drag object to scene in Outliner

    :return: Result of the operator call.
    """

def scene_operation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DELETE"] | None = "DELETE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Context menu for scene operations

    :param type: Scene Operation, (optional)
    :return: Result of the operator call.
    """

def scroll_page(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    up: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Scroll page up or down

    :param up: Up, Scroll up one page (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle the Outliner selection of items

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

def select_box(
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
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use box selection to select tree elements

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

def select_walk(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["UP", "DOWN", "LEFT", "RIGHT"] | None = "UP",
    extend: bool | None = False,
    toggle_all: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Use walk navigation to select tree elements

    :param direction: Walk Direction, Select/Deselect element in this direction (optional)
    :param extend: Extend, Extend selection on walk (optional)
    :param toggle_all: Toggle All, Toggle open/close hierarchy (optional)
    :return: Result of the operator call.
    """

def show_active(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Open up the tree and adjust the view so that the active object is shown centered

    :return: Result of the operator call.
    """

def show_hierarchy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Open all object entries and close all others

    :return: Result of the operator call.
    """

def show_one_level(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    open: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Expand/collapse all entries by one level

    :param open: Open, Expand all entries one level deep (optional)
    :return: Result of the operator call.
    """

def start_filter(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Start entering filter text

    :return: Result of the operator call.
    """

def unhide_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Unhide all objects and collections

    :return: Result of the operator call.
    """
