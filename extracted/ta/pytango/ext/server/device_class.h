/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "function_call_macros.h"
#include "convertors/vector_wrappers.h"

class DeviceClassTrampoline : public Tango::DeviceClass {
  public:
    DeviceClassTrampoline(const std::string &new_name) :
        Tango::DeviceClass(const_cast<std::string &>(new_name)) { }

    ~DeviceClassTrampoline() override = default;

    /**
     * Export a device.
     * Associate the servant to a CORBA object and send device network parameter
     * to TANGO database.
     * The main parameter sent to database is the CORBA object stringified device IOR.
     *
     * @param[in] dev The device to be exported (CORBA servant)
     * @param[in] corba_dev_name The name to be used in the CORBA object key.
     *                           This parameter does not need to be set in most of
     *                           cases and has a default value. It is used for special
     *                           device server like the database device server.
     */
    void export_device(Tango::DeviceImpl *dev, const char *corba_dev_nam = "Unused") {
        Tango::DeviceClass::export_device(dev, corba_dev_nam);
    }

    /**
     * Creates an attribute and adds it to the att_list.
     * This method is intended to be called by python to register a new
     * attribute.
     */
    void create_attribute(std::vector<Tango::Attr *> &att_list,
                          const std::string &attr_name,
                          Tango::CmdArgType attr_type,
                          Tango::AttrDataFormat attr_format,
                          Tango::AttrWriteType attr_write,
                          long dim_x,
                          long dim_y,
                          Tango::DispLevel display_level,
                          long polling_period,
                          bool memorized,
                          bool hw_memorized,
                          bool alarm_event_implemented,
                          bool alarm_event_detect,
                          bool archive_event_implemented,
                          bool archive_event_detect,
                          bool change_event_implemented,
                          bool change_event_detect,
                          bool data_ready_event_implemented,
                          const std::string &read_method_name,
                          const std::string &write_method_name,
                          const std::string &is_allowed_name,
                          Tango::UserDefaultAttrProp *att_prop);

    void create_fwd_attribute(std::vector<Tango::Attr *> &att_list,
                              const std::string &attr_name,
                              Tango::UserDefaultFwdAttrProp *att_prop);

    /**
     * Creates a command.
     * This method is intended to be called by python to register a new
     * command.
     */
    void create_command(const std::string &cmd_name,
                        Tango::CmdArgType param_type,
                        Tango::CmdArgType result_type,
                        const std::string &param_desc,
                        const std::string &result_desc,
                        Tango::DispLevel display_level,
                        bool default_command,
                        long polling_period,
                        const std::string &is_allowed);

    /**
     * This method forward a C++ call to the device_factory method to the
     * Python method
     *
     * @param[in] dev_list The device name list
     */
    void device_factory(const Tango::DevVarStringArray *dev_list) override {
        CALL_PURE_VOID_METHOD(device_factory,
                              dev_list);
    }

    /**
     * This method forward a C++ call to the attribute_factory method to the
     * Python method
     *
     * @param[in] att_list attribute list
     *
     * Note! Due to pybind11 does not allow to bind vectors of raw pointers in a way,
     * that they will be directly manipulated in Python.
     * We do here some trick, and sending to python not a list but a wrapper.
     * However, functionally in Python is not guaranteed!
     */

    void attribute_factory(std::vector<Tango::Attr *> &att_list) override {
        py::gil_scoped_acquire gil; // Ensure GIL is acquired
        py::function override = py::get_override(this, "_attribute_factory");
        if(override) {
            try {
                auto py_attr_list = std::make_shared<VectorWrapper<Tango::Attr>>(&att_list);
                override(py_attr_list);
                attr_vector_wrapper = py_attr_list;
            }
            CATCH_PY_EXCEPTION
        } else {
            Tango::DeviceClass::attribute_factory(att_list);
        }
    }

    /**
     * This method forward a C++ call to the pipe_factory method to the
     * Python method
     *
     * @param[in] pipe_list pipe list
     */
    void pipe_factory() override { }

    /**
     * This method forward a C++ call to the command_factory method to the
     * Python method
     */
    void command_factory() override {
        CALL_PURE_VOID_METHOD(_command_factory, );
    }

    /**
     * This method forward a C++ call to the device_name_factory method to the
     * Python method
     */
    void device_name_factory(StdStringVector &dev_list) override {
        CALL_VOID_METHOD(device_name_factory,
                         Tango::DeviceClass,
                         dev_list)
    }

    /**
     * This method forward a C++ call to the signal_handler method to the
     * Python method or executes default signal handler if no signal handler
     * is defined in python
     *
     * @param[in] signo signal identifier
     */
    void signal_handler(long signo) override {
        CALL_VOID_METHOD(signal_handler,
                         Tango::DeviceClass,
                         signo)
    }

  private:
    /* Keep the wrappers alive
     *
     * NOTE: We do it to provide opportunity of manipulating these cpp vectors from Python code
     * However, this is a potential source of both SEGFAULTS and memory leaks simultaneously....
     */

    std::shared_ptr<VectorWrapper<Tango::Attr>> attr_vector_wrapper;
};
