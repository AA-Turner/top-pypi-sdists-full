/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"

void export_poll_device(py::module &m);
void export_locker_info(py::module &m);
// TODO void export_locking_thread(py::module &m);
void export_dev_command_info(py::module &m);
void export_attribute_dimension(py::module &m);
void export_command_info(py::module &m);
void export_device_info(py::module &m);
void export_attribute_config_and_info(py::module &m);
void export_attribute_alarm_info(py::module &m);
void export_attribute_configs(py::module_ &m);
void export_time_val(py::module &m);
void export_client_addr(py::module &m);

void export_base_structures(py::module_ &m) {
    export_time_val(m);
    export_poll_device(m);
    export_locker_info(m);
    // TODO export_locking_thread();
    export_dev_command_info(m);
    export_attribute_dimension(m);
    export_command_info(m);
    export_device_info(m);
    export_attribute_alarm_info(m);
    export_attribute_config_and_info(m);
    export_attribute_configs(m);
    export_client_addr(m);
}
