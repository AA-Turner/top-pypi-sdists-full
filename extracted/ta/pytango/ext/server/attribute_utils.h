/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#ifndef PYTANGO_ATTRIBUTE_UTILS_H
#define PYTANGO_ATTRIBUTE_UTILS_H

#include "common_header.h"
#include "convertors/type_casters.h"

#include "server/attribute_utils.h"

#define __SET_ALARM_WARNING(self, c_value, target)     \
    switch(target) {                                   \
    case TargetValue::ALARM_MIN:                       \
        self.set_min_alarm(c_value);                   \
        break;                                         \
    case TargetValue::WARNING_MIN:                     \
        self.set_min_warning(c_value);                 \
        break;                                         \
    case TargetValue::WARNING_MAX:                     \
        self.set_max_warning(c_value);                 \
        break;                                         \
    case TargetValue::ALARM_MAX:                       \
        self.set_max_alarm(c_value);                   \
        break;                                         \
    default:                                           \
        throw std::invalid_argument("Unknown target"); \
    }

template <int tangoTypeConst>
inline void _set_value_limit(Tango::Attribute &self, py::object &value, TargetValue &target) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    TangoScalarType c_value;
    python_scalar_to_cpp<tangoTypeConst>::convert(value, c_value);
    __SET_ALARM_WARNING(self, c_value, target)
}

inline void _set_value_limit(Tango::Attribute &self, std::string &c_value, TargetValue &target) {
    __SET_ALARM_WARNING(self, c_value, target)
}

#define __SET_VALUE(self, c_value, target)             \
    switch(target) {                                   \
    case TargetValue::VALUE_MIN:                       \
        self.set_min_value(c_value);                   \
        break;                                         \
    case TargetValue::VALUE_MAX:                       \
        self.set_max_value(c_value);                   \
        break;                                         \
    default:                                           \
        throw std::invalid_argument("Unknown target"); \
    }

template <int tangoTypeConst>
inline void _set_value_limit(Tango::WAttribute &self, py::object &value, TargetValue &target) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    TangoScalarType c_value;
    python_scalar_to_cpp<tangoTypeConst>::convert(value, c_value);
    __SET_VALUE(self, c_value, target)
}

inline void _set_value_limit(Tango::WAttribute &self, std::string &c_value, TargetValue &target) {
    __SET_VALUE(self, c_value, target)
}

template <typename AttrType>
void set_value_limit(AttrType &self, py::object &value, TargetValue target) {
    if(py::str::check_(value)) {
        std::string c_value = value.cast<std::string>();
        _set_value_limit(self, c_value, target);
    } else {
        long tango_type = self.get_data_type();
        // TODO: the below line is a neat trick to properly raise a Tango exception if a property is set
        // for one of the forbidden attribute data types; code dependent on Tango C++ implementation
        if(tango_type == Tango::DEV_STRING || tango_type == Tango::DEV_BOOLEAN ||
           tango_type == Tango::DEV_STATE) {
            tango_type = Tango::DEV_DOUBLE;
        } else if(tango_type == Tango::DEV_ENCODED) {
            tango_type = Tango::DEV_UCHAR;
        }

        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(tango_type, _set_value_limit, self, value, target);
    }
}

#define __GET_ALARM_WARNING(att, tg_val, source)       \
    switch(source) {                                   \
    case TargetValue::ALARM_MIN:                       \
        att.get_min_alarm(tg_val);                     \
        break;                                         \
    case TargetValue::WARNING_MIN:                     \
        att.get_min_warning(tg_val);                   \
        break;                                         \
    case TargetValue::WARNING_MAX:                     \
        att.get_max_warning(tg_val);                   \
        break;                                         \
    case TargetValue::ALARM_MAX:                       \
        att.get_max_alarm(tg_val);                     \
        break;                                         \
    default:                                           \
        throw std::invalid_argument("Unknown target"); \
    }

template <int tangoTypeConst>
inline py::object _get_value_limit(Tango::Attribute &att, TargetValue &source) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    TangoScalarType tg_val;
    __GET_ALARM_WARNING(att, tg_val, source)

    return py::cast(tg_val);
}

#define __GET_VALUE(att, tg_val, source)               \
    switch(source) {                                   \
    case TargetValue::VALUE_MIN:                       \
        att.get_min_value(tg_val);                     \
        break;                                         \
    case TargetValue::VALUE_MAX:                       \
        att.get_max_value(tg_val);                     \
        break;                                         \
    default:                                           \
        throw std::invalid_argument("Unknown target"); \
    }

template <int tangoTypeConst>
inline py::object _get_value_limit(Tango::WAttribute &att, TargetValue &source) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    TangoScalarType tg_val;
    __GET_VALUE(att, tg_val, source)

    return py::cast(tg_val);
}

template <typename AttrType>
py::object get_value_limit(AttrType &att, TargetValue source) {
    long tango_type = att.get_data_type();

    if(tango_type == Tango::DEV_ENCODED) {
        tango_type = Tango::DEV_UCHAR;
    }

    TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(tango_type, return _get_value_limit, att, source);
    return py::none();
}

#endif // PYTANGO_ATTRIBUTE_UTILS_H
