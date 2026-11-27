from contextvars import ContextVar
from types import MappingProxyType
from typing import Mapping

CallContextScalar = str | int | bool

_EMPTY: Mapping[str, CallContextScalar] = MappingProxyType({})

call_context_var: ContextVar[Mapping[str, CallContextScalar]] = ContextVar("call_context", default=_EMPTY)


def get_call_context() -> Mapping[str, CallContextScalar]:
    """Return the call context the API caller attached to the call that runs the current code.

    A start, signal or update request can carry a small mapping of technical values (ids, flags).
    It travels in a Temporal header, outside of payload encryption, so it is readable even when the
    input is fully encrypted.

    - The workflow body sees the one sent with its start. Workflow retries and cron runs reuse the
      start, so they see it again.
    - A signal or update handler, and an update validator, see the one sent with that call.
    - Everything else sees an empty mapping, including activities, child workflows and runs that
      continue as new, which the worker starts.

    The values are set by the API caller and deserve the same trust as the input: do not use them
    for authorization. Workers on an older SDK ignore the call context.
    """
    return call_context_var.get()
