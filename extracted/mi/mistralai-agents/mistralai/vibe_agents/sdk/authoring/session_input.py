"""Session input authoring for dependency injection into tools, hooks and sandbox hooks.

A Session input is an immutable, caller-supplied value fixed for the lifetime
of one Session. Tools, hooks and sandbox hooks declare the inputs they need
with ``Annotated[T, agents.Depends()]``. Each declared value reaches its
consumer as a keyword argument, never through the model's context.
"""

import copy
import functools
import inspect
import sys
from collections.abc import Callable, Mapping
from types import MappingProxyType, UnionType
from typing import Annotated, Any, ClassVar, ForwardRef, Never, Union, cast, get_args, get_origin

from pydantic import BaseModel, ConfigDict, JsonValue, ValidationError

from .errors import SdkError

if sys.version_info >= (3, 14):
    import annotationlib

_MAX_DESCRIBED_ERRORS = 3
_MAX_DESCRIBED_ERROR_CHARS = 200


class SessionInput(BaseModel):
    """A value you pass when you start a session, which tools and hooks can read.

    Subclass it with the fields you need, such as a repository or an organization, and set
    ``input_id``. A tool, a hook or a sandbox hook reads it with a parameter annotated
    ``Annotated[YourInput, agents.Depends()]``; the model never sees it. Never put a credential in
    it: the session keeps it for its whole lifetime.

    A rule that only a validator expresses is checked where the value is used, and a rejected value
    fails that use. Never put the value in a validator's message, since the message reaches turn
    results and the model.

    A session keeps its inputs for its whole lifetime, across new deployments of the agent, so a
    change to a class must keep accepting the values its previous version accepted.
    """

    # pydantic's own validation errors then omit the supplied value.
    model_config = ConfigDict(frozen=True, hide_input_in_errors=True)

    input_id: ClassVar[str] = ""
    """The input's stable name, which a session uses to find it. It is not part of the value."""


class Depends:
    """Mark an ``Annotated`` parameter as a session input: ``Annotated[T, agents.Depends()]``.

    The annotated type ``T`` is the input class, declared once.
    """

    __slots__ = ()

    def __init__(self, *args: Never, **kwargs: Never) -> None:
        # ``Never`` lets type checkers flag ``agents.Depends(X)`` in ordinary code. Inside
        # ``Annotated[...]`` metadata they may not, so this error shows the fix when the
        # declaration is evaluated.
        if args or kwargs:
            raise SdkError(
                "agents.Depends() takes no arguments; declare the input type in the annotation: "
                "Annotated[RepositoryContext, agents.Depends()]"
            )

    def __repr__(self) -> str:
        return "agents.Depends()"


def require_input_id(input_class: type[SessionInput]) -> str:
    """Return the class's stable input ID, rejecting unusable declarations."""

    input_id = input_class.input_id
    if not isinstance(input_id, str) or not input_id.strip():
        raise ValueError(f"Session input class {input_class.__qualname__} must declare a non-empty input_id")
    return input_id


def required_input_ids(declarations: Mapping[str, type[SessionInput]]) -> list[str]:
    """Return the input IDs a consumer declares, in order, once each.

    Two parameters may declare the same input class; the consumer still requires it once.
    """

    return list(dict.fromkeys(require_input_id(input_class) for input_class in declarations.values()))


def session_input_schemas(
    input_classes: Mapping[str, type[SessionInput]],
) -> dict[str, dict[str, JsonValue]]:
    """Map each input ID to the JSON Schema of the value a caller must supply.

    The caller's JSON is checked with ``model_validate``, so the schema describes
    the validation shape. A model that tolerates extra fields keeps tolerating them.
    """

    return {
        input_id: cast(dict[str, JsonValue], input_class.model_json_schema(mode="validation"))
        for input_id, input_class in sorted(input_classes.items())
    }


def method_session_inputs[C](contract: type[C], owner: C, point: str) -> Mapping[str, type[SessionInput]]:
    """Map each Depends-annotated parameter of ``owner``'s ``point`` method to its input class.

    The caller passes the arguments that ``contract``'s ``point`` method declares by
    position, and the Session inputs by keyword. A Session input parameter in one of
    those positions is rejected here instead of failing when the method is called.
    """

    contract_method = inspect.getattr_static(contract, point)
    declarations, misplaced = _method_session_inputs(inspect.getattr_static(type(owner), point), contract_method)
    if misplaced is not None:
        # Names the class the author registered, even for an inherited method.
        raise SdkError(
            f"{type(owner).__name__}.{point} parameter {misplaced!r} declares a Session input "
            f"in a position the caller fills; declare it after the first "
            f"{_caller_filled_count(contract_method)} parameter(s) of {contract.__name__}.{point}, "
            "for example as keyword-only"
        )
    return declarations


@functools.cache
def _method_session_inputs(
    attribute: object,
    contract_method: Callable[..., Any],
) -> tuple[Mapping[str, type[SessionInput]], str | None]:
    """Return a method's declarations and the first one in a caller-filled position, if any.

    Keyed by the class attributes, so hooks called on every turn skip signature
    inspection and annotation evaluation, and no hook instance is kept alive. The
    declarations are read-only because every caller shares them.
    """

    function, offset = _unwrap_method(attribute)
    declarations = MappingProxyType(session_input_parameters_of(function))
    if not declarations:
        return declarations, None
    caller_filled = _caller_filled_count(contract_method)
    for parameter in _positional_parameters(function)[offset : offset + caller_filled]:
        if parameter.name in declarations:
            return declarations, parameter.name
    return declarations, None


def _unwrap_method(attribute: object) -> tuple[Callable[..., Any], int]:
    """Return the function behind a class attribute and how many leading slots Python binds.

    An instance call binds ``self`` for a plain method and ``cls`` for a classmethod,
    and nothing for a staticmethod.
    """

    if isinstance(attribute, staticmethod):
        return attribute.__func__, 0
    if isinstance(attribute, classmethod):
        return attribute.__func__, 1
    return cast(Callable[..., Any], attribute), 1


def _caller_filled_count(contract_method: Callable[..., Any]) -> int:
    """Count the arguments a caller passes by position: the contract's, after ``self``."""

    return len(_positional_parameters(contract_method)) - 1


def _positional_parameters(function: Callable[..., Any]) -> list[inspect.Parameter]:
    return [
        parameter
        for parameter in read_signature(function).parameters.values()
        if parameter.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)
    ]


def read_signature(function: Callable[..., Any]) -> inspect.Signature:
    # Python 3.14 evaluates annotations when the signature is read. An annotation that
    # cannot resolve, such as a TYPE_CHECKING-only name, stays a ForwardRef instead of failing.
    if sys.version_info >= (3, 14):
        return inspect.signature(function, annotation_format=annotationlib.Format.FORWARDREF)
    return inspect.signature(function)


def session_input_parameters_of(function: Callable[..., Any]) -> dict[str, type[SessionInput]]:
    """Map each Depends-annotated parameter name to its input class.

    A ``Depends`` marker that cannot be honored raises ``SdkError`` instead of
    being skipped, so a declaration is never silently dropped.
    """

    signature = read_signature(function)
    declarations: dict[str, type[SessionInput]] = {}
    for name, parameter in signature.parameters.items():
        label = f"{getattr(function, '__qualname__', function)!s} parameter {name!r}"
        annotation = _resolve_annotation(function, name, parameter.annotation)
        if get_origin(annotation) in (Union, UnionType) and any(
            _declares_session_input(label, arm) for arm in get_args(annotation)
        ):
            raise SdkError(f"{label} declares a Session input inside a union; use Annotated[T, agents.Depends()]")
        if not _declares_session_input(label, annotation):
            continue
        if parameter.kind not in (inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY):
            raise SdkError(f"{label} declares a Session input but cannot be passed by keyword")
        declarations[name] = _declared_input_class(label, get_args(annotation)[0])
    return declarations


def _declares_session_input(label: str, annotation: Any) -> bool:
    """Whether an ``Annotated`` type carries the ``Depends`` marker."""

    if get_origin(annotation) is not Annotated:
        return False
    _base_type, *metadata = get_args(annotation)
    if any(item is Depends for item in metadata):
        raise SdkError(f"{label} uses agents.Depends without parentheses; use Annotated[T, agents.Depends()]")
    for item in metadata:
        # Python 3.14 keeps a marker it cannot resolve, such as a TYPE_CHECKING-only import, as a
        # ForwardRef. Depends takes no arguments, so a real marker always ends with "Depends()".
        if isinstance(item, ForwardRef) and item.__forward_arg__.endswith("Depends()"):
            raise SdkError(
                f"{label} declares a Session input whose marker {item.__forward_arg__!r} cannot be resolved; "
                "import agents.Depends at runtime, not under TYPE_CHECKING"
            )
    return any(isinstance(item, Depends) for item in metadata)


def _declared_input_class(label: str, base_type: Any) -> type[SessionInput]:
    """Return the annotated input class, rejecting one that is not a SessionInput."""

    if not (isinstance(base_type, type) and issubclass(base_type, SessionInput)):
        raise SdkError(
            f"{label} depends on {getattr(base_type, '__qualname__', base_type)!s}, "
            "which is not an agents.SessionInput subclass"
        )
    return base_type


def evaluate_annotation(function: Callable[..., Any], annotation: Any) -> Any:
    """Evaluate one postponed annotation in the namespace of the module that defines ``function``.

    A wrapped function is unwrapped first, so its annotations resolve in the author's module, not
    the decorator's. A non-string annotation is returned as is. The evaluation error propagates:
    each caller decides what an annotation that cannot resolve means for it.
    """

    annotation = _annotation_source(annotation)
    if not isinstance(annotation, str):
        return annotation
    namespace = dict(getattr(inspect.unwrap(function), "__globals__", {}))
    # The same evaluation inspect.get_annotations(eval_str=True) performs, scoped
    # to one annotation the author wrote in this module.
    return eval(annotation, namespace)  # noqa: S307


def _annotation_source(annotation: Any) -> Any:
    # On Python 3.14, an annotation that failed lazy evaluation arrives as a ForwardRef holding its string.
    return annotation.__forward_arg__ if isinstance(annotation, ForwardRef) else annotation


def _resolve_annotation(function: Callable[..., Any], parameter_name: str, annotation: Any) -> Any:
    """Evaluate one postponed (string) annotation in the callable's module namespace.

    Under ``from __future__ import annotations`` every annotation is a string, so a
    ``Depends`` marker is only visible once evaluated. On Python 3.14, an annotation
    that failed lazy evaluation arrives as a ``ForwardRef`` holding that string.
    Each annotation is evaluated on its own: an unrelated one that cannot resolve
    (a ``TYPE_CHECKING``-only import) must not hide the parameters that can. A
    ``Depends`` annotation that cannot resolve is rejected, so a declaration is
    never silently dropped.
    """

    try:
        return evaluate_annotation(function, annotation)
    except SdkError:
        # Raised by the declaration itself, such as agents.Depends(X): its message shows the fix.
        raise
    except Exception as error:
        source = _annotation_source(annotation)
        if "Depends" not in source:
            return inspect.Parameter.empty
        raise SdkError(
            f"{getattr(function, '__qualname__', function)!s} parameter {parameter_name!r} declares a "
            f"Session input whose annotation {source!r} cannot be resolved at module scope: {error}"
        ) from error


def rebuild_session_inputs(
    consumer: str,
    declarations: Mapping[str, type[SessionInput]],
    injected: Mapping[str, Any] | None,
) -> dict[str, Any]:
    """Rebuild typed Session input objects from their delivered JSON values.

    ``consumer`` names the tool, hook or sandbox hook in the ``ValueError`` raised when a
    declared input is missing from ``injected`` or does not rebuild into its class. The
    SDK also calls this to check a caller's inputs for sandbox hooks before the sandbox
    is provisioned.
    """

    if not declarations:
        return {}
    values = injected or {}
    rebuilt: dict[str, Any] = {}
    for parameter_name, input_class in declarations.items():
        input_id = require_input_id(input_class)
        if input_id not in values:
            raise ValueError(f"{consumer} declares Session input {input_id!r} that was not delivered")
        try:
            # A copy of each declared value: pydantic passes nested containers through, and a
            # validator or the consumer could otherwise mutate the inputs other consumers receive.
            rebuilt[parameter_name] = input_class.model_validate(copy.deepcopy(values[input_id]))
        except ValidationError as error:
            raise ValueError(f"{consumer} cannot use Session input {input_id!r}: {_describe(error)}") from error
        except Exception as error:
            # pydantic re-raises any validator exception other than ValueError or AssertionError: a
            # bug in the class, outside the rule that keeps values out of messages. Only its type is
            # reported, and the cause is dropped so logs and Workflow history do not keep its text.
            raise ValueError(
                f"{consumer} cannot use Session input {input_id!r}: its class raised {type(error).__name__}"
            ) from None
    return rebuilt


def _describe(error: ValidationError) -> str:
    """Lay the errors out as pydantic does, without its documentation link.

    The text reaches Turn results, tool results the model reads, and Session results, which
    have size limits, so the number of errors and each path and message are bounded. A path
    can hold a dict key of any length.
    """

    details = error.errors(include_url=False, include_context=False, include_input=False)
    count = len(details)
    lines = [f"{count} validation error" if count == 1 else f"{count} validation errors"]
    for detail in details[:_MAX_DESCRIBED_ERRORS]:
        lines.append(_bounded(".".join(str(part) for part in detail["loc"]) or "value"))
        lines.append(f"  {_bounded(detail['msg'])} [type={detail['type']}]")
    if count > _MAX_DESCRIBED_ERRORS:
        lines.append(f"and {count - _MAX_DESCRIBED_ERRORS} more")
    return "\n".join(lines)


def _bounded(message: str) -> str:
    if len(message) <= _MAX_DESCRIBED_ERROR_CHARS:
        return message
    return f"{message[:_MAX_DESCRIBED_ERROR_CHARS]}..."


__all__ = [
    "Depends",
    "SessionInput",
    "method_session_inputs",
    "read_signature",
    "rebuild_session_inputs",
    "require_input_id",
    "required_input_ids",
    "session_input_parameters_of",
]
