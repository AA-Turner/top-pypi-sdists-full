#ifndef SORTED_DICT_KEYS_TYPE_HH_
#define SORTED_DICT_KEYS_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sorted_dict_view_type.hh"

struct SortedDictKeysIterType : public SortedDictViewIterType
{
public:
    static PyObject* New(PyTypeObject*, SortedDictType*);
};

struct SortedDictKeysType : public SortedDictViewType
{
public:
    int contains(PyObject*);
    static PyObject* New(PyTypeObject*, SortedDictType*);
};

#endif
