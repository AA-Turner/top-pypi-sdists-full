# Copyright 2025 Q-CTRL. All rights reserved.
#
# Licensed under the Q-CTRL Terms of service (the "License"). Unauthorized
# copying or use of this file, via any medium, is strictly prohibited.
# Proprietary and confidential. You may not use this file except in compliance
# with the License. You may obtain a copy of the License at
#
#    https://q-ctrl.com/terms
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS. See the
# License for the specific language.

from functools import wraps
from typing import (
    Any,
    Callable,
)

_REGISTRY: dict[str, Any] = {}


def global_value(key: str) -> Callable[[Callable[[], Any]], Callable[[], Any]]:
    """
    Add values to a global registry. If the
    `key` already exists in the registry, the
    stored value is returned.
    """

    def decorator(func: Callable[[], Any]) -> Callable[[], Any]:
        @wraps(func)
        def customized_decorator() -> Any:
            try:
                value = _REGISTRY[key]
            except KeyError:
                value = func()
                _REGISTRY[key] = value

            return value

        return customized_decorator

    return decorator


def update_global_value(key: str, value: Any) -> None:
    """Update global registry value."""
    if key in _REGISTRY:
        _REGISTRY[key] = value
    else:
        raise KeyError(f"Key not found in the registry: {key}")


def invalidate_global_value(*keys: str) -> None:
    """Remove the globally registered values, if they exist."""
    for key in keys:
        _REGISTRY.pop(key, None)
