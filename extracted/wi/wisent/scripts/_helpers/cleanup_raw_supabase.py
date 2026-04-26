"""Verify raw activations on HF combo-by-combo and delete from Supabase."""
import os
import re
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path

import psycopg2
from huggingface_hub import HfApi

# Config
hf_repo_id = "wisent-ai/activations"
hf_repo_type = "dataset"
hf_token = os.environ.get("HF_TOKEN") or "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"

db_host = "db.rbqjqnouluslojmmnuqi.supabase.co"
db_port = 5432
db_name = "postgres"
db_user = "cli_login_postgres"


def model_to_safe_name(model_id: str) -> str:
    return model_id.replace("/", "__")


def get_fresh_password():
    result = subprocess.run(
        ["supabase", "db", "dump", "--data-only", "--linked", "--dry-run"],
        capture_output=True, text=True,
    )
    match = re.search(r'PGPASSWORD="([^"]+)"', result.stdout)
    if not match:
        raise RuntimeError(f"Could not extract password:\n{result.stdout[:500]}")
    return match.group(1)


def get_db_connection():
    """Get DB connection using host and password from supabase CLI."""
    result = subprocess.run(
        ["supabase", "db", "dump", "--data-only", "--linked", "--dry-run"],
        capture_output=True, text=True,
    )
    host_match = re.search(r'PGHOST="([^"]+)"', result.stdout)
    pass_match = re.search(r'PGPASSWORD="([^"]+)"', result.stdout)
    port_match = re.search(r'PGPORT="([^"]+)"', result.stdout)
    user_match = re.search(r'PGUSER="([^"]+)"', result.stdout)
    if not pass_match or not host_match:
        raise RuntimeError(f"Could not extract credentials:\n{result.stdout[:500]}")

    conn = psycopg2.connect(
        host=host_match.group(1),
        port=int(port_match.group(1)) if port_match else db_port,
        dbname=db_name,
        user=user_match.group(1) if user_match else db_user,
        password=pass_match.group(1),
        sslmode="require",
    )
    cur = conn.cursor()
    cur.execute("SET ROLE postgres")
    cur.execute("SET statement_timeout = 0")
    conn.commit()
    return conn


def discover_combos(conn):
    """Find all (model, benchmark, prompt_format) combos in RawActivation."""
    cur = conn.cursor()
    cur.execute("""
        SELECT DISTINCT r."modelId", m."huggingFaceId", r."contrastivePairSetId",
               c.name, r."promptFormat"
        FROM public."RawActivation" r
        JOIN public."Model" m ON m.id = r."modelId"
        JOIN public."ContrastivePairSet" c ON c.id = r."contrastivePairSetId"
        ORDER BY m."huggingFaceId", c.name, r."promptFormat"
    """)
    combos = []
    for row in cur.fetchall():
        combos.append({
            "model_id": row[0],
            "model_name": row[1],
            "set_id": row[2],
            "task_name": row[3],
            "prompt_format": row[4],
        })
    cur.close()
    return combos


def get_db_pair_ids(conn, combo):
    """Get all (layer, pair_id, isPositive) tuples from Supabase for a combo."""
    cur = conn.cursor()
    cur.execute(
        """SELECT layer, "contrastivePairId", "isPositive"
           FROM public."RawActivation"
           WHERE "modelId" = %s AND "contrastivePairSetId" = %s
             AND "promptFormat" = %s""",
        (combo["model_id"], combo["set_id"], combo["prompt_format"]),
    )
    layer_pairs = defaultdict(set)
    for layer, pid, is_pos in cur.fetchall():
        layer_pairs[layer].add((pid, is_pos))
    cur.close()
    return layer_pairs


def get_hf_layers(api, combo):
    """Get set of layers present on HF for a combo (lightweight check)."""
    safe = model_to_safe_name(combo["model_name"])
    prefix = f"raw_activations/{safe}/{combo['task_name']}/{combo['prompt_format']}"

    entries = None
    for attempt in range(5):
        try:
            entries = list(api.list_repo_tree(
                repo_id=hf_repo_id, repo_type=hf_repo_type,
                path_in_repo=prefix, recursive=True,
            ))
            break
        except Exception as e:
            err = str(e)
            if any(code in err for code in ["500", "502", "503", "504", "429"]):
                wait = 60 * (attempt + 1)
                print(f"    HF API retry {attempt+1}/5 after {wait}s")
                subprocess.run(["sleep", str(wait)])
            else:
                print(f"  No HF data found: {e}")
                return None
    if entries is None:
        print(f"  HF API failed after retries")
        return None

    hf_layers = set()
    layer_re = re.compile(r"layer_(\d+)_chunk_(\d+)\.safetensors$")
    for e in entries:
        path = getattr(e, "path", "")
        m = layer_re.search(path)
        if m:
            hf_layers.add(int(m.group(1)))

    return hf_layers


def verify_combo(db_pairs, hf_layers):
    """Check that all DB layers are present on HF."""
    if hf_layers is None:
        return False, "no HF data"

    missing = []
    for layer in db_pairs:
        if layer not in hf_layers:
            missing.append(f"layer {layer}: not on HF")

    return (len(missing) == 0), missing


def delete_combo_from_db(conn, combo):
    """Delete all rows for a combo, one layer at a time, with reconnect on failure."""
    cur = conn.cursor()
    cur.execute(
        """SELECT DISTINCT layer FROM public."RawActivation"
           WHERE "modelId" = %s AND "contrastivePairSetId" = %s
             AND "promptFormat" = %s
           ORDER BY layer""",
        (combo["model_id"], combo["set_id"], combo["prompt_format"]),
    )
    layers = [row[0] for row in cur.fetchall()]
    cur.close()

    total = 0
    for layer in layers:
        for attempt in range(3):
            try:
                cur = conn.cursor()
                cur.execute(
                    """DELETE FROM public."RawActivation"
                       WHERE "modelId" = %s AND "contrastivePairSetId" = %s
                         AND "promptFormat" = %s AND layer = %s""",
                    (combo["model_id"], combo["set_id"], combo["prompt_format"], layer),
                )
                deleted = cur.rowcount
                conn.commit()
                cur.close()
                total += deleted
                print(f"      layer {layer}: deleted {deleted}", flush=True)
                break
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                print(f"      layer {layer} attempt {attempt+1}: {e}", flush=True)
                try:
                    conn.close()
                except Exception:
                    pass
                conn = get_db_connection()
                if attempt == 2:
                    raise
    return total, conn


def main():
    conn = get_db_connection()
    api = HfApi(token=hf_token)

    combos = discover_combos(conn)
    print(f"Found {len(combos)} combos in RawActivation\n")

    total_deleted = 0
    failed = []

    for i, combo in enumerate(combos):
        label = f"{combo['model_name']} / {combo['task_name']} / {combo['prompt_format']}"
        print(f"\n[{i+1}/{len(combos)}] {label}")

        print(f"  Fetching DB pair_ids...", flush=True)
        db_pairs = get_db_pair_ids(conn, combo)
        db_total = sum(len(s) for s in db_pairs.values())
        print(f"    DB: {len(db_pairs)} layers, {db_total} (pair, side) tuples")

        print(f"  Checking HF layers...", flush=True)
        hf_layers = get_hf_layers(api, combo)
        if hf_layers is None:
            print(f"    HF: NO DATA — skipping")
            failed.append((label, "no HF data"))
            continue
        print(f"    HF: {len(hf_layers)} layers present")

        ok, missing = verify_combo(db_pairs, hf_layers)
        if not ok:
            print(f"    VERIFY FAILED: {missing[:3]}")
            failed.append((label, missing))
            continue

        print(f"    Verified OK")
        print(f"  Deleting from Supabase...", flush=True)
        deleted, conn = delete_combo_from_db(conn, combo)
        print(f"    Deleted {deleted} rows")
        total_deleted += deleted

    conn.close()

    print(f"\n{'='*60}")
    print(f"Total deleted: {total_deleted} rows")
    if failed:
        print(f"Failed combos: {len(failed)}")
        for label, reason in failed:
            print(f"  - {label}: {reason}")
    else:
        print("All combos verified and cleaned!")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
