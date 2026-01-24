/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "convertors/data_array_from_py.h"
#include "pyutils.h"
#include "base_types_structures/exception.h"
#include "server/device_class.h"

Tango::TangoTimestamp __convert_time(const py::object py_time) {
    if(!py_time.is_none()) {
        return Tango::TangoTimestamp(static_cast<time_t>(py_time.cast<double>()));
    } else {
        return Tango::TangoTimestamp(Tango::get_current_system_datetime());
    }
}

template <int tangoTypeConst>
void __fill_attr_polling_buffer_scalar(Tango::Util &self,
                                       Tango::DeviceImpl *dev,
                                       std::string &att_name,
                                       py::sequence &data) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    auto attr_history_stack = Tango::AttrHistoryStack<TangoScalarType>();

    for(auto item : data) {
        py::object obj = item.cast<py::object>();

        Tango::TangoTimestamp time_stamp(__convert_time(obj.attr("time_stamp")));

        if(!obj.attr("error").is_none()) {
            Tango::DevErrorList error = obj.attr("error").cast<Tango::DevErrorList>();
            attr_history_stack.push(Tango::TimedAttrData<TangoScalarType>(error, time_stamp));

        } else {
            std::unique_ptr<TangoScalarType> value(new TangoScalarType);
            python_scalar_to_cpp<tangoTypeConst>::convert(obj.attr("value"), *value);

            auto quality = obj.attr("quality").cast<Tango::AttrQuality>();

            if(obj.attr("w_value").is_none()) {
                attr_history_stack.push(Tango::TimedAttrData(value.release(), quality, true, time_stamp));
            } else {
                std::unique_ptr<TangoScalarType> w_value(new TangoScalarType);
                python_scalar_to_cpp<tangoTypeConst>::convert(obj.attr("w_value"), *w_value);

                attr_history_stack.push(Tango::TimedAttrData(value.release(), w_value.release(), quality, true, time_stamp));
            }
        }
    }
    self.fill_attr_polling_buffer(dev, att_name, attr_history_stack);
}

template <int tangoTypeConst>
void __fill_attr_polling_buffer_array(Tango::Util &self,
                                      Tango::DeviceImpl *dev,
                                      std::string &att_name,
                                      py::sequence &data,
                                      bool is_image) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    static const int tangoArrayTypeConst = TANGO_const2arrayconst(tangoTypeConst);

    auto attr_history_stack = Tango::AttrHistoryStack<TangoScalarType>();

    for(auto item : data) {
        py::object obj = item.cast<py::object>();

        Tango::TangoTimestamp time_stamp(__convert_time(obj.attr("time_stamp")));

        if(!obj.attr("error").is_none()) {
            Tango::DevErrorList error = obj.attr("error").cast<Tango::DevErrorList>();
            attr_history_stack.push(Tango::TimedAttrData<TangoScalarType>(error, time_stamp));

        } else {
            py::object py_value = obj.attr("value");
            TangoScalarType *cpp_value;
            py::size_t dim_x = 0, dim_y = 0;

            cpp_value = python_to_cpp_buffer<tangoArrayTypeConst>(py_value,
                                                                  MemoryAllocation::NEW,
                                                                  "fill_attr_polling_buffer_array",
                                                                  is_image,
                                                                  dim_x,
                                                                  dim_y);

            long res_dim_x = static_cast<long>(dim_x);
            long res_dim_y = static_cast<long>(dim_y);

            auto quality = obj.attr("quality").cast<Tango::AttrQuality>();

            if(obj.attr("w_value").is_none()) {
                if(!is_image) {
                    attr_history_stack.push(Tango::TimedAttrData(cpp_value,
                                                                 res_dim_x,
                                                                 quality,
                                                                 true,
                                                                 time_stamp));
                } else {
                    attr_history_stack.push(Tango::TimedAttrData(cpp_value,
                                                                 res_dim_x,
                                                                 res_dim_y,
                                                                 quality,
                                                                 true,
                                                                 time_stamp));
                }
            } else {
                TangoScalarType *cpp_w_value;
                py::size_t w_dim_x = 0, w_dim_y = 0;
                py::object py_w_value = obj.attr("w_value");

                cpp_w_value = python_to_cpp_buffer<tangoArrayTypeConst>(py_w_value,
                                                                        MemoryAllocation::NEW,
                                                                        "fill_attr_polling_buffer_array",
                                                                        is_image,
                                                                        w_dim_x,
                                                                        w_dim_y);

                long w_res_dim_x = static_cast<long>(w_dim_x);
                long w_res_dim_y = static_cast<long>(w_dim_y);

                if(!is_image) {
                    attr_history_stack.push(Tango::TimedAttrData(cpp_value,
                                                                 res_dim_x,
                                                                 cpp_w_value,
                                                                 w_res_dim_x,
                                                                 quality,
                                                                 true,
                                                                 time_stamp));
                } else {
                    attr_history_stack.push(Tango::TimedAttrData(cpp_value,
                                                                 res_dim_x,
                                                                 res_dim_y,
                                                                 cpp_w_value,
                                                                 w_res_dim_x,
                                                                 w_res_dim_y,
                                                                 quality,
                                                                 true,
                                                                 time_stamp));
                }
            }
        }
    }
    self.fill_attr_polling_buffer(dev, att_name, attr_history_stack);
}

template <>
void __fill_attr_polling_buffer_array<Tango::DEV_ENCODED>([[maybe_unused]] Tango::Util &self,
                                                          [[maybe_unused]] Tango::DeviceImpl *dev,
                                                          [[maybe_unused]] std::string &att_name,
                                                          [[maybe_unused]] py::sequence &data,
                                                          [[maybe_unused]] bool is_image) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                   "DevEncoded is only supported for SCALAR attributes.",
                                   "fill_attr_polling_buffer()");
}

template <int tangoTypeConst>
void __fill_cmd_polling_buffer_scalar(Tango::Util &self,
                                      Tango::DeviceImpl *dev,
                                      std::string &cmd_name,
                                      py::sequence &data) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    auto cmd_history_stack = Tango::CmdHistoryStack<TangoScalarType>();

    for(auto item : data) {
        py::object obj = item.cast<py::object>();

        Tango::TangoTimestamp time_stamp(__convert_time(obj.attr("time_stamp")));

        if(!obj.attr("error").is_none()) {
            Tango::DevErrorList error = obj.attr("error").cast<Tango::DevErrorList>();
            cmd_history_stack.push(Tango::TimedCmdData<TangoScalarType>(error, time_stamp));

        } else {
            std::unique_ptr<TangoScalarType> value(new TangoScalarType);
            python_scalar_to_cpp<tangoTypeConst>::convert(obj.attr("value"), *value);

            cmd_history_stack.push(Tango::TimedCmdData(value.release(), true, time_stamp));
        }
    }
    self.fill_cmd_polling_buffer(dev, cmd_name, cmd_history_stack);
}

template <>
void __fill_cmd_polling_buffer_scalar<Tango::DEV_VOID>([[maybe_unused]] Tango::Util &self,
                                                       [[maybe_unused]] Tango::DeviceImpl *dev,
                                                       [[maybe_unused]] std::string &cmd_name,
                                                       [[maybe_unused]] py::sequence &data) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForCommand",
                                   "Cannot insert history for DevVoid cmd",
                                   "fill_cmd_polling_buffer()");
}

template <int tangoArrayTypeConst>
void __fill_cmd_polling_buffer_array(Tango::Util &self,
                                     Tango::DeviceImpl *dev,
                                     std::string &cmd_name,
                                     py::sequence &data) {
    using TangoArrayType = typename TANGO_const2type(tangoArrayTypeConst);

    auto cmd_history_stack = Tango::CmdHistoryStack<TangoArrayType>();

    for(auto item : data) {
        py::object obj = item.cast<py::object>();

        Tango::TangoTimestamp time_stamp(__convert_time(obj.attr("time_stamp")));

        if(!obj.attr("error").is_none()) {
            Tango::DevErrorList error = obj.attr("error").cast<Tango::DevErrorList>();
            cmd_history_stack.push(Tango::TimedCmdData<TangoArrayType>(error, time_stamp));
        } else {
            py::object py_value = obj.attr("value");
            TangoArrayType *cpp_value = fast_convert2array<tangoArrayTypeConst>(py_value);
            cmd_history_stack.push(Tango::TimedCmdData<TangoArrayType>(cpp_value, true, time_stamp));
        }
    }
    self.fill_cmd_polling_buffer(dev, cmd_name, cmd_history_stack);
}

template <>
void __fill_cmd_polling_buffer_array<Tango::DEVVAR_STATEARRAY>([[maybe_unused]] Tango::Util &self,
                                                               [[maybe_unused]] Tango::DeviceImpl *dev,
                                                               [[maybe_unused]] std::string &cmd_name,
                                                               [[maybe_unused]] py::sequence &data) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForCommand",
                                   "For unknown reason insert history to (DevState,) commands does not supported by cppTango",
                                   "fill_cmd_polling_buffer()");
}

namespace PyUtil {

void fill_attr_polling_buffer(Tango::Util &self, Tango::DeviceImpl *dev, std::string &att_name, py::sequence &data) {
    Tango::Attribute &att = dev->get_device_attr()->get_attr_by_name(att_name.c_str());

    long type = att.get_data_type();
    Tango::AttrDataFormat format = att.get_data_format();

    const bool is_scalar = (format == Tango::SCALAR);
    const bool is_image = (format == Tango::IMAGE);

    if(is_scalar) {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type,
                                             __fill_attr_polling_buffer_scalar,
                                             self,
                                             dev,
                                             att_name,
                                             data);
    } else {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type,
                                             __fill_attr_polling_buffer_array,
                                             self,
                                             dev,
                                             att_name,
                                             data,
                                             is_image);
    }
}

void fill_cmd_polling_buffer(Tango::Util &self, Tango::DeviceImpl *dev, std::string &cmd_name, py::sequence &data) {
    Tango::CmdArgType out_type = dev->get_command(cmd_name.c_str())->get_out_type();

    TANGO_DO_ON_DEVICE_DATA_TYPE_ID(out_type,
                                    __fill_cmd_polling_buffer_scalar<tangoTypeConst>(self, dev, cmd_name, data);
                                    ,
                                    __fill_cmd_polling_buffer_array<tangoTypeConst>(self, dev, cmd_name, data););
}

void cpp_device_class_delete(Tango::DeviceClass *dev_class_ptr) {
    TANGO_LOG_DEBUG << "PyUtil::cpp_device_class_delete called" << std::endl;

    // Verify if this object was created by Python layer or Cpp layer
    // delete only objects allocated in Cpp
    // python objects will delete by pybind11 when reference count drops to 0 in python

    std::string dev_class_name = dev_class_ptr->get_name();
    TANGO_LOG_DEBUG << "PyUtil::cpp_device_class_delete checking if " << dev_class_name << " can be deleted in Cpp"
                    << std::endl;

    py::gil_scoped_acquire gil;
    PYTANGO_MOD

    py::list cpp_class_list = py::cast<py::list>(pytango.attr("get_cpp_classes")());
    size_t cl_len = py::len(cpp_class_list);
    for(size_t i = 0; i < cl_len; ++i) {
        py::tuple class_info = py::cast<py::tuple>(cpp_class_list[i]);
        std::string par_name = class_info[1].cast<std::string>();

        if(par_name == dev_class_name) {
            TANGO_LOG_DEBUG << "PyUtil::cpp_device_class_delete DeviceClass " << dev_class_name
                            << " managed by Cpp. Deleting..." << std::endl;
            delete dev_class_ptr;
            return;
        }
    }
}

void _class_factory(Tango::DServer *dserver) {
    py::gil_scoped_acquire guard;
    PYTANGO_MOD

    //
    // First, create CPP class if any. Their names are defined in a Python list
    //
    py::list cpp_class_list = pytango.attr("get_cpp_classes")();
    size_t cl_len = py::len(cpp_class_list);
    for(size_t i = 0; i < cl_len; ++i) {
        py::tuple class_info = cpp_class_list[i].cast<py::tuple>();
        std::string class_name = class_info[0].cast<std::string>();
        std::string par_name = class_info[1].cast<std::string>();
        dserver->_create_cpp_class(class_name.c_str(), par_name.c_str(), {"lib"});
    }

    //
    // Create Python classes with a call to the class_factory Python function
    //
    pytango.attr("class_factory")();

    //
    // Make all Python tango class(es) known to C++ and set the PyInterpreter state
    //
    py::list constructed_classes = pytango.attr("get_constructed_classes")();
    size_t cc_len = py::len(constructed_classes);
    for(size_t i = 0; i < cc_len; ++i) {
        Tango::DeviceClass *cpp_dc = constructed_classes[i].cast<Tango::DeviceClass *>();
        dserver->_add_class(cpp_dc);
    }
}

void server_init(Tango::Util &instance, bool with_window = false) {
    py::gil_scoped_release no_gil;
    Tango::DServer::register_class_factory(_class_factory);
    instance.server_init(with_window);
}

inline Tango::Util *init(py::object &obj) {
    // overwrite DeviceClass* delete
    // used in DServer
    // to avoid deleting objects managed by python
    Tango::wrapper_compatible_delete = cpp_device_class_delete;

    PyObject *obj_ptr = obj.ptr();
    if(PySequence_Check(obj_ptr) == 0) {
        raise_(PyExc_TypeError, param_must_be_seq);
    }

    unsigned long argc = static_cast<unsigned long>(PySequence_Length(obj_ptr));

    std::vector<std::string> arg_strings(argc);
    std::vector<char *> argv(argc);

    Tango::Util *res = nullptr;

    for(unsigned long i = 0; i < argc; ++i) {
        PyObject *item_ptr = PySequence_GetItem(obj_ptr, static_cast<Py_ssize_t>(i));
        py::str item = py::reinterpret_steal<py::str>(item_ptr);
        arg_strings[i] = item.cast<std::string>();
        argv[i] = const_cast<char *>(arg_strings[i].c_str());
    }
    res = Tango::Util::init(static_cast<int>(argc), argv.data());

    return res;
}

inline Tango::Util *instance1() {
    return Tango::Util::instance();
}

inline Tango::Util *instance2(bool b) {
    return Tango::Util::instance(b);
}

inline py::object get_device_list_by_class(Tango::Util &self, const std::string &class_name) {
    // Create a Python list to hold the device implementations
    py::list py_dev_list;

    // Get the list of device implementations from Tango::Util
    std::vector<Tango::DeviceImpl *> dev_list;
    {
        py::gil_scoped_release no_gil;
        dev_list = self.get_device_list_by_class(class_name);
    }

    // Iterate over the device implementations
    for(auto *device_impl : dev_list) {
        py_dev_list.append(py::cast(device_impl, py::return_value_policy::reference));
    }

    return py_dev_list;
}

inline py::object get_device_by_name(Tango::Util &self, const std::string &dev_name) {
    // Get the device implementation by name
    Tango::DeviceImpl *value{nullptr};
    {
        py::gil_scoped_release no_gil;
        value = self.get_device_by_name(dev_name);
    }

    // Check if the device implementation exists
    if(value == nullptr) {
        return py::none();
    }

    // Convert the device implementation to a Python object without changing ownership
    return py::cast(value, py::return_value_policy::reference);
}

inline py::list get_device_list(Tango::Util &self, const std::string &name) {
    // Create a Python list to hold the device implementations
    py::list py_dev_list;

    // Get the list of device implementations from Tango::Util
    std::vector<Tango::DeviceImpl *> dev_list;
    {
        py::gil_scoped_release no_gil;
        dev_list = self.get_device_list(name);
    }

    // Iterate over the device implementations
    for(auto *device_impl : dev_list) {
        // Convert each device implementation to a Python object without changing ownership
        py_dev_list.append(py::cast(device_impl, py::return_value_policy::reference));
    }

    // Return the Python list
    return py_dev_list;
}

inline bool event_loop() {
    py::gil_scoped_acquire guard;
    PYTANGO_MOD
    py::object py_event_loop = pytango.attr("_server_event_loop");
    py::object py_ret = py_event_loop();
    bool ret = py_ret.cast<bool>();
    return ret;
}

inline void server_set_event_loop(Tango::Util &self, py::object &py_event_loop) {
    PYTANGO_MOD
    if(py_event_loop.ptr() == Py_None) {
        self.server_set_event_loop(nullptr);
        pytango.attr("_server_event_loop") = py_event_loop;
    } else {
        pytango.attr("_server_event_loop") = py_event_loop;
        self.server_set_event_loop(event_loop);
    }
}

void set_use_db(bool use_db) {
    Tango::Util::_UseDb = use_db;
}

py::str get_dserver_ior(Tango::Util &self, Tango::DServer *dserver) {
    Tango::Device_var d = dserver->_this();
    dserver->set_d_var(Tango::Device::_duplicate(d));
    char *dserver_ior = self.get_orb()->object_to_string(d);
    py::str ret(dserver_ior);
    CORBA::string_free(dserver_ior);
    return ret;
}

py::str get_device_ior(Tango::Util &self, Tango::DeviceImpl *device) {
    char *ior = self.get_orb()->object_to_string(device->get_d_var());
    py::str ret(ior);
    CORBA::string_free(ior);
    return ret;
}

void orb_run(Tango::Util &self) {
    py::gil_scoped_release no_gil;
    self.get_orb()->run();
}

} // namespace PyUtil

void export_util(py::module_ &m) {
    py::class_<Tango::Interceptors>(m, "Interceptors")
        .def(py::init<>())
        .def("create_thread", &Tango::Interceptors::create_thread)
        .def("delete_thread", &Tango::Interceptors::delete_thread);

    using util_holder = std::unique_ptr<Tango::Util, py::nodelete>;

    py::class_<Tango::Util, util_holder>(m,
                                         "Util",
                                         py::dynamic_attr(),
                                         R"doc(
            This class is a used to store TANGO device server process data and to
                provide the user with a set of utilities method.

                This class is implemented using the singleton design pattern.
                Therefore a device server process can have only one instance of this
                class and its constructor is not public. Example::

                    util = tango.Util.instance()
                        print(util.get_host_name()))doc")
        // No constructor exposed to prevent instantiation from Python
        // Static methods
        .def(py::init([](py::object args) {
                 Tango::Util *util = PyUtil::init(args);
                 return util;
             }),
             py::return_value_policy::reference)
        .def_static("init",
                    &PyUtil::init,
                    py::return_value_policy::reference,
                    R"doc(
                        init(*args) -> Util

                           Static method that creates and gets the singleton object reference.
                           This method returns a reference to the object of the Util class.
                           If the class singleton object has not been created, it will be instantiated

                           :param str \\*args: the process commandline arguments

                           :return: :class:`Util` the tango Util object
                           :rtype: :class:`Util`)doc")
        .def_static("instance",
                    py::overload_cast<>(&PyUtil::instance1),
                    py::return_value_policy::reference,
                    R"doc(
                        instance() -> Util

                               Static method that gets the singleton object reference.
                               If the class has not been initialised with it's init method,
                               this method prints a message and aborts the device server process.

                           :returns: the tango :class:`Util` object
                           :rtype: :class:`Util`

                           :raises: :class:`DevFailed` instead of aborting if exit is set to False)doc")
        .def_static("instance",
                    py::overload_cast<bool>(&PyUtil::instance2),
                    py::return_value_policy::reference,
                    R"doc(
                        instance(exit = True) -> Util

                               Static method that gets the singleton object reference.
                               If the class has not been initialised with it's init method,
                               this method prints a message and aborts the device server process.

                           :param exit: exit or throw DevFailed
                           :type exit: bool

                           :returns: the tango :class:`Util` object
                           :rtype: :class:`Util`

                           :raises: :class:`DevFailed` instead of aborting if exit is set to False)doc",
                    py::arg("exit"))
        .def_static("set_use_db",
                    &PyUtil::set_use_db,
                    R"doc(
                        set_use_db(self) -> None

                           Set the database use Tango::Util::_UseDb flag.
                           Implemented for device server started without database usage.

                           Use with extreme care!)doc")
        // Static attributes
        .def_readonly_static("_UseDb", &Tango::Util::_UseDb)
        .def_readonly_static("_FileDb", &Tango::Util::_FileDb)
        // Methods
        .def("set_trace_level",
             &Tango::Util::set_trace_level,
             R"doc(
                set_trace_level(self, level) -> None

                        Set the process trace level.

                    Parameters :
                        - level : (int) the new process level
                    Return     : None)doc",
             py::arg("level"))
        .def("get_trace_level",
             &Tango::Util::get_trace_level,
             R"doc(
                get_trace_level(self) -> int

                        Get the process trace level.

                    Parameters : None
                    Return     : (int) the process trace level.)doc")
        .def("get_ds_inst_name",
             &Tango::Util::get_ds_inst_name,
             py::return_value_policy::copy,
             R"doc(
                get_ds_inst_name(self) -> str

                        Get a COPY of the device server instance name.

                    Parameters : None
                    Return     : (str) a COPY of the device server instance name.

                    New in PyTango 3.0.4)doc")
        .def("get_ds_exec_name",
             &Tango::Util::get_ds_exec_name,
             py::return_value_policy::copy,
             R"doc(
                get_ds_exec_name(self) -> str

                        Get a COPY of the device server executable name.

                    Parameters : None
                    Return     : (str) a COPY of the device server executable name.

                    New in PyTango 3.0.4)doc")
        .def("get_ds_name",
             &Tango::Util::get_ds_name,
             py::return_value_policy::copy,
             R"doc(
                get_ds_name(self) -> str

                        Get the device server name.
                        The device server name is the <device server executable name>/<the device server instance name>

                    Parameters : None
                    Return     : (str) device server name

                    New in PyTango 3.0.4)doc")
        .def("get_host_name",
             &Tango::Util::get_host_name,
             py::return_value_policy::copy,
             R"doc(
                get_host_name(self) -> str

                        Get the host name where the device server process is running.

                    Parameters : None
                    Return     : (str) the host name where the device server process is running

                    New in PyTango 3.0.4)doc")
        .def("get_pid_str",
             &Tango::Util::get_pid_str,
             R"doc(
                get_pid_str(self) -> str

                        Get the device server process identifier as a string.

                    Parameters : None
                    Return     : (str) the device server process identifier as a string

                    New in PyTango 3.0.4)doc")
        .def("get_pid",
             &Tango::Util::get_pid,
             R"doc(
                get_pid(self) -> TangoSys_Pid

                        Get the device server process identifier.

                    Parameters : None
                    Return     : (int) the device server process identifier)doc")
        .def("get_tango_lib_release",
             &Tango::Util::get_tango_lib_release,
             R"doc(
                get_tango_lib_release(self) -> int

                        Get the TANGO library version number.

                    Parameters : None
                    Return     : (int) The Tango library release number coded in
                                 3 digits (for instance 550,551,552,600,....))doc")
        .def("get_version_str",
             &Tango::Util::get_version_str,
             R"doc(
                get_version_str(self) -> str

                        Get the IDL TANGO version.

                    Parameters : None
                    Return     : (str) the IDL TANGO version.

                    New in PyTango 3.0.4)doc")
        .def("get_server_version",
             &Tango::Util::get_server_version,
             py::return_value_policy::copy,
             R"doc(
                get_server_version(self) -> str

                        Get the device server version.

                    Parameters : None
                    Return     : (str) the device server version.)doc")
        .def("set_server_version",
             &Tango::Util::set_server_version,
             R"doc(
                set_server_version(self, vers) -> None

                        Set the device server version.

                    Parameters :
                        - vers : (str) the device server version
                    Return     : None)doc",
             py::arg("vers"))
        .def("set_serial_model",
             &Tango::Util::set_serial_model,
             R"doc(
                set_serial_model(self, ser) -> None

                        Set the serialization model.

                    Parameters :
                        - ser : (SerialModel) the new serialization model. The serialization model must
                                be one of BY_DEVICE, BY_CLASS, BY_PROCESS or NO_SYNC
                    Return     : None)doc",
             py::arg("ser"))
        .def("get_serial_model",
             &Tango::Util::get_serial_model,
             R"doc(
                get_serial_model(self) ->SerialModel

                        Get the serialization model.

                    Parameters : None
                    Return     : (SerialModel) the serialization model)doc")
        .def("unregister_server",
             &Tango::Util::unregister_server,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                unregister_server(self) -> None

                        Unregister a device server process from the TANGO database.
                        If the database call fails, a message is displayed on the screen
                        and the process is aborted

                    Parameters : None
                    Return     : None

                    New in PyTango 7.0.0)doc")
        .def("get_dserver_device",
             &Tango::Util::get_dserver_device,
             py::return_value_policy::reference,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_dserver_device(self) -> DServer

                        Get a reference to the dserver device attached to the device server process.

                    Parameters : None
                    Return     : (DServer) the dserver device attached to the device server process

                    New in PyTango 7.0.0)doc")
        .def("server_init",
             &PyUtil::server_init,
             R"doc(
                server_init(self, with_window = False) -> None

                        Initialize all the device server pattern(s) embedded in a device server process.

                    Parameters :
                        - with_window : (bool) default value is False
                    Return     : None

                    Throws     : DevFailed If the device pattern initialistaion failed)doc",
             py::arg("with_window") = false)
        .def("server_run",
             &Tango::Util::server_run,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                server_run(self) -> None

                        Run the CORBA event loop.
                        This method runs the CORBA event loop. For UNIX or Linux operating system,
                        this method does not return. For Windows in a non-console mode, this method
                        start a thread which enter the CORBA event loop.

                    Parameters : None
                    Return     : None)doc")
        .def("server_cleanup",
             &Tango::Util::server_cleanup,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                server_cleanup(self) -> None

                    Release device server resources (EXPERT FEATURE!)

                    This method cleans up the Tango device server and relinquishes
                    all computer resources before the process exits.  It is
                    unnecessary to call this, unless Util.server_run has been bypassed.)doc")
        .def("trigger_cmd_polling",
             &Tango::Util::trigger_cmd_polling,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                trigger_cmd_polling(self, dev, name) -> None

                        Trigger polling for polled command.
                        This method send the order to the polling thread to poll one object registered
                        with an update period defined as "externally triggerred"

                    Parameters :
                        - dev : (DeviceImpl) the TANGO device
                        - name : (str) the command name which must be polled
                    Return     : None

                    Throws     : DevFailed If the call failed)doc",
             py::arg("dev"),
             py::arg("name"))
        .def("trigger_attr_polling",
             &Tango::Util::trigger_attr_polling,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                trigger_attr_polling(self, dev, name) -> None

                        Trigger polling for polled attribute.
                        This method send the order to the polling thread to poll one object registered
                        with an update period defined as "externally triggerred"

                    Parameters :
                        - dev : (DeviceImpl) the TANGO device
                        - name : (str) the attribute name which must be polled
                    Return     : None)doc",
             py::arg("dev"),
             py::arg("name"))
        .def("set_polling_threads_pool_size",
             &Tango::Util::set_polling_threads_pool_size,
             R"doc(
                set_polling_threads_pool_size(self, thread_nb) -> None

                        Set the polling threads pool size.

                    Parameters :
                        - thread_nb : (int) the maximun number of threads in the polling threads pool
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("thread_nb"))
        .def("get_polling_threads_pool_size",
             &Tango::Util::get_polling_threads_pool_size,
             R"doc(
                get_polling_threads_pool_size(self) -> int

                        Get the polling threads pool size.

                    Parameters : None
                    Return     : (int) the maximum number of threads in the polling threads pool)doc")
        .def("is_svr_starting",
             &Tango::Util::is_svr_starting,
             R"doc(
                is_svr_starting(self) -> bool

                        Check if the device server process is in its starting phase

                    Parameters : None
                    Return     : (bool) True if the server is in its starting phase

                    New in PyTango 8.0.0)doc")
        .def("is_svr_shutting_down",
             &Tango::Util::is_svr_shutting_down,
             R"doc(
                is_svr_shutting_down(self) -> bool

                        Check if the device server process is in its shutting down sequence

                    Parameters : None
                    Return     : (bool) True if the server is in its shutting down phase.

                    New in PyTango 8.0.0)doc")
        .def("is_device_restarting",
             &Tango::Util::is_device_restarting,
             R"doc(
                is_device_restarting(self, dev_name) -> bool

                        Check if the device is actually restarted by the device server
                        process admin device with its DevRestart command

                    Parameters :
                        dev_name : (str) device name
                    Return     : (bool) True if the device is restarting.

                    New in PyTango 8.0.0)doc",
             py::arg("dev_name"))
        .def("get_sub_dev_diag",
             &Tango::Util::get_sub_dev_diag,
             py::return_value_policy::reference_internal,
             R"doc(
                get_sub_dev_diag(self) -> SubDevDiag

                        Get the internal sub device manager

                    Parameters : None
                    Return     : (SubDevDiag) the sub device manager

                    New in PyTango 7.0.0)doc")
        .def("connect_db",
             &Tango::Util::connect_db,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                connect_db(self) -> None

                        Connect the process to the TANGO database.
                        If the connection to the database failed, a message is
                        displayed on the screen and the process is aborted

                    Parameters : None
                    Return     : None)doc")
        .def("get_database",
             &Tango::Util::get_database,
             py::return_value_policy::reference_internal,
             R"doc(
                get_database(self) -> Database

                        Get a reference to the TANGO database object

                    Parameters : None
                    Return     : (Database) the database

                    New in PyTango 7.0.0)doc")
        .def("reset_filedatabase",
             &Tango::Util::reset_filedatabase,
             R"doc(
                reset_filedatabase(self) -> None

                        Reread the file database.

                    Parameters : None
                    Return     : None)doc")
        .def("get_device_list_by_class",
             &PyUtil::get_device_list_by_class,
             R"doc(
                get_device_list_by_class(self, class_name) -> sequence<DeviceImpl>

                        Get the list of device references for a given TANGO class.
                        Return the list of references for all devices served by one implementation
                        of the TANGO device pattern implemented in the process.

                    Parameters :
                        - class_name : (str) The TANGO device class name

                    Return     : (sequence<DeviceImpl>) The device reference list

                    New in PyTango 7.0.0)doc",
             py::arg("class_name"))
        .def("get_device_by_name",
             &PyUtil::get_device_by_name,
             R"doc(
                get_device_by_name(self, dev_name) -> DeviceImpl

                        Get a device reference from its name

                    Parameters :
                        - dev_name : (str) The TANGO device name
                    Return     : (DeviceImpl) The device reference

                    New in PyTango 7.0.0)doc",
             py::arg("dev_name"))
        .def("get_device_list",
             &PyUtil::get_device_list,
             R"doc(
                get_device_list(self) -> sequence<DeviceImpl>

                        Get device list from name.
                        It is possible to use a wild card ('*') in the name parameter
                        (e.g. "*", "/tango/tangotest/n*", ...)

                    Parameters : None
                    Return     : (sequence<DeviceImpl>) the list of device objects

                    New in PyTango 7.0.0)doc")
        .def("server_set_event_loop",
             &PyUtil::server_set_event_loop,
             R"doc(
                server_set_event_loop(self, event_loop) -> None

                    This method registers an event loop function in a Tango server.
                    This function will be called by the process main thread in an infinite loop
                    The process will not use the classical ORB blocking event loop.
                    It is the user responsibility to code this function in a way that it implements
                    some kind of blocking in order not to load the computer CPU. The following
                    piece of code is an example of how you can use this feature::

                        _LOOP_NB = 1
                        def looping():
                            global _LOOP_NB
                            print "looping", _LOOP_NB
                            time.sleep(0.1)
                            _LOOP_NB += 1
                            return _LOOP_NB > 100

                        def main():
                            util = tango.Util(sys.argv)

                            # ...

                            U = tango.Util.instance()
                            U.server_set_event_loop(looping)
                            U.server_init()
                            U.server_run()

                    Parameters : None
                    Return     : None

                    New in PyTango 8.1.0)doc",
             py::arg("event_loop"))
        .def("set_interceptors", &Tango::Util::set_interceptors, py::arg("interceptors"))
        .def("get_dserver_ior",
             &PyUtil::get_dserver_ior,
             R"doc(
                get_dserver_ior(self, device_server) -> str

                    Get the CORBA Interoperable Object Reference (IOR) associated with the device server

                    :param device_server: :class:`DServer` device object
                    :type device_server: :class:`DServer`

                    :return: the associated CORBA object reference
                    :rtype: str)doc",
             py::arg("device_server"))
        .def("get_device_ior",
             &PyUtil::get_device_ior,
             R"doc(
                get_device_ior(self, device) -> str

                    Get the CORBA Interoperable Object Reference (IOR) associated with the device

                    :param device: :class:`tango.LatestDeviceImpl` device object
                    :type device: :class:`tango.LatestDeviceImpl`

                    :return: the associated CORBA object reference
                    :rtype: str)doc",
             py::arg("device"))
        .def("orb_run",
             &PyUtil::orb_run,
             R"doc(
                orb_run(self) -> None

                        Run the CORBA event loop directly (EXPERT FEATURE!)

                        This method runs the CORBA event loop.  It may be useful if the
                        Util.server_run method needs to be bypassed.  Normally, that method
                        runs the CORBA event loop.

                    :return: None
                    :rtype: None)doc")
        .def("is_auto_alarm_on_change_event",
             &Tango::Util::is_auto_alarm_on_change_event,
             R"doc(
                is_auto_alarm_on_change_event(self) -> bool

                    Returns True if alarm events are automatically pushed to subscribers when a device
                    pushes a change event, and the attribute quality has changed to or from alarm.

                    Can be configured in two ways:

                      - via the ``CtrlSystem`` free Tango database property
                        ``AutoAlarmOnChangeEvent`` (set to true or false),
                      - by calling the :meth:`tango.Util.set_auto_alarm_on_change_event`.

                    :return: True if alarm events are automatically pushed to subscribers when a device
                        pushes a change event
                    :rtype: bool

                    .. versionadded:: 10.0.0)doc")
        .def("set_auto_alarm_on_change_event",
             &Tango::Util::set_auto_alarm_on_change_event,
             R"doc(
                set_auto_alarm_on_change_event(self, enabled) -> None

                    Toggles if alarm events are automatically pushed - see
                    :meth:`tango.Util.is_auto_alarm_on_change_event`.

                    This method takes priority over the value of the free property in the Tango database.

                    :param enabled: if True - the alarm event will be emitted with change event, if there is quality change to or from alarm
                    :type enabled: bool

                    :return: None
                    :rtype: None

                    .. versionadded:: 10.0.0)doc",
             py::arg("value"))
        .def("_fill_attr_polling_buffer",
             &PyUtil::fill_attr_polling_buffer,
             py::arg("dev"),
             py::arg("att_name"),
             py::arg("data"))
        .def("_fill_cmd_polling_buffer",
             &PyUtil::fill_cmd_polling_buffer,
             py::arg("dev"),
             py::arg("cmd_name"),
             py::arg("data"));
}
