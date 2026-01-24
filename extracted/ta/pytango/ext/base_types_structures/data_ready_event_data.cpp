/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

struct PyDataReadyEventData {
    static std::shared_ptr<Tango::DataReadyEventData> makeDataReadyEventData() {
        auto result = std::make_shared<Tango::DataReadyEventData>();

        // workaround https://gitlab.com/tango-controls/cppTango/-/issues/1383
        result->device = nullptr;

        return result;
    }

    static void set_errors(Tango::DataReadyEventData &event_data, py::object &dev_failed) {
        event_data.errors = dev_failed.attr("args").cast<Tango::DevErrorList>();
    }
};

void export_data_ready_event_data(py::module &m) {
    py::class_<Tango::DataReadyEventData, std::shared_ptr<Tango::DataReadyEventData>>(m,
                                                                                      "DataReadyEventData",
                                                                                      py::dynamic_attr(),
                                                                                      R"doc(
    This class is used to pass data to the callback method when an
    attribute data ready event (:obj:`tango.EventType.DATA_READY_EVENT`)
    is sent to the client. It contains the
    following public fields:

        - device : (DeviceProxy) The DeviceProxy object on which the call was executed
        - attr_name : (str) The attribute name
        - event : (str) The event type name
        - event_reason : (EventReason) The reason for the event
        - attr_data_type : (int) The attribute data type
        - ctr : (int) The user counter. Set to 0 if not defined when sent by the
          server
        - err : (bool) A boolean flag set to true if the request failed. False
          otherwise
        - errors : (sequence<DevError>) The error stack
        - reception_date: (TimeVal)

        New in PyTango 7.0.0
)doc")
        .def(py::init<const Tango::DataReadyEventData &>())
        .def(py::init(&PyDataReadyEventData::makeDataReadyEventData))
        .def_readwrite("device", &Tango::DataReadyEventData::device)
        .def_readwrite("attr_name", &Tango::DataReadyEventData::attr_name)
        .def_readwrite("event", &Tango::DataReadyEventData::event)
        .def_readwrite("event_reason", &Tango::DataReadyEventData::event_reason)
        .def_readwrite("attr_data_type", &Tango::DataReadyEventData::attr_data_type)
        .def_readwrite("ctr", &Tango::DataReadyEventData::ctr)
        .def_readwrite("err", &Tango::DataReadyEventData::err)
        .def_readwrite("reception_date", &Tango::DataReadyEventData::reception_date)
        .def_property(
            "errors",
            [](Tango::DataReadyEventData &self) -> Tango::DevErrorList & {
                return self.errors;
            },
            &PyDataReadyEventData::set_errors,
            py::return_value_policy::reference_internal)
        .def("get_date",
             &Tango::DataReadyEventData::get_date,
             R"doc(
                get_date(self) -> TimeVal

                    Returns the timestamp of the event.

                :returns: the timestamp of the event
                :rtype: TimeVal

                New in PyTango 7.0.0)doc",
             py::return_value_policy::reference_internal);
}
