/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_dev_command_info(py::module &m) {
    typedef Tango::CmdArgType Tango::_DevCommandInfo::*MemCmdArgType;

    py::class_<Tango::DevCommandInfo>(m,
                                      "DevCommandInfo",
                                      R"doc(
    A device command info with the following members:

        - cmd_name : (str) command name
        - cmd_tag : command as binary value (for TACO)
        - in_type : (CmdArgType) input type
        - out_type : (CmdArgType) output type
        - in_type_desc : (str) description of input type
        - out_type_desc : (str) description of output type

    New in PyTango 7.0.0
)doc")
        .def(py::init<>())
        .def_readonly("cmd_name", &Tango::DevCommandInfo::cmd_name)
        .def_readonly("cmd_tag", &Tango::DevCommandInfo::cmd_tag)
        .def_readonly("in_type", reinterpret_cast<MemCmdArgType>(&Tango::DevCommandInfo::in_type))
        .def_readonly("out_type", reinterpret_cast<MemCmdArgType>(&Tango::DevCommandInfo::out_type))
        .def_readonly("in_type_desc", &Tango::DevCommandInfo::in_type_desc)
        .def_readonly("out_type_desc", &Tango::DevCommandInfo::out_type_desc);
}
