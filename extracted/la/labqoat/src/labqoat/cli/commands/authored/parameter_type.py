"""Click types for primitive values and typed catalog references."""

from typing import Literal, get_args, get_origin
from types import UnionType
import typing

import click

from labqoat.cli.commands.authored.reference_parameter import ReferenceParameter
from labqoat.cli.commands.authored.structured_parameter import StructuredParameter


class ParameterType:
    """Translate supported signatures without interpreting string values as JSON."""

    @staticmethod
    def unwrap(annotation: object) -> object:
        """Accept optional annotations while retaining an omitted None default."""
        if get_origin(annotation) in (UnionType, typing.Union):
            members = tuple(value for value in get_args(annotation) if value is not type(None))
            if len(members) == 1:
                return members[0]
        return annotation

    @staticmethod
    def resolve(annotation: object) -> click.ParamType[object]:
        """Use shell scalars, literal choices and catalog references; anything else the SDK transports is JSON."""
        annotation = ParameterType.unwrap(annotation)
        scalars = {str: click.STRING, int: click.INT, float: click.FLOAT, bool: click.BOOL}
        if annotation in scalars:
            return scalars[annotation]
        if ReferenceParameter.matches(annotation):
            return ReferenceParameter(annotation)
        if get_origin(annotation) is Literal:
            values = get_args(annotation)
            if values and (all(type(value) is str for value in values) or all(type(value) is int for value in values)):
                return click.Choice(values)
        try:
            return StructuredParameter(annotation)
        except TypeError as error:
            raise click.UsageError(f"Unsupported CLI parameter type {annotation!r}: {error}") from error
