# Copyright 2026 zovdev
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# distutils: language = c++
# cython: language_level = 3

from libc.stdint cimport uint32_t, uint64_t, int32_t, int64_t
from libc.string cimport memcpy, memset
from libcpp.unordered_map cimport unordered_map
from libcpp.string cimport string
from cpython.ref cimport PyObject
from cpython.list cimport PyList_New, PyList_SET_ITEM
from cpython.bytes cimport PyBytes_FromStringAndSize

cdef extern from "string.h":
    char* strdup(const char* s)
    int strcmp(const char* s1, const char* s2)

cdef extern from "tl.h":
    ctypedef enum TLType:
        TL_TYPE_INT
        TL_TYPE_LONG
        TL_TYPE_DOUBLE
        TL_TYPE_STRING
        TL_TYPE_BYTES
        TL_TYPE_BOOL
        TL_TYPE_VECTOR
        TL_TYPE_OBJECT
    
    ctypedef struct TLOptionalFlag:
        int bit_position
        int flags_index
        char* name
    
    ctypedef struct TLField:
        char* name
        PyObject* py_name
        TLType type
        char* type_name
        int is_optional
        TLOptionalFlag flag_info
        int is_generic
    
    ctypedef struct TLConstructor:
        uint32_t id
        char* name
        char* type
        TLField* fields
        int field_count
        int has_flags
        int has_flags2
    
    ctypedef struct TLSchema:
        TLConstructor* constructors
        int constructor_count

cdef class TLSchemaCompiler:
    cdef TLSchema* _schema
    cdef unordered_map[uint32_t, TLConstructor*] _id_map
    cdef unordered_map[string, TLConstructor*] _name_map
    
    cdef void _parse_json_schema(self, object json_data)
    cdef TLConstructor* _create_constructor(self, dict constr_data, int index)
    cdef TLType _parse_type(self, str type_str)
    cdef void _free_schema(self)
    cdef TLSchema* get_schema(self)

cdef class TLParser:
    cdef TLSchema* _schema
    cdef TLSchemaCompiler _compiler
    cdef unsigned char* _buffer
    cdef size_t _buffer_alloc_size
    cdef size_t _buffer_size
    cdef size_t _position
    cdef int _error

    cdef object _read_value(self, TLType field_type, object type_name=*)
    cdef void _write_value(self, object value, TLType field_type, object type_name=*)
    cdef uint32_t _read_int32(self)
    cdef uint64_t _read_int64(self)
    cdef double _read_double(self)
    cdef bytes _read_bytes(self)
    cdef object _read_string(self)
    cdef object _read_vector(self, object type_name)
    cdef object _read_object(self)

    cdef void _write_int32(self, int32_t value)
    cdef void _write_int64(self, uint64_t value)
    cdef void _write_double(self, double value)
    cdef void _write_bytes(self, bytes data)
    cdef void _write_string(self, str data)
    cdef void _write_vector(self, object value, object type_name)
    cdef void _write_object(self, object value)
    cdef void _ensure_buffer(self, size_t needed)
