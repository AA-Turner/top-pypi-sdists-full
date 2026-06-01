"""Reason codes for autonomous OutcomeReports.

Module-level string constants (not an Enum) because reason values are
serialized over the wire as plain strings. Constants with ``{placeholder}``
suffixes are format templates — call ``.format(...)`` at the use site.
"""

from __future__ import annotations

NO_ADAPTER = "no_adapter:{framework}"
UNKNOWN_ACTION_TYPE = "unknown_action_type:{action_type}"
UNKNOWN_INTERVENTION_KIND = "unknown_intervention_kind"
ADAPTER_RAISED = "adapter_raised:{exc}"
IN_STEP_ALREADY_HANDLED_INLINE = "in_step_already_handled_inline"
AUTONOMOUS_RETRY = "autonomous_retry"
AUTONOMOUS_REWRITE_ARGS = "autonomous_rewrite_args"
AUTONOMOUS_FORCE_FALLBACK = "autonomous_force_fallback"
AUTONOMOUS_BREAK_LOOP = "autonomous_break_loop"
