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
# cython: boundscheck = False
# cython: wraparound = False
# cython: nonecheck = False
# cython: cdivision = True

import json
from cpython.ref cimport Py_INCREF, Py_DECREF, PyObject
from cpython.list cimport PyList_New, PyList_SET_ITEM
from cpython.dict cimport PyDict_Contains

cdef extern from "Python.h":
    object PyBytes_FromString(const char* s)

cdef extern from "stdlib.h":
    void* malloc(size_t size)
    void free(void* ptr)
    void* realloc(void* ptr, size_t size)

cdef class TLSchemaCompiler:
    def __cinit__(self):
        self._schema = NULL

    def __dealloc__(self):
        self._free_schema()

    cdef void _free_schema(self):
        cdef int i, j
        cdef TLConstructor* constr
        cdef TLField* field
        if self._schema != NULL:
            if self._schema.constructors != NULL:
                for i in range(self._schema.constructor_count):
                    constr = &self._schema.constructors[i]
                    if constr.fields != NULL:
                        for j in range(constr.field_count):
                            field = &constr.fields[j]
                            if field.name != NULL:
                                free(field.name)
                            if field.type_name != NULL:
                                free(field.type_name)
                            if field.py_name != NULL:
                                Py_DECREF(<object>field.py_name)
                                field.py_name = NULL
                        free(constr.fields)
                    if constr.name != NULL:
                        free(constr.name)
                    if constr.type != NULL:
                        free(constr.type)
                free(self._schema.constructors)
            free(self._schema)
            self._schema = NULL
        self._id_map.clear()
        self._name_map.clear()

    def compile(self, object json_data):
        self._parse_json_schema(json_data)

    cdef void _parse_json_schema(self, object json_data):
        cdef dict schema_dict
        cdef list constructors_list
        cdef dict constr_data
        cdef int i
        cdef TLConstructor* constr_ptr
        
        if isinstance(json_data, str):
            schema_dict = json.loads(json_data)
        else:
            schema_dict = json_data
        
        constructors_list = schema_dict.get('constructors', [])
        constructors_list.extend(schema_dict.get('methods', []))
        
        self._schema = <TLSchema*>malloc(sizeof(TLSchema))
        if self._schema == NULL:
            raise MemoryError("Cannot allocate memory for schema")
        memset(self._schema, 0, sizeof(TLSchema))
        
        self._schema.constructor_count = <int>len(constructors_list)
        self._schema.constructors = <TLConstructor*>malloc(
            self._schema.constructor_count * sizeof(TLConstructor))
            
        if self._schema.constructors == NULL:
            free(self._schema)
            raise MemoryError("Cannot allocate memory for constructors")
        memset(self._schema.constructors, 0, 
               self._schema.constructor_count * sizeof(TLConstructor))
        
        for i, constr_data in enumerate(constructors_list):
            constr_ptr = self._create_constructor(constr_data, i)
            if constr_ptr != NULL:
                self._id_map[constr_ptr.id] = constr_ptr
                self._name_map[string(constr_ptr.name)] = constr_ptr

    cdef TLConstructor* _create_constructor(self, dict constr_data, int index):
        cdef TLConstructor* constr = &self._schema.constructors[index]
        cdef str name = constr_data.get('predicate', constr_data.get('method', constr_data.get('type', '')))
        cdef str type_name = constr_data.get('type', '')
        cdef list params = constr_data.get('params', [])
        cdef dict param
        cdef str param_name, param_type, flag_spec, flags_name, bit_str
        cdef int i, bit_pos
        cdef bytes field_name_bytes, type_name_bytes, name_bytes, type_bytes
        cdef object id_obj
        
        name_bytes = name.encode('utf-8')
        constr.name = strdup(name_bytes)
        
        if type_name:
            type_bytes = type_name.encode('utf-8')
        else:
            type_bytes = name_bytes
        constr.type = strdup(type_bytes)
        
        id_obj = int(constr_data.get('id', 0))
        if id_obj < 0:
            constr.id = <uint32_t>(id_obj & 0xFFFFFFFF)
        else:
            constr.id = <uint32_t>id_obj
            
        constr.field_count = <int>len(params)
        if constr.field_count > 0:
            constr.fields = <TLField*>malloc(constr.field_count * sizeof(TLField))
            memset(constr.fields, 0, constr.field_count * sizeof(TLField))
            
            for i, param in enumerate(params):
                param_name = param['name']
                param_type = param['type']
                
                field_name_bytes = param_name.encode('utf-8')
                constr.fields[i].name = strdup(field_name_bytes)

                Py_INCREF(param_name) 
                constr.fields[i].py_name = <PyObject*>param_name
                
                constr.fields[i].type = self._parse_type(param_type)
                type_name_bytes = param_type.encode('utf-8')
                constr.fields[i].type_name = strdup(type_name_bytes)
                
                if '?' in param_type:
                    constr.fields[i].is_optional = 1
                    flag_spec = param_type.split('?')[0]
                    if '.' in flag_spec:
                        flags_name, bit_str = flag_spec.split('.')
                        bit_pos = int(bit_str)
                        constr.fields[i].flag_info.bit_position = bit_pos
                        if flags_name == "flags2":
                            constr.has_flags2 = 1
                            constr.fields[i].flag_info.flags_index = 1
                        else:
                            constr.has_flags = 1
                            constr.fields[i].flag_info.flags_index = 0
        return constr

    cdef TLType _parse_type(self, str type_str):
        cdef str clean_type = type_str.split('?')[1] if '?' in type_str else type_str
        if clean_type in ('int', '#'): return TL_TYPE_INT
        elif clean_type == 'long': return TL_TYPE_LONG
        elif clean_type == 'double': return TL_TYPE_DOUBLE
        elif clean_type == 'string': return TL_TYPE_STRING
        elif clean_type in ('bytes', 'byte'): return TL_TYPE_BYTES
        elif clean_type in ('Bool', 'true'): return TL_TYPE_BOOL
        elif clean_type.startswith('Vector'): return TL_TYPE_VECTOR
        else: return TL_TYPE_OBJECT

    cdef TLSchema* get_schema(self):
        return self._schema

cdef class TLParser:
    def __cinit__(self, object schema_json):
        self._compiler = TLSchemaCompiler()
        self._compiler.compile(schema_json)
        self._schema = self._compiler.get_schema()
        self._buffer = NULL
        self._buffer_alloc_size = 0
        self._buffer_size = 0
        self._position = 0
        self._error = 0

    def __dealloc__(self):
        if self._buffer != NULL:
            free(self._buffer)

    def unpack(self, bytes data):
        cdef object parsed
        cdef size_t data_len = len(data)
        
        if data_len > self._buffer_alloc_size:
            self._buffer_alloc_size = data_len
            self._buffer = <unsigned char*>realloc(self._buffer, self._buffer_alloc_size)
            if self._buffer == NULL:
                raise MemoryError("Cannot allocate buffer")
                
        memcpy(self._buffer, <unsigned char*>data, data_len)
        self._buffer_size = data_len
        self._position = 0
        self._error = 0
        
        parsed = self._read_object()
        if self._error:
            raise RuntimeError(f"Parse error at position {self._position}")
        return parsed

    cdef object _read_object(self):
        cdef uint32_t constructor_id, flag_mask
        cdef TLConstructor* constructor
        cdef dict result = {}
        cdef int32_t flags = 0, flags2 = 0
        cdef int i
        cdef TLField* field
        cdef object value
        cdef bytes type_name_bytes
        cdef bint field_present

        if self._position + 4 > self._buffer_size:
            self._error = 1
            return None

        constructor_id = self._read_int32()

        if self._compiler._id_map.count(constructor_id) == 0:
            raise ValueError(f"Unknown constructor ID: 0x{constructor_id:08x}")
        constructor = self._compiler._id_map[constructor_id]

        result['_'] = constructor.name.decode('utf-8')
        
        for i in range(constructor.field_count):
            field = &constructor.fields[i]
            
            if field.name[0] == 'f' and field.name[1] == 'l' and field.name[2] == 'a' and field.name[3] == 'g' and field.name[4] == 's':
                if field.name[5] == '\0':
                    flags = <int32_t>self._read_int32()
                    continue
                elif field.name[5] == '2' and field.name[6] == '\0':
                    flags2 = <int32_t>self._read_int32()
                    continue
            
            if field.is_optional:
                flag_mask = 1 << field.flag_info.bit_position
                if field.flag_info.flags_index == 0:
                    field_present = flags & flag_mask
                else:
                    field_present = flags2 & flag_mask
                
                if field.type == TL_TYPE_BOOL:
                    result[<object>field.py_name] = field_present
                    continue
                
                if not field_present:
                    result[<object>field.py_name] = None
                    continue
            
            if field.type_name != NULL:
                type_name_bytes = PyBytes_FromString(field.type_name)
            else:
                type_name_bytes = None
                
            value = self._read_value(field.type, type_name_bytes)
            if self._error: break
            
            result[<object>field.py_name] = value
            
        return result

    cdef object _read_value(self, TLType field_type, object type_name=None):
        if field_type == TL_TYPE_INT: return self._read_int32()
        elif field_type == TL_TYPE_STRING: return self._read_string()
        elif field_type == TL_TYPE_LONG: return self._read_int64()
        elif field_type == TL_TYPE_VECTOR: return self._read_vector(type_name)
        elif field_type == TL_TYPE_OBJECT: return self._read_object()
        elif field_type == TL_TYPE_DOUBLE: return self._read_double()
        elif field_type == TL_TYPE_BYTES: return self._read_bytes()
        elif field_type == TL_TYPE_BOOL: return self._read_int32() != 0
        else:
            self._error = 1
            raise ValueError(f"Unknown type: {field_type}")

    cdef object _read_vector(self, object type_name):
        cdef uint32_t vector_id = self._read_int32()
        if vector_id != 0x1cb5c415:
            self._error = 1
            raise ValueError(f"Invalid vector ID: 0x{vector_id:08x}")
            
        cdef int32_t count = <int32_t>self._read_int32()
        cdef list result = PyList_New(count)
        cdef int i
        cdef str elem_type_str
        cdef TLType elem_type = TL_TYPE_INT
        cdef bytes elem_type_bytes = None
        cdef object val

        if type_name is not None:
            elem_type_str = type_name.decode('utf-8').replace('Vector<', '').replace('>', '')
            elem_type = self._compiler._parse_type(elem_type_str)
            elem_type_bytes = elem_type_str.encode('utf-8')

        for i in range(count):
            val = self._read_value(elem_type, elem_type_bytes)
            Py_INCREF(val) 
            PyList_SET_ITEM(result, i, val) 
            
        return result

    cdef uint32_t _read_int32(self):
        if self._position + 4 > self._buffer_size:
            self._error = 1
            return 0
        cdef uint32_t value
        memcpy(&value, self._buffer + self._position, 4)
        self._position += 4
        return value

    cdef uint64_t _read_int64(self):
        if self._position + 8 > self._buffer_size:
            self._error = 1
            return 0
        cdef uint64_t value
        memcpy(&value, self._buffer + self._position, 8)
        self._position += 8
        return value

    cdef double _read_double(self):
        if self._position + 8 > self._buffer_size:
            self._error = 1
            return 0.0
        cdef double value
        memcpy(&value, self._buffer + self._position, 8)
        self._position += 8
        return value

    cdef bytes _read_bytes(self):
        cdef uint32_t length
        if self._position >= self._buffer_size:
            self._error = 1
            return b''
        length = self._buffer[self._position]
        self._position += 1
        if length == 254:
            if self._position + 3 > self._buffer_size:
                self._error = 1
                return b''
            length = (self._buffer[self._position] |
                      (self._buffer[self._position + 1] << 8) |
                      (self._buffer[self._position + 2] << 16))
            self._position += 3
        if self._position + length > self._buffer_size:
            self._error = 1
            return b''
        cdef bytes result = PyBytes_FromStringAndSize(<char*>self._buffer + self._position, length)
        self._position += length
        cdef int padding = (4 - (self._position % 4)) % 4
        self._position += padding
        return result

    cdef object _read_string(self):
        cdef bytes data = self._read_bytes()
        return data.decode('utf-8')

    def pack(self, object value):
        cdef bytes result
        self._buffer_size = 1024
        if self._buffer_alloc_size < self._buffer_size:
            self._buffer_alloc_size = self._buffer_size
            self._buffer = <unsigned char*>realloc(self._buffer, self._buffer_alloc_size)
            if self._buffer == NULL: raise MemoryError()
             
        self._position = 0
        self._error = 0
        self._write_object(value)
        return PyBytes_FromStringAndSize(<char*>self._buffer, self._position)

    cdef void _write_object(self, object value):
        cdef str constr_name = value.get('_')
        if not constr_name:
             raise ValueError("Object must have '_' field")
             
        cdef bytes constr_name_bytes_py = constr_name.encode('utf-8')
        cdef string constr_name_str = string(constr_name_bytes_py)
        
        if self._compiler._name_map.count(constr_name_str) == 0:
            raise ValueError(f"Unknown constructor: {constr_name}")
            
        cdef TLConstructor* constructor = self._compiler._name_map[constr_name_str]
        cdef uint32_t flags = 0, flags2 = 0
        cdef int i
        cdef TLField* field
        cdef object field_value
        cdef bytes type_name_bytes
        cdef bint should_set_flag
        
        for i in range(constructor.field_count):
            field = &constructor.fields[i]
            if (field.name[0]=='f' and field.name[1]=='l' and field.name[2]=='a' and field.name[3]=='g' and field.name[4]=='s' and 
               (field.name[5]=='\0' or (field.name[5]=='2' and field.name[6]=='\0'))):
                continue

            if field.is_optional:
                if PyDict_Contains(value, <object>field.py_name):
                    field_value = value[<object>field.py_name]
                    if field.type == TL_TYPE_BOOL:
                        should_set_flag = field_value is True
                    else:
                        should_set_flag = field_value is not None
                        
                    if should_set_flag:
                        if field.flag_info.flags_index == 0:
                            flags |= (1 << field.flag_info.bit_position)
                        else:
                            flags2 |= (1 << field.flag_info.bit_position)

        self._write_int32(<int32_t>constructor.id)
        
        for i in range(constructor.field_count):
            field = &constructor.fields[i]
            if field.name[0]=='f' and field.name[1]=='l' and field.name[2]=='a' and field.name[3]=='g' and field.name[4]=='s':
                if field.name[5] == '\0':
                    self._write_int32(<int32_t>flags)
                    continue
                elif field.name[5] == '2' and field.name[6] == '\0':
                    self._write_int32(<int32_t>flags2)
                    continue
            
            if field.is_optional:
                if field.flag_info.flags_index == 0:
                    if not (flags & (1 << field.flag_info.bit_position)): continue
                else:
                    if not (flags2 & (1 << field.flag_info.bit_position)): continue
                if field.type == TL_TYPE_BOOL: continue
            
            if PyDict_Contains(value, <object>field.py_name):
                field_value = value[<object>field.py_name]
            elif field.is_optional:
                continue
            else:
                if field.type == TL_TYPE_INT or field.type == TL_TYPE_LONG: field_value = 0
                elif field.type == TL_TYPE_DOUBLE: field_value = 0.0
                elif field.type == TL_TYPE_STRING: field_value = ""
                elif field.type == TL_TYPE_BYTES: field_value = b""
                elif field.type == TL_TYPE_BOOL: field_value = False
                elif field.type == TL_TYPE_VECTOR: field_value = []
                elif field.type == TL_TYPE_OBJECT: field_value = {}
                else: field_value = None

            if field.is_optional and field_value is None: continue
            
            if field.type_name != NULL:
                type_name_bytes = PyBytes_FromString(field.type_name)
            else:
                type_name_bytes = None
            self._write_value(field_value, field.type, type_name_bytes)

    cdef void _write_value(self, object value, TLType field_type, object type_name=None):
        if field_type == TL_TYPE_INT: self._write_int32(<int32_t>value)
        elif field_type == TL_TYPE_STRING: self._write_string(<str>value)
        elif field_type == TL_TYPE_LONG: self._write_int64(<uint64_t>value)
        elif field_type == TL_TYPE_VECTOR: self._write_vector(value, type_name)
        elif field_type == TL_TYPE_OBJECT: self._write_object(value)
        elif field_type == TL_TYPE_DOUBLE: self._write_double(<double>value)
        elif field_type == TL_TYPE_BYTES: self._write_bytes(<bytes>value)
        elif field_type == TL_TYPE_BOOL: self._write_int32(1 if value else 0)
        else: raise ValueError(f"Unknown type: {field_type}")

    cdef void _write_vector(self, object vector, object type_name):
        cdef list vec_list = vector if isinstance(vector, list) else list(vector)
        cdef int count = <int>len(vec_list)
        cdef str elem_type_str
        cdef TLType elem_type = TL_TYPE_INT
        cdef bytes elem_type_bytes = None
        cdef int i

        if type_name is not None:
            elem_type_str = type_name.decode('utf-8').replace('Vector<', '').replace('>', '')
            elem_type = self._compiler._parse_type(elem_type_str)
            elem_type_bytes = elem_type_str.encode('utf-8')
            
        self._write_int32(0x1cb5c415)
        self._write_int32(count)
        for i in range(count):
            self._write_value(vec_list[i], elem_type, elem_type_bytes)

    cdef void _write_int32(self, int32_t value):
        self._ensure_buffer(4)
        memcpy(self._buffer + self._position, &value, 4)
        self._position += 4

    cdef void _write_int64(self, uint64_t value):
        self._ensure_buffer(8)
        memcpy(self._buffer + self._position, &value, 8)
        self._position += 8

    cdef void _write_double(self, double value):
        self._ensure_buffer(8)
        memcpy(self._buffer + self._position, &value, 8)
        self._position += 8

    cdef void _write_bytes(self, bytes data):
        cdef int length = <int>len(data)
        cdef int i, padding
        self._ensure_buffer(length + 16)
        if length < 254:
            self._buffer[self._position] = length
            self._position += 1
        else:
            self._buffer[self._position] = 254
            self._buffer[self._position + 1] = length & 0xff
            self._buffer[self._position + 2] = (length >> 8) & 0xff
            self._buffer[self._position + 3] = (length >> 16) & 0xff
            self._position += 4
        if length > 0:
            memcpy(self._buffer + self._position, <unsigned char*>data, length)
            self._position += length
        padding = (4 - (self._position % 4)) % 4
        for i in range(padding):
            self._buffer[self._position] = 0
            self._position += 1

    cdef void _write_string(self, str data):
        cdef bytes encoded = data.encode('utf-8')
        self._write_bytes(encoded)

    cdef void _ensure_buffer(self, size_t needed):
        if self._position + needed <= self._buffer_alloc_size: return
        cdef size_t new_size = self._buffer_alloc_size * 2
        while new_size < self._position + needed: new_size *= 2
        cdef unsigned char* new_buffer = <unsigned char*>realloc(self._buffer, new_size)
        if new_buffer == NULL: raise MemoryError("Cannot reallocate buffer")
        self._buffer = new_buffer
        self._buffer_alloc_size = new_size
