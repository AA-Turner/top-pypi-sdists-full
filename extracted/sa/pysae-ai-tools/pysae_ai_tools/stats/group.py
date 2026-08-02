"""``stats`` command group — engineering & ops KPI collection."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="stats",
    help="Engineering & ops KPI collection",
    no_args_is_help=True,
    lazy_subcommands={
        "kpi": "pysae_ai_tools.stats.kpi.cli:app",
    },
)
