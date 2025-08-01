# Copyright © 2025 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
from __future__ import annotations
import contextvars

import contextlib
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from contrast.agent.request_context import RequestContext


class CvarContextTracker:
    """
    This descriptor class makes it simpler to set/get a ContextVar.
    Classes instantiating this descriptor must pass the name of the instance variable to which
    the ContextVar is assigned to.

    For example, a class that uses this descriptor as such:

    class SomeClass:
        my_desc = CvarContextTracker("sample_attr")

        # must have an instance variable defined as such:
        def __init__(self):
            self.sample_attr = ContextVar(...)
    """

    def __init__(self, name):
        self._cvar_instance_name = name

    def __set__(self, instance, value):
        getattr(instance, self._cvar_instance_name).set(value)

    def __get__(self, instance, instance_type=None):
        val = None

        with contextlib.suppress(LookupError):
            val = getattr(instance, self._cvar_instance_name).get()

        return val


class ContextTracker:
    CURRENT_CONTEXT = "CURRENT_CONTEXT"
    _CVAR_INSTANCE_NAME = "_cvar"
    _CVAR_VAR_NAME = "contrast_request_context"
    _DEFAULT_CVAR_VALUE = None

    request_context = CvarContextTracker(_CVAR_INSTANCE_NAME)

    def __init__(self):
        self._cvar = contextvars.ContextVar(
            self._CVAR_VAR_NAME, default=self._DEFAULT_CVAR_VALUE
        )

    def get(self):
        return self.request_context

    def set(self, value):
        self.request_context = value

    def delete(self):
        self.request_context = None

    def set_current(self, value):
        self.request_context = value

    def delete_current(self):
        self.request_context = None

    @contextlib.contextmanager
    def lifespan(self, context):
        self.set_current(context)
        try:
            yield context
        finally:
            self.delete_current()

    def current(self) -> RequestContext | None:
        return self.request_context
