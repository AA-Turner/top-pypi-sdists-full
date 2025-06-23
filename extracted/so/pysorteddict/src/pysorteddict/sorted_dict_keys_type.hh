#ifndef SORTED_DICT_KEYS_TYPE_HH_
#define SORTED_DICT_KEYS_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sorted_dict_view_type.hh"

struct SortedDictKeysIterType : public SortedDictViewIterType
{
    PyObject* next(void);
};

struct SortedDictKeysType : public SortedDictViewType
{
    int contains(PyObject*);
};

#endif
