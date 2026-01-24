# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import os
import time
import warnings

import numpy as np
import pytest
import tango
import asyncio
import gevent.event
import concurrent.futures

from tango import AttrWriteType, DevFailed, GreenMode, get_device_proxy, DeviceProxy
from tango.asyncio_executor import AsyncioExecutor
from tango.device_server import get_worker
from tango.gevent_executor import GeventExecutor
from tango.green import SynchronousExecutor
from tango.server import Device
from tango.server import command, attribute, device_property
from tango.test_utils import (
    DeviceTestContext,
    MultiDeviceTestContext,
    SimpleDevice,
    ClassicAPISimpleDeviceImpl,
    ClassicAPISimpleDeviceClass,
)


WINDOWS = "nt" in os.name


class Device1(Device):
    _attr1 = 100

    def init_device(self):
        super().init_device()
        self.set_state(tango.DevState.ON)

    @attribute(dtype=int, access=AttrWriteType.READ_WRITE)
    def attr1(self):
        return self._attr1

    def write_attr1(self, value):
        self._attr1 = value


class Device1GreenModeUnspecified(Device1):
    pass


class Device1Synchronous(Device1):
    green_mode = GreenMode.Synchronous


class Device1Gevent(Device1):
    green_mode = GreenMode.Gevent


class Device1Asyncio(Device):
    green_mode = GreenMode.Asyncio

    _attr1 = 100

    async def init_device(self):
        await super().init_device()
        self.set_state(tango.DevState.ON)

    @attribute(dtype=int, access=AttrWriteType.READ_WRITE)
    async def attr1(self):
        return self._attr1

    async def write_attr1(self, value):
        self._attr1 = value


class Device2(Device):
    _attr2 = 200

    def init_device(self):
        super().init_device()
        self.set_state(tango.DevState.ON)

    @attribute
    def attr2(self):
        return self._attr2


class Device2GreenModeUnspecified(Device2):
    pass


class Device2Synchronous(Device2):
    green_mode = GreenMode.Synchronous


class Device2Gevent(Device2):
    green_mode = GreenMode.Gevent


class Device2Asyncio(Device):
    green_mode = GreenMode.Asyncio

    _attr2 = 200

    async def init_device(self):
        await super().init_device()
        self.set_state(tango.DevState.ON)

    @attribute
    async def attr2(self):
        return self._attr2


class Device3(Device):
    def init_device(self):
        super().init_device()
        self.my_proxy = tango.DeviceProxy("test/device1/1")
        self.set_state(tango.DevState.ON)

    @attribute
    def attr3(self):
        return self.my_proxy.attr1


def test_no_warnings_in_test_context():
    class TestDevice(Device): ...

    warnings.filterwarnings("error")
    with DeviceTestContext(TestDevice):
        pass


def test_single_device(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device1Asyncio):
            pass

    else:

        class TestDevice(Device1):
            green_mode = server_green_mode

    with DeviceTestContext(TestDevice) as proxy:
        assert proxy.attr1 == 100


def test_single_device_old_api():
    with DeviceTestContext(
        ClassicAPISimpleDeviceImpl, ClassicAPISimpleDeviceClass
    ) as proxy:
        assert proxy.attr1 == 100


def test_nested_single_device_in_same_process_failure():
    # Nesting not recommended - use MultiDeviceTestContext
    with DeviceTestContext(Device1, process=False):
        with pytest.raises(DevFailed):
            with DeviceTestContext(Device2, process=False):
                pass


def test_nested_single_device_in_different_processes_success_without_short_names():
    # Nesting not recommended - use MultiDeviceTestContext
    with DeviceTestContext(Device1, process=True) as proxy1:
        with DeviceTestContext(Device2, process=True) as proxy2:
            assert proxy1.attr1 == 100
            assert proxy2.attr2 == 200


def test_nested_single_device_in_different_processes_failure_with_short_names():
    # Nesting not recommended - use MultiDeviceTestContext
    with DeviceTestContext(Device1, device_name="test/nodb/1", process=True):
        with DeviceTestContext(Device2, process=True):
            with pytest.raises(DevFailed):
                DeviceProxy("test/nodb/1")


@pytest.mark.parametrize(
    "class_field, device",
    [
        (SimpleDevice, SimpleDevice),
        ("tango.test_utils.SimpleDevice", SimpleDevice),
        (
            (
                "tango.test_utils.ClassicAPISimpleDeviceClass",
                "tango.test_utils.ClassicAPISimpleDeviceImpl",
            ),
            ClassicAPISimpleDeviceImpl,
        ),
        (
            (
                "tango.test_utils.ClassicAPISimpleDeviceClass",
                ClassicAPISimpleDeviceImpl,
            ),
            ClassicAPISimpleDeviceImpl,
        ),
        (
            (
                ClassicAPISimpleDeviceClass,
                "tango.test_utils.ClassicAPISimpleDeviceImpl",
            ),
            ClassicAPISimpleDeviceImpl,
        ),
        (
            (ClassicAPISimpleDeviceClass, ClassicAPISimpleDeviceImpl),
            ClassicAPISimpleDeviceImpl,
        ),
    ],
)
def test_multi_devices_info(class_field, device):
    devices_info = ({"class": class_field, "devices": [{"name": "test/device1/1"}]},)

    dev_class = device if isinstance(device, str) else device.__name__

    with MultiDeviceTestContext(devices_info) as context:
        proxy1 = context.get_device("test/device1/1")
        assert proxy1.info().dev_class == dev_class


def test_multi_with_single_device(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice(Device1Asyncio):
            pass

    else:

        class TestDevice(Device1):
            green_mode = server_green_mode

    devices_info = ({"class": TestDevice, "devices": [{"name": "test/device1/1"}]},)

    with MultiDeviceTestContext(devices_info) as context:
        proxy1 = context.get_device("test/device1/1")
        assert proxy1.attr1 == 100


def test_multi_with_single_device_old_api():
    devices_info = (
        {
            "class": (ClassicAPISimpleDeviceClass, ClassicAPISimpleDeviceImpl),
            "devices": [{"name": "test/device1/1"}],
        },
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy1 = context.get_device("test/device1/1")
        assert proxy1.attr1 == 100


def test_multi_with_two_devices(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice1(Device1Asyncio):
            pass

        class TestDevice2(Device2Asyncio):
            pass

    else:

        class TestDevice1(Device1):
            green_mode = server_green_mode

        class TestDevice2(Device2):
            green_mode = server_green_mode

    devices_info = (
        {"class": TestDevice1, "devices": [{"name": "test/device1/1"}]},
        {"class": TestDevice2, "devices": [{"name": "test/device2/1"}]},
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy1 = context.get_device("test/device1/1")
        proxy2 = context.get_device("test/device2/1")
        assert proxy1.State() == tango.DevState.ON
        assert proxy2.State() == tango.DevState.ON
        assert proxy1.attr1 == 100
        assert proxy2.attr2 == 200


@pytest.mark.parametrize(
    "first_type, second_type, exception_type",
    [
        (Device1GreenModeUnspecified, Device2GreenModeUnspecified, None),
        (Device1GreenModeUnspecified, Device2Synchronous, None),
        (Device1GreenModeUnspecified, Device2Gevent, ValueError),
        (Device1GreenModeUnspecified, Device2Asyncio, ValueError),
        (Device1Synchronous, Device2GreenModeUnspecified, None),
        (Device1Synchronous, Device2Synchronous, None),
        (Device1Synchronous, Device2Gevent, ValueError),
        (Device1Synchronous, Device2Asyncio, ValueError),
        (Device1Asyncio, Device2GreenModeUnspecified, ValueError),
        (Device1Asyncio, Device2Synchronous, ValueError),
        (Device1Asyncio, Device2Gevent, ValueError),
        (Device1Asyncio, Device2Asyncio, None),
        (Device1Gevent, Device2GreenModeUnspecified, ValueError),
        (Device1Gevent, Device2Synchronous, ValueError),
        (Device1Gevent, Device2Gevent, None),
        (Device1Gevent, Device2Asyncio, ValueError),
    ],
)
def test_multi_with_mixed_device_green_modes(first_type, second_type, exception_type):
    devices_info = (
        {"class": first_type, "devices": [{"name": "test/device1/1"}]},
        {"class": second_type, "devices": [{"name": "test/device2/1"}]},
    )

    if exception_type is None:
        with MultiDeviceTestContext(devices_info):
            pass
    else:
        with pytest.raises(exception_type, match=r"mixed green mode"):
            with MultiDeviceTestContext(devices_info):
                pass


def stringify_green_mode(value):
    if isinstance(value, GreenMode):
        return str(value)
    else:
        return None


@pytest.mark.parametrize(
    "device_type, green_mode, global_mode, exception_type, executor_type",
    [
        # If a device specifies its green mode explicitly, then both
        # green_mode kwarg and global green mode are ignored. The device must use its specified mode.
        (
            Device1Synchronous,
            GreenMode.Asyncio,
            GreenMode.Asyncio,
            None,
            SynchronousExecutor,
        ),
        (
            Device1Synchronous,
            GreenMode.Gevent,
            GreenMode.Gevent,
            None,
            SynchronousExecutor,
        ),
        (
            Device1Asyncio,
            GreenMode.Synchronous,
            GreenMode.Synchronous,
            None,
            AsyncioExecutor,
        ),
        (Device1Asyncio, GreenMode.Gevent, GreenMode.Gevent, None, AsyncioExecutor),
        (
            Device1Gevent,
            GreenMode.Synchronous,
            GreenMode.Synchronous,
            None,
            GeventExecutor,
        ),
        (Device1Gevent, GreenMode.Asyncio, GreenMode.Asyncio, None, GeventExecutor),
        # If device doesn't specify its green mode, but green_mode kwarg is provided,
        # then we use green_mode kwarg
        (
            Device1GreenModeUnspecified,
            GreenMode.Synchronous,
            GreenMode.Asyncio,
            None,
            SynchronousExecutor,
        ),
        (
            Device1GreenModeUnspecified,
            GreenMode.Synchronous,
            GreenMode.Gevent,
            None,
            SynchronousExecutor,
        ),
        (
            Device1GreenModeUnspecified,
            GreenMode.Gevent,
            GreenMode.Synchronous,
            None,
            GeventExecutor,
        ),
        (
            Device1GreenModeUnspecified,
            GreenMode.Gevent,
            GreenMode.Asyncio,
            None,
            GeventExecutor,
        ),
        # Finally, if neither device green mode nor green_mode kwarg are specified, then use global mode instead.
        # (currently only works for synchronous mode - see unsupported modes below)
        (
            Device1GreenModeUnspecified,
            None,
            GreenMode.Synchronous,
            None,
            SynchronousExecutor,
        ),
        # Deprecated modes - starting from PyTango 10 it is deprecated
        # to modify sync servers to async "on the fly".
        # All base methods should be defined with "async def" instead.
        (
            Device1GreenModeUnspecified,
            GreenMode.Asyncio,
            GreenMode.Synchronous,
            DeprecationWarning,
            AsyncioExecutor,
        ),
        (
            Device1GreenModeUnspecified,
            GreenMode.Asyncio,
            GreenMode.Gevent,
            DeprecationWarning,
            AsyncioExecutor,
        ),
        # Unsupported modes - device servers with the following combinations
        # fail to start up. The cause is unknown. This could be fixed in the future.
        (
            Device1GreenModeUnspecified,
            None,
            GreenMode.Asyncio,
            RuntimeError,
            AsyncioExecutor,
        ),
        (
            Device1GreenModeUnspecified,
            None,
            GreenMode.Gevent,
            RuntimeError,
            GeventExecutor,
        ),
        (Device1Asyncio, None, GreenMode.Asyncio, RuntimeError, AsyncioExecutor),
        (Device1Gevent, None, GreenMode.Gevent, RuntimeError, GeventExecutor),
    ],
    ids=stringify_green_mode,
)
def test_green_modes_in_device_kwarg_and_global(
    device_type, green_mode, global_mode, exception_type, executor_type
):
    if WINDOWS and exception_type is not None:
        pytest.skip("Skip test that hangs on Windows")

    old_green_mode = tango.get_green_mode()
    try:
        tango.set_green_mode(global_mode)

        if exception_type is None:
            with DeviceTestContext(device_type, green_mode=green_mode):
                pass
        elif exception_type is DeprecationWarning:
            with pytest.warns((DeprecationWarning, RuntimeWarning)):
                with DeviceTestContext(device_type, green_mode=green_mode):
                    pass
        else:
            with pytest.raises(exception_type, match=r"stuck at init"):
                with DeviceTestContext(device_type, green_mode=green_mode, timeout=0.5):
                    pass
        assert type(get_worker()) is executor_type

    finally:
        tango.set_green_mode(old_green_mode)


def test_multi_with_async_devices_initialised():
    devices_info = (
        {"class": Device1Asyncio, "devices": [{"name": "test/device1/1"}]},
        {"class": Device2Asyncio, "devices": [{"name": "test/device2/1"}]},
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy1 = context.get_device("test/device1/1")
        proxy2 = context.get_device("test/device2/1")
        assert proxy1.State() == tango.DevState.ON
        assert proxy2.State() == tango.DevState.ON
        assert proxy1.attr1 == 100
        assert proxy2.attr2 == 200


def test_multi_device_access_via_test_context_methods():
    devices_info = (
        {"class": Device1, "devices": [{"name": "test/device1/1"}]},
        {"class": Device2, "devices": [{"name": "test/device2/2"}]},
    )

    with MultiDeviceTestContext(devices_info) as context:
        device_access1 = context.get_device_access("test/device1/1")
        device_access2 = context.get_device_access("test/device2/2")
        server_access = context.get_server_access()
        assert "test/device1/1" in device_access1
        assert "test/device2/2" in device_access2
        assert context.server_name in server_access
        proxy1 = tango.DeviceProxy(device_access1)
        proxy2 = tango.DeviceProxy(device_access2)
        proxy_server = tango.DeviceProxy(server_access)
        assert proxy1.attr1 == 100
        assert proxy2.attr2 == 200
        assert proxy_server.State() == tango.DevState.ON


def test_multi_short_name_device_proxy_access_without_tango_db():
    devices_info = ({"class": Device1, "devices": [{"name": "test/device1/1"}]},)

    with MultiDeviceTestContext(devices_info, process=True):
        proxy1 = tango.DeviceProxy("test/device1/1")
        assert proxy1.name() == "test/device1/1"
        assert proxy1.attr1 == 100


def test_multi_short_name_device_proxy_with_dependencies_access_without_tango_db():
    devices_info = (
        {"class": Device1, "devices": [{"name": "test/device1/1"}]},
        {"class": Device3, "devices": [{"name": "test/device3/3"}]},
    )

    with MultiDeviceTestContext(devices_info, process=True):
        proxy1 = tango.DeviceProxy("test/device1/1")
        proxy3 = tango.DeviceProxy("test/device3/3")
        assert proxy1.name() == "test/device1/1"
        assert proxy1.attr1 == 100
        assert proxy3.name() == "test/device3/3"
        assert proxy3.attr3 == 100
        proxy1.attr1 = 300
        assert proxy3.attr3 == 300


def test_multi_short_name_attribute_proxy_access_without_tango_db():
    devices_info = ({"class": Device1, "devices": [{"name": "test/device1/1"}]},)

    with MultiDeviceTestContext(devices_info):
        attr1 = tango.AttributeProxy("test/device1/1/attr1")
        assert attr1.name() == "attr1"
        assert attr1.read().value == 100


def test_single_short_name_device_proxy_access_without_tango_db():
    with DeviceTestContext(Device1, device_name="test/device1/1"):
        proxy1 = tango.DeviceProxy("test/device1/1")
        assert proxy1.name() == "test/device1/1"
        assert proxy1.attr1 == 100


def test_single_short_name_attribute_proxy_access_without_tango_db():
    with DeviceTestContext(Device1, device_name="test/device1/1"):
        attr1 = tango.AttributeProxy("test/device1/1/attr1")
        assert attr1.name() == "attr1"
        assert attr1.read().value == 100


def test_multi_short_name_access_fails_if_override_disabled():
    devices_info = ({"class": Device1, "devices": [{"name": "test/device1/a"}]},)

    context = MultiDeviceTestContext(devices_info, process=True)
    context.enable_test_context_tango_host_override = False
    context.start()
    try:
        with pytest.raises(DevFailed):
            _ = tango.DeviceProxy("test/device1/a")
    finally:
        context.stop()


def test_multi_device_proxy_cached():
    devices_info = ({"class": Device1, "devices": [{"name": "test/device1/1"}]},)

    with MultiDeviceTestContext(devices_info) as context:
        device1_first = context.get_device("test/device1/1")
        device1_second = context.get_device("test/device1/1")
        assert device1_first is device1_second


def test_multi_with_two_devices_with_properties(server_green_mode):
    if server_green_mode == GreenMode.Asyncio:

        class TestDevice1(Device):
            green_mode = server_green_mode

            prop1 = device_property(dtype=str)

            @command(dtype_out=str)
            async def get_prop1(self):
                return self.prop1

        class TestDevice2(Device):
            green_mode = server_green_mode

            prop2 = device_property(dtype=int)

            @command(dtype_out=int)
            async def get_prop2(self):
                return self.prop2

    else:

        class TestDevice1(Device):
            green_mode = server_green_mode

            prop1 = device_property(dtype=str)

            @command(dtype_out=str)
            def get_prop1(self):
                return self.prop1

        class TestDevice2(Device):
            green_mode = server_green_mode

            prop2 = device_property(dtype=int)

            @command(dtype_out=int)
            def get_prop2(self):
                return self.prop2

    devices_info = (
        {
            "class": TestDevice1,
            "devices": [{"name": "test/device1/1", "properties": {"prop1": "abcd"}}],
        },
        {
            "class": TestDevice2,
            "devices": [{"name": "test/device2/2", "properties": {"prop2": 5555}}],
        },
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy1 = context.get_device("test/device1/1")
        proxy2 = context.get_device("test/device2/2")
        assert proxy1.get_prop1() == "abcd"
        assert proxy2.get_prop2() == 5555


def test_multi_raises_on_invalid_file_database_properties():
    class TestDevice(Device):
        empty = device_property(dtype=(str,))

    with pytest.raises(RuntimeError, match="FileDatabase"):
        with DeviceTestContext(TestDevice, properties={"empty": []}):
            pass


@pytest.fixture(
    # Per test we have the input config tuple, and then the expected exception type
    params=[
        # empty config
        [tuple(), IndexError],
        # missing/invalid keys
        [({"not-class": Device1, "devices": [{"name": "test/device1/1"}]},), KeyError],
        [({"class": Device1, "not-devices": [{"name": "test/device1/1"}]},), KeyError],
        [({"class": Device1, "devices": [{"not-name": "test/device1/1"}]},), KeyError],
        # duplicate class
        [
            (
                {"class": Device1, "devices": [{"name": "test/device1/1"}]},
                {"class": Device1, "devices": [{"name": "test/device1/2"}]},
            ),
            ValueError,
        ],
        # mixing old "classic" API and new high level API
        [
            (
                {"class": Device1, "devices": [{"name": "test/device1/1"}]},
                {
                    "class": (ClassicAPISimpleDeviceClass, ClassicAPISimpleDeviceImpl),
                    "devices": [{"name": "test/device1/2"}],
                },
            ),
            ValueError,
        ],
        # mixing green modes
        [
            (
                {"class": Device1Synchronous, "devices": [{"name": "test/device1/1"}]},
                {"class": Device1Gevent, "devices": [{"name": "test/device1/2"}]},
            ),
            ValueError,
        ],
    ]
)
def bad_multi_device_config(request):
    return request.param


def test_multi_bad_config_fails(bad_multi_device_config):
    bad_config, expected_error = bad_multi_device_config
    with pytest.raises(expected_error):
        with MultiDeviceTestContext(bad_config):
            pass


@pytest.fixture()
def memorized_attribute_test_device_factory():
    """
    Returns a test device factory that provides a test device with an
    attribute that is memorized or not, according to its boolean
    argument
    """

    def _factory(is_attribute_memorized):
        class _Device(Device):
            def init_device(self):
                self._attr_value = 0

            attr = attribute(
                access=AttrWriteType.READ_WRITE,
                memorized=is_attribute_memorized,
                hw_memorized=is_attribute_memorized,
            )

            def read_attr(self):
                return self._attr_value

            def write_attr(self, value):
                self._attr_value = value

        return _Device

    return _factory


@pytest.mark.parametrize(
    "is_attribute_memorized, memorized_value, expected_value",
    [
        (False, None, 0),
        (False, "1", 0),
        (True, None, 0),
        (True, "1", 1),
    ],
)
def test_multi_with_memorized_attribute_values(
    memorized_attribute_test_device_factory,
    is_attribute_memorized,
    memorized_value,
    expected_value,
):
    TestDevice = memorized_attribute_test_device_factory(is_attribute_memorized)

    device_info = {"name": "test/device1/1"}
    if memorized_value is not None:
        device_info["memorized"] = {"attr": memorized_value}

    devices_info = ({"class": TestDevice, "devices": [device_info]},)

    with MultiDeviceTestContext(devices_info) as context:
        proxy = context.get_device("test/device1/1")
        assert proxy.attr == expected_value


@pytest.mark.parametrize(
    "is_attribute_memorized, memorized_value, expected_value",
    [
        (False, None, 0),
        (False, 1, 0),
        (True, None, 0),
        (True, 1, 1),
    ],
)
def test_single_with_memorized_attribute_values(
    memorized_attribute_test_device_factory,
    is_attribute_memorized,
    memorized_value,
    expected_value,
):
    TestDevice = memorized_attribute_test_device_factory(is_attribute_memorized)

    kwargs = (
        {"memorized": {"attr": memorized_value}} if memorized_value is not None else {}
    )

    with DeviceTestContext(TestDevice, **kwargs) as proxy:
        assert proxy.attr == expected_value


@pytest.mark.parametrize(
    "property_type, property_value, expected_outcome",
    [
        (str, {"prop": ""}, " "),
        ((str,), {"prop": ["", ""]}, (" ", " ")),
        ((str,), {"prop": np.array(["", ""])}, (" ", " ")),
    ],
)
def test_empty_string_property_bug(property_type, property_value, expected_outcome):
    class TestDevice(Device):
        prop = device_property(
            dtype=property_type,
        )

        @attribute(dtype=property_type, max_dim_x=10)
        def attr(self):
            return self.prop

    with DeviceTestContext(TestDevice, properties=property_value) as proxy:
        assert proxy.attr == expected_outcome


class AsyncDevice(Device):
    green_mode = GreenMode.Asyncio
    _value = 0
    _my_proxy = None

    @attribute
    async def value(self):
        return self._value

    @command(dtype_out="DevShort")
    async def increment(self):
        await asyncio.sleep(0.1)
        self._value += 1
        return self._value

    @attribute(dtype=str)
    async def my_name(self):
        return self.get_name()

    @attribute(dtype=str)
    async def child_name(self):
        attr = await self._my_proxy.read_attribute("my_name")
        return attr.value

    @command(dtype_in="DevString")
    async def connect_to_device(self, fqdn):
        proxy_future = get_device_proxy(fqdn, green_mode=GreenMode.Asyncio)
        assert isinstance(proxy_future, asyncio.Future)

        self._my_proxy = await proxy_future
        assert isinstance(self._my_proxy, DeviceProxy)


@pytest.mark.asyncio
@pytest.mark.parametrize("process", [True, False])
async def test_test_context_async_device_proxy(process):
    config = ({"class": AsyncDevice, "devices": [{"name": "test/device/1"}]},)

    with MultiDeviceTestContext(config, process=process) as context:
        fq_name = context.get_device_access("test/device/1")

        proxy_future = get_device_proxy(fq_name, green_mode=GreenMode.Asyncio)
        assert isinstance(proxy_future, asyncio.Future)

        proxy = await proxy_future
        assert isinstance(proxy, DeviceProxy)

        assert proxy.get_green_mode() == GreenMode.Asyncio

        # Ensure that we use the correct access method for the DeviceProxy call
        value = await proxy.increment()
        assert value == 1

        # Ensure that we use the correct access method for the DeviceProxy call
        attr = await proxy.read_attribute("value")
        assert attr.value == 1


@pytest.mark.asyncio
@pytest.mark.parametrize("process", [True, False])
async def test_test_context_multi_async_device_proxy(process):
    config = (
        {
            "class": AsyncDevice,
            "devices": [{"name": "test/device/main"}, {"name": "test/device/child"}],
        },
    )

    with MultiDeviceTestContext(config, process=process) as context:
        fq_name_main = context.get_device_access("test/device/main")
        fq_name_child = context.get_device_access("test/device/child")

        proxy_future_main = get_device_proxy(fq_name_main, green_mode=GreenMode.Asyncio)
        assert isinstance(proxy_future_main, asyncio.Future)

        proxy_main = await proxy_future_main
        assert isinstance(proxy_main, DeviceProxy)

        assert proxy_main.get_green_mode() == GreenMode.Asyncio

        proxy_future_child = get_device_proxy(
            fq_name_child, green_mode=GreenMode.Asyncio
        )
        assert isinstance(proxy_future_child, asyncio.Future)

        proxy_child = await proxy_future_child
        assert isinstance(proxy_child, DeviceProxy)

        # Ensure that we use the correct access method for the DeviceProxy call
        await proxy_main.connect_to_device(fq_name_child)

        attr = await proxy_main.read_attribute("my_name")
        assert attr.value == "test/device/main"

        attr = await proxy_main.read_attribute("child_name")
        assert attr.value == "test/device/child"


class FutureAndGeventDevice(Device):
    green_mode = None
    _value = 0

    @attribute
    def value(self):
        return self._value

    @command(dtype_out="DevShort")
    def increment(self):
        self._value += 1
        return self._value


@pytest.mark.parametrize(
    "test_green_mode", [GreenMode.Futures, GreenMode.Gevent], ids=str
)
@pytest.mark.parametrize("process", [True, False])
def test_test_context_future_and_gevent_device_proxy(test_green_mode, process):
    FutureAndGeventDevice.green_mode = test_green_mode

    if test_green_mode == GreenMode.Futures:
        accessor = "result"
        expected_type = concurrent.futures.Future
    elif test_green_mode == GreenMode.Gevent:
        accessor = "get"
        expected_type = gevent.event.AsyncResult
    else:
        raise RuntimeError("Wrong GreenMode")

    config = ({"class": FutureAndGeventDevice, "devices": [{"name": "test/device/1"}]},)

    with MultiDeviceTestContext(config, process=process) as context:
        fq_name = context.get_device_access("test/device/1")

        proxy_future = get_device_proxy(fq_name, green_mode=test_green_mode, wait=False)
        assert isinstance(proxy_future, expected_type)

        proxy = getattr(proxy_future, accessor)()
        assert isinstance(proxy, DeviceProxy)

        assert proxy.get_green_mode() == test_green_mode

        # Ensure that we use the correct access method for the DeviceProxy call
        value_future = proxy.increment(wait=False)
        assert isinstance(value_future, expected_type)
        assert getattr(value_future, accessor)() == 1

        # Ensure that we use the correct access method for the DeviceProxy call
        attr_future = proxy.read_attribute("value", wait=False)
        assert isinstance(attr_future, expected_type)
        assert attr_future.result().value == 1


class FwdServer(Device):
    fwd_attr = attribute(forwarded=True)


@pytest.mark.parametrize("process", [True, False])
def test_forwarded_attributes(process):
    pytest.xfail(
        "Does not work yet - see https://gitlab.com/tango-controls/cppTango/-/issues/796"
    )
    devices_info = (
        {"class": Device1, "devices": [{"name": "test/device1/1"}]},
        {
            "class": FwdServer,
            "devices": [
                {
                    "name": "test/fwdserver/1",
                    "root_atts": {"fwd_attr": "test/device1/1/attr1"},
                }
            ],
        },
    )

    with MultiDeviceTestContext(devices_info, process=process):
        proxy_root = tango.DeviceProxy("test/device1/1")
        proxy_fwd = tango.DeviceProxy("test/fwdserver/1")
        assert "fwd_attr" in proxy_fwd.get_attribute_list()
        assert proxy_fwd.fwd_attr == 100
        proxy_fwd.fwd_attr = 200
        assert proxy_root.attr1 == 200
        proxy_root.attr1 = 300
        assert proxy_fwd.fwd_attr == 300


class DeviceStuckOnExit(Device):

    def delete_device(self):
        while True:
            time.sleep(1)


def test_device_context_thread_raises_if_device_server_stuck():
    context = DeviceTestContext(DeviceStuckOnExit)
    context.start()
    assert context.thread.daemon
    assert context.thread.is_alive()
    context.timeout = 0.2
    with pytest.raises(RuntimeError, match="failed to exit cleanly"):
        context.stop()
    # (thread can't be killed, so still alive here - it is a daemon so cleaned up
    # when test framework exits)


def test_device_context_process_raises_and_exits_if_device_server_stuck():
    context = DeviceTestContext(DeviceStuckOnExit, process=True)
    context.start()
    assert not context.thread.daemon  # don't want daemon for subprocess - kill instead
    assert context.thread.is_alive()
    context.timeout = 0.2
    with pytest.raises(RuntimeError, match=r"failed to exit cleanly.*kill subprocess"):
        context.stop()
    assert not context.thread.is_alive()


@pytest.mark.parametrize("process", [False, True])
def test_device_context_completes_if_device_server_not_stuck(process):
    context = DeviceTestContext(Device, process=process)
    context.start()
    assert context.thread.is_alive()
    context.stop()
    assert not context.thread.is_alive()
