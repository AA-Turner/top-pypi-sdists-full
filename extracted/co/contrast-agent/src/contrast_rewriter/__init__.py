# Copyright © 2026 Contrast Security, Inc.
# See https://www.contrastsecurity.com/enduser-terms-0317a for more details.
"""
Implements AST rewriter for Contrast Agent
"""

from __future__ import annotations

from datetime import datetime, timezone
import importlib.abc
import importlib.machinery
import importlib.util
import sys
import ast
import copy
import builtins
import operator
import os
import time
import cProfile
import contextvars
from types import ModuleType

# Seems like it is necessary to import this prior to rewriting to avoid some weird partial import state
import tokenize  # noqa: F401

from contrast_vendor.wrapt.importer import _ImportHookChainedLoader

# NOTE: It is extremely important to limit the number of imports used by this
# module. It should be restricted to only those imports that are absolutely
# necessary for the operation of the rewriter, and ideally should include only
# built-in or standard library modules that are already imported by the
# interpreter prior to the evaluation of this module. It is *very* important
# that this module does *not* import the core `contrast` package since that
# would introduce a huge number of dependencies that we do not want.
# By limiting the number of dependencies for the rewriter module, we can ensure
# that a minimal number of modules are already imported prior to the
# application of the rewriter, which means we maximize the coverage of our
# rewriter in application and library code.

_CONTRAST_PACKAGES = ["contrast", "contrast_vendor", "contrast_rewriter"]
# disable `assert` in contrast modules. We don't want to do this for contrast_vendor,
# since some vendored packages might rely on `assert` behavior.
_PACKAGES_TO_OPTIMIZE = ["contrast"]


class _ContrastImportHookChainedLoader(_ImportHookChainedLoader):
    pass


class DeferredLogger:
    def __init__(self):
        self.messages = []

    def debug(self, message, *args, **kwargs):
        kwargs.setdefault(
            "time", datetime.now(tz=timezone.utc).isoformat().replace("+00:00", "Z")
        )
        self.messages.append(("debug", message, args, kwargs))


# Can't use our Namespace here since we don't want to import contrast package yet
class rewriter_module:
    logger = DeferredLogger()
    enabled: bool = False
    registry = set()


LOG_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FORMAT = "{date_and_time} [{logger_name}] {msg}"


def log_stderr(msg: str, *, logger_name: str):
    """
    A basic logger that only depends on modules loaded before `sitecustomize`. Use
    sparingly, as these are highly visible and not configurable. We send all early logs
    to stderr (in structlog too) to minimize the probability of interfering with non-app
    process output in flex agent or operator environments.

    Use for log messages emitted before we have access to structlog.
    """
    date_and_time = time.strftime(LOG_TIME_FORMAT, time.localtime())
    output = LOG_FORMAT.format(
        date_and_time=date_and_time,
        logger_name=logger_name,
        msg=msg,
    )
    print(output, file=sys.stderr)


def _log(msg: str) -> None:
    log_stderr(msg, logger_name="contrast-rewriter")


STARTUP_PROFILER: contextvars.ContextVar[cProfile.Profile | None] = (
    contextvars.ContextVar("contrast_startup_profiler", default=None)
)
PROFILE_TIME_FORMAT = "%Y%m%d%H%M%S"
PROFILER_LOGGER_NAME = "contrast-startup-profiler"


def is_startup_profiler_enabled() -> bool:
    return sys.version_info[:2] < (3, 12) and bool(
        os.environ.get("CONTRAST_PROFILE_STARTUP")
    )


def start_profiler():
    """
    Create and enable a basic cProfile.Profile for the current context. Only for use in
    python 3.11 and earlier.

    This function is intended to be used during agent startup, when we can't use a
    contextmanager-based profiler (because the code section to be profiled doesn't
    necessarily align with a single function call that can be wrapped by a
    contextmanager). Additionally, this profiler's module dependencies are minimal, so
    it is suitable for use before the rewriter is registered.
    """
    if STARTUP_PROFILER.get() is not None:
        return

    log_stderr("Starting new profile", logger_name=PROFILER_LOGGER_NAME)
    profiler = cProfile.Profile()
    profiler.enable()
    STARTUP_PROFILER.set(profiler)


def stop_profiler(filename_slug: str):
    """
    Disable the cProfile.Profile previously created with `start_profiler` for the
    current context, outputting profile data to a file that will contain
    `filename_slug`. If the profiler was not running, take no action.

    It is the caller's responsibility to ensure that the provided slug contains
    filesystem-legal chars.
    """
    if (profiler := STARTUP_PROFILER.get()) is None:
        return

    profiler.disable()
    STARTUP_PROFILER.set(None)

    time_slug = time.strftime(PROFILE_TIME_FORMAT, time.localtime())
    # though collisions are possible here, colliding files should contain essentially
    # the same profiling data
    filename = f"cprofile-{time_slug}-{filename_slug}.startup.out"
    log_stderr(
        f"Writing out cprofile data: {filename}", logger_name=PROFILER_LOGGER_NAME
    )
    profiler.dump_stats(filename)


def _load_module(source, module, filename, *, force_optimize=False):
    """
    Convenience method to compile and execute the given module source

    It seems like we do not need any exception handling here since any
    exception that occurs gets handled further up by the import machinery and
    causes it to fall back on the original loader. This is definitely good for
    us since it means that even if we mess up here somehow, it shouldn't
    prevent the original module from being loaded. It will just be loaded
    without our rewrites.

    If force_optimize is set, python optimizations equivalent to PYTHONOPTIMIZE=1 or -O
    will be applied to the new module (if not already applied globally).
    """
    optimize_flag = max(1, sys.flags.optimize) if force_optimize else sys.flags.optimize
    code = compile(source, filename, "exec", dont_inherit=True, optimize=optimize_flag)
    exec(code, module.__dict__)


def add_dependency_to_module(module: ModuleType, dependency: ModuleType):
    """
    Add a dependency to the provided module if it doesn't already exist.
    """
    add_dependency_to_globals(module.__dict__, dependency)


def add_dependency_to_globals(globs: dict, dependency: ModuleType):
    """
    Add a dependency to the provided globals if it doesn't already exist.
    """
    globs.setdefault(_contrast_module_name(dependency.__name__), dependency)


def _contrast_module_name(module_name: str):
    return f"_contrast__{module_name}"


def _get_top_level_module_name(fullname: str) -> str:
    fullname_split = fullname.split(".")
    if len(fullname_split) == 0:
        return ""
    return fullname_split[0]


class ContrastMetaPathFinder(importlib.abc.MetaPathFinder):
    def __init__(self) -> None:
        super().__init__()
        self.in_progress = set()

    def find_spec(self, fullname, path, target=None):
        """
        The finder is in charge of finding a module's "spec". The spec includes import
        machinery metadata about the module - including its name, source file path, and
        the loader, among others.

        Here, we first use importlib's utility to get the spec for the module
        about to be imported. The problem with this spec is that it also uses the
        default loader, which isn't what we want. To get around this, we reuse some
        metadata and generate a new spec that points at our loader.
        """
        if fullname in self.in_progress:
            # Here, we're within our own call to importlib.util.find_spec.
            # return None to allow the following MetaPathFinders to find the spec.
            return None
        self.in_progress.add(fullname)
        try:
            spec = importlib.util.find_spec(fullname, path)

            if (
                spec is None
                or spec.origin is None
                or not isinstance(spec.loader, importlib.machinery.SourceFileLoader)
            ):
                rewriter_module.logger.debug(
                    "Skipping non-source module",
                    module_name=fullname,
                    path=getattr(spec, "origin", "<unknown>"),
                )
                return None

            new_spec = importlib.util.spec_from_file_location(
                fullname,
                spec.origin,
                loader=ContrastRewriteLoader(fullname, spec.origin),
                submodule_search_locations=spec.submodule_search_locations,
            )
            if new_spec is None:
                return None

            loader = getattr(new_spec, "loader", None)

            if loader and not isinstance(loader, _ContrastImportHookChainedLoader):
                new_spec.loader = _ContrastImportHookChainedLoader(loader)

            rewriter_module.logger.debug(
                "Updated spec for module: fullname=%s, path=%s",
                fullname,
                spec.origin,
            )
            return new_spec
        finally:
            self.in_progress.discard(fullname)


class ContrastRewriteLoader(importlib.machinery.SourceFileLoader):
    def exec_module(self, module) -> None:
        """
        This method is responsible for actually doing the module `exec`-ing. We take
        control of this system and do the following:
        - read the original source file. We require pyc caching to be disabled for this
        - parse the source file into an AST
        - rewrite the AST
        - compile the AST into a code object
        - exec the code object

        Note that we add our custom add function to the module's globals. This prevents
        the need for import rewriting entirely.

        Contrast modules are not rewritten. Instead, we compile them with python
        optimizations by default (as if using PYTHONOPTIMIZE=1 or -O). This removes
        `assert` and `if __debug__:` statements from contrast production code.
        """
        original_source_code = None
        filename = self.path

        # May be None in some cases such as for namespace packages
        if filename is None:
            return

        rewriter_module.logger.debug(
            "ContrastRewriteLoader started executing module",
            filename=filename,
            module_name=self.name,
        )

        try:
            original_source_code = self.get_source(self.name)
            tree = ast.parse(original_source_code)
        except Exception as ex:
            rewriter_module.logger.debug(
                "WARNING: failed to parse module AST",
                filename=filename,
                exc_info=ex,
                module_name=self.name,
            )

            _load_module(original_source_code, module, filename)
            return

        if _get_top_level_module_name(self.name) in _PACKAGES_TO_OPTIMIZE:
            _load_module(
                original_source_code,
                module,
                filename,
                force_optimize=(not os.environ.get("CONTRAST_TESTING")),
            )
            return

        if module_was_rewritten(self.name):
            rewriter_module.logger.debug(
                "WARNING: module appears to have been already rewritten; will not rewrite again",
                filename=filename,
            )
        else:
            try:
                propagation_rewriter = PropagationRewriter()
                propagation_rewriter.visit(tree)
                propagation_rewriter.populate_dependencies(module)
            except Exception as ex:
                rewriter_module.logger.debug(
                    "WARNING: failed to rewrite module",
                    filename=filename,
                    exc_info=ex,
                    module_name=self.name,
                )

        rewriter_module.registry.add(self.name)

        _load_module(tree, module, filename)
        rewriter_module.logger.debug(
            "ContrastRewriteLoader finished executing module",
            filename=filename,
            module_name=self.name,
        )


class PropagationRewriter(ast.NodeTransformer):
    # all_possible_injected_modules holds a set of all modules
    # that could be injected into rewritten ASTs by any instance.
    #
    # This is a broad set. See the injected_modules instance
    # attribute for only the modules injected by one instance.
    all_possible_injected_modules = {builtins, operator}

    def __init__(self) -> None:
        super().__init__()
        self.injected_modules = set()

    def populate_dependencies(self, module: ModuleType):
        """
        Adds dependencies that were required by past rewrites.
        """
        for dependency in self.injected_modules:
            add_dependency_to_module(module, dependency)

    def _copy_with_context(self, node, context):
        node = copy.copy(node)
        node.ctx = context
        return node

    def _make_attr(self, module: ModuleType, attr: str):
        self.injected_modules.add(module)
        return ast.Attribute(
            value=ast.Name(id=_contrast_module_name(module.__name__), ctx=ast.Load()),
            attr=attr,
            ctx=ast.Load(),
        )

    def visit_BinOp(self, binop: ast.BinOp):
        """
        If we see an "Add" or a "Mod" binary operation, replace it with a call to our custom add/modulo
        function, which includes all necessary instrumentation.
        """
        binop.left = self.visit(binop.left)
        binop.right = self.visit(binop.right)

        if isinstance(binop.op, ast.Mod):
            binop_replacement = ast.Call(
                func=self._make_attr(operator, "mod"),
                args=[binop.left, binop.right],
                keywords=[],
            )
            ast.copy_location(binop_replacement, binop)
            return ast.fix_missing_locations(binop_replacement)

        if not isinstance(binop.op, ast.Add):
            return binop

        binop_replacement = ast.Call(
            func=self._make_attr(operator, "add"),
            args=[binop.left, binop.right],
            keywords=[],
        )
        ast.copy_location(binop_replacement, binop)
        return ast.fix_missing_locations(binop_replacement)

    def visit_AugAssign(self, node: ast.AugAssign):
        """
        If we see an "Append", `+=` operation, rewrite it as a `+`.
        """
        node.value = self.visit(node.value)

        if not isinstance(node.op, ast.Add):
            return node

        target = left = None
        if isinstance(node.target, ast.Name):
            name = ast.Name(id=node.target.id)
            target = self._copy_with_context(name, ast.Store())
            left = self._copy_with_context(name, ast.Load())
        else:
            target = node.target
            left = self._copy_with_context(target, ast.Load())

        call_contrast_append_node = ast.Assign(
            targets=[target],
            value=ast.Call(
                func=self._make_attr(operator, "iadd"),
                args=[self.visit(left), node.value],
                keywords=[],
            ),
        )
        ast.copy_location(call_contrast_append_node, node)
        return ast.fix_missing_locations(call_contrast_append_node)

    def visit_JoinedStr(self, node: ast.JoinedStr):
        node.values = [self.visit(value) for value in node.values]
        call_node = ast.Call(
            func=ast.Attribute(value=ast.Constant(""), attr="join", ctx=ast.Load()),
            args=[ast.List(elts=node.values, ctx=ast.Load())],
            keywords=[],
        )
        ast.copy_location(call_node, node)
        return ast.fix_missing_locations(call_node)

    def visit_FormattedValue(self, node: ast.FormattedValue):
        node.value = self.visit(node.value)

        # See https://docs.python.org/3/library/ast.html#ast.FormattedValue
        # for the conversion codes.
        if node.conversion != -1:
            if node.conversion == 115:
                conversion = "str"
            elif node.conversion == 114:
                conversion = "repr"
            elif node.conversion == 97:
                conversion = "ascii"
            else:
                rewriter_module.logger.debug(
                    "unexpected conversion code", code=node.conversion
                )
                return node

            node.value = ast.Call(
                func=self._make_attr(builtins, conversion),
                args=[node.value],
                keywords=[],
            )

        call_node = ast.Call(
            func=self._make_attr(builtins, "format"),
            args=[node.value, node.format_spec] if node.format_spec else [node.value],
            keywords=[],
        )
        ast.copy_location(call_node, node)
        return ast.fix_missing_locations(call_node)


def _non_contrast_module_filter(module_item) -> bool:
    return (
        _get_top_level_module_name(getattr(module_item[1], "__package__", "") or "")
        not in _CONTRAST_PACKAGES
    )


def _log_imported_modules() -> None:
    module_map = {
        importlib.machinery.BuiltinImporter: "builtin",
        importlib.machinery.FrozenImporter: "frozen",
    }

    all_modules = list(filter(_non_contrast_module_filter, sys.modules.items()))

    rewriter_module.logger.debug(
        "the following %d modules are already imported", len(all_modules)
    )
    for name, module in sorted(all_modules):
        module_type = module_map.get(getattr(module, "__loader__", None), "source")
        rewriter_module.logger.debug("%-20s type=%s", name, module_type)


def _hook_assertion_rewrites(rewrite_module):
    from contrast_vendor.wrapt import function_wrapper

    # This hook enables us to apply our rewriter before assertion rewrites are applied
    def rewrite_asserts(wrapped, _, args, kwargs):
        file_ast = args[0]
        PropagationRewriter().visit(file_ast)
        wrapped(*args, **kwargs)

    # This hook ensures that we add our contrast-specfic functions to the rewritten module
    def exec_module(wrapped, _, args, kwargs):
        module = args[0]
        for dep in PropagationRewriter.all_possible_injected_modules:
            add_dependency_to_module(module, dep)
        wrapped(*args, **kwargs)

    rewrite_module.rewrite_asserts = function_wrapper(rewrite_asserts)(
        rewrite_module.rewrite_asserts
    )
    rewrite_module.AssertionRewritingHook.exec_module = function_wrapper(exec_module)(
        rewrite_module.AssertionRewritingHook.exec_module
    )


def register_assertion_rewrite_hooks():
    """
    Register hooks for pytest's assertion rewriter

    This is only to be used for internal testing purposes. It enables our
    rewrites to be compatible with pytest's assertion rewrites.
    """
    from contrast_vendor.wrapt import register_post_import_hook

    register_post_import_hook(_hook_assertion_rewrites, "_pytest.assertion.rewrite")


def register():
    """
    Register our rewriter with the import system. After this call, any newly imported
    modules (from source code) will use our custom rewriter.

    Note that because this function is defined in the same module that defines our add
    replacement function, we never have to worry about rewriting the addition in the
    replacement function itself. If that were to occur, we would get an infinite
    recursion.
    """
    if is_rewriter_enabled():
        rewriter_module.logger.debug("Rewriter already enabled, not applying again")
        return

    # Useful for debugging, but slow
    # _log_imported_modules()

    sys.meta_path.insert(0, ContrastMetaPathFinder())

    rewriter_module.logger.debug("enabled AST rewriter")

    rewriter_module.enabled = True


def deregister():
    """
    Remove our rewriter from the import system. Modules that were loaded by our rewriter
    will remain rewritten.

    Return True if we find and deregister our machinery, False otherwise.
    """
    for i, finder in enumerate(sys.meta_path.copy()):
        if isinstance(finder, ContrastMetaPathFinder):
            sys.meta_path.pop(i)
            rewriter_module.enabled = False
            return True
    return False


def initialize_rewriter_logger(agent_logger):
    if not isinstance(rewriter_module.logger, DeferredLogger):
        agent_logger.debug("WARNING: cannot process deferred rewriter logs")
        return

    if len(rewriter_module.logger.messages) > 0:
        agent_logger.debug("---- Beginning of deferred rewriter logs ----")
        for level, message, args, kwargs in rewriter_module.logger.messages:
            getattr(agent_logger, level)(message, *args, **kwargs)
        agent_logger.debug("---- End of deferred rewriter logs ----")
        rewriter_module.logger.messages.clear()

    agent_logger.debug("Setting rewriter logger to agent logger")
    rewriter_module.logger = agent_logger


def is_rewriter_enabled() -> bool:
    return rewriter_module.enabled


def module_was_rewritten(name: str) -> bool:
    return name in rewriter_module.registry


def clear_registry():
    rewriter_module.registry.clear()
