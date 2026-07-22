# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
Run a Tango device server and do some things that have either caused
memory leaks in the past, or are suspected of causing memory leaks.
"""

import contextlib
import json
import os
import sys
import time
from typing import ClassVar

import numpy as np
import psutil

from tango import (
    AttributeProxy,
    AttrQuality,
    AttrWriteType,
    DevFailed,
    DeviceProxy,
    DevState,
    EnsureOmniThread,
    EventType,
    Group,
)
from tango.server import Device, attribute, command
from tango.test_context import DeviceTestContext
from tango.test_utils import (
    COMMAND_TYPED_VALUES,
    GENERAL_TYPED_VALUES,
    IMAGE_TYPED_VALUES,
    repr_type,
)


class MemTestDevice(Device):
    _attr_data: ClassVar[dict] = {}
    _attr_quality = AttrQuality.ATTR_VALID
    _throw = False

    def initialize_dynamic_attributes(self):
        for dtype, values in {**GENERAL_TYPED_VALUES, **IMAGE_TYPED_VALUES}.items():
            name = f"attr_ro_{repr_type(dtype)}"
            self._attr_data[name] = {"value": values[0], "reads": 0, "writes": 0}

            attr = attribute(
                name=name,
                dtype=dtype,
                max_dim_x=3,
                max_dim_y=3,
                access=AttrWriteType.READ,
                fget=self.generic_read,
            )
            self.add_attribute(attr)
            self.set_change_event(name, implemented=True, detect=False)

            name = f"attr_rw_{repr_type(dtype)}"
            self._attr_data[name] = {"value": values[0], "reads": 0, "writes": 0}

            attr = attribute(
                name=name,
                dtype=dtype,
                max_dim_x=3,
                max_dim_y=3,
                access=AttrWriteType.READ_WRITE,
                fget=self.generic_read,
                fset=self.generic_write,
            )
            self.add_attribute(attr)
            self.set_change_event(name, implemented=True, detect=False)

        # Include standard attributes
        self.set_change_event("State", implemented=True, detect=False)
        self.set_change_event("Status", implemented=True, detect=False)
        self._attr_data["State"] = {"value": DevState.ON, "reads": 0, "writes": 0}
        self._attr_data["Status"] = {"value": "State ON", "reads": 0, "writes": 0}

    def generic_read(self, attr):
        attr_name = attr.get_name()
        value = self._attr_data[attr_name]["value"]
        self._attr_data[attr_name]["reads"] += 1
        if self._throw:
            raise RuntimeError("Error reading")
        return value, time.time(), self._attr_quality

    def generic_write(self, attr):
        attr_name = attr.get_name()
        value = attr.get_write_value()
        self._attr_data[attr_name]["writes"] += 1
        if self._throw:
            raise RuntimeError("Error writing")
        self._attr_data[attr_name]["value"] = value

    @command
    def cmd_void_void_(self):
        pass

    @command
    def cmd_int_in_(self, value: int):
        pass

    @command
    def cmd_int_out_(self) -> int:
        return 123

    @command
    def cmd_int_in_out_(self, value: int) -> int:
        return value

    @command
    def cmd_float_in_(self, value: float):
        pass

    @command
    def cmd_float_out_(self) -> float:
        return 123.4

    @command
    def cmd_float_in_out_(self, value: float) -> float:
        return value

    @command
    def cmd_str_in_(self, value: str):
        pass

    @command
    def cmd_str_out_(self) -> str:
        return "abc"

    @command
    def cmd_str_in_out_(self, value: str) -> str:
        return value

    @command
    def cmd_bool_in_(self, value: bool):
        pass

    @command
    def cmd_bool_out_(self) -> bool:
        return True

    @command
    def cmd_bool_in_out_(self, value: bool) -> bool:
        return value

    @command
    def cmd_int_list_in_(self, value: list[int]):
        pass

    @command
    def cmd_int_list_out_(self) -> list[int]:
        return [123, 456]

    @command
    def cmd_int_list_in_out_(self, value: list[int]) -> list[int]:
        return value

    @command
    def cmd_float_list_in_(self, value: list[float]):
        pass

    @command
    def cmd_float_list_out_(self) -> list[float]:
        return [123.4, 456.7]

    @command
    def cmd_float_list_in_out_(self, value: list[float]) -> list[float]:
        return value

    @command
    def cmd_str_list_in_(self, value: list[str]):
        pass

    @command
    def cmd_str_list_out_(self) -> list[str]:
        return ["abc", "def"]

    @command
    def cmd_str_list_in_out_(self, value: list[str]) -> list[str]:
        return value

    @command
    def cmd_bool_list_in_(self, value: list[bool]):
        pass

    @command
    def cmd_bool_list_out_(self) -> list[bool]:
        return [True, False]

    @command
    def cmd_bool_list_in_out_(self, value: list[bool]) -> list[bool]:
        return value

    @command
    def cmd_DevVarLongStringArray_in_(self, value: list[list[int], list[str]]):
        pass

    @command
    def cmd_DevVarLongStringArray_out_(self) -> list[list[int], list[str]]:
        return [[123, 456], ["abc", "def"]]

    @command
    def cmd_DevVarLongStringArray_in_out_(self, value: list[list[int], list[str]]) -> list[list[int], list[str]]:
        return value

    @command
    def cmd_DevVarDoubleStringArray_in_(self, value: list[list[float], list[str]]):
        pass

    @command
    def cmd_DevVarDoubleStringArray_out_(self) -> list[list[float], list[str]]:
        return [[123.4, 456.7], ["abc", "def"]]

    @command
    def cmd_DevVarDoubleStringArray_in_out_(self, value: list[list[float], list[str]]) -> list[list[float], list[str]]:
        return value

    def dev_state(self):
        self._attr_data["State"]["reads"] += 1
        return self._attr_data["State"]["value"]

    def dev_status(self):
        self._attr_data["Status"]["reads"] += 1
        return self._attr_data["Status"]["value"]

    @command
    def set_attr_quality_invalid(self, invalid: bool):
        if invalid:
            self._attr_quality = AttrQuality.ATTR_INVALID
        else:
            self._attr_quality = AttrQuality.ATTR_VALID

    @command
    def set_trowing(self, throw: bool):
        self._throw = throw

    @command
    def emit_events(self, config_json: str):
        config = json.loads(config_json)
        attr_name = config["name"]
        push_count = config["count"]
        value = self._attr_data[attr_name]["value"]
        for _ in range(push_count):
            self.push_change_event(attr_name, value)

    @command
    def get_attr_stats(self, attr_name: str) -> str:
        stats = {
            "reads": self._attr_data[attr_name]["reads"],
            "writes": self._attr_data[attr_name]["writes"],
        }
        return json.dumps(stats)


# RSS monitoring: valgrind cannot catch Python reference leaks (they show as
# "possibly lost", never "definitely lost" -- see run_valgrind_checks.sh). Such
# leaks only show up as heap growth over time, so we sample process RSS each cycle
# of the loops below and report per line whether it is still stable.
#
# The signal is only meaningful for the *tail* of the run: exercising many
# distinct commands/attributes has a one-time per-type cost (pybind11 casters,
# lazy imports, first-time code paths) that looks like growth but plateaus. We
# prime those paths in a warm-up pass, then judge the slope over a *trailing*
# window (not an expanding one), so a warm-up ramp cannot be mistaken for a leak
# while sustained growth still fails.
RSS_WINDOW = 15  # trailing samples used to assess the slope
RSS_TOL_BYTES_PER_CYCLE = 200_000  # slope tolerance; a real ref-leak grows far faster
# The RSS check is only meaningful WITHOUT valgrind -- valgrind's allocator (plus
# PYTHONMALLOC=malloc) makes RSS climb steadily on its own. run_valgrind_checks.sh
# runs this script twice: once under valgrind with MEMTEST_RSS_CHECK=0, once plainly
# with the check enabled.
RSS_CHECK_ENABLED = os.environ.get("MEMTEST_RSS_CHECK", "1") != "0"


def rss_slope(samples):
    """Least-squares slope (bytes/cycle) over the trailing RSS_WINDOW samples,
    or None until a full window is available."""
    window = samples[-RSS_WINDOW:]
    if len(window) < RSS_WINDOW:
        return None
    return float(np.polyfit(range(len(window)), window, 1)[0])


def rss_status(samples):
    """Per-line status string for the latest RSS sample (informational)."""
    slope = rss_slope(samples)
    if slope is None:
        return "RSS warmup"
    if slope <= RSS_TOL_BYTES_PER_CYCLE:
        return "RSS is OK"
    return f"RSS not stable ({slope:,.0f} B/cycle)"


def get_command_input_data_map():
    result = {}
    for dtype, values in {**GENERAL_TYPED_VALUES, **COMMAND_TYPED_VALUES}.items():
        type_name = repr_type(dtype) if not isinstance(dtype, tuple) else f"{repr_type(dtype[0])}_list"
        in_cmd_name = f"cmd_{type_name}_in_"
        in_out_cmd_name = f"cmd_{type_name}_in_out_"
        result[in_cmd_name] = values[0]
        result[in_out_cmd_name] = values[-1]
    return result


def progress_bar(current, total, width=40):
    progress = int(width * current / total)
    bar = "[" + "#" * progress + "-" * (width - progress) + "]"
    percent = f"{(current / total) * 100:.1f}%"
    sys.stdout.write(f"\r{bar} {percent}")
    sys.stdout.flush()


if __name__ == "__main__":
    print("Running PyTango MemTestDevice")
    ctx = DeviceTestContext(MemTestDevice, process=True)
    with ctx as proxy:
        print(f"Device info: {proxy.info()}")

        srv = psutil.Process(ctx.thread.pid)  # device server child process
        cli = psutil.Process(os.getpid())  # this (client) process
        srv_rss = []
        cli_rss = []

        def rss_line():
            """Sample server + client RSS and return a per-cycle status string."""
            srv_rss.append(srv.memory_info().rss)
            cli_rss.append(cli.memory_info().rss)
            base = f"RSS srv/cli {srv_rss[-1] // 1024}/{cli_rss[-1] // 1024} KiB"
            if not RSS_CHECK_ENABLED:
                return f"{base} | RSS check off (valgrind)"
            return f"{base} | srv {rss_status(srv_rss)} | cli {rss_status(cli_rss)}"

        cmd_names = [cmd for cmd in proxy.get_command_list() if cmd.startswith("cmd_")]
        cmd_input_data_map = get_command_input_data_map()
        attr_names = list(proxy.get_attribute_list())

        # Warm up: touch every command and attribute (including the throwing
        # paths, which lazily import `traceback`/`linecache`) once, so per-type
        # one-time allocations happen BEFORE we start sampling RSS. Without this
        # the first pass over ~30 distinct command types looks like a leak.
        print("\nWarming up (priming per-type code paths)...")
        for cmd_name in cmd_names:
            args = [cmd_input_data_map[cmd_name]] if "_in_" in cmd_name else []
            proxy.command_inout(cmd_name, *args)
        proxy.set_attr_quality_invalid(False)
        for attr_name in attr_names:
            value = proxy.read_attribute(attr_name).value
            proxy.set_trowing(True)
            with contextlib.suppress(Exception):
                proxy.read_attribute(attr_name)
            if "_rw_" in attr_name:
                with contextlib.suppress(Exception):
                    proxy.write_attribute(attr_name, value)
            proxy.set_trowing(False)
            if "_rw_" in attr_name:
                proxy.write_attribute(attr_name, value)

        print("\nExercising commands:")
        unique_num_cmd = 4
        for cmd_name in cmd_names:
            # use unique numbers, to help isolate causes of leaks
            unique_num_cmd += 1
            for _ in range(unique_num_cmd):
                args = []
                if "_in_" in cmd_name:
                    args = [cmd_input_data_map[cmd_name]]
                proxy.command_inout(cmd_name, *args)
            print(f"{cmd_name:>35} | calls: {unique_num_cmd:>3} | {rss_line()}")

        last_unsubscription_time = 0.0
        print("\nExercising attributes:")
        for count, attr_name in enumerate(attr_names):
            # use unique numbers, to help isolate causes of leaks
            offset = count * 10 + unique_num_cmd
            unique_num_ro_invalid = 10 + offset
            unique_num_ro_valid = 12 + offset
            unique_num_throw_reads = 14 + offset
            unique_num_rw = 16 + offset if "_rw_" in attr_name else 0
            unique_num_throw_writes = 18 + offset if "_rw_" in attr_name else 0
            unique_num_event_no_sub = 20 + offset
            unique_num_event_with_sub = 22 + offset

            # read (invalid quality)
            proxy.set_attr_quality_invalid(True)
            for _ in range(unique_num_ro_invalid):
                value = proxy.read_attribute(attr_name).value

            # read/write (valid quality)
            proxy.set_attr_quality_invalid(False)
            for _ in range(unique_num_ro_valid):
                value = proxy.read_attribute(attr_name).value

            proxy.set_trowing(True)

            for _ in range(unique_num_throw_reads):
                with contextlib.suppress(Exception):
                    value = proxy.read_attribute(attr_name).value

            proxy.set_trowing(False)

            for _ in range(unique_num_rw):
                proxy.write_attribute(attr_name, value)

            proxy.set_trowing(True)

            for _ in range(unique_num_throw_writes):
                with contextlib.suppress(Exception):
                    proxy.write_attribute(attr_name, value)

            proxy.set_trowing(False)

            config = {"name": attr_name, "count": unique_num_event_no_sub}
            proxy.emit_events(json.dumps(config))

            config = {"name": attr_name, "count": unique_num_event_with_sub}
            eid = proxy.subscribe_event(attr_name, EventType.CHANGE_EVENT, lambda x: None)
            proxy.emit_events(json.dumps(config))
            proxy.unsubscribe_event(eid)
            last_unsubscription_time = time.time()

            attr_stats = json.loads(proxy.get_attr_stats(attr_name))
            print(
                f"{attr_name:>25} | "
                f"reads: {unique_num_ro_invalid:>3} direct invalid,"
                f" {unique_num_ro_valid:>3} direct valid"
                f" {unique_num_throw_reads:>3} direct throw"
                f" ({attr_stats['reads']:>3} total) | "
                f"writes: {unique_num_rw:>3} direct "
                f" {unique_num_throw_writes:>3} direct throw"
                f" ({attr_stats['writes']:>3} total) | "
                f"events: {unique_num_event_no_sub:>3} no subscriber,"
                f" {unique_num_event_with_sub:>3} with subscriber,"
                f" ({unique_num_event_no_sub + unique_num_event_with_sub:>3} total) | {rss_line()}"
            )

        print("\nExercising client creation:")
        device_name = proxy.dev_name()
        offset = (len(attr_names) * 10 + unique_num_cmd + 10) * 2
        num_device_proxy_from_test_context = 2  # server + device
        unique_num_device_proxy = offset

        print("Creating DeviceProxies:")
        n_device_proxies = unique_num_device_proxy - num_device_proxy_from_test_context
        for ind in range(n_device_proxies):
            DeviceProxy(device_name)
            progress_bar(ind, n_device_proxies)
        print(f"\n              DeviceProxy | created: {unique_num_device_proxy:>3} | {rss_line()}")

        print("Creating DeviceProxies to non-existent devices:")
        unique_num_device_proxy_unreachable = unique_num_device_proxy + 1
        for ind in range(unique_num_device_proxy_unreachable):
            with contextlib.suppress(DevFailed):
                DeviceProxy("tango://127.0.0.1:12345/nonexistent/tango/name")
            progress_bar(ind, unique_num_device_proxy_unreachable)
        print(f"\n  unreachable DeviceProxy | created: {unique_num_device_proxy_unreachable:>3} | {rss_line()}")

        print("Creating AttributeProxies:")
        unique_num_attr_proxy = unique_num_device_proxy_unreachable + 1
        for ind in range(unique_num_attr_proxy):
            AttributeProxy(f"{device_name}/state")
            progress_bar(ind, unique_num_attr_proxy)
        print(f"\n           AttributeProxy | created: {unique_num_attr_proxy:>3} | {rss_line()}")

        print("Creating Groups:")
        unique_num_group = unique_num_attr_proxy + 1
        for ind in range(unique_num_group):
            group = Group("test")
            group.add(device_name)
            progress_bar(ind, unique_num_group)
        print(f"\n                    Group | created: {unique_num_group:>3} | {rss_line()}")

        print("Creating EnsureOmniThreads:")
        unique_num_ensure = unique_num_group + 1
        for _ in range(unique_num_ensure):
            with EnsureOmniThread():
                pass
        print(f"\n         EnsureOmniThread | created: {unique_num_ensure:>3} | {rss_line()}")

    print("\nMemTestDevice done.")

    if RSS_CHECK_ENABLED:
        problems = []
        for who, samples in (("server", srv_rss), ("client", cli_rss)):
            slope = rss_slope(samples)
            if slope is not None and slope > RSS_TOL_BYTES_PER_CYCLE:
                problems.append(f"{who} RSS slope {slope:,.0f} B/cycle (tol {RSS_TOL_BYTES_PER_CYCLE:,})")
        if problems:
            print("\nERROR: RSS kept growing beyond tolerance -- possible memory leak:")
            for problem in problems:
                print(f"  - {problem}")
            sys.exit(1)
