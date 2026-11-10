/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "pyutils.h"
#include "convertors/type_casters.h"

void export_attribute_proxy(py::module_ &m) {
    py::class_<Tango::AttributeProxy, std::shared_ptr<Tango::AttributeProxy>>(m, "__AttributeProxy")
        .def(py::init([](const Tango::AttributeProxy &attribute_proxy) {
                 py::gil_scoped_release no_gil{};
                 return std::shared_ptr<Tango::AttributeProxy>(
                     new Tango::AttributeProxy(attribute_proxy), DeleterWithoutGIL());
             }),
             py::arg("attribute_proxy"))
        .def(py::init([](const std::string &name) {
                 py::gil_scoped_release no_gil{};
                 return std::shared_ptr<Tango::AttributeProxy>(
                     new Tango::AttributeProxy(name.c_str()), DeleterWithoutGIL());
             }),
             py::arg("name"))
        .def(py::init([](const Tango::DeviceProxy *device_proxy, const std::string &name) {
                 py::gil_scoped_release no_gil{};
                 return std::shared_ptr<Tango::AttributeProxy>(
                     new Tango::AttributeProxy(device_proxy, name.c_str()), DeleterWithoutGIL());
             }),
             py::arg("device_proxy"),
             py::arg("name"))

        .def(py::pickle(
            [](Tango::AttributeProxy &self) { // __getstate__
                Tango::DeviceProxy *dev = self.get_device_proxy();
                // clang-format off
                std::string ret = dev->get_db_host() + ":" +
                                  dev->get_db_port() + "/" +
                                  dev->dev_name() + "/" +
                                  self.name();
                // clang-format on
                return py::make_tuple(ret);
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 1) {
                    throw std::runtime_error("Invalid state!");
                }
                std::string trl = py_tuple[0].cast<std::string>();
                py::gil_scoped_release no_gil{};
                return std::shared_ptr<Tango::AttributeProxy>(
                    new Tango::AttributeProxy(trl.c_str()), DeleterWithoutGIL());
            }))

        //
        // general methods
        //

        .def("name",
             &Tango::AttributeProxy::name,
             R"doc(
                Get attribute name
             )doc")

        .def("get_device_proxy",
             &Tango::AttributeProxy::get_device_proxy,
             R"doc(
                Get DeviceProxy instance used to communicate with the device to which the attributes belongs
             )doc",
             py::return_value_policy::reference_internal)

        //
        // property methods
        //
        .def("_get_property",
             py::overload_cast<const std::string &, Tango::DbData &>(&Tango::AttributeProxy::get_property),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("propname"),
             py::arg("propdata"))

        .def("_get_property",
             py::overload_cast<const std::vector<std::string> &, Tango::DbData &>(&Tango::AttributeProxy::get_property),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("propnames"),
             py::arg("propdata"))

        .def("_get_property",
             py::overload_cast<Tango::DbData &>(&Tango::AttributeProxy::get_property),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("propdata"))

        .def("_put_property",
             &Tango::AttributeProxy::put_property,
             py::call_guard<py::gil_scoped_release>(),
             py::arg("propdata"))

        .def("_delete_property",
             py::overload_cast<const Tango::DbData &>(&Tango::AttributeProxy::delete_property),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("propdata"));
}
