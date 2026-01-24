/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "precompiled_header.hpp"

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
