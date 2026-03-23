import typing
import collections.abc
import typing_extensions
import numpy.typing as npt
import bpy.stub_internal.rna_enums

def rule_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
    *,
    type: typing.Literal[bpy.stub_internal.rna_enums.BoidruleTypeItems] | None = "GOAL",
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a boid rule to the current boid state

    :param type: Type, (optional)
    :return: Result of the operator call.
    """

def rule_del(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete current boid rule

    :return: Result of the operator call.
    """

def rule_move_down(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move boid rule down in the list

    :return: Result of the operator call.
    """

def rule_move_up(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move boid rule up in the list

    :return: Result of the operator call.
    """

def state_add(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Add a boid state to the particle system

    :return: Result of the operator call.
    """

def state_del(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Delete current boid state

    :return: Result of the operator call.
    """

def state_move_down(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move boid state down in the list

    :return: Result of the operator call.
    """

def state_move_up(
    execution_context: int | str | None = None,
    undo: bool | None = None,
    /,
) -> set[typing.Literal[bpy.stub_internal.rna_enums.OperatorReturnItems]]:
    """Move boid state up in the list

    :return: Result of the operator call.
    """
