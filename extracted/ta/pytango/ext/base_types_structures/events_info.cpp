/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_event_infos(py::module &m) {
    py::class_<Tango::ChangeEventInfo>(m,
                                       "ChangeEventInfo",
                                       R"doc(
    A structure containing available change event information for an attribute
    with the following members:

        - rel_change : (str) relative change that will generate an event
        - abs_change : (str) absolute change that will generate an event
        - extensions : (StdStringVector) extensions (currently not used)
)doc")
        .def(py::init<>())

        .def(py::pickle(
            [](const Tango::ChangeEventInfo &self) { // __getstate__
                return py::make_tuple(self.rel_change,
                                      self.abs_change,
                                      pickle_stdstringvector(self.extensions));
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 3) {
                    throw std::runtime_error("Invalid state!");
                }

                Tango::ChangeEventInfo info;

                info.rel_change = py_tuple[0].cast<std::string>();
                info.abs_change = py_tuple[1].cast<std::string>();
                info.extensions = unpickled_stdstringvector(py_tuple[2]);
                return info;
            }))

        .def_readwrite("rel_change", &Tango::ChangeEventInfo::rel_change)
        .def_readwrite("abs_change", &Tango::ChangeEventInfo::abs_change)
        .def_readwrite("extensions", &Tango::ChangeEventInfo::extensions);

    py::class_<Tango::PeriodicEventInfo>(m,
                                         "PeriodicEventInfo",
                                         R"doc(
    A structure containing available periodic event information for an attribute
    with the following members:

        - period : (str) event period
        - extensions : (StdStringVector) extensions (currently not used)
)doc")
        .def(py::init<>())

        .def(py::pickle(
            [](const Tango::PeriodicEventInfo &self) { // __getstate__
                return py::make_tuple(self.period,
                                      pickle_stdstringvector(self.extensions));
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 2) {
                    throw std::runtime_error("Invalid state!");
                }

                Tango::PeriodicEventInfo info;

                info.period = py_tuple[0].cast<std::string>();
                info.extensions = unpickled_stdstringvector(py_tuple[1]);

                return info;
            }))

        .def_readwrite("period", &Tango::PeriodicEventInfo::period)
        .def_readwrite("extensions", &Tango::PeriodicEventInfo::extensions);

    py::class_<Tango::ArchiveEventInfo>(m,
                                        "ArchiveEventInfo",
                                        R"doc(
    A structure containing available archiving event information for an attribute
    with the following members:

        - archive_rel_change : (str) relative change that will generate an event
        - archive_abs_change : (str) absolute change that will generate an event
        - archive_period : (str) archive period
        - extensions : (sequence<str>) extensions (currently not used)
)doc")
        .def(py::init<>())

        .def(py::pickle(
            [](const Tango::ArchiveEventInfo &self) { // __getstate__
                return py::make_tuple(self.archive_rel_change,
                                      self.archive_abs_change,
                                      self.archive_period,
                                      pickle_stdstringvector(self.extensions));
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 4) {
                    throw std::runtime_error("Invalid state!");
                }

                Tango::ArchiveEventInfo info;

                info.archive_rel_change = py_tuple[0].cast<std::string>();
                info.archive_abs_change = py_tuple[1].cast<std::string>();
                info.archive_period = py_tuple[2].cast<std::string>();
                info.extensions = unpickled_stdstringvector(py_tuple[3]);

                return info;
            }))

        .def_readwrite("archive_rel_change", &Tango::ArchiveEventInfo::archive_rel_change)
        .def_readwrite("archive_abs_change", &Tango::ArchiveEventInfo::archive_abs_change)
        .def_readwrite("archive_period", &Tango::ArchiveEventInfo::archive_period)
        .def_readwrite("extensions", &Tango::ArchiveEventInfo::extensions);

    py::class_<Tango::AttributeEventInfo>(m,
                                          "AttributeEventInfo",
                                          R"doc(
    A structure containing available event information for an attribute
    with the following members:

        - ch_event : (ChangeEventInfo) change event information
        - per_event : (PeriodicEventInfo) periodic event information
        - arch_event :  (ArchiveEventInfo) archiving event information
)doc")
        .def(py::init<>())

        .def(py::pickle(
            [](const Tango::AttributeEventInfo &self) { // __getstate__
                return py::make_tuple(self.ch_event, self.per_event, self.arch_event);
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 3) {
                    throw std::runtime_error("Invalid state!");
                }

                Tango::AttributeEventInfo info;

                info.ch_event = py_tuple[0].cast<Tango::ChangeEventInfo>();
                info.per_event = py_tuple[1].cast<Tango::PeriodicEventInfo>();
                info.arch_event = py_tuple[2].cast<Tango::ArchiveEventInfo>();

                return info;
            }))

        .def_readwrite("ch_event", &Tango::AttributeEventInfo::ch_event)
        .def_readwrite("per_event", &Tango::AttributeEventInfo::per_event)
        .def_readwrite("arch_event", &Tango::AttributeEventInfo::arch_event);
}
