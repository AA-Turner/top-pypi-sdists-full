"""Fix Llama-3.2-1B/truthfulqa_custom/chat layer 9: delete stale chunks, re-upload."""
import json
import os
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

import numpy as np
import psycopg2
import torch
from huggingface_hub import HfApi, CommitOperationDelete, CommitOperationAdd
from safetensors.torch import save_file

hf_repo_id = "wisent-ai/activations"
hf_repo_type = "dataset"
hf_token = os.environ.get("HF_TOKEN") or "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"

db_host = "db.rbqjqnouluslojmmnuqi.supabase.co"
db_port = 5432
db_name = "postgres"
db_user = "cli_login_postgres"

model_name = "meta-llama/Llama-3.2-1B-Instruct"
task_name = "truthfulqa_custom"
prompt_format = "chat"
target_layer = 9

prefix = "raw_activations/meta-llama__Llama-3.2-1B-Instruct/truthfulqa_custom/chat"


def get_fresh_password():
    result = subprocess.run(
        ["supabase", "db", "dump", "--data-only", "--linked", "--dry-run"],
        capture_output=True, text=True,
    )
    match = re.search(r'PGPASSWORD="([^"]+)"', result.stdout)
    if not match:
        raise RuntimeError(f"Could not get password:\n{result.stdout[:500]}")
    return match.group(1)


def get_db_connection():
    conn = psycopg2.connect(
        host=db_host, port=db_port, dbname=db_name,
        user=db_user, password=get_fresh_password(),
        sslmode="require", connect_timeout=30,
    )
    cur = conn.cursor()
    cur.execute("SET ROLE postgres")
    cur.execute("SET statement_timeout = 0")
    conn.commit()
    return conn


def commit_with_retry(api, **kwargs):
    """Create commit with retry on 429 rate limit (1h wait)."""
    for attempt in range(6):
        try:
            return api.create_commit(**kwargs)
        except Exception as e:
            err = str(e)
            if "429" in err or "Too Many Requests" in err:
                wait = 3600
                print(f"  Rate limited, waiting 1h (attempt {attempt+1}/6)...", flush=True)
                subprocess.run(["sleep", str(wait)])
            elif attempt < 5:
                wait = 60 * (attempt + 1)
                print(f"  Retry {attempt+1}/6 after {wait}s: {e}", flush=True)
                subprocess.run(["sleep", str(wait)])
            else:
                raise


def main():
    api = HfApi(token=hf_token)

    # Step 1: list existing layer_9 chunks
    print(f"Step 1: listing stale layer_9 chunks on HF...")
    entries = list(api.list_repo_tree(
        repo_id=hf_repo_id, repo_type=hf_repo_type,
        path_in_repo=prefix, recursive=False,
    ))
    layer9_paths = [
        e.path for e in entries
        if hasattr(e, "path") and "layer_9_chunk_" in e.path
    ]
    print(f"  Found {len(layer9_paths)} stale files: {[Path(p).name for p in layer9_paths]}")

    # Step 2: fetch layer 9 data from Supabase
    print(f"\nStep 2: fetching layer 9 data from Supabase...")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id FROM public."Model" WHERE "huggingFaceId" = %s', (model_name,))
    model_id = cur.fetchone()[0]
    cur.execute('SELECT id FROM public."ContrastivePairSet" WHERE name = %s', (task_name,))
    set_id = cur.fetchone()[0]
    cur.close()

    layer_cur = conn.cursor("layer9_fix")
    layer_cur.execute(
        """SELECT "contrastivePairId", "hiddenStates", "isPositive"
           FROM public."RawActivation"
           WHERE "modelId" = %s AND "contrastivePairSetId" = %s
             AND "promptFormat" = %s AND layer = %s
           ORDER BY "contrastivePairId", "isPositive" """,
        (model_id, set_id, prompt_format, target_layer),
    )

    pair_acts = defaultdict(dict)
    row_count = 0
    while True:
        rows = layer_cur.fetchmany(200)
        if not rows:
            break
        for pid, hidden_bytes, is_pos in rows:
            key = "pos" if is_pos else "neg"
            pair_acts[pid][key] = np.frombuffer(
                bytes(hidden_bytes), dtype=np.float32
            ).copy()
            row_count += 1

    layer_cur.close()
    conn.commit()
    conn.close()

    sorted_pairs = sorted(
        [(pid, a) for pid, a in pair_acts.items()
         if "pos" in a and "neg" in a]
    )
    print(f"  Got {row_count} rows -> {len(sorted_pairs)} complete pairs")

    # Step 3: build single safetensors file with per-pair tensors
    print(f"\nStep 3: building safetensors file...")
    pids = [pid for pid, _ in sorted_pairs]
    tensors = {}
    for pid, a in sorted_pairs:
        tensors[f"pos_{pid}"] = torch.from_numpy(a["pos"])
        tensors[f"neg_{pid}"] = torch.from_numpy(a["neg"])

    tmp_dir = tempfile.mkdtemp(prefix="fix_layer9_")
    try:
        out_path = Path(tmp_dir) / "layer_9_chunk_0.safetensors"
        save_file(
            tensors,
            str(out_path),
            metadata={"pair_ids": json.dumps(pids)},
        )
        size_mb = out_path.stat().st_size / 1024 / 1024
        print(f"  Built {out_path.name} ({size_mb:.1f} MB)")

        # Step 4: combined commit — delete stale + add new in single commit
        print(f"\nStep 4: combined delete+add commit to HF...")
        ops = []
        for stale_path in layer9_paths:
            ops.append(CommitOperationDelete(path_in_repo=stale_path))
        ops.append(CommitOperationAdd(
            path_in_repo=f"{prefix}/layer_9_chunk_0.safetensors",
            path_or_fileobj=str(out_path),
        ))
        commit_with_retry(
            api,
            repo_id=hf_repo_id, repo_type=hf_repo_type,
            operations=ops,
            commit_message="fix: replace stale layer_9 chunks with single complete chunk",
        )
        print(f"  Committed: -{len(layer9_paths)} stale, +1 new")
    finally:
        import shutil
        shutil.rmtree(tmp_dir, ignore_errors=True)

    print(f"\n{'='*50}")
    print(f"Done! Layer 9 fixed with {len(sorted_pairs)} pairs.")
    print(f"Now re-run cleanup_raw_supabase.py to verify and delete.")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
