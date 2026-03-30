from typing import Annotated, Dict, List, Literal, Optional, Union

import flask
from pydantic import Discriminator, Field, Tag

from abstra_internals.repositories.tasks import TaskDTO
from abstra_internals.utils.dict import filter_non_string_values
from abstra_internals.utils.serializable import Serializable


class Request(Serializable):
    query_params: Dict[str, str]
    headers: Dict[str, str]
    method: str
    body: str


class Response(Serializable):
    headers: Dict[str, str]
    status: int
    body: str


class ExecutionMock(Serializable):
    test_pending_tasks: List[TaskDTO] = Field(default_factory=list)


class HookExecutionMock(ExecutionMock):
    test_request: Optional[Request] = None


class FormExecutionMock(ExecutionMock):
    test_answers: List[Union[str, None]] = Field(default_factory=list)


class ScriptExecutionMock(ExecutionMock):
    test_trigger_task: Optional[TaskDTO] = None


class JobExecutionMock(ExecutionMock):
    pass


class PageExecutionMock(ExecutionMock):
    pass


class CodeSnippetExecutionMock(ExecutionMock):
    pass


class HookContext(Serializable):
    type: Literal["hook"] = "hook"
    request: Request
    response: Response
    sent_tasks: List[str] = Field(default_factory=list)
    legacy_thread_data: dict = Field(default_factory=dict)
    mock_execution: HookExecutionMock = Field(default_factory=HookExecutionMock)


class FormContext(Serializable):
    type: Literal["form"] = "form"
    request: Request
    sent_tasks: List[str] = Field(default_factory=list)
    legacy_thread_data: dict = Field(default_factory=dict)
    mock_execution: FormExecutionMock = Field(default_factory=FormExecutionMock)


class ScriptContext(Serializable):
    type: Literal["script"] = "script"
    task_id: str
    sent_tasks: List[str] = Field(default_factory=list)
    legacy_thread_data: dict = Field(default_factory=dict)
    mock_execution: ScriptExecutionMock = Field(default_factory=ScriptExecutionMock)


class JobContext(Serializable):
    type: Literal["job"] = "job"
    sent_tasks: List[str] = Field(default_factory=list)
    legacy_thread_data: dict = Field(default_factory=dict)
    mock_execution: JobExecutionMock = Field(default_factory=JobExecutionMock)


class PageContext(Serializable):
    type: Literal["page"] = "page"
    request: Request
    response: Response
    page_path: str = ""
    page_execution_id: Optional[str] = None  # execution_id of the parent GET render
    sent_tasks: List[str] = Field(default_factory=list)
    legacy_thread_data: dict = Field(default_factory=dict)
    mock_execution: PageExecutionMock = Field(default_factory=PageExecutionMock)


class CodeSnippetContext(Serializable):
    type: Literal["code_snippet"] = "code_snippet"
    mock_execution: CodeSnippetExecutionMock = Field(
        default_factory=CodeSnippetExecutionMock
    )


def _context_discriminator(v):
    if isinstance(v, dict):
        t = v.get("type")
        if t is not None:
            return t
        # Legacy messages without type field (pages never existed without it)
        if "taskId" in v or "task_id" in v:
            return "script"
        if "request" in v and "response" in v:
            return "hook"
        if "request" in v:
            return "form"
        if "sentTasks" in v or "sent_tasks" in v:
            return "job"
        return "code_snippet"
    return getattr(v, "type", None)


ClientContext = Annotated[
    Union[
        Annotated[HookContext, Tag("hook")],
        Annotated[FormContext, Tag("form")],
        Annotated[ScriptContext, Tag("script")],
        Annotated[JobContext, Tag("job")],
        Annotated[PageContext, Tag("page")],
        Annotated[CodeSnippetContext, Tag("code_snippet")],
    ],
    Discriminator(_context_discriminator),
]


def extract_flask_request(request: flask.Request) -> Request:
    return Request(
        headers=filter_non_string_values(dict(request.headers)),
        body=request.get_data(as_text=True),
        query_params={**request.args},
        method=request.method,
    )
