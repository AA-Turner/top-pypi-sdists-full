"""``agent`` command group — agent batch orchestrator."""

from ..common.lazy_group import LazyGroup

app = LazyGroup(
    name="agent",
    help="Agent batch orchestrator",
    no_args_is_help=True,
    lazy_subcommands={
        "design-run": "pysae_ai_tools.agent.design.run:app",
        "candidates": "pysae_ai_tools.agent.candidates:main",
        "score-prompt": "pysae_ai_tools.agent.score_prompt_cmd:main",
        "rank": "pysae_ai_tools.agent.rank:main",
        "dep-graph": "pysae_ai_tools.agent.dep_graph_cmd:main",
        "label": "pysae_ai_tools.agent.label_cmd:app",
        "advise": "pysae_ai_tools.agent.advise_cmd:main",
        "watch-deploy": "pysae_ai_tools.agent.watch_deploy_cmd:main",
        "merge-gate": "pysae_ai_tools.agent.merge_gate_cmd:main",
        "batch-branch": "pysae_ai_tools.agent.batch_branch_cmd:app",
        "checkpoint": "pysae_ai_tools.agent.checkpoint_cmd:app",
        "report": "pysae_ai_tools.agent.report_cmd:main",
    },
)
