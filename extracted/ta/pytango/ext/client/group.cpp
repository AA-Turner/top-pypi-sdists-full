/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "pyutils.h"
#include "convertors/type_casters.h"

#include "client/device_attribute.h"
#include "base_types_structures/exception.h"

void export_group_reply_list(py::module &m);
void export_group_reply(py::module &m);

using GroupUniquePtr = std::unique_ptr<Tango::Group, DeleterWithoutGIL>;

namespace PyGroup {
void add(Tango::Group &self, Tango::Group *grp, int timeout_ms) {
    if(grp == nullptr) {
        raise_(PyExc_TypeError,
               "Param \"group\" is null. It probably means that it has"
               " already been inserted in another group.");
    }
    // After adding grp_ptr into self, self is the responsible for deleting grp.
    self.add(grp, timeout_ms);
    // I am not sure about this line - looks dangerous. But without it, I regularly get SEGFAULTs
    py::cast(grp).release();
}

static void __update_data_format(Tango::Group &self, Tango::GroupAttrReplyList &r) {
    // Usually we pass a device_proxy to "convert_to_python" in order to
    // get the data_format of the DeviceAttribute for Tango versions
    // older than 7.0. However, GroupAttrReply has no device_proxy to use!
    // So, we are using update_data_format() in here.
    // The convert_to_python method is called, without the usual
    // device_proxy argument, in PyGroupAttrReply::get_data().
    Tango::GroupAttrReplyList::iterator i, e = r.end();
    for(i = r.begin(); i != e; ++i) {
        Tango::DeviceProxy *dev_proxy = self.get_device(i->dev_name());
        if(dev_proxy == nullptr) {
            continue;
        }
        PyDeviceAttribute::update_data_format(*dev_proxy, &(i->get_data()), 1);
    }
}

Tango::GroupAttrReplyList read_attribute_reply(Tango::Group &self, long req_id, long timeout_ms = 0) {
    Tango::GroupAttrReplyList reply;
    {
        py::gil_scoped_release no_gil;
        reply = self.read_attribute_reply(req_id, timeout_ms);
    }
    __update_data_format(self, reply);
    return reply;
}

Tango::GroupAttrReplyList read_attributes_reply(Tango::Group &self, long req_id, long timeout_ms = 0) {
    Tango::GroupAttrReplyList reply;
    {
        py::gil_scoped_release no_gil;
        reply = self.read_attributes_reply(req_id, timeout_ms);
    }
    __update_data_format(self, reply);
    return reply;
}

long write_attribute_asynch(Tango::Group &self,
                            py::object &attr,
                            py::object py_value,
                            bool forward = true,
                            bool multi = false) {
    Tango::AttributeInfoEx attr_info;
    bool has_attr_info = false;
    std::string attr_name;

    try {
        attr_info = attr.cast<Tango::AttributeInfoEx>();
        has_attr_info = true;
    } catch(const py::cast_error &) {
        attr_name = attr.cast<std::string>();
    }

    Tango::DeviceProxy *dev_proxy = self.get_device(1);
    if(dev_proxy == nullptr) {
        Tango::DeviceAttribute dev_attr;
        dev_attr.set_name(attr_name.c_str());
        py::gil_scoped_release no_gil;
        return self.write_attribute_asynch(dev_attr, forward);
    }

    if(!has_attr_info) {
        py::gil_scoped_release no_gil;
        for(long dev_idx = 1; dev_idx <= self.get_size(); ++dev_idx) {
            try {
                attr_info = self[dev_idx]->get_attribute_config(attr_name);
                has_attr_info = true;
                break;
            } catch(...) {
            }
        }
    }

    if(multi) {
        if(!py::isinstance<py::sequence>(py_value)) {
            throw py::type_error("When multi is set, value must be a Python sequence "
                                 "(e.g., list or tuple)");
        }

        unsigned long attr_nb = py::len(py_value);
        std::vector<Tango::DeviceAttribute> dev_attr(attr_nb);
        auto seq = py_value.cast<py::sequence>();

        if(has_attr_info) {
            for(unsigned long i = 0; i < attr_nb; ++i) {
                py::object item = seq[i];
                PyDeviceAttribute::reset(dev_attr[i], attr_info, item);
            }
        } else {
            for(unsigned long i = 0; i < attr_nb; ++i) {
                dev_attr[i].set_name(attr_name.c_str());
            }
        }
        py::gil_scoped_release no_gil;
        return self.write_attribute_asynch(dev_attr, forward);
    } else {
        Tango::DeviceAttribute dev_attr;
        if(has_attr_info) {
            PyDeviceAttribute::reset(dev_attr, attr_info, py_value);
        } else {
            dev_attr.set_name(attr_name.c_str());
        }
        py::gil_scoped_release no_gil;
        return self.write_attribute_asynch(dev_attr, forward);
    }
}
} // namespace PyGroup

void export_group(py::module &m) {
    export_group_reply(m);
    export_group_reply_list(m);

    py::class_<Tango::Group, GroupUniquePtr>(m, "__Group")
        .def(py::init<const std::string &>())
        .def("_add",
             py::overload_cast<const std::string &, int>(&Tango::Group::add),
             py::arg("pattern"),
             py::arg("timeout_ms") = -1)
        .def("_add",
             py::overload_cast<const StdStringVector &, int>(&Tango::Group::add),
             py::arg("patterns"),
             py::arg("timeout_ms") = -1)
        .def("_add", &PyGroup::add, py::arg("group"), py::arg("timeout_ms") = -1)

        .def("_remove",
             py::overload_cast<const std::string &, bool>(&Tango::Group::remove),
             py::arg("pattern"),
             py::arg("forward") = true)
        .def("_remove",
             py::overload_cast<const StdStringVector &, bool>(&Tango::Group::remove),
             py::arg("patterns"),
             py::arg("forward") = true)

        .def("get_size",
             &Tango::Group::get_size,
             R"doc(
                The number of the devices in the hierarchy

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool
             )doc",
             py::arg("forward") = true)

        .def("get_group", &Tango::Group::get_group, py::return_value_policy::reference_internal, py::arg("group_name"))

        .def("get_device_list",
             &Tango::Group::get_device_list,
             R"doc(
                Considering the following hierarchy:

                ::

                    g2.add("my/device/04")
                    g2.add("my/device/05")

                    g4.add("my/device/08")
                    g4.add("my/device/09")

                    g3.add("my/device/06")
                    g3.add(g4)
                    g3.add("my/device/07")

                    g1.add("my/device/01")
                    g1.add(g2)
                    g1.add("my/device/03")
                    g1.add(g3)
                    g1.add("my/device/02")

                The returned vector content depends on the value of the forward option.
                If set to true, the results will be organized as follows:

                ::

                        dl = g1.get_device_list(True)

                    dl[0] contains "my/device/01" which belongs to g1
                    dl[1] contains "my/device/04" which belongs to g1.g2
                    dl[2] contains "my/device/05" which belongs to g1.g2
                    dl[3] contains "my/device/03" which belongs to g1
                    dl[4] contains "my/device/06" which belongs to g1.g3
                    dl[5] contains "my/device/08" which belongs to g1.g3.g4
                    dl[6] contains "my/device/09" which belongs to g1.g3.g4
                    dl[7] contains "my/device/07" which belongs to g1.g3
                    dl[8] contains "my/device/02" which belongs to g1

                If the forward option is set to false, the results are:

                ::

                        dl = g1.get_device_list(False);

                    dl[0] contains "my/device/01" which belongs to g1
                    dl[1] contains "my/device/03" which belongs to g1
                    dl[2] contains "my/device/02" which belongs to g1

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool

                :return: The list of devices currently in the hierarchy.
                :rtype: :py:obj:`list`\[:py:obj:`str`]
             )doc",
             py::arg("forward") = true)

        .def("remove_all",
             &Tango::Group::remove_all,
             R"doc(
                Removes all elements in the _RealGroup. After such a call, the _RealGroup is empty.)doc")

        // GroupElement redefinitions of enable/disable. If I didn't
        // redefine them, the later Group only definitions would
        // hide the ones defined in GroupElement.
        .def("enable", &Tango::GroupElement::enable)
        .def("disable", &Tango::GroupElement::disable)
        .def("enable",
             &Tango::Group::enable,
             R"doc(
                Enables group element. The element will participate in all group operations.

                :param dev_name: device_name name of the element, can contain wildcards (*).
                                 If more than one device matches the pattern, only the first one will be enabled.
                :type dev_name: :py:obj:`str`

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool
             )doc",
             py::arg("dev_name"),
             py::arg("forward") = true)
        .def("disable",
             &Tango::Group::disable,
             R"doc(
                Disables group element. The element will be excluded from all group operations.

                :param dev_name: device_name name of the element, can contain wildcards (*).
                                 If more than one device matches the pattern, only the first one will be disabled.
                :type dev_name: :py:obj:`str`

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool
             )doc",
             py::arg("dev_name"),
             py::arg("forward") = true)

        .def("get_parent", &Tango::Group::get_parent, py::return_value_policy::reference_internal)
        .def("contains",
             &Tango::Group::contains,
             R"doc(
                Returns true if the hierarchy contains groups and/or
                devices which name matches the specified pattern.

                :param pattern: The pattern can be a fully qualified or simple
                                group name, a device name or a device name pattern.
                :type pattern: :py:obj:`str`

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
             )doc",
             py::arg("pattern"),
             py::arg("forward") = true)
        .def("get_device",
             py::overload_cast<const std::string &>(&Tango::Group::get_device),
             py::return_value_policy::reference_internal,
             py::arg("dev_name"))
        .def("get_device",
             py::overload_cast<long>(&Tango::Group::get_device),
             py::return_value_policy::reference_internal,
             py::arg("idx"))
        .def("ping",
             &Tango::Group::ping,
             R"doc(
                Ping all devices in a group. This method returns true if all devices in the group are alive, false otherwise.

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool
             )doc",
             py::arg("forward") = true)
        .def("set_timeout_millis",
             &Tango::Group::set_timeout_millis,
             R"doc(
                Set client side timeout for all devices composing the group in
                milliseconds. Any method which takes longer than this time to execute
                will throw an exception.

                :param timeout_ms: timeout in milliseconds
                :type timeout_ms: int

                .. versionadded:: 7.0.0
             )doc",
             py::arg("timeout_ms"))
        .def("get_name",
             &Tango::Group::get_name,
             py::return_value_policy::copy,
             "Get the name of the group. Eg: Group('name').get_name() == 'name'")
        .def("get_fully_qualified_name",
             &Tango::Group::get_fully_qualified_name,
             "Get the complete (dpt-separated) name of the group. "
             "This takes into consideration the name of the group and its parents")
        .def("is_enabled",
             &Tango::Group::is_enabled,
             R"doc(
                Check if a device is enabled

                :param dev_name: device_name name of the element.
                                 If more than one device matches the pattern, only the first one will be checked.
                :type dev_name: :py:obj:`str`

                :param forward: flag to perform recursive search for the element in all sub-groups
                :type forward: bool

                .. versionadded:: 7.0.0
             )doc",
             py::arg("device_name"),
             py::arg("forward") = true)
        .def("name_equals",
             &Tango::Group::name_equals,
             R"doc(
                .. versionadded:: 7.0.0
             )doc",
             py::arg("name"))
        .def("name_matches",
             &Tango::Group::name_matches,
             R"doc(
                .. versionadded:: 7.0.0
             )doc",
             py::arg("name"))

        .def("command_inout_asynch",
             static_cast<long (Tango::Group::*)(const std::string &, bool, bool)>(&Tango::Group::command_inout_asynch),
             py::arg("cmd_name"),
             py::arg("forget") = false,
             py::arg("forward") = true)
        .def("command_inout_asynch",
             static_cast<long (Tango::Group::*)(const std::string &, const Tango::DeviceData &, bool, bool)>(
                 &Tango::Group::command_inout_asynch),
             R"doc(

                Executes a Tango command on each device in the group asynchronously.
                The method sends the request to all devices and returns immediately.
                Pass the returned request id to Group.command_inout_reply() to obtain
                the results.

                :param cmd_name: command name
                :type cmd_name: :py:obj:`str`

                :param param: parameter value
                :type param: Any

                :param forget: Fire and forget flag. If set to true, it means that
                               no reply is expected (i.e. the caller does not care
                               about it and will not even try to get it)
                :type forget: bool

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool

                :return: request id. Pass the returned request id to
                         Group.command_inout_reply() to obtain the results.
             )doc",
             py::arg("cmd_name"),
             py::arg("param"),
             py::arg("forget") = false,
             py::arg("forward") = true)
        .def("command_inout_asynch",
             static_cast<long (Tango::Group::*)(
                 const std::string &, const std::vector<Tango::DeviceData> &, bool, bool)>(
                 &Tango::Group::command_inout_asynch),
             R"doc(
                Executes a Tango command on each device in the group asynchronously.
                The method sends the request to all devices and returns immediately.
                Pass the returned request id to Group.command_inout_reply() to obtain
                the results.

                :param cmd_name: command name
                :type cmd_name: :py:obj:`str`

                :param param_list: sequence of parameters.
                :type param_list: :obj:`~tango.DeviceDataList`

                :param forget: Fire and forget flag. If set to true, it means that
                               no reply is expected (i.e. the caller does not care
                               about it and will not even try to get it)
                :type forget: bool

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool

                :return: request id. Pass the returned request id to
                         Group.command_inout_reply() to obtain the results.
             )doc",
             py::arg("cmd_name"),
             py::arg("param"),
             py::arg("forget") = false,
             py::arg("forward") = true)
        .def("command_inout_reply",
             &Tango::Group::command_inout_reply,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                Returns the results of an asynchronous command.

                :param req_id: Is a request identifier previously returned by one of the command_inout_asynch methods
                :type req_id: int

                :param timeout_ms: For each device in the hierarchy, if the command
                                   result is not yet available, command_inout_reply
                                   wait timeout_ms milliseconds before throwing an
                                   exception. This exception will be part of the
                                   global reply. If timeout_ms is set to 0,
                                   command_inout_reply waits "indefinitely".
                :type timeout_ms: int

                :rtype: :py:obj:`list`\[:obj:`~tango.GroupCmdReply`]
             )doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0)
        .def("read_attribute_asynch",
             &Tango::Group::read_attribute_asynch,
             R"doc(
                Reads an attribute on each device in the group asynchronously.
                The method sends the request to all devices and returns immediately.

                :param attr_name: Name of the attribute to read
                :type attr_name: :py:obj:`str`

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool

                :return: request id. Pass the returned request id to
                         Group.read_attribute_reply() to obtain the results.
             )doc",
             py::arg("attr_name"),
             py::arg("forward") = true)
        .def("read_attribute_reply",
             PyGroup::read_attribute_reply,
             R"doc(
                Returns the results of an asynchronous attribute reading.

                :param req_id: Is a request identifier previously returned by one of the read_attribute_asynch methods
                :type req_id: int

                :param timeout_ms: For each device in the hierarchy, if the command
                                   result is not yet available, command_inout_reply
                                   wait timeout_ms milliseconds before throwing an
                                   exception. This exception will be part of the
                                   global reply. If timeout_ms is set to 0,
                                   command_inout_reply waits "indefinitely".
                :type timeout_ms: int

                :rtype: :py:obj:`list`\[:obj:`~tango.GroupAttrReply`]
             )doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0)
        .def("read_attributes_asynch",
             &Tango::Group::read_attributes_asynch,
             R"doc(
                Reads the attributes on each device in the group asynchronously.
                The method sends the request to all devices and returns immediately.

                :param attr_names: Name of the attributes to read.
                :type attr_names: :py:obj:`list`\[:py:obj:`str`]

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool

                :return: request id. Pass the returned request id to
                         Group.read_attributes_reply() to obtain the results.
             )doc",
             py::arg("attr_names"),
             py::arg("forward") = true)
        .def("read_attributes_reply",
             &PyGroup::read_attributes_reply,
             R"doc(
                read_attributes_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupAttrReply>

                Returns the results of an asynchronous attribute reading.

                :param req_id: Is a request identifier previously returned by one of the read_attributes_asynch methods
                :type req_id: int

                :param timeout_ms: For each device in the hierarchy, if the command
                                   result is not yet available, command_inout_reply
                                   wait timeout_ms milliseconds before throwing an
                                   exception. This exception will be part of the
                                   global reply. If timeout_ms is set to 0,
                                   command_inout_reply waits "indefinitely".
                :type timeout_ms: int

                :rtype: :py:obj:`list`\[:obj:`~tango.GroupAttrReply`]
             )doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0)
        .def("write_attribute_asynch",
             &PyGroup::write_attribute_asynch,
             R"doc(
                Writes an attribute on each device in the group asynchronously.
                The method sends the request to all devices and returns immediately.

                :param attr_name: Name or AttributeInfoEx of the attribute to write.
                :type attr_name: :py:obj:`str` | :py:obj:`AttributeInfoEx`

                :param value: Value to write. See DeviceProxy.write_attribute
                :type value: :py:obj:`typing.Any`

                :param forward: If it is set to true (the default), the request is forwarded to sub-groups.
                                Otherwise, it is only applied to the local set of devices.
                :type forward: bool

                :param multi: If it is set to false (the default), the same
                              value is applied to all devices in the group.
                              Otherwise the value is interpreted as a sequence of
                              values, and each value is applied to the corresponding
                              device in the group. In this case len(value) must be
                              equal to group.get_size()!
                :type multi: bool

                :return: request id. Pass the returned request id to
                         Group.write_attribute_reply() to obtain the results.

                .. versionchanged:: 10.1.0 attr_name parameter was renamed to attr and
                                    added support for AttributeInfoEx for attr_values parameter
             )doc",
             py::arg("attr_name"),
             py::arg("value"),
             py::arg("forward") = true,
             py::arg("multi") = false)
        .def("write_attribute_reply",
             &Tango::Group::write_attribute_reply,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                write_attribute_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupReply>

                Returns the acknowledgements of an asynchronous attribute writing.

                :param req_id: Is a request identifier previously returned by one of the write_attribute_asynch methods
                :type req_id: int

                :param timeout_ms: For each device in the hierarchy, if the command
                                   result is not yet available, command_inout_reply
                                   wait timeout_ms milliseconds before throwing an
                                   exception. This exception will be part of the
                                   global reply. If timeout_ms is set to 0,
                                   command_inout_reply waits "indefinitely".
                :type timeout_ms: int

                :rtype: :py:obj:`list`\[:obj:`~tango.GroupReply`]
             )doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0);
}
