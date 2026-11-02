"""hugpy_core /prompt: the whole dispatch surface over one verb.

    POST /prompt        {"task": "text-generation", "prompt": "..."}  (or model_key,
                         messages, file/images, generation params — the execute_prompt
                         kwargs surface)
    GET  /prompt/tasks  -> {"tasks": [...], "defaults": {task: model_key}}

Hosted calls enter Core's router directly. Model selection remains in Core's
ranked resolver; only the selected worker is contacted over the network."""
from __future__ import annotations

import inspect
import logging

logger = logging.getLogger("hugpy_core")



def _result_payload(result) -> dict:
    """A TaskResult (pydantic) / dict / str -> a JSON-able dict."""
    if result is None:
        return {"ok": False, "error": "no result"}
    if hasattr(result, "model_dump"):
        return result.model_dump()
    if isinstance(result, dict):
        return dict(result)
    return {"text": str(result)}


def prompt_execute(**body):
    # Underscore-prefixed keys are internal routing controls; never client-set.
    kwargs = {k: v for k, v in body.items()
              if not k.startswith("_") and v is not None}
    if not kwargs:
        return {"ok": False, "error": "empty request body"}

    from hugpy_core.relay.internal import execute_prompt

    try:
        result = execute_prompt(caller="prompt", **kwargs)
        if inspect.isawaitable(result):   # defensive: execute_prompt is sync here
            from hugpy_platform.async_runtime import await_sync
            result = await_sync(result)
    except (KeyError, ValueError, TypeError, FileNotFoundError) as exc:
        # resolve()/builder validation — the caller's to fix.
        return {"ok": False, "error": str(exc).strip("'\"")}
    except Exception as exc:  # noqa: BLE001
        logger.exception("execute_prompt failed")
        return {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    payload = _result_payload(result)
    payload.setdefault("ok", not payload.get("error"))
    return payload


def prompt_tasks(surface="media"):
    """Live tasks + the operator's task bindings (settings_policies
    'task_bindings'): the model a task-only call is sent to. No constants."""
    from hugpy_core.relay.inference_catalog import picker_models
    from hugpy_core.config.settings import task_bindings
    return {
        "tasks": sorted({task for row in picker_models() for task in row.get("tasks", [])}),
        "defaults": task_bindings(surface="video" if surface == "video" else "media"),
    }
