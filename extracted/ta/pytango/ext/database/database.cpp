/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "pyutils.h"

const char *param_numb_or_str_numb = "Second parameter must be an int or a string representing an int";

struct PyDatabase {
    static py::str get_device_alias(Tango::Database &self, const std::string &alias) {
        std::string devname;
        self.get_device_alias(alias, devname);
        return py::str(devname);
    }

    static py::str get_alias(Tango::Database &self, const std::string &devname) {
        std::string alias;
        self.get_alias(devname, alias);
        return py::str(alias);
    }

    static py::str get_attribute_alias(Tango::Database &self, const std::string &alias) {
        std::string attrname;
        self.get_attribute_alias(alias, attrname);
        return py::str(attrname);
    }

    static py::str dev_name(Tango::Database &self) {
        Tango::Connection *conn = static_cast<Tango::Connection *>(&self);
        return py::str(conn->dev_name());
    }

    static py::str get_device_from_alias(Tango::Database &self, const std::string &input) {
        std::string output;
        self.get_device_from_alias(input, output);
        return py::str(output);
    }

    static py::str get_alias_from_device(Tango::Database &self, const std::string &input) {
        std::string output;
        self.get_alias_from_device(input, output);
        return py::str(output);
    }

    static py::str get_attribute_from_alias(Tango::Database &self, const std::string &input) {
        std::string output;
        self.get_attribute_from_alias(input, output);
        return py::str(output);
    }

    static py::str get_alias_from_attribute(Tango::Database &self, const std::string &input) {
        std::string output;
        self.get_alias_from_attribute(input, output);
        return py::str(output);
    }
};

void export_database(py::module &m) {
    py::class_<Tango::Database,
               std::shared_ptr<Tango::Database>,
               Tango::Connection>(m,
                                  "Database",
                                  py::dynamic_attr(),
                                  R"doc(
                            Database is the high level Tango object which contains the link to the static database.
                            Database provides methods for all database commands : get_device_property(),
                            put_device_property(), info(), etc..
                            To create a Database, use the default constructor. Example::

                                db = Database()

                            The constructor uses the TANGO_HOST env. variable to determine which
                            instance of the Database to connect to.

                            If TANGO_HOST env is not set, or you want to connect to a specific database, you can provide host and port to constructor:

                                 db = Database(host: str, port: int)

                                 or:

                                 db = Database(host: str, port: str)

                            Alternatively, it is possible to start Database using file instead of a real database:

                                db = Database(filename: str))doc")
        .def(py::init<>(), py::call_guard<py::gil_scoped_release>())
        .def(py::init<const Tango::Database &>(), py::arg("database"), py::call_guard<py::gil_scoped_release>())
        .def(py::init<std::string &, int>(),
             py::arg("host"),
             py::arg("port"),
             py::call_guard<py::gil_scoped_release>())
        .def(py::init<std::string &>(),
             py::arg("trl"),
             py::call_guard<py::gil_scoped_release>())

        // I do not like it (better to force user to do int(port) in Python, but this is legacy ....
        .def(py::init([](const std::string &host, const std::string &port_str) {
                 int port = std::stoi(port_str);
                 return std::make_shared<Tango::Database>(host, port);
             }),
             py::arg("host"),
             py::arg("port"),
             py::call_guard<py::gil_scoped_release>())

        .def(py::pickle(
            [](Tango::Database &self) { // __getstate__
                // Serialize the base class part
                std::string &host = self.get_db_host();
                std::string &port = self.get_db_port();
                if(host.size() > 0 && port.size() > 0) {
                    return py::make_tuple(host, port);
                } else {
                    return py::make_tuple();
                }
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() == 0) {
                    return Tango::Database();
                } else if(py_tuple.size() != 2) {
                    std::string host = py_tuple[0].cast<std::string>();
                    int port = std::stoi(py_tuple[1].cast<std::string>());
                    return Tango::Database(host, port);
                }
                throw std::runtime_error("Invalid state!");
            }))
        //
        // general methods
        //
        .def("dev_name", &PyDatabase::dev_name)
        .def("write_filedatabase",
             &Tango::Database::write_filedatabase,
             R"doc(
                write_filedatabase(self) -> None

                        Force a write to the file if using a file based database.

                    Parameters : None
                    Return     : None

                    New in PyTango 7.0.0)doc")
        .def("reread_filedatabase",
             &Tango::Database::reread_filedatabase,
             R"doc(
                reread_filedatabase(self) -> None

                        Force a complete refresh over the database if using a file based database.

                    Parameters : None
                    Return     : None

                    New in PyTango 7.0.0)doc")
        .def("build_connection",
             &Tango::Database::write_filedatabase,
             R"doc(
                build_connection(self) -> None

                        Tries to build a connection to the Database server.

                    Parameters : None
                    Return     : None

                    New in PyTango 7.0.0)doc")
        .def("check_tango_host",
             &Tango::Database::check_tango_host,
             R"doc(
                check_tango_host(self, tango_host_env) -> None

                        Check the TANGO_HOST environment variable syntax and extract
                        database server host(s) and port(s) from it.

                    Parameters :
                        - tango_host_env : (str) The TANGO_HOST env. variable value
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("tango_host_env"))
        .def("check_access_control",
             &Tango::Database::check_access_control,
             R"doc(
                check_access_control(self, dev_name) -> AccessControlType

                        Check the access for the given device for this client.

                    Parameters :
                        - dev_name : (str) device name
                    Return     : the access control type as a AccessControlType object

                    New in PyTango 7.0.0)doc",
             py::arg("dev_name"))
        .def("is_control_access_checked",
             &Tango::Database::is_control_access_checked,
             R"doc(
                is_control_access_checked(self) -> bool

                        Returns True if control access is checked or False otherwise.

                    Parameters : None
                    Return     : (bool) True if control access is checked or False

                    New in PyTango 7.0.0)doc")
        .def("set_access_checked",
             &Tango::Database::set_access_checked,
             R"doc(
                set_access_checked(self, val) -> None

                        Sets or unsets the control access check.

                    Parameters :
                        - val : (bool) True to set or False to unset the access control
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("val"))
        .def("get_access_except_errors",
             &Tango::Database::get_access_except_errors,
             py::return_value_policy::reference_internal,
             R"doc(
                get_access_except_errors(self) -> DevErrorList

                        Returns a reference to the control access exceptions.

                    Parameters : None
                    Return     : DevErrorList

                    New in PyTango 7.0.0)doc")
        .def("is_multi_tango_host",
             &Tango::Database::is_multi_tango_host,
             R"doc(
                is_multi_tango_host(self) -> bool

                        Returns if in multi tango host.

                    Parameters : None
                    Return     : True if multi tango host or False otherwise

                    New in PyTango 7.1.4)doc")
        .def("get_file_name",
             &Tango::Database::get_file_name,
             py::return_value_policy::copy,
             R"doc(
                get_file_name(self) -> str

                        Returns the database file name or throws an exception
                        if not using a file database

                    Parameters : None
                    Return     : a string containing the database file name

                    Throws     : DevFailed

                    New in PyTango 7.2.0)doc")

        //
        // General methods
        //

        .def("get_info",
             &Tango::Database::get_info,
             R"doc(
                get_info(self) -> str

                        Query the database for some general info about the tables.

                    Parameters : None
                    Return     : a multiline string)doc")
        .def("get_host_list",
             py::overload_cast<>(&Tango::Database::get_host_list),
             R"doc(
                get_host_list(self) -> DbDatum

                        Returns the list of all host names registered in the database.

                    Return     : DbDatum with the list of registered host names)doc")
        .def("get_host_list",
             py::overload_cast<const std::string &>(&Tango::Database::get_host_list),
             R"doc(
                get_host_list(self, wildcard) -> DbDatum

                        Returns the list of all host names registered in the database.

                    Parameters :
                        - wildcard : (str) (optional) wildcard (eg: 'l-c0*')
                    Return     : DbDatum with the list of registered host names)doc",
             py::arg("wildcard"))
        .def("get_services",
             py::overload_cast<const std::string &, const std::string &>(&Tango::Database::get_services),
             R"doc(
                get_services(self, serv_name, inst_name) -> DbDatum

                        Query database for specified services.

                    Parameters :
                        - serv_name : (str) service name
                        - inst_name : (str) instance name (can be a wildcard character ('*'))
                    Return     : DbDatum with the list of available services

                    New in PyTango 3.0.4)doc",
             py::arg("serv_name"),
             py::arg("inst_name"))
        .def("get_device_service_list",
             py::overload_cast<const std::string &>(&Tango::Database::get_device_service_list),
             R"doc(
                get_device_service_list(self, dev_name) -> DbDatum

                        Query database for the list of services provided by the given device.

                    Parameters :
                        - dev_name : (str) device name
                    Return     : DbDatum with the list of services

                    New in PyTango 8.1.0)doc",
             py::arg("dev_name"))
        .def("register_service",
             py::overload_cast<const std::string &, const std::string &, const std::string &>(
                 &Tango::Database::register_service),
             R"doc(
                register_service(self, serv_name, inst_name, dev_name) -> None

                        Register the specified service wihtin the database.

                    Parameters :
                        - serv_name : (str) service name
                        - inst_name : (str) instance name
                        - dev_name : (str) device name
                    Return     : None

                    New in PyTango 3.0.4)doc",
             py::arg("serv_name"),
             py::arg("inst_name"),
             py::arg("dev_name"))
        .def("unregister_service",
             py::overload_cast<const std::string &, const std::string &>(&Tango::Database::unregister_service),
             R"doc(
                unregister_service(self, serv_name, inst_name) -> None

                        Unregister the specified service from the database.

                    Parameters :
                        - serv_name : (str) service name
                        - inst_name : (str) instance name
                    Return     : None

                    New in PyTango 3.0.4)doc",
             py::arg("serv_name"),
             py::arg("inst_name"))

        //
        // Device methods
        //

        .def("add_device",
             &Tango::Database::add_device,
             R"doc(
                add_device(self, dev_info) -> None

                        Add a device to the database. The device name, server and class
                        are specified in the DbDevInfo structure

                        Example :
                            dev_info = DbDevInfo()
                            dev_info.name = 'my/own/device'
                            dev_info._class = 'MyDevice'
                            dev_info.server = 'MyServer/test'
                            db.add_device(dev_info)

                    Parameters :
                        - dev_info : (DbDevInfo) device information
                    Return     : None)doc",
             py::arg("dev_info"))
        .def("delete_device",
             &Tango::Database::delete_device,
             R"doc(
                delete_device(self, dev_name) -> None

                        Delete the device of the specified name from the database.

                    Parameters :
                        - dev_name : (str) device name
                    Return     : None)doc",
             py::arg("dev_name"))
        .def("import_device",
             py::overload_cast<const std::string &>(&Tango::Database::import_device),
             R"doc(
                import_device(self, dev_name) -> DbDevImportInfo

                        Query the databse for the export info of the specified device.

                        Example :
                            dev_imp_info = db.import_device('my/own/device')
                            print(dev_imp_info.name)
                            print(dev_imp_info.exported)
                            print(dev_imp_info.ior)
                            print(dev_imp_info.version)

                    Parameters :
                        - dev_name : (str) device name
                    Return     : DbDevImportInfo)doc",
             py::arg("dev_name"))
        .def("export_device",
             &Tango::Database::export_device,
             R"doc(
                export_device(self, dev_export) -> None

                        Update the export info for this device in the database.

                        Example :
                            dev_export = DbDevExportInfo()
                            dev_export.name = 'my/own/device'
                            dev_export.ior = <the real ior>
                            dev_export.host = <the host>
                            dev_export.version = '3.0'
                            dev_export.pid = '....'
                            db.export_device(dev_export)

                    Parameters :
                        - dev_export : (DbDevExportInfo) export information
                    Return     : None)doc",
             py::arg("dev_export"))
        .def("unexport_device",
             &Tango::Database::unexport_device,
             R"doc(
                unexport_device(self, dev_name) -> None

                        Mark the specified device as unexported in the database

                        Example :
                           db.unexport_device('my/own/device')

                    Parameters :
                        - dev_name : (str) device name
                    Return     : None)doc",
             py::arg("dev_name"))
        .def("get_device_info",
             &Tango::Database::get_device_info,
             R"doc(
                get_device_info(self, dev_name) -> DbDevFullInfo

                        Query the database for the full info of the specified device.

                        Example :
                            dev_info = db.get_device_info('my/own/device')
                            print(dev_info.name)
                            print(dev_info.class_name)
                            print(dev_info.ds_full_name)
                            print(dev_info.host)
                            print(dev_info.exported)
                            print(dev_info.ior)
                            print(dev_info.version)
                            print(dev_info.pid)
                            print(dev_info.started_date)
                            print(dev_info.stopped_date)

                    Parameters :
                        - dev_name : (str) device name
                    Return     : DbDevFullInfo

                    .. versionadded:: 8.1.0

                    .. versionchanged:: 10.1.0 Added *host* field to DbDevFullInfo)doc",
             py::arg("dev_name"))
        .def("get_device_name",
             py::overload_cast<const std::string &, const std::string &>(&Tango::Database::get_device_name),
             R"doc(
                get_device_name(self, serv_name, class_name) -> DbDatum

                        Query the database for a list of devices served by a server for
                        a given device class

                    Parameters :
                        - serv_name : (str) server name
                        - class_name : (str) device class name
                    Return     : DbDatum with the list of device names)doc",
             py::arg("serv_name"),
             py::arg("class_name"))
        .def("get_device_exported",
             &Tango::Database::get_device_exported,
             R"doc(
                get_device_exported(self, filter) -> DbDatum

                        Query the database for a list of exported devices whose names
                        satisfy the supplied filter (* is wildcard for any character(s))

                    Parameters :
                        - filter : (str) device name filter (wildcard)
                    Return     : DbDatum with the list of exported devices)doc",
             py::arg("filter"))
        .def("get_device_domain",
             &Tango::Database::get_device_domain,
             R"doc(
                get_device_domain(self, wildcard) -> DbDatum

                        Query the database for a list of of device domain names which
                        match the wildcard provided (* is wildcard for any character(s)).
                        Domain names are case insensitive.

                    Parameters :
                        - wildcard : (str) domain filter
                    Return     : DbDatum with the list of device domain names)doc",
             py::arg("wildcard"))
        .def("get_device_family",
             &Tango::Database::get_device_family,
             R"doc(
                get_device_family(self, wildcard) -> DbDatum

                        Query the database for a list of of device family names which
                        match the wildcard provided (* is wildcard for any character(s)).
                        Family names are case insensitive.

                    Parameters :
                        - wildcard : (str) family filter
                    Return     : DbDatum with the list of device family names)doc",
             py::arg("wildcard"))
        .def("get_device_member",
             &Tango::Database::get_device_member,
             R"doc(
                get_device_member(self, wildcard) -> DbDatum

                        Query the database for a list of of device member names which
                        match the wildcard provided (* is wildcard for any character(s)).
                        Member names are case insensitive.

                    Parameters :
                        - wildcard : (str) member filter
                    Return     : DbDatum with the list of device member names)doc",
             py::arg("wildcard"))
        .def("get_device_alias",
             &PyDatabase::get_device_alias,
             R"doc(
                get_device_alias(self, alias) -> str

                        Get the device name from an alias.

                    Parameters :
                        - alias : (str) alias
                    Return     : device name

                    .. deprecated:: 8.1.0
                        Use :meth:`~tango.Database.get_device_from_alias` instead)doc",
             py::arg("alias"))
        .def("get_alias",
             &PyDatabase::get_alias,
             R"doc(
                get_alias(self, dev_name) -> str

                        Get the device alias name from its name.

                    Parameters :
                        - dev_name : (str) device name
                    Return     : alias

                    New in PyTango 3.0.4

                    .. deprecated:: 8.1.0
                        Use :meth:`~tango.Database.get_alias_from_device` instead)doc",
             py::arg("dev_name"))
        .def("get_device_alias_list",
             &Tango::Database::get_device_alias_list,
             R"doc(
                get_device_alias_list(self, filter) -> DbDatum

                        Get device alias list. The parameter alias is a string to filter
                        the alias list returned. Wildcard (*) is supported.

                    Parameters :
                        - filter : (str) a string with the alias filter (wildcard (*) is supported)
                    Return     : DbDatum with the list of device names

                    New in PyTango 7.0.0)doc",
             py::arg("filter"))
        .def("get_class_for_device",
             &Tango::Database::get_class_for_device,
             R"doc(
                get_class_for_device(self, dev_name) -> str

                        Return the class of the specified device.

                    Parameters :
                        - dev_name : (str) device name
                    Return     : a string containing the device class)doc",
             py::arg("dev_name"))
        .def("get_class_inheritance_for_device",
             &Tango::Database::get_class_inheritance_for_device,
             R"doc(
                get_class_inheritance_for_device(self, dev_name) -> DbDatum

                        Return the class inheritance scheme of the specified device.

                    Parameters :
                        - devn_ame : (str) device name
                    Return     : DbDatum with the inheritance class list

                    New in PyTango 7.0.0)doc",
             py::arg("dev_name"))
        .def("get_device_exported_for_class",
             &Tango::Database::get_device_exported_for_class,
             R"doc(
                get_device_exported_for_class(self, class_name) -> DbDatum

                        Query database for list of exported devices for the specified class.

                    Parameters :
                        - class_name : (str) class name
                    Return     : DbDatum with the list of exported devices for the

                    New in PyTango 7.0.0)doc",
             py::arg("class_name"))
        .def("put_device_alias",
             &Tango::Database::put_device_alias,
             R"doc(
                put_device_alias(self, dev_name, alias) -> None

                        Query database for list of exported devices for the specified class.

                    Parameters :
                        - dev_name : (str) device name
                        - alias : (str) alias name
                    Return     : None)doc",
             py::arg("dev_name"),
             py::arg("alias"))
        .def("delete_device_alias",
             &Tango::Database::delete_device_alias,
             R"doc(
                delete_device_alias(self, alias) -> void

                        Delete a device alias

                    Parameters :
                        - alias : (str) alias name
                    Return     : None)doc",
             py::arg("alias"))

        //
        // server methods
        //

        .def("_add_server",
             &Tango::Database::add_server,
             R"doc(
                _add_server(self, serv_name, dev_info) -> None

                        Add a group of devices to the database.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - serv_name : (str) server name
                        - dev_info : (DbDevInfos) server device(s) information
                    Return     : None)doc",
             py::arg("serv_name"),
             py::arg("dev_info"))
        .def("delete_server",
             &Tango::Database::delete_server,
             R"doc(
                delete_server(self, server) -> None

                        Delete the device server and its associated devices from database.

                    Parameters :
                        - server : (str) name of the server to be deleted with
                                   format: <server name>/<instance>
                    Return     : None)doc",
             py::arg("server"))
        .def("_export_server",
             &Tango::Database::export_server,
             R"doc(
                _export_server(self, dev_info) -> None

                        Export a group of devices to the database.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_info : (DbDevExportInfos) device(s) to export information
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_info"))
        .def("unexport_server",
             &Tango::Database::unexport_server,
             R"doc(
                unexport_server(self, server) -> None

                        Mark all devices exported for this server as unexported.

                    Parameters :
                        - server : (str) name of the server to be unexported with
                                   format: <server name>/<instance>
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("server"))
        .def("rename_server",
             &Tango::Database::rename_server,
             R"doc(
                rename_server(self, old_ds_name, new_ds_name) -> None

                        Rename a device server process.

                    Parameters :
                        - old_ds_name : (str) old name
                        - new_ds_name : (str) new name
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 8.1.0)doc",
             py::arg("old_ds_name"),
             py::arg("new_ds_name"))
        .def("get_server_info",
             &Tango::Database::get_server_info,
             R"doc(
                get_server_info(self, server) -> DbServerInfo

                        Query the database for server information.

                    Parameters :
                        - server : (str) name of the server with format: <server name>/<instance>
                    Return     : DbServerInfo with server information

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("server"))
        .def("put_server_info",
             &Tango::Database::put_server_info,
             R"doc(
                put_server_info(self, info) -> None

                        Add/update server information in the database.

                    Parameters :
                        - info : (DbServerInfo) new server information
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("info"))
        .def("delete_server_info",
             &Tango::Database::delete_server_info,
             R"doc(
                delete_server_info(self, server) -> None

                        Delete server information of the specified server from the database.

                    Parameters :
                        - server : (str) name of the server to be deleted with
                                   format: <server name>/<instance>
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("server"))
        .def("get_server_class_list",
             &Tango::Database::get_server_class_list,
             R"doc(
                get_server_class_list(self, server) -> DbDatum

                        Query the database for a list of classes instantiated by the
                        specified server. The DServer class exists in all TANGO servers
                        and for this reason this class is removed from the returned list.

                    Parameters :
                        - server : (str) name of the server to be deleted with
                                   format: <server name>/<instance>
                    Return     : DbDatum containing list of class names instanciated by
                                 the specified server

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("server"))
        .def("get_server_name_list",
             &Tango::Database::get_server_name_list,
             R"doc(
                get_server_name_list(self) -> DbDatum

                        Return the list of all server names registered in the database.

                    Parameters : None
                    Return     : DbDatum containing list of server names

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc")
        .def("get_instance_name_list",
             &Tango::Database::get_instance_name_list,
             R"doc(
                get_instance_name_list(self, serv_name) -> DbDatum

                        Return the list of all instance names existing in the database for the specifed server.

                    Parameters :
                        - serv_name : (str) server name with format <server name>
                    Return     : DbDatum containing list of instance names for the specified server

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("serv_name"))
        .def("get_server_list",
             py::overload_cast<>(&Tango::Database::get_server_list),
             R"doc(
            get_server_list(self) -> DbDatum

                    Return the list of all servers registered in the database.

                Return     : DbDatum containing list of registered servers)doc")
        .def("get_server_list",
             py::overload_cast<const std::string &>(&Tango::Database::get_server_list),
             R"doc(
                get_server_list(self, wildcard) -> DbDatum

                        Return the list of of matching servers
                        will be returned (ex: Serial/\\*)

                    Parameters :
                        - wildcard : (str) host wildcard (ex: Serial/\\*)
                    Return     : DbDatum containing list of registered servers)doc",
             py::arg("wildcard"))
        .def("get_host_server_list",
             &Tango::Database::get_host_server_list,
             R"doc(
                get_host_server_list(self, host_name) -> DbDatum

                        Query the database for a list of servers registered on the specified host.

                    Parameters :
                        - host_name : (str) host name
                    Return     : DbDatum containing list of servers for the specified host

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("host_name"))
        .def("get_device_class_list",
             &Tango::Database::get_device_class_list,
             R"doc(
                get_device_class_list(self, server) -> DbDatum

                        Query the database for a list of devices and classes served by
                        the specified server. Return a list with the following structure:
                        [device name, class name, device name, class name, ...]

                    Parameters :
                        - server : (str) name of the server with format: <server name>/<instance>
                    Return     : DbDatum containing list with the following structure:
                                 [device_name, class name]

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 3.0.4)doc",
             py::arg("server"))
        .def("get_server_release",
             &Tango::Database::get_server_release,
             R"doc(
                get_server_release(self) -> int

                :return: server version
                :rtype: int)doc")

        //
        // property methods
        //

        .def("_get_property",
             py::overload_cast<std::string, Tango::DbData &>(&Tango::Database::get_property),
             R"doc(
                _get_property(self, obj_name, props) -> None

                        Query the database for a list of object (i.e non-device)
                        properties. The property names are specified by the
                        DbData (seq<DbDatum>) structures. The method returns the
                        properties in the same DbDatum structures
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - obj_name : (str) object name
                        - props [in, out] : (DbData) property names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("obj_name"),
             py::arg("props"))
        .def("_get_property_forced",
             &Tango::Database::get_property_forced,
             R"doc(
                _get_property_forced(self, obj, db_data, dsc) -> None

                :param obj:
                :type obj: str

                :param db_data:
                :type db_data: DbData

                :param dsc:
                :type dsc: DbServerCache)doc",
             py::arg("obj"),
             py::arg("db_data"),
             py::arg("dsc"))
        .def("_put_property",
             &Tango::Database::put_property,
             R"doc()doc",
             py::arg("obj_name"),
             py::arg("value"))
        .def("_delete_property",
             &Tango::Database::delete_property,
             R"doc(
                _delete_property(self, obj_name, props) -> None

                        Delete a list of properties for the specified object.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - obj_name : (str) object name
                        - props : (DbData) property names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("obj_name"),
             py::arg("props"))
        .def("get_property_history",
             &Tango::Database::get_property_history,
             R"doc(
                get_property_history(self, obj_name, prop_name) -> DbHistoryList

                        Get the list of the last 10 modifications of the specifed object
                        property. Note that propname can contain a wildcard character
                        (eg: 'prop*')

                    Parameters :
                        - serv_name : (str) server name
                        - prop_name : (str) property name
                    Return     : DbHistoryList containing the list of modifications

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("obj_name"),
             py::arg("props"))
        .def("get_object_list",
             &Tango::Database::get_object_list,
             R"doc(
                get_object_list(self, wildcard) -> DbDatum

                        Query the database for a list of object (free properties) for
                        which properties are defined and which match the specified
                        wildcard.

                    Parameters :
                        - wildcard : (str) object wildcard
                    Return     : DbDatum containing the list of object names matching the given wildcard

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("wildcard"))
        .def("get_object_property_list",
             &Tango::Database::get_object_property_list,
             R"doc(
                get_object_property_list(self, obj_name, wildcard) -> DbDatum

                        Query the database for a list of properties defined for the
                        specified object and which match the specified wildcard.

                    Parameters :
                        - obj_name : (str) object name
                        - wildcard : (str) property name wildcard
                    Return     : DbDatum with list of properties defined for the specified
                                 object and which match the specified wildcard

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("obj_name"),
             py::arg("wildcard"))
        .def("_get_device_property",
             py::overload_cast<std::string, Tango::DbData &>(&Tango::Database::get_device_property),
             R"doc(
                _get_device_property(self, dev_name, props) -> None

                        Query the database for a list of device properties for the
                        specified device. The property names are specified by the
                        DbData (seq<DbDatum>) structures. The method returns the
                        properties in the same DbDatum structures
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - props : (DbData) property names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("props"))
        .def("_put_device_property",
             &Tango::Database::put_device_property,
             R"doc(
                _put_device_property(self, dev_name, props) -> None

                        Insert or update a list of properties for the specified device.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - props : (DbData) property data
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("props"))
        .def("_delete_device_property",
             &Tango::Database::delete_device_property,
             R"doc(
                _delete_device_property(self, dev_name, props) -> None

                        Delete a list of properties for the specified device.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - props : (DbData) property names to be deleted
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("props"))
        .def("get_device_property_history",
             &Tango::Database::get_device_property_history,
             R"doc(
                get_device_property_history(self, dev_name, prop_name) -> DbHistoryList

                        Get the list of the last 10 modifications of the specified device
                        property. Note that propname can contain a wildcard character
                        (eg: 'prop*').
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) server name
                        - prop_name : (str) property name
                    Return     : DbHistoryList containing the list of modifications

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("dev_name"),
             py::arg("prop_name"))
        .def("_get_device_property_list",
             py::overload_cast<const std::string &, const std::string &>(&Tango::Database::get_device_property_list),
             R"doc(
                _get_device_property_list(self, dev_name, wildcard) -> DbDatum

                        Query the database for a list of properties defined for the
                        specified device and which match the specified wildcard.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - wildcard : (str) property name wildcard
                    Return     : DbDatum containing the list of property names or None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("wildcard"))

        .def("_get_device_property_list",
             py::overload_cast<std::string &, const std::string &, StdStringVector &, std::shared_ptr<Tango::DbServerCache>>(&Tango::Database::get_device_property_list),
             py::arg("dev_name"),
             py::arg("wildcard"),
             py::arg("container"),
             py::arg("dsc") = nullptr,
             R"doc(
                _get_device_property_list(self, dev_name, wildcard, container) -> None

                        Query the database for a list of properties defined for the
                        specified device and which match the specified wildcard.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - wildcard : (str) property name wildcard
                        - container [out] : (StdStringVector) array that will contain the matching
                                            property names
                    Return     : DbDatum containing the list of property names or None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc")
        .def("_get_device_attribute_property",
             py::overload_cast<std::string, Tango::DbData &>(&Tango::Database::get_device_attribute_property),
             R"doc(
                _get_device_attribute_property(self, dev_name, props) -> None

                        Query the database for a list of device attribute properties for
                        the specified device. The attribute names are specified by the
                        DbData (seq<DbDatum>) structures. The method returns all the
                        properties for the specified attributes in the same DbDatum structures.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - props [in, out] : (DbData) attribute names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("props"))
        .def("_put_device_attribute_property",
             &Tango::Database::put_device_attribute_property,
             R"doc(
                _put_device_attribute_property(self, dev_name, props) -> None

                        Insert or update a list of attribute properties for the specified device.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - props : (DbData) property data
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("props"))
        .def("_delete_device_attribute_property",
             &Tango::Database::delete_device_attribute_property,
             R"doc(
                _delete_device_attribute_property(self, dev_name, props) -> None

                        Delete a list of attribute properties for the specified device.
                        The attribute names are specified by the vector of DbDatum structures. Here
                        is an example of how to delete the unit property of the velocity attribute of
                        the id11/motor/1 device using this method :

                        db_data = tango.DbData();
                        db_data.append(DbDatum("velocity"));
                        db_data.append(DbDatum("unit"));
                        db.delete_device_attribute_property("id11/motor/1", db_data);

                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) server name
                        - props : (DbData) attribute property data
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("props"))
        .def("get_device_attribute_property_history",
             &Tango::Database::get_device_attribute_property_history,
             R"doc(
                get_device_attribute_property_history(self, dev_name, attr_name, prop_name) -> DbHistoryList

                        Get the list of the last 10 modifications of the specified device
                        attribute property. Note that propname and devname can contain a
                        wildcard character (eg: 'prop*').

                    Parameters :
                        - dev_name : (str) device name
                        - attr_name : (str) attribute name
                        - prop_name : (str) property name

                    Return     : DbHistoryList containing the list of modifications

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("dev_name"),
             py::arg("attr_name"),
             py::arg("prop_name"))
        .def("get_device_attribute_list",
             &Tango::Database::get_device_attribute_list,
             R"doc(
                get_device_attribute_list(self, dev_name, att_list) -> None

                        Get the list of attribute(s) with some data defined in database
                        for a specified device. Note that this is not the list of all
                        device attributes because not all attribute(s) have some data
                        in database
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - dev_name : (str) device name
                        - att_list [out] : (StdStringVector) array that will contain the
                                           attribute name list
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("dev_name"),
             py::arg("att_list"))
        .def("_get_class_property",
             py::overload_cast<std::string, Tango::DbData &>(&Tango::Database::get_class_property),
             R"doc(
                _get_class_property(self, class_name, props) -> None

                        Query the database for a list of class properties. The property
                        names are specified by the DbData (seq<DbDatum>) structures.
                        The method returns the properties in the same DbDatum structures.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - class_name : (str) class name
                        - props [in, out] : (DbData) property names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("_put_class_property",
             &Tango::Database::put_class_property,
             R"doc(
                _put_class_property(self, class_name, props) -> None

                        Insert or update a list of properties for the specified class.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - class_name : (str) class name
                        - props : (DbData) property data to be inserted
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("_delete_class_property",
             &Tango::Database::delete_class_property,
             R"doc(
                _delete_class_property(self, class_name, props) -> None

                        Delete a list of properties for the specified class.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - class_name : (str) class name
                        - props  : (DbData) property names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("get_class_property_history",
             &Tango::Database::get_class_property_history,
             R"doc(
                get_class_property_history(self, class_name, prop_name) -> DbHistoryList

                        Get the list of the last 10 modifications of the specified class
                        property. Note that propname can contain a wildcard character
                        (eg: 'prop*').

                    Parameters :
                        - class_name : (str) class name
                        - prop_name : (str) property name
                    Return     : DbHistoryList containing the list of modifications

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("get_class_list",
             &Tango::Database::get_class_list,
             R"doc(
                get_class_list(self, wildcard) -> DbDatum

                        Query the database for a list of classes which match the specified wildcard

                    Parameters :
                        - wildcard : (str) class wildcard
                    Return     : DbDatum containing the list of matching classes

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("wildcard"))
        .def("get_class_property_list",
             py::overload_cast<const std::string &>(&Tango::Database::get_class_property_list),
             R"doc(
                get_class_property_list(self, class_name) -> DbDatum

                        Query the database for a list of properties defined for the specified class.

                    Parameters :
                        - class_name : (str) class name
                    Return     : DbDatum containing the list of properties for the specified class

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"))
        .def("_get_class_attribute_property",
             py::overload_cast<std::string, Tango::DbData &>(&Tango::Database::get_class_attribute_property),
             R"doc(
                _get_class_attribute_property(self, class_name, props) -> None

                        Query the database for a list of class attribute properties for
                        the specified object. The attribute names are returned with the
                        number of properties specified as their value. The first DbDatum
                        element of the returned DbData vector contains the first
                        attribute name and the first attribute property number. The
                        following DbDatum element contains the first attribute property
                        name and property values.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - class_name : (str) class name
                        - props [in,out] : (DbData) property names
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("_put_class_attribute_property",
             &Tango::Database::put_class_attribute_property,
             R"doc(
                _put_class_attribute_property(self, class_name, props) -> None

                        Insert or update a list of attribute properties for the specified class.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - class_name : (str) class name
                        - props : (DbData) property data
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("_delete_class_attribute_property",
             &Tango::Database::delete_class_attribute_property,
             R"doc(
                _delete_class_attribute_property(self, class_name, props) -> None

                        Delete a list of attribute properties for the specified class.
                        This corresponds to the pure C++ API call.

                    Parameters :
                        - class_name : (str) class name
                        - props : (DbData) attribute property data
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("class_name"),
             py::arg("props"))
        .def("get_class_attribute_property_history",
             &Tango::Database::get_class_attribute_property_history,
             R"doc(
                get_class_attribute_property_history(self, class_name, attr_name, prop_name) -> DbHistoryList

                        Get the list of the last 10 modifications of the specifed class attribute
                        property. Note that prop_name and attr_name can contain a wildcard character
                        (eg: 'prop*').

                    Parameters :
                        - class_name : (str) class name
                        - attr_name : (str) attribute name
                        - prop_name : (str) property name
                    Return     : DbHistoryList containing the list of modifications

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("class_name"),
             py::arg("attr_name"),
             py::arg("prop_name"))
        .def("get_class_attribute_list",
             &Tango::Database::get_class_attribute_list,
             R"doc(
                get_class_attribute_list(self, class_name, wildcard) -> DbDatum

                        Query the database for a list of attributes defined for the specified
                        class which match the specified wildcard.

                    Parameters :
                        - class_name : (str) class name
                        - wildcard : (str) attribute name
                    Return     : DbDatum containing the list of matching attributes for the given class

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("class_name"),
             py::arg("wildcard"))

        //
        // Attribute methods
        //

        .def("get_attribute_alias",
             &PyDatabase::get_attribute_alias,
             R"doc(
                get_attribute_alias(self, alias) -> str

                        Get the full attribute name from an alias.

                    Parameters :
                        - alias : (str) attribute alias
                    Return     :  full attribute name

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    .. deprecated:: 8.1.0
                        Use :meth:`~tango.Database.get_attribute_from_alias` instead)doc",
             py::arg("alias"))
        .def("get_attribute_alias_list",
             &Tango::Database::get_attribute_alias_list,
             R"doc(
                get_attribute_alias_list(self, filter) -> DbDatum

                    Get attribute alias list. The parameter alias is a string to
                    filter the alias list returned. Wildcard (*) is supported. For
                    instance, if the string alias passed as the method parameter
                    is initialised with only the * character, all the defined
                    attribute alias will be returned. If there is no alias with the
                    given filter, the returned array will have a 0 size.

                Parameters :
                    - filter : (str) attribute alias filter
                Return     : DbDatum containing the list of matching attribute alias

                Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("filter"))
        .def("put_attribute_alias",
             &Tango::Database::put_attribute_alias,
             R"doc(
                put_attribute_alias(self, attr_name, alias) -> None

                        Set an alias for an attribute name. The attribute alias is
                        specified by alias and the attribute name is specifed by
                        attr_name. If the given alias already exists, a DevFailed exception
                        is thrown.

                    Parameters :
                        - attr_name : (str) full attribute name
                        - alias : (str) alias
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("attr_name"),
             py::arg("alias"))
        .def("delete_attribute_alias",
             &Tango::Database::delete_attribute_alias,
             R"doc(
                delete_attribute_alias(self, alias) -> None

                        Remove the alias associated to an attribute name.

                    Parameters :
                        - alias : (str) alias
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError))doc",
             py::arg("alias"))

        //
        // event methods
        //

        .def("export_event",
             &Tango::Database::export_event,
             R"doc(
                export_event(self, event_data) -> None

                        Export an event to the database.

                    Parameters :
                        - event_data : (sequence<str>) event data (same as DbExportEvent Database command)
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("event_data"))
        .def("unexport_event",
             &Tango::Database::unexport_event,
             R"doc(
                unexport_event(self, event) -> None

                        Un-export an event from the database.

                    Parameters :
                        - event : (str) event
                    Return     : None

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 7.0.0)doc",
             py::arg("event"))

        //
        // alias methods
        //

        .def("get_device_from_alias",
             &PyDatabase::get_device_from_alias,
             R"doc(
                get_device_from_alias(self, alias) -> str

                        Get the device name from an alias.

                    Parameters :
                        - alias : (str) alias
                    Return     : device name

                    New in PyTango 8.1.0)doc",
             py::arg("alias"))
        .def("get_alias_from_device",
             &PyDatabase::get_alias_from_device,
             R"doc(
                get_alias_from_device(self, dev_name) -> str

                        Get the device alias name from its name.

                    Parameters :
                        - dev_name : (str) device name
                    Return     : alias

                    New in PyTango 8.1.0)doc",
             py::arg("dev_name"))
        .def("get_attribute_from_alias",
             &PyDatabase::get_attribute_from_alias,
             R"doc(
                get_attribute_from_alias(self, alias) -> str

                    Get the full attribute name from an alias.

                Parameters :
                    - alias : (str) attribute alias
                Return     :  full attribute name

                Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                New in PyTango 8.1.0)doc",
             py::arg("alias"))
        .def("get_alias_from_attribute",
             &PyDatabase::get_alias_from_attribute,
             R"doc(
                get_alias_from_attribute(self, attr_name) -> str

                        Get the attribute alias from the full attribute name.

                    Parameters :
                        - attr_name : (str) full attribute name
                    Return     :  attribute alias

                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device (DB_SQLError)

                    New in PyTango 8.1.0)doc",
             py::arg("attr_name"));
}
