# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import gc
import multiprocessing
import os
import socket
import sys
import time
from threading import Event, Thread

import pytest

from tango import (
    AttrWriteType,
    DevFailed,
    DeviceData,
    DeviceDataList,
    DeviceProxy,
    DevState,
    EventType,
    Group,
    GroupAttrReply,
    GroupCmdReply,
    GroupReply,
    StdStringVector,
)
from tango.server import Device, attribute, command
from tango.test_context import MultiDeviceTestContext
from tango.test_utils import DeviceTestContext
from tango.utils import TO_TANGO_TYPE

_is_allowed = [True]


class SimpleDevice(Device):
    _attr = None

    def init_device(self):
        self._attr = int(self.get_name()[-1])
        super().init_device()
        self.set_state(DevState.ON)

    @attribute(access=AttrWriteType.READ_WRITE)
    def attr(self) -> int:
        return self._attr

    @attr.setter
    def set_attr(self, new_value):
        self._attr = new_value

    @attr.is_allowed
    def is_allowed(self, req) -> bool:
        return _is_allowed[0]

    @command()
    def identity(self, v_in: int) -> int:
        return v_in

    def is_identity_allowed(self) -> bool:
        return _is_allowed[0]


devices_info = (
    {
        "class": SimpleDevice,
        "devices": [{"name": "test/device/1"}, {"name": "test/device/2"}],
    },
)


@pytest.fixture(scope="module")
def context():
    with MultiDeviceTestContext(devices_info) as ctx:
        yield ctx


def test_wrong_device_name(context):
    group = Group("test_group")
    group.add("test/device/1")

    with pytest.raises(KeyError, match="some/wrong/device"):
        group.get_device("some/wrong/device")

    with pytest.raises(KeyError, match="some/wrong/device"):
        group["some/wrong/device"]


def test_nested_multi_group(context):
    group_singles = Group("add-one-at-a-time")
    group_singles.add("test/device/1")
    group_singles.add("test/device/2")
    group_multiples_list = Group("add-multiple-via-list")
    group_multiples_list.add(["test/device/1", "test/device/2"])
    group_multiples_vector = Group("add-multiple-via-std-vector")
    vector = StdStringVector()
    vector.append("test/device/1")
    vector.append("test/device/2")
    group_multiples_vector.add(vector)
    group_in_group = Group("add-sub-group")
    group_in_group.add(group_singles)

    groups = [
        group_singles,
        group_multiples_list,
        group_multiples_vector,
        group_in_group,
    ]

    device1_fqdn = context.get_device_access("test/device/1")
    device2_fqdn = context.get_device_access("test/device/2")
    for group in groups:
        assert device1_fqdn in group
        assert device2_fqdn in group
        reply = group.read_attribute("attr")
        assert reply[0].dev_name() == device1_fqdn
        assert reply[1].dev_name() == device2_fqdn
        assert not reply[0].has_failed()
        assert not reply[1].has_failed()
        assert reply[0].get_data().value == 1
        assert reply[1].get_data().value == 2

    # patterns are not supported via DeviceTestContext
    with pytest.raises(DevFailed):
        group_multiples_pattern = Group("add-multiple-via-pattern")
        group_multiples_pattern.add("test/device/*")


def test_read_write_attribute(context):

    _is_allowed[0] = True

    group = Group("test_group")
    group.add("test/device/1")
    group.add("test/device/2")

    seq = group.write_attribute("attr", 3)

    for ret in seq:
        assert not ret.has_failed()
        assert isinstance(ret, GroupReply)

    seq = group.read_attribute("attr")

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data().value == 3
        # we check, that we can read value for the second time
        assert ret.get_data().value == 3
        assert isinstance(ret, GroupAttrReply)

    # now we check that we can iterate over GroupReplyList for the second time
    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data().value == 3
        assert ret.get_data().value == 3
        assert isinstance(ret, GroupAttrReply)

    dev = group.get_device(1)
    attr_info = dev.get_attribute_config("attr")
    seq = group.write_attribute(attr_info, 4)

    for ret in seq:
        assert not ret.has_failed()
        assert isinstance(ret, GroupReply)

    seq = group.read_attribute("attr")

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data().value == 4

    _is_allowed[0] = False

    for ret in group.write_attribute("attr", 5):
        assert ret.has_failed()
        assert (
            ret.get_err_stack()[0].desc == "It is currently not allowed to write attribute attr. The device state is ON"
        )

    for ret in group.read_attribute("attr"):
        assert ret.has_failed()
        assert ret.get_err_stack()[0].desc == "It is currently not allowed to read attribute attr"


def test_command(context):

    _is_allowed[0] = True

    group = Group("test_group")
    group.add("test/device/1")
    group.add("test/device/2")

    seq = group.command_inout("identity", 1)

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1
        # we check, that we can read value for the second time
        assert ret.get_data() == 1
        assert isinstance(ret, GroupCmdReply)

    # now we check that we can iterate over GroupReplyList for the second time
    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1
        assert ret.get_data() == 1
        assert isinstance(ret, GroupCmdReply)

    param = DeviceData()
    param.insert(TO_TANGO_TYPE[int], 1)

    seq = group.command_inout("identity", param)

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1

    param_list = DeviceDataList()
    param_list.extend([param, param])

    seq = group.command_inout("identity", param_list)

    for ret in seq:
        assert not ret.has_failed()
        assert ret.get_data() == 1

    _is_allowed[0] = False

    for ret in group.command_inout("identity", 2):
        assert ret.has_failed()
        assert ret.get_err_stack()[0].desc == "Command identity not allowed when the device is in ON state"


def test_group_connection_and_async_submission(context):
    _is_allowed[0] = True
    group = Group("async-operations")
    group.add(["test/device/1", "test/device/2"])

    group.set_timeout_millis(500)
    assert group.ping() >= 0
    assert group.get_device(1).ping() >= 0
    assert group.get_device(context.get_device_access("test/device/2")).ping() >= 0

    request = group.command_inout_asynch("State")
    assert all(not reply.has_failed() for reply in group.command_inout_reply(request))

    request = group.command_inout_asynch("identity", 7)
    assert [reply.get_data() for reply in group.command_inout_reply(request)] == [7, 7]

    parameter = DeviceData()
    parameter.insert(TO_TANGO_TYPE[int], 9)
    parameters = DeviceDataList()
    parameters.extend([parameter, parameter])
    request = group.command_inout_asynch("identity", parameters)
    assert [reply.get_data() for reply in group.command_inout_reply(request)] == [9, 9]

    request = group.read_attribute_asynch("attr")
    assert [reply.get_data().value for reply in group.read_attribute_reply(request)] == [1, 2]

    request = group.read_attributes_asynch(["attr"])
    assert [reply.get_data().value for reply in group.read_attributes_reply(request)] == [1, 2]

    request = group.write_attribute_asynch("attr", 5)
    assert all(not reply.has_failed() for reply in group.write_attribute_reply(request))
    assert [reply.get_data().value for reply in group.read_attribute("attr")] == [5, 5]


@pytest.mark.extra_src_test
def test_group_connection_releases_gil_while_endpoint_is_unresponsive():
    with socket.socket() as listener:
        listener.bind(("127.0.0.1", 0))
        listener.listen()
        listener.settimeout(0.1)
        stop = Event()
        accepted = []

        def hold_connections():
            while not stop.is_set():
                try:
                    connection, _ = listener.accept()
                    accepted.append(connection)
                except TimeoutError:
                    continue

        server = Thread(target=hold_connections, daemon=True)
        server.start()
        try:
            port = listener.getsockname()[1]
            group = Group("unresponsive")
            group.set_timeout_millis(500)

            def record_progress_background_in_thread(progress_at):
                time.sleep(0.1)
                progress_at.append(time.monotonic())

            add_progress_at = []
            progress = Thread(target=record_progress_background_in_thread, args=(add_progress_at,))
            progress.start()
            add_started_at = time.monotonic()
            group.add(f"tango://127.0.0.1:{port}/test/device/1#dbase=no")
            add_returned_at = time.monotonic()
            progress.join(timeout=2)
            assert add_returned_at - add_started_at > 0.3, "The endpoint did not delay Group.add()"
            assert add_progress_at and add_progress_at[0] < add_returned_at, (
                "GIL not released to allow another Python thread to run"
            )

            ping_progress_at = []
            progress = Thread(target=record_progress_background_in_thread, args=(ping_progress_at,))
            progress.start()
            started_at = time.monotonic()
            assert not group.ping()
            returned_at = time.monotonic()
            progress.join(timeout=2)
            assert returned_at - started_at > 0.3, "The endpoint did not delay Group.ping()"
            assert ping_progress_at and ping_progress_at[0] < returned_at, (
                "GIL not released to allow another Python thread to run"
            )

            # A failed ping temporarily suppresses reconnect attempts.
            time.sleep(1.1)
            submit_progress_at = []
            progress = Thread(target=record_progress_background_in_thread, args=(submit_progress_at,))
            progress.start()
            submit_started_at = time.monotonic()
            group.command_inout_asynch("State")
            submit_returned_at = time.monotonic()
            progress.join(timeout=2)
            assert submit_returned_at - submit_started_at > 0.3, "The endpoint did not delay async submission"
            assert submit_progress_at and submit_progress_at[0] < submit_returned_at, (
                "GIL not released to allow another Python thread to run"
            )
        finally:
            stop.set()
            for connection in accepted:
                connection.close()
            server.join(timeout=2)


def test_nested_group_hierarchy_destruction():
    """Group.add(subgroup) hands ownership of the child to Tango::Group, whose
    destructor deletes it. The Python wrapper must not delete it as well."""
    root = Group("root")
    child = Group("child")
    grandchild = Group("grandchild")
    child.add(grandchild)
    root.add(child)

    assert root.get_group("child").get_name() == "child"
    assert root.get_group("grandchild").get_name() == "grandchild"

    del root
    gc.collect()


def test_readding_group_to_second_parent_is_rejected():
    """A group already attached to one parent must be refused by a second one,
    rather than being handed over twice and double-deleted.

    add() rebinds the child's inner wrapper to a non-owning view of the attached
    subgroup, so the second attempt is turned away on type before it can reach
    the ownership handover in C++ -- hence TypeError rather than a complaint
    about ownership.
    """
    first = Group("first")
    second = Group("second")
    child = Group("child")

    first.add(child)

    with pytest.raises(TypeError, match="Should be Group"):
        second.add(child)


def test_no_wrapper_leak_when_nesting_groups():
    """Group.add(subgroup) used to leak the subgroup's Python wrapper on every
    call, so that the wrapper could never delete a child that Tango::Group had
    already taken over.

    Counted with sys.getallocatedblocks() rather than gc.get_objects(): pybind11
    instances are only GC-tracked when the class is declared with
    py::dynamic_attr(), which __Group is not, so the GC never sees them. The
    memory-test harness in tests/valgrind cannot gate this either -- it samples
    once per section, and one step of a few hundred blocks is averaged away by
    its trailing-window slope. Measured 2.0 blocks/call leaked before the fix
    versus under 0.01 after, so the tolerance below has ~100x margin either way.
    """

    def nest_groups():
        root = Group("root")
        child = Group("child")
        grandchild = Group("grandchild")
        child.add(grandchild)
        root.add(child)

    warmup, iterations = 200, 500
    for _ in range(warmup):
        nest_groups()

    gc.collect()
    before = sys.getallocatedblocks()
    for _ in range(iterations):
        nest_groups()
    gc.collect()
    leaked = (sys.getallocatedblocks() - before) / iterations

    assert leaked < 0.5, f"{leaked:.2f} allocator blocks leaked per nested Group.add()"


class RemovalEventDevice(Device):
    @attribute(dtype=int, change_event_implemented=True, change_event_detect=False)
    def sample(self):
        return 0

    @command
    def send_sample(self):
        self.push_change_event("sample", 123)


def remove_group_during_event_callback(device_trl, operation, callback_started_connection):
    group = Group("root")
    if operation == "subgroup":
        subgroup = Group("child")
        subgroup.add(device_trl)
        group.add(subgroup)
        del subgroup  # the parent now owns the native child group
    else:
        group.add(device_trl)

    # get_device() returns a reference to the proxy owned by the group.
    # Drop the Python reference before removing its native owner.
    owned_proxy = group.get_device(1)
    callback_started = Event()
    callback_finished = Event()

    def callback(event):
        if not event.err and event.attr_value.value == 123:
            callback_started_connection.send(None)
            callback_started.set()
            time.sleep(3)
            callback_finished.set()

    owned_proxy.subscribe_event("sample", EventType.CHANGE_EVENT, callback)
    trigger_proxy = DeviceProxy(device_trl)
    trigger_proxy.send_sample()
    assert callback_started.wait(timeout=5)
    del owned_proxy

    if operation == "string":
        group.remove(group.get_device_list()[0])
    elif operation == "list":
        group.remove(list(group.get_device_list()))
    elif operation == "subgroup":
        group.remove("child")
    else:
        group.remove_all()

    assert group.get_size() == 0
    assert callback_finished.wait(timeout=5)
    os._exit(0)  # the removal operation is complete; skip unrelated teardown


@pytest.mark.extra_src_test
@pytest.mark.parametrize("operation", ["string", "list", "remove_all", "subgroup"])
def test_group_removal_does_not_deadlock_during_event_callback(operation):
    device_context = DeviceTestContext(RemovalEventDevice, process=True)
    with device_context:
        process_context = multiprocessing.get_context("spawn")
        callback_started, callback_started_connection = process_context.Pipe(duplex=False)
        client = process_context.Process(
            target=remove_group_during_event_callback,
            args=(device_context.get_device_access(), operation, callback_started_connection),
        )
        client.start()
        callback_started_connection.close()
        try:
            assert callback_started.poll(timeout=5), "The event callback did not start"
            callback_started.recv()
            client.join(timeout=6)
            assert client.exitcode is not None, f"Group {operation} blocked during the callback"
            assert client.exitcode == 0, f"Client exited unexpectedly: {client.exitcode}"
        finally:
            callback_started.close()
            if client.is_alive():
                client.terminate()
                client.join(timeout=2)
                if client.is_alive():
                    client.kill()
                    client.join()
