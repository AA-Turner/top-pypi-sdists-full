/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

namespace PyEventData {
static std::shared_ptr<Tango::EventData> makeEventData() {
    Tango::EventData *result = new Tango::EventData;

    // workaround https://gitlab.com/tango-controls/cppTango/-/issues/1383
    result->attr_value = new Tango::DeviceAttribute();
    result->device = nullptr;

    return std::shared_ptr<Tango::EventData>(result);
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
         - errors : (sequence<DevError>) The error stack
         - reception_date: (TimeVal)

    .. note::
        The ``attr_value`` field may be ``None``.  E.g., if ``err`` is True, or when subscribing in
        ``EventSubMode.Async`` mode and the initial callback is received with ``EventReason.SubSuccess``.
)doc");

    EventData
        .def(py::init<const Tango::EventData &>())

        .def(py::init(&PyEventData::makeEventData))

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
                get_date(self) -> TimeVal

                    Returns the timestamp of the event.

                :returns: the timestamp of the event
                :rtype: TimeVal

                New in PyTango 7.0.0)doc")

        // The original Tango::EventData structure has "get_attr_value" but
        // we can't refer it directly here because we have to extract value
        // and so on. So we initialize "attr_value" field with None and
        // later in callback.cpp (PyEventCallBack::fill_py_event) save extracted value

        .attr("attr_value") = py::none();
}
