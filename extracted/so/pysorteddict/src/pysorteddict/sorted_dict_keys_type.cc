#define PY_SSIZE_T_CLEAN
#include <Python.h>

#include "sorted_dict_keys_type.hh"
#include "sorted_dict_view_type.hh"

PyObject* SortedDictKeysIterType::next(void)
{
    return Py_XNewRef(this->SortedDictViewIterType::next().first);  // 🆕
}

int SortedDictKeysType::contains(PyObject* key)
{
    return this->sd->contains(key);
}
