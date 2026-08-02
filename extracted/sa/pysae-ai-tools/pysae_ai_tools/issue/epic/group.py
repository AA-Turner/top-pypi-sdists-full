"""``pysae-ai-tools issue epic`` — epic operations."""

from ...common.lazy_group import LazyGroup

app = LazyGroup(
    name="epic",
    help="Epic operations",
    no_args_is_help=True,
    lazy_subcommands={
        "list": "pysae_ai_tools.issue.epic.list_epics:main",
        "view": "pysae_ai_tools.issue.epic.view:main",
        "create": "pysae_ai_tools.issue.epic.create:main",
        "update": "pysae_ai_tools.issue.epic.update:main",
        "attach": "pysae_ai_tools.issue.epic.attach:main",
    },
)
