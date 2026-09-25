"""CLI command metadata shared with runtime prompts without loading cyclopts."""

LAZY_COMMANDS: dict[str, tuple[str, str | None, str]] = {
    "airt": (
        "dreadnode.app.cli.airt",
        None,
        "AI red teaming for models and agents. Launch attacks with `run` / `run-suite`; review results from the CLI (`analytics`, `traces`, `trials`, `findings`) or in the web app under AI Red Teaming — overview dashboard, per-assessment view, trace view, and custom report builder.",
    ),
    "capability": (
        "dreadnode.app.cli.capability",
        None,
        "Composable packages of agents, tools, and skills — capture domain expertise, share it, and refine it over time.",
    ),
    "dataset": (
        "dreadnode.app.cli.dataset",
        None,
        "Versioned data for training, optimization, and evaluation — the ground truth your agents learn from.",
    ),
    "environment": (
        "dreadnode.app.cli.environment",
        "env",
        "Provision and tear down task environments (sandboxed task instances).",
    ),
    "evaluation": (
        "dreadnode.app.cli.evaluation",
        None,
        "Batch evaluation of agents against security tasks — measure capability, track regressions, and compare models.",
    ),
    "inference-model": (
        "dreadnode.app.cli.inference_model",
        "llm",
        "Discover platform inference models and validate model IDs.",
    ),
    "judge": (
        "dreadnode.app.cli.judge",
        None,
        "Run a judge over an agent trajectory or other evidence.",
    ),
    "model": (
        "dreadnode.app.cli.model",
        None,
        "Fine-tuned weights and adapters — checkpoints from training, LoRAs, and quantized models ready for deployment.",
    ),
    "optimize": ("dreadnode.app.cli.optimize", None, "Optimize agents with jobs."),
    "runtime": ("dreadnode.app.cli.runtime", None, "Manage agent runtime environments."),
    "sandbox": ("dreadnode.app.cli.sandbox", None, "Inspect platform sandboxes."),
    "secret": ("dreadnode.app.cli.secret", None, "Discover user secrets (read-only)."),
    "session": (
        "dreadnode.app.cli.session",
        None,
        "Browse, inspect, and export agent session trajectories — the record of what an agent did during a run.",
    ),
    "task": (
        "dreadnode.app.cli.task",
        None,
        "Environments with success conditions that agents operate in — for evaluations, training, and optimization.",
    ),
    "task-set": (
        "dreadnode.app.cli.task_set",
        None,
        "Named, org-scoped lists of task references — curate suites and run them as one evaluation.",
    ),
    "train": ("dreadnode.app.cli.train", None, "Fine-tune models with hosted SFT and RL jobs."),
    "workflow": (
        "dreadnode.app.cli.workflow",
        None,
        "Authored multi-step agent pipelines: definitions, runs, and approvals.",
    ),
    "worlds": ("dreadnode.app.cli.worlds", None, "Work with simulated network environments."),
}

BUILTIN_COMMAND_SUMMARIES: dict[str, str] = {
    "login": "Authenticate with the Dreadnode platform.",
    "whoami": "Show current user, organization, and profile context.",
    "update": "Update the Dreadnode CLI to the latest version on PyPI.",
    "serve": "Host a runtime server for the TUI.",
}
