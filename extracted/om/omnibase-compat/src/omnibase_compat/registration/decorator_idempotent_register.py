# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT

"""Idempotent registration decorator [OMN-9239].

Provides ``@idempotent_register(key_attr=...)`` which turns any
``register_X(self, obj, **kwargs)`` or ``register_X(self, **kwargs)`` method
into a no-op on duplicate keys, protecting registries from double-registration
during runtime boot or hot-reload scenarios.

Key extraction protocol (DETERMINISTIC):
  1. If the wrapped function has a keyword parameter matching ``key_attr``,
     use its value from the call.
  2. Else if the first positional non-self argument can carry an attribute
     named ``key_attr``, read it at call time via ``getattr``.
  3. Else raise :class:`TypeError` at decoration time.

State: per-decorated-function ``set[str]`` of seen key values, guarded by a
``threading.Lock``.
"""

from __future__ import annotations

import functools
import inspect
import logging
import threading
from collections.abc import Callable
from typing import Any, TypeVar, cast

_LOGGER = logging.getLogger(__name__)

F = TypeVar("F", bound=Callable[..., Any])


def idempotent_register(key_attr: str) -> Callable[[F], F]:
    """Decorator making a ``register_*`` method idempotent per extracted key.

    See module docstring for the key extraction protocol. Raises
    :class:`TypeError` at decoration time if neither path can satisfy the
    wrapped signature.

    Args:
        key_attr: The kwarg name (path 1) or object attribute name (path 2)
            used to extract the registration key from each call.

    Returns:
        A decorator that wraps the target function with idempotency logic.
    """

    def decorator(fn: F) -> F:
        signature = inspect.signature(fn)
        params = list(signature.parameters.values())

        # Determine the two candidate extraction paths at decoration time.
        has_matching_kwarg = any(
            p.name == key_attr
            and p.kind
            in (
                inspect.Parameter.KEYWORD_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
            )
            for p in params
        )

        # "first positional non-self" that *could* carry an attribute:
        # any POSITIONAL_OR_KEYWORD / POSITIONAL_ONLY / VAR_POSITIONAL after
        # a leading ``self`` (if present). Since we cannot introspect the
        # object's attributes at decoration time, we accept any positional
        # slot as potentially satisfying path 2.
        positional_candidates = [
            p
            for p in params
            if p.kind
            in (
                inspect.Parameter.POSITIONAL_ONLY,
                inspect.Parameter.POSITIONAL_OR_KEYWORD,
                inspect.Parameter.VAR_POSITIONAL,
            )
            and p.name != "self"
        ]
        # Exclude a positional slot that IS the key_attr kwarg — that's path 1
        # already, not path 2.
        positional_candidates = [p for p in positional_candidates if p.name != key_attr]
        has_positional_attr_candidate = len(positional_candidates) > 0

        if not (has_matching_kwarg or has_positional_attr_candidate):
            raise TypeError(
                "idempotent_register: cannot extract key "
                f"{key_attr!r} from signature of {fn.__qualname__!r}: "
                "neither a matching keyword parameter nor a positional "
                "non-self argument is present."
            )

        seen: set[str] = set()
        lock = threading.Lock()

        @functools.wraps(fn)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            # Bind args/kwargs to parameter names so POSITIONAL_OR_KEYWORD
            # parameters passed positionally still register as bound
            # arguments. Apply defaults so optional kwargs with a default
            # are present in ``bound.arguments``.
            try:
                bound = signature.bind_partial(*args, **kwargs)
            except TypeError as exc:
                raise TypeError(
                    f"idempotent_register: cannot bind call to {fn.__qualname__!r}: {exc}"
                ) from exc
            bound.apply_defaults()

            key: Any
            # Path 1 — key_attr resolves as a bound parameter name.
            if has_matching_kwarg and key_attr in bound.arguments:
                key = bound.arguments[key_attr]
            else:
                # Path 2 — read the attribute from the first positional
                # non-self argument. Skip a leading ``self`` if present.
                if not args:
                    raise TypeError(
                        "idempotent_register: no positional argument to "
                        f"read attribute {key_attr!r} from at call to "
                        f"{fn.__qualname__!r}"
                    )
                first_param = params[0] if params else None
                is_method = first_param is not None and first_param.name == "self"
                target_index = 1 if is_method else 0
                if is_method and len(args) <= 1:
                    raise TypeError(
                        "idempotent_register: no positional non-self "
                        f"argument to read attribute {key_attr!r} from at "
                        f"call to {fn.__qualname__!r}"
                    )
                target = args[target_index]
                try:
                    key = getattr(target, key_attr)
                except AttributeError as exc:
                    raise TypeError(
                        "idempotent_register: positional argument of type "
                        f"{type(target).__name__!r} has no attribute "
                        f"{key_attr!r} at call to {fn.__qualname__!r}"
                    ) from exc

            key_str = str(key)
            with lock:
                if key_str in seen:
                    _LOGGER.info(
                        "idempotent skip: %s already registered",
                        key_str,
                    )
                    return None
                result = fn(*args, **kwargs)
                seen.add(key_str)
                return result

        return cast(F, wrapper)

    return decorator
