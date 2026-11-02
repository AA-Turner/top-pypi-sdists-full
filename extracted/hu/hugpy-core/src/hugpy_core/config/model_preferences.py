"""Ordered model pickers and public choices, persisted in Core policies."""
from __future__ import annotations

import copy
import re

CHAT_MODELS = (
    "Qwen3.5-0.8B",
    "flux2-klein-9b-uncensored-text-encoder",
    "Qwen3-Coder-Next-Q4_K_M",
)
TASK_DEFAULTS = {
    "text-generation": CHAT_MODELS[0],
    "image-text-to-text": "Qwen2.5-VL-3B-Instruct",
    "text-to-image": "sd-turbo", "image-to-image": "sd-turbo",
    "automatic-speech-recognition": "whisper-tiny",
    "feature-extraction": "all-MiniLM-L6-v2",
    "sentence-similarity": "all-MiniLM-L6-v2",
    "keyword-extraction": CHAT_MODELS[0],
    "depth-estimation": "Depth-Anything-V2-Small-hf",
    "object-detection": "detr-resnet-50",
    "image-classification": "vit-base-patch16-224",
    "image-segmentation": "segformer-b0-finetuned-ade-512-512",
}


def defaults():
    def tasks(names):
        return {task: {"preferred": list(CHAT_MODELS) if task == "text-generation" else [TASK_DEFAULTS[task]],
                       "public": list(CHAT_MODELS) if task == "text-generation" else [TASK_DEFAULTS[task]],
                       "show_more": False} for task in names}
    return {"media": tasks(TASK_DEFAULTS),
            "video": tasks(("text-to-image", "image-to-image", "text-generation", "image-text-to-text"))}


def valid(value):
    if not isinstance(value, dict) or set(value) - {"media", "video"}:
        return False
    for tasks in value.values():
        if not isinstance(tasks, dict) or len(tasks) > 64:
            return False
        for task, rule in tasks.items():
            if not isinstance(task, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,99}", task):
                return False
            if not isinstance(rule, dict) or set(rule) != {"preferred", "public", "show_more"}:
                return False
            if not isinstance(rule["show_more"], bool):
                return False
            for name in ("preferred", "public"):
                items = rule[name]
                if (not isinstance(items, list) or len(items) > 200
                        or any(not isinstance(key, str) or not key.strip() or len(key) > 512 for key in items)
                        or len(set(items)) != len(items)):
                    return False
            if not set(rule["public"]).issubset(rule["preferred"]):
                return False
    return True


_UNSET = object()


def read(value=_UNSET):
    if value is _UNSET:
        from .settings import _conn
        with _conn() as conn, conn.cursor() as cur:
            cur.execute("SELECT value FROM settings_policies WHERE key='model_preferences'")
            row = cur.fetchone()
        value = row["value"] if row else {}
    result = defaults()
    if value is not None:
        if not valid(value):
            raise ValueError("Invalid stored model preferences")
        for surface, tasks in value.items():
            result[surface].update(copy.deepcopy(tasks))
    return result


def supports(row, task):
    marker = row.get("metadata") or {}
    tasks = row.get("tasks") or marker.get("tasks") or [row.get("primary_task") or row.get("task")]
    if row.get("adapter") or marker.get("adapter") or row.get("serveable") is False or marker.get("serveable") is False:
        return False
    return task in tasks or (task in ("text-generation", "keyword-extraction")
                             and any(t in tasks for t in ("text-generation", "image-text-to-text")))


def public_models(surface, task, *, preferences=None, rows=None):
    preferences = read() if preferences is None else preferences
    rule = preferences.get(surface, {}).get(task, {})
    selected = list(rule.get("public") or [])
    if rule.get("show_more"):
        if rows is None:
            from hugpy_core.web.native_fleet import models
            rows = models()
        selected.extend(sorted({row.get("model_key") or row.get("id") for row in rows
                                if supports(row, task) and row.get("available") is not False}
                               - set(rule.get("preferred") or []) - set(selected)))
    return selected


def projection(preferences=None, *, public=False, rows=None):
    preferences = read() if preferences is None else preferences
    return {surface: {task: {"preferred": list(rule["public"] if public else rule["preferred"]),
                            "show_more": rule["show_more"] if public else True,
                            **({"allowed": public_models(surface, task, preferences=preferences, rows=rows)} if public else {})}
                      for task, rule in tasks.items()}
            for surface, tasks in preferences.items()}


def public_defaults(surface="media", *, preferences=None):
    preferences = read() if preferences is None else preferences
    rows = None
    if any(rule.get("show_more") for rule in preferences.get(surface, {}).values()):
        from hugpy_core.web.native_fleet import models
        rows = models()
    return {task: keys[0] for task in preferences.get(surface, {})
            if (keys := public_models(surface, task, preferences=preferences, rows=rows))}


def public_catalog(surface="media", *, preferences=None, rows=None):
    preferences = read() if preferences is None else preferences
    if rows is None and any(rule.get("show_more") for rule in preferences.get(surface, {}).values()):
        from hugpy_core.web.native_fleet import models
        rows = models()
    return {key for task in preferences.get(surface, {})
            for key in public_models(surface, task, preferences=preferences, rows=rows)}
