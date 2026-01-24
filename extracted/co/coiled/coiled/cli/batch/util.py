from __future__ import annotations

import json

import yaml


def load_sidecar_spec(spec_path: str | None):
    scheduler_sidecars = []
    if spec_path:
        with open(spec_path) as f:
            if spec_path.endswith((".yaml", ".yml")):
                sidecar_spec = yaml.safe_load(f)
            elif spec_path.endswith(".json"):
                sidecar_spec = json.load(f)
            else:
                raise ValueError(f"Unknown format for {spec_path}, json or yaml expected.")

            # support either list-like or dict-like
            if isinstance(sidecar_spec, list):
                scheduler_sidecars = sidecar_spec
            if isinstance(sidecar_spec, dict):
                scheduler_sidecars = [{"name": key, **val} for key, val in sidecar_spec.items()]

            for sidecar in scheduler_sidecars:
                # allow `image` as the key, to match docker compose spec
                sidecar["container"] = sidecar.get("container") or sidecar.get("image")
    return scheduler_sidecars
