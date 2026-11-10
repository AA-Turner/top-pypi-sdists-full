# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
import pytest

from tango import DevFailed, ErrSeverity, Except


def _make_dev_failed():
    with pytest.raises(DevFailed) as info:
        Except.throw_exception("Reason", "Description", "Origin", ErrSeverity.ERR)
    return info.value


def test_print_exception(capfd):
    Except.print_exception(exception=_make_dev_failed())

    # cppTango prints the exception on stderr
    printed = capfd.readouterr().err
    assert "Reason" in printed
    assert "Description" in printed
    assert "Origin" in printed


def test_print_error_stack(capfd):
    Except.print_error_stack(_make_dev_failed().args)

    printed = capfd.readouterr().err
    assert "Reason" in printed
    assert "Description" in printed
    assert "Origin" in printed
