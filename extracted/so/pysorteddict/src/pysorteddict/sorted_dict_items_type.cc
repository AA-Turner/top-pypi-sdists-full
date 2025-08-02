#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <map>

#include "sorted_dict_items_type.hh"
#include "sorted_dict_type.hh"
#include "sorted_dict_view_type.hh"

static PyObject* iterator_to_object(std::map<PyObject*, SortedDictValue, SortedDictKeyCompare>::iterator it)
{
    return PyTuple_Pack(2, it->first, it->second.value);  // 🆕
}

int SortedDictItemsType::contains(PyObject* item)
{
    if (!PyTuple_Check(item) || PyTuple_GET_SIZE(item) != 2)
    {
        return 0;
    }
    PyObject* key = PyTuple_GET_ITEM(item, 0);
    PyObject* value = PyTuple_GET_ITEM(item, 1);
    return this->sd->contains(key, value);
}

PyObject* SortedDictItemsType::New(PyTypeObject* type, SortedDictType* sd)
{
    return SortedDictViewType::New(type, sd, ::iterator_to_object);
}
