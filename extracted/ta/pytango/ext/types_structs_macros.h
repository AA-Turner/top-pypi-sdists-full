/*
 * SPDX-FileCopyrightText: All Contributors to the PyTango project
 *
 * SPDX-License-Identifier: LGPL-3.0-or-later
 */

#pragma once

#include "common_header.h"

namespace Tango {
typedef std::vector<DbHistory> DbHistoryList;

/*
 * I know it is weird, but:
 *
 * Due to commands have array type constant, while attributes element type constant + data format,
 * but we want to process them with the same code we have to do chain
 * element type constant -> array type constant -> array + data types
 *
 * To do it we have to have symmetry: to each element type constant must exist array type constant,
 * but for DEV_UCHAR and DEV_ENUM it is not the case (even Tango can process arrays of these data type)
 *
 * So either I have to do a lot of methods overloading and code splitting,
 * or I just FAKE these absent array type constant, to let macro compile.
 *
 * I know, it super weird, but: 4 lines of code here saves us ~300 lines in convertors and remove 4 code duplications
 *
 * */
static const int FAKED_UCHARARRAY = 101;
static const int FAKED_ENUMARRAY = 102;
} // namespace Tango

template <int N>
struct tango_name2type {
};

template <typename T>
struct tango_type2name {
    enum e_tango_type2name {
    };
};

template <int N>
struct tango_name2arraytype {
};

template <int N>
struct tango_name2arrayname {
    enum e_tango_name2arrayname {
    };
};

template <int N>
struct tango_name2scalarname {
    enum e_tango_name2scalarname {
    };
};

#define DEF_TANGO_SCALAR_ARRAY_NAMES(scalarname, arrayname) \
    template <>                                             \
    struct tango_name2arrayname<Tango::scalarname> {        \
        enum e_tango_name2arrayname {                       \
            value = Tango::arrayname                        \
        };                                                  \
    };                                                      \
    template <>                                             \
    struct tango_name2scalarname<Tango::arrayname> {        \
        enum e_tango_name2scalarname {                      \
            value = Tango::scalarname                       \
        };                                                  \
    };

#define DEF_TANGO_NAME2TYPE__(tangoname, tangotype) \
    template <>                                     \
    struct tango_name2type<Tango::tangoname> {      \
        typedef tangotype Type;                     \
    };

#define DEF_TANGO_TYPE2NAME__(tangotype, tangoname) \
    template <>                                     \
    struct tango_type2name<tangotype> {             \
        enum e_tango_type2name {                    \
            value = Tango::tangoname                \
        };                                          \
    };

#define DEF_TANGO_NAME2TYPE(tangoname, tangotype) \
    DEF_TANGO_NAME2TYPE__(tangoname, tangotype)   \
    DEF_TANGO_TYPE2NAME__(tangotype, tangoname)

#define DEF_TANGO_NAME2ARRAY(tangoname, tangotype, elementtype) \
    template <>                                                 \
    struct tango_name2arraytype<Tango::tangoname> {             \
        typedef tangotype Type;                                 \
        typedef elementtype ElementsType;                       \
    };

#define TSD_SIMPLE__(tangoname, eltangotype, arraytangotype) \
    DEF_TANGO_NAME2TYPE(tangoname, eltangotype)              \
    DEF_TANGO_NAME2ARRAY(tangoname, arraytangotype, eltangotype)

#define TSD_ARRAY__(tangoname, eltangotype, arraytangotype) \
    DEF_TANGO_NAME2TYPE(tangoname, arraytangotype)          \
    DEF_TANGO_NAME2ARRAY(tangoname, void, eltangotype)

TSD_SIMPLE__(DEV_SHORT, Tango::DevShort, Tango::DevVarShortArray)
TSD_SIMPLE__(DEV_LONG, Tango::DevLong, Tango::DevVarLongArray)
TSD_SIMPLE__(DEV_DOUBLE, Tango::DevDouble, Tango::DevVarDoubleArray)
TSD_SIMPLE__(DEV_STRING, Tango::DevString, Tango::DevVarStringArray)
TSD_SIMPLE__(DEV_FLOAT, Tango::DevFloat, Tango::DevVarFloatArray)
TSD_SIMPLE__(DEV_BOOLEAN, Tango::DevBoolean, Tango::DevVarBooleanArray)
TSD_SIMPLE__(DEV_USHORT, Tango::DevUShort, Tango::DevVarUShortArray)
TSD_SIMPLE__(DEV_ULONG, Tango::DevULong, Tango::DevVarULongArray)
TSD_SIMPLE__(DEV_UCHAR, Tango::DevUChar, Tango::DevVarUCharArray)
TSD_SIMPLE__(DEV_LONG64, Tango::DevLong64, Tango::DevVarLong64Array)
TSD_SIMPLE__(DEV_ULONG64, Tango::DevULong64, Tango::DevVarULong64Array)
TSD_SIMPLE__(DEV_STATE, Tango::DevState, Tango::DevVarStateArray)
TSD_SIMPLE__(DEV_ENCODED, Tango::DevEncoded, Tango::DevVarEncodedArray)

// since enum type is implemented as a short we cannot use tango_type2name because
// it will conflict with the DevShort template declaration
DEF_TANGO_NAME2TYPE__(DEV_ENUM, Tango::DevEnum)
DEF_TANGO_NAME2ARRAY(DEV_ENUM, Tango::DevVarShortArray, Tango::DevEnum)

TSD_SIMPLE__(DEV_VOID, void, void)

TSD_ARRAY__(DEVVAR_CHARARRAY, _CORBA_Octet, Tango::DevVarCharArray)
TSD_ARRAY__(DEVVAR_SHORTARRAY, Tango::DevShort, Tango::DevVarShortArray)
TSD_ARRAY__(DEVVAR_LONGARRAY, Tango::DevLong, Tango::DevVarLongArray)
TSD_ARRAY__(DEVVAR_FLOATARRAY, Tango::DevFloat, Tango::DevVarFloatArray)
TSD_ARRAY__(DEVVAR_DOUBLEARRAY, Tango::DevDouble, Tango::DevVarDoubleArray)
TSD_ARRAY__(DEVVAR_USHORTARRAY, Tango::DevUShort, Tango::DevVarUShortArray)
TSD_ARRAY__(DEVVAR_ULONGARRAY, Tango::DevULong, Tango::DevVarULongArray)
TSD_ARRAY__(DEVVAR_STRINGARRAY, Tango::DevString, Tango::DevVarStringArray)
TSD_ARRAY__(DEVVAR_LONGSTRINGARRAY, void, Tango::DevVarLongStringArray)
TSD_ARRAY__(DEVVAR_DOUBLESTRINGARRAY, void, Tango::DevVarDoubleStringArray)
TSD_ARRAY__(DEVVAR_BOOLEANARRAY, Tango::DevBoolean, Tango::DevVarBooleanArray)
TSD_ARRAY__(DEVVAR_LONG64ARRAY, Tango::DevLong64, Tango::DevVarLong64Array)
TSD_ARRAY__(DEVVAR_ULONG64ARRAY, Tango::DevULong64, Tango::DevVarULong64Array)
TSD_ARRAY__(DEVVAR_STATEARRAY, Tango::DevState, Tango::DevVarStateArray)

/*
 * Note: Here we use FAKED_UCHARARRAY and FAKED_ENUMARRAY constants, just to compile macro. Look above
 * */
DEF_TANGO_NAME2TYPE__(FAKED_UCHARARRAY, Tango::DevVarUCharArray)
DEF_TANGO_NAME2ARRAY(FAKED_UCHARARRAY, void, Tango::DevUChar)

DEF_TANGO_NAME2TYPE__(FAKED_ENUMARRAY, Tango::DevVarShortArray)
DEF_TANGO_NAME2ARRAY(FAKED_ENUMARRAY, void, Tango::DevEnum)

DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_SHORT, DEVVAR_SHORTARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_LONG, DEVVAR_LONGARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_DOUBLE, DEVVAR_DOUBLEARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_STRING, DEVVAR_STRINGARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_FLOAT, DEVVAR_FLOATARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_BOOLEAN, DEVVAR_BOOLEANARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_USHORT, DEVVAR_USHORTARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_ULONG, DEVVAR_ULONGARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_LONG64, DEVVAR_LONG64ARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_ULONG64, DEVVAR_ULONG64ARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_STATE, DEVVAR_STATEARRAY)
// DEF_TANGO_SCALAR_ARRAY_NAMES( DEV_ENCODED, DEVVAR_ENCODEDARRAY )
// DEF_TANGO_SCALAR_ARRAY_NAMES( DEV_,        DEVVAR_LONGSTRINGARRAY )
// DEF_TANGO_SCALAR_ARRAY_NAMES( DEV_,        DEVVAR_DOUBLESTRINGARRAY )

/*
 * Note: Here we use FAKED_UCHARARRAY and FAKED_ENUMARRAY constants, just to compile macro. Look above
 * */
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_UCHAR, FAKED_UCHARARRAY)
DEF_TANGO_SCALAR_ARRAY_NAMES(DEV_ENUM, FAKED_ENUMARRAY)

#define TANGO_type2const(type) tango_type2name<type>::value
#define TANGO_const2type(name) tango_name2type<name>::Type
#define TANGO_const2arraytype(name) tango_name2arraytype<name>::Type
#define TANGO_const2arrayelementstype(name) tango_name2arraytype<name>::ElementsType
#define TANGO_type2arraytype(type) TANGO_const2arraytype(TANGO_type2const(type))
#define TANGO_const2string(name) (Tango::CmdArgTypeName[name])

#define TANGO_const2arrayconst(scalarconst) tango_name2arrayname<scalarconst>::value
#define TANGO_const2scalarconst(arrayconst) tango_name2scalarname<arrayconst>::value
#define TANGO_const2scalartype TANGO_const2arrayelementstype

/// @name Conversion from a Tango scalar type name to the numpy equivalent name
/// @{

#define TANGO_const2numpy(tangoid) tango_name2numpy<tangoid>::value

template <int N>
struct tango_name2numpy {
    enum e_tango_name2numpy {
    };
};

#define DEF_TANGO2NUMPY(tangoid, numpyid) \
    template <>                           \
    struct tango_name2numpy<tangoid> {    \
        enum e_tango_name2numpy {         \
            value = numpyid               \
        };                                \
    };

DEF_TANGO2NUMPY(Tango::DEV_STATE, NPY_UINT32)
DEF_TANGO2NUMPY(Tango::DEV_SHORT, NPY_INT16)
DEF_TANGO2NUMPY(Tango::DEV_LONG, NPY_INT32)
DEF_TANGO2NUMPY(Tango::DEV_DOUBLE, NPY_FLOAT64)
DEF_TANGO2NUMPY(Tango::DEV_FLOAT, NPY_FLOAT32)
DEF_TANGO2NUMPY(Tango::DEV_BOOLEAN, NPY_BOOL)
DEF_TANGO2NUMPY(Tango::DEV_USHORT, NPY_UINT16)
DEF_TANGO2NUMPY(Tango::DEV_ULONG, NPY_UINT32)
// Unassigned Tango::DEV_STRING, mapping to NPY_STRING is not copy-free
DEF_TANGO2NUMPY(Tango::DEV_UCHAR, NPY_UBYTE)
// Unassigned: Tango::DEV_ENCODED
DEF_TANGO2NUMPY(Tango::DEV_LONG64, NPY_INT64)
DEF_TANGO2NUMPY(Tango::DEV_ULONG64, NPY_UINT64)
DEF_TANGO2NUMPY(Tango::DEV_ENUM, NPY_INT16)

/// @name Conversion from a Tango array type name to the scalar numpy name
/// For types like DEVVAR_DOUBLEARRAY. This is ended with ARRAY, except
/// DEVVAR_LONGSTRINGARRAY, DEVVAR_DOUBLESTRINGARRAY and DEVVAR_STRINGARRAY
/// @{

#define TANGO_const2scalarnumpy(tangoid) tango_name2scalarnumpy<tangoid>::value

// We can use TANGO_const2scalarconst which gives us the equivalence
// except for DEVVAR_CHARARRAY, that does not have any Scalar type
// equivalent.
template <int N>
struct tango_name2scalarnumpy {
    enum {
        value = TANGO_const2numpy(TANGO_const2scalarconst(N))
    };
};

template <>
struct tango_name2scalarnumpy<Tango::DEVVAR_CHARARRAY> {
    enum {
        value = NPY_UBYTE
    };
};

/// @}

#define __TANGO_DEPEND_ON_TYPE_AUX_ID(typename_, DOIT)      \
    case Tango::typename_: {                                \
        static const int tangoTypeConst = Tango::typename_; \
        DOIT;                                               \
        break;                                              \
    }

#define __TANGO_DEPEND_ON_TYPE_AUX_NAME(tid_, DOIT)      \
    case Tango::tid_: {                                  \
        typedef TANGO_const2type(Tango::tid_) TangoType; \
        DOIT;                                            \
        break;                                           \
    }

#define TANGO_DO_ON_ATTRIBUTE_DATA_TYPE_ID(tid, DOIT)        \
    if(true) {                                               \
        switch(tid) {                                        \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_SHORT, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_LONG, DOIT)    \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_DOUBLE, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_STRING, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_FLOAT, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_BOOLEAN, DOIT) \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_USHORT, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ULONG, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_UCHAR, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_LONG64, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ULONG64, DOIT) \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_STATE, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ENCODED, DOIT) \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ENUM, DOIT)    \
        default:                                             \
            assert(false);                                   \
        }                                                    \
    } else                                                   \
        (void) 0

#define TANGO_DO_ON_ATTRIBUTE_DATA_TYPE_NAME(tid, DOIT)        \
    if(true) {                                                 \
        switch(tid) {                                          \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_SHORT, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_LONG, DOIT)    \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_DOUBLE, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_STRING, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_FLOAT, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_BOOLEAN, DOIT) \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_USHORT, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ULONG, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_UCHAR, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_LONG64, DOIT)  \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ULONG64, DOIT) \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_STATE, DOIT)   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ENCODED, DOIT) \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ENUM, DOIT)    \
        default:                                               \
            assert(false);                                     \
        }                                                      \
    } else                                                     \
        (void) 0

#define TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_ID(tid, fn, ...) \
    TANGO_DO_ON_ATTRIBUTE_DATA_TYPE_ID(tid, fn<tangoTypeConst>(__VA_ARGS__))

#define TANGO_CALL_ON_ATTRIBUTE_DATA_TYPE_NAME(tid, fn, ...) \
    TANGO_DO_ON_ATTRIBUTE_DATA_TYPE_NAME(tid, fn<TangoType>(__VA_ARGS__))

#define TANGO_DO_ON_DEVICE_DATA_TYPE_ID(tid, DOIT_SCALAR, DOIT_ARRAY)                 \
    if(true) {                                                                        \
        switch(tid) {                                                                 \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_VOID, DOIT_SCALAR)                      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_BOOLEAN, DOIT_SCALAR)                   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_SHORT, DOIT_SCALAR)                     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_LONG, DOIT_SCALAR)                      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_FLOAT, DOIT_SCALAR)                     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_DOUBLE, DOIT_SCALAR)                    \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_USHORT, DOIT_SCALAR)                    \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ULONG, DOIT_SCALAR)                     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_STRING, DOIT_SCALAR)                    \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_STATE, DOIT_SCALAR)                     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_CHARARRAY, DOIT_ARRAY)               \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_SHORTARRAY, DOIT_ARRAY)              \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_LONGARRAY, DOIT_ARRAY)               \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_FLOATARRAY, DOIT_ARRAY)              \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_DOUBLEARRAY, DOIT_ARRAY)             \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_USHORTARRAY, DOIT_ARRAY)             \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_ULONGARRAY, DOIT_ARRAY)              \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_STRINGARRAY, DOIT_ARRAY)             \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_LONGSTRINGARRAY, DOIT_ARRAY)         \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_DOUBLESTRINGARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_STATEARRAY, DOIT_ARRAY)              \
            /*        __TANGO_DEPEND_ON_TYPE_AUX_ID(CONST_DEV_STRING, DOIT_SCALAR) */ \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_BOOLEANARRAY, DOIT_ARRAY)            \
            /*        __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_UCHAR, DOIT_SCALAR)*/         \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_LONG64, DOIT_SCALAR)                    \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ULONG64, DOIT_SCALAR)                   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_LONG64ARRAY, DOIT_ARRAY)             \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_ULONG64ARRAY, DOIT_ARRAY)            \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ENCODED, DOIT_SCALAR)                   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ENUM, DOIT_SCALAR)                      \
        default:                                                                      \
            assert(false);                                                            \
        }                                                                             \
    } else                                                                            \
        (void) 0

#define TANGO_DO_ON_DEVICE_ARRAY_DATA_TYPE_ID(tid, DOIT_ARRAY)                  \
    if(true) {                                                                  \
        switch(tid) {                                                           \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_CHARARRAY, DOIT_ARRAY)         \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_SHORTARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_LONGARRAY, DOIT_ARRAY)         \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_FLOATARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_DOUBLEARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_USHORTARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_ULONGARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_STRINGARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_LONGSTRINGARRAY, DOIT_ARRAY)   \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_DOUBLESTRINGARRAY, DOIT_ARRAY) \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_BOOLEANARRAY, DOIT_ARRAY)      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_LONG64ARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_ULONG64ARRAY, DOIT_ARRAY)      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_STATEARRAY, DOIT_ARRAY)        \
        default:                                                                \
            assert(false);                                                      \
        }                                                                       \
    } else                                                                      \
        (void) 0

#define TANGO_DO_ON_DEVICE_DATA_TYPE_NAME(tid, DOIT_SIMPLE, DOIT_ARRAY)           \
    if(true) {                                                                    \
        switch(tid) {                                                             \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_VOID, DOIT_SIMPLE)                \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_BOOLEAN, DOIT_SIMPLE)             \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_SHORT, DOIT_SIMPLE)               \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_LONG, DOIT_SIMPLE)                \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_FLOAT, DOIT_SIMPLE)               \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_DOUBLE, DOIT_SIMPLE)              \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_USHORT, DOIT_SIMPLE)              \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ULONG, DOIT_SIMPLE)               \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_STRING, DOIT_SIMPLE)              \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_CHARARRAY, DOIT_ARRAY)         \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_SHORTARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_LONGARRAY, DOIT_ARRAY)         \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_FLOATARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_DOUBLEARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_USHORTARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_ULONGARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_STRINGARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_LONGSTRINGARRAY, DOIT_ARRAY)   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_DOUBLESTRINGARRAY, DOIT_ARRAY) \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_STATE, DOIT_SIMPLE)               \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_STATEARRAY, DOIT_ARRAY)        \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEVVAR_BOOLEANARRAY, DOIT_ARRAY)        \
            /*        __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_UCHAR, DOIT_SIMPLE)*/   \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_LONG64, DOIT_SIMPLE)              \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ULONG64, DOIT_SIMPLE)             \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_LONG64ARRAY, DOIT_ARRAY)       \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEVVAR_ULONG64ARRAY, DOIT_ARRAY)      \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ENCODED, DOIT_SIMPLE)             \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ENUM, DOIT_SIMPLE)                \
        default:                                                                  \
            assert(false);                                                        \
        }                                                                         \
    } else                                                                        \
        (void) 0

#define TANGO_CALL_ON_DEVICE_DATA_TYPE_ID(tid, fn_simple, fn_array, ...) \
    TANGO_DO_ON_DEVICE_DATA_TYPE_ID(tid, fn_simple<tangoTypeConst>(__VA_ARGS__), fn_array<tangoTypeConst>(__VA_ARGS__))

#define TANGO_CALL_ON_DEVICE_DATA_TYPE_NAME(tid, fn_simple, fn_array, ...) \
    TANGO_DO_ON_DEVICE_DATA_TYPE_NAME(tid, fn_simple<TangoType>(__VA_ARGS__), fn_array<TangoType>(__VA_ARGS__))

#define TANGO_DO_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE_ID(tid, DOIT) \
    if(true) {                                                  \
        switch(tid) {                                           \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_SHORT, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_LONG, DOIT)       \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_DOUBLE, DOIT)     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_FLOAT, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_USHORT, DOIT)     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ULONG, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_UCHAR, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_LONG64, DOIT)     \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ULONG64, DOIT)    \
            __TANGO_DEPEND_ON_TYPE_AUX_ID(DEV_ENUM, DOIT)       \
        default:                                                \
            assert(false);                                      \
        }                                                       \
    } else                                                      \
        (void) 0

#define TANGO_DO_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE_NAME(tid, DOIT) \
    if(true) {                                                    \
        switch(tid) {                                             \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_SHORT, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_LONG, DOIT)       \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_DOUBLE, DOIT)     \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_FLOAT, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_USHORT, DOIT)     \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ULONG, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_UCHAR, DOIT)      \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_LONG64, DOIT)     \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ULONG64, DOIT)    \
            __TANGO_DEPEND_ON_TYPE_AUX_NAME(DEV_ENUM, DOIT)       \
        default:                                                  \
            assert(false);                                        \
        }                                                         \
    } else                                                        \
        (void) 0

#define TANGO_CALL_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE_ID(tid, fn, ...) \
    TANGO_DO_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE_ID(tid, fn<tangoTypeConst>(__VA_ARGS__))

#define TANGO_CALL_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE_NAME(tid, fn, ...) \
    TANGO_DO_ON_NUMERICAL_ATTRIBUTE_DATA_TYPE_NAME(tid, fn<tangoTypeConst>(__VA_ARGS__))
