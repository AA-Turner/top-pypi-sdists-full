/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

// Binding template
template <typename AttributeConfigType>
py::class_<AttributeConfigType> bind_AttributeConfig(py::module &m, const std::string &class_name) {
    py::class_<AttributeConfigType> attribute_config(m, class_name.c_str());
    attribute_config
        .def(py::init<>())
        .def_readwrite("name", &AttributeConfigType::name)
        .def_readwrite("writable", &AttributeConfigType::writable)
        .def_readwrite("data_format", &AttributeConfigType::data_format)
        .def_readwrite("data_type", &AttributeConfigType::data_type)
        .def_readwrite("max_dim_x", &AttributeConfigType::max_dim_x)
        .def_readwrite("max_dim_y", &AttributeConfigType::max_dim_y)
        .def_readwrite("description", &AttributeConfigType::description)
        .def_readwrite("label", &AttributeConfigType::label)
        .def_readwrite("unit", &AttributeConfigType::unit)
        .def_readwrite("standard_unit", &AttributeConfigType::standard_unit)
        .def_readwrite("display_unit", &AttributeConfigType::display_unit)
        .def_readwrite("format", &AttributeConfigType::format)
        .def_readwrite("min_value", &AttributeConfigType::min_value)
        .def_readwrite("max_value", &AttributeConfigType::max_value)
        .def_readwrite("writable_attr_name", &AttributeConfigType::writable_attr_name)
        .def_readwrite("extensions", &AttributeConfigType::extensions);
    return attribute_config;
}

void export_attribute_configs(py::module &m) {
    py::class_<Tango::AttributeAlarm>(m, "AttributeAlarm")
        .def(py::init<>())
        .def_readwrite("min_alarm", &Tango::AttributeAlarm::min_alarm)
        .def_readwrite("max_alarm", &Tango::AttributeAlarm::max_alarm)
        .def_readwrite("min_warning", &Tango::AttributeAlarm::min_warning)
        .def_readwrite("max_warning", &Tango::AttributeAlarm::max_warning)
        .def_readwrite("delta_t", &Tango::AttributeAlarm::delta_t)
        .def_readwrite("delta_val", &Tango::AttributeAlarm::delta_val)
        .def_readwrite("extensions", &Tango::AttributeAlarm::extensions);

    py::class_<Tango::ChangeEventProp>(m, "ChangeEventProp")
        .def(py::init<>())
        .def_readwrite("rel_change", &Tango::ChangeEventProp::rel_change)
        .def_readwrite("abs_change", &Tango::ChangeEventProp::abs_change)
        .def_readwrite("extensions", &Tango::ChangeEventProp::extensions);

    py::class_<Tango::PeriodicEventProp>(m, "PeriodicEventProp")
        .def(py::init<>())
        .def_readwrite("period", &Tango::PeriodicEventProp::period)
        .def_readwrite("extensions", &Tango::PeriodicEventProp::extensions);

    py::class_<Tango::ArchiveEventProp>(m, "ArchiveEventProp")
        .def(py::init<>())
        .def_readwrite("rel_change", &Tango::ArchiveEventProp::rel_change)
        .def_readwrite("abs_change", &Tango::ArchiveEventProp::abs_change)
        .def_readwrite("period", &Tango::ArchiveEventProp::period)
        .def_readwrite("extensions", &Tango::ArchiveEventProp::extensions);

    py::class_<Tango::EventProperties>(m, "EventProperties")
        .def(py::init<>())
        .def_readwrite("ch_event", &Tango::EventProperties::ch_event)
        .def_readwrite("per_event", &Tango::EventProperties::per_event)
        .def_readwrite("arch_event", &Tango::EventProperties::arch_event);

    auto AttributeConfig = bind_AttributeConfig<Tango::AttributeConfig>(m, "AttributeConfig");

    AttributeConfig
        .def_readwrite("min_alarm", &Tango::AttributeConfig::min_alarm)
        .def_readwrite("max_alarm", &Tango::AttributeConfig::max_alarm);

    auto AttributeConfig_2 = bind_AttributeConfig<Tango::AttributeConfig_2>(m, "AttributeConfig_2");
    AttributeConfig_2
        .def_readwrite("min_alarm", &Tango::AttributeConfig_2::min_alarm)
        .def_readwrite("max_alarm", &Tango::AttributeConfig_2::max_alarm)
        .def_readwrite("level", &Tango::AttributeConfig_2::level);

    auto AttributeConfig_3 = bind_AttributeConfig<Tango::AttributeConfig_3>(m, "AttributeConfig_3");
    AttributeConfig_3
        .def_readwrite("level", &Tango::AttributeConfig_3::level)
        .def_readwrite("att_alarm", &Tango::AttributeConfig_3::att_alarm)
        .def_readwrite("event_prop", &Tango::AttributeConfig_3::event_prop)
        .def_readwrite("sys_extensions", &Tango::AttributeConfig_3::sys_extensions);

    auto AttributeConfig_5 = bind_AttributeConfig<Tango::AttributeConfig_5>(m, "AttributeConfig_5");
    AttributeConfig_5
        .def_readwrite("memorized", &Tango::AttributeConfig_5::memorized)
        .def_readwrite("mem_init", &Tango::AttributeConfig_5::mem_init)
        .def_readwrite("level", &Tango::AttributeConfig_5::level)
        .def_readwrite("root_attr_name", &Tango::AttributeConfig_5::root_attr_name)
        .def_readwrite("enum_labels", &Tango::AttributeConfig_5::enum_labels)
        .def_readwrite("att_alarm", &Tango::AttributeConfig_5::att_alarm)
        .def_readwrite("event_prop", &Tango::AttributeConfig_5::event_prop)
        .def_readwrite("sys_extensions", &Tango::AttributeConfig_5::sys_extensions);
}
