/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

namespace PyDbServerData {

static inline py::str get_name(Tango::DbServerData &self) {
    return py::str(self.get_name());
}

} // namespace PyDbServerData

void export_db(py::module &m) {
    // Note: DbDatum in python is extended to support the python sequence API
    //       in the file ../PyTango/db.py. This way the DbDatum behaves like a
    //       sequence of strings. This allows the user to work with a DbDatum as
    //       if it was working with the old list of strings

    py::class_<Tango::DbDatum>(m,
                               "DbDatum",
                               R"doc(
                                    A single database value which has a name, type, address and value
                                    and methods for inserting and extracting C++ native types. This is
                                    the fundamental type for specifying database properties. Every
                                    property has a name and has one or more values associated with it.
                                    A status flag indicates if there is data in the DbDatum object or
                                    not. An additional flag allows the user to activate exceptions.

                                    Note: DbDatum is extended to support the python sequence API.
                                          This way the DbDatum behaves like a sequence of strings.
                                          This allows the user to work with a DbDatum as if it was
                                          working with the old list of strings.

                                    New in PyTango 7.0.0)doc")
        .def(py::init<>())
        .def(py::init<const char *>(), py::arg("name"))
        .def(py::init<const Tango::DbDatum &>(), py::arg("db_datum"))
        .def_readwrite("name", &Tango::DbDatum::name)
        //        .def_readwrite("value_string", &Tango::DbDatum::value_string)
        .def_property(
            "value_string",
            [](Tango::DbDatum &self) -> StdStringVector & { return self.value_string; },
            [](Tango::DbDatum &self, const StdStringVector &value) { self.value_string = value; },
            py::return_value_policy::reference_internal // Important to specify this policy
            )
        .def("size",
             &Tango::DbDatum::size,
             R"doc(
                size(self) -> int

                        Returns the number of separate elements in the value.

                    Parameters : None
                    Return     : the number of separate elements in the value.

                    New in PyTango 7.0.0)doc")
        .def("is_empty",
             &Tango::DbDatum::is_empty,
             R"doc(
                is_empty(self) -> bool

                        Returns True or False depending on whether the
                        DbDatum object contains data or not. It can be used to test
                        whether a property is defined in the database or not.

                    Parameters : None
                    Return     : (bool) True if no data or False otherwise.

                    New in PyTango 7.0.0)doc");

    py::class_<Tango::DbDevExportInfo>(m,
                                       "DbDevExportInfo",
                                       R"doc(
                                            A structure containing export info for a device (should be
                                            retrieved from the database) with the following members:

                                                - name : (str) device name
                                                - ior : (str) CORBA reference of the device
                                                - host : name of the computer hosting the server
                                                - version : (str) version
                                                - pid : process identifier)doc")
        .def(py::init<>())
        .def_readwrite("name", &Tango::DbDevExportInfo::name)
        .def_readwrite("ior", &Tango::DbDevExportInfo::ior)
        .def_readwrite("host", &Tango::DbDevExportInfo::host)
        .def_readwrite("version", &Tango::DbDevExportInfo::version)
        .def_readwrite("pid", &Tango::DbDevExportInfo::pid);

    py::class_<Tango::DbDevImportInfo>(m,
                                       "DbDevImportInfo",
                                       R"doc(
                                            A structure containing import info for a device (should be
                                            retrieved from the database) with the following members:

                                                - name : (str) device name
                                                - exported : 1 if device is running, 0 else
                                                - ior : (str)CORBA reference of the device
                                                - version : (str) version)doc")
        .def(py::init<>())
        .def_readonly("name", &Tango::DbDevImportInfo::name)
        .def_readonly("exported", &Tango::DbDevImportInfo::exported)
        .def_readonly("ior", &Tango::DbDevImportInfo::ior)
        .def_readonly("version", &Tango::DbDevImportInfo::version);

    py::class_<Tango::DbDevFullInfo, Tango::DbDevImportInfo>(m, "DbDevFullInfo")
        .def_readonly("class_name", &Tango::DbDevFullInfo::class_name)
        .def_readonly("ds_full_name", &Tango::DbDevFullInfo::ds_full_name)
        .def_readonly("host", &Tango::DbDevFullInfo::host)
        .def_readonly("started_date", &Tango::DbDevFullInfo::started_date)
        .def_readonly("stopped_date", &Tango::DbDevFullInfo::stopped_date)
        .def_readonly("pid", &Tango::DbDevFullInfo::pid);

    py::class_<Tango::DbDevInfo>(m,
                                 "DbDevInfo",
                                 R"doc(
                                    A structure containing available information for a device with
                                    the following members:

                                        - name : (str) name
                                        - _class : (str) device class
                                        - server : (str) server)doc")
        .def(py::init<>())
        .def_readwrite("name", &Tango::DbDevInfo::name)
        .def_readwrite("_class", &Tango::DbDevInfo::_class)
        .def_readwrite("klass", &Tango::DbDevInfo::_class)
        .def_readwrite("server", &Tango::DbDevInfo::server);

    py::class_<Tango::DbHistory>(m,
                                 "DbHistory",
                                 "A structure containing the modifications of a property. No public members.")
        .def(py::init<std::string, std::string, StdStringVector &>())
        .def(py::init<std::string, std::string, std::string, StdStringVector &>())
        .def("get_name",
             &Tango::DbHistory::get_name,
             R"doc(
                get_name(self) -> str

                        Returns the property name.

                    Parameters : None
                    Return     : (str) property name)doc")
        .def("get_attribute_name",
             &Tango::DbHistory::get_attribute_name,
             R"doc(
                get_attribute_name(self) -> str

                        Returns the attribute name (empty for object properties or device properties)

                    Parameters : None
                    Return     : (str) attribute name)doc")
        .def("get_date",
             &Tango::DbHistory::get_date,
             R"doc(
                get_date(self) -> str

                        Returns the update date

                    Parameters : None
                    Return     : (str) update date)doc")
        .def("get_value",
             &Tango::DbHistory::get_value,
             R"doc(
                get_value(self) -> DbDatum

                        Returns a COPY of the property value

                    Parameters : None
                    Return     : (DbDatum) a COPY of the property value)doc")
        .def("is_deleted",
             &Tango::DbHistory::is_deleted,
             R"doc(
               is_deleted(self) -> bool

                        Returns True if the property has been deleted or False otherwise

                    Parameters : None
                    Return     : (bool) True if the property has been deleted or False otherwise)doc");

    py::class_<Tango::DbServerInfo>(m,
                                    "DbServerInfo",
                                    R"doc(
                                        A structure containing available information for a device server with
                                            the following members:

                                                - name : (str) name
                                                - host : (str) host
                                                - mode : (str) mode
                                                - level : (str) level)doc")
        .def(py::init<>())
        .def_readwrite("name", &Tango::DbServerInfo::name)
        .def_readwrite("host", &Tango::DbServerInfo::host)
        .def_readwrite("mode", &Tango::DbServerInfo::mode)
        .def_readwrite("level", &Tango::DbServerInfo::level);

    py::class_<Tango::DbServerData>(m,
                                    "DbServerData",
                                    R"doc(
                                        A structure used for moving DS from one tango host to another.
                                        Create a new instance by: DbServerData(<server name>, <server instance>))doc")
        .def(py::init<const std::string &, const std::string &>())
        .def("get_name",
             &PyDbServerData::get_name,
             R"doc(
                get_name(self) -> str

                        Returns the full server name

                    Parameters : None
                    Return     : (str) the full server name)doc")
        .def("put_in_database",
             &Tango::DbServerData::put_in_database,
             R"doc(
                put_in_database(self, tg_host) -> None

                        Store all the data related to the device server process in the
                        database specified by the input arg.

                    Parameters :
                        - tg_host : (str) The tango host for the new database
                    Return     : None)doc",
             py::arg("tg_host"))
        .def("already_exist",
             &Tango::DbServerData::already_exist,
             R"doc(
                already_exist(self, tg_host) -> bool

                        Check if any of the device server process device(s) is already
                        defined in the database specified by the tango host given as input arg

                    Parameters :
                        - tg_host : (str) The tango host for the new database
                    Return     : (str) True in case any of the device is already known. False otherwise)doc",
             py::arg("tg_host"))
        .def("remove",
             py::overload_cast<>(&Tango::DbServerData::remove),
             R"doc(
                remove(self) -> None

                        Remove device server process from a database.

                    Parameters :
                        - tg_host : (str) The tango host for the new database
                    Return     : None)doc")
        .def("remove",
             py::overload_cast<const std::string &>(&Tango::DbServerData::remove),
             R"doc(
                remove(self, tg_host) -> None

                        Remove device server process from a database.

                    Parameters :
                        - tg_host : (str) The tango host for the new database
                    Return     : None)doc",
             py::arg("tg_host"));
}
