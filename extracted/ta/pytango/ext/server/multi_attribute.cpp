/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_multi_attribute(py::module_ &m) {
    py::class_<Tango::MultiAttribute>(m,
                                      "MultiAttribute",
                                      R"doc()doc")
        // No constructor provided to prevent instantiation from Python
        .def("get_attr_by_name",
             &Tango::MultiAttribute::get_attr_by_name,
             py::return_value_policy::reference,
             R"doc(
                get_attr_by_name(self, attr_name) -> Attribute

                    Get :class:`~tango.Attribute` object from its name.

                    This method returns an :class:`~tango.Attribute` object with a
                    name passed as parameter. The equality on attribute name is case
                    independent.

                :param attr_name: attribute name
                :type attr_name: str

                :returns: the attribute object
                :rtype: Attribute

                :raises DevFailed: If the attribute is not defined.)doc",
             py::arg("attr_name"))
        .def("get_attr_by_ind",
             &Tango::MultiAttribute::get_attr_by_ind,
             py::return_value_policy::reference,
             R"doc(
                get_attr_by_ind(self, ind) -> Attribute

                    Get :class:`~tango.Attribute` object from its index.

                    This method returns an :class:`~tango.Attribute` object from the
                    index in the main attribute vector.

                :param ind: the attribute index
                :type ind: int

                :returns: the attribute object
                :rtype: Attribute)doc",
             py::arg("ind"))
        .def("get_w_attr_by_name",
             &Tango::MultiAttribute::get_w_attr_by_name,
             py::return_value_policy::reference,
             R"doc(
                get_w_attr_by_name(self, attr_name) -> WAttribute

                    Get a writable attribute object from its name.

                    This method returns an :class:`~tango.WAttribute` object with a
                    name passed as parameter. The equality on attribute name is case
                    independent.

                :param attr_name: attribute name
                :type attr_name: str

                :returns: the attribute object
                :rtype: WAttribute

                :raises DevFailed: If the attribute is not defined.)doc",
             py::arg("attr_name"))
        .def("get_w_attr_by_ind",
             &Tango::MultiAttribute::get_w_attr_by_ind,
             py::return_value_policy::reference,
             R"doc(
                get_w_attr_by_ind(self, ind) -> WAttribute

                    Get a writable attribute object from its index.

                    This method returns an :class:`~tango.WAttribute` object from the
                    index in the main attribute vector.

                :param ind: the attribute index
                :type ind: int

                :returns: the attribute object
                :rtype: WAttribute)doc",
             py::arg("ind"))
        .def("get_attr_ind_by_name",
             &Tango::MultiAttribute::get_attr_ind_by_name,
             R"doc(
                get_attr_ind_by_name(self, attr_name) -> int

                    Get Attribute index into the main attribute vector from its name.

                    This method returns the index in the Attribute vector (stored in the
                    :class:`~tango.MultiAttribute` object) of an attribute with a
                    given name. The name equality is case independent.

                :param attr_name: attribute name
                :type attr_name: str

                :returns: the attribute index
                :rtype: int

                :raises DevFailed: If the attribute is not found in the vector.

                New in PyTango 7.0.0)doc",
             py::arg("attr_name"))
        .def("get_alarm_list",
             &Tango::MultiAttribute::get_alarm_list,
             py::return_value_policy::reference_internal,
             R"doc(
                get_alarm_list(self) -> list[int]

                    Get list of attribute with an alarm level defined

                :returns: A vector of int data. Each object is the index in the main attribute vector of attribute with alarm level defined
                :rtype: list[int]
             )doc")
        .def("get_attr_nb",
             &Tango::MultiAttribute::get_attr_nb,
             R"doc(
                get_attr_nb(self) -> int

                    Get the number of attributes.

                :returns: the number of attributes
                :rtype: int

                New in PyTango 7.0.0)doc")
        .def("check_alarm",
             py::overload_cast<>(&Tango::MultiAttribute::check_alarm),
             R"doc(
                check_alarm(self) -> bool

                    Checks an alarm on all attribute(s) with an alarm defined.

                :returns: True if at least one attribute is in alarm condition
                :rtype: bool

                :raises DevFailed: If at least one attribute does not have any alarm level defined

                New in PyTango 7.0.0)doc")
        .def("check_alarm",
             py::overload_cast<const long>(&Tango::MultiAttribute::check_alarm),
             R"doc(
                check_alarm(self, ind) -> bool

                    Checks an alarm for one attribute from its index in the main attributes vector.

                :param ind: the attribute index
                :type ind: int

                :returns: True if attribute is in alarm condition
                :rtype: bool

                :raises DevFailed: If at least one attribute does not have any alarm level defined

                New in PyTango 7.0.0)doc",
             py::arg("ind"))
        .def("check_alarm",
             py::overload_cast<const char *>(&Tango::MultiAttribute::check_alarm),
             R"doc(
                check_alarm(self, attr_name) -> bool

                    Checks an alarm for one attribute with a given name.
                    - The 3rd version of the method checks alarm for one attribute from its index in the main attributes vector.

                :param attr_name: attribute name
                :type attr_name: str

                :returns: True if attribute is in alarm condition
                :rtype: bool

                :raises DevFailed: If at least one attribute does not have any alarm level defined

                New in PyTango 7.0.0)doc",
             py::arg("attr_name"))
        .def("read_alarm",
             &Tango::MultiAttribute::read_alarm,
             R"doc(
                read_alarm(self, status)

                    Add alarm message to device status.

                    This method add alarm message to the string passed as parameter.
                    A message is added for each attribute which is in alarm condition

                :param status: a string (should be the device status)
                :type status: str

                New in PyTango 7.0.0)doc",
             py::arg("status"))
        .def("get_attribute_list",
             &Tango::MultiAttribute::get_attribute_list,
             py::return_value_policy::reference,
             R"doc(
                get_attribute_list(self) -> tuple[Attribute]

                    Get the tuple of :class:`~tango.Attribute` objects.

                :returns: attribute objects tuple.
                :rtype: tuple[Attribute]

                .. versionchanged:: 10.1.0
                   The return type was changed from ``AttributeList`` (now removed) to ``tuple[Attribute]``.

                New in PyTango 7.2.1)doc");
}
