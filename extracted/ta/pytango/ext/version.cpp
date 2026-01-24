/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"

void export_version(py::module_ &m) {
    m.attr("__tangolib_version__") = Tango::TgLibVers;
}
