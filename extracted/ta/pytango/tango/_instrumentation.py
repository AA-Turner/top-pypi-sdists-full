# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

import functools
import inspect
import os
import re
import sys
import threading
import warnings
from collections import namedtuple

from ._telemetry import _telemetry_runtime, _trace_api, _truthy_env_var
from ._warnings import PyTangoUserWarning
from .utils import _is_coroutine_function

_traced_coverage_run_active = False

try:
    import coverage

    _coverage = coverage.Coverage.current()
    if _coverage:
        _coverage_core = dict(_coverage.sys_info()).get("core", "").lower()
        if _coverage_core in {"pytracer", "ctracer"}:
            if _truthy_env_var("PYTANGO_DISABLE_COVERAGE_TRACE_PATCHING"):
                warnings.warn(
                    "Coverage run detected, but PYTANGO_DISABLE_COVERAGE_TRACE_PATCHING "
                    "environment variable is set. Reported coverage may be inaccurate.",
                    category=PyTangoUserWarning,
                    stacklevel=1,
                )
            else:
                if getattr(threading, "_trace_hook", None):
                    _traced_coverage_run_active = True
                    warnings.warn(
                        "Coverage run detected: tango.server.Device methods will be patched for tracing.",
                        category=PyTangoUserWarning,
                        stacklevel=1,
                    )
                else:
                    warnings.warn(
                        "Coverage run detected, but unable to get threading._trace_hook. "
                        "Reported coverage may be inaccurate.",
                        category=PyTangoUserWarning,
                        stacklevel=1,
                    )
except Exception:
    pass

_traced_debug_run_active = False
pydevd = None

try:
    _disabled_via_env_var = _truthy_env_var("PYTANGO_DISABLE_DEBUG_TRACE_PATCHING")
    if not _disabled_via_env_var:
        _forced_via_env_var = _truthy_env_var("PYTANGO_FORCE_DEBUG_TRACE_PATCHING")
        if sys.version_info < (3, 12) or _forced_via_env_var:
            if "PYDEVD_DISABLE_FILE_VALIDATION" not in os.environ:
                os.environ["PYDEVD_DISABLE_FILE_VALIDATION"] = "1"
            import pydevd

            _debugger = pydevd.get_global_debugger()
        else:
            _debugger = None

        if _debugger is not None:
            if _traced_coverage_run_active:
                warnings.warn(
                    "Debugger detected, but coverage run also detected. Patching only for coverage, not for debugger.",
                    category=PyTangoUserWarning,
                    stacklevel=1,
                )
            else:
                _traced_debug_run_active = True
                warnings.warn(
                    "Debugger detected: tango.server.Device methods will be patched for tracing.",
                    category=PyTangoUserWarning,
                    stacklevel=1,
                )
except Exception:
    pass


_force_tracing = _traced_debug_run_active or _traced_coverage_run_active or _telemetry_runtime.runtime_available()


def _forcefully_traced_method(fn, is_kernel_method=False):
    from tango.server import BaseDevice

    unwrapped_fn = inspect.unwrap(fn)

    def _telemetry_topic_enabled(device):
        if is_kernel_method:
            if _telemetry_runtime.skip_kernel_spans():
                return False
            return device._check_telemetry_topic("all")
        return device._check_telemetry_topic("user")

    def _get_device_server_trace_mode(*args):
        device = None
        emit_server_span = False
        propagate_context = False
        if _telemetry_runtime.runtime_available() and args:
            first = args[0]
            if isinstance(first, BaseDevice):
                device = first
            else:
                fn_self = getattr(unwrapped_fn, "__self__", None)
                if isinstance(fn_self, BaseDevice):
                    device = fn_self
            if device is not None:
                emit_server_span = (
                    device._is_telemetry_enabled()
                    and device._is_telemetry_tracing_enabled()
                    and _telemetry_topic_enabled(device)
                )
                propagate_context = device._is_telemetry_enabled()
        return device, emit_server_span, propagate_context

    def _set_sys_tracer_and_get_original():
        original_sys_tracer = "EMPTY"

        if _traced_coverage_run_active:
            original_sys_tracer = sys.gettrace()
            threading_trace_hook = getattr(threading, "_trace_hook", None)
            if threading_trace_hook:
                sys.settrace(threading_trace_hook)
        elif _traced_debug_run_active and pydevd is not None:
            pydevd.settrace(suspend=False, trace_only_current_thread=True)

        return original_sys_tracer

    @functools.wraps(fn)
    def trace_wrapper(*args, **kwargs):
        device, emit_server_span, propagate_context = _get_device_server_trace_mode(*args)
        original_sys_tracer = _set_sys_tracer_and_get_original()
        try:
            if emit_server_span and device is not None:
                with _telemetry_runtime.span_from_cpptango(device, fn):
                    ret = fn(*args, **kwargs)
            elif propagate_context:
                with _telemetry_runtime.context_from_cpptango():
                    ret = fn(*args, **kwargs)
            else:
                ret = fn(*args, **kwargs)
        finally:
            if original_sys_tracer != "EMPTY":
                sys.settrace(original_sys_tracer)
        return ret

    @functools.wraps(fn)
    async def async_trace_wrapper(*args, **kwargs):
        device, emit_server_span, propagate_context = _get_device_server_trace_mode(*args)
        original_sys_tracer = _set_sys_tracer_and_get_original()
        try:
            if emit_server_span and device is not None:
                with _telemetry_runtime.span_from_cpptango(device, fn):
                    ret = await fn(*args, **kwargs)
            elif propagate_context:
                with _telemetry_runtime.context_from_cpptango():
                    ret = await fn(*args, **kwargs)
            else:
                ret = await fn(*args, **kwargs)
        finally:
            if original_sys_tracer != "EMPTY":
                sys.settrace(original_sys_tracer)
        return ret

    if _is_coroutine_function(fn):
        return async_trace_wrapper
    return trace_wrapper


def _trace_client(fn, topic: str = "user"):
    """Wrapper/decorator to trace a client function for telemetry."""

    if _telemetry_runtime.runtime_available():
        fn_name = getattr(fn, "__qualname__", getattr(fn, "__name__", "unknown"))
        match = re.match(r"__(?P<prefix>\w+?)__(?P<suffix>.*)", fn_name)
        if match:
            fn_name = f"{match.group('prefix')}.{match.group('suffix')}"

        @functools.wraps(fn)
        def client_trace_wrapper(*args, **kwargs):
            location = kwargs.pop("trace_location", None)
            context = kwargs.pop("trace_context", None)
            _telemetry_runtime.refresh_from_env()
            if not _telemetry_runtime.can_propagate_context():
                return fn(*args, **kwargs)

            if _telemetry_runtime.should_emit_client_spans():
                tracer = _telemetry_runtime.get_or_create_client_tracer()
                if location is None:
                    filename, lineno, qualname = _get_non_tango_source_location()
                else:
                    filename, lineno, qualname = location
                with tracer.start_as_current_span(qualname, kind=_trace_api.SpanKind.CLIENT, context=context) as span:
                    span.set_attribute("code.filepath", filename)
                    span.set_attribute("code.lineno", lineno)
                    current_thread = threading.current_thread()
                    span.set_attribute("thread.id", hex(current_thread.ident))
                    span.set_attribute("thread.name", current_thread.name)
                    with _telemetry_runtime.span_to_cpptango(fn_name, topic=topic):
                        return fn(*args, **kwargs)

            with _telemetry_runtime.span_to_cpptango(fn_name, context=context, topic=topic):
                return fn(*args, **kwargs)

        client_trace_wrapper.__signature__ = inspect.signature(fn)
        client_trace_wrapper.__trace_kwargs__ = True
        return client_trace_wrapper

    return fn


_SourceLocation = namedtuple("_SourceLocation", ("filepath", "lineno", "qualname"))


def _get_non_tango_source_location(source=None) -> _SourceLocation:
    """Provides non-PyTango source caller for logging and tracing functions."""

    try:
        if source:
            source = inspect.unwrap(source)
            code = getattr(source, "__code__", None)
            if code:
                filepath = code.co_filename
                lineno = code.co_firstlineno
                qualname = getattr(code, "co_qualname", getattr(code, "co_name", str(source)))
                return _SourceLocation(filepath, lineno, qualname)
        else:
            caller, module = _get_first_non_tango_caller_and_module()
            if caller:
                code = caller.f_code
                filepath = code.co_filename
                lineno = caller.f_lineno
                qualname = getattr(code, "co_qualname", getattr(code, "co_name", "unknown"))
                if qualname == "<module>" and module in ("__main__", "__mp_main__"):
                    qualname = module
                return _SourceLocation(filepath, lineno, qualname)
        return _SourceLocation("(unknown)", 0, str(source))
    except Exception:
        return _SourceLocation("(unknown)", 0, str(source))


if hasattr(sys, "_getframemodulename") and hasattr(sys, "_getframe"):

    def _get_first_non_tango_caller_and_module():
        depth = 2
        caller = None
        while True:
            module = sys._getframemodulename(depth)
            if module != "tango" and not module.startswith("tango."):
                caller = sys._getframe(depth)
                break
            elif module is None:
                break
            depth += 1
        if caller:
            return caller, module
        return None, ""

elif hasattr(sys, "_getframe"):

    def _get_first_non_tango_caller_and_module():
        depth = 2
        caller = None
        module = ""
        try:
            while True:
                caller = sys._getframe(depth)
                module = caller.f_globals["__name__"]
                if module != "tango" and not module.startswith("tango."):
                    break
                depth += 1
        except ValueError:
            pass
        if caller:
            return caller, module
        return None, ""

else:

    def _get_first_non_tango_caller_and_module():
        for caller, _, _, _, _, _ in inspect.stack(0):
            module = caller.f_globals["__name__"]
            if module != "tango" and not module.startswith("tango."):
                return caller, module
        return None, ""
