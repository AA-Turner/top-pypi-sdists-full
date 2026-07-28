"""Local HDF5 fixtures for the GUI data tutorial."""

from __future__ import annotations

import shutil
from collections.abc import Callable
from pathlib import Path
from typing import Any

import tidy3d as td

DATA_DIR = Path(__file__).with_name("gui_data_tutorial_mock_data")

SIMULATION_DATA_TASK_IDS = (
    "sw-5f2a3905-a835-46ea-9a5b-b33923925b454",
    "sw-a05473ab-f17e-4b03-a6c4-53ae3df47f211",
    "sw-9494afda-cb41-4c85-815f-a767d86a20805",
    "sw-7126922d-64cd-4366-b6fe-1dde9055b4b63",
    "sw-a07f0f54-b5f6-4b4b-804b-f5f8b8b3a6940",
    "sw-b0d69553-4621-43cc-9f7c-6a4bd856f7c32",
    "sw-8738b266-4733-48da-aa13-11b4397872bf1",
    "sw-e490dc15-217f-49b3-a4f5-0675c92d85b80",
    "sw-b91352e9-fb81-4880-9394-3399fa724fc13",
    "sw-f48edeeb-5372-4bfb-acbf-c7f3199d0fc52",
)

MODE_SOLVER_DATA_TASK_IDS = (
    "sw-db60f8aa-3196-4361-b694-48f6100a4b474",
    "sw-3340fb2a-9627-40f0-a1d0-b5d67128f78914",
    "sw-8e22ae40-3b92-4221-9bf6-25c9104cd8ec11",
    "sw-608fd3e1-ad5c-41ca-a382-247268204ffb3",
    "sw-809cc1e1-0fd5-4f44-8454-fc1aea75df2e1",
    "sw-0fb58701-c820-4090-a309-ebbda46a86ca12",
    "sw-6dc7d32b-7ab6-49c3-8f64-168c9a54c8127",
    "sw-82abae19-4978-47ee-aac8-cb8da40c9e5e13",
    "sw-6d84d662-542c-46b6-91a6-718f84c12de12",
    "sw-5402252e-ccf1-46c1-8a89-789f18cffbe910",
    "sw-dc16e0a9-26c1-4e75-9564-36e6c7bdb05415",
    "sw-3b550f02-3fa4-46d2-9a75-8f0aec1a3a5e6",
    "sw-36823176-e570-4ebc-b339-f20ef0ef4b525",
    "sw-d5bc6181-9e34-4212-a665-87c7be630e718",
    "sw-723945f8-b3c0-4af6-a902-f204895bdc839",
    "sw-0c6e28fa-c2bd-49a7-aca9-cb1946b27f210",
)

SIMULATION_DATA_FIXTURES = {task_id: f"{task_id}.hdf5" for task_id in SIMULATION_DATA_TASK_IDS}
MODE_SOLVER_DATA_FIXTURES = {task_id: f"{task_id}.hdf5" for task_id in MODE_SOLVER_DATA_TASK_IDS}
_ORIGINAL_WEB_LOAD: Any | None = None


def register_web_load_mock() -> None:
    """Serve known GUI tutorial task IDs from local HDF5 files."""
    import tidy3d.web as web

    global _ORIGINAL_WEB_LOAD
    if getattr(web.load, "_gui_data_tutorial_mock", False):
        return

    _ORIGINAL_WEB_LOAD = web.load

    def load(
        task_id: str,
        path: str | Path | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> Any:
        if task_id in SIMULATION_DATA_FIXTURES:
            return _load_fixture(
                task_id=task_id,
                path=path,
                loader=td.SimulationData.from_file,
                fixtures=SIMULATION_DATA_FIXTURES,
            )
        if task_id in MODE_SOLVER_DATA_FIXTURES:
            return _load_fixture(
                task_id=task_id,
                path=path,
                loader=td.ModeSolverData.from_file,
                fixtures=MODE_SOLVER_DATA_FIXTURES,
            )
        if path is not None:
            kwargs["path"] = path
        return _ORIGINAL_WEB_LOAD(task_id, *args, **kwargs)

    load._gui_data_tutorial_mock = True
    web.load = load


def _load_fixture(
    *,
    task_id: str,
    path: str | Path | None,
    loader: Callable[[str], Any],
    fixtures: dict[str, str],
) -> Any:
    source = DATA_DIR / fixtures[task_id]
    if path is None:
        return loader(str(source))

    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)
    return loader(str(target))
