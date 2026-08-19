# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for the single-pass shuffled reference-table generator.

The Feistel shuffle and the vectorized derivation (the correctness boundary —
locators must match the scalar ``upload_images`` helpers byte-for-byte) are tested
without any infrastructure; a local multiprocessing build + a resume case exercise
the bootstrap → ``LanceFragment.create`` → batch ``Append`` path against local Lance.
"""

from __future__ import annotations

from typing import Any

import numpy as np
import pyarrow as pa
import pytest

from loadtest.azure_scale_bench import (
    benchmark_env,
    build_ref_table,
    constants,
    image_distribution,
    synthetic_image,
    upload_images,
)
from loadtest.azure_scale_bench.benchmark_env import BenchConfig


def _write_seed(
    tmp_path: Any,
    *,
    object_count: int,
    accounts: tuple[str, ...] = ("acct0", "acct1"),
    prefix_count: int = 8,
    image_format: str = "png",
    include_large_tail: bool = False,
    max_image_bytes: int | None = None,
    seed_run_id: str = "testrun",
) -> str:
    """Write a local ``.seedrun.json`` and return its URI (no Azure)."""
    record = upload_images.SeedRunConfig(
        schema_version=1,
        generator_version=constants.GENERATOR_VERSION,
        distribution_version=constants.DISTRIBUTION_VERSION,
        seed_run_id=seed_run_id,
        seed_run_salt=upload_images._seed_run_salt(seed_run_id),
        object_count=object_count,
        accounts=list(accounts),
        container="datasets",
        base_prefix="loadtest/images",
        prefix_count=prefix_count,
        image_format=image_format,
        include_large_tail=include_large_tail,
        max_image_bytes=max_image_bytes,
        created_at="2026-01-01T00:00:00+00:00",
        delete_after="2026-07-01T00:00:00+00:00",
        manifest_uri=str(tmp_path / "manifest.lance"),
    )
    uri = str(tmp_path / "manifest.seedrun.json")
    upload_images.write_seed_run(uri, record, {})
    return uri


def _local_cfg(
    monkeypatch: Any, tmp_path: Any, seed_uri: str, **kw: Any
) -> BenchConfig:
    """A BenchConfig pointing at local paths (no Azure storage_options)."""
    monkeypatch.setattr(benchmark_env, "storage_options_from_env", lambda **_: {})
    return BenchConfig(
        seed_run_config_uri=seed_uri, bench_uri=str(tmp_path / "ref.lance"), **kw
    )


# --- Hash + Feistel (pure) --------------------------------------------------


def test_vec_row_hash_matches_pins_and_scalar() -> None:
    pins = build_ref_table._vec_row_hash(np.array([0, 1, 12345], dtype=np.uint64))
    assert pins.tolist() == [
        0xE220A8397B1DCDAF,
        0x910A2DEC89025CC1,
        0x22118258A9D111A0,
    ]
    rng = np.arange(0, 1000, dtype=np.uint64)
    vec = build_ref_table._vec_row_hash(rng)
    assert vec.tolist() == [image_distribution.row_hash(int(x)) for x in rng]


@pytest.mark.parametrize("m", [1, 2, 3, 4, 7, 8, 16, 17, 100, 1000, 1024])
def test_feistel_is_a_bijection(m: int) -> None:
    y = build_ref_table.feistel(np.arange(m, dtype=np.uint64), m=m, salt=0)
    assert int(y.min()) >= 0
    assert int(y.max()) < m
    assert sorted(y.tolist()) == list(range(m))


def test_feistel_deterministic_and_salt_sensitive() -> None:
    r = np.arange(1000, dtype=np.uint64)
    a = build_ref_table.feistel(r, m=1000, salt=0)
    b = build_ref_table.feistel(r, m=1000, salt=0)
    c = build_ref_table.feistel(r, m=1000, salt=7)
    assert a.tolist() == b.tolist()
    assert a.tolist() != c.tolist()


def test_copy_counts_exact_when_divisible() -> None:
    n, m = 100, 1000
    img, exp = build_ref_table.map_rows(np.arange(m, dtype=np.uint64), n=n, m=m, salt=3)
    counts = np.bincount(img.astype(np.int64), minlength=n)
    assert counts.tolist() == [m // n] * n
    # Every (image_id, expansion_index) pair is unique.
    assert len({*zip(img.tolist(), exp.tolist(), strict=True)}) == m


def test_copy_counts_within_one_when_not_divisible() -> None:
    n, m = 100, 950
    img, _ = build_ref_table.map_rows(np.arange(m, dtype=np.uint64), n=n, m=m, salt=1)
    counts = np.bincount(img.astype(np.int64), minlength=n)
    assert set(counts.tolist()) <= {m // n, m // n + 1}
    assert int(counts.sum()) == m


def test_adjacency_rate_is_effectively_zero() -> None:
    # With copies present (m > n) the shuffle must not cluster an image's copies:
    # adjacency stays Poisson with rate ~ sample/n (here ~0.5), not the n-fold
    # spikes a block-interleaved layout would give. Threshold is a generous margin.
    n, m = 10_000, 100_000
    r = np.arange(5000, dtype=np.uint64)
    img, _ = build_ref_table.map_rows(r, n=n, m=m, salt=0)
    adjacent = int(np.sum(img[1:] == img[:-1]))
    assert adjacent <= 5


# --- Derivation equivalence (the correctness boundary) ----------------------


def test_vectorized_derivation_matches_scalar(tmp_path: Any, monkeypatch: Any) -> None:
    seed_uri = _write_seed(
        tmp_path, object_count=2000, accounts=("a", "b", "c"), prefix_count=64
    )
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=2000,
        rows_per_fragment=2000,
        validate_build=False,
    )
    plan = build_ref_table._plan_from_cfg(cfg)
    params = plan.params
    table = build_ref_table.generate_fragment(0, plan.m, plan).to_pydict()

    for i in range(plan.m):
        iid = int(table[constants.IMAGE_ID_COL][i])
        prefix_id = upload_images.prefix_id_for(iid, params)
        object_key = upload_images.object_key_for(iid, prefix_id, params)
        # Locators are pure integer math + string templates: must match exactly.
        assert table[constants.PREFIX_ID_COL][i] == prefix_id
        assert table[constants.OBJECT_KEY_COL][i] == object_key
        assert table[constants.URL_COL][i] == upload_images.url_for(object_key, params)
        assert table[constants.ACCOUNT_COL][i] == upload_images.account_for(iid, params)
        assert table[constants.CONTAINER_COL][i] == params.container
        # Sizes use float math: bucket exact, target_bytes within 1 (informational).
        assignment = synthetic_image.target_assignment(
            iid,
            include_large_tail=params.include_large_tail,
            max_bytes=params.max_bytes,
        )
        assert table[constants.TARGET_BUCKET_COL][i] == assignment.bucket
        assert abs(table[constants.TARGET_BYTES_COL][i] - assignment.target) <= 1


def test_schema_field_order_is_fixed() -> None:
    assert build_ref_table.build_schema().names == [
        constants.ROW_INDEX_COL,
        constants.IMAGE_ID_COL,
        constants.EXPANSION_INDEX_COL,
        constants.URL_COL,
        constants.ACCOUNT_COL,
        constants.CONTAINER_COL,
        constants.OBJECT_KEY_COL,
        constants.PREFIX_ID_COL,
        constants.TARGET_BUCKET_COL,
        constants.TARGET_BYTES_COL,
        constants.IMAGE_FORMAT_COL,
    ]


# --- Lance write path -------------------------------------------------------


def test_bootstrap_then_append_roundtrip_2_1(tmp_path: Any, monkeypatch: Any) -> None:
    """Bootstrap (real first fragment) + batch Append on data_storage_version 2.1."""
    import lance
    from lance.fragment import LanceFragment

    seed_uri = _write_seed(tmp_path, object_count=300)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=300,
        rows_per_fragment=100,
        validate_build=False,
    )
    plan = build_ref_table._plan_from_cfg(cfg)

    lance.write_dataset(
        build_ref_table.generate_fragment(0, 100, plan),
        plan.uri,
        schema=plan.schema,
        mode="overwrite",
        data_storage_version=constants.DATA_STORAGE_VERSION,
    )
    ds = lance.dataset(plan.uri)
    metas = []
    for idx in (1, 2):
        reader = pa.RecordBatchReader.from_batches(
            plan.schema,
            build_ref_table.generate_fragment(idx * 100, 100, plan).to_batches(),
        )
        metas.append(
            LanceFragment.create(
                plan.uri,
                reader,
                schema=plan.schema,
                mode="append",
                storage_options={},
                data_storage_version=constants.DATA_STORAGE_VERSION,
            )
        )
    committed = lance.LanceDataset.commit(
        plan.uri, lance.LanceOperation.Append(metas), read_version=ds.version
    )
    assert committed.count_rows() == 300
    assert len(committed.get_fragments()) == 3
    assert committed.data_storage_version == constants.DATA_STORAGE_VERSION


def test_build_ref_table_e2e_local(tmp_path: Any, monkeypatch: Any) -> None:
    """Full driver: spawn pool, bootstrap, batch-commit, validate."""
    import lance

    seed_uri = _write_seed(
        tmp_path, object_count=100, accounts=("a", "b"), prefix_count=8
    )
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=3,
    )
    metrics = build_ref_table.run_build_ref_table(cfg)
    assert metrics["ok"]
    assert metrics["target_rows"] == 1000
    assert metrics["num_fragments"] == 10
    assert metrics["validation"]["derivation_mismatches"] == 0
    assert metrics["validation"]["complete"]
    assert metrics["validation"]["expected_rows"] == 1000

    ds = lance.dataset(cfg.bench_uri)
    assert ds.count_rows() == 1000
    assert len(ds.get_fragments()) == 10
    assert ds.schema.names == build_ref_table.build_schema().names

    table = ds.to_table().to_pydict()
    counts = np.bincount(np.array(table[constants.IMAGE_ID_COL]), minlength=100)
    assert counts.tolist() == [10] * 100

    record = upload_images.read_seed_run(seed_uri, {})
    params = upload_images.params_from_seed_run(record)
    for i in range(0, 1000, 137):
        iid = int(table[constants.IMAGE_ID_COL][i])
        prefix_id = upload_images.prefix_id_for(iid, params)
        object_key = upload_images.object_key_for(iid, prefix_id, params)
        assert table[constants.URL_COL][i] == upload_images.url_for(object_key, params)


def test_build_ref_table_honors_data_storage_version(
    tmp_path: Any, monkeypatch: Any
) -> None:
    """The ref table can opt into newer Lance storage versions."""
    import lance

    seed_uri = _write_seed(tmp_path, object_count=30)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=120,
        rows_per_fragment=40,
        build_workers=2,
        commit_fragments=2,
        data_storage_version="2.2",
        validate_build=False,
    )

    metrics = build_ref_table.run_build_ref_table(cfg)

    ds = lance.dataset(cfg.bench_uri)
    assert metrics["ok"] is True
    assert metrics["data_storage_version"] == "2.2"
    assert ds.data_storage_version == "2.2"
    assert ds.count_rows() == 120


def test_build_ref_table_resume(tmp_path: Any, monkeypatch: Any) -> None:
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=2,
        validate_build=False,
        limit_fragments=5,
    )
    build_ref_table.run_build_ref_table(cfg)
    assert lance.dataset(cfg.bench_uri).count_rows() == 500

    cfg.limit_fragments = None  # resume the rest
    metrics = build_ref_table.run_build_ref_table(cfg)
    assert metrics["start_fragment"] == 5
    assert lance.dataset(cfg.bench_uri).count_rows() == 1000


def test_resume_refuses_non_fragment_aligned_dataset(
    tmp_path: Any, monkeypatch: Any
) -> None:
    # A non-fragment-aligned, incomplete dataset (150 rows, rpf=100) must be refused,
    # not resumed: a floored start_index of 1 would re-append rows [100, 150) and
    # duplicate them. Our own builds never produce this; --overwrite is the escape.
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        validate_build=False,
    )
    plan = build_ref_table._plan_from_cfg(cfg)
    lance.write_dataset(
        build_ref_table.generate_fragment(0, 150, plan),
        cfg.bench_uri,
        schema=plan.schema,
        data_storage_version=constants.DATA_STORAGE_VERSION,
    )
    with pytest.raises(RuntimeError, match="multiple of rows_per_fragment"):
        build_ref_table.run_build_ref_table(cfg)


def test_resume_refuses_data_storage_version_mismatch(
    tmp_path: Any, monkeypatch: Any
) -> None:
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=200,
        rows_per_fragment=100,
        validate_build=False,
    )
    plan = build_ref_table._plan_from_cfg(cfg)
    lance.write_dataset(
        build_ref_table.generate_fragment(0, 100, plan),
        cfg.bench_uri,
        schema=plan.schema,
        data_storage_version="2.0",
    )
    with pytest.raises(RuntimeError, match="data_storage_version"):
        build_ref_table.run_build_ref_table(cfg)


def test_plan_requires_seed_config(tmp_path: Any, monkeypatch: Any) -> None:
    monkeypatch.setattr(benchmark_env, "storage_options_from_env", lambda **_: {})
    cfg = BenchConfig(bench_uri=str(tmp_path / "ref.lance"))
    with pytest.raises(ValueError, match="seed-run-config"):
        build_ref_table._plan_from_cfg(cfg)


# --- Multi-base placement (pure helpers; no infrastructure) -----------------


def test_build_table_bases_az_layout() -> None:
    bases = build_ref_table.build_table_bases(
        output_uri="az://lancedbdatasets/brendan_ref_100m_20260703.lance",
        accounts=["lancetablebase1", "lancetablebase2", "lancetablebase3"],
        prefix="loadtest/table-bases",
    )
    assert [b.name for b in bases] == ["base_1", "base_2", "base_3"]
    assert [b.account for b in bases] == [
        "lancetablebase1",
        "lancetablebase2",
        "lancetablebase3",
    ]
    # Account-qualified abfss URI: the account is in the authority (so Lance routes
    # to it with no base_store_params) AND repeated as a path segment. Container
    # parsed from the output URI; run-id defaults to the output table name.
    assert bases[0].path == (
        "abfss://lancedbdatasets@lancetablebase1.dfs.core.windows.net"
        "/loadtest/table-bases/brendan_ref_100m_20260703/lancetablebase1/base.lance"
    )
    assert bases[2].path == (
        "abfss://lancedbdatasets@lancetablebase3.dfs.core.windows.net"
        "/loadtest/table-bases/brendan_ref_100m_20260703/lancetablebase3/base.lance"
    )


def test_build_table_bases_from_abfss_output_uri() -> None:
    # An abfss:// output URI: container is the authority's filesystem segment.
    bases = build_ref_table.build_table_bases(
        output_uri=(
            "abfss://lancedbdatasets@lanceimagededupe.dfs.core.windows.net/t.lance"
        ),
        accounts=["b1", "b2"],
        prefix="loadtest/table-bases",
        run_id="run9",
    )
    assert bases[0].path == (
        "abfss://lancedbdatasets@b1.dfs.core.windows.net"
        "/loadtest/table-bases/run9/b1/base.lance"
    )


def test_build_table_bases_run_id_and_container_override() -> None:
    bases = build_ref_table.build_table_bases(
        output_uri="az://primary/t.lance",
        accounts=["b1", "b2"],
        prefix="/loadtest/table-bases/",  # leading/trailing slashes tolerated
        run_id="fixed-run-7",
        container="datastore",
    )
    assert bases[0].path == (
        "abfss://datastore@b1.dfs.core.windows.net"
        "/loadtest/table-bases/fixed-run-7/b1/base.lance"
    )
    assert bases[1].path == (
        "abfss://datastore@b2.dfs.core.windows.net"
        "/loadtest/table-bases/fixed-run-7/b2/base.lance"
    )


def test_build_table_bases_empty_when_no_accounts() -> None:
    # Single-base preservation: no accounts -> no base specs at all.
    assert (
        build_ref_table.build_table_bases(
            output_uri="az://c/t.lance", accounts=[], prefix="p"
        )
        == ()
    )


def test_build_table_bases_requires_container_for_schemeless_root() -> None:
    with pytest.raises(ValueError, match="container"):
        build_ref_table.build_table_bases(
            output_uri="az://", accounts=["b1"], prefix="p"
        )


def test_build_table_bases_local_paths(tmp_path: Any) -> None:
    out = str(tmp_path / "ref.lance")
    bases = build_ref_table.build_table_bases(
        output_uri=out, accounts=["baseA", "baseB"], prefix="loadtest/table-bases"
    )
    # Local (schemeless) roots hang off the output table's parent directory.
    assert bases[0].path == str(
        tmp_path / "loadtest" / "table-bases" / "ref" / "baseA" / "base.lance"
    )
    assert "://" not in bases[0].path


def test_table_base_store_params_keyed_by_base_path() -> None:
    # Lance matches base_store_params by the exact base-path URI, NOT base name;
    # keying by name silently falls back to the root account. So the keys must be
    # the base paths (regression guard for that misrouting bug).
    az = build_ref_table.build_table_bases(
        output_uri="az://c/t.lance", accounts=["acct1", "acct2"], prefix="p"
    )
    params = build_ref_table.table_base_store_params(az)
    assert set(params) == {b.path for b in az}
    assert all(p.startswith("abfss://") for p in params)
    assert params[az[0].path] == {
        "account_name": "acct1",
        "azure_storage_account_name": "acct1",
    }
    # Local bases carry no auth options (empty mapping).
    local = build_ref_table.build_table_bases(
        output_uri="/data/ref.lance", accounts=["a", "b"], prefix="p"
    )
    assert build_ref_table.table_base_store_params(local) == {}


def test_canonical_base_store_params_keys_by_manifest_path() -> None:
    # The canonical map must key by the manifest's STORED base path (matched to
    # specs by name), so any path normalization Lance applies can't reintroduce
    # the name-vs-path key miss that silently routes to the root account.
    from types import SimpleNamespace

    specs = build_ref_table.build_table_bases(
        output_uri="az://c/t.lance", accounts=["acctX", "acctY"], prefix="p"
    )
    dataset = SimpleNamespace(
        _ds=SimpleNamespace(
            base_paths=lambda: {
                1: SimpleNamespace(
                    name="base_1", path=specs[0].path + "/", is_dataset_root=False
                ),
                2: SimpleNamespace(
                    name="base_2", path=specs[1].path, is_dataset_root=False
                ),
                0: SimpleNamespace(
                    name=None, path="az://c/t.lance", is_dataset_root=True
                ),
            }
        )
    )
    params = build_ref_table._canonical_base_store_params(dataset, specs)
    # keyed by the manifest path (incl. the normalized trailing slash), root excluded
    assert params == {
        specs[0].path + "/": {
            "account_name": "acctX",
            "azure_storage_account_name": "acctX",
        },
        specs[1].path: {
            "account_name": "acctY",
            "azure_storage_account_name": "acctY",
        },
    }


def test_base_name_for_fragment_round_robin() -> None:
    names = [build_ref_table.base_name_for_fragment(i, 3) for i in range(7)]
    assert names == [
        "base_1",
        "base_2",
        "base_3",
        "base_1",
        "base_2",
        "base_3",
        "base_1",
    ]
    # Fragment 0 always lands on base_1 (matches the bootstrap target).
    assert build_ref_table.base_name_for_fragment(0, 25) == "base_1"


def test_default_table_base_run_id() -> None:
    assert (
        build_ref_table.default_table_base_run_id("az://c/my_ref_100m.lance")
        == "my_ref_100m"
    )
    assert build_ref_table.default_table_base_run_id("/data/x/ref.lance") == "ref"


# --- Multi-base config parsing / validation ---------------------------------


def test_cli_parses_table_base_flags() -> None:
    from loadtest.azure_scale_bench import run

    args = run.build_parser().parse_args(
        [
            "build-ref-table",
            "--output-uri",
            "az://c/t.lance",
            "--table-base-accounts",
            "lancetablebase1,lancetablebase2",
            "--table-base-prefix",
            "custom/bases",
            "--table-base-run-id",
            "run-9",
        ]
    )
    assert args.table_base_accounts == "lancetablebase1,lancetablebase2"
    assert args.table_base_prefix == "custom/bases"
    assert args.table_base_run_id == "run-9"
    # The comma-string is normalized to a tuple by the field converter.
    cfg = BenchConfig(table_base_accounts=args.table_base_accounts)
    assert cfg.table_base_accounts == ("lancetablebase1", "lancetablebase2")


def test_config_rejects_duplicate_table_base_accounts() -> None:
    cfg = BenchConfig(table_base_accounts="a,b,a")
    with pytest.raises(ValueError, match="unique"):
        cfg.validate()


def test_config_rejects_bad_table_base_run_id() -> None:
    cfg = BenchConfig(table_base_accounts="a,b", table_base_run_id="bad/id")
    with pytest.raises(ValueError, match="table_base_run_id"):
        cfg.validate()


# --- Multi-base Lance write path (end-to-end, local filesystem) -------------


def test_build_ref_table_multibase_e2e_local(tmp_path: Any, monkeypatch: Any) -> None:
    """Full driver in multi-base mode: fragments spread round-robin across bases."""
    import lance

    seed_uri = _write_seed(
        tmp_path, object_count=100, accounts=("a", "b"), prefix_count=8
    )
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=3,
        table_base_accounts=("baseA", "baseB", "baseC"),
    )
    metrics = build_ref_table.run_build_ref_table(cfg)

    assert metrics["ok"]
    assert metrics["num_fragments"] == 10
    assert metrics["multi_base"]["base_count"] == 3
    assert metrics["multi_base"]["accounts"] == ["baseA", "baseB", "baseC"]

    placement = metrics["validation"]["base_distribution"]
    assert placement["ok"]
    # Fragment 0 bootstraps root; the remaining 9 fragments distribute evenly.
    assert placement["distribution"] == {
        "base_1": 3,
        "base_2": 3,
        "base_3": 3,
        "root": 1,
    }
    assert placement["expected_bases"] == ["base_1", "base_2", "base_3", "root"]
    assert placement["unexpected_bases"] == []
    assert placement["missing_bases"] == []

    # Apart from the one durable-root bootstrap fragment, data lands in the
    # per-account base datasets.
    for account in ("baseA", "baseB", "baseC"):
        base_dir = (
            tmp_path / "loadtest" / "table-bases" / "ref" / account / "base.lance"
        )
        assert base_dir.exists()

    ds = lance.dataset(cfg.bench_uri)
    assert ds.count_rows() == 1000
    assert len(ds.get_fragments()) == 10
    # Fragment 0 is the primary/root bootstrap; all later fragments have a base id.
    base_ids = {
        getattr(df, "base_id", 0)
        for frag in ds.get_fragments()
        for df in frag.data_files()
    }
    assert base_ids & {0, None}
    assert len(base_ids - {0, None}) == 3


def test_build_ref_table_multibase_fewer_fragments_than_bases(
    tmp_path: Any, monkeypatch: Any
) -> None:
    """With fewer fragments than bases, only the leading prefix of bases is used."""
    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=200,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=5,
        table_base_accounts=("b1", "b2", "b3", "b4", "b5"),
    )
    metrics = build_ref_table.run_build_ref_table(cfg)
    assert metrics["ok"]
    assert metrics["num_fragments"] == 2
    placement = metrics["validation"]["base_distribution"]
    assert placement["ok"]
    assert placement["distribution"] == {"base_1": 1, "root": 1}
    assert placement["expected_bases"] == ["base_1", "root"]


def test_build_ref_table_multibase_resume(tmp_path: Any, monkeypatch: Any) -> None:
    """Resume a multi-base build: later fragments still route to their target base."""
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=2,
        validate_build=False,
        limit_fragments=5,
        table_base_accounts=("baseA", "baseB", "baseC"),
    )
    build_ref_table.run_build_ref_table(cfg)
    assert lance.dataset(cfg.bench_uri).count_rows() == 500

    cfg.limit_fragments = None  # resume the rest
    cfg.validate_build = True
    metrics = build_ref_table.run_build_ref_table(cfg)
    assert metrics["start_fragment"] == 5
    assert metrics["ok"]
    assert lance.dataset(cfg.bench_uri).count_rows() == 1000
    assert metrics["validation"]["base_distribution"]["ok"]
    assert metrics["validation"]["base_distribution"]["distribution"] == {
        "base_1": 3,
        "base_2": 3,
        "base_3": 3,
        "root": 1,
    }


def test_config_rejects_empty_table_base_run_id() -> None:
    cfg = BenchConfig(table_base_accounts="a,b", table_base_run_id="")
    with pytest.raises(ValueError, match="non-empty"):
        cfg.validate()


def test_resume_refuses_single_to_multi(tmp_path: Any, monkeypatch: Any) -> None:
    """A single-base table cannot be resumed into multi-base (bases unregistered)."""
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=2,
        validate_build=False,
        limit_fragments=5,
    )
    build_ref_table.run_build_ref_table(cfg)  # single-base, 500 rows committed
    assert lance.dataset(cfg.bench_uri).count_rows() == 500

    cfg.limit_fragments = None
    cfg.table_base_accounts = ("baseA", "baseB", "baseC")
    with pytest.raises(RuntimeError, match="single-base"):
        build_ref_table.run_build_ref_table(cfg)


def test_resume_refuses_multi_to_single(tmp_path: Any, monkeypatch: Any) -> None:
    """A multi-base table cannot be silently resumed single-base (mixed placement)."""
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=2,
        validate_build=False,
        limit_fragments=5,
        table_base_accounts=("baseA", "baseB", "baseC"),
    )
    build_ref_table.run_build_ref_table(cfg)  # multi-base, 500 rows across bases
    assert lance.dataset(cfg.bench_uri).count_rows() == 500

    cfg.limit_fragments = None
    cfg.table_base_accounts = ()  # operator forgot the flag on resume
    with pytest.raises(RuntimeError, match="multi-base"):
        build_ref_table.run_build_ref_table(cfg)


def test_resume_refuses_reordered_table_base_accounts(
    tmp_path: Any, monkeypatch: Any
) -> None:
    """Reordering accounts on resume must be refused (name->account binding drift)."""
    import lance

    seed_uri = _write_seed(tmp_path, object_count=100)
    cfg = _local_cfg(
        monkeypatch,
        tmp_path,
        seed_uri,
        target_rows=1000,
        rows_per_fragment=100,
        build_workers=2,
        commit_fragments=2,
        validate_build=False,
        limit_fragments=5,
        table_base_accounts=("baseA", "baseB", "baseC"),
    )
    build_ref_table.run_build_ref_table(cfg)
    assert lance.dataset(cfg.bench_uri).count_rows() == 500

    cfg.limit_fragments = None
    cfg.table_base_accounts = ("baseC", "baseB", "baseA")  # same set, reordered
    with pytest.raises(RuntimeError, match="do not match"):
        build_ref_table.run_build_ref_table(cfg)


if __name__ == "__main__":  # pragma: no cover - convenience for manual runs
    raise SystemExit(pytest.main([__file__, "-v"]))
