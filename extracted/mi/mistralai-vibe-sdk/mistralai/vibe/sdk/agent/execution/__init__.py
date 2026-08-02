"""Agent execution context."""

from importlib import import_module
from typing import TYPE_CHECKING, Any

__all__ = [
    "AppendHistoryScope",
    "CallbackBridge",
    "CallbackResultReceived",
    "CallCallback",
    "DirectStateSink",
    "DownstreamWriter",
    "EffectExecutor",
    "EffectRegistry",
    "Emit",
    "ExecutionLoop",
    "FailSubTask",
    "FixedHistoryScope",
    "HistoryScope",
    "LocalCallbackBridge",
    "SpawnSubTask",
    "StateModule",
    "StateSink",
    "StreamScopeTracker",
    "SubTaskAction",
    "SubTaskCallRequest",
    "SubTaskCompleted",
    "SubTaskEffect",
    "resolve_callback_request",
    "sub_task_reducer",
]

if TYPE_CHECKING:
    from mistralai.vibe.sdk.agent.execution.loop import (
        AppendHistoryScope,
        CallbackBridge,
        DirectStateSink,
        DownstreamWriter,
        EffectExecutor,
        EffectRegistry,
        Emit,
        ExecutionLoop,
        FixedHistoryScope,
        HistoryScope,
        LocalCallbackBridge,
        StateModule,
        StateSink,
        StreamScopeTracker,
    )
    from mistralai.vibe.sdk.agent.execution.sub_task import (
        CallbackResultReceived,
        CallCallback,
        FailSubTask,
        SpawnSubTask,
        SubTaskAction,
        SubTaskCallRequest,
        SubTaskCompleted,
        SubTaskEffect,
        resolve_callback_request,
        sub_task_reducer,
    )

_LAZY_EXPORTS = {
    "AppendHistoryScope": "mistralai.vibe.sdk.agent.execution.loop",
    "CallbackBridge": "mistralai.vibe.sdk.agent.execution.loop",
    "CallbackResultReceived": "mistralai.vibe.sdk.agent.execution.sub_task",
    "CallCallback": "mistralai.vibe.sdk.agent.execution.sub_task",
    "DirectStateSink": "mistralai.vibe.sdk.agent.execution.loop",
    "DownstreamWriter": "mistralai.vibe.sdk.agent.execution.loop",
    "EffectExecutor": "mistralai.vibe.sdk.agent.execution.loop",
    "EffectRegistry": "mistralai.vibe.sdk.agent.execution.loop",
    "Emit": "mistralai.vibe.sdk.agent.execution.loop",
    "ExecutionLoop": "mistralai.vibe.sdk.agent.execution.loop",
    "FailSubTask": "mistralai.vibe.sdk.agent.execution.sub_task",
    "FixedHistoryScope": "mistralai.vibe.sdk.agent.execution.loop",
    "HistoryScope": "mistralai.vibe.sdk.agent.execution.loop",
    "LocalCallbackBridge": "mistralai.vibe.sdk.agent.execution.loop",
    "SpawnSubTask": "mistralai.vibe.sdk.agent.execution.sub_task",
    "StateModule": "mistralai.vibe.sdk.agent.execution.loop",
    "StateSink": "mistralai.vibe.sdk.agent.execution.loop",
    "StreamScopeTracker": "mistralai.vibe.sdk.agent.execution.loop",
    "SubTaskAction": "mistralai.vibe.sdk.agent.execution.sub_task",
    "SubTaskCallRequest": "mistralai.vibe.sdk.agent.execution.sub_task",
    "SubTaskCompleted": "mistralai.vibe.sdk.agent.execution.sub_task",
    "SubTaskEffect": "mistralai.vibe.sdk.agent.execution.sub_task",
    "resolve_callback_request": "mistralai.vibe.sdk.agent.execution.sub_task",
    "sub_task_reducer": "mistralai.vibe.sdk.agent.execution.sub_task",
}


def __getattr__(name: str) -> Any:
    if name not in _LAZY_EXPORTS:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

    value = getattr(import_module(_LAZY_EXPORTS[name]), name)
    globals()[name] = value
    return value
