import sys
from typing import Any
from typing import Callable
from typing import Dict
from typing import Optional

from tecton_core import materialization_context
from tecton_core.errors import TectonValidationError
from tecton_proto.args.user_defined_function__client_pb2 import UserDefinedFunction


# TODO(deprecated_after=0.5): handle backward-compatibility for builtin transformations that did not use tecton.materialization_context
# but instead directly accessed tecton_spark.materialization_context
sys.modules["tecton_spark.materialization_context"] = materialization_context


def _from_proto(
    serialized_transform: UserDefinedFunction,
    globals_: Optional[Dict[str, Any]] = None,
    locals_: Optional[Dict[str, Any]] = None,
) -> Callable:
    """
    deserialize into the provided scope, by default we deserialize the functions into their own scopes
    """

    if globals_ is None:
        globals_ = {}

    assert serialized_transform.HasField("body") and serialized_transform.HasField("name"), (
        "Invalid UserDefinedFunction."
    )

    try:
        exec(serialized_transform.body, globals_, locals_)
    except NameError as e:
        msg = "Failed to serialize function. Please note that all imports must be in the body of the function (not top-level) and type annotations cannot require imports. Additionally, be cautious of variables that shadow other variables. See https://docs.tecton.ai/docs/defining-features/feature-views/transformations for more details."
        raise TectonValidationError(
            msg,
            e,
        )

    # Return function pointer
    try:
        fn = eval(serialized_transform.name, globals_, locals_)
        fn._code = serialized_transform.body
        return fn
    except Exception as e:
        msg = "Invalid transform"
        raise ValueError(msg) from e


def _from_proto_pollute_main(serialized_transform: UserDefinedFunction) -> Callable:
    """Deserialize transform using main scope

    This version of function deserialization to __main__.__dict__. This has historically been the behavior of function
    deserialization. Generally this should be avoided since it can cause hard to debug issues, e.g. two helper functions
    of the same name can shadow each other, or allows for users to depend on libraries that they did not import themselves.
    """
    main_scope = __import__("__main__").__dict__
    # deserialize directly to main and modifies that namespace for all future functions :(
    return _from_proto(serialized_transform, globals_=main_scope)


def _from_proto_isolate(serialized_transform: UserDefinedFunction) -> Callable:
    """Deserialize transform with isolated context, but keep access to `spark` and `sc`.

    This version of function deserialization allows user to have access to the `spark` and `sc` variables from __main__
    scope if they exist, but also isolates functions from each other. The "spark" (SparkSession) and "sc" (SparkContext)
    variables are provided by default in shell environments and DataBricks Notebooks, so users may be relying on them.
    This version ensures these variables are still available without deserializing the function _into_ the main context.
    """
    deserialization_globals = {}
    main_scope = __import__("__main__").__dict__
    for var in ["spark", "sc"]:
        if var in main_scope:
            deserialization_globals[var] = main_scope.get(var)

    return _from_proto(serialized_transform, globals_=deserialization_globals)


def _from_proto_empty_globals(serialized_transform: UserDefinedFunction) -> Callable:
    """Deserialize transform with an empty globals

    Do not deserialize the function into __main__ context (good), do not import other random additional things into
    but also means users may lose access to any variables from __main__ they might have been relying on.
    """
    return _from_proto(serialized_transform, globals_={})


def from_proto(serialized_transform: UserDefinedFunction, include_main_variable_in_scope: bool = False) -> Callable:
    """Takes in a Serialized function and converts it into a python function.

    :param serialized_transform: A UserDefinedFunction proto object with the serialized function and additional config
    :param include_main_variable_in_scope: Whether to deserialize with globals 'empty', or ensure that certain variables
        such as 'spark' or 'sc' are passed in from the global context. This differs depending on if you are using
        materialization, local, etc.
    :return: The deserialized python function
    """
    flag_value = serialized_transform.isolate_function_deserialization
    if include_main_variable_in_scope and flag_value:
        deserialized_function = _from_proto_isolate(serialized_transform)
    elif include_main_variable_in_scope:
        deserialized_function = _from_proto_pollute_main(serialized_transform)
    else:
        deserialized_function = _from_proto_empty_globals(serialized_transform)

    return deserialized_function
