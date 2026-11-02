"""Parse one staged bundle with DagBag; run by `databaas dag validate`.

``python -P -m databaas_utils.airflow.dagcheck BUNDLE_DIR REPORT_JSON``

Runs in its own process so the DAG files get a clean ``sys.path`` and module
cache, and so `databaas_utils.dags` never imports Airflow. The bundle directory
is appended to ``sys.path``, as `DataBaasS3DagBundle` does in the cluster.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path


def main(argv: list[str]) -> int:
    """Write the DAGs and import errors found in ``argv[0]`` to ``argv[1]``."""
    bundle, report = Path(argv[0]), Path(argv[1])
    try:
        from airflow.models.dagbag import DagBag
    except Exception as exc:  # a broken install fails in many ways, not only ImportError
        fatal = f"cannot import Airflow: {type(exc).__name__}: {exc}"
        report.write_text(json.dumps({"fatal": fatal}))
        return 0
    sys.path.append(str(bundle))
    bag = DagBag(dag_folder=str(bundle), include_examples=False, safe_mode=False)
    report.write_text(
        json.dumps(
            {
                "import_errors": {
                    str(path): str(error) for path, error in bag.import_errors.items()
                },
                "dags": [
                    {"dag_id": dag.dag_id, "fileloc": str(dag.fileloc)}
                    for dag in bag.dags.values()
                ],
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
