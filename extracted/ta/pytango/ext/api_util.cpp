/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

namespace PyApiUtil {
inline py::object get_env_var(const char *name) {
    std::string value;
    if(Tango::ApiUtil::get_env_var(name, value) == 0) {
        return py::str(value);
    }
    return py::none();
}
} // namespace PyApiUtil

void export_api_util(py::module_ &m) {
    py::class_<Tango::ApiUtil,
               std::unique_ptr<Tango::ApiUtil,
                               py::nodelete>>(m,
                                              "ApiUtil",
                                              R"doc(
                                    This class allows you to access the tango synchronization model API.
                                    It is designed as a singleton. To get a reference to the singleton object
                                    you must do:

                                        import tango
                                        apiutil = tango.ApiUtil.instance()

                                    New in PyTango 7.1.3
                                    )doc")

        .def_static("instance",
                    &Tango::ApiUtil::instance,
                    py::return_value_policy::reference,
                    R"doc(
                    instance() -> ApiUtil

                        Returns the ApiUtil singleton instance.

                    :return: (ApiUtil) a reference to the ApiUtil singleton object.

                    New in PyTango 7.1.3
                    )doc")

        .def("pending_asynch_call",
             &Tango::ApiUtil::pending_asynch_call,
             R"doc(
                pending_asynch_call(self, req) -> int

                    Return the number of asynchronous pending requests (any device).
                    The input parameter is an enumeration with three values:
                    - POLLING
                    - CALL_BACK
                    - ALL_ASYNCH

                :param req: asynchronous request type
                :type req: asyn_req_type
                :return: the number of pending requests for the given type
                :rtype: int

                New in PyTango 7.1.3
                )doc",
             py::arg("req"))

        .def("get_asynch_replies",
             py::overload_cast<>(&Tango::ApiUtil::get_asynch_replies),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_asynch_replies(self) -> None

                    Fire callback methods for all asynchronous requests (command and attribute)
                    which already have arrived replies. Returns immediately if no replies arrived
                    or there are no asynchronous requests.

                :return: None

                Throws: None, all errors are reported via the callback's err/errors fields.

                New in PyTango 7.1.3
                )doc")
        .def("get_asynch_replies",
             py::overload_cast<long>(&Tango::ApiUtil::get_asynch_replies),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_asynch_replies(self, timeout: int) -> None

                    Fire callback methods for all asynchronous requests (command and attributes)
                    with already arrived replies. Wait up to `timeout` milliseconds if some replies
                    haven't arrived yet. If timeout=0, waits until all requests receive a reply.

                :param timeout: timeout in milliseconds
                :type timeout: int
                :return: None

                Throws: AsynReplyNotArrived if some replies did not arrive in time.
                        Other errors are reported via the callback's err/errors fields.

                New in PyTango 7.1.3
                )doc",
             py::arg("timeout"))

        .def("set_asynch_cb_sub_model",
             &Tango::ApiUtil::set_asynch_cb_sub_model,
             R"doc(
                set_asynch_cb_sub_model(self, model) -> None

                    Set the asynchronous callback sub-model between PULL_CALLBACK or PUSH_CALLBACK.

                :param model: the callback sub-model
                :type model: cb_sub_model
                :return: None

                New in PyTango 7.1.3
                )doc",
             py::arg("model"))
        .def("get_asynch_cb_sub_model",
             &Tango::ApiUtil::get_asynch_cb_sub_model,
             R"doc(
                get_asynch_cb_sub_model(self) -> cb_sub_model

                    Get the asynchronous callback sub-model.

                :return: the active asynchronous callback sub-model
                :rtype: cb_sub_model

                New in PyTango 7.1.3
                )doc")

        .def_static("get_env_var",
                    &PyApiUtil::get_env_var,
                    R"doc(
                        get_env_var(name) -> str

                            Return the environment variable for the given name.

                        :param name: Environment variable name
                        :type name: str

                        :return: The value of the environment variable
                        :rtype: str
                        )doc",
                    py::arg("name"))
        .def("is_notifd_event_consumer_created",
             &Tango::ApiUtil::is_notifd_event_consumer_created,
             R"doc(
                is_notifd_event_consumer_created(self) -> bool

                    Check if the notifd event consumer was created.

                :return: True if created, False otherwise
                :rtype: bool
                )doc")
        .def("is_zmq_event_consumer_created",
             &Tango::ApiUtil::is_zmq_event_consumer_created,
             R"doc(
                is_zmq_event_consumer_created(self) -> bool

                    Check if the ZMQ event consumer was created.

                :return: True if created, False otherwise
                :rtype: bool
                )doc")
        .def("get_user_connect_timeout",
             &Tango::ApiUtil::get_user_connect_timeout,
             R"doc(
                get_user_connect_timeout(self) -> int

                    Get the user connect timeout (in milliseconds).

                :return: The timeout in milliseconds
                :rtype: int
                )doc")
        .def("in_server",
             static_cast<bool (Tango::ApiUtil::*)()>(&Tango::ApiUtil::in_server),
             R"doc(
                in_server() -> bool

                    Returns True if the current process is running a Tango device server.

                :return: True if running in a server, otherwise False
                :rtype: bool

                .. versionadded:: 10.0.0
                )doc")
        .def("get_ip_from_if",
             &Tango::ApiUtil::get_ip_from_if,
             R"doc(
                 get_ip_from_if(self, interface_name: str) -> str

                    Get the IP address for the given network interface name.

                 :param interface_name: The name of the network interface
                 :type interface_name: str

                 :return: IP address associated to that interface
                 :rtype: str
                 )doc",
             py::arg("interface_name"))
        .def_static("cleanup",
                    &Tango::ApiUtil::cleanup,
                    R"doc(
                        cleanup() -> None

                        Destroy the ApiUtil singleton instance.
                        After calling cleanup(), any existing DeviceProxy, AttributeProxy,
                        or Database objects become invalid and must be reconstructed.

                    :return: None

                    New in PyTango 9.3.0
                    )doc");
}
