from __future__ import annotations

import os
import re
import sys
import typing as t

from dbt.contracts.graph.manifest import ManifestNode
from dbt.config.runtime import RuntimeConfig
from dbt.version import get_installed_version
from query_cache_common.utils import str_to_bool

if t.TYPE_CHECKING:
    from sqlglot import Expr
    from sqlglot.expressions import Table


def _get_dbt_version() -> tuple[int, int, int]:
    dbt_version = get_installed_version()
    return (
        int(dbt_version.major or "0"),
        int(dbt_version.minor or "0"),
        int(dbt_version.patch or "0"),
    )


DBT_VERSION = _get_dbt_version()


def is_full_refresh(config: RuntimeConfig, node: ManifestNode) -> bool:
    node_full_refresh = getattr(node.config, "full_refresh", None)
    if node_full_refresh:
        # If the node config explicitly requests full refresh, respect that
        return True
    # This is only full-refresh if the node didn't explicitly opt out and the CLI requested it
    return node_full_refresh is None and config.args.full_refresh


def is_incremental_or_snapshot(node: ManifestNode) -> bool:
    return node.get_materialization() == "incremental" or node.resource_type == "snapshot"


def is_view(node: ManifestNode) -> bool:
    return (node.get_materialization() or "view") in ("view", "materialized_view")


_KNOWN_MATERIALIZATIONS = frozenset(
    {"table", "view", "materialized_view", "incremental", "ephemeral", "semantic_view", "snapshot"}
)

# dbt's built-in incremental strategies. Any other strategy is a user-defined
# custom strategy backed by a `get_incremental_<strategy>_sql` macro
# (see https://docs.getdbt.com/docs/build/incremental-strategy#custom-strategies).
_KNOWN_INCREMENTAL_STRATEGIES = frozenset(
    {"append", "delete_insert", "merge", "insert_overwrite", "microbatch"}
)


def _normalize_incremental_strategy(strategy: str) -> str:
    return strategy.replace("+", "_").lower()


def is_custom_incremental_strategy(node: ManifestNode) -> bool:
    if node.get_materialization() != "incremental":
        return False
    strategy = getattr(node.config, "incremental_strategy", None)
    # A missing strategy means dbt falls back to the adapter's default, which is
    # always one of the built-in strategies.
    return (
        strategy is not None
        and _normalize_incremental_strategy(strategy) not in _KNOWN_INCREMENTAL_STRATEGIES
    )


def is_custom_materialization(node: ManifestNode) -> bool:
    materialization = node.get_materialization()
    if materialization is None:
        return False
    if materialization not in _KNOWN_MATERIALIZATIONS:
        return True
    return is_custom_incremental_strategy(node)


def is_table(node: ManifestNode) -> bool:
    # If get_materialization() returns None (i.e., materialization is not set in the node config),
    # dbt treats the model as a "view" by default. Therefore, we default to "view" here to match dbt's behavior.
    return (node.get_materialization() or "view") not in (
        "view",
        "materialized_view",
        "ephemeral",
        "semantic_view",
    )


def is_ci_environment() -> bool:
    """Detect if we're running in a CI environment by checking common CI environment variables.

    Returns:
        True if running in a CI environment, False otherwise.
    """
    ci_env_vars = [
        "CI",
        "GITHUB_ACTIONS",
        "GITLAB_CI",
        "CIRCLECI",
        "JENKINS_URL",
        "TEAMCITY_VERSION",
        "TRAVIS",
        "BUILDKITE",
    ]
    return any(str_to_bool(os.getenv(var, "false")) for var in ci_env_vars)


def is_non_interactive_environment() -> bool:
    """Detect if we're running in a non-interactive environment by checking if stdin or stdout
    is not connected to a TTY.

    Returns:
        True if either stdin or stdout has no TTY (non-interactive), False if both have TTYs.
    """
    if not sys.stdin or not sys.stdout:
        return True
    try:
        stdin_is_tty = sys.stdin.isatty()
        stdout_is_tty = sys.stdout.isatty()
        return not (stdin_is_tty and stdout_is_tty)
    except Exception:
        return True


def format_time_saved(ms: int) -> str:
    total_seconds = ms / 1000
    if total_seconds < 60:
        return f"{total_seconds:.2f}s"
    total_seconds = int(total_seconds)
    if total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        if seconds == 0:
            return f"{minutes}m"
        return f"{minutes}m{seconds}s"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    if minutes == 0:
        return f"{hours}h"
    return f"{hours}h{minutes}m"


NON_ALNUM_PATTERN = re.compile(r"\W")


def sanitize_name(name: str) -> str:
    return NON_ALNUM_PATTERN.sub("_", name)


# Remove once sqlglot is >=27.29.0 and use function from sqlglot directly
def find_tables(expression: Expr) -> t.Set[Table]:
    """
    Find all tables referenced in a query.

    Args:
        expressions: The query to find the tables in.

    Returns:
        A set of all the tables.
    """
    from sqlglot.optimizer.scope import traverse_scope

    return {
        table
        for scope in traverse_scope(expression)
        for table in scope.tables
        if table.name and table.name not in scope.cte_sources
    }


def set_invocation_context() -> None:
    if DBT_VERSION >= (1, 8, 0):
        from dbt_common.context import set_invocation_context

        set_invocation_context(os.environ)


def get_dbt_command_name(source: t.Any) -> t.Optional[str]:
    """Returns the active dbt subcommand name (e.g. ``"run"``, ``"compile"``), lowercased.

    Accepts any object exposing a ``which`` attribute — typically the dbt flags
    singleton (``dbt.flags.get_flags()``) or ``RuntimeConfig.args``. Returns
    ``None`` if no string command name is available.
    """
    name = getattr(source, "which", None)
    if not isinstance(name, str) or not name:
        return None
    return name.lower()
