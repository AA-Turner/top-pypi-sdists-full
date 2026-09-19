"""Wall-clock budgets of the host container phase.

They live here (not in ``docker_cli`` or the ``containers`` package, whose
``__init__`` imports the whole scan graph) so the ``--all-users`` child-timeout
arithmetic in ``windows_users`` can depend on them without an import cycle:
``docker_cli`` imports ``file_collector``, which imports ``windows_users``.
"""

SCAN_BASE_TIME_BUDGET_S = 30
SCAN_PER_CONTAINER_TIME_BUDGET_S = 10
SCAN_MAX_TIME_BUDGET_S = 300

# Docker, podman and nerdctl each receive an independent budget (see
# ``collect._scan_running_containers``); k3s does too but is Linux-only, so a
# Windows child never spends it.
HOST_CONTAINER_RUNTIMES_WITH_OWN_BUDGET = 3
HOST_CONTAINER_PHASE_MAX_TIME_BUDGET_S = (
    SCAN_MAX_TIME_BUDGET_S * HOST_CONTAINER_RUNTIMES_WITH_OWN_BUDGET
)
