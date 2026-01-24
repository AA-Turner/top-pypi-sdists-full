# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
"""Load tango-specific pytest fixtures."""

import multiprocessing
import sys
import os
import json
import shutil
from functools import partial
from subprocess import Popen

import pytest

from tango import DeviceProxy, GreenMode, Util
from tango.asyncio import DeviceProxy as asyncio_DeviceProxy
from tango.gevent import DeviceProxy as gevent_DeviceProxy
from tango.futures import DeviceProxy as futures_DeviceProxy
from tango.test_utils import (
    ClassicAPISimpleDeviceClass,
    ClassicAPISimpleDeviceImpl,
    attr_data_format,
    attribute_numpy_typed_values,
    attribute_typed_values,
    attribute_wrong_numpy_typed,
    base_type,
    command_numpy_typed_values,
    command_typed_values,
    dev_encoded_values,
    extract_as,
    general_typed_values,
    server_green_mode,
    server_serial_model,
    state,
    wait_for_nodb_proxy_via_pid,
)

from tango._tango import _dump_cpp_coverage

__all__ = (
    "state",
    "general_typed_values",
    "command_typed_values",
    "attribute_typed_values",
    "command_numpy_typed_values",
    "attribute_numpy_typed_values",
    "attribute_wrong_numpy_typed",
    "dev_encoded_values",
    "server_green_mode",
    "server_serial_model",
    "attr_data_format",
    "extract_as",
    "base_type",
)

device_proxy_map = {
    GreenMode.Synchronous: DeviceProxy,
    GreenMode.Futures: futures_DeviceProxy,
    GreenMode.Asyncio: partial(asyncio_DeviceProxy, wait=True),
    GreenMode.Gevent: gevent_DeviceProxy,
}


def pytest_addoption(parser):
    parser.addoption(
        "--run_extra_src_tests",
        action="store_true",
        default=False,
        help="run extra tests only for source builds",
    )
    parser.addoption(
        "--write_cpp_coverage",
        action="store_true",
        default=False,
        help="write cpp coverage data during tests",
    )


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "extra_src_test: mark test as only for source builds"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--run_extra_src_tests"):
        # --run_extra_src_tests given in cli: do not skip those tests
        return
    skip_extra_src_test = pytest.mark.skip(
        reason="need --run_extra_src_tests option to run"
    )
    for item in items:
        if "extra_src_test" in item.keywords:
            item.add_marker(skip_extra_src_test)


@pytest.hookimpl()
def pytest_sessionfinish(session):
    """Collects all tests to be run and outputs to bat script"""
    if "--collect-only" in sys.argv and "-q" in sys.argv and "nt" in os.name:
        print("Generating windows test script...")
        script_path = os.path.join(os.path.dirname(__file__), "run_tests_win.bat")

        total_tests = len(session.items)

        with open(script_path, "w") as f:
            f.write("@echo off\r\n")
            f.write("setlocal enabledelayedexpansion\r\n")
            f.write("REM This script will run all tests separately.\r\n")
            f.write(f"set TOTAL_TESTS={total_tests}\r\n")
            f.write("set CURRENT_TEST=0\r\n")
            f.write("\r\n")

            for item in session.items:
                # Escape special characters for batch file
                nodeid = item.nodeid
                nodeid_escaped = nodeid.replace("(", "^(").replace(")", "^)")

                lines = [
                    # Progress counter
                    "set /a CURRENT_TEST+=1",
                    f"echo [!CURRENT_TEST!/%TOTAL_TESTS%] Running: {nodeid_escaped}",
                    "",
                    # Run a single test
                    f'pytest -c pytest_win_config.toml "{nodeid}"',
                    "set FIRST_RUN_ERROR=!errorlevel!",
                    "",
                    # Check if test failed (exit code 1)
                    "if !FIRST_RUN_ERROR! equ 1 (",
                    # we retry ones
                    f"    echo [!CURRENT_TEST!/%TOTAL_TESTS%] FAILED - Retrying: {nodeid_escaped}",
                    f'    pytest --lf -c pytest_win_config.toml "{nodeid}"',
                    "    set RETRY_ERROR=!errorlevel!",
                    "    if !RETRY_ERROR! equ 1 (",
                    f'        echo {nodeid_escaped} >> "%~dp0failed_tests.txt"',
                    f"        echo [!CURRENT_TEST!/%TOTAL_TESTS%] FAILED after retry: {nodeid_escaped}",
                    "    ) else if !RETRY_ERROR! equ 0 (",
                    f"        echo [!CURRENT_TEST!/%TOTAL_TESTS%] PASSED on retry: {nodeid_escaped}",
                    "    ) else if !RETRY_ERROR! geq 2 if !RETRY_ERROR! leq 5 (",
                    # Abort if pytest could not execute properly
                    # From: https://docs.pytest.org/en/7.1.x/reference/exit-codes.html
                    #   Exit code 0: All tests were collected and passed successfully
                    #   Exit code 1: Tests were collected and run but some of the tests failed
                    #   Exit code 2: Test execution was interrupted by the user
                    #   Exit code 3: Internal error happened while executing tests
                    #   Exit code 4: pytest command line usage error
                    #   Exit code 5: No tests were collected
                    "        exit /b !RETRY_ERROR!",
                    "    )",
                    ") else if !FIRST_RUN_ERROR! equ 0 (",
                    f"    echo [!CURRENT_TEST!/%TOTAL_TESTS%] PASSED: {nodeid_escaped}",
                    # Abort if pytest could not execute properly (exit codes 2-5)
                    ") else if !FIRST_RUN_ERROR! geq 2 if !FIRST_RUN_ERROR! leq 5 (",
                    "    exit /b !FIRST_RUN_ERROR!",
                    ")",
                    "",
                ]
                f.writelines([f"{line}\r\n" for line in lines])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport():
    """Produces summary.json file for quick windows test summary"""
    summary_path = "summary.json"

    outcome = yield  # Run all other pytest_runtest_makereport non wrapped hooks
    result = outcome.get_result()
    if result.when == "call" and "nt" in os.name and os.path.isfile(summary_path):
        with open(summary_path, "r+") as f:
            summary = f.read()
            try:
                summary = json.loads(summary)
            except Exception:
                summary = []
            finally:
                outcome = str(result.outcome).capitalize()
                test = {
                    "testName": result.nodeid,
                    "outcome": outcome,
                    "durationMilliseconds": result.duration,
                    "StdOut": result.capstdout,
                    "StdErr": result.capstderr,
                }
                summary.append(test)
                f.seek(0)
                f.write(json.dumps(summary))
                f.truncate()


def start_server(host, server, inst, device):
    exe = shutil.which(server)
    cmd = f"{exe} {inst} -ORBendPoint giop:tcp:{host}:0 -nodb -dlist {device}"
    proc = Popen(cmd.split(), close_fds=True)
    proc.poll()
    return proc


@pytest.fixture(
    params=GreenMode.values.values(),
    ids=str,
    scope="module",
)
def tango_test_with_green_modes(request):
    green_mode = request.param
    server = "TangoTest"
    inst = "test"
    device = "sys/tg_test/17"
    host = "127.0.0.1"
    proc = start_server(host, server, inst, device)
    proxy = wait_for_nodb_proxy_via_pid(
        proc.pid, host, device, device_proxy_map[green_mode]
    )

    yield proxy

    proc.terminate()
    # let's not wait for it to exit, that takes too long :)


@pytest.fixture(scope="module")
def tango_test():
    green_mode = GreenMode.Synchronous
    server = "TangoTest"
    inst = "test"
    device = "sys/tg_test/17"
    host = "127.0.0.1"
    proc = start_server(host, server, inst, device)
    proxy = wait_for_nodb_proxy_via_pid(
        proc.pid, host, device, device_proxy_map[green_mode]
    )

    yield proxy

    proc.terminate()


@pytest.fixture(scope="function")
def tango_test_process_device_trl_with_function_scope():
    green_mode = GreenMode.Synchronous
    server = "TangoTest"
    inst = "test"
    device = "sys/tg_test/18"
    host = "127.0.0.1"
    proc = start_server(host, server, inst, device)
    proxy = wait_for_nodb_proxy_via_pid(
        proc.pid, host, device, device_proxy_map[green_mode]
    )

    device_trl = (
        f"tango://{proxy.get_dev_host()}:{proxy.get_dev_port()}/"
        f"{proxy.dev_name()}#dbase=no"
    )
    yield proc, device_trl

    proc.terminate()


@pytest.fixture(
    params=GreenMode.values.values(),
    ids=str,
    scope="module",
)
def green_mode_device_proxy(request):
    green_mode = request.param
    return device_proxy_map[green_mode]


def run_mixed_server():
    util = Util(
        [
            "MixedServer",
            "1",
            "-ORBendPoint",
            "giop:tcp:127.0.0.1:0",
            "-nodb",
            "-dlist",
            "my/mixed/1",
        ]
    )
    util.add_class(
        ClassicAPISimpleDeviceClass,
        ClassicAPISimpleDeviceImpl,
        "ClassicAPISimpleDevice",
    )
    util.add_class("TangoTest", "TangoTest", language="c++")
    u = Util.instance()
    u.server_init()
    u.server_run()


@pytest.fixture(autouse=True)
def flush_cpp_coverage_data(request):
    """
    Flushes C++ coverage data to disk after each test execution
    when --write_cpp_coverage command line argument was passed.
    """

    # nothing on enter
    yield

    if request.config.getoption("--write_cpp_coverage"):
        _dump_cpp_coverage()


@pytest.fixture
def mixed_tango_test_server():
    process = multiprocessing.Process(target=run_mixed_server)
    process.start()

    proxy_waiter = partial(
        wait_for_nodb_proxy_via_pid,
        process.pid,
        "127.0.0.1",
        "dserver/mixedserver/1",
        device_proxy_map[GreenMode.Synchronous],
    )
    yield process, proxy_waiter

    if process.is_alive():
        process.terminate()
        process.join(timeout=3.0)  # Allow TangoTest time to stop DataGenerator
