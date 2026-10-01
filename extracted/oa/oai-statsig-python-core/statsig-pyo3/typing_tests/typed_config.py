"""Static-only API contracts; checked with mypy --warn-unused-ignores."""

from typing import TypeVar

from google.protobuf.message import Message
from google.protobuf.struct_pb2 import Struct
from typing_extensions import assert_type

from statsig_python_core import Statsig, StatsigUser, TypedDynamicConfig

M = TypeVar("M", bound=Message)
T = TypeVar("T")


def wrapper(sdk: Statsig, user: StatsigUser, cls: type[M]) -> TypedDynamicConfig[M]:
    return sdk.get_typed_config("config", user, message_type=cls)


def valid_calls(sdk: Statsig, user: StatsigUser) -> None:
    assert_type(wrapper(sdk, user, Struct), TypedDynamicConfig[Struct])
    assert_type(
        sdk.get_typed_config("config", user, message_type=Struct),
        TypedDynamicConfig[Struct],
    )

    def callback(result: TypedDynamicConfig[Struct]) -> None:
        assert_type(result.value, Struct)

    sdk.register_typed_config_callback("config", user, callback, message_type=Struct)


def unbounded_wrapper(sdk: Statsig, user: StatsigUser, cls: type[T]) -> None:
    # Removing the Message bound must make these ignores fail as unused.
    sdk.get_typed_config("config", user, message_type=cls)  # type: ignore[type-var]
    sdk.register_typed_config_callback("config", user, lambda result: None, message_type=cls)  # type: ignore[type-var]


def invalid_class(sdk: Statsig, user: StatsigUser) -> None:
    sdk.get_typed_config("config", user, message_type=dict)  # type: ignore[type-var]
