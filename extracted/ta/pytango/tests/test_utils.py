# SPDX-FileCopyrightText: All Contributors to the PyTango project
# SPDX-License-Identifier: LGPL-3.0-or-later
# -*- coding: utf-8 -*-

import operator
from threading import Event

import pytest

from tango import (
    AttrDataFormat,
    CmdArgType,
    DbData,
    DbDatum,
    DbDevExportInfo,
    DbDevExportInfos,
    DbDevImportInfo,
    DbDevImportInfos,
    DbDevInfo,
    DbDevInfos,
    DbHistory,
    DbHistoryList,
    DeviceData,
    DeviceDataHistory,
    DeviceDataHistoryList,
    DeviceDataList,
    StdDoubleVector,
    StdStringVector,
    is_omni_thread,
)
from tango._internal.instrumentation import _traced_coverage_run_active
from tango.tango_numpy import NumpyType
from tango.utils import (
    FROM_TANGO_TO_NUMPY_TYPE,
    TO_TANGO_TYPE,
    CaselessList,
    EventCallback,
    InvalidTangoHostTrlError,
    PyTangoThread,
    StdDoubleVector_2_seq,
    StdStringVector_2_seq,
    _clear_test_context_tango_host_fqtrl,
    _get_device_fqtrl_if_necessary,
    _get_test_context_tango_host_fqtrl,
    _set_test_context_tango_host_fqtrl,
    get_attrs,
    get_tango_type,
    is_binary,
    is_bool,
    is_devstate_seq,
    is_enum_seq,
    is_float,
    is_int,
    is_str,
    seq_2_DbData,
    seq_2_DbDevExportInfos,
    seq_2_DbDevInfos,
    seq_2_StdDoubleVector,
    seq_2_StdStringVector,
    seqStr_2_obj,
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
def test_get_trl_with_test_fqtrl_success(override_trl, input_trl, expected_trl, restore_global):
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
    from tango import AttrDataFormat, DevLong64, DevString

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


def check_vector_to_seq_conversion(vec_type, seq_type, vec_2_seq_func, seq_2_vec_func, elem, equal_op=operator.eq):

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
        assert isinstance(ret, list)
        assert len(ret) == 1
        assert equal_op(ret[0], elem)

        seq = []
        ret = vec_2_seq_func(vec, seq=seq)
        assert seq is ret
        assert isinstance(ret, list)
        assert len(ret) == 1
        assert equal_op(ret[0], elem)

        with pytest.raises(TypeError, match="vec must be"):
            vec_2_seq_func([], [])


def test_sequence_to_string_vector_and_back():

    check_vector_to_seq_conversion(StdStringVector, list, StdStringVector_2_seq, seq_2_StdStringVector, "abcd")


def test_sequence_to_double_vector_and_back():

    check_vector_to_seq_conversion(StdDoubleVector, list, StdDoubleVector_2_seq, seq_2_StdDoubleVector, 123.0)


def test_sequence_to_dbdevinfo_vector_and_back():

    info = DbDevInfo()
    info.klass = "a"
    info.name = "b"
    info.server = "c"

    def equal_op(left, right):
        return left.klass == right.klass and left.name == right.name and left.server == right.server

    check_vector_to_seq_conversion(DbDevInfos, list, None, seq_2_DbDevInfos, info, equal_op=equal_op)


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

    check_vector_to_seq_conversion(DbDevExportInfos, list, None, seq_2_DbDevExportInfos, info, equal_op=equal_op)


def test_sequence_to_dbdata_vector_and_back():

    info = DbDatum()
    info.name = "a"

    def equal_op(left, right):
        return left.name == right.name

    check_vector_to_seq_conversion(DbData, list, None, seq_2_DbData, info, equal_op=equal_op)


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

    check_vector_to_seq_conversion(DbDevImportInfos, list, None, seq_2_DbDevImportInfos, info, equal_op=equal_op)


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

    check_vector_to_seq_conversion(DbHistoryList, list, None, seq_2_DbHistoryList, hist, equal_op=equal_op)


def seq_2_DeviceDataList(seq, vec=None):
    return seq_2_x(DeviceDataList, seq, vec=vec)


def test_sequence_to_devicedatalist_vector_and_back():

    dd = DeviceData()
    dd.insert(TO_TANGO_TYPE[int], 1)

    def equal_op(left, right):
        return left.is_empty() == right.is_empty()

    check_vector_to_seq_conversion(DeviceDataList, list, None, seq_2_DeviceDataList, dd, equal_op=equal_op)


def seq_2_DeviceDataHistoryList(seq, vec=None):
    return seq_2_x(DeviceDataHistoryList, seq, vec=vec)


def test_sequence_to_devicedatahistorylist_vector_and_back():

    ddh = DeviceDataHistory()

    def equal_op(left, right):
        return left.has_failed() == right.has_failed()

    check_vector_to_seq_conversion(
        DeviceDataHistoryList,
        list,
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


def test_pytango_thread_runs_with_omni():

    my_event = Event()

    def target(event):
        if is_omni_thread():
            event.set()

    thread = PyTangoThread(target=target, args=(my_event,))
    thread.start()
    thread.join()
    assert my_event.is_set()
    my_event.clear()

    class myTangoTask(PyTangoThread):
        def __init__(self, event):
            super().__init__(target=self.run)
            self.event = event

        def run(self):
            if is_omni_thread():
                self.event.set()

    task = myTangoTask(my_event)
    task.start()
    task.join()
    assert my_event.is_set()


def test_numpy_type_mapping_agrees_with_the_general_one():
    for tango_type, expected in NumpyType.mapping.items():
        assert FROM_TANGO_TO_NUMPY_TYPE[tango_type] == expected


@pytest.mark.parametrize(
    "tg_type, tg_format, seq, expected",
    [
        (CmdArgType.DevLong, AttrDataFormat.SCALAR, ["7"], 7),
        (CmdArgType.DevDouble, AttrDataFormat.SCALAR, ["1.5"], 1.5),
        (CmdArgType.DevString, AttrDataFormat.SCALAR, ["abc"], "abc"),
        (CmdArgType.DevBoolean, AttrDataFormat.SCALAR, ["true"], True),
        (CmdArgType.DevLong, AttrDataFormat.SPECTRUM, ["1", "2"], [1, 2]),
        (CmdArgType.DevDouble, AttrDataFormat.SPECTRUM, ["1.5", "2.5"], [1.5, 2.5]),
        (CmdArgType.DevString, AttrDataFormat.SPECTRUM, ["a", "b"], ["a", "b"]),
        (CmdArgType.DevBoolean, AttrDataFormat.SPECTRUM, ["true", "0"], [True, False]),
        (
            CmdArgType.DevLong,
            AttrDataFormat.IMAGE,
            [["1", "2"], ["3", "4"]],
            [[1, 2], [3, 4]],
        ),
        (
            CmdArgType.DevDouble,
            AttrDataFormat.IMAGE,
            [["1.5"], ["2.5"]],
            [[1.5], [2.5]],
        ),
        (CmdArgType.DevString, AttrDataFormat.IMAGE, [["a"], ["b"]], [["a"], ["b"]]),
        (
            CmdArgType.DevBoolean,
            AttrDataFormat.IMAGE,
            [["true", "0"]],
            [[True, False]],
        ),
    ],
)
def test_seq_str_2_obj_honours_explicit_format(tg_type, tg_format, seq, expected):
    assert seqStr_2_obj(seq, tg_type, tg_format) == expected


@pytest.mark.parametrize(
    "tg_type, seq",
    [
        (CmdArgType.DevLong, ["7"]),
        (CmdArgType.DevDouble, ["1.5"]),
        (CmdArgType.DevString, ["abc"]),
        (CmdArgType.DevBoolean, ["true"]),
    ],
)
def test_seq_str_2_obj_scalar_format_matches_omitted_format(tg_type, seq):
    # AttrDataFormat.SCALAR is 0, so it must not be treated as "no format given".
    assert seqStr_2_obj(seq, tg_type, AttrDataFormat.SCALAR) == seqStr_2_obj(seq, tg_type)


@pytest.mark.parametrize("tg_type", [CmdArgType.DevEnum, CmdArgType.DevState, CmdArgType.DevEncoded])
def test_seq_str_2_obj_rejects_type_without_array_equivalent(tg_type):
    with pytest.raises(ValueError):
        seqStr_2_obj(["a"], tg_type, AttrDataFormat.SPECTRUM)


def test_caseless_list_index_finds_first_match_ignoring_case():
    assert CaselessList(["Abc", "def", "ABC"]).index("aBc") == 0
    assert CaselessList(["Abc", "def"]).index("DEF") == 1


def test_caseless_list_index_raises_value_error_when_absent():
    with pytest.raises(ValueError):
        CaselessList(["a", "b"]).index("zzz")


def test_caseless_list_index_raises_type_error_for_non_string():
    with pytest.raises(TypeError):
        CaselessList(["a"]).index(1)


@pytest.mark.parametrize(
    "entries, item, minindex, maxindex, expected",
    [
        (["a", "b", "c"], "b", 1, None, 1),
        (["a", "b", "c"], "c", 0, 3, 2),
        (["a", "b", "a"], "a", 1, None, 2),
    ],
)
def test_caseless_list_index_honours_bounds(entries, item, minindex, maxindex, expected):
    assert CaselessList(entries).index(item, minindex, maxindex) == expected


@pytest.mark.parametrize(
    "entries, item, minindex, maxindex",
    [
        # maxindex is exclusive, so the match at that position is out of range.
        (["a", "b"], "b", 0, 1),
        (["a", "b"], "a", 1, 2),
    ],
)
def test_caseless_list_index_excludes_out_of_range_match(entries, item, minindex, maxindex):
    with pytest.raises(ValueError):
        CaselessList(entries).index(item, minindex, maxindex)


def test_caseless_list_in_place_add_returns_the_list():
    entries = CaselessList(["a"])
    entries += ["b"]
    assert isinstance(entries, CaselessList)
    assert list(entries) == ["a", "b"]


def test_caseless_list_reflected_add_keeps_operand_order():
    # The concatenation operator is what is under test here, so it must not be
    # rewritten as unpacking.
    assert list(["x"] + CaselessList(["a"])) == ["x", "a"]  # noqa: RUF005


def test_caseless_list_add_keeps_operand_order():
    assert list(CaselessList(["a"]) + ["x"]) == ["a", "x"]  # noqa: RUF005


@pytest.mark.parametrize("empty", [[], (), [[]], [()]])
def test_is_devstate_seq_handles_empty_sequences(empty):
    # Must agree with is_enum_seq, which already guards against this.
    assert is_devstate_seq(empty) is False
    assert is_enum_seq(empty) is False


def test_get_attrs_reports_bad_dict_without_writing_to_stdout(capsys):
    class Meta(type):
        @property
        def __dict__(cls):
            return "not a mapping"

    class BadDict(metaclass=Meta):
        pass

    with pytest.raises(TypeError):
        get_attrs(BadDict)

    assert capsys.readouterr().out == ""


def test_event_callback_value_for_unknown_event_type():
    class UnknownEvent:
        err = False

    value = EventCallback()._get_value(UnknownEvent())
    assert isinstance(value, str)
    assert value


def test_event_callback_append_accepts_zero_sized_buffer():
    callback = EventCallback(max_buf=0)
    callback._append(object())
    assert callback.get_events() == []


@pytest.mark.parametrize(
    "predicate, scalar_type, array_type",
    [
        (is_binary, CmdArgType.DevEncoded, CmdArgType.DevVarCharArray),
        (is_int, CmdArgType.DevLong, CmdArgType.DevVarLongArray),
        (is_float, CmdArgType.DevDouble, CmdArgType.DevVarDoubleArray),
        (is_bool, CmdArgType.DevBoolean, CmdArgType.DevVarBooleanArray),
        (is_str, CmdArgType.DevString, CmdArgType.DevVarStringArray),
    ],
)
def test_type_predicates_gate_array_types_on_inc_array(predicate, scalar_type, array_type):
    assert predicate(scalar_type) is True
    assert predicate(scalar_type, True) is True
    assert predicate(array_type) is False
    assert predicate(array_type, True) is True
