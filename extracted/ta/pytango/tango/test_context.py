# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Provide a context to run a device without a database."""

# Imports
import os
import time
import struct
import socket
import tempfile
import traceback
import collections
import psutil
from functools import partial

# Concurrency imports
import threading
import multiprocessing
import queue

# CLI imports
from ast import literal_eval
from importlib import import_module
from argparse import ArgumentParser, ArgumentTypeError

# Local imports
from tango.server import run
from tango.utils import (
    _clear_test_context_tango_host_fqtrl,
    is_non_str_seq,
    _set_test_context_tango_host_fqtrl,
)
from tango.green import switch_existing_global_executors_to_thread
from tango import Database, DevFailed, DeviceProxy, EnsureOmniThread, Util

__all__ = (
    "MultiDeviceTestContext",
    "DeviceTestContext",
    "run_device_test_context",
    "get_server_port_via_pid",
)

# Helpers

_DEFAULT_THREAD_TIMEOUT = 5.0
_DEFAULT_PROCESS_TIMEOUT = 7.0

IOR = collections.namedtuple(
    "IOR",
    "first dtype_length dtype nb_profile tag "
    "length major minor wtf host_length host port body",
)

NO_DB_FRAGMENT = "dbase=no"


def ascii_to_bytes(s):
    convert = lambda x: bytes((int(x, 16),))
    return b"".join(convert(s[i : i + 2]) for i in range(0, len(s), 2))


def parse_ior(encoded_ior):
    assert encoded_ior[:4] == "IOR:"
    ior = ascii_to_bytes(encoded_ior[4:])
    dtype_length = struct.unpack_from("II", ior)[-1]
    form = f"II{dtype_length:d}sIIIBBHI"
    host_length = struct.unpack_from(form, ior)[-1]
    form = f"II{dtype_length:d}sIIIBBHI{host_length:d}sH0I"
    values = struct.unpack_from(form, ior)
    values += (ior[struct.calcsize(form) :],)
    strip = lambda x: x[:-1] if isinstance(x, bytes) else x
    return IOR(*map(strip, values))


def get_server_host_port():
    util = Util.instance()
    ds = util.get_dserver_device()
    encoded_ior = util.get_dserver_ior(ds)
    ior = parse_ior(encoded_ior)
    return ior.host.decode(), ior.port


def get_server_port_via_pid(pid, host, retries=400, delay=0.03):
    """Return the TCP port that a device server process is listening on (GIOP).

    This checks TCP sockets open on the process with the given PID, and attempts
    to find the one that accepts GIOP traffic.  A connection will be made to each
    listening socket, and data may be sent to them.

    General Inter-ORB Protocol (GIOP) is the message protocol which object
    request brokers (ORBs) communicate in CORBA.  This port is the one that is
    used when connecting a DeviceProxy.  These are not the port(s) used for ZMQ
    event traffic.

    :param pid: operating system process identifier
    :type pid: int
    :param host: hostname/IP that device server is listening on.  E.g., 127.0.0.1,
                 IP address of a non-loopback network interface, etc.  Note that starting a device
                 server on "localhost" may fail if OmniORB creates an IPv6-only socket.
    :type host: str
    :param retries: number of times to retry attempts, optional
    :type retries: int
    :param delay: time to wait (seconds) between retries, optional
    :type delay: float

    :returns: TCP port number
    :rtype: int

    :raises RuntimeError: If the GIOP port couldn't be identified

    .. versionadded:: 9.4.0
    .. versionadded:: 9.5.0
        *retries* parameter.
        *delay* parameter.
    """

    count = 0
    port = None
    last_err = None
    while port is None and count < retries:
        ports = _get_listening_tcp_ports(pid)
        try:
            port = _get_giop_port(host, ports)
        except Exception as err:
            last_err = err
            time.sleep(delay)
        count += 1

    if port is None:
        raise RuntimeError(
            f"Failed to get GIOP TCP port within {count * delay:.1f} sec"
        ) from last_err

    return port


def _get_listening_tcp_ports(pid):
    p = psutil.Process(pid)
    if hasattr(p, "net_connections"):
        conns = p.net_connections(kind="tcp")
    else:
        conns = p.connections(kind="tcp")  # deprecated in psutil v6.0.0
    return list(set([c.laddr.port for c in conns if c.status == "LISTEN"]))


def _get_giop_port(host, ports):
    protocols = _try_get_protocols_on_ports(host, ports)
    for port, protocol in protocols.items():
        if protocol == "GIOP":
            return port
    raise RuntimeError(
        f"None of ports {ports} appear to have GIOP protocol. "
        f"Guessed protocols: {protocols}."
    )


def _try_get_protocols_on_ports(host, ports):
    """Return a dict with port to protocol mapping.

    This attempts to establish a TCP socket connection to the host
    for each port, and then determine the protocol it supports.

    ZMQ client sockets receive an unsolicited version check message on connection.
    CORBA GIOP client sockets don't receive an unsolicited message, so we send
    a requested to disconnect, and expect an empty message back.
    """
    zmq_response = (
        b"\xff\x00\x00\x00\x00\x00\x00\x00\x01\x7f"  # signature + version check
    )
    giop_send = b"GIOP\x01\x02\x01\x05\x00\x00\x00\x00"  # request disconnect
    giop_response = b""  # graceful disconnect
    max_bytes_expected = len(zmq_response)

    protocols = dict.fromkeys(ports, "Unknown")
    for port in ports:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.settimeout(0.001)
            server_address = (host, port)
            sock.connect(server_address)

            try:
                data = sock.recv(max_bytes_expected)
                if data == zmq_response:
                    protocols[port] = "ZMQ"
                    continue
            except OSError:
                pass

            try:
                sock.sendall(giop_send)
                data = sock.recv(max_bytes_expected)
                if data == giop_response:
                    protocols[port] = "GIOP"
                    continue
            except OSError:
                pass
        except OSError:
            pass
        finally:
            sock.close()
    return protocols


def literal_dict(arg):
    return dict(literal_eval(arg))


def device(path):
    """Get the device class from a given module."""
    module_name, device_name = path.rsplit(".", 1)
    try:
        module = import_module(module_name)
    except Exception:
        raise ArgumentTypeError(
            f"Error importing {module_name}.{device_name}:\n"
            f"{traceback.format_exc()}"
        )
    return getattr(module, device_name)


def get_host_ip():
    """Get the primary external host IP.

    This is used to be useful because an explicit IP was required to get
    tango events to work properly.  Now remains for backwards compatibility.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Connecting to a UDP address doesn't send packets
    # Note:  For some reason Python3 on macOS does not accept 0 as a port but
    # returns with an errno 49 instead. Therefore, just use port 80 which just
    # works as well.
    s.connect(("8.8.8.8", 80))
    # Get ip address
    ip = s.getsockname()[0]
    s.close()
    return ip


def _device_class_from_field(field):
    """
    Helper function that extracts and return a device class from a
    'class' field of a devices_info dictionary

    :param field: the field from which to extract the device class

    :return: the device class extracted from the field
    """
    device_cls_class = None
    if is_non_str_seq(field):
        (device_cls_class, device_class) = (field[0], field[1])
        if isinstance(device_cls_class, str):
            device_cls_class = device(device_cls_class)
    else:
        device_class = field
    if isinstance(device_class, str):
        device_class = device(device_class)
    return (device_cls_class, device_class)


class MultiDeviceTestContext:
    """Context to run device(s) without a database.

    The difference with respect to
    :class:`~tango.test_context.DeviceTestContext` is that it allows
    to export multiple devices (even of different Tango classes).

    Example usage::

        from tango import DeviceProxy
        from tango.server import Device, attribute
        from tango.test_context import MultiDeviceTestContext


        class Device1(Device):
            @attribute(dtype=int)
            def attr1(self):
                return 1


        class Device2(Device):
            @attribute(dtype=int)
            def attr2(self):
                dev1 = DeviceProxy("test/device/1")
                return dev1.attr1 * 2


        devices_info = (
            {
                "class": Device1,
                "devices": [
                    {"name": "test/device/1"},
                ],
            },
            {
                "class": Device2,
                "devices": [
                    {
                        "name": "test/device/2",
                    },
                ],
            },
        )


        def test_devices():
            with MultiDeviceTestContext(devices_info, process=True) as context:
                proxy1 = context.get_device("test/device/1")
                proxy2 = context.get_device("test/device/2")
                assert proxy1.attr1 == 1
                assert proxy2.attr2 == 2

    :param devices_info:
      a sequence of dicts with information about
      devices to be exported. Each dict consists of the following keys:

        * "class" which value is either of:

          * a :class:`~tango.server.Device` or the name of some such class
          * a sequence of two elements, the first element being a
            :class:`~tango.DeviceClass` or the name of some such class,
            the second element being a :class:`~tango.DeviceImpl` or the
            name of some such class

        * "devices" which value is a sequence of dicts with the following keys:

          * "name" (str)
          * "properties" (dict)
          * "memorized" (dict)
          * "root_atts" (dict)"

    :type devices_info:
      sequence<dict>
    :param server_name:
      Name to use for the device server.
      Optional.  Default is the first device's class name.
    :type server_name:
      :py:obj:`str`
    :param instance_name:
      Name to use for the device server instance.
      Optional.  Default is lower-case version of the server name.
    :type instance_name:
      :py:obj:`str`
    :param db:
      Path to a pre-populated text file to use for the
      database.
      Optional.  Default is to create a new temporary file and populate it
      based on the devices and properties supplied in `devices_info`.
    :type db:
      :py:obj:`str`
    :param host:
      Hostname to use for device server's ORB endpoint.
      Optional.  Default is the loopback IP address, 127.0.0.1.
    :type host:
      :py:obj:`str`
    :param port:
      Port number to use for the device server's ORB endpoint.
      Optional.  Default is chosen by omniORB.
    :type port:
      :py:obj:`int`
    :param debug:
      Debug level for the device server logging.
      0=OFF, 1=FATAL, 2=ERROR, 3=WARN, 4=INFO, 5=DEBUG.
      Optional. Default is warn.
    :type debug:
      :py:obj:`int`
    :param process:
      True if the device server should be launched in a new process, otherwise
      use a new thread.  Note:  if the context will be used mutiple times, it
      may seg fault if the thread mode is chosen.
      See the :ref:`issues <testing-approaches-issues>` and
      :ref:`process kwarg <testing-approaches-process-kwarg>` discussion in the docs.
      Optional.  Default is thread.
    :type process:
      :py:obj:`bool`
    :param daemon:
      True if the new thread/process must be created in daemon mode.
      Optional.  Default is not daemon.
    :type daemon:
      :py:obj:`bool`
    :param timeout:
      How long to wait (seconds) for the device server to start up, and also
      how long to wait on joining the thread/process when stopping.
      Optional.  Default differs for thread and process modes.
    :type timeout:
      :py:obj:`float`
    :param green_mode:
      Green mode to use for the device server.
      Optional.  Default uses the Device specification (via green_mode class attribute),
      or if that isn't specified the global green mode.
    :type green_mode:
      :obj:`~tango.GreenMode`

    .. versionadded:: 9.3.2

    .. versionadded:: 9.3.3
        Added support for `memorized` key to "devices" field in `devices_info`.
        Added support for literal names for "class" field in `devices_info`.

    .. versionadded:: 9.3.3
        added *green_mode* parameter.

    .. versionchanged:: 9.5.0
        By default, devices launched by a test context can be accessed using
        short names with :class:`~tango.AttributeProxy`, :class:`~tango.DeviceProxy`,
        and :class:`~tango.Group`.
        This can be disabled by setting the `enable_test_context_tango_host_override`
        class/instance attribute to `False` before starting the test context.
        Added support for `root_atts` key to "devices" field in `devices_info`.
    """

    command = "{0} {1} -ORBendPoint giop:tcp:{2}:{3} -file={4}"
    enable_test_context_tango_host_override = True

    thread_timeout = _DEFAULT_THREAD_TIMEOUT
    process_timeout = _DEFAULT_PROCESS_TIMEOUT

    def __init__(
        self,
        devices_info,
        server_name=None,
        instance_name=None,
        db=None,
        host=None,
        port=0,
        debug=3,
        process=False,
        daemon=False,
        timeout=None,
        green_mode=None,
    ):
        if not server_name:
            _, first_device = _device_class_from_field(devices_info[0]["class"])
            server_name = first_device.__name__
        if not instance_name:
            instance_name = server_name.lower()
        if db is None:
            handle, db = tempfile.mkstemp()
            self.handle = handle
        else:
            self.handle = None
        if host is None:
            host = "127.0.0.1"  # note: localhost does not currently work
        if timeout is None:
            timeout = self.process_timeout if process else self.thread_timeout
        # Attributes
        self.db = db
        self.host = host
        self.port = port
        self.timeout = timeout
        self.server_name = "/".join(("dserver", server_name, instance_name))
        if process:
            self._startup_exception_queue = multiprocessing.Queue()
            self._discovered_port_queue = multiprocessing.JoinableQueue()
        else:
            self._startup_exception_queue = queue.Queue()
            self._discovered_port_queue = queue.Queue()
        self._startup_exception = None
        self._devices = {}
        self._saved_environ = {}
        self._process = process

        # Command args
        string = self.command.format(server_name, instance_name, host, port, db)
        string += f" -v{debug}" if debug else ""
        cmd_args = string.split()

        class_list = []
        device_list = []
        tangoclass_list = []
        for device_info in devices_info:
            device_cls, device = _device_class_from_field(device_info["class"])
            tangoclass = device.__name__
            if tangoclass in tangoclass_list:
                self.delete_db()
                raise ValueError(
                    "multiple entries in devices_info pointing "
                    "to the same Tango class"
                )
            tangoclass_list.append(tangoclass)
            # File
            self.append_db_file(
                server_name, instance_name, tangoclass, device_info["devices"]
            )
            if device_cls:
                class_list.append((device_cls, device, tangoclass))
            else:
                device_list.append(device)

        # Target and arguments
        if class_list and device_list:
            self.delete_db()
            raise ValueError(
                "mixing HLAPI and classical API in devices_info is not supported"
            )
        if class_list:
            runserver = partial(run, class_list, cmd_args, green_mode=green_mode)
        elif len(device_list) == 1 and hasattr(device_list[0], "run_server"):
            runserver = partial(device.run_server, cmd_args, green_mode=green_mode)
        elif device_list:
            runserver = partial(run, device_list, cmd_args, green_mode=green_mode)
        else:
            raise ValueError("Wrong format of devices_info")

        cls = multiprocessing.Process if process else threading.Thread
        self.thread = cls(target=self.target, args=(runserver, process))
        self.thread.daemon = daemon

    def target(self, runserver, process=False):
        with EnsureOmniThread():
            threading.current_thread().name += " TestContext DS launcher"
            try:
                runserver(
                    pre_init_callback=self.pre_init,
                    post_init_callback=self.post_init,
                    raises=True,
                )
            except Exception as exc:
                self._startup_exception_queue.put(exc)
                self._discovered_port_queue.put(-1)  # don't block queue reader
            finally:
                # Put something in the queue just in case
                exc = RuntimeError("The server failed to report anything")
                self._startup_exception_queue.put(exc)
                # Make sure the process has enough time to send the items
                # because it might segfault while cleaning up the tango resources
                if process:
                    time.sleep(0.1)

    def pre_init(self):
        try:
            if not self.port:
                util = Util.instance()
                pid = util.get_pid()
                self.port = get_server_port_via_pid(pid, self.host)
            if self._process:
                # set TANGO_HOST override for device server (DS) launcher child process
                self._override_test_context_tango_host()
            # report it to the test context process (DS launcher's parent)
            self._discovered_port_queue.put(self.port)
            # and wait till it has been processed
            self._discovered_port_queue.join()
        except Exception as exc:
            self._startup_exception_queue.put(exc)
            self._discovered_port_queue.put(-1)  # don't block queue reader

    def _wait_until_port_is_known(self):
        try:
            self.port = self._discovered_port_queue.get(timeout=self.timeout)
        except queue.Empty:
            raise RuntimeError(
                "GIOP TCP port of TextContext device server not available during startup"
            )

        # set the TANGO_HOST override for the process that created the test context
        self._override_test_context_tango_host()
        # notify the server process, so it can continue
        self._discovered_port_queue.task_done()

    def _override_test_context_tango_host(self):
        if self.enable_test_context_tango_host_override:
            _set_test_context_tango_host_fqtrl(
                f"tango://{self.host}:{self.port}#{NO_DB_FRAGMENT}"
            )

    def post_init(self):
        # now we can connect to the device - success!
        self._startup_exception_queue.put(None)

    def append_db_file(self, server, instance, tangoclass, device_prop_info):
        """Generate a database file corresponding to the given arguments."""
        device_names = [info["name"] for info in device_prop_info]
        # Open the file
        with open(self.db, "a") as f:
            f.write("/".join((server, instance, "DEVICE", tangoclass)))
            f.write(": ")
            f.write(", ".join(device_names))
            f.write("\n")
        # Create database
        db = Database(self.db)
        # Write properties
        for info in device_prop_info:
            device_name = info["name"]
            properties = dict(info.get("properties", {}))
            # Patch the property dict to avoid a PyTango bug
            for key, value in properties.items():
                if is_non_str_seq(value):
                    properties[key] = [v if v != "" else " " for v in value]
                else:
                    properties[key] = value if value != "" else " "
            db.put_device_property(device_name, properties)

            root_atts = info.get("root_atts", {})
            properties_to_save = {
                attribute_name: {"__root_att": root_att}
                for (attribute_name, root_att) in root_atts.items()
            }

            memorized = info.get("memorized", {})
            for attribute_name, memorized_value in memorized.items():
                if attribute_name in properties_to_save:
                    properties_to_save[attribute_name]["__value"] = memorized_value
                else:
                    properties_to_save[attribute_name] = {"__value": memorized_value}

            db.put_device_attribute_property(device_name, properties_to_save)
        try:
            validated_db = Database(self.db)
        except DevFailed:
            with open(self.db, "r") as f:
                content = f.read()
            raise RuntimeError(
                f"Invalid FileDatabase file was created.\n"
                f"Check device properties (empty list or str?): "
                f"{device_prop_info}.\n"
                f"Problematic file has content:\n{content}"
            )
        return validated_db

    def delete_db(self):
        """delete temporary database file only if it was created by this class"""
        if self.handle is not None:
            os.close(self.handle)
            os.unlink(self.db)

    def get_server_access(self) -> str:
        """Return the full server name."""
        return f"tango://{self.host}:{self.port}/{self.server_name}#{NO_DB_FRAGMENT}"

    def get_device_access(self, device_name) -> str:
        """Return the full device name."""
        return f"tango://{self.host}:{self.port}/{device_name}#{NO_DB_FRAGMENT}"

    def get_device(self, device_name) -> DeviceProxy:
        """Return the device proxy corresponding to the given device name.

        Maintains previously accessed device proxies in a cache to not recreate
        then on every access.
        """
        if device_name not in self._devices:
            device = DeviceProxy(self.get_device_access(device_name))
            self._devices[device_name] = device
        return self._devices[device_name]

    def start(self):
        """Run the server.

        This method is automatically called when the context handler is entered.

        :raises RuntimeError: If device server does not start
        """
        self._set_up_environment_variables()
        if not self._process:
            self.thread.daemon = True
        self.thread.start()
        self.connect()
        return self

    def connect(self):
        try:
            self._wait_until_port_is_known()
            self._wait_until_startup_status_is_known()
        except RuntimeError:
            if self.thread.is_alive():
                raise RuntimeError(
                    "The server appears to be stuck at initialization. "
                    "Check stdout/stderr for more information."
                )
            elif hasattr(self.thread, "exitcode"):
                raise RuntimeError(
                    f"The server process stopped with exitcode {self.thread.exitcode}. "
                    f"Check stdout/stderr for more information."
                )
            else:
                raise RuntimeError(
                    "The server stopped without reporting. "
                    "Check stdout/stderr for more information."
                )

        if self._startup_exception:
            raise self._startup_exception

        # Get server proxy
        self.server = DeviceProxy(self.get_server_access())
        self.server.ping()

        # If server has green_mode, we should switch global executor to the main thread
        if not self._process:
            switch_existing_global_executors_to_thread()

    def _wait_until_startup_status_is_known(self):
        try:
            self._startup_exception = self._startup_exception_queue.get(
                timeout=self.timeout
            )
        except queue.Empty:
            raise RuntimeError(
                f"Timed-out waiting for device server startup ({self.timeout:1.3f} sec)"
            )

    def stop(self):
        """Kill the server.

        This method is automatically called when the context handler is exited.

        :raises RuntimeError: If device server does not stop cleanly

        .. versionchanged:: 10.1.0
            Can raise :class:`RuntimeError` on shutdown.
        """
        try:
            if self.server:
                self.server.command_inout("Kill")
            self.join(self.timeout)
            self._ensure_device_server_exited()
        finally:
            _clear_test_context_tango_host_fqtrl()
            self.delete_db()
            self._restore_environment_variables()

    def _ensure_device_server_exited(self):
        if not self.thread.is_alive():
            return
        if self._process:
            self.thread.kill()
            t_start = time.monotonic()
            while self.thread.is_alive() and time.monotonic() - t_start < self.timeout:
                time.sleep(0.1)
            raise RuntimeError(
                f"Device server failed to exit cleanly (stuck in shutdown?). "
                f"Tried to kill subprocess. "
                f"Still alive: {self.thread.is_alive()}."
            )
        else:
            raise RuntimeError(
                "Device server failed to exit cleanly (stuck in shutdown?)"
            )

    def join(self, timeout=None):
        self.thread.join(timeout)

    def _set_up_environment_variables(self):
        self._saved_environ = dict(os.environ)
        if self._process:
            # This variable is used by omniORB to tell it how often
            # to check for idle connections (which can be closed).
            # See: https://omniorb.net/omni43/omniORB/omniORB006.html#sec103
            # It is also used for various timeouts when shutting down.
            # We are interested in the shutdown case.
            # The default is 5 seconds, so we reduce it to get faster
            # process shutdown (especially noticeable on Windows)
            # We can't use 0 seconds because omniORB forces it to 5 seconds.
            # See: src/lib/omniORB/orbcore/giopServer.cc giopServer::deactivate()
            # See also: https://sourceforge.net/p/tango-cs/bugs/819/
            os.environ["ORBscanGranularity"] = "1"

    def _restore_environment_variables(self):
        modified_environ = dict(os.environ)
        saved_environ = self._saved_environ
        for key, value in modified_environ.items():
            if key in saved_environ:
                saved_value = saved_environ[key]
                if value != saved_value:
                    os.environ[key] = saved_value
            else:
                os.environ.pop(key)  # unset environment var

    def __enter__(self) -> "MultiDeviceTestContext":
        """Enter method for context handler support.

        :return:
          Instance of this test context.  Use `get_device` to get proxy
          access to any of the devices started by this context.
        :rtype:
          :class:`~tango.test_context.MultiDeviceTestContext`

        :raises RuntimeError: If device server does not start
        """
        if not self.thread.is_alive():
            self.start()
        return self

    def __exit__(self, exc_type, exception, trace):
        """Exit method for context handler support.

        :raises RuntimeError: If device server does not stop cleanly

        .. versionchanged:: 10.1.0
            Can raise :class:`RuntimeError` on shutdown.
        """
        self.stop()
        return False


# Single device test context
class DeviceTestContext(MultiDeviceTestContext):
    """Context to run a single device without a database.

    The difference with respect to
    :class:`~tango.test_context.MultiDeviceTestContext` is that it only
    allows to export a single device.

    Example usage::

        from time import sleep

        from tango.server import Device, attribute, command
        from tango.test_context import DeviceTestContext

        class PowerSupply(Device):

            @attribute(dtype=float)
            def voltage(self):
                return 1.23

            @command
            def calibrate(self):
                sleep(0.1)

        def test_calibrate():
            '''Test device calibration and voltage reading.'''
            with DeviceTestContext(PowerSupply, process=True) as proxy:
                proxy.calibrate()
                assert proxy.voltage == 1.23

    :param device:
      Device class to be run.
    :type device:
      :class:`~tango.server.Device` or :class:`~tango.DeviceImpl`
    :param device_cls:
      The device class can be provided if using the low-level API.
      Optional.  Not required for high-level API devices, of type
      :class:`~tango.server.Device`.
    :type device_cls:
      :class:`~tango.DeviceClass`

     The rest of the parameters are described in
     :class:`~tango.test_context.MultiDeviceTestContext`.

    .. versionadded:: 9.2.1

    .. versionadded:: 9.3.3
        added *memorized* parameter.

    .. versionadded:: 9.3.6
        added *green_mode* parameter.
    """

    def __init__(
        self,
        device,
        device_cls=None,
        server_name=None,
        instance_name=None,
        device_name=None,
        properties=None,
        db=None,
        host=None,
        port=0,
        debug=3,
        process=False,
        daemon=False,
        timeout=None,
        memorized=None,
        root_atts=None,
        green_mode=None,
    ):
        # Argument
        if not server_name:
            server_name = device.__name__
        if not instance_name:
            instance_name = server_name.lower()
        if not device_name:
            device_name = "test/nodb/" + server_name.lower()
        if properties is None:
            properties = {}
        if memorized is None:
            memorized = {}
        if root_atts is None:
            root_atts = {}
        if device_cls:
            cls = (device_cls, device)
        else:
            cls = device
        devices_info = (
            {
                "class": cls,
                "devices": (
                    {
                        "name": device_name,
                        "properties": properties,
                        "memorized": memorized,
                        "root_atts": root_atts,
                    },
                ),
            },
        )
        super().__init__(
            devices_info,
            server_name=server_name,
            instance_name=instance_name,
            db=db,
            host=host,
            port=port,
            debug=debug,
            process=process,
            daemon=daemon,
            timeout=timeout,
            green_mode=green_mode,
        )

        self.device_name = device_name
        self.device = self.server = None

    def get_device_access(self, device_name=None) -> str:
        """Return the full device name."""
        if device_name is None:
            device_name = self.device_name
        return super().get_device_access(device_name)

    def connect(self):
        super().connect()
        # Get device proxy
        self.device = self.get_device(self.device_name)
        self.device.ping()

    def __enter__(self) -> DeviceProxy:
        """Enter method for context handler support.

        :return:
          A device proxy to the device started by this context.
        :rtype:
          :class:`~tango.DeviceProxy`
        """
        if not self.thread.is_alive():
            self.start()
        return self.device


# Command line interface


def parse_command_line_args(args=None):
    """Parse arguments given in command line."""
    desc = "Run a given device on a given port."
    parser = ArgumentParser(description=desc)
    # Add arguments
    msg = "The device to run as a python path."
    parser.add_argument("device", metavar="DEVICE", type=device, help=msg)
    msg = "The hostname to use."
    parser.add_argument(
        "--host", metavar="HOST", type=str, help=msg, default=get_host_ip()
    )
    msg = "The port to use."
    parser.add_argument("--port", metavar="PORT", type=int, help=msg, default=8888)
    msg = "The debug level."
    parser.add_argument("--debug", metavar="DEBUG", type=int, help=msg, default=3)
    msg = "The properties to set as python dict."
    parser.add_argument(
        "--prop", metavar="PROP", type=literal_dict, help=msg, default="{}"
    )
    msg = "Whether to disable short-name lookup for devices launched by test context"
    parser.add_argument(
        "--disable-short-name-lookup",
        dest="disable_short_name_lookup",
        action="store_true",
        help=msg,
    )
    # Parse arguments
    namespace = parser.parse_args(args)
    return (
        namespace.device,
        namespace.host,
        namespace.port,
        namespace.prop,
        namespace.debug,
        namespace.disable_short_name_lookup,
    )


def run_device_test_context(args=None):
    (
        device_,
        host,
        port,
        properties,
        debug,
        disable_short_name_lookup,
    ) = parse_command_line_args(args)
    context = DeviceTestContext(
        device_, properties=properties, host=host, port=port, debug=debug
    )
    context.enable_test_context_tango_host_override = not disable_short_name_lookup
    context.start()
    msg = f"{device_.__name__} started on port {context.port} with properties {properties}"
    print(msg)
    print(f"Device access: {context.get_device_access()}")
    print(f"Server access: {context.get_server_access()}")
    context.join()
    print("Done")


# Main execution

if __name__ == "__main__":
    run_device_test_context()
