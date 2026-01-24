/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

namespace PyDevIntrChangeEventData {
static std::shared_ptr<Tango::DevIntrChangeEventData> makeDevIntrChangeEventData() {
    auto result = std::make_shared<Tango::DevIntrChangeEventData>();

    // workaround https://gitlab.com/tango-controls/cppTango/-/issues/1383
    result->device = nullptr;

    return result;
}

static void set_errors(Tango::DevIntrChangeEventData &event_data, py::object dev_failed) {
    event_data.errors = dev_failed.attr("args").cast<Tango::DevErrorList>();
}

} // namespace PyDevIntrChangeEventData

void export_devintr_change_event_data(py::module &m) {
    py::class_<Tango::DevIntrChangeEventData, std::shared_ptr<Tango::DevIntrChangeEventData>>(m,
                                                                                              "DevIntrChangeEventData",
                                                                                              py::dynamic_attr(),
                                                                                              R"doc(
    This class is used to pass data to the callback method when a
    device interface changed event (:obj:`tango.EventType.INTERFACE_CHANGE_EVENT`)
    is sent to the client. It contains the
    following public fields:

        - device : (DeviceProxy) The DeviceProxy object on which the call was executed
        - event : (str) The event type name
        - event_reason : (EventReason) The reason for the event
        - device_name : (str) Tango device name
        - dev_started : (bool) True when event sent due to device being (re)started and with only
          a possible, but not certain, interface change
        - att_list : (AttributeInfoListEx) List of attribute details (only available in callback)
        - cmd_list : (CommandInfoList) List of command details (only available in callback)
        - err : (bool) A boolean flag set to true if the request failed. False
          otherwise
        - errors : (sequence<DevError>) The error stack
        - reception_date: (TimeVal)
)doc")
        .def(py::init<const Tango::DevIntrChangeEventData &>())
        .def(py::init(&PyDevIntrChangeEventData::makeDevIntrChangeEventData))
        .def_readwrite("device", &Tango::DevIntrChangeEventData::device)
        .def_readwrite("event", &Tango::DevIntrChangeEventData::event)
        .def_readwrite("event_reason", &Tango::DevIntrChangeEventData::event_reason)
        .def_readwrite("device_name", &Tango::DevIntrChangeEventData::device_name)
        .def_readwrite("dev_started", &Tango::DevIntrChangeEventData::dev_started)
        .def_readwrite("err", &Tango::DevIntrChangeEventData::err)
        .def_readwrite("reception_date", &Tango::DevIntrChangeEventData::reception_date)
        .def_property(
            "errors",
            [](Tango::DevIntrChangeEventData &self) -> Tango::DevErrorList & {
                return self.errors;
            },
            &PyDevIntrChangeEventData::set_errors)
        .def("get_date",
             &Tango::DevIntrChangeEventData::get_date,
             R"doc(
                get_date(self) -> TimeVal

                    Returns the timestamp of the event.

                :returns: the timestamp of the event
                :rtype: TimeVal)doc",
             py::return_value_policy::reference_internal);
}
