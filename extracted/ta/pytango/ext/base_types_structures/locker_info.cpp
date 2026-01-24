/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

struct PyLockerInfo {
    static py::object get_locker_id(Tango::LockerInfo &li) {
        if(li.ll == Tango::CPP) {
            return py::cast(li.li.LockerPid);
        } else {
            return py::make_tuple(li.li.UUID);
        }
    }
};

void export_locker_info(py::module &m) {
    py::class_<Tango::LockerInfo>(m,
                                  "LockerInfo",
                                  R"doc(
    A structure with information about the locker with the following members:

        - ll : (tango.LockerLanguage) the locker language
        - li : (pid_t / UUID) the locker id
        - locker_host : (str) the host
        - locker_class : (str) the class

        pid_t should be an int, UUID should be a tuple of four numbers.

        New in PyTango 7.0.0
)doc")
        .def(py::init<>())
        .def_readonly("ll", &Tango::LockerInfo::ll)
        .def_property("li", &PyLockerInfo::get_locker_id, nullptr)
        .def_readonly("locker_host", &Tango::LockerInfo::locker_host)
        .def_readonly("locker_class", &Tango::LockerInfo::locker_class);
}
