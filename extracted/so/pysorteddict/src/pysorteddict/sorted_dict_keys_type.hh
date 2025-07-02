#ifndef SORTED_DICT_KEYS_TYPE_HH_
#define SORTED_DICT_KEYS_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sorted_dict_view_type.hh"

struct SortedDictKeysIterType : public SortedDictViewIterType
{
public:
    PyObject* next(void);
};

struct SortedDictKeysType : public SortedDictViewType
{
private:
    PyObject* getitem(Py_ssize_t);
    PyObject* getitem(Py_ssize_t, Py_ssize_t, Py_ssize_t);

public:
    int contains(PyObject*);
    PyObject* getitem(PyObject*);
};

#endif
