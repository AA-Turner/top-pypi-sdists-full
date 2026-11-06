"""Resumable local project setup and a small managed benchmark."""

from __future__ import annotations

import importlib.metadata
import os
import shlex
import tempfile
import tomllib
from pathlib import Path
from typing import Any

import tomli_w

from trajectory import BenchmarkSpec, TaskSpec
from trajectory.lib.benchmarks import DockerfileBuild
from trajectory.lib.cli.benchmark_source import BenchmarkSource
from trajectory.lib.cli.cookbook_prompt import EXAMPLES
from trajectory.lib.cli.guides import GuideLinks


class Project:
  choices = ("benchmark", "connect", "cookbook", "example", "skip")
  harness = '''"""One managed model call, exact-answer grading, and explicit completion."""
import os
import shlex

from trajectory import Client


def main() -> None:
  with Client() as client:
    tid = client.trajectories.create().tid
    try:
      response = client.chat.completions.create(
        model="policy",
        messages=[{"role": "user", "content": os.environ["TASK_PROMPT"]}],
        max_tokens=256,
        x_trajectory_id=tid,
      )
      choice = response.choices[0]
      if choice.finish_reason == "length":
        client.trajectories.complete(tid, termination_reason="TRUNCATION")
        return
      if choice.finish_reason != "stop" or choice.message.content is None:
        raise RuntimeError("The model did not produce a completed text answer")
      grade = float(choice.message.content.strip() == os.environ["EXPECTED_ANSWER"])
      client.trajectories.log_reward(tid, name="exact_answer", value=grade)
    except Exception:
      client.trajectories.complete(tid, termination_reason="ERROR")
      raise
    client.trajectories.complete(tid, termination_reason="ENV_DONE")


if __name__ == "__main__":
  main()
'''

  def __init__(self, directory: Path) -> None:
    self.directory = directory.resolve()
    self.path = self.directory / "trajectory.toml"

  def load(self) -> dict[str, Any]:
    if not self.path.exists():
      return {}
    with self.path.open("rb") as stream:
      data = tomllib.load(stream)
    unknown = data.keys() - {
      "version",
      "template",
      "agent_id",
      "bench_id",
      "manifest",
      "cookbook",
      "repo",
    }
    if unknown:
      raise ValueError(f"Unsupported project fields: {', '.join(sorted(unknown))}")
    if data.get("version", 1) != 1:
      raise ValueError("Unsupported trajectory.toml version")
    return data

  @staticmethod
  def _create_file(path: Path, content: str) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".trajectory-")
    try:
      with os.fdopen(fd, "w", encoding="utf-8") as stream:
        stream.write(content)
      try:
        os.link(temporary, path)
      except FileExistsError:
        return False
    finally:
      Path(temporary).unlink(missing_ok=True)
    return True

  def initialize(
    self,
    template: str,
    agent_id: str | None = None,
    cookbook: str | None = None,
    repo: str | None = None,
    resume_repo: bool = True,
  ) -> dict[str, Any]:
    if template not in self.choices:
      raise ValueError(f"Choose a template: {', '.join(self.choices)}")
    if template == "skip":
      return {"template": "skip", "next_steps": ["Run tj init when you are ready."]}
    previous = self.load()
    if previous:
      if previous.get("template", template) != template:
        raise ValueError(
          "This project already uses a different template; choose another --directory"
        )
      agent_id = agent_id or previous.get("agent_id")
    if template == "cookbook":
      cookbook = cookbook or previous.get("cookbook")
      if not isinstance(cookbook, str) or cookbook not in EXAMPLES:
        raise ValueError("Choose a cookbook example with --cookbook: " + ", ".join(EXAMPLES))
      if previous.get("cookbook") and previous["cookbook"] != cookbook:
        raise ValueError(
          "This project already uses a different cookbook example; choose another --directory"
        )
    elif cookbook is not None:
      raise ValueError("--cookbook requires the cookbook template")
    if repo is None and resume_repo:
      repo = previous.get("repo")
    source = BenchmarkSource.parse(repo) if repo is not None else None
    if source:
      if template != "benchmark":
        raise ValueError("--repo requires the benchmark template")
    if previous.get("repo") and previous["repo"] != (source.value if source else None):
      raise ValueError(
        "This project already uses a different benchmark source; choose another --directory"
      )
    config: dict[str, Any] = {**previous, "version": 1, "template": template}
    if source:
      config["repo"] = source.value
    if cookbook:
      config["cookbook"] = cookbook
    if agent_id:
      config["agent_id"] = agent_id
    created = []
    if template == "example":
      config["manifest"] = "trajectory-example/manifest.json"
      manifest = BenchmarkSpec(
        name="terminal-example",
        runtime=DockerfileBuild("Dockerfile"),
        tasks=[
          TaskSpec(
            name="addition-train",
            split="train",
            run_command="python /app/harness.py",
            env_vars={
              "TASK_PROMPT": "What is 2 + 3? Reply with only the number.",
              "EXPECTED_ANSWER": "5",
            },
          ),
          TaskSpec(
            name="addition-test",
            split="test",
            run_command="python /app/harness.py",
            env_vars={
              "TASK_PROMPT": "What is 3 + 4? Reply with only the number.",
              "EXPECTED_ANSWER": "7",
            },
          ),
        ],
      )
      files = {
        "harness.py": self.harness,
        "Dockerfile": f"FROM python:3.11-slim\nWORKDIR /app\nRUN pip install --no-cache-dir trajectory-sdk=={importlib.metadata.version('trajectory-sdk')}\nCOPY harness.py /app/harness.py\n",
        ".dockerignore": "*\n!Dockerfile\n!harness.py\n",
        "manifest.json": manifest.model_dump_json(indent=2) + "\n",
      }
      for name, content in files.items():
        path = self.directory / "trajectory-example" / name
        if self._create_file(path, content):
          created.append(str(path))
    text = tomli_w.dumps(config)
    if previous and config != previous:
      fd, temporary = tempfile.mkstemp(dir=self.directory, prefix=".trajectory-")
      try:
        with os.fdopen(fd, "w", encoding="utf-8") as stream:
          stream.write(text)
        os.replace(temporary, self.path)
      finally:
        Path(temporary).unlink(missing_ok=True)
    elif self._create_file(self.path, text):
      created.append(str(self.path))
    next_steps = self._next_steps(template, agent_id, cookbook)
    result = {
      "template": template,
      "project": str(self.path),
      "created": created,
      "next_steps": next_steps,
      "submitted": False,
      "guides": GuideLinks.for_setup(template, EXAMPLES[cookbook].can_train if cookbook else True),
    }
    if cookbook:
      result.update(cookbook=cookbook, cookbook_url=EXAMPLES[cookbook].readme_url)
    if source:
      result.update(repo=source.value, repo_kind=source.kind)
      result["next_steps"] = [
        f"Use benchmark source: {source.value}",
        "Choose a coding assistant or use --assistant copy for a source-specific integration prompt.",
        "Inspect the real task loader, customer agent, tools, runtime, and native grader; reproduce one task.",
        "Prepare the benchmark manifest and eval.json, then review a managed diagnostic against the native result.",
        "After confirming the first grade, run a small held-out evaluation and retain its IDs and resume commands.",
      ]
    return result

  def _next_steps(
    self, template: str, agent_id: str | None, cookbook: str | None = None
  ) -> list[str]:
    if cookbook:
      example = EXAMPLES[cookbook]
      steps = [
        f"Read {example.name}: {example.readme_url}",
        f"Run tj init --cookbook {cookbook} --assistant copy to get an example-specific setup prompt, or choose a coding assistant.",
        "Inspect the cookbook checkout and its prerequisites, then reuse or create an agent.",
        "Follow the example's smallest diagnostic; confirm before submitting remote work and inspect the recorded grade.",
        "Upload the benchmark and evaluate a small held-out baseline with supported models and options.",
      ]
      if example.can_train:
        steps.extend(
          [
            "Run tj training options --bench-id <bench-id> --json and prepare training.json with a small, agreed budget.",
            "Validate with tj training create --config training.json --dry-run --json; after review, submit without --dry-run.",
            "Use tj training watch <training-run-id> and tj training details <training-run-id> --json; compare a checkpoint on the same held-out tasks.",
          ]
        )
      else:
        steps.append(
          "This example is evaluation-only. Choose GSM8K or T Factory in a separate directory to train."
        )
      return steps

    if template == "connect":
      return [
        "Run tj docs --topic skill and ask your coding agent to integrate the existing harness.",
        "Follow the production-traces guide if capture is enabled for your organization; verify the first captured trace.",
      ]
    if template == "benchmark":
      return [
        "Run tj docs --topic skill and ask your coding agent to adapt the task loader, harness, and native grader.",
        "Create a BenchmarkSpec JSON manifest, then tj benchmarks push --manifest PATH --agent-id ID.",
        "Run a diagnostic before starting an eval or training.",
      ]
    owner = agent_id or "<agent-id>"
    return [
      "tj agents list --json (or tj agents create --name NAME)",
      f"tj benchmarks push --manifest {shlex.quote(str(self.directory / 'trajectory-example/manifest.json'))} --agent-id {owner}",
      "tj operations watch <operation-id> --timeout 300",
      "tj benchmarks readiness <bench-id>",
      "tj benchmarks diagnose <bench-id>",
      "tj diagnostics watch <diagnostic-id> --timeout 300",
      "tj evals models --json",
      "Create eval.json with bench_id and a catalog base_model_slug; use options.val_num_tasks=1 and options.val_trajectories_per_task=1.",
      "tj evals create --config eval.json",
      "tj evals watch <eval-run-id> --timeout 300",
    ]
