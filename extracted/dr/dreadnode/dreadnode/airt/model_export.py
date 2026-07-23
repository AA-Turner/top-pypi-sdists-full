"""Export a stolen surrogate model to the Dreadnode Hub (Models registry).

After a model-extraction attack recovers a surrogate, this serializes it and
pushes it to the org's Models registry via ``dn.push_model`` (OCI). The finding
then references the artifact, so an operator can download and inspect the actual
extracted model, not just read fidelity numbers.

Everything here is best-effort and import-guarded: if serialization or the push
fails (no registry, no credentials, offline), it returns ``None`` and the attack
result is unaffected.
"""

import typing as t

from loguru import logger

if t.TYPE_CHECKING:
    from pathlib import Path

    from dreadnode.airt.extraction import _Surrogate


def _slug(text: str) -> str:
    keep = [c if c.isalnum() else "-" for c in text.lower()]
    out = "".join(keep).strip("-")
    while "--" in out:
        out = out.replace("--", "-")
    return out or "model"


def _serialize(surrogate: "_Surrogate", target_dir: "Path") -> tuple[str, str] | None:
    """Write the surrogate to ``target_dir``; return (filename, framework)."""
    kind = surrogate.kind
    try:
        if kind in ("classifier", "soft"):
            import joblib  # sklearn ships joblib

            joblib.dump(surrogate.estimator, target_dir / "surrogate.joblib")
            return "surrogate.joblib", "sklearn"
        if kind == "linear":
            import numpy as np

            np.savez(
                target_dir / "surrogate.npz", weights=surrogate.weights, classes=surrogate.classes
            )
            return "surrogate.npz", "numpy"
        if kind in ("torch", "art"):
            import torch

            # ART's PyTorchClassifier keeps the nn.Module on `.model`.
            model = getattr(surrogate.estimator, "model", surrogate.estimator)
            torch.save(model, target_dir / "surrogate.pt")
            return "surrogate.pt", "pytorch"
    except Exception as e:  # pragma: no cover - defensive
        logger.warning("Surrogate serialization failed ({}): {}", kind, e)
        return None
    return None


def export_surrogate_to_hub(
    surrogate: "_Surrogate",
    *,
    strategy: str,
    target_model: str,
    fidelity: float,
    query_count: int,
    num_classes: int,
) -> dict[str, t.Any] | None:
    """Serialize + push the stolen surrogate to the Hub Models registry.

    Returns a small dict ``{name, version, framework, fidelity}`` recorded on the
    finding, or ``None`` if export is unavailable / fails.
    """
    import tempfile
    from pathlib import Path

    import yaml

    name = f"extracted-{_slug(target_model)}-{strategy}"
    version = "0.1.0"
    try:
        import dreadnode as dn

        with tempfile.TemporaryDirectory() as tmp_str:
            tmp = Path(tmp_str)
            ser = _serialize(surrogate, tmp)
            if ser is None:
                return None
            filename, framework = ser
            model_yaml = {
                "name": name,
                "version": version,
                "summary": (
                    f"Surrogate model extracted from '{target_model}' via {strategy} "
                    f"black-box queries ({round(fidelity * 100)}% fidelity)."
                ),
                "framework": framework,
                "task": "classification",
                "architecture": surrogate.name,
                "tags": ["extracted-model", "airt", "model-extraction", strategy],
                "files": [filename],
                "metrics": {
                    "fidelity": round(float(fidelity), 4),
                    "query_count": int(query_count),
                    "num_classes": int(num_classes),
                    "strategy": strategy,
                },
            }
            with (tmp / "model.yaml").open("w") as fh:
                yaml.safe_dump(model_yaml, fh)

            # Keep the surrogate private by default: an extracted model is
            # sensitive (it is a stolen copy of a victim), so it must not be
            # world-readable until the operator explicitly publishes it.
            result = dn.push_model(str(tmp), publish=False)
    except Exception as e:  # pragma: no cover - best effort
        logger.warning("Hub model export failed for {}: {}", strategy, e)
        return None

    if not getattr(result, "success", False):
        logger.info("Hub model export not uploaded (local-only mode) for {}", strategy)
        return None
    logger.info("Exported surrogate to Hub: {} v{}", result.package_name, result.package_version)
    return {
        "name": result.package_name,
        "version": result.package_version,
        "framework": framework,
        "fidelity": round(float(fidelity), 4),
    }
