# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import inspect
import os
import threading
import time
from asyncio import sleep as asleep
from collections import namedtuple
from typing import ClassVar

import pytest

from tango import DevFailed, DeviceProxy, GreenMode
from tango.log4tango import (
    DebugIt,
    ErrorIt,
    FatalIt,
    InfoIt,
    LogIt,
    TangoStream,
    WarnIt,
)
from tango.server import Device, attribute, command
from tango.test_context import DeviceTestContext, MultiDeviceTestContext
from tango.test_utils import general_asyncio_decorator, general_decorator

# Constants
WINDOWS = "nt" in os.name

LogConsumerEntry = namedtuple(
    "LogConsumerEntry",
    ["timestamp", "level", "source", "message", "unused", "thread_id"],
)


def check_log(received_logs, device_name, log_level, method_name, arg, kwarg, ret, error):

    entry_log = LogConsumerEntry(*received_logs[-2])
    exit_log = LogConsumerEntry(*received_logs[-1])

    assert entry_log.source == "test/logdevice/1"
    assert exit_log.source == "test/logdevice/1"
    assert log_level == entry_log.level
    assert log_level == exit_log.level
    if kwarg != "":
        assert f"-> {device_name}.{method_name}({arg}, {kwarg})" == entry_log.message
    else:
        assert f"-> {device_name}.{method_name}({arg})" == entry_log.message
    if error != "":
        assert f"<- {device_name}.{method_name}() raised exception!" == exit_log.message
    elif ret != "":
        assert f"{ret} <- {device_name}.{method_name}()" == exit_log.message
    else:
        assert f"<- {device_name}.{method_name}()" == exit_log.message


class LogReceiver(Device):
    _received_logs: ClassVar[list] = []

    @command
    def log(self, str_in: list[str]):
        self._received_logs.append(str_in)

    @command
    def log_size(self) -> int:
        return len(self._received_logs)

    @command
    def check_last_log(self, data_to_compare: list[str,]):
        check_log(self._received_logs, *data_to_compare)
        self._received_logs = []


class AsyncLogReceiver(Device):
    green_mode = GreenMode.Asyncio

    _received_logs: ClassVar[list] = []

    @command
    async def log(self, str_in: list[str]):
        self._received_logs.append(str_in)

    @command
    async def log_size(self) -> int:
        return len(self._received_logs)

    @command
    async def check_last_log(self, data_to_compare: list[str,]):
        check_log(self._received_logs, *data_to_compare)
        self._received_logs = []


# if we do not pause in method, sometimes method out log can come earlier, than method in
method_pause = 0.01


class LogDevice(Device):
    @command
    @LogIt()
    def log_cmd(self):
        time.sleep(method_pause)

    @attribute
    @DebugIt()
    def debug_attr(self) -> int:
        time.sleep(method_pause)
        return 1

    @attribute
    @InfoIt()
    def info_attr(self) -> int:
        time.sleep(method_pause)
        return 1

    @attribute
    @WarnIt()
    def warn_attr(self) -> int:
        time.sleep(method_pause)
        return 1

    @attribute
    @ErrorIt()
    def error_attr(self) -> int:
        time.sleep(method_pause)
        return 1

    @attribute
    @FatalIt()
    def fatal_attr(self) -> int:
        time.sleep(method_pause)
        return 1

    @LogIt(show_kwargs=True, show_args=True, show_ret=True)
    def arg_method(self, arg: str, kwarg: str):
        time.sleep(method_pause)
        return arg + kwarg

    @command
    def arg_kwarg_test(self, test_long_arg: bool):
        if test_long_arg:
            self.arg_method("a" * 26, kwarg="b" * 26)
        else:
            self.arg_method("a", kwarg="b")

    @command
    @LogIt()
    def error_test(self):
        time.sleep(method_pause)
        raise RuntimeError("Test error!")


class AsyncLogDevice(Device):
    green_mode = GreenMode.Asyncio

    @command
    @LogIt()
    async def log_cmd(self):
        await asleep(method_pause)

    @LogIt(show_kwargs=True, show_args=True, show_ret=True)
    async def arg_method(self, arg: int, kwarg: int):
        await asleep(method_pause)
        return arg + kwarg

    @command
    async def arg_kwarg_test(self):
        await self.arg_method(1, kwarg=2)

    @command
    @LogIt()
    async def error_test(self):
        await asleep(method_pause)
        raise RuntimeError("Test error!")


delay = 0.1
max_attempts = 10


def check_logs(log_device, expected_log):
    attempt = 0
    while log_device.log_size() < 2 and attempt < max_attempts:
        attempt += 1
        time.sleep(delay)

    if log_device.log_size() < 2:
        raise RuntimeError(f"Cannot receive logs for {expected_log[0]}:{expected_log[2]}")

    log_device.check_last_log(expected_log)


devices_info = (
    {
        "class": LogReceiver,
        "devices": [
            {"name": "test/logreceiver/1"},
        ],
    },
    {
        "class": LogDevice,
        "devices": [
            {"name": "test/logdevice/1"},
        ],
    },
)


def test_logging_decorators():
    with MultiDeviceTestContext(devices_info) as context:
        test_device = DeviceProxy("test/logdevice/1")
        log_device = DeviceProxy("test/logreceiver/1")

        test_device.add_logging_target(f"device::{context.get_device_access('test/logreceiver/1')}")
        test_device.log_cmd()
        check_logs(log_device, ("LogDevice", "DEBUG", "log_cmd", "", "", "", ""))

        for log_level, attr in (
            ("DEBUG", "debug_attr"),
            ("WARN", "warn_attr"),
            ("ERROR", "error_attr"),
            ("FATAL", "fatal_attr"),
            ("INFO", "info_attr"),
        ):
            getattr(test_device, attr)
            check_logs(log_device, ("LogDevice", log_level, attr, "", "", "", ""))

        test_device.arg_kwarg_test(False)
        check_logs(
            log_device,
            ("LogDevice", "DEBUG", "arg_method", "'a'", "kwarg='b'", "'ab'", ""),
        )

        test_device.arg_kwarg_test(True)
        check_logs(
            log_device,
            (
                "LogDevice",
                "DEBUG",
                "arg_method",
                "'" + "a" * 19 + "[...]",
                "kwarg='" + "b" * 19 + "[...]",
                "'" + "a" * 19 + "[...]",
                "",
            ),
        )

        with pytest.raises(DevFailed):
            test_device.error_test()
        check_logs(log_device, ("LogDevice", "DEBUG", "error_test", "", "", "", "Test error!"))


async_devices_info = (
    {
        "class": AsyncLogReceiver,
        "devices": [
            {"name": "test/logreceiver/1"},
        ],
    },
    {
        "class": AsyncLogDevice,
        "devices": [
            {"name": "test/logdevice/1"},
        ],
    },
)


def test_async_logging_decorators():
    with MultiDeviceTestContext(async_devices_info) as context:
        log_emitter = DeviceProxy("test/logdevice/1")
        log_receiver = DeviceProxy("test/logreceiver/1")

        log_emitter.add_logging_target(f"device::{context.get_device_access('test/logreceiver/1')}")
        log_emitter.log_cmd()
        check_logs(log_receiver, ("AsyncLogDevice", "DEBUG", "log_cmd", "", "", "", ""))

        log_emitter.arg_kwarg_test()
        check_logs(
            log_receiver,
            ("AsyncLogDevice", "DEBUG", "arg_method", "1", "kwarg=2", "3", ""),
        )

        with pytest.raises(DevFailed):
            log_emitter.error_test()
        check_logs(
            log_receiver,
            ("AsyncLogDevice", "DEBUG", "error_test", "", "", "", "Test error!"),
        )


class Receiver:
    n_calls = 0

    def __call__(self, stream):
        self.n_calls += 1
        assert stream == "ab\nc"

    def check_calls(self, expected_n):
        assert self.n_calls == expected_n


def test_tango_stream():
    receiver = Receiver()
    stream = TangoStream(receiver)
    stream.write("ab")
    stream.write("\nc\n")

    receiver.check_calls(1)

    stream.flush()
    receiver.check_calls(1)

    stream.write("ab\nc")
    receiver.check_calls(2)


def test_logging(server_green_mode):
    log_received = threading.Event()

    if server_green_mode == GreenMode.Asyncio:

        class LogSourceDevice(Device):
            green_mode = server_green_mode
            _last_log_time = 0.0

            @command(dtype_in=("str",))
            async def log_fatal_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.fatal_stream(msg[0], msg[1])
                else:
                    self.fatal_stream(msg[0])

            @command(dtype_in=("str",))
            async def log_error_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.error_stream(msg[0], msg[1])
                else:
                    self.error_stream(msg[0])

            @command(dtype_in=("str",))
            async def log_warn_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.warn_stream(msg[0], msg[1])
                else:
                    self.warn_stream(msg[0])

            @command(dtype_in=("str",))
            async def log_info_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.info_stream(msg[0], msg[1])
                else:
                    self.info_stream(msg[0])

            @command(dtype_in=("str",))
            async def log_debug_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.debug_stream(msg[0], msg[1])
                else:
                    self.debug_stream(msg[0])

            @attribute(dtype=float)
            async def last_log_time(self):
                return self._last_log_time

        class LogConsumerDevice(Device):
            green_mode = server_green_mode
            _last_log_data: ClassVar[list] = []

            @command(dtype_in=("str",))
            async def Log(self, argin):
                self._last_log_data = argin
                log_received.set()

            @attribute(dtype=int)
            async def last_log_timestamp_ms(self):
                return int(self._last_log_data[0])

            @attribute(dtype=str)
            async def last_log_level(self):
                return self._last_log_data[1]

            @attribute(dtype=str)
            async def last_log_source(self):
                return self._last_log_data[2]

            @attribute(dtype=str)
            async def last_log_message(self):
                return self._last_log_data[3]

            @attribute(dtype=str)
            async def last_log_context_unused(self):
                return self._last_log_data[4]

            @attribute(dtype=str)
            async def last_log_thread_id(self):
                return self._last_log_data[5]

    else:

        class LogSourceDevice(Device):
            green_mode = server_green_mode
            _last_log_time = 0.0

            @command(dtype_in=("str",))
            def log_fatal_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.fatal_stream(msg[0], msg[1])
                else:
                    self.fatal_stream(msg[0])

            @command(dtype_in=("str",))
            def log_error_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.error_stream(msg[0], msg[1])
                else:
                    self.error_stream(msg[0])

            @command(dtype_in=("str",))
            def log_warn_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.warn_stream(msg[0], msg[1])
                else:
                    self.warn_stream(msg[0])

            @command(dtype_in=("str",))
            def log_info_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.info_stream(msg[0], msg[1])
                else:
                    self.info_stream(msg[0])

            @command(dtype_in=("str",))
            def log_debug_message(self, msg):
                self._last_log_time = time.time()
                if len(msg) > 1:
                    self.debug_stream(msg[0], msg[1])
                else:
                    self.debug_stream(msg[0])

            @attribute(dtype=float)
            def last_log_time(self):
                return self._last_log_time

        class LogConsumerDevice(Device):
            green_mode = server_green_mode
            _last_log_data: ClassVar[list] = []

            @command(dtype_in=("str",))
            def Log(self, argin):
                self._last_log_data = argin
                log_received.set()

            @attribute(dtype=int)
            def last_log_timestamp_ms(self):
                return int(self._last_log_data[0])

            @attribute(dtype=str)
            def last_log_level(self):
                return self._last_log_data[1]

            @attribute(dtype=str)
            def last_log_source(self):
                return self._last_log_data[2]

            @attribute(dtype=str)
            def last_log_message(self):
                return self._last_log_data[3]

            @attribute(dtype=str)
            def last_log_context_unused(self):
                return self._last_log_data[4]

            @attribute(dtype=str)
            def last_log_thread_id(self):
                return self._last_log_data[5]

    def assert_log_details_correct(level, msg):
        assert log_received.wait(0.5)
        _assert_log_time_close_enough()
        _assert_log_fields_correct_for_level(level, msg)
        log_received.clear()

    def _assert_log_time_close_enough():
        log_emit_time = proxy_source.last_log_time
        log_receive_time = proxy_consumer.last_log_timestamp_ms / 1000.0
        now = time.time()
        # cppTango logger time function may use a different
        # implementation to CPython's time.time().  This is
        # especially noticeable on Windows platforms.
        timer_implementation_tolerance = 0.020 if WINDOWS else 0.001
        min_time = log_emit_time - timer_implementation_tolerance
        max_time = now + timer_implementation_tolerance
        assert min_time <= log_receive_time <= max_time

    def _assert_log_fields_correct_for_level(level, msg):
        assert proxy_consumer.last_log_level == level.upper()
        assert proxy_consumer.last_log_source == "test/log/source"
        assert proxy_consumer.last_log_message == msg
        assert proxy_consumer.last_log_context_unused == ""
        assert len(proxy_consumer.last_log_thread_id) > 0

    devices_info = (
        {"class": LogSourceDevice, "devices": [{"name": "test/log/source"}]},
        {"class": LogConsumerDevice, "devices": [{"name": "test/log/consumer"}]},
    )

    with MultiDeviceTestContext(devices_info) as context:
        proxy_source = context.get_device("test/log/source")
        proxy_consumer = context.get_device("test/log/consumer")
        consumer_access = context.get_device_access("test/log/consumer")
        proxy_source.add_logging_target(f"device::{consumer_access}")

        for msg in ([""], [" with literal %s"], [" with string %s as arg", "foo"]):
            level = "fatal"
            log_msg = msg[:]
            log_msg[0] = "test " + level + msg[0]
            proxy_source.log_fatal_message(log_msg)
            check_log_msg = log_msg[0] % log_msg[1] if len(msg) > 1 else log_msg[0]
            assert_log_details_correct(level, check_log_msg)

            level = "error"
            log_msg = msg[:]
            log_msg[0] = "test " + level + msg[0]
            proxy_source.log_error_message(log_msg)
            check_log_msg = log_msg[0] % log_msg[1] if len(msg) > 1 else log_msg[0]
            assert_log_details_correct(level, check_log_msg)

            level = "warn"
            log_msg = msg[:]
            log_msg[0] = "test " + level + msg[0]
            proxy_source.log_warn_message(log_msg)
            check_log_msg = log_msg[0] % log_msg[1] if len(msg) > 1 else log_msg[0]
            assert_log_details_correct(level, check_log_msg)

            level = "info"
            log_msg = msg[:]
            log_msg[0] = "test " + level + msg[0]
            proxy_source.log_info_message(log_msg)
            check_log_msg = log_msg[0] % log_msg[1] if len(msg) > 1 else log_msg[0]
            assert_log_details_correct(level, check_log_msg)

            level = "debug"
            log_msg = msg[:]
            log_msg[0] = "test " + level + msg[0]
            proxy_source.log_debug_message(log_msg)
            check_log_msg = log_msg[0] % log_msg[1] if len(msg) > 1 else log_msg[0]
            assert_log_details_correct(level, check_log_msg)


@pytest.mark.skipif(
    not os.environ.get("PYTHONUNBUFFERED"),
    reason="This test requires PYTHONUNBUFFERED=1 to capture the outputs.",
)
def test_decorator_logging_source_location(server_green_mode, capfd):
    """Run decorated commands and attributes and verify that @InfoIt decorator
    always logs the correct location."""

    if server_green_mode == GreenMode.Asyncio:

        class InfoItDevice(Device):
            green_mode = server_green_mode

            @command(dtype_out=int)
            @InfoIt()
            async def decorated_command(self):
                return inspect.currentframe().f_lineno

            @command(dtype_out=int)
            async def run_decorated_method(self):
                return await self.decorated_method()

            @InfoIt()
            @general_asyncio_decorator
            async def decorated_method(self):
                return inspect.currentframe().f_lineno

            @attribute(dtype=int)
            @InfoIt()
            async def decorated_attribute(self):
                return inspect.currentframe().f_lineno

    else:

        class InfoItDevice(Device):
            green_mode = server_green_mode

            @command(dtype_out=int)
            @InfoIt()
            def decorated_command(self):
                return inspect.currentframe().f_lineno

            @command(dtype_out=int)
            def run_decorated_method(self):
                return self.decorated_method()

            @InfoIt()
            @general_decorator
            def decorated_method(self):
                return inspect.currentframe().f_lineno

            @attribute(dtype=int)
            @InfoIt()
            def decorated_attribute(self):
                return inspect.currentframe().f_lineno

    with DeviceTestContext(InfoItDevice, debug=3) as device:
        filename = os.path.basename(__file__)
        for cmd, method in [
            ("decorated_command", "decorated_command"),
            ("run_decorated_method", "decorated_method"),
        ]:
            lineno = device.command_inout(cmd) - 3
            out, _ = capfd.readouterr()  # calling this function clears the buffer
            assert f"({filename}:{lineno}) test/nodb/infoitdevice -> InfoItDevice.{method}()" in out

        lineno = device.decorated_attribute - 3
        out, _ = capfd.readouterr()
        assert f"({filename}:{lineno}) test/nodb/infoitdevice -> InfoItDevice.decorated_attribute()" in out


@pytest.mark.skipif(
    not os.environ.get("PYTHONUNBUFFERED"),
    reason="This test requires PYTHONUNBUFFERED=1 to capture the outputs.",
)
def test_stream_logging_source_location(server_green_mode, capfd):
    if server_green_mode == GreenMode.Asyncio:

        class StreamLogsDevice(Device):
            green_mode = server_green_mode

            @command(dtype_out=int)
            async def log_streams(self):
                self.info_stream("info")
                self.debug_stream("debug")
                self.warn_stream("warn")
                self.error_stream("error")
                self.fatal_stream("fatal")
                return inspect.currentframe().f_lineno

    else:

        class StreamLogsDevice(Device):
            green_mode = server_green_mode

            @command(dtype_out=int)
            def log_streams(self):
                self.info_stream("info")
                self.debug_stream("debug")
                self.warn_stream("warn")
                self.error_stream("error")
                self.fatal_stream("fatal")
                return inspect.currentframe().f_lineno

    with DeviceTestContext(StreamLogsDevice, debug=3) as device:
        lineno = device.command_inout("log_streams") - 5
        filename = os.path.basename(__file__)
        out, _ = capfd.readouterr()
        for i, level in [
            (0, "INFO"),
            (1, "DEBUG"),
            (2, "WARN"),
            (3, "ERROR"),
            (4, "FATAL"),
        ]:
            assert f"{level} ({filename}:{lineno + i}) test/nodb/streamlogsdevice" in out
