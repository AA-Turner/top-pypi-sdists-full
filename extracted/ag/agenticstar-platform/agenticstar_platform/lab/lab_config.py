"""Local integration lab の単一正本設定（molt#1610）。

compose manifest・seed・sample・doctor・テストはすべてこのファイルの値を参照する
（docker-compose.yml は静的 YAML のため、値の一致は tests/lab/test_lab_contract.py の
drift テストで固定する）。

ここに書かれた credential は **lab 専用の非本番固定値** で、loopback (127.0.0.1) に
bind された local container にのみ適用される。production credential をここに書いては
ならないし、lab が要求・保存することもない。
"""

from __future__ import annotations

from pathlib import Path

LAB_DIR = Path(__file__).resolve().parent
COMPOSE_FILE = LAB_DIR / "docker-compose.yml"
COMPOSE_PROJECT = "agenticstar-lab"
# artifact はパッケージ内（site-packages）ではなく実行時 cwd へ出力する
ARTIFACTS_DIR = Path.cwd() / "agenticstar-lab-artifacts"

# seed / embedding のバージョン（互換性検証に使用。schema や文書を変えたら上げる）
SEED_VERSION = "1"
EMBEDDING_VERSION = "lab-offline-hashing-v1"
EMBEDDING_DIMENSIONS = 256

# --- PostgreSQL（lab 専用・非本番固定値） ---
PG_HOST = "127.0.0.1"
PG_PORT = 15432
PG_DATABASE = "agenticstar_lab"
PG_USER = "agenticstar_lab"
PG_PASSWORD = "agenticstar-lab-local-only"  # lab 専用固定値（本番 secret ではない）

# --- Qdrant ---
QDRANT_HTTP_PORT = 16333
QDRANT_GRPC_PORT = 16334
QDRANT_URL = f"http://127.0.0.1:{QDRANT_HTTP_PORT}"
QDRANT_COLLECTION = "lab_documents"

# --- S3 互換 storage（MinIO、lab 専用・非本番固定値） ---
MINIO_API_PORT = 19000
MINIO_CONSOLE_PORT = 19001
S3_ENDPOINT = f"http://127.0.0.1:{MINIO_API_PORT}"
S3_ACCESS_KEY = "agenticstar-lab"
S3_SECRET_KEY = "agenticstar-lab-local-only"  # lab 専用固定値（本番 secret ではない）
S3_BUCKET = "agenticstar-lab-artifacts"

# --- DB テーブル ---
RESULTS_TABLE = "lab_results"
META_TABLE = "lab_meta"

# --- compose の version 固定イメージ（drift はテストで検出） ---
LAB_IMAGES = {
    "lab-postgres": "postgres:16.6-alpine",
    "lab-qdrant": "qdrant/qdrant:v1.12.5",
    "lab-minio": "minio/minio:RELEASE.2024-01-16T16-07-38Z",
}

# service ごとの公開 host port（port 競合検査はこの全 port を対象にする）
SERVICE_PORTS = {
    "lab-postgres": [PG_PORT],
    "lab-qdrant": [QDRANT_HTTP_PORT, QDRANT_GRPC_PORT],
    "lab-minio": [MINIO_API_PORT, MINIO_CONSOLE_PORT],
}

# --- synthetic 文書（3件・低機微・英語） ---
SYNTHETIC_DOCUMENTS = [
    {
        "id": "doc-terminal-events",
        "title": "Terminal events",
        "content": (
            "Every agent run must emit exactly one terminal event. "
            "Emit COMPLETION_SUCCESS when the agent finishes successfully, "
            "or COMPLETION_FAILURE when it fails. The terminal event is what "
            "tells the frontend that the run is complete."
        ),
    },
    {
        "id": "doc-marketplace-runner",
        "title": "Marketplace runner",
        "content": (
            "run_marketplace_agent wraps your agent function with the "
            "Marketplace lifecycle: identity validation from environment "
            "variables, input message fetch, database persistence, webhook "
            "notification and cleanup."
        ),
    },
    {
        "id": "doc-artifact-storage",
        "title": "Artifact storage",
        "content": (
            "Store generated artifacts in object storage and persist run "
            "results to PostgreSQL so that users can download the outputs "
            "of a run later from the frontend."
        ),
    },
]

# 既知 query と期待 retrieval（offline embedding はトークン重合ベースなので、
# 語彙が重なる doc-terminal-events が決定論的に最上位になる。
# tests/lab/test_lab_contract.py が docker なしでこの期待を固定している）
SAMPLE_QUERY = "How does my agent emit exactly one terminal event when it finishes?"
EXPECTED_DOCUMENT_ID = "doc-terminal-events"

# 成功時に案内する次の一歩（README「### 2. 同じ関数を Marketplace 互換で動かす」）
NEXT_STEP_HINT = (
    "Next: make the same agent Marketplace-compatible.\n"
    "  See README section '2. 同じ関数を Marketplace 互換で動かす（runner）' and run:\n"
    "    pip install 'agenticstar-platform[runner]'\n"
    "    python marketplace_agent.py"
)

# lab が必要とする extra（doctor / run_lab の prerequisites 検査で使用）
REQUIRED_MODULES = {
    "asyncpg": "db",
    "azure.identity": "db",   # db extra 同梱（PostgreSQLManager が無条件 import）
    "qdrant_client": "rag",
    "openai": "rag",          # rag extra 同梱（embedding module が無条件 import）
    "boto3": "storage-aws",
}
INSTALL_HINT = "pip install 'agenticstar-platform[lab]'"


def postgres_config():
    """lab 用 PostgreSQLConfig（db extra が必要）。"""
    from agenticstar_platform.db import PostgreSQLConfig

    return PostgreSQLConfig(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DATABASE,
        username=PG_USER,
        password=PG_PASSWORD,
        pool_min_size=1,
        pool_max_size=4,
        ssl_mode="disable",  # loopback の lab container に SSL は不要
    )


def qdrant_config():
    """lab 用 QdrantConfig（rag extra が必要）。

    vector_size は offline embedding の EMBEDDING_DIMENSIONS と一致させる
    （QdrantManager が constructor で不一致を拒否する）。
    """
    from agenticstar_platform.rag import QdrantConfig

    return QdrantConfig(
        url=QDRANT_URL,
        collection_name=QDRANT_COLLECTION,
        vector_size=EMBEDDING_DIMENSIONS,
        prefer_grpc=False,
        check_compatibility=False,
    )


def s3_config():
    """lab 用 S3Config（storage-aws extra が必要）。"""
    from agenticstar_platform.storage import S3Config

    return S3Config(
        bucket_name=S3_BUCKET,
        aws_access_key_id=S3_ACCESS_KEY,
        aws_secret_access_key=S3_SECRET_KEY,
        endpoint_url=S3_ENDPOINT,
        auto_create_bucket=True,
    )
