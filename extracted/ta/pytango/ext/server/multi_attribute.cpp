/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_multi_attribute(py::module_ &m) {
    py::class_<Tango::MultiAttribute>(m, "MultiAttribute", R"doc()doc")
        // No constructor provided to prevent instantiation from Python
        .def("get_attr_by_name",
             &Tango::MultiAttribute::get_attr_by_name,
             py::return_value_policy::reference,
             R"doc(
                Get :class:`~tango.Attribute` object from its name.

                This method returns an :class:`~tango.Attribute` object with a
                name passed as parameter. The equality on attribute name is case
                independent.

                :param attr_name: attribute name
                :type attr_name: :py:obj:`str`

                :returns: the attribute object
                :rtype: :obj:`~tango.Attribute`

                :throws: :obj:`~tango.DevFailed`: If the attribute is not defined
             )doc",
             py::arg("attr_name"))
        .def("get_attr_by_ind",
             &Tango::MultiAttribute::get_attr_by_ind,
             py::return_value_policy::reference,
             R"doc(
                Get :class:`~tango.Attribute` object from its index.

                This method returns an :class:`~tango.Attribute` object from the
                index in the main attribute vector.

                :param ind: the attribute index
                :type ind: int
             )doc",
             py::arg("ind"))
        .def("get_w_attr_by_name",
             &Tango::MultiAttribute::get_w_attr_by_name,
             py::return_value_policy::reference,
             R"doc(
                Get a writable attribute object from its name.

                This method returns an :class:`~tango.WAttribute` object with a
                name passed as parameter. The equality on attribute name is case
                independent.

                :param attr_name: attribute name
                :type attr_name: :py:obj:`str`

                :throws: :obj:`~tango.DevFailed`: If the attribute is not defined
             )doc",
             py::arg("attr_name"))
        .def("get_w_attr_by_ind",
             &Tango::MultiAttribute::get_w_attr_by_ind,
             py::return_value_policy::reference,
             R"doc(
                Get a writable attribute object from its index.

                This method returns an :class:`~tango.WAttribute` object from the
                index in the main attribute vector.

                :param ind: the attribute index
                :type ind: int
             )doc",
             py::arg("ind"))
        .def("get_attr_ind_by_name",
             &Tango::MultiAttribute::get_attr_ind_by_name,
             R"doc(
                Get Attribute index into the main attribute vector from its name.

                This method returns the index in the Attribute vector (stored in the
                :class:`~tango.MultiAttribute` object) of an attribute with a
                given name. The name equality is case independent.

                :param attr_name: attribute name
                :type attr_name: :py:obj:`str`

                :throws: :obj:`~tango.DevFailed`: If the attribute is not found in the vector.

                .. versionadded:: 7.0.0
             )doc",
             py::arg("attr_name"))
        .def("get_alarm_list",
             &Tango::MultiAttribute::get_alarm_list,
             py::return_value_policy::reference_internal,
             R"doc(
                A vector of int data. Each object is the index in the main attribute vector of attribute with alarm level defined
             )doc")
        .def("get_attr_nb",
             &Tango::MultiAttribute::get_attr_nb,
             R"doc(
                Get the number of attributes.

                .. versionadded:: 7.0.0
             )doc")
        .def("check_alarm",
             py::overload_cast<>(&Tango::MultiAttribute::check_alarm),
             R"doc(
                Checks an alarm on all attribute(s) with an alarm defined. Returns True if at least one attribute is in alarm condition.

                :throws: :obj:`~tango.DevFailed`: If at least one attribute does not have any alarm level defined

                .. versionadded:: 7.0.0
             )doc")
        .def("check_alarm",
             py::overload_cast<const long>(&Tango::MultiAttribute::check_alarm),
             R"doc(
                Checks an alarm for one attribute from its index in the main attributes vector.

                :param ind: the attribute index
                :type ind: int

                :throws: :obj:`~tango.DevFailed`: If at least one attribute does not have any alarm level defined

                .. versionadded:: 7.0.0
             )doc",
             py::arg("ind"))
        .def("check_alarm",
             py::overload_cast<const char *>(&Tango::MultiAttribute::check_alarm),
             R"doc(
                Checks an alarm for one attribute with a given name.

                :param attr_name: attribute name
                :type attr_name: :py:obj:`str`

                :throws: :obj:`~tango.DevFailed`: If at least one attribute does not have any alarm level defined

                .. versionadded:: 7.0.0
             )doc",
             py::arg("attr_name"))
        .def("read_alarm",
             &Tango::MultiAttribute::read_alarm,
             R"doc(
                Add alarm message to device status.

                This method add alarm message to the string passed as parameter.
                A message is added for each attribute which is in alarm condition

                :param status: a string (should be the device status)
                :type status: :py:obj:`str`

                .. versionadded:: 7.0.0
             )doc",
             py::arg("status"))
        .def("get_attribute_list",
             &Tango::MultiAttribute::get_attribute_list,
             py::return_value_policy::reference,
             R"doc(
                Get the tuple of :class:`~tango.Attribute` objects.

                .. versionchanged:: 10.1.0
                    The return type was changed from ``AttributeList`` (now removed) to ``tuple[Attribute]``.

                .. versionadded:: 7.2.1
             )doc");
}
