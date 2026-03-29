import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums
import bpy.types

def brush_edit(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    stroke: bpy.types.bpy_prop_collection[bpy.types.OperatorStrokeElement]
    | None = None,
    pen_flip: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Apply a stroke of brush to the particles

    :param stroke: Stroke, (optional)
    :param pen_flip: Pen Flip, Whether a tablets eraser mode is being used (optional)
    :return: Result of the operator call.
    """

def connect_hair(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Connect hair to the emitter mesh

    :param all: All Hair, Connect all hair systems to the emitter mesh (optional)
    :return: Result of the operator call.
    """

def copy_particle_systems(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    space: typing.Literal["OBJECT", "WORLD"] | None = "OBJECT",
    remove_target_particles: bool | None = True,
    use_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Copy particle systems from the active object to selected objects

        :param space: Space, Space transform for copying from one object to another (optional)

    OBJECT
    Object -- Copy inside each objects local space.

    WORLD
    World -- Copy in world space.
        :param remove_target_particles: Remove Target Particles, Remove particle systems on the target objects (optional)
        :param use_active: Use Active, Use the active particle system from the context (optional)
        :return: Result of the operator call.
    """

def delete(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["PARTICLE", "KEY"] | None = "PARTICLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected particles or keys

    :param type: Type, Delete a full particle or only keys (optional)
    :return: Result of the operator call.
    """

def disconnect_hair(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    all: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Disconnect hair from the emitter mesh

    :param all: All Hair, Disconnect all hair systems from the emitter mesh (optional)
    :return: Result of the operator call.
    """

def duplicate_particle_system(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    use_duplicate_settings: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate particle system within the active object

    :param use_duplicate_settings: Duplicate Settings, Duplicate settings as well, so the new particle system uses its own settings (optional)
    :return: Result of the operator call.
    """

def dupliob_copy(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate the current instance object

    :return: Result of the operator call.
    """

def dupliob_move_down(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move instance object down in the list

    :return: Result of the operator call.
    """

def dupliob_move_up(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move instance object up in the list

    :return: Result of the operator call.
    """

def dupliob_refresh(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Refresh list of instance objects and their weights

    :return: Result of the operator call.
    """

def dupliob_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the selected instance object

    :return: Result of the operator call.
    """

def edited_clear(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Undo all edition performed on the particle system

    :return: Result of the operator call.
    """

def hair_dynamics_preset_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    name: str = "",
    remove_name: bool | None = False,
    remove_active: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add or remove a Hair Dynamics Preset

    :param name: Name, Name of the preset, used to make the path name (optional, never None)
    :param remove_name: remove_name, (optional)
    :param remove_active: remove_active, (optional)
    :return: Result of the operator call.
    """

def hide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide selected particles

    :param unselected: Unselected, Hide unselected rather than selected (optional)
    :return: Result of the operator call.
    """

def mirror(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate and mirror the selected particles along the local X axis

    :return: Result of the operator call.
    """

def new(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add new particle settings

    :return: Result of the operator call.
    """

def new_target(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a new particle target

    :return: Result of the operator call.
    """

def particle_edit_toggle(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Toggle particle edit mode

    :return: Result of the operator call.
    """

def particle_system_remove_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove all particle system within the active object

    :return: Result of the operator call.
    """

def rekey(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    keys_number: int | None = 2,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change the number of keys of selected particles (root and tip keys included)

    :param keys_number: Number of Keys, (in [2, inf], optional)
    :return: Result of the operator call.
    """

def remove_doubles(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    threshold: float | None = 0.0002,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove selected particles close enough to others

    :param threshold: Merge Distance, Threshold distance within which particles are removed (in [0, inf], optional)
    :return: Result of the operator call.
    """

def reveal(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Show hidden particles

    :param select: Select, (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """(De)select all particles keys

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

def select_less(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Deselect boundary selected keys of each particle

    :return: Result of the operator call.
    """

def select_linked(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select all keys linked to already selected ones

    :return: Result of the operator call.
    """

def select_linked_pick(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    deselect: bool | None = False,
    location: collections.abc.Sequence[int] | None = (0, 0),
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select nearest particle from mouse pointer

    :param deselect: Deselect, Deselect linked keys rather than selecting them (optional)
    :param location: Location, (array of 2 items, in [0, inf], optional)
    :return: Result of the operator call.
    """

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select keys linked to boundary selected keys of each particle

    :return: Result of the operator call.
    """

def select_random(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
    type: typing.Literal["HAIR", "POINTS"] | None = "HAIR",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select a randomly distributed set of hair or points

        :param ratio: Ratio, Portion of items to select randomly (in [0, 1], optional)
        :param seed: Random Seed, Seed for the random number generator (in [0, inf], optional)
        :param action: Action, Selection action to execute (optional)

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :param type: Type, Select either hair or points (optional)
        :return: Result of the operator call.
    """

def select_roots(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "SELECT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select roots of all visible particles

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

def select_tips(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "SELECT",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select tips of all visible particles

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

def shape_cut(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Cut hair to conform to the set shape object

    :return: Result of the operator call.
    """

def subdivide(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Subdivide selected particles segments (adds keys)

    :return: Result of the operator call.
    """

def target_move_down(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move particle target down in the list

    :return: Result of the operator call.
    """

def target_move_up(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move particle target up in the list

    :return: Result of the operator call.
    """

def target_remove(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Remove the selected particle target

    :return: Result of the operator call.
    """

def unify_length(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make selected hair the same length

    :return: Result of the operator call.
    """

def weight_set(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    factor: float | None = 1.0,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set the weight of selected keys

    :param factor: Factor, Interpolation factor between current brush weight, and keys weights (in [0, 1], optional)
    :return: Result of the operator call.
    """
