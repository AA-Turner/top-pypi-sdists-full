/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "function_call_macros.h"

#include "convertors/type_casters.h"

#include "client/callback.h"
#include "client/device_attribute.h"
#include "client/device_data.h"
#include "base_types_structures/exception.h"

// Wrapper classes to expose cppTango events to Python and manage their lifetime
class CmdDoneEventWrapper {
  public:
    CmdDoneEventWrapper(const Tango::CmdDoneEvent &original, PyTango::ExtractAs extract_as) :
        device(original.device),
        cmd_name(original.cmd_name),
        argout(original.argout),
        err(original.err),
        errors(original.errors),
        _extract_as(extract_as) { }

    Tango::DeviceProxy *device;
    std::string cmd_name;
    Tango::DeviceData argout;
    bool err;
    Tango::DevErrorList errors;
    PyTango::ExtractAs _extract_as;

    py::object get_converted_argout() const {
        py::object py_data = py::cast(argout);
        return PyDeviceData::extract(py_data, _extract_as);
    }
};

class AttrReadEventWrapper {
  public:
    AttrReadEventWrapper(const Tango::AttrReadEvent &original, PyTango::ExtractAs extract_as) :
        device(original.device),
        attr_names(original.attr_names),
        err(original.err),
        errors(original.errors),
        _extract_as(extract_as) {
        if(original.argout != nullptr) {
            argout = *original.argout;
        }
    }

    Tango::DeviceProxy *device;
    std::vector<std::string> attr_names;
    std::vector<Tango::DeviceAttribute> argout;
    bool err;
    Tango::DevErrorList errors;
    PyTango::ExtractAs _extract_as;

    py::object get_converted_argout() const {
        auto argout_unique_ptr = std::make_unique<std::vector<Tango::DeviceAttribute>>(argout);
        return PyDeviceAttribute::convert_to_python(argout_unique_ptr, *device, _extract_as);
    }
};

class AttrWrittenEventWrapper {
  public:
    AttrWrittenEventWrapper(const Tango::AttrWrittenEvent &original, [[maybe_unused]] PyTango::ExtractAs extract_as) :
        device(original.device),
        attr_names(original.attr_names),
        err(original.err),
        errors(original.errors) { }

    Tango::DeviceProxy *device;
    std::vector<std::string> attr_names;
    bool err;
    Tango::NamedDevFailedList errors;
};

template <typename OriginalT, typename CopyT>
static void _run_virtual_once(PyCallBackAutoDie *_self, OriginalT *ev, const char *virt_fn_name) {
    if(!Py_IsInitialized()) {
        TANGO_LOG_DEBUG << "Tango event received after python shutdown. "
                        << "Event will be ignored" << std::endl;
        return;
    }

    auto ev_copy = std::make_shared<CopyT>(*ev, _self->_extract_as);
    py::gil_scoped_acquire gil;
    py::function override = py::get_override(_self, virt_fn_name);

    if(override) // method is found
    {
        try {
            override(ev_copy); // Call the Python function.
        } catch(py::error_already_set &eas) {
            _self->delete_me();
            handle_python_exception(eas);
        }
    }
    _self->delete_me();
}

void PyCallBackAutoDie::delete_me() {
    py::module_ tango_utils = py::module_::import("tango.utils");
    py::object release_callback = tango_utils.attr("_release_CallbackAutoDie");
    release_callback(my_id);
}

/*helper method*/ void PyCallBackAutoDie::cmd_ended(Tango::CmdDoneEvent *ev) {
    _run_virtual_once<Tango::CmdDoneEvent, CmdDoneEventWrapper>(this, ev, "cmd_ended");
}

/*helper method*/ void PyCallBackAutoDie::attr_read(Tango::AttrReadEvent *ev) {
    _run_virtual_once<Tango::AttrReadEvent, AttrReadEventWrapper>(this, ev, "attr_read");
}

/*helper method*/ void PyCallBackAutoDie::attr_written(Tango::AttrWrittenEvent *ev) {
    _run_virtual_once<Tango::AttrWrittenEvent, AttrWrittenEventWrapper>(this, ev, "attr_written");
}

template <typename OriginalT>
static void _push_event(PyEventCallBack *self, OriginalT *ev) {
    // If the event is received after python dies but before the process
    // finishes then discard the event
    if(!Py_IsInitialized()) {
        TANGO_LOG_DEBUG << "Tango event (" << ev->event << ") received after python shutdown. "
                        << "Event will be ignored" << std::endl;
        return;
    }

    py::gil_scoped_acquire method_gil;

    // Make a copy of ev in python
    // (the original will be deleted by TangoC++ on return)
    auto ev_copy = new OriginalT(*ev);
    py::object py_ev = py::cast(ev_copy, py::return_value_policy::take_ownership);

    PyEventCallBack::fill_py_event(ev_copy, py_ev, self->_extract_as);

    py::function override = py::get_override(self, "push_event");

    if(override) // method is found
    {
        override(py_ev); // Call the Python function.
    }
}

/*helper method*/ void PyEventCallBack::push_event(Tango::EventData *ev) {
    _push_event<Tango::EventData>(this, ev);
}

/*helper method*/ void PyEventCallBack::push_event(Tango::AttrConfEventData *ev) {
    _push_event<Tango::AttrConfEventData>(this, ev);
}

/*helper method*/ void PyEventCallBack::push_event(Tango::DataReadyEventData *ev) {
    _push_event<Tango::DataReadyEventData>(this, ev);
}

/*helper method*/ void PyEventCallBack::push_event(Tango::DevIntrChangeEventData *ev) {
    _push_event<Tango::DevIntrChangeEventData>(this, ev);
}

void PyEventCallBack::fill_py_event(Tango::EventData *ev,
                                    py::object &py_ev,
                                    PyTango::ExtractAs extract_as) {
    // @todo on error extracting, we could save the error in DeviceData
    // instead of throwing it...?

    // Save a copy of attr_value, so we can still access it after
    // the execution of the callback (Tango will delete the original!)
    // I originally was 'stealing' the reference to TangoC++: I got
    // attr_value and set it to 0... But now TangoC++ is not deleting
    // attr_value pointer but its own copy, so my efforts are useless.

    if(ev->attr_value != nullptr) {
        auto *attr = new Tango::DeviceAttribute;
        (*attr) = std::move(*ev->attr_value);
        py_ev.attr("attr_value") = PyDeviceAttribute::convert_to_python(attr, *ev->device, extract_as);
    }
}

void PyEventCallBack::fill_py_event(Tango::AttrConfEventData *ev,
                                    py::object &py_ev,
                                    [[maybe_unused]] PyTango::ExtractAs extract_as) {
    if(ev->attr_conf != nullptr) {
        py_ev.attr("attr_conf") = *ev->attr_conf;
    }
}

void PyEventCallBack::fill_py_event([[maybe_unused]] Tango::DataReadyEventData *ev,
                                    [[maybe_unused]] py::object &py_ev,
                                    [[maybe_unused]] PyTango::ExtractAs extract_as) {
}

void PyEventCallBack::fill_py_event(Tango::DevIntrChangeEventData *ev,
                                    py::object &py_ev,
                                    [[maybe_unused]] PyTango::ExtractAs extract_as) {
    py_ev.attr("cmd_list") = ev->cmd_list;
    py_ev.attr("att_list") = ev->att_list;
}

void export_callback(py::module &m) {
    py::class_<CmdDoneEventWrapper,
               std::shared_ptr<CmdDoneEventWrapper>>(m,
                                                     "CmdDoneEvent",
                                                     R"doc(
                This class is used to pass data to the callback method in
                asynchronous callback model for command execution.)doc")
        .def_readonly("device",
                      &CmdDoneEventWrapper::device,
                      "(DeviceProxy) The DeviceProxy object on which the call was executed.")
        .def_readonly("cmd_name",
                      &CmdDoneEventWrapper::cmd_name,
                      "(str) The command name")
        .def_property_readonly("argout",
                               &CmdDoneEventWrapper::get_converted_argout,
                               "The command argout")
        .def_readonly("err",
                      &CmdDoneEventWrapper::err,
                      "(bool) A boolean flag set to true if the command failed. False otherwise")
        .def_readonly("errors",
                      &CmdDoneEventWrapper::errors,
                      "(sequence<DevError>) The error stack");

    py::class_<AttrReadEventWrapper,
               std::shared_ptr<AttrReadEventWrapper>>(m,
                                                      "AttrReadEvent",
                                                      R"doc()doc")
        .def_readonly("device",
                      &AttrReadEventWrapper::device,
                      "(DeviceProxy) The DeviceProxy object on which the call was executed")
        .def_readonly("attr_names",
                      &AttrReadEventWrapper::attr_names,
                      "(sequence<str>) The attribute name list")
        .def_property_readonly("argout",
                               &AttrReadEventWrapper::get_converted_argout,
                               "(DeviceAttribute) The attribute value")
        .def_readonly("err",
                      &AttrReadEventWrapper::err,
                      "(bool) A boolean flag set to true if the command failed. False otherwise")
        .def_readonly("errors",
                      &AttrReadEventWrapper::errors,
                      "(sequence<DevError>) The error stack");

    py::class_<AttrWrittenEventWrapper,
               std::shared_ptr<AttrWrittenEventWrapper>>(m,
                                                         "AttrWrittenEvent",
                                                         R"doc()doc")
        .def_readonly("device",
                      &AttrWrittenEventWrapper::device,
                      "(DeviceProxy) The DeviceProxy object on which the call was executed")
        .def_readonly("attr_names",
                      &AttrWrittenEventWrapper::attr_names,
                      "(sequence<str>) The attribute name list")
        .def_readonly("err",
                      &AttrWrittenEventWrapper::err,
                      "(bool) A boolean flag set to true if the command failed. False otherwise")
        .def_readonly("errors",
                      &AttrWrittenEventWrapper::errors,
                      "(sequence<DevError>) The error stack");

    py::class_<PyCallBackAutoDie>(m, "__CallBackAutoDie", "INTERNAL CLASS - DO NOT USE IT", py::dynamic_attr())
        .def(py::init<std::int64_t>())
        .def("cmd_ended", &Tango::CallBack::cmd_ended)
        .def("attr_read", &Tango::CallBack::attr_read)
        .def("attr_written", &Tango::CallBack::attr_written);

    py::class_<PyEventCallBack>(m, "__EventCallBack", "INTERNAL CLASS - DO NOT USE IT", py::dynamic_attr())
        .def(py::init<>())
        .def("push_event", py::overload_cast<Tango::EventData *>(&Tango::CallBack::push_event))
        .def("push_event", py::overload_cast<Tango::AttrConfEventData *>(&Tango::CallBack::push_event))
        .def("push_event", py::overload_cast<Tango::DataReadyEventData *>(&Tango::CallBack::push_event))
        .def("push_event", py::overload_cast<Tango::DevIntrChangeEventData *>(&Tango::CallBack::push_event));
}
