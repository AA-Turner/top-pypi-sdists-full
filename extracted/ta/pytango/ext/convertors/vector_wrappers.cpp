/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "vector_wrappers.h"

// Binding macro
#define BIND_VECTOR_WRAPPER(TYPE)                                                                   \
    py::class_<VectorWrapper<TYPE>, std::shared_ptr<VectorWrapper<TYPE>>>(m, #TYPE "VectorWrapper") \
        .def(py::init<std::vector<TYPE *> *>())                                                     \
        .def("__getitem__", &VectorWrapper<TYPE>::get_item)                                         \
        .def("__setitem__", &VectorWrapper<TYPE>::set_item)                                         \
        .def("append", &VectorWrapper<TYPE>::append)                                                \
        .def("__len__", &VectorWrapper<TYPE>::size);

void export_vector_wrappers(py::module &m) {
    BIND_VECTOR_WRAPPER(Tango::Attr)
}
