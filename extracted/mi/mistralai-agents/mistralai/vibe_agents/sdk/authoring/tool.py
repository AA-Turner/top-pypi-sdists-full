"""
Unified Agents SDK tool authoring.

- PythonTool: a Python function on the worker with the ToolDefinition the model sees, with explicit
  model access. It stays callable like the function.
- tool: public decorator that constructs PythonTool.
- client_tool: public decorator that declares a ClientTool, a tool the application running the
  agent answers. Its internal declaration is a ClientToolDefinition.

A tool built from a plain function needs no input model: its name defaults to
the function name, its description to the docstring, its input schema to a
model built from the parameters, and its output schema to the return
annotation's. Per-argument descriptions come from
``Annotated[T, Field(description=...)]``.

ClientToolDefinition inherits the retained Vibe SDK wrapper so Nuage adapters
can consume it during migration. Its public API and Unified-specific access
policy are owned here by the Agents SDK.

A tool that needs its run context takes an ``agents.ToolCallbackContext`` as its first,
positional-only parameter, found by its type: the worker fills it for each call, with the
Session, its sandbox and the call's ID.

Tools may declare Session inputs with parameters annotated
``Annotated[T, agents.Depends()]``: the declared IDs compile into the
Harness ``requiredSessionInputIds`` field, the parameters never appear in
the model-visible schema, and the executor rebuilds each object from the
Harness-selected ``injectedSessionInputs`` at invocation time.
"""

import asyncio
import collections.abc
import contextvars
import functools
import inspect
import logging
import re
import warnings
import weakref
from collections.abc import Awaitable, Callable
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any, Concatenate, Protocol, cast, get_args, get_origin, overload

from pydantic import BaseModel, JsonValue, TypeAdapter, create_model

from mistralai.vibe.harness.app_server.session import ToolModelAccess
from mistralai.vibe.sdk.agent.tasks.core import Card, TaskCallback
from mistralai.vibe.sdk.capabilities import authoring as legacy_authoring
from mistralai.vibe.sdk.capabilities.types import ToolHandler
from mistralai.vibe.sdk.capabilities.types import ToolResult as AnnotatedToolResult

# `contracts` imports this module first, so its names are read when a tool is built, not at import.
from . import contracts, session_input
from .errors import SdkError
from .keep_open import KeepCallbackOpen
from .tool_definition import ToolAnnotations, ToolDefinition
from .tool_errors import ToolCodeError, ToolFunctionError, call_is_cancelling
from .tool_result import ToolResult, is_rich_tool_result, is_rich_tool_result_type

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from typing_extensions import TypeIs

    from mistralai.vibe_agents.sdk.client.records import OpenCallback, OpenClientToolCall

    from .contracts import ToolCallbackContext

# Threads the rebuilt Session input objects through to the handler, past the argument validation.
_session_inputs_context: contextvars.ContextVar[dict[str, Any]] = contextvars.ContextVar(
    "_session_inputs_context", default={}
)

_TOOL_MODEL_ACCESS_ADAPTER = TypeAdapter(ToolModelAccess)

logger = logging.getLogger(__name__)

# The tool each plain function listed in `tools=` became. A tool built twice from one function would
# have two generated input models, which a tree cannot share one binding between.
_PLAIN_FUNCTION_TOOLS: "weakref.WeakKeyDictionary[Callable[..., Any], PythonTool[..., Any]]" = (
    weakref.WeakKeyDictionary()
)

# A synchronous handler holds its thread for the whole call, up to the tool timeout. Tools get their own
# threads so they cannot starve the loop's default executor, which asyncio also uses for DNS lookups.
# The size matches the worker's default activity concurrency, so an accepted call never waits for one.
_TOOL_THREADS = ThreadPoolExecutor(max_workers=100, thread_name_prefix="agents-sdk-tool")


async def call_handler(handler: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
    """Await an async handler on the loop; call a synchronous one in a tool thread.

    A synchronous handler on the loop would block it for its whole run: the worker could send no
    heartbeat and serve no other Session. Only the call leaves the loop: an awaitable it returns may
    belong to the caller's loop, so it is awaited there.
    """

    if inspect.iscoroutinefunction(handler):
        return await handler(*args, **kwargs)
    context = contextvars.copy_context()
    call = functools.partial(context.run, handler, *args, **kwargs)
    result = await asyncio.get_running_loop().run_in_executor(_TOOL_THREADS, call)
    if inspect.isawaitable(result):
        result = await result
    return result


def _validate_model_access(model_access: object) -> ToolModelAccess:
    return _TOOL_MODEL_ACCESS_ADAPTER.validate_python(model_access)


DEFAULT_TOOL_NAMESPACE = "client"
"""The namespace of a tool that names none: its ID is ``client.<name>``."""

# A namespace is a property name in `run_typescript` (`tools.<namespace>.<name>(...)`), so the
# Harness core takes only TypeScript identifiers.
_NAMESPACE_PATTERN = re.compile(r"[A-Za-z_$][A-Za-z0-9_$]*")
# The groups of the Harness's built-in tools (core RESERVED_TOOL_NAMESPACES, plus the deprecated
# subagent group). The core refuses them too, but only once a Session starts.
_CORE_NAMESPACES = frozenset({"self", "file_system", "skill", "process", "agents", "subagent"})
# The groups the SDK fills itself: connector tools and guardrail hooks.
_SDK_NAMESPACES = frozenset({"connectors", "guardrail"})
_SDK_NAMESPACE_PREFIX = "connector_"


def is_reserved_namespace(namespace: str) -> bool:
    """Whether the Harness's built-in tools or the SDK's connector and guardrail tools hold ``namespace``."""

    return namespace in _CORE_NAMESPACES or namespace in _SDK_NAMESPACES or namespace.startswith(_SDK_NAMESPACE_PREFIX)


def _checked_namespace(namespace: object, tool: str) -> str:
    """``namespace`` if a tool can take it, else an ``SdkError`` that says why."""

    if not isinstance(namespace, str) or not _NAMESPACE_PATTERN.fullmatch(namespace):
        raise SdkError(
            f"Tool {tool!r}: namespace {namespace!r} must be an identifier: letters, digits, _ and $, "
            "not starting with a digit, as in namespace='billing'"
        )
    if namespace in _CORE_NAMESPACES:
        raise SdkError(f"Tool {tool!r}: namespace {namespace!r} holds the Harness's built-in tools; choose another")
    if namespace in _SDK_NAMESPACES or namespace.startswith(_SDK_NAMESPACE_PREFIX):
        raise SdkError(
            f"Tool {tool!r}: namespace {namespace!r} holds the SDK's connector and guardrail tools; choose another"
        )
    return namespace


_KEYWORD_PASSABLE_PARAMETER_KINDS = {inspect.Parameter.POSITIONAL_OR_KEYWORD, inspect.Parameter.KEYWORD_ONLY}


def _validate_handler_signature(handler: Callable[..., Any], *, context_parameter: str | None) -> None:
    signature = inspect.signature(handler)
    expected_names = {"args"} if context_parameter is None else {context_parameter, "args"}
    if set(signature.parameters) != expected_names:
        expected_list = ", ".join(sorted(expected_names))
        raise ValueError(f"Tool handlers must accept exactly these named parameters: {expected_list}")
    if signature.parameters["args"].kind not in _KEYWORD_PASSABLE_PARAMETER_KINDS:
        raise ValueError("Tool handler parameter 'args' must be passable by keyword")


def _callback_context_type(handler: Callable[..., Any], annotation: Any) -> type | None:
    """The callback context class a parameter is annotated with, or None for any other annotation."""

    if annotation is inspect.Parameter.empty:
        return None
    try:
        resolved = session_input.evaluate_annotation(handler, annotation)
    except Exception:  # noqa: BLE001 - a tool argument's annotation that cannot resolve fails where it is read
        return None
    if isinstance(resolved, type) and issubclass(
        resolved, (contracts.CallbackContext, contracts.SandboxCallbackContext)
    ):
        return resolved
    return None


def _context_parameter(handler: Callable[..., Any]) -> str | None:
    """The name of the handler's ``ToolCallbackContext`` parameter, or None when it takes none.

    The context is found by its type, so any name works. It must come first and be positional-only:
    it is never a model argument, and a model argument can never take its place. A parameter typed
    with another callback context (``CallbackContext``, ``HookCallbackContext``...) raises, rather than
    silently becoming a plain argument, and so does a subclass of ``ToolCallbackContext``, which the
    worker never builds.
    """

    found: str | None = None
    for index, (name, parameter) in enumerate(session_input.read_signature(handler).parameters.items()):
        context_type = _callback_context_type(handler, parameter.annotation)
        if context_type is None:
            continue
        if not issubclass(context_type, contracts.ToolCallbackContext):
            raise SdkError(
                f"Tool {getattr(handler, '__qualname__', handler)!s} parameter {name!r} is an "
                f"agents.{context_type.__name__}, which a tool never gets: a tool's context is an "
                f"agents.ToolCallbackContext. def {getattr(handler, '__name__', 'tool')}"
                f"({name}: agents.ToolCallbackContext, /, ...)"
            )
        if context_type is not contracts.ToolCallbackContext:
            raise SdkError(
                f"Tool {getattr(handler, '__qualname__', handler)!s} parameter {name!r} is a "
                f"{context_type.__name__}, a subclass of agents.ToolCallbackContext, which a tool never "
                "gets: the worker passes an agents.ToolCallbackContext. "
                f"def {getattr(handler, '__name__', 'tool')}({name}: agents.ToolCallbackContext, /, ...)"
            )
        if index != 0 or parameter.kind is not inspect.Parameter.POSITIONAL_ONLY:
            raise SdkError(
                f"Tool {getattr(handler, '__qualname__', handler)!s} parameter {name!r} is an "
                "agents.ToolCallbackContext, which must be the first parameter and positional-only: "
                f"def {getattr(handler, '__name__', 'tool')}({name}: agents.ToolCallbackContext, /, ...)"
            )
        found = name
    return found


def resolved_model_access(
    tool: "PythonTool[..., Any] | ClientToolDefinition[Any]", *, programmatic: bool
) -> ToolModelAccess:
    """The model access a tool compiles to for an agent with or without programmatic tool calling.

    A tool that left ``model_access`` unset is callable from programs when the agent has
    programmatic tool calling, and is a direct tool when it does not. An explicit value is kept,
    so the Harness rejects an explicit ``"programmatic"`` on an agent without the feature.
    """

    if tool.model_access_is_default and not programmatic:
        return "direct"
    return tool.model_access


def _wrap_session_input_handler(
    handler: Callable[..., Any],
    session_input_parameters: dict[str, type[session_input.SessionInput]],
) -> Callable[..., Any]:
    """Present Depends-annotated parameters behind the (args, ...) handler shape.

    A tool checks that its handler accepts exactly ``args`` (after its context, when it takes
    one). Session inputs live outside that rule: this
    wrapper shows the authored signature without its Depends parameters, so the
    check still applies to the rest of it, while forwarding every rebuilt input
    object under its declared parameter name.
    """

    def wrapped(*args: Any, **kwargs: Any) -> Any:
        return handler(*args, **_session_inputs_context.get(), **kwargs)

    # The tool derives its module-scope check, name and docstring from these
    # attributes, so they must describe the authored handler.
    for attribute in ("__module__", "__name__", "__qualname__", "__doc__"):
        if hasattr(handler, attribute):
            setattr(wrapped, attribute, getattr(handler, attribute))
    # The signature check inspects the visible signature; present the authored
    # parameters it governs while the wrapper itself forwards everything given.
    signature = session_input.read_signature(handler)
    wrapped.__signature__ = signature.replace(  # type: ignore[attr-defined]
        parameters=[
            parameter for name, parameter in signature.parameters.items() if name not in session_input_parameters
        ]
    )
    return wrapped


def _resolve_parameter_annotation(handler: Callable[..., Any], label: str, annotation: Any) -> Any:
    try:
        return session_input.evaluate_annotation(handler, annotation)
    except Exception as error:
        raise SdkError(f"{label} has annotation {annotation!r} that cannot be resolved at module scope") from error


def _input_model_name(handler: Callable[..., Any]) -> str:
    return "".join(part[:1].upper() + part[1:] for part in handler.__name__.split("_") if part) + "Args"


def _plain_function_tool(
    handler: Callable[..., Any],
    *,
    context_parameter: str | None,
) -> tuple[type[BaseModel], Callable[..., Any]]:
    """Build the input model of a plain-function tool and adapt its handler to the ``(args, ...)`` shape.

    Each parameter becomes a model field, except Session inputs and the tool's context. The model
    depends only on the signature, so a worker that re-imports the tool by module path rebuilds the
    same schema.
    """

    signature = session_input.read_signature(handler)
    session_input_parameters = session_input.session_input_parameters_of(handler)
    qualname = getattr(handler, "__qualname__", handler)
    fields: dict[str, Any] = {}
    context: list[inspect.Parameter] = []
    forwarded: list[inspect.Parameter] = []
    for name, parameter in signature.parameters.items():
        label = f"Tool {qualname!s} parameter {name!r}"
        if name == context_parameter:
            context.append(parameter)
            continue
        if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
            raise SdkError(f"{label}: *{name} cannot become a tool argument; declare each argument by name")
        if parameter.kind is inspect.Parameter.VAR_KEYWORD:
            raise SdkError(f"{label}: **{name} cannot become a tool argument; declare each argument by name")
        if parameter.kind is inspect.Parameter.POSITIONAL_ONLY:
            raise SdkError(
                f"{label} is positional-only; tool arguments are passed by keyword, and only a first "
                "agents.ToolCallbackContext parameter is positional-only"
            )
        if name in session_input_parameters:
            annotation = _resolve_parameter_annotation(handler, label, parameter.annotation)
            forwarded.append(parameter.replace(kind=inspect.Parameter.KEYWORD_ONLY, annotation=annotation))
            continue
        if parameter.annotation is inspect.Parameter.empty:
            raise SdkError(f"{label} has no type annotation; annotate it so the model knows what to pass")
        if name.startswith("_"):
            raise SdkError(f"{label} starts with an underscore, which a tool argument cannot")
        annotation = _resolve_parameter_annotation(handler, label, parameter.annotation)
        default = ... if parameter.default is inspect.Parameter.empty else parameter.default
        fields[name] = (annotation, default)

    try:
        input_schema = create_model(_input_model_name(handler), __module__=handler.__module__, **fields)
    except Exception as error:
        raise SdkError(f"Tool {qualname!s} parameters cannot form an input schema: {error}") from error
    field_names = tuple(fields)

    # `context` is the tool's context, when it takes one: the handler receives it first, by position.
    if inspect.iscoroutinefunction(handler):

        async def adapted(*context: Any, args: BaseModel, **kwargs: Any) -> Any:
            return await handler(*context, **{name: getattr(args, name) for name in field_names}, **kwargs)

    else:

        def adapted(*context: Any, args: BaseModel, **kwargs: Any) -> Any:  # type: ignore[misc]
            return handler(*context, **{name: getattr(args, name) for name in field_names}, **kwargs)

    # The tool derives its module-scope check, name and docstring from these
    # attributes, so they must describe the authored handler.
    for attribute in ("__module__", "__name__", "__qualname__", "__doc__"):
        if hasattr(handler, attribute):
            setattr(adapted, attribute, getattr(handler, attribute))
    # The signature check and the Session-input wrapper read this signature: the context, args,
    # then Session inputs by keyword, with their annotations already resolved.
    args_parameter = inspect.Parameter("args", inspect.Parameter.POSITIONAL_OR_KEYWORD, annotation=input_schema)
    adapted.__signature__ = signature.replace(parameters=[*context, args_parameter, *forwarded])  # type: ignore[attr-defined]
    return input_schema, adapted


def _tool_description(handler: Callable[..., Any], description: str | None) -> str:
    if description is not None:
        return description
    docstring = inspect.getdoc(handler)
    if not docstring:
        raise SdkError(
            f"Tool {getattr(handler, '__qualname__', handler)!s} needs a description: "
            "give the function a docstring or pass description="
        )
    return docstring


def _output_type(annotation: Any) -> Any:
    """The type of what the model reads back from a function with this return annotation."""

    origin = get_origin(annotation)
    if isinstance(origin, type) and issubclass(origin, collections.abc.Awaitable) and get_args(annotation):
        # A function may return an awaitable, such as a Future: the tool awaits it.
        annotation = get_args(annotation)[-1]
    if isinstance(annotation, type) and issubclass(annotation, ToolResult | AnnotatedToolResult):
        # `ToolResult[T]` says its structured content is a T; a bare ToolResult says nothing.
        value_types = annotation.__pydantic_generic_metadata__["args"]
        return value_types[0] if value_types else Any
    if is_rich_tool_result_type(annotation):
        # An MCP result or content blocks: the annotation says nothing about the structured
        # output, so the tool has no output schema unless output_schema= gives one.
        return Any
    return annotation


_NO_OUTPUT_TYPE: Any = object()


def _return_output_type(handler: Callable[..., Any], *, or_output_schema: bool) -> Any:
    """The result type from the function's return annotation, or ``_NO_OUTPUT_TYPE`` with a warning.

    With ``or_output_schema``, each warning also says that ``output_schema=`` gives the model an output schema.
    """

    or_pass = " or pass output_schema=" if or_output_schema else ""

    qualname = getattr(handler, "__qualname__", handler)
    annotation = session_input.read_signature(handler).return_annotation
    if annotation is inspect.Signature.empty:
        logger.warning(
            "Tool %s has no return annotation, so the model gets no output schema for it: annotate the return type%s",
            qualname,
            or_pass,
        )
        return _NO_OUTPUT_TYPE
    try:
        resolved = session_input.evaluate_annotation(handler, annotation)
    except Exception as error:
        # A name imported only under TYPE_CHECKING stays unresolved at runtime, under
        # `from __future__ import annotations` or Python 3.14's lazy annotations. Such a
        # tool worked before it had an output schema, so it keeps working without one.
        logger.warning(
            "Tool %s return annotation cannot be resolved at module scope (%s), so the model gets no "
            "output schema for it: import the type at runtime%s",
            qualname,
            error,
            or_pass,
        )
        return _NO_OUTPUT_TYPE
    return _output_type(resolved)


def _output_schema(handler: Callable[..., Any], output_schema: type[BaseModel] | None) -> dict[str, JsonValue] | None:
    """The JSON Schema of the tool's result: ``output_schema`` when given, else the return annotation's."""

    if output_schema is not None:
        return cast(dict[str, JsonValue], output_schema.model_json_schema(mode="serialization"))
    output = _output_adapter(handler, or_output_schema=True)
    return None if output is None else output[1]


class PythonTool[**P, R]:
    """A tool that runs a Python function on the worker.

    It is callable like the function itself: ``tool(...)`` takes the function's parameters and
    returns what the function returns, nothing added. ``tool_definition`` is what the model sees.

    ``name`` defaults to the function's name and ``description`` to its docstring. Without
    ``input_schema``, the input schema is built from the function's parameters and the function
    receives each argument by name; with it, the function receives the validated model as ``args``.
    The output schema is built from the return annotation, unless ``output_schema`` is given.
    Both arguments are Pydantic models. ``annotations`` are the tool's hints, such as
    ``read_only_hint``: every approval of a call to the tool carries them, in
    ``request.tool.annotations``. A tool cannot be changed after it is built.

    A function whose first parameter is a positional-only ``agents.ToolCallbackContext`` gets the
    context of each call. Called directly, such a tool takes the context or leaves it out:
    ``search(ctx, "q")`` and ``search("q")`` both work, the second with ``ToolCallbackContext.local()``.

    Each field of ``tool_definition`` can also be read on the tool: ``tool.name`` is
    ``tool.tool_definition.name``, and ``tool.input_schema`` is the JSON Schema, not the model.
    """

    tool_definition: ToolDefinition
    """What the model sees of the tool: its name, description, input schema and output schema."""
    handler: Callable[..., Any]
    """The function the tool calls, adapted to receive the validated arguments as ``args``."""
    input_model: type[BaseModel]
    """The Pydantic model the model's arguments are validated with."""
    namespace: str
    """The tool's group: its ID is ``<namespace>.<name>``, as in ``ToolCall.name`` and permission rules."""
    model_access: ToolModelAccess
    model_access_is_default: bool
    session_inputs: dict[str, type[session_input.SessionInput]]

    __wrapped__: Callable[P, R]
    """The function, as written."""
    _output_model: type[BaseModel] | None
    """The ``output_schema=`` model, which the structured result must match. ``None`` without one."""
    __name__: str
    __qualname__: str
    _handler_is_async: bool
    _context_parameter: str | None

    def __init__(
        self,
        *,
        handler: Callable[P, R],
        name: str | None = None,
        namespace: str = DEFAULT_TOOL_NAMESPACE,
        description: str | None = None,
        input_schema: type[BaseModel] | None = None,
        output_schema: type[BaseModel] | None = None,
        model_access: ToolModelAccess | None = None,
        result_schema: type[BaseModel] | None = None,
        annotations: ToolAnnotations | None = None,
    ) -> None:
        if result_schema is not None:
            if output_schema is not None:
                raise TypeError("Pass output_schema= only: result_schema= is its deprecated name")
            warnings.warn("result_schema= is deprecated: use output_schema=", DeprecationWarning, stacklevel=2)
            output_schema = result_schema
        function = handler
        model_access_is_default = model_access is None
        model_access = _validate_model_access("programmatic" if model_access is None else model_access)
        name = function.__name__ if name is None else name
        if not name.strip():
            raise ValueError("Tool name cannot be empty")
        namespace = _checked_namespace(namespace, name)
        description = _tool_description(function, description)
        context_parameter = _context_parameter(function)
        adapted: Callable[..., Any] = function
        if input_schema is None:
            input_schema, adapted = _plain_function_tool(function, context_parameter=context_parameter)
        session_input_parameters = session_input.session_input_parameters_of(adapted)
        handler_is_async = inspect.iscoroutinefunction(adapted)
        if session_input_parameters:
            adapted = _wrap_session_input_handler(adapted, session_input_parameters)
        if "." in function.__qualname__:
            raise ValueError("Decorated tools must be defined at module scope")
        _validate_handler_signature(adapted, context_parameter=context_parameter)
        definition = ToolDefinition(
            name=name,
            description=description,
            input_schema=input_schema.model_json_schema(),
            output_schema=_output_schema(function, output_schema),
            annotations=ToolAnnotations() if annotations is None else annotations,
        )
        # The instance __dict__ directly: __setattr__ refuses every change once the tool is built.
        vars(self).update(
            tool_definition=definition,
            handler=adapted,
            input_model=input_schema,
            _output_model=output_schema,
            namespace=namespace,
            model_access=model_access,
            model_access_is_default=model_access_is_default,
            session_inputs=session_input_parameters,
            _handler_is_async=handler_is_async,
            _context_parameter=context_parameter,
            # A tool stands in for its function: `getattr(module, tool.__name__) is tool`, and
            # `inspect.signature(tool)` is the function's.
            __doc__=function.__doc__,
            __module__=function.__module__,
            __name__=function.__name__,
            __qualname__=function.__qualname__,
            __wrapped__=function,
        )

    def __setattr__(self, name: str, value: object) -> None:
        raise AttributeError(f"Tool {self.tool_definition.name!r} cannot be changed after it is built")

    def __delattr__(self, name: str) -> None:
        raise AttributeError(f"Tool {self.tool_definition.name!r} cannot be changed after it is built")

    def __repr__(self) -> str:
        return f"PythonTool(name={self.tool_definition.name!r})"

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Call the function with the arguments given, as if it were not a tool.

        A function that takes a ``ToolCallbackContext`` gets ``ToolCallbackContext.local()`` when the
        call leaves it out.
        """

        if self._context_parameter is not None and not (args and isinstance(args[0], contracts.ToolCallbackContext)):
            return cast(Callable[..., R], self.__wrapped__)(contracts.ToolCallbackContext.local(), *args, **kwargs)
        return self.__wrapped__(*args, **kwargs)

    # The fields of `tool_definition`, read-only, so code written for 1.1.0rc12 keeps reading them.
    @property
    def name(self) -> str:
        """``tool_definition.name``: the name the model calls the tool by."""
        return self.tool_definition.name

    @property
    def title(self) -> str | None:
        """``tool_definition.title``: a name for people, for example in an approval prompt."""
        return self.tool_definition.title

    @property
    def description(self) -> str:
        """``tool_definition.description``: what the tool does, as the model reads it."""
        return self.tool_definition.description

    @property
    def input_schema(self) -> dict[str, JsonValue]:
        """``tool_definition.input_schema``: the JSON Schema of the arguments. The model is ``input_model``."""
        return self.tool_definition.input_schema

    @property
    def output_schema(self) -> dict[str, JsonValue] | None:
        """``tool_definition.output_schema``: the JSON Schema of the result, or ``None``."""
        return self.tool_definition.output_schema

    @property
    def annotations(self) -> ToolAnnotations:
        """``tool_definition.annotations``: hints about what the tool does, for a policy to read."""
        return self.tool_definition.annotations

    @property
    def source(self) -> str | None:
        """``tool_definition.source``: ``None``, as the agent defines the tool in its own code."""
        return self.tool_definition.source

    @property
    def required_input_ids(self) -> list[str]:
        return session_input.required_input_ids(self.session_inputs)

    async def invoke(self, context: "ToolCallbackContext | None" = None, /, **kwargs: Any) -> Any:
        """Invoke the handler with model arguments plus rebuilt Session inputs.

        ``context`` reaches a function that takes a ``ToolCallbackContext``; without it, that function
        gets ``ToolCallbackContext.local()``. A tool whose function takes no context ignores it.

        A tool that declares Session inputs takes their JSON values as
        ``injected_session_inputs={input_id: value}``: each is rebuilt into its annotated class and
        passed to the handler under its parameter name, never through the schema the model sees.
        Without that keyword, such a tool raises ``ValueError``. A tool that declares no Session inputs
        treats an ``injected_session_inputs`` keyword as a model argument, checked by its input schema.
        """

        error: ToolCodeError | None = None
        try:
            result = await self._invoke_unconverted(context, kwargs)
        except ToolFunctionError as raised:
            error = raised.error
        if error is not None:
            # A direct call raises what the function raised; only an agent's call reads tool_errors.
            # Raised outside the except block, so its __cause__ and __context__ stay the function's.
            raise error
        if isinstance(result, BaseModel) and not (
            isinstance(result, AnnotatedToolResult) or is_rich_tool_result(result)
        ):
            # By alias, as the output schema names the fields, and as the input schema does.
            return result.model_dump(mode="json", by_alias=True)
        return result

    async def _invoke_unconverted(self, context: "ToolCallbackContext | None", kwargs: dict[str, Any]) -> Any:
        """``invoke`` without dumping a returned model: the Runtime trusts an instance of the
        ``output_schema=`` model, whose dump can carry computed fields the schema forbids."""

        if not self.session_inputs:
            return await self._invoke_handler(context, kwargs)
        injected_session_inputs: dict[str, Any] | None = kwargs.pop("injected_session_inputs", None)
        rebuilt = session_input.rebuild_session_inputs(
            f"Tool {self.tool_definition.name!r}", self.session_inputs, injected_session_inputs
        )
        token = _session_inputs_context.set(rebuilt)
        try:
            return await self._invoke_handler(context, kwargs)
        finally:
            _session_inputs_context.reset(token)

    async def _invoke_handler(self, context: "ToolCallbackContext | None", kwargs: dict[str, Any]) -> Any:
        handler_args: tuple[Any, ...] = ()
        if self._context_parameter is not None:
            handler_args = (contracts.ToolCallbackContext.local() if context is None else context,)
        return await self._call_handler(handler_args, {"args": self.input_model.model_validate(kwargs)})

    async def _call_handler(self, handler_args: tuple[Any, ...], handler_kwargs: dict[str, Any]) -> Any:
        try:
            if self._handler_is_async:
                return await cast(Awaitable[Any], self.handler(*handler_args, **handler_kwargs))
            return await call_handler(self.handler, *handler_args, **handler_kwargs)
        except asyncio.CancelledError as error:
            if call_is_cancelling():
                raise
            raise ToolFunctionError(error) from error
        except Exception as error:
            raise ToolFunctionError(error) from error


class PythonToolWithContext[**P, R](PythonTool[Concatenate["ToolCallbackContext", P], R]):
    """A ``PythonTool`` whose function takes a ``ToolCallbackContext`` first.

    It exists for type checkers only: ``tool(ctx, ...)`` and ``tool(...)`` both type-check.
    """

    @overload
    def __call__(self, context: "ToolCallbackContext", /, *args: P.args, **kwargs: P.kwargs) -> R: ...
    @overload
    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R: ...
    # mypy reads `*args: Any` as not accepting the first overload's positional-only context.
    def __call__(self, *args: Any, **kwargs: Any) -> Any:  # type: ignore[misc]
        return super().__call__(*args, **kwargs)


def takes_context(tool: "PythonTool[..., Any]") -> bool:
    """Whether the tool's function takes a ``ToolCallbackContext``, which the worker fills for each call."""

    return tool._context_parameter is not None


def _python_tool(handler: Callable[..., Any], **options: Any) -> PythonTool[..., Any]:
    tool_class = PythonToolWithContext if _context_parameter(handler) is not None else PythonTool
    return tool_class(handler=handler, **options)


def authored_tool(
    tool: "PythonTool[..., Any] | ClientToolDefinition[Any] | ClientTool[..., Any] | Callable[..., Any]",
) -> "PythonTool[..., Any] | ClientToolDefinition[Any]":
    """A tool from an entry of ``tools=``: a plain function becomes a ``PythonTool``, as with ``@agents.tool``.

    A function becomes one tool however many agents list it, so the agents of a tree share its binding.
    A client tool stands for its declaration.
    """

    if isinstance(tool, ClientTool):
        return tool._declaration
    if not inspect.isfunction(tool):
        return cast("PythonTool[..., Any] | ClientToolDefinition[Any]", tool)
    built = _PLAIN_FUNCTION_TOOLS.get(tool)
    if built is None:
        built = _PLAIN_FUNCTION_TOOLS[tool] = _python_tool(tool)
    return built


def tool_name(tool: "PythonTool[..., Any] | ClientToolDefinition[Any]") -> str:
    """The name the model calls a Python or client tool by."""

    return tool.tool_definition.name if isinstance(tool, PythonTool) else tool.name


def tool_id(tool: "PythonTool[..., Any] | ClientToolDefinition[Any]") -> str:
    """A Python or client tool's ID, ``<namespace>.<name>``, unique in an agent."""

    return f"{tool.namespace}.{tool_name(tool)}"


class ClientToolDefinition[ToolInput: BaseModel](legacy_authoring.ClientToolDefinition[ToolInput]):
    """The declaration of a client tool, as the agent compiles it. Internal: authors use ``agents.client_tool``.

    Without a handler it compiles to a ``client_tool`` callback, which the application answers.
    With one, the worker runs the handler like any other tool.

    Session inputs declared with ``Depends()`` on the handler, whether passed to
    the constructor or bound later with ``with_handler``, compile into
    ``required_session_input_ids`` exactly like an authored tool's, but they
    are not injected by this class: the handler is invoked from the
    assembly-side tool registration (``sdk.assembly``), which rebuilds the
    Harness-injected values and passes them as keyword arguments. Calling the
    handler outside that registration delivers no Session inputs.

    As on ``PythonTool``, the ``input_schema`` argument is a Pydantic model: the tool keeps it as
    ``input_model`` and its JSON Schema as ``input_schema``, and ``annotations`` are the tool's
    hints, which every approval of a call to the tool carries in ``request.tool.annotations``.
    """

    # The Vibe SDK class keeps the model as `input_schema`; this class keeps its JSON Schema there.
    input_schema: dict[str, JsonValue]  # type: ignore[assignment]
    """The JSON Schema of the tool's arguments."""
    input_model: type[ToolInput]
    """The Pydantic model the arguments are validated with."""
    namespace: str
    """The tool's group: its ID is ``<namespace>.<name>``."""
    model_access: ToolModelAccess
    model_access_is_default: bool
    output_json_schema: dict[str, JsonValue] | None
    """The JSON Schema of the result the model reads back, from ``output_schema``."""
    annotations: ToolAnnotations
    """Hints about what the tool does, for approvals. A hint not declared takes MCP's default."""

    def __init__(
        self,
        *,
        name: str,
        description: str,
        input_schema: type[ToolInput],
        model_access: ToolModelAccess | None = None,
        output_schema: type[BaseModel] | dict[str, JsonValue] | None = None,
        handler: ToolHandler[ToolInput, Any] | None = None,
        namespace: str = DEFAULT_TOOL_NAMESPACE,
        annotations: ToolAnnotations | None = None,
    ) -> None:
        self.namespace = _checked_namespace(namespace, name)
        model_access_is_default = model_access is None
        model_access = _validate_model_access("programmatic" if model_access is None else model_access)
        self.session_inputs: dict[str, type[session_input.SessionInput]] = {}
        super().__init__(
            name=name,
            description=description,
            input_schema=input_schema,
            # A JSON Schema from a return annotation has no model to keep.
            output_schema=None if isinstance(output_schema, dict) else output_schema,
            handler=handler,
        )
        self.input_model = input_schema
        self.input_schema = input_schema.model_json_schema()
        self.model_access = model_access
        self.model_access_is_default = model_access_is_default
        if isinstance(output_schema, dict):
            self.output_json_schema = output_schema
        elif output_schema is not None:
            self.output_json_schema = cast(dict[str, JsonValue], output_schema.model_json_schema(mode="serialization"))
        else:
            self.output_json_schema = None
        self.annotations = ToolAnnotations() if annotations is None else annotations
        # The `ClientTool` built on this declaration, which an approval gives as the tool object.
        self._client_tool: ClientTool[..., Any] | None = None

    def to_callback(self) -> TaskCallback:
        """Build the protocol callback declaration backing this client-handled tool."""

        return TaskCallback(
            card=Card(
                name=self.name,
                description=self.description,
                input_schema=self.input_schema,
                output_schema=self.output_json_schema,
            )
        )

    def _bind_handler(self, handler: ToolHandler[ToolInput, Any]) -> None:
        """Bind a handler from the constructor or ``with_handler``, recording its Session inputs."""

        client_session_inputs = session_input.session_input_parameters_of(handler)
        if client_session_inputs:
            handler = _wrap_session_input_handler(handler, client_session_inputs)
        super()._bind_handler(handler)
        self.session_inputs = client_session_inputs

    @property
    def required_input_ids(self) -> list[str]:
        return session_input.required_input_ids(self.session_inputs)


class _ToolDecorator(Protocol):
    @overload
    def __call__[**P, R](
        self, handler: Callable[Concatenate["ToolCallbackContext", P], R], /
    ) -> PythonToolWithContext[P, R]: ...
    @overload
    def __call__[**P, R](self, handler: Callable[P, R], /) -> PythonTool[P, R]: ...


# A handler with or without keywords: `@agents.tool` or `agents.tool(fn, name=...)`.
@overload
def tool[**P, R](
    handler: Callable[Concatenate["ToolCallbackContext", P], R],
    /,
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    input_schema: type[BaseModel] | None = None,
    output_schema: type[BaseModel] | None = None,
    model_access: ToolModelAccess | None = None,
    result_schema: type[BaseModel] | None = None,
    annotations: ToolAnnotations | None = None,
) -> PythonToolWithContext[P, R]: ...


@overload
def tool[**P, R](
    handler: Callable[P, R],
    /,
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    input_schema: type[BaseModel] | None = None,
    output_schema: type[BaseModel] | None = None,
    model_access: ToolModelAccess | None = None,
    result_schema: type[BaseModel] | None = None,
    annotations: ToolAnnotations | None = None,
) -> PythonTool[P, R]: ...


@overload
def tool(
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    input_schema: type[BaseModel] | None = None,
    output_schema: type[BaseModel] | None = None,
    model_access: ToolModelAccess | None = None,
    result_schema: type[BaseModel] | None = None,
    annotations: ToolAnnotations | None = None,
) -> _ToolDecorator: ...


def tool(
    handler: Callable[..., Any] | None = None,
    /,
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    input_schema: type[BaseModel] | None = None,
    output_schema: type[BaseModel] | None = None,
    model_access: ToolModelAccess | None = None,
    result_schema: type[BaseModel] | None = None,
    annotations: ToolAnnotations | None = None,
) -> Any:
    """Decorate a module-level function as an Agents SDK tool, a ``PythonTool``.

    Use it bare, ``@agents.tool``, to take the name from the function, the description from its
    docstring, the input schema from its parameters and the output schema from its return
    annotation, or call it to override any of them. The tool stays callable like the function.
    ``annotations=agents.ToolAnnotations(read_only_hint=True)`` declares hints that every approval
    of a call to the tool carries.

    ``namespace`` groups the tool: its ID is ``<namespace>.<name>``, ``client.<name>`` by default.
    The ID is what ``ToolCall.name`` and permission rules use, and what ``run_typescript`` calls
    (``tools.<namespace>.<name>(...)``). Namespaces of the Harness's built-in tools and of the
    SDK's connector and guardrail tools raise ``SdkError``.

    The function may take an ``agents.ToolCallbackContext`` as its first, positional-only parameter:
    ``def search(ctx: agents.ToolCallbackContext, /, query: str)``. The worker fills it for each call.
    """

    def decorate(handler: Callable[..., Any]) -> PythonTool[..., Any]:
        return _python_tool(
            handler,
            name=name,
            namespace=namespace,
            description=description,
            input_schema=input_schema,
            output_schema=output_schema,
            model_access=model_access,
            result_schema=result_schema,
            annotations=annotations,
        )

    if handler is not None:
        return decorate(handler)
    return decorate


def _output_adapter(
    function: Callable[..., Any], *, or_output_schema: bool
) -> tuple[TypeAdapter[Any], dict[str, JsonValue] | None] | None:
    """The adapter of the tool's result type and its JSON Schema, from the function's return annotation.

    ``or_output_schema`` is true for a tool that takes ``output_schema=``: the messages then say to pass it.
    """

    output_type = _return_output_type(function, or_output_schema=or_output_schema)
    if output_type is _NO_OUTPUT_TYPE:
        return None
    label = f"Tool {getattr(function, '__qualname__', function)!s} return"
    try:
        adapter: TypeAdapter[Any] = TypeAdapter(output_type)
        schema = adapter.json_schema(mode="serialization")
    except Exception as error:
        hint = (
            "Pass output_schema="
            if or_output_schema
            else "Annotate it with a type Pydantic can describe, "
            "or declare the tool with input_schema= and output_schema="
        )
        raise SdkError(f"{label} annotation {output_type!r} cannot form an output schema: {error}. {hint}") from error
    # `Any` gives the empty schema, which says nothing about the result.
    return adapter, cast(dict[str, JsonValue], schema) or None


class ClientTool[**P, R]:
    """A tool the model can call and the application running the agent answers.

    The agent holds only its declaration: no code runs for it where the agent runs. When the model
    calls it, the turn waits until the application sends the result. Bind the function that answers
    it with ``@<tool>.answer``, and pass that function to ``Agent.run`` in
    ``on_client_tool=agents.ClientToolAnswers(...)``.

    Build one with ``@agents.client_tool`` on a stub function, or with
    ``agents.client_tool(name=..., description=..., input_schema=...)``.
    """

    __slots__ = ("_by_name", "_declaration", "_output_adapter", "_tool_definition")

    def __init__(
        self,
        declaration: ClientToolDefinition[BaseModel],
        *,
        by_name: bool,
        output_adapter: TypeAdapter[Any] | None = None,
    ) -> None:
        # The declaration the agent compiles: it also keeps the input model and the model access.
        self._declaration = declaration
        declaration._client_tool = self
        self._tool_definition = ToolDefinition(
            name=declaration.name,
            description=declaration.description,
            input_schema=declaration.input_schema,
            output_schema=declaration.output_json_schema,
            annotations=declaration.annotations,
        )
        # True when the input schema comes from a function's parameters: the answer then takes
        # each argument by name, as that function does, instead of the validated model.
        self._by_name = by_name
        # The stub's return type, which serializes the answer's result as the output schema says.
        self._output_adapter = output_adapter

    @property
    def tool_definition(self) -> ToolDefinition:
        """What the model sees of the tool: its name, description, and the JSON Schemas of its input
        and output, as on a ``PythonTool``."""

        return self._tool_definition

    @property
    def name(self) -> str:
        """The name the model calls the tool by."""

        return self._tool_definition.name

    @property
    def namespace(self) -> str:
        """The tool's group: its ID is ``<namespace>.<name>``, as ``ClientToolCall.name`` gives it."""

        return self._declaration.namespace

    @overload
    def answer(
        self,
        handler: Callable[
            Concatenate["ToolCallbackContext", P],
            R | ToolResult | KeepCallbackOpen | Awaitable[R | ToolResult | KeepCallbackOpen],
        ],
        /,
    ) -> "ClientToolAnswer[P, R]": ...

    @overload
    def answer(
        self,
        handler: Callable[P, R | ToolResult | KeepCallbackOpen | Awaitable[R | ToolResult | KeepCallbackOpen]],
        /,
    ) -> "ClientToolAnswer[P, R]": ...

    def answer(self, handler: Callable[..., Any], /) -> "ClientToolAnswer[P, R]":
        """Bind the function that answers this tool's calls, in the process that runs the agent.

        It takes the tool's parameters and returns its result, synchronously or not: a value of
        the stub's return type, or an ``agents.ToolResult`` to choose what the model sees. It
        returns ``agents.KeepCallbackOpen()`` to leave the call open: nothing is sent, and a run returns
        ``Blocked`` on the call, which ``turn.answer`` or another client answers. Pass
        what this returns to ``Agent.run`` in ``on_client_tool=agents.ClientToolAnswers(...)``.
        It may take an ``agents.ToolCallbackContext`` first, positional-only, as a tool does:
        ``def answer(ctx: agents.ToolCallbackContext, /, city: str)``. It gets the Session and the
        call's ID there; its sandbox is unbound.
        Its other parameters are not checked here. An answer whose parameter names or kinds do not
        match fails at its first call, as a failed tool call the model sees. An answer that only
        types a parameter differently is still called, with the value the declaration validated.
        """

        return ClientToolAnswer(tool=self, handler=handler)

    def called(self, callback: "OpenCallback", /) -> "TypeIs[OpenClientToolCall[P, R]]":
        """Whether ``callback`` is an open call of this tool: an ``OpenClientToolCall`` whose
        ``call.name`` is this tool's ID, ``<namespace>.<name>``.

        A type checker then types ``callback.run(fn)`` by this stub: ``fn`` takes the stub's
        parameters and returns its return type::

            for callback in state.callbacks:
                if get_location.called(callback):
                    await turn.answer(callback.id, await callback.run(read_gps))
        """

        from mistralai.vibe_agents.sdk.client.records import OpenClientToolCall

        return isinstance(callback, OpenClientToolCall) and callback.call.name == f"{self.namespace}.{self.name}"

    def __repr__(self) -> str:
        return f"ClientTool(name={self.name!r})"


@dataclass(frozen=True)
class ClientToolAnswer[**P, R]:
    """The function that answers one client tool's calls, bound with ``@<tool>.answer``."""

    tool: ClientTool[P, R]
    handler: (
        Callable[P, R | ToolResult | KeepCallbackOpen | Awaitable[R | ToolResult | KeepCallbackOpen]]
        | Callable[
            Concatenate["ToolCallbackContext", P],
            R | ToolResult | KeepCallbackOpen | Awaitable[R | ToolResult | KeepCallbackOpen],
        ]
    )
    # True when the handler takes an ``agents.ToolCallbackContext`` first: read from the handler, so it
    # always matches it.
    _takes_context: bool = field(init=False, repr=False, compare=False)

    def __post_init__(self) -> None:
        object.__setattr__(self, "_takes_context", _context_parameter(self.handler) is not None)


async def call_client_tool_answer(
    answer: ClientToolAnswer[..., Any], arguments: object, context: "ToolCallbackContext | None" = None
) -> Any:
    """Validate the model's arguments to a client tool and call its answer with them.

    An answer that takes a context gets ``context``, or ``ToolCallbackContext.local()`` without one.
    A synchronous answer runs in a tool thread, as a tool body does, so it never blocks the loop
    that serves the Session.
    """

    tool = answer.tool
    parsed = tool._declaration.input_model.model_validate(arguments)
    # ``_takes_context`` tells which of the two forms the handler has.
    handler: Callable[..., Any] = answer.handler
    if answer._takes_context:
        handler = functools.partial(handler, contracts.ToolCallbackContext.local() if context is None else context)
    try:
        return await call_with_arguments(tool, handler, parsed)
    except asyncio.CancelledError as error:
        if call_is_cancelling():
            raise
        raise ToolFunctionError(error) from error
    except Exception as error:
        raise ToolFunctionError(error) from error


async def call_with_arguments(tool: ClientTool[..., Any], handler: Callable[..., Any], parsed: BaseModel) -> Any:
    """Call ``handler`` with a client tool's validated arguments, as the stub takes them: by name
    for a stub function, as the input model otherwise. A synchronous handler runs in a tool thread."""

    if tool._by_name:
        return await call_handler(handler, **{name: getattr(parsed, name) for name in type(parsed).model_fields})
    return await call_handler(functools.partial(handler, parsed))


def dump_client_tool_result(answer: ClientToolAnswer[..., Any], result: object) -> object:
    """The answer's result as JSON data, serialized by the stub's return type when it has one."""

    adapter = answer.tool._output_adapter
    if adapter is None or is_rich_tool_result(result):
        # A ToolResult or content blocks say themselves what the model sees.
        return result
    return adapter.dump_python(result, mode="json", by_alias=True)


def author_tool(
    tool: "PythonTool[..., Any] | ClientToolDefinition[Any]",
) -> "PythonTool[..., Any] | ClientToolDefinition[Any] | ClientTool[..., Any]":
    """The tool object the author gave for a compiled tool: the ``ClientTool`` a declaration comes from."""

    if isinstance(tool, ClientToolDefinition) and tool._client_tool is not None:
        return tool._client_tool
    return tool


def declared_tool(
    tool: "PythonTool[..., Any] | ClientToolDefinition[Any] | ClientTool[..., Any]",
) -> "PythonTool[..., Any] | ClientToolDefinition[Any]":
    """The declaration the agent compiles for an entry of ``tools=``."""

    return tool._declaration if isinstance(tool, ClientTool) else tool


def _client_tool_from_function(
    function: Callable[..., Any],
    *,
    name: str | None,
    namespace: str,
    description: str | None,
    model_access: ToolModelAccess | None,
    annotations: ToolAnnotations | None,
) -> ClientTool[Any, Any]:
    qualname = getattr(function, "__qualname__", function)
    session_inputs = session_input.session_input_parameters_of(function)
    if session_inputs:
        raise SdkError(
            f"Client tool {qualname!s} declares Session inputs ({', '.join(session_inputs)}): "
            "the application answers it, so read them there"
        )
    if (context := _context_parameter(function)) is not None:
        raise SdkError(
            f"Client tool {qualname!s} declares {context!r}, an agents.ToolCallbackContext: the stub "
            "declares only the model's arguments. Take the context in the answer: "
            f"def answer({context}: agents.ToolCallbackContext, /, ...)"
        )
    input_schema, _ = _plain_function_tool(function, context_parameter=None)
    output = _output_adapter(function, or_output_schema=False)
    definition = ClientToolDefinition(
        name=function.__name__ if name is None else name,
        namespace=namespace,
        description=_tool_description(function, description),
        input_schema=input_schema,
        model_access=model_access,
        output_schema=None if output is None else output[1],
        annotations=annotations,
    )
    return ClientTool(definition, by_name=True, output_adapter=None if output is None else output[0])


class _ClientToolDecorator(Protocol):
    @overload
    def __call__[**P, R](self, function: Callable[P, Awaitable[R]], /) -> ClientTool[P, R]: ...

    @overload
    def __call__[**P, R](self, function: Callable[P, R], /) -> ClientTool[P, R]: ...


# A stub with or without keywords: `@agents.client_tool` or `agents.client_tool(fn, name=...)`.
@overload
def client_tool[**P, R](
    function: Callable[P, Awaitable[R]],
    /,
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    model_access: ToolModelAccess | None = None,
    annotations: ToolAnnotations | None = None,
) -> ClientTool[P, R]: ...


@overload
def client_tool[**P, R](
    function: Callable[P, R],
    /,
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    model_access: ToolModelAccess | None = None,
    annotations: ToolAnnotations | None = None,
) -> ClientTool[P, R]: ...


@overload
def client_tool[ToolInput: BaseModel, ToolOutput: BaseModel](
    *,
    name: str,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str,
    input_schema: type[ToolInput],
    output_schema: type[ToolOutput],
    model_access: ToolModelAccess | None = None,
    annotations: ToolAnnotations | None = None,
) -> ClientTool[[ToolInput], ToolOutput]: ...


@overload
def client_tool[ToolInput: BaseModel](
    *,
    name: str,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str,
    input_schema: type[ToolInput],
    output_schema: None = None,
    model_access: ToolModelAccess | None = None,
    annotations: ToolAnnotations | None = None,
) -> ClientTool[[ToolInput], Any]: ...


@overload
def client_tool(
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    model_access: ToolModelAccess | None = None,
    annotations: ToolAnnotations | None = None,
) -> _ClientToolDecorator: ...


def client_tool(
    function: Callable[..., Any] | None = None,
    /,
    *,
    name: str | None = None,
    namespace: str = DEFAULT_TOOL_NAMESPACE,
    description: str | None = None,
    input_schema: type[BaseModel] | None = None,
    output_schema: type[BaseModel] | None = None,
    model_access: ToolModelAccess | None = None,
    annotations: ToolAnnotations | None = None,
) -> Any:
    """Declare a tool the model can call and the application running the agent answers.

    Put ``@agents.client_tool`` on a stub whose body is ``raise NotImplementedError``: the name
    comes from the function, the description from its docstring, the input schema from its
    parameters and the output schema from its return annotation. Call it with ``name=`` or
    ``description=`` to override them. The function never runs: it only describes the tool, and
    its answer takes the same parameters.

    Or declare the tool without a function, for example from a JSON contract: pass ``name=``,
    ``description=``, ``input_schema=`` and ``output_schema=``, Pydantic models. The answer then
    receives the validated model. Without ``output_schema=`` the model gets no output schema and
    the answer's return is not typed, so it warns.

    ``namespace`` groups the tool: its ID is ``<namespace>.<name>``, ``client.<name>`` by default,
    as ``ClientToolCall.name`` and ``ToolCall.name`` give it. Namespaces of the Harness's built-in
    tools and of the SDK's connector and guardrail tools raise ``SdkError``.

    ``annotations`` are the tool's hints, which every approval of a call to the tool carries in
    ``request.tool.annotations``.

    The worker never runs a client tool: the turn waits until the application sends the result.
    Answer it with a function bound by ``@<tool>.answer``, or by hand with
    ``turn.answer(callback.id, result)`` when a run returns ``Blocked``.
    """

    if input_schema is not None:
        if function is not None:
            raise SdkError(
                "agents.client_tool(input_schema=...) declares a tool without a function: it decorates nothing"
            )
        if name is None or description is None:
            missing = " and ".join(
                label for label, value in (("name=", name), ("description=", description)) if value is None
            )
            raise SdkError(
                f"agents.client_tool(input_schema=...) declares a tool without a function, so it needs {missing}"
            )
        if output_schema is None:
            warnings.warn(
                f"Client tool {name!r} has no output_schema=, so the model gets no output schema and its "
                "answer's return is neither typed nor checked: pass output_schema=",
                stacklevel=2,
            )
        definition = ClientToolDefinition(
            name=name,
            namespace=namespace,
            description=description,
            input_schema=input_schema,
            model_access=model_access,
            output_schema=output_schema,
            annotations=annotations,
        )
        return ClientTool(cast(ClientToolDefinition[BaseModel], definition), by_name=False)

    if output_schema is not None:
        raise SdkError(
            "agents.client_tool(output_schema=...) needs input_schema=, name= and description= too. "
            "On a function, the return annotation is the output schema"
        )

    def decorate(function: Callable[..., Any]) -> ClientTool[Any, Any]:
        return _client_tool_from_function(
            function,
            name=name,
            namespace=namespace,
            description=description,
            model_access=model_access,
            annotations=annotations,
        )

    if function is not None:
        return decorate(function)
    return decorate


__all__ = [
    "ClientTool",
    "ClientToolAnswer",
    "ClientToolDefinition",
    "PythonTool",
    "ToolModelAccess",
    "client_tool",
    "tool",
]
