/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "client/callback.h"

namespace PyConnection {

static void command_inout_asynch_cb(py::object py_self,
                                    const std::string &cmd_name,
                                    const Tango::DeviceData &argin,
                                    py::object py_cb) {
    Tango::Connection *self = py_self.cast<Tango::Connection *>();
    PyCallBackAutoDie *cb = py_cb.cast<PyCallBackAutoDie *>();

    py::gil_scoped_release no_gil;
    try {
        self->command_inout_asynch(const_cast<std::string &>(cmd_name),
                                   const_cast<Tango::DeviceData &>(argin),
                                   *cb);
    } catch(...) {
        cb->delete_me();
        throw;
    }
}

py::str get_fqdn() {
    std::string fqdn;
    Tango::Connection::get_fqdn(fqdn);
    return py::str(fqdn.c_str());
}
} // namespace PyConnection

class PyConnectionClass : public Tango::Connection {
  public:
    /* Inherit the constructors */
    using Tango::Connection::Connection;

    /* Trampoline for dev_name method */
    std::string dev_name() override {
        PYBIND11_OVERRIDE_PURE(std::string,       /* Return type */
                               Tango::Connection, /* Parent class */
                               dev_name           /* Name of function in C++ (must match Python name) */
                               , );               // cppcheck-suppress syntaxError
    }
};

void export_connection(py::module &m) {
    py::class_<Tango::Connection,
               std::shared_ptr<Tango::Connection>,
               PyConnectionClass>(m,
                                  "Connection",
                                  "The abstract Connection class for DeviceProxy. Not to be initialized directly.")
        //        .def(py::init<>(), py::return_value_policy::take_ownership)
        .def("dev_name",
             &Tango::Connection::dev_name,
             R"doc(
                dev_name(self) -> str

                    Return the device name as it is stored locally

                    Parameters : None
                    Return     : (str))doc")

        .def("get_db_host",
             &Tango::Connection::get_db_host,
             py::return_value_policy::reference,
             R"doc(
               get_db_host(self) -> str

                        Returns a string with the database host.

                    Parameters : None
                    Return     : (str)

                    New in PyTango 7.0.0)doc")

        .def("get_db_port",
             &Tango::Connection::get_db_port,
             py::return_value_policy::copy,
             R"doc(
                get_db_port(self) -> str

                        Returns a string with the database port.

                    Parameters : None
                    Return     : (str)

                    New in PyTango 7.0.0)doc")
        .def("get_db_port_num",
             &Tango::Connection::get_db_port_num,
             R"doc(
                get_db_port_num(self) -> int

                        Returns an integer with the database port.

                    Parameters : None
                    Return     : (int)

                    New in PyTango 7.0.0)doc")
        .def("get_from_env_var",
             &Tango::Connection::get_from_env_var,
             R"doc(
                get_from_env_var(self) -> bool

                        Returns True if determined by environment variable or
                        False otherwise

                    Parameters : None
                    Return     : (bool)

                    New in PyTango 7.0.0)doc")
        .def_static("get_fqdn",
                    &PyConnection::get_fqdn,
                    R"doc(
                        get_fqdn(self) -> str

                                Returns the fully qualified domain name

                            Parameters : None
                            Return     : (str) the fully qualified domain name

                            New in PyTango 7.2.0)doc")
        .def("is_dbase_used",
             &Tango::Connection::is_dbase_used,
             R"doc(
                is_dbase_used(self) -> bool

                        Returns if the database is being used

                    Parameters : None
                    Return     : (bool) True if the database is being used

                    New in PyTango 7.2.0)doc")
        .def("get_dev_host",
             &Tango::Connection::get_dev_host,
             py::return_value_policy::copy,
             R"doc(
                get_dev_host(self) -> str

                        Returns the current host

                    Parameters : None
                    Return     : (str) the current host

                    New in PyTango 7.2.0)doc")
        .def("get_dev_port",
             &Tango::Connection::get_dev_port,
             py::return_value_policy::copy,
             R"doc(
                get_dev_port(self) -> str

                        Returns the current port

                    Parameters : None
                    Return     : (str) the current port

                    New in PyTango 7.2.0)doc")
        .def("connect",
             &Tango::Connection::connect,
             R"doc(
                connect(self, corba_name) -> None

                        Creates a connection to a TANGO device using it's stringified
                        CORBA reference i.e. IOR or corbaloc.

                    Parameters :
                        - corba_name : (str) Name of the CORBA object
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("corba_name"))
        .def("reconnect",
             &Tango::Connection::reconnect,
             R"doc(
                reconnect(self, db_used) -> None

                        Reconnecto to a CORBA object.

                    Parameters :
                        - db_used : (bool) Use thatabase
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("db_used"))
        .def("get_idl_version",
             &Tango::Connection::get_idl_version,
             R"doc(
                get_idl_version(self) -> int

                        Get the version of the Tango Device interface implemented
                        by the device

                    Parameters : None
                    Return     : (int))doc")
        .def("set_timeout_millis",
             &Tango::Connection::set_timeout_millis,
             R"doc(
                set_timeout_millis(self, timeout_ms) -> None

                        Set client side timeout for device in milliseconds. Any method
                        which takes longer than this time to execute will throw an
                        exception

                    Parameters :
                        - timeout_ms : (int) integer value of timeout in milliseconds
                    Return     : None
                    Example    :
                                dev.set_timeout_millis(1000))doc",
             py::arg("timeout_ms"))
        .def("get_timeout_millis",
             &Tango::Connection::get_timeout_millis,
             R"doc(
                get_timeout_millis(self) -> int

                        Get the client side timeout in milliseconds

                    Parameters : None
                    Return     : (int))doc")
        .def("get_source",
             &Tango::Connection::get_source,
             R"doc(
                get_source(self) -> DevSource

                        Get the data source(device, polling buffer, polling buffer
                        then device) used by command_inout or read_attribute methods

                    Parameters : None
                    Return     : (DevSource)
                    Example    :
                                source = dev.get_source()
                                if source == DevSource.CACHE_DEV : ...)doc")
        .def("set_source",
             &Tango::Connection::set_source,
             R"doc(
                set_source(self, source) -> None

                        Set the data source(device, polling buffer, polling buffer
                        then device) for command_inout and read_attribute methods.

                    Parameters :
                        - source: (DevSource) constant.
                    Return     : None
                    Example    :
                                dev.set_source(DevSource.CACHE_DEV))doc",
             py::arg("source"))
        .def("get_transparency_reconnection",
             &Tango::Connection::get_transparency_reconnection,
             R"doc(
                get_transparency_reconnection(self) -> bool

                        Returns the device transparency reconnection flag.

                    Parameters : None
                    Return     : (bool) True if transparency reconnection is set
                                        or False otherwise)doc")
        .def("set_transparency_reconnection",
             &Tango::Connection::set_transparency_reconnection,
             R"doc(
                set_transparency_reconnection(self, yesno) -> None

                        Set the device transparency reconnection flag

                    Parameters :
                        "    - val : (bool) True to set transparency reconnection
                        "                   or False otherwise
                    Return     : None)doc",
             py::arg("yesno"))
        .def("__command_inout",
             py::overload_cast<const std::string &, const Tango::DeviceData &>(&Tango::Connection::command_inout),
             py::call_guard<py::gil_scoped_release>())
        .def("__command_inout_asynch_id",
             py::overload_cast<const std::string &, const Tango::DeviceData &, bool>(
                 &Tango::Connection::command_inout_asynch),
             py::call_guard<py::gil_scoped_release>())
        .def("__command_inout_asynch_cb", &PyConnection::command_inout_asynch_cb)
        .def("command_inout_reply_raw",
             py::overload_cast<long>(&Tango::Connection::command_inout_reply),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                command_inout_reply_raw(self, id) -> DeviceData

                        Check if the answer of an asynchronous command_inout is arrived
                        (polling model). If the reply is arrived and if it is a valid
                        reply, it is returned to the caller in a DeviceData object. If
                        the reply is an exception, it is re-thrown by this call. An
                        exception is also thrown in case of the reply is not yet arrived.

                    Parameters :
                        - id      : (int) Asynchronous call identifier.
                    Return     : (DeviceData)
                    Throws     : AsynCall, AsynReplyNotArrived, CommunicationFailed, DevFailed from device)doc",
             py::arg("id"))
        .def("command_inout_reply_raw",
             py::overload_cast<long, long>(&Tango::Connection::command_inout_reply),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                command_inout_reply_raw(self, id, timeout) -> DeviceData

                        Check if the answer of an asynchronous command_inout is arrived
                        (polling model). id is the asynchronous call identifier. If the
                        reply is arrived and if it is a valid reply, it is returned to
                        the caller in a DeviceData object. If the reply is an exception,
                        it is re-thrown by this call. If the reply is not yet arrived,
                        the call will wait (blocking the process) for the time specified
                        in timeout. If after timeout milliseconds, the reply is still
                        not there, an exception is thrown. If timeout is set to 0, the
                        call waits until the reply arrived.

                    Parameters :
                        - id      : (int) Asynchronous call identifier.
                        - timeout : (int)
                    Return     : (DeviceData)
                    Throws     : AsynCall, AsynReplyNotArrived, CommunicationFailed, DevFailed from device)doc",
             py::arg("id"),
             py::arg("timeout"))

        //
        // Asynchronous methods
        //

        .def("get_asynch_replies",
             py::overload_cast<>(&Tango::Connection::get_asynch_replies),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_asynch_replies(self) -> None

                        Try to obtain data returned by a command asynchronously
                        requested. This method does not block if the reply has not yet
                        arrived. It fires callback for already arrived replies.

                    Parameters : None
                    Return     : None

                    New in PyTango 7.0.0)doc")
        .def("get_asynch_replies",
             py::overload_cast<long>(&Tango::Connection::get_asynch_replies),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_asynch_replies(self, call_timeout) -> None

                        Try to obtain data returned by a command asynchronously
                        requested. This method blocks for the specified timeout if the
                        reply is not yet arrived. This method fires callback when the
                        reply arrived. If the timeout is set to 0, the call waits
                        undefinitely for the reply

                    Parameters :
                        - call_timeout : (int) timeout in miliseconds
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("call_timeout"))
        .def("cancel_asynch_request",
             &Tango::Connection::cancel_asynch_request,
             R"doc(
                cancel_asynch_request(self, id) -> None

                        Cancel a running asynchronous request

                        This is a client side call. Obviously, the call cannot be
                        aborted while it is running in the device.

                    Parameters :
                        - id : The asynchronous call identifier
                    Return     : None

                        New in PyTango 7.0.0)doc",
             py::arg("id"))
        .def("cancel_all_polling_asynch_request",
             &Tango::Connection::cancel_all_polling_asynch_request,
             R"doc(
                cancel_all_polling_asynch_request(self) -> None

                        Cancel all running asynchronous request

                        This is a client side call. Obviously, the calls cannot be
                        aborted while it is running in the device.

                    Parameters : None
                    Return     : None

                    New in PyTango 7.0.0)doc")

        //
        // Control access related methods
        //

        .def("get_access_control",
             &Tango::Connection::get_access_control,
             R"doc(
                get_access_control(self) -> AccessControlType

                        Returns the current access control type

                    Parameters : None
                    Return     : (AccessControlType) The current access control type

                    New in PyTango 7.0.0)doc")
        .def("set_access_control",
             &Tango::Connection::set_access_control,
             R"doc(
                set_access_control(self, acc) -> None

                        Sets the current access control type

                    Parameters :
                        - acc: (AccessControlType) the type of access
                               control to set
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("acc"))
        .def("get_access_right",
             &Tango::Connection::get_access_right,
             R"doc(
                get_access_right(self) -> AccessControlType

                        Returns the current access control type

                    Parameters : None
                    Return     : (AccessControlType) The current access control type

                    New in PyTango 8.0.0)doc");
}
