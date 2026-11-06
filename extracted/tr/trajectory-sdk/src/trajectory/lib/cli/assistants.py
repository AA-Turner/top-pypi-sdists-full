from __future__ import annotations

import os
import shlex
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

from trajectory.lib.auth.credentials import CredentialStore
from trajectory.lib.cli.benchmark_source import BenchmarkSource
from trajectory.lib.cli.cookbook_prompt import EXAMPLES
from trajectory.lib.cli.guides import GuideLinks

ASSISTANTS = {
  "claude": ("Claude Code", "https://code.claude.com/docs/en/setup"),
  "codex": ("Codex", "https://developers.openai.com/codex/cli/"),
  "gemini": ("Gemini CLI", "https://geminicli.com/docs/get-started/installation/"),
}
CHOICES = (*ASSISTANTS, "copy", "manual")


def assistant_choices() -> list[tuple[str, str]]:
  installed = []
  missing = []
  for executable, (label, _) in ASSISTANTS.items():
    if shutil.which(executable):
      installed.append((label, executable))
    else:
      missing.append((label + " (not installed)", executable))
  return [*installed, *missing, ("Copy setup prompt", "copy"), ("Continue manually", "manual")]


def copy_prompt(prompt: str) -> bool:
  command = None
  if sys.platform == "darwin":
    command = ["pbcopy"]
  elif sys.platform == "win32":
    command = ["clip.exe"]
  elif os.environ.get("WAYLAND_DISPLAY") and shutil.which("wl-copy"):
    command = ["wl-copy"]
  elif os.environ.get("DISPLAY") and shutil.which("xclip"):
    command = ["xclip", "-selection", "clipboard"]
  if command is None:
    return False
  try:
    return (
      subprocess.run(
        command,
        input=prompt,
        text=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        timeout=5,
        check=False,
      ).returncode
      == 0
    )
  except (OSError, subprocess.TimeoutExpired):
    return False


def handoff(
  assistant: str,
  directory: Path,
  template: str,
  skill: str,
  profile: str | None,
  base_url: str | None,
  interactive: bool,
  cookbook: str | None = None,
  repo: str | None = None,
) -> dict[str, Any]:
  credential = CredentialStore.resolve(base_url=base_url, profile=profile)
  origin = CredentialStore.validate_login_url(credential.base_url)
  command = [sys.executable, "-m", "trajectory.lib.cli.main", "--base-url", origin]
  if credential.profile:
    command.extend(["--profile", credential.profile])
  prefix = subprocess.list2cmdline(command) if os.name == "nt" else shlex.join(command)
  tasks = {
    "benchmark": "Inspect this repository's benchmark, task loader, harness, tools, and native grader. Adapt it for Trajectory while preserving its behavior and scores.",
    "connect": "Inspect this repository's existing agent and integrate Trajectory capture where supported. Check the production-traces guide and account availability before assuming private-beta capture is enabled.",
    "example": "Inspect the generated trajectory-example project and help the user run its first small benchmark evaluation.",
  }
  task = EXAMPLES[cookbook].prompt() if cookbook else tasks[template]
  if repo is not None:
    task = BenchmarkSource.parse(repo).prompt()
  guides = "\n".join(
    f"{guide['title']}: {guide['url']}"
    for guide in GuideLinks.for_setup(template, EXAMPLES[cookbook].can_train if cookbook else True)
  )
  scope = (
    "Follow the cookbook sequence above. Honor approval already given for the agreed remote workflow; ask again only if its scope or budget changes."
    if cookbook
    else "For benchmark setup, guide me through ingestion, a small diagnostic, and my first eval; confirm the remote workflow with me once before submission, honoring approval already given for that scope and budget. Do not start training or deployment as part of setup. For agent capture, verify one captured trace rather than inventing a benchmark."
  )
  prompt = f"""Help me finish Trajectory onboarding in {directory}.

{task}
Read trajectory.toml and existing repository instructions first. Use the bundled Trajectory skill below.
Inspect the code before asking questions; ask only for missing decisions. Reuse existing project files.
Validate representative samples locally. {scope}
Report what was actually verified and the next command to run. Link the relevant guide when explaining each stage:
{guides}

Use this installed CLI for every Trajectory command (even if tj is not on PATH):
{prefix}
Append commands such as whoami --json, schema --json, or docs --topic onboarding --json.
The API origin is {origin}; the selected profile is {credential.profile or "the environment/default credentials"}.
Use the existing saved credentials through the CLI/SDK. Never print credentials or put them in generated code or prompts. If authentication is missing, ask me to run tj login; do not wait for interactive login in an agent shell command.

Bundled Trajectory integration skill:
{skill}
"""
  result: dict[str, Any] = {"name": assistant, "prompt": prompt}
  if assistant == "copy":
    result["status"] = "copied" if interactive and copy_prompt(prompt) else "prompt_ready"
    return result
  executable = shutil.which(assistant)
  if executable is None:
    result.update(status="not_installed", install_url=ASSISTANTS[assistant][1], exit_code=127)
    return result
  args = [executable]
  if assistant == "gemini":
    args.append("--prompt-interactive")
  args.append(prompt)
  if sys.platform == "darwin" and assistant == "claude":
    # Bun can reject inherited terminal descriptors with kqueue EINVAL on macOS.
    args = ["/usr/bin/script", "-q", "/dev/null", *args]
  environment = os.environ.copy()
  environment["TRAJECTORY_BASE_URL"] = origin
  if credential.profile:
    environment["TRAJECTORY_PROFILE"] = credential.profile
  environment["PATH"] = str(Path(sys.executable).parent) + os.pathsep + environment.get("PATH", "")
  try:
    completed = subprocess.run(args, cwd=directory, env=environment, check=False)
  except OSError:
    result.update(status="launch_failed", exit_code=1)
    return result
  result.update(
    status="finished" if completed.returncode == 0 else "failed",
    exit_code=completed.returncode if completed.returncode >= 0 else 128 - completed.returncode,
  )
  return result
