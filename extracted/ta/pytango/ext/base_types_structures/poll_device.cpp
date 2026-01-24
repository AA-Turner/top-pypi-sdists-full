/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_poll_device(py::module &m) {
    py::class_<Tango::PollDevice>(m,
                                  "PollDevice",
                                  R"doc(
    A structure containing PollDevice information with the following members:

        - dev_name : (str) device name
        - ind_list : (sequence<int>) index list

        New in PyTango 7.0.0
)doc")
        .def_readwrite("dev_name", &Tango::PollDevice::dev_name)
        .def_readwrite("ind_list", &Tango::PollDevice::ind_list);
}
