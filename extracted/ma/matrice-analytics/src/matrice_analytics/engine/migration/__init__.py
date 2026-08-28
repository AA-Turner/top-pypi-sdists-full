"""The payload-diff harness -- the gate on every migration wave.

Deletion is the **output** of a migration wave, never the input (``PHASE2_PLAN`` §5,
decision **D2**).  Before any tier-3 deletion the app must run on the new engine **and**
its payloads must have been diffed against the legacy output on the same input.  Not "the
tests pass" -- the payloads match.  This package is what turns that sentence into a
command with an exit code.

    from matrice_analytics.engine.migration import compare_usecase, generate_frames

    report = compare_usecase("people_counting", "apps/people_counting", generate_frames(250))
    if not report.passed:
        print(report.render())

Three modules:

* :mod:`~matrice_analytics.engine.migration.differ` -- the semantic comparison and the
  registry of deliberate changes.  No engine dependencies at all; it compares dicts.
* :mod:`~matrice_analytics.engine.migration.keymap` -- the **verification-only** record of
  which legacy metric key is the same measurement as which new one, so the differ compares
  the right pairs.  It changes nothing the engine emits; an unmapped key stays BREAKING.
* :mod:`~matrice_analytics.engine.migration.harness` -- runs both engines on one
  deterministic synthetic input.

Neither imports ``matrice_analytics.post_processing`` at module scope: **PY-20** is fixed
for the engine only, so the legacy tree still executes ~180 modules and pulls in torch and
cv2.  The legacy import lives inside
:func:`~matrice_analytics.engine.migration.harness.run_legacy`.
"""

from __future__ import annotations

from matrice_analytics.engine.migration.differ import (
    DEFAULT_TOLERANCE,
    DELIBERATE_CHANGES,
    Classification,
    DeliberateChange,
    DiffContext,
    Difference,
    DiffReport,
    TolerancePolicy,
    Verdict,
    diff_results_agg,
)
from matrice_analytics.engine.migration.harness import (
    BASE_FRAME_TS,
    DEFAULT_FPS,
    DEFAULT_RESOLUTION,
    EngineRun,
    FrameSequence,
    SyntheticFrame,
    compare_usecase,
    default_stream_info,
    dump_frames_to_json,
    generate_frames,
    load_frames_from_json,
    run_legacy,
    run_new_engine,
)
from matrice_analytics.engine.migration.keymap import (
    EMPTY_KEY_MAP,
    VERIFICATION_KEY_MAPS,
    MetricKeyPair,
    MetricSide,
    UnpairedMetricKey,
    UsecaseKeyMap,
    key_map_for,
)

__all__ = [
    "BASE_FRAME_TS",
    "DEFAULT_FPS",
    "DEFAULT_RESOLUTION",
    "DEFAULT_TOLERANCE",
    "DELIBERATE_CHANGES",
    "EMPTY_KEY_MAP",
    "VERIFICATION_KEY_MAPS",
    "Classification",
    "DeliberateChange",
    "DiffContext",
    "DiffReport",
    "Difference",
    "EngineRun",
    "FrameSequence",
    "MetricKeyPair",
    "MetricSide",
    "SyntheticFrame",
    "TolerancePolicy",
    "UnpairedMetricKey",
    "UsecaseKeyMap",
    "Verdict",
    "compare_usecase",
    "default_stream_info",
    "diff_results_agg",
    "dump_frames_to_json",
    "generate_frames",
    "key_map_for",
    "load_frames_from_json",
    "run_legacy",
    "run_new_engine",
]
