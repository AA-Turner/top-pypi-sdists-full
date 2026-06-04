/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "pyutils.h"

namespace PyAttrConfEventData {
static std::shared_ptr<Tango::AttrConfEventData> makeAttrConfEventData(py::object device_proxy,
                                                                       py::object attr_name,
                                                                       py::object event_name,
                                                                       py::object attr_conf,
                                                                       py::object event_reason,
                                                                       py::object errors) {
    // Extract DeviceProxy pointer (nullptr if None)
    Tango::DeviceProxy *dev_ptr = device_proxy.is_none() ? nullptr : device_proxy.cast<Tango::DeviceProxy *>();

    // Extract attribute name (empty string if None)
    std::string attr_name_str = attr_name.is_none() ? "" : attr_name.cast<std::string>();

    // Extract event name (empty string if None)
    std::string event_name_str = event_name.is_none() ? "" : event_name.cast<std::string>();

    // Extract AttributeInfoEx (deep copy if provided)
    Tango::AttributeInfoEx *attr_conf_ptr = nullptr;
    std::unique_ptr<Tango::AttributeInfoEx> attr_conf_owner;
    if(!attr_conf.is_none()) {
        attr_conf_owner = std::make_unique<Tango::AttributeInfoEx>(attr_conf.cast<Tango::AttributeInfoEx>());
        attr_conf_ptr = attr_conf_owner.get();
    }

    // Extract EventReason (default to Update if None)
    Tango::EventReason reason =
        event_reason.is_none() ? Tango::EventReason::Update : event_reason.cast<Tango::EventReason>();

    // Extract DevErrorList (empty list if None)
    Tango::DevErrorList error_list = errors.is_none() ? Tango::DevErrorList{} : errors.cast<Tango::DevErrorList>();

    // Create the AttrConfEventData with the extracted values
    auto event_data = std::make_shared<Tango::AttrConfEventData>(
        dev_ptr, attr_name_str, event_name_str, attr_conf_ptr, reason, error_list);

    if(attr_conf_owner) {
        attr_conf_owner.release();
    }

    return event_data;
}

static void set_errors(Tango::AttrConfEventData &event_data, py::object &dev_failed) {
    event_data.errors = dev_failed.attr("args").cast<Tango::DevErrorList>();
}
} // namespace PyAttrConfEventData

void export_attr_conf_event_data(py::module &m) {
    py::class_<Tango::AttrConfEventData, std::shared_ptr<Tango::AttrConfEventData>>(m,
                                                                                    "AttrConfEventData",
                                                                                    py::dynamic_attr(),
                                                                                    R"doc(
    This class is used to pass data to the callback method when an
    attribute configuration event (:obj:`tango.EventType.ATTR_CONF_EVENT`)
    is sent to the client. It contains the
    following public fields:

    - device : (DeviceProxy) The DeviceProxy object on which the call was executed
    - attr_name : (str) The attribute name
    - event : (str) The event type name
    - event_reason : (EventReason) The reason for the event
    - attr_conf : (AttributeInfoEx) The attribute data
    - err : (bool) A boolean flag set to true if the request failed. False
      otherwise
    - errors : (list[DevError]) The error stack
    - reception_date: (TimeVal)
)doc")
        .def(py::init<const Tango::AttrConfEventData &>(), py::arg("event"))
        .def(py::init(&PyAttrConfEventData::makeAttrConfEventData),
             py::arg("device_proxy") = py::none(),
             py::arg("attr_name") = py::none(),
             py::arg("event_name") = py::none(),
             py::arg("attr_conf") = py::none(),
             py::arg("event_reason") = py::none(),
             py::arg("errors") = py::none())
        .def_readwrite("device", &Tango::AttrConfEventData::device)
        .def_readwrite("attr_name", &Tango::AttrConfEventData::attr_name)
        .def_readwrite("event", &Tango::AttrConfEventData::event)
        .def_readwrite("event_reason", &Tango::AttrConfEventData::event_reason)
        .def_readwrite("err", &Tango::AttrConfEventData::err)
        .def_readwrite("reception_date", &Tango::AttrConfEventData::reception_date)
        .def_readwrite("attr_conf", &Tango::AttrConfEventData::attr_conf)
        .def_property(
            "errors",
            [](Tango::AttrConfEventData &self) -> Tango::DevErrorList & { return self.errors; },
            &PyAttrConfEventData::set_errors,
            py::return_value_policy::reference_internal)
        .def("get_date",
             &Tango::AttrConfEventData::get_date,
             R"doc(
                Returns the timestamp of the event.

                .. versionadded:: 7.0.0
             )doc",
             py::return_value_policy::reference_internal);
    fix_dynamic_attr_dealloc<Tango::AttrConfEventData>();
}
