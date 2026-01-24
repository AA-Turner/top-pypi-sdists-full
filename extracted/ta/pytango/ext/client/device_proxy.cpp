/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "pyutils.h"
#include "convertors/type_casters.h"

#include "client/device_attribute.h"
#include "client/callback.h"

namespace PyDeviceProxy {

static inline void pylist_to_devattrs(Tango::DeviceProxy &self,
                                      py::object &py_list,
                                      std::vector<Tango::DeviceAttribute> &dev_attrs) {
    unsigned long u_size = len(py_list);

    std::vector<py::object> py_values;
    py_values.reserve(u_size);

    // This will hold the final, complete list of attribute configurations.
    std::vector<Tango::AttributeInfoEx> attr_infos(u_size);

    // These store the names we need to fetch and their original indices.
    std::vector<std::string> attr_names_to_fetch;
    std::vector<unsigned long> indices_to_fill;

    // 1. First pass: sort items into those we have info for and those we need to fetch.
    for(unsigned long n = 0; n < u_size; ++n) {
        // Use py::tuple for safer and cleaner element access
        py::tuple tup = py_list.attr("__getitem__")(n);
        py::object first_item = tup[0];
        py_values.push_back(tup[1]); // The value is always the second item

        try {
            // Try to cast the first item to Tango::AttributeInfoEx.
            // If it succeeds, we have the info directly.
            attr_infos[n] = first_item.cast<Tango::AttributeInfoEx>();
        } catch(const py::cast_error &) {
            // If casting fails, assume it's an attribute name (std::string).
            // Store the name and the original index `n` for later processing.
            attr_names_to_fetch.push_back(first_item.cast<std::string>());
            indices_to_fill.push_back(n);
        }
    }

    // 2. If we collected any names, fetch their configuration in a single batch call.
    if(!attr_names_to_fetch.empty()) {
        std::unique_ptr<Tango::AttributeInfoListEx> fetched_info_list;
        {
            py::gil_scoped_release no_gil;
            fetched_info_list.reset(self.get_attribute_config_ex(attr_names_to_fetch));
        }

        // 3. With the results, fill the gaps in our main attr_infos vector.
        for(size_t i = 0; i < fetched_info_list->size(); ++i) {
            unsigned long original_index = indices_to_fill[i];
            attr_infos[original_index] = (*fetched_info_list)[i];
        }
    }

    // 4. Now that attr_infos is complete, prepare the final dev_attrs vector.
    dev_attrs.resize(u_size);
    for(unsigned long n = 0; n < u_size; ++n) {
        PyDeviceAttribute::reset(dev_attrs[n], attr_infos[n], py_values[n]);
    }
}

static py::object read_attribute(Tango::DeviceProxy &self,
                                 const std::string &attr_name,
                                 PyTango::ExtractAs extract_as) {
    // Even if there's an exception in convert_to_python, the
    // DeviceAttribute will be deleted there, so we don't need to worry.
    Tango::DeviceAttribute *dev_attr = nullptr;
    {
        py::gil_scoped_release no_gil;
        dev_attr = new Tango::DeviceAttribute(self.read_attribute(attr_name.c_str()));
    }
    return PyDeviceAttribute::convert_to_python(dev_attr, self, extract_as);
}

static inline py::object read_attributes(Tango::DeviceProxy &self,
                                         py::object py_attr_names,
                                         PyTango::ExtractAs extract_as) {
    StdStringVector attr_names = py_attr_names.cast<StdStringVector>();

    PyDeviceAttribute::AutoDevAttrVector dev_attr_vec;
    {
        py::gil_scoped_release no_gil;
        dev_attr_vec.reset(self.read_attributes(attr_names));
    }

    return PyDeviceAttribute::convert_to_python(dev_attr_vec, self, extract_as);
}

static inline void write_attribute(Tango::DeviceProxy &self,
                                   const Tango::AttributeInfo &attr_info,
                                   py::object py_value) {
    Tango::DeviceAttribute da;
    PyDeviceAttribute::reset(da, attr_info, py_value);

    py::gil_scoped_release no_gil;
    self.write_attribute(da);
}

static inline void write_attribute(Tango::DeviceProxy &self,
                                   const std::string &attr_name,
                                   py::object py_value) {
    Tango::DeviceAttribute dev_attr;
    PyDeviceAttribute::reset(dev_attr, attr_name, self, py_value);

    py::gil_scoped_release no_gil;
    self.write_attribute(dev_attr);
}

static inline void write_attributes(Tango::DeviceProxy &self,
                                    py::object py_list) {
    std::vector<Tango::DeviceAttribute> dev_attrs;
    pylist_to_devattrs(self, py_list, dev_attrs);

    py::gil_scoped_release no_gil;
    self.write_attributes(dev_attrs);
}

static inline py::object write_read_attribute(Tango::DeviceProxy &self,
                                              const std::string &attr_name,
                                              py::object py_value,
                                              PyTango::ExtractAs extract_as) {
    Tango::DeviceAttribute w_dev_attr;
    std::unique_ptr<Tango::DeviceAttribute> r_dev_attr;

    // Prepare dev_attr structure
    PyDeviceAttribute::reset(w_dev_attr, attr_name, self, py_value);

    // Do the actual write_read_attribute thing...
    {
        py::gil_scoped_release no_gil;
        Tango::DeviceAttribute da = self.write_read_attribute(w_dev_attr);
        r_dev_attr = std::make_unique<Tango::DeviceAttribute>(da);
    }

    // Convert the result back to python
    return PyDeviceAttribute::convert_to_python(r_dev_attr.release(), self, extract_as);
}

static py::object write_read_attributes(Tango::DeviceProxy &self,
                                        py::object py_name_val_list,
                                        py::object py_attr_names,
                                        PyTango::ExtractAs extract_as) {
    // Convert write
    std::vector<Tango::DeviceAttribute> dev_attrs;
    pylist_to_devattrs(self, py_name_val_list, dev_attrs);

    // Convert read
    StdStringVector attr_names = py_attr_names.cast<StdStringVector>();
    PyDeviceAttribute::AutoDevAttrVector dev_attr_vec;

    // Do the actual write_read_attributes thing...
    {
        py::gil_scoped_release no_gil;
        dev_attr_vec.reset(self.write_read_attributes(dev_attrs, attr_names));
    }

    // Convert the result back to python
    return PyDeviceAttribute::convert_to_python(dev_attr_vec, self, extract_as);
}

static py::object command_history(Tango::DeviceProxy &self,
                                  const std::string &cmd_name,
                                  int depth) {
    std::vector<Tango::DeviceDataHistory> *device_data_hist = nullptr;
    py::list ret;
    {
        py::gil_scoped_release no_gil;
        device_data_hist = self.command_history(const_cast<std::string &>(cmd_name), depth);
    }
    auto it = device_data_hist->begin();
    for(; it != device_data_hist->end(); ++it) {
        Tango::DeviceDataHistory &hist = *it;
        ret.append(hist);
    }
    delete device_data_hist;
    return ret;
}

static inline py::object attribute_history(Tango::DeviceProxy &self,
                                           const std::string &attr_name,
                                           int depth,
                                           PyTango::ExtractAs extract_as) {
    std::unique_ptr<std::vector<Tango::DeviceAttributeHistory>> att_hist;
    {
        py::gil_scoped_release no_gil;
        att_hist.reset(self.attribute_history(const_cast<std::string &>(attr_name), depth));
    }
    return PyDeviceAttribute::convert_to_python(att_hist, self, extract_as);
}

static inline void read_attributes_asynch(Tango::DeviceProxy &self,
                                          py::object py_attr_names,
                                          py::object py_cb,
                                          PyTango::ExtractAs extract_as) {
    StdStringVector attr_names = py_attr_names.cast<StdStringVector>();

    PyCallBackAutoDie *cb = py_cb.cast<PyCallBackAutoDie *>();
    cb->set_extract_as(extract_as);

    py::gil_scoped_release no_gil;
    try {
        self.read_attributes_asynch(attr_names, *cb);
    } catch(...) {
        cb->delete_me();
        throw;
    }
}

static inline py::object read_attributes_reply(Tango::DeviceProxy &self,
                                               long id,
                                               PyTango::ExtractAs extract_as) {
    PyDeviceAttribute::AutoDevAttrVector dev_attr_vec;
    {
        py::gil_scoped_release no_gil;
        dev_attr_vec.reset(self.read_attributes_reply(id));
    }
    return PyDeviceAttribute::convert_to_python(dev_attr_vec, self, extract_as);
}

static inline py::object read_attributes_reply(Tango::DeviceProxy &self,
                                               long id,
                                               long timeout,
                                               PyTango::ExtractAs extract_as) {
    PyDeviceAttribute::AutoDevAttrVector dev_attr_vec;
    {
        py::gil_scoped_release no_gil;
        dev_attr_vec.reset(self.read_attributes_reply(id, timeout));
    }
    return PyDeviceAttribute::convert_to_python(dev_attr_vec, self, extract_as);
}

static inline long write_attributes_asynch(Tango::DeviceProxy &self,
                                           py::object py_list) {
    std::vector<Tango::DeviceAttribute> dev_attrs;
    pylist_to_devattrs(self, py_list, dev_attrs);

    py::gil_scoped_release no_gil;
    return self.write_attributes_asynch(dev_attrs);
}

static inline void write_attributes_asynch(Tango::DeviceProxy &self,
                                           py::object py_list,
                                           py::object py_cb) {
    std::vector<Tango::DeviceAttribute> dev_attrs;
    pylist_to_devattrs(self, py_list, dev_attrs);

    PyCallBackAutoDie *cb = py_cb.cast<PyCallBackAutoDie *>();

    py::gil_scoped_release no_gil;
    try {
        self.write_attributes_asynch(dev_attrs, *cb);
    } catch(...) {
        cb->delete_me();
        throw;
    }
}

static inline void write_attributes_reply(Tango::DeviceProxy &self,
                                          long id,
                                          long timestamp) {
    py::gil_scoped_release no_gil;
    self.write_attributes_reply(id, timestamp);
}

static inline void write_attributes_reply(Tango::DeviceProxy &self,
                                          long id) {
    py::gil_scoped_release no_gil;
    self.write_attributes_reply(id);
}

// Overload for the "old" case with stateless flag
static int subscribe_event_global_with_stateless_flag(py::object py_self,
                                                      Tango::EventType event,
                                                      py::object py_cb,
                                                      bool stateless) {
    Tango::DeviceProxy &self = py_self.cast<Tango::DeviceProxy &>();

    PyEventCallBack *cb = nullptr;
    try {
        cb = py_cb.cast<PyEventCallBack *>();
    } catch(const py::cast_error &) {
        Tango::Except::throw_exception("PyDs_CastError",
                                       "Cannot cast callback to PyEventCallBack",
                                       "subscribe_event");
    }

    {
        py::gil_scoped_release no_gil;
        return self.subscribe_event(event, cb, stateless);
    }
}

// Overload for the "new" case if EventSubMode is specified
static int subscribe_event_global_with_sub_mode(py::object py_self,
                                                Tango::EventType event,
                                                py::object py_cb,
                                                Tango::EventSubMode event_sub_mode) {
    Tango::DeviceProxy &self = py_self.cast<Tango::DeviceProxy &>();

    PyEventCallBack *cb = nullptr;
    try {
        cb = py_cb.cast<PyEventCallBack *>();
    } catch(const py::cast_error &) {
        Tango::Except::throw_exception("PyDs_CastError",
                                       "Cannot cast callback to PyEventCallBack",
                                       "subscribe_event");
    }

    {
        py::gil_scoped_release no_gil;
        return self.subscribe_event(event, cb, event_sub_mode);
    }
}

// Overload for the "old" case with stateless flag
static int subscribe_event_attrib_with_stateless_flag(py::object py_self,
                                                      const std::string &attr_name,
                                                      Tango::EventType event,
                                                      py::object py_cb_or_queuesize,
                                                      bool stateless,
                                                      PyTango::ExtractAs extract_as,
                                                      py::object &py_filters) {
    Tango::DeviceProxy &self = py_self.cast<Tango::DeviceProxy &>();
    StdStringVector filters = py_filters.cast<StdStringVector>();

    PyEventCallBack *cb = nullptr;
    int event_queue_size = 0;
    try {
        cb = py_cb_or_queuesize.cast<PyEventCallBack *>();
        cb->set_extract_as(extract_as);

        {
            py::gil_scoped_release no_gil;
            return self.subscribe_event(attr_name, event, cb, filters, stateless);
        }
    } catch(const py::cast_error &) {
        event_queue_size = py_cb_or_queuesize.cast<int>();
        {
            py::gil_scoped_release no_gil;
            return self.subscribe_event(attr_name, event, event_queue_size, filters, stateless);
        }
    }
}

// Overload for the "new" case if EventSubMode is specified
static int subscribe_event_attrib_with_sub_mode(py::object py_self,
                                                const std::string &attr_name,
                                                Tango::EventType event,
                                                py::object py_cb_or_queuesize,
                                                Tango::EventSubMode event_sub_mode,
                                                PyTango::ExtractAs extract_as) {
    Tango::DeviceProxy &self = py_self.cast<Tango::DeviceProxy &>();

    PyEventCallBack *cb = nullptr;
    int event_queue_size = 0;
    try {
        cb = py_cb_or_queuesize.cast<PyEventCallBack *>();
        cb->set_extract_as(extract_as);

        {
            py::gil_scoped_release no_gil;
            return self.subscribe_event(attr_name, event, cb, event_sub_mode);
        }
    } catch(const py::cast_error &) {
        event_queue_size = py_cb_or_queuesize.cast<int>();
        {
            py::gil_scoped_release no_gil;
            return self.subscribe_event(attr_name, event, event_queue_size, event_sub_mode);
        }
    }
}

template <typename ED, typename EDList>
static py::object get_events__aux(py::object py_self,
                                  int event_id,
                                  PyTango::ExtractAs extract_as = PyTango::ExtractAsNumpy) {
    Tango::DeviceProxy &self = py_self.cast<Tango::DeviceProxy &>();

    EDList event_list;
    self.get_events(event_id, event_list);

    py::list r;

    for(size_t i = 0; i < event_list.size(); ++i) {
        ED *event_data = event_list[i];

        py::object py_ev = py::cast(event_data, py::return_value_policy::take_ownership);

        // EventDataList deletes EventData's on destructor, so once
        // we are handling it somewhere else (as an py::object) we must
        // unset the reference
        event_list[i] = nullptr;

        PyEventCallBack::fill_py_event(event_data, py_ev, extract_as);

        r.append(py_ev);
    }
    return r;
}

static void get_events__callback(py::object py_self,
                                 int event_id,
                                 PyEventCallBack *cb,
                                 PyTango::ExtractAs extract_as) {
    Tango::DeviceProxy &self = py_self.cast<Tango::DeviceProxy &>();
    cb->set_extract_as(extract_as);
    self.get_events(event_id, cb);
}

static py::object get_events__attr_conf(py::object py_self,
                                        int event_id) {
    return get_events__aux<Tango::AttrConfEventData, Tango::AttrConfEventDataList>(py_self, event_id);
}

static py::object get_events__data(py::object py_self,
                                   int event_id,
                                   PyTango::ExtractAs extract_as) {
    return get_events__aux<Tango::EventData, Tango::EventDataList>(py_self, event_id, extract_as);
}

static py::object get_events__data_ready(py::object py_self,
                                         int event_id) {
    return get_events__aux<Tango::DataReadyEventData, Tango::DataReadyEventDataList>(py_self, event_id);
}

static py::object get_events__devintr_change_data(py::object py_self,
                                                  int event_id,
                                                  PyTango::ExtractAs extract_as) {
    return get_events__aux<Tango::DevIntrChangeEventData, Tango::DevIntrChangeEventDataList>(py_self, event_id, extract_as);
}

std::shared_ptr<Tango::DeviceProxy> device_proxy_init() {
    py::gil_scoped_release no_gil;
    return std::shared_ptr<Tango::DeviceProxy>(
        new Tango::DeviceProxy(),
        DeleterWithoutGIL());
}

std::shared_ptr<Tango::DeviceProxy> device_proxy_init(const std::string &name) {
    py::gil_scoped_release no_gil;
    return std::shared_ptr<Tango::DeviceProxy>(
        new Tango::DeviceProxy(name.c_str()),
        DeleterWithoutGIL());
}

std::shared_ptr<Tango::DeviceProxy> device_proxy_init(const std::string &name, bool ch_acc) {
    py::gil_scoped_release no_gil;
    return std::shared_ptr<Tango::DeviceProxy>(
        new Tango::DeviceProxy(name.c_str(), ch_acc),
        DeleterWithoutGIL());
}

std::shared_ptr<Tango::DeviceProxy> device_proxy_init(const Tango::DeviceProxy &device) {
    py::gil_scoped_release no_gil;
    return std::shared_ptr<Tango::DeviceProxy>(
        new Tango::DeviceProxy(device),
        DeleterWithoutGIL());
}
} // namespace PyDeviceProxy

void export_device_proxy(py::module &m) {
    py::class_<Tango::DeviceProxy,
               std::shared_ptr<Tango::DeviceProxy>,
               Tango::Connection>(m,
                                  "DeviceProxy",
                                  py::dynamic_attr(),
                                  R"doc(
    DeviceProxy is the high level Tango object which provides the client with
    an easy-to-use interface to TANGO devices. DeviceProxy provides interfaces
    to all TANGO Device interfaces.The DeviceProxy manages timeouts, stateless
    connections and reconnection if the device server is restarted. To create
    a DeviceProxy, a Tango Device name must be set in the object constructor.

    Example :
       dev = tango.DeviceProxy("sys/tg_test/1")

    DeviceProxy(dev_name, green_mode=None, wait=True, timeout=True) -> DeviceProxy
    DeviceProxy(self, dev_name, need_check_acc, green_mode=None, wait=True, timeout=True) -> DeviceProxy

    Creates a new :class:`~tango.DeviceProxy`.

    :param dev_name: the device name or alias
    :type dev_name: str
    :param need_check_acc: in first version of the function it defaults to True.
                           Determines if at creation time of DeviceProxy it should check
                           for channel access (rarely used)
    :type need_check_acc: bool
    :param green_mode: determines the mode of execution of the device (including.
                      the way it is created). Defaults to the current global
                      green_mode (check :func:`~tango.get_green_mode` and
                      :func:`~tango.set_green_mode`)
    :type green_mode: :obj:`~tango.GreenMode`
    :param wait: whether or not to wait for result. If green_mode
                 Ignored when green_mode is Synchronous (always waits).
    :type wait: bool
    :param timeout: The number of seconds to wait for the result.
                    If None, then there is no limit on the wait time.
                    Ignored when green_mode is Synchronous or wait is False.
    :type timeout: float
    :returns:
        if green_mode is Synchronous or wait is True:
            :class:`~tango.DeviceProxy`
        elif green_mode is Futures:
            :class:`concurrent.futures.Future`
        elif green_mode is Gevent:
            :class:`gevent.event.AsynchResult`
        elif green_mode is Asyncio:
            :class:`asyncio.Future`
    :throws:
        * :class:`~tango.DevFailed` if green_mode is Synchronous or wait is True
          and there is an error creating the device.
        * :class:`concurrent.futures.TimeoutError` if green_mode is Futures,
          wait is False, timeout is not None and the time to create the device
          has expired.
        * :class:`gevent.timeout.Timeout` if green_mode is Gevent, wait is False,
          timeout is not None and the time to create the device has expired.
        * :class:`asyncio.TimeoutError`` if green_mode is Asyncio,
          wait is False, timeout is not None and the time to create the device
          has expired.

    .. versionadded:: 8.1.0
        *green_mode* parameter.
        *wait* parameter.
        *timeout* parameter.
)doc")
        .def(py::init([]() {
            return PyDeviceProxy::device_proxy_init();
        }))
        .def(py::init([](const std::string &name) {
                 return PyDeviceProxy::device_proxy_init(name);
             }),
             py::arg("name"))
        .def(py::init([](const std::string &name, bool ch_acc) {
                 return PyDeviceProxy::device_proxy_init(name, ch_acc);
             }),
             py::arg("name"),
             py::arg("ch_acc"))
        .def(py::init([](const Tango::DeviceProxy &device) {
                 return PyDeviceProxy::device_proxy_init(device);
             }),
             py::arg("device"))

        .def(py::pickle(
            [](Tango::DeviceProxy &self) { // __getstate__
                std::string ret = self.get_db_host() + ":" + self.get_db_port() + "/" + self.dev_name();
                return py::make_tuple(ret);
            },
            [](py::tuple py_tuple) { // __setstate__
                if(py_tuple.size() != 1) {
                    throw std::runtime_error("Invalid state!");
                }
                std::string trl = py_tuple[0].cast<std::string>();
                return Tango::DeviceProxy(trl.c_str());
            }))

        //
        // general methods
        //
        .def("dev_name", &Tango::DeviceProxy::dev_name)

        .def("info",
             &Tango::DeviceProxy::info,
             py::return_value_policy::reference_internal,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                info(self) -> DeviceInfo

                        A method which returns information on the device

                    Parameters : None
                    Return     : (DeviceInfo) object
                    Example    :
                            dev_info = dev.info()
                            print(dev_info.dev_class)
                            print(dev_info.server_id)
                            print(dev_info.server_host)
                            print(dev_info.server_version)
                            print(dev_info.doc_url)
                            print(dev_info.dev_type)
                            print(dev_info.version_info))doc")

        .def("get_device_db",
             &Tango::DeviceProxy::get_device_db,
             py::return_value_policy::reference,
             R"doc(
                get_device_db(self) -> Database

                        Returns the internal database reference

                    Parameters : None
                    Return     : (Database) object

                    New in PyTango 7.0.0)doc")

        .def("_status", &Tango::DeviceProxy::status, py::return_value_policy::reference_internal, py::call_guard<py::gil_scoped_release>())

        .def("_state", &Tango::DeviceProxy::state, py::call_guard<py::gil_scoped_release>())

        .def("adm_name",
             &Tango::DeviceProxy::adm_name,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                adm_name(self) -> str

                        Return the name of the corresponding administrator device. This is
                        useful if you need to send an administration command to the device
                        server, e.g restart it

                    New in PyTango 3.0.4)doc")

        .def("description",
             &Tango::DeviceProxy::description,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                description(self) -> str

                        Get device description.

                    Parameters : None
                    Return     : (str) describing the device)doc")

        .def("name",
             &Tango::DeviceProxy::name,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                name(self) -> str

                    Return the device name from the device itself.

                Return: (str) device name)doc")

        .def("alias",
             &Tango::DeviceProxy::alias,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                alias(self) -> str

                        Return the device alias if one is defined.
                        Otherwise, throws exception.

                    Return: (str) device alias)doc")

        .def("get_tango_lib_version",
             &Tango::DeviceProxy::get_tango_lib_version,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_tango_lib_version(self) -> int

                        Returns the Tango lib version number used by the remote device
                        Otherwise, throws exception.

                    Return     : (int) The device Tango lib version as a 3 or 4 digits number.
                                 Possible return value are: 100,200,500,520,700,800,810,...

                    New in PyTango 8.1.0)doc")

        .def("_ping", &Tango::DeviceProxy::ping, py::call_guard<py::gil_scoped_release>())

        .def("black_box",
             &Tango::DeviceProxy::black_box,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                black_box(self, n) -> sequence<str>

                        Get the last commands executed on the device server

                    Parameters :
                        - n : n number of commands to get
                    Return     : (sequence<str>) sequence of strings containing the date, time,
                                 command and from which client computer the command
                                 was executed
                    Example :
                            print(black_box(4)))doc",
             py::arg("n"))

        //
        // command methods
        //
        .def("get_command_list",
             &Tango::DeviceProxy::get_command_list,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_command_list(self) -> sequence<str>

                        Return the names of all commands implemented for this device.

                    Parameters : None
                    Return     : sequence<str>

                    Throws     : ConnectionFailed, CommunicationFailed,
                                 DevFailed from device)doc")

        .def("_get_command_config",
             py::overload_cast<StdStringVector &>(&Tango::DeviceProxy::get_command_config),
             py::arg("attr_names"),
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>())

        .def("_get_command_config",
             py::overload_cast<const std::string &>(&Tango::DeviceProxy::get_command_config),
             py::arg("attr_name"),
             py::call_guard<py::gil_scoped_release>())

        .def("command_query",
             &Tango::DeviceProxy::command_query,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                command_query(self, command) -> CommandInfo

                        Query the device for information about a single command.

                    Parameters :
                            - command : (str) command name
                    Return     : (CommandInfo) object
                    Throws     : ConnectionFailed, CommunicationFailed, DevFailed from device
                    Example :
                            com_info = dev.command_query("DevString")
                            print(com_info.cmd_name)
                            print(com_info.cmd_tag)
                            print(com_info.in_type)
                            print(com_info.out_type)
                            print(com_info.in_type_desc)
                            print(com_info.out_type_desc)
                            print(com_info.disp_level)

                    See CommandInfo documentation string form more detail)doc",
             py::arg("command"))

        .def("command_list_query",
             &Tango::DeviceProxy::command_list_query,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                command_list_query(self) -> sequence<CommandInfo>

                        Query the device for information on all commands.

                    Parameters : None
                    Return     : (CommandInfoList) Sequence of CommandInfo objects)doc")

        .def("import_info",
             &Tango::DeviceProxy::import_info,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                import_info(self) -> DbDevImportInfo

                        Query the device for import info from the database.

                    Parameters : None
                    Return     : (DbDevImportInfo)
                    Example :
                            dev_import = dev.import_info()
                            print(dev_import.name)
                            print(dev_import.exported)
                            print(dev_ior.ior)
                            print(dev_version.version)

                    All DbDevImportInfo fields are strings except for exported which
                    is an integer")doc")

        //
        // property methods
        //
        .def("_get_property",
             py::overload_cast<const std::string &, Tango::DbData &>(&Tango::DeviceProxy::get_property),
             py::arg("propname"),
             py::arg("propdata"),
             py::call_guard<py::gil_scoped_release>())

        .def("_get_property",
             py::overload_cast<const std::vector<std::string> &, Tango::DbData &>(&Tango::DeviceProxy::get_property),
             py::arg("propnames"),
             py::arg("propdata"),
             py::call_guard<py::gil_scoped_release>())

        .def("_get_property",
             py::overload_cast<Tango::DbData &>(&Tango::DeviceProxy::get_property),
             py::arg("propdata"),
             py::call_guard<py::gil_scoped_release>())

        .def("_put_property",
             &Tango::DeviceProxy::put_property,
             py::arg("propdata"),
             py::call_guard<py::gil_scoped_release>())

        .def("_delete_property",
             py::overload_cast<const Tango::DbData &>(&Tango::DeviceProxy::delete_property),
             py::arg("propname"),
             py::call_guard<py::gil_scoped_release>())

        .def("_get_property_list",
             &Tango::DeviceProxy::get_property_list,
             py::arg("filter"),
             py::arg("array"),
             py::call_guard<py::gil_scoped_release>())

        //
        // attribute methods
        //

        .def("get_attribute_list",
             &Tango::DeviceProxy::get_attribute_list,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_attribute_list(self) -> sequence<str>

                        Return the names of all attributes implemented for this device.

                    Parameters : None
                    Return     : sequence<str>

                    Throws     : ConnectionFailed, CommunicationFailed,
                                 DevFailed from device)doc")

        .def("_get_attribute_config",
             py::overload_cast<const StdStringVector &>(&Tango::DeviceProxy::get_attribute_config),
             py::arg("attr_names"),
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>())

        .def("_get_attribute_config",
             py::overload_cast<const std::string &>(&Tango::DeviceProxy::get_attribute_config),
             py::arg("attr_name"),
             py::call_guard<py::gil_scoped_release>())

        .def("_get_attribute_config_ex",
             &Tango::DeviceProxy::get_attribute_config_ex,
             py::arg("attr_names"),
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>())

        .def("attribute_query",
             &Tango::DeviceProxy::attribute_query,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                attribute_query(self, attr_name) -> AttributeInfoEx

                        Query the device for information about a single attribute.

                    Parameters :
                            - attr_name :(str) the attribute name
                    Return     : (AttributeInfoEx) containing the attribute
                                 configuration

                    Throws     : ConnectionFailed, CommunicationFailed,
                                 DevFailed from device)doc",
             py::arg("attr_name"))

        .def("attribute_list_query",
             &Tango::DeviceProxy::attribute_list_query,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                attribute_list_query(self) -> sequence<AttributeInfo>

                        Query the device for info on all attributes. This method returns
                        a sequence of tango.AttributeInfo.

                    Parameters : None
                    Return     : (sequence<AttributeInfo>) containing the
                                 attributes configuration

                    Throws     : ConnectionFailed, CommunicationFailed,
                                 DevFailed from device)doc")

        .def("attribute_list_query_ex",
             &Tango::DeviceProxy::attribute_list_query_ex,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                attribute_list_query_ex(self) -> sequence<AttributeInfoEx>

                        Query the device for info on all attributes. This method returns
                        a sequence of tango.AttributeInfoEx.

                    Parameters : None
                    Return     : (sequence<AttributeInfoEx>) containing the
                                 attributes configuration

                    Throws     : ConnectionFailed, CommunicationFailed,
                                 DevFailed from device)doc")

        .def("_set_attribute_config",
             py::overload_cast<const Tango::AttributeInfoList &>(&Tango::DeviceProxy::set_attribute_config),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("seq"))

        .def("_set_attribute_config",
             py::overload_cast<const Tango::AttributeInfoListEx &>(&Tango::DeviceProxy::set_attribute_config),
             py::call_guard<py::gil_scoped_release>(),
             py::arg("seq"))

        .def("_read_attribute",
             &PyDeviceProxy::read_attribute,
             py::arg("attr_name"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("_read_attributes",
             &PyDeviceProxy::read_attributes,
             py::arg("attr_names"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("_write_attribute",
             py::overload_cast<Tango::DeviceProxy &, const std::string &, py::object>(&PyDeviceProxy::write_attribute),
             py::arg("attr_name"),
             py::arg("value"))

        .def("_write_attribute",
             py::overload_cast<Tango::DeviceProxy &, const Tango::AttributeInfo &, py::object>(&PyDeviceProxy::write_attribute),
             py::arg("attr_info"),
             py::arg("value"))

        .def("_write_attributes", &PyDeviceProxy::write_attributes, py::arg("name_val"))

        .def("_write_read_attribute",
             &PyDeviceProxy::write_read_attribute,
             py::arg("attr_name"),
             py::arg("value"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("_write_read_attributes",
             &PyDeviceProxy::write_read_attributes,
             py::arg("attr_in"),
             py::arg("attr_read_names"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        //
        // history methods
        //

        .def("command_history",
             &PyDeviceProxy::command_history,
             R"doc(
                command_history(self, cmd_name, depth) -> sequence<DeviceDataHistory>

                        Retrieve command history from the command polling buffer. See
                        chapter on Advanced Feature for all details regarding polling

                    Parameters :
                       - cmd_name  : (str) Command name.
                       - depth     : (int) The wanted history depth.
                    Return     : This method returns a vector of DeviceDataHistory types.

                    Throws     : NonSupportedFeature, ConnectionFailed,
                                 CommunicationFailed, DevFailed from device)doc",
             py::arg("cmd_name"),
             py::arg("depth"))

        .def("attribute_history",
             &PyDeviceProxy::attribute_history,
             R"doc(
                attribute_history(self, attr_name, depth, extract_as=ExtractAs.Numpy) -> sequence<DeviceAttributeHistory>

                        Retrieve attribute history from the attribute polling buffer. See
                        chapter on Advanced Feature for all details regarding polling

                    Parameters :
                       - attr_name  : (str) Attribute name.
                       - depth      : (int) The wanted history depth.
                       - extract_as : (ExtractAs)

                    Return     : This method returns a vector of DeviceAttributeHistory types.

                    Throws     : NonSupportedFeature, ConnectionFailed,
                                 CommunicationFailed, DevFailed from device)doc",
             py::arg("attr_name"),
             py::arg("depth"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        //
        // Polling administration methods
        //

        .def("polling_status",
             &Tango::DeviceProxy::polling_status,
             py::return_value_policy::take_ownership,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                polling_status(self) -> sequence<str>

                        Return the device polling status.

                    Parameters : None
                    Return     : (sequence<str>) One string for each polled command/attribute.
                                 Each string is multi-line string with:

                                    - attribute/command name
                                    - attribute/command polling period in milliseconds
                                    - attribute/command polling ring buffer
                                    - time needed for last attribute/command execution in milliseconds
                                    - time since data in the ring buffer has not been updated
                                    - delta time between the last records in the ring buffer
                                    - exception parameters in case of the last execution failed)doc")

        .def("poll_command",
             py::overload_cast<const char *, int>(&Tango::DeviceProxy::poll_command),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                poll_command(self, cmd_name, period) -> None

                        Add a command to the list of polled commands.

                    Parameters :
                        - cmd_name : (str) command name
                        - period   : (int) polling period in milliseconds
                    Return     : None)doc",
             py::arg("cmd_name"),
             py::arg("period"))

        .def("poll_attribute",
             py::overload_cast<const char *, int>(&Tango::DeviceProxy::poll_attribute),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                poll_attribute(self, attr_name, period) -> None

                        Add an attribute to the list of polled attributes.

                    Parameters :
                        - attr_name : (str) attribute name
                        - period    : (int) polling period in milliseconds
                    Return     : None)doc",
             py::arg("attr_name"),
             py::arg("period"))

        .def("get_command_poll_period",
             py::overload_cast<const char *>(&Tango::DeviceProxy::get_command_poll_period),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_command_poll_period(self, cmd_name) -> int

                        Return the command polling period.

                    Parameters :
                        - cmd_name : (str) command name
                    Return     : polling period in milliseconds)doc",
             py::arg("cmd_name"))

        .def("get_attribute_poll_period",
             py::overload_cast<const char *>(&Tango::DeviceProxy::get_attribute_poll_period),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_attribute_poll_period(self, attr_name) -> int

                        Return the attribute polling period.

                    Parameters :
                        - attr_name : (str) attribute name
                    Return     : polling period in milliseconds)doc",
             py::arg("attr_name"))

        .def("is_command_polled",
             py::overload_cast<const char *>(&Tango::DeviceProxy::is_command_polled),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                is_command_polled(self, cmd_name) -> bool

                    True if the command is polled.

                    :param str cmd_name: command name

                    :returns: boolean value
                    :rtype: bool)doc",
             py::arg("cmd_name"))

        .def("is_attribute_polled",
             py::overload_cast<const char *>(&Tango::DeviceProxy::is_attribute_polled),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                is_attribute_polled(self, attr_name) -> bool

                    True if the attribute is polled.

                    :param str attr_name: attribute name

                    :returns: boolean value
                    :rtype: bool)doc",
             py::arg("attr_name"))

        .def("stop_poll_command",
             py::overload_cast<const char *>(&Tango::DeviceProxy::stop_poll_command),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                stop_poll_command(self, cmd_name) -> None

                        Remove a command from the list of polled commands.

                    Parameters :
                        - cmd_name : (str) command name
                    Return     : None)doc",
             py::arg("cmd_name"))

        .def("stop_poll_attribute",
             py::overload_cast<const char *>(&Tango::DeviceProxy::stop_poll_attribute),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                stop_poll_attribute(self, attr_name) -> None

                        Remove an attribute from the list of polled attributes.

                    Parameters :
                        - attr_name : (str) attribute name
                    Return     : None)doc",
             py::arg("attr_name"))

        //
        // Asynchronous methods
        //
        .def("__read_attributes_asynch",
             py::overload_cast<const StdStringVector &>(&Tango::DeviceProxy::read_attributes_asynch),
             py::call_guard<py::gil_scoped_release>())

        .def("__read_attributes_asynch",
             py::overload_cast<Tango::DeviceProxy &, py::object, py::object, PyTango::ExtractAs>(&PyDeviceProxy::read_attributes_asynch),
             py::arg("attr_names"),
             py::arg("callback"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("__read_attributes_reply",
             py::overload_cast<Tango::DeviceProxy &, long, PyTango::ExtractAs>(&PyDeviceProxy::read_attributes_reply),
             py::arg("id"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("__read_attributes_reply",
             py::overload_cast<Tango::DeviceProxy &, long, long, PyTango::ExtractAs>(&PyDeviceProxy::read_attributes_reply),
             py::arg("id"),
             py::arg("timeout"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("pending_asynch_call",
             &Tango::DeviceProxy::pending_asynch_call,
             R"doc(
                pending_asynch_call(self) -> int

                    Return number of device asynchronous pending requests"

                New in PyTango 7.0.0)doc")

        .def("__write_attributes_asynch",
             py::overload_cast<Tango::DeviceProxy &, py::object>(&PyDeviceProxy::write_attributes_asynch),
             py::arg("values"))

        .def("__write_attributes_asynch",
             py::overload_cast<Tango::DeviceProxy &, py::object, py::object>(&PyDeviceProxy::write_attributes_asynch),
             py::arg("values"),
             py::arg("callback"))

        .def("__write_attributes_reply",
             py::overload_cast<Tango::DeviceProxy &, long>(&PyDeviceProxy::write_attributes_reply),
             py::arg("id"))

        .def("__write_attributes_reply",
             py::overload_cast<Tango::DeviceProxy &, long, long>(&PyDeviceProxy::write_attributes_reply),
             py::arg("id"),
             py::arg("timeout"))

        //
        // Logging administration methods
        //

        .def("add_logging_target",
             py::overload_cast<const std::string &>(&Tango::DeviceProxy::add_logging_target),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                add_logging_target(self, target_type_target_name) -> None

                        Adds a new logging target to the device.

                        The target_type_target_name input parameter must follow the
                        format: target_type::target_name. Supported target types are:
                        console, file and device. For a device target, the target_name
                        part of the target_type_target_name parameter must contain the
                        name of a log consumer device (as defined in A.8). For a file
                        target, target_name is the full path to the file to log to. If
                        omitted, the device's name is used to build the file name
                        (which is something like domain_family_member.log). Finally, the
                        target_name part of the target_type_target_name input parameter
                        is ignored in case of a console target and can be omitted.

                    Parameters :
                        - target_type_target_name : (str) logging target
                    Return     : None

                    Throws     : DevFailed from device

                    New in PyTango 7.0.0)doc",
             py::arg("target_type_target_name"))

        .def("remove_logging_target",
             py::overload_cast<const std::string &>(&Tango::DeviceProxy::remove_logging_target),
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                remove_logging_target(self, target_type_target_name) -> None

                        Removes a logging target from the device's target list.

                        The target_type_target_name input parameter must follow the
                        format: target_type::target_name. Supported target types are:
                        console, file and device. For a device target, the target_name
                        part of the target_type_target_name parameter must contain the
                        name of a log consumer device (as defined in ). For a file
                        target, target_name is the full path to the file to remove.
                        If omitted, the default log file is removed. Finally, the
                        target_name part of the target_type_target_name input parameter
                        is ignored in case of a console target and can be omitted.
                        If target_name is set to '*', all targets of the specified
                        target_type are removed.

                    Parameters :
                        - target_type_target_name : (str) logging target
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("target_type_target_name"))

        .def("get_logging_target",
             &Tango::DeviceProxy::get_logging_target,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_logging_target(self) -> sequence<str>

                        Returns a sequence of string containing the current device's
                        logging targets. Each vector element has the following format:
                        target_type::target_name. An empty sequence is returned is the
                        device has no logging targets.

                    Parameters : None
                    Return     : a sequence<str> with the logging targets

                    New in PyTango 7.0.0)doc")

        .def("get_logging_level",
             &Tango::DeviceProxy::get_logging_level,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_logging_level(self) -> int

                        Returns the current device's logging level, where:
                            - 0=OFF
                            - 1=FATAL
                            - 2=ERROR
                            - 3=WARNING
                            - 4=INFO
                            - 5=DEBUG

                    Parameters :None
                    Return     : (int) representing the current logging level

                    New in PyTango 7.0.0)doc")

        .def("set_logging_level",
             &Tango::DeviceProxy::set_logging_level,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                set_logging_level(self, level) -> None

                        Changes the device's logging level, where:
                            - 0=OFF
                            - 1=FATAL
                            - 2=ERROR
                            - 3=WARNING
                            - 4=INFO
                            - 5=DEBUG

                    Parameters :
                        - level : (int) logging level
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("level"))

        //
        // Event methods
        //

        .def("__subscribe_event_global_with_stateless_flag",
             &PyDeviceProxy::subscribe_event_global_with_stateless_flag,
             py::arg("event"),
             py::arg("cb"),
             py::arg("stateless"))

        .def("__subscribe_event_global_with_sub_mode",
             &PyDeviceProxy::subscribe_event_global_with_sub_mode,
             py::arg("event"),
             py::arg("cb"),
             py::arg("event_sub_mode"))

        .def("__subscribe_event_attrib_with_stateless_flag",
             &PyDeviceProxy::subscribe_event_attrib_with_stateless_flag,
             py::arg("attr_name"),
             py::arg("event"),
             py::arg("cb_or_queuesize"),
             py::arg("stateless"),
             py::arg("extract_as"),
             py::arg("filters"))

        .def("__subscribe_event_attrib_with_sub_mode",
             &PyDeviceProxy::subscribe_event_attrib_with_sub_mode,
             py::arg("attr_name"),
             py::arg("event"),
             py::arg("cb_or_queuesize"),
             py::arg("event_sub_mode"),
             py::arg("extract_as"))

        // If the callback is running, unsubscribe_event will lock
        // until it finishes. So we MUST release GIL to avoid a deadlock
        .def("__unsubscribe_event",
             &Tango::DeviceProxy::unsubscribe_event,
             py::call_guard<py::gil_scoped_release>(),
             py::arg("event_id"))

        .def("__get_callback_events",
             PyDeviceProxy::get_events__callback,
             py::arg("event_id"),
             py::arg("callback"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("__get_attr_conf_events",
             PyDeviceProxy::get_events__attr_conf,
             py::arg("event_id"))

        .def("__get_data_events",
             PyDeviceProxy::get_events__data,
             py::arg("event_id"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        .def("__get_data_ready_events",
             PyDeviceProxy::get_events__data_ready,
             py::arg("event_id"))

        .def("__get_devintr_change_events",
             PyDeviceProxy::get_events__devintr_change_data,
             py::arg("event_id"),
             py::arg_v("extract_as", PyTango::ExtractAsNumpy, "ExtractAs.Numpy"))

        // methods to access data in event queues
        .def("event_queue_size",
             &Tango::DeviceProxy::event_queue_size,
             R"doc(
                event_queue_size(self, event_id) -> int

                        Returns the number of stored events in the event reception
                        buffer. After every call to DeviceProxy.get_events(), the event
                        queue size is 0. During event subscription the client must have
                        chosen the 'pull model' for this event. event_id is the event
                        identifier returned by the DeviceProxy.subscribe_event() method.

                    Parameters :
                        - event_id : (int) event identifier
                    Return     : an integer with the queue size

                    Throws     : EventSystemFailed

                    New in PyTango 7.0.0)doc",
             py::arg("event_id"))

        .def("get_last_event_date",
             &Tango::DeviceProxy::get_last_event_date,
             R"doc(
                get_last_event_date(self, event_id) -> TimeVal

                        Returns the arrival time of the last event stored in the event
                        reception buffer. After every call to DeviceProxy:get_events(),
                        the event reception buffer is empty. In this case an exception
                        will be returned. During event subscription the client must have
                        chosen the 'pull model' for this event. event_id is the event
                        identifier returned by the DeviceProxy.subscribe_event() method.

                    Parameters :
                        - event_id : (int) event identifier
                    Return     : (tango.TimeVal) representing the arrival time

                    Throws     : EventSystemFailed

                    New in PyTango 7.0.0)doc",
             py::arg("event_id"))

        .def("is_event_queue_empty",
             &Tango::DeviceProxy::is_event_queue_empty,
             R"doc(
                is_event_queue_empty(self, event_id) -> bool

                        Returns true when the event reception buffer is empty. During
                        event subscription the client must have chosen the 'pull model'
                        for this event. event_id is the event identifier returned by the
                        DeviceProxy.subscribe_event() method.

                        Parameters :
                            - event_id : (int) event identifier
                        Return     : (bool) True if queue is empty or False otherwise

                        Throws     : EventSystemFailed

                        New in PyTango 7.0.0)doc",
             py::arg("event_id"))

        //
        // Locking methods
        //
        .def("lock",
             &Tango::DeviceProxy::lock,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                lock(self, (int)lock_validity) -> None

                        Lock a device. The lock_validity is the time (in seconds) the
                        lock is kept valid after the previous lock call. A default value
                        of 10 seconds is provided and should be fine in most cases. In
                        case it is necessary to change the lock validity, it's not
                        possible to ask for a validity less than a minimum value set to
                        2 seconds. The library provided an automatic system to
                        periodically re lock the device until an unlock call. No code is
                        needed to start/stop this automatic re-locking system. The
                        locking system is re-entrant. It is then allowed to call this
                        method on a device already locked by the same process. The
                        locking system has the following features:

                          * It is impossible to lock the database device or any device
                            server process admin device
                          * Destroying a locked DeviceProxy unlocks the device
                          * Restarting a locked device keeps the lock
                          * It is impossible to restart a device locked by someone else
                          * Restarting a server breaks the lock

                        A locked device is protected against the following calls when
                        executed by another client:

                          * command_inout call except for device state and status
                            requested via command and for the set of commands defined as
                            allowed following the definition of allowed command in the
                            Tango control access schema.
                          * write_attribute call
                          * write_read_attribute call
                          * set_attribute_config call

                    Parameters :
                        - lock_validity : (int) lock validity time in seconds
                                            (optional, default value is
                                            tango.constants.DEFAULT_LOCK_VALIDITY)
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("lock_validity") = Tango::DEFAULT_LOCK_VALIDITY)

        .def("unlock",
             &Tango::DeviceProxy::unlock,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                unlock(self, (bool)force) -> None

                        Unlock a device. If used, the method argument provides a back
                        door on the locking system. If this argument is set to true,
                        the device will be unlocked even if the caller is not the locker.
                        This feature is provided for administration purpose and should
                        be used very carefully. If this feature is used, the locker will
                        receive a DeviceUnlocked during the next call which is normally
                        protected by the locking Tango system.

                    Parameters :
                        - force : (bool) force unlocking even if we are not the
                                  locker (optional, default value is False)
                    Return     : None

                    New in PyTango 7.0.0)doc",
             py::arg("force") = false)

        .def("locking_status",
             &Tango::DeviceProxy::locking_status,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                locking_status(self) -> str

                        This method returns a plain string describing the device locking
                        status. This string can be:

                          * 'Device <device name> is not locked' in case the device is
                            not locked
                          * 'Device <device name> is locked by CPP or Python client with
                            PID <pid> from host <host name>' in case the device is
                            locked by a CPP client
                          * 'Device <device name> is locked by JAVA client class
                            <main class> from host <host name>' in case the device is
                            locked by a JAVA client

                    Parameters : None
                    Return     : a string representing the current locking status

                    New in PyTango 7.0.0)doc")

        .def("is_locked",
             &Tango::DeviceProxy::is_locked,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                is_locked(self) -> bool

                        Returns True if the device is locked. Otherwise, returns False.

                    Parameters : None
                    Return     : (bool) True if the device is locked. Otherwise, False

                    New in PyTango 7.0.0)doc")

        .def("is_locked_by_me",
             &Tango::DeviceProxy::is_locked_by_me,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                is_locked_by_me(self) -> bool

                        Returns True if the device is locked by the caller. Otherwise,
                        returns False (device not locked or locked by someone else)

                    Parameters : None
                    Return     : (bool) True if the device is locked by us.
                                    Otherwise, False

                    New in PyTango 7.0.0)doc")

        .def("get_locker",
             &Tango::DeviceProxy::get_locker,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                get_locker(self, lockinfo) -> bool

                        If the device is locked, this method returns True an set some
                        locker process informations in the structure passed as argument.
                        If the device is not locked, the method returns False.

                    Parameters :
                        - lockinfo [out] : (tango.LockInfo) object that will be filled
                                            with lock information
                    Return     : (bool) True if the device is locked by us.
                                 Otherwise, False

                    New in PyTango 7.0.0)doc",
             py::arg("lockinfo"));
}
