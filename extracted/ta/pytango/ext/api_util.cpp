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
    py::class_<Tango::ApiUtil, std::unique_ptr<Tango::ApiUtil, py::nodelete>>(m,
                                                                              "ApiUtil",
                                                                              R"doc(
                                    This class allows you to access the tango synchronization model API.
                                    It is designed as a singleton. To get a reference to the singleton object
                                    you must do::

                                        import tango
                                        api_util = tango.ApiUtil.instance()

                                    .. versionadded:: 7.1.3
                               )doc")

        .def_static("instance",
                    &Tango::ApiUtil::instance,
                    py::return_value_policy::reference,
                    R"doc(
                        Returns the ApiUtil singleton instance.

                        .. versionadded:: 7.1.3
                    )doc")

        .def("pending_asynch_call",
             &Tango::ApiUtil::pending_asynch_call,
             R"doc(
                Return the number of asynchronous pending requests (any device) for the given type.
                The input parameter is an enumeration with three values:
                - POLLING
                - CALL_BACK
                - ALL_ASYNCH

                :param req: asynchronous request type
                :type req: :obj:`~tango.asyn_req_type`

                .. versionadded:: 7.1.3
             )doc",
             py::arg("req"))

        .def("get_asynch_replies",
             py::overload_cast<>(&Tango::ApiUtil::get_asynch_replies),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                Fire callback methods for all asynchronous requests (command and attribute)
                which already have arrived replies. Returns immediately if no replies arrived
                or there are no asynchronous requests.

                :throws: None, all errors are reported via the callback's err/errors fields.

                .. versionadded:: 7.1.3
             )doc")
        .def("get_asynch_replies",
             py::overload_cast<long>(&Tango::ApiUtil::get_asynch_replies),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                Fire callback methods for all asynchronous requests (command and attributes)
                with already arrived replies. Wait up to `timeout` milliseconds if some replies
                haven't arrived yet. If timeout=0, waits until all requests receive a reply.

                :param timeout: timeout in milliseconds
                :type timeout: int

                :throws: :obj:`~tango.AsynReplyNotArrived` if some replies did not arrive in time.
                         Other errors are reported via the callback's err/errors fields.

                .. versionadded:: 7.1.3
                )doc",
             py::arg("timeout"))

        .def("set_asynch_cb_sub_model",
             &Tango::ApiUtil::set_asynch_cb_sub_model,
             R"doc(
                Set the asynchronous callback sub-model between PULL_CALLBACK or PUSH_CALLBACK.

                :param model: the callback sub-model
                :type model: :obj:`~tango.cb_sub_model`

                .. versionadded:: 7.1.3
             )doc",
             py::arg("model"))
        .def("get_asynch_cb_sub_model",
             &Tango::ApiUtil::get_asynch_cb_sub_model,
             R"doc(
                Get the asynchronous callback sub-model.

                .. versionadded:: 7.1.3
             )doc")

        .def_static("get_env_var",
                    &PyApiUtil::get_env_var,
                    R"doc(
                        Return the environment variable value for the given name.

                        :param name: Environment variable name
                        :type name: :py:obj:`str`\

                    )doc",
                    py::arg("name"))
        .def("is_notifd_event_consumer_created",
             &Tango::ApiUtil::is_notifd_event_consumer_created,
             R"doc(
                Check if the notifd event consumer was created.
             )doc")
        .def("is_zmq_event_consumer_created",
             &Tango::ApiUtil::is_zmq_event_consumer_created,
             R"doc(
                Check if the ZMQ event consumer was created.
             )doc")
        .def("get_user_connect_timeout",
             &Tango::ApiUtil::get_user_connect_timeout,
             R"doc(
                Get the user connect timeout (in milliseconds).
             )doc")
        .def("in_server",
             static_cast<bool (Tango::ApiUtil::*)()>(&Tango::ApiUtil::in_server),
             R"doc(
                Returns True if the current process is running a Tango device server.

                .. versionadded:: 10.0.0
             )doc")
        .def("get_ip_from_if",
             &Tango::ApiUtil::get_ip_from_if,
             R"doc(
                Get the IP address for the given network interface name.

                :param interface_name: The name of the network interface
                :type interface_name: :py:obj:`str`
             )doc",
             py::arg("interface_name"))
        .def_static("cleanup",
                    &Tango::ApiUtil::cleanup,
                    R"doc(
                        Destroy the ApiUtil singleton instance.
                        After calling cleanup(), any existing DeviceProxy, AttributeProxy,
                        or Database objects become invalid and must be reconstructed.

                        .. versionadded:: 9.3.0
                    )doc")
        .def("query_event_system",
             &Tango::ApiUtil::query_event_system,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                Returns info about both sides of event system in current process:
                server supplier (if running) and proxy consumer

                This feature is described in the cppTango docs:
                https://tango-controls.gitlab.io/cppTango/10.1.0/query_event_system.html

                See also :py:meth:`~tango.ApiUtil.enable_event_system_perf_mon`

                :return: Json dump of event system info

                .. versionadded:: 10.3.0
             )doc")
        .def("enable_event_system_perf_mon",
             &Tango::ApiUtil::enable_event_system_perf_mon,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                Enables/disables event system performance counter for server supplier (if running)
                and proxy consumer in current process

                See also :py:meth:`~tango.ApiUtil.query_event_system`

                :param flag: new state of system performance counter
                :type flag: :py:obj:`bool`

                .. versionadded:: 10.3.0

                .. warning:: Enabled monitoring has a small performance penalty for the event system.
             )doc",
             py::arg("flag"));
}
