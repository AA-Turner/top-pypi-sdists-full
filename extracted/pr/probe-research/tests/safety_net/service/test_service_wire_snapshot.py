"""Probe service API v1 as data: every wire constant's exact value, and every method's handler and policy.

tests/test_service_api_contract.py pins that no name an older client uses disappears (subset), and
tests/test_service_protocol.py::test_response_shapes pins the answer keys of the core methods on a
real service. This adds what they miss: exact values (limits, codes, messages, env lists, additions
included) and that every method still reaches a handler with the same policy and refusal shape.
"""

from __future__ import annotations

import inspect
import re

from probe.service import protocol, server


class _Anything:
    """Stands in for a Service: every attribute exists, so `_handlers()` can list its keys."""

    def __getattr__(self, name: str) -> _Anything:
        return self

    def __call__(self, *args, **kwargs) -> _Anything:
        return self


def _data(value):
    """The JSON form of a wire constant; `...` when it is not data (a function, a module)."""
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, (set, frozenset)):
        return sorted((_data(v) for v in value), key=repr)
    if isinstance(value, (list, tuple)):
        return [_data(v) for v in value]
    if isinstance(value, dict):
        return {str(k): _data(v) for k, v in sorted(value.items(), key=lambda kv: repr(kv[0]))}
    if isinstance(value, re.Pattern):
        return f"re:{value.pattern}"
    return ...


def _vocabulary() -> dict:
    """Every public constant of the protocol module: its classes' UPPER members and its own UPPER names."""
    classes, constants = {}, {}
    for name in dir(protocol):
        if name.startswith("_"):
            continue
        value = getattr(protocol, name)
        if inspect.isclass(value) and not issubclass(value, BaseException):
            members = {k: _data(v) for k, v in vars(value).items() if k.isupper() and _data(v) is not ...}
            if members:
                classes[name] = members
        elif name.isupper() and _data(value) is not ...:
            constants[name] = _data(value)
    return {"classes": classes, "constants": constants}


def _methods() -> dict:
    handled = set(server.Service._handlers(_Anything()))
    every = set(protocol.METHODS) | set(server.LOCAL_METHODS) | handled | set(server.METHOD_POLICY)
    return {
        method: {
            "in_protocol": method in protocol.METHODS,
            "local": method in server.LOCAL_METHODS,
            "handled": method in handled,
            "policy": server.METHOD_POLICY.get(method, "(default: work)"),
            "confined_answer": _data(server.CONFINED_ANSWERS.get(method)),
        }
        for method in sorted(every)
    }


def test_service_wire_vocabulary_is_unchanged(baseline):
    baseline("service_wire_vocabulary", _vocabulary())


def test_every_service_method_keeps_its_handler_policy_and_refusal(baseline):
    methods = _methods()
    unhandled = sorted(m for m, row in methods.items() if (row["in_protocol"] or row["local"]) and not row["handled"])
    assert not unhandled, f"methods with no handler (a client would get `internal error`): {unhandled}"
    baseline("service_methods", methods)
