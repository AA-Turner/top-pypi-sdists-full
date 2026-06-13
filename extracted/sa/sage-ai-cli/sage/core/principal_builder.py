"""Principal-engineer-grade project builder.

The orchestrator that wires bootstrap_scaffolders + architecture_modules +
feature_files + prompt_library + review_pass into a single end-to-end
pipeline. Replaces `dynamic_builder.build_project_dynamic` as the default
entry point used by the CLI — the older one is retained for the legacy
test surface and the rollback flag.

Stages:
  1. Decompose spec → ProjectPlan
  2. Bootstrap real CLI scaffolders (npx create-expo-app, alembic init)
  3. Emit deterministic root files (README, .gitignore, .github/, etc.)
  4. Resolve deps → requirements.txt + pyproject.toml + package.json
  5. Emit cross-cutting architecture files (auth, DB, Celery, middleware…)
  6. For each feature: emit the FULL vertical slice (model→schema→repo→
     service→api→tests) in topological order, with previously-written
     siblings injected into each prompt
  7. Per-file principal-engineer review → regenerate on low score
  8. Install + verify (iterate-until-green)
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from sage.core.architecture_modules import architecture_files
from sage.core.bootstrap_scaffolders import ScaffoldResult, run_bootstrap
from sage.core.dep_resolver import (
    DepSet,
    emit_node_package_json,
    emit_python_dep_files,
    resolve_dependencies,
    sanitize_dep_files_in_place,
)
from sage.core.dynamic_builder import (
    _make_test_runner,
    _verify_iterate_until_green,
)
from sage.core.code_doctors import DoctorReport, run_code_doctors
from sage.core.feature_files import files_for_feature
from sage.core.final_polish import PolishReport, run_final_polish
from sage.core.install_verify import VerifyReport
from sage.core.integration_check import IntegrationReport, run_integration_check
from sage.core.integrity_pass import IntegrityReport, run_integrity_pass
from sage.core.pre_write_validator import (
    ValidationResult,
    validated_generate,
)
from sage.core.principal_engineer import (
    CURRENT_VERSIONS,
    FileSpec,
    _strip_reasoning_blocks,
    compress_task_brief,
    strip_code_fences,
)
from sage.core.project_layout import FileSlot, LayoutPlan, plan_layout
from sage.core.prompt_library import build_specialized_prompt
from sage.core.review_pass import review_and_repair
from sage.core.spec_decomposer import (
    Feature,
    ProjectPlan,
    StackProfile,
    decompose_spec,
)


GenerateFn = Callable[[str], str]
ProgressFn = Callable[[str], None]


class BuildIncomplete(Exception):
    """Raised when the heal loop runs out of retries with install or tests
    still failing. The caller (CLI) is expected to catch this and surface a
    clear failure message to the user — sage MUST NOT report success when
    the generated code can't even install."""

    def __init__(self, message: str, report: "PrincipalBuildReport"):
        super().__init__(message)
        self.report = report


@dataclass
class PrincipalBuildReport:
    title: str
    stack: dict
    out_dir: str
    file_count: int
    feature_count: int
    bootstrap_results: list[dict] = field(default_factory=list)
    review_scores: dict[str, float] = field(default_factory=dict)
    validation_failures: list[dict] = field(default_factory=list)
    doctors: dict = field(default_factory=dict)
    integrity: dict = field(default_factory=dict)
    integration: dict = field(default_factory=dict)
    polish: dict = field(default_factory=dict)
    verify_reports: list[dict] = field(default_factory=list)
    install_ok: bool | None = None
    build_ok: bool | None = None
    runs_ok: bool | None = None
    tests_ok: bool | None = None
    stuck_features: list[str] = field(default_factory=list)

    def as_dict(self) -> dict:
        return asdict(self)


# ──────────────────────── helpers ──────────────────────────────────────


def _slug(text: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", text.strip()).strip("-").lower()
    return s[:60] or "project"


def _file_slot_to_spec(slot: FileSlot) -> FileSpec:
    return FileSpec(
        path=slot.path,
        role=slot.role,
        language=slot.language,
        template=slot.template,
        must_contain=list(slot.must_contain),
        must_not_contain=list(slot.must_not_contain),
    )


# Topological order for backend files within a feature. Earlier files are
# written first and their contents are made available as sibling context
# to later files. This is how we get the API file to reference the actual
# schema names, not invented ones.
_BACKEND_ORDER: dict[str, int] = {
    "models": 0,
    "schemas": 1,
    "repositories": 2,
    "services": 3,
    "tasks": 4,
    "api": 5,
}


_FRONTEND_ORDER: dict[str, int] = {
    "types": 0,
    "services": 1,
    "stores": 2,
    "hooks": 3,
    "components": 4,
    "app": 5,
}


def _layer_key(path: str) -> int:
    """Order key for topological sort — lower = generated first."""
    for k, v in _BACKEND_ORDER.items():
        if f"/{k}/" in path:
            return v
    for k, v in _FRONTEND_ORDER.items():
        if f"/{k}/" in path:
            return v + 10  # frontend after backend
    return 100  # everything else last


def _sort_for_generation(slots: list[FileSlot]) -> list[FileSlot]:
    """Sort: non-test before test, then by layer topology."""
    return sorted(slots, key=lambda s: (s.is_test, _layer_key(s.path), s.path))


def _read_sibling_context(out_dir: Path, paths: list[str], cap: int = 700) -> dict[str, str]:
    """Read up to 3 already-written files as context for the next prompt.

    Optimized for local-LLM speed: smaller cap + fewer siblings = shorter
    prompts = faster generation. We keep the model + schema as sibling
    context for API/service generation since those references matter most.
    """
    ctx: dict[str, str] = {}
    for rel in paths[-3:]:  # keep the most recent 3 siblings
        p = out_dir / rel
        if p.exists():
            try:
                content = p.read_text("utf-8", errors="replace")
            except OSError:
                continue
            ctx[rel] = content[:cap]
    return ctx


def _generate_one_file(
    slot: FileSlot,
    *,
    task: str,
    tree: list[str],
    stack_label: str,
    sibling_excerpts: dict[str, str],
    generate: GenerateFn,
    is_rn_frontend: bool = False,
    log: ProgressFn | None = None,
) -> tuple[str, ValidationResult]:
    """Generate one file with PRE-WRITE validation + retry.

    Returns (final_content, validation_result). If validation fails after
    `max_attempts`, returns the best-effort content + the failing result —
    the caller decides whether to write it anyway or skip.
    """
    spec = _file_slot_to_spec(slot)
    initial_prompt = build_specialized_prompt(
        task, spec, tree, stack_label,
        sibling_excerpts=sibling_excerpts,
    )
    return validated_generate(
        initial_prompt=initial_prompt,
        path=slot.path,
        generate=generate,
        sanitize=strip_code_fences,
        max_attempts=3,
        is_rn_frontend=is_rn_frontend,
        log=log,
    )


def _heal_until_green(
    out_dir: Path,
    *,
    generate: GenerateFn,
    log: ProgressFn,
    max_rounds: int = 3,
    stuck_threshold: int = 2,
) -> tuple[bool, bool, bool, bool, list[VerifyReport]]:
    """Loop deterministic-then-LLM repairs until install, build, run, + tests all pass.

    Called only when the post-polish state has any failures. Each round:
      1. Drop deprecated deps from requirements/pyproject (handles the
         class of bug where the LLM keeps re-emitting paypalcheckoutsdk).
      2. Re-run code doctors (truncated __init__, indent fixes, missing
         imports, ruff --fix).
      3. Re-run integrity pass + integration check using the latest verify
         logs as context.
      4. Run a verify pass; if green, return.

    Returns (install_ok, build_ok, runs_ok, tests_ok, latest_verify_reports).
    """
    log(f"[heal] entering heal loop (cap={max_rounds} rounds)")

    last_reports: list[VerifyReport] = []
    install_ok = build_ok = runs_ok = tests_ok = False

    for round_idx in range(1, max_rounds + 1):
        log(f"[heal] round {round_idx}/{max_rounds}")

        # 1. Deterministic dep cleanup — only the heal stage runs this on
        #    EXISTING files, since the build loop is upstream of any
        #    LLM-driven regen that might have reintroduced bad names.
        dropped = sanitize_dep_files_in_place(out_dir / "backend")
        if dropped:
            log(f"[heal] dropped {dropped} deprecated dep entries")

        # 2. Doctors again — they're idempotent and cheap (no LLM tokens).
        run_code_doctors(
            out_dir,
            log=log,
            fix_imports=True,
            fix_framework=True,
            detect_truncations_flag=True,
            run_ruff=True,
            run_eslint=True,
            run_prettier=False,
        )

        # 3. LLM-driven integrity + integration with fresh context.
        run_integrity_pass(
            out_dir,
            generate=generate,
            log=log,
            enable_ruff_fix=True,
            enable_lint_pass=True,
        )
        run_integration_check(out_dir, generate=generate, log=log)

        # 4. The main repair loop — pick up where verify last left off.
        last_reports = _verify_iterate_until_green(
            out_dir, generate=generate, log=log, stuck_threshold=stuck_threshold,
        )

        install_ok = all(r.install_ok in (True, None) for r in last_reports)
        build_ok = all(r.build_ok in (True, None) for r in last_reports)
        runs_ok = all(r.runs_ok in (True, None) for r in last_reports)
        # We're stricter than the caller here: a build with no test step
        # detected is NOT considered green. We always scaffold tests, so a
        # missing test step means the verify discovery missed something.
        tests_ok = bool(last_reports) and all(
            r.tests_ok is True for r in last_reports
        )
        if install_ok and build_ok and runs_ok and tests_ok:
            log(f"[heal] round {round_idx}: GREEN")
            return install_ok, build_ok, runs_ok, tests_ok, last_reports

        log(f"[heal] round {round_idx}: install_ok={install_ok} build_ok={build_ok} runs_ok={runs_ok} tests_ok={tests_ok}")

    return install_ok, build_ok, runs_ok, tests_ok, last_reports


# ──────────────────────── public entry ─────────────────────────────────


def _snapshot_project(out_dir: Path, log: "ProgressFn") -> Path | None:
    """Create a .tar.gz snapshot of out_dir before a build starts.

    Stored in out_dir/.sage/pre_build_snapshot.tar.gz.
    Returns the snapshot path on success, None on failure (non-fatal).
    This protects existing projects from being destroyed when a build
    errors mid-generation (e.g. cloud model disconnect).
    """
    import tarfile
    snapshot_dir = out_dir / ".sage"
    snapshot_dir.mkdir(parents=True, exist_ok=True)
    snapshot_path = snapshot_dir / "pre_build_snapshot.tar.gz"

    # Only snapshot if there are actual project files (not just .sage/)
    project_files = [
        p for p in out_dir.rglob("*")
        if p.is_file() and ".sage" not in p.parts and "__pycache__" not in p.parts
    ]
    if not project_files:
        return None  # Nothing to snapshot — fresh build

    try:
        with tarfile.open(snapshot_path, "w:gz") as tar:
            for fpath in project_files:
                tar.add(fpath, arcname=fpath.relative_to(out_dir))
        log(f"[snapshot] saved {len(project_files)} files to {snapshot_path.name}")
        return snapshot_path
    except Exception as exc:
        log(f"[snapshot] WARNING: could not create snapshot: {exc}")
        return None


def _restore_snapshot(snapshot_path: Path, out_dir: Path, log: "ProgressFn") -> bool:
    """Restore a project from a .tar.gz snapshot created by _snapshot_project.

    Called when a build fails and we need to preserve the user's existing work.
    Returns True on success.
    """
    import tarfile
    if not snapshot_path.exists():
        return False
    try:
        # Remove all non-.sage files that were written by the failed build
        for p in list(out_dir.rglob("*")):
            if p.is_file() and ".sage" not in p.parts and "__pycache__" not in p.parts:
                p.unlink()
        # Restore from snapshot
        with tarfile.open(snapshot_path, "r:gz") as tar:
            tar.extractall(path=out_dir)
        log(f"[snapshot] restored project from {snapshot_path.name}")
        return True
    except Exception as exc:
        log(f"[snapshot] ERROR: restore failed: {exc}")
        return False


def _clean_ansi(obj):
    import re
    if isinstance(obj, str):
        text = re.sub(r'\x1b\[[0-9;]*[mGKHFABCDEJst]', '', obj)
        text = re.sub(r'\x1b\].*?\x07', '', text)
        text = re.sub(r'\x1b[()][AB012]?', '', text)
        return text.replace('\x1b', '')
    if isinstance(obj, dict):
        return {k: _clean_ansi(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_clean_ansi(x) for x in obj]
    return obj


def build_project_principal(
    task: str,
    out_dir: Path,
    generate: GenerateFn,
    *,
    progress: ProgressFn | None = None,
    review_threshold: float = 7.0,
    max_review_rounds: int = 2,
    enable_review: bool = True,
    stuck_threshold: int = 3,
    enable_heal: bool = True,
    heal_rounds: int = 3,
) -> PrincipalBuildReport:
    """End-to-end principal-grade project build.

    SAFETY: If out_dir already contains project files, a snapshot is created
    before the build starts. If the build fails partway (e.g. cloud model
    disconnect mid-generation), the snapshot is restored so the user's
    existing work is NOT destroyed.
    """
    log = progress or (lambda _m: None)
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── Pre-build snapshot: protect existing files from failed builds ──
    # The most common failure mode (cloud model disconnect mid-generation)
    # leaves the project in a half-overwritten state. Snapshotting before
    # we touch anything means we can always restore the pre-build state.
    _snapshot = _snapshot_project(out_dir, log)

    try:
        return _build_project_principal_inner(
            task=task, out_dir=out_dir, generate=generate, log=log,
            review_threshold=review_threshold, max_review_rounds=max_review_rounds,
            enable_review=enable_review, stuck_threshold=stuck_threshold,
            enable_heal=enable_heal, heal_rounds=heal_rounds,
        )
    except Exception as exc:
        # CRITICAL: do NOT restore the snapshot on connectivity errors mid-build.
        # The old behavior wiped out hours of LLM-generated work whenever the
        # cloud API hiccupped (which is often). Instead, KEEP partial progress
        # so the user can re-run and fill in missing files. The pre-build
        # snapshot is still available at .sage/pre_build_snapshot.tar.gz if
        # the user explicitly wants to roll back.
        _connectivity_errors = (
            "Server disconnected", "RemoteProtocolError", "ReadError",
            "ConnectError", "All providers failed", "quota", "disconnected",
            "connection", "timeout", "503", "502", "429",
        )
        is_connectivity = any(e.lower() in str(exc).lower() for e in _connectivity_errors)
        if _snapshot and is_connectivity and not isinstance(exc, BuildIncomplete):
            # Count files written during this build so we can tell the user
            # what they have to keep working with.
            try:
                _generated = [
                    p for p in out_dir.rglob("*")
                    if p.is_file()
                    and ".sage" not in p.parts
                    and "__pycache__" not in p.parts
                    and "node_modules" not in p.parts
                ]
                log(
                    f"[snapshot] Build hit connectivity error ({type(exc).__name__}) "
                    f"but {len(_generated)} files are on disk — KEEPING them. "
                    "Re-run sage to fill in missing files. To roll back manually: "
                    "tar -xzf .sage/pre_build_snapshot.tar.gz"
                )
            except Exception:
                pass
        raise


def _build_project_principal_inner(
    task: str,
    out_dir: Path,
    generate: GenerateFn,
    log: "ProgressFn",
    *,
    review_threshold: float = 7.0,
    max_review_rounds: int = 2,
    enable_review: bool = True,
    stuck_threshold: int = 3,
    enable_heal: bool = True,
    heal_rounds: int = 3,
) -> PrincipalBuildReport:
    """Inner build function — called by build_project_principal after snapshotting."""

    # ── 1. Decompose ──
    log("[1/8] decomposing spec...")
    plan = decompose_spec(task, generate)
    log(f"      task_type={plan.task_type} features={len(plan.features)} stack={plan.stack}")

    # Game prompts route to sage/games — entirely separate pipeline because
    # game-engine projects have nothing structurally in common with the
    # webapp scaffold (no frontend/backend siblings, no FastAPI/React).
    # The PrincipalBuildReport shape we return is intentionally minimal for
    # games — the games pipeline owns its own richer GameBuildReport that
    # the CLI inspects via `report.game_report`.
    if plan.task_type == "game":
        from sage.games.exceptions import (
            BuildNotSupported,
            EngineNotInstalled,
            GameBuildIncomplete,
            ScaffoldPollution,
        )
        from sage.games.pipeline import build_game

        try:
            game_report = build_game(
                plan.game_request, out_dir, generate, progress=log,
            )
            return PrincipalBuildReport(
                title=plan.title,
                stack={"engine": game_report.engine},
                out_dir=str(out_dir),
                file_count=len(game_report.scripts_written)
                            + game_report.sprite_count
                            + game_report.mesh_count
                            + game_report.audio_count,
                feature_count=0,
                install_ok=True,
                tests_ok=True if game_report.build_artifact else None,
            )
        except EngineNotInstalled as exc:
            # Engine missing isn't a sage bug — surface a clear install
            # hint without raising BuildIncomplete (which would imply we
            # tried + couldn't recover).
            log(f"[game] {exc}")
            return PrincipalBuildReport(
                title=plan.title,
                stack={"engine": (plan.game_request.engine or "godot")},
                out_dir=str(out_dir), file_count=0, feature_count=0,
                install_ok=False, tests_ok=False,
            )
        except (BuildNotSupported, GameBuildIncomplete) as exc:
            log(f"[game] build did not complete: {exc}")
            return PrincipalBuildReport(
                title=plan.title,
                stack={"engine": (plan.game_request.engine or "godot")},
                out_dir=str(out_dir), file_count=0, feature_count=0,
                install_ok=True, tests_ok=False,
            )
        except ScaffoldPollution as exc:
            # Different-engine scaffold already in this directory. Don't
            # corrupt the user's existing project — surface a clear error
            # and let the CLI / user decide whether to clear the dir.
            log(f"[game] {exc}")
            return PrincipalBuildReport(
                title=plan.title,
                stack={"engine": (plan.game_request.engine or "godot"),
                        "existing_engine": exc.existing_engine},
                out_dir=str(out_dir), file_count=0, feature_count=0,
                install_ok=False, tests_ok=False,
            )

    # ── 2. Layout (root files only) ──
    log("[2/8] planning layout...")
    layout = plan_layout(plan)
    # Root files (deterministic templates) AND stack-package files
    # — but skip the per-feature files plan_layout creates, since
    # we'll replace those with feature_files below.
    layout_slots = [s for s in layout.files if s.feature is None]

    # Do NOT write template files directly anymore, treat them as pending slots so they are dynamically generated.
    _DEP_FILES = {
        "backend/requirements.txt",
        "backend/pyproject.toml",
        "frontend/package.json",
    }
    pending_slots: list[FileSlot] = []
    for slot in layout_slots:
        if slot.path in _DEP_FILES:
            continue
        pending_slots.append(slot)
    log(f"      routed {len(layout_slots) - len(_DEP_FILES)} root files for generation")

    # ── 3. Resolve deps ──
    log("[3/8] resolving dependencies...")
    deps = resolve_dependencies(plan, generate)
    slug = _slug(plan.title)
    if plan.stack.backend in {"fastapi", "django", "flask"}:
        emit_python_dep_files(deps, out_dir / "backend", project_name=slug + "-backend")
        log(f"      backend deps: {len(deps.python_runtime)}")
    if plan.stack.frontend and plan.stack.frontend in {"react", "react-native-web", "nextjs", "vue", "svelte"}:
        emit_node_package_json(
            deps, out_dir / "frontend",
            framework=plan.stack.frontend, project_name=slug + "-frontend",
        )
        log(f"      frontend deps: {len(deps.node_runtime)}")

    # Persist the plan so the user can see what sage understood
    sage_dir = out_dir / ".sage"
    sage_dir.mkdir(exist_ok=True)
    (sage_dir / "PROJECT_PLAN.json").write_text(
        json.dumps(
            {
                "title": plan.title,
                "stack": asdict(plan.stack),
                "features": [asdict(f) for f in plan.features],
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    # ── 4. Bootstrap real scaffolders ──
    log("[4/8] running real scaffolders (Expo, alembic)...")
    bootstrap_results = run_bootstrap(
        out_dir,
        frontend=plan.stack.frontend,
        backend=plan.stack.backend,
        log=log,
    )

    # ── 5. Architecture modules (cross-cutting infra) ──
    log("[5/8] planning architecture modules...")
    arch_slots = architecture_files(plan)
    log(f"      {len(arch_slots)} infrastructure files to generate")

    # ── 6. Per-feature multi-file plans ──
    log("[6/8] planning per-feature file sets...")
    all_feature_slots: list[FileSlot] = []
    for feat in plan.features:
        all_feature_slots.extend(
            files_for_feature(feat, frontend=plan.stack.frontend, backend=plan.stack.backend)
        )
    log(f"      {len(all_feature_slots)} feature-file slots planned")

    # Materialise architecture + feature slots in topological order
    all_slots = pending_slots + arch_slots + all_feature_slots
    all_slots = _sort_for_generation(all_slots)

    # Skip slots with deterministic templates (they're already written or
    # have a fixed body). Also skip files that already exist on disk —
    # this enables RESUME: if a previous run wrote some files but hit an
    # API error, re-running fills in only the missing files instead of
    # regenerating everything.
    to_generate: list[FileSlot] = []
    _skipped_existing = 0
    for slot in all_slots:
        if slot.template is not None:
            target_path = out_dir / slot.path
            target_path.parent.mkdir(parents=True, exist_ok=True)
            target_path.write_text(slot.template, encoding="utf-8")
            continue
        target_path = out_dir / slot.path
        # RESUME: if the file already has substantial content, skip regeneration.
        # Empty/stub files (< 50 bytes) get regenerated; real files are kept.
        if target_path.exists() and target_path.stat().st_size > 50:
            _skipped_existing += 1
            continue
        to_generate.append(slot)

    if _skipped_existing:
        log(f"      resume: skipping {_skipped_existing} files already on disk")
    log(f"      total: {len(to_generate)} files require LLM generation")

    # ── 7. LLM generation in topological order ──
    log("[7/8] generating files...")
    stack_label = f"{plan.stack.frontend or 'none'} + {plan.stack.backend or 'none'}"
    tree = [s.path for s in all_slots]

    # ── KEY OPTIMIZATION: compress the spec ONCE up-front. ──
    # The full 7.7KB spec was being copied into every per-file prompt (200×).
    # On a local model this is the dominant cost. Compressing it to a
    # ~1KB brief one extra LLM call now → 200 cheaper per-file calls
    # → net 2-3× faster on local hardware.
    if len(task) > 2000:
        log("      compressing spec to brief (one extra LLM call now → 200 cheaper later)...")
        try:
            brief = compress_task_brief(task, generate)
            log(f"      brief={len(brief)} chars (from {len(task)})")
        except Exception as exc:  # noqa: BLE001
            log(f"      compression failed: {exc}; using full task")
            brief = task
    else:
        brief = task

    # Persist the brief alongside PROJECT_PLAN.json so the user can see it
    (sage_dir / "PROJECT_BRIEF.md").write_text(brief, encoding="utf-8")

    review_scores: dict[str, float] = {}
    validation_failures: list[dict] = []
    is_rn = plan.stack.frontend == "react-native-web"

    # ── PARALLEL FILE GENERATION ────────────────────────────────────────
    # Group slots by feature, then run features in parallel (max 6 at a time
    # to avoid cloud-backend rate limits). Within a feature, slots run
    # sequentially so siblings can see each other's content for cohesion.
    #
    # Sequential time for 200 files × 90s each = 5 hours.
    # Parallel time for 25 features (8 files each) at 6-way concurrency
    # = ~5 batches × 8 files × 90s ≈ 60 minutes — ~5x speedup.
    from concurrent.futures import ThreadPoolExecutor, as_completed
    from collections import defaultdict
    import threading

    slots_by_feature: dict[str | None, list[FileSlot]] = defaultdict(list)
    for slot in to_generate:
        slots_by_feature[slot.feature].append(slot)

    _log_lock = threading.Lock()
    _completed = [0]
    _total = len(to_generate)

    def _safe_log(msg: str) -> None:
        with _log_lock:
            log(msg)

    def _generate_feature_group(
        feature_key: str | None, feature_slots: list[FileSlot]
    ) -> tuple[list[str], list[dict], dict[str, float]]:
        """Generate all files for one feature sequentially. Runs in a worker thread."""
        siblings_so_far: list[str] = []
        local_failures: list[dict] = []
        local_reviews: dict[str, float] = {}
        local_written: list[str] = []
        for slot in feature_slots:
            try:
                excerpts = _read_sibling_context(out_dir, siblings_so_far)
                is_rn_file = is_rn and slot.path.startswith("frontend/")
                content, vresult = _generate_one_file(
                    slot,
                    task=brief,
                    tree=tree,
                    stack_label=stack_label,
                    sibling_excerpts=excerpts,
                    generate=generate,
                    is_rn_frontend=is_rn_file,
                    log=lambda m: None,
                )
                target = out_dir / slot.path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")
                siblings_so_far.append(slot.path)
                local_written.append(slot.path)

                if not vresult.ok:
                    local_failures.append({"path": slot.path, "errors": vresult.errors})

                # Per-file review
                if enable_review and not slot.is_test and slot.language in {"python", "typescript"}:
                    framework = plan.stack.backend or plan.stack.frontend or "generic"
                    result = review_and_repair(
                        target, slot.role, framework, generate,
                        sanitize=strip_code_fences,
                        threshold=review_threshold,
                        max_rounds=max_review_rounds,
                        log=lambda m: None,
                    )
                    local_reviews[slot.path] = result.score

                with _log_lock:
                    _completed[0] += 1
                    log(f"      [{_completed[0]}/{_total}] {slot.path}")
            except Exception as exc:  # noqa: BLE001
                # Individual file failures shouldn't kill the whole build.
                # Log and continue — heal loop will retry later.
                _safe_log(f"      [warn] {slot.path} failed: {exc}")
                local_failures.append({"path": slot.path, "errors": [str(exc)]})
        return local_written, local_failures, local_reviews

    # Run features in parallel — 3 concurrent (was 6, but cloud backend can't handle that).
    # Each worker generates one feature's files SEQUENTIALLY (preserves sibling cohesion).
    _MAX_CONCURRENT_FEATURES = 3
    with ThreadPoolExecutor(max_workers=_MAX_CONCURRENT_FEATURES) as executor:
        futures = {
            executor.submit(_generate_feature_group, fkey, fslots): fkey
            for fkey, fslots in slots_by_feature.items()
        }
        for fut in as_completed(futures):
            try:
                _, fails, reviews = fut.result()
                validation_failures.extend(fails)
                review_scores.update(reviews)
            except Exception as exc:  # noqa: BLE001
                _safe_log(f"      [warn] feature group failed: {exc}")

    log(f"      generated {len(to_generate)} files, {len(review_scores)} reviewed (parallel)")

    # ── 7.4 Deterministic code-doctor pass (no LLM) ─────────────────────
    # Runs BEFORE the integrity pass. These doctors fix the systemic
    # LLM-output bugs we've observed (missing imports, wrong frontend
    # framework, unbalanced braces) in milliseconds with zero LLM
    # tokens. Whatever's left after this pass is what the LLM integrity
    # pass needs to handle.
    log("[7.4/8] running deterministic code doctors...")
    doctors = run_code_doctors(
        out_dir,
        log=log,
        fix_imports=True,
        fix_framework=True,
        detect_truncations_flag=True,
        run_ruff=True,
        run_eslint=True,
        run_prettier=False,  # optional, off for speed
    )

    # ── 7.5 Cross-file integrity pass ──────────────────────────────────
    # Catches the systemic missing-imports problem the overnight build
    # surfaced. Two sub-passes:
    #   a) `ruff check --fix --unsafe-fixes` — deterministic, kills
    #      ~80% of style + unused-import issues with no LLM tokens.
    #   b) Cross-module dangling-import detection — when X imports a
    #      name Y from sibling module M but M doesn't export Y, regen X
    #      with M's actual contents in the prompt.
    #   c) Per-file lint + undefined-name pass — catches names used at
    #      module scope that aren't bound anywhere (e.g. `Index` used
    #      without `from sqlalchemy import Index`).
    log("[7.5/8] running cross-file integrity pass...")
    integrity = run_integrity_pass(
        out_dir,
        generate=generate,
        log=log,
        enable_ruff_fix=True,
        enable_lint_pass=True,
    )

    # ── 7.6 Cross-file integration check ───────────────────────────────
    # Catches `from app.main import X` where main.py doesn't export X.
    # This is the class of bug the per-file validator can't see — it
    # needs full-project context. Closed the gap that caused tests_ok=
    # False in the previous build (conftest imported `settings` that
    # main.py never defined).
    log("[7.6/8] running cross-file integration check...")
    integration = run_integration_check(
        out_dir, generate=generate, log=log,
    )

    # ── 8. Install + verify (iterate-until-green) ──
    log("[8/8] installing and verifying...")
    verify_reports = _verify_iterate_until_green(
        out_dir,
        generate=generate,
        log=log,
        stuck_threshold=stuck_threshold,
    )

    install_ok = all(r.install_ok in (True, None) for r in verify_reports)
    build_ok = all(r.build_ok in (True, None) for r in verify_reports)
    runs_ok = all(r.runs_ok in (True, None) for r in verify_reports)
    tests_ok = all(r.tests_ok in (True, None) for r in verify_reports)

    # ── 9. Final polish — types/* deps + ruff/eslint --fix + final verify ──
    # Catches the trailing issues: missing @types/jest etc. (typecheck
    # failure cause in last build), and the 44 auto-fixable ruff errors
    # that doctor missed because integrity regenerated files AFTER
    # the doctor ran.
    log("[9/9] final polish...")
    polish = run_final_polish(out_dir, log=log)
    if polish.final_install_ok is not None:
        install_ok = polish.final_install_ok
    if polish.final_build_ok is not None:
        build_ok = polish.final_build_ok
    if polish.final_runs_ok is not None:
        runs_ok = polish.final_runs_ok
    if polish.final_tests_ok is not None:
        tests_ok = polish.final_tests_ok

    # ── 10. Heal-until-green ── sage MUST NOT report success when the
    # generated code can't install or its tests don't pass. This loop is
    # the user's "do not allow sage to complete early" guarantee.
    if enable_heal and (install_ok is False or build_ok is False or runs_ok is False or tests_ok is False):
        install_ok, build_ok, runs_ok, tests_ok, heal_reports = _heal_until_green(
            out_dir,
            generate=generate,
            log=log,
            max_rounds=heal_rounds,
            stuck_threshold=stuck_threshold,
        )
        if heal_reports:
            verify_reports = heal_reports  # use latest in the persisted report

    log(f"complete. install_ok={install_ok} build_ok={build_ok} runs_ok={runs_ok} tests_ok={tests_ok}")

    report = PrincipalBuildReport(
        title=plan.title,
        stack=asdict(plan.stack),
        out_dir=str(out_dir),
        file_count=len(to_generate) + len(_DEP_FILES) + sum(
            1 for s in all_slots if s.template is not None
        ),
        feature_count=len(plan.features),
        bootstrap_results=[
            {"name": r.name, "ran": r.ran, "ok": r.ok, "log_tail": r.log[-500:]}
            for r in bootstrap_results
        ],
        review_scores=review_scores,
        validation_failures=validation_failures,
        doctors=asdict(doctors),
        integrity=asdict(integrity),
        integration=asdict(integration),
        polish=asdict(polish),
        verify_reports=[
            {
                "project": {"kind": r.project.kind, "root": str(r.project.root)},
                "steps": [
                    {"name": s.name, "ok": s.ok, "returncode": s.returncode,
                     "duration_s": s.duration_s, "log_tail": s.log[-1500:]}
                    for s in r.steps
                ],
                "install_ok": r.install_ok,
                "build_ok": r.build_ok,
                "runs_ok": r.runs_ok,
                "tests_ok": r.tests_ok,
            }
            for r in verify_reports
        ],
        install_ok=install_ok,
        build_ok=build_ok,
        runs_ok=runs_ok,
        tests_ok=tests_ok,
    )

    (sage_dir / "BUILD_REPORT.json").write_text(
        json.dumps(_clean_ansi(report.as_dict()), indent=2),
        encoding="utf-8",
    )

    # Surface a hard failure if the heal loop couldn't make the build
    # green. Caller (CLI) is expected to catch BuildIncomplete and present
    # a clear message — sage MUST NOT silently return a broken project.
    if enable_heal and (install_ok is False or build_ok is False or runs_ok is False or tests_ok is False):
        raise BuildIncomplete(
            f"build did not converge: install_ok={install_ok} build_ok={build_ok} runs_ok={runs_ok} tests_ok={tests_ok}",
            report,
        )

    return report


__all__ = ["BuildIncomplete", "PrincipalBuildReport", "build_project_principal"]
