/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

// we have to do this import and init numpy before we include common_header

#define PY_ARRAY_UNIQUE_SYMBOL pytango_ARRAY_API
#include <numpy/arrayobject.h>

void *init_numpy() {
    import_array();
    return nullptr;
}

#include "common_header.h"

void export_version(py::module_ &m);
void export_enums(py::module_ &m);
void export_constants(py::module_ &m);
void export_base_types(py::module_ &m);
void export_base_structures(py::module_ &m);
void export_exceptions(py::module_ &m);
void export_vector_wrappers(py::module_ &m);
void export_event_infos(py::module &m);
void export_event_data(py::module_ &m);
void export_device_data(py::module &m);
void export_device_attribute(py::module &m);
void export_device_data_history(py::module &m);
void export_device_attribute_history(py::module &m);
void export_attr_conf_event_data(py::module_ &m);
void export_data_ready_event_data(py::module_ &m);
void export_api_util(py::module_ &m);
void export_connection(py::module_ &m);
void export_device_proxy(py::module_ &m);
void export_devintr_change_event_data(py::module_ &m);
void export_attribute_proxy(py::module_ &m);
void export_db(py::module_ &m);
void export_database(py::module &m);
void export_callback(py::module_ &m);
void export_util(py::module_ &m);
void export_attr(py::module_ &m);
void export_fwdattr(py::module_ &m);
void export_attribute(py::module_ &m);
void export_encoded_attribute(py::module_ &m);
void export_wattribute(py::module_ &m);
void export_multi_attribute(py::module_ &m);
void export_multi_class_attribute(py::module_ &m);
void export_user_default_attr_prop(py::module_ &m);
void export_user_default_fwdattr_prop(py::module_ &m);
void export_sub_dev_diag(py::module_ &m);
void export_dserver(py::module_ &m);
void export_device_class(py::module_ &m);
void export_device_impl(py::module_ &m);
void export_group(py::module_ &m);
void export_log4tango(py::module_ &m);
void export_auto_tango_monitor(py::module_ &m);
void export_ensure_omni_thread(py::module_ &m);
void export_telemetry_helpers(py::module_ &m);
void export_coverage_helper(py::module_ &m);
void export_complicated_types(py::module_ &m);

PYBIND11_MODULE(_tango, m) {
    init_numpy();
    export_version(m);
    export_enums(m);
    export_constants(m);
    export_base_types(m);
    export_base_structures(m);
    export_exceptions(m);
    export_device_data(m);
    export_device_attribute(m);
    export_device_data_history(m);
    export_device_attribute_history(m);
    export_connection(m);
    export_db(m);
    export_user_default_attr_prop(m);
    export_user_default_fwdattr_prop(m);
    export_fwdattr(m);
    export_attribute(m);
    export_wattribute(m);
    export_attr(m);
    export_vector_wrappers(m);
    //    @warning export_vector_wrappers must be made after export_attr
    export_event_data(m);
    export_complicated_types(m);
    export_multi_attribute(m);
    export_log4tango(m);
    export_device_class(m);
    export_device_impl(m);
    //    @warning export_dserver must be made after export_device_impl
    export_dserver(m);
    export_database(m);
    export_device_proxy(m);
    export_event_infos(m);
    export_attr_conf_event_data(m);
    export_data_ready_event_data(m);
    export_devintr_change_event_data(m);
    export_callback(m);
    export_attribute_proxy(m);
    export_encoded_attribute(m);
    export_multi_class_attribute(m);
    export_sub_dev_diag(m);
    export_group(m);
    export_util(m);
    export_api_util(m);
    export_auto_tango_monitor(m);
    export_ensure_omni_thread(m);
    export_telemetry_helpers(m);
    export_coverage_helper(m);
}
