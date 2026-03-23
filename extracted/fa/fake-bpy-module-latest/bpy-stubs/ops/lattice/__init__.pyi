import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def flip(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    axis: typing.Literal["U", "V", "W"] | None = "U",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Mirror all control points without inverting the lattice deform

    :param axis: Flip Axis, Coordinates along this axis get flipped (optional)
    :return: Result of the operator call.
    """

def make_regular(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Set UVW control points a uniform distance apart

    :return: Result of the operator call.
    """

def select_all(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    action: typing.Literal["TOGGLE", "SELECT", "DESELECT", "INVERT"] | None = "TOGGLE",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Change selection of all UVW control points

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
    """Deselect vertices at the boundary of each selection region

    :return: Result of the operator call.
    """

def select_mirror(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    axis: set[typing.Literal[bpy.stub_internal.rna_enums.AxisFlagXyzItems]] | None = {
        "X"
    },
    extend: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select mirrored lattice points

    :param axis: Axis, (optional)
    :param extend: Extend, Extend the selection (optional)
    :return: Result of the operator call.
    """

def select_more(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select vertices directly linked to already selected ones

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
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Randomly select UVW control points

        :param ratio: Ratio, Portion of items to select randomly (in [0, 1], optional)
        :param seed: Random Seed, Seed for the random number generator (in [0, inf], optional)
        :param action: Action, Selection action to execute (optional)

    SELECT
    Select -- Select all elements.

    DESELECT
    Deselect -- Deselect all elements.
        :return: Result of the operator call.
    """

def select_ungrouped(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    extend: bool | None = False,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Select vertices without a group

    :param extend: Extend, Extend the selection (optional)
    :return: Result of the operator call.
    """
