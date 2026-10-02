"""Local integration lab — 1 コマンドで credential 不要の SDK 統合 journey を完走する。

    python -m agenticstar_platform.lab           # prerequisites → services → seed → agent run → verify
    python -m agenticstar_platform.lab --reset   # lab の container / volume / artifact を破棄（確認あり）
    python -m agenticstar_platform.lab doctor    # read-only 診断

journey: synthetic 3 文書を Qdrant へ ingest → 既知 query で retrieve →
artifact を S3 互換 storage へ、result を PostgreSQL へ persist →
terminal event（COMPLETION_SUCCESS / COMPLETION_FAILURE を正確に 1 回）。

cloud account・production credential・手動 .env 編集は不要。使用する credential は
lab 専用の非本番固定値のみ（lab_config.py 参照。stdout には表示しない）。
artifact のローカルコピーは実行時 cwd の agenticstar-lab-artifacts/ に置かれる。
"""

from __future__ import annotations

import argparse
import asyncio
import json
import subprocess
import sys
import time
import uuid

from . import checks, lab_config
from . import seed as seed_module
from .offline_embedding import OfflineEmbeddingGenerator

PHASES = ["prerequisites", "services", "seed", "agent run", "verify"]


def _phase(n: int) -> None:
    print(f"\n[{n}/{len(PHASES)}] {PHASES[n - 1]}")


def _fail(message: str, next_command: str = "python -m agenticstar_platform.lab doctor") -> "NoReturn":  # noqa: F821
    print(f"\n❌ {message}")
    print(f"   next: {next_command}")
    sys.exit(1)


# ---------------------------------------------------------------- phase 1
def phase_prerequisites() -> None:
    _phase(1)
    results = [checks.check_docker_cli()]
    if results[-1].ok:
        results.append(checks.check_docker_daemon())
        if results[-1].ok:
            results.append(checks.check_compose())
    results.extend(checks.check_extras())
    # artifact 出力先の使用可否は service 起動前に preflight する
    # （phase 4 で初めて気づくと container/seed が作られた後になるため）
    results.append(checks.check_artifacts_path())
    for r in results:
        print("  " + r.render())
    if not all(r.ok for r in results):
        _fail("prerequisites を満たしていません（上の next を実行してください）")


# ---------------------------------------------------------------- phase 2
def phase_services(timeout_seconds: int = 180) -> None:
    _phase(2)
    print(f"  docker compose up -d --wait ({lab_config.COMPOSE_FILE.name})")
    try:
        proc = subprocess.run(
            ["docker", "compose", "-p", lab_config.COMPOSE_PROJECT,
             "-f", str(lab_config.COMPOSE_FILE), "up", "-d", "--wait"],
            capture_output=True, text=True, timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired:
        _fail(f"service の起動が {timeout_seconds}s で timeout しました")
    if proc.returncode != 0:
        print(proc.stderr.strip()[-2000:])
        _fail("service の起動に失敗しました")

    deadline = time.monotonic() + 60
    while True:
        pg = asyncio.run(checks.probe_postgres())
        ready = pg and checks.probe_qdrant() and checks.probe_minio()
        if ready:
            break
        if time.monotonic() >= deadline:
            _fail("service が readiness に到達しません")
        time.sleep(2)
    print("  ✅ lab-postgres / lab-qdrant / lab-minio ready "
          f"({lab_config.PG_HOST}:{lab_config.PG_PORT}, {lab_config.QDRANT_URL}, {lab_config.S3_ENDPOINT})")


# ---------------------------------------------------------------- phase 3
def phase_seed() -> None:
    _phase(3)
    try:
        summary = asyncio.run(seed_module.apply())
    except seed_module.SeedVersionMismatch as exc:
        _fail(f"seed version 不一致: {exc}", "python -m agenticstar_platform.lab --reset")
    except Exception as exc:  # traceback ではなく分類したメッセージで止める
        _fail(f"seed に失敗しました: {type(exc).__name__}: {exc}")
    print(f"  ✅ schema + {summary['documents']} synthetic documents "
          f"(collection={summary['collection']}, bucket={summary['bucket']})")


# ---------------------------------------------------------------- phase 4
async def _agent_journey(execution_id: str) -> dict:
    """RAG journey 本体。呼び出し側（_run_agent）が terminal event を保証する。"""
    from agenticstar_platform import EventType
    from agenticstar_platform.db import DataAccess, PostgreSQLManager
    from agenticstar_platform.rag import QdrantManager
    from agenticstar_platform.storage import S3StorageClient

    embedding = OfflineEmbeddingGenerator(
        dimensions=lab_config.EMBEDDING_DIMENSIONS,
        version=lab_config.EMBEDDING_VERSION,
    )

    # retrieve
    async with QdrantManager(lab_config.qdrant_config(), embedding) as qdrant:
        search = await qdrant.search(query_text=lab_config.SAMPLE_QUERY, limit=1,
                                     score_threshold=0.0)
    if not search.get("success") or not search["data"]["results"]:
        raise RuntimeError(f"retrieve failed: {search.get('error', 'no results')}")
    hit = search["data"]["results"][0]
    retrieved_id = hit["payload"]["document_id"]
    retrieved_title = hit["payload"].get("title", "")

    # artifact 生成 → S3 互換 storage へ persist
    lab_config.ARTIFACTS_DIR.mkdir(exist_ok=True)
    artifact_path = lab_config.ARTIFACTS_DIR / f"answer-{execution_id}.md"
    artifact_path.write_text(
        f"# Lab answer ({execution_id})\n\n"
        f"query: {lab_config.SAMPLE_QUERY}\n\n"
        f"retrieved: {retrieved_id} ({retrieved_title}), "
        f"similarity={hit['similarity']:.3f}\n\n"
        f"---\n\n{hit['payload'].get('content', '')}\n",
        encoding="utf-8",
    )
    storage = S3StorageClient(lab_config.s3_config())
    try:
        upload = await storage.upload_file(str(artifact_path), prefix=execution_id)
        if not upload.success or not upload.object_name:
            raise RuntimeError(
                f"artifact upload failed: {upload.error} ({upload.error_code})"
            )
        artifact_object = upload.object_name
    finally:
        await storage.close()

    # result を PostgreSQL へ persist
    manager = PostgreSQLManager(lab_config.postgres_config())
    da = DataAccess(manager)
    await da.initialize()
    try:
        inserted = await da.insert(
            lab_config.RESULTS_TABLE,
            {
                "execution_id": execution_id,
                "query": lab_config.SAMPLE_QUERY,
                "retrieved_document_id": retrieved_id,
                "artifact_object": artifact_object,
                "outcome": EventType.COMPLETION_SUCCESS.value,
            },
        )
        if not inserted.get("success"):
            raise RuntimeError(f"result insert failed: {inserted.get('error')}")
    finally:
        await da.close()

    return {
        "retrieved_document_id": retrieved_id,
        "retrieved_title": retrieved_title,
        "similarity": hit["similarity"],
        "artifact_object": artifact_object,
        "artifact_path": str(artifact_path),
    }


async def _run_agent(execution_id: str) -> dict:
    from agenticstar_platform import EventEmitter, EventType, create_json_handler

    emitter = EventEmitter(execution_id=execution_id, handler=create_json_handler())
    outcome: dict = {}

    async def agent() -> None:
        await emitter.emit_event(
            EventType.PHASE_START, f"lab journey: {lab_config.SAMPLE_QUERY}"
        )
        try:
            result = await _agent_journey(execution_id)
        except Exception as exc:  # terminal event は正確に 1 回（失敗時は FAILURE）
            outcome["error"] = f"{type(exc).__name__}: {exc}"
            await emitter.emit_event(EventType.COMPLETION_FAILURE, outcome["error"])
            return
        outcome.update(result)
        await emitter.emit_event(
            EventType.COMPLETION_SUCCESS,
            json.dumps({"retrieved": result["retrieved_document_id"],
                        "artifact": result["artifact_object"]}),
        )

    task = asyncio.create_task(agent())
    async for chunk in emitter.consume_events():
        print("  " + chunk)
    await task
    return outcome


def phase_agent_run(execution_id: str) -> dict:
    _phase(4)
    outcome = asyncio.run(_run_agent(execution_id))
    if "error" in outcome:
        _fail(f"agent run failed: {outcome['error']}")
    return outcome


# ---------------------------------------------------------------- phase 5
async def _verify(execution_id: str, outcome: dict) -> None:
    from agenticstar_platform.db import DataAccess, PostgreSQLManager
    from agenticstar_platform.rag import QdrantManager
    from agenticstar_platform.storage import S3StorageClient

    # PostgreSQL に result row
    manager = PostgreSQLManager(lab_config.postgres_config())
    da = DataAccess(manager)
    await da.initialize()
    try:
        row = await da.select_one(
            lab_config.RESULTS_TABLE, where={"execution_id": execution_id}
        )
        if row is None:
            raise RuntimeError(f"result row not found for {execution_id}")
    finally:
        await da.close()

    # S3 互換 storage に artifact
    storage = S3StorageClient(lab_config.s3_config())
    try:
        exists = await storage.object_exists(outcome["artifact_object"])
        if not exists:
            raise RuntimeError(f"artifact object missing: {outcome['artifact_object']}")
    finally:
        await storage.close()

    # Qdrant に synthetic 文書 + 期待 retrieval
    embedding = OfflineEmbeddingGenerator(
        dimensions=lab_config.EMBEDDING_DIMENSIONS,
        version=lab_config.EMBEDDING_VERSION,
    )
    async with QdrantManager(lab_config.qdrant_config(), embedding) as qdrant:
        stats = await qdrant.get_statistics()
    points = (stats.get("data") or {}).get("total_objects", 0)
    if points < len(lab_config.SYNTHETIC_DOCUMENTS):
        raise RuntimeError(f"collection has {points} points, expected >= "
                           f"{len(lab_config.SYNTHETIC_DOCUMENTS)}")

    if outcome["retrieved_document_id"] != lab_config.EXPECTED_DOCUMENT_ID:
        raise RuntimeError(
            f"retrieved {outcome['retrieved_document_id']}, "
            f"expected {lab_config.EXPECTED_DOCUMENT_ID}"
        )


def phase_verify(execution_id: str, outcome: dict) -> None:
    _phase(5)
    try:
        asyncio.run(_verify(execution_id, outcome))
    except Exception as exc:
        # terminal event（agent run の結果）は phase 4 で送信済み。verify は
        # lab 側の整合性検証なので、二重の terminal event は送らず exit code で示す
        _fail("agent run は成功しましたが、lab の整合性検証に失敗しました: "
              f"{exc}")
    print("  ✅ result row (PostgreSQL) / artifact (S3 互換 storage) / "
          f"{len(lab_config.SYNTHETIC_DOCUMENTS)} documents (Qdrant) を確認")

    print("\n🎉 lab journey succeeded")
    print(f"  retrieved : {outcome['retrieved_document_id']} "
          f"({outcome['retrieved_title']}, similarity={outcome['similarity']:.3f})")
    print(f"  artifact  : s3://{lab_config.S3_BUCKET}/{outcome['artifact_object']} "
          f"(local copy: {outcome['artifact_path']})")
    print("  outcome   : completion_success (exactly one terminal event)")
    print("\n" + lab_config.NEXT_STEP_HINT)


# ---------------------------------------------------------------- reset
def do_reset(assume_yes: bool) -> None:
    # 破壊的操作を始める前に artifact ディレクトリの安全性を確認する
    # （symlink だと第三者のディレクトリを消しうるため、何もせず中止）
    if lab_config.ARTIFACTS_DIR.is_symlink():
        _fail(f"{lab_config.ARTIFACTS_DIR} が symlink のため reset を中止しました"
              "（何も削除していません）",
              f"ls -la {lab_config.ARTIFACTS_DIR}")
    volumes = [f"{lab_config.COMPOSE_PROJECT}_lab-{name}-data"
               for name in ("postgres", "qdrant", "minio")]
    print("reset は以下を削除します:")
    print(f"  - containers: compose project '{lab_config.COMPOSE_PROJECT}' "
          "(lab-postgres / lab-qdrant / lab-minio)")
    for v in volumes:
        print(f"  - volume: {v}")
    print(f"  - local artifacts: {lab_config.ARTIFACTS_DIR} 配下の answer-lab-*.md "
          "（lab が生成したファイルのみ）")
    if not assume_yes:
        answer = input("削除して良ければ 'reset' と入力してください: ").strip()
        if answer != "reset":
            print("中止しました（何も削除していません）")
            sys.exit(0)
    # --remove-orphans は使わない: 事前列挙した manifest 記載 service 以外
    # （同名 project を流用した別 container 等）を巻き込まないため
    try:
        proc = subprocess.run(
            ["docker", "compose", "-p", lab_config.COMPOSE_PROJECT,
             "-f", str(lab_config.COMPOSE_FILE), "down", "-v"],
            capture_output=True, text=True, timeout=120,
        )
    except (subprocess.TimeoutExpired, OSError) as exc:
        _fail(f"compose down -v を実行できませんでした: {type(exc).__name__}: {exc}")
    if proc.returncode != 0:
        print(proc.stderr.strip()[-2000:])
        _fail("compose down -v に失敗しました")
    artifacts = lab_config.ARTIFACTS_DIR
    if artifacts.is_dir() and not artifacts.is_symlink():
        # cwd 配下の共有されうるディレクトリなので、lab が生成した命名パターンの
        # 通常ファイルだけを削除する（利用者のファイルは消さない）
        for f in artifacts.glob("answer-lab-*.md"):
            if f.is_file() and not f.is_symlink():
                f.unlink()
        try:
            artifacts.rmdir()
        except OSError:
            print(f"  note: {artifacts} に lab 由来でないエントリが残っているため"
                  "ディレクトリ自体は残しました")
    print("✅ reset 完了（次回の実行は初期状態から始まります）")


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="python -m agenticstar_platform.lab", description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--reset", action="store_true",
                        help="lab の container / volume / artifact を破棄する")
    parser.add_argument("--yes", action="store_true",
                        help="reset の確認プロンプトを省略する")
    args = parser.parse_args()

    if args.reset:
        do_reset(args.yes)
        return

    started = time.monotonic()
    execution_id = f"lab-{uuid.uuid4().hex[:8]}"
    phase_prerequisites()
    phase_services()
    phase_seed()
    outcome = phase_agent_run(execution_id)
    phase_verify(execution_id, outcome)
    print(f"\ntotal: {time.monotonic() - started:.1f}s (execution_id={execution_id})")


if __name__ == "__main__":
    main()
