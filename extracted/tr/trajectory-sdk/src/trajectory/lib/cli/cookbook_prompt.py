from __future__ import annotations

from dataclasses import dataclass

from trajectory.lib.cli.guides import DOCS_URL

COOKBOOK_URL = "https://github.com/Trajectorylabs/trajectory-cookbook"


@dataclass(frozen=True)
class CookbookExample:
  name: str
  path: str
  description: str
  guidance: str
  can_train: bool = True

  @property
  def readme_url(self) -> str:
    return f"{COOKBOOK_URL}/blob/main/{self.path}/README.md"

  def prompt(self) -> str:
    if self.can_train:
      finish = f"""Use the confirmed smoke-run plan from the setup workflow for this trainable example.
Recheck supported training models and bounds using training options --bench-id BENCH_ID --json.
Prepare training.json and validate it with training create --config training.json --dry-run --json.
Keep the confirmed model, task split, steps, batch/group sizes, concurrency, token/time limits, and budget; ask again only if the scope or budget changes before launching training.
Training scripts may also submit evaluations; inspect all their side effects and defaults before proposing a command.
Submit the agreed run, retain its ID, and use training watch and training details to inspect progress, rewards, and checkpoints.
Compare the final checkpoint against the baselines on the same held-out tasks and evaluation settings. Do not promise improvement from a smoke run.
Training and checkpoint guide: {DOCS_URL}/guides/training"""
    else:
      finish = """This cookbook example is evaluation-only and has no official training split.
Stop after a graded evaluation. Do not create a training split from held-out tasks or launch training.
If I want to train, offer a separate GSM8K or T Factory setup instead."""
    return f"""Help me set up {self.name} from the official Trajectory cookbook and {"train a model" if self.can_train else "run an evaluation"}.
Cookbook: {COOKBOOK_URL}
Example guide: {self.readme_url}

Locate an existing cookbook checkout in this project first. Otherwise clone {COOKBOOK_URL}.git into a new trajectory-cookbook subdirectory; never overwrite existing files.
Read that checkout's instructions, {self.path}/README.md, and the relevant harness, ingestion, and training code before running commands. Record the checkout revision and follow its actual flags and prerequisites rather than inventing scripts.
Run cookbook commands from its repository root. Use the installed SDK for Python snippets; if a script uses an isolated environment, ensure it supports the selected saved profile and API origin instead of silently switching credentials or downgrading the CLI.

Example-specific setup:
{self.guidance}

Confirm the organization with whoami --json. Reuse a suitable agent and benchmark when available.
Inspect representative tasks locally, preserving task IDs, train/test boundaries, native tools, and the source grader. Keep reference answers and hidden tests out of actor inputs.
Start with one task or the smallest supported subset. Review ingestion scripts for implicit diagnostics and model calls; confirm before any remote submission, including image builds and diagnostics.
Inspect recorded endings, failures, and rewards; zero is a valid grade, while a missing grade or ready image alone does not prove success.
Discover evaluation models/options, then run a small held-out baseline using the selected model and compatible source settings. Keep IDs and resumable commands; do not resubmit because a watch timed out.
Setup and diagnostics: {DOCS_URL}/guides/spec
Evaluation guide: {DOCS_URL}/guides/evaluations

{finish}
Do not deploy a model as part of this walkthrough. Explain each next step with the relevant cookbook/docs link and report only results actually observed."""


EXAMPLES = {
  "gsm8k": CookbookExample(
    "GSM8K",
    "examples/gsm8k",
    "Recommended first training run: grade-school math",
    "Follow the README's Python walkthrough, including a one-task diagnostic, upload, baseline, and training. There is no ingest.py or train.py required by this walkthrough. Preserve submit_answer grading and the separate training and held-out problems; begin with a small subset before the documented 64/16 upload.",
  ),
  "t-factory": CookbookExample(
    "T Factory",
    "examples/t_factory",
    "Small introduction to responses, rewards, and training",
    "Start with the README's one-task response/reward/completion example and the native t_word_density grader. Read training.md as well. ingest.py uploads and diagnoses tasks; train.py starts baseline evaluation alongside training and later evaluates a checkpoint, so it is not an eval-only command. Inspect its defaults before launch.",
  ),
  "harvey-lab": CookbookExample(
    "Harvey LAB",
    "examples/harvey_labs",
    "Legal research with external judges and nested Podman",
    "Check nested Podman support and the large pinned source image. Configure organization secrets for the selected native judges; never put their values in prompts, images, or project files. Preserve the source agent/tools and criteria_fraction reward. Inspect ingest.py's full-dataset upload, run a diagnostic, and follow the README's baseline/training/checkpoint snippets.",
  ),
  "tau3-banking": CookbookExample(
    "Tau 3 Banking",
    "examples/tau3_banking",
    "Multi-turn banking with an external user simulator",
    "Check the organization secret required by the selected simulator/judge provider. Preserve the upstream simulator, retrieval, task bytes, evaluator, and cookbook split. Inspect ingest.py, then diagnose with compatible multi-turn limits and sampling settings. The example has no separate training script; use the SDK training guide and supported run options.",
  ),
  "swe-bench-pro": CookbookExample(
    "SWE-Bench Pro",
    "examples/swe_bench_pro",
    "Code repair with large images and long-running tasks",
    "Check nested container support and budget for large task-image pulls and long attempts. Inspect ingest.py --help and begin with one train and one test task. Preserve the offline actor, hidden-test boundary, and fresh-container verifier. The train.py workflow includes baseline and checkpoint evaluations; review all settings before running it. Cookbook-split results are not leaderboard results.",
  ),
  "terminal-bench-4": CookbookExample(
    "Terminal-Bench 4.0",
    "examples/terminal_bench_4",
    "Evaluation only: Harbor environments and verifiers",
    "Check Python 3.12+, nested Docker, and supported CPU tasks. Inspect ingest.py and start with its single-task smoke path, including the diagnostic it launches. Preserve Harbor's environment and verifier and exclude solution/cheat files. A shortened agent timeout changes the evaluation budget, so do not call its score a leaderboard result.",
    can_train=False,
  ),
}
