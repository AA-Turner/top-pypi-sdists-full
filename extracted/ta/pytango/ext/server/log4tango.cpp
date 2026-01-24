/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "pyutils.h"

extern const char *param_must_be_seq;

// cppTango Logger API has changed between 9.3 and 9.4 to support source code
// location information (filename and line number). On PyTango side we always
// require this information from the caller and pass it to cppTango if it has
// the new signature.
typedef void (log4tango::Logger::*StringOnlyLogSignature)(const std::string &);
typedef void (log4tango::Logger::*StringAndLocationLogSignature)(const std::string &, int, const std::string &);

typedef void (log4tango::Logger::*StringOnlyWithLevelLogSignature)(log4tango::Level::Value, const std::string &);

typedef void (log4tango::Logger::*StringAndLocationWithLevelLogSignature)(const std::string &,
                                                                          int,
                                                                          log4tango::Level::Value,
                                                                          const std::string &);

template <StringOnlyLogSignature ptr>
static void call_logger(log4tango::Logger &logger, const std::string & /*file*/, int /*line*/, const std::string &msg) {
    (logger.*ptr)(msg);
}

template <StringAndLocationLogSignature ptr>
static void call_logger(log4tango::Logger &logger, const std::string &file, int line, const std::string &msg) {
    (logger.*ptr)(file, line, msg);
}

template <StringOnlyWithLevelLogSignature ptr>
static void call_logger(log4tango::Logger &logger,
                        const std::string & /*file*/,
                        int /*line*/,
                        log4tango::Level::Value level,
                        const std::string &msg) {
    (logger.*ptr)(level, msg);
}

template <StringAndLocationWithLevelLogSignature ptr>
static void call_logger(
    log4tango::Logger &logger,
    const std::string &file,
    int line,
    log4tango::Level::Value level,
    const std::string &msg) {
    (logger.*ptr)(file, line, level, msg);
}

void _convert_target_list(py::object &obj, Tango::DevVarStringArray *par) {
    py::sequence seq = obj.cast<py::sequence>();
    unsigned int len = static_cast<unsigned int>(seq.size());

    (*par).length(len);

    for(unsigned int i = 0; i < len; ++i) {
        py::object item = seq[i];
        std::string item_str = py::str(item);
        (*par)[i] = CORBA::string_dup(item_str.c_str());
    }
}

namespace PyLogging {
void add_logging_target(py::object &obj) {
    if(!py::isinstance<py::sequence>(obj)) {
        raise_(PyExc_TypeError, param_must_be_seq);
    }

    Tango::DevVarStringArray par;
    _convert_target_list(obj, &par);

    Tango::Logging::add_logging_target(&par);
}

void remove_logging_target(py::object &obj) {
    if(!py::isinstance<py::sequence>(obj)) {
        raise_(PyExc_TypeError, param_must_be_seq);
    }

    Tango::DevVarStringArray par;
    _convert_target_list(obj, &par);

    Tango::Logging::remove_logging_target(&par);
}
} // namespace PyLogging

void export_log4tango(py::module &m) {
    py::class_<log4tango::Level>(m, "Level")
        .def_static("get_name", &log4tango::Level::get_name, py::return_value_policy::copy)
        .def_static("get_value", &log4tango::Level::get_value);

    py::native_enum<log4tango::Level::LevelLevel>(m, "LevelLevel", "enum.IntEnum")
        .value("OFF", log4tango::Level::OFF)
        .value("FATAL", log4tango::Level::FATAL)
        .value("ERROR", log4tango::Level::ERROR)
        .value("WARN", log4tango::Level::WARN)
        .value("INFO", log4tango::Level::INFO)
        .value("DEBUG", log4tango::Level::DEBUG)
        .finalize();

    py::class_<log4tango::Logger>(m, "Logger")
        .def(py::init<const std::string &, log4tango::Level::Value>(),
             py::arg("name"),
             py::arg_v("level", log4tango::Level::OFF, "LevelLevel.OFF"))
        .def("get_name", &log4tango::Logger::get_name, py::return_value_policy::copy)
        .def("set_level", &log4tango::Logger::set_level)
        .def("get_level", &log4tango::Logger::get_level)
        .def("is_level_enabled", &log4tango::Logger::is_level_enabled)
        .def("__log", &call_logger<&log4tango::Logger::log>)
        .def("__log_unconditionally", &call_logger<&log4tango::Logger::log_unconditionally>)
        .def("__debug", &call_logger<&log4tango::Logger::debug>)
        .def("__info", &call_logger<&log4tango::Logger::info>)
        .def("__warn", &call_logger<&log4tango::Logger::warn>)
        .def("__error", &call_logger<&log4tango::Logger::error>)
        .def("__fatal", &call_logger<&log4tango::Logger::fatal>)
        .def("is_debug_enabled", &log4tango::Logger::is_debug_enabled)
        .def("is_info_enabled", &log4tango::Logger::is_info_enabled)
        .def("is_warn_enabled", &log4tango::Logger::is_warn_enabled)
        .def("is_error_enabled", &log4tango::Logger::is_error_enabled)
        .def("is_fatal_enabled", &log4tango::Logger::is_fatal_enabled);

    py::class_<Tango::Logging, std::unique_ptr<Tango::Logging, py::nodelete>>(m, "Logging")
        .def_static("get_core_logger", &Tango::Logging::get_core_logger, py::return_value_policy::reference)
        .def_static("add_logging_target", &PyLogging::add_logging_target)
        .def_static("remove_logging_target", &PyLogging::remove_logging_target)
        .def_static("start_logging", &Tango::Logging::start_logging)
        .def_static("stop_logging", &Tango::Logging::stop_logging);
}
