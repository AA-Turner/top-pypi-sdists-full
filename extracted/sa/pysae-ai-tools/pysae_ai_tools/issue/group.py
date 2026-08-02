"""``issue`` command group — provider-neutral issue, epic and label operations."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="issue",
    help="Issue, epic and label operations (provider-neutral: GitLab / GitHub)",
    no_args_is_help=True,
    lazy_subcommands={
        "create": "pysae_ai_tools.issue.create:main",
        "list": "pysae_ai_tools.issue.list_issues:main",
        "view": "pysae_ai_tools.issue.view:main",
        "update": "pysae_ai_tools.issue.update:main",
        "close": "pysae_ai_tools.issue.close:main",
        "reopen": "pysae_ai_tools.issue.reopen:main",
        "note": "pysae_ai_tools.issue.note:main",
        "whoami": "pysae_ai_tools.issue.whoami:main",
        "label": "pysae_ai_tools.issue.label.group:app",
        "epic": "pysae_ai_tools.issue.epic.group:app",
    },
)
