from __future__ import annotations

from pathlib import Path
from types import SimpleNamespace

from matrx_scraper.cloud_browser.worker.p6_benchmark import (
    BenchmarkConfig,
    _bitrate_kbps,
    run_benchmark,
)


class _Page:
    html = ""

    async def set_content(self, value: str) -> None:
        self.html = value


class _Worker:
    active_page_id = "page-1"
    page = _Page()

    def page_object(self, _page_id: str):
        return self.page


class _Control:
    def __init__(self) -> None:
        self.commands = 0
        self.shutdown_reason = None

    async def bootstrap(self, **_kwargs):
        return SimpleNamespace(ok=True, error=None)

    async def command(self, _command):
        self.commands += 1
        return SimpleNamespace(ok=True, error=None)

    async def heartbeat(self, **_kwargs):
        return SimpleNamespace(ok=True)

    async def shutdown(self, *, reason: str):
        self.shutdown_reason = reason
        return SimpleNamespace(ok=True)


class _Supervisor:
    started = False
    stopped = False

    def start(self) -> None:
        self.started = True

    def stop(self) -> None:
        self.stopped = True


class _CpuMeter:
    def sample(self) -> float:
        return 12.5


async def test_opt_in_contract_drives_real_runtime_seams_and_emits_jsonl_events(
    tmp_path: Path,
) -> None:
    worker = _Worker()
    control = _Control()
    supervisor = _Supervisor()
    events = []
    config = BenchmarkConfig(
        base_url="http://capacity.test",
        duration_s=0.02,
        action_interval_s=0.001,
        display=":99",
        width=1920,
        height=1080,
        profile_dir=tmp_path / "profile",
        requested_fps=30,
        requested_bitrate="4M",
    )

    result = await run_benchmark(
        config,
        worker=worker,  # type: ignore[arg-type]
        control=control,  # type: ignore[arg-type]
        supervisor=supervisor,  # type: ignore[arg-type]
        cpu_meter=_CpuMeter(),  # type: ignore[arg-type]
        emit=lambda **event: events.append(event),
    )

    assert result == 0
    assert control.commands > 0
    assert control.shutdown_reason == "operator"
    assert supervisor.started and supervisor.stopped
    assert "http://capacity.test" in worker.page.html
    kinds = {event["ev"] for event in events}
    assert {"ready", "action", "encoder", "done"} <= kinds
    assert next(event for event in events if event["ev"] == "encoder") == {
        "ev": "encoder",
        "utilisation_pct": 12.5,
        "source": "container_cpu_x264",
    }


def test_bitrate_contract_converts_human_units_to_selkies_kbps() -> None:
    assert _bitrate_kbps("4M") == "4000"
    assert _bitrate_kbps("750K") == "750"
    assert _bitrate_kbps("1200") == "1200"
