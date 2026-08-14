"""Unified READ-ONLY capability catalog (k90): the bridge over both registries.

Two disjoint model registries exist today (documented in studio/tester.py):

  * STUDIO — video_intel/studio: typed Capability/ModelConfig zoo with its own
    router, runner gates (``runner_gate_reason``) and viability facts
    (``ZERO_BYTE_MODELS`` / ``STUB_RUNNER_MODULES`` in presets).
  * TASKS  — imports/config/models: the legacy tasks-string registry
    (text/vision/ASR/imagegen rows carrying ``tasks: [str]``), dispatched
    through ``execute_prompt`` and gated at request time by worker heartbeat
    ``task_capabilities`` + central's own import probes (managers/task_deps).

This module COMPOSES the two behind one namespaced capability vocabulary and
joins the health signals each side already computes, so GET /oracle/capabilities
can explain WHY a capability is ineligible BEFORE anything executes (the
Phase-1 done-criterion). It never mutates either registry — pure reads.

The mapping tables are the contract k91's router will dispatch on:
``LEGACY_TASK_CAPABILITY`` (task string -> namespaced name) and
``STUDIO_CAPABILITY_NAME`` (studio Capability -> namespaced name), with
explicit EXCLUDED tables for members that deliberately do not become routable
capabilities. ``tests/test_oracle_catalog.py`` proves both maps total.

Import discipline (same as studio/tester.py): module top level is
dependency-light — contracts + the studio ENUMS only (both plain stdlib). Every
registry/worker read is LAZY inside a provider function, and those providers
are module-level seams (``_legacy_registry_rows`` / ``_online_workers`` / …)
precisely so tests monkeypatch them and need no live workers, GPU or network.
Worker/blocklist reads are guarded fail-open: a telemetry read must never turn
the catalog itself into the failure.
"""

from __future__ import annotations

import logging
from typing import Any, Callable

from abstract_hugpy_dev.video_intel.studio.enums import Capability

from .contracts import (
    ArtifactKind,
    CapabilityView,
    Eligibility,
    ResourceHints,
    SourceRegistry,
)

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# The mapping tables — defined ONCE, exported, proven total by tests.
# ---------------------------------------------------------------------------

# Legacy tasks-string registry: task string -> namespaced capability name.
# Covers every ML_TASKS dispatch task plus the registry task strings the
# models_default.py groupings key on (chat/embed aliases). A discovery row
# carrying a task string absent from BOTH tables is simply not catalogued —
# unknown discovery noise must not invent capabilities (see unmapped_tasks()).
LEGACY_TASK_CAPABILITY: dict[str, str] = {
    "text-generation":               "text.chat",
    "text-generation-inference":     "text.chat",
    "text2text-generation":          "text.chat",
    "text-summarization":            "text.summarize",
    "keyword-extraction":            "text.keywords",
    "feature-extraction":            "text.embed",
    "sentence-transformers":         "text.embed",
    "sentence-similarity":           "text.similarity",
    "automatic-speech-recognition":  "audio.transcribe",
    "speech-recognition":            "audio.transcribe",
    "image-text-to-text":            "image.understand",
    "text-to-image":                 "image.generate",
    "image-to-image":                "image.transform",
    "depth-estimation":              "image.depth",
    "object-detection":              "image.detect",
    "image-classification":          "image.classify",
    "image-segmentation":            "image.segment",
    "document-extraction":           "doc.extract",
    "url-extraction":                "web.fetch",
}

# Legacy tasks deliberately NOT catalogued as capabilities, with the reason.
# Every ML_TASKS member maps above; these are the OTHER task strings observed
# on live registry rows (discovery/classifier output). An exclusion is a
# recorded decision, never a silent gap — the completeness test enforces
# membership in exactly one of the two tables, and ``unmapped_tasks()`` reports
# any live task string that reaches neither.
LEGACY_TASK_EXCLUDED: dict[str, str] = {
    "text-to-video": (
        "video generation is owned by the STUDIO registry (video.generate.*); "
        "legacy diffusers video rows are reached through the studio/movie "
        "pipeline, not routed as a second t2v capability"),
    "image-to-video": (
        "video generation is owned by the STUDIO registry (video.generate.*); "
        "same ownership rule as text-to-video"),
    "adapter": (
        "classifier marker for LoRA/adapter weight dirs (model_classifier."
        "ADAPTER_TASK) — an adapter conditions another model, it is not an "
        "executable capability"),
    "needs-classification": (
        "classifier marker for un-classified discovery rows (model_classifier."
        "NEEDS_CLASSIFICATION_TASK) — unknown weights are not a capability"),
    "pipeline-component": (
        "classifier marker for partial pipeline dirs (VAE/text-encoder/…) — a "
        "component of a model, not an executable capability"),
}

# Deterministic ingest amenities (ml_routes._DETERMINISTIC_ML): they run as
# thin LOCAL handlers on central — no model row, no worker dispatch. A
# capability whose tasks are all deterministic is judged ONLY on central's
# dependency probe; "no model registered" would be a false refusal.
DETERMINISTIC_TASKS: frozenset[str] = frozenset(
    {"document-extraction", "url-extraction"})

# Studio registry: Capability enum member -> namespaced capability name.
STUDIO_CAPABILITY_NAME: dict[Capability, str] = {
    Capability.T2V:      "video.generate.t2v",
    Capability.I2V:      "video.generate.i2v",
    Capability.V2V:      "video.generate.v2v",
    Capability.KEYFRAME: "video.generate.keyframe",
    Capability.ID_LOCK:  "video.generate.id_lock",
    Capability.MOTION:   "video.generate.motion",
    Capability.STREAM:   "video.generate.stream",
    Capability.INPAINT:  "video.generate.inpaint",
    Capability.OUTPAINT: "video.generate.outpaint",
    Capability.RETAKE:   "video.generate.retake",
    Capability.AUDIO:    "video.generate.audio",
    Capability.LIPSYNC:  "video.generate.lipsync",
    Capability.UPRES:    "video.enhance.upres",
    Capability.INTERP:   "video.enhance.interp",
    Capability.RESTORE:  "video.enhance.restore",
}

# Studio Capability members that are NOT routable capabilities, with the why.
STUDIO_CAPABILITY_EXCLUDED: dict[Capability, str] = {
    Capability.ASSEMBLE: (
        "orchestration stage, not a model-served capability (studio "
        "PLANNED_CAPABILITIES): multi-shot assembly is a composition node the "
        "oracle plans, never a route it resolves to one model"),
}


# What each capability accepts/produces (artifact kinds). Declared here because
# neither registry states IO kinds today — the legacy registry has only task
# strings, and the studio's contract is capability-shaped, not artifact-shaped.
_K = ArtifactKind
_LEGACY_IO: dict[str, tuple[tuple[ArtifactKind, ...], tuple[ArtifactKind, ...]]] = {
    "text.chat":        ((_K.TEXT,), (_K.TEXT,)),
    "text.summarize":   ((_K.TEXT,), (_K.TEXT,)),
    "text.keywords":    ((_K.TEXT,), (_K.JSON,)),
    "text.embed":       ((_K.TEXT,), (_K.EMBEDDING,)),
    "text.similarity":  ((_K.TEXT,), (_K.JSON,)),
    "audio.transcribe": ((_K.AUDIO, _K.VIDEO), (_K.TEXT, _K.JSON)),
    "image.understand": ((_K.IMAGE, _K.TEXT), (_K.TEXT,)),
    "image.generate":   ((_K.TEXT,), (_K.IMAGE,)),
    "image.transform":  ((_K.IMAGE, _K.TEXT), (_K.IMAGE,)),
    "image.depth":      ((_K.IMAGE,), (_K.IMAGE,)),
    "image.detect":     ((_K.IMAGE,), (_K.JSON,)),
    "image.classify":   ((_K.IMAGE,), (_K.JSON,)),
    "image.segment":    ((_K.IMAGE,), (_K.IMAGE, _K.JSON)),
    "doc.extract":      ((_K.DOCUMENT,), (_K.TEXT,)),
    "web.fetch":        ((_K.URL,), (_K.TEXT,)),
}
_STUDIO_IO: dict[Capability, tuple[tuple[ArtifactKind, ...], tuple[ArtifactKind, ...]]] = {
    Capability.T2V:      ((_K.TEXT,), (_K.VIDEO,)),
    Capability.I2V:      ((_K.IMAGE, _K.TEXT), (_K.VIDEO,)),
    Capability.V2V:      ((_K.VIDEO, _K.TEXT), (_K.VIDEO,)),
    Capability.KEYFRAME: ((_K.IMAGE,), (_K.VIDEO,)),
    Capability.ID_LOCK:  ((_K.TEXT, _K.IMAGE), (_K.VIDEO,)),
    Capability.MOTION:   ((_K.TEXT, _K.IMAGE), (_K.VIDEO,)),
    Capability.STREAM:   ((_K.TEXT, _K.IMAGE), (_K.VIDEO,)),
    Capability.INPAINT:  ((_K.VIDEO, _K.TEXT), (_K.VIDEO,)),
    Capability.OUTPAINT: ((_K.VIDEO, _K.TEXT), (_K.VIDEO,)),
    Capability.RETAKE:   ((_K.VIDEO, _K.TEXT), (_K.VIDEO,)),
    Capability.AUDIO:    ((_K.TEXT, _K.IMAGE), (_K.VIDEO, _K.AUDIO)),
    Capability.LIPSYNC:  ((_K.VIDEO, _K.AUDIO), (_K.VIDEO,)),
    Capability.UPRES:    ((_K.VIDEO,), (_K.VIDEO,)),
    Capability.INTERP:   ((_K.VIDEO,), (_K.VIDEO,)),
    Capability.RESTORE:  ((_K.VIDEO,), (_K.VIDEO,)),
}


# ---------------------------------------------------------------------------
# Provider seams — lazy reads, monkeypatchable in tests.
# ---------------------------------------------------------------------------


def _legacy_registry_rows() -> dict[str, dict[str, Any]]:
    """The legacy registry as plain row dicts (model_key -> row). Served from
    models_config's cached build — a read, never a rebuild."""
    from abstract_hugpy_dev.imports.config.models.models_config import (
        get_model_registry)
    return dict(get_model_registry(dict_return=True))


def _online_workers() -> list[dict[str, Any]] | None:
    """Online workers per the heartbeat registry, or None when the worker
    plane is unreadable (signal UNKNOWN — the catalog then judges on central's
    own capabilities rather than inventing a fleet)."""
    try:
        from abstract_hugpy_dev.flask_app.app.functions.imports.utils.workers import (
            worker_store, _is_online)
        return [w for w in worker_store.all() if _is_online(w)]
    except Exception as exc:  # noqa: BLE001 — telemetry must not break the catalog
        logger.debug("oracle catalog: worker registry unreadable (%s)", exc)
        return None


def _worker_task_capable(worker: dict[str, Any], task: str) -> bool:
    """The fleet's own capability-honesty rule, reused verbatim where it lives
    (workers._task_capable: affirmative-deny only, legacy-permissive)."""
    try:
        from abstract_hugpy_dev.flask_app.app.functions.imports.utils.workers import (
            _task_capable)
        return _task_capable(worker, task)
    except Exception:  # noqa: BLE001
        return True


def _central_task_available(task: str) -> bool | None:
    """Can CENTRAL run ``task`` in-process? True/False from the canonical
    task->dependency probe (managers/task_deps, find_spec only); None when the
    task has no dependency entry there (no gate — e.g. chat, which central
    serves through its own engine path)."""
    from abstract_hugpy_dev.managers.task_deps import TASK_DEPS, have
    dep = TASK_DEPS.get(task)
    if dep is None:
        return None
    return have(dep[0])


def _blocked_model_keys() -> set[str]:
    """Operator-blocked model keys, fail-open like every blocklist read."""
    try:
        from abstract_hugpy_dev.comms.blocklist import blocked_keys
        return set(blocked_keys())
    except Exception:  # noqa: BLE001
        return set()


# ---------------------------------------------------------------------------
# View construction — TASKS side
# ---------------------------------------------------------------------------


def _capability_task_groups() -> dict[str, tuple[str, ...]]:
    """Invert LEGACY_TASK_CAPABILITY: capability name -> its task strings,
    sorted for stable output."""
    groups: dict[str, list[str]] = {}
    for task, cap in LEGACY_TASK_CAPABILITY.items():
        groups.setdefault(cap, []).append(task)
    return {cap: tuple(sorted(tasks)) for cap, tasks in groups.items()}


def _legacy_views() -> list[CapabilityView]:
    rows = _legacy_registry_rows()
    blocked = _blocked_model_keys()
    workers = _online_workers()

    views: list[CapabilityView] = []
    for cap_name, tasks in sorted(_capability_task_groups().items()):
        model_ids = tuple(sorted(
            key for key, row in rows.items()
            if any(t in (row.get("tasks") or ()) for t in tasks)))
        usable_ids = tuple(m for m in model_ids if m not in blocked)
        task_list = ", ".join(tasks)
        deterministic = all(t in DETERMINISTIC_TASKS for t in tasks)

        # Central-local signal (canonical task->dependency probe).
        central_flags = {t: _central_task_available(t) for t in tasks}
        central_ok = any(flag is not False for flag in central_flags.values())

        reasons: list[str] = []
        worker_ok: bool | None = None
        if deterministic:
            # No model, no worker dispatch — a thin local handler on central
            # (ml_routes._DETERMINISTIC_ML). Only the dependency probe gates.
            eligible = central_ok
            if not central_ok:
                reasons.append(
                    f"central cannot run deterministic task(s) {task_list} "
                    f"(dependency module not importable — see managers/task_deps)")
        else:
            if not model_ids:
                reasons.append(f"no model registered for task(s) {task_list}")
            elif not usable_ids:
                reasons.append(
                    f"every registered model for task(s) {task_list} is "
                    f"operator-blocked from the serving pool")

            # Worker signal (heartbeat task_capabilities, affirmative-deny only).
            if workers is not None:
                if not workers:
                    worker_ok = False
                    reasons.append("no online worker registered")
                else:
                    worker_ok = any(_worker_task_capable(w, t)
                                    for w in workers for t in tasks)
                    if not worker_ok:
                        reasons.append(
                            f"no online worker advertises task(s) {task_list} "
                            f"(heartbeat task_capabilities)")

            if not central_ok:
                missing = ", ".join(
                    t for t, f in sorted(central_flags.items()) if f is False)
                reasons.append(
                    f"central cannot serve task(s) {missing} in-process "
                    f"(dependency module not importable — see managers/task_deps)")

            eligible = bool(usable_ids) and (worker_ok is True or central_ok)
            if not eligible and not reasons:  # defensive: Eligibility requires reasons
                reasons.append("no execution path (no capable worker and no "
                               "central-local fallback)")

        frameworks = tuple(sorted({
            str(rows[m].get("framework")) for m in model_ids
            if rows.get(m, {}).get("framework")}))
        notes = "deterministic local amenity (no model)" if deterministic else ""
        accepts, produces = _LEGACY_IO[cap_name]
        views.append(CapabilityView(
            name=cap_name,
            source=SourceRegistry.TASKS,
            accepts=accepts,
            produces=produces,
            model_ids=usable_ids,
            eligibility=Eligibility(eligible=eligible, reasons=tuple(reasons)),
            resources=ResourceHints(frameworks=frameworks, notes=notes),
        ))
    return views


# ---------------------------------------------------------------------------
# View construction — STUDIO side
# ---------------------------------------------------------------------------


def _studio_views() -> list[CapabilityView]:
    """The studio side, through its own typed API only: capability_verdict for
    the servability answer + wording (two gates, one wording — this catalog is
    a third consumer of the SAME wording, never a rival derivation),
    capable_model_ids for the honest model set (synthetic excluded), and the
    registry/preset gate facts for per-model reasons."""
    # Importing the package registers the zoo (models_seed side effect) —
    # reads only; validate_registry() is deliberately NOT called (it enforces
    # weight-pinning policy, a serve-path concern, not a catalog concern).
    from abstract_hugpy_dev.video_intel.studio.presets import (
        STUB_RUNNER_MODULES, ZERO_BYTE_MODELS, capability_verdict)
    from abstract_hugpy_dev.video_intel.studio.registry import (
        MODEL_REGISTRY, model_gate_reasons, runner_for)
    from abstract_hugpy_dev.video_intel.studio.router import capable_model_ids

    views: list[CapabilityView] = []
    for cap, name in sorted(STUDIO_CAPABILITY_NAME.items(),
                            key=lambda item: item[1]):
        verdict = capability_verdict(cap)
        ids = capable_model_ids(cap)

        reasons: list[str] = []
        if not verdict.servable:
            reasons.append(verdict.reason)
        elif not ids:
            # The verdict says servable but no REAL model is capable: the
            # capability is carried by the last-resort tier (the ffmpeg
            # enhancer / synthetic rows rank below every real model but DO
            # render — e.g. interp/upres on a GPU-less fleet). Honor the
            # studio's own verdict; say honestly which tier serves it.
            ids = capable_model_ids(cap, include_synthetic=True)
            if ids:
                reasons.append(
                    "served only by the last-resort tier (synthetic/ffmpeg "
                    "fallback — every real model for it is gated or absent)")

        # Per-model "declared it but cannot run it" reasons, from the same
        # facts the router rejects on (gate + viability), so the catalog and a
        # routing refusal can never tell different stories.
        declared = [m for m in MODEL_REGISTRY.values()
                    if cap in m.capabilities and not m.synthetic]
        for cfg in sorted(declared, key=lambda m: m.model_id):
            if cfg.model_id in ids:
                continue
            if cfg.model_id in ZERO_BYTE_MODELS:
                reasons.append(f"{cfg.model_id}: weights absent "
                               f"(0 bytes on the shared store)")
                continue
            stub_tasks = [
                t.value for t in cfg.tasks
                if (spec := runner_for(cfg.family, t)) is not None
                and spec.entrypoint.split(":", 1)[0] in STUB_RUNNER_MODULES]
            if stub_tasks:
                reasons.append(f"{cfg.model_id}: stub runner "
                               f"({', '.join(stub_tasks)} — every path returns Err)")
                continue
            gates = model_gate_reasons(cfg.model_id)
            if gates:
                gate_text = "; ".join(f"{t}: {why}" for t, why in sorted(gates.items()))
                reasons.append(f"{cfg.model_id}: runner gated ({gate_text})")

        eligible = verdict.servable and bool(ids)
        if not eligible and not reasons:
            reasons.append("no capable model on this fleet")

        vram_mins = [cfg.vram.min_gb() for cfg in MODEL_REGISTRY.values()
                     if cfg.model_id in ids]
        frameworks = tuple(sorted({cfg.family.value
                                   for cfg in MODEL_REGISTRY.values()
                                   if cfg.model_id in ids}))
        accepts, produces = _STUDIO_IO[cap]
        views.append(CapabilityView(
            name=name,
            source=SourceRegistry.STUDIO,
            accepts=accepts,
            produces=produces,
            model_ids=ids,
            eligibility=Eligibility(eligible=eligible, reasons=tuple(reasons)),
            resources=ResourceHints(
                min_vram_gb=min(vram_mins) if vram_mins else None,
                frameworks=frameworks),
        ))
    return views


# ---------------------------------------------------------------------------
# Public surface
# ---------------------------------------------------------------------------


def list_capabilities() -> list[CapabilityView]:
    """Every namespaced capability from BOTH registries, sorted by name. The
    two vocabularies are disjoint by construction (the mapping tables share no
    names — proven by tests AND re-checked here, because a silent collision
    would mean one registry's view shadows the other's)."""
    views = _studio_views() + _legacy_views()
    by_name: dict[str, CapabilityView] = {}
    for view in views:
        if view.name in by_name:
            raise RuntimeError(
                f"capability name collision across registries: {view.name!r} "
                f"({by_name[view.name].source.value} vs {view.source.value})")
        by_name[view.name] = view
    return sorted(by_name.values(), key=lambda v: v.name)


def get_capability(name: str) -> CapabilityView | None:
    """The single view for ``name``, or None when no such capability exists."""
    for view in list_capabilities():
        if view.name == name:
            return view
    return None


def resolve_owners(name: str) -> tuple[SourceRegistry, tuple[str, ...]] | None:
    """Which registry owns ``name`` and which model ids implement it — the
    lookup k91's router starts from. None for an unknown name."""
    view = get_capability(name)
    if view is None:
        return None
    return (view.source, view.model_ids)


def unmapped_tasks() -> tuple[str, ...]:
    """Reporting hook (mirrors studio ``unpinned_models()``): task strings
    present on legacy registry rows but absent from BOTH mapping tables —
    discovery noise the catalog is deliberately not inventing capabilities
    for. Empty when the tables cover the live registry."""
    known = set(LEGACY_TASK_CAPABILITY) | set(LEGACY_TASK_EXCLUDED)
    seen: set[str] = set()
    for row in _legacy_registry_rows().values():
        for task in (row.get("tasks") or ()):
            if task and task not in known:
                seen.add(str(task))
    return tuple(sorted(seen))


__all__ = [
    "LEGACY_TASK_CAPABILITY", "LEGACY_TASK_EXCLUDED",
    "STUDIO_CAPABILITY_NAME", "STUDIO_CAPABILITY_EXCLUDED",
    "list_capabilities", "get_capability", "resolve_owners", "unmapped_tasks",
]
