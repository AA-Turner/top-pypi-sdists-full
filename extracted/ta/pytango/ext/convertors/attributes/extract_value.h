/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"

#define EXTRACT_VALUE(self, value_ptr)                                       \
    try {                                                                    \
        self >> value_ptr;                                                   \
    } catch(Tango::DevFailed & e) {                                          \
        if(strcmp(e.errors[0].reason.in(), "API_EmptyDeviceAttribute") != 0) \
            throw;                                                           \
    }
