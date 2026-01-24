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
    Tango::GroupAttrReplyList r;
    {
        py::gil_scoped_release no_gil;
        r = self.read_attribute_reply(req_id, timeout_ms);
    }
    __update_data_format(self, r);
    return r;
}

Tango::GroupAttrReplyList read_attributes_reply(Tango::Group &self, long req_id, long timeout_ms = 0) {
    Tango::GroupAttrReplyList r;
    {
        py::gil_scoped_release no_gil;
        r = self.read_attributes_reply(req_id, timeout_ms);
    }
    __update_data_format(self, r);
    return r;
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
            throw py::type_error(
                "When multi is set, value must be a Python sequence "
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
                get_size(self, forward=True) -> int

                    Parameters :
                        - forward : (bool) If it is set to true (the default), the request is
                                    forwarded to sub-groups.

                    Return     : (int) The number of the devices in the hierarchy

                    Throws     :)doc",
             py::arg("forward") = true)

        .def("get_group",
             &Tango::Group::get_group,
             R"doc(
               get_group(self, group_name ) -> Group

                        Returns a reference to the specified group or None if there is no group
                        by that name. The group_name can be a fully qualified name.

                        Considering the following group:

                        ::

                            -> gauges
                                |-> cell-01
                                |    |-> penning
                                |    |    |-> ...
                                |    |-> pirani
                                |    |-> ...
                                |-> cell-02
                                |    |-> penning
                                |    |    |-> ...
                                |    |-> pirani
                                |    |-> ...
                                | -> cell-03
                                |    |-> ...
                                |
                                | -> ...

                        A call to gauges.get_group("penning") returns the first group named
                        "penning" in the hierarchy (i.e. gauges.cell-01.penning) while
                        gauges.get_group("gauges.cell-02.penning'') returns the specified group.

                        The request is systematically forwarded to subgroups (i.e. if no group
                        named group_name could be found in the local set of elements, the request
                        is forwarded to subgroups).

                    Parameters :
                        - group_name : (str)

                    Return     : (Group)

                    Throws     :

                    New in PyTango 7.0.0)doc",
             py::arg("group_name"),
             py::return_value_policy::reference_internal)

        .def("get_device_list",
             &Tango::Group::get_device_list,
             R"doc(
               get_device_list(self, forward=True) -> sequence<str>

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


                    Parameters :
                        - forward : (bool) If it is set to true (the default), the request
                                    is forwarded to sub-groups. Otherwise, it is only
                                    applied to the local set of devices.

                    Return     : (sequence<str>) The list of devices currently in the hierarchy.

                    Throws     :)doc",
             py::arg("forward") = true)

        .def("remove_all",
             &Tango::Group::remove_all,
             R"doc(
                remove_all(self) -> None

                    Removes all elements in the _RealGroup. After such a call, the _RealGroup is empty.)doc")

        // GroupElement redefinitions of enable/disable. If I didn't
        // redefine them, the later Group only definitions would
        // hide the ones defined in GroupElement.
        .def("enable", &Tango::GroupElement::enable)
        .def("disable", &Tango::GroupElement::disable)
        .def("enable",
             &Tango::Group::enable,
             R"doc(
                enable(self, dev_name, forward=True) -> None

                    Enables group element. The element will participate in all group operations.

                :param dev_name: device_name name of the element, can contain wildcards (*). If more than one device matches the pattern, only the first one will be enabled.
                :type dev_name: str

                :param forward: flag to perform recursive search for the element in all sub-groups
                :type forward: bool
             )doc",
             py::arg("dev_name"),
             py::arg("forward") = true)
        .def("disable",
             &Tango::Group::disable,
             R"doc(
                disable(self, dev_name, forward=True) -> None

                    Disables group element. The element will be excluded from all group operations.

                :param dev_name: device_name name of the element, can contain wildcards (*). If more than one device matches the pattern, only the first one will be disabled.
                :type dev_name: str

                :param forward: flag to perform recursive search for the element in all sub-groups
                :type forward: bool
             )doc",
             py::arg("dev_name"),
             py::arg("forward") = true)

        .def("get_parent", &Tango::Group::get_parent, py::return_value_policy::reference_internal)
        .def("contains",
             &Tango::Group::contains,
             R"doc(
                contains(self, pattern, forward=True) -> bool

                    Parameters :
                        - pattern    : (str) The pattern can be a fully qualified or simple
                                        group name, a device name or a device name pattern.
                        - forward    : (bool) If fwd is set to true (the default), the remove
                                        request is also forwarded to subgroups. Otherwise,
                                        it is only applied to the local set of elements.

                    Return     : (bool) Returns true if the hierarchy contains groups and/or
                                 devices which name matches the specified pattern. Returns
                                 false otherwise.

                    Throws     :)doc",
             py::arg("pattern"),
             py::arg("forward") = true)
        .def("get_device",
             py::overload_cast<const std::string &>(&Tango::Group::get_device),
             py::return_value_policy::reference_internal,
             R"doc(
                get_device(self, dev_name) -> DeviceProxy

                        Returns a reference to the specified device or None if there is no
                        device by that name in the group. Or, returns a reference to the
                        "idx-th" device in the hierarchy or NULL if the hierarchy contains
                        less than "idx" devices.

                        This method may throw an exception in case the specified device belongs
                        to the group but can't be reached (not registered, down...). See example
                        below:

                        ::

                            try:
                                dp = g.get_device("my/device/01")
                                if dp is None:
                                    # my/device/01 does not belong to the group
                                    pass
                            except DevFailed, f:
                                # my/device/01 belongs to the group but can't be reached
                                pass

                        The request is systematically forwarded to subgroups (i.e. if no device
                        named device_name could be found in the local set of devices, the
                        request is forwarded to subgroups).

                    Parameters :
                        - dev_name    : (str) Device name.

                    Return     : DeviceProxy

                    Throws     : DevFailed)doc",
             py::arg("dev_name"))
        .def("get_device",
             py::overload_cast<long>(&Tango::Group::get_device),
             py::return_value_policy::reference_internal,
             R"doc(
                get_device(self, idx) -> DeviceProxy

                        Returns a reference to the specified device or None if there is no
                        device by that name in the group. Or, returns a reference to the
                        "idx-th" device in the hierarchy or NULL if the hierarchy contains
                        less than "idx" devices.

                        This method may throw an exception in case the specified device belongs
                        to the group but can't be reached (not registered, down...). See example
                        below:

                        ::

                            try:
                                dp = g.get_device("my/device/01")
                                if dp is None:
                                    # my/device/01 does not belong to the group
                                    pass
                            except DevFailed, f:
                                # my/device/01 belongs to the group but can't be reached
                                pass

                        The request is systematically forwarded to subgroups (i.e. if no device
                        named device_name could be found in the local set of devices, the
                        request is forwarded to subgroups).

                    Parameters :
                        - idx         : (int) Device number.

                    Return     : DeviceProxy

                    Throws     : DevFailed)doc",
             py::arg("idx"))
        .def("ping",
             &Tango::Group::ping,
             R"doc(
                ping(self, forward=True) -> bool

                        Ping all devices in a group.

                    Parameters :
                        - forward    : (bool) If fwd is set to true (the default), the request
                                        is also forwarded to subgroups. Otherwise, it is
                                        only applied to the local set of devices.

                    Return     : (bool) This method returns true if all devices in
                                 the group are alive, false otherwise.

                    Throws     :)doc",
             py::arg("forward") = true)
        .def("set_timeout_millis",
             &Tango::Group::set_timeout_millis,
             R"doc(
                set_timeout_millis(self, timeout_ms) -> bool

                        Set client side timeout for all devices composing the group in
                        milliseconds. Any method which takes longer than this time to execute
                        will throw an exception.

                    Parameters :
                        - timeout_ms : (int)

                    Return     : None

                    Throws     : (errors are ignored)

                    New in PyTango 7.0.0)doc",
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
                is_enabled(self, device_name, forward) -> bool

                    Check if a device is enabled

                :param dev_name: device_name name of the element. If more than one device matches the pattern, only the first one will be checked.
                :type dev_name: str

                :param forward: flag to perform recursive search for the element in all sub-groups
                :type forward: bool

                New in PyTango 7.0.0)doc",
             py::arg("device_name"),
             py::arg("forward") = true)
        .def("name_equals",
             &Tango::Group::name_equals,
             R"doc(
                name_equals(name) -> bool

                New in PyTango 7.0.0)doc",
             py::arg("name"))
        .def("name_matches",
             &Tango::Group::name_matches,
             R"doc(
                name_equals(name) -> bool

                New in PyTango 7.0.0)doc",
             py::arg("name"))

        .def("command_inout_asynch",
             static_cast<long (Tango::Group::*)(const std::string &, bool, bool)>(&Tango::Group::command_inout_asynch),
             R"doc(
                command_inout_asynch(self, cmd_name, forget=False, forward=True) -> int

                        Executes a Tango command on each device in the group asynchronously.
                        The method sends the request to all devices and returns immediately.
                        Pass the returned request id to Group.command_inout_reply() to obtain
                        the results.

                    Parameters :
                        - cmd_name   : (str) Command name
                        - forget     : (bool) Fire and forget flag. If set to true, it means that
                                       no reply is expected (i.e. the caller does not care
                                       about it and will not even try to get it)
                        - forward    : (bool) If it is set to true (the default) request is
                                        forwarded to subgroups. Otherwise, it is only applied
                                        to the local set of devices.

                    Return     : (int) request id. Pass the returned request id to
                                Group.command_inout_reply() to obtain the results.

                    Throws     :)doc",
             py::arg("cmd_name"),
             py::arg("forget") = false,
             py::arg("forward") = true)
        .def("command_inout_asynch",
             static_cast<long (Tango::Group::*)(const std::string &, const Tango::DeviceData &, bool, bool)>(&Tango::Group::command_inout_asynch),
             R"doc(
                command_inout_asynch(self, cmd_name, param, forget=False, forward=True) -> int

                        Executes a Tango command on each device in the group asynchronously.
                        The method sends the request to all devices and returns immediately.
                        Pass the returned request id to Group.command_inout_reply() to obtain
                        the results.

                    Parameters :
                        - cmd_name   : (str) Command name
                        - param      : (any) parameter value
                        - forget     : (bool) Fire and forget flag. If set to true, it means that
                                       no reply is expected (i.e. the caller does not care
                                       about it and will not even try to get it)
                        - forward    : (bool) If it is set to true (the default) request is
                                        forwarded to subgroups. Otherwise, it is only applied
                                        to the local set of devices.

                    Return     : (int) request id. Pass the returned request id to
                                Group.command_inout_reply() to obtain the results.

                    Throws     :)doc",
             py::arg("cmd_name"),
             py::arg("param"),
             py::arg("forget") = false,
             py::arg("forward") = true)
        .def("command_inout_asynch",
             static_cast<long (Tango::Group::*)(const std::string &, const std::vector<Tango::DeviceData> &, bool, bool)>(&Tango::Group::command_inout_asynch),
             R"doc(
                command_inout_asynch(self, cmd_name, param_list, forget=False, forward=True) -> int

                        Executes a Tango command on each device in the group asynchronously.
                        The method sends the request to all devices and returns immediately.
                        Pass the returned request id to Group.command_inout_reply() to obtain
                        the results.

                    Parameters :
                        - cmd_name   : (str) Command name
                        - param_list : (tango.DeviceDataList) sequence of parameters.
                                       When given, it's length must match the group size.
                        - forget     : (bool) Fire and forget flag. If set to true, it means that
                                       no reply is expected (i.e. the caller does not care
                                       about it and will not even try to get it)
                        - forward    : (bool) If it is set to true (the default) request is
                                        forwarded to subgroups. Otherwise, it is only applied
                                        to the local set of devices.

                    Return     : (int) request id. Pass the returned request id to
                                Group.command_inout_reply() to obtain the results.

                    Throws     :)doc",
             py::arg("cmd_name"),
             py::arg("param"),
             py::arg("forget") = false,
             py::arg("forward") = true)
        .def("command_inout_reply",
             &Tango::Group::command_inout_reply,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                command_inout_reply(self, req_id, timeout_ms=0) -> sequence<GroupCmdReply>

                        Returns the results of an asynchronous command.

                    Parameters :
                        - req_id     : (int) Is a request identifier previously returned by one
                                        of the command_inout_asynch methods
                        - timeout_ms : (int) For each device in the hierarchy, if the command
                                        result is not yet available, command_inout_reply
                                        wait timeout_ms milliseconds before throwing an
                                        exception. This exception will be part of the
                                        global reply. If timeout_ms is set to 0,
                                        command_inout_reply waits "indefinitely".

                    Return     : (sequence<GroupCmdReply>)

                    Throws     :)doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0)
        .def("read_attribute_asynch",
             &Tango::Group::read_attribute_asynch,
             R"doc(
                read_attribute_asynch(self, attr_name, forward=True,) -> int

                        Reads an attribute on each device in the group asynchronously.
                        The method sends the request to all devices and returns immediately.

                    Parameters :
                        - attr_name : (str) Name of the attribute to read.
                        - forward   : (bool) If it is set to true (the default) request is
                                        forwarded to subgroups. Otherwise, it is only applied
                                        to the local set of devices.

                    Return     : (int) request id. Pass the returned request id to
                                Group.read_attribute_reply() to obtain the results.

                    Throws     :)doc",
             py::arg("attr_name"),
             py::arg("forward") = true)
        .def("read_attribute_reply",
             PyGroup::read_attribute_reply,
             R"doc(
                read_attribute_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupAttrReply>

                        Returns the results of an asynchronous attribute reading.

                    Parameters :
                        - req_id     : (int) a request identifier previously returned by read_attribute_asynch.
                        - timeout_ms : (int) For each device in the hierarchy, if the attribute
                                        value is not yet available, read_attribute_reply
                                        wait timeout_ms milliseconds before throwing an
                                        exception. This exception will be part of the
                                        global reply. If timeout_ms is set to 0,
                                        read_attribute_reply waits "indefinitely".

                    Return     : (sequence<GroupAttrReply>)

                    Throws     :)doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0)
        .def("read_attributes_asynch",
             &Tango::Group::read_attributes_asynch,
             R"doc(
                read_attributes_asynch(self, attr_names, forward=True) -> int

                        Reads the attributes on each device in the group asynchronously.
                        The method sends the request to all devices and returns immediately.

                    Parameters :
                        - attr_names : (sequence<str>) Name of the attributes to read.
                        - forward    : (bool) If it is set to true (the default) request is
                                        forwarded to subgroups. Otherwise, it is only applied
                                        to the local set of devices.

                    Return     : (int) request id. Pass the returned request id to
                                Group.read_attributes_reply() to obtain the results.

                    Throws     :)doc",
             py::arg("attr_names"),
             py::arg("forward") = true)
        .def("read_attributes_reply",
             &PyGroup::read_attributes_reply,
             R"doc(
                read_attributes_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupAttrReply>

                        Returns the results of an asynchronous attribute reading.

                    Parameters :
                        - req_id     : (int) a request identifier previously returned by read_attribute_asynch.
                        - timeout_ms : (int) For each device in the hierarchy, if the attribute
                                       value is not yet available, read_attribute_reply
                                       ait timeout_ms milliseconds before throwing an
                                       exception. This exception will be part of the
                                       global reply. If timeout_ms is set to 0,
                                       read_attributes_reply waits "indefinitely".

                    Return     : (sequence<GroupAttrReply>)

                    Throws     :)doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0)
        .def("write_attribute_asynch",
             &PyGroup::write_attribute_asynch,
             R"doc(
                Writes an attribute on each device in the group asynchronously.
                The method sends the request to all devices and returns immediately.

                Parameters :
                    - attr : (str | AttributeInfoEx) Name or AttributeInfoEx of the attribute to write.
                    - value     : (any) Value to write. See DeviceProxy.write_attribute
                    - forward   : (bool) If it is set to true (the default) request is
                                  forwarded to subgroups. Otherwise, it is only applied
                                  to the local set of devices.
                    - multi     : (bool) If it is set to false (the default), the same
                                  value is applied to all devices in the group.
                                  Otherwise the value is interpreted as a sequence of
                                  values, and each value is applied to the corresponding
                                  device in the group. In this case len(value) must be
                                  equal to group.get_size()!

                Return     : (int) request id. Pass the returned request id to
                            Group.write_attribute_reply() to obtain the acknowledgements.

                Throws     :

                .. versionchanged:: 10.1.0 attr_name parameter was renamed to attr and
                                    added support for AttributeInfoEx for attr_values parameter
             )doc",
             py::arg("attr"),
             py::arg("value"),
             py::arg("forward") = true,
             py::arg("multi") = false)
        .def("write_attribute_reply",
             &Tango::Group::write_attribute_reply,
             py::call_guard<py::gil_scoped_release>(),
             R"doc(
                write_attribute_reply(self, req_id, timeout_ms=0 ) -> sequence<GroupReply>

                        Returns the acknowledgements of an asynchronous attribute writing.

                    Parameters :
                        - req_id     : (int) a request identifier previously returned by write_attribute_asynch.
                        - timeout_ms : (int) For each device in the hierarchy, if the acknowledgment
                                        is not yet available, write_attribute_reply
                                        wait timeout_ms milliseconds before throwing an
                                        exception. This exception will be part of the
                                        global reply. If timeout_ms is set to 0,
                                        write_attribute_reply waits "indefinitely".

                    Return     : (sequence<GroupReply>)

                    Throws     :)doc",
             py::arg("req_id"),
             py::arg("timeout_ms") = 0);
}
