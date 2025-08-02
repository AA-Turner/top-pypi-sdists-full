#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>

#include "sorted_dict_keys_type.hh"
#include "sorted_dict_type.hh"
#include "sorted_dict_view_type.hh"

static PyObject* iterator_to_object(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator it)
{
    return Py_NewRef(it->first);  // 🆕
}

PyObject* SortedDictKeysIterType::New(PyTypeObject* type, SortedDictType* sd)
{
    return SortedDictViewIterType::New(type, sd, ::iterator_to_object);
}

int SortedDictKeysType::contains(PyObject* key)
{
    return this->sd->contains(key);
}

PyObject* SortedDictKeysType::New(PyTypeObject* type, SortedDictType* sd)
{
    return SortedDictViewType::New(type, sd, ::iterator_to_object);
}
