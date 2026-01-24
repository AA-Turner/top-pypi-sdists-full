/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

typedef std::vector<std::string> StdStringVector;
typedef std::vector<long> StdLongVector;
typedef std::vector<double> StdDoubleVector;

typedef std::vector<Tango::NamedDevFailed> StdNamedDevFailedVector;

#ifndef TANGO_VERSION_NB
  #define TANGO_VERSION_NB TANGO_VERSION_MAJOR * 10000 + TANGO_VERSION_MINOR * 100 + TANGO_VERSION_MINOR
#endif

// Useful constants for exceptions

inline const char *param_must_be_seq = "Parameter must be a string or a python "
                                       "sequence (e.x.: a tuple or a list)";

inline const char *value_attr_name = "value";
inline const char *w_value_attr_name = "w_value";
inline const char *type_attr_name = "type";
inline const char *is_empty_attr_name = "is_empty";
inline const char *has_failed_attr_name = "has_failed";

namespace PyTango {
enum ExtractAs {
    ExtractAsNumpy,
    ExtractAsByteArray,
    ExtractAsBytes,
    ExtractAsTuple,
    ExtractAsList,
    ExtractAsString,
    ExtractAsPyTango3,
    ExtractAsNothing
};

enum ImageFormat {
    RawImage,
    JpegImage
};

enum GreenMode {
    GreenModeSynchronous,
    GreenModeFutures,
    GreenModeGevent,
    GreenModeAsyncio
};
} // namespace PyTango

// internal enum
enum TargetValue {
    VALUE_MIN,
    ALARM_MIN,
    WARNING_MIN,
    WARNING_MAX,
    ALARM_MAX,
    VALUE_MAX
};

// internal enum
enum EncodingType {
    GRAY8,
    JPEG_GRAY8,
    GRAY16,
    RGB24,
    JPEG_RGB24,
    JPEG_RGB32
};

// internal enum
enum DevVarNumericStringArray {
    LONG_STRING,
    DOUBLE_STRING
};
