# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Check the stress workload's OOM victim selection without exhausting memory."""

from __future__ import annotations

import resource
import sys
from pathlib import Path
from typing import TYPE_CHECKING

import pytest
import ray

from geneva.packager import DockerUDFPackager
from stress_tests.test_applier_oom import (
    BAD_PAYLOAD,
    PROTECTED_OOM_SCORE,
    _configure_ray_for_cgroup_oom,
    _oom_protected_runtime_env,
    alloc_no_skip,
    alloc_with_skip,
)

if TYPE_CHECKING:
    from geneva.packager import UDFSpec

# Address space left to the actor while it attempts a planted row, so the
# BAD_PAYLOAD allocation is refused instead of exhausting memory.
PLANTED_ROW_HEADROOM_BYTES = 2 * 1024 * 1024 * 1024


@pytest.mark.ray
@pytest.mark.timeout(90)
@pytest.mark.skipif(sys.platform != "linux", reason="Requires Linux OOM scores")
def test_oom_workload_makes_only_the_allocator_killable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Packaged UDFs run without their source module; only a planted row raises
    its process's score, and every other worker keeps the protected score."""
    _configure_ray_for_cgroup_oom(monkeypatch)
    # Outside the stress container no process may go below 0, so the setup
    # hook leaves workers at Ray's score.
    own_score = int(Path("/proc/self/oom_score_adj").read_text())
    worker_score = PROTECTED_OOM_SCORE if own_score == PROTECTED_OOM_SCORE else 0
    packager = DockerUDFPackager(prebuilt_docker_img="test:latest")
    specs = [
        (packager.marshal(allocate), allocate.func.__module__)
        for allocate in (alloc_with_skip, alloc_no_skip)
    ]
    ray.init(
        num_cpus=2,
        include_dashboard=False,
        runtime_env=_oom_protected_runtime_env(),
    )
    try:

        @ray.remote(max_restarts=0)
        class AllocatingActor:
            def scores(
                self, spec: UDFSpec, source_module: str
            ) -> tuple[int, int, int, bool]:
                # Pytest's source module is unavailable in the stress workers.
                sys.modules[source_module] = None
                restored = DockerUDFPackager().unmarshal(spec)
                assert restored is not None, "OOM UDF requires its source module"
                score_file = Path("/proc/self/oom_score_adj")
                before = int(score_file.read_text())
                assert restored.func(1) == b"\x00"
                after_good_row = int(score_file.read_text())

                limits = resource.getrlimit(resource.RLIMIT_AS)
                pages = int(Path("/proc/self/statm").read_text().split()[0])
                address_space = pages * resource.getpagesize()
                resource.setrlimit(
                    resource.RLIMIT_AS,
                    (address_space + PLANTED_ROW_HEADROOM_BYTES, limits[1]),
                )
                refused = False
                try:
                    restored.func(BAD_PAYLOAD)
                except MemoryError:
                    refused = True
                finally:
                    resource.setrlimit(resource.RLIMIT_AS, limits)
                return before, after_good_row, int(score_file.read_text()), refused

        @ray.remote(max_retries=0)
        def driver(
            specs: list[tuple[UDFSpec, str]],
        ) -> tuple[int, list[tuple[int, int, int, bool]], int]:
            score_file = Path("/proc/self/oom_score_adj")
            before = int(score_file.read_text())
            actor_scores = []
            for spec, source_module in specs:
                actor = AllocatingActor.remote()
                actor_scores.append(ray.get(actor.scores.remote(spec, source_module)))
                ray.kill(actor)
            return before, actor_scores, int(score_file.read_text())

        planted_row_actor = (worker_score, worker_score, 1000, True)
        assert ray.get(driver.remote(specs)) == (
            worker_score,
            [planted_row_actor, planted_row_actor],
            worker_score,
        )
    finally:
        ray.shutdown()
