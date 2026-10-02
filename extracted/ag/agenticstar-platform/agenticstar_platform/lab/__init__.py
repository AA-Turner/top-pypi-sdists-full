"""Local integration lab — credential 不要の SDK 統合 journey（molt#1610）。

    pip install 'agenticstar-platform[lab]'
    python -m agenticstar_platform.lab            # journey 実行（1 コマンド）
    python -m agenticstar_platform.lab doctor     # read-only 診断
    python -m agenticstar_platform.lab --reset    # 破棄（確認あり / --yes で省略）

PostgreSQL / Qdrant / S3 互換 storage (MinIO) を version 固定の Docker Compose で
起動し、synthetic 文書の ingest → retrieve → artifact/result persist →
terminal outcome を完走する。必要なのは Docker (compose v2) と Python 3.11+ だけ。
詳細はこのディレクトリの README.md を参照。

この __init__ は意図的に何も import しない（`import agenticstar_platform` の
軽量性を保つため。実行は __main__ 経由）。
"""
