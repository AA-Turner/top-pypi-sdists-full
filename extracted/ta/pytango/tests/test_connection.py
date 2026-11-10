# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later

"""Regression coverage for explicit Connection calls that can block."""

import multiprocessing
import socket
import threading
import time

import pytest

from tango import DeviceProxy


def _check_connection_thread_progress(operation):
    from tango import DevFailed

    listener = socket.socket()
    listener.bind(("127.0.0.1", 0))
    listener.listen(5)
    port = listener.getsockname()[1]

    if operation == "connect":
        proxy = DeviceProxy("tango://127.0.0.1:1/test/no/server#dbase=no")
    else:
        proxy = DeviceProxy(f"tango://127.0.0.1:{port}/test/no/server#dbase=no")
    proxy.set_timeout_millis(500)

    progressed = threading.Event()
    timer = threading.Timer(0.1, progressed.set)
    timer.start()
    started = time.monotonic()
    try:
        if operation == "connect":
            proxy.connect(f"corbaloc:iiop:127.0.0.1:{port}/test/no/server")
        else:
            proxy.reconnect(False)
    except DevFailed as exc:
        progressed_during_call = progressed.is_set()
        elapsed = time.monotonic() - started
        assert "TRANSIENT_CallTimedout" in str(exc)
    else:
        raise AssertionError("The unanswered CORBA request succeeded")
    finally:
        timer.join(2)
        listener.close()

    assert elapsed >= 0.2, "The connection call returned too quickly (dummy endpoint should have delayed it)"
    assert progressed_during_call, "The Python timer could not run during the call"


@pytest.mark.extra_src_test
@pytest.mark.parametrize("operation", ["connect", "reconnect"])
def test_explicit_connection_wait_allows_python_thread_progress(operation, monkeypatch):
    monkeypatch.setenv("TANGOconnectTimeout", "500")
    process = multiprocessing.get_context("spawn").Process(target=_check_connection_thread_progress, args=(operation,))
    process.start()
    process.join(15)
    if process.is_alive():
        process.kill()
        process.join()
        pytest.fail(f"{operation} timed out")
    assert process.exitcode == 0, f"{operation} exited with code {process.exitcode}"


def test_get_fqdn_returns_python_string_after_native_lookup():
    assert isinstance(DeviceProxy.get_fqdn(), str)
