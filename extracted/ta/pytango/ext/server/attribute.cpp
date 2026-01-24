/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"

#include "convertors/data_array_from_py.h"
#include "convertors/object_casters.h"

#include "pyutils.h"
#include "server/attribute_utils.h"
#include "server/attribute.h"

#ifdef WIN32
  #define PYTG_TIME_FROM_DOUBLE(dbl, tv)         \
      tv.time = static_cast<time_t>(floor(dbl)); \
      tv.millitm = static_cast<unsigned short>((dbl - tv.time) * 1.0e3);

  #define PYTG_NEW_TIME_FROM_DOUBLE(dbl, tv) \
      struct _timeb tv;                      \
      PYTG_TIME_FROM_DOUBLE(dbl, tv)
#else
  #define PYTG_TIME_FROM_DOUBLE(dbl, tv)                          \
      double sec = floor(dbl);                                    \
      tv.tv_usec = static_cast<suseconds_t>((dbl - sec) * 1.0E6); \
      tv.tv_sec = static_cast<time_t>(sec);

  #define PYTG_NEW_TIME_FROM_DOUBLE(dbl, tv) \
      struct timeval tv;                     \
      PYTG_TIME_FROM_DOUBLE(dbl, tv)
#endif

extern long TANGO_VERSION_HEX;

namespace PyAttribute {
/**
 * Tango Attribute set_value_date_quality wrapper for scalar attributes
 *
 * @param att attribute reference
 * @param value new attribute value
 * @param t timestamp
 * @param quality attribute quality
 */
template <int tangoTypeConst>
inline void __set_value_date_quality_scalar(Tango::Attribute &att,
                                            py::object &value,
                                            const double *time,
                                            const Tango::AttrQuality *quality) {
    typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;

    /*
       I hate doing because tango inside is doing a new again when
       set_value_date_quality is invoked with the release flag to true
       the other option would be to use per thread tango data like it was
       done in v3.0.4
       I prefer this one since it decouples TangoC++ from PyTango and creating
       a scalar is not so expensive after all
    */
    std::unique_ptr<TangoScalarType> cpp_val(new TangoScalarType);

    python_scalar_to_cpp<tangoTypeConst>::convert(value, *cpp_val);

    if(time != nullptr) {
        PYTG_NEW_TIME_FROM_DOUBLE(*time, tv);
        att.set_value_date_quality(cpp_val.release(), tv, *quality, 1, 0, true);
    } else {
        att.set_value(cpp_val.release(), 1, 0, true);
    }
}

template <int tangoTypeConst>
void __set_value_date_quality_array(Tango::Attribute &att,
                                    py::object &value,
                                    const double *time,
                                    const Tango::AttrQuality *quality,
                                    bool isImage) {
    typedef typename TANGO_const2type(tangoTypeConst) TangoScalarType;
    static const int tangoArrayTypeConst = TANGO_const2arrayconst(tangoTypeConst);

    TangoScalarType *data_buffer;

    py::size_t dim_x = 0, dim_y = 0;

    const std::string f_name = quality != nullptr ? "set_value_date_quality" : "set_value";

    data_buffer = python_to_cpp_buffer<tangoArrayTypeConst>(value,
                                                            MemoryAllocation::NEW,
                                                            f_name,
                                                            isImage,
                                                            dim_x,
                                                            dim_y);

    long res_dim_x = static_cast<long>(dim_x);
    long res_dim_y = static_cast<long>(dim_y);

    if(time != nullptr) {
        PYTG_NEW_TIME_FROM_DOUBLE(*time, tv);
        att.set_value_date_quality(data_buffer, tv, *quality, res_dim_x, res_dim_y, true);
    } else {
        att.set_value(data_buffer, res_dim_x, res_dim_y, true);
    }
}

template <>
void __set_value_date_quality_array<Tango::DEV_ENCODED>([[maybe_unused]] Tango::Attribute &att,
                                                        [[maybe_unused]] py::object &value,
                                                        [[maybe_unused]] const double *time,
                                                        [[maybe_unused]] const Tango::AttrQuality *quality,
                                                        [[maybe_unused]] bool isImage) {
    Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute",
                                   "DevEncoded is only supported for SCALAR attributes.",
                                   "set_value()");
}

inline void __set_encoded_attribute_value(Tango::Attribute &att, py::object &py_value) {
    auto *data = py_value.cast<Tango::EncodedAttribute *>();

    Tango::DevString *f = data->get_format();
    Tango::DevUChar *d = data->get_data();
    long size = data->get_size();

    if(*f == nullptr) {
        TangoSys_OMemStream o;
        o << "DevEncoded format for attribute " << att.get_name() << " not specified" << std::ends;

        TangoSys_OMemStream origin;
        origin << TANGO_EXCEPTION_ORIGIN << std::ends;

        Tango::Except::throw_exception("PyDs_DevEncodedFormatNotSpecified", o.str(), origin.str());
    }

    if(size == 0 || d == nullptr) {
        TangoSys_OMemStream o;
        o << "DevEncoded data for attribute " << att.get_name() << " not specified" << std::ends;

        TangoSys_OMemStream origin;
        origin << TANGO_EXCEPTION_ORIGIN << std::ends;

        Tango::Except::throw_exception("PyDs_DevEncodedDataNotSpecified", o.str(), origin.str());
    }

    Tango::DevString f_copy = Tango::string_dup(*f);

    Tango::DevUChar *d_copy = new Tango::DevUChar[static_cast<size_t>(size)];
    memcpy(d_copy, d, static_cast<size_t>(size));

    att.set_value(&f_copy, d_copy, size, true);
}

void set_generic_value(Tango::Attribute &att,
                       py::object &value,
                       double *time,
                       Tango::AttrQuality *quality) {
    if(py::isinstance<Tango::EncodedAttribute>(value)) {
        __set_encoded_attribute_value(att, value);
        return;
    }

    long type = att.get_data_type();
    Tango::AttrDataFormat format = att.get_data_format();

    const bool isScalar = (format == Tango::SCALAR);
    const bool isImage = (format == Tango::IMAGE);

    if(isScalar) {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type,
                                             __set_value_date_quality_scalar,
                                             att,
                                             value,
                                             time,
                                             quality);
    } else {
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(type,
                                             __set_value_date_quality_array,
                                             att,
                                             value,
                                             time,
                                             quality,
                                             isImage);
    }
}

/**
 * Tango Attribute set_value wrapper for DevEncoded attributes
 *
 * @param att attribute reference
 * @param encoding_str new attribute encoding info
 * @param data_str new attribute data
 * @param t timestamp
 * @param quality attribute quality
 */
void set_encoded_value(Tango::Attribute &att,
                       py::object &encoding,
                       py::object &data,
                       const double *time,
                       const Tango::AttrQuality *quality) {
    Tango::DevString encoding_char = from_python_str_to_cpp_char(encoding);
    Py_ssize_t size;
    Tango::DevString data_char = from_python_str_to_cpp_char(data, &size, true);

    if(time != nullptr) {
        PYTG_NEW_TIME_FROM_DOUBLE(*time, tv);
        att.set_value_date_quality(&encoding_char,
                                   reinterpret_cast<Tango::DevUChar *>(data_char),
                                   size,
                                   tv,
                                   *quality,
                                   true);
    } else {
        att.set_value(&encoding_char,
                      reinterpret_cast<Tango::DevUChar *>(data_char),
                      size,
                      true);
    }
}

template <typename TangoScalarType>
inline void _get_properties_multi_attr_prop(Tango::Attribute &att, py::object &multi_attr_prop) {
    Tango::MultiAttrProp<TangoScalarType> tg_multi_attr_prop;
    att.get_properties(tg_multi_attr_prop);

    to_py_object(tg_multi_attr_prop, multi_attr_prop);
}

inline py::object get_properties_multi_attr_prop(Tango::Attribute &att, py::object &multi_attr_prop) {
    long tangoTypeConst = att.get_data_type();
    TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_NAME(tangoTypeConst, _get_properties_multi_attr_prop, att, multi_attr_prop);
    return multi_attr_prop;
}

template <typename TangoScalarType>
inline void _set_properties_multi_attr_prop(Tango::Attribute &att, py::object &multi_attr_prop) {
    Tango::MultiAttrProp<TangoScalarType> tg_multi_attr_prop;
    from_py_object(multi_attr_prop, tg_multi_attr_prop);
    att.set_properties(tg_multi_attr_prop);
}

void set_properties_multi_attr_prop(Tango::Attribute &att, py::object &multi_attr_prop) {
    long tangoTypeConst = att.get_data_type();
    TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_NAME(tangoTypeConst, _set_properties_multi_attr_prop, att, multi_attr_prop);
}

void set_upd_properties(Tango::Attribute &att, py::object &attr_cfg) {
    auto tg_attr_cfg = attr_cfg.cast<Tango::AttributeConfig_3>();
    att.set_upd_properties(tg_attr_cfg);
}

void set_upd_properties(Tango::Attribute &att, py::object &attr_cfg, py::object &dev_name) {
    auto tg_attr_cfg = attr_cfg.cast<Tango::AttributeConfig_3>();
    std::string tg_dev_name = dev_name.cast<std::string>();
    att.set_upd_properties(tg_attr_cfg, tg_dev_name);
}

inline void generic_fire_event(Tango::Attribute &self, Tango::EventType eventType) {
    switch(eventType) {
    case Tango::EventType::CHANGE_EVENT:
        self.fire_change_event();
        break;
    case Tango::EventType::ALARM_EVENT:
        self.fire_alarm_event();
        break;
    default:
        throw std::invalid_argument("Unknown event type");
    }
}

inline void generic_fire_event(Tango::Attribute &self, Tango::EventType eventType, py::object &exception) {
    try {
        Tango::DevFailed except_convert = exception.cast<Tango::DevFailed>();
        switch(eventType) {
        case Tango::EventType::CHANGE_EVENT:
            self.fire_change_event(&except_convert);
            break;
        case Tango::EventType::ALARM_EVENT:
            self.fire_alarm_event(&except_convert);
            break;
        default:
            throw std::invalid_argument("Unknown event type");
        }
        return;
    } catch([[maybe_unused]] const py::cast_error &e) {
        TangoSys_OMemStream o;
        o << "Wrong Python argument type for attribute " << self.get_name() << ". Expected a DevFailed." << std::ends;

        TangoSys_OMemStream origin;
        origin << TANGO_EXCEPTION_ORIGIN << std::ends;

        Tango::Except::throw_exception("PyDs_WrongPythonDataTypeForAttribute", o.str(), origin.str());
    }
}

// usually not necessary to rewrite but with direct declaration the compiler
// gives an error. It seems to be because the tango method definition is not
// in the header file.
inline bool is_polled(Tango::Attribute &self) {
    return self.is_polled();
}
} // namespace PyAttribute

void export_attribute(py::module &m) {
    py::native_enum<Tango::Attribute::alarm_flags>(m, "alarm_flags", "enum.IntEnum")
        .value("min_level", Tango::Attribute::min_level)
        .value("max_level", Tango::Attribute::max_level)
        .value("rds", Tango::Attribute::rds)
        .value("min_warn", Tango::Attribute::min_warn)
        .value("max_warn", Tango::Attribute::max_warn)
        .value("numFlags", Tango::Attribute::numFlags)
        .finalize();
    py::object alarm_flags_class = m.attr("alarm_flags");
    add_names_values_to_native_enum(alarm_flags_class);

    py::class_<Tango::Attribute>(m,
                                 "Attribute",
                                 "This class represents a Tango attribute")
        .def("is_write_associated",
             &Tango::Attribute::is_writ_associated,
             R"doc(
                is_write_associated(self) -> bool

                    Check if the attribute has an associated writable attribute.

                :returns: True if there is an associated writable attribute
                :rtype: bool)doc")
        .def("is_min_alarm",
             &Tango::Attribute::is_min_alarm,
             R"doc(
                is_min_alarm(self) -> bool

                    Check if the attribute is in minimum alarm condition.

                :returns: true if the attribute is in alarm condition (read value below the min. alarm).
                :rtype: bool)doc")
        .def("is_max_alarm",
             &Tango::Attribute::is_max_alarm,
             R"doc(
                is_max_alarm(self) -> bool

                    Check if the attribute is in maximum alarm condition.

                :returns: true if the attribute is in alarm condition (read value above the max. alarm).
                :rtype: bool)doc")
        .def("is_min_warning",
             &Tango::Attribute::is_min_warning,
             R"doc(
                is_min_warning(self) -> bool

                    Check if the attribute is in minimum warning condition.

                :returns: true if the attribute is in warning condition (read value below the min. warning).
                :rtype: bool)doc")
        .def("is_max_warning",
             &Tango::Attribute::is_max_warning,
             R"doc(
                is_max_warning(self) -> bool

                    Check if the attribute is in maximum warning condition.

                :returns: true if the attribute is in warning condition (read value above the max. warning).
                :rtype: bool)doc")
        .def("is_rds_alarm",
             &Tango::Attribute::is_rds_alarm,
             R"doc(
                is_rds_alarm(self) -> bool

                    Check if the attribute is in RDS alarm condition.

                :returns: true if the attribute is in RDS condition (Read Different than Set).
                :rtype: bool)doc")
        .def("is_polled",
             &PyAttribute::is_polled,
             R"doc(
                is_polled(self) -> bool

                    Check if the attribute is polled.

                :returns: true if the attribute is polled.
                :rtype: bool)doc")
        .def("check_alarm",
             &Tango::Attribute::check_alarm,
             R"doc(
                check_alarm(self) -> bool

                    Check if the attribute read value is below/above the alarm level.

                :returns: true if the attribute is in alarm condition.
                :rtype: bool

                :raises DevFailed: If no alarm level is defined.)doc")
        .def("get_writable",
             &Tango::Attribute::get_writable,
             R"doc(
                get_writable(self) -> AttrWriteType

                    Get the attribute writable type (RO/WO/RW).

                :returns: The attribute write type.
                :rtype: AttrWriteType)doc")
        .def("get_name",
             static_cast<const std::string &(Tango::Attribute::*) () const>(&Tango::Attribute::get_name),
             py::return_value_policy::copy,
             R"doc(
                get_name(self) -> str

                    Get attribute name.

                :returns: The attribute name
                :rtype: str)doc")
        .def("get_data_type",
             &Tango::Attribute::get_data_type,
             R"doc(
                get_data_type(self) -> int

                    Get attribute data type.

                :returns: the attribute data type
                :rtype: int)doc")
        .def("get_data_format",
             &Tango::Attribute::get_data_format,
             R"doc(
                get_data_format(self) -> AttrDataFormat

                    Get attribute data format.

                :returns: the attribute data format
                :rtype: AttrDataFormat)doc")
        .def("get_assoc_name",
             &Tango::Attribute::get_assoc_name,
             py::return_value_policy::copy,
             R"doc(
                get_assoc_name(self) -> str

                    Get name of the associated writable attribute.

                :returns: the associated writable attribute name
                :rtype: str)doc")
        .def("get_assoc_ind",
             &Tango::Attribute::get_assoc_ind,
             R"doc(
                get_assoc_ind(self) -> int

                    Get index of the associated writable attribute.

                :returns: the index in the main attribute vector of the associated writable attribute
                :rtype: int)doc")
        .def("set_assoc_ind",
             &Tango::Attribute::set_assoc_ind,
             R"doc(
                set_assoc_ind(self, index)

                    Set index of the associated writable attribute.

                :param index: The new index in the main attribute vector of the associated writable attribute
                :type index: int)doc",
             py::arg("index"))
        .def("get_date",
             &Tango::Attribute::get_date,
             py::return_value_policy::copy,
             R"doc(
                get_date(self) -> TimeVal

                    Get a COPY of the attribute date.

                :returns: the attribute date
                :rtype: TimeVal)doc")
        .def("set_date",
             py::overload_cast<Tango::TimeVal &>(&Tango::Attribute::set_date),
             R"doc(
                set_date(self, new_date)

                    Set attribute date.

                :param new_date: the attribute date
                :type new_date: TimeVal)doc",
             py::arg("new_date"))
        .def("get_label",
             &Tango::Attribute::get_label,
             py::return_value_policy::copy,
             R"doc(
                get_label(self) -> str

                    Get attribute label property.

                :returns: the attribute label
                :rtype: str)doc")
        .def("get_quality",
             &Tango::Attribute::get_quality,
             py::return_value_policy::copy,
             R"doc(
                get_quality(self) -> AttrQuality

                    Get a COPY of the attribute data quality.

                :returns: the attribute data quality
                :rtype: AttrQuality)doc")
        .def("set_quality",
             &Tango::Attribute::set_quality,
             R"doc(
                set_quality(self, quality, send_event=False)

                    Set attribute data quality.

                :param quality: the new attribute data quality
                :type quality: AttrQuality
                :param send_event: true if a change event should be sent. Default is false.
                :type send_event: bool)doc",
             py::arg("quality"),
             py::arg("send_event") = false)
        .def("get_data_size",
             &Tango::Attribute::get_data_size,
             R"doc(
                get_data_size(self)

                    Get attribute data size.

                :returns: the attribute data size
                :rtype: int)doc")
        .def("get_x",
             &Tango::Attribute::get_x,
             R"doc(
                get_x(self) -> int

                    Get attribute data size in x dimension.

                :returns: the attribute data size in x dimension. Set to 1 for scalar attribute
                :rtype: int)doc")
        .def("get_max_dim_x",
             &Tango::Attribute::get_max_dim_x,
             R"doc(
                get_max_dim_x(self) -> int

                    Get attribute maximum data size in x dimension.

                :returns: the attribute maximum data size in x dimension. Set to 1 for scalar attribute
                :rtype: int)doc")
        .def("get_y",
             &Tango::Attribute::get_y,
             R"doc(
                get_y(self) -> int

                    Get attribute data size in y dimension.

                :returns: the attribute data size in y dimension. Set to 0 for scalar attribute
                :rtype: int)doc")
        .def("get_max_dim_y",
             &Tango::Attribute::get_max_dim_y,
             R"doc(
                get_max_dim_y(self) -> int

                    Get attribute maximum data size in y dimension.

                :returns: the attribute maximum data size in y dimension. Set to 0 for scalar attribute
                :rtype: int)doc")
        .def("get_polling_period",
             &Tango::Attribute::get_polling_period,
             R"doc(
                get_polling_period(self) -> int

                    Get attribute polling period.

                :returns: The attribute polling period in mS. Set to 0 when the attribute is not polled
                :rtype: int)doc")
        .def("set_attr_serial_model",
             &Tango::Attribute::set_attr_serial_model,
             R"doc(
                set_attr_serial_model(self, ser_model) -> None

                    Set attribute serialization model.

                    This method allows the user to choose the attribute serialization model.

                :param ser_model: The new serialisation model. The
                                  serialization model must be one of ATTR_BY_KERNEL,
                                  ATTR_BY_USER or ATTR_NO_SYNC
                :type ser_model: AttrSerialModel

                New in PyTango 7.1.0)doc",
             py::arg("ser_model"))
        .def("get_attr_serial_model",
             &Tango::Attribute::get_attr_serial_model,
             R"doc(
                get_attr_serial_model(self) -> AttrSerialModel

                    Get attribute serialization model.

                :returns: The attribute serialization model
                :rtype: AttrSerialModel

                New in PyTango 7.1.0)doc")

        .def(
            "set_min_alarm",
            [](Tango::Attribute &attr, py::object &value) {
                set_value_limit(attr, value, TargetValue::ALARM_MIN);
            },
            py::arg("value"))
        .def(
            "set_max_alarm",
            [](Tango::Attribute &attr, py::object &value) {
                set_value_limit(attr, value, TargetValue::ALARM_MAX);
            },
            py::arg("value"))
        .def(
            "set_min_warning",
            [](Tango::Attribute &attr, py::object &value) {
                set_value_limit(attr, value, TargetValue::WARNING_MIN);
            },
            py::arg("value"))
        .def(
            "set_max_warning",
            [](Tango::Attribute &attr, py::object &value) {
                set_value_limit(attr, value, TargetValue::WARNING_MAX);
            },
            py::arg("value"))

        .def("get_min_alarm",
             [](Tango::Attribute &attr) {
                 return get_value_limit(attr, TargetValue::ALARM_MIN);
             })
        .def("get_max_alarm",
             [](Tango::Attribute &attr) {
                 return get_value_limit(attr, TargetValue::ALARM_MAX);
             })
        .def("get_min_warning",
             [](Tango::Attribute &attr) {
                 return get_value_limit(attr, TargetValue::WARNING_MIN);
             })
        .def("get_max_warning",
             [](Tango::Attribute &attr) {
                 return get_value_limit(attr, TargetValue::WARNING_MAX);
             })

        .def("value_is_set",
             &Tango::Attribute::value_is_set,
             R"doc(
                value_is_set(self) -> bool

                :return: true if attribute has a value
                :rtype: bool)doc")
        .def("reset_value",
             &Tango::Attribute::reset_value,
             R"doc(
                reset_value(self) -> None

                    Clear attribute value)doc")

        .def("get_disp_level",
             &Tango::Attribute::get_disp_level,
             R"doc(
                get_disp_level(self) -> DisplLevel

                :return: attribute display level
                :rtype: DispLevel)doc")

        .def("change_event_subscribed",
             &Tango::Attribute::change_event_subscribed,
             R"doc(
                change_event_subscribed(self) -> bool

                :return: true if there are some subscriber listening for change event
                :rtype: bool)doc")
        .def("alarm_event_subscribed",
             &Tango::Attribute::alarm_event_subscribed,
             R"doc(
                alarm_event_subscribed(self) -> bool

                :return: true if there are some subscriber listening for alarm event
                :rtype: bool)doc")
        .def("periodic_event_subscribed",
             &Tango::Attribute::periodic_event_subscribed,
             R"doc(
                periodic_event_subscribed(self) -> bool

                :return: true if there are some subscriber listening for periodic event
                :rtype: bool)doc")
        .def("archive_event_subscribed",
             &Tango::Attribute::archive_event_subscribed,
             R"doc(
                archive_event_subscribed(self) -> bool

                :return: true if there are some subscriber listening for archive event
                :rtype: bool)doc")
        .def("user_event_subscribed",
             &Tango::Attribute::user_event_subscribed,
             R"doc(
                user_event_subscribed(self) -> bool

                :return: true if there are some subscriber listening for user event
                :rtype: bool)doc")

        .def("use_notifd_event",
             &Tango::Attribute::use_notifd_event,
             R"doc(
                use_notifd_event(self) -> bool

                :return: true if notifd events are emited
                :rtype: bool)doc")
        .def("use_zmq_event",
             &Tango::Attribute::use_zmq_event,
             R"doc(
                use_zmq_event(self) -> bool

                :return: true if zmq events are emited
                :rtype: bool)doc")

        .def(
            "_set_value",
            [](Tango::Attribute &attr, py::object &data) {
                PyAttribute::set_generic_value(attr, data);
            },
            py::arg("data"))
        .def(
            "_set_value_date_quality",
            [](Tango::Attribute &attr, py::object &data, double time, Tango::AttrQuality quality) {
                PyAttribute::set_generic_value(attr, data, &time, &quality);
            },
            py::arg("data"),
            py::arg("time"),
            py::arg("quality"))
        .def(
            "_set_value",
            [](Tango::Attribute &attr, py::object &encoding, py::object &data) {
                PyAttribute::set_encoded_value(attr, encoding, data);
            },
            py::arg("encoding"),
            py::arg("data"))

        .def(
            "_set_value_date_quality",
            [](Tango::Attribute &attr, py::object &encoding, py::object &data, double time, Tango::AttrQuality quality) {
                PyAttribute::set_encoded_value(attr, encoding, data, &time, &quality);
            },
            py::arg("encoding"),
            py::arg("data"),
            py::arg("time"),
            py::arg("quality"))

        .def("set_change_event",
             &Tango::Attribute::set_change_event,
             R"doc(
                Set a flag to indicate that the server fires change events manually,
                without the polling to be started for the attribute.

                If the detect parameter is set to true, the criteria specified for the
                change event (rel_change and abs_change) are verified and
                the event is only pushed if a least one of them are fulfilled
                (change in value compared to previous event exceeds a threshold).
                If detect is set to false the event is fired without
                any value checking!

                :param implemented: True when the server fires change events manually.
                :type implemented: bool
                :param detect: (optional, default is True) Triggers the verification of
                                the change event properties when set to true.
                :type detect: bool

                New in PyTango 7.1.0)doc",
             py::arg("implemented"),
             py::arg("detect") = true)
        .def("set_alarm_event",
             &Tango::Attribute::set_alarm_event,
             R"doc(
                Set a flag to indicate that the server fires alarm events manually,
                without the polling to be started for the attribute.

                If the detect parameter is set to true, the criteria specified for the
                alarm event (rel_change and abs_change) are verified and
                the event is only pushed if a least one of them are fulfilled
                (change in value compared to previous event exceeds a threshold).
                If detect is set to false the event is fired without
                any value checking!

                :param implemented: True when the server fires alarm events manually.
                :type implemented: bool
                :param detect: (optional, default is True) Triggers the verification of
                                the alarm event properties when set to true.
                :type detect: bool

                .. versionadded:: 10.0.0)doc",
             py::arg("implemented"),
             py::arg("detect") = true)
        .def("set_archive_event",
             &Tango::Attribute::set_archive_event,
             R"doc(
                Set a flag to indicate that the server fires archive events manually,
                without the polling to be started for the attribute.

                If the detect parameter is set to true, the criteria specified for the
                archive event (rel_change and abs_change) are verified and
                the event is only pushed if a least one of them are fulfilled
                (change in value compared to previous event exceeds a threshold).

                If detect is set to false the event is fired without any value checking!

                :param implemented: True when the server fires archive events manually.
                :type implemented: bool
                :param detect: (optional, default is True) Triggers the verification of
                                the archive event properties when set to true.
                :type detect: bool

                New in PyTango 7.1.0)doc",
             py::arg("implemented"),
             py::arg("detect") = true)

        .def("is_change_event",
             &Tango::Attribute::is_change_event,
             R"doc(
                is_change_event(self) -> bool

                    Check if the change event is fired manually (without polling) for this attribute.

                :returns: True if a manual fire change event is implemented.
                :rtype: bool

                New in PyTango 7.1.0)doc")
        .def("is_check_change_criteria",
             &Tango::Attribute::is_check_change_criteria,
             R"doc(
                is_check_change_criteria(self) -> bool

                    Check if the change event criteria should be checked when firing the
                    event manually.

                :returns: True if a change event criteria will be checked.
                :rtype: bool

                New in PyTango 7.1.0)doc")
        .def("is_alarm_event",
             &Tango::Attribute::is_alarm_event,
             R"doc(
                is_alarm_event(self) -> bool

                    Check if the alarm event is fired manually for this attribute.

                :returns: True if a manual fire alarm event is implemented.
                :rtype: bool

                New in PyTango 10.0.0)doc")
        .def("is_check_alarm_criteria",
             &Tango::Attribute::is_check_alarm_criteria,
             R"doc(
                is_check_alarm_criteria(self) -> bool

                    Check if the alarm event criteria should be checked when firing the
                    event manually.

                :returns: True if a change event criteria will be checked.
                :rtype: bool

                New in PyTango 10.0.0)doc")
        .def("is_archive_event",
             &Tango::Attribute::is_archive_event,
             R"doc(
                is_archive_event(self) -> bool

                    Check if the archive event is fired manually (without polling) for this attribute.

                :returns: True if a manual fire archive event is implemented.
                :rtype: bool

                New in PyTango 7.1.0)doc")
        .def("is_check_archive_criteria",
             &Tango::Attribute::is_check_archive_criteria,
             R"doc(
                is_check_archive_criteria(self) -> bool

                    Check if the archive event criteria should be checked when firing the
                    event manually.

                :returns: True if a archive event criteria will be checked.
                :rtype: bool

                New in PyTango 7.1.0)doc")
        .def("set_data_ready_event",
             &Tango::Attribute::set_data_ready_event,
             R"doc(
                set_data_ready_event(self, implemented)

                    Set a flag to indicate that the server fires data ready events.

                :param implemented: True when the server fires data ready events manually.
                :type implemented: bool

                New in PyTango 7.2.0)doc",
             py::arg("implemented"))
        .def("is_data_ready_event",
             &Tango::Attribute::is_data_ready_event,
             R"doc(
                is_data_ready_event(self) -> bool

                    Check if the data ready event is fired manually (without polling)
                    for this attribute.

                :returns: True if a manual fire data ready event is implemented.
                :rtype: bool

                New in PyTango 7.2.0)doc")
        .def("remove_configuration",
             &Tango::Attribute::remove_configuration,
             R"doc(
                remove_configuration(self)

                    Remove the attribute configuration from the database.

                    This method can be used to clean-up all the configuration of an
                    attribute to come back to its default values or the remove all
                    configuration of a dynamic attribute before deleting it.

                    The method removes all configured attribute properties and removes
                    the attribute from the list of polled attributes.

                    New in PyTango 7.1.0)doc")

        /*
        .def("_get_properties", &PyAttribute::get_properties)
        .def("_get_properties_2", &PyAttribute::get_properties_2)
        .def("_get_properties_3", &PyAttribute::get_properties_3)
        */
        .def("_get_properties_multi_attr_prop",
             &PyAttribute::get_properties_multi_attr_prop,
             py::arg("multi_attr_prop"))

        /*
        .def("_set_properties", &PyAttribute::set_properties)
        .def("_set_properties_3", &PyAttribute::set_properties_3)
        */
        .def("_set_properties_multi_attr_prop",
             &PyAttribute::set_properties_multi_attr_prop,
             py::arg("multi_attr_prop"))

        .def("set_upd_properties",
             py::overload_cast<Tango::Attribute &, py::object &>(&PyAttribute::set_upd_properties),
             py::arg("attr_cfg"))
        .def("set_upd_properties",
             py::overload_cast<Tango::Attribute &, py::object &, py::object &>(&PyAttribute::set_upd_properties),
             py::arg("attr_cfg"),
             py::arg("dev_name"))

        .def("fire_change_event",
             [](Tango::Attribute &attr) {
                 PyAttribute::generic_fire_event(attr, Tango::EventType::CHANGE_EVENT);
             })
        .def(
            "fire_change_event",
            [](Tango::Attribute &attr, py::object exception) {
                PyAttribute::generic_fire_event(attr, Tango::EventType::CHANGE_EVENT, exception);
            },
            py::arg("exception"))
        .def("fire_alarm_event",
             [](Tango::Attribute &attr) {
                 PyAttribute::generic_fire_event(attr, Tango::EventType::ALARM_EVENT);
             })
        .def(
            "fire_alarm_event",
            [](Tango::Attribute &attr, py::object exception) {
                PyAttribute::generic_fire_event(attr, Tango::EventType::ALARM_EVENT, exception);
            },
            py::arg("exception"));
}
