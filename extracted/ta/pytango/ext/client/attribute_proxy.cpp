/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_attribute_proxy(py::module_ &m) {
    py::class_<Tango::AttributeProxy, std::shared_ptr<Tango::AttributeProxy>>(m, "__AttributeProxy")
        .def(py::init<const Tango::AttributeProxy &>(), py::arg("attribute_proxy")) // Copy constructor
        .def(py::init([](const std::string &name) {
                 py::gil_scoped_release no_gil;
                 return new Tango::AttributeProxy(name.c_str());
             }),
             py::arg("name"))
        .def(py::init([](const Tango::DeviceProxy *dev, const std::string &name) {
                 py::gil_scoped_release no_gil;
                 return new Tango::AttributeProxy(dev, name.c_str());
             }),
             py::arg("device_proxy"),
             py::arg("name"))

        .def(py::pickle(
            [](Tango::AttributeProxy &self) { // __getstate__
                Tango::DeviceProxy *dev = self.get_device_proxy();
                std::string ret = dev->get_db_host() + ":" +
                                  dev->get_db_port() + "/" +
                                  dev->dev_name() + "/" +
                                  self.name();
                return py::make_tuple(ret);
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 1) {
                    throw std::runtime_error("Invalid state!");
                }
                std::string trl = py_tuple[0].cast<std::string>();
                return Tango::AttributeProxy(trl.c_str());
            }))

        //
        // general methods
        //

        .def("name",
             &Tango::AttributeProxy::name,
             R"doc(
                name(self) -> str

                    Get attribute name

                :return: the attribute name
                :rtype: str)doc")

        .def("get_device_proxy",
             &Tango::AttributeProxy::get_device_proxy,
             R"doc(
                get_device_proxy(self) -> DeviceProxy

                    Get associated DeviceProxy instance

                :return: the DeviceProxy instance used to communicate with the device to which the attributes belongs
                :rtype: DeviceProxy)doc",
             py::return_value_policy::reference_internal)

        //
        // property methods
        //
        .def("_get_property",
             py::overload_cast<const std::string &, Tango::DbData &>(&Tango::AttributeProxy::get_property),
             py::arg("propname"),
             py::arg("propdata"))

        .def("_get_property",
             py::overload_cast<const std::vector<std::string> &, Tango::DbData &>(&Tango::AttributeProxy::get_property),
             py::arg("propnames"),
             py::arg("propdata"))

        .def("_get_property",
             py::overload_cast<Tango::DbData &>(&Tango::AttributeProxy::get_property),
             py::arg("propdata"))

        .def("_put_property", &Tango::AttributeProxy::put_property, py::arg("propdata"))

        .def("_delete_property",
             py::overload_cast<const Tango::DbData &>(&Tango::AttributeProxy::delete_property),
             py::arg("propdata"));
}
