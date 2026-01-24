/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

namespace PyDeviceInfo {

py::dict get_version_info_dict(Tango::DeviceInfo &dev_info) {
    py::dict info_dict;
    for(const auto &pair : dev_info.version_info) {
        info_dict[pair.first.c_str()] = pair.second;
    }
    return info_dict;
}
} // namespace PyDeviceInfo

void export_device_info(py::module &m) {
    py::class_<Tango::DeviceInfo>(m,
                                  "DeviceInfo",
                                  R"doc(
A structure containing available information for a device with the"
    following members:

        - dev_class : (str) device class
        - server_id : (str) server ID
        - server_host : (str) host name
        - server_version : (str) server version
        - doc_url : (str) document url
        - version_info : (dict<str, str>) version info dict

    .. versionchanged:: 10.0.0
        Added `version_info` field
)doc")
        .def(py::init<>())
        .def_readonly("dev_class", &Tango::DeviceInfo::dev_class)
        .def_readonly("server_id", &Tango::DeviceInfo::server_id)
        .def_readonly("server_host", &Tango::DeviceInfo::server_host)
        .def_readonly("server_version", &Tango::DeviceInfo::server_version)
        .def_readonly("doc_url", &Tango::DeviceInfo::doc_url)
        .def_readonly("dev_type", &Tango::DeviceInfo::dev_type)
        .def_property("version_info", &PyDeviceInfo::get_version_info_dict, nullptr);
}
