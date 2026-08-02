"""``slack`` command group — Slack tooling."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="slack",
    help="Slack tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "ask-review": "pysae_ai_tools.slack.ask_review:main",
        "get-token": "pysae_ai_tools.slack.get_token:main",
        "post-message": "pysae_ai_tools.slack.post_message:main",
        "release-status": "pysae_ai_tools.slack.release_status.cli:main",
        "release-file": "pysae_ai_tools.slack.release_file:main",
        "upload-file": "pysae_ai_tools.slack.upload_file:main",
        "update-message": "pysae_ai_tools.slack.update_message:main",
        "mark-merged": "pysae_ai_tools.slack.mark_merged:main",
        "find-thread": "pysae_ai_tools.slack.find_thread:main",
        "set-status-line": "pysae_ai_tools.slack.set_status_line:main",
        "find-user": "pysae_ai_tools.slack.find_user:main",
    },
)
