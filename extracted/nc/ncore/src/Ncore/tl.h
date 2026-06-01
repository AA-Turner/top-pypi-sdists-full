// Copyright 2026 zovdev
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.


#ifndef TL_DEFS_H
#define TL_DEFS_H

#include <stdint.h>
#include <Python.h>

typedef enum {
    TL_TYPE_INT = 0,
    TL_TYPE_LONG,
    TL_TYPE_DOUBLE,
    TL_TYPE_STRING,
    TL_TYPE_BYTES,
    TL_TYPE_BOOL,
    TL_TYPE_VECTOR,
    TL_TYPE_OBJECT
} TLType;

typedef struct {
    int bit_position;
    int flags_index;
    char* name;
} TLOptionalFlag;

typedef struct {
    char* name;
    PyObject* py_name;
    TLType type;
    char* type_name;
    int is_optional;
    TLOptionalFlag flag_info;
    int is_generic;
} TLField;

typedef struct {
    uint32_t id;
    char* name;
    char* type;
    TLField* fields;
    int field_count;
    int has_flags;
    int has_flags2;
} TLConstructor;

typedef struct {
    TLConstructor* constructors;
    int constructor_count;
} TLSchema;

#endif
