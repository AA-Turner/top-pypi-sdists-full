"""Central inference for a call that names no model.

Operator 2026-10-23: "if a call doesnt have a model then its obvious they want
execute_prompt". A /v1 call with no ``model`` is answered by execute_prompt's own
choosing stages, run in-process (no new rules here):

  INFER  the task: the caller's ``task``, else the route's task (the engine's
         TASK_ROUTES), else hugpy_engine.task_resolution.infer over the messages
         (image / audio parts -> their task), else text-generation;
  RANK   hugpy_engine.resolvers.model_resolver.resolve -> the head model and its
         ranked alternatives (explicit > operator binding > default > capability;
         bindings are core's /v1/task-bindings = the console's model preferences);
  PLACE  the first ranked model a worker can serve (relay.pick), so the call then
         runs exactly like one that named that model.

A call that names a model never comes here.
"""
from __future__ import annotations

import logging
from typing import Optional

from hugpy_core.relay.pick import NoWorker, pick

log = logging.getLogger(__name__)


def task_for_route(route: str) -> Optional[str]:
    """The task a /v1 task route serves: the FIRST task the engine maps to it."""
    from hugpy_engine.task_endpoints import TASK_ROUTES
    for task, (path, _kind) in TASK_ROUTES.items():
        if path == route:
            return task
    return None


def infer_task(messages=None, body: Optional[dict] = None) -> Optional[str]:
    """execute_prompt's INFER stage over the request (additive; never raises)."""
    try:
        from abstract_essentials import derive_media_type
        from hugpy_engine.resolvers.task_resolution import infer
        kwargs = dict(body or {})
        if messages is not None:
            kwargs["messages"] = messages
        return infer((), kwargs, media_type_fn=derive_media_type).get("task")
    except Exception:  # noqa: BLE001 — inference only ADDS a task
        log.debug("central: task inference skipped", exc_info=True)
        return None


def ranked(task: str) -> tuple[list[str], dict]:
    """execute_prompt's RANK stage: (model keys strongest first, {task, chosen_via})."""
    from hugpy_engine.dispatch.dispatch import _ordered_candidates
    from hugpy_engine.resolvers.model_resolver import resolve
    res = resolve({"task": task})
    return [mk for mk, _src in _ordered_candidates(res)], {"task": res.task, "chosen_via": res.chosen_via}


def choose(*, task: Optional[str] = None, route: Optional[str] = None, messages=None,
           body: Optional[dict] = None, pool: str = "", pin: Optional[str] = None,
           workers: Optional[list] = None) -> tuple[str, dict, dict]:
    """(model_key, worker, info) for a call that named no model. Raises NoWorker
    when no ranked model has a worker, ValueError when nothing can serve the task."""
    task = (task or (task_for_route(route) if route else None)
            or infer_task(messages, body) or "text-generation")
    keys, info = ranked(task)
    if not keys:
        raise ValueError(f"no model serves task {task!r}")
    refused = {}
    for key in keys:
        try:
            worker = pick(key, pool=pool, pin=pin, workers=workers, source="central")
        except NoWorker as exc:
            refused[key] = str(exc)
            continue
        info = {**info, "model_key": key, "candidates": keys, "refused": refused}
        _remember(info)
        return key, worker, info
    raise NoWorker(f"no worker can serve any model ranked for {task!r}: "
                   + "; ".join(f"{k}: {v}" for k, v in refused.items()))


def _remember(info: dict) -> None:
    """Expose the choice on the response (X-Hugpy-Model / X-Hugpy-Model-Chosen-Via)."""
    try:
        from flask import g
        g.model_chosen = info
    except Exception:  # noqa: BLE001 — outside a request: nothing to expose
        pass
