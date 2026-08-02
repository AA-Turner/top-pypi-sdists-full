"""``skills`` command group — publish whitelisted Claude Code skills to the Anthropic Workspace."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="skills",
    help="Publish whitelisted Claude Code skills to the Anthropic Workspace.",
    no_args_is_help=True,
    lazy_subcommands={
        "push": "pysae_ai_tools.skills.push:app",
        "route-eval": "pysae_ai_tools.skills.route_eval:app",
    },
)
