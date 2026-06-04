/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_multi_class_attribute(py::module_ &m) {
    py::class_<Tango::MultiClassAttribute>(m,
                                           "MultiClassAttribute",
                                           R"doc(
            There is one instance of this class for each device class.

            This class is mainly an aggregate of :class:`~tango.Attr` objects.
            It eases management of multiple attributes

            .. versionadded:: 7.2.1
        )doc")
        .def("get_attr",
             py::overload_cast<const std::string &>(&Tango::MultiClassAttribute::get_attr),
             py::return_value_policy::reference,
             R"doc(
                Get the :class:`~tango.Attr` object for the attribute with
                name passed as parameter.

                :param attr_name: attribute name
                :type attr_name: :py:obj:`str`

                :returns: the attribute object
                :rtype: :obj:`~tango.Attr`

                :throws: :obj:`~tango.DevFailed`: If the attribute is not defined.

                .. versionadded:: 7.2.1
             )doc",
             py::arg("attr_name"))
        .def("remove_attr",
             &Tango::MultiClassAttribute::remove_attr,
             R"doc(
                Remove the :class:`~tango.Attr` object for the attribute with
                name passed as parameter.

                Does nothing if the attribute does not exist.

                :param attr_name: attribute name
                :type attr_name: :py:obj:`str`
                :param cl_name: the attribute class name
                :type cl_name: :py:obj:`str`

                .. versionadded:: 7.2.1
             )doc",
             py::arg("attr_name"),
             py::arg("cl_name"))
        .def("get_attr_list",
             &Tango::MultiClassAttribute::get_attr_list,
             py::return_value_policy::reference,
             R"doc(
                Get the tuple of :class:`~tango.Attr` for this device class.

                :returns: attr objects tuple
                :rtype: tuple[:obj:`~tango.Attr`]

                .. versionchanged:: 10.1.0
                   The return type was changed from ``AttrList`` (now removed) to ``tuple[Attr]``.

                .. versionadded:: 7.2.1
             )doc");
}
