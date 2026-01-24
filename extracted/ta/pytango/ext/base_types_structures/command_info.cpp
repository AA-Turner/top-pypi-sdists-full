/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_command_info(py::module &m) {
    py::class_<Tango::CommandInfo, Tango::DevCommandInfo>(m,
                                                          "CommandInfo",
                                                          R"doc(
    A device command info (inheriting from :class:`DevCommandInfo`) with the following members:

        - disp_level : (DispLevel) command display level

        Inherited members are (from :class:`DevCommandInfo`):

            - cmd_name : (str) command name
            - cmd_tag : (str) command as binary value (for TACO)
            - in_type : (CmdArgType) input type
            - out_type : (CmdArgType) output type
            - in_type_desc : (str) description of input type
            - out_type_desc : (str) description of output type
)doc")
        .def(py::init<>())
        .def_readonly("disp_level", &Tango::CommandInfo::disp_level);
}
