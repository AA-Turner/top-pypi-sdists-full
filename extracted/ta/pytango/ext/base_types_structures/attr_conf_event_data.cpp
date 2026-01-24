/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

namespace PyAttrConfEventData {
static std::shared_ptr<Tango::AttrConfEventData> makeAttrConfEventData() {
    auto result = std::make_shared<Tango::AttrConfEventData>();

    // workaround https://gitlab.com/tango-controls/cppTango/-/issues/1383
    result->attr_conf = nullptr;
    result->device = nullptr;

    return result;
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
        - errors : (sequence<DevError>) The error stack
        - reception_date: (TimeVal)
)doc")
        .def(py::init<const Tango::AttrConfEventData &>())
        .def(py::init(&PyAttrConfEventData::makeAttrConfEventData))
        .def_readwrite("device", &Tango::AttrConfEventData::device)
        .def_readwrite("attr_name", &Tango::AttrConfEventData::attr_name)
        .def_readwrite("event", &Tango::AttrConfEventData::event)
        .def_readwrite("event_reason", &Tango::AttrConfEventData::event_reason)
        .def_readwrite("err", &Tango::AttrConfEventData::err)
        .def_readwrite("reception_date", &Tango::AttrConfEventData::reception_date)
        .def_property(
            "errors",
            [](Tango::AttrConfEventData &self) -> Tango::DevErrorList & {
                return self.errors;
            },
            &PyAttrConfEventData::set_errors,
            py::return_value_policy::reference_internal)
        .def("get_date",
             &Tango::AttrConfEventData::get_date,
             R"doc(
                get_date(self) -> TimeVal

                    Returns the timestamp of the event.

                :returns: the timestamp of the event
                :rtype: TimeVal

                New in PyTango 7.0.0)doc",
             py::return_value_policy::reference_internal);
}
