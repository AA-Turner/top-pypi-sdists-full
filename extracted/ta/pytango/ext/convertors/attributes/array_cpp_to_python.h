/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"
#include "types_structs_macros.h"
#include "convertors/attributes/extract_value.h"
#include "convertors/type_casters.h"

namespace PyDeviceAttribute {

template <int tangoTypeConst>
static inline void array_value_from_cpp_into_python_as_bin_or_str(Tango::DeviceAttribute &self,
                                                                  PyTango::ExtractAs extract_as,
                                                                  py::object &read_value,
                                                                  py::object &written_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    using TangoArrayType = typename TANGO_const2arraytype(tangoTypeConst);

    Py_ssize_t nb_bytes_read = static_cast<Py_ssize_t>(self.get_nb_read()) *
                               static_cast<Py_ssize_t>(sizeof(TangoScalarType));
    Py_ssize_t nb_bytes_written = static_cast<Py_ssize_t>(self.get_nb_written()) *
                                  static_cast<Py_ssize_t>(sizeof(TangoScalarType));

    // Extract the actual data from Tango::DeviceAttribute (self)
    TangoArrayType *value_ptr = nullptr;
    EXTRACT_VALUE(self, value_ptr)
    std::unique_ptr<TangoArrayType> guard_value_ptr(value_ptr);

    if(value_ptr == nullptr) {
        // Empty device attribute
        value_ptr = new TangoArrayType;
    }

    TangoScalarType *buffer = value_ptr->get_buffer();
    const char *ch_ptr = reinterpret_cast<const char *>(buffer);

    switch(extract_as) {
    case PyTango::ExtractAsBytes: {
        read_value = py::bytes(ch_ptr, nb_bytes_read);
        written_value = py::bytes(ch_ptr + nb_bytes_read, nb_bytes_written);
        break;
    }
    case PyTango::ExtractAsByteArray: {
        read_value = py::bytearray(ch_ptr, nb_bytes_read);
        written_value = py::bytearray(ch_ptr + nb_bytes_read, nb_bytes_written);
        break;
    }
    case PyTango::ExtractAsString: {
        read_value = py::str(ch_ptr, nb_bytes_read);
        written_value = py::str(ch_ptr + nb_bytes_read, nb_bytes_written);
        break;
    }
    default:
        throw std::invalid_argument("Unsupported extract_as");
    }
}

template <>
inline void array_value_from_cpp_into_python_as_bin_or_str<Tango::DEV_STRING>([[maybe_unused]] Tango::DeviceAttribute &self,
                                                                              [[maybe_unused]] PyTango::ExtractAs extract_as,
                                                                              [[maybe_unused]] py::object &read_value,
                                                                              [[maybe_unused]] py::object &written_value) {
    assert(false);
}

template <int tangoTypeConst>
static void array_value_from_cpp_into_python_as_tuple_or_list(Tango::DeviceAttribute &self,
                                                              bool is_image,
                                                              PyTango::ExtractAs extract_as,
                                                              py::object &read_value,
                                                              py::object &written_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    using TangoArrayType = typename TANGO_const2arraytype(tangoTypeConst);

    // Extract the actual data from Tango::DeviceAttribute (self)
    TangoArrayType *value_ptr = nullptr;
    EXTRACT_VALUE(self, value_ptr)
    std::unique_ptr<TangoArrayType> guard_value_ptr(value_ptr);

    if(value_ptr == nullptr) {
        // Empty device attribute
        switch(extract_as) {
        case PyTango::ExtractAsTuple: {
            read_value = py::tuple();
            written_value = py::tuple();
            break;
        }
        case PyTango::ExtractAsList: {
            read_value = py::list();
            written_value = py::list();
            break;
        }
        default:
            throw std::invalid_argument("Unsupported extract_as");
        }
        return;
    }

    TangoScalarType *buffer = value_ptr->get_buffer();
    int total_length = static_cast<int>(value_ptr->length());

    // Determine if the attribute is AttrWriteType.WRITE
    int read_size = 0, write_size = 0;
    if(is_image) {
        read_size = self.get_dim_x() * self.get_dim_y();
        write_size = self.get_written_dim_x() * self.get_written_dim_y();
    } else {
        read_size = self.get_dim_x();
        write_size = self.get_written_dim_x();
    }
    bool is_write_type = (read_size + write_size) > total_length;

    // Convert to a tuple of tuples
    unsigned int offset = 0;
    for(int it = 1; it >= 0; --it) { // 2 iterations: read part/write part
        if((!it) && is_write_type) {
            written_value = read_value;
            continue;
        }

        unsigned int dim_x = static_cast<unsigned int>(it ? self.get_dim_x() : self.get_written_dim_x());
        unsigned int dim_y = static_cast<unsigned int>(it ? self.get_dim_y() : self.get_written_dim_y());

        py::tuple array(is_image ? dim_y : dim_x);

        if(is_image) {
            for(unsigned int y = 0; y < dim_y; ++y) {
                py::tuple row_vec(dim_x);
                for(unsigned int x = 0; x < dim_x; ++x) {
                    row_vec[x] = cpp_to_python_scalar<tangoTypeConst>::convert(buffer[offset + x + (y * dim_x)]);
                }
                switch(extract_as) {
                case PyTango::ExtractAsTuple:
                    array[y] = row_vec;
                    break;
                case PyTango::ExtractAsList:
                    array[y] = py::list(row_vec);
                    break;
                default:
                    throw std::invalid_argument("Unsupported extract_as");
                }
            }
            offset += dim_x * dim_y;
        } else {
            for(unsigned int x = 0; x < dim_x; ++x) {
                array[x] = cpp_to_python_scalar<tangoTypeConst>::convert(buffer[offset + x]);
            }
            offset += dim_x;
        }
        py::object result;
        switch(extract_as) {
        case PyTango::ExtractAsTuple:
            result = array;
            break;
        case PyTango::ExtractAsList:
            result = py::list(array);
            break;
        default:
            throw std::invalid_argument("Unsupported extract_as");
        }

        if(it) {
            read_value = result;
        } else {
            written_value = result;
        }
    }
}

template <int tangoTypeConst>
static void array_value_from_cpp_into_python_as_numpy(Tango::DeviceAttribute &self,
                                                      bool is_image,
                                                      py::object &read_value,
                                                      py::object &written_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);
    using TangoArrayType = typename TANGO_const2arraytype(tangoTypeConst);

    // Extract the actual data from Tango::DeviceAttribute (self)
    TangoArrayType *value_ptr = nullptr;
    EXTRACT_VALUE(self, value_ptr)

    if(value_ptr == nullptr) {
        // Empty device attribute
        value_ptr = new TangoArrayType();
    }

    TangoScalarType *buffer = value_ptr->get_buffer();
    std::size_t itemsize = static_cast<std::size_t>(sizeof(TangoScalarType));

    std::vector<std::size_t> dims;
    std::vector<std::size_t> strides;
    size_t write_part_offset = 0;

    if(is_image) {
        std::size_t dim_x = static_cast<std::size_t>(self.get_dim_x());
        std::size_t dim_y = static_cast<std::size_t>(self.get_dim_y());
        dims = {dim_y, dim_x};
        strides = {dim_x * itemsize, itemsize}; // For C-style (row-major) layout
        write_part_offset = dim_y * dim_x;
    } else {
        std::size_t dim_x = static_cast<std::size_t>(self.get_dim_x());
        dims = {dim_x};
        strides = {itemsize};
        write_part_offset = dim_x;
    }

    // Create a capsule to manage the lifetime of value_ptr
    py::capsule base(value_ptr, dev_var_attribute_array_deleter<tangoTypeConst>);

    // Create the numpy array without copying the data, and associate the base object
    read_value = py::array(py::dtype::of<TangoScalarType>(),
                           dims,
                           strides,
                           buffer,
                           base // Associate the capsule as the base object
    );

    // Handle the write part if present
    TangoScalarType *w_buffer = nullptr;
    std::vector<std::size_t> w_dims;
    std::vector<std::size_t> w_strides;
    w_buffer = buffer + write_part_offset;

    if(is_image) {
        std::size_t w_dim_x = static_cast<std::size_t>(self.get_written_dim_x());
        std::size_t w_dim_y = static_cast<std::size_t>(self.get_written_dim_y());
        w_dims = {w_dim_y, w_dim_x};
        w_strides = {w_dim_x * itemsize, itemsize};
    } else {
        std::size_t w_dim_x = static_cast<std::size_t>(self.get_written_dim_x());
        w_dims = {w_dim_x};
        w_strides = {itemsize};
    }

    written_value = py::array(py::dtype::of<TangoScalarType>(),
                              w_dims,
                              w_strides,
                              w_buffer,
                              base // Associate the same capsule as the base object
    );
}

template <>
inline void array_value_from_cpp_into_python_as_numpy<Tango::DEV_STRING>(Tango::DeviceAttribute &self,
                                                                         bool is_image,
                                                                         py::object &read_value,
                                                                         py::object &written_value) {
    array_value_from_cpp_into_python_as_tuple_or_list<Tango::DEV_STRING>(self,
                                                                         is_image,
                                                                         PyTango::ExtractAsTuple,
                                                                         read_value,
                                                                         written_value);
}

template <int tangoTypeConst>
static inline void array_value_from_cpp_into_python(Tango::DeviceAttribute &self,
                                                    py::object &py_value,
                                                    bool is_image,
                                                    PyTango::ExtractAs extract_as) {
    py::object read_value;
    py::object written_value;

    switch(extract_as) {
    default:
    case PyTango::ExtractAsNumpy:
        array_value_from_cpp_into_python_as_numpy<tangoTypeConst>(self,
                                                                  is_image,
                                                                  read_value,
                                                                  written_value);
        break;
    case PyTango::ExtractAsTuple:
    case PyTango::ExtractAsList:
        array_value_from_cpp_into_python_as_tuple_or_list<tangoTypeConst>(self,
                                                                          is_image,
                                                                          extract_as,
                                                                          read_value,
                                                                          written_value);
        break;
    case PyTango::ExtractAsBytes:
    case PyTango::ExtractAsByteArray:
    case PyTango::ExtractAsString:
        array_value_from_cpp_into_python_as_bin_or_str<tangoTypeConst>(self,
                                                                       extract_as,
                                                                       read_value,
                                                                       written_value);
        break;
    }

    py_value.attr(value_attr_name) = read_value;
    py_value.attr(w_value_attr_name) = written_value;
}

template <>
inline void array_value_from_cpp_into_python<Tango::DEV_ENCODED>([[maybe_unused]] Tango::DeviceAttribute &self,
                                                                 [[maybe_unused]] py::object &py_value,
                                                                 [[maybe_unused]] bool is_image,
                                                                 [[maybe_unused]] PyTango::ExtractAs extract_as) {
    /// @todo Sure, it is not necessary?
    assert(false);
}
} // namespace PyDeviceAttribute

namespace PyWAttribute {
// General helper template
template <int tangoTypeConst>
struct tango_const2type {
    using Type = typename TANGO_const2type(tangoTypeConst);
};

// Specialization for Tango::DEV_STRING
template <>
struct tango_const2type<Tango::DEV_STRING> {
    using Type = Tango::ConstDevString;
};

template <int tangoTypeConst>
inline void array_value_from_cpp_into_python_as_list(Tango::WAttribute &att,
                                                     py::object &py_value) {
    using TangoScalarType = typename tango_const2type<tangoTypeConst>::Type;

    const TangoScalarType *buffer = nullptr;
    att.get_write_value(buffer);

    if(buffer == nullptr) {
        py_value = py::list();
        return;
    }

    std::size_t dim_x = static_cast<std::size_t>(att.get_w_dim_x());
    std::size_t dim_y = static_cast<std::size_t>(att.get_w_dim_y());

    py::list result;

    if(att.get_data_format() == Tango::SPECTRUM) {
        for(size_t x = 0; x < dim_x; ++x) {
            result.append(cpp_to_python_scalar<tangoTypeConst>::convert(buffer[x]));
        }
    } else {
        for(size_t y = 0; y < dim_y; ++y) {
            py::list row;
            for(size_t x = 0; x < dim_x; ++x) {
                row.append(cpp_to_python_scalar<tangoTypeConst>::convert(buffer[x + (y * dim_x)]));
            }
            result.append(row);
        }
    }
    py_value = result;
}

template <int tangoTypeConst>
inline void array_value_from_cpp_into_python_as_numpy(Tango::WAttribute &att,
                                                      py::object &py_value) {
    using TangoScalarType = typename TANGO_const2type(tangoTypeConst);

    const TangoScalarType *buffer = nullptr;
    att.get_write_value(buffer);

    std::size_t itemsize = static_cast<std::size_t>(sizeof(TangoScalarType));

    std::vector<std::size_t> dims;
    std::vector<std::size_t> strides;

    std::size_t dim_x = static_cast<std::size_t>(att.get_w_dim_x());
    std::size_t dim_y = static_cast<std::size_t>(att.get_w_dim_y());

    if(att.get_data_format() == Tango::SPECTRUM) {
        dims = {dim_x};
        strides = {itemsize};
    } else {
        dims = {dim_y, dim_x};
        strides = {dim_x * itemsize, itemsize}; // For C-style (row-major) layout
    }

    // Create the numpy array. Note, that pybind11 copy the data automatically,
    // if there is no capsule object
    // https://github.com/pybind/pybind11/issues/1042#issuecomment-325938098
    py_value = py::array(py::dtype::of<TangoScalarType>(),
                         dims,
                         strides,
                         buffer);
}

template <>
inline void array_value_from_cpp_into_python_as_numpy<Tango::DEV_STRING>(Tango::WAttribute &att,
                                                                         py::object &py_value) {
    array_value_from_cpp_into_python_as_list<Tango::DEV_STRING>(att, py_value);
}

template <int tangoTypeConst>
static inline void array_value_from_cpp_into_python(Tango::WAttribute &att,
                                                    py::object &py_value,
                                                    PyTango::ExtractAs extract_as) {
    switch(extract_as) {
    case PyTango::ExtractAsPyTango3:
    case PyTango::ExtractAsList: {
        array_value_from_cpp_into_python_as_list<tangoTypeConst>(att, py_value);
        break;
    }
    case PyTango::ExtractAsNumpy: {
        array_value_from_cpp_into_python_as_numpy<tangoTypeConst>(att, py_value);
        break;
    }
    default:
        Tango::Except::throw_exception("PyDs_WrongParameterValue",
                                       "This extract method is not supported by the function.",
                                       "PyWAttribute::get_write_value()");
    }
}

template <>
inline void array_value_from_cpp_into_python<Tango::DEV_ENCODED>([[maybe_unused]] Tango::WAttribute &att,
                                                                 [[maybe_unused]] py::object &py_value,
                                                                 [[maybe_unused]] PyTango::ExtractAs extract_as) {
    assert(false);
}
} // namespace PyWAttribute
