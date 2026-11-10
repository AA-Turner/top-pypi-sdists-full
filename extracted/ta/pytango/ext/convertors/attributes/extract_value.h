/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"

// Extracting from an empty Tango::DeviceAttribute throws; that is not an error here,
// and value is left untouched, so the caller must pass an initialised value.
template <typename ValueType>
inline void extract_value(Tango::DeviceAttribute &self, ValueType &value) {
    try {
        self >> value;
    } catch(Tango::DevFailed &e) {
        if(e.errors.length() == 0 || strcmp(e.errors[0].reason.in(), "API_EmptyDeviceAttribute") != 0) {
            throw;
        }
    }
}
