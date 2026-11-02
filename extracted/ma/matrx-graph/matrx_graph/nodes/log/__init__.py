"""``log.*`` — the workflow's own diagnostic record.

A workflow that hits a serious problem and recovers from it must be able to
SAY SO. Before this pack it could only fail the run or stay silent, and
silence is what the Agent Foundry chose while shipping no component (Arman,
2026-08-23). Rows land in ``workflow.run_log`` — the USER's table, org-scoped
and read by the run's owner, never the platform's ``system_error`` queue.
"""

from matrx_graph.nodes.log.record import RecordIssueExecutor
from matrx_graph.run_log import MAX_ENTRIES_PER_RUN, SEVERITIES

__all__ = ["MAX_ENTRIES_PER_RUN", "SEVERITIES", "RecordIssueExecutor"]
