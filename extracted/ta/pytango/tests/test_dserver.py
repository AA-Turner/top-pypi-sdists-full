# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Regression coverage for direct DServer polling operations."""

import multiprocessing
import threading
import time

import pytest


def _check_remove_last_polled_attribute_while_handler_is_active():
    from tango import Util
    from tango.server import Device, attribute
    from tango.test_utils import DeviceTestContext

    armed = threading.Event()
    entered = threading.Event()
    release = threading.Event()
    completed = threading.Event()

    class TestDevice(Device):
        @attribute
        def value(self) -> int:
            if armed.is_set():
                entered.set()
                assert release.wait(5)
                completed.set()
            return 1

    with DeviceTestContext(TestDevice, process=False) as proxy:
        admin = Util.instance().get_dserver_device()
        name = proxy.name()
        admin.add_obj_polling(([100], [name, "attribute", "value"]), False)
        armed.set()
        assert entered.wait(5), "polling handler did not start"

        def allow_handler_to_finish():
            time.sleep(0.2)
            release.set()

        timer = threading.Thread(target=allow_handler_to_finish)
        timer.start()
        admin.rem_obj_polling([name, "attribute", "value"], False)
        timer.join(2)
        assert completed.is_set(), "polling handler did not finish"


@pytest.mark.extra_src_test
def test_remove_last_polled_attribute_while_handler_is_active():
    process = multiprocessing.get_context("spawn").Process(
        target=_check_remove_last_polled_attribute_while_handler_is_active
    )
    process.start()
    process.join(15)
    if process.is_alive():
        process.kill()
        process.join()
        pytest.fail("polling removal timed out")
    assert process.exitcode == 0, f"polling removal exited with code {process.exitcode}"


def _check_dserver_monitor_wait_allows_python_handler_to_finish(operation):
    from tango import DevFailed, SerialModel, Util
    from tango.server import Device, attribute
    from tango.test_utils import DeviceTestContext

    entered = threading.Event()
    release = threading.Event()
    handler_finished = threading.Event()
    removal_started = threading.Event()
    removal_finished = threading.Event()

    class TestDevice(Device):
        @attribute
        def value(self) -> int:
            entered.set()
            assert release.wait(5)
            handler_finished.set()
            return 1

    with DeviceTestContext(TestDevice, process=False) as proxy:
        util = Util.instance()
        util.set_serial_model(SerialModel.NO_SYNC)
        admin = util.get_dserver_device()
        name = proxy.name()
        admin.add_obj_polling(([100], [name, "attribute", "value"]), False)
        assert entered.wait(5), "polling handler did not start"

        def remove_polling():
            removal_started.set()
            try:
                admin.rem_obj_polling([name, "attribute", "value"], False)
            finally:
                removal_finished.set()

        removal = threading.Thread(target=remove_polling)
        removal.start()
        assert removal_started.wait(2)
        time.sleep(0.1)
        assert not removal_finished.is_set(), "polling removal finished before the DServer call"

        timer = threading.Timer(0.2, release.set)
        timer.start()
        started = time.monotonic()
        try:
            if operation == "lock_device":
                admin.lock_device(([30], [name]))
            elif operation == "query_class":
                admin.query_class()
            elif operation == "query_device":
                admin.query_device()
            elif operation == "query_sub_device":
                admin.query_sub_device()
            elif operation == "query_class_prop":
                admin.query_class_prop("TestDevice")
            elif operation == "query_dev_prop":
                admin.query_dev_prop("TestDevice")
            elif operation == "polled_device":
                admin.polled_device()
            elif operation == "dev_poll_status":
                admin.dev_poll_status(name)
            elif operation == "un_lock_device":
                admin.un_lock_device(([0], [name]))
            elif operation == "re_lock_devices":
                admin.re_lock_devices([name])
            elif operation == "dev_lock_status":
                admin.dev_lock_status(name)
            elif operation == "start_logging":
                admin.start_logging()
            elif operation == "stop_logging":
                admin.stop_logging()
            elif operation == "add_event_heartbeat":
                admin.add_event_heartbeat()
            elif operation == "rem_event_heartbeat":
                admin.rem_event_heartbeat()
        except DevFailed:
            if operation not in {"lock_device", "un_lock_device", "re_lock_devices"}:
                raise
        elapsed = time.monotonic() - started

        timer.join(2)
        removal.join(2)
        assert release.is_set(), f"Python timer could not run during {operation}"
        assert elapsed >= 0.15, f"{operation} did not wait for the DServer monitor"
        assert elapsed < 2, f"{operation} prevented the Python timer from running"
        assert handler_finished.is_set(), "polling handler timed out"
        assert removal_finished.is_set(), "polling removal did not finish"


@pytest.mark.extra_src_test
@pytest.mark.parametrize(
    "operation",
    [
        "lock_device",
        "query_class",
        "query_device",
        "query_sub_device",
        "query_class_prop",
        "query_dev_prop",
        "polled_device",
        "dev_poll_status",
        "un_lock_device",
        "re_lock_devices",
        "dev_lock_status",
        "start_logging",
        "stop_logging",
        "add_event_heartbeat",
        "rem_event_heartbeat",
    ],
)
def test_dserver_monitor_wait_allows_python_handler_to_finish(operation):
    process = multiprocessing.get_context("spawn").Process(
        target=_check_dserver_monitor_wait_allows_python_handler_to_finish,
        args=(operation,),
    )
    process.start()
    process.join(15)
    if process.is_alive():
        process.kill()
        process.join()
        pytest.fail(f"{operation} timed out while a Python handler held the monitor")
    assert process.exitcode == 0, f"{operation} exited with code {process.exitcode}"
