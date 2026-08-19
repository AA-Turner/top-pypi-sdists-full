# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors
"""Tests for YAML profile loading, application, guards, and precedence."""

from __future__ import annotations

import argparse
import textwrap
from typing import TYPE_CHECKING

import pytest

from loadtest.azure_scale_bench import profiles
from loadtest.azure_scale_bench.benchmark_env import BenchConfig

if TYPE_CHECKING:
    from pathlib import Path


def test_apply_dataset_and_scale() -> None:
    cfg = BenchConfig()
    profs = {
        "datasets": {
            "5b": {
                "source_uri": "az://d/5b.lance",
                "bench_uri": "az://d/5b_bench.lance",
                "expected_rows": 5_000_000_000,
            }
        },
        "scales": {"big": {"concurrency": 1800, "num_nodes": 100, "num_cpus": 3600}},
    }
    profiles.apply_profile(cfg, profs, dataset="5b", scale="big")
    assert cfg.source_uri.endswith("5b.lance")
    assert cfg.bench_uri.endswith("5b_bench.lance")
    assert cfg.expected_rows == 5_000_000_000
    assert cfg.concurrency == 1800
    assert cfg.num_nodes == 100
    assert cfg.num_cpus == 3600


def test_unknown_dataset_and_scale_error() -> None:
    with pytest.raises(ValueError, match="unknown dataset"):
        profiles.apply_profile(BenchConfig(), {"datasets": {}}, dataset="nope")
    with pytest.raises(ValueError, match="unknown scale"):
        profiles.apply_profile(BenchConfig(), {"scales": {}}, scale="nope")


def test_unknown_key_rejected() -> None:
    with pytest.raises(ValueError, match="unknown profile key"):
        profiles.apply_profile(
            BenchConfig(), {"datasets": {"d": {"bogus": 1}}}, dataset="d"
        )


def test_account_key_rejected() -> None:
    with pytest.raises(ValueError, match="account_key"):
        profiles.apply_profile(
            BenchConfig(), {"datasets": {"d": {"account_key": "secret"}}}, dataset="d"
        )


def test_load_profiles_default_has_50b_and_scales() -> None:
    profs = profiles.load_profiles()
    assert "50b" in profs["datasets"]
    assert {"local", "10n", "100n", "1000n"} <= set(profs["scales"])


def test_load_profiles_from_path(tmp_path: Path) -> None:
    path = tmp_path / "p.yaml"
    path.write_text(
        textwrap.dedent("""
            datasets: {d: {source_uri: az://x.lance}}
            scales: {s: {concurrency: 4}}
        """)
    )
    profs = profiles.load_profiles(path)
    assert profs["datasets"]["d"]["source_uri"] == "az://x.lance"


def test_profile_null_clears_a_value() -> None:
    # A profile overlays only the keys it lists; an explicit null clears a value
    # that env/default set (so a stray BENCH_CLUSTER can't bleed into --scale local).
    cfg = BenchConfig(cluster="stale-cluster", concurrency=8)
    profiles.apply_profile(
        cfg, {"scales": {"local": {"cluster": None, "concurrency": 2}}}, scale="local"
    )
    assert cfg.cluster is None
    assert cfg.concurrency == 2


def test_builtin_local_scale_nulls_cluster() -> None:
    cfg = BenchConfig(cluster="stale-cluster")
    profiles.apply_profile(cfg, profiles.load_profiles(), scale="local")
    assert cfg.cluster is None
    assert cfg.manifest is None


def test_precedence_flag_beats_profile_beats_default() -> None:
    profs = {"scales": {"s": {"concurrency": 1800}}}
    cfg = BenchConfig()  # default concurrency = 8
    profiles.apply_profile(cfg, profs, scale="s")
    assert cfg.concurrency == 1800  # profile beats default

    cfg._overlay_args(argparse.Namespace(concurrency=None))
    assert cfg.concurrency == 1800  # profile survives when the flag is absent

    cfg._overlay_args(argparse.Namespace(concurrency=99))
    assert cfg.concurrency == 99  # an explicit flag wins


def test_apply_upload_keys() -> None:
    # Upload-job keys overlay from a profile; the accounts list is coerced to a tuple.
    cfg = BenchConfig()
    profs = {
        "datasets": {
            "d": {
                "accounts": ["acctA", "acctB"],
                "loose_container": "cont",
                "base_prefix": "pre",
                "prefix_count": 4096,
                "seed_rows_per_fragment": 50_000,
            }
        }
    }
    profiles.apply_profile(cfg, profs, dataset="d")
    assert cfg.accounts == ("acctA", "acctB")
    assert cfg.loose_container == "cont"
    assert cfg.base_prefix == "pre"
    assert cfg.prefix_count == 4096
    assert cfg.seed_rows_per_fragment == 50_000
