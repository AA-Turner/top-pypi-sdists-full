#ifndef SORTED_DICT_VIEW_TYPE_HH_
#define SORTED_DICT_VIEW_TYPE_HH_

#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>

#include "sorted_dict_type.hh"

using IteratorToObject = PyObject* (*)(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator);

struct SortedDictViewIterType
{
public:
    PyObject_HEAD;

protected:
    SortedDictType* sd;
    std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator it;
    bool should_raise_stop_iteration;

    // See below for why this is required.
    IteratorToObject iterator_to_object;

private:
    void track(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator);
    void untrack(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator);

public:
    static void Delete(PyObject*);
    PyObject* next(void);
    static PyObject* New(PyTypeObject*, SortedDictType*, IteratorToObject);
};

struct SortedDictViewType
{
public:
    PyObject_HEAD;

protected:
    SortedDictType* sd;

    // To mimic dynamic dispatch. Child classes should provide this function,
    // which should convert a C++ iterator into a Python object. Using C++
    // virtual functions would require constructing instances the C++ way, but
    // C++ constructors won't know how to initialise the Python-specific
    // members. The default memory allocator provided by Python (which does
    // initialise Python-specific members) does not run constructors.
    IteratorToObject iterator_to_object;

private:
    PyObject* getitem(Py_ssize_t);
    PyObject* getitem(Py_ssize_t, Py_ssize_t, Py_ssize_t);

public:
    static void Delete(PyObject*);
    static PyObject* repr(PyObject*);
    Py_ssize_t len(void);
    PyObject* getitem(PyObject*);
    PyObject* iter(PyTypeObject*);
    static PyObject* New(PyTypeObject*, SortedDictType*, IteratorToObject);
};

#endif
