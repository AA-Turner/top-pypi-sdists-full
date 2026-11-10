/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

// Conversion of python sequences and numpy arrays into cpp buffers.

#pragma once

#include "types_structs_macros.h"
#include "convertors/generic_from_py.h"

// cppTango "feature": commands expect the buffer to come from "allocbuf", while
// attributes expect new[]. The strategy is a template parameter so that a buffer
// can only be handed to an API that frees it the matching way.
enum class MemoryAllocation { ALLOC, NEW };

template <int tangoArrayTypeConst, MemoryAllocation allocation>
class TangoBuffer {
  public:
    using TangoScalarType = typename TANGO_const2scalartype(tangoArrayTypeConst);
    using TangoArrayType = typename TANGO_const2type(tangoArrayTypeConst);

    explicit TangoBuffer(py::size_t length) :
        m_length(length) {
        if constexpr(allocation == MemoryAllocation::ALLOC) {
            m_data = TangoArrayType::allocbuf(static_cast<_CORBA_ULong>(length));
        } else {
            m_data = new TangoScalarType[length];
        }
    }

    TangoBuffer(TangoBuffer &&other) noexcept :
        m_data(other.m_data),
        m_length(other.m_length),
        m_filled(other.m_filled) {
        other.m_data = nullptr;
        other.m_length = 0;
        other.m_filled = 0;
    }

    TangoBuffer(const TangoBuffer &) = delete;
    TangoBuffer &operator=(const TangoBuffer &) = delete;

    ~TangoBuffer() {
        free();
    }

    // Borrowed view: the buffer stays the owner, so the callee must copy the data.
    TangoScalarType *data() const noexcept {
        return m_data;
    }

    // Appends one element and takes over ownership of it (DEV_STRING elements are
    // themselves new[] allocated), so that a converter throwing mid-sequence leaves
    // exactly the stored elements to free.
    void push_back(const TangoScalarType &element) {
        m_data[m_filled] = element;
        ++m_filled;
    }

    // For bulk copies written through data().
    void set_filled(py::size_t filled) noexcept {
        m_filled = filled;
    }

    // The caller (in practice cppTango, with release == true) frees the buffer
    // with delete[].
    [[nodiscard]] TangoScalarType *release() noexcept {
        static_assert(allocation == MemoryAllocation::NEW,
                      "a released buffer is freed with delete[], so it must come from new[]");
        TangoScalarType *data = m_data;
        m_data = nullptr;
        m_length = 0;
        m_filled = 0;
        return data;
    }

    // The returned sequence owns the buffer (release == true) and frees it with
    // freebuf(), so the buffer must come from allocbuf().
    [[nodiscard]] TangoArrayType *into_corba_sequence() {
        static_assert(allocation == MemoryAllocation::ALLOC, "a CORBA sequence frees its buffer with freebuf()");
        auto *sequence =
            new TangoArrayType(static_cast<_CORBA_ULong>(m_length), static_cast<_CORBA_ULong>(m_length), m_data, true);
        m_data = nullptr;
        m_length = 0;
        m_filled = 0;
        return sequence;
    }

  private:
    void free() noexcept {
        if(m_data == nullptr) {
            return;
        }
        if constexpr(allocation == MemoryAllocation::ALLOC) {
            TangoArrayType::freebuf(m_data);
        } else {
            if constexpr(tangoArrayTypeConst == Tango::DEVVAR_STRINGARRAY) {
                for(py::size_t i = 0; i < m_filled; ++i) {
                    delete[] m_data[i];
                }
            }
            delete[] m_data;
        }
        m_data = nullptr;
        m_length = 0;
        m_filled = 0;
    }

    TangoScalarType *m_data = nullptr;
    py::size_t m_length = 0;
    py::size_t m_filled = 0;
};

template <int tangoArrayTypeConst, MemoryAllocation allocation>
inline TangoBuffer<tangoArrayTypeConst, allocation> python_to_cpp_buffer_generic(py::object &py_val,
                                                                                 const std::string &fname,
                                                                                 bool isImage,
                                                                                 py::size_t &res_dim_x,
                                                                                 py::size_t &res_dim_y) {
    using TangoScalarType = typename TANGO_const2scalartype(tangoArrayTypeConst);

    std::string err_msg =
        isImage ? "Expecting a sequence of sequences (IMAGE attribute)." : "Expecting a sequence (SPECTRUM attribute).";

    if(py::isinstance<py::str>(py_val) || !py::isinstance<py::sequence>(py_val)) {
        Tango::Except::throw_exception("PyDs_WrongParameters", err_msg, fname + "()");
    }

    py::list py_list = py::cast<py::list>(py_val);
    py::size_t len = py::len(py_val);

    if(len > 0 && isImage) {
        py::object py_row0 = py_list[0];
        if(!py::isinstance<py::sequence>(py_row0)) {
            Tango::Except::throw_exception("PyDs_WrongParameters", err_msg, fname + "()");
        }

        res_dim_y = len;
        res_dim_x = py::len(py_row0);
        len = res_dim_x * res_dim_y;
    } else {
        res_dim_y = 0;
        res_dim_x = len;
    }

    TangoBuffer<tangoArrayTypeConst, allocation> buffer(len);

    TangoScalarType tg_scalar;
    if(isImage) {
        for(py::size_t y = 0; y < res_dim_y; y++) {
            py::list py_row = py_list[y];
            for(py::size_t x = 0; x < res_dim_x; x++) {
                array_element_from_py<tangoArrayTypeConst>::convert(py_row[x], tg_scalar);
                buffer.push_back(tg_scalar);
            }
        }
    } else {
        for(py::size_t x = 0; x < res_dim_x; x++) {
            array_element_from_py<tangoArrayTypeConst>::convert(py_list[x], tg_scalar);
            buffer.push_back(tg_scalar);
        }
    }
    return buffer;
}

template <int tangoArrayTypeConst, MemoryAllocation allocation>
inline TangoBuffer<tangoArrayTypeConst, allocation> python_to_cpp_buffer(py::object &py_val,
                                                                         const std::string &fname,
                                                                         bool isImage,
                                                                         py::size_t &res_dim_x,
                                                                         py::size_t &res_dim_y) {
    if constexpr(tangoArrayTypeConst == Tango::DEVVAR_STRINGARRAY) {
        // numpy has no dtype for Tango::DevString
        return python_to_cpp_buffer_generic<tangoArrayTypeConst, allocation>(
            py_val, fname, isImage, res_dim_x, res_dim_y);
    } else {
        using TangoScalarType = typename TANGO_const2scalartype(tangoArrayTypeConst);

        if(!py::isinstance<py::array>(py_val)) {
            return python_to_cpp_buffer_generic<tangoArrayTypeConst, allocation>(
                py_val, fname, isImage, res_dim_x, res_dim_y);
        }

        py::array arr = py_val.cast<py::array>();
        long nd = arr.ndim();
        const py::ssize_t *signed_dims = arr.shape();
        std::vector<py::size_t> dims;
        for(long i = 0; i < nd; ++i) {
            dims.push_back(static_cast<py::size_t>(signed_dims[i]));
        }
        py::size_t len = 0;

        // Retrieve the NumPy array flags
        int flags = arr.flags();

        // Check if the array is exactly what we need: contiguous, aligned, and correct data type
        const bool exact_array = ((flags & NPY_ARRAY_C_CONTIGUOUS) != 0) && ((flags & NPY_ARRAY_ALIGNED) != 0) &&
                                 arr.dtype().is(pybind11::dtype::of<TangoScalarType>());

        // Handle empty arrays first - set dimensions to 0 regardless of actual dimensions
        bool is_empty = false;
        if(isImage) {
            if(nd == 2 && dims[0] == 0) {
                // Empty 2D array
                is_empty = true;
            } else if(nd == 1 && dims[0] == 0) {
                // Empty 1D array passed as image - treat as empty 2D
                is_empty = true;
            } else if(nd != 2) {
                Tango::Except::throw_exception("PyDs_WrongNumpyArrayDimensions",
                                               "Expecting a sequence of sequences (IMAGE attribute).",
                                               fname + "()");
            }
        } else {
            if(nd == 1 && dims[0] == 0) {
                // Empty 1D array
                is_empty = true;
            } else if(nd != 1) {
                Tango::Except::throw_exception(
                    "PyDs_WrongNumpyArrayDimensions", "Expecting a sequence (SPECTRUM attribute).", fname + "()");
            }
        }

        if(is_empty) {
            len = 0;
            res_dim_x = 0;
            res_dim_y = 0;
        } else if(isImage) {
            len = dims[0] * dims[1];
            res_dim_x = dims[1];
            res_dim_y = dims[0];
        } else {
            len = dims[0];
            res_dim_x = dims[0];
        }

        TangoBuffer<tangoArrayTypeConst, allocation> buffer(len);

        if(exact_array) {
            memcpy(buffer.data(), arr.data(), len * sizeof(TangoScalarType));
        } else {
            py::array_t<TangoScalarType, py::array::c_style | py::array::forcecast> arr_casted(arr);

            py::size_t processed_elements = static_cast<py::size_t>(arr_casted.size());
            if(processed_elements < len) {
                throw py::value_error("Array size is smaller than expected.");
            }

            memcpy(buffer.data(), arr_casted.data(), len * sizeof(TangoScalarType));
        }
        buffer.set_filled(len);

        return buffer;
    }
}

// clang-format off
template <int tangoArrayTypeConst>
    inline typename TANGO_const2type(tangoArrayTypeConst) * fast_convert2array(py::object py_value) {
    // clang-format on
    py::size_t res_dim_x, res_dim_y;

    auto buffer = python_to_cpp_buffer<tangoArrayTypeConst, MemoryAllocation::ALLOC>(
        py_value, "array_python_data_to_cpp", false, res_dim_x, res_dim_y);

    // not a bug: res_dim_y means nothing to us, we are unidimensional
    return buffer.into_corba_sequence();
}

// clang-format off
template <int tangoArrayTypeConst>
    inline typename TANGO_const2type(tangoArrayTypeConst) * numeric_string_array_from_python(py::object py_value) {
    // clang-format on
    using TangoArrayType = typename TANGO_const2type(tangoArrayTypeConst);
    using traits = numeric_string_array_traits<TangoArrayType>;

    py::object py_numeric, py_string;
    split_numeric_string_sequence<TangoArrayType>(py_value, "fast_convert2array()", py_numeric, py_string);

    std::unique_ptr<typename traits::NumericArrayType> numeric(
        fast_convert2array<traits::numeric_array_const>(py_numeric));
    std::unique_ptr<Tango::DevVarStringArray> strings(fast_convert2array<Tango::DEVVAR_STRINGARRAY>(py_string));
    auto result = std::make_unique<TangoArrayType>();

    (*result).*traits::numeric_member = *numeric;
    (*result).*traits::string_member = *strings;

    return result.release();
}

// clang-format off
template <>
    inline TANGO_const2type(Tango::DEVVAR_LONGSTRINGARRAY) * fast_convert2array<Tango::DEVVAR_LONGSTRINGARRAY>(py::object py_value) {
    // clang-format on
    return numeric_string_array_from_python<Tango::DEVVAR_LONGSTRINGARRAY>(py_value);
}

// clang-format off
template <>
    inline TANGO_const2type(Tango::DEVVAR_DOUBLESTRINGARRAY) * fast_convert2array<Tango::DEVVAR_DOUBLESTRINGARRAY>(py::object py_value) {
    // clang-format on
    return numeric_string_array_from_python<Tango::DEVVAR_DOUBLESTRINGARRAY>(py_value);
}
