import json
import os
from typing import Any, Callable, Mapping, Optional, Tuple, TypeVar, overload

T = TypeVar("T")


def has_integration(integration_name: str) -> bool:
    encoded = os.getenv("_CHALK_AVAILABLE_INTEGRATIONS")
    if encoded is not None:
        available = set(json.loads(encoded))
        return integration_name in available
    return False


def _get_integration_variable_name(name: str, integration_name: Optional[str]) -> str:
    return name if integration_name is None else f"{integration_name}_{name}"


def _serialize_integration_value_to_str(val: Any) -> str:
    if isinstance(val, bytes):
        return val.decode("utf-8")
    return str(val)


@overload
def load_integration_variable(
    name: str,
    integration_name: Optional[str],
    override: Optional[Mapping[str, str]],
) -> Optional[str]:
    ...


@overload
def load_integration_variable(
    name: str, integration_name: Optional[str], override: Optional[Mapping[str, str]], parser: Callable[[str], T]
) -> Optional[T]:
    ...


def load_integration_variable(
    name: str,
    integration_name: Optional[str],
    override: Optional[Mapping[str, str]],
    parser: Callable[[str], Any] = str,
) -> Optional[Any]:
    integration_var_name = _get_integration_variable_name(name, integration_name)
    if override is not None:
        value = override.get(integration_var_name, os.getenv(integration_var_name))
    else:
        value = os.getenv(integration_var_name)

    return parser(value) if value is not None else None


def create_integration_variable(
    name: str,
    integration_name: Optional[str],
    value: Any,
    serializer: Callable[[Any], str] = _serialize_integration_value_to_str,
) -> Tuple[str, Optional[str]]:
    return _get_integration_variable_name(name, integration_name), serializer(value) if value is not None else None
