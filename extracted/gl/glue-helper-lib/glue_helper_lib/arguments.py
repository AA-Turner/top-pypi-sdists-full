import typing
from awsglue.utils import getResolvedOptions
import sys
import dataclasses


def parse_if_defined(
    arg_key: str,
    value_to_be_parsed: str,
    parsing_funs: typing.Optional[typing.Dict[str, typing.Callable]],
):
    if not parsing_funs:
        return value_to_be_parsed

    try:
        return parsing_funs[arg_key](value_to_be_parsed)
    except KeyError:
        return value_to_be_parsed


def parse_arguments_to_dict(
    custom_argument_keys: typing.Sequence[str],
    builtin_argument_keys: typing.Optional[typing.Sequence[str]] = None,
    parsing_funs: typing.Optional[typing.Dict[str, typing.Callable]] = None,
):
    args = getResolvedOptions(sys.argv, custom_argument_keys)
    all_argument_keys = (
        list(custom_argument_keys) + list(builtin_argument_keys)
        if builtin_argument_keys
        else custom_argument_keys
    )
    return {
        key: parse_if_defined(key, args[key], parsing_funs)
        for key in all_argument_keys
    }


class Arguments(typing.Protocol):
    """Interface for Glue job argument dataclasses.
    Can be implemented by defining a dataclass that inherrits
    from this protocol.
    The Dataclass can be instantiated by running
    dataclass.from_glue_arguments() insidevan AWS Glue job.
    """

    __dataclass_fields__: typing.ClassVar[typing.Dict]

    @classmethod
    def from_dict(cls, dict: typing.Dict[str, typing.Any]):
        return cls(**dict)

    @classmethod
    def _get_builtin_keys(cls):
        builtin_keys = ["JOB_NAME", "JOB_ID", "JOB_RUN_ID"]
        return [
            field_name
            for field_name in cls._field_names()
            if field_name in builtin_keys
        ]

    @classmethod
    def _field_names(cls):
        return [field.name for field in dataclasses.fields(cls)]

    @classmethod
    def parse_args_funs(cls):
        return None

    @classmethod
    def from_glue_arguments(cls):
        return cls.from_dict(
            parse_arguments_to_dict(
                cls._field_names(),
                cls._get_builtin_keys(),
                cls.parse_args_funs(),
            )
        )


@dataclasses.dataclass(kw_only=True)
class BaseJobArguments(Arguments):
    """Implementation of Arguments, with just the builtin
    'JOB_NAME' argument"""

    JOB_NAME: str
