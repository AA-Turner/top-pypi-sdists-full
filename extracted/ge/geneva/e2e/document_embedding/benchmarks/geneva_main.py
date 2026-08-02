# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import time
import uuid
from pathlib import Path

import geneva
from geneva.cluster import GenevaCluster, K8sConfigMethod
from geneva.cluster.builder import KubeRayClusterBuilder
from geneva.cluster.mgr import WorkerGroupConfig
from geneva.constants import DEFAULT_K8S_NS

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

from dataset import SOURCE_METADATA_PATH, load_document_metadata

DEFAULT_MANIFEST = "document-embedding-udfs-v1"
DERIVED_COLUMNS = ["pdf_bytes", "pages", "chunks", "chunk_embeddings"]
HEAD_SELECTOR_GCP = {"_PLACEHOLDER": "true"}
WORKER_SELECTOR_GCP = {"_PLACEHOLDER": "true"}
CLUSTER_NAME = "e2e-document-embedding-benchmark-cluster"
DEFAULT_HEAD_MEMORY = "3Gi"
AZURE_HEAD_MEMORY = "8Gi"


def _head_memory_for_csp(csp: str) -> str:
    if csp == "azure":
        return AZURE_HEAD_MEMORY
    return DEFAULT_HEAD_MEMORY


def upload_manifest(bucket: str, table_name: str, manifest_name: str) -> None:
    env = os.environ.copy()
    env["GENEVA_TABLE_NAME"] = table_name
    subprocess.run(
        [
            "uv",
            "run",
            "python",
            "upload_manifests.py",
            "--bucket",
            bucket,
            "--profile",
            "pdf_embedding",
            "--manifest-name",
            manifest_name,
        ],
        cwd=str(_ROOT),
        check=True,
        env=env,
    )


def ensure_cluster(conn: geneva.Connection, csp: str) -> str:
    """
    Define the benchmark cluster: 8 GPU workers, worker selector matches Ray Data benchmark.
    """
    head_selector = HEAD_SELECTOR_GCP
    worker_selector = WORKER_SELECTOR_GCP
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

    worker_cfg = WorkerGroupConfig(
        service_account=service_account,
        num_cpus=4,
        memory="16Gi",
        image="rayproject/ray:2.54.0-py310",
        num_gpus=1,
        node_selector=worker_selector,
        labels={},
        tolerations=[],
        k8s_spec_override={"replicas": 8, "min_replicas": 8, "max_replicas": 8},
    )

    builder = (
        GenevaCluster.create_kuberay(CLUSTER_NAME)
        .namespace(DEFAULT_K8S_NS)
        .config_method(k8s_config_method)
        .head_group(
            service_account=service_account,
            cpus=1,
            memory=_head_memory_for_csp(csp),
            image="rayproject/ray:2.54.0-py310",
            node_selector=head_selector,
        )
        # placeholder worker group; replaced below with explicit replicas
        .add_worker_group(
            KubeRayClusterBuilder.gpu_worker()
            .cpus(4)
            .memory("16Gi")
            .image("rayproject/ray:2.54.0-py310")
            .service_account(service_account)
            .node_selector(worker_selector)
            .build()
        )
    )

    if csp == "aws":
        builder.aws_config(region=region, role_name="geneva-client-role")

    cluster = builder.build()
    cluster.kuberay.worker_groups = [worker_cfg]

    conn.define_cluster(CLUSTER_NAME, cluster)
    return CLUSTER_NAME


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Geneva benchmark equivalent of ray_data_main.py (uses e2e fixtures)"
    )
    parser.add_argument("--csp", choices=["gcp", "aws", "azure"], default="gcp")
    parser.add_argument(
        "--slug", default=None, help="Slug for bucket path (random if omitted)"
    )
    parser.add_argument("--bucket", default=None, help="Override bucket path")
    parser.add_argument("--num-docs", type=int, default=200, help="Number of PDFs")
    parser.add_argument("--batch-size", type=int, default=8, help="Backfill batch size")
    parser.add_argument(
        "--manifest-name",
        default=DEFAULT_MANIFEST,
        help="Manifest name to use when backfilling",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    slug = args.slug or str(uuid.uuid4().hex[:8])
    bucket = args.bucket or default_bucket_path(args.csp, slug)

    metadata = load_document_metadata(args.num_docs, SOURCE_METADATA_PATH)
    if len(metadata) == 0:
        raise RuntimeError("No document metadata loaded; cannot run benchmark")

    conn = geneva.connect(bucket)
    table_name = f"document_embedding_{uuid.uuid4().hex}"
    tbl = conn.create_table(table_name, metadata, mode="overwrite")

    print(f"Created table {table_name} in {bucket} with {len(tbl)} rows")

    upload_manifest(bucket, table_name, args.manifest_name)
    tbl = conn.open_table(table_name)

    cluster_name = ensure_cluster(conn, args.csp)

    start = time.time()
    with conn.context(cluster=cluster_name, manifest=args.manifest_name):
        for col in DERIVED_COLUMNS:
            tbl.backfill(col, batch_size=args.batch_size)

    runtime = time.time() - start
    print(f"Runtime: {runtime:.2f}s")
    print(f"Wrote results to {bucket}/{table_name} using cluster {cluster_name}")


if __name__ == "__main__":
    main()
