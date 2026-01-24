/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include <map>
#include "common_header.h"
#include "convertors/type_casters.h"

struct weakref_cmp {
    bool operator()(const py::weakref &lhs, const py::weakref &rhs) const {
        auto lhandle = lhs(); // Use the call operator to attempt to get a live reference
        auto rhandle = rhs(); // Same for rhs

        return lhandle.ptr() < rhandle.ptr(); // Compare the underlying PyObject* if still alive
    }
};

/// Tango expects an object for callbacks derived from Tango::CallBack.
/// For read_attribute_asynch, write_attribute_asynch, the callback object
/// should be available until the callback is run. Then it can disappear.
/// Also if we forget about a DeviceProxy we don't need the callback anymore.
/// For event subscription however, the requirements are different. The C++
/// callback can be called way after the original DeviceProxy has disappered.
/// So for this case, the callback should live forever. As we don't want it,
/// we implemented the deletion of the callback in the DeviceProxy destructor
/// itself, after performing an unsubscribe.
/// @todo this is for cmd_ended, attr_read and attr_written. push_event are not done!
class PyCallBackAutoDie : public Tango::CallBack {
  public:
    PyCallBackAutoDie(std::int64_t id) :
        my_id(id) { }

    ~PyCallBackAutoDie() override = default;

    PyTango::ExtractAs _extract_as = PyTango::ExtractAsNumpy;

    void set_extract_as(PyTango::ExtractAs extract_as) {
        this->_extract_as = extract_as;
    }

    std::int64_t my_id;
    void delete_me();

    void cmd_ended(Tango::CmdDoneEvent *ev) override;
    void attr_read(Tango::AttrReadEvent *ev) override;
    void attr_written(Tango::AttrWrittenEvent *ev) override;

    void push_event([[maybe_unused]] Tango::EventData *ev) override { }

    void push_event([[maybe_unused]] Tango::AttrConfEventData *ev) override { }

    void push_event([[maybe_unused]] Tango::DataReadyEventData *ev) override { }

    void push_event([[maybe_unused]] Tango::PipeEventData *ev) override { }

    void push_event([[maybe_unused]] Tango::DevIntrChangeEventData *ev) override { }
};

class PyEventCallBack : public Tango::CallBack {
  public:
    PyEventCallBack() { }

    ~PyEventCallBack() override = default;

    PyTango::ExtractAs _extract_as = PyTango::ExtractAsNumpy;

    void set_extract_as(PyTango::ExtractAs extract_as) {
        this->_extract_as = extract_as;
    }

    void cmd_ended([[maybe_unused]] Tango::CmdDoneEvent *ev) override { }

    void attr_read([[maybe_unused]] Tango::AttrReadEvent *ev) override { }

    void attr_written([[maybe_unused]] Tango::AttrWrittenEvent *ev) override { }

    void push_event(Tango::EventData *ev) override;
    void push_event(Tango::AttrConfEventData *ev) override;
    void push_event(Tango::DataReadyEventData *ev) override;

    void push_event([[maybe_unused]] Tango::PipeEventData *ev) override { }

    void push_event(Tango::DevIntrChangeEventData *ev) override;

    static void fill_py_event(Tango::EventData *ev,
                              py::object &py_ev,
                              PyTango::ExtractAs extract_as);
    static void fill_py_event(Tango::AttrConfEventData *ev,
                              py::object &py_ev,
                              PyTango::ExtractAs extract_as);
    static void fill_py_event(Tango::DataReadyEventData *ev,
                              py::object &py_ev,
                              PyTango::ExtractAs extract_as);
    static void fill_py_event(Tango::DevIntrChangeEventData *ev,
                              py::object &py_ev,
                              PyTango::ExtractAs extract_as);
};
