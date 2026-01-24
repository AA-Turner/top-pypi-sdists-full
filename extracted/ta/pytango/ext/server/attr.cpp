/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "function_call_macros.h"
#include "convertors/type_casters.h"

#include "server/attr.h"
#include "base_types_structures/exception.h"
#include "pyutils.h"

void PyAttr::read(Tango::DeviceImpl *dev, Tango::Attribute &att) {
    GET_DEVICE
    if(!_is_method(py_dev, read_name)) {
        TangoSys_OMemStream o;
        o << read_name << " method not found for " << att.get_name();
        Tango::Except::throw_exception("PyTango_ReadAttributeMethodNotFound", o.str(), "PyTango::Attr::read");
    }
    try {
        py_dev.attr(read_name.c_str())(std::ref(att));
    }
    CATCH_PY_EXCEPTION
}

void PyAttr::write(Tango::DeviceImpl *dev, Tango::WAttribute &att) {
    GET_DEVICE
    if(!_is_method(py_dev, write_name)) {
        TangoSys_OMemStream o;
        o << write_name << " method not found for " << att.get_name();
        Tango::Except::throw_exception("PyTango_WriteAttributeMethodNotFound", o.str(), "PyTango::Attr::write");
    }
    try {
        py_dev.attr(write_name.c_str())(std::ref(att));
    }
    CATCH_PY_EXCEPTION
}

bool PyAttr::is_allowed(Tango::DeviceImpl *dev, Tango::AttReqType req_type) {
    GET_DEVICE
    if(_is_method(py_dev, py_allowed_name)) {
        try {
            return py_dev.attr(py_allowed_name.c_str())(req_type).cast<bool>();
        }
        CATCH_PY_EXCEPTION
    }
    // keep compiler quiet
    return true;
}

bool PyAttr::_is_method(py::object py_dev, const std::string &name) {
    return is_method_defined(py_dev, name);
}

void PyAttr::set_user_prop(std::vector<Tango::AttrProperty> &user_prop,
                           Tango::UserDefaultAttrProp &def_prop) {
    //
    // Is there any user defined prop. defined ?
    //

    size_t nb_prop = user_prop.size();
    if(nb_prop == 0) {
        return;
    }

    for(size_t loop = 0; loop < nb_prop; loop++) {
        Tango::AttrProperty prop = user_prop[loop];
        std::string &prop_name = prop.get_name();
        const char *prop_value = prop.get_value().c_str();

        if(prop_name == "label") {
            def_prop.set_label(prop_value);
        } else if(prop_name == "description") {
            def_prop.set_description(prop_value);
        } else if(prop_name == "unit") {
            def_prop.set_unit(prop_value);
        } else if(prop_name == "standard_unit") {
            def_prop.set_standard_unit(prop_value);
        } else if(prop_name == "display_unit") {
            def_prop.set_display_unit(prop_value);
        } else if(prop_name == "format") {
            def_prop.set_format(prop_value);
        } else if(prop_name == "min_value") {
            def_prop.set_min_value(prop_value);
        } else if(prop_name == "max_value") {
            def_prop.set_max_value(prop_value);
        } else if(prop_name == "min_alarm") {
            def_prop.set_min_alarm(prop_value);
        } else if(prop_name == "max_alarm") {
            def_prop.set_max_alarm(prop_value);
        } else if(prop_name == "min_warning") {
            def_prop.set_min_warning(prop_value);
        } else if(prop_name == "max_warning") {
            def_prop.set_max_warning(prop_value);
        } else if(prop_name == "delta_val") {
            def_prop.set_delta_val(prop_value);
        } else if(prop_name == "delta_t") {
            def_prop.set_delta_t(prop_value);
        } else if(prop_name == "abs_change") {
            def_prop.set_event_abs_change(prop_value);
        } else if(prop_name == "rel_change") {
            def_prop.set_event_rel_change(prop_value);
        } else if(prop_name == "period") {
            def_prop.set_event_period(prop_value);
        } else if(prop_name == "archive_abs_change") {
            def_prop.set_archive_event_abs_change(prop_value);
        } else if(prop_name == "archive_rel_change") {
            def_prop.set_archive_event_rel_change(prop_value);
        } else if(prop_name == "archive_period") {
            def_prop.set_archive_event_period(prop_value);
        } else if(prop_name == "enum_labels") {
            // Convert string back to vector
            std::vector<std::string> labels;
            const std::string &label_str = prop.get_value();
            size_t offset = 0, pos = 0;
            while((pos = label_str.find(',', offset)) != std::string::npos) {
                labels.push_back(label_str.substr(offset, pos - offset));
                offset = pos + 1;
            }
            labels.push_back(label_str.substr(offset));
            def_prop.set_enum_labels(labels);
        }
    }
}

void export_attr(py::module &m) {
    py::class_<Tango::AttrProperty>(m, "AttrProperty")
        .def(py::init<const char *, const char *>())
        .def("get_value",
             static_cast<const std::string &(Tango::AttrProperty::*) () const>(&Tango::AttrProperty::get_value),
             py::return_value_policy::copy)
        .def("get_lg_value", &Tango::AttrProperty::get_lg_value)
        .def("get_name",
             static_cast<const std::string &(Tango::AttrProperty::*) () const>(&Tango::AttrProperty::get_name),
             py::return_value_policy::copy);

    py::class_<Tango::Attr, PyScaAttr>(m,
                                       "Attr",
                                       R"doc()doc")
        .def(py::init<const char *, long, Tango::AttrWriteType>(),
             py::arg("name"),
             py::arg("data_type"),
             py::arg("w_type") = Tango::READ)
        .def("set_default_properties",
             &Tango::Attr::set_default_properties,
             R"doc(
                set_default_properties(self)

                    Set default attribute properties.

                    :param attr_prop: the user default property class
                    :type attr_prop: UserDefaultAttrProp)doc")
        .def("set_disp_level",
             &Tango::Attr::set_disp_level,
             R"doc(
                set_disp_level(self, disp_level)

                    Set the attribute display level.

                    :param disp_level: the new display level
                    :type disp_level: DispLevel)doc",
             py::arg("disp_level"))
        .def("set_polling_period",
             &Tango::Attr::set_polling_period,
             R"doc(
                set_polling_period(self, period_ms)

                    Set the attribute polling update period.

                    :param period_ms: the attribute polling period (in mS)
                    :type period_ms: int)doc",
             py::arg("period_ms"))
        .def("set_memorized",
             &Tango::Attr::set_memorized,
             R"doc(
                set_memorized(self)

                    Set the attribute as memorized in database (only for scalar
                    and writable attribute).

                    By default the setpoint will be written to the attribute during initialisation!
                    Use method set_memorized_init() with False as argument if you don't
                    want this feature.)doc")
        .def("set_memorized_init",
             &Tango::Attr::set_memorized_init,
             R"doc(
                set_memorized_init(self, write_on_init)

                    Set the initialisation flag for memorized attributes.

                    - true = the setpoint value will be written to the attribute on initialisation
                    - false = only the attribute setpoint is initialised.

                    No action is taken on the attribute

                    :param write_on_init: if true the setpoint value will be written
                                          to the attribute on initialisation
                    :type write_on_init: bool)doc",
             py::arg("write_on_init"))
        .def("set_change_event",
             &Tango::Attr::set_change_event,
             R"doc(
                set_change_event(self, implemented, detect)

                    Set a flag to indicate that the server fires change events manually
                    without the polling to be started for the attribute.

                    If the detect parameter is set to true, the criteria specified for the
                    change event (rel_change and abs_change) are verified and
                    the event is only pushed if a least one of them are fulfilled
                    (change in value compared to previous event exceeds a threshold).

                    If detect is set to false the event is fired without checking!

                    :param implemented: True when the server fires change events manually.
                    :type implemented: bool
                    :param detect: Triggers the verification of the change event properties
                                   when set to true.
                    :type detect: bool)doc",
             py::arg("implemented"),
             py::arg("detect"))
        .def("is_change_event",
             &Tango::Attr::is_change_event,
             R"doc(
                is_change_event(self) -> bool

                    Check if the change event is fired manually for this attribute.

                    :returns: true if a manual fire change event is implemented.
                    :rtype: bool)doc")
        .def("set_alarm_event",
             &Tango::Attr::set_alarm_event,
             R"doc(
                set_alarm_event(self, implemented, detect)

                    Set a flag to indicate that the server fires alarm events manually
                    without the polling to be started for the attribute.

                    If the detect parameter is set to true, the criteria specified for the
                    alarm event (rel_change and abs_change) are verified and
                    the event is only pushed if a least one of them are fulfilled
                    (change in value compared to previous event exceeds a threshold).

                    If detect is set to false the event is fired without checking!

                    :param implemented: True when the server fires alarm events manually.
                    :type implemented: bool
                    :param detect: Triggers the verification of the alarm event properties
                                   when set to true.
                    :type detect: bool

                    .. versionadded:: 10.0.0)doc",
             py::arg("implemented"),
             py::arg("detect"))
        .def("is_alarm_event",
             &Tango::Attr::is_alarm_event,
             R"doc(
                is_alarm_event(self) -> bool

                    Check if the alarm event is fired manually (without polling) for this attribute.

                :return: true if a manual fire alarm event is implemented
                :rtype: bool

                .. versionadded:: 10.0.0
             )doc")
        .def("is_check_change_criteria",
             &Tango::Attr::is_check_change_criteria,
             R"doc(
                is_check_change_criteria(self) -> bool

                    Check if the change event criteria should be checked when firing the event manually.

                :returns: true if a change event criteria will be checked.
                :rtype: bool)doc")
        .def("set_archive_event",
             &Tango::Attr::set_archive_event,
             R"doc(
                set_archive_event(self)

                    Set a flag to indicate that the server fires archive events manually
                    without the polling to be started for the attribute.

                    If the detect parameter is set to true, the criteria specified for the
                    archive event (rel_change and abs_change) are verified and
                    the event is only pushed if a least one of them are fulfilled
                    (change in value compared to previous event exceeds a threshold).

                    If detect is set to false the event is fired without checking!

                :param implemented: True when the server fires change events manually.
                :type implemented: bool
                :param detect: Triggers the verification of the archive event properties
                               when set to true.
                :type detect: bool)doc",
             py::arg("implemented"),
             py::arg("detect"))
        .def("is_archive_event",
             &Tango::Attr::is_archive_event,
             R"doc(
                is_archive_event(self) -> bool

                    Check if the archive event is fired manually for this attribute.

                :returns: true if a manual fire archive event is implemented.
                :rtype: bool)doc")
        .def("is_check_archive_criteria",
             &Tango::Attr::is_check_archive_criteria,
             R"doc(
                is_check_archive_criteria(self) -> bool

                    Check if the archive event criteria should be checked when firing the event manually.

                :returns: true if a archive event criteria will be checked.
                :rtype: bool)doc")
        .def("set_data_ready_event",
             &Tango::Attr::set_data_ready_event,
             R"doc(
                set_data_ready_event(self, implemented)

                    Set a flag to indicate that the server fires data ready events.

                :param implemented: True when the server fires data ready events
                :type implemented: bool

                New in PyTango 7.2.0)doc",
             py::arg("implemented"))
        .def("is_data_ready_event",
             &Tango::Attr::is_data_ready_event,
             R"doc(
                is_data_ready_event(self) -> bool

                    Check if the data ready event is fired for this attribute.

                    :returns: true if firing data ready event is implemented.
                    :rtype: bool

                    New in PyTango 7.2.0)doc")
        .def("get_name",
             static_cast<const std::string &(Tango::Attr::*) () const>(&Tango::Attr::get_name),
             py::return_value_policy::copy,
             R"doc(
                get_name(self) -> str

                    Get the attribute name.

                :returns: the attribute name
                :rtype: str)doc")
        .def("get_format",
             &Tango::Attr::get_format,
             R"doc(
                get_format(self) -> AttrDataFormat

                    Get the attribute format.

                :returns: the attribute format
                :rtype: AttrDataFormat)doc")
        .def("get_writable",
             &Tango::Attr::get_writable,
             R"doc(
                get_writable(self) -> AttrWriteType

                    Get the attribute write type.

                :returns: the attribute write type
                :rtype: AttrWriteType)doc")
        .def("get_type",
             &Tango::Attr::get_type,
             R"doc(
                get_type(self) -> int

                    Get the attribute data type.

                :returns: the attribute data type
                :rtype: int)doc")
        .def("get_disp_level",
             &Tango::Attr::get_disp_level,
             R"doc(
                get_disp_level(self) -> DispLevel

                    Get the attribute display level.

                :returns: the attribute display level
                :rtype: DispLevel)doc")
        .def("get_polling_period",
             &Tango::Attr::get_polling_period,
             R"doc(
                get_polling_period(self) -> int

                    Get the polling period (mS).

                :returns: the polling period (mS)
                :rtype: int)doc")
        .def("get_memorized",
             &Tango::Attr::get_memorized,
             R"doc(
                get_memorized(self) -> bool

                    Determine if the attribute is memorized or not.

                :returns: True if the attribute is memorized
                :rtype: bool)doc")
        .def("get_memorized_init",
             &Tango::Attr::get_memorized_init,
             R"doc(
                get_memorized_init(self) -> bool

                    Determine if the attribute is written at startup from the memorized
                    value if it is memorized.

                :returns: True if initialized with memorized value or not
                :rtype: bool)doc")
        .def("get_assoc",
             &Tango::Attr::get_assoc,
             py::return_value_policy::copy,
             R"doc(
                get_assoc(self) -> str

                    Get the associated name.

                :returns: the associated name
                :rtype: bool)doc")
        .def("is_assoc",
             &Tango::Attr::is_assoc,
             R"doc(
                is_assoc(self) -> bool

                    Determine if it is assoc.

                :returns: if it is assoc
                :rtype: bool)doc")
        .def("get_cl_name",
             &Tango::Attr::get_cl_name,
             py::return_value_policy::copy,
             R"doc(
                get_cl_name(self) -> str

                    Returns the class name.

                :returns: the class name
                :rtype: str

                New in PyTango 7.2.0)doc")
        .def("set_cl_name",
             &Tango::Attr::set_cl_name,
             R"doc(
                set_cl_name(self, cl)

                    Sets the class name.

                :param cl: new class name
                :type cl: str

                New in PyTango 7.2.0)doc")
        .def("get_class_properties",
             &Tango::Attr::get_class_properties,
             py::return_value_policy::reference_internal,
             R"doc(
                get_class_properties(self) -> Sequence[AttrProperty]

                    Get the class level attribute properties.

                :returns: the class attribute properties
                :rtype: Sequence[AttrProperty])doc")
        .def("get_user_default_properties",
             &Tango::Attr::get_user_default_properties,
             py::return_value_policy::reference_internal,
             R"doc(
                get_user_default_properties(self) -> Sequence[AttrProperty]

                    Get the user default attribute properties.

                :returns: the user default attribute properties
                :rtype: Sequence[AttrProperty])doc")
        .def("set_class_properties",
             &Tango::Attr::set_class_properties,
             R"doc(
                set_class_properties(self, props)

                    Set the class level attribute properties.

                :param props: new class level attribute properties
                :type props: StdAttrPropertyVector)doc")
        .def("check_type",
             &Tango::Attr::check_type,
             R"doc(
                check_type(self)

                    This method checks data type and throws an exception in case of unsupported data type

                :raises: :class:`DevFailed`: If the data type is unsupported.)doc")
        .def("read", &Tango::Attr::read)
        .def("write", &Tango::Attr::write)
        .def("is_allowed",
             &Tango::Attr::is_allowed,
             R"doc(
                is_allowed(self, device, request_type) -> bool

                    Returns whether the request_type is allowed for the specified device

                :param device: instance of Device
                :type device: :class:`tango.server.Device`

                :param request_type: AttReqType.READ_REQ for read request or AttReqType.WRITE_REQ for write request
                :type request_type: :const:`AttReqType`

                :returns: True if request_type is allowed for the specified device
                :rtype: bool)doc",
             py::arg("device"),
             py::arg("request_type"));

    py::class_<Tango::SpectrumAttr, Tango::Attr>(m, "SpectrumAttr")
        .def(py::init<const char *, long, Tango::AttrWriteType, long>());

    py::class_<Tango::ImageAttr, Tango::SpectrumAttr>(m, "ImageAttr")
        .def(py::init<const char *, long, Tango::AttrWriteType, long, long>());
}
