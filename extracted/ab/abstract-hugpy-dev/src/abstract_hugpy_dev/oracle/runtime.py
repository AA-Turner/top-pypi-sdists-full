"""Oracle runtime (k91): execute a resolved route through the EXISTING dispatch.

No new inference machinery. Model tasks go through the SAME two functions the
/ml amenity routes use — ``ml_routes.normalize_ml_kwargs`` (the request
normalization extracted from ``_run_ml`` for exactly this reuse) and
``execute_prompt`` (managers/dispatch, awaited via the shared runtime like
``ml_routes._await_sync``). The two deterministic amenities keep their thin
local handlers (``media_extract.extract_document`` / ``assess_url``), again the
same ones ``_run_ml`` branches to. What THIS module adds is the wrapper the
operator ruled on: timing, one retry on WORKER_UNAVAILABLE, failure
classification, artifact extraction + sha256 — all landing in an
``ExecutionReceipt`` on every call, success or not.

Artifacts come back as plain dicts (``{kind, uri, sha256, ...}``) carrying the
inline payload (``text`` / ``data``) when the result is not file-backed —
that dict form is what the scorecard checks and the route returns; the receipt
carries the same set as typed ``ArtifactRef``s.

Provider seams (``_dispatch`` / ``_normalized_kwargs`` / ``_extract_document``
/ ``_assess_url``) are module-level and lazy so tests monkeypatch them and no
GPU/network/worker is touched.

No pathlib; os.path only (project discipline).
"""

from __future__ import annotations

import hashlib
import json
import os
import time
from datetime import datetime, timezone
from typing import Any, Mapping

from .contracts import ArtifactKind, ArtifactRef, ExecutionReceipt, FailureClass, GoalSpec
from .router import RouteDecision

# ---------------------------------------------------------------------------
# Provider seams — the existing machinery, lazily bound.
# ---------------------------------------------------------------------------


def _normalized_kwargs(task: str, body: dict[str, Any]) -> dict[str, Any]:
    """The /ml normalization, verbatim (model fold, vision b64 fold, pool)."""
    from abstract_hugpy_dev.flask_app.app.routes.ml_routes import normalize_ml_kwargs
    return normalize_ml_kwargs(task, body)


def _dispatch(kwargs: dict[str, Any]) -> Any:
    """The single inference front door: dispatch.execute_prompt, driven to a
    concrete result on the shared loop exactly like ml_routes._await_sync."""
    from abstract_hugpy_dev.flask_app.app.functions.imports import execute_prompt
    from abstract_hugpy_dev.flask_app.app.routes.ml_routes import _await_sync
    return _await_sync(execute_prompt(**kwargs))


def _extract_document(path: str) -> dict[str, Any]:
    from abstract_hugpy_dev.flask_app.app.functions.media_extract import (
        extract_document)
    return extract_document(path)


def _assess_url(url: str) -> dict[str, Any]:
    from abstract_hugpy_dev.flask_app.app.functions.media_extract import assess_url
    return assess_url(url)


# ---------------------------------------------------------------------------
# Request building — goal + route -> the amenity-shaped body.
# ---------------------------------------------------------------------------


class GoalShapeError(ValueError):
    """The goal cannot feed this capability (missing required input) — a typed
    400 at the route, raised BEFORE any dispatch."""


def _refs(goal: GoalSpec, *kinds: str) -> list[str]:
    return [i.ref for i in goal.inputs if i.kind.value in kinds]


def build_request_body(goal: GoalSpec, route: RouteDecision) -> dict[str, Any]:
    """The pre-normalization body for ``route.capability`` — the same keys a
    caller of the matching /ml amenity would send, derived from typed inputs.
    Raises GoalShapeError when a required input is absent."""
    cap = route.capability
    prompt = goal.objective
    texts = _refs(goal, "text")
    media = _refs(goal, "image", "audio", "video")
    file = media[0] if media else None

    def need_file(kind: str) -> str:
        if file is None:
            raise GoalShapeError(
                f"{cap} needs a {kind} input (inputs: [{{kind: '{kind}', "
                f"uri: ...}}]); none was supplied")
        return file

    if cap == "text.chat":
        body: dict[str, Any] = {"prompt": prompt}
        if texts:
            body["prompt"] = prompt + "\n\n" + "\n\n".join(texts)
    elif cap in ("text.summarize", "text.keywords"):
        body = {"text": "\n\n".join(texts) if texts else prompt}
    elif cap == "text.embed":
        body = {"texts": texts or [prompt]}
    elif cap == "text.similarity":
        if len(texts) < 2:
            raise GoalShapeError(
                "text.similarity needs >=2 text inputs (the first is compared "
                f"against the rest); got {len(texts)}")
        body = {"texts": [texts[0]], "other_texts": texts[1:]}
    elif cap == "audio.transcribe":
        body = {"file": need_file("audio")}
    elif cap == "image.understand":
        body = {"file": need_file("image"), "prompt": prompt}
    elif cap == "image.generate":
        body = {"prompt": prompt}
    elif cap == "image.transform":
        body = {"prompt": prompt, "image_path": need_file("image")}
    elif cap in ("image.depth", "image.detect", "image.classify", "image.segment"):
        body = {"image_path": need_file("image")}
    elif cap == "doc.extract":
        paths = [r for r in texts + _refs(goal, "url") if os.path.sep in r] + media
        if not paths:
            raise GoalShapeError(
                "doc.extract needs a document input carrying a server file path")
        body = {"file": paths[0]}
    elif cap == "web.fetch":
        urls = _refs(goal, "url")
        if not urls:
            raise GoalShapeError("web.fetch needs a url input")
        body = {"url": urls[0]}
    else:
        raise GoalShapeError(f"no request builder for capability {cap!r}")

    if route.model_id:
        body["model_key"] = route.model_id
    return body


# ---------------------------------------------------------------------------
# Failure classification + artifact extraction.
# ---------------------------------------------------------------------------

_WORKER_MARKERS = ("worker", "connection refused", "connection reset",
                   "unreachable", "unavailable", "no route to host",
                   "name or service not known", "bad gateway", "502", "503")
_TIMEOUT_MARKERS = ("timed out", "timeout", "deadline")


def classify_failure(exc: BaseException) -> FailureClass:
    """WHERE the execution died, from the exception the dispatch path raised.
    Deliberately string-tolerant: the dispatch surface raises requests/OS/
    runner exceptions from several layers and this must never re-crash."""
    msg = f"{type(exc).__name__}: {exc}".lower()
    if isinstance(exc, TimeoutError) or any(m in msg for m in _TIMEOUT_MARKERS):
        return FailureClass.TIMEOUT
    if isinstance(exc, ConnectionError) or any(m in msg for m in _WORKER_MARKERS):
        return FailureClass.WORKER_UNAVAILABLE
    return FailureClass.RUNNER_ERROR


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _sha256_file(path: str) -> str | None:
    try:
        h = hashlib.sha256()
        with open(path, "rb") as fh:
            for chunk in iter(lambda: fh.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()
    except OSError:
        return None


def _inline_text_artifact(text: str) -> dict[str, Any]:
    digest = _sha256_bytes(text.encode("utf-8"))
    return {"kind": ArtifactKind.TEXT.value, "uri": f"inline:text/{digest[:16]}",
            "sha256": digest, "text": text}


def _inline_data_artifact(kind: ArtifactKind, data: Any) -> dict[str, Any]:
    canon = json.dumps(data, sort_keys=True, separators=(",", ":"), default=str)
    digest = _sha256_bytes(canon.encode("utf-8"))
    return {"kind": kind.value, "uri": f"inline:{kind.value}/{digest[:16]}",
            "sha256": digest, "data": data}


def _file_artifact(kind: ArtifactKind, path: str, **extra: Any) -> dict[str, Any]:
    return {"kind": kind.value, "uri": path, "sha256": _sha256_file(path), **extra}


def _result_payload(result: Any) -> dict[str, Any]:
    """Result object -> plain dict, same ladder as ml_routes._result_payload."""
    if isinstance(result, dict):
        return result
    for attr in ("model_dump", "to_dict", "dict"):
        fn = getattr(result, attr, None)
        if callable(fn):
            try:
                return fn()
            except TypeError:
                continue
    return {"text": str(result)}


def extract_artifacts(capability: str, payload: dict[str, Any]) -> list[dict[str, Any]]:
    """The capability-shaped read of a result payload. An empty/blank result
    STILL yields its (empty) artifact where the shape allows — the scorecard's
    EMPTY_OUTPUT check needs to see it, not infer it from absence."""
    arts: list[dict[str, Any]] = []

    if capability == "text.embed":
        arts.append(_inline_data_artifact(ArtifactKind.EMBEDDING,
                                          payload.get("embeddings") or []))
        return arts
    if capability == "text.similarity":
        arts.append(_inline_data_artifact(ArtifactKind.JSON,
                                          {"similarities": payload.get("similarities") or []}))
        return arts
    if capability == "text.keywords":
        keys = {k: payload[k] for k in ("primary", "secondary", "combined",
                                        "hashtags", "meta_keywords")
                if payload.get(k)}
        arts.append(_inline_data_artifact(ArtifactKind.JSON, keys))
        return arts
    if capability in ("image.detect", "image.classify"):
        arts.append(_inline_data_artifact(ArtifactKind.JSON,
                                          {"items": payload.get("items") or []}))
        return arts

    # File-backed images (generate/transform/depth/segment carry GeneratedImage
    # rows; segment/depth may also carry structured items).
    for img in payload.get("images") or ():
        if isinstance(img, dict) and img.get("path"):
            arts.append(_file_artifact(
                ArtifactKind.IMAGE, img["path"],
                width=img.get("width"), height=img.get("height")))
    if capability == "image.segment" and payload.get("items"):
        arts.append(_inline_data_artifact(ArtifactKind.JSON,
                                          {"items": payload["items"]}))
    if arts:
        return arts

    # Text-producing capabilities (chat/summarize/understand/transcribe/
    # doc.extract/web.fetch) — inline text, even when blank.
    text = payload.get("text")
    if text is None:
        text = payload.get("content") or ""
    arts.append(_inline_text_artifact(str(text)))
    return arts


# ---------------------------------------------------------------------------
# execute_route — the wrapper the receipt is made of.
# ---------------------------------------------------------------------------

_MAX_RECEIPT_VALUE = 2048  # chars per request field on the receipt


def _receipt_request(kwargs: dict[str, Any]) -> dict[str, Any]:
    """JSON-safe, size-bounded copy of the dispatched request for the receipt."""
    out: dict[str, Any] = {}
    for k, v in kwargs.items():
        try:
            encoded = json.dumps(v)
        except (TypeError, ValueError):
            v, encoded = repr(v), json.dumps(repr(v))
        if len(encoded) > _MAX_RECEIPT_VALUE:
            v = f"<{len(encoded)} json chars elided>"
        out[k] = v
    return out


def _utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def execute_route(goal: GoalSpec, route: RouteDecision,
                  overrides: Mapping[str, Any] | None = None,
                  ) -> tuple[list[dict[str, Any]], ExecutionReceipt]:
    """Run ``route`` for ``goal`` through the existing dispatch machinery and
    wrap the outcome into (artifacts, ExecutionReceipt). Never raises for an
    execution failure — that is receipt data; only GoalShapeError (a request-
    shape fault, pre-dispatch) escapes. ``overrides`` are extra body fields
    merged after the shape build (k92's reseed repair passes ``seed``)."""
    if route.execution != "execute":
        raise ValueError(f"execute_route called on a {route.execution!r} route")

    body = build_request_body(goal, route)
    if overrides:
        body.update(overrides)
    task = route.task or ""
    deterministic = task in ("document-extraction", "url-extraction")
    if deterministic:
        kwargs = dict(body, task=task)
    else:
        kwargs = _normalized_kwargs(task, body)

    started_at = _utc_now()
    t0 = time.monotonic()
    retries = 0
    failure: FailureClass | None = None
    log_excerpt: list[str] = []
    warnings: list[str] = []
    payload: dict[str, Any] = {}

    for attempt in (0, 1):
        try:
            if task == "document-extraction":
                result = _extract_document(body["file"])
            elif task == "url-extraction":
                result = _assess_url(body["url"])
            else:
                result = _dispatch(kwargs)
        except Exception as exc:  # noqa: BLE001 — classified, never propagated
            failure = classify_failure(exc)
            log_excerpt.append(f"{type(exc).__name__}: {exc}"[:500])
            if failure is FailureClass.WORKER_UNAVAILABLE and attempt == 0:
                retries = 1
                warnings.append("retried once after WORKER_UNAVAILABLE")
                continue
            break
        failure = None
        payload = _result_payload(result)
        if payload.get("ok") is False or payload.get("error"):
            failure = FailureClass.RUNNER_ERROR
            log_excerpt.append(str(payload.get("error") or "runner returned not-ok")[:500])
        break

    duration = time.monotonic() - t0
    artifacts = extract_artifacts(route.capability, payload) if failure is None else []

    receipt = ExecutionReceipt(
        request=ExecutionReceipt.normalize_request(_receipt_request(kwargs)),
        capability=route.capability,
        model_id=route.model_id or payload.get("model_key") or "(dispatch-default)",
        worker=None if route.placement == "auto" else route.placement,
        started_at=started_at,
        ended_at=_utc_now(),
        duration_s=round(duration, 4),
        retries=retries,
        failure=failure,
        artifacts=tuple(
            ArtifactRef(kind=ArtifactKind(a["kind"]), uri=a["uri"],
                        sha256=a.get("sha256"))
            for a in artifacts),
        warnings=tuple(warnings),
        log_excerpt=tuple(log_excerpt),
    )
    return artifacts, receipt


__all__ = ["GoalShapeError", "build_request_body", "classify_failure",
           "extract_artifacts", "execute_route"]
