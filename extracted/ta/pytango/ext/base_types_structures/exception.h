/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "convertors/type_casters.h"

/**
 * Handles the current python exception:
 * If a PyTango DevFailed -> translates it to C++ and throws the DevFailed
 * If a generic python exception -> translates it to C++ DevFailed and throws the DevFailed
 *
 * @param[in] eas the python exception
 * @param[in] reason string (optional, if set adds DevError to the error stack)
 * @param[in] desc string (optional, if set adds DevError to the error stack)
 * @param[in] origin string (optional, if set adds DevError to the error stack)
 */
[[noreturn]] void handle_python_exception(py::error_already_set &eas,
                                          const std::string &reason = "",
                                          const std::string &desc = "",
                                          const std::string &origin = "");
