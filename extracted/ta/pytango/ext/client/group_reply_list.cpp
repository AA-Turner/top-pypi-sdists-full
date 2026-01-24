/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

template <typename ListType, typename ItemType>
void bindGroupReplyList(py::module &m, const char *py_name) {
    py::class_<ListType>(m, py_name, py::dynamic_attr())
        .def(py::init<>())
        .def("has_failed", &ListType::has_failed)
        .def("reset", &ListType::reset)
        .def("push_back", &ListType::push_back)
        //        .def("__len__", &ListType::size)
        // I do not understand it, but if I just directly bind __len__ to size ,
        // I get recursion error, so have to do the following:
        .def("__len__", [](ListType &self) -> std::size_t {
            return self.size();
        })
        .def(
            "__getitem__", [](ListType &self, std::size_t i) -> ItemType & {
                if(i >= self.size()) {
                    throw py::index_error("Index out of range");
                }
                return self[i];
            },
            py::return_value_policy::reference_internal);
}

void export_group_reply_list(py::module &m) {
    bindGroupReplyList<Tango::GroupReplyList, Tango::GroupReply>(m, "GroupReplyList");
    bindGroupReplyList<Tango::GroupCmdReplyList, Tango::GroupCmdReply>(m, "GroupCmdReplyList");
    bindGroupReplyList<Tango::GroupAttrReplyList, Tango::GroupAttrReply>(m, "GroupAttrReplyList");
}
