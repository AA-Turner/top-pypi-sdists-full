# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
from tango import (
    Util,
    SerialModel,
    AutoTangoAllowThreads,
    EnsureOmniThread,
    AutoTangoMonitor,
    DevFailed,
)
from tango.server import Device, attribute
from tango.test_utils import DeviceTestContext

from threading import Thread, Event
from queue import Queue

import pytest

from time import sleep

pytestmark = pytest.mark.extra_src_test


def do_nothing():
    sleep(1e-3)


class SimpleDS(Device):

    def init_device(self):
        u = Util.instance()
        mode = SerialModel.BY_CLASS

        u.set_serial_model(mode)
        assert u.get_serial_model() == mode

        with AutoTangoAllowThreads(self):
            with AutoTangoAllowThreads(self):
                do_nothing()

    @attribute
    def attr(self) -> int:
        return 1234


def test_dont_crash_with_nested_tango_allow_threads():
    with DeviceTestContext(SimpleDS) as proxy:
        assert proxy.attr == 1234


class MonSameThread(Device):
    serial_model = None
    unlock = None
    running = None

    def init_device(self):
        u = Util.instance()

        u.set_serial_model(MonSameThread.serial_model)
        assert u.get_serial_model() == MonSameThread.serial_model

        self._thread = Thread(target=self.thread_func)
        MonSameThread.running = True
        self._thread.start()

    def delete_device(self):
        MonSameThread.running = False
        self._thread.join()

    def thread_func(self):
        with EnsureOmniThread():
            if MonDiffThread.serial_model == SerialModel.BY_CLASS:
                obj = self.get_device_class()
            else:
                obj = self

        with AutoTangoMonitor(obj):
            if MonSameThread.unlock:
                # unlock it again
                with AutoTangoAllowThreads(self):
                    while MonSameThread.running:
                        do_nothing()
            else:
                while MonSameThread.running:
                    do_nothing()

    @attribute
    def attr(self) -> int:
        return 1234


@pytest.mark.parametrize("unlock", [True, False])
def test_monitor_force_unlock_from_same_thread(
    unlock, server_green_mode, server_serial_model
):
    MonSameThread.serial_model = server_serial_model
    MonSameThread.unlock = unlock

    if unlock:
        if server_serial_model == SerialModel.BY_CLASS:
            pytest.xfail(
                "Not implemented, see https://gitlab.com/tango-controls/pytango/-/issues/650"
            )
        elif server_serial_model == SerialModel.BY_PROCESS:
            pytest.xfail(
                "Not implemented, see https://gitlab.com/tango-controls/pytango/-/issues/650"
            )

    with DeviceTestContext(MonSameThread) as proxy:

        if server_serial_model == SerialModel.NO_SYNC:
            assert proxy.attr == 1234
        elif unlock:
            assert proxy.attr == 1234
        else:
            with pytest.raises(
                DevFailed, match="not able to acquire serialization monitor"
            ):
                assert proxy.attr == 1234

        # required especially by SerialModel.BY_PROCESS so that the DS can be killed from the test context
        MonSameThread.running = False


class MonDiffThread(Device):
    serial_model = None
    unlock = None
    running = None

    def init_device(self):
        u = Util.instance()

        u.set_serial_model(MonDiffThread.serial_model)
        assert u.get_serial_model() == MonDiffThread.serial_model

        MonDiffThread.running = True

        self._lock_thread = Thread(target=self.lock_thread_func)
        self._lock_thread.start()

        self._unlock_thread = Thread(target=self.unlock_thread_func)
        self._unlock_thread.start()

    def delete_device(self):
        MonDiffThread.running = False
        self._lock_thread.join()
        self._unlock_thread.join()

    def lock_thread_func(self):
        with EnsureOmniThread():
            if MonDiffThread.serial_model == SerialModel.BY_CLASS:
                obj = self.get_device_class()
            else:
                obj = self

            with AutoTangoMonitor(obj):
                while MonDiffThread.running:
                    do_nothing()

    def unlock_thread_func(self):
        with EnsureOmniThread():
            if MonDiffThread.unlock:
                # try to unlock it, but as this is from a different thread, nothing happens
                with AutoTangoAllowThreads(self):
                    while MonDiffThread.running:
                        do_nothing()
            else:
                while MonDiffThread.running:
                    do_nothing()

    @attribute
    def attr(self) -> int:
        return 1234


@pytest.mark.parametrize("unlock", [True, False])
def test_monitor_force_unlock_from_different_thread(
    unlock, server_green_mode, server_serial_model
):
    MonDiffThread.serial_model = server_serial_model
    MonDiffThread.unlock = unlock

    with DeviceTestContext(MonDiffThread) as proxy:

        if server_serial_model == SerialModel.NO_SYNC:
            assert proxy.attr == 1234
        else:
            with pytest.raises(
                DevFailed, match="not able to acquire serialization monitor"
            ):
                assert proxy.attr == 1234

        # required especially by SerialModel.BY_PROCESS so that the DS can be killed from the test context
        MonDiffThread.running = False


class DontDeadlock(Device):
    def init_device(self) -> None:
        self.queue = Queue[Event | None]()
        self.thread = Thread(target=self._run)
        self.thread.start()

    def delete_device(self) -> None:
        self.queue.put(None)
        self.thread.join()

    def _run(self) -> None:
        with EnsureOmniThread():
            while True:
                ev = self.queue.get()
                if ev is None:
                    break

                with AutoTangoMonitor(self):
                    ev.set()

    @attribute
    def attr(self) -> int:
        ev = Event()
        self.queue.put(ev)
        # Allow the thread to run and start waiting for the monitor
        sleep(0.01)
        with AutoTangoAllowThreads(self):
            ev.wait()

        return 1234


# This test will probably only fail if the system is under load
def test_dont_deadlock_when_releasing_monitor():
    with DeviceTestContext(DontDeadlock, process=True) as proxy:
        for _ in range(100):
            assert proxy.attr == 1234
