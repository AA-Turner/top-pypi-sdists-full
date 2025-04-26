import argparse
import enum
import os
from datetime import datetime
from typing import Any, Callable, Optional, Type

from .dap_types import Format


class EnumAction(argparse.Action):
    "Sets the value of an argument of an enumeration type."

    _enum: Type[enum.Enum]

    def __init__(self, **kwargs: Any) -> None:
        # pop off the type value
        enum_type: Optional[type] = kwargs.pop("type", None)

        # ensure an Enum subclass is provided
        if enum_type is None:
            raise ValueError("type must be assigned an Enum when using EnumAction")
        if not issubclass(enum_type, enum.Enum):
            raise TypeError("type must be an Enum when using EnumAction")

        # generate choices from the Enum
        kwargs.setdefault("choices", tuple(e.value for e in enum_type))

        super().__init__(**kwargs)

        self._enum = enum_type

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: Optional[str] = None,
    ) -> None:
        # convert value back into an Enum
        value = self._enum(values)
        setattr(namespace, self.dest, value)


class EnvironmentDefault(argparse.Action):
    "Sets the value of an argument from an environment variable if no corresponding command-line argument is present."

    def __init__(
        self,
        var: str,
        *,
        required: bool = True,
        default: Optional[str] = None,
        help: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        if default is None:
            default = os.getenv(var)

        required = default is None

        # extend help text with variable name, and suppress printing default to avoid leaking secrets if environment variable is set
        text = f"{help} " if help is not None else ""
        suppress = "%(default).0s"
        help = f"{text}May be set via environment variable {var}.{suppress}"

        super().__init__(
            required=required,
            default=default,
            help=help,
            **kwargs,
        )

    def __call__(
        self,
        parser: argparse.ArgumentParser,
        namespace: argparse.Namespace,
        values: Any,
        option_string: Optional[str] = None,
    ) -> None:
        setattr(namespace, self.dest, values)


def environment_default(var: str) -> Callable[..., argparse.Action]:
    "Reads the value of an argument from the given environment variable if not supplied as a command-line argument."

    def _environment_default(**kwargs: Any) -> argparse.Action:
        return EnvironmentDefault(var, **kwargs)

    return _environment_default


class Arguments(argparse.Namespace):
    loglevel: str
    logfile: str

    base_url: str
    client_id: str
    client_secret: str

    connection_string: str

    command: str

    namespace: str
    table: str
    format: Format
    output_directory: str

    since: datetime
    until: Optional[datetime]
