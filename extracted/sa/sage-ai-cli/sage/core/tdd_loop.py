"""Test-first, iterate-until-green generation loop.

For each `Feature`:
  1. Generate the failing test from the acceptance criteria.
  2. Generate the impl with the test in context.
  3. Run the test. If green, done.
  4. If red, regenerate the impl with the failure log appended.
  5. Loop until green — no fixed cap (per user request).

Safety: a `StuckTracker` watches failure counts. If 3 consecutive rounds
fail to reduce the failure count, mark the feature as `stuck` and move
on. Without this a single impossible test (stub returning wrong type,
unreachable network, etc.) would lock the whole build forever.
"""

from __future__ import annotations

import os
from collections import deque
from dataclasses import dataclass
from pathlib import Path
from typing import Callable

from sage.core.spec_decomposer import Feature


GenerateFn = Callable[[str], str]
# (test_path, impl_path) -> (ok, log, failure_count)
TestRunnerFn = Callable[[Path, Path], tuple[bool, str, int]]


@dataclass
class RoundResult:
    round: int
    ok: bool
    failures: int
    log: str


@dataclass
class FeatureResult:
    feature: str
    ok: bool
    stuck: bool
    rounds: int
    failures: int
    history: list[RoundResult]


class StuckTracker:
    """Tracks failure-count over rounds. Flags 'stuck' when no progress.

    Definition of stuck: `threshold` consecutive rounds where the failure
    count did not strictly decrease. Zero failures (green) never counts
    as stuck.
    """

    def __init__(self, threshold: int = 7):
        self.threshold = threshold
        self._history: deque[int] = deque(maxlen=threshold)

    def record(self, failures: int) -> None:
        self._history.append(failures)

    def is_stuck(self) -> bool:
        if len(self._history) < self.threshold:
            return False
        # Green = not stuck
        if all(f == 0 for f in self._history):
            return False
        # Did failures strictly decrease across the window?
        decreased = any(
            self._history[i] < self._history[i - 1] for i in range(1, len(self._history))
        )
        return not decreased


# ──────────────────────── prompt builders ──────────────────────────────


_TEST_PROMPT = """Write a failing test for this feature.

Feature: {name}
Description: {description}

Acceptance criteria:
{acceptance}

## CRITICAL: Import the implementation using EXACTLY this path

The implementation file is at: {impl_path}
The test file will be at: {test_path}

For Python tests, use this import (copy exactly):
  {python_import_line}

For TypeScript/JS tests, use this import (copy exactly):
  {js_import_line}

Framework: {test_framework}

Rules:
- Use EXACTLY the import shown above — do NOT guess or invent paths.
- Each acceptance criterion becomes one test case.
- The test must fail when no implementation exists (imports/calls the real module).
- Output ONLY the test code, no prose, no markdown fences.
"""


def _python_import_line(impl_path: Path, test_path: Path) -> str:
    """Convert impl file path to a Python import statement."""
    # Convert path to module: services/backend/main.py → services.backend.main
    parts = impl_path.with_suffix("").parts
    module = ".".join(parts)
    return f"from {module} import app  # adjust symbol as needed"


def _js_import_line(impl_path: Path, test_path: Path) -> str:
    """Compute a relative JS import path from test to impl."""
    try:
        rel = os.path.relpath(impl_path.with_suffix(""), test_path.parent)
        # Normalize to forward slashes
        rel = rel.replace(os.sep, "/")
        if not rel.startswith("."):
            rel = "./" + rel
        return f"import ... from '{rel}'  // adjust import as needed"
    except Exception:
        return f"import ... from '{impl_path}'  // adjust import as needed"


_IMPL_PROMPT = """Write the implementation that makes the provided test pass.

Feature: {name}
Description: {description}

## Test file at {test_path}

```{lang}
{test_code}
```

## Previous attempt error log (if any)

{previous_error}

Output ONLY the production code for {impl_path}. No prose, no fences.
"""


# ──────────────────────── single-feature loop ─────────────────────────


def _strip_fences(text: str) -> str:
    """Sanitize LLM output before writing to a file.

    Delegates to `principal_engineer.strip_code_fences` so the TDD loop
    benefits from the same reasoning-tag stripping (qwen3 / deepseek-r1
    chain-of-thought) and markdown-fence stripping.
    """
    if not text:
        return ""
    # Late import to avoid a top-level cycle (principal_engineer doesn't
    # import tdd_loop, but keeping this lazy is cheap insurance).
    from sage.core.principal_engineer import strip_code_fences

    return strip_code_fences(text).rstrip() + "\n"


def _detect_test_framework(impl_path: Path) -> str:
    suffix = impl_path.suffix
    return {
        ".py": "pytest",
        ".ts": "vitest",
        ".tsx": "@testing-library/react-native + jest",
        ".js": "vitest",
        ".jsx": "vitest",
        ".go": "go test",
        ".rs": "cargo test",
        ".java": "JUnit 5",
        ".kt": "JUnit 5",
        ".swift": "XCTest",
        ".dart": "flutter test",
    }.get(suffix, "the project's test framework")


def _lang_label(impl_path: Path) -> str:
    return {
        ".py": "python",
        ".ts": "typescript",
        ".tsx": "tsx",
        ".js": "javascript",
        ".jsx": "jsx",
        ".go": "go",
        ".rs": "rust",
        ".java": "java",
        ".kt": "kotlin",
        ".swift": "swift",
        ".dart": "dart",
    }.get(impl_path.suffix, "")


def run_feature_tdd(
    feature: Feature,
    *,
    impl_path: Path,
    test_path: Path,
    generate: GenerateFn,
    run_tests: TestRunnerFn,
    stuck_threshold: int = 3,
    progress: Callable[[str], None] | None = None,
) -> FeatureResult:
    """Run the TDD loop for ONE feature, iterating until green or stuck."""
    log_fn = progress or (lambda _msg: None)
    history: list[RoundResult] = []
    tracker = StuckTracker(threshold=stuck_threshold)

    # ── Step 1: generate the test FIRST ──
    python_import_line = _python_import_line(impl_path, test_path)
    js_import_line = _js_import_line(impl_path, test_path)
    test_prompt = _TEST_PROMPT.format(
        name=feature.name,
        description=feature.description,
        acceptance="\n".join(f"  - {a}" for a in feature.acceptance) or "  - (none)",
        test_framework=_detect_test_framework(impl_path),
        impl_path=impl_path,
        test_path=test_path,
        python_import_line=python_import_line,
        js_import_line=js_import_line,
    )
    test_code = _strip_fences(generate(test_prompt))
    test_path.parent.mkdir(parents=True, exist_ok=True)
    test_path.write_text(test_code, encoding="utf-8")
    log_fn(f"  [{feature.name}] wrote test")

    previous_error = "(first attempt — no error log yet)"
    impl_path.parent.mkdir(parents=True, exist_ok=True)

    # ── Step 2+: impl loop ──
    round_num = 0
    while True:
        round_num += 1
        impl_prompt = _IMPL_PROMPT.format(
            name=feature.name,
            description=feature.description,
            test_path=test_path,
            lang=_lang_label(impl_path),
            test_code=test_code,
            impl_path=impl_path,
            previous_error=previous_error,
        )
        impl_code = _strip_fences(generate(impl_prompt))
        # Re-create parent dirs every iteration — defends against the user
        # (or a flaky filesystem) wiping the output dir mid-build.
        impl_path.parent.mkdir(parents=True, exist_ok=True)
        test_path.parent.mkdir(parents=True, exist_ok=True)
        impl_path.write_text(impl_code, encoding="utf-8")

        ok, run_log, failures = run_tests(test_path, impl_path)
        history.append(RoundResult(round=round_num, ok=ok, failures=failures, log=run_log))
        log_fn(f"  [{feature.name}] round {round_num}: ok={ok} failures={failures}")

        if ok:
            return FeatureResult(
                feature=feature.name,
                ok=True,
                stuck=False,
                rounds=round_num,
                failures=0,
                history=history,
            )

        tracker.record(failures)
        if tracker.is_stuck():
            log_fn(f"  [{feature.name}] STUCK after {round_num} rounds")
            return FeatureResult(
                feature=feature.name,
                ok=False,
                stuck=True,
                rounds=round_num,
                failures=failures,
                history=history,
            )

        # Detect import errors — the test has a wrong import path.
        # Regenerating the impl cannot fix this; regenerate the test instead.
        import_error_patterns = [
            "ImportError", "ModuleNotFoundError", "Cannot find module",
            "Module not found", "Cannot resolve", "Failed to resolve",
        ]
        is_import_error = any(p in run_log for p in import_error_patterns)

        if is_import_error and round_num <= 2:
            # Regenerate the test with an explicit import hint
            corrected_test_prompt = _TEST_PROMPT.format(
                name=feature.name,
                description=feature.description,
                acceptance="\n".join(f"  - {a}" for a in feature.acceptance) or "  - (none)",
                test_framework=_detect_test_framework(impl_path),
                impl_path=impl_path,
                test_path=test_path,
                python_import_line=_python_import_line(impl_path, test_path),
                js_import_line=_js_import_line(impl_path, test_path),
            ) + f"\n\nPrevious attempt failed with:\n{run_log[-1000:]}\nFix the import path."
            test_code = _strip_fences(generate(corrected_test_prompt))
            test_path.write_text(test_code, encoding="utf-8")
            log_fn(f"  [{feature.name}] regenerated test (import error detected)")
            previous_error = "(test regenerated — first impl attempt)"
            continue

        # Feed the failure log into the next prompt
        previous_error = run_log[-2000:]  # cap to avoid huge prompts


__all__ = [
    "FeatureResult",
    "GenerateFn",
    "RoundResult",
    "StuckTracker",
    "TestRunnerFn",
    "run_feature_tdd",
]
