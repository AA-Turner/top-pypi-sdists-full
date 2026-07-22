"""A large, diverse corpus of wire dicts (camelCase, as produced by the wire) used
by ``serializable_diff_test.py`` to prove the dataclass Serializable reproduces the
ORIGINAL pydantic behaviour byte-for-byte.

Pure data: no pydantic, no model imports, so this file is stable across the
pydantic->dataclass migration. Each case is ``(class_name, wire_dict)``; the test
maps ``class_name`` to the real class. Expected outputs are frozen in
``serializable_diff_expected.json`` (generated from the pydantic code — see the
generator in the PR description / scratchpad).

Coverage goals: every class; every context subtype (incl. legacy dicts WITHOUT a
``type`` field, to exercise the discriminator fallbacks); optional fields present
and absent; empty and populated collections; unicode; nested edge cases; every
control message; datetimes with and without ``updatedAt``.
"""

from typing import Any, Dict, List, Tuple

# --- reusable building blocks (camelCase wire form) -------------------------------

_REQ_MIN = {"method": "GET", "queryParams": {}, "headers": {}, "body": ""}
_REQ_FULL = {
    "method": "POST",
    "queryParams": {"c": "3", "q": "ção"},
    "headers": {"Auth": "secret", "X-Trace": "áé"},
    "body": '{"a": 1, "ç": "ê"}',
}
_RESP_MIN = {"headers": {}, "status": 200, "body": ""}
_RESP_FULL = {"headers": {"X": "y"}, "status": 404, "body": "not found — ção"}

_TEV = {"at": "2024-01-02T03:04:05+00:00", "byExecutionId": "e1", "byStageId": "s1"}
_TEV_NULLS = {
    "at": "2024-01-02T03:04:05+00:00",
    "byExecutionId": None,
    "byStageId": None,
}


def _task(tid: str = "t1", locked=None, completed=None) -> Dict[str, Any]:
    return {
        "id": tid,
        "type": "my_task",
        "payload": {"k": "v", "n": 1, "nested": {"deep": [1, 2, 3]}},
        "status": "pending",
        "targetStageId": "stage-x",
        "created": _TEV,
        "locked": locked,
        "completed": completed,
    }


_MOCK_HOOK = {"testPendingTasks": [], "testRequest": None}
_MOCK_HOOK_FULL = {"testPendingTasks": [_task("mp1")], "testRequest": _REQ_FULL}
_MOCK_FORM = {"testPendingTasks": [], "testAnswers": []}
_MOCK_FORM_FULL = {"testPendingTasks": [_task("mp2")], "testAnswers": ["a", None, "b"]}
_MOCK_SCRIPT = {"testPendingTasks": [], "testTriggerTask": None}
_MOCK_SCRIPT_FULL = {"testPendingTasks": [_task("mp3")], "testTriggerTask": _task("tt")}
_MOCK_BARE = {"testPendingTasks": []}


def _hook_ctx(req=_REQ_MIN, resp=_RESP_MIN, tasks=None, mock=None):
    return {
        "type": "hook",
        "request": req,
        "response": resp,
        "sentTasks": tasks or [],
        "legacyThreadData": {},
        "mockExecution": mock or _MOCK_HOOK,
    }


def _form_ctx(req=_REQ_MIN, tasks=None, mock=None, legacy=None):
    return {
        "type": "form",
        "request": req,
        "sentTasks": tasks or [],
        "legacyThreadData": legacy or {},
        "mockExecution": mock or _MOCK_FORM,
    }


def _script_ctx(task_id="task-1", tasks=None, mock=None):
    return {
        "type": "script",
        "taskId": task_id,
        "sentTasks": tasks or [],
        "legacyThreadData": {},
        "mockExecution": mock or _MOCK_SCRIPT,
    }


def _job_ctx(tasks=None):
    return {
        "type": "job",
        "sentTasks": tasks or [],
        "legacyThreadData": {},
        "mockExecution": _MOCK_BARE,
    }


def _page_ctx(req=_REQ_MIN, resp=_RESP_MIN, path="", pexec=None):
    return {
        "type": "page",
        "request": req,
        "response": resp,
        "pagePath": path,
        "pageExecutionId": pexec,
        "sentTasks": [],
        "legacyThreadData": {},
        "mockExecution": _MOCK_BARE,
    }


def _snippet_ctx():
    return {"type": "code_snippet", "mockExecution": _MOCK_BARE}


_ALL_CONTEXTS = [
    _hook_ctx(),
    _hook_ctx(_REQ_FULL, _RESP_FULL, ["t1", "t2"], _MOCK_HOOK_FULL),
    _form_ctx(),
    _form_ctx(_REQ_FULL, ["t9"], _MOCK_FORM_FULL, {"k": "v"}),
    _script_ctx(),
    _script_ctx("task-42", ["a"], _MOCK_SCRIPT_FULL),
    _job_ctx(),
    _job_ctx(["j1", "j2"]),
    _page_ctx(),
    _page_ctx(_REQ_FULL, _RESP_FULL, "/p", "parent-exec"),
    _snippet_ctx(),
]

# Legacy context dicts (NO "type" field) — must reconstruct via the discriminator
# fallbacks (task_id -> script, request+response -> hook, request -> form,
# sentTasks -> job, else -> code_snippet). Both camelCase and snake_case keys.
_LEGACY_CONTEXTS = [
    {
        "request": _REQ_MIN,
        "response": _RESP_MIN,
        "sentTasks": [],
        "legacyThreadData": {},
        "mockExecution": _MOCK_HOOK,
    },  # hook
    {
        "request": _REQ_MIN,
        "sentTasks": [],
        "legacyThreadData": {},
        "mockExecution": _MOCK_FORM,
    },  # form
    {
        "taskId": "t-legacy",
        "sentTasks": [],
        "legacyThreadData": {},
        "mockExecution": _MOCK_SCRIPT,
    },  # script (camel)
    {
        "task_id": "t-legacy2",
        "sent_tasks": [],
        "legacy_thread_data": {},
        "mock_execution": _MOCK_BARE,
    },  # script (snake)
    {"sentTasks": ["x"], "legacyThreadData": {}, "mockExecution": _MOCK_BARE},  # job
    {"mockExecution": _MOCK_BARE},  # code_snippet
]

_DT1 = "2024-01-02T03:04:05.000000Z"
_DT2 = "2024-06-07T08:09:10.123456Z"


def wire_cases() -> List[Tuple[str, Dict[str, Any]]]:
    cases: List[Tuple[str, Dict[str, Any]]] = []

    cases += [("Request", _REQ_MIN), ("Request", _REQ_FULL)]
    cases += [("Response", _RESP_MIN), ("Response", _RESP_FULL)]

    cases += [
        ("HookExecutionMock", _MOCK_HOOK),
        ("HookExecutionMock", _MOCK_HOOK_FULL),
        ("FormExecutionMock", _MOCK_FORM),
        ("FormExecutionMock", _MOCK_FORM_FULL),
        ("ScriptExecutionMock", _MOCK_SCRIPT),
        ("ScriptExecutionMock", _MOCK_SCRIPT_FULL),
        ("JobExecutionMock", _MOCK_BARE),
        ("PageExecutionMock", _MOCK_BARE),
        ("CodeSnippetExecutionMock", _MOCK_BARE),
    ]

    ctx_class = {
        "hook": "HookContext",
        "form": "FormContext",
        "script": "ScriptContext",
        "job": "JobContext",
        "page": "PageContext",
        "code_snippet": "CodeSnippetContext",
    }
    for ctx in _ALL_CONTEXTS:
        cases.append((ctx_class[ctx["type"]], ctx))

    cases += [
        ("TaskEventDetails", _TEV),
        ("TaskEventDetails", _TEV_NULLS),
        ("TaskDTO", _task("only-created")),
        ("TaskDTO", _task("locked", locked=_TEV)),
        ("TaskDTO", _task("done", locked=_TEV, completed=_TEV_NULLS)),
        ("ExecutionTasksResponse", {"triggerTask": None, "sentTasks": []}),
        (
            "ExecutionTasksResponse",
            {"triggerTask": _task("trig"), "sentTasks": [_task("s1"), _task("s2")]},
        ),
    ]

    # PreExecution around every context (typed + legacy), optionals present/absent.
    for i, ctx in enumerate(_ALL_CONTEXTS + _LEGACY_CONTEXTS):
        if i % 2 == 0:
            cases.append(
                (
                    "PreExecution",
                    {
                        "stageId": f"s{i}",
                        "context": ctx,
                        "executionId": f"e{i}",
                        "userJwt": "jwt",
                        "sendQueue": "sq",
                        "recvQueue": "rq",
                        "queueExpireMs": 1000,
                    },
                )
            )
        else:
            cases.append(
                (
                    "PreExecution",
                    {
                        "stageId": f"s{i}",
                        "context": ctx,
                        "executionId": f"e{i}",
                    },
                )
            )

    # Control messages.
    cases += [
        ("StopExecutionMessage", {"type": "stop", "payload": {"executionId": "e1"}}),
        (
            "StopExecutionMessage",
            {"type": "stop", "correlationId": "c1", "payload": {"executionId": "e2"}},
        ),
        ("StopAllExecutionsMessage", {"type": "stop_all"}),
        ("StopAllExecutionsMessage", {"type": "stop_all", "correlationId": "c9"}),
        (
            "RunSnippetMessage",
            {"type": "run_snippet", "payload": {"code": "print(1)", "title": "T"}},
        ),
        (
            "RunSnippetSandboxedMessage",
            {
                "type": "run_snippet_sandboxed",
                "payload": {"code": "x=1", "title": "Debug Snippet"},
                "queueExpireMs": 5000,
                "timeoutMs": 1000,
            },
        ),
        ("PingMessage", {"type": "ping"}),
        ("PingMessage", {"type": "ping", "correlationId": "p1"}),
    ]

    # Execution around every context, updatedAt present/None, both datetimes.
    for i, ctx in enumerate(_ALL_CONTEXTS):
        cases.append(
            (
                "Execution",
                {
                    "id": f"exec-{i}",
                    "stageId": f"stage-{i}",
                    "status": ["running", "failed", "finished", "abandoned"][i % 4],
                    "pid": 1000 + i,
                    "workerId": f"w{i}",
                    "createdAt": _DT1,
                    "updatedAt": None if i % 2 else _DT2,
                    "context": ctx,
                },
            )
        )

    return cases
