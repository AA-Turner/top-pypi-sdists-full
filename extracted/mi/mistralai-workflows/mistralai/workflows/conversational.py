from __future__ import annotations

import re
import types
import uuid
from collections.abc import Callable, Sequence
from datetime import date, datetime
from typing import Any, Generic, Literal, Self, TypeVar, Union, cast, get_args, get_origin, get_type_hints, overload

import structlog
from pydantic import BaseModel, ConfigDict, Field, model_validator

from mistralai.workflows.core.task.task import Task

logger = structlog.get_logger(__name__)

ChoiceT = TypeVar("ChoiceT", bound=str)


class TextChunk(BaseModel):
    type: Literal["text"] = "text"
    text: str


class SearchReplaceBlock(BaseModel):
    search: str
    replace: str


class CreateFileOperation(BaseModel):
    type: Literal["create"] = "create"
    uri: str
    content: str


class ReadFileOperation(BaseModel):
    type: Literal["read"] = "read"
    uri: str
    offset: int = 0
    linesRead: int = 0


class ReplaceFileOperation(BaseModel):
    type: Literal["replace"] = "replace"
    uri: str
    fileContentBefore: str
    blocks: list[SearchReplaceBlock]


class DeleteFileOperation(BaseModel):
    type: Literal["delete"] = "delete"
    uri: str


FileOperation = CreateFileOperation | ReadFileOperation | ReplaceFileOperation | DeleteFileOperation


class FileToolUIState(BaseModel):
    type: Literal["file"] = "file"
    toolCallId: str
    operations: list[FileOperation]


class ToolResultPending(BaseModel):
    status: Literal["pending"] = "pending"


class ToolResultRunning(BaseModel):
    status: Literal["running"] = "running"


class ToolResultFailed(BaseModel):
    status: Literal["failed"] = "failed"
    error: Any


class ToolResultSuccess(BaseModel):
    status: Literal["success"] = "success"
    value: Any


ToolResult = ToolResultPending | ToolResultRunning | ToolResultFailed | ToolResultSuccess


class GenericToolUIState(BaseModel):
    type: Literal["generic_tool"] = "generic_tool"
    toolCallId: str
    name: str
    arguments: dict[str, Any]
    result: ToolResult


class CommandResultRunning(BaseModel):
    status: Literal["running"] = "running"


class CommandResultSuccess(BaseModel):
    status: Literal["success"] = "success"
    output: str


class CommandResultFailed(BaseModel):
    status: Literal["failed"] = "failed"
    error: str


CommandResult = CommandResultRunning | CommandResultSuccess | CommandResultFailed


class CommandToolUIState(BaseModel):
    type: Literal["command"] = "command"
    toolCallId: str
    command: str
    result: CommandResult


ToolUIState = FileToolUIState | GenericToolUIState | CommandToolUIState


class ChatAssistantWorkingTask(BaseModel):
    model_config = ConfigDict(title="working")

    type: Literal["tool", "thinking"] | str = "tool"
    title: str
    content: str
    toolUIState: ToolUIState | None = None


class TodoListItemState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    status: TodoListItemStatus = "todo"
    title: str
    description: str


class TodoListState(BaseModel):
    model_config = ConfigDict(title="todo_list")
    items: list[TodoListItemState]


type TodoListItemStatus = Literal["todo", "in_progress", "done"]


class TodoListItem:
    """A todo list item with context manager support for automatic status updates.

    Usage:
        ```python
        item = TodoListItem(title="Validate expense", description="Check details")

        async with TodoList(items=[item]) as todo_list:
            # Using context manager for automatic status transitions
            async with item:
                # Status is set to "in_progress" on enter
                ...
                # Status is set to "done" on successful exit

            # Or manual status control
            await item.set_status("in_progress")
            ...
            await item.set_status("done")
        ```
    """

    def __init__(self, title: str, description: str) -> None:
        self._id: str = str(uuid.uuid4())
        self._title: str = title
        self._description: str = description
        self._status: TodoListItemStatus = "todo"
        self._todo_list: TodoList | None = None

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def status(self) -> TodoListItemStatus:
        return self._status

    def _bind(self, todo_list: TodoList) -> None:
        """Internal: bind this item to a TodoList."""
        if self._todo_list is not None and self._todo_list is not todo_list:
            raise RuntimeError("TodoListItem is already bound to a different TodoList")
        self._todo_list = todo_list

    def _unbind(self) -> None:
        """Internal: unbind this item from a TodoList."""
        self._todo_list = None

    async def set_status(self, status: TodoListItemStatus) -> None:
        """Update the status of this item and emit an event."""
        if self._todo_list is None:
            raise RuntimeError("TodoListItem is not bound to a TodoList - use within a TodoList context")
        self._status = status
        await self._todo_list._sync_state()

    async def __aenter__(self) -> TodoListItem:
        """Set status to 'in_progress' on enter."""
        await self.set_status("in_progress")
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: Any | None,
    ) -> None:
        """Set status to 'done' on success, leave unchanged on exception."""
        if exc_type is None:
            await self.set_status("done")


class TextOutput(BaseModel):
    type: Literal["text"] = "text"
    text: str


class TodoList(Task[TodoListState]):
    """A list of todo items with real-time status updates.

    TodoList is a specialized Task that manages a collection of TodoListItem instances
    and emits events as items progress through their lifecycle.

    Usage:
        ```python
        item1 = TodoListItem(title="Validate", description="Check details")
        item2 = TodoListItem(title="Process", description="Execute action")

        async with TodoList(items=[item1, item2]) as todo_list:
            # Add items
            item3 = TodoListItem(title="Notify", description="Send notification")
            await todo_list.add_item(item3)

            # Remove items
            await todo_list.remove_item(item2)

            # Work through items
            async with item1:
                ...  # item1 goes in_progress -> done
        ```
    """

    def __init__(self, items: list[TodoListItem] | None = None, id: str | None = None) -> None:
        self._todo_items: list[TodoListItem] = list(items) if items else []
        for item in self._todo_items:
            item._bind(self)
        super().__init__(
            type="todo_list",
            state=self._build_state(),
            id=id,
        )

    def _build_state(self) -> TodoListState:
        return TodoListState(
            items=[
                TodoListItemState(
                    id=item.id,
                    status=item.status,
                    title=item.title,
                    description=item.description,
                )
                for item in self._todo_items
            ]
        )

    async def _sync_state(self) -> None:
        await self.set_state(self._build_state())

    @property
    def items(self) -> list[TodoListItem]:
        return list(self._todo_items)

    async def add_item(self, item: TodoListItem) -> None:
        if item in self._todo_items:
            raise ValueError("TodoListItem is already in this TodoList")
        item._bind(self)
        self._todo_items.append(item)
        await self._sync_state()

    async def remove_item(self, item: TodoListItem) -> None:
        if item not in self._todo_items:
            raise ValueError("TodoListItem is not in this TodoList")
        item._unbind()
        self._todo_items.remove(item)
        await self._sync_state()

    async def __aenter__(self) -> Self:
        await super().__aenter__()
        return self


ChatInputMessageContent = list[TextChunk]

_ModelT = TypeVar("_ModelT", bound=BaseModel)


def input_tag(tag: str) -> Callable[[type[_ModelT]], type[_ModelT]]:
    """Annotate a Pydantic model's JSON schema with ``x-input-tag``.

    Clients use this annotation to select the correct input variant when a
    workflow exposes multiple input schemas for different consumers.

    Args:
        tag: Arbitrary identifier surfaced in the schema as ``x-input-tag``.

    Example::

        @input_tag("my-custom-input")
        class MyWorkflowInput(BaseModel):
            message: ChatInputMessageContent
    """

    def _decorator(cls: type[_ModelT]) -> type[_ModelT]:
        existing = cls.model_config.get("json_schema_extra")
        if callable(existing):
            original_callable = cast("Callable[[dict[str, Any]], None]", existing)

            def _composed(schema: dict[str, Any]) -> None:
                original_callable(schema)
                schema["x-input-tag"] = tag

            cls.model_config["json_schema_extra"] = _composed
        else:
            existing_dict = existing if isinstance(existing, dict) else {}
            cls.model_config["json_schema_extra"] = {**existing_dict, "x-input-tag": tag}
        cls.model_rebuild(force=True)
        return cls

    return _decorator


class ChatInputModel(BaseModel):
    model_config = ConfigDict(title="ChatInput", extra="forbid")
    message: ChatInputMessageContent


def ChatInput(
    prompt: str = "Type your message", *, suggestions: list[ChatInputMessageContent] | None = None
) -> type[ChatInputModel]:
    """Create a ChatInput schema with a custom prompt/placeholder.

    Args:
        prompt: The placeholder text shown in the chat input field.
        suggestions: List of message suggestions that can be directly submitted.

    Example:
        ```python
        user_input = await self.wait_for_input(ChatInput(
            "Ask a follow-up question",
            suggestions=[[TextChunk(text="What is the option 1?")], [TextChunk(text="What is the option 2?")]],
        ))
        ```
    """

    class _ChatInput(ChatInputModel):
        message: list[TextChunk] = Field(description=prompt, examples=suggestions)

    return _ChatInput


class CanvasInputData(BaseModel):
    title: str
    content: str


class CanvasInputModel(BaseModel):
    model_config = ConfigDict(title="Canvas", extra="forbid")
    canvas: CanvasInputData
    chatInput: ChatInputModel | None = None


def CanvasInput(canvas_uri: str, *, prompt: str | None = None) -> type[CanvasInputModel]:
    """Create a CanvasInput schema that references a previously output canvas.

    The canvas identified by ``canvas_uri`` must have been output in a prior
    workflow step with a ``CanvasResource`` whose ``uri`` matches.

    Args:
        canvas_uri: URI of the canvas to reference (must match a
            ``CanvasResource.uri`` from a previous workflow step output).
        prompt: Optional placeholder text for a chat input field alongside
            the canvas. When provided, the user can send follow-up
            instructions with their canvas edits.

    Example:
        ```python
        result = await self.wait_for_input(
            CanvasInput(canvas_uri="file://canvas/draft.md")
        )
        print(result.canvas.title, result.canvas.content)

        result = await self.wait_for_input(
            CanvasInput(
                canvas_uri="file://canvas/draft.md",
                prompt="Any feedback on the document?",
            )
        )
        if result.chatInput:
            print(result.chatInput.message)
        ```
    """
    metadata = {"canvasUri": canvas_uri}

    def _canvas_schema_extra(schema: dict[str, Any]) -> None:
        schema["$metadata"] = metadata
        props = schema.get("properties", {})
        if prompt is None:
            props.pop("chatInput", None)

    class _ChatInput(ChatInputModel):
        message: list[TextChunk] = Field(description=prompt or "")

    class _CanvasInput(CanvasInputModel):
        model_config = ConfigDict(title="Canvas", json_schema_extra=_canvas_schema_extra)
        chatInput: _ChatInput | None = None

    return _CanvasInput


class _SingleChoiceSchemaExtra:
    def __init__(
        self, options: Sequence[tuple[str, str]] | Sequence[str], description: str | None, default: str | None = None
    ):
        self.allowed_values: list[str] = []
        for opt in options:
            if isinstance(opt, str):
                self.allowed_values.append(opt)
            else:
                self.allowed_values.append(opt[0])
        self.options = options
        self.description = description

        # Validate that default is in allowed values
        if default is not None and default not in self.allowed_values:
            logger.warning(
                "SingleChoice prefilled_value is not a valid option, ignoring",
                prefilled_value=default,
                allowed_values=self.allowed_values,
            )
        self.default = default if default is not None and default in self.allowed_values else None

    def __call__(self, schema: dict[str, Any]) -> None:
        one_of = []
        for opt in self.options:
            if isinstance(opt, str):
                one_of.append({"type": "string", "const": opt})
            else:
                value, label = opt
                one_of.append({"type": "string", "const": value, "description": label})
        schema["oneOf"] = one_of
        if self.description:
            schema["description"] = self.description
        if self.default is not None:
            schema["default"] = self.default
        schema.pop("type", None)
        schema.pop("title", None)


class _MultiChoiceSchemaExtra:
    def __init__(
        self, options: list[tuple[str, str]] | list[str], description: str | None, default: list[str] | None = None
    ):
        self.allowed_values: list[str] = []
        for opt in options:
            if isinstance(opt, str):
                self.allowed_values.append(opt)
            else:
                self.allowed_values.append(opt[0])
        if len(self.allowed_values) != len(set(self.allowed_values)):
            raise ValueError("MultiChoice options contain duplicate values")
        self.options = options
        self.description = description

        # Validate that all default values are in allowed values, deduplicate
        if default:
            default = list(dict.fromkeys(default))
            invalid = [item for item in default if item not in self.allowed_values]
            if invalid:
                logger.warning(
                    "MultiChoice prefilled_value contains invalid options, ignoring",
                    invalid_values=invalid,
                    allowed_values=self.allowed_values,
                )
                self.default = None
            else:
                self.default = default
        else:
            self.default = None

    def __call__(self, schema: dict[str, Any]) -> None:
        any_of = []
        for opt in self.options:
            if isinstance(opt, str):
                any_of.append({"type": "string", "const": opt})
            else:
                value, label = opt
                any_of.append({"type": "string", "const": value, "description": label})
        schema["type"] = "array"
        schema["items"] = {"anyOf": any_of}
        schema["minItems"] = 1
        schema["uniqueItems"] = True
        if self.description:
            schema["description"] = self.description
        if self.default is not None:
            schema["default"] = self.default
        schema.pop("title", None)


class FormInput(BaseModel):
    """Base class for form input models used with wait_for_input().

    FormInput models generate JSON schemas that are compatible with
    the workflow form UI. Use this as a base class for models that
    will be used with wait_for_input().

    Example:
        ```python
        class ExpenseForm(FormInput):
            reason: str = TextField(description="Expense reason")
            amount: float = NumberField(description="Amount in USD", minimum=0)
            category: str = SingleChoice(
                options=[("travel", "Travel"), ("equipment", "Equipment")],
                description="Category"
            )
        ```
    """

    model_config = ConfigDict(title="FormInput")

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        super().__pydantic_init_subclass__(**kwargs)
        try:
            hints = get_type_hints(cls)
        except Exception:
            return
        for field_name, field_info in cls.model_fields.items():
            if not isinstance(field_info.json_schema_extra, _FileFieldSchemaExtra):
                continue
            # Validate that the type annotation matches the FileField config:
            # multiple=True requires list[...], include_metadata=True requires FileWithMetadataValue.
            config = field_info.json_schema_extra
            annotation = hints.get(field_name)
            if annotation is None:
                continue

            # Unwrap Optional / Union with None (e.g. list[str] | None -> list[str]).
            unwrapped = annotation
            origin = get_origin(annotation)
            if origin is Union or origin is types.UnionType:
                args = [a for a in get_args(annotation) if a is not type(None)]
                if len(args) == 1:
                    unwrapped = args[0]

            is_list = get_origin(unwrapped) is list
            if is_list:
                inner = get_args(unwrapped)[0] if get_args(unwrapped) else None
            else:
                inner = unwrapped

            if config.multiple and not is_list:
                raise TypeError(
                    f"Field '{field_name}' has multiple=True but type annotation is not a list. "
                    f"Expected list[str] or list[FileWithMetadataValue]."
                )
            if not config.multiple and is_list:
                raise TypeError(
                    f"Field '{field_name}' has multiple=False but type annotation is a list. "
                    f"Use multiple=True or change the annotation to a non-list type."
                )
            if config.include_metadata and inner is not FileWithMetadataValue:
                raise TypeError(
                    f"Field '{field_name}' has include_metadata=True but type annotation "
                    f"is not FileWithMetadataValue. Expected "
                    f"{'list[FileWithMetadataValue]' if config.multiple else 'FileWithMetadataValue'}."
                )
            if not config.include_metadata and inner is not str:
                raise TypeError(
                    f"Field '{field_name}' has include_metadata=False but type annotation "
                    f"is not str. Expected {'list[str]' if config.multiple else 'str'}."
                )

    @model_validator(mode="after")
    def _validate_single_choice_fields(self) -> Self:
        for field_name, field_info in self.__class__.model_fields.items():
            json_schema_extra = field_info.json_schema_extra
            if isinstance(json_schema_extra, _SingleChoiceSchemaExtra):
                value = getattr(self, field_name)
                if value not in json_schema_extra.allowed_values:
                    raise ValueError(
                        f"Invalid value '{value}' for field '{field_name}'. "
                        f"Must be one of: {json_schema_extra.allowed_values}"
                    )
        return self

    @model_validator(mode="after")
    def _validate_multi_choice_fields(self) -> Self:
        for field_name, field_info in self.__class__.model_fields.items():
            json_schema_extra = field_info.json_schema_extra
            if isinstance(json_schema_extra, _MultiChoiceSchemaExtra):
                values = getattr(self, field_name)
                if not isinstance(values, list):
                    raise ValueError(f"Invalid value for field '{field_name}'. Expected a list.")
                if len(values) == 0:
                    raise ValueError(f"Invalid value for field '{field_name}'. List must not be empty.")
                if len(values) != len(set(values)):
                    raise ValueError(f"Invalid value for field '{field_name}'. List must not contain duplicates.")
                for v in values:
                    if v not in json_schema_extra.allowed_values:
                        raise ValueError(
                            f"Invalid value '{v}' for field '{field_name}'. "
                            f"Must be one of: {json_schema_extra.allowed_values}"
                        )
        return self


def TextField(
    description: str,
    *,
    pattern: str | None = None,
    prefilled_value: str | None = None,
) -> Any:
    """Create a text field for form inputs.

    Args:
        description: Human-readable description shown as label/placeholder.
        pattern: Optional regex pattern for validation.
        prefilled_value: Optional pre-filled value for the UI form. This is a display hint
            only — the field remains required and must be explicitly submitted.

    Example:
        ```python
        class MyForm(FormInput):
            name: str = TextField(description="Enter your name", prefilled_value="John Doe")
        ```
    """

    validated_initial = prefilled_value
    if prefilled_value is not None and pattern is not None:
        if not re.fullmatch(pattern, prefilled_value):
            logger.warning(
                "TextField prefilled_value does not match pattern, ignoring",
                prefilled_value=prefilled_value,
                pattern=pattern,
            )
            validated_initial = None

    def _schema_extra(schema: dict[str, Any]) -> None:
        schema["type"] = "string"
        if validated_initial is not None:
            schema["default"] = validated_initial
        schema.pop("title", None)

    return Field(
        description=description,
        pattern=pattern,
        json_schema_extra=_schema_extra,
    )


def NumberField(
    description: str,
    *,
    minimum: float | None = None,
    maximum: float | None = None,
    exclusive_minimum: float | None = None,
    exclusive_maximum: float | None = None,
    prefilled_value: float | None = None,
) -> Any:
    """Create a number field for form inputs.

    Args:
        description: Human-readable description shown as label.
        minimum: Optional minimum value (inclusive).
        maximum: Optional maximum value (inclusive).
        exclusive_minimum: Optional exclusive minimum value.
        exclusive_maximum: Optional exclusive maximum value.
        prefilled_value: Optional pre-filled value for the UI form. This is a display hint
            only — the field remains required and must be explicitly submitted.

    Example:
        ```python
        class MyForm(FormInput):
            age: float = NumberField(description="Your age", minimum=0, maximum=120, prefilled_value=25)
            price: float = NumberField(
                description="Price in USD",
                minimum=0,
                exclusive_maximum=10000,
                prefilled_value=99.99
            )
        ```
    """

    validated_initial: float | None = None
    if prefilled_value is not None:
        if (
            (minimum is None or prefilled_value >= minimum)
            and (maximum is None or prefilled_value <= maximum)
            and (exclusive_minimum is None or prefilled_value > exclusive_minimum)
            and (exclusive_maximum is None or prefilled_value < exclusive_maximum)
        ):
            validated_initial = prefilled_value
        else:
            logger.warning(
                "NumberField prefilled_value is out of bounds, ignoring",
                prefilled_value=prefilled_value,
                minimum=minimum,
                maximum=maximum,
                exclusive_minimum=exclusive_minimum,
                exclusive_maximum=exclusive_maximum,
            )

    def _schema_extra(schema: dict[str, Any]) -> None:
        schema["type"] = "number"
        if validated_initial is not None:
            schema["default"] = validated_initial
        schema.pop("title", None)

    return Field(
        description=description,
        ge=minimum,
        le=maximum,
        gt=exclusive_minimum,
        lt=exclusive_maximum,
        json_schema_extra=_schema_extra,
    )


def DateTimeField(description: str, *, prefilled_value: datetime | str | None = None) -> Any:
    """Create a datetime field for form inputs.

    Args:
        description: Human-readable description shown as label.
        prefilled_value: Optional pre-filled value for the UI form (datetime object or ISO 8601 string).
            This is a display hint only — the field remains required and must be explicitly
            submitted. If invalid, no initial value will be set.

    Example:
        ```python
        from datetime import datetime, timezone

        class MyForm(FormInput):
            start_date: datetime = DateTimeField(
                description="Start date and time",
                prefilled_value=datetime(2023, 1, 1, tzinfo=timezone.utc),
            )
        ```
    """

    validated_initial: str | None = None
    if prefilled_value is not None:
        try:
            if isinstance(prefilled_value, str):
                prefilled_value = datetime.fromisoformat(prefilled_value.replace("Z", "+00:00"))
            validated_initial = prefilled_value.isoformat()
        except (ValueError, TypeError):
            logger.warning(
                "DateTimeField prefilled_value is not a valid datetime, ignoring",
                prefilled_value=prefilled_value,
            )
            validated_initial = None

    def _schema_extra(schema: dict[str, Any]) -> None:
        schema["type"] = "string"
        schema["format"] = "date-time"
        schema["description"] = description
        if validated_initial is not None:
            schema["default"] = validated_initial
        schema.pop("title", None)

    return Field(json_schema_extra=_schema_extra)


def DateField(description: str, *, prefilled_value: date | str | None = None) -> Any:
    """Create a date (date only) field for form inputs.

    Args:
        description: Human-readable description shown as label.
        prefilled_value: Optional pre-filled value for the UI form (date object or ISO 8601 date string).
            This is a display hint only — the field remains required and must be explicitly
            submitted. If invalid, no initial value will be set.

    Example:
        ```python
        from datetime import date

        class MyForm(FormInput):
            start_date: date = DateField(
                description="Start date",
                prefilled_value=date(2023, 1, 1),
            )
        ```
    """

    validated_initial: str | None = None
    if prefilled_value is not None:
        try:
            if isinstance(prefilled_value, str):
                prefilled_value = date.fromisoformat(prefilled_value)
            # datetime is a subclass of date, so .isoformat() would produce a full
            # datetime string — convert to a plain date first.
            if isinstance(prefilled_value, datetime):
                prefilled_value = prefilled_value.date()
            validated_initial = prefilled_value.isoformat()
        except (ValueError, TypeError):
            logger.warning(
                "DateField prefilled_value is not a valid date, ignoring",
                prefilled_value=prefilled_value,
            )
            validated_initial = None

    def _schema_extra(schema: dict[str, Any]) -> None:
        schema["type"] = "string"
        schema["format"] = "date"
        schema["description"] = description
        if validated_initial is not None:
            schema["default"] = validated_initial
        schema.pop("title", None)

    return Field(json_schema_extra=_schema_extra)


class FileWithMetadataValue(BaseModel):
    """Runtime value for a file upload field with metadata."""

    filename: str
    url: str
    content_type: str


class _FileFieldSchemaExtra:
    def __init__(self, description: str, multiple: bool, include_metadata: bool):
        self.description = description
        self.multiple = multiple
        self.include_metadata = include_metadata

    def __call__(self, schema: dict[str, Any]) -> None:
        if self.include_metadata:
            file_schema: dict[str, Any] = {
                "title": "FileWithMetadata",
                "type": "object",
                "properties": {
                    "filename": {"type": "string"},
                    "url": {"type": "string", "format": "uri"},
                    "content_type": {"type": "string"},
                },
                "required": ["filename", "url", "content_type"],
            }
            schema.clear()
            if self.multiple:
                schema["type"] = "array"
                schema["items"] = file_schema
                schema["description"] = self.description
            else:
                schema.update(file_schema)
                schema["description"] = self.description
        else:
            if self.multiple:
                schema["type"] = "array"
                schema["items"] = {"type": "string", "format": "uri", "title": "File"}
                schema["description"] = self.description
                schema.pop("title", None)
            else:
                schema["type"] = "string"
                schema["format"] = "uri"
                schema["title"] = "File"
                schema["description"] = self.description


def FileField(
    description: str,
    *,
    multiple: bool = False,
    include_metadata: bool = False,
) -> Any:
    """Create a file upload field for form inputs.

    Args:
        description: Human-readable description shown as label.
        multiple: If True, allows uploading multiple files.
        include_metadata: If True, the workflow receives structured metadata
            (filename, url, content_type) instead of plain URLs. Use
            ``FileWithMetadataValue`` as the type annotation when enabled.

    Example:
        ```python
        class MyForm(FormInput):
            # Plain URL fields
            document: str = FileField(description="Upload a document")
            attachments: list[str] = FileField(description="Upload files", multiple=True)

            # With metadata
            doc: FileWithMetadataValue = FileField(
                description="Upload a document", include_metadata=True
            )
            docs: list[FileWithMetadataValue] = FileField(
                description="Upload files", multiple=True, include_metadata=True
            )
        ```
    """
    return Field(json_schema_extra=_FileFieldSchemaExtra(description, multiple, include_metadata))


def SingleChoice(
    options: list[tuple[str, str]] | list[str],
    description: str | None = None,
    prefilled_value: str | None = None,
) -> Any:
    """Create a single choice (dropdown/select) field for form inputs.

    Args:
        options: List of options, either:
            - List of strings: ["value1", "value2"] - value is used as both value and label
            - List of tuples: [("value1", "Label 1"), ("value2", "Label 2")]
        description: Optional overall description for the field.
        prefilled_value: Optional pre-selected value for the UI form. This is a display hint
            only — the field remains required and must be explicitly submitted.

    Returns:
        FieldInfo that produces oneOf JSON schema.

    Example:
        ```python
        class MyForm(FormInput):
            priority: str = SingleChoice(
                options=[
                    ("low", "Low Priority"),
                    ("medium", "Medium Priority"),
                    ("high", "High Priority"),
                ],
                description="Select the priority level",
                prefilled_value="medium"
            )
        ```
    """
    return Field(json_schema_extra=_SingleChoiceSchemaExtra(options, description, prefilled_value))


def MultiChoice(
    options: list[tuple[str, str]] | list[str],
    description: str | None = None,
    prefilled_value: list[str] | None = None,
) -> Any:
    """Create a multi choice (multi-select) field for form inputs.

    Args:
        options: List of options, either:
            - List of strings: ["value1", "value2"] - value is used as both value and label
            - List of tuples: [("value1", "Label 1"), ("value2", "Label 2")]
        description: Optional overall description for the field.
        prefilled_value: Optional pre-selected values for the UI form. This is a display hint
            only — the field remains required and must be explicitly submitted.

    Returns:
        FieldInfo that produces array JSON schema with anyOf items.

    Example:
        ```python
        class MyForm(FormInput):
            tags: list[str] = MultiChoice(
                options=[
                    ("frontend", "Frontend"),
                    ("backend", "Backend"),
                    ("infra", "Infrastructure"),
                ],
                description="Select applicable tags",
                prefilled_value=["frontend"]
            )
        ```
    """
    return Field(json_schema_extra=_MultiChoiceSchemaExtra(options, description, prefilled_value))


class ConfirmationInputModel(BaseModel, Generic[ChoiceT]):
    model_config = ConfigDict(title="Confirmation", extra="forbid")
    choice: ChoiceT


def ConfirmationInput(
    options: list[tuple[ChoiceT, str]] | list[ChoiceT],
    description: str,
) -> type[ConfirmationInputModel[ChoiceT]]:
    """Create a ConfirmationInput schema for workflow confirmation dialogs.

    This creates a specialized input schema that renders as a confirmation UI
    in the workflow. The user must select one of the provided options.

    Args:
        options: List of (value, label) tuples for the confirmation options.
            Each tuple contains (value, label) where value is what you receive
            in the response and label is what the user sees.
        description: The description displayed to the user (mandatory).

    Returns:
        A ConfirmationInputModel class that can be used with wait_for_input().

    Example:
        ```python
        confirmation = await self.wait_for_input(
            ConfirmationInput(
                options=[
                    ("confirm", "Yes, proceed"),
                    ("cancel", "Cancel operation"),
                ],
                description="Do you want to continue with this action?"
            )
        )
        if confirmation.choice == "confirm":
            # proceed with action
            ...
        ```
    """
    if len(options) < 1:
        raise ValueError("Confirmation must have at least one option")

    schema_extra = _SingleChoiceSchemaExtra(options, description)

    class _ConfirmationInput(ConfirmationInputModel[ChoiceT]):
        choice: ChoiceT = Field(json_schema_extra=schema_extra)

        @model_validator(mode="after")
        def _validate_choice(self) -> Self:
            if self.choice not in schema_extra.allowed_values:
                raise ValueError(f"Invalid choice '{self.choice}'. Must be one of: {schema_extra.allowed_values}")
            return self

    return _ConfirmationInput


# Constants for first-class accept/decline support in the client
ACCEPT_OPTION_VALUE: Literal["accept"] = "accept"
DECLINE_OPTION_VALUE: Literal["decline"] = "decline"

AcceptChoice = Literal["accept"]
DeclineChoice = Literal["decline"]
AcceptDeclineChoice = Literal["accept", "decline"]


def is_accepted(confirmation: ConfirmationInputModel[ChoiceT]) -> bool:
    """Check if a confirmation result was accepted.

    Example:
        ```python
        confirmation = await self.wait_for_input(
            AcceptDeclineConfirmation(
                description="Do you want to proceed?",
            )
        )
        if is_accepted(confirmation):
            # proceed with action
            ...
        else:
            # user declined
            ...
        ```
    """
    return confirmation.choice == ACCEPT_OPTION_VALUE


@overload
def AcceptDeclineConfirmation(
    description: str,
    *,
    accept_label: str = "Accept",
    decline_label: None,
) -> type[ConfirmationInputModel[AcceptChoice]]: ...


@overload
def AcceptDeclineConfirmation(
    description: str,
    *,
    accept_label: str = "Accept",
    decline_label: str = "Decline",
) -> type[ConfirmationInputModel[AcceptDeclineChoice]]: ...


def AcceptDeclineConfirmation(
    description: str,
    *,
    accept_label: str = "Accept",
    decline_label: str | None = "Decline",
) -> type[ConfirmationInputModel[AcceptChoice]] | type[ConfirmationInputModel[AcceptDeclineChoice]]:
    """Create a confirmation dialog with accept/decline options that have keyboard hotkey support.

    This is a convenience wrapper around ConfirmationInput that uses special
    "accept" and "decline" values which the client recognizes for keyboard shortcuts.

    Args:
        description: The description displayed to the user (mandatory).
        accept_label: Label for the accept button. Defaults to "Accept".
        decline_label: Label for the decline button. Set to None for accept-only confirmation.
            Defaults to "Decline".

    Returns:
        A ConfirmationInputModel class that can be used with wait_for_input().
        The choice field will be "accept" or "decline".

    Example:
        ```python
        # Accept/Decline confirmation
        confirmation = await self.wait_for_input(
            AcceptDeclineConfirmation(
                description="Do you want to proceed with this action?",
                accept_label="Yes, proceed",
                decline_label="No, cancel",
            )
        )
        if is_accepted(confirmation):
            # proceed with action
            ...

        # Accept-only confirmation
        confirmation = await self.wait_for_input(
            AcceptDeclineConfirmation(
                description="Click to acknowledge and continue.",
                accept_label="I understand",
                decline_label=None,
            )
        )
        # User acknowledged, proceed...
        ```
    """
    if decline_label is None:
        options: list[tuple[AcceptChoice, str]] = [(ACCEPT_OPTION_VALUE, accept_label)]
        return ConfirmationInput(options=options, description=description)
    else:
        options_with_decline: list[tuple[AcceptDeclineChoice, str]] = [
            (DECLINE_OPTION_VALUE, decline_label),
            (ACCEPT_OPTION_VALUE, accept_label),
        ]
        return ConfirmationInput(options=options_with_decline, description=description)
