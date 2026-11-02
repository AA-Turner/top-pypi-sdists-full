"""The rules every coding agent working in a Labqoat project is reminded of, and whether its skills are current."""

from pathlib import Path

from labqoat.cli.skills.skill_bundle import SkillBundle


class AgentRules:
    """A short card injected at session start, after compaction and into every subagent."""

    card = """Labqoat rules for this project (from `lab agent brief`):
1. Before writing or launching a run, read the labqoat-runs skill; give subagents this card and that skill.
2. One question is one child run under one parent (`context.runs`, `context.group`). Never launch many root
   runs or drive runs from local scripts, loops or text files of run ids.
3. Launch with `--detach`, then block once: `lab run wait RUN... [--any] --timeout 2h` prints each run as it
   ends. Never poll with sleep, until, while or seq loops or scheduled (cron) checks; never re-read whole logs.
4. Read a run with `lab run status RUN`, metrics with `lab run watch RUN --metrics 'val/*'`, logs with
   `lab run logs RUN -n 50` or `--grep TEXT`, not `--all`.
5. Log metrics (`context.training().step(step, loss=..., reward=...)`), return typed results and Artifacts.
   Never print JSON lines to parse back from logs.
6. A run over 30 minutes saves checkpoints and takes a `Checkpoint[...] | None` resume input.
7. `.py` files and small files (1 MiB each, 16 MiB total) ship with a run; the launch names the rest. Big
   data goes on a volume, in an asset or via `Image.add_local_dir`.
8. Capacity comes from `lab run placement RUN`, `lab compute quotas` (free vCPUs per region and group) and
   `lab compute offerings`; never use aws, gcloud or kubectl.
9. In a strict project `lab run` submits nothing until `ruff format`, `ruff check` and `ty check` pass; fix
   the code, do not loosen the settings.
10. Use the built-in, not your own: compare runs with `lab run compare --app APP --metrics 'val/*'`, wait
   with `lab run wait`, chain stages through a parent run and typed results, repair with `lab run recover`.
   Never write report, watcher, driver or relaunch scripts around `lab`.

Never, unless the user asks for it:
- switch GPU model, count, region or spot, or use `gpu="any"`, to be placed sooner: waiting hours for a GPU
  is normal; `lab run placement RUN` says why it waits.
- give GPU work a short `queue_timeout`: left unset it waits 24 h for a GPU.
- cancel a run you did not start, or a running one to relaunch it; start the new version beside it.
- launch a run to recompute what a finished run recorded: read its result, metrics or logs.
- create a new app per variant (vary arguments and tags), or keep run ids in files (`--owner`, `--tag`).
- read the SDK's source in site-packages: use `lab ... --help` and labqoat-runs `reference/sdk.md`.
- train or tune on evaluation or benchmark data, or report a score from data the model saw.
- change budgets, quotas or project settings to get unblocked: report what blocks you."""

    @classmethod
    def brief(cls, workspace: Path) -> str:
        """The card, with a line asking for a skills update when the installed copies differ from this CLI's."""
        stale = [name for name in SkillBundle.contents() if cls.outdated(workspace, name)]
        if not stale:
            return cls.card
        return (
            f"{cls.card}\n\nThe installed Labqoat skills differ from this CLI ({', '.join(sorted(stale))}): run "
            "`lab skills install --agent claude --force` and `lab skills install --agent codex --force`."
        )

    @staticmethod
    def outdated(workspace: Path, name: str) -> bool:
        """Whether an installed copy of skill ``name`` exists and differs from the bundled one."""
        bundled = SkillBundle.contents()[name]
        copies = [workspace / root / "skills" / name / "SKILL.md" for root in (".claude", ".agents")]
        return any(path.is_file() and path.read_text(encoding="utf-8") != bundled for path in copies)
