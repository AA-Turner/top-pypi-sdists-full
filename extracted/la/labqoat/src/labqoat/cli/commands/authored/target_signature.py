"""Signature-derived options with explicit SDK context injection."""

import inspect
from typing import get_type_hints

import click

from labqoat.cli.commands.authored.authored_target import AuthoredTarget
from labqoat.cli.commands.authored.parameter_type import ParameterType
from labqoat.cli.commands.authored.reference_parameter import ReferenceParameter
from labqoat.cli.commands.authored.structured_parameter import StructuredParameter
from labqoat.client import Client
from labqoat.compute.function import Function
from labqoat.run_context import RunContext


class TargetSignature:
    """Validate an entrypoint and build typed options before obtaining credentials."""

    def __init__(self, target: AuthoredTarget) -> None:
        """Hide the injected Client or RunContext and reject unsupported Python signatures."""
        self.annotations = get_type_hints(target.function)
        parameters = tuple(inspect.signature(target.function).parameters.values())
        injected = RunContext if isinstance(target.declaration, Function) else Client
        if not parameters or self.annotations.get(parameters[0].name) is not injected:
            raise click.UsageError(f"The first parameter must be annotated {injected.__name__}.")
        if "return" not in self.annotations:
            raise click.UsageError("Entrypoints must declare their return type.")
        self.parameters = parameters[1:]

    def options(self) -> list[click.Parameter]:
        """Expose named parameters as kebab-case options with authored defaults."""
        return [self._option(parameter) for parameter in self.parameters]

    def reference(self, name: str) -> ReferenceParameter | None:
        """Recognize a typed catalog input independently of its parameter name."""
        annotation = ParameterType.unwrap(self.annotations.get(name, str))
        return ReferenceParameter(annotation) if ReferenceParameter.matches(annotation) else None

    def structured(self, name: str) -> StructuredParameter | None:
        """A JSON parameter, which may name assets by ID inside its document."""
        kind = ParameterType.resolve(self.annotations.get(name, str))
        return kind if isinstance(kind, StructuredParameter) else None

    def resolve(self, client: Client, arguments: dict[str, object]) -> dict[str, object]:
        """Resolve catalog selectors into immutable input values before ordinary submission."""
        resolved = {}
        for name, value in arguments.items():
            parameter = self.reference(name) or self.structured(name)
            try:
                resolved[name] = value if parameter is None else parameter.resolve(client, value)
            except (TypeError, ValueError) as error:
                raise click.UsageError(f"Invalid --{name.replace('_', '-')} input: {error}") from error
        return resolved

    def _option(self, parameter: inspect.Parameter) -> click.Option:
        """Capture one option and its positive/negative boolean spellings."""
        if parameter.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
            raise click.UsageError("Entrypoints require explicitly named parameters.")
        annotation = self.annotations.get(parameter.name, str)
        kind = ParameterType.resolve(annotation)
        name = parameter.name.replace("_", "-")
        if name in ("help", "h"):
            raise click.UsageError(f"Parameter {parameter.name!r} conflicts with CLI help.")
        spelling = f"--{name}"
        if ParameterType.unwrap(annotation) is bool:
            spelling += f"/--no-{name}"
        required = parameter.default is inspect.Parameter.empty
        option = click.Option(
            [spelling, parameter.name],
            type=kind,
            required=required,
            show_default=True,
            help=kind.help() if isinstance(kind, StructuredParameter) else None,
        )
        if not required:
            option.default = parameter.default
        return option
