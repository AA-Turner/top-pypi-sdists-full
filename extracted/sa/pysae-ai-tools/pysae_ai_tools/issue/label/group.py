"""``pysae-ai-tools issue label`` — owner-scoped label operations."""

from ...common.lazy_group import LazyGroup

app = LazyGroup(
    name="label",
    help="Owner-scoped label operations",
    no_args_is_help=True,
    lazy_subcommands={
        "ensure": "pysae_ai_tools.issue.label.ensure:main",
    },
)
