/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

void export_locking_thread(py::module_ &m) {
    py::class_<Tango::LockingThread>(m, "LockingThread");
}
