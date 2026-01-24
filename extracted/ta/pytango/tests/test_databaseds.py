# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import logging
import os
import sys
import time

import pytest
import socket
from subprocess import Popen, PIPE

from tango import DevState, DbData, DbDatum
from tango.utils import ensure_binary
from tango.test_utils import wait_for_proxy

# Helpers

MAX_STARTUP_TIME_SEC = 30.0


def start_database(port, inst):
    python = sys.executable
    tests_directory = os.path.dirname(__file__)
    cmd = (
        f"{python} -u -m tango.databaseds.database"
        f" --host=127.0.0.1 --port={port}"
        f" --logging_level=2 {inst}"
    )
    env = os.environ.copy()
    env["PYTANGO_DATABASE_NAME"] = ":memory:"  # Don't write to disk
    logging.debug("Starting databaseds subprocess...")
    proc = Popen(
        cmd.split(), cwd=tests_directory, stdout=PIPE, bufsize=1, text=True, env=env
    )
    logging.debug("Waiting for databaseds to startup...")
    try:
        wait_for_tango_server_startup(proc)
    except RuntimeError:
        proc.terminate()
        raise

    return proc


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
