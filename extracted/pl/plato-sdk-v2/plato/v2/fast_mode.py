"""Fast-mode step planning shared by the async and sync FlowExecutors.

Recorded sim flows carry two kinds of dead time that dominate wall-clock
(89-97% of a stock login) without doing any work:

- fixed ``wait`` sleeps recorded between actions, and
- a trailing confirmation tail after the last real action (a slow
  dashboard-render ``wait_for_selector``, ``verify`` steps, ...), which exists
  to *observe* the outcome, not to produce it.

Fast mode skips both at execution time, so no flow data changes. Mid-flow
``wait_for_selector``/``verify`` steps are kept: they gate a later action on
real page state, which is cheap when already true and load-bearing when not.
"""

from __future__ import annotations

from collections.abc import Sequence

FAST_MODE_ACTION_TYPES = frozenset({"click", "fill", "navigate"})


def fast_mode_skips(step_types: Sequence[str]) -> frozenset[int]:
    """Indices of steps a fast-mode execution skips.

    Skips every ``wait`` step, plus everything after the last
    ``click``/``fill``/``navigate`` (the confirmation tail). A flow with no
    action steps only has its ``wait`` steps skipped.
    """
    last_action = max(
        (index for index, step_type in enumerate(step_types) if step_type in FAST_MODE_ACTION_TYPES),
        default=-1,
    )
    return frozenset(
        index
        for index, step_type in enumerate(step_types)
        if step_type == "wait" or (last_action != -1 and index > last_action)
    )


__all__ = ["FAST_MODE_ACTION_TYPES", "fast_mode_skips"]
