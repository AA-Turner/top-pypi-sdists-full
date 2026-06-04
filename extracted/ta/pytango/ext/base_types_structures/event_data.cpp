/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "client/device_attribute.h"
#include "pyutils.h"

namespace PyEventData {
static std::shared_ptr<Tango::EventData> makeEventData(py::object device_proxy,
                                                       py::object attr_name,
                                                       py::object event_name,
                                                       py::object attr_value,
                                                       py::object event_reason,
                                                       py::object errors) {
    // Extract DeviceProxy pointer (nullptr if None)
    Tango::DeviceProxy *dev_ptr = device_proxy.is_none() ? nullptr : device_proxy.cast<Tango::DeviceProxy *>();

    // Extract attribute name (empty string if None)
    std::string attr_name_str = attr_name.is_none() ? "" : attr_name.cast<std::string>();

    // Extract event name (empty string if None)
    std::string event_name_str = event_name.is_none() ? "" : event_name.cast<std::string>();

    // Extract DeviceAttribute (deep copy if provided)
    Tango::DeviceAttribute *attr_ptr = nullptr;
    std::unique_ptr<Tango::DeviceAttribute> attr_owner;
    if(!attr_value.is_none()) {
        attr_owner = std::make_unique<Tango::DeviceAttribute>(attr_value.cast<Tango::DeviceAttribute>());
        attr_ptr = attr_owner.get();
    }

    // Extract EventReason (default to Update if None)
    Tango::EventReason reason =
        event_reason.is_none() ? Tango::EventReason::Update : event_reason.cast<Tango::EventReason>();

    // Extract DevErrorList (empty list if None)
    Tango::DevErrorList error_list = errors.is_none() ? Tango::DevErrorList{} : errors.cast<Tango::DevErrorList>();

    // Create the EventData with the extracted values
    // clang-format off
    auto event_data = std::make_shared<Tango::EventData>(dev_ptr,
                                                         attr_name_str,
                                                         event_name_str,
                                                         attr_ptr,
                                                         reason,
                                                         error_list);
    // clang-format on
    if(attr_owner) {
        // Transfer ownership to EventData which will delete attr_value in its destructor
        attr_owner.release();
    }
    return event_data;
}

static void set_errors(Tango::EventData &event_data, py::object &error) {
    event_data.errors = error.attr("args").cast<Tango::DevErrorList>();
}

static Tango::DevErrorList get_errors(Tango::EventData &event_data) {
    return event_data.errors;
}
} // namespace PyEventData

void export_event_data(py::module &m) {
    py::class_<Tango::EventData, std::shared_ptr<Tango::EventData>> EventData(m,
                                                                              "EventData",
                                                                              py::dynamic_attr(),
                                                                              R"doc(
    This class is used to pass data to the callback method when an event
    related to attribute data is sent to the client. It contains the following public fields:

    - device : (DeviceProxy) The DeviceProxy object on which the call was
      executed.
    - attr_name : (str) The attribute name
    - event : (str) The event type name
    - event_reason : (EventReason) The reason for the event
    - attr_value : (DeviceAttribute) The attribute data
    - err : (bool) A boolean flag set to true if the request failed. False
      otherwise
    - errors : (list[DevError]) The error stack
    - reception_date: (TimeVal)

    .. note::
        The ``attr_value`` field may be ``None``.  E.g., if ``err`` is True, or when subscribing in
        ``EventSubMode.Async`` mode and the initial callback is received with ``EventReason.SubSuccess``.
)doc");

    EventData.def(py::init<const Tango::EventData &>(), py::arg("event"))
        .def(py::init(&PyEventData::makeEventData),
             py::arg("device_proxy") = py::none(),
             py::arg("attr_name") = py::none(),
             py::arg("event_name") = py::none(),
             py::arg("attr_value") = py::none(),
             py::arg("event_reason") = py::none(),
             py::arg("errors") = py::none())
        .def_readwrite("device", &Tango::EventData::device)
        .def_readwrite("attr_name", &Tango::EventData::attr_name)
        .def_readwrite("event", &Tango::EventData::event)
        .def_readwrite("event_reason", &Tango::EventData::event_reason)

        .def_readwrite("err", &Tango::EventData::err)
        .def_readwrite("reception_date", &Tango::EventData::reception_date)
        .def_property("errors", &PyEventData::get_errors, &PyEventData::set_errors)

        .def("get_date",
             &Tango::EventData::get_date,
             py::return_value_policy::reference_internal,
             R"doc(
                Returns the timestamp of the event.

                .. versionadded:: 7.0.0
             )doc")

        // We initialize "attr_value" field with None and
        // later in callback.cpp (PyEventCallBack::fill_py_event) save extracted value

        .attr("attr_value") = py::none();
    fix_dynamic_attr_dealloc<Tango::EventData>();
}
