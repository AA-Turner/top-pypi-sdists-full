from __future__ import annotations

from trajectory.lib.cli.cookbook_prompt import COOKBOOK_URL
from trajectory.lib.cli.guides import DOCS_URL


class SetupPrompt:
  @staticmethod
  def benchmark(organization_key: str | None, agent_id: str | None) -> str:
    # Keep the workflow aligned with the platform's agent-setup-prompts.ts setupPrompt.
    organization = f"org {organization_key}" if organization_key else "the current organization"
    agent = f" to agent {agent_id}" if agent_id else ""
    return f"""Set up a benchmark in Trajectory {organization} following {COOKBOOK_URL}/blob/main/examples/gsm8k/README.md; see the docs ({DOCS_URL}) and cookbook ({COOKBOOK_URL}).

Follow the benchmark's data-use restrictions: if all records are evaluation-only or do_not_train, still pick a model and upload, but skip training options, training and checkpoint eval. Use information already supplied by me or established in the repository; ask only for missing decisions.

Resolve the remaining decisions one at a time:
1. Benchmark: from the cookbook, this repo's, a well-known one, or other (research first)?
2. Model: one from client.evals.list_models() for evaluation-only data, otherwise client.training.list_models().
3. Plan the upload{agent}. If trainable, propose a small smoke run (2 steps, batch 1, minimal supported group size, no in-training eval) within client.training.list_options() bounds, with estimated cost from list_models() pricing.
4. Confirm agent name, benchmark, task count, models, and training config and cost if training; wait for my yes.

After confirmation, upload and recheck model options with the returned bench_id. Then diagnose, omitting val_num_tasks, val_trajectories_per_task and val_max_concurrent_trajectories; eval the selected model and another from client.evals.list_models(), fix errors and rerun (incl. eval options like trajectory_timeout_seconds, max_turns_per_trajectory); warn if baseline ~1.0; if trainable, train and eval the final checkpoint. No deploy."""

  @staticmethod
  def sdk_instructions(organization_key: str | None) -> str:
    organization = (
      f'Confirm client.organizations.retrieve_current()["organization_key"] is {organization_key} before creating or changing resources; stop remote work on a mismatch.'
      if organization_key
      else 'Read client.organizations.retrieve_current()["organization_key"] before creating or changing resources and use that authenticated organization.'
    )
    return f"""Use this repository's package manager and interpreter to install or update trajectory-sdk; respect dependency constraints and report conflicts.

Install the skills with `npx skills add https://docs.trajectory.ai --skill trajectory --skill agent-feedback`, selecting the coding agent in use. Read the installed trajectory skill before SDK work: open trajectory/SKILL.md at the location reported by the installer, then read the relevant bundled guides. Setup, Python-only installation, and refresh: https://docs.trajectory.ai/coding-agents. When adapting a cookbook example, preserve its tasks, tools, and scoring.

{organization}
After that check, use PlatformLinks.from_client(client) from trajectory.lib.platform_links for production. For another API environment, supply its matching platform_url; ask for that URL if it is unknown rather than guessing a production link. Share a labeled resource link as soon as its ID exists, send another update with the outcome and link when work finishes, and link the specific evidence for results or failures. State what is running, verified, or blocked and what I can inspect next.

If you encounter concrete Trajectory API, SDK, or documentation friction, use the installed agent-feedback skill. Exclude credentials and private content; feedback failures must not block the requested task."""
