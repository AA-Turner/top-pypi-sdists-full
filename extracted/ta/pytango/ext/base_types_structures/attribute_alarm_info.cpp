/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_attribute_alarm_info(py::module &m) {
    py::class_<Tango::AttributeAlarmInfo>(m,
                                          "AttributeAlarmInfo",
                                          R"doc(
    A structure containing available alarm information for an attribute
    with the following members:

        - min_alarm : (str) low alarm level
        - max_alarm : (str) high alarm level
        - min_warning : (str) low warning level
        - max_warning : (str) high warning level
        - delta_t : (str) time delta
        - delta_val : (str) value delta
        - extensions : (StdStringVector) extensions (currently not used)
)doc")
        .def(py::init<>())

        .def(py::pickle(
            [](const Tango::AttributeAlarmInfo &self) { // __getstate__
                return py::make_tuple(self.min_alarm,
                                      self.max_alarm,
                                      self.min_warning,
                                      self.max_warning,
                                      self.delta_t,
                                      self.delta_val,
                                      pickle_stdstringvector(self.extensions));
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 7) {
                    throw std::runtime_error("Invalid state!");
                }

                Tango::AttributeAlarmInfo info;

                info.min_alarm = py_tuple[0].cast<std::string>();
                info.max_alarm = py_tuple[1].cast<std::string>();
                info.min_warning = py_tuple[2].cast<std::string>();
                info.max_warning = py_tuple[3].cast<std::string>();
                info.delta_t = py_tuple[4].cast<std::string>();
                info.delta_val = py_tuple[5].cast<std::string>();
                info.extensions = unpickled_stdstringvector(py_tuple[6]);
                return info;
            }))

        .def_readwrite("min_alarm", &Tango::AttributeAlarmInfo::min_alarm)
        .def_readwrite("max_alarm", &Tango::AttributeAlarmInfo::max_alarm)
        .def_readwrite("min_warning", &Tango::AttributeAlarmInfo::min_warning)
        .def_readwrite("max_warning", &Tango::AttributeAlarmInfo::max_warning)
        .def_readwrite("delta_t", &Tango::AttributeAlarmInfo::delta_t)
        .def_readwrite("delta_val", &Tango::AttributeAlarmInfo::delta_val)
        .def_readwrite("extensions", &Tango::AttributeAlarmInfo::extensions);
}
