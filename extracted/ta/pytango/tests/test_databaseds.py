# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import os
import pytest
import socket
import sys
from time import sleep
from subprocess import Popen
from tango import DeviceProxy, DevState, DevFailed


# Helpers


def start_database(port, inst):
    python = sys.executable
    tests_directory = os.path.dirname(__file__)
    cmd = (
        f"{python} -m tango.databaseds.database"
        f" --host 127.0.0.1 --port={port} --logging_level=2 {inst}"
    )
    env = os.environ.copy()
    env["PYTANGO_DATABASE_NAME"] = ":memory:"  # Don't write to disk
    proc = Popen(cmd.split(), cwd=tests_directory, env=env)
    sleep(1)
    return proc


def get_device_proxy(name, retries=400, delay=0.03):
    count = 0
    while count < retries:
        try:
            proxy = DeviceProxy(name)
            return proxy
        except DevFailed as exc:
            last_error = str(exc)
            sleep(delay)
        count += 1
    raise RuntimeError(
        f"Database proxy did not start up within {count * delay:.1f} sec!\n"
        f"Last error: {last_error}."
    )


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
    proxy = get_device_proxy(f"tango://127.0.0.1:{port}/sys/database/2")

    yield proxy

    proc.terminate()


# Tests
def test_ping(tango_database_test):
    duration = tango_database_test.ping(wait=True)
    assert isinstance(duration, int)


def test_status(tango_database_test):
    assert tango_database_test.status() == "The device is in ON state."


def test_state(tango_database_test):
    assert tango_database_test.state() == DevState.ON


def test_device_property(tango_database_test):
    test_property_name = "test property"
    test_property_value = "test property text"

    tango_database_test.put_property({test_property_name: test_property_value})
    return_property_list = tango_database_test.get_property_list("*")
    assert len(return_property_list) == 1
    assert return_property_list[0] == test_property_name

    return_property = tango_database_test.get_property("test property")
    assert return_property[test_property_name][0] == test_property_value


def test_info(tango_database_test):
    info = tango_database_test.info()

    assert info.dev_class == "DataBase"
    assert info.doc_url == "Doc URL = http://www.tango-controls.org"
    assert info.server_id == "DataBaseds/2"
