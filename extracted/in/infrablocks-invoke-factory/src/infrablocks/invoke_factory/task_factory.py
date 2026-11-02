import inspect
from collections.abc import Callable, Iterable
from typing import Any, NotRequired, TypedDict, cast

from invoke.context import Context
from invoke.tasks import Task


class Parameter(TypedDict):
    name: str
    help: NotRequired[str]
    default: NotRequired[str | int | float | bool | None]


def parameter(
    name: str, help: str = "", default: str | int | float | bool | None = None
) -> Parameter:
    return Parameter(name=name, help=help, default=default)


type ParameterList = Iterable[Parameter]
type Arguments = dict[str, str | int | float | bool]
type BodyCallable[T] = Callable[[Context, Arguments], T]


def create_task[T](
    body: BodyCallable[T], parameters: Iterable[Parameter] | None = None
) -> Task[Any]:
    parameters = parameters if parameters is not None else []
    help = {
        parameter["name"]: parameter.get("help", "")
        for parameter in parameters
    }
    task_body: BodyCallable[T] = _create_task_body(body, parameters)
    return Task(task_body, help=help)


def _create_task_body[T](
    body: BodyCallable[T], parameters: ParameterList
) -> BodyCallable[T]:
    # Construct the signature from parameters
    param_objects = [
        inspect.Parameter("context", inspect.Parameter.POSITIONAL_ONLY)
    ]
    for parameter in parameters:
        param = inspect.Parameter(
            parameter["name"],
            inspect.Parameter.KEYWORD_ONLY,
            default=parameter.get("default", None),
        )
        param_objects.append(param)

    sig = inspect.Signature(param_objects)

    def new_function(*args: Any, **kwargs: Any) -> T:
        # Bind the arguments to the parameters
        bound_args = sig.bind(*args, **kwargs)
        bound_args.apply_defaults()

        # Execute the body
        return body(args[0], kwargs)

    # Copy the signature to the new function
    setattr(new_function, "__signature__", sig)
    # Copy the name and docstring
    new_function.__name__ = body.__name__
    new_function.__doc__ = body.__doc__

    return cast(BodyCallable[T], new_function)
