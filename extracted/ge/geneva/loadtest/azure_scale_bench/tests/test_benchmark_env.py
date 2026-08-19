# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for storage_options auth flexibility and BenchConfig validation."""

from __future__ import annotations

import lance
import pyarrow as pa
import pytest

from loadtest.azure_scale_bench import benchmark_env
from loadtest.azure_scale_bench.benchmark_env import ACCOUNT_KEY_ENV, BenchConfig


def test_storage_options_name_only_without_key(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.delenv(ACCOUNT_KEY_ENV, raising=False)
    cfg = BenchConfig(account_name="acct", account_key=None)
    # No key available anywhere → name-only options, no error (WI/public path).
    # Both the plain and object-store canonical name keys are emitted.
    assert cfg.storage_options == {
        "account_name": "acct",
        "azure_storage_account_name": "acct",
    }


def test_storage_options_honors_explicit_key(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.delenv(ACCOUNT_KEY_ENV, raising=False)
    cfg = BenchConfig(account_name="acct", account_key="secret")
    assert cfg.storage_options == {
        "account_name": "acct",
        "azure_storage_account_name": "acct",
        "account_key": "secret",
    }


def test_storage_options_env_key_fallback(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv(ACCOUNT_KEY_ENV, "envkey")
    cfg = BenchConfig(account_name="acct", account_key=None)
    assert cfg.storage_options == {
        "account_name": "acct",
        "azure_storage_account_name": "acct",
        "account_key": "envkey",
    }


def test_validate_rejects_bad_image_mode() -> None:
    with pytest.raises(ValueError, match="image_mode"):
        BenchConfig(image_mode="decode_realistic").validate()


def test_validate_rejects_bad_image_format() -> None:
    with pytest.raises(ValueError, match="image_format"):
        BenchConfig(image_format="gif").validate()


@pytest.mark.parametrize("fmt", ["png", "PNG", "jpeg", "jpg"])
def test_validate_accepts_supported_formats(fmt: str) -> None:
    BenchConfig(image_format=fmt).validate()  # must not raise


def test_validate_rejects_overwrite_and_reuse_together() -> None:
    with pytest.raises(ValueError, match="mutually exclusive"):
        BenchConfig(overwrite=True, reuse_existing=True).validate()


def test_validate_rejects_bad_suffix() -> None:
    with pytest.raises(ValueError, match="suffix"):
        BenchConfig(suffix="bad-suffix").validate()


def test_table_exists_sees_past_the_table_names_page_limit(tmp_path) -> None:  # noqa: ANN001
    """conn.table_names() returns one 10-table page; the physical check must not.

    Regression: existence gates built on table_names() silently missed tables in
    a container holding more than the page limit.
    """
    db_uri = str(tmp_path)
    names = [f"t{i:02d}" for i in range(14)]
    for name in names:
        lance.write_dataset(pa.table({"id": [1]}), f"{db_uri}/{name}.lance")

    # every table is found, including those past the first page
    assert all(benchmark_env.table_exists(db_uri, n, {}) for n in names)
    assert not benchmark_env.table_exists(db_uri, "absent", {})


def test_validate_rejects_unsupported_data_storage_version() -> None:
    """An unwritable version must fail here, not partway through a build."""
    with pytest.raises(ValueError, match="data_storage_version"):
        BenchConfig(data_storage_version="2.9").validate()


@pytest.mark.parametrize("version", ["2.1", "2.2", "stable"])
def test_validate_accepts_supported_data_storage_versions(version: str) -> None:
    BenchConfig(data_storage_version=version).validate()  # must not raise


@pytest.mark.parametrize(
    "kwargs",
    [
        {"target_partition_size": 0},
        {"norm_size": 0},
        {"hamming_threshold": -1},
        {"dup_bit_flips": -1},
        {"decode_sample_count": 0},
        {"num_frags": 0},
        {"skip_frags": -1},
        {"object_count": 0},
        {"prefix_count": 0},
        {"seed_rows_per_fragment": 0},
        {"seed_rows_per_fragment": 2_000_000},  # above Lance's per-file cap
        {"delete_after_months": 0},  # below the 6-month lifecycle floor
        {"max_bucket_miss_rate": 1.5},
        {"shuffle_salt": -1},
        {"max_in_flight": 0},
        {"driver_rows_per_fragment": 0},
        {"driver_rows_per_fragment": 2_000_000},  # above Lance's per-file cap
        {"per_actor_cpus": 0},
        {"per_actor_cpus": -1},
    ],
)
def test_validate_rejects_bad_numeric_knobs(kwargs: dict) -> None:
    with pytest.raises(ValueError, match="must be|exceeds"):
        BenchConfig(**kwargs).validate()


def test_validate_accepts_unset_per_actor_cpus() -> None:
    BenchConfig().validate()  # None default must not raise
    BenchConfig(per_actor_cpus=4).validate()  # must not raise


def test_per_actor_cpus_from_env(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.setenv("BENCH_PER_ACTOR_CPUS", "4")
    assert BenchConfig.from_env_and_args().per_actor_cpus == 4.0


def test_per_actor_cpus_defaults_none(monkeypatch) -> None:  # noqa: ANN001
    monkeypatch.delenv("BENCH_PER_ACTOR_CPUS", raising=False)
    assert BenchConfig.from_env_and_args().per_actor_cpus is None


@pytest.mark.parametrize("bad", ["bad/id", "has space", "..", ""])
def test_validate_rejects_bad_seed_run_id(bad: str) -> None:
    with pytest.raises(ValueError, match="seed_run_id"):
        BenchConfig(seed_run_id=bad).validate()


def test_validate_accepts_good_seed_run_id() -> None:
    BenchConfig(seed_run_id="run-1_dry").validate()  # must not raise


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        ("a,b,c", ("a", "b", "c")),
        ("a, b ,c", ("a", "b", "c")),
        (["x", "y"], ("x", "y")),
        (None, ()),
        ("", ()),
    ],
)
def test_accounts_coerced_to_tuple(value: object, expected: tuple) -> None:
    assert BenchConfig(accounts=value).accounts == expected
