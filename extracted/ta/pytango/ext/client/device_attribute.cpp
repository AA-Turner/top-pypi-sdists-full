/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#include "common_header.h"
#include "convertors/type_casters.h"
#include "convertors/attributes/scalar_python_to_cpp.h"
#include "convertors/attributes/array_python_to_cpp.h"
#include "convertors/attributes/scalar_cpp_to_python.h"
#include "convertors/attributes/array_cpp_to_python.h"

#include "convertors/data_array_from_py.h"

#include "pyutils.h"
#include "client/device_attribute.h"

// Why am I storing 'type' as a python attribute with object::attr
// instead of as a property calling DeviceAttribute::get_type here?
// Because after 'extracting`, any call to get_type() will fail. Same
// for "value" and "w_value". And for has_failed and is_empty...

namespace PyDeviceAttribute {

void attribute_values_from_cpp_into_python(Tango::DeviceAttribute &self,
                                           py::object &py_value,
                                           PyTango::ExtractAs extract_as /*=ExtractAsNumpy*/) {
    // We do not want is_empty to launch an exception!!
    self.reset_exceptions(Tango::DeviceAttribute::isempty_flag);

    const bool has_failed = self.has_failed();
    py_value.attr(has_failed_attr_name) = py::cast(has_failed);

    const bool is_empty = self.is_empty();
    py_value.attr(is_empty_attr_name) = py::cast(is_empty);

    const int quality = self.get_quality();
    const bool is_invalid = quality == Tango::ATTR_INVALID;

    const int data_type = self.get_type();
    const bool failed_data_type = ((data_type < 0) || (data_type == Tango::DATA_TYPE_UNKNOWN));

    Tango::AttrDataFormat data_format = self.get_data_format();
    py_value.attr(type_attr_name) = py::cast(static_cast<Tango::CmdArgType>(data_type));

    if(failed_data_type || has_failed || is_invalid) {
        // In these cases we cannot/should not (to maintain backward compatibility) extract data
        py_value.attr(value_attr_name) = py::none();
        py_value.attr(w_value_attr_name) = py::none();
        return;
    }

    if(extract_as != PyTango::ExtractAsNothing) {
        bool is_image = false;
        switch(data_format) {
        case Tango::SCALAR:
            TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(data_type,
                                                 scalar_value_from_cpp_into_python,
                                                 self,
                                                 py_value,
                                                 extract_as);
            break;
        case Tango::IMAGE:
            is_image = true;
            [[fallthrough]];
        case Tango::SPECTRUM:
            TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(data_type,
                                                 array_value_from_cpp_into_python,
                                                 self,
                                                 py_value,
                                                 is_image,
                                                 extract_as);
            break;
        case Tango::FMT_UNKNOWN:
        default:
            raise_(PyExc_ValueError, "Can't extract data because: self.get_data_format()=FMT_UNKNOWN");
            assert(false);
        }
    }
}

void set_cpp_values_from_python(Tango::DeviceAttribute &self,
                                int data_type,
                                Tango::AttrDataFormat data_format,
                                py::object py_value) {
    bool is_image = false;
    switch(data_format) {
    case Tango::SCALAR:
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(data_type, scalar_value_from_python_into_cpp, self, py_value);
        break;
    case Tango::IMAGE:
        is_image = true;
        [[fallthrough]];
    case Tango::SPECTRUM:
        TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(data_type, array_value_from_python_into_cpp, self, is_image, py_value);
        break;
    default:
        raise_(PyExc_TypeError, "unsupported data_format.");
    }
}

void reset(Tango::DeviceAttribute &self, const Tango::AttributeInfo &attr_info, py::object py_value) {
    self.set_name(attr_info.name.c_str());
    set_cpp_values_from_python(self, attr_info.data_type, attr_info.data_format, py_value);
}

void reset(Tango::DeviceAttribute &self,
           const std::string &attr_name,
           Tango::DeviceProxy &dev_proxy,
           py::object py_value) {
    self.set_name(attr_name.c_str());
    Tango::AttributeInfoEx attr_info;
    {
        py::gil_scoped_release no_gil;
        try {
            attr_info = dev_proxy.get_attribute_config(attr_name);
        } catch(...) {
        }
    }
    set_cpp_values_from_python(self, attr_info.data_type, attr_info.data_format, py_value);
}
} // namespace PyDeviceAttribute

void export_device_attribute(py::module &m) {
    py::class_<Tango::DeviceAttribute> DeviceAttribute(m,
                                                       "DeviceAttribute",
                                                       py::dynamic_attr(),
                                                       R"doc(
        This is the fundamental type for RECEIVING data from device attributes.

        It contains several fields. The most important ones depend on the
        ExtractAs method used to get the value. Normally they are:

            - value   : Normal scalar value or numpy array of values.
            - w_value : The write part of the attribute.

        See other ExtractAs for different possibilities. There are some more
        fields, these really fixed:

            - name        : (str)
            - data_format : (AttrDataFormat) Attribute format
            - quality     : (AttrQuality)
            - time        : (TimeVal)
            - dim_x       : (int) attribute dimension x
            - dim_y       : (int) attribute dimension y
            - w_dim_x     : (int) attribute written dimension x
            - w_dim_y     : (int) attribute written dimension y
            - r_dimension : (tuple<int,int>) Attribute read dimensions.
            - w_dimension : (tuple<int,int>) Attribute written dimensions.
            - nb_read     : (int) attribute read total length
            - nb_written  : (int) attribute written total length


        And two methods:
            - get_date
            - get_err_stack)doc");

    DeviceAttribute
        .def(py::init<>())
        .def(py::init<const Tango::DeviceAttribute &>())
        .def_readwrite("name", &Tango::DeviceAttribute::name)
        .def_readwrite("quality", &Tango::DeviceAttribute::quality)
        .def_readwrite("time", &Tango::DeviceAttribute::time)
        .def_property("dim_x", &Tango::DeviceAttribute::get_dim_x, nullptr)
        .def_property("dim_y", &Tango::DeviceAttribute::get_dim_y, nullptr)
        .def_property("w_dim_x", &Tango::DeviceAttribute::get_written_dim_x, nullptr)
        .def_property("w_dim_y", &Tango::DeviceAttribute::get_written_dim_y, nullptr)
        .def_property("r_dimension", &Tango::DeviceAttribute::get_r_dimension, nullptr)
        .def_property("w_dimension", &Tango::DeviceAttribute::get_w_dimension, nullptr)
        .def_property("nb_read", &Tango::DeviceAttribute::get_nb_read, nullptr)
        .def_property("nb_written", &Tango::DeviceAttribute::get_nb_written, nullptr)
        .def_property("data_format", &Tango::DeviceAttribute::get_data_format, nullptr)
        .def("get_date",
             &Tango::DeviceAttribute::get_date,
             py::return_value_policy::reference_internal,
             R"doc(
                get_date(self) -> TimeVal

                        Get the time at which the attribute was read by the server.

                        Note: It's the same as reading the "time" attribute.

                    Parameters : None
                    Return     : (TimeVal) The attribute read timestamp.)doc")
        .def("get_err_stack",
             &Tango::DeviceAttribute::get_err_stack,
             py::return_value_policy::copy,
             R"doc(
                get_err_stack(self) -> sequence<DevError>

                        Returns the error stack reported by the server when the
                        attribute was read.

                    Parameters : None
                    Return     : (sequence<DevError>))doc")
        .def("set_w_dim_x",
             &Tango::DeviceAttribute::set_w_dim_x,
             R"doc(
                set_w_dim_x(self, val) -> None

                        Sets the write value dim x.

                    Parameters :
                        - val : (int) new write dim x

                    Return     : None

                    New in PyTango 8.0.0)doc",
             py::arg("val"))
        .def("set_w_dim_y",
             &Tango::DeviceAttribute::set_w_dim_y,
             R"doc(
                set_w_dim_y(self, val) -> None

                        Sets the write value dim y.

                    Parameters :
                        - val : (int) new write dim y

                    Return     : None

                    New in PyTango 8.0.0)doc",
             py::arg("val"));

    py::native_enum<Tango::DeviceAttribute::except_flags>(DeviceAttribute, "except_flags", "enum.IntEnum")
        .value("isempty_flag", Tango::DeviceAttribute::isempty_flag)
        .value("wrongtype_flag", Tango::DeviceAttribute::wrongtype_flag)
        .value("failed_flag", Tango::DeviceAttribute::failed_flag)
        .value("numFlags", Tango::DeviceAttribute::numFlags)
        .finalize();
    py::object except_flags_class = DeviceAttribute.attr("except_flags");
    add_names_values_to_native_enum(except_flags_class);
}
