#ifndef SORTED_DICT_VALUES_TYPE_HH_
#define SORTED_DICT_VALUES_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sorted_dict_view_type.hh"

struct SortedDictValuesIterType : public SortedDictViewIterType
{
};

struct SortedDictValuesType : public SortedDictViewType
{
public:
    static PyObject* New(PyTypeObject*, SortedDictType*);
};

#endif
