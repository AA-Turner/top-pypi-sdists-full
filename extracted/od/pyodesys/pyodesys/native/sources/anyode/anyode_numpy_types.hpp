#pragma once

#include <numpy/arrayobject.h>
#include <stdint.h>

// Compile-time conversions to (integer-like) numpy TYPENUMs for the "Index_t" PyOdeSys<Real_t, Index_t>
template<typename T>
struct has_npy_index_type : std::false_type {
};

template<typename T>
struct npy_index_type {
    static_assert(has_npy_index_type<T>::value, "Cannot find associated numpy integer type for supplied Index_t");
};

template<>
struct npy_index_type<int8_t> {
    const static NPY_TYPES type_tag = NPY_INT8;
};

template<>
struct npy_index_type<int16_t> {
    const static NPY_TYPES type_tag = NPY_INT16;
};

template<>
struct npy_index_type<int32_t> {
    const static NPY_TYPES type_tag = NPY_INT32;
};

#ifdef INT64_MAX
template <>
struct npy_index_type<int64_t>
{
    const static NPY_TYPES type_tag = NPY_INT64;
};
#endif

// Compile-time conversions to (float-like) numpy TYPENUMs for the "Real_t" in PyOdeSys<Real_t, Index_t>
template<typename T>
struct has_npy_real_type : std::false_type {
};

template<typename T>
struct npy_real_type {
    static_assert(has_npy_real_type<T>::value, "Cannot find associated numpy float type for supplied Real_t");
};

template<>
struct npy_real_type<float> {
    const static NPY_TYPES type_tag = NPY_FLOAT;
};

template<>
struct npy_real_type<double> {
    const static NPY_TYPES type_tag = NPY_DOUBLE;
};

template<>
struct npy_real_type<long double> {
    const static NPY_TYPES type_tag = NPY_LONGDOUBLE;
};
