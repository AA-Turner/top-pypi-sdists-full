"""Patching methods on a client object the customer constructed.

Most wrappers return a proxy. Bedrock and Cohere cannot: `boto3.client(...)`
builds its methods dynamically from a service model, so these two patch the
instance in place. That makes three things mandatory, all enforced here:
`functools.wraps` so `__wrapped__` holds the original, a marker so a second
`wrap_*` does not double-wrap, and an `unpatch` to undo it.
"""

from __future__ import annotations

import functools
import logging
from collections.abc import Callable
from types import MemberDescriptorType
from typing import Any

logger = logging.getLogger(__name__)

_MARKER = "_aigie_patched"


def _instance_owns(client: Any, attribute: str) -> bool:
    """Did the instance - not its class - hold this attribute before we wrote?

    Decides whether `unpatch` reassigns or deletes. A filled `__slots__` entry is
    instance state even though the descriptor lives on the type, so deleting it
    would throw the customer's own method away rather than restore it.
    """
    try:
        if attribute in getattr(client, "__dict__", {}):
            return True
        return isinstance(getattr(type(client), attribute, None), MemberDescriptorType)
    except Exception:  # noqa: BLE001 - a client may raise from `__dict__` itself
        return False


def _is_ours(fn: Any) -> bool:
    """Did we install this method?

    Identity, not truthiness: a client with a permissive `__getattr__` answers
    every name with something truthy, and would never be traced at all.
    """
    return getattr(fn, _MARKER, False) is True


def patch_method(client: Any, attribute: str, wrap: Callable[[Callable], Callable]) -> bool:
    """Replace `client.<attribute>` with `wrap(original)`, at most once.

    False means no patch: no such method, already ours, or assignment refused.
    """
    original = getattr(client, attribute, None)
    if original is None:
        return False

    if _is_ours(original):
        logger.debug("[wrapper] %s is already traced - not wrapping twice", attribute)
        return False

    traced = functools.wraps(original)(wrap(original))
    # `functools.wraps` merges the original's `__dict__` rather than replacing
    # ours, so the order here is not load-bearing - but setting it after keeps
    # the marker the last word on a method that already carried one.
    traced._aigie_patched = True  # type: ignore[attr-defined]
    # botocore builds methods on the class, so a name the instance did not own
    # must be deleted on restore rather than reassigned - a bound method left
    # shadowing the class attribute holds the client and leaks it.
    traced._aigie_owned_by_instance = _instance_owns(client, attribute)  # type: ignore[attr-defined]

    try:
        setattr(client, attribute, traced)
    except Exception as e:  # noqa: BLE001 - a sealed client can refuse in any way
        logger.debug("[wrapper] Could not patch %s: %s", attribute, e)
        return False
    return True


def unpatch_method(client: Any, attribute: str) -> bool:
    """Restore whatever `patch_method` replaced. Returns True if it restored."""
    current = getattr(client, attribute, None)
    if not _is_ours(current):
        return False

    original = getattr(current, "__wrapped__", None)
    if original is None:
        logger.debug("[wrapper] %s carries no __wrapped__ to restore", attribute)
        return False

    try:
        if getattr(current, "_aigie_owned_by_instance", True):
            setattr(client, attribute, original)
        else:
            delattr(client, attribute)
    except (AttributeError, TypeError) as e:
        logger.debug("[wrapper] Could not unpatch %s: %s", attribute, e)
        return False
    return True


def bind_options(factory: Callable[..., Callable], *options: Any) -> Callable[[Callable], Callable]:
    """Bind wrap-time options to a factory, leaving the one-arg patcher `patch_method` wants.

    The options are captured as arguments here rather than referenced from the
    enclosing scope, so a factory built in a loop keeps that iteration's values
    instead of the last one's.
    """
    return lambda original: factory(original, *options)


def unpatch_all(client: Any, attributes: tuple[str, ...]) -> bool:
    """Restore every patched method on `client`. True if any was restored."""
    return any([unpatch_method(client, attribute) for attribute in attributes])
