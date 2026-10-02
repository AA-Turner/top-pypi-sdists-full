"""pytest fixtures for the cluster environment tests. Test modules import them by name.

Opt-in: nothing here runs unless ``PROBE_ENV_TESTS=1`` (see ``requires_env_tests``).
"""

from __future__ import annotations

import os
import uuid

import pytest

from . import backend as backend_mod
from .lab import Lab, docker_available, ensure_image, sdk_version

requires_env_tests = pytest.mark.skipif(
    os.environ.get("PROBE_ENV_TESTS") != "1",
    reason="environment tests are opt-in: PROBE_ENV_TESTS=1 (agent/tests/environments/run.sh)",
)


#: The box these run on is shared and its disk is tight; a lab writes little, but
#: never start one below this much free space.
MIN_FREE_BYTES = int(float(os.environ.get("PROBE_ENV_MIN_FREE_GB", "5")) * (1 << 30))


@pytest.fixture(scope="session")
def image() -> str:
    problem = docker_available()
    if problem:
        pytest.skip(problem)
    import shutil

    free = shutil.disk_usage("/").free
    if free < MIN_FREE_BYTES:
        pytest.skip(f"only {free / (1 << 30):.1f} GiB free on /; PROBE_ENV_MIN_FREE_GB="
                    f"{MIN_FREE_BYTES / (1 << 30):.0f}")
    tag = ensure_image()
    print(f"\n[envtest] image {tag}, probe-research {sdk_version(tag)}")
    return tag


@pytest.fixture
def backend(tmp_path_factory):
    problem = backend_mod.real_mode_problem()
    if problem:
        pytest.fail(problem)
    workdir = tmp_path_factory.mktemp("envtest")
    b = backend_mod.make_backend(workdir)
    b.start()
    print(f"\n[envtest] backend={b.kind} url={b.url} project={b.project}")
    try:
        yield b
    finally:
        b.stop()


@pytest.fixture
def lab(image, request):
    lab = Lab(image=image)
    try:
        yield lab
    finally:
        failed = getattr(request.node, "rep_call", None)
        if os.environ.get("PROBE_ENV_KEEP") == "1":
            print(f"\n[envtest] PROBE_ENV_KEEP=1: leaving lab {lab.prefix}-* for inspection")
        else:
            if failed is not None and failed.failed:
                print("\n[envtest] diagnostics:\n" + lab.diagnostics()[-15000:])
            lab.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Lets `lab` print container logs on a failure. Active where a conftest
    re-exports this module (each environment directory's conftest.py does)."""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def unique(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:6]}"
