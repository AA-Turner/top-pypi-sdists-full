# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
# Imports
import asyncio
import time

import concurrent.futures
from concurrent.futures import Future

from dataclasses import dataclass
from typing import Union

import pytest

from tango import (
    ApiUtil,
    AttrReadEvent,
    AttrWriteType,
    AttrWrittenEvent,
    CmdDoneEvent,
    DevFailed,
    GreenMode,
    cb_sub_model,
    get_device_proxy,
)
from tango.server import Device, attribute, command
from tango.test_utils import DeviceTestContext, assert_close

A_BIT = 0.1


class ServerTest(Device):
    _value1 = 100
    _value2 = 200

    @attribute(access=AttrWriteType.READ_WRITE)
    def attr1(self) -> int:
        return self._value1

    @attr1.write
    def set_attr1(self, val):
        self._value1 = val

    @attribute(access=AttrWriteType.READ_WRITE)
    def attr2(self) -> int:
        return self._value2

    @attr2.write
    def set_attr2(self, val):
        self._value2 = val

    @attribute(dtype=int, access=AttrWriteType.READ)
    def attr_no_value(self):
        return

    @attribute(dtype=int, access=AttrWriteType.READ)
    def attr_exception(self):
        raise RuntimeError("Force exception for test")


@pytest.mark.asyncio
async def test_green_mode_kwarg_for_proxy_methods():
    with DeviceTestContext(ServerTest, device_name="test/test_device/1"):
        dev = await get_device_proxy("test/test_device/1", green_mode=GreenMode.Asyncio)

        # standard behavior for single attribute
        value = 12
        async_single_write_id = await dev.write_attribute_asynch("attr1", value)
        time.sleep(A_BIT)
        await dev.write_attribute_reply(async_single_write_id)

        async_single_read_id = await dev.read_attribute_asynch("attr1")
        time.sleep(A_BIT)
        attr = await dev.read_attribute_reply(async_single_read_id)
        assert value == attr.value

        # standard behavior for multiple attributes
        value = 34
        async_multiple_write_id = await dev.write_attributes_asynch([("attr1", value)])
        time.sleep(A_BIT)
        await dev.write_attributes_reply(async_multiple_write_id)

        async_multiple_read_id = await dev.read_attributes_asynch(["attr1"])
        time.sleep(A_BIT)
        attr = await dev.read_attributes_reply(async_multiple_read_id)
        assert value == attr[0].value

        # force sync execution for single attribute
        value = 56
        sync_single_write_id = dev.write_attribute_asynch(
            "attr1", value, green_mode=GreenMode.Synchronous
        )
        assert not isinstance(sync_single_write_id, asyncio.Future)
        time.sleep(A_BIT)
        dev.write_attribute_reply(
            sync_single_write_id, green_mode=GreenMode.Synchronous
        )

        sync_single_read_id = dev.read_attribute_asynch(
            "attr1", green_mode=GreenMode.Synchronous
        )
        assert not isinstance(sync_single_read_id, asyncio.Future)
        time.sleep(A_BIT)
        attr = dev.read_attribute_reply(
            sync_single_read_id, green_mode=GreenMode.Synchronous
        )
        assert value == attr.value

        # force sync execution for multiple attributes
        value = 78
        sync_multiple_write_id = dev.write_attributes_asynch(
            [("attr1", value)], green_mode=GreenMode.Synchronous
        )
        assert not isinstance(sync_multiple_write_id, asyncio.Future)
        time.sleep(A_BIT)
        dev.write_attributes_reply(
            sync_multiple_write_id, green_mode=GreenMode.Synchronous
        )

        sync_multiple_read_id = dev.read_attributes_asynch(
            ["attr1"], green_mode=GreenMode.Synchronous
        )
        assert not isinstance(sync_multiple_read_id, asyncio.Future)
        time.sleep(A_BIT)
        attr = dev.read_attributes_reply(
            sync_multiple_read_id, green_mode=GreenMode.Synchronous
        )
        assert value == attr[0].value


def test_async_write_with_attr_info():
    with DeviceTestContext(ServerTest) as proxy:

        attr_info = proxy.get_attribute_config_ex(["attr1", "attr2"])
        # reading single attribute with attr_info (no additional IO to fetch attr info during write method)
        value = 12
        async_single_write_id = proxy.write_attribute_asynch(attr_info[0], value)
        time.sleep(A_BIT)
        proxy.write_attribute_reply(async_single_write_id)

        async_single_read_id = proxy.read_attribute_asynch("attr1")
        time.sleep(A_BIT)
        attr = proxy.read_attribute_reply(async_single_read_id)
        assert value == attr.value

        # standard behavior for multiple attributes
        values = [34, 56]
        async_multiple_write_id = proxy.write_attributes_asynch(
            [(attr_info[0], values[0]), [attr_info[1], values[1]]]
        )
        time.sleep(A_BIT)
        proxy.write_attributes_reply(async_multiple_write_id)

        async_multiple_read_id = proxy.read_attributes_asynch(["attr1", "attr2"])
        time.sleep(A_BIT)
        attr = proxy.read_attributes_reply(async_multiple_read_id)
        assert values[0] == attr[0].value
        assert values[1] == attr[1].value


def test_async_attribute_polled():
    with DeviceTestContext(ServerTest) as proxy:
        # asynchronous write/read of single attribute
        single_write_id = proxy.write_attribute_asynch("attr1", 123)
        time.sleep(A_BIT)
        proxy.write_attribute_reply(single_write_id)

        single_read_id = proxy.read_attribute_asynch("attr1")
        time.sleep(A_BIT)
        attr = proxy.read_attribute_reply(single_read_id)
        assert 123 == attr.value

        # asynchronous write/read of multiple attributes
        multiple_write_id = proxy.write_attributes_asynch(
            [("attr1", 456), ("attr2", 789)]
        )
        time.sleep(A_BIT)
        proxy.write_attributes_reply(multiple_write_id)

        multiple_read_id = proxy.read_attributes_asynch(["attr1", "attr2"])
        time.sleep(A_BIT)
        attrs = proxy.read_attributes_reply(multiple_read_id)
        assert [456, 789] == [attr.value for attr in attrs]


def test_async_attribute_polled_no_return_value_or_exception():
    with DeviceTestContext(ServerTest) as proxy:
        read_id = proxy.read_attribute_asynch("attr_no_value")
        with pytest.raises(DevFailed, match="API_AttrValueNotSet"):
            proxy.read_attribute_reply(read_id, poll_timeout=int(A_BIT * 1000))

        read_id = proxy.read_attribute_asynch("attr_exception")
        with pytest.raises(DevFailed, match="RuntimeError"):
            proxy.read_attribute_reply(read_id, poll_timeout=int(A_BIT * 1000))

        multiple_read_id = proxy.read_attributes_asynch(
            ["attr1", "attr_no_value", "attr_exception"]
        )
        attr1, attr_no_value, attr_exception = proxy.read_attributes_reply(
            multiple_read_id, poll_timeout=int(A_BIT * 1000)
        )
        assert attr1.value == 100
        assert not attr1.has_failed
        assert attr_no_value.has_failed
        assert attr_exception.has_failed


@pytest.mark.parametrize("model", ["poll", "push"])
def test_async_attribute_with_callback(model):
    callbacks = []

    def write_callback(attr_written_event: AttrWrittenEvent):
        assert_close(attr_written_event.attr_names, ["attr1", "attr2"])
        assert attr_written_event.device == proxy
        assert not attr_written_event.err
        callbacks.append(attr_written_event)

    def read_callback(attr_read_event: AttrReadEvent):
        assert_close(attr_read_event.attr_names, ["attr1", "attr2"])
        assert_close([attr.value for attr in attr_read_event.argout], [123, 456])
        assert attr_read_event.device == proxy
        assert not attr_read_event.err
        callbacks.append(attr_read_event)

    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(
        cb_sub_model.PUSH_CALLBACK if model == "push" else cb_sub_model.PULL_CALLBACK
    )

    with DeviceTestContext(ServerTest) as proxy:
        # asynchronous write/read of multiple attributes
        proxy.write_attributes_asynch([("attr1", 123), ("attr2", 456)], write_callback)
        time.sleep(A_BIT)
        proxy.read_attributes_asynch(["attr1", "attr2"], read_callback)

        if model == "poll":
            api_util.get_asynch_replies(500)
        else:
            time.sleep(0.5)

        assert len(callbacks) == 2


def test_async_command_polled():
    class TestDevice(Device):
        @command(dtype_in=int, dtype_out=int)
        def identity(self, arg):
            return arg

    with DeviceTestContext(TestDevice) as proxy:
        eid = proxy.command_inout_asynch("identity", 123)
        assert 123 == proxy.command_inout_reply(eid, timeout=500)


class ServerForAsynchClients(Device):
    @command(dtype_in=int, dtype_out=int)
    def cmd_ok(self, arg):
        return arg

    @command(dtype_in=int, dtype_out=int)
    def cmd_timeout(self, arg):
        time.sleep(0.2)
        return arg

    @command(dtype_in=int, dtype_out=int)
    def cmd_exception(self, arg):
        raise Exception("Intentional exception")

    @attribute(dtype=int)
    def attr_ok(self):
        return 123

    @attr_ok.setter
    def attr_ok(self, value):
        pass

    @attribute(dtype=int)
    def attr_timeout(self):
        time.sleep(0.2)
        return 123

    @attr_timeout.setter
    def attr_timeout(self, value):
        time.sleep(0.2)
        pass

    @attribute(dtype=int)
    def attr_exception(self):
        raise Exception("Intentional exception")

    @attr_exception.setter
    def attr_exception(self, value):
        raise Exception("Intentional exception")


@pytest.mark.parametrize(
    "cmd,argin,argout,err,err_str",
    [
        ("cmd_ok", 123, 123, False, ""),
        ("cmd_timeout", 123, None, True, "TRANSIENT_CallTimedout"),
        ("cmd_exception", 123, None, True, "Intentional exception"),
    ],
)
def test_async_command_with_polled_callback(cmd, argin, argout, err, err_str):
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PULL_CALLBACK)

    with DeviceTestContext(ServerForAsynchClients, process=True) as proxy:
        future = Future()
        proxy.set_timeout_millis(
            150
        )  # this timeout does not have any influence on get_asynch_replies behaviour
        proxy.command_inout_asynch(cmd, argin, future.set_result)
        api_util.get_asynch_replies(500)  # this timeout is the one that matters
        result: CmdDoneEvent = future.result()
        assert result.err == err
        if not err:
            assert result.argout == argout
            assert len(result.errors) == 0
        else:
            with pytest.raises(DevFailed, match="API_EmptyDeviceData"):
                _ = result.argout
            assert err_str in str(result.errors[0])


@dataclass
class AttrReading:
    has_failed: bool
    value: Union[int, None]


@pytest.mark.parametrize(
    "attr,argout,err",
    [
        ("attr_ok", [AttrReading(has_failed=False, value=123)], False),
        ("attr_timeout", [], True),
        ("attr_exception", [AttrReading(has_failed=True, value=None)], True),
    ],
)
def test_async_attribute_read_with_polled_callback(attr, argout, err):
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PULL_CALLBACK)

    with DeviceTestContext(ServerForAsynchClients, process=True) as proxy:
        future = Future()
        proxy.set_timeout_millis(150)
        proxy.read_attribute_asynch(attr, future.set_result)
        api_util.get_asynch_replies(500)
        result: AttrReadEvent = future.result()
        assert result.err == err
        assert len(result.argout) == len(argout)
        # compare values of returned attributes
        for actual, expected in zip(result.argout, argout):
            assert actual.has_failed == expected.has_failed
            assert actual.value == expected.value


@pytest.mark.parametrize(
    "attr,err,num_errors,err_str",
    [
        ("attr_ok", False, 0, ""),
        ("attr_timeout", True, 0, ""),
        ("attr_exception", True, 1, "Intentional exception"),
    ],
)
def test_async_attribute_write_with_polled_callback(attr, err, num_errors, err_str):
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PULL_CALLBACK)

    with DeviceTestContext(ServerForAsynchClients, process=True) as proxy:
        future = Future()
        proxy.set_timeout_millis(150)
        proxy.write_attribute_asynch(attr, 123, future.set_result)
        # Future should be emtpy if we have not pulled replies
        with pytest.raises((concurrent.futures.TimeoutError, TimeoutError)):
            _ = future.result(timeout=0.1)

        api_util.get_asynch_replies(500)
        result: AttrWrittenEvent = future.result(timeout=0.1)

        assert result.err == err
        assert len(result.errors.err_list) == num_errors
        if num_errors > 0:
            assert err_str in str(result.errors.err_list[0].err_stack[0])


@pytest.mark.parametrize(
    "cmd,argin,argout,err,err_str",
    [
        ("cmd_ok", 123, 123, False, ""),
        ("cmd_timeout", 123, None, True, "TRANSIENT_CallTimedout"),
        ("cmd_exception", 123, None, True, "Intentional exception"),
    ],
)
def test_async_command_with_pushed_callback(cmd, argin, argout, err, err_str):
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PUSH_CALLBACK)

    with DeviceTestContext(ServerForAsynchClients, process=True) as proxy:
        future = Future()
        proxy.set_timeout_millis(100)
        proxy.command_inout_asynch(cmd, argin, future.set_result)
        result: CmdDoneEvent = future.result(timeout=5)
        assert result.err == err
        if not err:
            assert result.argout == argout
            assert len(result.errors) == 0
        else:
            with pytest.raises(DevFailed, match="API_EmptyDeviceData"):
                _ = result.argout
            assert err_str in str(result.errors[0])


@pytest.mark.parametrize(
    "attr,argout,err",
    [
        ("attr_ok", [AttrReading(has_failed=False, value=123)], False),
        ("attr_timeout", [], True),
        ("attr_exception", [AttrReading(has_failed=True, value=None)], True),
    ],
)
def test_async_attribute_read_with_pushed_callback(attr, argout, err):
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PUSH_CALLBACK)

    with DeviceTestContext(ServerForAsynchClients, process=True) as proxy:
        future = Future()
        proxy.set_timeout_millis(150)
        proxy.read_attribute_asynch(attr, future.set_result)
        result: AttrReadEvent = future.result(timeout=5)
        assert result.err == err
        assert len(result.argout) == len(argout)
        # compare values of returned attributes
        for actual, expected in zip(result.argout, argout):
            assert actual.has_failed == expected.has_failed
            assert actual.value == expected.value


@pytest.mark.parametrize(
    "attr,err,num_errors,err_str",
    [
        ("attr_ok", False, 0, ""),
        ("attr_timeout", True, 0, ""),
        ("attr_exception", True, 1, "Intentional exception"),
    ],
)
def test_async_attribute_write_with_pushed_callback(attr, err, num_errors, err_str):
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PUSH_CALLBACK)

    with DeviceTestContext(ServerForAsynchClients, process=True) as proxy:
        future = Future()
        proxy.set_timeout_millis(150)
        proxy.write_attribute_asynch(attr, 123, future.set_result)
        result: AttrWrittenEvent = future.result(timeout=5)
        assert result.err == err
        assert len(result.errors.err_list) == num_errors
        if num_errors > 0:
            assert err_str in str(result.errors.err_list[0].err_stack[0])


def test_async_exception_in_callback():
    api_util = ApiUtil.instance()
    api_util.set_asynch_cb_sub_model(cb_sub_model.PUSH_CALLBACK)

    def callback(_event):
        raise Exception("Some exception")

    with DeviceTestContext(ServerForAsynchClients) as proxy:
        proxy.read_attribute_asynch("attr_ok", callback)
        time.sleep(0.2)
