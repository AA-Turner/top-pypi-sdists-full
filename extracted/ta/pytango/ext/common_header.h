/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "precompiled_header.hpp"

// cppTango decides whether telemetry support exists via TANGO_USE_TELEMETRY.
// For testing PyTango's no-telemetry code paths, allow masking that feature
// at PyTango build time without rebuilding cppTango.
#if defined(PYTANGO_FORCE_DISABLE_TELEMETRY)
  #ifdef TANGO_USE_TELEMETRY
    #undef TANGO_USE_TELEMETRY
  #endif
#endif

#if defined(TANGO_USE_TELEMETRY)
  #define PYTANGO_USE_TELEMETRY 1
#endif

// define some common project-wide aliases
#include "defs.h"

// See "Importing the API" for the why of these weird defines before
// the inclusion of numpy. They are needed so that you can do import_array
// in just one file while using numpy in all the project files.
// http://docs.scipy.org/doc/numpy/reference/c-api.array.html#miscellaneous
// - {
#define PY_ARRAY_UNIQUE_SYMBOL pytango_ARRAY_API
#define NO_IMPORT_ARRAY
#include <numpy/arrayobject.h>
// - }
