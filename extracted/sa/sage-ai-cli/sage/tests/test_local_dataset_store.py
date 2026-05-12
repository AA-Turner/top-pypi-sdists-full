"""Tests for LocalDatasetStore — third-party-independent dataset access.

After datasets are mirrored to disk, the fine-tune flow loads them from
LocalDatasetStore so training has no runtime dependency on HuggingFace
or GCS. This module verifies that contract.
"""

from __future__ import annotations

import json
from pathlib import Path

import pytest


class TestLocalDatasetStorePresence:

    def test_empty_root_reports_no_datasets(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        store = LocalDatasetStore(root=tmp_path / "datasets")
        assert store.available() == []

    def test_directory_without_normalized_jsonl_skipped(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        d = tmp_path / "datasets" / "bogus"
        d.mkdir(parents=True)
        (d / "README.md").write_text("not a dataset file")
        store = LocalDatasetStore(root=tmp_path / "datasets")
        assert "bogus" not in store.available()

    def test_present_dataset_appears(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        d = tmp_path / "datasets" / "humaneval"
        d.mkdir(parents=True)
        (d / "normalized.jsonl").write_text(
            json.dumps({"instruction": "q", "output": "a"}) + "\n"
        )
        store = LocalDatasetStore(root=tmp_path / "datasets")
        assert "humaneval" in store.available()
        assert store.is_present("humaneval") is True


class TestLocalDatasetStoreIteration:

    def test_iter_examples_yields_records(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        d = tmp_path / "datasets" / "tiny"
        d.mkdir(parents=True)
        (d / "normalized.jsonl").write_text(
            json.dumps({"instruction": "q1", "output": "a1"}) + "\n"
            + json.dumps({"instruction": "q2", "output": "a2"}) + "\n"
        )
        store = LocalDatasetStore(root=tmp_path / "datasets")
        examples = list(store.iter_examples("tiny"))
        assert len(examples) == 2
        assert examples[0]["instruction"] == "q1"
        assert examples[1]["output"] == "a2"

    def test_iter_examples_skips_blank_and_malformed(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        d = tmp_path / "datasets" / "mixed"
        d.mkdir(parents=True)
        (d / "normalized.jsonl").write_text(
            json.dumps({"i": 1}) + "\n"
            + "\n"  # blank line
            + "not valid json\n"  # malformed
            + json.dumps({"i": 2}) + "\n"
        )
        store = LocalDatasetStore(root=tmp_path / "datasets")
        examples = list(store.iter_examples("mixed"))
        assert len(examples) == 2

    def test_count_examples_matches_iter(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        d = tmp_path / "datasets" / "tiny"
        d.mkdir(parents=True)
        (d / "normalized.jsonl").write_text(
            "\n".join([json.dumps({"i": i}) for i in range(7)]) + "\n"
        )
        store = LocalDatasetStore(root=tmp_path / "datasets")
        assert store.count_examples("tiny") == 7


class TestLocalDatasetStoreSummary:

    def test_summary_aggregates_across_datasets(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        for name, count in [("a", 3), ("b", 5)]:
            d = tmp_path / "datasets" / name
            d.mkdir(parents=True)
            (d / "normalized.jsonl").write_text(
                "\n".join([json.dumps({"x": i}) for i in range(count)]) + "\n"
            )
        store = LocalDatasetStore(root=tmp_path / "datasets")
        summary = store.summary()
        assert summary["total_examples"] == 8
        assert len(summary["datasets"]) == 2
        assert summary["total_size_bytes"] > 0

    def test_summary_handles_empty_root(self, tmp_path):
        from sage.training.datasets import LocalDatasetStore
        store = LocalDatasetStore(root=tmp_path / "empty")
        summary = store.summary()
        assert summary["total_examples"] == 0
        assert summary["datasets"] == []


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
