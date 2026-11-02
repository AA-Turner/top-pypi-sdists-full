"""Deprecated alias for `databaas_utils.airflow.target`.

`from databaas_target import target` is a de-facto platform ABI written into DAG
files across every pipeline repo, so the name ships from this wheel to keep them
working unchanged. Pure stdlib — importing it costs nothing and pulls in no
Airflow.

Removed in 2.0; import from `databaas_utils.airflow.target` instead.
"""

from __future__ import annotations

from databaas_utils.airflow.target import (
    DeploymentTarget,
    _CallerScopedTarget,
    target_for,
)

# A fresh proxy, not the one from the target module: __getattr__ uses
# sys._getframe(1), so the object must be reached directly from the DAG file.
target = _CallerScopedTarget()

__all__ = ["DeploymentTarget", "target", "target_for"]
