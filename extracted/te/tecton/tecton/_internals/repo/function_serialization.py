"""
Functions for serializing Python functions.

The only known areas where we will fail to serialize something usable are:

user imports like import foo.bar.baz instead of from foo.bar import baz
are not detected properly by the underlying library we use for looking up
dependencies. import json or other top-level modeuls still works just fine,
its just when you include multiple path components that we don't detect the
dependency properly

references to instantiated non-builtin types with a repr that can't be exec'd

users referring to a renamed version of an imported module has some wonky
behavior, for example `import json` then `foo=json` then referring to
`foo` in the func to be serialized.
"""

import inspect
import logging
from collections import defaultdict
from types import FunctionType
from types import ModuleType
from typing import Callable

from tecton.vendor.dill.dill.detect import freevars
from tecton.vendor.dill.dill.detect import globalvars
from tecton_core import conf
from tecton_core import repo_file_handler
from tecton_core.errors import TectonValidationError
from tecton_proto.args import user_defined_function__client_pb2 as user_defined_function_pb2


WINDOW_UNBOUNDED_PRECEDING = "unbounded_preceding"

logger = logging.getLogger(__name__)


def to_proto(transform: Callable) -> user_defined_function_pb2.UserDefinedFunction:
    if hasattr(transform, "_code"):
        code = transform._code
    else:
        code = _getsource(transform)

    _validate_code(code)
    isolate_function_deserialization = conf.IsolateFunctionDeserialization.enabled()

    return user_defined_function_pb2.UserDefinedFunction(
        name=transform.__name__, body=code, isolate_function_deserialization=isolate_function_deserialization
    )


BANNED_INDIRECT_IMPORTS = ["materialization_context", "tecton_sliding_window_udf", "WINDOW_UNBOUNDED_PRECEDING"]


def _validate_code(code):
    for banned_import in BANNED_INDIRECT_IMPORTS:
        if f"tecton.{banned_import}" in code:
            msg = f"Cannot serialize `tecton.{banned_import}`. Please use an import like `from tecton import {banned_import}`. Note that even comments may trigger this if your code contains `tecton.{banned_import}`"
            raise Exception(msg)


TECTON_TRANSFORMATION_WHITELIST = ["tecton/compat", "tecton\compat"]


# returns true if the module is defined by tecton, rather than by the user
def is_tecton_defined(module):
    return any(whitelist_str in module for whitelist_str in TECTON_TRANSFORMATION_WHITELIST)


def should_serialize_function(func):
    """Determines if the function should be serialized or not.

    During notebook development, not all functions need to be serialized since they never need to be sent over the wire.

    See https://www.notion.so/tecton/Micro-RFC-Function-Serialization-for-Notebook-Driven-Development-9385338c4fd144758fe3dc9587351142
    """
    # TECTON_FORCE_FUNCTION_SERIALIZATION is used for internal testing and also as a potential escape hatch for
    # notebook dev users.
    forced_behavior = conf.get_or_none("TECTON_FORCE_FUNCTION_SERIALIZATION")
    if forced_behavior is not None:
        if forced_behavior.lower() == "true":
            return True
        elif forced_behavior.lower() == "false":
            return False
        else:
            msg = "TECTON_FORCE_FUNCTION_SERIALIZATION should be 'true', 'false', or unset."
            raise ValueError(msg)

    func_module = inspect.getmodule(func)
    if func_module is None:
        # Used by NDD with EMR. In EMR pyspark notebook, 'inspect.getmodule' returns None for functions defined in main scope.
        return False

    if func_module.__name__ == "__main__":
        # This function was defined in the main module (i.e. probably in a notebook or repl). Do not attempt to
        # serialize it.
        return False

    func_file = inspect.getfile(func_module)

    if is_tecton_defined(func_file):
        # This is a Tecton defined transformation. It should always be serialized.
        return True

    if repo_file_handler.is_file_in_a_tecton_repo(func_file):
        # If a function is in a Tecton repo (i.e. an ancestor directory has a .tecton file), then always attemp to
        # serialize it. In notebook development, this will occur if an FCO is imported into the notebook from a repo.
        repo_file_handler.ensure_prepare_repo(func_file)
        if func_file not in repo_file_handler.repo_files_set():
            msg = f'Error during function serialization. The file "{func_file}" is in a Tecton repo but not in the cached repo data. Importing Tecton objects from multiple repos is not supported.'
            raise TectonValidationError(msg)
        return True
    else:
        # This function is defined outside of the main module, but not in a Tecton repo. Do not attempt to serialize it.
        return False


# UNDONE:
# this breaks for the following case:
# def f():
#    a = module.CONSTANT
#
# for some reason, the module/constant don't show up in globalvars.
# this case has not occurred in practice
def _getsource(func):
    imports = defaultdict(set)
    modules = set()
    code_lines = []
    seen_args = {}

    # file the func was defined in
    func_file = inspect.getfile(inspect.getmodule(func))

    # Check if the file is part of the tecton codebase, not the feature repo.
    # Only perform any feature repo initialization for functions in the feature repo.
    # We short-circuit any repo_file_handler functions that depend on initialization if we skip initialization here.
    if not is_tecton_defined(func_file):
        repo_file_handler.ensure_prepare_repo(func_file)

    def process_functiontype(name, obj, imports, modules, code_lines, seen_args):
        # if this is user-defined or otherwise unavailable to import at deserialization time
        # including anything without a module, with module of __main__, defined inside the feature repo
        # or anything with a qualified name containing characters invalid for an import path, like foo.<locals>.bar
        module = inspect.getfile(inspect.getmodule(obj))
        if (
            obj.__module__ in ("__main__", None)
            or "<" in obj.__qualname__
            or is_tecton_defined(module)
            or module in repo_file_handler.repo_files_set()
        ):
            objs = globalvars(obj, recurse=False)
            objs.update(freevars(obj))
            default_objs = {}
            for param in inspect.signature(obj).parameters.values():
                if param.default != inspect.Parameter.empty:
                    default_objs[param.name] = param.default
                    # these defaults shadow over obj
                    objs.pop(param.name, None)
            # need to sort the keys since globalvars ordering is non-deterministic
            for dependency, dep_obj in sorted(objs.items()):
                recurse(dependency, dep_obj, imports, modules, code_lines, seen_args, write_codelines=True)
            for dependency, dep_obj in sorted(default_objs.items()):
                # we dont re-write defaults at top-level since the `def` lines should have the declarations
                recurse(dependency, dep_obj, imports, modules, code_lines, seen_args, write_codelines=False)
            fdef = inspect.getsource(obj)
            fdef = fdef[fdef.find("def ") :]
            code_lines.append(fdef)
        else:
            imports[obj.__module__].add(obj.__name__)

    def recurse(name, obj, imports, modules, code_lines, seen_args, write_codelines):
        def _add_codeline(line):
            if write_codelines:
                code_lines.append(line)

        # prevent processing same dependency object multiple times, even if
        # multiple dependent objects exist in the tree from the original
        # func
        seen_key = str(name) + str(obj)
        if seen_args.get(seen_key) is True:
            return
        seen_args[seen_key] = True

        has_spark = True
        try:
            import pyspark  # noqa: F401
        except ImportError:
            has_spark = False

        is_spark_struct = False
        is_unbound_materialization_context = False
        is_tecton_sliding_window_udf = False
        if has_spark:
            from pyspark.sql import types as spark_types

            is_spark_struct = isinstance(obj, spark_types.StructType)
            from tecton_core.materialization_context import UnboundMaterializationContext

            is_unbound_materialization_context = isinstance(obj, UnboundMaterializationContext)

            from tecton_spark.udfs import tecton_sliding_window_udf

            is_tecton_sliding_window_udf = obj is tecton_sliding_window_udf

        # Confusingly classes are subtypes of 'type'; non-classes are not
        if isinstance(obj, type):
            if obj.__module__ == "__main__":
                msg = f"Cannot serialize class {obj.__name__} from module __main__"
                raise Exception(msg)
            imports[obj.__module__].add(obj.__name__)

        elif isinstance(obj, FunctionType):
            process_functiontype(name, obj, imports, modules, code_lines, seen_args)
        elif isinstance(obj, ModuleType):
            if obj.__name__ == "builtins":
                # builtins are always available, and inspect.getfile doesn't work on them
                return
            module_file = inspect.getfile(obj)
            # skip this check for functions written by Tecton
            if not is_tecton_defined(func_file) and module_file in repo_file_handler.repo_files_set():
                msg = f"Cannot serialize usage of {obj.__name__}. Instead, directly import objects from the module, e.g. `from {obj.__name__} import obj`"
                raise Exception(msg)
            if f"{obj.__package__}.{name}" == obj.__name__:
                imports[obj.__package__].add(name)
            else:
                modules.add(obj.__name__)
        elif is_spark_struct:
            _add_codeline(f"{name} = StructType.fromJson(json.loads('{obj.json()}'))")
            modules.add("json")
            imports["pyspark.sql.types"].add("StructType")
        elif is_unbound_materialization_context:
            imports["tecton_core.materialization_context"].add("materialization_context")
        elif is_tecton_sliding_window_udf:
            imports["tecton_spark.udfs"].add("tecton_sliding_window_udf")
        elif obj == WINDOW_UNBOUNDED_PRECEDING:
            imports["tecton_spark.time_utils"].add("WINDOW_UNBOUNDED_PRECEDING")
        else:
            try:
                repr_str = f"{name}={repr(obj)}"
                exec(repr_str)
                _add_codeline(repr_str)
            except Exception:
                msg = f"Cannot evaluate object {obj} of type '{type(obj)}' for serialization"
                raise Exception(msg)

    recurse(func.__name__, func, imports, modules, code_lines, seen_args, write_codelines=True)

    for module in sorted(imports):
        import_line = f"from {module} import "
        import_line += ", ".join(sorted(imports[module]))
        code_lines.insert(0, import_line)

    for module in sorted(modules):
        code_lines.insert(0, f"import {module}")

    return "\n".join(code_lines)


def inlined(func):
    # this a no-op that can be deleted later
    return func
