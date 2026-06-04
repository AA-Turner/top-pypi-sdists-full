/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_dserver(py::module &m) {
    py::class_<Tango::DServer, LeakingSmartPtr<Tango::DServer>, Tango::Device_6Impl>(m, "DServer")
        .def("query_class",
             &Tango::DServer::query_class,
             R"doc(
                Command to read all the classes used in a device server process
             )doc")
        .def("query_device",
             &Tango::DServer::query_device,
             R"doc(
                Command to read all the devices implemented by a device server process
             )doc")
        .def("query_sub_device",
             &Tango::DServer::query_sub_device,
             R"doc(
                Command to read all the sub devices used by a device server process
             )doc")
        .def("kill",
             &Tango::DServer::kill,
             R"doc(
                Command to kill the device server process. This is done by starting a thread which will kill the process.
                Starting a thread allows the client to receive something from the server before it is killed
             )doc")
        .def("restart",
             py::overload_cast<const std::string &>(&Tango::DServer::restart),
             R"doc(
                Command to restart a device

                :param d_name: The device name to be re-started
                :type d_name: :py:obj:`str`
             )doc",
             py::arg("d_name"))
        .def("restart_server",
             &Tango::DServer::restart_server,
             R"doc(
                Command to restart a server (all devices embedded within the server))doc")
        .def("query_class_prop",
             &Tango::DServer::query_class_prop,
             R"doc(
                Command to return the list of property device at class level for the specified class
             )doc")
        .def("query_dev_prop",
             &Tango::DServer::query_dev_prop,
             R"doc(
                Command to return the list of property device at device level for the specified class
             )doc")
        .def("polled_device",
             &Tango::DServer::polled_device,
             R"doc(
               Command to read all the devices actually polled by the device server
             )doc")
        .def("dev_poll_status",
             &Tango::DServer::dev_poll_status,
             R"doc(
                Command to read device polling status

                :param dev_name: The device name
                :type dev_name: :py:obj:`str`

                :return: The device polling status as a string (multiple lines)
             )doc")
        .def("add_obj_polling",
             &Tango::DServer::add_obj_polling,
             R"doc(
                Command to add one object to be polled

                :param argin: The polling parameters, as a sequence of two sequences.
                              E.g. ([2000], ["sys/tg_test/1", "attribute", "double_scalar"])
                              Where first element: list of integers, where element at index 0 is update period in milliseconds.
                              And second element: a list of strings: index 0: device name;
                              index 1: object type, either "command" or "attribute"; index 2: object name

                :type argin: :py:obj:`tuple`\[:py:obj:`list`\[:py:obj:`int`], :py:obj:`list`\[:py:obj:`str`]]

                :param with_db_upd: set to true if db has to be updated
                :type with_db_upd: bool

                :param delta_ms:
                :type delta_ms: int
             )doc",
             py::arg("argin"),
             py::arg("with_db_upd") = true,
             py::arg("delta_ms") = 0)
        .def("upd_obj_polling_period",
             &Tango::DServer::upd_obj_polling_period,
             R"doc(
                Command to update an already polled object update period

                :param argin: The polling parameters, as a sequence of two sequences.
                              E.g. ([2000], ["sys/tg_test/1", "attribute", "double_scalar"])
                              Where first element: list of integers, where element at index 0 is update period in milliseconds.
                              And second element: a list of strings: index 0: device name;
                              index 1: object type, either "command" or "attribute"; index 2: object name

                :type argin: :py:obj:`tuple`\[:py:obj:`list`\[:py:obj:`int`], :py:obj:`list`\[:py:obj:`str`]]

                :param with_db_upd: set to true if db has to be updated
                :type with_db_upd: bool
             )doc",
             py::arg("argin"),
             py::arg("with_db_upd") = true)
        .def("rem_obj_polling",
             &Tango::DServer::rem_obj_polling,
             R"doc(
                Command to remove an already polled object from the device polled object list

                :param argin: The polling parameters: device name; object type (command or attribute); object name
                :type argin: :py:obj:`list`\[:py:obj:`str`]

                :param with_db_upd: set to true if db has to be updated
                :type with_db_upd: bool
             )doc",
             py::arg("argin"),
             py::arg("with_db_upd") = true)
        .def("stop_polling",
             &Tango::DServer::stop_polling,
             R"doc(
                Command to stop the polling thread
             )doc")
        .def("start_polling",
             py::overload_cast<>(&Tango::DServer::start_polling),
             R"doc(
                Command to start the polling thread
             )doc")
        .def("add_event_heartbeat",
             &Tango::DServer::add_event_heartbeat,
             R"doc(
                Command to ask the heartbeat thread to send the event heartbeat every 9 seconds
             )doc")
        .def("rem_event_heartbeat",
             &Tango::DServer::rem_event_heartbeat,
             R"doc(
                Command to ask the heartbeat thread to stop sending the event heartbeat
             )doc")
        .def("lock_device",
             &Tango::DServer::lock_device,
             R"doc(
                Command to lock device

                :param in_data: a structure with: (lock validity, name of the device(s) to be locked,)
                :type in_data: :py:obj:`tuple`\[:py:obj:`list`\[:py:obj:`int`], :py:obj:`list`\[:py:obj:`str`]]
             )doc",
             py::arg("in_data"))
        .def("un_lock_device",
             &Tango::DServer::un_lock_device,
             R"doc(
                Command to unlock device

                :param in_data: a structure with: (lock validity, name of the device(s) to be unlocked)
                :type in_data: :py:obj:`tuple`\[:py:obj:`list`\[:py:obj:`int`], :py:obj:`list`\[:py:obj:`str`]]
             )doc",
             py::arg("in_data"))
        .def("re_lock_devices",
             &Tango::DServer::re_lock_devices,
             R"doc(
                Command to relock device

                :param in_data: a structure with: (lock validity, name of the device(s) to be relocked)
                :type in_data: :py:obj:`tuple`\[:py:obj:`list`\[:py:obj:`int`], :py:obj:`list`\[:py:obj:`str`]]
             )doc",
             py::arg("in_data"))
        .def("dev_lock_status",
             &Tango::DServer::dev_lock_status,
             R"doc(
                Command to get device lock status

                :param dev_name: device name
                :type dev_name: :py:obj:`str`

                :return: device lock status
             )doc",
             py::arg("dev_name"))
        .def("delete_devices",
             &Tango::DServer::delete_devices,
             R"doc(Call destructor for all objects registered in the server)doc")
        .def("start_logging", &Tango::DServer::start_logging)
        .def("stop_logging", &Tango::DServer::stop_logging)
        .def("get_process_name", &Tango::DServer::get_process_name)
        .def("get_personal_name", &Tango::DServer::get_personal_name)
        .def("get_instance_name", &Tango::DServer::get_instance_name)
        .def("get_full_name", &Tango::DServer::get_full_name)
        .def("get_fqdn", &Tango::DServer::get_fqdn)
        .def("get_poll_th_pool_size", &Tango::DServer::get_poll_th_pool_size)
        .def("get_opt_pool_usage", &Tango::DServer::get_opt_pool_usage)
        .def("get_poll_th_conf", &Tango::DServer::get_poll_th_conf);
}
