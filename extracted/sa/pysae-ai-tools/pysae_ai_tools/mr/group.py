"""``mr`` command group — provider-neutral merge-request / pull-request operations."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="mr",
    help="Merge-request / pull-request operations (provider-neutral: GitLab / GitHub)",
    no_args_is_help=True,
    lazy_subcommands={
        "create": "pysae_ai_tools.mr.create:main",
        "list": "pysae_ai_tools.mr.list_mrs:main",
        "view": "pysae_ai_tools.mr.view:main",
        "update": "pysae_ai_tools.mr.update:main",
        "note": "pysae_ai_tools.mr.note:main",
        "approve": "pysae_ai_tools.mr.approve:main",
        "approvals": "pysae_ai_tools.mr.approvals:main",
        "rebase": "pysae_ai_tools.mr.rebase:main",
        "merge": "pysae_ai_tools.mr.merge:main",
        "review-note": "pysae_ai_tools.mr.review_note:app",
        "whoami": "pysae_ai_tools.mr.whoami:main",
    },
)
