# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Controller for global scope state

Basically we use scoping to prevent us from assessing our own code. Scope
improves performance but it also prevents us from accidentally recursing
inside our analysis code. For example, we don't want to inadvertently cause
string propagation events while we're doing string building for reporting
purposes.
"""

import contextlib
from contextvars import ContextVar
import functools

CONTRAST_SCOPE = ContextVar("contrast_scope", default=0)
PROPAGATION_SCOPE = ContextVar("propagation_scope", default=0)
TRIGGER_SCOPE = ContextVar("trigger_scope", default=0)
OBSERVE_SCOPE = ContextVar("observe_scope", default=0)


def current_scope():
    return (
        CONTRAST_SCOPE.get(),
        PROPAGATION_SCOPE.get(),
        TRIGGER_SCOPE.get(),
        OBSERVE_SCOPE.get(),
    )


def set_scope(
    contrast_scope: int, propagation_scope: int, trigger_scope: int, observe_scope: int
):
    CONTRAST_SCOPE.set(contrast_scope)
    PROPAGATION_SCOPE.set(propagation_scope)
    TRIGGER_SCOPE.set(trigger_scope)
    OBSERVE_SCOPE.set(observe_scope)


def in_contrast_scope() -> bool:
    return CONTRAST_SCOPE.get() > 0


def in_propagation_scope() -> bool:
    return PROPAGATION_SCOPE.get() > 0


def in_trigger_scope() -> bool:
    return TRIGGER_SCOPE.get() > 0


def in_observe_scope() -> bool:
    return OBSERVE_SCOPE.get() > 0


def _build_scope_manager(scope: ContextVar):
    class _ScopeManager:
        def __enter__(self):
            # TODO: PYT-3433 ideally we'd use a token + reset() here, but this causes
            # LookupErrors in rare circumstances that we don't currently understand
            scope.set(scope.get() + 1)

        def __exit__(self, exc_type, exc_val, exc_tb):
            scope.set(scope.get() - 1)

        def __call__(self, f):
            @functools.wraps(f)
            def wrapper(*args, **kwargs):
                scope.set(scope.get() + 1)
                try:
                    return f(*args, **kwargs)
                finally:
                    scope.set(scope.get() - 1)

            return wrapper

    return _ScopeManager


contrast_scope = _build_scope_manager(CONTRAST_SCOPE)
propagation_scope = _build_scope_manager(PROPAGATION_SCOPE)
trigger_scope = _build_scope_manager(TRIGGER_SCOPE)
observe_scope = _build_scope_manager(OBSERVE_SCOPE)

###################################################
# Convenience functions not needed for all scopes #
###################################################


def in_contrast_or_propagation_scope():
    """Indicates we are in either contrast scope or propagation scope"""
    return in_contrast_scope() or in_propagation_scope()


@contextlib.contextmanager
def pop_contrast_scope():
    """
    Context manager that pops contrast scope and restores the previous scope level
    when it exits.
    """
    CONTRAST_SCOPE.set(CONTRAST_SCOPE.get() - 1)
    try:
        yield
    finally:
        CONTRAST_SCOPE.set(CONTRAST_SCOPE.get() + 1)
