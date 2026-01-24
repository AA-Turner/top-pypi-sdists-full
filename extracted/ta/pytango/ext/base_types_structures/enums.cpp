/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "pyutils.h"

void export_enums(py::module_ &m) {
    py::native_enum<Tango::LockerLanguage>(m,
                                           "LockerLanguage",
                                           "enum.IntEnum",
                                           R"doc(
    An enumeration representing the programming language in which the client application who locked is written.

    New in PyTango 7.0.0)doc")
        .value("CPP", Tango::CPP, "C++/Python language")
        .value("JAVA", Tango::JAVA, "Java language")
        .value("CPP_6", Tango::CPP_6, "C++/Python language, IDL 6")
        .value("JAVA_6", Tango::JAVA_6, "Java language, IDL 6")
        .finalize();
    py::object locker_language_class = m.attr("LockerLanguage");
    add_names_values_to_native_enum(locker_language_class);

    py::native_enum<Tango::CmdArgType>(m,
                                       "CmdArgType",
                                       "enum.IntEnum",
                                       "An enumeration representing the Tango data types.")
        .value(Tango::data_type_to_string(Tango::DEV_VOID), Tango::DEV_VOID)
        .value(Tango::data_type_to_string(Tango::DEV_BOOLEAN), Tango::DEV_BOOLEAN)
        .value(Tango::data_type_to_string(Tango::DEV_SHORT), Tango::DEV_SHORT)
        .value(Tango::data_type_to_string(Tango::DEV_LONG), Tango::DEV_LONG)
        .value(Tango::data_type_to_string(Tango::DEV_FLOAT), Tango::DEV_FLOAT)
        .value(Tango::data_type_to_string(Tango::DEV_DOUBLE), Tango::DEV_DOUBLE)
        .value(Tango::data_type_to_string(Tango::DEV_USHORT), Tango::DEV_USHORT)
        .value(Tango::data_type_to_string(Tango::DEV_ULONG), Tango::DEV_ULONG)
        .value(Tango::data_type_to_string(Tango::DEV_STRING), Tango::DEV_STRING)
        .value(Tango::data_type_to_string(Tango::DEVVAR_CHARARRAY), Tango::DEVVAR_CHARARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_SHORTARRAY), Tango::DEVVAR_SHORTARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_LONGARRAY), Tango::DEVVAR_LONGARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_FLOATARRAY), Tango::DEVVAR_FLOATARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_DOUBLEARRAY), Tango::DEVVAR_DOUBLEARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_USHORTARRAY), Tango::DEVVAR_USHORTARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_ULONGARRAY), Tango::DEVVAR_ULONGARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_STRINGARRAY), Tango::DEVVAR_STRINGARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_LONGSTRINGARRAY), Tango::DEVVAR_LONGSTRINGARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_DOUBLESTRINGARRAY), Tango::DEVVAR_DOUBLESTRINGARRAY)
        .value(Tango::data_type_to_string(Tango::DEV_STATE), Tango::DEV_STATE)
        .value(Tango::data_type_to_string(Tango::CONST_DEV_STRING), Tango::CONST_DEV_STRING)
        .value(Tango::data_type_to_string(Tango::DEVVAR_BOOLEANARRAY), Tango::DEVVAR_BOOLEANARRAY)
        .value(Tango::data_type_to_string(Tango::DEV_UCHAR), Tango::DEV_UCHAR)
        .value(Tango::data_type_to_string(Tango::DEV_LONG64), Tango::DEV_LONG64)
        .value(Tango::data_type_to_string(Tango::DEV_ULONG64), Tango::DEV_ULONG64)
        .value(Tango::data_type_to_string(Tango::DEVVAR_LONG64ARRAY), Tango::DEVVAR_LONG64ARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_ULONG64ARRAY), Tango::DEVVAR_ULONG64ARRAY)
        .value(Tango::data_type_to_string(Tango::DEV_ENCODED), Tango::DEV_ENCODED)
        .value(Tango::data_type_to_string(Tango::DEV_ENUM), Tango::DEV_ENUM)
        // skip DEV_PIPE_BLOB, as support removed from PyTango in 10.1.0
        .value(Tango::data_type_to_string(Tango::DEVVAR_STATEARRAY), Tango::DEVVAR_STATEARRAY)
        .value(Tango::data_type_to_string(Tango::DEVVAR_ENCODEDARRAY), Tango::DEVVAR_ENCODEDARRAY)
        .value(Tango::data_type_to_string(Tango::DATA_TYPE_UNKNOWN), Tango::DATA_TYPE_UNKNOWN)
        .finalize();
    py::object cmd_arg_type_class = m.attr("CmdArgType");
    add_names_values_to_native_enum(cmd_arg_type_class);

    /*
     * It is stupid, but I have to do it to maintain backward compatibility:
     *
     * Historically, PyTango was written with Boost, and Boost allows to overwrite exported DevState
     * data type with DevState Enum. PyBind11 does not allow it (and is absolutely right, imho, while Boost has bug),
     * so I have to export manually all values, except DevState
     *
     * My best greetings to cpp, where they define under the same name "DevState" both Enum and data type....
     */

    m.attr(Tango::data_type_to_string(Tango::DEV_VOID)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_VOID));
    m.attr(Tango::data_type_to_string(Tango::DEV_BOOLEAN)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_BOOLEAN));
    m.attr(Tango::data_type_to_string(Tango::DEV_SHORT)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_SHORT));
    m.attr(Tango::data_type_to_string(Tango::DEV_LONG)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_LONG));
    m.attr(Tango::data_type_to_string(Tango::DEV_FLOAT)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_FLOAT));
    m.attr(Tango::data_type_to_string(Tango::DEV_DOUBLE)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_DOUBLE));
    m.attr(Tango::data_type_to_string(Tango::DEV_USHORT)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_USHORT));
    m.attr(Tango::data_type_to_string(Tango::DEV_ULONG)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_ULONG));
    m.attr(Tango::data_type_to_string(Tango::DEV_STRING)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_STRING));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_CHARARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_CHARARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_SHORTARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_SHORTARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_LONGARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_LONGARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_FLOATARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_FLOATARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_DOUBLEARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_DOUBLEARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_USHORTARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_USHORTARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_ULONGARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_ULONGARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_STRINGARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_STRINGARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_LONGSTRINGARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_LONGSTRINGARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_DOUBLESTRINGARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_DOUBLESTRINGARRAY));
    // The whole buzz is because of this export.
    // m.attr(Tango::data_type_to_string(Tango::DEV_STATE)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_STATE));
    m.attr(Tango::data_type_to_string(Tango::CONST_DEV_STRING)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::CONST_DEV_STRING));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_BOOLEANARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_BOOLEANARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEV_UCHAR)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_UCHAR));
    m.attr(Tango::data_type_to_string(Tango::DEV_LONG64)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_LONG64));
    m.attr(Tango::data_type_to_string(Tango::DEV_ULONG64)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_ULONG64));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_LONG64ARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_LONG64ARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_ULONG64ARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_ULONG64ARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEV_ENCODED)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_ENCODED));
    m.attr(Tango::data_type_to_string(Tango::DEV_ENUM)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEV_ENUM));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_STATEARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_STATEARRAY));
    m.attr(Tango::data_type_to_string(Tango::DEVVAR_ENCODEDARRAY)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DEVVAR_ENCODEDARRAY));
    m.attr(Tango::data_type_to_string(Tango::DATA_TYPE_UNKNOWN)) = cmd_arg_type_class.attr(Tango::data_type_to_string(Tango::DATA_TYPE_UNKNOWN));

    py::native_enum<Tango::MessBoxType>(m,
                                        "MessBoxType",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the MessBoxType

    New in PyTango 7.0.0)doc")
        .value("STOP", Tango::STOP)
        .value("INFO", Tango::INFO)
        .finalize();
    py::object mess_box_type_class = m.attr("MessBoxType");
    add_names_values_to_native_enum(mess_box_type_class);

    py::native_enum<Tango::PollObjType>(m,
                                        "PollObjType",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the PollObjType

    New in PyTango 7.0.0)doc")
        .value("POLL_CMD", Tango::POLL_CMD)
        .value("POLL_ATTR", Tango::POLL_ATTR)
        .value("EVENT_HEARTBEAT", Tango::EVENT_HEARTBEAT)
        .value("STORE_SUBDEV", Tango::STORE_SUBDEV)
        .finalize();
    py::object poll_obj_type_class = m.attr("PollObjType");
    add_names_values_to_native_enum(poll_obj_type_class);

    py::native_enum<Tango::PollCmdCode>(m,
                                        "PollCmdCode",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the PollCmdCode

    New in PyTango 7.0.0)doc")
        .value("POLL_ADD_OBJ", Tango::POLL_ADD_OBJ)
        .value("POLL_REM_OBJ", Tango::POLL_REM_OBJ)
        .value("POLL_START", Tango::POLL_START)
        .value("POLL_STOP", Tango::POLL_STOP)
        .value("POLL_UPD_PERIOD", Tango::POLL_UPD_PERIOD)
        .value("POLL_REM_DEV", Tango::POLL_REM_DEV)
        .value("POLL_EXIT", Tango::POLL_EXIT)
        .value("POLL_REM_EXT_TRIG_OBJ", Tango::POLL_REM_EXT_TRIG_OBJ)
        .value("POLL_ADD_HEARTBEAT", Tango::POLL_ADD_HEARTBEAT)
        .value("POLL_REM_HEARTBEAT", Tango::POLL_REM_HEARTBEAT)
        .finalize();
    py::object poll_cmd_code_class = m.attr("PollCmdCode");
    add_names_values_to_native_enum(poll_cmd_code_class);

    py::native_enum<Tango::SerialModel>(m,
                                        "SerialModel",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the type of serialization performed by the device server)doc")
        .value("BY_DEVICE", Tango::BY_DEVICE)
        .value("BY_CLASS", Tango::BY_CLASS)
        .value("BY_PROCESS", Tango::BY_PROCESS)
        .value("NO_SYNC", Tango::NO_SYNC)
        .finalize();
    py::object serial_model_class = m.attr("SerialModel");
    add_names_values_to_native_enum(serial_model_class);

    py::native_enum<Tango::AttReqType>(m,
                                       "AttReqType",
                                       "enum.IntEnum",
                                       "An enumeration representing the type of attribute request")
        .value("READ_REQ", Tango::READ_REQ)
        .value("WRITE_REQ", Tango::WRITE_REQ)
        .finalize();
    py::object att_req_type_class = m.attr("AttReqType");
    add_names_values_to_native_enum(att_req_type_class);

    py::native_enum<Tango::LockCmdCode>(m,
                                        "LockCmdCode",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the LockCmdCode

    New in PyTango 7.0.0)doc")
        .value("LOCK_ADD_DEV", Tango::LOCK_ADD_DEV)
        .value("LOCK_REM_DEV", Tango::LOCK_REM_DEV)
        .value("LOCK_UNLOCK_ALL_EXIT", Tango::LOCK_UNLOCK_ALL_EXIT)
        .value("LOCK_EXIT", Tango::LOCK_EXIT)
        .finalize();
    py::object lock_cmd_code_class = m.attr("LockCmdCode");
    add_names_values_to_native_enum(lock_cmd_code_class);

    py::native_enum<Tango::LogLevel>(m,
                                     "LogLevel",
                                     "enum.IntEnum",
                                     R"doc(
    An enumeration representing the LogLevel

    New in PyTango 7.0.0)doc")
        .value("LOG_OFF", Tango::LOG_OFF)
        .value("LOG_FATAL", Tango::LOG_FATAL)
        .value("LOG_ERROR", Tango::LOG_ERROR)
        .value("LOG_WARN", Tango::LOG_WARN)
        .value("LOG_INFO", Tango::LOG_INFO)
        .value("LOG_DEBUG", Tango::LOG_DEBUG)
        .finalize();
    py::object log_level_class = m.attr("LogLevel");
    add_names_values_to_native_enum(log_level_class);

    py::native_enum<Tango::LogTarget>(m,
                                      "LogTarget",
                                      "enum.IntEnum",
                                      R"doc(
    An enumeration representing the LogTarget

    New in PyTango 7.0.0)doc")
        .value("LOG_CONSOLE", Tango::LOG_CONSOLE)
        .value("LOG_FILE", Tango::LOG_FILE)
        .value("LOG_DEVICE", Tango::LOG_DEVICE)
        .finalize();
    py::object log_target_class = m.attr("LogTarget");
    add_names_values_to_native_enum(log_target_class);

    py::native_enum<Tango::EventType>(m,
                                      "EventType",
                                      "enum.IntEnum",
                                      R"doc(

    An enumeration representing event type

    .. versionchanged:: 7.0.0 Added DATA_READY_EVENT
    .. versionchanged:: 9.2.2 Added INTERFACE_CHANGE_EVENT\n
    .. versionchanged:: 10.0.0 Added ALARM_EVENT
    .. versionchanged:: 10.0.0 Removed QUALITY_EVENT
    .. versionchanged:: 10.1.0 Removed PIPE_EVENT)doc")
        .value("CHANGE_EVENT", Tango::CHANGE_EVENT)
        .value("PERIODIC_EVENT", Tango::PERIODIC_EVENT)
        .value("ARCHIVE_EVENT", Tango::ARCHIVE_EVENT)
        .value("USER_EVENT", Tango::USER_EVENT)
        .value("ATTR_CONF_EVENT", Tango::ATTR_CONF_EVENT)
        .value("DATA_READY_EVENT", Tango::DATA_READY_EVENT)
        .value("INTERFACE_CHANGE_EVENT", Tango::INTERFACE_CHANGE_EVENT)
        .value("ALARM_EVENT", Tango::ALARM_EVENT)
        .finalize();
    py::object event_type_class = m.attr("EventType");
    add_names_values_to_native_enum(event_type_class);

    py::native_enum<Tango::AttrSerialModel>(m,
                                            "AttrSerialModel",
                                            "enum.IntEnum",
                                            R"doc(
    An enumeration representing the AttrSerialModel

    New in PyTango 7.1.0)doc")
        .value("ATTR_NO_SYNC", Tango::ATTR_NO_SYNC)
        .value("ATTR_BY_KERNEL", Tango::ATTR_BY_KERNEL)
        .value("ATTR_BY_USER", Tango::ATTR_BY_USER)
        .finalize();
    py::object attr_serial_model_class = m.attr("AttrSerialModel");
    add_names_values_to_native_enum(attr_serial_model_class);

    py::native_enum<Tango::KeepAliveCmdCode>(m,
                                             "KeepAliveCmdCode",
                                             "enum.IntEnum",
                                             R"doc(
    An enumeration representing the KeepAliveCmdCode

    New in PyTango 7.1.0)doc")
        .value("EXIT_TH", Tango::EXIT_TH)
        .finalize();
    py::object keep_alive_cmd_code_class = m.attr("KeepAliveCmdCode");
    add_names_values_to_native_enum(keep_alive_cmd_code_class);

    py::native_enum<Tango::AccessControlType>(m,
                                              "AccessControlType",
                                              "enum.IntEnum",
                                              R"doc(
    An enumeration representing the AccessControlType

    New in PyTango 7.0.0)doc")
        .value("ACCESS_READ", Tango::ACCESS_READ)
        .value("ACCESS_WRITE", Tango::ACCESS_WRITE)
        .finalize();
    py::object access_control_type_class = m.attr("AccessControlType");
    add_names_values_to_native_enum(access_control_type_class);

    py::native_enum<Tango::asyn_req_type>(m,
                                          "asyn_req_type",
                                          "enum.IntEnum",
                                          "An enumeration representing the asynchronous request type")
        .value("POLLING", Tango::POLLING)
        .value("CALLBACK", Tango::CALL_BACK)
        .value("ALL_ASYNCH", Tango::ALL_ASYNCH)
        .finalize();
    py::object asyn_req_type_class = m.attr("asyn_req_type");
    add_names_values_to_native_enum(asyn_req_type_class);

    py::native_enum<Tango::cb_sub_model>(m,
                                         "cb_sub_model",
                                         "enum.IntEnum",
                                         "An enumeration representing callback sub model")
        .value("PUSH_CALLBACK", Tango::PUSH_CALLBACK)
        .value("PULL_CALLBACK", Tango::PULL_CALLBACK)
        .finalize();
    py::object cb_sub_model_class = m.attr("cb_sub_model");
    add_names_values_to_native_enum(cb_sub_model_class);

    //
    // Tango IDL
    //

    py::native_enum<Tango::AttrQuality>(m,
                                        "AttrQuality",
                                        "enum.IntEnum",
                                        "An enumeration representing the attribute quality")
        .value("ATTR_VALID", Tango::ATTR_VALID)
        .value("ATTR_INVALID", Tango::ATTR_INVALID)
        .value("ATTR_ALARM", Tango::ATTR_ALARM)
        .value("ATTR_CHANGING", Tango::ATTR_CHANGING)
        .value("ATTR_WARNING", Tango::ATTR_WARNING)
        .finalize();
    py::object attr_quality_class = m.attr("AttrQuality");
    add_names_values_to_native_enum(attr_quality_class);

    py::native_enum<Tango::AttrWriteType>(m,
                                          "AttrWriteType",
                                          "enum.IntEnum",
                                          "An enumeration representing the attribute type")
        .value("READ", Tango::READ)
        .value("READ_WITH_WRITE", Tango::READ_WITH_WRITE)
        .value("WRITE", Tango::WRITE)
        .value("READ_WRITE", Tango::READ_WRITE)
        .value("WT_UNKNOWN", Tango::WT_UNKNOWN)
        .export_values()
        .finalize();
    py::object attr_write_type_class = m.attr("AttrWriteType");
    add_names_values_to_native_enum(attr_write_type_class);

    py::native_enum<Tango::AttrDataFormat>(m,
                                           "AttrDataFormat",
                                           "enum.IntEnum",
                                           "An enumeration representing the attribute format")
        .value("SCALAR", Tango::SCALAR)
        .value("SPECTRUM", Tango::SPECTRUM)
        .value("IMAGE", Tango::IMAGE)
        .value("FMT_UNKNOWN", Tango::FMT_UNKNOWN)
        .export_values()
        .finalize();
    py::object attr_data_format_class = m.attr("AttrDataFormat");
    add_names_values_to_native_enum(attr_data_format_class);

    py::native_enum<Tango::DevSource>(m,
                                      "DevSource",
                                      "enum.IntEnum",
                                      "An enumeration representing the device source for data")
        .value("DEV", Tango::DEV)
        .value("CACHE", Tango::CACHE)
        .value("CACHE_DEV", Tango::CACHE_DEV)
        .finalize();
    py::object dev_source_class = m.attr("DevSource");
    add_names_values_to_native_enum(dev_source_class);

    py::native_enum<Tango::ErrSeverity>(m,
                                        "ErrSeverity",
                                        "enum.IntEnum",
                                        "An enumeration representing the error severity")
        .value("WARN", Tango::WARN)
        .value("ERR", Tango::ERR)
        .value("PANIC", Tango::PANIC)
        .finalize();
    py::object err_severity_class = m.attr("ErrSeverity");
    add_names_values_to_native_enum(err_severity_class);

    py::native_enum<Tango::DevState>(m,
                                     "DevState",
                                     "enum.IntEnum",
                                     "An enumeration representing the device state")
        .value(Tango::DevStateName[Tango::ON], Tango::ON)
        .value(Tango::DevStateName[Tango::OFF], Tango::OFF)
        .value(Tango::DevStateName[Tango::CLOSE], Tango::CLOSE)
        .value(Tango::DevStateName[Tango::OPEN], Tango::OPEN)
        .value(Tango::DevStateName[Tango::INSERT], Tango::INSERT)
        .value(Tango::DevStateName[Tango::EXTRACT], Tango::EXTRACT)
        .value(Tango::DevStateName[Tango::MOVING], Tango::MOVING)
        .value(Tango::DevStateName[Tango::STANDBY], Tango::STANDBY)
        .value(Tango::DevStateName[Tango::FAULT], Tango::FAULT)
        .value(Tango::DevStateName[Tango::INIT], Tango::INIT)
        .value(Tango::DevStateName[Tango::RUNNING], Tango::RUNNING)
        .value(Tango::DevStateName[Tango::ALARM], Tango::ALARM)
        .value(Tango::DevStateName[Tango::DISABLE], Tango::DISABLE)
        .value(Tango::DevStateName[Tango::UNKNOWN], Tango::UNKNOWN)
        .finalize();
    py::object dev_state_class = m.attr("DevState");
    add_names_values_to_native_enum(dev_state_class);

    py::native_enum<Tango::DispLevel>(m,
                                      "DispLevel",
                                      "enum.IntEnum",
                                      "An enumeration representing the display level")
        .value("OPERATOR", Tango::OPERATOR)
        .value("EXPERT", Tango::EXPERT)
        .value("DL_UNKNOWN", Tango::DL_UNKNOWN)
        .finalize();
    py::object disp_level_class = m.attr("DispLevel");
    add_names_values_to_native_enum(disp_level_class);

    py::native_enum<Tango::EventSubMode>(m,
                                         "EventSubMode",
                                         "enum.IntEnum",
                                         R"doc(
    An enumeration representing the sub mode used when subscribing to events.

    * ``EventSubMode.SyncRead`` - synchronous subscription including attribute read (raises exception on failure), first callback immediately with current value.
    * ``EventSubMode.AsyncRead`` - asynchronous subscription and asynchronous attribute read (no exception on failure, retries automatically), first callback "soon" after read with current value.
    * ``EventSubMode.Sync`` - synchronous subscription without reading attribute (raises exception on failure), no callback on subscription (only on next event).
    * ``EventSubMode.Async`` - asynchronous subscription without reading attribute (no exception on failure, retries automatically), first callback with no value when subscription completed.
    * ``EventSubMode.Stateless`` - synchronous subscription including attribute read (no exception on failure, retries automatically) - equivalent to old stateless=True option, first callback immediately with current value.  Consider ``AsyncRead`` instead.

    The table below summarises this:

    .. list-table:: Event Subscription Modes
       :header-rows: 1

       * - EventSubMode
         - Tries subscription before returning
         - Raises on subscription failure
         - Reads entity
         - First callback
       * - SyncRead
         - Yes
         - Yes
         - Yes, during subscription
         - Immediately, with data
       * - AsyncRead
         - No
         - No
         - Yes, after subscription
         - After read, with data
       * - Sync
         - Yes
         - Yes
         - No
         - Only on next event
       * - Async
         - No
         - No
         - No
         - After subscription, no data
       * - Stateless
         - Yes
         - No
         - Yes, during subscription
         - Immediately, with data

    See :meth:`tango.DeviceProxy.subscribe_event`.

    .. versionadded:: 10.1.0)doc")
        .value("Sync", Tango::EventSubMode::Sync)
        .value("SyncRead", Tango::EventSubMode::SyncRead)
        .value("Async", Tango::EventSubMode::Async)
        .value("AsyncRead", Tango::EventSubMode::AsyncRead)
        .value("Stateless", Tango::EventSubMode::Stateless)
        .finalize();
    py::object event_sub_mode_class = m.attr("EventSubMode");
    add_names_values_to_native_enum(event_sub_mode_class);

    py::native_enum<Tango::EventReason>(m,
                                        "EventReason",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the reason for an event.

    * ``EventReason.SubSuccess`` - initial subscription was successful.  Note: Event data will not have a value for `EventSubMode.Async` subscription.  Not emitted for `EventSubMode.Sync`.
    * ``EventReason.Update`` -  new event available. Device has pushed a new event, or re-subscription after loosing connection to device (e.g., after restart).
    * ``EventReason.SubFail`` - initial asynchronous subscription failed, or event system down ("Event channel is not responding anymore").
    * ``EventReason.Unknown`` - unexpected - probably a bug in cppTango or PyTango.

    See :class:`tango.EventSubMode`.

    .. versionadded:: 10.1.0)doc")
        .value("Unknown", Tango::EventReason::Unknown)
        .value("SubFail", Tango::EventReason::SubFail)
        .value("SubSuccess", Tango::EventReason::SubSuccess)
        .value("Update", Tango::EventReason::Update)
        .finalize();
    py::object event_reason_class = m.attr("EventReason");
    add_names_values_to_native_enum(event_reason_class);

    py::native_enum<Tango::AttrMemorizedType>(m, "AttrMemorizedType", "enum.IntEnum")
        .value("NOT_KNOWN", Tango::NOT_KNOWN)
        .value("NONE", Tango::NONE)
        .value("MEMORIZED", Tango::MEMORIZED)
        .value("MEMORIZED_WRITE_INIT", Tango::MEMORIZED_WRITE_INIT)
        .finalize();
    py::object attr_memorized_type_class = m.attr("AttrMemorizedType");
    add_names_values_to_native_enum(attr_memorized_type_class);

    // PyTango Enums

    py::native_enum<PyTango::ExtractAs>(m,
                                        "ExtractAs",
                                        "enum.IntEnum",
                                        R"doc(
    Defines what will go into value field of DeviceAttribute,
    or what will Attribute.get_write_value() return.
    Not all the possible values are valid in all the cases)doc")
        .value("Numpy",
               PyTango::ExtractAsNumpy,
               " Value will be stored in [value, w_value]. "
               " If the attribute is an scalar, they will contain a value. "
               "If it's an SPECTRUM or IMAGE it will be exported as a numpy array")
        .value("ByteArray", PyTango::ExtractAsByteArray)
        .value("Bytes", PyTango::ExtractAsBytes)
        .value("Tuple",
               PyTango::ExtractAsTuple,
               "Value will be stored in [value, w_value]. "
               "If the attribute is an scalar, they will contain a value. "
               "If it's an SPECTRUM or IMAGE it will be exported as a tuple "
               "or tuple of tuples")
        .value("List",
               PyTango::ExtractAsList,
               "Value will be stored in [value, w_value]. "
               "If the attribute is an scalar, they will contain a value. "
               "If it's an SPECTRUM or IMAGE it will be exported as a list "
               "or list of lists")
        .value("String",
               PyTango::ExtractAsString,
               "The data will be stored 'as is', the binary data "
               "as it comes from TangoC++ in 'value'")
        .value("Nothing", PyTango::ExtractAsNothing)
        .finalize();
    py::object extract_as_class = m.attr("ExtractAs");
    add_names_values_to_native_enum(extract_as_class);

    py::native_enum<PyTango::GreenMode>(m,
                                        "GreenMode",
                                        "enum.IntEnum",
                                        R"doc(
    An enumeration representing the GreenMode

    .. versionadded:: 8.1.0
    .. versionchanged:: 8.1.9 Added Asyncio)doc")
        .value("Synchronous", PyTango::GreenModeSynchronous)
        .value("Futures", PyTango::GreenModeFutures)
        .value("Gevent", PyTango::GreenModeGevent)
        .value("Asyncio", PyTango::GreenModeAsyncio)
        .finalize();
    py::object green_mode_class = m.attr("GreenMode");
    add_names_values_to_native_enum(green_mode_class);

    py::native_enum<PyTango::ImageFormat>(m, "_ImageFormat", "enum.IntEnum")
        .value("RawImage", PyTango::RawImage)
        .value("JpegImage", PyTango::JpegImage)
        .finalize();
    py::object image_format_class = m.attr("_ImageFormat");
    add_names_values_to_native_enum(image_format_class);
}
