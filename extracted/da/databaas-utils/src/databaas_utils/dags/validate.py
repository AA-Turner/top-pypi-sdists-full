"""Parse a target's DAGs the way its Airflow will, before deploying them.

The tree is staged exactly as `deploy` stages it, then parsed with DagBag in a
subprocess running this interpreter, which therefore needs Airflow and the
DAGs' own dependencies installed.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Any

from databaas_utils.dags.config import DagsConfig
from databaas_utils.dags.deploy import ResolvedTarget, resolve_target, stage
from databaas_utils.dags.gitinfo import GitInfo, collect
from databaas_utils.errors import ConfigurationError, LakehouseError

_WORKER = "databaas_utils.airflow.dagcheck"


class DagValidationError(LakehouseError):
    """The DAG check itself could not run."""


@dataclass(frozen=True)
class Problem:
    """One reason the target's DAGs would not deploy cleanly.

    Attributes:
        file: The file, relative to `databaas.yml`; empty if not about one file.
        message: What is wrong.
    """

    file: str
    message: str


@dataclass(frozen=True)
class ValidationResult:
    """The DAG ids found and the problems with them."""

    resolved: ResolvedTarget
    dag_ids: tuple[str, ...]
    problems: tuple[Problem, ...]
    renamed: dict[str, str] = field(default_factory=dict)
    output: str = ""

    @property
    def ok(self) -> bool:
        """No problems."""
        return not self.problems


def validate(
    config: DagsConfig,
    target_name: str | None,
    *,
    dev_key: str | None = None,
    git: GitInfo | None = None,
) -> ValidationResult:
    """Stage the target's tree and parse every DAG file in it.

    Problems are import errors (Airflow's own checks, such as duplicate or
    over-long dag ids, among them), no DAGs at all, and, for a development
    target, dag ids without the ``dev_<dev_key>_`` prefix, which would replace
    the production DAG of the same id.

    Raises:
        ConfigurationError: On a bad target, or when Airflow is not installed.
        DagValidationError: If the check stopped without a report.
    """
    provenance = git or collect(config.root)
    resolved = resolve_target(config, target_name, dev_key=dev_key, git=provenance)
    with tempfile.TemporaryDirectory(prefix="databaas-validate-") as tmp:
        work = Path(tmp).resolve()
        bundle = work / "bundle"
        bundle.mkdir()
        renamed = stage(config, resolved, bundle, git=provenance)
        report_path = work / "report.json"
        env = dict(os.environ)
        env.setdefault("AIRFLOW_HOME", str(work / "airflow-home"))
        env["AIRFLOW__CORE__LOAD_EXAMPLES"] = "False"
        completed = subprocess.run(
            [sys.executable, "-P", "-m", _WORKER, str(bundle), str(report_path)],
            cwd=work,
            env=env,
            capture_output=True,
            text=True,
            check=False,
        )
        output = completed.stdout + completed.stderr
        if not report_path.is_file():
            tail = "\n".join(output.strip().splitlines()[-20:])
            raise DagValidationError(
                f"the DAG check exited with {completed.returncode} before reporting:"
                f"\n{tail}"
            )
        report = json.loads(report_path.read_text())
        if "fatal" in report:
            raise ConfigurationError(
                f"validating DAGs needs Airflow and the DAGs' dependencies in this "
                f"Python ({sys.executable}): {report['fatal']}. Install Airflow with "
                "its constraints file, e.g. -c https://raw.githubusercontent.com/"
                "apache/airflow/constraints-3.1.8/constraints-3.12.txt"
            )
        source = config.source.relative_to(config.root).as_posix()
        problems, dag_ids = _problems(report, resolved, bundle, source, renamed)
    return ValidationResult(resolved, dag_ids, problems, renamed, output)


def _problems(
    report: dict[str, Any],
    resolved: ResolvedTarget,
    bundle: Path,
    source: str,
    renamed: dict[str, str],
) -> tuple[tuple[Problem, ...], tuple[str, ...]]:
    original = {new: old for old, new in renamed.items()}

    def where(path: str) -> str:
        try:
            parts = list(Path(path).relative_to(bundle).parts)
        except ValueError:
            return path
        stem, dot, suffix = parts[0].partition(".")
        parts[0] = original.get(stem, stem) + dot + suffix
        return str(PurePosixPath(source, *parts))

    def unstaged(text: str) -> str:
        return text.replace(str(bundle), source)

    problems = [
        Problem(where(path), unstaged(error))
        for path, error in sorted(report["import_errors"].items())
    ]
    dags = sorted(report["dags"], key=lambda dag: dag["dag_id"])
    if not dags and not problems:
        problems.append(Problem("", f"no DAGs found in {source}/"))
    prefix = f"dev_{resolved.dev_key}_"
    for dag in dags:
        dag_id, file = dag["dag_id"], where(dag["fileloc"])
        if resolved.dev_key and not dag_id.startswith(prefix):
            problems.append(
                Problem(
                    file,
                    f"dag id {dag_id!r} does not start with {prefix!r}, so this dev "
                    "deploy would replace the production DAG of that id; build it "
                    "with target.dag_id(...)",
                )
            )
    return tuple(problems), tuple(dag["dag_id"] for dag in dags)
