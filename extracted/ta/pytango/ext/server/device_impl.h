/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#ifndef _DEVICE_IMPL_H
#define _DEVICE_IMPL_H

#include "common_header.h"
#include "function_call_macros.h"
#include "base_types_structures/exception.h"
#include "server/device_class.h"

class DeviceImplTrampoline : public Tango::DeviceImpl {
  public:
    // Inherit constructors from Tango::DeviceImpl
    using Tango::DeviceImpl::DeviceImpl;

    void init_device() override {
        PYBIND11_OVERRIDE_PURE(
            void,
            Tango::DeviceImpl,
            init_device, ); // cppcheck-suppress syntaxError
    }

    bool is_attribute_polled_public(const std::string &att_name) {
        return is_attribute_polled(att_name);
    }

    bool is_command_polled_public(const std::string &cmd_name) {
        return is_command_polled(cmd_name);
    }

    int get_attribute_poll_period_public(const std::string &att_name) {
        return get_attribute_poll_period(att_name);
    }

    int get_command_poll_period_public(const std::string &cmd_name) {
        return get_command_poll_period(cmd_name);
    }

    void poll_attribute_public(const std::string &att_name, int period) {
        poll_attribute(att_name, period);
    }

    void poll_command_public(const std::string &cmd_name, int period) {
        poll_command(cmd_name, period);
    }

    void stop_poll_attribute_public(const std::string &att_name) {
        stop_poll_attribute(att_name);
    }

    void stop_poll_command_public(const std::string &cmd_name) {
        stop_poll_command(cmd_name);
    }
};

// Trampoline class inheriting from Tango::DeviceImpl
class Device_2ImplTrampoline : public Tango::Device_2Impl {
  public:
    // Inherit constructors from Tango::DeviceImpl
    using Tango::Device_2Impl::Device_2Impl;

    void init_device() override {
        PYBIND11_OVERRIDE_PURE(
            void,
            Tango::Device_2Impl,
            init_device, );
    }
};

/**
 * A wrapper around the Tango::Device_XImpl class
 */
template <typename TangoDeviceImpl>
class Device_XImplTrampoline : public TangoDeviceImpl {
  public:
    Device_XImplTrampoline(Tango::DeviceClass *cl, std::string &st) :
        TangoDeviceImpl(cl, st) {
    }

    Device_XImplTrampoline(Tango::DeviceClass *cl,
                           const char *name,
                           const char *_desc = "A Tango device",
                           Tango::DevState sta = Tango::UNKNOWN,
                           const char *status = Tango::StatusNotSet) :
        TangoDeviceImpl(cl, name, _desc, sta, status) {
    }

    std::string the_status;

    ~Device_XImplTrampoline() override {
        // destructor must be non-throwing, while delete_device can throw:
        try {
            delete_device();
        } catch(const Tango::DevFailed &e) {
            Tango::ApiUtil *au = Tango::ApiUtil::instance();
            std::stringstream ss;
            ss << "delete_device() raised a DevFailed exception: \n\n";
            ss << e.errors[0].desc;
            au->print_error_message(ss.str().c_str());
        }
    }

    void init_device() override {
        PYBIND11_OVERRIDE_PURE(
            void,            // Return type
            TangoDeviceImpl, // Parent class
            init_device      // Name of the method in C++
            , );
    }

    void server_init_hook() override {
        CALL_VOID_METHOD(server_init_hook,
                         TangoDeviceImpl, )
    }

    void delete_device() override {
        CALL_VOID_METHOD(delete_device,
                         TangoDeviceImpl, )
    }

    void always_executed_hook() override {
        CALL_VOID_METHOD(always_executed_hook,
                         TangoDeviceImpl, )
    }

    void read_attr_hardware(std::vector<long> &attr_list) override {
        CALL_VOID_METHOD(read_attr_hardware,
                         TangoDeviceImpl,
                         attr_list)
    }

    void write_attr_hardware(std::vector<long> &attr_list) override{
        CALL_VOID_METHOD(write_attr_hardware,
                         TangoDeviceImpl,
                         attr_list)}

    Tango::DevState dev_state() override{
        CALL_RETURN_METHOD(Tango::DevState,
                           dev_state,
                           TangoDeviceImpl, )}

    Tango::ConstDevString dev_status() override {
        //  cppTango layer the caller of dev_status does not own the returned memory, so it is our duty
        GET_PYTHON_METHOD(dev_status)
        if(py_method) {
            try {
                this->the_status = py::cast<const std::string>(py_method());
            }
            CATCH_PY_EXCEPTION
        } else {
            this->the_status = TangoDeviceImpl::dev_status();
        };
        return this->the_status.c_str();
    }

    void signal_handler(long signo) override {
        try {
            CALL_VOID_METHOD(signal_handler,
                             TangoDeviceImpl,
                             signo)
        } catch(Tango::DevFailed &df) {
            unsigned int nb_err = df.errors.length();
            df.errors.length(nb_err + 1);

            df.errors[nb_err].reason = CORBA::string_dup("PyDs_UnmanagedSignalHandlerException");
            df.errors[nb_err].desc =
                CORBA::string_dup("An unmanaged Tango::DevFailed exception occurred in signal_handler");

            TangoSys_OMemStream origin;
            origin << TANGO_EXCEPTION_ORIGIN << std::ends;

            df.errors[nb_err].origin = CORBA::string_dup(origin.str().c_str());
            df.errors[nb_err].severity = Tango::ERR;

            Tango::Except::print_exception(df);
        }
    }
};

#endif // _DEVICE_IMPL_H
