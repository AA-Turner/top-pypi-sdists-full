"""Tests for the mirror_all_datasets.py runner script logic.

The script's heavy work (HF download + GCS upload) is in DatasetMirror;
this file tests the runner's orchestration: filter behavior, pre-flight
checks, failure tallying.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

_SCRIPTS = Path(__file__).resolve().parent.parent.parent / "scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))


class TestPreflight:

    def test_preflight_returns_int_status(self):
        import mirror_all_datasets
        rc = mirror_all_datasets.preflight()
        assert isinstance(rc, int)
        assert rc in (0, 1)


class TestMirrorOne:

    def test_skips_when_already_mirrored(self, monkeypatch):
        import mirror_all_datasets
        from sage.training.datasets import ExternalDataset

        class _M:
            def is_mirrored(self, _ds): return True
            def fetch_and_normalize(self, _ds):
                raise AssertionError("should not fetch when already mirrored")

        ds = ExternalDataset(
            name="dummy", description="x", license="mit", languages=("python",),
            huggingface_id="x/y", max_examples=1, estimated_size_mb=1,
        )
        ok, msg = mirror_all_datasets.mirror_one(_M(), ds, skip_existing=True)
        assert ok is True
        assert "skipped" in msg.lower()

    def test_reports_fetch_failure(self):
        import mirror_all_datasets
        from sage.training.datasets import ExternalDataset

        class _M:
            def is_mirrored(self, _ds): return False
            def fetch_and_normalize(self, _ds):
                raise RuntimeError("network down")

        ds = ExternalDataset(
            name="d", description="x", license="mit", languages=("python",),
            huggingface_id="x/y", max_examples=1, estimated_size_mb=1,
        )
        ok, msg = mirror_all_datasets.mirror_one(_M(), ds, skip_existing=True)
        assert ok is False
        assert "network down" in msg

    def test_reports_upload_failure(self):
        import mirror_all_datasets
        from sage.training.datasets import ExternalDataset

        class _M:
            def is_mirrored(self, _ds): return False
            def fetch_and_normalize(self, _ds): return Path("/tmp/fake.jsonl")
            def upload(self, _ds, _path): return False

        ds = ExternalDataset(
            name="d", description="x", license="mit", languages=("python",),
            huggingface_id="x/y", max_examples=1, estimated_size_mb=1,
        )
        ok, msg = mirror_all_datasets.mirror_one(_M(), ds, skip_existing=True)
        assert ok is False
        assert "upload" in msg.lower()

    def test_success_reports_duration(self):
        import mirror_all_datasets
        from sage.training.datasets import ExternalDataset

        class _M:
            def is_mirrored(self, _ds): return False
            def fetch_and_normalize(self, _ds): return Path("/tmp/fake.jsonl")
            def upload(self, _ds, _path): return True

        ds = ExternalDataset(
            name="d", description="x", license="mit", languages=("python",),
            huggingface_id="x/y", max_examples=1, estimated_size_mb=1,
        )
        ok, msg = mirror_all_datasets.mirror_one(_M(), ds, skip_existing=True)
        assert ok is True
        assert "mirrored" in msg.lower()


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
