# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
"""
Run a Tango device server and do some things that have either caused
memory leaks in the past, or are suspected of causing memory leaks.
"""

import contextlib
import gc
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
    ExtractAs,
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

# Extracting an array as bytes/bytearray/str uses a different convertor than the
# numpy/tuple extraction everything else here goes through.
BINARY_EXTRACT_AS = (ExtractAs.Bytes, ExtractAs.ByteArray, ExtractAs.String)

# An element that cannot be converted to a DevString, so that the python->cpp
# buffer conversion throws halfway: the elements converted before it are owned
# by the buffer and must be freed by it.
PARTIAL_STRING_SEQUENCE = ["a", 5, "c"]


class MemTestDevice(Device):
    _attr_data: ClassVar[dict] = {}
    _attr_quality = AttrQuality.ATTR_VALID
    _throw = False
    _return_empty = False

    def initialize_dynamic_attributes(self):
        for dtype, values in {**GENERAL_TYPED_VALUES, **IMAGE_TYPED_VALUES}.items():
            # Only arrays have an empty variant, and only for them does the
            # binary extraction below take its empty-value branch.
            empty = [] if isinstance(dtype, tuple) else None

            name = f"attr_ro_{repr_type(dtype)}"
            self._attr_data[name] = {"value": values[0], "empty": empty, "reads": 0, "writes": 0}

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
            self._attr_data[name] = {"value": values[0], "empty": empty, "reads": 0, "writes": 0}

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
        data = self._attr_data[attr_name]
        empty = data.get("empty")
        value = empty if self._return_empty and empty is not None else data["value"]
        data["reads"] += 1
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
        # WAttribute.set_write_value runs its own python->cpp buffer conversion,
        # which owns the converted elements. Nothing else here reaches it.
        self.get_device_attr().get_w_attr_by_name(attr_name).set_write_value(value)

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
    def set_return_empty(self, empty: bool):
        self._return_empty = empty

    @command
    def set_bad_write_value(self, attr_name: str):
        self.get_device_attr().get_w_attr_by_name(attr_name).set_write_value(PARTIAL_STRING_SEQUENCE)

    @command
    def emit_events(self, config_json: str):
        config = json.loads(config_json)
        attr_name = config["name"]
        push_count = config["count"]
        value = self._attr_data[attr_name]["value"]
        for _ in range(push_count):
            self.push_change_event(attr_name, value)

    @command
    def get_allocated_blocks(self) -> int:
        """Number of blocks currently held by the Python allocator, sampled
        inside the server process.

        The server runs in a child process, so the client cannot observe its
        Python objects directly -- yet that is exactly where the interesting
        reference leaks live (the exception-to-DevFailed translation, for
        instance). This command brings the number across the wire.
        """
        gc.collect()
        return sys.getallocatedblocks()

    @command
    def get_attr_stats(self, attr_name: str) -> str:
        stats = {
            "reads": self._attr_data[attr_name]["reads"],
            "writes": self._attr_data[attr_name]["writes"],
        }
        return json.dumps(stats)


# Two independent leak checks run over the loops below. Neither subsumes the
# other, so run_valgrind_checks.sh gates on both:
#
#   RSS      -- process resident size. Catches ANY heap growth, including pure
#               C/C++ leaks that never create a Python object (CORBA::string_dup,
#               the `new char[]` in from_python_str_to_cpp_char, cppTango
#               internals). Coarse: needs a sizeable leak to stand out.
#   BLOCKS   -- sys.getallocatedblocks(), the number of blocks live in the Python
#               allocator. Catches every leaked *Python* object exactly, however
#               small, including pybind11 wrapper instances (which the GC does not
#               track, so gc.get_objects() misses them). Blind to anything that is
#               not a Python object.
#
# Valgrind sees neither: a leaked PyObject stays reachable from CPython's
# internals, so memcheck calls it "still reachable"/"possibly lost" and never
# "definitely lost" -- and we only fail on definite leaks. See
# run_valgrind_checks.sh.
#
# Both signals are only meaningful for the *tail* of the run: exercising many
# distinct commands/attributes has a one-time per-type cost (pybind11 casters,
# lazy imports, first-time code paths) that looks like growth but plateaus. We
# prime those paths in a warm-up pass, then judge the slope over a *trailing*
# window (not an expanding one), so a warm-up ramp cannot be mistaken for a leak
# while sustained growth still fails.
TRAILING_WINDOW = 15  # trailing samples used to assess either slope

RSS_TOL_BYTES_PER_CYCLE = 200_000  # a real leak grows far faster
# Measured on the exception-translation leak fixed in eef80a98: server slope 2,216
# blocks/cycle (worst window 3,646) with the leak, versus 8 (worst window 94) on a
# clean tree. The worst-window figure is what matters -- the attribute sweep has a
# bounded warm-up ramp that peaks around 94 -- so the tolerance sits above that and
# still an order of magnitude below a real leak.
BLOCKS_TOL_PER_CYCLE = 300

# Both checks are opt-in, so each run says positively what it measures. Neither is
# meaningful UNDER valgrind -- its allocator (plus PYTHONMALLOC=malloc) makes RSS
# climb on its own -- so the valgrind run simply enables neither. The two are also
# kept in separate runs from each other, because sampling blocks costs a
# gc.collect() and an extra Tango round-trip per cycle, which perturbs the RSS
# slope. See run_valgrind_checks.sh for the three runs.
RSS_CHECK_ENABLED = os.environ.get("MEMTEST_RSS_CHECK", "0") == "1"
BLOCKS_CHECK_ENABLED = os.environ.get("MEMTEST_BLOCKS_CHECK", "0") == "1"
UNDER_VALGRIND = not RSS_CHECK_ENABLED and not BLOCKS_CHECK_ENABLED

# Valgrind slows every instruction down by more than an order of magnitude, and
# almost all of the device server's shutdown is spent after its last Python
# statement, in Py_FinalizeEx and the C++ static destructors. That alone needs
# longer than the default process timeout, which the test context applies to
# startup and shutdown alike.
CONTEXT_TIMEOUT = 120.0 if UNDER_VALGRIND else None


def trailing_slope(samples):
    """Least-squares slope per cycle over the trailing TRAILING_WINDOW samples,
    or None until a full window is available."""
    window = samples[-TRAILING_WINDOW:]
    if len(window) < TRAILING_WINDOW:
        return None
    return float(np.polyfit(range(len(window)), window, 1)[0])


def slope_status(samples, tolerance, unit):
    """Per-line status string for the latest sample (informational)."""
    slope = trailing_slope(samples)
    if slope is None:
        return "warmup"
    if slope <= tolerance:
        return "OK"
    return f"not stable ({slope:,.0f} {unit})"


def get_command_input_data_map():
    result = {}
    for dtype, values in {**GENERAL_TYPED_VALUES, **COMMAND_TYPED_VALUES}.items():
        type_name = repr_type(dtype) if not isinstance(dtype, tuple) else f"{repr_type(dtype[0])}_list"
        in_cmd_name = f"cmd_{type_name}_in_"
        in_out_cmd_name = f"cmd_{type_name}_in_out_"
        result[in_cmd_name] = values[0]
        result[in_out_cmd_name] = values[-1]
    return result


@contextlib.contextmanager
def expect_raises(exception):
    """Assert that the wrapped block raises `exception`."""
    try:
        yield
    except exception:
        return
    raise AssertionError(f"{exception.__name__} not raised")


def progress_bar(current, total, width=40):
    progress = int(width * current / total)
    bar = "[" + "#" * progress + "-" * (width - progress) + "]"
    percent = f"{(current / total) * 100:.1f}%"
    sys.stdout.write(f"\r{bar} {percent}")
    sys.stdout.flush()


if __name__ == "__main__":
    print("Running PyTango MemTestDevice")
    ctx = DeviceTestContext(MemTestDevice, process=True, timeout=CONTEXT_TIMEOUT)
    with ctx as proxy:
        print(f"Device info: {proxy.info()}")

        srv = psutil.Process(ctx.thread.pid)  # device server child process
        cli = psutil.Process(os.getpid())  # this (client) process
        srv_rss = []
        cli_rss = []
        srv_blocks = []
        cli_blocks = []

        def sample_line():
            """Sample whichever metrics are enabled and return a per-cycle status string."""
            parts = []

            if RSS_CHECK_ENABLED:
                srv_rss.append(srv.memory_info().rss)
                cli_rss.append(cli.memory_info().rss)
                parts.append(
                    f"RSS srv/cli {srv_rss[-1] // 1024}/{cli_rss[-1] // 1024} KiB"
                    f" | srv RSS {slope_status(srv_rss, RSS_TOL_BYTES_PER_CYCLE, 'B/cycle')}"
                    f" | cli RSS {slope_status(cli_rss, RSS_TOL_BYTES_PER_CYCLE, 'B/cycle')}"
                )

            if BLOCKS_CHECK_ENABLED:
                # Server first: the round-trip allocates on the client side, so
                # sample the client last to keep its number quiet.
                srv_blocks.append(proxy.get_allocated_blocks())
                gc.collect()
                cli_blocks.append(sys.getallocatedblocks())
                parts.append(
                    f"blocks srv/cli {srv_blocks[-1]}/{cli_blocks[-1]}"
                    f" | srv blocks {slope_status(srv_blocks, BLOCKS_TOL_PER_CYCLE, 'blocks/cycle')}"
                    f" | cli blocks {slope_status(cli_blocks, BLOCKS_TOL_PER_CYCLE, 'blocks/cycle')}"
                )

            if not parts:
                return "checks off (valgrind)"
            return " | ".join(parts)

        cmd_names = [cmd for cmd in proxy.get_command_list() if cmd.startswith("cmd_")]
        cmd_input_data_map = get_command_input_data_map()
        attr_names = list(proxy.get_attribute_list())
        # Arrays only, and not DevString: binary extraction is unsupported there.
        binary_extract_attr_names = [name for name in attr_names if "(" in name and "str" not in name]
        string_spectrum_attr_name = f"attr_rw_{repr_type((str,))}"

        # Warm up: touch every command and attribute (including the throwing
        # paths, which lazily import `traceback`/`linecache`) once, so per-type
        # one-time allocations happen BEFORE we start sampling. Without this the
        # first pass over ~30 distinct command types looks like a leak.
        #
        # It matters most to the block count, where a first-touch cache fill IS a
        # set of objects that stay alive: without this pass the server's worst
        # trailing window reaches 320 blocks/cycle, past BLOCKS_TOL_PER_CYCLE,
        # versus 77 with it.
        #
        # Only worth doing when we are actually sampling. Under valgrind we are
        # not, and skipping it keeps the call counts printed below equal to the
        # calls really made, so a reported leak can be compared against them.
        if RSS_CHECK_ENABLED or BLOCKS_CHECK_ENABLED:
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
            proxy.set_return_empty(True)
            for attr_name in binary_extract_attr_names:
                if "_rw_" in attr_name:
                    proxy.write_attribute(attr_name, [])
                for extract_as in BINARY_EXTRACT_AS:
                    proxy.read_attribute(attr_name, extract_as=extract_as)
            proxy.set_return_empty(False)
            with contextlib.suppress(Exception):
                proxy.write_attribute(string_spectrum_attr_name, PARTIAL_STRING_SEQUENCE)
            with contextlib.suppress(Exception):
                proxy.set_bad_write_value(string_spectrum_attr_name)

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
            print(f"{cmd_name:>35} | calls: {unique_num_cmd:>3} | {sample_line()}")

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
                f" ({unique_num_event_no_sub + unique_num_event_with_sub:>3} total) | {sample_line()}"
            )

        print("\nExercising binary extraction of empty arrays:")
        # The convertor takes its empty-value branch only when the attribute is
        # empty as a whole, so the written part has to be emptied as well.
        proxy.set_return_empty(True)
        for attr_name in binary_extract_attr_names:
            if "_rw_" in attr_name:
                proxy.write_attribute(attr_name, [])
        for count, attr_name in enumerate(binary_extract_attr_names):
            # use unique numbers, to help isolate causes of leaks
            unique_num_empty_reads = 24 + count * 10 + len(attr_names) * 10 + unique_num_cmd
            for index in range(unique_num_empty_reads):
                extract_as = BINARY_EXTRACT_AS[index % len(BINARY_EXTRACT_AS)]
                attr_read = proxy.read_attribute(attr_name, extract_as=extract_as)
                assert len(attr_read.value) == 0, f"{attr_name} value not empty: {attr_read.value!r}"
                assert len(attr_read.w_value) == 0, f"{attr_name} w_value not empty: {attr_read.w_value!r}"
            print(f"{attr_name:>25} | empty binary reads: {unique_num_empty_reads:>3} | {sample_line()}")
        proxy.set_return_empty(False)

        print("\nExercising conversions failing halfway through a string spectrum:")
        # use unique numbers, to help isolate causes of leaks
        unique_num_partial_client = 34 + (len(attr_names) + len(binary_extract_attr_names)) * 10 + unique_num_cmd
        unique_num_partial_server = unique_num_partial_client + 1
        # NOTE: only the valgrind pass sees leaks here: a leaked element is a
        # new char[], invisible to sys.getallocatedblocks(), and this section
        # emits a single sample, so the trailing-window slope averages a
        # per-call leak away.
        # client side: the buffer comes from allocbuf and is freed by freebuf
        for _ in range(unique_num_partial_client):
            with expect_raises(TypeError):
                proxy.write_attribute(string_spectrum_attr_name, PARTIAL_STRING_SEQUENCE)
        # server side: the buffer comes from new[] and frees its elements itself
        for _ in range(unique_num_partial_server):
            with expect_raises(DevFailed):
                proxy.set_bad_write_value(string_spectrum_attr_name)
        print(
            f"{string_spectrum_attr_name:>25} | partial conversions:"
            f" {unique_num_partial_client:>3} client, {unique_num_partial_server:>3} server | {sample_line()}"
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
        print(f"\n              DeviceProxy | created: {unique_num_device_proxy:>3} | {sample_line()}")

        print("Creating DeviceProxies to non-existent devices:")
        unique_num_device_proxy_unreachable = unique_num_device_proxy + 1
        for ind in range(unique_num_device_proxy_unreachable):
            with contextlib.suppress(DevFailed):
                DeviceProxy("tango://127.0.0.1:12345/nonexistent/tango/name")
            progress_bar(ind, unique_num_device_proxy_unreachable)
        print(f"\n  unreachable DeviceProxy | created: {unique_num_device_proxy_unreachable:>3} | {sample_line()}")

        print("Creating AttributeProxies:")
        unique_num_attr_proxy = unique_num_device_proxy_unreachable + 1
        for ind in range(unique_num_attr_proxy):
            AttributeProxy(f"{device_name}/state")
            progress_bar(ind, unique_num_attr_proxy)
        print(f"\n           AttributeProxy | created: {unique_num_attr_proxy:>3} | {sample_line()}")

        print("Creating Groups:")
        unique_num_group = unique_num_attr_proxy + 1
        for ind in range(unique_num_group):
            group = Group("test")
            group.add(device_name)
            # Nest a subgroup as well: Group.add(Group) hands ownership of the
            # child over to C++, and used to leak the child's Python wrapper to
            # avoid double-deleting it. NOTE: this section emits a single sample,
            # so a per-call wrapper leak here only shows up as one step and gets
            # averaged away by the trailing-window slope -- measured 641 leaked
            # blocks in that one step, which is not enough to move the statistic.
            # It is gated per-call in tests/test_group.py instead; exercising it
            # here is for the valgrind and RSS passes.
            group.add(Group(f"subgroup_{ind}"))
            progress_bar(ind, unique_num_group)
        print(f"\n                    Group | created: {unique_num_group:>3} | {sample_line()}")

        print("Creating EnsureOmniThreads:")
        unique_num_ensure = unique_num_group + 1
        for _ in range(unique_num_ensure):
            with EnsureOmniThread():
                pass
        print(f"\n         EnsureOmniThread | created: {unique_num_ensure:>3} | {sample_line()}")

    print("\nMemTestDevice done.")

    problems = []
    checks = []
    if RSS_CHECK_ENABLED:
        checks.append(("RSS", "B/cycle", RSS_TOL_BYTES_PER_CYCLE, (("server", srv_rss), ("client", cli_rss))))
    if BLOCKS_CHECK_ENABLED:
        checks.append(
            ("blocks", "blocks/cycle", BLOCKS_TOL_PER_CYCLE, (("server", srv_blocks), ("client", cli_blocks)))
        )

    for metric, unit, tolerance, series in checks:
        for who, samples in series:
            slope = trailing_slope(samples)
            if slope is not None and slope > tolerance:
                problems.append(f"{who} {metric} slope {slope:,.0f} {unit} (tol {tolerance:,})")

    if problems:
        print("\nERROR: memory kept growing beyond tolerance -- possible leak:")
        for problem in problems:
            print(f"  - {problem}")
        sys.exit(1)
