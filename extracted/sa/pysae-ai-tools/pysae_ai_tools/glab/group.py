"""``glab`` command group — GitLab tooling."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="glab",
    help="GitLab tooling",
    no_args_is_help=True,
    lazy_subcommands={
        "find-issue": "pysae_ai_tools.glab.find_issue:main",
        "issue-audit": "pysae_ai_tools.glab.issue_audit.audit_issues:main",
        "issue-from-ai-note": "pysae_ai_tools.glab.issue_from_ai_note.cli:app",
        "issue-ready-check": "pysae_ai_tools.glab.issue_ready_check.cli:app",
        "renovate-notify": "pysae_ai_tools.glab.renovate_notify:main",
        "workflow-transition": "pysae_ai_tools.glab.workflow_transition:main",
        "issue-workflow-update": "pysae_ai_tools.glab.issue_workflow_update.cli:app",
        "issue-close-release": "pysae_ai_tools.glab.issue_close_release.cli:main",
        "clone-group": "pysae_ai_tools.glab.clone_group:main",
        "epic-from-issues": "pysae_ai_tools.glab.epic_from_issues:main",
        "epic-attach-issues": "pysae_ai_tools.glab.issue_find_epic:app",
        "weekly-data": "pysae_ai_tools.glab.weekly_data:main",
    },
)
