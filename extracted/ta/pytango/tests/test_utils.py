# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -*- coding: utf-8 -*-

import pytest

from typing import List

import operator

from tango import (
    StdStringVector,
    StdDoubleVector,
    DbDevInfos,
    DbDevInfo,
    DbDevImportInfos,
    DbDevImportInfo,
    DbDevExportInfo,
    DbDevExportInfos,
    DbHistory,
    DbHistoryList,
    DbData,
    DbDatum,
    DeviceData,
    DeviceDataList,
    DeviceDataHistory,
    DeviceDataHistoryList,
)

from tango.utils import (
    _clear_test_context_tango_host_fqtrl,
    _get_device_fqtrl_if_necessary,
    _get_test_context_tango_host_fqtrl,
    _set_test_context_tango_host_fqtrl,
    _traced_coverage_run_active,
    InvalidTangoHostTrlError,
    StdStringVector_2_seq,
    StdDoubleVector_2_seq,
    seq_2_StdStringVector,
    seq_2_StdDoubleVector,
    seq_2_DbDevInfos,
    seq_2_DbDevExportInfos,
    seq_2_DbData,
    get_tango_type,
    TO_TANGO_TYPE,
)


@pytest.fixture()
def restore_global():
    yield
    _clear_test_context_tango_host_fqtrl()


@pytest.mark.parametrize(
    "override_trl, input_trl, expected_trl",
    [
        (None, "a/b/c", "a/b/c"),
        (None, "a/b/c/d", "a/b/c/d"),
        (None, "tango://host:12/a/b/c", "tango://host:12/a/b/c"),
        (None, "tango://host:12/a/b/c#dbase=no", "tango://host:12/a/b/c#dbase=no"),
        (None, "no://trl/validation", "no://trl/validation"),
        ("tango://host:12", "a/b/c", "tango://host:12/a/b/c"),
        ("tango://host:12", "a/b/c/d", "tango://host:12/a/b/c/d"),
        ("tango://host:12", "tango://host:12/a/b/c", "tango://host:12/a/b/c"),
        ("tango://host:12#dbase=no", "a/b/c", "tango://host:12/a/b/c#dbase=no"),
        ("tango://host:12#dbase=yes", "a/b/c", "tango://host:12/a/b/c#dbase=yes"),
        ("tango://127.0.0.1:12", "a/b/c", "tango://127.0.0.1:12/a/b/c"),
    ],
)
def test_get_trl_with_test_fqtrl_success(
    override_trl, input_trl, expected_trl, restore_global
):
    _set_test_context_tango_host_fqtrl(override_trl)
    actual_trl = _get_device_fqtrl_if_necessary(input_trl)
    assert actual_trl == expected_trl


@pytest.mark.parametrize(
    "override_trl, input_trl",
    [
        ("host:123", "a/b/c"),  # missing scheme
        ("tango://", "a/b/c"),  # missing hostname and port
        ("tango://:123", "a/b/c"),  # missing hostname
        ("tango://host", "a/b/c"),  # missing port
        ("tango://host:0", "a/b/c"),  # zero-value port
        ("tango://host:12/path", "a/b/c"),  # non-empty path
        ("tango://host:123?query=1", "a/b/c"),  # non-empty query
        ("tango://host:123#dbase=invalid", "a/b/c"),  # invalid fragment
    ],
)
def test_get_trl_with_test_fdqn_failure(override_trl, input_trl, restore_global):
    _set_test_context_tango_host_fqtrl(override_trl)
    with pytest.raises(InvalidTangoHostTrlError):
        _ = _get_device_fqtrl_if_necessary(input_trl)


def test_global_state_default_set_and_clear(restore_global):
    default = _get_test_context_tango_host_fqtrl()
    _set_test_context_tango_host_fqtrl("tango://localhost:1234")
    after_set = _get_test_context_tango_host_fqtrl()
    _clear_test_context_tango_host_fqtrl()
    after_clear = _get_test_context_tango_host_fqtrl()

    assert default is None
    assert after_set == "tango://localhost:1234"
    assert after_clear is None


def test_clear_global_var_without_set_does_not_raise():
    _clear_test_context_tango_host_fqtrl()


def test_get_tango_type_valid():
    from tango import DevString, DevLong64, AttrDataFormat

    assert get_tango_type("abc") == (DevString, AttrDataFormat.SCALAR)
    assert get_tango_type(123) == (DevLong64, AttrDataFormat.SCALAR)
    assert get_tango_type([1, 2, 3]) == (DevLong64, AttrDataFormat.SPECTRUM)
    assert get_tango_type([[1, 2, 3], [4, 5, 6]]) == (DevLong64, AttrDataFormat.IMAGE)


def test_get_tango_type_invalid_raises_type_error():
    class NonTangoType:
        pass

    with pytest.raises(TypeError):
        get_tango_type(NonTangoType())
    with pytest.raises(TypeError):
        get_tango_type([{"start with": "invalid type"}, "abc", 123])
    # TODO: check data type for all nested items.  E.g., this doesn't raise TypeError:  ["abc", 123, {"k": "v"}]


def check_vector_to_seq_conversion(
    vec_type, seq_type, vec_2_seq_func, seq_2_vec_func, elem, equal_op=operator.eq
):

    vec = vec_type()

    ret = seq_2_vec_func(vec)
    assert vec is ret

    ret = seq_2_vec_func([elem], vec)
    assert vec is ret
    assert isinstance(ret, vec_type)
    assert len(ret) == 1
    assert equal_op(ret[0], elem)

    ret = seq_2_vec_func([elem])
    assert isinstance(ret, vec_type)
    assert len(ret) == 1
    assert equal_op(ret[0], elem)

    with pytest.raises(TypeError, match="vec must be"):
        seq_2_vec_func([], [])

    if vec_2_seq_func is not None:

        vec = vec_type()
        vec.append(elem)

        ret = vec_2_seq_func(vec)
        assert isinstance(ret, List)
        assert len(ret) == 1
        assert equal_op(ret[0], elem)

        seq = []
        ret = vec_2_seq_func(vec, seq=seq)
        assert seq is ret
        assert isinstance(ret, List)
        assert len(ret) == 1
        assert equal_op(ret[0], elem)

        with pytest.raises(TypeError, match="vec must be"):
            vec_2_seq_func([], [])


def test_sequence_to_string_vector_and_back():

    check_vector_to_seq_conversion(
        StdStringVector, List, StdStringVector_2_seq, seq_2_StdStringVector, "abcd"
    )


def test_sequence_to_double_vector_and_back():

    check_vector_to_seq_conversion(
        StdDoubleVector, List, StdDoubleVector_2_seq, seq_2_StdDoubleVector, 123.0
    )


def test_sequence_to_dbdevinfo_vector_and_back():

    info = DbDevInfo()
    info.klass = "a"
    info.name = "b"
    info.server = "c"

    def equal_op(left, right):
        return (
            left.klass == right.klass
            and left.name == right.name
            and left.server == right.server
        )

    check_vector_to_seq_conversion(
        DbDevInfos, List, None, seq_2_DbDevInfos, info, equal_op=equal_op
    )


def test_sequence_to_dbdevexportinfo_vector_and_back():

    info = DbDevExportInfo()
    info.name = "a"
    info.ior = "b"
    info.host = "c"
    info.version = "d"
    info.pid = 123

    def equal_op(left, right):
        return (
            left.name == right.name
            and left.ior == right.ior
            and left.host == right.host
            and left.version == right.version
            and left.pid == right.pid
        )

    check_vector_to_seq_conversion(
        DbDevExportInfos, List, None, seq_2_DbDevExportInfos, info, equal_op=equal_op
    )


def test_sequence_to_dbdata_vector_and_back():

    info = DbDatum()
    info.name = "a"

    def equal_op(left, right):
        return left.name == right.name

    check_vector_to_seq_conversion(
        DbData, List, None, seq_2_DbData, info, equal_op=equal_op
    )


def seq_2_x(vec_type, seq, vec=None):
    if vec is None:
        if isinstance(seq, vec_type):
            return seq
        vec = vec_type()
    if not isinstance(vec, vec_type):
        raise TypeError("vec must be a ...")
    for e in seq:
        vec.append(e)
    return vec


def seq_2_DbDevImportInfos(seq, vec=None):
    return seq_2_x(DbDevImportInfos, seq, vec=vec)


def test_sequence_to_dbdevimport_vector_and_back():

    info = DbDevImportInfo()

    def equal_op(left, right):
        return (
            left.name == right.name
            and left.exported == right.exported
            and left.ior == right.ior
            and left.version == right.version
        )

    check_vector_to_seq_conversion(
        DbDevImportInfos, List, None, seq_2_DbDevImportInfos, info, equal_op=equal_op
    )


def seq_2_DbHistoryList(seq, vec=None):
    return seq_2_x(DbHistoryList, seq, vec=vec)


def test_sequence_to_dbhistorylist_vector_and_back():

    # second string, the date, is long enough that DbHistory::format_mysql_date in cppTango does not barf
    hist = DbHistory("a", "b" * 12, StdStringVector())

    def equal_op(left, right):
        return (
            left.get_attribute_name() == right.get_attribute_name()
            and left.get_date() == right.get_date()
            and left.get_name() == right.get_name()
            and left.get_value().name == right.get_value().name
        )

    check_vector_to_seq_conversion(
        DbHistoryList, List, None, seq_2_DbHistoryList, hist, equal_op=equal_op
    )


def seq_2_DeviceDataList(seq, vec=None):
    return seq_2_x(DeviceDataList, seq, vec=vec)


def test_sequence_to_devicedatalist_vector_and_back():

    dd = DeviceData()
    dd.insert(TO_TANGO_TYPE[int], 1)

    def equal_op(left, right):
        return left.is_empty() == right.is_empty()

    check_vector_to_seq_conversion(
        DeviceDataList, List, None, seq_2_DeviceDataList, dd, equal_op=equal_op
    )


def seq_2_DeviceDataHistoryList(seq, vec=None):
    return seq_2_x(DeviceDataHistoryList, seq, vec=vec)


def test_sequence_to_devicedatahistorylist_vector_and_back():

    ddh = DeviceDataHistory()

    def equal_op(left, right):
        return left.has_failed() == right.has_failed()

    check_vector_to_seq_conversion(
        DeviceDataHistoryList,
        List,
        None,
        seq_2_DeviceDataHistoryList,
        ddh,
        equal_op=equal_op,
    )


def test_report_coverage_tracing_enabled():
    # The point of this test is to have something in the test
    # output that shows if coverage tracing is active or not.
    # If it isn't active, we skip the test.
    if not _traced_coverage_run_active:
        pytest.skip("Coverage tracing is disabled")
    assert _traced_coverage_run_active
