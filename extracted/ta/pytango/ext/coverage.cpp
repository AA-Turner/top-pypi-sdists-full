/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"

#ifdef PYTANGO_ENABLE_COVERAGE

extern "C" void __gcov_dump();

void dump_cpp_coverage() {
    __gcov_dump();
}

#else

void dump_cpp_coverage() {
    throw std::runtime_error("No coverage support enabled, pass \"-DPYTANGO_ENABLE_COVERAGE=True\" to cmake "
                             "and recompile to enable it.");
}

#endif

void export_coverage_helper(py::module_ &m) {
    m.def("_dump_cpp_coverage", &dump_cpp_coverage);
}
