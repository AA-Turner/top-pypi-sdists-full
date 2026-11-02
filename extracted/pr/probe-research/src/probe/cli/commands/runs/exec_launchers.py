"""recognise a job launcher probe exec wraps (sbatch, srun, kubectl, ...) and the line that forwards the run to it."""

from __future__ import annotations
import os


#: Launchers that SUBMIT and return, keyed by (binary, subcommand). The
#: subcommand is load-bearing: `modal run` BLOCKS until the job finishes while
#: `modal deploy` returns as soon as the app is published, and `ray job submit`
#: returns while a bare `ray ...` may not. Keying on the binary alone sent
#: `modal run` -- the single most common real invocation -- down the hand-off
#: path, where its real exit code was thrown away.
#:
#: `None` as the subcommand means "any", for binaries that always submit.
_SUBMIT_LAUNCHERS: dict[tuple[str, str | None], str] = {
    ("sbatch", None): "sbatch --export=ALL,PROBE_RUN_ID={run_id},PROBE_RUN_EPOCH={epoch} ...",
    (
        "modal",
        "deploy",
    ): 'modal: secrets=[modal.Secret.from_dict({{"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}), modal.Secret.from_name("<the job token\'s secret>")]',
    (
        "ray",
        "submit",
    ): 'ray: runtime_env={{"env_vars": {{"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}}}',
    (
        "ray",
        "job",
    ): 'ray: runtime_env={{"env_vars": {{"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}}}',
    ("kubectl", "apply"): "kubectl: env: PROBE_RUN_ID={run_id}, PROBE_RUN_EPOCH={epoch}",
    ("kubectl", "create"): "kubectl: env: PROBE_RUN_ID={run_id}, PROBE_RUN_EPOCH={epoch}",
}

#: `--launcher NAME` override, for a wrapper this cannot see through.
_LAUNCHER_ALIASES: dict[str, tuple[str, str | None]] = {
    "sbatch": ("sbatch", None),
    "slurm": ("sbatch", None),
    "modal": ("modal", "deploy"),
    "ray": ("ray", "job"),
    "kubectl": ("kubectl", "apply"),
}


def _launcher_name(argv: list[str]) -> str:
    """The launcher `argv` actually invokes, unwrapping the usual prefixes.

    Matching argv[0] alone misses exactly the forms people write: `python -m
    modal run`, `uv run modal run`, `uvx modal run`. The hint that depends on
    this exists FOR those cases, so the detection has to see through them.
    """
    i = 0
    while i < len(argv):
        base = os.path.basename(argv[i]).lower()
        if base in {"uv", "uvx", "poetry", "pdm", "hatch"} and i + 1 < len(argv):
            i += 1
            if os.path.basename(argv[i]).lower() in {"run", "tool"}:
                i += 1
            continue
        if base in {"python", "python3"} and i + 2 < len(argv) and argv[i + 1] == "-m":
            i += 2
            continue
        return base
    return os.path.basename(argv[0]).lower() if argv else ""


def _launcher_key(argv: list[str]) -> tuple[str, str | None]:
    """(binary, first subcommand) after unwrapping, both lowercased."""
    name = _launcher_name(argv)
    rest = [a for a in argv if os.path.basename(a).lower() == name]
    idx = argv.index(rest[0]) if rest else 0
    sub = None
    for token in argv[idx + 1 :]:
        if not token.startswith("-"):
            sub = os.path.basename(token).lower()
            break
    return name, sub


def _submit_template(argv: list[str], table: dict | None = None) -> str | None:
    table = _SUBMIT_LAUNCHERS if table is None else table
    key = _launcher_key(argv)
    return table.get(key) or table.get((key[0], None))


#: `_SUBMIT_LAUNCHERS` once a per-run token was minted for the job. The launcher
#: runs with it as PROBE_TOKEN beside the id and epoch, so a launcher that reads
#: its own environment forwards all three by name (Modal reads it only locally:
#: `from_local_environ`). Ray's driver runs on the head node, where that
#: environment is not, so its hint names the values.
_SUBMIT_LAUNCHERS_WITH_TOKEN: dict[tuple[str, str | None], str] = {
    ("sbatch", None): "sbatch --export=ALL,PROBE_TOKEN,PROBE_RUN_ID={run_id},PROBE_RUN_EPOCH={epoch} ...",
    ("modal", "deploy"): (
        'modal: secrets=[modal.Secret.from_local_environ(["PROBE_TOKEN", "PROBE_RUN_ID", "PROBE_RUN_EPOCH"])]'
    ),
    ("ray", "submit"): (
        'ray: runtime_env={{"env_vars": {{"PROBE_TOKEN": "<the PROBE_TOKEN above>", '
        '"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}}}'
    ),
    ("ray", "job"): (
        'ray: runtime_env={{"env_vars": {{"PROBE_TOKEN": "<the PROBE_TOKEN above>", '
        '"PROBE_RUN_ID": "{run_id}", "PROBE_RUN_EPOCH": "{epoch}"}}}}'
    ),
    ("kubectl", "apply"): "kubectl: env: PROBE_TOKEN (above), PROBE_RUN_ID={run_id}, PROBE_RUN_EPOCH={epoch}",
    ("kubectl", "create"): "kubectl: env: PROBE_TOKEN (above), PROBE_RUN_ID={run_id}, PROBE_RUN_EPOCH={epoch}",
}


def _forwarding_hint(
    argv: list[str], run_id: str, epoch: int, *, token_minted: bool = False
) -> str | None:
    """The line that makes a remote job reachable, or None.

    `PROBE_RUN_ID` does not cross a machine boundary on its own: Modal does not
    forward local env, Ray workers do not inherit the submitter's, Slurm needs
    --export. Printing the exact incantation is cheaper than the researcher
    discovering it from an empty run three hours later. Advisory: never a gate.
    """
    tmpl = _submit_template(argv, _SUBMIT_LAUNCHERS_WITH_TOKEN if token_minted else None)
    return tmpl.format(run_id=run_id, epoch=epoch) if tmpl else None


def _is_submit_launcher(argv: list[str]) -> bool:
    return _submit_template(argv) is not None
