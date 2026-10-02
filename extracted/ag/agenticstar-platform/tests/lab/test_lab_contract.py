"""Local integration lab の契約テスト（Docker 不要、molt#1610）。

lab の credential 不要 journey が壊れる典型 drift を固定する:
- offline embedding の決定論（同 input + version → 同 vector）と既知ベクトル regression
- 既知 query が期待文書を retrieve する（Docker なしで cosine 順位を直接検証）
- offline embedding が network / cloud SDK への経路を持たないこと
- docker-compose.yml の version pin / loopback bind / credential が lab_config と一致
- README・main README との drift、README に secret を書かないこと

Docker を使う end-to-end は tests/lab/test_lab_docker.py（LAB_DOCKER_TESTS=1 で opt-in）。
"""

from __future__ import annotations

import math
import re
import sys
from pathlib import Path

SDK_ROOT = Path(__file__).resolve().parents[2]
LAB_DIR = SDK_ROOT / "agenticstar_platform" / "lab"
# site-packages の released 版ではなく repo コピーを検証する
sys.path.insert(0, str(SDK_ROOT))

from agenticstar_platform.lab import lab_config  # noqa: E402
from agenticstar_platform.lab.offline_embedding import OfflineEmbeddingGenerator  # noqa: E402


def _generator() -> OfflineEmbeddingGenerator:
    return OfflineEmbeddingGenerator(
        dimensions=lab_config.EMBEDDING_DIMENSIONS,
        version=lab_config.EMBEDDING_VERSION,
    )


def _cosine(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


class TestOfflineEmbedding:
    async def test_deterministic_same_input_same_vector(self):
        # AC3: 同じ input / version は常に同じ vector
        first = await _generator().generate(lab_config.SAMPLE_QUERY)
        second = await _generator().generate(lab_config.SAMPLE_QUERY)
        assert first == second

    async def test_dimensions_match_qdrant_vector_size(self):
        # QdrantManager は不一致を constructor で拒否する契約なので、ここで固定する
        vec = await _generator().generate("dimension check")
        assert len(vec) == lab_config.EMBEDDING_DIMENSIONS
        qdrant = lab_config.qdrant_config()
        assert qdrant.vector_size == lab_config.EMBEDDING_DIMENSIONS

    async def test_known_vector_regression(self):
        # アルゴリズム/version の無自覚な変更を検出する frozen regression。
        # 変更する場合は EMBEDDING_VERSION を上げ、この期待値を取り直すこと
        vec = await _generator().generate("hello world")
        nonzero = {i: round(v, 12) for i, v in enumerate(vec) if v}
        assert nonzero == {40: 0.707106781187, 69: 0.707106781187}

    async def test_vectors_are_normalized(self):
        for text in ["a", lab_config.SAMPLE_QUERY, ""]:
            vec = await _generator().generate(text)
            assert math.isclose(math.sqrt(sum(v * v for v in vec)), 1.0, rel_tol=1e-9)

    async def test_batch_generate_matches_generate(self):
        texts = [d["content"] for d in lab_config.SYNTHETIC_DOCUMENTS]
        batch = await _generator().batch_generate(texts)
        singles = [await _generator().generate(t) for t in texts]
        assert batch == singles

    async def test_expected_document_wins_retrieval(self):
        # AC2 の retrieval 期待を Docker なしで固定: 既知 query に対して
        # EXPECTED_DOCUMENT_ID が全文書中で最も高い cosine を持つ
        gen = _generator()
        query = await gen.generate(lab_config.SAMPLE_QUERY)
        scores = {
            d["id"]: _cosine(query, await gen.generate(d["content"]))
            for d in lab_config.SYNTHETIC_DOCUMENTS
        }
        best = max(scores, key=scores.get)
        assert best == lab_config.EXPECTED_DOCUMENT_ID, scores
        # 決定論デモとして意味のある差で勝つこと（同率一位の偶然を排除）
        others = [v for k, v in scores.items() if k != best]
        assert scores[best] > max(others) + 0.1, scores

    def test_no_network_or_cloud_dependencies(self):
        # AC3: 外部 network / API key への fallback 経路を持たない
        source = (LAB_DIR / "offline_embedding.py").read_text(encoding="utf-8")
        for banned in ["openai", "httpx", "aiohttp", "requests", "urllib", "socket",
                       "api_key", "http://", "https://"]:
            assert banned not in source, f"offline embedding must not reference {banned}"
        gen = _generator()
        assert not hasattr(gen, "client")


class TestComposeDrift:
    """docker-compose.yml（静的 YAML）と lab_config の値の一致を固定する。"""

    def _compose_text(self) -> str:
        return lab_config.COMPOSE_FILE.read_text(encoding="utf-8")

    def test_compose_file_lives_in_package(self):
        # wheel 同梱の前提: compose がパッケージディレクトリ内にあること
        assert lab_config.COMPOSE_FILE == LAB_DIR / "docker-compose.yml"
        assert lab_config.COMPOSE_FILE.is_file()

    def test_images_match_lab_config_pins_per_service(self):
        # 値集合ではなく service → image の対応ごと lab_config.LAB_IMAGES と一致すること
        text = self._compose_text()
        for service, image in lab_config.LAB_IMAGES.items():
            assert re.search(
                rf"^  {re.escape(service)}:\s*\n\s+image:\s+{re.escape(image)}\s*$",
                text, re.M,
            ), f"{service} must pin image {image}"
            assert not image.endswith(":latest")
        assert len(re.findall(r"image:", text)) == len(lab_config.LAB_IMAGES)

    # host port → container port の期待対応（compose の完全な mapping を固定する）
    EXPECTED_PORT_MAPPINGS = {
        "lab-postgres": [(lab_config.PG_PORT, 5432)],
        "lab-qdrant": [(lab_config.QDRANT_HTTP_PORT, 6333),
                       (lab_config.QDRANT_GRPC_PORT, 6334)],
        "lab-minio": [(lab_config.MINIO_API_PORT, 9000),
                      (lab_config.MINIO_CONSOLE_PORT, 9001)],
    }

    def test_ports_bound_to_loopback_with_expected_targets(self):
        # AC4: lab credential の適用先は loopback のみ。host/target 対応ごと検査する
        text = self._compose_text()
        mappings = re.findall(r'-\s*"([^"]+:\d+:\d+)"', text)
        expected = [f"127.0.0.1:{host}:{target}"
                    for pairs in self.EXPECTED_PORT_MAPPINGS.values()
                    for host, target in pairs]
        assert sorted(mappings) == sorted(expected)
        # SERVICE_PORTS（競合検査対象）が公開 host port 全体と一致すること
        assert sorted(p for ports in lab_config.SERVICE_PORTS.values() for p in ports) \
            == sorted(host for pairs in self.EXPECTED_PORT_MAPPINGS.values()
                      for host, _ in pairs)

    def test_credentials_match_lab_config(self):
        text = self._compose_text()
        assert f"POSTGRES_USER: {lab_config.PG_USER}" in text
        assert f"POSTGRES_PASSWORD: {lab_config.PG_PASSWORD}" in text
        assert f"POSTGRES_DB: {lab_config.PG_DATABASE}" in text
        assert f"MINIO_ROOT_USER: {lab_config.S3_ACCESS_KEY}" in text
        assert f"MINIO_ROOT_PASSWORD: {lab_config.S3_SECRET_KEY}" in text

    def test_named_volumes_and_healthchecks_present(self):
        # 状態保持（通常再起動で消えない）と compose up --wait の前提
        text = self._compose_text()
        for volume in ("lab-postgres-data", "lab-qdrant-data", "lab-minio-data"):
            assert volume in text
        assert text.count("healthcheck:") == 3


class TestLabConfigConsistency:
    def test_synthetic_documents_shape(self):
        docs = lab_config.SYNTHETIC_DOCUMENTS
        assert len(docs) == 3
        ids = [d["id"] for d in docs]
        assert len(set(ids)) == 3
        assert lab_config.EXPECTED_DOCUMENT_ID in ids
        for doc in docs:
            assert doc["content"].strip() and doc["title"].strip()

    def test_component_configs_use_lab_endpoints(self):
        pg = lab_config.postgres_config()
        assert (pg.host, pg.port) == (lab_config.PG_HOST, lab_config.PG_PORT)
        assert pg.ssl_mode == "disable"
        qd = lab_config.qdrant_config()
        assert qd.url == lab_config.QDRANT_URL
        assert qd.check_compatibility is False
        s3 = lab_config.s3_config()
        assert s3.endpoint_url == lab_config.S3_ENDPOINT
        assert s3.bucket_name == lab_config.S3_BUCKET
        assert s3.auto_create_bucket is True

    def test_artifacts_dir_outside_package(self):
        # site-packages（パッケージ内）を汚さない: artifact は cwd 配下
        assert LAB_DIR not in lab_config.ARTIFACTS_DIR.parents
        assert lab_config.ARTIFACTS_DIR.name == "agenticstar-lab-artifacts"

    def test_lab_extra_covers_required_modules(self):
        # [lab] extra が REQUIRED_MODULES を満たすこと（pyproject との drift 検出）
        pyproject = (SDK_ROOT / "pyproject.toml").read_text(encoding="utf-8")
        lab_block = re.search(r"^lab = \[(.*?)\]", pyproject, re.S | re.M)
        assert lab_block, "[lab] extra が pyproject にない"
        # module 名 → pip パッケージ名（REQUIRED_MODULES の全 module が対象）
        module_to_dep = {
            "asyncpg": "asyncpg",
            "azure.identity": "azure-identity",
            "qdrant_client": "qdrant-client",
            "openai": "openai",
            "boto3": "boto3",
        }
        assert set(module_to_dep) == set(lab_config.REQUIRED_MODULES)
        for module, dep in module_to_dep.items():
            assert dep in lab_block.group(1), f"[lab] extra に {dep} ({module}) がない"


class TestExtrasCheck:
    def test_missing_parent_package_is_reported_not_raised(self, monkeypatch):
        # dotted module（azure.identity 型）は親 package 不在だと find_spec 自体が
        # ModuleNotFoundError を投げる。check_extras は例外にせず「不足」として
        # install hint を返すこと（core-only インストールの外部利用者経路）
        from agenticstar_platform.lab import checks

        monkeypatch.setattr(
            lab_config, "REQUIRED_MODULES",
            {"no_such_parent_pkg_xyz.identity": "db"},
        )
        results = checks.check_extras()
        assert len(results) == 1 and results[0].ok is False
        assert "no_such_parent_pkg_xyz.identity" in results[0].reason
        assert results[0].next_command == lab_config.INSTALL_HINT


class TestReadmeDrift:
    def test_lab_readme_mentions_entrypoints(self):
        text = (LAB_DIR / "README.md").read_text(encoding="utf-8")
        for needle in ["python -m agenticstar_platform.lab", "doctor", "--reset",
                       "agenticstar-platform[lab]"]:
            assert needle in text

    def test_lab_readme_does_not_echo_secrets(self):
        # AC4: README/出力に secret を表示しない（固定値であっても echo しない）
        text = (LAB_DIR / "README.md").read_text(encoding="utf-8")
        assert lab_config.PG_PASSWORD not in text
        assert lab_config.S3_SECRET_KEY not in text

    def test_main_readme_links_to_lab(self):
        text = (SDK_ROOT / "README.md").read_text(encoding="utf-8")
        assert "python -m agenticstar_platform.lab" in text
        assert "agenticstar-platform[lab]" in text

    def test_run_lab_does_not_print_secrets(self):
        # stdout へ credential を出さない: 出力を作る行に secret 参照・実値が無いこと
        for name in ("run_lab.py", "doctor.py", "checks.py", "seed.py", "__main__.py"):
            source = (LAB_DIR / name).read_text(encoding="utf-8")
            for lineno, line in enumerate(source.splitlines(), 1):
                if "print(" in line or "render" in line:
                    for marker in ("PG_PASSWORD", "S3_SECRET_KEY",
                                   lab_config.PG_PASSWORD, lab_config.S3_SECRET_KEY):
                        assert marker not in line, f"{name}:{lineno} prints a secret"
