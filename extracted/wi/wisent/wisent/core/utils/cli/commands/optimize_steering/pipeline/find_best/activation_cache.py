"""Upload freshly extracted activations and trial artifacts to HF."""
import json
import os
import shutil
import tempfile

import torch


def upload_extracted_activations(activations_file: str, model: str, task: str) -> None:
    """Parse activations.json and upload all layer shards as a SINGLE HF
    commit per strategy.

    Earlier this called upload_activation_shard once per layer, producing
    one HF commit per (task, strategy, layer). With 7 strategies × ~16
    layers per Llama-3.2-1B job, a single job consumed 112 commits — past
    the HF 128-commits/hour-per-repo ceiling. With ~25 cloud agents
    running concurrently the rate limit was hit on EVERY job, surfacing
    as "Upload failed for ...: 429 Client Error" in 20/20 sampled
    completions on 2026-05-06. Batching to 1 commit per strategy drops
    this to 7 commits/job, well under the cap.

    Failures are now RAISED rather than swallowed so the caller can
    propagate them as a non-zero exit code; the runner-side
    verify_command (wisent-compute 0.4.59) catches the eventual mismatch
    if the script still exits 0.
    """
    from wisent.core.reading.modules.utilities.data.sources.hf.hf_writers import (
        flush_staging_dir,
        upload_activation_shard,
    )
    with open(activations_file) as f:
        data = json.load(f)
    strategy = data.get("extraction_strategy", "")
    component = data.get("extraction_component", "residual_stream")
    layers = data.get("layers", [])
    pairs = data.get("pairs", [])
    if not pairs or not layers:
        return
    hf_strategy = (f"{strategy}/{component}"
                    if component != "residual_stream" else strategy)
    staging = tempfile.mkdtemp(prefix="wisent_act_staging_")
    try:
        any_layer_staged = False
        for layer in layers:
            layer_str = str(layer)
            pos_list, neg_list, pair_ids = [], [], []
            for idx, pair in enumerate(pairs):
                pos_act = (pair.get("positive_response", {})
                           .get("layers_activations", {}).get(layer_str))
                neg_act = (pair.get("negative_response", {})
                           .get("layers_activations", {}).get(layer_str))
                if pos_act is not None and neg_act is not None:
                    pos_list.append(torch.tensor(pos_act))
                    neg_list.append(torch.tensor(neg_act))
                    pair_ids.append(idx)
            if not pos_list:
                continue
            upload_activation_shard(
                model_name=model, benchmark=task, strategy=hf_strategy,
                layer=layer,
                pos_activations=torch.stack(pos_list),
                neg_activations=torch.stack(neg_list),
                pair_ids=pair_ids,
                staging_dir=staging,
            )
            any_layer_staged = True
        if any_layer_staged:
            flush_staging_dir(staging)
    finally:
        shutil.rmtree(staging, ignore_errors=True)


def upload_trial(
    model: str, benchmark: str, method: str, trial_idx: int, trial_dir: str,
) -> None:
    """Upload trial artifacts (responses, scores, meta) to HF."""
    try:
        from wisent.core.reading.modules.utilities.data.sources.hf.hf_config import (
            HF_REPO_ID, HF_REPO_TYPE, model_to_safe_name,
        )
        from wisent.core.reading.modules.utilities.data.sources.hf.hf_writers import (
            _get_api,
        )
        safe = model_to_safe_name(model)
        api = _get_api()
        for fname in ("trial_meta.json", "responses.json", "scores.json"):
            local = os.path.join(trial_dir, fname)
            if not os.path.exists(local):
                continue
            hf_path = f"trials/{safe}/{benchmark}/{method.lower()}/trial_{trial_idx:04d}/{fname}"
            api.upload_file(
                path_or_fileobj=local, path_in_repo=hf_path,
                repo_id=HF_REPO_ID, repo_type=HF_REPO_TYPE,
            )
        print(f"  [trial] Uploaded trial {trial_idx} to HF")
    except Exception as exc:
        print(f"  [trial] Upload failed for trial {trial_idx}: {exc}")
