"""Collection guard for the analytics tests that need ``ultralytics``.

Six modules in this directory do a bare module-level ``from ultralytics import
YOLO``. ``ultralytics`` is deliberately absent from the wheel and from CI: it
drags in torch and ~2.3 GB of CUDA wheels, and the deployment image provides it
instead (CLAUDE.md 8.9 / 11e-G).

That combination was invisible for as long as it has existed. ``testpaths =
["tests"]`` keeps this directory out of a normal ``pytest`` run entirely, so
nothing ever imported these modules. CI's per-subfolder selective testing
(INC-104 C4) does reach them: when a sibling module under
``src/matrice_analytics/analytics`` changes, it passes that directory to pytest
by name, collection hits the six bare imports, and the ``ImportError`` aborts
the WHOLE run before a single test executes -- which is how a promotion with no
analytics test failures reported ``Interrupted: 6 errors during collection``.

Skipping by name keeps the directory collectable either way: with
``ultralytics`` installed every module runs as before, without it the six are
ignored and their siblings still run. The alternative -- ``pytest.importorskip``
at the top of each module -- edits six large legacy files and pulls every
pre-existing lint and typing finding in them into an unrelated change.
"""

from __future__ import annotations

from importlib.util import find_spec

#: Modules whose imports cannot survive a missing ``ultralytics``.
_NEEDS_ULTRALYTICS = [
    "test_identity_analytics.py",
    "test_incident_analytics.py",
    "test_quality_analytics.py",
    "test_safety_analytics.py",
    "test_volume_analytics.py",
    "test_zone_analytics.py",
]

collect_ignore = [] if find_spec("ultralytics") is not None else list(_NEEDS_ULTRALYTICS)
