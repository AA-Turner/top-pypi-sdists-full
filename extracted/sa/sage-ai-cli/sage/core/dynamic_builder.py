"""Dynamic spec-driven project builder.

The new top-level orchestrator. Replaces the hardcoded `plan_*()` pipeline
in `principal_engineer.build_project` with one that derives every
artifact from the actual spec:

    spec_text
      → spec_decomposer.decompose_spec()        # LLM: features + stack
      → project_layout.plan_layout()            # paths, .github at root
      → dep_resolver.resolve_dependencies()     # pinned deps
      → emit deterministic templates            # gitignore, ci.yml, etc.
      → tdd_loop.run_feature_tdd() per feature  # test-first, iterate-until-green
      → install_verify.verify_all()             # final install + test pass
      → report

The legacy `principal_engineer.build_project()` stays put behind the
`--legacy-plans` flag so we can fall back if the new pipeline regresses
on small tasks before tuning. See `docs/superpowers/specs/2026-05-12-...md`.
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

from sage.core.dep_resolver import (
    DepSet,
    emit_node_package_json,
    emit_python_dep_files,
    resolve_dependencies,
)
from sage.core.install_verify import (
    DiscoveredProject,
    StepResult,
    VerifyReport,
    verify_all,
    verify_project,
)
from sage.core.principal_engineer import (
    CURRENT_VERSIONS,
    FileSpec,
    _strip_reasoning_blocks,
    build_file_prompt,
    build_review_prompt,
    parse_review_response,
    strip_code_fences,
    validate_file,
)
from sage.core.project_layout import FileSlot, LayoutPlan, plan_layout
from sage.core.spec_decomposer import (
    Feature,
    ProjectPlan,
    StackProfile,
    decompose_spec,
)
from sage.core.tdd_loop import FeatureResult, run_feature_tdd


GenerateFn = Callable[[str], str]
ProgressFn = Callable[[str], None]


# Files that sage emits via deterministic templates — the LLM has no
# business rewriting these. If the repair loop tries to (because some
# stage 8 failure has a stack frame mentioning them), skip the write.
# Without this guard, the repair pass overwrote our pinned tsconfig.json
# with a broken one that referenced @types/jest packages we didn't ship.
_PROTECTED_TEMPLATE_PATHS: frozenset[str] = frozenset({
    "frontend/tsconfig.json",
    "frontend/.npmrc",
    "frontend/package.json",         # owned by dep_resolver
    "frontend/jest.config.js",       # LLM generates runaway transformIgnorePatterns
    "frontend/babel.config.js",      # owned by dep_resolver
    "frontend/metro.config.js",      # owned by dep_resolver
    "frontend/app.json",             # owned by dep_resolver
    # Firebase auth — LLM overwrites working auth with broken stubs
    "frontend/src/firebase/auth.js",
    "frontend/src/firebase/AuthContext.jsx",
    "frontend/src/firebase/firebaseEnv.js",
    "frontend/src/firebase/index.js",
    "frontend/src/firebase/index.ts",
    "backend/requirements.txt",      # owned by dep_resolver
    "backend/pyproject.toml",        # owned by dep_resolver
    "backend/tests/conftest.py",     # owned by architecture_modules
    ".gitignore",
    ".env.example",
    ".github/workflows/ci.yml",
    "docker-compose.yml",
    "backend/alembic.ini",
    "backend/alembic/script.py.mako",
})


@dataclass
class BuildReport:
    title: str
    stack: dict[str, str | None]
    out_dir: str
    file_count: int
    feature_count: int
    feature_results: list[dict] = field(default_factory=list)
    verify_reports: list[dict] = field(default_factory=list)
    stuck_features: list[str] = field(default_factory=list)
    install_ok: bool | None = None
    build_ok: bool | None = None
    runs_ok: bool | None = None
    tests_ok: bool | None = None

    def as_dict(self) -> dict:
        return asdict(self)


def _slug_project_name(title: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "-", title.strip()).strip("-").lower()
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


# ──────────────────────── per-file LLM generation ──────────────────────


def _generate_file(
    spec: FileSpec,
    *,
    task: str,
    tree: list[str],
    stack_label: str,
    generate: GenerateFn,
) -> str:
    """One-shot LLM call to write a single file with validate+retry."""
    versions = CURRENT_VERSIONS.get(_lang_for_python(spec.language), CURRENT_VERSIONS["python"])
    prompt = build_file_prompt(task, spec, tree, stack_label, versions)
    content = strip_code_fences(generate(prompt))
    for _ in range(3):
        errors = validate_file(spec, content)
        if not errors:
            return content
        fix_prompt = (
            prompt
            + "\n\n## Previous attempt defects (fix ALL):\n"
            + "\n".join(f"- {e}" for e in errors)
            + "\n\nOutput ONLY the corrected file contents."
        )
        content = strip_code_fences(generate(fix_prompt))
    return content


def _lang_for_python(language: str) -> str:
    if language in {"python"}:
        return "python"
    if language in {"typescript", "tsx", "javascript", "jsx"}:
        return "node"
    if language == "go":
        return "go"
    if language == "rust":
        return "rust"
    if language == "kotlin":
        return "kotlin"
    if language == "swift":
        return "swift"
    if language == "dart":
        return "dart"
    if language == "java":
        return "java"
    return "python"


# ──────────────────────── per-feature TDD wrapper ──────────────────────


def _make_test_runner(layout: LayoutPlan, out_dir: Path) -> Callable[..., tuple[bool, str, int]]:
    """Build a pytest/jest runner closure used inside the TDD loop.

    Picks the right tool based on the test file extension. Returns
    (ok, log, failure_count).
    """

    def run(test_path: Path, _impl_path: Path) -> tuple[bool, str, int]:
        rel = test_path.relative_to(out_dir)
        suffix = test_path.suffix

        if suffix == ".py":
            # Run pytest inside the backend project so imports resolve
            cwd = out_dir / "backend" if (out_dir / "backend").exists() else out_dir
            test_rel = test_path.relative_to(cwd)
            cmd = [sys.executable, "-m", "pytest", str(test_rel), "-q", "--no-header"]
        elif suffix in {".tsx", ".ts", ".jsx", ".js"}:
            cwd = out_dir / "frontend" if (out_dir / "frontend").exists() else out_dir
            test_rel = test_path.relative_to(cwd)
            cmd = ["npx", "--no-install", "jest", str(test_rel), "--passWithNoTests"]
        else:
            return False, f"no runner for {suffix}", 1

        try:
            proc = subprocess.run(
                cmd, cwd=cwd, capture_output=True, text=True, timeout=300, check=False
            )
        except (FileNotFoundError, subprocess.TimeoutExpired) as exc:
            return False, str(exc), 1

        log = (proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")
        failures = _count_failures(log)
        return proc.returncode == 0, log, failures

    return run


_PY_FAIL_RE = re.compile(r"(\d+)\s+failed", re.I)
_PY_PASS_RE = re.compile(r"(\d+)\s+passed", re.I)
_JEST_FAIL_RE = re.compile(r"Tests:\s+(\d+)\s+failed", re.I)


def _count_failures(log: str) -> int:
    """Count failing tests from pytest/jest output. Used for stuck-detection."""
    if not log:
        return 0
    m = _PY_FAIL_RE.search(log)
    if m:
        return int(m.group(1))
    m = _JEST_FAIL_RE.search(log)
    if m:
        return int(m.group(1))
    # No "failed" line but the runner reported non-zero — treat as 1 failure
    return 0 if "passed" in log.lower() else 1


# ──────────────────────── verify with iterate-until-green ───────────────


def _verify_iterate_until_green(
    out_dir: Path,
    *,
    generate: GenerateFn,
    log: ProgressFn,
    stuck_threshold: int = 2,  # exit faster when no progress — was 3
) -> list[VerifyReport]:
    """Run install+test on every discovered project; on failure regenerate
    the offending files and re-run. Uses progress-stuck detection to prevent
    infinite loops. stuck_threshold=2 means exit after 2 rounds with no improvement.
    """
    rounds = 0
    last_fail_count: int | None = None
    flat_rounds = 0
    _MAX_ROUNDS = 8  # hard safety cap — prevents truly infinite loops on cloud models

    while rounds < _MAX_ROUNDS:
        rounds += 1
        log(f"[verify] round {rounds}/{_MAX_ROUNDS}")
        reports = verify_all(out_dir)
        if all(r.all_ok for r in reports):
            return reports

        # Count failing steps across all projects
        fail_count = sum(1 for r in reports for s in r.steps if not s.ok)
        log(f"[verify] round {rounds}: {fail_count} failing steps")

        # Stuck detection: exit if no progress for stuck_threshold rounds
        if last_fail_count is not None:
            if fail_count >= last_fail_count:
                flat_rounds += 1
                if flat_rounds >= stuck_threshold:
                    log(
                        f"[verify] STUCK after {rounds} rounds ({fail_count} failures, "
                        f"{flat_rounds} flat rounds without progress). Stopping auto-repair."
                    )
                    return reports
            else:
                flat_rounds = 0
        last_fail_count = fail_count

        # Try to repair each failing step
        for report in reports:
            for step in report.steps:
                if step.ok:
                    continue
                _attempt_repair(report.project, step, generate=generate, log=log)


def _missing_modules_from_log(log_text: str, project_root: Path) -> list[str]:
    """Extract Python module paths that need to be CREATED from error logs.

    Handles 'ModuleNotFoundError: No module named X.Y.Z' where the module
    path maps to a file that doesn't exist in the project (not a library).
    Returns repo-relative paths like 'app/models/user.py'.
    """
    missing: list[str] = []
    for m in re.finditer(r"No module named '([\w.]+)'", log_text):
        mod = m.group(1)
        # Convert dotted module name to file path
        rel = mod.replace(".", "/") + ".py"
        target = project_root / rel
        if not target.exists():
            # Only create project-local files (skip stdlib/library names)
            parts = mod.split(".")
            if parts[0] in ("app", "src", "backend", "core", "api", "models", "schemas"):
                missing.append(rel)
    return missing


def _parse_fixes_from_llm(
    raw: str,
    relevant_files: list[Path],
    missing_paths: list[str],
    project_root: Path,
) -> dict[str, str] | None:
    """Tolerantly extract file updates from the LLM's raw response.

    Handles JSON formatting with literal control characters, markdown code fence
    block extractions with filepath comment markers, and single-file fallback.
    """
    raw_clean = _strip_reasoning_blocks(raw).strip()

    # Safe relative paths helper
    def _safe_relative(p: Path) -> str:
        try:
            return str(p.relative_to(project_root))
        except ValueError:
            try:
                return str(p.relative_to(project_root.parent))
            except ValueError:
                return p.name

    all_targets = [_safe_relative(p) for p in relevant_files] + missing_paths

    # 1. Try to parse as JSON first (with strict=False to allow literal newlines/tabs)
    start = raw_clean.find("{")
    end = raw_clean.rfind("}")
    if start != -1 and end != -1:
        try:
            fixes = json.loads(raw_clean[start : end + 1], strict=False)
            if isinstance(fixes, dict) and fixes:
                # Ensure at least one key matches a target file (exact, relative, or basename)
                any_match = False
                for k in fixes.keys():
                    k_clean = str(k).lower()
                    k_base = Path(k_clean).name
                    for target in all_targets:
                        t_lower = target.lower()
                        t_base = Path(t_lower).name
                        if k_clean == t_lower or k_base == t_base or t_lower in k_clean:
                            any_match = True
                            break
                    if any_match:
                        break
                if any_match:
                    return {str(k): str(v) for k, v in fixes.items()}
        except Exception:
            pass

    # 2. Fallback 1: Extract code blocks from Markdown fences (supporting multiline indent)
    blocks = re.findall(r"^[ \t]*```[a-zA-Z0-9+_-]*\n(.*?)\n^[ \t]*```", raw_clean, re.DOTALL | re.MULTILINE)
    fixes: dict[str, str] = {}

    def _find_target_in_block(block_content: str) -> str | None:
        lines = block_content.splitlines()[:5]
        for line in lines:
            line_clean = line.strip().lower()
            if not line_clean.startswith("#") and not line_clean.startswith("//") and not line_clean.startswith("/*"):
                continue
            for target in all_targets:
                t_lower = target.lower()
                t_base = Path(target).name.lower()
                # Check if full path or file basename is explicitly mentioned in the comment line
                if t_lower in line_clean or t_base in line_clean:
                    return target
        return None

    for block in blocks:
        target = _find_target_in_block(block)
        if target:
            fixes[target] = block

    if fixes:
        return fixes

    # 3. Fallback 2: If there is exactly one target file and the output is a single block, return it
    if len(all_targets) == 1:
        target = all_targets[0]
        clean_content = strip_code_fences(raw_clean)
        if len(clean_content) > 10:
            return {target: clean_content}

    return None


def _attempt_repair(
    project: DiscoveredProject,
    step: StepResult,
    *,
    generate: GenerateFn,
    log: ProgressFn,
) -> None:
    """Ask the LLM to rewrite/create files using the failure log, retrying on validation failures."""
    relevant_files = _likely_files_for_step(project, step)

    # Include missing-module paths as files-to-create (they don't exist yet)
    missing_paths = _missing_modules_from_log(step.log, project.root)
    missing_hint = ""
    if missing_paths:
        missing_hint = (
            "\n\n## Missing modules to CREATE\n"
            "These files do not yet exist and must be created:\n"
            + "\n".join(f"- {p}" for p in missing_paths[:5])
        )

    if not relevant_files and not missing_paths:
        return

    def _safe_relative(p: Path) -> str:
        try:
            return str(p.relative_to(project.root))
        except ValueError:
            try:
                return str(p.relative_to(project.root.parent))
            except ValueError:
                return p.name

    # Cap context per file to 1500 chars to keep repair prompts fast
    context = "\n\n".join(
        f"## {_safe_relative(p)}\n```\n{p.read_text('utf-8', errors='replace')[:1500]}\n```"
        for p in relevant_files
    )

    # Shorter prompt = faster model response = faster overall build
    # Keep the error tail tight (1500 chars) and rely on context for file details
    initial_prompt = (
        f"Fix a '{step.name}' failure in a {project.kind} project.\n\n"
        f"Error:\n```\n{step.log[-1500:]}\n```\n\n"
        f"Files:\n{context}\n"
        f"{missing_hint}\n\n"
        "Return ONLY a JSON object: {{\"path\": \"full corrected content\", ...}}\n"
        "No explanation. Fix only what the error says.\n"
        'Example: {"backend/app/main.py": "from fastapi import FastAPI\\napp=FastAPI()"}'
    )

    from sage.core.pre_write_validator import validate_generated_file

    prompt = initial_prompt
    for attempt in range(1, 4):
        try:
            raw = generate(prompt)
        except Exception as exc:  # noqa: BLE001 — verification loop must not crash
            log(f"[repair] generate() raised: {exc}")
            return

        fixes = _parse_fixes_from_llm(raw, relevant_files, missing_paths, project.root)
        if not fixes:
            log(f"[repair] could not parse fix JSON/output for {step.name} (attempt {attempt}/3)")
            prompt = (
                initial_prompt
                + "\n\n## Formatting feedback\n"
                "Your previous response could not be parsed as a JSON object or raw code block. "
                "Output ONLY a valid JSON object mapping filenames to their complete new contents as shown in the example."
            )
            continue

        all_ok = True
        validation_errors = []
        for rel_path, new_content in fixes.items():
            if not isinstance(new_content, str) or len(new_content) < 10:
                continue
            if rel_path in _PROTECTED_TEMPLATE_PATHS:
                continue
            is_rn = "frontend/" in rel_path and project.kind == "node"
            vresult = validate_generated_file(new_content, rel_path, is_rn_frontend=is_rn)
            if not vresult.ok:
                all_ok = False
                for err in vresult.errors:
                    validation_errors.append(f"- File `{rel_path}`: {err}")

        if all_ok:
            for rel_path, new_content in fixes.items():
                if not isinstance(new_content, str) or len(new_content) < 10:
                    continue
                if rel_path in _PROTECTED_TEMPLATE_PATHS:
                    log(f"[repair] SKIP {rel_path} (protected template)")
                    continue

                new_content = strip_code_fences(new_content)
                target = project.root / rel_path
                if not target.parent.exists():
                    target = project.root.parent / rel_path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(new_content, encoding="utf-8")
                log(f"[repair] wrote {rel_path}")
            return
        else:
            log(f"[repair] attempt {attempt}/3 failed validation for {step.name}")
            err_msg = "\n".join(validation_errors)
            prompt = (
                initial_prompt
                + "\n\n## Your previous attempt failed validation with the following defects:\n"
                + f"{err_msg}\n\n"
                + "Please output the corrected files, fixing ALL of these defects."
            )

    log(f"[repair] exhausted all 3 attempts for {step.name}")


def _likely_files_for_step(
    project: DiscoveredProject, step: StepResult
) -> list[Path]:
    """Heuristic: which files probably need to be regenerated for this failure."""
    root = project.root
    candidates: list[Path] = []

    # Extract file paths mentioned in the log (best signal)
    for match in re.finditer(
        r"(?P<path>(?:[\w\-./])+\.(?:py|tsx|ts|jsx|js|go|rs|java|kt))",
        step.log,
    ):
        path = Path(match.group("path"))
        # Skip absolute paths — they point to installed library files
        # (e.g. /usr/local/.../pydantic_settings/main.py), NOT project files.
        # Including them here used to crash `_attempt_repair.relative_to()`.
        if path.is_absolute():
            continue
        # Try to resolve against project root
        if (root / path).exists():
            candidate = (root / path).resolve()
            # Final safety: must be under project root or its parent
            try:
                candidate.relative_to(root.parent)
            except ValueError:
                continue
            candidates.append(candidate)
        elif (root.parent / path).exists():
            candidate = (root.parent / path).resolve()
            try:
                candidate.relative_to(root.parent)
            except ValueError:
                continue
            candidates.append(candidate)

    # Always include the main entry point for compile-style failures
    if project.kind == "python":
        for stem in ("app/main.py", "main.py", "pyproject.toml", "requirements.txt"):
            p = root / stem
            if p.exists() and p not in candidates:
                candidates.append(p)
    elif project.kind == "node":
        for stem in ("package.json", "tsconfig.json"):
            p = root / stem
            if p.exists() and p not in candidates:
                candidates.append(p)

    return candidates[:6]  # cap context size


def _clean_ansi(obj):
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


# ──────────────────────── public builder ───────────────────────────────


def build_project_dynamic(
    task: str,
    out_dir: Path,
    generate: GenerateFn,
    *,
    progress: ProgressFn | None = None,
    review_threshold: float = 7.0,
    enable_tdd_loop: bool = True,
    stuck_threshold: int = 3,
) -> BuildReport:
    """Build a project end-to-end with the new spec-driven pipeline.

    Pipeline:
      1. Decompose spec → features + stack profile.
      2. Plan layout → file list with frontend/ + backend/ siblings.
      3. Resolve deps → emit requirements.txt + pyproject.toml + package.json.
      4. For each feature: TDD loop (test first, iterate-until-green).
      5. For each non-feature file: per-file LLM generation with review.
      6. Cross-project verify (install + test + lint) with iterate-until-green.
    """
    log = progress or (lambda _m: None)
    out_dir = out_dir.resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    # ── 1. Decompose ──
    log("[1/6] decomposing spec...")
    plan = decompose_spec(task, generate)
    log(f"      title={plan.title!r} features={len(plan.features)} stack={plan.stack}")

    # ── 2. Layout ──
    log("[2/6] planning layout...")
    layout = plan_layout(plan)
    log(f"      {len(layout.files)} file slots planned across {layout.directories}")

    # Materialise deterministic-template files first (gitignore, ci.yml, etc.)
    # Skip dep files — they're owned by dep_resolver, which writes them in
    # the next step. If we let them through the LLM pass below they'd get
    # overwritten with empty content.
    _DEP_FILES = {
        "backend/requirements.txt",
        "backend/pyproject.toml",
        "frontend/package.json",
    }
    feature_slots: list[FileSlot] = []
    for slot in layout.files:
        if slot.path in _DEP_FILES:
            continue  # dep_resolver writes these
        feature_slots.append(slot)

    # ── 3. Deps ──
    log("[3/6] resolving dependencies...")
    deps = resolve_dependencies(plan, generate)
    project_slug = _slug_project_name(plan.title)
    if plan.stack.backend in {"fastapi", "django", "flask"}:
        emit_python_dep_files(
            deps, out_dir / "backend", project_name=project_slug + "-backend"
        )
        log(f"      wrote backend/requirements.txt + pyproject.toml ({len(deps.python_runtime)} deps)")
    if plan.stack.frontend:
        emit_node_package_json(
            deps,
            out_dir / "frontend",
            framework=plan.stack.frontend,
            project_name=project_slug + "-frontend",
        )
        log(f"      wrote frontend/package.json ({len(deps.node_runtime)} deps)")

    # Persist the brief so the user can see what sage understood
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

    # ── 4. Generate feature files (TDD-first if both impl+test in same feature) ──
    log("[4/6] generating feature implementations...")
    feature_results: list[FeatureResult] = []
    by_feature: dict[str, list[FileSlot]] = {}
    cross_cutting: list[FileSlot] = []
    for slot in feature_slots:
        if slot.feature is None:
            cross_cutting.append(slot)
        else:
            by_feature.setdefault(slot.feature, []).append(slot)

    feature_by_name = {f.name: f for f in plan.features}
    tree = [s.path for s in layout.files]
    stack_label = f"{plan.stack.frontend or 'none'} + {plan.stack.backend or 'none'}"
    test_runner = _make_test_runner(layout, out_dir)

    for feature_name, slots in by_feature.items():
        impl_slots = [s for s in slots if not s.is_test]
        test_slots = [s for s in slots if s.is_test]
        feat = feature_by_name.get(feature_name)
        if not feat or not impl_slots:
            continue

        # Generate non-primary impl files first (services, etc.) so the test
        # has all helpers available
        primary_impl = impl_slots[-1]
        for slot in impl_slots[:-1]:
            target = out_dir / slot.path
            target.parent.mkdir(parents=True, exist_ok=True)
            content = _generate_file(
                _file_slot_to_spec(slot),
                task=task,
                tree=tree,
                stack_label=stack_label,
                generate=generate,
            )
            target.write_text(content, encoding="utf-8")

        if enable_tdd_loop and test_slots:
            result = run_feature_tdd(
                feat,
                impl_path=out_dir / primary_impl.path,
                test_path=out_dir / test_slots[0].path,
                generate=generate,
                run_tests=test_runner,
                stuck_threshold=stuck_threshold,
                progress=log,
            )
            feature_results.append(result)
        else:
            # Just generate, no TDD loop
            content = _generate_file(
                _file_slot_to_spec(primary_impl),
                task=task,
                tree=tree,
                stack_label=stack_label,
                generate=generate,
            )
            target = out_dir / primary_impl.path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(content, encoding="utf-8")
            for slot in test_slots:
                content = _generate_file(
                    _file_slot_to_spec(slot),
                    task=task,
                    tree=tree,
                    stack_label=stack_label,
                    generate=generate,
                )
                target = out_dir / slot.path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text(content, encoding="utf-8")

    # ── 5. Cross-cutting impl files (main.py, conftest, layouts, etc.) ──
    for slot in cross_cutting:
        target = out_dir / slot.path
        target.parent.mkdir(parents=True, exist_ok=True)
        content = _generate_file(
            _file_slot_to_spec(slot),
            task=task,
            tree=tree,
            stack_label=stack_label,
            generate=generate,
        )
        target.write_text(content, encoding="utf-8")
        log(f"      ✓ {slot.path}")

    # ── 6. Install + verify loop ──
    log("[5/6] installing and verifying...")
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

    stuck = [r.feature for r in feature_results if r.stuck]
    log(f"[6/6] complete. install_ok={install_ok} build_ok={build_ok} runs_ok={runs_ok} tests_ok={tests_ok} stuck={stuck}")

    report = BuildReport(
        title=plan.title,
        stack=asdict(plan.stack),
        out_dir=str(out_dir),
        file_count=len(layout.files),
        feature_count=len(plan.features),
        feature_results=[asdict(r) for r in feature_results],
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
        stuck_features=stuck,
        install_ok=install_ok,
        build_ok=build_ok,
        runs_ok=runs_ok,
        tests_ok=tests_ok,
    )

    # Persist the report for the user
    (sage_dir / "BUILD_REPORT.json").write_text(
        json.dumps(_clean_ansi(report.as_dict()), indent=2), encoding="utf-8"
    )

    return report


__all__ = [
    "BuildReport",
    "GenerateFn",
    "ProgressFn",
    "build_project_dynamic",
]
