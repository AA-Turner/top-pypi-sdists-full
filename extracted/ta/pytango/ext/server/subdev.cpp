/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_sub_dev_diag(py::module_ &m) {
    py::class_<Tango::SubDevDiag>(m, "SubDevDiag")
        .def("set_associated_device",
             &Tango::SubDevDiag::set_associated_device,
             R"doc(Set the device name that should be associated to a thread in the device server)doc",
             py::arg("dev_name"))
        .def("get_associated_device",
             &Tango::SubDevDiag::get_associated_device,
             R"doc(Get the device name that is associated with the current thread of the device server)doc")
        .def("register_sub_device",
             &Tango::SubDevDiag::register_sub_device,
             R"doc(Register a sub device for an associated device in the list of sub devices of the device server)doc",
             py::arg("dev_name"),
             py::arg("sub_dev_name"))
        .def("remove_sub_devices",
             py::overload_cast<>(&Tango::SubDevDiag::remove_sub_devices),
             R"doc(Remove all sub devices)doc")
        .def("remove_sub_devices",
             py::overload_cast<std::string>(&Tango::SubDevDiag::remove_sub_devices),
             R"doc(Remove all sub devices for a device of the server)doc",
             py::arg("dev_name"))
        .def("get_sub_devices",
             &Tango::SubDevDiag::get_sub_devices,
             R"doc(
    Read the list of sub devices for the device server
    The returned strings are formated as:

    'device_name sub_device_name'

     or

     sub_device_name

     when no associated device could be identified)doc")
        .def("store_sub_devices",
             &Tango::SubDevDiag::store_sub_devices,
             R"doc(
    Store the list of sub devices for the devices of the server.
    The sub device names are stored as a string array
    under the device property "sub_devices".
    Sub device names without an associated device,
    will be stored under the name of the administration device.

    Database access will only happen when the list of
    sub devices was modified and when the list is different
    from the list read into the db_cache during the server
    startup)doc")
        .def("get_sub_devices_from_cache",
             &Tango::SubDevDiag::get_sub_devices_from_cache,
             R"doc(
    Read the list of sub devices from the database cache.
    The cache is filled at server sart-up)doc");
}
