/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"

void force_mem_leak_1234_blocks() {
    // Keep pointers so the compiler can't optimize the allocations away
    static std::vector<void *> leaks;
    leaks.reserve(1234);
    for(int i = 0; i < 1234; ++i) {
        void *block = std::malloc(64);
        leaks.push_back(block);
    }
    std::cout << "Warning: forced memory leak of 1234 blocks for memory leak testing" << std::endl;
}

void export_mem_leak_helper(py::module_ &m) {
    m.def("_force_mem_leak_1234_blocks", &force_mem_leak_1234_blocks);
}
