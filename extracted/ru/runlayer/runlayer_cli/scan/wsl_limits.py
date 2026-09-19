"""Shared defensive caps for Windows-host WSL scanning."""

MAX_WSL_DISTROS = 16
MAX_WSL_HOMES = 4
MAX_WSL_HOMES_TOTAL = MAX_WSL_DISTROS * MAX_WSL_HOMES
MAX_WSL_HOME_PROBES = 32
MAX_WSL_CLIENT_CONTEXTS = MAX_WSL_DISTROS * (MAX_WSL_HOMES + 1)

# Wall-clock budgets of the WSL phases. They live here (not in the phase
# modules) so the --all-users child-timeout arithmetic in windows_users can
# depend on them without an import cycle.
WSL_SCAN_MAX_TIME_BUDGET_S = 300
WSL_PRESENCE_TIME_BUDGET_S = 30.0
WSL_CONTAINER_SCAN_TIME_BUDGET_S = 30.0
