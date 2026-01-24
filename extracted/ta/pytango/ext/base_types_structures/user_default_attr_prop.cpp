/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_user_default_attr_prop(py::module &m) {
    py::class_<Tango::UserDefaultAttrProp>(m,
                                           "UserDefaultAttrProp",
                                           R"doc(
                User class to set attribute default properties.

                This class is used to set attribute default properties.
                Three levels of attributes properties setting are implemented within Tango.
                The highest property setting level is the database.
                Then the user default (set using this UserDefaultAttrProp class) and finally
                a Tango library default value.)doc")
        .def(py::init<>())
        .def("set_label",
             &Tango::UserDefaultAttrProp::set_label,
             R"doc(
                set_label(self, def_label)

                    Set default label property.

                :param def_label: the user default label property
                :type def_label: str)doc",
             py::arg(""))
        .def("set_description",
             &Tango::UserDefaultAttrProp::set_description,
             R"doc(
                set_description(self, def_description: str)

                    Set default description property.

                :param def_description: the user default description property
                :type def_description: str)doc",
             py::arg("def_description"))
        .def("set_format",
             &Tango::UserDefaultAttrProp::set_format,
             R"doc(
                set_format(self, def_format)

                    Set default format property.

                    :param def_format: the user default format property
                    :type def_format: str)doc")
        .def("set_unit",
             &Tango::UserDefaultAttrProp::set_unit,
             R"doc(
                set_unit(self, def_unit)

                    Set default unit property.

                    :param def_unit: te user default unit property
                    :type def_unit: str)doc")
        .def("set_standard_unit",
             &Tango::UserDefaultAttrProp::set_standard_unit,
             R"doc(
                set_standard_unit(self, def_standard_unit)

                    Set default standard unit property.

                    :param def_standard_unit: the user default standard unit property
                    :type def_standard_unit: str)doc")
        .def("set_display_unit",
             &Tango::UserDefaultAttrProp::set_display_unit,
             R"doc(
                set_display_unit(self, def_display_unit)

                    Set default display unit property.

                    :param def_display_unit: the user default display unit property
                    :type def_display_unit: str)doc")
        .def("set_min_value",
             &Tango::UserDefaultAttrProp::set_min_value,
             R"doc(
                set_min_value(self, def_min_value)

                    Set default min_value property.

                    :param def_min_value: the user default min_value property
                    :type def_min_value: str)doc")
        .def("set_max_value",
             &Tango::UserDefaultAttrProp::set_max_value,
             R"doc(
                set_max_value(self, def_max_value)

                    Set default max_value property.

                    :param def_max_value: the user default max_value property
                    :type def_max_value: str)doc")
        .def("set_min_alarm",
             &Tango::UserDefaultAttrProp::set_min_alarm,
             R"doc(
                set_min_alarm(self, def_min_alarm)

                    Set default min_alarm property.

                    :param def_min_alarm: the user default min_alarm property
                    :type def_min_alarm: str)doc")
        .def("set_max_alarm",
             &Tango::UserDefaultAttrProp::set_max_alarm,
             R"doc(
                set_max_alarm(self, def_max_alarm)

                    Set default max_alarm property.

                    :param def_max_alarm: the user default max_alarm property
                    :type def_max_alarm: str)doc")
        .def("set_min_warning",
             &Tango::UserDefaultAttrProp::set_min_warning,
             R"doc(
                set_min_warning(self, def_min_warning)

                    Set default min_warning property.

                    :param def_min_warning: the user default min_warning property
                    :type def_min_warning: str)doc")
        .def("set_max_warning",
             &Tango::UserDefaultAttrProp::set_max_warning,
             R"doc(
                set_max_warning(self, def_max_warning)

                    Set default max_warning property.

                    :param def_max_warning: the user default max_warning property
                    :type def_max_warning: str)doc")
        .def("set_delta_t",
             &Tango::UserDefaultAttrProp::set_delta_t,
             R"doc(
                set_delta_t(self, def_delta_t)

                    Set default RDS alarm delta_t property.

                    :param def_delta_t: the user default RDS alarm delta_t property
                    :type def_delta_t: str)doc")
        .def("set_delta_val",
             &Tango::UserDefaultAttrProp::set_delta_val,
             R"doc(
                set_delta_val(self, def_delta_val)

                    Set default RDS alarm delta_val property.

                    :param def_delta_val: the user default RDS alarm delta_val property
                    :type def_delta_val: str)doc")
        .def("set_abs_change",
             &Tango::UserDefaultAttrProp::set_event_abs_change,
             R"doc(
                set_abs_change(self, def_abs_change) <= DEPRECATED

                    Set default change event abs_change property.

                    :param def_abs_change: the user default change event abs_change property
                    :type def_abs_change: str

                    Deprecated since PyTango 8.0. Please use set_event_abs_change instead.)doc")
        .def("set_rel_change",
             &Tango::UserDefaultAttrProp::set_event_rel_change,
             R"doc(
                set_rel_change(self, def_rel_change) <= DEPRECATED

                    Set default change event rel_change property.

                    :param def_rel_change: the user default change event rel_change property
                    :type def_rel_change: str

                    Deprecated since PyTango 8.0. Please use set_event_rel_change instead.)doc")
        .def("set_period",
             &Tango::UserDefaultAttrProp::set_event_period,
             R"doc(
                set_period(self, def_period) <= DEPRECATED

                    Set default periodic event period property.

                    :param def_period: the user default periodic event period property
                    :type def_period: str

                    Deprecated since PyTango 8.0. Please use set_event_period instead.)doc")
        .def("set_archive_abs_change",
             &Tango::UserDefaultAttrProp::set_archive_event_abs_change,
             R"doc(
                set_archive_abs_change(self, def_archive_abs_change) <= DEPRECATED

                    Set default archive event abs_change property.

                    :param def_archive_abs_change: the user default archive event abs_change property
                    :type def_archive_abs_change: str

                    Deprecated since PyTango 8.0. Please use set_archive_event_abs_change instead.)doc")
        .def("set_archive_rel_change",
             &Tango::UserDefaultAttrProp::set_archive_event_rel_change,
             R"doc(
                set_archive_rel_change(self, def_archive_rel_change) <= DEPRECATED

                    Set default archive event rel_change property.

                    :param def_archive_rel_change: the user default archive event rel_change property
                    :type def_archive_rel_change: str

                    Deprecated since PyTango 8.0. Please use set_archive_event_rel_change instead.)doc")
        .def("set_archive_period",
             &Tango::UserDefaultAttrProp::set_archive_event_period,
             R"doc(
                set_archive_period(self, def_archive_period) <= DEPRECATED

                    Set default archive event period property.

                    :param def_archive_period: t
                    :type def_archive_period: str

                    Deprecated since PyTango 8.0. Please use set_archive_event_period instead.)doc")

        .def("set_event_abs_change",
             &Tango::UserDefaultAttrProp::set_event_abs_change,
             R"doc(
                set_event_abs_change(self, def_abs_change)

                    Set default change event abs_change property.

                    :param def_abs_change: the user default change event abs_change property
                    :type def_abs_change: str

                    New in PyTango 8.0)doc")
        .def("set_event_rel_change",
             &Tango::UserDefaultAttrProp::set_event_rel_change,
             R"doc(
                set_event_rel_change(self, def_rel_change)

                    Set default change event rel_change property.

                    :param def_rel_change: the user default change event rel_change property
                    :type def_rel_change: str

                    New in PyTango 8.0)doc")
        .def("set_event_period",
             &Tango::UserDefaultAttrProp::set_event_period,
             R"doc(
                set_event_period(self, def_period)

                    Set default periodic event period property.

                    :param def_period: the user default periodic event period property
                    :type def_period: str

                    New in PyTango 8.0)doc")
        .def("set_archive_event_abs_change",
             &Tango::UserDefaultAttrProp::set_archive_event_abs_change,
             R"doc(
                set_archive_event_abs_change(self, def_archive_abs_change)

                    Set default archive event abs_change property.

                    :param def_archive_abs_change: the user default archive event abs_change property
                    :type def_archive_abs_change: str

                    New in PyTango 8.0)doc")
        .def("set_archive_event_rel_change",
             &Tango::UserDefaultAttrProp::set_archive_event_rel_change,
             R"doc(
                set_archive_event_rel_change(self, def_archive_rel_change)

                    Set default archive event rel_change property.

                    :param def_archive_rel_change: the user default archive event rel_change property
                    :type def_archive_rel_change: str

                    New in PyTango 8.0)doc")
        .def("set_archive_event_period",
             &Tango::UserDefaultAttrProp::set_archive_event_period,
             R"doc(
                set_archive_event_period(self, def_archive_period)

                    Set default archive event period property.

                    :param def_archive_period: t
                    :type def_archive_period: str

                    New in PyTango 8.0)doc")

        .def("_set_enum_labels", &Tango::UserDefaultAttrProp::set_enum_labels)

        .def_readwrite("label", &Tango::UserDefaultAttrProp::label)
        .def_readwrite("description", &Tango::UserDefaultAttrProp::description)
        .def_readwrite("unit", &Tango::UserDefaultAttrProp::unit)
        .def_readwrite("standard_unit", &Tango::UserDefaultAttrProp::standard_unit)
        .def_readwrite("display_unit", &Tango::UserDefaultAttrProp::display_unit)
        .def_readwrite("format", &Tango::UserDefaultAttrProp::format)
        .def_readwrite("min_value", &Tango::UserDefaultAttrProp::min_value)
        .def_readwrite("max_value", &Tango::UserDefaultAttrProp::max_value)
        .def_readwrite("min_alarm", &Tango::UserDefaultAttrProp::min_alarm)
        .def_readwrite("max_alarm", &Tango::UserDefaultAttrProp::max_alarm)
        .def_readwrite("min_warning", &Tango::UserDefaultAttrProp::min_warning)
        .def_readwrite("max_warning", &Tango::UserDefaultAttrProp::max_warning)
        .def_readwrite("delta_val", &Tango::UserDefaultAttrProp::delta_val)
        .def_readwrite("delta_t", &Tango::UserDefaultAttrProp::delta_t)
        .def_readwrite("abs_change", &Tango::UserDefaultAttrProp::abs_change)
        .def_readwrite("rel_change", &Tango::UserDefaultAttrProp::rel_change)
        .def_readwrite("period", &Tango::UserDefaultAttrProp::period)
        .def_readwrite("archive_abs_change", &Tango::UserDefaultAttrProp::archive_abs_change)
        .def_readwrite("archive_rel_change", &Tango::UserDefaultAttrProp::archive_rel_change)
        .def_readwrite("archive_period", &Tango::UserDefaultAttrProp::archive_period)
        .def_readwrite("enum_labels", &Tango::UserDefaultAttrProp::enum_labels);
}
