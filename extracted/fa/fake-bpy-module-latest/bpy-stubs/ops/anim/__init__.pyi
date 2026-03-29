import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def change_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    frame: float | None = 0.0,
    snap: bool | None = False,
    seq_solo_preview: bool | None = False,
    pass_through_on_strip_handles: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interactively change the current frame number

    :param frame: Frame, (in [-1.04857e+06, 1.04857e+06], optional)
    :param snap: Snap, (optional)
    :param seq_solo_preview: Strip Preview, (optional)
    :param pass_through_on_strip_handles: Pass Through on Strip Handles, Allow another operator to operate on strip handles (optional)
    :return: Result of the operator call.
    """

def channel_select_keys(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all keyframes of channel under mouse

    :param extend: Extend, Extend selection (optional)
    :return: Result of the operator call.
    """

def channel_view_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    include_handles: bool | None = True,
    use_preview_range: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset viewable area to show the channel under the cursor

    :param include_handles: Include Handles, Include handles of keyframes when calculating extents (optional)
    :param use_preview_range: Use Preview Range, Ignore frames outside of the preview range (optional)
    :return: Result of the operator call.
    """

def channels_bake(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_scene_range: bool | None = True,
    range: collections.abc.Sequence[int] | None = (0, 0),
    step: float | None = 1.0,
    remove_outside_range: bool | None = False,
    interpolation_type: typing.Literal["BEZIER", "LIN", "CONST"] | None = "BEZIER",
    bake_modifiers: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create keyframes following the current shape of F-Curves of selected channels

        :param use_scene_range: Use Scene Range, If enabled, the scene start and end frame will be used to determine the bake range (optional)
        :param range: Frame Range, The custom range in which to create new keys. Only used when not using the scene range (array of 2 items, in [-inf, inf], optional)
        :param step: Frame Step, At which interval to add keys (in [0.01, inf], optional)
        :param remove_outside_range: Remove Outside Range, Removes keys outside the given range, leaving only the newly baked (optional)
        :param interpolation_type: Interpolation Type, Choose the interpolation type with which new keys will be added (optional)

    BEZIER
    Bézier -- New keys will be Bézier.

    LIN
    Linear -- New keys will be linear.

    CONST
    Constant -- New keys will be constant.
        :param bake_modifiers: Bake Modifiers, Bake Modifiers into keyframes and delete them after (optional)
        :return: Result of the operator call.
    """

def channels_clean_empty(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete all empty animation data containers from visible data-blocks

    :return: Result of the operator call.
    """

def channels_click(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
    extend_range: bool | None = False,
    children_only: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Handle mouse clicks over animation channels

    :param extend: Extend Select, (optional)
    :param extend_range: Extend Range, Selection of active channel to clicked channel (optional)
    :param children_only: Select Children Only, (optional)
    :return: Result of the operator call.
    """

def channels_collapse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Collapse (close) all selected expandable animation channels

    :param all: All, Collapse all channels (not just selected ones) (optional)
    :return: Result of the operator call.
    """

def channels_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete all selected animation channels

    :return: Result of the operator call.
    """

def channels_editable_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["TOGGLE", "DISABLE", "ENABLE", "INVERT"] | None = "TOGGLE",
    type: typing.Literal["PROTECT", "MUTE"] | None = "PROTECT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle editability of selected channels

    :param mode: Mode, (optional)
    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def channels_expand(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Expand (open) all selected expandable animation channels

    :param all: All, Expand all channels (not just selected ones) (optional)
    :return: Result of the operator call.
    """

def channels_fcurves_enable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear disabled tag from all F-Curves to get broken F-Curves working again

    :return: Result of the operator call.
    """

def channels_group(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add selected F-Curves to a new group

    :param name: Name, Name of newly created group (optional, never None)
    :return: Result of the operator call.
    """

def channels_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    direction: typing.Literal["TOP", "UP", "DOWN", "BOTTOM"] | None = "DOWN",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rearrange selected animation channels

    :param direction: Direction, (optional)
    :return: Result of the operator call.
    """

def channels_rename(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Rename animation channel under mouse

    :return: Result of the operator call.
    """

def channels_select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle selection of all animation channels

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

def channels_select_box(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
    deselect: bool | None = False,
    extend: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all animation channels within the specified region

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :param deselect: Deselect, Deselect rather than select items (optional)
    :param extend: Extend, Extend selection instead of deselecting everything first (optional)
    :return: Result of the operator call.
    """

def channels_select_filter(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Start entering text which filters the set of channels shown to only include those with matching names

    :return: Result of the operator call.
    """

def channels_setting_disable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["TOGGLE", "DISABLE", "ENABLE", "INVERT"] | None = "DISABLE",
    type: typing.Literal["PROTECT", "MUTE"] | None = "PROTECT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Disable specified setting on all selected animation channels

    :param mode: Mode, (optional)
    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def channels_setting_enable(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["TOGGLE", "DISABLE", "ENABLE", "INVERT"] | None = "ENABLE",
    type: typing.Literal["PROTECT", "MUTE"] | None = "PROTECT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Enable specified setting on all selected animation channels

    :param mode: Mode, (optional)
    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def channels_setting_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    mode: typing.Literal["TOGGLE", "DISABLE", "ENABLE", "INVERT"] | None = "TOGGLE",
    type: typing.Literal["PROTECT", "MUTE"] | None = "PROTECT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle specified setting on all selected animation channels

    :param mode: Mode, (optional)
    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def channels_ungroup(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected F-Curves from their current groups

    :return: Result of the operator call.
    """

def channels_view_selected(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    include_handles: bool | None = True,
    use_preview_range: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset viewable area to show the selected channels

    :param include_handles: Include Handles, Include handles of keyframes when calculating extents (optional)
    :param use_preview_range: Use Preview Range, Ignore frames outside of the preview range (optional)
    :return: Result of the operator call.
    """

def clear_useless_actions(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    only_unused: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mark actions with no F-Curves for deletion after save and reload of file preserving "action libraries"

    :param only_unused: Only Unused, Only unused (Fake User only) actions get considered (optional)
    :return: Result of the operator call.
    """

def copy_driver_button(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy the driver for the highlighted button

    :return: Result of the operator call.
    """

def driver_button_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add driver for the property under the cursor

    :return: Result of the operator call.
    """

def driver_button_edit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Edit the drivers for the connected property represented by the highlighted button

    :return: Result of the operator call.
    """

def driver_button_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the driver(s) for the connected property(s) represented by the highlighted button

    :param all: All, Delete drivers for all elements of the array (optional)
    :return: Result of the operator call.
    """

def end_frame_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the current frame as the preview or scene end frame

    :return: Result of the operator call.
    """

def keyframe_clear_button(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear all keyframes on the currently active property

    :param all: All, Clear keyframes from all elements of the array (optional)
    :return: Result of the operator call.
    """

def keyframe_clear_v3d(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all keyframe animation for selected objects

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def keyframe_clear_vse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all keyframe animation for selected strips

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def keyframe_delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DEFAULT"] | None = "DEFAULT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete keyframes on the current frame for all properties in the specified Keying Set

    :param type: Keying Set, The Keying Set to use (optional)
    :return: Result of the operator call.
    """

def keyframe_delete_button(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete current keyframe of current UI-active property

    :param all: All, Delete keyframes from all elements of the array (optional)
    :return: Result of the operator call.
    """

def keyframe_delete_by_name(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Alternate access to Delete Keyframe for keymaps to use

    :param type: Keying Set, The Keying Set to use (optional, never None)
    :return: Result of the operator call.
    """

def keyframe_delete_v3d(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove keyframes on current frame for selected objects and bones

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def keyframe_delete_vse(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove keyframes on current frame for selected strips

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def keyframe_insert(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DEFAULT"] | None = "DEFAULT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert keyframes on the current frame using either the active keying set, or the user preferences if no keying set is active

    :param type: Keying Set, The Keying Set to use (optional)
    :return: Result of the operator call.
    """

def keyframe_insert_button(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert a keyframe for current UI-active property

    :param all: All, Insert a keyframe for all element of the array (optional)
    :return: Result of the operator call.
    """

def keyframe_insert_by_name(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: str = "",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Alternate access to Insert Keyframe for keymaps to use

    :param type: Keying Set, The Keying Set to use (optional, never None)
    :return: Result of the operator call.
    """

def keyframe_insert_menu(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DEFAULT"] | None = "DEFAULT",
    always_prompt: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Insert Keyframes for specified Keying Set, with menu of available Keying Sets if undefined

    :param type: Keying Set, The Keying Set to use (optional)
    :param always_prompt: Always Show Menu, (optional)
    :return: Result of the operator call.
    """

def keying_set_active_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["DEFAULT"] | None = "DEFAULT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set a new active keying set

    :param type: Keying Set, The Keying Set to use (optional)
    :return: Result of the operator call.
    """

def keying_set_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new (empty) keying set to the active Scene

    :return: Result of the operator call.
    """

def keying_set_export(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    filepath: str = "",
    filter_folder: bool | None = True,
    filter_text: bool | None = True,
    filter_python: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Export Keying Set to a Python script

    :param filepath: filepath, (optional, never None)
    :param filter_folder: Filter folders, (optional)
    :param filter_text: Filter text, (optional)
    :param filter_python: Filter Python, (optional)
    :return: Result of the operator call.
    """

def keying_set_path_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add empty path to active keying set

    :return: Result of the operator call.
    """

def keying_set_path_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove active Path from active keying set

    :return: Result of the operator call.
    """

def keying_set_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the active keying set

    :return: Result of the operator call.
    """

def keyingset_button_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add current UI-active property to current keying set

    :param all: All, Add all elements of the array to a Keying Set (optional)
    :return: Result of the operator call.
    """

def keyingset_button_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove current UI-active property from current keying set

    :return: Result of the operator call.
    """

def merge_animation(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Merge the animation of the selected objects into the action of the active object. Actions are not deleted by this, but might end up with zero users

    :return: Result of the operator call.
    """

def paste_driver_button(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Paste the driver in the internal clipboard to the highlighted button

    :return: Result of the operator call.
    """

def previewrange_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Clear preview range

    :return: Result of the operator call.
    """

def previewrange_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    xmin: int | None = 0,
    xmax: int | None = 0,
    ymin: int | None = 0,
    ymax: int | None = 0,
    wait_for_input: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Interactively define frame range used for playback

    :param xmin: X Min, (in [-inf, inf], optional)
    :param xmax: X Max, (in [-inf, inf], optional)
    :param ymin: Y Min, (in [-inf, inf], optional)
    :param ymax: Y Max, (in [-inf, inf], optional)
    :param wait_for_input: Wait for Input, (optional)
    :return: Result of the operator call.
    """

def replace_action(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    old_session_uid: int | None = 0,
    new_session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap all users of one action to another one. The normal action slot assignment rules apply. This ignores the NLA and Action Constraints

    :param old_session_uid: Old Action, Old Actions session uid to replace (in [-inf, inf], optional)
    :param new_session_uid: Replacement Action, The replacement Actions session uid to remap all selected Actions users to (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def replace_action_new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    old_session_uid: int | None = 0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Swap all users of one action to a new action. This ignores the NLA and Action Constraints

    :param old_session_uid: Old Action, Old Actions session uid to replace (in [-inf, inf], optional)
    :return: Result of the operator call.
    """

def scene_range_frame(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reset the horizontal view to the current scene frame range, taking the preview range into account if it is active

    :return: Result of the operator call.
    """

def separate_slots(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move all slots of the action on the active object into newly created, separate actions. All users of those slots will be reassigned to the new actions. The current action wont be deleted but will be empty and might end up having zero users

    :return: Result of the operator call.
    """

def slot_channels_move_to_new_action(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move the selected slots into a newly created action

    :return: Result of the operator call.
    """

def slot_new_for_id(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Create a new action slot for this data-block, to hold its animation

    :return: Result of the operator call.
    """

def slot_unassign_from_constraint(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Un-assign the action slot from this constraint

    :return: Result of the operator call.
    """

def slot_unassign_from_id(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Un-assign the action slot, effectively making this data-block non-animated

    :return: Result of the operator call.
    """

def slot_unassign_from_nla_strip(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Un-assign the action slot from this NLA strip, effectively making it non-animated

    :return: Result of the operator call.
    """

def start_frame_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the current frame as the preview or scene start frame

    :return: Result of the operator call.
    """

def update_animated_transform_constraints(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_convert_to_radians: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Update f-curves/drivers affecting Transform constraints (use it with files from 2.70 and earlier)

    :param use_convert_to_radians: Convert to Radians, Convert f-curves/drivers affecting rotations to radians.Warning: Use this only once(optional)
    :return: Result of the operator call.
    """

def version_bone_hide_property(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Moves any F-Curves for the hide property of selected armatures into the action of the object. This will only operate on the first layer and strip of the action

    :return: Result of the operator call.
    """

def view_curve_in_graph_editor(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
    isolate: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Frame the property under the cursor in the Graph Editor

    :param all: Show All, Frame the whole array property instead of only the index under the cursor (optional)
    :param isolate: Isolate, Hides all F-Curves other than the ones being framed (optional)
    :return: Result of the operator call.
    """
