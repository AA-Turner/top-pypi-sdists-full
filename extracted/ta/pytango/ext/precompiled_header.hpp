/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

// These files are really basic, used everywhere within the project
// but they take a while (seconds!) to process.
// We don't want to waste those seconds for each cpp file, so we
// use this precompiled header.

#include <cassert>
#include <iostream>
#include <string>
#include <sstream>
#include <memory>
#include <vector>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>
#include <pybind11/stl_bind.h>
#include <pybind11/numpy.h>
#include <pybind11/pytypes.h>
#include <pybind11/chrono.h>
#include <pybind11/native_enum.h>

#include <tango/tango.h>

namespace py = pybind11;
