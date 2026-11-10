# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import logging
import os
import queue
import socket
import sys
import threading
import time
from subprocess import DEVNULL, PIPE, Popen

import pytest

from tango import (
    AttributeProxy,
    Database,
    DbData,
    DbDatum,
    DbDevInfo,
    DbServerData,
    DevFailed,
    DevState,
    EventType,
    StdStringVector,
)
from tango.test_utils import wait_for_proxy
from tango.utils import ensure_binary

# Helpers

MAX_STARTUP_TIME_SEC = 30.0
TESTS_DIR = os.path.dirname(__file__)


def start_database(port, inst):
    python = sys.executable
    cmd = f"{python} -u -m tango.databaseds.database --host=127.0.0.1 --port={port} --logging_level=2 {inst}"
    env = os.environ.copy()
    env["PYTANGO_DATABASE_NAME"] = ":memory:"  # Don't write to disk
    logging.debug("Starting databaseds subprocess...")
    proc = Popen(cmd.split(), cwd=TESTS_DIR, stdout=PIPE, bufsize=1, text=True, env=env)
    logging.debug("Waiting for databaseds to startup...")
    try:
        wait_for_tango_server_startup(proc)
    except RuntimeError:
        proc.terminate()
        raise

    return proc


def start_slow_database(port, inst, command_name, delay_seconds=1):
    bootstrap = """
import sys
import time
import types
from tango.databaseds import database

delay_seconds = float(sys.argv.pop())
name = sys.argv.pop()
method = getattr(database.DataBase, name)
while hasattr(method, '__wrapped__'):
    method = method.__wrapped__
method.__globals__['_gil_test_original'] = types.FunctionType(
    method.__code__, method.__globals__
)
method.__globals__['_gil_test_delay_seconds'] = delay_seconds

def delayed(self, argin):
    print('SLOW_DATABASE_COMMAND_ENTERED', flush=True)
    time.sleep(_gil_test_delay_seconds)
    return _gil_test_original(self, argin)

method.__code__ = delayed.__code__
database.main()
"""
    cmd = [
        sys.executable,
        "-u",
        "-c",
        bootstrap,
        "--host=127.0.0.1",
        f"--port={port}",
        "--logging_level=2",
        str(inst),
        command_name,
        str(delay_seconds),
    ]
    env = os.environ.copy()
    env["PYTANGO_DATABASE_NAME"] = ":memory:"
    proc = Popen(cmd, cwd=TESTS_DIR, stdout=PIPE, text=True, env=env)
    try:
        wait_for_tango_server_startup(proc)
    except BaseException:
        proc.terminate()
        proc.wait(timeout=10)
        raise
    proc.gil_test_lines = queue.Queue()

    def read_output():
        for line in proc.stdout:
            proc.gil_test_lines.put(line)

    threading.Thread(target=read_output, daemon=True).start()
    return proc


def assert_rpc_releases_gil(proc, operation):
    completed = threading.Event()
    result = []

    def call():
        try:
            result.append(operation())
        except BaseException as exc:
            result.append(exc)
        finally:
            completed.set()

    worker = threading.Thread(target=call, daemon=True)
    worker.start()
    deadline = time.monotonic() + 5
    while time.monotonic() < deadline:
        try:
            line = proc.gil_test_lines.get(timeout=0.1)
        except queue.Empty:
            continue
        if "SLOW_DATABASE_COMMAND_ENTERED" in line:
            break
    else:
        pytest.fail("The database command was not entered")

    assert not completed.is_set(), "The database call held the GIL until the server replied"
    progress = threading.Event()
    threading.Thread(target=progress.set, daemon=True).start()
    assert progress.wait(0.3), "Another Python thread could not run during the database RPC"
    worker.join(timeout=5)
    assert completed.is_set()
    assert len(result) == 1
    if isinstance(result[0], BaseException):
        raise result[0]
    return result[0]


def wait_for_tango_server_startup(proc):
    t0 = time.time()
    for line in proc.stdout:
        now = time.time()
        elapsed = now - t0
        print(line, end="")
        if "Ready to accept request" in line:
            logging.debug(f"Databaseds startup complete after {elapsed:.1f} sec")
            break
        if elapsed > MAX_STARTUP_TIME_SEC:
            msg = f"Databaseds startup timed out after {elapsed:.1f} sec"
            logging.error(msg)
            raise RuntimeError(msg)


def get_open_port():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


@pytest.fixture()
def tango_database_test():
    port = get_open_port()
    inst = 2

    proc = start_database(port, inst)
    logging.debug("Waiting for databaseds proxy...")
    proxy = wait_for_proxy(f"tango://127.0.0.1:{port}/sys/database/2")
    logging.debug("Databaseds proxy is ready")

    yield proxy

    proc.terminate()
    logging.debug("Terminated databaseds")
    print("Remaining databaseds output:")
    for line in proc.stdout:
        print(line, end="")


# Tests
def test_ping(tango_database_test):
    duration = tango_database_test.ping(wait=True)
    assert isinstance(duration, int)


def test_status(tango_database_test):
    assert tango_database_test.status() == "The device is in ON state."


def test_state(tango_database_test):
    assert tango_database_test.state() == DevState.ON


def test_device_property(tango_database_test):
    def get_name_value(num):
        val = f"value {num}"
        return f"property {num}", val, ensure_binary(val, encoding="latin-1")

    ## put_property overloads:
    # With DbDatum as argument:
    property_name, _, property_value_encoded = get_name_value(1)
    ddatum = DbDatum(property_name)
    ddatum.value_string.append(property_value_encoded)
    tango_database_test.put_property(ddatum)
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 1
    assert return_property_list[0] == property_name

    # With DbData as argument:
    property_name, _, property_value_encoded = get_name_value(2)
    ddatum = DbDatum(property_name)
    ddatum.value_string.append(property_value_encoded)
    ddata = DbData()
    ddata.append(ddatum)
    tango_database_test.put_property(ddata)
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 2
    assert return_property_list[1] == property_name

    # With dict[name: value] as argument:
    property_name, property_value, _ = get_name_value(3)
    tango_database_test.put_property({property_name: property_value})
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 3
    assert return_property_list[2] == property_name

    # With dict[name: DaDatum] as argument:
    property_name, _, property_value_encoded = get_name_value(4)
    ddatum = DbDatum(property_name)
    ddatum.value_string.append(property_value_encoded)
    tango_database_test.put_property({"some_name": ddatum})
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 4
    assert return_property_list[3] == property_name

    # With dict[str: list[str]] as argument:
    property_name, property_value_str, _ = get_name_value(5)
    tango_database_test.put_property({property_name: [property_value_str]})
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 5
    assert return_property_list[4] == property_name

    # With list[DaDatum] as argument:
    property_name_1, _, property_value_encoded_1 = get_name_value(6)
    ddatum_1 = DbDatum(property_name_1)
    ddatum_1.value_string.append(property_value_encoded_1)
    property_name_2, _, property_value_encoded_2 = get_name_value(7)
    ddatum_2 = DbDatum(property_name_2)
    ddatum_2.value_string.append(property_value_encoded_2)
    property_name_3, _, property_value_encoded_3 = get_name_value(8)
    ddatum_3 = DbDatum(property_name_3)
    ddatum_3.value_string.append(property_value_encoded_3)
    property_name_4, _, property_value_encoded_4 = get_name_value(9)
    ddatum_4 = DbDatum(property_name_4)
    ddatum_4.value_string.append(property_value_encoded_4)
    tango_database_test.put_property([ddatum_1, ddatum_2, ddatum_3, ddatum_4])
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 9
    assert return_property_list[5] == property_name_1
    assert return_property_list[6] == property_name_2
    assert return_property_list[7] == property_name_3
    assert return_property_list[8] == property_name_4

    # With empty dict as argument (should not raise):
    tango_database_test.put_property({})

    # With empty list as argument (should not raise):
    tango_database_test.put_property([])

    # With empty tuple as argument (should not raise):
    tango_database_test.put_property(())

    ## get_property overloads:
    return_property = tango_database_test.get_property(property_name)
    assert return_property[property_name][0] == property_value_str

    dbdata = DbData()
    assert len(dbdata) == 0
    return_property = tango_database_test.get_property(property_name, dbdata)
    assert return_property[property_name][0] == property_value_str
    assert len(dbdata) == 1

    datum = DbDatum(property_name)
    return_property = tango_database_test.get_property(datum)
    assert return_property[property_name][0] == property_value_str

    data = DbData()
    data.append(DbDatum(property_name))
    return_property = tango_database_test.get_property(data)
    assert return_property[property_name][0] == property_value_str

    return_property = tango_database_test.get_property([property_name])
    assert return_property[property_name][0] == property_value_str

    dbdata = DbData()
    assert len(dbdata) == 0
    return_property = tango_database_test.get_property([property_name], dbdata)
    assert return_property[property_name][0] == property_value_str
    assert len(dbdata) == 1

    return_property = tango_database_test.get_property([DbDatum(property_name)])
    assert return_property[property_name][0] == property_value_str

    return_property = tango_database_test.get_property({property_name: None})
    assert return_property[property_name][0] == property_value_str

    property_name, _, _ = get_name_value(5)
    ddatum = DbDatum(property_name)
    return_property = tango_database_test.get_property({"some_name": ddatum})
    assert return_property[property_name][0] == property_value_str

    # With empty dict as argument (should give empty dict):
    return_property = tango_database_test.get_property({})
    assert return_property == {}

    # With empty list as argument (should give empty dict):
    return_property = tango_database_test.get_property([])
    assert return_property == {}

    # With empty tuple as argument (should give empty dict):
    return_property = tango_database_test.get_property(())
    assert return_property == {}

    ## delete_property overloads:
    # With str as argument:
    property_name, _, _ = get_name_value(1)
    tango_database_test.delete_property(property_name)
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 8

    # With DbDatum as argument:
    property_name, _, _ = get_name_value(2)
    ddatum = DbDatum(property_name)
    tango_database_test.delete_property(ddatum)
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 7

    # With DbData as argument:
    property_name, _, _ = get_name_value(3)
    ddatum = DbDatum(property_name)
    ddata = DbData()
    ddata.append(ddatum)
    tango_database_test.delete_property(ddata)
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 6

    # With dict[name: value] as argument:
    property_name, _, _ = get_name_value(4)
    tango_database_test.delete_property({property_name: ""})
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 5

    # With dict[name: DaDatum] as argument:
    property_name, _, _ = get_name_value(5)
    ddatum = DbDatum(property_name)
    tango_database_test.delete_property({"some_name": ddatum})
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 4

    # With list[DaDatum] as argument:
    property_name_1, _, _ = get_name_value(6)
    ddatum_1 = DbDatum(property_name_1)
    property_name_2, _, _ = get_name_value(7)
    ddatum_2 = DbDatum(property_name_2)
    tango_database_test.delete_property([ddatum_1, ddatum_2])
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 2

    # With list[str] as argument:
    property_name_1, _, _ = get_name_value(8)
    property_name_2, _, _ = get_name_value(9)
    tango_database_test.delete_property([property_name_1, property_name_2])
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 0

    # With empty dict as argument (should not raise):
    tango_database_test.delete_property({})

    # With empty list as argument (should not raise):
    tango_database_test.delete_property([])

    # With empty tuple as argument (should not raise):
    tango_database_test.delete_property(())


def test_info(tango_database_test):
    info = tango_database_test.info()

    assert info.dev_class == "DataBase"
    assert info.doc_url == "Doc URL = http://www.tango-controls.org"
    assert info.server_id == "DataBaseds/2"


def test_get_device_property_list(tango_database_test):
    db = tango_database_test.get_device_db()
    device_name = "test/property/list"
    db.put_device_property(device_name, {"prop1": ["1"], "prop2": ["2"]})

    # Without a container, the matching names are returned in a new DbDatum:
    assert list(db.get_device_property_list(device_name, "*")) == ["prop1", "prop2"]

    # The wildcard is honoured:
    assert list(db.get_device_property_list(device_name, "prop1")) == ["prop1"]

    # With a StdStringVector, it is filled in place and returned:
    container = StdStringVector()
    assert db.get_device_property_list(device_name, "*", container) is container
    assert list(container) == ["prop1", "prop2"]

    # Any other sequence is appended to and returned:
    container = ["already there"]
    assert db.get_device_property_list(device_name, "*", container) is container
    assert container == ["already there", "prop1", "prop2"]


def test_get_device_property_list_releases_gil():
    port = get_open_port()
    proc = start_slow_database(port, 2, "DbGetDevicePropertyList")
    try:
        db = Database("127.0.0.1", port)
        device_name = "test/slow/property/list"
        db.put_device_property(device_name, {"progress": ["ok"]})

        result = assert_rpc_releases_gil(proc, lambda: db.get_device_property_list(device_name, "*"))
        assert list(result) == ["progress"]

        container = StdStringVector()
        result = assert_rpc_releases_gil(proc, lambda: db.get_device_property_list(device_name, "*", container))

        assert result is container
        assert list(container) == ["progress"]
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        proc.stdout.close()


def test_database_rpc_releases_gil_and_preserves_results(monkeypatch):
    port = get_open_port()
    proc = start_slow_database(port, 2, "DbGetDeviceProperty")
    try:
        db = Database("127.0.0.1", port)
        assert db.dev_name() == "sys/database/2"
        db.put_device_property("test/slow/device", {"progress": ["ok"]})
        result = assert_rpc_releases_gil(proc, lambda: db.get_device_property("test/slow/device", "progress"))
        assert result == {"progress": ["ok"]}
        with pytest.raises(DevFailed):
            db.get_device_from_alias("missing/alias/device")

        monkeypatch.setenv("TANGO_HOST", f"127.0.0.1:{port}")
        server_data = DbServerData("DataBaseds", "2")
        assert server_data.get_name() == "DataBaseds/2"
        assert server_data.already_exist(f"127.0.0.1:{port}")
        with pytest.raises(DevFailed, match="DBServerNotDefinedInDb"):
            DbServerData("MissingServer", "missing")
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        proc.stdout.close()


def test_attribute_proxy_property_rpc_releases_gil_and_preserves_overloads():
    port = get_open_port()
    proc = start_slow_database(port, 2, "DbGetDeviceAttributeProperty2")
    try:
        attr = AttributeProxy(f"tango://127.0.0.1:{port}/sys/database/2/Timing_maximum")
        attr.put_property({"progress": "ok"})

        result = assert_rpc_releases_gil(proc, lambda: attr.get_property("progress"))
        assert result == {"progress": ["ok"]}
        native_attr = attr._AttributeProxy__attr_proxy

        string_output = DbData()
        native_attr._get_property("progress", string_output)
        assert string_output[0].name == "progress"
        assert list(string_output[0].value_string) == ["ok"]

        sequence_output = DbData()
        native_attr._get_property(["progress"], sequence_output)
        assert list(sequence_output[0].value_string) == ["ok"]

        data_output = DbData()
        data_output.append(DbDatum("progress"))
        native_attr._get_property(data_output)
        assert list(data_output[0].value_string) == ["ok"]

        # The standalone database server rejects this delete request; check that
        # the native error crosses the released-GIL boundary intact.
        with pytest.raises(DevFailed, match="DB_IncorrectArguments"):
            attr.delete_property("progress")
    finally:
        proc.terminate()
        proc.wait(timeout=10)
        proc.stdout.close()


@pytest.mark.extra_src_test
def test_runtime_attribute_configuration_releases_gil_during_database_update(tmp_path):
    port = get_open_port()
    db_proc = start_slow_database(port, 2, "DbPutDeviceAttributeProperty2", delay_seconds=2)
    server_proc = None
    proxy = None
    subscription_id = None
    try:
        db = Database("127.0.0.1", port)
        info = DbDevInfo()
        info.name = "test/config/1"
        info._class = "ConfigDevice"
        info.server = "ConfigDevice/test"
        db.add_server(info.server, info, with_dserver=True)

        server_code = """
from pathlib import Path

import tango
from tango.server import Device, attribute, command, run

class ConfigDevice(Device):
    @attribute(dtype=float, access=tango.AttrWriteType.READ_WRITE)
    def value(self):
        return 1.0

    @value.setter
    def value(self, new_value):
        pass

    @command
    def change_alarm(self):
        attr = self.get_device_attr().get_attr_by_name('value')
        attr.set_min_alarm(0.5)

    @command
    def exercise_properties(self):
        attrs = self.get_device_attr()
        attr = attrs.get_attr_by_name('value')
        props = attr.get_properties()
        assert isinstance(props, tango.MultiAttrProp)
        supplied = tango.MultiAttrProp()
        assert attr.get_properties(supplied) is supplied
        props.label = 'Runtime label'
        attr.set_properties(props)
        assert attr.get_properties().label == 'Runtime label'

        attr.set_min_alarm('0.2')
        attr.set_max_alarm(2.0)
        attr.set_min_warning(0.3)
        attr.set_max_warning('1.7')
        assert attr.get_min_alarm() == 0.2
        assert attr.get_max_alarm() == 2.0
        assert attr.get_min_warning() == 0.3
        assert attr.get_max_warning() == 1.7

        writable = attrs.get_w_attr_by_name('value')
        writable.set_min_value('0.1')
        writable.set_max_value(3.0)
        assert writable.get_min_value() == 0.1
        assert writable.get_max_value() == 3.0

        config = self._get_attribute_config_3(['value'])[0]
        attr.set_upd_properties(config)
        attr.set_upd_properties(config, self.get_name())

    @command
    def remove_config(self):
        self.get_device_attr().get_attr_by_name('value').remove_configuration()

    @command(dtype_out=str)
    def progress(self):
        return 'ready'

    @command(dtype_in=str, dtype_out=str)
    def read_configuration(self, marker):
        Path(marker).touch()
        attr = self.get_device_attr().get_attr_by_name('value')
        return attr.get_properties().label

def set_concurrent_model():
    tango.Util.instance().set_serial_model(tango.SerialModel.NO_SYNC)

run((ConfigDevice,), args=['ConfigDevice', 'test'], pre_init_callback=set_concurrent_model)
"""
        env = os.environ.copy()
        env["TANGO_HOST"] = f"127.0.0.1:{port}"
        server_proc = Popen([sys.executable, "-u", "-c", server_code], cwd=TESTS_DIR, env=env, stdout=DEVNULL)
        proxy = wait_for_proxy(f"tango://127.0.0.1:{port}/test/config/1", retries=200, delay=0.05)
        proxy.set_timeout_millis(30000)
        config_events = queue.Queue()
        subscription_id = proxy.subscribe_event("value", EventType.ATTR_CONF_EVENT, config_events.put)
        assert not config_events.get(timeout=5).err

        completed = threading.Event()
        errors = []

        def update():
            try:
                proxy.change_alarm()
            except BaseException as exc:
                errors.append(exc)
            finally:
                completed.set()

        worker = threading.Thread(target=update, daemon=True)
        worker.start()
        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            try:
                line = db_proc.gil_test_lines.get(timeout=0.1)
            except queue.Empty:
                continue
            if "SLOW_DATABASE_COMMAND_ENTERED" in line:
                break
        else:
            pytest.fail("The configuration update did not reach the database")

        assert proxy.progress() == "ready"
        assert not completed.is_set(), "Configuration held the server GIL through its database RPC"
        config_result = []
        marker = tmp_path / "configuration-read-entered"
        config_reader = threading.Thread(
            target=lambda: config_result.append(proxy.read_configuration(str(marker))), daemon=True
        )
        config_reader.start()
        deadline = time.monotonic() + 1
        while not marker.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        assert marker.exists(), "The concurrent configuration read did not enter the handler"
        assert not completed.is_set(), "The writer finished before the configuration read entered"
        assert not config_result, "The read did not wait for the configuration monitor"
        worker.join(timeout=5)
        assert completed.is_set()
        config_reader.join(timeout=5)
        assert config_result == ["value"], "Concurrent configuration read did not complete"
        if errors:
            raise errors[0]
        assert not config_events.get(timeout=5).err

        proxy.exercise_properties()
        assert proxy.get_attribute_config("value").label == "Runtime label"
        proxy.remove_config()
    finally:
        if proxy is not None and subscription_id is not None:
            proxy.unsubscribe_event(subscription_id)
        if server_proc is not None:
            server_proc.terminate()
            server_proc.wait(timeout=10)
        db_proc.terminate()
        db_proc.wait(timeout=10)
        db_proc.stdout.close()
