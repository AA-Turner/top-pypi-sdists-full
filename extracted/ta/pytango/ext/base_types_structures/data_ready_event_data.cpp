/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "pyutils.h"

namespace PyDataReadyEventData {
static std::shared_ptr<Tango::DataReadyEventData> makeDataReadyEventData(py::object device_proxy,
                                                                         py::object att_data_ready,
                                                                         py::object event_name,
                                                                         py::object event_reason,
                                                                         py::object errors) {
    // Extract DeviceProxy pointer (nullptr if None)
    Tango::DeviceProxy *dev_ptr = device_proxy.is_none() ? nullptr : device_proxy.cast<Tango::DeviceProxy *>();

    // Extract AttDataReady pointer (nullptr if None)
    Tango::AttDataReady *att_data_ptr =
        att_data_ready.is_none() ? nullptr : att_data_ready.cast<Tango::AttDataReady *>();

    // Extract event name (empty string if None)
    std::string event_name_str = event_name.is_none() ? "" : event_name.cast<std::string>();

    // Extract EventReason (default to Update if None)
    Tango::EventReason reason =
        event_reason.is_none() ? Tango::EventReason::Update : event_reason.cast<Tango::EventReason>();

    // Extract DevErrorList (empty list if None)
    Tango::DevErrorList error_list = errors.is_none() ? Tango::DevErrorList{} : errors.cast<Tango::DevErrorList>();

    // Create the DataReadyEventData with the extracted values
    return std::make_shared<Tango::DataReadyEventData>(dev_ptr, att_data_ptr, event_name_str, reason, error_list);
}

static void set_errors(Tango::DataReadyEventData &event_data, py::object &dev_failed) {
    event_data.errors = dev_failed.attr("args").cast<Tango::DevErrorList>();
}
} // namespace PyDataReadyEventData

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
    - errors : (list[DevError]) The error stack
    - reception_date: (TimeVal)

    .. versionadded:: 7.0.0
)doc")
        .def(py::init<const Tango::DataReadyEventData &>(), py::arg("event"))
        .def(py::init(&PyDataReadyEventData::makeDataReadyEventData),
             py::arg("device_proxy") = py::none(),
             py::arg("att_data_ready") = py::none(),
             py::arg("event_name") = py::none(),
             py::arg("event_reason") = py::none(),
             py::arg("errors") = py::none())
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
            [](Tango::DataReadyEventData &self) -> Tango::DevErrorList & { return self.errors; },
            &PyDataReadyEventData::set_errors,
            py::return_value_policy::reference_internal)
        .def("get_date",
             &Tango::DataReadyEventData::get_date,
             R"doc(
                Returns the timestamp of the event.
             )doc",
             py::return_value_policy::reference_internal);
    fix_dynamic_attr_dealloc<Tango::DataReadyEventData>();
}
