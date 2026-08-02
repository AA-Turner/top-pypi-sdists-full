# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path
from typing import TYPE_CHECKING
from urllib.parse import urlparse

import geneva

DEFAULT_GCP_BUCKET_PREFIX = os.getenv(
    "GENEVA_E2E_GCP_BUCKET_PREFIX", "gs://lancedb-lancedb-dev-us-central1"
)
DEFAULT_AWS_BUCKET_PREFIX = os.getenv(
    "GENEVA_E2E_AWS_BUCKET_PREFIX", "s3://geneva-integ-test-devland-us-east-1"
)
DEFAULT_AZURE_BUCKET_PREFIX = os.getenv(
    "GENEVA_E2E_AZURE_BUCKET_PREFIX", "az://lancedbdatasets"
)


def default_bucket_path(csp: str, slug: str) -> str:
    if csp == "gcp":
        prefix = DEFAULT_GCP_BUCKET_PREFIX
    elif csp == "aws":
        prefix = DEFAULT_AWS_BUCKET_PREFIX
    elif csp == "azure":
        prefix = DEFAULT_AZURE_BUCKET_PREFIX
    else:
        raise ValueError(f"Unsupported CSP: {csp}")
    return f"{prefix.rstrip('/')}/{slug}/data"

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from dataset import write_large_image_table

if TYPE_CHECKING:
    from geneva.table import Table

DEFAULT_MANIFEST = "large-image-embedding-udfs-v1"
DEFAULT_MERGED_MANIFEST = "large-image-embedding-udfs-merged-v1"
STANDARD_DERIVED_COLUMNS = ["decoded", "preprocessed", "vit_logits"]
MERGED_DERIVED_COLUMNS = ["preprocessed", "vit_logits"]
DERIVED_COLUMNS = STANDARD_DERIVED_COLUMNS
GPU_DERIVED_COLUMNS = {"vit_logits"}
CLUSTER_NAME_PREFIX = "e2e-large-image-embedding"

MAX_TEXT_PROMPTS = 7358
PROMPT_FRAG_ROWS = 200


def default_manifest_name(use_merged_preprocess: bool) -> str:
    if use_merged_preprocess:
        return DEFAULT_MERGED_MANIFEST
    return DEFAULT_MANIFEST


def derived_columns(use_merged_preprocess: bool, skip_gpu: bool) -> list[str]:
    columns = (
        MERGED_DERIVED_COLUMNS.copy()
        if use_merged_preprocess
        else STANDARD_DERIVED_COLUMNS.copy()
    )
    if skip_gpu and columns:
        return columns[:-1]
    return columns


def upload_manifest(
    bucket: str,
    table_name: str,
    manifest_name: str,
    use_merged_preprocess: bool,
    skip_gpu: bool,
) -> None:
    env = os.environ.copy()
    env["GENEVA_TABLE_NAME"] = table_name
    cmd = [
        "uv",
        "run",
        "python",
        "upload_manifests.py",
        "--bucket",
        bucket,
        "--profile",
        "vit_image",
        "--manifest-name",
        manifest_name,
    ]
    if use_merged_preprocess:
        cmd.append("--use-merged-preprocess")
    if skip_gpu:
        cmd.append("--skip-gpu")
    subprocess.run(cmd, cwd=str(_ROOT), check=True, env=env)


def cluster_name_for_slug(slug: str) -> str:
    return f"{CLUSTER_NAME_PREFIX}-{slug}"


def resolve_dataset_path(
    dataset_path: str, default_bucket: str | None
) -> tuple[str, str]:
    normalized = dataset_path.rstrip("/")
    if normalized.startswith(("gs://", "s3://", "az://")):
        bucket_path, _, table_name = normalized.rpartition("/")
        if not bucket_path or not table_name:
            raise ValueError(
                f"Dataset path must include a table name, got: {dataset_path}"
            )
        return bucket_path, table_name
    if "/" in normalized:
        raise ValueError(
            "Dataset path without gs://, s3://, or az:// must be a table name only"
        )
    if default_bucket is None:
        raise ValueError(
            "Dataset path without bucket requires --bucket or --slug to derive a default"
        )
    return default_bucket, normalized


def checkpoint_uri(bucket_path: str, table_name: str) -> str:
    normalized_bucket = bucket_path.rstrip("/")
    if normalized_bucket.startswith(("gs://", "s3://", "az://")):
        return f"{normalized_bucket}/{table_name}.lance/_ckp"
    return str(Path(normalized_bucket) / f"{table_name}.lance" / "_ckp")


def delete_checkpoint_dir(uri: str) -> None:
    if not uri:
        return

    try:
        import pyarrow.fs as pafs

        fs, path = pafs.FileSystem.from_uri(uri)
        info = fs.get_file_info([path])[0]
        if info.type == pafs.FileType.NotFound:
            print(f"No checkpoint directory found at {uri}")
            return
        print(f"Deleting checkpoint directory {uri}")
        fs.delete_dir(path)
        return
    except Exception as exc:
        print(f"pyarrow delete_dir failed for {uri}: {exc}; falling back to CLI tools")

    scheme = urlparse(uri).scheme.lower()
    if scheme == "s3":
        subprocess.run(["aws", "s3", "rm", "--recursive", uri], check=True)
        return
    if scheme == "az":
        parsed = urlparse(uri)
        account_name = os.environ.get("AZURE_STORAGE_ACCOUNT")
        if not account_name:
            raise RuntimeError(
                "AZURE_STORAGE_ACCOUNT must be set to delete Azure checkpoint paths"
            )
        blob_prefix = parsed.path.lstrip("/")
        proc = subprocess.run(
            [
                "az",
                "storage",
                "blob",
                "delete-batch",
                "--account-name",
                account_name,
                "--source",
                parsed.netloc,
                "--pattern",
                f"{blob_prefix}/*",
                "--auth-mode",
                "login",
            ],
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            stderr = (proc.stderr or "").lower()
            if "no matched blobs" in stderr or "cannot find" in stderr:
                print(f"No checkpoint directory found at {uri}")
                return
            proc.check_returncode()
        return
    if scheme == "gs":
        proc = subprocess.run(
            ["gsutil", "-m", "rm", "-r", uri],
            text=True,
            capture_output=True,
        )
        if proc.returncode != 0:
            stderr = (proc.stderr or "").lower()
            if "matched no objects" in stderr:
                print(f"No checkpoint directory found at {uri}")
                return
            proc.check_returncode()
        return

    path = Path(uri)
    if not path.exists():
        print(f"No checkpoint directory found at {uri}")
        return
    print(f"Deleting checkpoint directory {uri}")
    shutil.rmtree(path)


def drop_existing_columns(tbl: Table, columns: list[str]) -> list[str]:
    existing = [col for col in columns if col in tbl.schema.names]
    if existing:
        print(f"Dropping existing columns: {existing}")
        tbl.drop_columns(existing)
    return existing


def worker_replica_override(num_replicas: int) -> dict[str, int]:
    if num_replicas < 1:
        raise ValueError("num_replicas must be >= 1")
    return {
        "replicas": num_replicas,
        "minReplicas": num_replicas,
        "maxReplicas": num_replicas,
    }


def ensure_cluster(
    conn: geneva.Connection,
    csp: str,
    cluster_name: str,
    num_cpu_workers: int | None,
    num_gpu_workers: int | None,
    skip_gpu: bool,
) -> str:
    from geneva.cluster import GenevaCluster, K8sConfigMethod
    from geneva.cluster.builder import KubeRayClusterBuilder
    from geneva.constants import DEFAULT_K8S_NS

    head_selector = (
        {"geneva.lancedb.com/ray-head": "true"}
        if csp == "aws"
        else {"_PLACEHOLDER": "true"}
    )
    worker_selector = {"geneva.lancedb.com/ray-worker-cpu": "true"}
    gpu_worker_selector = {"geneva.lancedb.com/ray-worker-gpu": "true"}
    k8s_config_method = (
        K8sConfigMethod.EKS_AUTH if csp == "aws" else K8sConfigMethod.LOCAL
    )
    service_account = "geneva-service-account"
    if csp == "gcp":
        region = "us-central1"
    elif csp == "aws":
        region = "us-east-1"
    else:
        region = "eastus"

    builder = GenevaCluster.create_kuberay(cluster_name)
    builder = (
        builder
        .namespace(DEFAULT_K8S_NS)
        .config_method(k8s_config_method)
        .head_group(
            service_account=service_account,
            cpus=4,
            memory="16Gi",
            image="rayproject/ray:2.54.0-py310",
            node_selector=head_selector,
        )
        .add_worker_group(
            KubeRayClusterBuilder.cpu_worker()
            .cpus(6)
            .memory("29Gi")
            .image("rayproject/ray:2.54.0-py310")
            .service_account(service_account)
            .node_selector(worker_selector)
            .build()
        )
    )
    if not skip_gpu:
        builder = builder.add_worker_group(
            KubeRayClusterBuilder.gpu_worker()
            .cpus(3.5)
            .memory("14Gi")
            .image("rayproject/ray:2.54.0-py310-gpu")
            .service_account(service_account)
            .node_selector(gpu_worker_selector)
            .build()
        )

    if csp == "aws":
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    if num_cpu_workers is not None:
        cpu_worker_cfg = cluster.kuberay.worker_groups[0]
        cpu_worker_cfg.k8s_spec_override = worker_replica_override(num_cpu_workers)
    if not skip_gpu and num_gpu_workers is not None:
        gpu_worker_cfg = cluster.kuberay.worker_groups[1]
        gpu_worker_cfg.k8s_spec_override = worker_replica_override(num_gpu_workers)
    conn.define_cluster(cluster_name, cluster)
    return cluster_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Geneva benchmark equivalent of Ray large_image_embedding"
    )
    parser.add_argument("--csp", choices=["gcp", "aws", "azure"], default="gcp")
    parser.add_argument("--slug", default=None, help="Slug for bucket/cluster names")
    parser.add_argument(
        "--cluster-name",
        default=None,
        help="Override cluster name (defaults to e2e-large-image-embedding-{slug})",
    )
    parser.add_argument("--bucket", default=None, help="Override bucket path")
    parser.add_argument(
        "--dataset-path",
        default=None,
        help="Existing dataset path (gs://.../table, s3://.../table, or az://.../table). Skips data write",
    )
    parser.add_argument(
        "--num-images",
        type=int,
        default=100_000,
        help="Number of prompts/images to process (max 1431167)",
    )
    parser.add_argument(
        "--fresh-run",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Ignore checkpoints (if --dataset-path is set, delete the table checkpoint directory first)",
    )
    parser.add_argument(
        "--min-checkpoint-size",
        dest="min_checkpoint_size",
        type=int,
        default=1,
        help="Minimum adaptive checkpoint size for backfill operations",
    )
    parser.add_argument(
        "--max-checkpoint-size",
        dest="max_checkpoint_size",
        type=int,
        default=512,
        help="Maximum adaptive checkpoint size for backfill operations",
    )
    parser.add_argument(
        "--task-size",
        type=int,
        default=None,
        help="Rows per read task for backfill operations",
    )
    parser.add_argument(
        "--num-cpu-workers",
        type=int,
        default=5,
        help="Fixed number of CPU Ray workers (replicas/min/max)",
    )
    parser.add_argument(
        "--num-gpu-workers",
        type=int,
        default=5,
        help="Fixed number of GPU Ray workers (replicas/min/max)",
    )
    parser.add_argument(
        "--intra-applier-concurrency",
        type=int,
        default=1,
        help="Threads per worker process for backfill tasks",
    )
    parser.add_argument(
        "--manifest-name",
        default=None,
        help="Manifest name to use when backfilling (defaults depend on preprocess mode)",
    )
    parser.add_argument(
        "--use-merged-preprocess",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Backfill preprocessed directly from image, skipping decoded backfill",
    )
    parser.add_argument(
        "--skip-gpu",
        action=argparse.BooleanOptionalAction,
        default=False,
        help="Skip the final GPU-backed UDF and do not create GPU workers",
    )
    parser.add_argument(
        "--write-concurrency",
        type=int,
        default=16,
        help="Concurrent add workers when building the source table",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    manifest_name = args.manifest_name or default_manifest_name(
        args.use_merged_preprocess
    )
    selected_derived_columns = derived_columns(
        args.use_merged_preprocess, args.skip_gpu
    )

    num_images = args.num_images
    num_frags = max(1, num_images // PROMPT_FRAG_ROWS)
    slug = args.slug or str(uuid.uuid4().hex[:8])
    bucket = args.bucket or default_bucket_path(args.csp, slug)
    cluster_name = args.cluster_name or cluster_name_for_slug(slug)

    if args.dataset_path:
        dataset_bucket, table_name = resolve_dataset_path(args.dataset_path, bucket)
        if args.bucket and dataset_bucket != args.bucket:
            print(
                f"Dataset path bucket {dataset_bucket} overrides --bucket {args.bucket}"
            )
        bucket = dataset_bucket
        if args.fresh_run:
            delete_checkpoint_dir(checkpoint_uri(bucket, table_name))
        conn = geneva.connect(bucket)
        tbl = conn.open_table(table_name)
        print(f"Using existing table {table_name} in {bucket} with {len(tbl)} rows")
        drop_existing_columns(tbl, selected_derived_columns)
    else:
        table_name = f"large_image_embedding_{uuid.uuid4().hex}"
        conn, tbl, num_frags = write_large_image_table(
            bucket,
            table_name,
            num_images=num_images,
            write_concurrency=args.write_concurrency,
        )

        print(
            f"Created table {table_name} in {bucket} with {len(tbl)} rows (num_images={num_images}, num_frags={num_frags})"
        )

    upload_manifest(
        bucket,
        table_name,
        manifest_name,
        args.use_merged_preprocess,
        args.skip_gpu,
    )
    tbl = conn.open_table(table_name)

    cluster_name = ensure_cluster(
        conn,
        args.csp,
        cluster_name,
        args.num_cpu_workers,
        args.num_gpu_workers,
        args.skip_gpu,
    )

    cpu_backfill_concurrency = args.num_cpu_workers if args.num_cpu_workers is not None else 8
    gpu_backfill_concurrency = (
        args.num_gpu_workers if args.num_gpu_workers is not None else 1
    )

    print(
        "num_cpu_workers="
        f"{args.num_cpu_workers}, "
        "num_gpu_workers="
        f"{args.num_gpu_workers}, "
        "use_merged_preprocess="
        f"{args.use_merged_preprocess}, "
        "skip_gpu="
        f"{args.skip_gpu}, "
        "manifest_name="
        f"{manifest_name}, "
        "task_size="
        f"{args.task_size}, "
        "cpu_backfill_concurrency="
        f"{cpu_backfill_concurrency}, "
        "gpu_backfill_concurrency="
        f"{gpu_backfill_concurrency}, "
        "intra_applier_concurrency="
        f"{args.intra_applier_concurrency}"
    )
    with conn.context(cluster=cluster_name, manifest=manifest_name):
        start = time.time()
        for col in selected_derived_columns:
            column_backfill_start = time.time()
            concurrency = (
                gpu_backfill_concurrency
                if col in GPU_DERIVED_COLUMNS
                else cpu_backfill_concurrency
            )
            tbl.backfill(
                col,
                min_checkpoint_size=args.min_checkpoint_size,
                max_checkpoint_size=args.max_checkpoint_size,
                task_size=args.task_size,
                concurrency=concurrency,
                intra_applier_concurrency=args.intra_applier_concurrency,
                num_frags=num_frags,
            )
            print(
                f"Column {col} backfill time: {time.time() - column_backfill_start:.2f}s"
            )

    runtime = time.time() - start
    print(f"Runtime: {runtime:.2f}s")
    print(f"Wrote results to {bucket}/{table_name} using cluster {cluster_name}")


if __name__ == "__main__":
    main()
