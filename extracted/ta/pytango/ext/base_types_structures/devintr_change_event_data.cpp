/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "pyutils.h"

namespace PyDevIntrChangeEventData {
static std::shared_ptr<Tango::DevIntrChangeEventData> makeDevIntrChangeEventData(py::object device_proxy,
                                                                                 py::object event_name,
                                                                                 py::object device_name,
                                                                                 py::object cmd_list,
                                                                                 py::object att_list,
                                                                                 py::object dev_started,
                                                                                 py::object event_reason,
                                                                                 py::object errors) {
    // Extract DeviceProxy pointer (nullptr if None)
    Tango::DeviceProxy *dev_ptr = device_proxy.is_none() ? nullptr : device_proxy.cast<Tango::DeviceProxy *>();

    // Extract device name (empty string if None)
    std::string device_name_str = device_name.is_none() ? "" : device_name.cast<std::string>();

    // Extract event name (empty string if None)
    std::string event_name_str = event_name.is_none() ? "" : event_name.cast<std::string>();

    // Extract CommandInfoList pointer (nullptr if None, will be filled with default)
    Tango::CommandInfoList *cmd_list_ptr = cmd_list.is_none() ? nullptr : cmd_list.cast<Tango::CommandInfoList *>();

    // Extract AttributeInfoListEx pointer (nullptr if None, will be filled with default)
    Tango::AttributeInfoListEx *att_list_ptr =
        att_list.is_none() ? nullptr : att_list.cast<Tango::AttributeInfoListEx *>();

    // Extract dev_started boolean (false if None)
    bool dev_started_bool = dev_started.is_none() ? false : dev_started.cast<bool>();

    // Extract EventReason (default to Update if None)
    Tango::EventReason reason =
        event_reason.is_none() ? Tango::EventReason::Update : event_reason.cast<Tango::EventReason>();

    // Extract DevErrorList (empty list if None)
    Tango::DevErrorList error_list = errors.is_none() ? Tango::DevErrorList{} : errors.cast<Tango::DevErrorList>();

    // Create the DevIntrChangeEventData with the extracted values
    // clang-format off
    auto result = std::make_shared<Tango::DevIntrChangeEventData>(dev_ptr,
                                                                  event_name_str,
                                                                  device_name_str,
                                                                  cmd_list_ptr,
                                                                  att_list_ptr,
                                                                  dev_started_bool,
                                                                  reason,
                                                                  error_list);
    // clang-format on
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
    - errors : (list[DevError]) The error stack
    - reception_date: (TimeVal)
)doc")
        .def(py::init<const Tango::DevIntrChangeEventData &>(), py::arg("event"))
        .def(py::init(&PyDevIntrChangeEventData::makeDevIntrChangeEventData),
             py::arg("device_proxy") = py::none(),
             py::arg("event_name") = py::none(),
             py::arg("device_name") = py::none(),
             py::arg("cmd_list") = py::none(),
             py::arg("att_list") = py::none(),
             py::arg("dev_started") = py::none(),
             py::arg("event_reason") = py::none(),
             py::arg("errors") = py::none())
        .def_readwrite("device", &Tango::DevIntrChangeEventData::device)
        .def_readwrite("event", &Tango::DevIntrChangeEventData::event)
        .def_readwrite("event_reason", &Tango::DevIntrChangeEventData::event_reason)
        .def_readwrite("device_name", &Tango::DevIntrChangeEventData::device_name)
        .def_readwrite("dev_started", &Tango::DevIntrChangeEventData::dev_started)
        .def_readwrite("err", &Tango::DevIntrChangeEventData::err)
        .def_readwrite("reception_date", &Tango::DevIntrChangeEventData::reception_date)
        .def_readwrite("cmd_list", &Tango::DevIntrChangeEventData::cmd_list)
        .def_readwrite("att_list", &Tango::DevIntrChangeEventData::att_list)
        .def_property(
            "errors",
            [](Tango::DevIntrChangeEventData &self) -> Tango::DevErrorList & { return self.errors; },
            &PyDevIntrChangeEventData::set_errors)
        .def("get_date",
             &Tango::DevIntrChangeEventData::get_date,
             R"doc(
                Returns the timestamp of the event.
             )doc",
             py::return_value_policy::reference_internal);
    fix_dynamic_attr_dealloc<Tango::DevIntrChangeEventData>();
}
