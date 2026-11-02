"""Documented All Combined benchmarks; no native or cloud imports."""

from dataclasses import dataclass

REVISION = "735138876887eb64650742631b8dda841dd264bf"  # upstream v0.2.9


@dataclass(frozen=True)
class MolmoBenchmark:
    path: str
    horizon_s: int
    renderer: str = "classic"
    cameras: tuple[str, str] | None = None


_V1 = "molmospaces-bench-v1/ithor"
_V2 = "molmospaces-bench-v2"
_HARD = f"{_V2}/procthor-objaverse"
_PICK = f"{_HARD}/FrankaPickHardBench/FrankaPickHardBench_20260206_json_benchmark"
BENCHMARKS = {
    "open-v1": MolmoBenchmark(
        f"{_V1}/FrankaOpenDataGenConfig/FrankaOpenDataGenConfig_20260123_json_benchmark", 30
    ),
    "close-v1": MolmoBenchmark(
        f"{_V1}/FrankaCloseDataGenConfig/FrankaCloseDataGenConfig_20260123_json_benchmark", 30
    ),
    "pick-v1.5": MolmoBenchmark(
        f"{_V2}/procthor-10k/FrankaPickDroidMiniBench/"
        "FrankaPickDroidMiniBench_json_benchmark_20251231",
        30,
    ),
    "pick-v2-classic": MolmoBenchmark(_PICK, 20),
    "pick-v2-filament": MolmoBenchmark(_PICK, 20, "filament"),
    "pick-v2-rand-cam": MolmoBenchmark(
        _PICK, 20, "filament", ("randomized_zed2_analogue_1", "wrist_camera_zed_mini")
    ),
    "pnp-v2": MolmoBenchmark(
        f"{_HARD}/FrankaPickandPlaceHardBench/FrankaPickandPlaceHardBench_20260206_json_benchmark",
        40,
        "filament",
    ),
    "pnp-next-to-v2": MolmoBenchmark(
        f"{_HARD}/FrankaPickandPlaceNextToHardBench/"
        "FrankaPickandPlaceNextToHardBench_20260305_json_benchmark",
        40,
        "filament",
    ),
    "pnp-color-v2": MolmoBenchmark(
        f"{_HARD}/FrankaPickandPlaceColorHardBench/"
        "FrankaPickandPlaceColorHardBench_20260304_json_benchmark",
        40,
        "filament",
    ),
}


def selected_suites(suite: str) -> tuple[str, ...]:
    value = suite.lower()
    if value == "all":
        return tuple(BENCHMARKS)
    if value not in BENCHMARKS:
        raise ValueError(f"MolmoSpaces --task-suite must be all or {', '.join(BENCHMARKS)}.")
    return (value,)


def episode_selection(value: str | int) -> int | str:
    if value == "all":
        return "all"
    if isinstance(value, bool):
        raise ValueError("MolmoSpaces --task-id must be a nonnegative episode index or all.")
    try:
        index = int(value)
    except (ValueError, TypeError) as exc:
        raise ValueError(
            "MolmoSpaces --task-id must be a nonnegative episode index or all."
        ) from exc
    if index < 0 or str(value) != str(index):
        raise ValueError("MolmoSpaces --task-id must be a nonnegative episode index or all.")
    return index
