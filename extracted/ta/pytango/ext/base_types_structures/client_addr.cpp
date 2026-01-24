/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_client_addr(py::module_ &m) {
    py::class_<Tango::client_addr, std::unique_ptr<Tango::client_addr, py::nodelete>>(m, "ClientAddr")
        .def(py::init<>())                              // client_addr()
        .def(py::init<const char *>(), py::arg("addr")) // client_addr("127.0.0.1")

        // unfortunate, we cannot use cppTango`s = and != for pybind11`s py::self == py::self and != due to
        // they can only be generated when the C++ comparison operator is declared const
        // (which is not the case of cppTango)
        .def(
            "__eq__",
            [](Tango::client_addr &self, const Tango::client_addr &other) {
                return self == other;
            },
            py::is_operator())
        .def(
            "__ne__",
            [](Tango::client_addr &self, const Tango::client_addr &other) {
                return self != other;
            },
            py::is_operator())

        .def_readonly("client_ident", &Tango::client_addr::client_ident)
        .def_readonly("client_lang", &Tango::client_addr::client_lang)
        .def_readonly("client_pid", &Tango::client_addr::client_pid)
        .def_readonly("java_main_class", &Tango::client_addr::java_main_class)

        .def_property_readonly("client_ip",
                               /* getter */ [](const Tango::client_addr &self) {
                                   return std::string(self.client_ip); // copy out as std::string
                               })

        .def_property_readonly("java_ident",
                               /* getter */ [](const Tango::client_addr &self) {
                                   return py::make_tuple(self.java_ident[0], self.java_ident[1]);
                               })

        .def(
            "get_client_hostname", [](const Tango::client_addr &self) {
                std::string host;
                int rc = self.client_ip_2_client_name(host);
                if(rc == -1) {
                    throw py::value_error(std::string("Cannot parse client_ip: ") + self.client_ip);
                }
                return host;
            },
            R"doc(
        get_client_hostname(self) -> str

            Returns client host name, extracted from client ip.

            :returns: client host name
            :rtype: str

            :throws: ValueError
            )doc")

        /* ------ Friend ostream ⇢ __str__ ------ */
        .def("__str__", [](const Tango::client_addr &self) {
            std::ostringstream oss;
            oss << self;
            return oss.str();
        });
}
