import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def delete_metaelems(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    confirm: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete selected metaball element(s)

    :param confirm: Confirm, Prompt for confirmation (optional)
    :return: Result of the operator call.
    """

def duplicate_metaelems(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Duplicate selected metaball element(s)

    :return: Result of the operator call.
    """

def duplicate_move(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    MBALL_OT_duplicate_metaelems: dict[str, typing.Any] | None = {},
    TRANSFORM_OT_translate: dict[str, typing.Any] | None = {},
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Make copies of the selected metaball elements and move them

    :param MBALL_OT_duplicate_metaelems: Duplicate Metaball Elements, Duplicate selected metaball element(s) (optional, `bpy.ops.mball.duplicate_metaelems` keyword arguments)
    :param TRANSFORM_OT_translate: Move, Move selected items (optional, `bpy.ops.transform.translate` keyword arguments)
    :return: Result of the operator call.
    """

def hide_metaelems(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    unselected: bool | None = False,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Hide (un)selected metaball element(s)

    :param unselected: Unselected, Hide unselected rather than selected (optional)
    :return: Result of the operator call.
    """

def reveal_metaelems(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    select: bool | None = True,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Reveal all hidden metaball elements

    :param select: Select, (optional)
    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change selection of all metaball elements

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

def select_random_metaelems(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    ratio: float | None = 0.5,
    seed: int | None = 0,
    action: typing.Literal["SELECT", "DESELECT"] | None = "SELECT",
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Randomly select metaball elements

        :param ratio: Ratio, Portion of items to select randomly (in [0, 1], optional)
        :param seed: Random Seed, Seed for the random number generator (in [0, inf], optional)
        :param action: Action, Selection action to execute (optional)

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :return: Result of the operator call.
    """

def select_similar(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal["TYPE", "RADIUS", "STIFFNESS", "ROTATION"] | None = "TYPE",
    threshold: float | None = 0.1,
) -> set[Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select similar metaballs by property types

    :param type: Type, (optional)
    :param threshold: Threshold, (in [0, inf], optional)
    :return: Result of the operator call.
    """
