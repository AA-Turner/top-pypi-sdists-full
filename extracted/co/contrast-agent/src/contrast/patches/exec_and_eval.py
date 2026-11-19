# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Instrumentation for exec/eval.

This was defined outside of policy.json because we need to pass globals/locals from the
frame in which function was originally called
"""

import __future__

import ast
import builtins
import operator
import sys
from collections.abc import Iterator
from contextlib import contextmanager
from functools import reduce, wraps
from sys import _getframe as getframe
from types import CodeType, FrameType, ModuleType

import contrast
from contrast.agent import scope
from contrast.agent.policy import patch_manager, registry_v2
from contrast.applies.assess.unsafe_code_execution import (
    apply_rule as apply_unsafe_code_exec_rule,
)
from contrast.utils.decorators import fail_quietly
from contrast.utils.patch_utils import (
    build_and_apply_patch,
    get_arg,
    register_module_patcher,
    set_arg,
    unregister_module_patcher,
)
from contrast_rewriter import PropagationRewriter, add_dependency_to_globals

orig_compile = builtins.compile


@scope.contrast_scope()
@fail_quietly("Error applying rule for exec/eval patch")
def apply_rule(rule_applicator, orig_func, result, args, kwargs):
    context = contrast.CONTEXT.get()
    with scope.pop_contrast_scope():
        # need to be in original scope to correctly check if we need to perform analysis
        if (
            context is None
            or not context.assess_enabled
            or scope.in_contrast_or_propagation_scope()
        ):
            return

    rule_applicator("builtins", orig_func.__name__, result, args, kwargs)


def rewrite(mode, code) -> tuple[CodeType, set[ModuleType]]:
    rewriter = PropagationRewriter()
    rewritten_code = rewriter.visit(ast.parse(code, mode=mode))
    return rewritten_code, rewriter.injected_modules


@scope.contrast_scope()
def apply_rewriter(mode, code, flags: int) -> tuple[CodeType, set[ModuleType]]:
    if not isinstance(code, str):
        return code, PropagationRewriter.all_possible_injected_modules

    rewritten_code, needs_modules = rewrite(mode, code)
    return (
        orig_compile(
            rewritten_code,
            filename="<internal>",
            mode=mode,
            flags=flags,
            # inheriting would cause changes in this module
            # to apply to the user code being compiled.
            dont_inherit=1,
        ),
        needs_modules,
    )


_FUTURE_FLAGS = reduce(
    operator.or_,
    [
        getattr(__future__, feature_name).compiler_flag
        for feature_name in __future__.all_feature_names
    ],
    0,
)


def future_flags(code: CodeType) -> int:
    """
    Extract the flags for future features from a code object.

    See https://docs.python.org/3/library/functions.html#compile
    documentation of "flags" parameter for more information.

    Also see "compute_code_flags" in Python's compile.c for
    the implementation of inheritance.
    """
    return code.co_flags & _FUTURE_FLAGS


# This is a context manager to guarantee that the frame is deleted.
# If the frame isn't deleted, we might end up with a reference cycle
# that would cascade into a memory leak, since the frame also holds
# references to the code object and the globals/locals.
# See the Note in https://docs.python.org/3/library/inspect.html#inspect.Traceback
@contextmanager
def calling_frame() -> Iterator[FrameType]:
    """
    Safely yields the frame that called into instrumentation.
    """
    # getframe at depth=3 because
    #   1 = context manager (caller of calling_frame)
    #   2 = patch function (caller of context manager)
    #   3 = user code (caller of patch function)
    # caller_frame also skips past general wrappers that might be applied,
    # depending on enabled modes
    frame = registry_v2.caller_frame(getframe(3))
    try:
        yield frame
    finally:
        del frame


def _frame_locals_proxy_type() -> type | None:
    """
    Returns the type of `f_locals` for a function's frame, which is a write-through
    proxy since Python 3.13 (PEP 667), or None for earlier versions.
    """
    if sys.version_info[:2] < (3, 13):
        return None
    return type(getframe().f_locals)


_FrameLocalsProxy = _frame_locals_proxy_type()


def _default_locals(frame: FrameType):
    """
    Returns the locals that exec and eval use when they're called from `frame` without
    globals or locals. Since Python 3.13 (PEP 667), these are a snapshot of a function's
    locals rather than the write-through proxy returned by `frame.f_locals`.
    """
    f_locals = frame.f_locals
    if _FrameLocalsProxy is not None and type(f_locals) is _FrameLocalsProxy:
        return dict(f_locals)
    return f_locals


def compile_source(mode: str, source, flags: int):
    """
    Compiles source for exec or eval the way they would themselves, but with the given
    __future__ compiler flags (the caller's) rather than this module's. Source is a str
    or any object supporting the buffer protocol, such as bytes or memoryview. Other
    source, such as code objects, is returned unchanged.
    """
    if isinstance(source, CodeType):
        return source
    if isinstance(source, str):
        # str.lstrip rather than source.lstrip, so that a subclass can't override it
        if mode == "eval":
            # eval ignores leading spaces and tabs, but compile doesn't
            source = str.lstrip(source, " \t")
    else:
        try:
            view = memoryview(source)
        except TypeError:
            # not valid source, so let exec or eval raise their own error
            return source
        with view:
            if not view.c_contiguous:
                # exec and eval reject these buffers, so let them raise their own error
                return source
            # tobytes returns exact bytes, so overrides in a subclass don't apply
            source = view.tobytes()
        if mode == "eval":
            source = source.lstrip(b" \t")
    return orig_compile(source, "<string>", mode, flags=flags, dont_inherit=True)


def build_exec_eval_patch(orig_func, _, rule_applicator, mode, assess=True):
    """
    Builds the patch for exec or eval.

    exec and eval depend on the frame that calls them: by default they run code in its
    globals and locals, and string source inherits its __future__ compiler flags. This
    patch calls the original function from a frame of its own, so it resolves those from
    the calling frame first, and passes them explicitly.

    When v2 policy is enabled, its generic wrapper is applied on top of this patch, and
    this patch is applied even if assess isn't enabled (`assess=False`), so that the
    wrapper doesn't need to know about exec and eval. Without assess, the patch only
    runs the code in the caller's namespace.
    """

    @wraps(orig_func)
    def exec_eval_patch(source, /, globals=None, locals=None, *, closure=None):
        # Code ported from six module
        # See https://github.com/benjaminp/six/blob/master/six.py#L694
        #
        # Reapplying the context from the calling frame is necessary because the
        # globals and locals in that frame are used in the original call to exec/eval.
        # The exception to this is if the caller passes custom globals/locals to the
        # function.
        #
        # If we fail provide this context we will see a number of NameErrors due to
        # things not defined in the scope of this function upon calling the original
        # function definition.
        result = None

        with calling_frame() as frame:
            if globals is None:
                globals = frame.f_globals
                if locals is None:
                    locals = _default_locals(frame)
            elif locals is None:
                locals = globals
            co_future_flags = future_flags(frame.f_code)

        if not assess:
            code = compile_source(mode, source, co_future_flags)
            if closure is None:
                return orig_func(code, globals, locals)
            return orig_func(code, globals, locals, closure=closure)

        try:
            code_to_run, needs_modules = apply_rewriter(mode, source, co_future_flags)
            # Ensure our rewriter patches are in (global) scope for the code about to be executed
            for mod in needs_modules:
                add_dependency_to_globals(globals, mod)
            result = (
                orig_func(code_to_run, globals, locals)
                if closure is None
                else orig_func(code_to_run, globals, locals, closure=closure)
            )
        except Exception:
            result = None
            raise
        finally:
            apply_rule(rule_applicator, orig_func, result, (source,), {})

        return result

    return exec_eval_patch


def build_compile_patch(orig_func, _, rule_applicator):
    def compile_patch(*args, **kwargs):
        if scope.in_contrast_scope():
            return orig_func(*args, **kwargs)

        result = None
        orig_args = args
        orig_kwargs = kwargs.copy()

        try:
            code = get_arg(args, kwargs, 0, kw="source")
            mode = get_arg(args, kwargs, 2, kw="mode", default="exec")
            flags = get_arg(args, kwargs, 3, kw="flags", default=0)
            if flags == 0:
                with calling_frame() as frame:
                    args, kwargs = set_arg(
                        future_flags(frame.f_code), args, kwargs, 3, kw="flags"
                    )
                    args, kwargs = set_arg(1, args, kwargs, 4, kw="dont_inherit")
            elif flags & ast.PyCF_ONLY_AST:
                # If the code is being parsed to an AST, it can't directly be exec'd or eval'd
                # so we don't need to apply the rewriter. We also don't want to conservatively
                # rewrite, because other tools might use the AST and raise errors when
                # encountering Contrast rewritten nodes. See SUP-6215 for an example.
                return orig_func(*args, **kwargs)

            with scope.contrast_scope():
                code_to_compile, _ = rewrite(mode, code)
                args, kwargs = set_arg(code_to_compile, args, kwargs, 0, kw="source")
                result = orig_func(*args, **kwargs)
        except Exception:
            result = None
            raise
        finally:
            apply_rule(rule_applicator, orig_func, result, orig_args, orig_kwargs)

        return result

    return compile_patch


def patch_exec_and_eval(builtins_module):
    build_and_apply_patch(
        builtins_module,
        "eval",
        build_exec_eval_patch,
        (apply_unsafe_code_exec_rule, "eval"),
    )

    build_and_apply_patch(
        builtins_module,
        "exec",
        build_exec_eval_patch,
        (apply_unsafe_code_exec_rule, "exec"),
    )

    build_and_apply_patch(
        builtins_module, "compile", build_compile_patch, (apply_unsafe_code_exec_rule,)
    )


def patch_exec_and_eval_for_policy_v2(builtins_module):
    """
    Patches exec and eval without assess, so that v2 policy's generic wrapper can be
    applied on top of these patches. See build_exec_eval_patch.
    """
    for mode in ("eval", "exec"):
        build_and_apply_patch(
            builtins_module, mode, build_exec_eval_patch, (None, mode, False)
        )


def register_patches():
    register_module_patcher(patch_exec_and_eval, builtins.__name__)


def register_policy_v2_patches():
    register_module_patcher(patch_exec_and_eval_for_policy_v2, builtins.__name__)


def reverse_patches():
    unregister_module_patcher(builtins.__name__)
    patch_manager.reverse_patches_by_owner(builtins)
