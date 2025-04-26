from __future__ import annotations

import contextlib
import warnings
from contextvars import ContextVar

from chalk.utils.string import to_snake_case

_CHALK_NAMESPACE: ContextVar[str] = ContextVar("_CHALK_NAMESPACE")

_NAMESPACE_SEP = "::"


@contextlib.contextmanager
def namespace(name: str):
    """Activate the given namespace. All features and resolvers defined herein will belong to this namespace, even if they defined in different files.

    This is an experimental feature and support for feature namespaces may change in backwards-incompatible ways.
    """
    warnings.warn(
        (
            "Hey! It looks like you discovered an experimental Chalk feature. Namespace contexts are not fully "
            "supported by Chalk, and they may change or break without notice, causing data loss. To fix, please "
            f"remove the call to the `with namespace('{name}'):` context manager."
        )
    )
    if len(name) == 0:
        raise ValueError("Namespace names cannot be empty.")
    new_namespace = build_namespaced_name(name=name)
    token = _CHALK_NAMESPACE.set(new_namespace)
    try:
        yield
    finally:
        _CHALK_NAMESPACE.reset(token)


def get_current_namespace() -> str:
    """Get the current namespace string"""
    return _CHALK_NAMESPACE.get()


def build_namespaced_name(*, namespace: str | None = None, name: str | None = None) -> str:
    """Prepend the namespace, with an extra separator token, onto the postfix. If the namespace is None, then the contextual namespace will be used"""
    if namespace is None:
        namespace = _CHALK_NAMESPACE.get("")
    if name is None:
        name = ""
    parts = (*(to_snake_case(x) for x in namespace.split(_NAMESPACE_SEP) if len(x) > 0), name)
    return _NAMESPACE_SEP.join(x for x in parts if len(x) > 0)
