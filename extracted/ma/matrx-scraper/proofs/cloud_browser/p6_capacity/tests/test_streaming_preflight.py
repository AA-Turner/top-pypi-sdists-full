from __future__ import annotations

from types import SimpleNamespace

from harness.workloads import streaming


def test_container_image_requires_explicit_benchmark_contract(monkeypatch):
    monkeypatch.setattr(streaming.shutil, "which", lambda binary: f"/usr/bin/{binary}")
    monkeypatch.delenv("P6_IMAGE_BENCHMARK_CONTRACT", raising=False)
    ctx = SimpleNamespace(selkies_image="production-browser-worker:latest")

    mode, reasons = streaming._stream_plane(ctx)

    assert mode == "none"
    assert "P6_IMAGE_BENCHMARK_CONTRACT=1 is not" in reasons[0]
    assert "Refusing a misleading capacity run" in reasons[0]


def test_container_image_with_declared_contract_is_accepted(monkeypatch):
    monkeypatch.setattr(streaming.shutil, "which", lambda binary: f"/usr/bin/{binary}")
    monkeypatch.setenv("P6_IMAGE_BENCHMARK_CONTRACT", "1")
    ctx = SimpleNamespace(selkies_image="benchmark-browser-worker:latest")

    assert streaming._stream_plane(ctx) == ("selkies", [])


def test_production_image_unit_explicitly_selects_benchmark_entrypoint(tmp_path):
    ctx = SimpleNamespace(
        base_url="http://127.0.0.1:8642",
        unit_duration_s=30,
        stream_fps=30,
        stream_bitrate="4M",
    )

    spec = streaming._selkies_unit(ctx, "w4_stream_1080p", "unit-1", "matrx-browser-worker:test")

    assert "P6_BENCHMARK_MODE=1" in spec.argv
    assert "BROWSER_WORKER_WIDTH=1920" in spec.argv
    assert "BROWSER_WORKER_HEIGHT=1080" in spec.argv
