"""A delayed stack capture must finish before the probe stops, resets, or dumps."""

import ctypes
import json
import platform
import shutil
import subprocess
import threading
from pathlib import Path

import pytest


@pytest.fixture(scope="module")
def allocation_probe(tmp_path_factory):
    compiler = shutil.which("cc")
    if (
        platform.system() != "Linux"
        or platform.libc_ver()[0] != "glibc"
        or not compiler
    ):
        pytest.skip("The allocation probe requires Linux/glibc and a C compiler")
    directory = tmp_path_factory.mktemp("allocation-probe")
    source = directory / "probe_test.c"
    probe = (
        Path(__file__).resolve().parents[1] / "benchmarks/native_context_allocations.c"
    )
    source.write_text(
        """
#include <stdlib.h>
#include <execinfo.h>
static int (*capture_hook)(void **, int);
static int controlled_backtrace(void **frames, int count) {
    return capture_hook(frames, count);
}
// Exercise the real capture implementation without interposing allocations
// made by the Python test runner itself.
#define malloc test_malloc
#define calloc test_calloc
#define realloc test_realloc
#define backtrace controlled_backtrace
#include """
        + json.dumps(str(probe))
        + """
#undef malloc
#undef calloc
#undef realloc
#undef backtrace
void test_set_capture_hook(int (*hook)(void **, int)) { capture_hook = hook; }
void test_allocate(void) { free(test_malloc(8)); }
"""
    )
    library = directory / "probe_test.so"
    subprocess.run(
        [
            compiler,
            "-std=c11",
            "-shared",
            "-fPIC",
            "-O2",
            "-o",
            str(library),
            str(source),
        ],
        check=True,
        capture_output=True,
        text=True,
        timeout=30,
    )
    loaded = ctypes.CDLL(str(library))
    loaded.probe_count.restype = ctypes.c_uint64
    loaded.probe_bytes.restype = ctypes.c_uint64
    loaded.probe_dump.argtypes = [ctypes.c_char_p]
    return loaded


@pytest.mark.parametrize("operation", ["stop", "start", "dump"])
def test_capture_finishes_before_lifecycle_operation(
    allocation_probe, tmp_path, operation
):
    probe = allocation_probe
    entered_capture = threading.Event()
    release_capture = threading.Event()
    controller_started = threading.Event()
    controller_finished = threading.Event()
    capture_timed_out = threading.Event()

    @ctypes.CFUNCTYPE(ctypes.c_int, ctypes.POINTER(ctypes.c_void_p), ctypes.c_int)
    def capture(frames, count):
        entered_capture.set()
        if not release_capture.wait(5):
            capture_timed_out.set()
        frames[0] = 0x1234
        return 1

    probe.test_set_capture_hook(capture)
    probe.probe_stacks(1)
    probe.probe_start()
    worker = threading.Thread(target=probe.test_allocate, daemon=True)
    worker.start()
    output = tmp_path / "stacks.txt"

    def control():
        controller_started.set()
        if operation == "dump":
            probe.probe_dump(str(output).encode())
        else:
            getattr(probe, f"probe_{operation}")()
        controller_finished.set()

    controller = threading.Thread(target=control, daemon=True)
    try:
        assert entered_capture.wait(5)
        controller.start()
        assert controller_started.wait(5)
        assert not controller_finished.wait(0.05), "Published an unfinished capture"
    finally:
        release_capture.set()
        worker.join(timeout=5)
        if controller.ident is not None:
            controller.join(timeout=5)
        probe.probe_stop()
    assert not worker.is_alive()
    assert not controller.is_alive()
    assert not capture_timed_out.is_set()
    assert controller_finished.is_set()
    assert probe.probe_count() == (0 if operation == "start" else 1)
    assert probe.probe_bytes() == (0 if operation == "start" else 8)
    probe.probe_dump(str(output).encode())
    assert output.read_text() == ("" if operation == "start" else "8 0x1234\n")
