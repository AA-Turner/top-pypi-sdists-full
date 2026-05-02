"""Extended Var implementations for reflex-enterprise."""

import inspect
from dataclasses import dataclass
from types import FunctionType
from typing import (
    Any,
    Callable,
    Literal,
    Mapping,
    TypeVar,
    get_args,
    get_origin,
    get_type_hints,
)

from reflex.components import dynamic
from reflex.event import EventSpec, run_script
from reflex.utils.format import format_library_name, to_camel_case
from reflex.utils.serializers import serializer
from reflex.utils.types import typehint_issubclass
from reflex.vars import LiteralVar, Var, VarData
from reflex.vars.function import ArgsFunctionOperation, FunctionVar
from reflex.vars.object import ObjectVar


class PromiseVar(Var):
    """A Var representing a JavaScript Promise."""

    def _chain(
        self, js_expr_chain: Literal["then", "catch"], callback: Var
    ) -> "PromiseVar":
        """Chain a callback to the promise.

        Args:
            js_expr_chain: The JavaScript expression to chain (then or catch).
            callback: The callback to chain.

        Returns:
            A new PromiseVar with the callback chained.
        """
        callback_var = Var.create(callback)
        return self._replace(
            _js_expr=f"{self!s}.{js_expr_chain}({callback!s})",
            merge_var_data=callback_var._get_all_var_data(),
        )

    def then(self, callback: Var) -> "PromiseVar":
        """Chain a callback to the promise.

        Args:
            callback: The callback to chain.

        Returns:
            A new PromiseVar with the callback chained.
        """
        return self._chain("then", callback)

    def catch(self, callback: Var) -> "PromiseVar":
        """Chain a callback to handle errors.

        Args:
            callback: The callback to handle errors.

        Returns:
            A new PromiseVar with the error handler chained.
        """
        return self._chain("catch", callback)


class ArgsFunctionOperationPromise(ArgsFunctionOperation):
    """A function operation that returns a PromiseVar when called.

    Used for chaining promises from python code.
    """

    def __call__(self, *args, **kwargs) -> PromiseVar:
        """Call the function with the given arguments.

        Args:
            *args: The arguments to pass to the function.
            **kwargs: The keyword arguments to pass to the function.

        Returns:
            A PromiseVar representing the result of the function call.
        """
        call_result = super().__call__(*args, **kwargs)
        return PromiseVar(
            _js_expr=call_result._js_expr,
            _var_data=call_result._get_all_var_data(),
        )


class LambdaVar(ArgsFunctionOperation, python_types=FunctionType):
    """A Var representing a JavaScript function."""


class LiteralLambdaVar(LambdaVar, LiteralVar):
    """A Var representing a python function converted to a JavaScript function."""

    @staticmethod
    def _validate_and_extend_return_expr(
        return_expr: Var, func_name: str | None = None
    ) -> Var:
        """Validate that the return expression can be used in all contexts.

        If possible, extend the return expression to gather necessary imports
        from the __reflex object using the same mechanism from (reflex.components.dynamic).

        Args:
            return_expr: The return expression to validate.
            func_name: The name of the function (for exception messages).

        Returns:
            A new Var representing the extended return expression.

        Raises:
            ValueError: If the return expression contains components that
                require custom code or dynamic imports or if when any import is
                not bundled.
        """
        local_vars = {}
        if vd := return_expr._get_all_var_data():
            if any(
                comp._get_all_custom_code() or comp._get_all_dynamic_imports()
                for comp in vd.components
            ):
                raise ValueError(
                    f"Function {func_name} cannot use components that require "
                    "custom code or dynamic imports. Try using an `@rx.memo` component. "
                    f"Got {vd.components}."
                )
            all_hooks = list(vd.hooks)
            all_hooks.extend(
                [hook for comp in vd.components for hook in comp._get_all_hooks()]
            )
            if all_hooks:
                raise ValueError(
                    f"Function {func_name} cannot use hooks in the return value. "
                    "Try using an `@rx.memo` component. "
                    f"Got {all_hooks}."
                )
            bundled_libraries = set(dynamic.bundled_libraries)
            for package, imports in vd.imports:
                normalize_package = format_library_name(package)
                if normalize_package not in bundled_libraries:
                    raise ValueError(
                        f"Library {normalize_package} is not bundled. "
                        "Use `from reflex.components.dynamic import bundle_library; "
                        f"bundle_library({normalize_package!r}) to enable it it."
                    )
                for iv in imports:
                    if (alias := (iv.alias or iv.tag)) not in local_vars:
                        local_vars[alias] = (
                            f"const {alias} = __reflex['{normalize_package}']?.{iv.tag};"
                        )
        if local_vars:
            const_exprs = "\n".join(local_vars.values())
            return Var(f"{{\n{const_exprs}\nreturn {return_expr}\n}}")
        return return_expr

    @classmethod
    def create(
        cls,
        func: Callable,
        _var_data: VarData | None = None,
    ) -> "LiteralLambdaVar":
        """Create a LiteralLambdaVar from a function."""
        if (
            (_as_var := getattr(func, "_as_var", None)) is not None
            and callable(_as_var)
            and isinstance((potential_var := _as_var()), Var)
        ):
            return potential_var  # pyright: ignore[reportReturnType]
        sig = inspect.signature(func)
        hints = get_type_hints(func)
        params = []
        for param in sig.parameters.values():
            if param.kind in {param.VAR_POSITIONAL, param.VAR_KEYWORD}:
                raise TypeError(
                    f"Function {func.__name__} cannot have *args or **kwargs parameters: {param}"
                )
            if (
                annotation := hints.get(param.name, param.annotation)  # type: ignore[assignment]
            ) != param.empty and not typehint_issubclass(annotation, Var):
                raise TypeError(
                    f"All parameters of {func.__name__} must be annotated as rx.Var[...], got {annotation}"
                )
            var_cls = (
                (Var if annotation is param.empty else annotation)
                if (annotation_origin := get_origin(annotation)) is None
                else annotation_origin
            )
            if annotation == param.empty or not (
                annotation_args := get_args(annotation)
            ):
                # Assume arbitrary attributes two layers deep
                annotation = dict[str, dict[str, Any]]
            else:
                annotation = annotation_args[0]
            param_var = var_cls(param.name, _var_type=annotation)
            if var_cls is Var:
                # Extra guessing for plain Var.
                param_var = param_var.guess_type()
            params.append(param_var)
        try:
            func_return = func(*params)
        except Exception as exc:
            raise ValueError(
                f"Function {func.__name__} could not be evaluated at compile time. "
                "When constructing the return value, make to only use Var operations, cond, and foreach."
            ) from exc

        try:
            return_expr = Var.create(func_return)
        except Exception as exc:
            raise ValueError(
                f"Function {func.__name__} must return a Var-able value, got {type(func_return)}"
            ) from exc

        if not is_static(func):
            # If the function is not static, we need to add the imports to the return expression.
            # This is because the function will be called at runtime and we need to ensure that
            # all imports are available if possible.
            return_expr = cls._validate_and_extend_return_expr(
                return_expr=return_expr,
                func_name=func.__name__,
            )

        return super().create(
            args_names=tuple(sig.parameters),
            return_expr=return_expr,
            _var_data=_var_data,
        )


@serializer
def serialize_lambda_var(lambda_var: LambdaVar) -> dict[str, Any]:
    """Serialize a LambdaVar to a var dict.

    Args:
        lambda_var: The LambdaVar to serialize.

    Returns:
        A LiteralLambdaVar dict representing the serialized function.
    """
    lv_dict = {k: getattr(lambda_var, k) for k in ["_js_expr", "_var_type"]}
    # Include VarData if present.
    lv_var_data = lambda_var._get_all_var_data()
    if lv_var_data:
        lv_dict["_var_data"] = lv_var_data
    return lv_dict


@serializer
def serialize_lambda(func: FunctionType) -> dict[str, Any]:
    """Serialize a lambda function to a LiteralLambdaVar dict.

    Args:
        func: The function to serialize.

    Returns:
        A LiteralLambdaVar dict representing the serialized function.
    """
    return serialize_lambda_var(LiteralLambdaVar.create(func))


T = TypeVar("T")


def static(obj: T) -> T:
    """Mark the object as `__rxe_static__` which means it cannot be used at runtime in a State class.

    Args:
        obj: The object to mark as static.
    """
    object.__setattr__(obj, "__rxe_static__", True)
    return obj


def is_static(obj: Any) -> bool:
    """Check if the object is marked as `__rxe_static__`.

    Args:
        obj: The object to check.

    Returns:
        True if the object is marked as static, False otherwise.
    """
    return getattr(obj, "__rxe_static__", False)


JS_API_TYPE = Mapping[str, Callable]


class JSAPIVar(ObjectVar[JS_API_TYPE]):
    """A generic wrapper for JavaScript API objects represented in JS.

    This class provides common functionality for mapping Python snake_case
    method names to JavaScript camelCase function names, which is useful
    for wrapping JavaScript APIs like Leaflet Map or AG Grid.
    """

    def __post_init__(self) -> None:
        """Post-initialization hook to set the JS expression."""
        if self._var_type is Any:
            # Assign a default type if not provided.
            self.__init__(
                self._js_expr,
                _var_type=JS_API_TYPE,
                _var_data=self._var_data,
            )

    def __getattr__(self, name: str) -> FunctionVar:
        """Get a callable JS FunctionVar for a given API function.

        Args:
            name: The method name in snake_case format.

        Returns:
            A FunctionVar that represents the JavaScript API method.
        """
        return super().__getattr__(to_camel_case(name)).to(FunctionVar)


@dataclass
class PassthroughAPI:
    """Abstract wrapper for defining a Reflex API that passthroughs any calls to the JS API.

    Inheriting classes should implement the `_api` property to define the JS API object.
    """

    @property
    def _api(self) -> JSAPIVar:
        """Get the JavaScript API object."""
        raise NotImplementedError

    def __getattr__(self, name: str) -> Callable[..., EventSpec]:
        """Get a callable JS FunctionVar for a given API function."""

        def _call_api(*args, **kwargs):
            """Call the API function with the given arguments.

            Args:
                *args: The arguments to pass to the API function.
                **kwargs: Additional keyword arguments to pass to run_script.

            Returns:
                An EventSpec that runs the API function in JavaScript.
            """
            return run_script(
                getattr(self._api, name)(*args),
                **kwargs,
            )

        return _call_api


@dataclass
class ElementAPI(PassthroughAPI):
    """Wrapper for DOM element API methods."""

    element_id: str

    @property
    def _api(self) -> JSAPIVar:
        """Get the JavaScript API object."""
        return JSAPIVar(f"document.getElementById('{self.element_id}')")
